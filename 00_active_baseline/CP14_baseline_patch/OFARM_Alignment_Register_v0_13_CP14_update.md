
# OFARM Alignment Register v0.13 — CP14 Update

Status: final CP14 alignment-register patch candidate  
Amendment: CP14 — Farm-to-Farm Intelligence Boundary

Add the CP14 concept family as OFARM-owned or OFARM-governed cross-farm intelligence boundary concepts. External data-space, certification, buyer, public-authority, social, exchange, or federated-learning systems may be anchors, profiles, mappings, evidence sources, attestations, or sister-platform references; they do not become hidden OFARM law.

## CP14 concept rows

| Concept | Domain | Alignment posture | External relationship | OFARM label | Reason |
|---|---|---|---|---|---|
| FarmIntelligenceBoundary | Cross-farm intelligence / Governance | OFARM_OWNED | Data-space/sister-platform references as anchors only | FarmIntelligenceBoundary | Governs cross-farm intelligence boundaries, advisory default, and non-authorisation rules. |
| FarmIntelligenceSharePolicy | Sharing / Governance | OFARM_OWNED | Contract/policy references as anchors | FarmIntelligenceSharePolicy | Defines what intelligence may be shared, with whom, for what purpose, and under what use constraints. |
| FarmIntelligenceShareGrant | Authority / Sharing | OFARM_OWNED | Existing SharingGrant foundation | FarmIntelligenceShareGrant | Specialised grant for intelligence sharing, recipient use, derivative use, training use, retention, onward sharing, and revocation. |
| FarmIntelligenceContribution | Cross-farm intelligence | OFARM_OWNED | External observations/signals as evidence candidates | FarmIntelligenceContribution | Represents contributed intelligence without making it farm truth. |
| IntelligenceContributionPackage | Packaging / Sharing | OFARM_OWNED | Data-package standards as mappings only | IntelligenceContributionPackage | Packages contribution, limitations, quality, permissions, and output posture. |
| LearningArtifactSharePackage | CP13 / Cross-farm intelligence | OFARM_OWNED | None | LearningArtifactSharePackage | Governs CP13 learning/farm-memory artifacts crossing farm boundaries. |
| RecipientUseConstraint | Sharing / Use restriction | OFARM_OWNED | Contract/policy references as anchors | RecipientUseConstraint | Defines recipient-side use limits, onward sharing, disclosure, and prohibited uses. |
| DerivativeUsePolicy | Sharing / Derivative use | OFARM_OWNED | Contract/policy references as anchors | DerivativeUsePolicy | Controls derivative analytics, summaries, benchmarks, and training derivatives. |
| TrainingUsePolicyBinding | Training / Use governance | OFARM_OWNED | Model-training policy references as anchors | TrainingUsePolicyBinding | Binds contribution use to allowed model/training purposes without creating CP15 deployment authority. |
| RevocationPropagationTrace | Sharing / Revocation | OFARM_OWNED | Existing revocation foundations | RevocationPropagationTrace | Traces revocation effects across packages, outputs, recipients, and training use. |
| RegionalAlert | Regional intelligence | OFARM_OWNED | Public/regional services as evidence or sister-platform sources | RegionalAlert | Represents regional alert outputs without creating farm-level occurrence truth. |
| RegionalRiskSignal | Regional intelligence | OFARM_OWNED | External risk feeds as anchors | RegionalRiskSignal | Represents regional risk signals as Advisory intelligence. |
| RegionalAlertCorrection | Regional intelligence | OFARM_OWNED | Correction/withdrawal references as evidence | RegionalAlertCorrection | Corrects or disputes regional alert outputs. |
| RegionalAlertWithdrawal | Regional intelligence | OFARM_OWNED | Withdrawal references as evidence | RegionalAlertWithdrawal | Withdraws alert outputs and blocks downstream use where required. |
| BenchmarkDelta | Benchmarking | OFARM_OWNED | Benchmark products as sister-platform/product references | BenchmarkDelta | Represents benchmark deltas without creating compliance facts or public ranking law. |
| AggregationFloor | Privacy / Aggregation | OFARM_OWNED | Statistical/privacy standards as anchors | AggregationFloor | States minimum aggregation conditions; not anonymisation by assertion. |
| DeidentificationClaim | Privacy / Disclosure | OFARM_OWNED | Privacy standards as anchors | DeidentificationClaim | Represents deidentification claim with risk basis. |
| AnonymisationClaim | Privacy / Disclosure | OFARM_OWNED | Privacy standards as anchors | AnonymisationClaim | Represents stronger anonymisation claim with approval and low re-identification risk requirements. |
| ReidentificationRiskAssessment | Privacy / Risk | OFARM_OWNED | Privacy risk methods as anchors | ReidentificationRiskAssessment | Controls disclosure posture and risk qualification. |
| FederatedLearningContribution | Federated learning boundary | OFARM_OWNED | Federated-learning systems as sister/platform references | FederatedLearningContribution | Contribution boundary only; not model deployment authority. |
| FederatedAggregationReceipt | Federated learning boundary | OFARM_OWNED | Federated aggregation system receipt | FederatedAggregationReceipt | Receipt/evidence candidate; not deployment authority. |
| ModelImprovementSignal | Model improvement boundary | OFARM_OWNED | CP15 future model-governance references | ModelImprovementSignal | Advisory model-improvement signal; not deployment authority. |
| TrainingUseReceipt | Training-use audit | OFARM_OWNED | Training systems as future CP15/sister refs | TrainingUseReceipt | Records training use under policy; not deployment law. |
| ContributionQualityAssessment | Quality / Security | OFARM_OWNED | Data-quality methods as anchors | ContributionQualityAssessment | Qualifies contribution usability and limitations. |
| PoisoningOrAnomalyReview | Security / Data quality | OFARM_OWNED | Security/anomaly methods as anchors | PoisoningOrAnomalyReview | Blocks or qualifies downstream use when poisoning/anomaly risk exists. |
| CrossFarmApplicabilityAssessment | Advisory / Applicability | OFARM_OWNED | None | CrossFarmApplicabilityAssessment | Required before received intelligence informs high-consequence local use. |
| IntelligenceOutputQualification | Output qualification | OFARM_OWNED | Result-qualification foundations | IntelligenceOutputQualification | Qualifies cross-farm outputs and blocks prohibited use classes. |

## CP14 alignment addendum

CP14 promotes the farm-to-farm intelligence boundary concept family as candidate baseline-recognised concepts. It does not promote CP14 machine contracts to current/default and does not create CP15, OFARM Social, OFARM Exchange, public benchmark product, or production federated-learning platform law.
