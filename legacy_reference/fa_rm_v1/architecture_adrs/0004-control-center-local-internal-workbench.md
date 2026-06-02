# ADR 0004: Control Center remains a local internal workbench

## Status

Accepted

## Context

The repository now proves more Control Center behavior than a diagnostics-only launcher:

- local review queue, detail, and review-action proxy routes exist in `apps/control-center/server.py`
- report-binding backfill is exposed through the same local hub
- tests cover the proxy behavior in `apps/control-center/tests/test_operation_review_workbench.py`
- the backend remains authoritative for committed operations, assessments, and report-binding state under `specs/api/v1/server/fastapi/app/main.py`

That progress creates a boundary risk in both directions:

- docs can understate the local workbench and route people away from implemented review tooling
- docs can overstate the surface as a standalone hosted approval product even though repo evidence does not yet prove that boundary

## Decision

Treat `apps/control-center/` as a local internal operator/admin workbench.

This means:

- Control Center may proxy review queue, review item, review action, and report-binding backfill routes.
- The backend runtime remains the source of truth for committed operations, additive assessments, and report-binding state.
- Control Center must not be described as a separate hosted approval system unless runtime, auth, ownership, and rollout evidence are added and documented.
- Ownership, escalation policy, and final compliance sign-off remain operational decisions outside the current Control Center scope.

## Consequences

Positive:

- operator-facing docs can describe the implemented workbench without pretending the product boundary is broader than it is
- future cleanup can treat Control Center as a local orchestration and review layer instead of inventing a second approval authority
- onboarding guidance can route local review workflows through one explicit boundary decision

Costs:

- hosted-workflow language must stay out of README, onboarding, and implementation notes until the repo proves it
- future productization work will need a new ADR or an update to this one once auth, ownership, and rollout semantics become concrete
