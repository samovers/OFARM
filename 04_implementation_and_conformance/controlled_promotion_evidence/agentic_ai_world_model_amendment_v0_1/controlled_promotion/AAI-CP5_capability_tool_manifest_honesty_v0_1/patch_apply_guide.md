# AAI-CP5 patch apply guide

Apply this patch after AAI-CP4.

1. Copy the accepted RFC, companion policy, active agent-manifest schemas, examples, fixtures, and CP5 controlled-promotion folder.
2. Apply the active baseline consistency updates.
3. Regenerate contract, example, decision, traceability, implementation-lane, material-status, and manifest indexes.
4. Run `python3 package_meta/tools/validate_repo_hygiene.py`.
5. Run `python3 04_implementation_and_conformance/controlled_promotion_evidence/agentic_ai_world_model_amendment_v0_1/controlled_promotion/AAI-CP5_capability_tool_manifest_honesty_v0_1/conformance/ofarm_cp5_manifest_honesty_conformance_runner_v0_1.py`.

Do not represent CP5 as runtime AI-agent readiness, two-agent compatibility, production readiness, or world-model readiness.
