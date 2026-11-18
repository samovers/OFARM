"""Typed context identities and directed fields without authority widening.

Context identities are resolved at their exact declared versions. Known parent
fields use the claimed context's actual use time. Source eligibility and other
relationship families remain explicit, and the sole authority anchor is never
replaced by a body context.
"""
from strict_inputs import same, digest
from identity_sources import KINDS, IDENTITY_SCHEMA


from domain_reader_occurrences import reader, selection as observe_selection, guard as observe_guard, origin as read_origin, observed_shape, branch as observed_branch, observe_comparisons


@reader('context_sources.py', ['AR_BODY'])
def evaluate(intent, sources, schemas, inventory=None):
    contexts = intent['assertionBody'].get('contextBindings', [])
    errors, missing, comparisons, ids, refs, uses = [], [], [], [], [], []
    def finish():
        return {'disposition': 'FAIL' if errors else 'NOT_EVALUATED' if missing else 'NOT_APPLICABLE' if not contexts else 'PASS',
            'errors': errors, 'remainingRoles': missing, 'comparisons': comparisons,
            'sourceInputIds': sorted(set(ids)), 'requiredReferences': refs, 'contextUses': uses,
            'qualification': 'Typed original context identities and selected directed parent fields only. Contexts do not enlarge the sole authority anchor; source/relationship eligibility remains separate.'}
    if not contexts: return finish()
    if inventory is None:
        from reference_roles import collect
        inventory = collect(intent)
    anchor = intent['resources'][0]['scope']
    def compare(code, a, b, source, destination, okay=None):
        equal = same(a, b) if okay is None else okay
        comparisons.append({'predicateId': code, 'equal': equal, 'pointer': destination['pointer'],
            'source': {**source, 'valueDigest': digest(a)}, 'destination': {**destination, 'valueDigest': digest(b)},
            'disposition': 'PASS' if equal else 'FAIL'})
        observe_comparisons([comparisons[-1]])
        if not equal: errors.append({'code': code, 'pointer': destination['pointer']})
    def original(role, path): return {'inputRole': role, 'pointer': path}
    def declared(path): return original('EFFECT_INTENT', path)
    def atoms(p, path):
        if p['form'] == 'ATOM': yield p, path
        elif 'child' in p: yield from atoms(p['child'], path + '/child')
        else:
            for n, child in enumerate(p['children']): yield from atoms(child, path + '/children/' + str(n))
    leaves = list(atoms(intent['assertionBody']['proposition'], '/assertionBody/proposition'))
    for n, context in enumerate(contexts):
        path = '/assertionBody/contextBindings/' + str(n); kind = context['contextRole']; binding = context['binding']
        if observed_branch('CONTEXT_IDENTITY_KIND', kind not in KINDS, origins=[declared(path + '/contextRole')]):
            missing.append({'role': 'EXACT_SPECIALIZED_CONTEXT_IDENTITY:' + kind, 'pointer': path})
        else:
            selected = [v for v in sources if same(v['binding'], binding)]
            observe_selection('CONTEXT_IDENTITY', sources, selected, binding=binding,
                origins=[read_origin('EFFECT_INTENT', path + '/binding'), read_origin('EFFECT_INTENT', path + '/contextRole')])
            if len(selected) != 1:
                missing.append({'role': 'EXACT_CONTEXT_IDENTITY_ORIGINAL', 'pointer': path + '/binding'})
            else:
                entry = selected[0]; record = entry['record']; ids.append(entry['id'])
                shape = observed_shape(schemas, IDENTITY_SCHEMA, record); errors.extend(shape)
                if not shape:
                    compare('CONTEXT_IDENTITY_BINDING_MISMATCH', record['identityRecordId'], binding['ref'],
                            original(entry['id'], '/identityRecordId'), declared(path + '/binding/ref'))
                    compare('CONTEXT_IDENTITY_KIND_MISMATCH', record['identityType'], kind,
                            original(entry['id'], '/identityType'), declared(path + '/contextRole'), record['identityType'] in KINDS[kind])
                    created_here = record.get('createdByAssertionRecordRef') == intent['effectSubject']['subjectRef']
                    observe_comparisons([{'predicateId': 'CONTEXT_IDENTITY_CANNOT_BE_CREATED_BY_THIS_ASSERTION',
                        'source': original(entry['id'], '/createdByAssertionRecordRef'),
                        'destination': declared('/effectSubject/subjectRef'),
                        'disposition': 'FAIL' if created_here else 'PASS'}])
                    if created_here:
                        errors.append({'code': 'CONTEXT_IDENTITY_CANNOT_BE_CREATED_BY_THIS_ASSERTION', 'pointer': path})
        times = []
        for atom, atom_path in leaves:
            subject = atom['scope']['subject']
            selected_binding = {'ref': subject['subjectRef'], **{k: subject[k] for k in ['digest', 'revisionRef'] if k in subject}}
            use_pointers = []
            if same(selected_binding, binding):
                use_pointers.append(atom_path + '/scope/subject')
                compare('CONTEXT_ATOM_SUBJECT_KIND_MISMATCH', kind, subject['subjectType'],
                        declared(path + '/contextRole'), declared(atom_path + '/scope/subject/subjectType'))
                for key, other in [('ref', 'subjectRef'), ('revisionRef', 'revisionRef'), ('digest', 'digest')]:
                    if key in binding:
                        compare('CONTEXT_ATOM_SUBJECT_' + key.upper() + '_MISMATCH', binding[key], subject[other],
                                declared(path + '/binding/' + key), declared(atom_path + '/scope/subject/' + other))
            # Use the audited typed-field inventory, not a suffix search or an
            # arbitrary recursive scan. A context used by a body parameter or
            # extent has the same child's time even when it is not its subject.
            body_uses = [v for v in inventory['references'] if same(v['binding'], binding)
                and (v['pointer'].startswith(atom_path + '/body/')
                     or v['pointer'] == atom_path + '/scope/extent/binding')]
            for use in body_uses:
                use_pointers.append(use['pointer'])
                for key in ['ref', 'revisionRef', 'digest']:
                    if key in binding:
                        compare('CONTEXT_TYPED_USE_' + key.upper() + '_MISMATCH', binding[key], use['binding'][key],
                                declared(path + '/binding/' + key), declared(use['pointer'] + '/' + key))
            if use_pointers:
                times.append((atom['scope']['subjectTime'], atom_path + '/scope/subjectTime', sorted(set(use_pointers))))
        if not times: times = [(intent['subjectTime'], '/subjectTime', [])]
        uses.extend({'contextPointer': path, 'timePointer': tp, 'timeDigest': digest(t), 'usePointers': pointers}
                    for t, tp, pointers in times)
        direct = kind == anchor['scopeType'] and same(binding, {'ref': anchor['scopeRef'], **{k: anchor[k] for k in ['revisionRef', 'digest'] if k in anchor}})
        if observed_branch('CONTEXT_DIRECT_ANCHOR', direct, origins=[declared(path + '/binding'), declared(path + '/contextRole'), declared('/resources/0/scope')]):
            for key, other in [('ref', 'scopeRef'), ('revisionRef', 'revisionRef'), ('digest', 'digest')]:
                if key in binding:
                    compare('DIRECT_CONTEXT_ANCHOR_' + key.upper() + '_MISMATCH', binding[key], anchor[other],
                            declared(path + '/binding/' + key), declared('/resources/0/scope/' + other))
            missing.append({'role': 'DECLARED_CONTEXT_RELATION_PROOF_USE', 'pointer': path + '/relationshipProofBindings'})
        elif kind == 'CROP_CYCLE' or kind == 'FIELD' and anchor['scopeType'] == 'FARM':
            from relation_sources import evaluate_body as relations
            for time, time_pointer, use_pointers in times:
                # This internal view selects existing original fields. Every
                # emitted destination pointer is redirected to those originals.
                view = {**intent, 'subject': {'subjectPosture': 'EXISTING_SUBJECT', 'subjectType': kind,
                    'subjectRef': binding['ref'], **{k: binding[k] for k in ['revisionRef', 'digest'] if k in binding}},
                    'subjectTime': time, 'subjectScopeProofBindings': context['relationshipProofBindings']}
                checked = relations(view, sources, schemas, subject_pointer=path + '/binding', subject_ref_field='ref',
                                    proofs_pointer=path + '/relationshipProofBindings', time_pointer=time_pointer,
                                    subject_kind_pointer=path + '/contextRole')
                errors.extend(checked['errors']); missing.extend(checked['remainingRoles']); comparisons.extend(checked['comparisons'])
                ids.extend(checked['sourceInputIds']); refs.extend(checked['requiredReferences'])
        else:
            missing.append({'role': 'EXACT_CONTEXT_RELATION_TO_SUBJECT_OR_ANCHOR:' + kind,
                            'pointer': path + '/relationshipProofBindings'})
    return finish()
