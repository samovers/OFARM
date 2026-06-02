# OFARM agronomic observation and measurement context fixtures v0.1

Date: 2026-05-12  
Status: active supporting implementation/conformance artifact  
Scope: Phase 2 conformance fixtures for `AgronomicObservationContext` and `MeasurementEvidence` carrier closure  
Audience: implementers, conformance authors, reviewers, and AI agents

---

## 1. Purpose

These fixtures prove the Phase 2 carrier closure created by `OFARM_Agronomic_Observation_and_Measurement_Context_RFC_v0_1.md`.

They validate that OFARM can now carry structured agronomic observation and measurement context without changing baseline truth law.

The fixtures are intentionally narrow:

- scouting observation context
- sample collection with result pending
- qualified lab result below LOQ
- calibrated sensor evidence
- narrative-only degraded context
- evidence sufficiency cases that block or allow only the declared strength of evidence

---

## 2. Active contract families under test

- `03_machine_contracts/schemas/agronomic/OFARM_AgronomicObservationContext_schema_v0_1.json`
- `03_machine_contracts/schemas/evidence/OFARM_MeasurementEvidence_schema_v0_1.json`
- existing `03_machine_contracts/schemas/evidence/OFARM_EvidenceSufficiencyCase_schema_v0_2.json` examples that reference the new carriers

---

## 3. Required behavior

A conforming implementation must show that:

1. An observation context record does not become current state directly.
2. Narrative observations remain preservable and advisory-useful.
3. Missing measurement result or missing method context blocks high-consequence promotion.
4. A numeric result carries quantity-kind and unit semantics.
5. A censored result such as below LOQ is not coerced into zero.
6. Calibration, lab method, provenance, and chain-of-custody details can be retained when available.
7. Existing evidence sufficiency v0.2 can evaluate the new measurement records without a schema change.

---

## 4. Fixture families

| Fixture family | Positive artifact | Expected posture |
|---|---|---|
| scouting context | `OFARM_AgronomicObservationContext_example_field_17_weed_patch_scouting_v0_1.json` | advisory-supporting, review-required for high-consequence use |
| sample pending result | `OFARM_AgronomicObservationContext_example_field_17_soil_sample_pending_lab_v0_1.json`, `OFARM_MeasurementEvidence_example_soil_sample_collected_pending_lab_v0_1.json` | retained as evidence, blocked for nutrient-status truth |
| qualified lab result | `OFARM_MeasurementEvidence_example_soil_nitrate_below_loq_lab_result_v0_1.json` | accepted as qualified support, not exact zero |
| calibrated sensor | `OFARM_MeasurementEvidence_example_leaf_wetness_sensor_calibrated_v0_1.json`, `OFARM_AgronomicObservationContext_example_field_17_leaf_wetness_sensor_context_v0_1.json` | advisory support with calibration and spatial representativeness retained |
| narrative-only context | `OFARM_AgronomicObservationContext_example_field_17_narrative_only_low_consequence_v0_1.json` | useful local knowledge; high-consequence automatic promotion blocked |
| sufficiency bridge | `OFARM_EvidenceSufficiencyCase_example_measurement_context_missing_review_v0_2.json`, `OFARM_EvidenceSufficiencyCase_example_qualified_lab_result_support_v0_2.json` | existing evidence sufficiency v0.2 gates the new carriers |

---

## 5. Boundary

These fixtures do not close quantity-bearing interventions, as-applied records, partial extent, agronomic code-binding profile, or query/output reconstruction.
Those remain follow-on phases.
