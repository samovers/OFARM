# 04_implementation_and_conformance

Status: active supporting implementation and conformance material. This folder does not create or override OFARM law.

This folder contains examples, fixtures, conformance suites, implementation notes, pilots, runtime/support material, draft/review snapshots, spikes, SDK/reference-platform candidates, and controlled-promotion evidence. It also contains machine-contract examples and fixtures moved out of `03_machine_contracts/`:

- `examples/machine_contracts/`
- `fixtures/machine_contracts/`

## Current navigation

Use these indexes in order:

1. `IMPLEMENTATION_SUBFOLDER_INDEX.json` for top-level subfolder status, class, and README coverage.
2. `IMPLEMENTATION_LANE_INDEX.json` for file-level path, byte-size, and SHA-256 navigation.
3. `NON_ACTIVE_SCHEMA_COPY_INDEX.json` for implementation/support JSON files that share basenames with active machine-contract schemas.
4. `examples_and_fixtures/examples/EXAMPLE_INDEX.json` and `examples_and_fixtures/fixtures/FIXTURE_INDEX.json` for Phase 8 example/fixture validation and coverage.
5. `package_meta/generated/schema_example_map.json` or `03_machine_contracts/EXAMPLE_SCHEMA_MAP.json` to connect examples back to source schemas.

For the agentic-AI controlled-promotion lifecycle, start here:

- `controlled_promotion_evidence/agentic_ai_world_model_amendment_v0_1/controlled_promotion/README.md`
- `controlled_promotion_evidence/agentic_ai_world_model_amendment_v0_1/controlled_promotion/PROMOTION_INDEX.json`

Current controlled-promotion endpoint: `AAI-CP10`. CP10 updates only active baseline readiness/hostile-review memo posture and adds no accepted RFCs, companion artifacts, or machine-contract schemas.

## Selection rules

- Use active machine-contract schemas only from `03_machine_contracts/` and its currentness maps.
- Treat `draft_machine_contracts/`, `review_copies_not_active/`, `experimental_machine_contracts/`, examples, fixtures, and spike folders as non-default support unless an active authority file explicitly promotes them.
- Treat `historical/`, `historical_outputs/`, and `historical_patches/` as audit/context material, not current implementation guidance.
- Do not infer production readiness, full runtime AI-agent readiness, world-model readiness, farmer UX readiness, live pilot validation, legal advice, or external-standard readiness from this folder.

## Default-search posture

Historical, spike, draft, review-copy, and non-active schema-copy material is excluded from default search. Use `04_implementation_and_conformance/IMPLEMENTATION_SUBFOLDER_INDEX.json` and `package_meta/repository_steward_completion_batch2_1_2026_05_20/DEFAULT_SEARCH_PROFILE.json` for lane/search-default status.


## CP14 conformance currentness note — 2026-05-30

The current CP14 farm-to-farm intelligence boundary conformance runner is `04_implementation_and_conformance/conformance_runners/farm_to_farm_intelligence_boundary_conformance/ofarm_cp14_phase7_2_conformance_runner.py`. Earlier CP14 runners are superseded/non-current.
