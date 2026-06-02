# Reference Snapshot Ingestion (EPPO/EU/CPVO -> Farm-RM)

This folder contains the ingestion runbook and sample files for loading a
versioned crop/variety snapshot into Farm-RM.

## Why this exists

`/v1/reference/snapshots/import` requires a strict payload shape. Real source
exports (EPPO/EU catalogue/CPVO) are usually tabular and not API-ready.

`tools/reference_snapshot_pipeline.py` provides a reproducible pipeline:

1. build JSON payload from CSV exports
2. import payload into Farm-RM API

The build step is strict by design:

1. duplicate `uri` values are rejected for crops and varieties
2. every `varieties.crop_uri` must exist in `crops.uri`

This prevents silent data corruption in downstream reference search.

## Runtime API surfaces

The repo now exposes a fuller operator-facing reference workflow around the
same snapshot/import model.

Read-only planning and guidance endpoints:

- `GET /v1/reference/sources`
  - lists supported source systems and can include latest snapshot status with
    `includeSnapshotStatus=true`
- `GET /v1/reference/source-plan`
  - returns deterministic source priority for a requested `entityType`
  - supports `jurisdiction`, `productionProfile`, and optional
    `includeSnapshotStatus=true`
  - requires `entityType`; current tests prove `productionProfile=organic` as
    the default when omitted
- `GET /v1/reference/source-profiles`
  - returns profile metadata, expected CSV headers, and acquisition guidance
    (`entryPointUrl`, auth requirement, artifact scope)

Pre-import validation and import endpoints:

- `POST /v1/reference/source-ingestion/check`
  - validates source/profile/version/header readiness before import
  - supports optional strict header mode with `requireHeaders=true`
  - returns typed readiness diagnostics via `checks.*`, including
    `checks.contractVersion`
- `POST /v1/reference/snapshots/import/preview`
  - side-effect free preview for duplicate-URI, unresolved-crop, and same-version
    hash replay/conflict checks
- `POST /v1/reference/snapshots/import`
  - persists an immutable snapshot bundle and returns `409` on conflicting
    re-import for the same `sourceSystem + sourceVersion`
- `GET /v1/reference/snapshots`
  - lists imported snapshot versions for client pinning and admin review
- `GET /v1/reference/snapshots/diff`
  - compares two imported versions for one source system

Reference search endpoint:

- `GET /v1/reference/varieties/search`
  - requires both `q` and `cropUri`
  - supports optional `sourceVersion` and `sourceSystem`
  - returns `reference_snapshot_not_found` when a pinned version, or
    version-plus-source-system slice, does not exist

These runtime/API surfaces are proven in the FastAPI runtime, contract-alignment
tests, and API tests. This README stays the runbook for operators and maintainers,
not the primary transport-contract source.

## Sample files

- `sample/crops.csv`
- `sample/varieties.csv`
- `sample/taxa.csv` (optional; plant taxonomy)

These are minimal examples with all required columns.

## Source profiles (where data comes from)

Profiles encode trusted source metadata and refresh guidance:

- `profiles/eu-catalog-2026.json` (EU common catalog context)
- `profiles/eu-pvp-portal-2026.json` (EU Plant Variety Portal official list export)
- `profiles/cpvo-2026.json` (CPVO context)
- `profiles/eppo-2026.json` (EPPO context)
- `profiles/agrovoc-eppo-bridge-2026.json` (second-source bridge for family/crop-type enrichment)

Each profile now also includes an `acquisition` block used by
`GET /v1/reference/source-profiles` to expose deterministic operator guidance:

- where to start (`entryPointUrl`)
- whether auth is expected (`requiresAuth`, optional `authHint`)
- which artifacts to fetch per entity scope (`artifacts[]`)

Use a profile to avoid repeating `sourceSystem/sourceRef/licenseHint` fields.

The folder also carries planning-only field-passport climate profiles for
future phase-6 source-native ingestion:

- `profiles/climate-projection-context-2026.json`
- `profiles/climate-indicator-trends-2026.json`
- `profiles/climate-adaptation-signals-2026.json`

It also carries planning-only Phase-5 benchmark/explainability profiles for a
future SURS / Eurostat / JRC style ingest path:

- `profiles/regional-benchmark-context-2026.json`
- `profiles/regional-market-context-2026.json`
- `profiles/regional-explainability-2026.json`

These climate profiles are not part of the current crop/variety reference
snapshot pipeline and are not exposed through `GET /v1/reference/source-profiles`.
They exist as scaffolding for future scenario-bearing field climate ingestion
and derivation work.
The benchmark/explainability profiles are similarly planning-only and are not
yet wired to a source-native benchmark adapter.
The FastAPI repo now does carry local prep/validation tooling that targets
those profiles:

- `specs/api/v1/server/fastapi/scripts/prepare_si_field_benchmark_context_facts_csv.py`
- `specs/api/v1/server/fastapi/scripts/validate_si_benchmark_intake_bundle.py`

These tools normalize already-downloaded benchmark extracts into the
`FIELD.field_benchmark_context_fact` importer contract, but they still rely on
operator-provided local source CSV and review metadata.

Before promoting any benchmark policy beyond local derivation, use:

- `BENCHMARK_POLICY_GOVERNANCE_CHECKLIST.md`

The folder now also carries checked-in explainability policy assets for real
benchmark series:

- `policies/si-surs-grapes-yield-explainability-1502410S-2026-draft.json`
- `policies/si-surs-grapes-yield-explainability-1502410S-2026-reviewed-local-v1.json`
- `policies/si-surs-grapes-yield-explainability-1502410S-2026-reviewed-local-v2.json`
- `policies/si-surs-vineyard-structure-explainability-15P2107S-2026-reviewed-local-v1.json`
- `policies/si-surs-grapes-market-context-0410812S-2026-reviewed-local-v1.json`

The reviewed-local `v2` policy is the active local/internal
benchmark-governance asset for SURS table `1502410S`. It governs:

- `yield_context/regional_yield_index`
- `yield_context/regional_yield_index_trend_pct_5y`
- `yield_context/regional_yield_index_volatility_cv_5y`

Absolute `regional_average_yield_t_ha` and the descriptive rolling-window
means remain non-rateable context only. `v1` and the draft file are retained
as policy history.

The folder now also carries a reviewed-local vineyard-structure policy for
SURS table `15P2107S`. It governs:

- `vineyard_structure/regional_average_vine_density_per_ha`

That metric is only rateable through local comparison against
`local_vine_density_per_ha`. The raw vineyard totals:

- `vineyard_area_ha`
- `vineyard_holding_count`
- `vineyard_vine_count`

remain descriptive context only.

The folder now also carries a reviewed-local market-context policy for SURS
table `0410812S` and a source profile for the same family:

- `profiles/surs-grapes-market-context-0410812S-2026.json`
- `policies/si-surs-grapes-market-context-0410812S-2026-reviewed-local-v1.json`

That policy governs:

- `market_context/producer_price_index_trend_pct_5y`
- `market_context/producer_price_index_volatility_cv_5y`

Annual `producer_price_index_2020_base` and the rolling mean remain
descriptive context only. The market family is national-scope, so downstream
matching should use explicit benchmark mapping rows with `geography_code=SI`.

## Recommended operator flow

For a new or refreshed source load, the current repo-backed order is:

1. `GET /v1/reference/sources` to confirm which source systems and latest
   snapshots are already known.
2. `GET /v1/reference/source-plan` for the target `entityType` and jurisdiction
   to confirm the recommended source priority.
3. `GET /v1/reference/source-profiles` to inspect acquisition guidance and CSV
   header expectations for the chosen source/profile.
4. Build local CSV or sync outputs with the repo tooling below.
5. `POST /v1/reference/source-ingestion/check` before import submission.
6. `POST /v1/reference/snapshots/import/preview` before any write path.
7. `POST /v1/reference/snapshots/import` only after preview is ready.
8. `GET /v1/reference/snapshots` and `GET /v1/reference/snapshots/diff` for
   post-import review and release pinning.

## Zero-manual sync (EU Plant Variety Portal)

If you want to avoid manual CSV work, use:

`tools/eu_pvp_portal_sync.py`

This tool:

1. downloads the official XLSX export ("EU Variety List")
2. extracts the portal species dropdown list (UPOV species codes + scientific labels)
3. enriches species with a second-source bridge (`EPPO_AGROVOC_BRIDGE`) to populate:
   - `family_taxon_uri` via family taxon rows
   - refined `crop_type_code` (`cereal/pulse/oilseed/...`) instead of only `AGR/VEG/FRU` fallbacks
4. generates `taxa.csv`, `crops.csv`, `varieties.csv`
4. builds a reference snapshot payload
5. optionally imports it into your running API

Example (auth disabled locally):

```bash
python3 tools/eu_pvp_portal_sync.py sync \
  --workdir /tmp/farm_rm_eupvp_sync \
  --reuse-downloads \
  --import-to-api \
  --api-base-url http://127.0.0.1:8080
```

To limit the import (useful for v1 pilots), filter by country/org codes:

```bash
python3 tools/eu_pvp_portal_sync.py sync \
  --countries "SI" \
  --max-unique-varieties 2000 \
  --import-to-api
```

Notes:

- Filtered/capped runs auto-suffix `sourceVersion` (unless you explicitly pass `--source-version`) so you don't accidentally "claim" the canonical full version with partial data.
- To disable second-source enrichment and keep portal-only values, pass `--no-bridge-enrichment`.
- Bridge files used by default:
  - `specs/v0.8/reference-ingest/enrichment/genus-family-crop-bridge-2026.csv`
  - `specs/v0.8/reference-ingest/enrichment/upov-species-overrides-2026.csv`
  - `specs/v0.8/reference-ingest/enrichment/upov-species-common-names-2026.csv`
- You can override bridge file paths with:
  - `--bridge-genus-map-csv /path/to/file.csv`
  - `--bridge-species-map-csv /path/to/file.csv`
  - `--common-names-csv /path/to/file.csv`
- Common-name policy (hybrid):
  - curated Slovenian and high-impact EN names come from `upov-species-common-names-2026.csv`
  - missing long-tail names can be resolved from GBIF at sync time (enabled by default)
  - disable GBIF fallback with `--no-gbif-common-name-lookup` when offline/deterministic runs are required
  - GBIF results are cached in `<workdir>/common-names-cache.json`, so repeated runs progressively fill the long tail

## Zero-manual sync (EPPO GD) for missing crops (e.g., black cumin)

EU Plant Variety Portal is an "official variety list" source, so it will miss
many minor crops that still matter in real farms (spices, herbs, medicinal
plants, niche cover crops).

EPPO Global Database (GD) is a European reference that fills this gap with:

- stable EPPO Codes
- taxonomy (family/genus/species) useful for rotation/IPM reasoning
- multilingual common names (often including `sl` and `sr`)

Prerequisite: EPPO API key (GD V2)

1. Create an EPPO account and accept the EPPO Open Data Licence at `https://data.eppo.int/`
2. Generate an API key in the dashboard
3. Export it as `EPPO_API_KEY`

Example: import black cumin (`Nigella sativa`, EPPO code `NIGSA`)

```bash
export EPPO_API_KEY="..."

python3 tools/eppo_gd_sync.py sync \
  --workdir /tmp/farm_rm_eppo_sync \
  --names "Nigella sativa,black cumin" \
  --langs "en,sl,sr" \
  --import-to-api \
  --farmrm-api-base-url http://127.0.0.1:8080
```

Notes:

- If EPPO does not provide a Slovene name for a minor crop, add a curated override row:
  `specs/v0.8/reference-ingest/enrichment/eppo-common-names-overrides-2026.csv`
- Crop type classification uses the same genus bridge as EU PVP when possible:
  `specs/v0.8/reference-ingest/enrichment/genus-family-crop-bridge-2026.csv`

## When to require common names vs scientific names

Use this rule in product decisions:

1. **Always require scientific identity** for persistence and interoperability:
   - `taxon.scientific_name` is mandatory
   - URIs/codes remain the source of truth
2. **Require common names** for operator-facing flows:
   - mobile field forms
   - seed/input purchase review
   - SI compliance-facing UIs and reports
3. **Do not block ingestion on missing common names** for long-tail species:
   - fallback is scientific label
   - enrich over time through curated CSV updates and/or GBIF lookups

## Build payload

```bash
python3 tools/reference_snapshot_pipeline.py build \
  --profile specs/v0.8/reference-ingest/profiles/eu-catalog-2026.json \
  --source-system EU_CATALOG \
  --source-version snapshot-2026-03 \
  --published-at 2026-03-01 \
  --taxa-csv specs/v0.8/reference-ingest/sample/taxa.csv \
  --crops-csv specs/v0.8/reference-ingest/sample/crops.csv \
  --varieties-csv specs/v0.8/reference-ingest/sample/varieties.csv \
  --out /tmp/reference-snapshot-eu-2026-03.json
```

Notes:

- `--source-system` and `--source-version` can come from CLI or profile.
- If both are provided, CLI values take precedence.

## Import payload

With auth disabled locally (`FARM_RM_DISABLE_AUTH=1`):

```bash
python3 tools/reference_snapshot_pipeline.py import \
  --api-base-url http://127.0.0.1:8080 \
  --payload /tmp/reference-snapshot-eu-2026-03.json
```

With auth enabled:

```bash
python3 tools/reference_snapshot_pipeline.py import \
  --api-base-url http://127.0.0.1:8080 \
  --payload /tmp/reference-snapshot-eu-2026-03.json \
  --auth-token "$FARM_RM_JWT" \
  --farm-uri "https://data.farmco.si/farm-rm/v1/farm/SI/FARM-001"
```

## CSV column contract

`taxa.csv` (optional) required:

- `uri`
- `rank_code`
- `scientific_name`

`taxa.csv` (optional) optional:

- `parent_taxon_uri`
- `labels_json` (JSON object map)
- `synonyms_json` (JSON array list)
- `external_codes_json` (JSON array of objects, e.g. `[{"codeSystem":"EPPO","code":"ZEAMA"}]`)
- `source_id`

`crops.csv` required:

- `uri`
- `code`
- `label`

`crops.csv` optional:

- `labels_json` (JSON object, e.g. `{"en":"Maize","sl-SI":"Koruza"}`)
- `synonyms_json` (JSON array, e.g. `["corn","koruza"]`)
- `source_id`
- `taxon_uri` (URI of a taxon entry, rank=`species`)
- `family_taxon_uri` (URI of a taxon entry, rank=`family`)
- `crop_type_code` (functional crop group, e.g. `cereal`)

`varieties.csv` required:

- `uri`
- `crop_uri`
- `code`
- `label`

`varieties.csv` optional:

- `labels_json` (JSON object)
- `synonyms_json` (JSON array)
- `breeder_name`
- `maturity_group`
- `source_id`
- `season_type_code` (e.g. `winter`, `spring`)
- `life_cycle_code` (e.g. `annual`, `perennial`)
- `market_class_code`
- `market_class_text`
- `registered_from` (YYYY-MM-DD)
- `registered_to` (YYYY-MM-DD)
- `status_code` (e.g. `active`, `expired`)
- `portal_id` (EU PVP identifier when available)
- `attributes_json` (JSON object; raw portal row payload)

## Operational cadence (recommended)

1. EU-first production profile: refresh monthly.
2. Freeze the imported snapshot version per release cycle (do not mutate in-place).
3. Record the exact `sourceVersion` (for example `snapshot-2026-03`) and keep it visible in operator/admin tools.
