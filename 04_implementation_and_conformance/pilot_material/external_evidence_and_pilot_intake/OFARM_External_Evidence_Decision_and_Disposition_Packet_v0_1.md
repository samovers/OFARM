# OFARM external evidence decision and disposition packet v0.1

Date: 2026-04-20
Status: active supporting implementation artifact
Scope: current reviewer-side entrypoint for accountable disposition of real external evidence after operator handoff, intake qualification, and rehearsal support were already operationalized

---

## Purpose

This packet is the reviewer-side companion to the current external evidence intake packet.
It separates two questions that should not be silently merged:

1. **intake qualification** — is the artifact in the correct lane, structurally complete enough, and non-template enough to be considered?
2. **accountable disposition** — has a named reviewer recorded what the artifact counts as, what it does not count as, and whether follow-up is still required?

The package already had the first question operationalized.
This packet makes the second question explicit.

It still does **not** fabricate deployment evidence.
It still does **not** promote a draft lane by itself.

## Decision lanes covered

### 1. Governed runtime-surface live deployment evidence

Use when a real artifact under `live_evidence_packets/runtime_surface_release_lane/` appears to qualify as governed runtime-surface live deployment evidence.

Typical positive disposition:
- `QUALIFY_AS_GOVERNED_RUNTIME_SURFACE_LIVE_EVIDENCE`

Typical hold/rework dispositions:
- `REQUIRE_REDACTION_REWORK`
- `REQUIRE_SCOPE_REVIEW`
- `REJECT_AS_NON_QUALIFYING`

### 2. Partner-output telemetry support evidence

Use when a real artifact under `live_evidence_packets/partner_output_channels/` is acceptable as partner-output support telemetry.

Typical positive disposition:
- `QUALIFY_AS_PARTNER_OUTPUT_SUPPORT_EVIDENCE`

Important boundary:
- this still does **not** by itself promote dashboard, CSV, PDF, dossier, or submission channels into governed runtime-surface law

### 3. Same-standard bridge promotion evidence

Use when real artifacts under `live_evidence_packets/same_standard_bridge/` are reviewed for bridge-promotion gating.

Typical dispositions:
- `COUNT_TOWARD_SAME_STANDARD_BRIDGE_PROMOTION_GATE`
- `HOLD_FOR_BRIDGE_SET_COMPLETION`
- `REQUIRE_REDACTION_REWORK`
- `REQUIRE_SCOPE_REVIEW`
- `REJECT_AS_NON_QUALIFYING`

Important boundary:
- one reviewed artifact does not by itself promote a bridge pair
- pair-specific bridge promotion still requires the full evidence class set plus an explicit later promotion decision

## Current operating sequence

1. operator uses `OFARM_External_Evidence_Pilot_Handoff_Packet_v0_2.md`
2. operator completes `OFARM_External_Evidence_Pilot_Day0_Operator_Checklist_v0_2.md`
3. operator places only real deployment artifacts in `live_evidence_packets/`
4. operator or reviewer runs `ofarm_external_evidence_intake_runner_v0_3.py`
5. reviewer reads `OFARM_External_Evidence_Reviewer_Handoff_Packet_v0_1.md`
6. reviewer completes `OFARM_External_Evidence_Reviewer_Checklist_v0_1.md`
7. reviewer copies `OFARM_external_evidence_decision_record_template_v0_1.json` into the matching `live_evidence_decisions/` lane and records an accountable decision
8. reviewer runs `ofarm_external_evidence_decision_runner_v0_1.py`
9. refresh the readiness packet only after a real evidence artifact and a real accountable decision both exist, or a contradiction appears

## Current package state

At this snapshot:
- the live-evidence intake lane is current and executable
- the pilot handoff kit is current
- the rehearsal lane remains explicitly non-qualifying
- the reviewer-side decision lane is now prepared
- accountable review decision count remains zero
- qualifying live deployment evidence count remains zero

## Current entry documents

- `OFARM_External_Evidence_Intake_Packet_v0_3.md`
- `OFARM_external_evidence_intake_registry_v0_3.json`
- `OFARM_external_evidence_intake_results_v0_3.json`
- `OFARM_External_Evidence_Reviewer_Handoff_Packet_v0_1.md`
- `OFARM_External_Evidence_Reviewer_Checklist_v0_1.md`
- `OFARM_external_evidence_decision_record_template_v0_1.json`
- `OFARM_external_evidence_decision_registry_v0_1.json`
- `OFARM_external_evidence_decision_results_v0_1.json`
- `live_evidence_decisions/README.md`
- `OFARM_post_hardening_readiness_packet_index_v0_6.md`
