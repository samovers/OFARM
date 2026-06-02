
# OFARM Runtime Event Ingress and Idempotency Fixtures v0.1

Date: 2026-04-18
Status: active supporting implementation artifact
Scope: bounded executable conformance proof for semantic event ingress, replay-safe idempotency, and promotion tracing after the event-boundary closure RFC

---

## 1. Purpose

This fixture set closes the next hostile-implementer seam around event ingress:
- semantic event versus transport separation is explicit
- replay-safe idempotency is expressed as a governed result rather than hidden queue logic
- promotion trace is a machine-contract family, not just support telemetry

It is intended to strengthen the package without changing:
- `00_active_baseline/`
- `01_companion_artifacts/`

---

## 2. Authority basis used

This wave is grounded in already-active law plus the new accepted event-boundary closure artifact:
- `00_active_baseline/OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md`
  - event law
  - commit/promotion law
  - fixed event families
- `00_active_baseline/OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md`
  - ingress normalization gate
  - offline sync discipline
  - event envelope versus semantic event distinction
  - retry-safe and idempotent asynchronous behavior
- `01_companion_artifacts/OFARM_Event_Grammar_and_Commit_Matrix_v0_1.md`
  - one-primary-family rule
  - commit classes
  - promotion safety matrix
- `02_accepted_rfcs/OFARM_Event_Ingress_and_Promotion_Boundary_Closure_RFC_v0_1.md`

---

## 3. Executable fixture families

### 3.1 Promoted operation-claim ingress
The runner must prove that a typed `OPERATION_CLAIM` ingress path can:
- bind to one semantic event envelope
- preserve event time versus record time versus ingest time
- emit source-truth records in order
- produce an accepted executed intervention consequence only after review

### 3.2 Replay-safe reuse
The runner must prove that a second request carrying the same idempotency key and canonical payload digest can:
- reuse the prior result deterministically
- avoid duplicate source-truth emission
- still return a governed machine-readable result and promotion trace

### 3.3 Trace consistency
The runner must prove that request, result, trace, assertion, review decision, and accepted consequence stay cross-linked and scope-consistent.

---

## 4. Included bounded scenarios

- promoted pruning operation claim captured offline and replayed to the online-authoritative core
- replay of the same pruning draft after the first request already succeeded

---

## 5. Non-goals

This fixture wave does not yet attempt to close:
- transport-protocol-specific contracts
- every event family and every commit class under the new ingress contracts
- live deployment telemetry or bridge promotion
- broad partner-surface version/deprecation closure
