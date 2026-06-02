# Spec Part 2: Inventory Persistence Targets (Label Flow + Backward Compatibility)

Version: 0.1 (draft)  
Date: 2026-03-01  
Applies to: Farm_RM persistence + API contract

## 0. Scope

Define the **minimal** Farm_RM persistence targets and API endpoints required to:

1. Persist confirmed “label scan” results (lot/batch capture) without abusing receipt semantics.
2. Keep `POST /v1/inventory/receipts/import` working and improve it to support idempotent retry and optional linking to previously captured lots.

This part is intentionally “inventory-only” and does not cover crop/variety reference (Part 3) or season windows (Part 4).

## 1. Goals / Non-goals

### 1.1 Goals

1. Provide an explicit endpoint for “label → lot/batch capture” persistence.
2. Provide idempotency semantics for offline-first retry.
3. Enable (optional) linking between:
   - receipt line items and
   - material lots (captured from labels or otherwise).

### 1.2 Non-goals

1. Perfect de-duplication of products across all receipts (this is a later curation problem).
2. Solving full commerce (pricing, shipping) in this feature.

## 2. Core Principle (Normative)

- AI parse outputs are **candidates**.
- Only after user confirmation does iOS call persistence endpoints.
- Persistence endpoints write **truth records** (even if incomplete), so validation must be strict enough to avoid garbage, but not so strict that capture becomes unusable.

## 3. New Endpoints (Normative)

### 3.1 `POST /v1/inventory/resources` (Create/Resolve Input Material Resource)

Purpose: create a Farm_RM `resource` of type `input_material` (seed, fertilizer, crop protection, etc.) to anchor lots and receipt line items.

Request shape (v1):

```json
{
  "farmUri": "https://data.farmco.si/farm-rm/v1/farm/SI/FARMCO",
  "resourceType": "input_material",
  "label": "Koruza seme (paket 250 g)",
  "externalCode": null,
  "localizedLabels": [
    {"lang": "sl-SI", "role": "pref", "text": "Koruza seme (paket 250 g)"},
    {"lang": "en", "role": "pref", "text": "Maize seed (250 g pack)"}
  ],
  "source": "ios",
  "sourceRef": "ios:labelDraft:7b2b6d3f-9b8a-4c87-9c3c-3d4b7b4e1a21"
}
```

Rules:

1. `resourceType` MUST be `input_material` for this endpoint version.
2. `label` MUST be non-empty.
3. `sourceRef` MUST be present and stable per client draft to support idempotency.

Response shape:

```json
{
  "resourceUri": "https://data.farmco.si/farm-rm/v1/resource/SI/INPUT-3c7f…",
  "resolved": "created",
  "farmUri": "…",
  "label": "Koruza seme (paket 250 g)"
}
```

Idempotency (normative):

- For the same `(farmUri, source, sourceRef)` the server MUST return the same `resourceUri` and MUST NOT create duplicates.

### 3.2 `POST /v1/inventory/material-lots` (Create/Resolve Lot/Batch)

Purpose: persist a confirmed lot/batch from a label scan (or manual entry).

Request shape (v1):

```json
{
  "farmUri": "https://data.farmco.si/farm-rm/v1/farm/SI/FARMCO",
  "lotKind": "material",
  "inputMaterial": {
    "resourceUri": "https://data.farmco.si/farm-rm/v1/resource/SI/INPUT-3c7f…"
  },
  "lotCode": "53001",
  "supplier": {
    "supplierName": "Agro Trgovina d.o.o.",
    "supplierCounterpartyUri": null
  },
  "validFrom": null,
  "validTo": null,
  "commercialReference": null,
  "evidence": {
    "labelEvidenceType": null,
    "labelEvidenceRef": null,
    "labelEvidenceUri": null
  },
  "source": "ios",
  "sourceRef": "ios:labelDraft:7b2b6d3f-9b8a-4c87-9c3c-3d4b7b4e1a21"
}
```

Rules:

1. `lotCode` MUST be non-empty and trimmed.
2. `inputMaterial.resourceUri` is REQUIRED unless `inputMaterial.resource` is provided (inline create).
3. `lotKind` MUST be one of:
   - `material` (generic input lot; persists to `material_lot`)
   - `seed` (persists seed extension; see 3.3)
4. `sourceRef` MUST be present and stable for idempotency.

Inline resource create (optional convenience):

```json
{
  "inputMaterial": {
    "resource": {
      "label": "Herbicide X (1 L)",
      "resourceType": "input_material"
    }
  }
}
```

Response shape:

```json
{
  "materialLotUri": "https://data.farmco.si/farm-rm/v1/material-lot/SI/LOT-91d2…",
  "resolved": "created",
  "inputMaterialResourceUri": "https://data.farmco.si/farm-rm/v1/resource/SI/INPUT-3c7f…",
  "lotCode": "53001",
  "lotKind": "material"
}
```

Idempotency (normative):

- For the same `(farmUri, source, sourceRef)` the server MUST return the same `materialLotUri`.

### 3.3 Seed Lots (v1 behavior)

Seed labels carry crop/variety significance. Farm_RM already has `seed_lot_ext` (seed-specific lot attributes) keyed by `(varietyUri, lotCode)`.

This feature adds seed support to the lot endpoint via `lotKind="seed"` and a required `seed` block:

```json
{
  "lotKind": "seed",
  "lotCode": "53001",
  "seed": {
    "varietyUri": "https://data.farmco.si/farm-rm/v1/variety/EU/MAIZE-FOO-123",
    "germinationPct": 95.0,
    "purityPct": 98.0,
    "treatedFlag": true,
    "certifiedFlag": true
  }
}
```

Rules:

1. If `lotKind="seed"`, `seed.varietyUri` is REQUIRED.
2. The server MUST create/resolve a `seed_lot_ext` record using `(varietyUri, lotCode)` uniqueness.
3. The response MUST include `seedLotUri` when a seed lot extension is created/resolved.

Response example:

```json
{
  "materialLotUri": "https://data.farmco.si/farm-rm/v1/material-lot/SI/LOT-91d2…",
  "seedLotUri": "https://data.farmco.si/farm-rm/v1/seed-lot/SI/SEEDLOT-2a1c…",
  "resolved": "created",
  "lotKind": "seed",
  "lotCode": "53001",
  "seed": {"varietyUri":"…", "germinationPct":95.0, "purityPct":98.0, "treatedFlag":true, "certifiedFlag":true}
}
```

Note: In v1, `seedLotUri` and `materialLotUri` are not guaranteed to be 1:1 linked in persistence (existing schema limitation). This is acceptable for the MVP capture workflow; a later refinement may explicitly link them.

## 4. Backward Compatibility: `POST /v1/inventory/receipts/import` (Normative Adjustments)

### 4.1 Contract Drift Fix (Normative)

Current server implementation accepts fields that are missing or incomplete in OpenAPI (`variety`, `statusCode`, invoice evidence fields).

Requirement:

1. Update OpenAPI request schema for receipt import so it matches implementation:
   - line item fields: `cropLabel` (seed reporting), `variety`, `statusCode`, `lotLabel`, `quantityValue`, `quantityUnit`
   - top-level fields: `invoiceEvidenceType`, `invoiceEvidenceRef`, `invoiceEvidenceUri`
2. Add response schema fields that are returned by the server.

Normalization note:
- Receipt import may continue to capture invoice evidence via top-level `invoiceEvidence*` fields.
- Downstream recordbook/binder contracts SHOULD normalize that invoice evidence into row-level `sources.attachmentEvidence[]` with `roleCode='invoice'`.

This is required so iOS can treat OCR output as “Farm_RM-shaped” without undefined behavior.

### 4.2 Optional Linking Fields (v1.1+ but recommended now)

Extend receipt import line items with optional identifiers:

- `resourceUri` (optional)
- `materialLotUri` (optional)

Rules:

1. If `resourceUri` is provided, the server MUST validate it resolves within the farm tenancy.
2. If `materialLotUri` is provided, the server MUST validate it resolves and use it for the line item rather than minting a new lot.
3. If neither is provided, server behavior remains “create new”.

### 4.3 SI Seed Purchases (A.7) Field Semantics (Normative)

The SI recordbook seed/seedling purchase section (A.7) requires distinguishing:

1. The **seed crop** ("Kultura")
2. The **seed variety** ("Sorta")
3. The **seed status** (`E|P|K`) used in organic / conversion / conventional differentiation
4. The **invoice/receipt reference** ("Stevilka priloge/racuna")

Receipt import MUST support these as first-class, user-confirmable fields on each seed line item:

- `categoryHint="seed"` (required to classify the row into A.7)
- `cropLabel` (optional but SI-reporting-critical): the crop name as shown/confirmed by the user
- `variety` (optional): variety/hybrid/cultivar label
- `statusCode` (optional): `E|P|K` (may be missing at capture time; binder will warn)
- `receiptRef` (top-level, required): invoice/receipt number

Normative reporting mapping (SI):

- A.7 `crop` and `cropLabel` MUST prefer `cropLabel` when present.
- If `cropLabel` is missing for a seed line item, Farm_RM SHOULD:
  - fall back to `resourceLabel` for A.7 output (best-effort), and
  - emit a binder warning indicating a missing crop label for the seed purchase row.

Note: `resourceLabel` is the commercial product label ("productName") and is not a reliable substitute for crop.

### 4.4 Idempotency for Offline Retry (Recommended)

Offline-first clients retry. Receipt import must not duplicate records under retry.

Normative idempotency rule:

- Treat `(farmUri, source, receiptRef)` as a **client idempotency key**.

Server requirements:

1. If an import exists for the same key, return the existing `receiptImportUri` and its line items.
2. Otherwise, create a new import.

Persistence requirement (schema):

- Add a unique constraint to `inventory_receipt_import`:
  - `UNIQUE(farm_uri, source, receipt_ref)`

## 5. Evidence Hooks (Optional, Normative Shape)

Label captures and receipts often need evidence (photo, invoice, certification label).

In v1, evidence can be attached as:

- `labelEvidenceType + labelEvidenceRef` (create new evidence record), or
- `labelEvidenceUri` (link to existing evidence record).

Rules:

1. If `*EvidenceType` is provided, either `*EvidenceRef` or `*EvidenceUri` MUST be provided.
2. If `*EvidenceUri` is provided, it MUST resolve to an existing evidence record.

## 6. Acceptance Criteria (Testable)

1. iOS can persist a confirmed label scan as a material lot without calling receipt import.
2. Replaying the same request with the same `sourceRef` returns the same URIs.
3. Receipt import OpenAPI matches actual server contract (no undocumented accepted fields).
4. Receipt import can be retried safely without duplicating records (idempotency).
5. If a receipt line item references an existing `materialLotUri`, the link is preserved and returned.
6. For `categoryHint="seed"` line items, `cropLabel` (when provided) is carried through into SI A.7 output as the crop/cropLabel value (no longer conflated with `resourceLabel`).

## 7. Dependencies

- Existing `resource`, `material_lot`, `seed_lot_ext` persistence primitives.
- Evidence model (`evidence_record`) for optional evidence attachment.

## 8. Next Part

Part 3: Crop/variety reference + normalization: [part-3-crop-variety-reference-normalization.md](/Users/einstein/Documents/Codex/Semantic%20farming/docs/implementation/ai-capture-assist/part-3-crop-variety-reference-normalization.md)
