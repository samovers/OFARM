# Prompt — Post-strengthening staple-crop hostile stress test for OFARM

You are doing a **hostile follow-up stress test** of **OFARM** after a pre-implementation strengthening pass.

## Mission
Try to break OFARM **after** the strengthening pass, not before it.
Assume the architecture itself is not to be reopened unless you can show a real contradiction.
Your job is to find:
- scenario families that still escape the strengthening docs
- cases where the strengthening docs are too vague to implement deterministically
- places where the new directions still allow hidden truth shortcuts, evidence drift, or authority ambiguity
- places where campaign-grade staple-crop reality still exceeds the specified conformance and telemetry obligations

## Read first from the active package
1. `PROJECT_AUTHORITY.md`
2. `ACTIVE_SUBSTANCE_README.md`
3. `00_active_baseline/OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md`
4. `00_active_baseline/OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md`
5. `00_active_baseline/OFARM_Alignment_Register_v0_13.md`
6. `00_active_baseline/OFARM_final_hostile_review_after_gap_closure_v0_1.md`
7. `00_active_baseline/OFARM_post_gap_closure_readiness_gate_memo_v0_1.md`
8. `01_companion_artifacts/OFARM_Event_Grammar_and_Commit_Matrix_v0_1.md`
9. `01_companion_artifacts/OFARM_Pack_Safety_and_Compatibility_Policy_v0_2.md`
10. `01_companion_artifacts/OFARM_Authority_Delegation_and_Data_Sovereignty_Policy_v0_2.md`
11. `01_companion_artifacts/OFARM_Compiled_Output_and_Passport_Taxonomy_Note_v0_1.md`
12. `02_accepted_rfcs/OFARM_Identity_and_Lifecycle_RFC_v0_1.md`
13. `02_accepted_rfcs/OFARM_Current_State_Materialization_RFC_v0_1.md`
14. `02_accepted_rfcs/OFARM_Pack_Merge_Semantics_RFC_v0_1.md`
15. `02_accepted_rfcs/OFARM_Authority_Policy_Model_RFC_v0_1.md`

## Then read the strengthening-pass artifacts from their slotted locations
16. `06_active_supporting_research/syntheses/OFARM_pre_implementation_strengthening_pass_staple_crop_v0_1.md`
17. `01_companion_artifacts/OFARM_Evidence_Quality_and_Promotion_Handling_Note_v0_1.md`
18. `04_implementation_and_conformance/implementation_notes/ofarm_staple_crop_scenario_hardening_v0_1/OFARM_Staple_Crop_Campaign_Fixture_Library_v0_1.md`
19. `04_implementation_and_conformance/implementation_notes/ofarm_staple_crop_scenario_hardening_v0_1/OFARM_High_Consequence_Freshness_Profiles_for_Staple_Crop_Campaigns_v0_1.md`
20. `04_implementation_and_conformance/implementation_notes/ofarm_staple_crop_scenario_hardening_v0_1/OFARM_Campaign_Query_and_Retrieval_Regression_Spec_v0_1.md`
21. `04_implementation_and_conformance/implementation_notes/ofarm_staple_crop_scenario_hardening_v0_1/OFARM_Deployment_Evidence_Obligations_for_Hard_Scenarios_v0_1.md`

## Focus areas
Stress-test the strengthening pass against scenario families such as:
- partial replant inside one field with subsidy and insurance timing consequences
- weak or ambiguous pesticide/input identity with later stronger evidence
- human-versus-machine contradiction in fertilization or spray records
- wet grain held temporarily before drying while current state changes repeatedly
- lot split, merge, sublot sampling, reclassification, and buyer dispute
- organic and conventional segregation on one mixed farm with shared equipment or storage
- contractor late reporting and revocation crossing a promotion boundary
- late evidence after dossier assembly or after submission filing
- pack conflicts affecting evidence policy, decision rules, or output shaping on the same scope
- stale current-state use in a high-consequence delivery, attestation, or filing path

## What to test aggressively
For every scenario family you choose, attack at least these dimensions:
1. identity/lifecycle determinism
2. current-state freshness/refusal behavior
3. evidence downgrade/upgrade handling
4. authority/delegation/revocation correctness
5. pack conflict or pack-merge determinism where relevant
6. output taxonomy correctness
7. query/retrieval equivalence and traceability
8. deployment-emitted evidence sufficiency

## Required output
Produce:

1. **Residual failure map**
- what can still break
- whether the break is common, messy-common, or rare-but-dangerous
- why the strengthening docs still leave space for failure

2. **Determinism failures**
- places where two implementers could still behave differently
- exactly which missing rule, fixture, contract, or emitted record causes that divergence

3. **False-strength findings**
- places where the strengthening docs look strong on paper but are still too soft in practice

4. **Promotion recommendations**
For each remaining weakness, say whether the fix belongs in:
- `01_companion_artifacts/`
- `02_accepted_rfcs/`
- `03_machine_contracts/`
- `04_implementation_and_conformance/`
- `06_active_supporting_research/`

5. **Concrete next patches**
- smallest controlled patch
- affected file(s)
- risk if left unresolved

## Important constraints
- do not reopen broad architecture unless a real contradiction exists
- do not flatten OFARM into CRUD or projection-first behavior
- do not let advisory or AI outputs become de facto governance decisions
- do not treat weak evidence as equivalent to missing evidence or to accepted fact
- do not let stale current-state remain acceptable in high-consequence paths by convenience
- do not silently merge pack conflicts
- do not collapse lot lineage ambiguity into hand-waving

## Output style
- be hostile and concrete
- prefer messy-common over exotic edge cases
- distinguish architecture weakness from conformance weakness from deployment-evidence weakness
- cite the exact strengthening artifact sections you are attacking
