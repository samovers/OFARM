# Phase 5 Spec - Regional Benchmark & Explainability Layer

Parcel-centric compliance twin, Slovenia-first, built on the phase-1 field compliance passport

Date: 2026-03-09

## Executive decision

- The original phase-5 planning slice is now materially implemented as repo-native archetypes, templates, projections, runtime routes, OpenAPI paths, and field-passport tests.
- Live repo evidence now includes:
  - `FIELD.field_benchmark_context_fact.v1.md`
  - `FIELD.field_explainability_signal.v1.md`
  - `template-field-benchmark-context-si-v0_8.md`
  - `template-field-explainability-summary-si-v0_8.md`
  - `template-field-regional-comparison-si-v0_8.md`
  - `GET /v1/fields/{fieldUri}/benchmark-context`
  - `GET /v1/fields/{fieldUri}/explainability-summary`
  - `GET /v1/fields/{fieldUri}/regional-comparison`
- Remaining future work is narrower: deeper benchmark-source adapter hardening, any later rulepack tightening, and importer/replay expansion beyond the current read-model slice.
- Phase 5 stays parcel-centric. Benchmark context remains advisory and explanatory; the live slice must not become legal authority or silently overrule field-level official geometry, declarations, or rulepack outcomes.

## Repo-grounded baseline

### Observed current state

- Markdown archetypes and templates are the human authoring layer; generated artifacts are derived from them. Repo evidence: 00-index.md, 90-glossary.md.
- The semantic backbone already includes Field, CropInstance, append-only semantics, EvidenceRecord, EventRecord, and RuleExecutionTrace. Repo evidence: 20-semantic-core.md, 90-glossary.md.
- The repo already has a template projection layer for app-facing workflows and a test path for projection contracts. Repo evidence: 20-semantic-core.md, 40-api-and-data-contracts.md, 60-build-run-test-generate.md.
- The repo now contains repo-native benchmark/explainability archetypes plus authored phase-5 templates and projection contracts.
- The runtime now exposes benchmark-context, explainability-summary, and regional-comparison read models and covers them in field-passport route tests and OpenAPI route-alignment tests.
- Rulepacks live under specs/v0.4/regulatory/rulepacks/, while active extension work is concentrated under specs/v0.8/. Repo evidence: 10-repo-map.md, 50-compliance-and-reporting.md, 70-implementation-status.md.
- The runtime loads spec assets from the repo and relies on FastAPI/Pydantic contracts, SHACL checks, DB smoke checks, and backend tests. Repo evidence: 30-runtime-architecture.md, 60-build-run-test-generate.md.

### Evidence-backed inference

- Phase 5 did extend the parcel passport rather than create a separate benchmark subsystem.
- The current repo-backed shape already persists time-bounded benchmark context facts append-only, derives explainability signals from those facts plus parcel state, and exposes field-focused benchmark/explainability projections.
- New benchmark/explainability semantic work already landed in specs/v0.8 for the core slice; later rulepack or adapter hardening still belongs in follow-up work rather than a second semantic family.
- Benchmark outputs should stay contextual: they explain a field, they do not replace parcel observations or become a hard compliance blocker.

### Recommended working assumption

- Use the live benchmark/explainability archetypes, templates, projections, runtime routes, OpenAPI paths, and tests as the authority for the current phase-5 surface.
- Keep geography, crop code, unit normalization, source provenance, and freshness explicit in the fact model.
- Keep narrative explanation as a projection-level output derived from facts, signals, and traces; do not store mutable free-form stories as the source of truth.
- Treat any later benchmark-source importer or rulepack work as additive hardening, not as proof that the current phase-5 read models are missing.

## Product goal

Phase 5 should answer these parcel questions:

1. Is this parcel issue local to the field, or is the whole municipality, region, or crop zone under similar stress?
2. How does this field compare with relevant official context for this crop, place, and season?
3. What official benchmark helps explain a weak field signal: crop-condition context, drought stress, production pattern, price pressure, or input-cost pressure?
4. Which explanation is strongest, and what evidence is missing or stale?
5. What should the farmer do next: inspect locally, wait for regional normalization, verify the crop declaration, or gather more evidence?

Outputs should stay narrow and explainable: local issue likely, partly regional, largely regional, market/context pressure only, monitor, or not decision-ready.

## Scope boundaries

### In scope

- Regional context for crop-condition, weather/drought, production, area, and market modules where they materially explain a parcel state.
- Parcel-facing comparison against municipality, statistical region, cohesion region, national, EU, or agroclimatic benchmark strata, depending on source availability.
- Explainability outputs that connect field state from phases 1-4 to regional evidence and state whether the parcel is a local outlier or part of a broader pattern.
- Reason codes, evidence refs, trace refs, and freshness indicators for every conclusion.

### Explicitly out of scope

- Generic BI dashboards or standalone market portals.
- Legal allow-block decisions based solely on benchmark context.
- Precise parcel yield forecasting or rate recommendations.
- Replacing field observations with coarse regional averages.
- New top-level twin entities outside the existing Field-anchored model.

## Working source assumptions

- Primary Slovenia statistics context: SURS SiStat / PxWeb for agriculture tables and regional/national indicators.
- Primary EU comparison context: Eurostat REST datasets for area, production, structural, and regional comparisons.
- Primary crop-condition and yield context: JRC MARS and public Agri4Cast resources for seasonal regional interpretation.
- Primary market and input context: DG AGRI Agri-food Data Portal modules such as cereals, oilseeds, fertiliser, organic, and related commodity dashboards.
- Parcel state context reused from earlier phases: passport identity/geometry/declarations, weather and plant-health signals, water/nitrate/flood signals, and EO anomaly status.
- Geography mapping layer: municipality, statistical region, cohesion region, NUTS, and optional agroclimatic grouping.

These are working assumptions for implementation planning. Codex should verify the exact adapter path, format, licensing, and refresh model in the live repo before implementation.

## Semantic design

### Reuse, do not replace

- Field
- CropInstance
- EvidenceRecord
- EventRecord
- RuleExecutionTrace
- Phase-1 passport facts
- Phase-2 plant-health facts if present
- Phase-3 water and stewardship facts if present
- Phase-4 EO anomaly and phenology facts if present

### Current repo-backed package layout

| Location | Add |
| --- | --- |
| specs/v0.8/archetypes | FIELD.field_benchmark_context_fact.v1.md
FIELD.field_explainability_signal.v1.md |
| specs/v0.8/templates | template-field-benchmark-context-si-v0_8.md
template-field-explainability-summary-si-v0_8.md
template-field-regional-comparison-si-v0_8.md |
| specs/v0.8/templates/projections | template-field-benchmark-context-si-v0_8.json
template-field-explainability-summary-si-v0_8.json
template-field-regional-comparison-si-v0_8.json |
| specs/v0.8/ontology | farm-rm-v1_7-field-benchmark-explainability.ttl |
| specs/v0.8/constraints | farm-rm-v1_7-field-benchmark-explainability.shacl.ttl |
| specs/v0.8/sql/migrations | <next>_v1_7_field_benchmark_context_fact.sql
<next>_v1_7_field_explainability_signal.sql |
| specs/v0.8/reference-ingest/profiles | regional-benchmark-context-2026.json
regional-market-context-2026.json
regional-explainability-2026.json |
| specs/v0.4/regulatory/rulepacks | si-field-ops-benchmark-explainability-2026-draft.json |

### Why this split

- field_benchmark_context_fact preserves normalized contextual metrics with geography, crop, period, unit, provenance, and freshness without pretending that context already equals explanation.
- field_explainability_signal stores derived, explainable conclusions such as local outlier likely, regional stress context, or market pressure context.
- Projection contracts should assemble field-facing explanations from those facts plus phase-1 to phase-4 parcel state, instead of writing mutable current-status tables.

## Contract boundaries

### field_benchmark_context_fact

Purpose: persist parcel-relevant regional benchmark metrics with explicit geography, period, unit, source provenance, and freshness.

- Required shape: fieldUri; cropInstanceUri; asOf; sourceSystem; sourceId; sourceVersion; geographyScope; geographyCode; benchmarkDomain; metricCode; metricValue; unitCode; periodType; periodStart; periodEnd; cropOrCommodityCode; baselineType; freshnessStatus; confidenceStatus; evidenceRefs.
- benchmarkDomain values: crop_condition | production_area | production_volume | yield_context | price_context | input_cost_context | climate_stress_context | drought_context | market_context.
- geographyScope values: municipality | statistical_region | cohesion_region | national | eu | nuts2 | nuts3 | agroclimatic_zone | custom.
- baselineType values: current | rolling_average | recent_average | seasonal_normal | anomaly | percentile | index | unknown.

### field_explainability_signal

Purpose: store explainable parcel-level conclusions derived from benchmark context and parcel state.

- Required shape: fieldUri; cropInstanceUri; asOf; signalType; signalLevel; localityStatus; confidenceStatus; recommendedNextStep; reasonCodes; traceRefs; evidenceRefs.
- signalType values: localOutlierContext | regionalStressContext | widespreadDelayContext | widespreadWaterStressContext | marketPressureContext | benchmarkGap | mixedSignalContext | dataCoverageGap.
- localityStatus values: local_only | partly_regional | largely_regional | national_pattern | eu_pattern | mixed | unknown.
- recommendedNextStep values: inspect_local | monitor_region | gather_more_evidence | verify_crop_context | check_market_exposure | no_action | unknown.

### Projection contracts

| Projection | Required surface |
| --- | --- |
| template-field-benchmark-context-si-v0_8.json | fieldUri, asOf, activeCropInstanceUri, geographyStrata, keyIndicators, freshnessSummary, evidenceRefs, traceRefs |
| template-field-explainability-summary-si-v0_8.json | fieldUri, asOf, activeCropInstanceUri, topSignals, localityConclusion, confidenceSummary, recommendedNextStep, evidenceGaps, evidenceRefs, traceRefs |
| template-field-regional-comparison-si-v0_8.json | fieldUri, asOf, activeCropInstanceUri, comparisonRows, selectedDomains, normalizationPolicyVersion, evidencePolicy, evidenceRefs, traceRefs |

## Authority model and conflict resolution

| Concern | Authority holder | Phase-5 behavior |
| --- | --- | --- |
| Parcel identity and geometry | Phase-1 official links and geometry snapshots | Reused unchanged. Benchmark context never mutates official parcel identity. |
| Crop and season context | CropInstance plus declaration snapshot | Benchmark matching depends on this context; missing or ambiguous crop context reduces confidence. |
| Regional benchmark facts | field_benchmark_context_fact plus evidence refs | Time-bounded contextual facts with geography, period, unit, and provenance. |
| Explainability outcome | field_explainability_signal plus rule trace | Derived and explainable; not a legal or cadastral truth. |
| Compliance authority | Phase-1 to phase-3 rule layers | Regional context can explain a decision or risk, but it does not overrule the decision itself. |

### Conflict handling rules

- If crop mapping to benchmark series is weak, degrade confidence and expose a benchmarkGap or dataCoverageGap signal instead of forcing a comparison.
- If parcel signals are severe but regional context is mild, preserve the parcel as a likely local outlier rather than smoothing it away.
- If market or price context is stale relative to parcel events, surface it as background context only, not as a top explanation.
- If multiple benchmark domains disagree, keep the disagreement explicit through mixedSignalContext and reason codes rather than collapsing to a single narrative.

## Evaluation categories

- Benchmark acquisition quality and freshness
- Geography and crop mapping fit
- Regional crop-condition context
- Regional drought or climate-stress context
- Production and area context
- Market and input-cost context
- Local outlier versus regional pattern inference
- Evidence sufficiency and explanation confidence

## API surface and runtime behavior

| Surface | Purpose | Notes |
| --- | --- | --- |
| GET /v1/fields/{fieldUri}/benchmark-context | Return parcel-relevant official benchmark context | Read model over normalized benchmark facts, evidence, and traces. |
| GET /v1/fields/{fieldUri}/explainability-summary | Return local-versus-regional explanation summary for the parcel | Should remain advisory and evidence-backed. |
| GET /v1/fields/{fieldUri}/regional-comparison | Return structured comparison rows for selected benchmark domains | No raw external dataset dumping in the core response. |
| POST /v1/fields/{fieldUri}/benchmark/evaluate | Refresh or recompute benchmark facts and explainability signals | Optional later if runtime convention prefers explicit recomputation. |
| Capability flags | fieldBenchmarkContext, fieldExplainabilitySummary, fieldRegionalComparison | Already live in the runtime capabilities payload; keep future naming aligned to that payload. |

## Refresh and evaluation flow

1. Resolve Field, active CropInstance, declaration context, and relevant geography mappings.
2. Load the parcel state from phases 1-4: compliance passport, spray-window or plant-health signals, water/flood/nitrate signals, and EO anomaly status where available.
3. Read or refresh normalized benchmark context from the configured source adapters.
4. Persist field_benchmark_context_fact records with geography, crop or commodity scope, period, metric, unit, provenance, and freshness.
5. Run explainability logic that compares parcel state against benchmark context and emits field_explainability_signal records.
6. Compile benchmark-context, explainability-summary, and regional-comparison projections.
7. Persist EventRecord and RuleExecutionTrace references, then return the projections.

## Current repo proof

- phase-5 archetypes, templates, projections, runtime routes, OpenAPI paths, and field-passport tests exist in the live repo
- fixture coverage already exists for benchmark-context, explainability-summary, regional-comparison, and benchmark-context importer behavior
- review must still confirm that benchmark outputs remain contextual and do not silently become compliance decisions

## Remaining future acceptance for later hardening

- any optional explicit `POST /v1/fields/{fieldUri}/benchmark/evaluate` recompute surface
- deeper benchmark-source importer or replay expansion beyond the current read-model slice
- any later rulepack tightening that reuses phase-5 signals without turning them into legal authority

## Codex implementation instructions for any later phase-5 widening

1. Start from the live benchmark/explainability archetypes, templates, projections, routes, tests, and importer seams rather than recreating them.
2. Audit the live repo first for existing benchmark, statistics, reporting, market, explainability, and regional-reference assets before widening the slice.
3. Keep the implementation narrow: normalize benchmark facts, derive explainability signals, expose parcel-facing projections, and avoid generic dashboard surfaces.
4. Preserve sourceSystem, sourceId, sourceVersion, geography scope, crop mapping basis, period bounds, and freshness on every imported contextual fact.
5. Add explicit recompute endpoints, importer expansion, or later rulepack tightening only when the live repo proves a real need beyond the current read-model surface.
6. Do not let benchmark context change official parcel authority, hard compliance state, or crop declaration truth.

### Recommended implementation sequence

1. Treat the live archetypes, templates, projections, routes, tests, and importer seams as the current baseline.
2. Audit whether richer benchmark-source importer coverage or rulepack tightening is truly needed beyond the current read-model slice.
3. Add explicit recompute endpoints only when the runtime proves a real need for them.
4. Only then expand to richer benchmark domains or market modules.

## Next phase

The next item after phase 5 is the climate adaptation layer. It should stay second-wave and planning-oriented, using the same parcel-first evidence and explainability discipline.
