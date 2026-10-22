"""Opt-in installed conformance runner. Never included in default CI."""
import argparse,json,subprocess,sys
from pathlib import Path

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--package-root',required=True);ap.add_argument('--fixtures-root',required=True);ap.add_argument('--source-root',required=True);ap.add_argument('--case-index',default='cases.json');ap.add_argument('--report',required=True);args=ap.parse_args()
 root=Path(args.fixtures_root).resolve();index=json.loads((root/args.case_index).read_text());rows=[]
 for c in index['cases']:
  wire=(root/c['wire']).resolve();pin=(root/c['contextPin']).resolve()
  if not wire.is_relative_to(root) or not pin.is_relative_to(root):raise ValueError('Case path escapes fixture root')
  p=subprocess.run([sys.executable,'-B',str(Path(__file__).with_name('verify_success_path.py')),'--wire',str(wire),'--context-sha256',pin.read_text().strip(),'--contract-root',args.package_root,'--source-root',args.source_root],capture_output=True,timeout=60)
  try:r=json.loads(p.stdout)
  except (ValueError,UnicodeError):r={'disposition':'INVALID_REPORT'}
  passed=r.get('disposition')=='PASS';okay=passed if c['expected']=='PASS' else r.get('disposition') in ['FAIL','INPUT_ERROR']
  okay=okay and [x['code'] for x in r.get('errors',[])]==c['expectedCodes']
  if c.get('expectedDetailContains'):okay=okay and len(r.get('errors',[]))==1 and c['expectedDetailContains'] in r['errors'][0]['detail']
  okay=okay and p.returncode=={'PASS':0,'FAIL':1,'INPUT_ERROR':2}.get(r.get('disposition'))
  rows.append({'id':c['id'],'expected':c['expected'],'actual':r.get('disposition'),'expectedCodes':c['expectedCodes'],'actualCodes':[x['code'] for x in r.get('errors',[])],'exitCode':p.returncode,'matched':okay})
 result={'cases':len(rows),'matched':sum(x['matched'] for x in rows),'results':rows,'scope':'FICTIONAL_SELECTED_OUTPUT_INTEGRITY_ONLY'};Path(args.report).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='results'}));return int(result['matched']!=result['cases'])
if __name__=='__main__':raise SystemExit(main())
