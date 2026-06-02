# Phase 4 Spec - EO Anomaly & Scout-First Engine

Parcel-centric compliance twin, Slovenia-first, built on the Phase 1 field compliance passport

Date: 2026-03-08

## Executive decision

- The original phase-4 planning slice is now materially implemented as repo-native archetypes, templates, projections, runtime routes, OpenAPI paths, and field-passport tests.
- Live repo evidence now includes:
  - `FIELD.field_eo_observation_fact.v1.md`
  - `FIELD.field_anomaly_signal.v1.md`
  - `template-field-eo-anomaly-triage-si-v0_8.md`
  - `template-field-phenology-status-si-v0_8.md`
  - `template-field-scout-priority-queue-si-v0_8.md`
  - `GET /v1/fields/{fieldUri}/eo-anomaly`
  - `GET /v1/fields/{fieldUri}/phenology-status`
  - `GET /v1/farms/{farmUri}/scout-priority-queue`
- Remaining future work is narrower: optional explicit refresh/recompute endpoints, richer EO adapter hardening, and any later cross-phase explainability tightening.
- Phase 4 remains advisory and scout-first. The live read-model slice still must not become legal or compliance authority.

## Repo-grounded baseline

### Observed current state

- Markdown archetypes and templates are the human authoring layer; generated artifacts are derived from them.
- The semantic backbone already includes Field, CropInstance, append-only semantics, EvidenceRecord, EventRecord, and RuleExecutionTrace.
- The repo already has a template projection layer for app-facing workflows.
- The repo now contains repo-native EO observation/anomaly archetypes plus authored phase-4 templates and projection contracts.
- The runtime now exposes the EO anomaly, phenology-status, and scout-priority-queue read models and covers them in field-passport route tests and OpenAPI route-alignment tests.
- Rulepacks live under specs/v0.4/regulatory/rulepacks/.
- Current extension work is concentrated under specs/v0.8/.
- Runtime contracts are strongest in FastAPI/Pydantic; static OpenAPI can lag.
- The runtime already loads spec assets from the repo and has SHACL, DB smoke, and FastAPI test entrypoints.

### Evidence-backed inference

- Phase 4 did extend the parcel passport rather than create a second parcel-state subsystem.
- The current repo-backed shape already keeps Field and CropInstance as anchors, persists EO observations and anomaly signals append-only, and exposes scout-first projections rather than a raw-imagery dashboard.
- New EO semantic work already landed in v0.8 for the core slice; later rulepack or adapter hardening still belongs in follow-up work rather than a second semantic family.
- EO outputs should stay advisory. They can influence scouting and explainability, but they should not silently overrule official geometry, declaration, or regulatory overlays.

### Recommended working assumption

- Use the live EO archetypes, templates, projections, runtime routes, OpenAPI paths, and tests as the authority for the current phase-4 surface.
- Use parcel statistics, quality flags, provenance, and rule traces as the stable contract layer; do not make raw raster payloads part of the core API contracts.
- Keep scout priority as a projection-level output. Do not force EO triage into legal allow-block semantics just for symmetry.
- Treat any later EO adapter or refresh endpoint work as additive hardening, not as proof that the current phase-4 read models are missing.

## Product goal

Phase 4 should answer these parcel questions:

1. Which field needs inspection first today?
2. Is this parcel showing a persistent anomaly or a one-off/noisy observation?
3. Does the anomaly look like delayed emergence, growth lag, abnormal heterogeneity, standing-water suspicion, or disturbance suspicion?
4. Is crop development broadly aligned with expected parcel and season context?
5. What evidence supports the answer, and what is missing or stale?

Outputs should stay narrow and advisory: `inspect now`, `inspect later`, `monitor`, `reacquire`, or `not decision-ready`.

## Scope boundaries

### In scope

- Parcel-level EO observation facts and quality-aware anomaly signals
- Scout-first triage outputs: inspect now, inspect later, monitor, or reacquire due to insufficient data
- Phenology alignment as an advisory status, not a black-box diagnosis
- Cross-sensor reasoning when radar and optical evidence both exist
- Explainable anomaly categories with reason codes, evidence refs, and trace refs
- Farm-scoped scout-priority queue built from parcel signals

### Explicitly out of scope

- Full raw-imagery browsing UX as the primary product surface
- Automated disease diagnosis or treatment prescription
- Yield forecasting, prescription maps, or rate optimization
- Using EO alone as a legal or compliance blocker
- Creating a second top-level digital-twin entity
- Generic dashboard sprawl outside the parcel passport model

## Working source assumptions

- Primary EO backend: a near-data compute adapter such as CDSE/openEO or an equivalent parcel-statistics backend.
- Primary parcel context: phase-1 field passport facts for identity, geometry, declaration, and overlays.
- Primary crop and season context: CropInstance plus declaration snapshot and any existing crop-stage semantics.
- Supporting context: weather/agromet, terrain, and water-stewardship facts where available.
- Baseline strategy: use same-field history first when available; otherwise fall back to crop and seasonal expectation logic.
- Vendor-specific job identifiers may be preserved as provenance, but they must not become core semantic identifiers.

Important: EO is an advisory evidence layer here. It is not a replacement for official parcel identity, legal declaration, or regulatory overlays.

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

### Current repo-backed package layout

| Location | Add |
|---|---|
| `specs/v0.8/archetypes` | `FIELD.field_eo_observation_fact.v1.md
FIELD.field_anomaly_signal.v1.md` |
| `specs/v0.8/templates` | `template-field-eo-anomaly-triage-si-v0_8.md
template-field-phenology-status-si-v0_8.md
template-field-scout-priority-queue-si-v0_8.md` |
| `specs/v0.8/templates/projections` | `template-field-eo-anomaly-triage-si-v0_8.json
template-field-phenology-status-si-v0_8.json
template-field-scout-priority-queue-si-v0_8.json` |
| `specs/v0.8/ontology` | `farm-rm-v1_7-field-eo-scout.ttl` |
| `specs/v0.8/constraints` | `farm-rm-v1_7-field-eo-scout.shacl.ttl` |
| `specs/v0.8/sql/migrations` | `<next>_v1_7_field_eo_observation_fact.sql
<next>_v1_7_field_anomaly_signal.sql` |
| `specs/v0.8/reference-ingest/profiles` | `eo-parcel-stats-2026.json
eo-phenology-baseline-2026.json
eo-scout-ranking-2026.json` |
| `specs/v0.4/regulatory/rulepacks` | `si-field-ops-eo-scout-2026-draft.json` |

### Why this split

- field_eo_observation_fact stores parcel-level EO summaries, quality, and provenance without pretending that EO is already interpretation.
- field_anomaly_signal stores explainable parcel-level interpretations such as growth lag or standing-water suspicion.
- Phenology status and scout queue should be projections assembled from those facts, not mutable current-status tables.
- If the runtime later wants a bridge into action evaluation for scouting, add that as a mapping layer rather than mutating EO meaning now.

## Contract boundaries

### `field_eo_observation_fact`

Purpose: preserve parcel-level EO summaries, quality, and provenance without pretending that observation already equals interpretation.

Required shape:

- fieldUri; cropInstanceUri; asOf; sourceSystem; sourceId; sourceVersion; sourceWindow; geometryRef
- observationType (optical_stats | radar_stats | multi_sensor_summary); sensorSet (optical | radar | multi)
- coveragePct; qualityStatus (usable | partial | poor | unusable | unknown); cloudOrNoiseStatus (clear | limited | obstructed | not_applicable | unknown)
- changeContext (stable | shifted | unknown); moistureProxyStatus (dry | balanced | wet | saturated | unknown)
- heterogeneityStatus (uniform | patchy | highly_variable | unknown); phenologyProxyStatus (behind | aligned | ahead | unknown)
- derivedMetricCodes; supportContextStatus; evidenceRefs

### `field_anomaly_signal`

Purpose: store explainable parcel-level EO interpretations and scout relevance.

Required shape:

- fieldUri; cropInstanceUri; asOf; signalType
- signalType values: delayedEmergence | growthLag | abnormalHeterogeneity | standingWaterSuspicion | disturbanceSuspicion | phenologyMismatch | dataQualityGap
- signalLevel (low | watch | elevated | high | unknown); persistenceStatus (single | repeated | persistent | unknown)
- crossSensorStatus (unconfirmed | optical_only | radar_only | cross_confirmed | unknown); phenologyStatus (behind | aligned | ahead | unknown)
- scoutPriority (none | low | normal | high | urgent); recommendedNextStep (none | monitor | reacquire | scout_later | scout_now | compare_history | candidate_check)
- reasonCodes; traceRefs; evidenceRefs

### Projection contracts

| Projection | Required surface |
|---|---|
| `template-field-eo-anomaly-triage-si-v0_8.json` | fieldUri, asOf, activeCropInstanceUri, topSignals, dataQualitySummary, phenologySummary, scoutRecommendation, requiredEvidence, traceRefs, evidenceRefs |
| `template-field-phenology-status-si-v0_8.json` | fieldUri, asOf, activeCropInstanceUri, stageStatus, confidenceStatus, baselineSummary, contributingSignals, evidenceGaps, traceRefs, evidenceRefs |
| `template-field-scout-priority-queue-si-v0_8.json` | farmUri, asOf, queueItems, rankingPolicyVersion, filters, evidencePolicy, traceRefs, evidenceRefs |

## Authority model and conflict resolution

| Concern | Authority holder | Phase-4 behavior |
|---|---|---|
| Parcel identity and geometry | Phase-1 official links and geometry snapshots | Reused. EO never mutates legal or official parcel identity. |
| Crop and season context | CropInstance plus declaration snapshot | EO is interpreted against this context; missing crop context reduces confidence. |
| EO acquisition facts | field_eo_observation_fact plus evidence refs | Time-bounded advisory observations with explicit provenance and quality. |
| Anomaly interpretation | field_anomaly_signal plus rule trace | Derived and explainable. No silent overreach into legal truth. |
| Scout ordering | Scout-priority queue projection | Farm-scoped prioritization, not a new historical truth table. |
| Compliance authority | Phase-1 to phase-3 layers and rulepacks | EO can inform attention and explanation, but it does not overrule compliance state. |

Conflict handling rules:

- If geometry is stale or crop context is missing, degrade confidence and surface evidence gaps instead of inventing certainty.
- If optical and radar disagree, persist the disagreement as crossSensorStatus and prefer confirmation over silent winner selection.
- If anomaly severity is high but data quality is poor, prefer reacquire or scout confirmation, not diagnosis.

## Evaluation categories

- Acquisition quality and freshness
- Baseline fit and phenology alignment
- Within-field heterogeneity and outlier detection
- Moisture or standing-water suspicion
- Abrupt disturbance suspicion
- Persistence and cross-sensor confirmation
- Scout prioritization
- Evidence sufficiency

## API surface and runtime behavior

| Surface | Purpose | Notes |
|---|---|---|
| `GET /v1/fields/{fieldUri}/eo-anomaly` | Return parcel anomaly triage projection | Read model over observation facts, anomaly signals, traces, and evidence. |
| `GET /v1/fields/{fieldUri}/phenology-status` | Return advisory phenology alignment summary | Should degrade gracefully when baseline quality is weak. |
| `GET /v1/farms/{farmUri}/scout-priority-queue` | Return ranked queue of fields to inspect | Farm-scoped projection; not a persisted mutable queue table. |
| `POST /v1/fields/{fieldUri}/eo/evaluate` | Refresh or recompute EO-derived facts and projections | Optional later if runtime convention prefers explicit recomputation. |
| `Capability flags` | fieldEoAnomaly, fieldPhenologyStatus, fieldScoutPriorityQueue | Already live in the runtime capabilities payload; keep future naming aligned to that payload. |

## Refresh and evaluation flow

1. Resolve Field, active CropInstance, declaration context, and selected compliance geometry.
2. Read latest parcel EO source payloads or call the adapter that materializes parcel statistics.
3. Persist field_eo_observation_fact records with coverage, quality, and provenance.
4. Compare the parcel against recent history and baseline expectation.
5. Derive field_anomaly_signal records with reason codes and cross-sensor status.
6. Compile parcel-level anomaly triage and phenology projections.
7. Rank the farm-scoped scout queue using signal severity, persistence, freshness, and evidence confidence.
8. Persist EventRecord and RuleExecutionTrace references, then return the projections.

## Current repo proof

- phase-4 archetypes, templates, projections, runtime routes, OpenAPI paths, and field-passport tests exist in the live repo
- fixture coverage already exists for clear optical growth lag, missing observations that force `reacquire`, phenology alignment, and farm-scoped scout prioritization
- review must still confirm that no legal compliance blocker is produced solely from EO outputs

## Remaining future acceptance for later hardening

- any optional explicit `POST /v1/fields/{fieldUri}/eo/evaluate` recompute surface
- richer EO adapter/runtime hardening beyond the current read-model slice
- any later cross-phase explainability tightening that reuses phase-4 signals without widening them into legal authority

## Codex implementation instructions for any later phase-4 widening

1. Start from the live EO archetypes, templates, projections, routes, tests, and capability flags rather than recreating them.
2. Audit the live repo first for existing EO, scouting, observation, remote-sensing, and phenology assets before widening the slice.
3. Keep parcel-statistics contracts stable and provenance-rich; do not make raw imagery or vendor-specific job objects part of the core API schema.
4. Add explicit recompute endpoints or richer adapter handling only when the live repo proves a real need beyond the current read-model surface.
5. Keep outputs advisory and scout-first; do not widen the slice into diagnosis, yield forecasting, or generic dashboarding.
6. Document unresolved authority, baseline, and equivalence questions in the PR memo rather than hiding them in code.

## Review cautions

- Do not duplicate existing v0.8 EO or scouting semantics if equivalent assets already exist.
- Do not let EO-derived suspicion silently mutate official geometry, declaration, or regulatory overlay facts.
- Do not collapse uncertainty into false precision. Surface evidence gaps, low confidence, and sensor disagreement explicitly.
- Do not store large raw raster payloads inside core persistence contracts for this phase.

## Grounding files to read first

- `AI_ONBOARDING.md`
- `20-semantic-core.md`
- `30-runtime-architecture.md`
- `50-compliance-and-reporting.md`
- `70-implementation-status.md`

## Next item after phase 4

Regional benchmark and explainability layer.
