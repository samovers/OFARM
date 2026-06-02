# OFARM Phase 6 Conformance Fixture Plan v0.1

## Positive fixtures

1. Disease-risk advisory scenario creates a risk flag, uncertainty statement, validity window, invalidation rules, and a human-gated BridgeCandidate proposal.
2. Irrigation timing scenario expires after rainfall divergence and is marked `REQUIRES_RECHECK`.
3. Storage-risk scenario creates an `ObservationRequest` candidate but no compliance fact.
4. Lot-lineage reconstruction scenario produces competing interpretations and a review prompt.
5. Observed-outcome reconciliation records scenario-versus-observation comparison without mutating canonical history.

## Hostile fixtures

1. Submit `WorldModelState` as current-state materialization.
2. Treat model confidence as evidence sufficiency.
3. File a submission from a stale scenario result.
4. Ignore pack/profile change after a scenario run.
5. Use model memory as accepted source truth.
6. Treat calibration evidence as authority.
7. Create an AI/world-model third twin.
8. Promote BridgeCandidate without human approval.

## Execution posture

These are pre-implementation fixtures. Runtime execution is `NOT_RUN_NO_IMPLEMENTATION`.
