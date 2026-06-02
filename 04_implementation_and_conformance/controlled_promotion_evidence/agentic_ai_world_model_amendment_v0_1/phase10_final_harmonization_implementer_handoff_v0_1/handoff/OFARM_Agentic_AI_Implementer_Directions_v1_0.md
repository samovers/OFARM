# OFARM Agentic AI Implementer Directions v1.0

## Implementation posture

These directions are implementation guidance. They do not override active OFARM law.

## Build order

1. Public operation catalogue.
2. Preflight/dry-run/explain.
3. RuntimeProblem reason codes and result qualification.
4. Trace retrieval.
5. Authority, SharingGrant, revocation, and permission-limited result enforcement.
6. Agent actorship and authority envelope.
7. AgentRunEnvelope and AgentRunTrace.
8. AgentToolManifest and Capability Manifest `agentSupport`.
9. AgentHandoffEnvelope.
10. Advisory WorldModelRun and ScenarioSpec/ScenarioResultSet support.
11. EvidenceNeed and ObservationRequest.
12. Farmer-facing agents and daily brief surfaces.
13. Phase 9 hostile suite execution.

## Non-negotiable implementation rules

- Do not let agents write directly to canonical stores.
- Do not let agents write directly to materialization stores.
- Do not let tool-call success mean OFARM governance success.
- Do not expose internal schemas as public contracts unless they are declared public.
- Do not collapse draft, advisory, planned, claimed, accepted, disputed, corrected, frozen, and filed states in UI.
- Do not let cached current state support high-consequence outputs without freshness qualification.
- Do not let model memory become truth.
- Do not let world-model state become Compliance Twin state.
- Do not let a handoff transfer authority.
- Do not let a Capability Manifest advertise unsupported behavior.
- Do not claim agentic readiness until hostile gates are executed.

## Suggested but non-normative implementation patterns

Equivalent alternatives are allowed if they satisfy OFARM behavior:

- workload identity / attestation for AgentInstance;
- policy decision point with decision IDs;
- OpenTelemetry-style trace propagation;
- PROV-compatible provenance export;
- OpenAPI/AsyncAPI/Arazzo-style public operation and workflow documentation;
- offline-first capture with signed delayed-sync envelopes;
- world-model quality monitoring with calibration, drift, invalidation, and reconciliation evidence.
