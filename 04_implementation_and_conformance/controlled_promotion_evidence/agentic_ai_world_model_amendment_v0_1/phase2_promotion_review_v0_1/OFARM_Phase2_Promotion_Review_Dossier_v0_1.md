# OFARM Agentic AI and World-Model Amendment — Phase 2 Promotion Review Dossier v0.1

Date: 2026-05-14  
Status: supporting review package; no active promotion applied  
Phase: P2 — promotion review of existing AI/app support material

## 1. Purpose

This dossier continues the Agentic AI and World-Model amendment by reviewing existing AI-agent-ready platform support material for possible controlled promotion.

This phase deliberately does **not** copy anything into `01_companion_artifacts/`, `02_accepted_rfcs/`, or `03_machine_contracts/`. Instead it stages review copies under this supporting folder and records artifact-by-artifact recommendations.

## 2. Authority posture

The active authority set remains unchanged. The review copies in `review_copies_not_active/` are convenience copies only. They are not active law, not accepted RFCs, and not active machine contracts.

The phase follows these rules:

- baseline law wins over all reviewed material;
- active accepted RFCs win over supporting drafts;
- app/agent surfaces must not become hidden truth stores;
- preflight/dry-run must not become execution by another name;
- capability declarations must not become readiness claims;
- no runtime conformance is claimed without implementation evidence.

## 3. Phase 2 conclusion

The existing AI-agent-ready platform work is valuable and mostly compatible with the agentic OFARM direction. The strongest near-term promotion candidates are public operation description, preflight/dry-run/explain, result qualification, runtime problem reason codes, trace retrieval, current-state/query display policies, and output preview discipline.

The material that should remain held is calculation/formula behavior, minimum capture profile, SDK/reference skeletons, two-agent execution evidence, and conformance execution reports.

## 4. Companion candidates

|Artifact|Recommendation|Target|Rationale|
|---|---|---|---|
|OFARM_AI_Agent_Use_and_Autonomy_Policy_v0_1.md|GREEN|01_companion_artifacts/OFARM_AI_Agent_Use_and_Autonomy_Policy_v0_1.md|Promote as companion after status wording is changed from draft; it gives the runtime/AI autonomy boundary without changing model law.|
|OFARM_Current_State_App_Display_and_Cache_Policy_v0_1.md|GREEN|01_companion_artifacts/OFARM_Current_State_App_Display_and_Cache_Policy_v0_1.md|Promote as companion; it protects governed current-state materialization from becoming app truth.|
|OFARM_Query_Result_Display_and_Freshness_Policy_v0_1.md|GREEN|01_companion_artifacts/OFARM_Query_Result_Display_and_Freshness_Policy_v0_1.md|Promote as companion; it protects QuerySpecification/result usage, freshness, redaction, and permission-limited answers.|
|OFARM_Application_Workflow_State_Matrix_v0_1.md|GREEN_WITH_REVIEW|01_companion_artifacts/OFARM_Application_Workflow_State_Matrix_v0_1.md|Promote as companion guidance if it remains UI/app language guidance rather than model law.|
|OFARM_Source_Fidelity_Loss_Map_and_FMIS_Shadow_Import_Boundary_Policy_v0_1.md|GREEN_WITH_REVIEW|01_companion_artifacts/OFARM_Source_Fidelity_Loss_Map_and_FMIS_Shadow_Import_Boundary_Policy_v0_1.md|Promote as companion; it preserves candidate-only import posture and makes loss visible.|
|OFARM_Application_Workflow_Cookbook_Policy_v0_1.md|AMBER_SUPPORT_ONLY|01_companion_artifacts/OFARM_Application_Workflow_Cookbook_Policy_v0_1.md|Hold as supporting until recipes and operation names are tested against public surfaces.|
|OFARM_Minimum_Capture_Profile_Boundary_Policy_v0_1.md|HOLD|01_companion_artifacts/OFARM_Minimum_Capture_Profile_Boundary_Policy_v0_1.md|Do not promote yet; minimum-capture could be mistaken as weaker evidence law without owner/live evidence and hostile review.|

## 5. RFC candidates

|Artifact|Recommendation|Target|Rationale|
|---|---|---|---|
|OFARM_Application_Builder_Surface_RFC_v0_1.md|GREEN|02_accepted_rfcs/OFARM_Application_Builder_Surface_RFC_v0_1.md|Promote after public/internal boundary review; needed so implementers and agents use governed public surfaces.|
|OFARM_Preflight_DryRun_and_Explain_Surface_RFC_v0_1.md|GREEN|02_accepted_rfcs/OFARM_Preflight_DryRun_and_Explain_Surface_RFC_v0_1.md|Promote after no-authoritative-side-effect wording review; central to safe agent execution.|
|OFARM_RuntimeProblem_Reason_Code_Registry_RFC_v0_1.md|GREEN|02_accepted_rfcs/OFARM_RuntimeProblem_Reason_Code_Registry_RFC_v0_1.md|Promote as runtime contract; stable reason codes prevent unsafe app/agent interpretation.|
|OFARM_Publication_and_Output_Assembly_Surface_RFC_v0_1.md|GREEN_WITH_REVIEW|02_accepted_rfcs/OFARM_Publication_and_Output_Assembly_Surface_RFC_v0_1.md|Promote if PassportView/DocumentAssembly distinction is preserved and previews are non-authoritative.|
|OFARM_Offline_Capture_and_Delayed_Sync_RFC_v0_1.md|AMBER|02_accepted_rfcs/OFARM_Offline_Capture_and_Delayed_Sync_RFC_v0_1.md|Promote only after authority recheck, revocation crossing, idempotency, and candidate-only paths are tightened.|
|OFARM_Identity_Resolution_and_Import_Deduplication_RFC_v0_1.md|AMBER|02_accepted_rfcs/OFARM_Identity_Resolution_and_Import_Deduplication_RFC_v0_1.md|Promote only after merge/refusal cases and AgronomicIdentityBinding alignment are checked.|
|OFARM_Calculation_Service_and_Quantity_Conversion_RFC_v0_1.md|HOLD|02_accepted_rfcs/OFARM_Calculation_Service_and_Quantity_Conversion_RFC_v0_1.md|Hold; formula, rounding, and quantity calculations can become hidden agronomic law without stronger review and numeric fixtures.|

## 6. Machine-contract candidates

|Artifact|Recommendation|Target|Rationale|
|---|---|---|---|
|OFARM_AgentReadinessConformanceCase_schema_v0_1.json|SUPPORT_ONLY|03_machine_contracts/OFARM_AgentReadinessConformanceCase_schema_v0_1.json|Keep under conformance until runtime execution exists.|
|OFARM_AgentReadinessConformanceExecutionReport_schema_v0_1.json|SUPPORT_ONLY|03_machine_contracts/OFARM_AgentReadinessConformanceExecutionReport_schema_v0_1.json|Keep under conformance until runtime execution exists.|
|OFARM_AgentReadinessConformanceSuite_schema_v0_1.json|SUPPORT_ONLY|03_machine_contracts/OFARM_AgentReadinessConformanceSuite_schema_v0_1.json|Keep under conformance until runtime execution exists.|
|OFARM_AgentToolManifest_schema_v0_1.json|AMBER|03_machine_contracts/OFARM_AgentToolManifest_schema_v0_1.json|Hold for Phase 5 so it can harmonize with AgentRunEnvelope and Capability Manifest agentSupport.|
|OFARM_AppDemoScenario_schema_v0_1.json|SUPPORT_ONLY|03_machine_contracts/OFARM_AppDemoScenario_schema_v0_1.json|Example/demo scenario support only.|
|OFARM_ApplicationWorkflowCookbookCase_schema_v0_1.json|AMBER_SUPPORT_ONLY|03_machine_contracts/OFARM_ApplicationWorkflowCookbookCase_schema_v0_1.json|Keep supporting until recipes stabilize.|
|OFARM_ApplicationWorkflowStateMatrix_schema_v0_1.json|AMBER|03_machine_contracts/OFARM_ApplicationWorkflowStateMatrix_schema_v0_1.json|Potentially promotable after workflow-state examples and app labels are tested.|
|OFARM_BaselineHarmonizationProposal_schema_v0_1.json|SUPPORT_ONLY|03_machine_contracts/OFARM_BaselineHarmonizationProposal_schema_v0_1.json|Harmonization-process support only.|
|OFARM_BaselineHarmonizationRegister_schema_v0_1.json|SUPPORT_ONLY|03_machine_contracts/OFARM_BaselineHarmonizationRegister_schema_v0_1.json|Harmonization-process support only.|
|OFARM_CalculationResult_schema_v0_1.json|HOLD|03_machine_contracts/OFARM_CalculationResult_schema_v0_1.json|Hold with calculation RFC.|
|OFARM_CalculationSpec_schema_v0_1.json|HOLD|03_machine_contracts/OFARM_CalculationSpec_schema_v0_1.json|Hold with calculation RFC.|
|OFARM_DoNotPromoteRegister_schema_v0_1.json|SUPPORT_ONLY|03_machine_contracts/OFARM_DoNotPromoteRegister_schema_v0_1.json|Control-plane support only.|
|OFARM_FormulaCatalog_schema_v0_1.json|HOLD|03_machine_contracts/OFARM_FormulaCatalog_schema_v0_1.json|Hold; formula catalog can become hidden agronomic law.|
|OFARM_HarmonizationDecisionLog_schema_v0_1.json|SUPPORT_ONLY|03_machine_contracts/OFARM_HarmonizationDecisionLog_schema_v0_1.json|Control-plane support only.|
|OFARM_IdentityResolutionRequest_schema_v0_1.json|AMBER|03_machine_contracts/OFARM_IdentityResolutionRequest_schema_v0_1.json|Promote with identity RFC after ambiguity/refusal cases are tightened.|
|OFARM_IdentityResolutionResult_schema_v0_1.json|AMBER|03_machine_contracts/OFARM_IdentityResolutionResult_schema_v0_1.json|Promote with identity RFC after ambiguity/refusal cases are tightened.|
|OFARM_ImportCandidate_schema_v0_1.json|AMBER|03_machine_contracts/OFARM_ImportCandidate_schema_v0_1.json|Promote with source-fidelity/import boundary if candidate-only status is explicit.|
|OFARM_ImportLossMap_schema_v0_1.json|AMBER|03_machine_contracts/OFARM_ImportLossMap_schema_v0_1.json|Promote with source-fidelity policy after mapping-loss examples validate.|
|OFARM_ImportReceipt_schema_v0_1.json|AMBER|03_machine_contracts/OFARM_ImportReceipt_schema_v0_1.json|Promote with import replay/idempotency checks.|
|OFARM_InternalSchemaCatalog_schema_v0_1.json|SUPPORT_ONLY|03_machine_contracts/OFARM_InternalSchemaCatalog_schema_v0_1.json|Internal catalog support; do not expose as active public law.|
|OFARM_MinimumCaptureProfile_schema_v0_1.json|HOLD|03_machine_contracts/OFARM_MinimumCaptureProfile_schema_v0_1.json|Hold; minimum capture must not weaken evidence law.|
|OFARM_ModuleImportBoundaryMatrix_schema_v0_1.json|SUPPORT_ONLY|03_machine_contracts/OFARM_ModuleImportBoundaryMatrix_schema_v0_1.json|Implementation/module-boundary support.|
|OFARM_OfflineCaptureEnvelope_schema_v0_1.json|GREEN_WITH_REVIEW|03_machine_contracts/OFARM_OfflineCaptureEnvelope_schema_v0_1.json|Useful for candidate-only offline capture; sync replay must recheck authority.|
|OFARM_OutputAssemblyPreviewRequest_schema_v0_1.json|GREEN_WITH_REVIEW|03_machine_contracts/OFARM_OutputAssemblyPreviewRequest_schema_v0_1.json|Useful for output preview surface; must remain no frozen output effect.|
|OFARM_OutputAssemblyPreviewResult_schema_v0_1.json|GREEN_WITH_REVIEW|03_machine_contracts/OFARM_OutputAssemblyPreviewResult_schema_v0_1.json|Useful for output preview result qualification.|
|OFARM_PreflightRequest_schema_v0_1.json|GREEN|03_machine_contracts/OFARM_PreflightRequest_schema_v0_1.json|Core no-side-effect preflight input.|
|OFARM_PreflightResult_schema_v0_1.json|GREEN|03_machine_contracts/OFARM_PreflightResult_schema_v0_1.json|Core preflight outcome and blocked/review-required posture.|
|OFARM_PromotionCandidateDossier_schema_v0_1.json|AMBER|03_machine_contracts/OFARM_PromotionCandidateDossier_schema_v0_1.json|Useful but must not bypass BridgeCandidate/review/promotion law.|
|OFARM_PublicApplicationSurfaceManifest_schema_v0_1.json|GREEN_WITH_REVIEW|03_machine_contracts/OFARM_PublicApplicationSurfaceManifest_schema_v0_1.json|Useful public surface catalog; must not expose internal shortcuts.|
|OFARM_PublicContractPackManifest_schema_v0_1.json|AMBER|03_machine_contracts/OFARM_PublicContractPackManifest_schema_v0_1.json|Potentially useful once public contract pack boundaries are reviewed.|
|OFARM_PublicOperationDescriptor_schema_v0_1.json|GREEN|03_machine_contracts/OFARM_PublicOperationDescriptor_schema_v0_1.json|Core public-operation declaration for apps/agents.|
|OFARM_PublicReadModelEnvelope_schema_v0_1.json|GREEN_WITH_REVIEW|03_machine_contracts/OFARM_PublicReadModelEnvelope_schema_v0_1.json|Useful if aligned with current-state materialization and no-hidden-truth rules.|
|OFARM_PublicSchemaCatalog_schema_v0_1.json|AMBER|03_machine_contracts/OFARM_PublicSchemaCatalog_schema_v0_1.json|Useful if public/internal schema boundary is locked.|
|OFARM_ReferencePlatformSkeletonManifest_schema_v0_1.json|SUPPORT_ONLY|03_machine_contracts/OFARM_ReferencePlatformSkeletonManifest_schema_v0_1.json|Implementation skeleton support, not active semantic contract yet.|
|OFARM_ResultQualificationEnvelope_schema_v0_1.json|GREEN|03_machine_contracts/OFARM_ResultQualificationEnvelope_schema_v0_1.json|Required for freshness, evidence, redaction, and use limits.|
|OFARM_RuntimeEvidenceGateRegister_schema_v0_1.json|SUPPORT_ONLY|03_machine_contracts/OFARM_RuntimeEvidenceGateRegister_schema_v0_1.json|Runtime evidence tracking support; not active readiness proof.|
|OFARM_RuntimeProblemReasonCodeRegistry_schema_v0_1.json|GREEN|03_machine_contracts/OFARM_RuntimeProblemReasonCodeRegistry_schema_v0_1.json|Stabilizes machine-readable runtime failure reasons.|
|OFARM_SDKCodegenManifest_schema_v0_1.json|SUPPORT_ONLY|03_machine_contracts/OFARM_SDKCodegenManifest_schema_v0_1.json|Keep supporting until SDK generation dry-run exists.|
|OFARM_SourceFidelityEnvelope_schema_v0_1.json|GREEN_WITH_REVIEW|03_machine_contracts/OFARM_SourceFidelityEnvelope_schema_v0_1.json|Makes import/source loss and fidelity machine-visible.|
|OFARM_SyncReplayResult_schema_v0_1.json|GREEN_WITH_REVIEW|03_machine_contracts/OFARM_SyncReplayResult_schema_v0_1.json|Needed for delayed-sync outcomes and revocation crossing.|
|OFARM_TraceRetrievalResult_schema_v0_1.json|GREEN|03_machine_contracts/OFARM_TraceRetrievalResult_schema_v0_1.json|Required for redaction-aware trace retrieval.|
|OFARM_TwoAgentCompatibilityBuildTest_schema_v0_1.json|SUPPORT_ONLY|03_machine_contracts/OFARM_TwoAgentCompatibilityBuildTest_schema_v0_1.json|Keep supporting until two independent agent builds are actually run.|
|OFARM_UnitConversionTrace_schema_v0_1.json|AMBER_HOLD_WITH_CALCULATION|03_machine_contracts/OFARM_UnitConversionTrace_schema_v0_1.json|Hold with calculation service unless separated as trace-only utility.|

## 7. Recommended controlled promotion batch

If the architect chooses to promote a first batch after review, the safest batch is:

### Companion artifacts

- `OFARM_AI_Agent_Use_and_Autonomy_Policy_v0_1.md`
- `OFARM_Current_State_App_Display_and_Cache_Policy_v0_1.md`
- `OFARM_Query_Result_Display_and_Freshness_Policy_v0_1.md`
- `OFARM_Application_Workflow_State_Matrix_v0_1.md`, after UI-state wording review
- `OFARM_Source_Fidelity_Loss_Map_and_FMIS_Shadow_Import_Boundary_Policy_v0_1.md`, after candidate-only import wording review

### Accepted RFCs

- `OFARM_Application_Builder_Surface_RFC_v0_1.md`
- `OFARM_Preflight_DryRun_and_Explain_Surface_RFC_v0_1.md`
- `OFARM_RuntimeProblem_Reason_Code_Registry_RFC_v0_1.md`
- `OFARM_Publication_and_Output_Assembly_Surface_RFC_v0_1.md`, after output-preview wording review

### Machine contracts

- `OFARM_PublicOperationDescriptor_schema_v0_1.json`
- `OFARM_PreflightRequest_schema_v0_1.json`
- `OFARM_PreflightResult_schema_v0_1.json`
- `OFARM_ResultQualificationEnvelope_schema_v0_1.json`
- `OFARM_RuntimeProblemReasonCodeRegistry_schema_v0_1.json`
- `OFARM_TraceRetrievalResult_schema_v0_1.json`
- `OFARM_PublicReadModelEnvelope_schema_v0_1.json`
- `OFARM_OutputAssemblyPreviewRequest_schema_v0_1.json`
- `OFARM_OutputAssemblyPreviewResult_schema_v0_1.json`
- `OFARM_PublicApplicationSurfaceManifest_schema_v0_1.json`
- `OFARM_SourceFidelityEnvelope_schema_v0_1.json`
- `OFARM_OfflineCaptureEnvelope_schema_v0_1.json`, only if offline RFC is promoted or held as draft dependency
- `OFARM_SyncReplayResult_schema_v0_1.json`, only if offline RFC is promoted or held as draft dependency

## 8. Hold decisions

Hold these until later phases or implementation evidence:

- `OFARM_Calculation_Service_and_Quantity_Conversion_RFC_v0_1.md` and calculation/formula schemas;
- `OFARM_Minimum_Capture_Profile_Boundary_Policy_v0_1.md` and minimum-capture schema;
- SDK/codegen, reference skeleton, OpenAPI/AsyncAPI execution evidence, and two-agent compatibility schemas;
- active `AgentToolManifest` promotion until Phase 5 harmonizes it with `AgentRunEnvelope`, `AgentRunTrace`, and Capability Manifest `agentSupport`.

## 9. Exit gate status

Phase 2 is complete as a **promotion-review phase**.

It is not complete as an **active-promotion phase** because no active folder changes were applied. The next possible move is either:

1. apply a first active promotion batch using the review copies, or
2. continue to Phase 3 agent actorship and authority while keeping Phase 2 as supporting review material.

