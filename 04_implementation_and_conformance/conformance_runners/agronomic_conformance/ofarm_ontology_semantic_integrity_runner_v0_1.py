#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MC = ROOT / "03_machine_contracts"
IMPL = ROOT / "04_implementation_and_conformance"
FIXTURES = IMPL / "OFARM_ontology_semantic_integrity_fixtures_v0_1.json"
OUT = IMPL / "OFARM_ontology_semantic_integrity_results_v0_1.json"
CARRIER_PREFIXES = ("OFARM_AgronomicObservationContext", "OFARM_MeasurementEvidence", "OFARM_InterventionIntentPayload", "OFARM_ExecutionRecordPayload")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def get_path(obj: Any, dotted: str) -> Any:
    cur = obj
    for part in dotted.split("."):
        if isinstance(cur, list):
            cur = cur[int(part)]
        else:
            cur = cur[part]
    return cur


def run_runner(rel: str) -> dict[str, Any]:
    path = IMPL / rel
    proc = subprocess.run([sys.executable, str(path)], cwd=str(ROOT), text=True, capture_output=True)
    return {"runner": rel, "returnCode": proc.returncode, "stdout": proc.stdout.strip(), "stderr": proc.stderr.strip(), "pass": proc.returncode == 0}


def check_carrier_file(path: Path) -> dict[str, Any]:
    obj = load_json(path)
    generic_ids = set(obj.get("identityBindingRefs", []) or [])
    canonical_ids = set(obj.get("agronomicIdentityBindingRefs", []) or [])
    generic_profile = obj.get("codeBindingProfileRef")
    canonical_profile = obj.get("agronomicCodeBindingProfileRef")
    conflicts = []
    warnings = []
    if generic_ids and canonical_ids and generic_ids != canonical_ids:
        conflicts.append("identityBindingRefs conflict with agronomicIdentityBindingRefs")
    if generic_profile and canonical_profile and generic_profile != canonical_profile:
        conflicts.append("codeBindingProfileRef conflicts with agronomicCodeBindingProfileRef")
    if generic_ids and not canonical_ids:
        warnings.append("compatibility identityBindingRefs used without canonical agronomicIdentityBindingRefs")
    if generic_profile and not canonical_profile:
        warnings.append("compatibility codeBindingProfileRef used without canonical agronomicCodeBindingProfileRef")
    status = "FAIL" if conflicts else ("WARN" if warnings else "PASS")
    return {"artifact": f"03_machine_contracts/{path.name}", "status": status, "warnings": warnings, "conflicts": conflicts}


def check_negative_carrier(case: dict[str, Any]) -> dict[str, Any]:
    generic_ids = set(case.get("identityBindingRefs", []))
    canonical_ids = set(case.get("agronomicIdentityBindingRefs", []))
    generic_profile = case.get("codeBindingProfileRef")
    canonical_profile = case.get("agronomicCodeBindingProfileRef")
    conflict = (generic_ids and canonical_ids and generic_ids != canonical_ids) or (generic_profile and canonical_profile and generic_profile != canonical_profile)
    return {"caseId": case["caseId"], "status": "EXPECTED_FAIL" if conflict else "UNEXPECTED_PASS", "expectedOutcome": case.get("expectedOutcome")}


def check_temporal_case(case: dict[str, Any]) -> dict[str, Any]:
    artifact = ROOT / case["artifact"]
    obj = load_json(artifact)
    missing = []
    values = []
    for field in case.get("requiredDistinctFields", []):
        try:
            values.append(str(get_path(obj, field)))
        except Exception:
            missing.append(field)
    all_equal = len(set(values)) <= 1 if values else True
    ok = not missing and (not case.get("mustNotAllEqual") or not all_equal)
    return {"caseId": case["caseId"], "artifact": case["artifact"], "status": "PASS" if ok else "FAIL", "missing": missing, "values": values}


def check_negative_temporal_case(case: dict[str, Any]) -> dict[str, Any]:
    values = [str(v) for v in case.get("fields", {}).values()]
    collapsed = len(set(values)) == 1 and len(values) >= 3
    return {"caseId": case["caseId"], "status": "EXPECTED_FAIL" if collapsed else "UNEXPECTED_PASS", "expectedOutcome": case.get("expectedOutcome")}


def is_high_consequence_query(obj: dict[str, Any]) -> bool:
    if obj.get("status") == "APPROVED" and obj.get("target", {}).get("twin") == "COMPLIANCE":
        return True
    mode = obj.get("resultProfile", {}).get("mode", "")
    view = obj.get("resultProfile", {}).get("viewModuleRef", "")
    if mode in {"PASSPORT_INPUT", "DOCUMENT_ASSEMBLY_INPUT", "VIEW_MODULE"} and ("passport" in view.lower() or obj.get("reconstructionPolicyRef")):
        return True
    if obj.get("reconstructionPolicyRef"):
        return True
    return False


def check_query_case(case: dict[str, Any]) -> dict[str, Any]:
    obj = load_json(ROOT / case["artifact"])
    high = is_high_consequence_query(obj)
    aliases = obj.get("semanticPathAliases", [])
    missing = [a.get("alias", "<missing>") for a in aliases if not a.get("aliasVersionRef")]
    if high and missing:
        observed = "FAIL_UNPINNED_HIGH_CONSEQUENCE_ALIAS"
    else:
        observed = "PASS"
    return {"caseId": case["caseId"], "artifact": case["artifact"], "expectedOutcome": case.get("expectedOutcome"), "observedOutcome": observed, "status": "PASS" if observed == case.get("expectedOutcome") else "FAIL", "missingAliasVersionRefs": missing, "highConsequence": high}


def main() -> int:
    fixtures = load_json(FIXTURES)
    prereq = [run_runner("ofarm_authority_status_lint_v0_1.py"), run_runner("ofarm_reference_resolution_runner_v0_1.py")]

    carrier_results = [check_carrier_file(p) for p in sorted(MC.glob("*_example_*.json")) if p.name.startswith(CARRIER_PREFIXES)]
    negative_carrier_results = [check_negative_carrier(c) for c in fixtures.get("negativeCarrierCases", [])]
    temporal_positive_results = [check_temporal_case(c) for c in fixtures.get("positiveTemporalCases", [])]
    temporal_negative_results = [check_negative_temporal_case(c) for c in fixtures.get("negativeTemporalCases", [])]
    query_results = [check_query_case(c) for c in fixtures.get("highConsequenceQueryCases", [])]

    fail_conditions = []
    if not all(r["pass"] for r in prereq):
        fail_conditions.append("prerequisite_runner_failed")
    if any(r["status"] == "FAIL" for r in carrier_results):
        fail_conditions.append("active_carrier_conflict")
    if any(r["status"] != "EXPECTED_FAIL" for r in negative_carrier_results):
        fail_conditions.append("negative_carrier_case_did_not_fail")
    if any(r["status"] != "PASS" for r in temporal_positive_results):
        fail_conditions.append("positive_temporal_case_failed")
    if any(r["status"] != "EXPECTED_FAIL" for r in temporal_negative_results):
        fail_conditions.append("negative_temporal_case_did_not_fail")
    if any(r["status"] != "PASS" for r in query_results):
        fail_conditions.append("query_gate_case_failed")

    warning_count = sum(1 for r in carrier_results if r["status"] == "WARN")
    overall = "FAIL" if fail_conditions else ("PASS_WITH_WARNINGS" if warning_count else "PASS")
    result = {
        "schemaVersion": "ofarm.ontologySemanticIntegrityResults.v0.1",
        "date": "2026-05-14",
        "runner": Path(__file__).name,
        "fixtureSetId": fixtures.get("fixtureSetId"),
        "overallStatus": overall,
        "failConditions": fail_conditions,
        "summary": {
            "prerequisiteRunners": len(prereq),
            "carrierFilesChecked": len(carrier_results),
            "carrierWarnings": warning_count,
            "carrierConflicts": sum(1 for r in carrier_results if r["status"] == "FAIL"),
            "positiveTemporalCases": len(temporal_positive_results),
            "negativeTemporalCases": len(temporal_negative_results),
            "queryGateCases": len(query_results)
        },
        "prerequisiteRunnerResults": prereq,
        "carrierCanonicalizationResults": carrier_results,
        "negativeCarrierResults": negative_carrier_results,
        "temporalPositiveResults": temporal_positive_results,
        "temporalNegativeResults": temporal_negative_results,
        "highConsequenceQueryResults": query_results,
        "breakTestStubs": fixtures.get("breakTestStubs", []),
        "limitations": fixtures.get("limitations", [])
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(overall)
    return 0 if overall != "FAIL" else 1


if __name__ == "__main__":
    raise SystemExit(main())
