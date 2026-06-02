# OFARM wave 21 alignment-register coverage hardening memo v0.1

Date: 2026-04-12  
Status: active supporting implementation artifact  
Scope: bounded conformance-side closure of the previously unstarted alignment-register coverage row

---

## 1. Why this wave exists

The wave-20 conformance matrix still left one central semantic-governance seam untouched:

- `alignment-register coverage checks`

This wave closes that seam without reopening baseline law.

No baseline file, accepted RFC, companion artifact, or machine-contract substance was amended.
The work is entirely in `04_implementation_and_conformance/`.

---

## 2. What this wave does

This wave adds a machine-checked coverage review over the harmonized `OFARM_Alignment_Register_v0_13.md` and the current OFARM workspace evidence set.

The runner:

- uses the wave-6 harmonized Alignment Register as the source register
- scans active baseline, companion, RFC, machine-contract, and implementation/conformance files across the migrated full baseline plus later wave workspaces
- records per-concept evidence hits by layer:
  - `BASELINE`
  - `COMPANION`
  - `RFC`
  - `CONTRACT`
  - `CONFORMANCE`
- classifies each register concept as:
  - `STRONG`
  - `MODERATE`
  - `REGISTER_ONLY`
- emits explicit gap records instead of leaving low-evidence rows implicit

---

## 3. Result summary

Counts emitted by the runner:

- register concepts checked: `91`
- workspace files scanned: `143`
- strength counts:
  - `STRONG`: `69`
  - `MODERATE`: `19`
  - `REGISTER_ONLY`: `3`
- gap concepts: `3`

Register-only follow-on targets are:

- `Variety / cultivar` (PROFILE_EXTERNAL, Layer 1 / Knowledge)
- `LocalConditionPattern` (OFARM_ALIGNED, Layer 4)
- `PlannedIntervention` (OFARM_OWNED, Layer 2)

This means the package now has an explicit machine-checked answer to the question:
“Which Alignment Register concepts are evidenced across the current OFARM artifact set, and which still live only in the register itself?”

---

## 4. Why the matrix row can move to COVERED

The requirement row is not “every concept must already have a full machine-contract family.”
It is “the package must ship alignment-register coverage checks.”

After this wave, it does.

The package now ships:
- a runner
- per-concept coverage records
- explicit gap records
- an aggregate result object

That is enough to mark the row as `COVERED`, while still preserving honest follow-on work for the three register-only concepts.

---

## 5. What this wave does not claim

This wave does **not** claim that all Alignment Register concepts are equally mature.

Specifically, it does **not** claim that:
- all concepts have dedicated machine contracts
- all concepts have runtime telemetry
- all concepts have symmetrical conformance depth

It only claims that coverage is now machine-checked and no longer implicit.

---

## 6. Most likely next bounded step

The next untouched central conformance seam is still:

- `graph-pattern equivalence tests`

That remains the cleanest next bounded closure after this wave.
