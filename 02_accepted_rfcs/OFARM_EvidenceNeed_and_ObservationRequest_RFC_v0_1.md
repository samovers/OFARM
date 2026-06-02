# OFARM EvidenceNeed and ObservationRequest RFC v0.1

Status: accepted RFC extension by AAI-CP8  
Date: 2026-05-16  
Authority tier: accepted RFC, subordinate to `00_active_baseline/`  
Scope: bounded request-layer contracts for missing-information needs and observation requests

## 1. Purpose

This RFC promotes a bounded active contract layer for EvidenceNeed, ObservationRequest, and supporting request governance artifacts.

The promoted layer lets OFARM represent a missing-information need, a bounded observation request, farmer burden, request priority, relevance windows, completion criteria, lifecycle state, satisfaction traces, deduplication, display envelopes, and request governance blockers.

It does not promote requests into evidence, assertions, obligations, compliance blockers, output approvals, or autonomous compliance decisions.

## 2. Governing rule

An `EvidenceNeed` is a statement that a material information gap exists. An `ObservationRequest` is a governed request to capture, provide, verify, or review information that may help satisfy an EvidenceNeed.

Neither artifact is evidence by itself. Neither is an accepted assertion by itself. Neither creates an obligation by itself. Neither blocks compliance by itself.

A request can point to an external rule, governance gate, pack requirement, output policy, sharing policy, or human decision that makes missing information consequential. That external basis, not the request alone, is the source of blocking force.

## 3. Required semantic boundaries

1. `notEvidence` must be true for request-layer artifacts that could otherwise be mistaken for evidence.
2. `notObligation` must be true for `EvidenceNeed` and `ObservationRequest`.
3. `notBlockerByItself` must be true for `EvidenceNeed` and `ObservationRequest`.
4. If a request is blocking, it must cite a `RequestBlockingBasis` that points to an external rule or gate.
5. Completion or satisfaction of a request does not automatically promote evidence; normal evidence, quality, authority, review, and promotion law still applies.
6. Farmer-facing requests must carry display text explaining why the request exists, what it blocks, what it does not block, how to satisfy it, and whether decline/defer is allowed.
7. Requests must carry burden, relevance-window, priority, deduplication, and noise-control posture sufficient to avoid hidden task spam.
8. Agent-generated requests must reference their source run and result qualification where applicable.
9. Observation requests must state acceptable modalities and minimum sufficient payloads without creating a minimum-capture-profile law.
10. Runtime conformance cannot be claimed merely because request-layer schemas validate.

## 4. Promoted contract families

AAI-CP8 promotes these active machine-contract families under `03_machine_contracts/schemas/request_layer/`:

- `EvidenceNeed`
- `ObservationRequest`
- `EvidenceOption`
- `RequestTargetScope`
- `RequestBurdenEstimate`
- `RequestPriorityClassification`
- `RequestRelevanceWindow`
- `RequestCompletionCriteria`
- `RequestLifecycleState`
- `RequestSatisfactionTrace`
- `RequestNoiseControlEnvelope`
- `RequestBlockingBasis`
- `RequestDeduplicationKey`
- `RequestDisplayEnvelope`
- `RequestGovernanceBlocker`

Minimum capture profiles and formula/default calculation rules are deliberately not promoted by CP8.

## 5. Farmer-burden and display rule

A request is release-eligible for farmer-facing display only if it exposes:

- plain-language reason;
- consequence if missing;
- what the request blocks and does not block;
- priority;
- burden estimate;
- relevance window;
- completion criteria;
- acceptable alternatives;
- deduplication/noise-control posture;
- privacy and safety notes where applicable;
- decline or defer posture;
- result qualification for AI-facing or public surfaces.

Suppression of these qualifications is a CP1/CP2 release-gate failure.

## 6. Conformance requirements

A CP8-conformant implementation or fixture must prove:

- an EvidenceNeed can be represented without becoming evidence;
- an ObservationRequest can be represented without becoming an obligation;
- a blocking request must cite an external blocking basis;
- a satisfied request still requires normal evidence/review/promotion before becoming accepted evidence;
- duplicate or low-value requests can be deduplicated, batched, suppressed, deferred, or qualified;
- farmer-facing display includes the required burden, relevance, and consequence fields.

## 7. Non-claims

CP8 does not claim:

- production runtime readiness;
- farmer UX readiness;
- autonomous compliance decisioning;
- minimum capture profile sufficiency;
- external-standard readiness;
- legal or agronomic advice.

CP8 is a controlled contract promotion and conformance-fixture phase only.
