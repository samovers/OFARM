# OFARM economic intelligence real-farm pilot runbook v0.1

## Purpose

Run the three bounded economics lanes against one **real farm** dataset without changing OFARM architecture again.

This runbook assumes the active posture already agreed:
- operations remain the authoritative substrate
- economics lives in Advisory-only scenario logic
- imported finance remains bounded extract input
- outputs remain screening / decision-support / dossier-prep only
- no ledger semantics, no AP/AR, no payroll, no tax, no shadow ERP

## Pilot scope

Run exactly three lanes:

1. **Lane A** — Scenario-1 crop/system ranking from operational/planning data only  
2. **Lane B** — Scenario-2 own-vs-contractor / bottleneck screen with partial finance extracts  
3. **Lane C** — Scenario-3 capex pre-gate screen with regular import extracts  

Do **not** expand to whole-farm finance, statutory reporting, or generalized profitability claims during the pilot.

## Inputs

Use `ofarm_economic_intelligence_real_farm_pilot_dataset_template_v0_1.json` as the required intake shape.

Fill it with:
- real operational basis refs
- redacted stable farm/field/facility refs
- bounded accounting-extract refs only where lanes B/C need them
- no personal identifiers not needed for the pilot
- no bank account numbers, tax identifiers, payroll line items, or unreduced invoice payloads

## Execution steps

1. Redact the farm dataset according to the sovereignty note.  
2. Fill the template and save as a new JSON file.  
3. Run the validator first.  
4. If a lane is `READY`, run the pilot runner.  
5. Review the markdown summary and JSON outputs.  
6. Keep the outputs in Advisory posture only.  
7. If a lane requires stronger claims than its maturity allows, stop and request more evidence instead of widening semantics.

## Command examples

```bash
python ofarm_economic_intelligence_real_farm_pilot_validator_v0_1.py ofarm_economic_intelligence_real_farm_pilot_dataset_realfarm_v0_1.json
python ofarm_economic_intelligence_real_farm_pilot_runner_v0_1.py ofarm_economic_intelligence_real_farm_pilot_dataset_realfarm_v0_1.json
```

## Stop rules

Stop the pilot immediately if any of these happens:
- a lane output starts claiming profit, NPV, IRR, DSCR, financing-readiness, or formal approval without the required data maturity
- the implementation starts storing a second economic current-state store
- imported finance starts behaving like ledger truth
- a second query model or hidden warehouse semantics appears
- fixed-cost allocation begins surfacing as field truth
- Advisory output is treated as Compliance truth without a human-governed bridge

## Expected honest outcomes

- Lane A should produce **screening-only** operational economics.
- Lane B should produce **relevant-cost + bottleneck** decision support.
- Lane C should produce a **pre-gate recommendation** such as `PROCEED_TO_FULL_APPRAISAL` or `HOLD_FOR_MORE_EVIDENCE`.

Anything stronger than that is a bug, not a success.
