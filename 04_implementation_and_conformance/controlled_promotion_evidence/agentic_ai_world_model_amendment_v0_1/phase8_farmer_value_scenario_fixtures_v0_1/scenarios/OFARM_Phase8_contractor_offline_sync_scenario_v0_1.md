# OFARM Phase 8 Scenario — Contractor offline evidence sync creates candidates and rechecks revocation

## Scenario family

`contractor_offline_sync`

## Farmer value

Make contractor records easier to collect without letting delayed offline uploads overwrite governed history.

## Actors

- Humans: farm owner, contractor operator
- Agents: Contractor Coordination Agent, Evidence Steward Agent
- External parties: spraying contractor

## Positive workflow

S1. **Contractor Coordination Agent** — captures offline operation claim and evidence bundle → `OFFLINE_CANDIDATE_CAPTURED`
S2. **Contractor Coordination Agent** — replays sync through central authority checks → `SYNC_REVIEW_REQUIRED`
S3. **Evidence Steward Agent** — attaches allowed evidence to draft packet while blocked claim waits for review → `PARTIAL_CANDIDATE_WITH_BLOCKER`

## Expected outputs

- OfflineCaptureEnvelope
- SyncReplayResult
- BlockedActionTrace
- Draft evidence packet

## Guardrails

- offline capture does not finalize facts
- revocation is rechecked on sync
- late data cannot silently overwrite

## Must not happen

- offline contractor upload updates Compliance Twin directly
- revoked delegation still authorizes final write

## Negative companion

`OFARM-AAI-P8-CONTRACTOR-OFFLINE-SYNC-NEG-001`

## Promotion status

This scenario is supporting-only and not promoted into active OFARM law.
