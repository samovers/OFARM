# OFARM Agent Run Envelope, Trace, and Handoff RFC v0.2 Candidate

Date: 2026-05-14  
Status: candidate accepted RFC; not accepted until promoted  
Depends on: Phase 3 Agent Actorship and Authority

## 1. Problem

Multi-agent OFARM needs run-level governance. Without it, an agent session can obscure objective, scope, target twin, permitted tools, current-state basis, pack basis, freshness posture, tool outputs, blocked actions, and handoff behavior.

## 2. Defined objects

This RFC candidate defines:

- `AgentRunEnvelope`
- `AgentRunTrace`
- `AgentToolInvocationTrace`
- `AgentOutputDisposition`
- `AgentBlockedActionTrace`
- `AgentHandoffEnvelope`
- `AgentRunInputBundle`
- `AgentRunStopCondition`
- `AgentRunApprovalCheckpoint`
- `AgentRunFreshnessRequirement`

## 3. Core rule

A governed agent run must be expressible as:

```text
Agent run R, under actorship binding B, bounded by envelope E, for objective O, within twin W and scope S, using permitted actions/tools A/T, reading governed input basis I, subject to freshness/sharing/approval/stop constraints C, producing trace Z and dispositions D, where handoff transfers context but not authority.
```

A run is not a source of authority. Each state-affecting step must still satisfy OFARM authority, evidence, freshness, query, pack, review, and promotion law.

## 4. AgentRunEnvelope

The envelope declares run purpose, actorship binding, sponsor, objective, target twin, target scope, requested and allowed action classes, authority envelope refs, allowed tools, allowed write surfaces, allowed output dispositions, required preflight, required approval, input bundle refs, context snapshot refs, materialization refs, pack refs, freshness requirements, data-sovereignty limits, external-call policy, farm-data-learning policy, stop conditions, trace requirement, handoff posture, and expiry.

## 5. AgentRunTrace

The trace records what happened: run envelope ref, actorship, agent profile/instance/sponsor/model-tool refs, objective, target scope, query/current-state/context/pack/evidence basis, result qualifications, assumptions, uncertainty, tool invocation traces, output dispositions, blocked-action traces, approval checkpoints, handoffs emitted/received, final outcome, and trace retrieval ref.

OFARM requires deterministic platform enforcement and replayable governance trace, not perfect deterministic replay of neural model internals.

## 6. Tool invocation

A governed tool call records the public operation/tool, requested action class, target twin/scope, input ref/summary, authorization/preflight/approval refs, side-effect class, result state, governance outcome, output dispositions, reason codes, and qualification ref.

Tool-call success is not OFARM governance success.

## 7. Output disposition

Agent output must resolve to an existing OFARM category or explicit no-artifact/blocked disposition. Generated-by-agent is provenance and authority context, not a truth category.

## 8. Blocked action trace

Blocked traces record attempted action, operation, target twin/scope, reason codes, violated envelope/authority/freshness/sharing/pack/evidence constraints, required response, and whether any draft material remains. They prove enforcement; they do not create accepted farm facts.

## 9. Handoff

Handoff transfers bounded task context. It must declare source run/agent, receiving agent if known, purpose, included and excluded context, redactions, permission-limited markers, stale-basis markers, unresolved conflicts, blocked-action refs, required decisions, expiry, trace refs, and permissions explicitly not transferred.

Core rule: context may move; authority does not. The receiving agent must independently reauthorize and preflight where required.

## 10. Freshness and revocation

Runs must preserve current-state/result qualifications. Stale, partial, permission-limited, advisory, or redacted inputs cannot become unqualified claims. If revocation occurs during a run, trace is retained, drafts may remain if policy allows, and final writes must reauthorize.

## 11. Negative cases

OFARM must block, deny, degrade, or require approval when there is no envelope for state-affecting work, actorship is missing, a tool or write surface is outside the envelope, stale materialization is used for high-consequence output, a permission-limited answer is treated as absence, handoff transfers authority, handoff exceeds SharingGrant, unresolved conflicts disappear, a human-governed action is attempted, agent memory is treated as truth, or output is stored in a generic `AgentOutput` truth bucket.

## 12. Promotion note

Promote this after Phase 3 actorship/authority and alongside Phase 2 preflight/dry-run/explain surfaces. Do not use it to claim runtime conformance before implementation evidence exists.
