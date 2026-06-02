# Spec Part 0: Fit, Invariants, Glossary (AI Capture Assist + Reference + Agronomy Knowledge)

Version: 0.2 (draft)
Date: 2026-03-13
Applies to: Farm_RM backend + Farman Lite iOS

## 0. Scope

This spec set adds four capabilities to the Farm_RM ecosystem, while keeping Farm_RM’s existing "truth model" stable:

1. **AI OCR Parse**: Turn OCR text into *proposed* structured objects with confidence + provenance.
2. **Reference Normalization**: Provide a stable crop/species + variety reference model and search/normalization endpoints.
3. **Agronomy Season Windows**: Provide deterministic “season windows” (planting/harvest timing priors) for location + crop.
4. **Universal Capture Intake**: Provide a session-based orchestration seam over document registry, OCR parse provenance, review, helpers, and route-specific commit adapters.

This Part 0 locks the conceptual contract and vocabulary so Parts 1-7 do not re-decide fundamentals.

## 1. Fit (Why This Belongs In Farm_RM)

Farming software breaks when “capture” and “meaning” are coupled to UI screens and vendor-specific heuristics. Farm_RM exists to be the semantic backbone for:

- compliance-ready records,
- cross-system interoperability (machines, sensors, invoices/receipts),
- planning vs execution comparisons,
- auditability (what was recorded, why, and from what evidence).

AI-assisted capture fits if we enforce strict boundaries:

- AI can *propose* structure, but cannot create truth by itself.
- Farm_RM remains the system that defines what a valid record is (schemas, constraints, jurisdiction packs).
- Session-based intake may persist document and parse provenance, but only explicit downstream commit routes create business truth records.
- Users confirm or correct before persistence.

## 2. Goals / Non-goals (Normative)

### 2.1 Goals

1. **Predictable capture**: outputs are typed, schema-valid, and explainable.
2. **Human review first**: iOS can safely present suggestions and ask for confirmation.
3. **No silent invention**: low-confidence or missing provenance leads to suggestions, not auto-fill.
4. **Stable reference**: crop/species and variety URIs do not change under the user.
5. **Deterministic knowledge**: season windows are versioned and produce stable outputs given the same version and inputs.
6. **Offline-first client**: capture/edit works without connectivity; parsing + sync are queued.

### 2.2 Non-goals (v1)

1. Fully automated compliance without user confirmation.
2. Replacing on-device OCR (Vision OCR stays on-device; backend consumes text).
3. Building a full agronomic simulator (e.g., APSIM/DSSAT).
4. Allowing AI to mint identifiers or create reference terms.
5. Requiring image upload; v1 must work with text-only, but may accept optional images to improve detection.

## 3. Terminology (Normative Glossary)

The terms below are used consistently across Parts 1-7.

### 3.1 Document and Parse

- **OCR Text**: the raw text extracted from an image (on-device). (Farm_RM does not perform OCR in this feature.)
- **OCR Lines**: optional structured OCR output as a list of lines with per-line confidence (if available from iOS).
- **Document Hint**: a weak client hint (`receipt|label|unknown`) to improve parsing; never authoritative.
- **Document Type**: Farm_RM classification produced by parsing (`receipt|label|mixed|unknown`).
- **Parse Item**: one extracted “thing” in the document (e.g., one line item on a receipt, or one labeled lot on a bag).
- **Field Proposal**: an extracted candidate value for a specific field with confidence + provenance.
- **Universal Capture Intake**: the session-based backend seam under `/v1/intake/*` that orchestrates document registry, OCR parse provenance, review, helpers, and route-specific commit adapters.
- **CaptureSession**: the current public session object returned by the universal capture intake API.

### 3.2 Candidate vs Confirmed

- **Candidate (proposed)**: data derived from AI parse that is not yet committed as truth.
- **Confirmed (persisted)**: data written into Farm_RM persistence primitives via explicit persistence endpoints after validation.

Rule: **Farm_RM persistence endpoints only accept confirmed records** (even if they were pre-filled by AI suggestions).

### 3.3 URI and Identity

- **URI**: canonical identifier used by Farm_RM for all persisted entities.
- **URI-first**: clients and services treat URIs as the primary key; labels are display-only.
- **No-URI-minting (AI)**: AI parse outputs must not invent new URIs.

Reference terms (crop/species, variety) must be selected from Farm_RM-managed references with stable URIs.

### 3.4 Provenance and Confidence

- **Provenance**: the evidence location(s) in OCR output that justify an extracted value.
  - Example: line index, or substring offsets in the OCR text.
- **Confidence**: a 0–1 score indicating the parser’s belief that the proposed field value is correct.
  - Confidence is used for UX decisions, not as a compliance guarantee.

### 3.5 Jurisdiction and Profiles

- **Jurisdiction**: program context for compliance rules/data packs (`SI`, `RS`, `EU`, etc.).
- **Production profile**: `organic_certified`, `in_conversion`, `conventional`.
  - Organic-first: where rules differ, **organic takes priority**, then in-conversion, then conventional.

## 4. Invariants (Hard Rules)

These invariants are non-negotiable and must be enforced by implementation and tests.

### 4.1 AI Boundaries (Hard)

1. `POST /v1/ai/ocr/parse` must be **proposal-only for business truth**:
   - no database writes that create or mutate Farm_RM truth records,
   - document and parse provenance persistence is allowed only when the contract explicitly documents it.
2. AI outputs must **never mint URIs** for:
   - inventory resources,
   - material lots,
   - crop/species,
   - varieties,
   - counterparties/parties,
   - any other persisted entities.
3. AI outputs must be **schema-valid JSON** (strict schema), or an explicit refusal.
4. AI outputs must include **confidence + provenance** for any proposed value that could become persisted without user re-typing.

### 4.2 Deterministic Validation (Hard)

After AI extraction, Farm_RM must run deterministic normalization + validation that:

1. rejects impossible values (e.g., negative quantities),
2. normalizes units and dates when possible,
3. ensures reference candidates are from known references (no free-text “variety URI”),
4. produces explicit, actionable validation messages.

### 4.3 Client Responsibilities (Hard)

1. iOS must treat AI output as **suggestions**.
2. iOS must not persist suggested records without user confirmation (unless an explicit future “auto-confirm mode” is introduced and gated).
3. iOS must work offline:
   - store drafts locally,
   - queue parse + sync jobs,
   - show understandable statuses.

## 5. Versioning Rules (Normative)

### 5.1 API and Dataset Versioning

1. Farm_RM API has a semantic version (e.g., `1.0.x`).
2. Reference datasets and agronomy windows must expose:
   - `datasetUri`
   - `datasetVersion`
   - `publishedAt`
   - `sourceAttribution[]`
3. Any deterministic API response must include enough metadata to reproduce:
   - either via explicit `datasetVersion` parameter, or via response including the version used.

### 5.2 Backward Compatibility Rule

Existing endpoints must remain supported:

- `POST /v1/inventory/receipts/import` remains valid for receipt ingestion.
- New endpoints must not force clients to upgrade all flows at once.

## 6. Privacy + Retention Baseline (Normative)

OCR text can contain personal data (names, phone numbers, emails), and purchase data.

Baseline:

1. Farm_RM should **not** store raw OCR text by default unless required for:
   - user-visible evidence retention, or
   - debugging with explicit opt-in.
2. If stored, raw OCR text must have a retention policy (default target: 30–90 days).
3. Logs must avoid emitting OCR text; log only hashes and structured error codes.

## 7. Acceptance Criteria (Part 0)

1. The system can be described with the rule: "AI proposes; Farm_RM enforces truth", and it is true across all endpoints in Parts 1-7.
2. No AI endpoint directly creates or mutates business truth records; document and parse provenance persistence is allowed only where explicitly documented.
3. All AI proposals include confidence + provenance for persisted-impact fields.
4. Reference and agronomy endpoints are versioned and deterministic.

## 8. Dependencies

- Existing persistence primitives and evidence model exist (Farm_RM schema).
- Auth model exists: bearer auth + `X-Farm-URI` tenancy header (Farm_RM API server).

## 9. Next Part

Part 1: OCR parse contract (`POST /v1/ai/ocr/parse`): [part-1-ocr-parse-contract.md](/Users/einstein/Documents/Codex/Semantic%20farming/docs/implementation/ai-capture-assist/part-1-ocr-parse-contract.md)
