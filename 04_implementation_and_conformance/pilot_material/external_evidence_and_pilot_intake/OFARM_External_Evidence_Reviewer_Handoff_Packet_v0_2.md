# OFARM external evidence reviewer handoff packet v0.2

Date: 2026-04-20
Status: active supporting implementation artifact
Scope: practical reviewer-side handoff packet for the first accountable disposition of a real external evidence artifact after authenticity-gated intake

Supersedes:
- `OFARM_External_Evidence_Reviewer_Handoff_Packet_v0_1.md`

---

## Purpose

This packet is for the reviewer who receives the first real external evidence artifact after operator handoff.
The reviewer now has to judge two things explicitly:
- whether the artifact was attributed honestly as real external evidence rather than repo-authored rehearsal material
- what narrow claim the artifact is allowed to support

## Minimum reviewer sequence

1. read `OFARM_External_Evidence_Decision_and_Disposition_Packet_v0_2.md`
2. read `OFARM_External_Evidence_Authenticity_and_Qualification_Note_v0_1.md`
3. inspect `OFARM_external_evidence_intake_results_v0_4.json`
4. complete `OFARM_External_Evidence_Reviewer_Checklist_v0_2.md`
5. copy `OFARM_external_evidence_decision_record_template_v0_2.json` into the correct `live_evidence_decisions/` lane using the production filename family for that lane
6. record one accountable decision with explicit rationale codes
7. run `ofarm_external_evidence_decision_runner_v0_2.py`
8. keep refusals, holds, and rework requests; those decisions are still part of the evidence story

## Stop rules

Stop and correct the review packet if any of the following are true:
- the reviewed artifact is still under `pilot_intake_rehearsal/`
- the reviewed artifact still contains placeholders or `templateOnly: true`
- a positive decision is being recorded against an artifact that still says `repositoryAuthored: true`
- the decision record overclaims what the artifact proves
- partner-output telemetry is being marked as governed runtime-surface proof
- a same-standard bridge artifact is being marked as promotion-ready without pair-specific evidence coverage
- the decision record does not point back to `OFARM_external_evidence_intake_results_v0_4.json`

## Bottom line

Make the smallest honest accountable decision that matches the reviewed artifact, its authenticity envelope, and its bounded qualification claim.
If the artifact only supports a hold, rework, or non-qualifying decision, record that directly.
