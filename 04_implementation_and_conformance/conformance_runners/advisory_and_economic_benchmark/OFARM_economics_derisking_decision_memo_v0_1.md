# OFARM economics de-risking decision memo v0.1

Date: 2026-04-12  
Status: implementation/conformance decision memo  
Scope: record the decision to cut back the first economics promotion wave after hostile review

---

## 1. Decision

The first economics promotion wave was directionally right but **too aggressive in promotion posture**.

Therefore this de-risked wave makes the following explicit decision:

### Keep as candidate companion-artifact material
- Advisory Scenario Workspace and Bridge Note
- Economic Intelligence Pack Note
- Advisory Scenario and Economic Output Taxonomy Addendum

### Demote out of active-substance promotion
- Advisory Scenario Contracts RFC candidate
- economics machine contracts and examples

Those items now remain only in `04_implementation_and_conformance/` as candidate implementation contracts until spike evidence proves they deserve RFC and machine-contract promotion.

---

## 2. Why the first wave was too aggressive

The first wave promoted:
- one candidate RFC into `02_accepted_rfcs/`
- one candidate schema set into `03_machine_contracts/`

That was too strong because:
- the readiness posture says the honest next move is implementation-scale work plus deeper conformance,
- the contracts had not yet survived spike evidence,
- and accepted-RFC / active-machine-contract placement would implicitly make them active substance.

For this topic, that is too much too early.

---

## 3. What remains true

The underlying architecture decision is unchanged:
- economics belongs natively in Advisory,
- operations remain authoritative substrate,
- ERP/accounting semantics stay out,
- bridge behavior stays human-gated and governed,
- and output taxonomy must block “economic passport” drift.

What changed is only the **promotion level**.

---

## 4. Promotion rule adopted here

Nothing in this wave may move into:
- `02_accepted_rfcs/`
- or `03_machine_contracts/`

until the spike proves all of the following:
- no second query model appears,
- no fake-current-state drift appears,
- ImportedFactExtract stays non-ledger,
- BridgeCandidate remains human-gated,
- stale high-consequence refusal works,
- output taxonomy stays clean.

---

## 5. Immediate consequence

The right next move is:
- keep companion-level clarification narrow,
- keep contracts experimental,
- intensify spike + conformance,
- and only then decide whether RFC/machine-contract promotion is earned.
