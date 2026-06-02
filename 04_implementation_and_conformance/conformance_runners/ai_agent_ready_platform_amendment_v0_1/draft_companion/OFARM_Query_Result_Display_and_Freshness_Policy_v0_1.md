# OFARM Query Result Display and Freshness Policy v0.1

Date: 2026-05-13  
Status: draft companion artifact, implementation/conformance support only  
Phase: AI-agent-ready platform amendment Phase 4  
Affected active authority: `01_companion_artifacts/OFARM_Query_Architecture_Note_v0_1.md`, `02_accepted_rfcs/OFARM_QuerySpecification_Schema_RFC_v0_1.md`, `03_machine_contracts/schemas/query/OFARM_QueryExecutionResult_schema_v0_1.json`, `03_machine_contracts/schemas/query/OFARM_QueryPlanIR_schema_v0_1.json`

## 1. Purpose

This draft policy defines how public OFARM query results should be surfaced to apps and AI coding agents.

It preserves the existing rule that QuerySpecification is a governed query contract and that query outputs must not become hidden truth stores.

## 2. Query result minimum envelope

Every public query execution result returned to an app should be wrapped or accompanied by a `PublicReadModelEnvelope` containing:

- `ResultQualificationEnvelope`
- query request and plan references
- authorization trace reference
- materialization trace/reference where current-state materialization is involved
- reconstruction trace/reference where historical reconstruction is involved
- app-safe display hints
- problems and reason codes
- next actions

## 3. Required result distinctions

Apps must be able to distinguish:

```text
no matching accepted records
records exist but user lacks permission
records exist but are redacted
records exist but are candidate-only
records exist but are disputed
records exist but are stale for requested use
records exist but evidence is insufficient
records exist but identity is unresolved
query refused because high-consequence freshness is not satisfied
```

No query result should collapse these states into `null`, `[]`, or a generic “not found”.

## 4. Query freshness and use class

A query must declare or derive intended use class:

| Use class | Freshness requirement |
|---|---|
| `INFORMATIONAL_DASHBOARD` | may allow stale informational results if qualified |
| `ADVISORY_DISPLAY` | may allow stale exploratory results if Advisory Twin policy allows |
| `FARMER_WORKFLOW_HINT` | may allow warning-qualified results; cannot imply accepted truth |
| `COMPLIANCE_REVIEW` | must disclose basis, limitations, and disputes |
| `COMPLIANCE_OUTPUT_INPUT` | must satisfy fresh/current-state and evidence requirements |
| `HIGH_CONSEQUENCE_DECISION` | must preflight and refuse stale/invalidated/permission-limited basis by default |

## 5. Evidence return behavior

Query results should support explicit evidence return policy:

- `SUMMARY_ONLY`
- `EVIDENCE_REFS_ONLY`
- `EVIDENCE_WITH_REDACTION`
- `FULL_EVIDENCE_WHERE_AUTHORIZED`
- `NO_EVIDENCE_RETURNED`

If evidence is hidden by authority, the result must say that evidence exists but is permission-limited unless even that fact is restricted by data sovereignty or law.

## 6. App-safe labels

Query results must not let apps label:

- operation claims as accepted execution
- recommendation as prescription
- prescription as work completed
- materialization as truth
- PassportView preview as frozen DocumentAssembly
- advisory output as compliance output

The result qualification should include safe labels and forbidden labels.

## 7. Query cookbook requirement

The implementation package should include runnable query cookbook cases for:

1. treatment history by field and week
2. prescribed-versus-applied rate
3. stale materialization blocking high-consequence output
4. permission-limited evidence view
5. candidate-only import result
6. disputed/corrected record reconstruction

Each case should include the QuerySpecification reference, QueryPlanIR reference, expected QueryExecutionResult, expected qualification envelope, display rules, and failure behavior.

## 8. Promotion route

This policy should remain draft support until cookbook cases validate against the active QuerySpecification and QueryExecutionResult contracts.
