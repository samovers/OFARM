# OFARM economic intelligence real-farm pilot data contract v0.1

## Core rule

The pilot must not assume more data than the farm actually has.
The intake contract is structured so each lane can run only when its own basis is present.

## Top-level fields

- `datasetId`
- `datasetKind`
- `farmIdentityMode`
- `provenance`
- `scenarioMaturity`
- `laneA`
- `laneB`
- `laneC`

## Lane A minimum

Lane A is operational-only. It requires:
- crop/system alternatives
- area
- expected yield range
- expected selling price range
- labour hours/ha
- machine hours/ha
- fuel litres/ha
- quantity index / input intensity proxy
- basis refs

Lane A must **not** request full accounting, fixed-cost allocations, or profitability claims.

## Lane B minimum

Lane B requires Lane A-style operational basis for one operation plus:
- contractor rate extract ref
- mobilization cost
- fuel price input
- labour rate input (benchmark or actual)
- timing penalty assumption
- bottleneck window assumptions

Lane B is a bounded decision screen. It is not field profitability.

## Lane C minimum

Lane C requires:
- candidate asset capacity and indicative capex
- base and downside throughput basis
- quality-fit shares
- committed outlet share
- current vs candidate process loss
- working-capital days assumption
- thresholds for utilization/quality-fit
- imported extract refs
- operational refs
- context and materialization refs

Lane C is strictly pre-gate screening. It is not full appraisal.

## Prohibited data requests

Do not request from the farm unless later explicitly justified:
- full general ledger export
- AP/AR subledger dumps
- payroll detail rows with personal data
- tax/VAT calculation detail
- bank reconciliation detail
- procurement workflow detail
- inventory valuation accounting detail

## Evidence posture

Each money-bearing or threshold-bearing input should be classed as one of:
- `ACTUAL_POSTED`
- `ACTUAL_PRELIMINARY`
- `ESTIMATE`
- `BENCHMARK`
- `PROXY`

The pilot runner does not turn any of these into canonical financial truth.
