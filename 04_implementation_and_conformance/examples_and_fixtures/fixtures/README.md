# 04 implementation fixtures

Status: active supporting fixture material only. This folder does not create or override OFARM law.

Current package: `OFARM2_2026-05-17_agentic_ai_controlled_promotion_cp10_v0_1`  
Latest controlled-promotion endpoint: `AAI-CP10`

Use fixtures as conformance and test inputs only. A fixture is not an active schema, current state source, compliance decision, production-readiness claim, or external-standard-readiness claim.

Current fixture entrypoints:

- `FIXTURE_INDEX.json`
- `FIXTURE_INDEX.md`
- `machine_contracts/README.md`
- `../../03_machine_contracts/EXAMPLE_SCHEMA_MAP.json`
- `../../package_meta/generated/schema_example_map.json`

Phase 8 validation posture:

- fixture records indexed: 14
- JSON fixture sets checked: 1
- missing declared fixture/example refs: 0
- fixture subfolders have local README and `folder.status.json` coverage

Rules:

- Fixtures must stay tied to an explicit runner, schema, or example map.
- Fixtures that target draft or non-default scenarios remain non-default support material.
- Historical or spike fixtures must not be treated as active runtime defaults.
