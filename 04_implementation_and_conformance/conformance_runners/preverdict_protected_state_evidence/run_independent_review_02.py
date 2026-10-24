"""Independent PR51 repair review. All observations are fictional and conditional.

No owner generator/rebinding helpers are imported. Exact inputs and reports are
retained for replay through the frozen public CLI. Run with Python -B.
"""
import argparse
import base64
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

import rfc8785
from jsonschema import Draft202012Validator

CLI = argparse.ArgumentParser(description=__doc__)
CLI.add_argument('--output-dir', type=Path, required=True)
CLI.add_argument('--replay-cli', action='store_true')
ARGS = CLI.parse_args()
HERE = ARGS.output_dir.resolve()
HERE.mkdir(parents=True, exist_ok=True)
ROOT = Path(__file__).resolve().parents[3]
CODE = ROOT / '04_implementation_and_conformance/conformance_runners/preverdict_protected_state_evidence'
PACKAGE = ROOT / '03_machine_contracts/drafts_non_default/authorization_finalization_evidence/protected_state_evidence'
FIXTURES = ROOT / '04_implementation_and_conformance/examples_and_fixtures/fixtures/preverdict_protected_state_evidence'
OUT = HERE / 'independent-cases'
sys.path.insert(0, str(CODE))
module = importlib.util.spec_from_file_location('reviewed_state', CODE / 'verify_state.py')
checker = importlib.util.module_from_spec(module)
module.loader.exec_module(checker)
REPORT = Draft202012Validator(json.loads((PACKAGE / 'schemas/report.schema.json').read_bytes()))
PASS = 'CONDITIONAL_CONFORMANCE_PASS'
COMMITTED = 'COMMITTED_AT_TRANSACTION_START'
FIXED = 'FIXED_BEFORE_DOMAIN_VERDICT'
ROWS = []


def raw(value):
    return (json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(',', ':')) + '\n').encode()


def sha(value):
    return hashlib.sha256(value).hexdigest()


def bind(value, ref):
    return {'ref': ref, 'digest': 'sha256:' + sha(rfc8785.dumps(value))}


def load_case(name):
    catalog = json.loads((FIXTURES / 'fixtures/positive-cases.json').read_bytes())['cases']
    folder = FIXTURES / next(x['path'] for x in catalog if x['id'] == name)
    c = {k: json.loads((folder / (k + '.json')).read_bytes()) for k in ['context', 'proof', 'snapshot', 'policy', 'selected']}
    c['records'] = {ref: (folder / f).read_bytes() for ref, f in json.loads((folder / 'records.json').read_bytes()).items()}
    return c


def seal(c):
    c['context']['attempt']['transactionSnapshot'] = bind(c['snapshot'], c['snapshot']['snapshotId'])
    c['proof']['snapshot'] = copy.deepcopy(c['context']['attempt']['transactionSnapshot'])
    c['proof']['context'] = bind(c['context'], c['context']['contextId'])
    c['selected']['contextRawSha256'] = sha(raw(c['context']))
    c['selected']['policyRawSha256'] = sha(raw(c['policy']))
    c['selected']['proofBinding'] = bind(c['proof'], c['proof']['proofId'])


def add(c, payload, *, mode='RAW_BYTES', fixed=False, key='review-input', ref='review:original', role='EVIDENCE', rev=None, outer=None):
    b = {'ref': ref} if mode == 'RAW_BYTES' else bind(json.loads(payload), ref)
    if rev is not None:
        b['revisionRef'] = rev
    spec = {'key': key, 'binding': b, 'rawSha256': sha(payload), 'availability': FIXED if fixed else COMMITTED, 'role': role}
    if mode is not None:
        spec['digestMode'] = mode
    if outer is not None:
        spec['revisionRef'] = outer
    guard = copy.deepcopy(spec)
    guard.pop('role')
    if fixed:
        spec['fixedInputVersion'] = 'review:fixed:1'
        guard.update(fixedInputVersion='review:fixed:1', observedVersion='review:fixed:1')
    else:
        obs = {k: copy.deepcopy(v) for k, v in spec.items() if k not in ['role', 'availability']}
        obs.update(visibility=COMMITTED, rowVersion='review:row:1')
        c['snapshot']['positiveRecords'].append(obs)
        guard.update(snapshotVersion='review:row:1', observedVersion='review:row:1')
    c['context']['requiredReads'].append(spec)
    c['proof']['readGuards'].append(guard)
    c['records'][ref] = payload
    return c


def replace_record(c, ref, value):
    payload = raw(value)
    c['records'][ref] = payload
    def walk(node):
        if isinstance(node, dict):
            if isinstance(node.get('binding'), dict) and node['binding'].get('ref') == ref:
                node['binding']['digest'] = bind(value, ref)['digest']
                node['rawSha256'] = sha(payload)
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)
    for key in ['context', 'snapshot', 'proof']:
        walk(c[key])


def facts_match(c, result):
    guards = {g['key']: g for g in c['proof']['readGuards']}
    expected = []
    for spec in c['context']['requiredReads']:
        v = copy.deepcopy(spec)
        v.setdefault('digestMode', 'JCS_JSON')
        for key in ['snapshotVersion', 'observedVersion']:
            if key in guards[v['key']]:
                v[key] = guards[v['key']][key]
        expected.append(v)
    return result.get('facts', {}).get('readBindings') == expected


def run(name, c, expected=PASS, code=None, group='other', cli=False, note=''):
    seal(c)
    folder = OUT / name
    folder.mkdir(parents=True, exist_ok=True)
    for k in ['context', 'policy', 'snapshot', 'proof', 'selected']:
        (folder / (k + '.json')).write_bytes(raw(c[k]))
    mapping = {}
    for i, (ref, payload) in enumerate(c['records'].items()):
        name_i = f'record-{i:03d}.bin'
        mapping[ref] = name_i
        (folder / name_i).write_bytes(payload)
    (folder / 'records.json').write_bytes(raw(mapping))
    result = checker.verify_state(raw(c['proof']), package_root=PACKAGE, selected=c['selected'],
                                 context_bytes=raw(c['context']), policy_bytes=raw(c['policy']),
                                 snapshot_bytes=raw(c['snapshot']), records=c['records'], source_root=FIXTURES)
    (folder / 'api-report.json').write_bytes(raw(result))
    codes = [x['code'] for x in result['errors']]
    valid = not list(REPORT.iter_errors(result))
    bounded = result['runtimeProtection'] == 'NOT_ESTABLISHED' and result['laterTransactionGate'] == 'NOT_EVALUATED'
    facts = facts_match(c, result) if result['status'] == PASS else 'facts' not in result
    good = result['status'] == expected and (code is None or code in codes) and valid and bounded and facts
    row = dict(id=name, group=group, expected=expected, requiredCode=code, actual=result['status'], codes=codes,
               reportSchemaValid=valid, limitsRetained=bounded, fullFactsOrNoFailureFacts=facts, pass_=good,
               cliRequested=cli, note=note)
    ROWS.append(row)
    return result


def attack(name, base, mutate, expected='FAIL', code=None, group='guards', cli=False):
    c = copy.deepcopy(base)
    mutate(c)
    return run(name, c, expected, code, group, cli)


def creation_edit(c, edit):
    ref = c['context']['priorAssertion']['creationEvidence']['binding']['ref']
    v = json.loads(c['records'][ref])
    edit(v)
    replace_record(c, ref, v)


def main():
    args = ARGS
    if args.replay_cli:
        return replay_cli()
    for action in ['assert_structure', 'assert_operation_claim', 'assert_compliance']:
        for route in ['initial', 'correction-legacy_immutable_ingress', 'correction-prior_governed_receipt']:
            run('control-' + action + '-' + route, load_case(action + '-' + route), group='controls', cli=True)
    base = load_case('assert_operation_claim-initial')
    original = (FIXTURES / 'fixtures/review-repair-02/occupancy-original.bin').read_bytes()
    assert sha(original) == '4f247c24ed1a700c237beca3b4571d24d946594be7a9bdd4bd4ae1160647e5ff'
    bodies = [('occupancy', original), ('empty', b''), ('nonutf8', b'\x00\xff\x80'),
              ('uint64', b'{"value":18446744073709551615}'), ('duplicates', b'{"x":1,"x":2}'),
              ('surrogate', b'{"x":"\\ud800"}'), ('bom', b'\xef\xbb\xbf{}'),
              ('scalar', b'false'), ('array', b'[1,2,3]'), ('nonfinite', b'{"value":NaN}')]
    for label, payload in bodies:
        for fixed in [False, True]:
            run('raw-' + label + '-' + str(fixed), add(copy.deepcopy(base), payload, fixed=fixed), group='B1-originals', cli=label=='occupancy')
    # These are not transaction artifacts. Their source-specific schemaVersion
    # member has no required type in a supporting read. Expected PASS is written
    # before observing the checker; failure remains in the ledger.
    for label, version in [('object', {'sourceSpecific': 1}), ('array', ['source-v1']),
                           ('empty-object', {}), ('empty-array', []), ('number', 5),
                           ('null', None), ('boolean', False), ('string', 'source.v1')]:
        for mode in ['JCS_JSON', 'RAW_BYTES']:
            for fixed in [False, True]:
                run('schemaVersion-' + label + '-' + mode + '-' + str(fixed),
                    add(copy.deepcopy(base), raw({'schemaVersion': version, 'measurement': 12.5}), mode=mode, fixed=fixed),
                    group='source-specific-schemaVersion', cli=label in ['object','array'] and fixed)
    committed = add(copy.deepcopy(base), original)
    fixed = add(copy.deepcopy(base), original, fixed=True)
    attack('raw-stale-pin', committed, lambda c: c['records'].__setitem__('review:original', original+b'\n'), code='BYTES_review-input', cli=True)
    attack('raw-missing-original', committed, lambda c: c['records'].pop('review:original'), code='BYTES_review-input')
    attack('raw-missing-positive', committed, lambda c: c['snapshot']['positiveRecords'].pop(), code='READ_COVERAGE')
    attack('raw-missing-guard', committed, lambda c: c['proof']['readGuards'].pop(), code='READ_COVERAGE')
    attack('raw-stale-row', committed, lambda c: c['proof']['readGuards'][-1].update(observedVersion='stale'), code='READ_VERSION_review-input')
    attack('raw-stale-fixed', fixed, lambda c: c['proof']['readGuards'][-1].update(observedVersion='stale'), code='FIXED_INPUT_VERSION_review-input', cli=True)
    attack('raw-digest-smuggling', committed, lambda c: c['context']['requiredReads'][-1]['binding'].update(digest='sha256:'+sha(original)), expected='INPUT_ERROR', code='SCHEMA')
    for role in ['EFFECT_INTENT', 'TRANSACTION_PROFILE', 'TRANSACTION_TIME_POLICY', 'PRIOR_ASSERTION', 'PRIOR_CREATION_EVIDENCE']:
        attack('raw-role-'+role, committed, lambda c, role=role: c['context']['requiredReads'][-1].update(role=role), expected='INPUT_ERROR', code='SCHEMA')
    c = add(copy.deepcopy(base), b'{}')
    add(c, b'{}', key='alias', mode='JCS_JSON')
    run('mixed-mode-same-ref', c, 'INPUT_ERROR', 'INPUT_ERROR', 'F1-ref-consistency')
    for availability in [False, True]:
        c = add(copy.deepcopy(committed if not availability else fixed), original, key='alias', role='PAYLOAD', fixed=availability)
        run('same-ref-two-roles-'+str(availability), c, group='F1-ref-consistency')
    c = add(copy.deepcopy(committed), original, key='alias', fixed=True)
    run('mixed-availability-same-ref', c, 'FAIL', 'REF_CONSISTENCY_alias', 'F1-ref-consistency', True)
    c = add(copy.deepcopy(fixed), original, key='alias', fixed=True)
    for group in [c['context']['requiredReads'], c['proof']['readGuards']]:
        group[-1]['fixedInputVersion'] = 'different'
    c['proof']['readGuards'][-1]['observedVersion'] = 'different'
    run('mixed-fixed-version-same-ref', c, 'FAIL', 'REF_CONSISTENCY_alias', 'F1-ref-consistency')
    for mode in [None, 'JCS_JSON', 'RAW_BYTES']:
        for fixed_value in [False, True]:
            c = add(copy.deepcopy(base), b'{"x":1}', mode=mode, fixed=fixed_value, rev='review:r1', outer='review:r1', role='AUTHORIZATION_VIEW')
            run('full-facts-'+str(mode)+'-'+str(fixed_value), c, group='F1-facts')
    c = add(copy.deepcopy(base), original, rev='review:r1', outer='review:r1')
    attack('outer-revision-conflict', c, lambda c: c['context']['requiredReads'][-1].update(revisionRef='review:r2'), code='READ_REVISION_review-input')
    attack('guard-revision-conflict', c, lambda c: c['proof']['readGuards'][-1]['binding'].update(revisionRef='review:r2'), code='READ_BINDING_review-input')
    current = base['context']['attempt']['transactionAttemptId']
    later = [('receipt', {'schemaVersion':'ofarm.notRequiredGovernedEffectReceipt.v0.1','attempt':{'transactionAttemptId':current}}),
             ('consumption', {'schemaVersion':'ofarm.notRequiredDecisionConsumption.v0.1','transactionAttemptId':current}),
             ('transaction-result', {'schemaVersion':'ofarm.notRequiredTransactionAttempt.v0.1','attempt':{'transactionAttemptId':current}}),
             ('checkpoint', {'transactionAttemptId':current,'authorizationEvaluatedAt':'2026-10-24T08:00:00Z','writeAuthorizationCheckedAt':'2026-10-24T08:00:01Z'}),
             ('gate', {'attempt':{'transactionAttemptId':current},'gateId':'DOMAIN','disposition':'PASS'})]
    for label, value in later:
        for mode in ['JCS_JSON', 'RAW_BYTES']:
            for posture in [False, True]:
                run('current-'+label+'-'+mode+'-'+str(posture), add(copy.deepcopy(base), raw(value), mode=mode, fixed=posture, role='OTHER_DOMAIN_INPUT'),
                    'FAIL', 'NO_LATER_ARTIFACT_review-input', 'F2-later', cli=posture and label=='receipt')
    for mode in ['JCS_JSON', 'RAW_BYTES']:
        older = {'schemaVersion':'ofarm.notRequiredGovernedEffectReceipt.v0.1','attempt':{'transactionAttemptId':'prior:one'}}
        run('prior-artifact-'+mode, add(copy.deepcopy(base), raw(older), mode=mode), group='F2-controls')
        unknown = {'schemaVersion':'unknown.futureReceipt','attempt':{'transactionAttemptId':current},'payload':'opaque'}
        run('unknown-shape-limit-'+mode, add(copy.deepcopy(base), raw(unknown), mode=mode, fixed=True), group='F2-declared-limit',
            note='PASS documents shape-detection limit; truthful pre-verdict availability remains storage-owner responsibility.')
    correction = load_case('assert_operation_claim-correction-prior_governed_receipt')
    def relabel(v):
        v['creationKind'] = 'LEGACY_IMMUTABLE_INGRESS'
        v.pop('creatorAttemptId')
        v['sourceDerivations'].pop('creatorAttemptId')
    attack('creation-route-relabel', correction, lambda c: creation_edit(c,relabel), code='CREATION_DERIVATION_creationKind', group='F3', cli=True)
    for field in ['creationKind','priorRecordBinding','governanceContext','recordedAnchorScopes','creatorAttemptId']:
        attack('creation-missing-'+field, correction, lambda c, f=field: creation_edit(c,lambda v:v['sourceDerivations'].pop(f)), code='SCHEMA', group='F3')
        attack('creation-wrong-pointer-'+field, correction, lambda c, f=field: creation_edit(c,lambda v:v['sourceDerivations'][f].update(pointer='/not-present')), code='CREATION_DERIVATION_'+field, group='F3')
    attack('creation-unselected-source', correction, lambda c: creation_edit(c,lambda v:v['sourceDerivations']['creationKind'].update(sourceRef='not-selected')), code='CREATION_DERIVATION_creationKind', group='F3')
    source_ref = next(ref for ref in correction['records'] if ref.startswith('fixture:prior-creation-source:'))
    def fixed_source(c):
        spec = next(s for s in c['context']['requiredReads'] if s['binding']['ref'] == source_ref)
        spec.update(availability=FIXED, fixedInputVersion='version:fixed')
        guard = next(s for s in c['proof']['readGuards'] if s['binding']['ref'] == source_ref)
        guard.pop('snapshotVersion');guard.update(availability=FIXED, fixedInputVersion='version:fixed', observedVersion='version:fixed')
        c['snapshot']['positiveRecords'] = [s for s in c['snapshot']['positiveRecords'] if s['binding']['ref'] != source_ref]
    attack('creation-source-fixed-too-late', correction, fixed_source, code='CREATION_SOURCE_COMMITTED_'+source_ref, group='F3', cli=True)
    # Use exact bytes from the already sealed authorization evidence packet.
    # This protects its inputs; it does not invoke or replace authorization checks.
    wire = json.loads((FIXTURES/'fixtures/review-repair-02/authorization-boundary-wire.json').read_bytes())
    auth_context = json.loads(base64.b64decode(wire['contextBytesBase64']))
    selectors = {s['key']:s for s in auth_context['sources']}
    auth = copy.deepcopy(base)
    for key in ['REQUEST','RESULT','TRACE','POLICY','RULE','BINDING_MANIFEST','DERIVED_VIEW','EVALUATION_SNAPSHOT','AUTHORIZATION_VIEW_EXTRACTOR','SOURCE_AUTHORITY']:
        b = base64.b64decode(wire['sourceBytesBase64'][key])
        selection = selectors[key]['binding']
        assert sha(b) == selectors[key]['bytesSha256']
        add(auth,b,mode='JCS_JSON',fixed=True,key=key,ref=selection['ref'],rev=selection.get('revisionRef'),role='AUTHORIZATION_VIEW')
    run('authorization-originals-guarded',auth,group='56-boundary',cli=True)
    attack('authorization-byte-substitution',auth,lambda c:c['records'].__setitem__(selectors['RESULT']['binding']['ref'],c['records'][selectors['RESULT']['binding']['ref']]+b' '),code='BYTES_RESULT',group='56-boundary',cli=True)
    grant_spec=next(s for s in auth['context']['requiredReads'] if s['key']=='SOURCE_AUTHORITY')
    grant_body=json.loads(auth['records'][grant_spec['binding']['ref']])
    assert grant_spec['binding']['digest'] != grant_body['sourceRecordDigest']
    def excluded_digest(c):
        for group in [c['context']['requiredReads'],c['proof']['readGuards']]:
            next(s for s in group if s['key']=='SOURCE_AUTHORITY')['binding']['digest']=grant_body['sourceRecordDigest']
    attack('authorization-owner-digest-is-not-whole-record',auth,excluded_digest,code='BYTES_SOURCE_AUTHORITY',group='56-boundary')
    # Demonstrate the declared consumer-closure limit, rather than claim this
    # storage checker verifies canonical path correctness or all source members.
    shortened=copy.deepcopy(auth)
    removed=next(s for s in shortened['context']['requiredReads'] if s['key']=='RESULT')
    shortened['context']['requiredReads'].remove(removed)
    shortened['proof']['readGuards']=[s for s in shortened['proof']['readGuards'] if s['key']!='RESULT']
    shortened['records'].pop(removed['binding']['ref'])
    run('authorization-shortened-manifest-limit',shortened,group='56-declared-limit',
        note='PASS is expected only for the selected storage manifest. #47 must independently derive and compare complete #56 inputs.')
    summary={'kind':'INDEPENDENT_CONDITIONAL_REVIEW','checks':len(ROWS),'metExpectation':sum(r['pass_'] for r in ROWS),
             'unexpected':[r for r in ROWS if not r['pass_']], 'rows':ROWS}
    (HERE/'independent-results.json').write_bytes(raw(summary))
    print(json.dumps({k:v for k,v in summary.items() if k not in ['rows','unexpected']}))
    print(json.dumps([{'id':r['id'],'expected':r['expected'],'actual':r['actual'],'codes':r['codes']} for r in summary['unexpected']]))
    return int(bool(summary['unexpected']))


def replay_cli():
    summary=json.loads((HERE/'independent-results.json').read_bytes())
    results=[]
    for row in summary['rows']:
        if not row['cliRequested']:
            continue
        folder=OUT/row['id']
        argv=[sys.executable,'-B',str(CODE/'verify_state.py'),'--package-root',str(PACKAGE),'--source-root',str(FIXTURES)]
        for flag in ['selection','context','policy','snapshot','proof','records-manifest','report']:
            filename={'selection':'selected.json','records-manifest':'records.json','report':'cli-report.json'}.get(flag,flag+'.json')
            argv.extend(['--'+flag,str(folder/filename)])
        proc=subprocess.run(argv,capture_output=True,text=True,env=os.environ.copy())
        api=json.loads((folder/'api-report.json').read_bytes())
        cli=json.loads((folder/'cli-report.json').read_bytes())
        expected_exit={PASS:0,'FAIL':1,'INPUT_ERROR':2,'DEPENDENCY_UNAVAILABLE':3}[api['status']]
        results.append({'id':row['id'],'returncode':proc.returncode,'sameReport':api==cli,'pass':api==cli and proc.returncode==expected_exit,'stdout':proc.stdout,'stderr':proc.stderr})
    result={'checks':len(results),'passed':sum(r['pass'] for r in results),'rows':results}
    (HERE/'independent-cli-results.json').write_bytes(raw(result))
    print(json.dumps({k:v for k,v in result.items() if k!='rows'}))
    return int(any(not r['pass'] for r in results))


if __name__ == '__main__':
    raise SystemExit(main())
