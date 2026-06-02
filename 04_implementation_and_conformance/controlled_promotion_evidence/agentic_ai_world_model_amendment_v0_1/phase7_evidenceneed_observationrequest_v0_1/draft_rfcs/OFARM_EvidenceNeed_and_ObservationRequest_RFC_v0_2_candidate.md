# OFARM EvidenceNeed and ObservationRequest RFC v0.2 Candidate

Date: 2026-05-15  
Status: draft candidate RFC; supporting review only; not accepted active law until promoted.  
Role: define bounded request objects for missing evidence and requested observations.

## 1. Problem statement

AI agents, world models, preflight checks, output previews, pack/evidence policies, and human reviews may discover missing information. If those signals remain informal, OFARM risks vague chores, hidden obligations, farmer overload, or compliance blockers without basis.

## 2. Scope

This RFC candidate defines:

- `EvidenceNeed`
- `ObservationRequest`
- request target scope
- evidence options
- burden and priority controls
- relevance windows
- completion criteria
- lifecycle states
- satisfaction traces
- noise-control envelopes
- blocking-basis rules
- local-knowledge annotations
- farmer-facing display envelopes

## 3. EvidenceNeed rule

An `EvidenceNeed` states that an OFARM workflow, claim, scenario, planned intervention, output, promotion path, pack rule, authority rule, or review path is missing evidence.

It must specify:

- target twin and target scope;
- blocked claim or decision where applicable;
- requesting basis;
- evidence gap and insufficiency reason;
- acceptable evidence options;
- severity, priority, and decision sensitivity;
- consequence if unresolved;
- deadline or relevance window;
- advisory, operational, evidence-sufficiency-related, or compliance-blocking posture;
- source agent run, world-model run, preflight, pack rule, or human review where applicable;
- completion criteria;
- burden/noise controls;
- lifecycle state.

## 4. ObservationRequest rule

An `ObservationRequest` asks for real-world capture, inspection, measurement, scouting, sampling, photograph, storage check, lot check, or local narrative that may reduce uncertainty or satisfy an evidence need.

It must specify:

- target twin and target scope;
- observation type;
- acceptable collection methods;
- acceptable artifact forms;
- minimum acceptable capture;
- preferred capture;
- reason and consequence if missing;
- severity and priority;
- burden estimate;
- deadline or relevance window;
- local-knowledge annotation option;
- authority required to satisfy it;
- linked EvidenceNeed where applicable;
- completion criteria;
- lifecycle state.

## 5. Request is not truth

Neither object is an accepted assertion, accepted observation, compliance fact, evidence sufficiency case, attestation, output approval, filing, or current-state materialization. Captured artifacts produced in response to a request must pass normal OFARM evidence, authority, review, and promotion paths.

## 6. Compliance-blocking basis rule

A request may be marked `COMPLIANCE_BLOCKING` only if it includes a `RequestBlockingBasis` tied to an active pack rule, evidence sufficiency policy, authority requirement, output/publication gate, promotion path, accepted RFC requirement, or explicit review decision.

If that basis is absent or invalid, the platform must block the request, downgrade it, or route it for review. It must not create a hidden compliance obligation.

## 7. Farmer burden and noise-control rule

Generated requests must include priority, burden estimate, relevance window, completion criteria, and noise-control metadata. A platform must be able to collapse duplicates, suppress low-value requests, expire stale requests, and surface unresolved high-consequence blockers.

## 8. Satisfaction and waiver rule

Satisfaction requires a `RequestSatisfactionTrace`. Compliance-blocking or evidence-sufficiency-related requests may require human review even when an artifact has been captured. Waiver requires review and does not imply that the missing evidence existed.

## 9. Local knowledge rule

A farmer or authorized actor may annotate, contest, or contextualize a request through `FarmerLocalKnowledgeAnnotation`. Such annotation remains advisory/local knowledge unless separately promoted through normal OFARM governance.

## 10. Negative cases

The platform must reject or qualify:

- evidence requests without reason or consequence;
- compliance blockers without explicit basis;
- request spam without deduplication or relevance control;
- observation requests that imply facts before capture;
- requests that use world-model confidence as evidence sufficiency;
- waived requests treated as evidence;
- local narrative treated as compliance fact without promotion.

## 11. Candidate machine contracts

- `OFARM_EvidenceNeed_schema_v0_2.json`
- `OFARM_ObservationRequest_schema_v0_2.json`
- helper request schemas listed in the Phase 7 candidate register.
