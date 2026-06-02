# Phase 6 Spec - Climate Adaptation Layer

Parcel-centric compliance twin, Slovenia-first, built on the phase-1 field compliance passport

Date: 2026-03-09

## Executive decision

- The original phase-6 planning slice is now materially implemented as repo-native archetypes, templates, projections, runtime routes, OpenAPI paths, and field-passport tests.
- Live repo evidence now includes:
  - `FIELD.field_climate_projection_fact.v1.md`
  - `FIELD.field_climate_adaptation_signal.v1.md`
  - `template-field-climate-adaptation-summary-si-v0_8.md`
  - `template-field-climate-suitability-outlook-si-v0_8.md`
  - `template-field-climate-indicator-trends-si-v0_8.md`
  - `template-field-climate-plan-tab-si-v0_8.md`
  - `GET /v1/fields/{fieldUri}/climate-adaptation-summary`
  - `GET /v1/fields/{fieldUri}/climate-suitability-outlook`
  - `GET /v1/fields/{fieldUri}/climate-indicator-trends`
  - `GET /v1/fields/{fieldUri}/climate-plan-tab`
- Remaining future work is narrower: deeper climate-source adapter hardening, any optional explicit climate recompute surface, and later planning-signal refinement that preserves uncertainty and non-authoritative behavior.
- Phase 6 stays parcel-centric and planning-oriented. Climate projections remain advisory, uncertainty-bearing, and horizon-specific, and production clients still must not synthesize roadmap-style `Later` placeholders for the Plan workspace.

## Repo-grounded baseline

### Observed current state

- Markdown archetypes and templates are the human authoring layer; generated FADL and JSON artifacts are derived from them. Repo evidence: 00-index.md, 90-glossary.md.
- The semantic backbone already includes Field, CropInstance, append-only semantics, EvidenceRecord, EventRecord, and RuleExecutionTrace. Repo evidence: 20-semantic-core.md, 90-glossary.md.
- The repo already has a template projection layer for app-facing workflows and a test path for projection contracts. Repo evidence: 20-semantic-core.md, 40-api-and-data-contracts.md, 60-build-run-test-generate.md.
- The repo now contains repo-native climate-projection/adaptation archetypes plus authored phase-6 templates and projection contracts.
- The runtime now exposes climate-adaptation-summary, climate-suitability-outlook, climate-indicator-trends, and climate-plan-tab read models and covers them in field-passport route tests and OpenAPI route-alignment tests.
- Rulepacks live under specs/v0.4/regulatory/rulepacks/, while active extension work is concentrated under specs/v0.8/. Repo evidence: 10-repo-map.md, 50-compliance-and-reporting.md, 70-implementation-status.md.
- The runtime loads spec assets from the repo and relies on FastAPI/Pydantic contracts, SHACL checks, DB smoke checks, and backend tests. Repo evidence: 30-runtime-architecture.md, 40-api-and-data-contracts.md, 60-build-run-test-generate.md.
- The v0.8 agronomy ontology already includes climate hazards, adaptation profiles, agrometeorology, irrigation, variety trial/risk, and remote sensing. Repo evidence: 20-semantic-core.md.

### Evidence-backed inference

- Phase 6 did extend the parcel passport rather than create a separate climate-planning subsystem.
- Climate hazards and adaptation profiles were already present in the ontology layer, and the current repo-backed shape now persists scenario-aware climate context append-only, derives parcel-facing adaptation signals, and exposes narrow planning projections.
- Climate outputs should stay advisory, scenario-aware, and uncertainty-bearing; they must not silently overrule compliance authority or same-season operational decisions.
- Any remaining climate work is adapter/recompute hardening, not proof that the core phase-6 read-model slice is absent.

### Recommended working assumption

- Use the live climate archetypes, templates, projections, runtime routes, OpenAPI paths, and tests as the authority for the current phase-6 surface.
- Prefer reusing existing v0.8 climate hazard, adaptation profile, agrometeorology, irrigation, and variety-risk semantics whenever they already fit.
- Keep scenario, baseline period, geography resolution, time horizon, uncertainty, and crop-context fit explicit in the fact model.
- Keep adaptation narratives as projection outputs derived from facts and traces; do not store mutable free-form advice as the source of truth.

## Product goal

Phase 6 should answer these parcel questions:

1. Which long-horizon climate shifts are likely to matter on this field?
2. How are frost, heat, dry spells, heavy rainfall or waterlogging pressure, evapotranspiration, and growing season characteristics shifting for this parcel zone?
3. Which adaptation themes are most relevant for this field and crop context: variety choice, sowing or harvest timing, irrigation planning, drainage, frost protection, or crop mix?
4. Is the signal mainly near-term, mid-century, or late-century?
5. How much confidence should the farmer place in the output, given scenario divergence, grid scale, terrain sensitivity, and missing crop context?

Target parcel outputs should stay narrow: monitor, consider adaptation theme, prioritize adaptation review, or not decision-ready.

## Scope boundaries

### In scope

- Scenario-aware climate indicator trends that are relevant to one field.
- Parcel-facing adaptation themes and crop-suitability pressure summaries.
- Horizon-specific and uncertainty-aware planning outputs.
- Reuse of phase-1 to phase-5 parcel state where it materially improves explanation and confidence.
- Reason codes, evidence refs, trace refs, geography fit, and freshness indicators for each conclusion.

### Explicitly out of scope

- Hard compliance blockers or same-day operational legality.
- Deterministic yield forecasting, engineering design, financial ROI modeling, or rate prescriptions.
- Generic climate dashboards or standalone adaptation portals.
- Hiding scenario divergence inside one opaque score.
- New top-level twin entities outside the existing Field-anchored model.

## Working source assumptions

- **Primary Slovenia-first planning source:** ARSO's Atlas podnebnih projekcij and related OPSI resources. Current official pages describe the atlas as a planning aid for adaptation and list drought indicators, agrometeorological variables, reference evapotranspiration, runoff, and groundwater recharge among the covered variables.
- **Primary gridded Slovenia projection source:** ARSO OPSI climate projection resources exposing bias-corrected EURO-CORDEX derived daily data at 0.125° and 30-year aggregated results at 0.125° and 1 km, including temperature, precipitation, and reference evapotranspiration variables.
- **Primary agroclimatic cross-check source:** Copernicus Climate Data Store agroclimatic indicators from 1951 to 2099, with 26 indicators at 0.5° resolution and 10-day, seasonal, or annual temporal outputs.
- **Optional historical alignment source:** Copernicus AgERA5, which provides daily agrometeorological indicators from 1979 to present at 0.1° resolution and is suitable for historical baseline alignment, calibration, and backtesting support.
- **Parcel context reused from earlier phases:** phase-1 identity, geometry, declarations, overlays and evidence log; phase-2 spray-window and plant-health relevance; phase-3 water, nitrate, and flood stewardship; phase-4 EO anomaly and scout-first outputs; phase-5 benchmark and explainability signals when present.
- These are working assumptions for implementation planning. Codex should verify exact adapter paths, licenses, refresh models, and storage patterns in the live repo before implementation.

## Semantic design

### Reuse, do not replace

- Field
- CropInstance
- EvidenceRecord
- EventRecord
- RuleExecutionTrace
- Phase-1 passport facts and projections
- Existing v0.8 agronomy semantics for climate hazards, adaptation profiles, agrometeorology, irrigation, variety trial or risk, crop stage, and remote sensing where already present and usable

### Current repo-backed package layout

| Location | Add or verify |
| --- | --- |
| specs/v0.8/archetypes | FIELD.field_climate_projection_fact.v1.md\nFIELD.field_climate_adaptation_signal.v1.md |
| specs/v0.8/templates | template-field-climate-adaptation-summary-si-v0_8.md\ntemplate-field-climate-suitability-outlook-si-v0_8.md\ntemplate-field-climate-indicator-trends-si-v0_8.md |
| specs/v0.8/templates/projections | template-field-climate-adaptation-summary-si-v0_8.json\ntemplate-field-climate-suitability-outlook-si-v0_8.json\ntemplate-field-climate-indicator-trends-si-v0_8.json |
| specs/v0.8/ontology | farm-rm-v1_7-field-climate-adaptation.ttl |
| specs/v0.8/constraints | farm-rm-v1_7-field-climate-adaptation.shacl.ttl |
| specs/v0.8/sql/migrations | <next>_v1_7_field_climate_projection_fact.sql\n<next>_v1_7_field_climate_adaptation_signal.sql |
| specs/v0.8/reference-ingest/profiles | climate-projection-context-2026.json\nclimate-indicator-trends-2026.json\nclimate-adaptation-signals-2026.json |
| specs/v0.4/regulatory/rulepacks | si-field-ops-climate-adaptation-2026-draft.json |

### Why this split

- `field_climate_projection_fact` preserves normalized, scenario-aware climate context with explicit source provenance, horizon, baseline, geography fit, and uncertainty without pretending that context already equals advice.
- `field_climate_adaptation_signal` stores derived, explainable parcel-level planning conclusions such as water demand increase, frost shift pressure, crop-suitability pressure, or a climate data gap.
- Projection contracts should assemble field-facing planning outputs from those facts plus earlier phase state rather than introducing a mutable current-status climate table.

## Contract boundaries

### field_climate_projection_fact

Purpose: persist parcel-relevant climate indicators and projection context with explicit scenario, horizon, geography, baseline, unit, provenance, and uncertainty.

- Required shape: fieldUri; asOf; planningContextMode; cropInstanceUriOrNull; cropOrVarietyCodeOrNull; sourceSystem; sourceId; sourceVersion; geographyScope; geographyCode; scenarioFamily; scenarioCode; horizonScope; periodStart; periodEnd; baselinePeriod; indicatorCode; indicatorValue; unitCode; aggregationType; uncertaintyClass; freshnessStatus; evidenceRefs.
- `planningContextMode` values: `current_crop | candidate_crop | generic_field`.
- `horizonScope` values: `near_term | mid_century | late_century | cross_horizon | custom`.
- `indicatorCode` examples: `frost_days | heat_stress_days | consecutive_dry_days | heavy_precip_days | growing_season_length | reference_et | seasonal_temp_anomaly | seasonal_precip_anomaly | drought_index | chill_accumulation`.

### field_climate_adaptation_signal

Purpose: store explainable parcel-level climate planning conclusions derived from climate context and parcel state.

- Required shape: fieldUri; asOf; planningContextMode; cropInstanceUriOrNull; signalType; priorityLevel; horizonScope; confidenceStatus; recommendedThemes; reasonCodes; traceRefs; evidenceRefs.
- `signalType` values: `warmingTrend | frostShiftRisk | heatStressRisk | waterDemandIncrease | heavyRainRunoffRisk | waterloggingRisk | phenologyShift | cropSuitabilityPressure | adaptationOpportunity | climateDataGap`.
- `priorityLevel` values: `low | medium | high | exploratory`.
- `recommendedThemes` values: `review_variety | review_sowing_window | review_irrigation | review_drainage | review_frost_protection | review_crop_mix | review_soil_cover | gather_more_evidence | no_change | unknown`.

### Projection contracts

| Projection | Required surface |
| --- | --- |
| template-field-climate-adaptation-summary-si-v0_8.json | fieldUri, asOf, planningContext, topSignals, horizonSummary, recommendedThemes, confidenceSummary, evidenceGaps, evidenceRefs, traceRefs |
| template-field-climate-suitability-outlook-si-v0_8.json | fieldUri, asOf, cropOrVarietyContext, horizonRows, indicatorHighlights, suitabilityPressureSummary, evidenceRefs, traceRefs |
| template-field-climate-indicator-trends-si-v0_8.json | fieldUri, asOf, indicatorRows, scenarioSet, baselinePolicy, geographyFitSummary, freshnessSummary, evidenceRefs, traceRefs |

## Authority model and conflict resolution

| Concern | Authority holder | Phase-6 behavior |
| --- | --- | --- |
| Parcel identity and geometry | Phase-1 official links and geometry snapshots | Reused unchanged. Climate context never mutates parcel authority. |
| Operational climate state | Phase-2 or phase-3 daily weather and agromet context | Used for daily decisions; keeps priority for operational timing over long-horizon climate planning. |
| Long-horizon climate context | field_climate_projection_fact plus evidence refs | Scenario-aware, time-bounded context with explicit uncertainty. |
| Adaptation conclusion | field_climate_adaptation_signal plus trace | Derived and explainable; not a legal or cadastral truth. |
| Compliance authority | Earlier rule layers | Climate adaptation can inform review priorities, not override allow/block outcomes. |

### Conflict handling rules

- If multiple scenarios diverge materially, expose a range or scenario set instead of collapsing to one opaque number.
- If ARSO and C3S indicators differ in scale, coverage, or semantics, keep source-specific interpretation explicit rather than blending them into one hidden composite.
- If same-season observations contradict long-run trend context, keep both: operational now versus structural trend.
- If crop context is missing or candidate crop is unknown, degrade gracefully to generic field planning rather than forcing crop-specific advice.
- If grid scale is too coarse for terrain-sensitive frost or ponding behavior, reduce confidence and ask for human review instead of over-claiming parcel precision.

## Evaluation categories

- Projection source quality and freshness
- Geography or downscaling fit
- Scenario coverage and divergence
- Baseline normalization
- Temperature and growing-season shift
- Frost, chill, or vernalization shift
- Heat stress and water demand trend
- Heavy precipitation, runoff, or waterlogging trend
- Crop or variety suitability pressure
- Adaptation theme prioritization
- Evidence sufficiency and uncertainty communication

## API surface and runtime behavior

| Surface | Purpose | Notes |
| --- | --- | --- |
| GET /v1/fields/{fieldUri}/climate-plan-tab | Return the field-facing climate Plan tab as one capability-gated projection | Production clients should render only cards that the payload returns and must not synthesize `Later` placeholders. |
| GET /v1/fields/{fieldUri}/climate-adaptation-summary | Return parcel-facing climate planning summary | Advisory only; must expose uncertainty, horizon, and evidence. |
| GET /v1/fields/{fieldUri}/climate-suitability-outlook | Return crop or variety suitability pressure by horizon | Should degrade gracefully when crop context is generic or candidate-only. |
| GET /v1/fields/{fieldUri}/climate-indicator-trends | Return structured climate indicator rows for the parcel zone | No raw external dataset dumping in the core response. |
| POST /v1/fields/{fieldUri}/climate/evaluate | Refresh or recompute climate context and adaptation signals | Optional later if runtime convention prefers explicit recomputation. |
| Capability flags | fieldClimatePlanning and the supporting phase-6 per-card flags plus fieldClimateAdaptationSummary, fieldClimateSuitabilityOutlook, fieldClimateIndicatorTrends | Already live in the runtime capabilities payload; keep future naming aligned to that payload. |

## Refresh and evaluation flow

1. Resolve Field, crop context, production profile, geometry, geography mappings, and terrain-sensitive context from the parcel passport.
2. Load earlier parcel state from phases 1-5 when available: declarations, overlays, spray-window and plant-health signals, water or flood stewardship, EO anomaly state, and benchmark or explainability context.
3. Read or refresh climate projection context from the configured ARSO and Copernicus adapters.
4. Persist `field_climate_projection_fact` records with source provenance, scenario, horizon, baseline, geography fit, indicator values, and uncertainty metadata.
5. Run adaptation logic that derives parcel-facing signals such as water-demand increase, frost-shift pressure, crop-suitability pressure, or data-gap outcomes.
6. Compile the climate-adaptation-summary, climate-suitability-outlook, and climate-indicator-trends projections.
7. Persist EventRecord and RuleExecutionTrace references, then return the projections without mutating compliance truth.

## Current repo proof

- phase-6 archetypes, templates, projections, runtime routes, OpenAPI paths, and field-passport tests exist in the live repo
- fixture coverage already exists for climate-adaptation-summary, climate-suitability-outlook, climate-indicator-trends, and climate plan-tab behavior
- review must still confirm that no hard compliance blocker, deterministic prescription, or fake parcel precision is produced solely from long-horizon climate projections

## Remaining future acceptance for later hardening

- any optional explicit `POST /v1/fields/{fieldUri}/climate/evaluate` recompute surface
- deeper climate-source adapter hardening or replay expansion beyond the current read-model slice
- later planning-signal refinement that preserves uncertainty and does not reintroduce “Later” placeholders or false precision

## Codex implementation instructions for any later phase-6 widening

1. Start from the live climate archetypes, templates, projections, routes, tests, and capability flags rather than recreating them.
2. Audit the live repo first for climate hazard, adaptation profile, agrometeorology, irrigation, variety-risk, and scenario-bearing assets before widening the slice.
3. Keep scenario, horizon, baseline, geography fit, and uncertainty explicit in every imported climate fact.
4. Keep climate outputs advisory and planning-oriented; they may influence review priorities, but they must not become legal authority or same-day operational legality.
5. Add explicit recompute endpoints or richer climate-source handling only when the live repo proves a real need beyond the current read-model surface.
6. Do not compress multiple scenarios into one opaque score and do not bury uncertainty inside free-form narrative text.
7. Stop before building a generic climate portal; this phase exists to explain one parcel and its likely adaptation themes.

### Recommended implementation sequence

1. Treat the live archetypes, templates, projections, routes, tests, and climate plan-tab mapping note as the current baseline.
2. Audit whether richer climate-source adapter coverage or recompute flows are truly needed beyond the current read-model slice.
3. Add explicit recompute endpoints only when the runtime proves a real need for them.
4. Only then expand to richer planning themes or source integrations.

## What comes after phase 6

- After phase 6, the highest-value next step is not another domain layer; it is cross-phase integration, acceptance gating, and implementation sequencing across phases 1 through 6.
- That means dependency tracking, rollout order, reusable adapter design, and a single integration checklist for Codex or human reviewers.

## Official source notes

These are working assumptions for implementation planning, not repo-confirmed adapters.

- ARSO / GOV.SI Atlas podnebnih projekcij: https://www.gov.si/novice/2022-01-20-atlas-podnebnih-projekcij-za-slovenijo-do-leta-2100/
- ARSO atlas application: https://meteo.arso.gov.si/uploads/probase/www/climate/OPS21/Priloge-app/
- ARSO OPSI 0.125° daily projection resource (bias-corrected EURO-CORDEX): https://podatki.gov.si/dataset/arsopodnebne-spremembe-projekcije-visine-padavin-dnevni-podatki-scenarij-rcp4-5-locljivost-0-125/resource/6529f8b8-8224-4904-bee5-a392478bced2
- ARSO OPSI 30-year results resource (0.125° and 1 km): https://podatki.gov.si/dataset/arsopodnebne-spremembe-rezultati-odkloni-osnovnih-spremenljivk-za-30-letna-obdobja-in-sedanje-stanje/resource/57bb3eba-ee15-45ba-b2ec-668a5de551ea
- Copernicus Climate Data Store - agroclimatic indicators: https://cds.climate.copernicus.eu/datasets/sis-agroclimatic-indicators
- Copernicus Climate Data Store - AgERA5: https://cds.climate.copernicus.eu/datasets/sis-agrometeorological-indicators?tab=overview
