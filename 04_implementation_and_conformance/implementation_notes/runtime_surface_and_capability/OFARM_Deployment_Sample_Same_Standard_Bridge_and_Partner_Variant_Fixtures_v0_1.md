# OFARM deployment-sample same-standard bridge and partner-variant fixtures v0.1

Date: 2026-04-11  
Status: active supporting implementation artifact  
Scope: bounded partner-variant sample replay fixtures for the ADAPT and ISOXML same-standard draft bridge pairs

---

## Purpose

These fixtures extend the same-standard bridge work one step beyond the Wave 12 executor-only runs.

They do **not** claim live field-collected production telemetry.
They replay **package-local anonymized partner deployment samples** through the bounded bridge conformance runner so the package can test:

- partner-specific supported variants within the declared reversible subsets
- partner-specific blocked variants for known conflict families
- sample-level bridge telemetry emission and stop conditions
- explicit non-promotion posture even when supported partner samples succeed

## Included sample families

### ADAPT
- partner alpha core field/operation subset success
- partner beta supported unit-normalization subset success
- partner gamma blocked vendor-extension sample

### ISOXML
- partner alpha core task/partfield subset success
- partner beta supported device/product-reference subset success
- partner gamma blocked high-consequence timestamp sample

## Guardrail

These fixtures are **sample replays**, not live deployment telemetry.
They may strengthen partner-variant coverage claims for conformance rehearsal, but they do **not** remove the promotion blocker around missing live deployment-collected bridge telemetry.
