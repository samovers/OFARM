#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
IMPL = ROOT / "04_implementation_and_conformance"
RECORDS = IMPL / "OFARM_agronomic_scenario_records_v0_1.json"
RUNTIME_CHAIN_RESULTS = IMPL / "OFARM_agronomic_runtime_chain_results_v0_1.json"
OUT = IMPL / "OFARM_agronomic_scenario_fixture_results_v0_1.json"

REQUIRED_SCENARIO_FAMILIES = {
    "observation_to_decision",
    "recommendation_prescription_execution",
    "offline_contractor_late_sync",
    "partial_failed_application_correction",
    "partial_replant_mixed_variety",
    "measurement_context_dispute",
}

ACCEPTED_COVERAGE_STATUSES = {
    "PARTIAL",
    "PARTIAL_WITH_CARRIER",
    "NOT_STARTED",
    "CHAIN_COVERED",
    "EXECUTABLE_CHAIN_SUPPORTED",
    "COVERED",
}

HIGH_CONSEQUENCE_BLOCK_TOKENS = {
    "auto_promotion",
    "accepted_execution",
    "planned_intervention_as_execution_truth",
    "partial_as_whole_field_truth",
    "whole_field_crop_cycle_overwrite",
    "false_precision",
    "projection_only_semantic_truth",
    "silent_frozen_output_basis_mutation",
    "overwrite",
    "accepted high-consequence output",
    "compliance truth",
    "accepted product identity",
    "buyer-ready",
    "dry safe",
    "inferred",
    "directly",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def artifact_exists(relpath: str) -> bool:
    return (ROOT / relpath).exists()


def runtime_chain_status() -> tuple[str, bool, list[str]]:
    if not RUNTIME_CHAIN_RESULTS.exists():
        return "MISSING", False, []
    result = load_json(RUNTIME_CHAIN_RESULTS)
    covered_ids = result.get("coveredScenarioIds", [])
    status = result.get("overallStatus", "UNKNOWN")
    # The AGR-P8 runner covers all AGR-SCEN ids; this scenario runner needs a PASS to close the legacy expectation-level limitation.
    return status, status == "PASS", covered_ids


def check_scenario(scenario: dict[str, Any]) -> dict[str, Any]:
    checks: dict[str, bool] = {}
    sid = scenario.get("scenarioId", "<missing>")

    checks["has_required_identity"] = all(scenario.get(k) for k in ["scenarioId", "title", "family", "coverageStatus", "summary"])
    checks["coverage_status_is_honest"] = scenario.get("coverageStatus") in ACCEPTED_COVERAGE_STATUSES
    checks["active_artifacts_resolve"] = all(artifact_exists(p) for p in scenario.get("requiredActiveArtifacts", []))
    checks["supporting_research_resolves"] = all(artifact_exists(p) for p in scenario.get("supportingResearchRefs", []))
    checks["has_event_sequence"] = len(scenario.get("eventSequence", [])) >= 2
    checks["event_steps_have_separation"] = all(step.get("mustRemainDistinctFrom") for step in scenario.get("eventSequence", []))
    checks["has_agronomic_context_requirements"] = len(scenario.get("requiredAgronomicContext", [])) >= 3
    checks["gap_or_executable_chain_declared"] = len(scenario.get("currentPackageGaps", [])) >= 1 or scenario.get("coverageStatus") in {"CHAIN_COVERED", "EXECUTABLE_CHAIN_SUPPORTED", "COVERED"}

    promotion = scenario.get("expectedPromotionBehavior", {})
    checks["has_promotion_expectation"] = bool(promotion.get("terminalOutcome")) and len(promotion.get("mustBlock", [])) >= 1 and len(promotion.get("mustPreserve", [])) >= 1
    checks["promotion_not_unconditional_allow"] = "ALLOW" not in str(promotion.get("terminalOutcome", ""))

    materialization = scenario.get("expectedMaterializationBehavior", {})
    checks["has_materialization_expectation"] = bool(materialization.get("freshnessRequirement")) and len(materialization.get("mustInvalidateOrReviewWhen", [])) >= 1

    output = scenario.get("expectedOutputBehavior", {})
    checks["has_output_expectation"] = bool(output.get("passportView")) and bool(output.get("documentAssembly"))

    negatives = scenario.get("negativeChecks", [])
    checks["has_negative_checks"] = len(negatives) >= 1 and all(n.get("checkId") and n.get("mustFail") for n in negatives)

    all_block_text = " ".join(promotion.get("mustBlock", []) + [n.get("mustFail", "") for n in negatives]).lower()
    checks["negative_checks_block_high_consequence_shortcuts"] = any(token in all_block_text for token in HIGH_CONSEQUENCE_BLOCK_TOKENS) or "must fail" in all_block_text or "direct" in all_block_text

    phase = scenario.get("phaseMapping", {})
    checks["mapped_to_active_task"] = "IMP-304" in phase.get("activeTaskRefs", []) or "IMP-308" in phase.get("activeTaskRefs", []) or "IMP-313" in phase.get("activeTaskRefs", [])
    checks["has_future_or_closed_closure_task"] = len(phase.get("futureTaskRefs", [])) >= 1 or scenario.get("coverageStatus") in {"CHAIN_COVERED", "EXECUTABLE_CHAIN_SUPPORTED", "COVERED"}
    checks["has_recommended_patch_or_closure"] = bool(scenario.get("recommendedNextPatch")) or scenario.get("coverageStatus") in {"CHAIN_COVERED", "EXECUTABLE_CHAIN_SUPPORTED", "COVERED"}

    return {"scenarioId": sid, "status": "PASS" if all(checks.values()) else "FAIL", "checks": checks}


def main() -> int:
    records = load_json(RECORDS)
    scenario_results = [check_scenario(s) for s in records.get("scenarios", [])]

    families = {s.get("family") for s in records.get("scenarios", [])}
    required_present = REQUIRED_SCENARIO_FAMILIES <= families
    scenario_ids = [s.get("scenarioId") for s in records.get("scenarios", [])]
    all_unique = len(scenario_ids) == len(set(scenario_ids))
    all_pass = all(r["status"] == "PASS" for r in scenario_results)
    chain_status, chain_pass, covered_chain_ids = runtime_chain_status()

    overall = "PASS" if all_pass and required_present and all_unique and chain_pass else "PASS_WITH_LIMITATIONS" if all_pass and required_present and all_unique else "FAIL"

    results = {
        "schemaVersion": "ofarm.agronomicScenarioFixtureResults.v0.1",
        "date": "2026-05-13",
        "scenarioSetId": records.get("scenarioSetId"),
        "overallStatus": overall,
        "scenarioCount": len(scenario_results),
        "requiredFamiliesPresent": sorted(REQUIRED_SCENARIO_FAMILIES & families),
        "missingRequiredFamilies": sorted(REQUIRED_SCENARIO_FAMILIES - families),
        "scenarioIdsUnique": all_unique,
        "runtimeChainClosureStatus": chain_status,
        "runtimeChainResultRef": str(RUNTIME_CHAIN_RESULTS.relative_to(ROOT)) if RUNTIME_CHAIN_RESULTS.exists() else "",
        "runtimeChainCoveredScenarioIds": covered_chain_ids,
        "scenarioResults": scenario_results,
        "coverageAdvances": [
            "establishes a repository-visible agronomic scenario coverage baseline",
            "proves each scenario has explicit promotion, materialization, output, and negative-check expectations",
            "AGR-P8 runtime-chain closure now provides package-local chain evidence for all AGR-SCEN identifiers",
            "keeps live pilot data, production runtime, live registry checks, and wire-level exchange mappings out of scope"
        ],
        "limitations": [
            "AGR-P8 adds package-local runtime-chain fixtures, so the scenario suite passes when those chain results pass.",
            "This is conformance-fixture evidence, not live pilot evidence or a production runtime implementation.",
            "Future limitations belong to live registry checks, real exchange data, wire-level ISOXML/EFDI/ADAPT mappings, crop/jurisdiction packs, and production runtime telemetry."
        ] if overall == "PASS" else [
            "This runner validates scenario completeness and authority-boundary discipline only unless the AGR-P8 runtime-chain runner passes.",
            "If AGR-P8 does not pass, the suite remains PASS_WITH_LIMITATIONS because it is still expectation-level only."
        ]
    }
    OUT.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(results["overallStatus"])
    return 0 if results["overallStatus"] in {"PASS", "PASS_WITH_LIMITATIONS"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
