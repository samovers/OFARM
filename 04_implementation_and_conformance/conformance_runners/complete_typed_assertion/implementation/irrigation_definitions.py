"""Normative irrigation requirements, distinct from delivered-water evidence."""
from definition_inputs import schema, obj, BINDING, TEXT, QUANTITY

DELIVERY = 'IRRIGATION_REQUIRED_VOLUME_DELIVERED'
TERMINATION = 'IRRIGATION_INFLOW_ZERO_AT_FINISH'
REPORTED_VOLUME_MEANINGS = {
    'EXACT': 'REPORTED_POINT', 'HUMAN_REPORTED': 'REPORTED_POINT', 'MACHINE_REPORTED': 'REPORTED_POINT',
    'MINIMUM': 'INCLUSIVE_LOWER_BOUND', 'MAXIMUM': 'INCLUSIVE_UPPER_BOUND',
    'ESTIMATED': 'REQUIRES_SELECTED_QUALIFIER_MEANING', 'RANGE_MIDPOINT': 'REQUIRES_SELECTED_QUALIFIER_MEANING',
    'LABEL_LIMIT': 'REQUIRES_SELECTED_QUALIFIER_MEANING', 'UNKNOWN': 'REQUIRES_SELECTED_QUALIFIER_MEANING',
}


def condition(predicate, quantity_kind, operator):
    return obj({'conditionId': TEXT, 'definitionBinding': BINDING,
        'predicateKind': {'const': predicate}, 'propertyBinding': BINDING,
        'quantityContext': obj({'quantityKind': {'const': quantity_kind}, 'unit': TEXT, 'unitProfile': BINDING}),
        'operator': {'const': operator}})


SCHEMAS = {'irrigation': schema('irrigation-finish-specification',
    'ofarm.assertionDomainIrrigationFinishSpecification.v0.1', {
        'activityRow': {'const': 'O04'},
        'profile': {'const': 'REQUIRED_CUMULATIVE_VOLUME_AND_ZERO_INFLOW_AT_FINISH'},
        'workSpecificationBinding': BINDING, 'procedureBinding': BINDING,
        'waterSourceBinding': BINDING, 'waterVolumeParameterId': TEXT,
        'reportedActualVolumeMeanings': {'const': REPORTED_VOLUME_MEANINGS},
        'delivery': condition(DELIVERY, 'qudt:Volume', 'GE'),
        'termination': condition(TERMINATION, 'qudt:VolumeFlowRate', 'LE'),
        'minimumDeliveredVolume': {**QUANTITY, 'properties': {**QUANTITY['properties'],
            'quantityKind': {'const': 'qudt:Volume'}, 'qualifier': {'const': 'EXACT'}}},
        'maximumFinishInflow': {**QUANTITY, 'properties': {**QUANTITY['properties'],
            'quantityKind': {'const': 'qudt:VolumeFlowRate'}, 'decimal': {'const': '0'}, 'qualifier': {'const': 'EXACT'}}},
        'finishConditionIds': {'type': 'array', 'minItems': 2, 'uniqueItems': True, 'items': TEXT},
        'interpretationScope': {'const': 'EVERY_BOUND_DELIVERY_AND_TERMINATION_CONDITION_OVER_SELECTED_WORK_EXTENT'},
    })}
SCHEMAS['irrigation']['properties']['delivery']['properties']['conditionId'] = {'const': 'finish:O04'}


def register(schemas):
    from referencing import Resource
    for value in SCHEMAS.values():
        schemas.schemas[value['$id']] = value
        schemas.registry = schemas.registry.with_resource(value['$id'], Resource.from_contents(value))
