#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
MC = ROOT / "03_machine_contracts"
OUT = Path(__file__).resolve().parent / "OFARM_external_standard_readiness_consistency_results_v0_1.json"

def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))

def main() -> int:
    result: Dict[str, Any] = {
        "mappingCoverageLossConsistency": {},
        "runtimeSurfaceReferences": {},
        "manifestReferenceConsistency": {},
        "claimSetConsistency": {},
        "promotionPostureChecks": {},
        "overall": "PASS",
    }

    coverage_files = [
        "OFARM_MappingCoverageStatement_example_adapt_import_v0_1.json",
        "OFARM_MappingCoverageStatement_example_isoxml_import_v0_1.json",
        "OFARM_MappingCoverageStatement_example_ngsi_ld_export_v0_1.json",
    ]
    loss_files = [
        "OFARM_LossMap_example_adapt_import_v0_1.json",
        "OFARM_LossMap_example_isoxml_import_v0_1.json",
        "OFARM_LossMap_example_ngsi_ld_export_v0_1.json",
    ]
    runtime_files = [
        "OFARM_RuntimeSurfaceContract_example_ngsi_ld_export_v0_1.json",
        "OFARM_RuntimeSurfaceContract_example_capability_discovery_v0_1.json",
        "OFARM_RuntimeSurfaceContract_example_cql2_query_facade_v0_1.json",
    ]
    claimset_files = [
        "OFARM_ConformanceClaimSet_example_core_deployment_v0_1.json",
        "OFARM_ConformanceClaimSet_example_partner_deployment_v0_1.json",
    ]

    coverage = [load_json(MC / name) for name in coverage_files]
    lossmaps = [load_json(MC / name) for name in loss_files]
    runtime_contracts = [load_json(MC / name) for name in runtime_files]
    claimsets = [load_json(MC / name) for name in claimset_files]
    manifest = load_json(MC / "OFARM_Capability_Manifest_example_core_deployment_v0_2_draft.json")
    substrate = load_json(MC / "OFARM_SemanticSubstrateBundle_example_core_profile_v0_1.json")

    loss_by_id = {item["lossMapId"]: item for item in lossmaps}
    contract_by_id = {item["contractId"]: item for item in runtime_contracts}
    claimset_by_id = {item["claimSetId"]: item for item in claimsets}
    coverage_ids = {item["statementId"] for item in coverage}
    coverage_by_mapping = {item["mappingModuleRef"]: item for item in coverage}

    for statement in coverage:
        key = statement["statementId"]
        reasons: List[str] = []
        lossmap = loss_by_id.get(statement["lossMapRef"])
        if not lossmap:
            reasons.append("lossMapRef does not resolve to a known LossMap example")
        elif lossmap["mappingCoverageStatementRef"] != key:
            reasons.append("LossMap back-reference does not match statementId")
        status = "PASS" if not reasons else "FAIL"
        result["mappingCoverageLossConsistency"][key] = {"status": status, "reasons": reasons}
        if status == "FAIL":
            result["overall"] = "FAIL"

        reasons = []
        for ref in statement.get("runtimeSurfaceContractRefs", []):
            if ref not in contract_by_id:
                reasons.append(f"runtimeSurfaceContractRef missing: {ref}")
        status = "PASS" if not reasons else "FAIL"
        result["runtimeSurfaceReferences"][key] = {"status": status, "reasons": reasons}
        if status == "FAIL":
            result["overall"] = "FAIL"

        reasons = []
        posture = statement["promotionPosture"]
        if posture.get("autoPromotionAllowed"):
            reasons.append("autoPromotionAllowed must remain false in the promoted horizontal examples")
        if statement["direction"] in {"IMPORT", "BIDIRECTIONAL"} and not posture.get("requiresReviewForAcceptedConsequences", False):
            reasons.append("import or bidirectional example should require review for accepted consequences")
        status = "PASS" if not reasons else "FAIL"
        result["promotionPostureChecks"][key] = {"status": status, "reasons": reasons}
        if status == "FAIL":
            result["overall"] = "FAIL"

    manifest_reasons: List[str] = []
    reg = manifest["registryRelation"]
    if reg.get("semanticSubstrateBundleRef") != substrate["bundleId"]:
        manifest_reasons.append("semanticSubstrateBundleRef does not match promoted substrate bundle example")
    claimset = claimset_by_id.get(reg.get("conformanceClaimSetRef"))
    if not claimset:
        manifest_reasons.append("conformanceClaimSetRef does not resolve to a promoted ConformanceClaimSet example")
    elif claimset.get("activeArtifactSetRef") != reg.get("activeArtifactSetRef"):
        manifest_reasons.append("ConformanceClaimSet activeArtifactSetRef does not match manifest activeArtifactSetRef")
    for surface in manifest["capabilitySections"]["importExportSupport"]["declaredSurfaces"]:
        contract_ref = surface.get("contractRef")
        if contract_ref and contract_ref not in contract_by_id:
            manifest_reasons.append(f"manifest contractRef missing promoted runtime surface: {contract_ref}")
        coverage_ref = surface.get("coverageStatementRef")
        if coverage_ref and coverage_ref not in coverage_ids:
            manifest_reasons.append(f"manifest coverageStatementRef missing promoted mapping coverage statement: {coverage_ref}")
        loss_ref = surface.get("lossMapRef")
        if loss_ref and loss_ref not in loss_by_id:
            manifest_reasons.append(f"manifest lossMapRef missing promoted LossMap: {loss_ref}")
    manifest_status = "PASS" if not manifest_reasons else "FAIL"
    result["manifestReferenceConsistency"][manifest["manifestId"]] = {"status": manifest_status, "reasons": manifest_reasons}
    if manifest_status == "FAIL":
        result["overall"] = "FAIL"

    for claimset in claimsets:
        reasons: List[str] = []
        for claim in claimset["claims"]:
            if claim["claimFamily"] == "SEMANTIC_SUBSTRATE" and claim["targetRef"] != substrate["bundleId"]:
                reasons.append(f"semantic substrate claim target not grounded in promoted substrate bundle: {claim['targetRef']}")
            if claim["claimFamily"] == "MAPPING":
                if claim["targetRef"] not in coverage_by_mapping:
                    reasons.append(f"mapping claim target missing promoted coverage example: {claim['targetRef']}")
                for ev in claim.get("evidenceRefs", []):
                    if ev.startswith("mapping-coverage:") and ev not in coverage_ids:
                        reasons.append(f"mapping claim evidence missing promoted mapping coverage statement: {ev}")
                    if ev.startswith("lossmap:") and ev not in loss_by_id:
                        reasons.append(f"mapping claim evidence missing promoted loss map: {ev}")
            if claim["claimFamily"] == "RUNTIME_SURFACE" and claim["targetRef"] not in contract_by_id:
                reasons.append(f"runtime-surface claim target missing promoted runtime surface contract: {claim['targetRef']}")
        status = "PASS" if not reasons else "FAIL"
        result["claimSetConsistency"][claimset["claimSetId"]] = {"status": status, "reasons": reasons}
        if status == "FAIL":
            result["overall"] = "FAIL"

    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(OUT)
    print(result["overall"])
    return 0 if result["overall"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
