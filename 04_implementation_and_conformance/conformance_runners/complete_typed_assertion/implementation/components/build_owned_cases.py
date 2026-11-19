"""Independent expected cases. Does not import or execute the component.

These are authored mathematical and source-rule expectations, not outcomes
copied from a verifier run. Fictional values establish no admitted facts.
"""
import copy,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
def binding(name):return {'ref':'fiction:'+name,'revisionRef':'r1'}
T0='2026-05-07T10:00:00Z';T1='2026-05-07T11:00:00Z'
SUBJECT={'kind':'FIELD','binding':binding('field')}
EXTENT={'posture':'FULL_TARGET_SCOPE','binding':binding('field')}
Q={
    'parameterId':'q:rate','parameterRole':'RATE','activityInstance':binding('activity'),'valuePosture':'ACTUAL',
    'material':{'presence':'PRESENT','materialRole':'PRODUCT','binding':binding('product')},
    'basis':{'presence':'PRESENT','quantity':{'quantityKind':'AREA','unit':'ha','decimal':'1'},'subject':SUBJECT},
    'value':{'state':'STATED','quantity':{'quantityKind':'VOLUME','unit':'L','decimal':'2.00'},'qualifier':'HUMAN_REPORTED',
        'unitProfile':binding('units'),'original':{'presence':'PRESENT','lexicalValue':'2.00','unitText':'L','sourceBinding':binding('quantity-source'),'sourcePointer':'/reported/rate'}},
    'appliesTo':{'target':SUBJECT,'extent':EXTENT,'subjectTime':{'profile':'PERFORMED_INTERVAL','start':T0,'end':T1},'processPoint':binding('nozzle'),'phase':'WHOLE_ACTIVITY'},
}
RESULTS=[
    {'resultKind':'NUMERIC','quantityKindRef':'quantity:mass-fraction','unitRef':'unit:mg-kg','numericValue':2,'originalLexicalValue':'2.00','originalUnitText':'mg/kg'},
    {'resultKind':'CODED','codedValueRef':'code:detected'},
    {'resultKind':'QUALITATIVE','qualitativeValue':'Visible spot on sampled leaf'},
    {'resultKind':'CENSORED_NUMERIC','quantityKindRef':'quantity:mass-fraction','unitRef':'unit:mg-kg','censoringQualifier':'BELOW_LOQ','detectionLimit':{'limitType':'LOQ','quantityKindRef':'quantity:mass-fraction','unitRef':'unit:mg-kg','value':2},'originalLexicalValue':'< 2 mg/kg'},
    {'resultKind':'ABSENT_PENDING','qualifierNote':'Assay pending; collection does not imply a result'},
]
NL={
    'form':'PROFILE_ROUTE_OUTCOME','profile':'profile:nl.go-glmc7.2026.v0_1','claimYear':2026,
    'route':'ORGANIC_OR_IN_CONVERSION','routeScope':'PARCEL','parcel':binding('nl-parcel'),
    'historyClaim':binding('nl-history'),'soilCategory':'SAND_OR_LOESS','soilEvidence':binding('nl-soil'),
    'rustgewasEvidence':binding('nl-rustgewas'),'routeEvidence':binding('nl-route'),
    'evaluationBasis':{'kind':'PROFILE_OWNER_EVALUATION','binding':binding('nl-evaluation')},
    'allegedOutcome':'INDETERMINATE','reviewState':'PENDING',
}
# Separate selected context, with no success/admission bit or alleged outcome.
NL_EXPECTED={
    'profile':'profile:nl.go-glmc7.2026.v0_1','claimYear':2026,'route':'ORGANIC_OR_IN_CONVERSION','routeScope':'PARCEL',
    'parcel':binding('nl-parcel'),'historyClaim':binding('nl-history'),'soilCategory':'SAND_OR_LOESS',
    'soilEvidence':binding('nl-soil'),'rustgewasEvidence':binding('nl-rustgewas'),'routeEvidence':binding('nl-route'),
    'evaluationBasis':{'kind':'PROFILE_OWNER_EVALUATION','binding':binding('nl-evaluation')},
}

def main():
    cases=[]
    def add(name,method,args,valid=True,outcome=None,category='intrinsic'):
        cases.append({'id':name,'category':category,'method':method,'args':copy.deepcopy(args),
                      'expected':{'valid':valid,**({'outcome':outcome} if outcome is not None else {})}})
    add('quantity/base','quantity_errors',[Q],category='explicit-value-types')
    # All optional quantity fields and disclosure variants, including forms
    # absent from the finite reviewed examples.
    v=copy.deepcopy(Q);v['sourceParameterBinding']=binding('source-parameter');v['value']['normalized']={'quantityKind':'VOLUME','unit':'mL','decimal':'2000','conversionBinding':binding('conversion')}
    add('quantity/normalized-with-source-parameter','quantity_errors',[v],category='unexemplified-valid')
    v=copy.deepcopy(Q);v['value']['original']['presence']='UNREPORTED';v['value']['original']['lexicalValue']=None;v['value']['original']['unitText']=None
    add('quantity/original-explicitly-unreported','quantity_errors',[v],category='unexemplified-valid')
    for role in ['RATE','DOSE','CONCENTRATION','TOTAL_QUANTITY','CARRIER_VOLUME','WATER_VOLUME','SEED_RATE','NUTRIENT_RATE','PRESSURE','FLOW_RATE','SPEED','TIMING_INTERVAL','APPLICATION_VOLUME','OTHER_PARAMETER']:
        v=copy.deepcopy(Q);v['parameterRole']=role
        if role=='APPLICATION_VOLUME':v['applicationMaterialInterpretation']='AS_IDENTIFIED_MATERIAL'
        if role=='OTHER_PARAMETER':v['otherRoleDefinition']='MATERIAL_HANDLED'
        add('quantity/role/'+role,'quantity_errors',[v],category='role-type-only')
    for role in ['PRODUCT','ACTIVE_SUBSTANCE','CARRIER','WATER','SEED','FERTILIZER','NUTRIENT','OTHER_MATERIAL']:
        v=copy.deepcopy(Q);v['material']['materialRole']=role
        if role=='OTHER_MATERIAL':v['material']['materialDefinition']=binding('material-definition')
        add('quantity/material/'+role,'quantity_errors',[v],category='role-type-only')
    for posture in ['ACTUAL','PLANNED','TARGET','LIMIT']:
        v=copy.deepcopy(Q);v['valuePosture']=posture;add('quantity/posture/'+posture,'quantity_errors',[v],category='explicit-value-types')
    for qualifier in ['EXACT','ESTIMATED','MINIMUM','MAXIMUM','RANGE_MIDPOINT','LABEL_LIMIT','MACHINE_REPORTED','HUMAN_REPORTED','UNKNOWN']:
        v=copy.deepcopy(Q);v['value']['qualifier']=qualifier;add('quantity/qualifier/'+qualifier,'quantity_errors',[v],category='role-type-only')
    for role in ['DEPTH','MOISTURE_TARGET','TREATED_AREA','TREATED_AMOUNT','MATERIAL_HANDLED']:
        v=copy.deepcopy(Q);v['parameterRole']='OTHER_PARAMETER';v['otherRoleDefinition']=role
        if role=='MOISTURE_TARGET':v['basis']['massBasis']='DRY_BASIS'
        add('quantity/other-role/'+role,'quantity_errors',[v],category='unexemplified-valid')
    v=copy.deepcopy(Q);v['value']={'state':'UNREPORTED','reason':'No quantity reported'};v['material']={'presence':'UNREPORTED','reason':'No material identity reported'};v['basis']={'presence':'UNREPORTED','reason':'No denominator reported'}
    add('quantity/unreported-not-zero','quantity_errors',[v],category='unexemplified-valid')
    v=copy.deepcopy(Q);v['parameterRole']='PRESSURE';v['material']={'presence':'NOT_APPLICABLE','reason':'Pressure at process point'};v['basis']={'presence':'NOT_APPLICABLE','reason':'Non-ratio pressure quantity'};v['value']['quantity']={'quantityKind':'PRESSURE','unit':'bar','decimal':'2'}
    add('quantity/non-ratio-process','quantity_errors',[v],category='unexemplified-valid')
    mixture=copy.deepcopy(Q);mixture['parameterRole']='APPLICATION_VOLUME';mixture['applicationMaterialInterpretation']='MIXTURE_AS_APPLIED';mixture['material']={'presence':'PRESENT','materialRole':'OTHER_MATERIAL','binding':binding('mixture'),'materialDefinition':binding('recipe'),'components':[{'materialRole':'PRODUCT','binding':binding('product')},{'materialRole':'WATER','binding':binding('water')}]}
    add('quantity/mixture','quantity_errors',[mixture],category='explicit-value-types')
    v=copy.deepcopy(mixture);v['material']['components'][1]['binding']=binding('product');add('quantity/duplicate-components','quantity_errors',[v],False)
    v=copy.deepcopy(mixture);v['material']['binding']=binding('product');add('quantity/mixture-is-component','quantity_errors',[v],False)
    v=copy.deepcopy(mixture);v['applicationMaterialInterpretation']='UNRESOLVED_SOURCE_MATERIAL';v['material']={'presence':'UNREPORTED','reason':'Applied material not identified'};add('quantity/unresolved-application','quantity_errors',[v],category='unexemplified-valid')
    for path,value in [(['parameterRole'],'UNKNOWN_ROLE'),(['valuePosture'],'PERFORMED'),(['value','qualifier'],'LAB_AUTOMATIC'),(['value','quantity','decimal'],'1e3'),(['value','quantity','decimal'],'1\n'),(['value','quantity','decimal'],True),(['material','materialRole'],'DRUG'),(['material','presence'],'UNREPORTED'),(['basis','massBasis'],'GUESS'),(['value','original','sourcePointer'],'/bad~2escape'),(['otherRoleDefinition'],'DEPTH'),(['applicationMaterialInterpretation'],'AS_IDENTIFIED_MATERIAL')]:
        v=copy.deepcopy(Q);d=v
        for key in path[:-1]:d=d[key]
        d[path[-1]]=value;add('quantity/invalid/'+('/'.join(path))+'/'+str(value),'quantity_errors',[v],False)
    for path in [[],['material'],['basis'],['value'],['value','quantity'],['value','original'],['appliesTo'],['appliesTo','target'],['appliesTo','extent']]:
        v=copy.deepcopy(Q);d=v
        for key in path:d=d[key]
        d['unknownMember']=True;add('quantity/closed/'+('/'.join(path) or 'root'),'quantity_errors',[v],False)
    for key in ['parameterId','parameterRole','activityInstance','valuePosture','material','basis','value','appliesTo']:
        v=copy.deepcopy(Q);del v[key];add('quantity/missing/'+key,'quantity_errors',[v],False)
    for role in ['RATE','DOSE','CONCENTRATION','TOTAL_QUANTITY','CARRIER_VOLUME','WATER_VOLUME','SEED_RATE','NUTRIENT_RATE','FLOW_RATE','APPLICATION_VOLUME']:
        v=copy.deepcopy(Q);v['parameterRole']=role;v['material']={'presence':'NOT_APPLICABLE','reason':'An unsupported assertion of non-applicability'}
        if role=='APPLICATION_VOLUME':v['applicationMaterialInterpretation']='AS_IDENTIFIED_MATERIAL'
        add('quantity/material-not-applicable/'+role,'quantity_errors',[v],False,category='material-basis-gates')
    for role in ['RATE','DOSE','CONCENTRATION','SEED_RATE','NUTRIENT_RATE','FLOW_RATE','SPEED','APPLICATION_VOLUME']:
        v=copy.deepcopy(Q);v['parameterRole']=role;v['basis']={'presence':'NOT_APPLICABLE','reason':'An unsupported assertion of non-ratio quantity'}
        if role=='APPLICATION_VOLUME':v['applicationMaterialInterpretation']='AS_IDENTIFIED_MATERIAL'
        add('quantity/ratio-basis-not-applicable/'+role,'quantity_errors',[v],False,category='material-basis-gates')
    add('quantity/context-exact','quantity_context_errors',[Q,Q],category='quantity-context-gates')
    for field,value in [('parameterRole','DOSE'),('valuePosture','PLANNED'),('activityInstance',binding('other-activity')),('material',{'presence':'PRESENT','materialRole':'PRODUCT','binding':binding('other-product')}),('basis',{'presence':'PRESENT','quantity':{'quantityKind':'AREA','unit':'ha','decimal':'2'},'subject':SUBJECT})]:
        v=copy.deepcopy(Q);v[field]=value;add('quantity/context-mismatch/'+field,'quantity_context_errors',[v,Q],False,category='quantity-context-gates')
    for field,value in [('subjectTime',{'profile':'PERFORMED_INTERVAL','start':'2026-05-07T09:00:00Z','end':T1}),('extent',{'posture':'PARTIAL_TARGET_SCOPE','binding':binding('half-field')}),('target',{'kind':'FIELD','binding':binding('other-field')}),('phase','OTHER_PHASE')]:
        v=copy.deepcopy(Q);v['appliesTo'][field]=value;add('quantity/context-mismatch/'+field,'quantity_context_errors',[v,Q],False,category='quantity-context-gates')
    for field in ['material','basis']:
        v=copy.deepcopy(Q);v[field]={'presence':'UNREPORTED','reason':'Source omitted this role'};add('quantity/unresolved-context/'+field,'quantity_context_errors',[v,v],False,category='quantity-context-gates')

    # Independent exact arithmetic vectors: no evaluator-produced oracle.
    vectors=[
        ('LE','0','2','1',True,False,'INDETERMINATE'),
        ('LE','0','2','2',True,False,'SATISFIED'),('LE','2',None,'2',False,True,'NOT_SATISFIED'),
        ('LT',None,'2','2',True,False,'SATISFIED'),('LT',None,'2','2',True,True,'INDETERMINATE'),
        ('LT','2',None,'2',True,True,'NOT_SATISFIED'),('GE','2',None,'2',True,True,'SATISFIED'),
        ('GE',None,'2','2',True,False,'NOT_SATISFIED'),('GE',None,'2','2',True,True,'INDETERMINATE'),
        ('GT','2',None,'2',False,True,'SATISFIED'),('GT','2',None,'2',True,True,'INDETERMINATE'),
        ('GT',None,'2','2',True,True,'NOT_SATISFIED'),('EQ','2','2','2.00',True,True,'SATISFIED'),
        ('EQ','2','3','2',False,True,'NOT_SATISFIED'),('EQ','1','3','2',True,True,'INDETERMINATE'),
        ('NE','2','2','2',True,True,'NOT_SATISFIED'),('NE','2','3','2',False,True,'SATISFIED'),
        ('NE','1','3','2',True,True,'INDETERMINATE'),('LE',None,None,'2',True,True,'INDETERMINATE'),
        ('EQ','0.10000000000000000001','0.10000000000000000001','0.1',True,True,'NOT_SATISFIED'),
    ]
    for i,v in enumerate(vectors):add('math/'+str(i),'interval_outcome',list(v[:-1]),outcome=v[-1],category='mathematical-expectation')
    for i,args in enumerate([['LE','2','1','2'],['LE','2','2','2',False,True],['LE','NaN','3','2'],['OTHER','1','2','2'],['LE','1','2','2',1,True]]):add('math/invalid/'+str(i),'interval_outcome',args,False)
    for form,children,outcome in [('ALL',['TRUE','INDETERMINATE'],'INDETERMINATE'),('ALL',['TRUE','FALSE'],'FALSE'),('ALL',['TRUE'],'TRUE'),('ANY',['FALSE','INDETERMINATE'],'INDETERMINATE'),('ANY',['INDETERMINATE','TRUE'],'TRUE'),('ANY',['FALSE'],'FALSE'),('NOT',['INDETERMINATE'],'INDETERMINATE'),('NOT',['FALSE'],'TRUE'),('NOT',['TRUE'],'FALSE'),('SEQUENCE',['TRUE','FALSE'],'FALSE')]:add('algebra/'+form+'-'+','.join(children),'composed_outcome',[form,children],outcome=outcome,category='proposition-algebra')
    for form,children in [('ALL',[]),('NOT',['TRUE','FALSE']),('UNKNOWN',['TRUE']),('ANY',[True])]:add('algebra/invalid/'+form,'composed_outcome',[form,children],False)

    profiles={
        'STRUCTURE_AS_OF':{'at':T0},'STRUCTURE_EFFECTIVE_FROM':{'start':T0},'STRUCTURE_EFFECTIVE_INTERVAL':{'start':T0,'end':T1},
        'COMPLIANCE_AS_OF':{'at':T0},'COMPLIANCE_EFFECTIVE_FROM':{'start':T0},'COMPLIANCE_EFFECTIVE_INTERVAL':{'start':T0,'end':T1},
        'INTENDED_WINDOW':{'start':T0,'end':T1},'PERFORMED_INSTANT':{'at':T0},'PERFORMED_INTERVAL':{'start':T0,'end':T1},
    }
    envelope={'schemaVersion':'ofarm.semanticeventenvelope.v0.1','semanticEventId':'event:fiction','primaryEventFamily':'OccurrenceEvent','dominantSemanticConsequence':'Fictional observed pruning completion.','anchorScopes':[{'scopeType':'FARM','scopeRef':'farm:fiction'}],'subjectRefs':['field:fiction'],'timeSemantics':{'recordTime':T1,'eventTime':T0,'observationTime':T0,'decisionTime':T0,'effectiveFrom':T0,'effectiveUntil':T1}}
    for profile,fields in profiles.items():
        t={'profile':profile,**fields};add('time/'+profile,'time_errors',[t],category='nine-time-profiles')
        add('event-absence/'+profile,'event_time_errors',[t,None,None],category='17-event-profile-cells')
        selector=['/timeSemantics/effectiveFrom','/timeSemantics/effectiveUntil'] if 'end' in fields else '/timeSemantics/effectiveFrom' if 'start' in fields else '/timeSemantics/eventTime'
        add('event-presence/'+profile,'event_time_errors',[t,envelope,selector],profile!='INTENDED_WINDOW',category='17-event-profile-cells' if profile!='INTENDED_WINDOW' else 'prohibited-event-cell')
        if profile!='INTENDED_WINDOW':
            bad=copy.deepcopy(envelope);bad['timeSemantics'].pop('effectiveUntil' if 'end' in fields else selector.rsplit('/',1)[-1]);add('event/missing-selected-time/'+profile,'event_time_errors',[t,bad,selector],False)
    for profile in ['STRUCTURE_AS_OF','COMPLIANCE_AS_OF','PERFORMED_INSTANT']:
        for selector in ['eventTime','observationTime','decisionTime','effectiveFrom']:
            add('event/selector/'+profile+'/'+selector,'event_time_errors',[{'profile':profile,'at':T0},envelope,'/timeSemantics/'+selector],category='selected-time-comparison')
    add('event/record-time-forbidden','event_time_errors',[{'profile':'PERFORMED_INSTANT','at':T1},envelope,'/timeSemantics/recordTime'],False)
    for stamp in ['2026-02-30T00:00:00Z','2026-05-07T10:00:00.100Z','2026-05-07T10:00:00+00:00','2026-05-07T10:00:00.1234567891Z']:
        add('time/invalid/'+stamp,'time_errors',[{'profile':'PERFORMED_INSTANT','at':stamp}],False)
    add('time/nanosecond-distinct','time_errors',[{'profile':'PERFORMED_INTERVAL','start':'2026-05-07T10:00:00.123456788Z','end':'2026-05-07T10:00:00.123456789Z'}],category='unexemplified-valid')
    add('time/nanosecond-reversed','time_errors',[{'profile':'PERFORMED_INTERVAL','start':'2026-05-07T10:00:00.123456789Z','end':'2026-05-07T10:00:00.123456788Z'}],False)
    outputs=[{'role':'PROSPECTIVE_OUTPUT_SPECIFICATION','specificationBinding':binding('output-spec')},{'role':'PENDING_OUTPUT','specificationBinding':binding('output-spec'),'outputState':'NOT_YET_PRODUCED'},{'role':'ACTUAL_OUTPUT','specificationBinding':binding('output-spec'),'binding':binding('output')}]
    for profile in ['INTENDED_WINDOW','PERFORMED_INSTANT','PERFORMED_INTERVAL']:
        for facet in ['OCCURRENCE','STARTED','IN_PROGRESS','COMPLETED']:
            # Independent table from the authored O22 rule, not its evaluator.
            allowed={'PROSPECTIVE_OUTPUT_SPECIFICATION'} if profile=='INTENDED_WINDOW' else {'ACTUAL_OUTPUT'} if facet=='COMPLETED' else {'PENDING_OUTPUT','ACTUAL_OUTPUT'}
            for output in outputs:add('O22/'+profile+'/'+facet+'/'+output['role'],'analysis_output_errors',[output,{'profile':profile,**profiles[profile]},'INTENDED' if profile=='INTENDED_WINDOW' else 'PERFORMED',facet,binding('output-spec')],output['role'] in allowed,category='O22-profile-facet-output-matrix')
            for output in outputs:
                target={'kind':'OPERATION','binding':binding('analysis-operation')};extent={'posture':'FULL_TARGET_SCOPE','binding':binding('analysis-operation')}
                atom={'form':'ATOM','atomId':'atom:analysis','definition':'candidate:assertion-domain-construction:2026-10-21:O22','scope':{'subject':target,'extent':extent,'subjectTime':{'profile':profile,**profiles[profile]}},'body':{'activity':'PRODUCE_ANALYSIS_RESULT','interventionKind':'OTHER_INTERVENTION','claimPosture':'INTENDED' if profile=='INTENDED_WINDOW' else 'PERFORMED','performanceFacet':facet,'activityInstance':binding('analysis-work'),'target':target,'extent':extent,'performedBy':binding('analyst'),'parameters':{'method':binding('analysis-method'),'sample':binding('sample'),'property':binding('property'),'producedResult':output},'quantityParameters':[],'workSpecification':{'binding':binding('analysis-spec'),'activityInstance':binding('analysis-work'),'procedure':binding('analysis-method'),'target':target,'extent':extent,'startConditionIds':['analysis:start'],'inProgressConditionIds':['analysis:progress'],'finishConditionIds':['analysis:finish'],'outputSpecification':binding('output-spec')}}}
                add('O22-full-row/'+profile+'/'+facet+'/'+output['role'],'check_explicit_o22',[atom],output['role'] in allowed,category='explicit-O22-row-matrix')
    # The last independently constructed atom is performed-interval completed
    # with actual output. Exercise new field combinations, not another sample.
    extra_quantity=copy.deepcopy(Q);extra_quantity['activityInstance']=binding('analysis-work');extra_quantity['appliesTo']['target']=copy.deepcopy(atom['body']['target']);extra_quantity['appliesTo']['extent']=copy.deepcopy(atom['body']['extent']);extra_quantity['value']['normalized']={'quantityKind':'VOLUME','unit':'mL','decimal':'2000','conversionBinding':binding('conversion')}
    extended=copy.deepcopy(atom);extended['body']['quantityParameters']=[extra_quantity]
    add('O22-full-row/unexemplified-normalized-quantity','check_explicit_o22',[extended],category='unexemplified-valid')
    for path,value in [(['body','parameters','method'],binding('other-method')),(['body','workSpecification','activityInstance'],binding('other-work')),(['body','workSpecification','finishConditionIds'],[]),(['body','performanceFacet'],'HAPPENED'),(['body','claimPosture'],'INTENDED'),(['body','parameters','producedResult','outputState'],'UNREPORTED')]:
        v=copy.deepcopy(atom);d=v
        for key in path[:-1]:d=d[key]
        d[path[-1]]=value;add('O22-full-row/invalid/'+('/'.join(path)),'check_explicit_o22',[v],False)
    pending=copy.deepcopy(outputs[1]);pending['outputState']='UNREPORTED';add('O22/pending-unreported','analysis_output_errors',[pending,{'profile':'PERFORMED_INSTANT','at':T0},'PERFORMED','STARTED',binding('output-spec')],category='unexemplified-valid')
    pending['binding']=binding('invented-result');add('O22/pending-forbids-result','analysis_output_errors',[pending,{'profile':'PERFORMED_INSTANT','at':T0},'PERFORMED','STARTED',binding('output-spec')],False)
    add('O22/wrong-specification','analysis_output_errors',[outputs[2],{'profile':'PERFORMED_INSTANT','at':T0},'PERFORMED','COMPLETED',binding('another-spec')],False)

    for result in RESULTS:
        kind=result['resultKind'];add('measurement/fidelity/'+kind,'measurement_result_errors',[result,result],category='five-result-forms')
        changed=copy.deepcopy(result);changed['qualifierNote']='Changed meaning';add('measurement/changed/'+kind,'measurement_result_errors',[result,changed],False)
        for role in ['OBSERVED_TIME','SAMPLE_TIME','RESULT_TIME','RECORD_TIME','ESTIMATED_TIME','ABSENT']:
            record={'schemaVersion':'ofarm.measurementevidence.v0.1','measurementEvidenceId':'measurement:fiction','evidenceClass':'FIELD_MEASUREMENT','observedPropertyRef':'property:fiction','resultTime':T1,'result':result,'source':{'sourceType':'HUMAN_OBSERVATION','sourceRef':'source:fiction','sourceCapturedAt':T1},'provenanceRefs':['provenance:fiction'],'evidenceStatus':'REPORTED','phenomenonTime':{'timeType':'INSTANT','instant':T0}}
            if role!='ABSENT':record['phenomenonTime']['timeBasis']=role
            add('measurement/time/'+kind+'/'+role,'measured_instant_errors',[record,{'profile':'PERFORMED_INSTANT','at':T0},role],category='five-results-by-six-time-roles')
            v=copy.deepcopy(record);del v['phenomenonTime'];add('measurement/no-capture-fallback/'+kind+'/'+role,'measured_instant_errors',[v,{'profile':'PERFORMED_INSTANT','at':T1},role],False)
    v=copy.deepcopy(record);v['phenomenonTime']['timeBasis']=None;add('measurement/omission-not-null','measured_instant_errors',[v,{'profile':'PERFORMED_INSTANT','at':T0},'ABSENT'],False)
    add('measurement/empty-result','measurement_result_errors',[{'resultKind':'NUMERIC'},{'resultKind':'NUMERIC'}],False)
    event_case={'subtypePresence':'PRESENT','eventSubtypeId':'candidate/pruning-completion','dominantSemanticConsequence':'Fictional observed pruning completion.'}
    selected_event=copy.deepcopy(envelope);selected_event['eventSubtypeId']='candidate/pruning-completion'
    add('event/literal-exact','event_literal_errors',[event_case,selected_event,'OccurrenceEvent'],category='event-literal-comparison')
    for field,value in [('eventSubtypeId','candidate/spray-completion'),('dominantSemanticConsequence','Fictional observed pruning'),('primaryEventFamily','ObservationEvent')]:
        v=copy.deepcopy(selected_event);v[field]=value;add('event/literal-changed/'+field,'event_literal_errors',[event_case,v,'OccurrenceEvent'],False,category='event-literal-comparison')
    absent_case={'subtypePresence':'ABSENT','dominantSemanticConsequence':'Fictional observed pruning completion.'}
    add('event/subtype-omitted','event_literal_errors',[absent_case,envelope,'OccurrenceEvent'],category='event-literal-comparison')
    v=copy.deepcopy(envelope);v['eventSubtypeId']=None;add('event/subtype-null-not-absent','event_literal_errors',[absent_case,v,'OccurrenceEvent'],False,category='event-literal-comparison')
    for body in [NL]:add('C16/qualified-positive','qualified_nl_errors',[body,NL_EXPECTED],category='qualified-C16')
    for key,value in [('allegedOutcome','SATISFIED'),('allegedOutcome','EXEMPT'),('reviewState','ACCEPTED'),('claimYear',2027),('route','UNDER_30_HECTARES'),('routeScope','HOLDING'),('parcel',binding('other-parcel')),('routeEvidence',binding('public-current-state')),('historyClaim',binding('wrong-history'))]:
        v=copy.deepcopy(NL);v[key]=value;add('C16/hostile/'+key+'/'+str(value),'qualified_nl_errors',[v,NL_EXPECTED],False)
    for key in NL:
        v=copy.deepcopy(NL);del v[key];add('C16/missing/'+key,'qualified_nl_errors',[v,NL_EXPECTED],False)
    (HERE/'independent-cases.json').write_text(json.dumps({'status':'FICTIONAL_CONDITIONAL_COMPONENT_CASES','expectationsAuthoredWithoutEvaluator':True,'admittedFactsEstablished':False,'cases':cases},indent=2)+'\n')
    print(json.dumps({'independentCases':len(cases)}))
if __name__=='__main__':main()
