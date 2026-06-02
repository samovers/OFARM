# OFARM FMIS investigation intake v0.1

Date: 2026-05-13  
Status: active supporting implementation artifact  
Source report: `source_report/codex_fmis_investigation_report.md`  
Change class: implementation/conformance implication  
Baseline impact: none

---

## Intake verdict

The Codex investigation is useful and should be accepted as **implementation-discovery evidence**, not as OFARM source truth.

It found a live FMIS-like BigQuery surface under `login-eko-data-layer`, especially the `prod__t_kis__*` family. That surface appears suitable for a first adapter fixture around:

`planned application -> actual application -> crop-zone actual operation geometry/material rows`

It does **not** yet prove the full OFARM crop-protection chain:

`scouting -> recommendation -> prescription -> planned work -> actual/as-applied work -> review/acceptance -> compliance reconstruction`

The report remains `partial` with overall confidence `3` and readiness assessment `needs_more_samples`.

## What the report proves

- A live BigQuery data layer exists and is reachable.
- KIS/FM​​IS-like marts include fields, crop zones, scouting observations, planned operations, actual operations, materials, equipment, tasks, work orders, traceability, and a soil measurement schema.
- Planned and actual `APPLICATION` operation surfaces are separate enough to design a first adapter fixture.
- A redacted completed application candidate exists with planned materials, actual materials, actual execution interval, task/work-order support, crop-zone geometry metrics, and source-side audit rows.
- The source-side probe found planned-operation audit entries, a work-order link, a finished work order, and a finished task result for the selected operation.

## What the report does not prove

- No original source API/export/machine payload was supplied.
- No recommendation or prescription authority was found.
- No OFARM-style evidence sufficiency decision or accepted consequence exists in the visible packet.
- No contractor/applicator license or delegation evidence was supplied.
- No regulatory crop-protection product binding was supplied for the materials.
- No direct scouting-to-application causal link was visible.
- Correction, cancellation, dispute, supersession, and late-sync lineage are not fully proven.
- Scouting image URLs are not yet custody-grade evidence.
- Soil/lab measurement rows were not available for a live measurement adapter.

## OFARM decision

Use the report to start a **redacted KIS adapter fixture skeleton** and a **P0 evidence request loop**.

Do not promote any BigQuery mart row, machine/task row, scouting image URL, material display name, or operation-zone geometry into accepted OFARM truth without:

1. source payload or API/export reference,
2. authority/delegation evidence,
3. evidence sufficiency decision,
4. correction/dispute/supersession check,
5. product/quantity/unit/code-binding checks where relevant,
6. materialization freshness and reconstruction policy.

## Current next move

Create a deterministic fixture that maps the redacted candidate into candidate carriers only:

- `InterventionIntentPayload` candidate from planned operation and material audit rows,
- `ExecutionRecordPayload` candidate from actual operation, task result, and work-order status,
- `PartialExtent` candidate from crop-zone and operation-zone metrics,
- `AgronomicIdentityBinding` candidate from local material hashes/rate/unit fields,
- `AgronomicReconstructionTrace` partial candidate from audit/task/work-order rows.

Expected outcome: promotion remains blocked; no `AcceptedEventConsequence` is produced.

## Addendum intake — Logineko entity package

A later addendum assessed `logineko-entity.zip` as a Java entity/model archive. OFARM treats it as a schema and source-map aid, not as standalone execution evidence.

The addendum confirms that the selected adapter-spike application candidate has two source-side work-order checkpoints (`START`, `END`) across `2026-04-28 11:48:40` to `2026-04-28 12:15:01`, matching the actual operation interval and strengthening source-side execution reconstruction. It also confirms that the selected candidate has zero linked scouting reports in the available source-side views and zero linked material sessions.

Result: execution/reconstruction confidence improves for adapter discovery, but accepted execution and compliance-grade promotion remain blocked.
