"""Bounded domain provenance for a proposed #51 identity comparison.

The caller supplies the independently selected #47 action, exact public result
bytes, the actual guarded v0.4 original-inventory report, and the C3 partial
requirement graph. This module does not call a storage owner or infer its
transaction facts from an offered #51 context. Its result is always partial.
"""

import sys
from pathlib import Path

from strict_inputs import InputError, digest, parse, sha
from original_inputs import selected_index


SELECTION_VERSION = 'ofarm.assertionDomainEvaluationSelection.v0.4'
SELECTION_SCHEMA_SHA256 = 'b0f5ffdc4e97ab745c6e666dcbbeef8ee4485efdb265251904f5447e966b03d9'
GRAPH_VERSION = 'candidate.partialOriginalRequirementGraph.v0.1'
ACTIONS = {'ASSERT_STRUCTURE', 'ASSERT_OPERATION_CLAIM', 'ASSERT_COMPLIANCE'}
IDENTITY_FIELDS = ('actionClass', 'storageOwnerRef', 'transactionAttemptId',
                   'atomicPersistenceBoundaryRef', 'proposedAssertionId')
HERE = Path(__file__).resolve().parent
RESULT_SCHEMA_ID = 'https://ofarm.dev/schema/drafts/non-default/assertion-record-domain-validation/result/v0.1'
RESULT_SCHEMA_SHA256 = 'f3362cbbb135584f8d7c96dcf01c27c60e727b48b1b1f8700f9f57ec0bbe9f05'
PROPOSITION_SCHEMA_ID = 'https://ofarm.dev/schema/drafts/non-default/assertion-domain/proposition/v0.1'
PROPOSITION_SCHEMA_SHA256 = '0d50b7a4685109cdc015ebd60ddf7d136a1e1416b4c881c71428ca659001f746'


def _pending(code):
    return {'disposition': 'NOT_EVALUATED', 'diagnostics': [{'code': code}]}


def _failed(code):
    return {'disposition': 'FAIL', 'diagnostics': [{'code': code}]}


def _pinned_result_schema_status(result):
    """Use the candidate's exact schema registry and format checks.

    The static schema hashes are the reviewed domain pins, not values supplied
    by the caller or the offered state context. Runtime/schema resolution
    problems stay distinct from an actual result shape error.
    """
    try:
        result_raw = (HERE / 'outer/carriers/result.schema.json').read_bytes()
        proposition_raw = (HERE / 'components/revision-02/proposition.schema.json').read_bytes()
    except OSError:
        return 'RESULT_SCHEMA_UNAVAILABLE'
    if sha(result_raw) != RESULT_SCHEMA_SHA256 or sha(proposition_raw) != PROPOSITION_SCHEMA_SHA256:
        return 'RESULT_SCHEMA_PIN_MISMATCH'
    try:
        result_schema, proposition_schema = parse(result_raw), parse(proposition_raw)
        if (result_schema.get('$id') != RESULT_SCHEMA_ID
                or proposition_schema.get('$id') != PROPOSITION_SCHEMA_ID):
            return 'RESULT_SCHEMA_ID_MISMATCH'
        component_root = str(HERE / 'components/revision-02')
        if component_root not in sys.path:
            sys.path.insert(0, component_root)
        import runtime_support
        from referencing import Registry, Resource
        if Path(runtime_support.__file__).resolve() != (Path(component_root) / 'runtime_support.py').resolve():
            return 'RESULT_SCHEMA_REGISTRY_CONFLICT'
        schemas = runtime_support.Schemas()
        if schemas.schemas.get(PROPOSITION_SCHEMA_ID) != proposition_schema:
            return 'RESULT_SCHEMA_REGISTRY_CONFLICT'
        schemas.schemas[RESULT_SCHEMA_ID] = result_schema
        schemas.registry = Registry().with_resources(
            (key, Resource.from_contents(value)) for key, value in schemas.schemas.items())
        errors = schemas.errors(RESULT_SCHEMA_ID, result)
    except (InputError, ValueError, TypeError, KeyError, OSError, ImportError,
            AttributeError, RecursionError):
        return 'RESULT_SCHEMA_VALIDATION_UNAVAILABLE'
    if any(error.get('code') == 'SCHEMA_RESOLUTION_ERROR' for error in errors):
        return 'RESULT_SCHEMA_VALIDATION_UNAVAILABLE'
    return 'RESULT_SCHEMA_INVALID' if errors else 'PASS'


def derive(independent_selected_action, original_result_bytes, *, selection_bytes=None,
           independent_selection_raw_sha256=None, checked_inventory=None,
           partial_requirement_graph=None):
    """Derive only identity members supported by independently selected inputs.

    The caller must already have verified the package manifest and action
    selection, and obtained checked_inventory through the guarded worker. A
    supplied report object alone is not an authenticated owner response.
    Missing C3 or inventory evidence leaves the proposed ID NOT_EVALUATED;
    contradictory claimed PASS evidence is FAIL. No complete expected identity
    vector or C4 PASS digest is issued here.
    """
    if not isinstance(independent_selected_action, str) or independent_selected_action not in ACTIONS:
        raise InputError('Independently selected domain action is invalid.')
    fields = {
        'actionClass': {
            'disposition': 'PASS', 'value': independent_selected_action,
            'source': {'role': 'INDEPENDENT_DOMAIN_ACTION',
                       'pointer': '/package/selectedAction'}, 'diagnostics': []},
        'storageOwnerRef': _pending('TRUSTED_STORAGE_OWNER_SOURCE_UNAVAILABLE'),
        'transactionAttemptId': _pending('TRUSTED_TRANSACTION_ATTEMPT_SOURCE_UNAVAILABLE'),
        'atomicPersistenceBoundaryRef': _pending('TRUSTED_ATOMIC_BOUNDARY_SOURCE_UNAVAILABLE'),
        'proposedAssertionId': _pending('GUARDED_PROPOSED_ORIGINAL_UNAVAILABLE'),
    }
    selected_inputs = (selection_bytes, independent_selection_raw_sha256,
                       checked_inventory, partial_requirement_graph)
    if all(item is not None for item in selected_inputs):
        fields['proposedAssertionId'] = _proposed_id(
            original_result_bytes, selection_bytes, independent_selection_raw_sha256,
            checked_inventory, partial_requirement_graph)
    return {'schemaVersion': 'candidate.partialProtectedIdentityProvenance.v0.1',
            'scope': 'ASSERTION_RECORD_DOMAIN_IDENTITY_ONLY', 'status': 'PARTIAL',
            'localDisposition': ('FAIL' if any(row['disposition'] == 'FAIL' for row in fields.values())
                                 else 'NOT_EVALUATED'),
            'fields': fields, 'sourceAdmission': 'NOT_ESTABLISHED',
            'runtimeProtection': 'NOT_ESTABLISHED',
            'qualification': 'Known identity members only; no full expected vector or C4 PASS.'}


def _proposed_id(raw, selection_bytes, independent_sha, inventory, graph):
    if not isinstance(selection_bytes, bytes) or not isinstance(independent_sha, str):
        return _failed('INDEPENDENT_SELECTION_PIN_INVALID')
    if sha(selection_bytes) != independent_sha:
        return _failed('INDEPENDENT_SELECTION_RAW_PIN_MISMATCH')
    if (not isinstance(inventory, dict)
            or inventory.get('selectionShapeValidated') != 'EXACT_REVIEWED_V0_4_SCHEMA_AND_UNIQUENESS'
            or inventory.get('selectionSchemaRawSha256') != SELECTION_SCHEMA_SHA256):
        return _failed('GUARDED_V0_4_INVENTORY_INVALID')
    try:
        selection, by_id, _, results, admitted = selected_index(selection_bytes, inventory)
    except (InputError, AttributeError, TypeError, KeyError, ValueError):
        return _failed('GUARDED_INVENTORY_SELECTION_CONFLICT')
    if selection.get('schemaVersion') != SELECTION_VERSION:
        return _failed('SELECTED_SCHEMA_VERSION_MISMATCH')
    if inventory.get('selectionBinding', {}).get('wholeJcsDigest') != digest(selection):
        return _failed('GUARDED_SELECTION_VALUE_BINDING_CONFLICT')
    if not isinstance(graph, dict) or graph.get('schemaVersion') != GRAPH_VERSION:
        return _failed('C3_GRAPH_INVALID')
    root_bindings = graph.get('rootBindings')
    root = root_bindings.get('proposedAssertion') if isinstance(root_bindings, dict) else None
    if not isinstance(root, dict):
        return _pending('C3_PROPOSED_ROOT_UNAVAILABLE')
    if root.get('disposition') == 'FAIL':
        return _failed('C3_PROPOSED_ROOT_FAILED')
    if root.get('disposition') != 'PASS':
        return _pending('C3_PROPOSED_ROOT_NOT_EVALUATED')
    iid = root.get('inputId')
    pin = by_id.get(iid) if isinstance(iid, str) else None
    if (root.get('role') != 'PROPOSED_ASSERTION' or pin is None
            or pin.get('digestMode') != 'JCS_JSON'
            or root.get('selectedRef') != pin.get('ref')
            or root.get('selectedRawSha256') != pin.get('rawSha256')
            or results[iid].get('status') != 'MATCHED'
            or results[iid].get('observedRawSha256') != pin.get('rawSha256')
            or results[iid].get('byteLength') != pin.get('byteLength')):
        return _failed('C3_PROPOSED_ROOT_INVENTORY_CONFLICT')
    if not isinstance(raw, bytes):
        return _failed('PUBLIC_PROPOSED_ORIGINAL_UNAVAILABLE')
    if sha(raw) != pin['rawSha256'] or len(raw) != pin['byteLength']:
        return _failed('PUBLIC_PROPOSED_ORIGINAL_RAW_MISMATCH')
    try:
        result = parse(raw)
    except InputError:
        return _failed('PUBLIC_PROPOSED_ORIGINAL_JSON_INVALID')
    if (not isinstance(result, dict) or digest(result) != pin.get('wholeJcsDigest')
            or admitted.get(iid) != result):
        return _failed('PUBLIC_PROPOSED_ORIGINAL_VALUE_MISMATCH')
    assertion_id = result.get('assertionRecordId')
    schema_status = _pinned_result_schema_status(result)
    if schema_status in {'RESULT_SCHEMA_PIN_MISMATCH', 'RESULT_SCHEMA_ID_MISMATCH',
                         'RESULT_SCHEMA_REGISTRY_CONFLICT'}:
        return _failed(schema_status)
    if schema_status != 'PASS':
        return _pending(schema_status)
    if not isinstance(assertion_id, str) or not assertion_id:
        return _pending('PUBLIC_PROPOSED_ASSERTION_ID_INVALID')
    return {'disposition': 'PASS', 'value': assertion_id,
            'source': {'role': 'GUARDED_SELECTED_PUBLIC_PROPOSED_ORIGINAL',
                       'inputId': iid, 'ref': pin['ref'],
                       'rawSha256': pin['rawSha256'],
                       'wholeJcsDigest': pin['wholeJcsDigest'],
                       'resultSchemaRef': RESULT_SCHEMA_ID,
                       'resultSchemaRawSha256': RESULT_SCHEMA_SHA256,
                       'pointer': '/assertionRecordId'}, 'diagnostics': []}


def compare_known_to_offered(provenance, offered_context_bytes):
    """Check only known domain identity members against offered #51 context.

    Matching known members cannot make the five-field vector complete. The
    context never supplies an expected storage owner, attempt, or boundary.
    """
    if (not isinstance(provenance, dict) or provenance.get('status') != 'PARTIAL'
            or provenance.get('schemaVersion') != 'candidate.partialProtectedIdentityProvenance.v0.1'
            or provenance.get('scope') != 'ASSERTION_RECORD_DOMAIN_IDENTITY_ONLY'):
        raise InputError('Partial domain identity provenance is required.')
    fields = provenance.get('fields')
    if not isinstance(fields, dict) or set(fields) != set(IDENTITY_FIELDS):
        raise InputError('Partial domain identity fields are malformed.')
    if any(fields[name].get('disposition') == 'PASS' for name in (
            'storageOwnerRef', 'transactionAttemptId', 'atomicPersistenceBoundaryRef')
            if isinstance(fields[name], dict)):
        raise InputError('A storage identity member cannot be derived from domain originals.')
    if not isinstance(offered_context_bytes, bytes):
        return {'status': 'FAIL', 'scope': 'KNOWN_IDENTITY_MEMBERS_ONLY',
                'comparisons': [], 'diagnostics': [{'code': 'OFFERED_CONTEXT_BYTES_INVALID'}]}
    try:
        context = parse(offered_context_bytes)
    except InputError:
        return {'status': 'FAIL', 'scope': 'KNOWN_IDENTITY_MEMBERS_ONLY',
                'comparisons': [], 'diagnostics': [{'code': 'OFFERED_CONTEXT_JSON_INVALID'}]}
    if not isinstance(context, dict):
        return {'status': 'FAIL', 'scope': 'KNOWN_IDENTITY_MEMBERS_ONLY',
                'comparisons': [], 'diagnostics': [{'code': 'OFFERED_CONTEXT_SHAPE_INVALID'}]}
    comparisons = []
    for name in IDENTITY_FIELDS:
        field = fields[name]
        if not isinstance(field, dict):
            raise InputError('Partial domain identity member is malformed.')
        if field.get('disposition') == 'PASS':
            equal = type(context.get(name)) is str and context[name] == field.get('value')
            comparisons.append({'field': name, 'disposition': 'PASS' if equal else 'FAIL',
                                'code': 'KNOWN_IDENTITY_MATCH' if equal else 'KNOWN_IDENTITY_CONTRADICTION'})
        elif field.get('disposition') == 'FAIL':
            comparisons.append({'field': name, 'disposition': 'FAIL',
                                'code': 'INDEPENDENT_IDENTITY_PROVENANCE_FAILED'})
        else:
            comparisons.append({'field': name, 'disposition': 'NOT_EVALUATED',
                                'code': 'INDEPENDENT_IDENTITY_MEMBER_UNAVAILABLE'})
    return {'status': 'FAIL' if any(row['disposition'] == 'FAIL' for row in comparisons)
            else 'NOT_EVALUATED', 'scope': 'KNOWN_IDENTITY_MEMBERS_ONLY',
            'comparisons': comparisons, 'diagnostics': [],
            'sourceAdmission': 'NOT_ESTABLISHED', 'runtimeProtection': 'NOT_ESTABLISHED'}
