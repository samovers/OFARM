# OFARM external evidence rehearsal fixtures v0.2

Date: 2026-04-20
Status: active supporting implementation artifact
Scope: bounded non-qualifying rehearsal support for the first external evidence packet after the authenticity gate was added

Supersedes:
- `OFARM_External_Evidence_Rehearsal_Fixtures_v0_1.md`

---

## Purpose

This wave keeps the rehearsal lane outside the canonical live-evidence drop zones.
It still gives deployment teams one production-shaped runtime-surface packet and one production-shaped partner-output telemetry packet to inspect before sending real artifacts.
The new addition is explicit authorship and authenticity posture:
rehearsal packets now mark themselves repo-authored and non-qualifying so copied rehearsal files cannot pass as real pilot evidence by accident.

## Included artifacts

- `pilot_intake_rehearsal/README.md`
- `pilot_intake_rehearsal/runtime_surface_release_lane/OFARM_runtime_surface_live_deployment_evidence_rehearsal_v0_2.json`
- `pilot_intake_rehearsal/partner_output_channels/OFARM_runtime_surface_partner_output_telemetry_rehearsal_v0_2.json`
- `ofarm_external_evidence_rehearsal_runner_v0_3.py`
- `OFARM_external_evidence_rehearsal_results_v0_3.json`

## What this does

- removes first-packet ambiguity for runtime-surface and partner-output evidence shape
- proves that placeholders can be removed cleanly while remaining explicitly non-qualifying
- proves that rehearsal packets can mark themselves `repositoryAuthored: true` and `sourceRealityClass: REHEARSAL`
- keeps rehearsal material separated from the canonical live-evidence intake lane

## What this does not do

- it does **not** create live deployment evidence
- it does **not** increase the count of qualifying live-evidence artifacts
- it does **not** promote same-standard bridge pairs
- it does **not** justify moving rehearsal files into `live_evidence_packets/`

## Same-standard bridge boundary

There is intentionally no same-standard bridge rehearsal JSON in this lane.
That boundary is stricter because a fake live-field bridge packet would be too easy to confuse with promotion evidence.
