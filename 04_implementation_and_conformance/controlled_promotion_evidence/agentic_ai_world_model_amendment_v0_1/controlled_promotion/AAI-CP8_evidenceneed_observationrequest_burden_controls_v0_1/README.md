# AAI-CP8 — EvidenceNeed and ObservationRequest with farmer-burden controls

Date: 2026-05-16
Status: BOUNDED_ACTIVE_REQUEST_LAYER_PROMOTION_WITH_EXPERIMENT_FIRST_UX_LIMITS

## Purpose

CP8 promotes a bounded request-layer contract set for `EvidenceNeed`, `ObservationRequest`, and supporting request burden, relevance, display, lifecycle, deduplication, satisfaction, and governance-blocker records.

The promotion makes missing-information requests explicit, traceable, deduplicated, farmer-displayable, burden-aware, and lifecycle-governed. It does **not** let a request become evidence, an accepted assertion, a compliance obligation, or a compliance blocker by itself.

## Deep Research posture

The attached Deep Research report warned that farmer-facing request systems should optimize for relevance, timing, trust, and low burden, not maximal data collection. CP8 therefore promotes request objects only with explicit non-evidence, non-obligation, non-blocker-by-itself fields; visible consequence text; relevance windows; deduplication; burden estimates; and noise-control/display envelopes.

## Active promotions

Accepted RFC:

- `02_accepted_rfcs/OFARM_EvidenceNeed_and_ObservationRequest_RFC_v0_1.md`

Companion policy:

- `01_companion_artifacts/OFARM_Request_Burden_Noise_and_Farmer_Display_Policy_v0_1.md`

Machine contracts:

- `03_machine_contracts/schemas/request_layer/OFARM_EvidenceNeed_schema_v0_1.json`
- `03_machine_contracts/schemas/request_layer/OFARM_ObservationRequest_schema_v0_1.json`
- `03_machine_contracts/schemas/request_layer/OFARM_EvidenceOption_schema_v0_1.json`
- `03_machine_contracts/schemas/request_layer/OFARM_RequestTargetScope_schema_v0_1.json`
- `03_machine_contracts/schemas/request_layer/OFARM_RequestBurdenEstimate_schema_v0_1.json`
- `03_machine_contracts/schemas/request_layer/OFARM_RequestPriorityClassification_schema_v0_1.json`
- `03_machine_contracts/schemas/request_layer/OFARM_RequestRelevanceWindow_schema_v0_1.json`
- `03_machine_contracts/schemas/request_layer/OFARM_RequestCompletionCriteria_schema_v0_1.json`
- `03_machine_contracts/schemas/request_layer/OFARM_RequestLifecycleState_schema_v0_1.json`
- `03_machine_contracts/schemas/request_layer/OFARM_RequestSatisfactionTrace_schema_v0_1.json`
- `03_machine_contracts/schemas/request_layer/OFARM_RequestNoiseControlEnvelope_schema_v0_1.json`
- `03_machine_contracts/schemas/request_layer/OFARM_RequestBlockingBasis_schema_v0_1.json`
- `03_machine_contracts/schemas/request_layer/OFARM_RequestDeduplicationKey_schema_v0_1.json`
- `03_machine_contracts/schemas/request_layer/OFARM_RequestDisplayEnvelope_schema_v0_1.json`
- `03_machine_contracts/schemas/request_layer/OFARM_RequestGovernanceBlocker_schema_v0_1.json`

## Explicit non-claims

CP8 does not promote:

- requests as evidence;
- requests as obligations;
- requests as blockers by themselves;
- minimum capture profile law;
- formula or calculation defaults;
- output assembly preview;
- runtime AI-agent readiness;
- two-agent compatibility;
- autonomous compliance decisioning;
- production readiness;
- live registry/tool integration;
- legal advice;
- external-standard readiness.

## Core invariant

A request may ask for information, explain why it matters, and point to an external rule or gate that would make missing information consequential. The request itself is not the evidence, not the obligation, and not the blocker.
