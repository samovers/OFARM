
# OFARM external evidence intake packet v0.1

Date: 2026-04-20
Status: active supporting implementation artifact
Scope: package-level operational packet for collecting future external deployment evidence without reopening OFARM law or promoting draft lanes prematurely

---

## Purpose

This packet turns the post-hardening **implementation-and-evidence** phase into an executable intake path.
It does not fabricate evidence.
It does not promote any draft lane by itself.
It provides one current entrypoint for where future live artifacts belong and how they will be re-evaluated.

## Evidence lanes covered

### 1. Governed runtime-surface live deployment evidence

Use when a real deployment can prove one governed runtime surface in the current release lane.

Current target drop zone:
- `live_evidence_packets/runtime_surface_release_lane/`

Current production filename family:
- `OFARM_runtime_surface_live_deployment_evidence_v*.json`

Governing context already present in the package:
- `../02_accepted_rfcs/OFARM_RuntimeSurface_Live_Deployment_Evidence_and_Output_Telemetry_Closure_Note_v0_1.md`
- `OFARM_RuntimeSurface_Live_Deployment_Evidence_Operator_Note_v0_2.md`
- `OFARM_runtime_surface_live_deployment_evidence_capture_template_v0_1.json`

### 2. Partner-output telemetry support evidence

Use when a real deployment emits partner-output telemetry that needs to be tied back to the release lane and publication traces.

Current target drop zone:
- `live_evidence_packets/partner_output_channels/`

Current production filename family:
- `OFARM_runtime_surface_partner_output_telemetry_v*.json`

Important boundary:
- these artifacts support traceability and future promotion analysis
- they do **not** by themselves promote implementation-local partner-output channels into governed runtime-surface law

### 3. Same-standard bridge promotion evidence

Use only when a real deployment exists for a same-standard bridge candidate pair.

Current target drop zone:
- `live_evidence_packets/same_standard_bridge/`

Current production filename families:
- `OFARM_live_field_same_standard_bridge_telemetry_v*.json`
- `OFARM_live_field_same_standard_bridge_trace_back_records_v*.json`
- `OFARM_same_standard_bridge_production_approval_record_v*.json`

Current blocking evidence classes:
- `LIVE_FIELD_COLLECTED_SAME_STANDARD_BRIDGE_TELEMETRY`
- `DEPLOYMENT_PRODUCED_TRACE_BACK_LINKAGE`
- `PRODUCTION_PROMOTION_APPROVAL_RECORD`

## Use order

1. collect or export the real deployment artifact
2. place it in the correct `live_evidence_packets/` drop zone using the current production filename family
3. keep all placeholders removed and all identifiers deployment-specific
4. run `ofarm_external_evidence_intake_runner_v0_1.py`
5. refresh the readiness packet only if qualifying evidence is actually present

## Non-claims

This packet does **not** claim that:
- real live deployment evidence already exists in the package
- ADAPT or ISOXML same-standard bridge pairs are promotion-ready now
- `RuntimeSurfaceContract v0.2` is the default current runtime-surface contract
- implementation-local partner-output channels are already governed runtime-surface lanes
- a filing-boundary equivalent contract lane is active

## Current package state

At this snapshot:
- the package is internally closed enough for the current scope
- the thin active-contract reference harness is present
- the remaining material debt is external evidence debt
- qualifying live deployment evidence count remains zero

## Current entry documents

- `OFARM_external_evidence_intake_registry_v0_1.json`
- `OFARM_external_evidence_intake_results_v0_1.json`
- `OFARM_RuntimeSurface_Live_Deployment_Evidence_Operator_Note_v0_2.md`
- `OFARM_live_field_same_standard_bridge_operator_note_v0_2.md`
- `OFARM_post_hardening_readiness_packet_index_v0_4.md`
