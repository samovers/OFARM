# OFARM Capability Manifest Agentic Extension RFC v0.2 Candidate

Status: SUPPORTING_DRAFT_NOT_ACCEPTED
Phase: AAI-P5

## Purpose

This candidate RFC extends the OFARM Capability Manifest with agentic self-description fields. It does not grant authority and does not claim runtime readiness.

## Scope

Add candidate sections:

- `agentSupport`
- `worldModelSupport`
- `agentToolManifestRefs`
- `readinessClaimLimits`

## Normative candidate rules

### Rule 1 — Capability declaration is not authority

A manifest section may declare support, but may not authorize a run, approve a tool call, satisfy an evidence requirement, activate a pack, publish an output, or promote an Advisory artifact.

### Rule 2 — Manifest claims are evidence-qualified

Each declared capability must carry a readiness posture:

- `DECLARED_ONLY`
- `STATIC_SCHEMA_VALIDATED`
- `STATIC_EXAMPLE_VALIDATED`
- `IMPLEMENTATION_PRESENT_NOT_TESTED`
- `RUNTIME_EXECUTED`
- `RUNTIME_PASSED`
- `TWO_AGENT_COMPATIBILITY_PASSED`
- `EXTERNAL_CONFORMANCE_REVIEWED`

Pre-implementation packages may not claim runtime-passed status.

### Rule 3 — Agent support depends on Phase 3 and Phase 4 concepts

A manifest may declare robust multi-agent support only if it references supported versions of:

- agent profile/instance/sponsor/authority contracts;
- agent run envelope contracts;
- agent run trace contracts;
- handoff contracts;
- AgentToolManifest contracts.

### Rule 4 — World-model support is advisory-only by default

Manifest-level `worldModelSupport` is declaration only. It must not imply that a world-model state can become Compliance Twin state or current-state materialization.

### Rule 5 — Deployment self-description must match implementation evidence

A deployment manifest must not claim a capability that cannot be demonstrated by supported contracts, examples, or executed conformance evidence appropriate to the readiness level.

## Negative cases

- `agentSupport.supported=true` with no tool manifest reference.
- `worldModelSupport.targetTwin=COMPLIANCE`.
- `readinessClaim=RUNTIME_PASSED` in a pre-implementation package.
- Manifest says `packActivationByAgent=true` without a human-governed path.

## Promotion note

This RFC should be reviewed after Phase 3 and Phase 4 candidates are accepted or explicitly named as draft dependencies.
