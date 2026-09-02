# OFARM Executable Authorization Constraints and Decision Evidence RFC v0.2

Date: 2026-08-31
Status: Phase A RFC candidate for issue `samovers/OFARM#10`, amended under `samovers/OFARM#18`; non-authoritative, not accepted law, and not a current/default machine contract
Triggered by: review of `samovers/OFARM2#353` and draft `samovers/OFARM2#359`
Blocks: `samovers/OFARM2#353` and draft `samovers/OFARM2#359` until accepted semantics, promoted contracts, and byte-identical extraction exist
Scope: define reviewable authorization semantics and the exact versioned contract delta needed before an implementation can claim a durable, fail-closed authorization decision

---

## 1. Decision requested

This candidate asks OFARM stewards to approve, reject, or amend one bounded design:

1. authorization-relevant principal resolution comes from a trusted boundary, while software-agent action posture preserves the accepted five-state CP3 model and remains independent from optional AI-assistance metadata;
2. the action class selects every policy-derived field from one immutable rule, including authority family, stage, inheritance/delegation ceilings, a closed authorization-view extractor, resource roles, effect subject, exact effect-intent schema binding, protected-effect contract binding where applicable, evidence, validity, historical-authority, external-effect, agent, approval, and consumption posture;
3. purpose is a closed, exact-match use constraint in v0.2, not a comparison between unrelated free-text fields;
4. untyped or unsupported conditions never evaluate to true;
5. required evidence is usable only under an active evidence-eligibility policy;
6. authority-target proof, typed input proof, effect-subject proof, scope proof, role scope, grant scope, delegation source, sharing basis, and revocation posture are independently evaluated and durably recorded, while every v0.2 authority source is bound to the exact action-rule meaning under which it was issued and has one immutable record identity;
7. the exact effect intent, trusted evaluation time, current authority snapshot, validity window, consumption mode, and challenge-based human approval are cryptographically bound and consumed under one lifecycle;
8. ingress rejection, request/result/trace evidence, internal writes, buffered governed reads, human-final outbox commitment, and non-`ALLOW` persistence have deterministic fail-closed authorization obligations and an exact digest projection, while every display or payload receipt states whether its bytes are retained and reconstructible or only digest-verifiable; and
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

Sections that define atomic effect and outbox evidence state only the authorization-side conformance condition under which a decision or receipt claim is truthful. They do not define domain result mappings, implement a transaction manager or dispatcher, authorize external byte release, choose retention or encryption policy, or perform runtime integration in this PR. Protected-effect contracts (`samovers/OFARM#12`), the final `ReviewDecision` contract (`samovers/OFARM#15`), transport-release eligibility (`samovers/OFARM#13`), evidence retention/key custody (`samovers/OFARM#14`), the governed interactive-approval transaction protocol (`samovers/OFARM#19`), and any CP2 machine-contract extension remain separate prerequisite or follow-up trust-boundary changes.

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
- accepted CP2 compatibility mapping: yes, reusing CP2 qualification and registered RuntimeProblem semantics without changing its active contracts in this PR;
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
- v0.2 authority sources are not yet bound to the exact action-rule meaning under which the grantor consented;
- the candidate's logical source-revision language conflicts with `RevocationDecision v0.1`, which can name only an artifact family and reference;
- no immutable action rule selects an exact operation-specific effect-intent schema, authorization-view extractor, resource-role policy, evidence profile, historical posture, or external-effect posture;
- v0.1 actor fields do not separately identify the authenticated principal, represented Party, representation basis, CP3 action posture, and human-finalization requirement;
- current CP3 does not establish one global software-agent authority subject, because valid grant/delegation subjects can differ by candidate path;
- fresh human approval has no governed challenge, display, authority-relevant-state comparison, exact approver-eligibility, expiry, or atomic-consumption contract;
- actual governed reads lack a same-snapshot authorization/retrieval/qualification/result-coverage protocol, while preflight-only cannot truthfully authorize disclosure;
- operation claims and execution reports can conflate the current reporter with the alleged historical performer;
- schema-invalid input cannot truthfully become a validated authorization refusal bundle;
- formal filing does not identify whether the human act or later transport is the authority-bearing linearization point, and decision-bundle digest projection lacks exact JSON Pointer rules;
- a completed human filing act does not by itself answer whether protected bytes may still be released to the destination under current sovereignty and disclosure law;
- `AuthorizationDecisionTrace` cannot identify the exact policy version and digest used;
- the trace cannot record trusted principal resolution, the typed derived resource view, prospective effect subject, generic scope proof, or constraint evidence;
- `dataSovereigntyBoundaryRefs` is specific to actual `DataSovereigntyBoundary` records and cannot truthfully hold arbitrary proof references;
- a role-targeted grant can appear to escape the referenced `RoleAssignment.anchorScopes` if only the grant scope is checked;
- current narrowing revocations name modes but do not carry enough closed operands to evaluate every narrowing deterministically;
- v0.1 does not define whether partial constraints from different grant paths may be unioned, how mixed path outcomes aggregate, or which immutable source record identities/digests were visible to the evaluator;
- hash-only approval displays and read payloads cannot support a claim of byte reconstruction when the covered representation is not retained; and
- an authorization-only minimum-disclosure projection can hide permission, review, or redaction posture required by accepted CP2.

Without closure, one runtime can silently normalize a purpose, another can ignore it, a third can treat free-text conditions as descriptive, and all three can claim conformance. That is an authorization trust failure, not merely an interoperability inconvenience.

---

## 5. Core safety stance

### 5.1 `ALLOW` is a complete-proof claim

`ALLOW` means one permitted authorization path has independently satisfied every constraint of the **authority gate** under one identified policy bundle.

Absence of a prohibition is not proof of authority.

`ALLOW` is necessary but not sufficient for a protected effect. The active Platform `EnforcementChain` still controls ingress, validation, pack applicability, evidence, review/promotion, materialization, and publication/export gates. This candidate neither duplicates those gates nor turns an authority result into a whole-chain success claim.

### 5.2 Caller assertions do not create policy facts

A caller may request an action, submit the exact rule-valid effect intent, disclose optional AI assistance, and provide retrieval hints. The rule-selected authorization-view extractor derives the authority target, other typed inputs, effect subject, scope, twin, subject time, and use purpose from that one intent. The caller may not submit mirrored authoritative copies of those facts or choose:

- the required authority family;
- the action stage;
- the governing effect-intent schema or schema digest;
- resource roles, kinds, composition, or cardinality;
- whether revocation is checked;
- whether the authenticated principal is a natural person or software agent;
- the actor's accountable sponsor;
- the authority target, other typed inputs, or the effect subject's kind or existence posture;
- the scope relationship;
- the policy version;
- decision validity, historical-authority, external-effect, approval, or consumption posture; and
- whether evidence is required, current, and eligible.

Those facts come from trusted resolution or from the selected policy bundle.

### 5.3 Unknown does not become false, and false does not become true

Missing AI disclosure does not prove that no AI participated. Missing condition semantics does not mean the condition passed. Missing proof does not mean the relationship is obvious. An unknown or unsupported authority-relevant fact produces a non-`ALLOW` outcome.

### 5.4 Partial paths are not unioned

An evaluator must not combine the action coverage of one grant, the purpose coverage of a second grant, and the evidence coverage of a third grant to manufacture a complete path. Each direct, delegated, or SharingGrant access path must be sufficient by itself. Section 13 evaluates an independently sufficient `RECEIVE_READ_DATA` access basis together with its resource-control constraints in one decision; it does not union partial authority between paths or layers.

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

`AGENT_PARTY_DIRECT_GRANT` binds the recognized agent Party/identity, active CP3 actorship evidence, and immutable direct or role-targeted grant record identity/digest.

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
- the derived authority target, typed inputs, and effect-subject identities;
- the policy digest;
- both challenge/final `authorityEvaluationSnapshotRef` values and their equal `authorityRelevantStateDigest`;
- `decisionValidUntil`; and
- the represented Party and representation basis, when applicable.

`DIRECT_HUMAN_ACTION_REQUIRED` requires the authenticated direct principal for the protected action to be a natural person. A sponsor approval of an agent request does not convert an agent into the direct human actor.

Approval for a different digest, policy, snapshot, Party, or validity window is not reusable.

For `FRESH_HUMAN_APPROVAL_REQUIRED`, the action rule also selects exactly one `approvalSeparationPolicy`:

- `SAME_PRINCIPAL_ALLOWED`
- `DISTINCT_APPROVER_REQUIRED`

`DISTINCT_APPROVER_REQUIRED` is a reserved closed token for a future action rule. Every current `FRESH_HUMAN_APPROVAL_REQUIRED` row selects `SAME_PRINCIPAL_ALLOWED`; no current v0.2 action may emit a distinct-approver disposition.

Every approver must independently satisfy a natural-person authority path for the same action, authority target, effect subject, scope, purpose, and effect intent. Sponsor status alone is never eligibility. A direct natural-person invocation may satisfy the fresh-approval requirement only through the governed challenge/approval lifecycle in section 18 and only when `SAME_PRINCIPAL_ALLOWED`. `DIRECT_HUMAN_ACTION_REQUIRED` is satisfied by the authenticated natural person performing the exact protected action; it does not require a separate approver unless a stronger action rule says so.

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

Agent-posture codes preserve CP3: `PC` = `AGENT_ALLOWED_WITH_POLICY_CHECK`, `PF` = `AGENT_ALLOWED_WITH_PREFLIGHT_ONLY`, `HA` = `AGENT_ALLOWED_WITH_HUMAN_APPROVAL`, and `HU` = `HUMAN_ONLY`. `PF` and the stronger `PROHIBITED_FOR_AGENT` value remain reserved for future action-rule selection; no current v0.2 row selects either value.

Human-finalization codes are `NR` = `NOT_REQUIRED`, `FA` = `FRESH_HUMAN_APPROVAL_REQUIRED`, and `DH` = `DIRECT_HUMAN_ACTION_REQUIRED`.

Existence codes are `E` = `EXISTING_REQUIRED` and `P` = `PROSPECTIVE_TARGET_ALLOWED`.

| Action class | Authority family | Stage | Inheritance | Delegation | Agent posture | Human finalization | Resource requirement policy | Effect subject / existence |
|---|---|---|---|---|---|---|---|---|
| `OBSERVE_CREATE_OBSERVATION` | `OBSERVE_REPORT` | `DRAFT_PREPARATION` | D | DA | PC | NR | `RP_SCOPE_ONE` | `OBSERVATION` / P |
| `OBSERVE_ATTACH_EVIDENCE` | `OBSERVE_REPORT` | `DRAFT_PREPARATION` | D | DA | PC | NR | `RP_EVIDENCE_TARGET_ONE` | `EVIDENCE_LINK` / P |
| `ASSERT_STRUCTURE` | `ASSERT_SUBMIT` | `DRAFT_PREPARATION` | X | DX | HA | FA | `RP_SCOPE_ONE` | `STRUCTURE_ASSERTION` / P |
| `ASSERT_OPERATION_CLAIM` | `ASSERT_SUBMIT` | `DRAFT_PREPARATION` | D | DA | PC | NR | `RP_SCOPE_ONE` | `OPERATION_ASSERTION` / P |
| `ASSERT_COMPLIANCE` | `ASSERT_SUBMIT` | `DRAFT_PREPARATION` | X | DX | HA | FA | `RP_SCOPE_ONE` | `COMPLIANCE_ASSERTION` / P |
| `OPERATE_PLAN_INTERVENTION` | `OPERATE_INTERVENE` | `DRAFT_PREPARATION` | D | DA | PC | NR | `RP_SCOPE_ONE` | `INTERVENTION_PLAN` / P |
| `OPERATE_REPORT_EXECUTION` | `OPERATE_INTERVENE` | `DRAFT_PREPARATION` | D | DA | PC | NR | `RP_SCOPE_ONE` | `EXECUTION_REPORT` / P |
| `REVIEW_REQUEST` | `REVIEW` | `DRAFT_PREPARATION` | X | DA | PC | NR | `RP_REVIEW_TARGET_ONE` | `REVIEW_REQUEST` / P |
| `REVIEW_ACCEPT` | `GOVERN_DECIDE` | `PROMOTION` | N | DP | HU | DH | `RP_FINAL_REVIEW_CASE_ELIGIBLE_TARGET_ONE` | `REVIEW_DECISION` / P |
| `REVIEW_REJECT_OR_CONTEST` | `GOVERN_DECIDE` | `PROMOTION` | N | DP | HU | DH | `RP_FINAL_REVIEW_CASE_ELIGIBLE_TARGET_ONE` | `REVIEW_DECISION` / P |
| `REVIEW_SUPERSEDE` | `GOVERN_DECIDE` | `PROMOTION` | N | DP | HU | DH | `RP_FINAL_REVIEW_TARGET_ONE` | `REVIEW_DECISION` / P |
| `CONTEXT_INSTALL_PACK` | `CONTEXT_GOVERNANCE` | `CONTEXT_ACTIVATION` | N | DP | HU | DH | `RP_PACK_INSTALL` | `PACK_INSTALLATION` / P |
| `CONTEXT_ACTIVATE_PACK` | `CONTEXT_GOVERNANCE` | `CONTEXT_ACTIVATION` | N | DP | HU | DH | `RP_PACK_ACTIVATE` | `STRUCTURE_EVENT` / P |
| `CONTEXT_DEACTIVATE_PACK` | `CONTEXT_GOVERNANCE` | `CONTEXT_ACTIVATION` | N | DP | HU | DH | `RP_PACK_DEACTIVATE` | `STRUCTURE_EVENT` / P |
| `OUTPUT_APPROVE_DOCUMENT_ASSEMBLY` | `ATTEST_SIGN` | `PUBLICATION` | N | DP | HU | DH | `RP_ASSEMBLY_ONE` | `ASSEMBLY_APPROVAL` / P |
| `OUTPUT_ATTEST_DOCUMENT_ASSEMBLY` | `ATTEST_SIGN` | `ATTESTATION` | N | DP | HU | DH | `RP_ASSEMBLY_ONE` | `ASSEMBLY_ATTESTATION` / P |
| `OUTPUT_FILE_SUBMISSION_ASSEMBLY` | `ATTEST_SIGN` | `PUBLICATION` | N | DX | HU | DH | `RP_SUBMISSION_ONE` | `SUBMISSION_FILING` / P |
| `SHARE_GRANT_ACCESS` | `SHARE_REVOKE` | `PROMOTION` | X | DA | HA | FA | `RP_SHARE_ARTIFACT_ONE` | `SHARING_GRANT` / P |
| `SHARE_REVOKE_ACCESS` | `SHARE_REVOKE` | `PROMOTION` | X | DA | HA | FA | `RP_SHARE_REVOKE` | `REVOCATION_DECISION` / P |
| `RECEIVE_READ_DATA` | `RECEIVE_USE` | `QUERY_READ` | D | DA | PC | NR | `RP_READ_TARGET_ONE` | `DATA_DISCLOSURE` / P |

### 7.3 Matrix rules

The inheritance entry is a ceiling, not a grant. A source record may narrow `D` to `X` or `N`, and may narrow `X` to `N`. It may not broaden the row. A row marked `N` must use `NO_INHERIT`.

The delegation entry is also a ceiling. Its intersection with source permission and the DelegationGrant is defined in section 10. Prose such as "with caution" has no executable meaning in v0.2.

All 20 proposed v0.2 rows use `SINGLE_USE`. No v0.2 row authorizes replay.

Each `resourceRequirementPolicy` derives one and only one `AUTHORITY_TARGET` plus any integrity, applicability, or state inputs needed to validate the exact effect. Only the authority target is matched to grant/role scope. Other inputs cannot create authority and cannot be used to combine partial grants. `effectSubject` is the object acted on or created. Sections 7.5 and 8 define the separation.

For `CONTEXT_INSTALL_PACK`, the effect intent binds an existing content-addressed `PACK_RELEASE` or `PACK_ARTIFACT`; `PACK_INSTALLATION` is the prospective result. Activation and deactivation each create a prospective `STRUCTURE_EVENT`, consistent with the active Event Grammar. Their intents bind the current activation state and the complete proposed successor state. The previous activation set remains immutable.

For `ASSERT_COMPLIANCE`, compiled outputs may be immutable evidence or effect-intent inputs, but the effect subject is the prospective compliance assertion. A runtime must not substitute a compiled-output reference for the assertion body covered by `effectIntentDigest`.

`OUTPUT_FILE_SUBMISSION_ASSEMBLY` resolves the v0.1 alternative family to `ATTEST_SIGN` for v0.2. The authenticated human's commit of the exact immutable filing envelope to the governed outbox is the final authority-bearing filing act. It does not authorize disclosure by itself. A transport worker does not perform this action class and may release only the committed bytes after the separate current transport-release gate in section 18.6 passes. A deployment that needs authority-bearing transmission must propose a separate action class rather than reinterpret this one locally.

Unknown action classes, resource kinds, effect-subject kinds, existence postures, stages, or policy rules are non-`ALLOW`.

The resource/subject list is a proposed closure point and requires specific steward approval. It must not be inferred from the word "typical" in the v0.1 matrix.

### 7.4 Complete `ActionAuthorizationRule`

The core row and its extension row form one immutable `ActionAuthorizationRule`. Every rule must carry:

- `ruleId`;
- action class, authority family, and stage;
- inheritance ceiling and delegation ceiling;
- exact CP3 agent-action posture and human-finalization requirement;
- immutable `humanApprovalPolicy` where human approval applies, including display/renderer profile, content-addressed evidence-retention policy, approver eligibility, separation, trusted session/transaction cutoff inputs, and single-use posture;
- `resourceRequirementPolicy` with named roles, cardinality, and composition;
- effect-subject kind and existence posture;
- one closed `effectIntentSchemaBinding`;
- one immutable `protectedEffectContractBinding` for every state-affecting action, or explicit `NO_STATE_EFFECT` for the governed-read action;
- one closed `authorizationViewExtraction`, including content-addressed ref/digest and exact JSON Pointer mappings from the validated effect intent to the authority target, typed inputs, effect subject, scope, twin, subject time, and use purpose;
- `decisionValidityPolicy`, including policy ref/digest, cutoff inputs, and calculation;
- `historicalAuthorityPosture`;
- `externalEffectPosture`;
- exact action-level evidence-policy bindings, including explicit `NONE`;
- `consumptionMode`; and
- immutable `ruleRevision` and `ruleDigest` over the complete resolved per-action semantic closure.

`effectIntentSchemaBinding` contains exactly:

- content-addressed `schemaRef`;
- `schemaVersion`;
- `schemaDigest`;
- `canonicalization`, fixed to `JCS_RFC8785_SHA256`; and
- one effect-intent profile ID from section 7.6.

For a state-affecting action, `protectedEffectContractBinding` contains a content-addressed contract ref, version, digest, and owning domain-contract family. The referenced contract, not this authorization RFC, owns the result schema, intent-to-result mapping, permitted derived fields, forbidden widening, event/commit classification, and postconditions. The authorization rule merely pins the exact contract that another applicable EnforcementChain gate must validate before commit. Missing, mutable, or digest-invalid effect-contract bindings make the rule non-executable. This Phase A PR neither creates those contracts nor moves their domain semantics into the authorization evaluator.

`authorizationViewExtraction` is declarative data, not caller data or executable plugin code. It lists required source JSON Pointers, destination fields, allowed concrete kinds, and canonical transformations; v0.2 permits identity extraction only. Every required pointer must resolve exactly once. Missing, duplicated, type-invalid, or conflicting extracted facts make the request invalid before path evaluation. A caller-provided mirrored resource, subject, scope, twin, time, purpose, destination, grantee, or rights field is prohibited by the request schema.

The caller submits an effect-intent instance. The selected action rule chooses the schema. A caller schema claim, if present for diagnostics, is non-authoritative and must exactly equal the rule binding. A mismatch is an ingress rejection; a caller can never select a weaker schema.

Phase A names the exact semantic profiles. Before accepted-RFC/action-matrix promotion, the draft-schema stage must materialize their bytes and produce a reviewed binding manifest containing every content-addressed ref and digest. Missing, placeholder, mutable, or mismatched bindings make the action rule invalid and non-executable. Accepted promotion cannot precede that manifest.

The profile IDs in sections 7.5 through 7.8 are review keys, not runtime indirection. The binding manifest maps each action class to exactly one complete resolved rule containing the actual schema/policy refs and digests, and the accepted action-rule bundle digest covers those resolved values. A runtime cannot follow a mutable registry entry or choose among schemas sharing a profile ID.

`ruleDigest` is `sha256:` plus the SHA-256 digest of the JCS representation of the complete resolved per-action semantic closure after removing exactly the top-level `/ruleDigest` member. The closure contains every field of the resolved `ActionAuthorizationRule` and immutable content-addressed bindings for every shared authorization component whose semantics can change eligibility or increase authority for that action. At minimum, it binds authority-family and exact purpose-token comparison, resource-role and authority-target interpretation, role/grant/scope/inheritance/delegation/sharing intersections, trusted-time and revocation application, evidence/sovereignty/proof and tenant interpretation, prohibition on combining partial paths, path sufficiency and selection, and the total outcome aggregation lattice. Imported semantics remain owned by their governing contracts; the resolved rule binds their immutable refs and digests rather than copying their implementations into this RFC.

The semantic closure excludes unrelated action rules and changes that affect only diagnostic wording, logging, diagnostic presentation, or other behavior that cannot alter this action's eligibility or authority. A component cannot be excluded merely because shared policy prose or a shared algorithm defines it rather than the visible matrix row. A missing, mutable, unresolved, or digest-invalid closure binding makes the action rule invalid and non-executable with `ACTION_RULE_BINDING_INVALID` at ingress. When an included component changes and the rule is validly repackaged, `ruleDigest` changes even if every visible row field is unchanged; a source carrying the prior digest then fails exact source-rule comparison with `SOURCE_RULE_BINDING_MISMATCH`.

This closure is a deterministic packaging rule inside the existing binding manifest. It creates no new top-level contract family or mutable semantics registry, does not compare the complete policy-bundle digest for source reuse, and does not introduce cross-digest compatibility or semantic-subset proof.

Every v0.2 row selects `TRANSACTION_BOUND_V0_2`. It requires consumption in the same final governed transaction as the protected effect, buffered read-evidence commit, or filing-outbox commit and uses the exact cutoff function in section 18.2. This authorization candidate neither requires an interactive database transaction to remain open while a human considers a challenge nor selects a reservation/finalization protocol. The separately owned governed-transaction contract in `samovers/OFARM#19` must close that runtime protocol before machine materialization or implementation. This candidate does not invent a universal wall-clock duration unsupported by an authoritative transaction contract.

Every `SA` row selects `FRESH_APPROVAL_SAME_ACTION_AUTHORITY_V0_2`: `SAME_PRINCIPAL_ALLOWED` and `SINGLE_USE`. `challengeExpiresAt` is the earliest trusted interactive-session expiry or relevant authority/policy/resource/evidence cutoff. `approvalExpiresAt` is the earlier of `challengeExpiresAt` and the final protected-effect transaction deadline. The profile does not invent a global duration or assume that an agent sponsor is eligible. The approver must independently satisfy a natural-person authority path for the same action, extracted authorization view, effect subject, and effect intent as defined in section 18.3. `NA` binds explicit `NO_SEPARATE_APPROVAL_POLICY`; it does not weaken a row's independent `DIRECT_HUMAN_ACTION_REQUIRED` posture. A future distinct-approver row must bind a new immutable profile with exact prohibited relationships.

### 7.5 Resource-role policies

The rule-selected extractor produces a typed resource view. Each role has one posture:

- `AUTHORITY_TARGET`: the single governed object against which the selected grant or role anchor is matched;
- `INTEGRITY_INPUT`: immutable content whose identity/digest must be verified but which grants no authority;
- `APPLICABILITY_INPUT`: immutable policy/registry state used by another EnforcementChain gate and never treated as an authority grant;
- `STATE_INPUT`: immutable current state needed to define a prospective transition and never mutated in place; or
- `EVIDENCE_INPUT`: typed evidence evaluated only under section 12.

Every current policy has exactly one `AUTHORITY_TARGET`. A sufficient path must cover that target by itself; it may not combine authority over different roles or different target branches. `ALL_OF` below means all validation inputs are present, not that separate grants are unioned. `ONE_OF` selects exactly one authority-target branch.

For non-authority inputs, this gate proves only the exact immutable binding, allowed kind, cardinality, tenant/scope relationship, and current revision needed to identify the protected intent. It does not turn `APPLICABILITY_INPUT` into a pack-applicability result or otherwise claim that a non-authority EnforcementChain gate passed.

Closed scope kinds are `FARM`, `SITE`, `FIELD`, `ZONE`, `CROP_CYCLE`, `LOT`, `FACILITY`, `OPERATION`, `DEPLOYMENT`, and `TENANT`. Closed record/artifact sets are enumerated in each policy; tokens such as `GOVERNED_SCOPE`, `GOVERNED_RECORD`, `SHARED_ARTIFACT`, and `DATA_RESOURCE` are not executable v0.2 kinds.

| Policy ID | Composition | Named requirements |
|---|---|---|
| `RP_SCOPE_ONE` | `ALL_OF` | `TARGET_SCOPE` (`AUTHORITY_TARGET`): exactly 1 closed scope kind |
| `RP_EVIDENCE_TARGET_ONE` | `ALL_OF` | `PRIMARY_RECORD` (`AUTHORITY_TARGET`): exactly 1 of `OBSERVATION`, `STRUCTURE_ASSERTION`, `OPERATION_ASSERTION`, `COMPLIANCE_ASSERTION`, `INTERVENTION_PLAN`, `EXECUTION_REPORT`, `REVIEW_REQUEST`, `REVIEW_DECISION`, `DOCUMENT_ASSEMBLY`, `DOSSIER_ASSEMBLY`, or `SUBMISSION_ASSEMBLY`; `ATTACHED_EVIDENCE` (`EVIDENCE_INPUT`): exactly 1 `EVIDENCE_RECORD` |
| `RP_REVIEW_TARGET_ONE` | `ALL_OF` | `PRIMARY_RECORD` (`AUTHORITY_TARGET`): exactly 1 of `STRUCTURE_ASSERTION`, `OPERATION_ASSERTION`, `COMPLIANCE_ASSERTION`, `INTERVENTION_PLAN`, `EXECUTION_REPORT`, `REVIEW_REQUEST`, `DOCUMENT_ASSEMBLY`, `DOSSIER_ASSEMBLY`, or `SUBMISSION_ASSEMBLY` |
| `RP_FINAL_REVIEW_TARGET_ONE` | `ALL_OF` | `PRIMARY_RECORD` (`AUTHORITY_TARGET`): exactly 1 of `STRUCTURE_ASSERTION`, `OPERATION_ASSERTION`, `COMPLIANCE_ASSERTION`, `INTERVENTION_PLAN`, `EXECUTION_REPORT`, `REVIEW_REQUEST`, `DOCUMENT_ASSEMBLY`, `DOSSIER_ASSEMBLY`, `SUBMISSION_ASSEMBLY`, or `ACCEPTED_EVENT_CONSEQUENCE` |
| `RP_FINAL_REVIEW_CASE_ELIGIBLE_TARGET_ONE` | `ALL_OF` | `PRIMARY_RECORD` (`AUTHORITY_TARGET`): exactly 1 of `STRUCTURE_ASSERTION`, `OPERATION_ASSERTION`, `COMPLIANCE_ASSERTION`, `INTERVENTION_PLAN`, `EXECUTION_REPORT`, `REVIEW_REQUEST`, `DOCUMENT_ASSEMBLY`, `DOSSIER_ASSEMBLY`, `SUBMISSION_ASSEMBLY`, `ACCEPTED_EVENT_CONSEQUENCE`, or `EVIDENCE_SUFFICIENCY_CASE` |
| `RP_PACK_INSTALL` | `ALL_OF` | `TARGET_SCOPE` (`AUTHORITY_TARGET`): exactly 1 closed scope kind; `PACK_REGISTRY` (`APPLICABILITY_INPUT`): exactly 1 `PACK_REGISTRY`; `PACK_RELEASE_INPUT` (`INTEGRITY_INPUT`): exactly 1 `PACK_RELEASE` or `PACK_ARTIFACT` |
| `RP_PACK_ACTIVATE` | `ALL_OF` | `TARGET_SCOPE` (`AUTHORITY_TARGET`): exactly 1 closed scope kind; `PACK_REGISTRY` (`APPLICABILITY_INPUT`): exactly 1 `PACK_REGISTRY`; `PACK_RELEASE_INPUTS` (`INTEGRITY_INPUT`): 1 or more `PACK_RELEASE` or `PACK_ARTIFACT`; `CURRENT_ACTIVATION_SET` (`STATE_INPUT`): exactly 1 `PACK_ACTIVATION_SET` |
| `RP_PACK_DEACTIVATE` | `ALL_OF` | `TARGET_SCOPE` (`AUTHORITY_TARGET`): exactly 1 closed scope kind; `PACK_REGISTRY` (`APPLICABILITY_INPUT`): exactly 1 `PACK_REGISTRY`; `CURRENT_ACTIVATION_SET` (`STATE_INPUT`): exactly 1 `PACK_ACTIVATION_SET` |
| `RP_ASSEMBLY_ONE` | `ONE_OF` | `PRIMARY_ASSEMBLY` (`AUTHORITY_TARGET`): exactly 1 `DOCUMENT_ASSEMBLY`; or `PRIMARY_DOSSIER` (`AUTHORITY_TARGET`): exactly 1 `DOSSIER_ASSEMBLY` |
| `RP_SUBMISSION_ONE` | `ALL_OF` | `PRIMARY_SUBMISSION` (`AUTHORITY_TARGET`): exactly 1 `SUBMISSION_ASSEMBLY` |
| `RP_SHARE_ARTIFACT_ONE` | `ALL_OF` | `SHARED_ARTIFACT` (`AUTHORITY_TARGET`): exactly 1 of `PASSPORT_VIEW`, `DOCUMENT_ASSEMBLY`, `DOSSIER_ASSEMBLY`, `SUBMISSION_ASSEMBLY`, `EVIDENCE_BUNDLE`, or `CURRENT_STATE_MATERIALIZATION` |
| `RP_SHARE_REVOKE` | `ALL_OF` | `SHARED_ARTIFACT` (`AUTHORITY_TARGET`): exactly 1 kind allowed by `RP_SHARE_ARTIFACT_ONE`; `AFFECTED_SHARING_GRANT` (`STATE_INPUT`): exactly 1 existing `SHARING_GRANT` |
| `RP_READ_TARGET_ONE` | `ALL_OF` | `READ_TARGET` (`AUTHORITY_TARGET`): exactly 1 closed scope kind or exactly 1 of `OBSERVATION`, `EVIDENCE_RECORD`, `STRUCTURE_ASSERTION`, `OPERATION_ASSERTION`, `COMPLIANCE_ASSERTION`, `INTERVENTION_PLAN`, `EXECUTION_REPORT`, `REVIEW_REQUEST`, `REVIEW_DECISION`, `PACK_INSTALLATION`, `PACK_ACTIVATION_SET`, `DOCUMENT_ASSEMBLY`, `DOSSIER_ASSEMBLY`, `SUBMISSION_ASSEMBLY`, `EVIDENCE_BUNDLE`, `CURRENT_STATE_MATERIALIZATION`, `SHARING_GRANT`, `REVOCATION_DECISION`, `PASSPORT_VIEW`, or `AUTHORIZATION_TRACE`; optional query form requires both `QUERY_SPECIFICATION` and `QUERY_PLAN` (`INTEGRITY_INPUT`), exactly 1 each, while direct-read form requires neither |

Every entry binds posture, role, one concrete kind, logical ref, immutable revision/digest, scope, twin where applicable, tenant, and typed proof. An unrecognized posture/role/kind, missing role, excess cardinality, or `ONE_OF` ambiguity is non-`ALLOW`.

`RP_FINAL_REVIEW_TARGET_ONE` preserves the active `ReviewDecision` scope over assertions and accepted event consequences. Its `ACCEPTED_EVENT_CONSEQUENCE` branch resolves exactly one concrete authority target with one logical ref and immutable revision ref or content digest. It remains selected by `REVIEW_SUPERSEDE`.

`RP_FINAL_REVIEW_CASE_ELIGIBLE_TARGET_ONE` adds the active `EVIDENCE_SUFFICIENCY_CASE` family for `REVIEW_ACCEPT` and `REVIEW_REJECT_OR_CONTEST`, the two accepted matrix rows that explicitly carry case scope. That branch also resolves one logical ref and immutable revision ref or content digest. It does not widen `REVIEW_SUPERSEDE`, `REVIEW_REQUEST`, or another action. `REVIEW_REQUEST` retains `RP_REVIEW_TARGET_ONE`; read, evidence-attachment, and every unrelated action policy remain unchanged.

#### 7.5.1 Explicit v0.1-to-v0.2 target delta ledger

The accepted v0.1 matrix labels its target column "Typical target scopes" rather than defining an exhaustive executable set. That wording is not authority to widen or narrow a row silently. The following ledger exposes the nature and, where the target axes are comparable, direction of every proposed v0.2 target change for steward approval; it is governance evidence, not a cross-version compatibility rule.

`WIDENING` adds target kinds without removing an explicitly listed v0.1 kind. `NARROWING` removes an explicit kind or replaces an open-ended v0.1 phrase with a closed set. `MIXED_DELTA` both adds and removes kinds within a comparable target family. `RETYPED` replaces a contextual-scope axis with a record/artifact axis for which no directional set comparison is claimed. `CLOSED_EQUIVALENT` closes an apparent v0.1 target without an intended breadth change. These classifications assume the named mappings in the final column; rejecting a mapping requires a row amendment and a new rule digest.

| Action class | v0.1 typical target | Proposed v0.2 authority target | Direction and explicit delta |
|---|---|---|---|
| `OBSERVE_CREATE_OBSERVATION` | farm, site, field, zone, crop cycle, lot, facility | any of 10 closed scope kinds | `WIDENING`: adds `OPERATION`, `DEPLOYMENT`, and `TENANT` |
| `OBSERVE_ATTACH_EVIDENCE` | observation targets plus operation and submission context | one of 11 named governed-record or assembly kinds | `RETYPED`: replaces contextual-scope targeting with the closed `RP_EVIDENCE_TARGET_ONE` record/artifact axis; no widening, narrowing, or scope-to-record equivalence is inferred |
| `ASSERT_STRUCTURE` | farm, site, field, zone, facility | any of 10 closed scope kinds | `WIDENING`: adds `CROP_CYCLE`, `LOT`, `OPERATION`, `DEPLOYMENT`, and `TENANT` |
| `ASSERT_OPERATION_CLAIM` | field, zone, crop cycle, operation | any of 10 closed scope kinds | `WIDENING`: adds `FARM`, `SITE`, `LOT`, `FACILITY`, `DEPLOYMENT`, and `TENANT` |
| `ASSERT_COMPLIANCE` | field, crop cycle, lot, submission scope | any of 10 closed scope kinds | `MIXED_DELTA`: adds `FARM`, `SITE`, `ZONE`, `FACILITY`, `OPERATION`, `DEPLOYMENT`, and `TENANT`; removes submission scope as an authority-target branch |
| `OPERATE_PLAN_INTERVENTION` | field, zone, crop cycle, operation | any of 10 closed scope kinds | `WIDENING`: adds `FARM`, `SITE`, `LOT`, `FACILITY`, `DEPLOYMENT`, and `TENANT` |
| `OPERATE_REPORT_EXECUTION` | field, zone, crop cycle, operation | any of 10 closed scope kinds | `WIDENING`: adds `FARM`, `SITE`, `LOT`, `FACILITY`, `DEPLOYMENT`, and `TENANT` |
| `REVIEW_REQUEST` | any governed review scope | one of 9 named governed-record or assembly kinds | `NARROWING`: replaces an open-ended review scope with the closed `RP_REVIEW_TARGET_ONE` set |
| `REVIEW_ACCEPT` | assertion, consequence, case scope | one of 11 named final-review targets | `MIXED_DELTA`: adds named plan, report, review-request, and assembly targets while narrowing consequence to `ACCEPTED_EVENT_CONSEQUENCE` and case to `EVIDENCE_SUFFICIENCY_CASE` |
| `REVIEW_REJECT_OR_CONTEST` | assertion, consequence, case scope | one of 11 named final-review targets | `MIXED_DELTA`: adds named plan, report, review-request, and assembly targets while narrowing consequence to `ACCEPTED_EVENT_CONSEQUENCE` and case to `EVIDENCE_SUFFICIENCY_CASE` |
| `REVIEW_SUPERSEDE` | assertion, consequence, state scope | one of 10 named final-review targets | `MIXED_DELTA`: adds named plan, report, review-request, and assembly targets, narrows consequence to `ACCEPTED_EVENT_CONSEQUENCE`, and removes open-ended state scope |
| `CONTEXT_INSTALL_PACK` | farm, site, field, crop cycle | any of 10 closed scope kinds | `WIDENING`: adds `ZONE`, `LOT`, `FACILITY`, `OPERATION`, `DEPLOYMENT`, and `TENANT` |
| `CONTEXT_ACTIVATE_PACK` | farm, site, field, crop cycle, lot, operation | any of 10 closed scope kinds | `WIDENING`: adds `ZONE`, `FACILITY`, `DEPLOYMENT`, and `TENANT` |
| `CONTEXT_DEACTIVATE_PACK` | same as activation scopes | any of 10 closed scope kinds | `WIDENING`: adds `ZONE`, `FACILITY`, `DEPLOYMENT`, and `TENANT` |
| `OUTPUT_APPROVE_DOCUMENT_ASSEMBLY` | report, dossier, submission scope | `DOCUMENT_ASSEMBLY` or `DOSSIER_ASSEMBLY` | `NARROWING`: maps report to `DOCUMENT_ASSEMBLY`, retains dossier, and excludes `SUBMISSION_ASSEMBLY` |
| `OUTPUT_ATTEST_DOCUMENT_ASSEMBLY` | report, dossier, submission scope | `DOCUMENT_ASSEMBLY` or `DOSSIER_ASSEMBLY` | `NARROWING`: maps report to `DOCUMENT_ASSEMBLY`, retains dossier, and excludes `SUBMISSION_ASSEMBLY` |
| `OUTPUT_FILE_SUBMISSION_ASSEMBLY` | submission scope | exactly one `SUBMISSION_ASSEMBLY` | `CLOSED_EQUIVALENT`: closes submission scope to its concrete assembly kind |
| `SHARE_GRANT_ACCESS` | any governed scope | one of 6 named shared-artifact kinds | `NARROWING`: replaces the open-ended governed scope with `RP_SHARE_ARTIFACT_ONE` |
| `SHARE_REVOKE_ACCESS` | any governed scope | one of the same 6 artifact kinds; existing SharingGrant is a state input | `NARROWING`: replaces the open-ended governed scope and does not make the SharingGrant a second authority target |
| `RECEIVE_READ_DATA` | any governed scope | one of 10 closed scope kinds or 20 named record/artifact kinds | `NARROWING`: replaces the open-ended governed scope with the closed `RP_READ_TARGET_ONE` set |

The ledger does not make any v0.1 source executable under v0.2. Exact source migration and rule-binding requirements remain those of section 19.

### 7.6 Effect-intent schema profiles

Every profile has one common authorization envelope inside the effect intent: every resource-role instance required by the selected policy, the effect-subject kind/ref or proposed ID, scope, tenant, twin where applicable, `subjectTime` where applicable, and optional `authorizationUsePurpose`. The extractor maps `authorizationUsePurpose` to `requestedUsePurpose`; it is distinct from an effect field such as the purpose limitation being written into a new SharingGrant.

The table lists additional operation-specific authorization-relevant content that the immutable schema must require. The schema may add governed fields, but a later schema revision that adds, removes, or changes an authorization-relevant field needs a new digest, extractor revision, and reviewed rule binding.

| Profile ID | Required authorization-relevant content |
|---|---|
| `EI_OBSERVATION_CREATE_V0_2` | scope/resource revisions, proposed observation ID, observation type/body, subject time, evidence revision refs |
| `EI_EVIDENCE_LINK_V0_2` | governed-record revision, evidence revision, relation type, subject time |
| `EI_STRUCTURE_ASSERTION_V0_2` | scope revision, proposed assertion ID, assertion body, subject time, evidence revisions |
| `EI_OPERATION_ASSERTION_V0_2` | scope/operation revisions, proposed assertion ID, claim body, closed `claimPosture` (`INTENDED` or `PERFORMED`), subject time, evidence revisions, and required `performedByPartyRef` plus conditional immutable software-agent actorship refs and optional immutable `performerAuthorityEvidenceRefs` when posture is `PERFORMED` |
| `EI_COMPLIANCE_ASSERTION_V0_2` | scope revision, proposed assertion ID, exact claim body, rule/evidence-policy revisions, evidence revisions, subject time |
| `EI_INTERVENTION_PLAN_V0_2` | scope revisions, proposed plan ID/body, intended time, governed inputs |
| `EI_EXECUTION_REPORT_V0_2` | scope, plan/operation revisions, proposed report ID/body, execution time, evidence revisions, required `performedByPartyRef`, conditional immutable software-agent actorship refs when an agent allegedly performed the work, and optional immutable `performerAuthorityEvidenceRefs` |
| `EI_REVIEW_REQUEST_V0_2` | governed-record revision, proposed request ID, review scope, reason, evidence revisions |
| `EI_REVIEW_DECISION_V0_2` | governed-record revision, proposed decision ID, review action fixed by action class, exact `decisionOutcomeState`, rationale, evidence revisions |
| `EI_PACK_INSTALL_V0_2` | scope and registry revisions, exact pack-release ref/digest, installation parameters, requested profiles, exclusions |
| `EI_PACK_ACTIVATE_V0_2` | scope/registry/current-activation-set revisions, every pack-release ref/digest, profiles, exclusions, event kind fixed to `PACK_ACTIVATED`, proposed StructureEvent ID, and complete proposed successor activation-set content |
| `EI_PACK_DEACTIVATE_V0_2` | scope/registry/current-activation-set revisions, exact deactivation selection, event kind fixed to `PACK_DEACTIVATED`, proposed StructureEvent ID, and complete proposed successor activation-set content |
| `EI_ASSEMBLY_APPROVAL_V0_2` | assembly/dossier revision, output profile, approval scope, evidence revisions |
| `EI_ASSEMBLY_ATTESTATION_V0_2` | assembly/dossier revision, attestation statement, signature policy, evidence revisions |
| `EI_SUBMISSION_FILING_V0_2` | submission revision, exact destination, filing mode, immutable envelope bytes/ref and digest, idempotency key, external identifiers, evidence revisions |
| `EI_SHARING_GRANT_V0_2` | immutable artifact revision, exact grantee, rights, delivery mode, resulting-grant purpose constraints, validity, scope, sovereignty revisions |
| `EI_SHARING_REVOKE_V0_2` | proposed RevocationDecision ID; affected family fixed to `SHARING_GRANT`; exact immutable SharingGrant ID/digest and artifact revision; mode fixed to `TERMINATE`; `effectiveFrom`; reason |
| `EI_DATA_READ_V0_2` | immutable read-target revision or QuerySpecification/plan revisions, projection, redaction-policy revision, purpose, buffered-response mode, snapshot policy, aggregate/metadata/lineage disclosure request |

For `EI_REVIEW_DECISION_V0_2`, the selected rule closes the intent's `decisionOutcomeState`: `REVIEW_ACCEPT` requires `ACCEPTED`, `REVIEW_SUPERSEDE` requires `SUPERSEDED`, and `REVIEW_REJECT_OR_CONTEST` requires exactly one intent-bound closed value, either `REJECTED` or `CONTESTED`. That value is part of the single validated effect intent and its digest; no mirrored caller field may select or override it. A result may carry the contract-required outcome, but it cannot independently choose a different one. This authorization closure does not define the `ReviewDecision` result schema, intent-to-result mapping, event/commit classification, or postconditions; the separately owned protected-effect contract must validate those before commit.

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

Validity `TX` means the exact `TRANSACTION_BOUND_V0_2` policy in sections 7.4 and 18.2. Historical posture `C` means `CURRENT_ONLY`; `CR` means `CURRENT_REPORT_AUTHORITY_ONLY`, which authorizes submission now without treating the reporter as the historical performer. No current row performs a historical authority check. External posture `N` means `NO_EXTERNAL_DISPATCH`; `OF` means `OUTBOX_COMMIT_IS_FINAL_FILING_ACT`. Consumption `SU` means `SINGLE_USE`. Approval `SA` means `FRESH_APPROVAL_SAME_ACTION_AUTHORITY_V0_2`; `NA` means `NO_SEPARATE_APPROVAL_POLICY`.

| Action class | Intent profile | Resource policy | Validity | Historical | External | Evidence profile | Consumption | Approval |
|---|---|---|---|---|---|---|---|---|
| `OBSERVE_CREATE_OBSERVATION` | `EI_OBSERVATION_CREATE_V0_2` | `RP_SCOPE_ONE` | TX | C | N | `EP_NONE` | SU | NA |
| `OBSERVE_ATTACH_EVIDENCE` | `EI_EVIDENCE_LINK_V0_2` | `RP_EVIDENCE_TARGET_ONE` | TX | C | N | `EP_EVIDENCE_LINK_ELIGIBILITY_V0_2` | SU | NA |
| `ASSERT_STRUCTURE` | `EI_STRUCTURE_ASSERTION_V0_2` | `RP_SCOPE_ONE` | TX | C | N | `EP_NONE` | SU | SA |
| `ASSERT_OPERATION_CLAIM` | `EI_OPERATION_ASSERTION_V0_2` | `RP_SCOPE_ONE` | TX | CR | N | `EP_NONE` | SU | NA |
| `ASSERT_COMPLIANCE` | `EI_COMPLIANCE_ASSERTION_V0_2` | `RP_SCOPE_ONE` | TX | C | N | `EP_COMPLIANCE_ASSERTION_V0_2` | SU | SA |
| `OPERATE_PLAN_INTERVENTION` | `EI_INTERVENTION_PLAN_V0_2` | `RP_SCOPE_ONE` | TX | C | N | `EP_NONE` | SU | NA |
| `OPERATE_REPORT_EXECUTION` | `EI_EXECUTION_REPORT_V0_2` | `RP_SCOPE_ONE` | TX | CR | N | `EP_EXECUTION_REPORT_V0_2` | SU | NA |
| `REVIEW_REQUEST` | `EI_REVIEW_REQUEST_V0_2` | `RP_REVIEW_TARGET_ONE` | TX | C | N | `EP_NONE` | SU | NA |
| `REVIEW_ACCEPT` | `EI_REVIEW_DECISION_V0_2` | `RP_FINAL_REVIEW_CASE_ELIGIBLE_TARGET_ONE` | TX | C | N | `EP_NONE` | SU | NA |
| `REVIEW_REJECT_OR_CONTEST` | `EI_REVIEW_DECISION_V0_2` | `RP_FINAL_REVIEW_CASE_ELIGIBLE_TARGET_ONE` | TX | C | N | `EP_NONE` | SU | NA |
| `REVIEW_SUPERSEDE` | `EI_REVIEW_DECISION_V0_2` | `RP_FINAL_REVIEW_TARGET_ONE` | TX | C | N | `EP_NONE` | SU | NA |
| `CONTEXT_INSTALL_PACK` | `EI_PACK_INSTALL_V0_2` | `RP_PACK_INSTALL` | TX | C | N | `EP_PACK_GOVERNANCE_V0_2` | SU | NA |
| `CONTEXT_ACTIVATE_PACK` | `EI_PACK_ACTIVATE_V0_2` | `RP_PACK_ACTIVATE` | TX | C | N | `EP_PACK_GOVERNANCE_V0_2` | SU | NA |
| `CONTEXT_DEACTIVATE_PACK` | `EI_PACK_DEACTIVATE_V0_2` | `RP_PACK_DEACTIVATE` | TX | C | N | `EP_PACK_GOVERNANCE_V0_2` | SU | NA |
| `OUTPUT_APPROVE_DOCUMENT_ASSEMBLY` | `EI_ASSEMBLY_APPROVAL_V0_2` | `RP_ASSEMBLY_ONE` | TX | C | N | `EP_OUTPUT_APPROVAL_V0_2` | SU | NA |
| `OUTPUT_ATTEST_DOCUMENT_ASSEMBLY` | `EI_ASSEMBLY_ATTESTATION_V0_2` | `RP_ASSEMBLY_ONE` | TX | C | N | `EP_ATTESTATION_V0_2` | SU | NA |
| `OUTPUT_FILE_SUBMISSION_ASSEMBLY` | `EI_SUBMISSION_FILING_V0_2` | `RP_SUBMISSION_ONE` | TX | C | OF | `EP_FORMAL_FILING_V0_2` | SU | NA |
| `SHARE_GRANT_ACCESS` | `EI_SHARING_GRANT_V0_2` | `RP_SHARE_ARTIFACT_ONE` | TX | C | N | `EP_SHARING_SOVEREIGNTY_V0_2` | SU | SA |
| `SHARE_REVOKE_ACCESS` | `EI_SHARING_REVOKE_V0_2` | `RP_SHARE_REVOKE` | TX | C | N | `EP_SHARING_SOVEREIGNTY_V0_2` | SU | SA |
| `RECEIVE_READ_DATA` | `EI_DATA_READ_V0_2` | `RP_READ_TARGET_ONE` | TX | C | N | `EP_CP2_READ_QUALIFICATION_V0_2` | SU | NA |

---

## 8. Temporal, effect-intent, resource, and proof separation

### 8.1 Materially distinct times

The v0.2 request and trace preserve these distinct times:

- `subjectTime`: the governed occurrence, observation, execution, assertion, or other domain time extracted from the validated effect intent and qualified by the relevant domain contract;
- `authorizationEvaluatedAt`: a trusted runtime clock value for the authority snapshot used to decide the current request;
- `decisionValidUntil`: the latest trusted time at which the exact decision may be consumed;
- `effectCommittedAt`: the transaction time at which an internal governed effect and its decision evidence become committed together; and
- `effectDispatchedAt`, where applicable, the transport time recorded for an already committed filing envelope after a separate release-eligibility decision.

`subjectTime` never substitutes for `authorizationEvaluatedAt`, `effectCommittedAt`, or `effectDispatchedAt`.

Current principal binding, representation, role validity, grant validity, delegation, sharing, policy applicability, and revocation are evaluated at `authorizationEvaluatedAt` and must still hold at the authority-bearing effect boundary. For an internal governed write or buffered read, the transaction defined in section 18 supplies that guarantee. For formal filing, the boundary is the authenticated human's atomic commit of the exact immutable filing envelope and decision evidence to the governed outbox. Later transport cannot acquire, widen, or re-exercise filing authority, but it still requires the separate current release-eligibility decision in section 18.6 before protected bytes cross an external boundary.

The selected rule's `historicalAuthorityPosture` is mandatory. `CURRENT_ONLY` checks only current authority for the action. `CURRENT_REPORT_AUTHORITY_ONLY` also checks only current authority, but additionally states that the effect is a claim/report whose submitter is not presumed to be its alleged performer. The exact posture for every row is fixed in section 7.8.

For `ASSERT_OPERATION_CLAIM` and `OPERATE_REPORT_EXECUTION`, the reporter's current path authorizes only submission of the claim/report. `performedByPartyRef`, alleged software-agent actorship references, and optional immutable `performerAuthorityEvidenceRefs` are claim provenance, not the reporter's authority subject and not proof that execution was authorized. The authorization trace marks performer authority `NOT_EVALUATED_BY_AUTHORIZATION`. Evidence, review, and promotion gates decide whether claimed execution authority is sufficient for an accepted execution consequence. A future action that truly requires historical performer authority must add an explicitly reviewed posture, performer-specific proof contract, and conformance cases; it may not reuse the reporter's current path at `subjectTime`.

A current request made after revocation cannot regain authority by supplying a pre-revocation `subjectTime`.

### 8.2 Exact effect-intent binding

Every v0.2 request, result, trace, and human approval binds:

- the rule-selected `effectIntentSchemaRef`, `effectIntentSchemaVersion`, and `effectIntentSchemaDigest`;
- `effectIntentRef` or an embedded immutable effect intent;
- `effectIntentDigest`; and
- `effectIntentCanonicalization`, fixed to `JCS_RFC8785_SHA256` for v0.2.

The evaluator selects the schema binding and authorization-view extractor from the action rule before validating the intent. The caller cannot choose either. `effectIntentDigest` is `sha256:` followed by the SHA-256 digest of the UTF-8 bytes produced by RFC 8785 JSON Canonicalization Scheme over the complete effect intent validated by that exact schema revision.

The effect intent contains every authorization-relevant operation input, including at least:

- the exact proposed grantee, rights, purpose, and artifact for `SHARE_GRANT_ACCESS`;
- the exact pack release/content digest, installation parameters, requested profiles, exclusions, and proposed activation-set content for context actions;
- the exact assertion body, evidence set, subject time, and claimed scope for assertion actions;
- the exact governed-record kind/ref/revision or digest, proposed decision content, and rule-constrained `decisionOutcomeState` for review actions; and
- the exact assembly revision, destination, filing mode, and payload digest for filing.

An operation-specific schema may require more. It may not omit a value that can change the authority result or protected effect.

The validated effect intent is the sole authoritative request source for every operation fact. The rule-selected extractor derives the complete authorization view and records its digest. No comparison against a second caller-authored resource, subject, scope, time, purpose, destination, grantee, rights, or payload field is permitted because no such duplicate field exists in the v0.2 request schema.

Payload substitution after evaluation changes the digest and requires a new decision. A decision is never authority for a merely similar payload.

### 8.3 Derived resource view

The rule-selected extractor derives the resource view from the validated effect intent. The selected `resourceRequirementPolicy` determines each named role's posture, allowed concrete kinds, cardinality, and `ALL_OF`/`ONE_OF` composition.

Each resource entry contains:

- `resourceRole`;
- `resourcePosture`;
- `resourceKind`;
- `resourceRef`;
- immutable `resourceRevisionRef` or content digest;
- `scopeType` and `scopeRef`;
- `twin` where applicable; and
- `authorizationResourceProofRefs`.

The proof must establish existence, exact posture/role/kind, immutable revision, currentness where required, twin, tenant, and scope binding at the applicable evaluation time. An opaque reference alone is not proof. Every `ALL_OF` input must pass its own typed validation. Only the one `AUTHORITY_TARGET` is compared with grant scope and role anchors; integrity, applicability, state, and evidence inputs cannot grant authority or be used to union partial paths.

### 8.4 Effect subject and existence posture

`effectSubject` is the existing or prospective object changed, created, disclosed, or acted upon, derived from the same validated effect intent. It contains:

- `subjectKind`;
- `subjectRef` or a proposed stable identifier;
- `existencePosture`, exactly `EXISTING_REQUIRED` or `PROSPECTIVE_TARGET_ALLOWED`;
- `subjectTime`, where the domain action has one;
- `effectSubjectProofRefs`; and
- the resulting immutable revision reference after a successful governed write.

For `EXISTING_REQUIRED`, proof must establish that the exact subject and immutable revision exist and are eligible for the action.

For `PROSPECTIVE_TARGET_ALLOWED`, proof establishes the permitted kind, namespace or parent, proposed identifier reservation where required, scope, tenant, and schema posture. It must not falsely claim that the result already exists. The committed result revision is added to effect evidence after success.

The authority target and effect subject may refer to the same existing object only when the action rule explicitly permits it. Their proof fields and semantic roles remain distinct.

### 8.5 Pack identity

`PACK_RELEASE` or `PACK_ARTIFACT` identifies immutable installable content. `PACK_INSTALLATION` identifies the governed installation result. `PACK_ACTIVATION_SET` identifies an immutable activation posture for a scope and time. A pack activation/deactivation intent creates one prospective `STRUCTURE_EVENT` that binds both the current set and complete proposed successor; it never mutates the earlier set. The successor activation-set revision is a linked consequence of that event, and the governed-effect receipt binds both immutable revisions.

These kinds are not interchangeable. An activation-set identifier cannot prove which pack release was installed, and a pack release cannot masquerade as an applied activation set.

### 8.6 Scope proof

`scopeProofRefs` prove the relationship between the one authority target, the effect subject, and every authority-source scope. Integrity, applicability, state, and evidence inputs carry their own typed relationship proofs where their governing policy requires them. Scope proofs may refer only to immutable governed identity, containment, tenancy, or explicitly allowed lineage records that establish the claimed relationship.

Authority-target proof, effect-subject proof, and scope proof are not interchangeable. One immutable artifact may be bound in more than one proof array only when it independently establishes each claimed fact, and each use has a typed disposition.

### 8.7 Sovereignty and tenant isolation

`dataSovereigntyBoundaryRefs` may contain only immutable revisions of actual `DataSovereigntyBoundary` records. Generic resource, subject, scope, tenant, role, policy, or constraint evidence uses its dedicated field.

Every source, proof, policy, and evidence record used by a path must resolve within the authorized deployment or tenant boundary. Cross-tenant equality of an opaque identifier does not establish authority. A cross-tenant reference without an accepted sharing and sovereignty path is non-`ALLOW`.

### 8.8 Protected-effect contract boundary

An authorization decision proves authority for the exact bound effect intent. It does not by itself prove that a later domain record or event faithfully implements that intent.

Before a state-affecting action can execute, another applicable EnforcementChain gate must validate the proposed result against the exact `protectedEffectContractBinding` selected by the action rule. The owning domain contract defines the result schema, exact intent-to-result mappings, allowed derivations, forbidden widening, event/commit classification, and postconditions. Authorization consumes only the binding and validation disposition; it does not interpret or own those domain rules.

The governed-effect receipt records at least the effect-intent digest, resulting immutable record/event ref and digest, protected-effect contract ref/digest, overall contract-validation disposition, and an immutable validation-trace ref/digest carrying the contract owner's field-mapping and postcondition dispositions. A mismatch aborts the transaction and is a domain/runtime conformance failure, not a rewritten authorization outcome. No state-affecting row is executable until its protected-effect contract exists through the separate reviewed contract work tracked by `samovers/OFARM#12`.

---

## 9. Role and grant semantics

### 9.1 Party-targeted AuthorityGrant

A Party-targeted `AuthorityGrant` path is eligible only when:

- the immutable one-record grant identity/digest is active at `authorizationEvaluatedAt` and remains valid at the effect boundary;
- its `authorizedRuleBindings` entry for the requested action exactly matches the selected rule ID and digest;
- the grant target and immutable principal/representation/actorship basis establish one permitted path-specific `authoritySubjectBasis` and `authoritySubjectPartyRef` from section 6.2;
- the action class is present;
- the derived authority family is present;
- the one authority target, effect subject, complete effect intent, and scope satisfy the grant's closed constraints, while every non-authority input passes its own governing validation;
- inheritance does not exceed the matrix ceiling;
- purpose, condition, and evidence rules pass;
- no active revocation defeats the path; and
- principal resolution, CP3 posture where applicable, and the human-finalization rule pass.

No current v0.2 row requires historical authority. A future accepted rule may add a performer-specific historical posture, but it must identify the historical authority subject and proof contract explicitly; historical success could never repair failure at current evaluation/effect time.

### 9.2 Role-targeted AuthorityGrant

In addition to section 9.1's source and rule-binding checks, a grant whose target kind is `ROLE_ASSIGNMENT` is eligible only when the referenced `RoleAssignment`:

- has an immutable revision that exists and is valid at `authorizationEvaluatedAt` and the effect boundary;
- names the path-specific `authoritySubjectPartyRef` and is supported by that path's immutable authority-subject basis;
- is valid in the same tenant boundary; and
- has at least one `anchorScopes` entry that independently covers the one authority target; the effect subject must be proven within or exactly related to that target as the action rule specifies.

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
2. the immutable source grant record explicitly permits the action at the required precision and its per-action rule binding exactly matches the selected rule ID/digest;
3. the delegation itself contains the requested action and family, and its own per-action rule binding exactly matches the selected rule ID/digest;
4. the delegator held a live, independently sufficient source authority at `authorizationEvaluatedAt` and the effect boundary;
5. the delegation establishes the path-specific authority-subject basis and satisfies principal, the one authority target, effect-subject, scope, time, purpose, condition, evidence, state, and revocation checks, while all other typed inputs pass their own governing validation;
6. the delegation does not broaden action, family, resource, subject, effect intent, scope, inheritance, time, purpose, evidence, CP3 posture, or human-finalization requirement;
7. every `sourceAuthorityGrantRef` resolves to an immutable one-record identity/digest and is recorded; and
8. any role-targeted source grant is capped by its referenced `RoleAssignment.anchorScopes` exactly as described in section 9.2.

The effective delegated permission is the intersection of the action-rule ceiling, source grant, source role anchor, and DelegationGrant. The narrowest value wins at every dimension. A prohibition, missing source link, missing explicit permission, rule-binding mismatch, or unresolved source identity makes the path ineligible.

The evaluator rejects cycles. The v0.2 default maximum delegation depth is one hop unless a later accepted policy introduces an explicit bounded chain contract and conformance suite.

---

## 11. Purpose semantics

### 11.1 Proposed v0.2 representation

Executable v0.2 sources use optional `permittedUsePurposes`, a non-empty unique array of closed purpose tokens. The optional scalar `requestedUsePurpose` is extracted from the validated effect intent; it is not a second caller-authored request fact.

Purpose tokens must match `^[A-Z][A-Z0-9_]{0,127}$`.

If a source has `permittedUsePurposes`:

- the derived authorization view must contain `requestedUsePurpose` from the validated effect intent;
- the scalar must equal one member exactly;
- the purpose is evaluated for the same action, effect-intent digest, authority target, and effect subject as the request; and
- the trace records the requested token, source tokens, selected source reference, and `MATCHED` or `NOT_MATCHED` disposition.

No trimming, case folding, Unicode normalization, punctuation replacement, stemming, hierarchy, wildcard, prefix, substring, or synonym rule is implied.

If a v0.2 source omits `permittedUsePurposes`, that source carries no purpose restriction. The extracted intent purpose remains provenance and does not add authority.

### 11.2 Legacy free-text purpose

The v0.1 `purpose` field is descriptive free text. It must not be silently converted into a v0.2 purpose token.

A v0.1 source does not enter the v0.2 path lattice because it lacks the required issuance-policy identity and exact per-action `authorizedRuleBindings`. If it is offered to a v0.2 evaluator, the path is `DENY` with `SOURCE_RULE_BINDING_MISMATCH` before purpose evaluation. A v0.1 evaluator remains governed by v0.1 and cannot emit a v0.2 legacy-purpose reason or claim v0.2 proof strength.

A source carrying non-empty v0.1 `purpose` can support v0.2 only after steward-reviewed migration creates a new v0.2 source with explicit tokens. The v0.1 record remains unchanged and linked as migration provenance.

A duplicate caller-only `usePurpose` is schema-invalid and never satisfies a source constraint.

---

## 12. Conditions, limits, and required evidence

### 12.1 No generic condition language

This proposal does not create a free-text condition interpreter or a generic expression language.

The executable v0.2 limits are only:

- action class;
- authority family;
- authority-target kind/reference, typed input roles, and effect-subject kind/reference/existence posture;
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

### 12.2 Legacy conditions are migration inputs

A non-empty v0.1 `conditions` array must never be guessed true or copied into an executable v0.2 source. It does not produce a v0.2 path-level legacy-condition outcome: the v0.1 source is excluded by its missing exact rule binding and is `DENY` with `SOURCE_RULE_BINDING_MISMATCH` if offered to the v0.2 evaluator. Under a v0.1 bundle, only v0.1 outcomes apply.

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
- bind to the authority target, effect subject, effect intent, and scope; and
- be eligible for `requestedUsePurpose` when purpose is constrained.

Missing, wrong-kind, stale, disputed, superseded, cross-tenant, unavailable, mutable-only, or otherwise ineligible evidence produces non-`ALLOW` and an individual evidence disposition in the trace.

Opaque existence of a logical reference is not evidence eligibility.

### 12.6 Legacy evidence

A v0.1 DelegationGrant containing `requiredEvidenceRefs` without an active evidence-policy revision is migration input only. It does not enter the v0.2 path lattice or produce a v0.2 legacy-evidence outcome; if offered to the v0.2 evaluator, its missing exact rule binding yields `DENY` with `SOURCE_RULE_BINDING_MISMATCH`. Migration creates a new source with the applicable typed evidence group without rewriting the v0.1 record.

---

## 13. Sharing and `RECEIVE_READ_DATA`

`SharingGrant` is an access right, not assertion, review, governance, signing, or mutation authority.

For `RECEIVE_READ_DATA`, the evaluator performs one final authority-gate decision with two layers:

1. an access basis: a sufficient `RECEIVE_USE` AuthorityGrant/DelegationGrant path or a sufficient SharingGrant for the exact grantee and artifact; and
2. a resource-control layer: read-target proof, effect-intent binding, scope proof, tenant and sovereignty policy, purpose, conditions, evidence, state, current time, and revocation.

Each candidate access basis must be independently sufficient. The resource-control layer can constrain or defeat that basis but cannot supply missing authority, and constraints from separate access bases are never unioned.

A SharingGrant path is eligible only when:

- `granteePartyRef` is the path-specific `authoritySubjectPartyRef`;
- `sharedArtifactFamily` equals the concrete `READ_TARGET` kind;
- `sharedArtifactRef` and immutable revision exactly equal that target;
- the requested scope is covered;
- the immutable one-record SharingGrant identity/digest is active at `authorizationEvaluatedAt` and remains valid at the effect boundary;
- its `authorizedRuleBindings` entry for `RECEIVE_READ_DATA` exactly matches the selected rule ID/digest;
- its purpose, conditions, and evidence groups are evaluable and pass for the exact effect intent;
- all actual sovereignty boundaries pass; and
- no active revocation defeats the sharing right.

A SharingGrant cannot authorize any action other than `RECEIVE_READ_DATA`. It cannot be cited as write, review, govern, context, sharing-administration, or signing authority.

A runtime must not evaluate a direct receive/use grant and a SharingGrant in separate endpoints that can return contradictory final answers. Their applicable bases and constraints are composed into one policy decision and one trace.

An `ALLOW` from those layers is not itself permission to release bytes. Actual disclosure must also pass every applicable EnforcementChain gate, mandatory CP2 qualification, result-item coverage, and the same-snapshot buffered governed-read protocol in section 18.5. A preflight/dry-run result can report only non-protected qualification/planning information and never becomes a cached disclosure authorization.

For `SHARE_GRANT_ACCESS`, `effectIntentDigest` covers the exact grantee, immutable artifact revision, rights, delivery mode, purpose, validity, scope, and sovereignty posture that will appear in the prospective SharingGrant. Substituting any of them requires a new decision and human approval.

For `SHARE_REVOKE_ACCESS`, the existing SharingGrant and shared artifact are inputs. The protected effect is a new prospective `RevocationDecision` whose affected family is `SHARING_GRANT` and whose mode is `TERMINATE`. The existing SharingGrant remains immutable. A partial-rights narrowing needs separately accepted closed narrowing semantics and cannot be smuggled into this action.

---

## 14. Revocation semantics

Revocation lookup is mandatory for every source path. A caller cannot disable it.

### 14.1 `TERMINATE`

Every v0.2 AuthorityGrant, DelegationGrant, and SharingGrant identifier names exactly one immutable record, as defined in section 17.3. `RevocationDecision v0.1.revokesArtifactFamily` plus `revokesArtifactRef` therefore identifies one exact source record rather than a mutable logical lineage.

An effective `TERMINATE` decision for that exact source ID makes only that source path ineligible from `effectiveFrom` onward. Current requests compare `effectiveFrom` with trusted `authorizationEvaluatedAt` and the effect boundary, never with caller-provided `subjectTime`. It does not erase historical decisions made before the effective time and does not implicitly terminate a separately issued replacement with a different source ID. Creating a replacement is itself governed and cannot reuse the revoked record's authority or identifier.

### 14.2 Narrowing modes

The current v0.1 `NARROW_SCOPE`, `NARROW_ACTIONS`, and `NARROW_TIME` forms do not close all operands and merge behavior needed for deterministic evaluation.

Until a separately reviewed version closes those operands, an active narrowing decision affecting a candidate source produces `UNSUPPORTED_REVOCATION_NARROWING` and a non-`ALLOW` outcome for that path. A runtime must not ignore it, treat it as termination without saying so, or infer replacement semantics from notes.

This is bounded design debt, not a claim that narrowing is unsupported forever.

### 14.3 Revocation candidates

Revocations must be found from a trusted complete index keyed by affected artifact family, exact immutable source ID, and trusted evaluation/effect time. The trace binds the index watermark and canonical-history position through `authorityEvaluationSnapshotRef`. Caller-supplied candidate lists are never the completeness boundary. A runtime must not apply one source ID's revocation to another ID through an inferred successor relationship, and it must not allow bytes under an already-used source ID to change.

### 14.4 Prospective administrative effects

`SHARE_REVOKE_ACCESS` commits a prospective `RevocationDecision`; it never edits or relabels the affected SharingGrant. `CONTEXT_ACTIVATE_PACK` and `CONTEXT_DEACTIVATE_PACK` commit prospective `StructureEvent` effects and immutable successor activation state; they never rewrite the previous activation set. The domain event family and commit class come from the active Event Grammar and the protected-effect contract, not from authorization audit records.

---

## 15. Deterministic evaluation

### 15.1 Evaluation order

The proposed evaluator order is:

1. receive only a schema-valid request and rule-valid effect intent from the ingress protocol in section 18.1;
2. canonicalize the effect intent, verify `effectIntentDigest`, and derive the complete authorization view through the rule-selected extractor;
3. assign trusted `authorizationEvaluatedAt` and load the immutable authority-evaluation snapshot;
4. load and verify the content-addressed policy bundle and complete action rule;
5. verify the rule-selected effect-intent schema ref/version/digest, protected-effect contract binding where applicable, and all other rule bindings;
6. resolve the authenticated principal, represented Party, and representation basis;
7. resolve CP3 evidence and exact agent-action posture where the principal is software;
8. resolve and prove the one authority target, every other typed input, and the effect subject under the row's existence posture;
9. prove tenant, sovereignty, and scope relationships;
10. resolve role, direct-grant, delegated, and sharing candidates, deriving an authority subject/basis separately for each path;
11. evaluate the source's exact per-action rule binding plus action, family, resources, subject, intent, scope, inheritance, time, state, purpose, conditions, and cumulative evidence requirements per path;
12. evaluate delegated source paths under the closed delegation intersection;
13. compose any applicable `RECEIVE_READ_DATA` SharingGrant path;
14. apply every effective revocation from the completeness-proven snapshot;
15. apply the rule's exact historical-authority posture; current report rows authorize only the submitter now and never reuse that path as historical performer authority;
16. run or verify the governed human-approval lifecycle for the exact intent where required;
17. assign one disposition to every path and aggregate them under section 15.3;
18. build the request, result, and trace records with immutable basis bindings;
19. validate `decisionValidUntil`, consumption posture, and the decision-bundle digest; and
20. enter the governed write, buffered governed read, filing-outbox, or non-`ALLOW` protocol in section 18; authority `ALLOW` does not bypass another applicable EnforcementChain gate.

No later step may repair missing proof from an earlier step by trusting a caller assertion.

### 15.2 Path selection

Outcome is computed over all completely evaluated paths, not over the first database row returned.

If one or more paths fully allow, the selected path is the lowest canonical tuple:

1. path type order: direct Party grant, role-targeted grant, delegated grant, SharingGrant access path;
2. immutable source record identifier in code-point order; and
3. immutable delegation/source record identifiers in code-point order.

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

Effect-intent/derived-view digest validity, loaded policy identity, trusted principal resolution, authority-target/effect-subject proof, tenant isolation, and authority-snapshot availability are authorization global preconditions. Parse, request-schema, action lookup, rule/binding-manifest, caller-schema-claim, action-specific intent-schema, and authorization-view-extraction failures never enter this lattice; section 18.1 records them as ingress rejections.

Global checks are attempted in the section 15.1 order under this explicit dependency relation:

- effect-intent/derived-view digest validity and trusted principal resolution use only their own independently trusted inputs;
- authority-snapshot availability and loaded policy identity must both pass before authority-target/effect-subject proof or tenant isolation is evaluated; and
- tenant isolation also requires every target/effect-subject identity on which that check depends to have been proven.

If a prerequisite in that relation fails, each dependent check is recorded as `NOT_EVALUATED`. `NOT_EVALUATED` is a trace disposition meaning that no pass or failure conclusion was made because a named prerequisite failed. It is not an authorization outcome or reason code, has no rank, and does not participate in aggregation. The evaluator collects every independent global failure it can truthfully establish, then selects the global result deterministically:

1. if one or more established global failures have default outcome `DENY`, the result is `DENY` and the lowest numeric deny rank among those failures is primary;
2. otherwise, if one or more established global failures have default outcome `REQUIRE_REVIEW`, the result is `REQUIRE_REVIEW` and the lowest numeric review rank among those failures is primary; and
3. otherwise, global preconditions pass and path evaluation may begin.

Global failures never produce `ALLOW` or `REQUIRE_HUMAN_APPROVAL`. When any global failure exists, candidate paths are not aggregated and no selected path is required. The explicit `DENY`-before-`REQUIRE_REVIEW` precedence applies only among simultaneous authorization-global failures; numeric ranks still are never compared across outcomes. Global diagnostics place the primary reason first, then the other established failures by global outcome precedence (`DENY`, then `REQUIRE_REVIEW`), numeric rank within that outcome, and reason code. No path may override a global result.

### 15.5 Total aggregation lattice

After global preconditions pass, path outcomes aggregate in this exact order:

1. if any path is `PATH_ALLOW`, outcome is `ALLOW`;
2. otherwise, if any path is `PATH_REQUIRE_HUMAN_APPROVAL`, outcome is `REQUIRE_HUMAN_APPROVAL`;
3. otherwise, if any path is `PATH_REQUIRE_REVIEW`, outcome is `REQUIRE_REVIEW`;
4. otherwise, outcome is `DENY`.

Therefore, a complete path that lacks only fresh human approval outranks an unrelated path with unsupported revocation-narrowing semantics. A complete `PATH_ALLOW` also outranks an unrelated revoked path. Revocation of the source actually selected or a global revocation/tenant blocker still prevents `ALLOW`.

The selected path is chosen by section 15.2 from paths with the winning disposition.

### 15.6 Primary reason selection

When global preconditions pass, primary reason is outcome-specific over the selected path:

- `ALLOW` uses `AUTHORIZED_BY_SELECTED_PATH`;
- `REQUIRE_HUMAN_APPROVAL` uses `HUMAN_FINAL_ACTION_REQUIRED` from the selected path;
- `REQUIRE_REVIEW` uses the lowest numeric review rank from the selected path; and
- `DENY` uses the lowest numeric deny rank from the selected path, or `NO_AUTHORITY_BASIS` when no applicable path exists.

`APPROVAL_CHALLENGE_STALE`, `APPROVAL_EXPIRED`, `APPROVAL_SEPARATION_UNSATISFIED`, and `APPROVER_AUTHORITY_INSUFFICIENT` are approval-lifecycle diagnostics. They explain why the selected otherwise-sufficient path still lacks consumable approval; none may replace `HUMAN_FINAL_ACTION_REQUIRED` as the primary reason. `APPROVAL_SEPARATION_UNSATISFIED` remains reserved until a current action rule selects `DISTINCT_APPROVER_REQUIRED`.

Problems from non-selected paths remain ordered diagnostics and can never become the primary reason for an `ALLOW` or human-approval result. A global result uses the primary-reason rule in section 15.4 and has no selected path. Numeric reason ranks are fixed in section 20; free-form severity does not select the primary reason.

---

## 16. Policy identity

Every v0.2 result and trace must identify:

- `policyId`;
- `policyVersion`;
- `policyDigest` in `sha256:<64 lowercase hexadecimal characters>` form;
- `selectedRuleId`, immutable `ruleRevision`, and per-action semantic-closure `ruleDigest`; and
- binding-manifest content ref and digest.

The `policyDigest` covers the exact immutable representation used by the evaluator, including the action matrix and referenced decision rules after deterministic packaging. A mutable URL, branch name, deployment label, or semantic version alone is not enough. It identifies the complete evaluation context; source reuse compares the selected action's narrower `ruleDigest` from section 7.4 so an unrelated action or diagnostic-only change does not invalidate the source.

If the loaded representation does not match the expected digest, the evaluator establishes the global failure `POLICY_DIGEST_MISMATCH`. It does not evaluate policy-dependent authority-target/effect-subject or tenant conclusions. Section 15.4 selects the overall outcome and primary reason from this and any other independently established global failure; absent another failure that precedes it under that rule, the result is `REQUIRE_REVIEW` with `POLICY_DIGEST_MISMATCH` primary.

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

A mutable logical identifier alone is insufficient for non-source artifacts. For v0.2 AuthorityGrant, DelegationGrant, and SharingGrant records, the binding instead carries the exact source-record ID and content digest because section 17.3 forbids another revision or byte sequence under that ID. Reusing a source ID with changed bytes is a conformance failure, not a successor revision.

For human approval, each full snapshot also produces `authorityRelevantStateDigest`: JCS/SHA-256 over a rule-selected projection containing the authenticated principal/representation basis, selected and eligible authority paths, grants/roles/delegations/sharing records with their issuance/rule bindings, revocations, authority target and typed input revisions, effect subject, extracted scope/twin/time/purpose, applicable policy/rule/extractor/protected-effect/evidence bindings, relevant evidence eligibility, tenant/sovereignty constraints, CP3 posture where applicable, and approver-separation facts. The projection and its JSON Pointers are content-addressed parts of the action rule.

The challenge, approval, and unrelated audit/history records are excluded from that projection merely by existing. Their expiry, consumption, or relationship facts are included only when the rule makes those facts relevant to eligibility or separation.

Challenge and final full snapshot refs may differ because unrelated canonical history advanced. Approval remains eligible only when their `authorityRelevantStateDigest` values are equal and every final cutoff still passes. A relevant change changes the digest and requires a new challenge and human act. An unrelated change outside the projection does not.

---

## 17. Proposed contract family delta

### 17.1 Why source records also need v0.2

Changing only `AuthorizationDecisionRequest`, `AuthorizationDecisionResult`, and `AuthorizationDecisionTrace` would leave executable constraints trapped in ambiguous v0.1 source fields. The smallest honest v0.2 machine surface therefore includes versioned authority sources as well as the decision bundle.

This is an approval point. If stewards reject the one-record immutable source-ID model, they must choose another closed source-identity and revocation model before the decision schemas can truthfully claim v0.2 proof.

### 17.2 Proposed versioned schema packages

To avoid multiplying top-level contract families, draft/non-default work in section 24 should use four bounded schema packages:

1. `AuthorizationPolicyBundle v0.2`: resolved `ActionAuthorizationRule` records, effect-intent schemas, separately owned protected-effect contract bindings, declarative authorization-view/relevant-state projections, evidence bindings, and one immutable manifest;
2. `AuthoritySourceBundle v0.2`: closed immutable v0.2 records for `AuthorityGrant`, `DelegationGrant`, and `SharingGrant` only;
3. `AuthorizationDecisionEvidence v0.2`: tagged request, ingress-rejection, result, and full-internal-trace profiles plus the authority-snapshot binding/projection; and
4. `AuthorizationFinalizationEvidence v0.2`: tagged challenge with content-addressed display evidence, human approval, single-use consumption, protected-effect-contract validation receipt, filing-outbox receipt, governed-read receipt with an explicit payload proof-strength posture, and references to separately governed transport-release receipts.

The tagged profiles remain separately validateable where their truth claims differ, but they do not become fourteen unrelated registries or new domain families. A standalone `AuthorityEvaluationSnapshot` family is unnecessary unless the later schema PR proves that the existing immutable snapshot reference plus closed projection cannot represent the required evidence.

`RoleAssignment v0.1`, `RevocationDecision v0.1`, and `DataSovereigntyBoundary v0.1` remain unchanged by default. If schema changes to those families prove necessary, they require an explicit scope review before editing.

When a valid decision/finalization evidence bundle enters OFARM authority, its primary event family is the existing `EvidenceEvent` and its commit class is the existing `evidence record`. Request/rejection telemetry that does not enter OFARM authority has no OFARM event/commit claim; if a governed deployment retains it in authority, it uses the same EvidenceEvent/evidence-record classification with its limited truth claims.

Governed authorization evidence is immutable and append-only. A correction or later failure is a new linked evidence record and never rewrites the earlier request, decision, approval, consumption, effect/read/outbox, or transport claim. These records support authorization-decision reconstruction and audit read models only; a payload marked `DIGEST_ONLY` remains outside any byte-reconstruction claim. Authorization evidence is not eligible to create domain current state, truth, promotion, materialization, publication, pack activation, or filing-delivery truth, and it creates no new top-level event family or commit class.

### 17.3 Source-record delta

Common v0.2 source behavior:

- make each family identifier a one-record immutable identity: after issuance, no bytes, fields, state, or meaning may change under the same identifier;
- require a `sourceRecordDigest` over the complete immutable source record;
- require `issuedUnderPolicyId`, `issuedUnderPolicyVersion`, and `issuedUnderPolicyDigest` as consent/audit context;
- require a non-empty `authorizedRuleBindings` array with exactly one `{ actionClass, ruleId, ruleDigest }` entry for every granted action class and no extra entry;
- make `authorityFamilies` closed and required where the source carries authority families;
- add optional closed `permittedUsePurposes`;
- remove free-text `purpose` and `conditions` from the executable v0.2 form;
- reject unknown fields;
- add optional narrowing by the authority target, effect-subject kinds/refs/existence postures, rule-selected effect-intent profile IDs, and twins; non-authority inputs cannot widen a source;
- retain closed action, scope, time, and inheritance constraints, and replace mutable-looking family state with immutable `issuanceState` (`DRAFT` or `ACTIVE`); and
- preserve immutable provenance linking a migrated record to its v0.1 predecessor.

For the requested action, the evaluator requires the source's `actionClass`, `ruleId`, and `ruleDigest` to equal the selected action rule and its complete resolved per-action semantic closure exactly. `issuedUnderPolicyDigest` records the complete issuance context but is not compared to the current bundle digest, because an unrelated action or diagnostic-only change must not invalidate a grant whose selected semantic closure is unchanged.

`sourceRecordDigest` uses JCS/SHA-256 over the complete source record after removing exactly the top-level `/sourceRecordDigest` field. The draft source schemas must define the provisional/final validation steps and forbid any other exclusion, following the decision-bundle projection discipline in section 18.8. A storage layer must reject a second byte sequence for an existing source ID even if a caller supplies a different digest.

For a SharingGrant, `authorizedRuleBindings` contains exactly the `RECEIVE_READ_DATA` binding; sharing remains ineligible for every other action. AuthorityGrant and DelegationGrant bindings cover exactly their respective `authorityActionClasses`.

V0.2 defines no automatic reuse across different rule digests, even when an implementation believes a new rule is narrower. `SOURCE_RULE_BINDING_MISMATCH` is non-`ALLOW` and requires a new source record with a new ID, an explicit steward-reviewed migration, or governed reapproval. A later extension may define content-addressed compatibility certificates, but no evaluator may invent a semantic-subset proof locally. This exact-match default closes target-kind expansion, extractor changes, weaker evidence, relaxed human posture, wider delegation, and changes to shared purpose, scope, revocation, proof, tenant, or path-composition semantics without creating a general policy theorem engine.

A correction, replacement, renewal, restriction, activation, or other change creates a different source ID and links the predecessor as provenance where applicable. `DRAFT` never grants authority. Current active, expired, or revoked posture is derived from the immutable record, its `issuanceState`, validity interval, applicable policy, and separate RevocationDecision records; v0.2 has no in-place `grantState`, `delegationState`, or `sharingState` mutation. Draft-to-active conversion likewise creates a new governed ID. A v0.1 source can support v0.2 only through the explicit migration in section 19.3.

Because source IDs are one-record identities, `RevocationDecision v0.1` remains sufficient for exact `TERMINATE` semantics: its family/ref pair names one immutable source record. It has no lineage reach, and no replacement source ID inherits either authority or revocation. This candidate therefore does not introduce `RevocationDecision v0.2`; any future lineage-wide or narrowing behavior requires its own scope review and contract version.

`AuthorityGrant v0.2` additionally carries required closed `delegationPermission` and conditional `delegableActionClasses` as defined in section 10.

Every v0.2 source family that can impose evidence uses the typed all-or-none `requiredEvidence` groups in section 12. `DelegationGrant v0.2` is not a special exception.

`SharingGrant v0.2` makes the immutable artifact-family/resource-kind binding explicit and keeps `dataSovereigntyBoundaryRefs` restricted to actual sovereignty records.

### 17.4 Request v0.2

Caller-provided request facts:

- request identifier and request time;
- requested action class;
- retrievable or embedded effect-intent instance and `effectIntentDigest`;
- optional AI-assistance disclosure; and
- optional retrieval hints that are explicitly non-authoritative.

Trusted boundary facts injected before evaluation:

- `resolvedPrincipalKind`;
- `authenticatedPrincipalRef` and immutable resolution revision;
- `representedPartyRef` and `representationBasisRef`, when applicable;
- the CP3 envelope/snapshot references for a software agent;
- trusted `authorizationEvaluatedAt`; and
- `authorityEvaluationSnapshotRef`.

The caller cannot choose any trusted-boundary fact, effect-intent schema, or authorization-view extractor. The action rule supplies the exact bindings. The extractor derives the authority target, typed inputs, effect subject, scope, twin, `subjectTime`, and requested purpose from the one validated intent. Mirrored caller fields for those facts are prohibited, not reconciled.

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
- rule-selected authorization-view extractor ref/digest and derived-view digest;
- rule-selected protected-effect contract ref/digest where applicable;
- requested action class;
- derived stage and authority family;
- policy identity, selected immutable rule revision/digest, and binding-manifest ref/digest;
- resolved-principal kind, selected path-specific authority subject/basis, accepted CP3 posture where applicable, and human-finalization requirement;
- deterministic outcome and primary reason code;
- winning per-path disposition and selected immutable basis;
- authority-target/input dispositions and role, direct grant, delegation, sharing, and revocation basis summaries, including the selected source's exact action-rule binding disposition;
- inheritance mode applied;
- human approval and effect-intent binding;
- stable ordered problems; and
- trace reference.

### 17.6 Trace v0.2

The trace records at least:

- trace, request, and result identifiers;
- extracted `subjectTime`, trusted `authorizationEvaluatedAt`, `decisionValidUntil`, and later effect/outbox/read/transport receipt refs with their declared proof-strength posture;
- rule-selected effect-intent schema ref/version/digest, immutable intent reference/digest, canonicalization, authorization-view extractor ref/digest, derived-view digest, and protected-effect contract ref/digest where applicable;
- policy ID/version/digest, selected immutable rule revision/digest, and binding-manifest ref/digest;
- action class, derived stage, and derived family;
- resolved-principal kind, authenticated principal and immutable resolution revision, represented Party, and representation basis;
- for software agents, executing instance, profile, sponsor, actorship binding, authority envelope, mandatory authority snapshot, revocation state, preflight, and qualification revision refs;
- accepted CP3 agent-action posture, human-finalization requirement, and AI-disclosure disposition;
- every named resource posture/role, concrete kind, immutable revision, scope, twin, proof refs, composition result, and individual disposition;
- full effect subject, existence posture, subject time, proof refs, resulting revision ref where applicable, and individual dispositions;
- scope proof refs and individual dispositions;
- `authorityEvaluationSnapshotRef`, canonical-history position, and all relevant index watermarks;
- role assignments and anchor-scope immutable basis bindings/dispositions;
- every path's authority-subject Party/basis plus each direct grant, delegation, source grant, and sharing record's immutable one-record ID/digest, issuance-policy identity, per-action rule binding, and disposition;
- revocation immutable basis bindings/dispositions;
- requested purpose, source purpose tokens, and purpose disposition;
- condition disposition;
- immutable evidence-policy refs, required evidence refs, constraint evidence refs, and individual evidence dispositions;
- immutable actual data-sovereignty boundary refs only;
- inheritance mode and delegation depth;
- alleged performer Party/agent identity, immutable actorship and performer-authority evidence refs for claim/report intents, and the explicit `NOT_EVALUATED_BY_AUTHORIZATION` performer-authority disposition, kept separate from the current reporter's authorization subject;
- human-finalization evidence refs, content-addressed display representation and renderer/display metadata, challenge/final snapshot refs, authority-relevant-state digests, approver eligibility path, and disposition;
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
4. validate the effect intent against the schema ref, version, and content digest selected by that rule;
5. execute the declarative authorization-view extraction, rejecting missing, duplicate, type-invalid, unknown-kind, or conflicting extracted facts.

Failure at any of those steps does not create a `DENY`, `REQUIRE_REVIEW`, or any other authorization result. If durable audit is required, the runtime records an `AuthorizationRequestRejection v0.2` or a lower-level transport/security event containing only facts it can truthfully establish:

- trusted receipt time and a digest of the received bytes;
- the claimed request identifier, action class, or schema hint only when they were safely parseable, explicitly marked as untrusted claims;
- the authenticated principal/session binding, when resolution had already succeeded;
- the selected action-rule and schema binding, only if ingress reached that step;
- stable ingress-rejection codes and validation locations; and
- the rejection-record schema identity and integrity digest.

The rejection must not assert that malformed input was a valid `AuthorizationDecisionRequest`, must not include an `AuthorizationDecisionResult` or `AuthorizationDecisionTrace`, and must not produce a protected effect. A caller-provided effect-intent schema hint is non-authoritative and, when present, must exactly equal the rule-selected binding; it can never select a weaker schema.

Only a schema-valid request with a rule-valid effect intent and one valid derived authorization view enters the authorization outcome lattice in section 15. Ingress rejection persistence failure is a runtime/audit failure, not a fabricated authorization result.

### 18.2 Transaction-bound decision validity

Every decision records `decisionValidUntil` from the selected action rule. The caller cannot extend it.

For every `TX` row, the selected `TRANSACTION_BOUND_V0_2` policy computes `decisionValidUntil` as the earliest instant in this exact candidate set:

1. the trusted protected-effect transaction deadline, fixed before evaluation;
2. the principal-resolution/session validity end;
3. every applicable representation, role-assignment, AuthorityGrant, DelegationGrant, source-grant, SharingGrant, and revocation-policy validity end used by the selected path;
4. policy/rule applicability end and authority-snapshot freshness deadline;
5. every applicable authority-target/input lease or currentness end, evidence eligibility/freshness end, and sovereignty-policy end; and
6. `approvalExpiresAt`, when approval is required.

Instants are compared as UTC timeline instants and all ends are exclusive. An explicitly unbounded governed interval contributes no cutoff; a missing or unparseable cutoff that its governing contract requires is non-`ALLOW`. If the candidate set cannot be constructed, or its minimum is not later than `authorizationEvaluatedAt`, no consumable decision exists. The decision must be consumed inside that protected-effect transaction and is not portable to a later transaction. The transaction deadline gives the decision its hard upper bound; this RFC does not invent a universal wall-clock duration without a governing runtime contract.

Every v0.2 decision records `SINGLE_USE`. Replay is outside v0.2; a future rule must define it explicitly rather than relying on a reserved token.

The consumption evidence records the decision, effect-intent and derived-view digests, consumer principal, consumption time, effect/read/outbox reference, and idempotency key where applicable. A second consumption is non-`ALLOW` even if the payload is identical. For formal filing, expiry constrains the human-final outbox commit; after that commit, a separately eligible transport attempt is not a second filing-decision consumption and does not inherit disclosure permission from the consumed decision.

For a row requiring interactive human approval, `TRANSACTION_BOUND_V0_2` governs the final re-evaluation, decision consumption, evidence, and protected-effect commit. It does not assert that challenge issuance and human think time occur inside that transaction. This document states the authorization-side invariants only; `samovers/OFARM#19` must define and review the reservation/finalization, concurrency, retry, and recovery protocol before any machine profile or runtime implementation may claim this lifecycle.

### 18.3 Human-approval lifecycle

An action whose rule requires `FRESH_HUMAN_APPROVAL_REQUIRED` does not accept an unattached approval reference or a bare boolean. It uses two versioned records.

The approval-challenge profile binds:

- a unique challenge identifier;
- the rule-selected effect-intent schema ref/version/digest, exact effect-intent digest, and retrievable intent reference;
- policy ID/version/digest and selected action-rule ID/digest;
- every resource posture/role/revision, effect subject, selected path-specific authority subject/basis, and represented Party;
- the intended authenticated natural-person approver, representation basis, and preliminary same-action eligibility-path refs;
- the immutable challenge authority-evaluation snapshot and `authorityRelevantStateDigest`;
- a content-addressed `humanVisibleRepresentationRef`, its exact byte digest and media type, renderer identifier/version/digest, display-policy ref/digest, locale, and timezone;
- trusted issue time and `challengeExpiresAt`;
- `approvalSeparationPolicy`; and
- closed approver-eligibility requirements.

The human-approval profile binds:

- a unique approval identifier and the exact challenge revision;
- the authenticated natural-person principal, represented Party, and immutable representation basis;
- trusted `humanActedAt`;
- the approved effect-intent, policy, rule, resource, subject, and human-visible representation ref/digests plus renderer/display metadata;
- the challenge and final authority-evaluation snapshot refs and their equal `authorityRelevantStateDigest` values;
- the approver's independent same-action natural-person authority-path evidence;
- `approvalExpiresAt`, single-use posture, and consumption status; and
- signature, attestation, or authenticated-session evidence required by the action rule.

The lifecycle is exactly:

1. evaluate the requesting path and a specific authenticated natural person's preliminary same-action eligibility path, render and retain the exact immutable display bytes for that person under the bound evidence-retention policy, then persist the challenge;
2. capture that same authenticated natural person's explicit act on the challenge;
3. re-evaluate every current authority, representation, revocation, resource, evidence, policy, and separation constraint, including the approver's independent eligibility path;
4. compute the final rule-selected relevant-state projection; require its digest to equal the challenge `authorityRelevantStateDigest`, while recording both full snapshot refs; if the relevant digest differs, invalidate the act and issue a new challenge, but do not invalidate merely because unrelated canonical history advanced; and
5. bind the approval to that final snapshot and consume both the approval and authorization decision atomically with the governed effect or outbox commit.

Approver eligibility is exact: run the same action rule for the authenticated natural-person approver, the same effect-intent/derived-view digests, authority target, effect subject, scope, twin, purpose, tenant, and sovereignty posture. Every non-finalization constraint must produce an otherwise sufficient `PATH_ALLOW`. The explicit challenged act may satisfy this row's finalization only under `SAME_PRINCIPAL_ALLOWED`; it cannot borrow the requesting agent's path. Sponsor status, ownership of an agent, shared representation, or account administration alone is never enough.

For a direct natural-person invocation, that person's same explicit act may satisfy fresh approval only through this lifecycle under `SAME_PRINCIPAL_ALLOWED`. A future rule selecting `DISTINCT_APPROVER_REQUIRED` additionally requires a different natural-person principal and the profile's exact relationship exclusions. `DIRECT_HUMAN_ACTION_REQUIRED` records the authenticated human act and representation basis as part of the request/effect transaction; it does not require a separate approval record unless another rule independently requires final approval.

The content-addressed representation must remain retrievable for the approval-evidence retention period. A digest without retrievable candidate bytes cannot support the claim that OFARM can reconstruct what the human saw. Retention duration, encryption, deletion, redaction, and key custody come from a separately governed evidence-retention policy ref/digest tracked by `samovers/OFARM#14`; this authorization RFC binds that policy and proof posture but does not define or implement those controls.

An expired challenge, unavailable or changed display bytes, changed renderer/display metadata or digest, changed intent, changed policy/rule/extractor, changed authority-relevant state, ineligible approver, or replayed/consumed approval is non-`ALLOW`. Approval can never extend `decisionValidUntil`, the trusted interactive session, the protected-effect transaction, or any relevant cutoff. This candidate imposes no unexplained universal wall-clock duration.

### 18.4 Internal governed writes

For an internal governed write, one atomic protected-effect transaction must:

1. evaluate or revalidate current principal, representation, source authority, revocation, authority-target/input revisions, effect-intent digest, and every other applicable EnforcementChain gate against the transaction snapshot;
2. build and validate the request/result/trace bundle;
3. reserve single-use consumption;
4. validate the proposed domain result against the rule-bound protected-effect contract, then apply only that validated result;
5. record the resulting immutable effect ref/digest and a governed-effect receipt containing the effect-intent digest, protected-effect contract ref/digest, overall contract-validation disposition, immutable field-mapping/postcondition validation-trace ref/digest, and trace refs/dispositions for every applicable ingress, authority, validation, pack-applicability, evidence, review/promotion, materialization, and publication/export gate;
6. commit the decision evidence, consumption, receipt, and effect together.

If concurrent relevant state invalidates the snapshot, the transaction must fail and the operation must be re-evaluated. The invariant is: **no governed effect becomes externally visible without its committed decision evidence**. The decision is not committed in an earlier transaction that creates a time-of-check/time-of-use gap.

Authorization `ALLOW` is only the authority-gate result. The transaction may apply the protected effect only after every other applicable active Platform `EnforcementChain` gate succeeds, including validation against the rule-bound protected-effect contract. The effect's mappings, postconditions, domain event family, and commit class are supplied by that separately governed contract and the active Event Grammar. Authorization bundles carry only the `EvidenceEvent`/`evidence record` classification in section 17.2; they do not themselves create assertion truth, governance promotion, pack applicability, materialization, publication, or current state. Missing result contracts or domain classifications are stacked prerequisites, not local authorization inventions.

### 18.5 Governed reads and protected disclosure

Actual `RECEIVE_READ_DATA` is a protected disclosure and uses `AGENT_ALLOWED_WITH_POLICY_CHECK`, not `AGENT_ALLOWED_WITH_PREFLIGHT_ONLY`. A preflight/dry-run may return only non-protected planning or qualification information and must never disclose protected bytes. Every actual read also requires the CP2 read-qualification evidence profile selected in section 7.8; this is an authorization-rule requirement and does not redefine a CP3 posture value.

One governed read snapshot must cover authorization, retrieval, redaction, qualification, coverage proof, and payload construction. The decision bundle and governed-read receipt bind at least:

- the immutable read-target revision and every immutable origin revision contributing returned information;
- the exact `QuerySpecification` and executable query/plan digest, where applicable;
- row, field, aggregate, count, metadata, lineage, tenant, purpose, sovereignty, and redaction-policy identities/digests;
- trace refs/dispositions for every applicable EnforcementChain gate, without claiming inapplicable gates passed;
- the CP2 qualification envelope, including qualification outcome, stable problems, trace/lineage refs, and prescribed next actions;
- a result-coverage manifest mapping every returned row, field, aggregate, count, metadata item, lineage item, and payload location to its origin revision and authority/redaction disposition;
- the exact returned buffered-payload digest, media type, serializer identifier/version/digest, and serialization-policy ref/digest;
- the selected `payloadEvidencePosture` and immutable evidence-retention policy ref/digest; and
- whether the read completed or failed before disclosure.

`payloadEvidencePosture` is exactly one of:

- `RETAINED_BYTES`: the receipt also binds a content-addressed payload ref whose bytes remain retrievable for the governed retention period; the disclosure is byte-reconstructible while those bytes are retained; or
- `DIGEST_ONLY`: no retained payload claim is made; the receipt can verify candidate bytes supplied later against the digest, but OFARM does not claim that it can reconstruct the disclosed bytes from the receipt.

The posture and policy are resolved from a trusted immutable evidence-retention policy at the governed read snapshot; the caller cannot choose or weaken them. If no applicable policy can be resolved, the read cannot claim v0.2 governed-read evidence and no protected bytes are disclosed.

The selected retention policy owns retention duration, encryption, deletion, redaction, and key custody. Those controls are the separate data-governance/security boundary tracked by `samovers/OFARM#14`. Expiry or governed deletion of retained payload bytes never deletes or rewrites the immutable receipt, payload digest, disclosure time, proof-strength posture, or historical fact that disclosure occurred.

Every unredacted result item must be covered by the selected authority path for the exact read target, purpose, scope, tenant, sovereignty boundary, and snapshot and must pass the selected redaction policy. CP2 qualification and lineage describe the result; they do not create missing read authority. If coverage for any item or aggregate-inference risk cannot be proven, that item is withheld or redacted under the bound policy; if the final payload cannot be completely covered, the read is denied.

The runtime stages and hashes the exact buffered payload, then atomically persists decision evidence, single-use consumption, governed-read receipt, coverage manifest, payload digest, and the retained payload ref/bytes when `RETAINED_BYTES` applies before the single disclosure linearization point. If persistence fails, zero protected bytes are released. Protected streaming is unsupported in v0.2; a request for it fails rule-selected intent-schema ingress validation. A later streaming design requires a separate Platform runtime RFC and cannot be inferred from this authorization policy.

No cache, secondary endpoint, preflight response, denial body, count, metadata field, trace field, or retry path may release protected information outside that protocol. The full decision trace is internal evidence. A caller-facing result uses the CP2-qualified safe projection in section 18.7. Reading the full trace requires a separate `RECEIVE_READ_DATA` decision over the exact `AUTHORIZATION_TRACE` target; CP2 redaction/denial indication applies to that trace read.

### 18.6 External side effects

Every action rule selects exactly one external-effect posture:

- `NO_EXTERNAL_DISPATCH`: the action cannot create an external dispatch;
- `OUTBOX_COMMIT_IS_FINAL_FILING_ACT`: consuming the decision and committing the exact idempotent filing envelope to the governed outbox is the human-final authority-bearing filing act; that act does not itself authorize later release of protected bytes.

`OUTPUT_FILE_SUBMISSION_ASSEMBLY` is the only current `OF` row. After every applicable EnforcementChain gate succeeds, its authenticated natural-person action atomically commits:

- the decision bundle;
- the single-use consumption reservation;
- an idempotent outbox record containing the exact immutable envelope bytes/ref, digest, destination, filing mode, and idempotency key; and
- a filing-effect receipt that names this outbox commit as OFARM's governed authority-bearing filing linearization point and binds every applicable EnforcementChain gate trace/disposition.

The decision and approval must be unexpired and current through that commit. A later revocation or natural expiry is prospective: it does not retroactively erase the committed human filing act. This RFC defines no cancellation or recall power after commit. Such a power needs a separate action and receiver-supported protocol.

Before any first send or retry that may disclose protected bytes, the separate transport-release gate tracked by `samovers/OFARM#13` must establish current release eligibility for the exact envelope, destination, and endpoint. Its content-addressed regime-specific policy must cover current data-sovereignty and disclosure posture, recipient eligibility, current SharingGrant or statutory disclosure basis where applicable, transport custody/endpoint binding, and cancellation/hold status.

The release gate neither impersonates the human nor re-exercises the completed filing authority. Expiry of the human's session, grant, approval, or `decisionValidUntil` does not retroactively invalidate the outbox commit, but neither does that historical validity grant current disclosure permission. A sharing, sovereignty, recipient, custody, endpoint, or hold change may stop release while leaving the filing record historically valid.

Only after the release gate passes may the transport worker send or retry the committed bytes to the committed destination under the same idempotency key. It cannot alter the envelope, choose a filing principal, consume another filing decision, or make another filing-authorization claim. It records the exact release-policy ref/digest and disposition plus delivery, receiver acknowledgement, duplicate acknowledgement, or failure in a transport receipt without rewriting the filing decision/effect receipt.

A filing regime may make delivery irrevocable at outbox commitment only through an explicit content-addressed regime policy accepted in the separate transport-release boundary. Irrevocability is never the v0.2 default and cannot be inferred from idempotency or from the fact that the human filing act completed.

The outbox commit does not claim receiver acceptance, delivery, or an external legal consequence that the receiver has not acknowledged. If a filing regime makes receipt or transmission itself a new authority-bearing human act, this row is insufficient. That regime needs a separate action class and governed boundary in a stacked RFC; a dispatcher must not reuse `OUTPUT_FILE_SUBMISSION_ASSEMBLY` to impersonate the required human.

### 18.7 Non-`ALLOW` responses

For a schema-valid authorization request whose outcome is `DENY`, `REQUIRE_REVIEW`, or `REQUIRE_HUMAN_APPROVAL`, the request/result/full-internal-trace refusal bundle commits atomically with no protected effect. The caller-facing surface must then return or link a CP2-compatible `ResultQualificationEnvelope` plus registered `RuntimeProblem` entries. It must preserve a truthful safe category and redaction posture while withholding sensitive basis details.

The proposed public mapping is:

- `DENY` -> registered public code `AUTHORIZATION_DENIED`;
- `REQUIRE_REVIEW` -> registered public code `AUTHORIZATION_REVIEW_REQUIRED`;
- `REQUIRE_HUMAN_APPROVAL` -> registered public code `HUMAN_ACTION_REQUIRED`, plus only the safe challenge display/ref allowed by its display policy;
- ingress rejection -> registered public code `REQUEST_INVALID`; and
- withheld or redacted diagnostics/trace -> CP2 permission/redaction posture plus registered public code `DETAILS_REDACTED` when details were suppressed.

These are proposed entries in the active CP2 RuntimeProblem reason-code process, not an authorization-private vocabulary. The CP2 envelope must truthfully carry or link permission/redaction posture, applicable data-absence reason, blocked use classes, trace availability/redaction/denial posture, and safe display hints. The current CP2 schema does not enumerate an authorization-result surface, so a separate CP2-compatible machine-contract change must be accepted before a public runtime claims v0.2 conformance; this candidate does not edit that active contract.

Basis identifiers, unseen resource existence, grant/revocation details, internal reason ranking, validation locations, policy internals, and full trace content remain internal. Full retrieval requires the separate authorized trace read in section 18.5. Minimization may redact sensitive details, but it may not hide whether the result was denied, requires review, requires human action, was invalid, or had details withheld.

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
- a source without issuance-policy identity and exact per-action rule bindings cannot prove that its grantor consented to the selected rule meaning;
- a caller-provided schema ref cannot reconstruct the rule-selected effect-intent schema binding or immutable binding manifest;
- optional AI metadata cannot reconstruct principal resolution, representation, CP3 posture, or human finalization;
- a sponsor or globally inferred Party cannot reconstruct a path-specific software-agent authority subject or its direct-grant/delegation basis;
- a target reference cannot reconstruct the rule-derived authority target, typed inputs, effect-subject separation, or existence posture;
- one target reference cannot reconstruct named resource postures/roles or their `ALL_OF`/`ONE_OF` disposition;
- caller target time cannot reconstruct trusted evaluation/effect time;
- an unbound payload cannot reconstruct the effect-intent digest;
- an approval reference, boolean, or display digest without retained representation bytes/renderer metadata cannot reconstruct the challenge, what the human saw, the authenticated human act, challenge/final relevant-state digest equality, approver authority path, separation policy, or single-use consumption;
- a read response cannot reconstruct same-snapshot query/redaction/qualification/result-coverage evidence, prove safe trace disclosure, or prove that evidence committed before disclosure; a digest-only payload receipt can verify candidate bytes but cannot reconstruct them;
- a scope string cannot reconstruct scope proof;
- mutable basis references cannot reconstruct the authority-evaluation snapshot;
- free-text purpose cannot reconstruct a purpose token;
- free-text conditions cannot be presumed satisfied; and
- untyped evidence refs cannot reconstruct an eligibility disposition.

### 19.3 Source migration

Migration creates a new v0.2 source record and preserves a provenance link to the v0.1 record. A steward must explicitly decide:

- the exact authority-family tokens;
- a new immutable source ID and complete source-record digest;
- the issuance-policy identity and exact per-action rule ID/digest bindings;
- immutable `issuanceState`, with any activation represented by a different source ID;
- closed delegation permission and any delegated action list;
- the purpose-token set, if any;
- how each legacy condition is preserved in supported closed constraints;
- every typed evidence-policy group, if required;
- authority-target/input/effect-subject narrowing; and
- whether the v0.1 source is retired, allowed to expire, or retained for the v0.1 evaluator only.

Automated migration may propose a mapping. It may not activate the new authority without steward approval.

### 19.4 Rule compatibility

Automatic source reuse is permitted only when the selected action's current rule ID and digest exactly equal the source's `authorizedRuleBindings` entry. Any digest change, whether believed to narrow or widen, requires a new source ID through explicit migration or governed reapproval. This conservative v0.2 rule deliberately avoids a generic semantic-subset engine.

A future accepted extension may permit cross-digest reuse through a content-addressed compatibility certificate whose issuer, proof method, covered old/new rule digests, and no-widening result are governed and auditable. No such certificate exists in v0.2, and a runtime cannot synthesize one.

### 19.5 Coexistence

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
| `AUTHORIZATION_VIEW_EXTRACTION_INVALID` | the rule-selected extractor is invalid or a required derived fact is missing, duplicated, type-invalid, conflicting, or of an unknown concrete kind |
| `INGRESS_AUDIT_PERSISTENCE_FAILED` | required rejection evidence could not be persisted |

These codes may appear only in `AuthorizationRequestRejection` or runtime/security telemetry. They must not be placed in a decision result or converted locally into `DENY`.

| Reason code | Default outcome | Rank |
|---|---:|---:|
| `AUTHORIZED_BY_SELECTED_PATH` | `ALLOW` | 0 |
| `HUMAN_FINAL_ACTION_REQUIRED` | `REQUIRE_HUMAN_APPROVAL` | 100 |
| `APPROVAL_CHALLENGE_STALE` | `REQUIRE_HUMAN_APPROVAL` | 110 |
| `APPROVAL_EXPIRED` | `REQUIRE_HUMAN_APPROVAL` | 120 |
| `APPROVAL_SEPARATION_UNSATISFIED` | `REQUIRE_HUMAN_APPROVAL` | 130 |
| `APPROVER_AUTHORITY_INSUFFICIENT` | `REQUIRE_HUMAN_APPROVAL` | 140 |
| `AUTHORIZATION_SNAPSHOT_UNAVAILABLE` | `REQUIRE_REVIEW` | 200 |
| `POLICY_NOT_AVAILABLE` | `REQUIRE_REVIEW` | 210 |
| `POLICY_DIGEST_MISMATCH` | `REQUIRE_REVIEW` | 220 |
| `UNSUPPORTED_REVOCATION_NARROWING` | `REQUIRE_REVIEW` | 230 |
| `UNSUPPORTED_EVIDENCE_POLICY` | `REQUIRE_REVIEW` | 240 |
| `EFFECT_INTENT_DIGEST_MISMATCH` | `DENY` | 1000 |
| `UNRESOLVED_PRINCIPAL` | `DENY` | 1010 |
| `REPRESENTATION_BASIS_INVALID` | `DENY` | 1020 |
| `AUTHORITY_SUBJECT_BASIS_INVALID` | `DENY` | 1030 |
| `CP3_EVIDENCE_MISSING` | `DENY` | 1040 |
| `CP3_AUTHORITY_SNAPSHOT_MISSING` | `DENY` | 1050 |
| `SOFTWARE_AGENT_NOT_PERMITTED` | `DENY` | 1060 |
| `APPROVAL_EFFECT_INTENT_MISMATCH` | `DENY` | 1080 |
| `APPROVAL_ALREADY_CONSUMED` | `DENY` | 1090 |
| `DECISION_EXPIRED` | `DENY` | 1100 |
| `DECISION_ALREADY_CONSUMED` | `DENY` | 1110 |
| `AUTHORITY_STATE_CHANGED_BEFORE_EFFECT` | `DENY` | 1120 |
| `TENANT_BOUNDARY_MISMATCH` | `DENY` | 1130 |
| `COMPOSITE_RESOURCE_REQUIREMENT_UNSATISFIED` | `DENY` | 1140 |
| `AUTHORITY_TARGET_NOT_PROVEN` | `DENY` | 1150 |
| `NON_AUTHORITY_INPUT_NOT_PROVEN` | `DENY` | 1155 |
| `EFFECT_SUBJECT_NOT_PROVEN` | `DENY` | 1160 |
| `RESOURCE_KIND_MISMATCH` | `DENY` | 1170 |
| `SUBJECT_KIND_MISMATCH` | `DENY` | 1180 |
| `RESOURCE_REF_MISMATCH` | `DENY` | 1190 |
| `SUBJECT_REF_MISMATCH` | `DENY` | 1200 |
| `PACK_RELEASE_MISMATCH` | `DENY` | 1210 |
| `REVOCATION_TARGET_MISMATCH` | `DENY` | 1215 |
| `TWIN_MISMATCH` | `DENY` | 1220 |
| `SCOPE_NOT_PROVEN` | `DENY` | 1230 |
| `ACTIVE_REVOCATION` | `DENY` | 1240 |
| `AUTHORITY_NOT_ACTIVE_AT_AUTHORIZATION_TIME` | `DENY` | 1250 |
| `ROLE_ASSIGNMENT_NOT_APPLICABLE` | `DENY` | 1270 |
| `ROLE_ANCHOR_SCOPE_MISMATCH` | `DENY` | 1280 |
| `DELEGATION_PROHIBITED_BY_ACTION_RULE` | `DENY` | 1290 |
| `DELEGATION_NOT_PERMITTED_BY_SOURCE` | `DENY` | 1300 |
| `DELEGATION_SOURCE_MISSING` | `DENY` | 1310 |
| `DELEGATION_BROADENS_AUTHORITY` | `DENY` | 1320 |
| `DELEGATION_CYCLE` | `DENY` | 1330 |
| `DELEGATION_DEPTH_EXCEEDED` | `DENY` | 1340 |
| `SHARING_BASIS_MISMATCH` | `DENY` | 1350 |
| `SOURCE_RULE_BINDING_MISMATCH` | `DENY` | 1355 |
| `ACTION_CLASS_NOT_GRANTED` | `DENY` | 1360 |
| `AUTHORITY_FAMILY_MISMATCH` | `DENY` | 1370 |
| `INHERITANCE_NOT_PERMITTED` | `DENY` | 1380 |
| `PURPOSE_REQUIRED` | `DENY` | 1390 |
| `PURPOSE_NOT_PERMITTED` | `DENY` | 1400 |
| `EVIDENCE_POLICY_REQUIRED` | `DENY` | 1410 |
| `REQUIRED_EVIDENCE_MISSING` | `DENY` | 1420 |
| `REQUIRED_EVIDENCE_INELIGIBLE` | `DENY` | 1430 |
| `READ_RESULT_COVERAGE_NOT_PROVEN` | `DENY` | 1440 |
| `TRACE_DISCLOSURE_NOT_AUTHORIZED` | `DENY` | 1450 |
| `NO_AUTHORITY_BASIS` | `DENY` | 1990 |

`HUMAN_FINAL_ACTION_REQUIRED` is the sole primary reason for a current `REQUIRE_HUMAN_APPROVAL` result. Ranks 110 through 140 are ordered diagnostics only; rank 130 and `APPROVAL_SEPARATION_UNSATISFIED` remain reserved until a current rule selects `DISTINCT_APPROVER_REQUIRED`.

The accepted CP3 posture `AGENT_ALLOWED_WITH_PREFLIGHT_ONLY` remains part of the preserved vocabulary, but no current v0.2 row selects it. `PREFLIGHT_REQUIRED` therefore is not a current v0.2 reason code and cannot be emitted by this bundle.

Unlisted numeric ranks are reserved and have no implied meaning. In particular, the unused 250 through 270 legacy slots, 1070 preflight slot, and 1260 deny slot are intentional gaps; an implementation may not assign them locally. v0.1 free-text purpose, conditions, and untyped evidence are migration inputs, not v0.2 path outcomes.

`DECISION_BUNDLE_PERSISTENCE_FAILED`, `DECISION_BUNDLE_PROJECTION_INVALID`, `READ_EVIDENCE_PERSISTENCE_FAILED`, protected-effect contract validation failures, transport-release/transport failures, and failure of another non-authority EnforcementChain gate are runtime/integrity/domain-gate results, not authorization outcomes, and therefore have no reason rank. A runtime must not fabricate or rewrite an authorization result to place them in this table.

Problem severity is fixed by outcome: `ALLOW` is `INFO`, `REQUIRE_HUMAN_APPROVAL` and `REQUIRE_REVIEW` are `WARNING`, and `DENY` is `ERROR`. Global-result diagnostics use section 15.4's order. After global preconditions pass, path diagnostics are ordered with the selected path first, then by path-type order, immutable source record ID, numeric rank, and related reference. Severity never chooses the primary reason.

Additional codes require a versioned policy update. Implementations must not collapse a known authorization failure into an unstructured message or assign local ranks.

The caller-facing CP2 codes proposed in section 18.7 are registered RuntimeProblem categories, not substitutes for these internal authorization reasons. Their registration and any `ResultQualificationEnvelope` surface extension travel in a separate CP2 machine-contract change.

---

## 21. Invariants

The accepted design and conformance suite must preserve these invariants:

1. Omitting or changing optional AI-assistance metadata never increases authority.
2. The validated effect intent is the only caller-authored source of operation facts; mirrored resource, subject, scope, time, purpose, grantee, destination, rights, or payload fields are prohibited.
3. Exactly one immutable action rule selects the intent schema, protected-effect contract binding where applicable, authorization-view/relevant-state projections, resource roles, validity function, historical posture, external-effect posture, evidence policy, approval policy, and consumption mode.
4. A caller can select neither a weaker schema nor a different extractor.
5. Every current rule derives exactly one `AUTHORITY_TARGET`; no action unions grants over different resource roles or target branches.
6. Integrity, applicability, state, and evidence inputs pass their own typed checks and never create authority.
7. The existing authority target and prospective effect subject are not conflated.
8. A pre-revocation `subjectTime` never authorizes a post-revocation current effect.
9. Unknown action, family, role, posture, concrete kind, effect-subject kind, condition, evidence policy, or proof type is fail-closed at ingress or authorization as its governing contract specifies.
10. Principal resolution, represented Party, representation basis, CP3 posture, and human-finalization requirement remain separate axes.
11. Every candidate path derives its own authority-subject Party and immutable direct-grant, representation, or delegation basis; sponsor identity never supplies authority.
12. Every software-agent path preserves the accepted CP3 posture and mandatory authority snapshot.
13. Authorization `ALLOW` is only a successful authority gate; it never bypasses another applicable Platform `EnforcementChain` gate.
14. Human approval is bound to the exact effect intent, derived view, retrievable content-addressed display bytes and renderer/display metadata, policy/rule/extractor, authority subject, represented Party, and validity window.
15. Every approver independently satisfies a natural-person path for the same action and effect; sponsorship alone is insufficient.
16. Challenge and final full snapshot refs may differ, but their rule-selected `authorityRelevantStateDigest` values must be equal; relevant change requires a new challenge and unrelated history does not.
17. Direct human invocation satisfies fresh approval only through the lifecycle and under `SAME_PRINCIPAL_ALLOWED`; a distinct-approver profile is independently enforced.
18. Approval and decision are single-use, and their consumption commits atomically with the protected effect, buffered read evidence, or filing-outbox record.
19. Payload substitution, pre-consumption expiry, and replay are non-`ALLOW`.
20. `SHARE_REVOKE_ACCESS` creates a prospective `RevocationDecision` that terminates one exact immutable SharingGrant ID and never edits that SharingGrant.
21. Pack activation/deactivation creates a prospective `StructureEvent` and successor activation state and never edits its prior activation set.
22. Pack release, installation, activation set, scope, and registry identities remain distinct; only the target scope is an authority target.
23. A role-targeted grant never exceeds either its grant scope or its role anchor scope.
24. A delegated path never exceeds the action-rule ceiling, source permission, source role anchor, or DelegationGrant at any dimension.
25. A purpose-constrained source cannot pass without the exact purpose extracted from the intent; a duplicate caller-only purpose never creates authority.
26. Free-text purpose and conditions are never guessed into executable v0.2 semantics.
27. Evidence requirements from the action rule and every selected source are cumulative and bind immutable active policy/evidence revisions.
28. Authority-target, typed-input, effect-subject, scope, constraint-evidence, read-qualification, and sovereignty proofs remain typed and distinct.
29. A SharingGrant grants read/receive use only for its exact grantee and immutable artifact revision.
30. Every effective revocation is considered from a completeness-proven snapshot and watermark and targets one exact immutable source ID; no lineage reach is inferred.
31. Partial paths or paths with different authority subjects are not unioned; mixed paths aggregate under one total lattice.
32. The same immutable intent/view, relevant snapshot facts, policy bytes, and basis revisions produce the same authority result and ordered evidence.
33. An internal domain effect passes its separately owned, rule-bound protected-effect contract and commits with its authorization evidence in one atomic transaction; authorization audit records do not create domain truth or event/commit classification.
34. Every unredacted read row, field, aggregate, count, metadata item, and lineage item has result-coverage proof under one governed snapshot before disclosure, and its receipt states whether payload bytes are retained/reconstructible or digest-only.
35. CP2 qualification describes a read result but never supplies missing read authority.
36. Protected streaming is unsupported in v0.2; only a fully evidenced buffered payload may cross the trust boundary.
37. Full traces are internal; caller-facing results use CP2 qualification and registered safe categories, truthfully indicate denial/review/human-action/redaction posture, and require a separate authorized `AUTHORIZATION_TRACE` read for full retrieval.
38. The authenticated human's atomic filing-outbox commit is the final authority-bearing filing act.
39. Later transport can send or retry only the committed bytes/destination/idempotency key after a separate current release-eligibility gate; post-commit expiry or revocation does not retroactively undo the filing act but may block future disclosure.
40. A typed authorization refusal never claims a durable trace that did not commit.
41. Malformed, schema-invalid, or extraction-invalid input creates only ingress rejection evidence and never a validated authorization outcome bundle.
42. Digest projection removes only `/result/decisionBundleDigest` and `/trace/decisionBundleDigest`; every other occurrence remains hashed, and an absent, malformed, or non-unique expected field fails integrity construction.
43. Every reconstructed decision resolves the same immutable basis and policy bytes visible at its recorded snapshot; v0.2 source IDs resolve to exactly one immutable record digest.
44. v0.1 records never silently claim v0.2 proof strength.
45. Draft schema presence never changes current/default status.
46. Every v0.2 authority source records issuance-policy identity and an exact selected-rule binding for each granted action; the rule digest covers the complete resolved per-action semantic closure, and any different closure digest is non-`ALLOW` until explicit migration or reapproval.
47. No runtime invents cross-digest semantic-subset compatibility; v0.2 automatic reuse is exact-digest only.
48. Every v0.2 AuthorityGrant, DelegationGrant, and SharingGrant ID is a one-record identity; a correction, replacement, renewal, activation, or restriction receives a new ID.
49. Current claim/report authority, alleged performer identity, and historical execution authority remain separate; current rows do not evaluate the reporter's path as performer authority at `subjectTime`.
50. A protected-effect receipt proves intent/result/contract binding only after the separately owned domain contract validates the proposed result; the authorization evaluator does not own domain mappings.
51. A display or payload digest never claims byte reconstruction without retrievable candidate bytes, and retention/key-custody policy remains separately governed.
52. Every final review binds exactly one eligible governed-record target, including an exact accepted-event-consequence revision when selected, and one rule-constrained outcome posture; only `REVIEW_ACCEPT` and `REVIEW_REJECT_OR_CONTEST` add the exact evidence-sufficiency-case branch, while `REVIEW_SUPERSEDE`, `REVIEW_REQUEST`, and unrelated action classes do not inherit that case-eligible closure.

---

## 22. Production-reachable hostile cases

The future executable conformance suite must include at least:

| Case | Required disposition |
|---|---|
| Same request retried after omitting `aiAssistance.assisted: true` | same resolved principal, CP3 posture, and no authority increase |
| Caller changes `nonHumanActor` or derived family/stage hint | hint ignored or schema-rejected; policy result unchanged |
| Caller supplies a weaker effect-intent schema that omits an authorization-relevant field | ingress rejection with `EFFECT_INTENT_SCHEMA_CLAIM_MISMATCH`; rule-selected schema remains authoritative |
| Bound effect-intent schema bytes differ while ref/version remain unchanged | ingress rejection with `ACTION_RULE_BINDING_INVALID`; no evaluation or effect |
| An unchanged source record is evaluated after its action rule adds a target kind, changes the extractor, weakens evidence, relaxes human finalization, or widens delegation | `DENY` with `SOURCE_RULE_BINDING_MISMATCH`; no automatic cross-digest reuse |
| The visible action row is unchanged, but shared purpose comparison, role/grant/scope intersection, revocation application, tenant/proof interpretation, partial-path prohibition, or path aggregation changes | the resolved semantic closure and `ruleDigest` change; the old source is `DENY` with `SOURCE_RULE_BINDING_MISMATCH` |
| An implementation claims a changed rule is a stricter subset without an accepted compatibility extension | conformance failure; v0.2 requires exact rule-digest equality or a new governed source ID |
| Caller supplies a mirrored resource, scope, subject, purpose, destination, grantee, rights, or payload fact outside the effect intent | request-schema rejection; no duplicate authority fact is reconciled |
| Rule-selected extractor pointer is missing, duplicated, type-invalid, or resolves an unknown broad bucket such as `GOVERNED_RECORD` | ingress rejection with `AUTHORIZATION_VIEW_EXTRACTION_INVALID` |
| Authority is revoked, then a current request supplies a pre-revocation `subjectTime` | current effect is `DENY`; subject time never replaces trusted current time |
| A farmer with current report authority reports work allegedly performed by a contractor | submission authority is evaluated against the farmer now; contractor identity/evidence remains claim provenance for later review/promotion |
| A successor operator submits a retrospective correction | current correction/report authority is evaluated now; the predecessor's historical path is not required merely because the subject time is earlier |
| An authorized reporter describes work allegedly performed without execution authority | the report may enter only as a qualified claim when the current submission path passes; it cannot become an accepted execution consequence until evidence/review/promotion closes performer authority |
| Natural person acts for an organization without a valid immutable representation basis | `DENY` |
| Organization-held grant is evaluated against the authenticated natural person rather than `authoritySubjectPartyRef` | conformance failure |
| Agent has a direct grant for Party A and explicit delegation for Party B | two independent path-specific authority subjects; no global Party and no cross-path union |
| Agent sponsor is substituted for a missing grant/delegation authority subject | `DENY`; sponsor identity creates no authority |
| Software agent omits the mandatory CP3 authority snapshot | `DENY` |
| Sponsor-bound agent attempts a human-only review decision | non-`ALLOW` |
| Agent sponsor approves an `FA` action but lacks an independently sufficient natural-person path for that same action and effect | `REQUIRE_HUMAN_APPROVAL`; primary `HUMAN_FINAL_ACTION_REQUIRED`; diagnostic `APPROVER_AUTHORITY_INSUFFICIENT` |
| A natural person other than the challenge-bound intended approver submits the act | challenge invalid for that principal; issue a new challenge after evaluating that person's path |
| Actual agent read lacks the rule-selected CP2 qualification evidence | `DENY`; `PREFLIGHT_ONLY` is not used to authorize the read |
| Governed read authorization and retrieval observe different snapshots | no disclosure; conformance failure |
| Governed read decision/read-receipt persistence fails before response | zero protected bytes leave; `READ_EVIDENCE_PERSISTENCE_FAILED` runtime failure |
| Read response substitutes another resource revision, query/plan, redaction policy, qualification envelope, or payload | digest/binding failure; zero substituted protected bytes leave |
| A retained read's serializer version or payload bytes change after disclosure | receipt reconstruction/verification fails against the bound serializer and payload digest |
| A read uses `DIGEST_ONLY` evidence because retention policy forbids payload retention | receipt explicitly says digest-verifiable, not byte-reconstructible; immutable disclosure fact/digest remain |
| One returned row or field lacks authority coverage although the containing query was authorized | withhold/redact it or `DENY` with `READ_RESULT_COVERAGE_NOT_PROVEN`; never release it |
| Aggregate, count, metadata, error detail, or lineage leaks an unauthorized record or resource existence | withhold/redact it or `DENY`; CP2 qualification does not create authority |
| Caller requests protected streaming | ingress rejection because `EI_DATA_READ_V0_2` fixes buffered mode; zero protected bytes leave |
| Denial response exposes grant IDs, revocation details, or unseen resource existence from the full trace | disclosure conformance failure |
| Denial or review response hides whether it was denied, requires review, or had details redacted | CP2 conformance failure even when sensitive basis details remain protected |
| Denial response returns a safe CP2 category and redaction posture without grant IDs, target existence, or revocation details | conforming minimized response |
| Caller requests a full decision trace without a sufficient `RECEIVE_READ_DATA` path over its exact `AUTHORIZATION_TRACE` | `DENY` or redacted response with CP2 indication; internal trace remains protected |
| AI-assisted high-risk assertion has no fresh human approval for the exact effect-intent digest | `REQUIRE_HUMAN_APPROVAL` |
| Unrelated canonical history advances between challenge and final evaluation while the relevant-state digest is unchanged | approval may proceed; both full snapshot refs are recorded |
| Grant, role, revocation, target/input revision, evidence eligibility, policy, or separation state changes between challenge and final evaluation | relevant-state digest changes; old act is stale and a new challenge/human act is required |
| Approval challenge or approval expires before effect consumption | `REQUIRE_HUMAN_APPROVAL`; primary `HUMAN_FINAL_ACTION_REQUIRED`; diagnostic `APPROVAL_EXPIRED`; no effect |
| Approval display bytes, renderer version, locale, timezone, or display-policy revision differ from the challenge evidence | prior act is ineligible; issue a new challenge over newly retained display bytes |
| Approval records only a display digest but the exact representation bytes are unavailable | reconstructibility conformance failure; no v0.2 approval claim |
| Natural person directly invokes an `FA` row under `SAME_PRINCIPAL_ALLOWED` | the same explicit act may satisfy approval only through the section 18.3 lifecycle and an independently sufficient same-action path |
| Approval covers payload A but the protected operation substitutes payload B | digest mismatch; `DENY` and no effect |
| Authorized read-only sharing intent produces a SharingGrant with broader rights | protected-effect contract validation failure; transaction aborts without rewriting the authorization result |
| Authorized assertion body, review-decision kind, destination, or pack successor state differs in the proposed result | protected-effect contract validation failure; transaction aborts |
| A final review effect intent names one exact `ACCEPTED_EVENT_CONSEQUENCE`, but an evaluator omits that eligible kind or substitutes another kind/ref/revision | omission is a rule/extractor conformance failure and cannot produce `ALLOW`; substitution changes the bound intent/resource view and requires a new authorization decision |
| A `REVIEW_ACCEPT` or `REVIEW_REJECT_OR_CONTEST` intent names one exact `EVIDENCE_SUFFICIENCY_CASE`, but the evaluator omits that eligible kind or substitutes another kind/ref/revision | omission is a rule/extractor conformance failure and cannot produce `ALLOW`; substitution changes the bound intent/resource view and requires a new authorization decision |
| `REVIEW_SUPERSEDE`, `REVIEW_REQUEST`, or another action attempts to use the case-eligible final-review resource policy or target branch | rule-policy binding fails; the case target cannot widen an action whose exact row does not select it |
| `REVIEW_REJECT_OR_CONTEST` intent binds `REJECTED`, but the proposed `ReviewDecision` result says `CONTESTED`, or vice versa | protected-effect contract validation failure; transaction aborts without rewriting the authorization result or intent |
| Consumed human approval is replayed with the same challenge and payload | `DENY` with `APPROVAL_ALREADY_CONSUMED`; no effect |
| A single-use decision is consumed twice with the same payload | second consumption is `DENY` |
| A decision is consumed after `decisionValidUntil` | `DENY` |
| Revocation commits between evaluation and an internal governed write | serialization/revalidation failure; no effect |
| Revocation or expiry occurs before the human-final filing-outbox commit | transaction fails/re-evaluates; no filing effect |
| Source grant, approval, session, or decision expires after the filing-outbox commit | human filing act remains historically valid; current transport-release policy independently decides whether bytes may be released |
| Sharing, sovereignty, recipient, custody, endpoint, or hold posture changes after outbox commit but before delivery | release gate blocks or holds disclosure while preserving the historical filing act |
| Regime policy claims delivery became irrevocable at outbox commit | allowed only when an explicit content-addressed transport-release policy established that rule before commitment; never inferred by default |
| Transport worker changes committed filing bytes, destination, filing mode, or idempotency key | conformance failure; no altered send |
| Grant purpose is `REGULATORY_FILING` and request purpose is `regulatory_filing` | exact mismatch; non-`ALLOW` |
| Intent supplies a purpose but source does not authorize it | exact mismatch; caller intent cannot create authority |
| A v0.1 source with free-text purpose/conditions or untyped evidence is offered to the v0.2 evaluator | `DENY` with `SOURCE_RULE_BINDING_MISMATCH` before those fields are evaluated; no legacy review reason |
| A v0.1 evaluator handles that source | only v0.1 policy/outcomes apply; it cannot claim v0.2 proof strength or emit v0.2 reasons |
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
| Role-targeted grant scope covers the authority target but role anchor does not | `DENY` |
| Delegated source is role-targeted and its role anchor does not cover the authority target | `DENY` |
| Prospective observation is rejected merely because it does not already exist | conformance failure; prospective proof rules apply |
| Existing-only subject does not exist | `DENY` |
| Pack install intent names one release digest and the protected effect substitutes another | `DENY` and no effect |
| Pack activation-set identifier is substituted for the installed pack release | `DENY` |
| Pack install omits its registry or release input | effect-intent schema/extraction rejection; those inputs do not require extra grants |
| Pack install supplies a registry/release ref whose immutable binding cannot be proven | `DENY` with `NON_AUTHORITY_INPUT_NOT_PROVEN`; no pack-applicability success is claimed |
| Runtime tries to combine one grant for target scope and another grant for a pack release input | conformance failure; only target scope is authority-bearing and paths are never unioned |
| Pack deactivation edits the prior activation set instead of creating the bound StructureEvent and successor state | conformance failure; no mutation of the prior set |
| Assembly request supplies both branches of `RP_ASSEMBLY_ONE` | `DENY`; `ONE_OF` ambiguity cannot widen authority |
| Authority target exists but has the wrong concrete resource kind | `DENY` |
| Scope string matches but no trusted scope proof exists | `DENY` |
| Authority-target proof is placed in `dataSovereigntyBoundaryRefs` | schema or semantic rejection |
| Scope proof is substituted into `constraintEvidenceRefs` | schema or semantic rejection |
| Policy version matches but digest differs | non-`ALLOW` |
| Active `TERMINATE` revocation is omitted from caller candidates | revocation still found; `DENY` |
| Active v0.1 narrowing revocation is present | `REQUIRE_REVIEW` until closed semantics exist |
| SharingGrant artifact family/ref/revision differs from the read target | `DENY` |
| SharingGrant is offered for a write or review action | basis ineligible |
| A direct receive/use path supplies only action coverage while a SharingGrant or resource-control fact supplies a missing purpose/evidence constraint | paths remain independently insufficient; no cross-basis or cross-layer union |
| `SHARE_REVOKE_ACCESS` attempts to edit or delete the existing SharingGrant | conformance failure; effect must be a prospective `RevocationDecision` |
| `SHARE_REVOKE_ACCESS` names a RevocationDecision affecting a different grant/artifact or a narrowing mode | `DENY` with `REVOCATION_TARGET_MISMATCH` or unsupported narrowing; no effect |
| One grant supplies action and another supplies matching purpose | paths remain incomplete; non-`ALLOW` |
| One path lacks only human approval, one has an unsupported evidence policy, and one is revoked | `REQUIRE_HUMAN_APPROVAL`; selected human path supplies `HUMAN_FINAL_ACTION_REQUIRED` as primary |
| One path allows and another is revoked | `ALLOW`; `AUTHORIZED_BY_SELECTED_PATH` is primary and revocation remains diagnostic |
| No path allows; one requires review and all others deny | `REQUIRE_REVIEW` with the selected review path's lowest rank |
| Policy digest mismatches and untrusted bytes would otherwise imply a tenant-boundary mismatch | `REQUIRE_REVIEW` with `POLICY_DIGEST_MISMATCH`; target/effect-subject proof and tenant isolation are `NOT_EVALUATED`; no path aggregation |
| Authority snapshot is unavailable and dependent target/effect-subject or tenant facts cannot be evaluated truthfully | `REQUIRE_REVIEW` with `AUTHORIZATION_SNAPSHOT_UNAVAILABLE`; dependent global checks are `NOT_EVALUATED`, not fabricated failures |
| A writer attempts to store changed source bytes under an existing v0.2 grant/delegation/sharing ID | schema/storage conformance failure; the changed source must receive a new governed ID |
| A terminated source is replaced under a new ID | replacement has no inherited authority or revocation posture; it must independently pass issuance, exact rule binding, and current evaluation |
| A revocation lookup applies one source ID's decision to a different replacement ID through inferred lineage | conformance failure; v0.1 `TERMINATE` lookup is exact family plus immutable source ID |
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
| Authority gate returns `ALLOW` but validation, pack applicability, evidence, review/promotion, materialization, or publication/export gate fails | no protected effect; authority result remains an authority-gate result only |
| Authorization result/trace/receipt is promoted as domain truth or current state | conformance failure; it is append-only EvidenceEvent/evidence-record audit support only |
| Draft v0.2 files exist but currentness still names v0.1 | v0.1 remains current/default |

Fixtures must enter through production-reachable evaluator and persistence paths. Unit-only helper tests are not enough for a conformance claim.

### 22.1 Reserved future-semantics examples

The following examples document preserved closed vocabulary but are not production-reachable v0.2 fixtures and are not part of the current conformance claim. A later action-rule version must select the posture/policy and register any needed current reason before these cases become executable.

| Reserved case | Future required disposition |
|---|---|
| A future row selects `AGENT_ALLOWED_WITH_PREFLIGHT_ONLY` and an agent attempts the protected action rather than an allowed preflight | protected action is denied; the future bundle defines its current reason, while preflight output remains non-protected |
| A future `FA` row selects `DISTINCT_APPROVER_REQUIRED` and the requesting principal attempts to approve | `REQUIRE_HUMAN_APPROVAL`; primary `HUMAN_FINAL_ACTION_REQUIRED`; diagnostic `APPROVAL_SEPARATION_UNSATISFIED`; no effect |
| A future row selects `PROHIBITED_FOR_AGENT` and a software agent invokes it | `DENY`; the future bundle defines its current reason |

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
| Composite pack resources have ambiguous singular/alternative semantics | sections 7.5, 7.8, 8.3, and 22 distinguish the one authority target from typed non-authority inputs |
| Governed reads lack same-snapshot authorization/disclosure evidence and preflight-only is reinterpreted | sections 6.3, 7.2, 7.8, 13, and 18.5 |
| Human-only filing conflicts with software dispatch under the same action | sections 7.3, 7.8, and 18.6 make the authenticated human's outbox commit the final filing act while a separate current release gate controls disclosure |
| Share revocation and pack deactivation mutate the wrong effect subject | sections 7.2, 7.5, 7.6, 8.5, 13, and 14 make RevocationDecision and StructureEvent/successor state prospective effects |
| Authorization bypasses EnforcementChain and audit records lack domain classification | sections 5.1, 14.4, 17.2, and 18.4 limit `ALLOW` to the authority gate and leave event/commit truth to active domain contracts |
| Human approval has no exact approver eligibility and full snapshot equality rejects unrelated history | sections 6.4, 16.1, and 18.3 require an independent same-action natural-person path plus relevant-state digest equality |
| Broad resource buckets and heterogeneous pack roles permit ambiguous or combined authority | sections 7.5 and 8.3 enumerate concrete kinds, one authority target, and typed non-authority inputs |
| Request and effect intent duplicate authorization facts without an exact binding | sections 5.2, 7.4, 8.2, 17.4, and 18.1 make intent plus rule-selected extraction the sole source |
| Read rows/fields/aggregates/metadata, streaming revocation, and denial traces can leak | sections 13, 18.5, 18.7, 21, and 22 require complete buffered-result coverage and separate authorized/redacted trace retrieval; streaming is out of v0.2 |
| Software-agent authority subject is globally inferred and not derivable from current CP3 | sections 6.2, 9, 10, 13, 15, and 17 |
| Invalid request cannot truthfully inhabit a validated refusal bundle | sections 15.4, 17.2, 18.1, 18.7, and 20 |
| Name-based decision-digest exclusion permits nested exclusion injection | sections 18.8, 21, and 22 |
| Existing grants silently inherit changed action-rule or shared authorization meaning | sections 7.4, 9, 10, 13, 16, 17.3, 19.3, 19.4, 21, and 22 require a digest of the complete resolved per-action semantic closure and no automatic cross-digest reuse |
| RevocationDecision cannot identify a mutable source revision | sections 14, 16.1, 17.3, 19.3, 21, and 22 make every v0.2 source ID a one-record immutable identity and keep v0.1 `TERMINATE` lookup exact |
| Intent is bound but the committed result can widen it | sections 7.4, 8.8, 18.4, 21, and 22 require a separately owned protected-effect contract binding and pre-commit validation without moving domain semantics into authorization |
| Historical authority conflates reporter and performer | sections 7.6, 7.8, 8.1, 17.6, 21, and 22 use current report authority and retain alleged performer identity/authority as separate claim evidence |
| Post-commit transport ignores current disclosure revocation | sections 7.3, 8.1, 18.2, 18.6, 21, and 22 preserve the filing act but require a separately governed current release decision |
| Hash-only display and read evidence overclaims reconstruction | sections 18.3, 18.5, 19.2, 21, and 22 require retained display bytes and explicit retained-versus-digest-only payload proof posture while leaving custody policy separate |
| Minimum disclosure hides CP2-required authorization and redaction posture | sections 18.7, 20, 21, and 22 reuse CP2 qualification and its registered RuntimeProblem process without exposing sensitive internal reasons |
| Final review cannot target an accepted event consequence or an eligible evidence-sufficiency case, or distinguish reject from contest before result validation | sections 7.2, 7.5, 7.6, 7.8, 8.2, 21, and 22 bind accepted consequences for all final-review rows, add case targets only to accept/reject-or-contest, and bind the intent outcome while leaving result mapping to the protected-effect contract |
| Human-approval primary reasons conflict with approval-specific hostile outcomes | sections 15.6, 20, and 22 make `HUMAN_FINAL_ACTION_REQUIRED` primary and approval-lifecycle codes ordered diagnostics only |
| v0.1 legacy-purpose/condition/evidence review outcomes are unreachable under exact v0.2 rule binding | sections 11, 12, 19, 20, and 22 keep v0.1 under v0.1, require explicit migration, and use `SOURCE_RULE_BINDING_MISMATCH` if a v0.1 source is offered to v0.2 |
| `RECEIVE_READ_DATA` is described as a partial-path exception | sections 5.4, 13, and 22 require every direct, delegated, or SharingGrant access basis to be independently sufficient |
| Simultaneous authorization-global failures have no deterministic result, dependency rule, or primary reason | sections 15.4, 15.6, 16, 20, and 22 evaluate only independently trusted facts, mark policy/snapshot-dependent checks `NOT_EVALUATED`, give an independently established global `DENY` precedence over global `REQUIRE_REVIEW`, then select the lowest rank within that outcome |
| v0.1-to-v0.2 target widening/narrowing is hidden behind shared resource policies | sections 7.5.1 and 25 expose every row and require separate directional approval |
| Evidence attachment changes from contextual scopes to a record/artifact target axis that cannot be honestly labeled as a directional set delta | sections 7.5.1 and 25 classify it separately as `RETYPED` and prohibit inferred cross-axis equivalence |
| Filing evidence could require a prior approval/attestation action that cannot target `SUBMISSION_ASSEMBLY` | sections 7.5.1, 7.7, 7.8, 24, and 25 require the binding review to reject or amend an unsatisfiable filing rule before promotion |
| Interactive approval appears to require a long-open transaction | sections 7.4, 18.2, 24, and 25 stop machine materialization on the separately governed transaction protocol in `samovers/OFARM#19` |
| Preflight-only and distinct-approver semantics appear production-reachable although no current row selects them | sections 6.4, 7.2, 20, and 22.1 mark them reserved future semantics |

This table does not authorize an OFARM2 fix. OFARM2 must wait for accepted semantics, promoted contracts, and byte-identical extraction.

---

## 24. Staged delivery and currentness

The required sequence is:

1. **Phase A candidate:** this document only; no authority or currentness effect.
2. **Semantic-profile approval:** stewards approve or amend the closed rule fields, concrete kinds, one-target resource policies, prospective effects, lifecycle semantics, and approval card in section 25; no RFC is accepted yet.
3. **Adjacent contract prerequisites:** separate PRs provide every content-addressed protected-effect contract required by a state-affecting rule (`samovers/OFARM#12`), including the final `ReviewDecision` contract (`samovers/OFARM#15`), any missing Event Grammar classification, the CP2 authorization-result surface/registered public reason codes, and the evidence-retention proof postures referenced by display/read evidence (`samovers/OFARM#14`). The governed interactive-approval transaction and consumption protocol must be closed separately under `samovers/OFARM#19` before an approval machine profile or runtime implementation can claim `TRANSACTION_BOUND_V0_2`. Domain mappings, public-surface contract changes, transaction coordination, retention, encryption, and key custody do not ride in an authorization-law PR. Transport-release semantics remain a separate downstream boundary (`samovers/OFARM#13`).
4. **Policy-bundle draft:** a separate non-default authorization-law PR materializes `AuthorizationPolicyBundle v0.2`, every effect-intent schema, bindings to already reviewed protected-effect contracts, both declarative projections, evidence bindings, trusted approval-cutoff mappings, and the immutable manifest with real content-addressed refs/digests. Before that manifest can pass review, stewards must verify that `EP_FORMAL_FILING_V0_2` does not require prior approval or attestation that is impossible for `SUBMISSION_ASSEMBLY` under `RP_ASSEMBLY_ONE`; any such contradiction requires a semantic row or evidence-policy amendment before promotion rather than an unsatisfiable filing rule.
5. **Source-bundle draft:** a separate authorization-source PR materializes only the closed, one-record immutable `AuthorityGrant`, `DelegationGrant`, and `SharingGrant` v0.2 contracts with issuance-policy and per-action rule bindings. `RevocationDecision v0.1` remains unchanged and its fixed `TERMINATE` lookup targets the exact source family/ID.
6. **Decision-evidence drafts:** separate bounded PRs materialize `AuthorizationDecisionEvidence v0.2` and `AuthorizationFinalizationEvidence v0.2`. They add tagged audit profiles, examples, and validation without inventing new domain event families or changing currentness.
7. **Binding review and accepted law:** stewards review the exact schema/manifest bytes; a later governed PR promotes the approved RFC and exact matrix while pinning those digests. Any semantic change returns to step 2.
8. **Hostile conformance:** a separate PR adds the production-reachable cases in section 22 and publishes the result.
9. **Explicit promotion:** after hostile review and steward approval, a separate PR changes current/default indexes and generated navigation.
10. **OFARM2 extraction:** promoted canonical assets are copied byte-for-byte and verified by digest.
11. **OFARM2 runtime work:** only then may `OFARM2#359` resume. Authority evaluation, protected-effect validation, buffered disclosure, filing-outbox commitment, and transport-release enforcement remain separately reviewable runtime trust boundaries rather than one catch-all implementation PR. No dispatcher may infer release eligibility from an authorization decision or outbox row.

No step is implied by completion of the prior step. Each PR retains one primary trust boundary and names any dependency on the prior step. CP15 human governance applies to current/default promotion.

---

## 25. Steward approval card

Before accepted-law work begins, stewards should record explicit decisions for all items:

| Decision | Proposed answer | Approval required |
|---|---|---|
| Are principal resolution, CP3 posture, and human finalization separate axes while AI disclosure stays non-authoritative? | yes | yes |
| Does the authorization RFC preserve all five accepted CP3 posture values without editing CP3 semantics? | yes | yes |
| Are `AGENT_ALLOWED_WITH_PREFLIGHT_ONLY`, `PROHIBITED_FOR_AGENT`, and `DISTINCT_APPROVER_REQUIRED` preserved but reserved until a future action rule explicitly selects them? | yes; they are not current production-reachable semantics | yes |
| Must organization representation record the natural-person principal, represented Party, and immutable representation basis separately? | yes | yes |
| Is every software-agent authority subject derived per candidate path from a closed immutable direct-grant, representation, or delegation basis, never from sponsor identity? | yes | yes |
| Are action stage and authority family policy-derived rather than caller-selected? | yes | yes |
| Is the exact matrix in section 7 the v0.2 closure, including delegation, CP3 posture, resources, subjects, and existence postures? | yes | yes, row-by-row amendments allowed |
| Are the `WIDENING` target rows in section 7.5.1 accepted exactly as itemized? | yes | yes, each listed row |
| Are the `NARROWING` target rows in section 7.5.1 accepted exactly as itemized? | yes | yes, each listed row |
| Are the `MIXED_DELTA` target rows and their named mappings in section 7.5.1 accepted exactly as itemized? | yes | yes, each listed row and mapping |
| Is the `RETYPED` evidence-attachment target axis in section 7.5.1 accepted without inferring cross-axis widening or narrowing? | yes | yes |
| Is the `CLOSED_EQUIVALENT` filing target mapping in section 7.5.1 accepted? | yes | yes |
| Must the immutable action rule select every policy-derived field in section 7.4? | yes | yes |
| Must each rule select an exact effect-intent schema ref/version/digest from a reviewed binding manifest rather than accept a caller-selected schema? | yes | yes |
| Must every state-affecting rule bind an exact separately owned protected-effect contract ref/digest before it becomes executable? | yes; domain mappings remain outside authorization | yes |
| Is the validated effect intent the sole caller-authored source for resources, subject, scope, time, purpose, destination, grantee, rights, and payload facts? | yes; mirrored fields are schema-invalid | yes |
| Must each rule select a content-addressed declarative extractor and relevant-state projection with exact JSON Pointers? | yes | yes |
| Must actual schema bytes and their binding manifest exist and be reviewed before accepted-RFC/action-matrix promotion? | yes | yes |
| Does every current action have exactly one concrete `AUTHORITY_TARGET`, with no executable broad buckets? | yes | yes |
| Do all final review actions retain one exact `ACCEPTED_EVENT_CONSEQUENCE` revision when chosen, while `REVIEW_REQUEST` and unrelated actions remain unchanged? | yes | yes |
| Do only `REVIEW_ACCEPT` and `REVIEW_REJECT_OR_CONTEST` select `RP_FINAL_REVIEW_CASE_ELIGIBLE_TARGET_ONE`, including one exact `EVIDENCE_SUFFICIENCY_CASE` revision when chosen, while `REVIEW_SUPERSEDE` retains its narrower policy? | yes | yes |
| Does each final-review intent bind the exact outcome posture—`ACCEPTED`, `SUPERSEDED`, or one of `REJECTED`/`CONTESTED`—without a mirrored selector or authorization-owned result mapping? | yes | yes |
| Are pack registry/release/current-state roles applicability, integrity, or state inputs rather than extra authority targets? | yes; no grant union across them | yes |
| Are assembly alternatives exact `ONE_OF` authority-target branches? | yes | yes |
| Is `OUTPUT_FILE_SUBMISSION_ASSEMBLY` fixed to `ATTEST_SIGN`? | yes | yes |
| Is the authenticated human's immutable filing-outbox commit the final authority-bearing act? | yes | yes |
| Must policy-bundle review reject or amend `EP_FORMAL_FILING_V0_2` if it requires prior approval/attestation that `RP_ASSEMBLY_ONE` cannot perform for `SUBMISSION_ASSEMBLY`? | yes; no unsatisfiable filing rule may be promoted | yes |
| Does that completed filing act remain distinct from current permission to release protected bytes? | yes; every release attempt needs the separate transport-release gate unless an explicit regime policy made delivery irrevocable | yes |
| Is transport forbidden from changing bytes/destination/idempotency after release eligibility passes? | yes | yes |
| Would an authority-bearing receipt/transmission regime require a separate action class? | yes | yes |
| Does `SHARE_REVOKE_ACCESS` create a prospective `RevocationDecision` and leave the SharingGrant immutable? | yes; `TERMINATE` only in this row | yes |
| Do pack activate/deactivate create prospective StructureEvents and immutable successor state? | yes | yes |
| Are no existing actions granted lineage inheritance? | yes | yes |
| Is current authority always checked at trusted evaluation/effect time, while claim/report rows authorize the current reporter and keep alleged performer/historical execution authority separate? | yes; no current row reuses the reporter path at subject time | yes |
| Must every decision and human approval bind the exact JCS/SHA-256 effect-intent digest? | yes | yes |
| Do all current rows use `TRANSACTION_BOUND_V0_2`, bounded by the trusted effect transaction and relevant cutoffs rather than an invented universal duration? | yes | yes |
| Must `samovers/OFARM#19` close the interactive approval reservation/finalization, concurrency, retry, and recovery protocol before machine materialization, without assuming a transaction stays open during human think time? | yes | yes |
| Are all v0.2 decisions single-use with no reserved replay mode? | yes | yes |
| Must internal effects and authorization evidence commit in one atomic protected-effect transaction? | yes | yes |
| Must the proposed domain result pass the rule-bound protected-effect contract before that transaction commits, with intent/result/contract digests in the receipt? | yes | yes |
| Is authorization `ALLOW` only the authority-gate result, never a bypass for another EnforcementChain gate? | yes | yes |
| Do Event Grammar/protected-effect contracts, not authorization audit records, determine domain event family and commit class? | yes | yes |
| Are governed authorization bundles append-only `EvidenceEvent`/`evidence record` artifacts with no domain-current-state eligibility? | yes | yes |
| Does actual `RECEIVE_READ_DATA` use `AGENT_ALLOWED_WITH_POLICY_CHECK` plus mandatory CP2 qualification, while preflight-only never discloses protected bytes? | yes | yes |
| Must every returned row, field, aggregate, count, metadata item, and lineage item have authority/redaction coverage under one snapshot? | yes | yes |
| Is protected streaming outside v0.2, leaving a later Platform runtime RFC to define it? | yes | yes |
| Is the full trace internal, with safe caller results and separate authorized/redacted `AUTHORIZATION_TRACE` retrieval? | yes | yes |
| Must caller-facing non-`ALLOW` responses reuse CP2 qualification and registered RuntimeProblem categories while still hiding sensitive basis details? | yes; denial/review/human-action/invalid/redacted posture cannot be hidden | yes |
| Are approval challenge and approval profiles required for fresh approval, with relevant-state digest equality and atomic single-use consumption? | yes | yes |
| Must every approver independently satisfy a natural-person path for the same action and effect, never sponsorship alone? | yes | yes |
| May a direct natural person satisfy `FA` only through that lifecycle under `SAME_PRINCIPAL_ALLOWED`, while a future `DISTINCT_APPROVER_REQUIRED` rule would need another eligible principal? | yes | yes |
| Are challenge/approval lifetimes bounded exactly by the trusted interactive session, relevant state cutoffs, and final protected-effect transaction rather than one global duration? | yes | yes |
| Must approval evidence retain the exact content-addressed human-visible bytes plus renderer, display-policy, media, locale, and timezone metadata? | yes | yes |
| Must read receipts distinguish retained/reconstructible payload bytes from digest-only evidence, without defining retention encryption or key custody here? | yes | yes |
| Are purpose tokens exact-match and optional only when the source is unrestricted? | yes | yes |
| Must legacy free-text purpose be explicitly migrated? | yes | yes |
| Are free-text conditions unsupported and fail-closed? | yes | yes |
| Must a v0.1 source remain under v0.1 or be explicitly migrated, with `SOURCE_RULE_BINDING_MISMATCH` rather than an unreachable legacy-review reason if it is offered to v0.2? | yes | yes |
| Must action-rule and all applicable source evidence requirements be cumulative and name immutable active policy revisions? | yes | yes |
| Must every v0.2 source bind issuance-policy identity and the exact selected-rule ID/digest for every granted action? | yes | yes |
| Must `ruleDigest` cover the complete resolved per-action semantic closure, including shared eligibility semantics but excluding unrelated actions and diagnostic-only behavior? | yes | yes |
| Is automatic cross-digest reuse prohibited in v0.2, requiring a new source ID, explicit migration, or governed reapproval? | yes; no generic subset theorem engine | yes |
| Is every v0.2 grant/delegation/sharing ID a one-record immutable identity so RevocationDecision v0.1 `TERMINATE` targets exactly that ID? | yes; any change receives a new ID | yes |
| Are role-targeted source paths capped by role anchor scopes? | yes | yes |
| Are delegation ceilings and source permissions closed tokens whose intersection controls every delegated path? | yes | yes |
| Is default delegation depth one hop? | yes | yes |
| Are v0.1 narrowing revocations non-`ALLOW` until separately closed? | yes | yes |
| Is SharingGrant an exact-artifact access basis only for `RECEIVE_READ_DATA`? | yes | yes |
| Must authority-target, other typed inputs, effect-subject, scope, evidence, and sovereignty proof use separate typed fields? | yes | yes |
| Must every result bind retrievable immutable policy bytes and an authority-evaluation snapshot? | yes | yes |
| Is the total path aggregation lattice and numeric reason table in sections 15 and 20 accepted? | yes | yes |
| Is `HUMAN_FINAL_ACTION_REQUIRED` the only primary reason for `REQUIRE_HUMAN_APPROVAL`, with approval-lifecycle codes diagnostic only? | yes | yes |
| Do simultaneous authorization-global failures choose `DENY` before `REQUIRE_REVIEW`, then the lowest rank within that outcome, without evaluating dependent facts from unavailable prerequisites? | yes | yes |
| Are malformed/base-schema/intent-schema failures ingress rejections outside the authorization outcome lattice? | yes | yes |
| Is the decision-bundle digest exactly the JCS/SHA-256 projection in section 18.8, excluding only the two enumerated JSON Pointers? | yes | yes |
| Must non-`ALLOW` bundles commit before transport errors are returned? | yes | yes |
| Does honest v0.2 use the four bounded schema packages in section 17.2 rather than proliferate independent top-level families? | yes | yes |
| Does current/default promotion remain a separate final step? | yes | yes |

Any amendment must state whether it changes only this authorization boundary. A requested authentication, principal-resolution, key-custody, database, or runtime-integration change must be split.

---

## 26. Completion criteria for Phase A

Phase A is complete when:

- this candidate is reviewed against issue `samovers/OFARM#10`;
- every acceptance criterion has a proposed disposition;
- the one-record immutable source-ID decision, issuance-policy binding, complete per-action semantic-closure digest, exact-digest compatibility law, and exact v0.1 `TERMINATE` lookup are explicit;
- the CP3 compatibility mapping is accepted without changing CP3 semantics, or a separate stacked change is named;
- the actual-read mapping to policy check, mandatory CP2 qualification, and retained-versus-digest-only payload evidence is explicitly accepted;
- the action matrix, the row-by-row v0.1-to-v0.2 target-delta ledger, complete rule fields, rule-selected intent/extractor profiles, protected-effect contract bindings, binding-manifest prerequisite, one-target resource roles, final-review accepted-consequence target, accept/reject-only evidence-sufficiency-case target, exact outcome posture, and prospective subject closure are reviewed;
- transaction-bound validity, single-use consumption, atomic-write, protected-effect validation, buffered-read coverage, filing-outbox finality, separate transport-release eligibility, aggregation, and accurately bounded reconstruction claims are reviewed, while the interactive reservation/finalization protocol remains stopped on `samovers/OFARM#19`;
- the path-specific software-agent authority-subject bases are accepted without sponsor inference;
- the human challenge/approval, retained exact display representation, independent approver path, relevant-state equality, current same-principal separation policy, expiry, and atomic-consumption invariants are reviewed, while distinct-approver semantics remain reserved;
- authorization `ALLOW` is confirmed as only the authority gate, and Event Grammar/Platform/runtime dependencies are explicitly stacked rather than absorbed;
- ingress rejection is kept outside the authorization outcome lattice and the exact digest projection is reviewed;
- migration and currentness rules are accepted or amended, with v0.1 sources kept outside the v0.2 path lattice until explicit migration;
- hostile cases are judged sufficient to detect silent rule-upgrade widening, source-ID mutation, wrong-source revocation, reporter/performer conflation, intent/result widening, weaker-schema/extractor substitution, mirrored facts, resource-role union, prospective-effect mutation, read/trace leakage, overclaimed reconstruction, post-commit release after disclosure revocation, CP2 over-redaction, approval rollover/replay, ambiguous agent authority, malformed input, nested digest-field injection, and other fail-open behavior;
- the trust boundary remains authorization law and machine-contract governance; and
- no active authority or schema was changed by the candidate PR.

What is next: steward review and explicit semantic approval before any accepted-RFC or machine-contract edit.
