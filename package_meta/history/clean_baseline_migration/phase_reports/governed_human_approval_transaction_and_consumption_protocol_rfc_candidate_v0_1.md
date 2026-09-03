# OFARM Governed Human-Approval Transaction and Consumption Protocol v0.1

Date: 2026-09-03<br>
Status: Phase A candidate for `samovers/OFARM#19`; non-authoritative, not accepted law, and not a current/default machine contract<br>
Depends on: the approved authorization candidate on PR #11 at `03a21f669ee04f96d444e14f00ae7212cab04803`, the approved final `ReviewDecision` protected-effect candidate on PR #17 at `9ef08030b25eb3db1c2da14d6595300198384ff2`, and the protected-effect program on `samovers/OFARM#12`<br>
Scope: define the shared runtime transaction, single-use consumption, concurrency, retry, and recovery protocol for fresh human approval and direct human final action without holding a database transaction open during human think time

---

## 1. Decision requested

Stewards are asked to approve, reject, or amend these bounded decisions:

1. the protocol preserves the two human-finalization modes selected by PR #11: `FRESH_HUMAN_APPROVAL_REQUIRED` uses a **two-stage reservation/challenge and finalization protocol**, while `DIRECT_HUMAN_ACTION_REQUIRED` uses one short direct-human finalization transaction and no separate approval challenge;
2. the fresh-approval reservation stage durably binds one logical operation, challenge, intended approver, exact effect intent, display evidence, preliminary authority-relevant state, and expiry, but grants no authority, consumes no decision, creates no protected effect, and reserves no domain truth;
3. after the applicable explicit human act, the shared short finalization transaction re-resolves the principal and session, re-evaluates all current authority and other relevant state, validates the proposed domain effect, and commits the effect, decision evidence, finalization evidence, single-use consumption, and governed-effect receipt atomically;
4. for fresh approval, challenge and final `authorityRelevantStateDigest` values must match exactly; for both modes, a separate transaction guard prevents any relevant authority, policy, evidence, resource, or protected-effect state used by finalization from changing before commit;
5. one operation-boundary-, requester-, representation-, action-, and human-finalization-scoped idempotency key identifies one logical operation digest, permits safe retrieval and retry of that same operation, and can never be reused for different intent bytes or a second protected effect;
6. every authorization decision is single-use, and every separate human approval is single-use where that mode applies; concurrent finalizers are serialized by durable uniqueness and commit guards rather than by an authority lease;
7. known rollback, state drift, expiry, cancellation, protected-effect failure, persistence failure, and uncertain commit remain distinct protocol outcomes and never fabricate or rewrite an authorization outcome;
8. an uncertain commit is reconciled by authoritative receipt and consumption lookup before any retry; the runtime must not blindly reapply an effect whose commit status is unknown;
9. reservation, finalization-attempt, consumption, and receipt evidence are immutable and append-only; mutable locks, queues, or coordination rows are derived operational indexes and cannot become the only surviving audit account; and
10. the first concrete protected-effect handoff is the approved final `ReviewDecision` contract from PR #17, whose actions use direct-human finalization rather than the separate approval-challenge mode, while every other effect family remains unsupported until its own contract is reviewed and bound.

Approval of this candidate authorizes no schema, database, runtime, currentness, acceptance, promotion, transport-release, retention, or key-custody change.

---

## 2. Primary trust boundary and intended PR boundary

### 2.1 Primary trust boundary

The primary trust boundary is **runtime transaction coordination and single-use consumption integrity**.

This boundary owns:

- where an interactive operation is durably reserved and where it is finalized;
- how rule-selected fresh-approval and direct-human-final-action modes enter the shared final transaction without being conflated;
- the rule that no database transaction remains open during human think time;
- reservation identity, lifecycle, expiry, cancellation, and replacement generation;
- trusted finalization transaction time, deadline, snapshot, and commit-guard inputs;
- concurrency control for the operation, authorization decision, protected effect, idempotency key, and approval where fresh approval applies;
- atomic visibility of the protected effect and its required evidence;
- safe retry, crash recovery, orphan cleanup, and uncertain-commit reconciliation; and
- the transaction-side handshake with separately owned authorization and protected-effect contracts.

### 2.2 Intended Phase A PR boundary

This PR adds only this non-authoritative candidate in the historical phase-report lane.

It does not own or change:

- authorization eligibility, action meanings, outcome aggregation, reason selection, approver eligibility, grants, delegation, sharing, revocation, principal resolution, or CP3 posture;
- the `ReviewDecision` result carrier, intent-to-result mappings, accepted-consequence composition, event family, commit class, or any other protected-effect domain semantics;
- authentication credentials, session issuance, signature verification, database roles, tables, migrations, row-level security, or infrastructure selection;
- external transport-release eligibility, dispatcher behavior, receiver acknowledgement, or delivery guarantees;
- retention duration, deletion, encryption, redaction, signing-key custody, or recovery-key custody;
- current schemas, accepted RFCs, current/default indexes, OFARM2 runtime code, or production-readiness claims.

If this protocol cannot close without changing one of those boundaries, implementation must stop before that edit and open a linked prerequisite, follow-up, or stacked PR.

---

## 3. Governing inputs and stop conditions

This candidate is constrained by:

- the active Constitution and Platform Runtime baseline, especially assertion/history-first truth, the `EnforcementChain`, current authority re-evaluation, immutable history, and governed commit paths;
- the accepted Authority Policy Model and Agent Actorship RFCs;
- the accepted Event Ingress and Promotion Boundary Closure RFC and its idempotency/replay posture;
- the accepted Source Truth Record Closure RFC and current source-record contracts;
- the approved authorization candidate on PR #11 at exact head `03a21f6`;
- the protected-effect inventory on issue #12; and
- the approved final `ReviewDecision` protected-effect candidate on PR #17 at exact head `9ef0803`.

PR #11 owns the authorization meaning of both `FRESH_HUMAN_APPROVAL_REQUIRED` and `DIRECT_HUMAN_ACTION_REQUIRED`, the exact challenge and approval bindings where fresh approval applies, approver eligibility, `authorityRelevantStateDigest` projection, `decisionValidUntil`, and `SINGLE_USE`. This candidate consumes those decisions and does not reinterpret or collapse them.

PR #17 owns the exact final-review result schema binding, `RD_*` mappings, `PC_*` postconditions, result classification, and protected-effect validation trace. This candidate verifies and atomically consumes that handoff without interpreting ReviewDecision fields independently.

Any semantic change to either approved exact head invalidates the corresponding dependency before machine materialization. A protected-effect family without an approved content-addressed contract remains non-executable even if this transaction protocol is approved.

---

## 4. Current capability and gap inventory

| Current source | Existing capability | Gap this candidate closes or preserves elsewhere |
|---|---|---|
| Platform Runtime baseline | requires every authoritative outcome to cross its applicable `EnforcementChain` gates | does not define an interactive reservation/finalization boundary, atomic commit set, or recovery protocol |
| Authority Policy Model v0.1 | fixes `ALLOW`, `DENY`, `REQUIRE_REVIEW`, and `REQUIRE_HUMAN_APPROVAL`; requires current revocation re-evaluation for long-running flows | current v0.1 records do not bind an exact approval challenge, effect intent, single-use consumption, or transaction deadline |
| Event Ingress and Promotion Boundary Closure v0.1 | defines idempotent request replay and conflicting-replay rejection | does not bind replay to an authorization decision, human approval, protected-effect contract, or atomic consumption |
| `AuthorizationDecisionResult v0.1` | exposes `humanApprovalRequired` and `finalActionPermitted` | a boolean is not an approval, reservation, consumption record, or commit proof |
| `AgentRunApprovalCheckpoint v0.1` | records an agent-run checkpoint and coarse approval state | it does not bind exact effect-intent bytes, display bytes, policy/rule digests, relevant-state equality, independent approver authority, or single-use consumption and cannot serve as v0.2 human approval |
| approved PR #11 candidate | defines exact challenge/approval truth claims, transaction-bound validity, single use, and authorization-side atomicity invariants | deliberately leaves reservation ownership, concurrency, retry, final commit, and recovery to issue #19 |
| approved PR #17 candidate | defines one exact ReviewDecision protected-effect validation handoff and `PC_ATOMIC_EVIDENCE`; its three actions are direct-human-final-action rows under PR #11 | deliberately leaves the shared transaction gate to issue #19 and does not create a fresh-approval challenge requirement |
| current machine-contract set | provides no approval-reservation, finalization-attempt, decision-consumption, or governed-effect-receipt transaction profile | later non-default materialization is required; this Phase A candidate creates none |

The gap is a transaction protocol, not another authorization evaluator, workflow engine, event grammar, or domain contract.

---

## 5. Core protocol stance

### 5.1 Two exact finalization entry modes

The selected PR #11 action rule determines one mode. This transaction protocol cannot substitute the other:

| Human-finalization requirement | Transaction entry | Approval evidence |
|---|---|---|
| `FRESH_HUMAN_APPROVAL_REQUIRED` | reservation and challenge issuance in one short transaction, followed by post-act finalization in a later short transaction | exact challenge, human approval, finalization evidence, and approval consumption are required |
| `DIRECT_HUMAN_ACTION_REQUIRED` | the authenticated natural person performs the exact protected action through one short finalization transaction | direct-human finalization evidence is required; no separate challenge, approver, approval record, or approval consumption is created |

`NOT_REQUIRED` is outside this candidate. This document neither binds that mode to this protocol nor claims its runtime transaction path.

The fresh-approval word “two-stage” does not mean XA, distributed two-phase commit, prepare/commit across services, or an open database transaction between the stages. Its first transaction commits only non-authoritative reservation and challenge evidence. It releases every database lock before the challenge is shown to the human.

### 5.2 A fresh-approval reservation is not authority or a resource lease

An open fresh-approval reservation proves only that one exact operation and challenge were durably registered. Direct-human-final-action rows create no such reservation. A reservation does not:

- produce an `ALLOW` decision;
- freeze grants, revocations, representation, evidence, policy, target state, or pack state;
- reserve a ReviewDecision outcome or other domain result;
- block another actor from changing the governed target;
- guarantee that finalization will remain eligible; or
- authorize any external release.

V0.1 reservations are non-exclusive intent reservations. A protected-effect contract may require exact current-state inputs at finalization, but it cannot turn this generic reservation into a hidden domain lock.

### 5.3 Finalization is the only protected-effect linearization point

The protected effect becomes committed only at the successful atomic finalization commit. Challenge issuance where applicable, display, button activation, human-act receipt, preliminary evaluation, reservation acquisition, transaction start, result construction, and protected-effect validation are not the protected-effect linearization point.

For a filing action whose approved policy selects an outbox posture, the internal outbox commit is the protected filing-effect linearization point. External byte release remains separately governed by issue #13 and is not part of this protocol's atomic internal commit.

### 5.4 History is authoritative; coordination is derived

Reservation issuance, terminalization, finalization attempts, consumption, and receipts are immutable evidence records. An implementation may maintain mutable rows, locks, queues, leases, or indexes for speed, but those are derived coordination state. They must be rebuildable or reconcilable from the immutable records and cannot override a committed receipt.

---

## 6. Logical operation and idempotency identity

### 6.1 Logical operation binding

One logical operation is identified by:

- exactly one operation boundary kind, `TENANT` or `DEPLOYMENT`, and its exact ref;
- authenticated requesting principal identity and immutable resolution binding;
- represented Party and representation basis when applicable;
- requested action class;
- exact rule-selected human-finalization requirement;
- rule-selected effect-intent schema identity;
- exact `effectIntentDigest`; and
- caller-supplied `operationIdempotencyKey` scoped as defined below.

The future transaction profile must compute `operationBindingDigest` as `sha256:` plus SHA-256 over RFC 8785 JCS bytes of this exact object:

```json
{
  "schemaVersion": "ofarm.governedHumanFinalizationOperationBinding.v0.1",
  "operationBoundary": {
    "kind": "TENANT",
    "ref": "..."
  },
  "requestingPrincipalBinding": {},
  "representedPartyBinding": null,
  "actionClass": "...",
  "humanFinalizationRequirement": "DIRECT_HUMAN_ACTION_REQUIRED",
  "effectIntentSchemaBinding": {},
  "effectIntentDigest": "sha256:...",
  "operationIdempotencyKey": "..."
}
```

`operationBoundary`, `requestingPrincipalBinding`, `representedPartyBinding`, and `effectIntentSchemaBinding` are complete contract-defined objects, not untyped or ref-only aliases. `operationBoundary.kind` is exactly `TENANT` or `DEPLOYMENT`. `humanFinalizationRequirement` is the exact rule-selected `FRESH_HUMAN_APPROVAL_REQUIRED` or `DIRECT_HUMAN_ACTION_REQUIRED` value for this candidate. When representation does not apply, `representedPartyBinding` is exactly JSON `null`; omission and empty objects are invalid. No member is excluded from this digest.

### 6.2 Idempotency scope

The authoritative idempotency scope is the tuple:

```text
(operationBoundaryKind, operationBoundaryRef, authenticatedRequestingPrincipalRef,
 representedPartyRef-or-null, actionClass, humanFinalizationRequirement,
 operationIdempotencyKey)
```

That tuple maps to exactly one `operationBindingDigest` and is never rebound under v0.1. A retry with the same tuple and digest retrieves the existing lifecycle state or committed receipt. The same tuple with a different digest is a conflicting replay and can never create another reservation or effect. Evidence-retention policy may govern bulky challenge or display bytes, but it must preserve enough immutable binding or tombstone evidence to prevent unsafe tuple reuse while the operation can be replayed or its committed result/outbox remains part of history.

For fresh approval, policy, rule, challenge, snapshot, and display bindings belong to a reservation generation, not the logical operation digest. If one reservation becomes terminal without an effect because its policy, challenge, display, or relevant state became stale, the same logical operation may receive a new sequential reservation generation under current bindings. Generations cannot overlap, and the logical operation can still commit at most once. Direct-human finalization has no reservation generation; an exact retry is resolved through the logical operation and final transaction attempt.

### 6.3 Immutable identifiers

The protocol binds distinct immutable identifiers for:

- logical operation;
- reservation generation and approval challenge when fresh approval applies;
- human-act submission;
- finalization attempt;
- final transaction attempt;
- authorization decision bundle;
- decision consumption and, when fresh approval applies, approval consumption;
- protected result or outbox entry; and
- governed-effect receipt.

No identifier may resolve to two byte sequences. A retry reuses the applicable existing identifier and result; it does not mint a second identity merely because the response was lost.

---

## 7. Fresh-approval reservation lifecycle

This section applies only when the selected action rule requires `FRESH_HUMAN_APPROVAL_REQUIRED`. A `DIRECT_HUMAN_ACTION_REQUIRED` operation skips this section and can neither claim nor consume a reservation or separate approval.

### 7.1 Derived reservation states

One reservation generation has exactly one derived state:

| State | Meaning |
|---|---|
| `OPEN` | challenge is committed, unexpired, uncancelled, and no terminal finalization exists |
| `FINALIZED` | the logical operation committed successfully and the receipt is authoritative |
| `INVALIDATED` | a human act or finalization attempt established that the challenge can no longer be used, including relevant-state drift |
| `CANCELLED` | an allowed cancellation terminalized the reservation before commit |
| `EXPIRED` | trusted time reached the exclusive reservation or challenge cutoff before successful commit |

`FINALIZING` is not a durable semantic state. It may be a short-lived operational lock while a final transaction is active. A crash cannot leave an authoritative reservation permanently finalizing.

An unresolved `OUTCOME_UNKNOWN` attempt blocks any new finalization, cancellation, expiry terminalization, or replacement generation until reconciliation establishes whether the operation is `FINALIZED` or no effect committed.

### 7.2 Reservation generation rules

- At most one generation for a logical operation is `OPEN`.
- `FINALIZED` is terminal for the logical operation, not only the generation.
- `INVALIDATED`, `CANCELLED`, or `EXPIRED` permits a later generation only for the same `operationBindingDigest` and only after the prior terminal record is durable.
- A replacement generation gets a new reservation and challenge identity and re-renders current display bytes under current policy.
- A human act is valid only for the exact challenge and generation it names.
- No transition deletes or rewrites an earlier reservation, challenge, act, attempt, or outcome.

### 7.3 Expiry

The reservation's exclusive `reservationExpiresAt` must be no later than the rule-owned `challengeExpiresAt`. Both are computed from trusted policy and runtime cutoffs; the caller cannot extend either. An act received at or after either exclusive cutoff cannot enter successful finalization.

Reservation expiry does not produce `DENY`. It is a protocol fact. If a new generation is requested, authorization and challenge issuance start again under current state.

---

## 8. Fresh-approval stage one: reservation and challenge issuance

This stage exists only for `FRESH_HUMAN_APPROVAL_REQUIRED`.

One short reservation transaction must perform this sequence:

1. validate the request and the rule-selected effect-intent schema, then compute and verify `effectIntentDigest` and `operationBindingDigest`;
2. resolve the tenant/deployment scope and the authenticated requesting principal through the trusted principal boundary;
3. resolve the exact intended authenticated natural-person approver and preliminary representation binding;
4. verify the complete operation-boundary/requester/representation/action/human-finalization-scoped idempotency tuple, returning an existing matching lifecycle or rejecting a conflicting replay;
5. resolve and digest-verify the exact governed transaction policy selected by the governed runtime-surface binding and bind it to this reservation generation;
6. evaluate the requesting path and the intended approver's preliminary same-action natural-person path under the exact PR #11 rule without treating either preliminary result as a consumable final decision;
7. construct the rule-owned challenge authority snapshot and exact `authorityRelevantStateDigest` projection;
8. render and content-address the exact human-visible representation under the rule-bound renderer, display, locale, timezone, media, and retention bindings;
9. compute `challengeExpiresAt` and `reservationExpiresAt` from the exact governed cutoffs;
10. atomically append the operation/idempotency binding when new, reservation-generation evidence, approval challenge, display-evidence binding, and governed transaction-policy binding; and
11. return or expose the challenge only after that transaction commits.

If the preliminary requesting or approver path is ineligible, the authorization boundary records its truthful outcome under PR #11. This protocol does not issue an `OPEN` reservation by converting `DENY`, `REQUIRE_REVIEW`, malformed input, or unresolved principal state into an approval opportunity.

The reservation transaction ends before human-visible bytes are presented. No database snapshot, row lock, advisory lock, transaction-local token, or uncommitted decision survives into human think time.

---

## 9. Human act and shared finalization entry

### 9.1 Exact act binding

Every mode binds:

- logical-operation identity and `operationBindingDigest`;
- human-act submission identity and complete act digest;
- authenticated-session evidence resolved by the trusted principal boundary;
- exact natural-person principal and representation binding;
- exact action, human-finalization requirement, effect-intent schema, and `effectIntentDigest`; and
- any signature or attestation evidence required by the rule.

Fresh-approval finalization additionally binds:

- reservation-generation identity;
- exact challenge identity and immutable revision;
- the exact intended approver;
- the exact displayed representation ref/digest acknowledged by the human;
- rule-owned challenge/final relevant-state bindings; and
- challenge and reservation cutoffs.

Direct-human finalization instead requires the authenticated natural person to be the direct requesting principal for the exact protected action. It carries no reservation, challenge, separate approver, approval identity, or approval-consumption claim. A sponsor approval, agent-presented confirmation, or approval obtained by another person cannot satisfy `DIRECT_HUMAN_ACTION_REQUIRED`.

The human-act submission is not authority by itself. A bare boolean, UI event, client timestamp, sponsor reference, agent assertion, copied approval ID, or signature over different bytes cannot enter finalization.

One `humanActSubmissionId` maps to one complete act digest within the logical operation and, for fresh approval, its reservation generation. An exact retry reuses it. The same ID with different bytes, or a different affirmative act after one has been durably admitted for the applicable operation/generation, is a conflict. A fresh-approval mode creates a consumable human-approval/finalization profile only from that exact act inside a finalization transaction. A direct-human mode records direct-human finalization evidence instead. In neither mode does the raw act become portable authority.

Trusted `humanActedAt` is the server-observed act time under the authenticated boundary. For fresh approval it must precede the exclusive challenge and reservation cutoffs. For direct-human finalization it must fall within the authenticated session and final transaction cutoffs selected by PR #11 and this protocol. Client time may be retained as non-authoritative telemetry but cannot establish timeliness.

### 9.2 Finalization admission

Before evaluating authority or a domain result, finalization must:

1. start a short transaction under the bound transaction policy;
2. acquire the operation, idempotency, decision-consumption, and prospective-result uniqueness guards needed for this attempt;
3. return the existing receipt for an exact retry of an already committed logical operation;
4. reject a different operation digest, act, consumer, or prospective result as a conflict; and
5. verify the rule-selected human-finalization mode without allowing caller substitution.

Fresh approval additionally acquires reservation and approval-consumption guards, resolves the current reservation state, and admits only the exact act against an `OPEN` generation. It rejects an `INVALIDATED`, `CANCELLED`, or `EXPIRED` generation without changing that terminal state.

Direct-human finalization admits no reservation or separate approval reference. It requires the direct authenticated principal and exact act to enter the same transaction that performs final authorization and protected-effect commit.

---

## 10. Trusted transaction time, snapshot, and cutoff inputs

### 10.1 Transaction policy ownership

The finalization transaction uses the exact immutable `governedTransactionPolicyRef` and digest selected by the governed runtime-surface binding. For fresh approval, that binding was committed with the reservation generation; a different binding invalidates the generation and requires a new one. For direct-human finalization, the binding is fixed with the logical operation at transaction admission. Neither mode permits caller selection or silent substitution. The policy is owned by this runtime-integration boundary and specifies:

- the trusted time source;
- the exact transaction-deadline calculation or trusted deadline source;
- for fresh approval, the exact reservation-expiry calculation and its relationship to the rule-owned challenge cutoff;
- the supported atomic persistence boundary;
- the isolation and commit-guard proof obligation;
- the authoritative commit-status lookup mechanism;
- the idempotency and uniqueness scope; and
- the permitted recovery and reconciliation states without defining retention or key custody.

The policy cannot change authorization eligibility or domain mappings. A mutable, missing, caller-selected, or digest-invalid transaction policy makes the lifecycle non-executable.

### 10.2 Trusted finalization inputs

At transaction start, the runtime supplies these trusted values to the authorization and gate evaluators:

- `transactionAttemptId`;
- `transactionStartedAt`;
- exclusive `transactionDeadline`;
- `transactionSnapshotRef` and snapshot digest or equivalent immutable proof;
- atomic persistence boundary identity;
- isolation/commit-guard mode and immutable policy binding;
- exact currentness watermarks or predicate-version guards needed for negative and set-valued facts; and
- the current transaction-status lookup key.

The caller, requesting agent, approver, UI, and domain result cannot choose or extend those values.

The future transaction policy must bind an exact deadline calculation, but this Phase A candidate does not invent one universal wall-clock duration. `transactionDeadline` is fixed before final authorization evaluation and contributes to PR #11's exact `decisionValidUntil` minimum. Successful commit time must be earlier than both values.

### 10.3 Snapshot and commit guard

A finalization read snapshot alone is insufficient if relevant state can change before commit. The transaction must use one of the exact modes admitted by its content-addressed policy:

- a serializable transaction whose conflict detection covers the complete relevant read and write set;
- explicit locks or version guards covering the complete relevant read and write set; or
- optimistic compare-and-commit guards over exact immutable revisions, set-completeness watermarks, and predicate versions.

The policy must name one mode and its proof fields. An implementation cannot claim equivalence from an undocumented isolation level.

Negative facts such as “no active revocation exists” require a guarded registry revision, range/predicate version, or other contract-defined completeness watermark. Locking only the positive grant records is insufficient.

If any current input or required success-set write cannot participate in, or be protected by, the bound atomic boundary and complete guard, successful finalization is unsupported. A compensating saga that briefly exposes a protected effect without its decision, finalization, consumption, and receipt evidence does not satisfy this protocol. Asynchronous caches and projections are allowed only as derived views of an already atomic authoritative commit.

---

## 11. Required post-act revalidation

After the human act and inside the finalization transaction, the runtime must re-resolve and re-evaluate every current fact that can change authority, human-finalization validity, protected-effect validity, or another applicable gate, including:

- authenticated principal and session validity;
- represented Party and representation basis;
- for fresh approval, intended approver identity, same-action natural-person eligibility path, and separation posture;
- for direct-human finalization, the direct natural-person principal posture required by the action rule;
- role assignments and anchor scopes;
- AuthorityGrant, DelegationGrant, source grant, and SharingGrant inputs where applicable;
- all applicable revocation records and completeness watermarks;
- action policy, rule, extractor, intent schema, and protected-effect contract bindings;
- governed runtime-surface and transaction-policy bindings;
- authority target, typed inputs, effect subject, immutable resource revisions, scope, twin, purpose, and tenant;
- evidence identity, eligibility, freshness, dispute, supersession, and policy state;
- data-sovereignty and other rule-selected applicability state;
- for fresh approval, challenge, display bytes, renderer, display policy, locale, timezone, evidence-retention binding, and the rule-owned `authorityRelevantStateDigest` projection;
- protected-effect state inputs and prospective result identifiers; and
- every other applicable `EnforcementChain` gate input.

For fresh approval, the final authority-relevant projection digest must equal the challenge digest exactly. If it differs, the human act is invalidated for this generation even if a new authorization evaluation might otherwise allow the action. A new challenge is required so the human sees and approves the current governed representation.

For direct-human finalization, there is no challenge digest to compare. The exact current state is evaluated and guarded inside the same short transaction as the human act and protected effect. Creating a synthetic challenge or using another person's approval would change the PR #11 posture and is prohibited.

In the fresh-approval mode, unrelated canonical history may advance without invalidating the challenge only when the exact rule-owned relevant-state projection excludes it and every final transaction guard still passes. This protocol cannot locally decide that a changed field is irrelevant.

The final transaction guard covers the complete revalidated state, including protected-effect and non-authorization gate inputs. It is therefore broader than the challenge/final authority-relevant digest comparison and must remain stable through commit.

---

## 12. Protected-effect transaction handoff

### 12.1 Required handoff

Every human-finalized state-affecting action entering this protocol must supply one rule-bound, digest-verified protected-effect contract handoff containing:

- action rule, effect-intent schema, and exact `effectIntentDigest`;
- protected-effect contract ID, version, ref, digest, and owning domain family;
- result-schema ref, version, and digest owned by that contract;
- every proposed result or outbox identity, complete bytes, and digest;
- every immutable domain state input revision/digest and required absence or uniqueness guard;
- the complete contract-owned mapping and postcondition validation trace;
- the overall contract-validation disposition;
- event-family and commit-class values supplied by the domain contract and active Event Grammar; and
- any separately approved composition binding and complete companion result set.

This handoff is structural transaction input, not a second domain authority. The transaction gate verifies identities, digests, dispositions, completeness, and stable state guards. It does not recompute or reinterpret domain mappings.

### 12.2 Handoff admission

The handoff is admitted only when:

- the authorization rule binds that exact protected-effect contract;
- all refs resolve to immutable bytes whose digests match;
- the result validates under the contract-owned result schema;
- every required mapping and postcondition has the contract-permitted truthful disposition;
- the overall protected-effect disposition is `PASS`;
- every proposed write and required absence is represented in the final commit set and transaction guard; and
- no unbound side effect, companion, current-state update, or external dispatch is present.

Authorization `ALLOW` never bypasses this handoff. Protected-effect failure leaves the authorization outcome truthful and unchanged, commits no protected result or consumption, and is recorded as a separate gate failure when durable failure evidence can be written.

### 12.3 Unsupported effects

Approval of this protocol does not make every issue #12 action executable. A state-affecting rule without its own approved protected-effect contract, result-schema binding, validation trace, and transaction handoff is unsupported and cannot enter successful finalization.

---

## 13. Successful finalization and atomic commit set

### 13.1 Finalization order

One successful finalization transaction performs this exact order:

1. admit and guard the exact logical operation and human act plus, for fresh approval, the open reservation and challenge under section 9;
2. establish trusted time, deadline, snapshot, policy, and complete currentness guards under section 10;
3. perform every post-act revalidation plus the challenge/final relevant-state comparison when fresh approval applies under section 11;
4. create the final authorization request/result/trace bundle under the approved PR #11 semantics;
5. require the final authority outcome and human-finalization disposition needed for the protected action;
6. build the proposed result and evaluate every applicable non-authorization `EnforcementChain` gate;
7. validate the complete protected-effect handoff under section 12;
8. construct mode-correct finalization evidence, single-use decision consumption, fresh-approval consumption and reservation terminalization where applicable, and the governed-effect receipt;
9. recheck the transaction deadline, `decisionValidUntil`, complete commit guard, and every uniqueness constraint; and
10. commit the complete success set atomically, then expose the receipt.

No successful component is durably visible before step 10.

### 13.2 Required atomic success set

The success commit contains, as applicable:

- final authorization request, result, and full internal trace evidence plus their `decisionBundleDigest`;
- finalization evidence bound to the exact act and final snapshot, plus exact challenge, display, approver, and approval bindings only for fresh approval;
- exactly one decision consumption record and, for fresh approval, exactly one approval consumption binding;
- exactly the protected result set admitted by the protected-effect contract and any separately approved composition;
- protected-effect and other applicable gate validation traces;
- exactly one reservation-success terminal record when fresh approval applies;
- exactly one governed-effect receipt; and
- for an approved outbox posture, the exact immutable outbox entry rather than an external send.

For fresh approval, the challenge, display evidence, and original reservation were committed in stage one and are referenced by immutable ref/digest; they are not rewritten in the success transaction. Direct-human finalization has none of those records.

### 13.3 Governed-effect receipt minimum

The governed-effect receipt must bind at least:

- logical operation, idempotency scope, human-finalization requirement, human act, finalization attempt, and transaction attempt, plus reservation and challenge only when fresh approval applies;
- trusted human-act, transaction-start, and commit times plus the transaction deadline;
- transaction policy, atomic persistence boundary, snapshot, isolation/guard proof, and complete guard digest;
- authorization decision bundle and mode-correct finalization-evidence refs/digests;
- decision consumption and, where applicable, approval-consumption refs/digests;
- effect-intent schema and exact `effectIntentDigest`;
- protected-effect contract and result-schema refs/digests;
- every committed result/outbox ref/digest and every protected-effect validation-trace ref/digest;
- every other applicable gate trace and disposition;
- the complete atomic commit-set membership; and
- final protocol outcome `EFFECT_COMMITTED`.

The receipt does not claim external delivery, receiver acceptance, current-state materialization, or another domain effect absent from the committed set.

The later evidence schema must define one exact RFC 8785 JCS/SHA-256 receipt projection and exclude only its one top-level digest member. This Phase A candidate does not create that schema.

---

## 14. Single-use consumption and concurrency

### 14.1 Consumption linearization

Decision consumption and, for fresh approval, approval consumption become durable only in the successful atomic commit. A provisional in-transaction reservation of uniqueness is not a committed consumption. If the transaction conclusively rolls back, no consumption claim exists and any retry must re-enter current finalization checks.

A failed attempt record is not a consumable approval or direct-human finalization. In fresh-approval mode, the same exact human-act submission may enter a later attempt only while its reservation remains `OPEN`, the challenge and act remain unexpired, and all final checks are repeated. In direct-human mode, an exact retry of the same act may enter another short transaction only while the trusted session and action cutoffs remain valid. The later transaction creates its own mode-correct finalization evidence bound to its own final snapshot and deadline; it never rewrites a failed-attempt record or reuses a previously committed finalization identity.

Each applicable consumption record binds:

- authorization decision bundle;
- mode-correct human finalization evidence;
- logical operation and, where applicable, reservation generation;
- exact consumer principal;
- `effectIntentDigest`;
- committed result/outbox and receipt;
- trusted consumption time; and
- `SINGLE_USE` posture.

### 14.2 Required uniqueness

The atomic boundary must enforce all of these logical uniqueness rules:

- one idempotency-scope tuple maps to one logical operation digest;
- at most one `OPEN` reservation generation exists per logical operation where fresh approval applies;
- at most one successful receipt exists per logical operation;
- one authorization decision bundle is consumed at most once;
- one human approval is consumed at most once where fresh approval applies;
- one reservation generation finalizes successfully at most once where fresh approval applies; and
- every protected result ID or outbox ID maps to one immutable byte sequence.

Application-level “check then insert” without an atomic uniqueness or commit guard is not sufficient.

### 14.3 Concurrent finalizers

When matching retries race, one transaction may commit. Every loser must resolve the winning receipt and return that same result after verifying the operation and effect digests.

When conflicting consumers, human acts, operation digests, or prospective result bytes race, at most one can commit. A loser reports a protocol conflict and cannot borrow the winner's receipt.

When two different logical operations target the same mutable domain state, the domain-state and relevant-set guards determine compatibility. If one commit changes state relevant to the other, the other must abort. For fresh approval, a change to the rule-owned challenge projection requires a new challenge; when that projection is unchanged, retry still requires complete final revalidation. Direct-human retry always requires a still-valid exact act and complete final revalidation.

---

## 15. Failure and no-effect commits

### 15.1 Truthful outcome separation

The protocol uses three top-level finalization-result classes:

| Result class | Meaning |
|---|---|
| `EFFECT_COMMITTED` | the complete success set committed atomically |
| `NO_EFFECT` | the runtime conclusively established that no protected effect or consumption committed |
| `OUTCOME_UNKNOWN` | the caller/runtime cannot yet establish whether the success commit occurred |

These are transaction results, not authorization outcomes or RuntimeProblem public reason codes.

Every durable fresh-approval `NO_EFFECT` finalization attempt also records exactly one reservation consequence: `REMAINS_OPEN`, `INVALIDATED`, `EXPIRED`, or `CANCELLED`. Direct-human attempts record `NOT_APPLICABLE` because no reservation exists. `OUTCOME_UNKNOWN` records no terminal reservation consequence until reconciliation. A failure cannot leave the protocol to guess whether the same challenge may be retried.

### 15.2 Known no-effect cases

| Condition | Required behavior | Reservation consequence by mode |
|---|---|---|
| malformed input or invalid rule/intent binding | ingress rejection; no authorization outcome, reservation, consumption, or effect | no reservation is created or changed; direct-human mode uses `NOT_APPLICABLE` |
| preliminary authorization or approver path cannot reach the fresh-approval lifecycle | preserve its exact authorization outcome; no open reservation or effect | no reservation is created |
| reservation or challenge is expired | `NO_EFFECT`; do not rewrite it as `DENY` | `EXPIRED` |
| reservation is already cancelled | `NO_EFFECT`; do not rewrite it as `DENY` | `CANCELLED` |
| unauthenticated, wrong-principal, wrong-challenge, or malformed act attempt | reject without revealing or consuming the valid challenge | `REMAINS_OPEN` if it was otherwise open and unexpired |
| intended principal submits the wrong display, intent, Party, or representation binding | reject the act; no effect or consumption | `REMAINS_OPEN` if the exact valid act may still arrive before expiry |
| final authority outcome is non-`ALLOW` | preserve that outcome and its evidence; no effect or consumption | `INVALIDATED` for fresh approval; `NOT_APPLICABLE` for direct-human mode |
| fresh-approval challenge/final `authorityRelevantStateDigest` differs | require a new challenge; no effect or consumption | `INVALIDATED` |
| protected-effect or another semantic gate proves that the approved intent, display, or relevant guarded state is stale or mismatched | preserve the authority-gate result and record the separate gate failure | `INVALIDATED` for fresh approval; `NOT_APPLICABLE` for direct-human mode |
| result construction or semantic-gate validation fails without changing the approved intent and while every relevant binding and guard remains current | preserve the authority-gate result; commit no effect or consumption and repeat every check before retry | `REMAINS_OPEN` until the existing cutoff for fresh approval; `NOT_APPLICABLE` for direct-human mode |
| transaction deadline, serialization, or persistence guard fails with conclusive rollback and the human act remains current | `NO_EFFECT`; resolve status and repeat all checks before retry | `REMAINS_OPEN` until the existing cutoff for fresh approval; `NOT_APPLICABLE` for direct-human mode |
| conflict establishes a relevant guarded-state change | `NO_EFFECT`; do not retry under stale human finalization | `INVALIDATED` for fresh approval; `NOT_APPLICABLE` for direct-human mode |
| failure-evidence persistence fails | no effect; return a runtime/persistence failure without claiming a durable finalization record | no new consequence claim; existing authoritative reservation evidence controls for fresh approval, otherwise `NOT_APPLICABLE` |

A durable no-effect attempt may atomically record the exact authorization result, gate failure, and attempt evidence without a consumption or protected result. It must be tagged non-consumable and cannot later be upgraded in place to a success record.

### 15.3 No authorization-result rewriting

If authorization evaluates to `ALLOW` but protected-effect validation fails, the audit may truthfully record authorization `ALLOW` and domain-gate `FAIL`. It must not rewrite `ALLOW` to `DENY`, claim that the effect committed, or make that transaction-bound decision portable to another attempt.

If the transaction fails before a decision bundle is durably recorded, later audit evidence may describe only what can be proven about the attempt. It cannot fabricate a durable authorization result from logs or caller memory.

---

## 16. Retry, crash recovery, and uncertain commit

### 16.1 Retry rule

Every retry first performs authoritative lookup by the complete operation-boundary/requester/representation/action idempotency tuple, logical operation, transaction attempt, consumption, and receipt identifiers plus reservation/challenge identifiers where fresh approval applies. It does not begin by rebuilding or applying the effect.

- A matching committed receipt is returned as the prior success.
- A conclusively aborted fresh-approval attempt may retry only while the reservation, challenge, and act remain eligible and after all finalization checks are repeated.
- A conclusively aborted direct-human attempt may retry only as the exact same act under a still-valid trusted session and after all finalization checks are repeated.
- A terminal fresh-approval generation requires a new reservation generation where section 7 allows one; direct-human mode has no generation to reopen.
- A conflicting operation digest or result is rejected.
- An unresolved attempt remains `OUTCOME_UNKNOWN`; no effect is reapplied.

### 16.2 Crash-boundary behavior

| Crash or loss point | Recovery rule |
|---|---|
| before fresh-approval stage-one commit | no reservation exists; exact request may be retried |
| after fresh-approval stage-one commit but before challenge response | retrieve the committed matching challenge; do not create another open generation |
| after fresh-approval challenge display but before human act | reservation remains open until cancellation, invalidation, expiry, or finalization |
| after either mode's act submission but before finalization commit | resolve the attempt by idempotency and transaction status; never infer success from UI completion |
| direct-human request is lost before its finalization transaction begins | no final decision or effect exists; the exact authenticated act may be retried only under a still-valid session |
| before final success commit with conclusive rollback | no consumption/effect exists; re-enter all final checks before retry |
| after success commit but before response | retrieve and return the authoritative receipt; do not consume or apply again |
| during external send | outside this internal protocol; use the committed outbox plus the separate issue #13 release and transport receipt rules |

### 16.3 Uncertain commit resolution

When the final commit response is lost or ambiguous, the runtime records or returns `OUTCOME_UNKNOWN` and enters reconciliation. Reconciliation must query the authoritative atomic store or commit-status mechanism bound by the transaction policy for:

- the exact governed-effect receipt;
- decision consumption and, where fresh approval applies, approval consumption;
- reservation-success terminal record where fresh approval applies;
- protected result or outbox ID/digest; and
- transaction-attempt status.

If the complete matching success set exists, reconciliation returns `EFFECT_COMMITTED` and the existing receipt. If authoritative status proves rollback and none of the success set exists, it returns `NO_EFFECT`. Until one conclusion is established, the operation stays blocked from reapplication.

A partial success set is an invariant breach, not a retry signal. The runtime must quarantine the operation for governed repair and must not synthesize missing evidence, delete the visible effect, or replay the effect automatically. Repair authority, database recovery, and operator break-glass procedures require their own governed implementation boundary.

---

## 17. Fresh-approval cancellation, expiry, and orphan cleanup

Reservation cancellation, expiry, and replacement in this section apply only to `FRESH_HUMAN_APPROVAL_REQUIRED`. Direct-human finalization has no reservation to cancel, expire, reopen, or clean up; its transaction deadline and session validity are checked within each attempt.

### 17.1 Cancellation

Before a successful commit, an `OPEN` reservation may be cancelled by:

- the same currently authenticated requesting principal under the same operation boundary and representation binding; or
- a separately authorized administrative/recovery operation whose authority semantics are not created by this candidate.

Cancellation appends an immutable terminal record and requires the current reservation generation. It grants no authority and does not erase challenge or act evidence. A stale cancellation racing a successful finalization loses to the authoritative committed receipt. No cancellation in this protocol recalls or reverses a committed protected effect.

### 17.2 Automatic expiry

Trusted expiry processing may append an `EXPIRED` terminal record after the exclusive cutoff when no success receipt exists. Expiry processing must use the same operation/reservation uniqueness guards as finalization so it cannot race into a false expiry after commit.

### 17.3 Orphan cleanup

Cleanup may release derived locks, queue entries, temporary render caches, or coordination leases only after authoritative state reconciliation. It does not delete or rewrite immutable reservation, challenge, act, attempt, consumption, result, or receipt evidence.

Retention and governed deletion of evidence bytes remain owned by issue #14 and its future policy. This protocol requires truthful refs/digests and lifecycle state but does not choose retention duration or key custody.

---

## 18. Evidence-profile ownership

This candidate adds no machine schema. Later materialization must keep record ownership explicit:

| Evidence or record | Semantic owner | Transaction obligation |
|---|---|---|
| authorization request/result/full trace | approved PR #11 authorization boundary | create under final snapshot; bind and commit according to success or truthful no-effect posture |
| approval challenge and human approval evidence | approved PR #11 authorization/finalization-evidence boundary | fresh approval only: stage-one challenge is immutable and final approval binds the exact act and final state |
| direct-human finalization evidence | approved PR #11 authorization/finalization-evidence boundary | direct-human only: bind the direct authenticated natural person, exact act, final state, and rule-selected posture without a challenge or separate approval |
| reservation generation | issue #19 transaction boundary | fresh approval only: record identity, lifecycle transition, and non-authority posture |
| finalization attempt | issue #19 transaction boundary | record the mode, logical operation, transaction attempt, and truthful outcome for either mode |
| decision consumption and conditional approval consumption | PR #11 finalization-evidence package with issue #19 atomicity and uniqueness rules | commit decision consumption exactly once only with successful effect/outbox; add approval consumption only for fresh approval |
| protected result and validation trace | applicable issue #12 domain contract; PR #17 for final ReviewDecision | admit only exact passing handoff and commit exact validated bytes |
| governed-effect receipt | issue #19 transaction boundary, later carried by the shared finalization-evidence package | bind the complete atomic set and transaction proof without inventing domain semantics |
| semantic event, ingress result, and promotion trace | active Event Grammar and Event Ingress boundary where applicable | reference exact committed domain/evidence records and truthful gate outcomes |
| external transport-release and delivery receipt | issue #13 and later transport boundary | not part of this internal finalization commit except by immutable outbox reference |
| retention/encryption/deletion/key-custody evidence | issue #14 and later custody boundaries | consumed only by immutable policy ref/digest; not defined here |

Reservation, finalization-attempt, fresh-approval, direct-human-finalization, conditional approval-consumption, decision-consumption, and governed-effect-receipt profiles should be tagged additions within the already proposed `AuthorizationFinalizationEvidence v0.2` package unless machine-schema review proves that the package cannot represent their distinct truth claims. Mode-inapplicable fields and records must be absent rather than populated with synthetic challenge, approver, approval, reservation, or approval-consumption values. The profiles must not become a new authorization policy registry or a mutable workflow-state source.

PR #11 already proposes `EvidenceEvent` and `evidence record` for its decision/finalization evidence package. Later materialization may carry the transaction profiles through that same package and classification only if schema review proves the new truth claims fit it without changing Event Grammar. Otherwise work must stop for a separate classification amendment. This candidate creates no new event family or commit class, and its evidence cannot create domain current state or promotion by itself.

---

## 19. Concrete final ReviewDecision handoff

The approved PR #11 rows for all three final-review actions select agent posture `HUMAN_ONLY` and human-finalization requirement `DIRECT_HUMAN_ACTION_REQUIRED`. The transaction therefore starts from the exact act of the direct authenticated natural person and performs final authorization, protected-effect validation, and atomic commit in one short transaction. It creates no reservation, challenge, intended-approver record, separate human approval, approval-consumption record, or reservation terminal record. Routing this path through a sponsor approval or fresh-approval challenge would alter PR #11 authorization semantics and is prohibited.

For the first concrete protected-effect handoff candidate, finalization consumes exactly:

- action `REVIEW_ACCEPT`, `REVIEW_REJECT_OR_CONTEST`, or `REVIEW_SUPERSEDE` under the approved PR #11 rule;
- intent profile `EI_REVIEW_DECISION_V0_2` and exact `effectIntentDigest`;
- protected-effect contract ID `ofarm.protectedeffect.reviewdecision.final.v0.1`, version, ref, and digest;
- the contract-owned future `ReviewDecision v0.2` result-schema binding;
- exactly one proposed immutable ReviewDecision result;
- the complete `RD_*` mapping and `PC_*` postcondition trace with overall `PASS`;
- trusted finalization evidence providing the deciding Party, authenticated human principal, exact human-act time, and immutable evidence binding; and
- the exact target, evidence, scope, rationale, outcome, optional lineage, and permitted companion posture already owned by PR #17.

The transaction protocol does not inspect ReviewDecision fields through a second mapping table. It verifies the contract/result/trace bindings and commits the exact validated bytes.

Absent a separately approved accepted-consequence contract and composition binding, the committed set contains no companion consequence. This candidate neither creates that composition nor infers permission from `REVIEW_ACCEPT`.

The successful atomic set for a standalone final review contains the exact ReviewDecision, final authorization request/result/trace, direct-human finalization evidence, exactly one decision-consumption record, passing protected-effect trace, governed-effect receipt, and any separate event-ingress evidence required by the active path. It contains no approval consumption, reservation terminal record, companion consequence, or current-state materialization.

---

## 20. Other protected-effect families

The issue #12 inventory names independently governed observation/evidence-link, assertion, intervention/execution-report, review-request, pack, output, sharing, and revocation boundaries. For a future protected-effect family whose exact approved PR #11 action rule selects `FRESH_HUMAN_APPROVAL_REQUIRED` or `DIRECT_HUMAN_ACTION_REQUIRED`, this protocol supplies only these common transaction obligations:

- exact rule-bound effect intent;
- exact content-addressed protected-effect contract;
- complete proposed result set and state guards;
- passing contract-owned trace;
- atomic evidence/consumption/result/receipt commit; and
- the retry and recovery rules in this candidate.

It does not supply their missing result carriers, mappings, derivations, event/commit classifications, postconditions, authority actions, external release rules, or composition semantics. It makes no transaction-path claim for `NOT_REQUIRED` actions. Each human-finalized family remains blocked until its own child issue and PR closes the protected-effect facts. A later family-specific requirement may extend this protocol only through a separate reviewed amendment if the common handoff is genuinely insufficient.

---

## 21. Production-reachable hostile cases

| Case | Required disposition |
|---|---|
| fresh-approval runtime leaves a database transaction or row lock open while the human considers the challenge | protocol conformance failure; no v0.1 lifecycle claim |
| fresh-approval reservation is treated as authority, approval, a domain-state lock, or proof finalization will pass | conformance failure; reservation has no such effect |
| same idempotency tuple is replayed with different intent, principal binding, Party binding, schema, or action | conflicting replay; no new reservation or effect |
| exact fresh-approval stage-one retry occurs after commit but before challenge response | return the existing challenge and open generation |
| two fresh-approval reservation generations are open for one logical operation | uniqueness failure; neither may silently supersede the other |
| wrong principal, sponsor, organization, agent, session, or representation submits the act | finalization admission fails; no effect or consumption |
| direct-human action is routed through a sponsor, intended approver, separate approval, or synthetic challenge | rule-mode binding failure; no effect or consumption |
| fresh-approval human acknowledges display bytes or renderer metadata different from the challenge | act binding fails; no effect or consumption |
| fresh-approval act arrives at exactly `challengeExpiresAt` or `reservationExpiresAt` | expired because cutoffs are exclusive |
| caller time is used instead of trusted `humanActedAt` | protocol conformance failure |
| fresh-approval challenge and final authority-relevant digests differ but current evaluation would still allow | invalidate the generation and issue a new challenge; no effect |
| fresh-approval unrelated history advances outside the exact relevant-state projection and all guards remain valid | challenge is not invalidated solely for that unrelated change |
| active revocation is inserted after final read but before commit and negative lookup is not predicate/watermark guarded | commit-guard conformance failure |
| role, representation, grant, delegation, resource, evidence, policy, or approval state changes after act | final current-state revalidation or commit guard blocks the effect |
| transaction-policy ref/digest or rule-selected human-finalization mode is substituted after operation binding | binding failure; no effect or consumption |
| transaction deadline or `decisionValidUntil` is caller-selected or extended by an act | binding failure; no consumable decision |
| commit occurs at exactly either exclusive deadline | transaction fails; no success claim |
| authorization `ALLOW` is used without a passing protected-effect trace | no effect; protected-effect gate fails |
| protected-effect validation fails and runtime rewrites authorization to `DENY` | conformance failure; preserve the authority-gate result |
| ReviewDecision bytes differ from the PR #17 validated result digest | transaction handoff or final guard fails |
| ReviewDecision commit adds an unbound companion consequence | protected-effect/atomic-set failure; no commit |
| result ID already exists with different bytes | uniqueness conflict; no overwrite or second result |
| two matching finalization retries race | one commit; loser returns the same verified receipt |
| two different acts or consumers race for one decision or fresh approval | at most one commit; loser receives conflict and cannot reuse receipt |
| provisional consumption commits before the effect and the effect later fails | atomicity violation |
| effect is visible without decision/finalization/consumption/receipt evidence | atomicity violation and governed repair quarantine |
| response is lost after commit and client retries | authoritative receipt lookup returns the prior success; no second effect |
| commit outcome is uncertain and runtime reapplies before reconciliation | conformance failure with duplicate-effect risk |
| receipt exists but effect or consumption is missing, or effect exists without receipt | partial-set invariant breach; quarantine, no automatic synthesis or replay |
| fresh-approval expiry cleanup deletes immutable challenge or attempt evidence | conformance failure; retention remains separately governed |
| fresh-approval cancellation races with committed success | committed receipt wins; cancellation cannot reverse the effect |
| a cancelled or expired fresh-approval generation is reopened in place | conformance failure; any allowed retry uses a new generation |
| current `AgentRunApprovalCheckpoint v0.1` is offered as v0.2 human approval | binding failure; it lacks the required proof |
| an unapproved issue #12 effect family uses the generic handoff without its domain contract | unsupported effect; no finalization |
| outbox commit is treated as current permission to send bytes | conformance failure; issue #13 release eligibility remains separate |

Fixtures must enter through the production mode-correct admission, authorization, protected-effect, persistence, receipt-lookup, and recovery paths, including reservation and challenge only where fresh approval applies. Unit-only state-machine helpers are not sufficient for a conformance claim.

---

## 22. Traceability to issue #19

| Issue #19 acceptance criterion | Candidate closure |
|---|---|
| place challenge where required, human act, re-evaluation, decision, consumption, protected-effect validation, and commit | sections 5, 8, 9, 11, 12, and 13 |
| choose a bounded mechanism without an interactive open transaction | sections 5, 7, 8, and 9 |
| define authoritative transaction deadline and snapshot/cutoff inputs without moving ownership into authorization | section 10 |
| final current-state revalidation after act and before commit | section 11 |
| fresh-approval reservation ownership, expiry, cancellation, duplicates, concurrency, idempotency, retry, recovery, and cleanup plus direct-human retry posture | sections 6, 7, 14, 16, and 17 |
| atomic effect, authorization evidence, finalization evidence, consumption, and receipt visibility | section 13 |
| failure behavior without fabricated or rewritten authorization outcomes | sections 15 and 16 |
| exact protected-effect interface dependency | sections 12, 19, and 20 |
| production-reachable concurrency, crash, retry, and state-change hostile cases | section 21 |

---

## 23. Steward approval card

| Decision | Proposed answer | Approval required |
|---|---|---|
| Does fresh human approval use two durable stages with no open database transaction during human think time? | yes | yes |
| Does direct human action instead use one short finalization transaction with no challenge, separate approver, or approval consumption? | yes | yes |
| Is the design explicitly not distributed two-phase commit? | yes | yes |
| Is a fresh-approval reservation non-exclusive and incapable of granting authority or reserving domain truth? | yes | yes |
| Is successful finalization the sole protected-effect linearization point? | yes | yes |
| Does the outbox posture stop the internal transaction before external release? | yes; issue #13 remains separate | yes |
| Does one operation-boundary/requester/representation/action/human-finalization/idempotency tuple bind one logical operation digest? | yes | yes |
| Can only the same logical operation reuse that tuple, with different bytes treated as conflict? | yes | yes |
| May a terminal non-success fresh-approval generation be replaced sequentially while the logical operation still commits at most once? | yes | yes |
| Are fresh-approval reservation records immutable while mutable coordination rows remain derived? | yes | yes |
| Are `OPEN`, `FINALIZED`, `INVALIDATED`, `CANCELLED`, and `EXPIRED` the complete fresh-approval reservation states? | yes | yes |
| Is fresh-approval `FINALIZING` operational rather than a durable semantic state? | yes | yes |
| Must the same intended natural person act on the exact fresh-approval challenge and display bytes before exclusive expiry? | yes | yes |
| Does trusted server-side act time control timeliness? | yes | yes |
| Does a content-addressed transaction policy own deadline, atomic-boundary, guard, and status-lookup semantics? | yes | yes |
| Does PR #11 remain owner of authorization cutoffs, `decisionValidUntil`, relevant-state projection, and approver eligibility? | yes | yes |
| Must fresh-approval challenge and final authority-relevant digests match exactly? | yes | yes |
| Must the broader complete transaction guard also remain stable through commit? | yes | yes |
| Must negative facts and set membership use completeness watermarks or predicate guards? | yes | yes |
| Does every human-finalized state-affecting action entering this protocol require an exact rule-bound protected-effect handoff? | yes | yes |
| Does the transaction gate verify that handoff without duplicating domain mappings? | yes | yes |
| Are unsupported issue #12 effect families still blocked on their own contracts? | yes | yes |
| Do authorization/finalization evidence, decision consumption, exact effect/outbox, traces, receipt, and mode-applicable approval consumption and reservation terminal record commit atomically on success? | yes | yes |
| Does consumption linearize only with successful commit? | yes | yes |
| Do durable uniqueness constraints prevent duplicate operations, decision consumptions, mode-applicable approval consumptions, and result IDs? | yes | yes |
| Do matching concurrent retries reuse one receipt while conflicting consumers fail? | yes | yes |
| Are `EFFECT_COMMITTED`, `NO_EFFECT`, and `OUTCOME_UNKNOWN` transaction results rather than authorization outcomes? | yes | yes |
| Does protected-effect failure preserve authorization `ALLOW` without making it portable? | yes | yes |
| Must uncertain commit resolve through authoritative receipt/consumption lookup before retry? | yes | yes |
| Is any partial success set quarantined instead of automatically repaired or replayed? | yes | yes |
| Can fresh-approval cancellation or expiry terminate only an uncommitted generation and never reverse an effect? | yes | yes |
| Do issue #14 and security/custody work retain ownership of retention, deletion, encryption, and keys? | yes | yes |
| Is the first concrete domain binding exactly approved PR #17 head `9ef0803` and contract `ofarm.protectedeffect.reviewdecision.final.v0.1`? | yes | yes |
| Does that PR #17 binding use PR #11 `HUMAN_ONLY` and `DIRECT_HUMAN_ACTION_REQUIRED` without fresh-approval artifacts? | yes | yes |
| Does this candidate create no machine schema, accepted law, runtime, currentness, or production claim? | yes | yes |

Any requested change to authorization, protected-effect mappings, transport release, retention/key custody, database authority, authentication, or runtime implementation must remain in a separate trust-boundary PR.

---

## 24. Staged delivery and Phase A completion

The required sequence is:

1. **Approved dependencies:** preserve the exact semantically approved PR #11 head `03a21f6` and PR #17 head `9ef0803`; any semantic change reopens dependency review.
2. **Phase A transaction candidate:** review and approve or amend this one-file issue #19 candidate without creating active law or schemas.
3. **Accepted semantic promotion:** separately promote exact approved RFC bytes under repository governance; approval of this candidate does not perform that step.
4. **Non-default evidence and transaction profiles:** separately materialize the bounded, mode-correct `AuthorizationFinalizationEvidence v0.2` tags for finalization attempt, direct-human finalization, decision consumption, governed-effect receipt, and, only for fresh approval, reservation, challenge, human approval, and approval consumption, plus the exact transaction-policy binding. Schema review must preserve the ownership table in section 18.
5. **ReviewDecision machine contracts:** separately materialize the approved PR #17 result schema and protected-effect contract, then bind their exact refs/digests into the authorization policy bundle.
6. **Other effect-family contracts:** close each issue #12 child boundary before integrating that family with this transaction gate.
7. **Hostile conformance:** exercise section 21 through production-reachable transaction and recovery paths.
8. **Current/default promotion:** update currentness only through an explicit steward-approved promotion after contract and conformance review.
9. **OFARM2 extraction and implementation:** consume only promoted, digest-verified canonical assets; keep authorization, transaction coordination, protected effects, transport, retention/custody, and database authority separately reviewable.

Phase A is complete when:

- every issue #19 acceptance criterion has a proposed disposition;
- both human-finalization entry modes are preserved: two-stage reservation/challenge for fresh approval and one short transaction for direct human action, with the mode-correct finalization sequence, transaction inputs, complete revalidation, commit guards, atomic set, single-use uniqueness, retry, uncertain-commit recovery, and fresh-approval cancellation and cleanup rules reviewed;
- the exact PR #11 and PR #17 dependencies remain approved;
- the ReviewDecision handoff is concrete and every other effect family remains explicitly conditional on its own contract;
- no adjacent trust boundary was changed; and
- this PR still changes only this non-authoritative candidate file.
