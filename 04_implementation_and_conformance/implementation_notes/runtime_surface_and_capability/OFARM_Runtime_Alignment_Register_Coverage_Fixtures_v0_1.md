# OFARM Runtime Alignment Register Coverage Fixtures v0.1

Date: 2026-04-18  
Status: active supporting implementation artifact  
Scope: machine-checked coverage review for canonical concepts in the harmonized Alignment Register

---

## 1. Purpose

These fixtures turn Alignment Register coverage from an implicit reading exercise into an executable review.

The review checks each canonical concept in the harmonized register against the current OFARM workspace evidence set and records where that concept is evidenced across:

- baseline law
- companion artifacts
- accepted RFCs
- machine contracts
- implementation/conformance artifacts

---

## 2. Inputs

### Source register
- `00_active_baseline/OFARM_Alignment_Register_v0_13.md` from the current standalone package root

### Workspace evidence scan
The runner scans the current standalone package and uses only textual artifact families relevant to semantic evidence review.

Excluded from the search:
- the Alignment Register row being checked
- conformance coverage matrix self-references
- conformance seed-set self-references
- self-generated alignment coverage artifacts and hardening notes
- stale readiness snapshots that only restate the old gap list
- historical patch/output areas and reviewed-thread holdings

Those exclusions prevent circular or self-fulfilling coverage counts.

---

## 3. Strength classes

### `STRONG`
The concept is evidenced outside the register and has at least one hit in:
- RFC
- machine-contract
- or implementation/conformance artifacts

### `MODERATE`
The concept is evidenced outside the register, but only through:
- baseline
- or companion artifacts

### `REGISTER_ONLY`
No non-register workspace evidence was found.

---

## 4. Acceptance rule for this wave

This wave passes if:

- all register rows are parsed successfully
- the workspace scan completes
- per-concept coverage records are emitted
- explicit gap records are emitted for any `REGISTER_ONLY` rows
- no self-referential coverage bookkeeping artifacts are counted as evidence

This wave does **not** require every concept to reach `STRONG`.

---

## 5. Output artifacts

The runner emits:

- `OFARM_alignment_register_coverage_records_v0_1.json`
- `OFARM_alignment_register_gap_records_v0_1.json`
- `OFARM_alignment_register_coverage_summary_v0_1.json`
- `OFARM_alignment_register_coverage_results_v0_1.json`

---

## 6. Current outcome

This wave checked `91` canonical concepts and found:

- `91` `STRONG`
- `0` `MODERATE`
- `0` `REGISTER_ONLY`

The current rerun now also closes the previously moderate OFARM-owned seams:

- `DataSovereigntyBoundary`
- `NarrativeObservation`
- `LocalMemoryRule`
- `LocalArtifact`
- `PackCompatibilityDeclaration`
- `PackMergePolicy`
- `PackExclusionRule`

Together with the earlier closure of `Variety / cultivar`, `LocalConditionPattern`, and `PlannedIntervention`, the standalone coverage review now finds explicit non-register workspace evidence for every harmonized Alignment Register concept.