
# Canonical validation suite

Status: package metadata only.

This is the current human-readable validation-suite entrypoint after Repository Steward Completion Batch 2.1.

Run:

```bash
python3 package_meta/tools/run_repository_validation_suite.py
```

The wrapper runs:

1. `package_meta/tools/validate_repo_hygiene.py`
2. `package_meta/tools/check_generated_currentness.py`
3. `package_meta/tools/check_repository_cross_references.py`
4. `package_meta/tools/check_repository_steward_guardrails.py`
5. `04_implementation_and_conformance/controlled_promotion_evidence/agentic_ai_world_model_amendment_v0_1/controlled_promotion/AAI-CP10_final_readiness_claim_limits_v0_1/conformance/ofarm_cp10_final_readiness_runner_v0_1.py`

Readiness may not be claimed unless the wrapper passes.

Supersedes the Batch 1 validation-suite pointer: `package_meta/repository_steward_remediation_2026_05_20/VALIDATION_SUITE.md`.
