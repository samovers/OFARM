# OFARM AAI-CP2 patch apply guide v0.1

Generated: 2026-05-16T14:30:00+02:00

## Basis package

Apply this patch to `OFARM2_2026-05-16_agentic_ai_controlled_promotion_cp1_v0_1`.

## Scope

AAI-CP2 promotes accepted RFCs and active machine contracts for the public-surface layer required to execute the CP1 release-qualification gate.

Promoted RFCs:

- `02_accepted_rfcs/OFARM_Application_Builder_Surface_RFC_v0_1.md`
- `02_accepted_rfcs/OFARM_Preflight_DryRun_and_Explain_Surface_RFC_v0_1.md`
- `02_accepted_rfcs/OFARM_RuntimeProblem_Reason_Code_Registry_RFC_v0_1.md`
- `02_accepted_rfcs/OFARM_AI_Facing_Result_Qualification_and_Trace_Surface_RFC_v0_1.md`

Promoted active machine contracts:

- `03_machine_contracts/schemas/runtime_surface/OFARM_PublicOperationDescriptor_schema_v0_1.json`
- `03_machine_contracts/schemas/runtime_surface/OFARM_PreflightRequest_schema_v0_1.json`
- `03_machine_contracts/schemas/runtime_surface/OFARM_PreflightResult_schema_v0_1.json`
- `03_machine_contracts/schemas/runtime_surface/OFARM_RuntimeProblemReasonCodeRegistry_schema_v0_1.json`
- `03_machine_contracts/schemas/runtime_surface/OFARM_ResultQualificationEnvelope_schema_v0_1.json`
- `03_machine_contracts/schemas/runtime_surface/OFARM_TraceRetrievalResult_schema_v0_1.json`
- `03_machine_contracts/schemas/runtime_surface/OFARM_PublicReadModelEnvelope_schema_v0_1.json`
- `03_machine_contracts/schemas/runtime_surface/OFARM_SourceFidelityEnvelope_schema_v0_1.json`

## Non-promotion boundary

CP2 does not promote agent actorship, AgentRunEnvelope, AgentRunTrace, AgentHandoffEnvelope, AgentToolManifest, world-model runtime, EvidenceNeed, ObservationRequest, output assembly preview, autonomous compliance decisioning, two-agent compatibility, production readiness, live-registry integration, legal advice, or external-standard readiness.

## Apply method

1. Copy the patch package contents over the CP1 package root, preserving relative paths.
2. Run `python3 package_meta/tools/validate_repo_hygiene.py`.
3. Run `python3 04_implementation_and_conformance/controlled_promotion_evidence/agentic_ai_world_model_amendment_v0_1/controlled_promotion/AAI-CP2_public_surface_preflight_trace_result_qualification_v0_1/conformance/runners/ofarm_aai_cp2_public_surface_contract_runner_v0_1.py`.
4. Confirm both commands pass before making any CP2 conformance claim.

## Expected validation posture

- Repository hygiene: pass.
- CP2 public-surface contract runner: pass.
- Runtime AI-agent readiness: not claimed.
- Two-agent compatibility: not claimed.
- Production readiness: not claimed.
- External-standard readiness: not claimed.
