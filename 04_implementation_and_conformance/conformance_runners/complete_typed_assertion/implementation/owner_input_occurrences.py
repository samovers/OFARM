"""Domain-side provenance of actual owner API arguments, independent of outcome.

These are invocation arguments, not a claim that a foreign checker interpreted
every supplied record. Byte arguments match independently pinned originals.
Structured controls retain their actual values' digests without being recast
as original bytes, source JSON fields or a storage producer selection.
"""
from duty_graph import PREREQUISITES
from owner_calls import FIELDS
from strict_inputs import digest, sha


# Concrete API argument shapes, checked against the existing transport API.
# No semantic source roles or internal owner read policies are introduced.
BYTE_FIELDS = {
    'act': ('act_bytes', 'content_bytes', 'rendered_bytes', 'context_bytes',
            'policy_bytes', 'intent_profile_bytes'),
    'event': ('proof_bytes', 'envelope_bytes', 'request_bytes', 'context_bytes', 'profile_bytes'),
    'state': ('proof_bytes', 'context_bytes', 'policy_bytes', 'snapshot_bytes'),
    'authorization': ('evidence_bytes', 'profile_bytes', 'context_bytes'),
    'occupancy': ('request_bytes', 'context_bytes'),
}
BYTE_MAPS = {
    'act': ('source_inputs', 'schema_bundle'),
    'event': (), 'state': ('records',),
    'authorization': ('source_bytes', 'schema_bytes'),
    'occupancy': ('records',),
}
CONTROL_FIELDS = {
    'act': ('trusted_pins', 'expected_act_selection'),
    'event': ('trusted_pins', 'expected_proof_binding', 'use_mode'),
    'state': ('selected',),
    'authorization': ('expected_context_sha256',),
    'occupancy': ('trusted_pins',),
}


def collect(bound, attempts, original_intent_bytes):
    """Return requirement/use rows for domain-observed invocation attempts.

    ``attempts`` is created at verify_domain's actual call sites; no public
    argument may supply it. Each attempt names owner, gate, invocationId,
    inputs and outcome. Missing owners retain their known API obligations.
    Exact byte identity is insufficient for source admission or live C4.
    """
    for owner in FIELDS:
        declared = (*BYTE_FIELDS[owner], *BYTE_MAPS[owner], *CONTROL_FIELDS[owner])
        if len(set(declared)) != len(declared) or set(declared) != FIELDS[owner]:
            raise ValueError('Owner argument coverage differs from actual API: ' + owner)
    pins = bound['selection']['originalSelections']
    pin_indexes = {pin['inputId']: i for i, pin in enumerate(pins)}
    requirements, uses, coverage = [], [], []
    seen = set()
    for attempt in attempts:
        owner = attempt['owner']; invocation = attempt['invocationId']; gate = attempt['gate']
        if owner not in FIELDS or invocation in seen:
            raise ValueError('Unknown or duplicate actual owner invocation.')
        seen.add(invocation)
        inputs = attempt.get('inputs')
        valid = type(inputs) is dict and set(inputs) == FIELDS[owner]
        finding_ids = [fid for fid, deps in PREREQUISITES.items() if gate in deps]
        # Occupancy is a per-atom AR_BODY interpretation, not a top-level owner gate.
        if owner == 'occupancy':
            finding_ids = ['AR_BODY']
        prefix = 'owner-argument:' + str(len(coverage)) + ':'
        guard_id = prefix + 'invocation'
        guard = {'id': guard_id, 'kind': 'CANDIDATE_OWNER_INVOCATION_GUARD',
                 'role': 'ACTUAL_OWNER_API_INVOCATION', 'edgeClass': 'CONDITIONAL',
                 'origin': {'inputRole': 'DOMAIN_OWNER_CALL_SITE', 'invocationId': invocation},
                 'inputIds': [], 'dependsOn': [], 'findingIds': finding_ids,
                 'disposition': 'PASS' if valid else 'NOT_EVALUATED' if inputs is None else 'FAIL',
                 'owner': owner, 'outcome': attempt.get('outcome', 'NOT_RETURNED'),
                 'diagnostics': [] if valid else [{'code': 'OWNER_ARGUMENTS_UNAVAILABLE' if inputs is None
                                                   else 'OWNER_API_ARGUMENT_SHAPE_MISMATCH'}],
                 'qualification': 'Actual domain call-site selection only; outcome does not select input coverage.'}
        requirements.append(guard)
        rows = []

        def control(path, value, available, *, set_keys=None):
            rid = prefix + str(len(rows)); rows.append(rid)
            # API control arguments have no independently established original
            # origin in this interface. Hashing their values does not create one.
            item = {'id': rid, 'kind': 'CANDIDATE_OWNER_CONTROL_OCCURRENCE',
                    'role': 'OWNER_API_CONTROL' if set_keys is None else 'OWNER_API_BYTE_MAP_KEYS',
                    'edgeClass': 'SELECTION_GUARD',
                    'origin': {'inputRole': 'DOMAIN_OWNER_CALL_SITE', 'invocationId': invocation,
                               'argumentPath': path},
                    'inputIds': [], 'dependsOn': [guard_id], 'findingIds': finding_ids,
                    'disposition': 'NOT_EVALUATED',
                    'diagnostics': [{'code': 'CONTROL_ORIGINAL_PROVENANCE_PENDING' if available
                                     else 'OWNER_CONTROL_ARGUMENT_UNAVAILABLE'}]}
            if available:
                try:
                    item['argumentValueDigest'] = digest(value)
                except (ValueError, TypeError):
                    item['diagnostics'] = [{'code': 'OWNER_CONTROL_ARGUMENT_NOT_JSON'}]
            if set_keys is not None:
                item['argumentKeys'] = set_keys
            requirements.append(item)
            return rid

        def byte_argument(path, raw, extra_deps=()):
            rid = prefix + str(len(rows)); rows.append(rid)
            row = {'id': rid, 'kind': 'CANDIDATE_OWNER_INPUT_OCCURRENCE',
                   'role': 'OWNER_API_BYTE_ARGUMENT', 'edgeClass': 'REQUIRED_ORIGINAL_READ',
                   'origin': {'inputRole': 'DOMAIN_OWNER_CALL_SITE', 'invocationId': invocation,
                              'argumentPath': path},
                   'inputIds': [], 'dependsOn': [guard_id, *extra_deps], 'findingIds': finding_ids,
                   'disposition': 'NOT_EVALUATED', 'diagnostics': [],
                   'qualification': 'Byte argument at the actual domain call site; transmission, foreign-checker internal reads and admitted use are not asserted.'}
            if not isinstance(raw, bytes):
                row['diagnostics'].append({'code': 'OWNER_BYTE_ARGUMENT_UNAVAILABLE' if raw is None
                                          else 'OWNER_ARGUMENT_NOT_BYTES'})
            else:
                raw_sha = sha(raw)
                row['argumentRawSha256'] = raw_sha; row['argumentByteLength'] = len(raw)
                matches = [pin for pin in pins if pin['rawSha256'] == raw_sha
                           and pin['byteLength'] == len(raw)]
                row['candidateInputIds'] = [pin['inputId'] for pin in matches]
                if len(matches) != 1:
                    row['diagnostics'].append({'code': 'OWNER_ARGUMENT_ORIGINAL_NOT_SELECTED' if not matches
                                              else 'OWNER_ARGUMENT_ORIGINAL_IDENTITY_AMBIGUOUS'})
                else:
                    pin = matches[0]; iid = pin['inputId']
                    row['inputIds'] = [iid]
                    row['digestMode'] = pin['digestMode']
                    row['dependsOn'].append('selected-original:' + str(pin_indexes[iid]))
                    status = bound['inventoryResults'][iid]['status']
                    row['disposition'] = {'MATCHED': 'PASS', 'MISMATCH': 'FAIL',
                                          'NOT_EVALUATED': 'NOT_EVALUATED'}[status]
                    row['diagnostics'].append({'code': 'OWNER_ARGUMENT_ORIGINAL_' + status})
                    uses.append({'id': rid + ':use', 'requirementId': rid, 'inputId': iid,
                                 'classification': 'DOMAIN_OWNER_TRANSPORT_ARGUMENT',
                                 'digestMode': pin['digestMode'],
                                 'treatment': {'kind': 'NOT_EVALUATED',
                                               'reason': 'OWNER_USE_AND_PROTECTED_TREATMENT_REMAIN_SEPARATE'}})
            requirements.append(row)

        data = inputs if isinstance(inputs, dict) else {}
        for field in BYTE_FIELDS[owner]:
            byte_argument([field], data.get(field))
        if owner == 'act':
            byte_argument(['intent_bytes'], original_intent_bytes)
        for field in BYTE_MAPS[owner]:
            mapping = data.get(field)
            shape_ok = type(mapping) is dict and all(isinstance(k, str) for k in mapping)
            keys = list(mapping) if shape_ok else []
            set_id = control([field], keys, shape_ok, set_keys=keys)
            if shape_ok:
                for key, raw in mapping.items():
                    byte_argument([field, key], raw, (set_id,))
        for field in CONTROL_FIELDS[owner]:
            control([field], data.get(field), field in data)
        coverage.append({'invocationId': invocation, 'owner': owner, 'gate': gate,
                         'outcome': attempt.get('outcome', 'NOT_RETURNED'),
                         'status': 'API_PATHS_RECORDED', 'requirementIds': [guard_id, *rows],
                         'argumentShapeValid': valid,
                         'byteArguments': sum(r['kind'] == 'CANDIDATE_OWNER_INPUT_OCCURRENCE'
                                              for r in requirements if r['id'] in rows),
                         'controls': sum(r['kind'] == 'CANDIDATE_OWNER_CONTROL_OCCURRENCE'
                                         for r in requirements if r['id'] in rows)})
    return {'schemaVersion': 'candidate.ownerArgumentOccurrences.v0.1',
            'requirements': requirements, 'uses': uses, 'readerCoverage': coverage,
            'qualification': 'All declared API argument paths for actual domain attempts; no owner-internal read, source admission, live C4 or publication claim.'}
