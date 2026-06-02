# OF Platform FastAPI Runtime For OFARM API Contract

This is the OF Platform FastAPI runtime that implements the OpenAPI surface in:

`./specs/api/v1/openapi-farm-rm.yaml`

Refresh or verify the checked-in snapshot with:

```bash
make openapi-export
make openapi-export-check
```

## Selected endpoint families

This opening list is intentionally non-exhaustive. It highlights representative or historically foundational endpoints, not the full current runtime surface.

The live runtime and static contract now also cover broader route families such as:

- `/v1/advisor/*`
- `/v1/investigator/*`
- `/v1/operations/*` and `/v1/control-center/*`
- field-passport and derived field projections under `/v1/fields/*` and `/v1/farms/{farmUri}/scout-priority-queue`
- AI OCR promotion and intake flows under `/v1/ai/ocr/*`, `/v1/documents/*`, and `/v1/intake/*`
- inventory review and repair surfaces under `/v1/inventory/review-items/*`

For current contract truth, prefer:

- `specs/api/v1/openapi-farm-rm.yaml`
- `specs/api/v1/server/fastapi/app/main.py`
- `specs/api/v1/server/fastapi/tests/test_openapi_contract_alignment.py`
- `docs/ai/onboarding/40-api-and-data-contracts.md`

1. `POST /v1/suitability/evaluate-seed`
2. `POST /v1/suitability/evaluate-equipment`
3. `POST /v1/planning/scenario/evaluate`
4. `POST /v1/risk/contamination/evaluate`
5. `POST /v1/compliance/claims/validate`
6. `GET /v1/assets/obligations/due`
7. `GET /v1/economics/fields/{fieldId}/profitability`
8. `POST /v1/reporting/render`
9. `POST /v1/telematics/segments/classify`
10. `POST /v1/coverage/assess`
11. `POST /v1/fuel-allocation/evaluate`
12. `POST /v1/labels/localized/resolve`
13. `GET /v1/commerce/partners/{partnerId}/price-history`
14. `POST /v1/tasks/dispatch`
15. `POST /v1/tasks/dispatch/{taskId}/complete`
16. `POST /v1/warehouse/lot-moves`
17. `GET /v1/compliance/dossiers/{claimId}`
18. `GET /v1/reporting/packs`
19. `POST /v1/reporting/export-bundles`
20. `GET /v1/assets/overview`
21. `POST /v1/assets/service-readiness/evaluate`
22. `POST /v1/assets/obligations/reminders/trigger`
23. `POST /v1/assets/obligations/reminders/status`
24. `POST /v1/field-ops/planting-events`
25. `POST /v1/field-ops/mechanical-weeding-events`
26. `POST /v1/field-ops/cover-crop-management-events`
27. `POST /v1/field-ops/tillage-events`
28. `POST /v1/field-ops/fertilizer-application-events`
29. `POST /v1/field-ops/plant-protection-application-events`
30. `POST /v1/field-ops/replant-assessments`
31. `POST /v1/reporting/crop-stand-counts`
32. `POST /v1/reporting/weed-pressure-assessments`
33. `POST /v1/reporting/pest-trap-counts`
34. `POST /v1/reporting/remote-sensing-index-observations`
35. `POST /v1/compliance/complaints`
36. `GET /v1/templates/projections/{templateId}`
37. `GET /v1/reference/snapshots`
38. `GET /v1/reference/sources`
39. `GET /v1/reference/source-plan`
40. `GET /v1/reference/source-profiles`
41. `POST /v1/reference/source-ingestion/check`
42. `GET /v1/ai/ocr/metrics`
43. `POST /v1/reference/snapshots/import`
44. `GET /v1/capabilities`
45. `POST /v1/reference/snapshots/import/preview`
46. `GET /v1/reference/snapshots/diff`

## Wiring

The first five validation endpoints call reference validators directly:

- `./specs/v0.3/validation/bin/evaluate-seed-suitability.sh`
- `./specs/v0.4/validation/bin/evaluate-equipment-suitability.sh`
- `./specs/v0.4/validation/bin/evaluate-scenario-risk.sh`
- `./specs/v0.2/validation/bin/evaluate-contamination-risk.sh`
- `./specs/v0.1/validation/bin/validate-claim.sh`

The v1.5-style interconnectedness endpoints are computed in Python in this runtime:
- telematics segment classification
- coverage estimation from distance and working width
- fuel allocation closure and diagnostics
- multilingual label resolution

When `FARM_RM_DATABASE_URL` is configured and `psycopg` is installed, those endpoints also persist into v1.5 tables:
- `equipment_activity_segment`
- `coverage_assessment`
- `fuel_allocation_batch`
- `fuel_allocation_line`
- `cost_ledger_entry` (fuel category when `farmUri` is provided)

The v1.6 API-surface endpoints persist/query through:
- `counterparty`, `commercial_offer`, `contract`, `delivery`, `transport_leg` (partner history read model)
- `operation_task_dispatch`
- `operation_task_completion`
- `warehouse_lot_move`
- `event_record` (audit events for dispatch/completion/warehouse moves/dossier access)

The v1.7 agronomy endpoints persist into:
- `planting_event`
- `mechanical_weeding_event`
- `cover_crop_management_event`
- `tillage_event`
- `fertilizer_application_event`
- `plant_protection_application_event`
- `crop_stand_count_observation`
- `weed_pressure_assessment_observation`
- `pest_trap_count_observation`
- `remote_sensing_index_observation`
- `replant_need_assessment`
- `inventory_receipt_import`
- `inventory_receipt_line_item`
- `complaint_log_entry`
- `reference_source_snapshot`
- `reference_crop_entry`
- `reference_variety_entry`

Supporting audit and evidence rows are also written for parts of that surface:

- planting and mechanical-weeding routes also persist `executed_operation`,
  `evidence_record`, `executed_operation_evidence`, and `event_record`
- crop-stand counts, weed-pressure assessments, and replant assessments also
  persist `event_record`

Additional DB-backed behavior:
- contamination risk assessments can be persisted into `contamination_risk_event` + `contamination_risk_evidence`
- field profitability endpoint can resolve from `cost_ledger_entry` and `revenue_ledger_entry` (period filtered)
- asset overview can resolve from `asset`, `asset_category`, `equipment_instance`, and `legal_obligation`
- asset service-readiness evaluations and reminder triggering can persist into `event_record` + `reminder_event`

To preload demo data for these modules, run:

```bash
export DATABASE_URL='postgresql://user:pass@localhost:5432/farmrm'
./specs/v0.6/sql/bin-run-v1_6-migrations.sh
```

`FARM_RM_DATABASE_URL` example:

```bash
export FARM_RM_DATABASE_URL='postgresql://user:pass@localhost:5432/farmrm'
```

For end-to-end persistence:
1. Call `/v1/telematics/segments/classify` first (so segment URIs exist in DB).
2. Use those segment URIs in `/v1/fuel-allocation/evaluate` input segments.
3. Provide `farmUri` in fuel-allocation input to post `cost_ledger_entry` rows.

Claim validation now uses jurisdiction rule packs from:
- `./specs/v0.4/regulatory/rulepacks/`

## Run

```bash
cd "./specs/api/v1/server/fastapi"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

Open docs:

- `http://localhost:8080/docs`
- `http://localhost:8080/openapi.json`

## Test

```bash
cd "./specs/api/v1/server/fastapi"
source .venv/bin/activate
./run-tests.sh
```

SI official-form golden baseline:

```bash
cd "./specs/api/v1/server/fastapi"
source .venv/bin/activate
PYTHONPATH=. python scripts/update_si_official_golden.py --check
PYTHONPATH=. python scripts/update_si_official_golden.py
```

## Notes

- This is a reference runtime and contract surface, not a production SaaS service.
- Due-obligations and reminder surfaces can run from database-backed state when persistence is enabled, and fall back to checked-in examples when it is not.
- Profitability endpoint uses DB read model when available and falls back to example artifacts.
- Reporting endpoint resolves template/layout from report packs in:
  `./specs/v0.4/regulatory/report-packs/`
- Reporting packs now carry authority export profiles used by:
  `POST /v1/reporting/export-bundles`
- Reference snapshot import tooling is available in:
  `tools/reference_snapshot_pipeline.py`
  with sample input files and usage in:
  `specs/v0.8/reference-ingest/README.md`
- Reference snapshot imports enforce version immutability:
  conflicting re-import for same `sourceSystem + sourceVersion` returns `409`.
- Reference search endpoints support optional `sourceVersion` + `sourceSystem` pinning and return
  `X-Reference-Source-Version` + dynamic `ETag` for deterministic client caching.
- Reference snapshot catalog endpoint (`GET /v1/reference/snapshots`) lists
  available snapshot versions for client-side pinning/selection workflows.
- Reference source catalog endpoint (`GET /v1/reference/sources`) lists
  authoritative source systems and ingest profile paths for crop/variety reference imports,
  and can include latest per-source snapshot status via `includeSnapshotStatus=true`.
- Reference source planning endpoint (`GET /v1/reference/source-plan`) returns
  deterministic prioritized ingestion order by `entityType`, `jurisdiction`, and `productionProfile`.
- Reference source profiles endpoint (`GET /v1/reference/source-profiles`) returns
  profile metadata, expected CSV headers, and source acquisition guidance
  (`entryPointUrl`, auth requirement, artifact fetch hints) for ingestion pipeline execution.
- Reference source ingestion readiness endpoint (`POST /v1/reference/source-ingestion/check`) validates
  profile/source/version/header readiness before import submission, including optional strict mode
  (`requireHeaders=true`) that fails readiness when required header input is missing, plus
  acquisition-coverage diagnostics (entry point/auth/artifact scope), entity-scope validation,
  and deterministic fallback source/profile recommendations on scope mismatch.
  Readiness diagnostics are exposed via typed `checks` contract models for stable client parsing,
  including explicit `checks.contractVersion`.
  Clients may optionally send `expectedChecksContractVersion` and get compatibility diagnostics
  via `checks.contractVersionMatch` + warning `checks_contract_version_mismatch`.
- Reference snapshot import endpoint (`POST /v1/reference/snapshots/import`) can be independently
  feature-gated via `REFERENCE_SNAPSHOT_IMPORT_ENABLED` / `FARMRM_FEATURE_REFERENCE_SNAPSHOT_IMPORT`
  and rejects duplicate crop/variety URIs inside a single payload.
- Reference snapshot import preview endpoint (`POST /v1/reference/snapshots/import/preview`) is side-effect free
  and can be independently feature-gated via
  `REFERENCE_SNAPSHOT_IMPORT_PREVIEW_ENABLED` / `FARMRM_FEATURE_REFERENCE_SNAPSHOT_IMPORT_PREVIEW`;
  it also reports same-version hash replay/conflict diagnostics before import.
- Reference snapshot diff endpoint (`GET /v1/reference/snapshots/diff`) compares two imported versions for a
  source system and returns deterministic added/removed/changed URI summaries for crops and varieties.
- OCR metrics endpoint (`GET /v1/ai/ocr/metrics`) exposes aggregate request
  counts, status/error distributions, and latency percentiles for QA/rollout checks.
- My Farm dashboard routes under `/v1/dashboard/my-farm/*` now cover summary,
  module drilldown, issue explanation, trace, recompute, and metrics surfaces.
- The My Farm dashboard metrics endpoint (`GET /v1/dashboard/my-farm/metrics`) exposes
  aggregate summary latency, HTTP/error distributions, summary freshness/state counts,
  per-module freshness counts, and source-slice failure counts for live-summary
  observability and materialization-threshold checks.
- Repo-local threshold guard for My Farm summary metrics is available in:
  `specs/api/v1/server/fastapi/scripts/check_my_farm_dashboard_metrics.py`
  For example:
  ```bash
  cd "./specs/api/v1/server/fastapi"
  python3 scripts/check_my_farm_dashboard_metrics.py \
    --base-url http://127.0.0.1:8080 \
    --min-total-requests 20 \
    --max-p95-ms 750 \
    --max-p99-ms 1500 \
    --max-http-5xx-count 0 \
    --max-noncurrent-rate 0.15 \
    --max-module-noncurrent-rate reporting=0.10 \
    --max-source-failure-count reporting.render_derivation=0
  ```
- Field-passport local demo bootstrap is available for the Slovenia demo farm:
  ```bash
  cd "./specs/api/v1/server/fastapi"
  python3 scripts/bootstrap_field_passport_local_demo.py \
    --postgres-url postgresql://localhost:5432/farm_rm \
    --base-url http://127.0.0.1:8080 \
    --farm-uri https://data.demo.si/farm-rm/v1/farm/SI/FARM-001
  ```
  For SQL-only bootstrap without replaying the checked-in API importers:
  ```bash
  cd "./specs/api/v1/server/fastapi"
  python3 scripts/bootstrap_field_passport_local_demo.py \
    --postgres-url postgresql://localhost:5432/farm_rm \
    --skip-api-imports
  ```
  This hydrates `FARM-001` / `FIELD-7` with one authority link, one compliance geometry snapshot,
  one declaration snapshot folded into `passport.cropContext`, one non-blocking overlay fact,
  one current-day daily-condition row, one demo input material, and two material lots with
  `authorized` / `rejected` input-authorization decisions so:
  - `GET /v1/fields/{fieldUri}/passport` returns meaningful local data
  - `POST /v1/fields/{fieldUri}/passport/evaluate-daily` returns meaningful local data
  - `POST /v1/fields/{fieldUri}/passport/evaluate-action` can be smoked with:
    - `actionCode=irrigation_event` for a candidate-free `allow`
    - `materialLotUri=https://data.demo.si/farm-rm/v1/material-lot/SI/INPUT-FIELD-PASSPORT-HERB-ALLOW-001`
      for a pesticide `allow`
    - `materialLotUri=https://data.demo.si/farm-rm/v1/material-lot/SI/INPUT-FIELD-PASSPORT-HERB-BLOCK-001`
      for a pesticide `block`
  The bootstrap script applies the field-passport migration and demo seed first,
  then replays the five checked-in field-passport importer demos through the
  live API unless `--skip-api-imports` is set. It also honors
  `FARM_RM_IMPORT_BEARER_TOKEN` for auth-enabled local backends.
- Field-passport core facts can also be appended through the API for an
  existing farm-scoped field:
  - `POST /v1/fields/{fieldUri}/passport/authority-links`
  - `POST /v1/fields/{fieldUri}/passport/geometry-snapshots`
  - `POST /v1/fields/{fieldUri}/passport/declaration-snapshots`
  - `POST /v1/fields/{fieldUri}/passport/overlay-facts`
  - `POST /v1/fields/{fieldUri}/passport/daily-conditions`
- Public Slovenia overlay/control-layer archives can now be inventoried into a
  normalized source catalog before any spatial intersection work:
  ```bash
  cd "./specs/api/v1/server/fastapi"
  python3 scripts/prepare_si_public_overlay_catalog.py \
    --source ../../../inbox/Kontrolni_sloji_2024.rar \
    --catalog-csv /tmp/kontrolni_sloji_2024_catalog.csv \
    --mapping-template-csv /tmp/kontrolni_sloji_2024_mapping.csv
  ```
  The catalog records:
  - physical shapefile bundles and DBF schema/sample attributes
  - workbook-defined logical control layers and `WHERE` selectors
  - a human-fill mapping template for canonical `overlayCode` /
    `severityCode` / `regimeCode` alignment before spatial intersection into
    `FIELD.field_overlay_fact`
  A conservative suggestion pass is also available for the catalog rows:
  ```bash
  cd "./specs/api/v1/server/fastapi"
  python3 scripts/suggest_si_public_overlay_mappings.py \
    --catalog-csv /tmp/kontrolni_sloji_2024_catalog.csv \
    --output-csv /tmp/kontrolni_sloji_2024_mapping_suggestions.csv
  ```
  This only suggests mappings for high-confidence public layers and leaves the
  rest in `manual_review` status. It does not fabricate parcel-level overlay
  facts or replace a real spatial intersection step.
  When the PostGIS staging database does not contain the Farm RM app tables,
  export the current `gerk_pid -> field_uri` map first:
  ```bash
  cd "./specs/api/v1/server/fastapi"
  PYTHONPATH="$(pwd)" ./.venv/bin/python scripts/export_field_gerk_map_csv.py \
    --postgres-url postgresql://localhost:5432/farm_rm \
    --output-csv /tmp/farm_rm_field_gerk_map.csv
  ```
  A PostGIS staging planner is also available to turn reviewed mapping rows
  into:
  - staging SQL
  - `shp2pgsql` load commands
  - a load manifest with prerequisite checks
  ```bash
  cd "./specs/api/v1/server/fastapi"
  python3 scripts/plan_si_public_overlay_postgis_stage.py \
    --source ../../../inbox/Kontrolni_sloji_2024.rar \
    --catalog-csv /tmp/kontrolni_sloji_2024_catalog.csv \
    --mapping-csv /tmp/kontrolni_sloji_2024_mapping_suggestions.csv \
    --field-map-csv /tmp/farm_rm_field_gerk_map.csv \
    --output-json /tmp/kontrolni_sloji_2024_postgis_stage_plan.json \
    --output-sql /tmp/kontrolni_sloji_2024_postgis_stage.sql \
    --output-shell /tmp/kontrolni_sloji_2024_postgis_stage.sh \
    --extract-dir /tmp/kontrolni_sloji_2024_stage_src \
    --postgres-url postgresql://localhost:5433/farm_rm_overlay_stage
  ```
  The planner does not require PostGIS to be installed in order to generate the
  plan, but it will report whether:
  - PostgreSQL is reachable
  - `postgis` is available and installed
  - `shp2pgsql` is available on the machine
  When `.cpg` files are present in the public archive, the generated
  `shp2pgsql` commands preserve the declared DBF encoding automatically, for
  example `CP1250` for the public `Kontrolni_sloji_2024` bundle.
  Once the overlay tables are staged and a GERK archive is available, a
  follow-on adapter can stage the GERK polygons and emit normalized
  `FIELD.field_overlay_fact` CSV:
  ```bash
  cd "./specs/api/v1/server/fastapi"
  PYTHONPATH="$(pwd)" ./.venv/bin/python scripts/prepare_si_field_overlay_facts_from_postgis_stage.py \
    --postgres-url postgresql://localhost:5433/farm_rm_overlay_stage \
    --gerk-source "/Users/einstein/Library/Developer/CoreSimulator/Devices/.../Library/Application Support/FarmanLiteiOS/Gerk" \
    --output-csv /tmp/si_field_overlay_facts_beta_20260309.csv
  ```
  For Farman Lite simulator caches, the output is intentionally marked as
  `beta_temporary_local_cache` in `attributes_json` and `notes`, while still
  preserving the official RKG archive name and URL from `metadata.json`.
  To make the beta CSV import-friendly, collapse canonical duplicates first:
  ```bash
  cd "./specs/api/v1/server/fastapi"
  PYTHONPATH="$(pwd)" ./.venv/bin/python scripts/collapse_field_overlay_facts_csv.py \
    --input-csv /tmp/si_field_overlay_facts_beta_20260309.csv \
    --output-csv /tmp/si_field_overlay_facts_beta_collapsed_20260309.csv
  ```
  The collapsed CSV:
  - groups by field + canonical overlay key
  - rounds `coverage_pct` to the API's persisted precision
  - preserves contributing logical-layer evidence in `attributes_json`
  These are append-only writes for all five non-evaluation fact families the
  passport projection reads directly. Upstream population of those facts is
  still missing; the local demo bootstrap remains useful for seeded dev data.
- Field-passport advisory read models now cover phases 2 through 6:
  - `GET /v1/fields/{fieldUri}/spray-window`
  - `GET /v1/fields/{fieldUri}/plant-health/relevance`
  - `GET /v1/fields/{fieldUri}/water-stewardship`
  - `GET /v1/fields/{fieldUri}/irrigation-readiness`
  - `GET /v1/fields/{fieldUri}/eo-anomaly`
  - `GET /v1/fields/{fieldUri}/phenology-status`
  - `GET /v1/fields/{fieldUri}/benchmark-context`
  - `GET /v1/fields/{fieldUri}/explainability-summary`
  - `GET /v1/fields/{fieldUri}/regional-comparison`
  - `GET /v1/fields/{fieldUri}/climate-adaptation-summary`
  - `GET /v1/fields/{fieldUri}/climate-suitability-outlook`
  - `GET /v1/fields/{fieldUri}/climate-indicator-trends`
  - `GET /v1/fields/{fieldUri}/climate-plan-tab`
  The phase-5 and phase-6 endpoints are read-only and intentionally reuse
  existing passport, water-stewardship, climate-hazard, EO, pedoclimatic,
  crop-adaptation, and variety-risk seams. Phase 6 now prefers stored
  `FIELD.field_climate_projection_fact` and
  `FIELD.field_climate_adaptation_signal` rows when present, and falls back to
  the older climate-hazard / pedoclimatic reuse path otherwise. The fallback
  path remains an honest cross-horizon advisory layer instead of inventing
  precise climate-planning fidelity.
  Source-native phase-6 scaffolding now exists under
  `specs/v0.8/reference-ingest/profiles/` and
  `specs/v0.4/regulatory/rulepacks/`, but it is intentionally not wired into
  `GET /v1/reference/source-profiles` because that catalog remains limited to
  crop/variety reference-snapshot intake.
- A narrow source-native climate producer path now exists for phase 6:
  - export a field-to-climate geography mapping CSV from the app DB using the
    latest pedoclimatic `region_code` evidence:
    `specs/api/v1/server/fastapi/scripts/export_field_climate_geography_map_csv.py`
  - export a Slovenia-specific field-to-climate geography mapping CSV from the
    official GeoHub statistical-region layer using staged GERK geometry:
    `specs/api/v1/server/fastapi/scripts/export_si_field_climate_geography_map_csv.py`
  - prepare field-scoped normalized climate facts directly from the official
    ARSO/OPSI 12 km ZIP bundle by sampling the grid cell containing each field
    centroid:
    `specs/api/v1/server/fastapi/scripts/prepare_arso_opsi_12km_field_climate_projection_facts.py`
  - validate a local climate intake bundle, including operator review of local
    derivation vs publication rights:
    `specs/api/v1/server/fastapi/scripts/validate_si_climate_intake_bundle.py`
  - normalize already-downloaded ARSO/C3S-style long-table extracts into
    `FIELD.field_climate_projection_fact` CSV:
    `specs/api/v1/server/fastapi/scripts/prepare_si_climate_projection_facts_csv.py`
  - derive `FIELD.field_climate_adaptation_signal` CSV from normalized
    projection facts:
    `specs/api/v1/server/fastapi/scripts/derive_field_climate_adaptation_signals_csv.py`
  This is intentionally an offline prep path, not a live downloader. It
  expects a local source extract plus a field-to-geography mapping.
- Field-passport history is also publicly readable for the seven append-only
  fact families that need rerun-safe producer comparison:
  - `GET /v1/fields/{fieldUri}/passport/declaration-snapshots`
  - `GET /v1/fields/{fieldUri}/passport/overlay-facts`
  - `GET /v1/fields/{fieldUri}/passport/daily-conditions`
  - `GET /v1/fields/{fieldUri}/passport/climate-projection-facts`
  - `GET /v1/fields/{fieldUri}/passport/climate-adaptation-signals`
  - `GET /v1/fields/{fieldUri}/passport/benchmark-context-facts`
  - `GET /v1/fields/{fieldUri}/passport/explainability-signals`
  These routes expose current field-scoped fact history without coupling CSV
  importers directly to persistence reads.
- Minimal rerun-safe normalized CSV importers now exist for all nine
  non-evaluation field-passport fact families:
  - authority links:
    `specs/api/v1/server/fastapi/scripts/import_field_authority_links.py`
  - geometry snapshots:
    `specs/api/v1/server/fastapi/scripts/import_field_geometry_snapshots.py`
  - declaration snapshots:
    `specs/api/v1/server/fastapi/scripts/import_field_declaration_snapshots.py`
  - overlay facts:
    `specs/api/v1/server/fastapi/scripts/import_field_overlay_facts.py`
  - daily conditions:
    `specs/api/v1/server/fastapi/scripts/import_field_daily_conditions.py`
  - climate projection facts:
    `specs/api/v1/server/fastapi/scripts/import_field_climate_projection_facts.py`
  - climate adaptation signals:
    `specs/api/v1/server/fastapi/scripts/import_field_climate_adaptation_signals.py`
  - benchmark context facts:
    `specs/api/v1/server/fastapi/scripts/import_field_benchmark_context_facts.py`
  - explainability signals:
    `specs/api/v1/server/fastapi/scripts/import_field_explainability_signals.py`
  Each importer posts through the canonical writer endpoints, reads the live
  passport or the matching history route first, and skips already-present
  identical facts on rerun instead of writing duplicate rows blindly.
- A source-native benchmark prep and validation path is now available too:
  - normalize already-downloaded SURS / Eurostat / JRC-style long-table
    extracts into `FIELD.field_benchmark_context_fact` CSV:
    `specs/api/v1/server/fastapi/scripts/prepare_si_field_benchmark_context_facts_csv.py`
  - validate a local benchmark intake bundle, including operator review of
    local derivation vs publication rights:
    `specs/api/v1/server/fastapi/scripts/validate_si_benchmark_intake_bundle.py`
  - derive `FIELD.field_explainability_signal` CSV from normalized benchmark
    facts plus operator-provided parcel-state context under an explicit policy:
    `specs/api/v1/server/fastapi/scripts/derive_field_benchmark_explainability_signals_csv.py`
  This path intentionally reuses the same field-to-geography mapping CSV shape
  as the climate prep seam, so the official/statistical-region mapping tools
  can be shared until a benchmark-specific geography exporter is needed.
- A conservative eRKG declaration prep adapter is also available:
  - `specs/api/v1/server/fastapi/scripts/prepare_erkg_last_meeting_declaration_csv.py`
  It converts an authenticated `Izvoz grafike GERK-ov` ZIP into an import-ready
  declaration-snapshot CSV without faking missing source fields. By default it:
  - maps `declaredUseCode` from `RABA_ID`
  - infers `seasonCode` from the supplied or derived declaration date
  - emits `productionStatus=unknown`
  - leaves `declaredAreaHa` blank unless the operator explicitly selects
    `--area-basis graph` or `--area-basis nup`
- Checked-in demo CSVs exist for the seven field-passport importers that were
  already part of the local demo/bootstrap path:
  - `specs/api/v1/server/fastapi/examples/field-authority-links-demo.csv`
  - `specs/api/v1/server/fastapi/examples/field-geometry-snapshots-demo.csv`
  - `specs/api/v1/server/fastapi/examples/field-declaration-snapshots-demo.csv`
  - `specs/api/v1/server/fastapi/examples/field-overlay-facts-demo.csv`
  - `specs/api/v1/server/fastapi/examples/field-daily-conditions-demo.csv`
  - `specs/api/v1/server/fastapi/examples/field-climate-projection-facts-demo.csv`
  - `specs/api/v1/server/fastapi/examples/field-climate-adaptation-signals-demo.csv`
  The new benchmark/explainability importers intentionally start from
  operator-produced normalized CSV instead of checked-in demo payloads.
- Checked-in demo source inputs also exist for the new climate prep path:
  - `specs/api/v1/server/fastapi/examples/field-climate-geography-mapping-demo.csv`
  - `specs/api/v1/server/fastapi/examples/si-climate-projection-source-demo.csv`
  - `specs/api/v1/server/fastapi/examples/climate-source-license-review-demo.json`
- A source-native ARSO daily-conditions prep adapter is also available:
  - script:
    `specs/api/v1/server/fastapi/scripts/prepare_arso_daily_conditions_csv.py`
  - example field-to-station mapping:
    `specs/api/v1/server/fastapi/examples/field-daily-conditions-arso-stations-demo.csv`
  It converts official ARSO surface observation XML feeds into the normalized
  daily-condition CSV contract already consumed by
  `scripts/import_field_daily_conditions.py`.
- Example ARSO prep run:
  ```bash
  cd "./specs/api/v1/server/fastapi"
  python3 scripts/prepare_arso_daily_conditions_csv.py \
    --mapping-csv examples/field-daily-conditions-arso-stations-demo.csv \
    --output-csv /tmp/arso_daily_conditions.csv
  ```
  Mapping CSV rules:
  - required: `field_uri`
  - optional: `crop_instance_uri`
  - provide either:
    - `station_code` (for official ARSO station-code URL construction), or
    - `station_xml_url` (for an explicit official feed URL)
  The current adapter is intentionally conservative:
  - it maps official ARSO point observations into generic daily readiness
    codes for spray, nutrient spreading, irrigation, and scouting
  - it does not claim a field-specific agronomic model or replace future
    remote-sensing / overlay-derived daily-condition producers
- A reusable official ARSO station-catalog helper is also available:
  - script:
    `specs/api/v1/server/fastapi/scripts/prepare_arso_station_catalog_csv.py`
  It resolves station titles and coordinates from the official ARSO XML feeds
  and emits a catalog CSV with:
  - `station_code`
  - `station_xml_url`
  - `station_title`
  - `station_lon`
  - `station_lat`
- Example station-catalog run:
  ```bash
  cd "./specs/api/v1/server/fastapi"
  python3 scripts/prepare_arso_station_catalog_csv.py \
    --station-code NOVA-GOR \
    --station-code POSTOJNA \
    --station-code LJUBL-ANA_BEZIGRAD \
    --station-code NOVO-MES \
    --output-csv /tmp/arso-station-catalog.csv
  ```
- A ranked station-fit diagnostic is also available:
  - script:
    `specs/api/v1/server/fastapi/scripts/diagnose_field_station_candidate_fit.py`
  It combines:
  - farm-scoped field URIs from the local DB
  - field centroids from a local eRKG GERK export ZIP
  - a prepared ARSO station catalog CSV
  and emits ranked candidate stations per field with explicit distances.
  By default it now resolves the same checked-in RealFarm weather policy and
  reviewed station-mapping asset as the daily bootstrap, so the selected row in
  the audit CSV matches the operator default instead of always meaning
  “nearest distance wins”.
- Example station-fit diagnostic run:
  ```bash
  cd "./specs/api/v1/server/fastapi"
  python3 scripts/diagnose_field_station_candidate_fit.py \
    --postgres-url postgresql://localhost:5432/farm_rm \
    --farm-uri https://data.example/farm-rm/v1/farm/SI/REALFARM-001 \
    --geometry-source-zip "../../inbox/RealFarm/Izvoz 20260310-0335 fe08957c.zip" \
    --candidate-station-csv /tmp/arso-station-catalog.csv \
    --output-csv /tmp/realfarm-station-fit.csv \
    --top-k 3 \
    --max-selected-distance-km 20
  ```
  Default-policy review output now includes:
  - `station_mapping_asset_id=si-realfarm-reviewed-station-map-v1`
  - selected rows with `status=reviewed_assignment_selected`
  - `mapping_mode=reviewed_field_station_proxy`
  - `selection_basis=operator_reviewed_assignment`
  Explicit overrides are still available:
  - `--station-mapping-asset-id`
  - `--ignore-station-mapping-asset`
- Example importer runs:
  ```bash
  cd "./specs/api/v1/server/fastapi"
  python3 scripts/import_field_authority_links.py \
    --base-url http://127.0.0.1:8080 \
    --csv examples/field-authority-links-demo.csv \
    --farm-uri https://data.demo.si/farm-rm/v1/farm/SI/FARM-001

  python3 scripts/import_field_geometry_snapshots.py \
    --base-url http://127.0.0.1:8080 \
    --csv examples/field-geometry-snapshots-demo.csv \
    --farm-uri https://data.demo.si/farm-rm/v1/farm/SI/FARM-001

  python3 scripts/import_field_declaration_snapshots.py \
    --base-url http://127.0.0.1:8080 \
    --csv examples/field-declaration-snapshots-demo.csv \
    --farm-uri https://data.demo.si/farm-rm/v1/farm/SI/FARM-001

  python3 scripts/prepare_erkg_last_meeting_declaration_csv.py \
    --zip "/path/to/Izvoz 20260310-0335 fe08957c.zip" \
    --meeting-pdf "/path/to/RKG_Zapisnik_100730702_2842476.pdf" \
    --output-csv /tmp/field-declaration-snapshots-erkg.csv \
    --field-uri-template https://data.example/farm-rm/v1/field/SI/GERK-{gerk_pid}

  python3 scripts/bootstrap_realfarm_local_profile.py \
    --postgres-url postgresql://localhost:5432/farm_rm \
    --zip "inbox/RealFarm/Izvoz 20260310-0335 fe08957c.zip" \
    --meeting-pdf "inbox/RealFarm/RKG_Zapisnik_100730702_2842476.pdf"

  python3 scripts/bootstrap_realfarm_source_documents.py \
    --base-url http://127.0.0.1:8081 \
    --bearer-token "<local-jwt>" \
    --zip "inbox/RealFarm/Izvoz 20260310-0335 fe08957c.zip" \
    --meeting-pdf "inbox/RealFarm/RKG_Zapisnik_100730702_2842476.pdf" \
    --output-json /tmp/realfarm-source-documents-manifest.json

  python3 scripts/bind_realfarm_source_evidence.py \
    --postgres-url postgresql://localhost:5432/farm_rm \
    --manifest-json /tmp/realfarm-source-documents-manifest.json \
    --execute

  python3 scripts/bootstrap_realfarm_crop_context.py \
    --postgres-url postgresql://localhost:5432/farm_rm \
    --farm-uri https://data.example/farm-rm/v1/farm/SI/REALFARM-001

  python3 scripts/bootstrap_realfarm_vineyard_components.py \
    --postgres-url postgresql://localhost:5432/farm_rm \
    --farm-uri https://data.example/farm-rm/v1/farm/SI/REALFARM-001 \
    --meeting-pdf "inbox/RealFarm/RKG_Zapisnik_100730702_2842476.pdf" \
    --manifest-json /tmp/realfarm-source-documents-manifest.json

  python3 scripts/bootstrap_realfarm_daily_conditions.py \
    --postgres-url postgresql://localhost:5432/farm_rm \
    --base-url http://127.0.0.1:8081 \
    --farm-uri https://data.example/farm-rm/v1/farm/SI/REALFARM-001 \
    --geometry-source-zip "../../inbox/RealFarm/Izvoz 20260310-0335 fe08957c.zip" \
    --candidate-station-csv /tmp/arso-station-catalog.csv \
    --output-prefix realfarm-daily-catalog

  python3 scripts/bootstrap_realfarm_leaf_wetness_proxy.py \
    --postgres-url postgresql://localhost:5432/farm_rm \
    --farm-uri https://data.example/farm-rm/v1/farm/SI/REALFARM-001

  python3 scripts/bootstrap_realfarm_agrometeorological_proxy.py \
    --postgres-url postgresql://localhost:5432/farm_rm \
    --farm-uri https://data.example/farm-rm/v1/farm/SI/REALFARM-001

  python3 scripts/bootstrap_field_climate_hazard_profiles.py \
    --postgres-url postgresql://localhost:5432/farm_rm \
    --farm-uri https://data.example/farm-rm/v1/farm/SI/REALFARM-001

  python3 scripts/import_field_overlay_facts.py \
    --base-url http://127.0.0.1:8080 \
    --csv examples/field-overlay-facts-demo.csv \
    --farm-uri https://data.demo.si/farm-rm/v1/farm/SI/FARM-001

  python3 scripts/import_field_daily_conditions.py \
    --base-url http://127.0.0.1:8080 \
    --csv examples/field-daily-conditions-demo.csv \
    --farm-uri https://data.demo.si/farm-rm/v1/farm/SI/FARM-001

  python3 scripts/import_field_climate_projection_facts.py \
    --base-url http://127.0.0.1:8080 \
    --csv examples/field-climate-projection-facts-demo.csv \
    --farm-uri https://data.demo.si/farm-rm/v1/farm/SI/FARM-001

  python3 scripts/import_field_climate_adaptation_signals.py \
    --base-url http://127.0.0.1:8080 \
    --csv examples/field-climate-adaptation-signals-demo.csv \
    --farm-uri https://data.demo.si/farm-rm/v1/farm/SI/FARM-001
  ```
  Notes:
  - `bootstrap_realfarm_local_profile.py` is the idempotent local-only bootstrap
    for the anonymized RealFarm profile derived from the authenticated eRKG
    GERK export ZIP. When a matching last-meeting PDF is provided, it now
    preserves the official document number, exact export timestamp, and a
    local-only PDF reference in declaration notes. It also accepts
    `--zip-evidence-uri` and `--meeting-pdf-evidence-uri` so a fresh bootstrap
    can bind first-class evidence records instead of relying on note-only
    provenance.
  - `prepare_erkg_last_meeting_declaration_csv.py` now accepts the
    authenticated last-meeting PDF too. It uses the official `Datum in čas
    izpisa` as the default `declared_at`, emits deterministic
    `authority_record_uri` and `geometry_ref` values from the GERK export, and
    can now bind a real `evidence_uri` when `--meeting-pdf-evidence-uri` is
    supplied. Without that override it keeps the local-only PDF reference in
    `notes`. Its default declaration-area behavior now copies
    `NUP_AREA` into `declared_area_ha` mechanically and records that choice in
    notes without claiming semantic equivalence.
  - `bootstrap_realfarm_source_documents.py` registers the authenticated local
    RealFarm ZIP/PDF through `/v1/documents/ingest`, computes stable SHA256
    digests, and writes a manifest with the minted `documentUri` and
    `evidenceUri` values.
  - `bind_realfarm_source_evidence.py` is the local repair step for existing
    RealFarm data. It binds the registered ZIP evidence onto
    `field_authority_link` and `field_geometry_snapshot`, and the registered PDF
    evidence onto `field_declaration_snapshot`, without rebuilding the rest of
    the RealFarm slice.
  - `bootstrap_realfarm_crop_context.py` turns the RealFarm declaration-use
    codes into deterministic local crop types plus current-season crop instances,
    so later phase-2/5/6 reads can resolve `current_crop` context instead of
    staying field-generic.
  - `bootstrap_realfarm_vineyard_components.py` parses the authenticated
    last-meeting PDF vineyard section and persists append-only
    `field_permanent_crop_component_snapshot` rows for permanent-crop fields.
    It reuses the registered RealFarm PDF evidence from
    `bootstrap_realfarm_source_documents.py`, ensures local `variety` rows for
    the vineyard crop species, and makes the source-native component history
    available as phase-6 variety context when no variety-risk record exists,
    using only dominant-composition fallback rather than inventing risk facts.
    It also makes the source-native component history
    available through:
    - `GET /v1/fields/{fieldUri}/passport/permanent-crop-component-snapshots`
    - `GET /v1/fields/{fieldUri}/permanent-crop-composition`
  - `bootstrap_realfarm_daily_conditions.py` reuses the existing ARSO
    daily-condition prep/import seam for the local RealFarm profile and now
    supports three honest mapping modes:
    - reviewed field-to-station proxy from a checked-in mapping asset
    - single explicit station proxy
    - nearest supported station proxy derived from a local eRKG GERK export ZIP
      plus candidate ARSO station codes or a prepared station catalog CSV
    The imported rows record `mappingMode`, `mappingStationCode`,
    `mappingSelectionBasis`, and centroid-distance metadata in `facts_json`
    so later proxy layers can inherit the same provenance instead of silently
    hardcoding a station.
    They now also carry:
    - `stationProxyPolicyId`
    - `stationMappingAssetId`
    so downstream proxy derivations can trace the reviewed assignment source,
    not just the selected station and distance.
    The default local policy is now checked in at
    `specs/v0.8/station-proxy-policies/si-realfarm-weather-proxy-v1.json`.
    That policy now points at the reviewed mapping asset
    `specs/v0.8/station-proxy-mappings/si-realfarm-reviewed-station-map-v1.json`,
    so the default RealFarm dry-run prefers reviewed field assignments before
    trying nearest-station selection or single-station fallback.
    When no explicit override flags are supplied, the daily bootstrap uses that
    policy to resolve:
    - `maxStationDistanceKm=20.0`
    - `enforceDistanceThreshold=true`
    - `mappingAssetId=si-realfarm-reviewed-station-map-v1`
    A live default dry-run now resolves:
    - `mapping_mode=reviewed_field_station_proxy`
    - `station_mapping_asset_id=si-realfarm-reviewed-station-map-v1`
    - `station_code=null`
    - `unique_station_count=1`
    - `within_threshold_count=4`
    with all four RealFarm fields assigned to `POSTOJNA` under
    `selectionBasis=operator_reviewed_assignment`.
    Explicit overrides are still available:
    - `--station-mapping-asset-id`
    - `--ignore-station-mapping-asset`
    - `--max-station-distance-km`
    - `--enforce-distance-threshold`
    - `--no-enforce-distance-threshold`
  - `diagnose_field_station_candidate_fit.py` is the read-only audit companion
    to that selector. It does not import anything; it ranks candidate stations
    per field and makes the proxy decision reviewable before or after import.
    By default it uses the same checked-in policy to resolve the selected-field
    threshold. `--max-selected-distance-km` remains available as an explicit
    override.
  - `bootstrap_realfarm_leaf_wetness_proxy.py` derives replay-safe local
    `leaf_wetness_duration_observation` rows from those imported ARSO daily
    facts. It stays a heuristic station proxy and inherits the daily row's
    mapping mode rather than inventing a separate station assignment. By
    default it loads `allowedMappingFitCodes=["within_threshold"]` from the
    same checked-in policy, and it will refuse to derive proxy rows when the
    latest daily-condition row falls outside that fit policy. Its notes
    preserve `stationProxyPolicyId`, `stationMappingAssetId`,
    `mappingDistanceKm`, `mappingThresholdKm`, and `mappingFitCode` when
    present on the daily row.
  - `bootstrap_realfarm_agrometeorological_proxy.py` derives replay-safe local
    `agrometeorological_station_observation` rows from the same official ARSO
    station feed selected by the latest imported RealFarm daily-condition row.
    It stays honest about the field assignment by marking the observation as an
    estimated station proxy in `notes` and `qualityFlag`, including whether the
    underlying daily row came from single-station or nearest-station mapping.
    It also defaults to `allowedMappingFitCodes=["within_threshold"]` from the
    same checked-in policy, while still allowing explicit
    `--allowed-mapping-fit-code` overrides.
    Those notes now also preserve `stationProxyPolicyId` and
    `stationMappingAssetId`, so the agromet payload still points back to the
    reviewed RealFarm station assignment asset.
  - those agrometeorological rows are now visible through
    `GET /v1/fields/{fieldUri}/passport/agrometeorological-observations`, and
    the field passport plus spray-window projection use the latest row as
    secondary weather support when daily facts do not carry humidity or wind.
  - `bootstrap_field_climate_hazard_profiles.py` is a local heuristic bridge
    from stored climate projection facts into drought/flood
    `climate_hazard_profile_observation` rows. It is useful for Phase 5 regional
    benchmark context, but it is not a source-native hazard model.
  - it creates the farm, fields, parcel blocks, GERKs, authority links,
    geometry snapshots, and declaration snapshots directly in the local DB
    without storing holder name or address
  - it keeps `declaredAreaHa` blank on purpose until `AREA` vs `NUP_AREA`
    policy is chosen
  - after bootstrapping RealFarm crop context, rerun the climate pipeline for
    that farm so stored climate rows are regenerated with
    `planningContextMode=current_crop`
- Example climate prep and derivation flow:
  ```bash
  cd "./specs/api/v1/server/fastapi"
  python3 scripts/export_si_field_climate_geography_map_csv.py \
    --postgres-url postgresql://localhost:5432/farm_rm \
    --overlay-stage-postgres-url postgresql://localhost:5433/farm_rm_overlay_stage \
    --farm-uri https://data.farmco.si/farm-rm/v1/farm/SI/FARM-001 \
    --output-csv /tmp/field-climate-geography-map-si-official.csv

  python3 scripts/prepare_arso_opsi_12km_field_climate_projection_facts.py \
    --zip /tmp/arso_opsi_rezultati_12km.zip \
    --postgres-url postgresql://localhost:5432/farm_rm \
    --overlay-stage-postgres-url postgresql://localhost:5433/farm_rm_overlay_stage \
    --farm-uri https://data.farmco.si/farm-rm/v1/farm/SI/FARM-001 \
    --source-version arso-opsi-12km-2025-08-01 \
    --as-of 2026-03-10 \
    --output-csv /tmp/field-climate-projection-facts-arso-12km-seasonal.csv

  python3 scripts/export_field_climate_geography_map_csv.py \
    --postgres-url postgresql://localhost:5432/farm_rm \
    --farm-uri https://data.demo.si/farm-rm/v1/farm/SI/FARM-001 \
    --output-csv /tmp/field-climate-geography-map.csv

  python3 scripts/validate_si_climate_intake_bundle.py \
    --profile-json ../../../../v0.8/reference-ingest/profiles/climate-projection-context-2026.json \
    --mapping-csv /tmp/field-climate-geography-map-si-official.csv \
    --source-csv examples/si-climate-projection-source-demo.csv \
    --review-json examples/climate-source-license-review-demo.json \
    --output-json /tmp/si-climate-intake-bundle.json \
    --require-local-ready

  python3 scripts/prepare_si_climate_projection_facts_csv.py \
    --mapping-csv /tmp/field-climate-geography-map-si-official.csv \
    --source-csv examples/si-climate-projection-source-demo.csv \
    --output-csv /tmp/field-climate-projection-facts.csv \
    --source-system ARSO_OPSI_CLIMATE_PROJECTIONS \
    --source-version arso-opsi-demo-2026-03 \
    --baseline-period 1991-2020 \
    --as-of 2026-03-10 \
    --source-ref https://example.invalid/arso-opsi-demo.csv

  python3 scripts/derive_field_climate_adaptation_signals_csv.py \
    --projection-csv /tmp/field-climate-projection-facts.csv \
    --output-csv /tmp/field-climate-adaptation-signals.csv

  python3 scripts/import_field_climate_projection_facts.py \
    --base-url http://127.0.0.1:8080 \
    --csv /tmp/field-climate-projection-facts.csv \
    --farm-uri https://data.demo.si/farm-rm/v1/farm/SI/FARM-001

  python3 scripts/import_field_climate_adaptation_signals.py \
    --base-url http://127.0.0.1:8080 \
    --csv /tmp/field-climate-adaptation-signals.csv \
    --farm-uri https://data.demo.si/farm-rm/v1/farm/SI/FARM-001
  ```
  Example benchmark prep and import flow:
  ```bash
  cd "./specs/api/v1/server/fastapi"
  python3 scripts/export_si_field_climate_geography_map_csv.py \
    --postgres-url postgresql://localhost:5432/farm_rm \
    --overlay-stage-postgres-url postgresql://localhost:5433/farm_rm_overlay_stage \
    --farm-uri https://data.farmco.si/farm-rm/v1/farm/SI/FARM-001 \
    --output-csv /tmp/field-benchmark-geography-map-si-official.csv

  python3 scripts/validate_si_benchmark_intake_bundle.py \
    --profile-json ../../../../v0.8/reference-ingest/profiles/regional-benchmark-context-2026.json \
    --mapping-csv /tmp/field-benchmark-geography-map-si-official.csv \
    --source-csv /tmp/surs-regional-benchmark-context.csv \
    --review-json /tmp/benchmark-source-license-review.json \
    --output-json /tmp/si-benchmark-intake-bundle.json \
    --require-local-ready

  python3 scripts/prepare_si_field_benchmark_context_facts_csv.py \
    --mapping-csv /tmp/field-benchmark-geography-map-si-official.csv \
    --source-csv /tmp/surs-regional-benchmark-context.csv \
    --output-csv /tmp/field-benchmark-context-facts.csv \
    --source-system SURS_SISTAT \
    --source-version surs-demo-2026-03 \
    --as-of 2026-03-11 \
    --default-source-ref https://example.invalid/surs-regional-benchmark-context.csv

  python3 scripts/derive_field_benchmark_explainability_signals_csv.py \
    --benchmark-csv /tmp/field-benchmark-context-facts.csv \
    --field-state-csv examples/field-benchmark-state-demo.csv \
    --policy-json ../../../../v0.8/reference-ingest/policies/si-surs-grapes-yield-explainability-1502410S-2026-reviewed-local-v2.json \
    --output-csv /tmp/field-explainability-signals.csv

  python3 scripts/import_field_benchmark_context_facts.py \
    --base-url http://127.0.0.1:8080 \
    --csv /tmp/field-benchmark-context-facts.csv \
    --farm-uri https://data.demo.si/farm-rm/v1/farm/SI/FARM-001

  python3 scripts/import_field_explainability_signals.py \
    --base-url http://127.0.0.1:8080 \
    --csv /tmp/field-explainability-signals.csv \
    --farm-uri https://data.demo.si/farm-rm/v1/farm/SI/FARM-001
  ```
  Notes:
  - the benchmark derivation step is intentionally policy-driven; the repo does
    not hardcode source-authoritative explainability thresholds for SURS /
    Eurostat / JRC data
  - `specs/v0.8/reference-ingest/policies/si-surs-grapes-yield-explainability-1502410S-2026-reviewed-local-v2.json`
    is the current checked-in reviewed-local policy asset for SURS
    grape-yield explainability; it rates `regional_yield_index` plus the
    derived `regional_yield_index_trend_pct_5y` and
    `regional_yield_index_volatility_cv_5y` window metrics
  - `specs/v0.8/reference-ingest/policies/si-surs-vineyard-structure-explainability-15P2107S-2026-reviewed-local-v1.json`
    is the checked-in reviewed-local policy asset for SURS vineyard structure.
    It only rates `regional_average_vine_density_per_ha`, and only through a
    local comparison against `local_vine_density_per_ha` from current
    permanent-crop component counts plus field area
  - `specs/v0.8/reference-ingest/policies/si-surs-grapes-market-context-0410812S-2026-reviewed-local-v1.json`
    is the checked-in reviewed-local policy asset for SURS producer-price
    index table `0410812S` product `64000` (grapes for industry). It rates:
    - `market_context/producer_price_index_trend_pct_5y`
    - `market_context/producer_price_index_volatility_cv_5y`
    while keeping annual `producer_price_index_2020_base` and the rolling
    mean descriptive only
  - when the source CSV comes from
    `prepare_surs_pxweb_regional_yield_context_source_csv.py`, pass
    `--emit-window-metrics` if you want the rolling-window benchmark metrics
    that the reviewed-local `v2` policy can rate
  - when the source CSV comes from
    `prepare_surs_pxweb_vineyard_benchmark_source_csv.py`, pass
    `--emit-derived-density-metrics` if you want the derived
    `regional_average_vine_density_per_ha` metric that the reviewed-local
    vineyard-structure policy can rate
  - when the source CSV comes from
    `prepare_surs_pxweb_market_context_source_csv.py`, pass
    `--emit-window-metrics` if you want the rolling-window market metrics that
    the reviewed-local `0410812S` policy can rate
  - market-context source rows are national-scope, so the benchmark mapping CSV
    must carry explicit `geography_code=SI` rows for the target fields
  - `examples/benchmark-explainability-policy-demo.json` and
    `examples/field-benchmark-state-demo.csv` are operator-facing demo inputs
    for the derivation step, not official benchmark source data
  Single-command wrapper for the same farm-scoped path:
  ```bash
  cd "./specs/api/v1/server/fastapi"
  python3 scripts/run_field_climate_pipeline.py \
    --zip /tmp/arso_opsi_rezultati_1km.zip \
    --postgres-url postgresql://localhost:5432/farm_rm \
    --overlay-stage-postgres-url postgresql://localhost:5433/farm_rm_overlay_stage \
    --base-url http://127.0.0.1:8081 \
    --farm-uri https://data.farmco.si/farm-rm/v1/farm/SI/FARM-001 \
    --source-version arso-opsi-1km-2025-08-01 \
    --as-of 2026-03-10 \
    --grid-code 1km \
    --output-dir /tmp \
    --dry-run
  ```
  Notes:
  - `run_field_climate_pipeline.py` is the repeatable operator wrapper for the
    current bounded climate flow: `prepare -> derive -> import`
  - every wrapper run now writes a JSON manifest by default at
    `<output-dir>/<prefix>-manifest.json`; override it with `--manifest-json`
  - use `--skip-prepare`, `--skip-derive`, or `--skip-import` when replaying
    only part of the pipeline against already prepared CSVs
  - the wrapper auto-derives stable output filenames from `farm-uri`,
    `grid-code`, `source-version`, and `as-of` unless `--output-prefix`,
    `--projection-csv`, or `--signal-csv` override that behavior
  - the manifest is operator-facing and intentionally avoids secrets; it keeps
    source ZIP checksum and path, key farm/grid/source metadata, generated CSV
    descriptors, and import summaries for replay and audit
  Farm-list exporter for batch runs:
  ```bash
  cd "./specs/api/v1/server/fastapi"
  python3 scripts/export_field_climate_batch_farm_list_csv.py \
    --postgres-url postgresql://localhost:5432/farm_rm \
    --overlay-stage-postgres-url postgresql://localhost:5433/farm_rm_overlay_stage \
    --output-csv /tmp/field-climate-farms.csv \
    --grid-code 1km \
    --source-version arso-opsi-1km-2025-08-01 \
    --as-of 2026-03-10
  ```
  Exporter notes:
  - `export_field_climate_batch_farm_list_csv.py` emits a batch-runner-ready
    CSV for farms that have at least one field backed by staged GERK geometry
  - exported rows already include `farm_uri`, `grid_code`, `source_version`,
    `as_of`, and `output_prefix`, plus field and GERK coverage counts for
    operator review
  Field-level blocker diagnostic:
  ```bash
  cd "./specs/api/v1/server/fastapi"
  python3 scripts/diagnose_field_climate_batch_gaps.py \
    --postgres-url postgresql://localhost:5432/farm_rm \
    --overlay-stage-postgres-url postgresql://localhost:5433/farm_rm_overlay_stage \
    --output-csv /tmp/field-climate-batch-gaps.csv \
    --only-blocked
  ```
  Diagnostic notes:
  - `diagnose_field_climate_batch_gaps.py` reports the exact field-level
    blocker used by the climate prep path
  - blocker codes are:
    - `missing_field_gerk_map`
    - `missing_staged_gerk_row`
    - `missing_staged_gerk_geom`
  - the CSV also includes mapped / staged / staged-with-geometry GERK PID
    counts and the missing PID list so you can tell whether a field is fully
    missing or only partially staged
  Local field-slice purge helper:
  ```bash
  cd "./specs/api/v1/server/fastapi"
  python3 scripts/purge_local_field_slice.py \
    --postgres-url postgresql://localhost:5432/farm_rm \
    --field-uri https://data.demo.si/farm-rm/v1/field/SI/FIELD-7
  ```
  Purge notes:
  - `purge_local_field_slice.py` is a local operator utility for cleaning up
    seeded/demo field slices that block climate prep or diagnostics
  - it is `dry-run` by default and only executes when `--execute` is present
  - it uses `SET LOCAL session_replication_role = replica` during the purge,
    because the Farm RM schema is append-only and normal `DELETE` is blocked
  - by default it only allows local/demo-style hosts such as
    `data.demo.si`, `data.farmco.si`, and `data.example`; use
    `--allow-any-host` only when that guard is intentionally too narrow
  Batch wrapper for multiple farms:
  ```bash
  cd "./specs/api/v1/server/fastapi"
  python3 scripts/run_field_climate_pipeline_batch.py \
    --farm-list-csv /tmp/field-climate-farms.csv \
    --zip /tmp/arso_opsi_rezultati_1km.zip \
    --postgres-url postgresql://localhost:5432/farm_rm \
    --overlay-stage-postgres-url postgresql://localhost:5433/farm_rm_overlay_stage \
    --base-url http://127.0.0.1:8081 \
    --output-dir /tmp \
    --dry-run \
    --continue-on-error
  ```
  Batch notes:
  - `run_field_climate_pipeline_batch.py` reads a farm-list CSV, runs the
    single-farm wrapper once per row, and writes a batch index manifest with
    per-farm status, manifest paths, row counts, and failures
  - default batch manifest path is derived from the farm-list CSV stem, for
    example `/tmp/field-climate-farms-batch-manifest.json`
  - supported row overrides include `zip_path`, `grid_code`, `source_version`,
    `as_of`, `output_prefix`, `projection_csv`, `signal_csv`, `manifest_json`,
    `season_codes`, `scenario_codes`, `period_labels`, `variable_codes`,
    `source_system`, `baseline_period`, `overlay_stage_schema`,
    `gerk_stage_table`, `skip_prepare`, `skip_derive`, and `skip_import`
  - `prepare_arso_opsi_12km_field_climate_projection_facts.py` is the first
    real source-native climate producer path in this repo. It now supports
    both the public ARSO/OPSI `12km` and `1km` NetCDF ZIP bundles via
    `--grid-code`, and it uses staged GERK geometry rather than demo source
    rows.
  - the current live adapter now covers the annual + seasonal slice:
    - seasons: `leto`, `DJF`, `MAM`, `JJA`, `SON`
    - variables:
    - `tas` -> `mean_temperature_c`
    - `tasmax` -> `max_temperature_c`
    - `tasmin` -> `min_temperature_c`
    - `evspsblpot` -> `reference_et`
    - `pr` -> `seasonal_precip_anomaly`
  - by default it emits all supported seasons; use `--season-codes` to narrow
    the export or the hidden compatibility flag `--season-code` for a
    one-season replay
  - the 1 km bundle uses projected raster coordinates rather than lon/lat; the
    adapter now resolves the 1 km NetCDF subdataset names dynamically and
    transforms field centroids into the raster CRS before sampling
  - farm-scoped prep now batches clustered pixel reads through small
    `gdal_translate -srcwin` extracts instead of shelling out to
    `gdallocationinfo` once per field per subdataset
  - the prep CSV uses `aggregation_type` to preserve seasonal identity:
    `annual_mean`, `seasonal_mean_djf`, `seasonal_mean_mam`,
    `seasonal_mean_jja`, `seasonal_mean_son`
  - it emits `geography_scope=custom` and `geography_fit_status=downscaled`
    because the source is a gridded climate surface sampled at the field
    centroid, not a statistical-region table
  - the phase-6 runtime now preserves `aggregationType` in
    `climate-indicator-trends` and `climate-suitability-outlook`, so imported
    seasonal rows stay distinguishable at read time
  - when multiple stored climate batches share the same `asOf`, the phase-6
    runtime now prefers the finer source family (`1km` over `12km`) rather
    than mixing rows from both resolutions into the same live response
  - on the current four-field Farmco batch, the optimized 1 km prep completed
    in about `172s` and still emitted `900` normalized facts
  - for Slovenia GERK-backed fields, prefer
    `export_si_field_climate_geography_map_csv.py` over the generic
    pedoclimatic export helper when the DB still carries smoke/demo
    `region_code` values or when you need an official geography lookup path
  - the exported geography map is conservative: it marks fields as
    `acceptable` only when the latest pedoclimatic profile has medium/high
    confidence, otherwise `regional_proxy`
  - the SI-specific exporter marks rows `acceptable` because the geography code
    comes from the official GeoHub statistical-region layer via staged GERK
    geometry, not from advisory pedoclimatic evidence
  - the intake validator is intentionally operator-facing and offline; it does
    not download climate sources or resolve license terms on its own
  - `--require-local-ready` is the honest default for now; production import
    should use `--require-production-ready` only after publication rights and
    non-proxy geography-fit rules are cleared
- Expected CSV headers:
  - authority-link CSV:
    - required: `field_uri`, `authority_scheme_code`, `authority_record_uri`,
      `recorded_at`, `source_version`
    - optional: `authority_code`, `authority_label`, `valid_from`, `valid_to`,
      `source_ref`, `evidence_uri`, `notes`
  - geometry-snapshot CSV:
    - required: `field_uri`, `geometry_role_code`, `geometry_ref`,
      `captured_at`
    - optional: `authority_link_uri`, `authority_record_uri`, `valid_from`,
      `valid_to`, `area_ha`, `source_version`, `is_compliance_geometry`,
      `evidence_uri`, `notes`
  - declaration-snapshot CSV:
    - required: `field_uri`, `declared_at`, `season_code`,
      `declared_use_code`, `production_status`, `source_version`
    - optional: `authority_link_uri`, `authority_record_uri`, `geometry_ref`,
      `geometry_snapshot_uri`, `crop_instance_uri`,
      `declared_crop_type_uri`, `declared_crop_label`, `declared_area_ha`,
      `valid_from`, `valid_to`, `compliance_geometry_ref`, `evidence_uri`,
      `notes`
  - overlay-fact CSV:
    - required: `field_uri`, `overlay_code`, `severity_code`,
      `observed_at`, `source_version`
    - optional: `authority_link_uri`, `authority_record_uri`,
      `geometry_snapshot_uri`, `geometry_ref`, `regime_code`, `coverage_pct`,
      `valid_from`, `valid_to`, `evidence_uri`, `attributes_json`, `notes`
  - daily-condition CSV:
    - required: `field_uri`, `as_of_date`, `observed_at`, `source_version`
    - optional: `crop_instance_uri`, `spray_window_code`,
      `nutrient_spreading_code`, `irrigation_readiness_code`,
      `scout_priority_code`, `weather_summary_text`, `eo_anomaly_flag`,
      `risk_summary_text`, `evidence_uri`, `facts_json`, `notes`
  - climate-projection CSV:
    - required: `field_uri`, `as_of`, `planning_context_mode`,
      `source_system`, `source_id`, `source_version`, `geography_scope`,
      `geography_code`, `scenario_family`, `scenario_code`,
      `horizon_scope`, `period_start`, `period_end`, `baseline_period`,
      `indicator_code`, `indicator_value`, `unit_code`, `aggregation_type`,
      `uncertainty_class`, `freshness_status`, `evidence_refs_json`
    - optional: `crop_instance_uri`, `crop_or_variety_code`,
      `geography_fit_status`, `baseline_value`, `baseline_unit_code`,
      `scenario_spread_value`, `notes`
  - climate-adaptation-signal CSV:
    - required: `field_uri`, `as_of`, `planning_context_mode`,
      `signal_type`, `priority_level`, `horizon_scope`,
      `confidence_status`, `recommended_themes_json`,
      `reason_codes_json`, `trace_refs_json`, `evidence_refs_json`
    - optional: `crop_instance_uri`, `crop_or_variety_code`,
      `geography_fit_status`, `uncertainty_codes_json`, `notes`
  - climate-geography-mapping CSV for `prepare_si_climate_projection_facts_csv.py`:
    - required: `field_uri`, `geography_code`
    - optional: `crop_instance_uri`, `crop_or_variety_code`,
      `geography_scope`, `geography_fit_status`, `planning_context_mode`
    - the DB export helper also emits extra audit columns such as
      `mapping_basis`, `pedoclimatic_profile_uri`,
      `pedoclimatic_confidence_status`, `pedoclimatic_confidence_score`, and
      `climate_source_ref`; the climate prep adapter safely ignores those
      extra columns
    - the Slovenia GeoHub export helper additionally emits `gerk_pids`,
      `official_region_name`, and `official_region_numeric_code` for operator
      review while keeping the same downstream-compatible core headers
  - climate-source long-table CSV for `prepare_si_climate_projection_facts_csv.py`:
    - required by alias: geography code, scenario code, period window,
      indicator code, indicator value, unit code
    - accepted aliases include:
      `geography_code|region_code`, `scenario_code|scenario`,
      `period_start/period_end|period`, `indicator_code|indicator`,
      `indicator_value|value`, `unit_code|unit`
    - optional aliases include:
      `baseline_value`, `baseline_unit_code`, `scenario_spread_value`,
      `source_id`, `source_version`, `source_ref`, `evidence_refs_json`,
      `aggregation_type`, `uncertainty_class`, `freshness_status`, `notes`
  - climate-source review JSON for `validate_si_climate_intake_bundle.py`:
    - required: `sourceSystem`, `sourceVersion`, `reviewStatus`,
      `reviewedAt`, `reviewedBy`, `localDerivationAllowed`,
      `publicationAllowed`
    - optional: `evidenceRefs`, `notes`
- An official GERK archive adapter now exists for the first source-native
  producer path:
  `specs/api/v1/server/fastapi/scripts/prepare_gerk_archive_field_passport_csv.py`
  It reads an official `GERK_YYYY_MM_DD.zip` archive, validates that the
  shapefile members are present, parses the `GERK_PID`/`AREA`/`RABA_ID`/
  `Z_AVG`/`NAGIB_AVG`/`BLOK_ID` DBF rows, and emits the normalized
  authority-link and geometry-snapshot CSV contracts already consumed by:
  - `scripts/import_field_authority_links.py`
  - `scripts/import_field_geometry_snapshots.py`
- The GERK archive adapter requires explicit field mapping through one of:
  - `--mapping-csv` with headers `gerk_pid,field_uri`
  - `--postgres-url` plus `--farm-uri`, which derives `gerk_pid -> field_uri`
    from Farm RM using:
    - `gerk -> parcel_block -> field`
    - `field.local_id` as a fallback when it is a numeric GERK code
  - `--field-uri-template`, e.g.
    `https://data.farmco.si/farm-rm/v1/field/SI/GERK-{gerk_pid}`
- Example source-native GERK flow:
  ```bash
  cd "./specs/api/v1/server/fastapi"
  python3 scripts/prepare_gerk_archive_field_passport_csv.py \
    --zip /tmp/GERK_2026_02_02.zip \
    --gerk-pid 2140403 \
    --field-uri-template 'https://data.farmco.si/farm-rm/v1/field/SI/GERK-{gerk_pid}' \
    --authority-csv /tmp/gerk-authority-2140403.csv \
    --geometry-csv /tmp/gerk-geometry-2140403.csv \
    --source-ref https://rkg.gov.si/arhiv/GERK/GERK_2026_02_02.zip \
    --is-compliance-geometry

  python3 scripts/import_field_authority_links.py \
    --base-url http://127.0.0.1:8080 \
    --csv /tmp/gerk-authority-2140403.csv \
    --farm-uri https://data.farmco.si/farm-rm/v1/farm/SI/FARM-001

  python3 scripts/import_field_geometry_snapshots.py \
    --base-url http://127.0.0.1:8080 \
    --csv /tmp/gerk-geometry-2140403.csv \
    --farm-uri https://data.farmco.si/farm-rm/v1/farm/SI/FARM-001
  ```
- Example using live DB-derived mapping instead of a hand-authored mapping CSV:
  ```bash
  cd "./specs/api/v1/server/fastapi"
  PYTHONPATH="$(pwd)" ./.venv/bin/python scripts/prepare_gerk_archive_field_passport_csv.py \
    --zip /tmp/GERK_2026_02_02.zip \
    --gerk-pid 2140403 \
    --postgres-url postgresql://localhost:5432/farm_rm \
    --farm-uri https://data.farmco.si/farm-rm/v1/farm/SI/FARM-001 \
    --authority-csv /tmp/gerk-authority-dbmap.csv \
    --geometry-csv /tmp/gerk-geometry-dbmap.csv \
    --source-ref https://rkg.gov.si/arhiv/GERK/GERK_2026_02_02.zip \
    --is-compliance-geometry
  ```
- Important current limitation: the adapter preserves official source identity,
  area, and metadata inside the normalized geometry contract, but the current
  field-passport geometry write surface stores `geometryRef` plus metadata, not
  raw polygon coordinates. The source polygon therefore remains in the official
  GERK shapefile archive rather than being embedded in Farm RM.
- Capabilities endpoint includes feature discovery for:
  `aiOcrParse`, `aiOcrMetrics`, `referenceSearch`, `referenceSnapshotCatalog`, `referenceSnapshotDiff`, `referenceSnapshotImport`, `referenceSnapshotImportPreview`, `referenceSourceCatalog`, `referenceSourcePlan`, `referenceSourceProfiles`, `referenceIngestionReadiness`, `seasonWindows`.
- Capabilities endpoint also exposes contract metadata in `contracts.*`,
  currently `contracts.referenceIngestionReadinessChecks.version`.
- Benchmark explainability signals now carry first-class `policyId` and
  `policyVersion` in the derived CSV, importer payload, stored record, and
  explainability summary/list responses. The runtime prefers the latest
  explainability batch for the active stored policy instead of mixing rows from
  different policy identities in the same top-signal slice.
