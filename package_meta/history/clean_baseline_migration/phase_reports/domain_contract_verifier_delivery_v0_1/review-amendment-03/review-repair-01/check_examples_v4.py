"""Run all current inherited checks over a pinned v4 overlay, then focused v4 checks.
All temporary writes and reports stay in this checker directory by default.
"""
import argparse,hashlib,json,os,shutil,subprocess,sys,tempfile
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--prior-packet',type=Path);p.add_argument('--repo-root',type=Path,required=True);p.add_argument('--frozen-root',type=Path);p.add_argument('--dependency-dir',type=Path);p.add_argument('--output',type=Path);a=p.parse_args();O=Path(__file__).resolve().parent
prior=(a.prior_packet or O.parent/'review-amendment-02').resolve();pins=json.loads((O/'source-pins-v4.json').read_text());sha=lambda raw:hashlib.sha256(raw).hexdigest()
for pin in pins['priorPacketFiles']:
 if sha((prior/pin['path']).read_bytes())!=pin['sha256']:raise ValueError('Prior packet changed: '+pin['path'])
for pin in pins['canonicalSources']:
 if sha((a.repo_root/pin['path']).read_bytes())!=pin['sha256']:raise ValueError('Canonical source changed: '+pin['path'])
if a.dependency_dir:sys.path.insert(0,str(a.dependency_dir.resolve()))
sys.path.insert(0,str(O));from focused_checks_v4 import run_focused
from fix01_checks import run_fix01
aliases={
 'candidate-examples-v4.json':'candidate-examples-v3.json',
 'projection-contract-v4.json':'projection-contract-v3.json',
 'criterion-expectations-v4.json':'criterion-expectations-v3.json',
 'measurement-fixtures-v4.json':'measurement-fixtures-v3.json',
 'measurement-hostiles-v4.json':'measurement-hostiles-v3.json',
 'measurement-role-contract-v4.json':'measurement-role-contract-v3.json',
 'evidence-selectors-v4.json':'evidence-selectors-v3.json',
 'source-transform-map-v4.json':'source-transform-map-v3.json'}
with tempfile.TemporaryDirectory(prefix='.v4-check-',dir=O) as temp:
 t=Path(temp)
 for f in prior.iterdir():
  if f.is_file():shutil.copyfile(f,t/f.name)
 shutil.copytree(prior/'commit-class-sources',t/'commit-class-sources')
 for source,target in aliases.items():shutil.copyfile(O/source,t/target)
 for name in ['measurement_checks_v4.py','role_checks_v4.py','provenance_checks_v4.py','w05_profile_checks_fix01.py','w05-owner-profile-fix01.json']:shutil.copyfile(O/name,t/name)
 cmd=[sys.executable,str(O/'inherited_checks_v4.py'),str(t),'--previous-amendment',str(prior.parent/'review-amendment'),'--packet',str(prior.parent),'--repo-root',str(a.repo_root.resolve()),'--output',str(t/'current-results.json')]
 if a.frozen_root:cmd+=['--frozen-root',str(a.frozen_root.resolve())]
 if a.dependency_dir:cmd+=['--dependency-dir',str(a.dependency_dir.resolve())]
 run=subprocess.run(cmd,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
 if not (t/'current-results.json').exists():raise RuntimeError(run.stdout+'\n'+run.stderr)
 inherited=json.loads((t/'current-results.json').read_text())
 focused=run_focused(O,prior,a.repo_root)
 repair=run_fix01(O)
 results=inherited['results']+focused+repair
 report={'status':'V4_FIX01_DESIGN_CHECKS_PASS' if all(x['passed'] for x in results) else 'V4_FIX01_DESIGN_CHECKS_FAIL','checks':len(results),'passed':sum(x['passed'] for x in results),'failed':sum(not x['passed'] for x in results),'inheritedCurrentRun':{'checks':inherited['checks'],'passed':inherited['passed'],'failed':inherited['failed'],'sourceHead':pins['sourceHead'],'transformFile':'checker-transforms-v4.json','overlayAliases':aliases},'focusedCurrentRun':{'checks':len(focused),'passed':sum(x['passed'] for x in focused)},'fix01CurrentRun':{'checks':len(repair),'passed':sum(x['passed'] for x in repair)},'results':results,'limits':['Every inherited check was rerun with current v4 inputs. No historical result count is reused.','Finite fictional checks only; no complete verifier, owner admission, source adoption, producer, CI or independent approval.'],'next':'Integrate the sealed v4 packet and obtain fresh exact-head review.'}
 if a.output:a.output.write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:report[k] for k in ['status','checks','passed','failed']}))
 for x in results:
  if not x['passed']:print(json.dumps(x))
 if run.returncode:print(run.stderr)
 raise SystemExit(bool(report['failed']))
