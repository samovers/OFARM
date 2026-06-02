# same_standard_bridge — evidence drop zone

Date: 2026-04-20
Status: active supporting implementation artifact
Scope: canonical location for future same-standard bridge promotion evidence once real deployments exist

---

## Allowed future production filenames

- `OFARM_live_field_same_standard_bridge_telemetry_v*.json`
- `OFARM_live_field_same_standard_bridge_trace_back_records_v*.json`
- `OFARM_same_standard_bridge_production_approval_record_v*.json`

## Required evidence classes

- `LIVE_FIELD_COLLECTED_SAME_STANDARD_BRIDGE_TELEMETRY`
- `DEPLOYMENT_PRODUCED_TRACE_BACK_LINKAGE`
- `PRODUCTION_PROMOTION_APPROVAL_RECORD`

## Current posture

Both candidate pairs remain `DRAFT` until real artifacts with those production filenames exist, carry explicit authenticity envelopes and qualification claims, and pass qualification checks.
Template files kept elsewhere in the package do not count as promotion evidence.

## Required follow-up

After adding real evidence artifacts here, run:
- `../../ofarm_external_evidence_intake_runner_v0_4.py`

If the artifact set is ready for reviewer inspection, place accountable decision records under:
- `../../live_evidence_decisions/same_standard_bridge/`

Then run:
- `../../ofarm_external_evidence_decision_runner_v0_2.py`
