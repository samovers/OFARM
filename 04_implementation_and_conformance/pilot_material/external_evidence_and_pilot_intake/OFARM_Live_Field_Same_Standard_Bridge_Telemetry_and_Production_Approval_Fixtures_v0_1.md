# OFARM live-field telemetry intake and production approval fixtures v0.1

Date: 2026-04-12  
Status: active supporting implementation artifact  
Scope: bounded Wave 16 fixtures for explicit live-field telemetry intake, deployment-produced trace-back linkage intake, and production approval scanning for same-standard bridge draft pairs

---

## Purpose

This wave does **not** fabricate live field evidence.
It makes the remaining promotion blockers explicit and machine-auditable.

## Search classes

The runner scans the package-local `04_implementation_and_conformance/` scope for three evidence classes:

1. live field-collected same-standard bridge telemetry
2. deployment-produced live-field trace-back linkage
3. production promotion approval records

## Search patterns

- `OFARM_live_field_same_standard_bridge_telemetry_v*.json`
- `OFARM_live_field_same_standard_bridge_trace_back_records_v*.json`
- `OFARM_same_standard_bridge_production_approval_record_v*.json`

## Guardrail

The following do **not** count toward these evidence classes:
- executor-produced same-standard bridge telemetry
- anonymized partner deployment sample replay telemetry
- redacted deployment-intake telemetry
- supplemental-family reversible round-trip proof
- replay-produced or adapter-produced trace-back records

## Expected posture in the current package

The expected result for the current package is:
- zero qualifying live field telemetry artifacts
- zero qualifying deployment-produced trace-back linkage artifacts
- zero qualifying production approval records
- both ADAPT and ISOXML bridge pairs remain at `DRAFT`
