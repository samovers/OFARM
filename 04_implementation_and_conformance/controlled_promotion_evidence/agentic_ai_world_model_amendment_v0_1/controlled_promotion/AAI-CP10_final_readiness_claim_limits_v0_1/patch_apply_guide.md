# Patch apply guide — AAI-CP10

Apply from package `OFARM2_2026-05-17_agentic_ai_controlled_promotion_cp9_v0_1`.

1. Add the CP10 folder:
   `04_implementation_and_conformance/controlled_promotion_evidence/agentic_ai_world_model_amendment_v0_1/controlled_promotion/AAI-CP10_final_readiness_claim_limits_v0_1/`
2. Append CP10 addenda to:
   - `00_active_baseline/OFARM_post_gap_closure_readiness_gate_memo_v0_1.md`
   - `00_active_baseline/OFARM_final_hostile_review_after_gap_closure_v0_1.md`
3. Refresh package metadata, indexes, manifests, and handover gate.
4. Run:
   `python3 package_meta/tools/validate_repo_hygiene.py`
5. Run:
   `python3 04_implementation_and_conformance/controlled_promotion_evidence/agentic_ai_world_model_amendment_v0_1/controlled_promotion/AAI-CP10_final_readiness_claim_limits_v0_1/conformance/ofarm_cp10_final_readiness_runner_v0_1.py`

CP10 does not add schemas, accepted RFCs, or companion artifacts.
