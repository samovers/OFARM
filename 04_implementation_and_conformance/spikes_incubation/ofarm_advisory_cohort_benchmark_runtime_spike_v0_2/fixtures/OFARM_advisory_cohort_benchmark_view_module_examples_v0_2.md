# OFARM advisory cohort benchmark view module examples v0.2

Date: 2026-04-15
Status: active supporting implementation artifact
Scope: example user-facing benchmark cards for the runtime proof packet

---

## Example 1 — fertilizer product-class benchmark card

- View module ref: `viewmodule:advisory-cohort-benchmark-fertilizerclass-v0.2`
- Basis: `productclass:fertilizer:npk_15_15_15`
- Window: 2026 Q1
- Headline: `1.135 EUR / kg`
- Quantity band: `HIGH`
- Contributor posture: `5-9`
- Freshness posture: `FRESH`
- Disclosure note: no raw peer rows, no exact contributor count, no peer total spend, no raw evidence

## Example 2 — seed exact-product benchmark card

- View module ref: `viewmodule:advisory-cohort-benchmark-seedexact-v0.2`
- Basis: `product:seed:maize:hybrid_abc_treated_50k`
- Window: 2026 Q1
- Headline: `31.0 EUR / bag:50000seeds`
- Quantity band: `MEDIUM`
- Contributor posture: `5-9`
- Freshness posture: `FRESH`
- Disclosure note: exact product allowed because normalization, cohort size, dominance, and request history all passed

## Example 3 — broadened fertilizer request

- Requested basis: `product:fertilizer:brandx_npk151515_25kg`
- Effective basis: `productclass:fertilizer:npk_15_15_15`
- Outcome: `BROADEN`
- Disclosure note: request-history and slice-safety posture did not permit the exact slice; broader product class was served instead

## Example 4 — recompute required

- Requested basis: `productclass:fertilizer:npk_15_15_15`
- Initial state: `UNAVAILABLE_RECOMPUTE_REQUIRED`
- Reason: contribution revoked after earlier materialization
- Outcome: view withheld until recompute completes
