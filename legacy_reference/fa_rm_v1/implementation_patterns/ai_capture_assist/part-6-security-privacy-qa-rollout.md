# Spec Part 6: Security, Privacy, QA, Rollout

Version: 0.1 (draft)  
Date: 2026-03-01  
Applies to: Farm_RM backend + Farman Lite iOS + CI/QA

## 0. Scope

Define the non-functional contract for the feature:

- security and access control,
- privacy and retention,
- QA strategy and regression gates,
- rollout strategy (feature flags, capability discovery, fallback behavior).

## 1. Security (Normative)

### 1.1 Authentication and Tenancy

All endpoints in Parts 1–4 MUST require the standard Farm_RM auth model:

- `Authorization: Bearer …`
- `X-Farm-URI: …`

Tenancy rule:

- any persisted URIs returned or accepted must be validated within the farm scope where applicable.

### 1.2 Rate Limiting

AI parsing is cost-sensitive and abuse-sensitive.

Farm_RM MUST enforce rate limits on:

- `POST /v1/ai/ocr/parse`

Minimum behaviors:

- return `429` on exceeded quota
- include `Retry-After` when possible
- enforce tenancy scope isolation (farm-level buckets) and prune stale scope state

### 1.3 Input Validation

Before invoking any AI provider, the server MUST:

- enforce request size limits (Part 1),
- reject empty/garbage text,
- strip or reject obviously malicious payloads (e.g., binary blobs in JSON).

## 2. Privacy and Retention (Normative)

### 2.1 Data Classification

OCR text may contain:

- personal data (names, emails, phone numbers),
- commercial data (prices, suppliers),
- compliance-relevant identifiers (lot/batch).

### 2.2 Default Retention Rules

Baseline (v1):

1. Farm_RM MUST NOT persist raw OCR text by default.
2. Farm_RM MAY persist:
   - a hash of the OCR text (`sha256`) for idempotency/debug, and
   - the structured parse output (proposals) if required for replay within a short window.

If any raw text is retained (debug mode):

- default retention: **30 days**
- must be deletable by policy (scheduled purge)

### 2.3 Logging Rules

Server logs MUST NOT include:

- raw OCR text,
- full receipt contents,
- full label contents.

Allowed:

- request ids,
- hashes,
- error codes,
- timing/metrics.

### 2.4 Image Upload (Optional, Privacy-Strict)

`POST /v1/ai/ocr/parse` may accept an optional `image` payload to improve extraction quality.

Rules:

- Client SHOULD make image upload an explicit, user-visible choice (e.g., "Send image to improve detection").
- Server MUST NOT log image bytes or base64 strings.
- Server MUST NOT retain images by default.
- If image retention is enabled for debugging:
  - strict retention (default 7-30 days),
  - policy-driven purge,
  - never reuse images for model training unless explicitly agreed.

## 3. QA Strategy (Normative)

### 3.1 Golden Fixtures (Backend)

Create a curated fixture set (stored in repo):

- receipts (Slovenia + Serbia; minimum 10 each)
- labels (seed bags + crop protection; minimum 10 each)
- mixed/ambiguous cases (minimum 5)

Each fixture includes:

- `ocrText`
- optional `ocrLines`
- expected `documentType`
- expected presence/absence of key fields (lotCode, quantity, date)

Note: Field-level exactness should be asserted only where evidence is unambiguous; otherwise assert confidence/provenance behaviors.

Current implementation baseline:

- Fixture corpus file: `specs/api/v1/server/fastapi/examples/ai-ocr-golden-fixtures.json`
- Coverage:
  - receipts: 10 (SI + RS)
  - labels: 10 (SI + RS)
  - mixed/ambiguous: 5
- Regression test:
  - `test_ai_ocr_parse_golden_fixture_corpus_regression`
- Runtime metrics endpoint:
  - `GET /v1/ai/ocr/metrics` (aggregate counts + latency percentiles)

### 3.2 Determinism and Schema Conformance Tests

For `/v1/ai/ocr/parse`:

- response validates against strict schema
- persist-impact fields include provenance
- refusal path returns structured refusal response

For reference endpoints:

- stable ordering for same dataset
- multilingual label selection rules

For season windows:

- stable outputs for pinned dataset version
- correct wrap-year splitting in `dayOfYearRanges[]`

### 3.3 Integration Smoke (iOS + Backend)

Add an end-to-end smoke test that:

1. Creates a receipt draft fixture
2. Calls parse
3. Applies confirmed edits
4. Imports receipt
5. Creates a label draft fixture
6. Calls parse
7. Persists a material lot

Assertions:

- offline queue replay produces exactly one persisted record per draft (idempotency)
- validation failures are surfaced as actionable errors (no infinite retries)

## 4. Rollout (Normative)

### 4.1 Feature Flags

Backend feature flags:

- `AI_OCR_PARSE_ENABLED`
- `AI_OCR_METRICS_ENABLED`
- `REFERENCE_SEARCH_ENABLED`
- `REFERENCE_SNAPSHOT_CATALOG_ENABLED`
- `REFERENCE_SNAPSHOT_IMPORT_ENABLED`
- `SEASON_WINDOWS_ENABLED`

iOS must treat these as capability-based, not hard assumptions.

### 4.2 Capability Discovery (Recommended)

Define a lightweight endpoint:

- `GET /v1/capabilities`

Response example:

```json
{
  "apiVersion": "1.0.8",
  "features": {
    "aiOcrParse": {"enabled": true, "minClientVersion": "ios-0.9.0"},
    "aiOcrMetrics": {"enabled": true},
    "referenceSearch": {"enabled": true},
    "referenceSnapshotCatalog": {"enabled": true},
    "referenceSnapshotImport": {"enabled": true},
    "seasonWindows": {"enabled": false}
  }
}
```

iOS fallback behaviors:

- if `aiOcrParse` disabled: use existing on-device heuristic field filling; keep the same review UI.
- if `referenceSearch` disabled: allow free-text crop/variety entry but mark as “unverified”.
- if `seasonWindows` disabled: use time-of-year heuristics without region windows.

### 4.3 Rollout Gates (Recommended)

Before enabling by default:

1. Fixture corpus passes in CI.
2. Parse endpoint P95 latency below a target threshold (e.g., 2s for text-only).
3. Error rate below target (e.g., <1% 5xx).
4. Manual QA on a small set of real receipts/labels.

## 5. Acceptance Criteria (Testable)

1. No raw OCR text appears in logs.
2. Rate limits are enforced for parse endpoint.
3. Golden fixtures run in CI and prevent regressions.
4. iOS can operate fully offline and replay jobs without duplicates.
5. Capability discovery drives clean fallback behaviors.

## 6. Dependencies

- Parts 1–4 provide endpoints and deterministic contracts.
- Part 2 idempotency keys are implemented server-side to support offline retry.

## 7. Next Step (Outside This Spec Set)

After Parts 0–6 are approved, create an implementation plan:

1. Backend: add endpoints and fixtures first (contract + tests).
2. iOS: implement label scan UI + queue types, integrate parse, then integrate season windows.
