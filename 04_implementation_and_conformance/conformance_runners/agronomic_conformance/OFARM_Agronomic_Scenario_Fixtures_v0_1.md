# OFARM agronomic scenario fixtures v0.1

Date: 2026-05-12  
Status: active supporting implementation artifact  
Scope: Phase 1 agronomic fixture expectations for scenario-driven amendment work  
Audience: conformance authors, implementers, reviewers, and AI agents

---

## 1. Purpose

This file describes the first agronomic fixture set in implementation terms.

It is deliberately scenario-first. The goal is to prevent premature schema design by proving exactly where existing active contracts are strong and where they are thin.

Machine-readable records are in:

- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_agronomic_scenario_records_v0_1.json`

Runner and results:

- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/ofarm_agronomic_scenario_fixture_runner_v0_1.py`
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_agronomic_scenario_fixture_results_v0_1.json`

---

## 2. Shared expected behavior

Every agronomic scenario must preserve these OFARM behaviors:

1. Advisory output does not become Compliance truth directly.
2. A plan does not become execution truth.
3. An operation claim does not become an accepted consequence without review and evidence gates.
4. Late evidence is retained without rewriting original capture.
5. Current-state materialization is derivative and must be fresh or refused/reviewed for high-consequence use.
6. PassportView remains live/recomputable and must not be treated as a frozen DocumentAssembly.
7. Corrections supersede or contest prior records; they do not erase them.
8. Partial spatial reality must not silently overwrite whole-field truth.

---

## 3. Fixture set

### AGR-SCEN-001 — Observation to decision

Stress case:
A scouting observation reports disease pressure on a field edge. An advisor recommends treatment.

Expected OFARM behavior:
- `ObservationEvent` / observation assertion is distinct from advisory recommendation.
- narrative scouting is retained.
- high-consequence treatment acceptance is blocked or requires review if crop stage, sampling method, threshold, or uncertainty context is missing.
- future `AgronomicObservationContext` should be the smallest carrier to close this gap.

Negative test:
The package must reject any path where a narrative-only observation becomes an accepted treatment consequence.

### AGR-SCEN-002 — Recommendation to prescription to execution

Stress case:
A recommendation becomes a prescription, a planned intervention, an operation claim, and then an accepted execution record.

Expected OFARM behavior:
- recommendation, prescription, plan, claim, accepted consequence, correction, and outcome remain distinct.
- product/input identity and rate/dose are required before a high-consequence as-applied acceptance can be trusted.
- future `InterventionDetail` should be the smallest carrier to close this gap.

Negative test:
The package must reject any path where `PlannedIntervention` alone is treated as as-applied truth.

### AGR-SCEN-003 — Offline contractor late sync

Stress case:
A contractor performs work offline and syncs after a delegation or context change.

Expected OFARM behavior:
- original record time and later arrival are preserved.
- promotion-time authority is rechecked.
- late machine data may support review but does not auto-promote.
- missing rate or incomplete machine log blocks automatic acceptance.

Negative test:
The package must reject any path where delayed sync bypasses revocation or evidence sufficiency.

### AGR-SCEN-004 — Partial failed application and correction

Stress case:
A sprayer treats only part of a field. One pass fails. A manual correction is added later.

Expected OFARM behavior:
- the operation claim is preserved.
- actual extent remains partial.
- manual correction supersedes or contests without erasing the original claim.
- whole-field current state must not be overwritten.

Negative test:
The package must reject any path where partial treatment is materialized as whole-field accepted treatment without explicit extent basis.

### AGR-SCEN-005 — Partial replant with different variety

Stress case:
Poor emergence on one zone causes partial replant with a different seed lot and variety.

Expected OFARM behavior:
- parent/child crop-cycle lineage is explicit.
- mixed variety and mixed crop-cycle state is preserved.
- stale current-state materializations are invalidated or marked stale where appropriate.
- PassportView and any DocumentAssembly disclose mixed state when relevant.

Negative test:
The package must reject any path where a partial replant overwrites the whole field crop-cycle identity.

### AGR-SCEN-006 — Measurement-context dispute

Stress case:
A soil, pest, disease, or moisture measurement is later challenged because method, sampling, calibration, or uncertainty is missing.

Expected OFARM behavior:
- weak measurement evidence may be retained.
- high-consequence promotion is blocked, downgraded, or requires review when measurement context is insufficient.
- output must not imply false precision.

Negative test:
The package must reject any path where a context-free numeric measurement drives accepted high-consequence output.

### AGR-SCEN-007 — Ambiguous product or input identity

Stress case:
A product is recorded under a local name, invoice name, label name, or machine-log identifier that cannot be deterministically resolved.

Expected OFARM behavior:
- ambiguity is preserved as an evidence sufficiency issue.
- reference snapshot and code-binding version are explicit.
- high-consequence promotion is blocked or review-required until product identity is resolved.

Negative test:
The package must reject any path where local-name-only input identity becomes accepted compliance truth.

### AGR-SCEN-008 — Wet grain held before drying

Stress case:
Wet grain is harvested, held temporarily, measured, dried, and later attached to a lot or buyer-facing output.

Expected OFARM behavior:
- material state changes are event/consequence driven.
- moisture and temperature measurement context is preserved.
- stale or missing material-state evidence blocks high-consequence output.

Negative test:
The package must reject any path where dry, safe, or buyer-ready state is inferred from harvest alone.

### AGR-SCEN-009 — Field geometry revision after operations

Stress case:
A field boundary is corrected after operations were recorded and after a filing or output used the old geometry.

Expected OFARM behavior:
- identity revision and materialization invalidation are explicit.
- old frozen output remains traceable to old basis.
- successor output or correction path is used when needed.

Negative test:
The package must reject any path where corrected geometry silently mutates the basis of an already frozen filing.

### AGR-SCEN-010 — Schema, example, glossary, and query drift

Stress case:
The same agronomic concept is named or resolved differently in schema, examples, alias catalog, packs, and output fixtures.

Expected OFARM behavior:
- alias paths resolve to governed semantic paths.
- code bindings are versioned and profile-scoped.
- projection-only semantics are refused.

Negative test:
The package must reject any path where an alias or projection creates hidden agronomic truth not backed by the semantic substrate.

---

## 4. Follow-on carrier implications

The fixture set justifies later work on:
- `AgronomicObservationContext`
- `InterventionDetail`
- `ScopeExtentBasis`
- `AgronomicCodeBindingProfile`
- agronomic query/output reconstruction fixtures

Those follow-on carriers are not created by this file.


## Phase AGR-P8 runtime-chain fixture closure — 2026-05-13

AGR-P8 closes the earlier AGR-P1 expectation-only limitation at package-local conformance level.

Added/recognized fixture artifacts:

- `OFARM_Agronomic_Runtime_Chain_Closure_Fixtures_v0_1.md`
- `OFARM_agronomic_runtime_chain_records_v0_1.json`
- `ofarm_agronomic_runtime_chain_runner_v0_1.py`
- `OFARM_agronomic_runtime_chain_results_v0_1.json`

The scenario fixture runner now reports `PASS` when the AGR-P8 runtime-chain results pass. This means every `AGR-SCEN-*` scenario is tied to package-local source records, carrier usage, promotion/materialization/output expectations, and negative shortcut checks.

Boundary: AGR-P8 is still conformance fixture evidence. It does not claim production runtime telemetry, live pilot performance, live external registry lookup, or wire-level ISOXML/EFDI/ADAPT conformance.
