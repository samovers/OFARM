# Phase 7 Spec — Cross-Phase Integration & Rollout Plan

Parcel-centric compliance twin, Slovenia-first, integrating phases 1 through 6

Date: 2026-03-09

## Executive decision

- The original phase-7 integration and rollout slice is now materially implemented as a parcel-centric field-passport read-model family with live runtime routes, capability flags, OpenAPI paths, and field-passport tests spanning phases 1 through 6.
- Live repo evidence now includes:
  - `GET /v1/fields/{fieldUri}/passport`
  - `POST /v1/fields/{fieldUri}/passport/evaluate-daily`
  - `POST /v1/fields/{fieldUri}/passport/evaluate-action`
  - `GET /v1/fields/{fieldUri}/spray-window`
  - `GET /v1/fields/{fieldUri}/plant-health/relevance`
  - `GET /v1/fields/{fieldUri}/water-stewardship`
  - `POST /v1/fields/{fieldUri}/water-stewardship/evaluate`
  - `GET /v1/fields/{fieldUri}/irrigation-readiness`
  - `GET /v1/fields/{fieldUri}/eo-anomaly`
  - `GET /v1/fields/{fieldUri}/phenology-status`
  - `GET /v1/farms/{farmUri}/scout-priority-queue`
  - `GET /v1/fields/{fieldUri}/benchmark-context`
  - `GET /v1/fields/{fieldUri}/explainability-summary`
  - `GET /v1/fields/{fieldUri}/regional-comparison`
  - `GET /v1/fields/{fieldUri}/climate-adaptation-summary`
  - `GET /v1/fields/{fieldUri}/climate-suitability-outlook`
  - `GET /v1/fields/{fieldUri}/climate-indicator-trends`
  - `GET /v1/fields/{fieldUri}/climate-plan-tab`
- Remaining future work is narrower: source-adapter hardening, optional recompute or evaluation helpers, telemetry or explainability refinement, later rulepack tightening, and any separately admitted environmental regime packs.
- Implementation order still matters historically, but the core rollout surfaces below are no longer hypothetical planning names.
- Do **not** create a second parcel-state subsystem, a generic dashboard, or a new top-level twin entity.

## Repo-grounded baseline

### Observed current state

- Markdown archetypes and templates are the human authoring layer; generated FADL/JSON artifacts are derived outputs.
- The stable semantic backbone already includes `Field`, `CropInstance`, append-only evidence/event discipline, and `RuleExecutionTrace`.
- Template projections already exist as the app-facing pattern over archetype content.
- Rulepacks live under `specs/v0.4/regulatory/rulepacks/`, while active extension work is concentrated under `specs/v0.8/`.
- Runtime contracts are strongest in FastAPI/Pydantic, and static OpenAPI can lag the running app.
- Existing build and QA seams already cover generation, SHACL checks, DB smoke, and backend tests.
- The runtime now exposes phase-1 through phase-6 field-passport read models plus matching capability flags and route-alignment tests, so the rollout contract is already materially present in repo truth.

Repo evidence referenced in this planning artifact: `00-index.md`; `10-repo-map.md`; `20-semantic-core.md`; `30-runtime-architecture.md`; `40-api-and-data-contracts.md`; `50-compliance-and-reporting.md`; `60-build-run-test-generate.md`; `70-implementation-status.md`.

### Evidence-backed inference

- All later phases should extend the phase-1 field compliance passport rather than building parallel field-state or dashboard subsystems.
- The right integration seam is: source adapters -> append-only facts -> rule evaluations and traces -> parcel-facing projections -> typed runtime endpoints.
- Most later work can still be released as additive projections and rulepacks, provided shared contracts stay stable and provenance remains explicit.
- The remaining rollout task is primarily hardening and extension of live surfaces, not proof that phases 2 through 6 still lack parcel-facing runtime contracts.

### Recommended working assumption

- Treat phase 1 as the non-negotiable integration foundation and the current live route family as the authority for parcel-centric rollout naming.
- Treat phases 2 and 3 as the first operational decisioning wave, phases 4 and 5 as advisory triage and explanation layers, and phase 6 as a planning layer with explicit uncertainty and no authority over same-day compliance outcomes.
- Use runtime Pydantic models, route tests, and current OpenAPI paths as the contract anchor whenever older planning notes drift.

## Cross-phase architecture

The integration model is intentionally narrow: one field-anchored passport, additive facts, additive projections, and explicit authority boundaries. Each phase contributes field context, not a new product surface.

| Phase | Primary outcome | Depends on | Authority class | Integration note |
| --- | --- | --- | --- | --- |
| 1 | Field compliance passport | None | Foundation / mixed | Creates the parcel identity, geometry, overlay, daily-state, and evidence spine. |
| 2 | Spray-window and plant-health relevance | 1 | Operational advisory + later candidate-specific legality | Consumes passport facts and adds plant-health advisory signals. |
| 3 | Water, nitrate and flood stewardship | 1 | Operational stewardship | Reuses passport overlays, daily state, and action evaluation patterns. |
| 4 | EO anomaly and scout-first engine | 1 (+2/3 optional) | Advisory | Adds anomaly triage, field prioritisation, and explainable EO context. |
| 5 | Regional benchmark and explainability | 1 (+2–4 optional) | Advisory / contextual | Adds local-versus-regional framing without leaving the parcel model. |
| 6 | Climate adaptation layer | 1 (+3–5 beneficial) | Planning advisory | Adds horizon-specific climate context and adaptation themes with uncertainty. |

## Shared semantic and integration invariants

1. Do not introduce a new top-level twin entity; keep `Field` as the semantic anchor and `CropInstance` as the seasonal crop context anchor.
2. Do not collapse GERK, cadastre, farm-operational, and derived geometries into one silently mutable parcel polygon.
3. Do not treat advisory sources or overlay presence as legal authority. If a Slovenia-specific legal pack is later admitted for a decision family, it must outrank EU-level or heuristic support layers; otherwise broader environmental-regime questions remain `Unknown`.
4. Keep every imported or derived fact provenance-rich: `sourceSystem`, `sourceId`, `sourceVersion`, evidence refs, trace refs, and freshness status.
5. Keep source facts append-only; projections are compiled read models, not mutable status tables.
6. Keep action outcomes explicit and narrow: `allow`, `warn`, `block`, or `unknown`.
7. Separate generic readiness from candidate-specific legality whenever a product, material, or plan choice changes the answer.
8. Prefer reusing existing `v0.8` agronomy semantics before adding new archetypes.
9. Do not hand-edit generated artifacts. Markdown sources remain the authoring layer.
10. When data are stale or missing, degrade honestly instead of fabricating complete readiness.

## Integration flow across phases

| Layer | What enters | What persists | What leaves |
| --- | --- | --- | --- |
| Source adapters | Official parcel, overlay, weather, advisory, EO, benchmark, climate feeds | Raw ingest snapshots, source metadata, evidence refs | Normalized field facts |
| Semantic facts | Normalized phase facts by field and date/horizon | Append-only `field_*` records and linked evidence | Stable inputs to rules and projections |
| Rule evaluation | Daily generic checks and candidate-specific checks | `RuleExecutionTrace` and `field_action_evaluation`-like outputs | Explainable `allow/warn/block/unknown` outcomes |
| Projection assembly | Facts, traces, events, evidence, freshness | Projection caches if the repo uses them | Field passport and phase-specific parcel views |
| Runtime contracts | Pydantic request/response models | API examples and contract tests | Field-facing endpoints and client capabilities |
| Release operations | Feature flags, backfill jobs, monitoring, pilot feedback | Rollout logs and enablement notes | Controlled release to pilot and wider cohorts |

## Rollout waves

| Wave | Includes | Purpose | Release gate | Pilot posture |
| --- | --- | --- | --- | --- |
| A | Phase 1 | Foundation: parcel identity, geometry, overlays, daily state, evidence spine | All phase-1 acceptance checks green | Internal and selected pilot farms only |
| B | Phases 2–3 | Operational decisioning: spray-window, plant-health relevance, stewardship | Wave A green + focused rulepack and runtime tests | Controlled field pilot with decision review |
| C | Phases 4–5 | Advisory triage and contextual explanation | Wave B green + anomaly/benchmark explainability tests | Broader advisory beta |
| D | Phase 6 | Planning layer: climate trends and adaptation themes | Wave C green + uncertainty/horizon contract checks | Opt-in planning beta |

Specification work for later phases can continue in parallel, but implementation order should still follow Waves A → B → C → D.

## Phase dependency and readiness matrix

| Phase | Minimum upstream | Can spec in parallel? | Can implement in parallel? | Notes |
| --- | --- | --- | --- | --- |
| 1 | None | N/A | Yes | Foundation phase. |
| 2 | 1 accepted | Yes | Only after 1 | Needs the passport and shared daily-state contracts. |
| 3 | 1 accepted | Yes | Yes with 2 if isolated | Operationally adjacent to phase 2, but not blocked by every plant-health detail. |
| 4 | 1 accepted | Yes | After 1; best after 2/3 semantics are visible | Should remain advisory and scout-first. |
| 5 | 1 accepted | Yes | After 1; benefits from 2–4 context | Contextual layer; do not let it drive legality. |
| 6 | 1 accepted | Yes | After 1; best after 3 and 5 | Planning layer with uncertainty and horizon semantics. |

## API and capability rollout plan

### Live endpoints

- `GET /v1/fields/{fieldUri}/passport`
- `POST /v1/fields/{fieldUri}/passport/evaluate-daily`
- `POST /v1/fields/{fieldUri}/passport/evaluate-action`
- `GET /v1/fields/{fieldUri}/spray-window`
- `GET /v1/fields/{fieldUri}/plant-health/relevance`
- `GET /v1/fields/{fieldUri}/water-stewardship`
- `POST /v1/fields/{fieldUri}/water-stewardship/evaluate`
- `GET /v1/fields/{fieldUri}/irrigation-readiness`
- `GET /v1/fields/{fieldUri}/eo-anomaly`
- `GET /v1/fields/{fieldUri}/phenology-status`
- `GET /v1/farms/{farmUri}/scout-priority-queue`
- `GET /v1/fields/{fieldUri}/benchmark-context`
- `GET /v1/fields/{fieldUri}/explainability-summary`
- `GET /v1/fields/{fieldUri}/regional-comparison`
- `GET /v1/fields/{fieldUri}/climate-adaptation-summary`
- `GET /v1/fields/{fieldUri}/climate-suitability-outlook`
- `GET /v1/fields/{fieldUri}/climate-indicator-trends`
- `GET /v1/fields/{fieldUri}/climate-plan-tab`

These are now live repo-native contracts. Later rollout or hardening work should reuse these exact path names, examples, and response models unless runtime code and tests change.

### Capability flags

| Capability flag | Enables |
| --- | --- |
| `fieldPassport` | Base parcel passport projection |
| `fieldPassportDailyEvaluation` | Daily generic evaluation flow |
| `fieldPassportActionEvaluation` | Candidate-specific action check |
| `fieldSprayWindow` | Phase-2 spray-window projection |
| `fieldPlantHealthRelevance` | Phase-2 plant-health relevance projection |
| `fieldWaterStewardship` | Phase-3 stewardship projection |
| `fieldNitrogenApplicationCheck` | Phase-3 nitrogen application review helper |
| `fieldIrrigationReadiness` | Phase-3 irrigation readiness projection |
| `fieldEoAnomaly` | Phase-4 EO anomaly projection |
| `fieldPhenologyStatus` | Phase-4 phenology-status projection |
| `fieldScoutPriorityQueue` | Phase-4 farm-scoped scout-priority queue |
| `fieldBenchmarkContext` | Phase-5 benchmark-context projection |
| `fieldExplainabilitySummary` | Phase-5 explainability-summary projection |
| `fieldRegionalComparison` | Phase-5 regional-comparison projection |
| `fieldClimatePlanning` | Phase-6 climate plan-tab screen family |
| `fieldClimatePlanningFrostTrend` | Climate plan frost-trend card |
| `fieldClimatePlanningHeatTrend` | Climate plan heat-trend card |
| `fieldClimatePlanningDrySpellTrend` | Climate plan dry-spell card |
| `fieldClimatePlanningIrrigationValue` | Climate plan irrigation-value card |
| `fieldClimatePlanningVarietyFit` | Climate plan variety-fit card |
| `fieldClimateAdaptationSummary` | Climate adaptation summary projection |
| `fieldClimateIndicatorTrends` | Climate indicator trends projection |
| `fieldClimateSuitabilityOutlook` | Climate suitability outlook projection |

## Test and acceptance gates

Use the same repo-native acceptance seams throughout the rollout:

- `make fadl-generate`
- `make fadl-check`
- `make shacl-test`
- `make db-smoke-v0_8`
- `specs/api/v1/server/fastapi/run-tests.sh`

| Wave | Must be true | Additional checks | Do not proceed if |
| --- | --- | --- | --- |
| A | Phase-1 source artifacts are repo-native and contracts resolve cleanly | Projection contract tests; minimal GET passport endpoint; evidence and freshness semantics | The passport still exists only as informal draft files |
| B | Spray/stewardship outputs explain `allow/warn/block/unknown` with traces and evidence | Rulepack tests; daily evaluation tests; honest missing-data degradation | Product/advisory logic silently overrules legal authority |
| C | EO and benchmark outputs stay advisory and parcel-centric | Explainability tests; context-only assertions; no generic dashboard regression | Anomaly or benchmark context is treated as legal truth |
| D | Climate outputs stay horizon-specific and uncertainty-aware | Scenario/horizon contract tests; advisory wording review | Climate context becomes a hard compliance blocker or same-day authority |

## Data onboarding and rollout operations

- Onboard data adapters in authority order: parcel identity and geometry first, overlays second, daily weather/agromet third, then later advisory, EO, benchmark, and climate layers.
- Keep freshness explicit by source family. A field can be decision-ready for one question and stale for another.
- Backfill historical context only after the forward path works; do not block pilot usefulness on perfect historical completeness.
- Release later phases behind capability flags so pilot farms can validate decision usefulness without exposing unfinished layers broadly.
- Capture pilot disagreements as evidence-linked events rather than patching outputs ad hoc.

## Cross-phase risk register

| Risk | Impact | Mitigation | Owner focus |
| --- | --- | --- | --- |
| Duplicate modeling of existing `v0.8` semantics | High | Codex audits live repo assets before adding new archetypes; reuse first, extend only when necessary. | Semantic modeling |
| Geometry authority collapse | High | Keep multiple geometry roles and explicit `complianceGeometryRef` selection. | Field model / spatial |
| Advisory versus legal confusion | High | Separate authority classes in rule outputs and never let advisory sources silently overrule jurisdictional legality. | Compliance / product |
| Runtime versus static contract drift | Medium | Review Pydantic models and tests as primary acceptance anchors; update static OpenAPI later if needed. | API / QA |
| Source adapter brittleness or missing machine interfaces | Medium | Use pluggable adapters, preserve provenance, and degrade honestly when ingest is partial. | Integrations |
| License or reuse ambiguity for some public layers | Medium | Verify ambiguous terms before broad commercial rollout; keep authority-link metadata explicit. | Data governance |
| Projection sprawl | Medium | Favor additive parcel projections over new standalone app surfaces. | Product / runtime |
| Over-coupled PRs across phases | Medium | Ship wave-sized slices with touched-file inventories and explicit dependency notes. | Delivery |

## Codex execution brief

1. Start with a live repo audit. Confirm the nearest real `v0.8` archetype/template grammar, runtime entrypoints, projection tests, and any already-existing semantics that cover parts of phases 2–6.
2. Produce a short technical delta memo before editing files. Separate: reused semantics, new semantics, runtime/API deltas, test deltas, and unresolved assumptions.
3. Implement Wave A first and stop at a green acceptance gate before starting Wave B.
4. Treat Waves B, C, and D as additive. Do not open a new parcel service, a second rule engine, or a generic dashboard surface.
5. For every new source artifact, maintain the chain: markdown source → generated artifacts → ontology/SHACL/SQL alignment → runtime contract → tests.
6. Where a live repo audit shows an existing semantic asset is adequate, reuse it and document the decision instead of creating a near-duplicate fact type.
7. Keep PRs wave-sized. Each PR should include a touched-file map by layer, generated artifact notes, executed test commands, and honest caveats.
8. If a public source is only partially machine-readable, preserve provenance and expose degraded readiness rather than fabricating a confident answer.

## Done definition for the overall rollout

- A reviewer can trace any parcel answer back through field facts, evidence records, rule traces, and source versions.
- Operational questions remain narrow and reliable: what am I allowed to do here, what is risky today, and which field needs attention first.
- Advisory layers remain advisory, planning layers remain planning, and legal authority remains explicit.
- Each wave has passing repo-native tests and an honest rollout note describing what is enabled and what still degrades.
- The client surface remains parcel-centric rather than expanding into a generic farm dashboard.

Primary next action: hand this rollout plan plus the phase-specific specs to Codex against the live repo checkout, and require a phase-0 technical delta memo before implementation starts.
