"""Construction only. Does not edit foreign sources or install anything."""
from pathlib import Path
import json,hashlib,shutil
H=Path(__file__).resolve().parent;ROOT=H.parents[2]
ID='https://ofarm.dev/schema/drafts/non-default/authorization-decision-evidence/canonical-success-path/'
def obj(p,required=None):return {'type':'object','additionalProperties':False,'properties':p,'required':list(p) if required is None else required}
def arr(s,n=0):return {'type':'array','items':s,'minItems':n}
def enum(xs):return {'enum':xs}
def const(v):return {'const':v}
def ref(n):return {'$ref':ID+'types/v0.1#/$defs/'+n}
T={'type':'string','minLength':1};P={'type':'string','pattern':'^/(?:[^~]|~[01])*(?![\\s\\S])'};SHA={'type':'string','pattern':'^[0-9a-f]{64}(?![\\s\\S])'};DIG={'type':'string','pattern':'^sha256:[0-9a-f]{64}(?![\\s\\S])'}
B=obj({'ref':T,'revisionRef':T,'digest':DIG},['ref']);B['oneOf']=[{'required':['revisionRef'],'not':{'required':['digest']}},{'required':['digest'],'not':{'required':['revisionRef']}}]
CORE=['REQUEST','RESULT','TRACE','POLICY','RULE','BINDING_MANIFEST','EFFECT_INTENT','DERIVED_VIEW','EVALUATION_SNAPSHOT']
BASES=['NATURAL_PERSON_SELF','REPRESENTED_PARTY_AUTHORIZED_REPRESENTATION','AGENT_PARTY_DIRECT_GRANT','REPRESENTED_PARTY_EXPLICIT_DELEGATION']
PATHS=['DIRECT_PARTY_GRANT','ROLE_TARGETED_GRANT','DELEGATED_GRANT','SHARING_GRANT_ACCESS']
ROLES=['AUTHENTICATED_PRINCIPAL','PRINCIPAL_RESOLUTION','NATURAL_PERSON_PARTY','AUTHORITY_SUBJECT_PARTY','REPRESENTED_PARTY','REPRESENTATION_BASIS','AGENT_PARTY','AGENT_IDENTITY','CP3_ACTORSHIP_BINDING','CP3_AUTHORITY_ENVELOPE','CP3_AUTHORITY_SNAPSHOT','CP3_REVOCATION_STATE','SOFTWARE_AGENT_PROFILE','SPONSOR_PARTY','SOURCE_AUTHORITY','DELEGATION_GRANT','ROLE_ASSIGNMENT','SHARING_GRANT','ADDITIONAL_AUTHORITY_BASIS']
entry=obj({'role':enum(ROLES),'sourceKey':T,'artifactFamily':T,'binding':B,'visibilitySourceKey':T})
path=obj({'pathId':T,'pathType':enum(PATHS),'pathDisposition':enum(['PATH_ALLOW','PATH_REQUIRE_HUMAN_APPROVAL','PATH_REQUIRE_REVIEW','PATH_DENY','PATH_INAPPLICABLE']),'sourceRecordBinding':B,'delegationSourceBindings':arr(B),'canonicalTuple':obj({'pathTypeOrder':{'type':'integer','minimum':0,'maximum':3},'sourceRecordId':T,'delegationSourceRecordIds':arr(T)}),'authoritySubjectPartyRef':T,'authoritySubjectBasis':enum(BASES),'authoritySubjectBasisRefs':arr(B,1),'basis':arr(entry,1)})
intent_schema=obj({'schemaId':T,'schemaVersion':T,'schemaDigest':DIG})
common={'requestId':T,'actionClass':T,'intentBinding':B,'intentSchema':intent_schema,'policyBinding':B,'ruleBinding':B,'manifestBinding':B,'derivedViewBinding':B,'snapshotBinding':B,'policyId':T,'policyVersion':T,'policyDigest':DIG,'selectedRuleId':T,'ruleRevision':T,'ruleDigest':DIG,'authorizationEvaluatedAt':{'type':'string','format':'date-time'},'decisionValidUntil':{'type':'string','format':'date-time'},'selectedPathId':T,'decisionOutcome':const('ALLOW'),'winningDisposition':const('PATH_ALLOW')}
result=obj({**common,'resultId':T,'traceId':T,'selectedPath':ref('path')})
trace=obj({**common,'traceId':T,'resultId':T,'paths':arr(ref('path'),1)})
for s in [result,trace]:
 s['properties'].update(effectIntentDigest=DIG,effectIntentCanonicalization=const('JCS_RFC8785_SHA256'),derivedViewDigest=DIG)
 s['required']+=['effectIntentDigest','effectIntentCanonicalization','derivedViewDigest']
def save(name,value):
 p=H/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
def schema(name,body):return {'$schema':'https://json-schema.org/draft/2020-12/schema','$id':ID+name+'/v0.1',**body}
schemas={'types':schema('types',{'$defs':{'binding':B,'path':path,'basisEntry':entry,'intentSchema':intent_schema,'resultProjection':result,'traceProjection':trace}})}
snapshot=obj({'policyBinding':B,'authorizationEvaluatedAt':{'type':'string','format':'date-time'},'principalResolutionBinding':B,'historyPosition':T,'indexWatermarks':obj({'roleGrant':T,'delegationSharing':T,'revocation':T}),'evidencePolicyRegistryBinding':B,'sovereigntyPolicyBinding':B,'cp3AuthoritySnapshotBinding':B,'visibleBasis':arr(obj({'binding':B,'artifactFamily':T,'visibilityBinding':B}),1)},['policyBinding','authorizationEvaluatedAt','principalResolutionBinding','historyPosition','indexWatermarks','evidencePolicyRegistryBinding','sovereigntyPolicyBinding','visibleBasis'])
schemas['types']['$defs']['snapshotProjection']=snapshot
schemas['evidence']=schema('evidence',obj({'schemaVersion':const('ofarm.canonicalSuccessfulPathEvidence.v0.1'),'evidenceId':T,'sourceProfileBinding':B,'sources':obj({k:B for k in CORE}),'decisionBundleDigest':DIG,'selectedPath':ref('path')}))
fmt=obj({'schemaId':T,'schemaSha256':SHA,'identityPointer':{'oneOf':[P,{'type':'null'}]},'projectionPointer':{'type':'string','pattern':'^(?:|/(?:[^~]|~[01])*)(?![\\s\\S])'},'digestMode':enum(['FULL_VALUE','SOURCE_RECORD_EXCLUDING_TOP_DIGEST'])})
schemas['profile']=schema('profile',obj({'schemaVersion':const('ofarm.canonicalSuccessfulPathSourceProfile.v0.1'),'profileId':T,'profileRevision':T,'authorizationLawSha256':SHA,'outputKind':const('AUTHORIZATION_OWNER_SUCCESSFUL_PATH_OUTPUT'),'schemaDigests':{'type':'object','minProperties':1,'additionalProperties':SHA},'formats':{'type':'object','minProperties':1,'additionalProperties':fmt}}))
source=obj({'key':T,'artifactFamily':T,'binding':B,'bytesSha256':SHA,'valueDigest':DIG,'formatId':T})
schemas['context']=schema('context',obj({'schemaVersion':const('ofarm.canonicalSuccessfulPathVerificationContext.v0.1'),'contextId':T,'contractDigest':DIG,'sourceOrigin':enum(['FICTIONAL_CONFORMANCE','INDEPENDENT_OWNER_SELECTION']),'profileBinding':B,'profileBytesSha256':SHA,'selectedActionClass':T,'coreSources':obj({k:T for k in CORE}),'sources':arr(source,1)}))
schemas['wire']=schema('wire',obj({'schemaVersion':const('ofarm.canonicalSuccessfulPathVerificationWire.v0.1'),'evidenceBytesBase64':T,'profileBytesBase64':T,'contextBytesBase64':T,'sourceBytesBase64':{'type':'object','additionalProperties':T},'schemaBytesBase64':{'type':'object','additionalProperties':T}}))
schemas['report']=schema('report',obj({'schemaVersion':const('ofarm.canonicalSuccessfulPathVerificationReport.v0.1'),'disposition':enum(['PASS','FAIL','INPUT_ERROR']),'verificationScope':const('SELECTED_OWNER_OUTPUT_INTEGRITY_ONLY'),'established':arr(T),'notEstablished':arr(T,1),'errors':arr(obj({'code':T,'pointer':{'type':'string'},'detail':{'type':'string'}})),'selectedParty':{'type':['string','null']},'sourceOrigin':{'type':['string','null']},'inputDigests':{'type':'object','additionalProperties':SHA},'next':T}))
for n,s in schemas.items():save('schemas/'+n+'.schema.json',s)
pr=ROOT/'plans/assertion-act-evidence-20261021/owner-contract/sources/pr11.md';raw=pr.read_bytes();assert hashlib.sha256(raw).hexdigest()=='8c218df076fcf06aceb531173a854091e21bda7775ad1fe66dd06a772857691f';(H/'sources/pr11.md').write_bytes(raw)
save('source-pins.json',{'sources':[{'path':'sources/pr11.md','repository':'samovers/OFARM','commit':'d1178fe07d57accedde5748672602db38346b3e6','originalPath':'package_meta/history/clean_baseline_migration/phase_reports/authorization_constraints_and_decision_evidence_rfc_candidate_v0_2.md','sha256':hashlib.sha256(raw).hexdigest(),'clauses':['6.2','8.2','15.2','16','16.1','17.2','17.5','17.6','18.8']}],'status':'PINNED_NON_DEFAULT_SOURCE_LAW_UNCHANGED'})
if __name__=='__main__':print('Schemas and exact PR11 source prepared.')
