# OFARM economic intelligence spike design notes v0.2

Date: 2026-04-13
Status: active supporting implementation artifact
Scope: define the first executable spike packet for the bounded native economics amendment without reopening OFARM architecture or drifting into ERP semantics

---

## 1. Purpose

This spike exists to answer one practical question:

**Can OFARM host a native Advisory-Twin economic-intelligence workspace over the same substrate, with explicit basis and refusal behavior, without creating a second truth store or shadow ERP?**

The active baseline already answers the broad architecture question:
- one semantic substrate,
- two logical twins,
- governed current-state materialization,
- no direct authoritative writes into projections or report stores,
- no Advisory-to-Compliance mutation without a governed bridge.

So this spike is not architecture exploration.
It is implementation proof.

---

## 2. Spike boundaries

### 2.1 In scope
- Advisory-only scenario specifications
- bounded imported fact extracts for economic use
- explicit economic evidence classes
- allocation-basis declaration and refusal behavior
- view/report/dossier output shaping
- bridge-candidate generation with human-gated follow-up only
- schema/example validation for the candidate scenario seam

### 2.2 Out of scope
- general ledger behavior
- AP/AR
- payroll workflow
- tax/VAT logic
- bank reconciliation
- procurement workflow
- statutory financial reporting
- inventory valuation close semantics
- any direct Compliance-Twin mutation path

---

## 3. Three vertical slices

### 3.1 Slice A — Scenario 1 crop/system ranking under operational-only data
Goal:
- prove OFARM can deliver useful screening with only operational/planning data
- prove the workspace refuses fake profitability claims when finance basis is too weak

Expected outputs:
- live scenario comparison view
- threshold screen result set
- optional draft report assembly

Hard rule:
- no net-profit claim
- no hidden fixed-cost allocation

### 3.2 Slice B — Scenario 2 own-versus-contractor decision
Goal:
- prove partial-finance inputs can be used conservatively through imported fact extracts and explicit rate-card assumptions

Expected outputs:
- contractor-versus-own comparison view
- frozen ReportAssembly for operational decision support
- explicit AllocationBasisDeclaration where shared machinery or labor cost is allocated

Hard rule:
- partial accounting input must not be presented as ledger truth

### 3.3 Slice C — Scenario 3 capex pre-gate dossier
Goal:
- prove OFARM can support pre-gate screening for a post-harvest line without pretending to perform a full investment appraisal

Expected outputs:
- capacity and utilization screen
- downside sensitivity set
- DossierAssembly for a capex pre-gate packet
- BridgeCandidate to request fuller external appraisal or additional evidence

Hard rule:
- no full NPV/IRR/financing-grade claim unless external appraisal input is complete and explicitly routed as such

---

## 4. Candidate contract seam exercised in this spike

The spike exercises four candidate contracts only:
- `AdvisoryScenarioSpec`
- `ImportedFactExtract`
- `AdvisoryScenarioResultSet`
- `BridgeCandidate`

These contracts remain in implementation/conformance only.
They are not active RFC law and they are not active machine contracts.

---

## 5. Execution packet contents

The packet for this spike should contain:
- package index
- candidate contract note
- four JSON schemas
- example instances for slices A/B/C
- validation runner
- conformance seed additions focused on economics
- a hostile checkpoint list

---

## 6. Success criteria

The spike succeeds only if all of these are true:
- scenario specs do not become a second query language
- imported finance remains extract-shaped and non-ledger
- scenario results are clearly advisory and never mistaken for current state
- bridge candidates remain human-gated
- stale or insufficient high-consequence outputs recompute or refuse
- output taxonomy remains clean: view vs report vs dossier vs submission
- no second truth store appears in projections or cached scenario tables

---

## 7. Failure conditions

Kill or cut back the seam if the spike reveals any of the following:
- hidden query semantics inside scenario objects
- fake-current-state materialization for economics
- connector-fed finance tables behaving like OFARM-owned accounting truth
- “economic passport” family drift
- approval shortcuts that let scenario results silently harden into truth

---

## 8. Exit rule

Promotion beyond implementation/conformance is earned only if the spike proves:
- stable seam shape,
- hostile-review survival,
- conformance usefulness,
- and no ERP creep.

Until then the right posture remains:
- companion clarification active,
- contracts experimental,
- implementation hostile.
