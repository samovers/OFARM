"""Selected normative drying finish meaning, never a moisture observation."""
from definition_inputs import schema, obj, BINDING, TEXT, PROPOSITION

SCHEMAS = {'drying': schema('drying-finish-specification',
    'ofarm.assertionDomainDryingFinishSpecification.v0.1', {
        'activityRow': {'const': 'O07'},
        'workSpecificationBinding': BINDING, 'procedureBinding': BINDING,
        'inputLot': BINDING,
        'targetMoistureParameter': {'$ref': PROPOSITION + '#/$defs/O07/properties/body/properties/quantityParameters/items'},
        'propertyBinding': BINDING,
        'quantityContext': obj({'quantityKind': TEXT, 'unit': TEXT, 'unitProfile': BINDING}),
        'ratioMeaning': obj({'numerator': {'const': 'WATER_MASS'},
            'massBasis': {'enum': ['WET_BASIS', 'DRY_BASIS']},
            'denominator': {'enum': ['TOTAL_WET_MASS', 'DRY_SOLIDS_MASS']},
            'scale': {'enum': [1, 100]}}),
        'thresholdOperator': {'enum': ['LE', 'LT']},
        'targetThresholdMeaning': {'const': 'SELECTED_UPPER_BOUND_WITH_REPORTING_QUALIFICATIONS_RETAINED'},
        'finishConditionIds': {'type': 'array', 'minItems': 1, 'uniqueItems': True, 'items': TEXT},
        'interpretationScope': {'const': 'MOISTURE_TARGET_AND_EVERY_BOUND_PROCEDURE_FINISH_CONDITION'},
    })}

SCHEMAS['drying']['allOf'] = [{
    'if': {'properties': {'ratioMeaning': {'properties': {'massBasis': {'const': 'WET_BASIS'}}}}},
    'then': {'properties': {'ratioMeaning': {'properties': {'denominator': {'const': 'TOTAL_WET_MASS'}}}}},
    'else': {'properties': {'ratioMeaning': {'properties': {'denominator': {'const': 'DRY_SOLIDS_MASS'}}}}},
}]


def register(schemas):
    from referencing import Resource
    for value in SCHEMAS.values():
        schemas.schemas[value['$id']] = value
        schemas.registry = schemas.registry.with_resource(value['$id'], Resource.from_contents(value))
