
#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

try:
    import jsonschema
except ImportError as e:
    raise SystemExit("jsonschema is required for this validator") from e

ROOT = Path(__file__).resolve().parents[1]
MC = ROOT / "03_machine_contracts"
OUT = Path(__file__).resolve().parent / "OFARM_runtime_event_ingress_and_idempotency_results_v0_1.json"

GATE_ORDER = [
    "INGRESS_NORMALIZATION",
    "AUTHORITY",
    "VALIDATION",
    "PACK_PROFILE_APPLICABILITY",
    "EVIDENCE_SUFFICIENCY",
    "REVIEW_PROMOTION",
    "CURRENT_STATE_MATERIALIZATION",
    "PUBLICATION_EXPORT_TRACEABILITY",
]

FILES = {
    "semantic_event": "OFARM_SemanticEventEnvelope_example_pruning_operation_v0_1.json",
    "assertion": "OFARM_AssertionRecord_example_pruning_operation_claim_v0_1.json",
    "review": "OFARM_ReviewDecision_example_pruning_operation_claim_accepted_v0_1.json",
    "consequence": "OFARM_AcceptedEventConsequence_example_pruning_operation_confirmed_v0_1.json",
    "request": "OFARM_CommitIngressRequest_example_pruning_operation_claim_v0_1.json",
    "result": "OFARM_CommitIngressResult_example_pruning_operation_claim_promoted_v0_1.json",
    "trace": "OFARM_PromotionTrace_example_pruning_operation_claim_promoted_v0_1.json",
    "replay_request": "OFARM_CommitIngressRequest_example_pruning_operation_claim_replay_v0_1.json",
    "replay_result": "OFARM_CommitIngressResult_example_pruning_operation_claim_replay_reused_v0_1.json",
    "replay_trace": "OFARM_PromotionTrace_example_pruning_operation_claim_replay_reused_v0_1.json",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def infer_schema(example_name: str, schema_names: list[str]) -> str | None:
    if "_example_" not in example_name:
        return None
    prefix = example_name.split("_example_")[0]
    candidates = sorted([s for s in schema_names if s.startswith(prefix + "_schema_")])
    if not candidates:
        return None
    return candidates[0]


def expect(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


def main() -> int:
    schema_names = sorted(p.name for p in MC.glob("*_schema_*.json"))
    schemas = {name: load_json(MC / name) for name in schema_names}
    for schema in schemas.values():
        jsonschema.Draft202012Validator.check_schema(schema)

    example_records: dict[str, Any] = {}
    example_validation: dict[str, str] = {}
    overall = "PASS"
    for key, filename in FILES.items():
        schema_name = infer_schema(filename, schema_names)
        if schema_name is None:
            raise AssertionError(f"Could not infer schema for {filename}")
        data = load_json(MC / filename)
        try:
            jsonschema.validate(data, schemas[schema_name])
            example_validation[f"{filename} :: {schema_name}"] = "PASS"
            example_records[key] = data
        except Exception as exc:
            example_validation[f"{filename} :: {schema_name}"] = f"FAIL: {exc}"
            overall = "FAIL"

    semantic_event = example_records["semantic_event"]
    assertion = example_records["assertion"]
    review = example_records["review"]
    consequence = example_records["consequence"]
    request = example_records["request"]
    result = example_records["result"]
    trace = example_records["trace"]
    replay_request = example_records["replay_request"]
    replay_result = example_records["replay_result"]
    replay_trace = example_records["replay_trace"]

    checks: dict[str, dict[str, Any]] = {}

    try:
        expect(semantic_event["primaryEventFamily"] == "InterventionEvent", "semantic event should be InterventionEvent")
        expect(request["semanticEventRef"] == semantic_event["semanticEventId"], "request semanticEventRef mismatch")
        expect(result["semanticEventRef"] == semantic_event["semanticEventId"], "result semanticEventRef mismatch")
        expect(trace["semanticEventRef"] == semantic_event["semanticEventId"], "trace semanticEventRef mismatch")
        expect(assertion["provenanceRefs"][0] == semantic_event["semanticEventId"], "assertion provenance should resolve to semantic event")
        checks["semantic_event_binding"] = {"status": "PASS"}
    except Exception as exc:
        checks["semantic_event_binding"] = {"status": "FAIL", "detail": str(exc)}
        overall = "FAIL"

    try:
        event_time = semantic_event["timeSemantics"]["eventTime"]
        record_time = semantic_event["timeSemantics"]["recordTime"]
        ingest_time = request["ingestedAt"]
        process_time = result["processedAt"]
        expect(event_time < record_time < ingest_time < process_time, "expected eventTime < recordTime < ingestedAt < processedAt")
        checks["temporal_distinction_preserved"] = {
            "status": "PASS",
            "eventTime": event_time,
            "recordTime": record_time,
            "ingestedAt": ingest_time,
            "processedAt": process_time,
        }
    except Exception as exc:
        checks["temporal_distinction_preserved"] = {"status": "FAIL", "detail": str(exc)}
        overall = "FAIL"

    try:
        expect(request["idempotencyKey"] == trace["idempotencyKey"], "request/trace idempotency key mismatch")
        expect(result["requestId"] == request["requestId"], "result requestId mismatch")
        expect(result["promotionTraceRef"] == trace["promotionTraceId"], "result/trace reference mismatch")
        expect(result["decisionOutcome"] == "PROMOTE_ACCEPTED", "promoted result should be PROMOTE_ACCEPTED")
        expect(result["inForceResultCategory"] == "ACCEPTED_EXECUTED_INTERVENTION_CONSEQUENCE", "wrong in-force result category")
        expect(trace["finalOutcome"] == result["decisionOutcome"], "trace/result final outcome mismatch")
        expect(consequence["acceptedEventConsequenceId"] in result["inForceArtifactRefs"], "result should point to accepted consequence")
        checks["promotion_path_consistency"] = {"status": "PASS"}
    except Exception as exc:
        checks["promotion_path_consistency"] = {"status": "FAIL", "detail": str(exc)}
        overall = "FAIL"

    try:
        gate_indexes = [GATE_ORDER.index(step["gate"]) for step in trace["gateSequence"]]
        expect(gate_indexes == sorted(gate_indexes), "promotion trace gate order is not monotonic")
        expect(trace["gateSequence"][-1]["gate"] == "CURRENT_STATE_MATERIALIZATION", "promoted example should end at current-state materialization")
        expect(trace["gateSequence"][-1]["outcome"] == "UPDATED", "promoted example last outcome should be UPDATED")
        checks["gate_order_and_terminal_outcome"] = {"status": "PASS", "gateCount": len(trace["gateSequence"])}
    except Exception as exc:
        checks["gate_order_and_terminal_outcome"] = {"status": "FAIL", "detail": str(exc)}
        overall = "FAIL"

    try:
        expect(review["reviewedArtifactRef"] == assertion["assertionRecordId"], "review should point to assertion")
        expect(consequence["acceptedByReviewDecisionRef"] == review["reviewDecisionId"], "consequence should point to review")
        expect(consequence["sourceEventRef"] == semantic_event["semanticEventId"], "consequence should point to semantic event")
        expect(consequence["acceptedEventConsequenceId"] in review["resultingAcceptedConsequenceRefs"], "review should emit accepted consequence")
        expect(assertion["assertionRecordId"] in result["emittedAssertionRecordRefs"], "result should emit assertion")
        expect(review["reviewDecisionId"] in result["emittedReviewDecisionRefs"], "result should emit review decision")
        expect(consequence["acceptedEventConsequenceId"] in result["emittedAcceptedConsequenceRefs"], "result should emit accepted consequence")
        checks["source_truth_chain_consistency"] = {"status": "PASS"}
    except Exception as exc:
        checks["source_truth_chain_consistency"] = {"status": "FAIL", "detail": str(exc)}
        overall = "FAIL"

    try:
        expect(replay_request["idempotencyKey"] == request["idempotencyKey"], "replay request must reuse idempotency key")
        expect(replay_request["sourcePayloadDigest"] == request["sourcePayloadDigest"], "replay request payload digest must match")
        expect(replay_result["decisionOutcome"] == "REPLAY_REUSED_RESULT", "replay result should be REPLAY_REUSED_RESULT")
        expect(replay_result["replayOfRequestId"] == request["requestId"], "replay result should point to original request")
        expect(replay_trace["replayOfRequestId"] == request["requestId"], "replay trace should point to original request")
        expect(replay_result.get("emittedAssertionRecordRefs") in (None, []), "replay result should not emit duplicate assertions")
        expect(replay_result.get("emittedReviewDecisionRefs") in (None, []), "replay result should not emit duplicate reviews")
        expect(replay_result.get("emittedAcceptedConsequenceRefs") in (None, []), "replay result should not emit duplicate consequences")
        expect(replay_trace["gateSequence"][0]["gate"] == "INGRESS_NORMALIZATION", "replay should short-circuit at ingress normalization")
        checks["replay_safe_reuse"] = {"status": "PASS", "reusedInForceArtifacts": replay_result["inForceArtifactRefs"]}
    except Exception as exc:
        checks["replay_safe_reuse"] = {"status": "FAIL", "detail": str(exc)}
        overall = "FAIL"

    output = {
        "exampleValidation": example_validation,
        "fixtureResults": checks,
        "summary": {
            "semanticEventBoundaryExplicit": checks.get("semantic_event_binding", {}).get("status") == "PASS",
            "temporalDistinctionPreserved": checks.get("temporal_distinction_preserved", {}).get("status") == "PASS",
            "promotionPathConsistent": checks.get("promotion_path_consistency", {}).get("status") == "PASS",
            "sourceTruthChainConsistent": checks.get("source_truth_chain_consistency", {}).get("status") == "PASS",
            "replaySafeReuseProved": checks.get("replay_safe_reuse", {}).get("status") == "PASS",
            "schemasAndExamplesValidated": all(v == "PASS" for v in example_validation.values()),
        },
        "overall": "PASS_WITH_LIMITATIONS" if overall == "PASS" else "FAIL",
        "notes": "This fixture set proves one promoted event-ingress chain and one replay-safe reuse chain. Coverage is intentionally narrow and does not yet cover every event family, commit class, or transport surface."
    }

    OUT.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(OUT)
    print(output["overall"])
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
