# OFARM Phase 6 Assumption, Uncertainty, Invalidation, and Reconciliation Rules v0.1

## Assumptions

Assumptions must be declared. They may not hide inside prompt text, model memory, or implementation defaults.

Each assumption should include:

- statement;
- assumption type;
- basis refs;
- confidence posture;
- status;
- invalidation trigger refs;
- promotion posture.

## Uncertainty

Uncertainty must be expressed as a decision-use limit, not only as a score.

A confidence score or uncertainty estimate does not satisfy evidence sufficiency and must not be used as a compliance proof.

## Invalidation

Invalidation rules must exist for scenario outputs whose usefulness depends on time, weather-like context, observations, crop stage, management actions, pack/profile state, model version, materialization freshness, or sharing/authority posture.

## Reconciliation

Observed-outcome reconciliation compares later observations to scenario outputs. It may support calibration, review, and future model-quality evidence. It cannot mutate canonical history or create accepted facts by itself.
