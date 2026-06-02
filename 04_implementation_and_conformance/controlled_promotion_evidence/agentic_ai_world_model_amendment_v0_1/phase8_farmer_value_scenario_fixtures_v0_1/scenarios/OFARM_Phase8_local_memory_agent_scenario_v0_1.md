# OFARM Phase 8 Scenario — Local memory agent preserves farmer knowledge without making it compliance fact

## Scenario family

`local_memory_agent`

## Farmer value

Keep field-specific lived knowledge durable across seasons and workers while preserving evidence discipline.

## Actors

- Humans: farm owner, seasonal worker
- Agents: Local Memory Agent
- External parties: advisor

## Positive workflow

S1. **Local Memory Agent** — captures farmer narrative and local context → `LOCAL_MEMORY_CANDIDATE`
S2. **Local Memory Agent** — links narrative to field/zone and creates optional ObservationRequest → `ADVISORY_LOCAL_MEMORY`
S3. **farm owner** — reviews local memory artifact for persistence → `REVIEW_PENDING`

## Expected outputs

- NarrativeObservation
- LocalMemoryRule candidate
- ObservationRequest

## Guardrails

- local memory stays Advisory unless separately governed
- narrative does not prove physical condition
- observation request is bounded

## Must not happen

- agent converts narrative into compliance fact
- local memory overrides accepted observation

## Negative companion

`OFARM-AAI-P8-LOCAL-MEMORY-AGENT-NEG-001`

## Promotion status

This scenario is supporting-only and not promoted into active OFARM law.
