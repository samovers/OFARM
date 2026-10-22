import sys,types,importlib.util,json,base64
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
