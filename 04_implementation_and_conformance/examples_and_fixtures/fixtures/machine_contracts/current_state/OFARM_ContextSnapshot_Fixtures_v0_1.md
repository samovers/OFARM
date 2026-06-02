# OFARM ContextSnapshot fixtures v0.1

Date: 2026-04-11  
Status: executable/conformance fixture note  
Scope: starter executable fixtures for Wave 2 context snapshot closure

---

## Purpose

These fixtures make the current-state materialization seam more executable by covering the smallest high-value context-basis cases:
- a resolvable baseline compliance context
- a materially changed context after orchard-pack activation
- fixture-level distinction between same-basis recomputation and true basis drift

They do **not** claim full materialization-runtime closure.
They provide a stable starter set for grounding `MaterializationBasis.contextSnapshotRefs` and freshness decisions.

---

## Executable fixtures in this package

### Fixture 1 — same-basis recomputation
- same `ContextSnapshot` before and after recomputation
- same twin, scope, and evaluation-time policy

Expected:
- relation = `BASIS_PRESERVING_RECOMPUTE`
- no new context snapshot required
- prior freshness remains `FRESH`

### Fixture 2 — basis drift for exploratory use
- orchard-pack activation materially changes active packs, profile posture, governing rule/evidence refs, and merge trace
- use class = exploratory

Expected:
- relation = `BASIS_DRIFT`
- a new context snapshot is required
- prior freshness becomes `STALE`

### Fixture 3 — basis drift for high-consequence use
- same context drift as Fixture 2
- use class = high consequence

Expected:
- relation = `BASIS_DRIFT`
- a new context snapshot is required
- prior freshness becomes `INVALID`

---

## Executable evidence

Machine-contract examples live under:
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/current_state/OFARM_ContextSnapshot_example_*.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/current_state/OFARM_MaterializationBasis_example_field_compliance*.json`

Executable fixture payloads live under:
- `04_implementation_and_conformance/examples_and_fixtures/ofarm_context_snapshot_fixtures_v0_1/`

Executable results are written to:
- `04_implementation_and_conformance/historical_archive/historical_archive/historical/OFARM_context_snapshot_fixture_results_v0_1.json`
