# Patch apply guide — Phase 10 final harmonization

## Apply mode

This phase is supporting-only. It adds final harmonization and implementer handoff files under:

`04_implementation_and_conformance/controlled_promotion_evidence/agentic_ai_world_model_amendment_v0_1/phase10_final_harmonization_implementer_handoff_v0_1/`

## Active folder impact

Phase 10 itself does not change active folders.

The cumulative working copy also includes the Phase AAI-P1 active-baseline safety clarification.

## Validation expectation

After applying, run JSON syntax validation across the amendment folder and confirm:

- Phase 10 folder exists.
- Phase AAI-P1 active-baseline markers exist in the five baseline files.
- Phase 3-7 candidate objects are not present in active `03_machine_contracts/` unless deliberately promoted later.
- Runtime conformance remains `NOT_RUN_NO_IMPLEMENTATION`.
