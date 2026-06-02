# OFARM external evidence intake packet v0.3

Date: 2026-04-20
Status: active supporting implementation artifact
Scope: current package-level entrypoint for the implementation-and-evidence phase after adding reviewer-side disposition support and cleaning the intake lane onto the same currentness posture

Supersedes:
- `OFARM_External_Evidence_Intake_Packet_v0_2.md`

---

## Purpose

This packet is now the current entrypoint for external evidence work.
It keeps the same three evidence lanes introduced earlier.
It carries forward the operator-facing handoff kit and the bounded rehearsal lane.
It now adds one reviewer-side decision lane so the first real pilot packet can land on an accountable recorded disposition rather than stopping at structural intake.

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
   - `OFARM_External_Evidence_Pilot_Handoff_Packet_v0_2.md`
   - `OFARM_External_Evidence_Pilot_Day0_Operator_Checklist_v0_2.md`
   - `OFARM_External_Evidence_Redaction_and_Sovereignty_Note_v0_1.md`
2. inspect the non-qualifying rehearsal lane under `pilot_intake_rehearsal/`
3. keep rehearsal packets **outside** `live_evidence_packets/`
4. only place real deployment artifacts into `live_evidence_packets/` using the current production filename families
5. run `ofarm_external_evidence_intake_runner_v0_3.py`
6. use the reviewer-side decision lane:
   - `OFARM_External_Evidence_Decision_and_Disposition_Packet_v0_1.md`
   - `OFARM_External_Evidence_Reviewer_Handoff_Packet_v0_1.md`
   - `OFARM_External_Evidence_Reviewer_Checklist_v0_1.md`
   - `OFARM_external_evidence_decision_record_template_v0_1.json`
7. place any real accountable decision record into `live_evidence_decisions/`
8. run `ofarm_external_evidence_decision_runner_v0_1.py`
9. refresh the readiness packet only if qualifying evidence actually arrives and an accountable decision is recorded, or a contradiction appears

## Rehearsal boundary

The rehearsal lane is deliberately non-qualifying.
It exists to show production-shaped artifact structure without polluting the canonical live-evidence drop zones.

Current rehearsal support:
- `pilot_intake_rehearsal/runtime_surface_release_lane/OFARM_runtime_surface_live_deployment_evidence_rehearsal_v0_1.json`
- `pilot_intake_rehearsal/partner_output_channels/OFARM_runtime_surface_partner_output_telemetry_rehearsal_v0_1.json`
- `OFARM_External_Evidence_Rehearsal_Fixtures_v0_1.md`
- `OFARM_external_evidence_rehearsal_results_v0_2.json`

By design, there is **no** same-standard bridge rehearsal artifact in this packet because a fake live-field bridge packet would blur the production-evidence threshold.

## Current package state

At this snapshot:
- the package is internally closed enough for the current scope
- the thin active-contract reference harness is present
- the external evidence intake lane is operationalized
- the pilot handoff kit is current
- the reviewer-side decision lane is prepared
- the rehearsal lane is present and explicitly non-qualifying
- qualifying live deployment evidence count remains zero
- accountable review decision count remains zero

## Current entry documents

- `OFARM_external_evidence_intake_registry_v0_3.json`
- `OFARM_external_evidence_intake_results_v0_3.json`
- `OFARM_External_Evidence_Pilot_Handoff_Packet_v0_2.md`
- `OFARM_External_Evidence_Pilot_Day0_Operator_Checklist_v0_2.md`
- `OFARM_External_Evidence_Redaction_and_Sovereignty_Note_v0_1.md`
- `OFARM_External_Evidence_Rehearsal_Fixtures_v0_1.md`
- `OFARM_external_evidence_rehearsal_results_v0_2.json`
- `OFARM_External_Evidence_Decision_and_Disposition_Packet_v0_1.md`
- `OFARM_external_evidence_decision_registry_v0_1.json`
- `OFARM_external_evidence_decision_results_v0_1.json`
- `live_evidence_packets/README.md`
- `live_evidence_decisions/README.md`
- `pilot_intake_rehearsal/README.md`
- `OFARM_post_hardening_readiness_packet_index_v0_6.md`
