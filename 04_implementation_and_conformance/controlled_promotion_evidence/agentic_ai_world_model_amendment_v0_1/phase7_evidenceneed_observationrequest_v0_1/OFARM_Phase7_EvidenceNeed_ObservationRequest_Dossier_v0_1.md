# OFARM Phase 7 — EvidenceNeed and ObservationRequest Dossier v0.1

Date: 2026-05-15  
Status: SUPPORTING_REVIEW_ONLY_NOT_PROMOTED  
Phase: AAI-P7

## 1. Purpose

Phase 7 defines a candidate request layer for missing evidence and requested observations. It is designed for AI agents, world-model runs, preflight/dry-run checks, output assembly previews, pack/evidence sufficiency checks, contractor/offline workflows, and human review.

The phase answers a narrow question:

> When an agent or world model discovers missing information, how does OFARM represent that need without creating vague chores, hidden obligations, or automatic truth?

## 2. Design conclusion

The phase separates two concepts:

- `EvidenceNeed`: a semantic statement that a claim, output, scenario, pack rule, promotion path, or review path is missing evidence.
- `ObservationRequest`: an actionable request to observe, capture, inspect, photograph, measure, sample, or annotate something in the real world.

An `ObservationRequest` may satisfy or reduce an `EvidenceNeed`, but it is not itself evidence until an acceptable artifact is captured, reviewed where necessary, and governed through normal OFARM evidence and promotion law.

## 3. Authority classification

This phase is supporting-only. It creates candidate RFC, companion, schema, example, and conformance material. It does not promote active law.

## 4. Research integration

The attached research recommends that evidence requests be bounded work items rather than unstructured AI nagging. It identifies minimum useful fields for `EvidenceNeed` and `ObservationRequest`, including blocked decision, insufficiency reason, acceptable evidence classes, observation target, location/time window, acceptable artifact forms, deadline, priority, burden estimate, local-knowledge option, and stop conditions.

Phase 7 implements those recommendations as candidate machine contracts and hostile fixtures.

## 5. Core invariants

1. A request is not canonical truth.
2. A request is not an accepted assertion.
3. A request is not evidence by itself.
4. A request is not a governance decision.
5. A request cannot mark itself compliance-blocking without explicit basis.
6. An AI request must be explainable to a farmer in practical terms.
7. A generated request must include priority, burden, consequence, relevance window, and completion criteria.
8. Repeated or duplicate requests must be collapsed, suppressed, or escalated through noise-control rules.

## 6. Main products

- RFC candidate: `OFARM_EvidenceNeed_and_ObservationRequest_RFC_v0_2_candidate.md`
- Companion candidates for request policy, noise control, satisfaction and waiver
- Candidate schemas for EvidenceNeed, ObservationRequest, request options, request display, request satisfaction, and request blockers
- Examples and negative fixtures

## 7. Exit posture

Phase 7 is ready for architect review. It is not runtime-tested and should not be cited as an accepted active OFARM contract until promoted.
