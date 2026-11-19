"""Explicit field roles for the 58 typed atoms and outer carrier.

These are field declarations, not a suffix search. Unknown binding paths cause
the schema-to-role audit to fail. Citation membership is separate from source
resolution, eligible use, admission and any claim of truth.
"""
from strict_inputs import same, digest

# Every entry is relative to atom.body. Common typed operation fields are
# declared once; each operation's distinct parameter fields remain explicit.
ROW_FIELDS = {
 'S01': 'crs value', 'S02': 'parent/binding', 'S03': 'geometry purpose',
 'S04': 'attempt crop establishment scope variety', 'S05': 'containers/* layout storagePlaces/*',
 'S06': 'cohort traceabilityClaimBasis', 'S07': 'formulation identity',
 'S08': 'assignedPerformer method resources/* target', 'S09': 'existingSuccessors/* predecessors/*',
 'S10': 'scheme', 'S11': 'parentScope value', 'S12': 'asset configuration inspectionEvidence/*',
 'S13': '''container occupancies/*/lot occupancyEvidence/selection/place/binding occupancyEvidence/selection/selectionBasis/*
 occupancyEvidence/episodes/*/binding occupancyEvidence/episodes/*/expectedFacts/relationConcept
 occupancyEvidence/episodes/*/expectedFacts/occupant/binding occupancyEvidence/episodes/*/expectedFacts/place/binding
 occupancyEvidence/episodes/*/expectedFacts/interval/start/basis occupancyEvidence/episodes/*/expectedFacts/interval/end/basis
 occupancyEvidence/episodes/*/expectedFacts/occupiedQuantity/quantityKind occupancyEvidence/episodes/*/expectedFacts/occupiedQuantity/unitIdentity
 occupancyEvidence/episodes/*/expectedFacts/occupiedCohort/binding occupancyEvidence/episodes/*/expectedFacts/relevantExtent/binding
 occupancyEvidence/episodes/*/expectedFacts/sourcePosture/ownerEvidence/* occupancyEvidence/episodes/*/expectedFacts/sourcePosture/supersededBy/*
 occupancyEvidence/episodes/*/expectedFacts/sourceEvidence/* occupancyEvidence/episodes/*/expectedFacts/lifecycleEvidence/*''',
 'S14': 'facility layoutPosition lineage/* location',
 'C01': 'basis rule', 'C02': 'crop rule use',
 'C03': 'criterion measurement', 'C04': 'criterion operand/codedValue operand/mappingBinding operand/scaleBinding',
 'C05': 'profile snapshots/* verificationTrace', 'C06': 'boundFrom condition crop product target rateSource/sourceBinding',
 'C07': 'basis criterion', 'C08': 'decision rule subject',
 'C09': 'charter claimBasis metric', 'C10': 'evidenceSet/* policy',
 'C11': 'holding officialArtefact renewal/binding',
 'C12': 'accreditationSnapshot category certificate certificateSubject/binding holding issuer/binding ministrySnapshot',
 'C13': 'accreditationSnapshot certifier/binding ministrySnapshot scope',
 'C14': 'authorityAddressed challengedAct reviewArtefact serviceProof',
 'C15': 'cropCodes filedGO history/*/crop history/*/cropCodeRevision history/*/lineage/* history/*/parcel history/*/source holding lineage/* parcel parcelSnapshot',
 'C16': 'evaluationBasis/binding evaluationBasis/lineageAllocation evaluationBasis/precedenceRule evaluationBasis/profileRevision evaluationBasis/roundingRule evaluationBasis/yearCodeCrosswalk historyClaim parcel routeEvidence rustgewasEvidence soilEvidence',
 'C17': 'record requirementsRevision',
}
OPERATION_COMMON = '''activityInstance extent/binding performedBy target/binding
 workSpecification/activityInstance workSpecification/binding workSpecification/extent/binding
 workSpecification/outputSpecification workSpecification/procedure workSpecification/target/binding
 quantityParameters/*/activityInstance quantityParameters/*/appliesTo/extent/binding
 quantityParameters/*/appliesTo/processPoint quantityParameters/*/appliesTo/target/binding
 quantityParameters/*/basis/subject quantityParameters/*/basis/subject/binding
 quantityParameters/*/material/binding quantityParameters/*/material/components/*/binding
 quantityParameters/*/material/materialDefinition quantityParameters/*/sourceParameterBinding
 quantityParameters/*/value/normalized/conversionBinding quantityParameters/*/value/original/sourceBinding
 quantityParameters/*/value/unitProfile'''
COHORT = '{field}/* {field}/*/claimBasis {field}/*/cohortBoundary {field}/*/materialIdentity'
OPERATION_PARAMETERS = {
 'O01': 'method overallWorkCoverage/overallWorkSpecification product targetOrganism',
 'O02': 'fertilizer nutrient', 'O03': 'attempt crop replantOf seedLot',
 'O04': 'method waterSource', 'O05': 'method',
 'O06': 'cropCycle ' + COHORT.format(field='outputLots'),
 'O07': 'inputLot method', 'O08': 'method plantPart',
 'O09': 'method observationContext observedProperty',
 'O10': 'analyticalResult/binding sample sampledProperty samplingProcedure',
 'O11': 'predecessors/* ' + COHORT.format(field='successors'),
 'O12': 'predecessors/* ' + COHORT.format(field='successors'),
 'O13': 'claimBasisAfter predecessors/* ' + COHORT.format(field='successors'),
 'O14': 'inputLots/* method ' + COHORT.format(field='outputLots'),
 'O15': 'from lot to', 'O16': 'reportedClaim reportingChannel', 'O17': 'material method',
 'O18': 'asset method replacedPart',
 'O19': 'crop equipment/binding equipment/inspection officialIdentity parcel/binding parcel/snapshot product professionalUser stage/basis stage/stage trainingEvidence',
 'O20': 'batchIfApplicable product', 'O21': 'batchIfApplicable product',
 'O22': 'method producedResult/binding producedResult/specificationBinding property sample',
 'O23': 'destinationContext report/binding sourceSystem',
 'O24': 'deliveryReference destination/binding material/binding origin/binding receiptMethod receivedCondition/condition receiver sender',
 'O25': 'afterClaimBasis beforeClaimBasis classificationBasis classificationScheme fromClass material/binding method successorProposal/lineage/* successorProposal/prospectiveCohort/claimBasis successorProposal/prospectiveCohort/cohortBoundary successorProposal/prospectiveCohort/materialIdentity toClass',
 'O26': 'destination/binding disposalMethod disposalRecord disposalRoute material/binding reason residualMaterial/material/binding',
 'O27': 'creationProcedure originActivity predecessors/* prospectiveLot/claimBasis prospectiveLot/cohortBoundary prospectiveLot/materialIdentity',
}
MEASUREMENT_FIELDS = 'measurementBinding contextBinding methodUseBinding subjectRelationBinding'
SCALAR_FIELDS = 'normalized/conversionBinding provenance/sourceBinding unitProfile'
MEASURED = {'C03': 'measurementSource', 'C04': 'operand/source',
            'C06': 'rateSource/measurementSource', 'C09': 'measurementSource'}
SCALARS = {'C03': 'threshold threshold/lower threshold/upper',
           'C04': 'operand/quantity operand/limit threshold threshold/lower threshold/upper',
           'C06': 'rate', 'C16': 'evaluationBasis/numerator evaluationBasis/denominator'}


def field_table():
    table = {r: set(paths.split()) for r, paths in ROW_FIELDS.items()}
    for row, paths in OPERATION_PARAMETERS.items():
        table[row] = set(OPERATION_COMMON.split()) | {'parameters/' + p for p in paths.split()}
    for row, prefix in MEASURED.items():
        table[row].update(prefix + '/' + p for p in MEASUREMENT_FIELDS.split())
        table[row].update(['measuredQualification/sourceBinding', 'measuredQualification/methodUseBinding'])
    for row, prefixes in SCALARS.items():
        table[row].update(prefix + '/' + p for prefix in prefixes.split() for p in SCALAR_FIELDS.split())
    assert len(table) == 58
    return table


# These fields are cited supporting records, rather than mere identity/value
# references. The v4 amendment supplies the established measured/output roles;
# the additional rows name their actual documentary/record fields explicitly.
CITATIONS = {
 'S13': 'occupancyEvidence/episodes/*/binding occupancyEvidence/selection/selectionBasis/*',
 'S12': 'configuration inspectionEvidence/*',
 'O10': 'parameters/analyticalResult/binding',
 'O16': 'parameters/reportedClaim',
 'O19': 'parameters/officialIdentity parameters/parcel/snapshot parameters/stage/basis parameters/trainingEvidence parameters/equipment/inspection',
 'O22': 'parameters/producedResult/binding', 'O23': 'parameters/report/binding',
 'O24': 'parameters/deliveryReference', 'O25': 'parameters/classificationBasis',
 'O26': 'parameters/disposalRecord',
 'C01': 'basis', 'C03': 'measurement', 'C04': 'operand/limit/provenance/sourceBinding operand/quantity/provenance/sourceBinding',
 'C05': 'snapshots/* verificationTrace', 'C06': 'rateSource/sourceBinding rate/provenance/sourceBinding',
 'C08': 'decision', 'C10': 'evidenceSet/*', 'C11': 'officialArtefact renewal/binding',
 'C12': 'certificate ministrySnapshot accreditationSnapshot',
 'C13': 'ministrySnapshot accreditationSnapshot',
 'C14': 'challengedAct reviewArtefact serviceProof',
 'C15': 'filedGO parcelSnapshot history/*/source',
 'C16': 'historyClaim soilEvidence rustgewasEvidence routeEvidence evaluationBasis/binding',
 'C17': 'record',
}


def citation_paths(row, body):
    result = set(CITATIONS.get(row, '').split())
    if row.startswith('O'):
        result.add('quantityParameters/*/value/original/sourceBinding')
    if row in MEASURED:
        prefix = MEASURED[row]
        result.update(prefix + '/' + p for p in MEASUREMENT_FIELDS.split())
        result.update(['measuredQualification/sourceBinding', 'measuredQualification/methodUseBinding'])
    if row == 'O22' and body['parameters']['producedResult']['role'] != 'ACTUAL_OUTPUT':
        result.discard('parameters/producedResult/binding')
    if row == 'O23' and body['parameters']['report']['role'] != 'ACTUAL_REPORT':
        result.discard('parameters/report/binding')
    return result


def select(value, pattern, path=''):
    parts = pattern.split('/') if pattern else []
    if not parts:
        return [(path, value)]
    key, rest = parts[0], '/'.join(parts[1:])
    if key == '*':
        if not isinstance(value, list):
            return []
        return [hit for n, v in enumerate(value) for hit in select(v, rest, path + '/' + str(n))]
    if not isinstance(value, dict) or key not in value:
        return []
    return select(value[key], rest, path + '/' + key)


def immutable(value):
    return (isinstance(value, dict)
            and set(value) in [{'ref', 'revisionRef'}, {'ref', 'digest'}]
            and all(isinstance(item, str) and item for item in value.values()))


def citation_membership_checks(references, evidence):
    """Compare each actual citation with the original declared evidence array."""
    return [{'pointer': entry['pointer'], 'binding': entry['binding'],
             'evidencePointer': '/evidenceBindings',
             'equal': any(same(entry['binding'], item) for item in evidence)}
            for entry in references if entry['role'] == 'ASSERTION_EVIDENCE']


def collect(intent):
    """Requires successful selected intent/proposition schema validation first."""
    refs = []; errors = []; table = field_table()
    def add(role, binding, path, row=None, *, rule_group, rule_selector,
            definition_ref=None, atom_pointer=None):
        if not immutable(binding):
            errors.append({'code': 'MALFORMED_TYPED_SOURCE_BINDING',
                           'pointer': path})
            return
        # This identifies the exact candidate field rule which exposed the
        # occurrence. It is not an owner selector or an admission decision.
        rule = {'module': 'reference_roles.py', 'group': rule_group,
                'selector': rule_selector}
        if definition_ref is not None:
            rule['definitionRef'] = definition_ref
            rule['atomPointer'] = atom_pointer
        refs.append({'role': role, 'binding': binding, 'pointer': path,
                     'candidateRule': rule,
                     **({'definition': row} if row else {})})
    body = intent['assertionBody']; evidence = intent['evidenceBindings']
    outer = {
        'evidenceBindings/*': 'ASSERTION_EVIDENCE',
        'subjectScopeProofBindings/*': 'SUBJECT_SCOPE_RELATION_PROOF',
        'scopeProofBindings/*': 'AUTHORITY_SCOPE_PROOF',
        'dataSovereigntyBoundaryBindings/*': 'DATA_SOVEREIGNTY_BOUNDARY',
        'associatedSemanticEventBinding': 'SEMANTIC_EVENT',
        'assertionActEvidenceBinding': 'ASSERTION_ACT_EVIDENCE',
        'supersedesAssertionRecordBinding': 'PRIOR_ASSERTION',
        'softwareAgentActorshipBindings/*': 'SOFTWARE_AGENT_ACTORSHIP',
        'performerAuthorityEvidenceBindings/*': 'PERFORMER_AUTHORITY_EVIDENCE',
        'ruleRevisionBindings/*': 'RULE_REVISION',
        'evidencePolicyRevisionBindings/*': 'EVIDENCE_POLICY_REVISION',
        'effectSubject/effectSubjectProofBindings/*': 'PROSPECTIVE_EFFECT_PROOF',
        'resources/*/authorizationResourceProofBindings/*': 'AUTHORIZATION_RESOURCE_PROOF',
        'assertionBody/contextBindings/*/binding': 'CONTEXT_IDENTITY',
        'assertionBody/contextBindings/*/relationshipProofBindings/*': 'CONTEXT_RELATIONSHIP_PROOF',
        'assertionBody/performedByBinding': 'PERFORMER_IDENTITY',
        'assertionBody/interventionIntentPayloadBindings/*': 'INTERVENTION_INTENT_PAYLOAD',
        'assertionBody/executionRecordPayloadBindings/*': 'EXECUTION_RECORD_PAYLOAD',
        'assertionBody/temporalQualifications/collectionProvenance': 'ASSERTION_EVIDENCE',
    }
    for selector, role in outer.items():
        for path, value in select(intent, selector):
            if immutable(value):
                add(role, value, path, rule_group='OUTER_FIELD',
                    rule_selector=selector)
            elif isinstance(value, dict) and 'ref' in value:
                # The existing explicitly typed payload/evidence wrappers carry
                # schema metadata in addition to the immutable binding itself.
                binding = {k: value[k] for k in ['ref', 'revisionRef', 'digest'] if k in value}
                if immutable(binding):
                    add(role, binding, path, rule_group='OUTER_FIELD',
                        rule_selector=selector)
                else:
                    errors.append({'code': 'MALFORMED_TYPED_SOURCE_BINDING',
                                   'pointer': path})
            else:
                errors.append({'code': 'MALFORMED_TYPED_SOURCE_BINDING',
                               'pointer': path})
    for selector, role, kind, ref in [('subject', 'ASSERTION_SUBJECT', 'subjectType', 'subjectRef'),
                                       ('resources/*/scope', 'AUTHORITY_SCOPE', 'scopeType', 'scopeRef')]:
        for path, value in select(intent, selector):
            if not isinstance(value, dict) or ref not in value:
                errors.append({'code': 'MALFORMED_TYPED_SOURCE_BINDING',
                               'pointer': path})
                continue
            binding = {'ref': value[ref], **{k: value[k] for k in ['revisionRef', 'digest'] if k in value}}
            if immutable(binding):
                add(role, binding, path, rule_group='OUTER_TYPED_SCOPE',
                    rule_selector=selector)
            else:
                errors.append({'code': 'MALFORMED_TYPED_SOURCE_BINDING',
                               'pointer': path})
    temporal = body.get('temporalBasis', {})
    if not isinstance(temporal, dict):
        errors.append({'code': 'MALFORMED_TEMPORAL_BASIS',
                       'pointer': '/assertionBody/temporalBasis'})
        temporal = {}
    for field, role in [('evidenceBinding', 'ASSERTION_EVIDENCE'),
                         ('payloadBinding', temporal.get('sourceKind', 'UNSELECTED_TEMPORAL_SOURCE'))]:
        if field in temporal:
            v = temporal[field]
            b = ({k: v[k] for k in ['ref', 'revisionRef', 'digest'] if k in v}
                 if isinstance(v, dict) else None)
            location = '/assertionBody/temporalBasis/' + field
            if immutable(b):
                add(role, b, location, rule_group='TEMPORAL_BASIS',
                    rule_selector=field)
            else:
                errors.append({'code': 'MALFORMED_TEMPORAL_SOURCE_BINDING',
                               'pointer': location})
    def walk(p, path):
        if p['form'] != 'ATOM':
            if 'child' in p:
                walk(p['child'], path + '/child')
            else:
                for n, child in enumerate(p['children']):
                    walk(child, path + '/children/' + str(n))
            return
        definition_ref = p.get('definition')
        if not isinstance(definition_ref, str):
            errors.append({'code': 'MALFORMED_ATOM_DEFINITION_REF',
                           'pointer': path + '/definition'})
            return
        row = definition_ref.split(':')[-1]
        if row not in table:
            errors.append({'code': 'UNKNOWN_ATOM_DEFINITION_ROW',
                           'pointer': path + '/definition'})
            return
        subject = p['scope']['subject']
        if not isinstance(subject, dict) or 'subjectRef' not in subject:
            errors.append({'code': 'MALFORMED_TYPED_SOURCE_BINDING',
                           'pointer': path + '/scope/subject'})
            return
        b = {'ref': subject['subjectRef'], **{k: subject[k] for k in ['revisionRef', 'digest'] if k in subject}}
        if immutable(b):
            add('ATOM_SUBJECT', b, path + '/scope/subject', row,
                rule_group='ROW_SCOPE', rule_selector='scope/subject',
                definition_ref=p['definition'], atom_pointer=path)
        else:
            errors.append({'code': 'MALFORMED_TYPED_SOURCE_BINDING',
                           'pointer': path + '/scope/subject'})
        add('ATOM_EXTENT', p['scope']['extent']['binding'], path + '/scope/extent/binding', row,
            rule_group='ROW_SCOPE', rule_selector='scope/extent/binding',
            definition_ref=p['definition'], atom_pointer=path)
        cites = citation_paths(row, p['body'])
        for pattern in sorted(table[row]):
            for suffix, value in select(p['body'], pattern):
                if immutable(value):
                    add('ASSERTION_EVIDENCE' if pattern in cites else 'DEFINITION_OR_CONTEXT_INPUT', value,
                        path + '/body' + suffix, row,
                        rule_group='ROW_BODY_FIELD', rule_selector=pattern,
                        definition_ref=p['definition'], atom_pointer=path)
                else:
                    errors.append({'code': 'MALFORMED_TYPED_SOURCE_BINDING',
                                   'pointer': path + '/body' + suffix})
    walk(body['proposition'], '/assertionBody/proposition')
    for entry in citation_membership_checks(refs, evidence):
        if not entry['equal']:
            errors.append({'code': 'CITATION_NOT_EXACT_EVIDENCE_MEMBER', 'pointer': entry['pointer'],
                           'bindingDigest': digest(entry['binding'])})
    return {'references': refs, 'errors': errors,
            'qualification': 'Typed reference and citation closure only. Every reference still needs original bytes, exact owner resolution and eligible-use checks.'}


def audit_schema_roles(schemas, proposition_id):
    """Check explicit declarations against typed binding paths, without data scans."""
    def walk(schema, base, path='', depth=0):
        if depth > 32:
            raise ValueError('Unexpected schema recursion in an atom field contract.')
        found = set()
        # The reviewed occupancy schema spells closed immutable selectors
        # inline. Recognize their exact schema structure, never field suffixes.
        alternatives = schema.get('oneOf', [])
        if len(alternatives) == 2 and {frozenset(v.get('required', [])) for v in alternatives} == {frozenset(['ref','digest']), frozenset(['ref','revisionRef'])}:
            if all(v.get('type') == 'object' and v.get('additionalProperties') is False
                   and set(v.get('properties', {})) == set(v['required']) for v in alternatives):
                return {path.lstrip('/')}
        if '$ref' in schema:
            url, _, fragment = schema['$ref'].partition('#'); url = url or base
            if fragment == '/$defs/immutableBinding':
                return {path.lstrip('/')}
            target = schemas[url]
            for key in fragment.split('/')[1:]:
                target = target[key]
            found.update(walk(target, url, path, depth + 1))
        for key, value in schema.get('properties', {}).items():
            found.update(walk(value, base, path + '/' + key, depth + 1))
        if isinstance(schema.get('items'), dict):
            found.update(walk(schema['items'], base, path + '/*', depth + 1))
        for keyword in ['oneOf', 'anyOf', 'allOf']:
            for sub in schema.get(keyword, []):
                found.update(walk(sub, base, path, depth + 1))
        return found
    errors = []
    for row, declared in field_table().items():
        actual = walk(schemas[proposition_id]['$defs'][row]['properties']['body'], proposition_id)
        if actual != declared:
            errors.append({'row': row, 'undeclared': sorted(actual - declared), 'obsolete': sorted(declared - actual)})
    return errors
