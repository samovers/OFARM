# OFARM thin active-contract reference harness fixtures v0.1

Date: 2026-04-19
Status: active supporting implementation artifact
Scope: bounded end-to-end implementation proof using only active OFARM contracts through one narrow pruning-to-passport path

---

## 1. Purpose

This fixture lane closes the remaining package-internal implementation-proof criticism named in the post-hardening hostile review.

It proves that one realistic path can run end to end without hidden glue logic outside the active contract set:
- semantic event ingress is explicit
- assertion, review, and accepted consequence remain distinct
- current-state materialization is grounded in accepted records
- buyer-facing passport publication is governed by sharing and authorization
- the final output remains a live `PassportView`, not a silently frozen or attested document

This fixture lane does **not** change active law or promote any draft lane.

---

## 2. Authority basis used

This harness relies only on already-active substance and already-active machine contracts:
- `00_active_baseline/OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md`
- `00_active_baseline/OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md`
- `02_accepted_rfcs/OFARM_Source_Truth_Record_Closure_RFC_v0_1.md`
- `02_accepted_rfcs/OFARM_Current_State_Materialization_RFC_v0_1.md`
- `02_accepted_rfcs/OFARM_Event_Ingress_and_Promotion_Boundary_Closure_RFC_v0_1.md`
- `03_machine_contracts/` active contract families used in the lot-pruning chain

No draft-only contract family is required.
No reviewed-thread holding artifact is required.
No baseline rewrite is required.

---

## 3. Narrow path proved

### 3.1 Core path
`SemanticEventEnvelope`
→ `CommitIngressRequest`
→ `CommitIngressResult`
→ `AssertionRecord`
→ `ReviewDecision`
→ `AcceptedEventConsequence`
→ `MaterializationRequest`
→ `MaterializationResult`
→ `PassportViewMetadata`
→ `PublicationAssemblyRequest`
→ `PublicationAssemblyResult`

### 3.2 Supporting governance side path
The harness also proves the side conditions that keep the publication path governed rather than implicit:
- `PromotionTrace`
- `MaterializationBasis`
- `MaterializationSnapshot`
- `SharingGrant`
- `AuthorizationDecisionRequest`
- `AuthorizationDecisionResult`
- `AuthorizationDecisionTrace`

---

## 4. Included bounded scenario

The harness uses one existing package-local chain:
- contractor-reported pruning event on `field:17`
- governed review and accepted execution consequence
- fresh Compliance materialization for `lot:field-17:apples:2026-batch-1`
- explicit buyer sharing and read authorization
- governed live passport publication for the buyer

This is intentionally narrow.
It is meant to prove composability, not to be a fake full product implementation.

---

## 5. Checks performed

The runner must prove at least the following:
- every chain artifact validates against its active schema
- every chain artifact is under `03_machine_contracts/` and none is draft-only
- semantic-event identity propagates consistently through ingress, truth records, and accepted consequence
- time ordering remains monotonic from event occurrence through publication
- materialization basis, snapshot, request, and result stay cross-linked and grounded in accepted records
- sharing and authorization govern the final buyer-facing publication
- publication stays a live `PASSPORT_VIEW` and does not silently turn into a frozen or attested document
- no `BridgeCandidate` or other non-active handoff object is required anywhere in the path

---

## 6. Non-goals

This fixture lane does not prove:
- live deployment evidence
- same-standard bridge promotion readiness
- broad partner-output promotion
- transport-protocol completeness
- query-engine completeness
- external standard-readiness

Those remain separate evidence or promotion questions.
