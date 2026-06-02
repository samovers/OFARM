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
RECORDS = IMPL / "OFARM_agronomic_observation_measurement_context_records_v0_1.json"
OUT = IMPL / "OFARM_agronomic_observation_measurement_context_results_v0_1.json"


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


def negative_numeric_unit_check(schema_path: str, example_path: str) -> dict[str, Any]:
    schema = load_json(ROOT / schema_path)
    data = load_json(ROOT / example_path)
    mutated = copy.deepcopy(data)
    mutated.get("result", {}).pop("unitRef", None)
    try:
        jsonschema.validate(mutated, schema)
        return {"case": "numeric_result_requires_unit", "status": "FAIL", "detail": "mutated numeric result validated without unitRef"}
    except Exception as exc:
        return {"case": "numeric_result_requires_unit", "status": "PASS", "detail": str(exc).splitlines()[0]}


def negative_required_id_check(schema_path: str, example_path: str, id_field: str) -> dict[str, Any]:
    schema = load_json(ROOT / schema_path)
    data = load_json(ROOT / example_path)
    mutated = copy.deepcopy(data)
    mutated.pop(id_field, None)
    try:
        jsonschema.validate(mutated, schema)
        return {"case": f"{id_field}_required", "status": "FAIL", "detail": f"mutated example validated without {id_field}"}
    except Exception as exc:
        return {"case": f"{id_field}_required", "status": "PASS", "detail": str(exc).splitlines()[0]}


def main() -> int:
    records = load_json(RECORDS)
    results: dict[str, Any] = {
        "schemaVersion": "ofarm.agronomicObservationMeasurementContextResults.v0.1",
        "date": "2026-05-12",
        "recordSetId": records.get("recordSetId"),
        "artifactExistence": [],
        "schemaExampleValidation": [],
        "negativeChecks": [],
        "behaviorChecks": [],
        "overallStatus": "PASS"
    }

    # Artifact existence and schema/example validation.
    for family in records.get("contractFamilies", []):
        schema_path = family["schemaPath"]
        results["artifactExistence"].append({"path": schema_path, "exists": rel_exists(schema_path)})
        if not rel_exists(schema_path):
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

    # Evidence sufficiency bridge examples validate against existing v0.2.
    suff_schema = "03_machine_contracts/schemas/evidence/OFARM_EvidenceSufficiencyCase_schema_v0_2.json"
    for example_path in records.get("evidenceSufficiencyBridgeExamples", []):
        results["artifactExistence"].append({"path": example_path, "exists": rel_exists(example_path)})
        try:
            results["schemaExampleValidation"].append(validate_json(suff_schema, example_path))
        except Exception as exc:
            results["schemaExampleValidation"].append({"schemaPath": suff_schema, "examplePath": example_path, "status": "FAIL", "detail": str(exc)})
            results["overallStatus"] = "FAIL"

    # Negative checks.
    results["negativeChecks"].append(negative_required_id_check(
        "03_machine_contracts/schemas/agronomic/OFARM_AgronomicObservationContext_schema_v0_1.json",
        "04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agronomic/OFARM_AgronomicObservationContext_example_field_17_weed_patch_scouting_v0_1.json",
        "agronomicObservationContextId"
    ))
    results["negativeChecks"].append(negative_required_id_check(
        "03_machine_contracts/schemas/evidence/OFARM_MeasurementEvidence_schema_v0_1.json",
        "04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agronomic/OFARM_MeasurementEvidence_example_soil_nitrate_below_loq_lab_result_v0_1.json",
        "measurementEvidenceId"
    ))
    results["negativeChecks"].append(negative_numeric_unit_check(
        "03_machine_contracts/schemas/evidence/OFARM_MeasurementEvidence_schema_v0_1.json",
        "04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/evidence/OFARM_MeasurementEvidence_example_leaf_wetness_sensor_calibrated_v0_1.json"
    ))
    if any(c.get("status") != "PASS" for c in results["negativeChecks"]):
        results["overallStatus"] = "FAIL"

    # Behavior checks on examples.
    obs_examples = [load_json(ROOT / p) for f in records["contractFamilies"] if f["contractFamily"] == "AgronomicObservationContext" for p in f["requiredExamplePaths"]]
    meas_examples = [load_json(ROOT / p) for f in records["contractFamilies"] if f["contractFamily"] == "MeasurementEvidence" for p in f["requiredExamplePaths"]]

    behavior = [
        {
            "check": "observation_examples_do_not_allow_direct_current_state_or_compliance_fact",
            "pass": all("CURRENT_STATE_DIRECTLY" in e["promotionUse"].get("mustNotPromoteTo", []) or e["promotionUse"]["highConsequenceUse"] in {"REVIEW_REQUIRED", "BLOCKED_PENDING_CONTEXT", "BLOCKED_PENDING_RESULT", "LOW_CONSEQUENCE_ONLY"} for e in obs_examples)
        },
        {
            "check": "pending_sample_blocks_high_consequence_use",
            "pass": any(e["contextCompleteness"] == "INCOMPLETE_BLOCK_HIGH_CONSEQUENCE" and e["promotionUse"]["highConsequenceUse"] == "BLOCKED_PENDING_RESULT" for e in obs_examples)
        },
        {
            "check": "below_loq_result_is_censored_not_zero",
            "pass": any(m["result"]["resultKind"] == "CENSORED_NUMERIC" and "detectionLimit" in m["result"] and m["result"].get("numericValue") is None for m in meas_examples)
        },
        {
            "check": "calibrated_sensor_retains_calibration_context",
            "pass": any(m.get("calibration", {}).get("calibrationStatus") == "CURRENT" for m in meas_examples)
        }
    ]
    results["behaviorChecks"] = [{"check": b["check"], "status": "PASS" if b["pass"] else "FAIL"} for b in behavior]
    if any(b["status"] != "PASS" for b in results["behaviorChecks"]):
        results["overallStatus"] = "FAIL"

    results["coverageAdvances"] = [
        "adds active AgronomicObservationContext and MeasurementEvidence contract families",
        "proves narrative-only support remains allowed but blocked from high-consequence shortcuts",
        "proves pending samples, below-LOQ results, and calibrated sensor readings can be expressed without fake precision",
        "keeps code-binding profile and query/output reconstruction as explicit later phases after intervention and partial extent closures"
    ]
    OUT.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(results["overallStatus"])
    return 0 if results["overallStatus"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
