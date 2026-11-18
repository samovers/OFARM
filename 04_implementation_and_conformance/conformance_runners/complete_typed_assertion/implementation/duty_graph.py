"""Explicit candidate prerequisites; independent copy failures stay visible.

No node consumes this evaluation's later trace, receipt, checkpoint or commit.
Missing source-owner interfaces are recorded as open construction dependencies,
not implemented as Boolean callbacks or silently replaced by fixture fields.
"""

# Empty prerequisites mean that the duty's own predicate is independent. Schema
# failure is never a global switch that hides an independent mismatch.
PREREQUISITES = {
 'AR_SCHEMA': [],
 'AR_ACTION_PROFILE': ['SELECTED_AUTHORIZATION_PATH'],
 'AR_EFFECT_SUBJECT': [], 'AR_ID': [], 'AR_TYPE': [], 'AR_SUBJECT': [],
 'AR_SCOPE': ['SELECTED_AUTHORIZATION_PATH'],
 'AR_SUBJECT_SCOPE_PROOF': ['SUBJECT_SCOPE_RELATION'],
 'AR_ASSERTOR': ['SELECTED_AUTHORIZATION_PATH'],
 'AR_ASSERTED_AT': ['ASSERTION_ACT'],
 'AR_ASSERTION_ACT_POSTURE': [], 'AR_ASSERTION_ACT_EVIDENCE': ['ASSERTION_ACT'],
 'AR_SUBJECT_TIME': [], 'AR_BODY': ['DOMAIN_MEANING', 'CONTEXT_IDENTITIES_AND_RELATIONS'],
 'AR_EVIDENCE': ['EVIDENCE_USE_AND_CITATION_CLOSURE'],
 'AR_CLAIM_STATE': [], 'AR_EVENT_ASSOCIATION': ['EVENT_OWNER', 'EVENT_DOMAIN'],
 'AR_OPERATION_POSTURE': [], 'AR_OPERATION_PERFORMER': ['PERFORMER_IDENTITY'],
 'AR_OPERATION_AGENT_ACTORSHIP': ['AGENT_ACTORSHIP'],
 'AR_OPERATION_PERFORMER_AUTHORITY': ['PERFORMER_AUTHORITY_EVIDENCE'],
 'AR_OPERATION_PAYLOADS': ['OPERATION_SOURCES'],
 'AR_COMPLIANCE_RULES': ['COMPLIANCE_RULE_SELECTION'],
 'AR_COMPLIANCE_EVIDENCE_POLICY': ['EVIDENCE_POLICY_SELECTION'],
 'AR_CORRECTION_LINEAGE': ['PRIOR_ASSERTION_CONTEXT'],
 'AR_STRUCTURE_BRANCH_ABSENCE': [], 'AR_OPERATION_BRANCH_ABSENCE': [],
 'AR_COMPLIANCE_BRANCH_ABSENCE': [], 'AR_LEGACY_ABSENCE': [],
 'PC_ONE_ASSERTION': ['AR_SCHEMA', 'PROTECTED_PROPOSED_STATE'],
 'PC_VALIDATED_BYTES': ['PROTECTED_PROPOSED_STATE', 'TRANSACTION_GATE_SELECTION'],
 'PC_INPUTS_IMMUTABLE': ['PROTECTED_PROPOSED_STATE', 'RESOLVED_INPUT_CLOSURE'],
 'PC_ACTION_TYPE': ['AR_ACTION_PROFILE', 'AR_EFFECT_SUBJECT', 'AR_TYPE'],
 'PC_PENDING_REVIEW': ['AR_CLAIM_STATE'],
 'PC_SUBJECT_SCOPE': ['AR_SUBJECT', 'AR_SCOPE', 'AR_SUBJECT_SCOPE_PROOF'],
 'PC_ASSERTOR': ['AR_ASSERTOR'],
 'PC_ASSERTION_ACT': ['AR_ASSERTOR', 'AR_ASSERTED_AT', 'AR_ASSERTION_ACT_POSTURE', 'AR_ASSERTION_ACT_EVIDENCE'],
 'PC_SUBJECT_TIME': ['AR_SUBJECT_TIME', 'SUBJECT_TIME_SOURCES'],
 'PC_TEMPORAL_SEPARATION': [],
 'PC_EVENT_ASSOCIATION': ['AR_EVENT_ASSOCIATION'],
 'PC_CORRECTION_LINEAGE': ['AR_CORRECTION_LINEAGE'],
 'PC_NO_UNBOUND_EFFECT': ['PROTECTED_PROPOSED_STATE'],
 'PC_NO_CURRENT_STATE': ['PROTECTED_PROPOSED_STATE', 'AR_CLAIM_STATE'],
 'PC_TRANSACTION_HANDOFF': ['TRANSACTION_GATE_SELECTION'],
 'PC_UNIQUE_ID': ['PROTECTED_PROPOSED_STATE'],
 'PC_STRUCTURE': ['AR_BODY', 'PC_NO_UNBOUND_EFFECT', 'PC_PENDING_REVIEW'],
 'PC_OPERATION': ['AR_OPERATION_POSTURE', 'AR_OPERATION_PERFORMER', 'AR_OPERATION_AGENT_ACTORSHIP',
                  'AR_OPERATION_PERFORMER_AUTHORITY', 'AR_OPERATION_PAYLOADS', 'PC_SUBJECT_TIME',
                  'AR_BODY', 'PC_NO_UNBOUND_EFFECT', 'PC_PENDING_REVIEW'],
 'PC_COMPLIANCE': ['AR_COMPLIANCE_RULES', 'AR_COMPLIANCE_EVIDENCE_POLICY', 'AR_EVIDENCE',
                   'PC_SUBJECT_TIME', 'AR_BODY', 'PC_NO_UNBOUND_EFFECT', 'PC_PENDING_REVIEW'],
 'PC_BRANCH_ABSENCE': ['AR_STRUCTURE_BRANCH_ABSENCE', 'AR_OPERATION_BRANCH_ABSENCE',
                      'AR_COMPLIANCE_BRANCH_ABSENCE', 'AR_LEGACY_ABSENCE'],
}

OWNER_DEPENDENCIES = {
 'SELECTED_AUTHORIZATION_PATH': 'Existing authorization owner must supply the canonical selected authoritySubjectPartyRef, path basis and exact action/rule/schema/contract selection. actingPartyRef and the act fixture expectation are not substitutes.',
 'SUBJECT_SCOPE_RELATION': 'Typed immutable subject/anchor resolution and any required directed relation at the selected time and extent.',
 'ASSERTION_ACT': 'Exact act owner checker over original content, intent, source, context, policy and profile bytes.',
 'DOMAIN_MEANING': 'All source predicates and returned source roles for every recursive atom, not only intrinsic or selected-meaning equality.',
 'CONTEXT_IDENTITIES_AND_RELATIONS': 'Every typed body context resolves at its exact selected identity and directed relation use time, without widening the sole authority anchor.',
 'EVIDENCE_USE_AND_CITATION_CLOSURE': 'Typed role table, every selected original evidence record and its existing use/admission mechanism.',
 'EVENT_OWNER': 'Exact pre-verdict Event Ingress checker; no later ingress result substitutes for it.',
 'EVENT_DOMAIN': 'Complete selected event meaning, subject/anchor, time and body/payload comparisons.',
 'PERFORMER_IDENTITY': 'Selected performer identity and source linkage, distinct from reporter and authority subject.',
 'AGENT_ACTORSHIP': 'Existing agent actorship evidence for performed software-agent allegations.',
 'PERFORMER_AUTHORITY_EVIDENCE': 'Actual optional evidence comparison; it never changes NOT_EVALUATED_BY_AUTHORIZATION.',
 'OPERATION_SOURCES': 'Actual intent/execution sources plus every row-required source role.',
 'COMPLIANCE_RULE_SELECTION': 'Exact selected governing rule revisions and their applicability predicates.',
 'EVIDENCE_POLICY_SELECTION': 'Exact selected evidence-policy revisions and eligible-use predicates.',
 'PRIOR_ASSERTION_CONTEXT': 'Storage-owner positive start-snapshot visibility plus subtype, boundary/twin, anchor and logical-subject comparisons.',
 'PROTECTED_PROPOSED_STATE': 'Exact pre-verdict state-owner checker and independent comparison of all domain-required protected reads, absence, set and write obligations to these original intent/result bytes.',
 'TRANSACTION_GATE_SELECTION': 'Reviewed owner selection of the applicable later atomic gate and pre-verdict handoff predicate. This is not a receipt or proof of an already completed atomic commit.',
 'RESOLVED_INPUT_CLOSURE': 'Every selected immutable input and original raw byte hash appears in the protected read set.',
 'SUBJECT_TIME_SOURCES': 'Exact profile-specific source selectors, including independent measurement for PERFORMED_INSTANT.',
}


def validate_graph(ordered_ids):
    if len(ordered_ids) != 49 or set(ordered_ids) != set(PREREQUISITES):
        raise ValueError('The graph must retain exactly the 49 original duty IDs.')
    complete, visiting = set(), set()
    def visit(node):
        if node in visiting:
            raise ValueError('Cyclic duty dependency: ' + node)
        if node in complete:
            return
        if node not in PREREQUISITES:
            if node not in OWNER_DEPENDENCIES:
                raise ValueError('Undeclared prerequisite: ' + node)
            return
        visiting.add(node)
        for parent in PREREQUISITES[node]:
            visit(parent)
        visiting.remove(node)
        complete.add(node)
    for node in ordered_ids:
        visit(node)
    return True
