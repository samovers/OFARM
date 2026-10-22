"""Reconstruct the sealed authorization candidate and rerun its fresh review."""
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
for row in mapping['mappings']:
 source=(repo/row['destination']).resolve();target=(snapshot/row['source']).resolve()
 if not source.is_relative_to(repo) or not target.is_relative_to(snapshot):raise ValueError('Mapping path escapes its root')
 data=source.read_bytes()
 if sha(data)!=row['sha256'] or len(data)!=row['bytes']:raise ValueError('Mapped bytes differ: '+row['destination'])
 target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
for name in ('DELIVERY_MANIFEST.json','integration-map.json'):shutil.copyfile(here/name,snapshot/name)
for row in manifest['files']:
 data=(snapshot/row['path']).read_bytes()
 if sha(data)!=row['sha256'] or len(data)!=row['bytes']:raise ValueError('Snapshot differs: '+row['path'])
for name in ('independent_semantic_probes.py','independent_import_probes.py'):shutil.copyfile(here/name,out/name)
print(json.dumps({'snapshot':str(snapshot),'sealedMembers':len(manifest['files']),'mappedFiles':len(mapping['mappings']),'verified':True}),flush=True)
if not args.prepare_only:
 for name,folder in [('independent_semantic_probes.py','api'),('independent_import_probes.py','imports')]:
  subprocess.run([sys.executable,'-B',str(out/name),'--snapshot',str(snapshot),'--out',str(out/folder)],check=True,cwd=out)
 subprocess.run([sys.executable,'-B',str(repo/mapping['checkerRoot']/'run_cases.py'),'--package-root',str(repo/mapping['packageRoot']),'--fixtures-root',str(repo/mapping['sourceRoot']),'--source-root',str(repo/mapping['sourceRoot']),'--report',str(out/'installed-cli-results.json')],check=True,cwd=out)
