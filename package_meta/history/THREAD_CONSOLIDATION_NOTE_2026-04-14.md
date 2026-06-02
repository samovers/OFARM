# Thread consolidation note — staple-crop stress-test and strengthening pass

Status: historical package assembly note
Current package entrypoint: `../../README.md`
Current change trail: `../../CURRENT_PACKAGE_CHANGELOG.md`


Date: 2026-04-14  
Scope: records the consolidation of the latest OFARM migration package with the final staple-crop stress-test and pre-implementation strengthening outputs produced in this thread.

## Source baseline used

This package was built from:

- `OFARM2_project_migration_seed_v0_6-4_with_economic_intelligence_consolidated_v0_1.zip`

The source package contents were unpacked into a clean repo tree without the `__MACOSX/` sidecar entries, then the thread artifacts were slotted into repo-relative locations.

## Added or slotted materials

### `01_companion_artifacts/`
- `OFARM_Evidence_Quality_and_Promotion_Handling_Note_v0_1.md`

### `04_implementation_and_conformance/implementation_notes/ofarm_staple_crop_scenario_hardening_v0_1/`
- `README.md`
- `OFARM_Staple_Crop_Campaign_Fixture_Library_v0_1.md`
- `OFARM_High_Consequence_Freshness_Profiles_for_Staple_Crop_Campaigns_v0_1.md`
- `OFARM_Campaign_Query_and_Retrieval_Regression_Spec_v0_1.md`
- `OFARM_Deployment_Evidence_Obligations_for_Hard_Scenarios_v0_1.md`
- `OFARM_staple_crop_strengthening_action_matrix_v0_1.csv`

### `05_project_handoff_and_prompts/`
- `OFARM_draft_slotting_map_v0_1.md`
- `OFARM_post_strengthening_stress_test_prompt_v0_2.md`
- `OFARM_Deep_Research_Prompts_index_v0_2.md`

### `06_active_supporting_research/`
- `OFARM_pre_implementation_strengthening_pass_staple_crop_v0_1.md`
- `OFARM_staple_crop_stress_test_report_v0_1.md`
- `OFARM_staple_crop_scenario_stress_test_matrix_v0_1.csv`

## Normalized-on-import filename changes

To keep the repo naming style coherent, these thread outputs were normalized on import:

- `OFARM_strengthening_action_matrix_2026-04-14.csv` -> `04_implementation_and_conformance/implementation_notes/ofarm_staple_crop_scenario_hardening_v0_1/OFARM_staple_crop_strengthening_action_matrix_v0_1.csv`
- `OFARM_staple_crop_stress_test_report_2026-04-14.md` -> `06_active_supporting_research/syntheses/OFARM_staple_crop_stress_test_report_v0_1.md`
- `OFARM_staple_crop_scenario_stress_test_matrix_2026-04-14.csv` -> `06_active_supporting_research/syntheses/OFARM_staple_crop_scenario_stress_test_matrix_v0_1.csv`

## Metadata updates

The package metadata files were updated to register the added materials:

- `MANIFEST.csv`
- `MATERIAL_STATUS.csv`
- `MATERIAL_STATUS.json`

## Intentionally not embedded as nested artifacts

The following thread-generated package artifacts were not re-embedded inside this consolidated package, because they are superseded by this repo snapshot and would only add nested-zip redundancy:

- `OFARM_preimplementation_strengthening_packet_2026-04-14.zip`
- `OFARM_staple_crop_strengthening_repo_relative_overlay_v0_1.zip`

Also omitted as superseded:

- `OFARM_post_strengthening_stress_test_prompt_v0_1.md`

## Interpretation rule

This consolidation does not change the authority model of the source package.
The new materials inherit their authority from the folders they are placed in:

- companion artifact = active normative support
- implementation/conformance subfolder = active supporting implementation
- handoff/prompts = active supporting context
- supporting research = active supporting research
- this note = package metadata only
