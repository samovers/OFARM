# OFARM Phase 7 — Attached Research Analysis v0.1

## Summary

The attached research specifically recommends `EvidenceNeed` and `ObservationRequest` as separate objects. It argues that AI-generated evidence requests should be bounded work items, not unstructured nagging, and that participatory/local-knowledge patterns matter for farm usability.

## Phase 7 application

Phase 7 converts that guidance into five OFARM-specific controls:

1. **Semantic/action split** — `EvidenceNeed` names the insufficiency; `ObservationRequest` names the action that may reduce or satisfy it.
2. **Farmer burden control** — every request carries priority, burden estimate, deadline/relevance window, and noise-control metadata.
3. **Completion clarity** — every request states acceptable evidence classes, artifact forms, and completion criteria.
4. **Compliance-blocking discipline** — a request may be compliance-blocking only if tied to explicit pack, evidence, output, authority, or promotion law.
5. **Local knowledge preservation** — farmer narrative can annotate or contest a request, but it does not become compliance fact unless separately governed.

## Held decisions

Phase 7 does not decide UI layout, notification channels, mobile capture methods, exact task-assignment UX, or implementation queue mechanics. Those remain implementer concerns.
