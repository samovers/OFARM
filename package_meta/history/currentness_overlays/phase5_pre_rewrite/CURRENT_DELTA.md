# Current delta
## 2026-05-21 Final repository-steward human-index closure

Changed:

- refreshed `06_active_supporting_research/CURRENT_SOURCE_INPUTS.md` from `SOURCE_INPUT_INDEX.json`; current counts are 22 records and 2 duplicate checksum groups;
- refreshed `TRACEABILITY_INDEX.md` from `TRACEABILITY_INDEX.json`; status cells now match the canonical JSON source;
- extended `package_meta/tools/check_repository_steward_guardrails.py` to catch those human-view currentness regressions.

Not changed:

- no active baseline semantic law was rewritten;
- no accepted RFC, companion artifact, or machine-contract schema was added;
- no review-held, legacy, historical, spike, or draft artifact was promoted.

## Batch 2.1 schema-reference closure

- Added `package_meta/repository_steward_completion_batch2_2026_05_20/FOLDER_STATUS_CANONICAL_SCHEMA_v1_1.json` and repointed all `folder.status.json` files to this existing schema.
- Hardened `package_meta/tools/check_repository_steward_guardrails.py` so missing `folderStatusSchema` references cannot pass validation.


Status: ROOT_PACKAGE_METADATA
Updated: 2026-05-20T16:30:00+02:00

Current package: `OFARM2_2026-05-17_agentic_ai_controlled_promotion_cp10_v0_1`.

## 2026-05-20 Repository Steward Completion Batch 2.1 currentness patch

Changed:

- added `package_meta/repository_steward_completion_batch2_1_2026_05_20/` as the current repository-steward currentness/control-surface folder;
- updated `README.md`, `CURRENT_ACTIVE_ENTRYPOINT.md`, `CURRENT_ACTIVE_ENTRYPOINT.json`, `AGENTS.md`, `llms.txt`, `DEVELOPMENT_HANDOVER.md`, `package_meta/README.md`, and validation docs to point to Batch 2.1 as current;
- kept Batch 2 as the structural completion evidence for physical review archive movement, schema-copy renames, and the physical `04_implementation_and_conformance/` lane split;
- marked Batch 1 remediation as historical/superseded lineage rather than the current control surface;
- removed `reviewed_*` from the current active-entrypoint read order and represented review holding through `archive/review_holding/` plus `REVIEW_HOLDING_INDEX.json`;
- updated the unresolved debt register so the prior same-basename schema-copy repository debt is closed by Batch 2;
- extended repository-steward guardrails to catch stale Batch 1-as-current pointers and stale review-holding cues.

Not changed:

- no active baseline semantic law was rewritten;
- no accepted RFC, companion artifact, or machine-contract schema was added;
- no review-held, legacy, historical, spike, or draft artifact was promoted;
- CP10 claim limits remain unchanged.

## 2026-05-20 Repository Steward Completion Batch 2 structural cleanup

Changed:

- root `reviewed_*` folders were archived into `archive/review_holding/OFARM_review_holding_snapshots_2026_05_20.zip`;
- `04_implementation_and_conformance/` was physically split into controlled lane folders;
- 77 non-active implementation/conformance schema copies were physically renamed with `__non_active_copy.json`;
- generated duplicate maps self-mark with `derivedFrom` and `doNotCiteAsIndependentSource`;
- legacy snake_case compatibility keys were removed from `folder.status.json` files.

## 2026-05-20 Repository Steward Batch 1 remediation history

Batch 1 added the first repository-steward remediation control surface under `package_meta/repository_steward_remediation_2026_05_20/`, canonical metadata fields, default-search quarantine, guardrails, and improved decision/traceability/source-input navigation. Batch 1 is now superseded/amended by Batch 2 and Batch 2.1 for current completion claims.

## Prior repository-currentness cleanup history

- 2026-05-18 batches 1-11 normalized root, active baseline, accepted RFC, companion, machine-contract, implementation/conformance, example/fixture, research, handoff, and review-holding navigation/currentness.
- 2026-05-19 phases 12-15 added legacy archive hygiene, package metadata/generated-currentness enforcement, cross-reference scan enforcement, final validation, release notes, and unresolved-debt closeout.

See `CURRENT_PACKAGE_CHANGELOG.md`, `package_meta/repository_steward_completion_batch2_1_2026_05_20/OFARM_repository_steward_completion_batch2_1_currentness_patch_v0_1.json`, and `package_meta/repository_steward_completion_batch2_2026_05_20/OFARM_repository_steward_completion_batch2_report_v0_1.json` for detail.


## 2026-05-28 — CP11 Sustainable Autonomous Farming Charter merge delta

Current package: `OFARM2_2026-05-28_cp11_sustainable_autonomous_farming_charter_merged_v0_1`.

CP11 merges the Sustainable Autonomous Farming Charter as a controlled baseline/RFC/companion/conformance amendment. CP11 machine contracts remain draft/non-default and are not current/default active machine contracts.

## 2026-05-28 — CP12 Cyber-Physical Mission Envelope merge delta

CP12 merges the Cyber-Physical Mission Envelope as a controlled baseline/RFC/companion/conformance amendment. CP12 machine contracts remain draft/non-default and are not current/default active machine contracts.

Delta: CP12 adds mission-envelope law for intent/candidate/plan/preflight/dispatch/command/acknowledgement/telemetry/receipt/verification/accepted consequence separation; mission authority actions; geofence/no-go-zone/geometry and execution-window posture; command integrity; emergency stop, human override, local fallback, lost-link and remote takeover posture; telemetry and execution-receipt truth boundaries; mission output qualification; and conformance fixtures.

Non-claims: no production robot/machine readiness, autonomous field-operation readiness, safety certification, legal advice, vendor protocol completeness, fleet optimisation law, CP13/CP14/CP15 readiness, or livestock-specific mission law.
