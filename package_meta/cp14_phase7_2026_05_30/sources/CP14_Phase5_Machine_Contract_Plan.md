# CP14 Phase 5 — Machine-Contract Plan

Date: 2026-05-29  
Status: CP14 Phase 5 draft machine-contract plan  
Amendment: CP14 — Farm-to-Farm Intelligence Boundary  

## Phase 5 verdict

```text
Status: draft/non-default machine-contract package
Current/default promotion: no
CP15 contracts: not created
OFARM Social / Exchange / public benchmark / reputation contracts: not created
Production farm-to-farm intelligence or federated-learning readiness claim: no
```

CP14's machine-contract layer should make cross-farm intelligence governable without converting it into truth, authority, compliance fact, public benchmark product law, model-deployment law, or production federated-learning platform readiness.

## Core invariant

```text
Cross-farm intelligence is advisory by default.
Farm-to-farm sharing is not authority.
Aggregation is not anonymisation by assertion.
Regional alerts are not farm-level truth.
Benchmark deltas are not compliance facts.
Federated-learning contribution is not model deployment authority.
CP13 local learning may not cross farm boundaries without CP14 governance.
```

## Contract families

### FarmIntelligenceBoundary

- **Purpose:** Declares the governed boundary for outgoing, incoming, transformed, or received cross-farm intelligence.
- **Required fields:** schemaVersion, artifactType, artifactId, createdAt, createdByPartyRef, boundaryState, boundaryDirection, dataSovereigntyBoundaryRefs, defaultTwinPosture, noFarmTruthCreation, noAuthorityCreation, noComplianceFactCreation, noModelDeploymentAuthority, cp15RequiredForDeployment.
- **Optional fields:** all declared schema properties not listed above, where applicable.
- **Validation rules:** JSON Schema 2020-12; `additionalProperties: false`; `schemaVersion` constant `cp14-v0.1-draft-phase5`; explicit artifact type; required authority/provenance where governance-relevant; no implicit truth/authority/deployment effects where guardrail fields apply.
- **Lifecycle:** draft/non-default CP14 schema; lifecycle is governed by its `*State` field where present; current/default promotion requires a later currentness decision.
- **Authority source:** existing OFARM authority, sharing, sovereignty, revocation, CP11 disclosure, CP12 incident/mission, and CP13 learning/farm-memory law as referenced by authority/grant/review fields.
- **Relation to events:** candidate event families include contribution packaged/shared/received, alert published/corrected/withdrawn, benchmark emitted, federated contribution submitted/aggregated, revocation propagated, quality/anomaly review completed, and output qualification emitted.
- **Relation to current-state materialisation:** Does not mutate current-state materialisation; received intelligence remains Advisory by default; stronger use requires separate governed OFARM gates.
- **Relation to Advisory Twin:** default target for received or cross-farm intelligence unless explicitly bridged by existing review/promotion/output gates.
- **Relation to Compliance Twin:** cannot create Compliance facts or claim basis by itself; Compliance use requires separate governed path.
- **Relation to CP11:** CP11 sustainability outputs or claim-supporting material may cross farm boundaries only through CP14 disclosure, grant, claim-basis, output-qualification, and sovereignty controls.
- **Relation to CP12:** mission/incident intelligence may be shared only as qualified intelligence; it does not create mission authority, execution truth, or safety certification.
- **Relation to CP13:** local learning and farm memory may not cross farm boundaries without CP14 packages, grants, use constraints, and applicability assessment.
- **Relation to CP15 deferral:** model-improvement and federated-learning signals do not create model/software deployment authority; CP15 remains required for deployment.
- **Conformance tests:** schema validation; positive example validation; negative fixtures for hidden truth, authority, disclosure, aggregation/anonymisation, revocation, poisoning, and deployment-boundary violations.
- **Example:** `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/farm_to_farm_intelligence_boundary/OFARM_FarmIntelligenceBoundary_example_v0_1.json`.
### FarmIntelligenceSharePolicy

- **Purpose:** Defines what farm intelligence may be shared, with whom, for what purpose, and under which restrictions.
- **Required fields:** schemaVersion, artifactType, artifactId, createdAt, createdByPartyRef, policyState, permittedIntelligenceClasses, allowedRecipientClasses, allowedPurposeClasses, requiredRecipientUseConstraintRefs, policyDoesNotConferAuthority.
- **Optional fields:** all declared schema properties not listed above, where applicable.
- **Validation rules:** JSON Schema 2020-12; `additionalProperties: false`; `schemaVersion` constant `cp14-v0.1-draft-phase5`; explicit artifact type; required authority/provenance where governance-relevant; no implicit truth/authority/deployment effects where guardrail fields apply.
- **Lifecycle:** draft/non-default CP14 schema; lifecycle is governed by its `*State` field where present; current/default promotion requires a later currentness decision.
- **Authority source:** existing OFARM authority, sharing, sovereignty, revocation, CP11 disclosure, CP12 incident/mission, and CP13 learning/farm-memory law as referenced by authority/grant/review fields.
- **Relation to events:** candidate event families include contribution packaged/shared/received, alert published/corrected/withdrawn, benchmark emitted, federated contribution submitted/aggregated, revocation propagated, quality/anomaly review completed, and output qualification emitted.
- **Relation to current-state materialisation:** Does not mutate current-state materialisation; received intelligence remains Advisory by default; stronger use requires separate governed OFARM gates.
- **Relation to Advisory Twin:** default target for received or cross-farm intelligence unless explicitly bridged by existing review/promotion/output gates.
- **Relation to Compliance Twin:** cannot create Compliance facts or claim basis by itself; Compliance use requires separate governed path.
- **Relation to CP11:** CP11 sustainability outputs or claim-supporting material may cross farm boundaries only through CP14 disclosure, grant, claim-basis, output-qualification, and sovereignty controls.
- **Relation to CP12:** mission/incident intelligence may be shared only as qualified intelligence; it does not create mission authority, execution truth, or safety certification.
- **Relation to CP13:** local learning and farm memory may not cross farm boundaries without CP14 packages, grants, use constraints, and applicability assessment.
- **Relation to CP15 deferral:** model-improvement and federated-learning signals do not create model/software deployment authority; CP15 remains required for deployment.
- **Conformance tests:** schema validation; positive example validation; negative fixtures for hidden truth, authority, disclosure, aggregation/anonymisation, revocation, poisoning, and deployment-boundary violations.
- **Example:** `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/farm_to_farm_intelligence_boundary/OFARM_FarmIntelligenceSharePolicy_example_v0_1.json`.
### FarmIntelligenceShareGrant

- **Purpose:** Specialised sharing grant for a concrete farm-intelligence sharing act or governed class of acts.
- **Required fields:** schemaVersion, artifactType, artifactId, createdAt, createdByPartyRef, grantState, grantorFarmScopeRef, recipientPartyRefs, sharePolicyRef, boundaryRef, intelligenceClassRefs, allowedUseClasses, validFrom, validUntil, authorityDecisionTraceRef, recipientUseConstraintRefs, revocable, grantDoesNotConferAuthority, grantDoesNotCreateTruth.
- **Optional fields:** all declared schema properties not listed above, where applicable.
- **Validation rules:** JSON Schema 2020-12; `additionalProperties: false`; `schemaVersion` constant `cp14-v0.1-draft-phase5`; explicit artifact type; required authority/provenance where governance-relevant; no implicit truth/authority/deployment effects where guardrail fields apply.
- **Lifecycle:** draft/non-default CP14 schema; lifecycle is governed by its `*State` field where present; current/default promotion requires a later currentness decision.
- **Authority source:** existing OFARM authority, sharing, sovereignty, revocation, CP11 disclosure, CP12 incident/mission, and CP13 learning/farm-memory law as referenced by authority/grant/review fields.
- **Relation to events:** candidate event families include contribution packaged/shared/received, alert published/corrected/withdrawn, benchmark emitted, federated contribution submitted/aggregated, revocation propagated, quality/anomaly review completed, and output qualification emitted.
- **Relation to current-state materialisation:** Does not mutate current-state materialisation; received intelligence remains Advisory by default; stronger use requires separate governed OFARM gates.
- **Relation to Advisory Twin:** default target for received or cross-farm intelligence unless explicitly bridged by existing review/promotion/output gates.
- **Relation to Compliance Twin:** cannot create Compliance facts or claim basis by itself; Compliance use requires separate governed path.
- **Relation to CP11:** CP11 sustainability outputs or claim-supporting material may cross farm boundaries only through CP14 disclosure, grant, claim-basis, output-qualification, and sovereignty controls.
- **Relation to CP12:** mission/incident intelligence may be shared only as qualified intelligence; it does not create mission authority, execution truth, or safety certification.
- **Relation to CP13:** local learning and farm memory may not cross farm boundaries without CP14 packages, grants, use constraints, and applicability assessment.
- **Relation to CP15 deferral:** model-improvement and federated-learning signals do not create model/software deployment authority; CP15 remains required for deployment.
- **Conformance tests:** schema validation; positive example validation; negative fixtures for hidden truth, authority, disclosure, aggregation/anonymisation, revocation, poisoning, and deployment-boundary violations.
- **Example:** `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/farm_to_farm_intelligence_boundary/OFARM_FarmIntelligenceShareGrant_example_v0_1.json`.
### FarmIntelligenceContribution

- **Purpose:** Represents one farm-scoped contribution prepared for cross-farm intelligence use.
- **Required fields:** schemaVersion, artifactType, artifactId, createdAt, createdByPartyRef, contributionState, contributionClass, sourceFarmScopeRef, shareGrantRef, doesNotCreateRecipientTruth, doesNotCreateComplianceFact, doesNotAuthorizeModelDeployment.
- **Optional fields:** all declared schema properties not listed above, where applicable.
- **Validation rules:** JSON Schema 2020-12; `additionalProperties: false`; `schemaVersion` constant `cp14-v0.1-draft-phase5`; explicit artifact type; required authority/provenance where governance-relevant; no implicit truth/authority/deployment effects where guardrail fields apply.
- **Lifecycle:** draft/non-default CP14 schema; lifecycle is governed by its `*State` field where present; current/default promotion requires a later currentness decision.
- **Authority source:** existing OFARM authority, sharing, sovereignty, revocation, CP11 disclosure, CP12 incident/mission, and CP13 learning/farm-memory law as referenced by authority/grant/review fields.
- **Relation to events:** candidate event families include contribution packaged/shared/received, alert published/corrected/withdrawn, benchmark emitted, federated contribution submitted/aggregated, revocation propagated, quality/anomaly review completed, and output qualification emitted.
- **Relation to current-state materialisation:** Does not mutate current-state materialisation; received intelligence remains Advisory by default; stronger use requires separate governed OFARM gates.
- **Relation to Advisory Twin:** default target for received or cross-farm intelligence unless explicitly bridged by existing review/promotion/output gates.
- **Relation to Compliance Twin:** cannot create Compliance facts or claim basis by itself; Compliance use requires separate governed path.
- **Relation to CP11:** CP11 sustainability outputs or claim-supporting material may cross farm boundaries only through CP14 disclosure, grant, claim-basis, output-qualification, and sovereignty controls.
- **Relation to CP12:** mission/incident intelligence may be shared only as qualified intelligence; it does not create mission authority, execution truth, or safety certification.
- **Relation to CP13:** local learning and farm memory may not cross farm boundaries without CP14 packages, grants, use constraints, and applicability assessment.
- **Relation to CP15 deferral:** model-improvement and federated-learning signals do not create model/software deployment authority; CP15 remains required for deployment.
- **Conformance tests:** schema validation; positive example validation; negative fixtures for hidden truth, authority, disclosure, aggregation/anonymisation, revocation, poisoning, and deployment-boundary violations.
- **Example:** `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/farm_to_farm_intelligence_boundary/OFARM_FarmIntelligenceContribution_example_v0_1.json`.
### IntelligenceContributionPackage

- **Purpose:** Packages one or more contributions with provenance, grant, aggregation, redaction, and output-qualification posture.
- **Required fields:** schemaVersion, artifactType, artifactId, createdAt, createdByPartyRef, packageState, contributionRefs, shareGrantRefs, sourceScopeClass, recipientUseConstraintRefs, outputQualificationRef, packageDoesNotCreateTruth.
- **Optional fields:** all declared schema properties not listed above, where applicable.
- **Validation rules:** JSON Schema 2020-12; `additionalProperties: false`; `schemaVersion` constant `cp14-v0.1-draft-phase5`; explicit artifact type; required authority/provenance where governance-relevant; no implicit truth/authority/deployment effects where guardrail fields apply.
- **Lifecycle:** draft/non-default CP14 schema; lifecycle is governed by its `*State` field where present; current/default promotion requires a later currentness decision.
- **Authority source:** existing OFARM authority, sharing, sovereignty, revocation, CP11 disclosure, CP12 incident/mission, and CP13 learning/farm-memory law as referenced by authority/grant/review fields.
- **Relation to events:** candidate event families include contribution packaged/shared/received, alert published/corrected/withdrawn, benchmark emitted, federated contribution submitted/aggregated, revocation propagated, quality/anomaly review completed, and output qualification emitted.
- **Relation to current-state materialisation:** Does not mutate current-state materialisation; received intelligence remains Advisory by default; stronger use requires separate governed OFARM gates.
- **Relation to Advisory Twin:** default target for received or cross-farm intelligence unless explicitly bridged by existing review/promotion/output gates.
- **Relation to Compliance Twin:** cannot create Compliance facts or claim basis by itself; Compliance use requires separate governed path.
- **Relation to CP11:** CP11 sustainability outputs or claim-supporting material may cross farm boundaries only through CP14 disclosure, grant, claim-basis, output-qualification, and sovereignty controls.
- **Relation to CP12:** mission/incident intelligence may be shared only as qualified intelligence; it does not create mission authority, execution truth, or safety certification.
- **Relation to CP13:** local learning and farm memory may not cross farm boundaries without CP14 packages, grants, use constraints, and applicability assessment.
- **Relation to CP15 deferral:** model-improvement and federated-learning signals do not create model/software deployment authority; CP15 remains required for deployment.
- **Conformance tests:** schema validation; positive example validation; negative fixtures for hidden truth, authority, disclosure, aggregation/anonymisation, revocation, poisoning, and deployment-boundary violations.
- **Example:** `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/farm_to_farm_intelligence_boundary/OFARM_IntelligenceContributionPackage_example_v0_1.json`.
### LearningArtifactSharePackage

- **Purpose:** Special package for CP13 local learning artifacts crossing farm boundaries under CP14 governance.
- **Required fields:** schemaVersion, artifactType, artifactId, createdAt, createdByPartyRef, packageState, cp13LearningArtifactRefs, shareGrantRef, recipientUseConstraintRefs, doesNotExportLocalFarmMemoryByDefault, doesNotCreateRecipientFarmMemory, doesNotCreateModelDeploymentAuthority.
- **Optional fields:** all declared schema properties not listed above, where applicable.
- **Validation rules:** JSON Schema 2020-12; `additionalProperties: false`; `schemaVersion` constant `cp14-v0.1-draft-phase5`; explicit artifact type; required authority/provenance where governance-relevant; no implicit truth/authority/deployment effects where guardrail fields apply.
- **Lifecycle:** draft/non-default CP14 schema; lifecycle is governed by its `*State` field where present; current/default promotion requires a later currentness decision.
- **Authority source:** existing OFARM authority, sharing, sovereignty, revocation, CP11 disclosure, CP12 incident/mission, and CP13 learning/farm-memory law as referenced by authority/grant/review fields.
- **Relation to events:** candidate event families include contribution packaged/shared/received, alert published/corrected/withdrawn, benchmark emitted, federated contribution submitted/aggregated, revocation propagated, quality/anomaly review completed, and output qualification emitted.
- **Relation to current-state materialisation:** Does not mutate current-state materialisation; received intelligence remains Advisory by default; stronger use requires separate governed OFARM gates.
- **Relation to Advisory Twin:** default target for received or cross-farm intelligence unless explicitly bridged by existing review/promotion/output gates.
- **Relation to Compliance Twin:** cannot create Compliance facts or claim basis by itself; Compliance use requires separate governed path.
- **Relation to CP11:** CP11 sustainability outputs or claim-supporting material may cross farm boundaries only through CP14 disclosure, grant, claim-basis, output-qualification, and sovereignty controls.
- **Relation to CP12:** mission/incident intelligence may be shared only as qualified intelligence; it does not create mission authority, execution truth, or safety certification.
- **Relation to CP13:** local learning and farm memory may not cross farm boundaries without CP14 packages, grants, use constraints, and applicability assessment.
- **Relation to CP15 deferral:** model-improvement and federated-learning signals do not create model/software deployment authority; CP15 remains required for deployment.
- **Conformance tests:** schema validation; positive example validation; negative fixtures for hidden truth, authority, disclosure, aggregation/anonymisation, revocation, poisoning, and deployment-boundary violations.
- **Example:** `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/farm_to_farm_intelligence_boundary/OFARM_LearningArtifactSharePackage_example_v0_1.json`.
### RecipientUseConstraint

- **Purpose:** Declares permitted, prohibited, retention, redisclosure, derivative-use, and training-use limits for a recipient.
- **Required fields:** schemaVersion, artifactType, artifactId, createdAt, createdByPartyRef, constraintState, recipientClass, allowedUseClasses, prohibitedUseClasses, redisclosurePosture, revocationPropagationRequired, useConstraintDoesNotConferAuthority.
- **Optional fields:** all declared schema properties not listed above, where applicable.
- **Validation rules:** JSON Schema 2020-12; `additionalProperties: false`; `schemaVersion` constant `cp14-v0.1-draft-phase5`; explicit artifact type; required authority/provenance where governance-relevant; no implicit truth/authority/deployment effects where guardrail fields apply.
- **Lifecycle:** draft/non-default CP14 schema; lifecycle is governed by its `*State` field where present; current/default promotion requires a later currentness decision.
- **Authority source:** existing OFARM authority, sharing, sovereignty, revocation, CP11 disclosure, CP12 incident/mission, and CP13 learning/farm-memory law as referenced by authority/grant/review fields.
- **Relation to events:** candidate event families include contribution packaged/shared/received, alert published/corrected/withdrawn, benchmark emitted, federated contribution submitted/aggregated, revocation propagated, quality/anomaly review completed, and output qualification emitted.
- **Relation to current-state materialisation:** Does not mutate current-state materialisation; received intelligence remains Advisory by default; stronger use requires separate governed OFARM gates.
- **Relation to Advisory Twin:** default target for received or cross-farm intelligence unless explicitly bridged by existing review/promotion/output gates.
- **Relation to Compliance Twin:** cannot create Compliance facts or claim basis by itself; Compliance use requires separate governed path.
- **Relation to CP11:** CP11 sustainability outputs or claim-supporting material may cross farm boundaries only through CP14 disclosure, grant, claim-basis, output-qualification, and sovereignty controls.
- **Relation to CP12:** mission/incident intelligence may be shared only as qualified intelligence; it does not create mission authority, execution truth, or safety certification.
- **Relation to CP13:** local learning and farm memory may not cross farm boundaries without CP14 packages, grants, use constraints, and applicability assessment.
- **Relation to CP15 deferral:** model-improvement and federated-learning signals do not create model/software deployment authority; CP15 remains required for deployment.
- **Conformance tests:** schema validation; positive example validation; negative fixtures for hidden truth, authority, disclosure, aggregation/anonymisation, revocation, poisoning, and deployment-boundary violations.
- **Example:** `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/farm_to_farm_intelligence_boundary/OFARM_RecipientUseConstraint_example_v0_1.json`.
### DerivativeUsePolicy

- **Purpose:** Controls whether and how recipients may derive new intelligence, outputs, products, or model signals from shared intelligence.
- **Required fields:** schemaVersion, artifactType, artifactId, createdAt, createdByPartyRef, policyState, prohibitedDerivativeClasses, recipientDisclosureRequired, derivativeOutputQualificationRequired, doesNotAuthorizeModelDeployment, cp15RequiredForDeployment.
- **Optional fields:** all declared schema properties not listed above, where applicable.
- **Validation rules:** JSON Schema 2020-12; `additionalProperties: false`; `schemaVersion` constant `cp14-v0.1-draft-phase5`; explicit artifact type; required authority/provenance where governance-relevant; no implicit truth/authority/deployment effects where guardrail fields apply.
- **Lifecycle:** draft/non-default CP14 schema; lifecycle is governed by its `*State` field where present; current/default promotion requires a later currentness decision.
- **Authority source:** existing OFARM authority, sharing, sovereignty, revocation, CP11 disclosure, CP12 incident/mission, and CP13 learning/farm-memory law as referenced by authority/grant/review fields.
- **Relation to events:** candidate event families include contribution packaged/shared/received, alert published/corrected/withdrawn, benchmark emitted, federated contribution submitted/aggregated, revocation propagated, quality/anomaly review completed, and output qualification emitted.
- **Relation to current-state materialisation:** Does not mutate current-state materialisation; received intelligence remains Advisory by default; stronger use requires separate governed OFARM gates.
- **Relation to Advisory Twin:** default target for received or cross-farm intelligence unless explicitly bridged by existing review/promotion/output gates.
- **Relation to Compliance Twin:** cannot create Compliance facts or claim basis by itself; Compliance use requires separate governed path.
- **Relation to CP11:** CP11 sustainability outputs or claim-supporting material may cross farm boundaries only through CP14 disclosure, grant, claim-basis, output-qualification, and sovereignty controls.
- **Relation to CP12:** mission/incident intelligence may be shared only as qualified intelligence; it does not create mission authority, execution truth, or safety certification.
- **Relation to CP13:** local learning and farm memory may not cross farm boundaries without CP14 packages, grants, use constraints, and applicability assessment.
- **Relation to CP15 deferral:** model-improvement and federated-learning signals do not create model/software deployment authority; CP15 remains required for deployment.
- **Conformance tests:** schema validation; positive example validation; negative fixtures for hidden truth, authority, disclosure, aggregation/anonymisation, revocation, poisoning, and deployment-boundary violations.
- **Example:** `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/farm_to_farm_intelligence_boundary/OFARM_DerivativeUsePolicy_example_v0_1.json`.
### TrainingUsePolicyBinding

- **Purpose:** Binds shared intelligence to training/model-improvement use restrictions without granting deployment authority.
- **Required fields:** schemaVersion, artifactType, artifactId, createdAt, createdByPartyRef, bindingState, trainingUseAllowed, trainingUseReceiptRequired, doesNotAuthorizeModelDeployment, doesNotAuthorizeFineTuningByDefault, cp15RequiredForDeployment.
- **Optional fields:** all declared schema properties not listed above, where applicable.
- **Validation rules:** JSON Schema 2020-12; `additionalProperties: false`; `schemaVersion` constant `cp14-v0.1-draft-phase5`; explicit artifact type; required authority/provenance where governance-relevant; no implicit truth/authority/deployment effects where guardrail fields apply.
- **Lifecycle:** draft/non-default CP14 schema; lifecycle is governed by its `*State` field where present; current/default promotion requires a later currentness decision.
- **Authority source:** existing OFARM authority, sharing, sovereignty, revocation, CP11 disclosure, CP12 incident/mission, and CP13 learning/farm-memory law as referenced by authority/grant/review fields.
- **Relation to events:** candidate event families include contribution packaged/shared/received, alert published/corrected/withdrawn, benchmark emitted, federated contribution submitted/aggregated, revocation propagated, quality/anomaly review completed, and output qualification emitted.
- **Relation to current-state materialisation:** Does not mutate current-state materialisation; received intelligence remains Advisory by default; stronger use requires separate governed OFARM gates.
- **Relation to Advisory Twin:** default target for received or cross-farm intelligence unless explicitly bridged by existing review/promotion/output gates.
- **Relation to Compliance Twin:** cannot create Compliance facts or claim basis by itself; Compliance use requires separate governed path.
- **Relation to CP11:** CP11 sustainability outputs or claim-supporting material may cross farm boundaries only through CP14 disclosure, grant, claim-basis, output-qualification, and sovereignty controls.
- **Relation to CP12:** mission/incident intelligence may be shared only as qualified intelligence; it does not create mission authority, execution truth, or safety certification.
- **Relation to CP13:** local learning and farm memory may not cross farm boundaries without CP14 packages, grants, use constraints, and applicability assessment.
- **Relation to CP15 deferral:** model-improvement and federated-learning signals do not create model/software deployment authority; CP15 remains required for deployment.
- **Conformance tests:** schema validation; positive example validation; negative fixtures for hidden truth, authority, disclosure, aggregation/anonymisation, revocation, poisoning, and deployment-boundary violations.
- **Example:** `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/farm_to_farm_intelligence_boundary/OFARM_TrainingUsePolicyBinding_example_v0_1.json`.
### RevocationPropagationTrace

- **Purpose:** Records propagation of a sharing, derivative-use, or training-use revocation to recipients and derivatives.
- **Required fields:** schemaVersion, artifactType, artifactId, createdAt, createdByPartyRef, revocationState, revocationDecisionRef, affectedGrantRefs, affectedRecipientRefs, propagationStartedAt, revocationDoesNotEraseHistory.
- **Optional fields:** all declared schema properties not listed above, where applicable.
- **Validation rules:** JSON Schema 2020-12; `additionalProperties: false`; `schemaVersion` constant `cp14-v0.1-draft-phase5`; explicit artifact type; required authority/provenance where governance-relevant; no implicit truth/authority/deployment effects where guardrail fields apply.
- **Lifecycle:** draft/non-default CP14 schema; lifecycle is governed by its `*State` field where present; current/default promotion requires a later currentness decision.
- **Authority source:** existing OFARM authority, sharing, sovereignty, revocation, CP11 disclosure, CP12 incident/mission, and CP13 learning/farm-memory law as referenced by authority/grant/review fields.
- **Relation to events:** candidate event families include contribution packaged/shared/received, alert published/corrected/withdrawn, benchmark emitted, federated contribution submitted/aggregated, revocation propagated, quality/anomaly review completed, and output qualification emitted.
- **Relation to current-state materialisation:** Does not mutate current-state materialisation; received intelligence remains Advisory by default; stronger use requires separate governed OFARM gates.
- **Relation to Advisory Twin:** default target for received or cross-farm intelligence unless explicitly bridged by existing review/promotion/output gates.
- **Relation to Compliance Twin:** cannot create Compliance facts or claim basis by itself; Compliance use requires separate governed path.
- **Relation to CP11:** CP11 sustainability outputs or claim-supporting material may cross farm boundaries only through CP14 disclosure, grant, claim-basis, output-qualification, and sovereignty controls.
- **Relation to CP12:** mission/incident intelligence may be shared only as qualified intelligence; it does not create mission authority, execution truth, or safety certification.
- **Relation to CP13:** local learning and farm memory may not cross farm boundaries without CP14 packages, grants, use constraints, and applicability assessment.
- **Relation to CP15 deferral:** model-improvement and federated-learning signals do not create model/software deployment authority; CP15 remains required for deployment.
- **Conformance tests:** schema validation; positive example validation; negative fixtures for hidden truth, authority, disclosure, aggregation/anonymisation, revocation, poisoning, and deployment-boundary violations.
- **Example:** `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/farm_to_farm_intelligence_boundary/OFARM_RevocationPropagationTrace_example_v0_1.json`.
### RegionalAlert

- **Purpose:** Represents regional advisory alert output derived from multiple signals/contributions.
- **Required fields:** schemaVersion, artifactType, artifactId, createdAt, createdByPartyRef, alertState, alertClass, regionalScopeRefs, temporalScope, riskSignalRefs, advisoryDefault, doesNotCreateFarmLevelTruth, doesNotCreateComplianceFact.
- **Optional fields:** all declared schema properties not listed above, where applicable.
- **Validation rules:** JSON Schema 2020-12; `additionalProperties: false`; `schemaVersion` constant `cp14-v0.1-draft-phase5`; explicit artifact type; required authority/provenance where governance-relevant; no implicit truth/authority/deployment effects where guardrail fields apply.
- **Lifecycle:** draft/non-default CP14 schema; lifecycle is governed by its `*State` field where present; current/default promotion requires a later currentness decision.
- **Authority source:** existing OFARM authority, sharing, sovereignty, revocation, CP11 disclosure, CP12 incident/mission, and CP13 learning/farm-memory law as referenced by authority/grant/review fields.
- **Relation to events:** candidate event families include contribution packaged/shared/received, alert published/corrected/withdrawn, benchmark emitted, federated contribution submitted/aggregated, revocation propagated, quality/anomaly review completed, and output qualification emitted.
- **Relation to current-state materialisation:** Does not mutate current-state materialisation; received intelligence remains Advisory by default; stronger use requires separate governed OFARM gates.
- **Relation to Advisory Twin:** default target for received or cross-farm intelligence unless explicitly bridged by existing review/promotion/output gates.
- **Relation to Compliance Twin:** cannot create Compliance facts or claim basis by itself; Compliance use requires separate governed path.
- **Relation to CP11:** CP11 sustainability outputs or claim-supporting material may cross farm boundaries only through CP14 disclosure, grant, claim-basis, output-qualification, and sovereignty controls.
- **Relation to CP12:** mission/incident intelligence may be shared only as qualified intelligence; it does not create mission authority, execution truth, or safety certification.
- **Relation to CP13:** local learning and farm memory may not cross farm boundaries without CP14 packages, grants, use constraints, and applicability assessment.
- **Relation to CP15 deferral:** model-improvement and federated-learning signals do not create model/software deployment authority; CP15 remains required for deployment.
- **Conformance tests:** schema validation; positive example validation; negative fixtures for hidden truth, authority, disclosure, aggregation/anonymisation, revocation, poisoning, and deployment-boundary violations.
- **Example:** `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/farm_to_farm_intelligence_boundary/OFARM_RegionalAlert_example_v0_1.json`.
### RegionalRiskSignal

- **Purpose:** Represents a regional risk signal that may support alerts or advisory regional intelligence.
- **Required fields:** schemaVersion, artifactType, artifactId, createdAt, createdByPartyRef, signalState, riskClass, regionalScopeRefs, sourceContributionRefs, confidenceClass, evidenceQualityState, doesNotCreateOccurrenceTruth, doesNotCreateFarmTruth.
- **Optional fields:** all declared schema properties not listed above, where applicable.
- **Validation rules:** JSON Schema 2020-12; `additionalProperties: false`; `schemaVersion` constant `cp14-v0.1-draft-phase5`; explicit artifact type; required authority/provenance where governance-relevant; no implicit truth/authority/deployment effects where guardrail fields apply.
- **Lifecycle:** draft/non-default CP14 schema; lifecycle is governed by its `*State` field where present; current/default promotion requires a later currentness decision.
- **Authority source:** existing OFARM authority, sharing, sovereignty, revocation, CP11 disclosure, CP12 incident/mission, and CP13 learning/farm-memory law as referenced by authority/grant/review fields.
- **Relation to events:** candidate event families include contribution packaged/shared/received, alert published/corrected/withdrawn, benchmark emitted, federated contribution submitted/aggregated, revocation propagated, quality/anomaly review completed, and output qualification emitted.
- **Relation to current-state materialisation:** Does not mutate current-state materialisation; received intelligence remains Advisory by default; stronger use requires separate governed OFARM gates.
- **Relation to Advisory Twin:** default target for received or cross-farm intelligence unless explicitly bridged by existing review/promotion/output gates.
- **Relation to Compliance Twin:** cannot create Compliance facts or claim basis by itself; Compliance use requires separate governed path.
- **Relation to CP11:** CP11 sustainability outputs or claim-supporting material may cross farm boundaries only through CP14 disclosure, grant, claim-basis, output-qualification, and sovereignty controls.
- **Relation to CP12:** mission/incident intelligence may be shared only as qualified intelligence; it does not create mission authority, execution truth, or safety certification.
- **Relation to CP13:** local learning and farm memory may not cross farm boundaries without CP14 packages, grants, use constraints, and applicability assessment.
- **Relation to CP15 deferral:** model-improvement and federated-learning signals do not create model/software deployment authority; CP15 remains required for deployment.
- **Conformance tests:** schema validation; positive example validation; negative fixtures for hidden truth, authority, disclosure, aggregation/anonymisation, revocation, poisoning, and deployment-boundary violations.
- **Example:** `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/farm_to_farm_intelligence_boundary/OFARM_RegionalRiskSignal_example_v0_1.json`.
### RegionalAlertCorrection

- **Purpose:** Records correction or amendment of a previously published regional alert.
- **Required fields:** schemaVersion, artifactType, artifactId, createdAt, createdByPartyRef, correctionState, targetAlertRef, correctionReasonClass, authorityDecisionTraceRef, notificationRequired, correctionDoesNotEraseHistory.
- **Optional fields:** all declared schema properties not listed above, where applicable.
- **Validation rules:** JSON Schema 2020-12; `additionalProperties: false`; `schemaVersion` constant `cp14-v0.1-draft-phase5`; explicit artifact type; required authority/provenance where governance-relevant; no implicit truth/authority/deployment effects where guardrail fields apply.
- **Lifecycle:** draft/non-default CP14 schema; lifecycle is governed by its `*State` field where present; current/default promotion requires a later currentness decision.
- **Authority source:** existing OFARM authority, sharing, sovereignty, revocation, CP11 disclosure, CP12 incident/mission, and CP13 learning/farm-memory law as referenced by authority/grant/review fields.
- **Relation to events:** candidate event families include contribution packaged/shared/received, alert published/corrected/withdrawn, benchmark emitted, federated contribution submitted/aggregated, revocation propagated, quality/anomaly review completed, and output qualification emitted.
- **Relation to current-state materialisation:** Does not mutate current-state materialisation; received intelligence remains Advisory by default; stronger use requires separate governed OFARM gates.
- **Relation to Advisory Twin:** default target for received or cross-farm intelligence unless explicitly bridged by existing review/promotion/output gates.
- **Relation to Compliance Twin:** cannot create Compliance facts or claim basis by itself; Compliance use requires separate governed path.
- **Relation to CP11:** CP11 sustainability outputs or claim-supporting material may cross farm boundaries only through CP14 disclosure, grant, claim-basis, output-qualification, and sovereignty controls.
- **Relation to CP12:** mission/incident intelligence may be shared only as qualified intelligence; it does not create mission authority, execution truth, or safety certification.
- **Relation to CP13:** local learning and farm memory may not cross farm boundaries without CP14 packages, grants, use constraints, and applicability assessment.
- **Relation to CP15 deferral:** model-improvement and federated-learning signals do not create model/software deployment authority; CP15 remains required for deployment.
- **Conformance tests:** schema validation; positive example validation; negative fixtures for hidden truth, authority, disclosure, aggregation/anonymisation, revocation, poisoning, and deployment-boundary violations.
- **Example:** `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/farm_to_farm_intelligence_boundary/OFARM_RegionalAlertCorrection_example_v0_1.json`.
### RegionalAlertWithdrawal

- **Purpose:** Records withdrawal of a regional alert without deleting history.
- **Required fields:** schemaVersion, artifactType, artifactId, createdAt, createdByPartyRef, withdrawalState, targetAlertRef, withdrawalReasonClass, authorityDecisionTraceRef, notificationRequired, withdrawalDoesNotEraseHistory.
- **Optional fields:** all declared schema properties not listed above, where applicable.
- **Validation rules:** JSON Schema 2020-12; `additionalProperties: false`; `schemaVersion` constant `cp14-v0.1-draft-phase5`; explicit artifact type; required authority/provenance where governance-relevant; no implicit truth/authority/deployment effects where guardrail fields apply.
- **Lifecycle:** draft/non-default CP14 schema; lifecycle is governed by its `*State` field where present; current/default promotion requires a later currentness decision.
- **Authority source:** existing OFARM authority, sharing, sovereignty, revocation, CP11 disclosure, CP12 incident/mission, and CP13 learning/farm-memory law as referenced by authority/grant/review fields.
- **Relation to events:** candidate event families include contribution packaged/shared/received, alert published/corrected/withdrawn, benchmark emitted, federated contribution submitted/aggregated, revocation propagated, quality/anomaly review completed, and output qualification emitted.
- **Relation to current-state materialisation:** Does not mutate current-state materialisation; received intelligence remains Advisory by default; stronger use requires separate governed OFARM gates.
- **Relation to Advisory Twin:** default target for received or cross-farm intelligence unless explicitly bridged by existing review/promotion/output gates.
- **Relation to Compliance Twin:** cannot create Compliance facts or claim basis by itself; Compliance use requires separate governed path.
- **Relation to CP11:** CP11 sustainability outputs or claim-supporting material may cross farm boundaries only through CP14 disclosure, grant, claim-basis, output-qualification, and sovereignty controls.
- **Relation to CP12:** mission/incident intelligence may be shared only as qualified intelligence; it does not create mission authority, execution truth, or safety certification.
- **Relation to CP13:** local learning and farm memory may not cross farm boundaries without CP14 packages, grants, use constraints, and applicability assessment.
- **Relation to CP15 deferral:** model-improvement and federated-learning signals do not create model/software deployment authority; CP15 remains required for deployment.
- **Conformance tests:** schema validation; positive example validation; negative fixtures for hidden truth, authority, disclosure, aggregation/anonymisation, revocation, poisoning, and deployment-boundary violations.
- **Example:** `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/farm_to_farm_intelligence_boundary/OFARM_RegionalAlertWithdrawal_example_v0_1.json`.
### BenchmarkDelta

- **Purpose:** Represents a benchmark delta between a farm/cohort and a governed comparison group without creating compliance fact.
- **Required fields:** schemaVersion, artifactType, artifactId, createdAt, createdByPartyRef, benchmarkState, metricProfileRef, subjectScopeRef, cohortDefinitionRef, aggregationFloorRef, deltaValue, deltaUnitRef, confidenceClass, doesNotCreateComplianceFact, doesNotCreateFarmRankingByDefault.
- **Optional fields:** all declared schema properties not listed above, where applicable.
- **Validation rules:** JSON Schema 2020-12; `additionalProperties: false`; `schemaVersion` constant `cp14-v0.1-draft-phase5`; explicit artifact type; required authority/provenance where governance-relevant; no implicit truth/authority/deployment effects where guardrail fields apply.
- **Lifecycle:** draft/non-default CP14 schema; lifecycle is governed by its `*State` field where present; current/default promotion requires a later currentness decision.
- **Authority source:** existing OFARM authority, sharing, sovereignty, revocation, CP11 disclosure, CP12 incident/mission, and CP13 learning/farm-memory law as referenced by authority/grant/review fields.
- **Relation to events:** candidate event families include contribution packaged/shared/received, alert published/corrected/withdrawn, benchmark emitted, federated contribution submitted/aggregated, revocation propagated, quality/anomaly review completed, and output qualification emitted.
- **Relation to current-state materialisation:** Does not mutate current-state materialisation; received intelligence remains Advisory by default; stronger use requires separate governed OFARM gates.
- **Relation to Advisory Twin:** default target for received or cross-farm intelligence unless explicitly bridged by existing review/promotion/output gates.
- **Relation to Compliance Twin:** cannot create Compliance facts or claim basis by itself; Compliance use requires separate governed path.
- **Relation to CP11:** CP11 sustainability outputs or claim-supporting material may cross farm boundaries only through CP14 disclosure, grant, claim-basis, output-qualification, and sovereignty controls.
- **Relation to CP12:** mission/incident intelligence may be shared only as qualified intelligence; it does not create mission authority, execution truth, or safety certification.
- **Relation to CP13:** local learning and farm memory may not cross farm boundaries without CP14 packages, grants, use constraints, and applicability assessment.
- **Relation to CP15 deferral:** model-improvement and federated-learning signals do not create model/software deployment authority; CP15 remains required for deployment.
- **Conformance tests:** schema validation; positive example validation; negative fixtures for hidden truth, authority, disclosure, aggregation/anonymisation, revocation, poisoning, and deployment-boundary violations.
- **Example:** `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/farm_to_farm_intelligence_boundary/OFARM_BenchmarkDelta_example_v0_1.json`.
### AggregationFloor

- **Purpose:** Declares minimum cohort and suppression requirements for aggregate cross-farm intelligence.
- **Required fields:** schemaVersion, artifactType, artifactId, createdAt, createdByPartyRef, floorState, minimumSourceFarmCount, minimumDistinctOperatorCount, minimumSpatialSeparationClass, minimumTemporalWindowClass, smallCellSuppressionRequired, aggregationDoesNotEqualAnonymisation.
- **Optional fields:** all declared schema properties not listed above, where applicable.
- **Validation rules:** JSON Schema 2020-12; `additionalProperties: false`; `schemaVersion` constant `cp14-v0.1-draft-phase5`; explicit artifact type; required authority/provenance where governance-relevant; no implicit truth/authority/deployment effects where guardrail fields apply.
- **Lifecycle:** draft/non-default CP14 schema; lifecycle is governed by its `*State` field where present; current/default promotion requires a later currentness decision.
- **Authority source:** existing OFARM authority, sharing, sovereignty, revocation, CP11 disclosure, CP12 incident/mission, and CP13 learning/farm-memory law as referenced by authority/grant/review fields.
- **Relation to events:** candidate event families include contribution packaged/shared/received, alert published/corrected/withdrawn, benchmark emitted, federated contribution submitted/aggregated, revocation propagated, quality/anomaly review completed, and output qualification emitted.
- **Relation to current-state materialisation:** Does not mutate current-state materialisation; received intelligence remains Advisory by default; stronger use requires separate governed OFARM gates.
- **Relation to Advisory Twin:** default target for received or cross-farm intelligence unless explicitly bridged by existing review/promotion/output gates.
- **Relation to Compliance Twin:** cannot create Compliance facts or claim basis by itself; Compliance use requires separate governed path.
- **Relation to CP11:** CP11 sustainability outputs or claim-supporting material may cross farm boundaries only through CP14 disclosure, grant, claim-basis, output-qualification, and sovereignty controls.
- **Relation to CP12:** mission/incident intelligence may be shared only as qualified intelligence; it does not create mission authority, execution truth, or safety certification.
- **Relation to CP13:** local learning and farm memory may not cross farm boundaries without CP14 packages, grants, use constraints, and applicability assessment.
- **Relation to CP15 deferral:** model-improvement and federated-learning signals do not create model/software deployment authority; CP15 remains required for deployment.
- **Conformance tests:** schema validation; positive example validation; negative fixtures for hidden truth, authority, disclosure, aggregation/anonymisation, revocation, poisoning, and deployment-boundary violations.
- **Example:** `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/farm_to_farm_intelligence_boundary/OFARM_AggregationFloor_example_v0_1.json`.
### DeidentificationClaim

- **Purpose:** Claims deidentification of a data/intelligence package with residual risk and method basis.
- **Required fields:** schemaVersion, artifactType, artifactId, createdAt, createdByPartyRef, claimState, subjectPackageRef, methodClass, residualRiskClass, claimBasisRefs, doesNotAssertIrreversibleAnonymisation, requiresOutputQualification.
- **Optional fields:** all declared schema properties not listed above, where applicable.
- **Validation rules:** JSON Schema 2020-12; `additionalProperties: false`; `schemaVersion` constant `cp14-v0.1-draft-phase5`; explicit artifact type; required authority/provenance where governance-relevant; no implicit truth/authority/deployment effects where guardrail fields apply.
- **Lifecycle:** draft/non-default CP14 schema; lifecycle is governed by its `*State` field where present; current/default promotion requires a later currentness decision.
- **Authority source:** existing OFARM authority, sharing, sovereignty, revocation, CP11 disclosure, CP12 incident/mission, and CP13 learning/farm-memory law as referenced by authority/grant/review fields.
- **Relation to events:** candidate event families include contribution packaged/shared/received, alert published/corrected/withdrawn, benchmark emitted, federated contribution submitted/aggregated, revocation propagated, quality/anomaly review completed, and output qualification emitted.
- **Relation to current-state materialisation:** Does not mutate current-state materialisation; received intelligence remains Advisory by default; stronger use requires separate governed OFARM gates.
- **Relation to Advisory Twin:** default target for received or cross-farm intelligence unless explicitly bridged by existing review/promotion/output gates.
- **Relation to Compliance Twin:** cannot create Compliance facts or claim basis by itself; Compliance use requires separate governed path.
- **Relation to CP11:** CP11 sustainability outputs or claim-supporting material may cross farm boundaries only through CP14 disclosure, grant, claim-basis, output-qualification, and sovereignty controls.
- **Relation to CP12:** mission/incident intelligence may be shared only as qualified intelligence; it does not create mission authority, execution truth, or safety certification.
- **Relation to CP13:** local learning and farm memory may not cross farm boundaries without CP14 packages, grants, use constraints, and applicability assessment.
- **Relation to CP15 deferral:** model-improvement and federated-learning signals do not create model/software deployment authority; CP15 remains required for deployment.
- **Conformance tests:** schema validation; positive example validation; negative fixtures for hidden truth, authority, disclosure, aggregation/anonymisation, revocation, poisoning, and deployment-boundary violations.
- **Example:** `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/farm_to_farm_intelligence_boundary/OFARM_DeidentificationClaim_example_v0_1.json`.
### AnonymisationClaim

- **Purpose:** Stronger anonymisation claim requiring explicit method/review basis; aggregation alone is insufficient.
- **Required fields:** schemaVersion, artifactType, artifactId, createdAt, createdByPartyRef, claimState, subjectPackageRef, methodClass, residualRiskClass, reidentificationRiskAssessmentRef, anonymisationNotInferredFromAggregation, irreversibilityNotAssumedByAssertion, requiresReview.
- **Optional fields:** all declared schema properties not listed above, where applicable.
- **Validation rules:** JSON Schema 2020-12; `additionalProperties: false`; `schemaVersion` constant `cp14-v0.1-draft-phase5`; explicit artifact type; required authority/provenance where governance-relevant; no implicit truth/authority/deployment effects where guardrail fields apply.
- **Lifecycle:** draft/non-default CP14 schema; lifecycle is governed by its `*State` field where present; current/default promotion requires a later currentness decision.
- **Authority source:** existing OFARM authority, sharing, sovereignty, revocation, CP11 disclosure, CP12 incident/mission, and CP13 learning/farm-memory law as referenced by authority/grant/review fields.
- **Relation to events:** candidate event families include contribution packaged/shared/received, alert published/corrected/withdrawn, benchmark emitted, federated contribution submitted/aggregated, revocation propagated, quality/anomaly review completed, and output qualification emitted.
- **Relation to current-state materialisation:** Does not mutate current-state materialisation; received intelligence remains Advisory by default; stronger use requires separate governed OFARM gates.
- **Relation to Advisory Twin:** default target for received or cross-farm intelligence unless explicitly bridged by existing review/promotion/output gates.
- **Relation to Compliance Twin:** cannot create Compliance facts or claim basis by itself; Compliance use requires separate governed path.
- **Relation to CP11:** CP11 sustainability outputs or claim-supporting material may cross farm boundaries only through CP14 disclosure, grant, claim-basis, output-qualification, and sovereignty controls.
- **Relation to CP12:** mission/incident intelligence may be shared only as qualified intelligence; it does not create mission authority, execution truth, or safety certification.
- **Relation to CP13:** local learning and farm memory may not cross farm boundaries without CP14 packages, grants, use constraints, and applicability assessment.
- **Relation to CP15 deferral:** model-improvement and federated-learning signals do not create model/software deployment authority; CP15 remains required for deployment.
- **Conformance tests:** schema validation; positive example validation; negative fixtures for hidden truth, authority, disclosure, aggregation/anonymisation, revocation, poisoning, and deployment-boundary violations.
- **Example:** `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/farm_to_farm_intelligence_boundary/OFARM_AnonymisationClaim_example_v0_1.json`.
### ReidentificationRiskAssessment

- **Purpose:** Assesses re-identification risk for deidentified, anonymised, or aggregate intelligence.
- **Required fields:** schemaVersion, artifactType, artifactId, createdAt, createdByPartyRef, assessmentState, subjectPackageRef, riskClass, attackerModelClass, highRiskBlocksPublicDisclosure.
- **Optional fields:** all declared schema properties not listed above, where applicable.
- **Validation rules:** JSON Schema 2020-12; `additionalProperties: false`; `schemaVersion` constant `cp14-v0.1-draft-phase5`; explicit artifact type; required authority/provenance where governance-relevant; no implicit truth/authority/deployment effects where guardrail fields apply.
- **Lifecycle:** draft/non-default CP14 schema; lifecycle is governed by its `*State` field where present; current/default promotion requires a later currentness decision.
- **Authority source:** existing OFARM authority, sharing, sovereignty, revocation, CP11 disclosure, CP12 incident/mission, and CP13 learning/farm-memory law as referenced by authority/grant/review fields.
- **Relation to events:** candidate event families include contribution packaged/shared/received, alert published/corrected/withdrawn, benchmark emitted, federated contribution submitted/aggregated, revocation propagated, quality/anomaly review completed, and output qualification emitted.
- **Relation to current-state materialisation:** Does not mutate current-state materialisation; received intelligence remains Advisory by default; stronger use requires separate governed OFARM gates.
- **Relation to Advisory Twin:** default target for received or cross-farm intelligence unless explicitly bridged by existing review/promotion/output gates.
- **Relation to Compliance Twin:** cannot create Compliance facts or claim basis by itself; Compliance use requires separate governed path.
- **Relation to CP11:** CP11 sustainability outputs or claim-supporting material may cross farm boundaries only through CP14 disclosure, grant, claim-basis, output-qualification, and sovereignty controls.
- **Relation to CP12:** mission/incident intelligence may be shared only as qualified intelligence; it does not create mission authority, execution truth, or safety certification.
- **Relation to CP13:** local learning and farm memory may not cross farm boundaries without CP14 packages, grants, use constraints, and applicability assessment.
- **Relation to CP15 deferral:** model-improvement and federated-learning signals do not create model/software deployment authority; CP15 remains required for deployment.
- **Conformance tests:** schema validation; positive example validation; negative fixtures for hidden truth, authority, disclosure, aggregation/anonymisation, revocation, poisoning, and deployment-boundary violations.
- **Example:** `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/farm_to_farm_intelligence_boundary/OFARM_ReidentificationRiskAssessment_example_v0_1.json`.
### FederatedLearningContribution

- **Purpose:** Represents a bounded federated-learning contribution without deployment authority.
- **Required fields:** schemaVersion, artifactType, artifactId, createdAt, createdByPartyRef, contributionState, sourceFarmScopeRef, shareGrantRef, trainingUsePolicyBindingRef, targetModelFamilyRef, privacyMechanismClass, contributionPayloadDigest, doesNotAuthorizeModelDeployment, cp15RequiredForDeployment.
- **Optional fields:** all declared schema properties not listed above, where applicable.
- **Validation rules:** JSON Schema 2020-12; `additionalProperties: false`; `schemaVersion` constant `cp14-v0.1-draft-phase5`; explicit artifact type; required authority/provenance where governance-relevant; no implicit truth/authority/deployment effects where guardrail fields apply.
- **Lifecycle:** draft/non-default CP14 schema; lifecycle is governed by its `*State` field where present; current/default promotion requires a later currentness decision.
- **Authority source:** existing OFARM authority, sharing, sovereignty, revocation, CP11 disclosure, CP12 incident/mission, and CP13 learning/farm-memory law as referenced by authority/grant/review fields.
- **Relation to events:** candidate event families include contribution packaged/shared/received, alert published/corrected/withdrawn, benchmark emitted, federated contribution submitted/aggregated, revocation propagated, quality/anomaly review completed, and output qualification emitted.
- **Relation to current-state materialisation:** Does not mutate current-state materialisation; received intelligence remains Advisory by default; stronger use requires separate governed OFARM gates.
- **Relation to Advisory Twin:** default target for received or cross-farm intelligence unless explicitly bridged by existing review/promotion/output gates.
- **Relation to Compliance Twin:** cannot create Compliance facts or claim basis by itself; Compliance use requires separate governed path.
- **Relation to CP11:** CP11 sustainability outputs or claim-supporting material may cross farm boundaries only through CP14 disclosure, grant, claim-basis, output-qualification, and sovereignty controls.
- **Relation to CP12:** mission/incident intelligence may be shared only as qualified intelligence; it does not create mission authority, execution truth, or safety certification.
- **Relation to CP13:** local learning and farm memory may not cross farm boundaries without CP14 packages, grants, use constraints, and applicability assessment.
- **Relation to CP15 deferral:** model-improvement and federated-learning signals do not create model/software deployment authority; CP15 remains required for deployment.
- **Conformance tests:** schema validation; positive example validation; negative fixtures for hidden truth, authority, disclosure, aggregation/anonymisation, revocation, poisoning, and deployment-boundary violations.
- **Example:** `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/farm_to_farm_intelligence_boundary/OFARM_FederatedLearningContribution_example_v0_1.json`.
### FederatedAggregationReceipt

- **Purpose:** Receipt from a federated aggregator indicating aggregation processing without model deployment authority.
- **Required fields:** schemaVersion, artifactType, artifactId, createdAt, createdByPartyRef, receiptState, aggregatorPartyRef, federatedContributionRefs, doesNotDeployModel, doesNotAuthorizeModelUpdate.
- **Optional fields:** all declared schema properties not listed above, where applicable.
- **Validation rules:** JSON Schema 2020-12; `additionalProperties: false`; `schemaVersion` constant `cp14-v0.1-draft-phase5`; explicit artifact type; required authority/provenance where governance-relevant; no implicit truth/authority/deployment effects where guardrail fields apply.
- **Lifecycle:** draft/non-default CP14 schema; lifecycle is governed by its `*State` field where present; current/default promotion requires a later currentness decision.
- **Authority source:** existing OFARM authority, sharing, sovereignty, revocation, CP11 disclosure, CP12 incident/mission, and CP13 learning/farm-memory law as referenced by authority/grant/review fields.
- **Relation to events:** candidate event families include contribution packaged/shared/received, alert published/corrected/withdrawn, benchmark emitted, federated contribution submitted/aggregated, revocation propagated, quality/anomaly review completed, and output qualification emitted.
- **Relation to current-state materialisation:** Does not mutate current-state materialisation; received intelligence remains Advisory by default; stronger use requires separate governed OFARM gates.
- **Relation to Advisory Twin:** default target for received or cross-farm intelligence unless explicitly bridged by existing review/promotion/output gates.
- **Relation to Compliance Twin:** cannot create Compliance facts or claim basis by itself; Compliance use requires separate governed path.
- **Relation to CP11:** CP11 sustainability outputs or claim-supporting material may cross farm boundaries only through CP14 disclosure, grant, claim-basis, output-qualification, and sovereignty controls.
- **Relation to CP12:** mission/incident intelligence may be shared only as qualified intelligence; it does not create mission authority, execution truth, or safety certification.
- **Relation to CP13:** local learning and farm memory may not cross farm boundaries without CP14 packages, grants, use constraints, and applicability assessment.
- **Relation to CP15 deferral:** model-improvement and federated-learning signals do not create model/software deployment authority; CP15 remains required for deployment.
- **Conformance tests:** schema validation; positive example validation; negative fixtures for hidden truth, authority, disclosure, aggregation/anonymisation, revocation, poisoning, and deployment-boundary violations.
- **Example:** `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/farm_to_farm_intelligence_boundary/OFARM_FederatedAggregationReceipt_example_v0_1.json`.
### ModelImprovementSignal

- **Purpose:** Signals potential model improvement without granting model deployment, training, or update authority.
- **Required fields:** schemaVersion, artifactType, artifactId, createdAt, createdByPartyRef, signalState, targetModelFamilyRef, basisRefs, improvementClaimClass, confidenceClass, doesNotAuthorizeDeployment, doesNotAuthorizeFineTuning, cp15RequiredForDeployment.
- **Optional fields:** all declared schema properties not listed above, where applicable.
- **Validation rules:** JSON Schema 2020-12; `additionalProperties: false`; `schemaVersion` constant `cp14-v0.1-draft-phase5`; explicit artifact type; required authority/provenance where governance-relevant; no implicit truth/authority/deployment effects where guardrail fields apply.
- **Lifecycle:** draft/non-default CP14 schema; lifecycle is governed by its `*State` field where present; current/default promotion requires a later currentness decision.
- **Authority source:** existing OFARM authority, sharing, sovereignty, revocation, CP11 disclosure, CP12 incident/mission, and CP13 learning/farm-memory law as referenced by authority/grant/review fields.
- **Relation to events:** candidate event families include contribution packaged/shared/received, alert published/corrected/withdrawn, benchmark emitted, federated contribution submitted/aggregated, revocation propagated, quality/anomaly review completed, and output qualification emitted.
- **Relation to current-state materialisation:** Does not mutate current-state materialisation; received intelligence remains Advisory by default; stronger use requires separate governed OFARM gates.
- **Relation to Advisory Twin:** default target for received or cross-farm intelligence unless explicitly bridged by existing review/promotion/output gates.
- **Relation to Compliance Twin:** cannot create Compliance facts or claim basis by itself; Compliance use requires separate governed path.
- **Relation to CP11:** CP11 sustainability outputs or claim-supporting material may cross farm boundaries only through CP14 disclosure, grant, claim-basis, output-qualification, and sovereignty controls.
- **Relation to CP12:** mission/incident intelligence may be shared only as qualified intelligence; it does not create mission authority, execution truth, or safety certification.
- **Relation to CP13:** local learning and farm memory may not cross farm boundaries without CP14 packages, grants, use constraints, and applicability assessment.
- **Relation to CP15 deferral:** model-improvement and federated-learning signals do not create model/software deployment authority; CP15 remains required for deployment.
- **Conformance tests:** schema validation; positive example validation; negative fixtures for hidden truth, authority, disclosure, aggregation/anonymisation, revocation, poisoning, and deployment-boundary violations.
- **Example:** `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/farm_to_farm_intelligence_boundary/OFARM_ModelImprovementSignal_example_v0_1.json`.
### TrainingUseReceipt

- **Purpose:** Records use or non-use of shared intelligence for training purposes under a binding policy.
- **Required fields:** schemaVersion, artifactType, artifactId, createdAt, createdByPartyRef, receiptState, trainingUsePolicyBindingRef, contributionRefs, recipientPartyRef, trainingPurposeClass, usedForTraining, policyCompliant, doesNotAuthorizeDeployment.
- **Optional fields:** all declared schema properties not listed above, where applicable.
- **Validation rules:** JSON Schema 2020-12; `additionalProperties: false`; `schemaVersion` constant `cp14-v0.1-draft-phase5`; explicit artifact type; required authority/provenance where governance-relevant; no implicit truth/authority/deployment effects where guardrail fields apply.
- **Lifecycle:** draft/non-default CP14 schema; lifecycle is governed by its `*State` field where present; current/default promotion requires a later currentness decision.
- **Authority source:** existing OFARM authority, sharing, sovereignty, revocation, CP11 disclosure, CP12 incident/mission, and CP13 learning/farm-memory law as referenced by authority/grant/review fields.
- **Relation to events:** candidate event families include contribution packaged/shared/received, alert published/corrected/withdrawn, benchmark emitted, federated contribution submitted/aggregated, revocation propagated, quality/anomaly review completed, and output qualification emitted.
- **Relation to current-state materialisation:** Does not mutate current-state materialisation; received intelligence remains Advisory by default; stronger use requires separate governed OFARM gates.
- **Relation to Advisory Twin:** default target for received or cross-farm intelligence unless explicitly bridged by existing review/promotion/output gates.
- **Relation to Compliance Twin:** cannot create Compliance facts or claim basis by itself; Compliance use requires separate governed path.
- **Relation to CP11:** CP11 sustainability outputs or claim-supporting material may cross farm boundaries only through CP14 disclosure, grant, claim-basis, output-qualification, and sovereignty controls.
- **Relation to CP12:** mission/incident intelligence may be shared only as qualified intelligence; it does not create mission authority, execution truth, or safety certification.
- **Relation to CP13:** local learning and farm memory may not cross farm boundaries without CP14 packages, grants, use constraints, and applicability assessment.
- **Relation to CP15 deferral:** model-improvement and federated-learning signals do not create model/software deployment authority; CP15 remains required for deployment.
- **Conformance tests:** schema validation; positive example validation; negative fixtures for hidden truth, authority, disclosure, aggregation/anonymisation, revocation, poisoning, and deployment-boundary violations.
- **Example:** `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/farm_to_farm_intelligence_boundary/OFARM_TrainingUseReceipt_example_v0_1.json`.
### ContributionQualityAssessment

- **Purpose:** Assesses quality, completeness, freshness, anomaly, poisoning, and usability posture of a contribution.
- **Required fields:** schemaVersion, artifactType, artifactId, createdAt, createdByPartyRef, assessmentState, targetContributionRef, completenessClass, freshnessClass, anomalyClass, assessmentDoesNotCreateTruth.
- **Optional fields:** all declared schema properties not listed above, where applicable.
- **Validation rules:** JSON Schema 2020-12; `additionalProperties: false`; `schemaVersion` constant `cp14-v0.1-draft-phase5`; explicit artifact type; required authority/provenance where governance-relevant; no implicit truth/authority/deployment effects where guardrail fields apply.
- **Lifecycle:** draft/non-default CP14 schema; lifecycle is governed by its `*State` field where present; current/default promotion requires a later currentness decision.
- **Authority source:** existing OFARM authority, sharing, sovereignty, revocation, CP11 disclosure, CP12 incident/mission, and CP13 learning/farm-memory law as referenced by authority/grant/review fields.
- **Relation to events:** candidate event families include contribution packaged/shared/received, alert published/corrected/withdrawn, benchmark emitted, federated contribution submitted/aggregated, revocation propagated, quality/anomaly review completed, and output qualification emitted.
- **Relation to current-state materialisation:** Does not mutate current-state materialisation; received intelligence remains Advisory by default; stronger use requires separate governed OFARM gates.
- **Relation to Advisory Twin:** default target for received or cross-farm intelligence unless explicitly bridged by existing review/promotion/output gates.
- **Relation to Compliance Twin:** cannot create Compliance facts or claim basis by itself; Compliance use requires separate governed path.
- **Relation to CP11:** CP11 sustainability outputs or claim-supporting material may cross farm boundaries only through CP14 disclosure, grant, claim-basis, output-qualification, and sovereignty controls.
- **Relation to CP12:** mission/incident intelligence may be shared only as qualified intelligence; it does not create mission authority, execution truth, or safety certification.
- **Relation to CP13:** local learning and farm memory may not cross farm boundaries without CP14 packages, grants, use constraints, and applicability assessment.
- **Relation to CP15 deferral:** model-improvement and federated-learning signals do not create model/software deployment authority; CP15 remains required for deployment.
- **Conformance tests:** schema validation; positive example validation; negative fixtures for hidden truth, authority, disclosure, aggregation/anonymisation, revocation, poisoning, and deployment-boundary violations.
- **Example:** `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/farm_to_farm_intelligence_boundary/OFARM_ContributionQualityAssessment_example_v0_1.json`.
### PoisoningOrAnomalyReview

- **Purpose:** Reviews suspicious contributions, alerts, benchmark deltas, or federated updates for poisoning/anomaly risk.
- **Required fields:** schemaVersion, artifactType, artifactId, createdAt, createdByPartyRef, reviewState, targetRefs, anomalyClass, severityClass, reviewDisposition, reviewDoesNotDeleteEvidence.
- **Optional fields:** all declared schema properties not listed above, where applicable.
- **Validation rules:** JSON Schema 2020-12; `additionalProperties: false`; `schemaVersion` constant `cp14-v0.1-draft-phase5`; explicit artifact type; required authority/provenance where governance-relevant; no implicit truth/authority/deployment effects where guardrail fields apply.
- **Lifecycle:** draft/non-default CP14 schema; lifecycle is governed by its `*State` field where present; current/default promotion requires a later currentness decision.
- **Authority source:** existing OFARM authority, sharing, sovereignty, revocation, CP11 disclosure, CP12 incident/mission, and CP13 learning/farm-memory law as referenced by authority/grant/review fields.
- **Relation to events:** candidate event families include contribution packaged/shared/received, alert published/corrected/withdrawn, benchmark emitted, federated contribution submitted/aggregated, revocation propagated, quality/anomaly review completed, and output qualification emitted.
- **Relation to current-state materialisation:** Does not mutate current-state materialisation; received intelligence remains Advisory by default; stronger use requires separate governed OFARM gates.
- **Relation to Advisory Twin:** default target for received or cross-farm intelligence unless explicitly bridged by existing review/promotion/output gates.
- **Relation to Compliance Twin:** cannot create Compliance facts or claim basis by itself; Compliance use requires separate governed path.
- **Relation to CP11:** CP11 sustainability outputs or claim-supporting material may cross farm boundaries only through CP14 disclosure, grant, claim-basis, output-qualification, and sovereignty controls.
- **Relation to CP12:** mission/incident intelligence may be shared only as qualified intelligence; it does not create mission authority, execution truth, or safety certification.
- **Relation to CP13:** local learning and farm memory may not cross farm boundaries without CP14 packages, grants, use constraints, and applicability assessment.
- **Relation to CP15 deferral:** model-improvement and federated-learning signals do not create model/software deployment authority; CP15 remains required for deployment.
- **Conformance tests:** schema validation; positive example validation; negative fixtures for hidden truth, authority, disclosure, aggregation/anonymisation, revocation, poisoning, and deployment-boundary violations.
- **Example:** `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/farm_to_farm_intelligence_boundary/OFARM_PoisoningOrAnomalyReview_example_v0_1.json`.
### CrossFarmApplicabilityAssessment

- **Purpose:** Assesses whether received cross-farm intelligence is applicable to a target farm context.
- **Required fields:** schemaVersion, artifactType, artifactId, createdAt, createdByPartyRef, assessmentState, receivedIntelligenceRef, targetFarmContextRef, applicabilityClass, requiresLocalEvidenceBeforeAction, doesNotCreateLocalTruth, doesNotCreateFarmMemory.
- **Optional fields:** all declared schema properties not listed above, where applicable.
- **Validation rules:** JSON Schema 2020-12; `additionalProperties: false`; `schemaVersion` constant `cp14-v0.1-draft-phase5`; explicit artifact type; required authority/provenance where governance-relevant; no implicit truth/authority/deployment effects where guardrail fields apply.
- **Lifecycle:** draft/non-default CP14 schema; lifecycle is governed by its `*State` field where present; current/default promotion requires a later currentness decision.
- **Authority source:** existing OFARM authority, sharing, sovereignty, revocation, CP11 disclosure, CP12 incident/mission, and CP13 learning/farm-memory law as referenced by authority/grant/review fields.
- **Relation to events:** candidate event families include contribution packaged/shared/received, alert published/corrected/withdrawn, benchmark emitted, federated contribution submitted/aggregated, revocation propagated, quality/anomaly review completed, and output qualification emitted.
- **Relation to current-state materialisation:** Does not mutate current-state materialisation; received intelligence remains Advisory by default; stronger use requires separate governed OFARM gates.
- **Relation to Advisory Twin:** default target for received or cross-farm intelligence unless explicitly bridged by existing review/promotion/output gates.
- **Relation to Compliance Twin:** cannot create Compliance facts or claim basis by itself; Compliance use requires separate governed path.
- **Relation to CP11:** CP11 sustainability outputs or claim-supporting material may cross farm boundaries only through CP14 disclosure, grant, claim-basis, output-qualification, and sovereignty controls.
- **Relation to CP12:** mission/incident intelligence may be shared only as qualified intelligence; it does not create mission authority, execution truth, or safety certification.
- **Relation to CP13:** local learning and farm memory may not cross farm boundaries without CP14 packages, grants, use constraints, and applicability assessment.
- **Relation to CP15 deferral:** model-improvement and federated-learning signals do not create model/software deployment authority; CP15 remains required for deployment.
- **Conformance tests:** schema validation; positive example validation; negative fixtures for hidden truth, authority, disclosure, aggregation/anonymisation, revocation, poisoning, and deployment-boundary violations.
- **Example:** `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/farm_to_farm_intelligence_boundary/OFARM_CrossFarmApplicabilityAssessment_example_v0_1.json`.
### IntelligenceOutputQualification

- **Purpose:** Qualifies cross-farm intelligence outputs with permitted/prohibited uses, source posture, advisory status, and disclosure limits.
- **Required fields:** schemaVersion, artifactType, artifactId, createdAt, createdByPartyRef, qualificationState, outputDisposition, allowedUseClasses, blockedUseClasses, sourcePosture, advisoryDefault, doesNotCreateFarmTruth, doesNotCreateComplianceFact, doesNotAuthorizeMission, doesNotAuthorizeModelDeployment.
- **Optional fields:** all declared schema properties not listed above, where applicable.
- **Validation rules:** JSON Schema 2020-12; `additionalProperties: false`; `schemaVersion` constant `cp14-v0.1-draft-phase5`; explicit artifact type; required authority/provenance where governance-relevant; no implicit truth/authority/deployment effects where guardrail fields apply.
- **Lifecycle:** draft/non-default CP14 schema; lifecycle is governed by its `*State` field where present; current/default promotion requires a later currentness decision.
- **Authority source:** existing OFARM authority, sharing, sovereignty, revocation, CP11 disclosure, CP12 incident/mission, and CP13 learning/farm-memory law as referenced by authority/grant/review fields.
- **Relation to events:** candidate event families include contribution packaged/shared/received, alert published/corrected/withdrawn, benchmark emitted, federated contribution submitted/aggregated, revocation propagated, quality/anomaly review completed, and output qualification emitted.
- **Relation to current-state materialisation:** Does not mutate current-state materialisation; received intelligence remains Advisory by default; stronger use requires separate governed OFARM gates.
- **Relation to Advisory Twin:** default target for received or cross-farm intelligence unless explicitly bridged by existing review/promotion/output gates.
- **Relation to Compliance Twin:** cannot create Compliance facts or claim basis by itself; Compliance use requires separate governed path.
- **Relation to CP11:** CP11 sustainability outputs or claim-supporting material may cross farm boundaries only through CP14 disclosure, grant, claim-basis, output-qualification, and sovereignty controls.
- **Relation to CP12:** mission/incident intelligence may be shared only as qualified intelligence; it does not create mission authority, execution truth, or safety certification.
- **Relation to CP13:** local learning and farm memory may not cross farm boundaries without CP14 packages, grants, use constraints, and applicability assessment.
- **Relation to CP15 deferral:** model-improvement and federated-learning signals do not create model/software deployment authority; CP15 remains required for deployment.
- **Conformance tests:** schema validation; positive example validation; negative fixtures for hidden truth, authority, disclosure, aggregation/anonymisation, revocation, poisoning, and deployment-boundary violations.
- **Example:** `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/farm_to_farm_intelligence_boundary/OFARM_IntelligenceOutputQualification_example_v0_1.json`.


## Conformance fixture families

Minimum CP14 conformance should include:

```text
share_grant_required_for_cross_farm_package
sharing_grant_does_not_create_authority
received_regional_alert_stays_advisory
regional_alert_does_not_create_farm_occurrence_truth
benchmark_delta_does_not_create_compliance_fact
aggregation_floor_missing_blocks_public_benchmark
aggregation_claim_not_equal_anonymisation
anonymisation_claim_requires_reidentification_assessment
high_reidentification_risk_blocks_public_output
farm_memory_share_without_cp14_grant_fails
learning_artifact_share_package_requires_recipient_use_constraint
cp12_incident_signal_share_requires_grant_and_output_qualification
federated_learning_contribution_does_not_authorize_model_deployment
model_improvement_signal_requires_cp15_for_deployment
training_use_receipt_must_match_training_policy_binding
revocation_propagation_required_after_share_grant_revocation
recipient_redisclosure_without_permission_fails
poisoning_review_quarantines_suspicious_contribution
regional_alert_correction_does_not_delete_history
regional_alert_withdrawal_propagates_to recipients
cross_farm_applicability_assessment_required_before local reliance
intelligence_output_qualification_blocks_compliance_fact_use
agent_tool_success_does_not_create_sharing_grant
```

## Phase 5 non-claims

CP14 Phase 5 does not claim production farm-to-farm intelligence readiness, production federated-learning platform readiness, legal/privacy/certification/advice readiness, public benchmark product readiness, OFARM Social or Exchange readiness, or CP15 model/software deployment governance.
