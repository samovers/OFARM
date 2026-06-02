# OFARM Phase 8 Scenario — Lot and storage buyer-readiness preview preserves event-first lineage

## Scenario family

`lot_storage_buyer_readiness`

## Farmer value

Reduce rejected loads and buyer friction by previewing lot readiness without leaking more farm data than necessary.

## Actors

- Humans: farm owner, storage manager
- Agents: Lot and Storage Agent, Sharing Sovereignty Agent
- External parties: buyer

## Positive workflow

S1. **Lot and Storage Agent** — queries field-to-lot-to-bin lineage and storage observations → `QUALIFIED_LINEAGE_VIEW`
S2. **Lot and Storage Agent** — detects missing lot-transfer evidence and creates EvidenceNeed → `EVIDENCENEED`
S3. **Sharing Sovereignty Agent** — previews scoped buyer-facing output → `DRAFT_BUYER_READINESS_PREVIEW`

## Expected outputs

- Qualified lineage view
- EvidenceNeed for lot transfer
- Buyer-readiness output preview

## Guardrails

- buyer system cannot define farm truth
- preview is not filed output
- redaction and sharing limits apply

## Must not happen

- agent infers accepted lot status from buyer portal alone
- buyer preview exposes whole farm history

## Negative companion

`OFARM-AAI-P8-LOT-STORAGE-BUYER-READINESS-NEG-001`

## Promotion status

This scenario is supporting-only and not promoted into active OFARM law.
