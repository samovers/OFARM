
#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

try:
    import jsonschema
except ImportError as e:
    raise SystemExit("jsonschema is required for this validator") from e

ROOT = Path(__file__).resolve().parents[1]
MC = ROOT / "03_machine_contracts"
OUT = Path(__file__).resolve().parent / "OFARM_runtime_advisory_bridge_candidate_results_v0_1.json"

FILES = {
    "bridge_operation_plan": "OFARM_BridgeCandidate_example_field_17_pruning_operation_plan_v0_1.json",
    "bridge_request_evidence": "OFARM_BridgeCandidate_example_field_17_pruning_request_evidence_v0_1.json",
    "planned_intervention": "OFARM_PlannedIntervention_example_field_17_bridge_prepared_pruning_draft_v0_1.json",
    "advisory_materialization": "OFARM_MaterializationResult_example_field_advisory_stale_v0_1.json",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def expect(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


def main() -> int:
    schema = load_json(MC / "OFARM_BridgeCandidate_schema_v0_1.json")
    jsonschema.Draft202012Validator.check_schema(schema)

    records = {k: load_json(MC / v) for k, v in FILES.items()}
    example_validation = {}
    overall_pass = True

    for key in ("bridge_operation_plan", "bridge_request_evidence"):
        filename = FILES[key]
        try:
            jsonschema.validate(records[key], schema)
            example_validation[filename] = "PASS"
        except Exception as exc:
            example_validation[filename] = f"FAIL: {exc}"
            overall_pass = False

    validations = []

    op = records["bridge_operation_plan"]
    adv = records["advisory_materialization"]
    plan = records["planned_intervention"]

    try:
        expect(op["originTwin"] == "ADVISORY", "operation-plan bridge should originate in Advisory")
        expect(op["bridgePosture"] == "PROPOSAL_ONLY", "operation-plan bridge should remain proposal-shaped")
        expect(op["requiresHumanApproval"] is True, "operation-plan bridge must require human approval")
        expect(op["intendedNextTwin"] == "COMPLIANCE", "operation-plan bridge should target Compliance")
        expect("RECHECK_COMPLIANCE_FRESHNESS" in op["recheckRequirements"], "Compliance-targeted bridge must declare compliance freshness recheck")
        expect(op["sourceMaterializationResultRef"] == adv["resultId"], "bridge should point at the advisory materialization it relied on")
        expect(adv["targetTwin"] == "ADVISORY", "source materialization should be Advisory")
        expect(adv["freshnessState"] == "STALE", "source materialization should demonstrate exploratory staleness")
        expect(op["proposedDraftArtifactRef"] == plan["plannedInterventionId"], "bridge should point to the draft planned intervention")
        expect(plan["planState"] == "DRAFT", "bridge-linked intervention should remain a draft plan")
        validations.append({
            "exampleFile": FILES["bridge_operation_plan"],
            "status": "PASS",
            "checks": {
                "originTwinIsAdvisory": True,
                "proposalOnly": True,
                "humanApprovalRequired": True,
                "complianceTargeted": True,
                "complianceFreshnessRecheckPresent": True,
                "advisoryStaleSourceReferenced": True,
                "localDraftPlanLinked": True,
                "draftPlanStillDraft": True,
            }
        })
    except Exception as exc:
        overall_pass = False
        validations.append({
            "exampleFile": FILES["bridge_operation_plan"],
            "status": "FAIL",
            "detail": str(exc)
        })

    req = records["bridge_request_evidence"]
    try:
        expect(req["originTwin"] == "ADVISORY", "request-evidence bridge should originate in Advisory")
        expect(req["bridgePosture"] == "PROPOSAL_ONLY", "request-evidence bridge should remain proposal-shaped")
        expect(req["requiresHumanApproval"] is True, "request-evidence bridge must require human approval")
        expect(req["intendedNextTwin"] == "ADVISORY", "request-evidence bridge should remain advisory-targeted")
        expect("COLLECT_ADDITIONAL_EVIDENCE" in req["recheckRequirements"], "request-evidence bridge should declare evidence collection")
        validations.append({
            "exampleFile": FILES["bridge_request_evidence"],
            "status": "PASS",
            "checks": {
                "originTwinIsAdvisory": True,
                "proposalOnly": True,
                "humanApprovalRequired": True,
                "advisoryTargeted": True,
                "collectAdditionalEvidenceDeclared": True,
            }
        })
    except Exception as exc:
        overall_pass = False
        validations.append({
            "exampleFile": FILES["bridge_request_evidence"],
            "status": "FAIL",
            "detail": str(exc)
        })

    negative_checks = []

    try:
        bad = copy.deepcopy(op)
        bad["requiresHumanApproval"] = False
        jsonschema.validate(bad, schema)
        negative_checks.append({
            "caseId": "neg-human-gate",
            "status": "UNEXPECTED_PASS"
        })
        overall_pass = False
    except Exception as exc:
        negative_checks.append({
            "caseId": "neg-human-gate",
            "status": "EXPECTED_FAIL",
            "detail": str(exc).splitlines()[0]
        })

    try:
        bad = copy.deepcopy(op)
        bad["recheckRequirements"] = [
            x for x in bad["recheckRequirements"] if x != "RECHECK_COMPLIANCE_FRESHNESS"
        ]
        jsonschema.validate(bad, schema)
        negative_checks.append({
            "caseId": "neg-compliance-freshness-missing",
            "status": "UNEXPECTED_PASS"
        })
        overall_pass = False
    except Exception as exc:
        negative_checks.append({
            "caseId": "neg-compliance-freshness-missing",
            "status": "EXPECTED_FAIL",
            "detail": str(exc).splitlines()[0]
        })

    results = {
        "generatedAt": "2026-04-19T12:10:00Z",
        "overall": "PASS_WITH_LIMITATIONS" if overall_pass else "FAIL",
        "summary": {
            "examplesValidated": 2,
            "complianceTargetedExamples": 1,
            "advisoryTargetedExamples": 1,
            "allRequireHumanApproval": all(r.get("status") == "PASS" for r in validations),
            "negativeCasesChecked": len(negative_checks),
            "negativeCasesExpectedFail": sum(1 for r in negative_checks if r["status"] == "EXPECTED_FAIL"),
        },
        "validations": validations,
        "negativeChecks": negative_checks,
        "limitations": [
            "This wave promotes only the narrow BridgeCandidate handoff contract, not the full scenario-workspace object family.",
            "ScenarioSpec, ScenarioResultSet, ImportedFactExtract, and AllocationBasisDeclaration remain implementation/conformance candidates.",
            "The proof is package-local and does not yet claim deployment-collected bridge telemetry."
        ]
    }
    OUT.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    return 0 if overall_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
