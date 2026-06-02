# Codex FMIS Adapter Backlog

## P0

1. Build BigQuery KIS source inventory adapter.
   - Capture row counts, last-modified times, schema hashes, join keys, and source-health warnings for selected `prod__t_kis__*` tables.
   - Blocked by raw source samples and a source-health contract.

2. Map field and crop-zone geometries to Field and PartialExtent candidates.
   - Use field UUIDs, geometry UUIDs, SCD effective ranges, WGS84 geography, origin fields, crop zones, operation zones, and intersection ratios.
   - Blocked by geometry quality policy and source payload references.

3. Separate planned intent from actual execution.
   - Planned operation rows become `InterventionIntentPayload` candidates; actual operation rows become `ExecutionRecordPayload` candidates.
   - Blocked by authority samples and correction lineage samples.

4. Design correction and dispute reconstruction probe.
   - Locate audit tables or event update streams for deleted, corrected, superseded, aborted, disputed, and late-synced records.
   - Blocked by before/after corrected operation samples and audit/revision tables.

## P1

1. Implement scouting observation importer.
   - Map scouting UUID, observation time, point geometry, EPPO target fields, severity, impacted area, comments, image URLs, field and observer references.
   - Blocked by image custody metadata and method/threshold evidence.

2. Implement material identity binding enrichment.
   - Preserve local material IDs, UUIDs, names, categories, units, target rates and SKU bridge, then add jurisdiction-scoped crop-protection product bindings.
   - Blocked by regulatory product registry binding and active substance evidence.

## P2

1. Add lab/soil measurement adapter only after live rows are available.
   - The schema is present, but live row count was zero.
   - Blocked by actual lab report rows and method/accreditation metadata.
