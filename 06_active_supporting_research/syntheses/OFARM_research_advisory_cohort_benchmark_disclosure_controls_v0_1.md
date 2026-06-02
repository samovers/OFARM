# OFARM research — advisory cohort benchmark disclosure controls v0.1

Date: 2026-04-15
Status: active supporting research
Scope: first-wave disclosure-control policy shape for the advisory cohort benchmark seam

---

## 1. Purpose

This memo defines the smallest deterministic disclosure-control posture that can be exercised in `04_implementation_and_conformance/` without reopening the active authority set.

Authority answers **who may access**.
Disclosure control answers **whether the accessed benchmark is safe to show**.

---

## 2. First-wave decision model

A benchmark request should end in exactly one of these outcomes:
- `ALLOW`
- `BROADEN`
- `SUPPRESS`
- `REFUSE`

### ALLOW
Show the benchmark as requested.

### BROADEN
Requested exact product is unsafe; broaden to governed product class and re-evaluate.

### SUPPRESS
The benchmark exists but must not be shown because of cohort size, dominance, or differencing risk.

### REFUSE
The request cannot produce a comparable benchmark because normalization/comparability failed.

---

## 3. Recommended first-wave thresholds

These are research/prototype thresholds, not active baseline law.

- minimum distinct contributors: **5**
- contributor-count display posture: **hidden or banded only**
- dominance threshold: **0.35** of total contribution amount for the selected benchmark window
- differencing guard: block any narrower request whose source cohort differs from a previously allowed cohort by fewer than **2** contributors within the same product/window family

These thresholds should be treated as starting points for spike validation, not as already-promoted law.

---

## 4. Safe filter whitelist

Wave 1 should allow only the following benchmark filters:
- benchmark window
- governed product class
- exact normalized product only when safe
- normalized currency
- normalized unit
- explicit participant farm set resolved before query execution

Wave 1 should avoid user-driven free combination of many dimensions.

Out of scope for wave 1:
- ad hoc geography slicing beyond pre-resolved participant sets
- free-form crop/field/season dimension stacking
- customer-specific pivoting
- historical repeated narrowing workflows without request-history guardrails

---

## 5. User-visible metrics allowed

Allowed:
- average unit price
- quantity band
- optional position band

Disallowed:
- total peer spend
- exact contributor counts
- min/max spend or min/max unit price
- percentiles/distributions
- spend-per-hectare

---

## 6. Required decision reasons

The spike should exercise reason codes such as:
- `BENCHMARK_INSUFFICIENT_COHORT`
- `BENCHMARK_DOMINANCE_RISK`
- `BENCHMARK_DIFFERENCING_RISK`
- `BENCHMARK_PRODUCT_BROADENED_TO_CLASS`
- `BENCHMARK_PRODUCT_AMBIGUOUS`
- `BENCHMARK_NONCOMPARABLE_UNIT`
- `BENCHMARK_NONCOMPARABLE_CURRENCY`
- `BENCHMARK_CONTRIBUTION_REVOKED`

---

## 7. Display rules

The user-facing view should always display:
- product or product-class basis
- benchmark window
- evidence posture
- freshness posture
- contributor-count band or hidden posture
- any fallback/broadening decision
- any suppression/refusal explanation

The user-facing view should never display:
- peer line items
- peer evidence refs
- peer raw amounts by contributor
- exact contributor counts in wave 1

---

## 8. Bottom line

The seam is only credible if disclosure safety becomes an explicit runtime decision layer rather than an informal promise that data is “anonymized.”
