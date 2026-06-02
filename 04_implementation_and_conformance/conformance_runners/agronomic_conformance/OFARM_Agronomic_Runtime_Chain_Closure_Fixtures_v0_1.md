# OFARM agronomic runtime chain closure fixtures v0.1

Date: 2026-05-13  
Status: active supporting implementation artifact  
Change class: implementation/conformance implication  
Phase: AGR-P8  
Scope: package-local agronomic runtime-chain conformance closure after AGR-P7 baseline harmonisation

---

## 1. Purpose

AGR-P8 closes the remaining AGR-P1 limitation by adding concrete, machine-readable agronomic runtime chains that use the already accepted carrier shells and reconstruction controls from AGR-P2 through AGR-P7.

This artifact does **not** create new baseline law, new accepted RFCs, or new active machine-contract schemas. It proves that the existing agronomic carriers can be assembled into end-to-end chains while preserving OFARM's source-of-truth law.

---

## 2. What this phase closes

Before AGR-P8, the AGR-P1 scenario suite was intentionally classified as `PASS_WITH_LIMITATIONS` because it checked scenario expectations rather than concrete event/assertion/evidence-chain fixture behavior.

AGR-P8 adds chains for:

1. scouting observation to recommendation, prescription, execution claim, accepted partial execution, and output reconstruction
2. soil/measurement evidence to qualified result and output refusal/qualification
3. offline contractor late-sync with unresolved product identity
4. partial failed application, correction, and dispute preservation
5. partial replant with mixed variety and crop-cycle lineage
6. geometry conflict and late correction under stale current-state pressure
7. wet grain or storage-condition measurement pressure as a measurement/materialization chain
8. schema/profile/query drift regression using code-binding and reconstruction policy

---

## 3. Required preservation rules

Every runtime chain must prove that:

- recommendation is not prescription
- prescription is not execution
- operation claim is not accepted execution
- machine log is not compliance truth by itself
- partial extent is not whole-field truth
- disputed geometry is not silently collapsed
- unresolved product or code identity cannot support high-consequence compliance output
- stale current state cannot drive high-consequence output without recompute, refusal, or review
- DocumentAssembly can preserve annexes and disputed evidence without mutating the accepted source history

---

## 4. Evidence artifacts

Machine-readable records and runner:

- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_agronomic_runtime_chain_records_v0_1.json`
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/ofarm_agronomic_runtime_chain_runner_v0_1.py`
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_agronomic_runtime_chain_results_v0_1.json`

The runner checks upstream phase results, scenario coverage, artifact references, chain step ordering, required carrier use, promotion/materialization/output behavior, and negative checks.

---

## 5. Boundary

AGR-P8 is package-local conformance closure. It is not:

- live pilot evidence
- wire-level ISOXML/EFDI/ADAPT mapping freeze
- jurisdiction-specific product registry verification
- production runtime implementation
- new baseline law

Those remain future work triggered by real implementation evidence.
