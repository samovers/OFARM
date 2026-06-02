# OFARM Runtime Event Family and Promotion Fixtures v0.1

Date: 2026-04-12  
Status: active supporting implementation artifact  
Scope: bounded executable conformance proof for event-family coverage, subtype compatibility, and commit-promotion safety

---

## 1. Purpose

This fixture set closes the central conformance gap around the OFARM event grammar:

- all seven fixed top-level event families are exercised
- subtype compatibility is checked with allow, block, and governance-review outcomes
- commit-promotion safety is exercised with runtime-shaped promotion traces across all nine baseline commit classes

It is intended to strengthen the post-amendment package without changing:
- `00_active_baseline/`
- `01_companion_artifacts/`
- `02_accepted_rfcs/`
- `03_machine_contracts/`

---

## 2. Authority basis used

This wave is grounded in the already-active OFARM event grammar and promotion law:

- `00_active_baseline/OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md`
  - fixed top-level event families
  - family meanings
  - dominant semantic consequence rule
- `01_companion_artifacts/OFARM_Event_Grammar_and_Commit_Matrix_v0_1.md`
  - stable event grammar
  - commit classes
  - promotion matrix
  - default no-auto-promotion safety bias
- `00_active_baseline/OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md`
  - event-family-aware gate sequencing
  - commit-gate awareness
  - evidence/review/promotion distinctions

---

## 3. Executable fixture families

### 3.1 Top-level family coverage
The runner must prove coverage for all seven fixed families:

- `StructureEvent`
- `ObservationEvent`
- `OccurrenceEvent`
- `InterventionEvent`
- `MaterialEvent`
- `EvidenceEvent`
- `GovernanceEvent`

### 3.2 Subtype compatibility
The runner must prove:

- declared subtype allow where root and semantic consequence match the family
- deterministic block where a subtype is attached to the wrong top-level family
- deterministic block where a pack invents a new top-level family
- explicit governance-review routing where a pack blurs dominant family semantics instead of making them explicit

### 3.3 Promotion safety
The runner must emit promotion traces that cover all nine commit classes:

- `note`
- `observation assertion`
- `hypothesis assertion`
- `structure assertion`
- `operation claim`
- `evidence record`
- `compliance assertion`
- `governance decision`
- `advisory output`

The traces must also show the guarded in-force result categories:

- accepted structural state
- accepted observation/occurrence state
- accepted executed intervention consequence
- accepted material state
- compliance fact

---

## 4. Included bounded scenarios

### 4.1 Family coverage scenarios
- field boundary correction
- stand-count scouting
- hail damage incident
- harvest with linked lot creation
- lot split and dispatch
- lab report ingest
- inspection closure and correction

### 4.2 Subtype compatibility cases
- 7 allow cases, one per top-level family
- 2 direct wrong-family block cases
- 1 ambiguous dominant-consequence governance-review case
- 1 invented-top-level-family block case

### 4.3 Promotion safety traces
- note typed only, no shortcut to executed fact
- observation assertion accepted after validation/evidence
- hypothesis assertion stays advisory
- structure assertion accepted only after validation/conflict/review
- operation claim blocked when evidence is missing
- operation claim accepted as executed intervention consequence when evidenced and reviewed
- material operation claim accepted as accepted material state when lineage/custody evidence passes
- evidence record remains support-only
- compliance assertion becomes compliance fact only through policy/evidence/review
- governance decision emits in-force status only when authority and evidence gates pass
- governance decision cannot bypass evidence rules
- advisory output emits warning/review request only

---

## 5. Non-goals

This fixture wave does not yet attempt to close:

- cross-precedence merge legality for conflicting event subtype declarations
- deployment-collected event-ingestion telemetry
- profile compatibility
- alignment-register coverage checking
- graph-pattern equivalence

Those remain separate follow-on conformance seams.
