"""Prepare the declared split layout and exact-code portable case index."""
from pathlib import Path
import json,shutil
from build_fixtures import raw
H=Path(__file__).resolve().parent;cases=[]
layout=H/'edge-checks/installed-layout';pkg=layout/'03_machine_contracts/drafts_non_default/authorization_decision_evidence/canonical_success_path';runner=layout/'04_implementation_and_conformance/conformance_runners/canonical_success_path';fixture=layout/'04_implementation_and_conformance/examples_and_fixtures/fixtures/canonical_success_path'
for folder in [pkg,runner,fixture]:folder.mkdir(parents=True,exist_ok=True)
contract=json.loads((H/'contract.json').read_bytes())
for name in ['contract.json',*contract['files']]:
 target=(fixture if name.startswith('sources/') else pkg)/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes((H/name).read_bytes())
for name in ['verify_success_path.py','path_common.py','run_cases.py']:(runner/name).write_bytes((H/name).read_bytes())
for report,folder,prefix in [('conformance-results.json','checks','cases'),('targeted-results.json','targeted-checks','targeted-cases'),('edge-results.json','edge-checks','edge-cases')]:
 data=json.loads((H/report).read_bytes());assert data['matched']==data['cases']
 for row in data['results']:
  if row['id'] in ['changed-installed-source-law','missing-installed-source-root'] or 'expectedCodes' not in row:continue
  src=H/folder/row['id']
  if not (src/'wire.json').exists():continue
  out=fixture/prefix/row['id'];out.mkdir(parents=True,exist_ok=True)
  for n in ['wire.json','context.sha256']:(out/n).write_bytes((src/n).read_bytes())
  case={'id':row['id'],'wire':prefix+'/'+row['id']+'/wire.json','contextPin':prefix+'/'+row['id']+'/context.sha256','expected':row['expected'],'expectedCodes':row['expectedCodes']}
  if row.get('expectedDetailContains'):case['expectedDetailContains']=row['expectedDetailContains']
  if row['id']=='oversize':case.update(expectedCodes=['INVALID_WIRE_OR_PACKAGE'],apiExpectedCodes=['INVALID_INPUT_BYTES'],transportDifference='The base64-expanded outer wire exceeds the strict document byte limit; the CLI rejects the wire before decoding the oversized evidence document.')
  cases.append(case)
assert len({x['id'] for x in cases})==len(cases)
index={'scope':'FICTIONAL_SELECTED_OUTPUT_INTEGRITY_ONLY','cases':cases,'excludedEnvironmentChecks':'Two API-only invalid map argument checks, seven helper-origin probes, two source-root/package mutation checks, and the AST fault-injection audit are reported separately.'}
(H/'cases.json').write_bytes(raw(index));(fixture/'cases.json').write_bytes(raw(index))
(H/'installed-replay-paths.json').write_bytes(raw({'packageRoot':str(pkg),'checkerRoot':str(runner),'fixtureRoot':str(fixture),'cases':len(cases)}));print('Prepared',len(cases),'specific-code portable cases.')
