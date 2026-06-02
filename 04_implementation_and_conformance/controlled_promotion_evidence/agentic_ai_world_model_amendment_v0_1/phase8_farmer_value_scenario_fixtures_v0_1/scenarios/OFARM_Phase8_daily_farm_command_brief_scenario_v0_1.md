# OFARM Phase 8 Scenario — Daily farm command brief preserves freshness and permission limits

## Scenario family

`daily_farm_command_brief`

## Farmer value

Reduce morning decision burden by turning governed current-state, advisory, pack, and evidence signals into a short attention brief.

## Actors

- Humans: farm owner
- Agents: Farm Orchestrator Agent, Compliance Steward Agent
- External parties: none

## Positive workflow

S1. **Farm Orchestrator Agent** — opens AgentRunEnvelope for read-only brief generation → `RUN_STARTED_READ_ONLY`
S2. **Farm Orchestrator Agent** — executes governed QuerySpecifications over current-state and advisory surfaces → `QUALIFIED_RESULTS`
S3. **Compliance Steward Agent** — adds evidence gaps and compliance blockers without approving anything → `ADVISORY_SUMMARY`

## Expected outputs

- DailyFarmBrief advisory summary
- RequestDisplayEnvelope with priority and burden
- Blocked/stale indicators

## Guardrails

- brief carries freshness posture
- permission-limited answers are labelled
- no hidden writes
- no document approval

## Must not happen

- brief hides stale current state
- brief implies no issue where permission-limited result prevented visibility

## Negative companion

`OFARM-AAI-P8-DAILY-FARM-COMMAND-BRIEF-NEG-001`

## Promotion status

This scenario is supporting-only and not promoted into active OFARM law.
