# OFARM AssertionRecord Submission Protected-Effect Contract v0.1

Date: 2026-09-03<br>
Status: Phase A candidate for `samovers/OFARM#22`; non-authoritative, not accepted law, and not a current/default machine contract<br>
Parent inventory: `samovers/OFARM#12`<br>
Depends on: the approved authorization candidate on issues #16 and #18 / PR #11 at `03a21f669ee04f96d444e14f00ae7212cab04803`, and the approved governed human-approval transaction candidate on issue #19 / PR #20 at `98f8c4fafbae42c8f7fd931f43f53adcb4733713`<br>
Blocking prerequisite: PR #20 closes the shared transaction protocol only for fresh approval and direct human final action; `ASSERT_OPERATION_CLAIM` remains non-executable until a separate transaction profile closes the `NOT_REQUIRED` finalization mode selected by PR #11<br>
Scope: define the AssertionRecord-specific mapping from one authorized assertion-submission intent to one immutable pending-review AssertionRecord

---

## 1. Decision requested

Stewards are asked to approve, reject, or amend these bounded decisions:

1. this contract validates exactly one new `AssertionRecord` for `ASSERT_STRUCTURE`, `ASSERT_OPERATION_CLAIM`, or `ASSERT_COMPLIANCE`;
2. the action fixes the result subtype: `STRUCTURE_ASSERTION`, `OPERATION_CLAIM_ASSERTION`, or `COMPLIANCE_ASSERTION` respectively;
3. every result created through these submission actions has `claimState` exactly `PENDING_REVIEW`;
4. fresh approval for structure or compliance authorizes submission of the exact assertion only; it does not accept the claim or make it current truth;
5. the result preserves the exact proposed ID, typed subject, sole authority-bearing anchor scope, asserting Party, governed assertion-act time/posture, closed subject-time profile, typed body, evidence, optional correction lineage, and branch-specific provenance or compliance basis;
6. for an operation claim, the current reporter remains separate from the alleged performer and performer authority remains `NOT_EVALUATED_BY_AUTHORIZATION`;
7. the result records have commit classes `STRUCTURE_ASSERTION`, `OPERATION_CLAIM`, and `COMPLIANCE_ASSERTION`; assertion action or subtype never derives a primary event family;
8. when an ingress path associates a governed semantic event, the contract consumes its exact immutable `SemanticEventEnvelope` binding and separately validated primary family, checks assertion-specific subject/scope/time compatibility, and records the association only in the protected-effect trace; without such a binding this contract makes no event-family claim;
9. a correction is a new pending-review assertion carrying one optional exact immutable `supersedesAssertionRecordBinding` to a prior assertion that passes the closed same-context predicate in section 5.5; it never edits, deactivates, accepts, or replaces the prior assertion by itself;
10. this contract creates no accepted structural state, accepted executed intervention consequence, compliance fact, ReviewDecision, SemanticEventEnvelope, current-state materialization, or mutation of prior history;
11. a narrow future `AssertionRecord v0.2` carrier is required because v0.1 cannot carry immutable subject, scope, evidence, body, temporal, lineage, and branch-specific bindings without relying on a competing sidecar description; and
12. a mapping or postcondition failure aborts the assertion effect without rewriting the prior authorization result.

The active Event Grammar owns primary event-family classification through the dominant-semantic-consequence rule. Existing active support records demonstrate that an `operation claim` may belong to either an `InterventionEvent` or `MaterialEvent`, and that a `compliance assertion` may be one of the commit classes emitted under `OccurrenceEvent`, `EvidenceEvent`, or `GovernanceEvent`. This contract therefore fixes only the AssertionRecord commit class and consumes any event classification from the separate Event Ingress boundary.

Approval of this candidate authorizes no schema, runtime, currentness, accepted-RFC, or promotion change.

---

## 2. Primary trust boundary and PR boundary

The primary trust boundary is **AssertionRecord submission semantics and commit classification**.

This candidate owns only:

- the v0.1 capability/gap inventory and minimum future carrier delta;
- the exact action-to-assertion-subtype mapping;
- exact intent-to-result mappings and permitted derivations;
- assertion-specific actor, temporal, subject, scope, evidence, and branch constraints;
- optional immutable correction lineage that creates a new assertion without changing prior history;
- assertion-specific compatibility checks for an optional separately governed semantic-event binding;
- assertion-specific forbidden widening and postconditions;
- separation of a semantic event, the submission act, and the committed assertion record; and
- the AssertionRecord-specific payload of the protected-effect validation trace.

This PR adds only this candidate in the historical phase-report lane. It does not own or change:

- authorization, grants, delegation, actor resolution, sharing, or revocation;
- generic transaction coordination, approval, finalization evidence, consumption, receipts, retention, encryption, or key custody;
- review, acceptance, later review decisions, current-state supersession, accepted-consequence, or current-state semantics;
- generic event ingress, primary event-family classification, Event Grammar vocabulary, or a SemanticEventEnvelope contract;
- assertion body vocabularies for every domain or pack;
- current schemas, accepted RFCs, machine manifests, current/default indexes, runtime implementation, or currentness; or
- OFARM2 implementation.

If implementation needs a new authorization target, action, effect-intent field that changes eligibility, event family, commit class, transaction mode, review effect, evidence-retention rule, or current-state rule, work stops before that boundary and proceeds through a separate issue and PR.

---

## 3. Governing inputs and stop conditions

This candidate is constrained by:

- Constitution RC2.1 sections 7.24 through 7.25, 10.1 through 10.3, 10.10a, and 10.11;
- the accepted Source Truth Record Closure RFC v0.1;
- the Event Grammar and Commit Matrix v0.1;
- the accepted Event Ingress and Promotion Boundary Closure RFC v0.1;
- the Temporal Field Conformance Matrix v0.1;
- the accepted Quantity-Bearing Intervention and As-Applied RFC v0.1;
- current `AssertionRecord v0.1` and its ten repository examples;
- the protected-effect inventory on issue #12;
- the approved PR #11 action rows, exact effect-intent profiles, one-target `RP_SCOPE_ONE` resource policy, authority-subject semantics, and protected-effect handoff at `03a21f6`; and
- the approved PR #20 transaction protocol at `98f8c4f`, only for the finalization modes it actually covers.

The exact PR #11 head authorizes assertion submission and binds the whole effect intent. It does not authorize acceptance or define this result. A semantic change to that head invalidates this candidate's authorization dependency before schema or executable-contract materialization.

The materialization step must stop and return to a separate boundary when any of these conditions is found:

- the exact result cannot be built from one validated, digest-bound effect intent plus trusted transaction facts;
- an assertion subject or body field changes authorization eligibility but is absent from the approved authorization-relevant field set;
- the sole `RP_SCOPE_ONE` target cannot map completely to one immutable result anchor scope;
- a requested assertion body needs another result family or an implicit accepted consequence;
- a linked semantic event lacks a separately passing Event Ingress classification or cannot be checked for subject/scope/time compatibility without changing Event Ingress law;
- generic evidence, retention, approval, or transaction machinery must change; or
- the `NOT_REQUIRED` transaction path for `ASSERT_OPERATION_CLAIM` remains unclosed.

This document may identify those dependencies. It cannot repair them locally.

---

## 4. Current `AssertionRecord v0.1` inventory

### 4.1 Capabilities and gaps

| Current field or behavior | v0.1 capability | Gap and Phase A disposition |
|---|---|---|
| `schemaVersion` | identifies `ofarm.assertionrecord.v0.1` | future carrier needs a distinct `ofarm.assertionrecord.v0.2` branch |
| `assertionRecordId` | stable logical assertion ID | retain and bind exactly to the prospective effect subject and result digest |
| `assertionType` | six assertion subtypes | `NARROWING`: this contract admits only structure, operation-claim, and compliance results |
| `subject` | one type and logical ref | retain logical identity and add explicit existing/prospective posture plus an immutable selector for an existing subject |
| `anchorScopes` | one or more type/ref pairs | `NARROWING`: close new v0.2 submissions to exactly one immutable authority-bearing anchor from `RP_SCOPE_ONE`; preserve other context in typed subject/body bindings and relationship proofs |
| `assertedByPartyRef` | accountable asserting Party | retain and bind to the selected path-specific authority subject, not an approver or alleged performer |
| `assertedAt` | one date-time | retain as assertion-act time and bind to the exact governed assertion-act source in section 6; never substitute record/commit time |
| `occurrenceTime`, `effectiveFrom`, `effectiveUntil` | optional flat temporal fields | replace for new v0.2 results with the closed tagged `subjectTime` profiles in section 6.4; do not guess a legacy projection |
| `evidenceRefs` | one or more logical refs | replace with a non-empty array of immutable typed evidence bindings |
| `provenanceRefs` | optional logical refs | replace loose provenance with branch-specific immutable bindings; do not preserve an untyped catch-all array |
| `claimState` | five postures, including `PENDING_REVIEW` and `IN_FORCE` | fix new results from these submission actions to `PENDING_REVIEW` |
| `supersedesAssertionRecordRef`, `supersededByReviewDecisionRef` | optional logical lineage | replace the former with an optional immutable `supersedesAssertionRecordBinding` allowed only for correction posture; keep the later-review field absent at submission |
| `benefitingPartyRef` | optional Party ref | require absence unless a future digest-bound domain amendment defines its exact meaning and mapping |
| `notes` | arbitrary optional prose | replace with the exact typed assertion body; no result-local notes side channel |
| payload ref arrays | optional loose intervention/execution refs | permit only exact immutable payload bindings inside the typed operation-claim body |
| tenant/twin and finalization metadata | absent | keep authorization-only tenant/twin, challenge, approver, and finalization details in authorization/finalization evidence and the receipt rather than duplicating them in domain truth |
| classification and integrity | absent | bind the fixed record commit class plus schema, contract, result, and trace digests; consume optional event family only from a separately validated semantic-event binding |

### 4.2 Example coverage

The repository has ten current `AssertionRecord v0.1` examples:

- one structure assertion, in `PENDING_REVIEW`;
- five operation-claim assertions, one in `PENDING_REVIEW` and four in `IN_FORCE`;
- three compliance assertions, two in `PENDING_REVIEW` and one in `IN_FORCE`; and
- one `LOT_ASSERTION`, in `IN_FORCE`, which is outside this contract.

All ten use `notes` as at least part of the human-readable claim content. All use logical evidence refs, six use logical provenance refs, and one operation claim uses a loose `executionRecordPayloadRefs` entry. That late-sync operation claim also carries both field and crop-cycle anchors. No example carries an immutable subject selector, exact body schema binding, effect-intent digest, or protected-effect trace.

The existing `IN_FORCE` examples remain valid v0.1 history. They are not retroactively relabeled, rejected, or used as precedent for direct in-force creation under v0.2.

### 4.3 Carrier decision

A narrow future `AssertionRecord v0.2` carrier is required. A sidecar around v0.1 would leave the history-bearing assertion unable to state the exact body, subject and scope revisions, subject time, evidence revisions, and operation/compliance branch facts that the sidecar claims to validate.

The future carrier is a versioned extension. Existing v0.1 records remain valid v0.1 history and do not silently acquire v0.2 proof strength. No schema is created or edited in this PR.

---

## 5. Minimum future `AssertionRecord v0.2` carrier

### 5.1 Common fields

| Field | Required meaning |
|---|---|
| `schemaVersion` | exactly `ofarm.assertionrecord.v0.2` |
| `assertionRecordId` | exact proposed assertion ID |
| `assertionType` | exact action-derived subtype from section 7 |
| `subject` | exact typed logical subject with `EXISTING_SUBJECT` or `PROSPECTIVE_SUBJECT` posture and section 5.2 selector rules |
| `anchorScopes` | exactly one immutable scope binding copied from the sole `RP_SCOPE_ONE` `TARGET_SCOPE` |
| `assertedByPartyRef` | exact selected path-specific `authoritySubjectPartyRef` |
| `assertedAt` | exact governed assertion-act time from section 6.2, distinct from record/commit time |
| `assertionActPosture` | exactly `TRUSTED_ONLINE_SUBMISSION` or `VERIFIED_OFFLINE_SUBMISSION` |
| `assertionActEvidenceBinding` | required only for verified offline submission and absent for trusted online submission |
| `subjectTime` | exact closed tagged domain-time value from section 6.4 |
| `assertionBody` | exact action-typed body copied from the validated intent; its absolute `/assertionBody/assertionPosture` child is exactly `INITIAL` or `CORRECTION` |
| `evidenceBindings` | non-empty array of exact immutable evidence bindings copied from the validated intent |
| `subjectScopeProofBindings` | exact immutable relationship-proof bindings when subject-to-anchor equality alone does not establish the relationship; otherwise required absent |
| `claimState` | exactly `PENDING_REVIEW` |
| `supersedesAssertionRecordBinding` | required only for `CORRECTION`, otherwise absent; section 5.5 |
| `operationClaimContext` | required only for `OPERATION_CLAIM_ASSERTION`; section 5.3 |
| `complianceBasis` | required only for `COMPLIANCE_ASSERTION`; section 5.4 |

Every object and branch rejects unknown properties. A field not admitted by its branch is absent, not `null`, empty, or populated with a placeholder.

The materialized contract binds one exact body-schema ref/version/digest for each assertion subtype. The review keys are `STRUCTURE_ASSERTION_BODY_V0_2`, `OPERATION_CLAIM_BODY_V0_2`, and `COMPLIANCE_ASSERTION_BODY_V0_2`; they are not mutable runtime registry entries and this candidate does not create their bytes. Every branch closes the common absolute `/assertionBody/assertionPosture` discriminator before adding branch-specific content. Within a schema whose root is the body object, `/assertionPosture` is explicitly a body-root-relative pointer to that same field, never a second top-level field.

### 5.2 Immutable binding and subject rules

An immutable binding contains one logical ref and exactly one immutable revision ref or `sha256:` content digest. Its exact kind is fixed by the containing field or an explicit closed kind discriminator. Every revision ref must resolve to immutable bytes, and the validation trace records the digest of those bytes.

`subject` has two closed postures:

| Posture | Required content and meaning |
|---|---|
| `EXISTING_SUBJECT` | exact `subjectType`, `subjectRef`, and exactly one immutable revision ref or content digest |
| `PROSPECTIVE_SUBJECT` | exact `subjectType` and proposed `subjectRef`; no revision/digest selector; the assertion records a claim about the proposed subject but does not create it |

The action-bound body schema closes the permitted `subjectType` values. This candidate does not enlarge the current domain vocabulary or let a caller supply an unregistered type. A prospective subject cannot be represented as existing, and an assertion about it cannot create durable identity or structural current state.

`NARROWING`: `AssertionRecord v0.1` permits one or more anchor scopes; this proposed v0.2 submission branch permits exactly one because all three approved action rows select `RP_SCOPE_ONE`, whose sole `TARGET_SCOPE` has cardinality one. The entry carries the exact scope kind, logical ref, and one immutable selector from the validated resource view. No ancestor, descendant, tenant, deployment, or convenient display scope may be added as a second authority-bearing anchor.

The narrowing must not discard claim context. A claim that needs field, crop-cycle, operation, lot, or other context represents it through:

- the one authority-bearing anchor selected by `RP_SCOPE_ONE`;
- the exact typed `subject`;
- immutable context bindings inside the selected typed `assertionBody`; and
- `subjectScopeProofBindings` that prove every required relationship.

The body-schema branch closes the permitted context roles, kinds, and cardinalities. Those contextual bindings grant no additional authority and do not become extra anchors. If a valid assertion represented by v0.1's multi-anchor form cannot be carried losslessly through these four elements, v0.2 materialization stops rather than dropping context or flattening multiple anchors into one.

When subject and anchor scope do not have the same exact identity and immutable revision, the validated intent must supply the complete immutable relationship proof selected by the action-bound body schema. The contract validates that relationship without treating it as another authority target. If the relationship cannot be proven, the assertion does not commit.

### 5.3 Operation-claim context

`operationClaimContext` contains:

- `claimPosture`, exactly `INTENDED` or `PERFORMED` as bound by `EI_OPERATION_ASSERTION_V0_2`;
- required `performedByPartyRef`, copied exactly from the intent and retained as claim provenance;
- `softwareAgentActorshipBindings`, required and non-empty only when `claimPosture` is `PERFORMED` and the claim alleges software-agent performance, otherwise absent; and
- `performerAuthorityEvidenceBindings`, optional only for `PERFORMED`, otherwise absent.

Each binding is immutable under section 5.2. Optional performer-authority evidence is evidence claimed by the reporter; its presence is not an authorization result and its absence cannot be filled from the reporter's path.

For `INTENDED`, the upstream-required `performedByPartyRef` identifies the Party named to perform the intended work; it does not assert that performance occurred. For `PERFORMED`, it identifies the alleged performer. The field name cannot upgrade either claim posture.

The current authorization path answers only whether the reporter may submit the operation claim. The selected `authoritySubjectPartyRef` maps to `assertedByPartyRef`; it never maps to `performedByPartyRef`. The authorization trace records performer authority as `NOT_EVALUATED_BY_AUTHORIZATION`. Evidence sufficiency, review, and promotion decide whether any claimed performance may later yield an accepted execution consequence.

An operation body may include intervention-intent or execution-record payload bindings only as exact immutable bindings covered by `effectIntentDigest`. A loose ref, latest-version lookup, or payload inserted after authorization fails.

### 5.4 Compliance basis

`complianceBasis` contains two non-empty arrays copied exactly from `EI_COMPLIANCE_ASSERTION_V0_2`:

- `ruleRevisionBindings`; and
- `evidencePolicyRevisionBindings`.

Each entry is immutable under section 5.2. The bound rules and policies identify what the assertion claims against; they do not prove that the claim is correct, that required evidence passed, or that a compliance fact exists.

Compiled outputs may be immutable evidence or intent inputs. They cannot replace `assertionBody`, select a different claim, or become the result. `EP_COMPLIANCE_ASSERTION_V0_2` remains a separately owned action evidence policy; this contract consumes its applicable gate disposition without copying that policy's evaluation rules.

### 5.5 Correction lineage

Every selected body schema requires absolute intent and result pointer `/assertionBody/assertionPosture` with one of two values. In body-schema-relative notation only, the same field is `/assertionPosture`:

| Posture | Lineage rule |
|---|---|
| `INITIAL` | `supersedesAssertionRecordBinding` is absent |
| `CORRECTION` | exactly one `supersedesAssertionRecordBinding` is required |

The correction binding at absolute intent and result pointer `/supersedesAssertionRecordBinding` contains one logical prior-assertion ref and exactly one immutable revision ref or `sha256:` content digest under section 5.2. It is present in the validated intent, covered by `effectIntentDigest`, resolved as an actual supported `AssertionRecord`, and copied exactly to the result.

For `CORRECTION`, `AR_CORRECTION_LINEAGE` applies one closed correction-target compatibility predicate. Every condition below must pass:

1. **Existing distinct prior record:** the authoritative transaction-start snapshot and its history watermark prove that the exact bound prior record was already committed at a canonical-history position included in that snapshot. The prior and proposed assertion IDs differ. A self-reference, unresolved or merely prospective reference, concurrent record absent from that starting snapshot, or timestamp-only claim of prior existence fails.
2. **Same subtype:** the prior and new records have exactly the same `assertionType`.
3. **Same governance boundary:** the current intent's rule-selected authorization view and the prior record's immutable creation or ingress evidence resolve to the same typed tenant or deployment boundary, including exact boundary kind and logical ref, and to the same applicable twin. Twin presence and value must match; absence is permitted only when the governing action profile makes twin context inapplicable to both records.
4. **Same authority anchor:** for a prior v0.2 record created under this profile, the new sole anchor equals the prior sole authority-bearing anchor in kind, logical ref, and immutable selector. For a prior v0.1 record, the new anchor's kind and logical ref equal one recorded prior `anchorScopes` entry directly; ancestor, descendant, alias, inferred-equivalence, or cross-scope matching is prohibited.
5. **Same logical subject:** prior and new `subjectType` and `subjectRef` are equal. Subject revision may change as claim content, but correction posture cannot change the logical subject identity.
6. **Claim-lineage semantics only:** the edge states that the new assertion corrects the bound prior assertion. It creates no acceptance, rejection, deactivation, claim-state transition, review result, in-force change, or current-state replacement.

The prior record does not self-attest its governance context. For a v0.2 record created under this profile, the resolver uses the exact governed-effect receipt, its bound `effectIntentDigest`, and the rule-selected extracted governance view. A legacy v0.1 target requires equivalent immutable creation or ingress evidence binding its exact record digest, commit position, governance boundary, twin posture, and recorded anchor context. A current mutable storage location, caller-supplied tenant/twin label, opaque-ID convention, or inferred scope ancestry is not proof. Missing, ambiguous, mutable, or digest-invalid context evidence fails the correction rather than being guessed.

A submission that changes subtype, logical subject, authority anchor, tenant/deployment boundary, or twin is a new `INITIAL` assertion under this candidate, even when its body discusses earlier history. A broader correction-relation profile requires a separately reviewed contract revision; body-schema authors cannot widen this predicate independently.

A correction creates a new immutable `PENDING_REVIEW` assertion. Its lineage edge does not edit, delete, relabel, accept, reject, contest, deactivate, or replace the prior assertion in current state. `supersededByReviewDecisionRef` remains absent because it describes a later review effect, not a fact available at assertion submission. The legacy ref-only `supersedesAssertionRecordRef` is also absent from v0.2.

Correction posture, lineage, and target compatibility are governed AssertionRecord-domain facts. The compatibility check consumes the already selected authorization view and immutable prior-creation evidence as integrity inputs; it does not grant authority over the prior record or change authorization eligibility, the sole authority target, or the selected authority subject. If a future authorization rule needs to inspect correction lineage, PR #11 must be separately amended and approved before that rule or this contract is materialized.

### 5.6 Fields deliberately not copied

The result does not duplicate:

- `effectIntentDigest`, authorization rules, grants, roles, path candidates, or authority snapshots;
- tenant/twin authorization context that is not itself the assertion's typed subject or sole anchor scope;
- an agent sponsor, authenticated principal, human approver, challenge, display, finalization evidence, or consumption record;
- a generic provenance array, arbitrary notes, mutable URLs, or unversioned payload refs; or
- later-review backlinks, acceptance, in-force status, materialization, or currentness fields.

Those facts remain in their owning immutable evidence, receipt, intent, or downstream domain records. The governed-effect receipt and validation trace bind the assertion result back to the exact intent, authorization, contract, finalization mode, and transaction evidence without making the AssertionRecord a second authorization ledger.

---

## 6. Actor and temporal ownership

### 6.1 Asserting Party

`assertedByPartyRef` is the `authoritySubjectPartyRef` from the one canonical sufficient authorization path selected under PR #11:

- for natural-person self action, it is that person's Party;
- for represented action, it is the represented Party;
- for a directly granted agent action, it is the recognized agent Party; and
- for explicitly delegated agent action, it is the represented Party selected by that path.

A sponsor, human approver, authenticated principal acting in representation, alleged performer, benefiting Party, compiled-output author, or caller-supplied mirror cannot replace it.

For `ASSERT_STRUCTURE` and `ASSERT_COMPLIANCE`, PR #11 requires fresh human approval for every invocation. A direct natural-person invocation still uses the governed fresh-approval lifecycle; an agent path requires an independently eligible natural-person approver for the same exact action and effect intent through PR #20. The approver is not thereby the asserting Party, and the approval does not change `claimState`.

### 6.2 Assertion act and `assertedAt`

The future effect-intent schema carries these AssertionRecord-domain fields at exact top-level pointers:

- `/assertedAt`;
- `/assertionActPosture`; and
- conditional `/assertionActEvidenceBinding`.

They are all covered by `effectIntentDigest`. They do not alter authorization eligibility, the authority target, or the selected authority subject under this candidate.

The two postures are closed:

| `assertionActPosture` | Exact source rule |
|---|---|
| `TRUSTED_ONLINE_SUBMISSION` | the trusted runtime observing the authenticated assertion submission supplies `/assertedAt` before intent validation and digest calculation; a caller-authored timestamp is prohibited; `/assertionActEvidenceBinding` is absent |
| `VERIFIED_OFFLINE_SUBMISSION` | `/assertedAt` comes from the exact immutable `/assertionActEvidenceBinding`, which must bind the asserting Party or represented-Party basis, the exact submitted subject/scope/body/evidence content, the source timestamp, and the separately governed evidence/time-trust policy under which that timestamp is admitted |

For verified offline submission, the resolved act-evidence timestamp at `/assertedAt` must equal the intent and result `/assertedAt` string exactly. Its assertion content must equal the corresponding intent content; a merely similar body or ref-only claim is insufficient. The effect intent binds that pre-existing evidence record; the evidence record does not claim the later `effectIntentDigest` and therefore creates no digest cycle.

For fresh-approval actions, `humanActedAt` is approval/finalization time under PR #20, not the assertion-act source in this v0.1 contract. It may happen to equal `assertedAt`, but equality is only an observed fact; it is never derived merely because the approver approved an agent or represented-Party submission. A future contract that makes final affirmation itself the assertion act must define that posture explicitly in a separately reviewed revision.

`effectCommittedAt` remains the transaction linearization/record time in the governed-effect receipt. It never supplies `assertedAt`. If assertion and commit happen at the same instant, both independently sourced fields retain their meanings.

### 6.3 Canonical time representation

Every timestamp introduced by this section is a valid RFC 3339 date-time normalized to UTC and ending in uppercase `Z`. Seconds are required. Fractional seconds are omitted when zero; otherwise they use one through nine digits and the final digit is non-zero. Numeric offsets, lowercase `z`, omitted seconds, `24:00:00`, and leap-second spellings are rejected by this v0.1 profile.

The contract preserves the exact canonical source string. It does not convert a numeric offset, round a fraction, or normalize a non-canonical input after authorization. Ordering compares the represented UTC instants.

### 6.4 Closed `subjectTime` profiles

`/subjectTime` is one closed object. It contains exactly one `profile` discriminator plus only the members admitted by that row:

| Assertion branch | Allowed `profile` | Required time members | Semantic posture |
|---|---|---|---|
| structure | `STRUCTURE_AS_OF` | `at` | structural claim applies at one instant |
| structure | `STRUCTURE_EFFECTIVE_FROM` | `start` | structural claim applies from the inclusive start with no asserted end |
| structure | `STRUCTURE_EFFECTIVE_INTERVAL` | `start`, `end` | structural claim applies over `[start, end)` |
| operation with `INTENDED` claim posture | `INTENDED_WINDOW` | `start`, `end` | exact intended operation window `[start, end)` |
| operation with `PERFORMED` claim posture | `PERFORMED_INSTANT` | `at` | alleged performance occurred at one instant |
| operation with `PERFORMED` claim posture | `PERFORMED_INTERVAL` | `start`, `end` | alleged effective execution interval `[start, end)` |
| compliance | `COMPLIANCE_AS_OF` | `at` | compliance claim is evaluated as of one instant |
| compliance | `COMPLIANCE_EFFECTIVE_FROM` | `start` | compliance claim applies from the inclusive start with no asserted end |
| compliance | `COMPLIANCE_EFFECTIVE_INTERVAL` | `start`, `end` | compliance claim applies over `[start, end)` |

`at`, `start`, and `end` use section 6.3. Every two-endpoint profile requires `start < end`. The source pointer is exactly `/subjectTime` in the validated effect intent and the destination is exactly `/subjectTime` in the result; the complete object is copied without conversion. The result rejects legacy `occurrenceTime`, `effectiveFrom`, and `effectiveUntil` mirrors.

When the operation body designates an immutable `InterventionIntentPayload` as its temporal basis, `INTENDED_WINDOW` must equal that payload's `/intendedTimeWindow` endpoints. When it designates an immutable `ExecutionRecordPayload` as its temporal basis, `PERFORMED_INTERVAL` must equal that payload's `/effectiveTimeInterval` endpoints. `capturedAt`, evidence receipt time, assertion time, or a payload's notes can never substitute. A `PERFORMED_INSTANT` must instead bind an exact instant-bearing domain/evidence source admitted by the operation body schema.

The structure and compliance body schemas similarly identify the exact body or evidence field that supplies their as-of/effective basis. A body branch with no exact source cannot use the corresponding profile. Adding another time profile requires a reviewed contract revision rather than schema-author discretion.

### 6.5 Distinct timeline

This contract preserves these separate facts:

- `subjectTime`: the closed structural, intended/performed-operation, or compliance applicability time from section 6.4;
- source capture or evidence times: retained in immutable evidence or payload bytes;
- `assertedAt`: when the asserting Party made or submitted the exact assertion under section 6.2;
- ingress receipt/synchronization and processing times: retained by separate ingress evidence where applicable;
- `humanActedAt`, where fresh approval applies: retained in finalization evidence;
- `authorizationEvaluatedAt`: retained in authorization evidence; and
- `effectCommittedAt`: retained in transaction evidence and the governed-effect receipt.

None is substituted for another. A delayed-sync path with assertion at `T1`, platform receipt at `T2`, and commit at `T3` preserves all three even when `T1 < T2 < T3`; the result's `assertedAt` remains `T1`, not `T3`.

---

## 7. Contract identity and exact action closure

### 7.1 Contract identity

| Property | Closed value |
|---|---|
| contract ID | `ofarm.protectedeffect.assertionrecord.submit.v0.1` |
| contract version | `0.1` |
| owning domain family | `ASSERTION_RECORD_SUBMISSION` |
| intent profiles | `EI_STRUCTURE_ASSERTION_V0_2`, `EI_OPERATION_ASSERTION_V0_2`, `EI_COMPLIANCE_ASSERTION_V0_2` |
| result carrier | future `ofarm.assertionrecord.v0.2` submission branches |
| own result cardinality | exactly one immutable `AssertionRecord` |
| canonicalization | `JCS_RFC8785_SHA256` |

The materialized contract must bind the exact intent-schema and result-schema refs, versions, and digests plus the three exact body-schema bindings, mappings, derivations, forbidden-widening rules, classifications, postconditions, and trace requirements below.

### 7.2 Exact action, effect-subject, result, and commit-class map

| Authorized action | Required intent profile | Required effect-subject kind | Required `assertionType` | Record commit class |
|---|---|---|---|---|
| `ASSERT_STRUCTURE` | `EI_STRUCTURE_ASSERTION_V0_2` | `STRUCTURE_ASSERTION` | `STRUCTURE_ASSERTION` | `STRUCTURE_ASSERTION` |
| `ASSERT_OPERATION_CLAIM` | `EI_OPERATION_ASSERTION_V0_2` | `OPERATION_ASSERTION` | `OPERATION_CLAIM_ASSERTION` | `OPERATION_CLAIM` |
| `ASSERT_COMPLIANCE` | `EI_COMPLIANCE_ASSERTION_V0_2` | `COMPLIANCE_ASSERTION` | `COMPLIANCE_ASSERTION` | `COMPLIANCE_ASSERTION` |

The `OPERATION_ASSERTION` to `OPERATION_CLAIM_ASSERTION` mapping is deliberate: the first is the approved authorization effect-subject token, while the second is the current AssertionRecord subtype. Neither may be used as a free alias outside this row.

Every other action, intent profile, effect-subject kind, subtype, or commit class fails this contract. A primary event family is intentionally absent from this map. `OBSERVATION_ASSERTION`, `LOT_ASSERTION`, and `OTHER_ASSERTION` remain valid v0.1 history but are not new-result branches here.

### 7.3 Optional semantic-event association

An AssertionRecord commit class, the world event or governed act described, and the platform assertion-submission act are three different things. This contract owns only the first and does not classify the other two by subtype lookup.

The validated effect intent may carry `/associatedSemanticEventBinding`. When present, it contains one logical `SemanticEventEnvelope` ref and exactly one immutable revision ref or content digest. The contract requires:

1. the binding resolves to exact bytes valid under the content-addressed active `SemanticEventEnvelope` schema selected by Event Ingress;
2. the separate Event Ingress classification gate passes for those bytes under the active dominant-semantic-consequence rule and supplies the primary family; this contract consumes but does not recompute that family;
3. the assertion's exact logical subject occurs in the envelope's subject set, or the selected body schema supplies an immutable relationship proof that makes the association explicit;
4. the sole assertion anchor-scope pair occurs in the envelope's anchor-scope set; other envelope scopes remain event context and do not become AssertionRecord authority anchors;
5. the body schema supplies exact envelope time selector pointers, each selector resolves once, and the selected values equal the assertion's section 6.4 subject-time values under the selected profile;
6. the envelope's `eventSubtypeId` and `dominantSemanticConsequence` context are compatible with the exact assertion body under a predicate fixed by the selected body schema; family equality alone is insufficient, and this check cannot recompute or override Event Ingress classification;
7. the separately passing Event Ingress evidence binds the envelope digest, its dominant-semantic-consequence classification, and this assertion's fixed commit class; and
8. the protected-effect trace records the envelope ref/digest, consumed primary family, selector comparisons, subject/scope/time/dominant-context compatibility dispositions, and Event Ingress evidence ref/digest.

For an as-of or instant profile, the body schema selects exactly one compatible pointer from `/timeSemantics/eventTime`, `/timeSemantics/observationTime`, `/timeSemantics/decisionTime`, or `/timeSemantics/effectiveFrom`; the branch schema, not the caller, closes which selectors are semantically allowed. For an effective or performed interval, selectors must resolve to `/timeSemantics/effectiveFrom` and `/timeSemantics/effectiveUntil`. For an effective-from profile, the selector resolves to `/timeSemantics/effectiveFrom`. The current envelope has no intended-window field, so `INTENDED_WINDOW` cannot claim association through `SemanticEventEnvelope v0.1`; its binding is absent unless a separately reviewed envelope revision later supplies an exact intended-window profile.

An associated operation claim may therefore consume `InterventionEvent` or `MaterialEvent`, and a compliance assertion may consume `OccurrenceEvent`, `EvidenceEvent`, or `GovernanceEvent`, when Event Ingress independently validates the dominant consequence and the compatibility checks pass. These examples are not a closed family allowlist. The family token alone neither proves nor disproves compatibility.

When `/associatedSemanticEventBinding` is absent, every event-association mapping and postcondition is legitimately `NOT_APPLICABLE`, and this contract makes no primary-event-family claim. Treating assertion submission itself as another semantic event requires a separately governed envelope for that act; it cannot borrow the asserted world's event family.

The immutable AssertionRecord enters under its section 7.2 record commit class. A `SemanticEventEnvelope`, `CommitIngressResult`, or `PromotionTrace` remains a separate governed record. This contract does not create or reclassify any of them. Authorization/finalization evidence, the protected-effect trace, and the governed-effect receipt remain `EvidenceEvent` / evidence-record material under their owning contracts.

---

## 8. Exact intent-to-result mappings

### 8.1 Stable common mappings

| Mapping ID | Authoritative source | Result destination and rule |
|---|---|---|
| `AR_SCHEMA` | selected result-schema binding | `schemaVersion` is exactly `ofarm.assertionrecord.v0.2` |
| `AR_ACTION_PROFILE` | selected action rule and rule-bound intent schema | both must match one row in section 7.2 |
| `AR_EFFECT_SUBJECT` | intent effect subject | kind and proposed ID match section 7.2 and `assertionRecordId` exactly |
| `AR_ID` | intent proposed assertion ID | exact copy to `assertionRecordId` |
| `AR_TYPE` | section 7.2 action/effect-subject row | exact derived `assertionType`; no caller or result override |
| `AR_SUBJECT` | intent assertion-subject binding covered by `effectIntentDigest` | exact copy to `subject`, including posture and conditional immutable selector |
| `AR_SCOPE` | sole rule-extracted `RP_SCOPE_ONE` `TARGET_SCOPE` | exact one-element `NARROWING` mapping to `anchorScopes`, including kind, ref, and immutable selector; other claim context remains in typed body/proof bindings |
| `AR_SUBJECT_SCOPE_PROOF` | intent relationship-proof bindings, conditional under section 5.2 | exact copy or required absence, followed by relationship validation |
| `AR_ASSERTOR` | canonical selected path's `authoritySubjectPartyRef` | exact copy to `assertedByPartyRef` |
| `AR_ASSERTED_AT` | validated intent `/assertedAt` under section 6.2 posture | exact copy to result `/assertedAt`; never derive from `effectCommittedAt`, `humanActedAt`, receipt, or subject time |
| `AR_ASSERTION_ACT_POSTURE` | intent `/assertionActPosture` | exact copy to result; only the two section 6.2 values are allowed |
| `AR_ASSERTION_ACT_EVIDENCE` | conditional intent `/assertionActEvidenceBinding` | exact immutable copy for `VERIFIED_OFFLINE_SUBMISSION`; required absence for `TRUSTED_ONLINE_SUBMISSION` |
| `AR_SUBJECT_TIME` | intent `/subjectTime` | exact copy of one section 6.4 object to result `/subjectTime`, including allowed discriminator, members, and endpoint posture |
| `AR_BODY` | intent action-typed assertion body | exact complete copy to `assertionBody`; no summarization, compilation replacement, or notes side channel |
| `AR_EVIDENCE` | intent evidence revision bindings | exact complete non-empty array in `evidenceBindings`; no addition, omission, mutable ref, or ref-only downgrade |
| `AR_CLAIM_STATE` | contract constant | exactly `PENDING_REVIEW` |
| `AR_EVENT_ASSOCIATION` | optional intent `/associatedSemanticEventBinding` plus separately passing Event Ingress output | section 7.3 compatibility and trace binding; no AssertionRecord destination and no event-family derivation; legitimate `NOT_APPLICABLE` only when binding is absent |

Every mapping receives one explicit disposition. A missing, duplicated, ambiguous, type-invalid, mutable, unresolved, or conflicting authoritative source fails the contract.

### 8.2 Branch mappings

| Mapping ID | Branch | Source and result rule |
|---|---|---|
| `AR_OPERATION_POSTURE` | operation only | exact copy of intent `claimPosture` to `operationClaimContext.claimPosture` |
| `AR_OPERATION_PERFORMER` | operation only | exact copy of intent `performedByPartyRef`; never derive from reporter or authority subject |
| `AR_OPERATION_AGENT_ACTORSHIP` | operation only | exact immutable array when posture is `PERFORMED` and the intent alleges agent performance; otherwise required absence |
| `AR_OPERATION_PERFORMER_AUTHORITY` | operation only | exact optional immutable array only for `PERFORMED`; trace retains `NOT_EVALUATED_BY_AUTHORIZATION` regardless of presence |
| `AR_OPERATION_PAYLOADS` | operation only | any admitted intent/execution payload bindings remain exact inside the typed body; otherwise required absence |
| `AR_COMPLIANCE_RULES` | compliance only | exact complete non-empty rule-revision array to `complianceBasis.ruleRevisionBindings` |
| `AR_COMPLIANCE_EVIDENCE_POLICY` | compliance only | exact complete non-empty evidence-policy-revision array to `complianceBasis.evidencePolicyRevisionBindings` |
| `AR_CORRECTION_LINEAGE` | every subtype | when absolute `/assertionBody/assertionPosture` is `CORRECTION`, copy `/supersedesAssertionRecordBinding` exactly and require every section 5.5 compatibility condition to pass; require the binding absent for `INITIAL` |
| `AR_STRUCTURE_BRANCH_ABSENCE` | structure only | `operationClaimContext` and `complianceBasis` are absent |
| `AR_OPERATION_BRANCH_ABSENCE` | operation only | `complianceBasis` is absent |
| `AR_COMPLIANCE_BRANCH_ABSENCE` | compliance only | `operationClaimContext` is absent |
| `AR_LEGACY_ABSENCE` | all branches | `benefitingPartyRef`, flat legacy time fields, loose provenance/payload refs, legacy `supersedesAssertionRecordRef`, `supersededByReviewDecisionRef`, and `notes` are absent |

### 8.3 Permitted derivations

These are the only permitted derivations:

| Derived value | Exact source and rule |
|---|---|
| `schemaVersion` | constant from the selected result-schema binding |
| `assertionType` | section 7.2 action/effect-subject map |
| `claimState` | contract constant `PENDING_REVIEW` |
| record commit class | section 7.2 action map, recorded outside result-local choice |
| canonical result and resolved-input digests | shared JCS/SHA-256 profile over exact validated or resolved bytes |

Primary event family is not a permitted derivation. When an exact semantic-event binding exists, the trace consumes the family selected by the separately passing Event Ingress boundary; otherwise no family is claimed.

Everything else is an exact copy, a contract-validated relationship, a governed assertion-act fact, or required absence. There is no default subject, scope, actor, assertion time, subject time, body, evidence, performer, compliance basis, lineage, event family, current state, or accepted consequence. There is no local sorting, name search, family coercion, latest-revision lookup, body compilation, or generated companion ID.

---

## 9. Forbidden widening and companion-effect boundary

This contract's own domain result cardinality is exactly one new AssertionRecord. Transaction evidence required by other contracts is not a second AssertionRecord or a companion domain effect.

The contract forbids:

- creating or mutating durable structure from a structure assertion;
- treating `INTENDED` as performed, or `PERFORMED` as accepted execution;
- creating an accepted executed intervention consequence from an operation claim;
- treating evidence, compiled output, or a passed evidence policy as a compliance fact;
- creating a ReviewDecision, accepted consequence, current-state materialization, or current-state supersession effect from a correction lineage edge;
- editing, deleting, relabeling, or replacing an earlier AssertionRecord, evidence item, payload, scope, subject, or rule revision;
- adding a second assertion, event envelope, or domain record because it seems implied by the body; and
- using fresh human approval as acceptance, attestation, performer-authority proof, or promotion.

If another governed result is needed, an enclosing composition must separately identify its authority basis, protected-effect contract, exact derivation, result digest, and atomicity rule. This candidate defines no such composition and recognizes no implicit companion domain result.

---

## 10. Assertion-specific postconditions

### 10.1 Common postconditions

| Postcondition ID | Required proposed-state condition |
|---|---|
| `PC_ONE_ASSERTION` | exactly one new assertion ID resolves to one schema-valid immutable result |
| `PC_VALIDATED_BYTES` | committed AssertionRecord bytes equal the bytes validated by this contract |
| `PC_INPUTS_IMMUTABLE` | assertion-act evidence, subject, scope, proof, semantic event, evidence, payload, prior assertion and its creation/ingress evidence, rule, and evidence-policy inputs remain byte-identical |
| `PC_ACTION_TYPE` | action, intent profile, effect subject, assertion subtype, and commit class match one section 7.2 row; no event family is inferred |
| `PC_PENDING_REVIEW` | result `claimState` is `PENDING_REVIEW`; no accepted or in-force result is emitted |
| `PC_SUBJECT_SCOPE` | subject posture is truthful and the subject is exactly equal to, or proven within the governed relation to, the sole anchor scope |
| `PC_ASSERTOR` | asserting Party is the canonical selected authority subject and is not substituted by an approver, sponsor, principal, performer, or beneficiary |
| `PC_ASSERTION_ACT` | `assertedAt`, act posture, conditional act evidence, and asserting Party satisfy section 6.2 |
| `PC_SUBJECT_TIME` | the exact branch/posture profile, members, canonical timestamps, endpoint order, source selectors, and conditional payload equality satisfy sections 6.3 and 6.4 |
| `PC_TEMPORAL_SEPARATION` | assertion, subject, evidence/capture, ingress, approval, authorization, and commit times retain their distinct meanings under section 6.5 |
| `PC_EVENT_ASSOCIATION` | section 7.3 association passes when bound and is `NOT_APPLICABLE` when absent; AssertionRecord subtype never selects a family |
| `PC_CORRECTION_LINEAGE` | section 5.5 posture, exact immutable prior binding, prior-commit proof, subtype, governance boundary/twin, authority anchor, and logical subject all agree without mutating or deactivating the prior assertion |
| `PC_NO_UNBOUND_EFFECT` | no prior record mutation, event envelope, review, consequence, materialization, or other governed result is inserted or changed without its own applicable authority and contract |
| `PC_NO_CURRENT_STATE` | this contract neither writes current state nor marks the assertion accepted solely because submission passed |
| `PC_TRANSACTION_HANDOFF` | the applicable transaction gate binds the exact passing result/trace and commits the effect, authorization/finalization evidence, receipt, and single-use consumption atomically |
| `PC_UNIQUE_ID` | a duplicate assertion ID with different bytes is rejected |

### 10.2 Branch postconditions

| Postcondition ID | Branch-specific meaning |
|---|---|
| `PC_STRUCTURE` | only a pending structure claim is created; no durable structure identity, revision, boundary, role, pack state, or current structural state changes |
| `PC_OPERATION` | claim posture, reporter, performer, agent actorship, performer-authority evidence, closed subject-time profile, and payloads satisfy sections 5.3 and 6.4; no execution is accepted |
| `PC_COMPLIANCE` | exact rules, evidence policies, evidence, closed subject-time profile, and body satisfy sections 5.4 and 6.4; no compliance fact or certification state is created |
| `PC_BRANCH_ABSENCE` | every field inapplicable to the selected branch is absent |

For `ASSERT_STRUCTURE` and `ASSERT_COMPLIANCE`, `PC_TRANSACTION_HANDOFF` relies on the PR #20 fresh-approval mode when that dependency is later materialized. For `ASSERT_OPERATION_CLAIM`, it cannot pass at an executable commit boundary until a separately reviewed `NOT_REQUIRED` transaction profile supplies the equivalent atomic handoff without inventing human approval.

---

## 11. Content addressing and validation trace

### 11.1 Digest closure

The machine contract's `contractDigest` is `sha256:` plus SHA-256 over RFC 8785 JCS bytes of the complete contract after removing exactly the top-level `/contractDigest` member. No nested or other top-level member is excluded.

`resultDigest` covers the complete schema-valid proposed AssertionRecord with no excluded member. `resultSchemaDigest` binds the exact selected result-schema bytes. Each action's intent-schema and body-schema digest binds its exact bytes. Every revision-ref resolution records the digest of the resolved immutable bytes.

These application rules do not create a competing generic digest framework. The later shared validation-trace and receipt profiles may carry these bindings by reference but cannot weaken or omit this contract's semantic closure.

### 11.2 Assertion validation payload

The immutable protected-effect validation trace must bind:

- authorization result/rule and effect-intent refs/digests;
- result ID/ref/digest and result-schema ref/version/digest;
- contract ID/version/ref/digest and selected action/body-schema binding;
- assertion-act posture and conditional evidence, sole authority-target scope, closed subject-time profile/selectors, and every resolved subject, relationship-proof, assertion evidence, payload, prior assertion, rule, and evidence-policy digest;
- for a correction, the prior assertion's immutable creation/ingress evidence ref/digest, committed canonical-history position and transaction-start snapshot/watermark, resolved governance boundary and twin posture, plus exact subtype, anchor, subject, and ID comparisons;
- one `PASS`, `FAIL`, legitimate `NOT_APPLICABLE`, or dependency-bound `NOT_EVALUATED` disposition for every `AR_*` mapping;
- one such disposition for every `PC_*` postcondition;
- source/destination selectors or pointers and compared digests;
- record commit class;
- when a semantic event is bound, its envelope ref/digest, separately consumed primary family, Event Ingress evidence ref/digest, and every subject/scope/time compatibility comparison; otherwise an explicit `NOT_APPLICABLE` event-association disposition and no family value;
- operation performer-authority disposition, exactly `NOT_EVALUATED_BY_AUTHORIZATION` for the operation branch; and
- an overall `PASS` or `FAIL` disposition.

`NOT_APPLICABLE` means that an item's contract-declared branch condition does not apply; a required item cannot use it. `NOT_EVALUATED` means no pass-or-fail conclusion was reached because a named prerequisite did not pass. A required dependent item may be `NOT_EVALUATED`, but that prevents overall `PASS`.

The materialized contract enumerates the prerequisite IDs for every dependency that can produce `NOT_EVALUATED`. A runtime cannot use it to suppress an independent failure or omit an evaluation arbitrarily. Overall `PASS` requires every required mapping and postcondition to pass. The trace itself is immutable and content-addressed under the separately reviewed shared evidence envelope; until that envelope exists with a real ref/digest, no executable binding exists.

This section owns only the AssertionRecord-specific validation payload. It does not restate generic approval, reservation, challenge, receipt, retention, transaction sequencing, or persistence machinery.

---

## 12. Validation and failure semantics

Before commit, the protected-effect gate must:

1. verify the selected action rule's exact effect-intent-schema and protected-effect-contract bindings;
2. load and digest-verify the referenced protected-effect contract;
3. verify the result-schema and selected body-schema refs, versions, and digests owned by that contract;
4. validate the proposed result against that exact result/body schema branch;
5. evaluate every applicable `AR_*` mapping and assertion-specific `PC_*` postcondition; and
6. supply an overall passing immutable trace to the applicable atomic transaction gate.

If any item fails, no AssertionRecord or companion domain effect commits and single-use consumption does not commit. The existing authorization result remains its authority-gate result; `ALLOW` is not rewritten to `DENY` or treated as proof that the domain gate passed.

An authorization `ALLOW` for `ASSERT_OPERATION_CLAIM` is not executable merely because this domain result validates. Until the separate `NOT_REQUIRED` transaction profile is approved and materialized, the transaction prerequisite remains absent and the operation has no compliant commit path.

This candidate states only AssertionRecord-specific preconditions and effects. It does not implement or redefine a transaction manager.

---

## 13. Production-reachable hostile cases

| Case | Required disposition |
|---|---|
| action, intent profile, or effect-subject kind is substituted | `AR_ACTION_PROFILE` or `AR_EFFECT_SUBJECT` fails; no assertion commits |
| `OPERATION_ASSERTION` is copied directly into `assertionType` instead of mapping to `OPERATION_CLAIM_ASSERTION` | `AR_TYPE` fails |
| observation, lot, other, or an unknown assertion subtype is offered through this contract | result-schema or `AR_TYPE` fails |
| proposed assertion ID differs between effect subject, intent, and result | `AR_EFFECT_SUBJECT` / `AR_ID` fails |
| duplicate assertion ID resolves to different bytes | `PC_UNIQUE_ID` fails |
| result uses `IN_FORCE`, `CONTESTED`, `REJECTED`, or `SUPERSEDED` | `AR_CLAIM_STATE` / `PC_PENDING_REVIEW` fails |
| fresh approval is treated as acceptance or a compliance fact | `PC_PENDING_REVIEW` / `PC_NO_CURRENT_STATE` fails |
| existing subject lacks exactly one immutable selector, or prospective subject carries one | `AR_SUBJECT` fails |
| prospective subject is treated as a created durable identity | `PC_STRUCTURE` or `PC_NO_UNBOUND_EFFECT` fails |
| a second anchor scope, ancestor, tenant, or display scope is added | `AR_SCOPE` fails |
| a multi-context claim is narrowed to one anchor by dropping its field, crop-cycle, operation, lot, or relationship context | `AR_BODY`, `AR_SUBJECT_SCOPE_PROOF`, or `PC_SUBJECT_SCOPE` fails; materialization stops if lossless representation is unavailable |
| subject differs from anchor scope and relationship proof is missing, mutable, stale, or invalid | `AR_SUBJECT_SCOPE_PROOF` / `PC_SUBJECT_SCOPE` fails |
| asserted Party is replaced by human approver, authenticated representative, agent sponsor, performer, or beneficiary | `AR_ASSERTOR` fails |
| caller supplies `/assertedAt` for `TRUSTED_ONLINE_SUBMISSION` instead of the trusted runtime | `AR_ASSERTED_AT` / `PC_ASSERTION_ACT` fails |
| verified offline submission omits, substitutes, or cannot validate assertion-act evidence, or its Party, time, or content differs | `AR_ASSERTION_ACT_EVIDENCE` / `PC_ASSERTION_ACT` fails |
| `effectCommittedAt`, `humanActedAt`, receipt, authorization, ingress, evidence-capture, or subject time is substituted for the assertion-act source | `AR_ASSERTED_AT` / `PC_TEMPORAL_SEPARATION` fails |
| offline assertion occurs at `T1`, platform receives it at `T2`, and commit occurs at `T3`, but the result records `T2` or `T3` as `assertedAt` | `AR_ASSERTED_AT` / `PC_TEMPORAL_SEPARATION` fails; `T1`, `T2`, and `T3` remain distinct |
| a timestamp uses a numeric offset, lowercase `z`, omitted seconds, trailing-zero fraction, `24:00:00`, leap-second spelling, or another non-canonical representation | `PC_ASSERTION_ACT` or `PC_SUBJECT_TIME` fails as applicable |
| subject-time profile is unavailable for the action/claim posture, carries an extra or missing member, or has `start >= end` | `AR_SUBJECT_TIME` / `PC_SUBJECT_TIME` fails |
| `INTENDED` uses a performed profile, or `PERFORMED` uses `INTENDED_WINDOW` | `AR_OPERATION_POSTURE` / `AR_SUBJECT_TIME` fails |
| payload `capturedAt` replaces intended/effective endpoints, or designated payload endpoints differ from `/subjectTime` | `AR_SUBJECT_TIME` / `AR_OPERATION_PAYLOADS` / `PC_SUBJECT_TIME` fails |
| `assertedAt` replaces structural, intended, performed, effective, or compliance subject time | `AR_SUBJECT_TIME` / `PC_TEMPORAL_SEPARATION` fails |
| assertion body differs by whitespace-bearing string value, case, translation, normalization, summarization, or compiled substitution | `AR_BODY` fails |
| evidence is changed, omitted, added, reordered contrary to schema posture, unresolved, mutable, or downgraded to a logical ref | `AR_EVIDENCE` fails |
| `EP_NONE` is interpreted as permission to omit the intent-bound evidence array | `AR_EVIDENCE` fails; the action policy and assertion evidence binding are different axes |
| operation reporter is copied into `performedByPartyRef` | `AR_OPERATION_PERFORMER` fails |
| `PERFORMED` is changed to `INTENDED`, or vice versa | `AR_OPERATION_POSTURE` fails |
| agent performance is alleged without exact actorship bindings, or agent bindings are added to a non-agent claim | `AR_OPERATION_AGENT_ACTORSHIP` fails |
| performer authority is reported as authorized because an evidence ref is present or the reporter was authorized | mapping or trace conformance fails; disposition remains `NOT_EVALUATED_BY_AUTHORIZATION` |
| loose or latest intervention/execution payload ref is added | `AR_OPERATION_PAYLOADS` fails |
| compliance rule or evidence-policy revision is missing, changed, mutable, or substituted | `AR_COMPLIANCE_RULES` / `AR_COMPLIANCE_EVIDENCE_POLICY` fails |
| compiled output replaces the exact compliance body | `AR_BODY` fails |
| branch-inapplicable operation or compliance fields are present as `null`, empty, or populated | applicable branch-absence mapping / `PC_BRANCH_ABSENCE` fails |
| `/assertionBody/assertionPosture` says `CORRECTION` but `/supersedesAssertionRecordBinding` is absent | `AR_CORRECTION_LINEAGE` / `PC_CORRECTION_LINEAGE` fails |
| correction binding resolves to the wrong digest, mutable bytes, or a non-AssertionRecord | `AR_CORRECTION_LINEAGE` fails |
| prior and new assertions have different `assertionType` values | `AR_CORRECTION_LINEAGE` / `PC_CORRECTION_LINEAGE` fails |
| prior creation context is unproved or resolves to another tenant/deployment boundary or applicable twin | `AR_CORRECTION_LINEAGE` / `PC_CORRECTION_LINEAGE` fails; an opaque ref or current storage location cannot repair it |
| new anchor differs from the exact prior v0.2 sole anchor or does not directly equal any prior v0.1 anchor kind/ref pair | `AR_CORRECTION_LINEAGE` / `PC_CORRECTION_LINEAGE` fails; scope ancestry or aliasing is not equality |
| prior and new assertions have different logical `subjectType` or `subjectRef` values | `AR_CORRECTION_LINEAGE` / `PC_CORRECTION_LINEAGE` fails |
| correction binding self-references the proposed assertion ID | `AR_CORRECTION_LINEAGE` / `PC_CORRECTION_LINEAGE` fails |
| bound prior assertion was not already committed and visible in the transaction-start snapshot | `AR_CORRECTION_LINEAGE` / `PC_CORRECTION_LINEAGE` fails; a prospective, future, concurrent, or timestamp-only reference is insufficient |
| `/assertionBody/assertionPosture` is `INITIAL` but correction lineage is present | `AR_CORRECTION_LINEAGE` / `PC_CORRECTION_LINEAGE` fails |
| correction lineage is treated as acceptance, deletion, deactivation, or current-state replacement | `PC_CORRECTION_LINEAGE` / `PC_NO_CURRENT_STATE` fails |
| notes, benefiting Party, loose provenance, legacy flat time, payload-ref, legacy `supersedesAssertionRecordRef`, or `supersededByReviewDecisionRef` is inserted | `AR_LEGACY_ABSENCE` fails |
| structure assertion creates a new field, boundary, role, or activation state | `PC_STRUCTURE` / `PC_NO_UNBOUND_EFFECT` fails |
| operation claim creates accepted execution or changes operation current state | `PC_OPERATION` / `PC_NO_CURRENT_STATE` fails |
| compliance assertion creates compliance fact, certification, or enforcement state | `PC_COMPLIANCE` / `PC_NO_CURRENT_STATE` fails |
| assertion creation mutates or deletes a prior assertion, evidence item, payload, subject, scope, or rule | `PC_INPUTS_IMMUTABLE` / `PC_NO_UNBOUND_EFFECT` fails |
| contract silently creates a SemanticEventEnvelope, ReviewDecision, consequence, or materialization | `PC_NO_UNBOUND_EFFECT` fails |
| valid operation claim binds a separately validated `MaterialEvent`, but subtype lookup forces `InterventionEvent` or fails the claim | conformance failure; `AR_EVENT_ASSOCIATION` consumes the Event Ingress family without deriving one |
| valid compliance assertion binds a separately validated `OccurrenceEvent` or `EvidenceEvent`, but subtype lookup forces `GovernanceEvent` or fails the claim | conformance failure; `AR_EVENT_ASSOCIATION` consumes the Event Ingress family without deriving one |
| semantic-event family changes without a matching change in dominant event semantics | Event Ingress classification fails; this contract cannot repair or reclassify it through assertion subtype |
| associated event is mutable, digest-invalid, lacks a passing Event Ingress disposition, omits the assertion's subject/scope, or has incompatible selected time values | `AR_EVENT_ASSOCIATION` / `PC_EVENT_ASSOCIATION` fails |
| no semantic event is bound but the trace invents a primary family | `AR_EVENT_ASSOCIATION` / `PC_EVENT_ASSOCIATION` fails; the correct association disposition is `NOT_APPLICABLE` with no family value |
| record commit class differs from section 7.2 | `PC_ACTION_TYPE` fails |
| AssertionRecord is retyped as an event envelope or given caller-selected classification fields | result schema / `PC_ACTION_TYPE` fails |
| contract, schema, intent, result, or resolved-input digest changes | binding or mapping fails |
| one required mapping or postcondition disposition is missing | overall trace cannot pass |
| a failed prerequisite's dependent item is marked `PASS`, `FAIL`, or `NOT_APPLICABLE` instead of dependency-bound `NOT_EVALUATED` | trace conformance fails |
| operation claim reaches commit through PR #20 even though its selected finalization mode is `NOT_REQUIRED` | transaction binding fails; no assertion or consumption commits |
| relevant state changes between validation and atomic commit | applicable transaction guard fails and requires re-evaluation |
| domain failure rewrites authorization `ALLOW` | conformance failure; authorization evidence remains unchanged |

Fixtures must enter through the production result builder, protected-effect validator, applicable transaction boundary, persistence path, and receipt lookup rather than unit-only helpers.

---

## 14. Migration and currentness

`AssertionRecord v0.1` remains current/default until a separately governed promotion says otherwise. Existing records and examples remain v0.1 history, including their recorded `IN_FORCE` values.

A v0.1 record cannot claim v0.2 strength unless immutable source evidence establishes every required field and mapping. Missing body schema/posture, subject/scope revision, relationship proof, closed subject-time profile, evidence revision, asserting-party basis, assertion-act posture/evidence, operation provenance, compliance basis, optional event association, or correction lineage cannot be guessed.

Migration never rewrites a v0.1 claim state, notes field, logical evidence/provenance ref, payload ref, assertion time, flat subject-time field, or supersession ref. A new v0.2 correction may bind an old AssertionRecord only through section 5.5's exact immutable `supersedesAssertionRecordBinding` and only when immutable creation/ingress evidence proves every legacy target-compatibility fact. Missing legacy governance, twin, anchor-context, or prior-commit proof is not reconstructed from current state; that submission must remain a new `INITIAL` assertion or stop. A compatible correction does not upgrade or rewrite the old record. A semantic-event association similarly binds exact existing envelope bytes without copying their primary family into the AssertionRecord.

Draft schema or contract presence changes no currentness. A v0.2 `PENDING_REVIEW` assertion does not enter an in-force materialization merely because it is schema-valid, authorized, human-approved for submission, or protected-effect-valid. Review and materialization remain downstream governed boundaries.

---

## 15. Later `AuthorizationPolicyBundle v0.2` binding

This PR does not create or edit the policy bundle.

After semantic approval and materialization of real content-addressed protected-effect contract bytes, the bundle PR must:

1. bind the exact contract ID/version/ref/digest and owning family;
2. bind the same reviewed contract to the three assertion action rules;
3. preserve each rule's exact intent profile, effect-subject kind, `RP_SCOPE_ONE` policy, evidence policy, human-finalization mode, and historical-authority posture from PR #11; and
4. include the protected-effect contract binding in each affected complete per-action `ruleDigest` closure.

The result-schema and body-schema bindings, `AR_*` selectors, derivations, forbidden-widening rules, classification, postconditions, and trace requirements remain solely inside the content-addressed protected-effect contract. Changing any of them changes `contractDigest`, which changes each affected action-rule digest. The bundle must not copy them or become a second source of domain semantics.

The bundle cannot point at this prose file as an executable contract. It also cannot make `ASSERT_OPERATION_CLAIM` executable while the separately owned `NOT_REQUIRED` transaction profile is missing.

---

## 16. Traceability to issue #22

| Acceptance criterion | Disposition |
|---|---|
| inventory current AssertionRecord capabilities, examples, and gaps | section 4 |
| decide whether a minimal v0.2 carrier is required | sections 4.3 and 5 |
| exact action, intent profile, effect-subject, result subtype, and fixed commit-class map without subtype-derived event family | section 7 |
| consume optional immutable SemanticEventEnvelope and separately validated family without copying Event Ingress ownership | sections 7.3, 8, 10, 11, and 13 |
| bind ID, subject, sole scope, asserting Party, assertion-act posture/time, closed subject time, body, evidence, correction lineage, and branch content | sections 5, 6, and 8 |
| preserve reporter/performer separation and `NOT_EVALUATED_BY_AUTHORIZATION` | sections 5.3, 6, 8.2, 11.2, and 13 |
| keep all new assertion submissions pending review | sections 1, 8, 10, and 14 |
| label and losslessly constrain the one-anchor `NARROWING` | sections 4.1, 5.2, 8.1, 13, and 17 |
| separate assertion time from record/commit time and close exact temporal profiles | sections 6, 8, 10, 11, 13, and 17 |
| preserve optional immutable correction lineage, close its target-compatibility predicate, and avoid mutating prior history | sections 5.5, 8.2, 9, 10, 11, 13, 14, and 17 |
| enumerate permitted derivations and required absences | section 8 |
| forbid mutation, acceptance, current state, and implicit companion effects | sections 9, 10, 12, and 13 |
| distinguish event classification, assertion submission, and record commit class | section 7.3 |
| content-address contract and deterministic digest projection | sections 7.1 and 11.1 |
| immutable dependency-aware mapping/postcondition trace | sections 11.2 and 13 |
| validate before atomic commit without rewriting authorization | section 12 |
| production-reachable hostile cases | section 13 |
| later whole-contract bundle registration without duplicating domain semantics | section 15 |
| expose the unclosed `NOT_REQUIRED` transaction dependency without editing that boundary | sections 3, 10, 12, 13, 15, 17, and 18 |

---

## 17. Steward approval card

| Decision | Proposed answer | Approval required |
|---|---|---|
| Is a future `AssertionRecord v0.2` carrier required? | yes | yes |
| Does this contract cover exactly three assertion-submission actions and exactly one new result? | yes | yes |
| Is the exact action-to-result subtype map in section 7.2 approved? | yes | yes |
| Must every result created by these submission actions be `PENDING_REVIEW`? | yes | yes |
| Does fresh approval authorize only the exact structure/compliance submission rather than acceptance? | yes | yes |
| Is reducing v0.1's one-or-more anchors to the sole immutable `RP_SCOPE_ONE` anchor explicitly a `NARROWING`? | yes; typed subject/body context and immutable relationship proofs must preserve the claim losslessly or materialization stops | yes |
| Is an existing subject immutable while a prospective subject remains only claimed and uncreated? | yes | yes |
| Must a different subject-to-scope relationship have exact immutable proof? | yes | yes |
| Is `assertedByPartyRef` the selected authority subject rather than approver, sponsor, principal, performer, or beneficiary? | yes | yes |
| Is `assertedAt` the exact governed assertion-act time rather than `effectCommittedAt`? | yes; commit time remains separate receipt/transaction evidence | yes |
| Are `TRUSTED_ONLINE_SUBMISSION` and `VERIFIED_OFFLINE_SUBMISSION` the only assertion-act postures, with exact conditional evidence? | yes | yes |
| Can fresh-approval `humanActedAt` become assertion time merely because approval occurred? | no; this contract never uses it as the source | yes |
| Are the nine section 6.4 structure, operation, and compliance subject-time rows the complete closed profiles? | yes | yes |
| Are all timestamps canonical UTC RFC 3339 values with exact endpoint and ordering rules? | yes | yes |
| Are body and evidence exact, typed, immutable, and free of notes or ref-only side channels? | yes | yes |
| May `CORRECTION` create one new pending assertion with one exact immutable prior-assertion binding? | yes; `INITIAL` requires absence | yes |
| Must a correction target already exist and differ from the proposed assertion ID? | yes; authoritative transaction-start history proof is required | yes |
| Must correction target and new assertion have the same subtype, governance boundary/twin, authority anchor, and logical subject? | yes; all section 5.5 conditions must pass exactly | yes |
| Does correction lineage leave the prior assertion immutable and avoid acceptance, deactivation, or current-state replacement? | yes | yes |
| Does the operation branch preserve required performer provenance without claiming historical performer authorization? | yes | yes |
| Must operation performer authority remain `NOT_EVALUATED_BY_AUTHORIZATION`? | yes | yes |
| Does the compliance branch bind exact rule and evidence-policy revisions without creating a compliance fact? | yes | yes |
| Does assertion action/subtype derive a primary event family? | no | yes |
| When a semantic event is bound, must its immutable envelope and separate Event Ingress classification pass subject/scope/time compatibility and enter only the trace? | yes | yes |
| When no semantic event is bound, does this contract make no primary-family claim? | yes | yes |
| Are record commit classes fixed to `STRUCTURE_ASSERTION`, `OPERATION_CLAIM`, and `COMPLIANCE_ASSERTION`? | yes | yes |
| Does this contract create no event envelope, review, accepted consequence, current state, current-state supersession, or other companion domain effect? | yes | yes |
| Must every `AR_*` and `PC_*` item have an explicit allowed trace disposition, with overall `PASS` requiring every required item to pass? | yes | yes |
| Does protected-effect failure leave authorization evidence unchanged? | yes | yes |
| Does PR #20 close fresh-approval transaction handling for structure/compliance but not `NOT_REQUIRED` handling for operation claims? | yes | yes |
| Must operation-claim execution wait for a separate `NOT_REQUIRED` transaction profile rather than borrowing fresh approval? | yes | yes |
| Do schema, transaction, shared evidence, hostile conformance, acceptance, promotion, and runtime remain separately owned? | yes | yes |

Any requested authorization, transaction, review, event-vocabulary, evidence-retention, runtime, or currentness change must remain in its own trust-boundary PR.

---

## 18. Staged delivery and completion

1. **Authorization prerequisite:** satisfied by semantic approval for exact PR #11 head `03a21f669ee04f96d444e14f00ae7212cab04803`; re-open this gate if that head's semantics change.
2. **Human-finalized transaction prerequisite:** PR #20 at `98f8c4fafbae42c8f7fd931f43f53adcb4733713` supplies the approved fresh-approval protocol selected by structure and compliance; later machine materialization must bind its exact promoted bytes.
3. **Phase A domain approval:** approve or amend this one-file AssertionRecord candidate.
4. **Missing transaction-mode closure:** separately define the atomic `NOT_REQUIRED` transaction path selected by `ASSERT_OPERATION_CLAIM`; do not edit PR #20 or this domain contract to simulate approval.
5. **Domain materialization:** separately create the non-default `AssertionRecord v0.2` schema, three exact body-schema branches, assertion-act fields, nine closed subject-time rows, optional event-association and correction-lineage inputs, the closed correction-target predicate and selectors, protected-effect contract, and digest fixtures. Stop if exact schema/contract bytes cannot implement this closure without changing another boundary.
6. **Shared evidence materialization:** separately create or bind the assertion-act evidence/time-trust posture, validation-trace envelope, governed-effect receipt profiles, and applicable immutable prior-creation/ingress evidence, together with finalization/consumption profiles owned by their existing boundaries. This contract consumes those exact bindings and does not redefine their evidence claims.
7. **Bundle binding:** separately bind the exact reviewed protected-effect contract identity/ref/digest as one unit into `AuthorizationPolicyBundle v0.2`.
8. **Hostile conformance:** exercise section 13 through production-reachable paths, including variable event families, delayed assertion/receipt/commit time, subject-time substitution, cross-context/self/future correction targets, multi-context single-anchor representation, fresh approval, agent-assisted submission, represented action, reporter/performer separation, and conflicting replay.
9. **Acceptance and promotion:** accept exact bytes and change current/default status only through separate governed steps in the sequence fixed by PR #11.
10. **OFARM2 extraction:** consume only promoted, digest-verified canonical bytes.

Phase A is complete when issue #22's criteria are reviewed, the exact PR #11 and PR #20 dependencies remain approved, event-family non-derivation, assertion/subject-time closure, correction lineage and target compatibility, one-anchor narrowing, and the missing transaction-mode dependency are explicit, and this PR still changes only this non-authoritative candidate file.
