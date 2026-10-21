"""Construction only. Seal once after all final checks; never run on a sealed packet."""
from pathlib import Path
import json,hashlib,shutil
H=Path(__file__).resolve().parent
if (H/'DELIVERY_MANIFEST.json').exists():raise SystemExit('Already sealed; create a sibling repair instead.')
def raw(x):return (json.dumps(x,indent=2,ensure_ascii=False)+'\n').encode()
def sha(b):return hashlib.sha256(b).hexdigest()
full=json.loads((H/'conformance-results.json').read_text());edge=json.loads((H/'edge-results.json').read_text());installed=json.loads((H/'installed-runner-results.json').read_text())
assert full['failed']==edge['failed']==0 and installed['matched']==installed['cases']
for d in (H/'fixtures').glob('basis-*'):
 report=H/'checks'/(d.name+'-baseline')/'api-report.json';assert json.loads(report.read_text())['disposition']=='PASS';(d/'api-report.json').write_bytes(report.read_bytes())
# Test installation copies are reproducible from the map. Keep their reports,
# not another mutable copy of the candidate inside the sealed packet.
layout=H/'edge-checks/installed-layout'
if layout.exists():shutil.rmtree(layout)
cases=[]
for x in full['results']:cases.append({'id':x['id'],'wire':'cases/'+x['id']+'/wire.json','contextPin':'cases/'+x['id']+'/context.sha256','expected':x['expected']})
for x in edge['results']:
 if x['id'] in ['changed-installed-source-law','missing-installed-source-root'] or not (H/'edge-checks'/x['id']/'wire.json').exists():continue
 cases.append({'id':x['id'],'wire':'edge-cases/'+x['id']+'/wire.json','contextPin':'edge-cases/'+x['id']+'/context.sha256','expected':x['expected']})
(H/'cases.json').write_bytes(raw({'scope':'FICTIONAL_SELECTED_OUTPUT_INTEGRITY_ONLY','cases':cases,'environmentChecks':'See edge-results.json for independent installed package/source-root mutation checks.'}))
pkg='03_machine_contracts/drafts_non_default/authorization_decision_evidence/canonical_success_path/'
runner='04_implementation_and_conformance/conformance_runners/canonical_success_path/'
fixture='04_implementation_and_conformance/examples_and_fixtures/fixtures/canonical_success_path/'
evidence='package_meta/history/clean_baseline_migration/phase_reports/canonical_success_path_delivery_v0_1/'
def target(name):
 if name in ['verify_success_path.py','path_common.py','run_cases.py']:return runner+name
 if name.startswith('sources/'):return fixture+name
 if name.startswith('schemas/') or name in ['contract.json','source-pins.json','README.md','DESIGN.md','SOURCE_INTERFACE.md','REGISTRATION.md']:return pkg+name
 if name.startswith('checks/'):return fixture+'cases/'+name[len('checks/'):]
 if name.startswith('edge-checks/'):return fixture+'edge-cases/'+name[len('edge-checks/'):]
 if name.startswith('fixtures/'):return fixture+'examples/'+name[len('fixtures/'):]
 if name=='cases.json':return fixture+name
 return evidence+name
mapping=[]
for f in sorted(H.rglob('*')):
 if not f.is_file() or f.name in ['DELIVERY_MANIFEST.json','integration-map.json']:continue
 name=str(f.relative_to(H));b=f.read_bytes();mapping.append({'source':name,'destination':target(name),'sha256':sha(b),'bytes':len(b)})
assert len({x['destination'] for x in mapping})==len(mapping)
mapvalue={'status':'EXACT_PROPOSED_INTEGRATION_MAP','primaryTrustBoundary':'Canonical authorization decision evidence','scopeStayedInsideBoundary':True,'packageRoot':pkg.rstrip('/'),'checkerRoot':runner.rstrip('/'),'sourceRoot':fixture.rstrip('/'),'selfDestination':evidence+'integration-map.json','manifestDestination':evidence+'DELIVERY_MANIFEST.json','mappings':mapping,'next':'Root independently reviews, integrates and publishes a separate draft; no default CI activation.'}
(H/'integration-map.json').write_bytes(raw(mapvalue))
files=[]
for f in sorted(H.rglob('*')):
 if f.is_file() and f.name!='DELIVERY_MANIFEST.json':
  b=f.read_bytes();files.append({'path':str(f.relative_to(H)),'sha256':sha(b),'bytes':len(b)})
manifest={'status':'SEALED_FOR_INDEPENDENT_REVIEW','primaryTrustBoundary':'Canonical authorization decision evidence','scopeStayedInsideBoundary':True,'contractRawSha256':sha((H/'contract.json').read_bytes()),'integrationMapSha256':sha((H/'integration-map.json').read_bytes()),'checks':{'fullCases':full['cases'],'edgeAndInstalledChecks':edge['cases'],'installedRunnerCases':installed['cases'],'allMatched':True},'files':files,'next':'Independent review before integration or publication; keep repairs in a sibling directory.'}
f=H/'DELIVERY_MANIFEST.json';f.write_bytes(raw(manifest));print(json.dumps({'sealSha256':sha(f.read_bytes()),'contractSha256':manifest['contractRawSha256'],'integrationMapSha256':manifest['integrationMapSha256'],'sealedFiles':len(files),'mappedFiles':len(mapping),'portableCases':len(cases),'checks':manifest['checks']},indent=2))
