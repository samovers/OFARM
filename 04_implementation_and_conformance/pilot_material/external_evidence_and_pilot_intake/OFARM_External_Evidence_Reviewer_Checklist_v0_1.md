# OFARM external evidence reviewer checklist v0.1

Date: 2026-04-20
Status: active supporting implementation artifact
Scope: reviewer-side checklist for accountable disposition of a real external evidence artifact

---

Use this checklist before recording a decision in `live_evidence_decisions/`.

- [ ] Reviewed artifact lives under `live_evidence_packets/`, not under `pilot_intake_rehearsal/`
- [ ] Reviewed artifact uses the correct production filename family for its lane
- [ ] `OFARM_external_evidence_intake_results_v0_3.json` was rerun against the current artifact set
- [ ] Reviewed artifact is not template-only and does not contain unresolved placeholders
- [ ] Reviewed artifact scope matches the lane being reviewed
- [ ] Runtime-surface evidence is not overclaimed beyond the governed release lane it actually proves
- [ ] Partner-output telemetry is kept as support evidence unless a later explicit promotion threshold is crossed
- [ ] Same-standard bridge review is pair-specific and does not overclaim beyond the actual evidence class coverage
- [ ] Decision rationale codes are explicit
- [ ] Reviewer party ref and reviewer role ref are explicit
- [ ] `ofarm_external_evidence_decision_runner_v0_1.py` passes
