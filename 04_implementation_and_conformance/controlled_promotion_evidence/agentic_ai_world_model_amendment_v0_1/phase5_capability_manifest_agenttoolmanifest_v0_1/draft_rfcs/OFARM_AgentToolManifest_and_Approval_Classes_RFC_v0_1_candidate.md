# OFARM AgentToolManifest and Approval Classes RFC v0.1 Candidate

Status: SUPPORTING_DRAFT_NOT_ACCEPTED
Phase: AAI-P5

## Purpose

Define candidate semantics for an `AgentToolManifest` that tells agents, apps, reviewers, and runtimes what tools are available and how OFARM must govern them.

## Core rule

Tool declaration is not tool approval.

A tool descriptor is an input to OFARM enforcement. It is not a bypass around OFARM enforcement.

## Tool descriptor requirements

Each descriptor must declare:

- tool identity;
- public operation binding;
- target twin;
- action class;
- effect class;
- input and output schemas;
- required authority basis;
- required approval class;
- semantic preconditions;
- declared hints;
- result qualification requirements;
- trace obligations;
- external-call policy;
- farm-data learning policy;
- redaction and permission-limited result policy;
- readiness-claim limit.

## Approval classes

- `NO_APPROVAL_READ_ONLY`
- `PRECHECK_ONLY`
- `HUMAN_APPROVAL_REQUIRED`
- `HUMAN_GOVERNED_ONLY`
- `NOT_AGENT_CALLABLE`

## Effect classes

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

## Declared hints

Declared hints are non-authoritative. They may include read-only, destructive, idempotent, open-world, external-disclosure, draft-only, and agent-safe hints. The runtime must check actual effect class, authority, scope, twin, freshness, sharing, and semantic preconditions.

## Outcome separation

A tool invocation must distinguish:

- transport outcome;
- tool outcome;
- policy outcome;
- OFARM semantic outcome;
- output disposition.

## Required refusal posture

If a tool cannot satisfy authority, preflight, approval, redaction, or semantic preconditions, the expected output is a qualified refusal or `RuntimeProblem` style outcome, not a silent no-op.
