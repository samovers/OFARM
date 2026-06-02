# Spec Part 1: OCR Parse Contract (Backend API)

Version: 0.10 (draft)
Date: 2026-03-13
Endpoint: `POST /v1/ai/ocr/parse`

## 0. Scope

Define a decision-complete API contract for turning OCR text into **proposed** structured objects suitable for:

- Receipt review (`receipt` document type)
- Label/lot review (`label` document type)
- Delivery-note / weigh-ticket review (`deliveryNote` payload, typically with `documentHint = weigh_ticket` or `unknown`)
- Soil lab review (`soilReport` payload, typically with `documentHint = soil_lab_report`)
- Fertilisation-plan review (`fertilisationPlan` payload, typically with `documentHint = unknown`)
- Seed authorization / derogation review (`seedSourcingException` payload, typically with `documentHint = certificate` or `unknown`)
- Fertiliser-label / product-composition review (`fertiliserProductComposition` payload, typically with `documentHint = fertiliser_label`)
- Mixed cases (`mixed`) and failure modes (`unknown`)

This endpoint is **proposal-only for business truth**. It does not persist Farm_RM truth records such as receipts, lots, soil results, fertilisation plans, delivery tickets, or seed-sourcing exceptions.

Current runtime note:

- when `documentUri` is supplied and persistence is enabled, runtime may persist a `document_parse_run` provenance record and return `parseRunUri`;
- session-based orchestration over this parse endpoint now lives under `/v1/intake/*` and is documented in [part-7-universal-capture-intake-contract.md](/Users/einstein/Documents/Codex/Semantic%20farming/docs/implementation/ai-capture-assist/part-7-universal-capture-intake-contract.md).

## 1. Goals / Non-goals

### 1.1 Goals

1. Return a single strict, typed JSON response that iOS can render without additional LLM parsing.
2. Include **confidence + provenance** for proposed values that impact persistence.
3. Provide deterministic “pre-parse signals” to support debugging and deterministic fallbacks.
4. Support text-first OCR input plus optional **image** input for multimodal parsing (image-first when provided).

### 1.2 Non-goals

1. Minting any URIs.
2. Directly writing Farm_RM business-truth persistence primitives.
3. Guaranteeing correctness; the user must confirm before persistence.

## 2. Request Contract (Normative)

### 2.1 HTTP

- Method: `POST`
- Path: `/v1/ai/ocr/parse`
- Auth: same as Farm_RM API
  - `Authorization: Bearer <token>`
  - `X-Farm-URI: <farmUri>`
- Content-Type: `application/json`

### 2.2 Body (Normative Shape)

```json
{
  "source": "ios",
  "locale": "sl-SI",
  "capturedAt": "2026-03-01T12:34:56Z",
  "documentHint": "unknown",
  "documentUri": "urn:document:demo-1",
  "idempotencyKey": "ios|demo-1|parse",
  "image": {
    "mimeType": "image/jpeg",
    "dataBase64": "…base64 JPEG bytes…",
    "widthPx": 3024,
    "heightPx": 4032
  },
  "ocrText": "…full OCR text…",
  "ocrLines": [
    {"text": "SEMENA KORUZE", "confidence": 0.96},
    {"text": "LOT: 53001", "confidence": 0.99},
    {"text": "250 g", "confidence": 0.98}
  ],
  "context": {
    "jurisdiction": "SI",
    "currencyHint": "EUR"
  }
}
```

#### Fields

- `source` (required, string): client identifier. v1 allowed: `ios`.
- `locale` (required, string): BCP-47 language tag. Used for date/number parsing and label selection.
- `capturedAt` (required, RFC3339 string): capture timestamp.
- `documentHint` (required, enum): `receipt|label|unknown`.
  - runtime-accepted hints also include `weigh_ticket|soil_lab_report|fertiliser_label|certificate`
- `documentUri` (optional, string): persisted document registry URI. When supplied and persistence is enabled, runtime may persist parse-run provenance against this document.
- `idempotencyKey` (optional, string): caller-supplied idempotency key for parse-run provenance persistence.
- `image` (optional, object): original capture image for multimodal parsing.
  - `mimeType` (required, string): `image/jpeg|image/png` (clients should prefer `image/jpeg`).
  - `dataBase64` (required, string): raw image bytes as base64 (no data-URI prefix).
  - `widthPx` (optional, int): image width in pixels (if known).
  - `heightPx` (optional, int): image height in pixels (if known).
- `ocrText` (required, string): full OCR text. Must be non-empty after trimming.
- `ocrLines` (optional, array): structured OCR lines. Recommended when available.
  - Each item:
    - `text` (required, string)
    - `confidence` (optional, number 0..1)
- `context` (optional, object): deterministic hints that do not change the meaning of text.
  - `jurisdiction` (optional, string): `SI|RS|EU|…` (used for vendor/date patterns, optional tax ID formats, etc.)
  - `currencyHint` (optional, string): ISO currency code (e.g., `EUR`, `RSD`)

### 2.3 Request Limits (Normative)

- `ocrText` max length: **20,000 chars** (hard limit). If exceeded: reject with HTTP 413.
- `ocrLines` max: **500 lines** (hard limit). If exceeded: reject with HTTP 413.
- `image.dataBase64` max decoded bytes: **4,000,000 bytes** (hard limit). If exceeded: reject with HTTP 413.

Rationale: keep parsing fast and predictable and reduce accidental PII ingestion.

## 3. Response Contract (Normative)

### 3.1 Top-level Shape

```json
{
  "status": "OK",
  "documentType": "label",
  "documentConfidence": 0.86,
  "documentUri": "urn:document:demo-1",
  "parseRunUri": "urn:parse-run:demo-1",
  "signals": [
    {"code": "HAS_LOT_KEYWORD", "evidence": {"lineIndex": 1}},
    {"code": "HAS_NET_WEIGHT", "evidence": {"lineIndex": 2}}
  ],
  "receipt": null,
  "deliveryNote": null,
  "soilReport": null,
  "fertilisationPlan": null,
  "seedSourcingException": null,
  "fertiliserProductComposition": null,
  "items": [
    {
      "itemType": "label_lot",
      "rawText": "LOT: 53001 250 g",
      "proposals": {
        "productLabel": {
          "valueText": "SEMENA KORUZE",
          "confidence": 0.74,
          "provenance": {"lineIndices": [0]}
        },
        "lotCode": {
          "valueText": "53001",
          "confidence": 0.98,
          "provenance": {"lineIndices": [1]}
        },
        "packQuantity": {
          "valueNum": 250,
          "unit": "g",
          "confidence": 0.97,
          "provenance": {"lineIndices": [2]}
        }
      },
      "warnings": [],
      "errors": []
    }
  ],
  "referenceHints": {
    "cropTokens": ["koruza"],
    "varietyTokens": [],
    "suggestedQueries": [
      {"endpoint": "/v1/reference/crops/search", "q": "koruza"}
    ]
  },
  "model": {
    "provider": "openai",
    "model": "gpt-4.1-mini",
    "schemaVersion": "v1"
  }
}
```

#### Fields (Normative)

- `status` (required, enum): `OK|REFUSED|ERROR`
- `documentType` (required, enum): `receipt|label|mixed|unknown`
- `documentConfidence` (required, number 0..1): model confidence in `documentType`.
- `documentUri` (nullable string): echoed when the request was tied to a persisted document record.
- `parseRunUri` (nullable string): populated when runtime persisted a parse-run provenance record.
- `signals` (required, array): deterministic pre-parse signals (see 4).
- `receipt` (nullable object): populated only if `documentType` is `receipt` or `mixed`.
- `deliveryNote` (nullable object): populated when delivery-note or weigh-ticket proposals can be extracted deterministically. This may coexist with `documentType = unknown`; the canonical delivery route key is the `deliveryNote` object, not a new `documentType` enum value.
- `soilReport` (nullable object): populated when soil-lab proposals can be extracted deterministically. This may coexist with `documentType = unknown`; the canonical soil route key is the `soilReport` object, not a new `documentType` enum value.
- `fertilisationPlan` (nullable object): populated when fertilisation-plan proposals can be extracted deterministically. This may also coexist with `documentType = unknown`; the canonical plan route key is the `fertilisationPlan` object, not a new `documentType` enum value.
- `seedSourcingException` (nullable object): populated when seed-authorization or derogation proposals can be extracted deterministically. This may coexist with `documentType = unknown`; the canonical seed-exception route key is the `seedSourcingException` object, not a new `documentType` enum value.
- `fertiliserProductComposition` (nullable object): populated when fertiliser-label proposals can be extracted deterministically. This typically coexists with `documentType = label` or `mixed`; the canonical fertiliser route key is the `fertiliserProductComposition` object, not a new `documentType` enum value.
- `items` (required, array): proposed items extracted from the document (receipt line items and/or label lots).
- `referenceHints` (required, object): tokens and recommended searches for crop/variety matching (see 6).
- `model` (required, object): metadata for audit/debug (not for UI display).

### 3.2 `receipt` Object (Normative)

When `documentType` is `receipt` or `mixed`, `receipt` MUST be non-null:

```json
{
  "vendorName": {"valueText": "Agro Trgovina d.o.o.", "confidence": 0.72, "provenance": {"lineIndices":[0]}},
  "purchaseDate": {"valueDate": "2026-02-28", "confidence": 0.90, "provenance": {"lineIndices":[2]}},
  "receiptRef": {"valueText": "RACUN 2026-00123", "confidence": 0.65, "provenance": {"lineIndices":[1]}},
  "currency": {"valueText": "EUR", "confidence": 0.55, "provenance": {"lineIndices":[3]}}
}
```

Rules:

1. `purchaseDate.valueDate` is an ISO date (`YYYY-MM-DD`) after normalization.
2. If purchase date cannot be reliably extracted, return proposal with low confidence or omit the field.

### 3.3 `items[]` (Normative)

Each item MUST have:

- `itemType`: `receipt_line_item|label_lot`
- `rawText`: a short snippet used for UI preview
- `proposals`: a map of field proposals (see 5)
- `warnings[]`: non-fatal issues (e.g., “unit inferred”)
- `errors[]`: item-level fatal issues (rare; e.g., “cannot parse quantity at all”)

### 3.4 `deliveryNote` Object (Normative)

When a delivery note or weigh ticket can be recognized, `deliveryNote` MAY be returned even if `documentType` remains `unknown`.

```json
{
  "deliveredAt": {"valueText": "2026-10-15T10:00:00", "confidence": 0.86, "provenance": {"lineIndices":[1]}},
  "lotCode": {"valueText": "L-2026-7788", "confidence": 0.90, "provenance": {"lineIndices":[2]}},
  "buyerLabel": {"valueText": "Phase1 Direct Customer", "confidence": 0.84, "provenance": {"lineIndices":[3]}},
  "buyerRegistrationId": {"valueText": "SMOKE-CUSTOMER-1", "confidence": 0.90, "provenance": {"lineIndices":[4]}},
  "buyerVatId": {"valueText": "SI12345678", "confidence": 0.90, "provenance": {"lineIndices":[5]}},
  "buyerAddress": {"valueText": "Industrial Zone 7, SI-3000 Celje", "confidence": 0.78, "provenance": {"lineIndices":[6]}},
  "ticketRef": {"valueText": "DN-2026-007", "confidence": 0.88, "provenance": {"lineIndices":[0]}},
  "netWeight": {"valueNum": 20000.0, "confidence": 0.90, "provenance": {"lineIndices":[7]}},
  "weightUnit": {"valueText": "kg", "confidence": 0.86, "provenance": {"lineIndices":[7]}},
  "grossWeight": {"valueNum": 24000.0, "confidence": 0.90, "provenance": {"lineIndices":[8]}},
  "tareWeight": {"valueNum": 4000.0, "confidence": 0.90, "provenance": {"lineIndices":[9]}},
  "moisturePct": {"valueNum": 13.8, "confidence": 0.86, "provenance": {"lineIndices":[10]}}
}
```

Rules:

1. `deliveryNote` is proposal-only and does not imply delivery-ticket commit-readiness.
2. `deliveredAt.valueText`, when present, MUST be normalized to an ISO date or ISO datetime string suitable for review and downstream datetime validation.
3. v0.5 deterministic support is intentionally narrow:
   - delivery-note / weigh-ticket title cues
   - explicit `lot` / `batch` code lines
   - explicit ticket/reference identifiers
   - explicit `net`, `gross`, and `tare` weight lines
   - explicit moisture percentage lines
   - labelled buyer-name, buyer-registration-id, buyer-vat-id, and buyer/destination address lines
4. `lotCode`, when present, is still proposal-only. Intake MAY use it to exact-resolve `fromStorageLotUri` against a single farm-scoped storage-lot match, but ambiguous or missing matches MUST stay review-only.
5. `buyerLabel`, `buyerRegistrationId`, and `buyerVatId`, when present, are still proposal-only. Intake MAY use exact buyer identifiers plus exact label agreement to resolve `buyerRef` against a single farm-scoped customer partner match, but ambiguous, conflicting, or identifier-free cases MUST stay review-only.

### 3.5 `soilReport` Object (Normative)

When a soil-lab report can be recognized, `soilReport` MAY be returned even if `documentType` remains `unknown`.

```json
{
  "labName": {"valueText": "Agro Lab d.o.o.", "confidence": 0.84, "provenance": {"lineIndices":[0]}},
  "sampleId": {"valueText": "S-2026-15", "confidence": 0.90, "provenance": {"lineIndices":[1]}},
  "sampleDate": {"valueDate": "2026-03-01", "confidence": 0.92, "provenance": {"lineIndices":[2]}},
  "gerkRef": {"valueText": "GERK-001", "confidence": 0.84, "provenance": {"lineIndices":[3]}},
  "reportDate": {"valueDate": "2026-03-05", "confidence": 0.88, "provenance": {"lineIndices":[4]}},
  "parameters": [
    {
      "parameterCode": {"valueText": "ph", "confidence": 0.90, "provenance": {"lineIndices":[5]}},
      "valueNum": {"valueNum": 6.4, "confidence": 0.93, "provenance": {"lineIndices":[5]}},
      "unit": {"valueText": "pH", "confidence": 0.86, "provenance": {"lineIndices":[5]}},
      "methodCode": {"valueText": "iso_10390", "confidence": 0.84, "provenance": {"lineIndices":[5]}}
    },
    {
      "parameterCode": {"valueText": "organic_matter", "confidence": 0.90, "provenance": {"lineIndices":[6]}},
      "valueText": {"valueText": "2.8%", "confidence": 0.90, "provenance": {"lineIndices":[6]}}
    }
  ]
}
```

Rules:

1. `sampleDate.valueDate` and `reportDate.valueDate`, when present, MUST be ISO dates (`YYYY-MM-DD`).
2. `parameters[]` is proposal-only and MAY be empty.
3. Each soil parameter row MUST contain `parameterCode` plus at least one of `valueNum` or `valueText`.
4. v0.3 deterministic support is intentionally narrow:
   - `ph`
   - `organic_matter`
   - optional explicit `gerkRef`
5. `soilReport` does not imply commit-readiness; downstream intake review may still require explicit `fieldUri`, `linkedSampleUris`, `unitSchema`, or additional parameter edits.

### 3.6 `fertilisationPlan` Object (Normative)

When a fertilisation plan can be recognized, `fertilisationPlan` MAY be returned even if `documentType` remains `unknown`.

```json
{
  "planTitle": {"valueText": "Fertilisation plan 2026", "confidence": 0.88, "provenance": {"lineIndices":[0]}},
  "planningWindowStart": {"valueDate": "2026-03-01", "confidence": 0.84, "provenance": {"lineIndices":[1]}},
  "planningWindowEnd": {"valueDate": "2026-04-15", "confidence": 0.84, "provenance": {"lineIndices":[1]}},
  "targetYieldValue": {"valueNum": 7.5, "confidence": 0.88, "provenance": {"lineIndices":[2]}},
  "targetYieldUnit": {"valueText": "t/ha", "confidence": 0.88, "provenance": {"lineIndices":[2]}},
  "ruleProfile": {"valueText": "si-organic-cereals-v1", "confidence": 0.86, "provenance": {"lineIndices":[3]}},
  "gerkRef": {"valueText": "GERK-001", "confidence": 0.84, "provenance": {"lineIndices":[4]}},
  "targetNutrients": [
    {
      "nutrientCode": {"valueText": "N", "confidence": 0.88, "provenance": {"lineIndices":[5]}},
      "valueNum": {"valueNum": 30.0, "confidence": 0.88, "provenance": {"lineIndices":[5]}},
      "unit": {"valueText": "kg/ha", "confidence": 0.88, "provenance": {"lineIndices":[5]}}
    }
  ]
}
```

Rules:

1. `fertilisationPlan` is proposal-only and does not imply plan commit-readiness.
2. `planningWindowStart` and `planningWindowEnd`, when present, MUST be ISO dates (`YYYY-MM-DD`).
3. `targetNutrients[]` rows MUST contain `nutrientCode`, at least one numeric value proposal, and a unit proposal.
4. v0.4 deterministic support is intentionally narrow:
   - title lines with fertilisation-plan cues
   - explicit planning-window date ranges
   - explicit target yield lines
   - explicit `ruleProfile`
   - explicit `GERK`
   - explicit `N`, `P2O5`, `K2O` targets in `kg/ha`
5. When no dedicated document hint exists, clients should continue using `documentHint = unknown` for fertilisation-plan captures.

### 3.7 `seedSourcingException` Object (Normative)

When a seed authorization or derogation document can be recognized, `seedSourcingException` MAY be returned even if `documentType` remains `unknown`.

```json
{
  "asOfDate": {"valueDate": "2026-03-04", "confidence": 0.88, "provenance": {"lineIndices":[1]}},
  "decisionStatusCode": {"valueText": "authorized", "confidence": 0.84, "provenance": {"lineIndices":[2]}},
  "reasonCode": {"valueText": "organic_variety_unavailable", "confidence": 0.82, "provenance": {"lineIndices":[3]}},
  "availabilityEvidenceText": {
    "valueText": "Supplier statement confirms unavailable organic variety.",
    "confidence": 0.78,
    "provenance": {"lineIndices":[4]}
  },
  "cropLabel": {"valueText": "Wheat", "confidence": 0.78, "provenance": {"lineIndices":[5]}},
  "varietyLabel": {"valueText": "Sana", "confidence": 0.80, "provenance": {"lineIndices":[6]}}
}
```

Rules:

1. `seedSourcingException` is proposal-only and does not imply seed-exception commit-readiness.
2. `asOfDate.valueDate`, when present, MUST be an ISO date (`YYYY-MM-DD`).
3. `decisionStatusCode`, when present, MUST normalize to the governed seed-sourcing exception decision values already used by runtime commit validation:
   - `authorized`
   - `conditional`
   - `rejected`
4. `reasonCode`, when present, MUST normalize to the governed seed-sourcing exception reason values already used by runtime commit validation:
   - `organic_seed_unavailable`
   - `organic_variety_unavailable`
   - `organic_planting_stock_unavailable`
   - `supplier_evidence_pending`
5. v0.6 deterministic support is intentionally narrow:
   - seed-plus-authorization/derogation title cues
   - explicit date, status, and reason lines
   - explicit availability-evidence or supplier-statement lines
   - explicit `Crop:` and `Variety:` lines
6. `seedSourcingException` does not imply that `fieldUri`, `purchaseLineUri`, `seedLotUri`, or attachment evidence can be inferred from OCR alone; intake review may still require explicit scope anchors and source-document binding before commit.

### 3.8 `fertiliserProductComposition` Object (Normative)

When a fertiliser label can be recognized, `fertiliserProductComposition` MAY be returned even if `documentType` remains `label` or `mixed`.

```json
{
  "productLabel": {"valueText": "NPK 15-15-15", "confidence": 0.86, "provenance": {"lineIndices":[0]}},
  "productCategory": {"valueText": "eu_pfc_1_c_i_a", "confidence": 0.84, "provenance": {"lineIndices":[2]}},
  "densityValue": {"valueNum": 1.23, "confidence": 0.84, "provenance": {"lineIndices":[1]}},
  "densityUnit": {"valueText": "kg/l", "confidence": 0.84, "provenance": {"lineIndices":[1]}},
  "ceOrCategoryMarkers": [
    {"valueText": "CE", "confidence": 0.82, "provenance": {"lineIndices":[2]}},
    {"valueText": "PFC_1_C_I_A", "confidence": 0.84, "provenance": {"lineIndices":[2]}}
  ],
  "applicationTextRaw": {"valueText": "Apply before sowing.", "confidence": 0.80, "provenance": {"lineIndices":[3]}},
  "storageTextRaw": {"valueText": "Keep dry.", "confidence": 0.80, "provenance": {"lineIndices":[4]}},
  "declaredNutrients": [
    {
      "nutrientCode": {"valueText": "N", "confidence": 0.86, "provenance": {"lineIndices":[0]}},
      "valueNum": {"valueNum": 15.0, "confidence": 0.86, "provenance": {"lineIndices":[0]}},
      "unit": {"valueText": "%", "confidence": 0.86, "provenance": {"lineIndices":[0]}}
    },
    {
      "nutrientCode": {"valueText": "P2O5", "confidence": 0.86, "provenance": {"lineIndices":[0]}},
      "valueNum": {"valueNum": 15.0, "confidence": 0.86, "provenance": {"lineIndices":[0]}},
      "unit": {"valueText": "%", "confidence": 0.86, "provenance": {"lineIndices":[0]}}
    },
    {
      "nutrientCode": {"valueText": "K2O", "confidence": 0.86, "provenance": {"lineIndices":[0]}},
      "valueNum": {"valueNum": 15.0, "confidence": 0.86, "provenance": {"lineIndices":[0]}},
      "unit": {"valueText": "%", "confidence": 0.86, "provenance": {"lineIndices":[0]}}
    }
  ]
}
```

Rules:

1. `fertiliserProductComposition` is proposal-only and does not imply fertiliser-composition commit-readiness.
2. `productLabel`, when present, SHOULD preserve the reviewer-visible label text rather than inventing a normalized product code.
3. `declaredNutrients[]` rows MUST contain `nutrientCode`, `valueNum`, and `unit`.
4. `densityValue` and `densityUnit`, when present, MUST be emitted as a complete pair.
5. `ceOrCategoryMarkers[]`, when present, MUST preserve reviewer-visible marker semantics such as `CE` or normalized `PFC_*` codes.
6. `productCategory`, when present, SHOULD be derived only from an explicit normalized category marker already visible on the label.
7. `applicationTextRaw` and `storageTextRaw`, when present, MUST come from explicit same-line labeled cues rather than paragraph-level summarization or inference.
8. v0.9 deterministic support is intentionally narrow:
   - `categoryHint = amendment` label items
   - fertiliser cue tokens such as `fertilizer`, `fertiliser`, `gnojivo`, `urea`, and `npk`
   - `NPK a-b-c` grade patterns
   - explicit `N`, `P2O5`, and `K2O` percentage tokens
   - explicit density lines in `kg/l` or `g/l`
   - explicit `CE` and `PFC` marker lines
   - explicit same-line `Application:` / `Use:` and `Storage:` cue lines
9. `fertiliserProductComposition` does not imply that input-material linkage can be inferred from OCR alone; intake review may still require explicit manual edits before commit.

## 4. Deterministic Signals (Normative)

`signals[]` are extracted without AI (regex/heuristics) and MUST be returned even if AI refuses.

Each signal:

- `code` (string): stable identifier
- `evidence` (object): at least one of:
  - `lineIndex` (int)
  - `offsetStart`/`offsetEnd` (int offsets in `ocrText`)

Minimum signal codes (v1):

- `HAS_LOT_KEYWORD` (e.g., “LOT”, “BATCH”, “SERIA”)
- `HAS_NET_WEIGHT` (e.g., “250 g”, “0.25 kg”)
- `HAS_DATE_CANDIDATE`
- `HAS_CURRENCY_CANDIDATE`
- `HAS_VENDOR_KEYWORD` (e.g., “d.o.o.”, “VAT”, “PIB”, “DDV”)
- `HAS_LINE_ITEM_PATTERN` (qty/unit + price-ish patterns)

## 5. Field Proposal Model (Normative)

`proposals` values are typed with *one* of the value fields set.

```json
{
  "valueText": "53001",
  "valueNum": null,
  "valueDate": null,
  "unit": null,
  "confidence": 0.98,
  "provenance": {"lineIndices":[1]},
  "normalizedFrom": {"valueText": "Lot:530O1"},
  "notes": "OCR corrected O→0 based on lot pattern"
}
```

Rules:

1. `confidence` MUST be present for any proposal returned.
2. `provenance` MUST be present for proposals for fields in the “persist-impact set”:
   - `lotCode`, `purchaseDate`, `quantity`, `packQuantity`, `productLabel`, `cropRefUri`, `varietyRefUri`.
3. If no provenance exists, the parser MUST either:
   - omit the proposal, or
   - return it with `confidence <= 0.40` and a warning explaining “no direct evidence”.

## 6. Reference Hints (Normative)

This endpoint does **not** persist reference entities. It provides hints to connect parsed text to Farm_RM reference URIs.

`referenceHints` must include:

- `cropTokens[]`: normalized tokens (lowercased, diacritics-folded).
- `varietyTokens[]`: same.
- `suggestedQueries[]`: explicit suggestions iOS can call.

Optional extension (v1.1+):

- `referenceCandidates[]`: if the backend has local reference snapshot loaded, it MAY include top-N candidate URIs and labels. If present, candidates MUST be produced by deterministic search; the AI may select among these candidates but may not invent new URIs.

## 7. Error Handling (Normative)

### 7.1 HTTP Errors

- `400` invalid body (missing required fields)
- `413` OCR text/lines too large
- `429` rate limited
- `503` AI service unavailable

### 7.2 In-band Refusal

If the AI model refuses (policy or safety), return HTTP 200 with:

```json
{
  "status": "REFUSED",
  "documentType": "unknown",
  "documentConfidence": 0.0,
  "signals": [...],
  "receipt": null,
  "items": [],
  "referenceHints": {"cropTokens":[], "varietyTokens":[], "suggestedQueries":[]},
  "refusal": {"code":"MODEL_REFUSED", "message":"Unable to parse this text."},
  "model": {...}
}
```

Rationale: iOS can still render deterministic signals and allow manual entry.

## 8. Acceptance Criteria (Testable)

1. For the same input payload, the response must be valid against the strict schema and parseable without additional model calls.
2. If `ocrText` contains a recognizable lot keyword and a code, `HAS_LOT_KEYWORD` appears in `signals`.
3. Persist-impact proposals include provenance.
4. The endpoint never returns minted URIs (no random `urn:*` created by parsing).
5. Refusal and AI-unavailable paths still return deterministic signals and an understandable status.

## 9. Dependencies

- Part 0 invariants apply.
- Part 3 reference endpoints (optional integration for candidates).

## 10. Next Part

Part 2: Inventory persistence targets (label flow + backward compatibility): [part-2-inventory-persistence-targets.md](/Users/einstein/Documents/Codex/Semantic%20farming/docs/implementation/ai-capture-assist/part-2-inventory-persistence-targets.md)
