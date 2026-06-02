# OFARM Phase 2 Machine-Contract Promotion Patch Plan v0.1

Status: supporting review plan; no active promotion applied

## Safe first contract family

The lowest-risk first machine-contract family is:

- public operation descriptors;
- preflight request/result;
- result qualification;
- runtime problem reason-code registry;
- trace retrieval;
- read-model/output preview envelopes;
- source-fidelity envelope.

These contracts make apps and agents safer without claiming that a runtime exists.

## Promotion dependencies

- `OfflineCaptureEnvelope` and `SyncReplayResult` should move only with offline/delayed-sync review.
- identity-resolution contracts should move only with identity/dedup RFC review.
- calculation/formula contracts should remain held.
- agent-tool manifest should wait for Phase 5 agent capability harmonization.
- conformance/execution-report schemas should remain under implementation/conformance until a runtime exists.

## Required checks

- JSON syntax valid.
- JSON Schema validates under declared draft where possible.
- `$id` values stable.
- Examples exist or are planned.
- Contract does not create a hidden write path.
- Contract result shape preserves freshness, permission, evidence, and authority posture.
