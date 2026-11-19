"""Conditional C01/C02 meaning from independently selected normative bytes.

These definitions are owned domain interpretations. They do not adopt rules,
establish legal currentness, supply factual crop/use context, or admit source
evidence. No applicable clause means unknown, never a negative determination.
"""
from definition_inputs import SCHEMAS, register
from strict_inputs import same, digest, distinct_selected_originals


from domain_reader_occurrences import reader, selection as observe_selection, guard as observe_guard, origin as read_origin, observed_shape, predicate_value, guard_refs, branch as observed_branch, observe_comparisons


@reader('rule_meaning_sources.py', ['AR_BODY'])
def evaluate(atom, sources, schemas, evidence_bindings):
    from runtime_support import instant
    from intrinsics import time_bounds
    register(schemas)
    body = atom['body']; row = atom['definition'].split(':')[-1]
    errors, missing, comparisons, ids, refs = [], [], [], [], []
    selected_binding, outcome, clause_results = None, None, []
    relevance_meaning = None
    def need(role, path): missing.append({'role': role, 'pointer': path})
    def origin(entry, path): return {'inputRole': entry['id'], 'pointer': path}
    def claim(path): return {'inputRole': 'ATOM:' + atom['atomId'], 'pointer': path}
    def compare(code, a, b, source, destination, equal=None, *, depends_on=()):
        equal = same(a, b) if equal is None else equal
        comparisons.append({'predicateId': code, 'equal': equal, 'pointer': destination['pointer'],
            'source': {**source, 'valueDigest': digest(a)}, 'destination': {**destination, 'valueDigest': digest(b)},
            'disposition': 'PASS' if equal else 'FAIL'})
        observe_comparisons([comparisons[-1]], depends_on=depends_on)
        if not equal: errors.append({'code': code, 'pointer': destination['pointer']})
    def result():
        return {'scope': 'CONDITIONAL_DOMAIN_RULE_MEANING_NOT_GOVERNING_RULE_ADMISSION',
            'disposition': 'FAIL' if errors else 'NOT_EVALUATED' if missing else 'PASS',
            'errors': errors, 'remainingRoles': missing, 'comparisons': comparisons,
            'sourceInputIds': sorted(set(ids)), 'requiredReferences': refs,
            'selectedDefinitionBinding': selected_binding, 'conditionalApplicability': outcome,
            'clauseEvaluations': clause_results,
            'selectedRelevanceMeaning': relevance_meaning,
            'qualification': 'Normative domain interpretation only. Governing-rule adoption/applicability, factual crop/use context, source eligibility and referenced identity versions remain separate.'}
    schema = SCHEMAS['ruleMeaning']
    matches = distinct_selected_originals([s for s in sources if 'selectorMapping' in s and predicate_value(s, '', isinstance(s['record'], dict), 'RULE_MEANING_DEFINITION')
        and predicate_value(s, '/schemaVersion', s['record'].get('schemaVersion'), 'RULE_MEANING_DEFINITION') == schema['properties']['schemaVersion']['const']
        and same(predicate_value(s, '/ruleBinding', s['record'].get('ruleBinding'), 'RULE_MEANING_DEFINITION'), body['rule'])])
    definition_selection = observe_selection('RULE_MEANING_DEFINITION', sources, matches,
        origins=[read_origin('ATOM:' + atom['atomId'], '/body/rule')])
    if len(matches) != 1:
        need('INDEPENDENT_RULE_MEANING_DEFINITION', '/body/rule')
        if len(matches) > 1:
            observe_comparisons([{'predicateId': 'AMBIGUOUS_RULE_MEANING_DEFINITION',
                'source': claim('/body/rule'), 'disposition': 'FAIL'}],
                depends_on=[definition_selection] if definition_selection is not None else [])
            errors.append({'code': 'AMBIGUOUS_RULE_MEANING_DEFINITION', 'pointer': '/body/rule'})
        return result()
    entry = matches[0]; definition = entry['record']; ids.append(entry['id']); selected_binding = entry['binding']
    refs.append({'role': 'DOMAIN_RULE_MEANING_DEFINITION', 'binding': entry['binding'], 'pointer': '/body/rule'})
    errors.extend(observed_shape(schemas, schema['$id'], definition))
    if errors: return result()
    identity_mismatch = observed_branch('RULE_DEFINITION_IDENTITY_STOP', definition['definitionId'] != entry['binding']['ref'], origins=[origin(entry, '/definitionId')])
    # The selected read supplies the expected ref; do not invent an original field.
    observe_comparisons([{'predicateId': 'RULE_MEANING_DEFINITION_IDENTITY_MISMATCH',
        'source': origin(entry, '/definitionId'), 'disposition': 'FAIL' if identity_mismatch else 'PASS'}],
        depends_on=guard_refs('RULE_DEFINITION_IDENTITY_STOP'))
    if identity_mismatch:
        errors.append({'code': 'RULE_MEANING_DEFINITION_IDENTITY_MISMATCH', 'pointer': '/definitionId'})
        return result()
    compare('RULE_MEANING_SELECTED_RULE_MISMATCH', definition['ruleBinding'], body['rule'], origin(entry, '/ruleBinding'), claim('/body/rule'))
    need('EXISTING_GOVERNING_RULE_OWNER_SELECTION_AND_APPLICABILITY', '/body/rule')
    if observed_branch('RULE_APPLICABILITY_BRANCH', row == 'C02', origins=[claim('/definition')]):
        rule_controls = guard_refs('RULE_DEFINITION_IDENTITY_STOP', 'RULE_APPLICABILITY_BRANCH')
        duplicate_ids = len({predicate_value(entry, '/applicabilityClauses/' + str(n) + '/clauseId',
            v['clauseId'], 'RULE_CLAUSE_IDENTIFIERS', depends_on=rule_controls)
            for n, v in enumerate(definition['applicabilityClauses'])}) != len(definition['applicabilityClauses'])
        identifier_check = observe_guard('RULE_CLAUSE_IDENTIFIERS', not duplicate_ids,
            origins=[origin(entry, '/applicabilityClauses')], depends_on=rule_controls, predicate_sites=['RULE_CLAUSE_IDENTIFIERS'])
        observe_comparisons([{'predicateId': 'DUPLICATE_RULE_APPLICABILITY_CLAUSE_ID',
            'source': origin(entry, '/applicabilityClauses'),
            'disposition': 'FAIL' if duplicate_ids else 'PASS'}],
            depends_on=[identifier_check] if identifier_check is not None else [])
        if duplicate_ids:
            errors.append({'code': 'DUPLICATE_RULE_APPLICABILITY_CLAUSE_ID', 'pointer': '/applicabilityClauses'})
        start, end = time_bounds(atom['scope']['subjectTime'])
        subject_time = observe_guard('RULE_CLAUSE_SUBJECT_TIME', True,
            origins=[claim('/scope/subjectTime')], depends_on=rule_controls)
        matched, scan_dependencies = [], []
        for n, clause in enumerate(definition['applicabilityClauses']):
            path = '/applicabilityClauses/' + str(n)
            site = 'RULE_CLAUSE_SCAN:' + str(n)
            def value(key):
                return predicate_value(entry, path + '/' + key, clause[key], site, depends_on=rule_controls)
            try:
                lo = instant(value('validFrom')); hi = instant(value('validUntil')) if value('validUntil') is not None else None
                if hi is not None and hi < lo: raise ValueError('Reversed validity interval')
            except (ValueError, TypeError):
                validity = observe_guard(site + ':VALIDITY', False, predicate_sites=[site])
                observe_comparisons([{'predicateId': 'INVALID_RULE_CLAUSE_VALID_TIME',
                    'pointer': path, 'disposition': 'FAIL'}],
                    depends_on=[validity] if validity is not None else [])
                if validity is not None: scan_dependencies.append(validity)
                errors.append({'code': 'INVALID_RULE_CLAUSE_VALID_TIME', 'pointer': path}); continue
            validity = observe_guard(site + ':VALIDITY', True, predicate_sites=[site])
            predicates = {'jurisdiction': value('jurisdiction') == body['jurisdiction'],
                'crop': same(value('cropBinding'), body['crop']), 'use': same(value('useBinding'), body['use']),
                'subjectKind': atom['scope']['subject']['subjectType'] in value('subjectKinds'),
                'timeCoverage': lo <= start and (hi is None or end is not None and end <= hi)}
            clause_match = observe_guard(site + ':MATCH', all(predicates.values()),
                origins=[claim('/body/jurisdiction'), claim('/body/crop'), claim('/body/use'),
                    claim('/scope/subject/subjectType'), claim('/scope/subjectTime')],
                depends_on=[v for v in [validity, subject_time] if v is not None], predicate_sites=[site])
            if clause_match is not None: scan_dependencies.append(clause_match)
            clause_results.append({'clauseId': clause['clauseId'], 'sourceInputId': entry['id'], 'pointer': path,
                                   'predicates': predicates, 'matches': all(predicates.values())})
            if all(predicates.values()): matched.append(n)
        clause_selection = observe_guard('RULE_MATCHING_CLAUSE_UNIQUE', len(matched) == 1,
            origins=[origin(entry, '/applicabilityClauses')], depends_on=rule_controls + scan_dependencies)
        selected_dependencies = [clause_selection] if clause_selection is not None else []
        if len(matched) > 1:
            observe_comparisons([{'predicateId': 'AMBIGUOUS_MATCHING_APPLICABILITY_CLAUSES',
                'pointer': '/applicabilityClauses', 'disposition': 'FAIL'}],
                depends_on=selected_dependencies)
            errors.append({'code': 'AMBIGUOUS_MATCHING_APPLICABILITY_CLAUSES', 'pointer': '/applicabilityClauses'})
        outcome = definition['applicabilityClauses'][matched[0]]['effect'] if len(matched) == 1 else 'INDETERMINATE'
        if len(matched) == 1:
            n = matched[0]; clause = definition['applicabilityClauses'][n]; path = '/applicabilityClauses/' + str(n)
            for source_key, claim_key in [('jurisdiction', 'jurisdiction'), ('cropBinding', 'crop'), ('useBinding', 'use')]:
                compare('RULE_CLAUSE_' + claim_key.upper() + '_MISMATCH', clause[source_key], body[claim_key],
                        origin(entry, path + '/' + source_key), claim('/body/' + claim_key),
                        depends_on=selected_dependencies)
            index = clause['subjectKinds'].index(atom['scope']['subject']['subjectType'])
            compare('RULE_CLAUSE_SUBJECT_KIND_MISMATCH', clause['subjectKinds'][index], atom['scope']['subject']['subjectType'],
                    origin(entry, path + '/subjectKinds/' + str(index)), claim('/scope/subject/subjectType'),
                    depends_on=selected_dependencies)
            # Coverage is a semantic predicate over the two original objects,
            # not lexical equality or a manufactured normalized input record.
            compare('RULE_CLAUSE_TIME_COVERAGE', clause, atom['scope']['subjectTime'],
                    origin(entry, path), claim('/scope/subjectTime'),
                    instant(clause['validFrom']) <= start and (clause['validUntil'] is None
                        or end is not None and end <= instant(clause['validUntil'])),
                    depends_on=selected_dependencies)
            compare('RULE_CLAUSE_ALLEGED_APPLICABILITY_MISMATCH', outcome, body['assertedApplicability'],
                    origin(entry, path + '/effect'), claim('/body/assertedApplicability'),
                    depends_on=selected_dependencies)
        else:
            unknown = body['assertedApplicability'] == 'INDETERMINATE'
            observe_comparisons([{'predicateId': 'NO_UNIQUE_RULE_CLAUSE_CANNOT_ESTABLISH_APPLICABILITY',
                'source': claim('/body/assertedApplicability'),
                'disposition': 'PASS' if unknown else 'FAIL'}], depends_on=selected_dependencies)
            if not unknown:
                errors.append({'code': 'NO_UNIQUE_RULE_CLAUSE_CANNOT_ESTABLISH_APPLICABILITY', 'pointer': '/body/assertedApplicability'})
        need('EXACT_FACTUAL_SUBJECT_CROP_USE_CONTEXT_FOR_RULE', '/body')
        return result()
    roles = [n for n, value in enumerate(definition['relevanceRoles']) if value['role'] == body['relevanceRole']]
    role_mismatch = observed_branch('RULE_RELEVANCE_ROLE_UNIQUE', len(roles) != 1,
        origins=([origin(entry, '/relevanceRoles/' + str(n) + '/role') for n in range(len(definition['relevanceRoles']))]
            or [origin(entry, '/relevanceRoles')])
            + [claim('/body/relevanceRole')],
        depends_on=guard_refs('RULE_DEFINITION_IDENTITY_STOP', 'RULE_APPLICABILITY_BRANCH'))
    observe_comparisons([{'predicateId': 'RULE_RELEVANCE_ROLE_NOT_UNIQUELY_DEFINED',
        'source': claim('/body/relevanceRole'), 'disposition': 'FAIL' if role_mismatch else 'PASS'}],
        depends_on=guard_refs('RULE_RELEVANCE_ROLE_UNIQUE'))
    if role_mismatch:
        errors.append({'code': 'RULE_RELEVANCE_ROLE_NOT_UNIQUELY_DEFINED', 'pointer': '/body/relevanceRole'}); return result()
    role_index = roles[0]; role = definition['relevanceRoles'][role_index]
    compare('RULE_RELEVANCE_ROLE_MISMATCH', role['role'], body['relevanceRole'],
            origin(entry, '/relevanceRoles/' + str(role_index) + '/role'), claim('/body/relevanceRole'),
            depends_on=guard_refs('RULE_RELEVANCE_ROLE_UNIQUE'))
    bases = [s for s in sources if same(s['binding'], body['basis'])]
    observe_selection('RELEVANCE_BASIS', sources, bases, binding=body['basis'],
        origins=[read_origin('ATOM:' + atom['atomId'], '/body/basis'), read_origin(entry['id'], '/relevanceRoles/' + str(role_index) + '/basisKind')],
        guards=guard_refs('RULE_DEFINITION_IDENTITY_STOP', 'RULE_APPLICABILITY_BRANCH', 'RULE_RELEVANCE_ROLE_UNIQUE'))
    if len(bases) != 1:
        need('EXACT_RELEVANCE_BASIS_ORIGINAL', '/body/basis'); return result()
    basis = bases[0]; record = basis['record']; ids.append(basis['id'])
    if observed_branch('RELEVANCE_BASIS_KIND', role['basisKind'] == 'EVENT_ABOUT_SUBJECT', origins=[origin(entry, '/relevanceRoles/' + str(role_index) + '/basisKind')]):
        schema_id, id_field = 'https://ofarm.dev/schema/semanticeventenvelope/v0.1', 'semanticEventId'
    else:
        schema_id, id_field = 'https://ofarm.dev/schema/measurementevidence/v0.1', 'measurementEvidenceId'
    shape = observed_shape(schemas, schema_id, record); errors.extend(shape)
    if shape: return result()
    basis_shape_ready = observe_guard('RELEVANCE_BASIS_SHAPE_READY', True, origins=[origin(basis, '')])
    compare('RELEVANCE_BASIS_IDENTITY_MISMATCH', record[id_field], body['basis']['ref'],
            origin(basis, '/' + id_field), claim('/body/basis/ref'))
    if observed_branch('RELEVANCE_BASIS_KIND', role['basisKind'] == 'EVENT_ABOUT_SUBJECT', origins=[origin(entry, '/relevanceRoles/' + str(role_index) + '/basisKind')]):
        subject = atom['scope']['subject']['subjectRef']
        subject_found = any(predicate_value(basis, '/subjectRefs/' + str(n), value,
            'RELEVANCE_EVENT_SUBJECT_LINK', depends_on=guard_refs('RELEVANCE_BASIS_KIND')) == subject
            for n, value in enumerate(record['subjectRefs']))
        subject_link = observe_guard('RELEVANCE_EVENT_SUBJECT_LINK', subject_found,
            origins=[claim('/scope/subject/subjectRef')] + ([] if record['subjectRefs'] else [origin(basis, '/subjectRefs')]),
            predicate_sites=['RELEVANCE_EVENT_SUBJECT_LINK'],
            depends_on=guard_refs('RELEVANCE_BASIS_KIND'))
        link_check = observe_comparisons([{'predicateId': 'RELEVANCE_EVENT_SUBJECT_LINK_MISSING',
            'source': claim('/scope/subject/subjectRef'), 'disposition': 'PASS' if subject_found else 'FAIL'}],
            depends_on=[subject_link] if subject_link is not None else [])
        if not subject_found:
            errors.append({'code': 'RELEVANCE_EVENT_SUBJECT_LINK_MISSING', 'pointer': '/subjectRefs'})
        else:
            n = record['subjectRefs'].index(subject)
            compare('RELEVANCE_EVENT_SUBJECT_MISMATCH', record['subjectRefs'][n], subject,
                    origin(basis, '/subjectRefs/' + str(n)), claim('/scope/subject/subjectRef'),
                    depends_on=[subject_link] if subject_link is not None else [])
        need('RELEVANCE_EVENT_SUBJECT_KIND_VERSION_AND_ELIGIBLE_USE', '/body/basis')
        meaning_allowed = observe_guard('RELEVANCE_EVENT_MEANING_ALLOWED', not errors,
            depends_on=observe_comparisons(comparisons) + link_check)
        if not errors and observed_branch('RELEVANCE_EVENT_CONCEPT_PRESENT', 'eventConcept' in role,
                origins=[origin(entry, '/relevanceRoles/' + str(role_index) + '/eventConcept')],
                depends_on=[meaning_allowed] if meaning_allowed is not None else []):
            relevance_meaning = {'concept': predicate_value(entry, '/relevanceRoles/' + str(role_index) + '/eventConcept',
                    role['eventConcept'], 'RELEVANCE_EVENT_CONCEPT', depends_on=guard_refs('RELEVANCE_EVENT_CONCEPT_PRESENT')),
                'conceptOrigin': origin(entry, '/relevanceRoles/' + str(role_index) + '/eventConcept'),
                'basisBinding': basis['binding'], 'basisInputId': basis['id'],
                'basisValueDigest': basis['valueDigest'], 'basisRawSha256': basis['rawSha256']}
    else:
        context_candidates = [s for s in sources if 'selectorMapping' in s and predicate_value(s, '', isinstance(s['record'], dict), 'RELEVANCE_SUBJECT_CONTEXT')
            and predicate_value(s, '/schemaVersion', s['record'].get('schemaVersion'), 'RELEVANCE_SUBJECT_CONTEXT') == 'ofarm.agronomicobservationcontext.v0.1'
            and (predicate_value(basis, '/agronomicObservationContextRef', record.get('agronomicObservationContextRef'), 'RELEVANCE_SUBJECT_CONTEXT')
                 == predicate_value(s, '/agronomicObservationContextId', s['record'].get('agronomicObservationContextId'), 'RELEVANCE_SUBJECT_CONTEXT')
                 or predicate_value(basis, '/measurementEvidenceId', record['measurementEvidenceId'], 'RELEVANCE_SUBJECT_CONTEXT')
                 in predicate_value(s, '/measurementEvidenceRefs', s['record'].get('measurementEvidenceRefs', []), 'RELEVANCE_SUBJECT_CONTEXT'))]
        contexts = distinct_selected_originals(context_candidates)
        context_controls = guard_refs('RULE_DEFINITION_IDENTITY_STOP', 'RULE_APPLICABILITY_BRANCH', 'RULE_RELEVANCE_ROLE_UNIQUE', 'RELEVANCE_BASIS_KIND')
        if basis_shape_ready is not None: context_controls.append(basis_shape_ready)
        context_unique = observe_guard('RELEVANCE_CONTEXT_UNIQUE', len(contexts) == 1,
            depends_on=context_controls, predicate_sites=['RELEVANCE_SUBJECT_CONTEXT'])
        if context_unique is not None: context_controls.append(context_unique)
        if len(contexts) != 1:
            context_selection = observe_selection('RELEVANCE_SUBJECT_CONTEXT', sources, contexts, guards=context_controls)
            need('EXACT_RELEVANCE_MEASUREMENT_SUBJECT_CONTEXT', '/body/basis')
            if len(contexts) > 1:
                observe_comparisons([{'predicateId': 'AMBIGUOUS_RELEVANCE_SUBJECT_CONTEXT',
                    'pointer': '/body/basis', 'disposition': 'FAIL'}],
                    depends_on=[context_selection] if context_selection is not None else [])
                errors.append({'code': 'AMBIGUOUS_RELEVANCE_SUBJECT_CONTEXT', 'pointer': '/body/basis'})
            return result()
        def evidence_member(item, site, dependencies, observations):
            consumed = []
            def matches(n, binding):
                consumed.append(read_origin('EFFECT_INTENT', '/evidenceBindings/' + str(n)))
                return same(item['binding'], binding)
            member = any(matches(n, binding) for n, binding in enumerate(evidence_bindings))
            observed = observe_guard(site, member,
                origins=consumed or [read_origin('EFFECT_INTENT', '/evidenceBindings')], depends_on=dependencies)
            if observed is not None: observations.append(observed)
            return member
        preference = []
        context = next((s for n, s in enumerate(context_candidates)
            if evidence_member(s, 'RELEVANCE_CONTEXT_EVIDENCE_PREFERENCE:' + str(n), context_controls, preference)), contexts[0])
        # This is the one acquisition already chosen by the ordinary reader.
        context_selection = observe_selection('RELEVANCE_SUBJECT_CONTEXT', sources, [context], guards=context_controls + preference)
        value = context['record']; ids.append(context['id'])
        refs.append({'role': 'RELEVANCE_SUBJECT_CONTEXT', 'binding': context['binding'], 'pointer': '/body/basis'})
        membership = []
        member = evidence_member(context, 'RELEVANCE_CONTEXT_EVIDENCE_MEMBER',
            [context_selection] if context_selection is not None else [], membership)
        observe_comparisons([{'predicateId': 'RELEVANCE_CONTEXT_NOT_EXACT_EVIDENCE_MEMBER',
            'pointer': '/body/basis', 'disposition': 'PASS' if member else 'FAIL'}], depends_on=membership)
        if not member:
            errors.append({'code': 'RELEVANCE_CONTEXT_NOT_EXACT_EVIDENCE_MEMBER', 'pointer': '/body/basis'})
        shape = observed_shape(schemas, 'https://ofarm.dev/schema/agronomicobservationcontext/v0.1', value); errors.extend(shape)
        if shape: return result()
        identity_mismatch = value['agronomicObservationContextId'] != context['binding']['ref']
        observe_comparisons([{'predicateId': 'RELEVANCE_CONTEXT_IDENTITY_MISMATCH',
            'source': origin(context, '/agronomicObservationContextId'), 'disposition': 'FAIL' if identity_mismatch else 'PASS'}],
            depends_on=[context_selection] if context_selection is not None else [])
        if identity_mismatch:
            errors.append({'code': 'RELEVANCE_CONTEXT_IDENTITY_MISMATCH', 'pointer': '/agronomicObservationContextId'})
        if not observed_branch('RELEVANCE_CONTEXT_TARGET_SCOPE', 'targetScope' in value,
                origins=[origin(context, '/targetScope')]):
            need('RELEVANCE_CONTEXT_TARGET_SCOPE', '/targetScope')
        else:
            for sk, ck in [('scopeType', 'subjectType'), ('scopeRef', 'subjectRef')]:
                compare('RELEVANCE_MEASUREMENT_TARGET_' + sk.upper() + '_MISMATCH', value['targetScope'][sk], atom['scope']['subject'][ck],
                        origin(context, '/targetScope/' + sk), claim('/scope/subject/' + ck),
                        depends_on=guard_refs('RELEVANCE_CONTEXT_TARGET_SCOPE'))
        compare('RELEVANCE_MEASUREMENT_CONTEXT_PROPERTY_MISMATCH', value['observedPropertyRef'], record['observedPropertyRef'],
                origin(context, '/observedPropertyRef'), origin(basis, '/observedPropertyRef'))
        need('RELEVANCE_SUBJECT_IDENTITY_VERSION_EXTENT_AND_ELIGIBLE_USE', '/body/basis')
    return result()
