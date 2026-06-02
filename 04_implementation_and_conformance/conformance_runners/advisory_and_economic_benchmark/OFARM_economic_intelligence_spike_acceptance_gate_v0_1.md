# OFARM economic intelligence spike acceptance gate v0.1

Date: 2026-04-13
Status: active supporting implementation artifact
Scope: hard pass/fail gate for the economics spike so the work does not drift into architecture theatre or ERP creep

---

## 1. Gate purpose

This gate exists to decide whether the economics spike:
- remains bounded and worth continuing,
- should be cut back,
- or should be killed.

No RFC or machine-contract promotion is allowed before this gate is passed.

---

## 2. Mandatory pass conditions

All of the following must pass:

1. **No second query model**  
   Scenario objects must not hide alternate retrieval semantics outside QuerySpecification / QueryPlanIR.

2. **No second truth store**  
   Scenario results, cached tables, or dashboards must not behave like authoritative current state.

3. **No ERP creep**  
   Imported finance remains extract-shaped and non-ledger.

4. **No silent bridge**  
   Bridge candidates remain explicitly human-gated and proposal-shaped.

5. **Freshness discipline survives contact with economics**  
   High-consequence outputs recompute or refuse when stale/invalid.

6. **Output taxonomy stays clean**  
   Economics uses ViewModule / ReportAssembly / DossierAssembly / SubmissionAssembly correctly and does not invent an economic passport family.

7. **Scenario-1 honesty**  
   Operational-only economics refuses fake profitability and stays at screening/threshold/constraint level.

8. **Authority/sharing discipline remains intact**  
   Economic outputs do not loosen farm-private defaults or collapse sharing into truth authority.

---

## 3. Automatic cut-back triggers

Cut back immediately if any of the following appear:
- broad manual finance data-entry burden before useful outputs exist,
- imported finance tables behaving like OFARM-owned accounting state,
- advisory results reused as current-state answers,
- a pack or view begins depending on undeclared scenario-only semantics,
- low-friction approval flows that effectively auto-promote economics into harder truth.

---

## 4. Exit outcomes

### PASS
Keep contracts experimental but allow a narrow promotion review.

### PARTIAL PASS
Keep companion guidance active and continue implementation only with a reduced seam.

### FAIL
Kill the current contract seam and fall back to narrower advisory views plus bounded imported fact extracts.
