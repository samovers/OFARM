# OFARM Lot Traceability fixtures v0.1

Date: 2026-04-11  
Status: executable/conformance fixture note  
Scope: starter executable fixtures for Wave 1 lot traceability and claim-basis closure

---

## Purpose

These fixtures make the lot seam more executable by covering the smallest high-value red-flag cases:
- split into distinct successor lots
- merge / commingling into a new successor lot
- transformation into a new successor lot
- shipment-reference continuity without false new-lot creation
- claim-basis reset with visible lineage consequences

They do **not** claim full end-to-end traceability closure.
They provide a stable starter set for contract validation and narrow semantic fixture checks.

---

## Executable fixtures in this package

### Fixture 1 — split
Expected:
- `changeType = SPLIT`
- `continuityOutcome = NEW_LOT_REQUIRED`
- one predecessor lot
- two or more successor lots
- successor lineage relation = `splitFrom`

### Fixture 2 — merge / commingle
Expected:
- `changeType = COMMINGLE`
- `continuityOutcome = NEW_LOT_REQUIRED`
- two or more predecessor lots
- one successor lot
- successor lineage relation = `mergedFrom`
- post-change claim basis is explicit

### Fixture 3 — transform
Expected:
- `changeType = TRANSFORM`
- `continuityOutcome = NEW_LOT_REQUIRED`
- predecessor/successor relation = `derivedFrom`

### Fixture 4 — shipment-reference continuity
Expected:
- `changeType = SHIPMENT_REFERENCE_ATTACH`
- `continuityOutcome = SAME_LOT_CONTINUES`
- shipment references attached without false new-lot creation

### Fixture 5 — claim-basis reset
Expected:
- `changeType = CLAIM_BASIS_RESET`
- `continuityOutcome = NEW_LOT_REQUIRED`
- pre/post claim basis refs differ
- successor lineage relation = `derivedFrom`

---

## Executable evidence

Schema validation results live in:
- `04_implementation_and_conformance/service_and_sdk_candidates/reference_platform_and_sdk/OFARM_machine_contract_validation_results_v0_3.json`

Lot fixture semantic checks live in:
- `04_implementation_and_conformance/historical_archive/historical_archive/historical/OFARM_lot_traceability_fixture_results_v0_1.json`
