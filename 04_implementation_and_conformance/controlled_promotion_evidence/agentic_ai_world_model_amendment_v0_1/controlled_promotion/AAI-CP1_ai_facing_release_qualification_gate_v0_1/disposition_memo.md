# AAI-CP1 disposition memo v0.1

Generated: 2026-05-16T13:00:00+02:00

## Decision

Promote a narrow active-baseline release-qualification gate. Do not promote draft result-qualification, trace-retrieval, public-operation, preflight, agent, tool-manifest, world-model, EvidenceNeed, or ObservationRequest schemas.

## Findings applied

- SYN-005: AI-facing qualification is not yet an executable product invariant.
- SYN-015: no-hidden-truth / no-hidden-governance should become an executable release gate.
- CP0 source-authority normalization: reviewed material and stale role-review outputs cannot bypass active authority order.

## Resulting control

State-affecting and high-consequence AI-facing/public-operation surfaces are release-eligible only when material limitations are machine-readable and faithfully surfaced. When required qualification is unavailable, the platform must require review, refuse output, or use another policy-declared successor disposition.

## Boundary

This phase hardens the baseline only. It intentionally leaves CP2 to define concrete active RFCs, machine contracts, examples, and trace retrieval behavior.
