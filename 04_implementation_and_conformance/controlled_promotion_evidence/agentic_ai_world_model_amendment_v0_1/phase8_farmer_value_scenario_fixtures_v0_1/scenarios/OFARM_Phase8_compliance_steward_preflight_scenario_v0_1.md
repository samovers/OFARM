# OFARM Phase 8 Scenario — Compliance steward preflight blocks a submission until missing evidence is resolved

## Scenario family

`compliance_steward_preflight`

## Farmer value

Prevent audit panic by identifying missing evidence before a compliance-grade output is frozen or filed.

## Actors

- Humans: farm owner
- Agents: Compliance Steward Agent
- External parties: certifier

## Positive workflow

S1. **Compliance Steward Agent** — runs preflight on draft submission assembly → `PREFLIGHT_RESULT_BLOCKED`
S2. **Compliance Steward Agent** — creates EvidenceNeed for missing product confirmation → `EVIDENCENEED_COMPLIANCE_BLOCKING`
S3. **farm owner** — decides whether to provide evidence, waive, or contest → `HUMAN_DECISION_REQUIRED`

## Expected outputs

- PreflightResult with blocker
- EvidenceNeed
- RequestDisplayEnvelope

## Guardrails

- failed preflight cannot be waived by agent
- submission cannot be filed
- request cites explicit blocking basis

## Must not happen

- agent files submission after failed preflight
- missing evidence is hidden in summary

## Negative companion

`OFARM-AAI-P8-COMPLIANCE-STEWARD-PREFLIGHT-NEG-001`

## Promotion status

This scenario is supporting-only and not promoted into active OFARM law.
