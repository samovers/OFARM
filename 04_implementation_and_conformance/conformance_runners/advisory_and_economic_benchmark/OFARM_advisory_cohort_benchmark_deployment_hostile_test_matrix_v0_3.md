# OFARM advisory cohort benchmark deployment hostile test matrix v0.3

Date: 2026-04-15
Status: active supporting implementation artifact
Scope: hostile deployment-readiness tests for the advisory cohort benchmark seam after the real-pilot handoff packet

---

| Hostile case | Expected behavior | Packet status |
|---|---|---|
| Operator submits a dataset marked `REAL_REDACTED_PILOT` but `actualTenantData` is false or null | Refuse the dataset honesty posture | PASS |
| Operator includes obvious personal, tax, banking, or free-form identity keys in the pilot packet | Refuse the dataset | PASS |
| Raw receipt payloads or raw peer rows are attached to the benchmark surface | Refuse the surface | PASS |
| Exact contributor count is shown on the surface | Refuse the surface | PASS |
| Peer total spend is shown on the surface | Refuse the surface | PASS |
| Spend-per-hectare or other forbidden metric appears on the surface | Refuse the surface | PASS |
| Exact-product fertilizer request has unsafe request history | Broaden or block depending on the request-history status | PASS |
| Long-horizon repeated exact-slice narrowing remains unsafe | Block | PASS |
| Contribution revoked after an earlier materialization is still present in the fresh recomputed view | Refuse the result as invalid | PASS |
| Real pilot packet lacks explicit share-grant refs or reviewed extract refs | Refuse intake | PASS |
| Mixed unit or mixed comparability posture is silently averaged | Refuse or send for review | OPEN_LIMITATION |
| Multiple viewers collude across tenants or time windows to infer hidden slices | Needs deployment telemetry and cross-viewer governance beyond this packet | OPEN_LIMITATION |
| Actual tenant pilot data absent from the workspace | Do not overclaim completion; gate only for handoff readiness | PASS |

---

## Interpretation

This matrix is good enough for a bounded redacted real pilot handoff.
It is not good enough to claim deployment closure or law-level readiness.
