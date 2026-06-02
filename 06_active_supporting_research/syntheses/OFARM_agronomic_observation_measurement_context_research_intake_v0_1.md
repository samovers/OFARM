# OFARM agronomic observation and measurement context research intake v0.1

Date: 2026-05-12  
Status: active supporting research intake  
Scope: intake summary for the user-supplied Deep Research report used to activate Phase 2 agronomic observation and measurement context closure

---

## 1. Source

This intake summarizes the user-supplied `deep-research-report-21.md` received on 2026-05-12.

The report is supporting research. It informs this amendment but does not override the active baseline by itself.

---

## 2. Research conclusions used in Phase 2

The report recommends a small-carrier approach rather than a greenfield agronomy redesign.

For Phase 2, the actionable conclusions are:

- create an `AgronomicObservationContext` carrier for field observations in agronomic context
- create a `MeasurementEvidence` carrier for sampled, measured, sensed, lab-derived, or imported measurement evidence
- keep `NarrativeObservation` as the rich human-observation carrier
- make method, sampling, time, spatial basis, evidence, provenance, quantity kind, unit, threshold, uncertainty, calibration, and laboratory context explicit when they matter
- align to O&M, SOSA/SSN, OWL-Time, GeoSPARQL-style spatial discipline, PROV-O, QUDT, UCUM, BBCH, EPPO, AGROVOC, Crop Ontology, and relevant registries without importing those standards as hidden OFARM law

---

## 3. Research conclusions deferred to later phases

The report also recommends carrier shells for:

- agronomic identity binding
- intervention intent payload
- execution record payload
- partial extent
- query/output reconstruction policy

Those remain follow-on work under `IMP-305`, `IMP-306`, `IMP-307`, and `IMP-309`.

---

## 4. Phase 2 application

Phase 2 applies the research by creating:

- `02_accepted_rfcs/OFARM_Agronomic_Observation_and_Measurement_Context_RFC_v0_1.md`
- `03_machine_contracts/schemas/agronomic/OFARM_AgronomicObservationContext_schema_v0_1.json`
- `03_machine_contracts/schemas/evidence/OFARM_MeasurementEvidence_schema_v0_1.json`
- positive examples and evidence-sufficiency bridge examples
- a supporting fixture runner and results record

No active baseline law text is changed in this phase.
