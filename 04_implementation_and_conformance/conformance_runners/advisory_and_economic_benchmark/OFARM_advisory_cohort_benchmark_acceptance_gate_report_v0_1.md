# OFARM advisory cohort benchmark acceptance gate report v0.1

Date: 2026-04-15
Status: active supporting implementation artifact
Scope: bounded acceptance gate for the advisory cohort benchmark spike

---

## Gate outcome

**PASS_WITH_LIMITATIONS**

This is sufficient to continue as `04`-only implementation/conformance work.
It is not sufficient for:
- companion-artifact promotion
- accepted RFC work
- machine-contract promotion
- baseline-law change

---

## Check summary

| Check | Outcome | Notes |
|---|---|---|
| B1_ADVISORY_ONLY_PLACEMENT | PASS | All experimental objects are fixed to the Advisory twin. |
| B2_TWO_LEG_SHARE_PATH | PASS | Runtime sharing fixtures separate contributor-to-operator and operator-to-viewer grants. |
| B3_NO_RAW_PEER_ROWS_OR_EVIDENCE | PASS | Viewer access to raw contribution rows and raw evidence is denied in runtime fixtures. |
| B4_NORMALIZATION_TRACE_REQUIRED | PASS | Contribution examples depend on `ProductNormalizationTrace`; ambiguity/refusal is explicit. |
| B5_DISCLOSURE_CONTROL_EXPLICIT | PASS_WITH_LIMITATIONS | A deterministic disclosure decision object exists, but live request-history enforcement is not proven. |
| B6_QUERY_SUBSET_STAYS_BOUNDED | PASS_WITH_LIMITATIONS | Query templates validate against the current schema and use only `COUNT` / `SUM` / `MAX` / `AVG`, but deployment-scale target equivalence remains unproven. |
| B7_NO_ERP_CREEP | PASS | Negative examples reject ledger-like and per-hectare drift. |
| B8_EXACT_PRODUCT_IS_CONDITIONAL | PASS | Exact product appears only in a safe positive bundle and remains a conditional path. |
| B9_PROMOTION_BLOCK_STILL_HOLDS | PASS | All contracts remain in `04` and are clearly experimental. |

---

## Why this is not a full PASS

- disclosure thresholds are still package-local proof, not deployment telemetry
- differencing control is still rule-shaped rather than production-shaped request-history evidence
- no real-farm pilot is included in this packet
- no user-facing runtime implementation is exercised
- no revocation recompute engine is proven end-to-end

---

## Promotion decision

Keep this seam in:
- `06_active_supporting_research/`
- `04_implementation_and_conformance/`

Do not promote anything from this packet into:
- `01_companion_artifacts/`
- `02_accepted_rfcs/`
- `03_machine_contracts/`

until stronger executable proof exists.

---

## Bottom line

The spike is now concrete enough to support bounded implementation work. It is not yet mature enough to change OFARM law.
