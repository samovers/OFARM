# OFARM Evidence Sufficiency fixtures v0.1

Date: 2026-04-11  
Status: executable/conformance fixture note  
Scope: starter executable fixtures for Wave 4 evidence sufficiency and attestation closure

---

## Purpose

These fixtures make the evidence-sufficiency gate more executable by covering the smallest high-value cases:
- an allowed high-consequence compliance assertion
- an allowed attested dossier/document path
- an allowed submission/filing package path
- a review-routed dossier because support is only partially sufficient
- a refused compliance assertion because required evidence/provenance is missing

They do **not** claim full publication/runtime/signature closure.
They provide a stable starter set for expressing:
`Claim or output` ← `Argument/rule posture` ← `Evidence bundle + provenance`.

---

## Executable fixtures in this package

### Fixture 1 — compliance assertion allow
Expected:
- decision = `ALLOW`
- subject class = `ASSERTION_RECORD`
- at least one complete evidence bundle supports the claim
- attestation is not automatically enabled

### Fixture 2 — attested dossier allow
Expected:
- decision = `ALLOW`
- subject class = `DOSSIER_ASSEMBLY`
- retained `MaterializationBasis` and `MaterializationSnapshot` are present
- attestation remains explicit and authority-bound

### Fixture 3 — submission package allow
Expected:
- decision = `ALLOW`
- subject class = `SUBMISSION_ASSEMBLY`
- retained `MaterializationBasis` and `MaterializationSnapshot` are present
- filing action stays distinct from canonical truth

### Fixture 4 — review-required dossier
Expected:
- decision = `REQUIRE_REVIEW`
- bundle status is partial rather than complete
- automatic attestation is not allowed
- at least one insufficiency reason and blocking gap is preserved

### Fixture 5 — refusal because evidence is insufficient
Expected:
- decision = `REFUSE`
- required support is missing
- refusal is explained with insufficiency reason codes and blocking gaps
- the platform does not guess or auto-promote

---

## Executable evidence

Machine-contract examples live under:
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/evidence/OFARM_EvidenceSufficiencyCase_example_*.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/current_state/OFARM_MaterializationSnapshot_example_field_dossier_v0_1.json`
- existing `MaterializationBasis` and `MaterializationSnapshot` examples already in the package

Executable fixture payloads live under:
- `04_implementation_and_conformance/examples_and_fixtures/ofarm_evidence_sufficiency_fixtures_v0_1/`

Executable results are written to:
- `04_implementation_and_conformance/conformance_runners/evidence_sufficiency_conformance/OFARM_evidence_sufficiency_fixture_results_v0_1.json`
