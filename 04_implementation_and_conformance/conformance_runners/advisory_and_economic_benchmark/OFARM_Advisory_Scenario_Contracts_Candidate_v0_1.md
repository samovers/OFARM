# OFARM Advisory Scenario Contracts Candidate v0.1

Date: 2026-04-19  
Status: implementation candidate; narrow BridgeCandidate handoff promoted separately  
Scope: hold the remaining reusable machine-contract seam for native Advisory-Twin scenario work after the narrow BridgeCandidate handoff was promoted separately into the active contract set

---

## 1. Why this document is in implementation/conformance, not RFC

The scenario seam is promising.
The promotion evidence is still insufficient.

Therefore the remaining scenario-workspace contracts stay **candidate contracts** only.
`BridgeCandidate` has now been promoted separately as an active contract through `02_accepted_rfcs/OFARM_BridgeCandidate_Closure_RFC_v0_1.md` and `03_machine_contracts/schemas/interoperability/OFARM_BridgeCandidate_schema_v0_1.json`.
The rest are here to be exercised, broken, tightened, and either promoted later or killed if they drift toward:
- hidden query semantics,
- shadow-ERP inputs,
- fake current state,
- or soft autopilot bridge behavior.

---

## 2. Candidate object set

The current remaining candidate object set is:
- `AdvisoryScenarioSpec`
- `ImportedFactExtract`
- `AdvisoryScenarioResultSet`

The experimental `BridgeCandidate` lineage material is preserved under:
- `experimental_machine_contracts/`

But the narrow active handoff contract now lives in:
- `03_machine_contracts/schemas/interoperability/OFARM_BridgeCandidate_schema_v0_1.json`

---

## 3. Non-negotiable candidate constraints

1. `AdvisoryScenarioSpec.targetTwin` remains Advisory-only.
2. `AdvisoryScenarioSpec` may reference basis/query objects but may not become a second query language.
3. `ImportedFactExtract` stays non-ledger and extract-shaped.
4. `AdvisoryScenarioResultSet` is never a CurrentStateMaterialization.
5. Any remaining scenario-workspace object must respect the now-active BridgeCandidate posture: proposal-shaped, human-gated, and non-authoritative by default.
6. None of these contracts may mutate Compliance state directly.

---

## 4. Promotion test

The remaining candidate set should not move to RFC or machine-contract active status until the spike proves:
- schema usefulness,
- implementation stability,
- refusal behavior,
- and anti-ERP boundaries under realistic use.
