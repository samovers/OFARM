#!/usr/bin/env python3
"""Offline supplied-byte comparisons. Never a full domain or admission verdict."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
import tempfile
import types
from collections import Counter
from pathlib import Path

DEPENDENCY_ERROR = None
try:
    import rfc8785
    from jsonschema import Draft202012Validator, FormatChecker
    from referencing import Registry, Resource
    from referencing.exceptions import NoSuchResource
except ImportError as error:
    DEPENDENCY_ERROR = error.name or 'pythonDependencies'

ROOT = Path(__file__).resolve().parents[2]
DIRECTORY = '03_machine_contracts/drafts_non_default/assertion_record_submission/domain_validation/'
MANIFEST = DIRECTORY + 'ASSERTION_RECORD_DOMAIN_MAPPING_manifest_v0_1.json'
MANIFEST_SHA256 = '79f81c58aff8e920e20b90772cdef04c931f8645086afac56a2d0c656b820b64'
CASES = '04_implementation_and_conformance/examples_and_fixtures/fixtures/machine_contracts/OFARM_AssertionRecord_domain_mapping_cases_v0_1.json'


class MappingError(ValueError):
    def __init__(self, layer, code, target, witness=None):
        super().__init__(code)
        self.layer, self.code, self.target, self.witness = layer, code, target, witness

    def as_dict(self):
        error = {'layer': self.layer, 'code': self.code, 'target': self.target}
        if self.witness is not None:
            error['schemaError'] = self.witness
        # Preflight failures deliberately have no claimed digests/comparisons.
        return {'componentResult': 'UNAVAILABLE', 'fullDomainValidation': 'UNAVAILABLE', 'error': error}


def file_bytes(path, target):
    try:
        return path.read_bytes()
    except OSError as error:
        raise MappingError('DEPENDENCY', 'FILE_UNAVAILABLE', target) from error


def value_digest(value):
    try:
        return 'sha256:' + hashlib.sha256(rfc8785.dumps(value)).hexdigest()
    except (rfc8785.CanonicalizationError, UnicodeError) as error:
        raise MappingError('CANONICAL', 'CANONICAL_DOMAIN', 'input') from error


def schema_check(validator, value, target):
    errors = list(validator.iter_errors(value))
    if errors:
        error = errors[0]
        raise MappingError('SCHEMA', 'SCHEMA', target, {
            'instancePath': list(error.absolute_path),
            'schemaPath': list(error.absolute_schema_path),
            'keyword': error.validator or 'falseSchema',
        })


class Component:
    """One immutable, hash-checked component load; verify accepts UTF-8 bytes."""
    def __init__(self, root=ROOT):
        if DEPENDENCY_ERROR is not None:
            raise MappingError('DEPENDENCY', 'LIBRARY_UNAVAILABLE', DEPENDENCY_ERROR)
        self.root = Path(root)
        raw = file_bytes(self.root / MANIFEST, 'manifest')
        if hashlib.sha256(raw).hexdigest() != MANIFEST_SHA256:
            raise MappingError('DEPENDENCY', 'ARTIFACT_DIGEST', 'manifest')
        self.manifest = json.loads(raw)
        self.raw, self.pins = {}, {}
        for pin in self.manifest['artifacts']:
            role = pin['role']
            raw = file_bytes(self.root / pin['path'], role)
            if len(raw) != pin['bytes'] or hashlib.sha256(raw).hexdigest() != pin['sha256']:
                raise MappingError('DEPENDENCY', 'ARTIFACT_DIGEST', role)
            self.raw[role], self.pins[role] = raw, pin
        # Execute only already hash-verified prior helper bytes. Their standalone
        # test mains do not run; supply the imports those mains normally install.
        support = {}
        for role in ('intentSupport', 'resultSupport'):
            module = types.ModuleType('_operation_mapping_' + role)
            module.__dict__.update(__file__=str(self.root / self.pins[role]['path']),
                                   rfc8785=rfc8785, Draft202012Validator=Draft202012Validator,
                                   FormatChecker=FormatChecker, Registry=Registry,
                                   Resource=Resource, NoSuchResource=NoSuchResource)
            exec(compile(self.raw[role], module.__file__, 'exec'), module.__dict__)
            support[role] = module
        self.intent_support, self.result_support = support['intentSupport'], support['resultSupport']
        artifact_pins = [{'path': p['path'], 'sha256': p['sha256'], 'kind': 'schema',
                          'schemaId': p['schemaId']} for p in self.manifest['artifacts'] if p['role'].endswith('Schema')]
        try:
            artifacts, registry = self.intent_support.load_artifacts(self.root, artifact_pins)
        except self.intent_support.CheckError as error:
            raise MappingError('DEPENDENCY', error.code, 'schemaRegistry') from error
        self.schemas = {role: artifacts[pin['path']] for role, pin in self.pins.items() if role.endswith('Schema')}
        formats = FormatChecker()
        self.validators = {role: Draft202012Validator(schema, registry=registry, format_checker=formats)
                           for role, schema in self.schemas.items()}
        self.body_validator = Draft202012Validator(
            {'$ref': self.pins['resultSchema']['schemaId'] + '#' + self.manifest['selectedBodyFragment']},
            registry=registry, format_checker=formats)

    def decode(self, raw, target):
        try:
            if not isinstance(raw, bytes):
                raise MappingError('JSON', 'INPUT_BYTES_REQUIRED', target)
            text = raw.decode('utf-8')
            if text.startswith('\ufeff'):
                raise MappingError('JSON', 'UTF8_BOM', target)
            try:
                value = self.intent_support.strict_loads(text)
            except self.intent_support.CheckError:
                raise
            except ValueError as error:
                # The JSON parser can reject a value before an object exists
                # (for example Python's protective integer digit limit).
                raise MappingError('JSON', 'PARSER_VALUE_REJECTED', target) from error
            value_digest(value)  # Reject non-interoperable values before any schema claim.
            return value
        except self.intent_support.CheckError as error:
            raise MappingError(error.layer, error.code, target) from error
        except MappingError as error:
            error.target = target
            raise
        except (UnicodeError, RecursionError) as error:
            raise MappingError('JSON', 'INVALID_JSON', target) from error

    def binding(self, role, version, fragment=''):
        return {'schemaRef': self.pins[role]['schemaId'] + fragment, 'schemaVersion': version,
                'schemaDigest': 'sha256:' + self.pins[role]['sha256'],
                'canonicalization': 'JCS_RFC8785_SHA256'}

    def verify(self, intent_bytes, result_bytes):
        """Return a schema-validated MATCH/MISMATCH report, or raise MappingError."""
        intent, result = self.decode(intent_bytes, 'intent'), self.decode(result_bytes, 'result')
        for target, role, value in [('intent', 'intentSchema', intent), ('result', 'resultSchema', result)]:
            schema_check(self.validators[role], value, target)
        schema_check(self.body_validator, result['assertionBody'], 'resultBody')
        for target, support, profile, value in (
            ('intent', self.intent_support, 'EI_OPERATION_ASSERTION_V0_2', intent),
            ('result', self.result_support, 'assertionRecord', result),
        ):
            try:
                support.check_component(profile, value)
            except (self.intent_support.CheckError, self.result_support.ContractError) as error:
                raise MappingError('LOCAL_CONSISTENCY', error.code, target) from error
            except (ValueError, OverflowError) as error:
                raise MappingError('LOCAL_CONSISTENCY', 'INVALID_LOCAL_VALUE', target) from error

        def optional(value, pointer):
            try:
                return True, self.intent_support.pointer(value, pointer)
            except self.intent_support.CheckError as error:
                if error.code == 'POINTER_MISSING':
                    return False, None
                raise

        checks, by_id = [], {}
        for row in self.manifest['mappings']:
            item = {'id': row['subcheckId']}
            mode = row['mode']
            if mode in ('reuse_schema_and_comparison', 'coverage_reference'):
                item.update(outcome=by_id[row['comparisonRef']]['outcome'], evidenceRef=row['comparisonRef'])
            elif mode == 'reuse_schema_validation_evidence':
                item.update(outcome='MATCH', evidenceRef='schemaValidation')
            else:
                if mode == 'source_fixed_constant':
                    source_present, source = True, row['expectedValue']
                    item['sourcePointer'] = 'PR23/7.2/ASSERT_OPERATION_CLAIM/assertionType'
                else:
                    source_present, source = optional(intent, row['sourcePointer'])
                    item['sourcePointer'] = row['sourcePointer']
                result_present, destination = optional(result, row['resultPointer'])
                item.update(resultPointer=row['resultPointer'], sourcePresent=source_present,
                            resultPresent=result_present)
                if source_present:
                    item['sourceDigest'] = value_digest(source)
                if result_present:
                    item['resultDigest'] = value_digest(destination)
                match = (source_present == result_present and
                         (not source_present or item['sourceDigest'] == item['resultDigest']))
                if mode != 'exact_copy_or_symmetric_absence' and not source_present:
                    match = False
                item['outcome'] = 'MATCH' if match else 'MISMATCH'
            checks.append(item)
            by_id[item['id']] = item
        report = {
            'schemaVersion': 'ofarm.assertionrecord.operationmappingreport.v0.1',
            'componentResult': 'MATCH' if all(c['outcome'] == 'MATCH' for c in checks) else 'MISMATCH',
            'fullDomainValidation': 'UNAVAILABLE',
            'inputDigest': value_digest(intent), 'resultDigest': value_digest(result),
            'inputSchemaBinding': self.binding('intentSchema', 'ofarm.operationassertioneffectintent.v0.2'),
            'resultSchemaBinding': self.binding('resultSchema', 'ofarm.assertionrecord.v0.2'),
            'selectedBodySchemaBinding': self.binding('resultSchema', 'ofarm.assertionrecord.v0.2',
                                                     '#' + self.manifest['selectedBodyFragment']),
            'schemaValidation': {'intent': True, 'result': True, 'resultBody': True},
            'localConsistency': {'intent': True, 'result': True},
            'checks': checks, 'unavailable': self.manifest['unavailable'],
        }
        schema_check(self.validators['reportSchema'], report, 'report')
        return report


def verify(intent_bytes, result_bytes, *, root=ROOT):
    """Convenience library entry point. Each call verifies fresh component bytes."""
    return Component(root).verify(intent_bytes, result_bytes)


def run_cases(root=ROOT, path=None):
    """Fixture expectations are explicit, independently authored outcomes."""
    root = Path(root)
    data = json.loads(file_bytes(Path(path) if path else root / CASES, 'cases'))
    component = Component(root)
    if len({c['name'] for c in data['cases']}) != len(data['cases']):
        raise MappingError('HARNESS', 'DUPLICATE_CASE_NAME', 'cases')
    counts, failures, evidence = Counter(), [], []
    for case in data['cases']:
        try:
            pair = copy.deepcopy(data['pairs'][case.get('pair', 'intended')])
            for target in ('intent', 'result'):
                pair[target] = component.intent_support.changed(pair[target], case.get(target + 'Edits', []))
            raw = {target: json.dumps(pair[target], ensure_ascii=False).encode() for target in ('intent', 'result')}
            for target in ('intent', 'result'):
                if target + 'Raw' in case:
                    raw[target] = case[target + 'Raw'].encode()
            if 'dependency' in case:
                with tempfile.TemporaryDirectory(prefix='ofarm-mapping-case-') as directory:
                    temp = Path(directory)
                    for relative in [MANIFEST] + [p['path'] for p in component.manifest['artifacts']]:
                        dest = temp / relative
                        dest.parent.mkdir(parents=True, exist_ok=True)
                        dest.write_bytes((root / relative).read_bytes())
                    target = temp / (MANIFEST if case['dependency'] == 'manifest' else component.pins[case['dependency']]['path'])
                    if case['mutation'] == 'missing':
                        target.unlink()
                    else:
                        target.write_bytes(target.read_bytes() + b' ')
                    report = verify(raw['intent'], raw['result'], root=temp)
            else:
                report = component.verify(raw['intent'], raw['result'])
            if 'reportEdits' in case:
                changed_report = component.intent_support.changed(report, case['reportEdits'])
                schema_check(component.validators['reportSchema'], changed_report, 'report')
            mismatches = [c['id'] for c in report['checks'] if c['outcome'] == 'MISMATCH']
            actual = {'componentResult': report['componentResult'], 'mismatches': mismatches}
            assert report['fullDomainValidation'] == 'UNAVAILABLE'
            assert 'overallDisposition' not in report and 'protectedEffectContractDigest' not in report
            # The evidence includes fresh complete-value digests for every
            # schema-valid mismatch, not stale hashes as a rejection shortcut.
            evidence.append({'name': case['name'], 'actual': actual,
                             'inputDigest': report['inputDigest'], 'resultDigest': report['resultDigest'],
                             'schemaValidation': report['schemaValidation']})
        except MappingError as error:
            actual = error.as_dict()
            evidence.append({'name': case['name'], 'actual': actual})
        if actual != case['expect']:
            failures.append({'name': case['name'], 'expected': case['expect'], 'actual': actual})
        counts[actual['componentResult']] += 1
    return {'result': 'FAIL' if failures else 'PASS', 'cases': len(data['cases']),
            'outcomes': dict(counts), 'failures': failures, 'evidence': evidence,
            'fullDomainValidation': 'UNAVAILABLE'}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--intent', type=Path)
    parser.add_argument('--result', type=Path)
    parser.add_argument('--cases', type=Path, help='Run the explicit component fixtures (also the default with no files).')
    args = parser.parse_args(argv)
    if bool(args.intent) != bool(args.result) or (args.cases and args.intent):
        parser.error('Use --intent and --result together, or --cases.')
    try:
        if args.intent:
            report = verify(file_bytes(args.intent, 'intent'), file_bytes(args.result, 'result'))
            status = 0 if report['componentResult'] == 'MATCH' else 1
        else:
            report = run_cases(path=args.cases)
            status = 0 if report['result'] == 'PASS' else 1
    except MappingError as error:
        report, status = error.as_dict(), 2
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return status


if __name__ == '__main__':
    sys.exit(main())
