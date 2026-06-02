# AAI-CP0 disposition memo v0.1

Generated: 2026-05-16T12:00:00+02:00

## Decision

Start the controlled promotion track with source-authority normalization only. Do not promote AAI-P2 through AAI-P10. Do not treat any `reviewed_*` folder as active authority.

## Findings applied

1. Reviewer evidence is asymmetric: only the regulatory-inspector output is available as a current schema-shaped role-review JSON.
2. Several reviewer-looking folders are source context or review holding, not role-review outputs.
3. The regulatory-inspector output is valid but stale relative to current closure registers.
4. AAI-P2 through AAI-P10 remain supporting-only and not runtime-proven.
5. Phase 9 remains `NOT_RUN_NO_IMPLEMENTATION` and cannot support runtime or two-agent readiness claims.

## CP0 resulting controls

- Require schema-shaped reviewer output or explicit source-context marking.
- Route each recommendation to a primary authority destination class.
- Use stale reviewer outputs only through disposition notes.
- Keep closed regulatory issues closed unless a current contradiction is shown.
- Carry unresolved warnings as hostile-test or external-evidence assumptions instead of reopening baseline law.

## Next phase

Proceed to CP1: draft a narrow active-baseline release-qualification gate for AI-facing and high-consequence surfaces.
