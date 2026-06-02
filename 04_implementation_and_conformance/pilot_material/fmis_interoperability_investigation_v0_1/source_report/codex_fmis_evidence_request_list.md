# Codex FMIS Evidence Request List

## P0

1. One complete redacted crop-protection operation packet linking scouting observation, recommendation or prescription, planned work order, actual/as-applied record, and any accepted or reviewed outcome.
   - Acceptable formats: BigQuery row packet, API responses, CSV exports, ADAPT, ISOXML, EFDI/ISO 5231, or PDF with matching source IDs.
   - Why: proves join keys across observation, intent, execution, and promotion.

2. Before/after correction or aborted/failed/partial application example, including audit/revision history and current row state.
   - Acceptable formats: audit table extract, BigQuery row packet, API responses before and after correction, screenshots plus export metadata.
   - Why: tests correction, dispute, supersession, and reconstruction behavior.

3. Authority and responsibility evidence for the same operation: recommender, prescriber, planned operator, actual operator, contractor if any, reviewer, and accepter.
   - Acceptable formats: job sheet, work order, role/delegation export, contractor invoice, review decision table, API response.
   - Why: separates recommendation, prescription, planned operation, operation claim, and accepted consequence.

4. Original machine/controller/as-applied source for one application with geometry and material rate details.
   - Acceptable formats: ISOXML TASKDATA, ADAPT work record, EFDI/ISO 5231 message set, machine timelog, controller export, API response.
   - Why: proves whether BigQuery actual operation rows preserve or derive as-applied facts.

## P1

1. Material/product identity evidence for crop-protection materials used in the sample operation.
   - Include product catalogue export, inventory item export, label PDF, national register reference, GTIN/SKU mapping, active-substance table.
   - Why: binds local materials to regulatory product identity, active substances, label constraints, units, and permitted rates.

2. Evidence asset manifest for scouting images and operation attachments.
   - Include asset table export, upload API response, hash manifest, storage metadata, review/deletion audit.
   - Why: determines whether image URLs are custody-grade evidence or convenience links.

## P2

1. Actual soil or lab report sample if lab/measurement workflows are in the pilot slice.
   - Include lab PDF, CSV, API response, BigQuery row packet, or sample chain-of-custody record.
   - Why: the soil measurement table exists but had zero rows; lab method, accreditation, units, uncertainty, and custody remain unproven.
