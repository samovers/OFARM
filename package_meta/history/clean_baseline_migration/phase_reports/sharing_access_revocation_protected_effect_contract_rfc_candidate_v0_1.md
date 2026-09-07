# OFARM Sharing-Access Revocation Protected-Effect Contract v0.1

Date: 2026-09-07

Status: non-authoritative Phase A candidate; review and semantic approval pending

Issue: [samovers/OFARM#27](https://github.com/samovers/OFARM/issues/27); parent [#12](https://github.com/samovers/OFARM/issues/12)

Inspected canonical main: `71ca724a8b6ec23f1655b086a6f549496d10a47f`

Downstream: [OFARM2#353](https://github.com/samovers/OFARM2/issues/353) / [draft PR #359](https://github.com/samovers/OFARM2/pull/359)

## 1. Decision requested

Approve or amend this proposed domain contract, not an authorization rule or runtime implementation:

1. `SHARE_REVOKE_ACCESS` produces exactly one new immutable `RevocationDecision v0.1`, affecting exactly one immutable `SharingGrant` through `TERMINATE`.
2. The current RevocationDecision schema stays unchanged. The result, complete intent, exact grant/artifact proof, finalization evidence, and protected-effect trace form one bound proof; a bare schema-valid result is insufficient.
3. The deciding Party comes from the independently eligible human approver's authority path. The authenticated human and requesting principal remain separately identifiable. `decidedAt` copies trusted `humanActedAt`.
4. `effectiveFrom`, the exact grant identity, proposed result identity, and common-envelope scope are not rewritten. The intent's reason is copied exactly into required `notes`; `affectedActionClasses` and `replacementGrantRefs` are absent in this contract.
5. The formal revocation act is classified as `GovernanceEvent`; the RevocationDecision record has commit class `governance decision`. This classification creates neither a second event record nor an automatic materialized consequence.
6. Domain validation passes before the common fresh-human-approval transaction can commit the exact result and its evidence. A domain failure never rewrites an authorization outcome.
7. No grant mutation, inferred replacement, lineage-wide termination, narrowing mode, retrospective history rewrite, or claim that every access route has ended is permitted.

These are candidate choices for review. Nothing in this file is accepted law, a materialized machine contract, semantic approval, merge authority, current/default promotion, or OFARM2 implementation authority.

## 2. Primary trust boundary and intended PR boundary

The primary trust boundary is **sharing-revocation domain effect semantics and commit classification**: the result carrier, mappings, permitted derivations, forbidden widening, postconditions, and validation evidence for this one action.

The intended PR changes only this Phase A file in the historical phase-report lane. It does not edit accepted RFCs, Event Grammar, companion policy, schemas, indexes, runtime code, or another candidate PR.

| Responsibility | Owner consumed by this candidate | Limit on this candidate |
|---|---|---|
| Who may revoke; action, target, sovereignty, evidence, human-approval and source-path rules | Approved PR #11 semantic candidate and active authority law | No second evaluator, extractor, eligibility rule, or reason-code registry |
| Authenticated principal, representation, sponsor and agent actorship proof | Trusted principal/representation and CP3 boundaries | No caller-asserted human or Party substitution |
| Exact RevocationDecision result and its domain validation | This issue #27 candidate | One action, one record family, `SHARING_GRANT` / `TERMINATE` only |
| Top-level event meanings and commit classes | Constitution and active Event Grammar | Apply existing categories; do not amend them here |
| Fresh-approval lifecycle, state guards, atomicity, single use, retry and recovery | Approved PR #20 semantic candidate | Consume its complete handoff; do not implement or change the protocol |
| Immutable SharingGrant v0.2 source and issuance semantics | Separate PR #11 section 24 source-bundle stage | No source issuance, migration or mutation here |
| Shared finalization/receipt envelopes and evidence retention | PR #11 / #19 evidence work and #14 | Define only the domain validation payload and required bindings; no second evidence store or custody policy |
| Acceptance, currentness, extraction and production implementation | PR #11 section 24 and #21; later OFARM2 decisions | No stage is implied by this candidate's approval |

If satisfying this contract requires another authority owner to change semantics or bytes, stop before that edit and propose a linked prerequisite. In particular, a RevocationDecision carrier change needs explicit scope review because PR #11 retains v0.1 unchanged.

## 3. Governing sources and exact dependency pins

Apply `PROJECT_AUTHORITY.md`: active baseline outranks accepted RFCs, then companion artifacts, then machine contracts. The historical candidates below are approved design dependencies, not active accepted law.

| Source | Relevant authority or dependency |
|---|---|
| `00_active_baseline/OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md`, sections 7.9-7.18, 11 and 13, AAI-C.3 and AAI-C.6 | Sharing differs from action authority; revocation preserves history; accountable human actorship; separate event families, commit classes and stronger in-force results |
| `00_active_baseline/OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md` | Applicable EnforcementChain gates, history-first authority and controlled materialization remain independent |
| `02_accepted_rfcs/OFARM_Authority_Source_Record_Closure_RFC_v0_1.md`, sections 2, 4.4 and 4.5 | Minimal, distinct SharingGrant and RevocationDecision source records; no hidden policy engine |
| `01_companion_artifacts/OFARM_Authority_Delegation_and_Data_Sovereignty_Policy_v0_2.md`, sections 3.5, 3.8, 6-10 | Governance decisions with effect; separate share/revoke authority; prospective, traceable revocation without erasing attested history |
| `01_companion_artifacts/OFARM_Event_Grammar_and_Commit_Matrix_v0_1.md`, sections 2, 3.7, 4, 6.8, 8 and 10 | Dominant-consequence classification; formal decision/mandate; governed in-force status change without a truth-promotion shortcut |
| [PR #11](https://github.com/samovers/OFARM/pull/11), exact head `03a21f669ee04f96d444e14f00ae7212cab04803` | `authorization_constraints_and_decision_evidence_rfc_candidate_v0_2.md`, sections 6-8, 14, 17.3, 18 and 24; exact approved action, intent, source identity, finalization and staged-delivery rules |
| [PR #20](https://github.com/samovers/OFARM/pull/20), exact head `98f8c4fafbae42c8f7fd931f43f53adcb4733713` | `governed_human_approval_transaction_and_consumption_protocol_rfc_candidate_v0_1.md`, sections 8-16, 18 and 20; approved fresh-approval transaction and domain handoff |
| `03_machine_contracts/CONTRACT_FAMILY_CURRENTNESS.json` and `CONTRACT_INDEX.json` | Select actual current carriers; presence or filename does not establish promotion |

Both candidate filenames above are under `package_meta/history/clean_baseline_migration/phase_reports/` at their stated commits. They are not copied into this PR. A dependency-head change requires inspection and renewed binding review, not substitution of the latest filename.

The baseline readiness and hostile-review records still identify sharing/revocation implementation depth as bounded debt. This candidate does not remove that readiness limit or change CP14 downstream revocation-propagation requirements.

## 4. Current carrier and coverage inventory

### 4.1 RevocationDecision

Current/default carrier: `03_machine_contracts/schemas/core/OFARM_RevocationDecision_schema_v0_1.json`.

Its raw-file SHA-256 at the inspected baseline is `71e24e0adef2b58c5103bd49c755a2922a47e0df9df94fcbab7d3054893bd68a`. Its `$id` is `https://ofarm.dev/schema/revocationdecision/v0.1`; `schemaVersion` is `ofarm.revocationdecision.v0.1`. It rejects additional properties.

The schema requires the nine fields `schemaVersion`, `revocationDecisionId`, `revokesArtifactFamily`, `revokesArtifactRef`, `decidedByPartyRef`, `decidedAt`, `effectiveFrom`, `revocationMode`, and `targetScope`. It also permits `affectedActionClasses`, `replacementGrantRefs`, and `notes`. Its general family and mode enums cover more than this action; schema validity is therefore weaker than this contract's validity.

It has no dedicated fields for the source digest, shared-artifact revision, tenant/twin proof, human principal, approval binding, protected-effect contract, or validation trace. Those facts must remain provable through the exact intent and bound evidence. Do not squeeze them into free-text notes or add undeclared result fields.

The currentness map names two examples: the service-provider operation revocation under `examples/machine_contracts/authority/` and the submission-officer filing revocation under `examples/machine_contracts/core/`, both inside `04_implementation_and_conformance/examples_and_fixtures/`. They revoke `DELEGATION_GRANT` and `AUTHORITY_GRANT` respectively; neither is a positive example of this sharing-only contract. They remain unchanged and do not establish its executable coverage.

### 4.2 SharingGrant

The current/default schema is `03_machine_contracts/schemas/authority/OFARM_SharingGrant_schema_v0_1.json`, raw-file SHA-256 `18be0d59e130c88ec0b408762488c84ddaa52a6e64cf217a2757b4f5d99a7c98`. The currentness map lists no draft/non-default SharingGrant successor at the inspected baseline.

That current source has logical artifact references, optional prose conditions/purpose, an `OTHER` artifact branch and mutable-looking sharing states. It does not supply PR #11's exact immutable v0.2 source identity, artifact-revision and rule-binding proof. It cannot be silently relabelled v0.2. The protected result remains RevocationDecision v0.1, while its affected source must meet the separately materialized SharingGrant v0.2 contract.

### 4.3 Carrier decision

Keep RevocationDecision v0.1 unchanged and constrain its use through one separate protected-effect contract. The complete proof includes the result and bound evidence; the result alone is not advertised as a self-contained authorization or revocation-proof package. If exact evidence binding cannot be represented by the later owning contracts, materialization stops. This candidate does not invent RevocationDecision v0.2 or an executable placeholder source.

## 5. Closed action and logical input set

### 5.1 Action binding

| Axis | Fixed approved value consumed here |
|---|---|
| Action | `SHARE_REVOKE_ACCESS` |
| Authority family / stage | `SHARE_REVOKE` / `PROMOTION` |
| Inheritance / delegation ceiling | `EXACT_ONLY` / `EXPLICIT_SOURCE_PERMISSION_REQUIRED` |
| Agent posture | `AGENT_ALLOWED_WITH_HUMAN_APPROVAL` |
| Human finalization / separation | `FRESH_HUMAN_APPROVAL_REQUIRED` / `SAME_PRINCIPAL_ALLOWED` |
| Intent / resource policy | `EI_SHARING_REVOKE_V0_2` / `RP_SHARE_REVOKE` |
| Effect subject / existence | `REVOCATION_DECISION` / `PROSPECTIVE_TARGET_ALLOWED` |
| Validity / consumption / external posture | `TRANSACTION_BOUND_V0_2` / `SINGLE_USE` / `NO_EXTERNAL_DISPATCH` |
| Action evidence policy | `EP_SHARING_SOVEREIGNTY_V0_2` |

This table does not authorize a caller to supply those values, change their source, or omit any other selected rule field. PR #11 selects the complete immutable rule and extractor. A natural-person request still follows the fresh-approval lifecycle; it is not silently routed through `DIRECT_HUMAN_ACTION_REQUIRED` or `NOT_REQUIRED`.

### 5.2 Inputs and proof ownership

The following names are logical operands for the later exact contract, not new wire fields, independent caller facts, or permission to materialize schemas in Phase A:

- `I`: the complete intent validated against the rule-selected schema, including its common authorization envelope, proposed result ID, affected family, immutable SharingGrant ID/digest, artifact revision, `TERMINATE`, `effectiveFrom` and reason.
- `V`: the complete authorization view produced only by the rule-selected extractor from `I`, including resources, effect subject, scope, tenant and twin where applicable. A result constructor may not run a second authority extractor.
- `G`: the exact immutable SharingGrant v0.2 record named by `I` and the `AFFECTED_SHARING_GRANT` input, with schema, source-record and artifact bindings plus typed relationship proofs.
- `H`: the mode-correct prospective finalization-evidence object constructed by PR #20 before the final authorization evaluation. It binds the trusted human act, exact challenge/display, requester basis, independently eligible human approver path, representation, both snapshots, equal relevant-state digests, and exact validity window. It is not portable or durably successful before atomic commit.
- `A`: the authoritative final authorization bundle admitting that exact `H`, with the same candidate requester basis and `decisionValidUntil`, the required finalization disposition, and `ALLOW` for the exact operation.
- `R`: the complete proposed RevocationDecision bytes, not yet committed.
- `S`: the final transaction snapshot, relevant immutable state inputs, result-identity absence/uniqueness evidence and complete commit guards supplied by the common protocol.
- `B`: the rule-bound domain contract and its exact schema, mapping, postcondition and evidence-profile bindings.

All used refs resolve to the exact governed immutable bytes and typed proofs. A digest match is not proof of tenant, scope, eligibility or representation by itself. The domain gate consumes the relevant proved facts and cross-bindings; it neither reevaluates grants nor replaces another gate's missing proof with a caller assertion.

### 5.3 One target, one affected source, one result

`SHARED_ARTIFACT` is the one `AUTHORITY_TARGET`, exactly one of:

- `PASSPORT_VIEW`;
- `DOCUMENT_ASSEMBLY`;
- `DOSSIER_ASSEMBLY`;
- `SUBMISSION_ASSEMBLY`;
- `EVIDENCE_BUNDLE`; or
- `CURRENT_STATE_MATERIALIZATION`.

`AFFECTED_SHARING_GRANT` is exactly one existing `SHARING_GRANT` with posture `STATE_INPUT`. It is not a second authority target or the grant authorizing this write. Its immutable artifact family, logical identity and revision must match the shared artifact bound by the same intent. Matching only the logical artifact ID is insufficient.

The proposed RevocationDecision ID is the distinct prospective effect subject. It must match the intent and be covered by the protocol's namespace/tenant and uniqueness guards. No existing result may be overwritten, even with a claimed correction or a new digest.

The result's `targetScope` copies the complete common-envelope scope from `V`, not a scope synthesized from the grant, a UI value or an inferred parent. All target, source and result scope relationships must also pass their governing typed proofs. The scope pair documents the bound action; under the already fixed `TERMINATE` semantics it cannot turn exact-source termination into partial scope revocation. This candidate adds no new inheritance or scope-equality rule for authority sources.

If the future approved common scope cannot be represented completely as one v0.1 `{scopeType, scopeRef}` pair, or if its relationship to the exact affected grant is ambiguous, stop materialization. Do not truncate the scope or silently alter the authorization envelope.

## 6. Exact intent-to-result mapping

Each mapping below must appear once in the validation trace. “Exact copy” means the same validated JSON value, including string contents; it is not paraphrase, case folding, timezone conversion, trimming, concatenation or interpretation. Object member order follows the bound canonicalization, not a new meaning.

| Mapping ID | Result field | Source and required mapping |
|---|---|---|
| `SR_SCHEMA` | `schemaVersion` | Contract constant `ofarm.revocationdecision.v0.1`; validate all of `R` under the exact v0.1 schema bytes |
| `SR_ID` | `revocationDecisionId` | Exact copy of `I`'s proposed RevocationDecision ID; equal to `V`'s prospective effect-subject ID |
| `SR_FAMILY` | `revokesArtifactFamily` | Exact copy of `I`'s affected family, required equal to `SHARING_GRANT` |
| `SR_GRANT` | `revokesArtifactRef` | Exact copy of the immutable SharingGrant ID in `I`; equal to `G`'s one-record ID and the state-input binding |
| `SR_PARTY` | `decidedByPartyRef` | Contract-defined selection of the independently eligible human approver path's `authoritySubjectPartyRef` from `H`, validated by `A`; see section 7.1 |
| `SR_DECIDED_AT` | `decidedAt` | Exact copy of trusted `H.humanActedAt`, never caller time or a retry/commit timestamp |
| `SR_EFFECTIVE_FROM` | `effectiveFrom` | Exact copy of the intent's `effectiveFrom`; no replacement by “now,” decision validity end, grant expiry or commit time |
| `SR_MODE` | `revocationMode` | Exact copy of the intent's mode, required equal to `TERMINATE` |
| `SR_SCOPE` | `targetScope` | Exact copy of the complete common-envelope scope produced in `V`, as the one schema-valid pair described in section 5.3 |
| `SR_ACTIONS_ABSENT` | `affectedActionClasses` | Required absence, including absence of an empty array; this contract terminates the exact grant rather than an action subset |
| `SR_REPLACEMENTS_ABSENT` | `replacementGrantRefs` | Required absence, including absence of an empty array; no replacement is created or implicitly governed by this result |
| `SR_REASON` | `notes` | Required exact copy of the intent-bound reason string, including its original content; no generated summary, added commands or missing value |

The later intent/schema binding must make the reason exactly representable as the v0.1 string. This candidate introduces no free-text interpreter and does not coerce a structured reason into JSON text. If the approved intent's reason has a different shape, binding review stops instead of inventing a lossy conversion. Any emptiness or content restriction imposed by that exact intent schema still applies; the result cannot weaken it.

The current v0.1 optional fields remain valid in their other governed uses. Requiring two to be absent and `notes` to be present is this contract's action-specific constraint, not a rewrite of the general carrier or historical examples.

Every other result property is forbidden by the unchanged schema. There are no discretionary generated result fields. Tenant, twin, artifact revision/digest, source digest, human-principal identity and evidence bindings remain in the complete bound proof described in section 10, not in invented result properties or encoded notes.

## 7. Human, Party and time mapping

### 7.1 Accountable deciding Party versus requesting principal

The act that decides the revocation is the independently eligible natural person's explicit approval under the exact PR #11 fresh-approval rule. For `SR_PARTY`:

- a self-action path yields that authenticated natural person's Party;
- an authorized-representation path yields the represented Party established by that human's exact eligible path and immutable representation evidence.

The requesting software agent's Party, sponsor, service account, grantor or grantee is not a substitute for this deciding Party. The requester and approver paths remain separate, even if their Party values happen to match. No extra equality or permission rule is inferred between those paths; all same-action, Party-posture and representation constraints remain exactly those of PR #11.

The validation payload binds the authenticated natural-person principal, its immutable resolution evidence, the selected human-path authority subject/basis, representation posture and evidence, trusted act time and exact `H` ref/digest. Under self-action, representation evidence is required absent rather than fabricated. Under represented action, its exact required evidence must be present and valid. The result's Party string alone cannot prove who acted.

This human-path selection is an explicit proposed domain mapping, not a modification of requester authorization or an assumption that sponsor status grants approval power. A missing or ambiguous human-path binding prevents a passing result.

### 7.2 Separate times and prospective effect

Keep these values distinct: the human's trusted act time; `R.decidedAt`; the intent-bound `effectiveFrom`; trusted final authorization time; transaction start/deadline; `decisionValidUntil`; and actual commit time. Any applicable subject time remains a separate intent fact. Compare instants under the exact governed time contracts; equality of copied fields still preserves the source value.

`decidedAt` records the actual challenged human act, not a fresh decision on each retry. `effectiveFrom` records the exact authorized requested effective instant. It may not be silently advanced because finalization took time or a scheduled instant passed. Copying that value does not backdate the commit, recreate a past authorization snapshot, void prior attested history, or authorize retrospective rewriting. This contract adds no grace period, universal scheduling interval, or stronger retrospective-governance rule.

The new record is unavailable as committed revocation evidence until the atomic success set commits. Thereafter PR #11's existing exact-source lookup evaluates effective termination at trusted evaluation/effect time against its complete governed snapshot. This contract does not build that index or reinterpret its historical-time behavior. A future effective instant remains future; merely recording the decision does not mean access was already cut off.

The only domain write is the new decision. Previously recorded grants, decisions, receipts, disclosures and attested history are unchanged. Any requested historical correction, recall, deletion or stronger retrospective consequence needs a separately governed action and contract; it cannot be hidden in `effectiveFrom` or the reason.

## 8. Event family, commit class and consequence boundary

The proposed classification is:

| Dimension | Value | Why it fits the existing law |
|---|---|---|
| Primary family of the formal revocation act | `GovernanceEvent` | Constitution 7.17 identifies a RevocationDecision; Constitution 13.2 and Event Grammar 3.7 cover formal decision/enforcement acts; this act decides cessation of a specified permission |
| Commit class of the immutable RevocationDecision record | `governance decision` | The decision mandates prospective cessation of the exact source's permission; the authority companion policy 3.5 covers governance decisions with effect, and Event Grammar 6.8/8 cover formal approve/mandate decisions and governed in-force status change |
| Classification of the separate authorization/finalization evidence | `EvidenceEvent` / `evidence record` under its own contract | It proves the authorization and transaction, not the domain decision's meaning |

This is an explicit interpretation for steward review, not an inference from the word “revoke” alone. The dominant consequence is a formal permission decision. The original grant is not mutated as a durable-configuration update, and the result is not an observation, operation claim, compliance assertion or mere audit evidence. No new top-level family or commit class is introduced.

Record the domain classification in the protected-effect validation payload and handoff; do not add event fields to RevocationDecision v0.1. Classifying the associated act does not construct a SemanticEvent, pass Event Ingress, or supply permission for a second domain write. Any separately required ingress evidence is admitted through its existing owner and truthful gate disposition. If the selected production path requires an additional domain event/consequence whose exact contract and composition are not already governed, stop for that separate prerequisite.

The contract's domain result set is exactly one RevocationDecision. It contains no replacement SharingGrant, grant-state update, accepted-event consequence, current-state materialization, filing outbox, transport command, notification, deletion or recipient-use propagation record. Downstream authorization/read and CP14 controls retain their own obligations; their existence is not a claim that this result alone executed them.

## 9. Domain postconditions and commit obligations

### 9.1 Domain postconditions evaluated before commit

| Postcondition ID | Required proof |
|---|---|
| `SR_PC_BINDINGS` | Exact selected rule, intent/schema, extractor/view, contract, result schema, source and finalization identities resolve and agree; no caller-selected substitute |
| `SR_PC_TARGET` | Exactly one allowed shared-artifact authority target, one exact affected SharingGrant state input and one prospective result; artifact kind/identity/revision and grant ID/digest cross-bind correctly |
| `SR_PC_SCOPE` | Complete scope mapping plus governing target/source/result tenant, scope and conditional twin relationship proofs; no alias or inferred-parent substitution |
| `SR_PC_HUMAN` | Exact independently eligible natural-person act and Party/representation binding support the mapped deciding Party and time; requester provenance remains distinct |
| `SR_PC_TIMES` | All copied times retain their sources; trusted finalization time/window checks are bound; no backdated commit or additional historical write is proposed |
| `SR_PC_APPEND_ONLY` | One new prospective result ID under complete absence/uniqueness guards; unchanged existing grant bytes and no updates/deletes to prior history in the admitted domain write set |
| `SR_PC_NO_WIDENING` | Exact-source `TERMINATE` only; no action/scope narrowing, source-family switch, replacement reach, new access rights or unbound companion effect |
| `SR_PC_CLASSIFICATION` | Associated act is `GovernanceEvent`; result class is `governance decision`; no fabricated event or promotion claim |
| `SR_PC_PROOF` | Complete, digest-verified mapping/postcondition inputs and trace payload are available for the exact result; proof missing from the bare carrier is retained in the bound evidence |

All twelve `SR_*` field mappings in section 6 must also pass. A required-absence check passes because absence was proved; it is not skipped as “not applicable.” The complete proposed write set must be bound before `SR_PC_APPEND_ONLY` and `SR_PC_NO_WIDENING` can pass.

The domain gate does not add a “one revocation ever per SharingGrant” uniqueness rule. Result identity and operation consumption are unique; whether a separate operation against an already affected grant is admissible remains governed by the selected authorization/resource policies. An existing matching operation succeeds only by retrieving its original receipt, not by creating a new decision.

### 9.2 Obligations owned by the common transaction boundary

The precommit domain trace proves the proposed bytes and required guards, not that a future transaction has already committed. PR #20 must maintain those guards, persist the exact validated bytes and complete success set atomically, and bind actual committed result identity/digest and commit time in its receipt.

Required integration assertions are: no result-byte substitution after validation; no guarded-state or identity race escaping the final guard; no visible partial result/evidence/consumption set; and no reuse of a decision or approval. The domain payload binds the expected guards and write set; the transaction receipt supplies the actual commit proof. A domain `PASS` is never substituted for that receipt.

## 10. Content addressing and immutable validation evidence

### 10.1 Proposed contract identity and digest discipline

Proposed contract ID: `ofarm.protectedeffect.sharingaccess.revocation.v0.1`; proposed version: `0.1`. These identify the candidate design, not currently resolvable machine-contract bytes.

Later materialization must bind one immutable contract unit containing the supported action, exact result-schema binding, input/schema selectors, all mapping and postcondition IDs, permitted conditional dispositions, canonicalization and validation-payload schema. The selected authorization rule binds that unit by ref, version and digest; it cannot select mappings independently or rely on a mutable latest-version lookup.

Digest domains remain explicit:

- The complete validated intent uses PR #11's RFC 8785 JCS/SHA-256 profile with no excluded intent member.
- The RevocationDecision result uses JCS/SHA-256 over the whole schema-valid result, including `notes`; it has no self-digest field to exclude.
- The SharingGrant's `sourceRecordDigest` uses PR #11 section 17.3's exact source projection excluding only its top-level `/sourceRecordDigest`. Preserve its distinction from a raw source-file byte digest.
- Schema and contract artifact bindings identify their actual immutable bytes and declared hash profile. The raw schema-file hash in section 4 is inventory evidence, not a guessed future contract/manifest digest.
- Finalization, decision, validation-trace envelope and receipt digests use their separately owned exact projections. This domain payload does not add exclusions to those envelopes.

Malformed JSON, duplicate members, unresolved schema refs, digest mismatch or schema-invalid result cannot produce a passing mapping. Later executable validation must assert the governed date-time formats and other relevant schema constraints, not merely parse JSON.

### 10.2 Domain validation payload

The immutable payload must bind:

1. Validation identity, domain contract ID/version/ref/digest, result-schema identity/version/ref/digest and exact mapping/postcondition revision.
2. Action rule and manifest bindings, complete intent and schema refs/digests, extractor identity/digest and complete derived-view digest.
3. The proposed result ID/ref, complete bytes or reconstructible content reference, whole-result digest, and exact one-member domain write set.
4. Exact source family/ID and source-record digest; source-schema binding; shared-artifact kind, logical identity and immutable revision/digest; the role/posture of every input; and typed scope, tenant, twin and sovereignty proof bindings/dispositions as applicable.
5. The exact prospective finalization-evidence ref/digest admitted by final authorization, final decision-bundle binding, authenticated human-principal proof, deciding-Party path/basis, self/representation posture, representation proof where required, trusted human-act time and independent requesting-principal provenance.
6. Final snapshot/attempt identity and the relevant state, complete absence/uniqueness, and write-set guard bindings. Challenge and final snapshot/equal relevant-state bindings are reached through the exact finalization evidence, not replaced by a result-local snapshot.
7. One entry for each section 6 mapping and section 9.1 postcondition: stable ID, exact source/destination selector bindings, source value or verified value digest where appropriate, permitted transformation, disposition, and bounded diagnostic detail.
8. Domain event-family and record commit-class values; overall domain disposition; required inputs that were unavailable; and dependency edges explaining any unevaluated check.

The human approval/display bindings must preserve the exact grant/artifact, effective instant, reason and scope covered by the intent and required representation policy. This contract does not add a renderer or decide retention duration. If existing display/finalization evidence cannot bind the necessary facts faithfully, report that separate evidence boundary rather than claim that a boolean proves what the person saw.

The payload belongs to the domain validation trace named by the common handoff and governed-effect receipt. It is not a second authority registry or independent audit database. The governed receipt links the result digest to the exact intent, contract, validation trace, finalization evidence and atomic set. The result has no new backlink field, so any consumer claiming full contract validity must resolve that complete immutable association. An opaque record ID or isolated result JSON cannot support the stronger claim.

### 10.3 Truthful dispositions and reconstructibility

Every fixed mapping and postcondition is required. Overall `PASS` requires all of them to pass and every required dependency to be present and proved. A failed comparison is `FAIL`; a check whose required input is unavailable is `NOT_EVALUATED`, with that dependency recorded. Neither permits a successful handoff. Overall disposition is `FAIL` if a definite domain failure is established; otherwise it is `NOT_EVALUATED` while required checks cannot run; otherwise it is `PASS`. There is no overall `NOT_APPLICABLE` for this state-affecting action.

If ingress, authorization or finalization admission fails before this gate can run, do not fabricate a domain evaluation or its trusted input bindings. The owning rejection/attempt evidence records only established facts. An unavailable contract cannot certify a trace under itself; the outer handoff rejects it, and any failure evidence follows its separately available governed profile.

Only subordinate conditional proof checks may use `NOT_APPLICABLE`, with the contract-defined branch proved: representation-proof applicability for an authenticated self-action, or a twin-specific proof when the selected governing resource contract explicitly declares twin inapplicable. The branch-selection and required-absence checks still pass explicitly. A missing input, unknown branch, omitted mapping or failed format check is never not-applicable.

Before commit, all bytes needed to establish a required claim must be available under their exact bindings. Later reconstruction claims depend on the governed retention/proof-strength posture. A remaining digest may verify supplied candidate bytes but cannot be advertised as reconstructing deleted or unavailable evidence. No reconstruction limitation rewrites an earlier receipt or authorizes new effects. Retention, encryption, deletion, redaction and key custody remain #14 work.

Keep content addressing acyclic: finalization evidence exists prospectively before final authorization; the result and domain trace bind the admitted evidence; the final receipt binds those objects and the atomic set. The precommit trace must not hash the future receipt back into itself. Logical operation/attempt identifiers may link stages without inventing mutual digest references. If later shared envelope bytes cannot support this ordering, stop for their owning amendment.

## 11. Fresh-approval transaction handoff and failure behavior

Use PR #20 unchanged. The domain-specific integration is:

1. The common protocol binds the exact logical operation, requester, intended human approver, intent, reservation generation and challenge/display before the human act. The reservation is not authority or a lease held through human think time.
2. After the exact trusted act, a short finalization transaction rechecks all current inputs and guards, the independent human path, both relevant-state projections and complete cutoffs. It constructs the complete prospective approval evidence before the final authorization evaluation; the final evaluation must return the identical candidate requester basis and validity window.
3. Only after that final authorization and required finalization disposition pass, construct `R` from the bound inputs and apply this domain gate and every other applicable EnforcementChain gate. A reservation, raw act or preliminary authorization does not authorize `R`.
4. Hand off `B`, exact intent/schema, complete result bytes/digest, source inputs and guards, the full mapping/postcondition trace, overall `PASS`, and domain classification. The common transaction gate checks the handoff's completeness and bindings without implementing a second field mapper.
5. Recheck complete state/deadline/uniqueness guards and commit the exact success set atomically: final authorization evidence, the previously prospective finalization evidence, one decision consumption, one approval consumption, one exact-generation reservation-success terminal record, one RevocationDecision, domain and other gate traces, and one governed-effect receipt. Stage-one challenge/display/reservation history is referenced, never rewritten.

There is no outbox or external dispatch for this action. Any additional domain effect not admitted by this one-record contract prevents this handoff from passing; proposing it requires its separate contract/composition boundary.

An intent/result mismatch is a domain failure and commits no revocation or consumption. If authorization already returned `ALLOW`, that remains its truthful outcome; the domain gate records its own failure. Do not translate a domain failure into an authorization denial or invent a public reason code. Use PR #20's failure table to distinguish invalidated intent/state from a retryable construction/persistence failure and to record the correct reservation consequence. Do not declare every failure retryable or invalidate every unchanged-intent failure.

An exact retry first looks up the authoritative operation/attempt state. A committed match returns its receipt without a new record or consumption. A conclusively rolled-back eligible attempt repeats every required check; it may reuse the exact act only where PR #20 permits, while all prospective approval/decision/validation evidence is rebuilt for the new attempt. Uncertain commit stays `OUTCOME_UNKNOWN` with no reapplication until authoritative reconciliation. A partial success set is an invariant breach for separately governed repair, not permission to synthesize missing proof or delete the grant/result.

## 12. Positive and hostile case specifications

These are design cases for later production-reachable conformance, not implemented or executed fixtures. The harness must enter the real rule-selected command/finalization path, observe authoritative records/receipts and failures, and distinguish domain from neighboring gates. A standalone constructor returning JSON does not satisfy them.

| Case | Stimulus | Required result and owner |
|---|---|---|
| `SR-T01` | Valid direct natural-person request through the fresh-approval lifecycle; exact grant/artifact, string reason, scope and time | One exact RevocationDecision, all mappings/postconditions pass, complete atomic receipt; no grant edit |
| `SR-T02` | Valid authorized represented-human approver for an agent request | Human path supplies deciding Party; exact human and requester remain separately bound; no sponsor shortcut |
| `SR-T03` | Exact authorized future `effectiveFrom` | Record that exact instant; no claim that merely saving it immediately ended current access |
| `SR-T04` | Scheduled bound instant passes before an otherwise valid final commit, or exact eligible retry occurs | Do not rewrite `effectiveFrom` or `decidedAt`; repeat common current checks; preserve actual commit time and history |
| `SR-T05` | Retry after success response was lost | Common protocol returns the original complete receipt; no additional record or consumption |
| `SR-T06` | Change action, affected family, mode or contract/schema binding | Ingress/authorization/handoff rejection as appropriate; no broader action or result |
| `SR-T07` | Another SharingGrant ID, changed source bytes under the same ID, or wrong source digest | Exact source/intent binding fails; no result |
| `SR-T08` | Same artifact logical ID but different immutable revision, wrong artifact kind, `OTHER`, or multiple targets/grants | Typed target/input or domain cross-binding fails; no result |
| `SR-T09` | Grant passed as authority target or as the permission to revoke | Rule/resource or authority gate rejects; domain gate cannot repair the missing authority |
| `SR-T10` | Same opaque IDs in another tenant, wrong twin, caller scope, truncated scope or inferred ancestor | Required proof or `SR_PC_SCOPE` fails; no result |
| `SR-T11` | Substitute result ID, overwrite an existing ID, or race a conflicting result reservation | Mapping/guard rejects; at most the admitted exact operation can commit |
| `SR-T12` | Rewrite reason, omit notes, append generated text, serialize a structured reason, or alter any mapped time | Exact field mapping fails; do not coerce values to make them pass |
| `SR-T13` | Set either forbidden optional array, even to empty, or encode a narrowing/replacement effect outside the exact result | Required-absence/write-set checks fail; no partial termination or implicit replacement |
| `SR-T14` | Populate deciding Party from the requester agent, sponsor, grantor or another human rather than the eligible approver path | `SR_PARTY` / human binding fails |
| `SR-T15` | Right Party string with wrong human principal, representation proof, act or trusted-time source | Human/finalization proof fails; bare Party equality is insufficient |
| `SR-T16` | Agent approval boolean, ineligible sponsor, synthetic direct-human mode or omitted challenge | Common authorization/finalization gate rejects; domain construction cannot turn it into approval |
| `SR-T17` | Changed grant/target/representation/policy/display or relevant-state digest after challenge | Common protocol invalidates the stale generation; no effect even if a fresh evaluation might otherwise allow |
| `SR-T18` | Unrelated history advances but rule-owned relevant projection and full transaction guard remain valid | Do not invent a domain-wide history-equality rule; complete normal checks determine success |
| `SR-T19` | Missing intent/source/display/evidence bytes, digest mismatch, or “not applicable” used for unavailable proof | No passing handoff; truthful failure/unevaluated dependencies and proof-strength claim |
| `SR-T20` | Missing mapping/postcondition, unsupported branch or schema/date-time format failure | No passing handoff; absence checks cannot be skipped |
| `SR-T21` | Edit/delete/relabel the grant, change prior receipts/history, or apply the revocation to another replacement ID | Domain write-set or exact-source checks fail; preserve history and independent source IDs |
| `SR-T22` | Classify the result as authorization audit evidence, fabricate a companion event, or create current state/outbox/notification | Classification or one-result write-set check fails; no unbound consequence |
| `SR-T23` | Change `R` after successful validation | Whole-result digest/write-set guard fails before commit |
| `SR-T24` | New relevant state, result collision, expiry or serialization conflict occurs after checks | Common final guard prevents commit; no stale `PASS` reuse |
| `SR-T25` | Authorization is `ALLOW` but a domain mapping fails | No revocation/consumption; retain truthful authorization outcome and separate domain failure |
| `SR-T26` | Result construction fails with unchanged eligible intent/state, then an exact eligible retry | PR #20 determines reservation consequence; new attempt repeats checks and rebuilds prospective evidence |
| `SR-T27` | Concurrent finalizers or reused approval/decision try to commit twice | Common consumption/identity guards admit at most one exact success; loser cannot borrow it |
| `SR-T28` | Persistence failure, lost commit acknowledgement or visible partial success set | Atomic rollback or authoritative reconciliation; unknown is not retry permission and partial visibility is not success |
| `SR-T29` | Another independent source still permits access, or a different replacement ID was separately issued | Do not claim all access ended or extend termination by lineage; actual access remains a separate current authorization decision |
| `SR-T30` | Later retrieval has only a digest after governed loss/deletion of evidence bytes | Keep immutable historical receipt; qualify reconstruction honestly; no invented bytes or new authority |

The approval/freshness/concurrency/recovery cases are integration obligations to the existing owners, not authorization to add their implementations to this domain PR.

## 13. Traceability to issue #27

| Issue criterion | Candidate closure | Key cases |
|---|---|---|
| 1: exact action/family/mode | Sections 1, 5 and 6 | T01, T06, T13 |
| 2: authority target versus affected grant | Sections 5.2-5.3 and 9 | T07-T10 |
| 3: complete result-field mapping | Sections 6-7 | T11-T15 |
| 4: missing proof outside unchanged v0.1 carrier | Sections 4 and 10 | T19, T30 |
| 5: append-only exact-source semantics | Sections 8-9 | T21, T29 |
| 6: trusted time and prospective history | Section 7.2 | T03-T04, T12, T21 |
| 7: event/commit classification | Section 8 | T22 |
| 8: immutable truthful validation trace | Sections 9-10 | T19-T20, T23 |
| 9: validation before atomic commit; no outcome rewriting | Section 11 | T16-T18, T24-T28 |
| 10: positive and hostile specifications | Section 12 | T01-T30 |
| 11: exact future bindings, stages and approval | Sections 2-3, 10 and 14-16 | Binding review and one-file scope test |

`Tnn` in this table abbreviates `SR-Tnn`. Later implementation must add invariant-to-code-to-test evidence in its own PR; this Phase A table is not executable coverage.

## 14. Remaining materialization and delivery gates

| Gate | Current status and required later evidence |
|---|---|
| Exact PR #11 semantic dependency | Approved candidate at the pinned head; remains draft/unmerged and not promoted |
| This domain semantic profile | Review and exact-head semantic approval pending |
| Human transaction semantics | Approved PR #20 candidate at the pinned head; its concrete policy/evidence/runtime bindings are not materialized by this PR |
| Domain contract unit | Exact schema selectors/pointers, digest profiles, conditional checks, validation-payload bytes, non-default contract and examples still required |
| SharingGrant v0.2 source | Separate source-bundle bytes, artifact-revision relationship proof and exact issuance/rule/source digest bindings still required; current v0.1 is not a substitute |
| Intent, policy and manifest | Rule-selected exact intent schema, extractor/projection, protected-effect binding and real immutable manifest remain separate authorization-law work |
| Shared evidence and retention | Finalization/receipt/trace envelopes and exact #14 proof-strength/retention bindings remain separately owned |
| Event ingress or companion composition | This candidate admits no companion domain result; any selected runtime path needing one must provide its separately governed classification/contract/composition before it can execute |
| Accepted law, conformance, currentness and extraction | Follow PR #11 section 24 and #21; no executable or production-readiness claim from a semantic candidate |

Semantic review of this proposed interface may proceed now. Executable binding review cannot pass using placeholder digests or unavailable source/evidence contracts. Drafting one artifact does not imply that its dependencies have been materialized or reviewed.

Preserve PR #11's staged order: adjacent contract work; separate policy-bundle draft; separate source-bundle draft; bounded evidence drafts; exact binding review and accepted law; hostile conformance; explicit current/default promotion; byte-identical OFARM2 extraction; separately authorized OFARM2 runtime work. If exact cross-bindings cannot be closed in that sequence, report the dependency conflict for its owner; do not silently reorder stages or activate a partial rule set.

Approval of this candidate addresses only this sharing-revocation family design. It does not complete parent #12, authorize the other missing effect families, close #14/#21, or unblock OFARM2#353 on its own. No existing approved candidate PR is changed here.

## 15. Steward approval card

Decision ID: `OFARM-ISSUE27-SHARING-REVOCATION-PROTECTED-EFFECT-001`

Version: `1`

Requested approval: the semantic choices in this Phase A file at its exact reviewed commit, not implementation or promotion.

| Decision | Proposed answer |
|---|---|
| One action, one new immutable RevocationDecision, exact SharingGrant and `TERMINATE` only? | Yes |
| Preserve current RevocationDecision v0.1 and prove omitted bindings through the complete intent/evidence/receipt association? | Yes; stop if the owning future evidence contracts cannot express it |
| Keep the shared artifact as the only authority target and the grant as a state input? | Yes |
| Use the independently eligible human approver's authority-subject Party, with the authenticated human and requester separately proved? | Yes |
| Copy trusted human-act time to `decidedAt`, preserve exact `effectiveFrom`, and prohibit backdated commit/history rewriting? | Yes |
| Copy the exact reason string to required notes; require both optional action/replacement arrays absent? | Yes |
| Classify the act as GovernanceEvent and the record as governance decision, without automatic event/consequence creation? | Yes; this explicit application of existing categories requires review |
| Require all fixed mappings/postconditions to pass, permitting not-applicable only for proved subordinate branches? | Yes |
| Require exact validated bytes and complete common fresh-approval success set to commit together? | Yes |
| Keep domain failure distinct from authorization, transaction failure and uncertain commit? | Yes |
| Preserve grants, independent access paths, replacement IDs, historical decisions and delivered-data history? | Yes |
| Leave all source, authorization, transaction, retention, shared-evidence, currentness and runtime changes to separate governed work? | Yes |

Any change to action eligibility, the immutable-source model, narrowing, scope interpretation, generic temporal law, human-approval protocol or top-level classification requires its owning review. It cannot be accepted implicitly by editing this card.

## 16. Verification and Phase A completion

For this design-only change, verify the diff contains only this candidate, inspect its complete mappings and traceability, confirm pinned source/schema bytes, and run the applicable repository hygiene/currentness/steward checks. No production command, PostgreSQL test, new machine fixture or effect validator is implemented by this PR. Historical phase reports are outside the current/default manifest lane; do not add this candidate to accepted/current indexes just to make it discoverable.

Read-only checks from the candidate worktree after committing its reviewed contents:

```sh
git diff --name-only 71ca724a8b6ec23f1655b086a6f549496d10a47f HEAD
git diff --check 71ca724a8b6ec23f1655b086a6f549496d10a47f HEAD
python3 -B package_meta/tools/validate_repo_hygiene.py
python3 -B package_meta/tools/check_generated_currentness.py
python3 -B package_meta/tools/check_repository_cross_references.py
python3 -B package_meta/tools/check_repository_steward_guardrails.py
```

The name-only diff must contain only this Phase A file. Separately inspect that all twelve schema properties have exactly one mapping, all nine fixed postconditions are required, and case IDs `SR-T01` through `SR-T30` are unique and complete. These static checks cannot prove the proposed semantics or substitute for focused review and later executable hostile conformance.

Phase A completes only after focused review and semantic approval of the exact candidate head, with no unresolved design blocker hidden as a passing prerequisite and with the one-file trust-boundary scope intact. Later machine materialization must prove exact selectors, field coverage, dispositions and real bindings, then execute the specified positive/hostile cases through separately authorized runtime paths.

What is next: review the exact candidate, especially the human-path Party mapping, unchanged-carrier evidence association, literal reason mapping, temporal claims and governance classification, before considering semantic approval.
