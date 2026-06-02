# OFARM external evidence reviewer checklist v0.2

Date: 2026-04-20
Status: active supporting implementation artifact
Scope: reviewer checklist for accountable disposition of real external evidence artifacts after authenticity-gated intake

Supersedes:
- `OFARM_External_Evidence_Reviewer_Checklist_v0_1.md`

---

Use this checklist before recording a decision.

- [ ] `OFARM_external_evidence_intake_results_v0_4.json` has been reviewed
- [ ] Reviewed artifact is in the correct `live_evidence_packets/` lane
- [ ] Reviewed artifact is not under `pilot_intake_rehearsal/`
- [ ] Reviewed artifact no longer has placeholders or `templateOnly: true`
- [ ] Reviewed artifact has an `authenticityEnvelope`
- [ ] For any positive decision, `authenticityEnvelope.repositoryAuthored` is `false`
- [ ] `authenticityEnvelope.attestedByRef`, `attestedAt`, and `artifactDigest` are explicit
- [ ] `qualificationClaim.claimKind` matches the lane and the intended decision
- [ ] `qualificationClaim.nonClaims` is explicit and has not been silently ignored
- [ ] Decision record repeats the reviewed artifact digest accurately
- [ ] Decision record repeats the reviewed artifact claim kind accurately
- [ ] Runtime-surface evidence is only counted for the governed release lane it actually proves
- [ ] Partner-output telemetry is kept as support evidence unless a later explicit promotion threshold is crossed
- [ ] Same-standard bridge review is pair-specific and does not overclaim beyond the actual evidence class coverage
- [ ] Decision rationale codes are explicit
- [ ] Reviewer party ref and reviewer role ref are explicit
- [ ] `ofarm_external_evidence_decision_runner_v0_2.py` passes
