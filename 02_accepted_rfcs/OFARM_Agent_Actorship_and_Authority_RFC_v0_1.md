# OFARM Agent Actorship and Sponsor-Bound Authority RFC v0.1

Date: 2026-05-16  
Status: accepted RFC extension by AAI-CP3; active substance unless overridden by active baseline or a later accepted RFC  
Scope: promote the bounded software-agent actorship and sponsor-bound authority layer

## 1. Problem statement

OFARM already permits AI assistance only through governed surfaces. Without a precise actorship and authority model, a runtime could accidentally treat a model identifier, tool identifier, API key, prompt, product feature, session, public-operation descriptor, or manifest declaration as authority.

That would violate OFARM's assertion/history-first truth model, explicit authority law, human-governed defaults, and CP1/CP2 result-qualification discipline.

## 2. Core decision

AAI-CP3 promotes a bounded software-agent actorship layer. A software agent may participate in OFARM only through a sponsor-bound actorship binding and an evaluated authority envelope.

For a state-affecting or high-consequence software-agent action, the platform must resolve:

```text
sponsor_id / sponsor reference
executing_agent_instance
software_agent_profile
model/tool profile basis
actorship basis
authority snapshot reference
requested AuthorityActionClass
target scope and time
twin context
revocation state
authorization decision trace
result qualification linkage
```

Missing sponsor, missing authority snapshot, stale or revoked authority, or unresolved action posture is not a soft UI warning. It is a governance blocker that must produce `DENY`, `REQUIRE_REVIEW`, `REQUIRE_HUMAN_APPROVAL`, or another policy-declared blocked disposition.

## 3. No silent delegation

A software-agent profile, deployed instance, model, tool, manifest, API key, prompt, session, or public operation does not grant authority.

Delegation to or through a software agent requires explicit authority basis and must remain scoped, revocable, time-bounded, action-class-specific, and target-scope-specific. If delegated rights are absent or ambiguous, the default is that no rights transferred.

## 4. Sponsor accountability

Every software-agent action must be accountable to a human or organizational sponsor/controller. The sponsor is not automatically the same as the user who initiated a prompt, the party who owns a model, the vendor who published a tool, or the tenant that hosts the runtime.

The sponsor reference must identify the accountable party and the scope in which the sponsor accepts responsibility for the agent's action.

## 5. AuthorityActionClass posture

Every AuthorityActionClass used by a software agent must resolve to one of the following postures:

- `AGENT_ALLOWED_WITH_POLICY_CHECK`; 
- `AGENT_ALLOWED_WITH_PREFLIGHT_ONLY`; 
- `AGENT_ALLOWED_WITH_HUMAN_APPROVAL`; 
- `HUMAN_ONLY`; 
- `PROHIBITED_FOR_AGENT`.

Human-governed defaults remain for review acceptance, pack activation, official output approval, attestation/signing, filing/submission, high-consequence Compliance Twin promotion, and grant/revocation/expansion of authority or sharing beyond pre-authorized scope unless a later active authority explicitly relaxes them.

## 6. Required machine contracts

AAI-CP3 promotes the following active machine contracts:

```text
OFARM_SoftwareAgentProfile_schema_v0_1.json
OFARM_AgentInstance_schema_v0_1.json
OFARM_AgentSponsorRef_schema_v0_1.json
OFARM_AgentModelToolProfile_schema_v0_1.json
OFARM_AgentAuthorityEnvelope_schema_v0_1.json
OFARM_AgentRevocationState_schema_v0_1.json
OFARM_AgentActorshipBinding_schema_v0_1.json
OFARM_AgentAuthorizationDecisionTrace_schema_v0_1.json
```

## 7. Runtime conformance obligations

A platform fails CP3 conformance if:

- it allows a state-affecting or high-consequence software-agent action without a sponsor reference;
- it treats model, tool, manifest, API key, prompt, or session identity as authority;
- it allows an action without an authority snapshot reference;
- it allows an action after an active revocation state;
- it hides that human approval was required but not obtained;
- it treats public-operation or tool-call success as governance success;
- it expands or transfers authority through context, memory, or handoff;
- it cannot return an agent authorization decision trace for the action.

## 8. Relation to CP2

CP2 defines the public-surface, preflight, trace-retrieval, source-fidelity, and result-qualification surface. CP3 defines who a software agent is allowed to be for authority purposes. CP3 agents must use the governed CP2 surface where public operations are involved.

## 9. Non-promotion boundary

This RFC does not promote `AgentRunEnvelope`, `AgentRunTrace`, `AgentToolInvocationTrace`, `AgentBlockedActionTrace`, `AgentHandoffEnvelope`, `AgentToolManifest`, world-model runtime, `EvidenceNeed`, `ObservationRequest`, autonomous compliance decisioning, two-agent compatibility, production readiness, live-registry integration, legal advice, or external-standard readiness.
