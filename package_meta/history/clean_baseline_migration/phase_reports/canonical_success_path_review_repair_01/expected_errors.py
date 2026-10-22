"""Reviewed first-error expectations; a different failure is a failed test."""
import re
ERRORS={
'evidence-authoritySubjectPartyRef':'SELECTED_PATH_CONTENT_MISMATCH','evidence-pathId':'SELECTED_PATH_CONTENT_MISMATCH','evidence-authoritySubjectBasis':'SELECTED_PATH_CONTENT_MISMATCH',
'coherent-mirrored-party':'ACCOUNTABLE_PARTY_MISMATCH','missing-AUTHENTICATED_PRINCIPAL':'REQUIRED_BASIS_ROLE_MISSING','missing-PRINCIPAL_RESOLUTION':'REQUIRED_BASIS_ROLE_MISSING','missing-SOURCE_AUTHORITY':'SOURCE_TUPLE_BINDING_NOT_RESOLVED','missing-AUTHORITY_SUBJECT_PARTY':'REQUIRED_BASIS_ROLE_MISSING',
'wrong-canonical-tuple':'CANONICAL_TUPLE_ENCODING_MISMATCH','unresolved-tuple-source':'SOURCE_TUPLE_BINDING_NOT_RESOLVED',
'wrong-REQUEST':'SELECTED_ACTION_MISMATCH','wrong-RESULT':'RESULT_TRACE_FIELD_MISMATCH','wrong-TRACE':'RESULT_TRACE_FIELD_MISMATCH','wrong-RULE':'SELECTED_ACTION_MISMATCH','wrong-BINDING_MANIFEST':'MANIFEST_POLICY_RULE_MISMATCH','wrong-DERIVED_VIEW':'DERIVED_VIEW_DIGEST_MISMATCH','wrong-EVALUATION_SNAPSHOT':'EVALUATION_SNAPSHOT_CONTEXT_MISMATCH',
'intent-substitution':'COMPLETE_INTENT_DIGEST_MISMATCH','nested-bundle-field':'DECISION_BUNDLE_DIGEST_MISMATCH','wrong-visibility-snapshot':'TRACE_PATH_VISIBILITY_MISMATCH',
'missing-snapshot-basis':'SCHEMA_INVALID','missing-snapshot-historyPosition':'SCHEMA_INVALID','missing-snapshot-indexWatermarks':'SCHEMA_INVALID','missing-snapshot-evidencePolicyRegistryBinding':'SCHEMA_INVALID','missing-snapshot-sovereigntyPolicyBinding':'SCHEMA_INVALID','mutable-selector':'SCHEMA_INVALID','consumer-report-profile':'SCHEMA_INVALID',
'changed-original-byte':'SOURCE_BYTES_MISMATCH','duplicate-json-name':'DUPLICATE_JSON_MEMBER','nonfinite-json':'INVALID_JSON_OR_CANONICAL_VALUE','unpaired-surrogate':'INVALID_JSON_OR_CANONICAL_VALUE','depth-limit':'JSON_DEPTH_LIMIT',
'representation-party-substitution':'REPRESENTATION_LINK_MISMATCH','mismatch-CP3_ACTORSHIP_BINDING-agentInstanceRef':'CP3_IDENTITY_LINK_MISMATCH','mismatch-CP3_AUTHORITY_ENVELOPE-executingAgentInstanceRef':'CP3_IDENTITY_LINK_MISMATCH','mismatch-CP3_AUTHORITY_ENVELOPE-agentSponsorRef':'CP3_IDENTITY_LINK_MISMATCH','mismatch-AGENT_IDENTITY-agentPartyRef':'AGENT_IDENTITY_LINK_MISMATCH',
'mismatch-CP3_AUTHORITY_ENVELOPE-authorizationDecisionResultRef':'CP3_DECISION_LINK_MISMATCH','mismatch-CP3_AUTHORITY_ENVELOPE-authorizationDecisionTraceRef':'CP3_DECISION_LINK_MISMATCH','mismatch-CP3_AUTHORITY_ENVELOPE-requestedActionClass':'CP3_DECISION_LINK_MISMATCH','mismatch-CP3_REVOCATION_STATE-authorityEnvelopeRef':'CP3_REVOCATION_LINK_MISMATCH','delegation-agent-substitution':'DELEGATION_PARTY_LINK_MISMATCH'}
def expected_error(name):
 suffix=re.sub(r'^basis-\d-(party|role)-','',name)
 if suffix=='source-target-substitution':return 'ROLE_PARTY_LINK_MISMATCH' if '-role-' in name else 'AUTHORITY_TARGET_PARTY_MISMATCH'
 return ERRORS[suffix]
