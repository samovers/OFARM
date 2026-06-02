# OFARM same-standard bridge promotion memo v0.4

Date: 2026-04-12  
Status: active supporting implementation artifact  
Scope: bounded decision memo for ADAPT and ISOXML same-standard bridge-pack draft promotion posture after supplemental-family reversible proof and explicit live-field evidence gating

---

## Decision

Keep both same-standard bridge-pack pairs at `DRAFT`.
Do **not** promote either ADAPT or ISOXML bridge export surface beyond draft on the evidence currently in the package.

## What improved in this wave

The package now also ships:
- reversible round-trip records for the currently supported ADAPT supplemental construct families
- reversible round-trip records for the currently supported ISOXML supplemental construct families
- blocked supplemental-family conflict records that keep the unsupported nested-vendor and timezone-ambiguous families outside reversible claims
- an explicit live-field evidence gate that checks for live field-collected same-standard bridge telemetry and records that none is present

This narrows the promotion blocker materially.

## What is now closed

The package no longer lacks reversible proof for the **supported supplemental construct families** under evaluation.
That part of the readiness gap is now closed inside the bounded draft bridge scope represented in the package.

## Why promotion is still denied

This wave still does **not** provide:
- live field-collected production same-standard bridge telemetry
- a production promotion approval path for either bridge surface
- evidence that either draft bridge surface should leave `DRAFT`

The new live-field evidence gate is intentionally conservative and currently reports missing evidence rather than trying to infer production-grade proof from executor, partner-sample, or redacted deployment-intake artifacts.

## Consequence

The package may now honestly claim:
- declared-subset same-standard bridge rehearsal exists
- executor-produced same-standard bridge evidence exists
- partner-variant sample replay coverage exists
- redacted deployment-intake same-standard bridge coverage exists
- reversible proof exists for the currently supported supplemental construct families
- blocked conflict families remain explicit and auditable

The package may **not** yet claim:
- live production-ready same-standard bridge surfaces
- live field-collected same-standard bridge telemetry
- draft-to-active promotion readiness

## Follow-on

The next bounded follow-on is real live-field telemetry intake plus production approval evidence.
Only after that should the package revisit whether either bridge surface deserves promotion beyond `DRAFT`.
