# OFARM Agentic AI / World-Model Amendment — Phase 7

Date: 2026-05-15
Status: SUPPORTING_REVIEW_ONLY_NOT_PROMOTED
Active folders changed: false
Runtime conformance: NOT_RUN_NO_IMPLEMENTATION
Two-agent compatibility: NOT_RUN_NO_IMPLEMENTATION

## Purpose

Phase 7 defines candidate `EvidenceNeed` and `ObservationRequest` semantics for agentic and world-model OFARM. It turns missing-information signals into bounded, farmer-usable request objects without creating hidden obligations, accepted facts, or automatic compliance blockers.

## Governing posture

- `EvidenceNeed` states what evidence is missing and why it matters.
- `ObservationRequest` asks for a real-world observation that may reduce uncertainty, satisfy an evidence need, or unblock review.
- A request is not evidence by itself.
- A request is not an accepted assertion.
- A request is not a promotion decision.
- Compliance-blocking posture requires an explicit pack/rule/evidence/promotion/output basis.
- Agent-generated requests must carry source, burden, priority, relevance window, acceptable completion, and noise-control metadata.

## Promotion status

No files in `00_active_baseline/`, `01_companion_artifacts/`, `02_accepted_rfcs/`, or `03_machine_contracts/` are changed by this phase.
