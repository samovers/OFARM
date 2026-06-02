# OFARM Agentic AI Implementer Directions v0.1

Date: 2026-05-14  
Status: draft implementer handoff; not model law and not runtime certification.

## Build order recommendation

1. Public operation catalogue
2. RuntimeProblem reason-code registry
3. Preflight/dry-run/explain surface
4. Trace retrieval surface
5. ResultQualificationEnvelope preservation
6. Authority and SharingGrant enforcement surfaces
7. AgentToolManifest
8. AgentRunEnvelope and AgentRunTrace
9. AgentHandoffEnvelope
10. WorldModelRun and Advisory scenario support
11. EvidenceNeed and ObservationRequest
12. Farmer-facing app flows

## Non-negotiable implementation rules

- Agents must not write directly to canonical history stores.
- Agents must not write directly to materialization stores.
- Tool-call success is not OFARM governance success.
- UI labels must not collapse draft, advisory, planned, claimed, accepted, disputed, corrected, superseded, stale, and permission-limited states.
- Cached current state must not support high-consequence outputs without freshness qualification.
- Model memory must not become truth.
- World-model state must not become Compliance Twin state.
- Handoff must not transfer authority.
- Capability Manifests must not advertise unsupported behavior.
- AI-agent readiness must not be claimed until break tests execute.

## Pre-implementation claim limits

Before implementation evidence exists, do not claim:

- production readiness
- legal/regulatory certification
- external standard readiness
- live registry integration
- two-agent compatibility
- autonomous compliance decisioning
- world-model compliance automation
- AI-certified audit readiness

## Required runtime evidence before stronger claims

- successful execution of semantic-law blocker tests
- successful two-agent compatibility build or client generation test
- authority/revocation replay tests
- stale-materialization and freshness tests
- sharing/redaction tests
- offline contractor sync/replay tests
- preflight no-side-effect tests
- trace retrieval completeness tests
- world-model Advisory-only boundary tests
