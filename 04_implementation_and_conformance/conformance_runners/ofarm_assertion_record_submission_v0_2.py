#!/usr/bin/env python3
"""Draft AssertionRecord shape and local integrity checks, never runtime approval."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from collections import Counter
from datetime import date
from importlib.metadata import version
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = '03_machine_contracts/drafts_non_default/assertion_record_submission/OFARM_AssertionRecord_schema_v0_2.json'
CASE_PATH = '04_implementation_and_conformance/examples_and_fixtures/fixtures/machine_contracts/OFARM_AssertionRecord_submission_cases_v0_2.json'
DEFINITIONS = ('assertionRecord', 'structureAssertionBody', 'operationClaimBody', 'complianceAssertionBody')
TIME_PROFILES = frozenset(('STRUCTURE_AS_OF', 'STRUCTURE_EFFECTIVE_FROM', 'STRUCTURE_EFFECTIVE_INTERVAL',
                           'INTENDED_WINDOW', 'PERFORMED_INSTANT', 'PERFORMED_INTERVAL',
                           'COMPLIANCE_AS_OF', 'COMPLIANCE_EFFECTIVE_FROM', 'COMPLIANCE_EFFECTIVE_INTERVAL'))
STAMP = re.compile(r'([0-9]{4})-([0-9]{2})-([0-9]{2})T([0-9]{2}):([0-9]{2}):([0-9]{2})(?:\.([0-9]{0,8}[1-9]))?Z\Z')


class ContractError(ValueError):
    def __init__(self, layer, code, detail=''):
        super().__init__(code)
        self.layer, self.code, self.detail = layer, code, detail


def require(condition, layer, code, detail=''):
    if not condition:
        raise ContractError(layer, code, detail)


def strict_loads(raw):
    def pairs(items):
        value = {}
        for key, item in items:
            require(key not in value, 'JSON', 'DUPLICATE_JSON_NAME', key)
            value[key] = item
        return value

    def invalid_constant(value):
        raise ContractError('JSON', 'NON_JSON_NUMBER', value)

    try:
        return json.loads(raw, object_pairs_hook=pairs, parse_constant=invalid_constant)
    except json.JSONDecodeError as error:
        raise ContractError('JSON', 'INVALID_JSON', str(error)) from error


def timestamp_ns(value):
    """Preserve all nine fractional digits; datetime microsecond truncation is unsafe."""
    match = STAMP.fullmatch(value) if isinstance(value, str) else None
    if match is None:
        raise ValueError('Non-canonical timestamp')
    year, month, day, hour, minute, second = map(int, match.groups()[:6])
    ordinal = date(year, month, day).toordinal()  # Real Gregorian calendar validation.
    if hour > 23 or minute > 59 or second > 59:
        raise ValueError('Invalid clock time')
    nanos = int((match.group(7) or '').ljust(9, '0'))
    return ((ordinal * 24 + hour) * 3600 + minute * 60 + second) * 1_000_000_000 + nanos


def digest(value):
    try:
        canonical = rfc8785.dumps(value)
    except (rfc8785.CanonicalizationError, UnicodeError) as error:
        raise ContractError('CANONICAL', 'CANONICAL_DOMAIN', str(error)) from error
    return 'sha256:' + hashlib.sha256(canonical).hexdigest()


def pointer(value, path):
    if path == '':
        return value
    for part in path.lstrip('/').split('/'):
        part = part.replace('~1', '/').replace('~0', '~')
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def changed(value, edits):
    value = copy.deepcopy(value)
    for edit in edits:
        parent_path, _, key = edit['path'].rpartition('/')
        parent = pointer(value, parent_path)
        key = key.replace('~1', '/').replace('~0', '~')
        if isinstance(parent, list):
            key = int(key)
        if edit['op'] == 'remove':
            del parent[key]
        elif edit['op'] == 'set':
            parent[key] = copy.deepcopy(edit['value'])
        else:
            raise ContractError('HARNESS', 'UNKNOWN_EDIT', edit['op'])
    return value


def objects(value):
    if isinstance(value, dict):
        yield value
        for item in value.values():
            yield from objects(item)
    elif isinstance(value, list):
        for item in value:
            yield from objects(item)


def check_component(definition, record):
    # These are comparisons within supplied bytes, not resolved-source/authority proof.
    for value in objects(record):
        if value.get('profile') in TIME_PROFILES and 'start' in value and 'end' in value:
            require(timestamp_ns(value['start']) < timestamp_ns(value['end']),
                    'COMPONENT', 'INTERVAL_ORDER')
    if definition != 'assertionRecord':
        return
    subject, anchor = record['subject'], record['anchorScopes'][0]
    if subject['subjectPosture'] == 'PROSPECTIVE_SUBJECT':
        identity = (subject['subjectType'], subject['subjectRef'])
        require(identity != (anchor['scopeType'], anchor['scopeRef']),
                'COMPONENT', 'PROSPECTIVE_SUBJECT_IS_ANCHOR')
        for context in record['assertionBody'].get('contextBindings', []):
            require(identity != (context['contextRole'], context['binding']['ref']),
                    'COMPONENT', 'PROSPECTIVE_SUBJECT_IS_CONTEXT')
    same = (subject['subjectPosture'] == 'EXISTING_SUBJECT'
            and subject['subjectType'] == anchor['scopeType']
            and subject['subjectRef'] == anchor['scopeRef']
            and {k: subject[k] for k in ('revisionRef', 'digest') if k in subject}
            == {k: anchor[k] for k in ('revisionRef', 'digest') if k in anchor})
    require(('subjectScopeProofBindings' in record) != same,
            'COMPONENT', 'SUBJECT_SCOPE_PROOF_ABSENCE' if same else 'SUBJECT_SCOPE_PROOF_REQUIRED')
    prior = record.get('supersedesAssertionRecordBinding')
    require(prior is None or prior['ref'] != record['assertionRecordId'], 'COMPONENT', 'CORRECTION_SELF_REFERENCE')
    body = record['assertionBody']
    if record['assertionType'] in ('STRUCTURE_ASSERTION', 'COMPLIANCE_ASSERTION'):
        require(body['applicability'] == record['subjectTime'], 'COMPONENT', 'BODY_TIME_EQUALITY')
    elif body['temporalBasis']['sourceKind'] == 'BODY_TIME':
        require(body['temporalBasis']['time'] == record['subjectTime'], 'COMPONENT', 'BODY_TIME_EQUALITY')
    # External temporal sources deliberately remain unresolved here.



def error_tree(errors):
    for error in errors:
        yield error
        yield from error_tree(error.context)


def matches_schema_error(error, witness):
    keyword = 'falseSchema' if error.schema is False else error.validator
    return (list(error.absolute_path) == witness['instancePath']
            and list(error.absolute_schema_path) == witness['schemaPath']
            and keyword == witness['keyword']
            and ('missingProperty' not in witness
                 or error.message == repr(witness['missingProperty']) + ' is a required property'))


def run_case(case, fixtures, validators):
    kind = case['kind']
    if kind == 'json':
        return strict_loads(case['raw'])
    if kind == 'canonical-domain':
        return digest(case['value'])
    if kind == 'canonical-vector':
        require(rfc8785.dumps(case['value']).decode('utf-8') == case['expected'],
                'CANONICAL', 'CANONICAL_VECTOR')
        return
    value = changed(fixtures[case['fixture']]['value'], case.get('edits', []))
    definition = case.get('definition', fixtures[case['fixture']]['definition'])
    errors = list(validators[definition].iter_errors(value))
    bare_errors = list(validators[definition + ':no-formats'].iter_errors(value))
    if definition == 'assertionRecord':
        require(bool(errors) == bool(list(validators['root'].iter_errors(value)))
                and bool(bare_errors) == bool(list(validators['root:no-formats'].iter_errors(value))),
                'HARNESS', 'ROOT_PROFILE_DISAGREEMENT')
    witness = case.get('schemaError')
    if witness:
        require(any(matches_schema_error(error, witness) for error in error_tree(errors)),
                'HARNESS', 'SCHEMA_REJECTION_WITNESS', case['name'])
        if witness['keyword'] == 'format':
            require(not bare_errors, 'HARNESS', 'FORMAT_DEPENDENCE_WITNESS', case['name'])
        else:
            require(any(matches_schema_error(error, witness) for error in error_tree(bare_errors)),
                    'HARNESS', 'NO_FORMAT_REJECTION_WITNESS', case['name'])
    else:
        require(not bare_errors, 'HARNESS', 'NO_FORMAT_POSITIVE_CONTROL', case['name'])
    if errors:
        raise ContractError('SCHEMA', 'SCHEMA', errors[0].json_path + ': ' + errors[0].message)
    if kind != 'schema':
        check_component(definition, value)
    if kind == 'integrity':
        selected = pointer(value, case.get('pointer', ''))
        require(digest(selected) == case['expectedDigest'], 'INTEGRITY', 'EXACT_BYTES_DIGEST')
    else:
        require(kind in ('schema', 'component'), 'HARNESS', 'UNKNOWN_CASE_KIND', kind)
    digest(value)  # Every admitted fixture must also be in the real RFC 8785 domain.


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--schema', type=Path, default=ROOT / SCHEMA_PATH)
    parser.add_argument('--cases', type=Path, default=ROOT / CASE_PATH)
    args = parser.parse_args()
    for path in (args.schema, args.cases):
        if not path.is_file():
            print(json.dumps({'result': 'UNAVAILABLE', 'missingPrerequisite': str(path),
                              'limit': 'No fallback schema or runtime conclusion.'}, indent=2))
            return 2
    require(version('rfc8785') == '0.1.4', 'PREREQUISITE', 'CANONICALIZER_VERSION')
    data = strict_loads(args.cases.read_text())
    require(data['posture'] == 'FICTIONAL_COMPONENT_ONLY', 'HARNESS', 'FIXTURE_POSTURE')
    if not data.get('schemaByteSha256'):
        print(json.dumps({'result': 'UNAVAILABLE', 'missingPrerequisite': 'Frozen actual schema checkpoint'}))
        return 2
    schema_bytes = args.schema.read_bytes()
    require(hashlib.sha256(schema_bytes).hexdigest() == data['schemaByteSha256'], 'INTEGRITY', 'SCHEMA_FILE_DIGEST')
    schema = strict_loads(schema_bytes)
    Draft202012Validator.check_schema(schema)
    formats = FormatChecker()

    @formats.checks('date-time', raises=(ValueError, TypeError))
    def valid_time(value):
        if not isinstance(value, str):
            return True  # The schema owns type rejection.
        timestamp_ns(value)
        return True

    validators = {name: Draft202012Validator({'$schema': schema['$schema'], '$defs': schema['$defs'],
                    '$ref': '#/$defs/' + name}, format_checker=formats) for name in DEFINITIONS}
    validators['root'] = Draft202012Validator(schema, format_checker=formats)
    for name in DEFINITIONS:
        validators[name + ':no-formats'] = Draft202012Validator(
            {'$schema': schema['$schema'], '$defs': schema['$defs'], '$ref': '#/$defs/' + name})
    validators['root:no-formats'] = Draft202012Validator(schema)
    require(all('schemaError' in c for c in data['cases'] if c['expect'] == {'layer': 'SCHEMA', 'code': 'SCHEMA'}),
            'HARNESS', 'MISSING_SCHEMA_WITNESS')
    counts, layers, failures = Counter(), Counter(), []
    names = [case['name'] for case in data['cases']]
    require(len(names) == len(set(names)), 'HARNESS', 'DUPLICATE_CASE_NAME')
    require(any(c['expect'] == 'PASS' for c in data['cases']) and any(c['expect'] != 'PASS' for c in data['cases']),
            'HARNESS', 'MISSING_CONTROLS')
    for case in data['cases']:
        try:
            run_case(case, data['fixtures'], validators)
        except ContractError as error:
            if case['expect'] == {'layer': error.layer, 'code': error.code}:
                counts['negativeCases'] += 1
                layers[error.layer] += 1
            else:
                failures.append({'name': case['name'], 'expected': case['expect'],
                                 'actual': {'layer': error.layer, 'code': error.code}, 'detail': error.detail})
        else:
            if case['expect'] == 'PASS':
                counts['positiveCases'] += 1
            else:
                failures.append({'name': case['name'], 'expected': case['expect'], 'actual': 'ACCEPTED'})
    print(json.dumps({'result': 'FAIL' if failures else 'PASS', 'schemaByteSha256': data['schemaByteSha256'],
                      'profiles': len(DEFINITIONS), 'fixtures': len(data['fixtures']), **counts,
                      'negativeRejectionLayers': dict(layers), 'failures': failures,
                      'schemaWithoutFormatChecks': dict(Counter(c['schemaWithoutFormats'] for c in data['cases'] if 'schemaWithoutFormats' in c)),
                      'deferredGuarantees': data['deferredGuarantees'],
                      'limit': 'Fictional shape, local comparisons and complete-byte digests only. No foreign resolution, authorization, trusted clock, transaction, acceptance or runtime proof.'}, indent=2))
    return 1 if failures else 0


if __name__ == '__main__':
    try:
        import rfc8785
        from jsonschema import Draft202012Validator, FormatChecker, ValidationError
    except ImportError as error:
        print(json.dumps({'result': 'UNAVAILABLE', 'missingPrerequisite': str(error)}))
        sys.exit(2)
    try:
        sys.exit(main())
    except ContractError as error:
        print(json.dumps({'result': 'FAIL', 'layer': error.layer, 'code': error.code, 'detail': error.detail}, indent=2))
        sys.exit(1)
