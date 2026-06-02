# OFARM Phase 5 Capability Manifest Agentic Profile Rules

## Candidate `agentSupport` fields

The candidate `agentSupport` section should declare:

- whether agent support is present;
- supported agent classes;
- supported autonomy levels;
- maximum autonomy level by authority action class;
- whether Phase 3 actorship concepts are supported;
- whether Phase 4 run envelopes, traces, and handoff envelopes are supported;
- which AgentToolManifest documents are in force;
- whether preflight is required by action class;
- whether human approval is required by action class;
- which target twins are available for agents;
- which write surfaces are available;
- which output dispositions are available;
- revocation handling;
- external tool policy;
- farm-data learning policy;
- trace-retention policy;
- redaction and permission-limited result policy;
- readiness-claim limits.

## Candidate `worldModelSupport` fields

Phase 5 allows manifest-level declaration of world-model support only. The deeper world-model runtime contracts remain Phase 6. Candidate fields include:

- support status;
- advisory-only flag;
- supported scenario purposes;
- supported invalidation trigger classes;
- uncertainty-statement support;
- calibration-evidence support;
- reconciliation support;
- maximum support posture.

## Manifest non-goals

The manifest does not:

- grant authority;
- create a legal sharing grant;
- decide evidence sufficiency;
- activate or merge packs;
- promote advisory outputs;
- attest, file, or publish;
- prove runtime conformance;
- prove two-agent compatibility.
