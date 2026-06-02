# live_evidence_packets — package map

Date: 2026-04-20
Status: active supporting implementation artifact
Scope: canonical intake locations for future external deployment evidence after the post-hardening package moved into implementation-and-evidence mode and gained an authenticity gate plus a reviewer-side decision lane

---

## Use this folder for

- future deployment-emitted runtime-surface evidence
- future partner-output telemetry artifacts collected from real deployments
- future same-standard bridge live-field telemetry, deployment-produced trace-back linkage, and production approval records

## Current posture

This folder is intentionally **prepared but unevidenced** in the current package.
Only README/index material is present here now.
Do not treat this folder as proof that real deployment evidence already exists.

Every future real artifact here is now expected to carry:
- an `authenticityEnvelope`
- a `qualificationClaim`

If you need a first-packet shape example, use:
- `../OFARM_External_Evidence_Pilot_Handoff_Packet_v0_3.md`
- `../OFARM_External_Evidence_Pilot_Day0_Operator_Checklist_v0_3.md`
- `../OFARM_External_Evidence_Redaction_and_Sovereignty_Note_v0_1.md`
- `../OFARM_External_Evidence_Authenticity_and_Qualification_Note_v0_1.md`
- `../pilot_intake_rehearsal/README.md`

The rehearsal lane stays outside this folder on purpose.
The accountable review decision lane lives under `../live_evidence_decisions/` and also stays separate on purpose.

## Drop zones

- `runtime_surface_release_lane/` — qualifying live deployment evidence for the governed runtime-surface release lane
- `same_standard_bridge/` — live-field bridge telemetry, deployment-produced trace-back linkage, and production promotion approval artifacts
- `partner_output_channels/` — implementation-support telemetry for partner-output channels; this does not by itself promote those channels into governed runtime-surface law

## Current entrypoints

- `../OFARM_External_Evidence_Intake_Packet_v0_4.md`
- `../OFARM_external_evidence_intake_registry_v0_4.json`
- `../OFARM_external_evidence_intake_results_v0_4.json`
- `../OFARM_External_Evidence_Pilot_Handoff_Packet_v0_3.md`
- `../OFARM_External_Evidence_Decision_and_Disposition_Packet_v0_2.md`
- `../OFARM_external_evidence_decision_registry_v0_2.json`
- `../OFARM_external_evidence_decision_results_v0_2.json`
- `../OFARM_External_Evidence_Authenticity_and_Qualification_Note_v0_1.md`
- `../OFARM_External_Evidence_Rehearsal_Fixtures_v0_2.md`
- `../OFARM_RuntimeSurface_Live_Deployment_Evidence_Operator_Note_v0_4.md`
- `../OFARM_live_field_same_standard_bridge_operator_note_v0_4.md`
