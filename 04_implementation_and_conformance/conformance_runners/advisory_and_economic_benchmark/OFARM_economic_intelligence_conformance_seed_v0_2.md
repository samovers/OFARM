# OFARM economic intelligence conformance seed v0.2

Date: 2026-04-13
Status: active supporting implementation artifact
Scope: first executable and design fixtures for the bounded economic-intelligence spike packet

---

## 1. Purpose

This seed set is intentionally narrow.
It exists to test the failure-prone seams introduced by native Advisory economics:
- evidence-class honesty,
- imported-fact conservatism,
- allocation visibility,
- stale/insufficient refusal,
- bridge safety,
- and output-family correctness.

It is not a full economics conformance program.

---

## 2. Executable fixtures in this packet

### 2.1 Schema validation
Validate these candidate contracts:
- `AdvisoryScenarioSpec`
- `ImportedFactExtract`
- `AdvisoryScenarioResultSet`
- `BridgeCandidate`

### 2.2 Positive examples
- Scenario 1 crop-system ranking example
- Scenario 2 own-versus-contractor example
- Scenario 3 capex pre-gate example
- contractor-rate extract example
- settlement-summary extract example
- capex-screen result-set example
- dossier-preparation bridge candidate example

### 2.3 Negative examples
- ScenarioSpec with non-Advisory target twin must fail
- ImportedFactExtract with ledger-like mutation field must fail
- ResultSet without basis trace refs must fail
- BridgeCandidate without human approval on dossier-prep path must fail

---

## 3. Design fixtures still prose-first

These remain design-level until the runtime spike deepens:
- hidden fixed-cost allocation attempt on field profitability
- stale scenario reused for high-consequence lender packet
- attempted direct Advisory-to-Compliance mutation
- attempted relabeling of a scenario packet as PassportView
- imported accounting payload treated as editable ledger master

---

## 4. Minimum questions every economics fixture must answer

For any test case, the system must be able to say:
- what was observed operationally,
- what was imported externally,
- what was assumed,
- what was benchmarked,
- what was allocated,
- what was merely advisory,
- and what was blocked from becoming harder truth.

---

## 5. Exit criterion

This seed is useful only if it makes later implementations fail deterministically when they drift toward:
- benchmark-as-truth,
- allocation-as-observation,
- dashboard-as-authority,
- connector-as-ledger,
- scenario-as-current-state.
