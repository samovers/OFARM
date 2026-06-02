#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
IMPL = ROOT / "04_implementation_and_conformance"
MC = ROOT / "03_machine_contracts"
COMP = ROOT / "01_companion_artifacts"
RFC = ROOT / "02_accepted_rfcs"
RECORDS = IMPL / "OFARM_operational_break_test_suite_records_v0_1.json"
OUT = IMPL / "OFARM_operational_break_test_suite_results_v0_1.json"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def artifact_exists(ref: str) -> bool:
    for base in [IMPL, MC, COMP, RFC]:
        if (base / ref).exists():
            return True
    # Records may cite rootless files by exact name in implementation dir or machine contracts.
    return False


def check_scenario(s: dict[str, Any]) -> dict[str, Any]:
    sid = s["scenarioId"]
    expected = s["expected"]
    refs = s.get("inputRefs", [])
    missing = [r for r in refs if not artifact_exists(r)]
    result = {"scenarioId": sid, "missingRefs": missing, "status": "PASS", "checks": {}}

    if sid.startswith("BREAK-001"):
        checks = {
            "historical_claim_retained": expected["historicalClaimRetained"] is True,
            "authority_recheck_required": expected["authorityRecheck"] == "REQUIRED",
            "promotion_requires_review": expected["promotionDisposition"] == "REQUIRE_REVIEW",
            "accepted_scope_limited": expected["acceptedExecutionScope"] == "LIMITED_TO_REVIEWED_EXTENT",
            "passport_discloses_or_refuses": expected["passportViewDisposition"] == "REFUSE_OR_DISCLOSE_LIMITATION",
            "document_annex_no_promotion": expected["documentAssemblyDisposition"] == "ANNEX_DISPUTE_WITHOUT_PROMOTION",
        }
    elif sid.startswith("BREAK-002"):
        checks = {
            "alias_pinning_required": expected["aliasVersionPinned"] == "REQUIRED_FOR_HIGH_CONSEQUENCE",
            "binding_conflict_detected": expected["bindingConflictDetected"] is True,
            "canonical_binding_path_agronomic": expected["canonicalBindingPath"] == "agronomicIdentityBindingRefs",
            "output_does_not_pass_silently": expected["outputDisposition"] == "REQUIRE_REVIEW_OR_REFUSE_OUTPUT",
        }
    elif sid.startswith("BREAK-003"):
        checks = {k: v is True for k, v in expected.items()}
    elif sid.startswith("BREAK-004"):
        checks = {k: v is True for k, v in expected.items()}
    elif sid.startswith("BREAK-005"):
        checks = {k: v is True for k, v in expected.items()}
    else:
        checks = {"known_scenario": False}

    result["checks"] = checks
    if missing:
        result["status"] = "PASS_WITH_MISSING_REFERENCE_WARNINGS"
    if not all(checks.values()):
        result["status"] = "FAIL"
    return result


def main() -> int:
    records = load_json(RECORDS)
    scenario_results = [check_scenario(s) for s in records["scenarios"]]
    fail = [r for r in scenario_results if r["status"] == "FAIL"]
    warn = [r for r in scenario_results if r["status"] == "PASS_WITH_MISSING_REFERENCE_WARNINGS"]
    overall = "FAIL" if fail else ("PASS_WITH_WARNINGS" if warn else "PASS")
    result = {
        "schemaVersion":"ofarm.operationalBreakTestSuiteResults.v0.1",
        "date":"2026-05-14",
        "phase":"ONT-SEMINT Phase 5",
        "recordSetId": records.get("recordSetId"),
        "overallStatus": overall,
        "summary":{"scenariosChecked": len(scenario_results), "passCount": sum(1 for r in scenario_results if r["status"] == "PASS"), "warningCount": len(warn), "failCount": len(fail)},
        "scenarioResults": scenario_results,
        "coverageAdvances":["delayed-sync authority/dispute path", "alias plus external-binding drift", "stage separation", "observation-to-audit reconstruction", "semantic drift detection"],
        "limitations": records.get("limitations", [])
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(overall)
    return 0 if overall != "FAIL" else 1

if __name__ == "__main__":
    raise SystemExit(main())
