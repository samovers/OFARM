#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Dict

try:
    import jsonschema
except ImportError as e:
    raise SystemExit("jsonschema is required for this runner") from e

ROOT = Path(__file__).resolve().parents[1]
MC = ROOT / "03_machine_contracts"
OUT = Path(__file__).resolve().parent / "OFARM_lot_traceability_fixture_results_v0_1.json"

LINEAGE_SCHEMA = json.loads((MC / "OFARM_LotLineageChange_schema_v0_1.json").read_text(encoding="utf-8"))
CLAIM_SCHEMA = json.loads((MC / "OFARM_TraceabilityClaimBasis_schema_v0_1.json").read_text(encoding="utf-8"))

CLAIM_FILES = {
    "identity_preserved": "OFARM_TraceabilityClaimBasis_example_identity_preserved_v0_1.json",
    "mass_balance": "OFARM_TraceabilityClaimBasis_example_mass_balance_v0_1.json",
}

FIXTURE_FILES = {
    "split": "OFARM_LotLineageChange_example_split_v0_1.json",
    "merge_commingle": "OFARM_LotLineageChange_example_merge_commingle_v0_1.json",
    "transform": "OFARM_LotLineageChange_example_transform_v0_1.json",
    "shipment_reference": "OFARM_LotLineageChange_example_shipment_reference_v0_1.json",
    "claim_basis_reset": "OFARM_LotLineageChange_example_claim_basis_reset_v0_1.json",
}


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def expect(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate_claim_basis(data: Dict[str, Any]) -> None:
    jsonschema.validate(data, CLAIM_SCHEMA)


def validate_lineage_payload(data: Dict[str, Any]) -> None:
    jsonschema.validate(data, LINEAGE_SCHEMA)


def check_split(data: Dict[str, Any]) -> None:
    expect(data["changeType"] == "SPLIT", "split fixture must declare SPLIT")
    expect(data["continuityOutcome"] == "NEW_LOT_REQUIRED", "split fixture must require new lots")
    expect(len(data.get("predecessorLotRefs", [])) == 1, "split fixture must have one predecessor")
    expect(len(data.get("successorLotRefs", [])) >= 2, "split fixture must have two or more successors")
    edges = data.get("lineageEdges", [])
    expect(len(edges) == len(data.get("successorLotRefs", [])), "split fixture must declare one edge per successor")
    expect(all(edge.get("relationOnTarget") == "splitFrom" for edge in edges), "split fixture lineage edges must use splitFrom")


def check_merge_commingle(data: Dict[str, Any]) -> None:
    expect(data["changeType"] == "COMMINGLE", "merge/commingle fixture must declare COMMINGLE")
    expect(data["continuityOutcome"] == "NEW_LOT_REQUIRED", "commingle fixture must require new lot")
    expect(len(data.get("predecessorLotRefs", [])) >= 2, "commingle fixture must have multiple predecessors")
    expect(len(data.get("successorLotRefs", [])) == 1, "commingle fixture must have one successor")
    edges = data.get("lineageEdges", [])
    expect(len(edges) == len(data.get("predecessorLotRefs", [])), "commingle fixture must declare one edge per predecessor")
    expect(all(edge.get("relationOnTarget") == "mergedFrom" for edge in edges), "commingle fixture lineage edges must use mergedFrom")
    expect(data.get("preChangeClaimBasisRef") != data.get("postChangeClaimBasisRef"), "commingle fixture must surface claim-basis transition")


def check_transform(data: Dict[str, Any]) -> None:
    expect(data["changeType"] == "TRANSFORM", "transform fixture must declare TRANSFORM")
    expect(data["continuityOutcome"] == "NEW_LOT_REQUIRED", "transform fixture must require new lot")
    expect(len(data.get("predecessorLotRefs", [])) == 1, "transform fixture must have one predecessor")
    expect(len(data.get("successorLotRefs", [])) == 1, "transform fixture must have one successor")
    edges = data.get("lineageEdges", [])
    expect(len(edges) == 1 and edges[0].get("relationOnTarget") == "derivedFrom", "transform fixture must use derivedFrom")


def check_shipment_reference(data: Dict[str, Any]) -> None:
    expect(data["changeType"] == "SHIPMENT_REFERENCE_ATTACH", "shipment fixture must declare SHIPMENT_REFERENCE_ATTACH")
    expect(data["continuityOutcome"] == "SAME_LOT_CONTINUES", "shipment fixture must keep same lot")
    expect(len(data.get("subjectLotRefs", [])) == 1, "shipment fixture must point to one subject lot")
    expect(len(data.get("shipmentReferenceRefs", [])) >= 1, "shipment fixture must attach shipment references")
    expect(data.get("preChangeClaimBasisRef") == data.get("postChangeClaimBasisRef"), "shipment fixture must not silently change claim basis")


def check_claim_basis_reset(data: Dict[str, Any]) -> None:
    expect(data["changeType"] == "CLAIM_BASIS_RESET", "claim-basis reset fixture must declare CLAIM_BASIS_RESET")
    expect(data["continuityOutcome"] == "NEW_LOT_REQUIRED", "claim-basis reset fixture must require new lot")
    expect(len(data.get("predecessorLotRefs", [])) == 1, "claim-basis reset fixture must have one predecessor")
    expect(len(data.get("successorLotRefs", [])) == 1, "claim-basis reset fixture must have one successor")
    expect(data.get("preChangeClaimBasisRef") != data.get("postChangeClaimBasisRef"), "claim-basis reset fixture must change claim basis")
    edges = data.get("lineageEdges", [])
    expect(len(edges) == 1 and edges[0].get("relationOnTarget") == "derivedFrom", "claim-basis reset fixture must preserve derivation lineage")


def main() -> int:
    result: Dict[str, Any] = {"schemaValidation": {}, "fixtureResults": {}, "overall": "PASS"}

    claims = {name: load_json(MC / fname) for name, fname in CLAIM_FILES.items()}
    for name, payload in claims.items():
        key = f"claim::{name}"
        try:
            validate_claim_basis(payload)
            result["schemaValidation"][key] = "PASS"
        except Exception as e:
            result["schemaValidation"][key] = f"FAIL: {e}"
            result["overall"] = "FAIL"

    fixtures = {name: load_json(MC / fname) for name, fname in FIXTURE_FILES.items()}
    checkers = {
        "split": check_split,
        "merge_commingle": check_merge_commingle,
        "transform": check_transform,
        "shipment_reference": check_shipment_reference,
        "claim_basis_reset": check_claim_basis_reset,
    }

    for name, payload in fixtures.items():
        try:
            validate_lineage_payload(payload)
            checkers[name](payload)
            result["fixtureResults"][name] = {"status": "PASS"}
        except Exception as e:
            result["fixtureResults"][name] = {"status": "FAIL", "detail": str(e)}
            result["overall"] = "FAIL"

    if result["overall"] == "PASS":
        result["overall"] = "PASS_WITH_LIMITATIONS"
        result["notes"] = "Fixture-level coverage passed. This runner checks narrow lot boundary semantics, not full event-to-promotion runtime integration."

    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(OUT)
    print(result["overall"])
    return 0 if result["overall"] != "FAIL" else 1

if __name__ == "__main__":
    raise SystemExit(main())
