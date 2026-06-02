# OFARM Phase 8 Scenario — Dispute reconstruction agent surfaces competing evidence interpretations

## Scenario family

`dispute_reconstruction_agent`

## Farmer value

Help the farmer defend records and narrow disputes without allowing the agent to decide the dispute.

## Actors

- Humans: farm owner, reviewer
- Agents: Dispute Reconstruction Agent
- External parties: buyer, contractor

## Positive workflow

S1. **Dispute Reconstruction Agent** — reconstructs timeline from canonical assertions, evidence, and traces → `DISPUTE_RECONSTRUCTION_PACKET`
S2. **Dispute Reconstruction Agent** — lists competing interpretations and missing evidence → `ADVISORY_RECONSTRUCTION`
S3. **reviewer** — reviews packet and decides next governance action → `HUMAN_REVIEW_REQUIRED`

## Expected outputs

- Dispute reconstruction packet
- Competing interpretations
- EvidenceNeed

## Guardrails

- agent does not decide dispute
- competing evidence is not suppressed
- timeline cites evidence and trace refs

## Must not happen

- agent silently chooses buyer interpretation
- agent rewrites lot history

## Negative companion

`OFARM-AAI-P8-DISPUTE-RECONSTRUCTION-AGENT-NEG-001`

## Promotion status

This scenario is supporting-only and not promoted into active OFARM law.
