# OFARM wave 22 graph-pattern equivalence hardening memo v0.1

Scope:
- bounded `04_implementation_and_conformance/` hardening wave
- no baseline-law, RFC, companion-policy, or machine-contract substance changes

Why this wave:
- the conformance matrix still had `graph-pattern equivalence tests` at `NOT_STARTED`
- the current package already had:
  - alias-governance starter coverage
  - limited query-plan semantic-equivalence across execution targets
- the missing central seam was same-semantics equivalence at the normalized graph-pattern layer before target planning

What this wave adds:
- a package-local runtime-shaped graph-pattern equivalence suite
- canonicalization of bounded internal query-fragment fixtures after alias resolution
- positive equivalence pairs covering:
  - variable renaming
  - predicate reordering
  - alias-version path equivalence
  - branch reordering
  - lineage-branch equivalence
  - operation/evidence branch equivalence
- explicit non-equivalence pairs covering:
  - optional versus required edges
  - anchor shifts
  - ComplianceTwin versus AdvisoryTwin posture shifts
  - current-state versus as-observed temporal posture
  - alias-path drift
  - relation changes

Why this is still bounded:
- the suite operates over a normalized internal fragment, not full QuerySpecification executor integration
- it closes graph-pattern equivalence only
- it does not claim execution-target equivalence, saved-query regression, or deployment-produced alias telemetry

Primary closure:
- moves `graph-pattern equivalence tests` from `NOT_STARTED` to `COVERED`

Validation summary:
- pair scenarios checked: 12
- equivalence pairs: 6
- non-equivalence pairs: 6
- query variants normalized: 24
- telemetry events emitted: 60
- overall: `PASS_WITH_LIMITATIONS`
