"""Fresh-process helper-origin regressions; no runtime-attestation claim."""
from pathlib import Path
import json,subprocess,sys,shutil
from build_fixtures import raw
H=Path(__file__).resolve().parent;OUT=H/'helper-probes';OUT.mkdir(exist_ok=True)
COMMON='''import sys,types,importlib.util,json,base64
from pathlib import Path
root=Path(sys.argv[1]); mode=sys.argv[2]; work=Path(sys.argv[3]); original=Path(sys.argv[4]); wire=Path(sys.argv[5])
if mode=='poisoned-sysmodules':
 fake=types.ModuleType('path_common');fake.equal=lambda *a:True;sys.modules['path_common']=fake
if mode=='shadow-syspath':sys.path.insert(0,str(work/'shadow'))
spec=importlib.util.spec_from_file_location('isolated_verified_path',root/'verify_success_path.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
if mode=='restore-helper-after-load':(root/'path_common.py').write_bytes((original/'path_common.py').read_bytes())
if mode=='swap-export':v.equal=lambda *a:True
if mode=='swap-helper-code':
 def always(*a):return True
 v._COMMON.equal.__code__=always.__code__
w=json.loads(wire.read_bytes());dec=lambda x:base64.b64decode(x)
context=dec(w['contextBytesBase64']);pin=(wire.parent/'context.sha256').read_text().strip()
r=v.verify(dec(w['evidenceBytesBase64']),dec(w['profileBytesBase64']),context,{k:dec(x) for k,x in w['sourceBytesBase64'].items()},{k:dec(x) for k,x in w['schemaBytesBase64'].items()},expected_context_sha256=pin,contract_root=original,source_root=original)
print(json.dumps(r))
'''
script=OUT/'isolated_probe.py';script.write_text(COMMON);rows=[]
for mode,code in [('baseline',None),('poisoned-sysmodules','ACCOUNTABLE_PARTY_MISMATCH'),('shadow-syspath','ACCOUNTABLE_PARTY_MISMATCH'),('restore-helper-after-load','EXECUTED_HELPER_BYTES_MISMATCH'),('swap-export','HELPER_EXPORT_IDENTITY_MISMATCH'),('swap-helper-code','HELPER_EXPORT_IDENTITY_MISMATCH'),('changed-adjacent-checker','VERIFICATION_CODE_BYTES_MISMATCH')]:
 d=OUT/mode;d.mkdir(exist_ok=True);root=d/'code';root.mkdir(exist_ok=True)
 for name in ['verify_success_path.py','path_common.py']:(root/name).write_bytes((H/name).read_bytes())
 if mode=='restore-helper-after-load':
  p=root/'path_common.py';s=p.read_text();assert 'return canonical(a)==canonical(b)' in s;p.write_text(s.replace('return canonical(a)==canonical(b)','return True'))
 if mode=='changed-adjacent-checker':
  p=root/'verify_success_path.py';p.write_bytes(p.read_bytes()+b'\n# Different installed verifier bytes.\n')
 if mode=='shadow-syspath':
  shadow=d/'shadow';shadow.mkdir(exist_ok=True);(shadow/'path_common.py').write_text('raise RuntimeError("SHADOW_HELPER_WAS_EXECUTED")\n')
 wire=H/'checks'/('basis-1-party-coherent-mirrored-party' if mode in ['poisoned-sysmodules','shadow-syspath'] else 'basis-1-party-baseline')/'wire.json'
 args=[sys.executable,'-B',str(script),str(root),mode,str(d),str(H),str(wire)]
 c=subprocess.run(args,capture_output=True,text=True,timeout=60)
 try:r=json.loads(c.stdout)
 except Exception:r={'disposition':'NO_REPORT','errors':[]}
 expected=[] if code is None else [code];actual=[x['code'] for x in r['errors']]
 ok=c.returncode==0 and actual==expected and (r['disposition']=='PASS' if code is None else r['disposition'] in ['FAIL','INPUT_ERROR'])
 row={'id':mode,'matched':ok,'expectedCodes':expected,'actualCodes':actual,'report':r,'exitCode':c.returncode,'stderr':c.stderr};rows.append(row);(d/'execution.json').write_bytes(raw({'argv':args,**row}));print(mode,ok,actual,flush=True)
 # Preserve the exact intentionally altered test copies and reports as evidence.
result={'scope':'AUTHOR_SIDE_HELPER_ORIGIN_AND_IDENTITY_PROBES','cases':len(rows),'matched':sum(x['matched'] for x in rows),'results':rows,'next':'Review both code-origin evidence and explicit limits; no hostile-process runtime attestation is established.'};(H/'helper-integrity-results.json').write_bytes(raw(result));raise SystemExit(result['matched']!=result['cases'])
