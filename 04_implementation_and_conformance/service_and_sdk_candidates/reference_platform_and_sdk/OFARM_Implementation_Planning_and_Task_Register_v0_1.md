# OFARM implementation planning and task register v0.1

Date: 2026-04-20  
Status: active supporting implementation artifact  
Scope: package-wide planning and task-intake scaffold for implementation, conformance, and pre-implementation carry-forward work after the post-hardening readiness v0.7 checkpoint  
Audience: repository stewards, implementers, reviewers, and AI agents

---

## 1. Why this file exists

The package now has:
- an implementation-directed stop point
- a bounded-debt readiness recommendation
- many seam-specific fixture lanes, memos, and spike notes

What it does **not** yet have is one package-wide home for implementation tasks that appear across seams.

This file creates that home.

It is the place to:
- log new implementation tasks
- classify whether a task belongs in planning only, implementation support, conformance, RFC extension, or later baseline harmonisation
- decide whether a task should start now or remain gated
- keep pre-implementation carry-forward tasks from getting lost or silently promoted into active law

The machine-readable companion register is:

- `04_implementation_and_conformance/service_and_sdk_candidates/reference_platform_and_sdk/OFARM_Implementation_Task_Register_v0_1.json`

---

## 2. Authority and boundary

This file is an **implementation/support artifact**.
It does **not** override the active authority set.

Use this scaffold under the normal OFARM authority order:

1. `00_active_baseline/`
2. `02_accepted_rfcs/`
3. `01_companion_artifacts/`
4. `03_machine_contracts/`
5. `04_implementation_and_conformance/`

This scaffold therefore:
- may organize work
- may triage tasks
- may point at candidate next changes

It may **not**:
- silently reopen RC2.1
- silently convert reviewed ideas into active law
- silently treat implementation-local work as standardized OFARM semantics

---

## 3. Current package decision

Current package posture remains:

- package phase = `IMPLEMENTATION_AND_EVIDENCE`
- gate outcome = `IMPLEMENTATION_DIRECTED_WITH_BOUNDED_DEBT`
- package-internal hardening stop point = valid unless a real trigger exists

Therefore the default operating mode is:

**Phase 0 — planning and task intake is active now.**

That means:
- new tasks should be logged and classified here
- implementation-support and repo-hygiene tasks may proceed
- semantic/runtime closure phases should stay gated unless an immediate implementation or pilot trigger exists

---

## 4. Phase model

| Phase | Name | Default posture now | When to activate | Typical outputs |
|---|---|---|---|---|
| P0 | Planning and task intake | ACTIVE | always | task triage, gating decisions, implementation planning notes, task register updates |
| P1 | Cross-cutting integrity patch wave | GATED | immediate implementation/prototype/pilot blocker across multiple seams | narrow RFC/support notes, machine-contract patches, validation updates |
| P2 | Hostile regression wave | GATED | implementation path needs end-to-end break tests | hostile fixtures, runner updates, regression records |
| P3 | Pilot-triggered semantic micro-closures | GATED | pilot scope proves a specific missing semantic carrier is needed | small reusable carrier contracts and targeted examples |
| P4 | Structural artifact-family cleanup | GATED | more than one implementation needs clearer standardized-surface or module/status structure | status artifacts, module boundary cleanup, possible later harmonisation |
| P5 | Live evidence and accountable review | EXTERNAL_TRIGGER | real pilot/runtime evidence arrives | intake packets, decision records, accountable acceptance/refusal traces |

### 4.1 Phase 0 — planning and task intake

Phase 0 is the package-wide holding and triage phase.
Use it to:
- register new work items
- classify authority impact
- decide whether a task is gated or active
- keep implementation tasks visible without pretending they are already approved change waves

### 4.2 Phase 1 — cross-cutting integrity patch wave

Only activate when an immediate implementation or pilot is blocked by a cross-cutting semantic/runtime gap.

Current candidate tasks in this lane:
- temporal qualifier micro-closure
- governed authority and role code closure
- currentness and standardized-surface boundary honesty cleanup

### 4.3 Phase 2 — hostile regression wave

Only activate when a real implementation path needs proof that the active package survives hostile edge cases.

Current candidate tasks in this lane:
- offline contractor late-sync regression
- boundary correction after frozen submission regression

### 4.4 Phase 3 — pilot-triggered semantic micro-closures

Only activate when a real pilot scope demonstrates a specific missing semantic carrier.

Current candidate tasks in this lane:
- quantity-bearing intervention carrier
- geometry-basis descriptor

### 4.5 Phase 4 — structural artifact-family cleanup

Only activate when real implementation or external-profile work proves the current status/module boundary is too implicit.

Current candidate task in this lane:
- structural cleanup for the claimed standardized surface and machine-readable status boundary

### 4.6 Phase 5 — live evidence and accountable review

This phase begins only when real external evidence is present.
It is intentionally not started by package-internal planning alone.

---

## 5. How to use the register

### 5.1 When a new task appears

For every new task:
1. identify the authority level it touches
2. assign a phase
3. decide whether it is `ACTIVE`, `QUEUED`, or `GATED_HOLD`
4. record the smallest controlled patch that would solve it
5. list affected artifacts
6. add or update the task in the JSON register

### 5.2 Allowed status values

Use these register statuses:
- `INTAKE`
- `GATED_HOLD`
- `QUEUED`
- `ACTIVE`
- `BLOCKED`
- `DONE`
- `SUPERSEDED`
- `DROPPED`

### 5.3 Change-class guidance

Use one of these broad change classes when logging a task:
- `IMPLEMENTATION_PLANNING`
- `IMPLEMENTATION_CONFORMANCE`
- `MACHINE_CONTRACT_PATCH`
- `RFC_EXTENSION`
- `BASELINE_HARMONISATION_LATER`
- `EXTERNAL_EVIDENCE_OPERATION`

### 5.4 Agent rule

Agents should prefer:
- the smallest controlled patch
- support-layer or conformance fixes before baseline edits
- explicit affected-file lists
- explicit trigger conditions before moving a task from `GATED_HOLD` to `ACTIVE`

Agents should avoid:
- opening broad redesign threads
- silently moving implementation notes into active law
- starting Phase 1+ just because a task looks interesting

### 5.5 Companion task notes

When a task grows beyond one register entry, create a companion note in `04_implementation_and_conformance/` using:

- `OFARM_Implementation_Task_<short_name>_v0_1.md`

Then link that note from the JSON register in `detailRef`.

---

## 6. Starter package-wide task set

The initial starter set is intentionally small and mirrors the currently identified implementation-facing debt:

- `IMP-000` — establish this package-wide planning/task register scaffold
- `IMP-101` — temporal qualifier micro-closure
- `IMP-102` — governed authority and role code closure
- `IMP-103` — currentness and standardized-surface boundary honesty cleanup
- `IMP-201` — offline contractor late-sync hostile regression
- `IMP-202` — boundary correction after frozen submission hostile regression
- `IMP-301` — quantity-bearing intervention carrier
- `IMP-302` — geometry-basis descriptor
- `IMP-401` — structural artifact-family/status cleanup
- `IMP-501` — live evidence and accountable review on first real packet

Additional agronomist-review amendment lane tasks added on 2026-05-12:

- `IMP-303` — agronomic observation and measurement context carrier
- `IMP-304` — agronomic scenario fixture library
- `IMP-305` — agronomic quantity-bearing intervention closure
- `IMP-306` — partial extent and geometry-basis closure
- `IMP-307` — agronomic code-binding and standards profile
- `IMP-308` — farm scenario coverage matrix
- `IMP-309` — agronomic query and output reconstruction fixtures
- `IMP-310` — agronomic local-knowledge rationale lineage fixtures
- `IMP-311` — crop-only scope and livestock non-goal harmonisation

These tasks are registered machine-readably in the companion JSON file.

---

## 7. Immediate operating rule

Until a real implementation or pilot trigger is explicit:

- keep Phase 0 active
- log new work here
- keep cross-cutting semantic closure tasks in `GATED_HOLD`
- allow only planning, organization, implementation-support prep, and conformance-prep work that does not silently reopen active law

That preserves the current stop-point while still giving the project one durable place to put implementation work as it appears.

---

## 8. What changed by adding this scaffold

This patch starts **Phase 0** in a formal, package-visible way.

It does **not** start Phase 1 or Phase 2 yet.
Those remain ready but gated.

That is the intended posture for the current repository state.

---

## 9. Agronomist-review amendment intake addendum — 2026-05-12

The Senior Agronomist Reviewer findings are now registered as a controlled implementation/conformance amendment lane.

This addendum starts only support-layer planning and scenario coverage. It does **not** reopen RC2.1, modify active law, or create new machine contracts.

New or refined agronomic tasks:

- `IMP-303` — agronomic observation and measurement context carrier
- `IMP-304` — agronomic scenario fixture library
- `IMP-305` — agronomic quantity-bearing intervention closure
- `IMP-306` — partial extent and geometry-basis closure
- `IMP-307` — agronomic code-binding and standards profile
- `IMP-308` — farm scenario coverage matrix
- `IMP-309` — agronomic query and output reconstruction fixtures
- `IMP-310` — agronomic local-knowledge rationale lineage fixtures
- `IMP-311` — crop-only scope and livestock non-goal harmonisation

Active now:

- `IMP-304`
- `IMP-308`

Queued or gated:

- `IMP-303` is now closed at the carrier-shell level by the Phase AGR-P2 RFC and machine contracts.
- `IMP-305` is now closed at carrier-shell level by the Phase AGR-P3 RFC and machine contracts; `IMP-306` is now closed at carrier-shell level by the Phase AGR-P4 RFC and machine contracts; `IMP-307` remains queued until standards research proves the exact minimum patch.
- `IMP-309` and `IMP-310` remain queued until carriers or pilot queries make executable reconstruction necessary.
- `IMP-311` remains gated for later baseline harmonisation unless scope ambiguity becomes a real implementation contradiction.

Primary new artifacts:

- `OFARM_Agronomic_Amendment_Control_Plan_v0_1.md`
- `OFARM_Agronomic_Scenario_Coverage_Matrix_v0_1.md`
- `OFARM_Agronomic_Scenario_Fixtures_v0_1.md`
- `OFARM_agronomic_scenario_records_v0_1.json`
- `ofarm_agronomic_scenario_fixture_runner_v0_1.py`
- `OFARM_agronomic_scenario_fixture_results_v0_1.json`

Operating rule:

Use the agronomic scenario records to drive the next RFC/contract patches. Do not promote the supporting research or scenario expectations into baseline law without an accepted RFC and matching machine contract where needed.

---


## 10. Agronomic observation and measurement context closure addendum — 2026-05-12

`IMP-303` has been activated and closed at the reusable carrier-shell level.

Closed outputs:
- `02_accepted_rfcs/OFARM_Agronomic_Observation_and_Measurement_Context_RFC_v0_1.md`
- `03_machine_contracts/schemas/agronomic/OFARM_AgronomicObservationContext_schema_v0_1.json`
- `03_machine_contracts/schemas/evidence/OFARM_MeasurementEvidence_schema_v0_1.json`
- positive examples for scouting context, sample pending lab result, below-LOQ lab result, calibrated sensor evidence, and narrative-only degraded context
- evidence-sufficiency bridge examples using existing `EvidenceSufficiencyCase v0.2`
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_Agronomic_Observation_Measurement_Context_Fixtures_v0_1.md`
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/ofarm_agronomic_observation_measurement_context_runner_v0_1.py`
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_agronomic_observation_measurement_context_results_v0_1.json`

Posture:
- `IMP-303`: `DONE`
- `IMP-304` and `IMP-308`: remain active scenario/matrix support
- `IMP-305`: closed at carrier-shell level by the Phase AGR-P3 RFC and machine contracts
- `IMP-306`: closed at carrier-shell level by the Phase AGR-P4 RFC and machine contracts
- `IMP-307`, `IMP-309`, `IMP-310`, `IMP-311`: unchanged queued/gated posture

Boundary:
- no active baseline text was modified
- the new RFC and machine contracts sit inside the active authority set
- later baseline harmonisation remains Phase AGR-P7 only


---

## 11. Agronomic quantity-bearing intervention and as-applied closure addendum — 2026-05-12

`IMP-305` has been activated and closed at the reusable carrier-shell level.

Closed outputs:
- `02_accepted_rfcs/OFARM_Quantity_Bearing_Intervention_and_As_Applied_RFC_v0_1.md`
- `03_machine_contracts/schemas/agronomic/OFARM_InterventionIntentPayload_schema_v0_1.json`
- `03_machine_contracts/schemas/agronomic/OFARM_ExecutionRecordPayload_schema_v0_1.json`
- positive examples for advisory recommendation, authorised prescription, planned operation, delayed contractor claim, partial machine as-applied evidence, partial accepted execution, manual correction, and extent dispute
- bridge examples for `PlannedIntervention`, `AssertionRecord`, `SemanticEventEnvelope`, `AcceptedEventConsequence`, and `EvidenceSufficiencyCase v0.2`
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_Agronomic_Intervention_As_Applied_Fixtures_v0_1.md`
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/ofarm_agronomic_intervention_as_applied_runner_v0_1.py`
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_agronomic_intervention_as_applied_results_v0_1.json`

Posture:
- `IMP-301`: closed/superseded by `IMP-305`
- `IMP-305`: `DONE`
- `IMP-304` and `IMP-308`: remain active scenario/matrix support
- `IMP-306`: closed at carrier-shell level by the Phase AGR-P4 RFC and machine contracts
- `IMP-307`, `IMP-309`, `IMP-310`, `IMP-311`: unchanged queued/gated posture

Boundary:
- no active baseline text was modified
- no external machine or FMIS exchange format became OFARM truth law
- `EvidenceSufficiencyCase v0.2` was reused, not widened
- the patch separates intent payloads from execution/as-applied payloads to avoid the one-object application anti-pattern


---

## Phase AGR-P4 amendment note — 2026-05-13

`IMP-306` has been activated and closed at carrier-shell level.

New active artifacts:

- `02_accepted_rfcs/OFARM_Partial_Extent_and_Geometry_Basis_RFC_v0_1.md`
- `03_machine_contracts/schemas/agronomic/OFARM_PartialExtent_schema_v0_1.json`

New supporting artifacts:

- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_Agronomic_Partial_Extent_Geometry_Basis_Fixtures_v0_1.md`
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_agronomic_partial_extent_geometry_basis_records_v0_1.json`
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/ofarm_agronomic_partial_extent_geometry_basis_runner_v0_1.py`
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_agronomic_partial_extent_geometry_basis_results_v0_1.json`

Task posture update:

- `IMP-302`: `DONE`, superseded by `IMP-306`
- `IMP-306`: `DONE`
- `IMP-304` and `IMP-308`: remain active scenario/matrix support
- `IMP-307`: next recommended standards/code-binding phase
- `IMP-309`: remains queued until query/output reconstruction phase
- `IMP-311`: remains gated baseline harmonisation

Boundary:

Phase AGR-P4 adds a geometry-basis carrier. It does not turn OFARM into a GIS topology engine, does not promote geometry imports to truth, and does not create durable identities unless existing identity/lifecycle law requires them.


## Phase AGR-P5 closure — agronomic code-binding and standards profile

Status: closed for this package increment.

Phase AGR-P5 closes `IMP-307` by adding:

- accepted RFC: `02_accepted_rfcs/OFARM_Agronomic_Code_Binding_and_Standards_Profile_RFC_v0_1.md`
- active schemas: `03_machine_contracts/schemas/agronomic/OFARM_AgronomicIdentityBinding_schema_v0_1.json` and `03_machine_contracts/schemas/agronomic/OFARM_AgronomicCodeBindingProfile_schema_v0_1.json`
- examples and bridge examples for scheme-bound identity, unresolved product capture, quantity kind plus unit-code policy, threshold-source binding, and code-bound observation/intent/execution records
- fixture note: `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_Agronomic_Code_Binding_Profile_Fixtures_v0_1.md`
- runner: `04_implementation_and_conformance/conformance_runners/agronomic_conformance/ofarm_agronomic_code_binding_profile_runner_v0_1.py`

The next agronomic implementation phase remains `IMP-309` query/output reconstruction. Baseline harmonisation remains gated until reconstruction fixtures prove stable.

## AGR-P6 closure note — query/output reconstruction

`IMP-309` is closed in this package. Closure artifacts:

- `02_accepted_rfcs/OFARM_Agronomic_Query_and_Output_Reconstruction_RFC_v0_1.md`
- `03_machine_contracts/schemas/agronomic/OFARM_AgronomicReconstructionPolicy_schema_v0_1.json`
- `03_machine_contracts/schemas/agronomic/OFARM_AgronomicReconstructionTrace_schema_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agronomic/OFARM_SemanticPathAliasCatalog_example_agronomic_reconstruction_profile_v0_1.json`
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_Agronomic_Query_Output_Reconstruction_Fixtures_v0_1.md`
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/ofarm_agronomic_query_output_reconstruction_runner_v0_1.py`

The closure is RFC/machine-contract/conformance level only. Baseline harmonisation remains gated.


## AGR-P7 closure note — baseline harmonisation

AGR-P7 is closed in this package.

- `IMP-311` is now `DONE`: the crop-only release boundary and livestock non-goal are explicit in the baseline.
- `IMP-312` is added as `DONE`: agronomic carrier baseline harmonisation reflects the already-accepted AGR-P2 through AGR-P6 RFC/contract closures.

Closure artifacts:
- `00_active_baseline/OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md`
- `00_active_baseline/OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md`
- `00_active_baseline/OFARM_Alignment_Register_v0_13.md`
- `00_active_baseline/OFARM_post_gap_closure_readiness_gate_memo_v0_1.md`
- `00_active_baseline/OFARM_final_hostile_review_after_gap_closure_v0_1.md`
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_Agronomic_Baseline_Harmonisation_Summary_v0_1.md`
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/ofarm_agronomic_baseline_harmonisation_runner_v0_1.py`
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_agronomic_baseline_harmonisation_results_v0_1.json`

Remaining agronomic posture:
- active carrier-shell law is baseline-harmonised
- scenario coverage remains an expectation-level harness until real implementation event chains and pilot datasets arrive
- external standard readiness remains out of claim scope


## AGR-P8 runtime-chain fixture closure — 2026-05-13

`IMP-313` is closed at package-local conformance-chain level.

New supporting conformance artifacts:

- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_Agronomic_Runtime_Chain_Closure_Fixtures_v0_1.md`
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_Agronomic_Runtime_Chain_Closure_Summary_v0_1.md`
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_agronomic_runtime_chain_records_v0_1.json`
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/ofarm_agronomic_runtime_chain_runner_v0_1.py`
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_agronomic_runtime_chain_results_v0_1.json`

Status changes:

- `IMP-304`: `DONE`; scenario fixture library now has package-local runtime-chain evidence.
- `IMP-313`: `DONE`; AGR-P8 runtime-chain closure added and validated.
- `IMP-308`: remains `ACTIVE` as a maintenance matrix, not as unresolved carrier debt.

Boundary:

- no active baseline law was changed
- no accepted RFC was added
- no machine-contract schema was added
- AGR-P8 is not a production runtime, live registry check, or wire-level exchange mapping

## AGR-P9 local-knowledge rationale lineage closure — 2026-05-13

`IMP-310` is closed at package-local conformance level.

New machine-contract examples using existing schemas:

- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agronomic/OFARM_InterventionIntentPayload_example_field_17_canopy_pruning_recommendation_from_local_rule_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agronomic/OFARM_InterventionIntentPayload_example_field_17_canopy_pruning_planned_operation_from_local_rule_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agronomic/OFARM_ExecutionRecordPayload_example_field_17_canopy_pruning_operation_claim_from_local_rule_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agronomic/OFARM_ExecutionRecordPayload_example_field_17_canopy_pruning_accepted_execution_from_local_rule_v0_1.json`

New supporting conformance artifacts:

- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_Agronomic_Local_Knowledge_Rationale_Lineage_Fixtures_v0_1.md`
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_Agronomic_Local_Knowledge_Rationale_Lineage_Summary_v0_1.md`
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_agronomic_local_knowledge_rationale_lineage_records_v0_1.json`
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/ofarm_agronomic_local_knowledge_rationale_lineage_runner_v0_1.py`
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_agronomic_local_knowledge_rationale_lineage_results_v0_1.json`

Status changes:

- `IMP-310`: `DONE`
- `IMP-308`: remains `ACTIVE` as scenario coverage maintenance only

Boundary:

- no active baseline law was changed
- no accepted RFC was added
- no machine-contract schema was added
- local knowledge remains rationale/evidence support and does not become compliance truth by shortcut


Additional FMIS implementation-discovery tasks added on 2026-05-13:

- `IMP-314` — FMIS interoperability investigation report intake
- `IMP-315` — KIS redacted adapter spike candidate fixture
- `IMP-316` — P0 FMIS evidence request bundle
- `IMP-317` — source-side correction and dispute reconstruction probe
- `IMP-318` — original machine/controller payload ingestion probe
- `IMP-319` — crop-protection product regulatory binding enrichment
- `IMP-320` — first read-only KIS adapter prototype

`IMP-314` and `IMP-315` are closed in the package because the Codex report was ingested and a redacted candidate fixture now passes package-local checks. `IMP-316` through `IMP-320` remain blocked or gated until external evidence is supplied.


Additional AGR-P10 addendum tasks added on 2026-05-13:

- `IMP-321` — Logineko entity package addendum intake — DONE
- `IMP-322` — entity-guided scouting and material-session probe expansion — BLOCKED

`IMP-321` is closed because the addendum was ingested as source-map aid evidence and the KIS adapter candidate runner now validates the checkpoint evidence while preserving promotion blockers. `IMP-322` remains blocked until source fields or operation examples are supplied for scouting links and material-session custody.

## Multi-addendum consolidation tasks — 2026-05-14

- `IMP-390` — consolidate May 14 multi-team addendums — `DONE`.
- `IMP-391` — review regulatory inspector RC2.1a held candidates — `GATED_HOLD`.
- `IMP-392` — rebase or supply CSF-P0 through P12 predecessor chain — `BLOCKED`.
- `IMP-393` — AI assistant computation promotion evidence review — `GATED_HOLD`.
- `IMP-394` — predevelopment AI-agent draft-artifact promotion review — `QUEUED`.
- `IMP-395` — farm-owner source-owner/live evidence closure — `GATED_HOLD`.

The P11/P12 task-register states from team packages were not copied into the active task register because they depend on missing predecessor packages. They remain review-holding source claims.

