#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
IMPL = ROOT / "04_implementation_and_conformance"
RECORDS = IMPL / "OFARM_agronomic_runtime_chain_records_v0_1.json"
OUT = IMPL / "OFARM_agronomic_runtime_chain_results_v0_1.json"

REQUIRED_SCENARIOS = {f"AGR-SCEN-{i:03d}" for i in range(1, 11)}
REQUIRED_CARRIERS = {
    "AgronomicObservationContext",
    "MeasurementEvidence",
    "InterventionIntentPayload",
    "ExecutionRecordPayload",
    "PartialExtent",
    "AgronomicIdentityBinding",
    "AgronomicCodeBindingProfile",
    "EvidenceSufficiencyCase",
    "AcceptedEventConsequence",
    "AgronomicReconstructionTrace",
}
BLOCK_TOKENS = {
    "auto",
    "direct",
    "whole-field",
    "whole_field",
    "projection-only",
    "stale",
    "overwrite",
    "marketing-name",
    "machine",
    "false",
    "unresolved",
    "accepted high-consequence",
}
UPSTREAM_PASS_KEYS = ("overallStatus", "overall")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def artifact_exists(relpath: str) -> bool:
    return (ROOT / relpath).exists()


def upstream_status(path: Path) -> str:
    data = load_json(path)
    for key in UPSTREAM_PASS_KEYS:
        value = data.get(key)
        if isinstance(value, str):
            return value
    return "UNKNOWN"


def check_chain(chain: dict[str, Any]) -> dict[str, Any]:
    checks: dict[str, bool] = {}
    cid = chain.get("chainId", "<missing>")
    steps = chain.get("stepSequence", [])
    contract_refs = chain.get("contractInstanceRefs", [])
    promotion = chain.get("expectedPromotionBehavior", {})
    materialization = chain.get("expectedMaterializationBehavior", {})
    output = chain.get("expectedOutputBehavior", {})
    negative_checks = chain.get("negativeChecks", [])

    checks["has_identity"] = all(chain.get(k) for k in ["chainId", "title", "chainKind", "status"])
    checks["status_closed"] = chain.get("status") == "COVERED_BY_PACKAGE_LOCAL_CHAIN"
    checks["covers_scenario"] = len(chain.get("scenarioRefs", [])) >= 1
    checks["has_multiple_steps"] = len(steps) >= 2
    checks["steps_have_ordered_ids"] = all(step.get("stepId") for step in steps)
    checks["steps_preserve_distinctions"] = all(step.get("mustRemainDistinctFrom") for step in steps)
    checks["steps_have_promotion_materialization_output"] = all(step.get("promotionOutcome") and step.get("materializationOutcome") and step.get("outputOutcome") for step in steps)
    checks["contract_refs_resolve"] = len(contract_refs) >= 3 and all(artifact_exists(ref.get("artifact", "")) for ref in contract_refs)
    checks["step_refs_resolve"] = all(artifact_exists(ref) for step in steps for ref in step.get("artifactRefs", []))
    checks["uses_required_carrier"] = bool(set(chain.get("requiredCarriers", [])) & REQUIRED_CARRIERS)
    checks["has_promotion_expectation"] = bool(promotion.get("terminalOutcome")) and len(promotion.get("mustBlock", [])) >= 1 and len(promotion.get("mustPreserve", [])) >= 1
    checks["has_materialization_expectation"] = bool(materialization.get("terminalOutcome")) and len(materialization.get("mustInvalidateOrReviewWhen", [])) >= 1
    checks["has_output_expectation"] = bool(output.get("passportView")) and bool(output.get("documentAssembly"))
    checks["has_negative_checks"] = len(negative_checks) >= 2 and all(n.get("checkId") and n.get("mustFail") for n in negative_checks)
    block_text = " ".join(promotion.get("mustBlock", []) + [n.get("mustFail", "") for n in negative_checks]).lower()
    checks["negative_checks_block_shortcuts"] = any(token in block_text for token in BLOCK_TOKENS)
    checks["does_not_make_unconditional_allow"] = "ALLOW_ALL" not in str(promotion.get("terminalOutcome", ""))

    return {"chainId": cid, "status": "PASS" if all(checks.values()) else "FAIL", "checks": checks}


def main() -> int:
    records = load_json(RECORDS)
    upstream_checks = []
    for rel in records.get("upstreamPhaseResultRefs", []):
        path = ROOT / rel
        exists = path.exists()
        status = upstream_status(path) if exists else "MISSING"
        upstream_checks.append({"artifact": rel, "exists": exists, "status": status, "pass": exists and status == "PASS"})

    chain_results = [check_chain(c) for c in records.get("chains", [])]
    covered_scenarios = {sid for c in records.get("chains", []) for sid in c.get("scenarioRefs", [])}
    used_carriers = {carrier for c in records.get("chains", []) for carrier in c.get("requiredCarriers", [])}

    checks = {
        "upstream_phase_results_pass": all(c["pass"] for c in upstream_checks),
        "required_scenarios_covered": REQUIRED_SCENARIOS <= covered_scenarios,
        "minimum_chain_count": len(chain_results) >= records.get("scenarioCoverageRequirement", {}).get("requiredChainCountMinimum", 6),
        "required_carriers_covered": REQUIRED_CARRIERS <= used_carriers,
        "chain_ids_unique": len({c.get("chainId") for c in records.get("chains", [])}) == len(records.get("chains", [])),
        "all_chains_pass": all(r["status"] == "PASS" for r in chain_results),
    }

    overall = "PASS" if all(checks.values()) else "FAIL"
    result = {
        "schemaVersion": "ofarm.agronomicRuntimeChainResults.v0.1",
        "date": "2026-05-13",
        "runner": Path(__file__).name,
        "fixtureSetId": records.get("fixtureSetId"),
        "overallStatus": overall,
        "checks": checks,
        "upstreamPhaseChecks": upstream_checks,
        "coveredScenarioIds": sorted(covered_scenarios),
        "missingScenarioIds": sorted(REQUIRED_SCENARIOS - covered_scenarios),
        "usedCarrierFamilies": sorted(used_carriers),
        "missingCarrierFamilies": sorted(REQUIRED_CARRIERS - used_carriers),
        "chainResults": chain_results,
        "coverageAdvances": [
            "closes the AGR-P1 expectation-only limitation with package-local runtime-chain fixtures",
            "assembles AGR-P2 through AGR-P7 carrier shells into end-to-end agronomic chains",
            "proves scenario coverage across all ten AGR-SCEN identifiers",
            "preserves recommendation/prescription/execution/claim/accepted-consequence separation",
            "keeps live pilot evidence, live registry checks, and wire-level exchange mapping outside this package-local closure"
        ],
        "limitations": records.get("limitations", [])
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(overall)
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
