#!/usr/bin/env python3
"""Draft shared validation-evidence integrity checks, never domain or runtime proof."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import re
import sys
from collections import Counter
from importlib.metadata import version
from pathlib import Path
from urllib.parse import urldefrag, urljoin

ROOT = Path(__file__).resolve().parents[2]
CASE_PATH = '04_implementation_and_conformance/examples_and_fixtures/fixtures/machine_contracts/OFARM_ProtectedEffectValidationTrace_envelope_cases_v0_1.json'
SCHEMA_PATH = '03_machine_contracts/drafts_non_default/authorization_finalization_evidence/protected_effect_validation/OFARM_ProtectedEffectValidationTrace_envelope_schema_v0_1.json'


class CheckError(ValueError):
    def __init__(self, layer, code, detail=''):
        super().__init__(code)
        self.layer, self.code, self.detail = layer, code, detail


def require(ok, layer, code, detail=''):
    if not ok:
        raise CheckError(layer, code, detail)


def strict_loads(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'JSON', 'DUPLICATE_JSON_NAME', key)
            result[key] = value
        return result

    def invalid_constant(value):
        raise CheckError('JSON', 'NON_JSON_NUMBER', value)

    def finite_float(value):
        result = float(value)
        require(math.isfinite(result), 'JSON', 'NON_FINITE_NUMBER', value)
        return result

    try:
        if isinstance(raw, bytes):
            raw = raw.decode('utf-8')
        value = json.loads(raw, object_pairs_hook=pairs, parse_constant=invalid_constant,
                           parse_float=finite_float)
        validate_json_domain(value)
        return value
    except CheckError:
        raise
    except (ValueError, RecursionError) as error:
        raise CheckError('JSON', 'INVALID_JSON', str(error)) from error


def validate_json_domain(value):
    if isinstance(value, str):
        try:
            value.encode('utf-8')
        except UnicodeEncodeError as error:
            raise CheckError('JSON', 'INVALID_UNICODE', str(error)) from error
    elif isinstance(value, bool) or value is None:
        return
    elif isinstance(value, int):
        require(abs(value) <= 9007199254740991, 'JSON', 'UNSAFE_INTEGER')
    elif isinstance(value, float):
        require(math.isfinite(value), 'JSON', 'NON_FINITE_NUMBER')
    elif isinstance(value, dict):
        for key, child in value.items():
            validate_json_domain(key)
            validate_json_domain(child)
    elif isinstance(value, list):
        for child in value:
            validate_json_domain(child)


def digest(value):
    """Complete-value RFC 8785 digest: no field exclusions or string normalization."""
    try:
        return 'sha256:' + hashlib.sha256(rfc8785.dumps(value)).hexdigest()
    except (rfc8785.CanonicalizationError, UnicodeError) as error:
        raise CheckError('CANONICAL', 'CANONICAL_DOMAIN', str(error)) from error


def tokens(path):
    require(isinstance(path, str) and (path == '' or path.startswith('/')),
            'BINDING', 'POINTER_SYNTAX')
    if not path:
        return []
    parts = path[1:].split('/')
    require(all(re.search(r'~(?![01])', part) is None for part in parts),
            'BINDING', 'POINTER_SYNTAX')
    return [part.replace('~1', '/').replace('~0', '~') for part in parts]


def pointer(value, path):
    for part in tokens(path):
        if isinstance(value, list):
            require(re.fullmatch(r'0|[1-9][0-9]*', part) is not None,
                    'BINDING', 'POINTER_SYNTAX')
            require(int(part) < len(value), 'BINDING', 'POINTER_MISSING', path)
            value = value[int(part)]
        else:
            require(isinstance(value, dict), 'BINDING', 'POINTER_TYPE', path)
            require(part in value, 'BINDING', 'POINTER_MISSING', path)
            value = value[part]
    return value


def changed(value, edits):
    result = copy.deepcopy(value)
    for edit in edits:
        parent_path, _, key = edit['path'].rpartition('/')
        parent = pointer(result, parent_path)
        key = tokens('/' + key)[0]
        if isinstance(parent, list):
            key = int(key)
        if edit['op'] == 'remove':
            del parent[key]
        elif edit['op'] == 'set':
            parent[key] = copy.deepcopy(edit['value'])
        else:
            raise CheckError('HARNESS', 'UNKNOWN_EDIT', edit['op'])
    return result


def objects(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from objects(child)
    elif isinstance(value, list):
        for child in value:
            yield from objects(child)


def error_tree(errors):
    for error in errors:
        yield error
        yield from error_tree(error.context)


def matches_error(error, witness):
    keyword = 'falseSchema' if error.schema is False else error.validator
    return (list(error.absolute_path) == witness['instancePath']
            and list(error.absolute_schema_path) == witness['schemaPath']
            and keyword == witness['keyword']
            and ('missingProperty' not in witness
                 or error.message == repr(witness['missingProperty']) + ' is a required property'))


def load_artifacts(root, pins, overrides=None):
    """Pin actual local bytes; no retrieval, mutable lookup or fallback resource."""
    overrides = overrides or {}
    result, schemas = {}, {}
    require(len({p['path'] for p in pins}) == len(pins), 'BINDING', 'DUPLICATE_ARTIFACT')
    for pin in pins:
        path = pin['path']
        require(not Path(path).is_absolute() and '..' not in Path(path).parts,
                'BINDING', 'ARTIFACT_PATH', path)
        source = root / path
        require(source.is_file() and overrides.get(path) != 'MISSING',
                'UNAVAILABLE', 'ARTIFACT_MISSING', path)
        raw = overrides.get(path, source.read_bytes())
        require(hashlib.sha256(raw).hexdigest() == pin['sha256'], 'BINDING', 'ARTIFACT_DIGEST', path)
        content = strict_loads(raw)
        result[path] = content
        if pin['kind'] == 'schema':
            require(isinstance(content, dict) and content.get('$id') == pin['schemaId'] and pin['schemaId'] not in schemas,
                    'BINDING', 'SCHEMA_ID', path)
            Draft202012Validator.check_schema(content)
            schemas[pin['schemaId']] = content
    for identity, schema in schemas.items():
        for node in objects(schema):
            require(node is schema or '$id' not in node, 'BINDING', 'NESTED_SCHEMA_ID_UNSUPPORTED')
            require('$dynamicRef' not in node, 'BINDING', 'DYNAMIC_SCHEMA_REFERENCE_UNSUPPORTED')
            for keyword in ('$ref', '$dynamicRef'):
                if keyword not in node:
                    continue
                document, fragment = urldefrag(urljoin(identity, node[keyword]))
                require(document in schemas, 'UNAVAILABLE', 'UNPINNED_SCHEMA_REFERENCE', document)
                if fragment:
                    require(fragment.startswith('/'), 'BINDING', 'UNSUPPORTED_SCHEMA_ANCHOR', fragment)
                    pointer(schemas[document], fragment)

    def unavailable(uri):
        raise NoSuchResource(ref=uri)

    registry = Registry(retrieve=unavailable).with_resources(
        (identity, Resource.from_contents(schema)) for identity, schema in schemas.items())
    return result, schemas, registry


CONTEXT_FIELDS = ('actionClass', 'authorizationResult', 'decisionBundleDigest', 'currentActionRuleBinding',
                  'effectIntent', 'effectIntentSchemaBinding', 'proposedResult', 'protectedEffectContractBinding',
                  'selectedActionBodySchemaBinding')
TRACE_PREFIX = 'urn:ofarm:protected-effect-validation-trace:sha256:'


def validate_shape(validator, value, case, target):
    errors = list(validator.iter_errors(value))
    witness = case.get('schemaError')
    if witness and (errors or case.get('schemaTarget', 'trace') == target):
        require(case.get('schemaTarget', 'trace') == target
                and any(matches_error(e, witness) for e in error_tree(errors)),
                'HARNESS', 'SCHEMA_REJECTION_WITNESS', case['name'])
    if errors:
        raise CheckError('SCHEMA', 'SCHEMA', target + ': ' + errors[0].json_path + ': ' + errors[0].message)


def schema_validator(binding, data, artifacts, registry):
    selections = [s for s in data['schemaSelections'] if s['binding']['schemaRef'] == binding['schemaRef']]
    require(len(selections) == 1, 'UNAVAILABLE', 'SCHEMA_SELECTOR_UNAVAILABLE', binding['schemaRef'])
    selected = selections[0]
    require(digest(binding) == digest(selected['binding']), 'BINDING', 'SCHEMA_BINDING_MISMATCH')
    document = artifacts[selected['path']]
    pin = next(p for p in data['artifactPins'] if p['path'] == selected['path'])
    require(binding['schemaDigest'] == 'sha256:' + pin['sha256']
            and binding['schemaRef'] == document['$id'] + ('#' + selected['pointer'] if selected['pointer'] else ''),
            'BINDING', 'SCHEMA_CATALOG_MISMATCH')
    target = pointer(document, selected['pointer'])
    # Follow exact referenced locations to check the selected object contract, not sibling definitions.
    seen = set()
    while isinstance(target, dict) and '$ref' in target:
        identity, fragment = urldefrag(urljoin(document['$id'], target['$ref']))
        require((identity, fragment) not in seen, 'BINDING', 'SCHEMA_REFERENCE_CYCLE')
        seen.add((identity, fragment))
        matches = [v for v in artifacts.values() if isinstance(v, dict) and v.get('$id') == identity]
        require(len(matches) == 1, 'UNAVAILABLE', 'SCHEMA_DOCUMENT_UNAVAILABLE', identity)
        document = matches[0]
        target = pointer(document, fragment)
    require(isinstance(target, dict) and target.get('type') == 'object'
            and target.get('additionalProperties') is False,
            'BINDING', 'CLOSED_OBJECT_SCHEMA_REQUIRED')
    validator = Draft202012Validator({'$schema': 'https://json-schema.org/draft/2020-12/schema',
                                     '$ref': binding['schemaRef']}, registry=registry)
    return validator, target


def payload_validator(binding, data, artifacts, registry):
    validator, selected = schema_validator(binding, data, artifacts, registry)
    require(selected.get('properties', {}).get('overallDisposition') == {'enum': ['PASS', 'FAIL']}
            and 'overallDisposition' in selected.get('required', []), 'BINDING', 'PAYLOAD_VERDICT_INTERFACE')
    return validator


def trace_reference(value):
    value_digest = digest(value)
    return {'ref': TRACE_PREFIX + value_digest[7:], 'digest': value_digest}


def verify_reference(value, reference, validators, case):
    validate_shape(validators['reference'], reference, case, 'reference')
    require(reference['digest'] == digest(value), 'INTEGRITY', 'TRACE_DIGEST')
    require(reference['ref'] == TRACE_PREFIX + reference['digest'][7:], 'INTEGRITY', 'TRACE_REF')


def example_value(scenario, role, data, artifacts, registry, case):
    require(role in scenario['foreign'], 'UNAVAILABLE', 'FOREIGN_VALUE_UNAVAILABLE', role)
    item = scenario['foreign'][role]
    validator, selected = schema_validator(item['schemaBinding'], data, artifacts, registry)
    validate_shape(validator, item['value'], case, role)
    if role in ('authorizationResult', 'rule', 'decisionBundle', 'contract', 'payload'):
        require(item['value'].get('fixtureOnly') is True and item['ref'].startswith('urn:ofarm-test:'),
                'UNAVAILABLE', 'PRODUCTION_OWNER_PROJECTION_UNAVAILABLE', role)
    digest(item['value'])
    return item


def verify_integrity(scenario, data, artifacts, registry, validators, case):
    trace, context = scenario['trace'], scenario['expectedContext']
    validate_shape(validators['trace'], trace, case, 'trace')
    digest(trace)
    require(scenario['posture'] == 'TEST_ONLY_INTEGRITY_EXAMPLE', 'HARNESS', 'EXAMPLE_POSTURE')
    # The context is separately supplied test input. It is not obtained by projecting the trace.
    require(all(key in context and digest(trace[key]) == digest(context[key]) for key in CONTEXT_FIELDS),
            'BINDING', 'EXPECTED_CONTEXT_MISMATCH')
    require(digest(trace['domainPayload']['schemaBinding']) == digest(context['domainPayloadSchemaBinding']),
            'BINDING', 'EXPECTED_CONTEXT_MISMATCH')
    for binding in (trace['effectIntentSchemaBinding'], trace['proposedResult']['resultSchemaBinding']):
        schema_validator(binding, data, artifacts, registry)
    selected_body_validator, _ = schema_validator(trace['selectedActionBodySchemaBinding'], data, artifacts, registry)
    schema_validator(trace['domainPayload']['schemaBinding'], data, artifacts, registry)

    # These five projections belong ONLY to the explicitly fictional examples in this bundle.
    # Real authorization result/rule/bundle and protected-effect contract producers remain absent.
    authorization = example_value(scenario, 'authorizationResult', data, artifacts, registry, case)
    require(trace['authorizationResult']['ref'] == authorization['ref']
            and authorization['value']['recordId'] == authorization['ref'], 'BINDING', 'AUTHORIZATION_IDENTITY')
    require(trace['authorizationResult']['digest'] == digest(authorization['value']), 'INTEGRITY', 'AUTHORIZATION_DIGEST')
    bundle = example_value(scenario, 'decisionBundle', data, artifacts, registry, case)
    require(bundle['value']['authorizationResultDigest'] == digest(authorization['value']),
            'INTEGRITY', 'EXAMPLE_BUNDLE_MEMBER')
    require(trace['decisionBundleDigest'] == digest(bundle['value']), 'INTEGRITY', 'EXAMPLE_BUNDLE_DIGEST')
    rule = example_value(scenario, 'rule', data, artifacts, registry, case)
    rb = trace['currentActionRuleBinding']
    require(rb['ruleRef'] == rule['ref'] and rb['ruleId'] == rule['value']['ruleId'], 'BINDING', 'RULE_IDENTITY')
    require(trace['actionClass'] == rule['value']['actionClass'], 'BINDING', 'RULE_ACTION_CLASS')
    require(rb['ruleDigest'] == digest(rule['value']), 'INTEGRITY', 'EXAMPLE_RULE_DIGEST')
    selector = rb['ruleRevisionSelector']
    if 'contentDigest' in selector:
        require(selector['contentDigest'] == digest(rule['value']), 'BINDING', 'RULE_SELECTOR_DIGEST')
    else:
        require(selector['revisionRef'] == rule['revisionRef'], 'BINDING', 'RULE_SELECTOR_REVISION')
    intent = example_value(scenario, 'intent', data, artifacts, registry, case)
    require(trace['effectIntent']['ref'] == intent['ref'], 'BINDING', 'INTENT_IDENTITY')
    require(digest(intent['schemaBinding']) == digest(trace['effectIntentSchemaBinding']), 'BINDING', 'INTENT_SCHEMA')
    require(trace['effectIntent']['digest'] == digest(intent['value']), 'INTEGRITY', 'INTENT_DIGEST')
    result = example_value(scenario, 'result', data, artifacts, registry, case)
    proposed = trace['proposedResult']
    require(proposed['resultRef'] == result['ref'] and proposed['resultId'] == result['value']['assertionRecordId'],
            'BINDING', 'RESULT_IDENTITY')
    require(digest(result['schemaBinding']) == digest(proposed['resultSchemaBinding']), 'BINDING', 'RESULT_SCHEMA')
    require(proposed['resultDigest'] == digest(result['value']), 'INTEGRITY', 'RESULT_DIGEST')
    contract = example_value(scenario, 'contract', data, artifacts, registry, case)
    cb = trace['protectedEffectContractBinding']
    require(cb['contractRef'] == contract['ref'] and cb['contractId'] == contract['value']['contractId']
            and cb['contractVersion'] == contract['value']['contractVersion'], 'BINDING', 'CONTRACT_IDENTITY')
    projected = copy.deepcopy(contract['value'])
    own_digest = projected.pop('contractDigest')
    require(own_digest == digest(projected) and cb['contractDigest'] == own_digest,
            'INTEGRITY', 'TEST_ONLY_CONTRACT_DIGEST')
    for field in ('intentSchemaBinding', 'resultSchemaBinding', 'bodySchemaBinding', 'payloadSchemaBinding'):
        schema_validator(contract['value'][field], data, artifacts, registry)
    require(digest(contract['value']['bodySchemaBinding']) == digest(trace['selectedActionBodySchemaBinding']),
            'BINDING', 'SELECTED_BODY_SCHEMA_MISMATCH')
    require(digest(contract['value']['intentSchemaBinding']) == digest(trace['effectIntentSchemaBinding'])
            and digest(contract['value']['resultSchemaBinding']) == digest(proposed['resultSchemaBinding'])
            and digest(contract['value']['payloadSchemaBinding']) == digest(trace['domainPayload']['schemaBinding']),
            'BINDING', 'TEST_ONLY_CONTRACT_SCHEMAS')
    validate_shape(selected_body_validator, result['value']['assertionBody'], case, 'resultBody')
    payload = example_value(scenario, 'payload', data, artifacts, registry, case)
    payload_validator(trace['domainPayload']['schemaBinding'], data, artifacts, registry)
    require(digest(payload['schemaBinding']) == digest(trace['domainPayload']['schemaBinding']), 'BINDING', 'PAYLOAD_SCHEMA')
    require(payload['ref'] == trace['domainPayload']['ref'], 'BINDING', 'PAYLOAD_IDENTITY')
    require(digest(payload['value']) == trace['domainPayload']['digest'], 'INTEGRITY', 'PAYLOAD_DIGEST')
    require(pointer(payload['value'], trace['domainPayload']['overallDispositionPointer']) == trace['overallDisposition'],
            'BINDING', 'PAYLOAD_VERDICT_MISMATCH')
    verify_reference(trace, scenario['reference'], validators, case)
    return trace


def run_case(case, data, artifacts, schemas, registry, validators, root):
    kind = case['kind']
    if kind == 'json':
        strict_loads(bytes.fromhex(case['rawHex']) if 'rawHex' in case else case['raw'])
        return
    if kind == 'canonical':
        value = json.loads(case['valueJson']) if 'valueJson' in case else case['value']
        digest(value)
        if 'expected' in case:
            require(rfc8785.dumps(value).decode('utf-8') == case['expected'], 'CANONICAL', 'CANONICAL_VECTOR')
        return
    if kind == 'artifact':
        pins = changed(data['artifactPins'], case.get('pinEdits', [])) + case.get('extraPins', [])
        path = case.get('path')
        override = {path: 'MISSING' if case.get('missing') else (root / path).read_bytes() + b' '} if path else {}
        load_artifacts(root, pins, override)
        return
    if kind == 'schema-policy':
        # Deliberate helper-boundary controls may corrupt the catalog or omit an already
        # loaded document. They are not claims about reaching these guards after preflight.
        catalog = changed(data, case.get('catalogEdits', []))
        available = {path: value for path, value in artifacts.items()
                     if path not in case.get('omitResolvedDocuments', [])}
        (payload_validator if case.get('payload') else schema_validator)(case['binding'], catalog, available, registry)
        return
    scenario = changed(data['scenarios'][case['scenario']], case.get('edits', []))
    trace = scenario['trace']
    if kind == 'schema':
        validate_shape(validators[case.get('schemaTarget', 'trace')],
                       scenario[case.get('schemaTarget', 'trace')], case, case.get('schemaTarget', 'trace'))
        digest(trace)
        return
    if kind == 'trace-digest':
        validate_shape(validators['trace'], trace, case, 'trace')
        verify_reference(trace, scenario['reference'], validators, case)
        return
    if kind == 'identity':
        ledger = {}
        for value in [data['scenarios'][case['scenario']]['trace'], trace]:
            identity, hashed = value['validationTraceId'], digest(value)
            require(identity not in ledger or ledger[identity] == hashed, 'BINDING', 'IMMUTABLE_ID_COLLISION')
            ledger[identity] = hashed
        return
    verify_integrity(scenario, data, artifacts, registry, validators, case)
    if kind == 'compatibility':
        validate_shape(validators['pr40Record'], scenario['reference'], case, 'pr40Record')
        validate_shape(validators['pr40Wrapper'], scenario['wrapper'], case, 'pr40Wrapper')
        require(digest(scenario['wrapper']['trace']) == digest(scenario['reference'])
                and scenario['wrapper']['disposition'] == trace['overallDisposition'], 'BINDING', 'PR40_WRAPPER_MISMATCH')
    elif kind == 'admitted-compatibility':
        # The fictional contract deliberately cannot satisfy PR40's production contract identity.
        admitted = {k: trace['proposedResult'][k] for k in ('resultId', 'resultDigest', 'resultSchemaBinding')}
        admitted.update(protectedEffectContractBinding=trace['protectedEffectContractBinding'], validationTrace=scenario['reference'])
        validate_shape(validators['pr40Admitted'], admitted, case, 'pr40Admitted')
    else:
        require(kind == 'integrity', 'HARNESS', 'UNKNOWN_CASE_KIND', kind)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--cases', type=Path)
    args = parser.parse_args()
    cases_path = args.cases or args.root / CASE_PATH
    require(cases_path.is_file() and (args.root / SCHEMA_PATH).is_file(), 'UNAVAILABLE', 'ACTUAL_CHECKPOINT_REQUIRED')
    require(version('rfc8785') == '0.1.4', 'PREREQUISITE', 'CANONICALIZER_VERSION')
    data = strict_loads(cases_path.read_bytes())
    require(data['posture'] == 'TEST_ONLY_ENVELOPE_INTEGRITY_EXAMPLES', 'HARNESS', 'FIXTURE_POSTURE')
    artifacts, schemas, registry = load_artifacts(args.root, data['artifactPins'])
    envelope, pr40 = artifacts[SCHEMA_PATH], artifacts[data['pr40SchemaPath']]
    validators = {'trace': Draft202012Validator(envelope, registry=registry)}
    for name, document, path in [('reference', envelope, 'traceReference'), ('pr40Record', pr40, 'recordBinding'),
                                  ('pr40Wrapper', pr40, 'protectedEffectValidation'), ('pr40Admitted', pr40, 'admittedProtectedResultBinding')]:
        validators[name] = Draft202012Validator({'$schema': document['$schema'], '$ref': document['$id'] + '#/$defs/' + path}, registry=registry)
    names = [c['name'] for c in data['cases']]
    require(len(names) == len(set(names)), 'HARNESS', 'DUPLICATE_CASE_NAME')
    require(all('schemaError' in c for c in data['cases'] if isinstance(c['expect'], dict) and c['expect']['layer'] == 'SCHEMA'),
            'HARNESS', 'SCHEMA_WITNESS_REQUIRED')
    counts, layers, failures = Counter(), Counter(), []
    for case in data['cases']:
        try:
            run_case(case, data, artifacts, schemas, registry, validators, args.root)
        except CheckError as error:
            if case['expect'] == {'layer': error.layer, 'code': error.code}:
                counts['negativeCases'] += 1
                layers[error.layer] += 1
            else:
                failures.append({'name': case['name'], 'expected': case['expect'], 'actual': {'layer': error.layer, 'code': error.code}, 'detail': error.detail})
        else:
            if case['expect'] == 'PASS':
                counts['positiveCases'] += 1
            else:
                failures.append({'name': case['name'], 'expected': case['expect'], 'actual': 'ACCEPTED'})
    print(json.dumps({'result': 'FAIL' if failures else 'PASS', 'posture': data['posture'], **counts,
                      'negativeRejectionLayers': dict(layers), 'schemaRejectionWitnesses': sum('schemaError' in c for c in data['cases']),
                      'failures': failures, 'artifactPins': data['artifactPins'], 'deferredGuarantees': data['deferredGuarantees'],
                      'productionDomainValidation': 'UNAVAILABLE', 'productionAuthorityValidation': 'UNAVAILABLE',
                      'expectedContextProvenance': 'Frozen test inputs; no runtime owner/context producer is exercised.',
                      'dependencies': {name: version(name) for name in ('jsonschema', 'referencing', 'rfc8785')},
                      'limit': 'Fictional envelope integrity and actual schema/reference compatibility only; no AR/PC truth, authority, admitted result, storage immutability, same-attempt FAIL-to-PASS prevention, transaction or runtime proof.'}, indent=2))
    return 1 if failures else 0


if __name__ == '__main__':
    try:
        import rfc8785
        from jsonschema import Draft202012Validator
        from referencing import Registry, Resource
        from referencing.exceptions import NoSuchResource
    except ImportError as error:
        print(json.dumps({'result': 'UNAVAILABLE', 'missingPrerequisite': str(error)}))
        sys.exit(2)
    try:
        sys.exit(main())
    except CheckError as error:
        print(json.dumps({'result': 'UNAVAILABLE' if error.layer == 'UNAVAILABLE' else 'FAIL',
                          'layer': error.layer, 'code': error.code, 'detail': error.detail}, indent=2))
        sys.exit(2 if error.layer == 'UNAVAILABLE' else 1)
