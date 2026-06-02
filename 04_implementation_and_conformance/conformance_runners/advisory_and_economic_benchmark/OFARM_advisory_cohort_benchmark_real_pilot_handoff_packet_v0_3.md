# OFARM advisory cohort benchmark real-pilot handoff packet v0.3

## Purpose

This packet is the practical handoff set for running one bounded redacted tenant cohort through the OFARM advisory cohort benchmark pilot.

It exists because there is still **no real tenant dataset in the workspace**.
The correct next step is therefore not more architecture drafting; it is a clean intake/run path for one real redacted pilot.

## What to send

Send **one redacted JSON dataset** built from:
- `ofarm_advisory_cohort_benchmark_real_pilot_spike_v0_3/fixtures/OFARM_advisory_cohort_benchmark_real_pilot_dataset_template_v0_3.json`

Apply the redaction rules in:
- `OFARM_advisory_cohort_benchmark_real_pilot_redaction_and_sovereignty_note_v0_3.md`

## What will be run

1. `ofarm_advisory_cohort_benchmark_real_pilot_validator_v0_3.py`
2. `ofarm_advisory_cohort_benchmark_real_pilot_runner_v0_3.py`

## Output boundaries

- output remains **Advisory-only**
- output remains **benchmarking only**
- no raw peer rows
- no raw evidence
- no exact contributor count
- no peer total spend
- no spend-per-hectare or ledger-style claims
- no promotion to Compliance truth

## Required stop rule

If the pilot asks for stronger claims than the benchmark seam supports, stop and ask for stronger evidence or narrower scope instead of widening semantics.
