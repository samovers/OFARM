"""Owned normative definitions for deterministic measurement interpretation.

These are domain definition inputs, not measurement, certificate, authority or
admission records. Independently selected original bytes fix their meaning.
They cannot redefine a foreign record schema or make a source true.
"""
from activity_condition_meanings import PREDICATE_KINDS
from completion_count_meanings import MEANINGS as COMPLETION_COUNTS

PREFIX = 'https://ofarm.dev/schema/drafts/non-default/assertion-domain/'
PROPOSITION = PREFIX + 'proposition/v0.1'
PAYLOAD = 'https://ofarm.dev/schema/drafts/non-default/assertion-record-domain-validation/payload/v0.1'


def obj(properties, required=None):
    return {'type': 'object', 'additionalProperties': False, 'properties': properties,
            'required': list(properties) if required is None else required}


TEXT = {'type': 'string', 'minLength': 1}
BINDING = {'$ref': PAYLOAD + '#/$defs/immutableBinding'}
DECIMAL = {'$ref': 'https://ofarm.dev/schema/drafts/non-default/assertion-domain/owned-value-types/v0.1#/$defs/decimal'}
POINTER = {'type': 'string', 'pattern': '^(?:/(?:[^~/]|~0|~1)*)*$'}
EXTENT_TEMPORAL_MEANING = obj({'extentBinding':BINDING,'sourceTimeType':{'enum':['INTERVAL','OPEN_INTERVAL']},
            'timeBasis':TEXT,'startBoundary':{'enum':['INCLUSIVE','EXCLUSIVE']},
            'endBoundary':{'enum':['INCLUSIVE','EXCLUSIVE','UNBOUNDED']}})
QUANTITY = obj({'quantityKind': TEXT, 'unit': TEXT, 'decimal': DECIMAL,
                'qualifier': {'$ref': PROPOSITION + '#/$defs/complianceQuantity/properties/qualifier'},
                'originalLexicalValue': TEXT, 'unitProfile': BINDING,
                'originalUnitText': {'type': ['string', 'null']}},
               ['quantityKind', 'unit', 'decimal', 'qualifier', 'originalLexicalValue', 'unitProfile'])
ENDPOINT = {'oneOf': [obj({'decimal': DECIMAL, 'inclusive': {'type': 'boolean'}}), obj({'kind': {'const': 'UNBOUNDED'}})]}
INTERVAL = obj({'lower': ENDPOINT, 'upper': ENDPOINT})
LIMIT_ENDPOINT = {'oneOf': [obj({'origin': {'enum': ['ZERO', 'DETECTION_LIMIT']}, 'inclusive': {'type': 'boolean'}}),
                              obj({'origin': {'const': 'UNBOUNDED'}})]}


def schema(name, version, fields):
    return {'$schema': 'https://json-schema.org/draft/2020-12/schema', '$id': PREFIX + name + '/v0.1',
            **obj({'schemaVersion': {'const': version}, 'definitionId': TEXT, **fields}),
            '$comment': 'New domain-owned normative input. Exact independent selection and protected original bytes are required. No source admission, authority, runtime producer or statutory applicability is asserted.'}


SCHEMAS = {
    'identifierAttribute': schema('identifier-attribute-definition', 'ofarm.assertionDomainIdentifierAttributeDefinition.v0.1', {
        'attributeDefinition': TEXT,
        'identifierRole': {'$ref': PROPOSITION + '#/$defs/S10/properties/body/properties/identifierRole'},
        'schemeBinding': BINDING, 'schemeVersion': TEXT, 'issuerBinding': BINDING,
        'sourceBindingRole': {'$ref': 'https://ofarm.dev/schema/agronomicidentitybinding/v0.1#/properties/bindingRole'},
        'sourceSubjectType': {'$ref': 'https://ofarm.dev/schema/agronomicidentitybinding/v0.1#/$defs/localSubject/properties/subjectType'},
        'subjectIdentityInterpretation': {'const': 'EXACT_SELECTED_IDENTITY_RECORD'},
        'valueField': {'enum': ['code', 'normalizedLabel', 'uri', 'registrationRef', 'authorisationRef', 'gtin', 'batchLot', 'digitalLinkUri', 'lotNumber', 'seedCertificateRef']},
        'interpretationScope': {'const': 'REPORTED_NAMED_IDENTIFIER_NOT_GOVERNANCE_OR_AUTHORIZATION'},
    }),
    'evidencePolicyMeaning': schema('evidence-policy-meaning-definition', 'ofarm.assertionDomainEvidencePolicyMeaningDefinition.v0.1', {
        'policyBinding': BINDING, 'requiredUse': TEXT, 'sufficiencyCaseBinding': BINDING,
        'caseClass': {'enum': ['COMPLIANCE_ASSERTION', 'DOCUMENT_ATTESTATION', 'SUBMISSION_ASSEMBLY']},
        'targetTwin': {'enum': ['COMPLIANCE', 'ADVISORY']},
        'evidenceProjection': {'enum': ['RAW_SOURCES', 'NORMALIZED_INTERPRETATIONS', 'ALL_SUPPORT_SOURCES']},
        'reasonKindMappings': {'type': 'array', 'items': obj({'reasonCode': {'enum': [
            'MISSING_NORMALIZED_INTERPRETATION', 'MISSING_PROVENANCE_LINK', 'CHAIN_OF_CUSTODY_PARTIAL',
            'CHAIN_OF_CUSTODY_UNKNOWN', 'BASIS_NOT_RETAINED', 'CONFLICTING_EVIDENCE', 'ATTESTATION_AUTHORITY_MISSING',
            'AMBIGUOUS_PRODUCT_ID', 'TIMESTAMP_INCOMPLETE', 'SOURCE_QUALITY_LOW', 'MACHINE_RECORD_PARTIAL',
            'HUMAN_MACHINE_CONFLICT', 'LATE_EVIDENCE_POST_OUTPUT', 'LATE_EVIDENCE_POST_SUBMISSION']}, 'kind': TEXT})},
        'interpretationScope': {'const': 'CONDITIONAL_REPORTED_SUFFICIENCY_ONLY'},
    }),
    'ruleMeaning': schema('compliance-rule-meaning-definition', 'ofarm.assertionDomainComplianceRuleMeaningDefinition.v0.1', {
        'ruleBinding': BINDING,
        'relevanceRoles': {'type': 'array', 'items': {
            **obj({'role': TEXT, 'basisKind': {'enum': ['MEASUREMENT_ABOUT_SUBJECT', 'EVENT_ABOUT_SUBJECT']},
                   'eventConcept': {'const': 'HAIL_DAMAGE_OCCURRENCE'}}, ['role', 'basisKind']),
            'allOf': [{'if': {'required': ['eventConcept']},
                       'then': {'properties': {'basisKind': {'const': 'EVENT_ABOUT_SUBJECT'}}}}]}},
        'applicabilityClauses': {'type': 'array', '$comment': 'Closed valid-time bounds, null upper bound unbounded; the entire claimed period must be covered. No match means INDETERMINATE, and multiple matching clauses are ambiguous.', 'items': obj({'clauseId': TEXT,
            'jurisdiction': {'$ref': PROPOSITION + '#/$defs/C02/properties/body/properties/jurisdiction'}, 'cropBinding': BINDING, 'useBinding': BINDING,
            'subjectKinds': {'type': 'array', 'minItems': 1, 'uniqueItems': True, 'items':
                {'$ref': PROPOSITION + '#/$defs/C02/properties/scope/properties/subject/allOf/1/properties/subjectType'}},
            'validFrom': {'type': 'string', 'format': 'date-time'},
            'validUntil': {'type': ['string', 'null'], 'format': 'date-time'},
            'effect': {'enum': ['APPLIES', 'DOES_NOT_APPLY']}})},
        'interpretationScope': {'const': 'CONDITIONAL_DOMAIN_MEANING_ONLY'},
    }),
    'jurisdiction': schema('profile-jurisdiction-definition', 'ofarm.assertionDomainProfileJurisdictionDefinition.v0.1', {
        'profileBinding': BINDING, 'jurisdictionCode': TEXT,
        'jurisdictionBinding': BINDING,
        'meaning': TEXT,
    }),
    'term': schema('interpretation-term-definition', 'ofarm.assertionDomainInterpretationTermDefinition.v0.1', {
        'category': {'enum': ['OBSERVED_PROPERTY', 'MEASUREMENT_METHOD', 'SAMPLING_PROTOCOL', 'UNIT_PROFILE', 'CODED_RESULT', 'QUALITATIVE_SCALE']},
        'meaning': TEXT,
        'quantityContext': {'oneOf': [{'type': 'null'}, obj({'quantityKind': TEXT, 'unit': TEXT})]},
        'procedureVersionRef': {'type': 'string', 'pattern': '^[A-Za-z0-9._:-]+$',
            '$comment': 'The original procedure version interpreted by this definition. It is distinct from this definition\'s immutable revision or content selector.'},
        'observationMeaning': obj({'concept': {'const': 'STAND_COUNT_OBSERVATION'},
            'quantityKind': {'const': 'candidate:quantitykind:emerged-plant-count'},
            'unit': {'const': 'candidate:unit:plant-count'},
            'resultDomain': {'const': 'NONNEGATIVE_INTEGER_COUNT'}}),
        'massFractionUnitMeaning': obj({'scale': {'enum': [1, 100]}, 'ratio': {'const': 'MASS_OVER_MASS'}}),
        'completionCountMeaning': {'enum': list(COMPLETION_COUNTS.values())},
        'splitCountPopulation': obj({
            'sourceLotBinding': BINDING,
            'sourceExtent': {'$ref': PROPOSITION + '#/$defs/O11/properties/body/properties/extent'},
            'successorLotBindings': {'type':'array','minItems':2,'uniqueItems':True,'items':BINDING},
            'lineageRelation': {'const':'splitFrom'},
            'sourceLinkMeaning': {'const':'EXACT_SOURCE_LOT_IS_WORK_TARGET_AND_SOLE_PREDECESSOR'},
            'successorMembership': {'const':'UNORDERED_EXACT_BINDING_SET_OF_DISTINCT_LOGICAL_LOTS'},
            'unitSelection': {'const':'EVERY_SOURCE_MATERIAL_UNIT_OF_SELECTED_EXTENT_UNDER_BOUND_SPLIT_PROCEDURE'},
            'unfinishedMeaning': {'const':'ANY_REQUIRED_SEPARATION_OR_OUTPUT_ASSIGNMENT_UNSATISFIED_OR_UNRESOLVED'},
            'missingObservationMeaning': {'const':'INCLUDE_UNIT_AS_UNFINISHED_OR_KEEP_RESULT_INDETERMINATE'},
            'successorMeaning': {'const':'NAMED_OUTPUT_PROPOSALS_NOT_ACCEPTED_IDENTITY_OR_LINEAGE'}}),
        'harvestCountPopulation': obj({'cropCycleBinding': BINDING,
            'outputLotBindings': {'type':'array','uniqueItems':True,'items':BINDING},
            'harvestedMaterialBinding': BINDING,
            'unitSelection': {'const':'ALL_CROP_MATERIAL_UNITS_SELECTED_BY_BOUND_HARVEST_PROCEDURE'},
            'unfinishedMeaning': {'const':'HANDLING_NOT_COMPLETE_UNDER_EVERY_REQUIRED_HARVEST_PROCEDURE_FINISH_CRITERION'},
            'outputLotMeaning': {'const':'NAMED_OUTPUT_LINKS_ONLY_NOT_ACCEPTED_LOT_CREATION'}}),
        'mixingCountPopulation': obj({
            'predecessorLotBindings': {'type':'array','minItems':1,'uniqueItems':True,'items':BINDING},
            'successorLotBindings': {'type':'array','minItems':1,'uniqueItems':True,'items':BINDING},
            'claimBasisAfterBinding': BINDING,'mixingPosture': {'const':'PHYSICAL_MIX'},
            'unitSelection': {'const':'EVERY_UNIT_OF_EVERY_INPUT_EXTENT_SELECTED_BY_BOUND_MIXING_PROCEDURE'},
            'unfinishedMeaning': {'const':'ANY_REQUIRED_MIXING_PROCEDURE_STEP_NOT_COMPLETED_FOR_SELECTED_INPUT_UNIT'},
            'successorMeaning': {'const':'NAMED_OUTPUT_PROPOSALS_NOT_ACCEPTED_SUCCESSOR_CREATION'},
            'basisMeaning': {'const':'ALLEGED_POST_MIX_BASIS_NOT_GOVERNING_CLASSIFICATION_OR_MASS_BALANCE'}}),
        'durationUnitMeaning': obj({'secondsPerUnit': DECIMAL, 'meaning': {'const': 'EXACT_ELAPSED_SECONDS_PER_UNIT'}}),
        'sanitationPropertyMeaning': obj({'specificationBinding': BINDING,
            'role': {'enum': ['MINIMUM_CONTINUOUS_MATERIAL_CONTACT_ACROSS_SELECTED_EXTENT', 'SELECTED_SANITATION_PROCEDURE_ACTIVITY_AT_FINISH']},
            'materialBinding': BINDING,
            'workTime': {'$ref': PROPOSITION + '#/$defs/O17/properties/scope/properties/subjectTime'}}),
        'irrigationPropertyMeaning': obj({'specificationBinding': BINDING,
            'role': {'enum': ['CUMULATIVE_WATER_DELIVERED_OVER_SELECTED_WORK', 'WATER_INFLOW_TO_SELECTED_EXTENT_AT_FINISH']},
            'waterSourceBinding': BINDING,
            'workTime': {'$ref': PROPOSITION + '#/$defs/O04/properties/scope/properties/subjectTime'}}),
        'moisturePropertyMeaning': obj({'massBasis': {'enum': ['WET_BASIS', 'DRY_BASIS']},
            'numerator': {'const': 'WATER_MASS'}, 'denominator': {'enum': ['TOTAL_WET_MASS', 'DRY_SOLIDS_MASS']}}),
        'workConditionMeaning': obj({'conditionDefinitionBinding': BINDING,
                                    'workSpecificationBinding': BINDING, 'procedureBinding': BINDING,
                                    'activityRow': {'enum': ['O' + str(n).zfill(2) for n in range(1, 28)]},
                                    'stage': {'enum': ['START', 'IN_PROGRESS', 'FINISH']},
                                    'predicateKind': {'enum': PREDICATE_KINDS},
                                    'conditionId': TEXT}),
    }),
    'criterion': schema('criterion-definition', 'ofarm.assertionDomainCriterionDefinition.v0.1', {
        'domainRow': {'const': 'C04'}, 'methodUseBinding': BINDING,
        'operator': {'enum': ['LT', 'LE', 'GE', 'GT', 'BETWEEN']},
        'threshold': {'oneOf': [QUANTITY, obj({'lower': QUANTITY, 'upper': QUANTITY,
                                              'lowerInclusive': {'type': 'boolean'}, 'upperInclusive': {'type': 'boolean'}})]},
        'permittedResultKinds': {'type': 'array', 'minItems': 1, 'uniqueItems': True,
                                  'items': {'enum': ['NUMERIC', 'CENSORED_NUMERIC', 'CODED', 'QUALITATIVE', 'ABSENT_PENDING']}},
    }),
    'method': schema('measurement-use-definition', 'ofarm.assertionDomainMeasurementUseDefinition.v0.1', {
        'scope': {'$ref': PROPOSITION + '#/$defs/C04/properties/scope'},
        'extentTemporalMeaning': EXTENT_TEMPORAL_MEANING,
        'propertyBinding': BINDING,
        'methodBinding': BINDING,
        'protocolBinding': {'oneOf': [BINDING, {'type': 'null'}]},
        'contextBinding': BINDING,
        'subjectRelationBinding': BINDING,
        'quantityContext': obj({'quantityKind': TEXT, 'unit': TEXT, 'unitProfile': BINDING}),
        'phenomenonTime': obj({'timeType': {'enum': ['INSTANT', 'INTERVAL', 'OPEN_INTERVAL', 'AS_OF']},
                               'sourceProjection': {'$ref': 'https://ofarm.dev/schema/measurementevidence/v0.1#/properties/phenomenonTime'}}),
        'qualificationPointers': {'type': 'array', 'minItems': 1, 'uniqueItems': True, 'items': POINTER},
        'qualificationInterpretation': {'enum': ['SOURCE_QUALITY_ONLY', 'STATISTICAL_NOT_HARD_BOUND', 'METHOD_DEFINED_HARD_BOUND', 'EXPLICIT_ESTIMATE', 'NOT_APPLICABLE_BY_BOUND_METHOD']},
        'numericSet': {'oneOf': [obj({'kind': {'const': 'EXACT_POINT'}}),
                                 obj({'kind': {'const': 'SOURCE_HARD_INTERVAL'}, 'lowerPointer': POINTER,
                                      'upperPointer': POINTER, 'lowerInclusive': {'type': 'boolean'}, 'upperInclusive': {'type': 'boolean'}})]},
        'censoringRules': {'type': 'array', 'items': obj({
            'qualifier': TEXT, 'limitType': TEXT, 'lower': LIMIT_ENDPOINT, 'upper': LIMIT_ENDPOINT,
            'nonnegative': {'type': 'boolean'}, 'basis': TEXT})},
        'mappingBinding': {'oneOf': [BINDING, {'type': 'null'}]},
        'scalarSource': {'oneOf': [{'type': 'null'}, obj({'binding': BINDING,
            'parameterIndex': {'type': 'integer', 'minimum': 0},
            'parameterRole': {'enum': ['CONCENTRATION', 'OTHER_PARAMETER']},
            'use': {'enum': ['NUMERIC_READING', 'DETECTION_LIMIT']}})]},
        'sourceResultQualification': obj({'requireOriginalLexicalValue': {'type': 'boolean'},
                                          'permittedEvidenceStatuses': {'type': 'array', 'minItems': 1, 'uniqueItems': True, 'items': TEXT},
                                          'requiredDegradationReasons': {'type': 'array', 'uniqueItems': True, 'items': TEXT}}),
    }),
    'mapping': schema('result-mapping-definition', 'ofarm.assertionDomainResultMappingDefinition.v0.1', {
        'quantityContext': obj({'quantityKind': TEXT, 'unit': TEXT, 'unitProfile': BINDING}),
        'entries': {'type': 'array', 'minItems': 1, 'items': obj({'resultKind': {'enum': ['CODED', 'QUALITATIVE']},
            'sourceValue': TEXT, 'admissibleValues': INTERVAL, 'basis': TEXT})},
    }),
}
# Ordinary property terms need no work-condition meaning. A property used to
# establish a work condition must supply the exact semantic link, checked by
# condition_sources against the independently selected work definition.
SCHEMAS['method']['required'].remove('extentTemporalMeaning')
SCHEMAS['method']['allOf']=[{'if':{'required':['extentTemporalMeaning']},'then':{'properties':{'scope':{'properties':{'extent':{'properties':{'posture':{'const':'PARTIAL_TARGET_SCOPE'}}}}}}}}]
SCHEMAS['sampleTargetUse']=schema('sample-target-relation-use-definition','ofarm.assertionDomainSampleTargetRelationUseDefinition.v0.1',{
    'relationConcept':{'const':'SAMPLE_SOURCE_SUPPORT_TARGET'},'sampleKind':{'const':'SAMPLE'},'sampleBinding':BINDING,
    'target':obj({'kind':{'enum':['FIELD','ZONE','CROP_CYCLE','LOT','PARTIAL_EXTENT']},'binding':BINDING}),
    'measurementBinding':BINDING,'contextBinding':BINDING,
    'partialExtentBinding':{'oneOf':[BINDING,{'type':'null'}]},
    'samplingProtocolBinding':BINDING,'samplingProtocolVersionRef':TEXT,
    'subjectTime':{'$ref':'https://ofarm.dev/schema/drafts/non-default/assertion-domain/owned-value-types/v0.1#/$defs/subjectTime'},
    'phenomenonTimeBasis':{'enum':['OBSERVED_TIME','SAMPLE_TIME','ESTIMATED_TIME']},
    'measurementIntervalMeaning':obj({'sourceTimeType':{'const':'INTERVAL'},'timeBasis':TEXT,
        'startBoundary':{'enum':['INCLUSIVE','EXCLUSIVE']},'endBoundary':{'enum':['INCLUSIVE','EXCLUSIVE']}}),
    'extentTemporalMeaning':EXTENT_TEMPORAL_MEANING,
})
for key in ['measurementIntervalMeaning','extentTemporalMeaning']:SCHEMAS['sampleTargetUse']['required'].remove(key)
SCHEMAS['sampleTargetUse']['allOf']=[{'if':{'required':['extentTemporalMeaning']},
    'then':{'properties':{'partialExtentBinding':BINDING}}}]
SCHEMAS['identifierAttribute']['required'].remove('subjectIdentityInterpretation')
SCHEMAS['identifierAttribute']['allOf'] = [
    {'if': {'required': ['subjectIdentityInterpretation']},
     'then': {'properties': {'sourceSubjectType': {'const': 'OTHER'}}}},
]
SCHEMAS['term']['required'].remove('workConditionMeaning')
SCHEMAS['term']['required'].remove('procedureVersionRef')
SCHEMAS['term']['required'].remove('observationMeaning')
SCHEMAS['term']['required'].remove('massFractionUnitMeaning')
SCHEMAS['term']['required'].remove('moisturePropertyMeaning')
SCHEMAS['term']['required'].remove('completionCountMeaning')
SCHEMAS['term']['required'].remove('splitCountPopulation')
SCHEMAS['term']['required'].remove('harvestCountPopulation')
SCHEMAS['term']['required'].remove('mixingCountPopulation')
SCHEMAS['term']['required'].remove('irrigationPropertyMeaning')
SCHEMAS['term']['required'].remove('sanitationPropertyMeaning')
SCHEMAS['term']['required'].remove('durationUnitMeaning')
SCHEMAS['criterion']['allOf'] = [
    {'if': {'properties': {'operator': {'const': 'BETWEEN'}}},
     'then': {'properties': {'threshold': {'required': ['lower', 'upper']}}},
     'else': {'properties': {'threshold': {'required': ['decimal']}}}},
]
SCHEMAS['term']['allOf'] = [
    {'if': {'required': ['splitCountPopulation']}, 'then': {'properties': {'category': {'const': 'OBSERVED_PROPERTY'},
        'workConditionMeaning': {'properties': {'activityRow': {'const':'O11'},'stage': {'const':'FINISH'}}}},'required':['workConditionMeaning']}},
    {'if': {'required': ['mixingCountPopulation']}, 'then': {'properties': {'category': {'const': 'OBSERVED_PROPERTY'},
        'workConditionMeaning': {'properties': {'activityRow': {'const':'O13'},'stage': {'const':'FINISH'}}}},'required':['workConditionMeaning']}},
    {'if': {'required': ['harvestCountPopulation']}, 'then': {'properties': {'category': {'const': 'OBSERVED_PROPERTY'},
        'workConditionMeaning': {'properties': {'activityRow': {'const':'O06'},'stage': {'const':'FINISH'}}}},'required':['workConditionMeaning']}},
    {'if': {'required': ['sanitationPropertyMeaning']}, 'then': {'properties': {'category': {'const': 'OBSERVED_PROPERTY'}}}},
    {'if': {'required': ['durationUnitMeaning']}, 'then': {'properties': {'category': {'const': 'UNIT_PROFILE'},
        'quantityContext': {'type': 'object', 'properties': {'quantityKind': {'const': 'qudt:Time'}}}}}},
    {'if': {'required': ['irrigationPropertyMeaning']}, 'then': {'properties': {'category': {'const': 'OBSERVED_PROPERTY'}}}},
    {'if': {'required': ['completionCountMeaning']}, 'then': {'properties': {'category': {'const': 'OBSERVED_PROPERTY'}}}},
    {'if': {'required': ['massFractionUnitMeaning']}, 'then': {'properties': {'category': {'const': 'UNIT_PROFILE'}}}},
    {'if': {'required': ['moisturePropertyMeaning']}, 'then': {'properties': {'category': {'const': 'OBSERVED_PROPERTY'}}}},
    {'if': {'required': ['observationMeaning']},
     'then': {'properties': {'category': {'const': 'OBSERVED_PROPERTY'}}}},
    {'if': {'required': ['procedureVersionRef']},
     'then': {'properties': {'category': {'enum': ['MEASUREMENT_METHOD', 'SAMPLING_PROTOCOL']}}}},
    {'if': {'properties': {'category': {'const': 'UNIT_PROFILE'}}},
     'then': {'properties': {'quantityContext': {'type': 'object'}}},
     'else': {'properties': {'quantityContext': {'type': 'null'}}}},
]


def register(schemas):
    from referencing import Resource
    import json
    from pathlib import Path
    payload = json.loads((Path(__file__).resolve().parent / 'payload-schema-amendment.schema.json').read_bytes())
    schemas.schemas[payload['$id']] = payload
    schemas.registry = schemas.registry.with_resource(payload['$id'], Resource.from_contents(payload))
    for value in SCHEMAS.values():
        schemas.schemas[value['$id']] = value
        schemas.registry = schemas.registry.with_resource(value['$id'], Resource.from_contents(value))
