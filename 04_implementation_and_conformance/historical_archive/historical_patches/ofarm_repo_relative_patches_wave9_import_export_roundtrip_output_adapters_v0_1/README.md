# OFARM wave 9 import/export round-trip and output-adapter patch v0.1

Date: 2026-04-11  
Status: active supporting implementation patch bundle

## Purpose

This patch adds the next post-amendment proof/hardening slice after Wave 8.
It keeps all changes inside `04_implementation_and_conformance/` plus package bookkeeping updates and does not amend baseline law, accepted RFCs, companion policy, or machine-contract substance.

## What is included

- `OFARM_Import_Export_RoundTrip_and_Output_Adapter_Fixtures_v0_1.md`
- `ofarm_import_export_roundtrip_and_output_adapter_runner_v0_1.py`
- `OFARM_import_export_path_gate_logs_v0_1.json`
- `OFARM_mapping_round_trip_records_v0_1.json`
- `OFARM_output_adapter_trace_back_records_v0_1.json`
- `OFARM_import_export_roundtrip_and_output_adapter_results_v0_1.json`
- `ofarm_import_export_roundtrip_output_adapter_fixtures_v0_1/*.json`
- updated `OFARM_conformance_coverage_matrix_v0_1.md`
- updated `OFARM_conformance_seed_set_v0_1.md`
- manifest/status refresh

## What changed functionally

This wave adds:
- runtime-shaped ADAPT and ISOXML import boundary paths that prove conservative promotion posture at the gate layer
- a starter declared-surface round-trip feasibility suite for ADAPT import, ISOXML import, and NGSI-LD export
- output-adapter trace-back records for live passport export, frozen dossier packaging, and frozen submission filing

## Validation posture

The new runner emits `PASS_WITH_LIMITATIONS` intentionally.
That is the correct posture for this wave because the package still ships one-way mapping surfaces and replay-shaped evidence rather than executor-native ingest/export telemetry.

## Intended use

Apply this patch on top of the Wave 8 package when continuing post-amendment proof/hardening work.
The next sensible follow-on is executor-produced import/export telemetry, richer partner-specific runtime surfaces, and same-standard reversible bridge-pack round-trip suites.
