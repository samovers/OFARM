# OFARM Phase 6 World Model Output Disposition Rules v0.1

## Required disposition

Every scenario output must resolve to one or more explicit disposition classes:

- `SIMULATION_ONLY`
- `ADVISORY_EXPLANATION`
- `HYPOTHESIS`
- `RISK_FLAG`
- `ADVISORY_DRAFT`
- `OBSERVATION_REQUEST`
- `EVIDENCE_NEED`
- `BRIDGE_CANDIDATE_PROPOSAL`
- `REVIEW_PROMPT`
- `BLOCKED`
- `NON_PROMOTABLE`

## Prohibited collapses

The following collapses are prohibited:

- `RISK_FLAG` -> compliance fact;
- `SIMULATION_ONLY` -> current state;
- `ADVISORY_DRAFT` -> accepted operation;
- `BRIDGE_CANDIDATE_PROPOSAL` -> accepted bridge;
- model confidence -> evidence sufficiency;
- calibration status -> authority;
- reconciliation record -> canonical correction.

## Bridge path

A world-model output may initiate a BridgeCandidate only if the BridgeCandidate remains proposal-shaped, human-gated, and separately subject to OFARM authority, evidence, review, and promotion law.
