# OFARM live-field same-standard bridge evidence capture kit v0.1

Date: 2026-04-18  
Status: active supporting implementation artifact  
Scope: bounded pre-implementation capture kit for the remaining same-standard bridge promotion blockers

---

## Purpose

This wave performs the next repo-only move for same-standard bridge promotion readiness.
It adds the capture artifacts that future live deployments should fill, without changing RC2.1, without promoting any bridge surface beyond `DRAFT`, and without treating templates as evidence.

## Included artifacts

- `OFARM_live_field_same_standard_bridge_telemetry_capture_template_v0_1.json`
- `OFARM_live_field_same_standard_bridge_trace_back_records_capture_template_v0_1.json`
- `OFARM_same_standard_bridge_production_approval_record_capture_template_v0_1.json`
- `OFARM_live_field_same_standard_bridge_operator_note_v0_1.md`
- `ofarm_live_field_same_standard_bridge_capture_kit_runner_v0_1.py`
- `OFARM_live_field_same_standard_bridge_capture_kit_results_v0_1.json`
- `ofarm_live_field_same_standard_bridge_telemetry_intake_and_production_approval_runner_v0_2.py`

## What this does

- gives future deployments a stable intake shape for the three remaining promotion blockers
- makes pre-implementation preparation explicit instead of leaving future deployments to invent ad hoc evidence packets
- hardens the intake gate so template-shaped or self-declared non-qualifying artifacts do not look like real promotion evidence by filename alone

## What this does not do

- it does **not** create live field-collected telemetry
- it does **not** create deployment-produced trace-back linkage
- it does **not** create production approval
- it does **not** promote ADAPT or ISOXML beyond `DRAFT`

## Conversion rule

Keep the three capture files at their template filenames while the project remains pre-implementation.
Only copy a template to the production-pattern filename after a real deployment artifact exists.
When that happens:

1. copy the template to the correct production-pattern filename  
2. set `templateOnly` to `false`  
3. replace every placeholder  
4. preserve only real deployment refs, timestamps, and emitted artifact refs  
5. rerun the live-field intake / promotion runner  

## Qualification rule

For a later artifact to count toward promotion readiness, it must satisfy all of the following:

- **live field telemetry** — a real deployment run in a live field setting, not executor output, not partner-sample replay, not deployment-intake rehearsal
- **deployment-produced trace-back linkage** — emitted by the deployment path itself, not manually reconstructed after the fact
- **production approval** — accountable pair-specific decision with explicit approver, time, evidence refs, and any conditions

## Non-qualifying material

The following still do **not** qualify for promotion:

- executor-produced bridge telemetry
- anonymized partner deployment sample replay telemetry
- redacted deployment-intake telemetry
- supplemental-family round-trip proof
- replay-produced or adapter-produced trace-back records
- template files and repo-only dry runs

## Current package posture

The package now has the pre-implementation evidence capture kit.
The promotion gate still correctly holds both same-standard bridge pairs at `DRAFT` until actual deployment evidence exists.
