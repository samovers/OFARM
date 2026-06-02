# OFARM AGR-P7 agronomic baseline harmonisation summary v0.1

Date: 2026-05-13  
Status: active supporting implementation/conformance artifact  
Scope: record the Phase AGR-P7 baseline harmonisation that reflects accepted agronomic RFC and machine-contract closures from AGR-P2 through AGR-P6

---

## 1. Purpose

AGR-P7 is a baseline harmonisation pass, not a new design phase.

It reflects already-accepted agronomic carrier-shell work into the active baseline:
- observation and measurement context
- quantity-bearing intervention intent and execution/as-applied payloads
- partial extent and geometry-basis governance
- agronomic identity/code-binding profile law
- agronomic query/output reconstruction policy and trace controls

## 2. Baseline files amended

- `00_active_baseline/OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md`
- `00_active_baseline/OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md`
- `00_active_baseline/OFARM_Alignment_Register_v0_13.md`
- `00_active_baseline/OFARM_post_gap_closure_readiness_gate_memo_v0_1.md`
- `00_active_baseline/OFARM_final_hostile_review_after_gap_closure_v0_1.md`

## 3. Active accepted RFCs reflected

- `02_accepted_rfcs/OFARM_Agronomic_Observation_and_Measurement_Context_RFC_v0_1.md`
- `02_accepted_rfcs/OFARM_Quantity_Bearing_Intervention_and_As_Applied_RFC_v0_1.md`
- `02_accepted_rfcs/OFARM_Partial_Extent_and_Geometry_Basis_RFC_v0_1.md`
- `02_accepted_rfcs/OFARM_Agronomic_Code_Binding_and_Standards_Profile_RFC_v0_1.md`
- `02_accepted_rfcs/OFARM_Agronomic_Query_and_Output_Reconstruction_RFC_v0_1.md`

## 4. Active machine-contract concepts reflected

- `AgronomicObservationContext`
- `MeasurementEvidence`
- `InterventionIntentPayload`
- `ExecutionRecordPayload`
- `PartialExtent`
- `AgronomicIdentityBinding`
- `AgronomicCodeBindingProfile`
- `AgronomicReconstructionPolicy`
- `AgronomicReconstructionTrace`

## 5. Preservation checks

AGR-P7 preserves:
- assertion/history-first canonical truth
- governed current-state materialization
- Advisory Twin versus Compliance Twin separation
- explicit event grammar and commit classes
- explicit authority, evidence, review, and promotion gates
- external standards as anchors/bindings/exchange surfaces, not hidden law
- pack non-mutation of core meaning
- PassportView versus DocumentAssembly separation

## 6. Scope boundary

The current active baseline remains crop-farming operational law.
Livestock-specific semantics are out of scope for this release and require a future explicit profile or sister model.

## 7. Remaining bounded debt

AGR-P7 does not claim external standard readiness or production runtime completion.
Remaining debt is now concentrated in:
- pilot-depth event/assertion/evidence chains
- crop-specific and jurisdiction-specific packs
- live registry verification
- wire-level ADAPT/ISOXML/EFDI/ISOBUS mapping work
- broader certification/buyer/regulatory profile examples
- real implementation telemetry and runtime conformance evidence


## 8. Fixture evidence

AGR-P7 support evidence includes:

- `OFARM_Agronomic_Baseline_Harmonisation_Fixtures_v0_1.md`
- `OFARM_agronomic_baseline_harmonisation_records_v0_1.json`
- `ofarm_agronomic_baseline_harmonisation_runner_v0_1.py`
- `OFARM_agronomic_baseline_harmonisation_results_v0_1.json`

The fixture family validates baseline reflection and preservation boundaries only. It does not claim production runtime execution, live registry verification, or external-standard readiness.
