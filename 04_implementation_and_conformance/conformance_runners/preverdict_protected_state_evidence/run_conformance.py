"""Authored storage-owner conformance cases; saved reports are never an oracle."""
import argparse
import copy
import hashlib
import json
import subprocess
import shutil
import sys
import tempfile
from pathlib import Path

import rfc8785
from jsonschema import Draft202012Validator
from verify_state import verify_state


def raw(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode()


def sha(value):
    return hashlib.sha256(value).hexdigest()


def digest(value):
    return 'sha256:' + sha(rfc8785.dumps(value))


def binding(value, ref):
    return {'ref': ref, 'digest': digest(value)}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--package-root', type=Path, default=Path(__file__).resolve().parent)
    p.add_argument('--fixture-root', type=Path, default=Path(__file__).resolve().parent)
    p.add_argument('--source-root', type=Path)
    p.add_argument('--output-dir', type=Path, required=True)
    a = p.parse_args()
    a.output_dir.mkdir(parents=True, exist_ok=True)
    report_schema = json.loads((a.package_root / 'schemas/report.schema.json').read_bytes())
    rows = []
    catalog = json.loads((a.fixture_root / 'fixtures/positive-cases.json').read_bytes())['cases']
    def load(row):
        root = a.fixture_root / row['path']
        s = {k: json.loads((root / (k + '.json')).read_bytes()) for k in ['proof', 'context', 'snapshot', 'policy', 'selected']}
        s['records'] = {ref: json.loads((root / name).read_bytes()) for ref, name in json.loads((root / 'records.json').read_bytes()).items()}
        return s
    def rebind(s, records=False):
        c, q, snap = s['context'], s['proof'], s['snapshot']
        if records:
            def update(spec):
                ref = spec['binding']['ref']
                if ref in s['records']:
                    spec['binding'] = binding(s['records'][ref], ref)
                    spec['rawSha256'] = sha(raw(s['records'][ref]))
            for spec in c['requiredReads']:
                update(spec)
            for key in ['effectIntent', 'proposedAssertion', 'transactionProfile', 'transactionTimePolicy']:
                update(c[key])
            if 'priorAssertion' in c:
                for spec in c['priorAssertion'].values():
                    update(spec)
            for spec in snap['positiveRecords'] + q['readGuards'] + q['proposedDomainWrites']:
                update(spec)
            c['attempt']['transactionTimePolicyBinding'] = c['transactionTimePolicy']['binding']
            # Exact set memberships are independently reselected for changed
            # fictional source bytes; predicate/version changes are not repaired.
            for group in [c['requiredSetReads'], snap['setRecords'], q['setGuards']]:
                for item in group:
                    item['members'] = [binding(s['records'][b['ref']], b['ref']) if b['ref'] in s['records'] else b for b in item['members']]
        c['attempt']['transactionSnapshot'] = binding(snap, snap['snapshotId'])
        c['attempt']['guardPolicyBinding'] = binding(s['policy'], s['policy']['policyId'])
        q['snapshot'] = copy.deepcopy(c['attempt']['transactionSnapshot'])
        q['guardPolicy'] = copy.deepcopy(c['attempt']['guardPolicyBinding'])
        q['context'] = binding(c, c['contextId'])
        s['selected'].update(contextRawSha256=sha(raw(c)), policyRawSha256=sha(raw(s['policy'])), proofBinding=binding(q, q['proofId']))
    def run(name, s, expected, code=None, override=None):
        kwargs = {'proof_bytes': raw(s['proof']), 'package_root': a.package_root, 'selected': s['selected'],
                  'context_bytes': raw(s['context']), 'policy_bytes': raw(s['policy']), 'snapshot_bytes': raw(s['snapshot']),
                  'records': {k: raw(v) for k, v in s['records'].items()}, 'source_root': a.source_root}
        if override:
            kwargs.update(override)
        result = verify_state(**kwargs)
        shape = not list(Draft202012Validator(report_schema).iter_errors(result))
        ok = result['status'] == expected and shape and (not code or any(e['code'] == code for e in result['errors']))
        rows.append({'id': name, 'expectedStatus': expected, 'requiredCode': code, 'status': result['status'], 'reportSchemaValid': shape, 'pass': ok})
        (a.output_dir / (name + '.report.json')).write_bytes(raw(result))
        return result
    for row in catalog:
        run(row['id'], load(row), 'CONDITIONAL_CONFORMANCE_PASS')
    base = load(catalog[3])
    correction = load(catalog[4])
    receipt_correction = load(catalog[5])
    def attack(name, change, code=None, source=base, expected='FAIL', refresh=False):
        s = copy.deepcopy(source)
        change(s)
        rebind(s, records=refresh)
        return run(name, s, expected, code)
    attack('wrong-owner', lambda s: s['proof'].update(storageOwnerRef='fixture:wrong-owner'), 'OWNER')
    attack('wrong-attempt', lambda s: s['proof'].update(transactionAttemptId='fixture:other-attempt'), 'ATTEMPT')
    attack('wrong-snapshot-attempt', lambda s: s['snapshot'].update(transactionAttemptId='fixture:other-attempt'), 'ATTEMPT')
    attack('wrong-boundary', lambda s: s['snapshot'].update(atomicPersistenceBoundaryRef='fixture:other-boundary'), 'ATOMIC_BOUNDARY')
    attack('missing-read-guard', lambda s: s['proof']['readGuards'].pop(), 'READ_COVERAGE')
    attack('missing-positive-observation', lambda s: s['snapshot']['positiveRecords'].pop(), 'READ_COVERAGE')
    attack('duplicate-read-key', lambda s: s['proof']['readGuards'].append(copy.deepcopy(s['proof']['readGuards'][0])), 'DUPLICATE_KEY')
    attack('changed-read-version', lambda s: s['proof']['readGuards'][0].update(observedVersion='changed'), 'READ_VERSION_intent')
    attack('missing-negative-guard', lambda s: s['proof'].update(negativeGuards=[]), 'SCHEMA', expected='INPUT_ERROR')
    attack('changed-negative-version', lambda s: s['proof']['negativeGuards'][0].update(observedVersion='changed'), 'NEGATIVE_VERSION_' + base['context']['proposedAssertionId'])
    attack('changed-negative-predicate', lambda s: s['proof']['negativeGuards'][0].update(predicateDigest='sha256:' + '0'*64), 'NEGATIVE_PREDICATE_' + base['context']['proposedAssertionId'])
    attack('missing-set-guard', lambda s: s['proof'].update(setGuards=[]), 'SET_COVERAGE')
    attack('changed-set-members', lambda s: s['proof']['setGuards'][0].update(members=[]), 'SET_PREDICATE_fixture:eligibility-set:one')
    attack('changed-set-version', lambda s: s['proof']['setGuards'][0].update(observedVersion='changed'), 'SET_VERSION_fixture:eligibility-set:one')
    attack('additional-assertion', lambda s: s['proof']['proposedDomainWrites'].append(copy.deepcopy(s['proof']['proposedDomainWrites'][0])), 'ONE_EXACT_INSERT')
    attack('event-write', lambda s: s['proof']['proposedDomainWrites'].append(s['proof']['proposedDomainWrites'][0] | {'recordType': 'SemanticEventEnvelope', 'key': 'fixture:extra-event'}), 'ONE_EXACT_INSERT')
    for operation in ['UPDATE', 'DELETE']:
        attack('forbidden-' + operation.lower(), lambda s, v=operation: s['proof']['proposedDomainWrites'][0].update(operation=v), 'ONE_EXACT_INSERT')
    attack('current-state-write', lambda s: s['proof']['proposedDomainWrites'][0].update(recordType='CurrentState'), 'ONE_EXACT_INSERT')
    attack('changed-write-bytes', lambda s: s['proof']['proposedDomainWrites'][0].update(rawSha256='0'*64), 'ONE_EXACT_INSERT')
    attack('wrong-result-id', lambda s: s['context'].update(proposedAssertionId='fixture:different'), 'RESULT_ID')
    attack('cyclic-receipt', lambda s: s['proof'].update(currentAttemptReceipt={'ref': 'fixture:future', 'digest': 'sha256:'+'0'*64}), 'SCHEMA', expected='INPUT_ERROR')
    attack('cyclic-verdict', lambda s: s['context'].update(domainVerdict={'disposition': 'PASS'}), 'SCHEMA', expected='INPUT_ERROR')
    attack('late-snapshot', lambda s: s['snapshot'].update(capturePhase='AFTER_DOMAIN_VERDICT'), 'SCHEMA', expected='INPUT_ERROR')
    attack('uncommitted-prior', lambda s: s['snapshot']['positiveRecords'][3].update(visibility='UNCOMMITTED'), 'SCHEMA', source=correction, expected='INPUT_ERROR')
    for stamp in ['2026-10-21T24:00:00Z', '2026-02-29T08:00:00Z', '2026-10-21T08:60:00Z', '2026-10-21T08:00:60Z', '2026-10-21T08:00:00+00:00', '2026-10-21T08:00:00.10Z', '2026-10-21T08:00:00.0000001Z']:
        attack('timestamp-' + str(len(rows)), lambda s, v=stamp: s['context']['attempt'].update(transactionStartedAt=v), expected='INPUT_ERROR')
    attack('expired-at-start', lambda s: s['context']['attempt'].update(transactionDeadline=s['context']['attempt']['transactionStartedAt']), 'ATTEMPT_DEADLINE')
    def fixed(s, key):
        spec = next(v for v in s['context']['requiredReads'] if v['key'] == key)
        spec.update(availability='FIXED_BEFORE_DOMAIN_VERDICT', fixedInputVersion='fixture:fixed-version:' + key)
        s['snapshot']['positiveRecords'] = [v for v in s['snapshot']['positiveRecords'] if v['key'] != key]
        guard = next(v for v in s['proof']['readGuards'] if v['key'] == key)
        guard.pop('snapshotVersion')
        guard.update(availability=spec['availability'], fixedInputVersion=spec['fixedInputVersion'], observedVersion=spec['fixedInputVersion'])
        for group in [s['context']['requiredSetReads'], s['snapshot']['setRecords'], s['proof']['setGuards']]:
            for item in group:
                item['members'] = [copy.deepcopy(s['context']['transactionProfile']['binding'])]
    s = copy.deepcopy(base)
    fixed(s, 'intent')
    rebind(s)
    run('fixed-validation-phase-input', s, 'CONDITIONAL_CONFORMANCE_PASS')
    f = copy.deepcopy(s)
    f['proof']['readGuards'][0]['observedVersion'] = 'changed'
    rebind(f)
    run('changed-fixed-input-version', f, 'FAIL', 'FIXED_INPUT_VERSION_intent')
    attack('prior-not-visible-at-start', lambda s: fixed(s, 'prior-record'), 'PRIOR_READ_record', source=correction)
    attack('creation-extraction-during-validation', lambda s: fixed(s, 'prior-creation'), source=correction, expected='CONDITIONAL_CONFORMANCE_PASS')
    def creation_value(s):
        return s['records'][s['context']['priorAssertion']['creationEvidence']['binding']['ref']]
    attack('wrong-creation-owner', lambda s: creation_value(s).update(storageOwnerRef='fixture:other'), 'CREATION_OWNER', source=correction, refresh=True)
    attack('creation-current-attempt', lambda s: creation_value(s).update(creatorAttemptId=s['context']['attempt']['transactionAttemptId']), 'PRIOR_ATTEMPT', source=receipt_correction, refresh=True)
    attack('governed-creation-missing-attempt', lambda s: creation_value(s).pop('creatorAttemptId'), 'SCHEMA', source=receipt_correction, refresh=True)
    attack('creation-source-after-start', lambda s: fixed(s, 'prior-source'), 'CREATION_SOURCE_COMMITTED_' + creation_value(correction)['sourceRecords'][0]['binding']['ref'], source=correction)
    attack('wrong-governance-boundary', lambda s: creation_value(s)['governanceContext'].update(boundaryRef='fixture:other'), 'GOVERNANCE_CONTEXT', source=correction, refresh=True)
    attack('wrong-twin', lambda s: creation_value(s)['governanceContext']['twin'].update(twinRef='fixture:other'), 'GOVERNANCE_CONTEXT', source=correction, refresh=True)
    attack('wrong-creation-id', lambda s: creation_value(s).update(creationEvidenceId='fixture:other'), 'CREATION_ID', source=correction, refresh=True)
    attack('broken-source-selector', lambda s: creation_value(s)['sourceDerivations']['governanceContext'].update(pointer='/missing'), 'CREATION_DERIVATION_governanceContext', source=correction, refresh=True)
    attack('extra-creation-source', lambda s: creation_value(s)['sourceRecords'].append(copy.deepcopy(creation_value(s)['sourceRecords'][0])), 'DUPLICATE_CREATION_SOURCE', source=correction, refresh=True)
    attack('null-creation-record', lambda s: s['records'].__setitem__(s['context']['priorAssertion']['creationEvidence']['binding']['ref'], None), 'SCHEMA', source=correction, refresh=True)
    attack('unselected-record', lambda s: s['records'].update({'fixture:unselected': {'x': 1}}), 'INPUT_RECORD_SET')
    attack('missing-record', lambda s: s['records'].pop(s['context']['effectIntent']['binding']['ref']), 'BYTES_intent')
    # Full opaque content remains bound across every event family and measurement
    # result kind. These cases establish byte fidelity, not domain admission.
    # Exact vocabularies from the pinned active envelope and measurement schemas.
    for family in ['StructureEvent', 'ObservationEvent', 'OccurrenceEvent', 'InterventionEvent', 'MaterialEvent', 'EvidenceEvent', 'GovernanceEvent']:
        for kind in ['NUMERIC', 'CODED', 'QUALITATIVE', 'CENSORED_NUMERIC', 'ABSENT_PENDING']:
            s = copy.deepcopy(base)
            v = s['records'][s['context']['effectIntent']['binding']['ref']]
            v['associatedSemanticEventContent']['primaryEventFamily'] = family
            v['measurementContent'] = {'resultKind': kind, 'exactValues': ['12.500', 'µg/L', 'not reported', False, 0], 'allOriginalContent': v['sourceClaimBytes']}
            rebind(s, records=True)
            result = run('opaque-' + family + '-' + kind, s, 'CONDITIONAL_CONFORMANCE_PASS')
            assert result['facts']['readBindings'][0]['binding']['digest'] == digest(v)
    # Hash preservation is tested separately from semantic mutation rebinding.
    changed = {k: raw(v) for k, v in base['records'].items()}
    changed[base['context']['effectIntent']['binding']['ref']] += b' '
    run('changed-raw-source-whitespace', base, 'FAIL', 'BYTES_intent', {'records': changed})
    for name, data in [('duplicate-json', b'{"x":1,"x":2}'), ('bom', b'\xef\xbb\xbf{}'), ('invalid-utf8', b'"\xff"'), ('nonfinite', b'{"x":NaN}'), ('unsafe-integer', b'{"x":9007199254740992}'), ('deep-json', b'['*66+b'0'+b']'*66), ('oversize', b' '*(2097152+1))]:
        run(name, base, 'INPUT_ERROR', override={'proof_bytes': data})
    s = copy.deepcopy(base)
    s['selected']['contextRawSha256'] = '0'*64
    run('wrong-independent-context-pin', s, 'INPUT_ERROR')
    s = copy.deepcopy(base)
    s['selected']['proofBinding']['digest'] = 'sha256:'+'0'*64
    run('wrong-independent-proof-binding', s, 'FAIL', 'INDEPENDENT_PROOF_BINDING')
    # Bad packages must fail structurally, including a schema-valid but wrong
    # report contract. Offered pins never replace the frozen supported closure.
    with tempfile.TemporaryDirectory(prefix='state-package-') as directory:
        package = Path(directory)
        for name in ['schemas', 'source-contracts']:
            shutil.copytree(a.package_root / name, package / name)
        shutil.copytree((a.source_root or a.package_root) / 'sources', package / 'sources')
        original_contract = (a.package_root / 'contract.json').read_bytes()
        (package / 'contract.json').write_bytes(original_contract)
        for path in ['schemas/proof.schema.json', 'schemas/report.schema.json', 'source-contracts/transaction.v0.2.schema.json', 'sources/transaction-rfc.md']:
            target = package / path
            original = target.read_bytes()
            target.write_bytes(b'{}')
            run('package-mismatch-' + target.name, base, 'INPUT_ERROR', override={'package_root': package, 'source_root': package})
            target.write_bytes(original)
        s = copy.deepcopy(base)
        c = json.loads(original_contract)
        c['schemas'][0]['rawSha256'] = '0'*64
        c['contractDigest'] = digest({k:v for k,v in c.items() if k!='contractDigest'})
        (package / 'contract.json').write_bytes(raw(c))
        s['selected']['contractRawSha256'] = sha(raw(c))
        run('unsupported-reselected-schema-closure', s, 'INPUT_ERROR', override={'package_root': package, 'source_root': package})
        (package / 'contract.json').write_bytes(b'{}')
        s['selected']['contractRawSha256'] = sha(b'{}')
        run('malformed-selected-contract', s, 'INPUT_ERROR', override={'package_root': package, 'source_root': package})
    run('missing-package', base, 'INPUT_ERROR', override={'package_root': a.output_dir / 'absent'})
    # Exercise the actual CLI once, independently of the in-process API calls.
    cli_case = a.fixture_root / catalog[0]['path']
    command = [sys.executable, '-B', str(Path(__file__).with_name('verify_state.py')),
               '--package-root', str(a.package_root), '--report', str(a.output_dir / 'cli.report.json')]
    for name in ['context', 'policy', 'snapshot', 'proof']:
        command += ['--' + name, str(cli_case / (name + '.json'))]
    command += ['--selection', str(cli_case / 'selected.json'), '--records-manifest', str(cli_case / 'records.json')]
    if a.source_root:
        command += ['--source-root', str(a.source_root)]
    cli = subprocess.run(command, capture_output=True, text=True)
    cli_report = json.loads((a.output_dir / 'cli.report.json').read_bytes()) if (a.output_dir / 'cli.report.json').exists() else {}
    rows.append({'id':'public-cli','pass':cli.returncode==0 and cli_report.get('status')=='CONDITIONAL_CONFORMANCE_PASS','exitCode':cli.returncode})
    summary = {'status': 'PASS' if all(r['pass'] for r in rows) else 'FAIL', 'checks': len(rows), 'passed': sum(r['pass'] for r in rows),
               'runtimeProtection': 'NOT_ESTABLISHED', 'primaryTrustBoundary': 'Transaction and history evidence for protected proposed state',
               'scopeStayedInsideBoundary': True, 'rows': rows}
    (a.output_dir / 'conformance-report.json').write_bytes(raw(summary))
    print(json.dumps({k: v for k, v in summary.items() if k != 'rows'}))
    if summary['status'] != 'PASS':
        print(json.dumps([r for r in rows if not r['pass']], indent=2))
    return 0 if summary['status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
