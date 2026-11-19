"""Build all 58 explicit atom field contracts and recursive proposition."""
import copy
from common import *
from structure_operation_types import definitions as structure_operations
from compliance_types import definitions as compliance

def main():
    inventory=reviewed('reviewed-input/domain/inventory.json');rows={r['id']:r for r in inventory['rows']}
    defs,structures,parameters=structure_operations();cd,compliance_fields=compliance();defs.update(cd)
    amendments={
        'S04':{'optional':['variety'],'reason':'typedFieldsAndOperators explicitly permits a variety allegation.'},
        'S07':{'makeOptional':['formulation'],'reason':'typedFieldsAndOperators says formulation if alleged; the new contract preserves that unexemplified path.'},
        'S09':{'optional':['existingSuccessors'],'reason':'typedFieldsAndOperators explicitly includes new or prospective bindings. Existing successors retain immutable selectors; prospective references never acquire them.'},
        'S13':{'makeOptional':['occupancies'],'optional':['occupancyEvidence','occupancyClaimPosture'],
               'reason':'PR57 R3 supplies the complete ordered inventory of overlapping reported episodes, including repeated visits. The complete branch retains every original endpoint, interval posture, amount, unit, cohort, extent and source qualification, and the consumer retains query intersections, supported applicability and coverage. UNQUALIFIED_EPISODES_DURING_WINDOW is a distinct domain meaning for clean support over retained intersections; it does not assert occupancy throughout the window or actual inventory completeness. UNQUALIFIED_OCCUPANCY continues to require full-window support for each episode. Legacy lot/start/end allegations remain shape-valid but cannot discharge complete source comparison.'},
        'S14':{'optional':['lineage'],'reason':'typedFieldsAndOperators explicitly includes lineage if restructured.'},
        'C03':{'required':['measurementSource'],'optional':['measuredQualification'],'reason':'Amendment 02 measured role and qualification requirements.'},
        'C04':{'required':['criterion'],'optional':['measuredQualification'],'reason':'Amendments 02/03 require exact criterion, source tuple, admissible set and scalar provenance; all result forms remain distinct.'},
        'C06':{'required':['rateSource'],'optional':['measuredQualification'],'reason':'Amendment 02 distinguishes human, operation-parameter and measured sources.'},
        'C09':{'optional':['measurementSource','measuredQualification'],'reason':'Amendment 02 requires measurementSource exactly for the measured branch; selected use independently determines qualification requirements.'},
    }
    trace=[]
    for row_id,row in rows.items():
        contract=row['atomContract'];required=list(contract['requiredBodyFields']);optional=list(contract['optionalBodyFields']);change=amendments.get(row_id,{})
        for field in change.get('makeOptional',[]):required.remove(field);optional.append(field)
        required+=change.get('required',[]);optional+=change.get('optional',[])
        if row_id.startswith('O'):
            pc=row['parameterContract'];field_types=parameters[row_id]
            assert set(field_types)==set(pc['required']+pc['optional']),(row_id,'parameter keys')
            p_schema=obj(field_types,pc['required'])
            for field,values in pc.get('enums',{}).items():
                assert set(field_types[field].get('enum',[]))==set(values),(row_id,field,'source enum drift')
            if row_id=='O24':p_schema['anyOf']=[{'properties':{'receiver':BINDING}},{'properties':{'destination':typed_binding()}}]
            if row_id=='O25':p_schema['allOf']=[condition('identityDisposition','SAME_COHORT_CLASSIFICATION_ONLY',{'properties':{'successorProposal':{'properties':{'presence':const('ABSENT')}}}}, {'properties':{'successorProposal':{'properties':{'presence':const('PRESENT')}}}})]
            if row_id=='O27':p_schema['allOf']=[{'if':{'properties':{'creationBasis':{'not':enum(['INITIAL_COHORT','HARVEST_OUTPUT'])}}},'then':{'properties':{'predecessors':{'minItems':1}}}}]
            fields={**{k:const(v) for k,v in contract['bodyDiscriminators'].items()},
                'claimPosture':enum(['INTENDED','PERFORMED']),'performanceFacet':enum(['OCCURRENCE','STARTED','IN_PROGRESS','COMPLETED']),
                'activityInstance':BINDING,'target':typed_binding(),'performedBy':BINDING,'extent':vref('extent'),
                'parameters':p_schema,'quantityParameters':arr(vref('quantityParameter')),'workSpecification':ref('workSpecification')}
            if row_id=='O22':fields['workSpecification']={'allOf':[ref('workSpecification'),{'required':['outputSpecification']}]}
        else:fields=(structures if row_id.startswith('S') else compliance_fields)[row_id]
        assert set(fields)==set(required+optional),(row_id,'body keys',set(fields)^set(required+optional))
        body=obj(fields,required)
        if row_id=='S13':body['oneOf']=[{'required':['occupancies'],'not':{'anyOf':[{'required':['occupancyEvidence']},{'required':['occupancyClaimPosture']}]}},
                                      {'required':['occupancyEvidence','occupancyClaimPosture'],'not':{'required':['occupancies']}}]
        if row_id=='S09':body['allOf']=[condition('case','SUCCESSOR_IDENTITIES',{'anyOf':[{'properties':{'prospectiveSuccessors':{'minItems':1}}},{'required':['existingSuccessors']}]},{'properties':{'prospectiveSuccessors':{'maxItems':0}}})]
        if row_id in ['C03','C04']:
            scalar='provenanceQuantity' if row_id=='C04' else 'complianceQuantity';range_name='provenanceComparisonRange' if row_id=='C04' else 'comparisonRange'
            body['allOf']=[condition('operator','BETWEEN',{'properties':{'threshold':ref(range_name)}},{'properties':{'threshold':ref(scalar)}})]
        if row_id=='C04':body.setdefault('allOf',[]).append({'if':{'properties':{'operand':{'properties':{'resultKind':const('ABSENT_PENDING')}}}},'then':{'properties':{'allegedOutcome':const('INDETERMINATE')}}})
        if row_id=='C09':body['allOf']=[condition('evidencePosture','MEASURED',{'required':['measurementSource']},{'not':{'required':['measurementSource']}})]
        if row_id=='C11':
            body['allOf']=[condition('statusKind',kind,{'properties':{'allegedStatus':enum(values+['UNKNOWN'])}}) for kind,values in {'REGISTRATION':['REGISTERED','NOT_REGISTERED'],'ACTIVE_PASSIVE':['ACTIVE','PASSIVE'],'SUBMISSION':['SUBMITTED','NOT_SUBMITTED'],'RENEWAL':['RENEWED','NOT_RENEWED']}.items()]
        subject={'allOf':[ref('domainSubject'),{'properties':{'subjectType':enum(row['subjectKinds'])}}]}
        atom=obj({'form':const('ATOM'),'atomId':TEXT,'definition':const(DEFINITION_PREFIX+row_id),
            'scope':obj({'subject':subject,'subjectTime':one(*[{'$ref':BASE_ID+'#/$defs/'+p} for p in row['subjectTimeProfiles']]),'extent':vref('extent')}),'body':body})
        if row_id.startswith('O'):
            atom['allOf']=[{'if':{'properties':{'scope':{'properties':{'subjectTime':{'properties':{'profile':const('INTENDED_WINDOW')}}}}}},
                           'then':{'properties':{'body':{'properties':{'claimPosture':const('INTENDED')}}}},
                           'else':{'properties':{'body':{'properties':{'claimPosture':const('PERFORMED')}}}}}]
            if row_id=='O22':
                profile_rules=reviewed('reviewed-input/domain/operation-profile-contract.json')['O22OutputContract']['byProfileAndFacet']
                for profile,facets in profile_rules.items():
                    for facet,allowed in facets.items():atom['allOf'].append({'if':{'properties':{'scope':{'properties':{'subjectTime':{'properties':{'profile':const(profile)}}}},'body':{'properties':{'performanceFacet':const(facet)}}}},'then':{'properties':{'body':{'properties':{'parameters':{'properties':{'producedResult':{'properties':{'role':enum(allowed)}}}}}}}}})
            if row_id=='O23':atom['allOf'].append({'if':{'properties':{'body':{'properties':{'claimPosture':const('INTENDED')}}}},'then':{'properties':{'body':{'properties':{'parameters':{'properties':{'report':{'properties':{'role':const('INTENDED_REPORT_OR_SELECTION')}}}}}}}},'else':{'properties':{'body':{'properties':{'parameters':{'properties':{'report':{'properties':{'role':const('ACTUAL_REPORT')}}}}}}}}})
        defs[row_id]=atom
        trace.append({'row':row_id,'sourceDefinition':row['conceptRevision'],'newDefinition':DEFINITION_PREFIX+row_id,
            'sourceRequiredFields':contract['requiredBodyFields'],'requiredFields':required,'optionalFields':optional,
            'explicitAmendment':change,'subjectKinds':row['subjectKinds'],'subjectPostures':['EXISTING_SUBJECT','PROSPECTIVE_SUBJECT'],
            'semanticLimits':'Field typing alone does not establish selected-source meaning, admission or the outer carrier prospective-subject obligations.'})
    defs['atom']=one(*[ref(name) for name in rows])
    defs['qualifiers']=obj({'epistemicPosture':enum(['ALLEGED','SUSPECTED','ESTIMATED','DISPUTED']),
        'sourceQuality':enum(['MEASURED','HUMAN_REPORTED','MACHINE_REPORTED','ESTIMATED','DEGRADED','DISPUTED','UNKNOWN']),
        'extentQualification':enum(['PARTIAL_ONLY','FULL_EXTENT','ESTIMATED_EXTENT','DISPUTED_EXTENT'])},[])
    defs['qualifiers']['minProperties']=1
    defs['all']=obj({'form':const('ALL'),'children':arr(ref('proposition'),1)})
    defs['any']=obj({'form':const('ANY'),'children':arr(ref('proposition'),1)})
    defs['not']=obj({'form':const('NOT'),'child':ref('proposition')})
    defs['qualified']=obj({'form':const('QUALIFIED'),'appliesToAtomId':TEXT,'child':ref('atom'),'qualifiers':ref('qualifiers')})
    defs['sequence']=obj({'form':const('SEQUENCE'),'children':arr(ref('proposition'),1),'orderRelations':arr(obj({'beforeAtomId':TEXT,'afterAtomId':TEXT,'temporalRelation':const('BEFORE')}),0,True)})
    defs['proposition']=one(ref('atom'),ref('all'),ref('any'),ref('not'),ref('qualified'),ref('sequence'))
    schema={'$schema':'https://json-schema.org/draft/2020-12/schema','$id':SCHEMA_ID,'title':'Explicit candidate proposition and 58 atom field contracts',
        '$comment':'New draft domain grammar. No foreign evidence admission or authority-anchor extension. Exact field definitions are authored from source rules; examples are regression data. Literal fields require exact selected-definition/source checks and never become executable policy from their spelling.',
        '$ref':'#/$defs/proposition','$defs':defs}
    put('proposition.schema.json',schema);put('field-contract-ledger.json',{'sourceHead':HEAD,'rows':trace,'counts':{'rows':len(rows),'completeSemanticEvaluatorClaims':0},'next':'Verify the complete row field contracts and implement their source-backed intrinsic and carrier comparisons.'})
    print(json.dumps({'explicitAtomFieldContracts':len(rows),'schemaId':SCHEMA_ID,'export':'#/$defs/proposition','definitionPrefix':DEFINITION_PREFIX}))
if __name__=='__main__':main()
