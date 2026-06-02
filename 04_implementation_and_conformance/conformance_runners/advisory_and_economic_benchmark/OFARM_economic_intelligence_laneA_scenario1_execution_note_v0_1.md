# OFARM economic intelligence Lane A — Scenario 1 execution note v0.1

Date: 2026-04-13
Status: active supporting implementation artifact
Scope: concrete execution note for Lane A (operational-only crop/system ranking) using only Scenario-1-confirmed data

---

## 1. Purpose

Lane A exists to prove that OFARM can support economically meaningful decision support **before accounting closes** and **without pretending to measure profitability**.

This lane is intentionally narrow:
- target twin = Advisory only
- output class = live view or bounded report only
- basis = operational/planning records plus estimate assumptions
- no ledger semantics
- no whole-farm finance claims
- no capex or submission bridge from Scenario 1 alone

---

## 2. Confirmed data basis

This lane may use only the confirmed Scenario 1 style basis:
- crop / candidate crop-system
- field
- hectares
- expected yield
- expected selling price
- working hours by field/activity
- machinery working hours
- fuel consumption and allocation
- seed use per field
- input use per field
- yield per field

No implicit rate tables or accounting actuals are allowed.

---

## 3. What this lane is allowed to answer

Allowed answers are screening-grade only, for example:
- estimated gross revenue per hectare
- estimated gross revenue per labour hour
- estimated gross revenue per machine hour
- estimated gross revenue per fuel litre
- ranked alternatives under a declared bottleneck assumption
- downside/upside revenue range from explicit yield/price bands
- explicit request for additional evidence before stronger economics is attempted

---

## 4. What this lane must refuse

This lane must refuse or downgrade all of the following:
- profit / profitability / net margin / operating margin claims
- gross-margin claims when no variable-cost prices are present
- break-even price or yield claims derived from missing cost basis
- ROI, NPV, IRR, DSCR, payback, or solvency language
- DossierAssembly / SubmissionAssembly preparation from Scenario 1 alone

---

## 5. Lane A execution method

1. Bind candidate field/crop alternatives to operational basis refs.
2. Record explicit estimate assumptions for yield and selling price, including ranges.
3. Declare the controlling bottleneck resource for ranking.
4. Compute only gross-revenue and resource-intensity style screens.
5. Emit a `RANKED_ALTERNATIVES` or `THRESHOLD_SCREEN` result set.
6. Emit a human-gated `BridgeCandidate` only to request more evidence or prepare a bounded internal report.

---

## 6. Required refusal text

Any user-facing result produced from Lane A must contain language equivalent to:

> Screening only. Operational/planning basis plus estimate assumptions. Not a profitability statement.

---

## 7. Deliverables in this lane package

- sample Scenario-1 dataset
- evaluator script
- generated example result set
- generated summary note
- positive scenario/result/bridge examples
- negative profitability-claim example
- updated contract validator with Scenario-1 honesty checks
- validator results

---

## 8. Promotion consequence

Lane A passing does **not** justify RFC promotion.
It only justifies continuing the economics spike at companion + implementation level.
