"""S10 reported identifier meaning from exact selected normative originals.

Values do not choose their own field: the selected attribute definition fixes
the source binding role and scalar field first. No identity, regulatory status,
scheme adoption or eligible use is established by this interpretation.
"""
from definition_inputs import SCHEMAS, register
from strict_inputs import same, digest, distinct_selected_originals

SUBJECT_TYPES = {'INPUT': {'PRODUCT_OR_INPUT'}, 'LOT': {'SEED_LOT', 'MATERIAL'}}
PRODUCT_IDENTIFIER_ROLES = {'OTHER', 'CROP_PROTECTION_PRODUCT', 'FERTILIZER_PRODUCT',
    'NUTRIENT_INPUT', 'PRODUCT_BATCH_OR_LOT', 'SEED_LOT'}


from domain_reader_occurrences import reader, selection as observe_selection, guard as observe_guard, origin as read_origin, observed_shape, predicate_value, guard_refs, branch as observed_branch, observe_comparisons


@reader('identifier_sources.py', ['AR_BODY'])
def evaluate(atom, request, sources, schemas, identity_schemas=None, intent=None):
    register(schemas)
    body = atom['body']; errors, missing, ids, refs, comparisons = [], [], [], [], []
    retained = None; subject_identity = None
    def result():
        return {'scope': 'SELECTED_IDENTIFIER_ATTRIBUTE_ROLE_AND_ORIGINAL_FIELD',
            'disposition': 'FAIL' if errors else 'NOT_EVALUATED' if missing else 'PASS',
            'errors': errors, 'remainingRoles': missing, 'sourceInputIds': sorted(set(ids)),
            'requiredReferences': refs, 'comparisons': comparisons, 'retainedSourceQualifications': retained}
    def claim(path): return {'inputRole': 'ATOM:' + atom['atomId'], 'pointer': path}
    def original(entry, path): return {'inputRole': entry['id'], 'pointer': path}
    def compare(code, left, right, src, dst, equal=None):
        okay = same(left, right) if equal is None else equal
        comparisons.append({'predicateId': code, 'source': {**src, 'valueDigest': digest(left)},
            'destination': {**dst, 'valueDigest': digest(right)}, 'disposition': 'PASS' if okay else 'FAIL'})
        observe_comparisons([comparisons[-1]])
        if not okay: errors.append({'code': code, 'pointer': src['pointer']})
    def absent_operand(predicate, entry, path, destination, value):
        from original_operand import select_operand
        comparisons.append({'predicateId': predicate, 'operandAvailability': {
            'source': select_operand(entry['record'], path, entry['id']),
            'destination': {**destination, 'valueDigest': digest(value)}}})
        observe_comparisons([comparisons[-1]])
    def role_constraint(code, invalid, path, applicable_site):
        # Keep the ordinary error unchanged; trace only the fields this
        # constraint actually consumed, including its role guard.
        operands = observe_guard(code + ':OPERANDS', not invalid,
            depends_on=guard_refs(applicable_site), predicate_sites=(code,))
        observe_comparisons([{'predicateId': code,
            'source': original(definition_entry, path),
            'disposition': 'FAIL' if invalid else 'PASS'}],
            depends_on=[operands] if operands is not None else [])
        if invalid: errors.append({'code': code, 'pointer': path})
    shape = SCHEMAS['identifierAttribute']
    candidates = distinct_selected_originals([v for v in sources if 'selectorMapping' in v
        and predicate_value(v, '', isinstance(v['record'], dict), 'IDENTIFIER_ATTRIBUTE_DEFINITION') and predicate_value(v, '/schemaVersion', v['record'].get('schemaVersion'), 'IDENTIFIER_ATTRIBUTE_DEFINITION') == shape['properties']['schemaVersion']['const']
        and same(predicate_value(v, '/schemeBinding', v['record'].get('schemeBinding'), 'IDENTIFIER_ATTRIBUTE_DEFINITION'), body['scheme'])
        and predicate_value(v, '/attributeDefinition', v['record'].get('attributeDefinition'), 'IDENTIFIER_ATTRIBUTE_DEFINITION') == body['attributeDefinition']])
    definition_selection = observe_selection('IDENTIFIER_ATTRIBUTE_DEFINITION', sources, candidates,
        origins=[read_origin('ATOM:' + atom['atomId'], '/body/scheme'), read_origin('ATOM:' + atom['atomId'], '/body/attributeDefinition')])
    if len(candidates) != 1:
        missing.append({'role': 'INDEPENDENT_NAMED_IDENTIFIER_ATTRIBUTE_DEFINITION', 'pointer': '/body/attributeDefinition'})
        if len(candidates) > 1:
            observe_comparisons([{'predicateId': 'AMBIGUOUS_IDENTIFIER_ATTRIBUTE_DEFINITION',
                'source': claim('/body/attributeDefinition'), 'disposition': 'FAIL'}],
                depends_on=[definition_selection] if definition_selection is not None else [])
            errors.append({'code': 'AMBIGUOUS_IDENTIFIER_ATTRIBUTE_DEFINITION', 'pointer': '/body/attributeDefinition'})
        return result()
    definition_entry = candidates[0]; definition = definition_entry['record']; ids.append(definition_entry['id'])
    refs.append({'role': 'NAMED_IDENTIFIER_ATTRIBUTE_DEFINITION', 'binding': definition_entry['binding'], 'pointer': '/body/attributeDefinition'})
    invalid = observed_shape(schemas, shape['$id'], definition); errors.extend(invalid)
    if invalid: return result()
    identity_matches = definition['definitionId'] == definition_entry['binding']['ref']
    # The expected ref is selected-read metadata, not a field in this original.
    observe_comparisons([{'predicateId': 'IDENTIFIER_DEFINITION_IDENTITY_MISMATCH',
        'source': original(definition_entry, '/definitionId'),
        'disposition': 'PASS' if identity_matches else 'FAIL'}])
    if not identity_matches:
        errors.append({'code': 'IDENTIFIER_DEFINITION_IDENTITY_MISMATCH', 'pointer': '/definitionId'})
    for key, expected, path in [('attributeDefinition', body['attributeDefinition'], '/body/attributeDefinition'),
        ('identifierRole', body['identifierRole'], '/body/identifierRole'), ('schemeBinding', body['scheme'], '/body/scheme')]:
        compare('IDENTIFIER_DEFINITION_' + key.upper() + '_MISMATCH', definition[key], expected,
            original(definition_entry, '/' + key), claim(path))
    if request is None or 'code' not in request['input']:
        missing.append({'role': 'EXACT_SELECTED_IDENTIFIER_CODE_SOURCE', 'pointer': '/body/value'}); return result()
    binding = request['input']['code']['binding']
    found = [v for v in sources if same(v['binding'], binding)]
    observe_selection('IDENTIFIER_CODE_SOURCE', sources, found, binding=binding,
        origins=[read_origin('ATOM:' + atom['atomId'], '/body/scheme'), read_origin('ATOM:' + atom['atomId'], '/body/originalLexicalValue')])
    if len(found) != 1:
        missing.append({'role': 'EXACT_SELECTED_IDENTIFIER_CODE_SOURCE', 'pointer': '/body/value'}); return result()
    entry = found[0]; code = entry['record']; ids.append(entry['id'])
    invalid = observed_shape(schemas, 'https://ofarm.dev/schema/agronomicidentitybinding/v0.1', code); errors.extend(invalid)
    if invalid: return result()
    refs.append({'role': 'REPORTED_IDENTIFIER_CODE_BINDING', 'binding': binding, 'pointer': '/body/value'})
    for actual, expected, path, dest in [
        (code['bindingRole'], definition['sourceBindingRole'], '/bindingRole', '/sourceBindingRole'),
        (code['localSubject']['subjectType'], definition['sourceSubjectType'], '/localSubject/subjectType', '/sourceSubjectType'),
        (code['externalScheme']['schemeRef'], definition['schemeBinding']['ref'], '/externalScheme/schemeRef', '/schemeBinding/ref'),
        (code['externalScheme']['issuerRef'], definition['issuerBinding']['ref'], '/externalScheme/issuerRef', '/issuerBinding/ref')]:
        compare('IDENTIFIER_SOURCE_' + path.rsplit('/', 1)[-1].upper() + '_MISMATCH', actual, expected,
            original(entry, path), original(definition_entry, dest))
    if 'schemeVersion' not in code['externalScheme']:
        missing.append({'role': 'IDENTIFIER_SOURCE_SCHEME_VERSION', 'pointer': '/externalScheme/schemeVersion'})
        absent_operand('IDENTIFIER_SOURCE_SCHEME_VERSION_AVAILABLE', entry, '/externalScheme/schemeVersion',
            original(definition_entry, '/schemeVersion'), definition['schemeVersion'])
    else:
        compare('IDENTIFIER_SOURCE_SCHEME_VERSION_MISMATCH', code['externalScheme']['schemeVersion'], definition['schemeVersion'],
            original(entry, '/externalScheme/schemeVersion'), original(definition_entry, '/schemeVersion'))
    subject = atom['scope']['subject']; kind = subject['subjectType']
    compare('IDENTIFIER_LOCAL_SUBJECT_MISMATCH', code['localSubject']['subjectRef'], subject['subjectRef'],
        original(entry, '/localSubject/subjectRef'), claim('/scope/subject/subjectRef'))
    if observed_branch('IDENTIFIER_IDENTITY_INTERPRETATION', definition.get('subjectIdentityInterpretation') == 'EXACT_SELECTED_IDENTITY_RECORD', origins=[original(definition_entry, '/subjectIdentityInterpretation')]):
        from identity_sources import IDENTITY_SCHEMA, KINDS
        subject_binding = {'ref': subject['subjectRef'], **{k:subject[k] for k in ['revisionRef','digest'] if k in subject}}
        identity_matches = [v for v in sources if same(v['binding'], subject_binding)]
        observe_selection('IDENTIFIER_SUBJECT_IDENTITY', sources, identity_matches, binding=subject_binding,
            origins=[read_origin('ATOM:' + atom['atomId'], '/scope/subject'), read_origin(definition_entry['id'], '/subjectIdentityInterpretation')], guards=guard_refs('IDENTIFIER_IDENTITY_INTERPRETATION'))
        if subject['subjectPosture'] != 'EXISTING_SUBJECT':
            missing.append({'role':'IDENTIFIER_PROSPECTIVE_SUBJECT_SOURCE_USE','pointer':'/scope/subject'})
        elif kind not in KINDS:
            missing.append({'role':'IDENTIFIER_EXACT_SUBJECT_KIND_MEANING:'+kind,'pointer':'/scope/subject/subjectType'})
        elif len(identity_matches)!=1 or identity_schemas is None or IDENTITY_SCHEMA not in identity_schemas.schemas:
            missing.append({'role':'IDENTIFIER_EXACT_SUBJECT_IDENTITY_ORIGINAL','pointer':'/scope/subject'})
        else:
            identity_entry=identity_matches[0]; identity=identity_entry['record'];ids.append(identity_entry['id'])
            refs.append({'role':'IDENTIFIER_SUBJECT_IDENTITY','binding':subject_binding,'pointer':'/scope/subject'})
            shape=observed_shape(identity_schemas, IDENTITY_SCHEMA,identity);errors.extend(shape)
            if not shape:
                subject_identity=identity
                compare('IDENTIFIER_SUBJECT_IDENTITY_BINDING_MISMATCH',identity['identityRecordId'],subject['subjectRef'],
                    original(identity_entry,'/identityRecordId'),claim('/scope/subject/subjectRef'))
                compare('IDENTIFIER_SUBJECT_IDENTITY_KIND_MISMATCH',identity['identityType'],kind,
                    original(identity_entry,'/identityType'),claim('/scope/subject/subjectType'),identity['identityType'] in KINDS[kind])
                if 'createdByAssertionRecordRef' in identity:
                    if intent is None:
                        missing.append({'role':'IDENTIFIER_IDENTITY_CREATION_CONTEXT','pointer':'/createdByAssertionRecordRef'})
                    else:
                        compare('IDENTIFIER_SUBJECT_NOT_CREATED_BY_PROPOSED_ASSERTION',identity['createdByAssertionRecordRef'],intent['effectSubject']['subjectRef'],
                            original(identity_entry,'/createdByAssertionRecordRef'),{'inputRole':'EFFECT_INTENT','pointer':'/effectSubject/subjectRef'},
                            identity['createdByAssertionRecordRef']!=intent['effectSubject']['subjectRef'])
    elif kind not in SUBJECT_TYPES:
        missing.append({'role': 'IDENTIFIER_EXACT_SUBJECT_KIND_MEANING:' + kind, 'pointer': '/scope/subject/subjectType'})
    elif code['localSubject']['subjectType'] == 'OTHER':
        missing.append({'role': 'IDENTIFIER_UNSPECIFIED_LOCAL_SUBJECT_KIND', 'pointer': '/localSubject/subjectType'})
    elif code['localSubject']['subjectType'] not in SUBJECT_TYPES[kind]:
        errors.append({'code': 'IDENTIFIER_LOCAL_SUBJECT_KIND_MISMATCH', 'pointer': '/localSubject/subjectType'})
    field = definition['valueField']; value = code['bindingValue']
    if field not in value:
        missing.append({'role': 'IDENTIFIER_SELECTED_VALUE_FIELD', 'pointer': '/bindingValue/' + field})
        absent_operand('IDENTIFIER_SELECTED_VALUE_FIELD_AVAILABLE', entry, '/bindingValue/' + field, claim('/body/value'), body['value'])
    else:
        compare('IDENTIFIER_SELECTED_VALUE_MISMATCH', value[field], body['value'], original(entry, '/bindingValue/' + field), claim('/body/value'))
    compare('IDENTIFIER_ORIGINAL_LABEL_CHANGED', value['capturedLabel'], body['originalLexicalValue'],
        original(entry, '/bindingValue/capturedLabel'), claim('/body/originalLexicalValue'))
    role = definition['identifierRole']
    if observed_branch('IDENTIFIER_PRODUCT_ROLE_APPLICABLE', role in ['COMMERCIAL_REFERENCE', 'PRODUCT_OR_INPUT', 'GTIN'],
            origins=[original(definition_entry, '/identifierRole')]):
        role_constraint('IDENTIFIER_PRODUCT_OR_COMMERCIAL_ROLE_REQUIRED',
            predicate_value(definition_entry, '/sourceBindingRole', definition['sourceBindingRole'],
                'IDENTIFIER_PRODUCT_OR_COMMERCIAL_ROLE_REQUIRED') not in PRODUCT_IDENTIFIER_ROLES,
            '/sourceBindingRole', 'IDENTIFIER_PRODUCT_ROLE_APPLICABLE')
    if observed_branch('IDENTIFIER_GTIN_ROLE_APPLICABLE', role == 'GTIN',
            origins=[original(definition_entry, '/identifierRole')]):
        role_constraint('IDENTIFIER_GTIN_FIELD_REQUIRED',
            predicate_value(definition_entry, '/valueField', field, 'IDENTIFIER_GTIN_FIELD_REQUIRED') != 'gtin',
            '/valueField', 'IDENTIFIER_GTIN_ROLE_APPLICABLE')
    if observed_branch('IDENTIFIER_REGULATORY_ROLE_APPLICABLE', role == 'REGULATORY_REFERENCE',
            origins=[original(definition_entry, '/identifierRole')]):
        role_constraint('IDENTIFIER_REGULATORY_REFERENCE_ROLE_REQUIRED',
            predicate_value(definition_entry, '/sourceBindingRole', definition['sourceBindingRole'],
                'IDENTIFIER_REGULATORY_REFERENCE_ROLE_REQUIRED') != 'REGULATORY_AUTHORISATION'
            or predicate_value(definition_entry, '/valueField', field,
                'IDENTIFIER_REGULATORY_REFERENCE_ROLE_REQUIRED') not in ['authorisationRef', 'registrationRef', 'code'],
            '/sourceBindingRole', 'IDENTIFIER_REGULATORY_ROLE_APPLICABLE')
    if observed_branch('IDENTIFIER_ACTIVE_SUBSTANCE_ROLE_APPLICABLE', role == 'ACTIVE_SUBSTANCE',
            origins=[original(definition_entry, '/identifierRole')]):
        role_constraint('IDENTIFIER_ACTIVE_SUBSTANCE_ROLE_REQUIRED',
            predicate_value(definition_entry, '/sourceBindingRole', definition['sourceBindingRole'],
                'IDENTIFIER_ACTIVE_SUBSTANCE_ROLE_REQUIRED') != 'ACTIVE_SUBSTANCE',
            '/sourceBindingRole', 'IDENTIFIER_ACTIVE_SUBSTANCE_ROLE_APPLICABLE')
    if role == 'GOVERNANCE_IDENTITY':
        missing.append({'role': 'GOVERNANCE_IDENTITY_SOURCE_USE', 'pointer': '/body/identifierRole'})
    if value.get('mappingRelation') not in ['EXACT', 'LOCAL_ONLY']:
        missing.append({'role': 'IDENTIFIER_NONEXACT_OR_UNSPECIFIED_MAPPING_USE', 'pointer': '/bindingValue/mappingRelation'})
    # Bare subject and issuer references provide no immutable version/time
    # applicability. Keep those owner/use duties after this field interpretation.
    retained = {'originalCodeBinding': code, 'definitionBinding': definition_entry['binding'],
        **({'originalSubjectIdentity':subject_identity} if subject_identity is not None else {}),
        'interpretationScope': definition['interpretationScope'],
        'notEstablished': ['SUBJECT_VERSION_AND_TIME_APPLICABILITY', 'SCHEME_ISSUER_AND_DEFINITION_ADOPTION',
            'SOURCE_ELIGIBLE_USE', 'GOVERNANCE_IDENTITY', 'REGULATORY_STATUS_OR_AUTHORIZATION']}
    return result()
