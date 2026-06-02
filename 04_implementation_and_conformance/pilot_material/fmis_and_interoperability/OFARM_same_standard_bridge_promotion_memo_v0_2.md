# OFARM same-standard bridge promotion memo v0.2

Date: 2026-04-11  
Status: active supporting implementation artifact  
Scope: bounded decision memo for ADAPT and ISOXML same-standard bridge-pack draft promotion posture after partner-variant sample replay

---

## Decision

Keep both same-standard bridge-pack pairs at `DRAFT`.
Do **not** promote either ADAPT or ISOXML bridge export surface beyond draft on the evidence currently in the package.

## What improved in this wave

The package now goes beyond Wave 12 executor-only bridge runs.

It now also ships:
- package-local anonymized partner deployment sample replay telemetry
- supported partner-variant sample success paths for ADAPT and ISOXML
- blocked partner-variant sample paths for the known vendor-extension and high-consequence timestamp conflict families
- explicit partner-variant coverage records tied back to the draft candidate pairs

This is a real strengthening of bridge evidence for the current declared subsets.

## Why promotion is still denied

This wave still does **not** provide:
- live field-collected production same-standard bridge telemetry
- broad construct-family coverage beyond the current declared reversible subsets
- evidence that draft bridge surfaces should leave `DRAFT`
- an explicit production promotion approval path for either bridge surface

The new partner-variant evidence is still bounded sample replay evidence.
It is useful for conformance hardening, but it is not the same thing as broad deployment-grade bridge evidence.

## Consequence

The package may now honestly claim:
- declared-subset same-standard bridge rehearsal exists
- executor-produced same-standard bridge evidence exists
- partner-variant sample replay coverage exists for ADAPT and ISOXML draft pairs
- blocked conflict families are explicit and auditable

The package may **not** yet claim:
- live production-ready same-standard bridge surfaces
- broad reversible transport semantics for ADAPT or ISOXML
- draft-to-active promotion readiness

## Follow-on

The next bounded follow-on is live deployment-collected same-standard bridge telemetry intake plus broader construct-family coverage.
Only after that should the package revisit whether either bridge surface deserves promotion beyond `DRAFT`.
