#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

try:
    import jsonschema
except ImportError as e:
    raise SystemExit("jsonschema is required for this validator") from e

ROOT = Path(__file__).resolve().parents[1]
MC = ROOT / "03_machine_contracts"
RFC = ROOT / "02_accepted_rfcs"
OUT = Path(__file__).resolve().parent / "OFARM_runtime_surface_contract_currentness_results_v0_1.json"

V1_FILES = {
    "ngsi": "OFARM_RuntimeSurfaceContract_example_ngsi_ld_export_v0_1.json",
    "discovery": "OFARM_RuntimeSurfaceContract_example_capability_discovery_v0_1.json",
    "query": "OFARM_RuntimeSurfaceContract_example_cql2_query_facade_v0_1.json",
}

V2_FILES = {
    "ngsi": "OFARM_RuntimeSurfaceContract_example_ngsi_ld_export_v0_2_draft.json",
    "discovery": "OFARM_RuntimeSurfaceContract_example_capability_discovery_v0_2_draft.json",
    "query": "OFARM_RuntimeSurfaceContract_example_cql2_query_facade_v0_2_draft.json",
    "event": "OFARM_RuntimeSurfaceContract_example_semantic_event_ingress_v0_2_draft.json",
    "file_export": "OFARM_RuntimeSurfaceContract_example_isoxml_bridge_export_draft_v0_2_draft.json",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def expect(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


def main() -> int:
    v1_schema = load_json(MC / "OFARM_RuntimeSurfaceContract_schema_v0_1.json")
    v2_schema = load_json(MC / "OFARM_RuntimeSurfaceContract_schema_v0_2_draft.json")
    jsonschema.Draft202012Validator.check_schema(v1_schema)
    jsonschema.Draft202012Validator.check_schema(v2_schema)

    v1_records = {k: load_json(MC / v) for k, v in V1_FILES.items()}
    v2_records = {k: load_json(MC / v) for k, v in V2_FILES.items()}

    overall_pass = True
    positive_validations = []

    for key, filename in V1_FILES.items():
        try:
            jsonschema.validate(v1_records[key], v1_schema)
            positive_validations.append({
                "exampleFile": filename,
                "schemaFamily": "v0.1",
                "status": "PASS"
            })
        except Exception as exc:
            overall_pass = False
            positive_validations.append({
                "exampleFile": filename,
                "schemaFamily": "v0.1",
                "status": "FAIL",
                "detail": str(exc)
            })

    for key, filename in V2_FILES.items():
        try:
            jsonschema.validate(v2_records[key], v2_schema)
            positive_validations.append({
                "exampleFile": filename,
                "schemaFamily": "v0.2-draft",
                "status": "PASS"
            })
        except Exception as exc:
            overall_pass = False
            positive_validations.append({
                "exampleFile": filename,
                "schemaFamily": "v0.2-draft",
                "status": "FAIL",
                "detail": str(exc)
            })

    semantic_checks = []

    try:
        note = (RFC / "OFARM_RuntimeSurfaceContract_Currentness_Closure_Note_v0_1.md").read_text(encoding="utf-8")
        expect("OFARM_RuntimeSurfaceContract_schema_v0_1.json" in note and "default current contract" in note, "currentness note must keep v0.1 as the default current contract")
        expect("v0.2 draft" in note, "currentness note must name the v0.2 draft extension")
        semantic_checks.append({
            "checkId": "currentness-note-defaults",
            "status": "PASS"
        })
    except Exception as exc:
        overall_pass = False
        semantic_checks.append({
            "checkId": "currentness-note-defaults",
            "status": "FAIL",
            "detail": str(exc)
        })

    try:
        ngsi = v2_records["ngsi"]
        expect(ngsi["surfaceBinding"]["bindingKind"] == "HTTP_PATH", "NGSI export should bind by HTTP path")
        expect(ngsi["authPosture"] == "PARTNER_SCOPED", "NGSI export should stay partner-scoped")
        expect(ngsi["deliverySemantics"] == "REQUEST_RESPONSE", "NGSI export should be request/response")
        expect(ngsi["idempotencyPosture"] == "SAFE_RETRY_SAME_RESULT", "NGSI export should be safe to repeat")
        semantic_checks.append({
            "checkId": "ngsi-http-surface-posture",
            "status": "PASS"
        })
    except Exception as exc:
        overall_pass = False
        semantic_checks.append({
            "checkId": "ngsi-http-surface-posture",
            "status": "FAIL",
            "detail": str(exc)
        })

    try:
        query = v2_records["query"]
        expect(query["surfaceBinding"]["bindingKind"] == "QUERY_NAMESPACE", "query façade should bind by query namespace")
        expect(query["versionPosture"]["compatibilityPosture"] == "EXPERIMENTAL_NON_DEFAULT", "query façade draft should remain non-default experimental")
        expect(query["idempotencyPosture"] == "SAFE_RETRY_SAME_RESULT", "query façade should be retry-safe")
        semantic_checks.append({
            "checkId": "query-facade-boundary-posture",
            "status": "PASS"
        })
    except Exception as exc:
        overall_pass = False
        semantic_checks.append({
            "checkId": "query-facade-boundary-posture",
            "status": "FAIL",
            "detail": str(exc)
        })

    try:
        event = v2_records["event"]
        expect(event["surfaceBinding"]["bindingKind"] == "TOPIC_NAMESPACE", "event surface should bind by topic namespace")
        expect(event["deliverySemantics"] == "AT_LEAST_ONCE_STREAM", "event surface should declare at-least-once delivery")
        expect(event["idempotencyPosture"] == "CONSUMER_DEDUP_REQUIRED", "event surface should declare consumer dedup")
        semantic_checks.append({
            "checkId": "event-surface-delivery-idempotency-posture",
            "status": "PASS"
        })
    except Exception as exc:
        overall_pass = False
        semantic_checks.append({
            "checkId": "event-surface-delivery-idempotency-posture",
            "status": "FAIL",
            "detail": str(exc)
        })

    negative_checks = []

    try:
        bad = copy.deepcopy(v2_records["discovery"])
        del bad["surfaceBinding"]
        jsonschema.validate(bad, v2_schema)
        negative_checks.append({"caseId": "neg-missing-surface-binding", "status": "UNEXPECTED_PASS"})
        overall_pass = False
    except Exception as exc:
        negative_checks.append({"caseId": "neg-missing-surface-binding", "status": "EXPECTED_FAIL", "detail": str(exc).splitlines()[0]})

    try:
        bad = copy.deepcopy(v2_records["query"])
        bad["surfaceBinding"]["bindingKind"] = "HTTP_PATH"
        jsonschema.validate(bad, v2_schema)
        negative_checks.append({"caseId": "neg-query-binding-kind", "status": "UNEXPECTED_PASS"})
        overall_pass = False
    except Exception as exc:
        negative_checks.append({"caseId": "neg-query-binding-kind", "status": "EXPECTED_FAIL", "detail": str(exc).splitlines()[0]})

    try:
        bad = copy.deepcopy(v2_records["event"])
        bad["idempotencyPosture"] = "SAFE_RETRY_SAME_RESULT"
        jsonschema.validate(bad, v2_schema)
        negative_checks.append({"caseId": "neg-event-idempotency-posture", "status": "UNEXPECTED_PASS"})
        overall_pass = False
    except Exception as exc:
        negative_checks.append({"caseId": "neg-event-idempotency-posture", "status": "EXPECTED_FAIL", "detail": str(exc).splitlines()[0]})

    try:
        bad = copy.deepcopy(v2_records["file_export"])
        bad["deliverySemantics"] = "REQUEST_RESPONSE"
        jsonschema.validate(bad, v2_schema)
        negative_checks.append({"caseId": "neg-file-exchange-delivery", "status": "UNEXPECTED_PASS"})
        overall_pass = False
    except Exception as exc:
        negative_checks.append({"caseId": "neg-file-exchange-delivery", "status": "EXPECTED_FAIL", "detail": str(exc).splitlines()[0]})

    results = {
        "generatedAt": "2026-04-19T15:20:00Z",
        "overall": "PASS_WITH_LIMITATIONS" if overall_pass else "FAIL",
        "summary": {
            "v0_1_examples_validated": len(V1_FILES),
            "v0_2_draft_examples_validated": len(V2_FILES),
            "eventSurfacesCovered": 1,
            "discoverySurfacesCovered": 1,
            "httpApiSurfacesCovered": 1,
            "queryFacadeSurfacesCovered": 1,
            "fileExchangeSurfacesCovered": 1,
            "negativeCasesChecked": len(negative_checks),
            "negativeCasesExpectedFail": sum(1 for r in negative_checks if r["status"] == "EXPECTED_FAIL")
        },
        "positiveValidations": positive_validations,
        "semanticChecks": semantic_checks,
        "negativeChecks": negative_checks,
        "limitations": [
            "v0.2 draft remains a non-default extension and is not yet referenced as the active package-wide runtime-surface default.",
            "The proof is package-local and contract-level; it does not yet publish deployment-collected endpoint/topic telemetry.",
            "Service-description artifacts remain references only and are not re-promoted as semantic authority by this wave."
        ]
    }
    OUT.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    return 0 if overall_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
