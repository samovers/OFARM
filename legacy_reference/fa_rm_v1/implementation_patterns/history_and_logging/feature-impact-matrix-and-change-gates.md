# Feature Impact Matrix and Change Gates

- Date: 2026-03-04
- Scope: mandatory cross-system impact review for every feature/change

## Why this exists

`farm_rm`, Hub/Dashboard, iOS client, and farming game/sim behavior are coupled through shared semantics, contracts, and operational tooling. A change in one area can silently break another if impacts are not reviewed explicitly.

This document defines the mandatory review matrix and minimum evidence required before merge.

## System map

1. **farm_rm semantics + persistence**
   - Archetypes/templates/value sets, SQL schema, persistence invariants, report-pack bindings.
2. **Backend API contract**
   - Endpoint behavior, OpenAPI, error contracts, `/v1/capabilities` feature gates.
3. **Hub / Dashboard (Control Center)**
   - Operational status, runbooks, service orchestration, payload diagnostics.
4. **iOS client (Farman Lite)**
   - Models, networking, feature flags, compatibility handling, rendering flow.
5. **Farming game/sim (Farman Sim)**
   - Simulation event shapes, mock/feed contract assumptions, operational launch paths.
6. **Release automation**
   - Backend release publication, iOS sync dispatch, compatibility PR/issue flows.

## Mandatory Feature Impact Matrix

Every PR must include a filled matrix in the PR body for all areas below:

1. `farm_rm semantics + persistence`
2. `Backend API contract`
3. `Hub / Dashboard (Control Center)`
4. `iOS client (Farman Lite)`
5. `Farming game/sim (Farman Sim)`
6. `Release automation`

For each area, author must provide:

- Impact: `yes` or `no`
- Summary: concrete change or reason for no impact
- Evidence: tests, files, or runbooks updated

`No impact` is valid only with a concrete justification.

## Required change gates

1. **Template-first rule**
   - New business fields/transaction attributes must map to valid farm_rm template attributes, or a backend request must be opened.
2. **Contract-safe API rule**
   - If API behavior changes, update OpenAPI and stable error contracts.
3. **Capability gate rule**
   - Any runtime-sensitive behavior change must be reflected in `/v1/capabilities` and client gating strategy.
4. **Operational visibility rule**
   - If service behavior changes, update Control Center diagnostics/runbooks where needed.
5. **Client impact rule**
   - iOS compatibility assumptions must be explicitly reviewed and documented.
6. **Sim impact rule**
   - Farming game/sim assumptions and payload/event mapping must be reviewed even when unchanged.
7. **Release chain rule**
   - Confirm backend release -> iOS sync automation is still correct for the changed contract line.

## Minimum evidence before merge

1. Relevant test suite(s) pass.
2. Impacted docs/runbooks are updated.
3. PR body includes completed Feature Impact Matrix.
4. If backend+iOS contract coupling changed, include compatibility plan and rollback note.

## Guard bypass policy

The PR check `feature-impact-matrix-guard` supports bypass only via label `skip-impact-matrix`.

- This label is restricted to maintainers.
- Workflow enforcement accepts bypass only when the latest actor who set the label is authorized.
- Authorized set = repository owner plus users listed in repo variable `IMPACT_MATRIX_SKIP_USERS` (comma-separated GitHub logins).

## Review ownership

- Author: fills matrix and provides evidence.
- Reviewer: verifies matrix correctness against actual diff.
- Maintainer: blocks merge when matrix is missing or materially incorrect.
