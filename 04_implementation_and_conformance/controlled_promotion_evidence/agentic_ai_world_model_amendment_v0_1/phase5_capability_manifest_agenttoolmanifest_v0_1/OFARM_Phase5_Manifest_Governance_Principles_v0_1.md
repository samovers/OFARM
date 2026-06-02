# OFARM Phase 5 Manifest Governance Principles

## Principle 1 — Manifest describes, authority decides

A Capability Manifest or AgentToolManifest may describe what a deployment or tool claims to support. It may not grant authority, approve an action, satisfy evidence sufficiency, promote an assertion, waive pack law, or override a SharingGrant.

## Principle 2 — Declaration is not conformance

A deployment may declare support for an agent feature only with a readiness status. `DECLARED_ONLY` and `STATIC_VALIDATED` are not runtime conformance.

## Principle 3 — Tool metadata is untrusted until checked

Declared tool hints are input to policy evaluation, not policy evaluation itself. A tool that declares `readOnlyHint=true` can still be blocked if the operation, target twin, side-effect class, scope, or external-call policy is unsafe or unauthorized.

## Principle 4 — Effect class is mandatory

Every agent-facing tool must declare an effect class:

- `READ_ONLY`
- `QUALIFIED_READ`
- `DRAFT_CREATE`
- `EVIDENCE_CANDIDATE_CREATE`
- `ADVISORY_CREATE`
- `BRIDGE_CANDIDATE_CREATE`
- `REVIEW_REQUEST_CREATE`
- `OUTPUT_PREVIEW_CREATE`
- `EXTERNAL_DISCLOSURE_PREPARE`
- `STATE_AFFECTING_GOVERNED_OPERATION`
- `PROHIBITED_FOR_AGENT_USE`

## Principle 5 — Approval class is mandatory

Every agent-facing tool must declare an approval class:

- `NO_APPROVAL_READ_ONLY`
- `PRECHECK_ONLY`
- `HUMAN_APPROVAL_REQUIRED`
- `HUMAN_GOVERNED_ONLY`
- `NOT_AGENT_CALLABLE`

## Principle 6 — Semantic preconditions are not optional

Tools must declare the semantic preconditions that the platform must satisfy before execution: authority, twin, scope, evidence, freshness, pack/profile applicability, sharing, redaction, output disposition, and traceability.

## Principle 7 — Output disposition is explicit

Every tool must declare the output dispositions it may create. It must not create a generic `AgentOutput` artifact family.

## Principle 8 — World-model support is advisory by default

A manifest may declare world-model support only as Advisory Twin support unless a later active RFC explicitly defines a governed bridge path.
