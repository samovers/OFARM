"""Fictional source formats exercise the interface; they are not authority schemas."""
from pathlib import Path
import json,sys,copy,base64
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H.parents[2]/'plans/domain-contract-verifier-20261021/local-dependencies'))
from path_common import sha,digest
from verify_success_path import CORE,PATHS,PARTY_ROLES
BASES=['NATURAL_PERSON_SELF','REPRESENTED_PARTY_AUTHORIZED_REPRESENTATION','AGENT_PARTY_DIRECT_GRANT','REPRESENTED_PARTY_EXPLICIT_DELEGATION']
def raw(v):return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode()
def b(v):return {'ref':v,'revisionRef':'fixture-r1'}
def infer(v):
 if isinstance(v,dict) and set(v) in [{'ref','revisionRef'},{'ref','digest'}]:return {'$ref':'https://ofarm.dev/schema/drafts/non-default/authorization-decision-evidence/canonical-success-path/types/v0.1#/$defs/binding'}
 if isinstance(v,dict):return {'type':'object','additionalProperties':False,'required':list(v),'properties':{k:infer(x) for k,x in v.items()}}
 if isinstance(v,list):return {'type':'array','items':{'anyOf':[infer(x) for x in v]} if v else {}}
 if type(v)is bool:return {'type':'boolean'}
 if isinstance(v,str):return {'type':'string'}
 if isinstance(v,int):return {'type':'integer'}
 if v is None:return {'type':'null'}
 raise ValueError(v)
def family(role):return 'PARTY' if role in PARTY_ROLES else 'PRINCIPAL' if role=='AUTHENTICATED_PRINCIPAL' else 'AUTHORITY_GRANT' if role=='SOURCE_AUTHORITY' else role

def fixture(basis,role_target=False):
 sources={};bindings={};families={};formats={};schemas={}
 def add(k,f,recordid,projection,source=False):
  v={'schemaVersion':'fictional.canonicalPathSource.v0.1','recordId':recordid,'projection':projection}
  if source:v['sourceRecordDigest']=digest(v)
  sources[k]=v;bindings[k]={'ref':recordid,'digest':v['sourceRecordDigest']} if source else b(recordid);families[k]=f
  return bindings[k]
 principal='principal:agent' if basis in BASES[2:] else 'principal:natural'
 subject='party:represented' if basis in [BASES[1],BASES[3]] else 'party:agent' if basis==BASES[2] else 'party:natural'
 roles={
 'AUTHENTICATED_PRINCIPAL':(principal,{'principalRef':principal}),
 'PRINCIPAL_RESOLUTION':('resolution:one',{'authenticatedPrincipalRef':principal,'resolvedPrincipalKind':'SOFTWARE_AGENT' if basis in BASES[2:] else 'NATURAL_PERSON','principalPartyRef':'party:agent' if basis in BASES[2:] else 'party:natural'}),
 'AUTHORITY_SUBJECT_PARTY':(subject,{'partyRef':subject}),
 }
 if basis in BASES[:2]:roles['NATURAL_PERSON_PARTY']=('party:natural',{'partyRef':'party:natural'})
 if basis in [BASES[1],BASES[3]]:roles['REPRESENTED_PARTY']=('party:represented',{'partyRef':'party:represented'})
 if basis==BASES[1]:roles['REPRESENTATION_BASIS']=('representation:one',{'naturalPersonPartyRef':'party:natural','representedPartyRef':'party:represented'})
 if basis in BASES[2:]:
  roles.update({'AGENT_PARTY':('party:agent',{'partyRef':'party:agent'}),'AGENT_IDENTITY':('identity:agent',{'agentPartyRef':'party:agent','agentInstanceRef':principal}),'SPONSOR_PARTY':('party:sponsor',{'partyRef':'party:sponsor'}),'SOFTWARE_AGENT_PROFILE':('profile:agent',{'profileRef':'profile:agent'}),'CP3_AUTHORITY_SNAPSHOT':('snapshot:cp3',{'snapshotRef':'snapshot:cp3'}),'CP3_REVOCATION_STATE':('revocation:cp3',{'agentInstanceRef':principal})})
  cp={'agentInstanceRef':principal,'agentSponsorRef':'party:sponsor','softwareAgentProfileRef':'profile:agent','authoritySnapshotRef':'snapshot:cp3'}
  env={k:v for k,v in cp.items() if k!='agentInstanceRef'};env.update(executingAgentInstanceRef=principal,agentActorshipBindingRef='actorship:one',revocationStateRef='revocation:cp3')
  roles['CP3_ACTORSHIP_BINDING']=('actorship:one',cp);roles['CP3_AUTHORITY_ENVELOPE']=('envelope:one',env)
  env.update(requestedActionClass='ASSERT_OPERATION_CLAIM',authorizationDecisionResultRef='result:one',authorizationDecisionTraceRef='trace:one')
  roles['CP3_REVOCATION_STATE']=('revocation:cp3',{'executingAgentInstanceRef':principal,'agentSponsorRef':'party:sponsor','authorityEnvelopeRef':'envelope:one'})
 if role_target:roles['ROLE_ASSIGNMENT']=('role:one',{'partyRef':subject})
 for role,(rid,projection) in roles.items():add(role,family(role),rid,projection)
 authority=add('SOURCE_AUTHORITY','AUTHORITY_GRANT','grant:one',{'grantTarget':{'targetKind':'ROLE_ASSIGNMENT' if role_target else 'PARTY','targetRef':'role:one' if role_target else subject}},True)
 if basis==BASES[3]:add('DELEGATION_GRANT','DELEGATION_GRANT','delegation:one',{'delegatingPartyRef':subject,'delegatePartyRef':'party:agent','sourceAuthorityGrantRefs':[authority['ref']]},True)
 add('SNAPSHOT_EVIDENCE_POLICY_REGISTRY','EVIDENCE_POLICY_REGISTRY','registry:evidence',{'revision':'fixture-r1','policyRefs':['policy:evidence']})
 add('SNAPSHOT_SOVEREIGNTY_POLICY','SOVEREIGNTY_POLICY','policy:sovereignty',{'revision':'fixture-r1','tenantRef':'tenant:fixture'})
 basis_roles=list(sources)
 # Complete fictional intent, including nested business content, is retained.
 intent=add('EFFECT_INTENT','EFFECT_INTENT','intent:one',{'proposedAssertion':{'text':'Fictional full submitted claim','nested':{'decisionBundleDigest':'retain-this-nested-value'}},'evidenceRefs':['measurement:one'],'subjectTime':{'profile':'PERFORMED_INSTANT','at':'2026-10-21T08:00:00Z'}})
 intent_sid='https://ofarm.dev/schema/fictional-conformance/canonical-success-path/EFFECT_INTENT/v0.1'
 intent_schema={'$schema':'https://json-schema.org/draft/2020-12/schema','$id':intent_sid,**infer(sources['EFFECT_INTENT'])};schemas[intent_sid]=intent_schema
 isc={'schemaId':intent_sid,'schemaVersion':'fictional.canonicalPathSource.v0.1','schemaDigest':'sha256:'+sha(raw(intent_schema))}
 policy=add('POLICY','POLICY','policy:one',{'policyId':'policy:one','policyVersion':'fixture-1','immutablePolicyRepresentation':{'selectedRules':['rule:one'],'purpose':'Fictional packaging for offline comparisons only'}})
 rule=add('RULE','RULE','rule:one',{'selectedRuleId':'rule:one','ruleRevision':'fixture-r1','actionClass':'ASSERT_OPERATION_CLAIM','intentSchema':isc,'semanticClosure':{'law':'PR11 pinned by the source profile','extractor':'fictional-preserve-complete-intent','eligibilityEvaluatorImplemented':False}})
 manifest=add('BINDING_MANIFEST','BINDING_MANIFEST','manifest:one',{'policyBinding':policy,'ruleBinding':rule})
 view=add('DERIVED_VIEW','DERIVED_VIEW','view:one',{'intentBinding':intent,'actionClass':'ASSERT_OPERATION_CLAIM','target':{'scopeType':'FARM','scopeRef':'farm:one'}})
 snapshot=b('snapshot:evaluation');visible=[];basis_entries=[]
 for role in basis_roles:
  key='visibility:'+role;vb=add(key,'SNAPSHOT_VISIBILITY_PROOF',key,{'sourceBinding':bindings[role],'snapshotBinding':snapshot})
  basis_entries.append({'role':'ADDITIONAL_AUTHORITY_BASIS' if role.startswith('SNAPSHOT_') else role,'sourceKey':role,'artifactFamily':families[role],'binding':bindings[role],'visibilitySourceKey':key})
  visible.append({'binding':bindings[role],'artifactFamily':families[role],'visibilityBinding':vb})
 add('EVALUATION_SNAPSHOT','EVALUATION_SNAPSHOT',snapshot['ref'],{'policyBinding':policy,'authorizationEvaluatedAt':'2026-10-21T09:00:00Z','visibleBasis':visible,'indexWatermarks':{'roleGrant':'fixture:10','delegationSharing':'fixture:20','revocation':'fixture:30'},'principalResolutionBinding':bindings['PRINCIPAL_RESOLUTION']})
 sources['EVALUATION_SNAPSHOT']['projection'].update(historyPosition='fixture:history:40',evidencePolicyRegistryBinding=bindings['SNAPSHOT_EVIDENCE_POLICY_REGISTRY'],sovereigntyPolicyBinding=bindings['SNAPSHOT_SOVEREIGNTY_POLICY'])
 if basis in BASES[2:]:sources['EVALUATION_SNAPSHOT']['projection']['cp3AuthoritySnapshotBinding']=bindings['CP3_AUTHORITY_SNAPSHOT']
 path_type='DELEGATED_GRANT' if basis==BASES[3] else 'ROLE_TARGETED_GRANT' if role_target else 'DIRECT_PARTY_GRANT'
 ds=[bindings['DELEGATION_GRANT']] if basis==BASES[3] else []
 path={'pathId':'path:selected','pathType':path_type,'pathDisposition':'PATH_ALLOW','sourceRecordBinding':authority,'delegationSourceBindings':ds,'canonicalTuple':{'pathTypeOrder':PATHS.index(path_type),'sourceRecordId':'grant:one','delegationSourceRecordIds':sorted(x['ref'] for x in ds)},'authoritySubjectPartyRef':subject,'authoritySubjectBasis':basis,'authoritySubjectBasisRefs':[x['binding'] for x in basis_entries],'basis':basis_entries}
 request=add('REQUEST','REQUEST','request:one',{'requestId':'request:one','actionClass':'ASSERT_OPERATION_CLAIM','intentBinding':intent,'effectIntentDigest':digest(sources['EFFECT_INTENT']),'effectIntentCanonicalization':'JCS_RFC8785_SHA256'})
 common={'requestId':'request:one','actionClass':'ASSERT_OPERATION_CLAIM','intentBinding':intent,'intentSchema':isc,'policyBinding':policy,'ruleBinding':rule,'manifestBinding':manifest,'derivedViewBinding':view,'snapshotBinding':snapshot,'policyId':'policy:one','policyVersion':'fixture-1','policyDigest':digest(sources['POLICY']),'selectedRuleId':'rule:one','ruleRevision':'fixture-r1','ruleDigest':digest(sources['RULE']),'authorizationEvaluatedAt':'2026-10-21T09:00:00Z','decisionValidUntil':'2026-10-21T10:00:00Z','selectedPathId':path['pathId'],'decisionOutcome':'ALLOW','winningDisposition':'PATH_ALLOW','resultId':'result:one','traceId':'trace:one'}
 common.update(effectIntentDigest=digest(sources['EFFECT_INTENT']),effectIntentCanonicalization='JCS_RFC8785_SHA256',derivedViewDigest=digest(sources['DERIVED_VIEW']))
 add('RESULT','RESULT','result:one',{**common,'selectedPath':path});add('TRACE','TRACE','trace:one',{**common,'paths':[path]})
 sources['RESULT']['retainedPayload']={'decisionBundleDigest':'nested field must remain in the digest input'}
 sources['TRACE']['retainedPayload']={'completeTraceNote':'Retained without reconstructing or evaluating authorization candidates.'}
 bundle=digest({'schemaVersion':'ofarm.authorizationDecisionBundleDigestInput.v0.2','request':sources['REQUEST'],'result':sources['RESULT'],'trace':sources['TRACE']})
 sources['RESULT']['decisionBundleDigest']=bundle;sources['TRACE']['decisionBundleDigest']=bundle
 for key,record in sources.items():
  sid='https://ofarm.dev/schema/fictional-conformance/canonical-success-path/'+key.replace(':','-')+'/v0.1'
  if sid not in schemas:schemas[sid]={'$schema':'https://json-schema.org/draft/2020-12/schema','$id':sid,**infer(record)}
  formats[key]={'schemaId':sid,'schemaSha256':sha(raw(schemas[sid])),'identityPointer':'/recordId','projectionPointer':'/projection','digestMode':'SOURCE_RECORD_EXCLUDING_TOP_DIGEST' if families[key] in ['AUTHORITY_GRANT','DELEGATION_GRANT'] else 'FULL_VALUE'}
 contract=json.loads((H/'contract.json').read_text())
 profile={'schemaVersion':'ofarm.canonicalSuccessfulPathSourceProfile.v0.1','profileId':'profile:fictional-success-path','profileRevision':'fixture-r1','authorizationLawSha256':contract['authorizationLawSha256'],'outputKind':'AUTHORIZATION_OWNER_SUCCESSFUL_PATH_OUTPUT','schemaDigests':{sid:sha(raw(s)) for sid,s in schemas.items()},'formats':formats}
 evidence={'schemaVersion':'ofarm.canonicalSuccessfulPathEvidence.v0.1','evidenceId':'evidence:successful-path','sourceProfileBinding':b(profile['profileId']),'sources':{k:bindings[k] for k in CORE},'decisionBundleDigest':bundle,'selectedPath':copy.deepcopy(path)}
 context={'schemaVersion':'ofarm.canonicalSuccessfulPathVerificationContext.v0.1','contextId':'context:independent-owner-fixture','contractDigest':contract['contractDigest'],'sourceOrigin':'FICTIONAL_CONFORMANCE','profileBinding':b(profile['profileId']),'profileBytesSha256':sha(raw(profile)),'selectedActionClass':'ASSERT_OPERATION_CLAIM','coreSources':{k:k for k in CORE},'sources':[{'key':k,'artifactFamily':families[k],'binding':bindings[k],'bytesSha256':sha(raw(v)),'valueDigest':digest(v),'formatId':k} for k,v in sources.items()]}
 return {'evidence':evidence,'profile':profile,'context':context,'sources':sources,'schemas':schemas}

def encode(model):
 enc=lambda b:base64.b64encode(b).decode()
 return {'schemaVersion':'ofarm.canonicalSuccessfulPathVerificationWire.v0.1','evidenceBytesBase64':enc(raw(model['evidence'])),'profileBytesBase64':enc(raw(model['profile'])),'contextBytesBase64':enc(raw(model['context'])),'sourceBytesBase64':{k:enc(raw(v)) for k,v in model['sources'].items()},'schemaBytesBase64':{k:enc(raw(v)) for k,v in model['schemas'].items()}}
if __name__=='__main__':
 rows=[]
 for n,basis in enumerate(BASES):
  for target in [False,True]:
   name=f'basis-{n+1}-'+('role' if target else 'party');m=fixture(basis,target);d=H/'fixtures'/name;d.mkdir(parents=True,exist_ok=True)
   (d/'model.json').write_bytes(raw(m));(d/'wire.json').write_bytes(raw(encode(m)));(d/'context.sha256').write_text(sha(raw(m['context']))+'\n');rows.append({'id':name,'basis':basis,'target':'ROLE_ASSIGNMENT' if target else 'PARTY','expected':'PASS','scope':'FICTIONAL_SELECTED_OUTPUT_INTEGRITY_ONLY'})
 (H/'fixtures/positive-cases.json').write_bytes(raw({'cases':rows}));print('Built',len(rows),'positive cases')
