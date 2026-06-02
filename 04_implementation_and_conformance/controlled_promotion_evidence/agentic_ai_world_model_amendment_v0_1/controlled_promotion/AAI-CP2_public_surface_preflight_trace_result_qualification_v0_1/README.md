# AAI-CP2 public surface, preflight, trace, and result-qualification contracts v0.1

Generated: 2026-05-16T14:00:00+02:00

Status: ACCEPTED RFC + ACTIVE MACHINE-CONTRACT PROMOTION + SUPPORTING IMPLEMENTATION / CONFORMANCE CONTROL MATERIAL.

Authority effect: CP2 adds accepted RFC extensions under `02_accepted_rfcs/` and active machine contracts under `03_machine_contracts/schemas/runtime_surface/`. It does not edit active baseline files. It implements the CP1 baseline release-qualification gate by giving it concrete public-surface, preflight, trace, source-fidelity, and result-qualification contract shapes.

## What CP2 promotes

Accepted RFCs:

- `02_accepted_rfcs/OFARM_Application_Builder_Surface_RFC_v0_1.md`
- `02_accepted_rfcs/OFARM_Preflight_DryRun_and_Explain_Surface_RFC_v0_1.md`
- `02_accepted_rfcs/OFARM_RuntimeProblem_Reason_Code_Registry_RFC_v0_1.md`
- `02_accepted_rfcs/OFARM_AI_Facing_Result_Qualification_and_Trace_Surface_RFC_v0_1.md`

Active machine contracts:

- `OFARM_PublicOperationDescriptor_schema_v0_1.json`
- `OFARM_PreflightRequest_schema_v0_1.json`
- `OFARM_PreflightResult_schema_v0_1.json`
- `OFARM_RuntimeProblemReasonCodeRegistry_schema_v0_1.json`
- `OFARM_ResultQualificationEnvelope_schema_v0_1.json`
- `OFARM_TraceRetrievalResult_schema_v0_1.json`
- `OFARM_PublicReadModelEnvelope_schema_v0_1.json`
- `OFARM_SourceFidelityEnvelope_schema_v0_1.json`

## What CP2 does not promote

CP2 does not promote agent actorship, `AgentRunEnvelope`, `AgentRunTrace`, `AgentHandoffEnvelope`, `AgentToolManifest`, world-model runtime, `EvidenceNeed`, `ObservationRequest`, output assembly preview contracts, production readiness, autonomous compliance decisioning, two-agent compatibility, or external-standard readiness.

## Quality gates applied

- Active RFCs exist for the promoted surface.
- Every promoted schema has at least one positive example in the tier-04 machine-contract example lane.
- Negative policy/schema examples are present in this folder.
- A CP2 conformance runner validates positive examples against schemas and checks selected negative policy failures.
- Contract currentness and traceability indexes are updated.
- Repository hygiene validation must pass after manifest/material-status regeneration.

## Next phase

Proceed to CP3: software-agent actorship and sponsor-bound authority. CP3 should not begin until this CP2 surface is treated as the public operation layer agents must use.
