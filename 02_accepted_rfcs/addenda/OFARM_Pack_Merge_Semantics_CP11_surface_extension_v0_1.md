# OFARM Pack Merge Semantics — CP11 Sustainability Surface Extension v0.1

Status: accepted addendum; machine contracts remain draft/non-default where applicable.

## CP11 pack surface families

| Surface family | Default merge posture |
|---|---|
| SUSTAINABILITY_CONSTRAINT | CONSTRAINT_INTERSECTION or STRONGEST_REQUIREMENT; otherwise HARD_FAIL |
| SUSTAINABILITY_OBJECTIVE | ADDITIVE_UNION for compatible objectives; ORDERED_COMPOSITION when priority order explicit; otherwise HARD_FAIL |
| SUSTAINABILITY_OBJECTIVE_PRIORITY | ORDERED_COMPOSITION only when precedence explicit and deterministic; otherwise HARD_FAIL |
| SUSTAINABILITY_TRADEOFF_POLICY | STRONGEST_REQUIREMENT for stricter review/prohibition posture; otherwise HARD_FAIL |
| SUSTAINABILITY_EVIDENCE_POLICY | STRONGEST_REQUIREMENT when cumulative and non-contradictory; otherwise HARD_FAIL |
| SUSTAINABILITY_METRIC_PROFILE | IDENTICAL_ONLY for claim-bearing use unless method/unit equivalence is proven; otherwise HARD_FAIL |
| SUSTAINABILITY_CLAIM_RULE | STRONGEST_REQUIREMENT for stronger basis/disclosure/review requirements; otherwise HARD_FAIL |
| CHARTER_EXCEPTION_POLICY | STRONGEST_REQUIREMENT for stricter approval, scope, evidence, expiry, or disclosure; otherwise HARD_FAIL |
| CHARTER_BREACH_POLICY | STRONGEST_REQUIREMENT for stricter detection, review, contestation, disclosure, or resolution; otherwise HARD_FAIL |

## Required pack-contract behaviour

`PackActivationSet`, `PackMergePolicy`, and `PackMergeResolutionTrace` must recognise the CP11 surface families above before CP11 pack-related conformance claims are made.

Conflicting sustainability pack rules must not silently merge.
