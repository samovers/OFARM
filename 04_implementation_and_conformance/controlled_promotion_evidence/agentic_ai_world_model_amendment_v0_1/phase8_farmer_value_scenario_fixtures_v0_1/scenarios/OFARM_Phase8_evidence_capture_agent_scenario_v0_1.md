# OFARM Phase 8 Scenario — Evidence capture agent turns product-label photo into candidate evidence

## Scenario family

`evidence_capture_agent`

## Farmer value

Reduce end-of-season paperwork by converting real-world material into candidate evidence with review path and source fidelity.

## Actors

- Humans: farm worker, farm owner reviewer
- Agents: Evidence Steward Agent
- External parties: input supplier

## Positive workflow

S1. **Evidence Steward Agent** — receives upload under capture-only authority → `CAPTURE_ACCEPTED_AS_CANDIDATE`
S2. **Evidence Steward Agent** — classifies material and attaches it to draft evidence packet → `DRAFT_EVIDENCE_CANDIDATE`
S3. **farm owner reviewer** — reviews evidence sufficiency before promotion → `REVIEW_PENDING`

## Expected outputs

- DRAFT_EVIDENCE_CANDIDATE
- ReviewRequest
- AgentRunTrace

## Guardrails

- photo is not accepted evidence by itself
- classification tool hint does not grant authority
- review is explicit

## Must not happen

- label photo becomes accepted evidence without review
- agent approves its own classification

## Negative companion

`OFARM-AAI-P8-EVIDENCE-CAPTURE-AGENT-NEG-001`

## Promotion status

This scenario is supporting-only and not promoted into active OFARM law.
