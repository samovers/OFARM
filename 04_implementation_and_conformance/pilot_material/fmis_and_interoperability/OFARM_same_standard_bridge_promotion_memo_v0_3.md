# OFARM same-standard bridge promotion memo v0.3

Date: 2026-04-12  
Status: active supporting implementation artifact  
Scope: bounded decision memo for ADAPT and ISOXML same-standard bridge-pack draft promotion posture after redacted deployment-intake and broader construct-family coverage work

---

## Decision

Keep both same-standard bridge-pack pairs at `DRAFT`.
Do **not** promote either ADAPT or ISOXML bridge export surface beyond draft on the evidence currently in the package.

## What improved in this wave

The package now goes beyond Wave 13 partner-variant sample replay.

It now also ships:
- package-local redacted deployment-intake telemetry for ADAPT and ISOXML same-standard draft bridge pairs
- broader construct-family sample coverage records for each draft pair
- supported supplemental construct-family intake paths for both standards
- blocked supplemental construct-family intake paths for unsupported vendor-private or high-consequence ambiguous cases

This is a real strengthening of bridge readiness evidence.

## Why promotion is still denied

This wave still does **not** provide:
- live field-collected production same-standard bridge telemetry
- full reversible round-trip proof for the supplemental construct families introduced in this wave
- evidence that draft bridge surfaces should leave `DRAFT`
- an explicit production promotion approval path for either bridge surface

The new intake evidence is still bounded package-local sample evidence.
It is useful for conformance hardening and readiness review, but it is not the same thing as live production-grade bridge evidence.

## Consequence

The package may now honestly claim:
- declared-subset same-standard bridge rehearsal exists
- executor-produced same-standard bridge evidence exists
- partner-variant sample replay coverage exists for ADAPT and ISOXML draft pairs
- redacted deployment-intake same-standard bridge coverage exists for broader construct families
- blocked conflict families remain explicit and auditable

The package may **not** yet claim:
- live production-ready same-standard bridge surfaces
- full reversible transport semantics for the broader construct families added in this wave
- draft-to-active promotion readiness

## Follow-on

The next bounded follow-on is live field-collected bridge telemetry plus fuller reversible proof across the broader construct families now under evaluation.
Only after that should the package revisit whether either bridge surface deserves promotion beyond `DRAFT`.
