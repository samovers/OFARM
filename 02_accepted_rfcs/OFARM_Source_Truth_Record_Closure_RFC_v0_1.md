# OFARM Source Truth Record Closure RFC v0.1

Date: 2026-04-17  
Status: accepted post-charter RFC  
Scope: close the machine-contract seam for source truth records already required by RC2.1 and the Current State Materialization RFC

---

## 1. Problem statement

RC2.1 and the current-state materialization closure already depend on:
- `AssertionRecord`
- `ReviewDecision`
- `AcceptedEventConsequence`

That is constitutionally sound.
It is not yet machine-closed inside the active contract set.

Today:
- `MaterializationBasis` points to these records by identifier
- `EvidenceSufficiencyCase` may point to them by identifier
- current examples rely on them
- the active machine layer does not yet define the records themselves

This RFC closes that seam with the smallest controlled patch.

---

## 2. Core stance

### 2.1 Thin closure, not new architecture
This RFC does not create a second truth layer.
It only gives first-class machine contracts to source truth records that are already required by the active baseline.

### 2.2 Assertion/history-first remains intact
Canonical truth remains assertion/history-first.
Current state, compiled outputs, and authorization traces remain downstream governed derivatives.

### 2.3 Minimum fields only
The contracts created here must carry only the minimum machine-verifiable fields needed for:
- identity
- subject and scope
- actor lineage where relevant
- time semantics
- evidence/provenance linkage
- in-force / review / supersession state

This RFC does **not** create a giant provenance ontology blob.

---

## 3. New contract families created by this RFC

This RFC creates these active machine-contract families in `03_machine_contracts/`:
- `OFARM_AssertionRecord_schema_v0_1.json`
- `OFARM_ReviewDecision_schema_v0_1.json`
- `OFARM_AcceptedEventConsequence_schema_v0_1.json`

---

## 4. Contract minimums

### 4.1 AssertionRecord minimums
An `AssertionRecord` contract must be able to carry at least:
- stable record identifier
- assertion type
- subject reference
- anchor scope
- asserting party
- assertion time
- evidence references
- provenance references where retained
- governed claim state
- supersession lineage where relevant

### 4.2 ReviewDecision minimums
A `ReviewDecision` contract must be able to carry at least:
- stable decision identifier
- reviewed artifact family and target reference
- review action and outcome state
- deciding party
- decision time
- anchor scope
- resulting accepted-consequence references where relevant
- supersession lineage where relevant

### 4.3 AcceptedEventConsequence minimums
An `AcceptedEventConsequence` contract must be able to carry at least:
- stable consequence identifier
- source event reference
- accepting review-decision reference
- subject reference
- anchor scope
- accepted/effective time
- in-force state
- supersession lineage where relevant

---

## 5. Compatibility rule

Existing `MaterializationBasis` and `EvidenceSufficiencyCase` contracts remain valid.
This RFC does not require them to embed the full source records.
It requires only that current package examples may now point to governed package-local source records rather than leaving those identifiers unresolved.

---

## 6. Out of scope

This RFC does not:
- redesign event grammar
- redesign review law
- standardize every future event subtype
- require that every assertion family get a dedicated subtype contract in this wave

---

## 7. Outcome

After this RFC:
- `MaterializationBasis` references can land on governed objects
- evidence and output cases can point to governed source truth records
- audit reconstruction can cross the source-record seam without manual reinterpretation of bare identifiers
