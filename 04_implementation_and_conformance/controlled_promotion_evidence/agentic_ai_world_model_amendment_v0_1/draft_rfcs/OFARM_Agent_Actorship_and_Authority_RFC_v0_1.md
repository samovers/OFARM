# OFARM Agent Actorship and Authority RFC v0.1

Date: 2026-05-14  
Status: draft candidate RFC; not accepted baseline law until promoted.  
Role: define governed software-agent identity, sponsorship, authority envelopes, and human-only defaults.


## 1. Problem statement

The active baseline allows non-human actors where governance permits, but serious multi-agent farming platforms need finer distinctions than “AI” or “software agent.”

Without explicit actorship, agent activity can obscure who is accountable, which deployed agent instance acted, what tool/model profile was used, which grant applied, and whether the requested action class was allowed.

## 2. Scope

This RFC defines:

- `SoftwareAgentProfile`
- `AgentInstance`
- `AgentSponsorRef`
- `AgentModelToolProfile`
- `AgentAuthorityEnvelope`
- `AgentRevocationState`

## 3. Normative rule

A valid agent action must be expressible as:

```text
Agent instance X,
sponsored by accountable party Y,
using model/tool profile Z where relevant,
acted under grant or delegated envelope G,
for action class A,
within scope S,
against twin T,
producing candidate/draft/advisory/governed artifact R.
```

Agent identity alone confers no authority.

## 4. Agent identity components

| Component | Meaning |
|---|---|
| Accountable party | Human or organization ultimately responsible for the agent’s deployment and authorized actions. |
| SoftwareAgentProfile | Declares agent class, intended uses, limits, and default autonomy posture. |
| AgentInstance | A concrete deployed/runtime instance with lifecycle state. |
| AgentModelToolProfile | Model, toolchain, runtime, or service profile used by the instance. |
| AgentAuthorityEnvelope | Action-class, scope, time, twin, approval, and revocation constraints for an agent action. |
| AgentRevocationState | Current revocation/suspension status for the profile, instance, grant, or tool profile. |

## 5. Human-governed defaults

Unless later explicitly relaxed by accepted OFARM law, the following remain human-governed by default:

- review acceptance
- review rejection/contest
- pack installation, activation, deactivation, or profile change
- official output approval
- attestation or signing
- filing or submission
- high-consequence compliance promotion
- sharing grants beyond pre-authorized scope
- governance changes to semantic substrate, authority policy, evidence policy, or promotion law

## 6. Allowed agent postures

| Posture | Meaning |
|---|---|
| `READ_ONLY` | Agent can read only through governed query/read surfaces. |
| `SUGGEST_ONLY` | Agent may generate advice, text, or proposals. |
| `DRAFT_ONLY` | Agent may create draft/candidate material but cannot promote it. |
| `PREFLIGHT_ONLY` | Agent may call preflight/dry-run/explain only. |
| `EXECUTE_WITH_APPROVAL` | Agent may execute only after human/platform approval. |
| `EXECUTE_WITH_POLICY_AUTHORITY` | Agent may execute if explicit authority policy allows this actor/scope/time/action class. |
| `FORBIDDEN` | Agent must not call or simulate this operation. |

## 7. Required authorization decision inputs

Agent authorization must consider:

- sponsor/accountable party
- agent profile
- agent instance lifecycle state
- model/tool profile status
- authority grant or delegation envelope
- action class
- target twin
- target scope
- valid time
- revocation state
- human-approval requirement
- data-sovereignty/sharing constraints

## 8. Negative cases

An OFARM-conformant platform must reject or require review when:

- agent sponsor is missing
- agent instance is unknown or revoked
- model/tool profile is unapproved for the requested use
- requested action class is human-only
- action scope exceeds grant scope
- authority expired or was revoked during a run
- agent tries to promote its own advisory output
- agent tries to attest, file, or activate packs without explicit human-governed path

## 9. Machine contracts

Candidate schemas:

- `OFARM_SoftwareAgentProfile_schema_v0_1.json`
- `OFARM_AgentInstance_schema_v0_1.json`
- `OFARM_AgentSponsorRef_schema_v0_1.json`
- `OFARM_AgentModelToolProfile_schema_v0_1.json`
- `OFARM_AgentAuthorityEnvelope_schema_v0_1.json`
- `OFARM_AgentRevocationState_schema_v0_1.json`

## 10. Conformance implications

Conformance tests must prove that software agents cannot become invisible human substitutes, cannot bypass human-only defaults, and cannot exercise stale or revoked authority.
