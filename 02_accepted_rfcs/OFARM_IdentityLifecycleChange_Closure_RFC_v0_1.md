# OFARM IdentityLifecycleChange Closure RFC v0.1

Date: 2026-04-19
Status: accepted post-charter RFC
Scope: close the active machine-contract seam for generic identity and lifecycle continuity decisions that already exist in RC2.1 law, the Identity and Lifecycle RFC, and the current-state materialization RFC

---

## 1. Problem statement

The active baseline and accepted RFC set already require OFARM to make explicit, explainable decisions about:
- revision versus new identity
- split and merge continuity
- replacement and successor relationships
- overlap treatment
- durable versus ephemeral zone treatment
- equipment, facility, storage-location, and container continuity
- current-state invalidation after identity/lifecycle change

That direction is correct.
It is still not fully machine-closed in the active contract set.

Today:
- `02_accepted_rfcs/OFARM_Identity_and_Lifecycle_RFC_v0_1.md` closes the semantic rules
- `04_implementation_and_conformance/implementation_notes/runtime_surface_and_capability/OFARM_Runtime_Identity_Lifecycle_Expansion_Fixtures_v0_1.md` and its runner/results prove bounded implementation coverage
- active contracts still only provide `LotLineageChange` as a specialized lineage object
- non-lot identity/lifecycle handling can still drift into local runtime logic

This RFC closes that seam with the smallest controlled patch.

---

## 2. Core stance

### 2.1 One generic continuity object, not a family explosion
This RFC does not create a separate contract for every governed family.
It creates one generic `IdentityLifecycleChange` object that can cover the first-priority families:
- field
- zone
- crop cycle
- equipment
- facility
- storage location
- container

Lot-specific lineage remains separately represented by `LotLineageChange`.

### 2.2 Generic closure does not replace lot-specific traceability law
`LotLineageChange` remains the stronger specialized contract for red-flag lot continuity and claim-basis boundaries.
`IdentityLifecycleChange` closes the broader non-lot lifecycle seam and may also be used for non-claim-basis lot continuity notes only where that does not weaken lot law.

### 2.3 Ephemeral no-mint decisions must also be explicit
A frequent failure mode is silently turning analytical overlays into governed identities.
The active contract layer must be able to record an explicit “no constitutional identity minted” outcome where the semantic rule requires it.

### 2.4 Materialization invalidation must be visible
Identity/lifecycle change is already an explicit invalidation trigger family in the current-state materialization RFC.
The active contract created here must be able to carry invalidation impact hints so current-state refusal or recomputation can point at a concrete lifecycle artifact.

### 2.5 Keep the contract minimal
This RFC closes the runtime seam with minimum governed fields only.
It does not standardize every future geometry diff, asset-maintenance payload, or agronomic detail schema.

---

## 3. New contract family created by this RFC

This RFC creates this active machine-contract family in `03_machine_contracts/`:
- `OFARM_IdentityLifecycleChange_schema_v0_1.json`

It is seeded by the already-shipped runtime support layer:
- `04_implementation_and_conformance/implementation_notes/runtime_surface_and_capability/OFARM_Runtime_Identity_Lifecycle_Expansion_Fixtures_v0_1.md`
- `04_implementation_and_conformance/implementation_notes/runtime_surface_and_capability/ofarm_runtime_identity_lifecycle_expansion_runner_v0_1.py`
- `04_implementation_and_conformance/implementation_notes/runtime_surface_and_capability/OFARM_runtime_identity_lifecycle_expansion_results_v0_1.json`

---

## 4. Contract minimums

A valid `IdentityLifecycleChange` contract must be able to carry at least:
- stable lifecycle-change identifier
- evaluated time and optional effective time
- governed family and optional subject class
- anchor scope
- generic change kind
- explicit continuity outcome
- identity continuity class
- predecessor and successor identity references
- lineage or overlap relations where relevant
- invalidation impacts for downstream current-state handling
- optional event, decision, and evidence references
- human-readable summary

---

## 5. First promoted example coverage

The package should promote starter examples that prove:
- field split with explicit child identities
- governed recurring zone revision
- ephemeral advisory mask that does not mint a constitutional zone
- crop-cycle replant successor
- equipment replacement
- facility revision
- storage-location replacement
- reusable-container occupancy continuity

These examples are intentionally narrow.
They prove the contract shape without reopening the full domain.

---

## 6. Compatibility rule

This RFC does not require:
- a new baseline-law rewrite
- a new geometry or topology contract
- current-state artifacts to embed the full lifecycle object inline
- authorization traces to embed lifecycle objects inline

It only requires that active package-local examples and downstream refusal/recompute artifacts may now point to a governed `IdentityLifecycleChange` object instead of leaving the continuity decision implicit or support-layer-only.

---

## 7. Out of scope

This RFC does not:
- replace `LotLineageChange`
- create a public editing API
- define merge math for every geometry case
- define a full physical-asset registry model
- standardize deployment telemetry or live sync orchestration

---

## 8. Outcome

After this RFC:
- non-lot identity/lifecycle continuity is no longer only prose plus support fixtures
- active machine contracts can represent revision, split, replacement, overlap, and no-mint outcomes
- current-state invalidation can point to a concrete lifecycle artifact
- the offline revocation + scope-drift break-test seam can compose against active lifecycle objects instead of support-only records
