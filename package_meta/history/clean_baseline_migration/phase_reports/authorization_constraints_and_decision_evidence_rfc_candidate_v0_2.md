# OFARM Executable Authorization Constraints and Decision Evidence RFC v0.2

Date: 2026-08-31
Status: Phase A RFC candidate for issue `samovers/OFARM#10`; non-authoritative, not accepted law, and not a current/default machine contract
Depends on: review of `samovers/OFARM2#353` and draft `samovers/OFARM2#359`
Scope: define reviewable authorization semantics and the exact versioned contract delta needed before an implementation can claim a durable, fail-closed authorization decision

---

## 1. Decision requested

This candidate asks OFARM stewards to approve, reject, or amend one bounded design:

1. authorization-relevant actor posture comes from a trusted principal and actorship boundary, not from optional AI-assistance metadata;
2. the action class selects its authority family, stage, inheritance ceiling, target-kind policy, delegation posture, and human-finalization posture from one versioned policy rule;
3. purpose is a closed, exact-match use constraint in v0.2, not a comparison between unrelated free-text fields;
4. untyped or unsupported conditions never evaluate to true;
5. required evidence is usable only under an active evidence-eligibility policy;
6. target proof, scope proof, role scope, grant scope, delegation source, sharing basis, and revocation posture are independently evaluated and durably recorded;
7. the request, result, and trace form one persisted decision bundle whose policy identity and proof basis can be reconstructed; and
8. current v0.1 records remain historical v0.1 records and are not silently treated as v0.2 proof.

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
- action-matrix version: yes, from v0.1 to a proposed v0.2;
- authority-source contract versions: yes, where closed constraints cannot be represented in v0.1;
- authorization-decision contract versions: yes;
- hostile conformance: yes; and
- current/default promotion: separate, explicit, human-governed step only.

---

## 4. Problem statement

The active v0.1 model correctly says that authorization depends on action class, accountable actor, target, scope, time, role, grant, delegation, sharing, revocation, inheritance, and human accountability. It does not yet close several comparisons tightly enough for independent runtimes to reach the same safe result.

The machine contracts expose the gap:

- `AuthorityGrant`, `DelegationGrant`, and `SharingGrant` carry free-text `purpose` and `conditions`;
- `AuthorizationDecisionRequest` carries a separate caller-provided `usePurpose`;
- `requiredAuthorityFamily`, `actionStage`, `nonHumanActor`, and `revocationCheckRequired` are caller fields even though they are policy conclusions or mandatory checks;
- optional `aiAssistance` can be omitted and cannot prove human authorship or human final action;
- `AuthorizationDecisionTrace` cannot identify the exact policy version and digest used;
- the trace cannot record trusted actor posture, full target identity, generic target proof, generic scope proof, or constraint evidence;
- `dataSovereigntyBoundaryRefs` is specific to actual `DataSovereigntyBoundary` records and cannot truthfully hold arbitrary proof references;
- a role-targeted grant can appear to escape the referenced `RoleAssignment.anchorScopes` if only the grant scope is checked;
- current narrowing revocations name modes but do not carry enough closed operands to evaluate every narrowing deterministically; and
- v0.1 does not define whether partial constraints from different grant paths may be unioned.

Without closure, one runtime can silently normalize a purpose, another can ignore it, a third can treat free-text conditions as descriptive, and all three can claim conformance. That is an authorization trust failure, not merely an interoperability inconvenience.

---

## 5. Core safety stance

### 5.1 `ALLOW` is a complete-proof claim

`ALLOW` means one permitted authorization path has independently satisfied every applicable constraint under one identified policy bundle.

Absence of a prohibition is not proof of authority.

### 5.2 Caller assertions do not create policy facts

A caller may request an action, name a target, disclose a purpose, and provide candidate references. The caller may not choose:

- the required authority family;
- the action stage;
- whether revocation is checked;
- whether the actor is human or software;
- the actor's accountable sponsor;
- the target's governed kind;
- the scope relationship;
- the policy version; or
- whether evidence is current and eligible.

Those facts come from trusted resolution or from the selected policy bundle.

### 5.3 Unknown does not become false, and false does not become true

Missing AI disclosure does not prove that no AI participated. Missing condition semantics does not mean the condition passed. Missing proof does not mean the relationship is obvious. An unknown or unsupported authority-relevant fact produces a non-`ALLOW` outcome.

### 5.4 Partial paths are not unioned

An evaluator must not combine the action coverage of one grant, the purpose coverage of a second grant, and the evidence coverage of a third grant to manufacture a complete path. Each selected direct or delegated authorization path must be sufficient by itself, except for the explicit `RECEIVE_READ_DATA` sharing composition defined in section 13.

---

## 6. Trusted actor posture

### 6.1 Actor posture values

The proposed v0.2 decision policy derives exactly one actor posture:

- `HUMAN_ACCOUNTABLE_PARTY`
- `SPONSOR_BOUND_SOFTWARE_AGENT`
- `UNRESOLVED_ACTOR_POSTURE`

`HUMAN_ACCOUNTABLE_PARTY` requires a trusted principal-resolution result that binds the authenticated session to a Party that can be accountable for the action. An organization, public body, or other non-natural Party does not become a human actor merely because its Party reference is present; human-final actions require a trusted natural-person accountability binding acting for that Party.

`SPONSOR_BOUND_SOFTWARE_AGENT` requires the active CP3 actorship envelope and a valid sponsor binding. A model name, tool name, process name, API key label, session identifier, or caller boolean is not an authority-bearing actor.

`UNRESOLVED_ACTOR_POSTURE` is always non-`ALLOW`.

### 6.2 AI-assistance disclosure

AI-assistance metadata is provenance only. It has exactly these decision-trace dispositions:

- `DISCLOSED_ASSISTED`
- `DISCLOSED_NOT_ASSISTED`
- `NOT_DISCLOSED_OR_UNKNOWN`

Changing, omitting, or retrying optional AI-assistance metadata must not:

- change the trusted actor posture;
- add an authority basis;
- remove a human-finalization requirement; or
- turn a non-`ALLOW` result into `ALLOW`.

### 6.3 Human final action

For a rule marked `HUMAN_FINAL_ACTION_REQUIRED`, software may prepare or recommend within its separately authorized posture, but the governed final action requires a fresh human act bound to:

- the action class;
- the full target;
- the target time or decision freshness window;
- the policy digest;
- the material decision inputs; and
- the accountable Party.

Reusing approval for a materially different target, policy digest, or decision input is not a fresh human final action.

For a rule marked `DIRECT_SOFTWARE_ACTION_PROHIBITED`, a software agent cannot be the direct actor even if a sponsor exists. It may only perform separately authorized preparatory activity.

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

Actor codes are `S` = `SPONSOR_BOUND_ALLOWED`, `H` = `HUMAN_FINAL_ACTION_REQUIRED`, and `P` = `DIRECT_SOFTWARE_ACTION_PROHIBITED`.

Target-kind codes are `CT` = `CANONICAL_TRUTH`, `PV` = `PASSPORT_VIEW`, `DA` = `DOCUMENT_ASSEMBLY`, `DO` = `DOSSIER_ASSEMBLY`, `SA` = `SUBMISSION_ASSEMBLY`, `QE` = `QUERY_EXECUTION`, `CM` = `CURRENT_STATE_MATERIALIZATION`, and `PA` = `PACK_ACTIVATION`.

| Action class | Authority family | Derived stage | Inheritance ceiling | Delegation default | Actor posture | Allowed target kinds |
|---|---|---|---|---|---|---|
| `OBSERVE_CREATE_OBSERVATION` | `OBSERVE_REPORT` | `DRAFT_PREPARATION` | D | allowed | S | CT |
| `OBSERVE_ATTACH_EVIDENCE` | `OBSERVE_REPORT` | `DRAFT_PREPARATION` | D | allowed | S | CT, DA, DO, SA |
| `ASSERT_STRUCTURE` | `ASSERT_SUBMIT` | `DRAFT_PREPARATION` | X | explicit/cautious | H | CT |
| `ASSERT_OPERATION_CLAIM` | `ASSERT_SUBMIT` | `DRAFT_PREPARATION` | D | allowed | S | CT |
| `ASSERT_COMPLIANCE` | `ASSERT_SUBMIT` | `DRAFT_PREPARATION` | X | explicit/cautious | H | CT, PV, DO, SA |
| `OPERATE_PLAN_INTERVENTION` | `OPERATE_INTERVENE` | `DRAFT_PREPARATION` | D | allowed | S | CT |
| `OPERATE_REPORT_EXECUTION` | `OPERATE_INTERVENE` | `DRAFT_PREPARATION` | D | allowed | S | CT |
| `REVIEW_REQUEST` | `REVIEW` | `DRAFT_PREPARATION` | X | allowed | S | CT, PV, DA, DO, SA, CM |
| `REVIEW_ACCEPT` | `GOVERN_DECIDE` | `PROMOTION` | N | prohibited by default | P | CT |
| `REVIEW_REJECT_OR_CONTEST` | `GOVERN_DECIDE` | `PROMOTION` | N | prohibited by default | P | CT |
| `REVIEW_SUPERSEDE` | `GOVERN_DECIDE` | `PROMOTION` | N | prohibited by default | P | CT |
| `CONTEXT_INSTALL_PACK` | `CONTEXT_GOVERNANCE` | `CONTEXT_ACTIVATION` | N | prohibited by default | P | PA |
| `CONTEXT_ACTIVATE_PACK` | `CONTEXT_GOVERNANCE` | `CONTEXT_ACTIVATION` | N | prohibited by default | P | PA |
| `CONTEXT_DEACTIVATE_PACK` | `CONTEXT_GOVERNANCE` | `CONTEXT_ACTIVATION` | N | prohibited by default | P | PA |
| `OUTPUT_APPROVE_DOCUMENT_ASSEMBLY` | `ATTEST_SIGN` | `PUBLICATION` | N | prohibited by default | P | DA, DO |
| `OUTPUT_ATTEST_DOCUMENT_ASSEMBLY` | `ATTEST_SIGN` | `ATTESTATION` | N | prohibited by default | P | DA, DO |
| `OUTPUT_FILE_SUBMISSION_ASSEMBLY` | `ATTEST_SIGN` | `PUBLICATION` | N | explicit only | H | SA |
| `SHARE_GRANT_ACCESS` | `SHARE_REVOKE` | `PROMOTION` | X | allowed | H | CT, PV, DA, DO, SA, QE, CM |
| `SHARE_REVOKE_ACCESS` | `SHARE_REVOKE` | `PROMOTION` | X | allowed | H | CT, PV, DA, DO, SA, QE, CM |
| `RECEIVE_READ_DATA` | `RECEIVE_USE` | `QUERY_READ` | D | allowed | S | CT, PV, DA, DO, SA, QE, CM |

### 7.3 Matrix rules

The inheritance entry is a ceiling, not a grant. A source record may narrow `D` to `X` or `N`, and may narrow `X` to `N`. It may not broaden the row. A row marked `N` must use `NO_INHERIT`.

`OUTPUT_FILE_SUBMISSION_ASSEMBLY` resolves the v0.1 alternative family to `ATTEST_SIGN` for v0.2. A deployment that needs a distinct non-attesting transmission action must propose a separate action class rather than reinterpret this one locally.

Unknown action classes, target kinds, stages, or policy rules are non-`ALLOW`.

The target-kind list is a proposed closure point and requires specific steward approval. It must not be inferred from the word "typical" in the v0.1 matrix.

---

## 8. Full governed target and proof separation

### 8.1 Required target identity

A v0.2 request and trace must carry:

- `targetKind`;
- `targetRef`;
- `scopeType`;
- `scopeRef`;
- `targetTime`; and
- `twin` when the target family can exist in Compliance or Advisory posture.

Where a field does not apply, the schema must use an explicit governed representation. A runtime must not omit an applicable field and rely on an implementation default.

### 8.2 Target proof

`targetProofRefs` prove that the named target:

- exists;
- is the stated target kind;
- is current or valid at the target time where required;
- belongs to the stated twin where relevant; and
- is bound to the stated scope.

A target reference string by itself is not target proof.

### 8.3 Scope proof

`scopeProofRefs` prove the relationship between the requested target scope and each authority source scope. They may refer to governed identity, containment, tenancy, or lineage records that actually establish the claimed relationship.

Target proof and scope proof are not interchangeable. One artifact may appear in both arrays only when it independently carries both facts, and each use must be recorded with its disposition.

### 8.4 Sovereignty proof

`dataSovereigntyBoundaryRefs` may contain only identifiers of actual `DataSovereigntyBoundary` records. Generic target, scope, tenant, role, policy, or constraint evidence must use its dedicated field.

### 8.5 Tenant isolation

Every source, proof, policy, and evidence record used by a path must resolve within the authorized deployment or tenant boundary. Cross-tenant equality of an opaque identifier does not establish authority. A cross-tenant reference without an accepted sharing and sovereignty path is non-`ALLOW`.

---

## 9. Role and grant semantics

### 9.1 Party-targeted AuthorityGrant

A Party-targeted `AuthorityGrant` path is eligible only when:

- the grant is active at `targetTime`;
- the target Party is the trusted acting Party;
- the action class is present;
- the derived authority family is present;
- the target and scope satisfy the grant's closed constraints;
- inheritance does not exceed the matrix ceiling;
- purpose, condition, and evidence rules pass;
- no active revocation defeats the path; and
- the actor posture and human-finalization rule pass.

### 9.2 Role-targeted AuthorityGrant

A grant whose target kind is `ROLE_ASSIGNMENT` is eligible only when the referenced `RoleAssignment`:

- exists and is valid at `targetTime`;
- names the trusted acting Party;
- is valid in the same tenant boundary; and
- has at least one `anchorScopes` entry that independently covers the requested target under the same exact scope-proof rules.

The effective scope is the intersection of the action-matrix ceiling, the grant scope, and the matching role anchor scope. The grant cannot widen the role assignment, and the role assignment cannot widen the grant.

### 9.3 Grant candidates are hints

Candidate IDs supplied by a caller are retrieval hints only. The evaluator must resolve the complete eligible set or use a trusted, completeness-proven index. Absence from a caller candidate list cannot hide a revocation or force selection of a weaker path.

---

## 10. Delegation semantics

A `DelegationGrant` is not origin authority. A delegated path is eligible only when:

1. the delegation itself satisfies actor, action, family, scope, time, purpose, condition, evidence, state, and revocation checks;
2. the delegator held a live, independently sufficient source authority at `targetTime`;
3. the source authority permitted delegation for this action;
4. the delegation does not broaden action, family, target, scope, inheritance, time, purpose, evidence, or actor posture;
5. every `sourceAuthorityGrantRef` resolves and is recorded; and
6. any role-targeted source grant is capped by its referenced `RoleAssignment.anchorScopes` exactly as described in section 9.2.

The effective delegated permission is the intersection of every link in the path. A missing or unresolved source link is non-`ALLOW`.

The evaluator must reject cycles. The v0.2 default maximum delegation depth is one hop unless a later accepted policy introduces an explicit bounded chain contract and conformance suite.

---

## 11. Purpose semantics

### 11.1 Proposed v0.2 representation

Executable v0.2 sources use optional `permittedUsePurposes`, a non-empty unique array of closed purpose tokens. A v0.2 request uses optional scalar `requestedUsePurpose`.

Purpose tokens must match `^[A-Z][A-Z0-9_]{0,127}$`.

If a source has `permittedUsePurposes`:

- the request must contain `requestedUsePurpose`;
- the scalar must equal one member exactly;
- the purpose is evaluated for the same action and full target as the request; and
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
- target kind and optional target reference narrowing;
- scope and inheritance;
- valid time;
- grant/delegation/sharing state;
- delegability and delegation depth;
- closed purpose tokens;
- required evidence under a named policy;
- revocation; and
- actor and human-finalization posture.

Unknown fields are schema-invalid. A future typed constraint needs its own accepted semantics, versioned contract, and hostile conformance.

### 12.2 Legacy conditions

A non-empty v0.1 `conditions` array is unevaluable under v0.2. The evaluator must return a non-`ALLOW` outcome with `UNSUPPORTED_LEGACY_CONDITION`; it must not guess that prose is true.

Migration requires a steward to map the intended restriction into an already supported closed field or into a separately accepted typed condition profile. Removing the prose without preserving its restriction is forbidden widening.

### 12.3 Required evidence representation

Where required evidence is supported, v0.2 uses both:

- `requiredEvidenceRefs`; and
- `requiredEvidencePolicyRef`.

If either is present, both are required. The policy reference must resolve to an active/current evidence-eligibility policy that defines the eligible evidence family, usable state, freshness, dispute/supersession behavior, target binding, scope binding, tenant rule, and use-purpose rule.

Until such a policy is active for the named evidence family, the requirement is `UNSUPPORTED_EVIDENCE_POLICY` and cannot support `ALLOW`.

### 12.4 Evidence evaluation

Every required evidence reference must:

- resolve;
- be the family required by the policy;
- be valid and usable at `targetTime`;
- not be stale beyond policy;
- not be disputed, invalid, withdrawn, or superseded when the policy excludes that state;
- belong to the permitted tenant and sovereignty boundary;
- bind to the requested target and scope; and
- be eligible for `requestedUsePurpose` when purpose is constrained.

Missing, wrong-kind, stale, disputed, superseded, cross-tenant, unavailable, or otherwise ineligible evidence produces non-`ALLOW` and an individual evidence disposition in the trace.

Opaque existence of a referenced record is not evidence eligibility.

---

## 13. Sharing and `RECEIVE_READ_DATA`

`SharingGrant` is an access right, not assertion, review, governance, signing, or mutation authority.

For `RECEIVE_READ_DATA`, the evaluator performs one final decision with two layers:

1. an access basis: a sufficient `RECEIVE_USE` AuthorityGrant/DelegationGrant path or a sufficient SharingGrant for the exact grantee and artifact; and
2. a resource-control layer: target proof, scope proof, tenant and sovereignty policy, purpose, conditions, evidence where required, state, time, and revocation.

A SharingGrant path is eligible only when:

- `granteePartyRef` is the trusted acting Party;
- `sharedArtifactFamily` maps to the requested `targetKind`;
- `sharedArtifactRef` exactly equals `targetRef`;
- the requested scope is covered;
- the grant is active at `targetTime`;
- its purpose and conditions are evaluable and pass;
- all actual sovereignty boundaries pass; and
- no active revocation defeats the sharing right.

A SharingGrant cannot authorize any action other than `RECEIVE_READ_DATA`. It cannot be cited as write, review, govern, context, sharing-administration, or signing authority.

A runtime must not evaluate a direct receive/use grant and a SharingGrant in separate endpoints that can return contradictory final answers. Their applicable bases and constraints are composed into one policy decision and one trace.

---

## 14. Revocation semantics

Revocation lookup is mandatory for every source path. A caller cannot disable it.

### 14.1 `TERMINATE`

An effective `TERMINATE` decision for a source record makes that source path ineligible from `effectiveFrom` onward. It does not erase historical decisions made before the effective time.

### 14.2 Narrowing modes

The current v0.1 `NARROW_SCOPE`, `NARROW_ACTIONS`, and `NARROW_TIME` forms do not close all operands and merge behavior needed for deterministic evaluation.

Until a separately reviewed version closes those operands, an active narrowing decision affecting a candidate source produces `UNSUPPORTED_REVOCATION_NARROWING` and a non-`ALLOW` outcome for that path. A runtime must not ignore it, treat it as termination without saying so, or infer replacement semantics from notes.

This is bounded design debt, not a claim that narrowing is unsupported forever.

### 14.3 Revocation candidates

Revocations must be found from a trusted complete index keyed by affected artifact family/reference and target time. Caller-supplied candidate lists are never the completeness boundary.

---

## 15. Deterministic evaluation

### 15.1 Evaluation order

The proposed evaluator order is:

1. validate request schema;
2. load and verify the immutable policy bundle;
3. select the exact action rule;
4. resolve trusted actor posture;
5. resolve and prove full target identity;
6. prove tenant and scope relationships;
7. resolve role and direct-grant paths;
8. evaluate action, family, target, scope, inheritance, time, state, purpose, conditions, and evidence;
9. resolve and evaluate delegated source paths;
10. compose any applicable `RECEIVE_READ_DATA` sharing path;
11. apply all effective revocations;
12. apply actor and human-finalization posture;
13. select a complete eligible path deterministically;
14. build request, result, and trace records;
15. persist the complete decision bundle; and
16. only after commit, allow the protected effect or return the typed non-`ALLOW` response.

No later step may repair missing proof from an earlier step by trusting a caller assertion.

### 15.2 Path selection

Outcome is computed over all completely evaluated paths, not over the first database row returned.

If one or more paths fully allow, the selected path is the lowest canonical tuple:

1. path type order: direct Party grant, role-targeted grant, delegated grant, SharingGrant access path;
2. source identifier in code-point order; and
3. delegation/source identifiers in code-point order.

All other evaluated paths remain summarized in the trace. Selection order changes which sufficient basis is cited, not whether incomplete authority becomes complete.

### 15.3 Outcome semantics

The v0.2 outcomes remain:

- `ALLOW`: at least one complete path passes and the required final actor posture is satisfied;
- `REQUIRE_HUMAN_APPROVAL`: the authority path passes but a fresh human final action is still required;
- `REQUIRE_REVIEW`: a potentially relevant path contains a governed unsupported or ambiguous constraint, such as legacy condition text or narrowing revocation semantics; and
- `DENY`: no path exists, or every path fails a closed constraint.

Explicit denial, active termination, expired authority, actor mismatch, action mismatch, family mismatch, target mismatch, scope mismatch, purpose mismatch, evidence failure, and tenant escape are `DENY` reasons. Unsupported semantics are `REQUIRE_REVIEW` unless a stronger active policy requires denial.

Problems are sorted by severity, reason code, and related reference. The primary `reasonCode` is the first item after that stable sort. Implementations must not select a friendlier reason based on caller retry shape.

---

## 16. Policy identity

Every v0.2 result and trace must identify:

- `policyId`;
- `policyVersion`;
- `policyDigest` in `sha256:<64 lowercase hexadecimal characters>` form; and
- `selectedRuleId`.

The digest covers the exact immutable representation used by the evaluator, including the action matrix and referenced decision rules after deterministic packaging. A mutable URL, branch name, deployment label, or semantic version alone is not enough.

If the loaded representation does not match the expected digest, the result is non-`ALLOW` with `POLICY_DIGEST_MISMATCH`.

This RFC does not require a new canonical policy-storage system. It requires the evaluator to identify the immutable policy bytes it actually used.

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
- `AuthorizationDecisionRequest v0.2`;
- `AuthorizationDecisionResult v0.2`; and
- `AuthorizationDecisionTrace v0.2`.

`RoleAssignment v0.1`, `RevocationDecision v0.1`, and `DataSovereigntyBoundary v0.1` remain unchanged by default. If schema changes to those families prove necessary, they require an explicit scope review before editing.

### 17.3 Source-record delta

Common v0.2 source behavior:

- make `authorityFamilies` closed and required where the source carries authority families;
- add optional closed `permittedUsePurposes`;
- remove free-text `purpose` and `conditions` from the executable v0.2 form;
- reject unknown fields;
- add optional target narrowing by governed target kinds, target refs, and twins;
- retain closed action, scope, time, state, and inheritance constraints; and
- preserve provenance linking a migrated record to its v0.1 predecessor.

`DelegationGrant v0.2` additionally pairs `requiredEvidenceRefs` with `requiredEvidencePolicyRef` and makes the pairing all-or-none.

`SharingGrant v0.2` makes the artifact-family to target-kind binding explicit and keeps `dataSovereigntyBoundaryRefs` restricted to actual sovereignty records.

### 17.4 Request v0.2

Caller-provided request facts:

- request identifier and request time;
- requested action class;
- trusted-boundary actor resolution reference, not a self-asserted posture;
- full target kind, reference, scope, time, and twin where applicable;
- optional requested use-purpose token;
- optional AI-assistance disclosure; and
- optional retrieval hints that are explicitly non-authoritative.

Remove these caller-authoritative v0.1 fields:

- `actionStage`;
- `requiredAuthorityFamily`;
- `nonHumanActor`; and
- `revocationCheckRequired`.

They are derived or mandatory policy facts in v0.2.

### 17.5 Result v0.2

The result records:

- request and result identifiers;
- evaluation time;
- requested action class;
- derived stage and authority family;
- policy identity and selected rule;
- actor posture;
- deterministic outcome and primary reason code;
- role, direct grant, delegation, sharing, and revocation basis summaries;
- inheritance mode applied;
- human approval and final-action posture;
- stable ordered problems; and
- trace reference.

### 17.6 Trace v0.2

The trace records at least:

- trace, request, and result identifiers;
- evaluation time;
- policy ID, version, digest, and selected rule;
- action class, derived stage, and derived family;
- acting Party, acting agent where applicable, trusted actor posture, actor-resolution evidence refs, and AI-disclosure disposition;
- full target kind, reference, scope, time, and twin;
- target proof refs and individual dispositions;
- scope proof refs and individual dispositions;
- role assignments and anchor-scope dispositions;
- direct grant, delegation, source-grant, and sharing bases and dispositions;
- revocation decisions and dispositions;
- requested purpose, source purpose tokens, and purpose disposition;
- condition disposition;
- evidence-policy refs, required evidence refs, constraint evidence refs, and individual evidence dispositions;
- actual data-sovereignty boundary refs only;
- inheritance mode and delegation depth;
- human-finalization evidence refs and disposition;
- every evaluated path summary, selected path, decision outcome, primary reason code, and reason; and
- a decision-bundle integrity digest.

Proof arrays are typed by use. An implementation must not place a scope proof in `constraintEvidenceRefs`, an evidence record in `dataSovereigntyBoundaryRefs`, or an arbitrary string in a proof array merely to satisfy cardinality.

---

## 18. Durable decision-bundle and effect ordering

The request, result, and trace are one logical decision bundle.

For both `ALLOW` and non-`ALLOW`:

1. build all three records from the same evaluated state and policy digest;
2. validate their cross-references and integrity digest;
3. persist them atomically, or under an equivalent protocol that cannot expose a final result without its trace;
4. commit the decision bundle; and
5. only then expose the final authorization response.

For `ALLOW`, the protected effect must not occur before the decision bundle commits.

For `DENY`, `REQUIRE_REVIEW`, or `REQUIRE_HUMAN_APPROVAL`, the refusal bundle must commit before an outer transport boundary converts the result into a typed error response.

If decision persistence fails, the runtime must fail closed with a persistence/runtime error. It must not claim that a durable authorization denial or allowance exists when no trace committed.

This ordering is a future runtime conformance obligation. Phase A changes no runtime code.

---

## 19. Compatibility and migration

### 19.1 Historical validity

Existing v0.1 records remain valid as v0.1 records under the policy that evaluated them. They are not rewritten in place.

### 19.2 No silent proof-strength upgrade

A v0.1 decision or source record must not be relabeled, wrapped, or served as v0.2 merely because a runtime can fill some new fields with defaults.

In particular:

- missing policy digest cannot be reconstructed from the current deployment without proving it is the same immutable policy;
- optional AI metadata cannot reconstruct trusted actor posture;
- a target reference cannot reconstruct target proof;
- a scope string cannot reconstruct scope proof;
- free-text purpose cannot reconstruct a purpose token;
- free-text conditions cannot be presumed satisfied; and
- untyped evidence refs cannot reconstruct an eligibility disposition.

### 19.3 Source migration

Migration creates a new v0.2 source record and preserves a provenance link to the v0.1 record. A steward must explicitly decide:

- the exact authority-family tokens;
- the purpose-token set, if any;
- how each legacy condition is preserved in supported closed constraints;
- the evidence policy, if required;
- target narrowing; and
- whether the v0.1 source is retired, allowed to expire, or retained for the v0.1 evaluator only.

Automated migration may propose a mapping. It may not activate the new authority without steward approval.

### 19.4 Coexistence

Draft v0.2 contracts remain under `drafts_non_default/` and cannot become current/default by file presence. Runtimes must declare which bundle they evaluate. A deployment may support v0.1 and v0.2 concurrently, but each decision is bound to exactly one policy and schema bundle.

---

## 20. Stable reason codes

The v0.2 conformance package should include at least these reason codes:

- `REQUEST_SCHEMA_INVALID`
- `UNKNOWN_ACTION_CLASS`
- `UNKNOWN_TARGET_KIND`
- `POLICY_NOT_AVAILABLE`
- `POLICY_DIGEST_MISMATCH`
- `UNRESOLVED_ACTOR_POSTURE`
- `SOFTWARE_AGENT_NOT_PERMITTED`
- `HUMAN_FINAL_ACTION_REQUIRED`
- `TARGET_NOT_PROVEN`
- `TARGET_KIND_MISMATCH`
- `TARGET_REF_MISMATCH`
- `TWIN_MISMATCH`
- `TENANT_BOUNDARY_MISMATCH`
- `SCOPE_NOT_PROVEN`
- `ROLE_ASSIGNMENT_NOT_APPLICABLE`
- `ROLE_ANCHOR_SCOPE_MISMATCH`
- `NO_AUTHORITY_BASIS`
- `ACTION_CLASS_NOT_GRANTED`
- `AUTHORITY_FAMILY_MISMATCH`
- `INHERITANCE_NOT_PERMITTED`
- `AUTHORITY_NOT_ACTIVE_AT_TARGET_TIME`
- `PURPOSE_REQUIRED`
- `PURPOSE_NOT_PERMITTED`
- `UNSUPPORTED_LEGACY_PURPOSE`
- `UNSUPPORTED_LEGACY_CONDITION`
- `EVIDENCE_POLICY_REQUIRED`
- `UNSUPPORTED_EVIDENCE_POLICY`
- `REQUIRED_EVIDENCE_MISSING`
- `REQUIRED_EVIDENCE_INELIGIBLE`
- `DELEGATION_SOURCE_MISSING`
- `DELEGATION_BROADENS_AUTHORITY`
- `DELEGATION_CYCLE`
- `DELEGATION_DEPTH_EXCEEDED`
- `SHARING_BASIS_MISMATCH`
- `ACTIVE_REVOCATION`
- `UNSUPPORTED_REVOCATION_NARROWING`
- `DECISION_BUNDLE_PERSISTENCE_FAILED`

Schemas may add more specific codes later. They must not collapse a known authorization failure into an unstructured message.

---

## 21. Invariants

The accepted design and conformance suite must preserve these invariants:

1. Omitting or changing optional AI-assistance metadata never increases authority.
2. Caller-supplied stage, family, actor type, or revocation posture never controls the policy result.
3. Exactly one versioned action rule derives stage, family, inheritance ceiling, target policy, delegation posture, and actor posture.
4. Unknown action, family, target-kind, condition, evidence policy, or proof type is non-`ALLOW`.
5. A role-targeted grant never exceeds either its grant scope or its role anchor scope.
6. A delegated path never exceeds its source path at any constraint dimension.
7. A purpose-constrained source cannot pass without an exact matching request purpose.
8. Caller-only purpose never creates source authority.
9. Free-text purpose and conditions are never guessed into executable v0.2 semantics.
10. Every required evidence ref is individually resolved and evaluated under the named active policy.
11. Target proof and scope proof remain distinct and are both required where applicable.
12. `dataSovereigntyBoundaryRefs` contains only actual sovereignty records.
13. A SharingGrant grants read/receive use only for its exact grantee and artifact.
14. Every effective revocation is considered from a completeness-proven source.
15. Partial grant paths are not unioned into a fabricated complete path.
16. The same immutable inputs and policy digest produce the same outcome, selected basis, ordered problems, and primary reason code.
17. A protected effect never precedes durable commit of its decision bundle.
18. A typed refusal never claims a durable trace that did not commit.
19. v0.1 records never silently claim v0.2 proof strength.
20. Draft schema presence never changes current/default status.

---

## 22. Production-reachable hostile cases

The future executable conformance suite must include at least:

| Case | Required disposition |
|---|---|
| Same request retried after omitting `aiAssistance.assisted: true` | same actor posture and no authority increase |
| Caller changes `nonHumanActor` or derived family/stage hint | hint ignored or schema-rejected; policy result unchanged |
| Sponsor-bound agent attempts a human-only review decision | non-`ALLOW` |
| AI-assisted high-risk assertion has no fresh human final action | `REQUIRE_HUMAN_APPROVAL` |
| Grant purpose is `REGULATORY_FILING` and request purpose is `regulatory_filing` | exact mismatch; non-`ALLOW` |
| Request supplies a purpose but source does not authorize it | caller-only purpose creates no authority |
| v0.1 source contains a non-empty free-text condition | `REQUIRE_REVIEW` with `UNSUPPORTED_LEGACY_CONDITION` |
| Required evidence ref is absent | `DENY` |
| Evidence resolves to the wrong family | `DENY` |
| Evidence is stale, disputed, or superseded under policy | `DENY` |
| Evidence belongs to another tenant | `DENY` |
| Role-targeted grant scope covers target but role anchor does not | `DENY` |
| Delegated source is role-targeted and its role anchor does not cover target | `DENY` |
| Target ref exists but has the wrong target kind | `DENY` |
| Scope string matches but no trusted scope proof exists | `DENY` |
| Target proof is placed in `dataSovereigntyBoundaryRefs` | schema or semantic rejection |
| Scope proof is substituted into `constraintEvidenceRefs` | schema or semantic rejection |
| Policy version matches but digest differs | non-`ALLOW` |
| Active `TERMINATE` revocation is omitted from caller candidates | revocation still found; `DENY` |
| Active v0.1 narrowing revocation is present | `REQUIRE_REVIEW` until closed semantics exist |
| SharingGrant artifact family/ref differs from requested target | `DENY` |
| SharingGrant is offered for a write or review action | basis ineligible |
| One grant supplies action and another supplies matching purpose | paths remain incomplete; non-`ALLOW` |
| Refusal trace insert is rolled back with a thrown transport error | conformance failure |
| Decision-bundle persistence fails | no effect and no false durable-decision claim |
| Draft v0.2 files exist but currentness still names v0.1 | v0.1 remains current/default |

Fixtures must enter through production-reachable evaluator and persistence paths. Unit-only helper tests are not enough for a conformance claim.

---

## 23. Traceability to the triggering review

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

This table does not authorize an OFARM2 fix. OFARM2 must wait for accepted semantics, promoted contracts, and byte-identical extraction.

---

## 24. Staged delivery and currentness

The required sequence is:

1. **Phase A candidate:** this document only; no authority or currentness effect.
2. **Semantic approval:** stewards approve or amend the approval card in section 25.
3. **Accepted RFC and action matrix:** a separate governed PR promotes approved prose and an exact v0.2 matrix.
4. **Draft/non-default contracts:** a separate PR adds source and decision v0.2 schemas, examples, and validation without currentness promotion.
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
| Is actor posture trusted-boundary derived and AI disclosure non-authoritative? | yes | yes |
| Are action stage and authority family policy-derived rather than caller-selected? | yes | yes |
| Is the exact matrix in section 7 the v0.2 closure, including target kinds? | yes | yes, row-by-row amendments allowed |
| Is `OUTPUT_FILE_SUBMISSION_ASSEMBLY` fixed to `ATTEST_SIGN`? | yes | yes |
| Are no existing actions granted lineage inheritance? | yes | yes |
| Are purpose tokens exact-match and optional only when the source is unrestricted? | yes | yes |
| Must legacy free-text purpose be explicitly migrated? | yes | yes |
| Are free-text conditions unsupported and fail-closed? | yes | yes |
| Must required evidence name an active eligibility policy? | yes | yes |
| Are role-targeted source paths capped by role anchor scopes? | yes | yes |
| Is default delegation depth one hop? | yes | yes |
| Are v0.1 narrowing revocations non-`ALLOW` until separately closed? | yes | yes |
| Is SharingGrant an exact-artifact access basis only for `RECEIVE_READ_DATA`? | yes | yes |
| Must target and scope proof use separate typed fields? | yes | yes |
| Must every result identify immutable policy bytes by SHA-256 digest? | yes | yes |
| Must non-`ALLOW` bundles commit before transport errors are returned? | yes | yes |
| Does honest v0.2 require versioned source records as well as decision records? | yes | yes |
| Does current/default promotion remain a separate final step? | yes | yes |

Any amendment must state whether it changes only this authorization boundary. A requested authentication, principal-resolution, key-custody, database, or runtime-integration change must be split.

---

## 26. Completion criteria for Phase A

Phase A is complete when:

- this candidate is reviewed against issue `samovers/OFARM#10`;
- every acceptance criterion has a proposed disposition;
- the source-record versioning decision is explicit;
- the action matrix and target-kind closure are reviewed;
- migration and currentness rules are accepted or amended;
- hostile cases are judged sufficient to detect proof substitution and fail-open behavior;
- the trust boundary remains authorization law and machine-contract governance; and
- no active authority or schema was changed by the candidate PR.

What is next: steward review and explicit semantic approval before any accepted-RFC or machine-contract edit.
