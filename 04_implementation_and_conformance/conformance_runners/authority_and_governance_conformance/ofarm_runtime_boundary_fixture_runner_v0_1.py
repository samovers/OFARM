#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Dict

try:
    import jsonschema
except ImportError as e:
    raise SystemExit("jsonschema is required for this validator") from e

ROOT = Path(__file__).resolve().parents[1]
MC = ROOT / "03_machine_contracts"
FIX = Path(__file__).resolve().parent / "ofarm_runtime_boundary_fixtures_v0_1"
OUT = Path(__file__).resolve().parent / "OFARM_runtime_boundary_fixture_results_v0_1.json"

SCHEMA_FILES = {
    "auth_request": "OFARM_AuthorizationDecisionRequest_schema_v0_1.json",
    "auth_result": "OFARM_AuthorizationDecisionResult_schema_v0_1.json",
    "auth_trace": "OFARM_AuthorizationDecisionTrace_schema_v0_1.json",
    "materialization_request": "OFARM_MaterializationRequest_schema_v0_1.json",
    "materialization_result": "OFARM_MaterializationResult_schema_v0_1.json",
    "query_request": "OFARM_QueryExecutionRequest_schema_v0_1.json",
    "query_result": "OFARM_QueryExecutionResult_schema_v0_1.json",
    "publication_request": "OFARM_PublicationAssemblyRequest_schema_v0_1.json",
    "publication_result": "OFARM_PublicationAssemblyResult_schema_v0_1.json",
    "passport_metadata": "OFARM_PassportViewMetadata_schema_v0_1.json",
    "document_metadata": "OFARM_DocumentAssemblyMetadata_schema_v0_1.json",
    "alias_trace": "OFARM_SemanticPathAliasResolutionTrace_schema_v0_1.json",
}

FIXTURES = sorted([p.name for p in FIX.glob("*.json")])


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def expect(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


def normalize(value: Any) -> Any:
    if isinstance(value, list):
        return sorted([normalize(v) for v in value], key=lambda x: json.dumps(x, sort_keys=True))
    if isinstance(value, dict):
        return {k: normalize(value[k]) for k in sorted(value)}
    return value


def schema_key_for_example(name: str) -> str:
    if name.startswith("OFARM_AuthorizationDecisionRequest_"):
        return "auth_request"
    if name.startswith("OFARM_AuthorizationDecisionResult_"):
        return "auth_result"
    if name.startswith("OFARM_AuthorizationDecisionTrace_"):
        return "auth_trace"
    if name.startswith("OFARM_MaterializationRequest_"):
        return "materialization_request"
    if name.startswith("OFARM_MaterializationResult_"):
        return "materialization_result"
    if name.startswith("OFARM_QueryExecutionRequest_"):
        return "query_request"
    if name.startswith("OFARM_QueryExecutionResult_"):
        return "query_result"
    if name.startswith("OFARM_PublicationAssemblyRequest_"):
        return "publication_request"
    if name.startswith("OFARM_PublicationAssemblyResult_"):
        return "publication_result"
    if name.startswith("OFARM_PassportViewMetadata_"):
        return "passport_metadata"
    if name.startswith("OFARM_DocumentAssemblyMetadata_"):
        return "document_metadata"
    if name.startswith("OFARM_SemanticPathAliasResolutionTrace_"):
        return "alias_trace"
    raise KeyError(f"Unknown schema mapping for {name}")


def validate_file(example_name: str, schemas: Dict[str, Dict[str, Any]]) -> None:
    key = schema_key_for_example(example_name)
    jsonschema.validate(load_json(MC / example_name), schemas[key])


def scope_of(item: Dict[str, Any]) -> Any:
    if "target" in item and "scope" in item["target"]:
        return normalize(item["target"]["scope"])
    if "anchorScope" in item:
        return normalize(item["anchorScope"])
    if "anchorScopes" in item:
        return normalize(item["anchorScopes"])
    if "targetScopes" in item:
        return normalize(item["targetScopes"])
    return None


def check_auth_pair(fixture: Dict[str, Any], schemas: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    request = load_json(MC / fixture["requestExample"])
    result = load_json(MC / fixture["resultExample"])
    trace = load_json(MC / fixture["traceExample"])
    for name in [fixture["requestExample"], fixture["resultExample"], fixture["traceExample"]]:
        validate_file(name, schemas)

    expect(result["requestId"] == request["requestId"], f"{fixture['fixtureId']} requestId mismatch")
    expect(result["requestedActionClass"] == request["actionClass"], f"{fixture['fixtureId']} action class mismatch")
    expect(result["actionStage"] == request["actionStage"], f"{fixture['fixtureId']} action stage mismatch")
    expect(trace["traceId"] == result["authorizationDecisionTraceRef"], f"{fixture['fixtureId']} trace ref mismatch")
    expect(trace["requestedActionClass"] == request["actionClass"], f"{fixture['fixtureId']} trace action mismatch")
    expect(trace["decisionOutcome"] == result["decisionOutcome"], f"{fixture['fixtureId']} trace outcome mismatch")
    expect(normalize(trace["target"]["scope"]) == normalize(request["target"]["scope"]), f"{fixture['fixtureId']} scope mismatch")
    expect(result["decisionOutcome"] == fixture["expectedOutcome"], f"{fixture['fixtureId']} expected outcome mismatch")
    expect(result["inheritanceModeApplied"] == fixture["expectedInheritanceMode"], f"{fixture['fixtureId']} inheritance mismatch")
    if "expectedRevocationResult" in fixture:
        expect(result["revocationResult"] == fixture["expectedRevocationResult"], f"{fixture['fixtureId']} revocation mismatch")
        expect(trace["revocationResult"] == fixture["expectedRevocationResult"], f"{fixture['fixtureId']} trace revocation mismatch")
    if fixture.get("expectDelegation"):
        expect(len(result["delegationBasisUsed"]) > 0, f"{fixture['fixtureId']} expected delegation basis")
        expect(len(trace.get("delegationBasisUsed", [])) > 0, f"{fixture['fixtureId']} expected delegation in trace")
    else:
        expect(len(result["delegationBasisUsed"]) == 0, f"{fixture['fixtureId']} unexpected delegation basis")
    if request.get("aiAssistance", {}).get("assisted"):
        expect(result["decisionOutcome"] == "REQUIRE_HUMAN_APPROVAL", f"{fixture['fixtureId']} AI-assisted path must require human approval here")
        expect(result["humanApprovalRequired"] is True, f"{fixture['fixtureId']} AI-assisted path must set humanApprovalRequired")
    if request.get("nonHumanActor"):
        expect(result["decisionOutcome"] != "ALLOW", f"{fixture['fixtureId']} non-human path must not allow this human-only action")
    return {
        "status": "PASS",
        "decisionOutcome": result["decisionOutcome"],
        "revocationResult": result["revocationResult"],
        "inheritanceModeApplied": result["inheritanceModeApplied"],
    }


def check_auth_read_write_pair(fixture: Dict[str, Any], schemas: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    read_request = load_json(MC / fixture["readRequestExample"])
    read_result = load_json(MC / fixture["readResultExample"])
    read_trace = load_json(MC / fixture["readTraceExample"])
    write_request = load_json(MC / fixture["writeRequestExample"])
    write_result = load_json(MC / fixture["writeResultExample"])
    write_trace = load_json(MC / fixture["writeTraceExample"])
    for name in [
        fixture["readRequestExample"], fixture["readResultExample"], fixture["readTraceExample"],
        fixture["writeRequestExample"], fixture["writeResultExample"], fixture["writeTraceExample"]
    ]:
        validate_file(name, schemas)

    shared_grant = fixture["sharedGrantRef"]
    expect(read_result["decisionOutcome"] == "ALLOW", f"{fixture['fixtureId']} read must allow")
    expect(write_result["decisionOutcome"] == "DENY", f"{fixture['fixtureId']} write must deny")
    expect(shared_grant in read_result["sharingBasisUsed"], f"{fixture['fixtureId']} read must use sharing grant")
    expect(shared_grant in write_result["sharingBasisUsed"], f"{fixture['fixtureId']} write denial should still explain sharing basis")
    expect(read_request["target"]["targetKind"] == "PASSPORT_VIEW", f"{fixture['fixtureId']} read target kind mismatch")
    expect(write_request["target"]["targetKind"] == "CANONICAL_TRUTH", f"{fixture['fixtureId']} write target kind mismatch")
    expect(read_trace["decisionOutcome"] == "ALLOW", f"{fixture['fixtureId']} read trace mismatch")
    expect(write_trace["decisionOutcome"] == "DENY", f"{fixture['fixtureId']} write trace mismatch")
    return {
        "status": "PASS",
        "readOutcome": read_result["decisionOutcome"],
        "writeOutcome": write_result["decisionOutcome"],
        "sharedGrantRef": shared_grant,
    }


def check_materialization_pair(fixture: Dict[str, Any], schemas: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    pair_results = []
    for pair in fixture["pairs"]:
        request = load_json(MC / pair["requestExample"])
        result = load_json(MC / pair["resultExample"])
        validate_file(pair["requestExample"], schemas)
        validate_file(pair["resultExample"], schemas)

        expect(result["requestId"] == request["requestId"], f"{fixture['fixtureId']} requestId mismatch for {pair['requestExample']}")
        expect(result["targetTwin"] == request["targetTwin"], f"{fixture['fixtureId']} twin mismatch")
        expect(normalize(result["anchorScopes"]) == normalize(request["anchorScopes"]), f"{fixture['fixtureId']} scope mismatch")
        expect(result["requiredFreshness"] == request["requiredFreshness"], f"{fixture['fixtureId']} requiredFreshness mismatch")
        expect(result["highConsequenceUse"] == request["highConsequenceUse"], f"{fixture['fixtureId']} highConsequenceUse mismatch")
        expect(result["decisionOutcome"] == pair["expectedDecision"], f"{fixture['fixtureId']} decision mismatch")
        expect(result["freshnessState"] == pair["expectedFreshness"], f"{fixture['fixtureId']} freshness mismatch")
        pair_results.append({
            "request": pair["requestExample"],
            "decisionOutcome": result["decisionOutcome"],
            "freshnessState": result["freshnessState"],
            "targetTwin": result["targetTwin"],
        })

    has_advisory_stale = any(p["targetTwin"] == "ADVISORY" and p["freshnessState"] == "STALE" and p["decisionOutcome"] == "ALLOW_REUSE" for p in pair_results)
    has_invalid_refusal = any(p["freshnessState"] == "INVALID" and p["decisionOutcome"] == "REFUSE_USE" for p in pair_results)
    expect(has_advisory_stale, f"{fixture['fixtureId']} must include advisory stale allow-reuse case")
    expect(has_invalid_refusal, f"{fixture['fixtureId']} must include invalid refusal case")
    return {"status":"PASS","pairs":pair_results}


def check_query_pair(fixture: Dict[str, Any], schemas: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    request = load_json(MC / fixture["requestExample"])
    result = load_json(MC / fixture["resultExample"])
    alias_trace = load_json(MC / fixture["aliasTraceExample"])
    for name in [fixture["requestExample"], fixture["resultExample"], fixture["aliasTraceExample"]]:
        validate_file(name, schemas)

    expect(result["querySpecificationRef"] == request["querySpecificationRef"], f"{fixture['fixtureId']} querySpecificationRef mismatch")
    expect(result["queryPlanRef"] == request["queryPlanRef"], f"{fixture['fixtureId']} queryPlanRef mismatch")
    expect(alias_trace["sourceQuerySpecificationId"] == request["querySpecificationRef"], f"{fixture['fixtureId']} alias trace query mismatch")
    expect(alias_trace["traceId"] in request["aliasResolutionTraceRefs"], f"{fixture['fixtureId']} request missing alias trace")
    expect(alias_trace["traceId"] in result["aliasResolutionTraceRefs"], f"{fixture['fixtureId']} result missing alias trace")
    expect(result["outcome"] == "SUCCESS", f"{fixture['fixtureId']} query should succeed")
    expect(result["projectionTraceBackReady"] is True, f"{fixture['fixtureId']} projection trace-back must be ready")
    return {"status":"PASS","outcome":result["outcome"],"resultShape":result["resultShape"]}


def check_publication_boundary(fixture: Dict[str, Any], schemas: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    passport_meta = load_json(MC / fixture["passportMetadataExample"])
    doc_meta = load_json(MC / fixture["documentMetadataExample"])
    pass_req = load_json(MC / fixture["passportPublishRequestExample"])
    pass_res = load_json(MC / fixture["passportPublishResultExample"])
    deny_req = load_json(MC / fixture["passportAttestRequestExample"])
    deny_res = load_json(MC / fixture["passportAttestResultExample"])
    sub_req = load_json(MC / fixture["submissionRequestExample"])
    sub_res = load_json(MC / fixture["submissionResultExample"])
    for name in [
        fixture["passportMetadataExample"], fixture["documentMetadataExample"],
        fixture["passportPublishRequestExample"], fixture["passportPublishResultExample"],
        fixture["passportAttestRequestExample"], fixture["passportAttestResultExample"],
        fixture["submissionRequestExample"], fixture["submissionResultExample"],
    ]:
        validate_file(name, schemas)

    expect(passport_meta["freezeState"] == "LIVE_RECOMPUTABLE", f"{fixture['fixtureId']} passport must remain live/recomputable")
    expect(doc_meta["documentFamily"] == "SUBMISSION_ASSEMBLY", f"{fixture['fixtureId']} document metadata must be submission assembly")
    expect(pass_req["outputKind"] == "PASSPORT_VIEW" and pass_res["outcome"] == "PUBLISHED", f"{fixture['fixtureId']} passport publish mismatch")
    expect(deny_req["outputKind"] == "PASSPORT_VIEW" and deny_res["outcome"] == "DENIED", f"{fixture['fixtureId']} passport attestation denial mismatch")
    expect(sub_req["outputKind"] == "SUBMISSION_ASSEMBLY" and sub_res["outcome"] == "FILED", f"{fixture['fixtureId']} submission filing mismatch")
    expect(sub_res.get("evidenceSufficiencyCaseRef"), f"{fixture['fixtureId']} submission filing must carry evidence sufficiency ref")
    expect(sub_res.get("authorizationDecisionTraceRef"), f"{fixture['fixtureId']} submission filing must carry authorization trace ref")
    expect(pass_res["outputMetadataRef"] == passport_meta["passportViewId"], f"{fixture['fixtureId']} passport metadata ref mismatch")
    expect(sub_res["outputMetadataRef"] == doc_meta["documentAssemblyId"], f"{fixture['fixtureId']} document metadata ref mismatch")
    return {
        "status":"PASS",
        "passportOutcome": pass_res["outcome"],
        "passportAttestationOutcome": deny_res["outcome"],
        "submissionOutcome": sub_res["outcome"],
    }


def main() -> int:
    result: Dict[str, Any] = {
        "exampleValidation": {},
        "fixtureResults": {},
        "overall": "PASS",
    }
    try:
        schemas = {k: load_json(MC / v) for k, v in SCHEMA_FILES.items()}
        for schema in schemas.values():
            jsonschema.Draft202012Validator.check_schema(schema)

        validated = set()
        for fixture_name in FIXTURES:
            fixture = load_json(FIX / fixture_name)
            # validate referenced examples once and record pass
            names_to_validate = []
            for key, value in fixture.items():
                if key.endswith("Example") and isinstance(value, str):
                    names_to_validate.append(value)
                elif key == "pairs":
                    for pair in value:
                        names_to_validate.extend([pair["requestExample"], pair["resultExample"]])
            for name in names_to_validate:
                if name not in validated:
                    validate_file(name, schemas)
                    result["exampleValidation"][name] = "PASS"
                    validated.add(name)

            if fixture["fixtureType"] == "AUTHORIZATION_PAIR":
                fixture_result = check_auth_pair(fixture, schemas)
            elif fixture["fixtureType"] == "AUTHORIZATION_READ_WRITE_PAIR":
                fixture_result = check_auth_read_write_pair(fixture, schemas)
            elif fixture["fixtureType"] == "MATERIALIZATION_MULTI_PAIR":
                fixture_result = check_materialization_pair(fixture, schemas)
            elif fixture["fixtureType"] == "QUERY_EXECUTION_PAIR":
                fixture_result = check_query_pair(fixture, schemas)
            elif fixture["fixtureType"] == "PUBLICATION_CLASS_BOUNDARY":
                fixture_result = check_publication_boundary(fixture, schemas)
            else:
                raise ValueError(f"Unknown fixture type {fixture['fixtureType']}")
            result["fixtureResults"][fixture["fixtureId"]] = fixture_result
    except Exception as e:
        result["overall"] = "FAIL"
        result["fatalError"] = str(e)

    if result["overall"] == "PASS":
        result["overall"] = "PASS_WITH_LIMITATIONS"
        result["notes"] = "Typed runtime-boundary envelope fixtures passed for the starter authority, materialization, query, and publication seams. Coverage is still narrow and does not yet prove full gate-ordering or full action-matrix completion."

    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(result["overall"])
    return 0 if result["overall"] != "FAIL" else 1


if __name__ == "__main__":
    raise SystemExit(main())
