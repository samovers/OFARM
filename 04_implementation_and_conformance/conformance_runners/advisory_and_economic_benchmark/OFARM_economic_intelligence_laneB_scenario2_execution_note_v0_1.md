# OFARM economic intelligence Lane B — Scenario 2 execution note v0.1

Date: 2026-04-13
Status: active supporting implementation artifact
Scope: concrete execution note for Lane B (own-vs-contractor and bottleneck economics) using Scenario-2-style partial finance

---

## 1. Purpose

Lane B exists to prove that OFARM can support a **bounded operational-economic decision** when some finance arrives, while still refusing to behave like ERP or fake field-profitability accounting.

This lane is intentionally narrow:
- target twin = Advisory only
- output class = live view or bounded internal report only
- basis = operational/planning records + partial finance extracts + explicit benchmark assumptions
- decision type = own-versus-contractor under a declared timing bottleneck
- no ledger semantics
- no whole-farm finance claims
- no dossier/submission bridge from this lane

---

## 2. Minimum data basis

Lane B may use:
- Scenario-1 operational/planning basis
- contractor/service rate extracts
- recent input-price snippets where available
- explicit benchmark rate assumptions where actual rates are missing

This lane still does **not** justify:
- full field profitability
- whole-farm operating margin
- debt-service logic
- statutory accounting semantics

---

## 3. What this lane is allowed to answer

Allowed answers are decision-support screens such as:
- direct execution outlay comparison
- timely-capacity coverage comparison
- untimely-area exposure screen from an explicit penalty assumption
- recommendation on whether paying more direct cost protects the bottleneck sufficiently
- bounded internal report preparation for human review

---

## 4. What this lane must refuse

This lane must refuse or downgrade all of the following:
- field profit / field profitability / operating margin claims
- hidden fixed-cost allocation through blended internal rates with no basis
- ledger/current-state language for imported extracts
- DossierAssembly / SubmissionAssembly preparation
- solvency, DSCR, NPV, IRR, or payback claims

---

## 5. Lane B execution method

1. Bind the operational basis for the target operation and area.
2. Import only bounded finance extracts needed for the immediate decision.
3. Declare benchmark assumptions separately from imported facts.
4. Compute direct execution outlay for each option.
5. Compute timely-capacity coverage for each option under the declared bottleneck window.
6. Compute untimely-area exposure only through an explicit risk assumption.
7. Emit a `CAPACITY_SCREEN` result set.
8. Emit a human-gated `BridgeCandidate` only for a bounded internal report.

---

## 6. Required refusal text

Any user-facing result produced from Lane B must contain language equivalent to:

> Decision support only. Partial finance plus benchmark assumptions. Not ledger truth. Not a profitability statement.

---

## 7. Deliverables in this lane package

- sample Scenario-2 own-versus-contractor dataset
- evaluator script
- generated example result set
- generated summary note
- positive capacity-screening contract examples
- negative field-profitability example
- updated contract validator with Lane-B honesty checks
- validator results

---

## 8. Promotion consequence

Lane B passing does **not** justify RFC promotion.
It only justifies continuing the economics spike into Lane C.
