# Patch apply guide — AAI-CP1

Generated: 2026-05-16T13:00:00+02:00

## Apply order

1. Apply the five active baseline file edits.
2. Add the CP1 support folder at `04_implementation_and_conformance/controlled_promotion_evidence/agentic_ai_world_model_amendment_v0_1/controlled_promotion/AAI-CP1_ai_facing_release_qualification_gate_v0_1/`.
3. Refresh root metadata, manifest, and material-status inventories.
4. Run `python3 package_meta/tools/validate_repo_hygiene.py`.

## Expected result

- Active baseline law includes the release-qualification gate.
- No draft schema is promoted.
- Repository hygiene passes.
- CP2 remains the next phase for concrete public-surface/result-qualification/trace contracts.
