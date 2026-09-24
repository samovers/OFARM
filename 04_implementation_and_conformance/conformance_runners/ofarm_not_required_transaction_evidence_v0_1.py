#!/usr/bin/env python3
"""Fictional contract-component checks; never a runtime or commit-status oracle."""
from __future__ import annotations

import copy
import hashlib
import json
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path

import rfc8785
from jsonschema import Draft202012Validator, FormatChecker, ValidationError

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / '03_machine_contracts/drafts_non_default/authorization_finalization_evidence'


class ContractError(ValueError):
    pass


def require(condition, code):
    if not condition:
        raise ContractError(code)


def strict_loads(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'DUPLICATE_JSON_NAME')
            result[key] = value
        return result

    def invalid_constant(_value):
        raise ContractError('NON_JSON_NUMBER')

    return json.loads(raw, object_pairs_hook=pairs, parse_constant=invalid_constant)


MANIFEST = strict_loads((PACKAGE / 'NOT_REQUIRED_TRANSACTION_EVIDENCE_manifest_v0_1.json').read_text())
SCHEMA = strict_loads((ROOT / MANIFEST['schemaPath']).read_text())
PROFILES = {p['definition']: p for p in MANIFEST['profiles']}
FORMATS = FormatChecker()


@FORMATS.checks('date-time', raises=(ValueError, TypeError))
def valid_calendar_time(value):
    if not isinstance(value, str):
        return True  # The schema's type check owns this error.
    datetime.fromisoformat(value.replace('Z', '+00:00'))
    return True


def digest(value):
    try:
        canonical = rfc8785.dumps(value)
    except rfc8785.CanonicalizationError as error:
        raise ContractError('CANONICAL_DOMAIN') from error
    return 'sha256:' + hashlib.sha256(canonical).hexdigest()


def pointer(value, path):
    for part in path.lstrip('/').split('/'):
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def validator(definition, provisional=False):
    definitions = copy.deepcopy(SCHEMA['$defs']) if provisional else SCHEMA['$defs']
    if provisional:
        profile = PROFILES[definition]
        definitions[definition]['properties'][profile['selfDigestMember']] = {'const': profile['provisionalSentinel']}
    return Draft202012Validator({'$schema': SCHEMA['$schema'], '$defs': definitions,
                                '$ref': '#/$defs/' + definition}, format_checker=FORMATS)


def validate_shape(definition, record):
    try:
        validator(definition).validate(record)
        if PROFILES[definition]['rootEvidenceRecord']:
            Draft202012Validator(SCHEMA, format_checker=FORMATS).validate(record)
    except ValidationError as error:
        raise ContractError('SCHEMA') from error


def finalize(definition, record):
    """Build only fictional records, following the profile's exact self exclusion."""
    profile = PROFILES[definition]
    result = copy.deepcopy(record)
    member = profile['selfDigestMember']
    if member:
        result[member] = profile['provisionalSentinel']
        try:
            validator(definition, provisional=True).validate(result)
        except ValidationError as error:
            raise ContractError('PROVISIONAL_SCHEMA') from error
        projection = {k: v for k, v in result.items() if k != member}
        result[member] = digest(projection)
    validate_shape(definition, result)
    return result


def verify_digest(definition, record):
    member = PROFILES[definition]['selfDigestMember']
    if member:
        require(record[member] == digest({k: v for k, v in record.items() if k != member}), 'OWNED_DIGEST')


def record_id(definition, record, carrier_ref=None):
    path = PROFILES[definition]['identityPointer']
    if path is None:
        require(definition == 'operationBinding' and carrier_ref is not None and carrier_ref != record['logicalOperationId'], 'OPERATION_REFERENCE')
        return carrier_ref
    identity = pointer(record, path)
    require(carrier_ref is None or carrier_ref == identity, 'RECORD_ID_BINDING')
    return identity


def binding(definition, record, carrier_ref=None):
    return {'ref': record_id(definition, record, carrier_ref), 'digest': record[PROFILES[definition]['selfDigestMember']]}


def resolve(data, value):
    for item in data['records'].values():
        definition, record = item['definition'], item['value']
        if record_id(definition, record, item['recordRef']) == value['ref']:
            require(binding(definition, record, item['recordRef']) == {k: value[k] for k in ('ref', 'digest')}, 'REFERENCE_DIGEST')
            return record
    external = data['externalRecords'].get(value['ref'])
    require(external is not None and digest(external) == value['digest'], 'FIXTURE_REFERENCE')
    return external  # Only fictional bytes are checked; no foreign owner semantics.


def verify_records(data):
    identities = []
    for item in data['records'].values():
        validate_shape(item['definition'], item['value'])
        verify_digest(item['definition'], item['value'])
        identities.append(record_id(item['definition'], item['value'], item['recordRef']))
        if item['definition'] == 'transactionAttempt':
            record = item['value']
            expected = {'role':'PROTECTED_EFFECT_TRANSACTION', 'atomicPersistenceBoundaryRef':record['attempt']['atomicPersistenceBoundaryRef'],
                        'transactionStatusLookupKey':record['attempt']['transactionStatusLookupKey'], 'transactionAttemptId':record['attempt']['transactionAttemptId']}
            require(expected in record['transactionRoles'], 'TRANSACTION_ROLE_BINDING')
            evidence_role = next((r for r in record['transactionRoles'] if r['role'] == 'SEPARATE_FAILURE_EVIDENCE_COMMIT'), None)
            require(('protectedEffectRollbackProof' in record) == (evidence_role is not None), 'FAILURE_TRANSACTION_BINDING')
            if evidence_role:
                require(evidence_role['transactionStatusLookupKey'] != expected['transactionStatusLookupKey'] and evidence_role['transactionAttemptId'] == expected['transactionAttemptId'], 'FAILURE_TRANSACTION_BINDING')
            for role in record['transactionRoles']:
                if role['role'] == 'FIRST_ADMISSION_COMMIT':
                    require(role == {**(evidence_role or expected), 'role':'FIRST_ADMISSION_COMMIT'}, 'ADMISSION_TRANSACTION_BINDING')
    require(len(identities) == len(set(identities)), 'DUPLICATE_RECORD_ID')


def verify_checkpoint(record):
    attempt, checkpoint = record['attempt'], record['checkpoint']
    start, deadline = (datetime.fromisoformat(attempt[k].replace('Z', '+00:00')) for k in ('transactionStartedAt', 'transactionDeadline'))
    evaluated, end, checked = (datetime.fromisoformat(checkpoint[k].replace('Z', '+00:00')) for k in ('authorizationEvaluatedAt', 'decisionValidUntil', 'writeAuthorizationCheckedAt'))
    require(deadline - start == timedelta(seconds=30), 'ORIGINAL_BUDGET')
    require(start <= evaluated <= checked < end <= deadline, 'CHECKPOINT_ORDER')
    # This is arithmetic on fixture claims, not proof of M0/M1, full D or clock trust.


def tuple_from(operation):
    represented = operation['representedPartyBinding']
    return {'operationBoundaryKind': operation['operationBoundary']['kind'],
            'operationBoundaryRef': operation['operationBoundary']['ref'],
            'authenticatedRequestingPrincipalRef': operation['requestingPrincipalBinding']['authenticatedPrincipalRef'],
            'representedPartyRef': represented['representedPartyRef'] if represented else None,
            'actionClass': operation['actionClass'], 'operationIdempotencyKey': operation['operationIdempotencyKey']}


def check_operation(data, record):
    identity = record['operation']
    operation = resolve(data, identity['operationBinding'])
    require(identity['logicalOperationId'] == operation['logicalOperationId'], 'OPERATION_IDENTITY')
    for key in ('callerSubmissionProjectionDigest', 'effectIntentDigest'):
        require(identity[key] == operation[key], 'OPERATION_IDENTITY')
    require(record['effectIntent'] == {'ref': operation['effectIntentRef'], 'digest': operation['effectIntentDigest']}, 'INTENT_BINDING')
    return operation


def check_mode_identity(mode, operation):
    for key in ('authenticatedPrincipalRef', 'resolvedPrincipalKind'):
        require(mode['requestingPrincipalBinding'][key] == operation['requestingPrincipalBinding'][key], 'CONSUMER_BINDING')
    def represented(record):
        binding = record['representedPartyBinding']
        return binding['representedPartyRef'] if binding is not None else None
    require(represented(mode) == represented(operation), 'REPRESENTATION_BINDING')
    # Current principal/representation revisions may differ from first admission.


def check_admitted_result(data, attempt):
    if 'admittedProtectedResultBinding' in attempt:
        owner = attempt
        reference = {'attempt': binding('transactionAttempt', owner), 'attemptSequence': owner['attempt']['attemptSequence'],
                     'pointer': '/admittedProtectedResultBinding'}
    else:
        reference = attempt['priorAdmittedProtectedResultBinding']
        owner = resolve(data, reference['attempt'])
        validate_shape('transactionAttempt', owner)
        verify_digest('transactionAttempt', owner)
        require(reference['attempt'] == binding('transactionAttempt', owner), 'ADMISSION_BINDING')
        require(reference['attemptSequence'] == owner['attempt']['attemptSequence'] < attempt['attempt']['attemptSequence'], 'ADMISSION_SEQUENCE')
        require(owner['outcome'] == 'NO_EFFECT', 'ADMISSION_OUTCOME')
    check_operation(data, owner)
    require(owner['operation'] == attempt['operation'] and owner['effectIntent'] == attempt['effectIntent'], 'ADMISSION_OPERATION')
    require('admittedProtectedResultBinding' in owner, 'ADMISSION_BINDING')
    admitted = owner['admittedProtectedResultBinding']
    require(admitted['validationTrace'] == owner['protectedEffectValidation']['trace'], 'ADMISSION_TRACE')
    require(admitted['protectedEffectContractBinding'] == owner['protectedEffectContractBinding'] == attempt['protectedEffectContractBinding'], 'RESULT_BINDING')
    return admitted, reference


def gate_members(record):
    return [{'role': 'OTHER_GATE_TRACE', **g['trace']} for g in record['gateTraces'] if 'trace' in g]


def evidence_members(record):
    members = []
    if 'modeEvidence' in record:
        members.append({'role': 'NOT_REQUIRED_MODE_EVIDENCE', **record['modeEvidence']})
    if 'authorizationBundle' in record:
        members.extend({'role': 'AUTHORIZATION_' + role.upper(), **record['authorizationBundle'][role]} for role in ('request', 'result', 'trace'))
    if 'protectedEffectValidation' in record:
        members.append({'role': 'PROTECTED_EFFECT_TRACE', **record['protectedEffectValidation']['trace']})
    return members + gate_members(record)


def verify_members(data, actual, required, self_member):
    require(actual.count(self_member) == 1, 'SELF_MEMBERSHIP')
    for member in actual:
        if member != self_member:
            resolve(data, member)
    require(Counter(rfc8785.dumps(m) for m in actual) == Counter(rfc8785.dumps(m) for m in required + [self_member]), 'MEMBERSHIP')


def projection_member(data, operation):
    matches = [{'role': 'CALLER_PROJECTION', 'ref': name, 'digest': digest(value)}
               for name, value in data['externalRecords'].items()
               if value.get('schemaVersion') == 'ofarm.notRequiredCallerSubmissionProjection.v0.1'
               and digest(value) == operation['callerSubmissionProjectionDigest']]
    require(len(matches) == 1, 'CALLER_PROJECTION')
    validate_shape('callerSubmissionProjection', data['externalRecords'][matches[0]['ref']])
    return matches[0]


def check_common_binding(record, other):
    for field in ('operation', 'attempt', 'actionClass', 'currentActionRuleBinding', 'effectIntentSchemaBinding', 'effectIntent', 'protectedEffectContractBinding', 'governedTransactionProfileBinding'):
        require(record[field] == other[field], 'COMMON_BINDING')


def receipt_attempt(data, receipt):
    attempts = [m for m in receipt['membership'] if m['role'] == 'TRANSACTION_ATTEMPT']
    require(len(attempts) == 1, 'MEMBERSHIP')
    return resolve(data, attempts[0])


def verify_success(data, name):
    receipt = data['records'][name]['value']
    operation = check_operation(data, receipt)
    require(receipt['lookupTuple'] == tuple_from(operation), 'LOOKUP_TUPLE')
    mode = resolve(data, receipt['modeEvidence'])
    consumption = resolve(data, receipt['decisionConsumption'])
    require(consumption['consumingPrincipalBinding'] == mode['requestingPrincipalBinding'], 'CONSUMER_BINDING')
    check_mode_identity(mode, operation)
    attempt = receipt_attempt(data, receipt)
    for record in (mode, consumption, attempt):
        check_operation(data, record)
        check_common_binding(record, receipt)
    for field in ('effectIntentSchemaBinding', 'protectedEffectContractBinding', 'governedTransactionProfileBinding'):
        require(receipt[field] == operation[field], 'ORIGINAL_BINDING')
    for record in (consumption, attempt, receipt):
        verify_checkpoint(record)
        require(record['checkpoint'] == receipt['checkpoint'], 'CHECKPOINT_BINDING')
        require(record['authorizationBundle'] == receipt['authorizationBundle'], 'DECISION_BINDING')
        require(record['modeEvidence'] == receipt['modeEvidence'], 'MODE_BINDING')
        require(record['governedEffectReceiptId'] == receipt['governedEffectReceiptId'], 'RECEIPT_BACKLINK')
    require(attempt['decisionConsumption'] == receipt['decisionConsumption'], 'CONSUMPTION_BINDING')
    require(attempt['completeGuardEvidence'] == receipt['completeGuardEvidence'], 'GUARD_BINDING')
    require(attempt['protectedEffectValidation'] == receipt['protectedEffectValidation'] and attempt['gateTraces'] == receipt['gateTraces'], 'GATE_BINDING')
    admitted_ref = receipt['admittedProtectedResult']
    admitted, expected_ref = check_admitted_result(data, attempt)
    require(admitted_ref['attemptSequence'] == expected_ref['attemptSequence'], 'ADMISSION_SEQUENCE')
    require(admitted_ref == expected_ref, 'ADMISSION_BINDING')
    require(receipt['committedResult'] == {'ref': admitted['resultId'], 'digest': admitted['resultDigest']}, 'RESULT_BINDING')
    require(receipt['resultSchemaBinding'] == admitted['resultSchemaBinding'] and receipt['protectedEffectContractBinding'] == admitted['protectedEffectContractBinding'], 'RESULT_BINDING')
    require(consumption['committedResults'] == [receipt['committedResult']], 'RESULT_BINDING')
    required = [{'role':'OPERATION_BINDING', **receipt['operation']['operationBinding']}, projection_member(data, operation),
                {'role':'TRANSACTION_ATTEMPT', **binding('transactionAttempt', attempt)},
                {'role':'DECISION_CONSUMPTION', **receipt['decisionConsumption']},
                {'role':'PROTECTED_RESULT', **receipt['committedResult']},
                {'role':'ADMITTED_RESULT_BINDING', **admitted_ref['attempt'], 'pointer':admitted_ref['pointer']}, *evidence_members(receipt)]
    verify_members(data, receipt['membership'], required, {'role':'GOVERNED_EFFECT_RECEIPT','ref':receipt['governedEffectReceiptId']})


def verify_no_effect(data, name):
    record = data['records'][name]['value']
    operation = check_operation(data, record)
    if 'modeEvidence' in record:
        mode = resolve(data, record['modeEvidence'])
        require(mode['operation'] == record['operation'] and mode['attempt'] == record['attempt'], 'MODE_BINDING')
        check_common_binding(mode, record)
        check_mode_identity(mode, operation)
    required = [{'role':'OPERATION_BINDING', **record['operation']['operationBinding']}, projection_member(data, operation), *evidence_members(record)]
    required += [{'role':'FAILURE_TRACE', **value} for value in record['failureEvidence']]
    required += [{'role':'QUALIFICATION_EVIDENCE', **value} for value in record.get('qualificationEvidence', [])]
    if 'admittedProtectedResultBinding' in record or 'priorAdmittedProtectedResultBinding' in record:
        _, reference = check_admitted_result(data, record)
        if 'priorAdmittedProtectedResultBinding' in record:
            required.append({'role':'ADMITTED_RESULT_BINDING', **reference['attempt'], 'pointer':reference['pointer']})
    if 'protectedEffectRollbackProof' in record:
        required.append({'role':'ROLLBACK_PROOF', **record['protectedEffectRollbackProof']})
    if 'checkpoint' in record:
        verify_checkpoint(record)  # A later abort must not erase a truthful checkpoint.
    verify_members(data, record['noEffectMembership'], required, {'role':'TRANSACTION_ATTEMPT','ref':record['attempt']['transactionAttemptId']})


def require_transaction_status(record, transaction, status):
    identity_fields = ('atomicPersistenceBoundaryRef', 'transactionStatusLookupKey', 'transactionAttemptId')
    same = [o for o in record['statusObservations'] if all(o['transaction'][k] == transaction[k] for k in identity_fields)]
    require(any(o['transaction']['role'] == transaction['role'] for o in same), 'STATUS_BINDING')
    require(same and all(o['status'] == status for o in same), 'STATUS_BINDING')


def require_declared_statuses(record, attempt):
    require(all(o['transaction'] in attempt['transactionRoles'] for o in record['statusObservations']), 'STATUS_ROLE_BINDING')


def verify_reconciliation(data, name):
    record = data['records'][name]['value']
    for observation in record['statusObservations']:
        require(observation['transaction']['transactionAttemptId'] == record['transactionAttemptId'], 'STATUS_ATTEMPT')
        resolve(data, observation['evidence'])
    if 'resolvedReceipt' in record:
        receipt = resolve(data, record['resolvedReceipt'])
        require(record['operation'] == receipt['operation'] and record['transactionAttemptId'] == receipt['attempt']['transactionAttemptId'] and record['attemptSequence'] == receipt['attempt']['attemptSequence'], 'RECONCILIATION_BINDING')
        if record['resolution'] == 'EFFECT_COMMITTED':
            attempt = receipt_attempt(data, receipt)
            require(attempt['attempt'] == receipt['attempt'], 'RECONCILIATION_BINDING')
            require_transaction_status(record, {'role':'PROTECTED_EFFECT_TRANSACTION', **receipt['attempt']}, 'COMMITTED')
            require_declared_statuses(record, attempt)
    if 'resolvedNoEffectAttempt' in record:
        attempt = resolve(data, record['resolvedNoEffectAttempt'])
        require(attempt['outcome'] == 'NO_EFFECT' and record['operation'] == attempt['operation'] and record['transactionAttemptId'] == attempt['attempt']['transactionAttemptId'] and record['attemptSequence'] == attempt['attempt']['attemptSequence'], 'RECONCILIATION_BINDING')
        evidence_role = next((r for r in attempt['transactionRoles'] if r['role'] == 'SEPARATE_FAILURE_EVIDENCE_COMMIT'), None)
        protected = {'role':'PROTECTED_EFFECT_TRANSACTION', **attempt['attempt']}
        require_transaction_status(record, evidence_role or protected, 'COMMITTED')
        if evidence_role:
            resolve(data, attempt['protectedEffectRollbackProof'])
            require_transaction_status(record, protected, 'ROLLED_BACK')
        require_declared_statuses(record, attempt)
    if 'protectedEffectRollbackProof' in record:
        resolve(data, record['protectedEffectRollbackProof'])
        protected = [o['transaction'] for o in record['statusObservations'] if o['transaction']['role'] == 'PROTECTED_EFFECT_TRANSACTION']
        require(bool(protected) and all(t == protected[0] for t in protected), 'STATUS_BINDING')
        require_transaction_status(record, protected[0], 'ROLLED_BACK')
    # Known rollback may coexist with uncertain evidence persistence, never with safe success.
    if record['resolution'] in ('NO_EFFECT', 'EFFECT_COMMITTED') and any(o['status'] == 'UNKNOWN' for o in record['statusObservations']):
        require(record['resolution'] == 'NO_EFFECT' and bool(record.get('unresolvedFacts')), 'UNRESOLVED_STATUS')
    if 'laterTimeObservation' in record:
        later = record['laterTimeObservation']
        require('resolvedReceipt' in record, 'OBSERVATION_RECEIPT')
        require(later['receipt'] == record['resolvedReceipt'], 'OBSERVATION_RECEIPT')
        resolve(data, later['ownerEvidence'])
        if record['resolution'] == 'EFFECT_COMMITTED':
            observed = utc_nanoseconds(later['observedTransactionTime'])
            checkpoint = utc_nanoseconds(receipt['checkpoint']['writeAuthorizationCheckedAt'])
            require(checkpoint <= observed <= utc_nanoseconds(later['observedAt']) <= utc_nanoseconds(record['observedAt']), 'LATER_CHRONOLOGY')
    # Status truth, original clock domain and observation admissibility remain owner obligations.


def utc_nanoseconds(value):
    """Exact fixture comparison; later owner observations may have nine fractional digits."""
    whole, _, fraction = value[:-1].partition('.')
    delta = datetime.fromisoformat(whole) - datetime(1970, 1, 1)
    return (delta.days * 86400 + delta.seconds) * 1_000_000_000 + int(fraction.ljust(9, '0'))


def mutate(data, edits):
    result = copy.deepcopy(data)
    for edit in edits:
        parts = edit['path'].lstrip('/').split('/')
        parent = result
        for part in parts[:-1]:
            parent = parent[int(part)] if isinstance(parent, list) else parent[part]
        key = int(parts[-1]) if isinstance(parent, list) else parts[-1]
        if edit['op'] == 'remove':
            del parent[key]
        elif edit['op'] == 'append':
            parent[key].append(edit['value'])
        else:
            parent[key] = edit['value']
    return result


def rehash_fixture_records(data):
    """Maintain only fixture digest links, so negative relation tests cannot pass by stale hashes."""
    def replace(value, identity, old, new):
        if isinstance(value, dict):
            if value.get('ref') == identity and value.get('digest') == old:
                value['digest'] = new
            for item in value.values():
                replace(item, identity, old, new)
        elif isinstance(value, list):
            for item in value:
                replace(item, identity, old, new)

    for name in data['constructionOrder']:
        item = data['records'][name]
        definition, record = item['definition'], item['value']
        field = PROFILES[definition]['selfDigestMember']
        old = record[field]
        record[field] = digest({k:v for k,v in record.items() if k != field})
        replace(data['records'], record_id(definition, record, item['recordRef']), old, record[field])


def main():
    Draft202012Validator.check_schema(SCHEMA)
    require(MANIFEST['schemaByteSha256'] == hashlib.sha256((ROOT / MANIFEST['schemaPath']).read_bytes()).hexdigest(), 'SCHEMA_FILE_DIGEST')
    require(MANIFEST['schemaJcsDigest'] == digest(SCHEMA), 'SCHEMA_JCS_DIGEST')
    require(MANIFEST['executable'] is False and MANIFEST['selectedReleaseClosureComplete'] is False and MANIFEST['promotedToCurrentDefault'] is False, 'DRAFT_ONLY')
    data = strict_loads((ROOT / MANIFEST['fixturePath']).read_text())
    require(data['posture'] == 'FICTIONAL_COMPONENT_ONLY', 'FIXTURE_POSTURE')
    verify_records(data)
    counts = Counter()
    dispatch = {'success':verify_success, 'no-effect':verify_no_effect, 'reconciliation':verify_reconciliation}
    for case in data['positiveSets']:
        changed = mutate(data, case.get('edits', []))
        if case.get('rehash'):
            rehash_fixture_records(changed)
        verify_records(changed)
        dispatch[case['kind']](changed, case['record'])
        counts['positiveSets'] += 1
    for case in data['negativeCases']:
        changed = mutate(data, case.get('edits', []))
        if case.get('rehash'):
            rehash_fixture_records(changed)
        try:
            kind = case['kind']
            if kind == 'json':
                strict_loads(case['raw'])
            elif kind == 'canonical-domain':
                digest(case['value'])
            elif kind == 'schema':
                item = changed['records'][case['record']]
                validate_shape(item['definition'], item['value'])
            elif kind == 'schema-without-formats':
                shape = {'$defs':SCHEMA['$defs'], '$ref':'#/$defs/' + case['definition']}
                require(Draft202012Validator(shape).is_valid(case['value']), 'SCHEMA')
            elif kind == 'integrity':
                item = changed['records'][case['record']]
                verify_digest(item['definition'], item['value'])
            else:
                verify_records(changed)
                dispatch[kind](changed, case['record'])
        except ContractError as error:
            require(str(error) == case['error'], case['name'] + ': wrong rejection ' + str(error))
        else:
            raise ContractError(case['name'] + ': accepted invalid fixture')
        counts['negativeCases'] += 1
    for vector in data['canonicalizationVectors']:
        require(rfc8785.dumps(vector['value']).decode() == vector['expected'], 'CANONICAL_VECTOR')
        counts['canonicalizationVectors'] += 1
    for item in data['records'].values():
        require(finalize(item['definition'], item['value']) == item['value'], 'PROVISIONAL_ROUNDTRIP')
        counts['provisionalRoundtrips'] += 1
    print(json.dumps({'result':'PASS', 'profiles':len(PROFILES), 'records':len(data['records']), **counts,
                      'limit':'Fictional syntax, owned digests and record consistency only; no database, authority, guard or clock proof.'}, indent=2))


if __name__ == '__main__':
    main()
