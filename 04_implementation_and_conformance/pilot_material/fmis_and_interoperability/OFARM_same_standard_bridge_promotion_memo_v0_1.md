# OFARM same-standard bridge promotion memo v0.1

Date: 2026-04-11  
Status: active supporting implementation artifact  
Scope: bounded decision memo for ADAPT and ISOXML same-standard bridge-pack draft promotion posture

---

## Decision

Keep both same-standard bridge-pack pairs at `DRAFT`.
Do **not** promote either ADAPT or ISOXML bridge export surface beyond draft on the evidence currently in the package.

## Why

Wave 12 strengthens the package in one important way: it now has executor-produced same-standard bridge telemetry for the declared ADAPT and ISOXML subsets, plus blocked telemetry for the known unsupported/high-consequence conflict families.
That is stronger than the Wave 11 declared-subset rehearsal alone.

It is still not enough for promotion.
The package does **not** yet provide:
- deployment-collected same-standard telemetry
- partner-variant coverage
- broad construct coverage beyond the declared reversible subset
- an explicit production promotion approval path for either bridge surface

## Consequence

The package may now honestly claim:
- declared-subset same-standard bridge rehearsal exists
- executor-produced same-standard bridge evidence exists
- blocked conflict families are explicit and auditable

The package may **not** yet claim:
- production-ready same-standard bridge surfaces
- broad reversible transport semantics for ADAPT or ISOXML
- draft-to-active promotion readiness

## Follow-on

The next bounded follow-on is deployment-grade same-standard bridge telemetry plus partner-variant and broader construct-family coverage.
Only after that should the package revisit whether either bridge surface deserves promotion beyond `DRAFT`.
