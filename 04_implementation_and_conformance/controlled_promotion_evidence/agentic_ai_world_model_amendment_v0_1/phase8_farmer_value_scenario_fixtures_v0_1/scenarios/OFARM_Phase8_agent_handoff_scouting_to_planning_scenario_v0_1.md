# OFARM Phase 8 Scenario — Scouting agent hands context to planning agent without transferring authority

## Scenario family

`agent_handoff_scouting_to_planning`

## Farmer value

Coordinate specialist agents while preventing silent delegation or privilege carryover.

## Actors

- Humans: farm owner, advisor
- Agents: Scouting Agent, Planning Agent
- External parties: none

## Positive workflow

S1. **Scouting Agent** — creates observation candidate and advisory risk note → `ADVISORY_OBSERVATION_CANDIDATE`
S2. **Scouting Agent** — creates handoff envelope with context and unresolved blockers → `CONTEXT_HANDOFF_ONLY`
S3. **Planning Agent** — opens new run and independently obtains authority before draft plan → `NEW_RUN_REQUIRED`

## Expected outputs

- AgentHandoffEnvelope
- New AgentRunEnvelope
- Draft planned intervention only if authorized

## Guardrails

- handoff does not carry authority
- receiving agent rechecks scope
- unresolved blockers preserved

## Must not happen

- planning agent acts using scouting agent authority
- handoff strips stale-context warning

## Negative companion

`OFARM-AAI-P8-AGENT-HANDOFF-SCOUTING-TO-PLANNING-NEG-001`

## Promotion status

This scenario is supporting-only and not promoted into active OFARM law.
