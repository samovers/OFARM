"""Independent-selection, parser, schema-closure and installed-layout probes."""
from pathlib import Path
import json,copy,sys,base64,subprocess,os,shutil
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H.parents[2]/'plans/domain-contract-verifier-20261021/local-dependencies'))
from build_fixtures import raw,encode
from path_common import sha,digest
from verify_success_path import verify
from jsonschema import Draft202012Validator
EXPECTED_ERRORS={'invalid-utf8': 'INVALID_JSON_OR_CANONICAL_VALUE', 'utf8-bom': 'INVALID_JSON_OR_CANONICAL_VALUE', 'duplicate-key': 'DUPLICATE_JSON_MEMBER', 'unsafe-integer': 'INVALID_JSON_OR_CANONICAL_VALUE', 'oversize': 'INVALID_INPUT_BYTES', 'array-instead-of-object': 'SCHEMA_INVALID', 'independent-context-digest-required': 'INDEPENDENT_CONTEXT_DIGEST_REQUIRED', 'independent-context-raw-mismatch': 'INDEPENDENT_CONTEXT_BYTES_MISMATCH', 'mirrored-party-in-context': 'SCHEMA_INVALID', 'admitted-boolean-in-context': 'SCHEMA_INVALID', 'duplicate-source-key': 'DUPLICATE_SOURCE_KEY', 'wrong-source-value-digest': 'SOURCE_VALUE_DIGEST_MISMATCH', 'missing-source-bytes': 'SOURCE_SET_MISMATCH', 'extra-source-bytes': 'SOURCE_SET_MISMATCH', 'malformed-selector': 'SCHEMA_INVALID', 'unresolved-selector': 'UNRESOLVED_POINTER', 'unresolved-unused-schema-ref': 'UNRESOLVED_SCHEMA_REFERENCE', 'nested-schema-id': 'NESTED_SCHEMA_ID_NOT_SUPPORTED', 'invalid-schema': 'MALFORMED_SOURCE_OR_DEPENDENCY', 'dynamic-schema-ref': 'DYNAMIC_SCHEMA_REFERENCE_NOT_SUPPORTED', 'missing-installed-source-root': 'PACKAGE_CLOSURE_MISMATCH', 'changed-installed-source-law': 'PACKAGE_CLOSURE_MISMATCH'}
base=json.loads((H/'fixtures/basis-1-party/model.json').read_text());out=H/'edge-checks';out.mkdir(exist_ok=True);rows=[]
def run(name,m=None,overrides=None,expected='FAIL'):
 m=copy.deepcopy(base) if m is None else m
 args=[raw(m['evidence']),raw(m['profile']),raw(m['context']),{k:raw(v) for k,v in m['sources'].items()},{k:raw(v) for k,v in m['schemas'].items()}]
 pin=sha(args[2]);kw={}
 if overrides:
  for k,v in overrides.items():
   if type(k)is int:args[k]=v
   else:kw[k]=v
 r=verify(*args,expected_context_sha256=kw.pop('pin',pin),**kw);Draft202012Validator(json.loads((H/'schemas/report.schema.json').read_text())).validate(r)
 expected_codes=[] if expected=='PASS' else [EXPECTED_ERRORS[name]]
 okay=((r['disposition']=='PASS') if expected=='PASS' else r['disposition'] in ['FAIL','INPUT_ERROR']) and [x['code'] for x in r['errors']]==expected_codes;entry={'id':name,'expected':expected,'expectedCodes':expected_codes,'actual':r['disposition'],'matched':okay,'report':r};rows.append(entry)
 w={'schemaVersion':'ofarm.canonicalSuccessfulPathVerificationWire.v0.1','evidenceBytesBase64':base64.b64encode(args[0]).decode(),'profileBytesBase64':base64.b64encode(args[1]).decode(),'contextBytesBase64':base64.b64encode(args[2]).decode(),'sourceBytesBase64':{k:base64.b64encode(v).decode() for k,v in args[3].items()},'schemaBytesBase64':{k:base64.b64encode(v).decode() for k,v in args[4].items()}}
 d=out/name;d.mkdir(exist_ok=True);(d/'wire.json').write_bytes(raw(w));(d/'context.sha256').write_text(overrides.get('pin',pin)+'\n' if overrides else pin+'\n');(d/'report.json').write_bytes(raw(entry));print(name,r['disposition'],r['errors'],flush=True)
for name,blob in [('invalid-utf8',b'\xff'),('utf8-bom',b'\xef\xbb\xbf{}'),('duplicate-key',b'{"evidenceId":"a","evidenceId":"b"}'),('unsafe-integer',b'{"x":9007199254740993}'),('oversize',b' '*((4*1024*1024)+1)),('array-instead-of-object',b'[]')]:run(name,overrides={0:blob})
run('independent-context-digest-required',overrides={'pin':''})
run('independent-context-raw-mismatch',overrides={2:raw(base['context'])+b' '})
m=copy.deepcopy(base);m['context']['expectedParty']='party:natural';run('mirrored-party-in-context',m)
m=copy.deepcopy(base);m['context']['admitted']=True;run('admitted-boolean-in-context',m)
m=copy.deepcopy(base);m['context']['sources'].append(copy.deepcopy(m['context']['sources'][0]));run('duplicate-source-key',m)
m=copy.deepcopy(base);m['context']['sources'][0]['valueDigest']='sha256:'+'0'*64;run('wrong-source-value-digest',m)
m=copy.deepcopy(base);del m['sources']['AUTHORITY_SUBJECT_PARTY'];run('missing-source-bytes',m)
m=copy.deepcopy(base);m['sources']['unselected']=copy.deepcopy(m['sources']['REQUEST']);run('extra-source-bytes',m)
m=copy.deepcopy(base);m['profile']['formats']['RESULT']['identityPointer']='/projection/resultId~2';m['context']['profileBytesSha256']=sha(raw(m['profile']));run('malformed-selector',m)
m=copy.deepcopy(base);m['profile']['formats']['RESULT']['identityPointer']='/missing';m['context']['profileBytesSha256']=sha(raw(m['profile']));run('unresolved-selector',m)
for name,modify in [('unresolved-unused-schema-ref',lambda s:s.update({'$defs':{'unused':{'$ref':'https://unselected.invalid/schema'}}})),('nested-schema-id',lambda s:s.update({'$defs':{'x':{'$id':'https://shadow.invalid/schema','type':'string'}}})),('invalid-schema',lambda s:s.update(type='nonsense')),('dynamic-schema-ref',lambda s:s.update({'$dynamicRef':'#any'}))]:
 m=copy.deepcopy(base);sid=m['profile']['formats']['AUTHORITY_SUBJECT_PARTY']['schemaId'];modify(m['schemas'][sid]);h=sha(raw(m['schemas'][sid]));m['profile']['schemaDigests'][sid]=h;m['profile']['formats']['AUTHORITY_SUBJECT_PARTY']['schemaSha256']=h;m['context']['profileBytesSha256']=sha(raw(m['profile']));run(name,m)
# Original complete intent can be bound by digest without an embedded intent ID.
m=copy.deepcopy(base);old=copy.deepcopy(m['context']['sources'][next(i for i,x in enumerate(m['context']['sources']) if x['key']=='EFFECT_INTENT')]['binding']);new={'ref':old['ref'],'digest':digest(m['sources']['EFFECT_INTENT'])}
def repl(v):
 if v==old:return copy.deepcopy(new)
 if isinstance(v,dict):return {k:repl(x) for k,x in v.items()}
 if isinstance(v,list):return [repl(x) for x in v]
 return v
m=repl(m);m['profile']['formats']['EFFECT_INTENT']['identityPointer']=None;m['context']['profileBytesSha256']=sha(raw(m['profile']))
r=copy.deepcopy(m['sources']['RESULT']);t=copy.deepcopy(m['sources']['TRACE']);r.pop('decisionBundleDigest');t.pop('decisionBundleDigest');d=digest({'schemaVersion':'ofarm.authorizationDecisionBundleDigestInput.v0.2','request':m['sources']['REQUEST'],'result':r,'trace':t})
for key in ['RESULT','TRACE']:m['sources'][key]['decisionBundleDigest']=d
m['evidence']['decisionBundleDigest']=d
m['sources']['DERIVED_VIEW']['projection']['intentBinding']=new
# The view changes too; its digest is retained in both owner outputs.
for key in ['RESULT','TRACE']:m['sources'][key]['projection']['derivedViewDigest']=digest(m['sources']['DERIVED_VIEW'])
r=copy.deepcopy(m['sources']['RESULT']);t=copy.deepcopy(m['sources']['TRACE']);r.pop('decisionBundleDigest');t.pop('decisionBundleDigest');d=digest({'schemaVersion':'ofarm.authorizationDecisionBundleDigestInput.v0.2','request':m['sources']['REQUEST'],'result':r,'trace':t})
for key in ['RESULT','TRACE']:m['sources'][key]['decisionBundleDigest']=d
m['evidence']['decisionBundleDigest']=d
for entry in m['context']['sources']:entry['bytesSha256']=sha(raw(m['sources'][entry['key']]));entry['valueDigest']=digest(m['sources'][entry['key']])
run('content-bound-complete-intent',m,expected='PASS')
# Check the exact split layout used by the integration map.
layout=out/'installed-layout';pkg=layout/'03_machine_contracts/drafts_non_default/authorization_decision_evidence/canonical_success_path';runner=layout/'04_implementation_and_conformance/conformance_runners/canonical_success_path';pkg.mkdir(parents=True,exist_ok=True);runner.mkdir(parents=True,exist_ok=True)
semantic=layout/'04_implementation_and_conformance/examples_and_fixtures/fixtures/canonical_success_path';semantic.mkdir(parents=True,exist_ok=True)
c=json.loads((H/'contract.json').read_text())
for f in ['contract.json',*c['files']]:
 dest=(semantic if f.startswith('sources/') else pkg)/f;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes((H/f).read_bytes())
 if f.startswith('sources/') and (pkg/f).exists():(pkg/f).unlink()
for f in c['verificationCode']:(runner/f).write_bytes((H/f).read_bytes())
installed=[]
for src in sorted((H/'fixtures').glob('basis-*')):
 pin=(src/'context.sha256').read_text().strip();p=subprocess.run([sys.executable,'-B',str(runner/'verify_success_path.py'),'--wire',str(src/'wire.json'),'--context-sha256',pin,'--contract-root',str(pkg),'--source-root',str(semantic)],capture_output=True,timeout=45);r=json.loads(p.stdout);installed.append({'id':src.name,'exitCode':p.returncode,'report':r,'matched':p.returncode==0 and r['disposition']=='PASS'})
(out/'installed-layout-results.json').write_bytes(raw(installed));rows.extend({'id':'installed-'+x['id'],'matched':x['matched'],'actual':x['report']['disposition']} for x in installed)
run('missing-installed-source-root',overrides={'contract_root':pkg})
(semantic/'sources/pr11.md').write_bytes((semantic/'sources/pr11.md').read_bytes()+b' ')
run('changed-installed-source-law',overrides={'contract_root':pkg,'source_root':semantic})
# Restore the test installation to the shipped bytes; no source packet is edited.
(semantic/'sources/pr11.md').write_bytes((H/'sources/pr11.md').read_bytes())
summary={'cases':len(rows),'matched':sum(x['matched'] for x in rows),'failed':sum(not x['matched'] for x in rows),'results':rows,'next':'Independent review; all successful results remain conditional source comparisons.'};(H/'edge-results.json').write_bytes(raw(summary));print(json.dumps({k:v for k,v in summary.items() if k!='results'}));raise SystemExit(bool(summary['failed']))
