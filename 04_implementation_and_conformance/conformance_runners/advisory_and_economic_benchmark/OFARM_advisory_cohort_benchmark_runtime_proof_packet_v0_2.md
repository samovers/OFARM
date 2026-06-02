# OFARM advisory cohort benchmark runtime proof packet v0.2

Date: 2026-04-15
Status: active supporting implementation artifact
Scope: second bounded `04`-only runtime proof tranche for the advisory cohort benchmark seam

---

## 1. Purpose

This packet executes the next tranche after the bounded benchmark pre-implementation gate.

It remains entirely inside `04_implementation_and_conformance/`.
It does **not** patch:

- `00_active_baseline/`
- `01_companion_artifacts/`
- `02_accepted_rfcs/`
- `03_machine_contracts/`
- `06_active_supporting_research/`

---

## 2. Affected active-baseline files

None.

---

## 3. Change type

- implementation/conformance implication

---

## 4. What this tranche adds

### Runtime proof workspace
`04_implementation_and_conformance/spikes_incubation/ofarm_advisory_cohort_benchmark_runtime_spike_v0_2/`

Contains:
- experimental schemas for request-history assessment and benchmark materialization state
- upgraded disclosure-decision schema with freshness and request-history grounding
- positive bundles for:
  - fertilizer product-class allow
  - seed exact-product allow
  - fertilizer exact request broadened to class
  - fertilizer recomputed after contribution revocation
- negative examples for:
  - ambiguous exact normalization
  - raw evidence leakage
  - revoked contribution still marked eligible
  - risky narrowing incorrectly cleared
  - fresh materialization with an invalidation trigger
  - stale materialization still allowed
  - forbidden total-spend metric exposure
- bounded query templates that validate against the active `QuerySpecification` schema
- an illustrative redacted pilot dataset
- view-module examples
- a validation runner and report

### Root-level runtime records
This packet also adds runtime-shaped record sets for:
- request-history decisions
- benchmark materialization freshness/recompute state
- disclosure decisions
- sharing-boundary access decisions

---

## 5. What this tranche proves

1. Request-history differencing control can be expressed explicitly rather than left as a hand-wave.
2. Risky exact-product narrowing can be broadened or blocked before view delivery.
3. Contribution revocation can invalidate prior benchmark materialization for future use.
4. Fresh recompute can produce a new safe benchmark view after revoked contributions are removed.
5. Stale or invalid benchmark materialization can be denied for this view surface rather than silently served.
6. A user-facing benchmark card can remain bounded to `VIEW_MODULE` / `SUMMARY_ROWS` without raw peer leakage.

---

## 6. What this tranche still does not prove

- deployment telemetry for request-history differencing controls
- actual multi-tenant production traffic behavior
- a real tenant-data pilot inside this package
- any reason to promote these contracts into `03_machine_contracts/`
- any reason to change OFARM law

The illustrative pilot dataset is explicit about this:
- `datasetKind = ILLUSTRATIVE_NON_REAL`
- `actualTenantData = false`

---

## 7. Bottom line

This is a tighter executable proof packet than the earlier benchmark spike because it closes the main open runtime seams:
- request-history differencing
- revocation invalidation
- forced recompute before future view use

It is still a bounded `04` packet and should be treated as breakable implementation evidence, not as promoted OFARM law.
