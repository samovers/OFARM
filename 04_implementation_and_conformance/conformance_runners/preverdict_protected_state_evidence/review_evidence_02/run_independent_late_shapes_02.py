"""Fresh R1 probes: non-string labels must not hide recognized later shapes."""
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--repository-root',type=Path,required=True)
parser.add_argument('--output-dir',type=Path,required=True)
args=parser.parse_args()
HERE=args.output_dir.resolve()
helper=args.repository_root.resolve()/'04_implementation_and_conformance/conformance_runners/preverdict_protected_state_evidence/run_independent_review_02.py'
expected='15e2bccb691d79958a8f70821b31584c77788d5c8f75b20db904f05c8f51a393'
if hashlib.sha256(helper.read_bytes()).hexdigest()!=expected:
    raise SystemExit('The separately reviewed independent generator pin does not match.')
# Import only the independently authored helper, not the authored test suites.
original_argv=sys.argv
try:
    sys.argv=[str(helper),'--output-dir',str(HERE)]
    spec=importlib.util.spec_from_file_location('pinned_independent_review',helper)
    p=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(p)
finally:
    sys.argv=original_argv
p.OUT=HERE/'late-shape-cases'
base=p.load_case('assert_operation_claim-initial')
attempt=base['context']['attempt']['transactionAttemptId']
shapes={
    'checkpoint':{'checkpoint':{}},
    'gateTraces':{'gateTraces':[]},
    'receiptDigest':{'governedEffectReceiptDigest':'sha256:'+'0'*64},
    'consumptionDigest':{'decisionConsumptionDigest':'sha256:'+'0'*64},
    'checkpointTimes':{'authorizationEvaluatedAt':'2026-10-24T08:00:00Z','writeAuthorizationCheckedAt':'2026-10-24T08:00:01Z'},
    'gate':{'gateId':'DOMAIN','disposition':'PASS'},
    'nestedAttemptGate':{'gateId':'DOMAIN','disposition':'PASS','attempt':{'transactionAttemptId':attempt}},
}
versions={'object':{'sourceSpecific':1},'array':['source',1],'null':None,'unknownString':'source.unknown.v9'}
for shape,fields in shapes.items():
    for label,version in versions.items():
        for mode in ['JCS_JSON','RAW_BYTES']:
            for fixed in [False,True]:
                value={'schemaVersion':version,**fields}
                if shape!='nestedAttemptGate':value['transactionAttemptId']=attempt
                case=p.add(copy.deepcopy(base),p.raw(value),mode=mode,fixed=fixed,role='OTHER_DOMAIN_INPUT')
                p.run('reject-'+shape+'-'+label+'-'+mode+'-'+str(fixed),case,'FAIL','NO_LATER_ARTIFACT_review-input',
                      'recognized-shape-with-unusual-label',cli=shape in ['checkpoint','nestedAttemptGate'] and label=='object' and fixed)
for label,version in versions.items():
    for mode in ['JCS_JSON','RAW_BYTES']:
        for fixed in [False,True]:
            value={'schemaVersion':version,'transactionAttemptId':attempt,'measurement':12.5}
            p.run('ordinary-current-'+label+'-'+mode+'-'+str(fixed),p.add(copy.deepcopy(base),p.raw(value),mode=mode,fixed=fixed),
                  group='current-attempt-is-not-alone-later',cli=label=='object' and fixed)
            value={'schemaVersion':version,'transactionAttemptId':'prior:one','gateId':'DOMAIN','disposition':'PASS'}
            p.run('prior-gate-'+label+'-'+mode+'-'+str(fixed),p.add(copy.deepcopy(base),p.raw(value),mode=mode,fixed=fixed),
                  group='prior-attempt-controls')
result={'checks':len(p.ROWS),'passed':sum(x['pass_'] for x in p.ROWS),'failed':sum(not x['pass_'] for x in p.ROWS),'rows':p.ROWS}
(HERE/'late-shape-results.json').write_bytes(p.raw(result))
print(json.dumps({k:v for k,v in result.items() if k!='rows'}))
raise SystemExit(int(result['failed']>0))
