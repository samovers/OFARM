# Phase 2 Spec — Spray-Window & Plant-Health Relevance

Parcel-centric compliance twin, Slovenia-first, built on the Phase 1 field compliance passport

Date: 2026-03-07

## Executive decision

- The original phase-2 planning slice is now materially implemented as repo-native read models.
- Live repo evidence now includes:
  - `GET /v1/fields/{fieldUri}/spray-window`
  - `GET /v1/fields/{fieldUri}/plant-health/relevance`
  - `template-field-spray-window-si-v0_8.md`
  - `template-field-plant-health-relevance-si-v0_8.md`
  - `template-field-spray-window-si-v0_8.json`
  - `template-field-plant-health-relevance-si-v0_8.json`
  - OpenAPI paths and field-passport route tests for both endpoints
- The remaining gap is narrower than the original plan: official advisory ingest as a first-class source seam, broader rulepack hardening, and optional candidate-specific spray checks.
- Phase 2 still depends on the phase-1 passport as its semantic anchor, but it no longer belongs in the repo as a “missing backend” note.

## Repo-grounded baseline

### Observed current state

- Markdown archetypes and templates are the authoring layer; generated artifacts are derived from them.
- The semantic backbone already includes `Field`, `CropInstance`, append-only semantics, evidence linkage, and rule execution traces.
- The repo already has a template projection layer for app-facing workflows.
- The repo now contains authored phase-2 workflow templates and projection contracts for spray-window and plant-health relevance.
- The runtime now exposes both phase-2 read models and covers them in field-passport route tests and OpenAPI route-alignment tests.
- Rulepacks live under `specs/v0.4/regulatory/rulepacks/`.
- Runtime contracts are strongest in FastAPI/Pydantic; static OpenAPI can lag.
- The runtime already loads spec assets from the repo and has SHACL, DB smoke, and FastAPI test entrypoints.

### Evidence-backed inference

Phase 2 did extend the parcel passport rather than replacing it. The current lowest-risk interpretation is:
1. keep `Field` and `CropInstance` as anchors,
2. reuse the phase-1 passport facts plus existing agronomy and disease-assessment seams,
3. keep spray-window and plant-health relevance as focused read models,
4. leave official advisory ingest explicit as a missing-evidence seam until a first-class source adapter is admitted,
5. treat broader rulepack/source-model promotion and candidate-specific checks as later, optional hardening work.

### Recommended working assumption

Use:
- the live phase-2 templates, projections, runtime routes, OpenAPI paths, and tests as the authority for the current surface
- `specs/v0.8/` for any later source-model promotion only when current reuse proves insufficient
- `specs/v0.4/regulatory/rulepacks/` for any later phase-2 rulepack hardening slice
- the existing FastAPI runtime/test seams for contracts and implementation

## Product goal

Phase 2 should answer four narrow parcel questions:

1. **Is this field operationally suitable for spraying now?**
2. **Is it likely to remain suitable in the next 6–24 hours?**
3. **Which disease or plant-health risks are relevant enough to surface for this parcel today?**
4. **What evidence supports the answer, and what is missing or stale?**

This is a narrow decision-support workflow, not a generic crop-protection suite and not a black-box diagnosis engine.

## Scope boundaries

### In scope

- Generic spray-window readiness for a parcel and active crop context
- Plant-health relevance scoring based on official advisories plus weather/stage/signal context
- Advisory-first explainability with evidence refs and trace refs
- Summary outputs for:
  - `spray now`
  - `spray later today`
  - `watch / scout`
  - `not decision-ready`
- Optional candidate-specific spray check if a product/material is supplied and the Slovenia authorization source is integrated

### Explicitly out of scope

- Automated disease diagnosis from imagery
- Full PPP legality for all products before the Slovenia authorization source is integrated
- Prescription-rate optimisation
- Autonomous operation planning
- A second dashboard layer separate from the passport
- Re-modeling existing crop-stage, scouting, remote-sensing, leaf-wetness, irrigation, or phytosanitary semantics if equivalent v0.8 archetypes already exist

## Working source assumptions for phase 2

These are product assumptions to verify during technical implementation:

- **Primary operational weather/agromet source:** ARSO observations, forecasts, agrometeorology
- **Primary official plant-health advisory source:** Slovenian public plant-health forecasting / warning content
- **Primary parcel context source:** phase-1 field compliance passport facts
- **Primary crop context:** `CropInstance`, declaration snapshot, and available crop-stage semantics
- **Advisory remote sensing / phenology context:** existing EO and agronomy archetypes where already present
- **Product authorization source for candidate-specific checks:** Slovenia-first PPP authorization source when integrated; EU pesticide data stays supplementary

Important: until a confirmed machine interface exists for official plant-health warnings, the implementation should model advisory ingest as a **pluggable adapter** that can preserve provenance for HTML/feed/manual-extract sources.

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

### Current repo-backed phase-2 artifact set

The repo now contains the core phase-2 read-model artifact family:

- `template-field-spray-window-si-v0_8.md`
- `template-field-plant-health-relevance-si-v0_8.md`
- `template-field-spray-window-si-v0_8.json`
- `template-field-plant-health-relevance-si-v0_8.json`

The current implementation reuses existing v0.8/runtime seams instead of first promoting separate `FIELD.field_plant_health_advisory_fact.v1` or `FIELD.field_plant_health_signal.v1` archetypes. Official advisory ingest therefore remains an explicit missing-evidence seam rather than a proven current source family.

Prefer **reusing** existing v0.8 agronomy semantics for crop stage, scouting, remote sensing, agrometeorology, leaf wetness, phytosanitary case files, irrigation, and diagnostics wherever those concepts already exist.

### Fallback additions only if a later authority review proves current reuse insufficient

```text
specs/v0.8/
  archetypes/
    FIELD.field_plant_health_advisory_fact.v1.md
    FIELD.field_plant_health_signal.v1.md
  templates/
    template-field-spray-window-si-v0_8.md
    template-field-plant-health-relevance-si-v0_8.md
  templates/projections/
    template-field-spray-window-si-v0_8.json
    template-field-plant-health-relevance-si-v0_8.json
  ontology/
    farm-rm-v1_7-field-spray-health.ttl
  constraints/
    farm-rm-v1_7-field-spray-health.shacl.ttl
  sql/migrations/
    <next>_v1_7_field_plant_health_advisory_fact.sql
    <next>_v1_7_field_plant_health_signal.sql
  reference-ingest/profiles/
    sl-plant-health-advisories-2026.json
    sl-weather-window-metrics-2026.json

specs/v0.4/regulatory/rulepacks/
  si-field-ops-spray-health-2026-draft.json
```

### Why this split

- `field_plant_health_advisory_fact` holds imported official advisory content with provenance.
- `field_plant_health_signal` holds parcel-specific, evidence-backed risk relevance signals.
- Spray-window outputs should usually be a **projection + rule evaluation** built from existing condition facts, not a new mutable state table.
- The final allow/warn/block result should continue to land in `field_action_evaluation` with trace/evidence refs.

## Contract boundaries

### `field_plant_health_advisory_fact`

Purpose: preserve official advisory content and metadata without pretending it is already field-specific.

Required shape:
- `fieldUri` or region binding strategy
- `jurisdiction`
- `sourceSystem`
- `sourceId`
- `sourceVersion`
- `issuedAt`
- `validFrom`
- `validTo`
- `cropScope`
- `hazardCode`
- `hazardLabel`
- `regionScope`
- `advisorySeverity`
- `advisoryText`
- `recommendedActionSummary`
- `ingestMethod` (`api|feed|html|manual_extract`)
- `evidenceRefs`

### `field_plant_health_signal`

Purpose: store parcel-specific relevance signals derived from advisory overlap plus field conditions.

Required shape:
- `fieldUri`
- `cropInstanceUri`
- `asOf`
- `hazardCode`
- `hazardLabel`
- `relevanceStatus` (`low|watch|elevated|high|unknown`)
- `phenologyStatus` (`match|partial|mismatch|unknown`)
- `officialAdvisoryStatus` (`none|regional|field-relevant|unknown`)
- `weatherSignalStatus` (`supporting|neutral|contradicting|unknown`)
- `scoutingEvidenceStatus` (`present|missing|stale|unknown`)
- `eoContextStatus` (`supporting|neutral|unknown`)
- `recommendedNextStep` (`none|monitor|scout|prepare-treatment|candidate-check`)
- `reasonCodes`
- `traceRefs`
- `evidenceRefs`

### Spray-window current repo-backed surface

The live spray-window read model exposes:

- `fieldUri`
- `asOfDate`
- `activeCropInstanceUri`
- `decision` (`allow|warn|block|unknown`)
- `blockingFindings`
- `warningFindings`
- `weatherMetrics`
- `surfaceConditionSummary`
- `driftRiskSummary`
- `advisoryContextSummary`
- `requiredEvidence`
- `traceRefs`
- `evidenceRefs`

Important: the current repo-backed read model is one selected-date answer. The older `now|next_6h|next_24h` horizon split remains a possible later widening, not the current runtime contract.

### Plant-health relevance current repo-backed surface

The live plant-health relevance read model exposes:

- `fieldUri`
- `asOfDate`
- `activeCropInstanceUri`
- `summaryStatus`
- `signals`
- `requiredEvidence`
- `traceRefs`
- `evidenceRefs`

Important: the current runtime reuses disease assessments, leaf-wetness context, and daily-state signals. Official advisories are still represented as required missing evidence rather than a current repo-backed source table.

## Authority model and conflict resolution

Keep these boundaries explicit:

| Concern | Authority holder | Phase-2 behavior |
| --- | --- | --- |
| Parcel identity and geometry | phase-1 field/passport facts | reused, not re-modeled |
| Weather/agromet conditions | weather/agromet ingest facts | operational signal |
| Official plant-health guidance | advisory fact with provenance | advisory source of truth |
| Parcel-specific risk relevance | plant-health signal + rule trace | derived, explainable |
| Generic spray suitability | spray-window projection + action evaluation | derived, time-bound |
| Candidate product legality | separate candidate-specific evaluation | optional until Slovenia source is integrated |

Do not let advisory content silently become field-specific truth. The field-specific step must remain explicit in `field_plant_health_signal` and in rule traces.

## Rule categories for the phase-2 draft rulepack

Use a dedicated inherited draft rulepack:

`si-field-ops-spray-health-2026-draft.json`

It should inherit from the broader field-ops pack and add these categories:

1. `spray_weather_window`
2. `spray_surface_and_access`
3. `spray_evidence_freshness`
4. `plant_health_official_advisory_alignment`
5. `plant_health_phenology_alignment`
6. `plant_health_weather_signal`
7. `plant_health_scouting_support`
8. `candidate_product_constraints` (optional, only when candidate check is active)

Outcome policy:
- `block` for hard spray-window failures
- `warn` for elevated risk or incomplete but non-blocking conditions
- `unknown` when evidence freshness is insufficient
- `allow` only when blockers are absent and evidence sufficiency is met

## Daily evaluation flows

### Flow A — generic spray window

1. Resolve field and active crop context from phase-1 passport facts.
2. Read latest `field_condition_daily`, overlays, and leaf-wetness/agrometeorological support observations.
3. Derive one selected-date spray-window answer.
4. Keep advisory context explicit in `requiredEvidence` and `advisoryContextSummary`.
5. Compile the spray-window projection.

### Flow B — plant-health relevance

1. Resolve field and active crop context.
2. Read disease assessments plus stage/agromet/leaf-wetness/remote-sensing/scouting facts where available.
3. Evaluate parcel-level relevance per hazard.
4. Keep official advisory ingest explicit as missing required evidence until the source adapter exists.
5. Compile the plant-health relevance projection.

### Flow C — candidate-specific spray check (optional)

1. Start from the generic spray-window result.
2. Load candidate product/material metadata.
3. Run candidate-specific authorization/label/profile rules.
4. Persist a second action evaluation with explicit candidate context.
5. Return a candidate check result that never overwrites the generic spray-window result.

## API surface

Current live phase-2 endpoints:

- `GET /v1/fields/{fieldUri}/spray-window`
- `GET /v1/fields/{fieldUri}/plant-health/relevance`

Still optional later:
- `POST /v1/fields/{fieldUri}/spray-window/evaluate`
- `POST /v1/fields/{fieldUri}/spray-window/evaluate-candidate`

Capabilities:
- `fieldSprayWindow`
- `fieldPlantHealthRelevance`
- optional later: `fieldSprayCandidateCheck`

Versioning rule:
- keep `field_compliance_passport_v1` stable in phase 2
- do not widen the passport contract unless the change is strictly additive and low-risk
- prefer dedicated phase-2 projections for focused workflows

## Runtime behavior requirements

- Preserve append-only semantics.
- Keep provenance on all ingested advisory/weather facts.
- Return explicit degraded/incomplete payloads when persistence or ingest dependencies are unavailable.
- Never hide evidence gaps behind optimistic decisions.
- Keep reason codes short, deterministic, and stable for client display and reporting reuse.

## Tests and acceptance gate

### Current repo proof

- repo-native markdown template sources for spray-window and plant-health relevance
- projection contracts for both read models
- Pydantic request/response models
- endpoint handlers
- OpenAPI paths
- field-passport route tests and route-alignment coverage

### Remaining future acceptance for a later hardening slice

- official advisory ingest/source-model promotion
- broader phase-2 draft rulepack
- candidate-specific spray-check runtime surface
- any ontology / SHACL / SQL support required by newly promoted phase-2 source facts

### Phase-2 acceptance checklist

All of the following must pass before phase-2 is considered implementation-ready:

```bash
make fadl-generate
make fadl-check
make shacl-test
make db-smoke-v0_8
specs/api/v1/server/fastapi/run-tests.sh
```

The current product-level proof already holds for the implemented read-model slice:

- A parcel can produce one selected-date spray-window result with clear blocking and warning findings.
- A parcel can produce at least one plant-health relevance result with clear reason codes.
- Missing advisory evidence is explicit in `requiredEvidence`.
- Missing/stale evidence can force `unknown`.
- Candidate-specific checks, if later implemented, must never overrule generic spray-window state silently.

## Codex instructions

### What Codex should do first

1. Inspect the live repo for any existing spray-window, plant-health, phytosanitary, agromet, crop-stage, or advisory overlaps.
2. Reuse existing v0.8 agronomy archetypes before creating any new semantic asset.
3. Confirm exact markdown grammar and naming patterns from neighboring `v0.8` source files.
4. Confirm whether the existing field-ops rulepack from phase 1 already exists in-repo and choose inheritance accordingly.

### What Codex should implement next only if Phase 2 is widened again

1. Audit whether dedicated advisory/source-model promotion is still necessary before adding new archetypes such as:
   - `FIELD.field_plant_health_advisory_fact.v1.md`
   - `FIELD.field_plant_health_signal.v1.md`
2. Keep using the live template/projection/route/test set as the starting point rather than recreating it.
3. Add ontology / SHACL / SQL support only if new source facts are actually promoted.
4. Add the inherited draft rulepack only when rule execution is widened beyond the current read-model slice.
5. Add candidate-specific spray checks only when the Slovenia authorization source path is ready.
6. Keep passport v1 stable unless a strictly additive field is unavoidable.

### What Codex should avoid

- Do not create a new top-level twin entity.
- Do not build a generic crop-protection dashboard.
- Do not duplicate existing v0.8 semantics for crop stage, scouting, leaf wetness, remote sensing, or phytosanitary cases if they already fit.
- Do not let EU-level pesticide metadata outrank Slovenia-specific authorization when a candidate-specific check is added.
- Do not rely on undocumented external APIs without a pluggable ingest adapter and explicit provenance.

### Expected deliverables from Codex

- repo-native semantic source files
- technical spec / ADR in the repo’s standard workitem location
- runtime endpoint implementation
- tests green on the phase-2 surface
- a short implementation note explaining any semantic compromises or discovered overlap

## Repo evidence anchors for Codex

These are the repo documents that motivated this spec and should be re-checked against the live checkout:

- `20-semantic-core.md`
- `30-runtime-architecture.md`
- `40-api-and-data-contracts.md`
- `50-compliance-and-reporting.md`
- `60-build-run-test-generate.md`
- `70-implementation-status.md`
- `80-open-questions-and-risks.md`
- `docs/ai/workitems/field-compliance-passport-si/TECH_SPEC.md`
- `docs/implementation/field_passport_phase1_acceptance_checklist.md`

## Current next-step order

1. Treat the live phase-2 templates, projections, endpoints, OpenAPI paths, and tests as the current baseline.
2. Audit whether a first-class official advisory source adapter and source-model promotion are actually needed beyond the current missing-evidence seam.
3. Add broader rulepack hardening only if it can stay explainable and parcel-centric.
4. Add candidate-specific spray checks only when the Slovenia authorization source path is ready.
5. Decide later whether any phase-2 summary should be folded back into a future passport contract revision.
