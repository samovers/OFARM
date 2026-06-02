# OFARM Phase 5 Attached Research Analysis

## Research conclusions applied in Phase 5

The Deep Research report supports a conservative OFARM amendment path. It does not recommend a new AI authority plane, a third twin, or a broad redesign. It recommends narrow baseline safety, machine-readable contracts, and hostile tests.

Phase 5 specifically applies these findings:

1. **Capability and authority must stay separate.**
   The research distinguishes software identity, runtime instance identity, accountable sponsorship, and delegated authority. Phase 5 follows that by making manifest fields descriptive only. Authority remains in Phase 3 `AgentAuthorityEnvelope` and runtime policy decisions.

2. **Tool hints are not trust decisions.**
   The research highlights MCP-style hints such as read-only, destructive, idempotent, and open-world status as useful metadata but unsafe as sole trust-and-safety controls. Phase 5 creates `AgentToolDeclaredHintSet` and marks it as non-authoritative.

3. **Layered manifests are safer than monoliths.**
   Phase 5 separates discovery, schema, side-effect classification, approval, semantic preconditions, external-call policy, redaction, learning policy, and trace requirements.

4. **Readiness claims need limits.**
   Phase 5 adds `AgentCapabilityReadinessClaimLimit`, so a manifest can declare support only with a status such as `DECLARED_ONLY`, `STATIC_VALIDATED`, or `RUNTIME_EXECUTED`. This prevents pre-implementation packages from sounding production-ready.

5. **World-model support declarations remain advisory-only.**
   Phase 5 includes only high-level `worldModelSupport` manifest declaration. It does not promote `WorldModelRun`, `WorldModelState`, or scenario contracts; those remain Phase 6 work.

## Resulting Phase 5 position

Phase 5 is ready for architect review as a supporting candidate package. It is not ready for active machine-contract promotion until Phase 3 and Phase 4 candidate contracts are either promoted or cross-referenced as explicitly draft dependencies.
