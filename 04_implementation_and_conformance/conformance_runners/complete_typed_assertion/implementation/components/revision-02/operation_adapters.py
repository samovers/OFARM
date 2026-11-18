"""Operation rows consume existing intent/execution carrier fields explicitly."""
from decimal import Decimal
import hashlib
import re
import rfc8785
from original_operand import select_operand
from time_validation import foreign_instant,foreign_seconds
from common import *
from runtime_support import Schemas,Values,exact,number,error,pointer
from intrinsics import Intrinsics
from build_canonical_inputs import IDS,ID_FIELDS,CANONICAL_ID
OP_INPUT_ID='https://ofarm.dev/schema/drafts/non-default/assertion-domain/operation-source-inputs/v0.1'

def build_schema():
    rows=[r for r in reviewed('reviewed-input/domain/inventory.json')['rows'] if r['id'].startswith('O')]
    defs={}
    for row in rows:
        variants=[]
        for kind in ['intent','execution']:
            fields={'atom':{'$ref':SCHEMA_ID+'#/$defs/'+row['id']},'sourceKind':const(kind),'source':{'$ref':CANONICAL_ID+'#/$defs/'+kind+'Source'},
                'quantitySelections':arr(obj({'parameterId':TEXT,'sourceIndex':{'type':'integer','minimum':0}}),0,True)}
            if kind=='execution':
                fields['performerPointer']=enum(['/actor/actorPartyRef','/actor/operatorPartyRef','/actor/contractorPartyRef'])
                fields['assetTargetRole']=enum(['equipmentRef','tractorOrPowerUnitRef','implementRef','controllerRef'])
            variants.append(obj(fields,[k for k in fields if k!='assetTargetRole']))
        defs[row['id']]=one(*variants)
    put('operation-source-inputs.schema.json',{'$schema':'https://json-schema.org/draft/2020-12/schema','$id':OP_INPUT_ID,'title':'27 operation source consumers','$defs':defs})

def selected_original_alias(source, binding, resolved_sources):
    """Resolve an alias from the verifier's already protected original inputs.

    Standalone callers get strict selector equality unless they supply the
    actual resolved originals. No alias flag or expected comparison is accepted.
    This compares original identity, raw hash, value hash and record value;
    eligible use remains outside this carrier comparison.
    """
    selected=[v for v in resolved_sources if exact(v.get('binding'),source['binding']) and exact(v.get('record'),source['record'])]
    aliases=[v for v in resolved_sources if exact(v.get('binding'),binding)]
    if len(selected)!=1 or len(aliases)!=1:return None
    left,right=selected[0],aliases[0]
    if left['binding']['ref']!=right['binding']['ref']:return None
    raw_hash=left.get('rawSha256');value_hash='sha256:'+hashlib.sha256(rfc8785.dumps(source['record'])).hexdigest()
    if not isinstance(raw_hash,str) or re.fullmatch('[a-f0-9]{64}',raw_hash) is None:return None
    if right.get('rawSha256')!=raw_hash or left.get('valueDigest')!=value_hash or right.get('valueDigest')!=value_hash:return None
    if not exact(right.get('record'),source['record']):return None
    return right


class OperationAdapters:
    def __init__(self):
        self.intrinsics=Intrinsics();self.schemas=self.intrinsics.schemas;self.values=self.intrinsics.values
        from referencing import Resource
        schema=json.loads((HERE/'operation-source-inputs.schema.json').read_text())
        self.schemas.schemas[OP_INPUT_ID]=schema;self.schemas.registry=self.schemas.registry.with_resource(OP_INPUT_ID,Resource.from_contents(schema))
        self.rows={r['id']:r for r in reviewed('reviewed-input/domain/inventory.json')['rows'] if r['id'].startswith('O')}
    def check(self,row,data,*,resolved_sources=()):
        errors=self.schemas.errors(OP_INPUT_ID,data,row)
        if errors:return self.result(errors,[],[])
        errors+=self.intrinsics.check(data['atom'])['errors'];a=data['atom'];b=a['body'];t=a['scope']['subjectTime'];kind=data['sourceKind'];src=data['source'];r=src['record'];requirements=[];comparisons=[]
        origins={'OPERATION_SOURCE':r,'ATOM:'+a['atomId']:a,'DOMAIN_DEFINITION:'+row:self.rows[row],
                 'OPERATION_SOURCE_SELECTOR':src['binding']}
        def emit(code,actual,expected,path,equal,source=None,destination=None):
            finding={'code':code,'predicateId':code,'pointer':path,'equal':equal}
            if source is not None and destination is not None:
                operands={}
                for side,origin,value in [('source',source,actual),('destination',destination,expected)]:
                    role,location=origin
                    operand=select_operand(origins[role],location,role);operands[side]=operand
                    if operand.get('valuePosture')=='ABSENT':
                        finding.setdefault('unavailableOriginalOperands',[]).append(side);continue
                    if not exact(pointer(origins[role],location),value):raise ValueError('Operation comparison labels a projected value as an original: '+code+':'+side)
                if all('valueDigest' in v for v in operands.values()):finding.update(**operands,disposition='PASS' if equal else 'FAIL')
                else:finding['operandAvailability']=operands
            comparisons.append(finding)
        def claim(path):return ('ATOM:'+a['atomId'],path)
        def original(path):return ('OPERATION_SOURCE',path.removeprefix('/source/record'))
        def definition(field):return ('DOMAIN_DEFINITION:'+row,'/typedFieldsAndOperators/'+field)
        def eq(code,actual,expected,path,destination=None,source=None,equal=None):
            same=exact(actual,expected) if equal is None else equal;emit(code,actual,expected,path,same,source or original(path),destination)
            if not same:errors.append(error(code,path))
        def need(role,path):requirements.append({'role':role,'pointer':path})
        eq('SOURCE_ID_BINDING_MISMATCH',r[ID_FIELDS[kind]],src['binding']['ref'],'/source/binding/ref',
           ('OPERATION_SOURCE_SELECTOR','/ref'),original('/'+ID_FIELDS[kind]))
        eq('SOURCE_POSTURE_MISMATCH',kind,'intent' if b['claimPosture']=='INTENDED' else 'execution','/sourceKind')
        types=self.rows[row]['typedFieldsAndOperators'];action='intendedAction' if kind=='intent' else 'actualAction';time='intendedTimeWindow' if kind=='intent' else 'effectiveTimeInterval'
        action_type=types.get('carrierActionType',types.get('carrierToken',types['activity']))
        action_field=next(k for k in ['carrierActionType','carrierToken','activity'] if k in types)
        eq('SOURCE_ACTION_TYPE_MISMATCH',r[action]['actionType'],action_type,'/source/record/'+action+'/actionType',definition(action_field))
        intervention=types.get('carrierInterventionKind',types.get('interventionKind'))
        if intervention:
            actual=r.get('interventionKind') if kind=='intent' else r[action].get('interventionKind')
            eq('SOURCE_INTERVENTION_KIND_MISMATCH',actual,intervention,'/source/record/'+('' if kind=='intent' else action+'/')+'interventionKind',
               definition('carrierInterventionKind' if 'carrierInterventionKind' in types else 'interventionKind'))
        target=r.get('targetScope') if kind=='intent' else r['executionExtent']['targetScope']
        if b['target']['kind'] in ['EQUIPMENT','TOOL'] and kind=='execution':
            if 'assetTargetRole' not in data:errors.append(error('EXACT_ASSET_TARGET_ROLE_REQUIRED','/assetTargetRole'))
            else:eq('SOURCE_ASSET_TARGET_MISMATCH',r.get('equipment',{}).get(data['assetTargetRole']),b['target']['binding']['ref'],'/source/record/equipment/'+data['assetTargetRole'],claim('/body/target/binding/ref'))
            need('ASSET_TARGET_TO_EXECUTION_GOVERNED_SCOPE_AND_EXTENT','/source/record/executionExtent')
        elif b['target']['kind'] in ['EQUIPMENT','TOOL','CONTAINER','STORAGE_LOCATION']:
            need('TYPED_TARGET_RELATION_NOT_REPRESENTED_BY_SOURCE_SCOPE:'+b['target']['kind'],'/source/record/targetScope')
        else:
            target_path='/source/record/targetScope' if kind=='intent' else '/source/record/executionExtent/targetScope'
            eq('SOURCE_TARGET_MISMATCH',target,{'scopeType':b['target']['kind'],'scopeRef':b['target']['binding']['ref']},target_path)
            for source_field,claim_field in [('scopeType','kind'),('scopeRef','binding/ref')]:
                eq('SOURCE_TARGET_'+source_field.upper()+'_MISMATCH',target[source_field],pointer(b['target'],'/'+claim_field),
                   target_path+'/'+source_field,claim('/body/target/'+claim_field))
        # The ordinary carrier subject may be the target rather than the
        # activity identity. This difference demands its exact relation; no
        # transitive association is inferred from a shared field or tenant.
        if r['subject']!={'subjectType':'OPERATION','subjectRef':b['activityInstance']['ref']}:need('EXACT_SOURCE_SUBJECT_TO_ACTIVITY_INSTANCE','/source/record/subject')
        if kind=='execution':
            try:actor=pointer(r,data['performerPointer'])
            except ValueError:actor=None
            eq('SOURCE_PERFORMER_REF_MISMATCH',actor,b['performedBy']['ref'],'/source/record'+data['performerPointer'],claim('/body/performedBy/ref'))
            need('PERFORMER_ROLE_IDENTIFICATION_NOT_REPORTER','/performerPointer')
            if b['extent']['posture']=='PARTIAL_TARGET_SCOPE':
                eq('SOURCE_PARTIAL_EXTENT_MISMATCH',r['executionExtent'].get('extentRef'),b['extent']['binding']['ref'],'/source/record/executionExtent/extentRef',claim('/body/extent/binding/ref'))
                if r['executionExtent']['extentClass']=='WHOLE_TARGET_SCOPE':errors.append(error('WHOLE_SOURCE_FOR_PARTIAL_CLAIM','/source/record/executionExtent/extentClass'))
            elif r['executionExtent']['extentClass']!='WHOLE_TARGET_SCOPE':errors.append(error('PARTIAL_SOURCE_FOR_WHOLE_CLAIM','/source/record/executionExtent/extentClass'))
        else:
            need('INTENDED_NAMED_PERFORMER_FROM_WORK_DEFINITION','/atom/body/performedBy')
            if b['extent']['posture']=='PARTIAL_TARGET_SCOPE':eq('SOURCE_INTENDED_EXTENT_MISMATCH',r.get('targetExtentRef'),b['extent']['binding']['ref'],'/source/record/targetExtentRef',claim('/body/extent/binding/ref'))
            elif 'targetExtentRef' in r:errors.append(error('PARTIAL_SOURCE_FOR_WHOLE_CLAIM','/source/record/targetExtentRef'))
        if t['profile'] in ['INTENDED_WINDOW','PERFORMED_INTERVAL']:
            for field in ['start','end']:
                original_time=r[time][field];location='/source/record/'+time+'/'+field
                try:
                    parsed=foreign_instant(original_time)
                    if parsed['unknownLocalOffset']:need('SOURCE_PROFILE_TIME_INSTANT_INTERPRETATION',location)
                    else:eq('SOURCE_PROFILE_TIME_MISMATCH',original_time,t[field],location,claim('/scope/subjectTime/'+field),
                            equal=parsed['seconds']==foreign_seconds(t[field]))
                except ValueError:errors.append(error('SOURCE_PROFILE_TIME_UNAVAILABLE',location))
            need('SELECTED_PAYLOAD_TIME_BASIS_INTERPRETATION','/source/record/'+time+'/timeBasis')
        else:need('INSTANT_FACET_MEASUREMENT_AT_PHENOMENON_TIME','/atom/scope/subjectTime')
        method=b['parameters'].get('method')
        if method:eq('SOURCE_METHOD_REF_MISMATCH',r[action].get('methodRef'),method['ref'],'/source/record/'+action+'/methodRef',claim('/body/parameters/method/ref'))
        # Exact work/condition meanings are not added to the foreign carrier.
        need('WORK_SPECIFICATION_ACTIVITY_TARGET_EXTENT_CONDITIONS','/atom/body/workSpecification')
        if b['performanceFacet']=='COMPLETED':need('ALL_BOUND_FINISH_CONDITIONS_OVER_ENTIRE_WORK_EXTENT','/atom/body/workSpecification/finishConditionIds')
        if action_type=='OTHER_ACTION':need('EXACT_SPECIFIC_ACTIVITY_DEFINITION_NOT_OTHER_ACTION_TOKEN','/atom/body/parameters')
        selections=data['quantitySelections'];ids=[x['parameterId'] for x in selections];source_indices=[x['sourceIndex'] for x in selections];byid={q['parameterId']:q for q in b['quantityParameters']}
        if len(ids)!=len(set(ids)) or len(source_indices)!=len(set(source_indices)):errors.append(error('AMBIGUOUS_QUANTITY_SOURCE_SELECTION','/quantitySelections'))
        for selection in selections:
            if selection['parameterId'] not in byid:errors.append(error('QUANTITY_SELECTION_UNKNOWN_ID','/quantitySelections'));continue
            q=byid[selection['parameterId']];array='quantityParameters' if kind=='intent' else 'actualQuantityParameters';index=selection['sourceIndex'];path='/'+array+'/'+str(index)
            try:actual=pointer(r,path)
            except ValueError:errors.append(error('QUANTITY_SOURCE_INDEX_MISSING','/source/record'+path));continue
            qindex=next(i for i,v in enumerate(b['quantityParameters']) if v['parameterId']==q['parameterId'])
            quantity_binding=src['binding']
            if q['value']['state']=='STATED' and not exact(q['value']['original']['sourceBinding'],quantity_binding):
                alias=selected_original_alias(src,q['value']['original']['sourceBinding'],resolved_sources)
                if alias is not None:
                    quantity_binding=alias['binding'];alias_role='OPERATION_QUANTITY_SOURCE:'+str(qindex)
                    origins[alias_role]=alias['record']
                    emit('ORIGINAL_QUANTITY_SOURCE_ALIAS_RECORD_MATCH',r,alias['record'],path,True,
                        ('OPERATION_SOURCE',''),(alias_role,''))
            qerrors,qrequirements=self.quantity(q,actual,quantity_binding,path,kind,emit,
                ('ATOM:'+a['atomId'],'/body/quantityParameters/'+str(qindex)))
            errors.extend(qerrors);requirements.extend(qrequirements)
        for q in b['quantityParameters']:
            if q['value']['state']=='STATED' and q['parameterId'] not in ids:need('EXACT_QUANTITY_SOURCE_FOR_PARAMETER:'+q['parameterId'],'/atom/body/quantityParameters')
        for field in self.rows[row]['parameterContract']['required']:
            if field not in self.rows[row]['parameterContract']['quantityFieldRoles'] and field!='method':need('ROW_PARAMETER_SOURCE:'+row+':'+field,'/atom/body/parameters/'+field)
        need('EXACT_IMMUTABLE_SOURCE_RESOLUTION','/source/binding');need('SOURCE_RECORD_ELIGIBLE_FOR_SELECTED_USE','/source')
        return self.result(errors,comparisons,requirements)
    def quantity(self,q,source_value,source_binding,source_pointer,kind,emit=None,claim_origin=None):
        errors=self.values.quantity_errors(q);requirements=[]
        if errors:return errors,requirements
        def trace(code,a,b,path,equal,source_field,claim_field):
            if emit is not None:
                emit(code,a,b,path,equal,('OPERATION_SOURCE',source_pointer+'/'+source_field) if source_field else None,
                    (claim_origin[0],claim_origin[1]+'/'+claim_field) if claim_field else None)
        def eq(code,a,b,path,source_field=None,claim_field=None):
            equal=exact(a,b);trace(code,a,b,path,equal,source_field,claim_field)
            if not equal:errors.append(error(code,path))
        def decimal_eq(code,actual,expected,path,source_field,claim_field):
            equal=not isinstance(actual,bool) and isinstance(actual,(int,float)) and Decimal(str(actual)).is_finite() and Decimal(str(actual))==number(expected)
            trace(code,actual,expected,path,equal,source_field,claim_field)
            if not equal:errors.append(error(code,path))
        path='/source/record'+source_pointer
        eq('QUANTITY_SOURCE_ROLE_MISMATCH',source_value['parameterRole'],q['parameterRole'],path+'/parameterRole','parameterRole','parameterRole')
        if q['valuePosture']!=('PLANNED' if kind=='intent' else 'ACTUAL'):
            requirements.append({'role':'QUANTITY_POSTURE_FROM_EXACT_PARAMETER_DEFINITION:'+q['valuePosture'],'pointer':'/atom/body/quantityParameters/valuePosture'})
        if q['value']['state']!='STATED':return errors+[error('QUANTITY_SOURCE_HAS_VALUE_BUT_CLAIM_UNREPORTED',path)],requirements
        value=q['value'];qty=value['quantity']
        eq('QUANTITY_SOURCE_KIND_MISMATCH',source_value['quantityKindRef'],qty['quantityKind'],path+'/quantityKindRef','quantityKindRef','value/quantity/quantityKind')
        eq('QUANTITY_SOURCE_UNIT_MISMATCH',source_value['unitRef'],qty['unit'],path+'/unitRef','unitRef','value/quantity/unit')
        decimal_eq('QUANTITY_SOURCE_VALUE_MISMATCH',source_value['value'],qty['decimal'],path+'/value','value','value/quantity/decimal')
        if 'qualifier' in source_value:eq('QUANTITY_SOURCE_QUALIFIER_MISMATCH',source_value['qualifier'],value['qualifier'],path+'/qualifier','qualifier','value/qualifier')
        else:requirements.append({'role':'OMITTED_QUANTITY_QUALIFIER_INTERPRETATION','pointer':path+'/qualifier'})
        m=q['material'];bs=q['basis']
        if m['presence']=='PRESENT':
            eq('QUANTITY_SOURCE_MATERIAL_ROLE_MISMATCH',source_value.get('materialRole'),m['materialRole'],path+'/materialRole','materialRole','material/materialRole')
            eq('QUANTITY_SOURCE_MATERIAL_REF_MISMATCH',source_value.get('materialRef'),m['binding']['ref'],path+'/materialRef','materialRef','material/binding/ref')
        elif 'materialRole' in source_value or 'materialRef' in source_value:errors.append(error('QUANTITY_SOURCE_MATERIAL_ERASED',path+'/materialRef'))
        if bs['presence']=='PRESENT':
            for field,sourcefield in [('quantityKind','basisQuantityKindRef'),('unit','basisUnitRef')]:eq('QUANTITY_SOURCE_BASIS_MISMATCH',source_value.get(sourcefield),bs['quantity'][field],path+'/'+sourcefield,sourcefield,'basis/quantity/'+field)
            decimal_eq('QUANTITY_SOURCE_BASIS_VALUE_MISMATCH',source_value.get('basisValue'),bs['quantity']['decimal'],path+'/basisValue','basisValue','basis/quantity/decimal')
        elif any(k in source_value for k in ['basisQuantityKindRef','basisUnitRef','basisValue']):errors.append(error('QUANTITY_SOURCE_BASIS_ERASED',path))
        o=value['original'];eq('ORIGINAL_QUANTITY_SOURCE_BINDING_MISMATCH',o['sourceBinding'],source_binding,'/original/sourceBinding');eq('ORIGINAL_QUANTITY_SOURCE_POINTER_MISMATCH',o['sourcePointer'],source_pointer+'/reportedValue','/original/sourcePointer')
        lexical=source_value.get('reportedValue') if isinstance(source_value.get('reportedValue'),str) else None
        reported=source_value.get('reportedValue')
        if type(reported) in [int,float]:
            eq('ORIGINAL_QUANTITY_NUMERIC_PRESENCE_MISMATCH',o['presence'],'PRESENT','/original/presence')
            if 'reportedValue' not in o:
                errors.append(error('ORIGINAL_QUANTITY_NUMERIC_REPRESENTATION_MISSING','/original/reportedValue'))
            else:eq('ORIGINAL_QUANTITY_NUMERIC_REPORTED_VALUE_MISMATCH',reported,o['reportedValue'],'/original/reportedValue','reportedValue','value/original/reportedValue')
        elif 'reportedValue' in o:
            errors.append(error('ORIGINAL_QUANTITY_NUMERIC_VALUE_NOT_IN_SOURCE','/original/reportedValue'))
        unit=source_value.get('reportedUnitLabel')
        eq('ORIGINAL_QUANTITY_LEXICAL_MISMATCH',lexical,o['lexicalValue'],'/original/lexicalValue','reportedValue' if isinstance(reported,str) else None,'value/original/lexicalValue')
        eq('ORIGINAL_QUANTITY_UNIT_TEXT_MISMATCH',unit,o['unitText'],'/original/unitText','reportedUnitLabel','value/original/unitText')
        if 'normalizedValue' in source_value:
            if 'normalized' not in value:requirements.append({'role':'NORMALIZED_VALUE_CONVERSION_AND_RETENTION','pointer':path+'/normalizedValue'})
            else:decimal_eq('NORMALIZED_SOURCE_VALUE_MISMATCH',source_value['normalizedValue'],value['normalized']['decimal'],path+'/normalizedValue','normalizedValue','value/normalized/decimal')
        if q['material']['presence']=='UNREPORTED' or q['basis']['presence']=='UNREPORTED':requirements.append({'role':'MISSING_QUANTITY_COMPARISON_CONTEXT','pointer':path})
        for role in ['QUANTITY_KIND_UNIT_PROFILE_AND_CONVERSION','MATERIAL_BASIS_IDENTITY_AND_PROCESS_POINT','QUANTITY_ACTIVITY_EXTENT_TIME_AND_POSTURE']:
            requirements.append({'role':role,'pointer':path})
        return errors,requirements
    @staticmethod
    def result(errors,comparisons,requirements):return {'scope':'OPERATION_CARRIER_COMPARISONS_ONLY','disposition':'COMPARISON_FAILED' if errors else 'COMPARISONS_SATISFIED_WITH_OWNER_ROLES_REQUIRED','errors':errors,'comparisons':comparisons,'requiredOwnerRoles':requirements}

if __name__=='__main__':build_schema();print(json.dumps({'operationInputContracts':27,'schemaId':OP_INPUT_ID}))
