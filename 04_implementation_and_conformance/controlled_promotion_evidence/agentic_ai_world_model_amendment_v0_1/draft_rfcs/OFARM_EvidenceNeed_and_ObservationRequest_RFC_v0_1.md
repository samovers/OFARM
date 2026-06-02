# OFARM EvidenceNeed and ObservationRequest RFC v0.1

Date: 2026-05-14  
Status: draft candidate RFC; not accepted baseline law until promoted.  
Role: define bounded, actionable missing-evidence and observation-request objects for agents, world models, apps, and compliance workflows.


## 1. Problem statement

AI agents and world models should be able to ask for missing information. Without governed request objects, this can create farmer task spam, hidden obligations, or vague compliance blockers.

## 2. Scope

This RFC defines:

- `EvidenceNeed`
- `ObservationRequest`

## 3. EvidenceNeed rule

An `EvidenceNeed` states that an OFARM workflow, pack rule, scenario, planned intervention, output, or promotion path is missing evidence.

It must specify:

- target scope
- target twin
- linked pack/rule/output/plan/scenario
- evidence gap
- acceptable evidence options
- reason
- severity
- consequence
- deadline or relevance window
- advisory versus compliance-blocking posture
- requesting agent/run/world-model ref where applicable
- review or promotion path if satisfied

## 4. ObservationRequest rule

An `ObservationRequest` asks for a real-world observation useful for an advisory, operational, evidence, or compliance purpose.

It must specify:

- observation type
- target field/zone/lot/bin/crop cycle/etc.
- minimum acceptable capture
- preferred capture
- reason
- consequence if missing
- relevance window
- advisory/operational/evidence/compliance posture
- authority required to satisfy it

## 5. Noise-control rule

A generated request must not be emitted unless it has:

- purpose
- basis
- severity
- consequence
- relevance window
- target scope
- acceptable completion criteria

## 6. Compliance-blocking basis rule

A request may be marked compliance-blocking only if tied to an active pack, evidence sufficiency policy, authority rule, output assembly rule, promotion rule, or accepted RFC requirement.

## 7. Negative cases

The platform must reject or downgrade:

- evidence requests without consequence
- task spam without relevance window
- compliance blockers without pack/rule/policy basis
- observations that imply accepted facts before capture and promotion
- world-model requests that hide uncertainty or competing interpretations

## 8. Machine contracts

Candidate schemas:

- `OFARM_EvidenceNeed_schema_v0_1.json`
- `OFARM_ObservationRequest_schema_v0_1.json`
