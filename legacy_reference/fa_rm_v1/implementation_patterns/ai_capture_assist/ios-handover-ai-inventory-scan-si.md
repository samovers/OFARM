# iOS Handover: AI Inventory Scan (Receipts/Invoices/Labels) for SI A.6/A.7

Version: 0.3 (handover)
Date: 2026-03-13
Applies to: Farman Lite iOS client
Scanner orchestration authority: [ios-handover-universal-scanner-phase-2.md](/Users/einstein/Documents/Codex/Semantic%20farming/docs/implementation/ai-capture-assist/ios-handover-universal-scanner-phase-2.md)
Route-specific dependencies: Farm_RM `POST /v1/ai/ocr/parse`, `POST /v1/inventory/receipts/import`, `POST /v1/inventory/material-lots`, reference search (Part 3)

This handover explains what iOS must capture, how to review it, and how to sync it so SI reporting sections A.6 (inputs) and A.7 (seed/seedlings) can be produced without manual re-entry.

Use [ios-handover-universal-scanner-phase-2.md](/Users/einstein/Documents/Codex/Semantic%20farming/docs/implementation/ai-capture-assist/ios-handover-universal-scanner-phase-2.md) as the current scanner-orchestration authority for document ingest, universal capture intake, offline resume, and route gating. This document is narrower: it defines the SI-specific review fields and payload expectations that the scanner flow must preserve.

This document avoids code-level detail; it is a product/contract handoff for the client team.

Organic seed-sourcing exception semantics are governed separately by [phase-1-22-detailed-spec-organic-seed-sourcing-exception-evidence.md](/Users/einstein/Documents/Codex/Semantic%20farming/docs/implementation/phase-1-22-detailed-spec-organic-seed-sourcing-exception-evidence.md). This handover defines only what the mobile review flow must preserve for later linkage.

Residual Phase 1 follow-up after backend implementation is tracked separately in [ios-handover-residual-phase-1-client-followup-2026-03-06.md](/Users/einstein/Documents/Codex/Semantic%20farming/docs/implementation/ai-capture-assist/ios-handover-residual-phase-1-client-followup-2026-03-06.md).

## 0. What Problem This Solves

When a farmer buys inputs, the recordbook requires:

- A.6 Input purchases: what was bought, how much, when, and which invoice/receipt it came from.
- A.7 Seed/seedling purchases: same, plus crop, variety, and seed status code (E/P/K).
- For seed lines that are not straightforward organic stock, the review flow may also need exception-review context that stays separate from the purchase fact.

The goal is to make the purchase record a byproduct of scanning a receipt/invoice (and optionally the product label), not a separate data-entry module.

Purchase facts and seed-exception review facts must remain separate but linkable.

## 1. Entry Point and Capture Intents

Keep a single "Scan" entry point that opens a review sheet.

Support two intents:

1. Receipt/Invoice (default)
   - Extract: vendor, purchase date, receipt/invoice number, and line items.
2. Product Label (dev toggle initially)
   - Extract: lot/batch number, expiration date, pack size, and seed identity hints (crop/variety).

## 2. Fields iOS Must Collect (User-Confirmable)

### 2.1 Receipt Header

Required for SI reporting:

- `receiptRef` (Receipt/Invoice number)

Recommended:

- `vendorName`
- `purchaseDate`
- invoice evidence link (photo attachment or invoice reference)

### 2.2 Receipt Line Items (A.6 vs A.7)

Each line item must have:

- `resourceLabel` (product name as bought)
- `categoryHint` (seed / cropProtection / amendment / other)
- `quantityValue` + `quantityUnit` (when present)
- `lotLabel` (when present)

Seed-only fields (visible only when `categoryHint == seed`):

- `cropLabel` (Kultura)
- `variety` (Sorta)
- `statusCode` picker: `E`, `P`, `K`
- `exceptionReviewNeeded`: `yes`, `no`, `unknown`
- `exceptionReasonCode`: `organic_seed_unavailable`, `organic_variety_unavailable`, `organic_planting_stock_unavailable`, `supplier_evidence_pending`, `other`
- `exceptionEvidenceRefs[]`: zero or more receipt, photo, supplier-statement, or note references kept on the draft review item
- `exceptionNote` (optional; use only when the governed reason field is insufficient)

Notes:

- `cropLabel` is SI-reporting-critical. Do not use `resourceLabel` as a substitute for crop.
- `statusCode` is allowed to be blank at capture time, but the reporting binder will warn if missing.
- Do not encode seed-exception reason into `statusCode` or into notes alone.
- If exception review may be needed and evidence is not yet complete, preserve `exceptionReviewNeeded = yes` or `unknown`; do not force a clean `no`.

## 3. Using Farm_RM AI Parse (Lower-Level Parse Dependency)

Under the current universal scanner flow, iOS typically registers the document first and then orchestrates review through `/v1/intake/*`. This section is only about the lower-level OCR parse call and the SI-specific proposal fields the review flow should preserve.

iOS should call `POST /v1/ai/ocr/parse` with:

- `ocrText` (required)
- `ocrLines[]` (recommended)
- `image` (recommended, base64 JPEG)
- `context.jurisdiction = "SI"`
- `documentHint` = `receipt` or `label` (best guess)

Rules:

1. Treat all returned values as suggestions only.
2. Apply auto-fill only for high-confidence proposals with provenance.
3. When AI returns no usable proposals, the user must still be able to complete the review manually.

## 4. Leveraging Crop/Variety Reference Data

For seed line items, iOS should help the user select crop and variety using reference search:

1. Search crops:
   - `GET /v1/reference/crops/search?q=<user text>`
2. Search varieties (when crop is known):
   - `GET /v1/reference/varieties/search?q=<user text>&cropUri=<selected crop uri>`

UI expectations:

- Show Slovenian labels when available; otherwise show English label.
- Always allow "Unknown" (manual free text) when no match is found.

## 5. Sync to Farm_RM (Truth Persistence Targets)

Under the universal scanner flow, iOS will usually reach these persistence targets through `POST /v1/intake/sessions/{sessionId}/commit`. Direct route-specific calls remain lower-level fallback behavior and must preserve the same field semantics.

After the user confirms the review sheet, iOS persists using:

1. Receipt import:
   - `POST /v1/inventory/receipts/import`
2. Optional label-driven lot capture (if label flow enabled):
   - `POST /v1/inventory/resources` (create/resolve input material)
   - `POST /v1/inventory/material-lots` (create/resolve material/seed lot)

Minimum persistence for SI A.6/A.7:

- `receiptRef` at the receipt level
- For each line item:
  - `resourceLabel`, `categoryHint`
  - Seed lines: `cropLabel`, `variety`, `statusCode`

Additional draft review state to preserve for seed lines when exception review is in play:

- `exceptionReviewNeeded`
- `exceptionReasonCode`
- `exceptionEvidenceRefs[]`
- `exceptionNote`

These fields are not the canonical exception record. They are the minimum review-state handoff needed so the purchase line can later link to a separate exception evidence record without re-entering the seed line from scratch.

## 6. Offline and Retry Expectations

If offline:

1. Save the draft locally (photo + OCR text + current edits).
2. Defer AI parse and sync until online.

Retry rules (high level):

- Do not duplicate persisted receipts under retry:
  - keep `receiptRef` stable for the same receipt
- If the backend returns validation errors, stop auto-retrying and show the user what to fix.

## 7. Acceptance Checklist (For iOS QA)

1. A seed receipt can be scanned, reviewed, and synced with:
   - purchaseDate, receiptRef, cropLabel, variety, quantity, statusCode (if known).
2. A non-seed input receipt can be scanned and synced for A.6 with:
   - purchaseDate, receiptRef, input type, quantity.
3. No dead ends:
   - user can always correct missing crop/variety/status fields before sync.
4. When reference search is available, crop/variety pickers use it and keep the UI bilingual-friendly (sl-SI preferred).
5. A seed line that may need exception review can be saved and synced without flattening exception-needed state, reason, or evidence refs into a generic note.

## 8. Relationship To Newer Scanner Handover

1. [ios-handover-universal-scanner-phase-2.md](/Users/einstein/Documents/Codex/Semantic%20farming/docs/implementation/ai-capture-assist/ios-handover-universal-scanner-phase-2.md) is the current scanner-orchestration handoff.
2. This document remains the SI-specific field and payload-detail appendix for receipt and label review.
3. If scanner-flow guidance here conflicts with the universal scanner handover or Part 7 intake contract, the newer scanner handover and runtime-backed intake contract win.
