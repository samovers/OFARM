# OFARM Phase 5 Dossier — Capability Manifest and AgentToolManifest

## Status

- Phase: AAI-P5
- Date: 2026-05-14
- Status: SUPPORTING_REVIEW_ONLY_NOT_PROMOTED
- Active folders changed: false
- Runtime conformance: NOT_RUN_NO_IMPLEMENTATION
- Two-agent compatibility: NOT_RUN_NO_IMPLEMENTATION

## Source posture

This phase continues the agentic amendment sequence after:

1. baseline safety clarifications,
2. promotion review of existing app/agent support material,
3. agent actorship and authority candidate work,
4. agent run envelope, trace, and handoff candidate work.

The attached research report strengthens Phase 5 in three places:

- manifests are layered discovery and declaration surfaces, not authority surfaces;
- tool hints such as read-only, destructive, idempotent, and open-world status are untrusted unless verified by OFARM policy;
- readiness claims must distinguish declared support from implemented support and from executed conformance.

## Design result

Phase 5 proposes a candidate manifest stack:

```text
Capability Manifest
  agentSupport
  worldModelSupport
  agentToolManifestRefs

AgentToolManifest
  toolDescriptors[]
    discovery
    input/output schemas
    effect classification
    declared hints
    semantic preconditions
    required authority
    approval requirements
    trace requirements
    external-call policy
    redaction and permission-limited result policy
    farm-data learning policy
    readiness-claim limits
```

## Controlled boundary

The candidate RFC says:

> Capability declaration is not authority. Tool declaration is not approval. A successful tool call is not OFARM semantic success.

## Why this phase matters

Without Phase 5, an implementer can define agents and traces, but cannot safely expose a self-description surface that tells other agents, apps, or reviewers what can be called, what requires approval, and which claims remain unproven.

## No active promotion

This phase intentionally leaves all Phase 5 materials under `04_implementation_and_conformance/controlled_promotion_evidence/agentic_ai_world_model_amendment_v0_1/phase5_capability_manifest_agenttoolmanifest_v0_1/`.

Promotion would require a separate architect review and should be done as a controlled RFC/machine-contract promotion, not by copying this folder wholesale.
