
# OFARM repository-steward Completion Batch 2.1 currentness patch

Generated: 2026-05-20T16:30:00+02:00

Status: package metadata only. No active OFARM law changed.

This narrow patch follows Batch 2 structural completion and fixes remaining currentness/documentation drift.

## What changed

- Root README and current-entrypoint files now point to Batch 2.1 as the current repository-steward currentness layer.
- Batch 2 remains the structural completion evidence for physical review-archive movement, lane split, and schema-copy rename work.
- Batch 1 is marked as historical/superseded remediation lineage, not the current control surface.
- `CURRENT_ACTIVE_ENTRYPOINT.json` no longer lists `reviewed_*` in the active/default read order; review-holding snapshots are represented through `archive/review_holding/` and `REVIEW_HOLDING_INDEX.json`.
- Current validation and default-search policy pointers now live in this folder.
- The unresolved repository debt about same-basename active-schema copies is marked closed by Batch 2.
- Guardrails were extended to catch stale Batch 1-as-current pointers and stale review-holding read-order cues.

## Current control surface

- `package_meta/repository_steward_completion_batch2_1_2026_05_20/CURRENT_REPOSITORY_STEWARD_CONTROL_SURFACE.json`
- `package_meta/repository_steward_completion_batch2_1_2026_05_20/VALIDATION_SUITE.md`
- `package_meta/repository_steward_completion_batch2_1_2026_05_20/DEFAULT_SEARCH_PROFILE.json`
- `package_meta/repository_steward_completion_batch2_1_2026_05_20/DERIVED_GENERATED_INDEX_POLICY.json`
- `package_meta/repository_steward_completion_batch2_2026_05_20/OFARM_repository_steward_completion_batch2_report_v0_1.json`

## Active-law non-promotion

This patch changes package metadata, navigation, generated-index pointers, currentness records, validator guardrails, and debt-status wording only. It does not change active OFARM semantic/runtime law.


## Validation status

Repository validation suite passed after this currentness patch.

```text
Repository hygiene check: OK
Generated currentness check: OK
Repository cross-reference check: OK
Repository steward guardrail check: OK
AAI-CP10 final readiness runner: PASS
Repository validation suite: OK
```
