# OFARM Agent Run Envelope, Trace, and Handoff RFC v0.1

Date: 2026-05-14  
Status: draft candidate RFC; not accepted baseline law until promoted.  
Role: define governed multi-step agent execution, traceability, output disposition, blocked actions, and inter-agent handoff.


## 1. Problem statement

Multi-step agents can create hidden state unless OFARM defines what an agent run is, what it may read, which tools it may call, what it may write, when it must stop, and how its actions are traced.

## 2. Scope

This RFC defines:

- `AgentRunEnvelope`
- `AgentRunTrace`
- `AgentToolInvocationTrace`
- `AgentOutputDisposition`
- `AgentBlockedActionTrace`
- `AgentHandoffEnvelope`

## 3. AgentRunEnvelope rule

Every state-affecting, high-consequence, external-tool-using, multi-step, or draft-creating agent run must be governed by an `AgentRunEnvelope`.

An envelope must declare:

- agent instance
- sponsor/accountable party
- objective
- target twin
- target scope
- requested and allowed action classes
- authority grant/delegation envelope
- permitted query classes or `QuerySpecification` refs
- allowed tools
- allowed write surfaces
- allowed output classes
- preflight and approval requirements
- input bundle refs
- context snapshot refs
- materialization refs
- pack activation basis
- freshness requirements
- sharing/data-sovereignty limits
- external-call limits
- stop conditions
- trace requirements

## 4. AgentRunTrace rule

Every governed run must produce a trace sufficient to explain:

```text
what was read,
what basis was used,
what tools were called,
what assumptions were made,
what was produced,
what was blocked,
and why OFARM allowed or denied each state-affecting step.
```

OFARM does not require impossible disclosure of proprietary model internals. It requires deterministic governance trace around model activity.

## 5. Output disposition rule

Every run output must resolve to an existing OFARM category or an explicit non-truth status:

- `EPHEMERAL_SCRATCH`
- `QUERY_PROPOSAL`
- `DRAFT_ARTIFACT`
- `CANDIDATE_EVIDENCE`
- `ADVISORY_OUTPUT`
- `HYPOTHESIS`
- `SCENARIO_RESULT`
- `EVIDENCE_NEED`
- `OBSERVATION_REQUEST`
- `BRIDGE_CANDIDATE`
- `REVIEW_REQUEST`
- `OUTPUT_PREVIEW`
- `PERMISSION_LIMITED_ANSWER`
- `BLOCKED_ACTION`

A generic `AgentOutput` truth bucket is forbidden.

## 6. Handoff rule

An `AgentHandoffEnvelope` may transfer task context, artifacts, unresolved conflicts, stale-basis markers, and trace references.

It must not transfer authority. The receiving agent must independently satisfy:

- authority
- scope
- freshness
- sharing
- target twin
- write-surface permissions
- preflight requirements

## 7. Stop conditions

A run must stop or require reauthorization when:

- authority is revoked
- context snapshot expires for intended use
- pack activation basis changes
- materialization becomes stale for high-consequence use
- data-sharing constraint blocks required input
- requested output class exceeds envelope
- tool is unavailable or unapproved
- human approval is required and not present
- unresolved conflict affects requested promotion or publication

## 8. Negative cases

The platform must block:

- hidden chain-of-agent authority
- agent A authorizing agent B by prompt
- stale context handoff without warning
- unresolved conflicts disappearing during handoff
- agent scratch memory becoming current state
- world-model scenario result becoming accepted fact without bridge/review
- tool-call result labelled as accepted OFARM truth

## 9. Machine contracts

Candidate schemas:

- `OFARM_AgentRunEnvelope_schema_v0_1.json`
- `OFARM_AgentRunTrace_schema_v0_1.json`
- `OFARM_AgentToolInvocationTrace_schema_v0_1.json`
- `OFARM_AgentOutputDisposition_schema_v0_1.json`
- `OFARM_AgentBlockedActionTrace_schema_v0_1.json`
- `OFARM_AgentHandoffEnvelope_schema_v0_1.json`

## 10. Conformance implications

Break tests must prove that authority does not move by handoff, revocation during a run blocks final write, and traces preserve enough basis to explain allowed and blocked actions.
