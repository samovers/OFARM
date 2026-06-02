
# OFARM Application Workflow Negative Examples v0.1

These examples are intended for conformance tests and prompt guardrails for AI coding agents.

## Claim-to-done collapse

Unsafe pattern:

```text
POST /commits with operation claim
→ app sets task.status = "completed"
→ dashboard includes product as applied for compliance output
```

Required behavior:

```text
POST /commits with operation claim
→ app shows Submitted work record
→ evidence and promotion traces determine whether an Accepted execution record appears
```

## Advisory-to-compliance collapse

Unsafe pattern:

```text
AI assistant recommendation
→ app labels it Approved treatment
→ app creates compliance report input
```

Required behavior:

```text
AI assistant recommendation
→ app labels Suggested action
→ authorised actor may create prescription through governed public surface
```

## Projection-to-truth collapse

Unsafe pattern:

```text
GET materialization
→ app writes materialization row back to local truth store
```

Required behavior:

```text
GET materialization
→ app stores only cache/display copy with basis, freshness, and trace
```

## Redaction-to-absence collapse

Unsafe pattern:

```text
Query result hides evidence due to permission
→ app shows No evidence exists
```

Required behavior:

```text
Query result hides evidence due to permission
→ app shows Restricted evidence details and a safe access/trace action
```

## Passport-bucket collapse

Unsafe pattern:

```text
Every report/dossier/submission/output is called a passport
```

Required behavior:

```text
Use PassportView for live/recomputable scope summaries.
Use DocumentAssembly for frozen, purpose-bound compiled outputs.
Use report/dossier/submission subfamilies where appropriate.
```
