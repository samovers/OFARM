# Spec Part 1A: Hybrid Per-Item Resolution + Prompt Registry (Backend)

Version: 0.1 (draft)  
Date: 2026-03-03  
Applies to: Farm_RM backend (`/v1/ai/ocr/parse`)  
Primary use-case: SI compulsory inventory-derived sections (A.6 input purchases, A.7 seed/seedling purchases)

This document defines how Farm_RM turns a captured document (receipt/invoice/label) into a **proposal** response using:

1. Deterministic candidate generation, and
2. LLM calls that resolve **exactly one inventory item per call** (hybrid per-item pipeline),
3. A prompt registry that is jurisdiction- and tenant-aware.

This is an implementation-level spec. The public API contract remains in Part 1 (`part-1-ocr-parse-contract.md`).

Current runtime note:

- session-based orchestration now lives under `/v1/intake/*` and is documented in [part-7-universal-capture-intake-contract.md](/Users/einstein/Documents/Codex/Semantic%20farming/docs/implementation/ai-capture-assist/part-7-universal-capture-intake-contract.md);
- this Part 1A remains the parse-side hybrid item-resolution spec used by those flows.

## 0. Invariants (Normative)

1. **AI proposes; Farm_RM enforces truth**: `/v1/ai/ocr/parse` does not create or mutate Farm_RM business-truth records. Persisted document or parse provenance is allowed only when the contract explicitly documents it.
2. **No URI minting**: neither the LLM nor the parse endpoint invents Farm_RM URIs.
3. **Never return \"0 items\" when deterministic candidates exist**:
   - If LLM calls fail, fall back to deterministic item extraction.
4. **Receipt/vendor authority rule**:
   - Vendor is derived only from receipt/invoice seller context, never from manufacturer text on labels.
5. **Privacy by default**:
   - No raw OCR text or images in logs.
   - No long-term image retention unless explicitly enabled (Part 6).

## 1. Inputs and Outputs (Normative)

### 1.1 Inputs

Farm_RM receives:

- `ocrText` (required): full OCR output text.
- `ocrLines[]` (optional): structured lines.
- `image` (optional): base64 image bytes; when present, the pipeline is **image-first**.
- `context.jurisdiction` (optional): drives prompt selection and SI-specific extraction priorities.

### 1.2 Output

Farm_RM returns an `OcrParseResponse` (Part 1) with:

- receipt header proposals (vendor, date, receiptRef, currency) when applicable
- `items[]` containing proposed line items / lots
- `referenceHints` suitable for iOS to resolve crop/variety through reference endpoints (Part 3)

## 2. Prompt Registry (Normative)

### 2.1 Repository Layout

Prompts are stored in-repo so they can be reviewed, versioned, and deployed with the backend.

Normative path:

- `/Users/einstein/Documents/Codex/Semantic farming/specs/api/v1/server/fastapi/app/prompts/ai_ocr/`

Each prompt file is a JSON object representing a provider request template with placeholders.

### 2.2 Prompt IDs and Selection

The parser selects prompts in this order:

1. Tenant/profile override (optional):
   - keyed by `(X-Farm-URI, X-Farman-Profile)` when provided
2. Jurisdiction default:
   - keyed by `context.jurisdiction` (e.g., `SI`)
3. Global default:
   - for unknown jurisdiction

If no prompt is available, the pipeline MUST still produce deterministic results (no failure solely due to prompt absence).

### 2.3 Required Prompt Templates (v1)

1. **Per-item resolver** (one call resolves exactly one agronomic inventory item):
   - File: `inventory-item-ai-prompt-v5-farmrm-attributes.template.json`
   - Source baseline: `/Users/einstein/Downloads/inventory-item-ai-prompt-v4-product-name.json` (adapted to Farm_RM-native attributes)
   - Output schema: `FarmRmInventoryItemAiResult` (included in the template's `response_format.json_schema`)

2. **Receipt/invoice header extractor** (one call resolves header fields only):
   - File: `receipt-header-ai-prompt-v1.template.json`
   - Output schema: `ReceiptHeaderAiResult` (defined below)

### 2.4 Placeholder Rendering (Normative)

Prompt templates MAY contain placeholders in message content strings.

Required placeholders:

- `{ocrRawText}`: the input text for the current resolution call.
- `{allowedCropValues}`: JSON string of allowed crop values (optional but recommended).

Rendering rules:

1. Placeholders are replaced by Farm_RM before sending the provider request.
2. `{ocrRawText}` MUST be bounded:
   - max 8,000 characters per call (hard cap)
   - prefer candidate block text over full document text
3. `{allowedCropValues}` MUST be bounded:
   - max 200 items (hard cap)
   - represent the caller's jurisdiction and installed reference snapshot
4. Placeholders MUST be rendered without breaking JSON encoding.

## 3. Reference-Aware Context (Using Crop/Variety DB) (Normative)

Farm_RM uses the local reference snapshot (Part 3) to improve:

1. LLM extraction (allowed values context), and
2. Deterministic normalization after LLM extraction.

### 3.1 Allowed Crop Values (Normative)

When `context.jurisdiction` is known and reference search is enabled, Farm_RM SHOULD provide `{allowedCropValues}` as:

```json
[
  {"uri":"https://data.farmco.si/farm-rm/v1/crop-species/EU/ZEAMA","label":"Koruza","code":"ZEAMA","synonyms":["maize","corn"]},
  {"uri":"https://data.farmco.si/farm-rm/v1/crop-species/EU/TRZAW","label":"Psenica","code":"TRZAW","synonyms":["wheat"] }
]
```

Rules:

1. Prefer Slovenian labels (`sl-SI`) when available; fallback to English label otherwise.
2. If Farm_RM cannot determine a jurisdiction-specific list, provide an empty array (`[]`) rather than guessing.

### 3.2 Deterministic Normalization (Normative)

After LLM extraction, Farm_RM MUST:

1. Generate `referenceHints.cropTokens[]` from extracted crop strings and OCR tokens.
2. Generate `referenceHints.varietyTokens[]` from extracted variety strings and OCR tokens.
3. Provide `referenceHints.suggestedQueries[]` so iOS can call:
   - `GET /v1/reference/crops/search?q=...`
   - `GET /v1/reference/varieties/search?q=...&cropUri=...` (when crop known)

Note: In v1, the parse response is not required to return resolved `cropUri`/`varietyUri` proposals, but it MAY in later revisions.

## 4. Hybrid Pipeline (Normative)

### 4.1 High-Level Algorithm

1. Prepare lines and deterministic `signals[]` (existing logic).
2. Determine an initial document type guess:
   - based on deterministic signals and `documentHint`
3. Generate deterministic candidates:
   - receipt/invoice: line item candidates
   - label: product identity + lot/expiry candidates
4. Run LLM calls (when enabled and keys available):
   - header call (receipt/invoice): `receipt-header-ai-prompt-v1`
   - per-item calls: `inventory-item-ai-prompt-v5-farmrm-attributes`
5. Assemble `OcrParseResponse`:
   - merge deterministic receipt fields when LLM is missing fields
   - map per-item results into `items[]`
6. If any LLM call fails:
   - continue with other calls
   - ensure deterministic fallback items are present when candidates exist

### 4.2 Deterministic Candidate Generation (Normative)

Receipt/invoice candidates:

1. Remove obvious noise lines (totals, VAT summary, signatures).
2. Identify potential item lines by patterns:
   - product descriptor tokens
   - quantity/unit patterns
   - price-like patterns
3. Merge wrapped lines:
   - merge only when the second line has no quantity/price and looks like a continuation
4. Cap candidates at **20**.

Label candidates:

1. Prefer blocks containing:
   - lot/batch keywords
   - expiry date patterns
   - net content / pack-size patterns
2. Build 1-3 candidate blocks, then resolve exactly one item.

### 4.3 LLM Calls (Normative)

#### 4.3.1 Header Extraction Call

This call produces proposals for:

- vendor name
- purchase date
- receipt/invoice number (`receiptRef`)
- currency (optional)

The input MUST include:

- `ocrRawText`: full OCR text (bounded)
- optional image content when provided in request
- jurisdiction hint when present

`ReceiptHeaderAiResult` schema (normative):

```json
{
  "status": "OK",
  "documentType": "receipt",
  "confidence": 0.0,
  "vendorName": null,
  "purchaseDate": null,
  "receiptRef": null,
  "currency": null,
  "decisionTrace": ""
}
```

Rules:

1. `purchaseDate` MUST be ISO date (`YYYY-MM-DD`) when present.
2. `documentType` MUST be one of: `receipt|invoice|label|mixed|unknown`.

Mapping to Farm_RM response:

- `invoice` maps to `receipt` for `OcrParseResponse.documentType`.

#### 4.3.2 Per-Item Resolver Calls

For each candidate (or for the whole label capture), Farm_RM calls the per-item resolver using:

- template: `inventory-item-ai-prompt-v5-farmrm-attributes.template.json`
- `{ocrRawText}`: candidate text block
- `{allowedCropValues}`: reference-aware crop list (when available)
- optional image when provided (image-first)

The resolver returns `FarmRmInventoryItemAiResult`:

- `vendorName` (receipt/invoice only)
- `resourceLabel`
- `cropLabel` (seed items primarily)
- `variety` (seed items primarily)
- `measure`
- `lotLabel`
- `expirationDate`
- quantity fields (package count/base quantity)
- `documentType`, `resolvedProductClass`, `overallConfidenceScore`, `decisionTrace`

### 4.4 Mapping Per-Item Output -> `OcrParseItem` (Normative)

For each resolved item:

1. `itemType`:
   - receipt/invoice candidates: `receipt_line_item`
   - label candidates: `label_lot`
2. `categoryHint`:
   - prefer direct model value from `categoryHint`
   - if missing, map `resolvedProductClass` into one of:
     - `seed`
     - `cropprotection`
     - `amendment`
     - `other`
3. Proposals (minimum expected keys when available):
   - `productLabel` <- `resourceLabel`
   - `cropLabel` <- `cropLabel` (seed items)
   - `variety` <- `variety` (seed items)
   - `lotCode` <- `lotLabel`
   - `expirationDate` <- `expirationDate` (ISO date if possible)
   - `quantity` / `packQuantity`:
     - prefer `quantityValue` + `quantityUnit`
     - fallback to `totalBaseQuantityDetected` + `baseUnitDetected`
     - label flow prefers `packQuantity`
     - receipt flow prefers `quantity`
4. Warnings:
   - include a warning when `multipleItemsDetected=true`
   - include a warning when `overallConfidenceScore < 0.55`
5. Provenance:
   - In v1, per-item prompts may not return line indices; proposals SHOULD include `notes` and lower confidence when provenance is missing.

Seed status code (E/P/K):

- The per-item resolver prompt does not currently produce an SI seed status code.
- Farm_RM MAY propose `statusCode` only when the document contains unambiguous cues; otherwise leave it unset and require manual selection in iOS.

## 5. Error Handling (Normative)

1. LLM unavailability MUST NOT cause HTTP 500 for `/v1/ai/ocr/parse`.
2. If all LLM calls fail, return deterministic extraction with:
   - `model.provider="farm-rm"`
   - `persistenceTargets` based on deterministic document type
3. If some items resolve and others fail:
   - include the resolved items
   - include deterministic items for unresolved candidates only if that avoids returning empty results

## 6. Acceptance Criteria (Testable)

1. Given a receipt with multiple line items, the response contains `items[].itemType="receipt_line_item"` entries and does not return an empty items array.
2. Given a seed label, the response proposes `lotCode` and `packQuantity` when present on the label.
3. When a reference snapshot is installed, the response includes `referenceHints.suggestedQueries` for crop/variety lookup.
4. If OpenAI is disabled/unavailable, deterministic extraction still returns non-empty items when candidates exist.
5. No response contains invented URIs (no `urn:*`/`https://data...` created by parsing).

## 7. Dependencies

- Part 1: OCR parse contract (`/v1/ai/ocr/parse` request/response).
- Part 3: reference search endpoints and snapshot ingestion.
- Part 6: privacy defaults for images and OCR text.
