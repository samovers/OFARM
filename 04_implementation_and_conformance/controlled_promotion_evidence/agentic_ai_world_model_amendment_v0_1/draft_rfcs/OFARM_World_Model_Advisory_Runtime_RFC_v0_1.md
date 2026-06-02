# OFARM World Model Advisory Runtime RFC v0.1

Date: 2026-05-14  
Status: draft candidate RFC; not accepted baseline law until promoted.  
Role: define Advisory-only world-model run and state contracts without creating a third twin or hidden current state.


## 1. Problem statement

World-model AI can help farmers reason about scenarios, risk, causality, missing evidence, and likely consequences. But if world-model state becomes hidden truth, OFARM loses its assertion/history-first discipline.

## 2. Scope

This RFC defines:

- `WorldModelRun`
- `WorldModelState`
- `WorldModelAssumptionSet`
- `WorldModelUncertaintyStatement`
- `WorldModelInvalidationRule`
- `ScenarioSpec`
- `ScenarioResultSet`

## 3. Core rule

`WorldModelState` is Advisory-only. It is not:

- canonical truth
- Compliance Twin state
- current-state materialization
- accepted event consequence
- attestation basis
- filed submission basis
- high-consequence basis unless bridged and rechecked through normal OFARM enforcement

## 4. Permitted outputs

A world-model run may produce:

- advisory explanation
- hypothesis
- risk flag
- scenario result
- EvidenceNeed
- ObservationRequest
- draft plan
- BridgeCandidate
- review prompt
- non-promotable advisory report

It may not directly produce:

- accepted compliance fact
- accepted execution consequence
- review decision
- pack activation
- attestation
- filed submission
- hidden materialization

## 5. Required basis fields

A `WorldModelRun` must declare:

- objective
- target scope
- target twin, normally Advisory
- input refs
- query refs
- context snapshot refs
- materialization refs
- pack activation basis
- model/method ref
- assumptions
- uncertainty
- stale input markers
- missing evidence
- competing interpretations where relevant
- output artifacts
- invalidation rules
- BridgeCandidate refs where created

## 6. Invalidation

World-model state must be invalidated or downgraded when:

- context snapshot changes materially
- pack activation basis changes
- materialization basis becomes stale for intended use
- authority/sharing constraints alter available evidence
- observation contradicts scenario assumptions
- model/method profile is revoked or deprecated
- input evidence is corrected, contested, or superseded

## 7. Observed-outcome reconciliation

Where feasible, scenario results should be linked to later observed outcomes without converting the original scenario into truth. Reconciliation improves future advisory quality and traceability.

## 8. Negative cases

The platform must block or qualify:

- scenario result used as compliance fact
- model confidence used as evidence sufficiency
- world-model memory used as source truth
- stale scenario output used for submission
- world-model state exposed as current state
- benchmark signal used as farm-specific compliance fact

## 9. Machine contracts

Candidate schemas:

- `OFARM_WorldModelRun_schema_v0_1.json`
- `OFARM_WorldModelState_schema_v0_1.json`
- `OFARM_WorldModelAssumptionSet_schema_v0_1.json`
- `OFARM_WorldModelUncertaintyStatement_schema_v0_1.json`
- `OFARM_WorldModelInvalidationRule_schema_v0_1.json`
- `OFARM_ScenarioSpec_schema_v0_1.json`
- `OFARM_ScenarioResultSet_schema_v0_1.json`
