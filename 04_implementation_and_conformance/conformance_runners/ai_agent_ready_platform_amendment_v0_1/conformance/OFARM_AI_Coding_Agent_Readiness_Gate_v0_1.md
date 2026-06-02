# OFARM AI Coding Agent Readiness Gate v0.1

Date: 2026-05-13  
Status: active supporting implementation/conformance candidate

## 1. Purpose

This gate defines minimum evidence that OFARM Platform is ready for AI coding agents to implement and for AI-generated applications to build against.

## 2. Minimum readiness criteria

A platform implementation is not AI-agent-ready until all of the following pass:

1. Public application surface manifest exists and validates.
2. Public/internal schema catalogues exist and validate.
3. Capability discovery identifies public operations and active artifact context.
4. Every high-consequence operation has preflight or dry-run.
5. RuntimeProblem reason codes are registry-backed.
6. Trace retrieval exists for authorization, promotion, query, materialization, publication, pack activation, import, calculation, and preflight.
7. State-affecting operations require idempotency or equivalent replay control.
8. Materialization reads expose basis and freshness posture.
9. Query results distinguish missing, redacted, permission-limited, stale, disputed, and no-record states.
10. Publication assembly exposes PassportView/DocumentAssembly distinction and basis trace.
11. AI-agent tool manifest marks human-only and approval-required actions.
12. No application or SDK path can write internal materialization or canonical stores directly.
13. Import candidates cannot become accepted facts without governed promotion.
14. Offline or delayed sync is preserved as capture/candidate material until sync-time gates pass.
15. Conformance tests cover the prohibited shortcuts below.

## 3. Prohibited shortcuts to test

Fail readiness if an implementation allows:

```text
AI output -> accepted compliance truth
client cache -> canonical truth
materialization store direct app write
query result -> truth store
FMIS import -> accepted fact without promotion
offline draft -> accepted execution without sync-time gates
operation claim -> accepted consequence without promotion
stale materialization -> high-consequence output
permission redaction -> fabricated value
pack conflict -> silent meaning change
identity ambiguity -> silent merge
unit ambiguity -> hidden UI calculation
```

## 4. Two-agent compatibility test

Give the same amended package to two independent AI coding agents and ask both to build a minimal FMIS client. Compare:

- public API usage
- workflow state labels
- authority handling
- stale-state handling
- RuntimeProblem handling
- trace retrieval
- advisory/compliance separation

Fail if the two clients implement materially different OFARM semantics.

## 5. Hard-path break test

Required scenario:

```text
contractor performs work offline
→ delayed sync
→ authority revoked before sync
→ field geometry changed
→ duplicate retry occurs
→ partial execution discovered
→ evidence incomplete
→ record disputed
→ manual correction submitted
→ high-consequence output requested
```

Expected posture:

- offline capture preserved but not accepted truth
- sync-time authority rechecked
- duplicate retry controlled by idempotency
- promotion denied or review-required
- materialization invalidated or stale-blocking
- correction/dispute visible
- high-consequence output blocked or annexed
- trace reconstructs full sequence



## Phase 6 additional gates

A platform is not AI-coding-agent-ready for practical farm workflows until:

- governed calculations refuse unresolved unit/product/area/formula/rounding inputs for high-consequence use
- formula and rounding decisions are traceable and not hidden in UI code
- identity resolution preserves ambiguous/unresolved state
- duplicate import replay is idempotent
- source-fidelity and loss-map envelopes are present for external imports
- FMIS shadow imports remain candidate-only
- offline capture rechecks authority at sync and does not become accepted truth locally
- minimum capture profiles remain non-default and block high-consequence use when required data is missing

## Phase 8 additional gates

A platform is not AI-coding-agent-ready until the Phase 8 agent-readiness conformance suite passes:

- semantic-law blocker tests
- public/internal contract-discipline tests
- sync/import/conflict tests
- numeric/display/trace tests
- SDK boundary tests
- explainability regression tests
- two-agent FMIS compatibility build test
- offline contractor dispute hard-path break test

Protocol success does not waive semantic-law blockers. Runtime execution evidence must be supplied before claiming Phase 8 runtime conformance.
