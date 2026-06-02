#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MC = ROOT / "03_machine_contracts"
IMP = ROOT / "04_implementation_and_conformance"
RECORDS = IMP / "OFARM_offline_revocation_and_scope_drift_break_test_records_v0_1.json"
DISPUTE_RESULTS = IMP / "OFARM_runtime_dispute_path_results_v0_1.json"
OUT = IMP / "OFARM_offline_revocation_and_scope_drift_break_test_results_v0_1.json"

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

def build_index() -> dict[str, tuple[str, Any]]:
    index: dict[str, tuple[str, Any]] = {}
    for path in sorted(MC.glob("*_example_*.json")):
        obj = load_json(path)
        for value in collect_primary_ids(obj):
            index[value] = (path.name, obj)
    return index

def main() -> int:
    records = load_json(RECORDS)
    dispute_results = load_json(DISPUTE_RESULTS)
    id_index = build_index()

    scenario_results = []
    all_pass = True
    dispute_map = {s["scenarioId"]: s for s in dispute_results.get("scenarioResults", [])}

    for scenario in records["scenarios"]:
        checks: dict[str, bool] = {}
        delegation = id_index.get(scenario["delegationGrantRef"])
        revocation = id_index.get(scenario["revocationDecisionRef"])
        trace = id_index.get(scenario["syncRecheckTraceRef"])
        lifecycle = id_index.get(scenario["identityLifecycleChangeRef"])
        mat_result = id_index.get(scenario["materializationResultRef"])
        dispute = dispute_map.get(scenario["disputePathScenarioId"])

        checks["delegationGrantResolvable"] = delegation is not None
        checks["revocationDecisionResolvable"] = revocation is not None
        checks["syncRecheckTraceResolvable"] = trace is not None
        checks["identityLifecycleChangeResolvable"] = lifecycle is not None
        checks["materializationResultResolvable"] = mat_result is not None
        checks["disputeScenarioPresent"] = dispute is not None

        if delegation and revocation:
            checks["revocationLinksDelegation"] = revocation[1].get("revokesArtifactRef") == delegation[1].get("delegationGrantId")
            checks["delegationScopeIsParentField"] = delegation[1].get("targetScope", {}).get("scopeRef") == "field:17"
        else:
            checks["revocationLinksDelegation"] = False
            checks["delegationScopeIsParentField"] = False

        if trace:
            checks["syncTraceRequiresReview"] = trace[1].get("decisionOutcome") == "REQUIRE_REVIEW"
            checks["syncTraceHasActiveRevocation"] = trace[1].get("revocationResult") == "ACTIVE_REVOCATION_FOUND"
            checks["traceTargetsParentField"] = trace[1].get("target", {}).get("scope", {}).get("scopeRef") == "field:17"
        else:
            checks["syncTraceRequiresReview"] = False
            checks["syncTraceHasActiveRevocation"] = False
            checks["traceTargetsParentField"] = False

        if lifecycle:
            checks["fieldSplitOutcomeValid"] = lifecycle[1].get("continuityOutcome") == "NEW_IDENTITIES_WITH_SPLIT_FROM"
            checks["fieldSplitCreatesChildren"] = len(lifecycle[1].get("newIdentityRefs", [])) >= 2
        else:
            checks["fieldSplitOutcomeValid"] = False
            checks["fieldSplitCreatesChildren"] = False

        if mat_result:
            related_refs = []
            for problem in mat_result[1].get("problems", []):
                related_refs.extend(problem.get("relatedRefs", []))
            checks["materializationRefusesReuse"] = mat_result[1].get("decisionOutcome") == "REFUSE_USE"
            checks["materializationMarkedInvalid"] = mat_result[1].get("freshnessState") == "INVALID"
            checks["identityLifecycleTriggerPresent"] = "IDENTITY_LIFECYCLE" in mat_result[1].get("invalidationTriggerFamilies", [])
            checks["materializationProblemLinksFieldSplit"] = scenario["identityLifecycleChangeRef"] in related_refs
        else:
            checks["materializationRefusesReuse"] = False
            checks["materializationMarkedInvalid"] = False
            checks["identityLifecycleTriggerPresent"] = False
            checks["materializationProblemLinksFieldSplit"] = False

        if dispute:
            checks["existingDisputeScenarioPasses"] = dispute.get("status") == "PASS"
            checks["manualReviewRequired"] = bool(dispute.get("checks", {}).get("manualReviewRequired"))
            checks["autoPromotionBlockedAfterRevocation"] = bool(dispute.get("checks", {}).get("autoPromotionBlockedAfterRevocation"))
        else:
            checks["existingDisputeScenarioPasses"] = False
            checks["manualReviewRequired"] = False
            checks["autoPromotionBlockedAfterRevocation"] = False

        checks["expectedTerminalOutcomeValid"] = (
            scenario["expectedTerminalOutcome"] == "REVIEW_AND_RECOMPUTE_REQUIRED"
            and checks["syncTraceRequiresReview"]
            and checks["materializationRefusesReuse"]
        )

        status = "PASS" if all(checks.values()) else "FAIL"
        if status != "PASS":
            all_pass = False
        scenario_results.append({
            "scenarioId": scenario["scenarioId"],
            "status": status,
            "checks": checks
        })

    results = {
        "wave": records["wave"],
        "title": records["title"],
        "overallStatus": "PASS_WITH_LIMITATIONS" if all_pass else "FAIL",
        "scenarioCount": len(records["scenarios"]),
        "scenarioResults": scenario_results,
        "coverageAdvances": [
            "composes delayed-sync revocation review with an active field-split lifecycle contract",
            "proves stale parent-scope current-state refusal after governed scope drift",
            "keeps historical contractor record while blocking silent high-consequence reuse"
        ],
        "limitations": [
            "This is a package-local hostile composition test rather than deployment-collected sync telemetry.",
            "The test proves one parent-field split path only; broader merge/supersession permutations remain follow-on work."
        ]
    }
    OUT.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    return 0 if all_pass else 1

if __name__ == "__main__":
    raise SystemExit(main())
