# OFARM advisory cohort benchmark rehearsal summary v0.3

Dataset: **ofarm.benchmarkpilot.rehearsal.v0.3**

Dataset kind: **REDACTED_REHEARSAL_NON_REAL**

**Warning:** redacted rehearsal non-real dataset. Handoff proof only.

## req-fertilizer-class-q1

- Decision: **ALLOW**
- Effective kind: **PRODUCT_CLASS**
- Basis: `productclass:fertilizer:npk_15_15_15`
- Contributors shown as: **5-9**
- Freshness: **FRESH**
- AVG_UNIT_PRICE: **1.134 EUR / kg**
- QUANTITY_BAND: **HIGH**
- Output boundary: no raw peer rows, no raw evidence, no exact contributor count, no peer total spend

## req-seed-exact-q1

- Decision: **ALLOW**
- Effective kind: **EXACT_PRODUCT**
- Basis: `product:seed:maize:hybrid_abc_treated_50k`
- Contributors shown as: **5-9**
- Freshness: **FRESH**
- AVG_UNIT_PRICE: **31.01 EUR / bag:50000seeds**
- QUANTITY_BAND: **MEDIUM**
- Output boundary: no raw peer rows, no raw evidence, no exact contributor count, no peer total spend

## req-fertilizer-exact-broaden

- Decision: **BROADEN**
- Effective kind: **PRODUCT_CLASS**
- Basis: `productclass:fertilizer:npk_15_15_15`
- Contributors shown as: **5-9**
- Freshness: **FRESH**
- AVG_UNIT_PRICE: **1.134 EUR / kg**
- QUANTITY_BAND: **HIGH**
- Output boundary: no raw peer rows, no raw evidence, no exact contributor count, no peer total spend

## req-fertilizer-long-horizon-block

- Decision: **REFUSE**
- Effective kind: **NONE**
- Basis: `product:fertilizer:brandx_npk151515_25kg`
- Contributors shown as: **HIDDEN**
- Freshness: **FRESH**
- Blocking reasons: `REQUEST_HISTORY_BLOCKED, DIFFERENCING_RISK_HIGH`
- Output boundary: no raw peer rows, no raw evidence, no exact contributor count, no peer total spend

## req-fertilizer-pre-recompute-invalid

- Decision: **REFUSE**
- Effective kind: **PRODUCT_CLASS**
- Basis: `productclass:fertilizer:npk_15_15_15`
- Contributors shown as: **5-9**
- Freshness: **INVALID**
- Blocking reasons: `MATERIALIZATION_NOT_FRESH, RECOMPUTE_REQUIRED`
- Output boundary: no raw peer rows, no raw evidence, no exact contributor count, no peer total spend

## req-fertilizer-post-recompute-fresh

- Decision: **ALLOW**
- Effective kind: **PRODUCT_CLASS**
- Basis: `productclass:fertilizer:npk_15_15_15`
- Contributors shown as: **5-9**
- Freshness: **FRESH**
- AVG_UNIT_PRICE: **1.139 EUR / kg**
- QUANTITY_BAND: **HIGH**
- Output boundary: no raw peer rows, no raw evidence, no exact contributor count, no peer total spend

No output here is promoted OFARM law or deployment-proof tenant intelligence.
