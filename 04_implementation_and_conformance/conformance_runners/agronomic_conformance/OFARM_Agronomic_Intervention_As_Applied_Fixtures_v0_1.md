# OFARM agronomic intervention and as-applied fixtures v0.1

Date: 2026-05-12  
Status: active supporting implementation/conformance artifact  
Scope: Phase AGR-P3 fixtures for quantity-bearing intervention intent and execution/as-applied payload closure

---

## 1. Purpose

These fixtures validate the Phase AGR-P3 carrier closure introduced by `OFARM_Quantity_Bearing_Intervention_and_As_Applied_RFC_v0_1.md`.

The goal is not to create a universal operation ontology.
The goal is to prove that OFARM can preserve agronomic intervention payloads across recommendation, prescription, planned operation, operation claim, as-applied evidence, accepted execution, correction, and dispute without weakening promotion law.

---

## 2. Fixture families

| Fixture family | Positive artifacts | Expected posture |
|---|---|---|
| advisory recommendation | `OFARM_InterventionIntentPayload_example_field_17_spot_spray_advisory_recommendation_v0_1.json` | advisory-only; no authority or execution truth |
| authorised prescription | `OFARM_InterventionIntentPayload_example_field_17_spot_spray_authorized_prescription_v0_1.json` | authorised intent with product/rate/target/time window; not execution |
| planned operation | `OFARM_InterventionIntentPayload_example_field_17_spot_spray_planned_operation_v0_1.json`, `OFARM_PlannedIntervention_example_field_17_spot_spray_with_intent_payload_v0_1.json` | planned work only; no accepted consequence |
| delayed contractor claim | `OFARM_ExecutionRecordPayload_example_field_17_contractor_spot_spray_claim_late_sync_v0_1.json`, `OFARM_AssertionRecord_example_field_17_contractor_spot_spray_claim_with_execution_payload_v0_1.json` | retained operation claim; missing rate requires review |
| partial as-applied evidence | `OFARM_ExecutionRecordPayload_example_field_17_machine_log_partial_application_v0_1.json` | retained machine/import evidence; not truth by import |
| partial accepted execution | `OFARM_ExecutionRecordPayload_example_field_17_partial_accepted_execution_v0_1.json`, `OFARM_AcceptedEventConsequence_example_field_17_partial_spot_spray_with_execution_payload_v0_1.json` | accepted only for reviewed sub-extent |
| manual correction | `OFARM_ExecutionRecordPayload_example_field_17_manual_correction_supersedes_claim_v0_1.json` | correction lineage preserved without deleting original claim |
| extent dispute | `OFARM_ExecutionRecordPayload_example_field_17_extent_dispute_v0_1.json` | disputed record remains visible and review-gated |
| sufficiency bridge | `OFARM_EvidenceSufficiencyCase_example_intervention_missing_rate_review_v0_2.json`, `OFARM_EvidenceSufficiencyCase_example_partial_as_applied_acceptance_v0_2.json` | existing evidence-sufficiency v0.2 evaluates Phase 3 payloads |

---

## 3. Required behavior

A conforming implementation must show that:

1. quantity-bearing recommendations remain advisory unless separately authorised and promoted
2. authorised prescriptions still do not imply execution
3. plans still do not imply execution
4. late contractor claims can be retained without becoming accepted consequences
5. missing rate blocks automatic accepted execution
6. machine/as-applied evidence preserves source semantics without becoming truth by import
7. accepted execution is limited to reviewed actual extent and quantity basis
8. corrections supersede through history rather than edit/delete
9. disputes remain visible and excluded from high-consequence materialization until resolved
10. every carried quantity has both quantity-kind and unit semantics

---

## 4. Boundary

These fixtures do not close the full partial-extent/geometry-basis carrier, the agronomic code-binding profile, or query/output reconstruction.
Those remain follow-on phases.
