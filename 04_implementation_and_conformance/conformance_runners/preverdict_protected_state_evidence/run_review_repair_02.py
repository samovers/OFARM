"""Replayable authored regression cases for PR51 B1 and F1-F3; fictional inputs."""
import argparse
import copy
import json
from pathlib import Path

from jsonschema import Draft202012Validator
from run_conformance import raw, sha, binding
from verify_state import verify_state

ROOT = Path(__file__).resolve().parents[3]
PACKAGE = ROOT / '03_machine_contracts/drafts_non_default/authorization_finalization_evidence/protected_state_evidence'
FIXTURES = ROOT / '04_implementation_and_conformance/examples_and_fixtures/fixtures/preverdict_protected_state_evidence'


def load_case(name):
    catalog = json.loads((FIXTURES / 'fixtures/positive-cases.json').read_bytes())
    folder = FIXTURES / next(x['path'] for x in catalog['cases'] if x['id'] == name)
    case = {k: json.loads((folder / (k + '.json')).read_bytes()) for k in ['context', 'policy', 'snapshot', 'proof', 'selected']}
    case['records'] = {ref: (folder / path).read_bytes() for ref, path in json.loads((folder / 'records.json').read_bytes()).items()}
    return case


def rebind(case):
    context, proof, snapshot = case['context'], case['proof'], case['snapshot']
    context['attempt']['transactionSnapshot'] = binding(snapshot, snapshot['snapshotId'])
    proof['snapshot'] = copy.deepcopy(context['attempt']['transactionSnapshot'])
    proof['context'] = binding(context, context['contextId'])
    case['selected'].update(contextRawSha256=sha(raw(context)), policyRawSha256=sha(raw(case['policy'])),
                            proofBinding=binding(proof, proof['proofId']))


def add_read(case, value, *, mode='RAW_BYTES', fixed=False, key='raw', ref='fixture:source-observation', role='EVIDENCE', revision=None):
    selected = {'ref': ref} if mode == 'RAW_BYTES' else binding(json.loads(value), ref)
    if revision is not None:
        selected['revisionRef'] = revision
    spec = {'key': key, 'role': role, 'digestMode': mode, 'binding': selected, 'rawSha256': sha(value),
            'availability': 'FIXED_BEFORE_DOMAIN_VERDICT' if fixed else 'COMMITTED_AT_TRANSACTION_START'}
    guard = {k: copy.deepcopy(v) for k, v in spec.items() if k != 'role'}
    if fixed:
        spec['fixedInputVersion'] = 'fixture:fixed:' + key
        guard.update(fixedInputVersion=spec['fixedInputVersion'], observedVersion=spec['fixedInputVersion'])
    else:
        case['snapshot']['positiveRecords'].append({k: copy.deepcopy(spec[k]) for k in ['key', 'digestMode', 'binding', 'rawSha256']} |
                                                  {'rowVersion': 'row:1', 'visibility': 'COMMITTED_AT_TRANSACTION_START'})
        guard.update(snapshotVersion='row:1', observedVersion='row:1')
    case['context']['requiredReads'].append(spec)
    case['proof']['readGuards'].append(guard)
    case['records'][ref] = value
    rebind(case)
    return case


def replace_record(case, ref, value):
    case['records'][ref] = raw(value)
    def update(spec):
        if spec['binding']['ref'] == ref:
            spec.update(binding=binding(value, ref), rawSha256=sha(raw(value)))
    for group in [case['context']['requiredReads'], case['snapshot']['positiveRecords'], case['proof']['readGuards']]:
        for spec in group:
            update(spec)
    for spec in case['context'].get('priorAssertion', {}).values():
        update(spec)
    rebind(case)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    validator = Draft202012Validator(json.loads((PACKAGE / 'schemas/report.schema.json').read_bytes()))
    rows = []
    base = load_case('assert_operation_claim-initial')
    original = (FIXTURES / 'fixtures/review-repair-02/occupancy-original.bin').read_bytes()
    assert sha(original) == '4f247c24ed1a700c237beca3b4571d24d946594be7a9bdd4bd4ae1160647e5ff'

    def run(name, case, expected='CONDITIONAL_CONFORMANCE_PASS', code=None, facts_check=None):
        rebind(case)
        result = verify_state(raw(case['proof']), package_root=PACKAGE, selected=case['selected'],
                              context_bytes=raw(case['context']), policy_bytes=raw(case['policy']),
                              snapshot_bytes=raw(case['snapshot']), records=case['records'], source_root=FIXTURES)
        valid = not list(validator.iter_errors(result))
        facts_ok = facts_check(result.get('facts', {})) if facts_check and result['status'] == expected else not facts_check
        ok = result['status'] == expected and valid and (not code or any(e['code'] == code for e in result['errors'])) and facts_ok
        rows.append({'id': name, 'expectedStatus': expected, 'requiredError': code, 'status': result['status'], 'pass': ok})
        # Every input and output can be replayed through the public CLI; no saved
        # report is treated as an oracle by this script.
        folder = args.output_dir / name
        folder.mkdir(exist_ok=True)
        for key in ['context', 'policy', 'snapshot', 'proof', 'selected']:
            (folder / (key + '.json')).write_bytes(raw(case[key]))
        mapping = {}
        for index, (ref, value) in enumerate(case['records'].items()):
            path = 'record-' + str(index) + '.bin'
            (folder / path).write_bytes(value)
            mapping[ref] = path
        (folder / 'records.json').write_bytes(raw(mapping))
        (folder / 'report.json').write_bytes(raw(result))
        return result

    def attack(name, mutate, source, expected='FAIL', code=None):
        case = copy.deepcopy(source)
        mutate(case)
        return run(name, case, expected, code)

    committed = add_read(copy.deepcopy(base), original)
    fixed = add_read(copy.deepcopy(base), original, fixed=True)
    def raw_fact(facts):
        row = facts['readBindings'][-1]
        return row['rawSha256'] == sha(original) and row['digestMode'] == 'RAW_BYTES' and 'digest' not in row['binding'] and row['role'] == 'EVIDENCE' and row['key'] == 'raw' and 'observedVersion' in row
    run('occupancy-original-committed', committed, facts_check=raw_fact)
    run('occupancy-original-fixed', fixed, facts_check=lambda f: raw_fact(f) and f['readBindings'][-1]['fixedInputVersion'] == 'fixture:fixed:raw')
    for label, value in [('empty', b''), ('binary', b'\x00\xff\xfe\x80'), ('uint64-json', b'{"value":18446744073709551615}'),
                         ('duplicate-json', b'{"value":1,"value":2}'), ('bom', b'\xef\xbb\xbf{}'), ('surrogate-json', b'{"text":"\\ud800"}')]:
        for fixed_input in [False, True]:
            run(label + ('-fixed' if fixed_input else '-committed'), add_read(copy.deepcopy(base), value, fixed=fixed_input))
    # Supporting records retain source-specific schemaVersion values; detection
    # of recognized later artifacts must be total over arbitrary decoded JSON.
    for label, version in [('object', {'sourceSpecific': 1}), ('array', ['source', 1]),
                           ('empty-object', {}), ('empty-array', [])]:
        value = raw({'schemaVersion': version, 'measurement': 12.5})
        for digest_mode in ['JCS_JSON', 'RAW_BYTES']:
            for fixed_input in [False, True]:
                run('source-schemaVersion-' + label + '-' + digest_mode + '-' + str(fixed_input),
                    add_read(copy.deepcopy(base), value, mode=digest_mode, fixed=fixed_input),
                    facts_check=lambda f, value=value: f['readBindings'][-1]['rawSha256'] == sha(value))
    attack('raw-byte-substitution', lambda c: c['records'].__setitem__('fixture:source-observation', original + b' '), committed, code='BYTES_raw')
    attack('missing-raw-original', lambda c: c['records'].pop('fixture:source-observation'), committed, code='BYTES_raw')
    attack('raw-hash-in-jcs-field', lambda c: c['context']['requiredReads'][-1]['binding'].update(digest='sha256:' + sha(original)), committed, expected='INPUT_ERROR', code='SCHEMA')
    attack('missing-raw-positive', lambda c: c['snapshot']['positiveRecords'].pop(), committed, code='READ_COVERAGE')
    attack('changed-raw-row-version', lambda c: c['proof']['readGuards'][-1].update(observedVersion='changed'), committed, code='READ_VERSION_raw')
    attack('changed-raw-fixed-version', lambda c: c['proof']['readGuards'][-1].update(observedVersion='changed'), fixed, code='FIXED_INPUT_VERSION_raw')
    attack('wrong-raw-guard-hash', lambda c: c['proof']['readGuards'][-1].update(rawSha256='0'*64), committed, code='READ_BINDING_raw')
    attack('missing-raw-guard', lambda c: c['proof']['readGuards'].pop(), committed, code='READ_COVERAGE')
    for role in ['EFFECT_INTENT', 'TRANSACTION_PROFILE', 'TRANSACTION_TIME_POLICY', 'PRIOR_ASSERTION', 'PRIOR_CREATION_EVIDENCE']:
        attack('forbidden-raw-role-' + role, lambda c, role=role: c['context']['requiredReads'][-1].update(role=role), committed, expected='INPUT_ERROR', code='SCHEMA')
    attack('raw-oversize', lambda c: c['records'].__setitem__('fixture:source-observation', b'x'*(2097152+1)), committed, expected='INPUT_ERROR')
    case = add_read(copy.deepcopy(base), b'{}')
    add_read(case, b'{}', key='alias', mode='JCS_JSON')
    run('conflicting-modes-one-ref', case, 'INPUT_ERROR')
    case = copy.deepcopy(committed)
    add_read(case, original, key='alias', fixed=True)
    run('conflicting-availability-one-ref', case, 'FAIL', 'REF_CONSISTENCY_alias')
    case = copy.deepcopy(fixed)
    add_read(case, original, key='alias', fixed=True)
    run('conflicting-fixed-version-one-ref', case, 'FAIL', 'REF_CONSISTENCY_alias')
    case = copy.deepcopy(committed)
    add_read(case, original, key='alias', role='PAYLOAD')
    run('same-ref-two-roles', case)
    attack('conflicting-guard-version-one-ref', lambda c: c['proof']['readGuards'][-1].update(snapshotVersion='row:2', observedVersion='row:2'), case, code='REF_GUARD_CONSISTENCY_alias')
    for revision, role in [('rev:A', 'SUBJECT'), ('rev:B', 'RULE')]:
        case = add_read(copy.deepcopy(base), b'{"evidence":true}', mode='JCS_JSON', role=role, revision=revision)
        run('full-facts-' + role, case, facts_check=lambda f, rev=revision, role=role: f['readBindings'][-1]['role'] == role and f['readBindings'][-1]['binding']['revisionRef'] == rev and f['readBindings'][-1]['snapshotVersion'] == 'row:1')
    case = add_read(copy.deepcopy(base), original, revision='rev:A')
    attack('guard-revision-mismatch', lambda c: c['proof']['readGuards'][-1]['binding'].update(revisionRef='rev:B'), case, code='READ_BINDING_raw')
    attack('conflicting-outer-revision', lambda c: c['context']['requiredReads'][-1].update(revisionRef='rev:B'), case, code='READ_REVISION_raw')
    for group in [case['context']['requiredReads'], case['snapshot']['positiveRecords'], case['proof']['readGuards']]:
        group[-1]['revisionRef'] = 'rev:A'
    run('full-outer-revision-facts', case, facts_check=lambda f: f['readBindings'][-1]['revisionRef'] == 'rev:A')
    case = copy.deepcopy(committed)
    member = {'ref': 'fixture:source-observation', 'digestMode': 'RAW_BYTES', 'rawSha256': sha(original)}
    for group in [case['context']['requiredSetReads'], case['snapshot']['setRecords'], case['proof']['setGuards']]:
        group[0]['members'].append(copy.deepcopy(member))
    run('raw-committed-set-member', case)
    def wrong_member(c):
        for group in [c['context']['requiredSetReads'], c['snapshot']['setRecords'], c['proof']['setGuards']]:
            group[0]['members'][-1]['rawSha256'] = '0'*64
    attack('wrong-raw-set-member-pin', wrong_member, case, code='SET_MEMBERS_fixture:eligibility-set:one')
    # All family/kind combinations and absence of an event preserve complete raw
    # source content. These are byte-custody cases, never semantic admission.
    for family in [None, 'StructureEvent', 'ObservationEvent', 'OccurrenceEvent', 'InterventionEvent', 'MaterialEvent', 'EvidenceEvent', 'GovernanceEvent']:
        for kind in ['NUMERIC', 'CODED', 'QUALITATIVE', 'CENSORED_NUMERIC', 'ABSENT_PENDING']:
            payload = raw({'eventFamily': family, 'resultKind': kind, 'original': ['12.500', 'µg/L', '<0.05', None, False],
                           'time': {'start': '2026-04-08T08:00:00Z', 'end': '2026-04-08T09:00:00Z'}, 'support': 'PARTIAL_WINDOW'})
            run('raw-content-' + str(family) + '-' + kind, add_read(copy.deepcopy(base), payload),
                facts_check=lambda f, payload=payload: f['readBindings'][-1]['rawSha256'] == sha(payload))
    current = base['context']['attempt']['transactionAttemptId']
    for name, value in [
        ('receipt', {'schemaVersion': 'ofarm.notRequiredGovernedEffectReceipt.v0.1', 'attempt': {'transactionAttemptId': current}}),
        ('consumption', {'schemaVersion': 'ofarm.notRequiredDecisionConsumption.v0.1', 'attempt': {'transactionAttemptId': current}}),
        ('checkpoint', {'transactionAttemptId': current, 'authorizationEvaluatedAt': '2026-04-08T08:00:00Z', 'writeAuthorizationCheckedAt': '2026-04-08T08:00:00Z'}),
        ('gate', {'transactionAttemptId': current, 'gateId': 'DOMAIN', 'disposition': 'PASS'})]:
        for mode in ['JCS_JSON', 'RAW_BYTES']:
            run('later-' + name + '-' + mode, add_read(copy.deepcopy(base), raw(value), mode=mode, fixed=True, role='OTHER_DOMAIN_INPUT'), 'FAIL', 'NO_LATER_ARTIFACT_raw')
    prior = {'schemaVersion': 'ofarm.notRequiredGovernedEffectReceipt.v0.1', 'attempt': {'transactionAttemptId': 'fixture:older'}}
    run('prior-attempt-artifact-control', add_read(copy.deepcopy(base), raw(prior), mode='JCS_JSON', role='OTHER_DOMAIN_INPUT'))
    correction = load_case('assert_operation_claim-correction-prior_governed_receipt')
    creation_ref = correction['context']['priorAssertion']['creationEvidence']['binding']['ref']
    def relabel(c):
        v = json.loads(c['records'][creation_ref])
        v['creationKind'] = 'LEGACY_IMMUTABLE_INGRESS'
        v.pop('creatorAttemptId')
        v['sourceDerivations'].pop('creatorAttemptId')
        replace_record(c, creation_ref, v)
    attack('governed-source-relabelled-legacy', relabel, correction, code='CREATION_DERIVATION_creationKind')
    def missing_route(c):
        v = json.loads(c['records'][creation_ref]);v['sourceDerivations'].pop('creationKind');replace_record(c, creation_ref, v)
    attack('missing-creation-route-derivation', missing_route, correction, code='SCHEMA')
    run('creation-route-in-facts', correction, facts_check=lambda f: f['priorCreationKind'] == 'PRIOR_GOVERNED_RECEIPT')
    summary = {'status': 'PASS' if all(r['pass'] for r in rows) else 'FAIL', 'checks': len(rows), 'passed': sum(r['pass'] for r in rows),
               'kind': 'AUTHORED_REPLAYABLE_REVIEW_REGRESSIONS', 'runtimeProtection': 'NOT_ESTABLISHED', 'rows': rows}
    (args.output_dir / 'results.json').write_bytes(raw(summary))
    print(json.dumps({k: v for k, v in summary.items() if k != 'rows'}))
    if summary['status'] != 'PASS':
        print(json.dumps([r for r in rows if not r['pass']], indent=2))
    return int(summary['status'] != 'PASS')


if __name__ == '__main__':
    raise SystemExit(main())
