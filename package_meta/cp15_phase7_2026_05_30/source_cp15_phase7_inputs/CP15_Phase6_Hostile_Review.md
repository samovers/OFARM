# CP15 Phase 6 — Hostile Review

## Verdict

```text
Acceptance recommendation: ACCEPT WITH CHANGES.
Do not split CP15.
Do not return to Phase 0.
Do not merge CP15 as final baseline yet.
Do not promote CP15 schemas to current/default.
Do not claim production software-delivery, model-deployment, cybersecurity, generated-adapter, or autonomous release readiness.
```

CP15 is conceptually correct. It identifies the right missing layer:

```text
agentic software delivery and model deployment governance
```

not:

```text
full CI/CD product specification
specific cloud/vendor deployment architecture
generic MLOps platform
automatic code-generation approval law
robot mission law
farm-to-farm intelligence law
OFARM Social or OFARM Exchange constitution
production software-delivery readiness
production model-deployment readiness
cybersecurity certification
legal/security/compliance advice
automatic current/default schema promotion
```

The CP15 RFC and baseline patch direction are sound. The Phase 5 machine-contract package is useful and uses the correct draft/non-default staging posture, but the schemas are mostly syntactic. They validate examples, but they do not yet enforce the critical delivery boundary mechanically.

The problem is not scope. The problem is:

```text
semantic hardening, cross-record enforcement, and executable conformance
```

Superseded review recommendation: proceed to CP15 Phase 6.1 remediation and schema hardening.

---

# 1. Direct answers to hostile-review checks

| Check | Verdict | Notes |
|---|---:|---|
| 1. Contradicts existing OFARM truth law? | PASS | CP15 does not rewrite assertion/history truth or current-state materialisation. |
| 2. Preserves distinction among generated artifact, provenance, SBOM, scans, conformance, deployment candidate, deployment plan, authorisation, promotion, runtime binding, receipt, telemetry, rollback, incident? | PARTIAL | The taxonomy is present, but schemas do not cross-check that stronger lifecycle states are supported by compatible upstream records. |
| 3. Lets generated software become deployment authority? | TEXT SAYS NO; SCHEMA NEEDS HARDENING | Generated artifacts carry non-authorisation booleans, but `APPROVED_CANDIDATE` states can exist without strong review/conformance/security linkage. |
| 4. Lets build/test/scan/conformance/canary/runtime receipt/telemetry/tool success become authority/readiness? | RISK PRESENT | Individual artifacts have “doesNotCreate...” flags, but `DeploymentCandidate`, `DeploymentPromotionDecision`, and `RuntimeDeploymentReceipt` can reference failed/weak upstream records unless cross-record conformance is added. |
| 5. Accidentally promotes schemas/contracts to current/default? | PASS | Draft/non-default path and schema IDs are correct. No current/default promotion occurs. |
| 6. Preserves CP11 sustainability gates? | PARTIAL | `DeploymentPlan.cpGateRefs` allows empty arrays and does not require CP11 gates for sustainability-sensitive surfaces. |
| 7. Preserves CP12 mission/adapter gates? | PARTIAL | Mission/robot adapters are recognised, but CP12 gate linkage is not enforceable. |
| 8. Preserves CP13 learning-output and farm-memory boundaries? | PARTIAL | Model deployment candidates reference CP13 learning outputs, but do not verify CP13 output qualification or promotion state. |
| 9. Preserves CP14 training/federated/model-improvement boundaries? | PARTIAL | Training receipts and CP14 model-improvement refs exist, but cross-record eligibility is not checked. |
| 10. Distinguishes model evaluation evidence from deployment authority? | TEXT YES; SCHEMA WEAK | `ModelEvaluationEvidence` can be sufficient despite high/unknown bias unless hardened. |
| 11. Defines SBOM/dependency/static/security/waiver/incident strongly enough? | PARTIAL | Presence is good; risk/severity/disposition contradictions are allowed. |
| 12. Defines runtime binding/environment/canary/rollback/telemetry/receipt strongly enough? | PARTIAL | Shapes exist; temporal coherence and cross-record consistency are weak. |
| 13. Accidentally creates excluded domains? | PASS | Does not create CI/CD product, MLOps platform, cloud topology, Social/Exchange, robot mission, or legal/security certification law. |
| 14. Defines enough conformance? | FAIL | There is only a fixture plan, not an executable runner. |
| 15. Preserves OFARM machine-contract style? | MOSTLY PASS | JSON Schema 2020-12, `additionalProperties: false`, draft/non-default IDs, schemaVersion constants, refs, and non-authorisation booleans align with OFARM style. |
| 16. Too broad/narrow/wrongly named or implementing excluded domains? | MOSTLY OK | Artifact family is broad but coherent. Main risk is weak cross-record enforcement, not naming/scope. |

---

# 2. Top defects

## Defect 1 — No executable CP15 conformance runner exists

**Severity:** P0 / blocking

The package includes:

```text
CP15_agentic_software_delivery_model_deployment_conformance_fixture_plan_v0_1.md
```

but no executable schema-aware/cross-record conformance runner.

**Why it matters**

CP15 is about deployment governance. A fixture plan does not prove that generated software, model deployment, security, conformance, canary, rollback, runtime receipt, or telemetry boundaries are enforceable.

**Required fix**

Create an executable runner with:

```text
schemaAware: true
semanticHardeningAware: true
crossRecordAware: true
supplyChainAware: true
modelDeploymentBoundaryAware: true
```

Minimum first-run fixture families:

```text
deployment_candidate_references_failed_security_scan_fails
deployment_candidate_references_critical_dependency_risk_fails
deployment_candidate_references_failed_conformance_run_fails
deployment_promotion_references_denied_authorization_fails
runtime_receipt_references_revoked_authorization_fails
release_bundle_with_failed_conformance_fails
canary_pass_with_failed_telemetry_fails
rollback_ready_with_future_test_fails
model_candidate_with_high_bias_evaluation_fails
cp13_learning_output_does_not_authorize_model_deployment
cp14_model_signal_does_not_authorize_model_deployment
valid_limited_canary_release_chain_passes
```

---

## Defect 2 — DeploymentCandidate can become approved while referencing failed evidence

**Severity:** P0 / blocking

`DeploymentCandidate` requires refs to:

```text
buildProvenanceRef
sbomRef
dependencyRiskAssessmentRef
staticAnalysisResultRefs
securityScanResultRefs
conformanceRunRefs
```

But it does not verify that these referenced records are acceptable.

A `DeploymentCandidate` can be `APPROVED_CANDIDATE` while the referenced records are:

```text
SecurityScanResult.disposition = BLOCK
StaticAnalysisResult.disposition = BLOCK
DependencyRiskAssessment.riskClass = CRITICAL
DependencyRiskAssessment.disposition = ALLOW
ConformanceRunReceipt.runDisposition = FAIL
BuildProvenance.buildStatus = FAILED
SBOMReference.sbomStatus = REJECTED
```

**Why it matters**

This lets “evidence presence” substitute for “evidence sufficiency.” It repeats the anti-pattern OFARM has been avoiding since CP11.

**Required fix**

Add cross-record conformance:

```text
If DeploymentCandidate.candidateState = APPROVED_CANDIDATE:
- BuildProvenance.buildStatus must be SUCCEEDED.
- SBOMReference.sbomStatus must be VALIDATED.
- DependencyRiskAssessment.disposition must be ALLOW or ALLOW_WITH_REVIEW with review basis.
- DependencyRiskAssessment.riskClass must not be CRITICAL unless waived by governed SecurityFindingWaiver / review decision.
- StaticAnalysisResult.disposition must not be BLOCK or TOOL_FAILED.
- SecurityScanResult.disposition must not be BLOCK or TOOL_FAILED.
- ConformanceRunReceipt.runDisposition must be PASS or PASS_WITH_WARNINGS with allowed warnings.
```

Add fixtures:

```text
approved_candidate_with_failed_build_fails
approved_candidate_with_rejected_sbom_fails
approved_candidate_with_blocking_security_scan_fails
approved_candidate_with_failed_conformance_run_fails
valid_approved_candidate_with_sufficient_evidence_passes
```

---

## Defect 3 — Security and static-analysis result contradictions are allowed

**Severity:** P0 / blocking

The schemas allow:

```text
SecurityScanResult.severityMax = CRITICAL
SecurityScanResult.disposition = PASS

StaticAnalysisResult.severityMax = CRITICAL
StaticAnalysisResult.disposition = PASS
```

**Why it matters**

This defeats the security gate. A critical finding cannot be treated as an ordinary pass without waiver/review linkage.

**Required fix**

Add semantic rules:

```text
If severityMax in [HIGH, CRITICAL]:
  disposition must be REQUIRE_REVIEW or BLOCK unless a SecurityFindingWaiver is approved, unexpired, and scoped to the finding.

If scanState = FAILED:
  disposition must be TOOL_FAILED, BLOCK, or REQUIRE_REVIEW.

If disposition = PASS:
  severityMax must be NONE, LOW, or policy-declared acceptable MEDIUM.
```

Add fixtures:

```text
security_scan_critical_pass_fails
static_analysis_critical_pass_fails
security_scan_failed_with_pass_fails
valid_security_scan_high_with_approved_waiver_passes
```

---

## Defect 4 — DependencyRiskAssessment can allow critical or unknown risk

**Severity:** P0 / blocking

The schema allows:

```text
riskClass = CRITICAL
disposition = ALLOW
```

and:

```text
riskClass = UNKNOWN
disposition = ALLOW
```

**Why it matters**

Dependency risk is one of the main software supply-chain gates. Unknown or critical risk cannot become deployment-sufficient without review/waiver.

**Required fix**

Add rules:

```text
If riskClass = CRITICAL:
  disposition must be BLOCK or ALLOW_WITH_REVIEW with waiver/review refs.

If riskClass = UNKNOWN:
  disposition must be INSUFFICIENT_BASIS or ALLOW_WITH_REVIEW.

If disposition = ALLOW:
  riskClass must be LOW or MEDIUM depending on policy.
```

Add fixtures:

```text
critical_dependency_risk_allow_fails
unknown_dependency_risk_allow_fails
valid_low_dependency_risk_allow_passes
valid_critical_dependency_risk_with_review_passes
```

---

## Defect 5 — DeploymentPlan can omit CP gates and use unsafe blast radius

**Severity:** P0 / blocking

`DeploymentPlan.cpGateRefs` has `minItems: 0`, and there is no rule tying blast radius to approval/gates.

This allows:

```text
planState = APPROVED_CANDIDATE
blastRadiusClass = GLOBAL
cpGateRefs = []
```

**Why it matters**

CP15’s core invariant requires applicable CP11/CP12/CP13/CP14 gates before deployment. An empty gate set may be legitimate for a trivial sandbox artifact, but not for high-consequence runtime surfaces, model deployment, mission adapters, sustainability outputs, or cross-farm/training surfaces.

**Required fix**

Add:

```text
If planState = APPROVED_CANDIDATE:
  rollbackPlanRef and canaryPlanRef must point to READY/APPROVED records.
  cpGateRefs must have minItems >= 1 unless noApplicableCPGatesBasis is present.

If blastRadiusClass in [SINGLE_FARM, MULTI_FARM, GLOBAL]:
  require authority review and explicit blast-radius approval.

If blastRadiusClass = GLOBAL:
  require multi-party governance review and staged rollout/canary plan.
```

Add fixtures:

```text
approved_global_deployment_plan_without_cp_gates_fails
approved_plan_without_rollback_readiness_fails
approved_plan_without_canary_approval_fails
valid_limited_canary_plan_with_cp_gates_passes
```

---

## Defect 6 — DeploymentAuthorization temporal coherence and support are weak

**Severity:** P0 / blocking

The schema permits:

```text
authorizationState = ACTIVE
validUntil < validFrom
```

It also does not cross-check that the referenced plan is approved or that authorization scope matches the plan environment/blast radius.

**Why it matters**

Deployment authorisation is one of CP15’s central governance gates. It cannot be merely a syntactically valid object.

**Required fix**

Add semantic conformance:

```text
validUntil must be after validFrom.
ACTIVE authorization must not be expired at evaluation time.
ACTIVE/APPROVED authorization must reference DeploymentPlan.planState = APPROVED_CANDIDATE.
authorizationScopeRefs must cover targetEnvironmentRefs / runtime surface / blast radius.
```

Add fixtures:

```text
active_deployment_authorization_expired_fails
deployment_authorization_valid_until_before_valid_from_fails
deployment_authorization_references_rejected_plan_fails
valid_active_deployment_authorization_passes
```

---

## Defect 7 — DeploymentPromotionDecision can promote to runtime without sufficient chain

**Severity:** P0 / blocking

`DeploymentPromotionDecision` can be:

```text
decisionState = APPROVED
promotionDisposition = PROMOTE_TO_RUNTIME
```

without verifying:

```text
DeploymentCandidate is approved and supported by passed evidence.
DeploymentAuthorization is active.
ReleaseBundle is signed and matched to the candidate.
RuntimeSurfaceReleaseBinding exists and is bounded/non-default.
CanaryResult is acceptable where required.
RollbackPlan is ready.
```

**Why it matters**

This is a hidden deployment-authority gap. Promotion decision is the artifact that can move a candidate toward runtime. It needs hard cross-record checks.

**Required fix**

Add cross-record rules:

```text
If decisionState = APPROVED and promotionDisposition in [PROMOTE_TO_CANARY, PROMOTE_TO_RELEASE_BUNDLE, PROMOTE_TO_RUNTIME]:
- DeploymentCandidate.candidateState must be APPROVED_CANDIDATE.
- DeploymentAuthorization.authorizationState must be APPROVED or ACTIVE.
- DeploymentAuthorization must be unexpired.
- required reviewDecisionRef and authorityDecisionTraceRef must be present and current.

If promotionDisposition = PROMOTE_TO_RUNTIME:
- require releaseBundleRef or runtimeSurfaceReleaseBindingRef.
- require rollbackPlan readiness.
- require canary result where policy requires canary.
```

Add fixtures:

```text
approved_runtime_promotion_with_rejected_candidate_fails
approved_runtime_promotion_with_denied_authorization_fails
approved_runtime_promotion_without_release_bundle_fails
valid_promotion_to_canary_passes
```

---

## Defect 8 — RuntimeSurfaceReleaseBinding can look active without real deployment chain support

**Severity:** P0 / blocking

`RuntimeSurfaceReleaseBinding.bindingState = ACTIVE_NON_DEFAULT` requires refs, but does not verify those refs are valid, active, signed, or authorised.

**Why it matters**

A runtime surface binding is where release artifacts begin to affect runtime behaviour. It must not be activated by reference presence alone.

**Required fix**

Add cross-record conformance:

```text
If bindingState = ACTIVE_NON_DEFAULT:
- ReleaseBundle.bundleState must be SIGNED or RELEASE_CANDIDATE.
- DeploymentAuthorization.authorizationState must be ACTIVE.
- CapabilityManifest must declare matching surface and no overclaim.
- ReleaseBundle.releaseDigest must match RuntimeDeploymentReceipt/ReleaseBinding evidence where applicable.
- doesNotPromoteCurrentDefault must remain true.
```

Add fixtures:

```text
active_runtime_binding_with_unsigned_bundle_fails
active_runtime_binding_with_revoked_authorization_fails
runtime_binding_promotes_current_default_fails
valid_active_non_default_runtime_binding_passes
```

---

## Defect 9 — RuntimeDeploymentReceipt can become too strong

**Severity:** P0 / blocking

`RuntimeDeploymentReceipt` records runtime receipt, but does not enforce:

```text
authorization is active
release bundle is signed
runtime binding is active non-default
receipt time is within authorization window
receipt does not imply production readiness
```

The schema has `doesNotCreateProductionReadiness: true`, which is good, but cross-record semantics are missing.

**Required fix**

Add cross-record conformance:

```text
If receiptState = CONFIRMED_BY_RUNTIME:
- DeploymentAuthorization must be ACTIVE and not expired.
- ReleaseBundle must be SIGNED or RELEASE_CANDIDATE.
- RuntimeSurfaceReleaseBinding must be ACTIVE_NON_DEFAULT.
- deployedAt must fall inside authorization window.
- doesNotCreateProductionReadiness must be true.
```

Add fixtures:

```text
runtime_receipt_with_revoked_authorization_fails
runtime_receipt_with_unsigned_release_bundle_fails
runtime_receipt_outside_authorization_window_fails
valid_runtime_receipt_as_receipt_only_passes
```

---

## Defect 10 — CanaryResult can pass despite failing telemetry or contradictory state/disposition

**Severity:** P0 / blocking

The schema permits contradictions such as:

```text
resultState = PASSED
resultDisposition = FAIL
```

and does not cross-check telemetry.

**Why it matters**

Canary success must not be used as production readiness, but it is still an important gate. It must be internally coherent and evidence-based.

**Required fix**

Add rules:

```text
If resultState = PASSED:
  resultDisposition must be PASS.
  referenced telemetry must not have incident/blocking disposition.

If resultDisposition = PASS:
  resultState must be PASSED.

If resultState = FAILED:
  resultDisposition must be FAIL or REQUIRE_REVIEW.
```

Add fixtures:

```text
canary_pass_with_fail_disposition_fails
canary_pass_with_incident_telemetry_fails
canary_success_does_not_create_production_readiness
valid_canary_pass_with_normal_telemetry_passes
```

---

## Defect 11 — Rollback readiness is too weak

**Severity:** P0 / blocking

`RollbackPlan` can be:

```text
rollbackReadinessState = READY
lastTestedAt = 2999-01-01T00:00:00Z
```

and still pass. It also has no freshness state or test-result reference.

**Why it matters**

Rollback is a required safety gate. A stale, future-dated, or untested rollback plan should not support deployment.

**Required fix**

Add:

```text
rollbackReadinessFreshnessState: FRESH | STALE | UNKNOWN | INVALIDATED
rollbackTestResultRefs
```

Semantic checks:

```text
lastTestedAt must not be after evaluation time.
READY requires recent successful test evidence.
READY must not coexist with STALE/UNKNOWN/INVALIDATED freshness.
```

Add fixtures:

```text
rollback_ready_with_future_test_fails
rollback_ready_without_test_result_fails
rollback_ready_with_stale_freshness_fails
valid_rollback_ready_with_recent_test_passes
```

---

## Defect 12 — SecurityFindingWaiver can be approved while expired or temporally impossible

**Severity:** P0 / blocking

`SecurityFindingWaiver` can be:

```text
waiverState = APPROVED
expiresAt < createdAt
```

and there is no evaluation-time currentness check.

**Why it matters**

Security waivers are dangerous exceptions. They must be bounded and current.

**Required fix**

Add semantic checks:

```text
expiresAt must be after createdAt.
APPROVED waiver must not be expired at evaluation time.
APPROVED waiver must be scoped to exact finding refs.
Waiver cannot cover CRITICAL findings unless severity-specific authority permits it.
```

Add fixtures:

```text
approved_security_waiver_expired_fails
approved_security_waiver_expiry_before_created_fails
critical_finding_waiver_without_special_authority_fails
valid_security_waiver_with_expiry_passes
```

---

## Defect 13 — ModelEvaluationEvidence can be sufficient despite high/unknown bias

**Severity:** P0 / blocking

The schema permits:

```text
biasRiskClass = HIGH
evaluationDisposition = SUFFICIENT_FOR_CANDIDATE
```

**Why it matters**

Model deployment is a major risk path. High or unknown bias cannot support candidate sufficiency without review/qualification.

**Required fix**

Add rules:

```text
If biasRiskClass in [HIGH, UNKNOWN]:
  evaluationDisposition must be REQUIRE_REVIEW, INSUFFICIENT, or BLOCK.

If evaluationDisposition = SUFFICIENT_FOR_CANDIDATE:
  biasRiskClass must be LOW or MEDIUM with declared limitations.
```

Add cross-record checks for CP13/CP14:

```text
ModelDeploymentCandidate cannot be APPROVED_CANDIDATE unless referenced ModelEvaluationEvidence is sufficient and not high/unknown bias.
```

Add fixtures:

```text
model_evaluation_high_bias_sufficient_fails
model_evaluation_unknown_bias_sufficient_fails
model_candidate_with_insufficient_evaluation_fails
valid_model_candidate_for_review_passes
```

---

## Defect 14 — CP13 and CP14 boundaries for model deployment are only references

**Severity:** P0 / blocking

`ModelDeploymentCandidate` requires:

```text
modelEvaluationEvidenceRefs
trainingUseReceiptRefs
cp13LearningOutputRefs
cp14ModelImprovementSignalRefs
```

But it does not verify:

```text
CP13 learning outputs are qualified for model-candidate support.
CP14 training-use receipts are confirmed and policy-compliant.
CP14 model-improvement signals are not deployment authority.
Federated or cross-farm signals are not used beyond permitted derivative/training purposes.
```

**Why it matters**

This is the highest CP15/CP14 boundary risk.

**Required fix**

Add cross-record conformance:

```text
If ModelDeploymentCandidate.modelCandidateState = APPROVED_CANDIDATE:
- referenced CP13 learning outputs must be qualified for model-deployment candidate support, not deployment authority.
- referenced CP14 TrainingUseReceipt must be CONFIRMED and purpose/recipient compliant.
- referenced CP14 ModelImprovementSignal must be accepted/usable but explicitly non-deploying.
- no CP14 revocation or poisoning/anomaly block may be active.
```

Add fixtures:

```text
cp13_learning_output_does_not_authorize_model_deployment
cp14_model_signal_does_not_authorize_deployment
model_candidate_with_revoked_training_use_fails
model_candidate_with_poisoned_federated_signal_fails
valid_model_deployment_candidate_for_review_passes
```

---

## Defect 15 — GeneratedPromptOrPolicyArtifact can approve high-consequence policy without review

**Severity:** P0 / blocking

The schema permits:

```text
targetUseClass = HIGH_CONSEQUENCE
reviewRequired = false
artifactStatus = APPROVED_CANDIDATE
```

**Why it matters**

Prompts and policies can steer agents, tool use, authority checks, and output behaviour. High-consequence prompt/policy changes must require review and conformance.

**Required fix**

Add schema/conformance rule:

```text
If targetUseClass in [STATE_AFFECTING, HIGH_CONSEQUENCE, DEPLOYMENT_RELATED, MISSION_RELATED]:
  reviewRequired must be true.
  artifactStatus = APPROVED_CANDIDATE requires authorityDecisionTraceRef, conformanceRunRefs, and security/risk review refs.
```

Add fixtures:

```text
high_consequence_prompt_policy_without_review_fails
mission_related_prompt_policy_without_conformance_fails
valid_high_consequence_policy_candidate_with_review_passes
```

---

## Defect 16 — GeneratedAdapterArtifact can become approved candidate without CP12/CP14 gates by adapter kind

**Severity:** P0 / blocking

The schema recognises adapter kinds:

```text
ROBOT_VENDOR_ADAPTER
DATA_SPACE_ADAPTER
REGISTRY_ADAPTER
```

but does not enforce corresponding gates.

**Why it matters**

Adapters are high-risk because they translate external systems into OFARM surfaces. Robot/vendor adapters intersect CP12. Data-space adapters intersect CP14. Registry adapters may affect evidence/authority/currentness.

**Required fix**

Add conditional/cross-record rules:

```text
If adapterKind = ROBOT_VENDOR_ADAPTER:
  require CP12 mission/command boundary review refs.

If adapterKind = DATA_SPACE_ADAPTER:
  require CP14 sharing/training/data-sovereignty review refs.

If adapterKind = REGISTRY_ADAPTER:
  require external-standard/currentness/mapping coverage review refs.

If adapterStatus = APPROVED_CANDIDATE:
  require conformanceRunRefs, securityScanRefs, and mapping loss/coverage sufficiency.
```

Add fixtures:

```text
robot_vendor_adapter_without_cp12_gate_fails
data_space_adapter_without_cp14_gate_fails
adapter_with_insufficient_mapping_coverage_fails
valid_robot_adapter_candidate_with_cp12_gate_passes
```

---

## Defect 17 — SemanticMappingCandidate can approve high confidence despite loss/coverage weakness

**Severity:** P1 / strong before final

`SemanticMappingCandidate` can be `APPROVED_CANDIDATE` with `mappingConfidenceClass = HIGH`, but no cross-record proof that `lossMapRef` and `mappingCoverageStatementRef` are sufficient.

**Required fix**

Add conformance:

```text
APPROVED_CANDIDATE with HIGH confidence requires MappingCoverageStatement sufficient and LossMap disposition acceptable.
INSUFFICIENT confidence cannot be APPROVED_CANDIDATE.
```

---

## Defect 18 — ReleaseBundle can be release candidate with failed conformance or mismatched artifacts

**Severity:** P0 / blocking

`ReleaseBundle` requires refs and signature, but does not verify:

```text
bundle artifacts match candidate artifacts
conformance runs passed
SBOM matches release artifact digest
signature covers releaseDigest, artifact refs, SBOM, and candidate
```

**Required fix**

Add cross-record conformance:

```text
If bundleState in [SIGNED, RELEASE_CANDIDATE]:
- ConformanceRunReceipt.runDisposition must be PASS or accepted PASS_WITH_WARNINGS.
- SBOM artifactRefs must cover artifactRefs.
- signatureRef must cover releaseDigest/artifacts/SBOM/candidate.
- deploymentCandidateRef must resolve to APPROVED_CANDIDATE or UNDER_REVIEW depending state.
```

Add fixtures:

```text
release_bundle_with_failed_conformance_fails
release_bundle_with_mismatched_sbom_fails
release_bundle_without_signature_coverage_fails
valid_signed_release_bundle_passes
```

---

## Defect 19 — DeploymentOutputQualification is too narrow but still not lifecycle-aware

**Severity:** P1

`DeploymentOutputQualification` blocks strong uses through enum design, which is good. But it does not enforce that `PRODUCTION_READINESS_CANDIDATE` has special qualification/review, nor does it require blocked uses to contain all prohibited classes for advisory outputs.

**Required fix**

Rules:

```text
If outputDisposition = ADVISORY_ONLY:
  blockedUseClasses must include all strong uses.

If outputDisposition = PRODUCTION_READINESS_CANDIDATE:
  require explicit review basis and keep PRODUCTION_READINESS blocked until separate readiness gate.

allowedUseClasses and blockedUseClasses must remain disjoint.
```

---

## Defect 20 — Incidents and rollback are not connected enough to deployment state

**Severity:** P1

`DeploymentIncident` and `SoftwareSupplyChainIncident` require review/rollback refs, but downstream blocking is not specified. A confirmed critical incident should block or revoke candidate/authorization/binding use until resolved.

**Required fix**

Add conformance:

```text
Confirmed HIGH/CRITICAL DeploymentIncident or SoftwareSupplyChainIncident blocks DeploymentPromotionDecision, RuntimeSurfaceReleaseBinding, and DeploymentAuthorization unless resolved/mitigated by reviewed action.
```

---

# 3. What CP15 got right

The draft is strong on scope and taxonomy:

```text
- clear non-authorisation invariant;
- generated artifacts are separated from delivery artifacts;
- deployment candidate / plan / authorization / promotion decision are distinct;
- build, SBOM, dependency, static analysis, security, conformance, canary, rollback, telemetry, receipt, and incident records are separated;
- model deployment is distinguished from model evaluation;
- CP11/CP12/CP13/CP14 gates are recognised;
- draft/non-default currentness is preserved;
- no full CI/CD, vendor topology, MLOps, Social, Exchange, or certification law is created.
```

The required fixes are enforcement fixes, not architectural redesign.

---

# 4. Does CP15 need to be split?

```text
No.
```

CP15 is one coherent amendment:

```text
Agentic Software Delivery and Model Deployment Governance
```

Splitting it into separate software, model, adapter, and security amendments would create coordination risk because the safety problem is the interaction among those surfaces.

The right approach is:

```text
Keep CP15 intact.
Harden the draft schemas.
Add executable cross-record conformance.
Keep all schemas draft/non-default.
```

---

# 5. Required next phase

```text
CP15 Phase 6.1 — Remediation and Schema Hardening
```

Minimum scope:

```text
1. Add executable CP15 conformance runner.
2. Harden DeploymentCandidate evidence sufficiency and cross-record checks.
3. Harden DeploymentPlan CP gate / rollback / canary / blast-radius requirements.
4. Harden DeploymentAuthorization temporal and plan-state checks.
5. Harden DeploymentPromotionDecision promotion-chain checks.
6. Harden ReleaseBundle signature/SBOM/conformance/candidate consistency.
7. Harden RuntimeSurfaceReleaseBinding active-state checks.
8. Harden RuntimeDeploymentReceipt receipt-only and authorization-window checks.
9. Harden CanaryResult state/disposition/telemetry consistency.
10. Harden RollbackPlan and SecurityFindingWaiver temporal/currentness checks.
11. Harden security/static/dependency risk disposition consistency.
12. Harden ModelEvaluationEvidence and ModelDeploymentCandidate cross-record gates.
13. Harden GeneratedPromptOrPolicyArtifact high-consequence review requirements.
14. Harden GeneratedAdapterArtifact adapter-kind CP gate requirements.
15. Add incident-driven deployment blocking.
```

---

# 6. Recommended next command

```text
Start CP15 Phase 6.1.

Using the CP15 Phase 6 hostile review, produce a CP15 remediation plan.

For each P0 and P1 defect, provide:
- exact RFC text change;
- exact baseline patch change if needed;
- exact schema change;
- exact conformance fixture change;
- whether the change is blocking for Phase 7.

Then produce revised schema-style definitions only for the affected schemas:
- DeploymentCandidate
- DeploymentPlan
- DeploymentAuthorization
- DeploymentPromotionDecision
- ReleaseBundle
- RuntimeSurfaceReleaseBinding
- RuntimeDeploymentReceipt
- CanaryResult
- RollbackPlan
- SecurityFindingWaiver
- SecurityScanResult
- StaticAnalysisResult
- DependencyRiskAssessment
- DeploymentOutputQualification
- ModelEvaluationEvidence
- ModelDeploymentCandidate
- GeneratedPromptOrPolicyArtifact
- GeneratedAdapterArtifact
- SemanticMappingCandidate
- BuildProvenance, if needed
- SBOMReference, if needed
- ConformanceRunReceipt, if needed
- CanaryPlan, if needed
- DeploymentIncident, if needed
- SoftwareSupplyChainIncident, if needed

Also produce:
- executable conformance fixture plan;
- minimum P0 runner specification;
- positive and negative fixture list.

Do not create OFARM Social, OFARM Exchange, production CI/CD, generic MLOps, legal/security certification, or post-CP15 contracts.
Do not promote CP11, CP12, CP13, CP14, or CP15 schemas to current/default.
Do not claim production software-delivery, model-deployment, generated-adapter, cybersecurity, or autonomous release readiness.
Keep all CP15 machine contracts in drafts_non_default.
```

---

# 7. Final hostile-review recommendation

```text
Acceptance recommendation: ACCEPT WITH CHANGES.
Do not reject CP15.
Do not split CP15.
Do not merge CP15 yet.
Do not promote CP15 schemas to current/default.
Proceed to CP15 Phase 6.1 remediation.
```

CP15 is the right final amendment in this CP sequence. Its scope is correct. The next work is making the machine-contract layer enforce the law it already states.
