# OFARM FMIS Shadow Adapter Acceptance Gates v0.1

Date: 2026-05-13

The adapter is acceptable for predevelopment only if all gates pass:

1. Every source payload has a source-fidelity envelope.
2. Every import has an immutable receipt and idempotency key.
3. Every semantic loss has a loss-map item.
4. Unresolved actor, product, unit, time, or geometry identity is app-visible.
5. Candidate records are never displayed as accepted execution.
6. High-consequence outputs are blocked when material loss or unresolved identity exists.
7. Duplicate replay reuses the prior receipt or blocks conflicting replay.
8. Trace references exist for intake, identity resolution, and review-required decisions.
