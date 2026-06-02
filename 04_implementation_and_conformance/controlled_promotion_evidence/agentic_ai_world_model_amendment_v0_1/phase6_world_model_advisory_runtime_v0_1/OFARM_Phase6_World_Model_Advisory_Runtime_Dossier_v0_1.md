# OFARM Phase 6 — World Model Advisory Runtime Dossier v0.1

## Classification

- Phase: AAI-P6
- Package status: Supporting implementation/conformance material
- Promotion status: Not promoted
- Runtime status: Not run; no implementation exists
- Two-agent compatibility: Not run; no implementation exists

## Why this phase exists

Earlier phases established agent actorship, run envelopes, traces, handoff, and tool/capability self-description. Phase 6 adds the missing advisory runtime shape for world-model AI.

A world model is useful to farmers only if it can reason across fields, crop cycles, observations, local memory, weather-like context, operations, storage, lots, and future scenarios. But a world model is dangerous if it becomes a hidden farm truth store. Phase 6 therefore gives world-model outputs a governed place inside the Advisory Twin without creating a third twin or weakening current-state materialization law.

## Active authority posture

This phase relies on the active OFARM posture already clarified by AAI-P1:

- two logical twins remain Compliance and Advisory;
- world-model state cannot become Compliance Twin state;
- projections, caches, AI memory, scenario state, and public surfaces cannot become hidden truth;
- tool-call success and model confidence do not waive semantic or promotion law.

No active baseline file is changed by this phase.

## Candidate artefacts

Phase 6 introduces candidate contracts for:

- `WorldModelRun`
- `WorldModelState`
- `WorldModelInputBasis`
- `WorldModelObservationBasis`
- `WorldModelAssumptionSet`
- `WorldModelUncertaintyStatement`
- `WorldModelValidityWindow`
- `WorldModelInvalidationRule`
- `WorldModelOutputDisposition`
- `WorldModelGovernanceBlocker`
- `WorldModelCalibrationEvidence`
- `WorldModelReconciliationRecord`
- `ScenarioSpec`
- `ScenarioResultSet`

## Minimum controlled claim

A valid world-model run can claim only this:

> The system produced an advisory scenario result under declared inputs, assumptions, uncertainty, validity, invalidation, and output-disposition constraints.

It cannot claim:

- accepted disease presence;
- accepted operation need;
- accepted compliance fact;
- accepted current state;
- accepted evidence sufficiency;
- accepted submission readiness;
- pack or policy activation;
- filing or attestation authorization.

## Promotion recommendation

After architect review, promote this phase as an accepted RFC and machine-contract family only if the following boundaries remain intact:

1. `targetTwin` is `ADVISORY` for world-model runs and scenario state.
2. Every world-model state object has `notCurrentStateMaterialization=true`, `notComplianceState=true`, and `notThirdTwin=true`.
3. Every scenario result has output dispositions and at least one freshness or uncertainty posture.
4. Invalidation and reconciliation are explicit.
5. Observed-outcome reconciliation cannot mutate canonical history by itself.
6. Scenario results may create BridgeCandidates only through human-gated OFARM pathways.

## Risks controlled

- world model as hidden third twin;
- scenario result as compliance fact;
- confidence score as evidence sufficiency;
- stale scenario as submission basis;
- model memory as truth;
- observed-outcome reconciliation as silent correction;
- model calibration as authority.
