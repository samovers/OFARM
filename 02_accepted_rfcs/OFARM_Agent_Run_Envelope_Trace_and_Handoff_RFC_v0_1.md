# OFARM Agent Run Envelope, Trace, Blocked-Action Trace, and Handoff RFC v0.1

Date: 2026-05-16  
Status: accepted RFC extension by AAI-CP4; active substance unless overridden by active baseline or a later accepted RFC  
Scope: promote the bounded agent-run, trace, blocked-action, output-disposition, input-bundle, approval/freshness/stop-condition, tool-invocation-trace, and handoff contract layer

## 1. Problem statement

CP3 made software-agent actorship sponsor-bound, scoped, revocable, and action-class-specific. That is necessary but not sufficient for multi-step or multi-agent behavior.

Without a governed run envelope and retrievable trace, a platform could let a software agent read stale state, invoke a successful tool, hide a blocked action, pass draft outputs through a handoff, or let a receiving agent treat context as inherited authority.

The failure mode is semantic laundering: a handoff becomes implicit delegation, a tool success becomes governance success, agent memory becomes evidence, or a blocked action disappears because it never executed.

## 2. Core decision

AAI-CP4 promotes a bounded active agent-run and handoff layer. A state-affecting, high-consequence, or multi-step software-agent run must be governed by an `AgentRunEnvelope`, explained by an `AgentRunTrace`, and linked to result qualification and trace retrieval.

The run layer must record, where applicable:

- sponsor, executing agent instance, software-agent profile, actorship binding, and authority envelope references;
- objective, target twin, target scope, allowed and forbidden action classes;
- input bundles, query/current-state basis, freshness requirements, approval checkpoints, and stop conditions;
- tool/public-operation invocation traces;
- output disposition records;
- blocked-action traces;
- handoff envelopes emitted or received;
- revocation checks;
- result qualification references;
- trace retrieval references.

## 3. Tool success is not governance success

An `AgentToolInvocationTrace` must separate tool result from governance outcome. A tool call may succeed while the governance outcome is `FAIL`, `REQUIRE_REVIEW`, `REQUIRE_HUMAN_APPROVAL`, or `BLOCKED_NOT_ATTEMPTED`.

A platform fails CP4 conformance if it treats HTTP success, model confidence, function-call completion, or public-operation success as proof that authority, freshness, evidence, sharing, pack/profile, output-disposition, or promotion gates passed.

## 4. Blocked-action traces are first-class audit material

A blocked software-agent action is not a missing event. It is a required traceable outcome.

If an agent attempts an action that is forbidden, stale, permission-limited, evidence-insufficient, human-only, sharing-blocked, pack-blocked, profile-blocked, or outside its run envelope, the platform must emit an `AgentBlockedActionTrace` or an equivalent traceable record available through the CP2 trace-retrieval surface.

A blocked-action trace does not create an accepted farm fact, activate a pack, grant authority, or approve output. It records why a governed action did not proceed.

## 5. Output disposition

Agent output must resolve to an explicit disposition. Generated-by-agent status remains provenance only and does not create a generic `AgentOutput` truth bucket.

Allowed CP4 output dispositions include draft/candidate/advisory/review/blocked postures. Promotion to accepted Compliance Twin fact, official output, publication, attestation, filing, sharing grant, or pack activation remains governed by existing OFARM promotion, authority, review, and human-governed default rules.

## 6. Handoff rule

A handoff may transfer task context. It may not silently transfer authority, sharing permission, evidence sufficiency, freshness posture, approval status, or promotion rights.

`AgentHandoffEnvelope.authorityTransferred` is false in this CP4 contract layer. The receiving agent must reauthorize and revalidate sponsor, authority, revocation, action-class posture, freshness, evidence, sharing, pack/profile, and result-qualification posture before any state-affecting or high-consequence action.

If delegated rights are absent, ambiguous, stale, or not backed by separate authority/delegation law, the default is that no rights transferred.

## 7. Required machine contracts

AAI-CP4 promotes the following active machine contracts:

```text
OFARM_AgentRunEnvelope_schema_v0_1.json
OFARM_AgentRunTrace_schema_v0_1.json
OFARM_AgentToolInvocationTrace_schema_v0_1.json
OFARM_AgentOutputDisposition_schema_v0_1.json
OFARM_AgentBlockedActionTrace_schema_v0_1.json
OFARM_AgentHandoffEnvelope_schema_v0_1.json
OFARM_AgentRunInputBundle_schema_v0_1.json
OFARM_AgentRunStopCondition_schema_v0_1.json
OFARM_AgentRunApprovalCheckpoint_schema_v0_1.json
OFARM_AgentRunFreshnessRequirement_schema_v0_1.json
```

## 8. Runtime conformance obligations

A platform fails CP4 conformance if:

- it permits a state-affecting or high-consequence agent run without an `AgentRunEnvelope`;
- it cannot retrieve an `AgentRunTrace` for the governed run;
- it hides a blocked action because no side effect occurred;
- it allows a tool success to be presented as governance success;
- it treats agent memory or scratch state as evidence;
- it permits a receiving agent to act on sender authority without independent reauthorization;
- it omits material result qualification for stale, permission-limited, review-required, approval-required, or blocked outcomes;
- it lets an output disposition create accepted farm facts without ordinary OFARM promotion and review gates.

## 9. Relation to CP2 and CP3

CP2 defines public surfaces, preflight/dry-run, trace retrieval, source fidelity, reason codes, and result qualification. CP3 defines sponsor-bound actorship and authority evaluation. CP4 binds those into bounded run execution, run traceability, blocked-action traceability, and handoff discipline.

## 10. Non-promotion boundary

This RFC does not promote `AgentToolManifest`, world-model runtime, `WorldModelRun`, `WorldModelState`, `ScenarioSpec`, `ScenarioResultSet`, `EvidenceNeed`, `ObservationRequest`, output assembly preview, runtime AI-agent readiness, two-agent compatibility, autonomous compliance decisioning, production readiness, live-registry integration, legal advice, or external-standard readiness.
