# OFARM agronomic amendment control plan v0.1

Date: 2026-05-12  
Status: active supporting implementation artifact  
Scope: control plan for the agronomist-review amendment lane through Phase AGR-P7 baseline harmonisation  
Audience: repository stewards, implementers, reviewers, and AI agents

---

## 1. Purpose

This file creates a controlled amendment lane for the Senior Agronomist Reviewer findings.

The lane was intentionally support-layer first. The plan itself does **not** create law; accepted RFCs, machine contracts, and AGR-P7 baseline edits carry the authoritative amendments.

The purpose is to keep the agronomic findings visible while preventing premature architecture drift.

---

## 2. Authority boundary

This plan sits in `04_implementation_and_conformance/` and therefore follows the normal authority order:

1. `00_active_baseline/`
2. `02_accepted_rfcs/`
3. `01_companion_artifacts/`
4. `03_machine_contracts/`
5. `04_implementation_and_conformance/`
6. `06_active_supporting_research/`

This plan may:
- organize implementation tasks
- define conformance-prep scenarios
- identify smallest controlled patches
- recommend later RFC or contract work

This plan may not:
- silently add baseline law
- promote supporting research into active law
- relax assertion/history-first truth
- turn Advisory Twin outputs into Compliance Twin truth
- use packs to mutate core meaning
- allow stale materializations to drive high-consequence output

---

## 3. Reviewer verdict absorbed by this lane

The agronomist review classified the package as:

**directionally right but premature**

Interpretation for OFARM work:
- the baseline architecture remains valid
- the main risk is insufficient agronomic payload and scenario realism
- the next work should be scenario and conformance expansion first
- RFC and machine-contract patches should follow only where scenarios prove the gap

---

## 4. Amendment phases

| Phase | Name | Change class | Status in this package | Output |
|---|---|---|---|---|
| AGR-P0 | Amendment control and task intake | IMPLEMENTATION_PLANNING | CLOSED / SUPPORT RETAINED | this plan plus task-register updates |
| AGR-P1 | Agronomic scenario coverage | IMPLEMENTATION_CONFORMANCE | ACTIVE SUPPORT | scenario matrix, fixture notes, machine-readable records, runner, results; remains expectation-level |
| AGR-P2 | Observation and measurement context | RFC_EXTENSION / MACHINE_CONTRACT_PATCH | CLOSED IN THIS PACKAGE | accepted RFC, `AgronomicObservationContext`, `MeasurementEvidence`, examples, runner, results |
| AGR-P3 | Quantity-bearing intervention and as-applied closure | RFC_EXTENSION / MACHINE_CONTRACT_PATCH | CLOSED IN THIS PACKAGE | accepted RFC, `InterventionIntentPayload`, `ExecutionRecordPayload`, bridge examples, runner, results |
| AGR-P4 | Partial extent and geometry basis | RFC_EXTENSION / MACHINE_CONTRACT_PATCH | CLOSED IN THIS PACKAGE | accepted RFC, `PartialExtent`, bridge examples, runner, results |
| AGR-P5 | Agronomic code-binding profile | RFC_EXTENSION / MACHINE_CONTRACT_PATCH | CLOSED IN THIS PACKAGE | accepted RFC, `AgronomicIdentityBinding`, `AgronomicCodeBindingProfile`, examples, runner, results |
| AGR-P6 | Query/output reconstruction | RFC_EXTENSION / MACHINE_CONTRACT_PATCH / CONFORMANCE | CLOSED IN THIS PACKAGE | accepted RFC, reconstruction policy/trace schemas, query/output examples, runner, results |
| AGR-P7 | Baseline harmonisation | BASELINE_HARMONISATION | CLOSED IN THIS PACKAGE | active baseline edits reflecting accepted AGR-P2 through AGR-P6 closures |
| AGR-P8 | Runtime-chain fixture closure | IMPLEMENTATION_CONFORMANCE | CLOSED IN THIS PACKAGE | package-local runtime chains covering AGR-P1 scenarios |
| AGR-P9 | Local-knowledge rationale lineage | IMPLEMENTATION_CONFORMANCE | CLOSED IN THIS PACKAGE | local observation/rule/recommendation/plan/claim/accepted-outcome lineage fixtures |

---

## 5. Finding-to-task map

| Reviewer finding | Problem | Current treatment | Task |
|---|---|---|---|
| AGR-001 | Observation context is too thin | closed at carrier-shell level by Phase AGR-P2; deeper scenario execution remains Phase AGR-P6+ | IMP-303, IMP-304, IMP-309 |
| AGR-002 | Recommendation/prescription/execution chain lacks as-applied payload | closed at carrier-shell level by Phase AGR-P3; extent/code-binding/query depth remains future | IMP-305, IMP-304 |
| AGR-003 | Partial and mixed-condition spatial reality is under-executable | closed at PartialExtent carrier-shell level by Phase AGR-P4; scenario coverage remains active | IMP-306, IMP-304 |
| AGR-004 | Evidence sufficiency does not yet cover measurement quality | closed at measurement-evidence carrier level by Phase AGR-P2; evidence-policy specialization remains future if pilots need it | IMP-303, IMP-304 |
| AGR-005 | Agronomic code-list/input identity governance is under-executable | closed at code-binding/profile carrier-shell level by Phase AGR-P5 | IMP-307 |
| AGR-006 | Scenario inventory should become conformance fixtures | active now | IMP-304, IMP-308 |
| AGR-007 | Agronomic queries should be testable | closed at reconstruction policy/trace and query/output fixture level by Phase AGR-P6 | IMP-309 |
| AGR-008 | Local knowledge can become explainable rationale trail | closed by AGR-P9 local-knowledge rationale lineage fixtures | IMP-310 |
| AGR-009 | Livestock appears out of scope | closed by AGR-P7 crop-only baseline harmonisation | IMP-311 |
| AGR-010 | Pack/profile detail needs shared minimum carriers | `AgronomicObservationContext`, `MeasurementEvidence`, `InterventionIntentPayload`, `ExecutionRecordPayload`, `PartialExtent`, `AgronomicIdentityBinding`, `AgronomicCodeBindingProfile`, `AgronomicReconstructionPolicy`, and `AgronomicReconstructionTrace` now provide shared carrier shells | IMP-303, IMP-305, IMP-306, IMP-307 |
| AGR-011 | External standards must be version-profiled | closed by AGR-P5 code-binding profile | IMP-307 |
| AGR-012 | Add AgronomicObservationContext | closed by `OFARM_Agronomic_Observation_and_Measurement_Context_RFC_v0_1.md` and active schema/examples | IMP-303 |
| AGR-013 | Activate quantity-bearing intervention carrier | closed at carrier-shell level by Phase AGR-P3 | IMP-305 |
| AGR-014 | Add farm scenario coverage matrix | active now | IMP-308 |
| AGR-015 | Offline contractor spray dispute break test | Phase AGR-P3 and AGR-P6 cover claim/as-applied/review/correction/dispute payloads and reconstruction fixtures; production pilot-depth chain execution remains future | IMP-304, IMP-305, IMP-309 |
| AGR-016 | Partial replant break test | PartialExtent, crop-cycle lineage, stale-materialization, and reconstruction fixtures are now represented; production pilot-depth chain execution remains future | IMP-304, IMP-306 |
| AGR-017 | Preserve assertion/history-first and twin boundary | explicit constraint across all amendment phases | all agronomic tasks |

---

## 6. Active work started by this amendment

This package now carries the AGR-P0 through AGR-P9 amendment lane. AGR-P1 through AGR-P9 are closed at scenario, carrier, reconstruction, baseline-harmonisation, runtime-chain, or local-rationale conformance level as applicable. `IMP-308` remains active only as maintenance for future pilot, crop-profile, live-registry, and wire-level exchange additions.

Phase AGR-P0/AGR-P1 support artifacts:
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_Agronomic_Amendment_Control_Plan_v0_1.md`
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_Agronomic_Scenario_Coverage_Matrix_v0_1.md`
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_Agronomic_Scenario_Fixtures_v0_1.md`
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_agronomic_scenario_records_v0_1.json`
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/ofarm_agronomic_scenario_fixture_runner_v0_1.py`
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_agronomic_scenario_fixture_results_v0_1.json`

Phase AGR-P2 active-law and contract artifacts:
- `02_accepted_rfcs/OFARM_Agronomic_Observation_and_Measurement_Context_RFC_v0_1.md`
- `03_machine_contracts/schemas/agronomic/OFARM_AgronomicObservationContext_schema_v0_1.json`
- `03_machine_contracts/schemas/evidence/OFARM_MeasurementEvidence_schema_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agronomic/OFARM_AgronomicObservationContext_example_field_17_weed_patch_scouting_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agronomic/OFARM_AgronomicObservationContext_example_field_17_soil_sample_pending_lab_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agronomic/OFARM_AgronomicObservationContext_example_field_17_leaf_wetness_sensor_context_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agronomic/OFARM_AgronomicObservationContext_example_field_17_narrative_only_low_consequence_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agronomic/OFARM_MeasurementEvidence_example_soil_sample_collected_pending_lab_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agronomic/OFARM_MeasurementEvidence_example_soil_nitrate_below_loq_lab_result_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/evidence/OFARM_MeasurementEvidence_example_leaf_wetness_sensor_calibrated_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/evidence/OFARM_EvidenceSufficiencyCase_example_measurement_context_missing_review_v0_2.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/evidence/OFARM_EvidenceSufficiencyCase_example_qualified_lab_result_support_v0_2.json`

Phase AGR-P2 support artifacts:
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_Agronomic_Observation_Measurement_Context_Fixtures_v0_1.md`
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_agronomic_observation_measurement_context_records_v0_1.json`
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/ofarm_agronomic_observation_measurement_context_runner_v0_1.py`
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_agronomic_observation_measurement_context_results_v0_1.json`
- `06_active_supporting_research/syntheses/OFARM_agronomic_observation_measurement_context_research_intake_v0_1.md`


Phase AGR-P3 active-law and contract artifacts:
- `02_accepted_rfcs/OFARM_Quantity_Bearing_Intervention_and_As_Applied_RFC_v0_1.md`
- `03_machine_contracts/schemas/agronomic/OFARM_InterventionIntentPayload_schema_v0_1.json`
- `03_machine_contracts/schemas/agronomic/OFARM_ExecutionRecordPayload_schema_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agronomic/OFARM_InterventionIntentPayload_example_field_17_spot_spray_advisory_recommendation_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agronomic/OFARM_InterventionIntentPayload_example_field_17_spot_spray_authorized_prescription_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agronomic/OFARM_InterventionIntentPayload_example_field_17_spot_spray_planned_operation_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agronomic/OFARM_ExecutionRecordPayload_example_field_17_contractor_spot_spray_claim_late_sync_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agronomic/OFARM_ExecutionRecordPayload_example_field_17_machine_log_partial_application_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agronomic/OFARM_ExecutionRecordPayload_example_field_17_partial_accepted_execution_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agronomic/OFARM_ExecutionRecordPayload_example_field_17_manual_correction_supersedes_claim_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agronomic/OFARM_ExecutionRecordPayload_example_field_17_extent_dispute_v0_1.json`
- bridge examples for `PlannedIntervention`, `AssertionRecord`, `SemanticEventEnvelope`, `AcceptedEventConsequence`, and `EvidenceSufficiencyCase v0.2`

Phase AGR-P3 support artifacts:
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_Agronomic_Intervention_As_Applied_Fixtures_v0_1.md`
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_agronomic_intervention_as_applied_records_v0_1.json`
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/ofarm_agronomic_intervention_as_applied_runner_v0_1.py`
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_agronomic_intervention_as_applied_results_v0_1.json`
- `06_active_supporting_research/syntheses/OFARM_agronomic_intervention_as_applied_research_intake_v0_1.md`

New research/handoff artifact retained from Phase AGR-P1:
- `05_project_handoff_and_prompts/prompts/OFARM_Deep_Research_Prompt_Agronomic_Code_Binding_and_Intervention_Context_v0_1.md`

---

## 7. Post-AGR-P7 future-work gate

AGR-P2 through AGR-P7 are now closed at carrier, reconstruction, and baseline-harmonisation level. Future agronomic work should not reopen those closures unless a real contradiction, missing executable contract, or pilot failure is shown.

Activate additional follow-on work only when at least one is true:
- a real pilot or prototype needs the carrier
- a scenario fixture cannot be expressed honestly with the active contracts
- conformance evidence shows a repeatable implementation divergence
- a standards-alignment decision requires external research before field use

---

## 8. Smallest controlled patch sequence

1. Keep the existing architecture unchanged.
2. Add scenario coverage and machine-readable scenario expectations.
3. Run the scenario fixture runner to prove the current package state is honestly partial.
4. Use the runner output to decide which future RFC/contract closures become active.
5. Baseline harmonisation was kept last and is now closed by AGR-P7.

---

## 9. Non-negotiable preservation rules

All agronomic amendments must preserve:
- assertion/history-first canonical truth
- governed current-state materialization
- Advisory Twin versus Compliance Twin separation
- explicit event grammar and commit classes
- explicit authority, evidence, and promotion gates
- explicit source-of-truth discipline
- stale-materialization refusal or review for high-consequence outputs
- pack compatibility and non-mutation of core meaning

No agronomic patch may compensate for missing payload fields by weakening promotion law.

---

## 10. Phase AGR-P2 closure note — 2026-05-12

Phase AGR-P2 is closed at the carrier-shell level.

Closure artifacts:
- accepted RFC: `02_accepted_rfcs/OFARM_Agronomic_Observation_and_Measurement_Context_RFC_v0_1.md`
- active observation-context contract: `03_machine_contracts/schemas/agronomic/OFARM_AgronomicObservationContext_schema_v0_1.json`
- active measurement-evidence contract: `03_machine_contracts/schemas/evidence/OFARM_MeasurementEvidence_schema_v0_1.json`
- fixture runner/result: `04_implementation_and_conformance/conformance_runners/agronomic_conformance/ofarm_agronomic_observation_measurement_context_runner_v0_1.py`, `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_agronomic_observation_measurement_context_results_v0_1.json`

Validation status:
- `ofarm_agronomic_observation_measurement_context_runner_v0_1.py` returns `PASS`
- `ofarm_contract_validation_runner_v0_20.py` returns `PASS` after the new contract family and examples
- `ofarm_agronomic_scenario_fixture_runner_v0_1.py` remains `PASS_WITH_LIMITATIONS` because intervention, extent, code-binding, and query/output closures remain future work

Boundary:
- no active baseline file was edited in this phase
- `EvidenceSufficiencyCase v0.2` was not schema-expanded; it is reused through bridge examples
- partial extent, agronomic code-binding, and query/output reconstruction remain explicitly separate tasks

## 11. Phase AGR-P3 closure note — 2026-05-12

Phase AGR-P3 is closed at the carrier-shell level.

Closure artifacts:
- accepted RFC: `02_accepted_rfcs/OFARM_Quantity_Bearing_Intervention_and_As_Applied_RFC_v0_1.md`
- active intent contract: `03_machine_contracts/schemas/agronomic/OFARM_InterventionIntentPayload_schema_v0_1.json`
- active execution/as-applied contract: `03_machine_contracts/schemas/agronomic/OFARM_ExecutionRecordPayload_schema_v0_1.json`
- fixture runner/result: `04_implementation_and_conformance/conformance_runners/agronomic_conformance/ofarm_agronomic_intervention_as_applied_runner_v0_1.py`, `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_agronomic_intervention_as_applied_results_v0_1.json`

Validation status:
- `ofarm_agronomic_intervention_as_applied_runner_v0_1.py` returns `PASS`
- `ofarm_contract_validation_runner_v0_20.py` returns `PASS` after the new contract family and bridge examples
- `ofarm_agronomic_observation_measurement_context_runner_v0_1.py` remains `PASS`
- `ofarm_agronomic_scenario_fixture_runner_v0_1.py` remains `PASS_WITH_LIMITATIONS` because code-binding and query/output closures remain future work

Boundary:
- no active baseline file was edited in this phase
- `EvidenceSufficiencyCase v0.2` was not schema-expanded; it is reused through bridge examples
- `PlannedIntervention`, `AssertionRecord`, `SemanticEventEnvelope`, and `AcceptedEventConsequence` received optional additive payload reference fields only
- `PartialExtent` is now active; agronomic code-binding and query/output reconstruction remain explicitly separate tasks


## 9. Phase AGR-P4 closure note — 2026-05-13

`IMP-306` has been activated and closed at the reusable carrier-shell level.

New active artifacts:

- `02_accepted_rfcs/OFARM_Partial_Extent_and_Geometry_Basis_RFC_v0_1.md`
- `03_machine_contracts/schemas/agronomic/OFARM_PartialExtent_schema_v0_1.json`

New supporting conformance artifacts:

- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_Agronomic_Partial_Extent_Geometry_Basis_Fixtures_v0_1.md`
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_agronomic_partial_extent_geometry_basis_records_v0_1.json`
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/ofarm_agronomic_partial_extent_geometry_basis_runner_v0_1.py`
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_agronomic_partial_extent_geometry_basis_results_v0_1.json`

Status changes:

- `IMP-302`: closed/superseded by `IMP-306`
- `IMP-306`: `DONE`
- `IMP-304` and `IMP-308`: remain active scenario/matrix support
- `IMP-307`: next highest-leverage standards/profile patch
- `IMP-309`, `IMP-310`, `IMP-311`: unchanged queued/gated posture

Boundary:

- No active baseline law is edited in this phase.
- PartialExtent does not mint durable identities by itself.
- Geometry imports remain evidence/exchange surfaces rather than truth stores.
- Query/output reconstruction and baseline harmonisation remain later phases.


## Phase AGR-P5 closure — code-binding and standards profile

Phase AGR-P5 adds scheme-bound identity and profile control without changing baseline law text.

Added active substance:

- `02_accepted_rfcs/OFARM_Agronomic_Code_Binding_and_Standards_Profile_RFC_v0_1.md`
- `03_machine_contracts/schemas/agronomic/OFARM_AgronomicIdentityBinding_schema_v0_1.json`
- `03_machine_contracts/schemas/agronomic/OFARM_AgronomicCodeBindingProfile_schema_v0_1.json`

Added active supporting conformance:

- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_Agronomic_Code_Binding_Profile_Fixtures_v0_1.md`
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_agronomic_code_binding_profile_records_v0_1.json`
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/ofarm_agronomic_code_binding_profile_runner_v0_1.py`
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_agronomic_code_binding_profile_results_v0_1.json`

The phase closes `IMP-307`. It preserves the rule that external standards, runtime lookup surfaces, registries, packs, and free-text labels do not become hidden OFARM law or canonical farm truth.

## AGR-P6 closure — query/output reconstruction

AGR-P6 is closed at RFC, machine-contract, and conformance-fixture level. It adds reconstruction policy and trace shells, patches query/output contracts additively, and covers all AGR-P1 scenarios with query reconstruction examples.

AGR-P7 baseline harmonisation is now closed by the Phase AGR-P7 package. AGR-P6 itself did not edit `00_active_baseline/`; AGR-P7 does.


## AGR-P7 closure — baseline harmonisation

AGR-P7 is closed at baseline-harmonisation level.

Updated active baseline artifacts:
- `00_active_baseline/OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md`
- `00_active_baseline/OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md`
- `00_active_baseline/OFARM_Alignment_Register_v0_13.md`
- `00_active_baseline/OFARM_post_gap_closure_readiness_gate_memo_v0_1.md`
- `00_active_baseline/OFARM_final_hostile_review_after_gap_closure_v0_1.md`

Supporting closure artifacts:
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_Agronomic_Baseline_Harmonisation_Summary_v0_1.md`
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/ofarm_agronomic_baseline_harmonisation_runner_v0_1.py`
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_agronomic_baseline_harmonisation_results_v0_1.json`

Boundary:
- no new carrier design was introduced in AGR-P7
- accepted AGR-P2 through AGR-P6 RFC and machine-contract closures were reflected in baseline law
- livestock remains out of scope for this crop-farming release unless a later accepted profile or sister model is opened
- external standards remain anchors, bindings, exchange mappings, runtime surfaces, or attestation wrappers, not hidden OFARM truth


## 18. Phase AGR-P8 runtime-chain closure note — 2026-05-13

AGR-P8 closes the remaining AGR-P1 limitation at package-local conformance level.

Closure artifacts:

- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_Agronomic_Runtime_Chain_Closure_Fixtures_v0_1.md`
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_agronomic_runtime_chain_records_v0_1.json`
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/ofarm_agronomic_runtime_chain_runner_v0_1.py`
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_agronomic_runtime_chain_results_v0_1.json`
- updated `04_implementation_and_conformance/conformance_runners/agronomic_conformance/ofarm_agronomic_scenario_fixture_runner_v0_1.py`
- updated `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_agronomic_scenario_fixture_results_v0_1.json`

Validation status:

- `ofarm_agronomic_runtime_chain_runner_v0_1.py` returns `PASS`
- `ofarm_agronomic_scenario_fixture_runner_v0_1.py` now returns `PASS` when AGR-P8 results are present
- AGR-P2 through AGR-P7 runners remain `PASS`

Boundary:

- no new baseline law, accepted RFC, or machine-contract schema was required
- AGR-P8 proves package-local chain composition only
- live pilot evidence, live registry checks, and wire-level ISOXML/EFDI/ADAPT mappings remain future trigger-based work

## AGR-P9 closure — local-knowledge rationale lineage

AGR-P9 closes `IMP-310` at package-local conformance level.

Closure artifacts:

- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_Agronomic_Local_Knowledge_Rationale_Lineage_Fixtures_v0_1.md`
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_Agronomic_Local_Knowledge_Rationale_Lineage_Summary_v0_1.md`
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_agronomic_local_knowledge_rationale_lineage_records_v0_1.json`
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/ofarm_agronomic_local_knowledge_rationale_lineage_runner_v0_1.py`
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_agronomic_local_knowledge_rationale_lineage_results_v0_1.json`

AGR-P9 does not add new baseline law or schemas. It proves that local knowledge can be retained as explainable rationale while only reviewed accepted consequences may support compliance-grade outputs.


## Phase AGR-P10 — FMIS investigation intake and KIS adapter spike fixture

Status: package-local implementation/conformance closure completed for the returned Codex investigation report.

AGR-P10 does not change baseline law, accepted RFCs, or active machine-contract schemas. It imports the Codex report as active supporting implementation evidence and converts the redacted KIS operation packet into candidate OFARM carrier fixtures.

The key decision is that `prod__t_kis__*` BigQuery marts are useful discovery surfaces, not OFARM source truth. The package-local KIS fixture passes only because promotion remains blocked and missing external evidence is explicit.

Remaining work after AGR-P10:

- collect the P0 evidence bundle,
- prove original source/API/machine payload lineage,
- prove authority/delegation and acceptance decisions,
- prove correction/dispute/supersession behavior,
- bind local materials to regulatory product identity before compliance use,
- build a read-only adapter prototype only after evidence gates are supplied.
