"""Normative O09 acquisition requirements, never factual observations."""
from definition_inputs import schema, obj, BINDING, TEXT, EXTENT_TEMPORAL_MEANING

SCHEMAS={'observationAcquisition':schema('observation-acquisition-specification',
    'ofarm.assertionDomainObservationAcquisitionSpecification.v0.1',{
        'activityRow':{'const':'O09'},'workSpecificationBinding':BINDING,'procedureBinding':BINDING,
        'propertyBinding':BINDING,'methodBinding':BINDING,'methodVersionRef':TEXT,'observationContextBinding':BINDING,
        'extentTemporalMeaning':EXTENT_TEMPORAL_MEANING,
        'requiredObservations':{'type':'array','minItems':1,'uniqueItems':True,'items':obj({
            'slotId':TEXT,'measurementBinding':BINDING,
            'permittedResultKinds':{'type':'array','minItems':1,'uniqueItems':True,'items':{'enum':['NUMERIC','CODED','QUALITATIVE','CENSORED_NUMERIC']}},
            'quantityContext':{'oneOf':[{'type':'null'},obj({'quantityKind':TEXT,'unit':TEXT})]}})},
        'productionTimeRule':{'const':'ALL_REQUIRED_RESULTS_RECORDED_WITHIN_CLAIMED_WORK_TIME'},
        'interpretationScope':{'const':'REQUIRED_OBSERVATION_RECORDS_NOT_INTERVENTION_OR_MEASURED_TRUTH'},
    })}
SCHEMAS['observationAcquisition']['required'].remove('extentTemporalMeaning')


def register(schemas):
    from referencing import Resource
    for value in SCHEMAS.values():
        schemas.schemas[value['$id']]=value
        schemas.registry=schemas.registry.with_resource(value['$id'],Resource.from_contents(value))
