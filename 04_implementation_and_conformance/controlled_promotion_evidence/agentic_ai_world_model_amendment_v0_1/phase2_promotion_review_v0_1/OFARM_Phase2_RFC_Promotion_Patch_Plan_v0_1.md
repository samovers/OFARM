# OFARM Phase 2 RFC Promotion Patch Plan v0.1

Status: supporting review plan; no active promotion applied

## Recommended first RFC batch

1. `OFARM_Application_Builder_Surface_RFC_v0_1.md`
2. `OFARM_Preflight_DryRun_and_Explain_Surface_RFC_v0_1.md`
3. `OFARM_RuntimeProblem_Reason_Code_Registry_RFC_v0_1.md`
4. `OFARM_Publication_and_Output_Assembly_Surface_RFC_v0_1.md`

## Recommended amber batch

- `OFARM_Offline_Capture_and_Delayed_Sync_RFC_v0_1.md`
- `OFARM_Identity_Resolution_and_Import_Deduplication_RFC_v0_1.md`

These should not be promoted until refusal, ambiguity, revocation, stale-context, idempotency, and candidate-only cases are tightened.

## Held RFC

- `OFARM_Calculation_Service_and_Quantity_Conversion_RFC_v0_1.md`

Reason: formula and numeric policy can become hidden agronomic law. It needs separate review and fixtures.

## Required edits before active RFC promotion

- Change `Status:` from draft to accepted only at promotion time.
- Add a relation section naming affected active baseline files and accepted RFCs.
- Add explicit no-hidden-truth and no-side-effect rules.
- Add negative cases and conformance expectations.
- Ensure operation names are stable enough for machine-contract references.
