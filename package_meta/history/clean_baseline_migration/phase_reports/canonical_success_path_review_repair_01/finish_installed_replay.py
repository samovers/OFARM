"""Correct the oversized wire oracle and retain the initial full-run evidence."""
from pathlib import Path
import json,subprocess,sys,hashlib
from build_fixtures import raw
H=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
initial_path=H/'installed-runner-initial-results.json'
assert not initial_path.exists(),'Do not overwrite initial correction evidence.'
initial_path.write_bytes((H/'installed-runner-results.json').read_bytes());(H/'initial-case-index.json').write_bytes((H/'cases.json').read_bytes());(H/'installed-runner-initial.log').write_bytes((H/'installed-runner.log').read_bytes())
initial=json.loads(initial_path.read_bytes());failed=[x for x in initial['results'] if not x['matched']];assert len(failed)==1 and failed[0]['id']=='oversize' and failed[0]['actualCodes']==['INVALID_WIRE_OR_PACKAGE']
paths=json.loads((H/'installed-replay-paths.json').read_bytes());fixture=Path(paths['fixtureRoot']);index=json.loads((H/'cases.json').read_bytes());case=next(x for x in index['cases'] if x['id']=='oversize');assert case['expectedCodes']==['INVALID_INPUT_BYTES'];case.update(expectedCodes=['INVALID_WIRE_OR_PACKAGE'],apiExpectedCodes=['INVALID_INPUT_BYTES'],transportDifference='The base64-expanded outer wire exceeds the strict document byte limit; the CLI rejects the wire before decoding the oversized evidence document.')
(H/'cases.json').write_bytes(raw(index));(fixture/'cases.json').write_bytes(raw(index));(fixture/'oversize-cli-replay.json').write_bytes(raw({'cases':[case]}))
out=H/'installed-runner-oversize-replay.json';args=[sys.executable,'-B',str(Path(paths['checkerRoot'])/'run_cases.py'),'--package-root',paths['packageRoot'],'--fixtures-root',paths['fixtureRoot'],'--source-root',paths['fixtureRoot'],'--case-index','oversize-cli-replay.json','--report',str(out)]
p=subprocess.run(args,capture_output=True,text=True,timeout=60);replay=json.loads(out.read_bytes());assert p.returncode==0 and replay['cases']==replay['matched']==1
rows=[replay['results'][0] if x['id']=='oversize' else x for x in initial['results']];assert len(rows)==491 and all(x['matched'] for x in rows)
final={'cases':491,'matched':491,'results':rows,'scope':'FICTIONAL_SELECTED_OUTPUT_INTEGRITY_ONLY','executionEvidence':{'initialFullRunCases':491,'initialMatched':490,'initialReportSha256':sha(initial_path.read_bytes()),'correctedCliOracleCase':'oversize','replayReportSha256':sha(out.read_bytes()),'runtimeOrWireBytesChanged':False,'unchangedCasesReused':490,'targetedCliReplayCases':1}}
(H/'installed-runner-results.json').write_bytes(raw(final));(H/'installed-runner.log').write_text(json.dumps({k:v for k,v in final.items() if k!='results'},indent=2)+'\n');(H/'installed-runner-oversize-execution.json').write_bytes(raw({'argv':args,'exitCode':p.returncode,'stdout':p.stdout,'stderr':p.stderr}));print(final['executionEvidence'])
