# OFARM external evidence pilot handoff packet v0.3

Date: 2026-04-20
Status: active supporting implementation artifact
Scope: practical handoff packet for the first real deployment team sending OFARM external evidence into the authenticity-gated intake lane and forward into the reviewer-side decision lane

Supersedes:
- `OFARM_External_Evidence_Pilot_Handoff_Packet_v0_2.md`

---

## Purpose

This packet is the operator-facing bridge between the current package and the first real pilot artifact.
The remaining debt is still attributable deployment evidence plus one honest accountable decision.
This refresh closes one more ambiguity: a production-shaped JSON is not enough by itself.
A real packet now also needs an explicit authenticity envelope and a bounded qualification claim.

## What to send now

### Minimum first packet

Send **one redacted runtime-surface evidence artifact** when a real governed runtime surface can be observed in deployment.
Use the current filename family in:
- `live_evidence_packets/runtime_surface_release_lane/`

Optional in the same pilot packet:
- one redacted partner-output telemetry artifact in `live_evidence_packets/partner_output_channels/`

### Do not send yet unless all three are real

Do **not** treat same-standard bridge promotion as ready unless all three real artifacts exist:
- live-field telemetry
- deployment-produced trace-back linkage
- accountable production approval

## First-use sequence

1. read `OFARM_External_Evidence_Redaction_and_Sovereignty_Note_v0_1.md`
2. read `OFARM_External_Evidence_Authenticity_and_Qualification_Note_v0_1.md`
3. complete `OFARM_External_Evidence_Pilot_Day0_Operator_Checklist_v0_3.md`
4. inspect the rehearsal lane under `pilot_intake_rehearsal/` if this is the first operator packet
5. place only real deployment artifacts into `live_evidence_packets/` using the production filename families
6. run `ofarm_external_evidence_intake_runner_v0_4.py`
7. hand the packet forward using:
   - `OFARM_External_Evidence_Reviewer_Handoff_Packet_v0_2.md`
   - `OFARM_External_Evidence_Reviewer_Checklist_v0_2.md`
8. keep blocked runs, warnings, and denials; they are still evidence

## Stop rules

Stop and correct the packet if any of the following are true:
- placeholders remain
- `templateOnly` is still `true`
- `authenticityEnvelope.repositoryAuthored` is still `true`
- `authenticityEnvelope.sourceRealityClass` still says rehearsal or other non-real capture mode
- the file was left under `pilot_intake_rehearsal/` but is being claimed as live evidence
- a runtime binding was replaced with vague prose rather than a stable controlled alias or binding record
- partner-output telemetry is being claimed as governed runtime-surface proof by itself
- a same-standard bridge packet is missing one of the three required evidence classes

## Non-claims

This handoff packet does **not** mean:
- runtime-surface live deployment evidence already exists in the package
- partner-output channels are promoted into governed runtime-surface law
- same-standard bridge draft pairs are promotion-ready
- `RuntimeSurfaceContract v0.2` is the package default

## Bottom line

Send the smallest honest redacted packet that preserves release identity, surface identity, binding meaning, trace-back provenance, and attributable authenticity.
Do not widen scope to make the packet look more complete than the deployment actually proves.
