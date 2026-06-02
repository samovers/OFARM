# OFARM live POC first-slice status addendum v0.1

Date: 2026-04-17  
Status: implementation/conformance addendum  
Scope: reconcile the currently strongest live POC-proven slice with the older reference-spike narrative without changing baseline law

---

## 1. Purpose

This addendum records the current strongest **live POC-proven first slice** observed across the external prototype backend and client used as OFARM proof-of-concept input:

- `Semantic farming`
- `Farman Lite`

This addendum is **not** a baseline-law change.
It does **not** amend:

- `00_active_baseline/`
- `01_companion_artifacts/`
- `02_accepted_rfcs/`
- `03_machine_contracts/`

It is an **implementation/conformance implication** inside `04_implementation_and_conformance/`.

Its job is narrower:

1. state which slice is currently strongest in live code
2. state what is and is not inside that slice boundary
3. explain how that live slice relates to the earlier spike design note

---

## 2. What this addendum affects

### 2.1 Affected OFARM artifact

This addendum affects the interpretation of:

- `04_implementation_and_conformance/service_and_sdk_candidates/reference_platform_and_sdk/OFARM_reference_implementation_spike_design_notes_v0_1.md`

### 2.2 What remains true

The spike note remains useful as a **design fixture**.
It still captures a valid target slice for exercising hard OFARM seams.

What changes here is only this:

- the spike note's chosen vertical slice is **not** the strongest slice currently proven by the live POC codebase
- the strongest live proof today is narrower and different

---

## 3. Confirmed live POC first slice

### 3.1 Confirmed slice

The strongest current live POC first slice is:

**`receipt.invoice` universal scanner intake commit**

### 3.2 Plain-language description

In the current live POC, the cleanest business-complete path is:

1. a farmer or field operator opens the mobile inventory intake surface
2. captures a receipt/invoice image or document
3. optionally runs document ingest and parse/OCR
4. sends the capture through backend intake analysis
5. receives the `receipt.invoice` route selection
6. reviews or corrects extracted payload fields
7. sends the session through backend review
8. commits the session through backend commit
9. receives a committed downstream receipt-import result
10. persists the confirmed receipt locally on device

This is the strongest currently evidenced end-to-end write path with a clear entrypoint, review boundary, commit boundary, and durable result.

---

## 4. Evidence basis

This conclusion is grounded in live-code inspection of the external POC repositories and their tests.

### 4.1 Semantic farming evidence

- `Semantic farming/specs/api/v1/server/fastapi/app/ocr_intake_routes.py`
- `Semantic farming/specs/api/v1/server/fastapi/app/intake_session_routes.py`
- `Semantic farming/specs/api/v1/server/fastapi/app/main.py`
- `Semantic farming/specs/api/v1/server/fastapi/tests/test_api.py`
- `Semantic farming/specs/api/v1/server/fastapi/tests/test_universal_capture_receipt_mixed_label_lot.py`

### 4.2 Farman Lite evidence

- `Farman Lite/apps/ios/FarmanLiteiOS/FarmanLiteiOS/Features/Inventory/InventoryView.swift`
- `Farman Lite/apps/ios/FarmanLiteiOS/FarmanLiteiOS/Core/Storage/DraftOperationStore.swift`
- `Farman Lite/apps/ios/FarmanLiteiOS/FarmanLiteiOS/Networking/FarmRMAPIClient.swift`

### 4.3 Inspected working state

Inspection was performed against the following external repo states:

- `Semantic farming` — branch `codex/explain-slovenian-phrase-use`, commit `a0a8479742711ab38abcf462627fb4814249a94c`, working tree dirty
- `Farman Lite` — branch `codex/add-slovenian-switcher`, commit `4670aa6a0a15d966128148240fab0bd8dd9d8585`, working tree dirty

This means the conclusion is strong enough for implementation/conformance narrative correction, but still tied to an inspected development state rather than a clean promoted build.

---

## 5. Exact slice boundary

### 5.1 In scope

The confirmed slice includes:

- mobile receipt/invoice capture from the inventory surface
- optional document ingest and parse/OCR
- backend intake analyze
- backend intake review
- backend intake commit
- route-specific downstream receipt import result
- local persistence of the confirmed receipt on the device

### 5.2 Backend surfaces inside the slice

- `/v1/documents/ingest`
- `/v1/documents/{documentUri}/parse`
- `/v1/intake/captures`
- `/v1/intake/analyze`
- `/v1/intake/sessions/{sessionId}/review`
- `/v1/intake/sessions/{sessionId}/commit`

### 5.3 Output of the slice

The confirmed slice produces, at minimum:

- `documentUri`
- `parseRunUri`
- `sessionId`
- review decisions / route-ready state
- committed downstream receipt-import result
- local confirmed `InventoryReceiptRecord`

---

## 6. Boundary clarifications from follow-up inspection

### 6.1 `operationDraftFollowUp` is outside the confirmed core slice

`operationDraftFollowUp` is an **optional downstream handoff**, not part of business completion for `receipt.invoice`.

It is primarily associated with the `seed_label_or_tag` route and may still remain in a `needs_context` or `ready_to_create` posture after a successful commit.

Therefore:

- the first slice does **not** require planting-follow-up completion
- the first slice ends cleanly at committed receipt intake plus local confirmed receipt persistence

### 6.2 Field-passport regeneration is not evidenced from this slice

The inspected live POC does **not** currently prove that `receipt.invoice` commit automatically invalidates or regenerates field-passport materialization.

Therefore the confirmed slice must **not** be described as:

- receipt intake plus fresh field-passport regeneration
- receipt intake proving current-state recompute

Those may exist later, but they are **not evidenced** in the current confirmed live slice.

### 6.3 Review is split by stage

The authoritative review/commit boundary is split like this:

- **mobile local state** — staging, retry, resume, pending edits, offline buffering
- **backend intake review** — authoritative readiness decision for commit
- **backend intake commit** — authoritative final write boundary for the slice

This means device-local editing is useful and real, but it is not the governing review decision for the committed result.

---

## 7. OFARM runtime interpretation

The confirmed live slice maps into OFARM most cleanly as follows.

### 7.1 Capture/input posture

The slice begins as evidence/document capture entering a governed runtime path.
It is not a current-state materialization entrypoint.

### 7.2 Enforcement boundary

The effective enforcement boundary in the live POC is the backend chain:

- analyze
- review
- commit

That is the closest live-POC analogue to the OFARM runtime enforcement chain.

### 7.3 Commit meaning

This commit is a real runtime commit.
It is **not yet proven** as:

- attestation/sign-off
- document-assembly approval
- publication action
- a high-governance OFARM output action

### 7.4 Current-state/materialization effect

No field-passport or other governed current-state materialization effect is currently evidenced from this confirmed slice.

### 7.5 Authority surface

The confirmed slice most closely resembles operator-run submission/reporting execution with human responsibility.
It does **not** yet prove govern/decide review or attest/sign actions inside the confirmed boundary.

---

## 8. Relationship to the earlier spike note

### 8.1 Earlier spike-note slice

`OFARM_reference_implementation_spike_design_notes_v0_1.md` centers this chosen vertical slice:

**Delegated service-provider execution on an orchard field under Slovenia + Organic + Orchard packs, followed by fresh field-passport regeneration.**

### 8.2 Current live-POC reality

The currently strongest code-proven live slice is different:

**mobile `receipt.invoice` intake through backend analyze/review/commit, ending in committed downstream receipt import plus local confirmed persistence**

### 8.3 Correct interpretation

The earlier spike-note slice should therefore be read as:

- a valid **target/reference spike slice**
- a useful design fixture for exercising hard OFARM seams
- **not** the strongest currently evidenced live POC slice

That is the central reconciliation recorded by this addendum.

---

## 9. Explicitly out of scope for the confirmed first slice

The following are outside the exact confirmed slice boundary:

- `seed_label_or_tag` planting follow-up
- field-passport regeneration or freshness recompute
- inventory remediation queue
- control-center operation review/attestation
- reporting/export surfaces
- voice-session and Gemma flows
- manual operation logging sync

These may remain important adjacent seams, but they are not part of the strongest currently proven first-slice claim.

---

## 10. Controlled cautions

### 10.1 Dirty working-tree caution

The inspected `Semantic farming` and `Farman Lite` working trees were reported as dirty during the Codex runs that produced this reconciliation.

This addendum is therefore a live-status correction, not a claim that the inspected POC state is a frozen release artifact.

### 10.2 Remaining unknown

The main unresolved question is whether `receipt.invoice` commit later feeds any governed current-state/materialization path.

As of this addendum, that effect is **not evidenced** and should not be claimed.

---

## 11. Consequence for next work

The safe next step is:

- keep the older spike note as a design-fixture artifact
- treat this addendum as the current live-POC status correction
- use `receipt.invoice` intake commit as the bounded first-slice reference when discussing current backend/client proof

Do **not** silently describe the live POC as already proving delegated service-provider execution plus fresh field-passport regeneration unless that path is later demonstrated directly and recorded in a superseding implementation artifact.

---

## 12. Change classification

- **Affected active area:** `04_implementation_and_conformance/`
- **Change class:** implementation/conformance implication
- **Risk if omitted:** continuing to talk about one first slice in OFARM support materials while the live prototype actually proves a different one
- **Reason for smallest patch:** this addendum reconciles narrative drift without reopening baseline law or rewriting the earlier spike note
