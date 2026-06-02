<!--
Promotion review copy only. This file is included inside the Phase 2 supporting review folder.
It is not active OFARM law unless copied to the active target path by a separate controlled promotion.
Phase 2 classification: GREEN.
-->

# OFARM AI Agent Use and Autonomy Policy v0.1

Date: 2026-05-13  
Status: draft companion artifact; not active companion law until promoted  
Role: AI-agent behavior policy for OFARM Platform and OFARM-based applications

## 1. Purpose

This policy defines how AI coding agents and runtime assistant agents may interact with OFARM Platform public operations.

It preserves active OFARM law by requiring AI agents to use public surfaces, preflight high-consequence actions, and never become hidden governance decision makers.

## 2. Agent classes

| Agent class | Meaning |
|---|---|
| Coding agent | Generates platform, SDK, adapter, test, or application code. |
| Runtime assistant agent | Helps users create drafts, queries, explanations, or decisions inside an OFARM app. |
| Import/adapter agent | Maps external source records into candidate OFARM material. |
| Advisory agent | Produces advisory recommendations, explanations, summaries, or suggestions. |
| Compliance-support agent | Helps assemble compliance evidence or reports, but cannot self-certify truth. |

## 3. Autonomy levels

| Level | Meaning | Allowed example |
|---|---|---|
| `SUGGEST_ONLY` | Agent may produce text or draft proposals only. | advisory recommendation draft |
| `PREFLIGHT_ONLY` | Agent may call dry-run/preflight/explain, but not execute. | publication dry-run |
| `EXECUTE_WITH_APPROVAL` | Agent may execute only after required human/platform approval. | commit submission for high-consequence operation |
| `EXECUTE_WITH_POLICY_AUTHORITY` | Agent may execute if authority policy explicitly allows it for actor/scope/time. | low-risk query or draft creation |
| `FORBIDDEN` | Agent must not call or simulate the operation. | direct materialization-store mutation |

## 4. Required workflow

AI agents must use this pattern for state-affecting or high-consequence operations:

```text
propose
→ preflight/dry-run
→ request human approval if required
→ execute through public operation only
→ retrieve trace
→ display outcome with evidence/freshness/authority posture
```

## 5. Human approval required

Human approval or explicitly delegated non-human authority is required for:

- promotion into accepted compliance-relevant state
- publication of frozen/compliance-grade DocumentAssembly
- pack activation or profile change
- correction/dispute with high-consequence effect
- identity binding acceptance when ambiguous
- source import promotion from candidate to accepted state
- any action that may affect regulated compliance status

## 6. AI outputs are not governance decisions

AI-generated recommendations, summaries, classifications, code mappings, and explanations remain advisory or candidate material until accepted through governed OFARM gates.

Forbidden pattern:

```text
AI recommendation -> accepted OFARM fact
```

Required pattern:

```text
AI recommendation -> candidate/draft -> authority/evidence/review gates -> accepted only if gates pass
```

## 7. Source fidelity rule for import/adapter agents

Import/adapter agents must preserve:

- source record IDs
- source timestamps
- source actor identifiers
- source payload references
- mapping confidence/loss
- unresolved identity markers
- evidence qualification posture

They must not silently infer contractor identity, product identity, geometry version, or compliance status.

## 8. Permission-limited result rule

When data is unavailable due to authority, redaction, tenant boundary, or sovereignty restriction, the agent must say that the result is permission-limited. It must not fabricate missing values or say no records exist unless the platform result actually says no records exist.

## 9. Coding-agent repository rule

Coding agents must follow `AGENT_NAVIGATION.md` and `agent_authority_map.json` before generating code.

They must not copy examples marked:

```text
CONFORMANCE_ONLY
DRAFT_NON_DEFAULT
REVIEW_HOLDING
LEGACY_DO_NOT_COPY
PLATFORM_INTERNAL_CONTRACT
```

into public application semantics.

## 10. Tool manifest requirement

Every AI-agent-callable operation should be listed in an `OFARM_AgentToolManifest` with:

- autonomy level
- preflight operation
- approval requirement
- allowed caller class
- trace types
- refusal reason codes
- safe display states

## 11. Conformance failure conditions

A platform or app fails AI-agent readiness if an agent can:

- execute high-consequence operation without preflight
- mutate internal stores directly
- promote AI output to accepted truth
- hide authority denial
- treat stale materialization as current truth
- fabricate permission-limited data
- publish compliance output without trace/basis

