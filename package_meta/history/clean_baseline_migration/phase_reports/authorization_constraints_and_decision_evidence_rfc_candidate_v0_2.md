# OFARM Executable Authorization Constraints and Decision Evidence RFC v0.2

Date: 2026-08-31
Status: Phase A RFC candidate for issue `samovers/OFARM#10`; non-authoritative, not accepted law, and not a current/default machine contract
Triggered by: review of `samovers/OFARM2#353` and draft `samovers/OFARM2#359`
Blocks: `samovers/OFARM2#353` and draft `samovers/OFARM2#359` until accepted semantics, promoted contracts, and byte-identical extraction exist
Scope: define reviewable authorization semantics and the exact versioned contract delta needed before an implementation can claim a durable, fail-closed authorization decision

---

## 1. Decision requested

This candidate asks OFARM stewards to approve, reject, or amend one bounded design:

1. authorization-relevant principal resolution comes from a trusted boundary, while software-agent action posture preserves the accepted five-state CP3 model and remains independent from optional AI-assistance metadata;
2. the action class selects its authority family, stage, inheritance ceiling, authorization-resource policy, effect-subject policy, delegation ceiling, agent-action posture, and human-finalization requirement from one versioned policy rule;
3. purpose is a closed, exact-match use constraint in v0.2, not a comparison between unrelated free-text fields;
4. untyped or unsupported conditions never evaluate to true;
5. required evidence is usable only under an active evidence-eligibility policy;
6. authorization-resource proof, effect-subject proof, scope proof, role scope, grant scope, delegation source, sharing basis, and revocation posture are independently evaluated and durably recorded;
7. the exact effect intent, trusted evaluation time, current authority snapshot, validity window, consumption mode, and human approval are cryptographically bound to one decision;
8. the request, result, trace, and governed effect commit form a reconstructible decision/effect protocol with deterministic mixed-path outcomes; and
9. current v0.1 records remain historical v0.1 records and are not silently treated as v0.2 proof.

This document deliberately precedes accepted-RFC, schema, conformance, and currentness changes. Approval of this candidate does not itself promote any law or contract.

---

## 2. Primary trust boundary and intended PR boundary

### 2.1 Primary trust boundary

The primary trust boundary is **canonical authorization law and machine-contract governance**.

It defines:

- which facts may contribute authority;
- what each authorization constraint means;
- what must be proved before `ALLOW`;
- what outcome is required when a fact is absent, ambiguous, unsupported, or contradictory; and
- what durable evidence must exist for an authorization decision claim.

### 2.2 Intended Phase A PR boundary

The Phase A PR adds only this non-authoritative candidate under historical phase reports. It does not change:

- the active Constitution or Platform runtime baseline;
- an accepted RFC or companion policy;
- a current/default or draft machine schema;
- authentication or credential verification;
- principal resolution;
- CP3 software-agent envelope implementation;
- grant, delegation, sharing, role, or revocation mutation;
- database roles, tables, migrations, or row-level security;
- signing, key custody, bootstrap, recovery, or break-glass behavior;
- OFARM2 runtime code; or
- any production-readiness claim.

If review requires one of those boundaries to change, that work must be split into a prerequisite, follow-up, or stacked PR.

Sections that define atomic effect and outbox evidence state the conformance condition under which an authorization claim is truthful. They do not implement a transaction manager, dispatcher, or runtime integration in this PR. That later implementation remains a separate OFARM2 trust-boundary change after canonical promotion.

---

## 3. Authority map and change classification

The authority order remains:

1. `00_active_baseline/`
2. `02_accepted_rfcs/`
3. `01_companion_artifacts/`
4. current/default contracts under `03_machine_contracts/schemas/`

Relevant accepted and companion authority includes:

- `OFARM_Authority_Policy_Model_RFC_v0_1.md`;
- `OFARM_Authority_Action_Matrix_v0_1.md`;
- `OFARM_Authority_Source_Record_Closure_RFC_v0_1.md`;
- `OFARM_Agent_Actorship_and_Authority_RFC_v0_1.md`; and
- `OFARM_Authority_Delegation_and_Data_Sovereignty_Policy_v0_2.md`.

This candidate is lower authority than every item above. Where it differs, active authority wins until a later governed promotion explicitly changes that authority.

Proposed change classification after approval:

- Constitution change: no;
- active-baseline rewrite: no;
- accepted RFC extension: yes;
- accepted CP3 compatibility mapping: yes, preserving the five accepted posture values without changing CP3 semantics;
- action-matrix version: yes, from v0.1 to a proposed v0.2;
- authority-source contract versions: yes, where closed constraints cannot be represented in v0.1;
- authorization-decision contract versions: yes;
- hostile conformance: yes; and
- current/default promotion: separate, explicit, human-governed step only.

The proposed compatibility mapping adopts the active CP3 posture vocabulary. It does not edit the accepted CP3 RFC or its current machine contracts. If later review requires different posture meanings or a changed CP3 envelope, that authority change must travel in a separate stacked PR.

---

## 4. Problem statement

The active v0.1 model correctly says that authorization depends on action class, accountable actor, target, scope, time, role, grant, delegation, sharing, revocation, inheritance, and human accountability. It does not yet close several comparisons tightly enough for independent runtimes to reach the same safe result.

The machine contracts expose the gap:

- `AuthorityGrant`, `DelegationGrant`, and `SharingGrant` carry free-text `purpose` and `conditions`;
- `AuthorizationDecisionRequest` carries a separate caller-provided `usePurpose`;
- `requiredAuthorityFamily`, `actionStage`, `nonHumanActor`, and `revocationCheckRequired` are caller fields even though they are policy conclusions or mandatory checks;
- optional `aiAssistance` can be omitted and cannot prove human authorship or human final action;
- caller-provided `targetTime` can be confused with the trusted time at which current authority and revocation must be checked;
- the decision is not bound to a digest of the complete protected effect and has no closed validity or replay posture;
- v0.1 actor fields do not separately identify the authenticated principal, represented Party, representation basis, CP3 action posture, and human-finalization requirement;
- `AuthorizationDecisionTrace` cannot identify the exact policy version and digest used;
- the trace cannot record trusted principal resolution, full authorization resource, prospective effect subject, generic scope proof, or constraint evidence;
- `dataSovereigntyBoundaryRefs` is specific to actual `DataSovereigntyBoundary` records and cannot truthfully hold arbitrary proof references;
- a role-targeted grant can appear to escape the referenced `RoleAssignment.anchorScopes` if only the grant scope is checked;
- current narrowing revocations name modes but do not carry enough closed operands to evaluate every narrowing deterministically; and
- v0.1 does not define whether partial constraints from different grant paths may be unioned, how mixed path outcomes aggregate, or which immutable source revisions were visible to the evaluator.

Without closure, one runtime can silently normalize a purpose, another can ignore it, a third can treat free-text conditions as descriptive, and all three can claim conformance. That is an authorization trust failure, not merely an interoperability inconvenience.

---

## 5. Core safety stance

### 5.1 `ALLOW` is a complete-proof claim

`ALLOW` means one permitted authorization path has independently satisfied every applicable constraint under one identified policy bundle.

Absence of a prohibition is not proof of authority.

### 5.2 Caller assertions do not create policy facts

A caller may request an action, name an authorization resource and effect subject, state a governed subject time, disclose a purpose, and provide candidate references. The caller may not choose:

- the required authority family;
- the action stage;
- whether revocation is checked;
- whether the authenticated principal is a natural person or software agent;
- the actor's accountable sponsor;
- the authorization resource's governed kind or the effect subject's existence posture;
- the scope relationship;
- the policy version; or
- whether evidence is current and eligible.

Those facts come from trusted resolution or from the selected policy bundle.

### 5.3 Unknown does not become false, and false does not become true

Missing AI disclosure does not prove that no AI participated. Missing condition semantics does not mean the condition passed. Missing proof does not mean the relationship is obvious. An unknown or unsupported authority-relevant fact produces a non-`ALLOW` outcome.

### 5.4 Partial paths are not unioned

An evaluator must not combine the action coverage of one grant, the purpose coverage of a second grant, and the evidence coverage of a third grant to manufacture a complete path. Each selected direct or delegated authorization path must be sufficient by itself, except for the explicit `RECEIVE_READ_DATA` sharing composition defined in section 13.

---

## 6. Principal resolution, CP3 posture, and human finalization

The earlier candidate overloaded one "actor posture" field with three different decisions. v0.2 keeps them separate.

### 6.1 Resolved principal axis

Trusted principal resolution produces exactly one `resolvedPrincipalKind`:

- `NATURAL_PERSON`
- `SOFTWARE_AGENT`
- `UNRESOLVED`

The decision bundle also records:

- `authenticatedPrincipalRef`;
- `authenticatedPrincipalRevisionRef` or content digest;
- `representedPartyRef`, when the principal acts for another Party;
- `representationBasisRef` and immutable revision, when representation applies; and
- `authoritySubjectPartyRef`, the Party against which Party- or role-targeted grants are compared.

For a natural person acting for self, `authoritySubjectPartyRef` is that person's Party reference and `representedPartyRef` is absent. For a natural person acting for an organization, `representedPartyRef` and `representationBasisRef` are mandatory and `authoritySubjectPartyRef` is the represented organization. An organization reference alone never proves a natural-person final action.

For a software agent, `authenticatedPrincipalRef` identifies the executing agent instance. `authoritySubjectPartyRef` must be resolved from the active CP3 authority envelope; a sponsor reference is accountability evidence and is not automatically the grant holder. A model, tool, API key, prompt, session, public-operation descriptor, or caller boolean is not an authority-bearing principal.

`UNRESOLVED` is always non-`ALLOW`.

### 6.2 Accepted CP3 `AgentActionPosture` axis

Every software-agent action uses one exact posture already accepted by `OFARM_Agent_Actorship_and_Authority_RFC_v0_1.md`:

- `AGENT_ALLOWED_WITH_POLICY_CHECK`
- `AGENT_ALLOWED_WITH_PREFLIGHT_ONLY`
- `AGENT_ALLOWED_WITH_HUMAN_APPROVAL`
- `HUMAN_ONLY`
- `PROHIBITED_FOR_AGENT`

This candidate does not rename, collapse, or reinterpret those values.

`AGENT_ALLOWED_WITH_POLICY_CHECK` permits a sponsor-bound agent to perform the action only after the complete v0.2 authorization policy passes.

`AGENT_ALLOWED_WITH_PREFLIGHT_ONLY` additionally requires the active preflight and result-qualification surface before the action can be treated as permitted.

`AGENT_ALLOWED_WITH_HUMAN_APPROVAL` requires the complete agent policy path plus a fresh human approval bound to the same effect-intent digest.

`HUMAN_ONLY` means the action may be performed only with an authenticated natural person as the direct principal. A software agent may perform a separately authorized preparatory action class, but cannot be the direct principal for this action.

`PROHIBITED_FOR_AGENT` means the action is unavailable through a software-agent action surface, including as a nominal direct request. No v0.2 row is assigned this posture by default, but the value remains distinct and available for a stronger action policy.

For every software-agent decision, the trace must bind immutable revisions or digests of:

- `executingAgentInstanceRef`;
- `softwareAgentProfileRef`;
- `agentSponsorRef`;
- `agentActorshipBindingRef`;
- `agentAuthorityEnvelopeRef`;
- mandatory `authoritySnapshotRef`;
- `agentRevocationStateRef`; and
- any required preflight and result-qualification records.

Missing, stale, revoked, mismatched, or mutable-only CP3 evidence is non-`ALLOW`.

### 6.3 Human-finalization axis

The separate `humanFinalizationRequirement` is one of:

- `NOT_REQUIRED`
- `FRESH_HUMAN_APPROVAL_REQUIRED`
- `DIRECT_HUMAN_ACTION_REQUIRED`

`FRESH_HUMAN_APPROVAL_REQUIRED` requires a trusted natural-person approval record bound to:

- the action class;
- `effectIntentSchemaRef` and `effectIntentDigest`;
- the authorization-resource and effect-subject identities;
- the policy digest;
- `authorityEvaluationSnapshotRef`;
- `decisionValidUntil`; and
- the represented Party and representation basis, when applicable.

`DIRECT_HUMAN_ACTION_REQUIRED` requires the authenticated direct principal for the protected action to be a natural person. A sponsor approval of an agent request does not convert an agent into the direct human actor.

Approval for a different digest, policy, snapshot, Party, or validity window is not reusable.

### 6.4 AI-assistance disclosure

AI-assistance metadata is provenance only. It has exactly these decision-trace dispositions:

- `DISCLOSED_ASSISTED`
- `DISCLOSED_NOT_ASSISTED`
- `NOT_DISCLOSED_OR_UNKNOWN`

Changing, omitting, or retrying optional AI-assistance metadata must not change principal resolution, CP3 posture, human-finalization requirements, authority basis, or outcome.

### 6.5 Compatibility boundary

This RFC extension may map each authorization action class to an existing CP3 posture. It may not change CP3 posture meanings or weaken the active AgentAuthorityEnvelope obligations. A requested semantic or schema change to CP3 must be split into a stacked prerequisite or follow-up PR.

---

## 7. Proposed action-policy matrix v0.2

### 7.1 Exact authority-family tokens

The v0.2 tokens are:

- `OBSERVE_REPORT`
- `ASSERT_SUBMIT`
- `OPERATE_INTERVENE`
- `REVIEW`
- `GOVERN_DECIDE`
- `CONTEXT_GOVERNANCE`
- `ATTEST_SIGN`
- `SHARE_REVOKE`
- `RECEIVE_USE`

An action rule selects one token. A source record's `authorityFamilies` must contain that exact token. Comparison is code-point exact: no trimming, case folding, punctuation replacement, synonym expansion, or substring matching. A source record containing an unknown family token is schema-invalid in v0.2 and is not eligible for `ALLOW`.

### 7.2 Exact matrix

Inheritance codes are `D` = `DESCENDANT_SCOPES`, `X` = `EXACT_ONLY`, and `N` = `NO_INHERIT`. This proposal does not add `DERIVED_LINEAGE_SCOPES` to any of the 20 existing action rows.

Delegation codes are `DA` = `DELEGATION_ALLOWED`, `DX` = `EXPLICIT_SOURCE_PERMISSION_REQUIRED`, and `DP` = `DELEGATION_PROHIBITED`.

Agent-posture codes preserve CP3: `PC` = `AGENT_ALLOWED_WITH_POLICY_CHECK`, `PF` = `AGENT_ALLOWED_WITH_PREFLIGHT_ONLY`, `HA` = `AGENT_ALLOWED_WITH_HUMAN_APPROVAL`, and `HU` = `HUMAN_ONLY`. `PROHIBITED_FOR_AGENT` remains a valid stronger-policy value but is not the default for these rows.

Human-finalization codes are `NR` = `NOT_REQUIRED`, `FA` = `FRESH_HUMAN_APPROVAL_REQUIRED`, and `DH` = `DIRECT_HUMAN_ACTION_REQUIRED`.

Existence codes are `E` = `EXISTING_REQUIRED` and `P` = `PROSPECTIVE_TARGET_ALLOWED`.

| Action class | Authority family | Stage | Inheritance | Delegation | Agent posture | Human finalization | Authorization resource | Effect subject / existence |
|---|---|---|---|---|---|---|---|---|
| `OBSERVE_CREATE_OBSERVATION` | `OBSERVE_REPORT` | `DRAFT_PREPARATION` | D | DA | PC | NR | `GOVERNED_SCOPE` | `OBSERVATION` / P |
| `OBSERVE_ATTACH_EVIDENCE` | `OBSERVE_REPORT` | `DRAFT_PREPARATION` | D | DA | PC | NR | `GOVERNED_RECORD` | `EVIDENCE_LINK` / P |
| `ASSERT_STRUCTURE` | `ASSERT_SUBMIT` | `DRAFT_PREPARATION` | X | DX | HA | FA | `GOVERNED_SCOPE` | `STRUCTURE_ASSERTION` / P |
| `ASSERT_OPERATION_CLAIM` | `ASSERT_SUBMIT` | `DRAFT_PREPARATION` | D | DA | PC | NR | `GOVERNED_SCOPE` | `OPERATION_ASSERTION` / P |
| `ASSERT_COMPLIANCE` | `ASSERT_SUBMIT` | `DRAFT_PREPARATION` | X | DX | HA | FA | `GOVERNED_SCOPE` | `COMPLIANCE_ASSERTION` / P |
| `OPERATE_PLAN_INTERVENTION` | `OPERATE_INTERVENE` | `DRAFT_PREPARATION` | D | DA | PC | NR | `GOVERNED_SCOPE` | `INTERVENTION_PLAN` / P |
| `OPERATE_REPORT_EXECUTION` | `OPERATE_INTERVENE` | `DRAFT_PREPARATION` | D | DA | PC | NR | `GOVERNED_SCOPE` | `EXECUTION_REPORT` / P |
| `REVIEW_REQUEST` | `REVIEW` | `DRAFT_PREPARATION` | X | DA | PC | NR | `GOVERNED_RECORD` | `REVIEW_REQUEST` / P |
| `REVIEW_ACCEPT` | `GOVERN_DECIDE` | `PROMOTION` | N | DP | HU | DH | `GOVERNED_RECORD` | `REVIEW_DECISION` / P |
| `REVIEW_REJECT_OR_CONTEST` | `GOVERN_DECIDE` | `PROMOTION` | N | DP | HU | DH | `GOVERNED_RECORD` | `REVIEW_DECISION` / P |
| `REVIEW_SUPERSEDE` | `GOVERN_DECIDE` | `PROMOTION` | N | DP | HU | DH | `GOVERNED_RECORD` | `REVIEW_DECISION` / P |
| `CONTEXT_INSTALL_PACK` | `CONTEXT_GOVERNANCE` | `CONTEXT_ACTIVATION` | N | DP | HU | DH | `GOVERNED_SCOPE`, `PACK_REGISTRY` | `PACK_INSTALLATION` / P |
| `CONTEXT_ACTIVATE_PACK` | `CONTEXT_GOVERNANCE` | `CONTEXT_ACTIVATION` | N | DP | HU | DH | `GOVERNED_SCOPE`, `PACK_REGISTRY` | `PACK_ACTIVATION_SET` / P |
| `CONTEXT_DEACTIVATE_PACK` | `CONTEXT_GOVERNANCE` | `CONTEXT_ACTIVATION` | N | DP | HU | DH | `GOVERNED_SCOPE`, `PACK_REGISTRY` | `PACK_ACTIVATION_SET` / E |
| `OUTPUT_APPROVE_DOCUMENT_ASSEMBLY` | `ATTEST_SIGN` | `PUBLICATION` | N | DP | HU | DH | `DOCUMENT_ASSEMBLY`, `DOSSIER_ASSEMBLY` | `ASSEMBLY_APPROVAL` / P |
| `OUTPUT_ATTEST_DOCUMENT_ASSEMBLY` | `ATTEST_SIGN` | `ATTESTATION` | N | DP | HU | DH | `DOCUMENT_ASSEMBLY`, `DOSSIER_ASSEMBLY` | `ASSEMBLY_ATTESTATION` / P |
| `OUTPUT_FILE_SUBMISSION_ASSEMBLY` | `ATTEST_SIGN` | `PUBLICATION` | N | DX | HU | DH | `SUBMISSION_ASSEMBLY` | `SUBMISSION_FILING` / P |
| `SHARE_GRANT_ACCESS` | `SHARE_REVOKE` | `PROMOTION` | X | DA | HA | FA | `SHARED_ARTIFACT` | `SHARING_GRANT` / P |
| `SHARE_REVOKE_ACCESS` | `SHARE_REVOKE` | `PROMOTION` | X | DA | HA | FA | `SHARED_ARTIFACT` | `SHARING_GRANT` / E |
| `RECEIVE_READ_DATA` | `RECEIVE_USE` | `QUERY_READ` | D | DA | PF | NR | `DATA_RESOURCE` | `DATA_ACCESS` / P |

### 7.3 Matrix rules

The inheritance entry is a ceiling, not a grant. A source record may narrow `D` to `X` or `N`, and may narrow `X` to `N`. It may not broaden the row. A row marked `N` must use `NO_INHERIT`.

The delegation entry is also a ceiling. Its intersection with source permission and the DelegationGrant is defined in section 10. Prose such as "with caution" has no executable meaning in v0.2.

All 20 proposed v0.2 rows use `SINGLE_USE`. No default row authorizes replay. Section 18 defines the only future-compatible replay posture and prevents a runtime from inventing local replay behavior.

`authorizationResource` is the pre-existing governed object against which authority is checked. `effectSubject` is the object acted on or created. They are not aliases. Section 8 defines both.

For `CONTEXT_INSTALL_PACK`, the effect intent must additionally bind an existing content-addressed `PACK_RELEASE` or `PACK_ARTIFACT`; `PACK_INSTALLATION` is the prospective result. For activation, every requested pack release is an immutable effect-intent input and `PACK_ACTIVATION_SET` is the proposed governed result. For deactivation, the existing activation set is the effect subject and the effect intent binds its proposed successor state.

For `ASSERT_COMPLIANCE`, compiled outputs may be immutable evidence or effect-intent inputs, but the effect subject is the prospective compliance assertion. A runtime must not substitute a compiled-output reference for the assertion body covered by `effectIntentDigest`.

`OUTPUT_FILE_SUBMISSION_ASSEMBLY` resolves the v0.1 alternative family to `ATTEST_SIGN` for v0.2. A deployment that needs a distinct non-attesting transmission action must propose a separate action class rather than reinterpret this one locally.

Unknown action classes, resource kinds, effect-subject kinds, existence postures, stages, or policy rules are non-`ALLOW`.

The resource/subject list is a proposed closure point and requires specific steward approval. It must not be inferred from the word "typical" in the v0.1 matrix.

---

## 8. Temporal, effect-intent, resource, and proof separation

### 8.1 Materially distinct times

The v0.2 request and trace preserve these distinct times:

- `subjectTime`: the governed occurrence, observation, execution, assertion, or other domain time to which the requested record refers; it may originate with the caller and must be qualified by the relevant domain contract;
- `authorizationEvaluatedAt`: a trusted runtime clock value for the authority snapshot used to decide the current request;
- `decisionValidUntil`: the latest trusted time at which the exact decision may be consumed;
- `effectCommittedAt`: the transaction time at which an internal governed effect and its decision evidence become committed together; and
- `effectDispatchedAt`, where applicable, the time an already committed external outbox intent is dispatched.

`subjectTime` never substitutes for `authorizationEvaluatedAt`, `effectCommittedAt`, or `effectDispatchedAt`.

Current principal binding, representation, role validity, grant validity, delegation, sharing, policy applicability, and revocation are evaluated at `authorizationEvaluatedAt` and must still hold at the effect boundary. For an internal governed write, the serializable transaction defined in section 18 supplies that effect-boundary guarantee. For an external side effect, the authorization applies to committing the exact outbox intent; any policy that requires authority to remain current at dispatch must perform and record a new dispatch-time evaluation.

An action rule may additionally require a historical authority check at `subjectTime`. That check is a second condition with its own evidence and disposition. It never replaces the current-authority check.

A current request made after revocation cannot regain authority by supplying a pre-revocation `subjectTime`.

### 8.2 Exact effect-intent binding

Every v0.2 request, result, trace, and human approval binds:

- `effectIntentSchemaRef`;
- `effectIntentRef` or an embedded immutable effect intent;
- `effectIntentDigest`; and
- `effectIntentCanonicalization`, fixed to `JCS_RFC8785_SHA256` for v0.2.

`effectIntentDigest` is `sha256:` followed by the SHA-256 digest of the UTF-8 bytes produced by RFC 8785 JSON Canonicalization Scheme over the complete effect intent validated by `effectIntentSchemaRef`.

The effect intent contains every authorization-relevant operation input, including at least:

- the exact proposed grantee, rights, purpose, and artifact for `SHARE_GRANT_ACCESS`;
- the exact pack release/content digest, installation parameters, requested profiles, exclusions, and proposed activation-set content for context actions;
- the exact assertion body, evidence set, subject time, and claimed scope for assertion actions;
- the exact governed record and proposed decision content for review actions; and
- the exact assembly revision, destination, filing mode, and payload digest for filing.

An operation-specific schema may require more. It may not omit a value that can change the authority result or protected effect.

Payload substitution after evaluation changes the digest and requires a new decision. A decision is never authority for a merely similar payload.

### 8.3 Authorization resource

`authorizationResource` is the pre-existing governed object against which grant scope and action authority are checked. It contains:

- `resourceKind`;
- `resourceRef`;
- immutable `resourceRevisionRef` or content digest;
- `scopeType` and `scopeRef`;
- `twin` where applicable; and
- `authorizationResourceProofRefs`.

The proof must establish existence, exact kind, immutable revision, currentness where required, twin, tenant, and scope binding at the applicable evaluation time. An opaque reference alone is not proof.

### 8.4 Effect subject and existence posture

`effectSubject` is the existing or prospective object changed, created, read, or acted upon. It contains:

- `subjectKind`;
- `subjectRef` or a proposed stable identifier;
- `existencePosture`, exactly `EXISTING_REQUIRED` or `PROSPECTIVE_TARGET_ALLOWED`;
- `subjectTime`, where the domain action has one;
- `effectSubjectProofRefs`; and
- the resulting immutable revision reference after a successful governed write.

For `EXISTING_REQUIRED`, proof must establish that the exact subject and immutable revision exist and are eligible for the action.

For `PROSPECTIVE_TARGET_ALLOWED`, proof establishes the permitted kind, namespace or parent, proposed identifier reservation where required, scope, tenant, and schema posture. It must not falsely claim that the result already exists. The committed result revision is added to effect evidence after success.

The authorization resource and effect subject may refer to the same existing object only when the action rule explicitly permits it. Their proof fields and semantic roles remain distinct.

### 8.5 Pack identity

`PACK_RELEASE` or `PACK_ARTIFACT` identifies immutable installable content. `PACK_INSTALLATION` identifies the governed installation result. `PACK_ACTIVATION_SET` identifies the concrete activation posture evaluated for a scope and time.

These kinds are not interchangeable. An activation-set identifier cannot prove which pack release was installed, and a pack release cannot masquerade as an applied activation set.

### 8.6 Scope proof

`scopeProofRefs` prove the relationship between the authorization resource, effect subject, and every authority-source scope. They may refer only to immutable governed identity, containment, tenancy, or explicitly allowed lineage records that establish the claimed relationship.

Authorization-resource proof, effect-subject proof, and scope proof are not interchangeable. One immutable artifact may be bound in more than one proof array only when it independently establishes each claimed fact, and each use has a typed disposition.

### 8.7 Sovereignty and tenant isolation

`dataSovereigntyBoundaryRefs` may contain only immutable revisions of actual `DataSovereigntyBoundary` records. Generic resource, subject, scope, tenant, role, policy, or constraint evidence uses its dedicated field.

Every source, proof, policy, and evidence record used by a path must resolve within the authorized deployment or tenant boundary. Cross-tenant equality of an opaque identifier does not establish authority. A cross-tenant reference without an accepted sharing and sovereignty path is non-`ALLOW`.

---

## 9. Role and grant semantics

### 9.1 Party-targeted AuthorityGrant

A Party-targeted `AuthorityGrant` path is eligible only when:

- the immutable grant revision is active at `authorizationEvaluatedAt` and remains valid at the effect boundary;
- the target Party is `authoritySubjectPartyRef` from trusted principal and representation resolution;
- the action class is present;
- the derived authority family is present;
- the authorization resource, effect subject, effect intent, and scope satisfy the grant's closed constraints;
- inheritance does not exceed the matrix ceiling;
- purpose, condition, and evidence rules pass;
- no active revocation defeats the path; and
- principal resolution, CP3 posture where applicable, and the human-finalization rule pass.

If the action rule requires historical authority, the same path is separately evaluated at `subjectTime`; historical success does not repair failure at current evaluation/effect time.

### 9.2 Role-targeted AuthorityGrant

A grant whose target kind is `ROLE_ASSIGNMENT` is eligible only when the referenced `RoleAssignment`:

- has an immutable revision that exists and is valid at `authorizationEvaluatedAt` and the effect boundary;
- names `authoritySubjectPartyRef`;
- is valid in the same tenant boundary; and
- has at least one `anchorScopes` entry that independently covers the authorization resource and effect subject under the same exact scope-proof rules.

The effective scope is the intersection of the action-matrix ceiling, the grant scope, and the matching role anchor scope. The grant cannot widen the role assignment, and the role assignment cannot widen the grant.

### 9.3 Grant candidates are hints

Candidate IDs supplied by a caller are retrieval hints only. The evaluator must resolve the complete eligible set or use a trusted, completeness-proven index. The decision trace records the immutable `authorityEvaluationSnapshotRef`, canonical-history position, and index watermark used to prove completeness. Absence from a caller candidate list cannot hide a source or revocation, force selection of a weaker path, or change the outcome.

---

## 10. Delegation semantics

### 10.1 Closed action-rule ceiling

Every action rule carries one `delegationCeiling`:

- `DELEGATION_ALLOWED`
- `EXPLICIT_SOURCE_PERMISSION_REQUIRED`
- `DELEGATION_PROHIBITED`

`DELEGATION_PROHIBITED` makes every delegated path ineligible.

`DELEGATION_ALLOWED` permits evaluation of a source whose explicit source permission covers all granted actions or lists the requested action.

`EXPLICIT_SOURCE_PERMISSION_REQUIRED` permits only a source that explicitly lists the requested action class. A blanket source permission is insufficient.

### 10.2 Closed source permission

`AuthorityGrant v0.2` carries required `delegationPermission`:

- `NOT_DELEGABLE`
- `DELEGABLE_GRANTED_ACTIONS`
- `DELEGABLE_LISTED_ACTIONS`

`delegableActionClasses` is prohibited for `NOT_DELEGABLE`, optional and narrowing for `DELEGABLE_GRANTED_ACTIONS`, and required/non-empty for `DELEGABLE_LISTED_ACTIONS`. Every listed class must also occur in the grant's `authorityActionClasses`.

No source permission is inferred from role type, notes, historical behavior, or the existence of a DelegationGrant.

### 10.3 Intersection and precedence

A `DelegationGrant` is not origin authority. A delegated path is eligible only when:

1. the action-rule ceiling permits it;
2. the immutable source grant revision explicitly permits the action at the required precision;
3. the delegation itself contains the requested action and family;
4. the delegator held a live, independently sufficient source authority at `authorizationEvaluatedAt` and the effect boundary;
5. the delegation satisfies principal, authorization-resource, effect-subject, scope, time, purpose, condition, evidence, state, and revocation checks;
6. the delegation does not broaden action, family, resource, subject, effect intent, scope, inheritance, time, purpose, evidence, CP3 posture, or human-finalization requirement;
7. every `sourceAuthorityGrantRef` resolves to an immutable revision and is recorded; and
8. any role-targeted source grant is capped by its referenced `RoleAssignment.anchorScopes` exactly as described in section 9.2.

The effective delegated permission is the intersection of the action-rule ceiling, source grant, source role anchor, and DelegationGrant. The narrowest value wins at every dimension. A prohibition, missing source link, missing explicit permission, or unresolved revision makes the path ineligible.

The evaluator rejects cycles. The v0.2 default maximum delegation depth is one hop unless a later accepted policy introduces an explicit bounded chain contract and conformance suite.

---

## 11. Purpose semantics

### 11.1 Proposed v0.2 representation

Executable v0.2 sources use optional `permittedUsePurposes`, a non-empty unique array of closed purpose tokens. A v0.2 request uses optional scalar `requestedUsePurpose`.

Purpose tokens must match `^[A-Z][A-Z0-9_]{0,127}$`.

If a source has `permittedUsePurposes`:

- the request must contain `requestedUsePurpose`;
- the scalar must equal one member exactly;
- the purpose is evaluated for the same action, effect-intent digest, authorization resource, and effect subject as the request; and
- the trace records the requested token, source tokens, selected source reference, and `MATCHED` or `NOT_MATCHED` disposition.

No trimming, case folding, Unicode normalization, punctuation replacement, stemming, hierarchy, wildcard, prefix, substring, or synonym rule is implied.

If a v0.2 source omits `permittedUsePurposes`, that source carries no purpose restriction. The request purpose remains provenance and does not add authority.

### 11.2 Legacy free-text purpose

The v0.1 `purpose` field is descriptive free text. It must not be silently converted into a v0.2 purpose token.

A v0.1 source that carries non-empty `purpose` cannot support an automatic v0.2 `ALLOW` until a steward-reviewed migration creates a v0.2 source with explicit tokens. The v0.1 record remains unchanged and linked as migration provenance.

A caller-only `usePurpose` never satisfies a source constraint.

---

## 12. Conditions, limits, and required evidence

### 12.1 No generic condition language

This proposal does not create a free-text condition interpreter or a generic expression language.

The executable v0.2 limits are only:

- action class;
- authority family;
- authorization-resource kind/reference and effect-subject kind/reference/existence posture;
- effect-intent schema and digest;
- scope and inheritance;
- subject time, current authorization time, decision validity, and effect time;
- grant/delegation/sharing state;
- closed delegation ceiling, source permission, and delegation depth;
- closed purpose tokens;
- required evidence under a named policy;
- revocation; and
- resolved principal, accepted CP3 action posture, and human-finalization requirement.

Unknown fields are schema-invalid. A future typed constraint needs its own accepted semantics, versioned contract, and hostile conformance.

### 12.2 Legacy conditions

A non-empty v0.1 `conditions` array is unevaluable under v0.2. The evaluator must return a non-`ALLOW` outcome with `UNSUPPORTED_LEGACY_CONDITION`; it must not guess that prose is true.

Migration requires a steward to map the intended restriction into an already supported closed field or into a separately accepted typed condition profile. Removing the prose without preserving its restriction is forbidden widening.

### 12.3 Evidence-requirement origins

Evidence requirements may originate only from:

1. the selected action rule's `evidenceRequirementPolicyRefs`; and
2. typed `requiredEvidence` groups on `AuthorityGrant v0.2`, `DelegationGrant v0.2`, or `SharingGrant v0.2`.

Each source `requiredEvidence` entry contains exactly:

- `requiredEvidencePolicyRef` with immutable revision or content digest; and
- a non-empty unique `requiredEvidenceRefs` array whose members also bind immutable revisions or content digests.

The two members are an all-or-none group. No v0.2 source may carry unqualified evidence references. The pairing applies to every source family that can impose evidence, not only DelegationGrant.

An action-rule policy may derive required evidence from the exact `effectIntentDigest`; it cannot depend on an unbound payload supplied after evaluation.

### 12.4 Evidence intersection

Requirements are cumulative:

- every selected action-rule evidence policy must pass;
- every required-evidence group on the selected source path must pass;
- a delegated path must pass the action rule, source AuthorityGrant, and DelegationGrant groups; and
- a sharing path must pass the action rule and SharingGrant groups.

One evidence revision may satisfy more than one requirement only when each policy independently evaluates it as eligible. No source or policy overrides, erases, or weakens another requirement.

Until an evidence policy is active/current and its exact revision is retrievable, the requirement is `UNSUPPORTED_EVIDENCE_POLICY` and cannot support `ALLOW`.

### 12.5 Evidence evaluation

Every required evidence reference must:

- resolve to the exact immutable revision or content digest recorded by the decision;
- be the family required by the policy;
- be valid for the policy's explicit subject-time and authorization-time rules;
- not be stale beyond policy at `authorizationEvaluatedAt` or the effect boundary;
- not be disputed, invalid, withdrawn, or superseded when the policy excludes that state;
- belong to the permitted tenant and sovereignty boundary;
- bind to the authorization resource, effect subject, effect intent, and scope; and
- be eligible for `requestedUsePurpose` when purpose is constrained.

Missing, wrong-kind, stale, disputed, superseded, cross-tenant, unavailable, mutable-only, or otherwise ineligible evidence produces non-`ALLOW` and an individual evidence disposition in the trace.

Opaque existence of a logical reference is not evidence eligibility.

### 12.6 Legacy evidence

A v0.1 DelegationGrant containing `requiredEvidenceRefs` without an active evidence-policy revision is unevaluable for v0.2. It produces `UNSUPPORTED_LEGACY_EVIDENCE_REQUIREMENT`, not an inferred pass. Migration creates the applicable typed evidence group without rewriting the v0.1 source.

---

## 13. Sharing and `RECEIVE_READ_DATA`

`SharingGrant` is an access right, not assertion, review, governance, signing, or mutation authority.

For `RECEIVE_READ_DATA`, the evaluator performs one final decision with two layers:

1. an access basis: a sufficient `RECEIVE_USE` AuthorityGrant/DelegationGrant path or a sufficient SharingGrant for the exact grantee and artifact; and
2. a resource-control layer: authorization-resource proof, effect-intent binding, scope proof, tenant and sovereignty policy, purpose, conditions, evidence, state, current time, and revocation.

A SharingGrant path is eligible only when:

- `granteePartyRef` is `authoritySubjectPartyRef`;
- `sharedArtifactFamily` maps to `authorizationResource.resourceKind`;
- `sharedArtifactRef` and immutable revision exactly equal the authorization resource;
- the requested scope is covered;
- the immutable grant revision is active at `authorizationEvaluatedAt` and remains valid at the effect boundary;
- its purpose, conditions, and evidence groups are evaluable and pass for the exact effect intent;
- all actual sovereignty boundaries pass; and
- no active revocation defeats the sharing right.

A SharingGrant cannot authorize any action other than `RECEIVE_READ_DATA`. It cannot be cited as write, review, govern, context, sharing-administration, or signing authority.

A runtime must not evaluate a direct receive/use grant and a SharingGrant in separate endpoints that can return contradictory final answers. Their applicable bases and constraints are composed into one policy decision and one trace.

For `SHARE_GRANT_ACCESS`, `effectIntentDigest` covers the exact grantee, immutable artifact revision, rights, delivery mode, purpose, validity, scope, and sovereignty posture that will appear in the prospective SharingGrant. Substituting any of them requires a new decision and human approval.

---

## 14. Revocation semantics

Revocation lookup is mandatory for every source path. A caller cannot disable it.

### 14.1 `TERMINATE`

An effective `TERMINATE` decision for a source record makes that source path ineligible from `effectiveFrom` onward. Current requests compare `effectiveFrom` with trusted `authorizationEvaluatedAt` and the effect boundary, never with caller-provided `subjectTime`. It does not erase historical decisions made before the effective time.

### 14.2 Narrowing modes

The current v0.1 `NARROW_SCOPE`, `NARROW_ACTIONS`, and `NARROW_TIME` forms do not close all operands and merge behavior needed for deterministic evaluation.

Until a separately reviewed version closes those operands, an active narrowing decision affecting a candidate source produces `UNSUPPORTED_REVOCATION_NARROWING` and a non-`ALLOW` outcome for that path. A runtime must not ignore it, treat it as termination without saying so, or infer replacement semantics from notes.

This is bounded design debt, not a claim that narrowing is unsupported forever.

### 14.3 Revocation candidates

Revocations must be found from a trusted complete index keyed by affected artifact family/reference and trusted evaluation/effect time. The trace binds the index watermark and canonical-history position through `authorityEvaluationSnapshotRef`. Caller-supplied candidate lists are never the completeness boundary.

---

## 15. Deterministic evaluation

### 15.1 Evaluation order

The proposed evaluator order is:

1. validate the request and operation-specific effect-intent schema;
2. canonicalize the effect intent and verify `effectIntentDigest`;
3. assign trusted `authorizationEvaluatedAt` and load the immutable authority-evaluation snapshot;
4. load and verify the content-addressed policy bundle;
5. select the exact action rule;
6. resolve the authenticated principal, represented Party, representation basis, and authority subject;
7. resolve CP3 evidence and exact agent-action posture where the principal is software;
8. resolve and prove the authorization resource and effect subject under the row's existence posture;
9. prove tenant, sovereignty, and scope relationships;
10. resolve role and direct-grant paths at current authorization time;
11. evaluate action, family, resource, subject, intent, scope, inheritance, time, state, purpose, conditions, and cumulative evidence requirements per path;
12. resolve and evaluate delegated source paths under the closed delegation intersection;
13. compose any applicable `RECEIVE_READ_DATA` SharingGrant path;
14. apply every effective revocation from the completeness-proven snapshot;
15. apply any action-specific historical authority condition at `subjectTime` without replacing the current check;
16. apply human-finalization requirements bound to the exact effect-intent digest;
17. assign one disposition to every path and aggregate them under section 15.3;
18. build the request, result, and trace records with immutable basis bindings;
19. validate `decisionValidUntil`, consumption posture, and the decision-bundle digest; and
20. enter the atomic internal-effect or external-outbox protocol in section 18.

No later step may repair missing proof from an earlier step by trusting a caller assertion.

### 15.2 Path selection

Outcome is computed over all completely evaluated paths, not over the first database row returned.

If one or more paths fully allow, the selected path is the lowest canonical tuple:

1. path type order: direct Party grant, role-targeted grant, delegated grant, SharingGrant access path;
2. immutable source revision identifier in code-point order; and
3. immutable delegation/source revision identifiers in code-point order.

All other evaluated paths remain summarized in the trace. Selection order changes which sufficient basis is cited, not whether incomplete authority becomes complete.

### 15.3 Per-path dispositions

Every evaluated path receives exactly one disposition:

- `PATH_ALLOW`: every path constraint passes and no human approval remains outstanding;
- `PATH_REQUIRE_HUMAN_APPROVAL`: every authority constraint passes and only a fresh bound human approval remains outstanding;
- `PATH_REQUIRE_REVIEW`: the path is relevant but contains an explicitly unsupported or ambiguous governed semantic;
- `PATH_DENY`: the path fails one or more closed constraints; or
- `PATH_INAPPLICABLE`: the source does not target this principal/action/resource and contributes no outcome.

A path with both a closed denial and an unsupported semantic is `PATH_DENY`; a known failed constraint is not softened into review. A path with an outstanding human approval and any other failure is not `PATH_REQUIRE_HUMAN_APPROVAL`.

### 15.4 Global preconditions

Request-schema validity, effect-intent digest validity, policy integrity, trusted principal resolution, authorization-resource/effect-subject proof, tenant isolation, and authority-snapshot availability are global preconditions. A failed global precondition produces its reason-table outcome before path aggregation; no path may override it.

### 15.5 Total aggregation lattice

After global preconditions pass, path outcomes aggregate in this exact order:

1. if any path is `PATH_ALLOW`, outcome is `ALLOW`;
2. otherwise, if any path is `PATH_REQUIRE_HUMAN_APPROVAL`, outcome is `REQUIRE_HUMAN_APPROVAL`;
3. otherwise, if any path is `PATH_REQUIRE_REVIEW`, outcome is `REQUIRE_REVIEW`;
4. otherwise, outcome is `DENY`.

Therefore, a complete path that lacks only fresh human approval outranks an unrelated path with an unsupported legacy condition. A complete `PATH_ALLOW` also outranks an unrelated revoked path. Revocation of the source actually selected or a global revocation/tenant blocker still prevents `ALLOW`.

The selected path is chosen by section 15.2 from paths with the winning disposition.

### 15.6 Primary reason selection

Primary reason is outcome-specific:

- `ALLOW` uses `AUTHORIZED_BY_SELECTED_PATH`;
- `REQUIRE_HUMAN_APPROVAL` uses `HUMAN_FINAL_ACTION_REQUIRED` from the selected path;
- `REQUIRE_REVIEW` uses the lowest numeric review rank from the selected path; and
- `DENY` uses the lowest numeric deny rank from the selected path, or `NO_AUTHORITY_BASIS` when no applicable path exists.

Problems from non-selected paths remain ordered diagnostics and can never become the primary reason for an `ALLOW` or human-approval result. Numeric reason ranks are fixed in section 20; free-form severity does not select the primary reason.

---

## 16. Policy identity

Every v0.2 result and trace must identify:

- `policyId`;
- `policyVersion`;
- `policyDigest` in `sha256:<64 lowercase hexadecimal characters>` form; and
- `selectedRuleId`.

The digest covers the exact immutable representation used by the evaluator, including the action matrix and referenced decision rules after deterministic packaging. A mutable URL, branch name, deployment label, or semantic version alone is not enough.

If the loaded representation does not match the expected digest, the result is non-`ALLOW` with `POLICY_DIGEST_MISMATCH`.

The exact bytes covered by `policyDigest` must remain retrievable through a durable content-addressed reference for at least the decision-evidence retention period. A runtime that records a digest but cannot retrieve or independently verify the covered bytes cannot claim reconstructible v0.2 decisions.

### 16.1 Authority-evaluation snapshot

Every result and trace binds `authorityEvaluationSnapshotRef` to a governed immutable snapshot containing or resolving:

- canonical-history position or equivalent assertion/event watermark;
- role and grant index watermark;
- delegation and sharing index watermark;
- revocation index watermark;
- principal/representation resolution revision;
- CP3 authority snapshot where applicable;
- evidence-policy registry revision;
- sovereignty-policy revision; and
- policy-bundle content reference.

Every selected and rejected basis is represented by a typed binding with:

- logical reference;
- immutable revision/assertion reference or `sha256:` content digest;
- artifact family;
- evaluation disposition; and
- snapshot visibility proof.

A mutable logical identifier alone is insufficient. A later successor revision must not change reconstruction of the earlier decision.

---

## 17. Proposed contract family delta

### 17.1 Why source records also need v0.2

Changing only `AuthorizationDecisionRequest`, `AuthorizationDecisionResult`, and `AuthorizationDecisionTrace` would leave executable constraints trapped in ambiguous v0.1 source fields. The smallest honest v0.2 machine surface therefore includes versioned authority sources as well as the decision bundle.

This is an approval point. If stewards reject source-record versioning, they must choose another closed, versioned source of purpose and evidence constraints before the decision schemas can truthfully claim v0.2 proof.

### 17.2 Proposed versioned contracts

Draft/non-default work after RFC acceptance should add:

- `AuthorityGrant v0.2`;
- `DelegationGrant v0.2`;
- `SharingGrant v0.2`;
- `AuthorityEvaluationSnapshot v0.2`;
- `AuthorizationDecisionRequest v0.2`;
- `AuthorizationDecisionResult v0.2`;
- `AuthorizationDecisionTrace v0.2`;
- `AuthorizationDecisionConsumption v0.2`; and
- `AuthorizationEffectReceipt v0.2`.

`RoleAssignment v0.1`, `RevocationDecision v0.1`, and `DataSovereigntyBoundary v0.1` remain unchanged by default. If schema changes to those families prove necessary, they require an explicit scope review before editing.

### 17.3 Source-record delta

Common v0.2 source behavior:

- make `authorityFamilies` closed and required where the source carries authority families;
- add optional closed `permittedUsePurposes`;
- remove free-text `purpose` and `conditions` from the executable v0.2 form;
- reject unknown fields;
- add optional narrowing by authorization-resource kinds/refs, effect-subject kinds/refs/existence postures, effect-intent schema refs, and twins;
- retain closed action, scope, time, state, and inheritance constraints; and
- preserve immutable provenance linking a migrated record to its v0.1 predecessor.

`AuthorityGrant v0.2` additionally carries required closed `delegationPermission` and conditional `delegableActionClasses` as defined in section 10.

Every v0.2 source family that can impose evidence uses the typed all-or-none `requiredEvidence` groups in section 12. `DelegationGrant v0.2` is not a special exception.

`SharingGrant v0.2` makes the immutable artifact-family/resource-kind binding explicit and keeps `dataSovereigntyBoundaryRefs` restricted to actual sovereignty records.

### 17.4 Request v0.2

Caller-provided request facts:

- request identifier and request time;
- requested action class;
- authorization resource and immutable revision claimed by the request;
- effect subject, proposed identifier, existence posture, scope, `subjectTime`, and twin where applicable;
- `effectIntentSchemaRef`, retrievable effect intent, and `effectIntentDigest`;
- optional requested use-purpose token;
- optional AI-assistance disclosure; and
- optional retrieval hints that are explicitly non-authoritative.

Trusted boundary facts injected before evaluation:

- `resolvedPrincipalKind`;
- `authenticatedPrincipalRef` and immutable resolution revision;
- `representedPartyRef` and `representationBasisRef`, when applicable;
- `authoritySubjectPartyRef`;
- the CP3 envelope/snapshot references for a software agent;
- trusted `authorizationEvaluatedAt`; and
- `authorityEvaluationSnapshotRef`.

The caller cannot choose any trusted-boundary fact. `subjectTime` describes the governed subject only and never controls current authority.

Remove these caller-authoritative v0.1 fields:

- `actionStage`;
- `requiredAuthorityFamily`;
- `nonHumanActor`; and
- `revocationCheckRequired`.

They are derived or mandatory policy facts in v0.2.

### 17.5 Result v0.2

The result records:

- request and result identifiers;
- `authorizationEvaluatedAt`, `decisionValidUntil`, and `consumptionMode`;
- effect-intent schema, reference, digest, and canonicalization;
- requested action class;
- derived stage and authority family;
- policy identity and selected rule;
- resolved-principal kind, authority subject, accepted CP3 posture where applicable, and human-finalization requirement;
- deterministic outcome and primary reason code;
- winning per-path disposition and selected immutable basis;
- role, direct grant, delegation, sharing, and revocation basis summaries;
- inheritance mode applied;
- human approval and effect-intent binding;
- stable ordered problems; and
- trace reference.

### 17.6 Trace v0.2

The trace records at least:

- trace, request, and result identifiers;
- `subjectTime`, trusted `authorizationEvaluatedAt`, `decisionValidUntil`, and later effect/dispatch receipt refs;
- effect-intent schema, immutable reference, digest, and canonicalization;
- policy ID, version, digest, and selected rule;
- action class, derived stage, and derived family;
- resolved-principal kind, authenticated principal and immutable resolution revision, represented Party, representation basis, and authority subject;
- for software agents, executing instance, profile, sponsor, actorship binding, authority envelope, mandatory authority snapshot, revocation state, preflight, and qualification revision refs;
- accepted CP3 agent-action posture, human-finalization requirement, and AI-disclosure disposition;
- full authorization resource, immutable revision, scope, twin, proof refs, and individual dispositions;
- full effect subject, existence posture, subject time, proof refs, resulting revision ref where applicable, and individual dispositions;
- scope proof refs and individual dispositions;
- `authorityEvaluationSnapshotRef`, canonical-history position, and all relevant index watermarks;
- role assignments and anchor-scope immutable basis bindings/dispositions;
- direct grant, delegation, source-grant, and sharing immutable basis bindings/dispositions;
- revocation immutable basis bindings/dispositions;
- requested purpose, source purpose tokens, and purpose disposition;
- condition disposition;
- immutable evidence-policy refs, required evidence refs, constraint evidence refs, and individual evidence dispositions;
- immutable actual data-sovereignty boundary refs only;
- inheritance mode and delegation depth;
- human-finalization evidence refs bound to the effect-intent digest and disposition;
- every evaluated path's single disposition and ranked reasons, selected path, aggregated outcome, primary reason code, and reason; and
- a decision-bundle integrity digest.

Proof arrays are typed by use. An implementation must not place a scope proof in `constraintEvidenceRefs`, an evidence record in `dataSovereigntyBoundaryRefs`, or an arbitrary string in a proof array merely to satisfy cardinality.

---

## 18. Decision validity, consumption, and atomic effect protocol

### 18.1 Decision validity and replay

Every decision records `decisionValidUntil` from the selected action rule. The caller cannot extend it.

For the default `SINGLE_USE` rows, `decisionValidUntil` is the earliest of the trusted serializable-transaction deadline, selected source validity end, representation validity end, policy validity end, approval expiry, and authority-snapshot freshness deadline. The decision is consumed inside that transaction; it is not portable to a later transaction.

Every decision records one `consumptionMode`:

- `SINGLE_USE`; or
- `REPLAYABLE_IDENTICAL_READ`.

All v0.2 matrix rows are `SINGLE_USE`. `REPLAYABLE_IDENTICAL_READ` is reserved for a later accepted `RECEIVE_READ_DATA` rule and requires an exact `maxDecisionAge` in that rule. If promoted later, replay is limited to the same authenticated principal, authority subject, immutable resource revision, snapshot policy, and exact effect-intent digest until `decisionValidUntil`. Absent that accepted rule, replay is prohibited.

`AuthorizationDecisionConsumption` records the decision, effect-intent digest, consumer principal, consumption time, effect/outbox reference, and idempotency key. A second consumption of a single-use decision is non-`ALLOW` even if the payload is identical.

### 18.2 Internal governed writes

For an internal governed write, one serializable transaction must:

1. evaluate or revalidate current principal, representation, source authority, revocation, resource revision, and effect-intent digest against the transaction snapshot;
2. build and validate the request/result/trace bundle;
3. reserve single-use consumption;
4. apply the exact protected effect;
5. record the resulting immutable effect revision and `AuthorizationEffectReceipt`;
6. commit the decision evidence, consumption, receipt, and effect together.

If a concurrent authority, revocation, or resource change invalidates the snapshot, serialization must fail and the operation must be re-evaluated. The invariant is: **no governed effect becomes externally visible without its committed decision evidence**. The decision is not committed in an earlier transaction that creates a time-of-check/time-of-use gap.

### 18.3 External side effects

For an external side effect, one serializable transaction must atomically commit:

- the decision bundle;
- the single-use consumption reservation;
- an idempotent outbox record containing the exact effect-intent digest and destination; and
- a pending `AuthorizationEffectReceipt` reference.

The dispatcher may send only the committed bytes bound by the digest and idempotency key. It records dispatch completion or failure without rewriting the original decision.

Before dispatch, it must compare the current revocation/policy watermark with the recorded snapshot. If the selected action rule requires dispatch-current authority, or if a relevant watermark changed, dispatch pauses and a fresh authorization decision is required. Backdating `subjectTime` cannot bypass this check.

### 18.4 Non-`ALLOW` responses

For `DENY`, `REQUIRE_REVIEW`, or `REQUIRE_HUMAN_APPROVAL`, the request/result/trace refusal bundle commits atomically with no protected effect. Only after commit may an outer transport boundary convert it into a typed response.

If persistence fails, the runtime fails closed with a persistence/runtime error. It must not claim that a durable authorization denial or allowance exists when no trace committed.

### 18.5 Decision-bundle digest

The canonical v0.2 digest input is exactly:

```json
{
  "schemaVersion": "ofarm.authorizationDecisionBundleDigestInput.v0.2",
  "request": {},
  "result": {},
  "trace": {}
}
```

`request`, `result`, and `trace` are the complete validated records. The only excluded member is `decisionBundleDigest` wherever it occurs, preventing a hash cycle. No other semantic, proof, ordering, null, or metadata field is excluded.

The object is canonicalized with RFC 8785 JSON Canonicalization Scheme, encoded as UTF-8, hashed with SHA-256, and represented as `sha256:<64 lowercase hexadecimal characters>`. Every copy of `decisionBundleDigest` must match. Consumption and effect receipts refer to this digest and have their own schema-defined integrity digests.

This protocol is a future runtime conformance obligation. Phase A changes no runtime code.

---

## 19. Compatibility and migration

### 19.1 Historical validity

Existing v0.1 records remain valid as v0.1 records under the policy that evaluated them. They are not rewritten in place.

### 19.2 No silent proof-strength upgrade

A v0.1 decision or source record must not be relabeled, wrapped, or served as v0.2 merely because a runtime can fill some new fields with defaults.

In particular:

- missing policy digest cannot be reconstructed from the current deployment without proving it is the same immutable policy;
- optional AI metadata cannot reconstruct principal resolution, representation, CP3 posture, or human finalization;
- a target reference cannot reconstruct authorization-resource/effect-subject separation or existence posture;
- caller target time cannot reconstruct trusted evaluation/effect time;
- an unbound payload cannot reconstruct the effect-intent digest;
- a scope string cannot reconstruct scope proof;
- mutable basis references cannot reconstruct the authority-evaluation snapshot;
- free-text purpose cannot reconstruct a purpose token;
- free-text conditions cannot be presumed satisfied; and
- untyped evidence refs cannot reconstruct an eligibility disposition.

### 19.3 Source migration

Migration creates a new v0.2 source record and preserves a provenance link to the v0.1 record. A steward must explicitly decide:

- the exact authority-family tokens;
- closed delegation permission and any delegated action list;
- the purpose-token set, if any;
- how each legacy condition is preserved in supported closed constraints;
- every typed evidence-policy group, if required;
- authorization-resource/effect-subject narrowing; and
- whether the v0.1 source is retired, allowed to expire, or retained for the v0.1 evaluator only.

Automated migration may propose a mapping. It may not activate the new authority without steward approval.

### 19.4 Coexistence

Draft v0.2 contracts remain under `drafts_non_default/` and cannot become current/default by file presence. Runtimes must declare which bundle they evaluate. A deployment may support v0.1 and v0.2 concurrently, but each decision is bound to exactly one policy and schema bundle.

---

## 20. Stable reason codes

Lower rank wins within the outcome selected by section 15. Ranks are never compared across different outcomes.

| Reason code | Default outcome | Rank |
|---|---:|---:|
| `AUTHORIZED_BY_SELECTED_PATH` | `ALLOW` | 0 |
| `HUMAN_FINAL_ACTION_REQUIRED` | `REQUIRE_HUMAN_APPROVAL` | 100 |
| `AUTHORIZATION_SNAPSHOT_UNAVAILABLE` | `REQUIRE_REVIEW` | 200 |
| `POLICY_NOT_AVAILABLE` | `REQUIRE_REVIEW` | 210 |
| `POLICY_DIGEST_MISMATCH` | `REQUIRE_REVIEW` | 220 |
| `UNSUPPORTED_REVOCATION_NARROWING` | `REQUIRE_REVIEW` | 230 |
| `UNSUPPORTED_EVIDENCE_POLICY` | `REQUIRE_REVIEW` | 240 |
| `UNSUPPORTED_LEGACY_EVIDENCE_REQUIREMENT` | `REQUIRE_REVIEW` | 250 |
| `UNSUPPORTED_LEGACY_CONDITION` | `REQUIRE_REVIEW` | 260 |
| `UNSUPPORTED_LEGACY_PURPOSE` | `REQUIRE_REVIEW` | 270 |
| `OUTBOX_DISPATCH_REAUTH_REQUIRED` | `REQUIRE_REVIEW` | 280 |
| `REQUEST_SCHEMA_INVALID` | `DENY` | 1000 |
| `EFFECT_INTENT_SCHEMA_INVALID` | `DENY` | 1010 |
| `EFFECT_INTENT_DIGEST_MISMATCH` | `DENY` | 1020 |
| `UNKNOWN_ACTION_CLASS` | `DENY` | 1030 |
| `UNKNOWN_RESOURCE_KIND` | `DENY` | 1040 |
| `UNKNOWN_EFFECT_SUBJECT_KIND` | `DENY` | 1050 |
| `INVALID_EXISTENCE_POSTURE` | `DENY` | 1060 |
| `UNRESOLVED_PRINCIPAL` | `DENY` | 1070 |
| `REPRESENTATION_BASIS_INVALID` | `DENY` | 1080 |
| `CP3_EVIDENCE_MISSING` | `DENY` | 1090 |
| `CP3_AUTHORITY_SNAPSHOT_MISSING` | `DENY` | 1100 |
| `SOFTWARE_AGENT_NOT_PERMITTED` | `DENY` | 1110 |
| `PREFLIGHT_REQUIRED` | `DENY` | 1120 |
| `APPROVAL_EFFECT_INTENT_MISMATCH` | `DENY` | 1130 |
| `DECISION_EXPIRED` | `DENY` | 1140 |
| `DECISION_ALREADY_CONSUMED` | `DENY` | 1150 |
| `AUTHORITY_STATE_CHANGED_BEFORE_EFFECT` | `DENY` | 1160 |
| `TENANT_BOUNDARY_MISMATCH` | `DENY` | 1170 |
| `AUTHORIZATION_RESOURCE_NOT_PROVEN` | `DENY` | 1180 |
| `EFFECT_SUBJECT_NOT_PROVEN` | `DENY` | 1190 |
| `RESOURCE_KIND_MISMATCH` | `DENY` | 1200 |
| `SUBJECT_KIND_MISMATCH` | `DENY` | 1210 |
| `RESOURCE_REF_MISMATCH` | `DENY` | 1220 |
| `SUBJECT_REF_MISMATCH` | `DENY` | 1230 |
| `PACK_RELEASE_MISMATCH` | `DENY` | 1240 |
| `TWIN_MISMATCH` | `DENY` | 1250 |
| `SCOPE_NOT_PROVEN` | `DENY` | 1260 |
| `ACTIVE_REVOCATION` | `DENY` | 1270 |
| `AUTHORITY_NOT_ACTIVE_AT_AUTHORIZATION_TIME` | `DENY` | 1280 |
| `HISTORICAL_AUTHORITY_REQUIRED` | `DENY` | 1290 |
| `ROLE_ASSIGNMENT_NOT_APPLICABLE` | `DENY` | 1300 |
| `ROLE_ANCHOR_SCOPE_MISMATCH` | `DENY` | 1310 |
| `DELEGATION_PROHIBITED_BY_ACTION_RULE` | `DENY` | 1320 |
| `DELEGATION_NOT_PERMITTED_BY_SOURCE` | `DENY` | 1330 |
| `DELEGATION_SOURCE_MISSING` | `DENY` | 1340 |
| `DELEGATION_BROADENS_AUTHORITY` | `DENY` | 1350 |
| `DELEGATION_CYCLE` | `DENY` | 1360 |
| `DELEGATION_DEPTH_EXCEEDED` | `DENY` | 1370 |
| `SHARING_BASIS_MISMATCH` | `DENY` | 1380 |
| `ACTION_CLASS_NOT_GRANTED` | `DENY` | 1390 |
| `AUTHORITY_FAMILY_MISMATCH` | `DENY` | 1400 |
| `INHERITANCE_NOT_PERMITTED` | `DENY` | 1410 |
| `PURPOSE_REQUIRED` | `DENY` | 1420 |
| `PURPOSE_NOT_PERMITTED` | `DENY` | 1430 |
| `EVIDENCE_POLICY_REQUIRED` | `DENY` | 1440 |
| `REQUIRED_EVIDENCE_MISSING` | `DENY` | 1450 |
| `REQUIRED_EVIDENCE_INELIGIBLE` | `DENY` | 1460 |
| `NO_AUTHORITY_BASIS` | `DENY` | 1990 |

`DECISION_BUNDLE_PERSISTENCE_FAILED` is a runtime failure, not an authorization outcome, and therefore has no reason rank. A runtime must not fabricate a result record to place it in this table.

Problem severity is fixed by outcome: `ALLOW` is `INFO`, `REQUIRE_HUMAN_APPROVAL` and `REQUIRE_REVIEW` are `WARNING`, and `DENY` is `ERROR`. Diagnostic problems are ordered with the selected path first, then by path-type order, immutable source revision, numeric rank, and related reference. Severity never chooses the primary reason.

Additional codes require a versioned policy update. Implementations must not collapse a known authorization failure into an unstructured message or assign local ranks.

---

## 21. Invariants

The accepted design and conformance suite must preserve these invariants:

1. Omitting or changing optional AI-assistance metadata never increases authority.
2. Caller-supplied stage, family, principal kind, revocation posture, or authority time never controls the policy result.
3. A pre-revocation `subjectTime` never authorizes a post-revocation current effect.
4. Exactly one versioned action rule derives stage, family, inheritance ceiling, resource/subject policy, delegation ceiling, CP3 posture, human finalization, validity, and consumption mode.
5. Unknown action, family, resource kind, effect-subject kind, existence posture, condition, evidence policy, or proof type is non-`ALLOW`.
6. Principal resolution, represented Party, representation basis, CP3 posture, and human-finalization requirement remain separate axes.
7. Every software-agent path preserves the accepted CP3 posture and mandatory authority snapshot.
8. Human approval is valid only for the exact effect-intent digest, policy digest, authority snapshot, Party, and validity window.
9. Payload substitution, expired decisions, and replay of a single-use decision are non-`ALLOW`.
10. An existing authorization resource and a prospective effect subject are not conflated.
11. Pack release, installation, and activation-set identities are not interchangeable.
12. A role-targeted grant never exceeds either its grant scope or its role anchor scope.
13. A delegated path never exceeds the action-rule ceiling, source permission, source role anchor, or DelegationGrant at any dimension.
14. A purpose-constrained source cannot pass without an exact matching request purpose.
15. Caller-only purpose never creates source authority.
16. Free-text purpose and conditions are never guessed into executable v0.2 semantics.
17. Evidence requirements from the action rule and every selected source are cumulative.
18. Every required evidence ref and policy is bound to an immutable revision and evaluated under the named active policy.
19. Authorization-resource proof, effect-subject proof, scope proof, and constraint evidence remain typed and distinct.
20. `dataSovereigntyBoundaryRefs` contains only immutable revisions of actual sovereignty records.
21. A SharingGrant grants read/receive use only for its exact grantee and immutable artifact revision.
22. Every effective revocation is considered from a completeness-proven snapshot and watermark.
23. Partial grant paths are not unioned into a fabricated complete path.
24. Every path receives one disposition and mixed paths aggregate under one total lattice.
25. A failed non-selected path never supplies the primary reason for an `ALLOW` result.
26. The same immutable effect intent, authority snapshot, policy bytes, and basis revisions produce the same path dispositions, outcome, selected basis, ordered problems, and primary reason code.
27. Internal effect and decision evidence commit in one serializable transaction; neither precedes the other in a separate committed transaction.
28. External dispatch sends only the committed content-addressed outbox intent and observes dispatch-time revalidation policy.
29. A typed refusal never claims a durable trace that did not commit.
30. Every reconstructed decision resolves the same immutable basis and policy bytes visible at its recorded snapshot.
31. v0.1 records never silently claim v0.2 proof strength.
32. Draft schema presence never changes current/default status.

---

## 22. Production-reachable hostile cases

The future executable conformance suite must include at least:

| Case | Required disposition |
|---|---|
| Same request retried after omitting `aiAssistance.assisted: true` | same resolved principal, CP3 posture, and no authority increase |
| Caller changes `nonHumanActor` or derived family/stage hint | hint ignored or schema-rejected; policy result unchanged |
| Authority is revoked, then a current request supplies a pre-revocation `subjectTime` | current effect is `DENY`; subject time never replaces trusted current time |
| Natural person acts for an organization without a valid immutable representation basis | `DENY` |
| Organization-held grant is evaluated against the authenticated natural person rather than `authoritySubjectPartyRef` | conformance failure |
| Software agent omits the mandatory CP3 authority snapshot | `DENY` |
| Sponsor-bound agent attempts a human-only review decision | non-`ALLOW` |
| Agent requests a preflight-only read without valid preflight/qualification evidence | `DENY` |
| AI-assisted high-risk assertion has no fresh human approval for the exact effect-intent digest | `REQUIRE_HUMAN_APPROVAL` |
| Approval covers payload A but the protected operation substitutes payload B | digest mismatch; `DENY` and no effect |
| A single-use decision is consumed twice with the same payload | second consumption is `DENY` |
| A decision is consumed after `decisionValidUntil` | `DENY` |
| Revocation commits between evaluation and an internal governed write | serialization/revalidation failure; no effect |
| Revocation watermark changes before external dispatch | dispatch pauses and fresh authorization is required where policy requires current dispatch authority |
| Grant purpose is `REGULATORY_FILING` and request purpose is `regulatory_filing` | exact mismatch; non-`ALLOW` |
| Request supplies a purpose but source does not authorize it | caller-only purpose creates no authority |
| v0.1 source contains a non-empty free-text condition | `REQUIRE_REVIEW` with `UNSUPPORTED_LEGACY_CONDITION` |
| Action rule permits delegation but the source is `NOT_DELEGABLE` | `DENY` |
| Source permits delegation but the action rule is `DELEGATION_PROHIBITED` | `DENY` |
| Explicit-source row receives only blanket `DELEGABLE_GRANTED_ACTIONS` | `DENY` |
| Direct AuthorityGrant evidence requirement lacks a paired policy | schema rejection or `DENY` |
| SharingGrant evidence requirement lacks a paired policy | schema rejection or `DENY` |
| Action-rule and source evidence requirements differ | both are enforced cumulatively |
| Required evidence ref is absent | `DENY` |
| Evidence resolves to the wrong family | `DENY` |
| Evidence is stale, disputed, or superseded under policy | `DENY` |
| Evidence belongs to another tenant | `DENY` |
| Role-targeted grant scope covers the subject but role anchor does not | `DENY` |
| Delegated source is role-targeted and its role anchor does not cover the resource/subject | `DENY` |
| Prospective observation is rejected merely because it does not already exist | conformance failure; prospective proof rules apply |
| Existing-only subject does not exist | `DENY` |
| Pack install intent names one release digest and dispatch substitutes another | `DENY` and no dispatch |
| Pack activation-set identifier is substituted for the installed pack release | `DENY` |
| Authorization resource exists but has the wrong resource kind | `DENY` |
| Scope string matches but no trusted scope proof exists | `DENY` |
| Authorization-resource proof is placed in `dataSovereigntyBoundaryRefs` | schema or semantic rejection |
| Scope proof is substituted into `constraintEvidenceRefs` | schema or semantic rejection |
| Policy version matches but digest differs | non-`ALLOW` |
| Active `TERMINATE` revocation is omitted from caller candidates | revocation still found; `DENY` |
| Active v0.1 narrowing revocation is present | `REQUIRE_REVIEW` until closed semantics exist |
| SharingGrant artifact family/ref/revision differs from the authorization resource | `DENY` |
| SharingGrant is offered for a write or review action | basis ineligible |
| One grant supplies action and another supplies matching purpose | paths remain incomplete; non-`ALLOW` |
| One path lacks only human approval, one has an unsupported condition, and one is revoked | `REQUIRE_HUMAN_APPROVAL`; selected human path supplies the primary reason |
| One path allows and another is revoked | `ALLOW`; `AUTHORIZED_BY_SELECTED_PATH` is primary and revocation remains diagnostic |
| No path allows; one requires review and all others deny | `REQUIRE_REVIEW` with the selected review path's lowest rank |
| Logical grant ID resolves to a successor after the decision | reconstruction still resolves the recorded immutable predecessor revision |
| Revocation index contents change after the decision | reconstruction uses the recorded snapshot/watermark |
| Policy digest is recorded but the exact bytes are unavailable | reconstructibility conformance failure |
| Refusal trace insert is rolled back with a thrown transport error | conformance failure |
| Decision-bundle persistence fails | no effect and no false durable-decision claim |
| Internal decision commits before a later effect transaction | conformance failure because the TOCTOU gap is observable |
| External dispatcher sends bytes that differ from the committed outbox digest | conformance failure |
| Draft v0.2 files exist but currentness still names v0.1 | v0.1 remains current/default |

Fixtures must enter through production-reachable evaluator and persistence paths. Unit-only helper tests are not enough for a conformance claim.

---

## 23. Traceability to the triggering reviews

| Review blocker | Canonical disposition proposed here |
|---|---|
| Optional AI-assistance omission/retry bypass | sections 6 and 21 |
| Role-targeted grant can escape role anchor scope | sections 9 and 10 |
| Purpose, conditions, limits, evidence, and authority-family comparison are undefined | sections 7, 11, and 12 |
| Narrowing revocations are under-specified | section 14 |
| Target kind/ref proof is conflated with scope proof | section 8 |
| v0.1 trace cannot carry the claimed policy and proof basis | sections 16 and 17 |
| `RECEIVE_READ_DATA` omits SharingGrant composition | section 13 |
| Refusal trace can roll back with a typed error | section 18 |
| Proposed lineage inheritance expands the accepted matrix | section 7 retains D/X/N and proposes no lineage rows |
| Caller `targetTime` permits backdated authorization | sections 8.1, 9, 14, and 18 |
| Decision is not bound to exact effect and creates a TOCTOU race | sections 8.2, 17, and 18 |
| Actor posture is overloaded and conflicts with CP3 | sections 6 and 7 preserve separate axes and exact CP3 values |
| Delegation and evidence constraints are not encodable | sections 10, 12, and 17.3 |
| Target model cannot represent prospective creation/installation | sections 7 and 8 separate resource, subject, and existence posture |
| Mixed-path outcome and reason selection is incomplete | sections 15 and 20 |
| Logical refs and one policy digest do not guarantee reconstruction | sections 16, 17, and 18.5 |
| Header reverses dependency direction | header now says `Triggered by` and explicitly `Blocks` OFARM2 work |

This table does not authorize an OFARM2 fix. OFARM2 must wait for accepted semantics, promoted contracts, and byte-identical extraction.

---

## 24. Staged delivery and currentness

The required sequence is:

1. **Phase A candidate:** this document only; no authority or currentness effect.
2. **Semantic approval:** stewards approve or amend the approval card in section 25.
3. **Accepted RFC and action matrix:** a separate governed PR promotes approved prose and an exact v0.2 matrix.
4. **Draft/non-default contracts:** a separate PR adds source, authority-snapshot, decision, consumption, and effect-receipt v0.2 schemas, examples, and validation without currentness promotion.
5. **Hostile conformance:** a separate PR adds executable production-reachable cases and publishes the result.
6. **Explicit promotion:** after hostile review and steward approval, a separate PR changes current/default indexes and generated navigation.
7. **OFARM2 extraction:** promoted canonical assets are copied byte-for-byte and verified by digest.
8. **OFARM2 implementation:** only then may `OFARM2#359` resume against the promoted policy and contracts.

No step is implied by completion of the prior step. CP15 human governance applies to current/default promotion.

---

## 25. Steward approval card

Before accepted-law work begins, stewards should record explicit decisions for all items:

| Decision | Proposed answer | Approval required |
|---|---|---|
| Are principal resolution, CP3 posture, and human finalization separate axes while AI disclosure stays non-authoritative? | yes | yes |
| Does the authorization RFC preserve all five accepted CP3 posture values without editing CP3 semantics? | yes | yes |
| Must organization representation record the natural-person principal, represented Party, and immutable representation basis separately? | yes | yes |
| Are action stage and authority family policy-derived rather than caller-selected? | yes | yes |
| Is the exact matrix in section 7 the v0.2 closure, including delegation, CP3 posture, resources, subjects, and existence postures? | yes | yes, row-by-row amendments allowed |
| Is `OUTPUT_FILE_SUBMISSION_ASSEMBLY` fixed to `ATTEST_SIGN`? | yes | yes |
| Are no existing actions granted lineage inheritance? | yes | yes |
| Is current authority always checked at trusted evaluation/effect time, with historical subject-time authority only as a second rule? | yes | yes |
| Must every decision and human approval bind the exact JCS/SHA-256 effect-intent digest? | yes | yes |
| Are state-affecting decisions single-use with policy-bounded expiry? | yes | yes |
| Must internal effects and decision evidence commit in one serializable transaction? | yes | yes |
| Must external effects use a digest-bound idempotent outbox and dispatch receipt? | yes | yes |
| Are purpose tokens exact-match and optional only when the source is unrestricted? | yes | yes |
| Must legacy free-text purpose be explicitly migrated? | yes | yes |
| Are free-text conditions unsupported and fail-closed? | yes | yes |
| Must action-rule and all applicable source evidence requirements be cumulative and name immutable active policy revisions? | yes | yes |
| Are role-targeted source paths capped by role anchor scopes? | yes | yes |
| Are delegation ceilings and source permissions closed tokens whose intersection controls every delegated path? | yes | yes |
| Is default delegation depth one hop? | yes | yes |
| Are v0.1 narrowing revocations non-`ALLOW` until separately closed? | yes | yes |
| Is SharingGrant an exact-artifact access basis only for `RECEIVE_READ_DATA`? | yes | yes |
| Must authorization-resource, effect-subject, scope, evidence, and sovereignty proof use separate typed fields? | yes | yes |
| Must every result bind retrievable immutable policy bytes and an authority-evaluation snapshot? | yes | yes |
| Is the total path aggregation lattice and numeric reason table in sections 15 and 20 accepted? | yes | yes |
| Is the decision-bundle digest exactly the JCS/SHA-256 projection in section 18.5? | yes | yes |
| Must non-`ALLOW` bundles commit before transport errors are returned? | yes | yes |
| Does honest v0.2 require versioned source, snapshot, decision, consumption, and effect-receipt records? | yes | yes |
| Does current/default promotion remain a separate final step? | yes | yes |

Any amendment must state whether it changes only this authorization boundary. A requested authentication, principal-resolution, key-custody, database, or runtime-integration change must be split.

---

## 26. Completion criteria for Phase A

Phase A is complete when:

- this candidate is reviewed against issue `samovers/OFARM#10`;
- every acceptance criterion has a proposed disposition;
- the source-record versioning decision is explicit;
- the CP3 compatibility mapping is accepted without changing CP3 semantics, or a separate stacked change is named;
- the action matrix and resource/subject/existence closure are reviewed;
- the temporal, effect-intent, replay, atomic-effect, aggregation, and reconstruction rules are reviewed;
- migration and currentness rules are accepted or amended;
- hostile cases are judged sufficient to detect proof substitution and fail-open behavior;
- the trust boundary remains authorization law and machine-contract governance; and
- no active authority or schema was changed by the candidate PR.

What is next: steward review and explicit semantic approval before any accepted-RFC or machine-contract edit.
