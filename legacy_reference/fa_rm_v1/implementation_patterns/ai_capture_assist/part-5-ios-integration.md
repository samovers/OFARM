# Spec Part 5: Farman Lite iOS Integration (Flows, Offline Queue, UX Rules)

Version: 0.1 (draft)  
Date: 2026-03-01  
Applies to: Farman Lite iOS client behavior

## 0. Scope

Define how Farman Lite iOS integrates with:

1. `POST /v1/ai/ocr/parse` (Part 1) for predictable OCR structuring.
2. Inventory persistence endpoints (Part 2) for receipts and label-derived lots.
3. Reference endpoints (Part 3) for crop/species + variety selection.
4. Season windows endpoint (Part 4) for operation suggestion priors.

This part is written as a product+engineering contract: flows, offline behavior, and UX rules.

Current backend note:

- where session-based orchestration is available, `/v1/intake/*` is the canonical backend seam for universal scanner flows;
- direct `POST /v1/ai/ocr/parse` plus route-specific writes remain lower-level building blocks.

## 1. Goals / Non-goals

### 1.1 Goals

1. Keep OCR capture **offline-first** and safe.
2. Reduce user review effort by using AI proposals with explainable provenance.
3. Avoid “random autofill” by gating auto-application on confidence + provenance.
4. Enable a new “label scan” flow that creates/links lots.
5. Improve operation suggestions using cached season windows.

### 1.2 Non-goals (v1)

1. Long-term retention of raw receipt/label images on the backend (proposal-only parse may accept images; retention is a separate opt-in).
2. Auto-linking receipts to labels without confirmation.
3. Forcing reference matches when unclear (“Unknown” must be allowed).

## 2. UX Principles (Normative)

1. **Trust before speed**:
   - never auto-apply low-confidence fields;
   - always show “why” a value was suggested.
2. **One-screen clarity**:
   - show proposed fields, required fields, and missing fields clearly.
3. **No internal jargon**:
   - do not expose URIs or table names in normal UI.
   - provide a “Technical details” debug view for internal identifiers.

## 3. Local Draft Models (Normative)

iOS maintains drafts locally; they are the “candidate layer”.

### 3.1 ReceiptDraft

Minimum fields:

- `draftId` (UUID)
- `capturedAt` (timestamp)
- `photoRef` (local file reference)
- `ocrText` (string)
- `ocrLines[]` (optional)
- `parseStatus` (enum): `pending|parsed|failed|skipped`
- `parseResult` (optional): last successful parse response (Part 1)
- `userEdits` (structured): the confirmed/edited receipt import payload
- `syncStatus` (enum): `not_synced|queued|synced|failed`
- `farmUri`, `jurisdiction`, `locale`

### 3.2 LabelDraft

Minimum fields:

- `draftId` (UUID)
- `capturedAt`
- `photoRef`
- `ocrText`, `ocrLines[]`
- `parseStatus`, `parseResult`
- `userEdits` (structured): confirmed/edited lot payload (Part 2)
- `linkedReceiptDraftId` (optional)
- `syncStatus`
- `farmUri`, `jurisdiction`, `locale`

## 4. Flows (Normative)

### 4.1 Scan Receipt (Updated Flow)

1. Capture photo.
2. Run on-device OCR (Vision) → `ocrText` (+ `ocrLines[]` if available).
3. Create `ReceiptDraft(parseStatus=pending)`.
4. If online and backend supports parse endpoint:
   - call `POST /v1/ai/ocr/parse` (include `image` when available).
   - store `parseResult`, set `parseStatus=parsed`.
5. If offline:
   - enqueue `OCRParseJob(draftId, documentHint=receipt)`.
6. Render “Receipt review” screen:
   - show proposed values and line items.
   - apply auto-fill only when confidence+provenance meet thresholds (see 6).
7. On Save:
   - build a confirmed payload for `POST /v1/inventory/receipts/import`.
   - attempt sync immediately if online; else enqueue `SyncJob`.

### 4.2 Scan Label (New Flow)

1. Capture photo of label/bag.
2. On-device OCR → `ocrText` (+ `ocrLines[]`).
3. Create `LabelDraft(parseStatus=pending)`.
4. Online:
   - call parse endpoint with `documentHint=label` (include `image` when available).
5. Offline:
   - enqueue `OCRParseJob(draftId, documentHint=label)`.
6. Render “Label review” screen:
   - product label
   - lot/batch
   - pack quantity
   - optional crop/species + variety selection (Part 3)
7. On Save:
   - call `POST /v1/inventory/material-lots` (and/or create resource first if needed).
   - store returned `materialLotUri`/`seedLotUri` in draft for later linking.

### 4.3 Link Receipt ↔ Label (Manual-first)

User-visible behavior:

- In receipt review: “Attach label” → pick from recent label drafts.
- In label review: “Attach receipt” → pick from recent receipt drafts.

Best-effort suggestion (optional):

- Suggest candidate links based on:
  - capture time proximity,
  - token overlap in product label,
  - compatible quantities.

Rule (hard):

- Never auto-link without user confirmation.

## 5. Crop/Variety Selection UX (Normative)

When label/receipt indicates seed/plant material:

1. iOS calls `GET /v1/reference/crops/search?q=…`
2. User selects crop/species or “Unknown”.
3. If crop selected, iOS calls `GET /v1/reference/varieties/search?q=…&cropUri=…`
4. User selects variety or “Unknown”.

UI requirements:

- show top 3–10 candidates with:
  - name (preferred language),
  - optional synonyms,
  - optional source attribution hint (“EU catalog”, etc.).

## 6. Confidence + Provenance UX Rules (Normative)

iOS should interpret parse response proposals with two controls:

1. A numeric threshold (config):
   - `AUTO_APPLY_HIGH >= 0.85`
   - `SUGGEST_MEDIUM >= 0.55`
2. A provenance requirement:
   - if no provenance, do not auto-apply regardless of confidence.

Behavior:

- High confidence + provenance:
  - auto-fill field, show subtle “detected” badge.
- Medium confidence or weak provenance:
  - show as tappable suggestion chip.
- Low confidence:
  - show nothing or show under “Suggestions” collapsed section.

Required fields:

- If a required field is missing, UI must guide the user to fill it before sync.

## 7. Offline Queue (Normative)

### 7.1 Job Types

- `OCRParseJob`
  - fields: `jobId`, `draftId`, `documentHint`, `attempt`, `nextRunAt`, `lastError`
- `SyncJob`
  - fields: `jobId`, `draftId`, `entityKind` (`receipt|material_lot`), `attempt`, `nextRunAt`, `lastError`

### 7.2 Retry and Backoff

Rules:

1. Exponential backoff with jitter.
2. Maximum delay: 1 hour.
3. Stop retrying after 24 hours unless the user taps “Retry now”.

Ordering:

1. Run queued parse jobs first.
2. Then run sync jobs.

### 7.3 Error Classification

- Network unreachable: retry.
- `429`: retry with server-provided `Retry-After` when present.
- `422` validation errors: do not retry automatically; surface actionable missing/invalid fields.
- `503` AI unavailable: retry parse later; allow manual editing meanwhile.

## 8. Season Windows Caching and Operation Suggestion (Normative)

iOS uses season windows to improve operation suggestions without requiring online inference.

Rules:

1. When online and a crop is known for a field-season:
   - fetch `GET /v1/agronomy/season-windows?cropUri=…&lat=…&lon=…`
   - cache response keyed by `(cropUri, regionId, datasetVersion)`.
2. When offline:
   - use cached windows as priors.
3. Ranking is computed on-device:
   - window overlap boosts plausible operations (planting/harvest).
   - out-of-window down-ranks but does not hard-block.

UI:

- show short reasons:
  - “In planting window for maize in this region”
  - “Recent seed lot purchase suggests planting”

## 9. Acceptance Criteria (Testable)

1. Receipt scan works offline; parse+sync replay correctly later.
2. Label scan persists a material lot and shows lot/batch provenance.
3. Low-confidence values are not silently applied.
4. Crop/variety selection uses Farm_RM reference endpoints and supports “Unknown”.
5. Operation suggestions change when season windows are in/out of range (with cached priors).

## 10. Dependencies

- Parts 1–4 implemented in backend (or feature-flagged).
- iOS must have a capability discovery mechanism and fallbacks if endpoints are missing.

## 11. Next Part

Part 6: Security, privacy, QA, rollout: [part-6-security-privacy-qa-rollout.md](/Users/einstein/Documents/Codex/Semantic%20farming/docs/implementation/ai-capture-assist/part-6-security-privacy-qa-rollout.md)
