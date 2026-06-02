# OFARM Pack Merge Semantics — CP15 surface extension v0.1

Status: CP15 final amendment accepted/merged addendum  
Date: 2026-05-30

CP15 adds draft pack/profile surfaces:

```text
SOFTWARE_DELIVERY_POLICY
GENERATED_ARTIFACT_POLICY
SEMANTIC_MAPPING_POLICY
SECURITY_SCAN_POLICY
SECURITY_WAIVER_POLICY
CONFORMANCE_RUN_POLICY
DEPLOYMENT_CANDIDATE_POLICY
DEPLOYMENT_PLAN_POLICY
DEPLOYMENT_AUTHORIZATION_POLICY
RELEASE_BUNDLE_POLICY
RUNTIME_SURFACE_BINDING_POLICY
CANARY_POLICY
ROLLBACK_POLICY
MODEL_DEPLOYMENT_POLICY
PROMPT_POLICY_CHANGE_POLICY
DEPLOYMENT_OUTPUT_QUALIFICATION_POLICY
```

Default merge posture:

- security, waiver, conformance, deployment authorization, release, canary, rollback, model-deployment, and high-consequence prompt/policy surfaces use STRONGEST_REQUIREMENT or HARD_FAIL;
- semantic mapping surfaces use IDENTICAL_ONLY or HARD_FAIL unless loss/coverage equivalence is explicit;
- deployment output qualification uses STRONGEST_REQUIREMENT;
- any policy that would weaken CP11, CP12, CP13, CP14, authority, evidence, currentness, or output gates hard-fails by default.
