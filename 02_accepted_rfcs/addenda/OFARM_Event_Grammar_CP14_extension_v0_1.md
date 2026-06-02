
# OFARM Event Grammar and Commit Matrix — CP14 Extension v0.1

Status: accepted/merged CP14 addendum; active RFC addendum below the active baseline

CP14 adds event/commit handling for cross-farm intelligence. These events do not create local farm truth, current state, Compliance Twin facts, or deployment authority merely by existing.

## Candidate event families

- FarmIntelligenceShareGrantCreated / Amended / Revoked
- FarmIntelligenceContributionCaptured
- IntelligenceContributionPackaged
- LearningArtifactSharePackageCreated
- RecipientUseConstraintAttached
- DerivativeUsePolicyAttached
- TrainingUsePolicyBindingAttached
- RevocationPropagationRecorded
- RegionalAlertPublished / Corrected / Withdrawn
- RegionalRiskSignalReceived
- BenchmarkDeltaProduced
- AggregationFloorDeclared
- DeidentificationClaimMade
- AnonymisationClaimMade
- ReidentificationRiskAssessed
- FederatedLearningContributionSubmitted
- FederatedAggregationReceiptRecorded
- TrainingUseReceiptRecorded
- ModelImprovementSignalRecorded
- ContributionQualityAssessed
- PoisoningOrAnomalyReviewRecorded
- CrossFarmApplicabilityAssessed
- IntelligenceOutputQualified

Default commit posture is evidence/advisory/governance candidate unless separately accepted through existing OFARM review, authority, evidence, output, and twin gates.
