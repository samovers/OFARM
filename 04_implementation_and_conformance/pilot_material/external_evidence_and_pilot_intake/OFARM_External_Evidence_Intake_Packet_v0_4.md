# OFARM external evidence intake packet v0.4

Date: 2026-04-20
Status: active supporting implementation artifact
Scope: current package-level entrypoint for the implementation-and-evidence phase after adding an explicit authenticity and qualification gate to the live external-evidence lane

Supersedes:
- `OFARM_External_Evidence_Intake_Packet_v0_3.md`

---

## Purpose

This packet is the current entrypoint for external evidence work.
The package already had live evidence lanes, a pilot handoff kit, a rehearsal lane, and a reviewer-side decision lane.
This refresh adds one narrower requirement:
**a production-shaped file is not enough to count as pilot evidence unless it also carries an explicit authenticity envelope and bounded qualification claim.**

This packet still does **not** fabricate evidence.
It still does **not** promote any draft lane by itself.

## Evidence lanes covered

### 1. Governed runtime-surface live deployment evidence

Use when a real deployment can prove one governed runtime surface in the current release lane.

Current target drop zone:
- `live_evidence_packets/runtime_surface_release_lane/`

Current production filename family:
- `OFARM_runtime_surface_live_deployment_evidence_v*.json`

### 2. Partner-output telemetry support evidence

Use when a real deployment emits partner-output telemetry that must be tied back to release-bound publication traces.

Current target drop zone:
- `live_evidence_packets/partner_output_channels/`

Current production filename family:
- `OFARM_runtime_surface_partner_output_telemetry_v*.json`

Important boundary:
- these artifacts support traceability and future promotion analysis
- they do **not** by themselves promote implementation-local partner-output channels into governed runtime-surface law

### 3. Same-standard bridge promotion evidence

Use only when a real deployment exists for one of the same-standard bridge draft pairs.

Current target drop zone:
- `live_evidence_packets/same_standard_bridge/`

Current production filename families:
- `OFARM_live_field_same_standard_bridge_telemetry_v*.json`
- `OFARM_live_field_same_standard_bridge_trace_back_records_v*.json`
- `OFARM_same_standard_bridge_production_approval_record_v*.json`

## Current operating sequence

1. if no real deployment artifact exists yet, start with the pilot handoff kit:
   - `OFARM_External_Evidence_Pilot_Handoff_Packet_v0_3.md`
   - `OFARM_External_Evidence_Pilot_Day0_Operator_Checklist_v0_3.md`
   - `OFARM_External_Evidence_Redaction_and_Sovereignty_Note_v0_1.md`
   - `OFARM_External_Evidence_Authenticity_and_Qualification_Note_v0_1.md`
2. inspect the non-qualifying rehearsal lane under `pilot_intake_rehearsal/`
3. keep rehearsal packets **outside** `live_evidence_packets/`
4. only place real deployment artifacts into `live_evidence_packets/` using the current production filename families
5. require an `authenticityEnvelope` and a `qualificationClaim` in each real artifact
6. run `ofarm_external_evidence_intake_runner_v0_4.py`
7. use the reviewer-side decision lane:
   - `OFARM_External_Evidence_Decision_and_Disposition_Packet_v0_2.md`
   - `OFARM_External_Evidence_Reviewer_Handoff_Packet_v0_2.md`
   - `OFARM_External_Evidence_Reviewer_Checklist_v0_2.md`
   - `OFARM_external_evidence_decision_record_template_v0_2.json`
8. place any real accountable decision record into `live_evidence_decisions/`
9. run `ofarm_external_evidence_decision_runner_v0_2.py`
10. refresh the readiness packet only if qualifying evidence actually arrives and an accountable decision is recorded, or a contradiction appears

## Rehearsal boundary

The rehearsal lane is deliberately non-qualifying.
It exists to show production-shaped artifact structure without polluting the canonical live-evidence drop zones.
Rehearsal packets are now also expected to mark themselves as repo-authored inside the authenticity envelope so copied rehearsal files cannot pass as real pilot evidence by accident.

## Current package state

At this snapshot:
- the package is internally closed enough for the current scope
- the thin active-contract reference harness is present
- the external evidence intake lane is operationalized
- the pilot handoff kit is current
- the reviewer-side decision lane is prepared
- the rehearsal lane is present, explicitly non-qualifying, and explicitly repo-authored
- the authenticity and qualification gate is now present
- qualifying live deployment evidence count remains zero
- accountable review decision count remains zero
