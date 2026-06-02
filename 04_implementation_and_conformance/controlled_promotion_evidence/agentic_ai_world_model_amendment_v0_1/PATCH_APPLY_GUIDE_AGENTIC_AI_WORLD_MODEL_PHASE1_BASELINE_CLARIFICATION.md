# Patch Apply Guide — OFARM Agentic AI / World Model Phase AAI-P1 Baseline Safety Clarification

Date: 2026-05-14  
Patch status: controlled active-baseline clarification delta.  
Apply target: OFARM package that already contains the `agentic_ai_world_model_amendment_v0_1` start package.

## Apply order

1. Replace the five files under `00_active_baseline/` with the files in this delta.
2. Replace the package-control files `ACTIVE_SUBSTANCE_README.md`, `PROJECT_AUTHORITY.md`, `CURRENT_PACKAGE_CHANGELOG.md`, `MATERIAL_STATUS.json`, `MATERIAL_STATUS.csv`, and `MANIFEST.csv`.
3. Add or replace files under `04_implementation_and_conformance/controlled_promotion_evidence/agentic_ai_world_model_amendment_v0_1/`.
4. Read `phase1_baseline_safety_clarification_v0_1/OFARM_Agentic_AI_Phase1_Baseline_Clarification_Summary_v0_1.md` before proceeding to AAI-P2.

## Authority posture

The baseline addenda are active because they are inserted in `00_active_baseline/`. Draft RFCs and schemas under the amendment folder remain active supporting implementation/conformance material only.

## Non-claims

Do not interpret this patch as runtime readiness, production readiness, autonomous compliance decisioning, world-model compliance readiness, two-agent compatibility, legal advice, or external-standard readiness.
