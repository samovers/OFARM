# OFARM external evidence reviewer handoff packet v0.1

Date: 2026-04-20
Status: active supporting implementation artifact
Scope: practical reviewer-side handoff packet for the first accountable disposition of a real external evidence artifact

---

## Purpose

This packet is for the reviewer who receives the first real external evidence artifact after operator handoff.
It exists because the first pilot packet should not stop at “the JSON is in the right folder.”
A named reviewer still needs to say what the artifact counts as and what it still does not prove.

## Minimum reviewer sequence

1. read `OFARM_External_Evidence_Decision_and_Disposition_Packet_v0_1.md`
2. inspect `OFARM_external_evidence_intake_results_v0_3.json`
3. complete `OFARM_External_Evidence_Reviewer_Checklist_v0_1.md`
4. copy `OFARM_external_evidence_decision_record_template_v0_1.json` into the correct `live_evidence_decisions/` lane using the production filename family for that lane
5. record one accountable decision with explicit rationale codes
6. run `ofarm_external_evidence_decision_runner_v0_1.py`
7. keep refusals, holds, and rework requests; those decisions are still part of the evidence story

## Stop rules

Stop and correct the review packet if any of the following are true:
- the reviewed artifact is still under `pilot_intake_rehearsal/`
- the reviewed artifact still contains placeholders or `templateOnly: true`
- the decision record overclaims what the artifact proves
- partner-output telemetry is being marked as governed runtime-surface proof
- a same-standard bridge artifact is being marked as promotion-ready without pair-specific evidence coverage
- the decision record does not point back to `OFARM_external_evidence_intake_results_v0_3.json`

## Non-claims

This reviewer packet does **not** mean:
- real deployment evidence already exists in the package
- runtime-surface v0.2 becomes default
- partner-output channels are promoted into governed runtime-surface law
- same-standard bridge draft pairs are automatically ready for promotion

## Bottom line

Make the smallest honest accountable decision that matches the reviewed artifact.
Do not fill semantic or operational gaps by optimism.
If the artifact only supports a hold, rework, or non-qualifying decision, record that directly.
