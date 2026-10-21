"""Reproducible fictional act cases. Expected outcomes are authored here.

No network, Git, runtime resolver, producer or authority evaluator is invoked.
"""
from pathlib import Path
import argparse,copy,hashlib,json,os,shutil,subprocess,sys,tempfile
P=Path(__file__).resolve().parent
KEYS=['act','content','rendered','intent','context','policy']
PASS='CONDITIONAL_CONFORMANCE_PASS'
def raw(v):return (json.dumps(v,indent=2,ensure_ascii=False)+'\n').encode()
def sha(v):return hashlib.sha256(v).hexdigest()
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--package-root',type=Path,default=P);ap.add_argument('--fixture-root',type=Path,default=P);ap.add_argument('--dependency-dir',type=Path);ap.add_argument('--output-dir',type=Path);a=ap.parse_args()
 C=a.package_root.resolve();F=a.fixture_root.resolve()
 if a.dependency_dir:sys.path.insert(0,str(a.dependency_dir.resolve()))
 import rfc8785
 from jsonschema import Draft202012Validator
 import verify_assertion_act as checker
 import act_common
 from act_report_contract import REPORT_SCHEMA
 def dg(v):return 'sha256:'+sha(rfc8785.dumps(v))
 def rd(p):return json.loads(p.read_bytes())
 temp=None
 if a.output_dir:out=a.output_dir.resolve();out.mkdir(parents=True,exist_ok=True)
 else:temp=tempfile.TemporaryDirectory(prefix='.act-checks-',dir=P);out=Path(temp.name)
 def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw(v))
 records=[];catalog=[];validator=Draft202012Validator(rd(C/'schemas/report.schema.json'))
 specs=rd(F/'fixtures/positive-cases.json')['cases']
 def load(s):return {'raws':{k:(F/s['paths'][k]).read_bytes() for k in KEYS},'sources':{v['ref']:(F/v['path']).read_bytes() for v in s['sourceInputs']},'pins':copy.deepcopy(s['trustedPins']),'selection':copy.deepcopy(s['expectedActSelection']),'profile':(F/s['paths']['intentProfile']).read_bytes(),'bundle':{k:(F/v).read_bytes() for k,v in s['schemaBundle'].items()}}
 def val(s,k):return json.loads(s['raws'][k])
 def put(s,k,v):s['raws'][k]=raw(v)
 def mutate(s,k,fn):v=val(s,k);fn(v);put(s,k,v)
 def repin_context(s):s['pins']['contextSha256']=sha(s['raws']['context'])
 def repin_act(s):
  v=val(s,'act');s['selection']={'binding':{'ref':v['recordId'],'digest':dg(v)},'bytesSha256':sha(s['raws']['act']),'valueDigest':dg(v)}
 def run(name,s,status,code=None,package=C,*,persist=True,expected=None):
  kw={'trusted_pins':s['pins'],'expected_act_selection':s['selection'],'package_root':package,'intent_profile_bytes':s['profile'],'schema_bundle':s['bundle']}
  r=checker.verify(*(s['raws'][k] for k in KEYS),s['sources'],**kw);again=checker.verify(*(s['raws'][k] for k in KEYS),s['sources'],**kw)
  schema_errors=list(validator.iter_errors(r));codes=[x['code'] for x in r['errors']]
  ok=r['status']==status and (code is None or code in codes) and not schema_errors and r==again and r['runtimeAdmission']=='NOT_ESTABLISHED' and 'AUTHORIZATION_SELECTED_PATH_SOURCE_CONTRACT_UNIDENTIFIED' in r['unestablishedClaims']
  if status==PASS:ok=ok and set(r['checkedRules'])==set(rd(C/'contract.json')['requiredRules'])
  if expected:ok=ok and all(r['result'][k]==v for k,v in expected.items())
  records.append({'id':name,'pass':bool(ok),'expectedStatus':status,'actualStatus':r['status'],'requiredErrorCode':code,'errorCodes':codes,'reportSchemaValid':not schema_errors,'deterministic':r==again})
  if persist:
   entry={'id':name,'expectedStatus':status,'requiredErrorCode':code,'trustedPins':s['pins'],'expectedActSelection':s['selection'],'inputs':{},'sources':{},'intentProfileSha256':sha(s['profile']) if isinstance(s['profile'],bytes) else None,'schemaBundleHashes':{k:sha(v) for k,v in s['bundle'].items()} if isinstance(s['bundle'],dict) else None,'report':'reports/'+name+'.json'}
   for k,b in s['raws'].items():
    if isinstance(b,bytes):path='input-bytes/'+sha(b)+'.json';(out/path).parent.mkdir(parents=True,exist_ok=True);(out/path).write_bytes(b);entry['inputs'][k]=path
    else:entry['inputs'][k]={'apiValue':b}
   if isinstance(s['sources'],dict):
    for k,b in s['sources'].items():
     if isinstance(b,bytes):path='input-bytes/'+sha(b)+'.json';(out/path).write_bytes(b);entry['sources'][k]=path
   catalog.append(entry);write(out/entry['report'],r)
  if not ok:print('FAIL',name,r['status'],codes,[e.message for e in schema_errors])
  return r
 for spec in specs:run(spec['id'],load(spec),PASS,expected={'accountablePartyRef':spec['expectedParty'],'assertedAt':spec['expectedAssertedAt'],'posture':spec['expectedPosture']})
 bases=[load(specs[0]),load(specs[1])]
 for base,label in zip(bases,['online','offline']):
  def attack(name,key,fn,code,status='FAIL'):
   s=copy.deepcopy(base);mutate(s,key,fn);return run(label+'-'+name,s,status,code)
  for key in KEYS:
   for suffix,b,code,status in [('missing',None,'MISSING_OR_NONBYTE_INPUT','INPUT_ERROR'),('duplicate',b'{"a":1,"a":2}','DUPLICATE_JSON_NAME','INPUT_ERROR'),('deep',b'['*1100+b'0'+b']'*1100,'INPUT_DEPTH_LIMIT','INPUT_ERROR'),('unsafe-number',b'{"v":9007199254740992}','NON_CANONICAL_VALUE','INPUT_ERROR'),('bad-utf8',b'\xff','INVALID_UTF8_JSON','INPUT_ERROR')]:
    s=copy.deepcopy(base);s['raws'][key]=b;run(label+'-'+key+'-'+suffix,s,status,code)
  attack('changed-body','rendered',lambda v:v['assertionBody'].update(claimText='Changed claim.'),'COMPLETE_CONTENT_MISMATCH')
  attack('changed-subject','rendered',lambda v:v['subject'].update(subjectRef='field:other'),'COMPLETE_CONTENT_MISMATCH')
  attack('changed-scope','rendered',lambda v:v['resources'][0]['scope'].update(scopeRef='field:other'),'COMPLETE_CONTENT_MISMATCH')
  attack('changed-evidence','rendered',lambda v:v['evidenceBindings'][0].update(digest='sha256:'+'0'*64),'COMPLETE_CONTENT_MISMATCH')
  attack('extra-submitted-field','rendered',lambda v:v.update(laterReceiptBinding={'ref':'receipt:later','digest':'sha256:'+'0'*64}),'COMPLETE_CONTENT_MISMATCH')
  attack('act-metadata-in-rendered-body','rendered',lambda v:v.update(assertedAt=val(base,'act')['assertedAt']),'ACT_METADATA_IN_RENDERED_CONTENT')
  attack('changed-intent-body','intent',lambda v:v['assertionBody'].update(claimText='Changed after the act.'),'COMPLETE_CONTENT_MISMATCH')
  # Both strings have equal JSON values; the original rendered field bytes still matter.
  s=copy.deepcopy(base);s['raws']['intent']=json.dumps(val(s,'intent'),separators=(',',':')).encode();run(label+'-rerendered-intent',s,'FAIL','RENDERED_FIELD_BYTES_CHANGED')
  attack('wrong-party','act',lambda v:v.update(accountablePartyRef='party:fictional:performer'),'ACCOUNTABLE_PARTY_OR_BASIS_MISMATCH')
  attack('wrong-basis','act',lambda v:v.update(authoritySubjectBasis='AGENT_PARTY_DIRECT_GRANT'),'ACCOUNTABLE_PARTY_OR_BASIS_MISMATCH')
  attack('wrong-basis-record','act',lambda v:v['authoritySubjectBasisBindings'][0].update(revisionRef='basis:other:r1'),'ACCOUNTABLE_PARTY_OR_BASIS_MISMATCH')
  attack('wrong-time','act',lambda v:v.update(assertedAt='2026-10-20T12:34:57.123456789Z'),'SOURCE_TIME_MISMATCH')
  attack('wrong-policy','act',lambda v:v['sourcePolicyBinding'].update(digest='sha256:'+'0'*64),'SOURCE_POLICY_BINDING_MISMATCH')
  attack('wrong-posture','act',lambda v:v.update(posture='VERIFIED_OFFLINE_SUBMISSION' if label=='online' else 'TRUSTED_ONLINE_SUBMISSION'),'ACT_POSTURE_MISMATCH')
  attack('wrong-source-kind','act',lambda v:v.update(sourceKind='IMMUTABLE_OFFLINE_ASSERTION_ACT' if label=='online' else 'TRUSTED_RUNTIME_SUBMISSION_OBSERVATION'),'ACT_POSTURE_MISMATCH')
  attack('wrong-contract','act',lambda v:v['contractBinding'].update(digest='sha256:'+'0'*64),'CONTRACT_BINDING_MISMATCH')
  attack('forged-admitted','act',lambda v:v.update(admitted=True),'SCHEMA_INVALID')
  for field in ['selfBinding','effectIntentDigest','domainVerdictBinding','domainTraceBinding','finalAssertionEffect','receiptBinding','verificationContextBinding','dependencies']:
   attack('late-'+field,'act',lambda v,k=field:v.update({k:{'ref':'late:output','digest':'sha256:'+'0'*64}}),'SCHEMA_INVALID')
  attack('late-input-role','act',lambda v:v['inputRoles'].append('LATER_INTENT'),'SCHEMA_INVALID')
  attack('policy-as-admission','policy',lambda v:v.update(admitted=True),'SCHEMA_INVALID')
  attack('policy-fake-timestamp-rule','policy',lambda v:v.update(timestampRule='CALLER_TIMESTAMP_ACCEPTED'),'SCHEMA_INVALID')
  s=copy.deepcopy(base);s['selection']['valueDigest']='sha256:'+'0'*64;run(label+'-wrong-immutable-selector',s,'FAIL','ACT_SELECTOR_MISMATCH')
  s=copy.deepcopy(base);s['selection']['binding']['ref']='act:other';run(label+'-wrong-immutable-ref',s,'FAIL','ACT_SELECTOR_MISMATCH')
  s=copy.deepcopy(base);s['selection']={};run(label+'-missing-selector',s,'INPUT_ERROR','INVALID_ACT_SELECTION')
  for key,code in [('contextSha256','CONTEXT_PIN_MISMATCH'),('policySha256','POLICY_PIN_MISMATCH'),('contractSha256','CONTRACT_PIN_MISMATCH'),('intentProfileSha256','INTENT_PROFILE_PIN_MISMATCH')]:
   s=copy.deepcopy(base);s['pins'][key]='0'*64;run(label+'-wrong-'+key,s,'INPUT_ERROR' if key=='contractSha256' else 'FAIL',code)
  s=copy.deepcopy(base);s['pins']={};run(label+'-missing-pins',s,'INPUT_ERROR','INVALID_INDEPENDENT_PINS')
  # Forging a new self-consistent act cannot replace independent selected roots.
  s=copy.deepcopy(base);mutate(s,'act',lambda v:v.update(accountablePartyRef='party:attacker'));repin_act(s)
  run(label+'-forged-act-recomputed-selector',s,'FAIL','ACT_SELECTION_CONTEXT_MISMATCH')
  for timestamp in ['2026-02-30T12:00:00Z','2026-10-20T12:34:56+01:00','2026-10-20T12:34:56+01:99','2026-10-20T12:34:56z','2026-10-20T12:34:56.0Z','2026-10-20T12:34:56.1234567890Z','2026-10-20T24:00:00Z','2026-10-20T23:59:60Z']:
   for key,field in [('act','assertedAt'),('intent','assertedAt'),('context','expectedAssertedAt')]:
    s=copy.deepcopy(base);mutate(s,key,lambda v:v.update({field:timestamp}));run(label+'-bad-time-'+key+'-'+sha(timestamp.encode())[:8],s,'FAIL','SCHEMA_INVALID')
  for ref,source in base['sources'].items():
   s=copy.deepcopy(base);s['sources'][ref]+=b' ';run(label+'-source-whitespace-'+sha(ref.encode())[:8],s,'FAIL','ORIGINAL_SOURCE_BYTES_MISMATCH')
   s=copy.deepcopy(base);v=json.loads(source)
   if 'semanticEventId' in v:v['dominantSemanticConsequence']='Changed content under same logical event ID.'
   else:v['measurementMethod']['procedureRef']='method:changed-under-same-id'
   s['sources'][ref]=raw(v);run(label+'-source-metadata-'+sha(ref.encode())[:8],s,'FAIL','ORIGINAL_SOURCE_BYTES_MISMATCH')
  s=copy.deepcopy(base);s['sources'].pop(next(iter(s['sources'])));run(label+'-missing-source-bytes',s,'FAIL','SOURCE_INPUT_SET_MISMATCH')
  s=copy.deepcopy(base);s['sources']['verdict:later']=b'{}';run(label+'-extra-later-source',s,'FAIL','SOURCE_INPUT_SET_MISMATCH')
  attack('aliased-later-source-role','content',lambda v:v['sourceInputs'][0].update(role='DOMAIN_VERDICT'),'SCHEMA_INVALID')
  attack('self-basis-ref','act',lambda v:v['authoritySubjectBasisBindings'][0].update(ref=v['recordId']),'SELF_OR_LATER_IDENTITY_ALIAS')
  attack('later-context-basis-revision','act',lambda v:v['authoritySubjectBasisBindings'][0].update(revisionRef=val(base,'context')['contextId']),'SELF_OR_LATER_IDENTITY_ALIAS')
  attack('source-self-alias','content',lambda v:v['sourceInputs'][0]['binding'].update(ref=val(base,'act')['recordId']),'SELF_OR_LATER_IDENTITY_ALIAS')
  # General source timestamps also use the repaired numeric-offset validation.
  for offset,valid in [('+01:30',True),('-01:30',True),('+01:60',False),('+01:99',False),('-01:99',False),('+24:00',False)]:
   s=copy.deepcopy(base);ref=next(k for k in s['sources'] if k.startswith('measurement-evidence:'));v=json.loads(s['sources'][ref]);v['resultTime']='2026-05-06T09:20:00'+offset;s['sources'][ref]=raw(v)
   run(label+'-source-offset-'+offset.replace('+','plus').replace('-','minus').replace(':','-'),s,'FAIL','ORIGINAL_SOURCE_BYTES_MISMATCH' if valid else 'SCHEMA_INVALID')
 # R1: a source selector is retained verbatim; the independently pinned context
 # carries its exact resolution. Neither digest nor revision is inferred from spelling.
 def rebind_content(s, select_sources=True):
  content=val(s,'content');content.update(renderedContentBytesSha256=sha(s['raws']['rendered']),renderedContentDigest=dg(val(s,'rendered')));put(s,'content',content)
  cb={'ref':content['contentId'],'digest':dg(content)}
  mutate(s,'act',lambda v:v.update(submittedContentBinding=cb,submittedContentBytesSha256=sha(s['raws']['content'])))
  repin_act(s)
  if val(s,'intent')['assertionActPosture']=='VERIFIED_OFFLINE_SUBMISSION':mutate(s,'intent',lambda v:v.update(assertionActEvidenceBinding=s['selection']['binding']))
  context=val(s,'context');context.update(actSelection=s['selection'],submittedContentBinding=cb,submittedContentBytesSha256=sha(s['raws']['content']),renderedContentBytesSha256=sha(s['raws']['rendered']),intentBytesSha256=sha(s['raws']['intent']),intentDigest=dg(val(s,'intent')))
  if select_sources:context['selectedSourceInputs']=copy.deepcopy(content['sourceInputs'])
  put(s,'context',context);repin_context(s)
 def replace_submitted_selector(s, old, new):
  for key in ['rendered','intent']:
   v=val(s,key);v['evidenceBindings']=[copy.deepcopy(new) if b==old else b for b in v['evidenceBindings']]
   if v.get('associatedSemanticEventBinding')==old:v['associatedSemanticEventBinding']=copy.deepcopy(new)
   put(s,key,v)
 for selector_mode in ['digest','revision']:
  for posture in ['online','offline']:
   spec=next(x for x in specs if x['id']=='operation-natural_person_self-'+posture+('' if selector_mode=='digest' else '-revision'))
   base=load(spec)
   for index,entry in enumerate(val(base,'content')['sourceInputs']):
    label='r1-'+selector_mode+'-'+posture+'-'+str(index);ref=entry['binding']['ref']
    for field in ['valueDigest','bytesSha256']:
     s=copy.deepcopy(base);mutate(s,'content',lambda v:v['sourceInputs'][index].pop(field));rebind_content(s);run(label+'-missing-'+field,s,'FAIL','SCHEMA_INVALID')
     s=copy.deepcopy(base);mutate(s,'content',lambda v:v['sourceInputs'][index].update({field:('sha256:' if field=='valueDigest' else '')+'0'*64}));rebind_content(s);run(label+'-wrong-'+field,s,'FAIL','ORIGINAL_SOURCE_BYTES_MISMATCH')
    s=copy.deepcopy(base);s['sources'][ref]+=b' ';run(label+'-changed-original-bytes',s,'FAIL','ORIGINAL_SOURCE_BYTES_MISMATCH')
    s=copy.deepcopy(base);v=json.loads(s['sources'][ref]);
    if entry['role']=='SEMANTIC_EVENT_ENVELOPE':v['dominantSemanticConsequence']='Source content changed under the same ref.'
    else:v['measurementMethod']['procedureRef']='method:changed-under-same-id'
    s['sources'][ref]=raw(v);run(label+'-changed-original-value',s,'FAIL','ORIGINAL_SOURCE_BYTES_MISMATCH')
    s=copy.deepcopy(base);s['sources'].pop(ref);run(label+'-missing-original-bytes',s,'FAIL','SOURCE_INPUT_SET_MISMATCH')
    s=copy.deepcopy(base);mutate(s,'context',lambda v:v['selectedSourceInputs'].pop(index));repin_context(s);run(label+'-missing-independent-mapping',s,'FAIL','SOURCE_INPUT_SELECTION_MISMATCH')
    s=copy.deepcopy(base);mutate(s,'content',lambda v:v['sourceInputs'].append(copy.deepcopy(v['sourceInputs'][index])));rebind_content(s);run(label+'-duplicate-ref',s,'FAIL','SOURCE_INPUT_SET_MISMATCH')
    if selector_mode=='digest':
     s=copy.deepcopy(base);changed=copy.deepcopy(entry['binding']);changed['digest']='sha256:'+'1'*64
     mutate(s,'content',lambda v:v['sourceInputs'][index].update(binding=changed));replace_submitted_selector(s,entry['binding'],changed);rebind_content(s);run(label+'-wrong-binding-digest',s,'FAIL','SOURCE_BINDING_DIGEST_MISMATCH')
    else:
     s=copy.deepcopy(base);changed={'ref':ref,'revisionRef':'fixture:other-revision'};mutate(s,'content',lambda v:v['sourceInputs'][index].update(binding=changed));replace_submitted_selector(s,entry['binding'],changed);rebind_content(s,select_sources=False);run(label+'-unselected-revision',s,'FAIL','SOURCE_INPUT_SELECTION_MISMATCH')
     s=copy.deepcopy(base);changed={'ref':ref,'digest':entry['valueDigest']};mutate(s,'content',lambda v:v['sourceInputs'][index].update(binding=changed));rebind_content(s)
     if entry['role']=='MEASUREMENT_EVIDENCE':run(label+'-silently-translated-selector',s,'FAIL','SOURCE_NOT_IN_SUBMITTED_EVIDENCE')
     elif val(base,'intent').get('associatedSemanticEventBinding')==entry['binding']:run(label+'-silently-translated-selector',s,'FAIL','ASSOCIATED_EVENT_BYTES_MISSING')
     for later_key,later_field in [('act','recordId'),('context','contextId'),('content','contentId'),('policy','policyId')]:
      s=copy.deepcopy(base);changed={'ref':ref,'revisionRef':val(s,later_key)[later_field]};mutate(s,'content',lambda v:v['sourceInputs'][index].update(binding=changed));replace_submitted_selector(s,entry['binding'],changed);rebind_content(s);run(label+'-revision-alias-'+later_key,s,'FAIL','SELF_OR_LATER_IDENTITY_ALIAS')
 # Every typed carrier also has preserved revision and mixed-selector positives.
 # Future carrier support is selected by an exact versioned profile, not a body whitelist.
 for spec in [x for x in specs if x['id'].endswith('-typed')]:
  s=load(spec);mutate(s,'rendered',lambda v:v['assertionBody']['proposition'].update(form='ALL'));run(spec['id']+'-typed-content-changed',s,'FAIL','COMPLETE_CONTENT_MISMATCH')
  s=load(spec);ref=next(iter(s['bundle']));s['bundle'][ref]+=b' ';run(spec['id']+'-schema-bytes-changed',s,'INPUT_ERROR','PROFILE_SCHEMA_PIN_MISMATCH')
  s=load(spec);s['bundle'].pop(next(iter(s['bundle'])));run(spec['id']+'-schema-closure-missing',s,'INPUT_ERROR','PROFILE_SCHEMA_SET_MISMATCH')
  s=load(spec);profile=json.loads(s['profile']);profile['claimLanguageRevision']=None;s['profile']=raw(profile);s['pins']['intentProfileSha256']=sha(s['profile']);run(spec['id']+'-wrong-language-profile',s,'FAIL','CLAIM_LANGUAGE_PROFILE_MISMATCH')
 s=copy.deepcopy(bases[0]);s['profile']=None;run('missing-intent-profile',s,'INPUT_ERROR','MISSING_OR_NONBYTE_INPUT',persist=False)
 s=copy.deepcopy(bases[0]);s['profile']+=b' ';run('unselected-profile-bytes',s,'FAIL','INTENT_PROFILE_PIN_MISMATCH')
 # Online forbids the offline field; offline requires the exact independently selected binding.
 s=copy.deepcopy(bases[0]);mutate(s,'intent',lambda v:v.update(assertionActEvidenceBinding=s['selection']['binding']));run('online-has-offline-binding',s,'FAIL','SCHEMA_INVALID')
 s=copy.deepcopy(bases[1]);mutate(s,'intent',lambda v:v.pop('assertionActEvidenceBinding'));run('offline-missing-binding',s,'FAIL','SCHEMA_INVALID')
 s=copy.deepcopy(bases[1]);mutate(s,'intent',lambda v:v['assertionActEvidenceBinding'].update(digest='sha256:'+'0'*64));run('offline-wrong-binding',s,'FAIL','OFFLINE_ACT_BINDING_MISMATCH')
 # Explicit fictional revision-to-byte mapping, selected independently after act finalization.
 s=copy.deepcopy(bases[1]);selection=copy.deepcopy(s['selection']);selection['binding']={'ref':selection['binding']['ref'],'revisionRef':'fixture:act-revision:r1'};s['selection']=selection
 mutate(s,'intent',lambda v:v.update(assertionActEvidenceBinding=selection['binding']))
 mutate(s,'context',lambda v:v.update(actSelection=selection,intentBytesSha256=sha(s['raws']['intent']),intentDigest=dg(val(s,'intent'))));repin_context(s);run('offline-independent-revision-selection',s,PASS)
 s=copy.deepcopy(s);s['selection']['binding']['revisionRef']='fixture:mutable:latest';run('offline-revision-alias-changed',s,'FAIL','ACT_SELECTION_CONTEXT_MISMATCH')
 # Selected invalid package paths remain structured failures, with no remote retrieval.
 pkg=out/'disposable-package';pkg.mkdir(exist_ok=True)
 for d in ['schemas','source-contracts','sources']:shutil.copytree(C/d,pkg/d,dirs_exist_ok=True)
 shutil.copy2(C/'contract.json',pkg/'contract.json')
 def bad_package(name,edit,code,status='INPUT_ERROR'):
  path=pkg/'schemas/act.schema.json';original=path.read_bytes();original_contract=(pkg/'contract.json').read_bytes();v=json.loads(original);edit(v);path.write_bytes(raw(v));c=json.loads(original_contract);c['schemas']['act']['sha256']=sha(path.read_bytes());c.pop('contractDigest');c['contractDigest']=dg(c);(pkg/'contract.json').write_bytes(raw(c));s=copy.deepcopy(bases[0]);s['pins']['contractSha256']=sha((pkg/'contract.json').read_bytes());run(name,s,status,code,package=pkg,persist=False);path.write_bytes(original);(pkg/'contract.json').write_bytes(original_contract)
 bad_package('malformed-selected-schema',lambda v:v.update(type=23),'PACKAGE_UNAVAILABLE_OR_INVALID','DEPENDENCY_UNAVAILABLE')
 bad_package('unregistered-remote-reference',lambda v:v.update(**{'$ref':'https://untrusted.invalid/schema'}),'UNPINNED_SCHEMA_REFERENCE')
 bad_package('unresolved-local-reference',lambda v:v.update(**{'$ref':'#/missing'}),'UNPINNED_SCHEMA_REFERENCE')
 run('missing-package',bases[0],'DEPENDENCY_UNAVAILABLE','PACKAGE_UNAVAILABLE_OR_INVALID',package=out/'absent',persist=False)
 def assertion(name,ok):records.append({'id':name,'pass':bool(ok)})
 assertion('frozen-report-schema',REPORT_SCHEMA==rd(C/'schemas/report.schema.json'))
 for pin in rd(C/'source-pins.json')['sources']:
  where=F if pin['copy'].startswith('fixtures/') else C
  assertion('source-byte-pin-'+pin['copy'],sha((where/pin['copy']).read_bytes())==pin['sha256'])
 # Direct helper checks separate syntax acceptance from binding failures above.
 for text,valid in [('2026-05-08T08:20:00+01:30',True),('2026-05-08T08:20:00-01:30',True),('2026-05-08T08:20:00+23:59',True),('2026-05-08T08:20:00+01:99',False),('2026-05-08T08:20:00-01:60',False),('2026-05-08T08:20:00+24:00',False)]:
  assertion('offset-helper-'+text,act_common.date_time(text)==valid)
 for text,valid in [('2026-05-08T24:00:00+01:30',False),('2026-05-08T23:60:00Z',False),('2026-05-08T23:59:60Z',False),('２０２６-05-08T00:00:00Z',False),('2026-05-08T00:00:00.١Z',False),('2026-05-08T00:00:00+٠١:00',False),('2026-05-08T23:59:59.123456789Z',True)]:
  assertion('explicit-component-range-'+text,act_common.date_time(text)==valid)
 original=act_common.version;act_common.version=lambda name:'0.0.0'
 try:run('unsupported-jcs-version',bases[0],'DEPENDENCY_UNAVAILABLE','DEPENDENCY_UNAVAILABLE',persist=False)
 finally:act_common.version=original
 # CLI uses explicit package and input roots; code lives in a separate directory.
 code_dir=out/'portable-checker';code_dir.mkdir(exist_ok=True)
 for f in ['verify_assertion_act.py','act_common.py','act_report_contract.py']:shutil.copy2(P/f,code_dir/f)
 spec=specs[0];write(out/'schema-bundle.json',{k:str(F/v) for k,v in spec['schemaBundle'].items()});write(out/'selection.json',spec['expectedActSelection']);write(out/'source-inputs.json',{x['ref']:str(F/x['path']) for x in spec['sourceInputs']})
 cmd=[sys.executable,'-B',str(code_dir/'verify_assertion_act.py'),'--package-root',str(C),'--selection',str(out/'selection.json'),'--source-inputs',str(out/'source-inputs.json'),'--schema-bundle',str(out/'schema-bundle.json'),'--intent-profile',str(F/spec['paths']['intentProfile']),'--trusted-intent-profile-sha256',spec['trustedPins']['intentProfileSha256']]
 for k in KEYS:cmd+=['--'+k,str(F/spec['paths'][k])]
 for k in ['contract','context','policy']:cmd+=['--trusted-'+k+'-sha256',spec['trustedPins'][k+'Sha256']]
 if a.dependency_dir:cmd+=['--dependency-dir',str(a.dependency_dir.resolve())]
 env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}
 for name,extra,status,exitcode in [('portable-split-cli',[],PASS,0),('portable-missing-act',['--act',str(out/'no-act')],'INPUT_ERROR',2)]:
  proc=subprocess.run(cmd+extra,cwd=out,env=env,capture_output=True,text=True);r=json.loads(proc.stdout);assertion(name,proc.returncode==exitcode and r['status']==status and not list(validator.iter_errors(r)));write(out/'reports'/('cli-'+name+'.json'),r)
 no_deps=[cmd[0],'-S','-B',*cmd[2:]]
 if '--dependency-dir' in no_deps:
  i=no_deps.index('--dependency-dir');del no_deps[i:i+2]
 proc=subprocess.run(no_deps,cwd=out,env=env,capture_output=True,text=True);r=json.loads(proc.stdout);assertion('portable-missing-dependency',proc.returncode==3 and r['status']=='DEPENDENCY_UNAVAILABLE' and not list(validator.iter_errors(r)))
 shutil.rmtree(pkg);shutil.rmtree(code_dir)
 write(out/'case-catalog.json',{'cases':catalog,'meaning':'Fictional conditional comparisons. The runner authors expectations; no saved report is an oracle.'})
 result={'status':'PASS' if all(x['pass'] for x in records) else 'FAIL','checks':len(records),'passed':sum(x['pass'] for x in records),'failed':[x for x in records if not x['pass']],'runtimeAdmission':'NOT_ESTABLISHED','authorizationSelectedPathSourceContract':'UNIDENTIFIED','results':records}
 write(out/'conformance-report.json',result);print(json.dumps({k:v for k,v in result.items() if k!='results'}));print('Next: independent review of the act boundary and its explicit authorization-source gap.')
 return 0 if result['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
