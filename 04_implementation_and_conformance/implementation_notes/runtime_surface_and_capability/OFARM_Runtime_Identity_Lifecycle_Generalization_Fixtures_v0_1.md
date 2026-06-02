# OFARM Runtime Identity Lifecycle Generalization Fixtures v0.1

Date: 2026-04-19
Status: active supporting implementation artifact
Scope: promote the bounded runtime identity/lifecycle support seam into an active generic contract family and prove the materialization invalidation cross-link

---

## 1. Purpose

This fixture wave exists to move identity/lifecycle handling one step closer to real implementation closure without reopening RC2.1 architecture.

It does three things:
- promotes a generic active `IdentityLifecycleChange` contract
- proves starter active examples across the first-priority non-lot families
- proves that current-state refusal can point to a concrete lifecycle-change artifact through `IDENTITY_LIFECYCLE` invalidation

---

## 2. Authority basis used

This wave is grounded in already-active law:
- `02_accepted_rfcs/OFARM_Identity_and_Lifecycle_RFC_v0_1.md`
- `02_accepted_rfcs/OFARM_Current_State_Materialization_RFC_v0_1.md`
- `03_machine_contracts/schemas/core/OFARM_LotLineageChange_schema_v0_1.json`
- `04_implementation_and_conformance/implementation_notes/runtime_surface_and_capability/OFARM_Runtime_Identity_Lifecycle_Expansion_Fixtures_v0_1.md`
- `04_implementation_and_conformance/implementation_notes/runtime_surface_and_capability/OFARM_runtime_identity_lifecycle_expansion_results_v0_1.json`

No constitutional contradiction was found that would justify a baseline rewrite.

---

## 3. Promoted active example families

The active promotion set covers:
- field split
- governed recurring zone revision
- ephemeral advisory mask no-mint decision
- crop-cycle replant successor
- equipment replacement
- facility revision
- storage-location replacement
- reusable-container occupancy continuity

The current-state invalidation cross-link is proved through:
- `OFARM_MaterializationRequest_example_field_split_submission_invalid_v0_1.json`
- `OFARM_MaterializationSnapshot_example_field_split_submission_invalid_v0_1.json`
- `OFARM_MaterializationResult_example_field_split_submission_invalid_v0_1.json`

---

## 4. What this wave proves

The runner for this wave must prove:
- the new active schema validates
- each promoted example validates
- the promoted set covers the priority subject families named above
- both governed continuity outcomes and explicit no-mint outcomes are present
- the field-split refusal path uses `IDENTITY_LIFECYCLE` as the invalidation trigger family
- the refusal path points to a concrete `IdentityLifecycleChange` artifact rather than support-only prose

---

## 5. What this wave still does not prove

This wave does not yet prove:
- full geometry/topology diff interchange
- deployment-collected lifecycle telemetry
- every merge or overlap permutation
- inline lifecycle embedding inside authorization traces
- replacement of the specialized `LotLineageChange` contract

Those remain follow-on implementation and conformance work.
