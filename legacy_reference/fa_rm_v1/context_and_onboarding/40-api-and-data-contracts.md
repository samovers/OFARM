# API And Data Contracts

Use this doc for contract ownership and the highest-value request or response families. For runtime process shape, use [30-runtime-architecture.md](30-runtime-architecture.md). For compliance boundaries, use [50-compliance-and-reporting.md](50-compliance-and-reporting.md). For commands that exercise these surfaces, use [60-build-run-test-generate.md](60-build-run-test-generate.md).

## Contract sources

- `implemented`: the primary OF Platform runtime contract source is the Pydantic model layer in `app.main`, not just the static OpenAPI YAML. `specs/api/v1/server/fastapi/app/main.py:L214-L246`, `specs/api/v1/server/fastapi/app/main.py:L1134-L1157`, `specs/api/v1/server/fastapi/app/main.py:L1252-L1311`, `specs/api/v1/server/fastapi/app/main.py:L1705-L1824`
- `implemented`: the repository also ships a static OpenAPI contract file. The legacy filename remains `openapi-farm-rm.yaml` for compatibility even when user-facing terminology says OF Platform / OFARM. `specs/api/v1/openapi-farm-rm.yaml:L1-L5`
- `implemented`: the static and runtime OpenAPI metadata currently align at `1.0.26`, and both now present the API as `OF Platform API`. `specs/api/v1/openapi-farm-rm.yaml:L1-L5`, `specs/api/v1/server/fastapi/app/main.py:L285-L320`
- `implemented`: the repo now has a canonical snapshot refresh path: `make openapi-export` rewrites `specs/api/v1/openapi-farm-rm.yaml` from the runtime app, and `make openapi-export-check` proves whether the checked-in snapshot is already current. `Makefile:L1-L35`, `specs/api/v1/server/fastapi/run-openapi-export.sh:L1-L35`, `specs/api/v1/server/fastapi/scripts/export_openapi_snapshot.py:L1-L49`
- `implemented`: there are explicit contract-alignment tests for selected request/response schemas and paths, plus top-level metadata/security parity. `specs/api/v1/server/fastapi/tests/test_openapi_contract_alignment.py:L98-L243`

## High-value contract families

### `/v1/capabilities`

- `implemented`: exposes feature flags and minimum client-version gates for OCR parse and metrics, advisor recommendation surfaces, crop-context ensure, additive operation-workbench surfaces, reference search/import/catalog/diff, ingestion readiness, and season windows. `specs/api/v1/server/fastapi/app/main.py:L21427-L21464`, `specs/api/v1/server/fastapi/tests/test_advisor_api.py:L289-L306`, `specs/api/v1/server/fastapi/tests/test_operation_drafts.py:L693-L700`
- `implemented`: the response model is explicitly typed. `specs/api/v1/server/fastapi/app/main.py:L223-L246`

### `/v1/advisor/*`

- `implemented`: the advisor runtime exposes recommendation, bundle fetch, accept, override, supersede, and objective-profile routes under `/v1/advisor/*`. `specs/api/v1/server/fastapi/app/main.py:L21770-L21915`, `specs/api/v1/openapi-farm-rm.yaml:L294-L482`
- `implemented`: capability exposure is honest about preview versus persistence-backed behavior; tests prove preview-mode feature flags and the persistence-disabled reason for persisted bundles. `specs/api/v1/server/fastapi/tests/test_advisor_api.py:L289-L310`
- `implemented`: selected static/runtime OpenAPI alignment checks already cover the advisor path group and `AdvisorRecommendationBundle` schema. `specs/api/v1/server/fastapi/tests/test_openapi_contract_alignment.py:L194-L264`

### `/v1/ai/ocr/parse`

- `implemented`: the request contract accepts text, OCR lines, optional image, locale, capture time, document hint, and optional context. `specs/api/v1/server/fastapi/app/main.py:L1681-L1714`
- `implemented`: the response returns status, document type, confidence, signals, receipt header fields, typed proposal payloads, item proposals, reference hints, persistence targets, refusal, and model info. `specs/api/v1/server/fastapi/app/main.py:L1716-L1793`
- `implemented`: endpoint behavior is feature-flagged and supports deterministic fallback plus optional OpenAI-backed hybrid parsing, with document-specific proposal enrichment layered in by runtime code rather than a receipt-only schema. `specs/api/v1/server/fastapi/app/main.py:L9129-L9299`
- `implemented`: tests cover deterministic Slovenian parsing and hybrid enrichment against reference data. `specs/api/v1/server/fastapi/tests/test_ai_ocr_slovenian_label_fallbacks.py:L50-L76`, `specs/api/v1/server/fastapi/tests/test_ai_ocr_slovenian_label_fallbacks.py:L78-L129`, `specs/api/v1/server/fastapi/tests/test_ai_ocr_slovenian_label_fallbacks.py:L131-L185`, `specs/api/v1/server/fastapi/tests/test_ai_ocr_slovenian_label_fallbacks.py:L214-L260`

### `/v1/inventory/receipts/import`

- `implemented`: the request supports `receiptRef`, vendor metadata, invoice evidence fields, and line items that can carry `cropLabel`, `variety`, `statusCode`, `lotLabel`, and quantity. `specs/api/v1/server/fastapi/app/main.py:L1134-L1157`
- `implemented`: the response returns imported line items, normalized fields, and persistence info. `specs/api/v1/server/fastapi/app/main.py:L1795-L1824`
- `implemented`: the runtime endpoint enforces category hints and E/P/K status code validation and persists or normalizes crop label for reporting. `specs/api/v1/server/fastapi/app/main.py:L25324-L25440`, `specs/v0.8/sql/migrations/0086_v1_7_inventory_receipt_line_item_crop_label.sql:L1-L8`

### Reference ingestion and search

- `implemented`: `/v1/reference/sources`, `/v1/reference/source-plan`, `/v1/reference/source-profiles`, and `/v1/reference/source-ingestion/check` cover source cataloging, deterministic ingestion planning, profile-backed operator guidance, and pre-import readiness checks for crop and variety reference ingestion. `specs/api/v1/server/fastapi/tests/test_api.py:L14754-L15098`, `specs/api/v1/server/fastapi/tests/test_openapi_contract_alignment.py:L1510-L1649`, `specs/v0.8/reference-ingest/README.md:L1-L198`
- `implemented`: `/v1/reference/snapshots/import`, `/v1/reference/snapshots/import/preview`, `/v1/reference/snapshots`, and `/v1/reference/snapshots/diff` cover immutable snapshot import, side-effect-free preview, snapshot catalog listing, and version-to-version diff review. `specs/api/v1/server/fastapi/tests/test_api.py:L14004-L14753`, `specs/api/v1/server/fastapi/tests/test_openapi_contract_alignment.py:L1333-L1509`
- `implemented`: `/v1/reference/evidence-items` creates canonical `evidence_item` rows for downstream reference and decision consumers, and can bind them to an existing `evidence_record` when `evidenceUri` is supplied. `specs/api/v1/server/fastapi/app/main.py`, `specs/api/v1/server/fastapi/app/persistence.py`
- `implemented`: `CropRefItem` and `VarietyRefItem` contracts expose multilingual labels, synonyms, taxonomy or market fields, match score, and source provenance. `specs/api/v1/server/fastapi/app/main.py:L1252-L1311`
- `implemented`: `/v1/reference/varieties/search` requires both `q` and `cropUri`, supports language and source-version or source-system filters, returns ranked matches, and returns `reference_snapshot_not_found` when a requested snapshot slice is missing. `specs/api/v1/server/fastapi/tests/test_api.py:L13962-L14003`, `specs/api/v1/server/fastapi/tests/test_api.py:L15162-L15314`
- For operator flow and tooling, use [60-build-run-test-generate.md](60-build-run-test-generate.md) and `specs/v0.8/reference-ingest/README.md`.

### Field-operation logging and crop context

- `implemented`: `/v1/capabilities` advertises `features.cropContextEnsure`, and `/v1/field-ops/crop-contexts/ensure` is the explicit pre-resolution contract for crop-bound logging. `specs/api/v1/server/fastapi/app/main.py:L15444-L15452`, `specs/api/v1/server/fastapi/app/main.py:L21752-L21920`, `specs/api/v1/server/fastapi/tests/test_crop_context_ensure.py:L89-L376`
- `implemented`: current operation commit routes are family-specific rather than generic. Confirmed route inventory includes planting, mechanical weeding, cover-crop management, tillage, plant protection, pesticide, irrigation, and harvest. `specs/api/v1/server/fastapi/app/main.py:L25109-L28988`
- `implemented`: representative write contracts keep strict farm, field, and crop context and preserve ad-hoc execution by making `plannedOperationUri` optional. `specs/api/v1/server/fastapi/app/main.py:L25171-L25179`, `specs/api/v1/server/fastapi/app/main.py:L28540-L28548`, `specs/api/v1/server/fastapi/app/main.py:L28865-L28873`
- `implemented`: `/v1/capabilities` also exposes `operationProposals`, `operationDrafts`, `operationAssessments`, and `controlCenterAttestationWorkbench` with explicit minimum client versions. `specs/api/v1/server/fastapi/app/main.py:L21427-L21431`, `specs/api/v1/server/fastapi/tests/test_operation_drafts.py:L693-L700`
- `implemented`: generic proposal, draft, assessment, report-binding backfill, and review-queue routes exist as additive runtime surfaces, static OpenAPI paths, and contract-tested schemas. They complement the authoritative event-specific commit routes rather than replacing them. `specs/api/v1/server/fastapi/app/main.py:L47920-L49173`, `specs/api/v1/server/fastapi/tests/test_openapi_contract_alignment.py:L1588-L1695`, `specs/api/v1/server/fastapi/tests/test_operation_drafts.py:L703-L1348`
- `implemented`: `/v1/fields/{fieldUri:path}/operation-history` is the field-scoped read model for committed executed operations, with capability gating through `features.fieldOperationHistory` and contract-tested static/runtime alignment. `specs/api/v1/server/fastapi/app/main.py:L20761-L20839`, `specs/api/v1/server/fastapi/app/persistence.py:L18219-L18429`, `specs/api/v1/server/fastapi/tests/test_api.py:L20549-L20624`, `specs/api/v1/server/fastapi/tests/test_openapi_contract_alignment.py:L182-L207`

### Reporting and compliance

- `implemented`: `/v1/reporting/render` takes report/template/layout codes, period, field/context snapshots, and blank-handling flags. `specs/api/v1/server/fastapi/app/main.py:L265-L304`, `specs/api/v1/server/fastapi/app/main.py:L30683-L30940`
- `implemented`: `/v1/reporting/packs` lists report pack registry items. `specs/api/v1/server/fastapi/app/main.py:L30943-L30994`
- `implemented`: `/v1/compliance/claims/validate` still shells to the rulepack-driven validator for semantics, but the runtime/OpenAPI contract is now explicitly typed through `ClaimValidationRequest`, `ClaimValidationResponse`, and `ClaimValidationRuleResult` instead of generic `object` payloads. `specs/api/v1/server/fastapi/app/main.py:L6213-L6253`, `specs/api/v1/server/fastapi/app/main.py:L31873-L31875`, `specs/api/v1/server/fastapi/app/reporting_routes.py:L10-L15`, `specs/api/v1/server/fastapi/tests/test_openapi_contract_alignment.py:L177-L208`, `specs/v0.1/validation/bin/validate-claim.sh:L20-L75`
- For jurisdiction and reporting-scope boundaries, use [50-compliance-and-reporting.md](50-compliance-and-reporting.md).

### Compliance fact capture for attestation workflows

- `implemented`: `/v1/compliance/jurisdiction-facts` rejects derived fact keys and enforces value-type-specific contracts. `specs/api/v1/server/fastapi/app/main.py:L42049-L42257`, `specs/api/v1/server/fastapi/tests/test_api.py:L13543-L13714`
- `implemented`: `/v1/compliance/conversion-timelines` supports farm or field scope, supersession, and role-coded attachment evidence. `specs/api/v1/server/fastapi/app/main.py:L42260-L42489`, `specs/api/v1/server/fastapi/tests/test_api.py:L13728-L13809`
- `implemented`: `/v1/compliance/parallel-production-controls` enforces minimum control signals when parallel production is present. `specs/api/v1/server/fastapi/app/main.py:L42581-L42766`, `specs/api/v1/server/fastapi/tests/test_api.py:L13829-L13881`
- `implemented`: `/v1/compliance/seed-sourcing-exceptions` requires at least one scope anchor plus attachment evidence. `specs/api/v1/server/fastapi/app/main.py:L42806-L42898`, `specs/api/v1/server/fastapi/tests/test_api.py:L13903-L13996`

### Other tested operational surfaces

- `implemented`: coverage, fuel allocation, telematics classification, localized label resolution, and template projection retrieval are present in both the static contract and runtime. `specs/api/v1/openapi-farm-rm.yaml:L7-L207`, `specs/api/v1/openapi-farm-rm.yaml:L114-L150`
- `implemented`: tests also exercise seed or equipment suitability, scenario risk, contamination risk, claim validation, and partner price-history tenancy flow. `specs/api/v1/server/fastapi/tests/test_api.py:L138-L260`

## Data-contract patterns worth preserving

- strongly typed Pydantic models in runtime code
- capability discovery for client gating
- explicit reference provenance (`sourceSystem`, `sourceId`, `sourceVersion`)
- evidence-aware import and report payloads
- template projection contracts kept separate from archetype source meaning

## Contract-layer cautions

- `partial`: alignment tests verify selected schemas and paths plus top-level metadata or security parity, not every endpoint or every nested field. `specs/api/v1/server/fastapi/tests/test_openapi_contract_alignment.py:L98-L243`
- `inferred`: when conflicts appear, runtime Pydantic models plus tests are more trustworthy than the static YAML, even though the current user-facing naming now aligns. `specs/api/v1/server/fastapi/app/main.py:L214-L232`, `specs/api/v1/server/fastapi/tests/test_openapi_contract_alignment.py:L85-L243`
