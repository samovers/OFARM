# Consolidation decision ledger — 2026-05-14

## D001 — immutable_base

- Decision: `BASE_UNPACKED_IMMUTABLE_REFERENCE`
- Classification: base_control
- Authority effect: none
- Rationale: Treat this dated source package as the canonical starting point for consolidation.
- Remaining risk: None beyond source package integrity; checksums recorded.

## D002 — farm_owner_consolidated_v0_1

- Decision: `MERGED_AS_ACTIVE_SUPPORTING_IMPLEMENTATION_AND_REVIEW_HOLDING`
- Classification: implementation/conformance support
- Authority effect: No active baseline, RFC, companion, or machine-contract promotion.
- Rationale: The package explicitly states no baseline change, no live ordinary-farm evidence, and implementation/conformance posture. Paths do not overwrite active law.
- Remaining risk: Owner/live evidence remains missing; source-owner closure tasks still required.

## D003 — predevelopment_ai_agent_ready_v0_1

- Decision: `MERGED_AS_ACTIVE_SUPPORTING_IMPLEMENTATION_AND_RESEARCH_WITH_ROOT_NAVIGATION`
- Classification: implementation/conformance support
- Authority effect: Draft companion and draft machine contracts remain nested in implementation support; no promotion into 01/02/03 active authority folders.
- Rationale: The package declares active-support-only authority and non-claims for runtime/API/conformance/external readiness. Its MATERIAL_STATUS files were not copied; final currentness was rebuilt.
- Remaining risk: Later governance must decide whether any draft artifacts are promoted.

## D004 — ai_assistant_computation_finalisation_v0_8

- Decision: `PRESERVED_AS_REVIEW_HOLDING_ONLY`
- Classification: review holding
- Authority effect: No active baseline, accepted RFC, companion, or active machine-contract promotion.
- Rationale: The package is marked draft/proposed/non-default and states active baseline promotion is blocked pending real platform evidence. Direct placement of draft schemas under active 03_machine_contracts would risk silent promotion.
- Remaining risk: Promotion path remains open only after runtime isolation, source-readiness, regulated profile, review workflow, and capability manifest evidence are supplied.

## D005 — regulatory_inspector_RC2_1a_full_snapshot

- Decision: `PRESERVED_AS_REVIEW_HOLDING_ONLY`
- Classification: authority conflict / stale snapshot
- Authority effect: No active baseline/RFC/companion/machine-contract changes accepted from this snapshot.
- Rationale: The addendum is a full older snapshot that modifies active baseline files, adds candidate accepted RFCs/companion/machine contracts, and lacks later active AGR material from the base. It cannot override the current active package.
- Remaining risk: Requires selective promotion review if any regulatory RC2.1a candidates should enter active law.

## D006 — csf_p11_repo_relative_patch

- Decision: `PRESERVED_AS_REVIEW_HOLDING_ONLY_NOT_APPLIED`
- Classification: structural/currentness conflict
- Authority effect: No active folder changes accepted from P11 in this consolidation.
- Rationale: The patch fails against the immutable base and expects a missing CSF-P10-amended predecessor. It also tries to modify PROJECT_AUTHORITY, currentness files, README, validation files, and task register.
- Remaining risk: Need the CSF-P0 through P10/P11 chain or a rebased patch before active merge.

## D007 — csf_p12_patch_bundle

- Decision: `PRESERVED_AS_REVIEW_HOLDING_ONLY_NOT_APPLIED`
- Classification: structural/currentness conflict
- Authority effect: No active folder changes accepted from P12 in this consolidation.
- Rationale: The patch contains stale local path prefixes and assumes a P11-amended base. Its task register references predecessor CSF schemas not present in the immutable base. Currentness files were rebuilt instead of copied.
- Remaining risk: Need a rebased P12 patch and missing predecessor artifacts before active merge.

## D008 — currentness_and_package_metadata

- Decision: `REBUILT_AFTER_MERGE`
- Classification: currentness
- Authority effect: Package navigation only; no semantic/runtime law.
- Rationale: Multiple addendums supplied conflicting/stale currentness files. Final currentness is generated from the consolidated filesystem after safe merge decisions.
- Remaining risk: Currentness must be regenerated after any later merge.

## D009 — implementation_task_register

- Decision: `UPDATED_WITH_CONSOLIDATION_TASKS_ONLY`
- Classification: implementation/conformance implication
- Authority effect: Implementation planning only.
- Rationale: P11/P12 task register diffs depend on unavailable predecessor packages, so the final register records consolidation work and unresolved follow-up tasks rather than copying incompatible task state.
- Remaining risk: P11/P12 task IDs IMP-375 through IMP-389 remain source claims in holding until the missing predecessor chain is reconciled.
