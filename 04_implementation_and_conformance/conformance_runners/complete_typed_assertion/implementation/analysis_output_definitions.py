"""Normative O22 output requirements, not a source or admission contract."""
from definition_inputs import schema, obj, BINDING, TEXT, SCHEMAS as BASE_SCHEMAS

SCHEMAS = {
    'analysisOutput': schema('analysis-output-specification', 'ofarm.assertionDomainAnalysisOutputSpecification.v0.1', {
        'activityRow': {'const': 'O22'}, 'workSpecificationBinding': BINDING,
        'procedureBinding': BINDING, 'sampleBinding': BINDING,
        'propertyBinding': BINDING, 'methodBinding': BINDING,
        'sampleTargetRelationProofBindings': {'type': 'array', 'minItems': 1, 'uniqueItems': True, 'items': BINDING},
        'sampleTarget': BASE_SCHEMAS['sampleTargetUse']['properties']['target'],
        'methodVersionRef': {'type': 'string', 'pattern': '^[A-Za-z0-9._:-]+$',
            '$comment': 'Expected original procedure version; not the selected meaning definition revision or digest.'},
        'permittedResultKinds': {'type': 'array', 'minItems': 1, 'uniqueItems': True,
            'items': {'enum': ['NUMERIC', 'CODED', 'QUALITATIVE', 'CENSORED_NUMERIC']}},
        'quantityContext': {'oneOf': [{'type': 'null'}, obj({'quantityKind': TEXT, 'unit': TEXT})]},
        'productionTimeRule': {'const': 'RESULT_TIME_WITHIN_CLAIMED_WORK_TIME'},
        'interpretationScope': {'const': 'REPORTED_OUTPUT_EXISTENCE_NOT_RESULT_TRUTH_OR_ADMISSION'},
    }),
}
SCHEMAS['analysisOutput']['required'].remove('methodVersionRef')
SCHEMAS['analysisOutput']['required'].remove('sampleTargetRelationProofBindings')
SCHEMAS['analysisOutput']['required'].remove('sampleTarget')
SCHEMAS['analysisOutput']['allOf']=[{'if':{'required':['sampleTargetRelationProofBindings']},'then':{'required':['sampleTarget']}}]


def register(schemas):
    from definition_inputs import register as base_register
    from referencing import Resource
    base_register(schemas)
    for value in SCHEMAS.values():
        schemas.schemas[value['$id']] = value
        schemas.registry = schemas.registry.with_resource(value['$id'], Resource.from_contents(value))
