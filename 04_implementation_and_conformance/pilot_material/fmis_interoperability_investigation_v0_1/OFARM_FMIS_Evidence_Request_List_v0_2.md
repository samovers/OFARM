# OFARM FMIS evidence request list v0.2

Date: 2026-05-13  
Status: active supporting implementation artifact  
Source: normalized from Codex FMIS investigation report  
Change class: external evidence operation

---

## P0 — required before compliance-grade mapping

### REQ-001 — complete crop-protection operation packet

Provide one complete redacted packet linking, where available:

- scouting observation,
- recommendation or prescription,
- planned work order,
- actual/as-applied record,
- review or accepted outcome.

Acceptable formats: BigQuery row packet, API responses, CSV exports, ADAPT, ISOXML, EFDI/ISO 5231, or PDF with matching source IDs.

Purpose: prove join keys across observation, intent, execution, and promotion without guessing from table names.

### REQ-002 — correction / aborted / failed / partial example

Provide before/after evidence for one corrected, aborted, failed, partial, deleted, superseded, disputed, or late-synced operation.

Acceptable formats: audit table extract, BigQuery row packet, API responses before and after correction, screenshots plus export metadata.

Purpose: test OFARM correction, dispute, supersession, late evidence, and reconstruction behavior.

### REQ-003 — authority and responsibility evidence

Provide authority and responsibility evidence for the same operation:

- recommender,
- prescriber,
- planned operator,
- actual operator,
- contractor if any,
- reviewer,
- accepter.

Acceptable formats: job sheet, work order, role/delegation export, contractor invoice, review decision table, API response.

Purpose: separate recommendation, prescription, planned operation, operation claim, and accepted consequence.

### REQ-004 — original machine/controller/as-applied source

Provide the original machine/controller/as-applied source for one application with geometry and material-rate details.

Acceptable formats: ISOXML TASKDATA, ADAPT work record, EFDI/ISO 5231 message set, machine timelog, controller export, API response.

Purpose: prove whether BigQuery actual-operation rows preserve or derive as-applied facts.

---

## P1 — required before high-consequence product/evidence use

### REQ-005 — material/product identity evidence

Provide material/product identity evidence for crop-protection materials used in the sample operation.

Include product catalogue export, inventory item export, label PDF, national register reference, GTIN/SKU mapping, active-substance table, and any local-to-regulatory product binding.

Purpose: bind local material records to regulatory product identity, active substances, label constraints, units, and permitted rates.

### REQ-006 — evidence asset manifest

Provide evidence asset metadata for scouting images and operation attachments.

Include asset table export, upload API response, hash manifest, storage metadata, review/deletion audit, uploader, upload timestamp, and retention policy.

Purpose: decide whether URLs are custody-grade evidence or convenience links.

---

## P2 — only if measurement workflows enter the first pilot slice

### REQ-007 — actual soil/lab measurement packet

Provide an actual soil or lab report sample if lab/measurement workflows are in the pilot slice.

Acceptable formats: lab PDF, CSV, API response, BigQuery row packet, sample chain-of-custody record.

Purpose: the soil measurement table exists but had zero rows; lab method, accreditation, units, uncertainty, and custody remain unproven.

## Addendum-driven evidence requests

The Logineko entity package addendum adds these targeted requests:

- Provide access or export support for `FieldOperationPlanned.scoutingReportUuids` or the equivalent source relationship because the exposed BigQuery source view did not include that array column.
- Provide at least one operation packet where `ScoutingReport.fieldOperationPlanned` links scouting to the planned operation.
- Provide source-side work-order checkpoint rows with any available coverage/fuel image paths, completion state, and user attribution.
- Provide material-session rows for an operation with real material transfer, lot/location, quantity, unknown-quantity reason, lost-material flag, and image-path evidence.
- Provide audit/revision rows that show correction, supersession, cancellation, dispute, or late-sync behavior.

These requests do not replace the original P0 evidence requests for original FMIS/API/export payload custody, authority, evidence sufficiency, product regulatory binding, and source-health/loss maps.
