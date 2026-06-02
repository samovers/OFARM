# Patch apply guide — AAI-CP0 controlled promotion start

Generated: 2026-05-16T12:00:00+02:00

## What this patch adds

A supporting implementation/conformance folder:

`04_implementation_and_conformance/controlled_promotion_evidence/agentic_ai_world_model_amendment_v0_1/controlled_promotion/AAI-CP0_amendment_control_reviewer_normalization_v0_1/`

It also updates package metadata files so the repository manifest and material-status inventory remain current.

## What this patch does not do

- It does not edit `00_active_baseline/`.
- It does not edit `01_companion_artifacts/`.
- It does not edit `02_accepted_rfcs/`.
- It does not edit `03_machine_contracts/`.
- It does not promote AAI-P2 through AAI-P10.
- It does not claim runtime readiness, two-agent compatibility, production readiness, external-standard readiness, or autonomous compliance decisioning.

## Apply sequence

1. Copy the CP0 folder into `04_implementation_and_conformance/controlled_promotion_evidence/agentic_ai_world_model_amendment_v0_1/controlled_promotion/`.
2. Update `CURRENT_DELTA.md` with the CP0 supporting-control addition.
3. Regenerate `MANIFEST.csv`, `MATERIAL_STATUS.csv`, and `MATERIAL_STATUS.json`.
4. Run `package_meta/tools/validate_repo_hygiene.py`.
5. Begin CP1 only if validation passes.
