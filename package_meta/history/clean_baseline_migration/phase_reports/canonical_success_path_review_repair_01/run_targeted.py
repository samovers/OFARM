"""Specific-code repair regressions; all owner inputs here are fictional."""
from pathlib import Path
import base64,copy,json,sys
from build_fixtures import raw,encode,infer
from test_support import fresh,outputs,selected,cohere,rebind_key,replace,repin
from path_common import sha,digest
from verify_success_path import verify,PATHS
H=Path(__file__).resolve().parent;OUT=H/'targeted-checks';OUT.mkdir(exist_ok=True);rows=[]
def run(name,m,code=None,detail=None,wire_edit=None):
 w=encode(m)
 if wire_edit:wire_edit(w)
 dec=lambda x:base64.b64decode(x)
 cb=dec(w['contextBytesBase64']);pin=sha(cb)
 r=verify(dec(w['evidenceBytesBase64']),dec(w['profileBytesBase64']),cb,{k:dec(v) for k,v in w['sourceBytesBase64'].items()},{k:dec(v) for k,v in w['schemaBytesBase64'].items()},expected_context_sha256=pin)
 codes=[x['code'] for x in r['errors']];expected=[] if code is None else [code]
 ok=(r['disposition']=='PASS' if code is None else r['disposition'] in ['FAIL','INPUT_ERROR']) and codes==expected
 if detail:ok=ok and len(r['errors'])==1 and detail in r['errors'][0]['detail']
 d=OUT/name;d.mkdir(exist_ok=True);(d/'wire.json').write_bytes(raw(w));(d/'context.sha256').write_text(pin+'\n');(d/'api-report.json').write_bytes(raw(r))
 row={'id':name,'expected':'PASS' if code is None else 'FAIL','expectedCodes':expected,'actual':r['disposition'],'codes':codes,'matched':ok}
 if detail:row['expectedDetailContains']=detail
 rows.append(row);print(name,'OK' if ok else 'MISMATCH',codes,flush=True)
 return r

def output_change(m,field,value):
 for o in outputs(m):o[field]=copy.deepcopy(value)
 return cohere(m)
def source_change(m,key,field,value):m['sources'][key]['projection'][field]=copy.deepcopy(value);return cohere(m)

# F1: projected native revisions, complete immutable identity in one snapshot.
for name in ['basis-1-party','basis-2-party','basis-3-party','basis-4-party']:
 m=fresh(name);m['sources']['AUTHORITY_SUBJECT_PARTY']['recordRevision']='fixture-r2';run(name+'-native-revision-mismatch',cohere(m),'SOURCE_RECORD_REVISION_MISMATCH')
 m=fresh(name);m['profile']['formats']['AUTHORITY_SUBJECT_PARTY']['revisionPointer']=None;run(name+'-missing-revision-pointer',cohere(m),'REVISION_POINTER_REQUIRED')
 m=fresh(name);m['sources']['AUTHORITY_SUBJECT_PARTY']['recordRevision']='fixture-r2';rebind_key(m,'AUTHORITY_SUBJECT_PARTY',{'ref':m['sources']['AUTHORITY_SUBJECT_PARTY']['recordId'],'revisionRef':'fixture-r2'});run(name+'-two-party-revisions',cohere(m),'IMMUTABLE_ID_REUSED_WITH_DIFFERENT_BYTES')
 m=fresh(name);entry=next(x for x in m['context']['sources'] if x['key']=='AUTHORITY_SUBJECT_PARTY');rebind_key(m,'AUTHORITY_SUBJECT_PARTY',{'ref':entry['binding']['ref'],'digest':digest(m['sources']['AUTHORITY_SUBJECT_PARTY'])});m['profile']['formats']['AUTHORITY_SUBJECT_PARTY']['revisionPointer']=None;run(name+'-digest-party-no-revision-pointer',cohere(m))
# Alternate native revision field is profile selected, not hard-coded.
m=fresh();rec=m['sources']['AUTHENTICATED_PRINCIPAL'];rec['nativeRevision']=rec.pop('recordRevision');f=m['profile']['formats']['AUTHENTICATED_PRINCIPAL'];f['revisionPointer']='/nativeRevision';m['schemas'][f['schemaId']]={'$schema':'https://json-schema.org/draft/2020-12/schema','$id':f['schemaId'],**infer(rec)};run('native-revision-alternate-field',cohere(m))

# F2: every retained tuple is encoded, ordered and consistent with owner selection.
for change,code in [('order','CANONICAL_TUPLE_ENCODING_MISMATCH'),('source-id','CANONICAL_TUPLE_ENCODING_MISMATCH'),('delegation-order','CANONICAL_TUPLE_ENCODING_MISMATCH'),('duplicate-delegation','DUPLICATE_TUPLE_SOURCE')]:
 m=fresh('basis-4-party');other=copy.deepcopy(m['sources']['TRACE']['projection']['paths'][0]);other.update(pathId='path:retained',pathDisposition='PATH_DENY')
 if change=='order':other['canonicalTuple']['pathTypeOrder']=0
 elif change=='source-id':other['canonicalTuple']['sourceRecordId']='grant:other'
 elif change=='delegation-order':other['canonicalTuple']['delegationSourceRecordIds']=[]
 else:other['delegationSourceBindings']*=2;other['canonicalTuple']['delegationSourceRecordIds']*=2
 m['sources']['TRACE']['projection']['paths'].append(other);run('retained-tuple-'+change,cohere(m),code)
for disposition,code in [('PATH_ALLOW','RETAINED_ALLOW_PATH_PRECEDES_SELECTION'),('PATH_DENY',None),('PATH_REQUIRE_HUMAN_APPROVAL',None)]:
 m=fresh('basis-1-role');other=copy.deepcopy(m['sources']['TRACE']['projection']['paths'][0]);other.update(pathId='path:lower-retained',pathType='DIRECT_PARTY_GRANT',pathDisposition=disposition)
 # A genuinely separate direct-Party source, not a role grant relabelled direct.
 for source_key,new_key in [('SOURCE_AUTHORITY','LOWER_DIRECT_AUTHORITY'),('visibility:SOURCE_AUTHORITY','visibility:LOWER_DIRECT_AUTHORITY')]:
  rec=copy.deepcopy(m['sources'][source_key]);rec['recordId']='grant:aaa' if source_key=='SOURCE_AUTHORITY' else new_key
  entry=copy.deepcopy(next(x for x in m['context']['sources'] if x['key']==source_key));entry['key']=new_key
  if source_key=='SOURCE_AUTHORITY':
   rec['projection']['grantTarget']={'targetKind':'PARTY','targetRef':'party:natural'};rec['sourceRecordDigest']=digest({k:v for k,v in rec.items() if k!='sourceRecordDigest'});grant_binding={'ref':rec['recordId'],'digest':rec['sourceRecordDigest']};entry['binding']=grant_binding
  else:
   rec['projection']['sourceBinding']=grant_binding;entry['binding']={'ref':new_key,'revisionRef':'fixture-r1'};visibility_binding=entry['binding']
  m['sources'][new_key]=rec;m['context']['sources'].append(entry)
 other['sourceRecordBinding']=grant_binding;other['canonicalTuple'].update(pathTypeOrder=0,sourceRecordId=grant_binding['ref'])
 for item in other['basis']:
  if item['role']=='SOURCE_AUTHORITY':item.update(sourceKey='LOWER_DIRECT_AUTHORITY',binding=grant_binding,visibilitySourceKey='visibility:LOWER_DIRECT_AUTHORITY')
 other['authoritySubjectBasisRefs']=[x['binding'] for x in other['basis']]
 m['sources']['EVALUATION_SNAPSHOT']['projection']['visibleBasis'].append({'binding':grant_binding,'artifactFamily':'AUTHORITY_GRANT','visibilityBinding':visibility_binding})
 m['sources']['TRACE']['projection']['paths'].append(other);run('lower-retained-'+disposition,cohere(m),code)
m=fresh();other=copy.deepcopy(m['sources']['TRACE']['projection']['paths'][0]);other.update(pathId='path:equal-retained');m['sources']['TRACE']['projection']['paths'].append(other);run('equal-retained-allow-tuple',cohere(m))

# F5: PR11 result/trace fields, exact rule-selected extractor bytes and postures.
for field in ['resolvedPrincipalKind','agentActionPosture','humanFinalizationRequirement','primaryReasonCode','authorizationViewExtractorRef','authorizationViewExtractorDigest']:
 m=fresh('basis-3-party')
 for o in outputs(m):del o[field]
 run('missing-output-'+field,cohere(m),'SCHEMA_INVALID',detail=field)
for name in ['basis-1-party','basis-3-party']:
 for field,value,code in [('resolvedPrincipalKind','NATURAL_PERSON' if name=='basis-3-party' else 'SOFTWARE_AGENT','OUTPUT_PRINCIPAL_KIND_MISMATCH'),('agentActionPosture','HUMAN_ONLY','OUTPUT_CP3_POSTURE_MISMATCH'),('humanFinalizationRequirement','FRESH_HUMAN_APPROVAL_REQUIRED','HUMAN_FINALIZATION_RULE_MISMATCH'),('primaryReasonCode','NO_AUTHORITY_BASIS','SUCCESS_PRIMARY_REASON_MISMATCH'),('authorizationViewExtractorRef','extractor:other','EXTRACTOR_REFERENCE_MISMATCH'),('authorizationViewExtractorDigest','sha256:'+'0'*64,'EXTRACTOR_DIGEST_MISMATCH')]:run(name+'-output-'+field,output_change(fresh(name),field,value),code)
for field,value,code in [('authorizationViewExtractorRef','extractor:other','EXTRACTOR_REFERENCE_MISMATCH'),('authorizationViewExtractorDigest','sha256:'+'0'*64,'EXTRACTOR_DIGEST_MISMATCH'),('humanFinalizationRequirement','DIRECT_HUMAN_ACTION_REQUIRED','HUMAN_FINALIZATION_RULE_MISMATCH'),('agentActionPosture','HUMAN_ONLY','OUTPUT_CP3_POSTURE_MISMATCH')]:run('rule-'+field,source_change(fresh('basis-3-party'),'RULE',field,value),code)
for field,value in [('authorizationViewExtractorRef','extractor:other'),('authorizationViewExtractorDigest','sha256:'+'0'*64)]:run('view-'+field,source_change(fresh(),'DERIVED_VIEW',field,value),'DERIVED_VIEW_EXTRACTOR_MISMATCH')
m=fresh();m['sources']['AUTHORIZATION_VIEW_EXTRACTOR']['projection']['transformation']='changed';run('changed-extractor-original-bytes',cohere(m),'SOURCE_BINDING_DIGEST_MISMATCH')
m=fresh();rebind_key(m,'AUTHORIZATION_VIEW_EXTRACTOR',{'ref':'extractor:one','revisionRef':'fixture-r1'});run('extractor-revision-only',cohere(m),'EXTRACTOR_REQUIRES_DIGEST_BINDING')
# All accepted vocabulary is retained as owner claims; this is not eligibility.
for posture in ['AGENT_ALLOWED_WITH_POLICY_CHECK','AGENT_ALLOWED_WITH_PREFLIGHT_ONLY','AGENT_ALLOWED_WITH_HUMAN_APPROVAL','HUMAN_ONLY','PROHIBITED_FOR_AGENT']:
 m=fresh('basis-3-party');m['sources']['RULE']['projection']['agentActionPosture']=posture
 for o in outputs(m):o['agentActionPosture']=posture
 run('compared-owner-posture-'+posture,cohere(m))
for finalization in ['NOT_REQUIRED','FRESH_HUMAN_APPROVAL_REQUIRED','DIRECT_HUMAN_ACTION_REQUIRED']:
 m=fresh();m['sources']['RULE']['projection']['humanFinalizationRequirement']=finalization
 for o in outputs(m):o['humanFinalizationRequirement']=finalization
 run('compared-owner-finalization-'+finalization,cohere(m))

# P1: intentional profile limit, before misleading direct/role target failure.
m=fresh()
for p in selected(m):p['pathType']='SHARING_GRANT_ACCESS';p['canonicalTuple']['pathTypeOrder']=3
run('selected-sharing-explicit-profile-rejection',cohere(m),'SELECTED_SHARING_PATH_OUTSIDE_PROFILE')
# A retained sharing source is still bound in full; it grants no selected authority.
m=fresh();other=copy.deepcopy(m['sources']['TRACE']['projection']['paths'][0]);other.update(pathId='path:sharing-retained',pathType='SHARING_GRANT_ACCESS',pathDisposition='PATH_INAPPLICABLE');other['canonicalTuple']['pathTypeOrder']=3
# Keep a complete independently pinned fictional SharingGrant and visibility.
for key,family,projection in [('SHARING_GRANT','SHARING_GRANT',{'granteePartyRef':'party:natural','sharedArtifactRef':'artifact:one','sharedArtifactFamily':'MEASUREMENT'}),('visibility:SHARING_GRANT','SNAPSHOT_VISIBILITY_PROOF',{})]:
 rec={'schemaVersion':'fictional.canonicalPathSource.v0.1','recordId':key,'recordRevision':'fixture-r1','projection':projection}
 if family=='SHARING_GRANT':rec['sourceRecordDigest']=digest(rec);binding={'ref':key,'digest':rec['sourceRecordDigest']};sharing=binding
 else:binding={'ref':key,'revisionRef':'fixture-r1'};rec['projection']={'sourceBinding':sharing,'snapshotBinding':m['evidence']['sources']['EVALUATION_SNAPSHOT']};visibility=binding
 sid='https://ofarm.dev/schema/fictional-conformance/repair/'+key.replace(':','-');m['sources'][key]=rec;m['schemas'][sid]={'$schema':'https://json-schema.org/draft/2020-12/schema','$id':sid,**infer(rec)}
 m['profile']['formats'][key]={'schemaId':sid,'schemaSha256':sha(raw(m['schemas'][sid])),'identityPointer':'/recordId','revisionPointer':'/recordRevision','schemaVersionPointer':'/schemaVersion','projectionPointer':'/projection','digestMode':'SOURCE_RECORD_EXCLUDING_TOP_DIGEST' if family=='SHARING_GRANT' else 'FULL_VALUE'}
 m['context']['sources'].append({'key':key,'artifactFamily':family,'binding':binding,'bytesSha256':sha(raw(rec)),'valueDigest':digest(rec),'formatId':key})
other['sourceRecordBinding']=sharing;other['canonicalTuple']['sourceRecordId']=sharing['ref'];other['basis'].append({'role':'SHARING_GRANT','sourceKey':'SHARING_GRANT','artifactFamily':'SHARING_GRANT','binding':sharing,'visibilitySourceKey':'visibility:SHARING_GRANT'});other['authoritySubjectBasisRefs']=[x['binding'] for x in other['basis']];m['sources']['TRACE']['projection']['paths'].append(other);run('retained-sharing-source-bound',cohere(m))

# P2: the native intent schema version location is selected by the profile.
m=fresh();record=m['sources']['EFFECT_INTENT'];record['metadata']={'contractVersion':record.pop('schemaVersion')};fmt=m['profile']['formats']['EFFECT_INTENT'];fmt['schemaVersionPointer']='/metadata/contractVersion';sid=fmt['schemaId'];m['schemas'][sid]={'$schema':'https://json-schema.org/draft/2020-12/schema','$id':sid,**infer(record)};new_digest='sha256:'+sha(raw(m['schemas'][sid]));m['sources']['RULE']['projection']['intentSchema']['schemaDigest']=new_digest
for o in outputs(m):o['intentSchema']['schemaDigest']=new_digest
alternate=cohere(m);run('intent-alternate-version-field',alternate)
m=copy.deepcopy(alternate);m['sources']['EFFECT_INTENT']['metadata']['contractVersion']='wrong';run('intent-alternate-version-mismatch',cohere(m),'INTENT_VERSION_MISMATCH')
m=fresh();m['profile']['formats']['EFFECT_INTENT']['schemaVersionPointer']=None;run('intent-missing-version-pointer',cohere(m),'INTENT_VERSION_POINTER_REQUIRED')

# Deeper semantic checks: repair earlier hashes so each test reaches its target.
for key,field,value,code in [
('PRINCIPAL_RESOLUTION','authenticatedPrincipalRef','principal:wrong','PRINCIPAL_RESOLUTION_LINK_MISMATCH'),
('PRINCIPAL_RESOLUTION','principalPartyRef','party:wrong','NATURAL_PERSON_RESOLUTION_MISMATCH'),
('PRINCIPAL_RESOLUTION','resolvedPrincipalKind','SOFTWARE_AGENT','PRINCIPAL_BASIS_KIND_MISMATCH'),
('DERIVED_VIEW','actionClass','ASSERT_STRUCTURE','DERIVED_VIEW_SOURCE_MISMATCH'),
('BINDING_MANIFEST','policyBinding',{'ref':'policy:wrong','revisionRef':'fixture-r1'},'MANIFEST_POLICY_RULE_MISMATCH'),
('EVALUATION_SNAPSHOT','principalResolutionBinding',{'ref':'resolution:wrong','revisionRef':'fixture-r1'},'SNAPSHOT_PRINCIPAL_RESOLUTION_MISMATCH'),
('RULE','selectedRuleId','rule:wrong','RULE_OUTPUT_MISMATCH'),
('RULE','ruleRevision','fixture-r2','RULE_OUTPUT_MISMATCH'),
('POLICY','policyVersion','fixture-2','POLICY_OUTPUT_MISMATCH')]:run('deep-'+key+'-'+field,source_change(fresh(),key,field,value),code)
for key,field,value,code in [
('PRINCIPAL_RESOLUTION','principalPartyRef','party:sponsor','AGENT_PARTY_RESOLUTION_MISMATCH'),
('AGENT_IDENTITY','agentInstanceRef','principal:wrong','AGENT_IDENTITY_LINK_MISMATCH'),
('CP3_ACTORSHIP_BINDING','softwareAgentProfileRef','profile:wrong','CP3_IDENTITY_LINK_MISMATCH'),
('CP3_AUTHORITY_ENVELOPE','authoritySnapshotRef','snapshot:wrong','CP3_IDENTITY_LINK_MISMATCH'),
('CP3_AUTHORITY_ENVELOPE','agentActorshipBindingRef','actorship:wrong','CP3_EVIDENCE_LINK_MISMATCH'),
('CP3_AUTHORITY_ENVELOPE','revocationStateRef','revocation:wrong','CP3_EVIDENCE_LINK_MISMATCH'),
('CP3_REVOCATION_STATE','executingAgentInstanceRef','principal:wrong','CP3_REVOCATION_LINK_MISMATCH'),
('CP3_REVOCATION_STATE','agentSponsorRef','party:wrong','CP3_REVOCATION_LINK_MISMATCH'),
('EVALUATION_SNAPSHOT','cp3AuthoritySnapshotBinding',{'ref':'snapshot:other','revisionRef':'fixture-r1'},'SNAPSHOT_CP3_BINDING_MISMATCH')]:run('deep-agent-'+key+'-'+field,source_change(fresh('basis-3-party'),key,field,value),code)
# Valid selected source bindings, but a wrong required semantic role.
m=fresh();
for p in selected(m):
 for entry in p['basis']:
  if entry['role']=='AUTHENTICATED_PRINCIPAL':entry['role']='REPRESENTATION_BASIS'
run('deep-basis-role-family',cohere(m),'BASIS_ROLE_FAMILY_MISMATCH')
m=fresh();
for p in selected(m):
 extra=copy.deepcopy(next(x for x in p['basis'] if x['role']=='AUTHENTICATED_PRINCIPAL'));p['basis'].append(extra);p['authoritySubjectBasisRefs'].append(extra['binding'])
run('deep-duplicate-basis-role',cohere(m),'DUPLICATE_BASIS_ROLE')
m=fresh();m['sources']['EVALUATION_SNAPSHOT']['projection']['visibleBasis']=[x for x in m['sources']['EVALUATION_SNAPSHOT']['projection']['visibleBasis'] if x['binding']['ref']!='grant:one'];run('deep-basis-absent-from-snapshot',cohere(m),'BASIS_NOT_IN_SELECTED_SNAPSHOT')
for field in ['evidencePolicyRegistryBinding','sovereigntyPolicyBinding']:
 m=fresh();m['sources']['EVALUATION_SNAPSHOT']['projection'][field]={'ref':'source:wrong','revisionRef':'fixture-r1'};run('deep-snapshot-'+field,cohere(m),'SNAPSHOT_REGISTRY_SOURCE_NOT_EXACTLY_RESOLVED')

# Specific first-error witnesses for the remaining reachable package/semantic checks.
for name,edit,code in [
('selected-contract',lambda m:m['context'].update(contractDigest='sha256:'+'0'*64),'SELECTED_CONTRACT_MISMATCH'),
('profile-bytes',lambda m:m['context'].update(profileBytesSha256='0'*64),'SOURCE_PROFILE_BYTES_MISMATCH'),
('profile-binding',lambda m:m['evidence']['sourceProfileBinding'].update(ref='profile:wrong'),'SOURCE_PROFILE_BINDING_MISMATCH'),
('profile-id',lambda m:m['profile'].update(profileId='profile:wrong'),'SOURCE_PROFILE_ID_MISMATCH'),
('profile-revision',lambda m:m['profile'].update(profileRevision='fixture-r2'),'SOURCE_PROFILE_REVISION_MISMATCH'),
('source-law',lambda m:m['profile'].update(authorizationLawSha256='0'*64),'SOURCE_LAW_MISMATCH'),
('unknown-format',lambda m:m['context']['sources'][0].update(formatId='unknown'),'UNKNOWN_SOURCE_FORMAT'),
('unresolved-core',lambda m:m['context']['coreSources'].update(REQUEST='unknown'),'UNRESOLVED_SOURCE_KEY'),
('core-binding',lambda m:m['evidence']['sources']['REQUEST'].update(ref='request:wrong'),'CORE_SOURCE_BINDING_MISMATCH'),
('core-family',lambda m:next(x for x in m['context']['sources'] if x['key']=='REQUEST').update(artifactFamily='OTHER'),'CORE_SOURCE_FAMILY_MISMATCH'),
('format-hash',lambda m:m['profile']['formats']['REQUEST'].update(schemaSha256='0'*64),'FORMAT_SCHEMA_NOT_SELECTED'),
('logical-id',lambda m:m['sources']['REQUEST'].update(recordId='request:wrong'),'SOURCE_LOGICAL_ID_MISMATCH'),
('content-only-party',lambda m:m['profile']['formats']['AUTHORITY_SUBJECT_PARTY'].update(identityPointer=None),'CONTENT_ONLY_IDENTITY_REQUIRES_DIGEST'),
('authority-digest-profile',lambda m:m['profile']['formats']['SOURCE_AUTHORITY'].update(digestMode='FULL_VALUE'),'AUTHORITY_SOURCE_DIGEST_PROFILE_REQUIRED')]:
 m=fresh();edit(m)
 if name!='profile-bytes':m['context']['profileBytesSha256']=sha(raw(m['profile']))
 run('coverage-'+name,repin(m),code)
m=fresh();old=m['context']['profileBinding'];m=replace(m,old,{'ref':old['ref'],'digest':'sha256:'+'0'*64});run('coverage-profile-digest',m,'SOURCE_PROFILE_DIGEST_MISMATCH')
m=fresh();sid=next(iter(m['schemas']));del m['schemas'][sid];run('coverage-schema-set',m,'SCHEMA_SET_MISMATCH')
m=fresh();sid=next(iter(m['schemas']));run('coverage-schema-bytes',m,'SCHEMA_BYTES_MISMATCH',wire_edit=lambda w:w['schemaBytesBase64'].__setitem__(sid,base64.b64encode(base64.b64decode(w['schemaBytesBase64'][sid])+b' ').decode()))
m=fresh();sid=m['profile']['formats']['REQUEST']['schemaId'];m['schemas'][sid]['$schema']='https://json-schema.org/draft/2019-09/schema';run('coverage-schema-dialect',cohere(m),'SCHEMA_ID_OR_DIALECT_MISMATCH')
m=fresh();sid=m['profile']['formats']['REQUEST']['schemaId'];new='https://ofarm.dev/schema/drafts/non-default/authorization-decision-evidence/canonical-success-path/types/v0.1';sc=m['schemas'].pop(sid);sc['$id']=new;m['schemas'][new]=sc;m['profile']['schemaDigests'].pop(sid);m['profile']['formats']['REQUEST']['schemaId']=new;run('coverage-owned-schema-override',cohere(m),'OWNED_SCHEMA_OVERRIDE')
m=fresh();entry=next(x for x in m['context']['sources'] if x['key']=='SOURCE_AUTHORITY');entry['binding']={'ref':'grant:one','revisionRef':'fixture-r1'};run('coverage-one-record-revision',repin(m),'ONE_RECORD_SOURCE_REQUIRES_DIGEST_BINDING')
m=fresh();del m['sources']['SOURCE_AUTHORITY']['sourceRecordDigest'];sid=m['profile']['formats']['SOURCE_AUTHORITY']['schemaId'];m['schemas'][sid]={'$schema':'https://json-schema.org/draft/2020-12/schema','$id':sid,**infer(m['sources']['SOURCE_AUTHORITY'])};run('coverage-self-digest-missing',cohere(m),'SOURCE_RECORD_DIGEST_MISSING')
m=fresh();m['sources']['SOURCE_AUTHORITY']['sourceRecordDigest']='sha256:'+'0'*64;run('coverage-self-digest-mismatch',repin(m,source_digests=False),'SOURCE_RECORD_SELF_DIGEST_MISMATCH')
for field,value,code in [('resultId','result:wrong','OUTPUT_ID_MISMATCH'),('requestId','request:wrong','REQUEST_ID_MISMATCH'),('policyDigest','sha256:'+'0'*64,'POLICY_CONTENT_DIGEST_MISMATCH'),('ruleDigest','sha256:'+'0'*64,'RULE_CLOSURE_CONTENT_DIGEST_MISMATCH'),('decisionValidUntil','2026-10-21T09:00:00Z','INVALID_DECISION_INTERVAL'),('selectedPathId','path:missing','SELECTED_PATH_NOT_IN_TRACE'),('snapshotBinding',{'ref':'snapshot:wrong','revisionRef':'fixture-r1'},'OUTPUT_SOURCE_BINDING_MISMATCH')]:
 m=fresh()
 for o in outputs(m):o[field]=copy.deepcopy(value)
 run('coverage-output-'+field,repin(m),code)
m=fresh();m['sources']['RESULT']['projection']['resultId']='result:other';run('coverage-result-trace-id',repin(m),'RESULT_TRACE_ID_MISMATCH')
m=fresh();m['sources']['REQUEST']['projection']['intentBinding']={'ref':'intent:wrong','revisionRef':'fixture-r1'};run('coverage-request-intent',cohere(m),'REQUEST_INTENT_MISMATCH')
m=fresh();m['sources']['REQUEST']['projection']['effectIntentCanonicalization']='WRONG';run('coverage-intent-canonicalization',cohere(m),'INTENT_CANONICALIZATION_MISMATCH')
m=fresh();m['sources']['RULE']['projection']['intentSchema']['schemaVersion']='wrong';run('coverage-rule-intent-schema',cohere(m),'RULE_INTENT_SCHEMA_MISMATCH')
m=fresh();m['sources']['RULE']['projection']['intentSchema']['schemaDigest']='sha256:'+'0'*64
for o in outputs(m):o['intentSchema']['schemaDigest']='sha256:'+'0'*64
run('coverage-intent-schema-selection',cohere(m),'INTENT_SCHEMA_NOT_SELECTED')
for field,value,code in [('ruleRevision','fixture-r2','RULE_REVISION_BINDING_MISMATCH'),('selectedRuleId','rule:wrong','POLICY_RULE_IDENTITY_MISMATCH')]:
 m=fresh();m['sources']['RULE']['projection'][field]=value
 for o in outputs(m):o[field]=value
 run('coverage-rule-'+field,cohere(m),code)
m=fresh();m['sources']['TRACE']['projection']['paths']*=2;run('coverage-duplicate-path',cohere(m),'DUPLICATE_PATH_ID')
m=fresh()
for p in selected(m):p['pathDisposition']='PATH_DENY'
run('coverage-selected-not-allow',cohere(m),'SELECTED_PATH_NOT_SUCCESSFUL')
m=fresh()
for p in selected(m):p['authoritySubjectBasisRefs'].pop(0)
run('coverage-trace-basis-closure',cohere(m),'TRACE_PATH_BASIS_CLOSURE_MISMATCH')
m=fresh()
for p in selected(m):p['basis'][0]['artifactFamily']='OTHER'
run('coverage-trace-source',cohere(m),'TRACE_PATH_SOURCE_MISMATCH')
m=fresh();next(x for x in m['context']['sources'] if x['key']=='visibility:AUTHENTICATED_PRINCIPAL')['artifactFamily']='OTHER';run('coverage-visibility-family',cohere(m),'VISIBILITY_FAMILY_MISMATCH')
m=fresh('basis-4-party')
for p in selected(m):p['sourceRecordBinding']=next(x['binding'] for x in p['basis'] if x['role']=='DELEGATION_GRANT');p['canonicalTuple']['sourceRecordId']=p['sourceRecordBinding']['ref']
run('coverage-path-source-authority',cohere(m),'PATH_SOURCE_AUTHORITY_MISMATCH')
for name,path_type,code in [('basis-1-party','ROLE_TARGETED_GRANT','DIRECT_PATH_TYPE_MISMATCH'),('basis-1-role','DIRECT_PARTY_GRANT','ROLE_PATH_TYPE_MISMATCH'),('basis-4-party','DIRECT_PARTY_GRANT','DELEGATION_PATH_TYPE_MISMATCH')]:
 m=fresh(name)
 for p in selected(m):p['pathType']=path_type;p['canonicalTuple']['pathTypeOrder']=PATHS.index(path_type)
 run('coverage-path-type-'+name,cohere(m),code)
m=fresh();m['sources']['NATURAL_PERSON_PARTY']['recordId']='party:other';m['sources']['NATURAL_PERSON_PARTY']['projection']['partyRef']='party:other';rebind_key(m,'NATURAL_PERSON_PARTY',{'ref':'party:other','revisionRef':'fixture-r1'});m['sources']['PRINCIPAL_RESOLUTION']['projection']['principalPartyRef']='party:other';run('coverage-self-party',cohere(m),'SELF_PARTY_MISMATCH')
m=fresh('basis-3-party');m['sources']['AUTHORITY_SUBJECT_PARTY']['recordId']='party:other';m['sources']['AUTHORITY_SUBJECT_PARTY']['projection']['partyRef']='party:other';rebind_key(m,'AUTHORITY_SUBJECT_PARTY',{'ref':'party:other','revisionRef':'fixture-r1'})
for p in selected(m):p['authoritySubjectPartyRef']='party:other'
run('coverage-direct-agent-party',cohere(m),'DIRECT_AGENT_PARTY_MISMATCH')
for label,refs,code in [('missing',[],'DELEGATION_SOURCE_AUTHORITY_MISMATCH'),('unresolved',['grant:one','grant:other'],'DELEGATION_SOURCE_REF_UNRESOLVED')]:
 m=fresh('basis-4-party');m['sources']['DELEGATION_GRANT']['projection']['sourceAuthorityGrantRefs']=refs;run('coverage-delegation-sources-'+label,cohere(m),code)
m=fresh('basis-4-party')
for p in selected(m):p['delegationSourceBindings']=[];p['canonicalTuple']['delegationSourceRecordIds']=[]
run('coverage-delegation-tuple',cohere(m),'DELEGATION_TUPLE_BINDING_MISSING')
m=fresh();m['sources']['UNUSED_REQUEST_ALIAS']=copy.deepcopy(m['sources']['REQUEST']);entry=copy.deepcopy(next(x for x in m['context']['sources'] if x['key']=='REQUEST'));entry['key']='UNUSED_REQUEST_ALIAS';m['context']['sources'].append(entry);run('coverage-unused-source',cohere(m),'UNUSED_DECLARED_SOURCE')

result={'status':'AUTHOR_SIDE_TARGETED_REGRESSIONS','cases':len(rows),'matched':sum(r['matched'] for r in rows),'failed':sum(not r['matched'] for r in rows),'results':rows,'next':'Review exact error witnesses and mutation evidence before sealing.'};(H/'targeted-results.json').write_bytes(raw(result));print(json.dumps({k:v for k,v in result.items() if k!='results'},indent=2));raise SystemExit(bool(result['failed']))
