# Wave 11 same-standard bridge-pack patch bundle v0.1

Date: 2026-04-11  
Status: active supporting implementation artifact  
Scope: repo-relative patch bundle for the Wave 11 same-standard reversible bridge-pack conformance step

---

## What this patch does

This patch adds the next bounded post-Wave-10 hardening step.
It does **not** change:
- `00_active_baseline/`
- `01_companion_artifacts/`
- `02_accepted_rfcs/`

It does change:
- `03_machine_contracts/` by adding **draft** ADAPT and ISOXML export bridge examples
- `04_implementation_and_conformance/` by adding same-standard reverse-pair scans, candidate-pair records, declared-subset round-trip records, conflict records, an updated contract-validation result, and conformance-matrix/seed-set updates

## Main added artifacts

### Machine-contract additions
- `OFARM_Bridge_Pack_Draft_Fixtures_v0_1.md`
- `OFARM_MappingCoverageStatement_example_adapt_export_bridge_draft_v0_1.json`
- `OFARM_LossMap_example_adapt_export_bridge_draft_v0_1.json`
- `OFARM_RuntimeSurfaceContract_example_adapt_bridge_export_draft_v0_1.json`
- `OFARM_MappingCoverageStatement_example_isoxml_export_bridge_draft_v0_1.json`
- `OFARM_LossMap_example_isoxml_export_bridge_draft_v0_1.json`
- `OFARM_RuntimeSurfaceContract_example_isoxml_bridge_export_draft_v0_1.json`

### Implementation/conformance additions
- `OFARM_Same_Standard_Reversible_Bridge_Pack_Fixtures_v0_1.md`
- `ofarm_same_standard_reversible_bridge_pack_runner_v0_1.py`
- `OFARM_same_standard_reverse_pair_scan_v0_2.json`
- `OFARM_same_standard_bridge_pack_candidate_pairs_v0_1.json`
- `OFARM_same_standard_bridge_pack_round_trip_records_v0_1.json`
- `OFARM_same_standard_bridge_pack_conflict_records_v0_1.json`
- `OFARM_same_standard_reversible_bridge_pack_results_v0_1.json`
- `OFARM_machine_contract_validation_results_v0_8.json`

## Why this wave exists

Wave 10 still left one explicit conformance gap open: same-standard reversible bridge-pack proof.
This patch closes that gap at the declared-surface level by adding draft same-standard export bridge examples for ADAPT and ISOXML, then exercising them through declared-subset round-trip and conflict suites.

## Remaining gap after this patch

The package still does **not** ship:
- deployment-collected same-standard runtime telemetry
- active production bridge-pack promotion for ADAPT or ISOXML
- broad reversible claims outside the declared draft subsets
