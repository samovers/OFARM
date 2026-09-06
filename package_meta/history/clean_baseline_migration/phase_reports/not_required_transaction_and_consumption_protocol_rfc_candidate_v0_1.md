# OFARM `NOT_REQUIRED` Transaction and Consumption Protocol v0.1

Date: 2026-09-06<br>
Status: Phase A candidate for `samovers/OFARM#25`; non-authoritative, not accepted law, and not a current/default machine contract<br>
Parent inventory: `samovers/OFARM#10` and `samovers/OFARM#12`<br>
Depends on: the approved authorization candidate on PR #11 at `03a21f669ee04f96d444e14f00ae7212cab04803`, the approved governed human-approval transaction candidate on PR #20 at `98f8c4fafbae42c8f7fd931f43f53adcb4733713`, and the approved AssertionRecord protected-effect candidate on PR #23 at `622376e2998cf8b3954ca19e81d2cce6fd57e5fe`<br>
Scope: one canonical transaction profile for state-affecting actions whose immutable current rule selects `humanFinalizationRequirement = NOT_REQUIRED`, with `ASSERT_OPERATION_CLAIM` as the first concrete handoff

---

## 1. Decision requested

Stewards are asked to approve, reject, or amend these bounded decisions:

1. a state-affecting action may enter this protocol only when its immutable current rule selects `NOT_REQUIRED`, `TRANSACTION_BOUND_V0_2`, and `SINGLE_USE`, and binds an exact protected-effect contract and this exact transaction profile;
2. `RECEIVE_READ_DATA` is excluded even though its rule also selects `NOT_REQUIRED`; its protected-disclosure protocol remains separately owned;
3. one authoritative idempotency tuple identifies one logical operation across transaction handlers and profile revisions, while a separate caller-submission projection determines whether a request is an exact retry;
4. the complete `operationBindingDigest` is constructed once from the winning first admitted submission and is recovered, never recomputed from newly generated trusted fields on retry;
5. for `TRUSTED_ONLINE_SUBMISSION`, the runtime-observed `assertedAt` is supplied before full intent validation and hashing, and the timestamp selected by the first durable operation binding remains the assertion-act time for that logical operation;
6. the durable operation-binding point is the first atomic commit that makes the immutable binding visible as part of either a complete success set or a conclusively recorded no-effect attempt set; staging, locks, caches, and a write acknowledgement alone cannot prove that point;
7. one short guarded protected-effect transaction obtains a fresh current authorization decision, validates every applicable gate and the exact domain handoff, and atomically commits the complete success set;
8. no approval reservation, generation, challenge, intended approver, human-finalization act, approval, approval consumption, reservation terminal record, or direct-human finalization evidence exists in this mode;
9. the mode-correct evidence records that the rule selected no human finalization; it never claims that a human approval occurred and never replaces AssertionRecord-domain assertion-act provenance;
10. decision consumption becomes durable only with the successful protected effect, and one logical operation has at most one successful consumption, result, and governed-effect receipt;
11. transaction outcomes are exactly `EFFECT_COMMITTED`, `NO_EFFECT`, and `OUTCOME_UNKNOWN`, separate from authorization outcomes;
12. every conclusively durable `NO_EFFECT` attempt has exactly one immutable consequence, `RETRYABLE_SAME_OPERATION` or `TERMINAL_REQUIRES_NEW_OPERATION_KEY`; an uncertain attempt has neither;
13. operation admission uses verified evidence in this precedence: a complete matching success set, a partial success-set breach, any unresolved attempt, then the most recent conclusively ordered durable `NO_EFFECT` consequence;
14. a current mode change after a durable no-effect `NOT_REQUIRED` attempt is terminal under the old key, but it cannot bypass an unresolved earlier attempt;
15. an exact successful retry returns the original verified result and receipt without another effect or consumption, subject to current disclosure controls; and
16. the first concrete successful result is exactly one immutable `PENDING_REVIEW` operation-claim AssertionRecord under PR #23, not accepted execution, review, current state, or another implied domain effect.

Approval of this candidate authorizes no schema, accepted RFC, currentness, runtime, database, migration, or OFARM2 change.

---

## 2. Primary trust boundary and intended PR boundary

### 2.1 Primary trust boundary

The primary trust boundary is **canonical transaction admission, guarded ordering, atomic success, single-use consumption, retry identity, and authoritative outcome reconciliation for state-affecting `NOT_REQUIRED` actions**.

This candidate owns only:

- mode admission for state-affecting `NOT_REQUIRED` actions;
- the cross-profile idempotency lookup scope and key profile;
- the caller-owned comparison projection and bind-once operation binding;
- trusted intent-completion preservation across retries;
- immutable transaction-attempt ordering and operation-level admission precedence;
- the guarded successful transaction sequence;
- successful decision-consumption and receipt uniqueness;
- `NOT_REQUIRED` mode and attempt evidence truth claims;
- no-effect consequence semantics and uncertain-outcome reconciliation; and
- the concrete transaction handoff to the already proposed operation-claim contract.

It does not own or change:

- authorization rules, principal resolution, representation, grants, delegation, revocation, CP3 posture, evidence eligibility, or the authorization outcome lattice;
- human-approval or direct-human-final-action transaction semantics in PR #20;
- AssertionRecord fields, mappings, correction rules, event association, or postconditions in PR #23;
- governed-read disclosure, external transport release, retention duration, encryption, deletion, key custody, database roles, repair authority, or break-glass authority;
- accepted law, active-baseline text, machine schemas, current/default indexes, runtime code, or readiness claims; or
- OFARM2 implementation.

### 2.2 Intended Phase A PR boundary

The Phase A PR adds exactly this one non-authoritative file:

```text
package_meta/history/clean_baseline_migration/phase_reports/not_required_transaction_and_consumption_protocol_rfc_candidate_v0_1.md
```

Mechanical branch and draft-PR metadata may accompany it. No active authority, accepted RFC, companion policy, machine contract, generated currentness artifact, runtime, database object, or OFARM2 file changes.

If review requires a change in authorization, AssertionRecord semantics, Event Grammar, human-finalization modes, disclosure, retention/custody, database authority, or repair authority, work stops before that boundary and proceeds through a separate prerequisite, follow-up, or stacked PR.

---

## 3. Governing inputs, exact pins, and stop conditions

The authority order remains:

1. `00_active_baseline/`;
2. `02_accepted_rfcs/`;
3. `01_companion_artifacts/`; and
4. `03_machine_contracts/`.

This candidate preserves the active Constitution's assertion/history-first truth law, default-deny authority law, commit-class separation, and prohibition on treating an operation claim as accepted execution. It preserves the Platform Runtime requirement that every state-affecting path cross the applicable deterministic `EnforcementChain` gates and that only accepted/in-force material may affect current-state materialization.

The exact Phase A dependency pins are:

| Dependency | Exact approved head | Meaning consumed here |
|---|---|---|
| Authorization PR #11 | `03a21f669ee04f96d444e14f00ae7212cab04803` | action-rule selection, trusted principal and representation, `NOT_REQUIRED`, `TRANSACTION_BOUND_V0_2`, `SINGLE_USE`, current evaluation, `decisionValidUntil`, refusal evidence, and safe disclosure |
| Human-finalization transaction PR #20 | `98f8c4fafbae42c8f7fd931f43f53adcb4733713` | compatible operation, transaction, consumption, failure, and reconciliation patterns only; its two human-finalization modes remain unchanged and are not extended here |
| AssertionRecord protected-effect PR #23 | `622376e2998cf8b3954ca19e81d2cce6fd57e5fe` | exact operation-claim result carrier, assertion-act time/provenance, mappings, postconditions, result digest, and protected-effect trace |

The exact-head steward approval evidence is:

- PR #11: `https://github.com/samovers/OFARM/pull/11#issuecomment-5506778575`;
- PR #20: `https://github.com/samovers/OFARM/pull/20#issuecomment-5523100320`; and
- PR #23: exact-head re-review at `https://github.com/samovers/OFARM/pull/23#issuecomment-5525740023` and semantic approval at `https://github.com/samovers/OFARM/pull/23#issuecomment-5525764697`.

These are explicit steward comments, not formal GitHub `APPROVED` review objects. All three candidates remain draft and non-authoritative. Any semantic change to a pinned head reopens dependency review.

Materialization or implementation must stop when:

- the current action rule does not select `NOT_REQUIRED`, `TRANSACTION_BOUND_V0_2`, and `SINGLE_USE`;
- the action is not state-affecting or is `RECEIVE_READ_DATA`;
- an immutable, digest-valid transaction profile or protected-effect contract is absent;
- exact caller content cannot be projected without omitting an operation-changing caller field;
- trusted intent completion cannot be preserved or recovered exactly;
- an authoritative lookup cannot span the relevant transaction handlers;
- a complete current read/write guard or authoritative status lookup is unavailable;
- a protected result cannot be validated without changing its owning domain contract;
- retention would erase the evidence needed for conflict detection, retry, or reconciliation; or
- another trust boundary must change.

This document may identify such a prerequisite. It cannot silently fill it in.

---

## 4. Compatibility and ownership ledger against PR #20

PR #20 remains limited to `FRESH_HUMAN_APPROVAL_REQUIRED` and `DIRECT_HUMAN_ACTION_REQUIRED`. Reusing a compatible pattern does not widen that PR.

| PR #20 concept | `NOT_REQUIRED` disposition | Exact constraint here |
|---|---|---|
| stable idempotency tuple | adopted | the same boundary/requester/representation/action/key tuple is used across handlers; no mode, schema, result, or profile sub-namespace is allowed |
| operation binding and digest conflict detection | adopted with a required refinement | the full binding is fixed once; retry identity is decided by the stored caller-submission projection, so a newly generated trusted timestamp cannot create a false conflict |
| trusted transaction policy, time, deadline, snapshot, and status lookup | adopted | all are immutable rule/runtime bindings and trusted inputs; none is caller-selectable |
| complete isolation and commit guards | adopted | positive, negative, and set-valued facts plus all writes and uniqueness constraints are covered |
| successful-effect linearization | adopted | the protected effect becomes visible only at the complete atomic success commit |
| single-use decision consumption | adopted | exactly one successful decision consumption per logical operation; a failed attempt consumes nothing |
| `EFFECT_COMMITTED`, `NO_EFFECT`, and `OUTCOME_UNKNOWN` | adopted | they remain transaction outcomes, not authorization outcomes or public problem codes |
| authoritative reconciliation and partial-set quarantine | adopted with explicit no-effect-commit closure | verified complete success, a verified committed no-effect set, or conclusive protected-effect rollback resolves the corresponding uncertainty under section 10.3; partial success is quarantined; PR #20 is not amended |
| immutable history with derived coordination | adopted | locks, leases, queues, and indexes may optimize the short transaction but cannot override immutable binding, attempt, consumption, result, or receipt evidence |
| reservation generation and approval challenge | not applicable | absent; no synthetic or empty values |
| intended approver, human approval, and approval consumption | not applicable | absent; natural-person assertion provenance is a separate PR #23 domain fact |
| direct-human finalization evidence | not applicable | absent; a natural person may submit under `NOT_REQUIRED`, but that does not change the rule-selected mode |
| reservation cancellation, expiry, and terminal record | not applicable | absent; transaction deadline and other current cutoffs still apply to each attempt |
| new `NOT_REQUIRED` mode evidence and attempt profiles | new, owned by issue #25 | proposed as distinct tagged profiles in `AuthorizationFinalizationEvidence v0.2`; the package name does not imply human finalization |

No human-finalization record can satisfy, supplement, or replace this profile. Conversely, `NOT_REQUIRED` mode evidence cannot satisfy an action whose current rule requires fresh approval or direct human action.

---

## 5. Closed operation identity

### 5.1 Authoritative lookup tuple

The authoritative lookup scope is exactly:

```text
(operationBoundaryKind,
 operationBoundaryRef,
 authenticatedRequestingPrincipalRef,
 representedPartyRef-or-null,
 actionClass,
 operationIdempotencyKey)
```

`operationBoundaryKind` is exactly `TENANT` or `DEPLOYMENT`. When representation does not apply, the tuple's represented-Party component is exact JSON `null` in structured evidence and the corresponding database or index key has the one contract-defined null value. Omission, an empty string, an empty object, and a sentinel string are not equal to null.

Every non-key tuple identity is compared by the exact typed identity semantics of its owning contract. An implementation may not use display names, aliases, scope ancestry, case-insensitive collation, or storage-local string coercion as identity equality.

The lookup is shared across every transaction handler that can receive the action. `humanFinalizationRequirement`, effect-intent schema/version/digest, transaction-profile version, protected-effect contract, result digest, and current handler are deliberately not lookup dimensions. They cannot hide an earlier operation behind another namespace.

The tuple is derived only after malformed bytes and duplicate JSON names are rejected, the base request is valid enough to identify the action and caller key as an exact JSON string, and trusted authentication, operation boundary, and applicable representation refs are resolved. Shared internal discovery uses those exact key bytes before a current handler is allowed to create a new lifecycle. The original stored key profile controls an existing operation; the current profile grammar controls whether an absent tuple may be newly admitted. If any tuple component cannot be established truthfully, no authoritative tuple exists and no logical-operation lifecycle claim is made.

### 5.2 Canonical `operationIdempotencyKey` profile

This candidate defines `OFARM_OPERATION_IDEMPOTENCY_KEY_V0_1` for issue #25 operation admission and shared cross-handler lookup; it does not import an OFARM2 implementation convention or silently amend PR #20.

The key is a JSON string whose UTF-8 content is between 1 and 255 bytes and matches exactly:

```regex
^[A-Za-z0-9._:-]{1,255}$
```

Because every admitted code point is single-byte ASCII, byte equality and Unicode code-point equality produce the same result. Equality is byte-exact over the admitted UTF-8 bytes. Implementations must not trim, case-fold, apply Unicode normalization, use locale or database collation, replace punctuation, decode percent escapes, or interpret separators.

Consequences are exact:

- `Farm:1` and `farm:1` are different valid keys;
- `farm:1` and `farm:1 ` are not two comparable valid keys because the latter is invalid;
- any non-ASCII or canonically equivalent Unicode spelling is invalid, not normalized;
- `.`, `_`, `:`, and `-` are literal distinct characters; and
- a different valid key deliberately identifies a different logical operation under the other tuple components.

An invalid key is an ingress rejection before a new durable operation binding. It cannot be normalized into another key. Shared internal discovery may still find an exact pre-existing cross-profile tuple before rejection or reconciliation, but safe-response rules must not expose existence merely because an invalid current-profile request supplied those bytes.

### 5.3 Exact caller-owned submission projection

The authoritative retry comparison is the lookup tuple plus `callerSubmissionProjectionDigest`. The projection has this closed shape:

```json
{
  "schemaVersion": "ofarm.notRequiredCallerSubmissionProjection.v0.1",
  "callerEffectIntent": {}
}
```

`callerEffectIntent` is the complete resolved JSON object supplied by the caller as operation-semantic effect-intent content before trusted runtime completion. It is independent of whether transport supplied that immutable object inline or by retrievable ref. Duplicate names are rejected before construction. Unknown members are retained in the projection and will later fail the rule-selected schema; they are never silently dropped.

For the first operation-claim handoff, the two exact branches are:

- `TRUSTED_ONLINE_SUBMISSION`: the caller object must contain `/assertionActPosture` with that exact value and must omit `/assertedAt` and `/assertionActEvidenceBinding`. Every other caller-supplied effect-intent member is retained. The runtime later adds exactly `/assertedAt`.
- `VERIFIED_OFFLINE_SUBMISSION`: the caller object contains `/assertionActPosture`, `/assertedAt`, and `/assertionActEvidenceBinding` as required by PR #23. Every member is retained; trusted validation verifies the evidence but does not replace the submitted timestamp.

`callerSubmissionProjectionDigest` is `sha256:` plus the SHA-256 digest of the RFC 8785 JCS UTF-8 bytes of the complete projection. No member is excluded because the projection contains no self-digest.

The following request-envelope facts are per-attempt or non-authoritative and are not operation content: request identifier, caller request time, AI-assistance disclosure, transport locator for otherwise identical immutable intent bytes, schema hint, retrieval hints, tracing headers, and response preferences. They remain in their owning attempt or ingress evidence. The action, boundary, authenticated principal, represented Party, and idempotency key are not omitted from comparison: they are already exact members of the authoritative lookup tuple. Any other caller field capable of changing the protected operation must be inside `callerEffectIntent`; a schema that places such a field elsewhere is ineligible for this profile.

Two submissions are exact caller-content retries only when both their authoritative tuples and projection digests are equal and the stored projection bytes or a recomputation from retained exact bytes verifies that digest. Digest equality without valid binding evidence is not permission to execute.

### 5.4 Runtime-completed effect intent

The caller projection is not a second authoritative effect intent. It exists only for retry comparison.

For `TRUSTED_ONLINE_SUBMISSION`, the trusted ingress runtime observes the authenticated submission and supplies a canonical PR #23 `assertedAt` value before full effect-intent validation and digest calculation. It creates the full intent by adding that one member to the exact caller object. It may not replace, normalize, summarize, or default another operation field.

For `VERIFIED_OFFLINE_SUBMISSION`, the runtime verifies the exact act-evidence binding and timestamp under PR #23 and uses the unchanged caller object as the full intent.

The complete runtime-finished intent is then validated against the exact rule-selected schema. `effectIntentDigest` is computed over the complete schema-valid intent using `JCS_RFC8785_SHA256`. The caller projection never weakens that full-intent digest and never supplies an authorization fact.

### 5.5 Complete logical-operation binding

The immutable operation binding has this closed semantic shape:

```json
{
  "schemaVersion": "ofarm.notRequiredOperationBinding.v0.1",
  "logicalOperationId": "...",
  "operationBoundary": {
    "kind": "TENANT",
    "ref": "...",
    "revisionSelector": {}
  },
  "requestingPrincipalBinding": {
    "resolvedPrincipalKind": "NATURAL_PERSON",
    "authenticatedPrincipalRef": "...",
    "principalRevisionSelector": {}
  },
  "representedPartyBinding": null,
  "actionClass": "...",
  "operationIdempotencyKeyProfile": "OFARM_OPERATION_IDEMPOTENCY_KEY_V0_1",
  "humanFinalizationRequirement": "NOT_REQUIRED",
  "effectIntentSchemaBinding": {
    "schemaRef": "...",
    "schemaVersion": "...",
    "schemaDigest": "sha256:...",
    "canonicalization": "JCS_RFC8785_SHA256"
  },
  "protectedEffectContractBinding": {
    "contractId": "...",
    "contractVersion": "...",
    "contractRef": "...",
    "contractDigest": "sha256:..."
  },
  "governedTransactionProfileBinding": {
    "profileId": "ofarm.transaction.not-required-state-effect.v0.1",
    "profileVersion": "0.1",
    "profileRef": "...",
    "profileDigest": "sha256:..."
  },
  "callerSubmissionProjectionProfile": "ofarm.notRequiredCallerSubmissionProjection.v0.1",
  "callerSubmissionProjectionDigest": "sha256:...",
  "effectIntentRef": "...",
  "effectIntentDigest": "sha256:...",
  "effectIntentCanonicalization": "JCS_RFC8785_SHA256",
  "operationIdempotencyKey": "...",
  "operationBindingDigest": "sha256:..."
}
```

Every object rejects unknown members. Each `revisionSelector` contains exactly one immutable `revisionRef` or `contentDigest`, never both or neither. `resolvedPrincipalKind` is exactly `NATURAL_PERSON` or `SOFTWARE_AGENT`; an `UNRESOLVED` principal cannot be admitted. `logicalOperationId` is one opaque, unique, non-reassignable identifier created by the trusted transaction boundary; it is not caller-selected and does not replace tuple lookup.

When representation applies, `representedPartyBinding` is exactly:

```json
{
  "representedPartyRef": "...",
  "representedPartyRevisionSelector": {},
  "representationBasisRef": "...",
  "representationBasisRevisionSelector": {}
}
```

When it does not apply, the member is required and is exact JSON `null`. The complete requesting-principal and representation bindings record the immutable first-admission resolution. Current principal, session, representation, and revocation state are still re-resolved for every execution attempt; current facts cannot rewrite the historical operation binding.

`effectIntentRef` resolves to the complete runtime-finished immutable intent bytes. When the caller supplied an embedded object, the trusted boundary assigns its internal content-addressed ref before binding; changing from embedded transport to another immutable locator does not change the bytes. A mutable URL, branch, latest-version lookup, or digest without resolvable bytes while retry remains possible is insufficient.

`operationBindingDigest` is constructed by:

1. rejecting duplicate JSON member names in every source object;
2. validating a provisional complete operation binding whose top-level `/operationBindingDigest` is exactly `ofarm:pending-operation-binding-digest`;
3. removing exactly that one top-level member and no nested member;
4. applying RFC 8785 JCS, UTF-8, and SHA-256;
5. representing the result as `sha256:` plus 64 lowercase hexadecimal characters;
6. inserting that value at `/operationBindingDigest`; and
7. validating the final complete object.

Missing, duplicated, mutable, unresolved, digest-invalid, or extra binding content fails admission. Once durable, the complete bytes and digest never change. A retry recovers them; it never rebuilds them from current policy, a new timestamp, caller memory, or a cached response.

### 5.6 Exact result-binding rule

Result identity and digest are not lookup dimensions. They therefore cannot create another operation namespace.

Before a protected result has passed its owning contract, the operation has no admitted result binding. The first durable attempt that records an overall passing protected-effect handoff fixes one immutable `admittedProtectedResultBinding` containing the result ID, result-schema ref/version/digest, complete result digest, protected-effect contract ref/digest, and passing validation-trace ref/digest. It is a required closed subobject of that `NOT_REQUIRED_TRANSACTION_ATTEMPT_V0_1` record and is addressed thereafter by the attempt ref/digest plus its fixed `/admittedProtectedResultBinding` pointer. The attempt's integrity digest covers the complete subobject; it is not mutable coordination state or an independently selectable namespace. A no-effect attempt may fix this binding without making the result exist, but only when the proposed bytes passed the complete domain contract before the later failure.

The authoritative admitted binding is the one in the lowest `attemptSequence` durable attempt that contains that subobject. Every later occurrence must equal it exactly. Every later attempt must reproduce and verify that exact binding before success. A committed result must equal it byte-for-byte. A different result under the same tuple cannot borrow the operation or its receipt. A deterministically rejected result is never labeled admitted; its exact attempted binding may be retained only as non-consumable failure evidence.

---

## 6. First durable admission and trusted assertion-act identity

### 6.1 What creates the durable operation

The logical operation first exists authoritatively when one atomic commit makes the complete operation binding visible in either:

- the complete successful effect set; or
- a conclusively `NO_EFFECT` attempt set that contains the operation binding and its truthful attempt evidence.

An in-memory object, staged insert, row lock, lease, queue item, uncommitted uniqueness claim, cache entry, log line, or ambiguous commit response is not proof of a durable operation binding. Loss of the response does not undo an actual commit: section 10.3 may recover either a complete committed success set or a complete committed no-effect set and its original binding. A lower-level ingress or security record may truthfully record what it observed, but it cannot claim that the logical operation was admitted.

On a first attempt that conclusively fails after full ingress validation, a separate failure-evidence commit may create the operation binding only when it atomically verifies authoritative rollback of the protected-effect transaction, verifies that the tuple is still unbound, and commits the exact staged binding together with one no-effect attempt and consequence. If that evidence commit conclusively fails or loses the tuple race, it creates no operation consequence. It may never run while the protected-effect commit remains uncertain. Its own transaction identity and commit status are distinct from the rolled-back transaction: a lost failure-evidence response requires reconciliation of that evidence commit before claiming that no binding survived or permitting another attempt.

### 6.2 Meaning of the online assertion timestamp

For `TRUSTED_ONLINE_SUBMISSION`, `assertedAt` is the trusted runtime observation time captured before full intent validation and hashing for the submission whose binding wins the first durable admission. The later operation-binding commit selects and preserves that already observed value; it does not redefine its source.

Therefore:

- `assertedAt` is not operation-binding commit time;
- `assertedAt` is not transaction start, authorization, receipt-response, retry, or `effectCommittedAt` time;
- concurrent contenders may transiently observe different timestamps, but only the winner's runtime-finished intent becomes authoritative;
- a matching loser discards its own uncommitted timestamp, recovers the winner's full intent and `assertedAt`, and follows the winner's lifecycle; and
- if no durable operation binding ever commits, this protocol claims no surviving operation-level assertion-act timestamp.

This preserves PR #23's assertion, receipt/synchronization, authorization, and commit-time separation.

### 6.3 Concurrent first-admission winner

The atomic boundary enforces one binding per authoritative tuple. Each contender stages its complete binding only after its own caller projection, trusted completion, full intent validation, and authorization-view extraction succeed.

Exactly one binding may commit. A loser must:

1. stop before making any protected effect visible;
2. load the authoritative winner through the shared tuple index;
3. evaluate the operation-level evidence precedence in section 10;
4. compare its tuple and caller projection with the winner;
5. discard every locally generated trusted field and provisional result; and
6. return, block, conflict, or begin a later allowed attempt only as the authoritative winner state permits.

The loser must not compare a newly computed full operation digest to the winner and report a timestamp-induced conflict. Application-level check-then-insert without an atomic unique constraint or equivalent commit guard is non-conforming.

### 6.4 Surviving-binding rule after rollback

After conclusive rollback of the named protected-effect transaction:

- if a prior operation binding already existed, it and its original caller projection, full intent, trusted fields, and any admitted result binding survive unchanged;
- if a separate authorized failure-evidence commit durably recorded the first binding with a no-effect attempt, those exact facts survive; the rolled-back transaction itself committed nothing;
- if that separate evidence commit remains uncertain, keep the tuple blocked until its own status is reconciled;
- if authoritative status proves that neither a prior commit nor a separate evidence commit admitted the binding, no operation binding or operation-level assertion-act fact survives; and
- caller memory, a request retry, a local cache, or a lower-level receipt log cannot reconstruct the missing trusted timestamp or full operation digest.

Every permitted later attempt under an existing operation uses the stored full intent and obtains a fresh current authorization decision. It never reuses the earlier decision.

A transaction that committed a complete no-effect set is not a rollback case. Its binding and recorded consequence survive under sections 10.3 and 11.4, including when its commit response was lost.

---

## 7. Mode admission and evidence truth claim

### 7.1 Admission predicate

A new execution attempt enters this profile only when all of these are true:

1. shared tuple lookup and operation-level precedence permit an attempt;
2. the immutable current action rule selects `humanFinalizationRequirement = NOT_REQUIRED`;
3. the same rule selects `TRANSACTION_BOUND_V0_2` and `SINGLE_USE`;
4. the action is state-affecting and is not `RECEIVE_READ_DATA`;
5. the exact effect-intent schema, protected-effect contract, transaction profile, and rule bindings are immutable and digest-valid;
6. any existing operation's stored mode, schema, protected-effect contract, and transaction profile remain exactly compatible with current execution without rebinding the operation; and
7. every prerequisite needed to produce a guarded atomic result is available.

A caller cannot select, downgrade, or override the mode. A human being the authenticated requester does not convert `NOT_REQUIRED` to direct human action. A software agent being the requester does not remove PR #11's complete CP3 and authority checks.

### 7.2 Closed absence posture

These records and fields are absent in this profile:

- approval reservation and reservation generation;
- approval challenge and human-visible approval display;
- intended approver and approver authority path;
- human-finalization act and human approval;
- approval expiry and approval consumption;
- reservation cancellation, expiry, or success terminal record; and
- direct-human finalization evidence.

They are not represented by `null`, empty objects, empty arrays, `NOT_APPLICABLE` placeholder records, or fabricated proof. A validation trace may truthfully mark a contract-declared conditional check `NOT_APPLICABLE`; that does not create the inapplicable record.

### 7.3 `NOT_REQUIRED` mode evidence

The proposed tagged profile `NOT_REQUIRED_MODE_EVIDENCE_V0_1` belongs in the separately materialized `AuthorizationFinalizationEvidence v0.2` package. The package name is a packaging decision from PR #11; this profile's truth claim is only:

> For this exact logical operation and transaction attempt, the immutable current action rule selected `NOT_REQUIRED`; no human-finalization condition or evidence was required or supplied by the transaction protocol.

The evidence binds:

- logical operation and operation-binding ref/digest;
- transaction attempt ID and immutable attempt sequence;
- action class and exact current action-rule ref/revision/digest;
- `NOT_REQUIRED`, `TRANSACTION_BOUND_V0_2`, and `SINGLE_USE` selections;
- effect-intent schema/ref/digest and caller-projection digest;
- protected-effect contract and governed transaction-profile refs/digests;
- trusted principal and applicable representation refs used for the attempt;
- transaction snapshot, deadline, and guard-policy bindings; and
- an explicit closed absence bitmap or equivalent schema branch proving the mode-inapplicable records are absent.

It is constructed inside the short transaction after current bindings and trusted transaction inputs are fixed and before the final authorization evaluation. It is not supplied as an approval and cannot make an authorization path sufficient. On success it commits in the complete success set. On a conclusively committed no-effect attempt, a non-consumable instance may commit with that attempt to prove which mode was evaluated. If neither commit succeeds, no durable mode-evidence claim is made.

PR #23 assertion-act evidence remains separate. In particular, `VERIFIED_OFFLINE_SUBMISSION` may require immutable natural-person or represented-Party assertion-act evidence even though transaction finalization requires no human approval.

---

## 8. Trusted transaction policy and complete guard

### 8.1 Profile binding

The future content-addressed profile ID is `ofarm.transaction.not-required-state-effect.v0.1`, version `0.1`. Before executable use, the immutable profile ref/digest must specify:

- trusted timestamp source and canonical time representation;
- exact transaction-deadline calculation or trusted deadline source;
- supported atomic persistence boundary;
- exact isolation or compare-and-commit mode;
- positive-record revision guards;
- negative/predicate and set-completeness guards;
- tuple, attempt, consumption, receipt, and result uniqueness rules;
- authoritative commit-status lookup and uncertainty fence;
- immutable attempt ordering; and
- permitted reconciliation evidence.

This Phase A candidate defines the semantics but creates no profile bytes. A caller, UI, software agent, domain result, or mutable deployment setting cannot choose or extend these values.

### 8.2 Trusted attempt inputs

At attempt start the runtime supplies:

- unique `transactionAttemptId`;
- next immutable `attemptSequence` for the logical operation, allocated under an atomic operation guard;
- trusted `transactionStartedAt`;
- exclusive `transactionDeadline`;
- `transactionSnapshotRef` and digest or equivalent immutable snapshot proof;
- atomic persistence-boundary identity;
- isolation/guard-mode binding and complete guard accumulator;
- exact currentness watermarks or predicate versions for negative and set-valued facts; and
- authoritative transaction-status lookup key.

An attempt sequence is a positive integer. Only a durably recorded attempt owns a sequence. Among durable attempts, larger sequence means later authoritative attempt; timestamps and lexical IDs never break ties. A failed provisional allocation may leave no authoritative sequence and cannot be reused to falsify order.

At most one effect-capable attempt per logical operation may be admitted at a time. Short-lived locks or leases may implement this rule, but they are derived coordination, not approval reservations, operation truth, or authority.

### 8.3 Complete current re-resolution

Inside the transaction, the runtime re-resolves and guards every current fact that can affect authority or the protected result, including:

- principal identity, session validity, represented Party, and representation basis;
- software-agent identity, sponsorship, actorship, authority envelope, authority snapshot, revocation, and other applicable CP3 evidence;
- RoleAssignments, AuthorityGrants, DelegationGrants, source grants, SharingGrants where applicable, and all relevant revocations;
- policy, rule, extractor, effect-intent schema, protected-effect contract, and transaction-profile bindings;
- authority target, typed inputs, effect subject, scope, twin, tenant, purpose, and sovereignty boundary;
- resource, evidence, identity, correction-target, and protected-effect state revisions;
- absence of an existing prospective result and every other uniqueness predicate;
- pack/profile applicability and every other applicable `EnforcementChain` input; and
- any admitted protected-result binding from an earlier attempt.

The final authorization evaluation uses PR #11's complete current algorithm. It computes `decisionValidUntil` as the exact minimum of every applicable exclusive cutoff, including `transactionDeadline`. Missing required cutoff evidence or a minimum not later than `authorizationEvaluatedAt` produces no consumable decision.

### 8.4 Guard sufficiency

A read snapshot is insufficient by itself. The transaction policy must use one documented, content-addressed proof mode:

- serializable conflict detection over the complete relevant read/write set;
- explicit locks or immutable version guards over that complete set; or
- optimistic compare-and-commit over exact revisions, predicate versions, and set-completeness watermarks.

The guard covers facts such as “no active revocation exists,” “no result with this proposed ID exists,” complete applicable-grant sets, evidence eligibility sets, and policy/currentness registries. Locking only positive records is insufficient. Every required success-set write and uniqueness condition participates in the same atomic boundary.

If any current input, required absence, success member, or uniqueness rule cannot be protected, the action is unsupported. A saga that exposes the effect before its decision, mode evidence, consumption, traces, and receipt is non-conforming.

---

## 9. Ordered admission and successful transaction

### 9.1 Pre-transaction discovery and ingress order

The mode-correct admission order is:

1. reject malformed bytes and duplicate JSON member names;
2. validate the base request shape far enough to resolve the action and caller key without claiming an authorization outcome;
3. authenticate the principal and resolve the exact operation boundary and applicable represented-Party ref; for an online submission, capture a trusted per-request `submissionObservedAtCandidate` at this authenticated observation point, without yet claiming it as an admitted operation fact;
4. require `operationIdempotencyKey` to be an exact safely parsed JSON string and form the authoritative discovery tuple without normalization;
5. perform shared authoritative tuple and transaction-status lookup before current-profile key validation or selection of a new handler lifecycle;
6. if an operation or unresolved first attempt exists, apply its stored key/profile binding and section 10 before generating any trusted intent field;
7. if none exists, validate the key under section 5.2, resolve the current action rule, and require the section 7.1 mode predicate;
8. resolve the complete caller-owned intent object, construct the exact section 5.3 projection, and compute its digest;
9. perform PR #23 mode-correct trusted intent completion: for a new online operation add the step 3 `submissionObservedAtCandidate` as `/assertedAt`, or verify the exact offline act evidence and timestamp; an existing operation instead recovers its stored full intent and never inserts the new per-request time;
10. validate the complete runtime-finished effect intent against the rule-selected schema and compute `effectIntentDigest`;
11. execute PR #11's declarative authorization-view extraction and reject any missing, duplicate, type-invalid, unknown-kind, or conflicting fact; and
12. construct the provisional operation binding and enter the short guarded transaction.

Steps 1 through 11 are ingress and trusted preparation. They create no authorization result, protected effect, consumption, success receipt, or durable operation unless a later atomic commit satisfies section 6. A schema hint remains non-authoritative and must match the current rule when present.

### 9.2 Exact successful order

One successful short transaction performs this order:

1. establish trusted attempt time, deadline, snapshot, status lookup, attempt sequence, and complete guard under section 8;
2. perform the shared tuple lookup again under the atomic uniqueness boundary; on a concurrent winner, stop and resolve it under sections 6.3 and 10;
3. insert or verify the exact immutable operation binding, original caller projection, full runtime-finished intent, and any prior admitted result binding;
4. re-resolve and guard every current fact in section 8.3, including the current rule-selected mode and all negative/set-valued facts;
5. construct the prospective `NOT_REQUIRED_MODE_EVIDENCE_V0_1` object, without making it authority or durable success evidence;
6. run the complete PR #11 evaluator exactly once for this attempt and construct the final request/result/full-internal-trace bundle and `decisionBundleDigest`;
7. require authorization `ALLOW` and a consumable decision whose exclusive `decisionValidUntil` remains later than the prospective commit;
8. build the proposed domain result and evaluate every applicable non-authorization `EnforcementChain` gate, leaving inapplicable gates truthfully inapplicable rather than passed;
9. validate the complete rule-bound protected-effect handoff, including result schema, exact result bytes/digest, state inputs, absence guards, mappings, postconditions, and overall `PASS`;
10. insert or verify the immutable admitted protected-result binding from section 5.6;
11. finish the required gate traces, preallocate the receipt ID, and construct the decision-consumption record, transaction-attempt record, and complete-set receipt in the acyclic digest order in section 12.2;
12. recheck `transactionDeadline`, `decisionValidUntil`, current rule mode, every complete guard, tuple/result/consumption/receipt uniqueness, and authoritative absence of a prior success or unresolved attempt; and
13. atomically commit the complete success set, then expose a response allowed by current disclosure policy.

No successful component becomes durably visible before step 13. The mode evidence and authorization decision are transaction-bound and non-portable. A later attempt cannot consume them.

### 9.3 Required atomic success set

The success membership is exactly:

- the immutable operation binding and caller-projection binding;
- the successful `NOT_REQUIRED_TRANSACTION_ATTEMPT_V0_1` record;
- final authorization request, result, full internal trace, and `decisionBundleDigest`;
- the exact `NOT_REQUIRED_MODE_EVIDENCE_V0_1` record;
- exactly one single-use decision-consumption record;
- exactly the protected domain result set admitted by the bound domain contract;
- the complete passing protected-effect trace and every other applicable gate trace;
- the successful attempt's exact `admittedProtectedResultBinding` subobject, or an exact reference to the already fixed subobject in the lowest prior durable attempt sequence; and
- exactly one `NOT_REQUIRED_GOVERNED_EFFECT_RECEIPT_V0_1` identifying every member and the atomic commit proof.

On the first successful admission, the operation binding is inserted in this atomic commit. If an earlier conclusive no-effect attempt already committed the immutable binding, the success set contains and guards that exact pre-existing member by ref/digest rather than rewriting or inserting it again; every newly successful component still commits atomically.

The set contains no approval, reservation, human-finalization, implicit domain companion, external dispatch, ReviewDecision, accepted consequence, or current-state materialization. Pre-existing evidence or semantic-event records consumed by reference are guarded inputs, not newly created success effects.

### 9.4 Receipt minimum and complete-set verification

The governed-effect receipt binds at least:

- tuple, logical operation, operation-binding ref/digest, caller-projection digest, and key profile;
- transaction attempt ID/sequence, trusted start and commit times, exclusive deadline, snapshot, atomic boundary, transaction policy, and complete guard proof/digest;
- action rule and `NOT_REQUIRED` mode-evidence refs/digests;
- authorization request/result/trace refs and `decisionBundleDigest`;
- decision-consumption ref/digest and `SINGLE_USE` posture;
- effect-intent schema/ref/digest and full intent digest;
- protected-effect contract, result-schema, admitted-result, committed-result, and validation-trace refs/digests;
- every other applicable gate trace/disposition;
- exact role-labelled membership of the complete atomic success set; and
- final outcome `EFFECT_COMMITTED`.

The receipt's immutable identifier is allocated before consumption is hashed. Consumption binds that receipt identifier only, not its digest; the receipt binds the finalized consumption ref/digest. Verification enforces both the identifier back-reference and the digest-bearing forward reference.

The role-labelled membership includes the receipt itself exactly once, by its preallocated identifier and role only. That self-entry has no digest member, including no null or provisional digest. Every other member is bound by its finalized owning digest; the admitted-result subobject is bound through its containing attempt ref/digest and fixed pointer. The receipt's own digest exists only in its top-level self-digest member and is verified using section 12.1. No nested membership entry repeats that digest. Later reconciliation evidence points back to the unchanged receipt; it is never inserted into the original receipt or original success membership.

A receipt row or label alone is not proof of success. A complete matching success set is verified only when:

1. the receipt and every required member resolve to immutable bytes with matching digests;
2. membership has exactly the required role cardinalities, its identifier-only receipt self-entry names this receipt, and there is no conflicting member;
3. operation, intent, rule, decision, consumption, result, trace, and attempt bindings all agree;
4. the protected-effect disposition is `PASS` and committed result bytes equal validated bytes;
5. authoritative atomic-store status proves the named transaction committed; and
6. uniqueness lookup finds no second success, consumption, or differing result bytes.

A missing or mismatched required member is a partial-set invariant breach, not a degraded success. No cache, replica, caller receipt, or success string may weaken this verification.

---

## 10. Deterministic operation-level admission view

### 10.1 Evidence ordering

Every lookup constructs one authoritative operation view from immutable evidence and the transaction policy's authoritative status mechanism. Derived caches may accelerate the lookup but never decide it.

The exact precedence is:

1. **Verified complete success:** if section 9.4 proves one complete matching success set and authoritative inspection finds no partial or competing success material, the operation is `COMPLETED`. A matching retry may receive the original permitted response. Conflicting caller content cannot borrow that receipt, but it also cannot reopen the operation.
2. **Partial success or competing-success breach:** if any success-labelled component exists without the complete matching set, or more than one success/consumption/result identity conflicts, the operation is `QUARANTINED_PARTIAL_SUCCESS`. No automatic synthesis, deletion, compensation, or replay is allowed.
3. **Unresolved attempt or commit fact:** if any attempt that could have applied the effect remains `OUTCOME_UNKNOWN`, or authoritative status is incomplete, the operation is `BLOCKED_PENDING_RECONCILIATION` and names every exact unresolved attempt or fact. This step precedes caller-content, mode-change, and no-effect retry decisions.
4. **Conclusive no-effect history:** only when the first three steps do not apply, select the durable `NO_EFFECT` attempt with the greatest `attemptSequence`. Its one immutable consequence controls admission.

An earlier no-effect attempt never cancels a later unresolved attempt. A current mode change never invites a new-key submission while an earlier effect may still commit.

### 10.2 Request-specific decision after evidence ordering

After the operation view is safe to use:

- compare the exact tuple and caller-submission projection; a mismatch is a conflicting submission and creates no new attempt;
- for a completed matching operation, verify the committed result binding and apply current disclosure policy before returning the original result/receipt;
- for a quarantined or unresolved operation, do not execute regardless of caller match or current mode;
- for a conclusive no-effect operation, a current rule mode other than the stored `NOT_REQUIRED` mode yields `TERMINAL_REQUIRES_NEW_OPERATION_KEY` under the old key;
- an incompatible current intent-schema, protected-effect-contract, or transaction-profile binding that would require rebinding the immutable operation is terminal under the old key;
- a latest `TERMINAL_REQUIRES_NEW_OPERATION_KEY` consequence prohibits another attempt; and
- a latest `RETRYABLE_SAME_OPERATION` consequence permits a new attempt only with the stored original full intent, original trusted fields, a fresh current decision, and every current check repeated.

`RETRYABLE_SAME_OPERATION` means protocol eligibility, not an instruction for an automatic loop. Rate limits, backoff, and caller-visible retry timing may be governed operationally, but they cannot reuse a decision or change the immutable operation.

### 10.3 Reconciliation

Reconciliation distinguishes a database transaction's commit status from the attempt's protected-effect outcome. A database transaction can commit a valid `NO_EFFECT` evidence set. That is neither a protected-effect success nor a database rollback.

Every status proof names the atomic-store boundary, exact transaction-status lookup key, logical operation or provisional tuple, and `transactionAttemptId`. The evidence records the transaction's role:

- **protected-effect transaction:** the transaction that could apply the effect, but may instead commit only truthful no-effect evidence;
- **first-admission commit:** the transaction that first made the operation binding durable, whether in a success set or a no-effect set; and
- **separate failure-evidence commit:** a later transaction that records proven failure after the protected-effect transaction rolled back, and may also be the first-admission commit.

Roles name the same transaction only when they are the same actual atomic commit. Distinct transactions have distinct status lookup keys, even when they concern the same attempt. A failure-evidence commit binds the rollback proof for the exact protected-effect transaction it describes. Proof that the latter rolled back says nothing about whether the former committed. A pre-existing operation binding is a guarded historical input, not a new write or partial success by the attempt being reconciled.

Using those identities, reconciliation queries the authoritative atomic store or commit-status mechanism for:

- operation binding and any admission commit;
- transaction-attempt status and sequence;
- mode evidence and authorization bundle;
- decision consumption;
- admitted and committed protected-result bindings;
- protected-effect and gate traces;
- governed-effect receipt; and
- complete success or no-effect set membership and the status of every relevant evidence commit.

The resolutions are:

| Authoritatively verified condition | Exact resolution |
|---|---|
| The complete matching protected-effect success set committed under section 9.4 | `EFFECT_COMMITTED`; complete-success precedence controls and the original receipt is resolved, never rebuilt. |
| A complete matching no-effect set committed under section 11.4, with no protected effect, decision consumption, or success receipt for that attempt | `NO_EFFECT`; preserve that set's immutable binding, original trusted intent facts, and recorded consequence. The database commit succeeded; do not label it rolled back or re-evaluate to recreate its refusal or failure evidence. |
| The protected-effect transaction conclusively rolled back | Its protected-effect outcome is `NO_EFFECT`. Apply section 6.4 and verify any separate failure-evidence commit independently. A committed no-effect set uses the preceding row; an uncertain evidence commit keeps the operation blocked; conclusive failure to persist evidence creates no new consequence and leaves prior authoritative history controlling. Without any surviving binding, no operation is admitted. |
| Status or required evidence remains incomplete or contradictory | Keep the operation blocked and name the exact unresolved transaction or fact. A proven partial-success or conflicting-set invariant breach is quarantined for separately governed repair. No missing member, commit, rollback, or consequence is invented. |

Verification is attempt-specific and uses authoritative status plus complete, digest-valid membership. A cache, replica, timed-out lookup, incomplete query, or caller-visible absence response proves neither rollback nor a complete no-effect set. A refusal bundle alone does not prove that an effect transaction cannot still commit.

Resolution appends or exposes immutable reconciliation evidence without rewriting the original observation, attempt, receipt, binding, or consequence. A resolution of success refers to the original receipt ref/digest; the receipt does not refer forward to that later resolution. No new effect-capable attempt may begin while any relevant protected-effect or evidence-commit fact remains unresolved. Once all such facts are settled, section 10.1 selects the surviving authoritative history; reconciliation itself grants no retry or disclosure authority.

---

## 11. Outcomes, no-effect consequences, and failure matrix

### 11.1 Three transaction outcomes

The closed transaction outcomes are:

| Outcome | Exact meaning |
|---|---|
| `EFFECT_COMMITTED` | section 9.4 verifies the complete matching success set and authoritative commit status |
| `NO_EFFECT` | authoritative evidence conclusively proves that no protected result, decision consumption, or success receipt committed for this attempt |
| `OUTCOME_UNKNOWN` | available authoritative evidence cannot yet establish whether the attempt committed a protected effect or conclusively had no effect |

These outcomes describe the protected effect, not whether every related database transaction committed. `NO_EFFECT` may be established by a complete committed no-effect set or by authoritative protected-effect rollback proof. If the protected-effect rollback is proven but a separate failure-evidence commit is uncertain, the protected-effect fact remains `NO_EFFECT` while the operation is `BLOCKED_PENDING_RECONCILIATION`; no new durable consequence is claimed until that evidence status is settled.

They are not authorization outcomes, public `RuntimeProblem` codes, or domain result states. `DENY`, `REQUIRE_REVIEW`, and any other PR #11 result remain authorization outcomes inside their own evidence.

### 11.2 Two immutable no-effect consequences

Every durably recorded, conclusively proven `NO_EFFECT` attempt under an existing logical operation carries exactly one:

- `RETRYABLE_SAME_OPERATION`: the immutable operation may receive a later attempt using its stored caller projection, full intent, trusted fields, and any admitted result binding. The new attempt obtains a fresh current decision and repeats every guard and gate.
- `TERMINAL_REQUIRES_NEW_OPERATION_KEY`: the operation can never receive another effect-capable attempt. A genuinely new operation requires a new valid caller key and follows the then-current mode and contracts.

These values describe one no-effect attempt. `BLOCKED_PENDING_RECONCILIATION` is a derived operation state and is never stored as that attempt's no-effect consequence. `OUTCOME_UNKNOWN` carries neither consequence.

`NO_OPERATION_CONSEQUENCE` and `NO_NEW_CONSEQUENCE` below are explanatory postures, not third no-effect values. They mean that no new immutable operation-attempt consequence was truthfully committed.

### 11.3 Closed lifecycle matrix

| Condition | Evidence and transaction outcome | Exact lifecycle consequence |
|---|---|---|
| malformed bytes or duplicate JSON names | PR #11 ingress rejection if it can be durably recorded; no authorization result, effect, consumption, or operation binding | `NO_OPERATION_CONSEQUENCE` |
| base request, principal, boundary, representation ref, action, or key cannot establish the complete tuple | truthful ingress/security rejection only | `NO_OPERATION_CONSEQUENCE` |
| invalid key, caller projection, full intent, rule-selected schema, or authorization-view extraction before the first durable binding | PR #11 ingress rejection; no effect or consumption | `NO_OPERATION_CONSEQUENCE` |
| new request selects a non-`NOT_REQUIRED` mode, governed read, unsupported effect, or missing/digest-invalid binding before a durable operation exists | admission rejection; no authorization result unless PR #11 independently reached one; no effect or consumption | `NO_OPERATION_CONSEQUENCE` |
| schema-valid final authorization is `DENY` and the operation/refusal/attempt set commits conclusively | preserve the complete PR #11 refusal bundle; `NO_EFFECT`; no decision consumption or success receipt | `RETRYABLE_SAME_OPERATION`; a later attempt uses fresh current evaluation and the earlier refusal is never reused |
| schema-valid final authorization is `REQUIRE_REVIEW` and the operation/refusal/attempt set commits conclusively | preserve the complete PR #11 refusal bundle; `NO_EFFECT`; no fabricated review or approval artifact | `RETRYABLE_SAME_OPERATION`; retry eligibility does not itself satisfy the requested review |
| a purported `NOT_REQUIRED` evaluation returns `REQUIRE_HUMAN_APPROVAL` because the current rule or evaluator is inconsistent with admission | preserve truthful available evidence; `NO_EFFECT`; do not route into PR #20 | `TERMINAL_REQUIRES_NEW_OPERATION_KEY` when durably recorded; the contract/rule inconsistency requires separate repair |
| authorization `ALLOW`, then a current resource, evidence, pack/profile, correction-target, state, or other gate fails in a way that can change without changing caller content | preserve `ALLOW`, the gate failure, and non-consumable attempt evidence; `NO_EFFECT` | `RETRYABLE_SAME_OPERATION`; every later gate and current fact is re-evaluated |
| authorization `ALLOW`, then the exact fixed caller content deterministically cannot produce a contract-valid protected result | preserve `ALLOW` plus exact protected-effect failure; `NO_EFFECT` | `TERMINAL_REQUIRES_NEW_OPERATION_KEY`; unchanged deterministic invalidity cannot loop under the old key |
| proposed result ID already names different immutable bytes, or a prior admitted result binding differs | integrity/uniqueness conflict; no overwrite, effect, or consumption; `NO_EFFECT` when conclusively recorded | `TERMINAL_REQUIRES_NEW_OPERATION_KEY` |
| current rule changes away from stored `NOT_REQUIRED` after a durable no-effect operation | discover and reconcile the old operation first; no entry into either mode under the old key | terminal under the old key; when an attempt record is durably appended it carries `TERMINAL_REQUIRES_NEW_OPERATION_KEY` |
| current schema, protected-effect contract, or transaction profile would require rebinding the immutable operation | no effect or consumption; preserve original binding | `TERMINAL_REQUIRES_NEW_OPERATION_KEY` when conclusive and durably recorded |
| complete guard, serialization, uniqueness, or exclusive deadline check fails with authoritative rollback and no permanent content conflict | no effect or consumption; any committed attempt evidence is non-consumable | `RETRYABLE_SAME_OPERATION` |
| transient persistence or infrastructure failure has authoritative rollback proof | `NO_EFFECT`; never infer a decision consumption | `RETRYABLE_SAME_OPERATION` when the no-effect attempt is durably recorded |
| protected transaction rolls back before a first binding and no failure-evidence commit creates one | lower-level failure evidence may exist, but no operation is admitted | `NO_OPERATION_CONSEQUENCE` |
| failure-evidence persistence conclusively fails after proven rollback | do not claim a refusal, attempt, binding, or consequence that did not commit | `NO_NEW_CONSEQUENCE`; prior authoritative operation evidence controls, or no operation exists |
| response is lost after a complete refusal or domain-failure no-effect set committed | reconcile the exact commit and section 11.4 membership; recover `NO_EFFECT`, the original binding, and its already recorded consequence | preserve the original `RETRYABLE_SAME_OPERATION` or `TERMINAL_REQUIRES_NEW_OPERATION_KEY`; do not recalculate it |
| separate failure-evidence commit is uncertain after protected-effect rollback is proven | `NO_EFFECT` is already proven for the protected-effect transaction, but whether its evidence or first binding committed remains unknown | `BLOCKED_PENDING_RECONCILIATION` naming the evidence transaction; no new durable consequence or permission to replace the binding |
| caller projection conflicts with an existing tuple | reject the conflicting submission without creating an attempt for the existing operation | `NO_NEW_CONSEQUENCE`; existing operation state controls |
| protected-effect transaction outcome is ambiguous and no complete no-effect set is verified | `OUTCOME_UNKNOWN`; no no-effect claim or consequence | derived `BLOCKED_PENDING_RECONCILIATION`, naming the exact attempt or unresolved fact |
| one attempt is conclusively no-effect while another may have committed | retain the conclusive attempt and its consequence, but do not use it to authorize replay | derived `BLOCKED_PENDING_RECONCILIATION` because unresolved evidence has higher precedence |
| any success-labelled member is missing, mismatched, duplicated, or not atomically proven | invariant breach; neither success nor rollback is fabricated | `QUARANTINED_PARTIAL_SUCCESS`; separately governed repair only |

Immediate automatic retry is never implied. A deployment may require a current-state change, explicit caller retry, or bounded backoff before using `RETRYABLE_SAME_OPERATION`, provided it does not reinterpret the operation or reuse a decision.

### 11.4 Truthful failure evidence

A conclusive no-effect evidence commit contains only facts proven for that attempt. Depending on how far the attempt progressed, it may contain:

- the existing or newly admitted immutable operation binding;
- `NOT_REQUIRED` mode evidence;
- a PR #11 refusal request/result/internal-trace bundle;
- an `ALLOW` bundle plus a separately failing gate trace;
- an attempted or admitted result binding;
- authoritative rollback/status proof;
- the immutable attempt outcome and one consequence; and
- safe caller-facing qualification or problem references owned by PR #11 and CP2.

It contains no decision consumption, successful finalization evidence, protected result, success receipt, approval artifact, or success claim. A failed attempt is immutable and non-consumable. It can never be upgraded in place; later attempts append new evidence.

For a **complete matching no-effect set**, verification requires all of the following, not an arbitrary subset of the facts above:

1. exactly one immutable `NO_EFFECT` attempt record with its ID, authoritative sequence, tuple and operation-binding ref/digest, full-intent digest, reached-stage dispositions, and exactly one section 11.2 consequence;
2. the complete original operation binding and caller projection, newly committed for first admission or verified as unchanged historical inputs;
3. every record required by the stages actually reached: mode evidence when constructed, the complete PR #11 bundle when evaluation produced a result, and the exact failure and applicable gate traces supporting the recorded disposition; unperformed stages are explicit and never fabricated;
4. exact role-labelled membership recorded by the attempt, with finalized refs/digests for the required evidence and an identifier-only self-entry for that attempt; no nested copy of its own digest and no receipt, consumption, or later reconciliation record;
5. the section 10.3 transaction-role bindings, authoritative proof that this exact no-effect evidence set committed atomically, and matching immutable bytes/digests for all required members; and
6. authoritative proof that no protected result, consumption, or success receipt committed or can still commit for this attempt. When the set was written in a separate failure-evidence transaction, this includes conclusive rollback proof for the distinct protected-effect transaction.

A committed `DENY` or `REQUIRE_REVIEW` set retains its refusal bundle. A committed `ALLOW` plus domain-gate-failure set retains `ALLOW` and the failure trace; authorization is not rewritten to explain the no-effect outcome. Missing required members or contradictory status cannot be treated as complete failure evidence, and a pre-existing binding alone satisfies none of the attempt-specific outcome proofs.

If failure-evidence persistence conclusively fails, the runtime fails closed and reports only the runtime failure it can prove. If its acknowledgement is lost, it reconciles that evidence transaction before claiming persistence failed. Audit intent is not durable evidence.

---

## 12. Evidence-profile ownership

This candidate adds no machine schema. Later materialization may add the issue #25 profiles as distinct tags within the already proposed `AuthorizationFinalizationEvidence v0.2` package. If that package cannot express these truth claims without ambiguity, schema work stops for a separate reviewed packaging decision; it must not widen PR #20 silently.

| Evidence or record | Semantic owner | Proposed package/profile | Exact truth claim | Success-set placement | Failure and retry posture |
|---|---|---|---|---|---|
| operation binding | issue #25 | `AuthorizationFinalizationEvidence v0.2` / `NOT_REQUIRED_OPERATION_BINDING_V0_1` | one tuple and caller projection admitted one immutable runtime-finished intent, mode, contract, profile, and bind-once digest | required member; inserted on first success or referenced unchanged if a prior no-effect set admitted it | may commit with a conclusive no-effect set; never rewritten; retained or tombstoned against unsafe reuse |
| transaction attempt | issue #25 | `AuthorizationFinalizationEvidence v0.2` / `NOT_REQUIRED_TRANSACTION_ATTEMPT_V0_1` | one ordered attempt used exact trusted transaction inputs and had one truthful outcome | exactly one successful-attempt record | no-effect attempt is non-consumable and has one consequence; uncertain observation has neither and remains subject to reconciliation |
| mode-correct `NOT_REQUIRED` evidence | issue #25 | `AuthorizationFinalizationEvidence v0.2` / `NOT_REQUIRED_MODE_EVIDENCE_V0_1` | the current rule selected no human-finalization requirement and no human-finalization evidence was supplied | exactly one | may accompany a no-effect attempt; never an approval or authority source |
| authorization request/result/full internal trace | PR #11 | `AuthorizationDecisionEvidence v0.2` | the complete evaluator input, current result, selected path/basis, cutoffs, and internal reasoning for this attempt | exact final `ALLOW` bundle and digest | truthful refusal bundle may commit without effect; never reused by a later attempt |
| decision consumption | PR #11 semantics with issue #25 atomicity | `AuthorizationFinalizationEvidence v0.2` / single-use decision-consumption tag | this exact transaction consumed this exact decision once with the committed effect; its receipt link is the preallocated immutable ID only, never a receipt digest | exactly one; hashed before the receipt, which binds its ref/digest | absent for no-effect and uncertain outcomes; provisional uniqueness is not durable consumption |
| AssertionRecord assertion-act fields/evidence | PR #23 | future `AssertionRecord v0.2` and its immutable assertion-act evidence binding | who asserted, exact `assertedAt`, posture, and conditional verified-offline evidence | inside exact protected result or referenced immutable evidence as PR #23 requires | original admitted facts persist across retry; never reclassified as human approval |
| protected result | PR #23 for the first handoff; each later domain contract for its own family | future `AssertionRecord v0.2` operation branch for the first handoff | exactly one immutable pending-review operation claim whose bytes satisfy the contract | exact contract-owned result set | absent on no effect; an admitted-but-uncommitted result binding is evidence, not the result |
| admitted protected-result binding | issue #25 transaction boundary, consuming the domain contract's values | `AuthorizationFinalizationEvidence v0.2` / fixed `/admittedProtectedResultBinding` subobject of `NOT_REQUIRED_TRANSACTION_ATTEMPT_V0_1` | the first passing handoff fixed one exact proposed result identity, bytes digest, schema, contract, and trace for this operation | required in the successful attempt or referenced to the lowest prior durable attempt that fixed it | may exist in a no-effect attempt without making the result exist; every later binding must match exactly |
| protected-effect validation trace | PR #23 for the first handoff | separately reviewed shared trace envelope carrying PR #23 `AR_*` and `PC_*` payload | exact mappings and postconditions were evaluated with overall `PASS` or truthful `FAIL` | one overall passing trace | failing trace may be retained as non-consumable attempt evidence; it cannot become `PASS` later |
| other applicable gate traces | each active `EnforcementChain` gate owner | each owner's existing or separately reviewed evidence profile | the named gate's exact inputs and truthful disposition | every applicable passing trace; inapplicable gates are not invented | truthful failure may commit without effect; one gate cannot reinterpret another's result |
| governed-effect receipt | issue #25 transaction boundary | `AuthorizationFinalizationEvidence v0.2` / `NOT_REQUIRED_GOVERNED_EFFECT_RECEIPT_V0_1` | the complete matching success membership committed atomically; finalized consumption ref/digest and identifier-only receipt self-entry prevent a digest cycle | exactly one, hashed last among the success records and exposed only after commit | absent for no effect; an uncertain caller copy is not proof; partial membership is quarantined |
| ingress rejection | PR #11 | `AuthorizationDecisionEvidence v0.2` / `AuthorizationRequestRejection v0.2` | only safely established malformed or invalid ingress facts | never a success member | may exist without an operation; persistence failure invents no rejection or operation consequence |
| authorization refusal evidence | PR #11 | `AuthorizationDecisionEvidence v0.2` request/result/trace refusal branch | one schema-valid current evaluation returned `DENY`, `REQUIRE_REVIEW`, or another truthful non-allow outcome | never a success member | may commit in a no-effect attempt set; non-consumable and never reused as authority |
| non-consumable failure-attempt evidence | issue #25 plus the failing gate owner | `AuthorizationFinalizationEvidence v0.2` / `NOT_REQUIRED_TRANSACTION_ATTEMPT_V0_1` with bound failure traces | no protected effect or consumption committed and the recorded failure facts were proven | never a success member | one immutable no-effect consequence when conclusive; no consequence when persistence fails or outcome is uncertain |
| reconciliation observation/resolution | issue #25 transaction boundary | `AuthorizationFinalizationEvidence v0.2` / `NOT_REQUIRED_RECONCILIATION_EVIDENCE_V0_1` | exact transaction roles/status keys and evidence proving complete success, a committed no-effect set, protected-effect rollback, or a still-unresolved fact | outside the original atomic set; a later resolution points back to the existing receipt or attempt ref/digest, never the reverse | append-only; cannot rewrite an uncertain observation, committed receipt, or recorded consequence, or manufacture missing members |
| retention, encryption, deletion, or key-custody evidence | issue #14 and later custody boundaries | separately owned policy/evidence profiles | how bytes are retained or governedly removed | immutable policy refs only where required | cannot make a tuple reusable or erase the historical binding while obligations remain |

### 12.1 Integrity closure for issue #25 profiles

Every later issue #25 machine profile rejects duplicate JSON names and unknown members and uses RFC 8785 JCS, UTF-8, and SHA-256. In addition to the already closed `operationBindingDigest`, the exact top-level self-digest members and provisional sentinels are:

| Profile | Self-digest member | Exact provisional sentinel |
|---|---|---|
| `NOT_REQUIRED_TRANSACTION_ATTEMPT_V0_1` | `transactionAttemptDigest` | `ofarm:pending-transaction-attempt-digest` |
| `NOT_REQUIRED_MODE_EVIDENCE_V0_1` | `notRequiredModeEvidenceDigest` | `ofarm:pending-not-required-mode-evidence-digest` |
| `NOT_REQUIRED_RECONCILIATION_EVIDENCE_V0_1` | `reconciliationEvidenceDigest` | `ofarm:pending-reconciliation-evidence-digest` |
| `NOT_REQUIRED_GOVERNED_EFFECT_RECEIPT_V0_1` | `governedEffectReceiptDigest` | `ofarm:pending-governed-effect-receipt-digest` |

Each construction removes exactly its one top-level self-digest member after validating that sentinel, hashes every other member, inserts `sha256:` plus 64 lowercase hexadecimal characters, and validates the final record. No nested member or other top-level member is excluded. The caller projection remains the self-digest-free object defined in section 5.3.

An identifier-only reference under sections 9.4, 11.4, and 12.2 has no digest field in the record's schema branch; it is not a digest excluded from hashing. In particular, consumption has no receipt-digest member, and the receipt self-membership entry has no digest member. Those absent fields cannot be represented by nulls, sentinels, duplicate nested self-digests, or an undocumented projection exception. Final committed records contain no provisional sentinel and undergo no post-hash mutation.

Decision-evidence, decision-consumption, protected-effect-trace, and domain-result digests remain governed by their owning contracts. This integrity rule cannot alter their projections.

All transaction/evidence tags enter OFARM authority, if admitted there, as the existing `EvidenceEvent` / `evidence record` classification described by PR #11. They create no new event family, domain truth, current state, or promotion by themselves.

### 12.2 Acyclic construction and verification order

The proposed evidence profiles must support this exact construction order within the guarded atomic boundary:

1. allocate the unique immutable transaction-evidence identifiers needed for identifier-only forward references, including the governed-effect receipt ID, independently of their eventual digests; this does not replace content-addressed refs owned by other contracts;
2. finalize the operation binding, mode evidence, authorization bundle, proposed domain result, and applicable validation/guard evidence under their owning contracts, in dependency order; mode evidence names the attempt by ID/sequence, not by its later digest;
3. construct and hash consumption with those finalized bindings, the exact transaction/attempt identity, and the preallocated receipt ID only;
4. construct and hash the successful attempt, including its admitted-result subobject or prior binding, finalized evidence/consumption refs and digests, and any receipt back-reference by ID only; it contains no receipt digest and no reference to its own digest inside its admitted-result subobject;
5. construct and hash the receipt with the finalized consumption and attempt refs/digests, every other required member binding, and the identifier-only receipt self-entry in section 9.4;
6. independently verify every final digest using its owning projection, verify all role cardinalities and identifier back-references, recheck the complete guards, and commit the unchanged complete success set atomically; and
7. if later reconciliation is needed, construct append-only resolution evidence pointing back to the original finalized receipt or no-effect attempt. No earlier record gains a forward reference to that later evidence.

Inside this transaction-evidence construction, a reference to a record finalized later may contain only its preallocated immutable ID, never a future digest. A digest-bearing reference must point to already finalized bytes. This does not alter owner-defined bundle projections such as PR #11's joint decision-bundle digest. If an owning contract cannot satisfy the construction without changing its semantics, stop for separate prerequisite review; do not invent an exclusion or modify that contract here.

For a no-effect set, finalize the truthful supporting evidence and any required protected-effect rollback proof first, then hash the no-effect attempt and its section 11.4 membership. There is no consumption or receipt. Its evidence-commit status is verified separately using the preallocated transaction-status key; later status/reconciliation evidence is not inserted into the already hashed attempt. Any historical admission trace remains provenance; a current attempt still supplies its fresh passing validation trace and current authorization/snapshot bindings before success.

---

## 13. Single-use consumption, identifiers, and concurrency

### 13.1 Immutable identifiers

The protocol keeps distinct immutable identifiers for:

- logical operation;
- caller-submission projection and operation binding;
- transaction attempt and attempt sequence;
- authorization request/result/trace bundle;
- `NOT_REQUIRED` mode evidence;
- decision consumption;
- admitted protected-result binding;
- protected result and validation trace;
- governed-effect receipt; and
- reconciliation evidence.

No identifier may resolve to two byte sequences. A retry resolves existing identifiers where required; it does not mint a replacement identity for a completed fact.

### 13.2 Required uniqueness

The authoritative atomic boundary enforces:

- one lookup tuple maps to one logical operation and one operation-binding digest;
- one logical operation has at most one effect-capable unresolved attempt;
- each durable attempt sequence belongs to exactly one immutable attempt;
- one logical operation has at most one successful receipt;
- one logical operation has at most one successful write-decision consumption;
- one authorization decision is consumed at most once;
- one admitted protected-result role maps to one result identity/digest;
- every committed result ID maps to one immutable byte sequence; and
- one success receipt identifies one complete atomic membership set.

No application-level check followed by an unguarded insert satisfies these rules.

### 13.3 Consumption linearization

Decision consumption becomes durable only at the complete successful commit. Reserving a unique row, building a consumption object, obtaining authorization `ALLOW`, validating a result, or starting commit is not consumption.

The consumption record binds the authorization decision bundle, logical operation and operation-binding digest, exact transaction/attempt identity, `NOT_REQUIRED` mode evidence, consuming principal, full effect-intent digest, exact committed result refs/digests, the preallocated immutable receipt ID only, trusted consumption time, and `SINGLE_USE`. It contains no receipt digest. The receipt is finalized later and binds this finalized consumption ref/digest; both commit atomically and verification enforces that consumption's receipt ID names that same receipt. Section 12.2 closes the construction order. Human approval, reservation, and approval-consumption fields are absent.

If the transaction conclusively rolls back, the decision remains unconsumed and non-portable. A later attempt obtains another current decision and creates another prospective consumption object. It never consumes the earlier decision.

### 13.4 Concurrent and repeated submissions

When identical first submissions race, the tuple uniqueness rule selects one authoritative binding. Matching losers discard their provisional trusted completion and resolve the winner.

When exact retries race after a retryable no-effect attempt, at most one effect-capable attempt proceeds. Others wait for or resolve its authoritative status. When a successful commit wins, matching contenders return the same verified result/receipt subject to disclosure controls.

When caller projections, represented parties, operation bindings, admitted results, or committed result bytes conflict, no loser may borrow the winner's receipt. Different logical operations that target the same mutable domain state remain subject to the domain-state and complete guard; one operation's idempotency does not grant compatibility with another.

---

## 14. Disclosure, retention, and no-unsafe-forgetting rule

### 14.1 Receipt lookup is not read authority

Every retry or status lookup authenticates the requester and scopes access before exposing operation information. The caller key is not a read credential. PR #11 safe-response, trace-minimization, redaction, and CP2 qualification rules govern returned content.

A matching completed operation remains historically complete even if current permissions no longer permit the original result bytes to be returned. The runtime withholds or redacts as currently required and does not re-execute the write to recreate a response. Any separate full trace or protected-result read requires its own governed read authority; it is not another consumption of the original write decision.

A conflicting caller receives no receipt as proof of its different submission. Public response codes remain owned by PR #11 and CP2; this candidate's internal lifecycle labels do not register new public codes.

### 14.2 No unsafe forgetting

Retention or governed deletion may remove bulky bytes only under separately approved issue #14 policy. It may not make the authoritative tuple reusable while any of these remains reachable:

- committed protected effect or result;
- governed-effect receipt or decision consumption;
- unresolved transaction attempt or reconciliation obligation;
- retryable same-operation obligation;
- admitted protected-result binding;
- conflict-detection or audit obligation; or
- authoritative historical operation binding.

While same-operation retry is possible, the complete runtime-finished intent and every trusted fact needed for fresh evaluation remain retrievable and digest-verifiable. While reconciliation is pending, every status and membership input needed to distinguish complete success, a committed no-effect set, protected-effect rollback, and any separate evidence-commit outcome remains available.

After policy permits removal of bulky evidence, an immutable binding or tombstone still preserves at least the tuple binding, key-profile identity, operation-binding digest, caller-projection digest, original intent digest, mode/schema/contract/profile bindings, final operation state, admitted or committed result binding, receipt/consumption binding where applicable, and the reason tuple reuse remains prohibited. A tombstone never turns a completed or terminal operation into an unused key.

If required retry or reconciliation bytes disappear contrary to policy, the operation is quarantined; the runtime must not guess, reconstruct trusted fields, or rebind the tuple.

This candidate selects no retention duration, encryption method, deletion mechanism, table layout, or key custodian.

---

## 15. First concrete handoff: `ASSERT_OPERATION_CLAIM`

### 15.1 Exact rule and contract closure

The first handoff consumes these exact approved candidate facts:

| Dimension | Exact value |
|---|---|
| action | `ASSERT_OPERATION_CLAIM` |
| authority family | `ASSERT_SUBMIT` |
| stage | `DRAFT_PREPARATION` |
| agent posture | `AGENT_ALLOWED_WITH_POLICY_CHECK` |
| human finalization | `NOT_REQUIRED` |
| intent profile | `EI_OPERATION_ASSERTION_V0_2` |
| resource policy | `RP_SCOPE_ONE` |
| historical authority posture | `CURRENT_REPORT_AUTHORITY_ONLY` |
| external effect posture | `NO_EXTERNAL_DISPATCH` |
| action-level evidence policy | `EP_NONE` |
| consumption | `SINGLE_USE` |
| approval policy | `NO_SEPARATE_APPROVAL_POLICY` |
| protected-effect contract | `ofarm.protectedeffect.assertionrecord.submit.v0.1` |

`EP_NONE` means no additional action-level authorization evidence policy. It does not permit omission of PR #23's non-empty assertion evidence bindings or conditional verified-offline assertion-act evidence.

### 15.2 Exact result mapping

The transaction preserves this complete mapping without reinterpretation:

```text
ASSERT_OPERATION_CLAIM
  -> EI_OPERATION_ASSERTION_V0_2
  -> authorization effect-subject kind OPERATION_ASSERTION
  -> AssertionRecord assertionType OPERATION_CLAIM_ASSERTION
  -> claimState PENDING_REVIEW
  -> record commit class: operation claim (OPERATION_CLAIM)
```

The protected result is exactly one future `ofarm.assertionrecord.v0.2` operation branch. The transaction coordinator verifies PR #23's exact result schema, complete bytes/digest, `AR_*` mappings, `PC_*` postconditions, and overall passing trace. It does not inspect the record through a second mapping table.

### 15.3 Preserved domain distinctions

The result preserves:

- the proposed assertion ID, typed subject, sole immutable authority anchor, body, non-empty evidence bindings, and `PENDING_REVIEW` state;
- `assertedByPartyRef` from the canonical selected authority subject;
- alleged `performedByPartyRef` separately from the reporter;
- performer authority exactly `NOT_EVALUATED_BY_AUTHORIZATION`;
- `INTENDED` or `PERFORMED` claim posture and its exact permitted subject-time profile;
- `TRUSTED_ONLINE_SUBMISSION` with runtime-supplied bind-once `assertedAt`, or `VERIFIED_OFFLINE_SUBMISSION` with exact immutable act evidence;
- conditional software-agent actorship and performer-authority evidence bindings;
- conditional correction lineage, including positive prior-record visibility in the trusted transaction-start snapshot; and
- optional semantic-event association only through PR #23 and the separately passing Event Ingress classification.

The transaction supplies the trusted starting-snapshot proof and complete guards used by PR #23's correction predicate. It does not redefine that predicate, derive a primary event family from assertion subtype, or treat an event association as another result.

### 15.4 Forbidden effects

Successful submission creates no:

- accepted executed intervention consequence;
- proof that the alleged performer was authorized;
- ReviewDecision, acceptance, rejection, contestation, or supersession;
- current-state materialization or current operation state;
- mutation or deletion of a prior assertion;
- implicit SemanticEventEnvelope or companion domain record; or
- external dispatch.

Other state-affecting `NOT_REQUIRED` actions remain unsupported until their own approved protected-effect contracts and exact bindings enter this profile through separately reviewed work.

---

## 16. Production-reachable falsifiable cases

These are obligations for later executable conformance. This documentation PR does not claim that runtime tests ran.

| Case | Required disposition |
|---|---|
| eligible initial operation claim | one complete atomic success set and exactly one immutable pending-review AssertionRecord |
| construct a complete success set in section 12.2 order | independently verify every final digest and back-reference; no receipt digest in consumption, nested receipt self-digest, provisional sentinel in final bytes, post-hash mutation, or undocumented exclusion |
| a receipt self-entry gains a digest, consumption gains a receipt digest, or an earlier record hashes a future record | reject the invalid evidence profile or construction; no protected effect or consumption commits |
| later reconciliation proves a committed success | append resolution evidence referencing the original receipt ref/digest; original receipt bytes, digest, and atomic membership stay unchanged |
| exact retry after commit, including lost response | verify and return the original permitted IDs, digests, `assertedAt`, result, and receipt; no second decision consumption or effect |
| identical online submissions with the same tuple arrive concurrently at different receipt times | one authoritative binding and one success; matching losers recover the winner's `assertedAt`; no artificial timestamp conflict |
| same tuple carries changed caller effect content | discover the earlier operation, reject the projection conflict, and create no new hidden operation |
| same tuple is routed under a changed schema, contract, transaction profile, or mode | discover and reconcile the earlier operation before any terminal or conflict result; never use another namespace |
| durable no-effect `NOT_REQUIRED` attempt followed by a current fresh-approval or direct-human mode | `TERMINAL_REQUIRES_NEW_OPERATION_KEY` after success/partial/unresolved precedence; do not enter either profile under the old key |
| a mode change exists while an earlier attempt remains unresolved | `BLOCKED_PENDING_RECONCILIATION`; do not encourage a new-key submission until the possible old effect is resolved |
| retry recomputes a full operation digest with a new runtime timestamp | conformance failure; compare the stored caller projection and recover the bind-once full intent/digest |
| caller supplies an online assertion timestamp or cached binding evidence | ingress rejection or projection conflict as applicable; it cannot create trusted time or override stored evidence |
| verified offline assertion has different assertion, receipt, authorization, and commit times | preserve each exact governed time and evidence; create no human-finalization artifact |
| natural-person requester is treated as direct-human-finalization mode | conformance failure; current rule-selected `NOT_REQUIRED` remains controlling |
| software-agent requester omits CP3 evidence because human approval is absent | authorization non-allow; absence of finalization does not weaken agent authorization |
| approval, challenge, reservation, intended-approver, or approval-consumption data is inserted | profile/branch failure; no effect or consumption |
| revocation is inserted after lookup, or a relevant resource/evidence/policy/state input changes before commit | complete positive/negative/set guard blocks stale success |
| commit reaches `transactionDeadline` or `decisionValidUntil` exactly | exclusive cutoff fails; no successful commit claim |
| result bytes, result schema, contract binding, or validation trace are substituted | handoff/integrity failure; no effect or consumption |
| authorization is `ALLOW` and a domain gate fails | preserve `ALLOW` as the authority-gate result and record only truthful non-consumable failure evidence |
| committed `DENY`, then authority changes and exact retry occurs | original refusal remains immutable; fresh current evaluation is required under `RETRYABLE_SAME_OPERATION`; original `assertedAt` remains fixed |
| complete `DENY` no-effect set commits but its response is lost | verify the exact committed refusal/attempt/binding set and authoritative absence of an effect/consumption/receipt for that attempt; recover `NO_EFFECT` and its original retryable consequence, not a rollback or a newly evaluated refusal |
| complete `ALLOW` plus domain-gate-failure no-effect set commits but its response is lost | recover `ALLOW`, the exact failure trace, original binding, and recorded retryable or terminal consequence; a successful evidence commit is not a protected-effect success |
| protected-effect transaction rolls back, then a separate first-admission failure-evidence commit succeeds but its response is lost | verify both distinct transaction identities/statuses; recover the committed binding, original `assertedAt`, and no-effect consequence without claiming that the evidence transaction rolled back |
| protected-effect rollback is proven but the separate evidence commit remains uncertain | retain the proven no-effect fact, block the tuple on the evidence-transaction key, and create no replacement binding or new durable consequence |
| protected-effect rollback and conclusive failure of the separate evidence commit are both proven | no new consequence; an earlier binding/history remains unchanged, or no operation exists if no binding ever committed |
| an earlier binding survives while the current attempt rolls back | verify rollback only for the current attempt's writes; the historical binding alone is not a partial-success breach |
| purported committed no-effect evidence lacks a required gate trace, names another attempt's status proof, or coexists with consumption for that attempt | do not resolve as `NO_EFFECT`; block incomplete evidence or quarantine a proven invariant breach, without replay or evidence synthesis |
| committed `REQUIRE_REVIEW`, then exact retry occurs | apply `RETRYABLE_SAME_OPERATION` without fabricating review completion or reusing the earlier decision |
| current-state-dependent domain failure later clears | later attempt may proceed only under `RETRYABLE_SAME_OPERATION` with complete fresh evaluation and guards |
| deterministically invalid protected-result bytes are retried unchanged | prior terminal consequence prevents an indefinite same-key loop |
| transient infrastructure failure has conclusive durable no-effect evidence | `RETRYABLE_SAME_OPERATION`; no earlier decision is reused |
| first transaction rolls back and failure evidence does not durably admit a binding | no logical-operation consequence or surviving operation-level `assertedAt` is claimed |
| idempotency keys differ only by case | both are valid and byte-distinct keys |
| key has trailing space or non-ASCII Unicode | key is invalid and is not normalized into another key |
| key substitutes `.`, `_`, `:`, or `-` | punctuation remains literal; changed valid bytes identify a different key |
| bulky evidence is governedly deleted while an operation remains reachable | required tombstone preserves conflict detection; tuple is not rebound |
| retryable full intent is deleted | quarantine as retention conformance failure; do not reconstruct or rebind |
| valid request is refused but refusal-evidence persistence fails | no false durable refusal or new attempt consequence; prior authoritative evidence controls |
| malformed ingress fails before durable binding | only the truthful PR #11 ingress rejection may be recorded; no operation lifecycle is invented |
| one attempt is conclusive no-effect and another remains unresolved | unresolved precedence blocks reapplication and names the separate attempt |
| status lookup is stale, incomplete, timed out, or cache-only | remain blocked; absence is not rollback proof |
| success receipt exists but a required member is missing or mismatched | quarantine partial success; no automatic synthesis, deletion, or replay |
| two success receipts or two consumptions appear | quarantine invariant breach; no winner is guessed from timestamps |
| receipt retry occurs after disclosure permission changes | preserve historical completion and prevent duplicate execution while applying current safe disclosure rules |
| conflicting caller content asks for the winner's receipt | do not disclose or lend the receipt as success for the conflicting submission |
| governed read or unapproved effect family attempts to use this profile | unsupported; no inferred transaction support |

Later tests must enter through the real shared lookup, trusted enrichment, authorization, protected-effect validation, atomic persistence, receipt lookup, and reconciliation paths. Unit-only helpers are not sufficient for a conformance claim.

---

## 17. Protocol invariants

1. One authoritative tuple names at most one logical operation across handlers.
2. Tuple equality and caller-projection equality are separate and both are required for an exact retry.
3. A valid key is compared byte-for-byte with no normalization or collation.
4. The operation-binding digest is fixed once and recovered thereafter.
5. Online `assertedAt` is the winner's runtime-observed pre-validation assertion time, never a commit or retry time.
6. No durable binding means no surviving operation-level trusted-intent claim.
7. No caller, cache, schema hint, or response receipt supplies a trusted operation fact.
8. The current immutable rule alone selects the transaction mode.
9. `NOT_REQUIRED` creates no human-finalization artifact, while domain assertion-act provenance remains intact.
10. Every effect-capable attempt obtains a fresh current authorization decision.
11. `ALLOW` proves only the authority gate and never bypasses another applicable gate.
12. The complete relevant read/write set, including negative and set-valued facts, is guarded through commit.
13. `decisionValidUntil` and `transactionDeadline` are exclusive and both remain valid through commit.
14. No protected effect becomes visible without its matching decision evidence, mode evidence, consumption, traces, and receipt.
15. Decision consumption linearizes only with the complete successful effect set.
16. One logical operation commits at most one protected result set, one decision consumption, and one success receipt.
17. A result ID never resolves to two byte sequences.
18. A failed attempt is non-consumable and never upgraded in place.
19. `NO_EFFECT` requires conclusive evidence; uncertainty is never converted to rollback by timeout or missing cache data.
20. Every durable no-effect attempt has exactly one of the two closed consequences.
21. Complete verified success outranks partial, unresolved, and no-effect evidence; partial outranks unresolved; unresolved outranks no-effect retry policy.
22. A mode change cannot bypass an unresolved attempt.
23. A partial success set is quarantined, not repaired or replayed automatically.
24. Receipt lookup cannot create disclosure authority.
25. Retention or deletion cannot make an authoritative tuple reusable while its obligations or history remain reachable.
26. An operation claim remains pending review and never becomes accepted execution or current state through this protocol.
27. Receipt and consumption linkage is bidirectional by identity but acyclic by digest; finalized records are never mutated to complete a reference cycle.
28. A committed no-effect evidence transaction is not a rollback, and every proof identifies the exact transaction and attempt it proves.
29. A separate evidence commit must be settled independently before its binding or consequence can govern another attempt.

---

## 18. Traceability to issue #25 and pinned dependencies

### 18.1 Issue #25 acceptance closure

| Issue #25 requirement | Candidate disposition |
|---|---|
| admit only state-affecting `NOT_REQUIRED`; exclude `RECEIVE_READ_DATA` | sections 1, 3, and 7 |
| preserve exact PR #11, #20, and #23 heads and ownership | sections 3 and 4 |
| explicit compatibility ledger against PR #20 | section 4 |
| exact shared lookup tuple, separate from operation digest | sections 5.1 and 5.5 |
| cross-handler lookup with no mode/schema/result namespace | sections 5.1, 9.1, and 10 |
| exact key grammar and equality | section 5.2 |
| exact caller-owned projection and exclusions | section 5.3 |
| runtime-completed intent and full-intent digest relationship | section 5.4 |
| bind-once complete operation binding | section 5.5 |
| result substitution against admitted/committed binding | section 5.6 |
| exact first durable admission point | section 6.1 |
| preserve runtime-observed online assertion time rather than commit time | sections 5.4 and 6.2 |
| concurrent first-admission winner | section 6.3 |
| rollback survival and no reconstruction from caller memory | section 6.4 |
| no fabricated human-finalization artifacts | sections 4 and 7.2 |
| exact `NOT_REQUIRED` evidence truth claim and placement | section 7.3 |
| immutable transaction policy, trusted inputs, and complete guards | section 8 |
| ordered current evaluation, gates, handoff, and commit | section 9.2 |
| complete atomic success set and verified receipt | sections 9.3 and 9.4 |
| acyclic consumption/receipt digests, self-membership, and append-only reconciliation | sections 9.4, 12.1, 12.2, and 13.3 |
| deterministic success/partial/unresolved/no-effect precedence | section 10.1 |
| mode-change terminal without bypassing uncertainty | sections 10.1, 10.2, and 11.3 |
| `EFFECT_COMMITTED`, `NO_EFFECT`, and `OUTCOME_UNKNOWN` | section 11.1 |
| exactly two conclusive no-effect consequences | section 11.2 |
| closed failure lifecycle and evidence-persistence failure | sections 11.3 and 11.4 |
| committed no-effect recovery and distinct protected-effect/evidence transaction proofs | sections 6, 10.3, 11, and 16 |
| evidence-profile ownership table | section 12 |
| one consumption/result/receipt and concurrency behavior | section 13 |
| receipt disclosure limits | section 14.1 |
| no unsafe forgetting | section 14.2 |
| first concrete operation-claim handoff | section 15 |
| production-reachable hostile cases | section 16 |
| staged delivery and completion | sections 21 and 22 |

### 18.2 PR #11 authorization handoff

This candidate consumes without redefining:

- exact principal/representation and path-specific authority-subject resolution;
- the `ASSERT_OPERATION_CLAIM` action row and its `NOT_REQUIRED`, `TRANSACTION_BOUND_V0_2`, and `SINGLE_USE` selections;
- the `EI_OPERATION_ASSERTION_V0_2`, `RP_SCOPE_ONE`, `CURRENT_REPORT_AUTHORITY_ONLY`, `EP_NONE`, and `NO_EXTERNAL_DISPATCH` semantics;
- full effect-intent validation and JCS/SHA-256 binding;
- current authorization evaluation, outcome lattice, cutoff calculation, internal trace, and decision-bundle digest;
- truthful ingress rejection and refusal evidence; and
- safe response and disclosure boundaries.

The new operation projection, admission, attempt, and reconciliation rules do not become a second authorization evaluator. A later accepted-law promotion must update the transaction prerequisite for state-affecting `NOT_REQUIRED` rows to name issue #25 alongside issue #19; this Phase A PR does not edit the approved PR #11 candidate.

### 18.3 PR #20 transaction compatibility handoff

This candidate adopts only the concepts marked compatible in section 4. It does not edit PR #20, add a third mode to that document, or attach approval semantics to `NOT_REQUIRED`. The issue #25 profiles remain a separate semantic owner even if later machine review packages their tags beside PR #20 tags in `AuthorizationFinalizationEvidence v0.2`.

### 18.4 PR #23 domain handoff

This candidate verifies and commits the exact PR #23 operation branch without copying its field mappings or postconditions. PR #23 remains the sole owner of:

- `AssertionRecord v0.2` shape;
- online/offline assertion-act posture and timestamp sourcing;
- assertion subject, sole anchor, body, evidence, reporter/performer separation, subject time, and correction lineage;
- optional Event Ingress association;
- action/effect-subject/subtype/commit-class mapping;
- result digest and validation trace; and
- prohibition on acceptance, current state, prior-history mutation, or implicit companion effects.

The transaction owns the starting snapshot and guard evidence consumed by those checks, not the checks' domain meaning.

### 18.5 Downstream implementation ownership

OFARM2 #173 owns UnitOfWork foundations, OFARM2 #178 owns command-idempotency implementation, and OFARM2 #353 owns authorization-evaluator implementation. They may consume this protocol only after exact non-default machine-contract materialization and binding review, accepted semantic promotion, required conformance and current/default promotion, and byte/digest-verified extraction in section 21's governed order. None may infer canonical meaning from this candidate alone.

---

## 19. Steward approval card

| Decision | Proposed answer | Approval required |
|---|---|---|
| Does this protocol apply only to state-affecting rules selecting `NOT_REQUIRED`? | yes | yes |
| Is `RECEIVE_READ_DATA` excluded despite also selecting `NOT_REQUIRED`? | yes; PR #11 governed-read semantics remain separate | yes |
| Does adoption of compatible PR #20 concepts leave that PR's two human-finalization modes unchanged? | yes | yes |
| Is the authoritative lookup tuple exactly boundary kind/ref, authenticated principal ref, represented Party ref-or-null, action, and caller key? | yes | yes |
| Are mode, schema, intent digest, result digest, transaction-profile version, and handler prohibited as lookup namespaces? | yes | yes |
| Is `OFARM_OPERATION_IDEMPOTENCY_KEY_V0_1` exactly 1–255 ASCII bytes matching `^[A-Za-z0-9._:-]{1,255}$`? | yes | yes |
| Is key equality byte-exact with no trim, case folding, Unicode normalization, collation, escape interpretation, or punctuation replacement? | yes | yes |
| Do action/boundary/principal/representation/key remain compared through the tuple while caller operation content remains in one exact projection? | yes | yes |
| Does the caller projection include the complete resolved caller-owned effect-intent object and exclude only named per-attempt/non-authoritative envelope facts? | yes | yes |
| For trusted online submission, are only runtime-owned `/assertedAt` and the already prohibited offline evidence member absent from caller content? | yes | yes |
| For verified offline submission, are `assertedAt` and its immutable evidence binding retained in caller content? | yes | yes |
| Is the projection only a conflict oracle rather than a second effect intent or authorization source? | yes | yes |
| Does full-intent JCS/SHA-256 still cover the runtime-completed schema-valid effect intent? | yes | yes |
| Is the complete operation binding shape and digest projection closed by section 5.5? | yes | yes |
| Is `representedPartyBinding` required as exact JSON null when representation does not apply? | yes | yes |
| Is the operation-binding digest fixed once and recovered rather than recomputed on retry? | yes | yes |
| Does an admitted protected-result binding stop result substitution without becoming another lookup namespace or result existence claim? | yes | yes |
| Is the first durable binding exactly the first atomic success or conclusive-no-effect commit containing it? | yes | yes |
| Are locks, staged inserts, caches, and an ambiguous response insufficient to prove that binding, while a verified commit still admits it if its reply was lost? | yes | yes |
| Does a first-attempt failure-evidence commit require authoritative rollback proof and atomic tuple uniqueness? | yes | yes |
| Is online `assertedAt` still the runtime-observed pre-validation assertion time, not the binding commit or effect commit time? | yes | yes |
| Do matching concurrent losers discard their timestamps and recover the winning binding? | yes | yes |
| If no binding survives rollback, is no operation-level timestamp or digest reconstructed from caller memory? | yes | yes |
| Does the current immutable rule, never the caller or principal kind, select the mode? | yes | yes |
| Are every approval, challenge, reservation, intended-approver, approval-consumption, and direct-human-finalization artifact absent? | yes | yes |
| Does `NOT_REQUIRED_MODE_EVIDENCE_V0_1` claim only rule-selected absence of human finalization? | yes | yes |
| Can PR #23 offline assertion-act evidence remain required without becoming human approval? | yes | yes |
| Is the future transaction profile content-addressed and caller-invariable? | yes | yes |
| Must the transaction guard positive, negative, set-valued, and write facts through commit? | yes | yes |
| Is one undocumented isolation label insufficient? | yes | yes |
| Does every effect-capable retry obtain a fresh current PR #11 decision and repeat all gates? | yes | yes |
| Is authorization `ALLOW` only the authority-gate result? | yes | yes |
| Does successful commit include exact operation, attempt, decision, mode, consumption, result, trace, and receipt evidence? | yes | yes |
| If the immutable operation binding predates success, is it guarded and referenced rather than rewritten? | yes | yes |
| Does a successful receipt count only after complete matching set and atomic-status verification? | yes | yes |
| Does consumption bind a preallocated receipt ID without its digest, while the later receipt binds finalized consumption and has an identifier-only self-entry? | yes; section 12.2 defines the acyclic order | yes |
| Must later reconciliation point back to unchanged committed records rather than change their bytes or original membership? | yes | yes |
| Does operation admission apply complete success, partial breach, unresolved attempt, then latest no-effect consequence in that order? | yes | yes |
| Does unresolved evidence block a mode-change terminal response and new reapplication? | yes | yes |
| Are transaction outcomes separate from authorization outcomes and public problem codes? | yes | yes |
| Does every durable conclusive no-effect attempt carry exactly one of the two closed consequences? | yes | yes |
| Is `BLOCKED_PENDING_RECONCILIATION` derived rather than a third no-effect consequence? | yes | yes |
| Are committed `DENY` and `REQUIRE_REVIEW` retryable only through a fresh current decision, never decision reuse? | yes | yes |
| Is a deterministic fixed-content protected-result failure terminal under the old key? | yes | yes |
| Is a transient failure with authoritative rollback proof retryable under the same immutable operation? | yes | yes |
| Does failure-evidence persistence failure create no false durable consequence? | yes | yes |
| Can reconciliation recover a complete committed no-effect set without falsely calling its database commit a rollback? | yes; preserve its original binding and recorded consequence | yes |
| Are protected-effect, first-admission, and separate failure-evidence transaction roles explicitly identified and independently verified when distinct? | yes; uncertainty about an evidence commit blocks replacement admission | yes |
| Is a partial success set quarantined without automatic synthesis, deletion, compensation, or replay? | yes | yes |
| Does consumption become durable only with the successful atomic effect? | yes | yes |
| Are one operation/one success/one consumption/one result-byte-sequence uniqueness rules mandatory? | yes | yes |
| Is receipt lookup subject to current authentication, authorization, minimization, and redaction? | yes | yes |
| Can historical completion remain true while current response disclosure is withheld? | yes | yes |
| Does retention preserve retry/reconciliation evidence and an irreversible tuple-binding tombstone where bulky bytes may be removed? | yes | yes |
| Is the first result exactly one pending-review operation-claim AssertionRecord under PR #23? | yes | yes |
| Does the transaction preserve reporter/performer separation and leave performer authority unevaluated? | yes | yes |
| Does it create no accepted execution, review, current state, prior-record mutation, event-family derivation, or implicit companion effect? | yes | yes |
| Does this candidate add no schema, accepted law, currentness, runtime, database, readiness, or OFARM2 change? | yes | yes |
| Must required non-default profiles, prerequisites, and exact schema/manifest bindings be materialized and reviewed before accepted-law promotion? | yes; semantic approval alone accepts no law | yes |

Any requested change to authorization, human-finalization semantics, AssertionRecord mappings, Event Grammar, disclosure, retention/custody, database authority, repair authority, or runtime implementation must remain in a separate trust-boundary PR.

---

## 20. Non-goals and explicit stop conditions

This candidate does not create:

- a generic workflow or transaction engine;
- a reservation or long-lived lock;
- a portable authorization decision cache;
- a new authorization registry or evaluator;
- a new domain truth store;
- a governed-read or external-dispatch protocol;
- a new Event Grammar family or commit class;
- public `RuntimeProblem` codes;
- retention, encryption, deletion, or key-custody policy;
- database roles, tables, recovery procedures, administrative repair, or break-glass authority;
- accepted RFC or active-baseline text;
- machine schemas, runtime code, conformance results, or current/default promotion; or
- a production-readiness claim.

Outcome reconciliation belongs to this semantic boundary. Executing database repair does not. If reconciliation finds a partial-set breach, work stops at quarantine and separately governed repair ownership.

Stop and split before changing a dependency's semantics, introducing a missing domain/evidence/time-trust rule, materializing schemas in this candidate PR, modifying active/current files, or implementing OFARM2 behavior before canonical promotion and extraction.

---

## 21. Staged delivery and currentness

The required sequence is:

1. **Phase A transaction candidate:** review and approve or amend this one non-authoritative issue #25 file.
2. **Exact-head semantic approval:** record source-verified review and explicit approval of the candidate's exact head; candidate approval changes no active law.
3. **Non-default transaction/evidence materialization:** separately create exact content-addressed operation-binding, caller-projection, mode-evidence, attempt, reconciliation, consumption, and receipt profiles. Stop for a separate packaging decision if `AuthorizationFinalizationEvidence v0.2` cannot represent the distinct truth claims. This creates no accepted law or current/default selection.
4. **Domain/shared-evidence prerequisites:** separately materialize the approved PR #23 AssertionRecord result/body schemas, assertion-act evidence, protected-effect contract, trace envelope, and exact bundle bindings. Complete the other applicable prerequisites and separately owned draft profiles required by PR #11 section 24 before accepted-law work.
5. **Non-default authorization policy-bundle binding:** bind the exact materialized issue #25 transaction profile and PR #23 protected-effect contract into the affected complete action rule and immutable manifest without duplicating their semantics. The referenced bytes and digests must actually exist; they are not yet promoted by this step.
6. **Exact binding review, then accepted semantic promotion:** stewards review the required schema/profile/manifest bytes and their content-addressed bindings before a separate governed PR performs the applicable accepted-law promotion under PR #11 section 24. Pin the reviewed digests. Any semantic change returns to exact-head semantic review and approval. The eventual accepted-law transaction prerequisite for applicable `NOT_REQUIRED` rows must name issue #25 alongside issue #19; do not edit the historical approved PR #11 candidate in this Phase A PR.
7. **Hostile conformance:** exercise section 16 through production-reachable lookup, trusted enrichment, authorization, gate, persistence, receipt, and reconciliation paths, and record actual evidence.
8. **Explicit current/default promotion:** change currentness only through a separate steward-approved step after contract and conformance review.
9. **OFARM2 extraction:** copy only promoted canonical assets, verify exact bytes and digests, and retain source provenance.
10. **Separately reviewable runtime work:** keep UnitOfWork, command idempotency, authorization evaluation, protected-effect application, disclosure, retention/custody, and database authority in their respective trust-boundary PRs.

No step is implied by completion of the prior step. This candidate remains historical Phase A material until separately accepted.

---

## 22. Phase A completion criteria

Phase A is complete when:

- every issue #25 requirement has a proposed closed disposition;
- the exact PR #11, #20, and #23 heads remain unchanged and semantically approved;
- the key grammar, tuple, caller projection, operation binding, digest construction, result binding, durable admission point, concurrent winner, and rollback-survival rules are reviewed;
- the first-admitted online assertion timestamp remains the runtime-observed pre-validation value rather than a commit time;
- the transaction sequence, current re-evaluation, complete guards, success membership, verified receipt, and single-use uniqueness are reviewed;
- the acyclic digest construction, identifier-only receipt links and self-membership, and append-only reconciliation references are reviewed;
- the exact outcome/consequence separation and deterministic success/partial/unresolved/no-effect precedence are reviewed;
- recovery covers committed no-effect sets and separately identified protected-effect, first-admission, and failure-evidence commits without conflating commit status with protected-effect outcome;
- the mode-change terminal rule cannot bypass unresolved evidence;
- every required failure class and failure-evidence persistence failure has one truthful posture;
- evidence ownership and shared-package posture are explicit;
- the operation-claim handoff is exact and creates only one pending-review assertion;
- non-default materialization and exact binding review precede accepted-law promotion under section 21 and PR #11 section 24;
- no semantic choice required by this boundary is left to schema or runtime authors;
- every unresolved cross-boundary need is named as a blocker rather than silently filled; and
- the PR still changes only this non-authoritative candidate file.

Repository validation and green CI can establish structural consistency only. They do not provide steward semantic approval, accepted law, executable contracts, conformance evidence, current/default promotion, or runtime authorization.
