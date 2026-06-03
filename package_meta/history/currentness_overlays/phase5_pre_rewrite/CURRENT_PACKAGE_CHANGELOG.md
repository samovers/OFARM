# Current package changelog

## 2026-05-30 — CP15 final currentness normalization

- Normalized machine-readable currentness after the CP15 steward-remediated merge.
- Updated `CURRENT_ACTIVE_ENTRYPOINT.json`, package metadata, generated indexes, manifests, and currentness fields so CP15 is the unambiguous latest controlled amendment endpoint.
- No CP11, CP12, CP13, CP14, or CP15 semantic law changed.
- No draft/non-default machine contracts were promoted to current/default.

Package: `OFARM2_2026-05-30_cp15_agentic_software_delivery_model_deployment_governance_merged_v0_2_final_currentness_normalized`

## 2026-05-28 — CP12 Cyber-Physical Mission Envelope merge

- Merged CP12 as a controlled amendment candidate.
- Added `02_accepted_rfcs/OFARM_Cyber_Physical_Mission_Envelope_RFC_v0_1.md`.
- Added CP12 authority, event-grammar, and pack-surface RFC addenda.
- Added `01_companion_artifacts/OFARM_Cyber_Physical_Mission_Envelope_and_Safety_Policy_v0_1.md`.
- Added CP12 draft/non-default machine contracts and conformance runner/fixtures.
- Applied CP12 controlled addenda to the five active baseline files.
- Preserved non-claims: no production robot/machine readiness, no legal/safety certification, no autonomous field-operation readiness, no vendor protocol conformance, no fleet optimisation law, no livestock-specific mission law, and no CP13/CP14/CP15 readiness.

Package: `OFARM2_2026-05-28_cp12_cyber_physical_mission_envelope_merged_v0_1`


## 2026-05-28 — CP11 Sustainable Autonomous Farming Charter merge

- Merged CP11 as a controlled Sustainable Autonomous Farming Charter amendment.
- Added controlled baseline addenda, accepted RFC and addenda, companion policy, draft/non-default schemas, and conformance fixtures.
- Preserved non-claims: no production readiness, no current/default CP11 machine-contract promotion, no robot/machine execution readiness, no autonomous compliance decisioning, no certification readiness, no livestock expansion, and no CP12/CP13/CP14/CP15 readiness.

Package: `OFARM2_2026-05-28_cp11_sustainable_autonomous_farming_charter_merged_v0_1`

# Current package changelog
## 2026-05-21 — Final repository-steward human-index closure

- Refreshed the human current-source-input summary from the machine source-input index; current counts are 22 records and 2 duplicate checksum groups.
- Refreshed the human traceability table from the canonical traceability index.
- Added guardrail coverage for source-input summary count drift and traceability status drift.

No active OFARM semantic law was changed.

## Batch 2.1 schema-reference closure

- Added `package_meta/repository_steward_completion_batch2_2026_05_20/FOLDER_STATUS_CANONICAL_SCHEMA_v1_1.json` and repointed all `folder.status.json` files to this existing schema.
- Hardened `package_meta/tools/check_repository_steward_guardrails.py` so missing `folderStatusSchema` references cannot pass validation.


Package: `OFARM2_2026-05-17_agentic_ai_controlled_promotion_cp10_v0_1`

## 2026-05-20 — Repository Steward Completion Batch 2.1 currentness patch

- Added the current repository-steward currentness/control-surface folder under `package_meta/repository_steward_completion_batch2_1_2026_05_20/`.
- Updated root entrypoints and agent/handover docs so Batch 2.1 is current, Batch 2 is structural completion evidence, and Batch 1 is historical/superseded remediation lineage.
- Removed `reviewed_*` from the current active-entrypoint read order and represented review holding through `archive/review_holding/` plus `REVIEW_HOLDING_INDEX.json`.
- Updated default-search, derived-index, validation-suite, handover-gate, and generated-map policy pointers to the current Batch 2.1 folder.
- Closed stale repository debt wording for same-basename active-schema copies, which Batch 2 physically resolved.
- Extended guardrails to catch stale Batch 1-as-current and stale `reviewed_*` read-order regressions.

No active OFARM semantic law was changed.

## 2026-05-20 — Repository Steward Completion Batch 2 structural cleanup

- Archived root `reviewed_*` snapshots into `archive/review_holding/OFARM_review_holding_snapshots_2026_05_20.zip`.
- Physically split `04_implementation_and_conformance/` into controlled lane folders.
- Physically renamed 77 non-active implementation/conformance schema copies with `__non_active_copy.json`.
- Added direct derived-source markers to generated duplicate maps.
- Removed legacy snake_case compatibility keys from `folder.status.json` files.

No active OFARM semantic law was changed.

## 2026-05-20 — Repository Steward Batch 1 remediation history

- Added a repository-steward remediation control surface under `package_meta/repository_steward_remediation_2026_05_20/`.
- Added canonical folder-status schema guidance and compatibility-preserving canonical fields to all `folder.status.json` files.
- Added material-status overlays distinguishing folder/file status from active-law artifact status.
- Excluded historical, spike, draft, review-held, legacy, and non-active schema-copy material from default search policy.
- Added quarantine policies for non-active schema copies and review-held material.
- Updated validation instructions across root README, agent instructions, handover, tools, and validators documentation.
- Added `check_repository_steward_guardrails.py` and `run_repository_validation_suite.py`.
- Renamed the generated-currentness workflow file to `.github/workflows/validate_generated_currentness.yml`.
- Regenerated human-facing decision and traceability indexes.
- Added `06_active_supporting_research/CURRENT_SOURCE_INPUTS.md`.
- Refreshed final-validation summary counts from the current repository scan.

Batch 1 is now historical/superseded remediation lineage for completion-claim purposes.

## 2026-05-19 — Repository-currentness cleanup history

- Phase 12: legacy-reference archive hygiene.
- Phase 13: package metadata and generated-index currentness enforcement.
- Phase 14: cross-reference, stale-currentness, duplicate-basename, and schema-copy scan enforcement.
- Phase 15: final validation, release notes, cleanup report, and unresolved-debt closeout.

## 2026-05-18 — Batches 1-11 repository currentness cleanup

- Normalized root, active baseline, accepted RFC, companion artifact, machine-contract, implementation/conformance, example/fixture, research, handoff, and review-holding navigation/currentness.
- Preserved active authority order and CP10 claim limits.

## Active-law non-promotion note

Cleanup, validation, index, package metadata, and repository-steward files do not create active OFARM law unless explicitly promoted by the active authority chain.

## 2026-05-28 — CP12 Cyber-Physical Mission Envelope merge

- Merged CP12 as a controlled Cyber-Physical Mission Envelope amendment.
- Added accepted RFC `OFARM_Cyber_Physical_Mission_Envelope_RFC_v0_1.md`.
- Added authority-action, event-grammar, and pack-merge CP12 addenda.
- Added companion policy `OFARM_Cyber_Physical_Mission_Envelope_and_Safety_Policy_v0_1.md`.
- Added draft/non-default cyber-physical mission machine contracts and conformance runner/fixtures.
- Preserved non-claims: no production robot/machine readiness, autonomous field-operation readiness, legal or safety certification, fleet optimisation, vendor protocol completeness, CP13/CP14/CP15 readiness, or livestock-specific mission law.

## CP12 steward remediation — 2026-05-28

Repository currentness, root overlay, manifest, generated-index, and validation hygiene remediated for `OFARM2_2026-05-28_cp12_cyber_physical_mission_envelope_merged_v0_2_steward_remediated`. No new CP12 law.
