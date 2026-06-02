# OFARM advisory cohort benchmark view card examples v0.1

Date: 2026-04-15
Status: active supporting implementation artifact
Scope: example user-facing cards for the first-wave benchmark seam

---

## Example 1 — fertilizer product-class benchmark

- Basis: `productclass:fertilizer:npk_15_15_15`
- Window: 2026 Q1
- Metric: average unit price
- Contributor posture: `5-9`
- Headline: `1.129 EUR / kg`
- Quantity band: `MEDIUM`
- Freshness posture: exploratory Advisory view
- Disclosure note: no raw peer rows, no exact contributor count, no peer total spend

## Example 2 — seed exact-product benchmark

- Basis: `product:seed:maize:hybrid_abc_treated_50k`
- Window: 2026 Q1
- Metric: average unit price
- Contributor posture: `5-9`
- Headline: `31.0 EUR / bag:50000seeds`
- Quantity band: `MEDIUM`
- Disclosure note: exact product allowed because normalization and cohort safety both passed

## Example 3 — broadened request

- Requested basis: exact fertilizer product
- Effective basis: governed fertilizer product class
- Outcome: broadened and re-evaluated
- Disclosure note: exact slice was unsafe; broader class was used instead
