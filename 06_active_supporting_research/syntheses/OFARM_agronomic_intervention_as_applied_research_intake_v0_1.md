# OFARM agronomic intervention and as-applied research intake v0.1

Date: 2026-05-12  
Status: active supporting research intake  
Scope: intake summary for the user-supplied Deep Research report used to activate Phase AGR-P3 quantity-bearing intervention and as-applied closure

---

## 1. Source

This intake summarizes the user-supplied `deep-research-report-21.md` received on 2026-05-12.

The report is supporting research. It informs this amendment but does not override the active baseline by itself.

---

## 2. Research conclusions used in Phase AGR-P3

The report recommends small OFARM carrier shells rather than a greenfield agronomy ontology.

For Phase AGR-P3, the actionable conclusions are:

- keep operational states disjoint
- carry rate, dose, concentration, quantity, quantity kind, and unit explicitly
- preserve recommendation, prescription, plan, operation claim, as-applied evidence, accepted consequence, correction, and dispute as separate states
- treat ADAPT, ISOXML, EFDI, ISOBUS DDI, machine logs, and controller files as exchange/evidence surfaces rather than truth stores
- preserve late evidence and corrections as first-class records rather than overwrite paths

---

## 3. Phase AGR-P3 application

Phase AGR-P3 applies the research by creating:

- `02_accepted_rfcs/OFARM_Quantity_Bearing_Intervention_and_As_Applied_RFC_v0_1.md`
- `03_machine_contracts/schemas/agronomic/OFARM_InterventionIntentPayload_schema_v0_1.json`
- `03_machine_contracts/schemas/agronomic/OFARM_ExecutionRecordPayload_schema_v0_1.json`
- positive examples for recommendation, prescription, planned operation, late contractor claim, partial machine as-applied evidence, partial accepted execution, correction, and dispute
- evidence-sufficiency bridge examples using existing `EvidenceSufficiencyCase v0.2`
- a dedicated Phase AGR-P3 runner and result record

No active baseline law text is changed in this phase.

---

## 4. Deferred research conclusions

The report also recommends carrier shells or policy work for:

- full partial extent and geometry basis
- agronomic code-binding profile
- query/output reconstruction policy
- later baseline harmonisation

Those remain follow-on work under `IMP-306`, `IMP-307`, `IMP-309`, and `IMP-311`.
