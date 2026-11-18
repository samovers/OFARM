"""Retain unresolved event selections and original operand absence in FAIL payloads."""
import copy
import json
from pathlib import Path
from strict_inputs import sha

HERE = Path(__file__).resolve().parent


def main():
    path = HERE / 'outer/payload-schema.json'; raw = path.read_bytes()
    pin = next(v for v in json.loads((HERE / 'input-pins.json').read_bytes())['members'] if v['path'] == 'outer/payload-schema.json')
    if sha(raw) != pin['rawSha256']:
        raise ValueError('Original domain payload schema differs from its input pin.')
    base = json.loads(raw); schema = copy.deepcopy(base)
    association = schema['$defs']['eventAssociation']['oneOf'][1]
    association['properties']['selectedEnvelopeBinding'] = {'$ref': '#/$defs/immutableBinding'}
    association['properties']['unresolvedSelections'] = {'type': 'array', 'minItems': 1, 'uniqueItems': True,
        'items': {'enum': ['EVENT_ENVELOPE_DIGEST', 'EVENT_MEANING_CASE_DEFINITION']}}
    association['required'] = [v for v in association['required'] if v not in ['envelope', 'caseDefinitionBinding']] + ['selectedEnvelopeBinding']
    association['allOf'] = [{
        'if': {'properties': {'disposition': {'const': 'PASS'}}},
        'then': {'required': ['envelope', 'caseDefinitionBinding'], 'not': {'required': ['unresolvedSelections']}},
    }, {
        'if': {'required': ['envelope', 'caseDefinitionBinding']},
        'then': {'not': {'required': ['unresolvedSelections']}},
        'else': {'required': ['unresolvedSelections'], 'properties': {
            'disposition': {'enum': ['FAIL', 'NOT_EVALUATED']},
            'failedPrerequisites': {'minItems': 1}, 'diagnostics': {'minItems': 1}}},
    }]
    for field, role in [('envelope', 'EVENT_ENVELOPE_DIGEST'), ('caseDefinitionBinding', 'EVENT_MEANING_CASE_DEFINITION')]:
        association['allOf'].append({
            'if': {'not': {'required': [field]}},
            'then': {'properties': {'unresolvedSelections': {'contains': {'const': role}}}},
            'else': {'properties': {'unresolvedSelections': {'not': {'contains': {'const': role}}}}},
        })
    association['$comment'] = ('Retain the submitted immutable event selector exactly. A missing envelope digest or meaning-case '
        'definition is explicit in a FAIL/NOT_EVALUATED payload, never replaced by a fabricated binding. PASS retains both resolved fields.')
    schema['$defs']['absentSourceSelection'] = {
        'type': 'object', 'additionalProperties': False,
        'required': ['inputRole', 'pointer', 'valuePosture', 'ancestorPointer', 'ancestorValueDigest', 'absenceReason'],
        'properties': {
            'inputRole': {'$ref': '#/$defs/text'}, 'pointer': {'$ref': '#/$defs/pointer', 'minLength': 1},
            'valuePosture': {'const': 'ABSENT'}, 'ancestorPointer': {'$ref': '#/$defs/pointer'},
            'ancestorValueDigest': {'$ref': '#/$defs/digest'},
            'absenceReason': {'enum': ['OBJECT_MEMBER_ABSENT', 'ARRAY_INDEX_ABSENT', 'NON_CONTAINER_ANCESTOR']},
        },
        '$comment': 'The requested path has no original value or valueDigest. Reproduce the missing traversal from its closest existing ancestor and original whole-value digest; a stored null remains a present value.',
    }
    availability = {'type': 'object', 'additionalProperties': False,
        'required': ['predicateId', 'source', 'destination'],
        'properties': {'predicateId': {'$ref': '#/$defs/text'}}, 'oneOf': []}
    for side in ['source', 'destination']:
        availability['properties'][side] = {'oneOf': [
            {'$ref': '#/$defs/sourceSelection'}, {'$ref': '#/$defs/absentSourceSelection'}]}
    for left, right in [('absentSourceSelection', 'sourceSelection'), ('sourceSelection', 'absentSourceSelection'),
                        ('absentSourceSelection', 'absentSourceSelection')]:
        availability['oneOf'].append({'properties': {'source': {'$ref': '#/$defs/' + left},
                                                    'destination': {'$ref': '#/$defs/' + right}}})
    schema['$defs']['operandAvailabilityFinding'] = availability
    predicate = schema['$defs']['atomFinding']['properties']['predicateFindings']['items']
    predicate['properties']['operandAvailabilityFindings'] = {'type': 'array', 'minItems': 1,
        'items': {'$ref': '#/$defs/operandAvailabilityFinding'}}
    predicate.setdefault('allOf', []).append({'if': {'required': ['operandAvailabilityFindings']},
        'then': {'properties': {'disposition': {'enum': ['FAIL', 'NOT_EVALUATED']}}}})
    duty=schema['$defs']['dutyFinding']
    duty['properties']['operandAvailabilityFindings']=copy.deepcopy(predicate['properties']['operandAvailabilityFindings'])
    duty.setdefault('allOf',[]).append({'if':{'required':['operandAvailabilityFindings']},
        'then':{'properties':{'disposition':{'enum':['FAIL','NOT_EVALUATED']}}}})
    schema['$comment'] = (schema.get('$comment', '') + ' Active unsealed event-association and operand-absence amendment; original input schema remains unchanged.').strip()
    for key, value in base['$defs'].items():
        if key not in ['eventAssociation', 'atomFinding', 'dutyFinding'] and schema['$defs'][key] != value:
            raise ValueError('Unrelated payload definition changed.')
    target = HERE / 'payload-schema-amendment.schema.json'
    target.write_text(json.dumps(schema, indent=2) + '\n')
    record = {'status': 'UNSEALED_DOMAIN_OWNED_PAYLOAD_AMENDMENT',
        'primaryTrustBoundary': 'AssertionRecord domain meaning and validation integrity', 'scopeStayedInsideBoundary': True,
        'base': {'path': 'outer/payload-schema.json', 'rawSha256': sha(raw)},
        'active': {'path': target.name, 'rawSha256': sha(target.read_bytes()), 'schemaId': schema['$id']},
        'changedDefinition': 'eventAssociation',
        'changedDefinitions': ['eventAssociation', 'atomFinding', 'dutyFinding'],
        'addedDefinitions': ['absentSourceSelection', 'operandAvailabilityFinding'],
        'meaning': 'Preserve every duty, exact unresolved event selector and verifiable original operand absence. Missing values have no fabricated digest or successful comparison; only the existing ancestor has a digest.',
        'next': 'Check unresolved event and absent-operand payloads through the public evaluator and retain the original schema pin.'}
    (HERE / 'payload-schema-amendment.json').write_text(json.dumps(record, indent=2) + '\n')


if __name__ == '__main__': main()
