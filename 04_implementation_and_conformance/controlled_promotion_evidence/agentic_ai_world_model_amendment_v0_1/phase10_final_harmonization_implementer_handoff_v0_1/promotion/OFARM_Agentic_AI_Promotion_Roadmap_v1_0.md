# OFARM Agentic AI Promotion Roadmap v1.0

## Promotion principle

Promote only the smallest controlled patch that has a clear authority posture, machine shape, negative cases, and conformance path.

## Batch 1 — Public operation and preflight surfaces

Promote from Phase 2 after architect review:

- PublicOperationDescriptor
- PreflightRequest / PreflightResult
- ResultQualificationEnvelope
- RuntimeProblemReasonCodeRegistry
- TraceRetrievalResult
- PublicReadModelEnvelope
- OutputAssemblyPreviewRequest / OutputAssemblyPreviewResult
- SourceFidelityEnvelope

Reason: apps and agents need governed public surfaces before deeper autonomy.

## Batch 2 — Agent actorship and authority

Promote from Phase 3:

- SoftwareAgentProfile
- AgentInstance
- AgentSponsorRef
- AgentModelToolProfile
- AgentAuthorityEnvelope
- AgentRevocationState
- AgentActorshipBinding
- AgentAuthorizationDecisionTrace

Reason: identity, sponsor, and authority must be separate before agent runs are allowed.

## Batch 3 — Agent run governance and handoff

Promote from Phase 4:

- AgentRunEnvelope
- AgentRunTrace
- AgentToolInvocationTrace
- AgentOutputDisposition
- AgentBlockedActionTrace
- AgentHandoffEnvelope

Reason: multi-step agent work needs envelopes, traces, and no-authority-transfer handoff.

## Batch 4 — Manifests

Promote from Phase 5:

- AgentToolManifest
- AgentToolDescriptor
- AgentSupportSection
- AgenticCapabilityManifestOverlay
- readiness claim limits
- untrusted tool hint rule

Reason: deployments need self-description, but manifests must not grant authority.

## Batch 5 — Advisory world model

Promote from Phase 6:

- WorldModelRun
- WorldModelState
- ScenarioSpec
- ScenarioResultSet
- assumption, uncertainty, validity, invalidation, calibration, reconciliation, and blocker contracts

Reason: world models can support scenarios without becoming Compliance state.

## Batch 6 — Missing-information requests

Promote from Phase 7:

- EvidenceNeed
- ObservationRequest
- burden/noise/deduplication/satisfaction contracts

Reason: farmers need bounded, meaningful requests, not AI task spam.

## Keep supporting until runtime exists

Keep Phase 8 and Phase 9 as supporting conformance/implementation material until a runtime executes them.
