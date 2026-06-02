#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Dict, List

try:
    import jsonschema
except ImportError as e:
    raise SystemExit("jsonschema is required for this runner") from e

ROOT = Path(__file__).resolve().parents[1]
MC = ROOT / "03_machine_contracts"
OUT = Path(__file__).resolve().parent / "OFARM_alias_governance_fixture_results_v0_1.json"

CATALOG_SCHEMA = json.loads((MC / "OFARM_SemanticPathAliasCatalog_schema_v0_1.json").read_text(encoding="utf-8"))
TRACE_SCHEMA = json.loads((MC / "OFARM_SemanticPathAliasResolutionTrace_schema_v0_1.json").read_text(encoding="utf-8"))
QUERY_SCHEMA = json.loads((MC / "OFARM_QuerySpecification_schema_v0_1.json").read_text(encoding="utf-8"))
PLAN_SCHEMA = json.loads((MC / "OFARM_QueryPlanIR_schema_v0_1.json").read_text(encoding="utf-8"))

FILES = {
    "catalog_core": "OFARM_SemanticPathAliasCatalog_example_core_profile_v0_1.json",
    "catalog_conflict": "OFARM_SemanticPathAliasCatalog_example_conflict_cropstage_v0_1.json",
    "query_active": "OFARM_QuerySpecification_example_field_passport_v0_1.json",
    "query_legacy": "OFARM_QuerySpecification_example_field_passport_legacy_alias_v0_1.json",
    "query_unpinned": "OFARM_QuerySpecification_example_field_passport_unpinned_alias_v0_1.json",
    "trace_active": "OFARM_SemanticPathAliasResolutionTrace_example_field_passport_active_v0_1.json",
    "trace_deprecated": "OFARM_SemanticPathAliasResolutionTrace_example_field_passport_deprecated_rollover_v0_1.json",
    "trace_ambiguous": "OFARM_SemanticPathAliasResolutionTrace_example_field_passport_ambiguous_fail_v0_1.json",
    "plan_base": "OFARM_QueryPlanIR_example_field_passport_v0_1.json",
    "plan_alt": "OFARM_QueryPlanIR_example_field_passport_search_target_v0_1.json",
}


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def expect(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate(payload: Dict[str, Any], schema: Dict[str, Any]) -> None:
    jsonschema.validate(payload, schema)


def root_concept_ref(query: Dict[str, Any], root_var: str) -> str:
    for section in (query.get("anchors", []), query.get("graphPattern", {}).get("nodes", [])):
        for item in section:
            if item.get("var") == root_var and item.get("conceptRef"):
                return item["conceptRef"]
    raise AssertionError(f"No root concept found for {root_var}")


def first_alias(query: Dict[str, Any]) -> Dict[str, Any]:
    aliases = query.get("semanticPathAliases", [])
    expect(len(aliases) >= 1, "Query must contain at least one semanticPathAlias")
    return aliases[0]


def find_catalog_entry(catalog: Dict[str, Any], version_ref: str) -> Dict[str, Any]:
    for entry in catalog.get("entries", []):
        if entry.get("aliasVersionRef") == version_ref:
            return entry
    raise AssertionError(f"Catalog entry not found for {version_ref}")


def matching_candidates(catalog: Dict[str, Any], alias_name: str, root_concept: str, path_ref: str) -> List[Dict[str, Any]]:
    return [
        entry for entry in catalog.get("entries", [])
        if entry.get("status") == "ACTIVE"
        and entry.get("aliasName") == alias_name
        and entry.get("rootConceptRef") == root_concept
        and entry.get("pathRef") == path_ref
    ]


def alias_projection(plan: Dict[str, Any]) -> List[tuple]:
    return sorted(
        (
            entry.get("alias"),
            entry.get("rootVar"),
            entry.get("pathRef"),
            entry.get("resolvedRef"),
            entry.get("resolutionVersionRef"),
        )
        for entry in plan.get("resolvedPathAliases", [])
    )


def check_active(core_catalog: Dict[str, Any], query: Dict[str, Any], trace: Dict[str, Any]) -> Dict[str, Any]:
    alias = first_alias(query)
    requested = alias.get("aliasVersionRef")
    expect(requested is not None, "Active query fixture must be version-pinned")
    catalog_entry = find_catalog_entry(core_catalog, requested)
    resolution = trace["aliasResolutions"][0]
    expect(catalog_entry.get("status") == "ACTIVE", "Active fixture must resolve to an active catalog entry")
    expect(trace.get("overallOutcome") == "PASS", "Active trace must pass")
    expect(resolution.get("outcome") == "RESOLVED", "Active trace must resolve directly")
    expect(resolution.get("matchedCatalogAliasVersionRef") == requested, "Matched alias version must equal requested alias version")
    expect(resolution.get("canonicalAliasVersionRef") == requested, "Canonical alias version must equal requested alias version")
    expect(resolution.get("resolvedRef") == catalog_entry.get("resolvedRef"), "Resolved target must match catalog entry")
    return {"status": "PASS", "canonicalAliasVersionRef": requested}


def check_deprecated(core_catalog: Dict[str, Any], query: Dict[str, Any], trace: Dict[str, Any]) -> Dict[str, Any]:
    alias = first_alias(query)
    requested = alias.get("aliasVersionRef")
    expect(requested is not None, "Deprecated fixture must remain explicitly version-pinned")
    catalog_entry = find_catalog_entry(core_catalog, requested)
    successor = catalog_entry.get("supersededByAliasVersionRef")
    resolution = trace["aliasResolutions"][0]
    expect(catalog_entry.get("status") == "DEPRECATED", "Deprecated fixture must target a deprecated catalog entry")
    expect(successor is not None, "Deprecated fixture must declare a canonical successor")
    expect(trace.get("overallOutcome") == "PASS", "Deprecated rollover trace must still pass")
    expect(resolution.get("outcome") == "RESOLVED_WITH_DEPRECATION", "Deprecated fixture must resolve with deprecation")
    expect(resolution.get("matchedCatalogAliasVersionRef") == requested, "Matched deprecated version must equal query version")
    expect(resolution.get("canonicalAliasVersionRef") == successor, "Canonical successor must come from catalog supersession")
    expect("DEPRECATED_ALIAS_VERSION" in resolution.get("warnings", []), "Deprecated rollover must retain deprecation warning")
    expect("CANONICAL_SUCCESSOR_APPLIED" in resolution.get("warnings", []), "Deprecated rollover must retain successor warning")
    successor_entry = find_catalog_entry(core_catalog, successor)
    expect(resolution.get("resolvedRef") == successor_entry.get("resolvedRef"), "Deprecated rollover must land on successor semantic target")
    expect(resolution.get("semanticEquivalenceGroupRef") == successor_entry.get("semanticEquivalenceGroupRef"), "Deprecated rollover must preserve semantic equivalence group")
    return {"status": "PASS", "canonicalAliasVersionRef": successor}


def check_ambiguous(conflict_catalog: Dict[str, Any], query: Dict[str, Any], trace: Dict[str, Any]) -> Dict[str, Any]:
    alias = first_alias(query)
    expect(alias.get("aliasVersionRef") is None, "Ambiguity fixture must be unpinned")
    root_concept = root_concept_ref(query, alias["rootVar"])
    candidates = matching_candidates(conflict_catalog, alias["alias"], root_concept, alias["pathRef"])
    resolution = trace["aliasResolutions"][0]
    expect(len(candidates) > 1, "Ambiguity fixture must have multiple active candidates")
    expect(trace.get("overallOutcome") == "FAIL", "Ambiguity trace must fail")
    expect(resolution.get("outcome") == "AMBIGUOUS_FAIL", "Ambiguity fixture must hard-fail")
    expect(set(resolution.get("ambiguityCandidateAliasVersionRefs", [])) == {entry["aliasVersionRef"] for entry in candidates}, "Ambiguity candidates must match active catalog candidates")
    return {"status": "PASS", "candidateCount": len(candidates)}


def check_cross_target_equivalence(base_plan: Dict[str, Any], alt_plan: Dict[str, Any], canonical_alias_version: str) -> Dict[str, Any]:
    expect(base_plan.get("sourceQuerySpecificationId") == alt_plan.get("sourceQuerySpecificationId"), "Equivalent plans must come from the same source query")
    expect(base_plan.get("normalizedTarget") == alt_plan.get("normalizedTarget"), "Equivalent plans must share normalized target")
    expect(base_plan.get("outputAssembly") == alt_plan.get("outputAssembly"), "Equivalent plans must share output assembly")
    expect(base_plan.get("equivalenceRequirements", {}).get("semanticEquivalenceRequired") is True, "Base plan must require semantic equivalence")
    expect(alt_plan.get("equivalenceRequirements", {}).get("semanticEquivalenceRequired") is True, "Alt plan must require semantic equivalence")
    expect(alias_projection(base_plan) == alias_projection(alt_plan), "Equivalent plans must preserve canonical alias projection")
    expect(all(entry[4] == canonical_alias_version for entry in alias_projection(base_plan)), "Base plan alias version must match canonical alias version")
    expect(all(entry[4] == canonical_alias_version for entry in alias_projection(alt_plan)), "Alt plan alias version must match canonical alias version")
    expect(base_plan.get("executionSteps") != alt_plan.get("executionSteps"), "Equivalent plans must differ in execution strategy")
    return {
        "status": "PASS",
        "classification": "SEMANTIC_EQUIVALENCE_FIXTURE",
        "executionTargets": sorted({step.get("executorType") for step in base_plan.get("executionSteps", [])} | {step.get("executorType") for step in alt_plan.get("executionSteps", [])})
    }


def main() -> int:
    result: Dict[str, Any] = {"schemaValidation": {}, "fixtureResults": {}, "overall": "PASS"}
    payloads = {name: load_json(MC / filename) for name, filename in FILES.items()}

    validations = {
        "catalog_core": (payloads["catalog_core"], CATALOG_SCHEMA),
        "catalog_conflict": (payloads["catalog_conflict"], CATALOG_SCHEMA),
        "query_active": (payloads["query_active"], QUERY_SCHEMA),
        "query_legacy": (payloads["query_legacy"], QUERY_SCHEMA),
        "query_unpinned": (payloads["query_unpinned"], QUERY_SCHEMA),
        "trace_active": (payloads["trace_active"], TRACE_SCHEMA),
        "trace_deprecated": (payloads["trace_deprecated"], TRACE_SCHEMA),
        "trace_ambiguous": (payloads["trace_ambiguous"], TRACE_SCHEMA),
        "plan_base": (payloads["plan_base"], PLAN_SCHEMA),
        "plan_alt": (payloads["plan_alt"], PLAN_SCHEMA),
    }

    for name, (payload, schema) in validations.items():
        try:
            validate(payload, schema)
            result["schemaValidation"][name] = "PASS"
        except Exception as e:
            result["schemaValidation"][name] = f"FAIL: {e}"
            result["overall"] = "FAIL"

    if result["overall"] == "FAIL":
        OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(OUT)
        print(result["overall"])
        return 1

    try:
        active_result = check_active(payloads["catalog_core"], payloads["query_active"], payloads["trace_active"])
        result["fixtureResults"]["active_version_pinned_resolution"] = active_result
    except Exception as e:
        result["fixtureResults"]["active_version_pinned_resolution"] = {"status": "FAIL", "detail": str(e)}
        result["overall"] = "FAIL"
        active_result = {"canonicalAliasVersionRef": None}

    try:
        deprecated_result = check_deprecated(payloads["catalog_core"], payloads["query_legacy"], payloads["trace_deprecated"])
        result["fixtureResults"]["deprecated_rollover"] = deprecated_result
    except Exception as e:
        result["fixtureResults"]["deprecated_rollover"] = {"status": "FAIL", "detail": str(e)}
        result["overall"] = "FAIL"

    try:
        ambiguous_result = check_ambiguous(payloads["catalog_conflict"], payloads["query_unpinned"], payloads["trace_ambiguous"])
        result["fixtureResults"]["ambiguity_hard_fail"] = ambiguous_result
    except Exception as e:
        result["fixtureResults"]["ambiguity_hard_fail"] = {"status": "FAIL", "detail": str(e)}
        result["overall"] = "FAIL"

    try:
        equivalence_result = check_cross_target_equivalence(payloads["plan_base"], payloads["plan_alt"], active_result.get("canonicalAliasVersionRef"))
        result["fixtureResults"]["cross_target_queryplan_equivalence"] = equivalence_result
    except Exception as e:
        result["fixtureResults"]["cross_target_queryplan_equivalence"] = {"status": "FAIL", "detail": str(e)}
        result["overall"] = "FAIL"

    if result["overall"] == "PASS":
        result["overall"] = "PASS_WITH_LIMITATIONS"
        result["notes"] = "Fixture-level alias governance passed. This runner checks cataloged alias resolution, deprecation traceability, ambiguity hard-fail, and starter cross-target QueryPlanIR equivalence, not full runtime execution equivalence."

    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(OUT)
    print(result["overall"])
    return 0 if result["overall"] != "FAIL" else 1


if __name__ == "__main__":
    raise SystemExit(main())
