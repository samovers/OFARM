# OFARM Agent Actorship and Authority RFC v0.2 Candidate

Date: 2026-05-14  
Status: candidate accepted RFC; **not accepted until promoted**  
Supersedes for review: draft `OFARM_Agent_Actorship_and_Authority_RFC_v0_1` in the Phase 0/1 start package  
Scope: software-agent identity, sponsorship, lifecycle, authority envelopes, revocation state, and agent-specific authorization trace.

---

## 1. Problem statement

The active OFARM authority model already permits non-human actors where governance allows them, and already requires explicit action-class authority. Serious multi-agent farming platforms need a finer representation than a generic “AI actor.”

Without explicit actorship, agent activity can obscure:

- the human or organization accountable for the agent;
- the deployed agent instance that acted;
- the profile and intended-use limits of the agent;
- the model/tool profile used;
- the grant, delegation, sharing, or revocation basis;
- the requested `AuthorityActionClass`;
- whether the output is advisory, draft, review-requesting, or promotable.

This RFC defines the minimum agent actorship layer needed before OFARM can safely promote multi-agent run governance.

---

## 2. Scope

This RFC defines:

- `SoftwareAgentProfile`
- `AgentInstance`
- `AgentSponsorRef`
- `AgentModelToolProfile`
- `AgentAuthorityEnvelope`
- `AgentRevocationState`
- `AgentActorshipBinding`
- `AgentAuthorizationDecisionTrace`

This RFC does **not** define full multi-step run governance, tool invocation traces, or handoff semantics. Those belong to the Phase 4 run-envelope/handoff RFC.

---

## 3. Core normative rule

A valid OFARM software-agent action must be expressible as:

```text
Agent instance X,
sponsored by accountable party Y,
using model/tool profile Z where relevant,
acting under grant/delegation/sharing basis G,
for AuthorityActionClass A,
within target scope S and valid time T,
against target twin W,
producing output disposition D,
with authorization outcome O and trace R.
```

Agent identity alone confers no authority. Tool-call success is not governance success.

---

## 4. Agent identity model

### 4.1 Accountable party

The accountable party is the human or organization responsible for deploying, authorizing, supervising, and revoking the agent. The accountable party may be the farmer, farm organization, contractor, advisor, buyer, certifier, platform operator, or other governed party, depending on scope.

### 4.2 SoftwareAgentProfile

A `SoftwareAgentProfile` declares the general class, intended uses, prohibited uses, default autonomy posture, default allowed and forbidden action classes, trace requirements, and sponsor requirement for a kind of software agent.

### 4.3 AgentInstance

An `AgentInstance` is a concrete deployed/runtime instance of a profile. It has lifecycle state and must not act if suspended, revoked, retired, or outside declared deployment scope.

### 4.4 AgentSponsorRef

An `AgentSponsorRef` links the agent action to the accountable party, sponsor role, authority-basis references, and data-sovereignty responsibilities.

### 4.5 AgentModelToolProfile

An `AgentModelToolProfile` describes the model, service, runtime, toolchain, or external service set used by the agent. It must declare intended use, approval status, permitted output posture, data-retention behavior, and whether external calls or farm-data learning are allowed.

### 4.6 AgentAuthorityEnvelope

An `AgentAuthorityEnvelope` constrains a requested action by action class, target twin, target scope, valid time, grant/delegation/sharing basis, approval requirement, revocation state, and output disposition.

### 4.7 AgentRevocationState

An `AgentRevocationState` records whether a profile, instance, sponsor relation, grant, delegation, model/tool profile, or tool permission is active, suspended, revoked, or expired.

### 4.8 AgentActorshipBinding

An `AgentActorshipBinding` joins the accountable party, agent profile, agent instance, sponsor relation, and model/tool profile into a single explainable actorship basis for an action or run.

### 4.9 AgentAuthorizationDecisionTrace

An `AgentAuthorizationDecisionTrace` explains how OFARM reached `ALLOW`, `DENY`, `REQUIRE_REVIEW`, or `REQUIRE_HUMAN_APPROVAL` for an agent request.

---

## 5. Allowed agent postures

| Posture | Meaning |
|---|---|
| `READ_ONLY` | Agent may read through governed query/read surfaces only. |
| `SUGGEST_ONLY` | Agent may generate advice, text, or proposals without creating governed drafts. |
| `DRAFT_ONLY` | Agent may create draft/candidate material but cannot promote it. |
| `PREFLIGHT_ONLY` | Agent may call preflight/dry-run/explain surfaces only. |
| `REQUEST_REVIEW_ONLY` | Agent may create review requests or route candidate material to review. |
| `EXECUTE_WITH_APPROVAL` | Agent may execute only after explicit human/platform approval for the action. |
| `EXECUTE_WITH_POLICY_AUTHORITY` | Agent may execute only if explicit authority policy allows this actor, scope, time, action class, and target twin. |
| `FORBIDDEN` | Agent must not call or simulate this operation as if authorized. |

---

## 6. Default posture by authority family

### 6.1 Observe/report

Agents may usually operate in `DRAFT_ONLY`, `REQUEST_REVIEW_ONLY`, or `EXECUTE_WITH_POLICY_AUTHORITY` posture for observation/evidence actions when explicitly authorized and traceable.

### 6.2 Assert/submit

Agents may prepare draft or candidate assertions. Compliance assertions and structural assertions require stricter review or human approval by default.

### 6.3 Operate/intervene

Agents may plan interventions or report execution only within explicit delegated scope, valid time, and evidence posture. Reporting execution is still not accepted execution truth.

### 6.4 Review/govern

Review requests may be agent-assisted. Review acceptance, rejection/contest, and supersession remain human-governed by default.

### 6.5 Context-governance

Pack installation, activation, and deactivation remain human-governed by default. Agents may draft proposals or preflight effects only if explicitly allowed.

### 6.6 Output/signing/submission

Output preview may be agent-assisted. Official approval, attestation/signing, and formal filing remain human-governed by default unless later accepted law explicitly relaxes a narrow case.

### 6.7 Sharing/access

Agents may read within SharingGrant and may prepare scoped sharing recommendations. Creating or revoking sharing grants requires human approval by default.

---

## 7. Required authorization inputs

Agent authorization must evaluate at minimum:

- accountable party and sponsor role;
- software-agent profile;
- agent-instance lifecycle state;
- model/tool profile approval state;
- requested `AuthorityActionClass`;
- target twin;
- target scope and scope inheritance mode;
- target time and valid interval;
- authority grant, delegation envelope, and/or sharing grant;
- revocation state of party, grant, delegation, profile, instance, model/tool profile, and tool permission;
- required human approval or review;
- data-sovereignty and sharing constraints;
- allowed output disposition.

---

## 8. Human-governed defaults

Unless later explicitly relaxed by accepted OFARM law, the following remain human-governed by default:

- `REVIEW_ACCEPT`
- `REVIEW_REJECT_OR_CONTEST`
- `REVIEW_SUPERSEDE`
- `CONTEXT_INSTALL_PACK`
- `CONTEXT_ACTIVATE_PACK`
- `CONTEXT_DEACTIVATE_PACK`
- `OUTPUT_APPROVE_DOCUMENT_ASSEMBLY`
- `OUTPUT_ATTEST_DOCUMENT_ASSEMBLY`
- `OUTPUT_FILE_SUBMISSION_ASSEMBLY`

AI assistance may prepare material for these actions, but the final decision path must be human-governed unless explicitly changed by later accepted OFARM law.

---

## 9. Output disposition rule

Agent-produced material must resolve into an existing OFARM artifact, commit class, output class, advisory scenario class, review request, evidence need, observation request, or BridgeCandidate path. “Generated by agent” is provenance and authority context, not a standalone truth category.

Allowed dispositions include:

- `READ_RESULT`
- `ADVISORY_TEXT`
- `HYPOTHESIS`
- `DRAFT_ASSERTION`
- `DRAFT_OBSERVATION`
- `EVIDENCE_ATTACHMENT_CANDIDATE`
- `PLANNED_INTERVENTION_DRAFT`
- `OPERATION_CLAIM_DRAFT`
- `BRIDGE_CANDIDATE`
- `REVIEW_REQUEST`
- `PREFLIGHT_RESULT`
- `OUTPUT_PREVIEW`
- `DENIED_NO_ARTIFACT_CREATED`

---

## 10. Revocation and long-running work

Revocation is prospective but mandatory for authorization decisions. If authority, delegation, sharing, profile, instance, model/tool approval, or tool permission changes during a draft or prepared flow, final execution or promotion must re-evaluate against current authority state.

A previously prepared agent output must not be promoted merely because it was prepared before revocation.

---

## 11. Negative cases

An OFARM-conformant platform must deny, require review, or require human approval when:

- agent sponsor is missing;
- accountable party is ambiguous;
- agent instance is unknown, suspended, revoked, or retired;
- model/tool profile is not approved for the requested use;
- requested action class is human-governed by default;
- requested target twin is outside the envelope;
- action scope exceeds grant scope;
- grant, delegation, sharing, or tool permission expired;
- revocation occurred before final action;
- agent tries to promote its own advisory output;
- agent tries to create an `AgentOutput` truth bucket;
- agent tries to treat prompt approval as authority approval;
- tool-call success is used as a substitute for OFARM authorization;
- permission-limited data is treated as proof of absence;
- model memory is used as canonical truth.

---

## 12. Machine contracts

Candidate schemas:

- `OFARM_SoftwareAgentProfile_schema_v0_2.json`
- `OFARM_AgentInstance_schema_v0_2.json`
- `OFARM_AgentSponsorRef_schema_v0_2.json`
- `OFARM_AgentModelToolProfile_schema_v0_2.json`
- `OFARM_AgentAuthorityEnvelope_schema_v0_2.json`
- `OFARM_AgentRevocationState_schema_v0_2.json`
- `OFARM_AgentActorshipBinding_schema_v0_1.json`
- `OFARM_AgentAuthorizationDecisionTrace_schema_v0_1.json`

---

## 13. Conformance implications

Conformance fixtures should prove at minimum:

- evidence-steward agent can attach draft evidence within delegated scope;
- contractor agent cannot report execution outside delegated scope/time;
- advisory agronomy agent cannot promote advisory recommendation into compliance fact;
- compliance steward agent cannot approve or file a submission without human-governed path;
- sharing agent cannot disclose beyond SharingGrant;
- pack activation attempt by agent is denied or human approval required;
- suspended or revoked agent instance is denied;
- revoked authority during long-running flow blocks final execution;
- model/tool profile not approved for requested use blocks or downgrades output posture.

---

## 14. Promotion note

This RFC should be promoted before Phase 4 run-envelope/handoff law. Phase 4 depends on the actorship basis defined here.
