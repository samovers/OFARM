# Authority Re-Research Report: Farm-RM v0.8 Agronomy Archetypes (58)

Date: 2026-02-27

## Executive Summary

We re-reviewed the 58 Farm-RM v0.8 agronomy archetypes one-at-a-time against:
1. Extension/university protocols (field/lab protocols and recordkeeping guidance)
2. Standards/method references (ISO/ASTM/AOAC/ASABE/EPPO/USDA/FAO/traceability as applicable)
3. Peer-reviewed literature (papers or review papers)

Output is a citation-backed review memo per archetype with a clear decision:
- `no_change`, or
- `change_spec_ready` (decision-complete change spec; not implemented).

## Repo Deliverables

1. Overview + rules:
   - `/Users/einstein/Documents/Codex/Semantic farming/docs/research/agronomy-archetype-authority-review/README.md`
2. Tracker (canonical status table):
   - `/Users/einstein/Documents/Codex/Semantic farming/docs/research/agronomy-archetype-authority-review/tracker.md`
3. Gap analysis roll-up + prioritized backlog:
   - `/Users/einstein/Documents/Codex/Semantic farming/docs/research/agronomy-archetype-authority-review/gap-analysis.md`
4. 58 per-archetype review memos:
   - `/Users/einstein/Documents/Codex/Semantic farming/docs/research/agronomy-archetype-authority-review/archetypes/*.review.md`

## Results (What Changed vs What Held Up)

Archetypes reviewed: 58

Decisions:
- `no_change`: 4
- `change_spec_ready`: 54

By kind:
- `ACTION`: 13 total (2 `no_change`, 11 `change_spec_ready`)
- `OBSERVATION`: 27 total (2 `no_change`, 25 `change_spec_ready`)
- `EVALUATION`: 11 total (0 `no_change`, 11 `change_spec_ready`)
- `INSTRUCTION`: 4 total (0 `no_change`, 4 `change_spec_ready`)
- `ADMIN`: 3 total (0 `no_change`, 3 `change_spec_ready`)

Archetypes judged sufficient as-is (`no_change`):
- `ACTION.planting_event.v1`
- `ACTION.tillage_event.v1`
- `OBSERVATION.pest_trap_count.v1`
- `OBSERVATION.remote_sensing_index_observation.v1`

## What "Change Needed" Mostly Means

The dominant change themes across archetypes were:
1. **Provenance**: records need a procedure/standard reference in addition to a method code (sampling protocols, sensor deployment/QC, decision thresholds, lab methods, grade systems).
2. **Evidence**: single `evidenceRef` patterns are often insufficient; many records need multiple attachments with roles (tickets, reports, invoices, calibration sheets, photos).
3. **Comparability semantics**: values need explicit basis/meaning (water accounting basis, sensor summary basis, storage loss basis, units normalization constraints).
4. **Stack alignment**: multiple places show spec/SHACL/API/SQL drift; bringing the whole stack into alignment is required to make archetypes enforceable end-to-end.
5. **Admin/case packaging**: compliance and incident workflows need first-class case/evidence-set identifiers and clean linkage into submission packages/rendered reports.

## Breaking-Change Recommendations (Proposed `.v2` Archetypes)

Across 29 review memos, 30 distinct `.v2` archetype IDs were recommended due to semantic restructuring (typically free-text to typed/structured records).

Proposed `.v2` IDs (see the corresponding review memo for details):
- `ACTION.disease_control_operation.v2`
- `ACTION.pesticide_application_event.v2`
- `ACTION.soil_amendment_application.v2`
- `ADMIN.phytosanitary_case_file.v2`
- `ADMIN.soil_compliance_evidence.v2`
- `ADMIN.variety_evidence_package.v2`
- `EVALUATION.disease_case_assessment.v2`
- `EVALUATION.disease_risk_forecast.v2`
- `EVALUATION.equipment_field_suitability.v2`
- `EVALUATION.seed_field_compatibility.v2`
- `EVALUATION.soil_constraint_risk.v2`
- `EVALUATION.soil_fertility_status.v2`
- `EVALUATION.suitability_assessment.v2`
- `EVALUATION.variety_field_suitability.v2`
- `EVALUATION.variety_risk_profile.v2`
- `INSTRUCTION.ipm_control_plan.v2`
- `INSTRUCTION.variety_selection_plan.v2`
- `OBSERVATION.agrometeorological_station_observation.v2`
- `OBSERVATION.climate_hazard_profile.v2`
- `OBSERVATION.crop_adaptation_profile.v2`
- `OBSERVATION.crop_scouting_signs.v2`
- `OBSERVATION.diagnostic_test_result.v2`
- `OBSERVATION.equipment_capability_profile.v2`
- `OBSERVATION.field_pedoclimatic_profile.v2`
- `OBSERVATION.forecast_scenario_bundle.v2`
- `OBSERVATION.seed_lot_quality_health.v2`
- `OBSERVATION.soil_sensor_series.v2`
- `OBSERVATION.storage_quality_conditions.v2`
- `OBSERVATION.variety_trial_result.v2`
- `OBSERVATION.water_allocation_and_use.v2`

## Prioritized Roadmap (From Gap Analysis)

Use `/Users/einstein/Documents/Codex/Semantic farming/docs/research/agronomy-archetype-authority-review/gap-analysis.md` as the master checklist.

Suggested first implementation slice (highest leverage):
1. Standardize a multi-evidence attachment pattern (with roles) across "evidence-bearing" records.
2. Add procedure/method provenance and measurement-basis semantics for the highest-risk observations (sampling, sensors, quality panels, water accounting).
3. Fix template references to missing primitives and close spec/impl drift for already-shipped endpoints.
4. Implement compliance evidence "sets" as first-class admin records linked to submissions/reports for organic/regulatory workflows.

