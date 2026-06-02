# OFARM Phase 9 Multi-Agent and World-Model Break-Test Dossier v0.1

## Authority posture

This dossier is active supporting implementation/conformance material. It does not amend baseline law, promote accepted RFCs, or install active machine contracts.

## Research basis

The attached research recommends hostile suites for spoofed identities, sponsor revocation, handoff authority transfer, tool-hint escalation, external-data auto-promotion, hidden truth stores, query and sharing bypass, world-model invalidation failure, memory-to-truth leakage, benchmark deanonymisation, blocked-action trace omission, offline late-sync conflict, and BridgeCandidate auto-promotion. Phase 9 converts those recommendations into explicit OFARM test gates.

## Design objective

A platform should not be able to claim agentic or world-model readiness merely because it has agents, manifests, traces, or simulations. It must show that hostile shortcuts are blocked and that the block is traceable.

## Counts

- Hostile break tests: 22
- Expected blocked trace fixtures: 22
- Multi-agent matrix tests: 12
- World-model/request/freshness matrix tests: 6

## Non-promoted concepts exercised

- SoftwareAgentProfile
- AgentInstance
- AgentAuthorityEnvelope
- AgentRunEnvelope
- AgentRunTrace
- AgentHandoffEnvelope
- AgentToolManifest
- AgentSupportSection
- WorldModelRun
- WorldModelState
- ScenarioSpec
- ScenarioResultSet
- EvidenceNeed
- ObservationRequest

## Exit gate

Phase 9 is complete when all fixture JSON validates against the supporting schema and the validation report preserves `NOT_RUN_NO_IMPLEMENTATION`.
