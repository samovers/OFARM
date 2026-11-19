"""Explicit shared domain value contracts, authored from named source rules.

Unlike finite-reviewed-forms, this builder does not infer types or required keys
from examples. It defines only the named shared types and the qualified C16
variant, not complete row contracts or foreign evidence/admission contracts.
"""
import argparse, hashlib, json, subprocess
from pathlib import Path
from build_owned_inputs import BASE_ID, BASE_PATH, HEAD, PACKET, DEFINITION_PREFIX, obj, put

VALUE_ID = 'https://ofarm.dev/schema/drafts/non-default/assertion-domain/owned-value-types/v0.1'
MEASUREMENT_PATH = '03_machine_contracts/schemas/evidence/OFARM_MeasurementEvidence_schema_v0_1.json'
EXECUTION_PATH = '03_machine_contracts/schemas/agronomic/OFARM_ExecutionRecordPayload_schema_v0_1.json'
MEASUREMENT_ID = 'https://ofarm.dev/schema/measurementevidence/v0.1'
EVENT_PATH = '03_machine_contracts/schemas/event_ingress/OFARM_SemanticEventEnvelope_schema_v0_1.json'
EVENT_ID = 'https://ofarm.dev/schema/semanticeventenvelope/v0.1'
HERE = Path(__file__).resolve().parent

def ref(name): return {'$ref': '#/$defs/' + name}
def const(value): return {'const': value}
def enum(values): return {'enum': list(values)}
def when(field, value, consequence, otherwise=None):
    rule = {'if': {'required': [field], 'properties': {field: const(value)}}, 'then': consequence}
    if otherwise is not None: rule['else'] = otherwise
    return rule

def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--repo-root', type=Path, required=True)
    repo = parser.parse_args().repo_root.resolve(); pins = {}
    def source(path):
        raw = (repo / path).read_bytes()
        if raw != subprocess.check_output(['git', 'show', HEAD + ':' + path], cwd=repo):
            raise ValueError('Source differs from reviewed head: ' + path)
        pins[path] = {'path': path, 'commit': HEAD, 'sha256': hashlib.sha256(raw).hexdigest()}
        return json.loads(raw)
    q = source(PACKET + '/reviewed-input/domain/quantity-contract.json')
    inventory = source(PACKET + '/reviewed-input/domain/inventory.json')
    profiles = source(PACKET + '/reviewed-input/domain/operation-profile-contract.json')
    execution = source(EXECUTION_PATH); source(MEASUREMENT_PATH); source(BASE_PATH); source(EVENT_PATH)
    qualifiers = execution['properties']['actualQuantityParameters']['items']['properties']['qualifier']['enum']
    text = {'type': 'string', 'minLength': 1}
    nullable_text = {'type': ['string', 'null'], 'minLength': 1}
    binding = {'$ref': BASE_ID + '#/$defs/immutableBinding'}
    defs = {
        'binding': binding,
        'decimal': {'type': 'string', 'pattern': r'^-?(0|[1-9][0-9]*)(\.[0-9]+)?$(?![\s\S])'},
        'pointer': {'type': 'string', 'pattern': r'^(?:/(?:[^~/]|~[01])*)*$(?![\s\S])'},
        'subjectTime': {'$ref': BASE_ID + '#/$defs/subjectTime'},
        'operationTime': {'$ref': BASE_ID + '#/$defs/operationTime'},
        'target': obj({'kind': enum(sorted({k for r in inventory['rows'] for k in r['subjectKinds']})), 'binding': ref('binding')}),
        'extent': obj({'posture': enum(['FULL_TARGET_SCOPE', 'PARTIAL_TARGET_SCOPE']), 'binding': ref('binding')}),
        'scalarQuantity': obj({'quantityKind': text, 'unit': text, 'decimal': ref('decimal')}),
        'materialComponent': obj({'materialRole': enum(q['materialRoles']), 'binding': ref('binding')}),
        'normalizedQuantity': obj({'quantityKind': text, 'unit': text, 'decimal': ref('decimal'), 'conversionBinding': ref('binding')}),
        'quantityReference': obj({'quantityParameterId': text}),
        'measurementResult': {'$ref': MEASUREMENT_ID + '#/properties/result'},
        'measurementRecord': {'$ref': MEASUREMENT_ID},
        'eventEnvelope': {'$ref': EVENT_ID},
    }
    material_present = obj({
        'presence': const('PRESENT'), 'materialRole': enum(q['materialRoles']), 'binding': ref('binding'),
        'materialDefinition': ref('binding'),
        'components': {'type': 'array', 'minItems': 2, 'uniqueItems': True, 'items': ref('materialComponent')},
    }, ['presence', 'materialRole', 'binding'])
    material_present['allOf'] = [when('materialRole', 'OTHER_MATERIAL', {'required': ['materialDefinition']})]
    defs['material'] = {'oneOf': [material_present, obj({'presence': enum(['UNREPORTED', 'NOT_APPLICABLE']), 'reason': text})]}
    defs['basis'] = {'oneOf': [
        obj({'presence': const('PRESENT'), 'quantity': ref('scalarQuantity'),
             'subject': {'oneOf': [ref('target'), ref('binding')]},
             'massBasis': enum(['WET_BASIS', 'DRY_BASIS'])}, ['presence', 'quantity', 'subject']),
        obj({'presence': enum(['UNREPORTED', 'NOT_APPLICABLE']), 'reason': text}),
    ]}
    original = obj({'presence': enum(['PRESENT', 'UNREPORTED']), 'lexicalValue': nullable_text,
                    'unitText': nullable_text, 'sourceBinding': ref('binding'), 'sourcePointer': ref('pointer')})
    original['allOf'] = [when('presence', 'UNREPORTED',
        {'properties': {'lexicalValue': {'type': 'null'}, 'unitText': {'type': 'null'}}},
        {'anyOf': [{'properties': {'lexicalValue': text}}, {'properties': {'unitText': text}}]})]
    defs['originalQuantity'] = original
    defs['quantityValue'] = {'oneOf': [
        obj({'state': const('STATED'), 'quantity': ref('scalarQuantity'), 'qualifier': enum(qualifiers),
             'unitProfile': ref('binding'), 'original': ref('originalQuantity'),
             'normalized': ref('normalizedQuantity')}, ['state', 'quantity', 'qualifier', 'unitProfile', 'original']),
        obj({'state': const('UNREPORTED'), 'reason': text}),
    ]}
    defs['quantityScope'] = obj({'target': ref('target'), 'extent': ref('extent'),
        'subjectTime': ref('operationTime'), 'processPoint': ref('binding'), 'phase': text})
    parameter = obj({
        'parameterId': text, 'parameterRole': enum(q['parameterRoles']), 'activityInstance': ref('binding'),
        'valuePosture': enum(q['shape']['valuePostures']), 'material': ref('material'), 'basis': ref('basis'),
        'value': ref('quantityValue'), 'appliesTo': ref('quantityScope'),
        'otherRoleDefinition': enum(q['otherRoleDefinitions']), 'sourceParameterBinding': ref('binding'),
        'applicationMaterialInterpretation': enum(q['applicationVolumeMaterialContract']['variants']),
    }, q['shape']['required'])
    parameter['allOf'] = [
        when('parameterRole', 'OTHER_PARAMETER', {'required': ['otherRoleDefinition']}, {'not': {'required': ['otherRoleDefinition']}}),
        when('parameterRole', 'APPLICATION_VOLUME', {'required': ['applicationMaterialInterpretation']}, {'not': {'required': ['applicationMaterialInterpretation']}}),
        when('applicationMaterialInterpretation', 'MIXTURE_AS_APPLIED', {'properties': {'material': {
            'required': ['presence', 'materialRole', 'binding', 'materialDefinition', 'components'],
            'properties': {'presence': const('PRESENT'), 'materialRole': const('OTHER_MATERIAL')},
        }}}),
        when('applicationMaterialInterpretation', 'AS_IDENTIFIED_MATERIAL', {'properties': {'material': {'properties': {'presence': const('PRESENT')}}}}),
        when('applicationMaterialInterpretation', 'UNRESOLVED_SOURCE_MATERIAL', {'properties': {'material': {'properties': {'presence': const('UNREPORTED')}}}}),
        when('otherRoleDefinition', 'MOISTURE_TARGET', {'properties': {'basis': {
            'if': {'properties': {'presence': const('PRESENT')}}, 'then': {'required': ['massBasis']},
        }}}),
    ]
    defs['quantityParameter'] = parameter
    defs['analysisOutput'] = {'oneOf': [
        obj({'role': const('PROSPECTIVE_OUTPUT_SPECIFICATION'), 'specificationBinding': ref('binding')}),
        obj({'role': const('PENDING_OUTPUT'), 'specificationBinding': ref('binding'),
             'outputState': enum(profiles['O22OutputContract']['variants']['PENDING_OUTPUT']['outputStates'])}),
        obj({'role': const('ACTUAL_OUTPUT'), 'specificationBinding': ref('binding'), 'binding': ref('binding')}),
    ]}
    # O22 uses a fully authored row field contract, not the sample-keyset
    # scaffolding. Cross-record work evidence remains a separate predicate.
    o22 = next(r for r in inventory['rows'] if r['id']=='O22')
    condition_ids={'type':'array','minItems':1,'uniqueItems':True,'items':text}
    operation_target=obj({'kind':const('OPERATION'),'binding':ref('binding')})
    defs['analysisWorkSpecification']=obj({
        'binding':ref('binding'),'activityInstance':ref('binding'),'procedure':ref('binding'),
        'target':operation_target,'extent':ref('extent'),'startConditionIds':condition_ids,
        'inProgressConditionIds':condition_ids,'finishConditionIds':condition_ids,
        'outputSpecification':ref('binding'),
    })
    analysis_parameters={'method':ref('binding'),'sample':ref('binding'),'property':ref('binding'),'producedResult':ref('analysisOutput')}
    assert set(analysis_parameters)==set(o22['parameterContract']['required']+o22['parameterContract']['optional'])
    body_fields={
        'activity':const('PRODUCE_ANALYSIS_RESULT'),'interventionKind':const('OTHER_INTERVENTION'),
        'claimPosture':enum(['INTENDED','PERFORMED']),'performanceFacet':enum(['OCCURRENCE','STARTED','IN_PROGRESS','COMPLETED']),
        'activityInstance':ref('binding'),'target':operation_target,'performedBy':ref('binding'),'extent':ref('extent'),
        'parameters':obj(analysis_parameters,o22['parameterContract']['required']),
        'quantityParameters':{'type':'array','items':ref('quantityParameter')},
        'workSpecification':ref('analysisWorkSpecification'),
    }
    assert set(body_fields)==set(o22['atomContract']['requiredBodyFields']+o22['atomContract']['optionalBodyFields'])
    defs['O22']=obj({'form':const('ATOM'),'atomId':text,'definition':const(DEFINITION_PREFIX+'O22'),
        'scope':obj({'subject':operation_target,'subjectTime':ref('operationTime'),'extent':ref('extent')}),
        'body':obj(body_fields,o22['atomContract']['requiredBodyFields'])})
    defs['O22']['allOf']=[]
    for profile,facets in profiles['O22OutputContract']['byProfileAndFacet'].items():
        for facet,roles in facets.items():
            defs['O22']['allOf'].append({
                'if':{'properties':{'scope':{'properties':{'subjectTime':{'properties':{'profile':const(profile)}}}},'body':{'properties':{'performanceFacet':const(facet)}}}},
                'then':{'properties':{'body':{'properties':{
                    'claimPosture':const('INTENDED' if profile=='INTENDED_WINDOW' else 'PERFORMED'),
                    'parameters':{'properties':{'producedResult':{'properties':{'role':enum(roles)}}}},
                }}}},
            })
    # Deliberately one defined qualified variant. This is not all C16 routes or
    # an evaluation-record schema, and it makes no calculated/legal outcome.
    defs['nlQualifiedOrganicParcelBody'] = obj({
        'form': const('PROFILE_ROUTE_OUTCOME'), 'profile': const('profile:nl.go-glmc7.2026.v0_1'),
        'claimYear': const(2026), 'route': const('ORGANIC_OR_IN_CONVERSION'), 'routeScope': const('PARCEL'),
        'parcel': ref('binding'), 'historyClaim': ref('binding'), 'soilCategory': const('SAND_OR_LOESS'),
        'soilEvidence': ref('binding'), 'rustgewasEvidence': ref('binding'), 'routeEvidence': ref('binding'),
        'evaluationBasis': obj({'kind': const('PROFILE_OWNER_EVALUATION'), 'binding': ref('binding')}),
        'allegedOutcome': const('INDETERMINATE'), 'reviewState': const('PENDING'),
    })
    schema = {'$schema': 'https://json-schema.org/draft/2020-12/schema', '$id': VALUE_ID,
        'title': 'Explicit shared domain value types and qualified C16 variant v0.1',
        '$comment': 'Candidate claim-language types. No source resolution, admission, complete row semantics, calculation engine or foreign proof contract. Quantity kinds, units and named process phases require independent selected-definition checks; syntax alone does not interpret them. All nine subject-time profiles reuse the exact historical schema without changing it.',
        '$defs': defs}
    put('owned-value-types.schema.json', schema)
    pins_doc = json.loads((HERE / 'source-pins.json').read_text())
    pins_doc['sources'] = list({**{s['path']: s for s in pins_doc['sources']}, **pins}.values())
    put('source-pins.json', pins_doc)
    print(json.dumps({'explicitDefinitionsIncludingRow': len(defs), 'completeRowFieldContracts': 1,
                      'completeRowSemantics': 0,
                      'qualifiedC16Variants': 1, 'parameterRoles': len(q['parameterRoles']), 'materialRoles': len(q['materialRoles'])}))

if __name__ == '__main__': main()
