# OFARM FMIS Logineko entity package addendum intake v0.1

Date: 2026-05-13
Status: active supporting implementation evidence
Change class: implementation / conformance implication
Authority impact: does not change active baseline law, accepted RFCs, or machine-contract schemas

## Source

- `source_report/codex_fmis_logineko_entity_package_addendum.md`

## OFARM interpretation

The Logineko entity package addendum is accepted as a source-map aid and schema-discovery input, not as standalone evidence of execution, authority, regulatory identity, original FMIS payload custody, or OFARM promotion eligibility.

The addendum improves the Phase AGR-P10 investigation by identifying source-side entity families and relationship paths that were not fully visible in the BigQuery projection surface. It confirms that Logineko's model includes source concepts for planned operations, planned-operation materials, work-order links, work orders, task results, work-order checkpoints, material sessions, scouting reports, scouting report items, reverse-ETL projections, global/external identity, audit timestamps, and user attribution.

## Source-side execution evidence added

The addendum adds stronger source-side support for the selected KIS adapter-spike candidate:

- selected operation hash: `3bdbb71f4697ab0efa344f6d36e12c842904720c4972384a90b5828b05c59b88`
- source-side work-order checkpoints found: `2`
- checkpoint types: `START`, `END`
- checkpoint time range: `2026-04-28 11:48:40` to `2026-04-28 12:15:01`
- checkpoints with coverage values: `2`
- completed checkpoint count: `1`

OFARM interpretation: this strengthens the `ExecutionRecordPayload` candidate and `AgronomicReconstructionTrace` candidate by adding checkpoint evidence that matches the actual operation interval. It remains source-side discovery evidence and does not create an accepted consequence.

## Source-side gaps confirmed

The addendum confirms or sharpens these blockers:

- selected application has no linked scouting reports in the available source-side BigQuery views
- selected application has no linked scouting report items through those reports
- selected application has no linked material sessions
- checkpoint fuel values and checkpoint image evidence are absent for the selected candidate
- the package does not provide original FMIS/API/export payload custody
- the package does not provide OFARM promotion authority, evidence-sufficiency decision, correction/dispute status, regulatory material identity, or a complete scouting-to-recommendation-to-prescription-to-application chain

## Implementation consequence

The first read-only KIS adapter spike should add entity-guided probes for:

1. `FieldOperationPlanned.scoutingReportUuids` or equivalent source-side relationship recovery.
2. `ScoutingReport.fieldOperationPlanned` relationship recovery.
3. Work-order checkpoint capture and mapping into source-side execution evidence.
4. `WorkOrderTaskResult` and `TaskResultHub` interval, coverage, vehicle, implement, user, and task UUID extraction.
5. Material-session capture for transfer, lot/location, quantity, image-path, unknown-quantity, and lost-material fields.
6. Audit timestamp and user attribution extraction for correction/dispute/supersession reconstruction.

## Boundary

The entity package is a map, not an evidence source of final truth. It should guide adapter probes and source-health checks, while OFARM continues to block promotion until original source payloads, authority evidence, regulatory product bindings, correction/dispute checks, and evidence-sufficiency decisions are present.
