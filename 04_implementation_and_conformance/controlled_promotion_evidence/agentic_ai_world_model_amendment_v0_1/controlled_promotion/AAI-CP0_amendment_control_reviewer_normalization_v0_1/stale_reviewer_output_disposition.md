# Stale reviewer-output disposition v0.1

Generated: 2026-05-16T12:00:00+02:00

Source reviewer output: `reviewed_regulatory_inspector_thread_v0_1/review/OFARM_regulatory_inspector_review_output_v0_1.json`

Source review date: 2026-04-17. Current package date: 2026-05-15.

## Rule

Use the regulatory review as historical reviewer evidence. Do not reopen closed findings unless a new contradiction is found in the current active authority set.

## Disposition table

| Source finding | Current status | Current package disposition | CP0 reuse rule |
|---|---|---|---|
| REG-001 | closed_in_package_v0_5 | closed in active package | do_not_reopen_without_new_contradiction |
| REG-002 | closed_in_package_v0_5 | closed in active/supporting package | do_not_reopen_without_new_contradiction |
| REG-003 | closed_in_package_v0_5 | closed in active package | do_not_reopen_without_new_contradiction |
| REG-004 | closed_in_package_v0_5 | closed in active package | do_not_reopen_without_new_contradiction |
| REG-005 | closed_in_package_v0_5 | closed in active package | do_not_reopen_without_new_contradiction |
| REG-006/015/016 | closed_in_package_v0_5 | closed in supporting implementation package | do_not_reopen_without_new_contradiction |
| REG-007 | closed_in_package_v0_5 | closed in active/supporting package | do_not_reopen_without_new_contradiction |
| REG-008 | closed_in_package_v0_5 | closed in package metadata tooling | do_not_reopen_without_new_contradiction |
| REG-011 | open_external_evidence_blocker | bounded external dependency remains | carry_as_bounded_external_dependency_not_agentic_cp0_blocker |
| REG-009 | carry_forward_to_CP2_CP4_CP6_as_test_assumption | not directly closed by issue register; preserved as hostile-runtime concern | use as runtime hostile-test assumption, not as proof of an open model-law gap |
| REG-010 | subsumed_or_bounded | substantially addressed by reference snapshot and code-binding closures; verify against current closure before reuse | do not reopen unless a new current artifact contradicts closure |
| REG-012/013/014 | closed_in_package_v0_5 | closed by active package landing artifacts named in REG-001, REG-003, and REG-004 issue-register entries | treat as implemented closure context; do not duplicate in agentic amendment unless new agentic field binding is needed |
| REG-017 | preserve | preserved and strengthened by AAI-P1 baseline clarification | preserve as non-negotiable amendment boundary |

## CP0 decision

The regulatory-review output remains useful, but it is stale relative to current closure artifacts. CP1 and later phases should reuse it only for preserved warnings, hostile-test assumptions, or unresolved external blockers.
