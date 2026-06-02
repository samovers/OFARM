# FMIS interoperability investigation v0.1

Date: 2026-05-13  
Status: active supporting implementation evidence  
Change class: implementation/conformance implication  
Authority: does not change active baseline law, accepted RFCs, or active machine-contract schemas

This folder records the first Codex FMIS/machinery/source-surface investigation for OFARM after agronomic Phase AGR-P9.

The investigation found a useful live BigQuery KIS/FM​​IS-like surface for a first adapter spike, but it also confirmed that the visible marts are discovery surfaces only. They must not be treated as OFARM source truth or compliance-grade accepted consequences.

## Folder layout

- `source_report/` — the Codex investigation results, mapping matrix, payload index, evidence requests, and unresolved questions.
- `adapter_spike/` — the redacted candidate operation packet, source-side probe packet, and SQL queries supplied by Codex.
- `OFARM_FMIS_Investigation_Intake_v0_1.md` — OFARM interpretation of the report.
- `OFARM_FMIS_Evidence_Request_List_v0_2.md` — normalized evidence request list for implementers and source-system owners.
- `OFARM_KIS_Adapter_Spike_Plan_v0_1.md` — next implementation-spike plan.
- `OFARM_kis_adapter_spike_candidate_records_v0_1.json` — deterministic fixture draft using the redacted candidate packet.
- `ofarm_kis_adapter_spike_candidate_runner_v0_1.py` — package-local runner for the adapter-spike fixture.
- `OFARM_kis_adapter_spike_candidate_results_v0_1.json` — runner result.

## Boundary

This folder is not a production adapter, not a live promotion engine, and not a wire-level ADAPT / ISOXML / EFDI conformance claim. It is an implementation-discovery and fixture-preparation lane.

## Addendum intake — Logineko entity package

The `source_report/codex_fmis_logineko_entity_package_addendum.md` addendum is included as a source-map aid. It identifies Logineko entity relationships for scouting, planned operations, work orders, task results, work-order checkpoints, material sessions, external identity, and audit/user attribution. It adds source-side checkpoint evidence for the selected candidate but does not unblock promotion.
