# OFARM advisory cohort benchmark view module examples v0.3

Date: 2026-04-15
Status: active supporting implementation artifact
Scope: example user-facing benchmark cards and refusal states for the real-pilot handoff packet

---

## Example 1 — fertilizer product-class benchmark card

- View module ref: `viewmodule:advisory-cohort-benchmark-fertilizerclass-v0.3`
- Basis: `productclass:fertilizer:npk_15_15_15`
- Window: 2026 Q1
- Headline: `1.134 EUR / kg`
- Quantity band: `HIGH`
- Contributor posture: `5-9`
- Freshness posture: `FRESH`
- Disclosure note: no raw peer rows, no exact contributor count, no peer total spend, no raw evidence

## Example 2 — seed exact-product benchmark card

- View module ref: `viewmodule:advisory-cohort-benchmark-seedexact-v0.3`
- Basis: `product:seed:maize:hybrid_abc_treated_50k`
- Window: 2026 Q1
- Headline: `31.01 EUR / bag:50000seeds`
- Quantity band: `MEDIUM`
- Contributor posture: `5-9`
- Freshness posture: `FRESH`
- Disclosure note: exact product remains allowed only because normalization, cohort size, dominance, and request history all pass

## Example 3 — broadened fertilizer request

- Requested basis: `product:fertilizer:brandx_npk151515_25kg`
- Effective basis: `productclass:fertilizer:npk_15_15_15`
- Outcome: `BROADEN`
- Disclosure note: long-horizon slice safety did not permit the exact slice; broader product class was served instead

## Example 4 — blocked long-horizon narrowing

- Requested basis: `product:fertilizer:brandx_npk151515_25kg`
- Outcome: `REFUSE`
- Reason: `REQUEST_HISTORY_BLOCKED, DIFFERENCING_RISK_HIGH`
- Disclosure note: no fallback was served because the request pattern remained unsafe at the requested horizon

## Example 5 — pre-recompute refusal

- Requested basis: `productclass:fertilizer:npk_15_15_15`
- Initial state: `INVALID`
- Reason: contribution revoked after an earlier materialization and recompute is still required
- Outcome: view withheld until recompute completes

## Example 6 — post-recompute fresh allow

- Requested basis: `productclass:fertilizer:npk_15_15_15`
- Materialization: recomputed fresh view after contribution revocation
- Headline: `1.139 EUR / kg`
- Contributor posture: `5-9`
- Freshness posture: `FRESH`
