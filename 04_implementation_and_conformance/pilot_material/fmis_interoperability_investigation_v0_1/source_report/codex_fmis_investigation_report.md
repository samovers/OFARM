# Codex FMIS Investigation Report

Prepared: 2026-05-13  
Status: partial  
Scope: crop-protection scouting to audit reconstruction.

## Executive Finding

Live BigQuery access proves a useful FMIS-like data surface exists for the first OFARM adapter spike. The strongest candidate is the `prod__t_kis__*` family in `login-eko-data-layer`: it exposes fields, crop zones, scouting observations, planned operations, actual operations, crop/material catalogues, equipment, tasks, work orders, traceability, and soil measurement schema.

This is not yet enough for compliance-grade OFARM mapping. The investigation did not receive raw FMIS export files, API payload packets, correction examples, authority/delegation records, machine/controller files, or evidence custody manifests. Current marts and projected tables must be treated as discovery evidence, not OFARM truth.

## Materials Inspected

- `input_context/OFARM2_agronomic_phase9_local_knowledge_rationale_lineage_amended_2026-05-13.zip`: active OFARM context, extracted read-only.
- `input_context/OFARM2_agronomic_deep_research_report_2026-05-12.md`: carrier and standards discipline.
- BigQuery `login-eko-data-layer`, queried with billing project `login-eko-samoa-sbx`.
- `fmis_ofarm_shadow_assessment_v0_1/`: earlier local shadow assessment, used only as reference because it did not run live database queries.
- `outputs/bigquery_data_layer_review_2026-05-10/REVIEW_HANDOFF.md`: metadata starting context, superseded where live checks differ.

## Live BigQuery Findings

Live dataset visibility:

- `bq ls` showed `login-eko-data-layer` is reachable and includes `prod__t_kis__*`, `prod__farming__*`, `prod__openwms__*`, and backup/source datasets.
- INFORMATION_SCHEMA showed 162 prod-style datasets.
- Key LoginEKO operational dataset counts included `prod__farming__t_logineko` with 184 tables, `prod__openwms__t_logineko` with 42, `prod__t_logineko__inventory` with 16, `prod__t_logineko__tasks` with 6, and `prod__t_logineko__work_orders` with 2.
- The `prod__t_kis__*` family is broader for this OFARM slice: operations, scoutings, fields, crops, crop fact zones, materials, equipment, tasks, work orders, traceability, soil, storage, inventory, vehicles, BBCH/crop/EPPO source datasets.

Representative live row counts and freshness:

| Table | Rows | Last modified or max source time |
| --- | ---: | --- |
| `prod__t_kis__fields.dim_field` | 125 | table modified 2026-05-13 12:05:23 |
| `prod__t_kis__scoutings.fact_scouting_observation` | 4 | table modified 2026-05-13 09:26:00; max observation time 2026-03-24 13:28:34.740+00 |
| `prod__t_kis__operations.fact_field_operation_planned` | 1832 | table modified 2026-05-13 12:05:57; 607 planned `APPLICATION` rows |
| `prod__t_kis__operations.fact_field_operation_actual` | 1124 | table modified 2026-05-13 12:05:57; 409 completed `APPLICATION`, 8 aborted `APPLICATION`, 1 in-progress `APPLICATION` |
| `prod__t_kis__crops_fact_zone.fact_crop_zone_planned_operation` | 283 | table modified 2026-05-13 12:06:05 |
| `prod__t_kis__crops_fact_zone.fact_crop_zone_actual_operation` | 1999 | table modified 2026-05-13 12:06:25 |
| `prod__t_kis__materials.dim_material` | 100 | table modified 2026-05-13 12:05:35; max modification timestamp 2026-05-13 08:06:40.388148+00 |
| `prod__t_kis__soil.fact_soil_measurement` | 0 | schema exists; no live rows |

## Mapping Assessment

The field and crop-zone surfaces can partially map to `Field` and `PartialExtent`. They include stable field IDs, UUIDs, source origin, geometry version IDs, WGS84 geography, SCD effective times, area, change author, and changed timestamp.

The scouting surface can partially map to `AgronomicObservationContext`. It has observation UUIDs, observation time, WGS84 point geometry, observation type, EPPO target references, severity, impacted area, image URLs, comments, field geometry, and observer person fields. It does not prove method, threshold source, BBCH crop stage, correction lineage, or evidence custody.

The planned operation surface can partially map to `InterventionIntentPayload`. It separates planned time windows, status, vehicles, implements, persons, crops, materials, material quantities, material units, application rates, and application units. It does not prove recommendation versus prescription authority, delegation, cancellation/supersession lineage, or original payload hash.

The actual operation surface can partially map to `ExecutionRecordPayload`. It exposes actual start/end, coverage, units, fuel, active time, materials, people, vehicles, implements, crops, status, and last-modified timestamp. It does not prove original machine/controller files, DDI mappings, offline sync, accepted consequence decisions, correction history, or disputes.

The material catalogue can partially map to `AgronomicIdentityBinding`, but only as local material identity. It has material UUID, local name, category, type, SKU bridge, base unit, target rate, target rate unit, crop links, crop-variety links, organic flag, active/available flags, and modification timestamp. It does not prove regulatory crop-protection product authorization, active substance, manufacturer/registrant, or label constraints.

The soil measurement table is not ready for `MeasurementEvidence`: the schema exists, but live row count was zero and lab method, accreditation, units, LOD/LOQ, uncertainty, result time, and custody fields were not observed.

## Main Gaps

1. Raw payloads and source file/API references are missing.
2. Correction, supersession, dispute, and late-sync history are not proven.
3. Authority and contractor/applicator evidence are incomplete.
4. Product identity is local-catalogue grade, not regulatory-grade.
5. Projected/current marts could be mistaken for truth unless loss maps and source traces are required.
6. Lab/soil evidence is modeled but not populated.

## Recommended Next Action

Run a narrow adapter discovery spike over `prod__t_kis__*` BigQuery metadata and a small approved row packet for one crop-protection operation chain. Do not start compliance-grade OFARM promotion until the P0 evidence request bundle is supplied.
