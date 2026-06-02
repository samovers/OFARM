# OFARM Preflight, Dry-Run, and Explain Surface RFC v0.1

Date: 2026-05-13  
Status: draft candidate RFC; not accepted baseline law until promoted  
Scope: define plan-before-execute and trace/explain behavior for OFARM Platform public operations

## 1. Problem statement

AI coding agents and client applications need a safe way to ask whether an action would be allowed before mutating state or publishing an output.

Without explicit preflight/dry-run behavior, AI agents may:

- execute high-consequence operations directly
- retry destructively
- ignore authority revocation
- use stale materializations
- publish compliance outputs without evidence or basis
- hide why an operation was blocked

## 2. Definitions

| Term | Meaning |
|---|---|
| Preflight | A no-authoritative-side-effect check of authority, evidence, identity, freshness, pack/profile, and policy posture for an intended operation. |
| Dry-run | A no-authoritative-side-effect simulation of an operation result, including validation, likely traces, RuntimeProblems, and next actions. |
| Explain | A governed retrieval of why a decision/result occurred, including gate outcomes and redactions. |
| Trace retrieval | A redaction-aware read of stored trace records for authorization, promotion, query, materialization, publication, import, pack activation, calculation, or preflight. |

## 3. Required preflight posture

Preflight is required for:

- commit submission that may affect accepted state
- publication assembly that may create frozen or compliance-grade output
- correction/dispute submission
- import candidate submission into a promotion path
- pack activation
- identity binding acceptance
- high-consequence calculation use
- any AI-agent action marked `EXECUTE_WITH_APPROVAL` or `EXECUTE_WITH_POLICY_AUTHORITY`

## 4. No-side-effect rule

Preflight/dry-run must not:

- create accepted assertions
- change current-state materializations
- activate packs
- publish frozen outputs
- promote evidence sufficiency
- resolve identity permanently
- consume inventory
- create compliance facts

It may create diagnostic trace records if clearly marked as preflight/dry-run trace.

## 5. Required PreflightResult decisions

A PreflightResult decision must be one of:

```text
ALLOWED
ALLOWED_WITH_WARNINGS
HUMAN_APPROVAL_REQUIRED
REVIEW_REQUIRED
CANDIDATE_ONLY
BLOCKED
```

## 6. Required posture fields

A PreflightResult should include:

```text
authorityPosture
freshnessPosture
evidencePosture
identityPosture
packPosture
calculationPosture
publicationPosture
problems[]
nextActions[]
traceRefs[]
```

## 7. Explain and trace surface

The platform should support trace retrieval for:

```text
AUTHORIZATION
PROMOTION
QUERY
MATERIALIZATION
PUBLICATION
PACK_ACTIVATION
IMPORT
CALCULATION
PREFLIGHT
```

Trace retrieval must preserve data sovereignty and redaction rules.

## 8. Idempotency and retry

State-affecting public operations should require idempotency keys or equivalent replay protection. RuntimeProblem reason codes must distinguish:

```text
IDEMPOTENCY_REPLAY_REUSED
IDEMPOTENCY_REPLAY_CONFLICT
RETRY_CONFLICT
```

## 9. Agent use rule

AI agents must follow:

```text
propose
→ preflight/dry-run
→ request approval when required
→ execute through public operation
→ retrieve trace
→ display outcome with evidence/freshness/authority posture
```

## 10. Conformance tests

A platform implementation must fail conformance if:

- a high-consequence operation can execute without preflight
- preflight changes authoritative state
- blocked operations omit RuntimeProblem reason codes
- trace retrieval is unavailable for accepted/rejected/review-required state changes
- an AI-agent tool can execute a human-only operation

