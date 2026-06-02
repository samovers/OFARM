# OFARM same-standard bridge promotion memo v0.6

Date: 2026-04-18  
Status: active supporting implementation artifact  
Scope: bounded decision memo for ADAPT and ISOXML same-standard bridge-pack draft promotion posture after adding a pre-implementation deployment-evidence capture kit
Current in family: `OFARM_same_standard_bridge_promotion_memo_v0_6.md`

---

## Decision

Keep both same-standard bridge-pack pairs at `DRAFT`.
Do **not** promote either ADAPT or ISOXML bridge export surface beyond draft on the evidence currently in the package.

## What improved in this wave

The package now also ships a pre-implementation capture kit for the three remaining promotion blockers:

- a live-field telemetry capture template
- a deployment-produced trace-back capture template
- a production approval capture template
- an operator note explaining how those templates become real future evidence
- an updated intake runner that treats template-shaped or self-declared non-qualifying artifacts as non-evidence

This improves future deployment readiness without weakening the promotion standard.

## What did not change

This wave still does **not** provide:

- live field-collected production same-standard bridge telemetry
- deployment-produced live-field trace-back linkage for either bridge pair
- a production promotion approval record for either bridge surface
- evidence that either draft bridge surface should leave `DRAFT`

## Why promotion is still denied

Templates, operator notes, and repo-only dry runs are preparation artifacts.
They do **not** satisfy the three actual promotion blockers.

The promotion gate therefore still depends on real artifacts discovered under the live evidence filename families:

- `OFARM_live_field_same_standard_bridge_telemetry_v*.json`
- `OFARM_live_field_same_standard_bridge_trace_back_records_v*.json`
- `OFARM_same_standard_bridge_production_approval_record_v*.json`

## Consequence

The package may now honestly claim:

- bounded same-standard bridge proof remains strong inside the current draft scope
- reversible proof exists for the currently supported supplemental construct families
- the remaining promotion blockers are explicit at intake-gate level
- the package is now prepared to collect qualifying deployment evidence later without inventing ad hoc shapes
- template-shaped artifacts are explicitly excluded from counting as promotion evidence

The package may **not** yet claim:

- live production-ready same-standard bridge surfaces
- draft-to-active bridge promotion readiness
- production approval for either bridge surface

## Follow-on

When real deployments become available:

1. copy the three capture templates into the production-pattern filenames  
2. replace every placeholder with real deployment evidence  
3. rerun `ofarm_live_field_same_standard_bridge_telemetry_intake_and_production_approval_runner_v0_2.py`  
4. revisit promotion only for the pair or pairs that actually clear all three evidence classes  
