# OFARM Local Knowledge and Planning Closure RFC v0.1

Date: 2026-04-18  
Status: accepted post-charter RFC  
Scope: close the machine-contract seam for OFARM-owned local knowledge and planned intervention constructs already named by the harmonized Alignment Register

---

## 1. Problem statement

The active baseline and the harmonized Alignment Register already require OFARM to preserve:
- `NarrativeObservation`
- `LocalMemoryRule`
- `LocalArtifact`
- `PlannedIntervention`

That direction is correct.
The active machine layer still lacks first-class contract families for these records.

Today:
- the package can describe claims, accepted consequences, and frozen outputs
- the package can mention local agronomic knowledge in prose and conformance fixtures
- the package cannot yet carry these OFARM-owned constructs as governed machine objects inside the active contract set

This RFC closes that seam with the smallest controlled patch.

---

## 2. Core stance

### 2.1 Thin closure, not a second farm-knowledge stack
This RFC does not create a separate local-knowledge platform inside OFARM.
It only adds first-class machine contracts for a bounded set of OFARM-owned constructs already named by active law.

### 2.2 Rich human knowledge remains explicit
Narrative farmer knowledge must remain preservable without flattening everything into scalar measurements.
This closure therefore preserves rich narrative content, local support artifacts, and locally remembered rules as first-class inputs to planning.

### 2.3 Planning remains distinct from execution truth
`PlannedIntervention` remains a plan object.
It does not silently become execution truth, an operation claim, or an accepted consequence.

### 2.4 Minimum fields only
The contracts created here must carry only the minimum machine-verifiable fields needed for:
- identity
- actor and scope
- time semantics
- local supporting artifact linkage
- planning rationale linkage
- plan/rule/observation state

This RFC does **not** create a giant agronomic notebook ontology.

---

## 3. New contract families created by this RFC

This RFC creates these active machine-contract families in `03_machine_contracts/`:
- `OFARM_LocalArtifact_schema_v0_1.json`
- `OFARM_NarrativeObservation_schema_v0_1.json`
- `OFARM_LocalMemoryRule_schema_v0_1.json`
- `OFARM_PlannedIntervention_schema_v0_1.json`

---

## 4. Contract minimums

### 4.1 LocalArtifact minimums
A `LocalArtifact` contract must be able to carry at least:
- stable artifact identifier
- artifact kind
- holding party
- creation time
- target scope
- storage/redaction posture
- short title or provenance note

### 4.2 NarrativeObservation minimums
A `NarrativeObservation` contract must be able to carry at least:
- stable observation identifier
- observer party
- observed time
- target scope
- rich narrative content
- observation state
- supporting local artifact references where retained

### 4.3 LocalMemoryRule minimums
A `LocalMemoryRule` contract must be able to carry at least:
- stable rule identifier
- author party
- authored or validity time
- target scope
- rule statement
- rule state
- supporting narrative/local artifact references where retained
- optional recommended action or trigger condition

### 4.4 PlannedIntervention minimums
A `PlannedIntervention` contract must be able to carry at least:
- stable planned-intervention identifier
- planning party
- planning time
- target scope
- intended intervention kind
- intended execution window
- plan state
- rationale references to narrative observations and/or local memory rules where retained

---

## 5. Compatibility rule

This RFC does not change truth law.
`PlannedIntervention` remains distinct from:
- `OperationClaim`
- `ReviewDecision`
- `AcceptedEventConsequence`
- frozen dossiers or submission assemblies

The package may now point runtime and conformance fixtures to governed package-local planning and local-knowledge objects rather than leaving them as prose-only seams.

---

## 6. Out of scope

This RFC does not:
- standardize every future advisory object
- replace external observation standards where OFARM already profiles them
- create a full execution-intervention subtype family in this wave
- turn local memory into automatic compliance truth

---

## 7. Outcome

After this RFC:
- OFARM can preserve rich human observation and local supporting artifacts as governed machine objects
- local farm heuristics can remain explicit instead of disappearing into notes
- dispute and planning fixtures can point to a governed `PlannedIntervention` object rather than a prose-only placeholder
