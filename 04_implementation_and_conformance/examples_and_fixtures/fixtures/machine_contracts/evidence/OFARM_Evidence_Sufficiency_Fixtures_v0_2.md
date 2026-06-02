# OFARM Evidence Sufficiency fixtures v0.2

Date: 2026-04-18  
Status: executable/conformance fixture note  
Scope: promoted evidence-sufficiency fixture coverage after the degraded-evidence and late-evidence closure pass

---

## Purpose

These fixtures keep the original high-consequence allow/review/refuse starter set and add the farm-reality evidence cases that were previously carried only by the controlled `v0.2-draft` extension.

The promoted `v0.2` family now covers:
- ambiguous product/input identity
- partial machine log plus manual top-up
- late support before final decision
- late evidence after frozen output
- late evidence after formal submission
- timestamp incomplete / record-time-only posture
- source quality too weak for high-consequence use
- explicit human-versus-machine contradiction

The fixtures still do **not** claim:
- full runtime-generated assurance graphs
- executor-backed signature pipelines
- deployment-collected publication telemetry

---

## Promotion stance

`OFARM_EvidenceSufficiencyCase_schema_v0_2.json` is the active current contract for new degraded-evidence and late-evidence cases.
The v0.1 contract remains available for narrow compatibility.
The `v0.2-draft` contract remains only as a retained superseded transition artifact.

---

## Executable evidence in this package

Promoted machine-contract examples live under:
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/evidence/OFARM_EvidenceSufficiencyCase_example_*_v0_2.json`

The compatibility baseline examples remain under:
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/evidence/OFARM_EvidenceSufficiencyCase_example_*_v0_1.json`

Implementation-side fixtures and results live under:
- `04_implementation_and_conformance/examples_and_fixtures/ofarm_evidence_sufficiency_fixtures_v0_2/`
- `04_implementation_and_conformance/conformance_runners/evidence_sufficiency_conformance/OFARM_evidence_sufficiency_fixture_results_v0_2.json`
