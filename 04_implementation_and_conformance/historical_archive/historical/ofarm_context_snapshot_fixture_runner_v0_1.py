#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Dict, List

try:
    import jsonschema
except ImportError as e:
    raise SystemExit("jsonschema is required for this validator") from e

ROOT = Path(__file__).resolve().parents[1]
MC = ROOT / "03_machine_contracts"
FIX = Path(__file__).resolve().parent / "ofarm_context_snapshot_fixtures_v0_1"
OUT = Path(__file__).resolve().parent / "OFARM_context_snapshot_fixture_results_v0_1.json"

SCHEMAS = {
    "context": "OFARM_ContextSnapshot_schema_v0_1.json",
    "materializationBasis": "OFARM_MaterializationBasis_schema_v0_1.json",
    "packActivationSet": "OFARM_PackActivationSet_schema_v0_1.json",
    "activeArtifactSet": "OFARM_ActiveArtifactSet_schema_v0_1.json",
    "packMergeResolutionTrace": "OFARM_PackMergeResolutionTrace_schema_v0_1.json",
}

EXAMPLE_GROUPS = {
    "context": [
        "OFARM_ContextSnapshot_example_field_compliance_v0_1.json",
        "OFARM_ContextSnapshot_example_field_compliance_after_orchard_v0_1.json",
    ],
    "materializationBasis": [
        "OFARM_MaterializationBasis_example_field_compliance_v0_1.json",
        "OFARM_MaterializationBasis_example_field_compliance_after_orchard_context_v0_1.json",
    ],
    "packActivationSet": [
        "OFARM_PackActivationSet_example_field_17_compliance_context_v0_1.json",
        "OFARM_PackActivationSet_example_field_17_orchard_context_v0_1.json",
    ],
    "activeArtifactSet": [
        "OFARM_ActiveArtifactSet_example_core_deployment_v0_1.json",
        "OFARM_ActiveArtifactSet_example_core_orchard_deployment_v0_1.json",
    ],
    "packMergeResolutionTrace": [
        "OFARM_PackMergeResolutionTrace_example_field_17_orchard_evidence_merge_v0_1.json",
    ],
}

FIXTURES = [
    "context_snapshot_same_basis_recompute.json",
    "context_snapshot_basis_drift_exploratory.json",
    "context_snapshot_basis_drift_high_consequence.json",
]

MATERIAL_FIELDS = [
    "targetTwin",
    "anchorScopes",
    "evaluationTimePolicy",
    "activeArtifactSetRef",
    "sourcePackActivationSetRefs",
    "activePackRefs",
    "activeProfileRefs",
    "activeScopedExtensionRefs",
    "relevantPrecedenceClasses",
    "governingRuleArtifactRefs",
    "evidencePolicyRefs",
    "referenceSnapshotRefs",
    "identityRevisionRefs",
    "packMergeResolutionTraceRefs",
]


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize(value: Any) -> Any:
    if isinstance(value, list):
        if not value:
            return []
        if all(isinstance(v, dict) for v in value):
            normalized = [normalize(v) for v in value]
            return sorted(normalized, key=lambda item: json.dumps(item, sort_keys=True))
        return sorted(normalize(v) for v in value)
    if isinstance(value, dict):
        return {k: normalize(value[k]) for k in sorted(value)}
    return value


def fingerprint(snapshot: Dict[str, Any]) -> str:
    payload = {}
    for field in MATERIAL_FIELDS:
        default = [] if field.endswith("Refs") or field in {"anchorScopes", "relevantPrecedenceClasses", "activePackRefs", "activeProfileRefs", "activeScopedExtensionRefs"} else None
        payload[field] = normalize(snapshot.get(field, default))
    return json.dumps(payload, sort_keys=True)


def validate_examples() -> Dict[str, str]:
    results: Dict[str, str] = {}
    schemas = {name: load_json(MC / fname) for name, fname in SCHEMAS.items()}
    for key, schema in schemas.items():
        jsonschema.Draft202012Validator.check_schema(schema)
        for example in EXAMPLE_GROUPS[key]:
            data = load_json(MC / example)
            jsonschema.validate(data, schema)
            results[f"{example} :: {SCHEMAS[key]}"] = "PASS"
    return results


def build_indexes() -> Dict[str, Dict[str, Dict[str, Any]]]:
    contexts = {}
    for fname in EXAMPLE_GROUPS["context"]:
        data = load_json(MC / fname)
        contexts[data["contextSnapshotId"]] = data

    bases = {}
    for fname in EXAMPLE_GROUPS["materializationBasis"]:
        data = load_json(MC / fname)
        bases[data["basisId"]] = data

    activation_sets = {}
    for fname in EXAMPLE_GROUPS["packActivationSet"]:
        data = load_json(MC / fname)
        activation_sets[data["packActivationSetId"]] = data

    artifact_sets = {}
    for fname in EXAMPLE_GROUPS["activeArtifactSet"]:
        data = load_json(MC / fname)
        artifact_sets[data["activeArtifactSetId"]] = data

    merge_traces = {}
    for fname in EXAMPLE_GROUPS["packMergeResolutionTrace"]:
        data = load_json(MC / fname)
        merge_traces[data["traceId"]] = data

    return {
        "contexts": contexts,
        "bases": bases,
        "activation_sets": activation_sets,
        "artifact_sets": artifact_sets,
        "merge_traces": merge_traces,
    }


def expect(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


def check_context_grounding(indexes: Dict[str, Dict[str, Dict[str, Any]]]) -> Dict[str, str]:
    results: Dict[str, str] = {}
    contexts = indexes["contexts"]
    activation_sets = indexes["activation_sets"]
    artifact_sets = indexes["artifact_sets"]
    merge_traces = indexes["merge_traces"]

    for context_id, snapshot in contexts.items():
        active_artifact = artifact_sets.get(snapshot["activeArtifactSetRef"])
        expect(active_artifact is not None, f"{context_id} must resolve activeArtifactSetRef")
        for ref in snapshot["sourcePackActivationSetRefs"]:
            expect(ref in activation_sets, f"{context_id} must resolve sourcePackActivationSetRef {ref}")
        for ref in snapshot.get("packMergeResolutionTraceRefs", []):
            expect(ref in merge_traces, f"{context_id} must resolve packMergeResolutionTraceRef {ref}")
            trace = merge_traces[ref]
            expect(trace["packActivationSetRef"] in snapshot["sourcePackActivationSetRefs"], f"{context_id} merge trace must point to one of the snapshot activation sets")

        # Snapshot packs/profiles/extensions must be subsets of active artifact grounding.
        expect(set(snapshot.get("activePackRefs", [])).issubset(set(active_artifact.get("activePackRefs", []))), f"{context_id} packs must be grounded in the active artifact set")
        expect(set(snapshot.get("activeProfileRefs", [])).issubset(set(active_artifact.get("activeProfileRefs", []))), f"{context_id} profiles must be grounded in the active artifact set")
        expect(set(snapshot.get("activeScopedExtensionRefs", [])).issubset(set(active_artifact.get("activeScopedExtensionRefs", []))), f"{context_id} scoped extensions must be grounded in the active artifact set")

        # If one activation set is used, the resolved snapshot subset should align with it.
        if len(snapshot["sourcePackActivationSetRefs"]) == 1:
            activation = activation_sets[snapshot["sourcePackActivationSetRefs"][0]]
            expect(set(snapshot.get("activePackRefs", [])) == set(activation.get("activePackRefs", [])), f"{context_id} packs must align with the resolved activation set")
            expect(set(snapshot.get("activeProfileRefs", [])) == set(activation.get("activeProfileRefs", [])), f"{context_id} profiles must align with the resolved activation set")
            expect(set(snapshot.get("activeScopedExtensionRefs", [])) == set(activation.get("activeScopedExtensionRefs", [])), f"{context_id} scoped extensions must align with the resolved activation set")
        results[context_id] = "PASS"
    return results


def check_basis_resolution(indexes: Dict[str, Dict[str, Dict[str, Any]]]) -> Dict[str, str]:
    results: Dict[str, str] = {}
    contexts = indexes["contexts"]
    bases = indexes["bases"]
    for basis_id, basis in bases.items():
        for ref in basis["contextSnapshotRefs"]:
            expect(ref in contexts, f"{basis_id} must resolve contextSnapshotRef {ref}")
            snapshot = contexts[ref]
            expect(snapshot["targetTwin"] == basis["twin"], f"{basis_id} must align with snapshot twin")
            expect(normalize(snapshot["anchorScopes"]) == normalize(basis["anchorScopes"]), f"{basis_id} must align with snapshot anchorScopes")
            expect(normalize(snapshot["evaluationTimePolicy"]) == normalize(basis["evaluationTimePolicy"]), f"{basis_id} must align with snapshot evaluationTimePolicy")
        results[basis_id] = "PASS"
    return results


def evaluate_fixture(fixture: Dict[str, Any], indexes: Dict[str, Dict[str, Dict[str, Any]]]) -> Dict[str, Any]:
    facts = fixture["facts"]
    bases = indexes["bases"]
    contexts = indexes["contexts"]

    basis = bases[facts["priorMaterializationBasisRef"]]
    expect(facts["priorContextSnapshotRef"] in basis["contextSnapshotRefs"], f"{fixture['fixtureId']} prior context must be referenced by the prior basis")
    prior = contexts[facts["priorContextSnapshotRef"]]
    candidate = contexts[facts["candidateContextSnapshotRef"]]

    same = fingerprint(prior) == fingerprint(candidate)
    if same:
        outcome = {
            "relation": "BASIS_PRESERVING_RECOMPUTE",
            "mustMintNewContextSnapshot": False,
            "priorFreshnessState": "FRESH",
            "mustRecompute": False,
        }
    else:
        use_class = facts.get("useClass", "EXPLORATORY")
        freshness = "INVALID" if use_class == "HIGH_CONSEQUENCE" else "STALE"
        outcome = {
            "relation": "BASIS_DRIFT",
            "mustMintNewContextSnapshot": True,
            "priorFreshnessState": freshness,
            "mustRecompute": True,
        }
    return outcome


def main() -> int:
    result: Dict[str, Any] = {
        "exampleValidation": {},
        "contextGrounding": {},
        "basisResolution": {},
        "fixtureResults": {},
        "overall": "PASS",
    }

    try:
        result["exampleValidation"] = validate_examples()
        indexes = build_indexes()
        result["contextGrounding"] = check_context_grounding(indexes)
        result["basisResolution"] = check_basis_resolution(indexes)
        for fname in FIXTURES:
            fixture = load_json(FIX / fname)
            actual = evaluate_fixture(fixture, indexes)
            expected = fixture["expectedOutcome"]
            status = "PASS" if all(actual.get(k) == v for k, v in expected.items()) else "FAIL"
            payload = {"status": status, "actual": actual, "expected": expected}
            result["fixtureResults"][fixture["fixtureId"]] = payload
            if status == "FAIL":
                result["overall"] = "FAIL"
    except Exception as e:
        result["overall"] = "FAIL"
        result["fatalError"] = str(e)

    if result["overall"] == "PASS":
        result["overall"] = "PASS_WITH_LIMITATIONS"
        result["notes"] = "Fixture-level context/basis coverage passed. This runner checks context grounding and basis-drift semantics, not full materialization runtime generation."

    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(OUT)
    print(result["overall"])
    return 0 if result["overall"] != "FAIL" else 1

if __name__ == "__main__":
    raise SystemExit(main())
