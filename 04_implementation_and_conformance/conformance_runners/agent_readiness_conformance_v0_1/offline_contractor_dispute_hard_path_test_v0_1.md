# OFARM Offline Contractor Dispute Hard-Path Break Test v0.1

Date: 2026-05-14  
Status: active supporting implementation/conformance candidate

## Scenario

```text
contractor performs work offline
→ delayed sync
→ contractor authority is revoked before sync
→ field geometry changes before sync
→ duplicate retry occurs
→ partial execution discovered
→ evidence is incomplete
→ record is disputed
→ manual correction is submitted
→ high-consequence output is requested
```

## Required platform behavior

1. Offline capture is preserved as local/candidate evidence, not accepted truth.
2. Sync replay uses idempotency keys and duplicate detection.
3. Authority is rechecked at sync time.
4. Field/geometry successor context is checked before promotion.
5. Partial execution remains distinct from accepted full execution.
6. Incomplete evidence is exposed as evidence-insufficient or review-required.
7. Dispute and correction preserve history rather than deleting the original record.
8. Materialization is invalidated or stale-blocking when the basis changes.
9. High-consequence DocumentAssembly is blocked, annexed, or review-required until basis gaps are resolved.
10. Trace retrieval reconstructs capture time, sync time, authority posture, geometry posture, idempotency posture, evidence posture, dispute/correction lineage, and publication refusal/annex logic.

## Required app behavior

The app must display:

- `offline draft saved`, not `completed`
- `submitted for sync`, not `accepted`
- `authority review required` after revocation
- `field basis changed` after geometry drift
- `partial execution`, not `full execution`
- `evidence incomplete`
- `under dispute`
- `corrected/superseded with trace`
- `high-consequence output blocked or annexed`

## Failure rule

Fail if the platform or app treats offline capture, stale authority, duplicate replay, or disputed/corrected records as accepted clean truth without governed promotion and trace.
