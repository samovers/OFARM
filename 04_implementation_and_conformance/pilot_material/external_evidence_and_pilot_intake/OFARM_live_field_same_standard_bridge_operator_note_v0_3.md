# OFARM live-field same-standard bridge operator note v0.3

Date: 2026-04-20
Status: active supporting implementation artifact
Scope: operator-facing steps for placing future same-standard bridge promotion evidence into the canonical external evidence intake lane and forward into the reviewer-side decision lane

Supersedes:
- `OFARM_live_field_same_standard_bridge_operator_note_v0_2.md`

---

## Use this when

Use this note only when a real live deployment exists for one of the same-standard bridge draft pairs.
Until then, keep the capture files as templates and do not rename them into the production filename families.

## Target production filenames and location

Place future real artifacts in `live_evidence_packets/same_standard_bridge/` using these filename families:

- `OFARM_live_field_same_standard_bridge_telemetry_v*.json`
- `OFARM_live_field_same_standard_bridge_trace_back_records_v*.json`
- `OFARM_same_standard_bridge_production_approval_record_v*.json`

## Fill order

1. fill the live-field telemetry artifact first
2. fill the deployment-produced trace-back artifact second
3. fill the production approval artifact last
4. run `ofarm_external_evidence_intake_runner_v0_3.py`
5. hand the packet to the reviewer using `OFARM_External_Evidence_Reviewer_Handoff_Packet_v0_1.md`
6. record any accountable bridge decision under `live_evidence_decisions/same_standard_bridge/`
7. refresh bridge-promotion posture only if all three evidence classes are present, qualifying, and later covered by explicit accountable review decisions

## Minimum honesty rules

- do not reuse executor telemetry as live field telemetry
- do not reuse partner-sample or deployment-intake replay as live field telemetry
- do not reconstruct trace-back linkage manually if the deployment path did not emit it
- do not issue one approval record for both bridge pairs unless the decision text explicitly covers both pairs and both evidence classes
- do not drop blocked runs; blocked outcomes are part of the evidence

## Current package state

As of this snapshot, no qualifying live deployment evidence exists in the package.
This note is preparation only and does **not** count as promotion evidence.
