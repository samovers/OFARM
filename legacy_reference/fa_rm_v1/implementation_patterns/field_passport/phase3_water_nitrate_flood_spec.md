# Phase 3 Spec — Water, Nitrate & Flood Stewardship

Parcel-centric compliance twin, Slovenia-first, built on the Phase 1 field compliance passport

Date: 2026-03-08

## Executive decision

- The original phase-3 planning slice is now materially implemented as repo-native archetypes, templates, projections, runtime routes, OpenAPI paths, and field-passport tests.
- Live repo evidence now includes:
  - `FIELD.field_water_balance_fact.v1.md`
  - `FIELD.field_stewardship_signal.v1.md`
  - `template-field-water-stewardship-si-v0_8.md`
  - `template-field-nitrogen-application-check-si-v0_8.md`
  - `template-field-irrigation-readiness-si-v0_8.md`
  - `GET /v1/fields/{fieldUri}/water-stewardship`
  - `POST /v1/fields/{fieldUri}/water-stewardship/evaluate`
  - `POST /v1/fields/{fieldUri}/nitrogen-application/evaluate`
  - `GET /v1/fields/{fieldUri}/irrigation-readiness`
- Remaining future work is narrower: any later jurisdiction-specific environmental regime packs, optional sensor-assisted refinement, and further stewardship/rulepack hardening without widening unsupported obligation coverage.
- The stewardship slice still must honor the March 20 overlay and environmental-scope guards. Broader environmental-regime questions remain `Unknown` unless a separate pack is admitted.

## Repo-grounded baseline

### Observed current state

- Markdown archetypes and templates are the human authoring layer; generated FADL/JSON artifacts are derived from them.
- The semantic backbone already includes `Field`, `CropInstance`, append-only semantics, `EvidenceRecord`, `EventRecord`, and `RuleExecutionTrace`.
- The repo already has a template projection layer for app-facing workflows.
- The repo now contains repo-native water-balance/stewardship archetypes plus authored phase-3 templates and projection contracts.
- The runtime now exposes water-stewardship, water-stewardship evaluation, nitrogen-application evaluation, and irrigation-readiness surfaces and covers them in field-passport route tests and OpenAPI route-alignment tests.
- Rulepacks live under `specs/v0.4/regulatory/rulepacks/`.
- Current extension work is concentrated under `specs/v0.8/`.
- Runtime contracts are strongest in FastAPI/Pydantic; static OpenAPI can lag.
- The runtime already loads spec assets from the repo and has SHACL, DB smoke, and FastAPI test entrypoints.

### Evidence-backed inference

Phase 3 did extend the field compliance passport rather than create a second parcel-state subsystem. The current lowest-risk interpretation is:

1. keep `Field` and `CropInstance` as anchors,
2. reuse phase-1 parcel/passport facts,
3. reuse phase-2 daily evaluation patterns where useful,
4. use the live water/stewardship source artifacts and runtime surfaces as the current baseline,
5. expose focused parcel workflows for water, nitrate, and flood risk while keeping broader unsupported regime questions explicit as `Unknown`,
6. express operational decisions through rule traces plus evidence.

### Recommended working assumption

Use:

- the live phase-3 archetypes, templates, projections, runtime routes, OpenAPI paths, and tests as the authority for the current surface
- `specs/v0.8/` for any later source-model or contract hardening only when current reuse proves insufficient
- `specs/v0.4/regulatory/rulepacks/` for any later stewardship rulepack hardening slice
- the existing FastAPI runtime/test seams for contracts and implementation

## Product goal

Phase 3 should answer five narrow parcel questions:

1. **Is this field suitable for nitrogen or manure application today?**
2. **Is irrigation urgent, justified, or likely to be wasteful today?**
3. **Is flood, ponding, runoff, or leaching risk high enough to warn or block?**
4. **Which facts explain the decision: recent rain, ET, slope, protection regime, flood class, or drought status?**
5. **What evidence is missing or stale?**

This is a narrow stewardship and parcel decision-support workflow, not a full irrigation controller, not a fertilizer optimiser, and not a hydrology simulation platform.

## Scope boundaries

### In scope

- Generic daily parcel stewardship evaluation for:
  - `spreadNitrogen`
  - `spreadManure`
  - `irrigate`
  - `delayForFloodRisk`
- Water-accounting summaries built from weather/agromet and optional regional EO/climate support
- Flood/runoff/leaching/ponding risk signals with explainability
- Overlay-aware stewardship outputs that use water-protection, flood, and related overlays as parcel-level context without implying that a separate environmental obligation pack is already admitted
- Evidence-first reasoning with explicit freshness and provenance
- Optional later sensor-assisted refinement when on-farm soil moisture or irrigation telemetry exists

### Explicitly out of scope

- Full nutrient recommendation or rate optimisation
- Replacement of farm-specific nutrient planning or laboratory soil tests
- Private irrigation hardware control/orchestration
- Parcel-external water-rights administration or permitting workflows
- A separate dashboard outside the parcel passport model
- Re-modeling existing v0.8 agronomy, irrigation, soil, or EO semantics if equivalent assets already exist in the repo

## Working source assumptions for phase 3

These are product assumptions to verify during technical implementation:

- **Primary operational weather/agromet source:** ARSO observations, forecasts, agrometeorology, rainfall and reference ET context
- **Primary parcel restrictions/context source:** phase-1 field passport facts for overlays and geometry; overlay presence remains descriptive or decision-support context unless a separate regime pack is admitted
- **Primary protection/flood context:** water-protection and flood overlays as parcel context together with terrain-derived slope/ponding signals
- **Primary regional water-stress context:** ET and drought-support datasets used as secondary, regional signals
- **Primary legal/jurisdiction context for nutrient timing:** only already admitted rulepack constraints; broader Slovenia-first nitrate or territorial stewardship obligations remain `Unknown` unless a separate pack is admitted
- **Optional sensor refinement:** soil-moisture or irrigation telemetry only as additive evidence, never as a prerequisite for day-one usefulness

Important: if a Slovenia-specific legal regime pack is later admitted for this decision family, its constraints must outrank generic agronomic heuristics. Until then, regional EO/climate products remain **supporting evidence**, and broader environmental-regime questions stay `Unknown`.

## Semantic design

### Reuse, do not replace

Keep these as canonical anchors:

- `Field`
- `CropInstance`
- `EvidenceRecord`
- `EventRecord`
- `RuleExecutionTrace`
- phase-1 field facts:
  - `field_authority_link`
  - `field_geometry_snapshot`
  - `field_declaration_snapshot`
  - `field_overlay_fact`
  - `field_condition_daily`
  - `field_action_evaluation`
- phase-2 assets if present:
  - plant-health advisory/signal facts stay separate and are not widened here

### Current repo-backed phase-3 artifact set

The repo now contains the core phase-3 stewardship artifact family:

- `FIELD.field_water_balance_fact.v1.md`
- `FIELD.field_stewardship_signal.v1.md`
- `template-field-water-stewardship-si-v0_8.md`
- `template-field-nitrogen-application-check-si-v0_8.md`
- `template-field-irrigation-readiness-si-v0_8.md`
- `template-field-water-stewardship-si-v0_8.json`
- `template-field-nitrogen-application-check-si-v0_8.json`
- `template-field-irrigation-readiness-si-v0_8.json`

Prefer **reusing** existing v0.8 agronomy semantics for weather observations, irrigation operations, soil observations, terrain context, remote sensing context, and scouting/operations where those concepts already exist.

### Current repo-backed package layout

```text
specs/v0.8/
  archetypes/
    FIELD.field_water_balance_fact.v1.md
    FIELD.field_stewardship_signal.v1.md
  templates/
    template-field-water-stewardship-si-v0_8.md
    template-field-nitrogen-application-check-si-v0_8.md
    template-field-irrigation-readiness-si-v0_8.md
  templates/projections/
    template-field-water-stewardship-si-v0_8.json
    template-field-nitrogen-application-check-si-v0_8.json
    template-field-irrigation-readiness-si-v0_8.json
  ontology/
    farm-rm-v1_7-field-water-stewardship.ttl
  constraints/
    farm-rm-v1_7-field-water-stewardship.shacl.ttl
  sql/migrations/
    <next>_v1_7_field_water_balance_fact.sql
    <next>_v1_7_field_stewardship_signal.sql
  reference-ingest/profiles/
    sl-water-stewardship-weather-2026.json
    sl-water-stewardship-overlays-2026.json
    regional-et-drought-support-2026.json

specs/v0.4/regulatory/rulepacks/
  si-field-ops-water-stewardship-2026-draft.json
```

### Why this split

- `field_water_balance_fact` holds time-bounded parcel water-accounting summaries with provenance.
- `field_stewardship_signal` holds parcel-specific stewardship risks and urgencies derived from overlays, recent weather, terrain, and optional support datasets.
- Final allow/warn/block outcomes for operations should still land in `field_action_evaluation` with trace/evidence refs.
- The projection layer should present parcel-facing decisions without introducing a mutable “current status” table.

## Contract boundaries

### `field_water_balance_fact`

Purpose: preserve the parcel’s daily water-accounting summary without pretending to be a crop model or a sensor truth source.

Required shape:

- `fieldUri`
- `cropInstanceUri`
- `asOf`
- `sourceWindow`
- `precipitationRecentMm`
- `referenceEtRecentMm`
- `referenceEtForecastMm`
- `soilWaterProxyStatus` (`drying|balanced|wet|saturated|unknown`)
- `waterDeficitProxyStatus` (`low|moderate|high|unknown`)
- `droughtContextStatus` (`none|regional-watch|regional-elevated|unknown`)
- `floodContextStatus` (`none|watch|elevated|unknown`)
- `supportDatasetStatus` (`none|regional-et|regional-drought|multi-source|unknown`)
- `reasonCodes`
- `evidenceRefs`

### `field_stewardship_signal`

Purpose: store parcel-specific, explainable stewardship signals derived from overlays, terrain, weather, and water-balance context.

Required shape:

- `fieldUri`
- `cropInstanceUri`
- `asOf`
- `signalType` (`runoffRisk|leachingRisk|pondingRisk|floodRisk|irrigationUrgency|nitrateTimingRisk|manureTimingRisk`)
- `signalLevel` (`low|watch|elevated|high|unknown`)
- `jurisdictionStatus` (`clear|restricted|blocked|unknown`)
- `overlayStatus` (`none|waterProtection|floodHazard|multi-regime|unknown`)
- `terrainStatus` (`flat|moderate|steep|depression|unknown`)
- `recentWeatherStatus` (`supporting|neutral|adverse|unknown`)
- `waterBalanceStatus` (`dry|balanced|wet|saturated|unknown`)
- `sensorSupportStatus` (`none|supporting|contradicting|unknown`)
- `recommendedNextStep` (`none|delay|inspect|irrigate|prepare-application|candidate-check`)
- `reasonCodes`
- `traceRefs`
- `evidenceRefs`

### Water stewardship current repo-backed surface

The live water-stewardship surface exposes:

- `fieldUri`
- `asOfDate`
- `activeCropInstanceUri`
- `dailyDecisions`
- `topSignals`
- `overlayContext`
- `recentWeatherSummary`
- `waterBalanceSummary`
- `recommendedActions`
- `requiredEvidence`
- `traceRefs`
- `evidenceRefs`

### Nitrogen/manure application current repo-backed surface

The live nitrogen/manure application check surface exposes:

- `fieldUri`
- `asOfDate`
- `actionType` (`spreadNitrogen|spreadManure`)
- `decision` (`allow|warn|block|unknown`)
- `blockingFindings`
- `warningFindings`
- `jurisdictionSummary`
- `runoffLeachingSummary`
- `weatherWindowSummary`
- `requiredEvidence`
- `traceRefs`
- `evidenceRefs`

### Irrigation readiness current repo-backed surface

The live irrigation-readiness surface exposes:

- `fieldUri`
- `asOfDate`
- `decision` (`allow|warn|block|unknown`)
- `urgencyStatus` (`none|monitor|recommended|urgent|unknown`)
- `waterBalanceSummary`
- `droughtContextSummary`
- `floodPondingSummary`
- `requiredEvidence`
- `traceRefs`
- `evidenceRefs`

## Authority model and conflict resolution

Keep these boundaries explicit:

| Concern | Authority holder | Phase-3 behavior |
| --- | --- | --- |
| Parcel identity and geometry | phase-1 field/passport facts | reused, not re-modeled |
| Spatial regulatory context | overlay facts from phase 1 | parcel overlay context and decision-support input; broader obligation status stays `Unknown` unless a separate pack is admitted |
| Recent parcel weather context | weather/agromet facts | operational signal |
| Regional ET / drought support | support datasets with provenance | supporting context only |
| Parcel water-accounting summary | `field_water_balance_fact` | derived, time-bound |
| Parcel stewardship risk | `field_stewardship_signal` + rule trace | derived, explainable |
| Final operation decision | `field_action_evaluation` | allow/warn/block/unknown with evidence |

Do not let regional EO or climate layers silently overrule admitted restrictions or parcel overlay facts. The field-specific step must remain explicit in `field_stewardship_signal` and in rule traces, and overlay presence alone must not be read as proof that a broader environmental regime pack is admitted.

## Rule categories for the phase-3 draft rulepack

Use a dedicated inherited draft rulepack:

`si-field-ops-water-stewardship-2026-draft.json`

It should inherit from the broader field-ops pack and add these categories:

1. `water_stewardship_authority_and_freshness`
2. `water_protection_and_flood_regimes`
3. `recent_rain_and_runoff_conditions`
4. `terrain_and_ponding_context`
5. `water_balance_and_irrigation_need`
6. `nitrate_and_manure_timing_risk`
7. `regional_drought_and_flood_support`
8. `evidence_sufficiency`

This draft stewardship rulepack is decision-support only unless and until a separately admitted environmental regime pack proves broader legal-obligation coverage.

Outcome policy:

- `block` for admitted hard constraints or stewardship failures inside this decision-support scope
- `warn` for elevated operational risk or incomplete but non-blocking conditions
- `unknown` when freshness or evidence sufficiency is inadequate, or when a broader environmental regime question lacks an admitted pack
- `allow` only when blockers are absent and evidence sufficiency is met

## Daily evaluation flows

### Flow A — daily water stewardship summary

1. Resolve field and active crop context from phase-1 passport facts.
2. Read latest `field_condition_daily`.
3. Pull current overlay intersections and terrain-derived context.
4. Build/update `field_water_balance_fact` from recent weather, ET context, and support datasets.
5. Evaluate top stewardship signals.
6. Compile the water stewardship projection.

### Flow B — nitrogen/manure application check

1. Start from the daily water stewardship summary.
2. Evaluate admitted constraints plus overlay-derived decision-support restrictions; unresolved broader regime questions remain `Unknown`.
3. Evaluate recent rainfall, runoff/leaching, and saturation risk.
4. Persist action evaluation with `actionType = spreadNitrogen` or `spreadManure`.
5. Compile the nitrogen/manure application check projection.

### Flow C — irrigation readiness

1. Start from the daily water stewardship summary.
2. Evaluate water deficit, drought context, and short-term rainfall context.
3. Evaluate flood/ponding or waste-risk contradictions.
4. Persist action evaluation with `actionType = irrigate`.
5. Compile the irrigation readiness projection.

### Flow D — sensor-assisted refinement (optional)

1. Read on-farm soil-moisture or irrigation telemetry if available.
2. Compare the sensor signal to water-balance and stewardship summaries.
3. Add sensor support or contradiction into `field_stewardship_signal`.
4. Re-evaluate only if the sensor materially changes confidence or urgency.

## API surface

Current live phase-3 endpoints:

- `POST /v1/fields/{fieldUri}/water-stewardship/evaluate`
- `GET /v1/fields/{fieldUri}/water-stewardship`
- `POST /v1/fields/{fieldUri}/nitrogen-application/evaluate`
- `GET /v1/fields/{fieldUri}/irrigation-readiness`

Capabilities:

- `fieldWaterStewardship`
- `fieldNitrogenApplicationCheck`
- `fieldIrrigationReadiness`

Versioning rule:

- keep `field_compliance_passport_v1` stable in phase 3
- do not widen the passport contract unless the change is strictly additive and low-risk
- prefer dedicated phase-3 projections for focused workflows

## Runtime behavior requirements

- Preserve append-only semantics.
- Keep provenance on all imported weather, overlay, and support facts.
- Return explicit degraded/incomplete payloads when a support source is unavailable.
- Never hide evidence gaps behind optimistic decisions.
- Keep reason codes short, deterministic, and stable for client display and later reporting reuse.
- Ensure regional support datasets can be disabled without breaking baseline parcel compliance behavior.

## Current repo proof

- phase-3 archetypes, templates, projections, runtime routes, OpenAPI paths, and field-passport tests exist in the live repo
- fixture coverage already exists for water stewardship, stewardship evaluation, nitrogen/manure application checks, and irrigation readiness
- review must still confirm that overlay restrictions remain visible and that broader unsupported environmental-regime questions remain `Unknown`

## Remaining future acceptance for later hardening

- any separately admitted environmental regime pack beyond the current scope guards
- optional sensor-assisted refinement or telemetry-backed stewardship support
- later stewardship/rulepack hardening that preserves the March 20 overlay and environmental-scope boundaries

## Codex instructions for any later phase-3 widening

### What Codex should do first

1. Start from the live phase-3 archetypes, templates, projections, routes, tests, and capability flags rather than recreating them.
2. Inspect the live repo for any existing irrigation, soil-water, weather, terrain, flood, nutrient, or stewardship overlaps before widening the slice.
3. Reuse existing v0.8 agronomy archetypes before creating any new semantic asset.
4. Confirm whether additional rulepack hardening is truly needed beyond the current surfaces.
5. Keep the March 20 overlay and environmental-scope guards authoritative.

### What Codex should implement next only if Phase 3 is widened again

1. Add new source-model or rulepack material only where a true gap remains beyond the live phase-3 slice.
2. Keep passport v1 stable unless a strictly additive field is unavoidable.
3. Add optional telemetry refinement or environmental-pack logic only when the authority boundary is explicit and admitted.

### What Codex should avoid

- Do not create a new top-level twin entity.
- Do not build a generic irrigation dashboard.
- Do not duplicate existing v0.8 semantics for irrigation, soil observations, EO, or nutrient operations if they already fit.
- Do not let generic drought/ET support layers outrank Slovenia-specific overlay or rulepack constraints.
- Do not present nitrogen/manure timing as a nutrient recommendation engine.
- Do not make private sensors mandatory for baseline usefulness.

### Expected deliverables from Codex

- repo-native semantic source files
- technical spec / ADR in the repo’s standard workitem location
- runtime endpoint implementation
- tests green on the phase-3 surface
- a short implementation note explaining any semantic compromises, reused overlaps, or source-governance decisions

## Repo evidence anchors for Codex

These are the repo documents that motivated this spec and should be re-checked against the live checkout:

- `AI_ONBOARDING.md`
- `20-semantic-core.md`
- `30-runtime-architecture.md`
- `40-api-and-data-contracts.md`
- `50-compliance-and-reporting.md`
- `60-build-run-test-generate.md`
- `70-implementation-status.md`
- `80-open-questions-and-risks.md`
- `docs/ai/workitems/field-compliance-passport-si/TECH_SPEC.md`
- `docs/implementation/field_passport_phase1_acceptance_checklist.md`
- `docs/implementation/field_passport_phase2_spray_window_plant_health_spec.md`

## Final implementation order

1. Treat the live phase-3 archetypes, templates, projections, runtime routes, OpenAPI paths, and tests as the current baseline.
2. Audit whether any separately admitted environmental regime pack is actually needed beyond the current scope guards.
3. Add optional telemetry or further rulepack hardening only when it stays parcel-centric, explainable, and within the admitted boundary.
4. Decide later whether any phase-3 summary should be folded into a future passport contract revision.
