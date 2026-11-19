"""S02 original parent fields, exact endpoint identities and child use time.

The body parent is a structural allegation, never a replacement authority
anchor. Logical parent fields and a cycle lifetime do not establish eligible
historical membership or the relationship's endpoint version applicability.
"""
from strict_inputs import same, digest
from identity_sources import IDENTITY_SCHEMA, KINDS
from relation_sources import KINDS as PARENT_KINDS, evaluate_body as relation_fields


from domain_reader_occurrences import reader, selection as observe_selection, guard as observe_guard, origin as read_origin, observed_shape, predicate_value, observe_comparisons


@reader('parent_claim_sources.py', ['AR_BODY'])
def evaluate(atom, intent, sources, schemas, path):
    subject = atom['scope']['subject']; parent = atom['body']['parent']
    errors, missing, comparisons, ids, refs = [], [], [], [], []
    result = {'scope': 'ORIGINAL_BODY_PARENT_FIELDS_AND_ENDPOINT_IDENTITIES',
              'errors': errors, 'remainingRoles': missing, 'comparisons': comparisons,
              'sourceInputIds': ids, 'requiredReferences': refs}
    def finish():
        return {**result, 'disposition': 'FAIL' if errors else 'NOT_EVALUATED' if missing else 'PASS',
                'qualification': 'Selected original identity and parent fields only. No authority, admitted governed membership, prospective identity creation or source eligibility is inferred.'}
    def need(role, pointer): missing.append({'role': role, 'pointer': pointer})
    def compare(code, actual, expected, source, destination, equal=None):
        okay = same(actual, expected) if equal is None else equal
        comparisons.append({'predicateId': code, 'equal': okay,
            'source': {**source, 'valueDigest': digest(actual)},
            'destination': {'inputRole': 'EFFECT_INTENT', 'pointer': destination, 'valueDigest': digest(expected)},
            'disposition': 'PASS' if okay else 'FAIL'})
        observe_comparisons([comparisons[-1]])
        if not okay: errors.append({'code': code, 'pointer': destination})
    def endpoint(binding, kind, binding_path, ref_field, kind_path, role):
        if kind not in KINDS:
            need('EXACT_SPECIALIZED_PARENT_ENDPOINT_IDENTITY:' + kind, binding_path); return None
        matches = [v for v in sources if same(v['binding'], binding)]
        observe_selection(role, sources, matches, binding=binding,
            origins=[read_origin('EFFECT_INTENT', binding_path), read_origin('EFFECT_INTENT', kind_path)])
        if len(matches) != 1:
            need('EXACT_' + role + '_IDENTITY_ORIGINAL', binding_path); return None
        entry = matches[0]; record = entry['record']; ids.append(entry['id'])
        refs.append({'role': role + '_IDENTITY', 'binding': binding, 'pointer': binding_path})
        shape = observed_shape(schemas, IDENTITY_SCHEMA, record); errors.extend(shape)
        if shape: return None
        compare(role + '_IDENTITY_BINDING_MISMATCH', record['identityRecordId'], binding['ref'],
                {'inputRole': entry['id'], 'pointer': '/identityRecordId'}, binding_path + '/' + ref_field)
        compare(role + '_IDENTITY_KIND_MISMATCH', record['identityType'], kind,
                {'inputRole': entry['id'], 'pointer': '/identityType'}, kind_path, record['identityType'] in KINDS[kind])
        created_here = record.get('createdByAssertionRecordRef') == intent['effectSubject']['subjectRef']
        observe_comparisons([{'predicateId': role + '_IDENTITY_CREATED_BY_THIS_ASSERTION',
            'source': {'inputRole': entry['id'], 'pointer': '/createdByAssertionRecordRef'},
            'destination': {'inputRole': 'EFFECT_INTENT', 'pointer': '/effectSubject/subjectRef'},
            'disposition': 'FAIL' if created_here else 'PASS'}])
        if created_here:
            errors.append({'code': role + '_IDENTITY_CREATED_BY_THIS_ASSERTION', 'pointer': binding_path})
        return entry

    binding = {'ref': subject['subjectRef'], **{k: subject[k] for k in ['revisionRef', 'digest'] if k in subject}}
    child = None
    if subject['subjectPosture'] == 'EXISTING_SUBJECT':
        child = endpoint(binding, subject['subjectType'], path + '/scope/subject', 'subjectRef',
                         path + '/scope/subject/subjectType', 'PARENT_RELATION_CHILD')
    else:
        need('EXACT_PROSPECTIVE_CHILD_PARENT_RELATION_SOURCE', path + '/scope/subject')
    endpoint(parent['binding'], parent['kind'], path + '/body/parent/binding', 'ref',
             path + '/body/parent/kind', 'PARENT_RELATION_PARENT')
    kind = subject['subjectType']
    if kind not in PARENT_KINDS or subject['subjectPosture'] != 'EXISTING_SUBJECT':
        need('EXACT_DIRECTED_BODY_PARENT_SOURCE:' + kind, path + '/body/parent'); return finish()

    # Only real selected citation/proof paths can select a parent payload. A
    # protected read or independent revision map alone is not a claim selection.
    version = PARENT_KINDS[kind][0]
    candidates = []
    seen = set()
    for entry in sources:
        if not predicate_value(entry, '', isinstance(entry['record'], dict), 'BODY_PARENT_PAYLOAD') or predicate_value(entry, '/schemaVersion', entry['record'].get('schemaVersion'), 'BODY_PARENT_PAYLOAD') != version: continue
        selections = [v for v in entry['claimRoles'] if v['role'] in
                      ['ASSERTION_EVIDENCE', 'SUBJECT_SCOPE_RELATION_PROOF', 'CONTEXT_RELATIONSHIP_PROOF']]
        key = (entry['binding']['ref'], entry['rawSha256'], entry['valueDigest'])
        if selections and key not in seen:
            candidates.append((entry, selections[0]['pointer'])); seen.add(key)
    matches = [v for v in candidates if predicate_value(v[0], '/identityRecordRef', v[0]['record'].get('identityRecordRef'), 'BODY_PARENT_PAYLOAD') == binding['ref']]
    chosen = matches if matches else candidates
    selected_read = observe_selection('BODY_PARENT_PAYLOAD', sources, chosen,
        origins=[read_origin('EFFECT_INTENT', path + '/scope/subject'), read_origin('EFFECT_INTENT', path + '/body/parent')]
            + [read_origin('EFFECT_INTENT', location) for _, location in chosen])
    if len(chosen) != 1:
        need('EXACT_SELECTED_' + kind + '_BODY_PARENT_PAYLOAD', path + '/body/parent')
        if len(chosen) > 1:
            observe_comparisons([{'predicateId': 'AMBIGUOUS_BODY_PARENT_PAYLOAD',
                'source': read_origin('EFFECT_INTENT', path + '/body/parent'), 'disposition': 'FAIL'}],
                depends_on=[selected_read] if selected_read is not None else [])
            errors.append({'code': 'AMBIGUOUS_BODY_PARENT_PAYLOAD', 'pointer': path + '/body/parent'})
        return finish()
    entry, selection_pointer = chosen[0]
    result['selectedParentPayloadBinding'] = entry['binding']
    result['retainedSourceQualifications'] = {'originalParentPayload': entry['record']}
    # Internal view fields each point back to the actual submitted atom. The
    # authority resource is never used as the claimed structural parent.
    view = {**intent, 'subject': subject, 'subjectTime': atom['scope']['subjectTime'],
            'resources': [{'scope': parent}]}
    # A malformed identity cannot supply the current-payload link.
    checked_sources = [v for v in sources if not same(v['binding'], binding) or child is not None]
    finding = relation_fields(view, checked_sources, schemas,
        subject_pointer=path + '/scope/subject', time_pointer=path + '/scope/subjectTime',
        proofs_pointer=selection_pointer, selected_proofs=[(entry['binding'], selection_pointer)],
        anchor_pointer=path + '/body/parent', anchor_kind_field='kind', anchor_ref_field='binding/ref')
    errors.extend(finding['errors']); missing.extend(finding['remainingRoles'])
    comparisons.extend(finding['comparisons']); ids.extend(finding['sourceInputIds']); refs.extend(finding['requiredReferences'])
    # The original parent fields are bare logical references. Resolving both
    # selected identities does not bind those historical edges to their versions.
    need('PARENT_RELATION_ENDPOINT_VERSION_APPLICABILITY', selection_pointer)
    return finish()
