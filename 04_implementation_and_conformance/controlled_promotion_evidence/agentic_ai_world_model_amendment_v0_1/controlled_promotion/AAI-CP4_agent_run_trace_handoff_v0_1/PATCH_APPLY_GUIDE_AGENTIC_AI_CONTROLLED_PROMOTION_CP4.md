# CP4 patch apply guide

Apply this CP4 patch only on top of the CP3 package:

`OFARM2_2026-05-16_agentic_ai_controlled_promotion_cp3_v0_1`

Expected result:

`OFARM2_2026-05-16_agentic_ai_controlled_promotion_cp4_v0_1`

Validation commands from repository root:

```bash
python3 04_implementation_and_conformance/controlled_promotion_evidence/agentic_ai_world_model_amendment_v0_1/controlled_promotion/AAI-CP4_agent_run_trace_handoff_v0_1/conformance/runners/ofarm_aai_cp4_agent_run_trace_contract_runner_v0_1.py
python3 package_meta/tools/validate_repo_hygiene.py
```

CP4 must not be used to claim runtime AI-agent readiness, two-agent compatibility, autonomous compliance decisioning, production readiness, or external-standard readiness.
