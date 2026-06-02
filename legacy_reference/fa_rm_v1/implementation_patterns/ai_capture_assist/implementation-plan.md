# Implementation Plan: AI Capture Assist + Reference + Agronomy Knowledge

Version: 0.2 (draft)
Date: 2026-03-13
Scope: Farm_RM backend + Farman Lite iOS

This plan originally turned the spec set in `docs/implementation/ai-capture-assist/` into executable phases.

Current status note (2026-03-13):

1. Several early phases are now implemented in runtime, including `/v1/capabilities`, `/v1/ai/ocr/parse`, reference search, season windows, document registry, and the universal capture intake seam under `/v1/intake/*`.
2. Use [part-7-universal-capture-intake-contract.md](/Users/einstein/Documents/Codex/Semantic%20farming/docs/implementation/ai-capture-assist/part-7-universal-capture-intake-contract.md) as the current backend contract for scanner-style orchestration.
3. Keep this page as historical phase provenance plus residual-work ordering, not as the canonical current intake contract.

Guiding constraints (must hold throughout):

1. AI endpoints are proposal-only for business truth; document and parse provenance may persist when the contract explicitly allows it.
2. Offline-first retry must not create duplicates (idempotency).
3. Clients never mint Farm_RM URIs.
4. Privacy by default (no raw OCR in logs; bounded retention).

## Phase 0: Contract Alignment + Capability Discovery (Backend)

Goal: make contracts stable so iOS can integrate safely without guessing.

Deliverables:

1. Update OpenAPI for `POST /v1/inventory/receipts/import` to match server behavior (drift fix).
2. Add `GET /v1/capabilities` endpoint (feature discovery + server version).
3. Add CI checks ensuring OpenAPI and server stay aligned for the touched endpoints.

Acceptance criteria:

1. OpenAPI contains all request/response fields used by the server for receipt import.
2. iOS can determine if `aiOcrParse`, `referenceSearch`, `seasonWindows` are available at runtime.

## Phase 1: `/v1/ai/ocr/parse` (Backend) + Golden Fixtures

Goal: create the proposal endpoint with strict schema, deterministic signals, and stable failure modes.

Deliverables:

1. Implement `POST /v1/ai/ocr/parse` with:
   - request size limits
   - deterministic `signals[]`
   - strict response schema
   - refusal/unavailable behavior returning `status=REFUSED|ERROR` with signals
2. Add golden OCR fixtures and regression tests:
   - receipts: SI + RS
   - labels: seed + crop protection
   - mixed/unknown
3. Add privacy guardrails:
   - no raw OCR text in logs
   - structured error codes

Acceptance criteria:

1. Fixtures pass in CI and validate strict schema.
2. Persist-impact proposals include provenance when present.
3. Endpoint does not create or mutate Farm_RM business-truth records; document and parse provenance persistence is allowed when `documentUri` is supplied and the contract explicitly supports it.

## Phase 2: Receipt Flow Integration (iOS)

Goal: improve receipt capture predictability without breaking offline flow.

Deliverables:

1. Update receipt scan flow:
   - call `/v1/ai/ocr/parse` when available
   - apply values only if confidence + provenance meet thresholds
   - show provenance highlights / “why” strings
2. Add `OCRParseJob` to offline queue:
   - retry/backoff rules
   - clear user statuses
3. Keep current `/v1/inventory/receipts/import` sync behavior as the persistence step after user confirmation.

Acceptance criteria:

1. Offline capture works end-to-end (draft created, later parse, later sync).
2. Low-confidence fields are never silently applied.
3. Validation failures stop auto-retry and surface actionable UI.

## Phase 3: Inventory Lot Persistence Endpoints (Backend)

Goal: support label-driven lot capture without misusing receipts.

Deliverables:

1. Implement `POST /v1/inventory/resources`:
   - create/resolve `resource` (`input_material`)
   - idempotency via `(farmUri, source, sourceRef)`
2. Implement `POST /v1/inventory/material-lots`:
   - create/resolve `material_lot`
   - optional seed extension create/resolve (`seed_lot_ext`) for `lotKind=seed`
   - evidence hooks (optional)
3. Add (recommended) DB uniqueness constraints to support idempotency keys.

Acceptance criteria:

1. Replaying the same request does not create duplicates.
2. Seed lots can be captured with `varietyUri` and `lotCode` without manual DB work.

## Phase 4: Label Flow Integration (iOS)

Goal: add label scan + review + lot persistence, with manual linking to receipts.

Deliverables:

1. Label scan + review UI driven by parse response.
2. Persistence path:
   - ensure resource exists (create/resolve)
   - create/resolve lot (`material-lots`)
3. Manual receipt↔label linking UI (no auto-link).

Acceptance criteria:

1. Label scan produces a persisted lot (or a clear validation error).
2. Users can attach a label to a receipt and vice versa.

## Phase 5: Crop/Variety Reference Search (Backend) + iOS UI

Goal: normalization becomes a user-visible, stable selection process.

Deliverables:

1. Implement `GET /v1/reference/crops/search` and `/v1/reference/varieties/search`:
   - deterministic ranking
   - multilingual labels
   - source attribution
   - caching headers
2. iOS crop/variety selection UI:
   - top-N candidates
   - “Unknown” option

Acceptance criteria:

1. Same query returns stable ordering for the same snapshot.
2. Slovenian labels are shown when present.
3. iOS persists only URIs selected from the reference endpoints.

## Phase 6: Season Windows Knowledge Pack (Backend) + iOS Priors

Goal: provide deterministic timing priors to improve operation suggestions.

Deliverables:

1. Implement `GET /v1/agronomy/season-windows`:
   - dataset identity + versioning
   - region mapping
   - caching headers
2. iOS caching and ranker integration:
   - cache by `(cropUri, regionId, datasetVersion)`
   - use as priors in on-device ranking with explainable reasons

Acceptance criteria:

1. Pinned `datasetVersion` yields stable results.
2. iOS shows clear “in window” explanations and continues functioning offline.

## Phase 7: Security, QA, Rollout Hardening

Goal: safely enable the feature for real users.

Deliverables:

1. Rate limiting for AI parse endpoint.
2. Metrics:
   - request volume
   - error codes
   - parse latency
   - fixture regression outcomes
3. Rollout flags and staging defaults:
   - parse enabled only for internal/staging until fixture corpus is strong

Acceptance criteria:

1. No OCR text leaked in logs.
2. Feature can be disabled server-side without breaking iOS flows.

## Phase 8: Reference Source Ingestion Operationalization

Goal: make reference-data onboarding reproducible and safe for real source snapshots (EU catalog/CPVO/EPPO style).

Deliverables:

1. Add a source-profile mechanism to ingestion tooling:
   - profile-driven defaults for source metadata
   - explicit override precedence for CLI fields
2. Harden snapshot build validation:
   - reject duplicate crop/variety URIs
   - reject varieties whose `crop_uri` is not present in crop rows
3. Add regression tests for the ingestion CLI:
   - profile defaults path
   - duplicate/unknown-reference failure paths
   - required version metadata rules
4. Document source profiles and operational cadence in the runbook.

Acceptance criteria:

1. Invalid source CSVs fail at build time with clear errors.
2. Pipeline behavior is covered by CI tests.
3. Operators can run ingestion with profile + version arguments without hand-editing payload JSON.

## Phase 9: Reference Search Version Pinning + Cache Correctness

Goal: guarantee deterministic query behavior and correct caching when multiple snapshots exist.

Deliverables:

1. Extend reference search endpoints with optional `sourceVersion` filter.
2. Return effective response `sourceVersion` in search payloads.
3. Emit cache/version headers from effective snapshot:
   - dynamic `ETag`
   - `X-Reference-Source-Version`
4. Return `404` for unknown pinned versions.
5. Add API/OpenAPI tests for pinning and header behavior.

Acceptance criteria:

1. Repeated search with pinned snapshot yields stable ordering and stable `ETag`.
2. Unknown pinned snapshot returns deterministic `404` error code.
3. OpenAPI and runtime contracts remain aligned and CI guards pass.

## Phase 10: Reference Snapshot Discovery Endpoint

Goal: make snapshot/version selection explicit for clients and operators.

Deliverables:

1. Add `GET /v1/reference/snapshots` endpoint with optional `sourceSystem` filter.
2. Return catalog metadata for each snapshot:
   - `snapshotUri`, `sourceSystem`, `sourceVersion`
   - `publishedAt`, `importedAt`
   - `cropCount`, `varietyCount`
   - `isLatest`
3. Provide bundled fallback catalog item when DB snapshot tables are unavailable.
4. Add API/OpenAPI tests for endpoint behavior and contract alignment.

Acceptance criteria:

1. iOS/backend clients can discover available versions without hardcoded lists.
2. Endpoint returns deterministic ordering and stable cache headers.
3. CI guards (`pytest`, OpenAPI alignment, bundle verify) stay green.

## Phase 11: OCR Runtime Metrics Endpoint

Goal: provide rollout-quality telemetry directly from the API stub for QA gating.

Deliverables:

1. Add `GET /v1/ai/ocr/metrics` endpoint.
2. Track aggregate OCR parse metrics in-memory:
   - total request count
   - parse status counts (`OK`, `REFUSED`)
   - HTTP status counts
   - error code counts
   - latency stats (`p50`, `p95`, `max`, window size)
3. Add API/OpenAPI tests for metrics endpoint contract and behavior.

Acceptance criteria:

1. Endpoint shows metric deltas after OCR parse calls.
2. Latency/stat payload is schema-stable and OpenAPI-aligned.
3. CI passes with metrics path included in contract checks.

## Phase 12: Capability Discovery Expansion

Goal: keep client fallback logic accurate as new endpoints are added.

Deliverables:

1. Extend `/v1/capabilities` with:
   - `aiOcrMetrics`
   - `referenceSnapshotCatalog`
2. Gate endpoint availability with dedicated feature flags:
   - `AI_OCR_METRICS_ENABLED`
   - `REFERENCE_SNAPSHOT_CATALOG_ENABLED`
3. Add API/OpenAPI tests to prevent capability-schema drift.

Acceptance criteria:

1. Clients can detect and conditionally use metrics/catalog endpoints.
2. Feature-disabled endpoints return deterministic `503 feature_disabled`.
3. Capability contract stays OpenAPI-aligned in CI.

## Phase 13: OCR Rate-Limit Isolation + Memory Safety

Goal: prevent cross-tenant interference and long-running memory growth in OCR throttling.

Deliverables:

1. Make OCR rate-limit bucket operations lock-safe.
2. Ensure farm-scope isolation in throttling behavior.
3. Prune expired/stale scope buckets automatically.
4. Add regression tests for scope isolation and stale-state pruning.

Acceptance criteria:

1. Requests from one farm do not consume quota of another farm.
2. Expired idle scope buckets are removed over time.
3. All OCR parse/rate-limit tests and full CI suite remain green.

## Phase 14: Reference Snapshot Immutability Enforcement

Goal: prevent silent mutation of already-published snapshot versions.

Deliverables:

1. Detect conflicting re-imports for existing `(sourceSystem, sourceVersion)` by payload hash.
2. Return deterministic `409 reference_snapshot_conflict` for mismatched re-import attempts.
3. Add API/OpenAPI tests for conflict behavior.

Acceptance criteria:

1. Same payload re-import stays idempotent.
2. Different payload with same version is rejected.
3. Contract/documentation clearly reflects immutability guarantee.

## Phase 15: Reference Search Source-System Disambiguation

Goal: make reference search deterministic when the same `sourceVersion` exists across multiple source systems.

Deliverables:

1. Extend `GET /v1/reference/crops/search` and `GET /v1/reference/varieties/search` with optional `sourceSystem` query filter.
2. Apply source-system filtering in both DB-backed and bundled-fallback search flows.
3. Return deterministic `400 invalid_source_system` when blank `sourceSystem` is provided.
4. Return deterministic `404 reference_snapshot_not_found` when `(sourceVersion, sourceSystem)` has no matching data.
5. Add API/OpenAPI tests for filter behavior and persistence pass-through.

Acceptance criteria:

1. Search results can be pinned by `sourceVersion` and narrowed by `sourceSystem` without ambiguity.
2. DB path and fallback path return equivalent filter semantics.
3. CI bundle checks (`pytest`, `fadl-check`, `bundle-verify`) remain green.

## Phase 16: Reference Source Catalog for Ingestion Planning

Goal: make upstream crop/variety source selection explicit for operators and client apps.

Deliverables:

1. Add `GET /v1/reference/sources` endpoint with optional filters:
   - `entityType` (`crop_species` or `variety`)
   - `jurisdiction`
   - `sourceSystem`
2. Return deterministic source metadata:
   - source system code and display label
   - scope (`entities`, `jurisdictionScopes`)
   - authority URL/reference and cadence
   - linked ingest profile path (when available)
3. Extend `/v1/capabilities` with `referenceSourceCatalog`.
4. Add API/OpenAPI tests for endpoint behavior and capability discovery.

Acceptance criteria:

1. Product and ops teams can discover where variety data should be sourced for a target jurisdiction.
2. Endpoint filtering is deterministic and validates malformed filters with explicit errors.
3. CI bundle checks (`pytest`, `fadl-check`, `bundle-verify`) remain green.

## Phase 17: Reference Source Snapshot Status Visibility

Goal: let clients and operators verify which snapshot version is actually loaded per source system.

Deliverables:

1. Extend `GET /v1/reference/sources` with `includeSnapshotStatus` flag.
2. Add per-source `latestSnapshot` metadata in source-catalog responses when status is requested and available.
3. Add response-level `snapshotStatusAvailable` indicator.
4. Add API/OpenAPI tests for status-enabled and status-unavailable behavior.

Acceptance criteria:

1. Clients can fetch source recommendations and current loaded snapshot status in one call.
2. Status enrichment degrades gracefully when persistence is unavailable.
3. CI bundle checks (`pytest`, `fadl-check`, `bundle-verify`) remain green.

## Phase 18: Deterministic Source Ingestion Plan Endpoint

Goal: provide an executable source-ingestion order so clients do not guess which source to ingest first.

Deliverables:

1. Add `GET /v1/reference/source-plan` endpoint.
2. Require `entityType` and support:
   - `jurisdiction`
   - `productionProfile` (`organic`, `in_transition`, `conventional`)
   - `includeSnapshotStatus`
3. Return ordered plan steps with:
   - source system
   - human-readable selection reason
   - profile path/source reference
   - optional latest snapshot status
4. Add API/OpenAPI tests for ordering, validation, and feature-flag behavior.

Acceptance criteria:

1. For `entityType=variety&jurisdiction=RS`, plan prioritizes `RS_CATALOG` before EU-level sources.
2. For `entityType=variety&jurisdiction=SI`, plan prioritizes `EU_CATALOG`.
3. CI bundle checks (`pytest`, `fadl-check`, `bundle-verify`) remain green.

## Phase 19: Source Plan Capability Discovery and Gating

Goal: let clients discover and gate `GET /v1/reference/source-plan` independently from other reference endpoints.

Deliverables:

1. Extend `/v1/capabilities` with `referenceSourcePlan`.
2. Add dedicated source-plan feature flags:
   - `REFERENCE_SOURCE_PLAN_ENABLED`
   - `FARMRM_FEATURE_REFERENCE_SOURCE_PLAN`
3. Add dedicated source-plan min client version wiring:
   - `REFERENCE_SOURCE_PLAN_MIN_CLIENT_VERSION`
   - `FARMRM_MIN_CLIENT_VERSION_REFERENCE_SOURCE_PLAN`
4. Update API/OpenAPI tests for capabilities and feature-disabled behavior.

Acceptance criteria:

1. Capability payload exposes `referenceSourcePlan.enabled` and optional `minClientVersion`.
2. `/v1/reference/source-plan` returns deterministic `503 feature_disabled` when plan-specific flag is off.
3. CI bundle checks (`pytest`, `fadl-check`, `bundle-verify`) remain green.

## Phase 20: Source Profile Catalog API

Goal: expose ingestion profile metadata and CSV schema contracts through the API, so clients can prepare imports without reading repository files directly.

Deliverables:

1. Add `GET /v1/reference/source-profiles` endpoint with optional `sourceSystem` filter.
2. Return per-profile metadata:
   - source system
   - profile path/reference metadata
   - required and optional CSV headers for crops and varieties
   - example pipeline build command
3. Extend `/v1/capabilities` with `referenceSourceProfiles`.
4. Add dedicated source-profile feature flags/min-client-version env wiring.
5. Add API/OpenAPI tests for endpoint behavior and capability discovery.

Acceptance criteria:

1. Clients can discover profile requirements (`requiredHeaders`, `optionalHeaders`) via API.
2. Endpoint can be independently feature-gated (`503 feature_disabled`).
3. CI bundle checks (`pytest`, `fadl-check`, `bundle-verify`) remain green.

## Phase 21: Ingestion Readiness Check API

Goal: provide a deterministic pre-import validation gate so clients can detect profile/header/source-version issues before snapshot import.

Deliverables:

1. Add `POST /v1/reference/source-ingestion/check`.
2. Validate and return readiness for:
   - source system and source version format
   - resolved profile presence
   - required crops/varieties CSV headers
   - optional planning-context warnings (non-primary source for scope)
3. Extend `/v1/capabilities` with `referenceIngestionReadiness`.
4. Add dedicated readiness feature flag/min-client-version env wiring.
5. Add API/OpenAPI tests for endpoint behavior and feature gating.

Acceptance criteria:

1. API returns structured `errors`, `warnings`, and `checks` plus boolean `ready`.
2. Missing required headers are reported deterministically without side effects.
3. Endpoint can be independently gated (`503 feature_disabled`) and discovered in capabilities.

## Phase 22: Snapshot Import Capability Discovery and Gating

Goal: let clients discover and gate `POST /v1/reference/snapshots/import` independently from read-only reference endpoints.

Deliverables:

1. Extend `/v1/capabilities` with `referenceSnapshotImport`.
2. Add dedicated snapshot-import feature flags:
   - `REFERENCE_SNAPSHOT_IMPORT_ENABLED`
   - `FARMRM_FEATURE_REFERENCE_SNAPSHOT_IMPORT`
3. Add dedicated snapshot-import min client version wiring:
   - `REFERENCE_SNAPSHOT_IMPORT_MIN_CLIENT_VERSION`
   - `FARMRM_MIN_CLIENT_VERSION_REFERENCE_SNAPSHOT_IMPORT`
4. Gate `POST /v1/reference/snapshots/import` behind snapshot-import feature flag and return deterministic `503 feature_disabled` when disabled.
5. Add API/OpenAPI tests for capabilities wiring and feature-disabled behavior.

Acceptance criteria:

1. Capability payload exposes `referenceSnapshotImport.enabled` and optional `minClientVersion`.
2. `POST /v1/reference/snapshots/import` returns deterministic `503 feature_disabled` when import-specific flag is off.
3. CI bundle checks (`pytest`, `fadl-check`, `bundle-verify`) remain green.

## Phase 23: Ingestion Readiness Strict Header Mode

Goal: prevent false-positive readiness by allowing clients to opt into strict header-input enforcement before import.

Deliverables:

1. Extend `POST /v1/reference/source-ingestion/check` request with `requireHeaders` boolean.
2. In strict mode, require header input for relevant scope:
   - `entityType=variety` requires `varietiesCsvHeaders`
   - `entityType=crop_species` requires `cropsCsvHeaders`
   - unspecified `entityType` requires both
3. Always return deterministic required-header expectations in response checks:
   - `expectedCropsRequiredHeaders`
   - `expectedVarietiesRequiredHeaders`
4. Add API/OpenAPI tests for strict-mode error behavior.

Acceptance criteria:

1. Strict mode with missing relevant header input returns `ready=false` and explicit `missing_*_headers_input` errors.
2. Response `checks` includes expected required-header arrays regardless of strict mode.
3. CI bundle checks (`pytest`, `fadl-check`, `bundle-verify`) remain green.

## Phase 24: Snapshot Import Preview API

Goal: allow clients/operators to preview snapshot import validity and impact without persistence side effects.

Deliverables:

1. Add `POST /v1/reference/snapshots/import/preview`.
2. Validate snapshot payload shape with the same structural rules as import:
   - source system/version required
   - published date format
   - non-empty crops/varieties payload
3. Return deterministic preview diagnostics:
   - `ready`, `errors`, `warnings`
   - payload counts and duplicate URI detection
   - unresolved variety crop references
4. Extend `/v1/capabilities` with `referenceSnapshotImportPreview`.
5. Add dedicated preview feature flag/min-client-version wiring:
   - `REFERENCE_SNAPSHOT_IMPORT_PREVIEW_ENABLED`
   - `FARMRM_FEATURE_REFERENCE_SNAPSHOT_IMPORT_PREVIEW`
   - `REFERENCE_SNAPSHOT_IMPORT_PREVIEW_MIN_CLIENT_VERSION`
   - `FARMRM_MIN_CLIENT_VERSION_REFERENCE_SNAPSHOT_IMPORT_PREVIEW`
6. Add API/OpenAPI tests for preview path, capability discovery, and feature-disabled behavior.

Acceptance criteria:

1. Preview endpoint performs no DB writes and returns deterministic counts/diagnostics.
2. Unresolved variety crop references are surfaced as explicit preview errors.
3. Endpoint can be independently gated (`503 feature_disabled`) and discovered in capabilities.
4. CI bundle checks (`pytest`, `fadl-check`, `bundle-verify`) remain green.

## Phase 25: Snapshot Import Preview Hash Conflict Precheck

Goal: detect same-version payload conflicts before import by comparing preview payload hash with existing imported snapshot hash.

Deliverables:

1. Extend preview diagnostics with deterministic payload hash:
   - `checks.previewImportHashSha256`
2. Resolve existing imported snapshot for `(sourceSystem, sourceVersion)` when persistence is available.
3. Add deterministic version-state outcomes in preview:
   - same hash: warning `source_version_already_imported_same_payload`
   - different hash: error `source_version_conflicts_with_existing_payload`
4. Preserve existing latest-version context fields (`latestImportedSourceVersion`, `snapshotVersionAlreadyImported`).
5. Add API tests for same-payload and conflicting-payload cases.

Acceptance criteria:

1. Preview returns `ready=false` for same-version hash conflict without writing any records.
2. Preview returns `ready=true` with explicit warning for same-version same-payload replay.
3. CI bundle checks (`pytest`, `fadl-check`, `bundle-verify`) remain green.

## Phase 26: Duplicate URI Payload Hard Validation

Goal: prevent ambiguous or silently collapsed imports by treating duplicate crop/variety URIs in one snapshot payload as hard validation failures.

Deliverables:

1. Add duplicate URI hard validation to `POST /v1/reference/snapshots/import`:
   - `duplicate_crop_uri_in_payload` (`422`)
   - `duplicate_variety_uri_in_payload` (`422`)
2. Align `POST /v1/reference/snapshots/import/preview` readiness:
   - duplicate URIs produce preview errors and `ready=false`
3. Add API tests for import and preview duplicate-URI behavior.

Acceptance criteria:

1. Import requests with duplicate crop or variety URIs fail deterministically with explicit error code and URI list.
2. Preview flags the same duplicates as errors before import.
3. CI bundle checks (`pytest`, `fadl-check`, `bundle-verify`) remain green.

## Phase 27: Snapshot Version Diff API

Goal: let clients/operators compare two imported snapshot versions deterministically before switching pinned versions.

Deliverables:

1. Add `GET /v1/reference/snapshots/diff`.
2. Require and validate:
   - `sourceSystem`
   - `fromSourceVersion`
   - `toSourceVersion`
   - optional `entityType` (`all`, `crop_species`, `variety`)
3. Return deterministic diff summary for selected scope:
   - counts (`from`, `to`, `added`, `removed`, `changed`, `unchanged`)
   - sample URI lists (`added`, `removed`, `changed`)
4. Extend `/v1/capabilities` with `referenceSnapshotDiff`.
5. Add dedicated diff feature flag/min-client-version wiring:
   - `REFERENCE_SNAPSHOT_DIFF_ENABLED`
   - `FARMRM_FEATURE_REFERENCE_SNAPSHOT_DIFF`
   - `REFERENCE_SNAPSHOT_DIFF_MIN_CLIENT_VERSION`
   - `FARMRM_MIN_CLIENT_VERSION_REFERENCE_SNAPSHOT_DIFF`
6. Add API/OpenAPI tests for path contract, feature gating, and success behavior.

Acceptance criteria:

1. Diff endpoint returns stable counts and sample URIs for the same snapshots.
2. Missing snapshot versions return deterministic `404 reference_snapshot_not_found`.
3. Endpoint can be independently gated (`503 feature_disabled`) and discovered in capabilities.
4. CI bundle checks (`pytest`, `fadl-check`, `bundle-verify`) remain green.

## Phase 28: Source Profile Acquisition Guidance

Goal: make source onboarding operationally clear by exposing deterministic "where/how to fetch" metadata for each reference profile (especially variety feeds).

Deliverables:

1. Extend source profile metadata shape with acquisition guidance:
   - `entryPointUrl`
   - `requiresAuth`
   - optional `authHint`
   - `artifacts[]` (entity scope, URL, format, short note)
2. Populate acquisition metadata in bundled profiles:
   - `eu-catalog-2026.json`
   - `cpvo-2026.json`
   - `eppo-2026.json`
3. Extend `GET /v1/reference/source-profiles` response contract to include acquisition metadata.
4. Add API tests for acquisition metadata presence and CPVO auth requirement.
5. Update Part 3 spec narrative to include acquisition guidance contract.

Acceptance criteria:

1. `GET /v1/reference/source-profiles` returns `acquisition.entryPointUrl` and `acquisition.artifacts[]` for bundled profiles.
2. CPVO profile explicitly reports `acquisition.requiresAuth=true` and provides `authHint`.
3. OpenAPI/runtime schema alignment remains clean after contract update.
4. CI bundle checks (`pytest`, `fadl-check`, `bundle-verify`) remain green.

## Phase 29: Acquisition Coverage Validation in Readiness Check

Goal: prevent false-ready ingestion checks by verifying that selected source profile acquisition artifacts actually cover the requested entity scope.

Deliverables:

1. Extend `POST /v1/reference/source-ingestion/check` diagnostics with acquisition readiness fields:
   - `checks.acquisitionGuidanceAvailable`
   - `checks.acquisitionEntryPointUrl`
   - `checks.acquisitionRequiresAuth`
   - `checks.acquisitionArtifactEntityTypes`
   - `checks.missingAcquisitionEntityTypes`
2. Emit deterministic warning when source access needs credentials:
   - `source_access_requires_auth`
3. Fail readiness when explicit `entityType` has no matching acquisition artifact in selected profile:
   - `missing_acquisition_artifact_for_entity_type`
4. Add API tests for:
   - CPVO auth-required warning path
   - missing entity-type artifact failure path (`CPVO + crop_species`)
5. Update Part 3 spec narrative for acquisition coverage checks.

Acceptance criteria:

1. Readiness responses always include acquisition diagnostics when profile is resolved.
2. CPVO readiness includes `source_access_requires_auth` warning and `acquisitionRequiresAuth=true`.
3. `entityType=crop_species` against CPVO profile returns `ready=false` and `missing_acquisition_artifact_for_entity_type`.
4. CI bundle checks (`pytest`, `fadl-check`, `bundle-verify`) remain green.

## Phase 30: Full-Scope Acquisition Coverage Validation

Goal: eliminate false-ready checks when `entityType` is omitted by enforcing acquisition coverage for both crop/species and variety scopes.

Deliverables:

1. Update readiness coverage rule:
   - when `entityType` is omitted, require acquisition artifacts for both `crop_species` and `variety`
2. Keep deterministic diagnostics:
   - `checks.missingAcquisitionEntityTypes` lists missing scopes in stable order
3. Add API test for no-entityType case:
   - `CPVO` profile should fail readiness due to missing `crop_species` artifact scope
4. Update Part 3 spec narrative to explicitly describe full-scope behavior.

Acceptance criteria:

1. `POST /v1/reference/source-ingestion/check` with omitted `entityType` returns `ready=false` if either scope lacks acquisition artifacts.
2. `missingAcquisitionEntityTypes` reports deterministic missing scope list.
3. CI bundle checks (`pytest`, `fadl-check`, `bundle-verify`) remain green.

## Phase 31: Acquisition Fallback Recommendations

Goal: reduce operator ambiguity when readiness fails on acquisition scope by returning deterministic fallback source/profile suggestions.

Deliverables:

1. Extend `POST /v1/reference/source-ingestion/check` diagnostics for scope mismatches:
   - `checks.recommendedAcquisitionSources[]` with
     - `entityType`
     - `recommendedSourceSystems[]`
     - `recommendedProfileCodes[]`
2. Emit deterministic warning for scope mismatch recommendations:
   - `acquisition_guidance_scope_mismatch`
3. Derive recommendations from existing source plan priorities + available source profiles.
4. Add API tests for CPVO scope mismatch recommendations (`EPPO` / `eppo-2026`).
5. Update Part 3 spec narrative for fallback recommendation behavior.

Acceptance criteria:

1. Scope mismatch responses include non-empty `recommendedAcquisitionSources[]`.
2. Recommendations are deterministic for the same request inputs.
3. CI bundle checks (`pytest`, `fadl-check`, `bundle-verify`) remain green.

## Phase 32: Typed Readiness Checks Contract

Goal: stabilize client integration by replacing loosely-typed readiness diagnostics with an explicit schema while preserving existing JSON keys.

Deliverables:

1. Introduce typed readiness diagnostics model:
   - `ReferenceIngestionReadinessChecks`
2. Introduce typed fallback suggestion model:
   - `ReferenceIngestionRecommendedAcquisitionSource`
3. Change `ReferenceIngestionReadinessResponse.checks` from free-form map to typed model.
4. Keep wire compatibility:
   - existing `checks.*` keys remain present in JSON response.
5. Extend OpenAPI alignment tests to assert schema parity for new components.

Acceptance criteria:

1. Existing API behavior remains backward compatible for current `checks.*` fields.
2. OpenAPI exposes typed schemas for readiness checks and fallback recommendations.
3. CI bundle checks (`pytest`, `fadl-check`, `bundle-verify`) remain green.

## Phase 33: Readiness Checks Contract Versioning

Goal: make client parsing upgrades explicit by adding an in-payload readiness checks contract version.

Deliverables:

1. Add `checks.contractVersion` to `ReferenceIngestionReadinessChecks`.
2. Set a stable initial value (`1.0.0`) in readiness responses.
3. Add API tests asserting `checks.contractVersion`.
4. Update Part 3 narrative to document contract version field and semantics.

Acceptance criteria:

1. `POST /v1/reference/source-ingestion/check` responses always include `checks.contractVersion`.
2. Value is deterministic and stable (`1.0.0`) for this release line.
3. CI bundle checks (`pytest`, `fadl-check`, `bundle-verify`) remain green.

## Phase 34: Capabilities Contract Signaling

Goal: let clients discover readiness-check contract versions during capability bootstrap before parsing endpoint payloads.

Deliverables:

1. Extend `/v1/capabilities` response with contract metadata:
   - `contracts.referenceIngestionReadinessChecks.version`
2. Keep value aligned with readiness payload contract version (`1.0.0`).
3. Add API tests asserting contracts metadata presence and value.
4. Extend OpenAPI alignment tests for new capabilities contract schemas.
5. Update Part 3 and server README to document capability-time contract signaling.

Acceptance criteria:

1. `/v1/capabilities` always includes `contracts.referenceIngestionReadinessChecks.version`.
2. Value is stable and matches readiness payload contract version.
3. CI bundle checks (`pytest`, `fadl-check`, `bundle-verify`) remain green.

## Phase 35: Readiness Contract Negotiation Hint

Goal: allow clients to declare expected readiness-check contract version and receive deterministic compatibility diagnostics.

Deliverables:

1. Extend `POST /v1/reference/source-ingestion/check` request with:
   - `expectedChecksContractVersion` (optional semantic version string)
2. Extend `checks` diagnostics with:
   - `expectedChecksContractVersion`
   - `contractVersionMatch`
3. Emit deterministic warning on mismatch:
   - `checks_contract_version_mismatch`
4. Validate expected version format and return deterministic errors for invalid values.
5. Add API tests for:
   - match path
   - mismatch warning path
   - invalid expected-version errors
6. Update Part 3 + README narrative.

Acceptance criteria:

1. Clients can provide expected contract version without breaking readiness behavior.
2. Mismatch is signaled deterministically without converting readiness to failure.
3. Invalid expected version input returns deterministic validation errors.
4. CI bundle checks (`pytest`, `fadl-check`, `bundle-verify`) remain green.
