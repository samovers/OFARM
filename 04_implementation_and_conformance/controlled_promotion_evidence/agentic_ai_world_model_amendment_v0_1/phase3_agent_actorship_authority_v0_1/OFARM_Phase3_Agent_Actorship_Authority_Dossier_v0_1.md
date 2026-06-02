# OFARM Phase 3 Agent Actorship and Authority Dossier v0.1

Date: 2026-05-14  
Status: supporting review dossier; not promoted  
Base: Phase 2 working-copy package

## 1. Purpose

Phase 3 prepares OFARM for multi-agent work by making software-agent actorship explicit before any run-envelope or handoff semantics are promoted.

The core question this phase answers is:

> When a software agent acts, who is accountable, which deployed agent instance acted, what model/tool profile was in use, what grant or delegation basis applied, what action class was requested, and why did OFARM allow, deny, require review, or require human approval?

## 2. Active-law fit

This phase fits the active OFARM authority model because:

- authority is action-class based, not role-label based;
- non-human actors are already allowed only where governance permits;
- AI assistance does not borrow human authority silently;
- review, context-governance, signing/attestation, and official filing remain human-governed by default;
- every state-affecting action must still cross the Platform EnforcementChain.

## 3. Deliverables

This phase adds:

- RFC candidate: `OFARM_Agent_Actorship_and_Authority_RFC_v0_2_candidate.md`
- default agent authority matrix
- machine-contract drafts for agent identity/lifecycle/authority
- positive and negative examples
- authorization trace requirements
- conformance fixture plan
- static validation report

## 4. Main controlled patch

The smallest controlled future promotion should be:

1. add an accepted RFC for agent actorship and authority;
2. add machine contracts for agent profile, instance, sponsor, model/tool profile, authority envelope, revocation state, actorship binding, and agent authorization trace;
3. add an agent-default posture matrix tied to existing `AuthorityActionClass` values;
4. keep the full AgentRunEnvelope and AgentHandoffEnvelope work in Phase 4.

## 5. Promotion classification

| Item | Classification | Promotion recommendation |
|---|---|---|
| Agent actorship/lifecycle RFC | accepted RFC candidate | promote after architect review |
| Agent identity/lifecycle schemas | machine-contract candidates | promote after schema review |
| Agent authority default matrix | companion or RFC appendix candidate | promote with RFC |
| Agent authorization decision trace schema | machine-contract candidate | promote with RFC or Phase 4 |
| Run-envelope/handoff fields | out of scope for Phase 3 | defer to Phase 4 |

## 6. Human-governed defaults preserved

The following remain human-governed by default unless explicitly relaxed by later accepted OFARM law:

- review acceptance, rejection/contest, and supersession;
- context pack installation, activation, and deactivation;
- official output approval;
- attestation or signing;
- filing or formal submission;
- high-consequence compliance promotion;
- governance changes to core semantics, authority policy, evidence policy, or promotion law.

## 7. New risk closed by this phase

This phase closes the ambiguity risk where “AI did it” hides the accountable party, deployed instance, authority grant, tool/model basis, or action-class posture.

## 8. Remaining risk after this phase

A full multi-step agent workflow still needs Phase 4:

- `AgentRunEnvelope`
- `AgentRunTrace`
- `AgentToolInvocationTrace`
- `AgentOutputDisposition`
- `AgentHandoffEnvelope`

Phase 3 deliberately does not solve run-level governance alone.

## 9. Exit status

Phase 3 is complete when the draft contracts validate syntactically, examples validate against their schemas, and the dossier clearly states that no runtime conformance has been executed.
