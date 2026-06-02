# Consolidation validation results — 2026-05-14

Overall: `PASS`

## Validation checks

- `machine_contract_runner_v0_20_execution` — `PASS`
- `json_parse` — `PASS`
- `active_schema_meta_validation` — `PASS`
- `schema_example_negative_reference_runner_results` — `PASS`
- `active_authority_unchanged_from_base` — `PASS`
- `manifest_currentness` — `PASS`
- `material_status_currentness` — `PASS`
- `package_hygiene` — `PASS`
- `non_claims` — `PASS`
- `conflict_ledger_presence` — `PASS`

## Machine-contract runner summary

- Runner execution: `PASS`
- Runner reported overall: `PASS`
- Schemas validated by runner: `74`
- Positive examples validated: `370`
- Negative cases checked: `74`; unexpected passes: `0`
- Package-local resolvable refs checked: `714`
- Broken-reference cases checked: `20`; unexpected passes: `0`

## Additional consolidation checks

- JSON files parsed: `2533`
- Active schema meta-validation files checked: `74`
- Manifest rows checked: `4347`
- Material-status rows checked: `4345`
- Conflict ledger conflicts recorded: `120`
- Conflict classes: `{"authority": 17, "currentness": 34, "semantic": 41, "structural": 22, "textual": 2, "validation": 4}`

## Active authority equality check

- `00_active_baseline` — files `5`, added `0`, removed `0`, modified `0`
- `01_companion_artifacts` — files `13`, added `0`, removed `0`, modified `0`
- `02_accepted_rfcs` — files `36`, added `0`, removed `0`, modified `0`
- `03_machine_contracts` — files `458`, added `0`, removed `0`, modified `0`

## Currentness note

`MANIFEST.csv` excludes itself and the final validation result files to avoid self-referential hash cycles. `MATERIAL_STATUS` excludes generated currentness/validation files listed in its `currentnessExclusions`. External deliverable checksums cover the final package artifacts.

## Non-claims

This validation does not establish live pilot evidence, source-owner evidence, production readiness, standards readiness, or baseline harmonization.
