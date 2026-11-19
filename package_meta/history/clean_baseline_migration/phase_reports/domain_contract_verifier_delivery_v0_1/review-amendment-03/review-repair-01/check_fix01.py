"""Validate exact reviewed bytes plus the explicitly listed fix01 replacements."""
import argparse,hashlib,json,os,shutil,subprocess,sys,tempfile
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--base-packet',type=Path,required=True);p.add_argument('--repo-root',type=Path,required=True);p.add_argument('--dependency-dir',type=Path);p.add_argument('--frozen-root',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();O=Path(__file__).resolve().parent
pins=json.loads((O/'source-pins-fix01.json').read_text());changes=json.loads((O/'correction-files-fix01.json').read_text());sha=lambda b:hashlib.sha256(b).hexdigest()
for pin in pins['files']:
    if sha((a.base_packet/pin['path']).read_bytes())!=pin['sha256']:raise ValueError('Reviewed source bytes changed: '+pin['path'])
with tempfile.TemporaryDirectory(prefix='.fix01-check-',dir=O) as temp:
    parent=Path(temp);current=parent/'review-amendment-03';shutil.copytree(a.base_packet,current)
    (parent/'review-amendment-02').symlink_to((a.base_packet.parent/'review-amendment-02').resolve(),target_is_directory=True)
    for name in changes['files']:shutil.copyfile(O/name,current/name)
    result=parent/'current-results.json';cmd=[sys.executable,str(current/'check_examples_v4.py'),'--repo-root',str(a.repo_root.resolve()),'--output',str(result)]
    if a.dependency_dir:cmd+=['--dependency-dir',str(a.dependency_dir.resolve())]
    if a.frozen_root:cmd+=['--frozen-root',str(a.frozen_root.resolve())]
    run=subprocess.run(cmd,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
    if not result.exists():raise RuntimeError(run.stdout+'\n'+run.stderr)
    report=json.loads(result.read_text());report['repairSourceHead']=pins['sourceHead'];report['repairMode']='Full frozen source run' if a.frozen_root else 'Portable default sibling layout; no --prior-packet override';report['sourcePacketFilesVerified']=len(pins['files']);report['correctionFiles']=[{'path':name,'sha256':sha((O/name).read_bytes())} for name in changes['files']];report['processExitCode']=run.returncode;report['next']='Integrate declared corrections and obtain fresh exact-head review; historical reports remain unchanged.'
    a.output.write_text(json.dumps(report,indent=2)+'\n');print(run.stdout,end='');print(run.stderr,end='');raise SystemExit(run.returncode or bool(report['failed']))
