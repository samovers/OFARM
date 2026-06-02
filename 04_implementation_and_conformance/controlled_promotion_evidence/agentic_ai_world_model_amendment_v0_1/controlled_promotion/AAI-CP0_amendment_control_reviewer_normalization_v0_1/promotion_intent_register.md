# Promotion-intent register v0.1

Generated: 2026-05-16T12:00:00+02:00

Status: supporting control register. This register promotes nothing. It maps recommendations to future authority destinations so that later work cannot silently convert review-holding or draft material into active law.

| ID | Phase | Target authority class | Current disposition | Next gate |
|---|---|---|---|---|
| CP0-001 | AAI-CP0 | IMPLEMENTATION_CONFORMANCE | started_and_packaged_no_active_law_change | CP0 validation report passes; proceed to CP1 baseline release-gate patch. |
| CP1-001 | AAI-CP1 | BASELINE_PATCH | candidate_for_CP1_not_started | CP1 draft patch must preserve no-hidden-truth and avoid schema promotion. |
| CP2-001 | AAI-CP2 | ACCEPTED_RFC_PLUS_MACHINE_CONTRACTS | candidate_for_CP2 | ADR or RFC review with negative cases. |
| CP3-001 | AAI-CP3 | ACCEPTED_RFC_PLUS_MACHINE_CONTRACTS | candidate_for_CP3 | ADR: Agent actorship and sponsor-bound authority. |
| CP4-001 | AAI-CP4 | ACCEPTED_RFC_PLUS_MACHINE_CONTRACTS | candidate_for_CP4 | ADR: Agent run envelope, trace, and handoff obligations. |
| CP5-001 | AAI-CP5 | ACCEPTED_RFC_PLUS_COMPANION_PLUS_MACHINE_CONTRACTS | candidate_for_CP5 | Manifest-overclaim negative examples. |
| CP6-001 | AAI-CP6 | CONFORMANCE_FIXTURE | implementation_experiment_required | Runtime execution report with expected blocked traces. |
| CP7-001 | AAI-CP7 | ACCEPTED_RFC_PLUS_MACHINE_CONTRACTS | candidate_for_later_deep_research_then_CP7 | Deep research or hostile review focused on advisory-world-model governance. |
| CP8-001 | AAI-CP8 | ACCEPTED_RFC_PLUS_COMPANION_PLUS_MACHINE_CONTRACTS | candidate_for_later_deep_research_then_CP8 | UX prototype and request-lifecycle conformance. |
| CP9-001 | AAI-CP9 | CONFORMANCE_FIXTURE_PLUS_IMPLEMENTATION_GUIDANCE | experiment_required | Farmer-value scenario execution report. |
| HOLD-001 | postpone | POSTPONED_ITEM | hold | Remain held. |

## CP0 decision

Proceed to CP1 only after preserving the CP0 rule that every recommendation must be routed to one primary destination class before drafting begins.
