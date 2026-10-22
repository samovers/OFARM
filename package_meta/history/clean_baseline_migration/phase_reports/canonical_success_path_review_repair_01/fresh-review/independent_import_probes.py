"""Independent process-isolated import checks of the frozen authorization API."""
from pathlib import Path
import argparse, base64, hashlib, json, shutil, subprocess, sys

ap=argparse.ArgumentParser();ap.add_argument('--snapshot',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
P=a.snapshot.resolve();O=a.out.resolve();O.mkdir(parents=True,exist_ok=True)
DRIVER=r'''
import base64,hashlib,importlib.util,json,sys,types
from pathlib import Path
code,package,mode=Path(sys.argv[1]),Path(sys.argv[2]),sys.argv[3]
if mode=='cached':sys.modules['path_common']=types.ModuleType('path_common')
if mode=='shadow':sys.path.insert(0,str(code/'shadow'))
spec=importlib.util.spec_from_file_location('isolated_review',code/'verify_success_path.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
if mode=='changed-loaded-helper':(code/'path_common.py').write_bytes((package/'path_common.py').read_bytes())
if mode=='changed-export':v.equal=lambda a,b:True
if mode=='changed-code':
 def false_equality(a,b):return True
 v._COMMON.equal.__code__=false_equality.__code__
if mode=='changed-file-after-load':(code/'path_common.py').write_bytes((code/'path_common.py').read_bytes()+b'\n# independent disk change\n')
w=json.loads((package/'fixtures/basis-3-party/wire.json').read_bytes());dec=lambda x:base64.b64decode(x,validate=True)
xs=[dec(w['evidenceBytesBase64']),dec(w['profileBytesBase64']),dec(w['contextBytesBase64']),{k:dec(x) for k,x in w['sourceBytesBase64'].items()},{k:dec(x) for k,x in w['schemaBytesBase64'].items()}]
r=v.verify(*xs,expected_context_sha256=hashlib.sha256(xs[2]).hexdigest(),contract_root=package)
print(json.dumps({'disposition':r['disposition'],'codes':[e['code'] for e in r['errors']]}))
'''
(O/'isolated_driver.py').write_text(DRIVER)
rows=[]
for mode,expected in [('baseline',[]),('cached',[]),('shadow',[]),('changed-loaded-helper',['EXECUTED_HELPER_BYTES_MISMATCH']),('changed-export',['HELPER_EXPORT_IDENTITY_MISMATCH']),('changed-code',['HELPER_EXPORT_IDENTITY_MISMATCH']),('changed-file-after-load',['VERIFICATION_CODE_BYTES_MISMATCH'])]:
    d=O/mode;d.mkdir(exist_ok=True)
    for f in ('verify_success_path.py','path_common.py'):shutil.copyfile(P/f,d/f)
    if mode=='shadow':
        (d/'shadow').mkdir(exist_ok=True);(d/'shadow/path_common.py').write_text('raise RuntimeError("untrusted shadow helper executed")\n')
    if mode=='changed-loaded-helper':(d/'path_common.py').write_bytes((d/'path_common.py').read_bytes()+b'\n# independent changed load bytes\n')
    proc=subprocess.run([sys.executable,'-B',str(O/'isolated_driver.py'),str(d),str(P),mode],capture_output=True,text=True,timeout=45)
    try:result=json.loads(proc.stdout)
    except ValueError:result={'disposition':'PROCESS_FAILURE','codes':[]}
    ok=proc.returncode==0 and result['codes']==expected and (result['disposition']=='PASS' if not expected else result['disposition']!='PASS')
    rows.append({'name':mode,'pass':ok,'expectedCodes':expected,'result':result,'exitCode':proc.returncode,'stderr':proc.stderr})
out={'status':'PASS' if all(r['pass'] for r in rows) else 'FINDINGS','checks':len(rows),'passed':sum(r['pass'] for r in rows),'results':rows,'limit':'Trusted verifier execution is assumed; these checks do not attest a hostile Python process or protect arbitrary code replacement.'}
(O/'independent-import-review.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));raise SystemExit(out['status']!='PASS')
