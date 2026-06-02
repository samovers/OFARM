# pilot_intake_rehearsal — package map

Date: 2026-04-20
Status: active supporting implementation artifact
Scope: production-shaped but explicitly non-qualifying rehearsal packets for the first OFARM external evidence submission after the authenticity gate was added

---

## Purpose

This folder helps deployment teams inspect the expected artifact shape before sending a real packet.
It is **not** part of the canonical live-evidence intake lane.

## Hard boundary

- Do not treat files here as live deployment evidence.
- Do not move files from here into `../live_evidence_packets/` without creating a real deployment artifact.
- Do not claim that rehearsal files reduce the external-evidence debt.
- Rehearsal packets are expected to say `repositoryAuthored: true` in their authenticity envelope.

## Current rehearsal lanes

- `runtime_surface_release_lane/` — one production-shaped governed runtime-surface evidence rehearsal packet
- `partner_output_channels/` — one production-shaped partner-output telemetry rehearsal packet

## No same-standard bridge rehearsal

The same-standard bridge lane stays template-only until real live deployment artifacts exist for all required evidence classes.
