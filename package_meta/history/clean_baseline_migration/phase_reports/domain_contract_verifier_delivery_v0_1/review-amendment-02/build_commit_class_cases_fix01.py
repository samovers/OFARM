"""Construct finite independent-token controls; never writes preserved sources."""
import argparse,copy,hashlib,json,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--dependency-dir',type=Path,required=True);a=p.parse_args();sys.path.insert(0,str(a.dependency_dir.resolve()));import rfc8785
O=Path(__file__).resolve().parent;sys.path.insert(0,str(O));from event_checks_v3 import event_errors

def read(n):return json.loads((O/n).read_text())
def dg(x):return 'sha256:'+hashlib.sha256(rfc8785.dumps(x)).hexdigest()
events=read('event-cases-v3.json');package=read('event-compatibility-package-v3.json');base=events['positiveCases'][0];cases=[]
for id,token,expect in [
 ('CC01_SELF_CONSISTENT_SUBTYPE_AS_COMMIT_CLASS','OPERATION_CLAIM_ASSERTION',['PACKAGE_COMMIT_CLASS_NOT_IN_INGRESS_ENUM','PACKAGE_COMMIT_CLASS_NOT_CANONICAL','TRACE_COMMIT_CLASS_NOT_IN_INGRESS_ENUM','TRACE_COMMIT_CLASS_NOT_CANONICAL','PROOF_COMMIT_CLASS_NOT_IN_INGRESS_ENUM','PROOF_COMMIT_CLASS_NOT_CANONICAL']),
 ('CC02_SELF_CONSISTENT_WRONG_VALID_ENUM_CLASS','STRUCTURE_ASSERTION',['PACKAGE_COMMIT_CLASS_NOT_CANONICAL','TRACE_COMMIT_CLASS_NOT_CANONICAL','PROOF_COMMIT_CLASS_NOT_CANONICAL'])]:
 c=copy.deepcopy(base);pkg=copy.deepcopy(package);pkg['cases'][c['exampleId']]['commitClass']=token;c['proof']['commitClass']=token;c['traceIllustration']['commitClass']=token;c['traceIllustration']['ingressProofDigest']=dg(c['proof'])
 cases.append({'id':id,'case':c,'package':pkg,'packageDigest':dg(pkg),'expectedErrors':expect,'reason':'Package, proof and trace agree with each other; independent canonical source enum/action mapping must still reject.'})
c=copy.deepcopy(base);c['result']['assertionType']='OPERATION_CLAIM';c['proposedResultDigest']=dg(c['result'])
cases.append({'id':'CC03_COMMIT_CLASS_AS_RESULT_SUBTYPE','case':c,'package':copy.deepcopy(package),'packageDigest':dg(package),'expectedErrors':['RESULT_SUBTYPE_MISMATCH'],'reason':'The result subtype must stay OPERATION_CLAIM_ASSERTION; no global token replacement.'})
for x in cases:
 actual=event_errors(x['case'],x['package'])
 if actual!=x['expectedErrors']:raise ValueError((x['id'],actual,x['expectedErrors']))
(O/'commit-class-cases-fix01.json').write_text(json.dumps({'status':'FINITE_CANONICAL_TOKEN_CONTROLS_NOT_ADMISSION','cases':cases},indent=2)+'\n')
print('Built 3 independent canonical-token negatives with recomputed package/proof/result digests.')
