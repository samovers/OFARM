# partner_output_channels — evidence drop zone

Date: 2026-04-20
Status: active supporting implementation artifact
Scope: canonical location for future partner-output telemetry artifacts collected from real deployments

---

## Allowed future production filenames

- `OFARM_runtime_surface_partner_output_telemetry_v*.json`

## Current posture

These artifacts are implementation-support evidence.
They help trace deployment behavior and future promotion decisions.
They do not by themselves promote dashboard, CSV, PDF, dossier, or submission channels into governed runtime-surface law.

A future real artifact here must still carry an `authenticityEnvelope` and `qualificationClaim` and must not remain repo-authored rehearsal material.

## Required follow-up

After adding a real telemetry artifact here, run:
- `../../ofarm_external_evidence_intake_runner_v0_4.py`

If the artifact is structurally and authentically reviewable, place a matching accountable decision record under:
- `../../live_evidence_decisions/partner_output_channels/`

Then run:
- `../../ofarm_external_evidence_decision_runner_v0_2.py`
