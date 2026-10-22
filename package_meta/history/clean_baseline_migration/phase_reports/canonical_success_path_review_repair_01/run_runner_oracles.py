"""Prove the installed runner fails a wrong code or missing-field-detail oracle."""
from pathlib import Path
import json,subprocess,sys,copy
from build_fixtures import raw
H=Path(__file__).resolve().parent;paths=json.loads((H/'installed-replay-paths.json').read_bytes());fixture=Path(paths['fixtureRoot']);index=json.loads((H/'cases.json').read_bytes());rows=[]
for label,case_id,field,value in [('wrong-code','basis-1-party-coherent-mirrored-party','expectedCodes',['SCHEMA_INVALID']),('wrong-detail','missing-output-primaryReasonCode','expectedDetailContains','not-a-missing-field')]:
 case=copy.deepcopy(next(x for x in index['cases'] if x['id']==case_id));case[field]=value;filename='oracle-'+label+'.json';(fixture/filename).write_bytes(raw({'cases':[case]}));out=H/('runner-oracle-'+label+'.json')
 args=[sys.executable,'-B',str(Path(paths['checkerRoot'])/'run_cases.py'),'--package-root',paths['packageRoot'],'--fixtures-root',paths['fixtureRoot'],'--source-root',paths['fixtureRoot'],'--case-index',filename,'--report',str(out)]
 p=subprocess.run(args,capture_output=True,text=True,timeout=60);r=json.loads(out.read_bytes());rows.append({'id':label,'matched':p.returncode==1 and r['cases']==1 and r['matched']==0,'argv':args,'exitCode':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'report':r})
result={'cases':len(rows),'matched':sum(x['matched'] for x in rows),'results':rows};(H/'runner-oracle-results.json').write_bytes(raw(result));print({k:v for k,v in result.items() if k!='results'});raise SystemExit(result['matched']!=result['cases'])
