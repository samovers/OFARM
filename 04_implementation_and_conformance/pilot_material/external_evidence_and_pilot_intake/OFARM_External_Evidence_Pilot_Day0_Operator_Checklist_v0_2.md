# OFARM external evidence pilot day-0 operator checklist v0.2

Date: 2026-04-20
Status: active supporting implementation artifact
Scope: first-packet checklist for deployment teams sending runtime-surface or partner-output evidence into the current intake lane before reviewer-side disposition begins

Supersedes:
- `OFARM_External_Evidence_Pilot_Day0_Operator_Checklist_v0_1.md`

---

Use this checklist before sending the first pilot artifact.

- [ ] Packet is for a **real** deployment artifact, not a template and not a rehearsal copy
- [ ] Filename uses the current production family for the correct live-evidence drop zone
- [ ] `templateOnly` is `false`
- [ ] Every placeholder is removed
- [ ] Release bundle ref is explicit
- [ ] Deployment scope ref is explicit
- [ ] Surface identity or adapter surface identity is explicit
- [ ] Observed runtime binding is preserved directly or through a stable controlled alias
- [ ] Deployment evidence refs point to deployment-emitted or deployment-controlled records, not package-local replay artifacts
- [ ] Trace-back refs are explicit where required
- [ ] Blocked or warning outcomes are preserved instead of dropped
- [ ] API secrets, tokens, passwords, and raw access credentials are not included
- [ ] Direct personal identifiers are removed unless a specific approver identity is required and governed to appear
- [ ] Same-standard bridge packets are only sent when all required evidence classes exist
- [ ] `ofarm_external_evidence_intake_runner_v0_3.py` passes
- [ ] Reviewer handoff packet and reviewer checklist are bundled for the next step
