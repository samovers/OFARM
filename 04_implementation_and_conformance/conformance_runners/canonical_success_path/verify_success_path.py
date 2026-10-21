"""Original-byte API/CLI. Compares owner output; never makes authorization decisions."""
import base64,copy,json,re,sys
from pathlib import Path
from jsonschema import Draft202012Validator,FormatChecker
from referencing import Registry,Resource
from path_common import Fault,strict,sha,canonical,digest,equal,at,instant
H=Path(__file__).resolve().parent
ID='https://ofarm.dev/schema/drafts/non-default/authorization-decision-evidence/canonical-success-path/'
CORE=['REQUEST','RESULT','TRACE','POLICY','RULE','BINDING_MANIFEST','EFFECT_INTENT','DERIVED_VIEW','EVALUATION_SNAPSHOT']
PATHS=['DIRECT_PARTY_GRANT','ROLE_TARGETED_GRANT','DELEGATED_GRANT','SHARING_GRANT_ACCESS']
PARTY_ROLES={'NATURAL_PERSON_PARTY','AUTHORITY_SUBJECT_PARTY','REPRESENTED_PARTY','AGENT_PARTY','SPONSOR_PARTY'}
NOT=['AUTHORIZATION_ELIGIBILITY','PRINCIPAL_RESOLUTION_TRUST','CANDIDATE_SET_COMPLETENESS','CANONICAL_SELECTION_CORRECTNESS','OWNER_OUTPUT_RUNTIME_ORIGIN','SOURCE_CURRENTNESS_AND_MIGRATION','CP3_ADMISSION','RUNTIME_PROTECTION_OR_EFFECT_PERMISSION']

def package(root,source_root=None):
 from importlib.metadata import version
 if version('jsonschema')!='4.26.0':raise Fault('DEPENDENCY_VERSION_MISMATCH')
 root=Path(root).resolve();semantic_root=Path(source_root).resolve() if source_root is not None else root;c=strict((root/'contract.json').read_bytes());unsigned={k:v for k,v in c.items() if k!='contractDigest'}
 if digest(unsigned)!=c['contractDigest']:raise Fault('CONTRACT_DIGEST_MISMATCH')
 if set(c.get('verificationCode',{}))!={'verify_success_path.py','path_common.py'}:raise Fault('VERIFICATION_CODE_SET_MISMATCH')
 for name,h in c['verificationCode'].items():
  if sha((H/name).read_bytes())!=h:raise Fault('VERIFICATION_CODE_BYTES_MISMATCH',name)
 for p,h in c['files'].items():
  selected_root=semantic_root if p.startswith('sources/') else root;f=(selected_root/p).resolve()
  if not f.is_relative_to(selected_root) or not f.is_file() or sha(f.read_bytes())!=h:raise Fault('PACKAGE_CLOSURE_MISMATCH',p)
 return c,{n:strict((root/('schemas/'+n+'.schema.json')).read_bytes()) for n in ['types','evidence','profile','context','wire','report']}

def verify(evidence_bytes,profile_bytes,context_bytes,source_bytes,schema_bytes,*,expected_context_sha256,contract_root=H,source_root=None):
 report={'schemaVersion':'ofarm.canonicalSuccessfulPathVerificationReport.v0.1','disposition':'INPUT_ERROR','verificationScope':'SELECTED_OWNER_OUTPUT_INTEGRITY_ONLY','established':[],'notEstablished':NOT.copy(),'errors':[],'selectedParty':None,'sourceOrigin':None,'inputDigests':{},'next':'Use only as a conditional integrity comparison; the authorization owner must establish every remaining duty before any effect.'}
 def must(ok,code,p='',detail=''):
  if not ok:raise Fault(code,p,detail)
 try:
  contract,owned=package(contract_root,source_root)
  must(isinstance(expected_context_sha256,str) and re.fullmatch(r'[0-9a-f]{64}',expected_context_sha256),'INDEPENDENT_CONTEXT_DIGEST_REQUIRED')
  must(sha(context_bytes)==expected_context_sha256,'INDEPENDENT_CONTEXT_BYTES_MISMATCH')
  e,p,c=map(strict,[evidence_bytes,profile_bytes,context_bytes]);report['inputDigests']={k:sha(v) for k,v in [('evidence',evidence_bytes),('profile',profile_bytes),('context',context_bytes)]}
  reg=Registry().with_resources((s['$id'],Resource.from_contents(s)) for s in owned.values())
  def valid(value,schema_id,registry=reg):
   try:errs=list(Draft202012Validator({'$ref':schema_id},registry=registry,format_checker=FormatChecker()).iter_errors(value))
   except Exception as exc:raise Fault('SCHEMA_CLOSURE_ERROR',schema_id,str(exc)) from None
   if errs:raise Fault('SCHEMA_INVALID',schema_id,errs[0].message)
  for n,v in [('evidence',e),('profile',p),('context',c)]:valid(v,ID+n+'/v0.1')
  report['disposition']='FAIL';report['sourceOrigin']=c['sourceOrigin']
  must(c['contractDigest']==contract['contractDigest'],'SELECTED_CONTRACT_MISMATCH')
  must(sha(profile_bytes)==c['profileBytesSha256'],'SOURCE_PROFILE_BYTES_MISMATCH')
  must(equal(e['sourceProfileBinding'],c['profileBinding']),'SOURCE_PROFILE_BINDING_MISMATCH')
  must(c['profileBinding']['ref']==p['profileId'],'SOURCE_PROFILE_ID_MISMATCH')
  if 'revisionRef' in c['profileBinding']:must(c['profileBinding']['revisionRef']==p['profileRevision'],'SOURCE_PROFILE_REVISION_MISMATCH')
  else:must(c['profileBinding']['digest']==digest(p),'SOURCE_PROFILE_DIGEST_MISMATCH')
  must(p['authorizationLawSha256']==contract['authorizationLawSha256'],'SOURCE_LAW_MISMATCH')
  must(type(source_bytes)is dict and type(schema_bytes)is dict,'SOURCE_MAP_REQUIRED')
  must(set(schema_bytes)==set(p['schemaDigests']),'SCHEMA_SET_MISMATCH')
  foreign={}
  for sid,raw in schema_bytes.items():
   must(sha(raw)==p['schemaDigests'][sid],'SCHEMA_BYTES_MISMATCH',sid);s=strict(raw)
   must(s.get('$id')==sid and s.get('$schema')=='https://json-schema.org/draft/2020-12/schema','SCHEMA_ID_OR_DIALECT_MISMATCH',sid)
   must(sid not in [x['$id'] for x in owned.values()],'OWNED_SCHEMA_OVERRIDE',sid)
   Draft202012Validator.check_schema(s);foreign[sid]=s
  fullreg=reg.with_resources((sid,Resource.from_contents(s)) for sid,s in foreign.items())
  def audit_schema(v,sid,top=True):
   if isinstance(v,dict):
    must(top or '$id' not in v,'NESTED_SCHEMA_ID_NOT_SUPPORTED',sid)
    must('$dynamicRef' not in v and '$recursiveRef' not in v,'DYNAMIC_SCHEMA_REFERENCE_NOT_SUPPORTED',sid)
    if '$ref' in v:
     try:fullreg.resolver(sid).lookup(v['$ref'])
     except Exception as exc:raise Fault('UNRESOLVED_SCHEMA_REFERENCE',sid,str(exc)) from None
    for x in v.values():audit_schema(x,sid,False)
   elif isinstance(v,list):
    for x in v:audit_schema(x,sid,False)
  for sid,s in foreign.items():audit_schema(s,sid)
  for f in p['formats'].values():must(f['schemaId'] in foreign and f['schemaSha256']==p['schemaDigests'][f['schemaId']],'FORMAT_SCHEMA_NOT_SELECTED')
  catalog={x['key']:x for x in c['sources']};must(len(catalog)==len(c['sources']),'DUPLICATE_SOURCE_KEY');must(set(source_bytes)==set(catalog),'SOURCE_SET_MISMATCH')
  records={};projections={};identities={};used=set()
  for k,entry in catalog.items():
   must(entry['formatId'] in p['formats'],'UNKNOWN_SOURCE_FORMAT',k);f=p['formats'][entry['formatId']];raw=source_bytes[k]
   must(sha(raw)==entry['bytesSha256'],'SOURCE_BYTES_MISMATCH',k);v=strict(raw);must(digest(v)==entry['valueDigest'],'SOURCE_VALUE_DIGEST_MISMATCH',k);valid(v,f['schemaId'],fullreg)
   if f['identityPointer'] is None:
    must(entry['artifactFamily'] in ['EFFECT_INTENT','DERIVED_VIEW','POLICY','RULE','BINDING_MANIFEST','EVALUATION_SNAPSHOT'] and 'digest' in entry['binding'],'CONTENT_ONLY_IDENTITY_REQUIRES_DIGEST',k)
   else:must(at(v,f['identityPointer'])==entry['binding']['ref'],'SOURCE_LOGICAL_ID_MISMATCH',k)
   content=digest(v)
   if entry['artifactFamily'] in ['AUTHORITY_GRANT','DELEGATION_GRANT','SHARING_GRANT']:
    must(f['digestMode']=='SOURCE_RECORD_EXCLUDING_TOP_DIGEST','AUTHORITY_SOURCE_DIGEST_PROFILE_REQUIRED',k)
    must('digest' in entry['binding'],'ONE_RECORD_SOURCE_REQUIRES_DIGEST_BINDING',k)
   if f['digestMode']=='SOURCE_RECORD_EXCLUDING_TOP_DIGEST':
    must(isinstance(v,dict) and isinstance(v.get('sourceRecordDigest'),str),'SOURCE_RECORD_DIGEST_MISSING',k)
    content=digest({a:b for a,b in v.items() if a!='sourceRecordDigest'});must(v['sourceRecordDigest']==content,'SOURCE_RECORD_SELF_DIGEST_MISMATCH',k)
   if 'digest' in entry['binding']:must(entry['binding']['digest']==content,'SOURCE_BINDING_DIGEST_MISMATCH',k)
   identity=(entry['artifactFamily'],entry['binding']['ref'],None if entry['artifactFamily'] in ['AUTHORITY_GRANT','DELEGATION_GRANT','SHARING_GRANT'] else entry['binding'].get('revisionRef'))
   must(identity not in identities or identities[identity]==entry['bytesSha256'],'IMMUTABLE_ID_REUSED_WITH_DIFFERENT_BYTES',k);identities[identity]=entry['bytesSha256']
   records[k]=v;projections[k]=at(v,f['projectionPointer'])
  def use(k):must(k in catalog,'UNRESOLVED_SOURCE_KEY',k);used.add(k);return projections[k]
  def slot(name):return use(c['coreSources'][name])
  for role,k in c['coreSources'].items():
   use(k);must(equal(e['sources'][role],catalog[k]['binding']),'CORE_SOURCE_BINDING_MISMATCH',role)
   must(catalog[k]['artifactFamily']==role,'CORE_SOURCE_FAMILY_MISMATCH',role)
  rq,rs,tr,pol,rule,man,it,view,snap=[slot(k) for k in CORE]
  valid(rs,ID+'types/v0.1#/$defs/resultProjection');valid(tr,ID+'types/v0.1#/$defs/traceProjection')
  valid(snap,ID+'types/v0.1#/$defs/snapshotProjection')
  for field in set(rs)&set(tr):
   if field not in ['resultId','traceId']:must(equal(rs[field],tr[field]),'RESULT_TRACE_FIELD_MISMATCH',field)
  for field in ['resultId','traceId']:must(rs[field]==tr[field],'RESULT_TRACE_ID_MISMATCH',field)
  must(rs['resultId']==catalog[c['coreSources']['RESULT']]['binding']['ref'] and rs['traceId']==catalog[c['coreSources']['TRACE']]['binding']['ref'],'OUTPUT_ID_MISMATCH')
  must(rq['requestId']==rs['requestId']==catalog[c['coreSources']['REQUEST']]['binding']['ref'],'REQUEST_ID_MISMATCH')
  must(rq['actionClass']==rs['actionClass']==rule['actionClass']==c['selectedActionClass'],'SELECTED_ACTION_MISMATCH')
  must(equal(rq['intentBinding'],rs['intentBinding']),'REQUEST_INTENT_MISMATCH')
  for field,role in [('intentBinding','EFFECT_INTENT'),('policyBinding','POLICY'),('ruleBinding','RULE'),('manifestBinding','BINDING_MANIFEST'),('derivedViewBinding','DERIVED_VIEW'),('snapshotBinding','EVALUATION_SNAPSHOT')]:must(equal(rs[field],catalog[c['coreSources'][role]]['binding']),'OUTPUT_SOURCE_BINDING_MISMATCH',field)
  for field in ['policyId','policyVersion']:must(rs[field]==pol[field],'POLICY_OUTPUT_MISMATCH',field)
  must(rs['policyDigest']==digest(records[c['coreSources']['POLICY']]),'POLICY_CONTENT_DIGEST_MISMATCH')
  for field in ['selectedRuleId','ruleRevision']:must(rs[field]==rule[field],'RULE_OUTPUT_MISMATCH',field)
  must(rs['ruleDigest']==digest(records[c['coreSources']['RULE']]),'RULE_CLOSURE_CONTENT_DIGEST_MISMATCH')
  must(equal(rule['intentSchema'],rs['intentSchema']),'RULE_INTENT_SCHEMA_MISMATCH')
  isc=rs['intentSchema'];must(isc['schemaId'] in foreign and 'sha256:'+p['schemaDigests'][isc['schemaId']]==isc['schemaDigest'],'INTENT_SCHEMA_NOT_SELECTED')
  original_intent=records[c['coreSources']['EFFECT_INTENT']];valid(original_intent,isc['schemaId'],fullreg);must(original_intent['schemaVersion']==isc['schemaVersion'],'INTENT_VERSION_MISMATCH')
  must(rq['effectIntentDigest']==rs['effectIntentDigest']==digest(original_intent),'COMPLETE_INTENT_DIGEST_MISMATCH');must(rq['effectIntentCanonicalization']==rs['effectIntentCanonicalization'],'INTENT_CANONICALIZATION_MISMATCH')
  must(rs['derivedViewDigest']==digest(records[c['coreSources']['DERIVED_VIEW']]),'DERIVED_VIEW_DIGEST_MISMATCH')
  must(rs['policyId']==rs['policyBinding']['ref'] and rs['selectedRuleId']==rs['ruleBinding']['ref'],'POLICY_RULE_IDENTITY_MISMATCH')
  if 'revisionRef' in rs['ruleBinding']:must(rs['ruleRevision']==rs['ruleBinding']['revisionRef'],'RULE_REVISION_BINDING_MISMATCH')
  must(equal(man['policyBinding'],rs['policyBinding']) and equal(man['ruleBinding'],rs['ruleBinding']),'MANIFEST_POLICY_RULE_MISMATCH')
  must(equal(view['intentBinding'],rs['intentBinding']) and view['actionClass']==rs['actionClass'],'DERIVED_VIEW_SOURCE_MISMATCH')
  must(equal(snap['policyBinding'],rs['policyBinding']) and snap['authorizationEvaluatedAt']==rs['authorizationEvaluatedAt'],'EVALUATION_SNAPSHOT_CONTEXT_MISMATCH')
  for field,family in [('evidencePolicyRegistryBinding','EVIDENCE_POLICY_REGISTRY'),('sovereigntyPolicyBinding','SOVEREIGNTY_POLICY')]:
   matches=[k for k,x in catalog.items() if x['artifactFamily']==family and equal(x['binding'],snap[field])]
   must(len(matches)==1,'SNAPSHOT_REGISTRY_SOURCE_NOT_EXACTLY_RESOLVED',field);use(matches[0])
  must(instant(rs['authorizationEvaluatedAt'])<instant(rs['decisionValidUntil']),'INVALID_DECISION_INTERVAL')
  paths=tr['paths'];must(len({x['pathId'] for x in paths})==len(paths),'DUPLICATE_PATH_ID');chosen=[x for x in paths if x['pathId']==rs['selectedPathId']];must(len(chosen)==1,'SELECTED_PATH_NOT_IN_TRACE');path=chosen[0]
  for candidate in paths:
   must(equal(candidate['authoritySubjectBasisRefs'],[x['binding'] for x in candidate['basis']]),'TRACE_PATH_BASIS_CLOSURE_MISMATCH',candidate['pathId'])
   for source_binding in [candidate['sourceRecordBinding'],*candidate['delegationSourceBindings']]:
    must(any(equal(source_binding,x['binding']) and x['artifactFamily'] in ['AUTHORITY_GRANT','DELEGATION_GRANT','SHARING_GRANT'] for x in candidate['basis']),'SOURCE_TUPLE_BINDING_NOT_RESOLVED',candidate['pathId'])
   for x in candidate['basis']:
    k=x['sourceKey'];use(k);must(equal(x['binding'],catalog[k]['binding']) and x['artifactFamily']==catalog[k]['artifactFamily'],'TRACE_PATH_SOURCE_MISMATCH',k)
    vis=use(x['visibilitySourceKey']);must(equal(vis['sourceBinding'],x['binding']) and equal(vis['snapshotBinding'],rs['snapshotBinding']),'TRACE_PATH_VISIBILITY_MISMATCH',k)
  must(equal(path,rs['selectedPath']) and equal(path,e['selectedPath']),'SELECTED_PATH_CONTENT_MISMATCH');must(path['pathDisposition']=='PATH_ALLOW','SELECTED_PATH_NOT_SUCCESSFUL')
  tup=path['canonicalTuple'];ids=[b['ref'] for b in path['delegationSourceBindings']]
  must(tup=={'pathTypeOrder':PATHS.index(path['pathType']),'sourceRecordId':path['sourceRecordBinding']['ref'],'delegationSourceRecordIds':sorted(ids)},'CANONICAL_TUPLE_ENCODING_MISMATCH');must(len(ids)==len(set(ids)),'DUPLICATE_TUPLE_SOURCE')
  basis=path['basis'];must(equal(path['authoritySubjectBasisRefs'],[x['binding'] for x in basis]),'BASIS_REFERENCE_CLOSURE_MISMATCH')
  roles={}
  for x in basis:
   k=x['sourceKey'];use(k);must(equal(x['binding'],catalog[k]['binding']) and x['artifactFamily']==catalog[k]['artifactFamily'],'BASIS_SOURCE_BINDING_MISMATCH',k)
   family='PARTY' if x['role'] in PARTY_ROLES else 'PRINCIPAL' if x['role']=='AUTHENTICATED_PRINCIPAL' else 'AUTHORITY_GRANT' if x['role']=='SOURCE_AUTHORITY' else x['role']
   if x['role']!='ADDITIONAL_AUTHORITY_BASIS':must(x['artifactFamily']==family,'BASIS_ROLE_FAMILY_MISMATCH',k)
   must(x['role']=='ADDITIONAL_AUTHORITY_BASIS' or x['role'] not in roles,'DUPLICATE_BASIS_ROLE',x['role']);roles[x['role']]=k
   vis=use(x['visibilitySourceKey']);must(catalog[x['visibilitySourceKey']]['artifactFamily']=='SNAPSHOT_VISIBILITY_PROOF','VISIBILITY_FAMILY_MISMATCH',k);must(vis['sourceBinding']==x['binding'] and equal(vis['snapshotBinding'],rs['snapshotBinding']),'SNAPSHOT_VISIBILITY_LINK_MISMATCH',k)
   expected={'binding':x['binding'],'artifactFamily':x['artifactFamily'],'visibilityBinding':catalog[x['visibilitySourceKey']]['binding']}
   must(any(equal(z,expected) for z in snap['visibleBasis']),'BASIS_NOT_IN_SELECTED_SNAPSHOT',k)
  def role(n):must(n in roles,'REQUIRED_BASIS_ROLE_MISSING',n);return use(roles[n])
  def rb(n):role(n);return catalog[roles[n]]['binding']
  def rid(n):return rb(n)['ref']
  party=rid('AUTHORITY_SUBJECT_PARTY');must(party==path['authoritySubjectPartyRef'],'ACCOUNTABLE_PARTY_MISMATCH')
  principal=rid('AUTHENTICATED_PRINCIPAL');resolution=role('PRINCIPAL_RESOLUTION');must(resolution['authenticatedPrincipalRef']==principal,'PRINCIPAL_RESOLUTION_LINK_MISMATCH')
  must(equal(snap['principalResolutionBinding'],rb('PRINCIPAL_RESOLUTION')),'SNAPSHOT_PRINCIPAL_RESOLUTION_MISMATCH')
  authority=role('SOURCE_AUTHORITY');must(equal(rb('SOURCE_AUTHORITY'),path['sourceRecordBinding']),'PATH_SOURCE_AUTHORITY_MISMATCH')
  basis_kind=path['authoritySubjectBasis'];is_agent=basis_kind in ['AGENT_PARTY_DIRECT_GRANT','REPRESENTED_PARTY_EXPLICIT_DELEGATION']
  must(resolution['resolvedPrincipalKind']==('SOFTWARE_AGENT' if is_agent else 'NATURAL_PERSON'),'PRINCIPAL_BASIS_KIND_MISMATCH')
  if is_agent:
   must('cp3AuthoritySnapshotBinding' in snap and equal(snap['cp3AuthoritySnapshotBinding'],rb('CP3_AUTHORITY_SNAPSHOT')),'SNAPSHOT_CP3_BINDING_MISMATCH')
   agent=rid('AGENT_PARTY');must(resolution['principalPartyRef']==agent,'AGENT_PARTY_RESOLUTION_MISMATCH');must(role('AGENT_IDENTITY')['agentPartyRef']==agent and role('AGENT_IDENTITY')['agentInstanceRef']==principal,'AGENT_IDENTITY_LINK_MISMATCH')
   cp=role('CP3_ACTORSHIP_BINDING');env=role('CP3_AUTHORITY_ENVELOPE')
   for rec,principal_field in [(cp,'agentInstanceRef'),(env,'executingAgentInstanceRef')]:
    must(rec[principal_field]==principal and rec['agentSponsorRef']==rid('SPONSOR_PARTY') and rec['softwareAgentProfileRef']==rid('SOFTWARE_AGENT_PROFILE') and rec['authoritySnapshotRef']==rid('CP3_AUTHORITY_SNAPSHOT'),'CP3_IDENTITY_LINK_MISMATCH')
   must(env['agentActorshipBindingRef']==rid('CP3_ACTORSHIP_BINDING') and env['revocationStateRef']==rid('CP3_REVOCATION_STATE'),'CP3_EVIDENCE_LINK_MISMATCH')
   must(env['requestedActionClass']==rs['actionClass'] and env['authorizationDecisionResultRef']==rs['resultId'] and env['authorizationDecisionTraceRef']==rs['traceId'],'CP3_DECISION_LINK_MISMATCH')
   rev=role('CP3_REVOCATION_STATE');must(rev['executingAgentInstanceRef']==principal and rev['agentSponsorRef']==rid('SPONSOR_PARTY') and rev['authorityEnvelopeRef']==rid('CP3_AUTHORITY_ENVELOPE'),'CP3_REVOCATION_LINK_MISMATCH')
  else:must(resolution['principalPartyRef']==rid('NATURAL_PERSON_PARTY'),'NATURAL_PERSON_RESOLUTION_MISMATCH')
  if basis_kind=='NATURAL_PERSON_SELF':must(party==rid('NATURAL_PERSON_PARTY'),'SELF_PARTY_MISMATCH')
  elif basis_kind=='REPRESENTED_PARTY_AUTHORIZED_REPRESENTATION':
   rep=role('REPRESENTATION_BASIS');must(party==rid('REPRESENTED_PARTY') and rep['naturalPersonPartyRef']==rid('NATURAL_PERSON_PARTY') and rep['representedPartyRef']==party,'REPRESENTATION_LINK_MISMATCH')
  elif basis_kind=='AGENT_PARTY_DIRECT_GRANT':must(party==rid('AGENT_PARTY'),'DIRECT_AGENT_PARTY_MISMATCH')
  else:
   dg=role('DELEGATION_GRANT');must(party==rid('REPRESENTED_PARTY') and dg['delegatingPartyRef']==party and dg['delegatePartyRef']==rid('AGENT_PARTY'),'DELEGATION_PARTY_LINK_MISMATCH');must(path['pathType']=='DELEGATED_GRANT','DELEGATION_PATH_TYPE_MISMATCH');must(rid('SOURCE_AUTHORITY') in dg['sourceAuthorityGrantRefs'],'DELEGATION_SOURCE_AUTHORITY_MISMATCH');must(any(equal(b,rb('DELEGATION_GRANT')) for b in path['delegationSourceBindings']),'DELEGATION_TUPLE_BINDING_MISSING')
   for source_ref in dg['sourceAuthorityGrantRefs']:must(any(x['artifactFamily']=='AUTHORITY_GRANT' and x['binding']['ref']==source_ref for x in basis),'DELEGATION_SOURCE_REF_UNRESOLVED',source_ref)
  target=authority['grantTarget']
  if target['targetKind']=='PARTY':
   must(target['targetRef']==party,'AUTHORITY_TARGET_PARTY_MISMATCH')
   if basis_kind!='REPRESENTED_PARTY_EXPLICIT_DELEGATION':must(path['pathType']=='DIRECT_PARTY_GRANT','DIRECT_PATH_TYPE_MISMATCH')
  elif target['targetKind']=='ROLE_ASSIGNMENT':
   must(target['targetRef']==rid('ROLE_ASSIGNMENT') and role('ROLE_ASSIGNMENT')['partyRef']==party,'ROLE_PARTY_LINK_MISMATCH')
   if basis_kind!='REPRESENTED_PARTY_EXPLICIT_DELEGATION':must(path['pathType']=='ROLE_TARGETED_GRANT','ROLE_PATH_TYPE_MISMATCH')
  else:raise Fault('UNSUPPORTED_AUTHORITY_TARGET_KIND')
  # The complete original request/result/trace, not a projection, is hashed.
  request=records[c['coreSources']['REQUEST']];result=copy.deepcopy(records[c['coreSources']['RESULT']]);trace=copy.deepcopy(records[c['coreSources']['TRACE']])
  dr=result.pop('decisionBundleDigest');dt=trace.pop('decisionBundleDigest');bundle=digest({'schemaVersion':'ofarm.authorizationDecisionBundleDigestInput.v0.2','request':request,'result':result,'trace':trace})
  must(dr==dt==e['decisionBundleDigest']==bundle,'DECISION_BUNDLE_DIGEST_MISMATCH')
  # Extra declared sources must be named by a retained path or the snapshot;
  # they do not become hidden unvalidated evidence or selectable alternatives.
  for other in paths:
   for b in other['basis']:use(b['sourceKey']);use(b['visibilitySourceKey'])
  must(used==set(catalog),'UNUSED_DECLARED_SOURCE')
  report['disposition']='PASS';report['selectedParty']=party;report['established']=['ORIGINAL_SOURCE_BYTES_AND_SCHEMAS','COMPLETE_SELECTED_PATH_BASIS_CLOSURE','RESULT_TRACE_REQUEST_RULE_INTENT_SNAPSHOT_AGREEMENT','SELECTED_OWNER_OUTPUT_INTEGRITY_COMPARED']
 except Fault as exc:report['errors'].append({'code':exc.code,'pointer':exc.pointer,'detail':exc.detail})
 except Exception as exc:report['errors'].append({'code':'MALFORMED_SOURCE_OR_DEPENDENCY','pointer':'','detail':str(exc)})
 return report

def main():
 import argparse
 ap=argparse.ArgumentParser();ap.add_argument('--wire',required=True);ap.add_argument('--context-sha256',required=True);ap.add_argument('--contract-root',default=str(H));ap.add_argument('--source-root');args=ap.parse_args()
 try:
  w=strict(Path(args.wire).read_bytes());_,ss=package(args.contract_root,args.source_root);Draft202012Validator(ss['wire']).validate(w)
  dec=lambda x:base64.b64decode(x,validate=True)
  r=verify(dec(w['evidenceBytesBase64']),dec(w['profileBytesBase64']),dec(w['contextBytesBase64']),{k:dec(v) for k,v in w['sourceBytesBase64'].items()},{k:dec(v) for k,v in w['schemaBytesBase64'].items()},expected_context_sha256=args.context_sha256,contract_root=args.contract_root,source_root=args.source_root)
 except Exception as exc:
  r={'schemaVersion':'ofarm.canonicalSuccessfulPathVerificationReport.v0.1','disposition':'INPUT_ERROR','verificationScope':'SELECTED_OWNER_OUTPUT_INTEGRITY_ONLY','established':[],'notEstablished':NOT,'errors':[{'code':'INVALID_WIRE_OR_PACKAGE','pointer':'','detail':str(exc)}],'selectedParty':None,'sourceOrigin':None,'inputDigests':{},'next':'Supply exact original bytes and an independently selected context digest.'}
 print(json.dumps(r,ensure_ascii=False,allow_nan=False));return {'PASS':0,'FAIL':1,'INPUT_ERROR':2}[r['disposition']]
if __name__=='__main__':raise SystemExit(main())
