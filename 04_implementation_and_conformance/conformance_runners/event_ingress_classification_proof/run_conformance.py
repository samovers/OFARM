"""Portable owner-contract checks. Expectations are authored, not read from reports.

No network, Git, runtime resolver or deployed producer. All temporary files stay
below --output-dir; omit it for an ephemeral directory inside this package.
"""
from pathlib import Path
import argparse,copy,hashlib,importlib,json,os,shutil,subprocess,sys,tempfile

P=Path(__file__).resolve().parent
KEYS=['proof','envelope','request','context','profile']
PASS='CONDITIONAL_CONFORMANCE_PASS'
# These sentences/families are authored against grammar sections 3.1–3.7 and 4.
# No family is taken from an incoming envelope or derived from a commit class.
FAMILY_CASES=[
 ('StructureEvent','A field boundary configuration is changed.','3.1; 4'),
 ('ObservationEvent','A soil measurement is observed and recorded.','3.2; 4'),
 ('OccurrenceEvent','A frost incident occurs without deliberate intervention.','3.3; 4'),
 ('InterventionEvent','Deliberate pruning changes canopy structure.','3.4; 4'),
 ('MaterialEvent','A lot is split into two identified lots.','3.5; 4'),
 ('EvidenceEvent','A receipt scan is captured as evidence.','3.6; 4'),
 ('GovernanceEvent','A formal review rejection is recorded.','3.7; 4')]
CLASSES=['NOTE','OBSERVATION_ASSERTION','HYPOTHESIS_ASSERTION','STRUCTURE_ASSERTION','OPERATION_CLAIM','EVIDENCE_RECORD','COMPLIANCE_ASSERTION','GOVERNANCE_DECISION','ADVISORY_OUTPUT']
def raw(v):return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode()
def sha(v):return hashlib.sha256(v).hexdigest()
def get(path):return json.loads((P/path).read_bytes())
def write(path,value):path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw(value))

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--dependency-dir',type=Path);ap.add_argument('--output-dir',type=Path);ap.add_argument('--package-root',type=Path,default=P);ap.add_argument('--fixture-root',type=Path,default=P);ap.add_argument('--source-root',type=Path);args=ap.parse_args()
 C=args.package_root.resolve();F=args.fixture_root.resolve();S=(args.source_root or C).resolve()
 def get(path):return json.loads(((F if path.startswith('fixtures/') or path=='classification-profile.json' else C)/path).read_bytes())
 if args.dependency_dir:sys.path.insert(0,str(args.dependency_dir.resolve()))
 import rfc8785
 from jsonschema import Draft202012Validator
 import verify_event_proof as checker
 from report_contract import REPORT_SCHEMA
 def dg(v):return 'sha256:'+sha(rfc8785.dumps(v))
 temp=None
 if args.output_dir:out=args.output_dir.resolve();out.mkdir(parents=True,exist_ok=True)
 else:temp=tempfile.TemporaryDirectory(prefix='.conformance-',dir=P);out=Path(temp.name)
 records=[];catalog=[]
 report_validator=Draft202012Validator(get('schemas/report.schema.json'))
 fixture_specs=get('fixtures/positive-cases.json')['cases']
 def load(spec):return {'raws':{k:(F/spec[k]).read_bytes() for k in KEYS},'pins':copy.deepcopy(spec['trustedPins']),'selector':copy.deepcopy(spec['expectedProofBinding']),'mode':'INITIAL_EVALUATION'}
 base=load(fixture_specs[0])
 def val(s,k):return json.loads(s['raws'][k])
 def put(s,k,v):s['raws'][k]=raw(v)
 def mutate(s,k,fn):v=val(s,k);fn(v);put(s,k,v)
 def selector(s):v=val(s,'proof');s['selector']={'ref':v['proofId'],'digest':dg(v)}
 def rebind(s,*,profile=False,context=True):
  """Explicit alternate independent test selection, never used for attack pins."""
  pr=val(s,'profile');e=val(s,'envelope');q=val(s,'request');c=val(s,'context');p=val(s,'proof')
  bindings={'classificationProfileBinding':{'ref':pr['profileId'],'digest':dg(pr)},'envelopeBinding':{'ref':e['semanticEventId'],'digest':dg(e)},'ingressRequestBinding':{'ref':q['requestId'],'digest':dg(q)},'envelopeBytesSha256':sha(s['raws']['envelope']),'ingressRequestBytesSha256':sha(s['raws']['request'])}
  c.update(bindings);p.update(bindings);put(s,'context',c)
  p['ownerContextBinding']={'ref':c['contextId'],'digest':dg(c)};put(s,'proof',p);selector(s)
  if profile:s['pins']['profileSha256']=sha(s['raws']['profile'])
  if context:s['pins']['contextSha256']=sha(s['raws']['context'])
 def run(name,s,expected,code=None,package=C,*,persist=True,family=None):
  kw={'trusted_pins':s['pins'],'expected_proof_binding':s['selector'],'use_mode':s['mode'],'package_root':package,'source_root':S if package==C else package}
  r=checker.verify(*(s['raws'][k] for k in KEYS),**kw)
  r2=checker.verify(*(s['raws'][k] for k in KEYS),**kw)
  errs=list(report_validator.iter_errors(r));codes=[e['code'] for e in r['errors']]
  passed=r['status']==expected and (code is None or code in codes) and not errs and r==r2 and r['runtimeAdmission']=='NOT_ESTABLISHED' and (expected!=PASS or r['checkedRules']==get('contract.json')['requiredRules'] or set(r['checkedRules'])==set(get('contract.json')['requiredRules'])) and (family is None or r['classification']['authoritativePrimaryFamily']==family)
  records.append({'id':name,'pass':passed,'expectedStatus':expected,'actualStatus':r['status'],'requiredErrorCode':code,'errorCodes':codes,'reportSchemaValid':not errs,'deterministic':r==r2,'runtimeAdmission':r['runtimeAdmission']})
  if persist:
   entry={'id':name,'expectedStatus':expected,'requiredErrorCode':code,'trustedPins':s['pins'],'expectedProofBinding':s['selector'],'useMode':s['mode'],'inputs':{},'report':'reports/'+name+'.json'}
   for k,v in s['raws'].items():
    if isinstance(v,bytes):
     path='cases/'+name+'/'+k+'.json';(out/path).parent.mkdir(parents=True,exist_ok=True);(out/path).write_bytes(v);entry['inputs'][k]={'path':path,'sha256':sha(v)}
    else:entry['inputs'][k]={'apiValue':v}
   catalog.append(entry);write(out/entry['report'],r)
  if not passed:print('FAIL',name,r['status'],codes,[e.message for e in errs])
  return r
 def attack(name,key,fn,code,*,refresh=False,expected='FAIL'):
  s=copy.deepcopy(base);mutate(s,key,fn)
  if refresh:selector(s)
  return run(name,s,expected,code)
 for spec in fixture_specs:
  s=load(spec);run(spec['id'],s,PASS,family='InterventionEvent')
  s['mode']='EXACT_REEVALUATION';allowed=spec['id']!='pruning-no-reuse'
  run(spec['id']+'-reevaluation',s,PASS if allowed else 'FAIL',None if allowed else 'REUSE_NOT_ALLOWED')
 # Exact selected source bytes: whitespace changes have unchanged JCS but fail raw pins.
 for k in KEYS:
  s=copy.deepcopy(base);s['raws'][k]+=b' '
  if k=='proof':run('proof-whitespace-same-immutable-value',s,PASS)
  else:run(k+'-whitespace',s,'FAIL',{'envelope':'SOURCE_BYTES_MISMATCH','request':'SOURCE_BYTES_MISMATCH','context':'CONTEXT_PIN_MISMATCH','profile':'PROFILE_PIN_MISMATCH'}[k])
 for k in KEYS:
  for suffix,payload,code,status in [('missing',None,'MISSING_OR_NONBYTE_INPUT','INPUT_ERROR'),('duplicate',b'{"a":1,"a":2}','DUPLICATE_JSON_NAME','INPUT_ERROR'),('deep',b'['*1100+b'0'+b']'*1100,'INPUT_DEPTH_LIMIT','INPUT_ERROR'),('bad-utf8',b'\xff','INVALID_UTF8_JSON','INPUT_ERROR'),('nan',b'{"x":NaN}','NON_JSON_NUMBER','INPUT_ERROR'),('unsafe-integer',b'{"x":9007199254740992}','NON_CANONICAL_VALUE','INPUT_ERROR'),('wrong-type',b'[]','SCHEMA_INVALID','FAIL')]:
   s=copy.deepcopy(base);s['raws'][k]=payload;run(k+'-'+suffix,s,status,code)
 s=copy.deepcopy(base);s['raws']['proof']=b' '* (2*1024*1024+1);run('oversized-input',s,'INPUT_ERROR','INPUT_SIZE_LIMIT',persist=False)
 attack('wrong-family-proof','proof',lambda v:v['classification'].update(authoritativePrimaryFamily='ObservationEvent'),'CLASSIFICATION_MISMATCH',refresh=True)
 attack('wrong-family-envelope','envelope',lambda v:v.update(primaryEventFamily='ObservationEvent'),'FAMILY_MISMATCH')
 attack('dominant-shortened','proof',lambda v:v['classification'].update(dominantSemanticConsequence='pruning'),'CLASSIFICATION_MISMATCH',refresh=True)
 attack('dominant-envelope-same-id','envelope',lambda v:v.update(dominantSemanticConsequence='No deliberate pruning happened.'),'CLASSIFICATION_CASE_NOT_EXACT')
 attack('subtype-removed','envelope',lambda v:v.pop('eventSubtypeId'),'CLASSIFICATION_MISMATCH')
 attack('subtype-null','envelope',lambda v:v.update(eventSubtypeId=None),'SCHEMA_INVALID')
 attack('subtype-case-change','envelope',lambda v:v.update(eventSubtypeId='Intervention/pruning-action'),'CLASSIFICATION_CASE_NOT_EXACT')
 attack('subtype-as-commit-class','proof',lambda v:v['classification'].update(commitClass='intervention/pruning-action'),'SCHEMA_INVALID')
 attack('wrong-commit-class','request',lambda v:v.update(commitClass='NOTE'),'COMMIT_CLASS_MISMATCH')
 attack('changed-request-same-id','request',lambda v:v.update(idempotencyKey='other:attempt'),'INPUT_BINDING_MISMATCH')
 attack('changed-request-event','request',lambda v:v.update(semanticEventRef='event:other'),'REQUEST_EVENT_MISMATCH')
 attack('changed-request-scope','request',lambda v:v['targetScopes'][0].update(scopeRef='field:99'),'REQUEST_SCOPE_MISMATCH')
 # Review repair R1: RFC3339 offset hours/minutes, on every admitted timestamp field.
 timestamp_targets=[('request','ingestedAt')]+[('envelope',field) for field in ['observationTime','eventTime','assertionTime','recordTime','effectiveFrom','effectiveUntil','decisionTime']]
 for document,field in timestamp_targets:
  for offset in ['+00:00','-00:00','+01:30','-01:30','+23:59','-23:59','+01:60','+01:99','-01:60','-01:99','+24:00','-24:00','+99:00','-99:00']:
   valid=offset in ['+00:00','-00:00','+01:30','-01:30','+23:59','-23:59']
   s=copy.deepcopy(base)
   if document=='request':mutate(s,document,lambda v:v.update({field:'2026-05-08T08:20:00'+offset}))
   else:mutate(s,document,lambda v:v['timeSemantics'].update({field:'2026-05-08T08:20:00'+offset}))
   rebind(s)
   run('r1-offset-'+document+'-'+field+'-'+offset.replace('+','plus').replace('-','minus').replace(':','-'),s,PASS if valid else 'FAIL',None if valid else 'SCHEMA_INVALID')
 # Review repair R2: every numeric component is ASCII and range checked before parsing.
 boundary_times=[('2026-05-08T00:00:00Z',True),('2026-05-08T23:59:59+01:30',True),('2026-05-08t23:59:59.123456789z',True),('2026-05-08T24:00:00+01:30',False),('2026-05-08T24:00:00Z',False),('2026-05-08T99:00:00Z',False),('2026-05-08T23:60:00Z',False),('2026-05-08T23:99:00Z',False),('2026-05-08T23:59:60Z',False),('2026-05-08T23:59:99Z',False),('2026-00-08T00:00:00Z',False),('2026-13-08T00:00:00Z',False),('2026-05-00T00:00:00Z',False),('2026-05-32T00:00:00Z',False),('2026-02-30T00:00:00Z',False),('２０２６-05-08T00:00:00Z',False),('2026-05-08T00:٠١:00Z',False),('2026-05-08T00:00:00.١Z',False),('2026-05-08T00:00:00+٠١:00',False)]
 for document,field in timestamp_targets:
  for number,(stamp,valid) in enumerate(boundary_times):
   s=copy.deepcopy(base)
   if document=='request':mutate(s,document,lambda v:v.update({field:stamp}))
   else:mutate(s,document,lambda v:v['timeSemantics'].update({field:stamp}))
   rebind(s);run('r2-time-'+document+'-'+field+'-'+str(number),s,PASS if valid else 'FAIL',None if valid else 'SCHEMA_INVALID')
 attack('bad-calendar','request',lambda v:v.update(ingestedAt='2026-02-30T00:00:00Z'),'SCHEMA_INVALID')
 attack('bad-calendar-envelope','envelope',lambda v:v['timeSemantics'].update(recordTime='2026-13-01T00:00:00Z'),'SCHEMA_INVALID')
 attack('forged-owner-role','proof',lambda v:v.update(ownerRole='COMMIT_ADMISSION'),'SCHEMA_INVALID')
 attack('forged-admitted-boolean','proof',lambda v:v.update(admitted=True),'SCHEMA_INVALID')
 for field in ['domainVerdictBinding','traceBinding','finalAssertionEffect','attemptReceiptBinding','ingressResultBinding']:
  attack('late-'+field,'proof',lambda v,f=field:v.update({f:{'ref':'late:result','digest':'sha256:'+'0'*64}}),'SCHEMA_INVALID')
 attack('wrong-production-mode','proof',lambda v:v.update(productionMode='VALIDATION_PHASE_PROOF'),'PRODUCTION_MODE_MISMATCH',refresh=True)
 attack('wrong-completion-milestone','proof',lambda v:v.update(completionMilestone='AFTER_VERDICT'),'SCHEMA_INVALID')
 attack('missing-required-binding','proof',lambda v:v.pop('ownerContextBinding'),'SCHEMA_INVALID')
 attack('wrong-context-binding','proof',lambda v:v['ownerContextBinding'].update(digest='sha256:'+'0'*64),'OWNER_CONTEXT_BINDING_MISMATCH',refresh=True)
 attack('wrong-contract-binding','proof',lambda v:v['contractBinding'].update(digest='sha256:'+'0'*64),'CONTRACT_BINDING_MISMATCH',refresh=True)
 attack('wrong-proof-id','proof',lambda v:v.update(proofId='proof:other'),'OWNER_PROOF_ID_MISMATCH',refresh=True)
 attack('proof-mutated-original-selector','proof',lambda v:v['classification'].update(authoritativePrimaryFamily='MaterialEvent'),'PROOF_SELECTOR_MISMATCH')
 for key in ['contextSha256','profileSha256','contractSha256']:
  s=copy.deepcopy(base);s['pins'][key]='0'*64;run('wrong-'+key,s,'INPUT_ERROR' if key=='contractSha256' else 'FAIL',{'contextSha256':'CONTEXT_PIN_MISMATCH','profileSha256':'PROFILE_PIN_MISMATCH','contractSha256':'CONTRACT_PIN_MISMATCH'}[key])
 for name,pins in [('missing-pins',{}),('boolean-pins',True),('pin-extra-field',{**base['pins'],'admitted':True})]:
  s=copy.deepcopy(base);s['pins']=pins;run(name,s,'INPUT_ERROR','INVALID_INDEPENDENT_PINS')
 for name,select in [('selector-missing',{}),('selector-invalid-digest',{'ref':'proof:x','digest':'sha256:wrong'}),('selector-boolean',True)]:
  s=copy.deepcopy(base);s['selector']=select;run(name,s,'INPUT_ERROR','INVALID_PROOF_SELECTOR')
 s=copy.deepcopy(base);s['mode']='COMMIT_REPLAY';run('unsupported-reuse',s,'INPUT_ERROR','UNKNOWN_USE_MODE')
 # Forgers can recompute their own proof hashes but cannot replace selected roots.
 s=copy.deepcopy(base)
 mutate(s,'envelope',lambda v:v.update(primaryEventFamily='EvidenceEvent'))
 mutate(s,'proof',lambda v:v['classification'].update(authoritativePrimaryFamily='EvidenceEvent'))
 mutate(s,'profile',lambda v:v['cases'][0].update(authoritativePrimaryFamily='EvidenceEvent'))
 rebind(s,context=False);run('self-consistent-forgery-fixed-owner-pins',s,'FAIL','PROFILE_PIN_MISMATCH')
 s=copy.deepcopy(base);mutate(s,'request',lambda v:v.update(commitClass='NOTE'));mutate(s,'proof',lambda v:v['classification'].update(commitClass='NOTE'));selector(s)
 run('self-consistent-commit-forgery-fixed-context',s,'FAIL','COMMIT_CLASS_MISMATCH')
 # Alternate trusted roots here are explicit test setups, not attack repinning.
 for name,edit,code in [
  ('duplicate-owner-case-id',lambda v:v['cases'][1].update(caseId=v['cases'][0]['caseId']),'AMBIGUOUS_CLASSIFICATION_PROFILE'),
  ('duplicate-owner-case-signature',lambda v:v['cases'].append({**copy.deepcopy(v['cases'][0]),'caseId':'case:second'}),'AMBIGUOUS_CLASSIFICATION_PROFILE'),
  ('owner-source-pin-mismatch',lambda v:v['cases'][0]['semanticSourceBinding'].update(digest='sha256:'+'0'*64),'CLASSIFICATION_SOURCE_MISMATCH'),
  ('no-owner-case',lambda v:v.update(cases=v['cases'][1:]),'CLASSIFICATION_CASE_NOT_EXACT')]:
  s=copy.deepcopy(base);mutate(s,'profile',edit);rebind(s,profile=True);run(name,s,'FAIL',code)
 s=copy.deepcopy(base);mutate(s,'context',lambda v:v.update(selectedCaseId='case:spot-spray-late-sync'));rebind(s);run('wrong-independent-case-selection',s,'FAIL','OWNER_CASE_SELECTION_MISMATCH')
 s=copy.deepcopy(base);mutate(s,'context',lambda v:v.update(permittedUseModes=['EXACT_REEVALUATION']));rebind(s);run('reevaluation-without-initial-context',s,'FAIL','SCHEMA_INVALID')
 s=copy.deepcopy(base);mutate(s,'context',lambda v:v['inputRoles'].append('LATE_VERDICT'));rebind(s);run('late-input-owner-context',s,'FAIL','SCHEMA_INVALID')
 s=copy.deepcopy(base);mutate(s,'context',lambda v:v.update(contextId='context:another'));s['pins']['contextSha256']=sha(s['raws']['context']);run('proof-reused-another-context',s,'FAIL','OWNER_CONTEXT_BINDING_MISMATCH')
 # All seven families and nine classes remain supported, with no coupling table.
 all_profile=val(base,'profile');all_profile['profileId']='fixture:profile:all-families';all_profile['cases']=[]
 gb=copy.deepcopy(val(base,'profile')['cases'][0]['semanticSourceBinding'])
 for family,text,clause in FAMILY_CASES:
  all_profile['cases'].append({'caseId':'fixture:case:'+family,'dominantSemanticConsequence':text,'subtype':{'presence':'ABSENT'},'authoritativePrimaryFamily':family,'semanticSourceBinding':gb,'sourceClause':clause,'classificationReason':'Fictional owner classification of the exact description using the cited existing family definition.'})
 for family,text,clause in FAMILY_CASES:
  for commit in CLASSES:
   s=copy.deepcopy(base);put(s,'profile',all_profile)
   mutate(s,'envelope',lambda v:v.update(primaryEventFamily=family,dominantSemanticConsequence=text))
   mutate(s,'envelope',lambda v:v.pop('eventSubtypeId'))
   mutate(s,'request',lambda v:v.update(commitClass=commit))
   mutate(s,'context',lambda v:v.update(selectedCaseId='fixture:case:'+family,expectedCommitClass=commit))
   mutate(s,'proof',lambda v:v.update(classification={'caseId':'fixture:case:'+family,'authoritativePrimaryFamily':family,'commitClass':commit,'dominantSemanticConsequence':text,'subtype':{'presence':'ABSENT'}}))
   rebind(s,profile=True);run('support-'+family+'-'+commit,s,PASS,family=family)
  # A self-consistent envelope/proof family swap must still fail owner comparison.
  wrong='EvidenceEvent' if family!='EvidenceEvent' else 'MaterialEvent'
  mutate(s,'envelope',lambda v:v.update(primaryEventFamily=wrong));mutate(s,'proof',lambda v:v['classification'].update(authoritativePrimaryFamily=wrong));rebind(s)
  run('owner-authority-'+family,s,'FAIL','FAMILY_MISMATCH')
 # Malformed package cases are explicitly repinned to reach dependency validation.
 pkg=out/'disposable-package';pkg.mkdir(exist_ok=True)
 for d in ['schemas','source-contracts','sources']:shutil.copytree((S if d=='sources' else C)/d,pkg/d,dirs_exist_ok=True)
 shutil.copy2(C/'contract.json',pkg/'contract.json')
 def package_case(name,path,payload,code,*,repin=False,expected='DEPENDENCY_UNAVAILABLE'):
  original=(pkg/path).read_bytes();original_contract=(pkg/'contract.json').read_bytes();s=copy.deepcopy(base)
  (pkg/path).write_bytes(payload)
  if repin:
   c=json.loads(original_contract)
   if path!='contract.json':
    for item in c['schemas'].values():
     if item['path']==path:item['sha256']=sha(payload)
   else:c=json.loads(payload)
   c.pop('contractDigest',None);c['contractDigest']=dg(c);(pkg/'contract.json').write_bytes(raw(c));s['pins']['contractSha256']=sha((pkg/'contract.json').read_bytes())
  run(name,s,expected,code,package=pkg,persist=False)
  (pkg/path).write_bytes(original);(pkg/'contract.json').write_bytes(original_contract)
 sch=get('schemas/proof.schema.json');sch['type']=23
 package_case('invalid-pinned-schema','schemas/proof.schema.json',raw(sch),'PACKAGE_UNAVAILABLE_OR_INVALID',repin=True)
 sch=get('schemas/proof.schema.json');sch['$ref']='https://untrusted.invalid/schema'
 package_case('external-schema-reference','schemas/proof.schema.json',raw(sch),'SCHEMA_ID_OR_REFERENCE_MISMATCH',repin=True,expected='INPUT_ERROR')
 sch=get('schemas/proof.schema.json');sch['$ref']='#/missing'
 package_case('unexpected-local-reference','schemas/proof.schema.json',raw(sch),'SCHEMA_ID_OR_REFERENCE_MISMATCH',repin=True,expected='INPUT_ERROR')
 package_case('schema-bytes-changed','schemas/proof.schema.json',(C/'schemas/proof.schema.json').read_bytes()+b' ','SCHEMA_PIN_MISMATCH',expected='INPUT_ERROR')
 package_case('semantic-source-changed','sources/event-grammar.md',b'changed','SEMANTIC_SOURCE_PIN_MISMATCH',expected='INPUT_ERROR')
 c=get('contract.json');c['semanticSources']=c['semanticSources'][:1]
 package_case('incomplete-semantic-source-closure','contract.json',raw(c),'SEMANTIC_SOURCE_CLOSURE_MISMATCH',repin=True,expected='INPUT_ERROR')
 package_case('deep-contract','contract.json',b'['*1100+b'0'+b']'*1100,'CONTRACT_PIN_MISMATCH',expected='INPUT_ERROR')
 s=copy.deepcopy(base);run('missing-package',s,'DEPENDENCY_UNAVAILABLE','PACKAGE_UNAVAILABLE_OR_INVALID',package=out/'absent',persist=False)
 # A pinned deeply nested contract is rejected before recursive schema walking.
 original_contract=(pkg/'contract.json').read_bytes();deep=b'['*1100+b'0'+b']'*1100
 (pkg/'contract.json').write_bytes(deep);s=copy.deepcopy(base);s['pins']['contractSha256']=sha(deep)
 run('deep-pinned-contract',s,'DEPENDENCY_UNAVAILABLE','PACKAGE_UNAVAILABLE_OR_INVALID',package=pkg,persist=False)
 (pkg/'contract.json').write_bytes(original_contract)
 # Frozen fallback schema and source copies are checked independently of verifier.
 def assertion(name,ok):records.append({'id':name,'pass':bool(ok)})
 assertion('frozen-report-schema-exact',REPORT_SCHEMA==get('schemas/report.schema.json'))
 for pin in get('source-pins.json')['sources'] if 'sources' in get('source-pins.json') else get('source-pins.json')['sourcePins']:
  assertion('source-copy-'+pin['copy'],sha(((F if pin['copy'].startswith('fixtures/') else S if pin['copy'].startswith('sources/') else C)/pin['copy']).read_bytes())==pin['sha256'])
 # Independent JCS vectors: property ordering, escaping, float boundaries, rejection.
 vectors=[({'\ue000':2,'\U00010000':3},b'{"\xf0\x90\x80\x80":3,"\xee\x80\x80":2}'),([-0.0,1e-7,1e-6,1e20,1e21],b'[0,1e-7,0.000001,100000000000000000000,1e+21]'),({'x':'\n\t"\\'},b'{"x":"\\n\\t\\"\\\\"}')]
 for i,(v,want) in enumerate(vectors):assertion('jcs-vector-'+str(i),rfc8785.dumps(v)==want)
 for i,v in enumerate([float('nan'),float('inf'),9007199254740992,'\ud800']):
  try:rfc8785.dumps(v);ok=False
  except (ValueError,UnicodeError):ok=True
  assertion('jcs-invalid-'+str(i),ok)
 # CLI runs from a relocated copy and unrelated working directory. No local paths in code.
 portable=out/'portable-package';portable.mkdir(exist_ok=True)
 for f in ['verify_event_proof.py','report_contract.py']:shutil.copy2(P/f,portable/f)
 shutil.copy2(C/'contract.json',portable/'contract.json')
 for d in ['schemas','source-contracts','sources']:shutil.copytree((S if d=='sources' else C)/d,portable/d,dirs_exist_ok=True)
 shutil.copytree(F/'fixtures',portable/'fixtures',dirs_exist_ok=True)
 shutil.copy2(F/'classification-profile.json',portable/'classification-profile.json')
 spec=fixture_specs[0]
 cmd=[sys.executable,'-B',str(portable/'verify_event_proof.py')]
 for k in KEYS:cmd+=['--'+k,str(portable/spec[k])]
 for k in ['contract','context','profile']:cmd+=['--trusted-'+k+'-sha256',spec['trustedPins'][k+'Sha256']]
 cmd+=['--expected-proof-ref',spec['expectedProofBinding']['ref'],'--expected-proof-digest',spec['expectedProofBinding']['digest']]
 if args.dependency_dir:cmd+=['--dependency-dir',str(args.dependency_dir.resolve())]
 env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}
 for name,extra,want,exitcode in [('portable-cli',[],PASS,0),('portable-cli-bad-use',['--use-mode','REPLAY'],'INPUT_ERROR',2),('portable-cli-missing',['--proof',str(out/'missing-proof')],'INPUT_ERROR',2)]:
  proc=subprocess.run(cmd+extra,cwd=out,env=env,capture_output=True,text=True);r=json.loads(proc.stdout)
  assertion(name,proc.returncode==exitcode and r['status']==want and not list(report_validator.iter_errors(r)));write(out/'reports'/('cli-'+name+'.json'),r)
 # Separate contract and checker roots work without changing the pinned checker.
 code_dir=out/'split-checker';code_dir.mkdir(exist_ok=True)
 for f in ['verify_event_proof.py','report_contract.py']:shutil.copy2(P/f,code_dir/f)
 splitcmd=cmd.copy();splitcmd[2]=str(code_dir/'verify_event_proof.py');splitcmd+=['--package-root',str(C),'--source-root',str(S)]
 proc=subprocess.run(splitcmd,cwd=out,env=env,capture_output=True,text=True);r=json.loads(proc.stdout)
 assertion('split-installation-cli',proc.returncode==0 and r['status']==PASS and not list(report_validator.iter_errors(r)))
 helper=code_dir/'report_contract.py';helper.write_bytes(helper.read_bytes()+b'\n# unauthorized bytes change\n')
 proc=subprocess.run(splitcmd,cwd=out,env=env,capture_output=True,text=True);r=json.loads(proc.stdout)
 assertion('helper-code-tamper',proc.returncode==2 and any(e['code']=='VERIFIER_PIN_MISMATCH' for e in r['errors']) and not list(report_validator.iter_errors(r)))
 shutil.rmtree(code_dir)
 # No-site Python has no jsonschema; dependency errors still use frozen report validation.
 no_deps=[cmd[0],'-S','-B',*cmd[2:]]
 if '--dependency-dir' in no_deps:
  i=no_deps.index('--dependency-dir');del no_deps[i:i+2]
 proc=subprocess.run(no_deps,cwd=out,env=env,capture_output=True,text=True);r=json.loads(proc.stdout)
 assertion('portable-cli-missing-dependencies',proc.returncode==3 and r['status']=='DEPENDENCY_UNAVAILABLE' and not list(report_validator.iter_errors(r)));write(out/'reports'/'cli-missing-dependencies.json',r)
 # Controlled dependency-version mismatch exercises the actual check, without writing dependencies.
 original_version=checker.version
 checker.version=lambda name:'0.0.0'
 try:run('jcs-version-mismatch',base,'DEPENDENCY_UNAVAILABLE','RFC8785_DEPENDENCY_MISMATCH',persist=False)
 finally:checker.version=original_version
 original_filepins=checker.JCS_FILES.copy();checker.JCS_FILES['__init__.py']='0'*64
 try:run('jcs-implementation-pin-mismatch',base,'DEPENDENCY_UNAVAILABLE','RFC8785_DEPENDENCY_MISMATCH',persist=False)
 finally:checker.JCS_FILES=original_filepins
 original_dumps=rfc8785.dumps;rfc8785.dumps=lambda v:b'{}'
 try:run('jcs-behavior-mismatch',base,'DEPENDENCY_UNAVAILABLE','RFC8785_DEPENDENCY_MISMATCH',persist=False)
 finally:rfc8785.dumps=original_dumps
 shutil.rmtree(pkg);shutil.rmtree(portable)
 write(out/'case-catalog.json',{'schemaVersion':'fixture-catalog.v1','cases':catalog,'trustModel':'All fixtures are fictional. Repinned alternate profiles/contexts are explicitly owner-selected test setups. Attack cases preserve base trust roots unless stated in source.'})
 result={'status':'PASS' if all(x['pass'] for x in records) else 'FAIL','checks':len(records),'passed':sum(x['pass'] for x in records),'failed':[x for x in records if not x['pass']],'familyCount':7,'commitClassCount':9,'allPairingsChecked':63,'runtimeAdmission':'NOT_ESTABLISHED','results':records}
 write(out/'conformance-report.json',result)
 print(json.dumps({k:v for k,v in result.items() if k!='results'}));print('Next: independent owner review of this candidate packet.')
 return 0 if result['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
