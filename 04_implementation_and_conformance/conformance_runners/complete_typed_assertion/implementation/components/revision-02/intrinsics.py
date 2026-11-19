"""Explicit intrinsic predicates for the recursive claim grammar.

These checks reject inconsistent allegations before source comparison. Passing
is conditional claim consistency, never truth, admission or the public verdict.
No free-form body label is interpreted as a policy or calculation rule.
"""
from common import *
from runtime_support import Schemas,Values,exact,instant,number,error,interval_outcome


def time_bounds(t):
    if 'at' in t:return instant(t['at']),instant(t['at'])
    return instant(t['start']),instant(t['end']) if 'end' in t else None


def nonempty_interval(value,path):
    errors=[]
    if value.get('kind')!='INTERVAL':return [error('ADMISSIBLE_SET_KIND',path)]
    ends=[]
    for key in ['lower','upper']:
        end=value[key];ends.append(None if end.get('kind')=='UNBOUNDED' else number(end['decimal']))
    lo,hi=ends
    if lo is not None and hi is not None and (lo>hi or (lo==hi and not(value['lower']['inclusive'] and value['upper']['inclusive']))):
        errors.append(error('EMPTY_ADMISSIBLE_SET',path))
    return errors


class Intrinsics:
    def __init__(self):
        self.schemas=Schemas();self.values=Values(self.schemas)
        self.rows={r['id']:r for r in reviewed('reviewed-input/domain/inventory.json')['rows']}
    def check(self,proposition):
        errors=self.schemas.errors(SCHEMA_ID,proposition)
        if errors:return self.result(errors,[])
        atoms=[];sequences=[];qualifications=[]
        def walk(p,path):
            if p['form']=='ATOM':atoms.append((p,path))
            elif p['form'] in ['NOT','QUALIFIED']:
                if p['form']=='QUALIFIED':qualifications.append((p,path))
                walk(p['child'],path+'/child')
            else:
                if p['form']=='SEQUENCE':sequences.append((p,path))
                for i,c in enumerate(p['children']):walk(c,path+'/children/'+str(i))
        walk(proposition,'')
        ids=[a['atomId'] for a,_ in atoms]
        if len(ids)!=len(set(ids)):errors.append(error('DUPLICATE_ATOM_ID',''))
        for atom,path in atoms:errors.extend({**e,'pointer':path+e['pointer']} for e in self.atom(atom))
        for q,path in qualifications:
            if q['appliesToAtomId']!=q['child']['atomId']:errors.append(error('QUALIFICATION_TARGET_MISMATCH',path+'/appliesToAtomId'))
            if q['qualifiers'].get('extentQualification')=='FULL_EXTENT' and q['child']['scope']['extent']['posture']!='FULL_TARGET_SCOPE':
                errors.append(error('QUALIFIED_EXTENT_CONTRADICTION',path+'/qualifiers/extentQualification'))
        for seq,path in sequences:
            children=[]
            def leaves(p):
                if p['form']=='ATOM':children.append(p)
                elif 'child' in p:leaves(p['child'])
                else:
                    for c in p['children']:leaves(c)
            leaves(seq);byid={a['atomId']:a for a in children}
            for i,r in enumerate(seq['orderRelations']):
                here=path+'/orderRelations/'+str(i)
                if r['beforeAtomId'] not in byid or r['afterAtomId'] not in byid:errors.append(error('SEQUENCE_ENDPOINT_OUTSIDE_CHILDREN',here));continue
                if r['beforeAtomId']==r['afterAtomId']:errors.append(error('SEQUENCE_SELF_ORDER',here));continue
                try:
                    _,before_end=time_bounds(byid[r['beforeAtomId']]['scope']['subjectTime']);after_start,_=time_bounds(byid[r['afterAtomId']]['scope']['subjectTime'])
                    if before_end is None:errors.append(error('SEQUENCE_UNBOUNDED_CHILD_TIME',here))
                    elif before_end>=after_start:errors.append(error('SEQUENCE_BEFORE_NOT_STRICT',here))
                except ValueError:pass # The atom time check already records the cause.
            for a in children:
                if 'end' not in a['scope']['subjectTime'] and 'at' not in a['scope']['subjectTime']:errors.append(error('SEQUENCE_UNBOUNDED_CHILD_TIME',path))
        return self.result(errors,[a['definition'].removeprefix(DEFINITION_PREFIX) for a,_ in atoms])
    @staticmethod
    def result(errors,rows):
        return {'scope':'INTRINSIC_CLAIM_CONSISTENCY_ONLY','disposition':'INCONSISTENT' if errors else 'INTRINSICALLY_CONSISTENT',
            'errors':errors,'rowsChecked':rows,
            'nextRequiredComparisons':['EXACT_SELECTED_DEFINITION_AND_SOURCE_ROLES','SOURCE_RESOLUTION_AND_ELIGIBLE_USE','OUTER_CARRIER_MANDATORY_GATES']}
    def atom(self,a):
        row=a['definition'].removeprefix(DEFINITION_PREFIX);b=a['body'];s=a['scope'];t=s['subjectTime'];errors=[]
        errors.extend({**e,'pointer':'/scope/subjectTime'+e['pointer']} for e in self.values.time_errors(t))
        def check(code,okay,path):
            if not okay:errors.append(error(code,path))
        if row.startswith('O'):
            spec=b['workSpecification'];p=b['parameters'];qs=b['quantityParameters']
            check('ACTIVITY_EXTENT_MISMATCH',exact(b['extent'],s['extent']),'/body/extent')
            for key in ['activityInstance','target','extent']:
                check('WORK_SPECIFICATION_'+key.upper()+'_MISMATCH',exact(spec[key],b[key]),'/body/workSpecification/'+key)
            ids=[q['parameterId'] for q in qs];check('DUPLICATE_QUANTITY_ID',len(ids)==len(set(ids)),'/body/quantityParameters');byid={q['parameterId']:q for q in qs}
            for i,q in enumerate(qs):
                path='/body/quantityParameters/'+str(i)
                errors.extend({**e,'pointer':path+e['pointer']} for e in self.values.quantity_errors(q))
                check('QUANTITY_ACTIVITY_MISMATCH',exact(q['activityInstance'],b['activityInstance']),path+'/activityInstance')
                for key in ['target','extent']:check('QUANTITY_SCOPE_MISMATCH',exact(q['appliesTo'][key],b[key]),path+'/appliesTo/'+key)
                check('QUANTITY_TIME_MISMATCH',exact(q['appliesTo']['subjectTime'],t),path+'/appliesTo/subjectTime')
                if b['claimPosture']=='INTENDED':check('INTENDED_ACTUAL_QUANTITY',q['valuePosture']!='ACTUAL',path+'/valuePosture')
            pc=self.rows[row]['parameterContract']
            for field,role in pc['quantityFieldRoles'].items():
                if field not in p:continue
                q=byid.get(p[field]['quantityParameterId']);path='/body/parameters/'+field
                check('QUANTITY_REFERENCE_MISMATCH',q is not None and q['parameterRole']==role,path)
                required_material=pc.get('quantityFieldMaterialRoles',{}).get(field)
                if q is not None and required_material and q['material']['presence']=='PRESENT':check('PARAMETER_MATERIAL_ROLE_MISMATCH',q['material']['materialRole']==required_material,path)
            if row in ['O11','O12','O13']:
                predecessors=[v['ref'] for v in p['predecessors']];successors=[v.get('ref',v.get('proposalId')) for v in p['successors']]
                check('DUPLICATE_PREDECESSOR_IDENTITY',len(predecessors)==len(set(predecessors)),'/body/parameters/predecessors')
                check('DUPLICATE_SUCCESSOR_IDENTITY',len(successors)==len(set(successors)),'/body/parameters/successors')
                check('NEW_COHORT_REUSES_PREDECESSOR_IDENTITY',not set(predecessors)&set(successors),'/body/parameters/successors')
            if row=='O22':
                check('ANALYSIS_METHOD_SPECIFICATION_MISMATCH',exact(p['method'],spec['procedure']),'/body/workSpecification/procedure')
                check('ANALYSIS_OUTPUT_SPECIFICATION_MISMATCH',exact(p['producedResult']['specificationBinding'],spec['outputSpecification']),'/body/parameters/producedResult/specificationBinding')
            if row=='O25':
                check('UNCHANGED_RECLASSIFICATION',not exact(p['fromClass'],p['toClass']),'/body/parameters/toClass')
                if p['identityDisposition']=='SAME_COHORT_CLASSIFICATION_ONLY':check('SAME_COHORT_BASIS_CHANGED',exact(p['beforeClaimBasis'],p['afterClaimBasis']),'/body/parameters/afterClaimBasis')
            if row=='O26' and p['residualMaterial']['state']=='STATED':
                q=byid.get(p['residualMaterial']['quantityParameterId'])
                check('RESIDUAL_QUANTITY_REFERENCE_MISSING',q is not None,'/body/parameters/residualMaterial/quantityParameterId')
                if q is not None and q['material']['presence']=='PRESENT':check('RESIDUAL_MATERIAL_MISMATCH',exact(q['material']['binding'],p['residualMaterial']['material']['binding']),'/body/parameters/residualMaterial/material')
            if row=='O27':
                if s['subject']['subjectPosture']=='EXISTING_SUBJECT':check('PROPOSED_LOT_USED_AS_EXISTING_SUBJECT',s['subject']['subjectRef']!=p['prospectiveLot']['proposalId'],'/scope/subject/subjectRef')
        if row=='S12':check('ASSET_KIND_ALIAS',b['assetKind']==s['subject']['subjectType'],'/body/assetKind')
        if row=='S13':
            for i,o in enumerate(b.get('occupancies',[])):
                path='/body/occupancies/'+str(i)
                try:
                    start=instant(o['start'])
                    if 'end' in o:check('EMPTY_OR_REVERSED_OCCUPANCY',start<instant(o['end']),path)
                except ValueError:errors.append(error('INVALID_OCCUPANCY_TIME',path))
        if row=='C03':check('MEASURED_SOURCE_ALIAS_MISMATCH',exact(b['measurement'],b['measurementSource']['measurementBinding']) and b['operandPointer']==b['measurementSource']['resultPointer'],'/body/measurementSource')
        if row=='C06' and b['rateSource']['sourceKind']=='MEASUREMENT_EVIDENCE':
            r=b['rateSource'];check('RATE_MEASURED_SOURCE_ALIAS_MISMATCH',exact(r['sourceBinding'],r['measurementSource']['measurementBinding']) and r['valuePointer']==r['measurementSource']['resultPointer'],'/body/rateSource')
        if row in ['C03','C04'] and b['operator']=='BETWEEN':
            lo,hi=b['threshold']['lower'],b['threshold']['upper'];path='/body/threshold'
            for key in ['quantityKind','unit','unitProfile']:check('RANGE_BOUND_CONTEXT_MISMATCH',exact(lo[key],hi[key]),path+'/'+key)
            check('EMPTY_OR_REVERSED_THRESHOLD',number(lo['decimal'])<number(hi['decimal']) or (number(lo['decimal'])==number(hi['decimal']) and b['threshold']['lowerInclusive'] and b['threshold']['upperInclusive']),path)
        if row=='C04' and 'admissibleValues' in b['operand']:
            errors.extend(nonempty_interval(b['operand']['admissibleValues'],'/body/operand/admissibleValues'))
            if b['operand'].get('nonnegative'):
                lower=b['operand']['admissibleValues']['lower']
                check('NONNEGATIVE_DOMAIN_CONTRADICTION','decimal' in lower and number(lower['decimal'])>=0,'/body/operand/admissibleValues/lower')
        if row=='C12':
            try:check('EMPTY_OR_REVERSED_CERTIFICATE_TIME',instant(b['validFrom'])<instant(b['validUntil']),'/body/validUntil')
            except ValueError:errors.append(error('INVALID_CERTIFICATE_TIME','/body'))
        if row=='C13':
            try:instant(b['at'])
            except ValueError:errors.append(error('INVALID_REFERENCE_TIME','/body/at'))
        return errors
