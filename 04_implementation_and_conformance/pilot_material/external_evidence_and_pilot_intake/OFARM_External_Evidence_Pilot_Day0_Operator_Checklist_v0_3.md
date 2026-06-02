# OFARM external evidence pilot day-0 operator checklist v0.3

Date: 2026-04-20
Status: active supporting implementation artifact
Scope: first-packet checklist for deployment teams sending runtime-surface, partner-output, or same-standard bridge evidence into the authenticity-gated intake lane

Supersedes:
- `OFARM_External_Evidence_Pilot_Day0_Operator_Checklist_v0_2.md`

---

Use this checklist before sending the first pilot artifact.

- [ ] Packet is for a **real** deployment artifact, not a rehearsal copy and not a cleaned template
- [ ] Filename uses the current production family for the correct live-evidence drop zone
- [ ] `templateOnly` is `false`
- [ ] Every placeholder is removed
- [ ] `authenticityEnvelope` is present
- [ ] `authenticityEnvelope.repositoryAuthored` is `false`
- [ ] `authenticityEnvelope.sourceRealityClass` is a real deployment, real live-field run, or accountable production approval and not rehearsal
- [ ] `authenticityEnvelope.attestedByRef` and `authenticityEnvelope.attestedAt` are explicit
- [ ] `authenticityEnvelope.artifactDigest` is explicit
- [ ] `qualificationClaim` is present and `claimKind` matches the lane
- [ ] `qualificationClaim.nonClaims` is explicit and honest
- [ ] Release bundle ref is explicit where required
- [ ] Deployment scope ref is explicit where required
- [ ] Surface identity or adapter surface identity is explicit where required
- [ ] Observed runtime binding is preserved directly or through a stable controlled alias
- [ ] Deployment evidence refs point to deployment-emitted or deployment-controlled records, not rehearsal packets
- [ ] Trace-back refs are explicit where required
- [ ] Blocked or warning outcomes are preserved instead of dropped
- [ ] API secrets, tokens, passwords, and raw access credentials are not included
- [ ] Direct personal identifiers are removed unless a specific approver identity is required and governed to appear
- [ ] Same-standard bridge packets are only sent when the artifact's evidence class is real and explicit
- [ ] `ofarm_external_evidence_intake_runner_v0_4.py` passes
- [ ] Reviewer handoff packet and reviewer checklist are bundled for the next step
