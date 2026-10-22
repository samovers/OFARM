"""Reconstruct the sealed occupancy snapshot and replay its exact review harness."""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess,sys

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--repo',type=Path,required=True)
parser.add_argument('--out',type=Path,required=True)
parser.add_argument('--prepare-only',action='store_true')
args=parser.parse_args();repo=args.repo.resolve();out=args.out.resolve();here=Path(__file__).resolve().parent
if out.exists():parser.error('--out must be a new directory; frozen reviews must not be overwritten')
def sha(raw):return hashlib.sha256(raw).hexdigest()
mapping=json.loads((here/'integration-map.json').read_bytes())
manifest=json.loads((here/'DELIVERY_MANIFEST.json').read_bytes())
snapshot=out/'snapshot';snapshot.mkdir(parents=True)
for row in mapping['files']:
    source=(repo/row['destination']).resolve();target=(snapshot/row['source']).resolve()
    if not source.is_relative_to(repo) or not target.is_relative_to(snapshot):raise ValueError('Mapping path escapes its root')
    data=source.read_bytes()
    if sha(data)!=row['sha256'] or len(data)!=row['bytes']:raise ValueError('Mapped bytes differ: '+row['destination'])
    target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
for name in ('DELIVERY_MANIFEST.json','integration-map.json'):shutil.copyfile(here/name,snapshot/name)
for row in manifest['files']:
    data=(snapshot/row['path']).read_bytes()
    if sha(data)!=row['sha256'] or len(data)!=row['bytes']:raise ValueError('Snapshot differs: '+row['path'])
shutil.copyfile(here/'independent_probes.py',out/'independent_probes.py')
print(json.dumps({'snapshot':str(snapshot),'sealedMembers':len(manifest['files']),'mappedFiles':len(mapping['files']),'verified':True}),flush=True)
if not args.prepare_only:raise SystemExit(subprocess.run([sys.executable,'-B',str(out/'independent_probes.py')],cwd=out).returncode)
