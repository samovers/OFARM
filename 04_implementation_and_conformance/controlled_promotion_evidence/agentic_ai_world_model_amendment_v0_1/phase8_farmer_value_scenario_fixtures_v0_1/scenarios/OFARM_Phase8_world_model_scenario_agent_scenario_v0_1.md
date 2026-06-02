# OFARM Phase 8 Scenario — World-model scenario agent generates risk flag, EvidenceNeed, and BridgeCandidate proposal only

## Scenario family

`world_model_scenario_agent`

## Farmer value

Help the farmer rehearse disease or irrigation decisions with uncertainty and invalidation instead of pretending prediction is truth.

## Actors

- Humans: farm owner, advisor
- Agents: World Model Agent, Advisory Agronomy Agent
- External parties: weather data provider

## Positive workflow

S1. **World Model Agent** — runs advisory scenario with assumptions and validity window → `SCENARIO_RESULT_ADVISORY_ONLY`
S2. **World Model Agent** — creates EvidenceNeed and ObservationRequest for discriminating field observation → `MISSING_INFORMATION_REQUEST`
S3. **Advisory Agronomy Agent** — creates BridgeCandidate proposal for human review if intervention planning is considered → `BRIDGECANDIDATE_PROPOSAL_ONLY`

## Expected outputs

- WorldModelRun
- ScenarioResultSet
- EvidenceNeed
- ObservationRequest
- BridgeCandidate

## Guardrails

- world model remains Advisory-only
- uncertainty is explicit
- BridgeCandidate cannot auto-promote

## Must not happen

- scenario result becomes current-state materialization
- model confidence waives field observation

## Negative companion

`OFARM-AAI-P8-WORLD-MODEL-SCENARIO-AGENT-NEG-001`

## Promotion status

This scenario is supporting-only and not promoted into active OFARM law.
