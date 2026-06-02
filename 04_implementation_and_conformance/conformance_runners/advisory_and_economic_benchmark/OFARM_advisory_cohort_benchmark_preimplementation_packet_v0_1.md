# OFARM advisory cohort benchmark pre-implementation packet v0.1

Date: 2026-04-15
Status: active supporting implementation artifact
Scope: bounded `04`-only spike for the advisory cohort benchmark seam after critical evaluation

---

## 1. Purpose

This packet implements the smallest controlled pre-implementation step allowed by the critical evaluation.

It does **not** patch:
- `00_active_baseline/`
- `01_companion_artifacts/`
- `02_accepted_rfcs/`
- `03_machine_contracts/`

It adds only:
- experimental benchmark contracts and examples
- query templates that stay inside the current `QuerySpecification` subset
- hostile fixtures for disclosure and sharing boundaries
- a narrow acceptance gate for the benchmark seam

---

## 2. Affected active-baseline files

None.

---

## 3. Change type

- implementation/conformance implication
- supporting research implication through linked `06` memos

---

## 4. Main additions

### Spike workspace
`04_implementation_and_conformance/spikes_incubation/ofarm_advisory_cohort_benchmark_spike_v0_1/`

Contains:
- experimental schemas
- positive and negative examples
- synthetic benchmark dataset
- query templates
- validation runner and report

### Root-level benchmark fixtures
- benchmark sharing boundary records
- benchmark disclosure decision records
- hostile test matrix
- acceptance gate report

---

## 5. Experimental objects added in `04`

### `ProductNormalizationTrace`
Captures reviewed normalization from receipt-backed line extract to exact product, product class, or refusal.

### `BenchmarkContribution`
A one-row-per-contributor-per-benchmark-window derived object used to keep the first-wave aggregate/query surface inside the current `COUNT` / `SUM` / `MAX` / `AVG` subset.

### `BenchmarkDisclosureDecision`
A deterministic disclosure decision object that separates access control from disclosure safety.

---

## 6. What this packet proves

1. The feature can remain Advisory-only.
2. A two-leg share path can be expressed without reopening authority law.
3. Product normalization can remain explicit and separate from raw extract shape.
4. Disclosure control can be exercised as a runtime decision layer.
5. The current `QuerySpecification` aggregate subset is sufficient when the contribution layer is explicit.

---

## 7. What this packet does not prove yet

- deployment-scale request-history differencing control
- real-farm cohort viability across enough participants
- production-grade revocation recompute behavior
- user-interface ergonomics
- any reason to promote these contracts into `03_machine_contracts/`

---

## 8. Bottom line

This packet is a bounded executable proof step, not a promotion packet. It is designed to be broken, tightened, or cut back without disturbing the active OFARM 2 authority set.
