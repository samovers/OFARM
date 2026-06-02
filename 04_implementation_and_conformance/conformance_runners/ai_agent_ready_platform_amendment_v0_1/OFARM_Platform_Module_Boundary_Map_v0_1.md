# OFARM Platform Module Boundary Map v0.1

Date: 2026-05-13  
Status: active supporting implementation/conformance candidate  
Role: platform implementation boundary map for AI coding-agent readiness

## 1. Purpose

This artifact defines the minimum OFARM Platform modules an implementation should expose internally and externally before an AI coding agent writes platform code.

It does not replace `OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md`. It turns that baseline into an implementation-facing module map.

## 2. Core rule

The platform must not be implemented as generic CRUD over farm records.

Every state-affecting path must cross the relevant governed checkpoints:

```text
ingress normalization
→ authority
→ structural/semantic validation
→ pack/profile applicability
→ evidence sufficiency
→ review/promotion
→ materialization
→ publication/export
```

## 3. Required platform modules

| Module | Purpose | Public surface posture |
|---|---|---|
| Artifact Registry | Stores governed artifacts, schemas, profiles, packs, activation context, and active artifact sets. | mostly internal; discovery may be public through Capability Discovery. |
| Capability Discovery Service | Exposes runtime-supported capabilities, deployment scope, public surfaces, conformance classes, and active artifact references. | public read-only. |
| Authority Service | Evaluates action class, actor, delegation, revocation, sharing, tenant, non-human action, and scope. | public preflight; internal enforcement. |
| Pack Activation Service | Plans, validates, and activates pack/profile sets and detects conflicts. | public planning and trace; activation may be restricted. |
| Commit Ingress Service | Receives candidate assertions, events, imports, operation claims, and correction/dispute requests. | public state-affecting via governed API only. |
| Evidence Service | Registers evidence references, evidence authenticity posture, sufficiency cases, and redaction/sovereignty constraints. | public registration/read through authorization. |
| Promotion / Review Service | Decides draft, accepted, contested, rejected, review-required, superseded, and accepted consequence. | internal decision; public trace/result retrieval. |
| Materialization Service | Produces governed current-state views from accepted/in-force substrate and valid context. | public read only; no client direct writes. |
| Query Service | Accepts QuerySpecification, plans QueryPlanIR, executes safely, returns evidence/freshness/problem posture. | public read/query through governed API. |
| Publication / Assembly Service | Builds PassportView and DocumentAssembly outputs with basis, freshness, redaction, and trace. | public dry-run/create subject to authority. |
| Correction / Dispute Service | Records correction, dispute, hold, counter-evidence, supersession, and successor-output flows. | public state-affecting via governed API only. |
| Identity Binding Service | Resolves local/external IDs, machine IDs, product IDs, actor IDs, geometry revisions, and duplicates. | public resolve/propose; acceptance may require review. |
| Adapter / Import Service | Converts FMIS, machinery, sensor, weather, inventory, and external compliance data into candidate OFARM material with loss maps. | public/import-partner candidate submission; no auto-truth. |
| Calculation Service | Performs governed unit conversion, quantity calculation, rounding, uncertainty, formula application, and refusal on unresolved identity. | public calculation/dry-run; high-consequence use requires basis. |
| Trace / Audit Service | Stores and retrieves authorization, promotion, materialization, query, publication, pack activation, import, and calculation traces. | public read subject to authority/redaction. |

## 4. Module interface template

Each module implementation must define:

```text
moduleName
moduleId
responsibility
publicOperations[]
internalOperations[]
inputSchemaRefs[]
outputSchemaRefs[]
emittedEventFamilies[]
requiredTraceTypes[]
authorityActionClassRefs[]
allowedCallers[]
forbiddenCallers[]
forbiddenShortcuts[]
RuntimeProblem reason codes[]
conformanceTests[]
```

## 5. Public versus internal rule

A module may expose public results without exposing its internal store.

For example:

| Internal component | Public alternative |
|---|---|
| canonical assertion store | commit/query/publication APIs |
| materialization store | materialization read API with freshness/basis posture |
| promotion decision state | promotion trace/result API |
| authority decision state | authorization decision result/trace API |
| pack merge internals | pack activation plan/result/trace API |
| trace assembly internals | trace retrieval API with redaction |

## 6. Minimum service dependencies

```text
Commit Ingress -> Authority, Pack Activation, Evidence, Promotion
Promotion -> Authority, Evidence, Pack Activation, Trace
Materialization -> Promotion, Artifact Registry, Pack Activation, Trace
Query -> Authority, Materialization, Artifact Registry, Trace
Publication -> Authority, Query, Evidence, Materialization, Trace
Adapter/Import -> Identity Binding, Evidence, Commit Ingress, Trace
Calculation -> Artifact Registry, Identity Binding, Trace
```

## 7. Forbidden implementation shortcuts

Do not permit:

- application code to write materializations directly
- AI code to promote advisory output into Compliance Twin truth
- importer code to convert FMIS or machinery records into accepted assertions without promotion
- SDK code to mutate internal stores
- UI code to perform governed unit conversions or agronomic calculations without Calculation Service
- query code to return redacted or permission-limited data as if no data exists
- publication code to assemble compliance-grade output without trace and basis

## 8. Conformance hooks

Each module must support conformance tests for at least:

- authority denial
- human approval required
- evidence insufficient
- stale materialization blocked for high-consequence output
- unresolved identity blocked for promotion
- pack conflict blocked
- idempotency replay reused or conflicted
- permission redaction preserved
- trace retrieval succeeds with appropriate redactions

## 9. Relationship to later phases

This module map prepares, but does not close, later work on:

- SDK code generation
- workflow cookbook
- calculation service formulas
- offline sync service
- FMIS shadow import MVP
- reference platform skeleton
- two-agent compatibility tests

