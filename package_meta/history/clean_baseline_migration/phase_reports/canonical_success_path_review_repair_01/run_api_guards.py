"""API-only inputs that cannot be represented by the closed wire transport."""
from pathlib import Path
import json,base64
from build_fixtures import raw,encode
from test_support import fresh
from path_common import sha
from verify_success_path import verify
H=Path(__file__).resolve().parent;rows=[]
for argument in [3,4]:
 m=fresh();w=encode(m);dec=lambda x:base64.b64decode(x);args=[dec(w['evidenceBytesBase64']),dec(w['profileBytesBase64']),dec(w['contextBytesBase64']),{k:dec(v) for k,v in w['sourceBytesBase64'].items()},{k:dec(v) for k,v in w['schemaBytesBase64'].items()}];pin=sha(args[2]);args[argument]=[]
 r=verify(*args,expected_context_sha256=pin);codes=[x['code'] for x in r['errors']];name='nondictionary-argument-'+str(argument);row={'id':name,'expected':'FAIL','expectedCodes':['SOURCE_MAP_REQUIRED'],'apiOverrides':{str(argument):[]},'actual':r['disposition'],'codes':codes,'matched':r['disposition']=='FAIL' and codes==['SOURCE_MAP_REQUIRED']};rows.append(row)
 d=H/'api-only-checks'/name;d.mkdir(parents=True,exist_ok=True);(d/'wire.json').write_bytes(raw(w));(d/'context.sha256').write_text(pin+'\n');(d/'api-report.json').write_bytes(raw(r))
result={'cases':len(rows),'matched':sum(x['matched'] for x in rows),'results':rows,'scope':'API_ONLY_INVALID_TRANSPORT_ARGUMENTS'};(H/'api-only-results.json').write_bytes(raw(result));print(result);raise SystemExit(result['matched']!=result['cases'])
