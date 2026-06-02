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
RECORDS = IMPL / "OFARM_agronomic_intervention_as_applied_records_v0_1.json"
OUT = IMPL / "OFARM_agronomic_intervention_as_applied_results_v0_1.json"


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
        "schemaVersion": "ofarm.agronomicInterventionAsAppliedResults.v0.1",
        "date": "2026-05-12",
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

    results["negativeChecks"].append(expect_invalid(
        "intent_quantity_requires_unit",
        "03_machine_contracts/schemas/agronomic/OFARM_InterventionIntentPayload_schema_v0_1.json",
        "04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agronomic/OFARM_InterventionIntentPayload_example_field_17_spot_spray_authorized_prescription_v0_1.json",
        lambda d: d["quantityParameters"][0].pop("unitRef", None),
    ))
    results["negativeChecks"].append(expect_invalid(
        "execution_quantity_requires_unit",
        "03_machine_contracts/schemas/agronomic/OFARM_ExecutionRecordPayload_schema_v0_1.json",
        "04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agronomic/OFARM_ExecutionRecordPayload_example_field_17_partial_accepted_execution_v0_1.json",
        lambda d: d["actualQuantityParameters"][0].pop("unitRef", None),
    ))
    results["negativeChecks"].append(expect_invalid(
        "accepted_execution_requires_sufficiency_case",
        "03_machine_contracts/schemas/agronomic/OFARM_ExecutionRecordPayload_schema_v0_1.json",
        "04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agronomic/OFARM_ExecutionRecordPayload_example_field_17_partial_accepted_execution_v0_1.json",
        lambda d: d.pop("evidenceSufficiencyCaseRef", None),
    ))
    results["negativeChecks"].append(expect_invalid(
        "correction_requires_correction_lineage",
        "03_machine_contracts/schemas/agronomic/OFARM_ExecutionRecordPayload_schema_v0_1.json",
        "04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agronomic/OFARM_ExecutionRecordPayload_example_field_17_manual_correction_supersedes_claim_v0_1.json",
        lambda d: d.pop("correctionOfExecutionRecordPayloadRef", None),
    ))
    if any(c.get("status") != "PASS" for c in results["negativeChecks"]):
        results["overallStatus"] = "FAIL"

    rec = load_json(ROOT / "04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agronomic/OFARM_InterventionIntentPayload_example_field_17_spot_spray_advisory_recommendation_v0_1.json")
    presc = load_json(ROOT / "04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agronomic/OFARM_InterventionIntentPayload_example_field_17_spot_spray_authorized_prescription_v0_1.json")
    plan = load_json(ROOT / "04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agronomic/OFARM_InterventionIntentPayload_example_field_17_spot_spray_planned_operation_v0_1.json")
    claim = load_json(ROOT / "04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agronomic/OFARM_ExecutionRecordPayload_example_field_17_contractor_spot_spray_claim_late_sync_v0_1.json")
    mach = load_json(ROOT / "04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agronomic/OFARM_ExecutionRecordPayload_example_field_17_machine_log_partial_application_v0_1.json")
    accepted = load_json(ROOT / "04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agronomic/OFARM_ExecutionRecordPayload_example_field_17_partial_accepted_execution_v0_1.json")
    correction = load_json(ROOT / "04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agronomic/OFARM_ExecutionRecordPayload_example_field_17_manual_correction_supersedes_claim_v0_1.json")
    dispute = load_json(ROOT / "04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agronomic/OFARM_ExecutionRecordPayload_example_field_17_extent_dispute_v0_1.json")

    behavior = [
        ("recommendation_advisory_only", rec["intentClass"] == "RECOMMENDATION" and rec["promotionBoundary"]["targetTwin"] == "ADVISORY" and "ACCEPTED_EXECUTION" in rec["promotionBoundary"]["mustNotPromoteTo"]),
        ("prescription_has_authority_but_not_execution", presc["intentClass"] == "PRESCRIPTION" and "authorityRef" in presc and "ACCEPTED_EXECUTION" in presc["promotionBoundary"]["mustNotPromoteTo"]),
        ("planned_operation_plan_only", plan["intentClass"] == "PLANNED_OPERATION" and plan["promotionBoundary"]["highConsequenceUse"] == "PLAN_ONLY"),
        ("claim_missing_rate_review_required", claim["recordClass"] == "OPERATION_CLAIM" and "actualQuantityParameters" not in claim and any(d["deltaType"] == "MISSING_RATE" for d in claim.get("actualVsPlannedDeltas", []))),
        ("machine_log_as_evidence_not_truth", mach["recordClass"] == "AS_APPLIED_EVIDENCE" and mach["promotionBoundary"]["highConsequenceUse"] == "EVIDENCE_ONLY"),
        ("partial_accepted_execution_limited_to_subextent", accepted["recordClass"] == "ACCEPTED_EXECUTION_DETAIL" and accepted["recordState"] == "PARTIAL_ACCEPTED" and accepted["executionExtent"]["extentClass"] in {"PARTIAL_TARGET_SCOPE", "FAILED_PASS"}),
        ("correction_preserves_lineage", correction["recordClass"] == "CORRECTION" and correction.get("correctionOfExecutionRecordPayloadRef") == claim["executionRecordPayloadId"]),
        ("dispute_review_gated", dispute["recordClass"] == "DISPUTE" and dispute["promotionBoundary"]["highConsequenceUse"] == "REVIEW_REQUIRED"),
        ("quantity_kind_and_unit_required", all("quantityKindRef" in q and "unitRef" in q for q in presc["quantityParameters"] + accepted["actualQuantityParameters"])),
    ]
    results["behaviorChecks"] = [{"check": name, "status": "PASS" if ok else "FAIL"} for name, ok in behavior]
    if any(b["status"] != "PASS" for b in results["behaviorChecks"]):
        results["overallStatus"] = "FAIL"

    results["coverageAdvances"] = [
        "adds active InterventionIntentPayload and ExecutionRecordPayload contract families",
        "binds planned-intervention, assertion, event-envelope, accepted-consequence, and evidence-sufficiency examples to the new payloads",
        "proves recommendation/prescription/plan/claim/as-applied/accepted/correction/dispute separation through behavior checks",
        "keeps agronomic code-binding, query/output reconstruction, and baseline harmonization as explicit future phases after PartialExtent closure",
    ]
    OUT.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(results["overallStatus"])
    return 0 if results["overallStatus"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
