# OFARM draft slotting map v0.1

Date: 2026-04-14  
Scope: exact placement of the staple-crop pre-implementation strengthening drafts into the current OFARM 2 migrated project structure

## 1. Placement rule

Use the project authority model exactly as intended:

- `00_active_baseline/` = baseline law only
- `01_companion_artifacts/` = active normative support that clarifies or operationalizes existing law without reopening baseline architecture
- `02_accepted_rfcs/` = accepted extension law only
- `03_machine_contracts/` = machine-readable schemas/examples/contracts only
- `04_implementation_and_conformance/` = implementation, fixtures, runners, validation, telemetry, conformance hardening
- `05_project_handoff_and_prompts/` = prompts, handoff, orchestration, rerun instructions
- `06_active_supporting_research/` = research synthesis, stress tests, design-pressure memos, curated development input

## 2. Recommended slotting

### Promote into active companion support

Place this file in `01_companion_artifacts/`:

- `01_companion_artifacts/OFARM_Evidence_Quality_and_Promotion_Handling_Note_v0_1.md`

Reason:
- this is the only strengthening artifact written as a proposed active companion artifact
- it clarifies evidence-quality and late-evidence handling without reopening RC2.1 law
- it belongs beside:
  - `OFARM_Event_Grammar_and_Commit_Matrix_v0_1.md`
  - `OFARM_Evidence_Sufficiency_and_Attestation_Policy_v0_1.md`
  - `OFARM_Compiled_Output_and_Passport_Taxonomy_Note_v0_1.md`

### Place implementation/conformance material in a dedicated hardening subfolder

Create:

- `04_implementation_and_conformance/implementation_notes/ofarm_staple_crop_scenario_hardening_v0_1/`

Place these files there:

- `04_implementation_and_conformance/implementation_notes/ofarm_staple_crop_scenario_hardening_v0_1/OFARM_Staple_Crop_Campaign_Fixture_Library_v0_1.md`
- `04_implementation_and_conformance/implementation_notes/ofarm_staple_crop_scenario_hardening_v0_1/OFARM_High_Consequence_Freshness_Profiles_for_Staple_Crop_Campaigns_v0_1.md`
- `04_implementation_and_conformance/implementation_notes/ofarm_staple_crop_scenario_hardening_v0_1/OFARM_Campaign_Query_and_Retrieval_Regression_Spec_v0_1.md`
- `04_implementation_and_conformance/implementation_notes/ofarm_staple_crop_scenario_hardening_v0_1/OFARM_Deployment_Evidence_Obligations_for_Hard_Scenarios_v0_1.md`
- `04_implementation_and_conformance/implementation_notes/ofarm_staple_crop_scenario_hardening_v0_1/OFARM_staple_crop_strengthening_action_matrix_v0_1.csv`

Rename on import:
- `OFARM_strengthening_action_matrix_2026-04-14.csv`
  -> `OFARM_staple_crop_strengthening_action_matrix_v0_1.csv`

Reason:
- these are implementation and conformance obligations, not new model law
- they fit the existing style of fixture libraries, runtime hardening memos, runner inputs, and validation assets
- the dedicated subfolder keeps campaign hardening coherent instead of scattering related files through an already dense `04_implementation_and_conformance/`

### Keep the control memo in supporting research

Place this file in `06_active_supporting_research/`:

- `06_active_supporting_research/syntheses/OFARM_pre_implementation_strengthening_pass_staple_crop_v0_1.md`

Reason:
- it is the synthesis memo explaining why these additions exist and how they should be interpreted
- it should inform development, but should not outrank active law or conformance artifacts

### Put the hostile rerun prompt in handoff/prompts

Place this file in `05_project_handoff_and_prompts/`:

- `05_project_handoff_and_prompts/prompts/OFARM_post_strengthening_stress_test_prompt_v0_2.md`

Reason:
- it is an orchestration prompt, not semantic law or implementation evidence
- it should reference folder-qualified paths to the slotted strengthening artifacts

## 3. Optional placement for the earlier research outputs

If you want the whole scenario chain preserved inside the project, also place:

- `06_active_supporting_research/syntheses/OFARM_staple_crop_stress_test_report_v0_1.md`
- `06_active_supporting_research/syntheses/OFARM_staple_crop_scenario_stress_test_matrix_v0_1.csv`

Rename on import:
- `OFARM_staple_crop_stress_test_report_2026-04-14.md`
  -> `OFARM_staple_crop_stress_test_report_v0_1.md`
- `OFARM_staple_crop_scenario_stress_test_matrix_2026-04-14.csv`
  -> `OFARM_staple_crop_scenario_stress_test_matrix_v0_1.csv`

These are research inputs and should stay in `06_active_supporting_research/`, not in `04_implementation_and_conformance/`.

## 4. Do not slot here yet

Do **not** place any of the current drafts in:

- `00_active_baseline/`
- `02_accepted_rfcs/`
- `03_machine_contracts/`

Reason:
- no baseline rewrite is being proposed
- no accepted RFC is being proposed in this pass
- the current outputs are prose specs and fixture directions, not yet machine-readable contracts

## 5. Immediate meta updates after placement

After copying the files, update these package-meta assets:

- `MANIFEST.csv`
- `MATERIAL_STATUS.csv`
- `MATERIAL_STATUS.json`

Recommended status classes:

- `01_companion_artifacts/OFARM_Evidence_Quality_and_Promotion_Handling_Note_v0_1.md`
  - `ACTIVE_SUBSTANCE`
- everything under `04_implementation_and_conformance/implementation_notes/ofarm_staple_crop_scenario_hardening_v0_1/`
  - `ACTIVE_SUPPORTING_IMPLEMENTATION`
- `06_active_supporting_research/syntheses/OFARM_pre_implementation_strengthening_pass_staple_crop_v0_1.md`
  - `ACTIVE_SUPPORTING_RESEARCH`
- `05_project_handoff_and_prompts/prompts/OFARM_post_strengthening_stress_test_prompt_v0_2.md`
  - `ACTIVE_SUPPORTING_CONTEXT`

If you also import the earlier stress-test report and matrix into `06_active_supporting_research/`, mark them `ACTIVE_SUPPORTING_RESEARCH`.

## 6. Prompt/index update

Also update:

- `05_project_handoff_and_prompts/prompts/OFARM_Deep_Research_Prompts_index_v0_1.md`

Add an entry for:

- `OFARM_post_strengthening_stress_test_prompt_v0_2.md`

## 7. Next machine-contract follow-on

After these files are slotted, the next controlled step is not another prose memo. It is a selective conversion of the `04_implementation_and_conformance/` obligations into new or extended machine contracts in `03_machine_contracts/`, especially for:

- degraded evidence reason codes / evidence-posture fields
- freshness-trigger examples for storage and filing flows
- campaign query regression examples
- emitted deployment trace record schemas

That is a second step, not part of the initial slotting.

## 8. Copy-ready shell sketch

```bash
mkdir -p 04_implementation_and_conformance/implementation_notes/ofarm_staple_crop_scenario_hardening_v0_1

cp /path/to/OFARM_Evidence_Quality_and_Promotion_Handling_Note_v0_1.md \
  01_companion_artifacts/

cp /path/to/OFARM_Staple_Crop_Campaign_Fixture_Library_v0_1.md \
  04_implementation_and_conformance/implementation_notes/ofarm_staple_crop_scenario_hardening_v0_1/
cp /path/to/OFARM_High_Consequence_Freshness_Profiles_for_Staple_Crop_Campaigns_v0_1.md \
  04_implementation_and_conformance/implementation_notes/ofarm_staple_crop_scenario_hardening_v0_1/
cp /path/to/OFARM_Campaign_Query_and_Retrieval_Regression_Spec_v0_1.md \
  04_implementation_and_conformance/implementation_notes/ofarm_staple_crop_scenario_hardening_v0_1/
cp /path/to/OFARM_Deployment_Evidence_Obligations_for_Hard_Scenarios_v0_1.md \
  04_implementation_and_conformance/implementation_notes/ofarm_staple_crop_scenario_hardening_v0_1/
cp /path/to/OFARM_strengthening_action_matrix_2026-04-14.csv \
  04_implementation_and_conformance/implementation_notes/ofarm_staple_crop_scenario_hardening_v0_1/OFARM_staple_crop_strengthening_action_matrix_v0_1.csv

cp /path/to/OFARM_pre_implementation_strengthening_pass_staple_crop_v0_1.md \
  06_active_supporting_research/

cp /path/to/OFARM_post_strengthening_stress_test_prompt_v0_2.md \
  05_project_handoff_and_prompts/
```
