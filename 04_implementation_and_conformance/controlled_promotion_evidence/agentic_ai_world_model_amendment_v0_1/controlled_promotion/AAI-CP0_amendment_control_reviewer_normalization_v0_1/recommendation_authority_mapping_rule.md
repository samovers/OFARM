# Recommendation authority mapping rule v0.1

Generated: 2026-05-16T12:00:00+02:00

Status: supporting control rule, not baseline law.

Every future synthesis finding, reviewer recommendation, and CP-phase proposal must be mapped to one primary destination class before drafting begins.

Allowed destination classes:

- BASELINE_PATCH
- ACCEPTED_RFC
- COMPANION_ARTIFACT
- MACHINE_CONTRACT
- CONFORMANCE_FIXTURE
- IMPLEMENTATION_ONLY_NOTE
- POSTPONED_ITEM

| Rule | Requirement | Reason |
|---|---|---|
| MAP-001 | Every recommendation must name exactly one primary destination class before drafting begins. | Prevents review-holding or supporting material from being silently treated as active law. |
| MAP-002 | A BASELINE_PATCH may clarify model/runtime law but must not promote draft schemas by implication. | Baseline law has the highest authority and must remain narrow. |
| MAP-003 | A MACHINE_CONTRACT promotion requires an accepted RFC or an existing active baseline/companion basis plus positive and negative examples. | Schemas should execute law; they should not create law alone. |
| MAP-004 | A CONFORMANCE_FIXTURE proves behavior only inside its tested profile and cannot create active semantic law. | Runtime evidence should not overclaim authority. |
| MAP-005 | Review-holding material can supply evidence or candidate text only after its folder status and stale-disposition are recorded. | Prevents stale or contextual materials from bypassing authority order. |
| MAP-006 | A POSTPONED_ITEM must include the risk that blocks promotion and the separate review needed to reopen it. | Avoids implicit future acceptance of held concepts. |
| MAP-007 | Every finding or recommendation must cite at least one active artifact, supporting artifact, reviewed artifact, or mark insufficient evidence. | Preserves traceability and confidence discipline. |
