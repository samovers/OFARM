# Field Passport Later Planning Cards Gap Analysis

Status note, 2026-03-15:

- The placeholder-only production path is retired.
- The repo now treats these labels as outputs of a backend-backed climate plan-tab contract rather than acceptable `Later` UI behavior.
- Use the climate plan-tab template and runtime contract work as the current implementation path.
- Update, 2026-03-20: the original backend-gap framing is now mostly closed. This note remains useful as a screen-label-to-canonical-signal alignment memo, not as evidence that the card contract is still missing.

## Scope

This note analyzes the current repo status for the requested planning-card labels:

- `Frost trend`
- `Heat trend`
- `Dry-spell trend`
- `Irrigation value`
- `Variety fit`

It is intentionally narrow. It does not redefine field-passport semantics. It maps the requested labels to the current backend, projection, and documentation state.

## Authority map

1. Runtime implementation and tests
   - `specs/api/v1/server/fastapi/app/field_passport.py`
   - `specs/api/v1/server/fastapi/tests/test_field_passport.py`
   - `specs/api/v1/server/fastapi/app/dev_context.py`
   - `config/dev-context/packages.json`
2. Canonical field-passport implementation notes
   - `docs/implementation/phase-2-9-detailed-spec-climate-plan-card-signal-mapping.md`
   - `docs/implementation/field_passport_phase3_water_nitrate_flood_spec.md`
   - `docs/implementation/field_passport_phase6_climate_adaptation_spec.md`
   - `docs/implementation/field_passport_phase7_integration_rollout_plan.md`
3. Canonical templates and archetypes
   - `specs/v0.8/templates/template-field-climate-plan-tab-si-v0_8.md`
   - `specs/v0.8/templates/projections/template-field-climate-plan-tab-si-v0_8.json`
   - `specs/v0.8/templates/template-field-climate-suitability-outlook-si-v0_8.md`
   - `specs/v0.8/archetypes/FIELD.field_climate_adaptation_signal.v1.md`
4. Runtime and static API surfaces
   - `specs/api/v1/server/fastapi/examples/response-field-climate-plan-tab-v1.json`
   - `specs/api/v1/server/fastapi/README.md`
   - `specs/api/v1/openapi-farm-rm.yaml`

## Observed current state

### 1. Exact card labels are now documented as screen-level backend contract labels

- The runtime now exposes a dedicated plan-tab endpoint and template with exact screen-level `cardType` values:
  - `frostTrend`
  - `heatTrend`
  - `drySpellTrend`
  - `irrigationValue`
  - `varietyFit`
- Evidence:
  - `specs/v0.8/templates/template-field-climate-plan-tab-si-v0_8.md`
  - `specs/v0.8/templates/projections/template-field-climate-plan-tab-si-v0_8.json`
  - `specs/api/v1/server/fastapi/app/field_passport.py`
  - `specs/api/v1/server/fastapi/tests/test_field_passport.py`
  - `specs/api/v1/server/fastapi/examples/response-field-climate-plan-tab-v1.json`

### 2. The dedicated planning-card projection now exists

- Climate planning now has a first-class screen contract:
  - `GET /v1/fields/{fieldUri}/climate-plan-tab`
  - template id `farm.tpl.si.field_climate_plan_tab.v0_8`
- Capability flags are present for the screen and each card family:
  - `fieldClimatePlanning`
  - `fieldClimatePlanningFrostTrend`
  - `fieldClimatePlanningHeatTrend`
  - `fieldClimatePlanningDrySpellTrend`
  - `fieldClimatePlanningIrrigationValue`
  - `fieldClimatePlanningVarietyFit`
- Evidence:
  - `specs/api/v1/server/fastapi/app/main.py`
  - `specs/api/v1/server/fastapi/app/field_passport.py`
  - `specs/api/v1/server/fastapi/app/dev_context.py`
  - `config/dev-context/packages.json`
  - `specs/api/v1/server/fastapi/README.md`
  - `specs/api/v1/openapi-farm-rm.yaml`
  - `specs/api/v1/server/fastapi/tests/test_field_passport.py`

### 3. The cards are implemented as screen labels over canonical climate or irrigation semantics

- The runtime and mapping spec keep `cardType` presentation-level while preserving canonical backing concepts:
  - `frostTrend` -> `frostShiftRisk`
  - `heatTrend` -> `heatStressRisk` and `warmingTrend`
  - `drySpellTrend` -> `waterDemandIncrease`
  - `irrigationValue` -> irrigation-readiness and water-balance context
  - `varietyFit` -> `cropSuitabilityPressure`, `adaptationOpportunity`, and variety context
- Evidence:
  - `docs/implementation/phase-2-9-detailed-spec-climate-plan-card-signal-mapping.md`
  - `docs/implementation/field_passport_phase6_climate_adaptation_spec.md`
  - `specs/v0.8/archetypes/FIELD.field_climate_adaptation_signal.v1.md`
  - `specs/api/v1/server/fastapi/app/field_passport.py`

### 4. Irrigation still uses readiness semantics under the screen-level `irrigationValue` card

- Phase 3 still defines irrigation canonically as `irrigation readiness`
- The plan-tab card is a screen-level view over that readiness output, not a new economic or agronomic value score
- Evidence:
  - `docs/implementation/phase-2-9-detailed-spec-climate-plan-card-signal-mapping.md`
  - `docs/implementation/field_passport_phase3_water_nitrate_flood_spec.md`
  - `specs/api/v1/server/fastapi/app/field_passport.py`
  - `specs/api/v1/server/fastapi/tests/test_field_passport.py`

### 5. Variety context now has an explicit `varietyFit` card

- Climate suitability outlook still carries crop or variety context
- The plan-tab runtime now emits a dedicated `varietyFit` card when capability and evidence permit
- Evidence:
  - `specs/v0.8/templates/template-field-climate-plan-tab-si-v0_8.md`
  - `specs/api/v1/server/fastapi/examples/response-field-climate-plan-tab-v1.json`
  - `specs/v0.8/templates/template-field-climate-suitability-outlook-si-v0_8.md`
  - `specs/api/v1/server/fastapi/app/field_passport.py`
  - `specs/api/v1/server/fastapi/tests/test_field_passport.py`

### 6. The remaining gap is documentation drift risk, not backend absence

- The backend phase docs, template, projection, example payload, runtime route, capabilities, and tests now exist in this repo
- What remains important is keeping screen-level labels from being mistaken for canonical domain symbols
- The primary repo-owned mapping authority is now the climate plan-tab template plus the card-to-signal mapping note

## Evidence-backed inference

1. The original planning-card backend gap is materially closed.
2. The requested labels now exist as first-class screen-level contract values, not just as hypothetical UI copy.
3. The remaining risk is semantic confusion: `cardType` labels are presentation-level and must not replace canonical climate, irrigation, or suitability concepts.
4. The right authority chain is now:
   - climate plan-tab template and projection for the screen contract,
   - runtime route and tests for behavior,
   - phase-2-9 mapping note for card-to-canonical-signal meaning.

## Recommended working assumption

Treat these five labels as implemented screen-level contract names on top of canonical field-passport backend surfaces.

Under that assumption:

- `frostTrend`, `heatTrend`, and `drySpellTrend` are live climate plan-tab cards backed by canonical climate signals and indicator support
- `irrigationValue` is a live screen card backed by Phase 3 irrigation readiness
- `varietyFit` is a live screen card backed by climate suitability and variety context
- phase-2-9 remains the authority for explaining how card labels map to canonical meanings

## Findings table

| issue_id | category | severity | canonical_source | conflicting_sources | evidence | impact | recommended action | validation classes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LPC-001 | resolved contract gap | low | `specs/v0.8/templates/template-field-climate-plan-tab-si-v0_8.md` | older gap note wording | The dedicated climate plan-tab template and projection now exist | The original “no contract” claim is stale | Refresh this note to treat the screen contract as implemented | none for doc-only analysis |
| LPC-002 | resolved runtime gap | low | `specs/api/v1/server/fastapi/app/field_passport.py` | older gap note wording | The runtime now exposes `/v1/fields/{fieldUri}/climate-plan-tab` with card ordering, capability gating, and detail endpoints | The original “generic projections only” claim is stale | Reference the live route, example payload, and tests directly | none for doc-only analysis |
| LPC-003 | residual mapping discipline | medium | `docs/implementation/phase-2-9-detailed-spec-climate-plan-card-signal-mapping.md` | screen-level labels if treated as canonical domain symbols | Card labels now exist, but they still summarize canonical signals or irrigation context rather than replacing them | Future docs or clients could silently redefine backend meaning | Keep phase-2-9 as the mapping authority and cite it wherever the cards are described | none for doc-only analysis |
| LPC-004 | residual wording risk | low | `docs/implementation/phase-2-9-detailed-spec-climate-plan-card-signal-mapping.md` | `irrigationValue` screen label | The card remains backed by readiness/urgency, not a generic “value” score | UI or docs may overread the card as a broader agronomic or financial score | Keep the screen-level label but describe its backing semantics explicitly | none for doc-only analysis |
| LPC-005 | residual documentation sync risk | medium | `specs/api/v1/server/fastapi/tests/test_field_passport.py` | stale narrative notes | Runtime, example payload, and capabilities are now ahead of this note | Old planning memos can mislead implementers if not refreshed | Treat this memo as an alignment note and keep it synchronized with the template, runtime, and tests | none for doc-only analysis |

## Card-by-card assessment

### Frost trend

- Current backend source:
  - `climate-plan-tab` card `frostTrend`
  - canonical backing via `frostShiftRisk` and frost-oriented indicator trends
- Status:
  - implemented
- Gap:
  - keep the screen label mapped to canonical signals rather than treating it as a new domain symbol

### Heat trend

- Current backend source:
  - `climate-plan-tab` card `heatTrend`
  - canonical backing via `heatStressRisk`, `warmingTrend`, and temperature-oriented indicator trends
- Status:
  - implemented
- Gap:
  - keep the screen label mapped to canonical signals rather than treating it as a new domain symbol

### Dry-spell trend

- Current backend source:
  - `climate-plan-tab` card `drySpellTrend`
  - canonical backing via `waterDemandIncrease` and drought/precipitation-oriented indicator trends
- Status:
  - implemented
- Gap:
  - this is still the least stable semantic label, so phase-2-9 should remain the explicit mapping anchor

### Irrigation value

- Current backend source:
  - `climate-plan-tab` card `irrigationValue`
  - backing detail endpoint `irrigation-readiness`
- Status:
  - implemented
- Gap:
  - the label is still screen-level shorthand over readiness and urgency semantics

### Variety fit

- Current backend source:
  - `climate-plan-tab` card `varietyFit`
  - backing detail endpoint `climate-suitability-outlook`
  - dominant permanent-crop variety fallback in planning context where needed
- Status:
  - implemented
- Gap:
  - keep the card tied to suitability and variety context rather than overreading it as a standalone optimization family

## Proposed change

Shortest safe path:

1. Keep the current climate plan-tab backend contract as the authority for these five cards.
2. Keep phase-2-9 as the explicit mapping note from screen labels to canonical climate or irrigation meaning.
3. Treat this file as a refreshed alignment memo, not as proof that the planning-card contract is still missing.

## Cross-layer impact

- Backend:
  - no backend rename or new endpoint is justified by current evidence
- Contracts:
  - the climate plan-tab transport already exists and is tested
- Documentation:
  - this note was the stale layer; the canonical template, mapping note, and runtime already exist
- Frontend:
  - the frontend can now rely on the dedicated screen contract rather than stitching the cards ad hoc

## Risks and uncertainties

1. `drySpellTrend` remains the least stable card semantically, because it still summarizes more than one lower-level climate source family.
2. `irrigationValue` may still over-promise if read as a generic score instead of a readiness-oriented screen card.
3. `varietyFit` remains only as strong as the available crop or variety context and may still fall back to broader suitability context.
4. This note is now repo-current, but any future runtime or template changes should refresh it again so the memo does not become stale a second time.

## Best next move

Keep the new climate plan-tab projection authoritative for the screen-level contract, and continue to reuse the existing lower-level field-passport climate endpoints as drill-down surfaces:

- `Frost trend` -> `climate-adaptation-summary` plus `climate-indicator-trends`
- `Heat trend` -> `climate-adaptation-summary` plus `climate-indicator-trends`
- `Dry-spell trend` -> `climate-adaptation-summary` plus selected indicator trends
- `Irrigation value` -> `irrigation-readiness`
- `Variety fit` -> `climate-suitability-outlook`
