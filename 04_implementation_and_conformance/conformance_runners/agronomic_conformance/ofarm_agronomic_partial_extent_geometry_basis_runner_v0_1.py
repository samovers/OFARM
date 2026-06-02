#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

try:
    import jsonschema
except ImportError as e:  # pragma: no cover
    raise SystemExit("jsonschema is required for this validator") from e

ROOT = Path(__file__).resolve().parents[1]
IMPL = ROOT / "04_implementation_and_conformance"
RECORDS = IMPL / "OFARM_agronomic_partial_extent_geometry_basis_records_v0_1.json"
OUT = IMPL / "OFARM_agronomic_partial_extent_geometry_basis_results_v0_1.json"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def rel_exists(path: str) -> bool:
    return (ROOT / path).exists()


def validate_json(schema_path: str, example_path: str) -> dict[str, Any]:
    schema = load_json(ROOT / schema_path)
    data = load_json(ROOT / example_path)
    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.validate(data, schema)
    return {"schemaPath": schema_path, "examplePath": example_path, "status": "PASS"}


def expect_invalid(case: str, schema_path: str, example_path: str, mutate) -> dict[str, Any]:
    schema = load_json(ROOT / schema_path)
    data = load_json(ROOT / example_path)
    mutated = copy.deepcopy(data)
    mutate(mutated)
    try:
        jsonschema.validate(mutated, schema)
        return {"case": case, "status": "FAIL", "detail": "mutated example validated unexpectedly"}
    except Exception as exc:
        return {"case": case, "status": "PASS", "detail": str(exc).splitlines()[0]}


def main() -> int:
    records = load_json(RECORDS)
    results: dict[str, Any] = {
        "schemaVersion": "ofarm.agronomicPartialExtentGeometryBasisResults.v0.1",
        "date": "2026-05-13",
        "recordSetId": records.get("recordSetId"),
        "artifactExistence": [],
        "schemaExampleValidation": [],
        "negativeChecks": [],
        "behaviorChecks": [],
        "overallStatus": "PASS",
    }

    for family in records.get("contractFamilies", []):
        schema_path = family["schemaPath"]
        exists = rel_exists(schema_path)
        results["artifactExistence"].append({"path": schema_path, "exists": exists})
        if not exists:
            results["overallStatus"] = "FAIL"
        for example_path in family.get("requiredExamplePaths", []):
            exists = rel_exists(example_path)
            results["artifactExistence"].append({"path": example_path, "exists": exists})
            if not exists:
                results["overallStatus"] = "FAIL"
                continue
            try:
                results["schemaExampleValidation"].append(validate_json(schema_path, example_path))
            except Exception as exc:
                results["schemaExampleValidation"].append({"schemaPath": schema_path, "examplePath": example_path, "status": "FAIL", "detail": str(exc)})
                results["overallStatus"] = "FAIL"

    for bridge in records.get("bridgeExamples", []):
        for p in [bridge["schemaPath"], bridge["examplePath"]]:
            results["artifactExistence"].append({"path": p, "exists": rel_exists(p)})
            if not rel_exists(p):
                results["overallStatus"] = "FAIL"
        try:
            results["schemaExampleValidation"].append(validate_json(bridge["schemaPath"], bridge["examplePath"]))
        except Exception as exc:
            results["schemaExampleValidation"].append({"schemaPath": bridge["schemaPath"], "examplePath": bridge["examplePath"], "status": "FAIL", "detail": str(exc)})
            results["overallStatus"] = "FAIL"

    schema_path = "03_machine_contracts/schemas/agronomic/OFARM_PartialExtent_schema_v0_1.json"
    results["negativeChecks"].append(expect_invalid(
        "geometry_basis_requires_crs",
        schema_path,
        "04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agronomic/OFARM_PartialExtent_example_field_17_failed_pass_machine_logged_v0_1.json",
        lambda d: d["geometryBasis"].pop("coordinateReferenceSystem", None),
    ))
    results["negativeChecks"].append(expect_invalid(
        "quality_statement_required",
        schema_path,
        "04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agronomic/OFARM_PartialExtent_example_field_17_spot_spray_treatment_area_v0_1.json",
        lambda d: d.pop("qualityStatement", None),
    ))
    results["negativeChecks"].append(expect_invalid(
        "durable_identity_true_requires_ref",
        schema_path,
        "04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agronomic/OFARM_PartialExtent_example_field_17_west_zone_replant_area_v0_1.json",
        lambda d: (d["durableIdentityPolicy"].update({"createsDurableIdentity": True, "durableIdentityDecision": "CREATES_OR_REVISES_DURABLE_SCOPE"}), d["durableIdentityPolicy"].pop("durableIdentityRef", None)),
    ))
    if any(c.get("status") != "PASS" for c in results["negativeChecks"]):
        results["overallStatus"] = "FAIL"

    observed = load_json(ROOT / "04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agronomic/OFARM_PartialExtent_example_field_17_west_edge_weed_patch_observed_v0_1.json")
    treat = load_json(ROOT / "04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agronomic/OFARM_PartialExtent_example_field_17_spot_spray_treatment_area_v0_1.json")
    failed = load_json(ROOT / "04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agronomic/OFARM_PartialExtent_example_field_17_failed_pass_machine_logged_v0_1.json")
    accepted = load_json(ROOT / "04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agronomic/OFARM_PartialExtent_example_field_17_accepted_treated_slice_v0_1.json")
    dispute = load_json(ROOT / "04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agronomic/OFARM_PartialExtent_example_field_17_operator_sketch_disputed_geometry_v0_1.json")
    replant = load_json(ROOT / "04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agronomic/OFARM_PartialExtent_example_field_17_west_zone_replant_area_v0_1.json")
    intent_bridge = load_json(ROOT / "04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agronomic/OFARM_InterventionIntentPayload_example_field_17_spot_spray_prescription_with_partial_extent_v0_1.json")
    failed_bridge = load_json(ROOT / "04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agronomic/OFARM_ExecutionRecordPayload_example_field_17_failed_pass_with_partial_extent_v0_1.json")
    accepted_bridge = load_json(ROOT / "04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agronomic/OFARM_ExecutionRecordPayload_example_field_17_partial_accepted_execution_with_partial_extent_v0_1.json")
    idlife = load_json(ROOT / "04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/identity_lifecycle/OFARM_IdentityLifecycleChange_example_field_17_partial_replant_with_partial_extent_v0_1.json")
    mat = load_json(ROOT / "04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/current_state/OFARM_MaterializationResult_example_field_17_partial_replant_whole_field_stale_v0_1.json")

    behavior = [
        ("observed_patch_not_whole_field_truth", observed["extentRole"] == "OBSERVED_PATCH" and "WHOLE_FIELD_TRUTH" in observed["promotionBoundary"]["mustNotPromoteTo"] and observed["durableIdentityPolicy"]["createsDurableIdentity"] is False),
        ("treatment_area_intent_not_execution", treat["extentRole"] == "TREATMENT_AREA" and treat["extentState"] == "REVIEW_REQUIRED" and "ACCEPTED_EXECUTION" in treat["promotionBoundary"]["mustNotPromoteTo"]),
        ("failed_pass_evidence_only", failed["extentRole"] == "FAILED_PASS" and failed["promotionBoundary"]["highConsequenceUse"] == "EVIDENCE_ONLY" and failed["durableIdentityPolicy"]["durableIdentityDecision"] == "EVENT_BOUND_ONLY"),
        ("accepted_treated_slice_limited", accepted["extentRole"] == "TREATMENT_AREA" and accepted["promotionBoundary"]["mayDriveMaterialization"] is True and "WHOLE_FIELD_TRUTH" in accepted["promotionBoundary"]["mustNotPromoteTo"]),
        ("disputed_geometry_parallel", dispute["extentRole"] == "DISPUTED_GEOMETRY" and dispute["extentState"] == "DISPUTED" and dispute["promotionBoundary"]["highConsequenceUse"] == "DISPUTE_ONLY"),
        ("partial_replant_event_bound_geometry", replant["extentRole"] == "REPLANT_AREA" and replant["durableIdentityPolicy"]["createsDurableIdentity"] is False and "identityLifecycleChangeRef" in replant["durableIdentityPolicy"]),
        ("intent_bridge_uses_partial_extent", intent_bridge["targetExtentRef"] == treat["partialExtentId"] and intent_bridge["intentClass"] == "PRESCRIPTION"),
        ("failed_execution_bridge_uses_partial_extent", failed_bridge["executionExtent"]["extentRef"] == failed["partialExtentId"] and failed_bridge["recordClass"] == "AS_APPLIED_EVIDENCE"),
        ("accepted_execution_bridge_uses_accepted_slice", accepted_bridge["executionExtent"]["extentRef"] == accepted["partialExtentId"] and accepted_bridge["recordClass"] == "ACCEPTED_EXECUTION_DETAIL"),
        ("identity_lifecycle_replant_lineage_preserved", idlife["changeKind"] == "REPLANT" and replant["partialExtentId"] in idlife["evidenceRefs"] and len(idlife["newIdentityRefs"]) == 1),
        ("materialization_refuses_stale_whole_field", mat["decisionOutcome"] == "REFUSE_USE" and mat["freshnessState"] == "INVALID" and "IDENTITY_LIFECYCLE" in mat["invalidationTriggerFamilies"] and any(ref.startswith("partial-extent:") for prob in mat.get("problems", []) for ref in prob.get("relatedRefs", []))),
    ]
    results["behaviorChecks"] = [{"check": name, "status": "PASS" if ok else "FAIL"} for name, ok in behavior]
    if any(b["status"] != "PASS" for b in results["behaviorChecks"]):
        results["overallStatus"] = "FAIL"

    results["coverageAdvances"] = [
        "adds active PartialExtent contract family with geometry-basis and quality statements",
        "bridges PartialExtent into observation, intent, execution, identity lifecycle, and materialization examples",
        "proves event-bound geometry does not become durable identity by default",
        "proves stale whole-field materialization is refused after partial replant mixed-state change",
        "keeps agronomic code binding, query/output reconstruction, and baseline harmonization as explicit future phases",
    ]
    OUT.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(results["overallStatus"])
    return 0 if results["overallStatus"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
