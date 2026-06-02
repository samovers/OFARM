# OFARM advisory cohort benchmark runtime acceptance gate report v0.2

Date: 2026-04-15
Status: active supporting implementation artifact
Scope: runtime-proof acceptance gate for the advisory cohort benchmark seam

---

## Gate outcome

**PASS_WITH_LIMITATIONS**

This is sufficient to continue bounded `04` implementation/conformance work.
It is not sufficient for:
- companion-artifact promotion
- accepted RFC work
- machine-contract promotion
- baseline-law change

---

## Check summary

| Check | Outcome | Notes |
|---|---|---|
| R1_REQUEST_HISTORY_GUARD_EXECUTABLE | PASS | The packet now carries explicit request-history assessment objects and runtime records for clear, broaden, and blocked paths. |
| R2_RISKY_NARROWING_BROADEN_OR_BLOCK | PASS | Exact-product fertilizer requests are either broadened to product class or denied when repeated narrowing creates differencing risk. |
| R3_REVOCATION_INVALIDATES_PRIOR_MATERIALIZATION | PASS | The recompute bundle proves that contributor revocation invalidates future use of the old benchmark materialization. |
| R4_RECOMPUTED_VIEW_EXCLUDES_REVOKED_CONTRIBUTION | PASS | The fresh recomputed materialization and disclosure decision use only active contributions. |
| R5_STALE_OR_INVALID_VIEW_NOT_SERVED | PASS | Runtime sharing and disclosure records deny the stale/invalid view until recompute completes. |
| R6_USER_SURFACE_REMAINS_BOUNDED | PASS | Example cards remain `VIEW_MODULE` / `SUMMARY_ROWS` shaped and do not expose raw peer rows, exact contributor counts, or peer total spend. |
| R7_QUERY_SURFACE_STAYS_BOUNDED | PASS | Query templates validate against the active `QuerySpecification` schema and stay inside the existing aggregate subset. |
| R8_ILLUSTRATIVE_REDACTED_PILOT_PACKET_PRESENT | PASS_WITH_LIMITATIONS | A redacted pilot packet is present, but it is explicitly illustrative and non-real. |
| R9_PROMOTION_BLOCK_STILL_HOLDS | PASS | All benchmark-specific contracts remain inside `04` and are clearly experimental. |

---

## Why this is not a full PASS

- request-history proof is still package-local and not deployment telemetry
- the redacted pilot dataset is illustrative non-real, not actual tenant data
- multi-viewer collusion and long-horizon cross-window differencing are still hostile-review subjects rather than deployed controls
- no live runtime service has been exercised

---

## Promotion decision

Keep this seam in:
- `04_implementation_and_conformance/`

Do not promote anything from this packet into:
- `01_companion_artifacts/`
- `02_accepted_rfcs/`
- `03_machine_contracts/`

until real deployment-grade evidence exists.

---

## Bottom line

The runtime seam is now much more concrete.
The main remaining gap is no longer “can OFARM represent this?”.
The remaining gap is “can a deployment enforce this safely at real tenant scale?”.
