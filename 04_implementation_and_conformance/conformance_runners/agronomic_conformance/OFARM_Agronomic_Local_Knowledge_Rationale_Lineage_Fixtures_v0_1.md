
# OFARM Agronomic Local-Knowledge Rationale Lineage Fixtures v0.1

Date: 2026-05-13  
Status: active supporting conformance artifact  
Scope: Phase AGR-P9 closure for `IMP-310` local-knowledge rationale lineage fixtures

---

## 1. Purpose

AGR-P9 closes the remaining agronomist-review opportunity that local farm knowledge should become an explainable rationale trail without becoming compliance truth by shortcut.

The fixture set proves this chain:

`NarrativeObservation -> LocalMemoryRule -> advisory recommendation -> PlannedIntervention -> operation claim -> reviewed accepted consequence`

The chain is deliberately **not** a new truth model. It only links already active OFARM carrier families in a conformance fixture.

---

## 2. Boundary

This phase does not add baseline law, accepted RFCs, or new schemas.

It adds:
- machine-contract examples using existing schemas
- package-local lineage records
- a package-local runner and results

It preserves:
- narrative/local knowledge as evidence and rationale
- Advisory Twin / Compliance Twin separation
- plan versus claim versus accepted consequence separation
- assertion/history-first truth
- governed materialization and output disclosure rules

---

## 3. Positive lineage fixture

The main positive fixture links:

1. `OFARM_NarrativeObservation_example_field_17_west_edge_canopy_note_v0_1.json`
2. `OFARM_AgronomicObservationContext_example_field_17_narrative_only_low_consequence_v0_1.json`
3. `OFARM_LocalMemoryRule_example_field_17_west_edge_mildew_rule_v0_1.json`
4. `OFARM_InterventionIntentPayload_example_field_17_canopy_pruning_recommendation_from_local_rule_v0_1.json`
5. `OFARM_InterventionIntentPayload_example_field_17_canopy_pruning_planned_operation_from_local_rule_v0_1.json`
6. `OFARM_PlannedIntervention_example_field_17_row_selective_pruning_v0_1.json`
7. `OFARM_ExecutionRecordPayload_example_field_17_canopy_pruning_operation_claim_from_local_rule_v0_1.json`
8. `OFARM_AssertionRecord_example_pruning_operation_claim_v0_1.json`
9. `OFARM_ExecutionRecordPayload_example_field_17_canopy_pruning_accepted_execution_from_local_rule_v0_1.json`
10. `OFARM_AcceptedEventConsequence_example_pruning_operation_confirmed_v0_1.json`

Expected result: the rationale is reconstructable, but only the reviewed accepted consequence can support compliance-grade accepted execution.

---

## 4. Negative controls

The runner requires explicit negative controls for:

- direct promotion of a narrative observation into compliance truth
- direct promotion of a local memory rule into accepted execution
- treating a recommendation as a prescription or plan
- treating a plan as an operation claim
- treating an operation claim as an accepted consequence
- default PassportView exposure of advisory/local rationale without profile permission

---

## 5. Validation

The runner is:

- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/ofarm_agronomic_local_knowledge_rationale_lineage_runner_v0_1.py`

It validates:

- referenced package-local artifacts exist
- referenced JSON examples validate against their schemas where a schema is declared
- upstream AGR-P2 through AGR-P8 result files are present and passing
- every lineage step has an explicit stage and distinctness rule
- Advisory/Compliance separation is preserved
- accepted outcomes are represented only through reviewed accepted-consequence records

---

## 6. Remaining non-claims

AGR-P9 is still not:

- live pilot evidence
- a production runtime proof
- a wire-level exchange mapping
- an external registry check
- a claim that local heuristics are regulatory evidence by themselves
