"""Conditional assertion-act verification with independently selected input pins.

This supplies no authorization decision, actual source identity, clock trust or
runtime admission. The authorization-selected path source interface remains open.
"""
from pathlib import Path
import argparse,json,re,sys
import act_common
from act_common import InputFault,sha,strict,load_jcs,pointer,date_time,top_fields,report_matches
import act_report_contract
from act_report_contract import REPORT_SCHEMA

PACKAGE=Path(__file__).resolve().parent
CID='ofarm.assertion-act-evidence.v0.1'
ACT_FIELDS=['assertedAt','assertionActPosture','assertionActEvidenceBinding']
ROLES=['PREEXISTING_SOURCE_POLICY','FIXED_SUBMITTED_CONTENT','PREEXISTING_PARTY_BASIS']
POSTURES=['TRUSTED_ONLINE_SUBMISSION','VERIFIED_OFFLINE_SUBMISSION']
SOURCE_KINDS=['TRUSTED_RUNTIME_SUBMISSION_OBSERVATION','IMMUTABLE_OFFLINE_ASSERTION_ACT']
RULES=['PACKAGE_CLOSURE','STRICT_JSON','INDEPENDENT_SELECTION','PINNED_INTENT_PROFILE','PINNED_SCHEMAS','CONTRACT_AND_POLICY','EXACT_ACT_SOURCE','ACCOUNTABLE_PARTY_AND_BASIS','CANONICAL_SOURCE_TIME','EXACT_RENDERED_CONTENT','COMPLETE_INTENT_PROJECTION','ORIGINAL_SOURCE_BYTES','POSTURE_AND_BINDING','CYCLE_FREE_DECLARED_INPUTS']
GAPS=['AUTHORIZATION_SELECTED_PATH_SOURCE_CONTRACT_UNIDENTIFIED','RUNTIME_SOURCE_IDENTITY_NOT_ESTABLISHED','TIMESTAMP_TRUST_NOT_ESTABLISHED','RUNTIME_ADMISSION_NOT_ESTABLISHED']
QUALIFICATION='Passing comparisons assume independently selected fictional expected Party/basis, policy and source bytes. They do not prove authorization selection, actor identity, clock trust, source execution or admission.'
SCHEMA_PATHS={**{n:'schemas/'+n+'.schema.json' for n in ['act','content','context','policy','report','contract','intent_profile','wire']},'assertion':'source-contracts/AssertionRecord.v0.2.json','operationIntent':'source-contracts/OperationAssertionEffectIntent.v0.2.json','structureIntent':'source-contracts/StructureAssertionEffectIntent.v0.2.json','complianceIntent':'source-contracts/ComplianceAssertionEffectIntent.v0.2.json','event':'source-contracts/SemanticEventEnvelope.v0.1.json','measurement':'source-contracts/MeasurementEvidence.v0.1.json'}
CODE_FILES=['verify_assertion_act.py','act_common.py','act_report_contract.py']
def references_closed(schema,registry):
    def walk(v,base):
        if isinstance(v,dict):
            if '$dynamicRef' in v or '$recursiveRef' in v:return False
            for k,s in v.items():
                if k=='$ref':
                    if not isinstance(s,str):return False
                    url,_,frag=s.partition('#');target=registry.get(url or base)
                    if target is None:return False
                    if frag:
                        if not frag.startswith('/'):return False
                        try:
                            for part in frag[1:].split('/'):
                                part=part.replace('~1','/').replace('~0','~')
                                target=target[int(part)] if isinstance(target,list) else target[part]
                        except (KeyError,TypeError,ValueError,IndexError):return False
                elif not walk(s,base):return False
        elif isinstance(v,list):return all(walk(s,base) for s in v)
        return True
    return walk(schema,schema['$id'])

def _verify(act_bytes,content_bytes,rendered_bytes,intent_bytes,context_bytes,policy_bytes,source_inputs,*,trusted_pins,expected_act_selection,intent_profile_bytes,schema_bundle,package_root):
    report={'schemaVersion':'ofarm.assertionActVerificationReport.v0.1','status':'INPUT_ERROR','contractId':CID,'verificationMode':'OFFLINE_CANDIDATE_CONFORMANCE','runtimeAdmission':'NOT_ESTABLISHED','checkedRules':[],'errors':[],'result':None,'unestablishedClaims':GAPS.copy(),'qualification':QUALIFICATION}
    def error(code,doc,p='',detail=None):
        e={'code':code,'document':doc,'pointer':p}
        if detail is not None:e['detail']=detail
        report['errors'].append(e)
    def check(ok,code,doc,p=''):
        if not ok:error(code,doc,p)
        return ok
    def mark(rule):report['checkedRules'].append(rule)
    try:
        jcs=load_jcs()
        from jsonschema import Draft202012Validator,FormatChecker
        from jsonschema.exceptions import SchemaError,_WrappedReferencingError
        from referencing import Registry,Resource
        from referencing.exceptions import NoSuchResource
    except (ImportError,act_common.PackageNotFoundError,InputFault,OSError,ValueError,TypeError) as e:
        report['status']='DEPENDENCY_UNAVAILABLE';error('DEPENDENCY_UNAVAILABLE','package',detail=type(e).__name__);return report
    def dg(v):return 'sha256:'+sha(jcs.dumps(v))
    if not isinstance(trusted_pins,dict) or set(trusted_pins)!={'contractSha256','contextSha256','policySha256','intentProfileSha256'} or any(not isinstance(v,str) or re.fullmatch('[0-9a-f]{64}',v) is None for v in trusted_pins.values()):
        error('INVALID_INDEPENDENT_PINS','trustedPins');return report
    if not isinstance(source_inputs,dict) or any(not isinstance(k,str) or not isinstance(v,bytes) for k,v in source_inputs.items()):error('INVALID_SOURCE_INPUTS','sourceInputs');return report
    try:
        contract_raw=(Path(package_root)/'contract.json').read_bytes()
        if not check(sha(contract_raw)==trusted_pins['contractSha256'],'CONTRACT_PIN_MISMATCH','contract'):return report
        contract=strict(contract_raw)
        if not isinstance(contract,dict) or contract.get('contractId')!=CID or contract.get('requiredRules')!=RULES or contract.get('actFields')!=ACT_FIELDS or contract.get('actInputRoles')!=ROLES:
            error('UNSUPPORTED_CONTRACT','contract');return report
        if not check(contract.get('contractDigest')==dg({k:v for k,v in contract.items() if k!='contractDigest'}),'CONTRACT_SELF_DIGEST_MISMATCH','contract'):return report
        if not isinstance(contract.get('verificationCode'),dict) or set(contract['verificationCode'])!=set(CODE_FILES):error('CODE_CLOSURE_MISMATCH','contract');return report
        local=Path(__file__).resolve().parent
        if Path(act_common.__file__).resolve()!=local/'act_common.py' or Path(act_report_contract.__file__).resolve()!=local/'act_report_contract.py':error('HELPER_LOCATION_MISMATCH','package');return report
        for name,pin in contract['verificationCode'].items():
            if not check(sha((local/name).read_bytes())==pin,'CODE_PIN_MISMATCH','package',name):return report
        sources=contract.get('semanticSources')
        if not isinstance(sources,dict) or set(sources)!={'sources/pr11.md','sources/pr23.md'}:error('SEMANTIC_SOURCE_CLOSURE_MISMATCH','contract');return report
        for name,pin in sources.items():
            if not check(sha((Path(package_root)/name).read_bytes())==pin,'SEMANTIC_SOURCE_PIN_MISMATCH','contract',name):return report
        if not isinstance(contract.get('schemas'),dict) or set(contract['schemas'])!=set(SCHEMA_PATHS):error('SCHEMA_CLOSURE_MISMATCH','contract');return report
        schemas={};byid={}
        for key,path in SCHEMA_PATHS.items():
            binding=contract['schemas'][key]
            if not isinstance(binding,dict) or binding.get('path')!=path:error('SCHEMA_PATH_MISMATCH','contract');return report
            raw=(Path(package_root)/path).read_bytes()
            if not check(sha(raw)==binding.get('sha256'),'SCHEMA_PIN_MISMATCH',key):return report
            schema=strict(raw)
            if not isinstance(schema,dict) or schema.get('$id')!=binding.get('schemaId') or schema.get('$schema')!='https://json-schema.org/draft/2020-12/schema' or schema.get('$id') in byid:error('SCHEMA_ID_MISMATCH',key);return report
            Draft202012Validator.check_schema(schema);schemas[key]=schema;byid[schema['$id']]=schema
        if any(not references_closed(v,byid) for v in schemas.values()):error('UNPINNED_SCHEMA_REFERENCE','package');return report
        # Foreign intent declarations must match the exact retained carrier bytes.
        for key in ['operationIntent','structureIntent','complianceIntent']:
            declarations=schemas[key].get('x-ofarm-schemaDependencies')
            expected=['assertion'] if key=='operationIntent' else ['operationIntent','assertion']
            selected={schemas[k]['$id']:'sha256:'+contract['schemas'][k]['sha256'] for k in expected}
            if not isinstance(declarations,list) or len(declarations)!=len(selected) or any(not isinstance(d,dict) or d.get('digestBasis')!='EXACT_FILE_BYTES_SHA256' for d in declarations) or {d.get('schemaRef'):d.get('schemaDigest') for d in declarations}!=selected:
                error('FOREIGN_SCHEMA_DEPENDENCY_MISMATCH',key);return report
        def no_retrieve(uri):raise NoSuchResource(ref=uri)
        registry=Registry(retrieve=no_retrieve).with_resources((k,Resource.from_contents(v)) for k,v in byid.items())
    except (OSError,InputFault,ValueError,TypeError,OverflowError,KeyError,SchemaError,RecursionError) as e:
        report['status']='DEPENDENCY_UNAVAILABLE';error('PACKAGE_UNAVAILABLE_OR_INVALID','package',detail=type(e).__name__);return report
    mark('PACKAGE_CLOSURE')
    fmt=FormatChecker();fmt.checks('date-time',raises=(ValueError,TypeError))(date_time)
    def shape(key,value):
        try:errors=sorted(Draft202012Validator(schemas[key],registry=registry,format_checker=fmt).iter_errors(value),key=lambda e:(pointer(e.absolute_path),e.message))
        except (_WrappedReferencingError,RecursionError) as e:
            error('SCHEMA_EVALUATION_FAILED',key,detail=type(e).__name__);return False
        for e in errors:error('SCHEMA_INVALID',key,pointer(e.absolute_path),e.message)
        return not errors
    if not shape('contract',contract):return report
    raws=dict(act=act_bytes,content=content_bytes,rendered=rendered_bytes,intent=intent_bytes,context=context_bytes,policy=policy_bytes,intentProfile=intent_profile_bytes);values={}
    for key,raw in raws.items():
        try:v=strict(raw);dg(v);values[key]=v
        except (InputFault,ValueError,TypeError,OverflowError,RecursionError) as e:error(str(e) if isinstance(e,InputFault) else 'NON_CANONICAL_VALUE',key)
    mark('STRICT_JSON')
    if len(values)!=len(raws):return report
    check(sha(context_bytes)==trusted_pins['contextSha256'],'CONTEXT_PIN_MISMATCH','context');check(sha(policy_bytes)==trusted_pins['policySha256'],'POLICY_PIN_MISMATCH','policy');check(sha(intent_profile_bytes)==trusted_pins['intentProfileSha256'],'INTENT_PROFILE_PIN_MISMATCH','intentProfile')
    # Validate independently supplied selection against the exact owned selection shape.
    selection_schema=schemas['context']['properties']['actSelection']
    selection_errors=list(Draft202012Validator(selection_schema,registry=registry).iter_errors(expected_act_selection))
    if selection_errors:error('INVALID_ACT_SELECTION','expectedActSelection');return report
    mark('INDEPENDENT_SELECTION')
    valid=[shape(k,values[k]) for k in ['act','content','context','policy']]
    valid.append(shape('intent_profile',values['intentProfile']))
    if not all(valid) or report['errors']:report['status']='FAIL';return report
    profile=values['intentProfile']
    if not isinstance(schema_bundle,dict) or any(not isinstance(k,str) or not isinstance(v,bytes) for k,v in schema_bundle.items()):error('INVALID_PROFILE_SCHEMA_BUNDLE','schemaBundle');return report
    entries=profile['extraSchemas'];ids=[x['schemaId'] for x in entries]
    if len(ids)!=len(set(ids)) or set(ids)!=set(schema_bundle):error('PROFILE_SCHEMA_SET_MISMATCH','schemaBundle');return report
    try:
        for entry in entries:
            data=schema_bundle[entry['schemaId']]
            if not check(sha(data)==entry['sha256'],'PROFILE_SCHEMA_PIN_MISMATCH','schemaBundle',entry['schemaId']):return report
            schema=strict(data)
            if not isinstance(schema,dict) or schema.get('$id')!=entry['schemaId'] or schema.get('$schema')!='https://json-schema.org/draft/2020-12/schema':error('PROFILE_SCHEMA_ID_MISMATCH','schemaBundle');return report
            if entry['schemaId'] in byid and sha(data)!=next((x['sha256'] for x in contract['schemas'].values() if x['schemaId']==entry['schemaId']),None):error('PROFILE_SCHEMA_COLLISION','schemaBundle');return report
            Draft202012Validator.check_schema(schema);byid[entry['schemaId']]=schema
        if any(not references_closed(v,byid) for v in byid.values()):error('UNPINNED_PROFILE_SCHEMA_REFERENCE','schemaBundle');return report
        if profile['intentSchemaId'] not in byid:error('PROFILE_INTENT_SCHEMA_MISSING','intentProfile');return report
        registry=Registry(retrieve=no_retrieve).with_resources((k,Resource.from_contents(v)) for k,v in byid.items())
        schemas['selectedIntent']=byid[profile['intentSchemaId']]
    except (InputFault,ValueError,TypeError,OverflowError,KeyError,SchemaError,RecursionError) as e:
        report['status']='DEPENDENCY_UNAVAILABLE';error('PROFILE_SCHEMA_UNAVAILABLE_OR_INVALID','schemaBundle',detail=type(e).__name__);return report
    mark('PINNED_INTENT_PROFILE')
    intent=values['intent'];rendered=values['rendered']
    if not isinstance(intent,dict) or not isinstance(rendered,dict):error('EXPECTED_CONTENT_OBJECT','intent');report['status']='FAIL';return report
    valid=[shape('selectedIntent',intent),shape('wire',intent)]
    check(intent.get('schemaVersion')==profile['intentSchemaVersion'],'INTENT_SCHEMA_VERSION_MISMATCH','intent')
    if valid[1]:
        revision=profile['claimLanguageRevision']
        check(('claimLanguageRevision' not in intent['assertionBody']) if revision is None else intent['assertionBody'].get('claimLanguageRevision')==revision,'CLAIM_LANGUAGE_PROFILE_MISMATCH','intent')
    mark('PINNED_SCHEMAS')
    if not all(valid) or report['errors']:report['status']='FAIL';return report
    act,content,context,policy=(values[k] for k in ['act','content','context','policy'])
    cb={'ref':CID,'digest':contract['contractDigest']};pb={'ref':policy['policyId'],'digest':dg(policy)}
    for k,v in [('act',act),('context',context),('policy',policy),('intentProfile',profile)]:check(v['contractBinding']==cb,'CONTRACT_BINDING_MISMATCH',k,'/contractBinding')
    ipb={'ref':profile['profileId'],'digest':dg(profile)}
    for k,v in [('content',content),('context',context)]:check(v['intentProfileBinding']==ipb,'INTENT_PROFILE_BINDING_MISMATCH',k,'/intentProfileBinding')
    for k,v in [('act',act),('context',context)]:check(v['sourcePolicyBinding']==pb,'SOURCE_POLICY_BINDING_MISMATCH',k,'/sourcePolicyBinding')
    check(policy['posture']==context['expectedPosture'] and policy['sourceKind']==context['expectedSourceKind'],'SOURCE_POLICY_CONTEXT_MISMATCH','policy');mark('CONTRACT_AND_POLICY')
    check(context['actSelection']==expected_act_selection,'ACT_SELECTION_CONTEXT_MISMATCH','context','/actSelection')
    selection=expected_act_selection;binding=selection['binding']
    check(binding['ref']==act['recordId'] and selection['bytesSha256']==sha(act_bytes) and selection['valueDigest']==dg(act),'ACT_SELECTOR_MISMATCH','act')
    if 'digest' in binding:check(binding['digest']==dg(act),'ACT_BINDING_DIGEST_MISMATCH','act')
    mark('EXACT_ACT_SOURCE')
    party={'partyRef':act['accountablePartyRef'],'authoritySubjectBasis':act['authoritySubjectBasis'],'authoritySubjectBasisBindings':act['authoritySubjectBasisBindings']}
    check(party==context['expectedParty'],'ACCOUNTABLE_PARTY_OR_BASIS_MISMATCH','act');mark('ACCOUNTABLE_PARTY_AND_BASIS')
    check(act['assertedAt']==context['expectedAssertedAt']==intent['assertedAt'],'SOURCE_TIME_MISMATCH','act','/assertedAt');mark('CANONICAL_SOURCE_TIME')
    cont={'ref':content['contentId'],'digest':dg(content)}
    for k,v in [('act',act),('context',context)]:
        check(v['submittedContentBinding']==cont and v['submittedContentBytesSha256']==sha(content_bytes),'SUBMITTED_CONTENT_BINDING_MISMATCH',k)
    check(content['renderedContentBytesSha256']==context['renderedContentBytesSha256']==sha(rendered_bytes) and content['renderedContentDigest']==dg(rendered),'RENDERED_CONTENT_BINDING_MISMATCH','content');mark('EXACT_RENDERED_CONTENT')
    check(content['intentSchemaId']==context['intentSchemaId']==profile['intentSchemaId'],'INTENT_SCHEMA_SELECTION_MISMATCH','context')
    check(sha(intent_bytes)==context['intentBytesSha256'] and dg(intent)==context['intentDigest'],'INTENT_SELECTION_MISMATCH','intent')
    projected={k:v for k,v in intent.items() if k not in ACT_FIELDS}
    check(rendered==projected,'COMPLETE_CONTENT_MISMATCH','rendered')
    # Exact field fragments ensure appending act metadata does not re-render bodies.
    try:
        before=top_fields(rendered_bytes);after=top_fields(intent_bytes)
        check(all(after.get(k)==v for k,v in before.items()),'RENDERED_FIELD_BYTES_CHANGED','intent')
    except (InputFault,ValueError,TypeError,IndexError,RecursionError) as e:error('RENDERED_FIELD_EXTRACTION_FAILED','rendered',detail=type(e).__name__)
    check(not any(k in rendered for k in ACT_FIELDS),'ACT_METADATA_IN_RENDERED_CONTENT','rendered');mark('COMPLETE_INTENT_PROJECTION')
    check(content['sourceInputs']==context['selectedSourceInputs'],'SOURCE_INPUT_SELECTION_MISMATCH','content')
    entries=content['sourceInputs'];refs=[x['binding']['ref'] for x in entries]
    check(len(refs)==len(set(refs)) and set(refs)==set(source_inputs),'SOURCE_INPUT_SET_MISMATCH','sourceInputs')
    for i,entry in enumerate(entries):
        ref=entry['binding']['ref'];raw=source_inputs.get(ref)
        if raw is None:continue
        try:source=strict(raw);digest=dg(source)
        except (InputFault,ValueError,TypeError,OverflowError,RecursionError) as e:error(str(e) if isinstance(e,InputFault) else 'NON_CANONICAL_VALUE','sourceInputs',pointer([ref]));continue
        source_key,id_key=('event','semanticEventId') if entry['role']=='SEMANTIC_EVENT_ENVELOPE' else ('measurement','measurementEvidenceId')
        if not shape(source_key,source):continue
        check(source[id_key]==ref and digest==entry['valueDigest'] and sha(raw)==entry['bytesSha256'],'ORIGINAL_SOURCE_BYTES_MISMATCH','sourceInputs',pointer([ref]))
        # Revision spelling has no resolution semantics. The independently pinned
        # context selects this exact ref/selector-to-raw-bytes/JCS mapping.
        if 'digest' in entry['binding']:check(entry['binding']['digest']==digest,'SOURCE_BINDING_DIGEST_MISMATCH','sourceInputs',pointer([ref]))
        if entry['role']=='MEASUREMENT_EVIDENCE':check(entry['binding'] in intent['evidenceBindings'],'SOURCE_NOT_IN_SUBMITTED_EVIDENCE','content',pointer(['sourceInputs',i]))
        # Additional supplied event inputs may be retained evidence context. Only
        # the explicit associatedSemanticEventBinding is an event association.
    if 'associatedSemanticEventBinding' in intent:
        check(any(x['role']=='SEMANTIC_EVENT_ENVELOPE' and x['binding']==intent['associatedSemanticEventBinding'] for x in entries),'ASSOCIATED_EVENT_BYTES_MISSING','content')
    mark('ORIGINAL_SOURCE_BYTES')
    expected_kind=SOURCE_KINDS[POSTURES.index(context['expectedPosture'])]
    check(act['posture']==intent['assertionActPosture']==context['expectedPosture'] and act['sourceKind']==context['expectedSourceKind']==expected_kind,'ACT_POSTURE_MISMATCH','act')
    if act['posture']=='VERIFIED_OFFLINE_SUBMISSION':check(intent.get('assertionActEvidenceBinding')==binding,'OFFLINE_ACT_BINDING_MISMATCH','intent','/assertionActEvidenceBinding')
    else:check('assertionActEvidenceBinding' not in intent,'ONLINE_OFFLINE_BINDING_FORBIDDEN','intent')
    mark('POSTURE_AND_BINDING')
    check(act['inputRoles']==ROLES,'ACT_INPUT_ORDER_MISMATCH','act','/inputRoles')
    # The act schema has no context/intent/verdict/receipt dependency slot. The
    # content is the complete pre-act projection and sources are exact typed
    # bytes. No alias graph is traversed and no later output is accepted as input.
    identities=[act['recordId'],context['contextId'],intent['effectSubject']['subjectRef'],content['contentId'],policy['policyId']]
    forbidden_refs=set(identities)
    if 'revisionRef' in binding:forbidden_refs.add(binding['revisionRef'])
    def binding_aliases(value):
        if isinstance(value,dict):
            if 'ref' in value and ('digest' in value or 'revisionRef' in value):
                if value['ref'] in forbidden_refs or value.get('revisionRef') in forbidden_refs:return True
            return any(binding_aliases(v) for v in value.values())
        if isinstance(value,list):return any(binding_aliases(v) for v in value)
        return False
    check(len(identities)==len(set(identities)) and not (set(refs)&forbidden_refs) and not binding_aliases(rendered) and not binding_aliases(entries) and not binding_aliases(act['authoritySubjectBasisBindings']),'SELF_OR_LATER_IDENTITY_ALIAS','content')
    mark('CYCLE_FREE_DECLARED_INPUTS')
    report['status']='FAIL' if report['errors'] else 'CONDITIONAL_CONFORMANCE_PASS'
    if not report['errors']:report['result']={'accountablePartyRef':act['accountablePartyRef'],'assertedAt':act['assertedAt'],'posture':act['posture'],'intentDigest':dg(intent),'actDigest':dg(act),'contentDigest':dg(content)}
    return report

def verify(act_bytes,content_bytes,rendered_bytes,intent_bytes,context_bytes,policy_bytes,source_inputs,*,trusted_pins,expected_act_selection,intent_profile_bytes,schema_bundle,package_root=PACKAGE):
    """All expectations/pins come from independent caller selection, never act claims."""
    r=_verify(act_bytes,content_bytes,rendered_bytes,intent_bytes,context_bytes,policy_bytes,source_inputs,trusted_pins=trusted_pins,expected_act_selection=expected_act_selection,intent_profile_bytes=intent_profile_bytes,schema_bundle=schema_bundle,package_root=package_root)
    if not report_matches(REPORT_SCHEMA,r):raise RuntimeError('Internal owned report schema violation')
    return r

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for k in ['act','content','rendered','intent','context','policy','selection','source-inputs','intent-profile','schema-bundle']:p.add_argument('--'+k,type=Path,required=True)
    for k in ['contract','context','policy','intent-profile']:p.add_argument('--trusted-'+k+'-sha256',required=True)
    p.add_argument('--package-root',type=Path,default=PACKAGE);p.add_argument('--dependency-dir',type=Path);p.add_argument('--output',type=Path);a=p.parse_args()
    if a.dependency_dir:sys.path.insert(0,str(a.dependency_dir.resolve()))
    def read(path):
        try:return path.read_bytes()
        except OSError:return None
    try:
        selection=strict(read(a.selection));paths=strict(read(a.source_inputs));bundle_paths=strict(read(a.schema_bundle))
        bundle={k:read(a.schema_bundle.parent/v) for k,v in bundle_paths.items()} if isinstance(bundle_paths,dict) and all(isinstance(v,str) for v in bundle_paths.values()) else None
        inputs={k:read(a.source_inputs.parent/v) for k,v in paths.items()} if isinstance(paths,dict) and all(isinstance(v,str) for v in paths.values()) else None
    except (InputFault,ValueError,TypeError):selection=None;inputs=None;bundle=None
    r=verify(*(read(getattr(a,k)) for k in ['act','content','rendered','intent','context','policy']),inputs,trusted_pins={**{k+'Sha256':getattr(a,'trusted_'+k+'_sha256') for k in ['contract','context','policy']},'intentProfileSha256':a.trusted_intent_profile_sha256},expected_act_selection=selection,intent_profile_bytes=read(a.intent_profile),schema_bundle=bundle,package_root=a.package_root)
    rendered=json.dumps(r,indent=2,ensure_ascii=False)+'\n'
    if a.output:a.output.write_text(rendered)
    else:print(rendered,end='')
    return {'CONDITIONAL_CONFORMANCE_PASS':0,'FAIL':1,'INPUT_ERROR':2,'DEPENDENCY_UNAVAILABLE':3}[r['status']]
if __name__=='__main__':raise SystemExit(main())
