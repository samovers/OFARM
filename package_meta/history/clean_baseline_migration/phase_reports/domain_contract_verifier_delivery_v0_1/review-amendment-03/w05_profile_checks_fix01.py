"""Independent finite W05 owner pins and guards; no runtime source admission."""
import json
from pathlib import Path
from role_checks_v4 import json_type, MISSING

PROFILE = json.loads((Path(__file__).with_name('w05-owner-profile-fix01.json')).read_text())

def same_json(left, right):
    return json.dumps(left, sort_keys=True, separators=(',', ':')) == json.dumps(right, sort_keys=True, separators=(',', ':'))

def profile_errors(expect):
    if not isinstance(expect, dict):
        return [{'code': 'INVALID_OWNER_PROFILE', 'pointer': '/ownerProfile', 'expected': 'object'}]
    errors = []
    def require(code, key, value):
        if not same_json(expect.get(key), value):
            errors.append({'code': code, 'pointer': '/ownerProfile/' + key})
    require('OWNER_PROFILE_CRITERION_MISMATCH', 'criterionOwnerBinding', PROFILE['criterionBinding'])
    require('OWNER_PROFILE_CRITERION_MISMATCH', 'criterionBinding', PROFILE['criterionBinding'])
    require('OWNER_PROFILE_CRITERION_PIN_MISMATCH', 'criterionOwnerDigest', PROFILE['criterionOwnerDigest'])
    require('OWNER_PROFILE_RESULT_KIND_MISMATCH', 'resultKind', PROFILE['requiredResultKind'])
    matches = [x for x in PROFILE['approvedQuantitySources'] if same_json(x['binding'], expect.get('quantityProvenanceBinding'))]
    if len(matches) != 1:
        errors.append({'code': 'UNAPPROVED_QUANTITY_SOURCE_REVISION', 'pointer': '/ownerProfile/quantityProvenanceBinding'})
    else:
        require('OWNER_PROFILE_QUANTITY_PIN_MISMATCH', 'quantityProvenanceDigest', matches[0]['recordDigest'])
    for role, key in [('MEASUREMENT', 'measurementBinding'), ('OBSERVATION_CONTEXT', 'contextBinding'), ('SAMPLE_SUPPORT_RELATION', 'subjectRelationBinding'), ('METHOD_USE_QUALIFICATION', 'methodUseBinding')]:
        if not any(p['role'] == role and same_json(p['binding'], expect.get(key)) for p in PROFILE['measurementSources']):
            errors.append({'code': 'UNAPPROVED_MEASUREMENT_SOURCE_REVISION', 'pointer': '/ownerProfile/' + key})
    return errors

def claim_container_errors(content):
    errors = []
    for key, kind in [('subject', 'object'), ('subjectTime', 'object'), ('evidenceBindings', 'array'), ('ruleRevisionBindings', 'array'), ('evidencePolicyRevisionBindings', 'array')]:
        value = content.get(key, MISSING)
        if json_type(value) != kind:
            errors.append({'code': 'INVALID_TYPE', 'pointer': '/' + key, 'expected': kind, 'actual': json_type(value)})
    scope = content['proposition'].get('scope', MISSING)
    if not isinstance(scope, dict):
        errors.append({'code': 'INVALID_TYPE', 'pointer': '/proposition/scope', 'expected': 'object', 'actual': json_type(scope)})
    return errors

def record_errors(body, records, expect, digest):
    """Guard accessed containers before semantics; check independent measurement pins.

    A well-shaped hostile record may still reach semantic checks to retain their
    useful diagnostics, but an independent pin error always rejects that record.
    """
    if not isinstance(records, list):
        error = {'code': 'INVALID_TYPE', 'pointer': '/resolvedRecords', 'expected': 'array', 'actual': json_type(records)}
        return [error], True
    errors = []
    unsafe = False
    source = body['operand']['source']
    selected = [(source[k], '/operand/source/' + k, role) for k, role in [('measurementBinding', 'MEASUREMENT'), ('contextBinding', 'OBSERVATION_CONTEXT'), ('subjectRelationBinding', 'SAMPLE_SUPPORT_RELATION'), ('methodUseBinding', 'METHOD_USE_QUALIFICATION')]]
    selected += [(body['operand']['limit']['provenance']['sourceBinding'], '/operand/limit/provenance/sourceBinding', 'QUANTITY_PROVENANCE'), (body['threshold']['provenance']['sourceBinding'], '/threshold/provenance/sourceBinding', 'CRITERION_OWNER')]
    for binding, path, role in selected:
        matches = [r for r in records if isinstance(r, dict) and same_json(r.get('binding'), binding)]
        if len(matches) != 1:
            errors.append({'code': 'SOURCE_RESOLUTION_NOT_EXACT', 'pointer': path})
            unsafe = True
            continue
        resolved = matches[0]
        record = resolved.get('record', MISSING)
        if not isinstance(record, dict):
            errors.append({'code': 'INVALID_SOURCE_RECORD_TYPE', 'pointer': path, 'expected': 'object', 'actual': json_type(record)})
            unsafe = True
            continue
        try:
            record_digest = digest(record)
        except (ValueError, TypeError, OverflowError):
            errors.append({'code': 'INVALID_SOURCE_RECORD_VALUE', 'pointer': path})
            unsafe = True
            continue
        if record_digest != resolved.get('contentDigest'):
            errors.append({'code': 'RESOLVED_DIGEST_MISMATCH', 'pointer': path})
        expected_key = {'MEASUREMENT': 'measurementBinding', 'OBSERVATION_CONTEXT': 'contextBinding', 'SAMPLE_SUPPORT_RELATION': 'subjectRelationBinding', 'METHOD_USE_QUALIFICATION': 'methodUseBinding'}.get(role)
        pin = next((p for p in PROFILE['measurementSources'] if p['role'] == role and same_json(p['binding'], expect.get(expected_key))), None)
        if pin is not None:
            if not same_json(binding, pin['binding']):
                errors.append({'code': 'MEASUREMENT_SOURCE_BINDING_MISMATCH', 'pointer': path})
            if record_digest != pin['recordDigest']:
                errors.append({'code': 'MEASUREMENT_SOURCE_PIN_MISMATCH', 'pointer': path, 'role': role})
        fields = {'MEASUREMENT': [('measurementEvidenceId', 'string'), ('source', 'object'), ('labContext', 'object')], 'OBSERVATION_CONTEXT': [('spatialContext', 'object'), ('procedure', 'object'), ('measurementEvidenceRefs', 'array')], 'CRITERION_OWNER': [('operator', 'string'), ('threshold', 'object')]}.get(role, [])
        for key, kind in fields:
            value = record.get(key, MISSING)
            if json_type(value) != kind:
                errors.append({'code': 'INVALID_SOURCE_FIELD_TYPE', 'pointer': path, 'recordPointer': '/' + key, 'expected': kind, 'actual': json_type(value)})
                unsafe = True
    return errors, unsafe
