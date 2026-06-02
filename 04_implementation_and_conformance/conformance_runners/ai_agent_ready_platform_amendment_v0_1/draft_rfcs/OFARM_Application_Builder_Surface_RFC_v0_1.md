# OFARM Application Builder Surface RFC v0.1

Date: 2026-05-13  
Status: draft candidate RFC; not accepted baseline law until promoted  
Scope: define public OFARM Platform surfaces for client applications, SDKs, and AI coding agents

## 1. Problem statement

OFARM has strong model/runtime law and machine contracts, but an application builder needs a callable public surface. Without this surface, apps and AI coding agents may:

- invent endpoints
- copy platform internals
- mutate materializations directly
- treat projections as truth
- bypass authority/promotion/evidence gates
- collapse recommendation, prescription, work order, claim, accepted execution, correction, and dispute

## 2. Core stance

An OFARM client application may only affect authoritative outcomes through governed public operations.

A public operation must declare:

```text
operationId
surfaceCategory
request schema
result schema
callers allowed
authority requirement
preflight/dry-run requirement
trace requirement
RuntimeProblem reason codes
cache/display policy
forbidden shortcuts
```

## 3. Public operation families

| Family | Required operation posture |
|---|---|
| Capability discovery | read-only; credential-scoped where possible |
| Authority preflight | read-only decision/explain surface |
| Commit ingress | state-affecting only through governed submission |
| Evidence registration | state-affecting evidence-reference registration; no automatic truth promotion |
| Query planning/execution | read/query only; must expose freshness/evidence/permission posture |
| Materialization read | read-only; must expose basis/freshness and not claim canonical truth |
| Publication assembly | dry-run and create; must expose basis, redaction, frozen/draft status, trace |
| Correction/dispute | state-affecting; never deletes history silently |
| Identity binding | resolve/propose/flag ambiguity; no hidden merge |
| Import candidate | candidate material only unless later promoted through gates |
| Pack activation planning | plan/conflict/explain before activation |
| Trace retrieval | read-only, redaction-aware |
| Calculation | governed formula/unit/rounding service; no hidden UI formulas |

## 4. Candidate public operations

Endpoint names are draft names. Implementations may adjust transport naming, but must preserve operation meaning.

| Operation ID | Candidate endpoint | Consequence class | Preflight required | Trace required |
|---|---|---:|---:|---:|
| `capabilities.get` | `GET /.well-known/ofarm-capabilities` | read-only | no | no |
| `authority.preflight` | `POST /authority/decisions:preflight` | read-only | n/a | yes |
| `commits.dryRun` | `POST /commits:dryRun` | read-only validation | n/a | yes |
| `commits.submit` | `POST /commits` | state-affecting | yes | yes |
| `evidence.register` | `POST /evidence-references` | state-affecting candidate support | policy | yes |
| `queries.plan` | `POST /queries:plan` | read-only | no | yes |
| `queries.execute` | `POST /queries` | read/query | policy | yes |
| `materializations.get` | `GET /materializations/{scope}` | read-only | no | yes |
| `assemblies.dryRun` | `POST /assemblies:dryRun` | read-only validation | n/a | yes |
| `assemblies.create` | `POST /assemblies` | publication-affecting | yes | yes |
| `corrections.submit` | `POST /corrections` | state-affecting | yes | yes |
| `disputes.submit` | `POST /disputes` | state-affecting | yes | yes |
| `identity.resolve` | `POST /identity-bindings:resolve` | read/propose | policy | yes |
| `imports.submitCandidate` | `POST /imports/candidates` | candidate-only | yes | yes |
| `packs.planActivation` | `POST /packs/activation:plan` | read-only validation | n/a | yes |
| `traces.get` | `GET /traces/{traceType}/{traceId}` | read-only | no | no |
| `calculations.evaluate` | `POST /calculations:evaluate` | read/calculation result | policy | yes |

## 5. Forbidden direct client operations

Applications and AI agents must not directly call or mutate:

- canonical assertion/history store
- materialization store
- projection cache
- promotion decision store
- authority decision store
- pack merge internals
- publication frozen-output internals
- internal trace assembly store
- AI memory or prompt cache as a source of truth

## 6. Required operation result posture

Every public operation result must return or link to:

- operation identifier
- request identifier or idempotency key
- decision/status
- RuntimeProblem array when applicable
- trace references when applicable
- evidence posture when applicable
- authority posture when applicable
- freshness posture when applicable
- redaction or permission-limited posture when applicable
- next actions when blocked, review-required, or candidate-only

## 7. Cache/display policy

Applications may cache public results only under the returned cache/freshness posture.

Applications must not cache as canonical truth:

- materialization results
- query results
- publication outputs
- AI-generated summaries
- external import candidates
- local offline drafts

## 8. Capability Manifest relationship

The Capability Manifest should expose which public operations are supported for a deployment/tenant. A credential-scoped capability view should narrow the answer to what the current actor may actually call.

## 9. Conformance obligations

A platform claiming this surface must prove:

- every state-affecting operation crosses authority and promotion gates
- high-consequence operations support preflight/dry-run
- materialization reads expose basis/freshness
- query results expose permission and freshness posture
- publication assembly exposes basis/trace/redaction
- import candidate submission does not auto-promote truth
- RuntimeProblem reason codes are registry-backed
- traces are retrievable subject to authority and redaction

## 10. Promotion note

When accepted, this RFC should create active machine contracts for public operation descriptors, public/internal schema catalogs, and agent tool manifests.

