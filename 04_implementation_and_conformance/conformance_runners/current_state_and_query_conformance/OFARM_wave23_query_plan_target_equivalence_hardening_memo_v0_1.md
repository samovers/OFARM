# OFARM Wave 23 query-plan target-equivalence hardening memo v0.1

Date: 2026-04-12  
Status: active supporting implementation artifact  
Scope: bounded conformance hardening for cross-target QueryPlanIR semantic equivalence

---

## Purpose

This wave closes the remaining direct query-planner seam that stayed open after graph-pattern equivalence.

The package already had:
- QuerySpecification and QueryPlanIR schema validation
- alias-governance starter fixtures
- internal graph-pattern equivalence canonicalization

What was still missing was runtime-backed proof that semantically identical queries preserve their meaning after target-specific plan shaping across:
- `CURRENT_STATE_MATERIALIZATION`
- `READ_MODEL`
- `SEARCH_INDEX`
- `SEMANTIC_GRAPH`

This wave adds that proof without changing OFARM law, accepted RFCs, companion policy, or machine-contract substance.

---

## Delivered in this wave

- bounded runtime-shaped cross-target query-plan equivalence fixtures
- target-plan compilation into canonical semantics fingerprints
- per-target execution/result digests over a shared bounded data model
- explicit blocked paths for:
  - freshness-insufficient targets on compliance queries
  - semantic-drift targets that silently drop a required filter
- matrix and seed-set updates that move the row from `PARTIAL` to `COVERED`

---

## Important limit

This wave does **not** claim live deployment-produced query execution telemetry.
It closes the conformance seam at bounded runtime-runner level, not at field deployment telemetry level.
