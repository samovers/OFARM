"""Concrete owned checks over finite reviewed forms and pure domain values.

No function here admits foreign evidence or returns full domain PASS. Source
resolution/admission and the remaining row predicates are explicit integration
requirements, never successful stubs or permanent UNAVAILABLE branches.
"""
from datetime import datetime
from decimal import Decimal, InvalidOperation
import hashlib,json,re
from pathlib import Path
from jsonschema import Draft202012Validator,FormatChecker
from referencing import Registry,Resource
from build_owned_inputs import BASE_ID,BASE_PATH,SCHEMA_ID
from build_value_types import VALUE_ID,MEASUREMENT_ID,MEASUREMENT_PATH,EVENT_ID,EVENT_PATH

HERE=Path(__file__).resolve().parent
QUALIFIERS={'EXACT','ESTIMATED','MINIMUM','MAXIMUM','RANGE_MIDPOINT','LABEL_LIMIT','MACHINE_REPORTED','HUMAN_REPORTED','UNKNOWN'}
# quantity-contract roleMeanings define these roles as amounts of a material
# and/or relative to an explicit basis. Unknown kind/unit definitions still
# require selected definition checks; these role rules are not a unit engine.
MATERIAL_ROLES={'RATE','DOSE','CONCENTRATION','TOTAL_QUANTITY','CARRIER_VOLUME','WATER_VOLUME','SEED_RATE','NUTRIENT_RATE','FLOW_RATE','APPLICATION_VOLUME'}
RATIO_ROLES={'RATE','DOSE','CONCENTRATION','SEED_RATE','NUTRIENT_RATE','FLOW_RATE','SPEED','APPLICATION_VOLUME'}

def error(code,pointer,**details):return {'code':code,'pointer':pointer,**details}
def exact(left,right):
    if type(left)is bool or type(right)is bool:return type(left)is type(right) and left==right
    if isinstance(left,(int,float)) and isinstance(right,(int,float)):
        a,b=Decimal(str(left)),Decimal(str(right))
        return a.is_finite() and b.is_finite() and a==b
    if type(left)is not type(right):return False
    if isinstance(left,dict):return left.keys()==right.keys() and all(exact(left[k],right[k]) for k in left)
    if isinstance(left,list):return len(left)==len(right) and all(exact(a,b) for a,b in zip(left,right))
    return left==right

def instant(value):
    # PR23 canonical form allows 1..9 fractional digits, with no trailing zero.
    # datetime is used only for the calendar check; its microsecond precision
    # must never truncate the independently compared nanoseconds.
    if not isinstance(value,str) or not re.fullmatch(r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{0,8}[1-9])?Z',value):raise ValueError('canonical UTC timestamp required')
    dt=datetime.strptime(value[:19],'%Y-%m-%dT%H:%M:%S')
    fraction=value[20:-1] if len(value)>20 else ''
    return (dt.year,dt.month,dt.day,dt.hour,dt.minute,dt.second,int(fraction.ljust(9,'0') or '0'))

def number(value):
    if not isinstance(value,str) or not re.fullmatch(r'-?(0|[1-9][0-9]*)(\.[0-9]+)?',value):raise ValueError('finite plain decimal string required')
    result=Decimal(value)
    if not result.is_finite():raise ValueError('finite decimal required')
    return result

def interval_outcome(operator,lower,upper,threshold,lower_inclusive=True,upper_inclusive=True):
    """Exact mathematical comparison only; bounds/threshold authority is external."""
    try:
        if type(lower_inclusive)is not bool or type(upper_inclusive)is not bool:raise ValueError('Boolean inclusivity required')
        lo=None if lower is None else number(lower);hi=None if upper is None else number(upper);b=number(threshold)
        if lo is not None and hi is not None and (lo>hi or (lo==hi and not(lower_inclusive and upper_inclusive))):raise ValueError('empty or reversed interval')
        if operator not in ['LE','LT','GE','GT','EQ','NE']:raise ValueError('unknown comparison operator')
    except (ValueError,InvalidOperation) as exc:return {'errors':[error('INVALID_NUMERIC_COMPARISON','',reason=str(exc))]}
    if operator=='LE':yes=hi is not None and hi<=b;no=lo is not None and (lo>b or (lo==b and not lower_inclusive))
    elif operator=='LT':yes=hi is not None and (hi<b or (hi==b and not upper_inclusive));no=lo is not None and lo>=b
    elif operator=='GE':yes=lo is not None and lo>=b;no=hi is not None and (hi<b or (hi==b and not upper_inclusive))
    elif operator=='GT':yes=lo is not None and (lo>b or (lo==b and not lower_inclusive));no=hi is not None and hi<=b
    else:
        yes=lo is not None and hi is not None and lo==hi==b
        no=(lo is not None and (b<lo or (b==lo and not lower_inclusive))) or (hi is not None and (b>hi or (b==hi and not upper_inclusive)))
        if operator=='NE':yes,no=no,yes
    return {'errors':[],'outcome':'SATISFIED' if yes else 'NOT_SATISFIED' if no else 'INDETERMINATE','scope':'EXACT_BOUND_COMPARISON_ONLY'}

def composed_outcome(form,children):
    if form not in ['ALL','ANY','NOT','SEQUENCE'] or not isinstance(children,list) or not children or any(v not in ['TRUE','FALSE','INDETERMINATE'] for v in children) or (form=='NOT' and len(children)!=1):return {'errors':[error('INVALID_COMPOSITION','')]}
    if form=='NOT':value={'TRUE':'FALSE','FALSE':'TRUE','INDETERMINATE':'INDETERMINATE'}[children[0]]
    elif form in ['ALL','SEQUENCE']:value='FALSE' if 'FALSE' in children else 'INDETERMINATE' if 'INDETERMINATE' in children else 'TRUE'
    else:value='TRUE' if 'TRUE' in children else 'INDETERMINATE' if 'INDETERMINATE' in children else 'FALSE'
    return {'errors':[],'value':value,'scope':'PROPOSITION_ALGEBRA_ONLY; mandatory gates and sequence timing are separate'}

def measured_instant_errors(measurement,subject_time,selected_role):
    errors=[]
    if not isinstance(measurement,dict) or not isinstance(subject_time,dict):return [error('INVALID_TYPE','')]
    t=measurement.get('phenomenonTime')
    if not isinstance(t,dict):return [error('MISSING_PHENOMENON_TIME','/phenomenonTime')]
    if t.get('timeType')!='INSTANT':errors.append(error('PERFORMANCE_REQUIRES_INSTANT','/phenomenonTime/timeType'))
    if subject_time.get('profile')!='PERFORMED_INSTANT':errors.append(error('PERFORMANCE_PROFILE_MISMATCH','/subjectTime/profile'))
    try:instant(t.get('instant'));instant(subject_time.get('at'))
    except ValueError:errors.append(error('INVALID_TIME','/phenomenonTime/instant'))
    if t.get('instant')!=subject_time.get('at'):errors.append(error('PHENOMENON_TIME_MISMATCH','/phenomenonTime/instant'))
    if selected_role=='ABSENT':
        if 'timeBasis' in t:errors.append(error('TIME_QUALIFIER_PRESENCE_MISMATCH','/phenomenonTime/timeBasis'))
    elif selected_role not in ['OBSERVED_TIME','SAMPLE_TIME','RESULT_TIME','RECORD_TIME','ESTIMATED_TIME'] or t.get('timeBasis')!=selected_role:errors.append(error('TIME_QUALIFIER_MISMATCH','/phenomenonTime/timeBasis'))
    return errors

def result_fidelity_errors(source_result,claim_result):
    if not isinstance(source_result,dict) or not isinstance(claim_result,dict):return [error('INVALID_RESULT_TYPE','/result')]
    if source_result.get('resultKind') not in ['NUMERIC','CODED','QUALITATIVE','CENSORED_NUMERIC','ABSENT_PENDING']:return [error('UNKNOWN_RESULT_KIND','/result/resultKind')]
    return [] if exact(source_result,claim_result) else [error('RESULT_OR_QUALIFICATION_CHANGED','/result')]

def event_literal_errors(case,envelope,authoritative_family):
    if not isinstance(case,dict) or not isinstance(envelope,dict):return [error('INVALID_EVENT_INPUT_TYPE','')]
    errors=[];presence=case.get('subtypePresence')
    if presence=='ABSENT':
        if 'eventSubtypeId' in envelope:errors.append(error('EVENT_SUBTYPE_PRESENCE_MISMATCH','/eventSubtypeId'))
    elif presence=='PRESENT':
        if not isinstance(case.get('eventSubtypeId'),str) or envelope.get('eventSubtypeId')!=case['eventSubtypeId']:errors.append(error('EVENT_SUBTYPE_MISMATCH','/eventSubtypeId'))
    else:errors.append(error('UNKNOWN_EVENT_CASE','/subtypePresence'))
    if envelope.get('dominantSemanticConsequence')!=case.get('dominantSemanticConsequence'):errors.append(error('EVENT_CONSEQUENCE_MISMATCH','/dominantSemanticConsequence'))
    if not isinstance(authoritative_family,str) or envelope.get('primaryEventFamily')!=authoritative_family:errors.append(error('EVENT_FAMILY_MISMATCH','/primaryEventFamily'))
    return errors

class OwnedComponent:
    def __init__(self,repo_root):
        self.repo=Path(repo_root);self.contracts=json.loads((HERE/'owned-contract-inputs.json').read_text());self.map=json.loads((HERE/'definition-construction-map.json').read_text());self.rows={r['id']:r for r in self.map['definitions']};self.schema=json.loads((HERE/'finite-reviewed-forms.schema.json').read_text())
        pins=json.loads((HERE/'source-pins.json').read_text())
        for pin in pins['sources']:
            if hashlib.sha256((self.repo/pin['path']).read_bytes()).hexdigest()!=pin['sha256']:raise ValueError('Pinned source changed: '+pin['path'])
        base=json.loads((self.repo/BASE_PATH).read_text());self.value_schema=json.loads((HERE/'owned-value-types.schema.json').read_text());measurement=json.loads((self.repo/MEASUREMENT_PATH).read_text())
        event=json.loads((self.repo/EVENT_PATH).read_text())
        self.registry=Registry().with_resources([(BASE_ID,Resource.from_contents(base)),(SCHEMA_ID,Resource.from_contents(self.schema)),(VALUE_ID,Resource.from_contents(self.value_schema)),(MEASUREMENT_ID,Resource.from_contents(measurement)),(EVENT_ID,Resource.from_contents(event))])
    def value_errors(self,name,value):
        if name not in self.value_schema['$defs']:return [error('UNKNOWN_VALUE_TYPE','')]
        validator=Draft202012Validator({'$ref':VALUE_ID+'#/$defs/'+name},registry=self.registry,format_checker=FormatChecker())
        return [error('OWNED_VALUE_SHAPE','/'+('/'.join(str(x).replace('~','~0').replace('/','~1') for x in e.absolute_path)),keyword=e.validator) for e in sorted(validator.iter_errors(value),key=lambda e:str(list(e.absolute_path)))]
    def time_errors(self,value):
        errors=self.value_errors('subjectTime',value)
        if errors:return errors
        for field in ['at','start','end']:
            if field in value:
                try:instant(value[field])
                except ValueError:errors.append(error('INVALID_CALENDAR_TIME','/'+field))
        if not errors and 'end' in value and instant(value['start'])>=instant(value['end']):errors.append(error('EMPTY_OR_REVERSED_INTERVAL',''))
        return errors
    def quantity_errors(self,value):
        errors=self.value_errors('quantityParameter',value)
        if errors:return errors
        errors.extend({**e,'pointer':'/appliesTo/subjectTime'+e['pointer']} for e in self.time_errors(value['appliesTo']['subjectTime']))
        material=value['material']
        material_required=value['parameterRole'] in MATERIAL_ROLES or (value['parameterRole']=='OTHER_PARAMETER' and value['otherRoleDefinition'] in ['MOISTURE_TARGET','TREATED_AMOUNT','MATERIAL_HANDLED'])
        basis_required=value['parameterRole'] in RATIO_ROLES or (value['parameterRole']=='OTHER_PARAMETER' and value['otherRoleDefinition']=='MOISTURE_TARGET')
        if material_required and material['presence']=='NOT_APPLICABLE':errors.append(error('MATERIAL_ROLE_REQUIRES_MATERIAL_DISCLOSURE','/material/presence'))
        if basis_required and value['basis']['presence']=='NOT_APPLICABLE':errors.append(error('RATIO_ROLE_REQUIRES_BASIS_DISCLOSURE','/basis/presence'))
        if value.get('applicationMaterialInterpretation')=='MIXTURE_AS_APPLIED':
            bindings=[c['binding'] for c in material['components']]
            if any(exact(a,b) for i,a in enumerate(bindings) for b in bindings[i+1:]):errors.append(error('DUPLICATE_CONSTITUENT_IDENTITY','/material/components'))
            if any(exact(material['binding'],c) for c in bindings):errors.append(error('MIXTURE_EQUALS_CONSTITUENT','/material/binding'))
        return errors
    def quantity_context_errors(self,quantity,selected_expectation):
        """Compare two domain quantity allegations under independent selection.

        This establishes only exact role/material/basis/posture/activity/scope,
        quantity-kind/unit and qualifier agreement. It is not a foreign record
        format or source-admission decision. Numeric comparison is a subsequent
        operation and cannot use these selectors as proof of their resolution.
        """
        errors=self.quantity_errors(quantity)+self.quantity_errors(selected_expectation)
        if errors:return errors
        for field in ['parameterId','parameterRole','activityInstance','valuePosture','material','basis','appliesTo','otherRoleDefinition','applicationMaterialInterpretation']:
            if (field in quantity)!=(field in selected_expectation) or not exact(quantity.get(field),selected_expectation.get(field)):errors.append(error('QUANTITY_SELECTED_CONTEXT_MISMATCH','/'+field))
        for name,value in [('claim',quantity),('expectation',selected_expectation)]:
            if value['value']['state']!='STATED' or value['material']['presence']=='UNREPORTED' or value['basis']['presence']=='UNREPORTED':errors.append(error('QUANTITY_COMPARISON_CONTEXT_UNRESOLVED','/'+name))
        if errors:return errors
        for field in ['quantityKind','unit']:
            if quantity['value']['quantity'][field]!=selected_expectation['value']['quantity'][field]:errors.append(error('QUANTITY_SELECTED_CONTEXT_MISMATCH','/value/quantity/'+field))
        for field in ['qualifier','unitProfile']:
            if not exact(quantity['value'][field],selected_expectation['value'][field]):errors.append(error('QUANTITY_SELECTED_CONTEXT_MISMATCH','/value/'+field))
        return errors
    def analysis_output_errors(self,output,subject_time,posture,facet,specification):
        errors=self.value_errors('analysisOutput',output)+self.time_errors(subject_time)+self.value_errors('binding',specification)
        if errors:return errors
        profile=subject_time['profile'];profiles=self.contracts['operationProfiles']['O22OutputContract']['byProfileAndFacet']
        if profile not in profiles:return [error('ANALYSIS_PROFILE_UNKNOWN','/subjectTime/profile')]
        if facet not in profiles[profile]:return [error('ANALYSIS_FACET_UNKNOWN','/performanceFacet')]
        if posture!=('INTENDED' if profile=='INTENDED_WINDOW' else 'PERFORMED'):errors.append(error('PROFILE_POSTURE_MISMATCH','/claimPosture'))
        if output['role'] not in profiles[profile][facet]:errors.append(error('ANALYSIS_OUTPUT_ROLE_MISMATCH','/producedResult/role'))
        if not exact(output['specificationBinding'],specification):errors.append(error('ANALYSIS_OUTPUT_SPECIFICATION_MISMATCH','/producedResult/specificationBinding'))
        return errors
    def measurement_result_errors(self,source_result,claim_result):
        # Reuse the actual carrier schema, including all five result branches.
        # Exact preservation does not establish property/method/eligible use.
        errors=self.value_errors('measurementResult',source_result)+self.value_errors('measurementResult',claim_result)
        return errors or result_fidelity_errors(source_result,claim_result)
    def measured_instant_errors(self,measurement,subject_time,selected_role):
        errors=self.value_errors('measurementRecord',measurement)+self.time_errors(subject_time)
        return errors or measured_instant_errors(measurement,subject_time,selected_role)
    def event_time_errors(self,subject_time,envelope,selected_selector):
        """Profile/presence and exact selected time only, never ingress approval.

        selected_selector must come from the independently selected immutable
        meaning package, not a caller-supplied escape or an envelope field.
        """
        errors=self.time_errors(subject_time)
        if errors:return errors
        if envelope is None:return []
        if subject_time['profile']=='INTENDED_WINDOW':return [error('INTENDED_EVENT_PROHIBITED','/associatedSemanticEvent')]
        errors=self.value_errors('eventEnvelope',envelope)
        if errors:return errors
        spec=next(t for t in self.contracts['timeProfiles'] if t['profile']==subject_time['profile'])
        if 'end' in subject_time:
            if selected_selector!=['/timeSemantics/effectiveFrom','/timeSemantics/effectiveUntil']:return [error('EVENT_SELECTOR_MISMATCH','/selectedSelector')]
            pairs=[('effectiveFrom','start'),('effectiveUntil','end')]
        else:
            if not isinstance(selected_selector,str) or selected_selector not in spec['eventSelectors']:return [error('EVENT_SELECTOR_MISMATCH','/selectedSelector')]
            pairs=[(selected_selector.rsplit('/',1)[-1],'at' if 'at' in subject_time else 'start')]
        for event_field,claim_field in pairs:
            actual=envelope['timeSemantics'].get(event_field)
            if actual!=subject_time[claim_field]:errors.append(error('EVENT_TIME_MISMATCH','/timeSemantics/'+event_field))
        return errors
    def qualified_nl_errors(self,body,expected_context):
        # Bounded, independently executable positive: the qualified organic
        # parcel allegation. No calculation or asserted exemption is accepted.
        errors=self.value_errors('nlQualifiedOrganicParcelBody',body)
        if errors:return errors
        fields=['profile','claimYear','route','routeScope','parcel','historyClaim','soilCategory','soilEvidence','rustgewasEvidence','routeEvidence','evaluationBasis']
        if not isinstance(expected_context,dict) or set(expected_context)!=set(fields):return [error('INVALID_NL_EXPECTATION_FIELDS','')]
        for field in fields:
            if not exact(body[field],expected_context[field]):errors.append(error('NL_SELECTED_CONTEXT_MISMATCH','/'+field))
        return errors
    def finite_form_errors(self,row,atom):
        if row not in self.schema['$defs'] or row=='quantityParameter':return [error('UNKNOWN_ATOM_DEFINITION','/definition')]
        validator=Draft202012Validator({'$ref':SCHEMA_ID+'#/$defs/'+row},registry=self.registry)
        return [error('FINITE_REVIEWED_FORM_SHAPE','/'+('/'.join(str(x).replace('~','~0').replace('/','~1') for x in e.absolute_path)),keyword=e.validator) for e in sorted(validator.iter_errors(atom),key=lambda e:str(list(e.absolute_path)))]
    def check_reviewed_atom(self,row,atom):
        errors=self.finite_form_errors(row,atom)
        if errors:return {'disposition':'OWNED_CHECKS_FAILED','errors':errors,'scope':'FINITE_REVIEWED_FORM_AND_LISTED_INTRINSIC_CHECKS'}
        return self._check_atom(row,atom,'FINITE_REVIEWED_FORM_AND_LISTED_INTRINSIC_CHECKS_ONLY')
    def check_explicit_o22(self,atom):
        errors=self.value_errors('O22',atom)
        if errors:return {'disposition':'OWNED_CHECKS_FAILED','errors':errors,'scope':'EXPLICIT_O22_FIELD_CONTRACT_AND_LISTED_INTRINSIC_CHECKS'}
        return self._check_atom('O22',atom,'EXPLICIT_O22_FIELD_CONTRACT_AND_LISTED_INTRINSIC_CHECKS')
    def _check_atom(self,row,atom,execution_scope):
        errors=[]
        b=atom['body'];scope=atom['scope'];t=scope['subjectTime']
        def bad(code,okay,path):
            if not okay:errors.append(error(code,path))
        for key in ['at','start','end']:
            if key in t:
                try:instant(t[key])
                except ValueError:errors.append(error('INVALID_CALENDAR_TIME','/scope/subjectTime/'+key))
        if 'start' in t and 'end' in t:
            try:bad('EMPTY_OR_REVERSED_INTERVAL',instant(t['start'])<instant(t['end']),'/scope/subjectTime')
            except ValueError:pass
        if row.startswith('O'):
            intended=t['profile']=='INTENDED_WINDOW';bad('PROFILE_POSTURE_MISMATCH',b['claimPosture']==('INTENDED' if intended else 'PERFORMED'),'/body/claimPosture');bad('ACTIVITY_EXTENT_MISMATCH',exact(b['extent'],scope['extent']),'/body/extent')
            spec=b['workSpecification']
            for key in ['activityInstance','target','extent']:bad('WORK_SPECIFICATION_'+key.upper()+'_MISMATCH',exact(spec[key],b[key]),'/body/workSpecification/'+key)
            for key in ['startConditionIds','inProgressConditionIds','finishConditionIds']:bad('EMPTY_WORK_CONDITIONS',bool(spec[key]) and len(spec[key])==len(set(spec[key])),'/body/workSpecification/'+key)
            quantities=b['quantityParameters'];ids=[q['parameterId'] for q in quantities];bad('DUPLICATE_QUANTITY_ID',len(ids)==len(set(ids)),'/body/quantityParameters');byid={q['parameterId']:q for q in quantities}
            for i,q in enumerate(quantities):
                errors.extend({**e,'pointer':'/body/quantityParameters/'+str(i)+e['pointer']} for e in self.quantity_errors(q))
                path='/body/quantityParameters/'+str(i);bad('QUANTITY_ROLE_UNKNOWN',q['parameterRole'] in self.contracts['quantity']['parameterRoles'],path+'/parameterRole');bad('QUANTITY_ACTIVITY_MISMATCH',exact(q['activityInstance'],b['activityInstance']),path+'/activityInstance')
                for key in ['target','extent']:bad('QUANTITY_SCOPE_MISMATCH',exact(q['appliesTo'][key],b[key]),path+'/appliesTo/'+key)
                bad('QUANTITY_TIME_MISMATCH',exact(q['appliesTo']['subjectTime'],t),path+'/appliesTo/subjectTime')
                bad('QUANTITY_POSTURE_MISMATCH',q['valuePosture'] in ['PLANNED','ACTUAL','TARGET','LIMIT'],path+'/valuePosture')
                value=q['value']
                if value.get('state')=='STATED':
                    try:number(value['quantity']['decimal'])
                    except (ValueError,KeyError):errors.append(error('INVALID_QUANTITY_DECIMAL',path+'/value/quantity/decimal'))
                    bad('QUANTITY_QUALIFIER_UNKNOWN',value.get('qualifier') in QUALIFIERS,path+'/value/qualifier')
                elif value.get('state')!='UNREPORTED':errors.append(error('UNKNOWN_QUANTITY_VALUE_STATE',path+'/value/state'))
                material=q['material']
                if material.get('presence')=='PRESENT':
                    bad('MATERIAL_ROLE_UNKNOWN',material.get('materialRole') in self.contracts['quantity']['materialRoles'],path+'/material/materialRole')
                    if material.get('materialRole')=='OTHER_MATERIAL':bad('MISSING_MATERIAL_DEFINITION','materialDefinition' in material,path+'/material/materialDefinition')
                if q['parameterRole']=='APPLICATION_VOLUME':
                    mode=q.get('applicationMaterialInterpretation');bad('APPLICATION_MATERIAL_INTERPRETATION_UNKNOWN',mode in self.contracts['quantity']['applicationVolumeMaterialContract']['variants'],path+'/applicationMaterialInterpretation')
                    if mode=='MIXTURE_AS_APPLIED':
                        components=material.get('components',[]);bad('MIXTURE_IDENTITY_ROLE_MISMATCH',material.get('materialRole')=='OTHER_MATERIAL' and 'materialDefinition' in material,path+'/material')
                        bad('MIXTURE_CONSTITUENTS_MISSING',len(components)>=2,path+'/material/components')
                        if 'binding' in material:bad('MIXTURE_EQUALS_CONSTITUENT',all(not exact(c.get('binding'),material['binding']) for c in components),path+'/material/binding')
                    elif mode=='UNRESOLVED_SOURCE_MATERIAL':bad('UNRESOLVED_MATERIAL_POSTURE_MISMATCH',material.get('presence')=='UNREPORTED',path+'/material/presence')
                if q['parameterRole']=='OTHER_PARAMETER':bad('OTHER_QUANTITY_DEFINITION_MISSING','otherRoleDefinition' in q,path+'/otherRoleDefinition')
            for field,role in self.rows[row]['parameterContract']['quantityFieldRoles'].items():
                selected=b['parameters'][field]['quantityParameterId'];q=byid.get(selected);bad('QUANTITY_REFERENCE_MISMATCH',q is not None and q['parameterRole']==role,'/body/parameters/'+field)
                required_material=self.rows[row]['parameterContract'].get('quantityFieldMaterialRoles',{}).get(field)
                if q is not None and required_material and q['material'].get('presence')=='PRESENT':bad('PARAMETER_MATERIAL_ROLE_MISMATCH',q['material'].get('materialRole')==required_material,'/body/parameters/'+field)
            if row=='O22':
                output=b['parameters']['producedResult'];allowed=self.contracts['operationProfiles']['O22OutputContract']['byProfileAndFacet'][t['profile']][b['performanceFacet']]
                bad('ANALYSIS_OUTPUT_ROLE_MISMATCH',output['role'] in allowed,'/body/parameters/producedResult/role');bad('ANALYSIS_OUTPUT_SPECIFICATION_MISMATCH',exact(output['specificationBinding'],spec.get('outputSpecification')),'/body/parameters/producedResult/specificationBinding')
                bad('ANALYSIS_METHOD_SPECIFICATION_MISMATCH',exact(b['parameters']['method'],spec['procedure']),'/body/workSpecification/procedure')
            if row=='O25':
                p=b['parameters'];bad('UNCHANGED_RECLASSIFICATION',not exact(p['fromClass'],p['toClass']),'/body/parameters/toClass')
                if p['identityDisposition']=='SAME_COHORT_CLASSIFICATION_ONLY':bad('SAME_COHORT_BASIS_CHANGED',exact(p['beforeClaimBasis'],p['afterClaimBasis']) and p['successorProposal']['presence']=='ABSENT','/body/parameters')
            if row=='O27':
                p=b['parameters'];bad('FORBIDDEN_IDENTITY_EFFECT',p['creationEffectRequested'] is False and p['prospectiveLot']['identityStatus']=='PROPOSED_NOT_CREATED','/body/parameters/creationEffectRequested')
                bad('MISSING_CREATION_PREDECESSORS',bool(p['predecessors']) or p['creationBasis'] in ['INITIAL_COHORT','HARVEST_OUTPUT'],'/body/parameters/predecessors')
        if row=='C03':bad('MEASURED_SOURCE_ALIAS_MISMATCH',exact(b['measurement'],b['measurementSource']['measurementBinding']) and b['operandPointer']==b['measurementSource']['resultPointer'],'/body/measurementSource')
        if row=='C06':
            source=b['rateSource'];bad('UNKNOWN_RATE_SOURCE_KIND',source['sourceKind'] in ['HUMAN_REPORT','OPERATION_PARAMETER','MEASUREMENT_EVIDENCE'],'/body/rateSource/sourceKind')
            if source['sourceKind']=='MEASUREMENT_EVIDENCE':bad('RATE_MEASURED_SOURCE_ALIAS_MISMATCH','measurementSource' in source and exact(source['sourceBinding'],source['measurementSource']['measurementBinding']) and source['valuePointer']==source['measurementSource']['resultPointer'],'/body/rateSource')
        if row=='C04':bad('CENSORED_PROFILE_REQUIRED',b['operand']['resultKind']=='CENSORED_NUMERIC','/body/operand/resultKind')
        if row=='C17':bad('RECORDKEEPING_IS_NOT_LAWFUL_USE',b['lawfulUseAlleged'] is False,'/body/lawfulUseAlleged')
        if row=='C16':
            # This finite reviewed branch is the expressly qualified positive;
            # calculated or authority-determined routes need their own contract.
            errors.extend({**e,'pointer':'/body'+e['pointer']} for e in self.value_errors('nlQualifiedOrganicParcelBody',b))
        if row=='S03':bad('DURABLE_ZONE_REQUIRES_RECURRING',b['recurring'] is True,'/body/recurring')
        if row=='S12':bad('ASSET_KIND_ALIAS',b['assetKind']==scope['subject']['kind'],'/body/assetKind')
        return {'disposition':'OWNED_CHECKS_FAILED' if errors else 'OWNED_CHECKS_SATISFIED','errors':errors,'scope':execution_scope,'remainingRowSpecifications':self.rows[row]['domainPredicates'],'ownerPrerequisites':self.rows[row]['exactOwnerPrerequisites']}
