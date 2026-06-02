# OFARM FMIS Adapter Spike

Prepared: 2026-05-13  
Status: completed redacted discovery packet  
Data source: BigQuery `login-eko-data-layer`, queried with billing project `login-eko-samoa-sbx`

## What Was Done

I ran a narrow read-only BigQuery spike against the live `prod__t_kis__*` FMIS-like marts.

The goal was to find a single operation chain suitable for first adapter design without exporting personal names, field names, or coordinates.

The selected packet is saved as:

- `ofarm_fmis_adapter_spike_candidate_packet.json`

The query is saved as:

- `ofarm_fmis_adapter_spike_candidate_query.sql`

## Selected Candidate

The selected candidate is a completed `APPLICATION` operation with:

- one hashed operation identity
- one hashed field identity
- planned operation status: `COMPLETED`
- actual operation status: `COMPLETED`
- planned window: 2026-04-20 to 2026-04-26
- actual execution: 2026-04-28 11:48:40 to 2026-04-28 12:15:01
- actual last-modified timestamp: 2026-05-07 21:47:14
- 2 planned material entries
- 2 actual material entries
- 1 vehicle reference
- 1 implement reference
- 1 person reference
- 5 crop-zone actual rows
- 5 crop-zone rows with crop-zone geometry
- 5 crop-zone rows with operation-zone geometry
- no coordinates exported
- no personal names exported

## Important Pattern Found

The strongest operation chain available from the live marts is:

`planned application -> actual application -> crop-zone actual operation geometry/material rows`

The scouting rows do not directly form a full scouting-to-application chain in the visible marts. All 4 scouting observations link to planned `SCOUTING` operations, not to treatment application operations.

This means the first adapter can prove operation intent and execution separation, but it cannot yet prove:

- scouting observation caused or supported the application,
- recommendation existed between scouting and planned operation,
- prescription authority existed,
- accepted consequence was reviewed or promoted.

## OFARM Mapping Implication

The candidate is usable for adapter design as:

- `InterventionIntentPayload` candidate from `fact_field_operation_planned`
- `ExecutionRecordPayload` candidate from `fact_field_operation_actual`
- event-bound `PartialExtent` candidates from `fact_crop_zone_actual_operation`
- local `AgronomicIdentityBinding` candidates from material hashes and rate/unit fields

It is not usable as an `AcceptedEventConsequence` yet.

Promotion is blocked by missing:

- authority or delegation evidence,
- original API/export/machine payload,
- evidence sufficiency decision,
- correction, dispute, and supersession history,
- source-health gate result for the exact source chain,
- product regulatory identity bindings.

## Redaction Policy

The packet intentionally exports:

- hashed operation, field, field geometry, crop-zone, crop, and material identities,
- timestamps,
- status values,
- material quantities and rate/unit fields,
- geometry presence flags,
- geometry area and intersection ratios.

The packet intentionally does not export:

- field names,
- farm names,
- person names,
- material display names,
- crop display names,
- coordinates or WKT geometries.

## Files Produced

- `ofarm_fmis_adapter_spike_candidate_query.sql`
- `ofarm_fmis_adapter_spike_candidate_packet.json`
- `ofarm_fmis_adapter_spike_report.md`
- `ofarm_fmis_source_side_probe_query.sql`
- `ofarm_fmis_source_side_probe_packet.json`

## Source-Side Probe

I then probed the source-facing farming views for the same selected operation.

The selected candidate has:

- 1 source planned-operation row
- source planned-operation status: `COMPLETED`
- 0 deleted markers on the source planned-operation row
- source planned-operation created timestamp: 2025-09-08 06:34:46
- source planned-operation modified timestamp: 2026-04-28 12:15:03
- 3 planned-operation audit entries
- audit entry types:
  - `OPERATION_MODIFY` / `DATE` at 2026-04-09 14:31:34
  - `OPERATION_MODIFY` / `MATERIAL` at 2026-04-20 13:59:46
  - `OPERATION_MODIFY` / `MATERIAL` at 2026-04-20 13:59:46
- 4 planned material audit rows
- 1 work-order link
- 1 work order with status `FINISHED`
- 0 deleted markers on the work order
- 1 task result with status `FINISHED`
- task execution interval matches the actual operation interval: 2026-04-28 11:48:40 to 2026-04-28 12:15:01
- task field coverage moves from 0 ha to 5.37 ha
- task active hours: about 0.4392

This is stronger than the first packet because it proves source-side audit and work-order/task support for the same operation. It still does not prove OFARM acceptance, because the audit entries show modifications and material additions, not an explicit authority or promotion decision.

## Updated OFARM Mapping Implication

The selected candidate now supports a better first fixture skeleton:

- `InterventionIntentPayload`: planned operation row plus material audit entries.
- `ExecutionRecordPayload`: actual operation row plus task result and work-order status.
- `PartialExtent`: crop-zone and operation-zone geometry metrics from crop-zone actual operation rows.
- `PromotionTrace`: not yet mappable; no OFARM-style evidence sufficiency or acceptance decision found.
- `AgronomicReconstructionTrace`: partially mappable; source audit entries and task/work-order rows support a reconstruction trace, but source payload hashes and original API/export bodies are still absent.

## Remaining Blockers After Source Probe

The source probe reduced the correction-history gap, but these blockers remain:

1. No original source API/export/machine payload.
2. No explicit recommendation or prescription authority.
3. No contractor or applicator license/delegation evidence.
4. No evidence sufficiency or acceptance decision.
5. No binary evidence custody.
6. No regulatory product binding for the two materials.
7. No direct scouting-to-application causal link in visible marts.

## Recommended Next Step

Use this candidate as the first adapter fixture skeleton. The next useful implementation artifact is a deterministic OFARM fixture draft that transforms these two redacted packets into separate candidate carriers and explicitly leaves promotion blocked.
