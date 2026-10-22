"""Opt-in fictional interface conformance; never activates authorization."""
from pathlib import Path
import base64,copy,json,subprocess,sys,os
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H.parents[2]/'plans/domain-contract-verifier-20261021/local-dependencies'))
from build_fixtures import raw,encode
from path_common import sha,digest
from verify_success_path import verify
from jsonschema import Draft202012Validator
OUT=H/'checks';OUT.mkdir(exist_ok=True);REPORT=json.loads((H/'schemas/report.schema.json').read_text());results=[]
def replace(v,old,new):
 if v==old:return copy.deepcopy(new)
 if isinstance(v,dict):return {k:replace(x,old,new) for k,x in v.items()}
 if isinstance(v,list):return [replace(x,old,new) for x in v]
 return v

def repin(m,bundle=True,source_digests=True):
 if source_digests:
  for entry in list(m['context']['sources']):
   rec=m['sources'][entry['key']]
   if 'sourceRecordDigest' in rec:
    d=digest({k:v for k,v in rec.items() if k!='sourceRecordDigest'})
    if d!=rec['sourceRecordDigest']:
     old=copy.deepcopy(entry['binding']);new={'ref':old['ref'],'digest':d};rec['sourceRecordDigest']=d;m=replace(m,old,new)
 if bundle:
  r=copy.deepcopy(m['sources']['RESULT']);t=copy.deepcopy(m['sources']['TRACE']);r.pop('decisionBundleDigest');t.pop('decisionBundleDigest');d=digest({'schemaVersion':'ofarm.authorizationDecisionBundleDigestInput.v0.2','request':m['sources']['REQUEST'],'result':r,'trace':t});m['sources']['RESULT']['decisionBundleDigest']=d;m['sources']['TRACE']['decisionBundleDigest']=d;m['evidence']['decisionBundleDigest']=d
 for entry in m['context']['sources']:
  if entry['key'] in m['sources']:
   b=raw(m['sources'][entry['key']]);entry['bytesSha256']=sha(b);entry['valueDigest']=digest(m['sources'][entry['key']])
 return m

def paths(m):return [m['evidence']['selectedPath'],m['sources']['RESULT']['projection']['selectedPath'],m['sources']['TRACE']['projection']['paths'][0]]
def run(name,m,expected='FAIL',mutate_bytes=None,cli=False):
 w=encode(m)
 if mutate_bytes:mutate_bytes(w)
 dec=lambda x:base64.b64decode(x)
 cb=dec(w['contextBytesBase64']);pin=sha(cb)
 r=verify(dec(w['evidenceBytesBase64']),dec(w['profileBytesBase64']),cb,{k:dec(v) for k,v in w['sourceBytesBase64'].items()},{k:dec(v) for k,v in w['schemaBytesBase64'].items()},expected_context_sha256=pin)
 Draft202012Validator(REPORT).validate(r)
 okay=r['disposition']==expected if expected=='PASS' else r['disposition']!='PASS'
 d=OUT/name;d.mkdir(exist_ok=True);(d/'wire.json').write_bytes(raw(w));(d/'context.sha256').write_text(pin+'\n');(d/'api-report.json').write_bytes(raw(r))
 entry={'id':name,'expected':expected,'actual':r['disposition'],'codes':[x['code'] for x in r['errors']],'matched':okay}
 if cli:
  p=subprocess.run([sys.executable,'-B',str(H/'verify_success_path.py'),'--wire',str(d/'wire.json'),'--context-sha256',pin],capture_output=True,timeout=45)
  actual=json.loads(p.stdout);(d/'cli-report.json').write_bytes(raw(actual));entry['cliMatchesApi']=actual==r;entry['cliExitCode']=p.returncode;entry['matched']=okay and actual==r and p.returncode=={'PASS':0,'FAIL':1,'INPUT_ERROR':2}[r['disposition']]
 results.append(entry);print(name,entry['actual'],'OK' if entry['matched'] else 'MISMATCH',','.join(entry['codes']),flush=True)

def mutate_core(m,key,field,value):m['sources'][key]['projection'][field]=value;return repin(m)
for d in sorted((H/'fixtures').glob('basis-*')):
 base=json.loads((d/'model.json').read_text());tag=d.name
 run(tag+'-baseline',copy.deepcopy(base),'PASS',cli=True)
 # Digest-bound Party support without rewriting the selected source bytes.
 m=copy.deepcopy(base);entry=next(x for x in m['context']['sources'] if x['key']=='AUTHORITY_SUBJECT_PARTY');old=entry['binding'];new={'ref':old['ref'],'digest':digest(m['sources']['AUTHORITY_SUBJECT_PARTY'])};m=replace(m,old,new);run(tag+'-digest-party',repin(m),'PASS')
 m=copy.deepcopy(base);old=m['context']['profileBinding'];new={'ref':old['ref'],'digest':digest(m['profile'])};m=replace(m,old,new);run(tag+'-digest-profile',m,'PASS')
 m=copy.deepcopy(base);other=copy.deepcopy(m['sources']['TRACE']['projection']['paths'][0]);other['pathId']='path:other';other['pathDisposition']='PATH_DENY';m['sources']['TRACE']['projection']['paths'].append(other);run(tag+'-retained-other-path',repin(m),'PASS')
 for field,value in [('authoritySubjectPartyRef','party:substitute'),('pathId','path:wrong'),('authoritySubjectBasis','NATURAL_PERSON_SELF' if 'basis-1-' not in tag else 'AGENT_PARTY_DIRECT_GRANT')]:
  m=copy.deepcopy(base);m['evidence']['selectedPath'][field]=value;run(tag+'-evidence-'+field,m)
 m=copy.deepcopy(base)
 for p in paths(m):p['authoritySubjectPartyRef']='party:substitute'
 run(tag+'-coherent-mirrored-party',repin(m),cli=True)
 for role in ['AUTHENTICATED_PRINCIPAL','PRINCIPAL_RESOLUTION','SOURCE_AUTHORITY','AUTHORITY_SUBJECT_PARTY']:
  m=copy.deepcopy(base)
  for p in paths(m):p['basis']=[x for x in p['basis'] if x['role']!=role];p['authoritySubjectBasisRefs']=[x['binding'] for x in p['basis']]
  run(tag+'-missing-'+role,repin(m))
 m=copy.deepcopy(base)
 for p in paths(m):p['canonicalTuple']['pathTypeOrder']=3
 run(tag+'-wrong-canonical-tuple',repin(m))
 m=copy.deepcopy(base);m['sources']['SOURCE_AUTHORITY']['projection']['grantTarget']['targetRef']='party:other';run(tag+'-source-target-substitution',repin(m))
 m=copy.deepcopy(base)
 for p in paths(m):p['delegationSourceBindings'].append({'ref':'source:unresolved','digest':'sha256:'+'1'*64});p['canonicalTuple']['delegationSourceRecordIds']=sorted(x['ref'] for x in p['delegationSourceBindings'])
 run(tag+'-unresolved-tuple-source',repin(m))
 for core,field,value in [('REQUEST','actionClass','ASSERT_STRUCTURE'),('RESULT','snapshotBinding',{'ref':'snapshot:wrong','revisionRef':'r1'}),('TRACE','selectedPathId','path:wrong'),('RULE','actionClass','ASSERT_COMPLIANCE'),('BINDING_MANIFEST','ruleBinding',{'ref':'rule:wrong','revisionRef':'r1'}),('DERIVED_VIEW','actionClass','ASSERT_COMPLIANCE'),('EVALUATION_SNAPSHOT','authorizationEvaluatedAt','2026-10-21T08:59:59Z')]:
  run(tag+'-wrong-'+core,mutate_core(copy.deepcopy(base),core,field,value))
 m=copy.deepcopy(base);m['sources']['EFFECT_INTENT']['projection']['proposedAssertion']['text']='A different complete effect';run(tag+'-intent-substitution',repin(m))
 m=copy.deepcopy(base);m['sources']['RESULT']['retainedPayload']['decisionBundleDigest']='changed nested value';run(tag+'-nested-bundle-field',repin(m,bundle=False))
 m=copy.deepcopy(base);m['sources']['visibility:SOURCE_AUTHORITY']['projection']['snapshotBinding']={'ref':'snapshot:wrong','revisionRef':'r1'};run(tag+'-wrong-visibility-snapshot',repin(m))
 m=copy.deepcopy(base);m['sources']['EVALUATION_SNAPSHOT']['projection']['visibleBasis']=[];run(tag+'-missing-snapshot-basis',repin(m))
 for f in ['historyPosition','indexWatermarks','evidencePolicyRegistryBinding','sovereigntyPolicyBinding']:
  m=copy.deepcopy(base);del m['sources']['EVALUATION_SNAPSHOT']['projection'][f];run(tag+'-missing-snapshot-'+f,repin(m))
 m=copy.deepcopy(base);m['context']['sources'][0]['binding']={'ref':'mutable:bare'};run(tag+'-mutable-selector',m)
 m=copy.deepcopy(base);m['profile']['outputKind']='CONSUMER_REPORT';m['context']['profileBytesSha256']=sha(raw(m['profile']));run(tag+'-consumer-report-profile',m)
 # Parser/raw-byte tests are run against every basis, without repairing pins.
 run(tag+'-changed-original-byte',copy.deepcopy(base),mutate_bytes=lambda w:w['sourceBytesBase64'].__setitem__('REQUEST',base64.b64encode(base64.b64decode(w['sourceBytesBase64']['REQUEST'])+b' ').decode()))
 run(tag+'-duplicate-json-name',copy.deepcopy(base),mutate_bytes=lambda w:w.__setitem__('evidenceBytesBase64',base64.b64encode(b'{"a":1,"a":2}').decode()))
 run(tag+'-nonfinite-json',copy.deepcopy(base),mutate_bytes=lambda w:w.__setitem__('evidenceBytesBase64',base64.b64encode(b'{"a":1e309}').decode()))
 run(tag+'-unpaired-surrogate',copy.deepcopy(base),mutate_bytes=lambda w:w.__setitem__('evidenceBytesBase64',base64.b64encode(b'{"a":"\\ud800"}').decode()))
 run(tag+'-depth-limit',copy.deepcopy(base),mutate_bytes=lambda w:w.__setitem__('evidenceBytesBase64',base64.b64encode(b'['*65+b'0'+b']'*65).decode()))
 if 'basis-3' in tag or 'basis-4' in tag:
  for role,field,value in [('CP3_ACTORSHIP_BINDING','agentInstanceRef','principal:other'),('CP3_AUTHORITY_ENVELOPE','executingAgentInstanceRef','principal:other'),('CP3_AUTHORITY_ENVELOPE','agentSponsorRef','party:other'),('AGENT_IDENTITY','agentPartyRef','party:sponsor')]:
   run(tag+'-mismatch-'+role+'-'+field,mutate_core(copy.deepcopy(base),role,field,value))
  for role,field,value in [('CP3_AUTHORITY_ENVELOPE','authorizationDecisionResultRef','result:other'),('CP3_AUTHORITY_ENVELOPE','authorizationDecisionTraceRef','trace:other'),('CP3_AUTHORITY_ENVELOPE','requestedActionClass','ASSERT_STRUCTURE'),('CP3_REVOCATION_STATE','authorityEnvelopeRef','envelope:other')]:
   run(tag+'-mismatch-'+role+'-'+field,mutate_core(copy.deepcopy(base),role,field,value))
 if 'basis-2' in tag:run(tag+'-representation-party-substitution',mutate_core(copy.deepcopy(base),'REPRESENTATION_BASIS','representedPartyRef','party:other'))
 if 'basis-4' in tag:run(tag+'-delegation-agent-substitution',mutate_core(copy.deepcopy(base),'DELEGATION_GRANT','delegatePartyRef','party:other'))
summary={'status':'FICTIONAL_OFFLINE_CONFORMANCE_ONLY','cases':len(results),'matched':sum(x['matched'] for x in results),'failed':sum(not x['matched'] for x in results),'results':results,'next':'Independent review of the exact sealed interface; no authorization, canonical-selection or runtime admission is established.'}
(H/'conformance-results.json').write_bytes(raw(summary));print(json.dumps({k:v for k,v in summary.items() if k!='results'},indent=2));raise SystemExit(bool(summary['failed']))
