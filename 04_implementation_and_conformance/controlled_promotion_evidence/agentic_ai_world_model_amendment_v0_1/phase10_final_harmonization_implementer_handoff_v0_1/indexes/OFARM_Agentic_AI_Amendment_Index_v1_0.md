# OFARM Agentic AI and World Model Amendment Index v1.0

## Package status

- Amendment status: supporting final harmonization.
- Active baseline clarification: Phase AAI-P1 included.
- Candidate RFCs/contracts: supporting-only.
- Runtime evidence: not run.

## Phase index

| Phase | Name | Status | Primary output |
|---|---|---|---|
| AAI-P1 | Baseline safety clarification | Active clarification included | No hidden AI truth/governance, no third twin, no tool-call waiver |
| AAI-P2 | Promotion review | Supporting | Reviewed app/public-surface/preflight candidates |
| AAI-P3 | Agent actorship and authority | Supporting | SoftwareAgentProfile, AgentInstance, AgentAuthorityEnvelope candidates |
| AAI-P4 | Agent run envelope, trace, and handoff | Supporting | AgentRunEnvelope, AgentRunTrace, AgentHandoffEnvelope candidates |
| AAI-P5 | Capability Manifest and AgentToolManifest | Supporting | agentSupport and AgentToolManifest candidates |
| AAI-P6 | World-model advisory runtime | Supporting | WorldModelRun, WorldModelState, ScenarioSpec, ScenarioResultSet candidates |
| AAI-P7 | EvidenceNeed and ObservationRequest | Supporting | Missing-information request layer candidates |
| AAI-P8 | Farmer-value scenario fixtures | Supporting | 11 positive and 11 negative farmer-value fixtures |
| AAI-P9 | Break-test suite | Supporting | 22 hostile break tests and expected blocked traces |
| AAI-P10 | Final harmonization | Supporting | Readiness memo, claim limits, implementer handoff |

## Recommended promotion order

1. Phase 2 public surfaces, preflight/dry-run/explain, result qualification, reason codes, trace retrieval.
2. Phase 3 agent actorship and authority.
3. Phase 4 agent run envelope, trace, and handoff.
4. Phase 5 agentic Capability Manifest and AgentToolManifest.
5. Phase 6 advisory-only world-model runtime.
6. Phase 7 EvidenceNeed and ObservationRequest.
7. Keep Phase 8 and Phase 9 as conformance and implementation material until a runtime exists.

## Do-not-promote defaults

Do not promote a generic `AgentOutput` truth bucket, third AI/world-model twin, agent memory as truth, world-model state as Compliance current state, handoff-carried authority, tool hints as authority, self-review, or autonomous pack activation.
