# AAI-CP3 agent actorship and sponsor-bound authority v0.1

Generated: 2026-05-16T15:30:00+02:00

Status: ACTIVE BASELINE CLARIFICATION + ACCEPTED RFC + ACTIVE MACHINE-CONTRACT PROMOTION + SUPPORTING IMPLEMENTATION / CONFORMANCE CONTROL MATERIAL.

Authority effect: CP3 adds a bounded active actorship and sponsor-bound authority layer. It amends the active baseline with a narrow sponsor-bound authority gate, adds one accepted RFC under `02_accepted_rfcs/`, and promotes eight active authority-lane machine contracts under `03_machine_contracts/schemas/authority/`.

## What CP3 promotes

Accepted RFC:

- `02_accepted_rfcs/OFARM_Agent_Actorship_and_Authority_RFC_v0_1.md`

Active machine contracts:

- `OFARM_SoftwareAgentProfile_schema_v0_1.json`
- `OFARM_AgentInstance_schema_v0_1.json`
- `OFARM_AgentSponsorRef_schema_v0_1.json`
- `OFARM_AgentModelToolProfile_schema_v0_1.json`
- `OFARM_AgentAuthorityEnvelope_schema_v0_1.json`
- `OFARM_AgentRevocationState_schema_v0_1.json`
- `OFARM_AgentActorshipBinding_schema_v0_1.json`
- `OFARM_AgentAuthorizationDecisionTrace_schema_v0_1.json`

## What CP3 does not promote

CP3 does not promote `AgentRunEnvelope`, `AgentRunTrace`, `AgentToolInvocationTrace`, `AgentBlockedActionTrace`, `AgentHandoffEnvelope`, `AgentToolManifest`, world-model runtime, `EvidenceNeed`, `ObservationRequest`, output assembly preview contracts, autonomous compliance decisioning, runtime AI-agent readiness, two-agent compatibility, production readiness, live-registry integration, legal advice, or external-standard readiness.

## Quality gates applied

- Active baseline files identify sponsor-bound software-agent authority as a release/runtime gate.
- Accepted RFC exists for agent actorship and sponsor-bound authority.
- Every promoted schema has at least one positive example in the tier-04 machine-contract example lane.
- Negative policy examples are present in this folder.
- A CP3 conformance runner validates positive examples against schemas and checks selected negative policy failures.
- Contract currentness, decision, traceability, source-input, manifest, and material-status indexes are updated.
- Repository hygiene validation must pass after regeneration.

## Deep Research use

The attached Deep Research report is included as active supporting research. CP3 follows its recommendation to promote sponsor-bound actorship after targeted revision while keeping run tracing, handoff, manifest honesty, world-model, EvidenceNeed, and ObservationRequest outside this phase.

## Next phase

Proceed to CP4: AgentRunEnvelope, AgentRunTrace, blocked-action trace, and handoff law. CP4 should not begin until CP3 actorship authority is treated as the gate that agent runs must satisfy.

## CP3 quality patch — authority-action posture map

Added `03_machine_contracts/maps/authority/OFARM_Agent_Authority_Action_Class_Posture_Map_v0_1.json` so every software-agent AuthorityActionClass posture is explicitly declared rather than left as prose-only guidance.
