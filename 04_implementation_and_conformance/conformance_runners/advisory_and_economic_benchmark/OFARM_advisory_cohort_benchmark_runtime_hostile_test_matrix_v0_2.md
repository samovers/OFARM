# OFARM advisory cohort benchmark runtime hostile test matrix v0.2

Date: 2026-04-15
Status: active supporting implementation artifact
Scope: hostile runtime tests for the advisory cohort benchmark seam after the runtime proof packet

---

| Hostile case | Expected behavior | Packet status |
|---|---|---|
| Same viewer repeats a broad product-class request | Allow if the request is equivalent and all other safety checks pass | PASS |
| Same viewer narrows from product class to exact product over the same window | Broaden or block before delivery | PASS |
| Same viewer repeats overlapping narrowed requests to infer a hidden cohort | Block due to request-history differencing risk | PASS |
| Viewer requests raw evidence after benchmark view access was granted | Deny | PASS |
| Viewer requests raw contribution rows after benchmark view access was granted | Deny | PASS |
| Contribution is revoked after an earlier benchmark materialization was generated | Invalidate old materialization for future use and require recompute | PASS |
| Stale or invalid benchmark materialization is served as current | Refuse or recompute first | PASS |
| Exact contributor count is exposed on the view | Refuse the shape; show band or hidden posture only | PASS |
| Raw peer total spend appears on the view | Refuse the shape | PASS |
| Exact-product fertilizer request has unsafe history but broader class is still safe | Broaden to product class and re-evaluate | PASS |
| Unit/currency comparability fails | Refuse or route to reviewed normalization, not silent averaging | OPEN_LIMITATION |
| Multiple viewers collude across long time horizons to reconstruct hidden slices | Needs stronger deployment-grade telemetry/guarding than this packet provides | OPEN_LIMITATION |

---

## Interpretation

This matrix is good enough for continued bounded `04` work.
It is not good enough to claim deployment closure or law-level readiness.
