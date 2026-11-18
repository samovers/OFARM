"""Normative work and condition definitions; no factual witness is authored."""
from definition_inputs import obj,schema,BINDING,TEXT,PROPOSITION
from activity_condition_meanings import PREDICATE_KINDS
from completion_count_meanings import COUNTS

SCHEMAS={
 'work':schema('work-specification-definition','ofarm.assertionDomainWorkSpecificationDefinition.v0.1',{
    'activityRow':{'enum':['O'+str(n).zfill(2) for n in range(1,28)]},
    'activityInstance':BINDING,'procedure':BINDING,
    'target':{'$ref':PROPOSITION+'#/$defs/typedBinding'},
    'extent':{'$ref':'https://ofarm.dev/schema/drafts/non-default/assertion-domain/owned-value-types/v0.1#/$defs/extent'},
    'intendedPerformer':BINDING,
    'parameters':{'anyOf':[{'$ref':PROPOSITION+'#/$defs/O'+str(n).zfill(2)+'/properties/body/properties/parameters'} for n in range(1,28)]},
    'startConditions':{'type':'array','minItems':1,'items':obj({'conditionId':TEXT,'definitionBinding':BINDING})},
    'inProgressConditions':{'type':'array','minItems':1,'items':obj({'conditionId':TEXT,'definitionBinding':BINDING})},
    'finishConditions':{'type':'array','minItems':1,'items':obj({'conditionId':TEXT,'definitionBinding':BINDING})},
    'outputSpecification':{'oneOf':[BINDING,{'type':'null'}]},
    'carrierMeaning':obj({'actionType':TEXT,'interventionKind':{'type':['string','null']},
                          'specificActivity':{'type':['string','null']},'methodBinding':{'oneOf':[BINDING,{'type':'null'}]}}),
 }),
 'workCondition':schema('work-condition-definition','ofarm.assertionDomainWorkConditionDefinition.v0.1',{
    'conditionId':TEXT,'activityRow':{'enum':['O'+str(n).zfill(2) for n in range(1,28)]},
    'stage':{'enum':['START','IN_PROGRESS','FINISH']},'meaning':TEXT,
    'predicateKind':{'enum':PREDICATE_KINDS},
    'criterionBinding':{'oneOf':[BINDING,{'type':'null'}]},
    'measurementBinding':{'oneOf':[BINDING,{'type':'null'}]},
    'resultTerms':obj({'codedValues':{'type':'array','items':BINDING},'qualitativeScale':{'oneOf':[BINDING,{'type':'null'}]}}),
    'temporalRole':{'enum':['AT_WORK_START','DURING_WORK','AT_WORK_FINISH']},
 }),
}
SCHEMAS['workCondition']['properties']['acquisitionSpecificationBinding']=BINDING
SCHEMAS['workCondition']['properties']['dryingSpecificationBinding']=BINDING
SCHEMAS['workCondition']['properties']['irrigationSpecificationBinding']=BINDING
SCHEMAS['workCondition']['properties']['sanitationSpecificationBinding']=BINDING
SCHEMAS['workCondition']['allOf']=[{
    'if':{'properties':{'predicateKind':{'enum':['ANALYSIS_OUTPUT_RECORDED','REQUIRED_OBSERVATIONS_ACQUIRED_AND_RECORDED']}}},
    'then':{'properties':{'stage':{'const':'FINISH'},'criterionBinding':{'type':'null'},'measurementBinding':{'type':'null'},
        'resultTerms':{'const':{'codedValues':[],'qualitativeScale':None}}}},
    'else':{'properties':{'criterionBinding':BINDING,'measurementBinding':BINDING}},
},{'if':{'properties':{'predicateKind':{'const':'ANALYSIS_OUTPUT_RECORDED'}}},
   'then':{'properties':{'activityRow':{'const':'O22'}}}},
  {'if':{'properties':{'predicateKind':{'const':'REQUIRED_OBSERVATIONS_ACQUIRED_AND_RECORDED'}}},
   'then':{'properties':{'activityRow':{'const':'O09'}},'required':['acquisitionSpecificationBinding']},
   'else':{'not':{'required':['acquisitionSpecificationBinding']}}},
  {'if':{'properties':{'predicateKind':{'const':'TARGET_MOISTURE_ON_DEFINED_MASS_BASIS'}}},
   'then':{'properties':{'activityRow':{'const':'O07'},'stage':{'const':'FINISH'}},'required':['dryingSpecificationBinding']},
   'else':{'not':{'required':['dryingSpecificationBinding']}}},
  {'if':{'properties':{'predicateKind':{'enum':['IRRIGATION_REQUIRED_VOLUME_DELIVERED','IRRIGATION_INFLOW_ZERO_AT_FINISH']}}},
   'then':{'properties':{'activityRow':{'const':'O04'},'stage':{'const':'FINISH'}},'required':['irrigationSpecificationBinding']},
   'else':{'not':{'required':['irrigationSpecificationBinding']}}},
  {'if':{'properties':{'predicateKind':{'enum':['SANITATION_REQUIRED_CONTINUOUS_MATERIAL_CONTACT','SANITATION_PROCEDURE_INACTIVE_AT_FINISH']}}},
   'then':{'properties':{'activityRow':{'const':'O17'},'stage':{'const':'FINISH'}},'required':['sanitationSpecificationBinding']},
   'else':{'not':{'required':['sanitationSpecificationBinding']}}}]
for row, (predicate, _, _) in COUNTS.items():
    SCHEMAS['workCondition']['allOf'].append({
        'if': {'properties': {'predicateKind': {'const': predicate}}},
        'then': {'properties': {'activityRow': {'const': row}, 'stage': {'const': 'FINISH'}}},
    })



def register(schemas):
    from definition_inputs import register as register_criterion
    from referencing import Resource
    register_criterion(schemas)
    for value in SCHEMAS.values():
        schemas.schemas[value['$id']]=value
        schemas.registry=schemas.registry.with_resource(value['$id'],Resource.from_contents(value))
