"""Conservative #47 construction graph for known original and claim occurrences.

Selection membership, typed claim references, proposition positions and
independently selected action copy facts are derived without inspecting an
offered #51 requiredReads list.
This module intentionally stops before
recursive source-rule expansion, read/guard expectations and semantic admission.
It cannot emit a complete immutableInputClosure or a passing domain verdict.
"""

from collections import deque
from pathlib import Path
import sys

from duty_graph import PREREQUISITES, validate_graph
from nested_source_occurrences import derive as derive_nested_source_occurrences
from original_inputs import bind_roots
sys.path.insert(0, str(Path(__file__).resolve().parent / 'outer'))
from domain_mapping import BRANCHES, copy_facts
from reference_roles import collect as collect_typed_references, citation_membership_checks
from strict_inputs import canonical, digest, parse, sha, pointer, InputError


SEPARATE_SOURCE_RESPONSIBILITIES = (
    'SAMPLE_ENDPOINT_IDENTITY',
    'SAMPLE_EVIDENCE_ELIGIBILITY',
    'PHYSICAL_SAMPLE_CUSTODY',
    'GEOMETRY_ACCEPTANCE',
    'SAMPLING_REPRESENTATIVENESS',
    'PROTECTED_ORIGINAL_STORAGE',
)


# These links name existing candidate duty slots, not a source-owner decision or
# a finding outcome. Unlisted roles have no established finding attribution.
TYPED_ROLE_FINDINGS = {
    'ASSERTION_SUBJECT': ('AR_SUBJECT',),
    'AUTHORITY_SCOPE': ('AR_SCOPE',),
    'SUBJECT_SCOPE_RELATION_PROOF': ('AR_SUBJECT_SCOPE_PROOF',),
    'ASSERTION_ACT_EVIDENCE': ('AR_ASSERTION_ACT_EVIDENCE',),
    'ASSERTION_EVIDENCE': ('AR_EVIDENCE',),
    'SEMANTIC_EVENT': ('AR_EVENT_ASSOCIATION',),
    'PERFORMER_IDENTITY': ('AR_OPERATION_PERFORMER',),
    'SOFTWARE_AGENT_ACTORSHIP': ('AR_OPERATION_AGENT_ACTORSHIP',),
    'PERFORMER_AUTHORITY_EVIDENCE': ('AR_OPERATION_PERFORMER_AUTHORITY',),
    'INTERVENTION_INTENT_PAYLOAD': ('AR_OPERATION_PAYLOADS',),
    'EXECUTION_RECORD_PAYLOAD': ('AR_OPERATION_PAYLOADS',),
    'RULE_REVISION': ('AR_COMPLIANCE_RULES',),
    'EVIDENCE_POLICY_REVISION': ('AR_COMPLIANCE_EVIDENCE_POLICY',),
    'PRIOR_ASSERTION': ('AR_CORRECTION_LINEAGE',),
    'CONTEXT_IDENTITY': ('AR_BODY',),
    'CONTEXT_RELATIONSHIP_PROOF': ('AR_BODY',),
    'ATOM_SUBJECT': ('AR_BODY',),
    'ATOM_EXTENT': ('AR_BODY',),
    'DEFINITION_OR_CONTEXT_INPUT': ('AR_BODY',),
}


# Exact predicate IDs in the pinned pure domain copy module. Each tuple names
# finding slots, source original (None means selected-action constant) and
# destination original. New predicates must be reviewed instead of inherited
# by a prefix guess. A finding slot can receive both a copy fact and distinct
# typed source-use occurrences.
COPY_FACT_ATTRIBUTION = {
    'intent.schemaVersion': (('AR_ACTION_PROFILE', 'PC_ACTION_TYPE'), None, 'effectIntent'),
    'result.schemaVersion': (('AR_SCHEMA', 'PC_ACTION_TYPE'), None, 'proposedAssertion'),
    'intent.effectKind': (('AR_EFFECT_SUBJECT', 'PC_ACTION_TYPE'), None, 'effectIntent'),
    'intent.effectPosture': (('AR_EFFECT_SUBJECT', 'PC_ACTION_TYPE'), None, 'effectIntent'),
    'result.assertionType': (('AR_TYPE', 'PC_ACTION_TYPE'), None, 'proposedAssertion'),
    'result.pending': (('AR_CLAIM_STATE', 'PC_PENDING_REVIEW'), None, 'proposedAssertion'),
    'mapping.id': (('AR_EFFECT_SUBJECT', 'AR_ID'), 'effectIntent', 'proposedAssertion'),
    'mapping.scope': (('AR_SCOPE',), 'effectIntent', 'proposedAssertion'),
    'mapping.subject': (('AR_SUBJECT',), 'effectIntent', 'proposedAssertion'),
    'mapping.assertedAt': (('AR_ASSERTED_AT',), 'effectIntent', 'proposedAssertion'),
    'mapping.assertionActPosture': (('AR_ASSERTION_ACT_POSTURE',), 'effectIntent', 'proposedAssertion'),
    'mapping.subjectTime': (('AR_SUBJECT_TIME',), 'effectIntent', 'proposedAssertion'),
    'mapping.assertionBody': (('AR_BODY',), 'effectIntent', 'proposedAssertion'),
    'mapping.evidenceBindings': (('AR_EVIDENCE',), 'effectIntent', 'proposedAssertion'),
    'mapping.assertionActEvidenceBinding': (('AR_ASSERTION_ACT_EVIDENCE',), 'effectIntent', 'proposedAssertion'),
    'mapping.subjectScopeProofBindings': (('AR_SUBJECT_SCOPE_PROOF',), 'effectIntent', 'proposedAssertion'),
    'mapping.supersedesAssertionRecordBinding': (('AR_CORRECTION_LINEAGE',), 'effectIntent', 'proposedAssertion'),
    'mapping.claimPosture': (('AR_OPERATION_POSTURE',), 'effectIntent', 'proposedAssertion'),
    'mapping.performedByPartyRef': (('AR_OPERATION_PERFORMER',), 'effectIntent', 'proposedAssertion'),
    'mapping.softwareAgentActorshipBindings': (('AR_OPERATION_AGENT_ACTORSHIP',), 'effectIntent', 'proposedAssertion'),
    'mapping.performerAuthorityEvidenceBindings': (('AR_OPERATION_PERFORMER_AUTHORITY',), 'effectIntent', 'proposedAssertion'),
    'body.performerRef': (('AR_OPERATION_PERFORMER',), 'effectIntent', 'effectIntent'),
    'mapping.ruleRevisionBindings': (('AR_COMPLIANCE_RULES',), 'effectIntent', 'proposedAssertion'),
    'mapping.evidencePolicyRevisionBindings': (('AR_COMPLIANCE_EVIDENCE_POLICY',), 'effectIntent', 'proposedAssertion'),
    'body.applicability': (('AR_SUBJECT_TIME',), 'effectIntent', 'effectIntent'),
}

def bind_copy_operands(fact, action):
    """Locate both value digests in the original documents used by copy_facts."""
    _, source, destination = COPY_FACT_ATTRIBUTION[fact['predicateId']]
    roles = {'effectIntent': 'EFFECT_INTENT', 'proposedAssertion': 'PROPOSED_RESULT', None: 'DOMAIN_CONTRACT'}
    result = dict(fact, disposition='PASS' if fact['equal'] else 'FAIL')
    for side, root in (('source', source), ('destination', destination)):
        if fact[side + 'Present']:
            path = (fact[side + 'Pointer'] if root is not None else
                    '/actions/' + action + '/predicateConstants/' + fact['predicateId'])
            result[side] = {'inputRole': roles[root], 'pointer': path, 'valueDigest': fact[side + 'ValueDigest']}
    return result


COPY_COMMON_PREDICATES = (
    'intent.schemaVersion', 'result.schemaVersion', 'intent.effectKind',
    'intent.effectPosture', 'result.assertionType', 'result.pending',
    'mapping.id', 'mapping.scope', 'mapping.subject', 'mapping.assertedAt',
    'mapping.assertionActPosture', 'mapping.subjectTime', 'mapping.assertionBody',
    'mapping.evidenceBindings', 'mapping.assertionActEvidenceBinding',
    'mapping.subjectScopeProofBindings', 'mapping.supersedesAssertionRecordBinding',
)
COPY_ACTION_PREDICATES = {
    'ASSERT_STRUCTURE': ('body.applicability',),
    'ASSERT_OPERATION_CLAIM': (
        'mapping.claimPosture', 'mapping.performedByPartyRef',
        'mapping.softwareAgentActorshipBindings',
        'mapping.performerAuthorityEvidenceBindings', 'body.performerRef'),
    'ASSERT_COMPLIANCE': (
        'mapping.ruleRevisionBindings', 'mapping.evidencePolicyRevisionBindings',
        'body.applicability'),
}


def _input_outcome(result):
    status = result['status']
    if status == 'MATCHED':
        return 'PASS'
    if status == 'MISMATCH':
        return 'FAIL'
    return 'NOT_EVALUATED'


def _reference_selection(reference, by_ref, inventory_results):
    binding = reference.get('binding')
    if (not isinstance(binding, dict)
            or set(binding) not in ({'ref', 'digest'}, {'ref', 'revisionRef'})
            or not isinstance(binding.get('ref'), str) or not binding['ref']
            or not all(isinstance(value, str) and value for value in binding.values())):
        return None, 'FAIL', 'CLAIM_REFERENCE_BINDING_MALFORMED'
    pin = by_ref.get(binding['ref'])
    if pin is None:
        return None, 'FAIL', 'CLAIM_REFERENCE_NOT_IN_INDEPENDENT_SELECTION'
    iid = pin['inputId']
    result = inventory_results[iid]
    if result['status'] == 'MISMATCH':
        return iid, 'FAIL', 'CLAIM_REFERENCE_SELECTED_ORIGINAL_MISMATCH'
    if result['status'] == 'NOT_EVALUATED':
        return iid, 'NOT_EVALUATED', 'CLAIM_REFERENCE_ORIGINAL_UNAVAILABLE'
    if pin['digestMode'] == 'RAW_BYTES':
        return iid, 'NOT_EVALUATED', 'RAW_SOURCE_USE_RULE_PENDING'
    if pin['digestMode'] != 'JCS_JSON':
        return iid, 'FAIL', 'UNKNOWN_SELECTED_ORIGINAL_MODE'
    # A typed source's digest may use its owner's source-specific rule (for
    # example a self-digest exclusion), not the storage whole-JCS digest.
    # Only a selected source contract may decide their relationship.
    if 'digest' in binding and binding['digest'] != pin['wholeJcsDigest']:
        return iid, 'NOT_EVALUATED', 'SOURCE_DIGEST_RULE_PENDING'
    if 'revisionRef' in binding:
        return iid, 'NOT_EVALUATED', 'CLAIM_REFERENCE_REVISION_RESOLUTION_PENDING'
    return iid, 'PASS', 'EXACT_SELECTED_JSON_VALUE_ONLY'


def _source_selection(selected, by_ref, inventory_results):
    """Compare one independent source nomination with its selected original.

    A source digest or revision can have owner-specific meaning. Equality of
    exact raw and whole-value pins is structural only, never admission for use.
    """
    pin = by_ref.get(selected['binding']['ref'])
    if pin is None:
        return None, 'NOT_EVALUATED', 'SOURCE_ORIGINAL_MAPPING_PENDING'
    iid = pin['inputId']
    if selected['rawSha256'] != pin['rawSha256']:
        return iid, 'FAIL', 'SOURCE_ORIGINAL_RAW_PIN_CONFLICT'
    # The retained v0.1 sourceSelections collection is JSON-only. A selected
    # RAW_BYTES original needs the separate v0.4 original/use trace, even when
    # its ref and raw pin happen to match this legacy nomination.
    if pin['digestMode'] == 'RAW_BYTES':
        return iid, 'FAIL', 'LEGACY_JSON_SOURCE_SELECTION_RAW_CONFLICT'
    if pin['digestMode'] == 'JCS_JSON' and selected['valueDigest'] != pin['wholeJcsDigest']:
        return iid, 'FAIL', 'SOURCE_ORIGINAL_VALUE_PIN_CONFLICT'
    result = inventory_results[iid]
    if result['status'] == 'MISMATCH':
        return iid, 'FAIL', 'SOURCE_SELECTED_ORIGINAL_MISMATCH'
    if result['status'] == 'NOT_EVALUATED':
        return iid, 'NOT_EVALUATED', 'SOURCE_SELECTED_ORIGINAL_UNAVAILABLE'
    binding = selected['binding']
    if 'digest' in binding and binding['digest'] != selected['valueDigest']:
        return iid, 'NOT_EVALUATED', 'SOURCE_DIGEST_RULE_PENDING'
    if 'revisionRef' in binding:
        return iid, 'NOT_EVALUATED', 'SOURCE_REVISION_RESOLUTION_PENDING'
    return iid, 'PASS', 'EXACT_SELECTED_SOURCE_VALUE_ONLY'


def _known_rule_fixed_point(selection, bound, requirements, typed_expansion_available,
                            nested_expansion):
    """Exhaust the one established expansion rule without claiming closure.

    Only selected originals discharged by an explicit candidate rule enter the
    expanded set. Unrecognized selected sources stay on the frontier even when
    their bytes match and a nomination names them.
    """
    roots = [finding['inputId'] for finding in bound['roots'].values()
             if finding['inputId'] is not None]
    roots.extend(item['inputId'] for item in nested_expansion['selectedEventUseRoots'])
    queue = deque(dict.fromkeys(roots))
    reached, expanded = [], []
    seen = set()
    intent = bound['roots']['effectIntent']
    nested_expanded = set(nested_expansion['expandedInputIds'])
    while queue:
        iid = queue.popleft()
        if iid in seen:
            continue
        seen.add(iid)
        reached.append(iid)
        if (iid == intent['inputId'] and intent['disposition'] == 'PASS'
                and typed_expansion_available):
            expanded.append(iid)
            for requirement in requirements:
                if requirement['id'].startswith('typed-reference:'):
                    queue.extend(requirement['inputIds'])
        elif iid in nested_expanded:
            expanded.append(iid)
            for requirement in requirements:
                if (requirement.get('kind') == 'CANDIDATE_NESTED_SOURCE_OCCURRENCE'
                        and requirement['origin']['inputRole'] == iid):
                    queue.extend(requirement['inputIds'])
    return {'status': 'PARTIAL', 'reachedInputIds': reached,
            'expandedInputIds': expanded,
            'frontierInputIds': [iid for iid in reached if iid not in expanded],
            'unclassifiedSelectedInputIds': [pin['inputId'] for pin in selection['originalSelections']
                                             if pin['inputId'] not in seen],
            'expansionRulesApplied': (['EFFECT_INTENT_TYPED_REFERENCE_ROLES']
                                      if intent['inputId'] in expanded else [])
                                     + (['EXACT_SELECTED_WORK_SAMPLE_EVENT_FIELDS']
                                        if nested_expanded else []),
            'qualification': 'Fixed point of explicit candidate structural edges only; unexpanded owner source rules remain on the frontier.'}


def _derive_copy_facts(bound, selected_action, requirements, uses):
    """Retain exact original-to-original candidate copy facts when roots permit.

    The action must come from the independent package, never owner state. A
    copy PASS is only field equality under the pinned pure candidate rule.
    """
    if selected_action is None:
        return {'status': 'NOT_EVALUATED', 'reason': 'INDEPENDENT_PACKAGE_ACTION_NOT_SUPPLIED'}
    if selected_action not in BRANCHES:
        raise ValueError('Unknown independent selected action for copy attribution.')
    if set(COPY_FACT_ATTRIBUTION) != (set(COPY_COMMON_PREDICATES)
                                      | {pid for extra in COPY_ACTION_PREDICATES.values()
                                         for pid in extra}):
        raise ValueError('Candidate copy-fact attribution table is incomplete.')
    expected = COPY_COMMON_PREDICATES + COPY_ACTION_PREDICATES[selected_action]
    roots = bound['roots']
    blocked_roots = [name for name in ('effectIntent', 'proposedAssertion')
                     if roots[name]['disposition'] != 'PASS']
    facts = []
    if not blocked_roots:
        intent = bound['admittedJson'][roots['effectIntent']['inputId']]
        result = bound['admittedJson'][roots['proposedAssertion']['inputId']]
        facts = copy_facts(intent, result, selected_action)
        if [fact['predicateId'] for fact in facts] != list(expected):
            raise ValueError('Pinned candidate copy rule set differs from its attributed predicate IDs.')
    failed = []
    for index, predicate in enumerate(expected):
        fact = facts[index] if facts else None
        finding_ids, source_root, destination_root = COPY_FACT_ATTRIBUTION[predicate]
        input_ids, root_dependencies, observations = [], [], []
        for side, name in (('SOURCE', source_root), ('DESTINATION', destination_root)):
            if fact is not None:
                pointer = fact['sourcePointer' if side == 'SOURCE' else 'destinationPointer']
                present = fact['sourcePresent' if side == 'SOURCE' else 'destinationPresent']
                value_digest = fact.get('sourceValueDigest' if side == 'SOURCE'
                                        else 'destinationValueDigest')
                input_role = {'effectIntent': 'EFFECT_INTENT',
                              'proposedAssertion': 'PROPOSED_ASSERTION'}.get(
                                  name, 'SELECTED_ACTION_RULE_CONSTANT')
                observation = {'side': side, 'inputRole': input_role, 'pointer': pointer,
                               'present': present}
                if value_digest is not None:
                    observation['valueDigest'] = value_digest
            if name is not None:
                iid = roots[name]['inputId']
                if fact is not None:
                    observation['inputId'] = iid
                if iid is not None and iid not in input_ids:
                    input_ids.append(iid)
                dependency = 'root:' + name
                if dependency not in root_dependencies:
                    root_dependencies.append(dependency)
                if iid is not None:
                    uses.append({'id': 'copy-use:' + str(index) + ':' + side.lower(),
                                 'requirementId': 'copy-fact:' + predicate,
                                 'inputId': iid, 'classification': 'CANDIDATE_COPY_' + side
                                                   if fact is not None else 'CANDIDATE_COPY_' + side + '_PENDING'})
            if fact is not None:
                observations.append(observation)
        if fact is not None and not fact['equal']:
            failed.append(predicate)
        requirements.append({'id': 'copy-fact:' + predicate, 'kind': 'CANDIDATE_COPY_FACT',
                             'role': 'ORIGINAL_TO_ORIGINAL_COPY_PREDICATE',
                             'origin': {'inputRole': 'CANDIDATE_COPY_RULE',
                                        'pointer': '/copyFactRules/' + str(index)},
                             'rule': {'module': 'outer/domain_mapping.py',
                                      'function': 'copy_facts', 'predicateId': predicate,
                                      'selectedAction': selected_action},
                             'findingIds': list(finding_ids),
                             'inputIds': input_ids, 'dependsOn': root_dependencies,
                             'observations': observations,
                             'disposition': 'NOT_EVALUATED' if fact is None else
                                            'PASS' if fact['equal'] else 'FAIL',
                             'diagnostics': [{'code': 'SELECTED_COPY_ROOT_UNAVAILABLE'}]
                                            if fact is None else [] if fact['equal'] else [
                                 {'code': 'CANDIDATE_COPY_PREDICATE_MISMATCH',
                                  'predicateId': predicate}],
                             'qualification': 'Pure selected-action copy equality only; no source admission, owner check or complete finding result.'})
    return {'status': 'PARTIAL', 'selectedAction': selected_action,
            'knownPredicateIds': list(expected), 'blockedRootNames': blocked_roots,
            'independentFailurePredicateIds': failed,
            'qualification': 'Candidate copy predicates retained from the package action; field observations require both exact selected original roots, and complete source/use rules remain open.'}


def _derive_proposition_occurrences(bound, selected_action, requirements, uses):
    """Retain every checked-intent proposition position and exact local row pin.

    This is structural accounting over one admitted original, not an atom
    predicate, source-use decision or three-valued proposition evaluation.
    """
    intent_root = bound['roots']['effectIntent']
    if intent_root['disposition'] != 'PASS':
        return {'status': 'NOT_EVALUATED', 'reason': 'EXACT_SELECTED_INTENT_ROOT_UNAVAILABLE',
                'knownOccurrenceCount': 0}
    raw_definitions = (Path(__file__).resolve().parent / 'domain-definitions.json').read_bytes()
    definitions = parse(raw_definitions)['definitions']
    by_ref = {}
    for index, row in enumerate(definitions):
        ref = row['definitionRef']
        if ref in by_ref:
            raise ValueError('Candidate domain definition refs are not unique.')
        by_ref[ref] = (index, row)
    if len(definitions) != 99 or len({row['id'] for row in definitions}) != 99:
        raise ValueError('Candidate definition registry does not retain its 99 distinct rows.')
    iid = intent_root['inputId']
    intent = bound['admittedJson'][iid]
    body = intent.get('assertionBody')
    proposition = body.get('proposition') if isinstance(body, dict) else None
    if not isinstance(proposition, dict):
        return {'status': 'PARTIAL', 'selectedAction': selected_action,
                'definitionRegistryRawSha256': sha(raw_definitions),
                'knownOccurrenceCount': 0,
                'diagnostics': [{'code': 'PROPOSITION_ORIGINAL_SHAPE_UNAVAILABLE',
                                 'pointer': '/assertionBody/proposition'}],
                'qualification': 'The matched original has no traversable proposition object; other root and copy facts remain independent.'}
    start = len(requirements)
    atom_ids = {}
    def append(role, path, *, parent=None, disposition='NOT_EVALUATED', diagnostics=None,
               details=None):
        index = len(requirements) - start
        rid = 'proposition-occurrence:' + str(index)
        requirements.append({'id': rid, 'kind': 'CANDIDATE_PROPOSITION_OCCURRENCE',
                             'role': role, 'origin': {'inputRole': 'EFFECT_INTENT',
                                                      'pointer': path},
                             'findingIds': ['AR_BODY'], 'inputIds': [iid],
                             'dependsOn': ['root:effectIntent'],
                             **({'parentRequirementId': parent} if parent else {}),
                             **(details or {}),
                             'disposition': disposition,
                             'diagnostics': diagnostics or [],
                             'qualification': 'Exact proposition occurrence/definition selection only; semantic source use remains open.'})
        uses.append({'id': 'proposition-use:' + str(index), 'requirementId': rid,
                     'inputId': iid, 'classification': 'PROPOSITION_OCCURRENCE_ONLY'})
        return requirements[-1]
    def walk(node, path, parent=None):
        if not isinstance(node, dict) or not isinstance(node.get('form'), str):
            append('MALFORMED_PROPOSITION_NODE', path, parent=parent,
                   disposition='FAIL', diagnostics=[{'code': 'MALFORMED_PROPOSITION_NODE'}])
            return
        form = node['form']
        row = append('PROPOSITION_' + form, path, parent=parent,
                     details={'form': form})
        rid = row['id']
        if form == 'ATOM':
            atom_id = node.get('atomId')
            ref = node.get('definition')
            row['atomId'] = atom_id
            row['definitionRef'] = ref
            if not isinstance(atom_id, str) or not atom_id:
                row['disposition'] = 'FAIL'
                row['diagnostics'].append({'code': 'ATOM_ID_MALFORMED'})
            else:
                atom_ids.setdefault(atom_id, []).append(row)
            selected = by_ref.get(ref) if isinstance(ref, str) else None
            if selected is None:
                row['disposition'] = 'FAIL'
                row['diagnostics'].append({'code': 'ATOM_EXACT_DEFINITION_REF_NOT_SELECTED'})
                return
            index, definition = selected
            row['definitionPointer'] = '/definitions/' + str(index)
            row['definitionRowId'] = definition['id']
            row['definitionAction'] = definition['sourceDefinition'].get('action')
            if row['definitionAction'] is None:
                row['disposition'] = 'FAIL'
                row['diagnostics'].append({'code': 'ATOM_DEFINITION_NOT_ACTION_ROW'})
            elif selected_action is None:
                row['diagnostics'].append({'code': 'INDEPENDENT_PACKAGE_ACTION_PENDING'})
            elif row['definitionAction'] != selected_action:
                row['disposition'] = 'FAIL'
                row['diagnostics'].append({'code': 'ATOM_DEFINITION_ACTION_MISMATCH'})
            elif row['disposition'] != 'FAIL':
                row['disposition'] = 'PASS'
            return
        if form in ('NOT', 'QUALIFIED'):
            if form == 'QUALIFIED':
                if 'qualifiers' in node:
                    append('DECLARED_QUALIFICATION', path + '/qualifiers', parent=rid,
                           details={'selectedValueDigest': digest(node['qualifiers']),
                                    'appliesToAtomId': node.get('appliesToAtomId')})
                else:
                    row['disposition'] = 'FAIL'
                    row['diagnostics'].append({'code': 'QUALIFICATION_VALUE_MISSING'})
            if 'child' not in node:
                row['disposition'] = 'FAIL'
                row['diagnostics'].append({'code': 'PROPOSITION_CHILD_MISSING'})
                return
            walk(node['child'], path + '/child', rid)
            return
        if form in ('ALL', 'ANY', 'SEQUENCE'):
            children = node.get('children')
            if not isinstance(children, list) or not children:
                row['disposition'] = 'FAIL'
                row['diagnostics'].append({'code': 'PROPOSITION_CHILDREN_MISSING'})
                return
            for index, child in enumerate(children):
                walk(child, path + '/children/' + str(index), rid)
            if form == 'SEQUENCE':
                relations = node.get('orderRelations')
                if not isinstance(relations, list):
                    row['disposition'] = 'FAIL'
                    row['diagnostics'].append({'code': 'SEQUENCE_ORDER_RELATIONS_MALFORMED'})
                else:
                    for index, relation in enumerate(relations):
                        valid = (isinstance(relation, dict)
                                 and isinstance(relation.get('beforeAtomId'), str)
                                 and isinstance(relation.get('afterAtomId'), str))
                        append('DECLARED_ORDER_RELATION', path + '/orderRelations/' + str(index),
                               parent=rid, disposition='NOT_EVALUATED' if valid else 'FAIL',
                               diagnostics=[] if valid else [{'code': 'ORDER_RELATION_SHAPE_MALFORMED'}],
                               details={'selectedValueDigest': digest(relation),
                                        'beforeAtomId': relation.get('beforeAtomId')
                                        if isinstance(relation, dict) else None,
                                        'afterAtomId': relation.get('afterAtomId')
                                        if isinstance(relation, dict) else None})
            return
        row['disposition'] = 'FAIL'
        row['diagnostics'].append({'code': 'UNKNOWN_PROPOSITION_FORM'})
    walk(proposition, '/assertionBody/proposition')
    for repeated in atom_ids.values():
        if len(repeated) > 1:
            for row in repeated:
                row['disposition'] = 'FAIL'
                row['diagnostics'].append({'code': 'DUPLICATE_ATOM_ID'})
    rows = requirements[start:]
    return {'status': 'PARTIAL', 'selectedAction': selected_action,
            'definitionRegistryRawSha256': sha(raw_definitions),
            'knownOccurrenceCount': len(rows),
            'independentFailureRequirementIds': [row['id'] for row in rows
                                                 if row['disposition'] == 'FAIL'],
            'qualification': 'Each exact proposition position is retained. Local definition/action checks do not prove atom meaning, source use, or complete closure.'}


def _collect_claim_source_occurrences(references, intent_root, by_ref, results,
                                      source_lookup, requirements, uses):
    """Retain each declared claim source position before offered state reads.

    The candidate role table exposes an exact claim field rule. A matched
    original pin identifies the candidate source bytes, but owner selector,
    eligible use, revision and protected treatment remain unresolved here.
    """
    if references is None:
        return {'status': 'NOT_EVALUATED', 'reason': 'EXACT_SELECTED_INTENT_ROOT_UNAVAILABLE',
                'knownOccurrenceCount': 0, 'occurrences': []}
    rule_raw_sha = sha((Path(__file__).resolve().parent / 'reference_roles.py').read_bytes())
    definition_raw_sha = sha((Path(__file__).resolve().parent / 'domain-definitions.json').read_bytes())
    atom_rows = {row['origin']['pointer']: row for row in requirements
                 if row.get('kind') == 'CANDIDATE_PROPOSITION_OCCURRENCE'
                 and row['role'] == 'PROPOSITION_ATOM'}
    occurrences = []
    for index, reference in enumerate(references):
        iid, structural, reason = _reference_selection(reference, by_ref, results)
        linked = source_lookup.get(canonical(reference['binding']), [])
        if any(requirement['disposition'] == 'FAIL' for _, requirement in linked):
            structural, reason = 'FAIL', 'INDEPENDENT_SOURCE_SELECTION_CONFLICT'
        rule = dict(reference['candidateRule'])
        rule['moduleRawSha256'] = rule_raw_sha
        depends_on = ['root:effectIntent'] + [requirement['id'] for _, requirement in linked]
        diagnostics = [{'code': reason}]
        atom_pointer = rule.get('atomPointer')
        if atom_pointer is not None:
            atom = atom_rows.get(atom_pointer)
            if atom is None or atom.get('definitionRef') != rule['definitionRef']:
                structural = 'FAIL'
                diagnostics.append({'code': 'ATOM_SOURCE_RULE_ORIGIN_MISMATCH'})
            else:
                depends_on.append(atom['id'])
                if 'definitionPointer' in atom:
                    rule['candidateDefinitionPointer'] = atom['definitionPointer']
                    rule['candidateDefinitionRegistryRawSha256'] = definition_raw_sha
                # A failing atom definition is a separate AR_BODY failure.
                # Its dependency remains explicit; this source-use row does
                # not recast that semantic failure as an input-custody FAIL.
        disposition = 'FAIL' if structural == 'FAIL' else 'NOT_EVALUATED'
        rid = 'typed-reference:' + str(index)
        requirement = {'id': rid, 'kind': 'CANDIDATE_CLAIM_SOURCE_OCCURRENCE',
                       'role': reference['role'],
                       'origin': {'inputRole': 'EFFECT_INTENT',
                                  'pointer': reference['pointer']},
                       'rule': rule, 'selectedBinding': reference['binding'],
                       'inputIds': [iid] if iid is not None else [],
                       'dependsOn': depends_on,
                       'disposition': disposition,
                       'structuralSelection': structural,
                       'diagnostics': diagnostics,
                       'qualification': 'One exact claim field use. The candidate rule does not establish owner selection, admission, revision or protected treatment.'}
        requirements.append(requirement)
        use_id = None
        if iid is not None:
            use_id = 'typed-reference-use:' + str(index)
            uses.append({'id': use_id, 'requirementId': rid, 'inputId': iid,
                         'classification': 'OWNER_SOURCE_USE_AND_TREATMENT_PENDING',
                         'ownerSelectorsStatus': 'NOT_EVALUATED',
                         'treatment': {'kind': 'NOT_EVALUATED',
                                       'reason': 'OWNER_SOURCE_USE_RULE_PENDING'}})
        binding_ref = reference['binding'].get('ref') if isinstance(reference['binding'], dict) else None
        pin = by_ref.get(binding_ref)
        occurrences.append({'requirementId': rid, 'useId': use_id,
                            'origin': requirement['origin'], 'rule': rule,
                            'role': reference['role'],
                            'selectedBinding': reference['binding'],
                            'selectedInputId': iid,
                            'selectedOriginal': ({'ref': pin['ref'],
                                                  'digestMode': pin['digestMode'],
                                                  'rawSha256': pin['rawSha256'],
                                                  'byteLength': pin['byteLength'],
                                                  'inventoryStatus': results[iid]['status']}
                                                 if pin is not None else None),
                            'dependsOn': depends_on, 'disposition': disposition})
    return {'status': 'PARTIAL', 'knownOccurrenceCount': len(occurrences),
            'occurrences': occurrences,
            'unresolved': ['RECURSIVE_OWNER_SOURCE_USE_RULES',
                           'OWNER_SELECTOR_AND_ADMISSION',
                           'PROTECTED_READ_AND_GUARD_TREATMENT'],
            'qualification': 'Each direct claim source position is independent of offered requiredReads; nested owner-declared source uses remain open.'}


NESTED_EDGE_CLASSES = frozenset({'REQUIRED_ORIGINAL_READ', 'COMPARISON_VALUE',
                                 'CONDITIONAL', 'SOURCE_SHAPE', 'SELECTION_GUARD'})
TYPED_OCCURRENCE_KINDS = frozenset({
    'CANDIDATE_NESTED_SOURCE_OCCURRENCE', 'CANDIDATE_DOMAIN_READER_OCCURRENCE',
    'CANDIDATE_OWNER_INPUT_OCCURRENCE', 'CANDIDATE_OWNER_CONTROL_OCCURRENCE',
    'CANDIDATE_OWNER_INVOCATION_GUARD', 'CANDIDATE_LOCAL_FINDING_OCCURRENCE'})


def record_local_predicate(graph, bound, duty, predicate, outcome, operands, *,
                           selected_action, edge_class='COMPARISON_VALUE',
                           controls=None, additional_dependencies=(), rule=None):
    """Record fields consumed by an already evaluated local predicate.

    Call sites supply exact paths, never a new condition or caller verdict.
    Schema validation may consume a complete root. Other predicates name their
    actual fields. Derived owner/rendering controls remain separate from these
    original observations; absence requires a matched original ancestor.
    """
    if duty not in PREREQUISITES or edge_class not in {'COMPARISON_VALUE', 'SOURCE_SHAPE', 'CONDITIONAL', 'SELECTION_GUARD'}:
        raise ValueError('Unknown local finding predicate role.')
    observations, issues, ids, dependencies = [], [], [], list(additional_dependencies)
    indexes = {pin['inputId']: n for n, pin in enumerate(bound['selection']['originalSelections'])}
    for operand in operands:
        path = operand['pointer']
        if 'root' in operand:
            root = bound['roots'][operand['root']]
            dependencies.append('root:' + operand['root'])
            iid = root['inputId'] if root['disposition'] == 'PASS' else None
        else:
            iid = operand.get('inputId')
        if iid not in bound['admittedJson']:
            issues.append({'code': 'LOCAL_PREDICATE_ORIGINAL_UNAVAILABLE',
                           'root': operand.get('root'), 'inputId': iid, 'pointer': path})
            continue
        original = bound['admittedJson'][iid]
        present = True
        try:
            value = pointer(original, path)
        except (InputError, ValueError, KeyError, TypeError, IndexError):
            present = False
        observation = {'inputRole': iid, 'pointer': path, 'present': present}
        if 'present' in operand and present != operand['present']:
            issues.append({'code': 'LOCAL_PREDICATE_OPERAND_PRESENCE_MISMATCH', 'inputId': iid, 'pointer': path})
        if present:
            observation['valueDigest'] = digest(value)
        else:
            ancestor = path
            while ancestor:
                ancestor = ancestor.rsplit('/', 1)[0]
                try:
                    value = pointer(original, ancestor)
                    break
                except (InputError, ValueError, KeyError, TypeError, IndexError):
                    continue
            else:
                value = original
            observation['absentAncestor'] = {'pointer': ancestor, 'valueDigest': digest(value)}
        if 'valueDigest' in operand:
            observation['annotatedValueDigest'] = operand['valueDigest']
            observation['annotationMatchesOriginal'] = present and digest(value) == operand['valueDigest']
            if not observation['annotationMatchesOriginal']:
                issues.append({'code': 'LOCAL_PREDICATE_OPERAND_MISMATCH', 'inputId': iid, 'pointer': path})
        observations.append(observation)
        ids.append(iid)
        dependencies.append('selected-original:' + str(indexes[iid]))
    rid = 'local-finding:' + str(sum(row.get('kind') == 'CANDIDATE_LOCAL_FINDING_OCCURRENCE'
                                   for row in graph['requirements']))
    row = {'id': rid, 'kind': 'CANDIDATE_LOCAL_FINDING_OCCURRENCE',
           'role': predicate, 'edgeClass': edge_class, 'findingIds': [duty],
           'origin': ({'inputRole': observations[0]['inputRole'], 'pointer': observations[0]['pointer']}
                      if observations else {'inputRole': 'CANDIDATE_LOCAL_RULE'}),
           'inputIds': list(dict.fromkeys(ids)), 'dependsOn': list(dict.fromkeys(dependencies)),
           'observations': observations, 'actualLocalOutcome': bool(outcome),
           'disposition': 'NOT_EVALUATED' if issues else 'PASS' if outcome or edge_class == 'SELECTION_GUARD' else 'FAIL',
           'diagnostics': issues,
           'rule': rule or {'module': 'verify_domain.py', 'moduleRawSha256': sha((Path(__file__).parent / 'verify_domain.py').read_bytes()),
                    'predicate': predicate, 'selectedAction': selected_action,
                    'constants': 'PINNED_READER_RULE_NOT_ORIGINAL_INPUT'},
           'qualification': 'Actual local predicate operands only; no storage use, source adoption or completion claim.'}
    if controls is not None:
        row['derivedControls'] = controls
    graph['requirements'].append(row)
    graph['derivation']['knownRequirementCount'] = len(graph['requirements'])
    if row['disposition'] == 'FAIL':
        graph['localDisposition'] = 'FAIL'
    return row


def materialize_local_observations(graph, bound, observations, *, selected_action):
    """Bind queued actual call-site observations to independently selected bytes.

    Queues are internal observations of the already executed local evaluator,
    never caller verdicts. Owner reports and selected controls stay derived;
    only exact matched byte arguments or selected roots become original operands.
    """
    linked = {}
    base = Path(__file__).resolve().parent
    manifest = parse((base / 'candidate-manifest.json').read_bytes())
    members = {member['path']: member for member in manifest['members']}
    for event in observations:
        if event['id'] in linked or any(
                duty not in PREREQUISITES for duty in event['findingIds']):
            raise ValueError('Invalid local observation identity or finding role.')
        operands, dependencies, issues = [], [], []
        for item in event.get('operands', []):
            operand = dict(item)
            if 'owner' in operand:
                owner = operand.pop('owner')
                candidates = [row for row in graph['requirements']
                    if row.get('kind') == 'CANDIDATE_OWNER_INPUT_OCCURRENCE'
                    and row['origin']['invocationId'] == owner
                    and row['origin']['argumentPath'] == operand['argumentPath']]
                operand.pop('argumentPath')
                match = candidates[0] if len(candidates) == 1 else None
                operand['inputId'] = (match['inputIds'][0] if match is not None
                    and match['disposition'] == 'PASS' and len(match['inputIds']) == 1 else None)
                if match is not None:
                    dependencies.append(match['id'])
            operands.append(operand)
        for prior in event.get('dependsOn', []):
            if prior in linked:
                dependencies.append(linked[prior])
            else:
                issues.append({'code': 'LOCAL_OBSERVATION_DEPENDENCY_UNAVAILABLE', 'eventId': prior})
        invocation = event.get('ownerInvocationId')
        if invocation is not None:
            guards = [row['id'] for row in graph['requirements']
                if row.get('kind') == 'CANDIDATE_OWNER_INVOCATION_GUARD'
                and row['origin']['invocationId'] == invocation]
            dependencies.extend(guards)
            if len(guards) != 1:
                issues.append({'code': 'LOCAL_OBSERVATION_OWNER_INVOCATION_UNAVAILABLE', 'invocationId': invocation})
            if (event.get('controls') or {}).get('kind') == 'RECOMPUTED_OWNER_REPORT_CONTROL':
                dependencies.extend(row['id'] for row in graph['requirements']
                    if row.get('kind') in {'CANDIDATE_OWNER_INPUT_OCCURRENCE', 'CANDIDATE_OWNER_CONTROL_OCCURRENCE'}
                    and row.get('origin', {}).get('invocationId') == invocation)
        rules = []
        for supplied in event.get('ruleOperands', []):
            checked = dict(supplied)
            try:
                path = (base / supplied['localPath']).resolve()
                if not path.is_relative_to(base):
                    raise ValueError('Rule path outside candidate.')
                raw = path.read_bytes()
                member = members.get(supplied['localPath'])
                okay = (member is not None and member['rawSha256'] == supplied['rawSha256']
                        and sha(raw) == supplied['rawSha256'] and len(raw) == member['byteLength'])
                if 'pointer' in supplied:
                    okay = okay and digest(pointer(parse(raw), supplied['pointer'])) == supplied['valueDigest']
                checked['matchesPinnedRule'] = okay
            except (OSError, ValueError, KeyError, TypeError, IndexError):
                checked['matchesPinnedRule'] = False
            if not checked['matchesPinnedRule']:
                issues.append({'code': 'LOCAL_OBSERVATION_RULE_OPERAND_MISMATCH', 'localPath': supplied.get('localPath')})
            rules.append(checked)
        rule = event.get('rule')
        if rule is not None:
            rule = dict(rule)
            try:
                path = (base / rule['module']).resolve()
                module_ok = path.is_relative_to(base) and sha(path.read_bytes()) == rule['moduleRawSha256']
            except (OSError, ValueError, KeyError, TypeError):
                module_ok = False
            rule['matchesObservedModuleBytes'] = module_ok
            rule['selectedManifestModuleMatch'] = (rule.get('module') in members and
                members[rule['module']]['rawSha256'] == rule.get('moduleRawSha256'))
            rule['kind'] = 'EXACT_READER_MODULE_BYTES_PACKAGE_PREFLIGHT_SEPARATE'
            if not module_ok:
                issues.append({'code': 'LOCAL_OBSERVATION_RULE_MODULE_MISMATCH', 'module': rule.get('module')})
        before_disposition = graph.get('localDisposition')
        # A selection-set control can have no direct duty. Its consumers attach
        # exact dependencies after their real source reads are known.
        row = record_local_predicate(graph, bound, event['findingIds'][0] if event['findingIds'] else 'AR_BODY',
            event['predicate'], event['outcome'], operands, selected_action=selected_action,
            edge_class=event.get('edgeClass', 'COMPARISON_VALUE'), controls=event.get('controls'),
            additional_dependencies=dependencies, rule=rule)
        row['findingIds'] = list(event['findingIds'])
        row['observedEventId'] = event['id']
        if rules:
            row['ruleObservations'] = rules
        if issues:
            row['diagnostics'].extend(issues)
            row['disposition'] = 'NOT_EVALUATED'
            if before_disposition is None:
                graph.pop('localDisposition', None)
            else:
                graph['localDisposition'] = before_disposition
        linked[event['id']] = row['id']
    return linked


def _derive_citation_comparisons(bound, references, requirements):
    root = bound['roots']['effectIntent']
    if root['disposition'] != 'PASS' or references is None:
        return
    iid = root['inputId']
    intent = bound['admittedJson'][iid]
    if not isinstance(intent, dict) or not isinstance(intent.get('evidenceBindings'), list):
        # A malformed root has no original evidence-array operand. Its shape
        # diagnostic remains separate; never substitute an empty array.
        return
    typed = {row['origin']['pointer']: row['id'] for row in requirements
             if row.get('kind') == 'CANDIDATE_CLAIM_SOURCE_OCCURRENCE'}
    rule_sha = sha((Path(__file__).resolve().parent / 'reference_roles.py').read_bytes())
    for index, check in enumerate(citation_membership_checks(references, intent['evidenceBindings'])):
        # Membership uses two values in the intent, not the cited record's
        # availability or immutable bytes. Do not depend on its read outcome.
        pointer = check['pointer']
        findings = ['AR_EVIDENCE']
        if pointer.startswith('/assertionBody/'):
            findings.append('AR_BODY')
        requirements.append({
            'id': 'citation-comparison:' + str(index), 'kind': 'CANDIDATE_CITATION_COMPARISON',
            'role': 'CITATION_EXACT_EVIDENCE_MEMBERSHIP', 'edgeClass': 'COMPARISON_VALUE',
            'origin': {'inputRole': iid, 'pointer': pointer},
            'rule': {'module': 'reference_roles.py', 'moduleRawSha256': rule_sha,
                     'rule': 'citation_membership_checks'},
            'findingIds': findings, 'inputIds': [iid], 'dependsOn': ['root:effectIntent'],
            'sourceOccurrenceRequirementId': typed.get(pointer),
            'observations': [
                {'inputRole': iid, 'pointer': pointer, 'valueDigest': digest(check['binding'])},
                {'inputRole': iid, 'pointer': '/evidenceBindings',
                 'valueDigest': digest(intent['evidenceBindings'])}],
            'equal': check['equal'], 'disposition': 'PASS' if check['equal'] else 'FAIL',
            'diagnostics': [] if check['equal'] else [{'code': 'CITATION_NOT_EXACT_EVIDENCE_MEMBER'}],
            'qualification': 'Original-backed citation membership only; source-use eligibility and original immutability remain separate.'})


def _is_immutable_input_diagnostic(item):
    return item['code'] not in {'TYPED_CLAIM_REFERENCE_DERIVATION_BLOCKED',
                                'CITATION_NOT_EXACT_EVIDENCE_MEMBER'}


def _nested_edge_class(row):
    edge_class = row.get('edgeClass')
    if edge_class not in NESTED_EDGE_CLASSES:
        raise ValueError('Nested source occurrence lacks a recognized edge class: '
                         + row['id'])
    return edge_class


def _is_immutable_input_requirement(row):
    kind = row.get('kind')
    if kind in {'CANDIDATE_COPY_FACT', 'CANDIDATE_PROPOSITION_OCCURRENCE',
                'CANDIDATE_CITATION_COMPARISON'}:
        return False
    if kind in TYPED_OCCURRENCE_KINDS:
        return _nested_edge_class(row) == 'REQUIRED_ORIGINAL_READ'
    return True


def _known_finding_attribution(requirements, uses, *, finding_results=None):
    """Attribute known occurrences, without claiming full findingLinks closure.

    The candidate 49-duty graph gives the denominator of possible finding IDs.
    Exact checked-intent roles supply only direct links named below. Requirement
    dependencies supply the known transitive portion, including selected source
    nominations and original membership. No offered finding or state read list
    may define these links or their completeness.
    """
    # Match the actual report array order, not dictionary insertion order in
    # the prerequisite graph. These are candidate construction pointers only.
    duties = parse((Path(__file__).resolve().parent / 'outer/source-duties.json').read_bytes())['duties']
    finding_ids = [duty['id'] for duty in duties]
    validate_graph(finding_ids)
    pointers = {}
    mapping_index, post_index = 0, 0
    for finding_id in finding_ids:
        if finding_id.startswith('AR_'):
            pointers[finding_id] = '/mappingFindings/' + str(mapping_index)
            mapping_index += 1
        elif finding_id.startswith('PC_'):
            pointers[finding_id] = '/postconditionFindings/' + str(post_index)
            post_index += 1
        else:
            raise ValueError('Unknown source duty prefix: ' + finding_id)
    if mapping_index != 29 or post_index != 20:
        raise ValueError('Candidate finding pointer count differs from the source duty record.')
    by_id = {row['id']: row for row in requirements}
    if len(by_id) != len(requirements):
        raise ValueError('Duplicate known requirement IDs prevent finding attribution.')
    direct = {finding_id: [] for finding_id in finding_ids}
    unattributed_typed = []
    for row in requirements:
        rid = row['id']
        if row.get('kind') in {'CANDIDATE_COPY_FACT', 'CANDIDATE_PROPOSITION_OCCURRENCE',
                              'CANDIDATE_CITATION_COMPARISON'}:
            for finding_id in row['findingIds']:
                if finding_id not in direct:
                    raise ValueError('Copy fact cites unknown candidate finding: ' + finding_id)
                direct[finding_id].append(rid)
            continue
        if row.get('kind') in TYPED_OCCURRENCE_KINDS:
            # A selected source can contain comparison values and conditional
            # selectors which do not establish another required original read.
            # Keep their domain finding path without treating them as input
            # custody obligations.
            if _nested_edge_class(row) == 'REQUIRED_ORIGINAL_READ':
                direct['PC_INPUTS_IMMUTABLE'].append(rid)
            for finding_id in row['findingIds']:
                if finding_id not in direct:
                    raise ValueError('Nested source cites unknown candidate finding: ' + finding_id)
                if rid not in direct[finding_id]:
                    direct[finding_id].append(rid)
            continue
        # Selected original, root, source nomination and direct typed source
        # occurrences are independently known input membership obligations.
        direct['PC_INPUTS_IMMUTABLE'].append(rid)
        if not rid.startswith('typed-reference:'):
            continue
        role = row['role']
        finding_roles = list(TYPED_ROLE_FINDINGS.get(role, ()))
        pointer = row['origin']['pointer']
        if pointer.startswith('/assertionBody/proposition/') and 'AR_BODY' not in finding_roles:
            finding_roles.append('AR_BODY')
        if not finding_roles:
            unattributed_typed.append(rid)
        for finding_id in finding_roles:
            direct[finding_id].append(rid)

    closure_cache = {}
    visiting = set()
    def ancestors(rid):
        if rid in closure_cache:
            return closure_cache[rid]
        if rid in visiting:
            raise ValueError('Cyclic known requirement dependency: ' + rid)
        if rid not in by_id:
            raise ValueError('Unknown known requirement dependency: ' + rid)
        visiting.add(rid)
        reached = []
        for parent in by_id[rid]['dependsOn']:
            for member in ancestors(parent):
                if member not in reached:
                    reached.append(member)
        reached.append(rid)
        visiting.remove(rid)
        closure_cache[rid] = reached
        return reached

    actual_findings = None
    if finding_results is not None:
        actual_findings = {row['id']: row for row in finding_results}
        if (len(actual_findings) != len(finding_results)
                or set(actual_findings) != set(finding_ids)
                or any(row.get('disposition') not in {'PASS', 'FAIL', 'NOT_EVALUATED', 'NOT_APPLICABLE'}
                       for row in finding_results)):
            raise ValueError('Finding prerequisite attribution requires the exact 49 actual finding results.')
    duty_cache, duty_visiting = {}, set()
    def duty_requirements(finding_id):
        if finding_id in duty_cache:
            return duty_cache[finding_id]
        if finding_id in duty_visiting:
            raise ValueError('Cyclic actual finding prerequisite: ' + finding_id)
        duty_visiting.add(finding_id)
        actual = actual_findings[finding_id] if actual_findings is not None else None
        inapplicable = actual is not None and actual['disposition'] == 'NOT_APPLICABLE'
        local_failure = actual is not None and bool(actual.get('diagnostics'))
        active_direct = [] if inapplicable else direct[finding_id]
        reached = []
        for rid in active_direct:
            for member in ancestors(rid):
                if member not in reached:
                    reached.append(member)
        traversed, owner_prerequisites = [], []
        if actual is not None and not inapplicable and not local_failure:
            for prerequisite in PREREQUISITES[finding_id]:
                if prerequisite not in PREREQUISITES:
                    owner_prerequisites.append(prerequisite)
                    continue
                traversed.append(prerequisite)
                for member in duty_requirements(prerequisite)['requirements']:
                    if member not in reached:
                        reached.append(member)
        mode = ('AWAITING_ACTUAL_FINDINGS' if actual is None else 'NOT_APPLICABLE'
                if inapplicable else 'LOCAL_FAILURE_PRECEDENCE' if local_failure
                else 'ACTUAL_PREREQUISITES_EVALUATED')
        value = {'requirements': reached, 'direct': active_direct,
                 'dutyPrerequisites': traversed, 'ownerPrerequisites': owner_prerequisites,
                 'mode': mode}
        duty_visiting.remove(finding_id); duty_cache[finding_id] = value
        return value

    links = []
    for finding_id in finding_ids:
        duty = duty_requirements(finding_id)
        reached = duty['requirements']
        reached_set = set(reached)
        links.append({'findingId': finding_id, 'findingPointer': pointers[finding_id],
                      'status': 'PARTIAL',
                      'directRequirementIds': duty['direct'],
                      'prerequisiteTraversal': duty['mode'],
                      'directDutyPrerequisiteIds': duty['dutyPrerequisites'],
                      'directOwnerPrerequisiteIds': duty['ownerPrerequisites'],
                      'inapplicableRequirementIds': (direct[finding_id]
                                                     if duty['mode'] == 'NOT_APPLICABLE' else []),
                      'knownTransitiveRequirementIds': reached,
                      'knownUseIds': [use['id'] for use in uses
                                      if use['requirementId'] in reached_set],
                      'independentFailRequirementIds': [rid for rid in reached
                                                        if by_id[rid]['disposition'] == 'FAIL'
                                                        and (finding_id != 'PC_INPUTS_IMMUTABLE'
                                                             or _is_immutable_input_requirement(by_id[rid]))]})
    return {'status': 'PARTIAL', 'candidateFindingCount': len(finding_ids),
            'links': links,
            'dutyPrerequisiteCoverage': ('ACTUAL_FINDING_EVALUATION_PATHS' if actual_findings is not None
                                         else 'AWAITING_ACTUAL_FINDINGS'),
            'findingIdsWithoutKnownDirectLinks': [link['findingId'] for link in links
                                                 if not link['directRequirementIds']],
            'typedReferenceIdsWithoutSpecificFindingLink': unattributed_typed,
            'provenance': ['CANDIDATE_49_DUTY_GRAPH', 'CHECKED_INTENT_TYPED_REFERENCE_ROLES',
                           'PINNED_SELECTION_ORIGINAL_MEMBERSHIP']
                          + (['MATCHED_ORIGINAL_CANDIDATE_COPY_FACTS']
                             if any(row.get('kind') == 'CANDIDATE_COPY_FACT' and row.get('observations')
                                    for row in requirements)
                             else []),
            'unresolved': ['SOURCE_SPECIFIC_FINDING_RULES', 'SELECTED_ACTION_APPLICABILITY',
                           'COMPLETE_OWNER_INPUT_OCCURRENCES', 'PROTECTED_READ_AND_GUARD_KEYS',
                           'ALL_AND_ONLY_FINDING_LINKS'],
            'qualification': 'Known requirement and actual evaluated duty-prerequisite links only. Uncollected reader and owner inputs still prevent complete findingLinks; no domain PASS or owner admission follows.'}


def refresh_known_finding_attribution(graph, finding_results=None):
    """Refresh after actual reader/owner rows and public findings are available."""
    graph['knownFindingAttribution'] = _known_finding_attribution(
        graph['requirements'], graph['uses'], finding_results=finding_results)
    return graph['knownFindingAttribution']


def derive(selection_bytes, checked_inventory, original_intent_bytes,
           original_result_bytes, *, selected_state_context=None, selected_action=None,
           original_bytes=None):
    """Return a partial graph and exact root findings for one selected claim.

    The caller must use the guarded inventory result and actual selected #51
    context after its owner invocation. `selected_action`, when supplied, must
    be the independently selected package action, never owner state.
    `reference_roles.collect` is a local
    structural declaration over the admitted intent, not an evidence-use rule.
    It runs here so a caller cannot offer a shortened reference list.
    """
    bound = bind_roots(selection_bytes, checked_inventory, original_intent_bytes,
                       original_result_bytes, selected_state_context=selected_state_context,
                       original_bytes=original_bytes)
    selection = bound['selection']
    by_ref = bound['pinsByRef']
    results = bound['inventoryResults']
    pin_indexes = {pin['inputId']: index
                   for index, pin in enumerate(selection['originalSelections'])}
    requirements, uses, diagnostics = [], [], []
    for index, pin in enumerate(selection['originalSelections']):
        iid = pin['inputId']
        outcome = _input_outcome(results[iid])
        rid = 'selected-original:' + str(index)
        requirements.append({'id': rid, 'role': 'SELECTED_ORIGINAL_MEMBERSHIP',
                             'origin': {'inputRole': 'PINNED_EVALUATION_SELECTION',
                                        'pointer': '/originalSelections/' + str(index)},
                             'inputIds': [iid], 'dependsOn': [], 'disposition': outcome,
                             'qualification': 'Original pin/inventory result only.'})
        uses.append({'id': 'membership-use:' + str(index), 'requirementId': rid,
                     'inputId': iid, 'classification': 'ROLE_NOT_YET_DERIVED'})
    root_input_ids = []
    for name, finding in bound['roots'].items():
        iid = finding['inputId']
        if iid is not None and iid not in root_input_ids:
            root_input_ids.append(iid)
        index = pin_indexes.get(iid)
        requirements.append({'id': 'root:' + name, 'role': name.upper(),
                             'origin': {'inputRole': 'PINNED_EVALUATION_SELECTION'
                                        if name != 'proposedAssertion' else 'SELECTED_STATE_CONTEXT',
                                        'pointer': {'effectIntent': '/effectIntent',
                                                    'authorizationResult': '/authorizationResult',
                                                    'currentActionRule': '/currentActionRuleBinding',
                                                    'proposedAssertion': '/proposedAssertion'}[name]},
                             'inputIds': [iid] if iid is not None else [],
                             'dependsOn': ['selected-original:' + str(index)] if index is not None else [],
                             'disposition': finding['disposition'],
                             'diagnostics': finding['diagnostics'],
                             'qualification': 'Exact root binding only; owner/source use remains separate.'})
        if iid is not None:
            uses.append({'id': 'root-use:' + name, 'requirementId': 'root:' + name,
                         'inputId': iid,
                         'classification': 'PROPOSED_ASSERTION' if name == 'proposedAssertion'
                         else 'ROOT_CONTROL'})
    source_lookup = {}
    for index, selected in enumerate(selection.get('sourceSelections', [])):
        iid, structural, reason = _source_selection(selected, by_ref, results)
        rid = 'selected-source:' + str(index)
        pin_index = pin_indexes.get(iid)
        requirement = {'id': rid, 'role': 'INDEPENDENT_SOURCE_SELECTION',
                       'origin': {'inputRole': 'PINNED_EVALUATION_SELECTION',
                                  'pointer': '/sourceSelections/' + str(index)},
                       'selectedBinding': selected['binding'],
                       'inputIds': [iid] if iid is not None else [],
                       'dependsOn': ['selected-original:' + str(pin_index)]
                       if pin_index is not None else [],
                       'disposition': structural, 'diagnostics': [{'code': reason}],
                       'qualification': 'Exact source nomination and original pins only; digest rule, revision and admission remain separate.'}
        requirements.append(requirement)
        source_lookup.setdefault(canonical(selected['binding']), []).append((selected, requirement))
        if iid is not None:
            uses.append({'id': 'selected-source-use:' + str(index), 'requirementId': rid,
                         'inputId': iid, 'classification': 'INDEPENDENT_SOURCE_MAPPING_ONLY'})
    for linked in source_lookup.values():
        if len({(selected['rawSha256'], selected['valueDigest'])
                for selected, _ in linked}) > 1:
            for _, requirement in linked:
                requirement['disposition'] = 'FAIL'
                requirement['diagnostics'].append({'code': 'CONFLICTING_SOURCE_SELECTIONS'})
    # Proposition positions establish the exact atom/definition dependency
    # before direct source occurrences are collected from the admitted claim.
    proposition_expansion = _derive_proposition_occurrences(bound, selected_action,
                                                              requirements, uses)
    intent_root = bound['roots']['effectIntent']
    typed_expansion_available = False
    references = None
    if intent_root['disposition'] == 'PASS':
        intent = bound['admittedJson'][intent_root['inputId']]
        try:
            collected = collect_typed_references(intent)
            typed_expansion_available = True
        except (AttributeError, KeyError, TypeError, ValueError, IndexError) as exc:
            collected = {'references': [], 'errors': [
                {'code': 'TYPED_REFERENCE_DERIVATION_ERROR',
                 'detail': str(exc)[:400]}]}
        claim_shape_errors = {'TYPED_REFERENCE_DERIVATION_ERROR',
                              'MALFORMED_ATOM_DEFINITION_REF',
                              'UNKNOWN_ATOM_DEFINITION_ROW',
                              'MALFORMED_TYPED_SOURCE_BINDING',
                              'MALFORMED_TEMPORAL_SOURCE_BINDING',
                              'MALFORMED_TEMPORAL_BASIS'}
        for issue in collected['errors']:
            if issue['code'] in claim_shape_errors:
                diagnostics.append({'code': 'TYPED_CLAIM_REFERENCE_DERIVATION_BLOCKED',
                                    'reason': issue['code'],
                                    **({'pointer': issue['pointer']}
                                       if 'pointer' in issue else {})})
                typed_expansion_available = False
            else:
                diagnostics.append(issue)
        references = collected['references']
    else:
        diagnostics.append({'code': 'TYPED_CLAIM_REFERENCE_DERIVATION_BLOCKED',
                            'detail': 'The exact selected intent original is unavailable or mismatched.'})
    source_expansion = _collect_claim_source_occurrences(
        references, intent_root, by_ref, results, source_lookup, requirements, uses)
    _derive_citation_comparisons(bound, references, requirements)
    nested_expansion = derive_nested_source_occurrences(bound, requirements, uses)
    for event_root in nested_expansion['selectedEventUseRoots']:
        if event_root['inputId'] not in root_input_ids:
            root_input_ids.append(event_root['inputId'])
    copy_expansion = _derive_copy_facts(bound, selected_action, requirements, uses)
    blocked = [pin['inputId'] for pin in selection['originalSelections']
               if results[pin['inputId']]['status'] != 'MATCHED']
    for finding in bound['roots'].values():
        if (finding['inputId'] is not None and finding['disposition'] != 'PASS'
                and finding['inputId'] not in blocked):
            blocked.append(finding['inputId'])
    for requirement in requirements:
        if (requirement['id'].startswith('selected-source:')
                and requirement['disposition'] == 'FAIL'):
            for iid in requirement['inputIds']:
                if iid not in blocked:
                    blocked.append(iid)
    fixed_point = _known_rule_fixed_point(selection, bound, requirements,
                                          typed_expansion_available, nested_expansion)
    attribution = _known_finding_attribution(requirements, uses)
    input_fail = (any(_is_immutable_input_diagnostic(d) for d in diagnostics)
                  or any(r['disposition'] == 'FAIL' and _is_immutable_input_requirement(r)
                         for r in requirements))
    nested_domain_fail = any((r.get('kind') in TYPED_OCCURRENCE_KINDS
                             or r.get('kind') == 'CANDIDATE_CITATION_COMPARISON')
                             and r.get('edgeClass') in {'SOURCE_SHAPE', 'COMPARISON_VALUE', 'CONDITIONAL', 'SELECTION_GUARD'}
                             and r['disposition'] == 'FAIL' for r in requirements)
    copy_rows = [r for r in requirements if r.get('kind') == 'CANDIDATE_COPY_FACT']
    copy_fail = any(r['disposition'] == 'FAIL' for r in copy_rows)
    proposition_rows = [r for r in requirements
                        if r.get('kind') == 'CANDIDATE_PROPOSITION_OCCURRENCE']
    proposition_fail = any(r['disposition'] == 'FAIL' for r in proposition_rows)
    copy_disposition = ('FAIL' if copy_fail else
                        'PASS' if copy_rows and all(r['disposition'] == 'PASS' for r in copy_rows)
                        else 'NOT_EVALUATED')
    return {'schemaVersion': 'candidate.partialOriginalRequirementGraph.v0.1',
            'scope': 'CONSTRUCTION_ONLY_NOT_IMMUTABLE_INPUT_CLOSURE',
            'derivation': {'status': 'PARTIAL', 'knownRequirementCount': len(requirements),
                           'knownRootInputIds': root_input_ids, 'blockedInputIds': blocked,
                           'unresolvedRoles': ['RECURSIVE_DEFINITION_AND_SOURCE_RULES',
                                               'COMPLETE_OWNER_INPUT_OCCURRENCES',
                                               'PROTECTED_READ_NEGATIVE_SET_WRITE_EXPECTATIONS',
                                               'COMPLETE_FINDING_TRANSITIVE_LINKS']},
            'rootBindings': bound['roots'], 'knownRuleFixedPoint': fixed_point,
            'knownPropositionExpansion': proposition_expansion,
            'knownSourceOccurrenceExpansion': source_expansion,
            'knownNestedSourceOccurrenceExpansion': nested_expansion,
            'knownCopyFactExpansion': copy_expansion,
            'knownFindingAttribution': attribution,
            'requirements': requirements,
            'uses': uses, 'diagnostics': diagnostics,
            'originalInputDisposition': 'FAIL' if input_fail else 'NOT_EVALUATED',
            'knownPropositionDisposition': 'FAIL' if proposition_fail else 'NOT_EVALUATED',
            'knownCopyFactDisposition': copy_disposition,
            'localDisposition': ('FAIL' if input_fail or nested_domain_fail or copy_fail
                                 or proposition_fail else 'NOT_EVALUATED'),
            'separateResponsibilitiesNotEvaluatedHere': list(SEPARATE_SOURCE_RESPONSIBILITIES),
            'qualification': 'Known membership, typed and selected nested source uses, proposition and selected-action copy occurrences only. No full closure, source admission, domain PASS or runtime protection.'}
