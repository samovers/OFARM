# CP14 Phase 6 — Hostile Review

## Verdict

```text
Acceptance recommendation: ACCEPT WITH CHANGES.
Do not split CP14.
Do not return to Phase 0.
Do not merge CP14 as final baseline yet.
Do not promote CP14 schemas to current/default.
Do not start CP15 yet.
```

CP14 is conceptually correct. It identifies the right missing layer:

```text
farm-to-farm intelligence boundary law
```

not:

```text
OFARM Social constitution
OFARM Exchange constitution
public benchmark product law
production federated-learning platform law
model/software deployment governance
generic reputation law
legal/certification/advice readiness
```

The RFC and baseline patch direction are sound. The Phase 5 machine-contract package is useful, but it is not yet enforceable enough. The draft schemas validate examples, but they have almost no conditional or cross-record hardening. The fixture plan is also not executable.

The problem is not scope. The problem is **semantic hardening and cross-record enforcement**.

---

## Review basis

Reviewed materials:

```text
- CP14 Phase 3 RFC draft
- CP14 Phase 4 baseline patch plan
- CP14 Phase 5 machine-contract plan
- CP14 Phase 5 draft machine-contract package
- CP14 Phase 5 conformance fixture plan
```

The draft package contains:

```text
27 draft/non-default CP14 schemas
27 draft examples
1 fixture plan
no executable conformance runner yet
```

All schemas and examples validate syntactically, but all CP14 schemas currently lack conditional validation logic. Several semantically invalid cases pass schema validation.

Examples that currently pass schema validation but should not pass CP14 conformance:

```text
- active share grant with validUntil before validFrom
- allowedUseClasses and prohibitedUseClasses containing the same use
- output qualification allowing farm-truth/compliance/model-deployment uses
- approved anonymisation claim with HIGH residual risk and no approval decision
- accepted federated-learning contribution with privacyMechanismClass = NONE_DECLARED
- confirmed training-use receipt with policyCompliant = false
- published regional alert without output qualification
```

---

## Direct answers to hostile-review checks

| Check | Verdict | Notes |
|---|---|---|
| 1. Contradicts existing OFARM truth law? | **No, but tighten.** | The prose preserves truth law. The schemas still allow received intelligence / outputs to carry strong-use classes unless blocked by conformance. |
| 2. Preserves distinction between sharing, authority, intelligence, alert, benchmark, applicability, output qualification, and compliance fact? | **Text yes; schemas weak.** | Artifact names are right, but cross-record and output-use constraints are under-enforced. |
| 3. Lets received intelligence become farm truth or current state? | **Text says no; schema can be misused.** | `IntelligenceOutputQualification.allowedUseClasses` is free text and can include strong uses. |
| 4. Lets regional alerts become farm-level occurrence truth? | **Mostly no in prose; incomplete in schema.** | `RegionalAlert` has non-truth booleans, but published alerts do not require output qualification or local-applicability assessment. |
| 5. Lets benchmark deltas become compliance facts? | **Mostly no in benchmark schema; still output risk.** | `BenchmarkDelta` has `doesNotCreateComplianceFact`, but output qualification can still allow compliance-like use. |
| 6. Lets aggregation become anonymisation by assertion? | **Partly controlled.** | `AggregationFloor` says aggregation does not equal anonymisation, good. But `AnonymisationClaim` can be approved with HIGH/UNKNOWN risk unless tightened. |
| 7. Distinguishes deidentification from anonymisation strongly enough? | **Conceptually yes; mechanically weak.** | The artifacts are separate. But approval/risk/review conditions need enforcement. |
| 8. Defines re-identification risk strongly enough? | **Incomplete.** | Risk assessment exists, but public/partner disclosure is not cross-checked against high risk. |
| 9. Preserves data sovereignty and revocation propagation? | **Conceptually yes; mechanically weak.** | Grants, recipient constraints, and revocation traces exist. Cross-record currentness/revocation checks are missing. |
| 10. Prevents CP13 local farm memory crossing boundaries without governance? | **Conceptually yes; mechanically incomplete.** | `LearningArtifactSharePackage` requires a grant and constraints, but farm-memory refs can appear without stronger checks. |
| 11. Preserves CP11 sustainability disclosure and claim-basis boundaries? | **Partial.** | CP11 trace/claim refs are not cross-checked before sustainability-sensitive cross-farm outputs. |
| 12. Preserves CP12 mission/incident disclosure boundaries? | **Partial.** | CP12 mission/incident signals are named, but no cross-record gate ensures incident telemetry disclosure is authorised/qualified. |
| 13. Accidentally creates CP15 model/software deployment law? | **Mostly no.** | Deployment is explicitly not authorised. But federated contribution / model improvement / training receipt logic must be hardened so it cannot imply deployment readiness. |
| 14. Accidentally creates Social, Exchange, benchmark product, or reputation law? | **Mostly no.** | The scope is bounded. Benchmark artifacts are present but not product law. Do not expand them. |
| 15. Defines enough conformance? | **No.** | Only a fixture plan exists. CP14 needs an executable runner with positive/negative and cross-record cases. |
| 16. Draft schemas preserve OFARM machine-contract style? | **Mostly yes.** | JSON Schema 2020-12, `additionalProperties: false`, refs, draft/non-default path, non-authorisation booleans. But conditional/cross-record rules are missing. |
| 17. Schemas too broad/narrow/wrongly named or accidentally implementing CP15? | **Some are too permissive.** | Biggest issues: `IntelligenceOutputQualification`, `FarmIntelligenceShareGrant`, `RecipientUseConstraint`, `AnonymisationClaim`, `RegionalAlert`, `FederatedLearningContribution`, `TrainingUseReceipt`, `RevocationPropagationTrace`. |

---

## Top defects

## Defect 1 — No executable CP14 conformance runner

**Severity:** High

The package includes only:

```text
CP14_farm_to_farm_intelligence_boundary_conformance_fixture_plan_v0_1.md
```

It explicitly says it is a draft fixture plan and not an executable runner.

**Why it matters**

CP14 is about cross-farm data, privacy, sovereignty, revocation, regional alerts, benchmarks, poisoning risk, and training-use boundaries. A fixture plan is not enough. Without executable cross-record tests, the schemas cannot prove the advisory-default and data-sovereignty rules.

**Required fix**

Create an executable conformance suite with:

```text
schema-aware validation
cross-record grant/use/revocation checks
reidentification-risk checks
recipient-use and redisclosure checks
training-use policy checks
CP11 disclosure/claim-basis checks
CP12 incident/mission disclosure checks
CP13 local-learning/farm-memory boundary checks
positive and negative fixtures
```

**Blocking for Phase 7:** Yes.

---

## Defect 2 — Share grants do not enforce temporal coherence or active-state requirements

**Severity:** High

`FarmIntelligenceShareGrant` requires:

```text
validFrom
validUntil
authorityDecisionTraceRef
```

but does not enforce:

```text
validUntil > validFrom
ACTIVE requires an approval/review decision
ACTIVE must not be expired at evaluation time
REVOKED/EXPIRED states must not be used for sharing
```

A grant with `validUntil` before `validFrom` currently passes schema validation.

**Why it matters**

An expired, impossible, or unapproved grant can become the basis for cross-farm disclosure.

**Required fix**

Add semantic conformance and schema conditions:

```text
validUntil must be after validFrom
ACTIVE requires approvalDecisionRef or authorityDecisionTraceRef and evaluationTime within validity window
REVOKED / EXPIRED / DENIED grants cannot support sharing
SUSPENDED grants cannot support new packages
```

Add fixtures:

```text
active_share_grant_invalid_time_window_fails
active_share_grant_expired_at_evaluation_time_fails
share_with_revoked_grant_fails
share_with_denied_grant_fails
valid_active_share_grant_passes
```

**Blocking for Phase 7:** Yes.

---

## Defect 3 — Allowed and prohibited use classes can overlap

**Severity:** High

These contracts allow the same use class to appear in both allowed and prohibited arrays:

```text
FarmIntelligenceShareGrant.allowedUseClasses / prohibitedUseClasses
RecipientUseConstraint.allowedUseClasses / prohibitedUseClasses
IntelligenceOutputQualification.allowedUseClasses / blockedUseClasses
ContributionQualityAssessment.usableForClasses / blockedUseClasses
```

This currently passes schema validation.

**Why it matters**

A downstream agent or system can read the allowed side and ignore the blocked side. This creates ambiguous authority and disclosure posture.

**Required fix**

Add no-overlap checks in semantic conformance. Where possible add schema constraints or runner checks:

```text
allowedUseClasses ∩ prohibitedUseClasses = ∅
allowedUseClasses ∩ blockedUseClasses = ∅
usableForClasses ∩ blockedUseClasses = ∅
```

Add fixtures:

```text
share_grant_allowed_prohibited_overlap_fails
recipient_use_allowed_prohibited_overlap_fails
intelligence_output_allowed_blocked_overlap_fails
contribution_quality_usable_blocked_overlap_fails
valid_non_overlapping_use_constraints_pass
```

**Blocking for Phase 7:** Yes.

---

## Defect 4 — Intelligence outputs can allow strong prohibited uses

**Severity:** High

`IntelligenceOutputQualification.allowedUseClasses` is free-form. It can include values such as:

```text
CREATE_FARM_TRUTH
CURRENT_STATE
COMPLIANCE_FACT
MISSION_AUTHORITY
MODEL_DEPLOYMENT
TRAINING_AUTHORITY
CLAIM_BEARING_OUTPUT
```

while the object still carries booleans like:

```text
doesNotCreateFarmTruth: true
doesNotCreateComplianceFact: true
doesNotAuthorizeMission: true
doesNotAuthorizeModelDeployment: true
```

**Why it matters**

This is the central CP14 boundary failure mode. A qualified intelligence output must never grant farm truth, compliance fact, mission authority, or model deployment authority.

**Required fix**

Define a controlled `IntelligenceUseClass` enum. Forbid these globally in `allowedUseClasses`:

```text
FARM_TRUTH
CURRENT_STATE
COMPLIANCE_FACT
MISSION_AUTHORITY
MODEL_DEPLOYMENT
AUTOMATIC_EXECUTION
CP13_FARM_MEMORY_PROMOTION
UNQUALIFIED_SUSTAINABILITY_CLAIM
```

Require default blocked uses to include those classes.

Add fixtures:

```text
intelligence_output_allows_farm_truth_fails
intelligence_output_allows_compliance_fact_fails
intelligence_output_allows_mission_authority_fails
intelligence_output_allows_model_deployment_fails
valid_regional_alert_advisory_output_passes
valid_benchmark_advisory_output_passes
```

**Blocking for Phase 7:** Yes.

---

## Defect 5 — Regional alerts can be published without output qualification or local-applicability boundary

**Severity:** High

`RegionalAlert` can be:

```text
alertState = PUBLISHED
```

without requiring:

```text
outputQualificationRef
crossFarmApplicabilityAssessmentRef
local evidence requirement
correction/withdrawal pathway
```

**Why it matters**

A regional alert is useful, but it must remain Advisory by default. Published regional alerts should not be interpreted as farm-level occurrence truth or a local action instruction.

**Required fix**

If `RegionalAlert.alertState = PUBLISHED`, require:

```text
outputQualificationRef
at least one riskSignalRef
publicationAuthorityTraceRef or authorityDecisionTraceRef
```

And in conformance require any local farm use to pass through:

```text
CrossFarmApplicabilityAssessment
requiresLocalEvidenceBeforeAction = true
```

Add fixtures:

```text
published_regional_alert_without_output_qualification_fails
regional_alert_used_as_farm_occurrence_truth_fails
regional_alert_action_without_applicability_assessment_fails
valid_published_regional_alert_advisory_passes
```

**Blocking for Phase 7:** Yes.

---

## Defect 6 — BenchmarkDelta does not harden aggregation/deidentification/ranking enough

**Severity:** High

`BenchmarkDelta` includes:

```text
aggregationFloorRef
confidenceClass
doesNotCreateComplianceFact
doesNotCreateFarmRankingByDefault
```

but does not require deidentification/anonymisation, output qualification, or re-identification risk handling by state/use.

It can also carry `confidenceClass = HIGH` without proving quality, aggregation floor strength, or low re-identification risk.

**Why it matters**

Benchmark deltas can become coercive commercial ranking, buyer leverage, insurance risk, or pseudo-compliance.

**Required fix**

For `benchmarkState = PUBLISHED_ADVISORY`, require:

```text
outputQualificationRef
aggregationFloorRef
reidentificationRiskAssessmentRef or deidentificationClaimRef
```

For any public/partner benchmark output, require:

```text
AggregationFloor.floorState = ACTIVE
minimumSourceFarmCount >= policy minimum
high re-identification risk blocks public/partner disclosure
```

Add fixtures:

```text
published_benchmark_without_output_qualification_fails
benchmark_with_weak_aggregation_floor_for_public_output_fails
benchmark_high_reidentification_risk_public_output_fails
benchmark_delta_as_compliance_fact_fails
valid_benchmark_advisory_with_floor_and_low_risk_passes
```

**Blocking for Phase 7:** Yes.

---

## Defect 7 — AggregationFloor is too permissive for privacy-sensitive use

**Severity:** Medium/high

`AggregationFloor` permits:

```text
minimumSourceFarmCount = 2
minimumDistinctOperatorCount = 1
minimumSpatialSeparationClass = NONE
minimumTemporalWindowClass = NONE
```

This may be acceptable for a draft object, but not for any public/partner benchmark or anonymisation-adjacent claim.

**Why it matters**

A small or poorly separated cohort can be re-identifiable. Aggregation is not anonymisation, but weak aggregation can still leak farm identity.

**Required fix**

Do not hardcode universal thresholds in baseline, but add policy-class thresholds:

```text
PUBLIC_BENCHMARK requires stronger aggregation floor
PARTNER_BENCHMARK requires minimum farm/operator count and separation
INTERNAL_ADVISORY can use lower floors with qualification
```

Add conformance checks that public/partner disclosure cannot rely on an insufficient floor.

**Blocking for public/partner benchmark claims:** Yes.

---

## Defect 8 — AnonymisationClaim and DeidentificationClaim approval is under-hardened

**Severity:** High

`AnonymisationClaim` can be `APPROVED` with:

```text
residualRiskClass = HIGH or UNKNOWN
approvalDecisionRef missing
```

`DeidentificationClaim` can be `CLAIMED` or `REVIEWED` without requiring an explicit re-identification risk assessment.

**Why it matters**

This reopens the core CP14 warning:

```text
aggregation/deidentification/anonymisation cannot be accepted by assertion.
```

**Required fix**

For `AnonymisationClaim.claimState = APPROVED`, require:

```text
approvalDecisionRef
reidentificationRiskAssessmentRef
residualRiskClass in [VERY_LOW, LOW]
methodClass not OTHER unless reviewDecisionRef present
```

For `DeidentificationClaim.claimState in [CLAIMED, REVIEWED]`, require:

```text
reidentificationRiskAssessmentRef
claimBasisRefs
outputQualificationRef or requiresOutputQualification true
```

Add fixtures:

```text
approved_anonymisation_high_risk_fails
approved_anonymisation_without_approval_fails
deidentification_claim_without_risk_assessment_fails
valid_reviewed_deidentification_claim_passes
valid_approved_anonymisation_low_risk_passes
```

**Blocking for Phase 7:** Yes.

---

## Defect 9 — Re-identification risk is not cross-checked against disclosure

**Severity:** High

`ReidentificationRiskAssessment` exists and has:

```text
riskClass
highRiskBlocksPublicDisclosure: true
```

But there is no cross-record enforcement connecting it to:

```text
IntelligenceOutputQualification
BenchmarkDelta
DeidentificationClaim
AnonymisationClaim
IntelligenceContributionPackage
```

**Why it matters**

A high-risk assessment should block public disclosure and usually block partner disclosure unless explicitly reviewed.

**Required fix**

Add cross-record conformance:

```text
if reidentification risk is HIGH or UNKNOWN_BLOCKING and highRiskBlocksPublicDisclosure = true,
then public disclosure must fail.
```

For partner disclosure, require review/approval and visible limitation.

Add fixtures:

```text
public_output_with_high_reidentification_risk_fails
partner_output_with_high_reidentification_risk_without_review_fails
valid_partner_output_high_risk_with_review_and_qualification_passes
```

**Blocking for Phase 7:** Yes.

---

## Defect 10 — Revocation propagation is not connected to grants, packages, outputs, or training use

**Severity:** High

`RevocationPropagationTrace` exists, but other contracts do not cross-check whether a grant, package, contribution, output, or training receipt is affected by an active revocation.

**Why it matters**

Farm-sovereignty law depends on revocation propagation. A revoked sharing grant should block new use, redisclosure, benchmark inclusion, regional alert use, and training use unless policy explicitly says otherwise.

**Required fix**

Add conformance checks:

```text
share with revoked grant fails
package with revoked grant fails
received contribution under revoked grant is quarantined or blocked
training receipt after revocation fails unless grandfathered by policy
revocationState = COMPLETE requires propagationCompletedAt and no unresolved recipients
revocationState = PARTIAL requires unresolvedRecipientRefs
revocationState = FAILED requires failureReasonRefs
```

Add fixtures:

```text
revoked_share_grant_used_for_package_fails
training_use_after_revocation_fails
revocation_complete_with_unresolved_recipients_fails
revocation_partial_without_unresolved_recipients_fails
valid_revocation_complete_passes
```

**Blocking for Phase 7:** Yes.

---

## Defect 11 — CP13 local farm memory can be shared too easily

**Severity:** High

`LearningArtifactSharePackage` requires:

```text
cp13LearningArtifactRefs
shareGrantRef
recipientUseConstraintRefs
```

but it allows `farmMemoryEntryRefs` without stronger state/approval checks. There is no cross-record conformance proving:

```text
farm memory is eligible to cross farm boundary
share grant permits farm-memory derivative sharing
recipient use constraints block local truth/current state/farm memory creation
```

**Why it matters**

CP13 farm memory is local and not hidden current state. CP14 must not turn it into cross-farm truth or recipient farm memory.

**Required fix**

For `LearningArtifactSharePackage` with `farmMemoryEntryRefs`, require:

```text
explicit share grant permission for FARM_MEMORY_DERIVATIVE
recipient use constraints blocking recipient farm memory creation
crossFarmApplicabilityAssessmentRef
output qualification
```

Add fixtures:

```text
farm_memory_share_without_cp14_permission_fails
farm_memory_share_creates_recipient_memory_fails
farm_memory_share_without_applicability_assessment_fails
valid_farm_memory_derivative_share_passes
```

**Blocking for Phase 7:** Yes.

---

## Defect 12 — CP11 sustainability disclosure and claim-basis boundary is under-enforced

**Severity:** Medium/high

CP14 introduces CP11 sustainability signal classes, but the machine contracts do not require CP11 claim-basis or output-qualification references when sustainability-sensitive intelligence is shared or published.

**Why it matters**

Sustainability signals can become greenwashing, buyer pressure, or certification-like assertions.

**Required fix**

For contribution or output classes containing:

```text
CP11_SUSTAINABILITY_SIGNAL
SUSTAINABILITY_RISK
UNQUALIFIED_SUSTAINABILITY_CLAIM
```

require:

```text
CP11 SustainabilityClaimBasis or SustainabilityOutputQualification where claim-bearing
CP11 charter evaluation trace where policy-sensitive
blocked use for compliance/certification unless separately governed
```

Add fixtures:

```text
sustainability_signal_without_cp11_qualification_fails
sustainability_signal_as_certification_claim_fails
valid_advisory_sustainability_signal_with_cp11_qualification_passes
```

**Blocking for CP11-sensitive sharing claims:** Yes.

---

## Defect 13 — CP12 mission/incident disclosure boundary is under-enforced

**Severity:** Medium/high

The schemas permit CP12 mission and incident signals, but do not enforce CP12 output/incident qualification before cross-farm sharing.

**Why it matters**

Mission telemetry, near-miss data, and physical-safety incidents can reveal commercial, safety, or liability-sensitive information.

**Required fix**

For contribution classes:

```text
CP12_MISSION_SIGNAL
CP12_INCIDENT_SIGNAL
MISSION_SAFETY_PATTERN
```

require:

```text
CP12 MissionOutputQualification or incident review reference
redaction/recipient-use constraints
no mission authority / no compliance fact / no liability determination posture
```

Add fixtures:

```text
mission_incident_signal_without_cp12_qualification_fails
incident_signal_as_compliance_or_liability_fact_fails
valid_redacted_mission_safety_pattern_passes
```

**Blocking for CP12-sensitive disclosure claims:** Yes.

---

## Defect 14 — Federated-learning contributions can be accepted with no privacy mechanism or non-compliant training policy

**Severity:** High

`FederatedLearningContribution` can be:

```text
contributionState = ACCEPTED_BY_AGGREGATOR
privacyMechanismClass = NONE_DECLARED
```

`TrainingUseReceipt` can be:

```text
receiptState = CONFIRMED
usedForTraining = true
policyCompliant = false
```

and still pass schema validation.

**Why it matters**

This is the CP15 boundary risk. CP14 may allow contribution/receipt tracking, but it must not allow ungoverned training or imply deployment authority.

**Required fix**

If `FederatedLearningContribution.contributionState in [SUBMITTED, ACCEPTED_BY_AGGREGATOR]`, require:

```text
trainingUsePolicyBindingRef active
shareGrantRef active
privacyMechanismClass != NONE_DECLARED unless explicitly review-approved
qualityAssessmentRef
poisoningOrAnomalyReviewRef for accepted contributions or high-risk contributions
```

If `TrainingUseReceipt.receiptState = CONFIRMED and usedForTraining = true`, require:

```text
policyCompliant = true
trainingUsePolicyBinding active
contributions covered by grants
```

Add fixtures:

```text
accepted_federated_contribution_without_privacy_mechanism_fails
confirmed_training_use_noncompliant_fails
training_use_without_policy_binding_fails
valid_federated_contribution_with_policy_and_privacy_passes
```

**Blocking for Phase 7:** Yes.

---

## Defect 15 — ModelImprovementSignal can overstate confidence without quality/federated receipt basis

**Severity:** Medium/high

`ModelImprovementSignal` allows:

```text
confidenceClass = HIGH
```

without requiring:

```text
federatedAggregationReceiptRef
quality assessment basis
privacy/training-use compliance
poisoning/anomaly review
```

**Why it matters**

A high-confidence model-improvement signal can be mistaken for model-update or deployment readiness.

**Required fix**

For `confidenceClass = HIGH`, require:

```text
federatedAggregationReceiptRef or basisRefs covering accepted receipt
ContributionQualityAssessment complete/low anomaly
PoisoningOrAnomalyReview no issue or qualified
training use receipts policy compliant
```

Always preserve:

```text
doesNotAuthorizeDeployment = true
cp15RequiredForDeployment = true
```

Add fixtures:

```text
high_confidence_model_signal_without_quality_basis_fails
model_signal_as_deployment_authority_fails
valid_model_improvement_advisory_signal_passes
```

**Blocking for high-confidence model-improvement claims:** Yes.

---

## Defect 16 — Poisoning/anomaly review is not integrated into use blocking

**Severity:** High

`PoisoningOrAnomalyReview` has dispositions such as:

```text
BLOCK_USE
QUARANTINE
WITHDRAW
REQUIRE_HUMAN_REVIEW
```

but contribution, alert, federated, benchmark, and model-improvement objects do not cross-check those dispositions.

**Why it matters**

A poisoned or anomalous contribution could still be used in regional alerts, benchmarks, federated aggregation, or model-improvement signals.

**Required fix**

Add cross-record conformance:

```text
If poisoning review disposition is BLOCK_USE, QUARANTINE, WITHDRAW, or REQUIRE_HUMAN_REVIEW, dependent alert/benchmark/federated/model outputs must block, quarantine, withdraw, or require review.
```

Add fixtures:

```text
poisoned_contribution_used_for_alert_fails
poisoned_contribution_used_for_benchmark_fails
poisoned_contribution_accepted_for_federated_learning_fails
valid_contribution_no_issue_passes
```

**Blocking for Phase 7:** Yes.

---

## Defect 17 — CrossFarmApplicabilityAssessment is advisory but not required enough before local action

**Severity:** Medium/high

`CrossFarmApplicabilityAssessment` correctly says:

```text
requiresLocalEvidenceBeforeAction = true
doesNotCreateLocalTruth = true
doesNotCreateFarmMemory = true
```

But the package does not require such an assessment before received intelligence is used for local recommendations, CP13 farm memory, or mission preparation.

**Why it matters**

Received intelligence should not drive farm-level action without local applicability and evidence gating.

**Required fix**

Add conformance rule:

```text
Received intelligence used for local recommendation, CP13 candidate memory, mission-preparation context, or high-consequence output requires CrossFarmApplicabilityAssessment and local evidence requirement.
```

Add fixtures:

```text
received_intelligence_used_for_local_action_without_applicability_fails
received_intelligence_used_for_farm_memory_without_applicability_fails
valid_received_alert_with_applicability_assessment_passes
```

**Blocking for high-consequence local-use claims:** Yes.

---

## Defect 18 — TrainingUsePolicyBinding is too permissive when training is allowed

**Severity:** Medium/high

`TrainingUsePolicyBinding` allows:

```text
trainingUseAllowed = true
```

without requiring:

```text
allowedTrainingPurposeClasses
recipientPartyRefs
targetModelFamilyRefs
retention/revocation posture
```

**Why it matters**

Training use is one of the most commercially sensitive CP14 surfaces.

**Required fix**

If `trainingUseAllowed = true`, require:

```text
allowedTrainingPurposeClasses minItems >= 1
recipientPartyRefs minItems >= 1
targetModelFamilyRefs minItems >= 1
trainingUseReceiptRequired = true
revocation/retention policy basis
```

If `trainingUseAllowed = false`, require prohibited purposes or all training blocked.

Add fixtures:

```text
training_allowed_without_purpose_recipient_model_fails
training_allowed_without_receipt_requirement_fails
valid_training_policy_binding_passes
```

**Blocking for training-use support:** Yes.

---

## Defect 19 — Package currentness/draft posture is acceptable but not hardened for final package hygiene

**Severity:** Medium

The CP14 schemas are staged under:

```text
03_machine_contracts/drafts_non_default/farm_to_farm_intelligence_boundary/
```

with:

```text
schemaVersion = cp14-v0.1-draft-phase5
```

That is acceptable at Phase 5. Before final package assembly, use a harmonised version string after remediation.

**Required fix**

After remediation:

```text
schemaVersion = cp14-v0.1-draft-phase6-1-remediated
```

or later final hardening versions as appropriate.

**Blocking now:** No.

---

## What CP14 got right

Despite the hardening gaps, CP14’s design direction is good.

Strong elements:

```text
1. Cross-farm intelligence is Advisory by default.
2. Farm-to-farm sharing is not authority.
3. Sharing grants are explicit.
4. Recipient use constraints are explicit.
5. Derivative-use and training-use surfaces are separated.
6. Revocation propagation is recognised.
7. Aggregation, deidentification, anonymisation, and reidentification risk are separate concepts.
8. Federated contribution is separated from model deployment.
9. Model-improvement signal does not authorise deployment.
10. Received intelligence does not create local truth, compliance facts, mission authority, or farm memory by itself.
11. CP15 is deferred.
12. OFARM Social and Exchange are not accidentally created.
```

The hostile review does **not** support a rewrite or split. It supports a hardening pass.

---

## Does CP14 need to be split?

No.

CP14 remains one coherent amendment:

```text
Farm-to-Farm Intelligence Boundary
```

Splitting it now would create unnecessary coordination risk. The defects are not because the amendment is conceptually too large; they are because cross-record checks and conformance are not yet executable.

Do not split into separate federated-learning, benchmark, alert, or data-sharing RFCs yet. If later implementation proves one surface too large, split after CP14 establishes the boundary.

---

## Required fixes before Phase 7

## P0 — Blocking fixes

These must be fixed before final CP14 package assembly:

```text
1. Build an executable CP14 conformance runner.
2. Add share-grant temporal/currentness/revocation checks.
3. Enforce no-overlap between allowed and prohibited/blocked uses.
4. Forbid intelligence outputs from allowing farm truth, current state, compliance fact, mission authority, model deployment, automatic execution, or unqualified claims.
5. Require output qualification and local-applicability boundaries for published regional alerts.
6. Harden benchmark outputs against compliance/ranking/public-disclosure misuse.
7. Harden anonymisation/deidentification approval/risk requirements.
8. Cross-check re-identification risk against output/disclosure posture.
9. Connect revocation propagation to grants, packages, outputs, and training use.
10. Prevent CP13 local farm memory from crossing farm boundaries without explicit CP14 governance.
11. Require CP11 qualification for sustainability-sensitive cross-farm disclosures.
12. Require CP12 qualification/redaction for mission/incident intelligence disclosures.
13. Harden federated-learning contribution and training-use receipt policy compliance.
14. Integrate poisoning/anomaly review into downstream use blocking.
```

## P1 — Strongly recommended fixes

```text
15. Add policy-class thresholds for AggregationFloor.
16. Require CrossFarmApplicabilityAssessment before local high-consequence use.
17. Harden TrainingUsePolicyBinding when training is allowed.
18. Harden ModelImprovementSignal confidence requirements.
19. Harmonise schema versions after remediation.
```

## P2 — Can remain open, but record explicitly

```text
20. Production federated-learning implementation details.
21. External data-space protocol conformance.
22. Public benchmark product policy.
23. OFARM Social / OFARM Exchange constitutions.
24. Legal/privacy/certification review.
25. Real re-identification risk methodology selection.
```

---

## Recommended Phase 6.1 remediation scope

CP14 Phase 6.1 should be a narrow remediation pass, not a redesign.

Affected schemas likely requiring revision:

```text
FarmIntelligenceShareGrant
RecipientUseConstraint
IntelligenceOutputQualification
RegionalAlert
RegionalRiskSignal
BenchmarkDelta
AggregationFloor
DeidentificationClaim
AnonymisationClaim
ReidentificationRiskAssessment
RevocationPropagationTrace
IntelligenceContributionPackage
LearningArtifactSharePackage
FederatedLearningContribution
FederatedAggregationReceipt
TrainingUsePolicyBinding
TrainingUseReceipt
ModelImprovementSignal
ContributionQualityAssessment
PoisoningOrAnomalyReview
CrossFarmApplicabilityAssessment
FarmIntelligenceContribution
FarmIntelligenceSharePolicy
```

Minimum executable fixtures:

```text
share_without_active_grant_fails
share_with_expired_grant_fails
allowed_prohibited_use_overlap_fails
received_intelligence_as_farm_truth_fails
regional_alert_as_farm_occurrence_truth_fails
published_regional_alert_without_qualification_fails
benchmark_delta_as_compliance_fact_fails
public_benchmark_without_aggregation_floor_fails
aggregation_claim_as_anonymisation_fails
approved_anonymisation_high_risk_fails
high_reidentification_risk_public_output_fails
farm_memory_share_without_cp14_permission_fails
sustainability_signal_without_cp11_qualification_fails
mission_incident_signal_without_cp12_qualification_fails
federated_contribution_authorizes_deployment_fails
accepted_federated_contribution_without_privacy_mechanism_fails
confirmed_training_use_noncompliant_fails
model_improvement_signal_authorizes_deployment_fails
poisoning_review_blocked_contribution_used_for_alert_fails
revoked_share_grant_without_revocation_propagation_fails
recipient_redisclosure_without_permission_fails
agent_tool_success_as_sharing_grant_fails
valid_share_grant_allows_regional_risk_signal_package_passes
valid_received_regional_alert_remains_advisory_passes
valid_benchmark_delta_with_aggregation_floor_passes
valid_deidentification_claim_with_reidentification_assessment_passes
valid_federated_learning_contribution_with_training_policy_passes
valid_revocation_propagation_trace_passes
```

---

## Acceptance recommendation

```text
Acceptance recommendation: ACCEPT WITH CHANGES.
Do not split CP14.
Do not return to Phase 0.
Do not merge CP14 as final baseline yet.
Do not promote CP14 schemas to current/default.
Do not start CP15 yet.
```

CP14 is on the right track. The next step is not design expansion; it is hardening the contracts so they mechanically enforce the farm-to-farm intelligence boundary.

---

## Recommended next prompt

```text
Start CP14 Phase 6.1.

Using the CP14 Phase 6 hostile review, produce a CP14 remediation plan.

For each P0 and P1 defect, provide:
- exact RFC text change;
- exact baseline patch change if needed;
- exact schema change;
- exact conformance fixture change;
- whether the change is blocking for Phase 7.

Then produce revised schema-style definitions only for the affected schemas:
- FarmIntelligenceShareGrant
- RecipientUseConstraint
- IntelligenceOutputQualification
- RegionalAlert
- RegionalRiskSignal
- BenchmarkDelta
- AggregationFloor
- DeidentificationClaim
- AnonymisationClaim
- ReidentificationRiskAssessment
- RevocationPropagationTrace
- IntelligenceContributionPackage
- LearningArtifactSharePackage
- FederatedLearningContribution
- FederatedAggregationReceipt
- TrainingUsePolicyBinding
- TrainingUseReceipt
- ModelImprovementSignal
- ContributionQualityAssessment
- PoisoningOrAnomalyReview
- CrossFarmApplicabilityAssessment
- FarmIntelligenceContribution
- FarmIntelligenceSharePolicy, if needed

Also produce:
- executable conformance fixture plan;
- minimum P0 runner specification;
- positive and negative fixture list.

Do not create CP15 contracts.
Do not create OFARM Social, OFARM Exchange, public benchmark product, or generic reputation contracts.
Do not promote CP11, CP12, CP13, or CP14 schemas to current/default.
Do not claim production farm-to-farm intelligence or federated-learning readiness.
Keep all CP14 machine contracts in drafts_non_default.
```
