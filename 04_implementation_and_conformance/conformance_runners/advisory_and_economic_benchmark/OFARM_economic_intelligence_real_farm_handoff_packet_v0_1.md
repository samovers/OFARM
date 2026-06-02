# OFARM economic intelligence real-farm handoff packet v0.1

## Purpose

This packet is the **practical handoff set** for running one redacted farm through the bounded OFARM economics pilot.

It exists because there is still **no real farm dataset in the workspace**.
The correct next step is therefore not more architecture drafting; it is a clean intake/run path for one real farm.

## What to send

Send **one redacted JSON dataset** built from:
- `ofarm_economic_intelligence_real_farm_pilot_dataset_template_v0_1.json`

Use the redaction rules in:
- `OFARM_economic_intelligence_real_farm_pilot_redaction_and_sovereignty_note_v0_1.md`

## What will be run

1. `ofarm_economic_intelligence_real_farm_pilot_validator_v0_2.py`
2. `ofarm_economic_intelligence_real_farm_pilot_runner_v0_2.py`
3. or the combined wrapper `ofarm_economic_intelligence_real_farm_pilot_cli_v0_1.py`

## Output boundaries

- Lane A output = **screening only**, not profitability
- Lane B output = **relevant-cost + bottleneck screen**, not field profitability
- Lane C output = **pre-gate screening**, not appraisal, NPV, IRR, payback, DSCR, financing approval, or investment decision authority

## Required stop rule

If the farm asks for stronger claims than the data maturity supports, stop and ask for stronger evidence instead of widening semantics.
