# OFARM World Model Advisory Runtime RFC v0.2 Candidate

## Status

Supporting candidate only. Not accepted. Not active law.

## Scope

This RFC candidate defines advisory world-model runtime artifacts for OFARM. It does not create a third twin, alter evidence law, alter authority law, alter current-state materialization law, or permit AI-generated outputs to become governance decisions.

## Normative candidate rule

A `WorldModelRun` executes in the Advisory Twin. Any `WorldModelState`, `ScenarioSpec`, `ScenarioResultSet`, assumption, uncertainty statement, invalidation rule, reconciliation record, calibration evidence, or output disposition produced by that run is advisory unless and until a separate OFARM-governed path accepts a distinct artifact through normal evidence, authority, review, promotion, and publication rules.

## Candidate objects

### WorldModelRun

A run-level object that records the advisory objective, target scopes, agent run envelope where applicable, input basis, observation basis, scenario specs, scenario result sets, world-model states, assumptions, uncertainty statements, invalidation rules, output dispositions, and blockers.

Required invariant:

- `targetTwin=ADVISORY`
- `advisoryOnly=true`
- `cannotPromoteDirectly=true`

### WorldModelState

An advisory state-like runtime object. It is useful for scenario continuity and simulation, but is not canonical truth.

Required invariant:

- `originTwin=ADVISORY`
- `truthPosture=ADVISORY_ONLY_NOT_CANONICAL_TRUTH`
- `notCurrentStateMaterialization=true`
- `notComplianceState=true`
- `notThirdTwin=true`

### ScenarioSpec

A scenario request describing purpose, question, type, scope, input basis, observation basis, assumption set, model/method, requested outputs, and prohibited uses.

### ScenarioResultSet

A scenario output package containing result items, uncertainty, evidence/observation requests where applicable, BridgeCandidate refs where created, blocker refs, output dispositions, and freshness posture.

### WorldModelAssumptionSet

A declared assumption package. Assumptions are never hidden inside prompt text or model memory for governed use.

### WorldModelUncertaintyStatement

A statement of uncertainty and decision-use limit. Uncertainty statements explicitly do not satisfy evidence sufficiency.

### WorldModelValidityWindow

A validity or relevance window for advisory use.

### WorldModelInvalidationRule

A rule that marks state or scenario output stale, invalidated, or requiring recomputation when declared triggers occur.

### WorldModelOutputDisposition

A disposition class for a world-model output. Disposition controls whether an output is simulation-only, advisory explanation, risk flag, draft, evidence/observation request, BridgeCandidate proposal, review prompt, blocked, or non-promotable.

### WorldModelGovernanceBlocker

A blocker record for attempted unsafe use of world-model material.

### WorldModelCalibrationEvidence

A credibility/evaluation artifact for model quality. It is not authority and not evidence sufficiency.

### WorldModelReconciliationRecord

A record comparing scenario output to later observed outcomes. It may inform calibration and review, but cannot mutate canonical history by itself.

## Output path

World-model outputs may resolve to:

- advisory explanation;
- hypothesis;
- risk flag;
- advisory draft;
- EvidenceNeed;
- ObservationRequest;
- BridgeCandidate proposal;
- review prompt;
- governance blocker;
- non-promotable output.

They may not directly resolve to accepted compliance fact, accepted current-state materialization, accepted execution, pack activation, attestation, filing, or frozen output.

## Relationship to BridgeCandidate

A scenario may create or reference a BridgeCandidate only as a proposal-shaped, human-gated advisory-to-compliance handoff. This RFC does not modify BridgeCandidate law.

## Relationship to Phase 7

This RFC references `EvidenceNeed` and `ObservationRequest` because world-model runs commonly reveal missing information. Their full farmer-facing request semantics remain a later EvidenceNeed / ObservationRequest RFC.

## Negative cases

Implementations must block:

- world-model state as current state;
- scenario result as compliance fact;
- model confidence as evidence sufficiency;
- stale/invalidated scenario as submission basis;
- reconciliation as canonical correction;
- model memory as truth;
- third twin creation.
