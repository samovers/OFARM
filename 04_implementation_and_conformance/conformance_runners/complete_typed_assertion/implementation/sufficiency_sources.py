"""C10 comparison of actual sufficiency-case fields under owned meanings.

No ALLOW string, schema-valid graph, or normative mapping admits the case or
its sources. Generic missing-support reasons never identify a specific missing
kind. Reporting an existing outcome does not recompute an owner's decision.
"""
from definition_inputs import SCHEMAS, register
from strict_inputs import same, digest, distinct_selected_originals

CASE_SCHEMA = 'https://ofarm.dev/schema/evidencesufficiencycase/v0.2'
OUTCOME = {'ALLOW': 'SUFFICIENT', 'REFUSE': 'INSUFFICIENT', 'REQUIRE_REVIEW': 'INDETERMINATE'}


from domain_reader_occurrences import reader, selection as observe_selection, guard as observe_guard, origin as read_origin, observed_shape, predicate_value, guard_refs, branch as observed_branch, observe_comparisons


@reader('sufficiency_sources.py', ['AR_BODY'])
def evaluate(atom, sources, schemas, evidence_bindings):
    register(schemas)
    body = atom['body']; errors, missing, comparisons, ids, refs = [], [], [], [], []
    case_binding, selected_definition, outcome = None, None, None
    retained = None
    def need(role, path): missing.append({'role': role, 'pointer': path})
    def original(entry, path): return {'inputRole': entry['id'], 'pointer': path}
    def claimed(path): return {'inputRole': 'ATOM:' + atom['atomId'], 'pointer': path}
    def observe_predicate(code, okay, source, destination=None, *, depends_on=(), predicate_sites=()):
        # Trace existing decisions without changing ordinary comparison results.
        # Containers are real originals; derived sets travel through their reads.
        operands = [source] + ([destination] if destination is not None else [])
        dependencies = list(depends_on)
        if predicate_sites:
            event = observe_guard(code + ':OPERANDS', okay, origins=operands,
                                  depends_on=dependencies, predicate_sites=predicate_sites)
            dependencies = [event] if event is not None else []
        observation = {'predicateId': code, 'source': source,
                       'disposition': 'PASS' if okay else 'FAIL'}
        if destination is not None: observation['destination'] = destination
        return observe_comparisons([observation], depends_on=dependencies) or []
    def compare(code, a, b, source, destination, equal=None, *, depends_on=()):
        okay = same(a, b) if equal is None else equal
        comparisons.append({'predicateId': code, 'equal': okay, 'pointer': destination['pointer'],
            'source': {**source, 'valueDigest': digest(a)}, 'destination': {**destination, 'valueDigest': digest(b)},
            'disposition': 'PASS' if okay else 'FAIL'})
        observe_comparisons([comparisons[-1]], depends_on=depends_on)
        if not okay: errors.append({'code': code, 'pointer': destination['pointer']})
    def result():
        return {'scope': 'REPORTED_SUFFICIENCY_FIELDS_NOT_OWNER_DECISION_OR_ADMISSION',
            'disposition': 'FAIL' if errors else 'NOT_EVALUATED' if missing else 'PASS',
            'errors': errors, 'remainingRoles': missing, 'comparisons': comparisons,
            'sourceInputIds': sorted(set(ids)), 'requiredReferences': refs,
            'selectedCaseBinding': case_binding, 'selectedDefinitionBinding': selected_definition,
            'conditionalReportedOutcome': outcome, 'retainedSourcePosture': retained,
            'qualification': 'Exact selected case graph, evidence projection and reported-outcome interpretation only. Policy version/use, subject/time linkage, source eligibility and the existing owner decision mechanism remain unresolved.'}
    schema = SCHEMAS['evidencePolicyMeaning']
    definitions = distinct_selected_originals([v for v in sources if 'selectorMapping' in v and predicate_value(v, '', isinstance(v['record'], dict), 'EVIDENCE_POLICY_MEANING')
        and predicate_value(v, '/schemaVersion', v['record'].get('schemaVersion'), 'EVIDENCE_POLICY_MEANING') == schema['properties']['schemaVersion']['const']
        and same(predicate_value(v, '/policyBinding', v['record'].get('policyBinding'), 'EVIDENCE_POLICY_MEANING'), body['policy'])])
    definition_selection = observe_selection('EVIDENCE_POLICY_MEANING', sources, definitions,
        origins=[read_origin('ATOM:' + atom['atomId'], '/body/policy')])
    if len(definitions) != 1:
        need('INDEPENDENT_EVIDENCE_POLICY_MEANING', '/body/policy')
        if len(definitions) > 1:
            observe_predicate('AMBIGUOUS_EVIDENCE_POLICY_MEANING', False, claimed('/body/policy'),
                              depends_on=[definition_selection] if definition_selection is not None else [])
            errors.append({'code': 'AMBIGUOUS_EVIDENCE_POLICY_MEANING', 'pointer': '/body/policy'})
        return result()
    entry = definitions[0]; definition = entry['record']; ids.append(entry['id']); selected_definition = entry['binding']
    refs.append({'role': 'DOMAIN_EVIDENCE_POLICY_MEANING', 'binding': entry['binding'], 'pointer': '/body/policy'})
    errors.extend(observed_shape(schemas, schema['$id'], definition))
    if errors: return result()
    if observed_branch('POLICY_MEANING_IDENTITY_STOP', definition['definitionId'] != entry['binding']['ref'], origins=[original(entry, '/definitionId')]):
        observe_predicate('EVIDENCE_POLICY_MEANING_IDENTITY_MISMATCH', False, original(entry, '/definitionId'),
                          depends_on=[definition_selection] if definition_selection is not None else [])
        errors.append({'code': 'EVIDENCE_POLICY_MEANING_IDENTITY_MISMATCH', 'pointer': '/definitionId'}); return result()
    for key, claim_key in [('policyBinding', 'policy'), ('requiredUse', 'requiredUse')]:
        compare('SUFFICIENCY_SELECTED_' + claim_key.upper() + '_MISMATCH', definition[key], body[claim_key],
                original(entry, '/' + key), claimed('/body/' + claim_key))
    case_binding = definition['sufficiencyCaseBinding']
    case_is_cited = any(same(case_binding, b) for b in evidence_bindings)
    observe_predicate('SUFFICIENCY_CASE_NOT_EXACT_EVIDENCE_MEMBER', case_is_cited,
                      original(entry, '/sufficiencyCaseBinding'), read_origin('EFFECT_INTENT', '/evidenceBindings'))
    if not case_is_cited:
        errors.append({'code': 'SUFFICIENCY_CASE_NOT_EXACT_EVIDENCE_MEMBER', 'pointer': '/body/policy'})
    refs.append({'role': 'SELECTED_EVIDENCE_SUFFICIENCY_CASE', 'binding': case_binding, 'pointer': '/body/policy'})
    cases = [v for v in sources if same(v['binding'], case_binding)]
    observe_selection('SUFFICIENCY_CASE', sources, cases, binding=case_binding,
        origins=[read_origin(entry['id'], '/sufficiencyCaseBinding')], guards=guard_refs('POLICY_MEANING_IDENTITY_STOP'))
    if len(cases) != 1:
        need('EXACT_SELECTED_EVIDENCE_SUFFICIENCY_CASE', '/body/policy'); return result()
    case = cases[0]; record = case['record']; ids.append(case['id'])
    errors.extend(observed_shape(schemas, CASE_SCHEMA, record))
    if errors: return result()
    compare('SUFFICIENCY_CASE_IDENTITY_MISMATCH', record['sufficiencyCaseId'], case_binding['ref'],
            original(case, '/sufficiencyCaseId'), original(entry, '/sufficiencyCaseBinding/ref'))
    if record['sufficiencyCaseId'] != case_binding['ref']: return result()
    for key in ['caseClass', 'targetTwin']:
        compare('SUFFICIENCY_SELECTED_' + key.upper() + '_MISMATCH', record[key], definition[key],
                original(case, '/' + key), original(entry, '/' + key))
    policy_is_linked = body['policy']['ref'] in record['governingPolicyRefs']
    observe_predicate('SUFFICIENCY_SELECTED_POLICY_LINK_MISSING', policy_is_linked,
                      claimed('/body/policy/ref'), original(case, '/governingPolicyRefs'))
    if not policy_is_linked:
        errors.append({'code': 'SUFFICIENCY_SELECTED_POLICY_LINK_MISSING', 'pointer': '/governingPolicyRefs'})
    else:
        index = record['governingPolicyRefs'].index(body['policy']['ref'])
        compare('SUFFICIENCY_POLICY_REFERENCE_MISMATCH', record['governingPolicyRefs'][index], body['policy']['ref'],
                original(case, '/governingPolicyRefs/' + str(index)), claimed('/body/policy/ref'))
    claim_ids = [predicate_value(case, '/claims/' + str(n) + '/claimId', v['claimId'], 'SUFFICIENCY_CLAIM_IDS')
                 for n, v in enumerate(record['claims'])]
    argument_ids = [predicate_value(case, '/arguments/' + str(n) + '/argumentId', v['argumentId'], 'SUFFICIENCY_ARGUMENT_IDS')
                    for n, v in enumerate(record['arguments'])]
    bundle_ids = [predicate_value(case, '/evidenceBundles/' + str(n) + '/bundleId', v['bundleId'], 'SUFFICIENCY_BUNDLE_IDS')
                  for n, v in enumerate(record['evidenceBundles'])]
    for label, field, values in [('CLAIM', 'claims', claim_ids), ('ARGUMENT', 'arguments', argument_ids), ('BUNDLE', 'evidenceBundles', bundle_ids)]:
        unique = len(set(values)) == len(values)
        observe_predicate('DUPLICATE_SUFFICIENCY_' + label + '_ID', unique, original(case, '/' + field),
                          predicate_sites=('SUFFICIENCY_' + label + '_IDS',))
        if not unique: errors.append({'code': 'DUPLICATE_SUFFICIENCY_' + label + '_ID', 'pointer': '/' + label.lower()})
    for n, argument in enumerate(record['arguments']):
        for k, claim_id in enumerate(argument['supportsClaimIds']):
            linked = claim_id in claim_ids
            observe_predicate('SUFFICIENCY_ARGUMENT_CLAIM_LINK_MISSING', linked,
                              original(case, '/arguments/' + str(n) + '/supportsClaimIds/' + str(k)),
                              original(case, '/claims'), predicate_sites=('SUFFICIENCY_CLAIM_IDS',))
            if not linked:
                errors.append({'code': 'SUFFICIENCY_ARGUMENT_CLAIM_LINK_MISSING', 'pointer': '/arguments/' + str(n) + '/supportsClaimIds/' + str(k)})
        linked = argument['policyRef'] in record['governingPolicyRefs']
        observe_predicate('SUFFICIENCY_ARGUMENT_POLICY_LINK_MISSING', linked,
                          original(case, '/arguments/' + str(n) + '/policyRef'), original(case, '/governingPolicyRefs'))
        if not linked:
            errors.append({'code': 'SUFFICIENCY_ARGUMENT_POLICY_LINK_MISSING', 'pointer': '/arguments/' + str(n) + '/policyRef'})
    projected = []
    projection_fields = {'RAW_SOURCES': ['rawSourceRefs'], 'NORMALIZED_INTERPRETATIONS': ['normalizedInterpretationRefs'],
                         'ALL_SUPPORT_SOURCES': ['rawSourceRefs', 'normalizedInterpretationRefs', 'provenanceRefs']}[
                             predicate_value(entry, '/evidenceProjection', definition['evidenceProjection'], 'SUFFICIENCY_EVIDENCE_PROJECTION')]
    projection_arrays = []
    for n, bundle in enumerate(record['evidenceBundles']):
        for k, argument_id in enumerate(bundle['supportsArgumentIds']):
            linked = argument_id in argument_ids
            observe_predicate('SUFFICIENCY_BUNDLE_ARGUMENT_LINK_MISSING', linked,
                              original(case, '/evidenceBundles/' + str(n) + '/supportsArgumentIds/' + str(k)),
                              original(case, '/arguments'), predicate_sites=('SUFFICIENCY_ARGUMENT_IDS',))
            if not linked:
                errors.append({'code': 'SUFFICIENCY_BUNDLE_ARGUMENT_LINK_MISSING', 'pointer': '/evidenceBundles/' + str(n) + '/supportsArgumentIds/' + str(k)})
        for field in projection_fields:
            path = '/evidenceBundles/' + str(n) + '/' + field
            projection_arrays.append(original(case, path))
            projected.extend((predicate_value(case, path + '/' + str(k), ref, 'SUFFICIENCY_PROJECTED_REFS'),
                              path + '/' + str(k)) for k, ref in enumerate(bundle[field]))
    claim_refs = [v['ref'] for v in body['evidenceSet']]
    unique = len(set(claim_refs)) == len(claim_refs)
    observe_predicate('AMBIGUOUS_SUFFICIENCY_EVIDENCE_VERSION', unique, claimed('/body/evidenceSet'))
    if not unique:
        errors.append({'code': 'AMBIGUOUS_SUFFICIENCY_EVIDENCE_VERSION', 'pointer': '/body/evidenceSet'})
    matched_projection = set(claim_refs) == {ref for ref, path in projected}
    projection_guard = observe_guard('SUFFICIENCY_PROJECTED_EVIDENCE_SET', matched_projection,
        origins=[claimed('/body/evidenceSet'), original(entry, '/evidenceProjection'), *projection_arrays],
        predicate_sites=('SUFFICIENCY_EVIDENCE_PROJECTION', 'SUFFICIENCY_PROJECTED_REFS'))
    observe_predicate('SUFFICIENCY_EVIDENCE_SET_MISMATCH', matched_projection, claimed('/body/evidenceSet'),
                      original(entry, '/evidenceProjection'),
                      depends_on=[projection_guard] if projection_guard is not None else [])
    if not matched_projection:
        errors.append({'code': 'SUFFICIENCY_EVIDENCE_SET_MISMATCH', 'pointer': '/body/evidenceSet'})
    for n, ref in enumerate(claim_refs):
        found = next((path for value, path in projected if value == ref), None)
        reference_guard = observe_guard('SUFFICIENCY_PROJECTED_REFERENCE:' + str(n), found is not None,
            origins=[claimed('/body/evidenceSet/' + str(n) + '/ref'), original(entry, '/evidenceProjection'), *projection_arrays],
            predicate_sites=('SUFFICIENCY_EVIDENCE_PROJECTION', 'SUFFICIENCY_PROJECTED_REFS'))
        if found is not None:
            compare('SUFFICIENCY_EVIDENCE_REFERENCE_MISMATCH', ref, body['evidenceSet'][n]['ref'],
                    original(case, found), claimed('/body/evidenceSet/' + str(n) + '/ref'),
                    depends_on=[reference_guard] if reference_guard is not None else [])
    mapping = definition['reasonKindMappings']
    unique = len({predicate_value(entry, '/reasonKindMappings/' + str(n) + '/reasonCode', v['reasonCode'],
                                 'SUFFICIENCY_REASON_CODES') for n, v in enumerate(mapping)}) == len(mapping)
    observe_predicate('AMBIGUOUS_SUFFICIENCY_REASON_KIND_MAPPING', unique, original(entry, '/reasonKindMappings'),
                      predicate_sites=('SUFFICIENCY_REASON_CODES',))
    if not unique:
        errors.append({'code': 'AMBIGUOUS_SUFFICIENCY_REASON_KIND_MAPPING', 'pointer': '/reasonKindMappings'})
    reasons = record['outcome'].get('insufficiencyReasonCodes', [])
    mapped = []; reason_guards = []; mapped_guards = []
    for n, reason in enumerate(reasons):
        site = 'SUFFICIENCY_REASON_MAPPING:' + str(n)
        found = [(k, v) for k, v in enumerate(mapping)
                 if predicate_value(entry, '/reasonKindMappings/' + str(k) + '/reasonCode', v['reasonCode'], site) == reason]
        reason_guard = observe_guard(site, len(found) == 1,
            origins=[original(case, '/outcome/insufficiencyReasonCodes/' + str(n)), original(entry, '/reasonKindMappings')],
            predicate_sites=(site,))
        if reason_guard is not None: reason_guards.append(reason_guard)
        if len(found) != 1:
            need('EXACT_SUFFICIENCY_MISSING_KIND_DETAIL:' + reason, '/outcome/insufficiencyReasonCodes/' + str(n))
        else:
            k, value = found[0]
            mapped.append((predicate_value(entry, '/reasonKindMappings/' + str(k) + '/kind', value['kind'],
                'SUFFICIENCY_MAPPED_KINDS', depends_on=[reason_guard] if reason_guard is not None else []), k))
            mapped_guards.append(reason_guard)
            compare('SUFFICIENCY_REASON_CODE_MAPPING_MISMATCH', reason, value['reasonCode'],
                    original(case, '/outcome/insufficiencyReasonCodes/' + str(n)), original(entry, '/reasonKindMappings/' + str(k) + '/reasonCode'),
                    depends_on=[reason_guard] if reason_guard is not None else [])
    known = {kind for kind, k in mapped}; alleged = set(body['missingKinds'])
    kinds_match = not (not known <= alleged or not missing and known != alleged)
    observe_predicate('SUFFICIENCY_MISSING_KINDS_MISMATCH', kinds_match, claimed('/body/missingKinds'),
                      original(case, '/outcome/insufficiencyReasonCodes'), depends_on=reason_guards,
                      predicate_sites=('SUFFICIENCY_MAPPED_KINDS',))
    if not kinds_match:
        errors.append({'code': 'SUFFICIENCY_MISSING_KINDS_MISMATCH', 'pointer': '/body/missingKinds'})
    for (kind, k), reason_guard in zip(mapped, mapped_guards):
        kind_present = kind in body['missingKinds']
        kind_guard = observe_guard('SUFFICIENCY_MAPPED_KIND_PRESENT', kind_present,
            origins=[original(entry, '/reasonKindMappings/' + str(k) + '/kind'), claimed('/body/missingKinds')],
            depends_on=[reason_guard] if reason_guard is not None else [])
        if kind_present:
            n = body['missingKinds'].index(kind)
            compare('SUFFICIENCY_MISSING_KIND_MISMATCH', kind, body['missingKinds'][n],
                    original(entry, '/reasonKindMappings/' + str(k) + '/kind'), claimed('/body/missingKinds/' + str(n)),
                    depends_on=[kind_guard] if kind_guard is not None else [])
    outcome = OUTCOME[record['outcome']['decision']]
    compare('SUFFICIENCY_REPORTED_OUTCOME_MISMATCH', record['outcome']['decision'], body['allegedOutcome'],
            original(case, '/outcome/decision'), claimed('/body/allegedOutcome'), outcome == body['allegedOutcome'])
    retained = {'outcome': record['outcome'], 'evidenceBundles': record['evidenceBundles'],
                'subject': record['subject'], 'anchorScopes': record['anchorScopes']}
    need('EXISTING_SUFFICIENCY_OWNER_DECISION_AND_ELIGIBLE_USE', '/body/policy')
    need('EXACT_SUFFICIENCY_POLICY_ARGUMENT_REVISION_AND_REQUIRED_USE', '/governingPolicyRefs')
    need('EXACT_SUFFICIENCY_SUBJECT_SCOPE_TIME_AND_EVIDENCE_VERSION_LINKS', '/subject')
    return result()
