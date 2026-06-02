# OFARM economic intelligence Lane B — Scenario 2 hostile checks v0.1

Date: 2026-04-13
Status: active supporting implementation artifact
Scope: hostile checks specific to own-versus-contractor and bottleneck economics

---

| ID | Failure mode | Why it fails OFARM | Required behavior |
|---|---|---|---|
| LB-H1 | Result says "profit", "profitability", or "operating margin" | Smuggles field-profit semantics out of partial finance | Reject the result set or mark validation failure |
| LB-H2 | Own-option cost uses hidden depreciation, rent, or overhead allocation | Turns a screen into fake field-profit accounting | Fail until the basis is removed or explicitly downgraded |
| LB-H3 | Imported rate extract behaves like ledger truth | Creates a shadow accounting store | Force extract language back to bounded non-ledger posture |
| LB-H4 | Contractor recommendation is made without an explicit timing/capacity assumption | Hidden bottleneck semantics | Fail until the bottleneck window and capacity basis are declared |
| LB-H5 | Bridge prepares dossier or submission output | Lane B is not strong enough for high-consequence export | Reject bridge and keep it report-only |
| LB-H6 | Result implies current-state truth | Makes advisory scenario output a hidden truth store | Reject wording and force Advisory-only notes |
| LB-H7 | Shared output implies recipient write or review authority | Violates sharing-versus-authority separation | Require explicit SharingGrant-only posture |
| LB-H8 | Validator allows field-profitability negative example to pass | Means the seam can drift into pseudo-ERP language | Treat as lane failure |

---

## Lane B stop rule

If Lane B needs broad manual entry of ownership costs, depreciation schedules, and overhead buckets to stay useful, cut it back. The point is bounded operational-economic decision support, not shadow management accounting.
