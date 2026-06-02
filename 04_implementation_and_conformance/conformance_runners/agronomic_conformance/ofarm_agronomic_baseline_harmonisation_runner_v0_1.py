#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "04_implementation_and_conformance" / "OFARM_agronomic_baseline_harmonisation_results_v0_1.json"
RECORDS = ROOT / "04_implementation_and_conformance" / "OFARM_agronomic_baseline_harmonisation_records_v0_1.json"
FIXTURES = ROOT / "04_implementation_and_conformance" / "OFARM_Agronomic_Baseline_Harmonisation_Fixtures_v0_1.md"

CONSTITUTION = ROOT / "00_active_baseline" / "OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md"
PLATFORM = ROOT / "00_active_baseline" / "OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md"
ALIGNMENT = ROOT / "00_active_baseline" / "OFARM_Alignment_Register_v0_13.md"
READINESS = ROOT / "00_active_baseline" / "OFARM_post_gap_closure_readiness_gate_memo_v0_1.md"
HOSTILE = ROOT / "00_active_baseline" / "OFARM_final_hostile_review_after_gap_closure_v0_1.md"

REQUIRED_TERMS = [
    "AgronomicObservationContext",
    "MeasurementEvidence",
    "InterventionIntentPayload",
    "ExecutionRecordPayload",
    "PartialExtent",
    "AgronomicIdentityBinding",
    "AgronomicCodeBindingProfile",
    "AgronomicReconstructionPolicy",
    "AgronomicReconstructionTrace",
]

REQUIRED_RFC_REFS = [
    "OFARM Agronomic Observation and Measurement Context RFC v0.1",
    "OFARM Quantity-Bearing Intervention and As-Applied RFC v0.1",
    "OFARM Partial Extent and Geometry Basis RFC v0.1",
    "OFARM Agronomic Code Binding and Standards Profile RFC v0.1",
    "OFARM Agronomic Query and Output Reconstruction RFC v0.1",
]

PRESERVATION_TOKENS = [
    "not alternate stores of truth",
    "external standards and registries remain anchors",
    "does not by itself create accepted observation state",
    "does not make truth stronger by existing",
    "does not by itself create a Field",
    "PassportView defaults to accepted consequences",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> int:
    constitution = read(CONSTITUTION)
    platform = read(PLATFORM)
    alignment = read(ALIGNMENT)
    readiness = read(READINESS)
    hostile = read(HOSTILE)
    records = json.loads(RECORDS.read_text(encoding="utf-8"))
    fixtures = read(FIXTURES)

    checks: dict[str, bool] = {}
    checks["constitution_has_phase_marker"] = "AGR-P7 agronomic carrier harmonization" in constitution
    checks["platform_has_phase_marker"] = "AGR-P7 agronomic carrier harmonization" in platform
    checks["alignment_has_phase_marker"] = "AGR-P7 agronomic carrier" in alignment
    checks["crop_only_boundary_present"] = "Crop-only release boundary" in constitution and "Livestock-specific" in constitution
    checks["constitution_mentions_all_terms"] = all(term in constitution for term in REQUIRED_TERMS)
    checks["platform_mentions_all_terms"] = all(term in platform for term in REQUIRED_TERMS)
    checks["alignment_registers_all_terms"] = all(f"| {term} |" in alignment for term in REQUIRED_TERMS)
    checks["constitution_lists_agronomic_rfcs"] = all(ref in constitution for ref in REQUIRED_RFC_REFS)
    checks["preservation_rules_present"] = all(token.lower() in constitution.lower() for token in PRESERVATION_TOKENS)
    checks["readiness_addendum_present"] = "AGR-P7 agronomic baseline-harmonisation addendum" in readiness
    checks["hostile_addendum_present"] = "AGR-P7 agronomic hostile-review addendum" in hostile
    checks["baseline_no_external_truth_import"] = "do not import external standards" in readiness.lower() or "external standards" in constitution.lower() and "do not become hidden ofarm law" in constitution.lower()
    checks["records_expected_status_pass"] = records.get("expectedOverallStatus") == "PASS"
    checks["records_list_all_terms"] = all(term in records.get("reflectedCarrierConcepts", []) for term in REQUIRED_TERMS)
    checks["records_list_all_rfcs"] = all(any(ref.replace("OFARM ", "OFARM_").replace(" ", "_").replace("-", "_").split("_RFC")[0] in path for path in records.get("reflectedAcceptedRfcs", [])) or ref in constitution for ref in REQUIRED_RFC_REFS)
    checks["fixtures_describe_non_goals"] = "external-standard readiness" in fixtures and "production runtime execution" in fixtures

    results = {
        "schemaVersion": "ofarm.agronomicBaselineHarmonisationResults.v0.1",
        "date": "2026-05-13",
        "phase": "AGR-P7",
        "overallStatus": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "coverageAdvances": [
            "active baseline now reflects accepted agronomic carrier closures",
            "crop-only release boundary is explicit",
            "new agronomic carrier concepts are alignment-registered",
            "readiness and hostile-review posture are updated without claiming external standard readiness",
        ],
        "preservedBoundaries": [
            "assertion/history-first truth",
            "governed current-state materialization",
            "advisory versus compliance separation",
            "pack non-mutation of core meaning",
            "external standards as anchors/bindings/exchange surfaces rather than OFARM truth",
            "PassportView versus DocumentAssembly separation",
        ],
        "limitations": [
            "AGR-P7 is baseline harmonisation only; it does not provide production runtime execution evidence.",
            "Wire-level standard mappings, live registry verification, and jurisdiction/crop-specific packs remain future implementation/conformance work.",
        ],
    }
    OUT.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(results["overallStatus"])
    return 0 if results["overallStatus"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
