"""Owned O10 meanings; these definitions contain no factual completion witness."""
from definition_inputs import schema, BINDING, TEXT, SCHEMAS as BASE_SCHEMAS

SCHEMAS = {'sampleCollection': schema('sample-collection-specification',
    'ofarm.assertionDomainSampleCollectionSpecification.v0.1', {
        'activityRow': {'const': 'O10'},
        'workSpecificationBinding': BINDING, 'procedureBinding': BINDING,
        'sampleBinding': BINDING, 'sampledPropertyBinding': BINDING,
        'samplingProcedureBinding': BINDING, 'samplingProcedureVersionRef': TEXT,
        'collectionMeasurementBinding': BINDING, 'collectionContextBinding': BINDING,
        'sampleTargetRelationProofBindings': {'type': 'array', 'minItems': 1, 'uniqueItems': True, 'items': BINDING},
        'sampleTarget': BASE_SCHEMAS['sampleTargetUse']['properties']['target'],
        'completionProperty': {'const': 'PROTOCOL_SAMPLE_AND_SUPPORT_COLLECTION_RECORDED'},
        'custodyMeaning': {'const': 'PRESERVED_IS_COMPLETE_PARTIAL_AND_UNKNOWN_RETAIN_THEIR_NAMES'},
        'interpretationScope': {'const': 'REPORTED_COLLECTION_AND_SUPPORT_NOT_ANALYTICAL_TRUTH_OR_ADMISSION'},
    })}
SCHEMAS['sampleCollection']['required'].remove('sampleTargetRelationProofBindings')
SCHEMAS['sampleCollection']['required'].remove('sampleTarget')
SCHEMAS['sampleCollection']['allOf']=[{'if':{'required':['sampleTargetRelationProofBindings']},'then':{'required':['sampleTarget']}}]


def register(schemas):
    from referencing import Resource
    for value in SCHEMAS.values():
        schemas.schemas[value['$id']] = value
        schemas.registry = schemas.registry.with_resource(value['$id'], Resource.from_contents(value))
