"""Row-specific comparisons that consume existing pinned source records."""
from decimal import Decimal
import rfc8785
from original_operand import select_operand
from common import *
from runtime_support import Schemas,exact,error,pointer,number
from intrinsics import Intrinsics
from build_canonical_inputs import IDS,ID_FIELDS
from referencing import Resource
ROW_SOURCE_ID='https://ofarm.dev/schema/drafts/non-default/assertion-domain/row-source-inputs/v0.1'
EXTRA={'traceability':('https://ofarm.dev/schema/traceabilityclaimbasis/v0.1','claimBasisId'),'lotLineage':('https://ofarm.dev/schema/lotlineagechange/v0.1','lineageChangeId'),'registry':('https://ofarm.dev/schema/externalregistryverificationtrace/v0.1','externalRegistryVerificationTraceId'),'resource':('https://ofarm.dev/schema/appliedresourceidentitypayload/v0.1','appliedresourceidentitypayloadId')}
SOURCES={**{k:(v,ID_FIELDS[k]) for k,v in IDS.items()},**EXTRA}
BRANCHES={'S01':[['extent']],'S02':[['field'],['cycle']],'S04':[['cycle']],'S06':[['traceability','lotLineage']],
 'S07':[['resource','code']],'S08':[['intent']],'S09':[['lineage']],'S10':[['code']],'S11':[['extent']],'S12':[['equipment']],'S14':[['lineage']],
 'C03':[['measurement','context']],'C04':[['measurement','context']],'C05':[['registry','codeProfile']],
 'C06':[['measurement','context'],['execution']],'C07':[['traceability']],'C08':[['decision']],'C09':[['measurement','context']],'C10':[['sufficiency']]}

def build_schema():
    defs={}
    for row,branches in BRANCHES.items():
        variants=[]
        for branch in branches:
            fields={'atom':{'$ref':SCHEMA_ID+'#/$defs/'+row},**{k:obj({'binding':BINDING,'record':{'$ref':SOURCES[k][0]}}) for k in branch}}
            if row=='C05':fields['selectedJurisdictionRef']=LOGICAL_REF
            variants.append(obj(fields))
        defs[row]=one(*variants) if len(variants)>1 else variants[0]
    put('row-source-inputs.schema.json',{'$schema':'https://json-schema.org/draft/2020-12/schema','$id':ROW_SOURCE_ID,'title':'Structural and compliance actual source consumers','$defs':defs})

class RecordComparisons:
    def __init__(self):
        self.intrinsics=Intrinsics();self.schemas=self.intrinsics.schemas
        self.rules=json.loads((HERE/'record-comparison-rules.json').read_text())['rules']
        self.definitions={v['id']:v for v in reviewed('reviewed-input/domain/inventory.json')['rows']}
        schema=json.loads((HERE/'row-source-inputs.schema.json').read_text());self.schemas.schemas[ROW_SOURCE_ID]=schema;self.schemas.registry=self.schemas.registry.with_resource(ROW_SOURCE_ID,Resource.from_contents(schema))
    def check(self,row,data):
        if row not in BRANCHES:return self.result([error('NO_SELECTED_ROW_SOURCE_BRANCH','/row')],[],[])
        errors=self.schemas.errors(ROW_SOURCE_ID,data,row)
        if errors:return self.result(errors,[],[])
        a=data['atom'];b=a['body'];errors+=self.intrinsics.check(a)['errors'];requirements=[];comparisons=[]
        def emit(code,x,y,p,equal,left=None,right=None):
            finding={'pointer':p,'code':code,'predicateId':code,'equal':equal}
            if left is not None and right is not None:
                operands={}
                for side,location,value in [('source',left,x),('destination',right,y)]:
                    parts=location.split('/')
                    if parts[1]=='rules':role='DOMAIN_COMPARISON_RULES:'+parts[2];suffix=location.removeprefix('/rules/'+parts[2]);base=self.rules[parts[2]]
                    elif parts[1]=='definitions':role='DOMAIN_DEFINITION:'+parts[2];suffix=location.removeprefix('/definitions/'+parts[2]);base=self.definitions[parts[2]]
                    elif parts[1]=='atom':role='ATOM:'+a['atomId'];suffix=location.removeprefix('/atom');base=a
                    elif parts[1] in SOURCES and parts[2] in ['record','binding']:
                        role=('RECORD_SOURCE:' if parts[2]=='record' else 'RECORD_SELECTOR:')+parts[1]
                        suffix=location.removeprefix('/'+parts[1]+'/'+parts[2]);base=data[parts[1]][parts[2]]
                    else:raise ValueError('Unknown original record operand path: '+location)
                    operand=select_operand(base,suffix,role);operands[side]=operand
                    if operand.get('valuePosture')=='ABSENT':
                        finding.setdefault('unavailableOriginalOperands',[]).append(side);continue
                    if not exact(pointer(base,suffix),value):raise ValueError('Record comparison labels a projected value as an original: '+code+':'+side)
                if all('valueDigest' in v for v in operands.values()):finding.update(**operands,disposition='PASS' if equal else 'FAIL')
                else:finding['operandAvailability']=operands
            comparisons.append(finding)
        def eq(code,x,y,p,left=None,right=None):
            equal=exact(x,y);emit(code,x,y,p,equal,left,right)
            if not equal:errors.append(error(code,p))
        def related(code,actual,claimed,left,right,okay):
            emit(code,actual,claimed,left,okay,left,right)
            if not okay:errors.append(error(code,left))
        def member(code,values,value,source_path,claim_path):
            okay=value in values;emit(code,values,value,source_path,okay,source_path,claim_path)
            if not okay:errors.append(error(code,source_path))
        def binding_array(code,values,claims,source_path,claim_path):
            okay=exact(values,[v['ref'] for v in claims])
            emit(code,values,claims,source_path,okay,source_path,claim_path)
            if not okay:errors.append(error(code,source_path))
        def need(role,p):requirements.append({'role':role,'pointer':p})
        def get(kind):
            entry=data[kind];value=entry['record'];eq('SOURCE_ID_BINDING_MISMATCH',value[SOURCES[kind][1]],entry['binding']['ref'],'/'+kind+'/binding/ref','/'+kind+'/record/'+SOURCES[kind][1],'/'+kind+'/binding/ref');need('EXACT_IMMUTABLE_SOURCE_RESOLUTION','/'+kind+'/binding');need('SOURCE_ELIGIBLE_FOR_ROW_USE:'+row,'/'+kind);return value
        def binding(field,kind):eq('ROW_SOURCE_BINDING_MISMATCH',b[field],data[kind]['binding'],'/atom/body/'+field,'/atom/body/'+field,'/'+kind+'/binding')
        def ref_field(value,claim,p,claim_path=None):eq('ROW_SOURCE_REF_MISMATCH',value,claim['ref'],p,p,claim_path+'/ref' if claim_path else None);need('EXACT_REFERENCED_IDENTITY_VERSION',p)
        def numeric(value,decimal,p,claim_path=None):
            equal=type(value) in [int,float] and Decimal(str(value)).is_finite() and Decimal(str(value))==number(decimal)
            emit('ROW_NUMERIC_SOURCE_MISMATCH',value,decimal,p,equal,p,claim_path)
            if not equal:errors.append(error('ROW_NUMERIC_SOURCE_MISMATCH',p))
        if row in ['S01','S11']:
            r=get('extent');g=r['geometryBasis']
            if row=='S01':
                ref_field(g.get('geometryRef'),b['value'],'/extent/record/geometryBasis/geometryRef','/atom/body/value');ref_field(g['coordinateReferenceSystem'],b['crs'],'/extent/record/geometryBasis/coordinateReferenceSystem','/atom/body/crs');eq('GEOMETRY_PRECISION_MISMATCH',g['geometryQualityClass'],b['precision'],'/atom/body/precision','/extent/record/geometryBasis/geometryQualityClass','/atom/body/precision');need('EXACT_GEOMETRY_BASIS_DEFINITION','/atom/body/geometryBasis')
            else:
                binding('value','extent');eq('EXTENT_ROLE_MISMATCH',r['extentRole'],b['extentRole'],'/atom/body/extentRole','/extent/record/extentRole','/atom/body/extentRole');ref_field(r['parentScope']['scopeRef'],b['parentScope'],'/extent/record/parentScope/scopeRef','/atom/body/parentScope')
                field='geometryBasisKind' if b['quality']=='OPERATOR_SKETCH' else 'geometryQualityClass';eq('EXTENT_QUALITY_MEANING_MISMATCH',g[field],b['quality'],'/atom/body/quality','/extent/record/geometryBasis/'+field,'/atom/body/quality')
                expected=self.rules[row]['durableIdentityPosture'][b['durableIdentityPosture']];eq('DURABLE_IDENTITY_POSTURE_MISMATCH',r['durableIdentityPolicy']['durableIdentityDecision'],expected,'/atom/body/durableIdentityPosture','/extent/record/durableIdentityPolicy/durableIdentityDecision','/rules/'+row+'/durableIdentityPosture/'+b['durableIdentityPosture'])
            need('EXTENT_PARENT_TIME_GEOMETRY_APPLICABILITY','/extent/record/temporalApplicability')
        elif row=='S02':
            kind='field' if 'field' in data else 'cycle';r=get(kind);eq('SUBJECT_SOURCE_IDENTITY_MISMATCH',a['scope']['subject']['subjectRef'],r['identityRecordRef'],'/atom/scope/subject/subjectRef','/atom/scope/subject/subjectRef','/'+kind+'/record/identityRecordRef')
            eq('SUBJECT_SOURCE_KIND_MISMATCH',a['scope']['subject']['subjectType'],self.rules[row]['subjectKindByCarrier'][kind],'/atom/scope/subject/subjectType','/atom/scope/subject/subjectType','/rules/'+row+'/subjectKindByCarrier/'+kind)
            if kind=='field':eq('PARENT_KIND_MISMATCH',b['parent']['kind'],self.rules[row]['fieldParentKind'],'/atom/body/parent/kind','/atom/body/parent/kind','/rules/'+row+'/fieldParentKind');ref_field(r['parentFarmIdentityRef'],b['parent']['binding'],'/field/record/parentFarmIdentityRef','/atom/body/parent/binding')
            else:member('PARENT_SCOPE_NOT_LISTED',r['parentScopeRefs'],b['parent']['binding']['ref'],'/cycle/record/parentScopeRefs','/atom/body/parent/binding/ref')
            need('PARENT_RELATION_KIND_TIME_AND_PROSPECTIVE_APPLICABILITY','/atom/scope/subject')
        elif row=='S04':
            r=get('cycle');ref_field(r['identityRecordRef'],b['attempt'],'/cycle/record/identityRecordRef','/atom/body/attempt')
            member('CROP_CYCLE_SCOPE_MISSING',r['parentScopeRefs'],b['scope']['ref'],'/cycle/record/parentScopeRefs','/atom/body/scope/ref')
            member('CROP_BINDING_MISSING',r.get('cropBindingRefs',[]),b['crop']['ref'],'/cycle/record/cropBindingRefs','/atom/body/crop/ref')
            for role in ['EXACT_CROP_ATTEMPT_ESTABLISHMENT','CROP_VARIETY_ROLE_AND_CODE_REVISION','CROP_SCOPE_TIME_APPLICABILITY']:need(role,'/atom/body')
        elif row in ['S06','C07']:
            r=get('traceability');binding('traceabilityClaimBasis' if row=='S06' else 'basis','traceability')
            eq('PHYSICAL_CONTINUITY_CLASS_MISMATCH',r['physicalContinuityClass'],b['physicalContinuityClass' if row=='S06' else 'continuityClass'],'/traceability/record/physicalContinuityClass','/traceability/record/physicalContinuityClass','/atom/body/'+('physicalContinuityClass' if row=='S06' else 'continuityClass'))
            if row=='C07':eq('TRACEABILITY_MODEL_MISMATCH',r['traceabilityModel'],b['model'],'/traceability/record/traceabilityModel','/traceability/record/traceabilityModel','/atom/body/model');need('EXACT_TRACEABILITY_CRITERION_AND_ACCOUNTING_EVIDENCE','/atom/body/criterion')
            else:
                l=get('lotLineage');refs=l.get('subjectLotRefs',[])+l.get('predecessorLotRefs',[])+l.get('successorLotRefs',[])
                related('COHORT_LINEAGE_LINK_MISSING',l,b['cohort']['ref'],'/lotLineage/record','/atom/body/cohort/ref',b['cohort']['ref'] in refs)
                cohort=b['cohort']['ref'];predecessor=cohort in l.get('predecessorLotRefs',[]);successor=cohort in l.get('successorLotRefs',[])
                basis_fields=[]
                if predecessor!=successor:
                    endpoint_field='predecessorLotRefs' if predecessor else 'successorLotRefs'
                    member('COHORT_BASIS_ENDPOINT_ROLE',l[endpoint_field],cohort,'/lotLineage/record/'+endpoint_field,'/atom/body/cohort/ref')
                    basis_fields=['preChangeClaimBasisRef' if predecessor else 'postChangeClaimBasisRef']
                elif not predecessor and cohort in l.get('subjectLotRefs',[]) and l['changeType']=='CREATE':
                    basis_fields=['postChangeClaimBasisRef']
                elif all(field in l for field in ['preChangeClaimBasisRef','postChangeClaimBasisRef']) and l['preChangeClaimBasisRef']==l['postChangeClaimBasisRef']:
                    # Phase cannot alter the logical basis when both originals
                    # explicitly name the same reference. Versions still matter.
                    basis_fields=['preChangeClaimBasisRef','postChangeClaimBasisRef']
                else:need('COHORT_CLAIM_BASIS_PHASE_SELECTION','/lotLineage/record')
                for field in basis_fields:
                    location='/lotLineage/record/'+field
                    if field in l:eq('COHORT_BASIS_ROLE_MISMATCH',l[field],b['traceabilityClaimBasis']['ref'],location,location,'/atom/body/traceabilityClaimBasis/ref')
                    else:
                        need('COHORT_SELECTED_CLAIM_BASIS_SOURCE',location)
                        emit('COHORT_SELECTED_CLAIM_BASIS_AVAILABLE',None,b['traceabilityClaimBasis']['ref'],location,False,location,'/atom/body/traceabilityClaimBasis/ref')
                # evaluatedAt records the decision's evaluation, not an effective
                # interval for this immutable cohort/basis pair at the claim time.
                need('COHORT_BASIS_EFFECTIVE_TIME_AND_ENDPOINT_VERSION','/atom/body/traceabilityClaimBasis')
                need('LOT_COHORT_BOUNDARY_AND_SELECTED_CONTINUITY_DECISION','/lotLineage')
            if r['traceabilityModel']=='DECLARED_OTHER':need('EXACT_GOVERNING_OTHER_MODEL_DEFINITION','/traceability/record/governingArtifactRefs')
        elif row in ['S07','S10']:
            code=get('code')
            if row=='S07':
                r=get('resource');ref_field(r['identityRecordRef'],b['identity'],'/resource/record/identityRecordRef','/atom/body/identity')
                member('RESOURCE_CODE_BINDING_LINK_MISSING',r.get('identityBindingRefs',[]),code['agronomicIdentityBindingId'],'/resource/record/identityBindingRefs','/code/record/agronomicIdentityBindingId')
                ref_field(code['localSubject']['subjectRef'],b['identity'],'/code/record/localSubject/subjectRef','/atom/body/identity')
                eq('ORIGINAL_INPUT_LABEL_CHANGED',code['bindingValue']['capturedLabel'],b['originalLabel'],'/atom/body/originalLabel','/code/record/bindingValue/capturedLabel','/atom/body/originalLabel');need('INPUT_FORMULATION_AND_IDENTIFIER_ROLE_DEFINITION','/atom/body')
            else:
                eq('ORIGINAL_IDENTIFIER_LABEL_CHANGED',code['bindingValue']['capturedLabel'],b['originalLexicalValue'],'/atom/body/originalLexicalValue','/code/record/bindingValue/capturedLabel','/atom/body/originalLexicalValue');ref_field(code['externalScheme']['schemeRef'],b['scheme'],'/code/record/externalScheme/schemeRef','/atom/body/scheme')
                related('BOUND_IDENTIFIER_VALUE_MISMATCH',code['bindingValue'],b['value'],'/code/record/bindingValue','/atom/body/value',b['value'] in [code['bindingValue'].get(field) for field in self.rules[row]['candidateIdentifierFields']])
                need('EXACT_NAMED_ATTRIBUTE_AND_IDENTIFIER_ROLE','/atom/body/attributeDefinition')
        elif row=='S08':
            r=get('intent');ref_field(r['targetScope']['scopeRef'],b['target'],'/intent/record/targetScope/scopeRef','/atom/body/target');known={};definition_paths={}
            for definition in reviewed('reviewed-input/domain/inventory.json')['rows']:
                if definition['id'].startswith('O'):
                    fields=definition['typedFieldsAndOperators'];token=fields.get('carrierActionType',fields.get('carrierToken',fields['activity']))
                    known[definition['conceptRevision']]=token;known[DEFINITION_PREFIX+definition['id']]=token
                    field=next(k for k in ['carrierActionType','carrierToken','activity'] if k in fields)
                    for ref in [definition['conceptRevision'],DEFINITION_PREFIX+definition['id']]:definition_paths[ref]='/definitions/'+definition['id']+'/typedFieldsAndOperators/'+field
            if b['activity'] in known:eq('CONFIGURATION_ACTIVITY_MISMATCH',r['intendedAction']['actionType'],known[b['activity']],'/intent/record/intendedAction/actionType','/intent/record/intendedAction/actionType',definition_paths[b['activity']])
            else:need('EXACT_ACTIVITY_DEFINITION_TO_CARRIER_ACTION','/atom/body/activity')
            ref_field(r['intendedAction'].get('methodRef'),b['method'],'/intent/record/intendedAction/methodRef','/atom/body/method');need('ASSIGNED_PERFORMER_AND_RESOURCE_CONFIGURATION','/atom/body')
        elif row in ['S09','S14']:
            r=get('lineage')
            if row=='S09':
                binding_array('PREDECESSOR_IDENTITIES_MISMATCH',r['oldIdentityRefs'],b['predecessors'],'/lineage/record/oldIdentityRefs','/atom/body/predecessors')
                successors=b['prospectiveSuccessors']+[x['ref'] for x in b.get('existingSuccessors',[])]
                if successors:
                    okay=exact(r['newIdentityRefs'],successors)
                    emit('SUCCESSOR_IDENTITIES_MISMATCH',r['newIdentityRefs'],b,'/lineage/record/newIdentityRefs',okay,'/lineage/record/newIdentityRefs','/atom/body')
                    if not okay:errors.append(error('SUCCESSOR_IDENTITIES_MISMATCH','/lineage/record/newIdentityRefs'))
                if b['case']=='REVISION_ONLY':eq('REVISION_CASE_MISMATCH',r['continuityOutcome'],self.rules[row]['revisionOnlyContinuity'],'/lineage/record/continuityOutcome','/lineage/record/continuityOutcome','/rules/'+row+'/revisionOnlyContinuity')
                if b['case']=='SAME_IDENTITY':related('SAME_IDENTITY_CASE_CONTINUITY_MISMATCH',r['continuityOutcome'],self.rules[row]['sameIdentityOutcomes'],
                    '/lineage/record/continuityOutcome','/rules/'+row+'/sameIdentityOutcomes',r['continuityOutcome'] in self.rules[row]['sameIdentityOutcomes'])
                if b['case'] in ['SAME_IDENTITY','REVISION_ONLY']:
                    eq('SAME_IDENTITY_CONTINUITY_CLASS_MISMATCH',r['identityContinuityClass'],self.rules[row]['sameIdentityContinuityClass'],
                        '/lineage/record/identityContinuityClass','/lineage/record/identityContinuityClass','/rules/'+row+'/sameIdentityContinuityClass')
                    # Existing carriers may omit a repeated continuing identity or
                    # repeat it in newIdentityRefs. Neither form may name a different
                    # durable identity. Revision endpoint proof remains separate.
                    related('CONTINUING_IDENTITY_SET_MISMATCH',r['newIdentityRefs'],r['oldIdentityRefs'],
                        '/lineage/record/newIdentityRefs','/lineage/record/oldIdentityRefs',set(r['newIdentityRefs']) <= set(r['oldIdentityRefs']))
                    if 'existingSuccessors' in b:
                        related('SAME_IDENTITY_CLAIM_INTRODUCES_SUCCESSOR',b['existingSuccessors'],b['predecessors'],
                            '/atom/body/existingSuccessors','/atom/body/predecessors',
                            {v['ref'] for v in b['existingSuccessors']} <= {v['ref'] for v in b['predecessors']})
                if b['case']=='SUCCESSOR_IDENTITIES':related('SUCCESSOR_CASE_CONTINUITY_MISMATCH',r['continuityOutcome'],self.rules[row]['forbiddenSuccessorOutcomes'],'/lineage/record/continuityOutcome','/rules/'+row+'/forbiddenSuccessorOutcomes',r['continuityOutcome'] not in self.rules[row]['forbiddenSuccessorOutcomes'])
                for index,edge in enumerate(r['lineageRelations']):
                    eq('LINEAGE_RELATION_KIND_MISMATCH',edge['relationType'],b['lineageRelation'],'/lineage/record/lineageRelations/'+str(index)+'/relationType','/lineage/record/lineageRelations/'+str(index)+'/relationType','/atom/body/lineageRelation')
                if b['case']=='SUCCESSOR_IDENTITIES':
                    old={v['ref'] for v in b['predecessors']};new=set(successors)
                    related('LINEAGE_PREDECESSOR_SUCCESSOR_IDENTITY_OVERLAP',b['predecessors'],b,
                        '/atom/body/predecessors','/atom/body',not bool(old & new))
                    direction=self.rules[row]['successorEdgeDirections'][b['lineageRelation']]
                    covered_old,covered_new=set(),set()
                    for index,edge in enumerate(r['lineageRelations']):
                        forward=edge['fromRef'] in new and edge['toRef'] in old
                        reverse=direction=='EITHER_DIRECTION_BETWEEN_SELECTED_ENDPOINT_SETS' and edge['fromRef'] in old and edge['toRef'] in new
                        okay=edge['relationType']==b['lineageRelation'] and (forward or reverse)
                        related('DIRECTED_LINEAGE_EDGE_ENDPOINTS_MISMATCH',edge,direction,
                            '/lineage/record/lineageRelations/'+str(index),'/rules/'+row+'/successorEdgeDirections/'+b['lineageRelation'],okay)
                        if okay:
                            covered_old.add(edge['toRef'] if forward else edge['fromRef'])
                            covered_new.add(edge['fromRef'] if forward else edge['toRef'])
                    related('LINEAGE_PREDECESSOR_EDGE_MISSING',r['lineageRelations'],b['predecessors'],
                        '/lineage/record/lineageRelations','/atom/body/predecessors',old<=covered_old)
                    related('LINEAGE_SUCCESSOR_EDGE_MISSING',r['lineageRelations'],b,
                        '/lineage/record/lineageRelations','/atom/body',new<=covered_new)
                if 'effectiveFrom' not in r:need('LINEAGE_EFFECTIVE_TIME_SOURCE','/lineage/record/effectiveFrom')
                else:
                    from time_validation import foreign_instant,foreign_seconds
                    time=a['scope']['subjectTime'];field='at' if 'at' in time else 'start'
                    try:
                        effective=foreign_instant(r['effectiveFrom'])
                        if effective['unknownLocalOffset']:need('LINEAGE_EFFECTIVE_TIME_KNOWN_OFFSET','/lineage/record/effectiveFrom')
                        else:related('LINEAGE_EFFECTIVE_TIME_AFTER_CLAIM',r['effectiveFrom'],time[field],
                            '/lineage/record/effectiveFrom','/atom/scope/subjectTime/'+field,effective['seconds']<=foreign_seconds(time[field]))
                    except (ValueError,TypeError,KeyError):errors.append(error('INVALID_LINEAGE_EFFECTIVE_TIME','/lineage/record/effectiveFrom'))
                need('EXACT_CONTINUITY_BASIS_AND_DIRECTED_ENDPOINT_VERSION_PROOF','/atom/body/basis')
            else:
                eq('STORAGE_LINEAGE_FAMILY_MISMATCH',r['subjectFamily'],self.rules[row]['lineageSubjectFamily'],'/lineage/record/subjectFamily','/lineage/record/subjectFamily','/rules/'+row+'/lineageSubjectFamily')
                related('STORAGE_LOCATION_LINEAGE_LINK_MISSING',r,b['location']['ref'],'/lineage/record','/atom/body/location/ref',b['location']['ref'] in r['oldIdentityRefs']+r['newIdentityRefs'])
                need('LOCATION_FACILITY_LAYOUT_POSITION_AND_TIME','/atom/body')
        elif row=='S12':
            r=get('equipment');ref_field(r['identityRecordRef'],b['asset'],'/equipment/record/identityRecordRef','/atom/body/asset');binding_array('INSPECTION_EVIDENCE_REFS_MISMATCH',r.get('inspectionEvidenceRefs',[]),b['inspectionEvidence'],'/equipment/record/inspectionEvidenceRefs','/atom/body/inspectionEvidence');need('ASSET_CONFIGURATION_AND_INSPECTION_DATE_IDENTITY','/atom/body/configuration')
        elif row in ['C03','C04','C06','C09'] and 'measurement' in data:
            m=get('measurement');c=get('context')
            role=b['operand']['source'] if row=='C04' else b.get('measurementSource') if row!='C06' else b['rateSource'].get('measurementSource')
            if role is None:errors.append(error('ROW_MEASURED_SOURCE_ROLE_REQUIRED','/atom/body'));return self.result(errors,comparisons,requirements)
            role_path='/atom/body/'+('operand/source' if row=='C04' else 'rateSource/measurementSource' if row=='C06' else 'measurementSource')
            eq('MEASUREMENT_BINDING_MISMATCH',role['measurementBinding'],data['measurement']['binding'],role_path+'/measurementBinding',role_path+'/measurementBinding','/measurement/binding');eq('CONTEXT_BINDING_MISMATCH',role['contextBinding'],data['context']['binding'],role_path+'/contextBinding',role_path+'/contextBinding','/context/binding')
            if 'agronomicObservationContextRef' in m:
                eq('MEASUREMENT_CONTEXT_LINK_MISMATCH',m['agronomicObservationContextRef'],c['agronomicObservationContextId'],'/measurement/record/agronomicObservationContextRef','/measurement/record/agronomicObservationContextRef','/context/record/agronomicObservationContextId')
            else:member('MEASUREMENT_CONTEXT_LINK_MISSING',c.get('measurementEvidenceRefs',[]),m['measurementEvidenceId'],'/context/record/measurementEvidenceRefs','/measurement/record/measurementEvidenceId')
            eq('MEASUREMENT_PROPERTY_CONTEXT_MISMATCH',m['observedPropertyRef'],c['observedPropertyRef'],'/context/record/observedPropertyRef','/measurement/record/observedPropertyRef','/context/record/observedPropertyRef')
            for index,p in enumerate(role['qualificationPointers']):
                left='/measurement/record'+p;right=role_path+'/qualificationPointers/'+str(index)
                try:operand=select_operand(m,p,'MEASUREMENT')
                except ValueError:
                    errors.append(error('SOURCE_QUALIFICATION_POINTER_MISSING',p))
                    # Invalid syntax has no meaningful missing path.
                    continue
                if operand.get('valuePosture')=='ABSENT':
                    errors.append(error('SOURCE_QUALIFICATION_POINTER_MISSING',p))
                    emit('SOURCE_QUALIFICATION_POINTER_MISSING',None,p,p,False,left,right)
                else:
                    emit('SOURCE_QUALIFICATION_POINTER_MISSING',pointer(m,p),p,p,True,left,right)
            if row in ['C03','C06']:
                eq('MEASURED_NUMERIC_POINTER_MISMATCH',role['resultPointer'],self.rules[row]['numericResultPointer'],role_path+'/resultPointer',role_path+'/resultPointer','/rules/'+row+'/numericResultPointer');eq('MEASURED_NUMERIC_KIND_MISMATCH',m['result']['resultKind'],self.rules[row]['numericResultKind'],'/measurement/record/result/resultKind','/measurement/record/result/resultKind','/rules/'+row+'/numericResultKind')
                if row=='C06' and m['result']['resultKind']=='NUMERIC':
                    rate=b['rate'];numeric(m['result']['numericValue'],rate['decimal'],'/measurement/record/result/numericValue','/atom/body/rate/decimal')
                    for field,sourcefield in [('quantityKind','quantityKindRef'),('unit','unitRef')]:eq('RATE_QUANTITY_CONTEXT_MISMATCH',rate[field],m['result'].get(sourcefield),'/atom/body/rate/'+field,'/atom/body/rate/'+field,'/measurement/record/result/'+sourcefield)
            elif row=='C04':
                o=b['operand'];r=m['result'];eq('C04_FULL_RESULT_POINTER_REQUIRED',role['resultPointer'],self.rules[row]['fullResultPointer'],'/atom/body/operand/source/resultPointer','/atom/body/operand/source/resultPointer','/rules/'+row+'/fullResultPointer');eq('C04_RESULT_KIND_MISMATCH',o['resultKind'],r['resultKind'],'/atom/body/operand/resultKind','/atom/body/operand/resultKind','/measurement/record/result/resultKind')
                if o['resultKind']==r['resultKind']=='CENSORED_NUMERIC':
                    eq('CENSORING_QUALIFIER_CHANGED',o['qualifier'],r['censoringQualifier'],'/atom/body/operand/qualifier','/atom/body/operand/qualifier','/measurement/record/result/censoringQualifier');numeric(r['detectionLimit']['value'],o['limit']['decimal'],'/measurement/record/result/detectionLimit/value','/atom/body/operand/limit/decimal')
                    for field,sourcefield in [('quantityKind','quantityKindRef'),('unit','unitRef')]:eq('CENSOR_LIMIT_CONTEXT_MISMATCH',o['limit'][field],r['detectionLimit'][sourcefield],'/atom/body/operand/limit/'+field,'/atom/body/operand/limit/'+field,'/measurement/record/result/detectionLimit/'+sourcefield)
                    need('EXACT_LIMIT_SCALAR_LEXICAL_AND_QUALIFIER_PROVENANCE','/atom/body/operand/limit/provenance')
                elif o['resultKind']==r['resultKind']=='NUMERIC':
                    numeric(r['numericValue'],o['quantity']['decimal'],'/measurement/record/result/numericValue','/atom/body/operand/quantity/decimal')
                    for field,sourcefield in [('quantityKind','quantityKindRef'),('unit','unitRef')]:eq('C04_NUMERIC_CONTEXT_MISMATCH',o['quantity'][field],r[sourcefield],'/atom/body/operand/quantity/'+field,'/atom/body/operand/quantity/'+field,'/measurement/record/result/'+sourcefield)
                elif o['resultKind']==r['resultKind']=='CODED':ref_field(r['codedValueRef'],o['codedValue'],'/measurement/record/result/codedValueRef','/atom/body/operand/codedValue')
                elif o['resultKind']==r['resultKind']=='QUALITATIVE':eq('QUALITATIVE_TEXT_CHANGED',o['originalText'],r['qualitativeValue'],'/measurement/record/result/qualitativeValue','/atom/body/operand/originalText','/measurement/record/result/qualitativeValue')
                need('SELECTED_RESULT_ADMISSIBLE_SET_MAPPING_AND_THRESHOLD_PROVENANCE','/atom/body')
            need('EXACT_PROPERTY_METHOD_USE_SUBJECT_RELATION_AND_COMPLETE_QUALIFICATIONS','/atom/body')
        elif row=='C06':
            r=get('execution');p=b['rateSource']['valuePointer'];import re
            if b['rateSource']['sourceKind']!='OPERATION_PARAMETER' or not re.fullmatch(r'/actualQuantityParameters/(0|[1-9][0-9]*)/value',p):errors.append(error('RATE_EXECUTION_SOURCE_POINTER_MISMATCH','/atom/body/rateSource'))
            else:
                try:q=pointer(r,p.rsplit('/',1)[0])
                except ValueError:q=None
                if q is None:
                    errors.append(error('RATE_PARAMETER_NOT_FOUND',p))
                    emit('RATE_PARAMETER_NOT_FOUND',None,p,p,False,'/execution/record'+p,'/atom/body/rateSource/valuePointer')
                else:
                    numeric(q['value'],b['rate']['decimal'],'/execution/record'+p,'/atom/body/rate/decimal')
                    for field,sourcefield in [('quantityKind','quantityKindRef'),('unit','unitRef')]:eq('RATE_QUANTITY_CONTEXT_MISMATCH',b['rate'][field],q[sourcefield],p+'/'+sourcefield,'/atom/body/rate/'+field,'/execution/record'+p.rsplit('/',1)[0]+'/'+sourcefield)
                    related('RATE_PARAMETER_ROLE_MISMATCH',q['parameterRole'],self.rules[row]['allowedOperationParameterRoles'],
                        '/execution/record'+p.rsplit('/',1)[0]+'/parameterRole','/rules/'+row+'/allowedOperationParameterRoles',q['parameterRole'] in self.rules[row]['allowedOperationParameterRoles'])
                    qpath='/execution/record'+p.rsplit('/',1)[0]
                    for sourcefield,claimfield,code,role in [
                        ('qualifier','qualifier','RATE_SOURCE_QUALIFIER_CHANGED','RATE_ORIGINAL_QUALIFIER_SOURCE'),
                        ('reportedValue','originalLexicalValue','RATE_ORIGINAL_REPORTED_VALUE_CHANGED','RATE_ORIGINAL_REPORTED_VALUE_SOURCE')]:
                        if sourcefield in q:
                            eq(code,q[sourcefield],b['rate'][claimfield],qpath+'/'+sourcefield,qpath+'/'+sourcefield,'/atom/body/rate/'+claimfield)
                        else:
                            need(role,qpath+'/'+sourcefield)
                            emit(code,None,b['rate'][claimfield],qpath+'/'+sourcefield,False,qpath+'/'+sourcefield,'/atom/body/rate/'+claimfield)
                    # Only the direct PRODUCT role has an established mapping to
                    # this body's product binding. Other material roles require
                    # their own condition meaning, never an inferred conversion.
                    direct=q.get('materialRole')==self.rules[row]['directProductMaterialRole']
                    emit('RATE_MATERIAL_ROLE_DIRECT_PRODUCT',q.get('materialRole'),self.rules[row]['directProductMaterialRole'],qpath+'/materialRole',direct,
                        qpath+'/materialRole','/rules/'+row+'/directProductMaterialRole')
                    if not direct:need('RATE_MATERIAL_ROLE_TO_LABEL_PRODUCT_MEANING:'+q.get('materialRole','ABSENT'),qpath+'/materialRole')
                    if 'reportedUnitLabel' in q or 'originalUnitText' in b['rate']:
                        if 'reportedUnitLabel' in q and 'originalUnitText' in b['rate']:
                            eq('RATE_ORIGINAL_UNIT_TEXT_CHANGED',q['reportedUnitLabel'],b['rate']['originalUnitText'],qpath+'/reportedUnitLabel',qpath+'/reportedUnitLabel','/atom/body/rate/originalUnitText')
                        else:
                            need('RATE_ORIGINAL_UNIT_TEXT_RETENTION',qpath+'/reportedUnitLabel')
                            emit('RATE_ORIGINAL_UNIT_TEXT_AVAILABLE',q.get('reportedUnitLabel'),b['rate'].get('originalUnitText'),qpath+'/reportedUnitLabel',False,
                                qpath+'/reportedUnitLabel','/atom/body/rate/originalUnitText')
                    ref_field(q.get('materialRef'),b['product'],'/execution/record'+p.rsplit('/',1)[0]+'/materialRef','/atom/body/product')
            eq('RATE_SOURCE_BINDING_MISMATCH',b['rateSource']['sourceBinding'],data['execution']['binding'],'/atom/body/rateSource/sourceBinding','/atom/body/rateSource/sourceBinding','/execution/binding');need('EXACT_LABEL_CONDITION_PRODUCT_CROP_TARGET_TIME_AND_BASIS','/atom/body/condition')
        elif row=='C05':
            r=get('registry');p=get('codeProfile');binding('verificationTrace','registry');binding('profile','codeProfile')
            eq('REGISTRY_PROFILE_LINK_MISMATCH',r['profileRef'],p['agronomicCodeBindingProfileId'],'/registry/record/profileRef','/registry/record/profileRef','/codeProfile/record/agronomicCodeBindingProfileId');eq('PROFILE_JURISDICTION_MISMATCH',p['profileScope']['jurisdiction'],b['jurisdiction'],'/codeProfile/record/profileScope/jurisdiction','/codeProfile/record/profileScope/jurisdiction','/atom/body/jurisdiction');eq('TRACE_JURISDICTION_MISMATCH',r['traceJurisdictionRef'],data['selectedJurisdictionRef'],'/registry/record/traceJurisdictionRef')
            eq('PRODUCT_IDENTITY_PURPOSE_MISMATCH',r['verificationPurpose'],self.rules[row]['verificationPurpose'],'/registry/record/verificationPurpose','/registry/record/verificationPurpose','/rules/'+row+'/verificationPurpose');eq('OFFICIAL_IDENTIFIER_MISMATCH',r['selectedExternalId'].get('externalId'),b['officialIdentifier'],'/registry/record/selectedExternalId/externalId','/registry/record/selectedExternalId/externalId','/atom/body/officialIdentifier');binding_array('SOURCE_SNAPSHOT_REFS_MISMATCH',r['snapshotRefs'],b['snapshots'],'/registry/record/snapshotRefs','/atom/body/snapshots')
            if b['allegedOutcome']=='SATISFIED':
                eq('AMBIGUOUS_PRODUCT_SELECTION',r['candidateCount'],self.rules[row]['unambiguousCandidateCount'],'/registry/record/candidateCount','/registry/record/candidateCount','/rules/'+row+'/unambiguousCandidateCount')
                related('COMMERCIAL_OR_SUBSTANCE_ID_NOT_AUTHORISATION',r['selectedExternalId']['externalIdRole'],self.rules[row]['authorizationIdentifierRoles'],'/registry/record/selectedExternalId/externalIdRole','/rules/'+row+'/authorizationIdentifierRoles',r['selectedExternalId']['externalIdRole'] in self.rules[row]['authorizationIdentifierRoles'])
                eq('OWNER_TRACE_DOES_NOT_REPORT_PASS',r['finalOutcome'],self.rules[row]['reportedSuccessfulOutcome'],'/registry/record/finalOutcome','/registry/record/finalOutcome','/rules/'+row+'/reportedSuccessfulOutcome')
            need('OWNER_TRACE_AUTHENTICITY_CURRENTNESS_AND_CONDITIONAL_LABEL_CERTIFICATE','/registry')
        elif row=='C08':
            r=get('decision');binding('decision','decision');need('EXACT_DECISION_FINDING_RULE_ARTIFACT_SUBJECT_AND_EFFECT','/atom/body/finding')
        elif row=='C10':
            r=get('sufficiency')
            member('SUFFICIENCY_POLICY_LINK_MISSING',r['governingPolicyRefs'],b['policy']['ref'],'/sufficiency/record/governingPolicyRefs','/atom/body/policy/ref')
            need('SUFFICIENCY_REQUIRED_USE_EVIDENCE_SET_MISSING_KINDS_AND_OUTCOME_MAPPING','/atom/body')
        return self.result(errors,comparisons,requirements)
    @staticmethod
    def result(errors,comparisons,requirements):return {'scope':'ROW_FIELDS_AGAINST_ACTUAL_SOURCE_CARRIERS','disposition':'COMPARISON_FAILED' if errors else 'COMPARISONS_SATISFIED_WITH_OWNER_ROLES_REQUIRED','errors':errors,'comparisons':comparisons,'requiredOwnerRoles':requirements}

if __name__=='__main__':build_schema();print(json.dumps({'structuralComplianceSourceRows':len(BRANCHES),'schemaId':ROW_SOURCE_ID}))
