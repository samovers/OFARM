# Logineko entity package addendum

Generated: 2026-05-13T13:04:27Z

## Question

Assess whether `/Users/einstein/Downloads/10 Work/Farm RM - Logineko/Packages/logineko-entity.zip` can help answer the original OFARM/FMIs investigation after the Google Cloud Postgres path was found stopped.

## Short answer

Yes, but as a schema and source-map aid rather than as standalone evidence.

The package is a Java entity/model archive. It does not contain live records or original FMIS payloads, but it does identify source-side farming entities and reverse-ETL projections that can guide better BigQuery probes.

## Useful findings from the package

The package contains source models for:

- planned field operations
- planned operation materials
- planned-operation-to-work-order links
- work orders
- task results
- work-order checkpoints
- material sessions
- scouting reports
- scouting report items
- reverse-ETL field operation projections
- reverse-ETL crop-zone scouting projections
- global identity and external identity handling
- audit timestamp and user attribution handling

Important semantic details:

- `FieldOperationPlanned` has a first-class scouting relationship through `scoutingReportUuids` in the Java entity, while the BigQuery source view exposed in this environment does not include that array column.
- `ScoutingReport` also links directly to `FieldOperationPlanned` through `fieldOperationPlanned`.
- `WorkOrderTaskResult` and `TaskResultHub` preserve execution interval, coverage, fuel consumption fields, vehicle, implement, user, and task UUID.
- `WorkOrderCheckpoint` can preserve start/end checkpoints, coverage values, fuel readings, completion state, and image-path fields.
- `MaterialSession` can preserve material transfer, lot/location, quantity, image-path, unknown-quantity reason, and lost-material fields.

## Entity-guided BigQuery recheck

Using the package as a map, I rechecked source-side BigQuery views for the selected adapter-spike application candidate:

- operation hash: `3bdbb71f4697ab0efa344f6d36e12c842904720c4972384a90b5828b05c59b88`
- source views checked:
  - `prod__t_kis__source_farming.evpss_scouting_report`
  - `prod__t_kis__source_farming.evpss_scouting_report_item`
  - `prod__t_kis__source_farming.evpos_work_order_checkpoint`
  - `prod__t_kis__source_farming.evpos_material_session`

Results:

- scouting reports linked to the selected application operation: `0`
- scouting report items linked through those reports: `0`
- work-order checkpoints linked to the selected operation's work order: `2`
- checkpoint types: `START`, `END`
- checkpoint time range: `2026-04-28 11:48:40` to `2026-04-28 12:15:01`
- checkpoints with coverage values: `2`
- checkpoints with fuel values: `0`
- checkpoint coverage images: `0`
- checkpoint fuel images: `0`
- completed checkpoint count: `1`
- incomplete reason count: `0`
- material sessions linked to the selected work order: `0`

## Investigation impact

This package improves the investigation in three ways:

1. It confirms that the Logineko model has a real scouting-to-planned-operation concept, even though the selected completed application candidate did not have linked source scouting rows in the available BigQuery views.
2. It adds a stronger source-side execution check for the selected operation: the work order has start/end checkpoint rows matching the task execution interval and coverage trail.
3. It identifies material custody/session tables that should be part of any future OFARM-grade adapter, even though no material sessions existed for the selected candidate.

It does not resolve:

- original FMIS/API/export payload custody
- OFARM acceptance or promotion authority
- correction/dispute status
- regulatory material identity
- a complete scouting-to-recommendation/prescription-to-application chain for the selected application
- material transfer or quantity-image evidence for the selected application

## Conclusion

The entity package helps more than the stopped Postgres path because it gives a reliable model map for additional BigQuery source probes. It adds one useful answer to the current report: the selected completed application has source-side work-order checkpoint evidence. It does not, by itself, supply the missing original FMIS materials or prove OFARM-grade acceptance.
