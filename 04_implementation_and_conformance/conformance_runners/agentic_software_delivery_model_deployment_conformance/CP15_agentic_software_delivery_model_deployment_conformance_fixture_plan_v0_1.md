# CP15 Conformance Fixture Plan v0.1

Status: fixture plan only; executable runner expected after hostile review/remediation.

| Fixture | Type | Purpose |
|---|---|---|
| `generated_artifact_without_agent_trace_fails` | negative | Generated software artifact must carry agent-run/source provenance where generated. |
| `adapter_without_mapping_coverage_fails` | negative | Generated adapter must reference mapping coverage and loss map. |
| `build_success_does_not_authorize_deployment` | negative | BuildProvenance cannot be used as deployment authority. |
| `sbom_missing_for_deployment_candidate_fails` | negative | DeploymentCandidate requires SBOM evidence. |
| `security_scan_blocking_result_blocks_candidate` | negative | Blocking security scan must prevent approval candidate. |
| `waiver_without_expiry_or_authority_fails` | negative | Security waiver requires expiry and authority trace. |
| `conformance_run_pass_does_not_authorize_deployment` | negative | ConformanceRunReceipt pass cannot authorize deployment. |
| `deployment_authorization_without_authority_trace_fails` | negative | DeploymentAuthorization requires authority trace. |
| `deployment_plan_without_rollback_fails` | negative | DeploymentPlan requires rollback plan. |
| `release_bundle_without_signature_fails` | negative | ReleaseBundle requires signature. |
| `runtime_binding_promotes_current_default_fails` | negative | RuntimeSurfaceReleaseBinding cannot promote current/default. |
| `canary_success_does_not_create_production_readiness` | negative | CanaryResult pass cannot create production readiness. |
| `rollback_plan_without_test_evidence_fails` | negative | RollbackPlan requires last-tested evidence. |
| `runtime_receipt_does_not_create_compliance_fact` | negative | RuntimeDeploymentReceipt is not compliance fact. |
| `model_deployment_candidate_without_evaluation_fails` | negative | ModelDeploymentCandidate requires evaluation evidence. |
| `cp13_learning_output_does_not_authorize_model_deployment` | negative | CP13 learning output cannot authorize model deployment. |
| `cp14_model_improvement_signal_does_not_authorize_deployment` | negative | CP14 model signal cannot authorize deployment. |
| `prompt_policy_change_without_conformance_fails` | negative | Prompt/policy change requires conformance run refs. |
| `software_supply_chain_incident_requires_review` | negative | High-severity supply-chain incident requires review. |
| `valid_limited_canary_deployment_candidate_passes` | positive | Valid candidate with build, SBOM, scans, conformance, authorization, canary, rollback can pass. |
| `valid_model_deployment_candidate_for_review_passes` | positive | ModelDeploymentCandidate with evaluation/training evidence passes as review candidate only. |
| `valid_security_waiver_with_expiry_passes` | positive | Security waiver with authority and expiry passes. |
| `valid_runtime_receipt_as_receipt_only_passes` | positive | RuntimeDeploymentReceipt passes as receipt without production-readiness claim. |
