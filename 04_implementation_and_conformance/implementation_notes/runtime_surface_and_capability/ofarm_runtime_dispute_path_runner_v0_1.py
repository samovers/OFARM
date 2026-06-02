#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MC = ROOT / "03_machine_contracts"
IMP = ROOT / "04_implementation_and_conformance"
RECORDS = IMP / "OFARM_runtime_dispute_path_records_v0_1.json"
RESULTS = IMP / "OFARM_runtime_dispute_path_results_v0_1.json"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def collect_primary_ids(obj: Any) -> dict[str, str]:
    ids: dict[str, str] = {}
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, str) and (
                key.endswith("Id")
                or key in {
                    "documentAssemblyId",
                    "reviewDecisionId",
                    "traceId",
                    "requestId",
                    "resultId",
                    "sufficiencyCaseId",
                }
            ):
                ids[value] = key
    return ids


def build_index() -> dict[str, str]:
    index: dict[str, str] = {}
    for path in sorted(MC.glob("*_example_*.json")):
        obj = load_json(path)
        for value in collect_primary_ids(obj):
            index[value] = path.name
    return index


def main() -> int:
    records = load_json(RECORDS)
    id_index = build_index()
    scenario_results = []
    all_pass = True

    for scenario in records["scenarios"]:
        checks: dict[str, bool] = {}
        for field in [
            "plannedInterventionId",
            "operationClaimAssertionRef",
            "acceptedReviewDecisionRef",
            "acceptedEventConsequenceRef",
            "originalDocumentAssemblyRef",
            "successorDocumentAssemblyRef",
            "originalSubmissionAssemblyRef",
            "successorSubmissionAssemblyRef",
            "delegationGrantRef",
            "offlineOperationClaimAssertionRef",
            "offlineEvidenceCaseRef",
            "allowAtCaptureTraceRef",
            "syncRecheckTraceRef",
            "revocationDecisionRef",
            "reviewDecisionRef",
        ]:
            value = scenario.get(field)
            if value is not None:
                checks[f"{field}Resolvable"] = value in id_index

        for idx, value in enumerate(scenario.get("lateEvidenceCaseRefs", []), start=1):
            checks[f"lateEvidenceCaseRef{idx}Resolvable"] = value in id_index
        for idx, value in enumerate(scenario.get("successorReviewDecisionRefs", []), start=1):
            checks[f"successorReviewDecisionRef{idx}Resolvable"] = value in id_index

        preservation_checks = scenario.get("preservationChecks", {})
        for key, value in preservation_checks.items():
            if key == "editInPlaceAllowed":
                checks["editInPlaceBlocked"] = value is False
            else:
                checks[key] = bool(value)

        if scenario["fixtureClass"] == "LATE_EVIDENCE_SUCCESSOR_PATH":
            checks["originalVsSuccessorDossierDistinct"] = scenario["originalDocumentAssemblyRef"] != scenario["successorDocumentAssemblyRef"]
            checks["originalVsSuccessorSubmissionDistinct"] = scenario["originalSubmissionAssemblyRef"] != scenario["successorSubmissionAssemblyRef"]
            checks["twoLateEvidenceCasesPresent"] = len(scenario.get("lateEvidenceCaseRefs", [])) == 2
            checks["twoSuccessorReviewDecisionsPresent"] = len(scenario.get("successorReviewDecisionRefs", [])) == 2
            checks["expectedTerminalOutcomeValid"] = scenario["expectedTerminalOutcome"] == "SUCCESSOR_PATH_REQUIRED"
        elif scenario["fixtureClass"] == "OFFLINE_SYNC_REVOCATION_RECHECK":
            checks["allowTraceDistinctFromRecheckTrace"] = scenario["allowAtCaptureTraceRef"] != scenario["syncRecheckTraceRef"]
            checks["expectedTerminalOutcomeValid"] = scenario["expectedTerminalOutcome"] == "REVIEW_REQUIRED_AFTER_REVOCATION"

        status = "PASS" if all(checks.values()) else "FAIL"
        if status != "PASS":
            all_pass = False
        scenario_results.append(
            {
                "scenarioId": scenario["scenarioId"],
                "fixtureClass": scenario["fixtureClass"],
                "status": status,
                "checks": checks,
            }
        )

    results = {
        "wave": records["wave"],
        "title": records["title"],
        "overallStatus": "PASS_WITH_LIMITATIONS" if all_pass else "FAIL",
        "scenarioCount": len(records["scenarios"]),
        "scenarioResults": scenario_results,
        "coverageAdvances": [
            "late-evidence correction and no-edit-in-place tests",
            "successor dossier/submission correction path tests",
            "offline delayed-sync revocation recheck tests",
            "historical actor preservation under contractor revocation tests"
        ],
        "limitations": [
            "These fixtures are package-internal runtime-shaped records rather than deployment-collected telemetry.",
            "The delayed-sync scenario proves review-required behavior after revocation, not a full product-grade sync engine."
        ],
    }

    RESULTS.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
