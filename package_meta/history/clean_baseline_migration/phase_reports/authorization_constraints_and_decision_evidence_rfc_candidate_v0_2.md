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
2. the action class selects every policy-derived field from one immutable rule, including authority family, stage, inheritance/delegation ceilings, named composite resources, effect subject, exact effect-intent schema binding, evidence, validity, historical-authority, dispatch, agent, approval, and consumption posture;
3. purpose is a closed, exact-match use constraint in v0.2, not a comparison between unrelated free-text fields;
4. untyped or unsupported conditions never evaluate to true;
5. required evidence is usable only under an active evidence-eligibility policy;
6. authorization-resource proof, effect-subject proof, scope proof, role scope, grant scope, delegation source, sharing basis, and revocation posture are independently evaluated and durably recorded;
7. the exact effect intent, trusted evaluation time, current authority snapshot, validity window, consumption mode, and challenge-based human approval are cryptographically bound and consumed under one lifecycle;
8. ingress rejection, request/result/trace evidence, internal writes, governed reads, external dispatch, and non-`ALLOW` persistence form reconstructible fail-closed protocols with deterministic mixed-path outcomes and an exact digest projection; and
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
- no immutable action rule selects an exact operation-specific effect-intent schema, composite resource policy, evidence profile, historical posture, or dispatch posture;
- v0.1 actor fields do not separately identify the authenticated principal, represented Party, representation basis, CP3 action posture, and human-finalization requirement;
- current CP3 does not establish one global software-agent authority subject, because valid grant/delegation subjects can differ by candidate path;
- fresh human approval has no governed challenge, display, final-snapshot, separation, expiry, or atomic-consumption contract;
- actual governed reads lack a same-snapshot authorization/retrieval/qualification/payload-evidence protocol, while preflight-only cannot truthfully authorize disclosure;
- schema-invalid input cannot truthfully become a validated authorization refusal bundle;
- external dispatch and decision-bundle digest projection lack exact expiry/recheck and JSON Pointer rules;
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
- the governing effect-intent schema or schema digest;
- named resource composition/cardinality;
- whether revocation is checked;
- whether the authenticated principal is a natural person or software agent;
- the actor's accountable sponsor;
- the authorization resource's governed kind or the effect subject's existence posture;
- the scope relationship;
- the policy version; or
- decision validity, historical-authority, dispatch, approval, or consumption posture; or
- whether evidence is required, current, and eligible.

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
- `representationBasisRef` and immutable revision, when representation applies.

An organization reference alone never proves a natural-person final action. For a natural person acting for an organization, `representedPartyRef` and `representationBasisRef` are mandatory.

For a software agent, `authenticatedPrincipalRef` identifies the executing agent instance. A sponsor reference is accountability evidence and is never an authority subject by itself. A model, tool, API key, prompt, session, public-operation descriptor, or caller boolean is not an authority-bearing principal.

`UNRESOLVED` is always non-`ALLOW`.

### 6.2 Path-specific authority subject

Authority subject is evaluated per candidate path, after trusted principal resolution. Every path records one `authoritySubjectBasis`:

- `NATURAL_PERSON_SELF`
- `REPRESENTED_PARTY_AUTHORIZED_REPRESENTATION`
- `AGENT_PARTY_DIRECT_GRANT`
- `REPRESENTED_PARTY_EXPLICIT_DELEGATION`

Every path also records `authoritySubjectPartyRef` and immutable `authoritySubjectBasisRefs`.

`NATURAL_PERSON_SELF` binds the authenticated natural person's Party revision to a direct Party or role-targeted source.

`REPRESENTED_PARTY_AUTHORIZED_REPRESENTATION` binds the authenticated natural person, represented Party, immutable representation basis, and source authority.

`AGENT_PARTY_DIRECT_GRANT` binds the recognized agent Party/identity, active CP3 actorship evidence, and immutable direct grant or role-targeted grant revision.

`REPRESENTED_PARTY_EXPLICIT_DELEGATION` binds the agent, CP3 actorship evidence, represented Party, immutable DelegationGrant, and immutable source authority. The sponsor is recorded but cannot substitute for the delegation or source grant.

When candidate paths imply different authority subjects, each subject/path is evaluated independently. No global pre-path `authoritySubjectPartyRef` is injected, and partial paths for different subjects cannot be combined.

Current CP3 contracts remain sufficient as actorship inputs because the authority subject is derived from the immutable grant/delegation path, not from a new envelope field. If later implementation evidence requires a CP3 envelope field, that is a separate stacked CP3 contract version.

### 6.3 Accepted CP3 `AgentActionPosture` axis

Every software-agent action uses one exact posture already accepted by `OFARM_Agent_Actorship_and_Authority_RFC_v0_1.md`:

- `AGENT_ALLOWED_WITH_POLICY_CHECK`
- `AGENT_ALLOWED_WITH_PREFLIGHT_ONLY`
- `AGENT_ALLOWED_WITH_HUMAN_APPROVAL`
- `HUMAN_ONLY`
- `PROHIBITED_FOR_AGENT`

This candidate does not rename, collapse, or reinterpret those values.

`AGENT_ALLOWED_WITH_POLICY_CHECK` permits a sponsor-bound agent to perform the action only after the complete v0.2 authorization policy passes.

`AGENT_ALLOWED_WITH_PREFLIGHT_ONLY` permits only a non-authoritative preflight or dry-run surface. It never authorizes the protected action, data disclosure, state change, or final output. A separate protected action must use another posture and a fresh authorization decision.

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

### 6.4 Human-finalization axis

The separate `humanFinalizationRequirement` is one of:

- `NOT_REQUIRED`
- `FRESH_HUMAN_APPROVAL_REQUIRED`
- `DIRECT_HUMAN_ACTION_REQUIRED`

`FRESH_HUMAN_APPROVAL_REQUIRED` requires a trusted natural-person approval record bound to:

- the action class;
- the action-rule-selected effect-intent schema ref/digest and `effectIntentDigest`;
- the authorization-resource and effect-subject identities;
- the policy digest;
- `authorityEvaluationSnapshotRef`;
- `decisionValidUntil`; and
- the represented Party and representation basis, when applicable.

`DIRECT_HUMAN_ACTION_REQUIRED` requires the authenticated direct principal for the protected action to be a natural person. A sponsor approval of an agent request does not convert an agent into the direct human actor.

Approval for a different digest, policy, snapshot, Party, or validity window is not reusable.

For `FRESH_HUMAN_APPROVAL_REQUIRED`, the action rule also selects exactly one `approvalSeparationPolicy`:

- `SELF_APPROVAL_ALLOWED`
- `DISTINCT_APPROVER_REQUIRED`

A direct natural-person invocation may satisfy the fresh-approval requirement only through the governed challenge/approval lifecycle in section 18 and only when `SELF_APPROVAL_ALLOWED`. `DIRECT_HUMAN_ACTION_REQUIRED` is satisfied by the authenticated natural person performing the exact protected action; it does not require a separate approver unless a stronger action rule says so.

### 6.5 AI-assistance disclosure

AI-assistance metadata is provenance only. It has exactly these decision-trace dispositions:

- `DISCLOSED_ASSISTED`
- `DISCLOSED_NOT_ASSISTED`
- `NOT_DISCLOSED_OR_UNKNOWN`

Changing, omitting, or retrying optional AI-assistance metadata must not change principal resolution, CP3 posture, human-finalization requirements, authority basis, or outcome.

### 6.6 Compatibility boundary

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

| Action class | Authority family | Stage | Inheritance | Delegation | Agent posture | Human finalization | Resource requirement policy | Effect subject / existence |
|---|---|---|---|---|---|---|---|---|
| `OBSERVE_CREATE_OBSERVATION` | `OBSERVE_REPORT` | `DRAFT_PREPARATION` | D | DA | PC | NR | `RP_SCOPE_ONE` | `OBSERVATION` / P |
| `OBSERVE_ATTACH_EVIDENCE` | `OBSERVE_REPORT` | `DRAFT_PREPARATION` | D | DA | PC | NR | `RP_RECORD_ONE` | `EVIDENCE_LINK` / P |
| `ASSERT_STRUCTURE` | `ASSERT_SUBMIT` | `DRAFT_PREPARATION` | X | DX | HA | FA | `RP_SCOPE_ONE` | `STRUCTURE_ASSERTION` / P |
| `ASSERT_OPERATION_CLAIM` | `ASSERT_SUBMIT` | `DRAFT_PREPARATION` | D | DA | PC | NR | `RP_SCOPE_ONE` | `OPERATION_ASSERTION` / P |
| `ASSERT_COMPLIANCE` | `ASSERT_SUBMIT` | `DRAFT_PREPARATION` | X | DX | HA | FA | `RP_SCOPE_ONE` | `COMPLIANCE_ASSERTION` / P |
| `OPERATE_PLAN_INTERVENTION` | `OPERATE_INTERVENE` | `DRAFT_PREPARATION` | D | DA | PC | NR | `RP_SCOPE_ONE` | `INTERVENTION_PLAN` / P |
| `OPERATE_REPORT_EXECUTION` | `OPERATE_INTERVENE` | `DRAFT_PREPARATION` | D | DA | PC | NR | `RP_SCOPE_ONE` | `EXECUTION_REPORT` / P |
| `REVIEW_REQUEST` | `REVIEW` | `DRAFT_PREPARATION` | X | DA | PC | NR | `RP_RECORD_ONE` | `REVIEW_REQUEST` / P |
| `REVIEW_ACCEPT` | `GOVERN_DECIDE` | `PROMOTION` | N | DP | HU | DH | `RP_RECORD_ONE` | `REVIEW_DECISION` / P |
| `REVIEW_REJECT_OR_CONTEST` | `GOVERN_DECIDE` | `PROMOTION` | N | DP | HU | DH | `RP_RECORD_ONE` | `REVIEW_DECISION` / P |
| `REVIEW_SUPERSEDE` | `GOVERN_DECIDE` | `PROMOTION` | N | DP | HU | DH | `RP_RECORD_ONE` | `REVIEW_DECISION` / P |
| `CONTEXT_INSTALL_PACK` | `CONTEXT_GOVERNANCE` | `CONTEXT_ACTIVATION` | N | DP | HU | DH | `RP_PACK_INSTALL` | `PACK_INSTALLATION` / P |
| `CONTEXT_ACTIVATE_PACK` | `CONTEXT_GOVERNANCE` | `CONTEXT_ACTIVATION` | N | DP | HU | DH | `RP_PACK_ACTIVATE` | `PACK_ACTIVATION_SET` / P |
| `CONTEXT_DEACTIVATE_PACK` | `CONTEXT_GOVERNANCE` | `CONTEXT_ACTIVATION` | N | DP | HU | DH | `RP_PACK_DEACTIVATE` | `PACK_ACTIVATION_SET` / E |
| `OUTPUT_APPROVE_DOCUMENT_ASSEMBLY` | `ATTEST_SIGN` | `PUBLICATION` | N | DP | HU | DH | `RP_ASSEMBLY_ONE` | `ASSEMBLY_APPROVAL` / P |
| `OUTPUT_ATTEST_DOCUMENT_ASSEMBLY` | `ATTEST_SIGN` | `ATTESTATION` | N | DP | HU | DH | `RP_ASSEMBLY_ONE` | `ASSEMBLY_ATTESTATION` / P |
| `OUTPUT_FILE_SUBMISSION_ASSEMBLY` | `ATTEST_SIGN` | `PUBLICATION` | N | DX | HU | DH | `RP_SUBMISSION_ONE` | `SUBMISSION_FILING` / P |
| `SHARE_GRANT_ACCESS` | `SHARE_REVOKE` | `PROMOTION` | X | DA | HA | FA | `RP_SHARED_ARTIFACT_ONE` | `SHARING_GRANT` / P |
| `SHARE_REVOKE_ACCESS` | `SHARE_REVOKE` | `PROMOTION` | X | DA | HA | FA | `RP_SHARED_ARTIFACT_ONE` | `SHARING_GRANT` / E |
| `RECEIVE_READ_DATA` | `RECEIVE_USE` | `QUERY_READ` | D | DA | PC | NR | `RP_DATA_RESOURCE_ONE` | `DATA_DISCLOSURE` / P |

### 7.3 Matrix rules

The inheritance entry is a ceiling, not a grant. A source record may narrow `D` to `X` or `N`, and may narrow `X` to `N`. It may not broaden the row. A row marked `N` must use `NO_INHERIT`.

The delegation entry is also a ceiling. Its intersection with source permission and the DelegationGrant is defined in section 10. Prose such as "with caution" has no executable meaning in v0.2.

All 20 proposed v0.2 rows use `SINGLE_USE`. No default row authorizes replay. Section 18 defines the only future-compatible replay posture and prevents a runtime from inventing local replay behavior.

Each `resourceRequirementPolicy` names the pre-existing governed objects against which authority is checked. `effectSubject` is the object acted on or created. They are not aliases. Sections 7.5 and 8 define both.

For `CONTEXT_INSTALL_PACK`, the effect intent must additionally bind an existing content-addressed `PACK_RELEASE` or `PACK_ARTIFACT`; `PACK_INSTALLATION` is the prospective result. For activation, every requested pack release is an immutable effect-intent input and `PACK_ACTIVATION_SET` is the proposed governed result. For deactivation, the existing activation set is the effect subject and the effect intent binds its proposed successor state.

For `ASSERT_COMPLIANCE`, compiled outputs may be immutable evidence or effect-intent inputs, but the effect subject is the prospective compliance assertion. A runtime must not substitute a compiled-output reference for the assertion body covered by `effectIntentDigest`.

`OUTPUT_FILE_SUBMISSION_ASSEMBLY` resolves the v0.1 alternative family to `ATTEST_SIGN` for v0.2. A deployment that needs a distinct non-attesting transmission action must propose a separate action class rather than reinterpret this one locally.

Unknown action classes, resource kinds, effect-subject kinds, existence postures, stages, or policy rules are non-`ALLOW`.

The resource/subject list is a proposed closure point and requires specific steward approval. It must not be inferred from the word "typical" in the v0.1 matrix.

### 7.4 Complete `ActionAuthorizationRule`

The core row and its extension row form one immutable `ActionAuthorizationRule`. Every rule must carry:

- `ruleId`;
- action class, authority family, and stage;
- inheritance ceiling and delegation ceiling;
- exact CP3 agent-action posture and human-finalization requirement;
- immutable `humanApprovalPolicy` where human approval applies, including display profile, approver eligibility, separation, challenge maximum age, approval maximum age, and single-use posture;
- `resourceRequirementPolicy` with named roles, cardinality, and composition;
- effect-subject kind and existence posture;
- one closed `effectIntentSchemaBinding`;
- `decisionValidityPolicy`, including policy ref/digest, exact maximum age, cutoff inputs, and calculation;
- `historicalAuthorityPosture`;
- `externalEffectPosture`;
- exact action-level evidence-policy bindings, including explicit `NONE`;
- `consumptionMode`; and
- immutable rule revision and content digest.

`effectIntentSchemaBinding` contains exactly:

- content-addressed `schemaRef`;
- `schemaVersion`;
- `schemaDigest`;
- `canonicalization`, fixed to `JCS_RFC8785_SHA256`; and
- one effect-intent profile ID from section 7.6.

The caller submits an effect-intent instance. The selected action rule chooses the schema. A caller schema claim, if present for diagnostics, is non-authoritative and must exactly equal the rule binding. A mismatch is an ingress rejection; a caller can never select a weaker schema.

Phase A names the exact semantic profiles. Before accepted-RFC/action-matrix promotion, the draft-schema stage must materialize their bytes and produce a reviewed binding manifest containing every content-addressed ref and digest. Missing, placeholder, mutable, or mismatched bindings make the action rule invalid and non-executable. Accepted promotion cannot precede that manifest.

The profile IDs in sections 7.5 through 7.8 are review keys, not runtime indirection. The binding manifest maps each action class to exactly one complete resolved rule containing the actual schema/policy refs and digests, and the accepted action-rule bundle digest covers those resolved values. A runtime cannot follow a mutable registry entry or choose among schemas sharing a profile ID.

Every v0.2 row selects `TRANSACTION_BOUND_30S_V0_2`. That policy fixes `maxDecisionAge` to ISO 8601 duration `PT30S`, uses the exact minimum function in section 18.2, and requires consumption in the same governed transaction as the protected effect, read-evidence commit, or outbox commit. A future row may choose another immutable validity policy only through a reviewed matrix version.

Every `SA` row selects `FRESH_APPROVAL_SELF_5M_V0_2`: `SELF_APPROVAL_ALLOWED`, `challengeMaxAge` `PT5M`, `approvalMaxAge` `PT5M`, and `SINGLE_USE`. `challengeExpiresAt` is the earlier of challenge issue time plus `PT5M` and every challenge-snapshot authority/policy/resource/evidence cutoff. `approvalExpiresAt` is the earlier of `humanActedAt + PT5M`, `challengeExpiresAt`, and every final-snapshot cutoff. `NA` binds explicit `NO_SEPARATE_APPROVAL_POLICY`; it does not weaken a row's independent `DIRECT_HUMAN_ACTION_REQUIRED` posture. A future distinct-approver row must bind a new immutable policy profile with exact eligible roles and prohibited relationships.

### 7.5 Resource requirement policies

Every request carries `authorizationResources`, an array. Each rule selects one policy below. `ALL_OF` requires every named role at its cardinality. `ONE_OF` requires exactly one allowed branch and prohibits a second branch.

| Policy ID | Composition | Named requirements |
|---|---|---|
| `RP_SCOPE_ONE` | `ALL_OF` | `TARGET_SCOPE`: exactly 1 `GOVERNED_SCOPE` |
| `RP_RECORD_ONE` | `ALL_OF` | `PRIMARY_RECORD`: exactly 1 `GOVERNED_RECORD` |
| `RP_PACK_INSTALL` | `ALL_OF` | `TARGET_SCOPE`: exactly 1 `GOVERNED_SCOPE`; `PACK_REGISTRY`: exactly 1 `PACK_REGISTRY`; `PACK_RELEASE_INPUT`: exactly 1 `PACK_RELEASE` or `PACK_ARTIFACT` |
| `RP_PACK_ACTIVATE` | `ALL_OF` | `TARGET_SCOPE`: exactly 1 `GOVERNED_SCOPE`; `PACK_REGISTRY`: exactly 1 `PACK_REGISTRY`; `PACK_RELEASE_INPUTS`: 1 or more `PACK_RELEASE` or `PACK_ARTIFACT` |
| `RP_PACK_DEACTIVATE` | `ALL_OF` | `TARGET_SCOPE`: exactly 1 `GOVERNED_SCOPE`; `PACK_REGISTRY`: exactly 1 `PACK_REGISTRY`; `CURRENT_ACTIVATION_SET`: exactly 1 `PACK_ACTIVATION_SET` |
| `RP_ASSEMBLY_ONE` | `ONE_OF` | `PRIMARY_ASSEMBLY`: exactly 1 `DOCUMENT_ASSEMBLY`; or `PRIMARY_DOSSIER`: exactly 1 `DOSSIER_ASSEMBLY` |
| `RP_SUBMISSION_ONE` | `ALL_OF` | `PRIMARY_SUBMISSION`: exactly 1 `SUBMISSION_ASSEMBLY` |
| `RP_SHARED_ARTIFACT_ONE` | `ALL_OF` | `SHARED_ARTIFACT`: exactly 1 `SHARED_ARTIFACT` |
| `RP_DATA_RESOURCE_ONE` | `ALL_OF` | `DATA_RESOURCE`: exactly 1 `DATA_RESOURCE` |

Every resource instance binds kind, logical ref, immutable revision/digest, scope, twin, tenant, and proof. An unrecognized role, missing role, excess cardinality, or `ONE_OF` ambiguity is non-`ALLOW`.

### 7.6 Effect-intent schema profiles

The profile lists the minimum authorization-relevant fields that its immutable schema must require. The schema may add governed fields, but a later schema revision that adds, removes, or changes an authorization-relevant field needs a new digest and reviewed rule binding.

| Profile ID | Required authorization-relevant content |
|---|---|
| `EI_OBSERVATION_CREATE_V0_2` | scope/resource revisions, proposed observation ID, observation type/body, subject time, evidence revision refs |
| `EI_EVIDENCE_LINK_V0_2` | governed-record revision, evidence revision, relation type, subject time |
| `EI_STRUCTURE_ASSERTION_V0_2` | scope revision, proposed assertion ID, assertion body, subject time, evidence revisions |
| `EI_OPERATION_ASSERTION_V0_2` | scope/operation revisions, proposed assertion ID, claim body, subject time, evidence revisions |
| `EI_COMPLIANCE_ASSERTION_V0_2` | scope revision, proposed assertion ID, exact claim body, rule/evidence-policy revisions, evidence revisions, subject time |
| `EI_INTERVENTION_PLAN_V0_2` | scope revisions, proposed plan ID/body, intended time, governed inputs |
| `EI_EXECUTION_REPORT_V0_2` | scope, plan/operation revisions, proposed report ID/body, execution time, evidence revisions |
| `EI_REVIEW_REQUEST_V0_2` | governed-record revision, proposed request ID, review scope, reason, evidence revisions |
| `EI_REVIEW_DECISION_V0_2` | governed-record revision, proposed decision ID, decision kind fixed by action class, rationale, evidence revisions |
| `EI_PACK_INSTALL_V0_2` | scope and registry revisions, exact pack-release ref/digest, installation parameters, requested profiles, exclusions |
| `EI_PACK_ACTIVATE_V0_2` | scope and registry revisions, every pack-release ref/digest, profiles, exclusions, complete proposed activation-set content |
| `EI_PACK_DEACTIVATE_V0_2` | scope, registry, and current activation-set revisions, deactivation selection, complete proposed successor content |
| `EI_ASSEMBLY_APPROVAL_V0_2` | assembly/dossier revision, output profile, approval scope, evidence revisions |
| `EI_ASSEMBLY_ATTESTATION_V0_2` | assembly/dossier revision, attestation statement, signature policy, evidence revisions |
| `EI_SUBMISSION_FILING_V0_2` | submission revision, exact destination, filing mode, payload digest, external identifiers, evidence revisions |
| `EI_SHARING_GRANT_V0_2` | immutable artifact revision, exact grantee, rights, delivery mode, purpose, validity, scope, sovereignty revisions |
| `EI_SHARING_REVOKE_V0_2` | immutable SharingGrant and artifact revisions, effective time, revocation scope/reason |
| `EI_DATA_READ_V0_2` | immutable resource revision or QuerySpecification/plan revisions, projection, redaction-policy revision, purpose, response/stream mode, snapshot policy |

### 7.7 Action-level evidence policy profiles

Each evidence profile is itself an immutable policy binding in the final action rule. `EP_NONE` is an explicit empty requirement, not a missing field. Source-record evidence groups remain cumulative.

- `EP_NONE`
- `EP_EVIDENCE_LINK_ELIGIBILITY_V0_2`
- `EP_COMPLIANCE_ASSERTION_V0_2`
- `EP_EXECUTION_REPORT_V0_2`
- `EP_PACK_GOVERNANCE_V0_2`
- `EP_OUTPUT_APPROVAL_V0_2`
- `EP_ATTESTATION_V0_2`
- `EP_FORMAL_FILING_V0_2`
- `EP_SHARING_SOVEREIGNTY_V0_2`
- `EP_CP2_READ_QUALIFICATION_V0_2`

Every non-`NONE` profile must have a content-addressed policy ref/digest in the binding manifest before accepted promotion.

### 7.8 Closed rule-extension matrix

Validity `TX` means the exact `TRANSACTION_BOUND_30S_V0_2` policy in sections 7.4 and 18.2. Historical posture `C` means `CURRENT_ONLY`; `CS` means `CURRENT_AND_SUBJECT_TIME`. External posture `N` means `NO_EXTERNAL_DISPATCH`; `DC` means `DISPATCH_CURRENT_AUTHORITY_REQUIRED`. Consumption `SU` means `SINGLE_USE`. Approval `SA` means `FRESH_APPROVAL_SELF_5M_V0_2`; `NA` means `NO_SEPARATE_APPROVAL_POLICY`.

| Action class | Intent profile | Resource policy | Validity | Historical | External | Evidence profile | Consumption | Approval |
|---|---|---|---|---|---|---|---|---|
| `OBSERVE_CREATE_OBSERVATION` | `EI_OBSERVATION_CREATE_V0_2` | `RP_SCOPE_ONE` | TX | C | N | `EP_NONE` | SU | NA |
| `OBSERVE_ATTACH_EVIDENCE` | `EI_EVIDENCE_LINK_V0_2` | `RP_RECORD_ONE` | TX | C | N | `EP_EVIDENCE_LINK_ELIGIBILITY_V0_2` | SU | NA |
| `ASSERT_STRUCTURE` | `EI_STRUCTURE_ASSERTION_V0_2` | `RP_SCOPE_ONE` | TX | C | N | `EP_NONE` | SU | SA |
| `ASSERT_OPERATION_CLAIM` | `EI_OPERATION_ASSERTION_V0_2` | `RP_SCOPE_ONE` | TX | CS | N | `EP_NONE` | SU | NA |
| `ASSERT_COMPLIANCE` | `EI_COMPLIANCE_ASSERTION_V0_2` | `RP_SCOPE_ONE` | TX | C | N | `EP_COMPLIANCE_ASSERTION_V0_2` | SU | SA |
| `OPERATE_PLAN_INTERVENTION` | `EI_INTERVENTION_PLAN_V0_2` | `RP_SCOPE_ONE` | TX | C | N | `EP_NONE` | SU | NA |
| `OPERATE_REPORT_EXECUTION` | `EI_EXECUTION_REPORT_V0_2` | `RP_SCOPE_ONE` | TX | CS | N | `EP_EXECUTION_REPORT_V0_2` | SU | NA |
| `REVIEW_REQUEST` | `EI_REVIEW_REQUEST_V0_2` | `RP_RECORD_ONE` | TX | C | N | `EP_NONE` | SU | NA |
| `REVIEW_ACCEPT` | `EI_REVIEW_DECISION_V0_2` | `RP_RECORD_ONE` | TX | C | N | `EP_NONE` | SU | NA |
| `REVIEW_REJECT_OR_CONTEST` | `EI_REVIEW_DECISION_V0_2` | `RP_RECORD_ONE` | TX | C | N | `EP_NONE` | SU | NA |
| `REVIEW_SUPERSEDE` | `EI_REVIEW_DECISION_V0_2` | `RP_RECORD_ONE` | TX | C | N | `EP_NONE` | SU | NA |
| `CONTEXT_INSTALL_PACK` | `EI_PACK_INSTALL_V0_2` | `RP_PACK_INSTALL` | TX | C | N | `EP_PACK_GOVERNANCE_V0_2` | SU | NA |
| `CONTEXT_ACTIVATE_PACK` | `EI_PACK_ACTIVATE_V0_2` | `RP_PACK_ACTIVATE` | TX | C | N | `EP_PACK_GOVERNANCE_V0_2` | SU | NA |
| `CONTEXT_DEACTIVATE_PACK` | `EI_PACK_DEACTIVATE_V0_2` | `RP_PACK_DEACTIVATE` | TX | C | N | `EP_PACK_GOVERNANCE_V0_2` | SU | NA |
| `OUTPUT_APPROVE_DOCUMENT_ASSEMBLY` | `EI_ASSEMBLY_APPROVAL_V0_2` | `RP_ASSEMBLY_ONE` | TX | C | N | `EP_OUTPUT_APPROVAL_V0_2` | SU | NA |
| `OUTPUT_ATTEST_DOCUMENT_ASSEMBLY` | `EI_ASSEMBLY_ATTESTATION_V0_2` | `RP_ASSEMBLY_ONE` | TX | C | N | `EP_ATTESTATION_V0_2` | SU | NA |
| `OUTPUT_FILE_SUBMISSION_ASSEMBLY` | `EI_SUBMISSION_FILING_V0_2` | `RP_SUBMISSION_ONE` | TX | C | DC | `EP_FORMAL_FILING_V0_2` | SU | NA |
| `SHARE_GRANT_ACCESS` | `EI_SHARING_GRANT_V0_2` | `RP_SHARED_ARTIFACT_ONE` | TX | C | N | `EP_SHARING_SOVEREIGNTY_V0_2` | SU | SA |
| `SHARE_REVOKE_ACCESS` | `EI_SHARING_REVOKE_V0_2` | `RP_SHARED_ARTIFACT_ONE` | TX | C | N | `EP_SHARING_SOVEREIGNTY_V0_2` | SU | SA |
| `RECEIVE_READ_DATA` | `EI_DATA_READ_V0_2` | `RP_DATA_RESOURCE_ONE` | TX | C | N | `EP_CP2_READ_QUALIFICATION_V0_2` | SU | NA |

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

Current principal binding, representation, role validity, grant validity, delegation, sharing, policy applicability, and revocation are evaluated at `authorizationEvaluatedAt` and must still hold at the effect boundary. For an internal governed write, the serializable transaction defined in section 18 supplies that effect-boundary guarantee. For an external side effect, the initial decision applies to committing the exact outbox intent. A `DISPATCH_CURRENT_AUTHORITY_REQUIRED` row treats delivery as a second protected boundary and must perform, consume, and record the fresh dispatch decision in section 18.6.

The selected rule's `historicalAuthorityPosture` is mandatory. `CURRENT_ONLY` performs no historical authority claim. `CURRENT_AND_SUBJECT_TIME` performs a second authority check at `subjectTime` with its own snapshot evidence and disposition. It never replaces the current-authority check. The exact posture for every row is fixed in section 7.8.

A current request made after revocation cannot regain authority by supplying a pre-revocation `subjectTime`.

### 8.2 Exact effect-intent binding

Every v0.2 request, result, trace, and human approval binds:

- the rule-selected `effectIntentSchemaRef`, `effectIntentSchemaVersion`, and `effectIntentSchemaDigest`;
- `effectIntentRef` or an embedded immutable effect intent;
- `effectIntentDigest`; and
- `effectIntentCanonicalization`, fixed to `JCS_RFC8785_SHA256` for v0.2.

The evaluator selects the schema binding from the action rule before validating the intent. The caller cannot choose it. `effectIntentDigest` is `sha256:` followed by the SHA-256 digest of the UTF-8 bytes produced by RFC 8785 JSON Canonicalization Scheme over the complete effect intent validated by that exact schema revision.

The effect intent contains every authorization-relevant operation input, including at least:

- the exact proposed grantee, rights, purpose, and artifact for `SHARE_GRANT_ACCESS`;
- the exact pack release/content digest, installation parameters, requested profiles, exclusions, and proposed activation-set content for context actions;
- the exact assertion body, evidence set, subject time, and claimed scope for assertion actions;
- the exact governed record and proposed decision content for review actions; and
- the exact assembly revision, destination, filing mode, and payload digest for filing.

An operation-specific schema may require more. It may not omit a value that can change the authority result or protected effect.

Payload substitution after evaluation changes the digest and requires a new decision. A decision is never authority for a merely similar payload.

### 8.3 Authorization resources

`authorizationResources` is the set of pre-existing governed objects against which grant scope and action authority are checked. The selected `resourceRequirementPolicy` determines named roles, allowed kinds, cardinality, and `ALL_OF`/`ONE_OF` composition.

Each resource entry contains:

- `resourceRole`;
- `resourceKind`;
- `resourceRef`;
- immutable `resourceRevisionRef` or content digest;
- `scopeType` and `scopeRef`;
- `twin` where applicable; and
- `authorizationResourceProofRefs`.

The proof must establish existence, exact role/kind, immutable revision, currentness where required, twin, tenant, and scope binding at the applicable evaluation time. An opaque reference alone is not proof. Every `ALL_OF` role must independently pass; authority over only one pack resource cannot satisfy a pack action.

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

An authorization resource and effect subject may refer to the same existing object only when the action rule explicitly permits it. Their proof fields and semantic roles remain distinct.

### 8.5 Pack identity

`PACK_RELEASE` or `PACK_ARTIFACT` identifies immutable installable content. `PACK_INSTALLATION` identifies the governed installation result. `PACK_ACTIVATION_SET` identifies the concrete activation posture evaluated for a scope and time.

These kinds are not interchangeable. An activation-set identifier cannot prove which pack release was installed, and a pack release cannot masquerade as an applied activation set.

### 8.6 Scope proof

`scopeProofRefs` prove the relationship between every required authorization-resource role, the effect subject, and every authority-source scope. They may refer only to immutable governed identity, containment, tenancy, or explicitly allowed lineage records that establish the claimed relationship.

Authorization-resource proof, effect-subject proof, and scope proof are not interchangeable. One immutable artifact may be bound in more than one proof array only when it independently establishes each claimed fact, and each use has a typed disposition.

### 8.7 Sovereignty and tenant isolation

`dataSovereigntyBoundaryRefs` may contain only immutable revisions of actual `DataSovereigntyBoundary` records. Generic resource, subject, scope, tenant, role, policy, or constraint evidence uses its dedicated field.

Every source, proof, policy, and evidence record used by a path must resolve within the authorized deployment or tenant boundary. Cross-tenant equality of an opaque identifier does not establish authority. A cross-tenant reference without an accepted sharing and sovereignty path is non-`ALLOW`.

---

## 9. Role and grant semantics

### 9.1 Party-targeted AuthorityGrant

A Party-targeted `AuthorityGrant` path is eligible only when:

- the immutable grant revision is active at `authorizationEvaluatedAt` and remains valid at the effect boundary;
- the grant target and immutable principal/representation/actorship basis establish one permitted path-specific `authoritySubjectBasis` and `authoritySubjectPartyRef` from section 6.2;
- the action class is present;
- the derived authority family is present;
- every required authorization resource, the effect subject, effect intent, and scope satisfy the grant's closed constraints;
- inheritance does not exceed the matrix ceiling;
- purpose, condition, and evidence rules pass;
- no active revocation defeats the path; and
- principal resolution, CP3 posture where applicable, and the human-finalization rule pass.

If the action rule requires historical authority, the same path is separately evaluated at `subjectTime`; historical success does not repair failure at current evaluation/effect time.

### 9.2 Role-targeted AuthorityGrant

A grant whose target kind is `ROLE_ASSIGNMENT` is eligible only when the referenced `RoleAssignment`:

- has an immutable revision that exists and is valid at `authorizationEvaluatedAt` and the effect boundary;
- names the path-specific `authoritySubjectPartyRef` and is supported by that path's immutable authority-subject basis;
- is valid in the same tenant boundary; and
- has at least one `anchorScopes` entry that independently covers every required authorization resource and the effect subject under the same exact scope-proof rules.

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
5. the delegation establishes the path-specific authority-subject basis and satisfies principal, every authorization-resource role, effect-subject, scope, time, purpose, condition, evidence, state, and revocation checks;
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

- `granteePartyRef` is the path-specific `authoritySubjectPartyRef`;
- `sharedArtifactFamily` maps to the `DATA_RESOURCE` authorization-resource role;
- `sharedArtifactRef` and immutable revision exactly equal that resource;
- the requested scope is covered;
- the immutable grant revision is active at `authorizationEvaluatedAt` and remains valid at the effect boundary;
- its purpose, conditions, and evidence groups are evaluable and pass for the exact effect intent;
- all actual sovereignty boundaries pass; and
- no active revocation defeats the sharing right.

A SharingGrant cannot authorize any action other than `RECEIVE_READ_DATA`. It cannot be cited as write, review, govern, context, sharing-administration, or signing authority.

A runtime must not evaluate a direct receive/use grant and a SharingGrant in separate endpoints that can return contradictory final answers. Their applicable bases and constraints are composed into one policy decision and one trace.

An `ALLOW` from those layers is not itself permission to release bytes. Actual disclosure must complete the policy-check plus mandatory CP2 qualification and the same-snapshot governed-read protocol in section 18.5. A preflight/dry-run result can report only non-protected qualification/planning information and never becomes a cached disclosure authorization.

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

1. receive only a schema-valid request and rule-valid effect intent from the ingress protocol in section 18.1;
2. canonicalize the effect intent and verify `effectIntentDigest`;
3. assign trusted `authorizationEvaluatedAt` and load the immutable authority-evaluation snapshot;
4. load and verify the content-addressed policy bundle and complete action rule;
5. verify the rule-selected effect-intent schema ref/version/digest and all rule bindings;
6. resolve the authenticated principal, represented Party, and representation basis;
7. resolve CP3 evidence and exact agent-action posture where the principal is software;
8. resolve and prove every named authorization-resource requirement and the effect subject under the row's existence posture;
9. prove tenant, sovereignty, and scope relationships;
10. resolve role, direct-grant, delegated, and sharing candidates, deriving an authority subject/basis separately for each path;
11. evaluate action, family, resources, subject, intent, scope, inheritance, time, state, purpose, conditions, and cumulative evidence requirements per path;
12. evaluate delegated source paths under the closed delegation intersection;
13. compose any applicable `RECEIVE_READ_DATA` SharingGrant path;
14. apply every effective revocation from the completeness-proven snapshot;
15. apply the rule's exact historical-authority posture at `subjectTime` without replacing the current check;
16. run or verify the governed human-approval lifecycle for the exact intent where required;
17. assign one disposition to every path and aggregate them under section 15.3;
18. build the request, result, and trace records with immutable basis bindings;
19. validate `decisionValidUntil`, consumption posture, and the decision-bundle digest; and
20. enter the governed write, governed read, external-dispatch, or non-`ALLOW` protocol in section 18.

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

Effect-intent digest validity, loaded policy identity, trusted principal resolution, authorization-resource/effect-subject proof, tenant isolation, and authority-snapshot availability are authorization global preconditions. Parse, request-schema, action lookup, rule/binding-manifest, caller-schema-claim, and action-specific intent-schema failures never enter this lattice; section 18.1 records them as ingress rejections. A failed authorization global precondition produces its reason-table outcome before path aggregation; no path may override it.

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
- `selectedRuleId`, immutable rule revision, and rule content digest; and
- binding-manifest content ref and digest.

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

Draft/non-default work in the controlled sequence in section 24 should add:

- `ActionAuthorizationRule v0.2` and its immutable binding manifest;
- the closed operation-specific `EffectIntent` schema revisions from section 7.6;
- `AuthorityGrant v0.2`;
- `DelegationGrant v0.2`;
- `SharingGrant v0.2`;
- `AuthorityEvaluationSnapshot v0.2`;
- `AuthorizationRequestRejection v0.2`;
- `AuthorizationDecisionRequest v0.2`;
- `AuthorizationDecisionResult v0.2`;
- `AuthorizationDecisionTrace v0.2`;
- `AuthorizationApprovalChallenge v0.2`;
- `AuthorizationHumanApproval v0.2`;
- `AuthorizationDecisionConsumption v0.2`; and
- `AuthorizationEffectReceipt v0.2` and `AuthorizationGovernedReadReceipt v0.2`.

`RoleAssignment v0.1`, `RevocationDecision v0.1`, and `DataSovereigntyBoundary v0.1` remain unchanged by default. If schema changes to those families prove necessary, they require an explicit scope review before editing.

### 17.3 Source-record delta

Common v0.2 source behavior:

- make `authorityFamilies` closed and required where the source carries authority families;
- add optional closed `permittedUsePurposes`;
- remove free-text `purpose` and `conditions` from the executable v0.2 form;
- reject unknown fields;
- add optional narrowing by named authorization-resource roles/kinds/refs, effect-subject kinds/refs/existence postures, rule-selected effect-intent profile IDs, and twins;
- retain closed action, scope, time, state, and inheritance constraints; and
- preserve immutable provenance linking a migrated record to its v0.1 predecessor.

`AuthorityGrant v0.2` additionally carries required closed `delegationPermission` and conditional `delegableActionClasses` as defined in section 10.

Every v0.2 source family that can impose evidence uses the typed all-or-none `requiredEvidence` groups in section 12. `DelegationGrant v0.2` is not a special exception.

`SharingGrant v0.2` makes the immutable artifact-family/resource-kind binding explicit and keeps `dataSovereigntyBoundaryRefs` restricted to actual sovereignty records.

### 17.4 Request v0.2

Caller-provided request facts:

- request identifier and request time;
- requested action class;
- named authorization-resource instances and immutable revisions claimed by the request;
- effect subject, proposed identifier, existence posture, scope, `subjectTime`, and twin where applicable;
- retrievable or embedded effect-intent instance and `effectIntentDigest`;
- optional requested use-purpose token;
- optional AI-assistance disclosure; and
- optional retrieval hints that are explicitly non-authoritative.

Trusted boundary facts injected before evaluation:

- `resolvedPrincipalKind`;
- `authenticatedPrincipalRef` and immutable resolution revision;
- `representedPartyRef` and `representationBasisRef`, when applicable;
- the CP3 envelope/snapshot references for a software agent;
- trusted `authorizationEvaluatedAt`; and
- `authorityEvaluationSnapshotRef`.

The caller cannot choose any trusted-boundary fact or effect-intent schema. The action rule supplies the exact schema binding. `subjectTime` describes the governed subject only and never controls current authority.

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
- rule-selected effect-intent schema ref/version/digest, intent reference/digest, and canonicalization;
- requested action class;
- derived stage and authority family;
- policy identity, selected immutable rule revision/digest, and binding-manifest ref/digest;
- resolved-principal kind, selected path-specific authority subject/basis, accepted CP3 posture where applicable, and human-finalization requirement;
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
- rule-selected effect-intent schema ref/version/digest, immutable intent reference/digest, and canonicalization;
- policy ID/version/digest, selected immutable rule revision/digest, and binding-manifest ref/digest;
- action class, derived stage, and derived family;
- resolved-principal kind, authenticated principal and immutable resolution revision, represented Party, and representation basis;
- for software agents, executing instance, profile, sponsor, actorship binding, authority envelope, mandatory authority snapshot, revocation state, preflight, and qualification revision refs;
- accepted CP3 agent-action posture, human-finalization requirement, and AI-disclosure disposition;
- every named authorization-resource role, immutable revision, scope, twin, proof refs, composition result, and individual disposition;
- full effect subject, existence posture, subject time, proof refs, resulting revision ref where applicable, and individual dispositions;
- scope proof refs and individual dispositions;
- `authorityEvaluationSnapshotRef`, canonical-history position, and all relevant index watermarks;
- role assignments and anchor-scope immutable basis bindings/dispositions;
- every path's authority-subject Party/basis, direct grant, delegation, source-grant, and sharing immutable basis bindings/dispositions;
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

### 18.1 Ingress rejection is not an authorization outcome

Ingress performs these checks in order, before authorization evaluation:

1. reject malformed bytes and duplicate JSON member names before constructing an object model;
2. validate the base `AuthorizationDecisionRequest v0.2` shape;
3. resolve the action class and verify the selected immutable `ActionAuthorizationRule` and binding manifest; and
4. validate the effect intent against the schema ref, version, and content digest selected by that rule.

Failure at any of those steps does not create a `DENY`, `REQUIRE_REVIEW`, or any other authorization result. If durable audit is required, the runtime records an `AuthorizationRequestRejection v0.2` or a lower-level transport/security event containing only facts it can truthfully establish:

- trusted receipt time and a digest of the received bytes;
- the claimed request identifier, action class, or schema hint only when they were safely parseable, explicitly marked as untrusted claims;
- the authenticated principal/session binding, when resolution had already succeeded;
- the selected action-rule and schema binding, only if ingress reached that step;
- stable ingress-rejection codes and validation locations; and
- the rejection-record schema identity and integrity digest.

The rejection must not assert that malformed input was a valid `AuthorizationDecisionRequest`, must not include an `AuthorizationDecisionResult` or `AuthorizationDecisionTrace`, and must not produce a protected effect. A caller-provided effect-intent schema hint is non-authoritative and, when present, must exactly equal the rule-selected binding; it can never select a weaker schema.

Only a schema-valid request with a rule-valid effect intent enters the authorization outcome lattice in section 15. Ingress rejection persistence failure is a runtime/audit failure, not a fabricated authorization result.

### 18.2 Decision validity and replay

Every decision records `decisionValidUntil` from the selected action rule. The caller cannot extend it.

For every `TX` row, the selected `TRANSACTION_BOUND_30S_V0_2` policy computes `decisionValidUntil` as the earliest instant in this exact candidate set:

1. `authorizationEvaluatedAt + PT30S`;
2. the trusted serializable-transaction deadline, which must be fixed before evaluation and must not exceed item 1;
3. the principal-resolution/session validity end;
4. every applicable representation, role-assignment, AuthorityGrant, DelegationGrant, source-grant, SharingGrant, and revocation-policy validity end used by the selected path;
5. policy/rule applicability end and authority-snapshot freshness deadline;
6. every applicable resource lease/currentness end, evidence eligibility/freshness end, and sovereignty-policy end; and
7. `approvalExpiresAt`, when approval is required.

Instants are compared as UTC timeline instants and all ends are exclusive. An explicitly unbounded governed interval contributes no cutoff; a missing or unparseable cutoff that its governing contract requires is non-`ALLOW`. If the candidate set cannot be constructed, or its minimum is not later than `authorizationEvaluatedAt`, no consumable decision exists. The decision must be consumed inside that transaction and is not portable to a later transaction.

Every decision records one `consumptionMode`:

- `SINGLE_USE`; or
- `REPLAYABLE_IDENTICAL_READ`.

All v0.2 matrix rows are `SINGLE_USE`. `REPLAYABLE_IDENTICAL_READ` is reserved for a later accepted `RECEIVE_READ_DATA` rule and requires an exact `maxDecisionAge` in that rule. If promoted later, replay is limited to the same authenticated principal, authority subject, immutable resource revision, snapshot policy, and exact effect-intent digest until `decisionValidUntil`. Absent that accepted rule, replay is prohibited.

`AuthorizationDecisionConsumption` records the decision, effect-intent digest, consumer principal, consumption time, effect/outbox reference, and idempotency key. A second consumption of a single-use decision is non-`ALLOW` even if the payload is identical.

### 18.3 Human-approval lifecycle

An action whose rule requires `FRESH_HUMAN_APPROVAL_REQUIRED` does not accept an unattached approval reference or a bare boolean. It uses two versioned records.

`AuthorizationApprovalChallenge v0.2` binds:

- a unique challenge identifier;
- the rule-selected effect-intent schema ref/version/digest, exact effect-intent digest, and retrievable intent reference;
- policy ID/version/digest and selected action-rule ID/digest;
- every authorization-resource role/revision, effect subject, selected path-specific authority subject/basis, and represented Party;
- the immutable authority-evaluation snapshot used to prepare the challenge;
- a digest of the exact human-visible representation of the protected effect;
- trusted issue time and `challengeExpiresAt`;
- `approvalSeparationPolicy`; and
- closed approver-eligibility requirements.

`AuthorizationHumanApproval v0.2` binds:

- a unique approval identifier and the exact challenge revision;
- the authenticated natural-person principal, represented Party, and immutable representation basis;
- trusted `humanActedAt`;
- the approved effect-intent, policy, rule, resource, subject, and human-visible representation digests;
- the challenge snapshot and the identical final authority-evaluation snapshot;
- `approvalExpiresAt`, single-use posture, and consumption status; and
- signature, attestation, or authenticated-session evidence required by the action rule.

The lifecycle is exactly:

1. evaluate enough trusted state to prepare and display the exact protected effect, then persist its challenge;
2. capture an authenticated natural person's explicit act on that challenge;
3. re-evaluate every current authority, representation, revocation, resource, evidence, policy, and separation constraint;
4. require the final `authorityEvaluationSnapshotRef` to equal the challenge snapshot; if it is stale or differs for any reason, invalidate the act and issue a new challenge for the new snapshot and display; and
5. bind the approval to that final snapshot and consume both the approval and authorization decision atomically with the governed effect or outbox commit.

For a direct natural-person invocation, `FRESH_HUMAN_APPROVAL_REQUIRED` may be satisfied by that person's same explicit act only through this lifecycle and only when the rule says `SELF_APPROVAL_ALLOWED`. A rule saying `DISTINCT_APPROVER_REQUIRED` requires a different authenticated natural-person principal whose immutable authority and relationship constraints independently pass; sponsor status, ownership of an agent, or shared representation alone does not satisfy separation. `DIRECT_HUMAN_ACTION_REQUIRED` records the authenticated human act and representation basis as part of the request/effect transaction; it does not require a separate approval record unless another rule independently requires final approval.

An expired challenge, changed display digest, changed intent, changed policy/rule, changed resource revision, changed authority snapshot, ineligible approver, or replayed/consumed approval is non-`ALLOW`. Approval can never extend `decisionValidUntil` or outlive its own expiry.

### 18.4 Internal governed writes

For an internal governed write, one serializable transaction must:

1. evaluate or revalidate current principal, representation, source authority, revocation, resource revision, and effect-intent digest against the transaction snapshot;
2. build and validate the request/result/trace bundle;
3. reserve single-use consumption;
4. apply the exact protected effect;
5. record the resulting immutable effect revision and `AuthorizationEffectReceipt`;
6. commit the decision evidence, consumption, receipt, and effect together.

If a concurrent authority, revocation, or resource change invalidates the snapshot, serialization must fail and the operation must be re-evaluated. The invariant is: **no governed effect becomes externally visible without its committed decision evidence**. The decision is not committed in an earlier transaction that creates a time-of-check/time-of-use gap.

### 18.5 Governed reads and protected disclosure

Actual `RECEIVE_READ_DATA` is a protected disclosure and uses `AGENT_ALLOWED_WITH_POLICY_CHECK`, not `AGENT_ALLOWED_WITH_PREFLIGHT_ONLY`. A preflight/dry-run may return only non-protected planning or qualification information and must never disclose protected bytes. Every actual read also requires the CP2 read-qualification evidence profile selected in section 7.8; this is an authorization-rule requirement and does not redefine a CP3 posture value.

One governed read snapshot must cover both authorization and retrieval. The decision bundle and `AuthorizationGovernedReadReceipt v0.2` bind at least:

- every immutable authorization-resource revision read;
- the exact `QuerySpecification` and executable query/plan digest, where applicable;
- row, field, tenant, purpose, sovereignty, and redaction-policy identities/digests;
- the CP2 qualification envelope, including qualification outcome, stable problems, trace/lineage refs, and prescribed next actions;
- the returned payload digest or a complete immutable payload/chunk manifest; and
- whether the read completed, failed before disclosure, or stopped after an explicitly recorded partial stream.

For a buffered read, the runtime must stage and hash the exact returned payload, then atomically persist the decision evidence, single-use consumption, governed-read receipt, and payload manifest before any protected byte crosses the trust boundary. If that persistence fails, zero protected bytes are released.

Streaming is permitted only when the complete ordered immutable chunk manifest, every chunk digest and length, the total payload digest, and the decision/read evidence can be staged and committed before the first protected byte is released. The stream may emit only the committed chunks in order. A transport failure stops disclosure and appends a separate failure/partial-delivery receipt without rewriting the committed authorization evidence or claiming complete delivery. If the complete payload cannot be predetermined and committed in that form, streaming the protected response is forbidden.

Authorization, retrieval, redaction, qualification, and payload construction must observe the same governed snapshot. No cache, secondary endpoint, preflight response, error body, count, metadata field, or retry path may release protected information before the required evidence commits.

### 18.6 External side effects

Every action rule selects exactly one external-effect posture:

- `NO_EXTERNAL_DISPATCH`: the action cannot create an external dispatch;
- `OUTBOX_COMMIT_IS_FINAL_EFFECT`: consuming the decision and committing the exact idempotent outbox record is the governed final effect; later delivery may not exercise new authority; or
- `DISPATCH_CURRENT_AUTHORITY_REQUIRED`: external delivery is itself a protected effect and requires fresh current authority at dispatch.

For an external side effect, one serializable transaction must atomically commit:

- the decision bundle;
- the single-use consumption reservation;
- an idempotent outbox record containing the exact effect-intent digest and destination; and
- a pending `AuthorizationEffectReceipt` reference.

The dispatcher may send only the committed bytes bound by the digest and idempotency key. It records dispatch completion or failure without rewriting the original decision.

No dispatcher may send after the decision's `decisionValidUntil`, even when no watermark changed. For `DISPATCH_CURRENT_AUTHORITY_REQUIRED`, every dispatch attempt unconditionally re-evaluates current principal and representation validity, source grant/delegation/sharing validity, natural time expiry, revocations, policy/rule identity, resource revisions, required evidence freshness, sovereignty constraints, approval validity/separation, destination, payload digest, and idempotency posture. A watermark comparison is an optimization hint only and never substitutes for these checks.

For that posture, the dispatcher creates a fresh dispatch authorization decision over the exact committed outbox bytes, destination, idempotency key, and original effect-intent digest. A serializable dispatch-reservation transaction commits that decision, its single-use consumption, and a dispatch-attempt reference immediately before send. The dispatcher may send only while the fresh decision remains unexpired and records its decision/attempt refs in the final delivery/failure receipt. Expiry before send abandons that attempt and requires another complete evaluation; it does not revive or rewrite the earlier outbox decision.

`OUTPUT_FILE_SUBMISSION_ASSEMBLY` uses `DISPATCH_CURRENT_AUTHORITY_REQUIRED` in v0.2 because formal filing creates authority at the receiving boundary. No current row uses `OUTBOX_COMMIT_IS_FINAL_EFFECT`; adopting it later requires an explicit row amendment describing why later delivery exercises no new authority. A changed fact, expired source, expired approval, expired decision, or unavailable current snapshot pauses dispatch and requires a fresh sufficient decision. Backdating `subjectTime` cannot bypass dispatch-time checks.

### 18.7 Non-`ALLOW` responses

For a schema-valid authorization request whose outcome is `DENY`, `REQUIRE_REVIEW`, or `REQUIRE_HUMAN_APPROVAL`, the request/result/trace refusal bundle commits atomically with no protected effect. Only after commit may an outer transport boundary convert it into a typed response. Ingress failures remain section 18.1 rejections and are never represented through this protocol.

If persistence fails, the runtime fails closed with a persistence/runtime error. It must not claim that a durable authorization denial or allowance exists when no trace committed.

### 18.8 Decision-bundle digest

The canonical v0.2 digest input is exactly:

```json
{
  "schemaVersion": "ofarm.authorizationDecisionBundleDigestInput.v0.2",
  "request": {},
  "result": {},
  "trace": {}
}
```

`request`, `result`, and `trace` are the complete records. Digest construction uses this exact projection algorithm:

1. reject duplicate JSON member names before parsing any component;
2. validate the request normally and validate provisional result/trace records with each required digest field set to the exact pre-digest sentinel `ofarm:pending-decision-bundle-digest`; the sentinel is legal only to the dedicated pre-digest validators and is forbidden in a final record;
3. construct the digest-input object above;
4. require and remove exactly the JSON Pointer paths `/result/decisionBundleDigest` and `/trace/decisionBundleDigest`;
5. retain and hash every other member, including any nested member coincidentally named `decisionBundleDigest` inside schema-permitted extension content;
6. canonicalize, hash, and populate both removed fields with the same final digest; and
7. validate the complete final result and trace against their ordinary schemas.

If either exact pointer is absent, has the wrong type or sentinel, cannot be removed exactly once, or the final values differ, construction fails with `DECISION_BUNDLE_PROJECTION_INVALID`. This is a runtime/integrity failure with no protected effect, not an authorization outcome. Unknown members remain governed by the component schemas; the projection rule never grants permission to add them.

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
- a caller-provided schema ref cannot reconstruct the rule-selected effect-intent schema binding or immutable binding manifest;
- optional AI metadata cannot reconstruct principal resolution, representation, CP3 posture, or human finalization;
- a sponsor or globally inferred Party cannot reconstruct a path-specific software-agent authority subject or its direct-grant/delegation basis;
- a target reference cannot reconstruct authorization-resource/effect-subject separation or existence posture;
- one target reference cannot reconstruct named composite resource roles or their `ALL_OF`/`ONE_OF` disposition;
- caller target time cannot reconstruct trusted evaluation/effect time;
- an unbound payload cannot reconstruct the effect-intent digest;
- an approval reference or boolean cannot reconstruct the challenge, displayed-effect digest, authenticated human act, snapshot equality, separation policy, or single-use consumption;
- a read response cannot reconstruct same-snapshot query/redaction/qualification evidence or prove that evidence committed before disclosure;
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

Malformed or schema-invalid v0.1/v0.2 inputs coexist only as ingress rejection evidence; they are never upgraded into validated v0.2 authorization decisions. A v0.1 read path also cannot claim v0.2 governed-read evidence unless it implements the complete section 18.5 contract and binds the promoted v0.2 policy/schema bundle.

---

## 20. Stable reason codes

Lower rank wins within the outcome selected by section 15. Ranks are never compared across different outcomes.

Ingress rejection codes are stable but are outside `AuthorizationDecisionOutcome` and have no authorization rank:

| Ingress rejection code | Meaning |
|---|---|
| `DUPLICATE_JSON_MEMBER` | received JSON contains a duplicate member name |
| `REQUEST_PARSE_INVALID` | received bytes cannot be parsed as the required representation |
| `REQUEST_SCHEMA_INVALID` | the parsed value is not a valid base request |
| `UNKNOWN_ACTION_CLASS` | no closed action class/rule can be selected |
| `ACTION_RULE_BINDING_INVALID` | the selected rule or binding manifest is missing, mutable, malformed, or digest-invalid |
| `EFFECT_INTENT_SCHEMA_CLAIM_MISMATCH` | a caller schema hint differs from the rule-selected schema binding |
| `EFFECT_INTENT_SCHEMA_INVALID` | the effect intent fails the rule-selected schema |
| `INGRESS_AUDIT_PERSISTENCE_FAILED` | required rejection evidence could not be persisted |

These codes may appear only in `AuthorizationRequestRejection` or runtime/security telemetry. They must not be placed in a decision result or converted locally into `DENY`.

| Reason code | Default outcome | Rank |
|---|---:|---:|
| `AUTHORIZED_BY_SELECTED_PATH` | `ALLOW` | 0 |
| `HUMAN_FINAL_ACTION_REQUIRED` | `REQUIRE_HUMAN_APPROVAL` | 100 |
| `APPROVAL_CHALLENGE_STALE` | `REQUIRE_HUMAN_APPROVAL` | 110 |
| `APPROVAL_EXPIRED` | `REQUIRE_HUMAN_APPROVAL` | 120 |
| `APPROVAL_SEPARATION_UNSATISFIED` | `REQUIRE_HUMAN_APPROVAL` | 130 |
| `AUTHORIZATION_SNAPSHOT_UNAVAILABLE` | `REQUIRE_REVIEW` | 200 |
| `POLICY_NOT_AVAILABLE` | `REQUIRE_REVIEW` | 210 |
| `POLICY_DIGEST_MISMATCH` | `REQUIRE_REVIEW` | 220 |
| `UNSUPPORTED_REVOCATION_NARROWING` | `REQUIRE_REVIEW` | 230 |
| `UNSUPPORTED_EVIDENCE_POLICY` | `REQUIRE_REVIEW` | 240 |
| `UNSUPPORTED_LEGACY_EVIDENCE_REQUIREMENT` | `REQUIRE_REVIEW` | 250 |
| `UNSUPPORTED_LEGACY_CONDITION` | `REQUIRE_REVIEW` | 260 |
| `UNSUPPORTED_LEGACY_PURPOSE` | `REQUIRE_REVIEW` | 270 |
| `OUTBOX_DISPATCH_REAUTH_REQUIRED` | `REQUIRE_REVIEW` | 280 |
| `EFFECT_INTENT_DIGEST_MISMATCH` | `DENY` | 1000 |
| `UNRESOLVED_PRINCIPAL` | `DENY` | 1010 |
| `REPRESENTATION_BASIS_INVALID` | `DENY` | 1020 |
| `AUTHORITY_SUBJECT_BASIS_INVALID` | `DENY` | 1030 |
| `CP3_EVIDENCE_MISSING` | `DENY` | 1040 |
| `CP3_AUTHORITY_SNAPSHOT_MISSING` | `DENY` | 1050 |
| `SOFTWARE_AGENT_NOT_PERMITTED` | `DENY` | 1060 |
| `PREFLIGHT_REQUIRED` | `DENY` | 1070 |
| `APPROVAL_EFFECT_INTENT_MISMATCH` | `DENY` | 1080 |
| `APPROVAL_ALREADY_CONSUMED` | `DENY` | 1090 |
| `DECISION_EXPIRED` | `DENY` | 1100 |
| `DECISION_ALREADY_CONSUMED` | `DENY` | 1110 |
| `AUTHORITY_STATE_CHANGED_BEFORE_EFFECT` | `DENY` | 1120 |
| `TENANT_BOUNDARY_MISMATCH` | `DENY` | 1130 |
| `COMPOSITE_RESOURCE_REQUIREMENT_UNSATISFIED` | `DENY` | 1140 |
| `AUTHORIZATION_RESOURCE_NOT_PROVEN` | `DENY` | 1150 |
| `EFFECT_SUBJECT_NOT_PROVEN` | `DENY` | 1160 |
| `RESOURCE_KIND_MISMATCH` | `DENY` | 1170 |
| `SUBJECT_KIND_MISMATCH` | `DENY` | 1180 |
| `RESOURCE_REF_MISMATCH` | `DENY` | 1190 |
| `SUBJECT_REF_MISMATCH` | `DENY` | 1200 |
| `PACK_RELEASE_MISMATCH` | `DENY` | 1210 |
| `TWIN_MISMATCH` | `DENY` | 1220 |
| `SCOPE_NOT_PROVEN` | `DENY` | 1230 |
| `ACTIVE_REVOCATION` | `DENY` | 1240 |
| `AUTHORITY_NOT_ACTIVE_AT_AUTHORIZATION_TIME` | `DENY` | 1250 |
| `HISTORICAL_AUTHORITY_REQUIRED` | `DENY` | 1260 |
| `ROLE_ASSIGNMENT_NOT_APPLICABLE` | `DENY` | 1270 |
| `ROLE_ANCHOR_SCOPE_MISMATCH` | `DENY` | 1280 |
| `DELEGATION_PROHIBITED_BY_ACTION_RULE` | `DENY` | 1290 |
| `DELEGATION_NOT_PERMITTED_BY_SOURCE` | `DENY` | 1300 |
| `DELEGATION_SOURCE_MISSING` | `DENY` | 1310 |
| `DELEGATION_BROADENS_AUTHORITY` | `DENY` | 1320 |
| `DELEGATION_CYCLE` | `DENY` | 1330 |
| `DELEGATION_DEPTH_EXCEEDED` | `DENY` | 1340 |
| `SHARING_BASIS_MISMATCH` | `DENY` | 1350 |
| `ACTION_CLASS_NOT_GRANTED` | `DENY` | 1360 |
| `AUTHORITY_FAMILY_MISMATCH` | `DENY` | 1370 |
| `INHERITANCE_NOT_PERMITTED` | `DENY` | 1380 |
| `PURPOSE_REQUIRED` | `DENY` | 1390 |
| `PURPOSE_NOT_PERMITTED` | `DENY` | 1400 |
| `EVIDENCE_POLICY_REQUIRED` | `DENY` | 1410 |
| `REQUIRED_EVIDENCE_MISSING` | `DENY` | 1420 |
| `REQUIRED_EVIDENCE_INELIGIBLE` | `DENY` | 1430 |
| `NO_AUTHORITY_BASIS` | `DENY` | 1990 |

`DECISION_BUNDLE_PERSISTENCE_FAILED`, `DECISION_BUNDLE_PROJECTION_INVALID`, `READ_EVIDENCE_PERSISTENCE_FAILED`, and dispatch transport failures are runtime/integrity failures, not authorization outcomes, and therefore have no reason rank. A runtime must not fabricate a result record to place them in this table.

Problem severity is fixed by outcome: `ALLOW` is `INFO`, `REQUIRE_HUMAN_APPROVAL` and `REQUIRE_REVIEW` are `WARNING`, and `DENY` is `ERROR`. Diagnostic problems are ordered with the selected path first, then by path-type order, immutable source revision, numeric rank, and related reference. Severity never chooses the primary reason.

Additional codes require a versioned policy update. Implementations must not collapse a known authorization failure into an unstructured message or assign local ranks.

---

## 21. Invariants

The accepted design and conformance suite must preserve these invariants:

1. Omitting or changing optional AI-assistance metadata never increases authority.
2. Caller-supplied stage, family, principal kind, revocation posture, or authority time never controls the policy result.
3. Exactly one immutable action rule selects every policy-derived field, including the effect-intent schema ref/digest, named resource composition, validity function, historical posture, dispatch posture, evidence policy, and consumption mode.
4. A caller may submit an effect-intent instance but can never select or substitute its governing schema.
5. Every named `ALL_OF` resource role independently passes; every `ONE_OF` policy selects exactly one permitted branch.
6. A pre-revocation `subjectTime` never authorizes a post-revocation current effect.
7. Unknown action, family, resource kind, effect-subject kind, existence posture, condition, evidence policy, or proof type is fail-closed at ingress or authorization as its governing contract specifies.
8. Principal resolution, represented Party, representation basis, CP3 posture, and human-finalization requirement remain separate axes.
9. Every candidate path derives its own closed authority-subject Party and immutable direct-grant, representation, or delegation basis; sponsor identity never supplies authority.
10. Every software-agent path preserves the accepted CP3 posture and mandatory authority snapshot.
11. `AGENT_ALLOWED_WITH_PREFLIGHT_ONLY` never permits protected disclosure; actual `RECEIVE_READ_DATA` uses policy check plus the mandatory CP2 qualification profile.
12. Human approval is valid only for the exact effect intent, displayed representation, policy/rule, resources, authority subject, snapshot, represented Party, and validity window.
13. Challenge and final authority snapshots must be identical; a changed snapshot requires a new challenge and human act.
14. Direct human invocation satisfies fresh approval only through the approval lifecycle and only under `SELF_APPROVAL_ALLOWED`; a distinct-approver rule is independently enforced.
15. Approval and decision are single-use; their consumption commits atomically with the governed effect or outbox record.
16. Payload substitution, expired decisions, expired approvals, and replay are non-`ALLOW`.
17. An existing authorization resource and a prospective effect subject are not conflated.
18. Pack release, installation, activation-set, scope, and registry identities are not interchangeable or optional when their resource roles are required.
19. A role-targeted grant never exceeds either its grant scope or its role anchor scope.
20. A delegated path never exceeds the action-rule ceiling, source permission, source role anchor, or DelegationGrant at any dimension.
21. A purpose-constrained source cannot pass without an exact matching request purpose, and caller-only purpose never creates authority.
22. Free-text purpose and conditions are never guessed into executable v0.2 semantics.
23. Evidence requirements from the action rule and every selected source are cumulative.
24. Every required evidence ref and policy is bound to an immutable revision and evaluated under the named active policy.
25. Authorization-resource proof, effect-subject proof, scope proof, constraint evidence, and read-qualification evidence remain typed and distinct.
26. `dataSovereigntyBoundaryRefs` contains only immutable revisions of actual sovereignty records.
27. A SharingGrant grants read/receive use only for its exact grantee and immutable artifact revision.
28. Every effective revocation is considered from a completeness-proven snapshot and watermark.
29. Partial grant paths or paths with different authority subjects are not unioned into a fabricated complete path.
30. Every path receives one disposition and mixed paths aggregate under one total lattice; a failed non-selected path never supplies the primary reason for an `ALLOW` result.
31. The same immutable effect intent, authority snapshot, policy bytes, and basis revisions produce the same path dispositions, outcome, selected basis, ordered problems, and primary reason code.
32. Internal effect and decision evidence commit in one serializable transaction; neither precedes the other in a separate committed transaction.
33. Governed-read authorization, retrieval, redaction, qualification, and payload construction use one snapshot, and no protected byte leaves before decision/read evidence commits.
34. Protected streaming uses only a complete precommitted immutable chunk manifest; a partial transport failure never becomes a complete-delivery claim.
35. External dispatch sends only the committed content-addressed outbox intent, never occurs after the authorizing decision expires, and unconditionally rechecks every clock-dependent constraint when dispatch-current authority is required.
36. A typed authorization refusal never claims a durable trace that did not commit.
37. Malformed or schema-invalid input creates only ingress rejection evidence and never a validated authorization outcome bundle.
38. Digest projection removes only `/result/decisionBundleDigest` and `/trace/decisionBundleDigest`; every other occurrence remains hashed, and an absent, malformed, or non-unique expected field fails integrity construction.
39. Every reconstructed decision resolves the same immutable basis and policy bytes visible at its recorded snapshot.
40. v0.1 records never silently claim v0.2 proof strength.
41. Draft schema presence never changes current/default status.

---

## 22. Production-reachable hostile cases

The future executable conformance suite must include at least:

| Case | Required disposition |
|---|---|
| Same request retried after omitting `aiAssistance.assisted: true` | same resolved principal, CP3 posture, and no authority increase |
| Caller changes `nonHumanActor` or derived family/stage hint | hint ignored or schema-rejected; policy result unchanged |
| Caller supplies a weaker effect-intent schema that omits an authorization-relevant field | ingress rejection with `EFFECT_INTENT_SCHEMA_CLAIM_MISMATCH`; rule-selected schema remains authoritative |
| Bound effect-intent schema bytes differ while ref/version remain unchanged | ingress rejection with `ACTION_RULE_BINDING_INVALID`; no evaluation or effect |
| Authority is revoked, then a current request supplies a pre-revocation `subjectTime` | current effect is `DENY`; subject time never replaces trusted current time |
| Natural person acts for an organization without a valid immutable representation basis | `DENY` |
| Organization-held grant is evaluated against the authenticated natural person rather than `authoritySubjectPartyRef` | conformance failure |
| Agent has a direct grant for Party A and explicit delegation for Party B | two independent path-specific authority subjects; no global Party and no cross-path union |
| Agent sponsor is substituted for a missing grant/delegation authority subject | `DENY`; sponsor identity creates no authority |
| Software agent omits the mandatory CP3 authority snapshot | `DENY` |
| Sponsor-bound agent attempts a human-only review decision | non-`ALLOW` |
| A preflight-only endpoint attempts to disclose protected data, even with valid preflight evidence | disclosure prohibited; conformance failure if any protected byte leaves |
| Actual agent read lacks the rule-selected CP2 qualification evidence | `DENY`; `PREFLIGHT_ONLY` is not used to authorize the read |
| Governed read authorization and retrieval observe different snapshots | no disclosure; conformance failure |
| Governed read decision/read-receipt persistence fails before response | zero protected bytes leave; `READ_EVIDENCE_PERSISTENCE_FAILED` runtime failure |
| Read response substitutes another resource revision, query/plan, redaction policy, qualification envelope, or payload | digest/binding failure; zero substituted protected bytes leave |
| Protected streaming begins without a complete committed ordered chunk manifest | stream forbidden; conformance failure if any protected byte leaves |
| Protected stream fails after committed chunks were delivered | stop immediately and record exact partial/failure receipt; never claim complete delivery |
| AI-assisted high-risk assertion has no fresh human approval for the exact effect-intent digest | `REQUIRE_HUMAN_APPROVAL` |
| Authority snapshot changes between approval challenge and final evaluation | old challenge/act is stale; issue a new challenge and require a new human act |
| Approval challenge or approval expires before effect consumption | `REQUIRE_HUMAN_APPROVAL`; no effect |
| Natural person directly invokes an `FA` row under `SELF_APPROVAL_ALLOWED` | the same explicit act may satisfy approval only through the section 18.3 lifecycle |
| Same principal attempts an `FA` row under `DISTINCT_APPROVER_REQUIRED` | `REQUIRE_HUMAN_APPROVAL` with separation unsatisfied; no effect |
| Approval covers payload A but the protected operation substitutes payload B | digest mismatch; `DENY` and no effect |
| Consumed human approval is replayed with the same challenge and payload | `DENY` with `APPROVAL_ALREADY_CONSUMED`; no effect |
| A single-use decision is consumed twice with the same payload | second consumption is `DENY` |
| A decision is consumed after `decisionValidUntil` | `DENY` |
| Revocation commits between evaluation and an internal governed write | serialization/revalidation failure; no effect |
| Revocation watermark changes before dispatch-current external filing | dispatch pauses and a fresh authorization decision is required |
| Source grant naturally expires after outbox commit while every watermark remains unchanged | no dispatch; expiry is re-evaluated and a fresh sufficient decision is required |
| Dispatcher attempts filing after the authorizing decision's `decisionValidUntil` | no dispatch regardless of unchanged watermarks or valid idempotency key |
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
| Pack install proves only `PACK_REGISTRY`, only `TARGET_SCOPE`, or omits `PACK_RELEASE_INPUT` | `DENY` with `COMPOSITE_RESOURCE_REQUIREMENT_UNSATISFIED` |
| Assembly request supplies both branches of `RP_ASSEMBLY_ONE` | `DENY`; `ONE_OF` ambiguity cannot widen authority |
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
| Malformed JSON or a duplicate member name is submitted | ingress rejection only; no authorization result/trace bundle and no protected effect |
| Base request or rule-selected effect intent is schema-invalid | `AuthorizationRequestRejection`, never a validated `DENY` bundle |
| Nested schema-permitted content contains `decisionBundleDigest` and is changed | nested member remains hashed and the bundle digest changes |
| `/result/decisionBundleDigest` or `/trace/decisionBundleDigest` is absent, malformed, or not removable exactly once | `DECISION_BUNDLE_PROJECTION_INVALID`; no protected effect |
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
| Logical refs and one policy digest do not guarantee reconstruction | sections 16, 17, and 18.8 |
| Header reverses dependency direction | header now says `Triggered by` and explicitly `Blocks` OFARM2 work |
| Action rule is incomplete and caller can select a weaker intent schema | sections 7.4 through 7.8, 8.2, 17, and 18.1 |
| Composite pack resources have ambiguous singular/alternative semantics | sections 7.5, 7.8, 8.3, and 22 |
| Governed reads lack same-snapshot authorization/disclosure evidence and preflight-only is reinterpreted | sections 6.3, 7.2, 7.8, 13, and 18.5 |
| External dispatch can outlive decision, grants, approval, or evidence without a watermark change | sections 7.8 and 18.6 |
| Human approval has no challenge, final-snapshot, separation, or atomic-consumption lifecycle | sections 6.4, 17, and 18.3 |
| Software-agent authority subject is globally inferred and not derivable from current CP3 | sections 6.2, 9, 10, 13, 15, and 17 |
| Invalid request cannot truthfully inhabit a validated refusal bundle | sections 15.4, 17.2, 18.1, 18.7, and 20 |
| Name-based decision-digest exclusion permits nested exclusion injection | sections 18.8, 21, and 22 |

This table does not authorize an OFARM2 fix. OFARM2 must wait for accepted semantics, promoted contracts, and byte-identical extraction.

---

## 24. Staged delivery and currentness

The required sequence is:

1. **Phase A candidate:** this document only; no authority or currentness effect.
2. **Semantic-profile approval:** stewards approve or amend the closed rule fields, profile IDs, resource composition, lifecycle semantics, compatibility route, and approval card in section 25; no RFC is accepted yet.
3. **Binding-schema draft:** a separate non-default PR materializes every effect-intent schema, action-rule/evidence-profile schema, and immutable binding manifest with actual content-addressed refs and digests. It contains no placeholder or mutable binding and does not change currentness.
4. **Binding-manifest approval:** stewards review the exact schema bytes and manifest digests against the approved semantic profiles. Any semantic change returns to step 2.
5. **Accepted RFC and action matrix:** a separate governed PR promotes the approved prose and exact v0.2 matrix while pinning the reviewed binding-manifest revision/digest. Accepted prose cannot point at schemas that do not yet exist.
6. **Remaining draft/non-default contracts:** separate bounded PRs add authority-source, snapshot, request-rejection, decision, approval/challenge, consumption, governed-read, and effect-receipt v0.2 schemas, examples, and validation without currentness promotion.
7. **Hostile conformance:** a separate PR adds the production-reachable cases in section 22 and publishes the result.
8. **Explicit promotion:** after hostile review and steward approval, a separate PR changes current/default indexes and generated navigation.
9. **OFARM2 extraction:** promoted canonical assets are copied byte-for-byte and verified by digest.
10. **OFARM2 implementation:** only then may `OFARM2#359` resume against the promoted policy and contracts.

No step is implied by completion of the prior step. Each PR retains one primary trust boundary and names any dependency on the prior step. CP15 human governance applies to current/default promotion.

---

## 25. Steward approval card

Before accepted-law work begins, stewards should record explicit decisions for all items:

| Decision | Proposed answer | Approval required |
|---|---|---|
| Are principal resolution, CP3 posture, and human finalization separate axes while AI disclosure stays non-authoritative? | yes | yes |
| Does the authorization RFC preserve all five accepted CP3 posture values without editing CP3 semantics? | yes | yes |
| Must organization representation record the natural-person principal, represented Party, and immutable representation basis separately? | yes | yes |
| Is every software-agent authority subject derived per candidate path from a closed immutable direct-grant, representation, or delegation basis, never from sponsor identity? | yes | yes |
| Are action stage and authority family policy-derived rather than caller-selected? | yes | yes |
| Is the exact matrix in section 7 the v0.2 closure, including delegation, CP3 posture, resources, subjects, and existence postures? | yes | yes, row-by-row amendments allowed |
| Must the immutable action rule select every policy-derived field in section 7.4? | yes | yes |
| Must each rule select an exact effect-intent schema ref/version/digest from a reviewed binding manifest rather than accept a caller-selected schema? | yes | yes |
| Must actual schema bytes and their binding manifest exist and be reviewed before accepted-RFC/action-matrix promotion? | yes | yes |
| Are pack resource requirements conjunctive `ALL_OF`, and assembly alternatives exact `ONE_OF`, with named roles/cardinality? | yes | yes |
| Is `OUTPUT_FILE_SUBMISSION_ASSEMBLY` fixed to `ATTEST_SIGN`? | yes | yes |
| Are no existing actions granted lineage inheritance? | yes | yes |
| Is current authority always checked at trusted evaluation/effect time, with historical subject-time authority only as a second rule? | yes | yes |
| Must every decision and human approval bind the exact JCS/SHA-256 effect-intent digest? | yes | yes |
| Do all current rows use `TRANSACTION_BOUND_30S_V0_2`, with an exact `PT30S` maximum and the minimum-cutoff function in section 18.2? | yes | yes |
| Are state-affecting decisions single-use with policy-bounded expiry? | yes | yes |
| Must internal effects and decision evidence commit in one serializable transaction? | yes | yes |
| Must external effects use a digest-bound idempotent outbox and dispatch receipt? | yes | yes |
| Does every external row declare outbox-final versus dispatch-current authority, with formal filing dispatch-current by default? | yes | yes |
| Is dispatch after `decisionValidUntil` always forbidden, with clock-dependent authority/evidence rechecked even when watermarks do not change? | yes | yes |
| Does actual `RECEIVE_READ_DATA` use `AGENT_ALLOWED_WITH_POLICY_CHECK` plus mandatory CP2 qualification, while preflight-only never discloses protected bytes? | yes | yes |
| Must governed reads authorize, retrieve, redact, qualify, hash, and persist evidence under one snapshot before disclosure? | yes | yes |
| Are protected streams permitted only from a complete precommitted immutable chunk manifest? | yes | yes |
| Are `AuthorizationApprovalChallenge` and `AuthorizationHumanApproval` required for fresh approval, with challenge/final snapshot equality and atomic single-use consumption? | yes | yes |
| May a direct natural person satisfy `FA` only through that lifecycle under `SELF_APPROVAL_ALLOWED`, while `DISTINCT_APPROVER_REQUIRED` needs another eligible principal? | yes | yes |
| Do current `FA` rows use `FRESH_APPROVAL_SELF_5M_V0_2` with exact `PT5M` challenge/approval maxima? | yes | yes |
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
| Are malformed/base-schema/intent-schema failures ingress rejections outside the authorization outcome lattice? | yes | yes |
| Is the decision-bundle digest exactly the JCS/SHA-256 projection in section 18.8, excluding only the two enumerated JSON Pointers? | yes | yes |
| Must non-`ALLOW` bundles commit before transport errors are returned? | yes | yes |
| Does honest v0.2 require versioned source, snapshot, rejection, decision, approval, consumption, governed-read, and effect-receipt records? | yes | yes |
| Does current/default promotion remain a separate final step? | yes | yes |

Any amendment must state whether it changes only this authorization boundary. A requested authentication, principal-resolution, key-custody, database, or runtime-integration change must be split.

---

## 26. Completion criteria for Phase A

Phase A is complete when:

- this candidate is reviewed against issue `samovers/OFARM#10`;
- every acceptance criterion has a proposed disposition;
- the source-record versioning decision is explicit;
- the CP3 compatibility mapping is accepted without changing CP3 semantics, or a separate stacked change is named;
- the actual-read mapping to policy check plus mandatory CP2 qualification is explicitly accepted;
- the action matrix, complete rule fields, rule-selected intent-schema profiles, binding-manifest prerequisite, and composite resource/subject/existence closure are reviewed;
- the temporal, effect-intent, replay, atomic-write, governed-read, dispatch-current, aggregation, and reconstruction rules are reviewed;
- the path-specific software-agent authority-subject bases are accepted without sponsor inference;
- the human challenge/approval, snapshot-equality, self/distinct-approver, expiry, and atomic-consumption lifecycle is reviewed;
- ingress rejection is kept outside the authorization outcome lattice and the exact digest projection is reviewed;
- migration and currentness rules are accepted or amended;
- hostile cases are judged sufficient to detect weaker-schema substitution, composite-resource escape, read leakage, expired dispatch, approval rollover/replay, ambiguous agent authority, malformed input, nested digest-field injection, and other fail-open behavior;
- the trust boundary remains authorization law and machine-contract governance; and
- no active authority or schema was changed by the candidate PR.

What is next: steward review and explicit semantic approval before any accepted-RFC or machine-contract edit.
