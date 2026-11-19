"""A selected material-contact procedure requirement, not a hygiene finding."""
from definition_inputs import schema, obj, BINDING, TEXT, QUANTITY

CONTACT='SANITATION_REQUIRED_CONTINUOUS_MATERIAL_CONTACT'
TERMINATION='SANITATION_PROCEDURE_INACTIVE_AT_FINISH'
REPORTED_DURATION_MEANINGS={
    'EXACT':'REPORTED_POINT','HUMAN_REPORTED':'REPORTED_POINT','MACHINE_REPORTED':'REPORTED_POINT',
    'MINIMUM':'INCLUSIVE_LOWER_BOUND','MAXIMUM':'INCLUSIVE_UPPER_BOUND',
    'ESTIMATED':'REQUIRES_SELECTED_QUALIFIER_MEANING','RANGE_MIDPOINT':'REQUIRES_SELECTED_QUALIFIER_MEANING',
    'LABEL_LIMIT':'REQUIRES_SELECTED_QUALIFIER_MEANING','UNKNOWN':'REQUIRES_SELECTED_QUALIFIER_MEANING',
}


def condition(predicate,quantity_kind,operator):
    return obj({'conditionId':TEXT,'definitionBinding':BINDING,'predicateKind':{'const':predicate},
        'propertyBinding':BINDING,'quantityContext':obj({'quantityKind':{'const':quantity_kind},'unit':TEXT,'unitProfile':BINDING}),
        'operator':{'const':operator}})


SCHEMAS={'sanitation':schema('sanitation-finish-specification','ofarm.assertionDomainSanitationFinishSpecification.v0.1',{
    'activityRow':{'const':'O17'},'sanitationKind':{'const':'SANITIZE'},
    'profile':{'const':'MINIMUM_CONTINUOUS_CONTACT_ACROSS_ENTIRE_EXTENT_AND_PROCEDURE_TERMINATION'},
    'workSpecificationBinding':BINDING,'procedureBinding':BINDING,'materialBinding':BINDING,
    'contactDurationParameterId':TEXT,'reportedActualDurationMeanings':{'const':REPORTED_DURATION_MEANINGS},
    'contact':condition(CONTACT,'qudt:Time','GE'),
    'termination':condition(TERMINATION,'ofarm.quantitykind:ActivityPresence','LE'),
    'minimumContactDuration':{**QUANTITY,'properties':{**QUANTITY['properties'],'quantityKind':{'const':'qudt:Time'},'qualifier':{'const':'EXACT'}}},
    'maximumFinishActivity':{**QUANTITY,'properties':{**QUANTITY['properties'],'quantityKind':{'const':'ofarm.quantitykind:ActivityPresence'},
        'unit':{'const':'ofarm.unit:boolean'},'decimal':{'const':'0'},'qualifier':{'const':'EXACT'}}},
    'finishConditionIds':{'type':'array','minItems':2,'uniqueItems':True,'items':TEXT},
    'interpretationScope':{'const':'SELECTED_SANITATION_CONTACT_PROCEDURE_COMPLETION_NOT_ACHIEVED_HYGIENE'},
})}
SCHEMAS['sanitation']['properties']['termination']['properties']['observationDomain']={'const':'EXACT_BOOLEAN_POINT'}
SCHEMAS['sanitation']['properties']['termination']['required'].append('observationDomain')
SCHEMAS['sanitation']['properties']['contact']['properties']['conditionId']={'const':'finish:O17'}
SCHEMAS['sanitation']['properties']['termination']['properties']['quantityContext']['properties']['unit']={'const':'ofarm.unit:boolean'}


def register(schemas):
    from referencing import Resource
    for value in SCHEMAS.values():
        schemas.schemas[value['$id']]=value
        schemas.registry=schemas.registry.with_resource(value['$id'],Resource.from_contents(value))
