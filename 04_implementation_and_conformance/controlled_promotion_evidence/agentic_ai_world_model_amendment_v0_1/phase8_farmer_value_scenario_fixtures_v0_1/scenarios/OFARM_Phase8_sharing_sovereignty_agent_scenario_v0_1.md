# OFARM Phase 8 Scenario — Sharing and sovereignty agent produces scoped permission-limited answer

## Scenario family

`sharing_sovereignty_agent`

## Farmer value

Let the farmer share useful proof with a buyer, lender, certifier, or advisor without surrendering broad farm data.

## Actors

- Humans: farm owner
- Agents: Sharing Sovereignty Agent
- External parties: buyer, advisor

## Positive workflow

S1. **Sharing Sovereignty Agent** — evaluates SharingGrant and redaction profile for buyer → `PERMISSION_LIMITED_RESULT`
S2. **Sharing Sovereignty Agent** — prepares scoped PassportView-like preview only if output taxonomy permits → `DRAFT_SCOPED_VIEW`
S3. **Sharing Sovereignty Agent** — explains hidden/withheld fields without revealing them → `QUALIFIED_ANSWER`

## Expected outputs

- PermissionLimitedResult
- Scoped draft output preview
- ResultQualificationEnvelope

## Guardrails

- revocation respected
- withheld data not exposed by explanation
- PassportView not used as generic bucket

## Must not happen

- agent over-discloses beyond SharingGrant
- permission-limited result is treated as no records exist

## Negative companion

`OFARM-AAI-P8-SHARING-SOVEREIGNTY-AGENT-NEG-001`

## Promotion status

This scenario is supporting-only and not promoted into active OFARM law.
