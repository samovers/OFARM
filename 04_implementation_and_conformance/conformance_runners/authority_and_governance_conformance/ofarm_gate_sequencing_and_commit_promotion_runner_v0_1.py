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
FIX = Path(__file__).resolve().parent / "ofarm_gate_sequencing_fixtures_v0_1"
OUT = Path(__file__).resolve().parent / "OFARM_gate_sequencing_and_commit_promotion_results_v0_1.json"

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

WEAK_TO_HARD_TRUTH_FORBIDDEN = {"note", "hypothesis assertion", "evidence record", "advisory output"}
HARD_TRUTH_TARGETS = {
    "accepted executed intervention consequence",
    "compliance fact",
    "accepted structural state",
    "accepted observation/occurrence state",
    "accepted material state",
}


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def expect(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


def infer_schema(example_name: str, schema_names: List[str]) -> str | None:
    if "_example_" not in example_name:
        return None
    prefix = example_name.split("_example_")[0]
    candidates = sorted([s for s in schema_names if s.startswith(prefix + "_schema_")])
    if not candidates:
        return None
    if len(candidates) == 1:
        return candidates[0]
    for candidate in candidates:
        if "v0_2_draft" in example_name and "v0_2_draft" in candidate:
            return candidate
    for candidate in candidates:
        if "v0_1" in candidate:
            return candidate
    return candidates[0]


def validate_example(example_name: str, schemas: Dict[str, Dict[str, Any]], cache: Dict[str, str]) -> None:
    if example_name in cache:
        return
    schema_name = infer_schema(example_name, list(schemas.keys()))
    if schema_name is None:
        raise AssertionError(f"could not infer schema for {example_name}")
    jsonschema.validate(load_json(MC / example_name), schemas[schema_name])
    cache[example_name] = schema_name


def normalize_target_scope(value: Any) -> Any:
    if isinstance(value, list):
        return sorted([normalize_target_scope(v) for v in value], key=lambda x: json.dumps(x, sort_keys=True))
    if isinstance(value, dict):
        return {k: normalize_target_scope(value[k]) for k in sorted(value)}
    return value


def check_gate_order(fixture: Dict[str, Any]) -> None:
    indexes = [GATE_ORDER.index(g["gate"]) for g in fixture["gates"]]
    expect(indexes == sorted(indexes), f"{fixture['fixtureId']} gate order is not monotonic")
    expect(fixture["gates"][-1]["gate"] == fixture["expectedStopGate"], f"{fixture['fixtureId']} expected stop gate mismatch")
    expect(fixture["gates"][-1]["outcome"] == fixture["expectedStopOutcome"], f"{fixture['fixtureId']} expected stop outcome mismatch")


def check_authority_gate(fixture: Dict[str, Any], gate: Dict[str, Any], schemas: Dict[str, Dict[str, Any]], cache: Dict[str, str]) -> Dict[str, Any]:
    detail: Dict[str, Any] = {"outcome": gate["outcome"]}
    req = res = trace = None
    if gate.get("requestExample"):
        validate_example(gate["requestExample"], schemas, cache)
        req = load_json(MC / gate["requestExample"])
    if gate.get("resultExample"):
        validate_example(gate["resultExample"], schemas, cache)
        res = load_json(MC / gate["resultExample"])
    if gate.get("traceExample"):
        validate_example(gate["traceExample"], schemas, cache)
        trace = load_json(MC / gate["traceExample"])

    if req is not None and res is not None:
        expect(res["requestId"] == req["requestId"], f"{fixture['fixtureId']} authority requestId mismatch")
        expect(res["decisionOutcome"] == gate["outcome"], f"{fixture['fixtureId']} authority outcome mismatch")
        if fixture.get("actionClass"):
            expect(req["actionClass"] == fixture["actionClass"], f"{fixture['fixtureId']} actionClass mismatch")
            expect(res["requestedActionClass"] == fixture["actionClass"], f"{fixture['fixtureId']} result actionClass mismatch")
        if fixture.get("actionStage"):
            expect(req["actionStage"] == fixture["actionStage"], f"{fixture['fixtureId']} actionStage mismatch")
            expect(res["actionStage"] == fixture["actionStage"], f"{fixture['fixtureId']} result actionStage mismatch")
        detail["requestExample"] = gate["requestExample"]
        detail["resultExample"] = gate["resultExample"]
    if trace is not None and res is not None:
        expect(trace["traceId"] == res["authorizationDecisionTraceRef"], f"{fixture['fixtureId']} trace ref mismatch")
        expect(trace["decisionOutcome"] == res["decisionOutcome"], f"{fixture['fixtureId']} trace outcome mismatch")
    if trace is not None and req is not None:
        expect(trace["requestedActionClass"] == req["actionClass"], f"{fixture['fixtureId']} trace action mismatch")
        expect(normalize_target_scope(trace["target"]["scope"]) == normalize_target_scope(req["target"]["scope"]), f"{fixture['fixtureId']} trace scope mismatch")
    if trace is not None and req is None and fixture.get("actionClass"):
        expect(trace["requestedActionClass"] == fixture["actionClass"], f"{fixture['fixtureId']} trace action class mismatch")
        expect(trace["decisionOutcome"] == gate["outcome"], f"{fixture['fixtureId']} trace outcome mismatch")
    if fixture["fixtureType"] == "AUTHORITY_RECHECK_SEQUENCE" and res is not None and fixture.get("requiresFinalReauthorization"):
        expect(res["revocationResult"] == "ACTIVE_REVOCATION_FOUND", f"{fixture['fixtureId']} expected active revocation")
        detail["revocationResult"] = res["revocationResult"]
    return detail


def check_evidence_gate(fixture: Dict[str, Any], gate: Dict[str, Any], schemas: Dict[str, Dict[str, Any]], cache: Dict[str, str]) -> Dict[str, Any]:
    detail: Dict[str, Any] = {"outcome": gate["outcome"]}
    if gate.get("caseExample"):
        validate_example(gate["caseExample"], schemas, cache)
        case = load_json(MC / gate["caseExample"])
        decision = case["outcome"]["decision"]
        mapped = {"ALLOW": "SATISFIED", "REFUSE": "INSUFFICIENT", "REVIEW_REQUIRED": "REVIEW_REQUIRED"}.get(decision)
        expect(mapped == gate["outcome"], f"{fixture['fixtureId']} evidence gate outcome mismatch")
        detail["caseExample"] = gate["caseExample"]
        detail["caseDecision"] = decision
    return detail


def check_materialization_gate(fixture: Dict[str, Any], gate: Dict[str, Any], schemas: Dict[str, Dict[str, Any]], cache: Dict[str, str]) -> Dict[str, Any]:
    detail: Dict[str, Any] = {"outcome": gate["outcome"]}
    if gate.get("resultExample"):
        validate_example(gate["resultExample"], schemas, cache)
        result = load_json(MC / gate["resultExample"])
        expect(result["decisionOutcome"] == gate["outcome"], f"{fixture['fixtureId']} materialization outcome mismatch")
        detail["resultExample"] = gate["resultExample"]
        detail["freshnessState"] = result["freshnessState"]
        if fixture["fixtureType"] == "PUBLICATION_SEQUENCE":
            expect(result["highConsequenceUse"] is True, f"{fixture['fixtureId']} publication path must use high-consequence materialization")
            expect(result["targetTwin"] == "COMPLIANCE", f"{fixture['fixtureId']} publication path must use compliance twin")
    return detail


def check_publication_gate(fixture: Dict[str, Any], gate: Dict[str, Any], schemas: Dict[str, Dict[str, Any]], cache: Dict[str, str]) -> Dict[str, Any]:
    detail: Dict[str, Any] = {"outcome": gate["outcome"]}
    request = result = None
    if gate.get("requestExample"):
        validate_example(gate["requestExample"], schemas, cache)
        request = load_json(MC / gate["requestExample"])
        detail["requestExample"] = gate["requestExample"]
    if gate.get("resultExample"):
        validate_example(gate["resultExample"], schemas, cache)
        result = load_json(MC / gate["resultExample"])
        detail["resultExample"] = gate["resultExample"]
    if request is not None and result is not None:
        expect(result["requestId"] == request["requestId"], f"{fixture['fixtureId']} publication requestId mismatch")
        expect(result["publicationAction"] == request["publicationAction"], f"{fixture['fixtureId']} publicationAction mismatch")
        expect(result["outputKind"] == request["outputKind"], f"{fixture['fixtureId']} outputKind mismatch")
        expect(result["outcome"] == gate["outcome"], f"{fixture['fixtureId']} publication outcome mismatch")
        expect(request["outputKind"] == fixture["outputKind"], f"{fixture['fixtureId']} publication fixture outputKind mismatch")
        expect(request["publicationAction"] == fixture["publicationAction"], f"{fixture['fixtureId']} publication fixture action mismatch")
        if fixture.get("requiresFrozenOutput"):
            expect(request["requiresFrozenOutput"] is True, f"{fixture['fixtureId']} expected frozen output requirement")
            expect(request["outputKind"] != "PASSPORT_VIEW", f"{fixture['fixtureId']} frozen output cannot be passport")
    return detail


def check_commit_promotion_rules(fixture: Dict[str, Any]) -> None:
    commit_class = fixture["commitClass"]
    target = fixture["requestedInForceCategory"]
    terminal = fixture["terminalOutcome"]
    gate_map = {g["gate"]: g for g in fixture["gates"]}
    if commit_class in WEAK_TO_HARD_TRUTH_FORBIDDEN and target in HARD_TRUTH_TARGETS:
        expect(terminal != "PROMOTED_ACCEPTED", f"{fixture['fixtureId']} weak class may not promote directly to hard truth")
    if commit_class == "operation claim" and terminal == "PROMOTED_ACCEPTED":
        expect(gate_map.get("EVIDENCE_SUFFICIENCY", {}).get("outcome") == "SATISFIED", f"{fixture['fixtureId']} operation claim needs satisfied evidence gate")
        expect(gate_map.get("REVIEW_PROMOTION", {}).get("outcome") == "PROMOTE_ACCEPTED", f"{fixture['fixtureId']} operation claim needs review/promotion accept")
    if commit_class == "compliance assertion" and target == "compliance fact" and terminal == "PROMOTED_ACCEPTED":
        expect(gate_map.get("EVIDENCE_SUFFICIENCY", {}).get("outcome") == "SATISFIED", f"{fixture['fixtureId']} compliance assertion needs satisfied evidence gate")
        expect(gate_map.get("REVIEW_PROMOTION", {}).get("outcome") == "PROMOTE_ACCEPTED", f"{fixture['fixtureId']} compliance assertion needs review/promotion accept")
    if fixture.get("currentStateUpdateExpected"):
        expect(gate_map.get("CURRENT_STATE_MATERIALIZATION", {}).get("outcome") == "UPDATED", f"{fixture['fixtureId']} expected current-state update")
    else:
        if terminal in {"RETAIN_DRAFT", "DENY", "REQUIRE_HUMAN_APPROVAL"}:
            expect("CURRENT_STATE_MATERIALIZATION" not in gate_map, f"{fixture['fixtureId']} should not reach current-state update")


def check_publication_rules(fixture: Dict[str, Any]) -> None:
    gate_map = {g["gate"]: g for g in fixture["gates"]}
    for required in ["AUTHORITY", "EVIDENCE_SUFFICIENCY", "CURRENT_STATE_MATERIALIZATION", "PUBLICATION_EXPORT_TRACEABILITY"]:
        expect(required in gate_map, f"{fixture['fixtureId']} missing required gate {required}")
    expect(gate_map["AUTHORITY"]["outcome"] == "ALLOW", f"{fixture['fixtureId']} publication path requires authority allow")
    expect(gate_map["EVIDENCE_SUFFICIENCY"]["outcome"] == "SATISFIED", f"{fixture['fixtureId']} publication path requires satisfied evidence")
    expect(gate_map["CURRENT_STATE_MATERIALIZATION"]["outcome"] in {"ALLOW_REUSE", "RECOMPUTE_REQUIRED"}, f"{fixture['fixtureId']} publication path needs governed materialization decision")
    expect(gate_map["PUBLICATION_EXPORT_TRACEABILITY"]["outcome"] == fixture["terminalOutcome"], f"{fixture['fixtureId']} publication terminal mismatch")
    if fixture.get("requiresFrozenOutput"):
        expect(fixture["outputKind"] != "PASSPORT_VIEW", f"{fixture['fixtureId']} frozen output cannot be passport")


def check_authority_recheck_rules(fixture: Dict[str, Any]) -> None:
    gate_map = {g["gate"]: g for g in fixture["gates"]}
    expect("AUTHORITY" in gate_map, f"{fixture['fixtureId']} missing authority gate")
    expect(gate_map["AUTHORITY"]["outcome"] in {"DENY", "REQUIRE_HUMAN_APPROVAL", "ALLOW", "REQUIRE_REVIEW"}, f"{fixture['fixtureId']} unexpected authority outcome")
    if gate_map["AUTHORITY"]["outcome"] in {"DENY", "REQUIRE_HUMAN_APPROVAL", "REQUIRE_REVIEW"}:
        for later in ["REVIEW_PROMOTION", "CURRENT_STATE_MATERIALIZATION", "PUBLICATION_EXPORT_TRACEABILITY"]:
            expect(later not in gate_map, f"{fixture['fixtureId']} must stop before {later}")


def main() -> int:
    result: Dict[str, Any] = {
        "exampleValidation": {},
        "fixtureResults": {},
        "overall": "PASS",
    }
    try:
        schema_names = sorted([p.name for p in MC.glob("*_schema_*.json")])
        schemas = {name: load_json(MC / name) for name in schema_names}
        for schema in schemas.values():
            jsonschema.Draft202012Validator.check_schema(schema)
        cache: Dict[str, str] = {}

        fixture_paths = sorted(FIX.glob("*.json"))
        for fixture_path in fixture_paths:
            fixture = load_json(fixture_path)
            check_gate_order(fixture)
            gate_details: List[Dict[str, Any]] = []
            for gate in fixture["gates"]:
                if gate["gate"] == "AUTHORITY":
                    gate_details.append({"gate": gate["gate"], **check_authority_gate(fixture, gate, schemas, cache)})
                elif gate["gate"] == "EVIDENCE_SUFFICIENCY":
                    gate_details.append({"gate": gate["gate"], **check_evidence_gate(fixture, gate, schemas, cache)})
                elif gate["gate"] == "CURRENT_STATE_MATERIALIZATION":
                    gate_details.append({"gate": gate["gate"], **check_materialization_gate(fixture, gate, schemas, cache)})
                elif gate["gate"] == "PUBLICATION_EXPORT_TRACEABILITY":
                    gate_details.append({"gate": gate["gate"], **check_publication_gate(fixture, gate, schemas, cache)})
                else:
                    gate_details.append({"gate": gate["gate"], "outcome": gate["outcome"]})

            if fixture["fixtureType"] == "COMMIT_PROMOTION_SEQUENCE":
                check_commit_promotion_rules(fixture)
            elif fixture["fixtureType"] == "PUBLICATION_SEQUENCE":
                check_publication_rules(fixture)
            elif fixture["fixtureType"] == "AUTHORITY_RECHECK_SEQUENCE":
                check_authority_recheck_rules(fixture)
            else:
                raise AssertionError(f"Unknown fixtureType {fixture['fixtureType']}")

            result["fixtureResults"][fixture["fixtureId"]] = {
                "status": "PASS",
                "terminalOutcome": fixture["terminalOutcome"],
                "expectedStopGate": fixture["expectedStopGate"],
                "expectedStopOutcome": fixture["expectedStopOutcome"],
                "gateDetails": gate_details,
            }

        for example_name, schema_name in sorted(cache.items()):
            result["exampleValidation"][f"{example_name} :: {schema_name}"] = "PASS"
    except Exception as e:
        result["overall"] = "FAIL"
        result["fatalError"] = str(e)

    if result["overall"] == "PASS":
        result["overall"] = "PASS_WITH_LIMITATIONS"
        result["notes"] = (
            "Fixture-level gate-ordering and promotion-safety checks passed for starter commit-promotion, final re-authorization, "
            "and high-consequence publication paths. The runner still relies on declared fixtures rather than runtime-produced gate traces, "
            "and it does not yet cover all event families, review-decision contracts, or projection trace-back completion."
        )
        result["coverageAdvances"] = [
            "commit-promotion safety checks",
            "enforcement-gate sequencing tests",
        ]

    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(result["overall"])
    return 0 if result["overall"] != "FAIL" else 1


if __name__ == "__main__":
    raise SystemExit(main())
