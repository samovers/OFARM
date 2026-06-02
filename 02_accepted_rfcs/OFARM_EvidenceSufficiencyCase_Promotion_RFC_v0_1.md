# OFARM EvidenceSufficiencyCase Promotion RFC v0.1

Date: 2026-04-18  
Status: accepted post-charter RFC  
Scope: promote the degraded-evidence and late-evidence extension from controlled draft into an active current machine-contract family aligned to the evidence sufficiency policy and the promotion-handling note

---

## 1. Problem statement

The package already contains:
- an active evidence sufficiency and attestation policy
- an active evidence-quality and promotion-handling note
- a controlled `OFARM_EvidenceSufficiencyCase_schema_v0_2_draft.json`
- five draft examples covering the mandatory degraded-evidence and late-evidence fixture families

That is useful.
It is still not fully closed.

Today:
- `v0.2-draft` is not the default target for new degraded-evidence or late-evidence work
- the bundle-axis vocabulary in the draft is narrower and less exact than the companion note vocabulary
- several of the newly introduced insufficiency reason codes are not yet exercised in active examples

This RFC closes that seam with the smallest controlled patch.

---

## 2. Core stance

### 2.1 Promote, do not redesign
This RFC does not create a new assurance ontology and does not reopen constitutional truth law.
It promotes the already accepted narrow extension posture into an active current contract family.

### 2.2 Optional degraded-evidence axes remain optional
The five bundle-level evidence-quality axes remain optional.
They exist to make weak, partial, late, and contradictory evidence explicit when those conditions matter.
They do not become a universal required scoring grid.

### 2.3 The companion note vocabulary becomes canonical for v0.2
The active `v0.2` contract must align its bundle-axis value vocabulary to the active companion note:
- `sourceSpecificity`
- `captureIntegrity`
- `chronologyIntegrity`
- `crossSourceAgreement`
- `lateArrivalPosture`

This RFC therefore supersedes the narrower interim value set used in `v0.2-draft`.

### 2.4 v0.1 remains valid for narrow compatibility
`OFARM_EvidenceSufficiencyCase_schema_v0_1.json` remains valid as the minimal compatibility baseline.
It is not removed.
It simply stops being the preferred target when degraded-evidence or late-evidence posture must be expressed explicitly.

### 2.5 No scoring engine
Nothing in this RFC legalizes a global confidence score or silent weighted promotion logic.
Outcome remains governed through explicit allow/review/refuse posture.

---

## 3. New active current contract family created by this RFC

This RFC creates:
- `03_machine_contracts/schemas/evidence/OFARM_EvidenceSufficiencyCase_schema_v0_2.json`

It also promotes package-local `v0.2` examples that exercise:
- the five mandatory fixture families named by the active companion note
- the full added insufficiency-reason-code set needed for degraded/late evidence stability in this package

---

## 4. v0.2 contract minimums

`OFARM_EvidenceSufficiencyCase_schema_v0_2.json` must preserve all `v0.1` minimum structure and additionally support:
- the five optional bundle-level evidence-quality axes named in the active companion note
- the seven added insufficiency reason codes named in the active companion note
- current-state basis and retained-snapshot linkage for output and submission classes
- continued explicit allow/review/refuse posture without edit-in-place shortcuts

---

## 5. Currentness rule after this RFC

After this RFC:
- `OFARM_EvidenceSufficiencyCase_schema_v0_2.json` is the active default target for new degraded-evidence and late-evidence cases
- `OFARM_EvidenceSufficiencyCase_schema_v0_1.json` remains available for narrow compatibility or minimal deployments
- `OFARM_EvidenceSufficiencyCase_schema_v0_2_draft.json` is retained only as a superseded transition artifact and should not be used for new work

---

## 6. Conformance expectation

To treat this promotion as closed at package level, conformance must show at least:
- package-local validation of the promoted `v0.2` contract
- package-local examples for ambiguous identity, partial machine log plus manual top-up, late lab support, late evidence after frozen output, and late evidence after formal submission
- active examples that exercise all newly added insufficiency reason codes in the promoted vocabulary
- explicit proof that late evidence after frozen output or submission preserves prior output/submission lineage rather than rewriting history

---

## 7. Out of scope

This RFC does not:
- require full runtime-generated assurance graphs
- require a portable attestation credential ecosystem
- change constitutional promotion law
- turn live `PassportView` into an attested output family
- require every `EvidenceSufficiencyCase` to populate all optional bundle axes

---

## 8. Outcome

After this RFC:
- degraded-evidence and late-evidence posture can be expressed with the note-aligned vocabulary inside the active contract set
- the package no longer depends on a non-default draft for core farm-reality evidence cases
- the remaining bridge-promotion partiality stays external-evidence-bound rather than hiding another package-internal closure seam
