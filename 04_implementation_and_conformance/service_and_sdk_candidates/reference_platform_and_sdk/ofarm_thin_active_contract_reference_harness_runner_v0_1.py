#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

try:
    import jsonschema
except ImportError as e:
    raise SystemExit("jsonschema is required for this validator") from e

ROOT = Path(__file__).resolve().parents[1]
MC = ROOT / "03_machine_contracts"
IMPL = ROOT / "04_implementation_and_conformance"
CHAIN = IMPL / "OFARM_thin_active_contract_reference_harness_chain_v0_1.json"
OUT = IMPL / "OFARM_thin_active_contract_reference_harness_results_v0_1.json"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def infer_schema(example_name: str, schema_names: list[str]) -> str | None:
    if "_example_" not in example_name:
        return None
    prefix = example_name.split("_example_")[0]
    candidates = sorted([s for s in schema_names if s.startswith(prefix + "_schema_")])
    return candidates[0] if candidates else None


def expect(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


def parse_dt(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def walk_strings(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from walk_strings(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from walk_strings(item)


def first_scope_ref(obj: dict[str, Any], key: str = "anchorScopes") -> str | None:
    scopes = obj.get(key) or []
    if scopes and isinstance(scopes, list):
        first = scopes[0]
        if isinstance(first, dict):
            return first.get("scopeRef")
    return None


def main() -> int:
    chain = load_json(CHAIN)
    schema_names = sorted(p.name for p in MC.glob("*_schema_*.json"))
    schemas = {name: load_json(MC / name) for name in schema_names}
    for schema in schemas.values():
        jsonschema.Draft202012Validator.check_schema(schema)

    examples: dict[str, Any] = {}
    example_validation: dict[str, str] = {}
    chain_artifacts: dict[str, dict[str, Any]] = {}
    overall = "PASS"

    for slot, relpath in chain["artifactFiles"].items():
        path = ROOT / relpath
        filename = path.name
        schema_name = infer_schema(filename, schema_names)
        if schema_name is None:
            raise AssertionError(f"Could not infer schema for {filename}")
        data = load_json(path)
        try:
            jsonschema.validate(data, schemas[schema_name])
            example_validation[f"{relpath} :: 03_machine_contracts/{schema_name}"] = "PASS"
            examples[slot] = data
            chain_artifacts[slot] = {
                "path": relpath,
                "schema": f"03_machine_contracts/{schema_name}",
            }
        except Exception as exc:
            example_validation[f"{relpath} :: 03_machine_contracts/{schema_name}"] = f"FAIL: {exc}"
            overall = "FAIL"

    checks: dict[str, dict[str, Any]] = {}

    try:
        expect(all(str(rel).startswith("03_machine_contracts/") for rel in chain["artifactFiles"].values()), "all harness artifacts must come from 03_machine_contracts")
        expect(not any("draft" in str(rel).lower() for rel in chain["artifactFiles"].values()), "draft-only artifacts are not allowed in the harness")
        expect(not any("BridgeCandidate" in str(rel) for rel in chain["artifactFiles"].values()), "bridge artifacts are not allowed in the harness path")
        checks["active_contract_only_path"] = {
            "status": "PASS",
            "artifactCount": len(chain["artifactFiles"]),
        }
    except Exception as exc:
        checks["active_contract_only_path"] = {"status": "FAIL", "detail": str(exc)}
        overall = "FAIL"

    try:
        semantic_event = examples["semantic_event"]
        commit_request = examples["commit_ingress_request"]
        commit_result = examples["commit_ingress_result"]
        promotion_trace = examples["promotion_trace"]
        assertion = examples["assertion_record"]
        review = examples["review_decision"]
        consequence = examples["accepted_consequence"]

        event_id = semantic_event["semanticEventId"]
        expect(commit_request["semanticEventRef"] == event_id, "commit request semanticEventRef mismatch")
        expect(commit_result["semanticEventRef"] == event_id, "commit result semanticEventRef mismatch")
        expect(promotion_trace["semanticEventRef"] == event_id, "promotion trace semanticEventRef mismatch")
        expect(event_id in assertion["provenanceRefs"], "assertion provenance must include semantic event")
        expect(consequence["sourceEventRef"] == event_id, "accepted consequence sourceEventRef mismatch")
        checks["semantic_event_propagation"] = {"status": "PASS", "semanticEventId": event_id}
    except Exception as exc:
        checks["semantic_event_propagation"] = {"status": "FAIL", "detail": str(exc)}
        overall = "FAIL"

    try:
        commit_request = examples["commit_ingress_request"]
        commit_result = examples["commit_ingress_result"]
        promotion_trace = examples["promotion_trace"]
        assertion = examples["assertion_record"]
        review = examples["review_decision"]
        consequence = examples["accepted_consequence"]

        expect(commit_result["requestId"] == commit_request["requestId"], "commit result requestId mismatch")
        expect(promotion_trace["requestId"] == commit_request["requestId"], "promotion trace requestId mismatch")
        expect(commit_result["promotionTraceRef"] == promotion_trace["promotionTraceId"], "promotion trace reference mismatch")
        expect(commit_result["decisionOutcome"] == chain["expectedOutcome"]["promotionDecision"], "unexpected promotion outcome")
        expect(assertion["assertionRecordId"] in commit_result["emittedAssertionRecordRefs"], "commit result must emit assertion")
        expect(review["reviewDecisionId"] in commit_result["emittedReviewDecisionRefs"], "commit result must emit review decision")
        expect(consequence["acceptedEventConsequenceId"] in commit_result["emittedAcceptedConsequenceRefs"], "commit result must emit accepted consequence")
        expect(review["reviewedArtifactRef"] == assertion["assertionRecordId"], "review must point to assertion")
        expect(consequence["acceptedByReviewDecisionRef"] == review["reviewDecisionId"], "consequence must point to review")
        expect(consequence["acceptedEventConsequenceId"] in review["resultingAcceptedConsequenceRefs"], "review must emit accepted consequence")
        expect(promotion_trace["finalOutcome"] == commit_result["decisionOutcome"], "promotion trace finalOutcome mismatch")
        checks["governed_promotion_chain"] = {"status": "PASS"}
    except Exception as exc:
        checks["governed_promotion_chain"] = {"status": "FAIL", "detail": str(exc)}
        overall = "FAIL"

    try:
        semantic_event = examples["semantic_event"]
        commit_request = examples["commit_ingress_request"]
        commit_result = examples["commit_ingress_result"]
        assertion = examples["assertion_record"]
        review = examples["review_decision"]
        consequence = examples["accepted_consequence"]
        mat_request = examples["materialization_request"]
        mat_snapshot = examples["materialization_snapshot"]
        mat_result = examples["materialization_result"]
        passport = examples["passport_view_metadata"]
        share = examples["sharing_grant"]
        auth_request = examples["authorization_request"]
        auth_result = examples["authorization_result"]
        auth_trace = examples["authorization_trace"]
        pub_request = examples["publication_request"]
        pub_result = examples["publication_result"]

        chronology = {
            "eventTime": semantic_event["timeSemantics"]["eventTime"],
            "recordTime": semantic_event["timeSemantics"]["recordTime"],
            "assertedAt": assertion["assertedAt"],
            "ingestedAt": commit_request["ingestedAt"],
            "processedAt": commit_result["processedAt"],
            "decidedAt": review["decidedAt"],
            "acceptedAt": consequence["acceptedAt"],
            "materializationRequestedAt": mat_request["requestedAt"],
            "materializationGeneratedAt": mat_snapshot["generatedAt"],
            "materializationEvaluatedAt": mat_result["evaluatedAt"],
            "passportGeneratedAt": passport["generatedAt"],
            "sharingValidFrom": share["validFrom"],
            "authRequestedAt": auth_request["requestedAt"],
            "authEvaluatedAt": auth_result["evaluatedAt"],
            "publicationRequestedAt": pub_request["requestedAt"],
            "publicationEvaluatedAt": pub_result["evaluatedAt"],
        }
        ordered = [parse_dt(v) for v in chronology.values()]
        expect(ordered == sorted(ordered), "chronology is not monotonic across the reference harness")
        checks["temporal_monotonicity"] = {"status": "PASS", "chronology": chronology}
    except Exception as exc:
        checks["temporal_monotonicity"] = {"status": "FAIL", "detail": str(exc)}
        overall = "FAIL"

    try:
        assertion = examples["assertion_record"]
        review = examples["review_decision"]
        consequence = examples["accepted_consequence"]
        mat_request = examples["materialization_request"]
        mat_basis = examples["materialization_basis"]
        mat_snapshot = examples["materialization_snapshot"]
        mat_result = examples["materialization_result"]
        passport = examples["passport_view_metadata"]

        expect(mat_request["materializationBasisRef"] == mat_basis["basisId"], "materialization request basis mismatch")
        expect(mat_request["reuseCandidateSnapshotRef"] == mat_snapshot["snapshotId"], "materialization request snapshot mismatch")
        expect(assertion["assertionRecordId"] in mat_basis["contributingAssertionRefs"], "materialization basis missing assertion")
        expect(review["reviewDecisionId"] in mat_basis["contributingReviewDecisionRefs"], "materialization basis missing review")
        expect(consequence["acceptedEventConsequenceId"] in mat_basis["contributingAcceptedConsequenceRefs"], "materialization basis missing consequence")
        expect(mat_snapshot["materializationBasisRef"] == mat_basis["basisId"], "materialization snapshot basis mismatch")
        expect(mat_result["requestId"] == mat_request["requestId"], "materialization result request mismatch")
        expect(mat_result["materializationBasisRef"] == mat_basis["basisId"], "materialization result basis mismatch")
        expect(mat_result["materializationSnapshotRef"] == mat_snapshot["snapshotId"], "materialization result snapshot mismatch")
        expect(mat_result["decisionOutcome"] == chain["expectedOutcome"]["materializationDecision"], "unexpected materialization decision")
        expect(mat_result["freshnessState"] == "FRESH", "materialization freshness must be FRESH")
        expect(mat_result["satisfiedFreshnessRequirement"] is True, "freshness requirement must be satisfied")
        expect(passport["materializationResultRef"] == mat_result["resultId"], "passport metadata must resolve to materialization result")
        checks["materialization_grounding"] = {"status": "PASS", "materializationResultRef": mat_result["resultId"]}
    except Exception as exc:
        checks["materialization_grounding"] = {"status": "FAIL", "detail": str(exc)}
        overall = "FAIL"

    try:
        share = examples["sharing_grant"]
        auth_request = examples["authorization_request"]
        auth_result = examples["authorization_result"]
        auth_trace = examples["authorization_trace"]
        passport = examples["passport_view_metadata"]
        pub_request = examples["publication_request"]
        pub_result = examples["publication_result"]
        mat_result = examples["materialization_result"]

        expect(share["sharedArtifactRef"] == passport["passportViewId"], "sharing grant must target passport view")
        expect(auth_request["target"]["targetRef"] == passport["passportViewId"], "authorization request targetRef mismatch")
        expect(auth_result["requestId"] == auth_request["requestId"], "authorization result request mismatch")
        expect(auth_result["authorizationDecisionTraceRef"] == auth_trace["traceId"], "authorization trace mismatch")
        expect(share["sharingGrantId"] in auth_result["sharingBasisUsed"], "authorization result missing sharing grant")
        expect(share["sharingGrantId"] in auth_trace["sharingBasisUsed"], "authorization trace missing sharing grant")
        expect(auth_result["decisionOutcome"] == "ALLOW", "authorization must allow buyer read")
        expect(auth_result["finalActionPermitted"] is True, "authorization must permit final action")
        expect(pub_request["materializationResultRef"] == mat_result["resultId"], "publication request materialization result mismatch")
        expect(pub_request["authorizationDecisionTraceRef"] == auth_trace["traceId"], "publication request auth trace mismatch")
        expect(pub_request["outputMetadataRef"] == passport["passportViewId"], "publication request output metadata mismatch")
        expect(pub_request["outputKind"] == chain["expectedOutcome"]["outputKind"], "publication output kind mismatch")
        expect(pub_request["requiresFrozenOutput"] == chain["expectedOutcome"]["requiresFrozenOutput"], "publication must remain live and non-frozen")
        expect(pub_request["attestationRequested"] == chain["expectedOutcome"]["attestationRequested"], "attestation should not be requested for live passport view")
        expect(pub_result["requestId"] == pub_request["requestId"], "publication result request mismatch")
        expect(pub_result["publicationAction"] == pub_request["publicationAction"], "publication action mismatch")
        expect(pub_result["outcome"] == chain["expectedOutcome"]["publicationOutcome"], "publication outcome mismatch")
        expect(pub_result["outputMetadataRef"] == passport["passportViewId"], "publication result output metadata mismatch")
        checks["output_surface_governance"] = {"status": "PASS", "publicationRef": pub_result["publicationRef"]}
    except Exception as exc:
        checks["output_surface_governance"] = {"status": "FAIL", "detail": str(exc)}
        overall = "FAIL"

    try:
        offending_values = []
        for slot, data in examples.items():
            for value in walk_strings(data):
                if value.startswith("bridge:") or value.startswith("scenario:"):
                    offending_values.append({"slot": slot, "value": value})
        expect(not offending_values, f"bridge/scenario refs should be absent, found {offending_values}")
        checks["no_bridge_shortcut"] = {"status": "PASS"}
    except Exception as exc:
        checks["no_bridge_shortcut"] = {"status": "FAIL", "detail": str(exc)}
        overall = "FAIL"

    output = {
        "harnessDefinition": str(CHAIN.relative_to(ROOT)),
        "chainArtifacts": chain_artifacts,
        "exampleValidation": example_validation,
        "fixtureResults": checks,
        "summary": {
            "activeContractOnlyPath": checks.get("active_contract_only_path", {}).get("status") == "PASS",
            "semanticEventPropagationConsistent": checks.get("semantic_event_propagation", {}).get("status") == "PASS",
            "governedPromotionChainConsistent": checks.get("governed_promotion_chain", {}).get("status") == "PASS",
            "temporalMonotonicityProved": checks.get("temporal_monotonicity", {}).get("status") == "PASS",
            "materializationGroundingProved": checks.get("materialization_grounding", {}).get("status") == "PASS",
            "outputSurfaceGovernanceProved": checks.get("output_surface_governance", {}).get("status") == "PASS",
            "bridgeShortcutAbsent": checks.get("no_bridge_shortcut", {}).get("status") == "PASS",
            "schemasAndExamplesValidated": all(v == "PASS" for v in example_validation.values()),
            "activeContractArtifactCount": len(chain["artifactFiles"]),
        },
        "overall": "PASS_WITH_LIMITATIONS" if overall == "PASS" else "FAIL",
        "notes": "This harness proves one narrow active-contract path from semantic event ingress through governed live passport publication. It does not prove live deployment evidence, same-standard bridge promotion, or broad external-standard readiness."
    }

    OUT.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(OUT)
    print(output["overall"])
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
