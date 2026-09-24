#!/usr/bin/env python3
"""Draft authorization-input checks; no authority evaluation or runtime admission."""
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
from urllib.parse import urldefrag, urljoin

ROOT = Path(__file__).resolve().parents[2]
CASE_PATH = '04_implementation_and_conformance/examples_and_fixtures/fixtures/machine_contracts/OFARM_AuthorizationEffectIntent_cases_v0_2.json'
STAMP = re.compile(r'([0-9]{4})-([0-9]{2})-([0-9]{2})T([0-9]{2}):([0-9]{2}):([0-9]{2})(?:\.([0-9]{0,8}[1-9]))?Z\Z')


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

    def invalid(value):
        raise CheckError('JSON', 'NON_JSON_NUMBER', value)

    try:
        return json.loads(raw, object_pairs_hook=pairs, parse_constant=invalid)
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        raise CheckError('JSON', 'INVALID_JSON', str(error)) from error


def digest(value):
    try:
        raw = rfc8785.dumps(value)
    except (rfc8785.CanonicalizationError, UnicodeError) as error:
        raise CheckError('CANONICAL', 'CANONICAL_DOMAIN', str(error)) from error
    return 'sha256:' + hashlib.sha256(raw).hexdigest()


def tokens(path):
    require(isinstance(path, str) and (path == '' or path.startswith('/')),
            'EXTRACTION', 'POINTER_SYNTAX')
    if path == '':
        return []
    parts = path[1:].split('/')
    require(all(re.search(r'~(?![01])', part) is None for part in parts),
            'EXTRACTION', 'POINTER_SYNTAX')
    return [part.replace('~1', '/').replace('~0', '~') for part in parts]


def pointer(value, path):
    for part in tokens(path):
        if isinstance(value, list):
            require(re.fullmatch(r'0|[1-9][0-9]*', part) is not None,
                    'EXTRACTION', 'POINTER_SYNTAX')
            index = int(part)
            require(index < len(value), 'EXTRACTION', 'POINTER_MISSING', path)
            value = value[index]
        else:
            require(isinstance(value, dict), 'EXTRACTION', 'POINTER_TYPE', path)
            require(part in value, 'EXTRACTION', 'POINTER_MISSING', path)
            value = value[part]
    return value


def changed(value, edits):
    result = copy.deepcopy(value)
    for edit in edits:
        if edit['op'] == 'append':
            target = pointer(result, edit['path'])
            require(isinstance(target, list), 'HARNESS', 'APPEND_TARGET')
            target.append(copy.deepcopy(edit['value']))
            continue
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


def timestamp_ns(value):
    match = STAMP.fullmatch(value) if isinstance(value, str) else None
    if match is None:
        raise ValueError('Non-canonical timestamp')
    year, month, day, hour, minute, second = map(int, match.groups()[:6])
    ordinal = date(year, month, day).toordinal()
    if hour > 23 or minute > 59 or second > 59:
        raise ValueError('Invalid clock time')
    return ((ordinal * 24 + hour) * 3600 + minute * 60 + second) * 1_000_000_000 + int((match.group(7) or '').ljust(9, '0'))


def objects(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from objects(child)
    elif isinstance(value, list):
        for child in value:
            yield from objects(child)


def load_artifacts(root, pins, overrides=None):
    """Only hash-verified actual bytes enter the registry; retrieval is never allowed."""
    overrides = overrides or {}
    result, ids = {}, set()
    require(len({p['path'] for p in pins}) == len(pins), 'BINDING', 'DUPLICATE_ARTIFACT')
    for pin in pins:
        path = pin['path']
        require(not Path(path).is_absolute() and '..' not in Path(path).parts,
                'BINDING', 'ARTIFACT_PATH', path)
        file = root / path
        require(file.is_file() and overrides.get(path) != 'MISSING', 'BINDING', 'ARTIFACT_MISSING', path)
        raw = overrides.get(path, file.read_bytes())
        require(hashlib.sha256(raw).hexdigest() == pin['sha256'], 'BINDING', 'ARTIFACT_DIGEST', path)
        content = strict_loads(raw)
        if pin['kind'] == 'schema':
            require(content.get('$id') == pin['schemaId'] and pin['schemaId'] not in ids,
                    'BINDING', 'SCHEMA_ID', path)
            ids.add(pin['schemaId'])
            Draft202012Validator.check_schema(content)
        result[path] = content
    schemas = {p['schemaId']: result[p['path']] for p in pins if p['kind'] == 'schema'}
    # Preflight all references, including ones no positive fixture happens to visit.
    for identity, schema in schemas.items():
        for node in objects(schema):
            if '$ref' not in node:
                continue
            document, fragment = urldefrag(urljoin(identity, node['$ref']))
            require(document in schemas, 'BINDING', 'UNPINNED_SCHEMA_REFERENCE', document)
            if fragment:
                require(fragment.startswith('/'), 'BINDING', 'UNSUPPORTED_SCHEMA_ANCHOR', fragment)
                pointer(schemas[document], fragment)

    def unavailable(uri):
        raise NoSuchResource(ref=uri)

    registry = Registry(retrieve=unavailable).with_resources(
        (identity, Resource.from_contents(schema)) for identity, schema in schemas.items())
    return result, registry



def verify_descriptor(descriptor, schemas, pins):
    require(descriptor['status'] == 'DRAFT_NON_DEFAULT_INCOMPLETE_NON_EXECUTABLE',
            'BINDING', 'DESCRIPTOR_POSTURE')
    profiles = descriptor['profiles']
    required_profiles = {'EI_OPERATION_ASSERTION_V0_2': 'ASSERT_OPERATION_CLAIM',
                         'EI_DATA_READ_V0_2': 'RECEIVE_READ_DATA'}
    require(len(profiles) == 2 and {p['profileId']: p['actionClass'] for p in profiles} == required_profiles,
            'BINDING', 'PROFILE_SET')
    by_id = {p['schemaId']: p for p in pins if p['kind'] == 'schema'}

    def binding(value):
        pin = by_id.get(value['schemaRef'])
        require(pin is not None and value['schemaDigest'] == 'sha256:' + pin['sha256'],
                'BINDING', 'SCHEMA_BINDING_DIGEST')
        schema = schemas[pin['path']]
        # The dependency root delegates to a definition; its carrier schemaVersion is there.
        props = schema.get('properties') or schema['$defs']['assertionRecord']['properties']
        require(value['schemaVersion'] == props['schemaVersion']['const'], 'BINDING', 'SCHEMA_BINDING_VERSION')
        if 'repositoryPath' in value:
            require(value['repositoryPath'] == pin['path'] and value['digestBasis'] == 'EXACT_FILE_BYTES_SHA256',
                    'BINDING', 'DEPENDENCY_PATH')

    for profile in profiles:
        value = profile['intentSchemaBinding']
        binding(value)
        require(value['profileId'] == profile['profileId'] and value['canonicalization'] == 'JCS_RFC8785_SHA256'
                and profile['schemaDigestBasis'] == 'EXACT_FILE_BYTES_SHA256', 'BINDING', 'PROFILE_BINDING')
        pin = by_id[value['schemaRef']]
        dependencies = schemas[pin['path']]['x-ofarm-schemaDependencies']
        require(profile['dependencySchemaBindings'] == dependencies, 'BINDING', 'DEPENDENCY_BINDING')
        for dependency in dependencies:
            binding(dependency)
        mappings = profile['mappings']
        require(len({m['mappingId'] for m in mappings}) == len(mappings), 'EXTRACTION', 'DUPLICATE_MAPPING_ID')
        for mapping in mappings:
            require(set(mapping) <= {'mappingId', 'sourcePointer', 'destinationPointer', 'transformation', 'required', 'when'}
                    and {'mappingId', 'sourcePointer', 'destinationPointer', 'transformation', 'required'} <= set(mapping),
                    'EXTRACTION', 'DESCRIPTOR_MEMBERS')
            require(mapping['transformation'] == 'IDENTITY' and isinstance(mapping['required'], bool),
                    'EXTRACTION', 'IDENTITY_ONLY')
            tokens(mapping['sourcePointer'])
            require(bool(tokens(mapping['destinationPointer'])), 'EXTRACTION', 'DESTINATION_ROOT')
            if 'when' in mapping:
                require(set(mapping['when']) == {'allOf'} and bool(mapping['when']['allOf']),
                        'EXTRACTION', 'CONDITION_SHAPE')
                for condition in mapping['when']['allOf']:
                    require(set(condition) == {'pointer', 'equals'}, 'EXTRACTION', 'CONDITION_SHAPE')
                    tokens(condition['pointer'])


def extract(value, profile):
    selected = []
    for mapping in profile['mappings']:
        if not all(digest(pointer(value, c['pointer'])) == digest(c['equals']) for c in mapping.get('when', {}).get('allOf', [])):
            continue
        try:
            item = pointer(value, mapping['sourcePointer'])
        except CheckError as error:
            if error.code == 'POINTER_MISSING' and mapping['required'] is False:
                continue
            raise
        destination = tokens(mapping['destinationPointer'])
        for existing, _ in selected:
            n = min(len(existing), len(destination))
            require(existing[:n] != destination[:n], 'EXTRACTION', 'DESTINATION_CONFLICT')
        selected.append((destination, item))
    result = {}
    for path, value in selected:
        parent = result
        for i, key in enumerate(path):
            last = i == len(path) - 1
            child = copy.deepcopy(value) if last else ([] if re.fullmatch(r'0|[1-9][0-9]*', path[i + 1]) else {})
            if isinstance(parent, list):
                require(re.fullmatch(r'0|[1-9][0-9]*', key) is not None,
                        'EXTRACTION', 'DESTINATION_CONTAINER')
                index = int(key)
                require(index <= len(parent), 'EXTRACTION', 'DESTINATION_GAP')
                if index == len(parent):
                    parent.append(child)
                if not last:
                    parent = parent[index]
            else:
                require(isinstance(parent, dict), 'EXTRACTION', 'DESTINATION_CONTAINER')
                if key not in parent or last:
                    parent[key] = child
                if not last:
                    parent = parent[key]
    return result


def check_component(profile_id, value):
    if profile_id != 'EI_OPERATION_ASSERTION_V0_2':
        return
    for node in objects(value):
        if 'profile' in node and 'start' in node and 'end' in node:
            require(timestamp_ns(node['start']) < timestamp_ns(node['end']), 'COMPONENT', 'INTERVAL_ORDER')
    subject, target = value['subject'], value['resources'][0]['scope']
    if subject['subjectPosture'] == 'PROSPECTIVE_SUBJECT':
        identity = (subject['subjectType'], subject['subjectRef'])
        require(identity != (target['scopeType'], target['scopeRef']),
                'COMPONENT', 'PROSPECTIVE_SUBJECT_IS_ANCHOR')
        for context in value['assertionBody'].get('contextBindings', []):
            require(identity != (context['contextRole'], context['binding']['ref']),
                    'COMPONENT', 'PROSPECTIVE_SUBJECT_IS_CONTEXT')
    same = (subject['subjectPosture'] == 'EXISTING_SUBJECT'
            and subject['subjectType'] == target['scopeType'] and subject['subjectRef'] == target['scopeRef']
            and {k: subject[k] for k in ('revisionRef', 'digest') if k in subject}
            == {k: target[k] for k in ('revisionRef', 'digest') if k in target})
    require(('subjectScopeProofBindings' in value) != same, 'COMPONENT',
            'SUBJECT_SCOPE_PROOF_ABSENCE' if same else 'SUBJECT_SCOPE_PROOF_REQUIRED')
    prior = value.get('supersedesAssertionRecordBinding')
    require(prior is None or prior['ref'] != value['effectSubject']['subjectRef'], 'COMPONENT', 'CORRECTION_SELF_REFERENCE')
    basis = value['assertionBody']['temporalBasis']
    if basis['sourceKind'] == 'BODY_TIME':
        require(basis['time'] == value['subjectTime'], 'COMPONENT', 'BODY_TIME_EQUALITY')


def run_case(case, data, validators, descriptor, artifacts, root):
    kind = case['kind']
    if kind == 'json':
        return strict_loads(case['raw'])
    if kind == 'pointer':
        result = pointer(case['value'], case['pointer'])
        require(digest(result) == digest(case['expectedValue']), 'EXTRACTION', 'POINTER_IDENTITY')
        return
    if kind == 'canonical':
        digest(case['value'])
        if 'expected' in case:
            require(rfc8785.dumps(case['value']).decode('utf-8') == case['expected'], 'CANONICAL', 'CANONICAL_VECTOR')
        return
    if kind == 'artifact':
        path = case['path']
        raw = 'MISSING' if case.get('missing') else (root / path).read_bytes() + case['append'].encode()
        load_artifacts(root, data['artifactPins'], {path: raw})
        return
    fixture = data['fixtures'][case['fixture']]
    value = changed(fixture['value'], case.get('edits', []))
    profile_id = fixture['profile']
    try:
        validators[profile_id].validate(value)
    except ValidationError as error:
        raise CheckError('SCHEMA', 'SCHEMA', error.json_path + ': ' + error.message) from error
    check_component(profile_id, value)
    selected_descriptor = changed(descriptor, case.get('descriptorEdits', []))
    verify_descriptor(selected_descriptor, artifacts, data['artifactPins'])
    profile = next(p for p in selected_descriptor['profiles'] if p['profileId'] == profile_id)
    view = extract(value, profile)
    if kind in ('extraction', 'descriptor'):
        expected = changed(fixture['expectedView'], case.get('viewEdits', []))
        require(digest(view) == digest(expected), 'EXTRACTION', 'VIEW_IDENTITY')
    elif kind == 'integrity':
        require(digest(value) == case['expectedDigest'], 'INTEGRITY', 'COMPLETE_INTENT_DIGEST')
    else:
        require(kind == 'component', 'HARNESS', 'UNKNOWN_CASE_KIND', kind)
    digest(value)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--cases', type=Path)
    args = parser.parse_args()
    case_path = args.cases or args.root / CASE_PATH
    if not case_path.is_file():
        print(json.dumps({'result': 'UNAVAILABLE', 'missingPrerequisite': str(case_path)}))
        return 2
    data = strict_loads(case_path.read_bytes())
    require(data['posture'] == 'FICTIONAL_INPUT_COMPONENT_ONLY', 'HARNESS', 'FIXTURE_POSTURE')
    if not data.get('checkpointReady'):
        print(json.dumps({'result': 'UNAVAILABLE', 'missingPrerequisite': 'Frozen real schemas and extraction descriptors',
                          'limit': 'No schema fallback or runtime conclusion.'}))
        return 2
    require(version('rfc8785') == '0.1.4', 'PREREQUISITE', 'CANONICALIZER_VERSION')
    artifacts, registry = load_artifacts(args.root, data['artifactPins'])
    descriptor = artifacts[data['extractorPath']]
    verify_descriptor(descriptor, artifacts, data['artifactPins'])
    formats = FormatChecker()

    @formats.checks('date-time', raises=(ValueError, TypeError))
    def calendar(value):
        if isinstance(value, str):
            timestamp_ns(value)
        return True

    by_id = {pin['schemaId']: artifacts[pin['path']] for pin in data['artifactPins'] if pin['kind'] == 'schema'}
    validators = {p['profileId']: Draft202012Validator(by_id[p['intentSchemaBinding']['schemaRef']],
                  registry=registry, format_checker=formats) for p in descriptor['profiles']}
    names = [c['name'] for c in data['cases']]
    require(len(names) == len(set(names)), 'HARNESS', 'DUPLICATE_CASE_NAME')
    require(any(c['expect'] == 'PASS' for c in data['cases']) and any(c['expect'] != 'PASS' for c in data['cases']),
            'HARNESS', 'MISSING_CONTROLS')
    counts, layers, failures, read_pairs = Counter(), Counter(), [], set()
    for case in data['cases']:
        try:
            run_case(case, data, validators, descriptor, artifacts, args.root)
        except CheckError as error:
            if case['expect'] == {'layer': error.layer, 'code': error.code}:
                counts['negativeCases'] += 1
                layers[error.layer] += 1
            else:
                failures.append({'name': case['name'], 'expected': case['expect'],
                                 'actual': {'layer': error.layer, 'code': error.code}, 'detail': error.detail})
        else:
            if case['expect'] == 'PASS':
                counts['positiveCases'] += 1
                if 'readCoverage' in case:
                    value = data['fixtures'][case['fixture']]['value']
                    target = value['resources'][0]
                    target_kind = target['scope']['scopeType'] if target['targetType'] == 'SCOPE' else target['resourceKind']
                    require(case['readCoverage'] == [target_kind, value['readForm']], 'HARNESS', 'FALSE_COVERAGE_LABEL')
                    read_pairs.add((target_kind, value['readForm']))
            else:
                failures.append({'name': case['name'], 'expected': case['expect'], 'actual': 'ACCEPTED'})
    expected_pairs = {(kind, form) for kind in data['requiredReadKinds'] for form in ('DIRECT', 'QUERY')}
    require(len(expected_pairs) == 60, 'HARNESS', 'READ_KIND_SET')
    if read_pairs != expected_pairs:
        failures.append({'name': 'read-kind-form-coverage', 'missing': sorted(expected_pairs - read_pairs)})
    print(json.dumps({'result': 'FAIL' if failures else 'PASS', 'profiles': len(validators),
                      'fixtures': len(data['fixtures']), **counts, 'negativeRejectionLayers': dict(layers),
                      'readKindFormPairs': len(read_pairs), 'failures': failures,
                      'artifactPins': data['artifactPins'], 'deferredGuarantees': data['deferredGuarantees'],
                      'limit': 'Fictional input shapes, exact identity extraction and byte integrity only. Query compatibility, authority, foreign proofs, trusted time, transaction and disclosure remain deferred.'}, indent=2))
    return 1 if failures else 0


if __name__ == '__main__':
    try:
        import rfc8785
        from jsonschema import Draft202012Validator, FormatChecker, ValidationError
        from referencing import Registry, Resource
        from referencing.exceptions import NoSuchResource
    except ImportError as error:
        print(json.dumps({'result': 'UNAVAILABLE', 'missingPrerequisite': str(error)}))
        sys.exit(2)
    try:
        sys.exit(main())
    except CheckError as error:
        print(json.dumps({'result': 'FAIL', 'layer': error.layer, 'code': error.code, 'detail': error.detail}, indent=2))
        sys.exit(1)
