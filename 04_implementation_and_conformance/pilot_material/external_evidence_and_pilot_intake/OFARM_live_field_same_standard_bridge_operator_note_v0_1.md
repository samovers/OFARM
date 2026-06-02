# OFARM live-field same-standard bridge operator note v0.1

Date: 2026-04-18  
Status: active supporting implementation artifact  
Scope: operator-facing steps for filling the same-standard bridge capture kit once live deployments exist

---

## Use this when

Use this note only when a real live deployment exists for one of the same-standard bridge draft pairs.
Until then, keep the capture files at their template filenames and do not rename them into the promotion-scan patterns.

## Target production filenames

When real evidence exists, copy the templates into these filename families:

- `OFARM_live_field_same_standard_bridge_telemetry_v0_1.json`
- `OFARM_live_field_same_standard_bridge_trace_back_records_v0_1.json`
- `OFARM_same_standard_bridge_production_approval_record_v0_1.json`

Later minor versions may use the same filename family with a higher `v*` suffix.

## Fill order

1. Fill the live-field telemetry file first.  
2. Fill the deployment-produced trace-back file second.  
3. Fill the production approval file last.  
4. Run `ofarm_live_field_same_standard_bridge_capture_kit_runner_v0_1.py` to check the kit shape.  
5. Run `ofarm_live_field_same_standard_bridge_telemetry_intake_and_production_approval_runner_v0_2.py` to re-evaluate the promotion gate.  

## Minimum honesty rules

- do not reuse executor telemetry as live field telemetry
- do not reuse partner-sample or deployment-intake replay as live field telemetry
- do not reconstruct trace-back linkage manually if the deployment path did not emit it
- do not issue one approval record for both bridge pairs unless the decision text explicitly covers both pairs and both evidence classes
- do not drop blocked runs; blocked outcomes are part of the evidence

## Stop rules

Stop and keep the pair at `DRAFT` if any of the following remains true:

- live field telemetry is still missing
- trace-back linkage was not emitted by the deployment path
- approval is missing, ambiguous, or undated
- placeholders remain in the copied production files
- one pair is being inferred from evidence that belongs to the other pair

## Current package state

As of this snapshot, no qualifying live deployment evidence exists in the package.
This note is preparation only and does **not** count as promotion evidence.
