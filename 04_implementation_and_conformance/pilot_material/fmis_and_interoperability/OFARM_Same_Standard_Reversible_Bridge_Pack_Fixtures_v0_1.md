# OFARM Same-Standard Reversible Bridge Pack Fixtures v0.1

Status: active supporting implementation artifact  
Scope: bounded conformance rehearsal for same-standard reversible bridge-pack pairs

---

## Goal

This wave closes the specific post-Wave-10 gap that remained explicit in the conformance matrix:
- same-standard reverse-pair eligibility
- declared-subset reversible bridge-pack round trips
- conflict cases where the bridge-pack claim must stop and disclose limitations

## What this wave does

This wave introduces draft bridge-pack machine-contract examples for ADAPT and ISOXML export and then tests them against the already-shipped import mapping posture.
The conformance runner produces:
- an updated same-standard reverse-pair scan
- candidate-pair records for draft reversible bridge packs
- declared-subset round-trip records
- conflict records for unsupported or high-consequence constructs

## What this wave does not do

This wave does **not**:
- promote bridge packs into baseline law
- claim deployment-collected same-standard runtime telemetry
- claim that every construct in ADAPT or ISOXML is lossless or reversible
- bypass OFARM authority, evidence, or current-state freshness rules

## Fixture families

- `SAME_STANDARD_DECLARED_SUBSET_ROUNDTRIP`
- `SAME_STANDARD_CONFLICT_CASE`

## Expected posture

A fixture may pass while still carrying limitations.
Passing in this wave means:
- the package declares a draft same-standard reverse pair
- the declared subset can be round-tripped with stated loss posture
- unsupported or high-consequence constructs are blocked and disclosed instead of silently flattened
