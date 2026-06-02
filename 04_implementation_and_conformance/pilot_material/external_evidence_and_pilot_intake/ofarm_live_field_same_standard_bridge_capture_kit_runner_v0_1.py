#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

HERE = Path(__file__).resolve().parent
OUT = HERE / "OFARM_live_field_same_standard_bridge_capture_kit_results_v0_1.json"
CANDIDATE_PAIRS = HERE / "OFARM_same_standard_bridge_pack_candidate_pairs_v0_6.json"
TEMPLATE_FILES = {
    "live_field": HERE / "OFARM_live_field_same_standard_bridge_telemetry_capture_template_v0_1.json",
    "trace_back": HERE / "OFARM_live_field_same_standard_bridge_trace_back_records_capture_template_v0_1.json",
    "approval": HERE / "OFARM_same_standard_bridge_production_approval_record_capture_template_v0_1.json",
}
DOC_FILES = {
    "capture_kit": HERE / "OFARM_Live_Field_Same_Standard_Bridge_Evidence_Capture_Kit_v0_1.md",
    "operator_note": HERE / "OFARM_live_field_same_standard_bridge_operator_note_v0_1.md",
}
EXPECTED_PATTERNS = {
    "live_field": "OFARM_live_field_same_standard_bridge_telemetry_v*.json",
    "trace_back": "OFARM_live_field_same_standard_bridge_trace_back_records_v*.json",
    "approval": "OFARM_same_standard_bridge_production_approval_record_v*.json",
}

def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))

def expect(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)

def main() -> int:
    result: Dict[str, Any] = {
        "evaluatedAt": "2026-04-18T12:30:00Z",
        "templateChecks": {},
        "documentChecks": {},
        "guardrailChecks": {},
        "summary": {},
        "overall": "PASS",
    }
    try:
        candidate_pairs = load_json(CANDIDATE_PAIRS)
        expected_pair_ids = sorted(entry["candidatePairId"] for entry in candidate_pairs)
        for key, path in TEMPLATE_FILES.items():
            payload = load_json(path)
            result["templateChecks"][f"{path.name} :: parseable-json"] = "PASS"
            expect(payload.get("templateOnly") is True, f"{path.name} must remain templateOnly")
            result["templateChecks"][f"{path.name} :: templateOnly-true"] = "PASS"
            expect(payload.get("qualifiesForPromotionIntake") is False, f"{path.name} must remain non-qualifying")
            result["templateChecks"][f"{path.name} :: non-qualifying-while-template"] = "PASS"
            expect(payload.get("targetProductionArtifactPattern") == EXPECTED_PATTERNS[key], f"{path.name} target pattern mismatch")
            result["templateChecks"][f"{path.name} :: target-pattern-match"] = "PASS"
            expect(path.name != EXPECTED_PATTERNS[key], f"{path.name} must not equal production pattern")
            result["templateChecks"][f"{path.name} :: template-name-avoids-production-pattern"] = "PASS"
            stub_ids = sorted(entry.get("candidatePairId") for entry in payload.get("candidatePairStubs", []))
            expect(stub_ids == expected_pair_ids, f"{path.name} candidate pair coverage mismatch")
            result["templateChecks"][f"{path.name} :: candidate-pair-coverage"] = "PASS"
            record_key = "approvalRecords" if key == "approval" else "records"
            rec_ids = sorted({entry.get("candidatePairId") for entry in payload.get(record_key, []) if entry.get("candidatePairId")})
            expect(rec_ids == expected_pair_ids, f"{path.name} placeholder records must cover both candidate pairs")
            result["templateChecks"][f"{path.name} :: placeholder-record-coverage"] = "PASS"
        for key, path in DOC_FILES.items():
            text = path.read_text(encoding="utf-8")
            result["documentChecks"][f"{path.name} :: exists"] = "PASS"
            expect("does **not**" in text or "do **not**" in text, f"{path.name} must preserve explicit non-qualification language")
            result["documentChecks"][f"{path.name} :: explicit-non-qualification-language"] = "PASS"
            expect("DRAFT" in text, f"{path.name} must preserve hold-at-draft posture")
            result["documentChecks"][f"{path.name} :: draft-posture-mentioned"] = "PASS"
        for key, pattern in EXPECTED_PATTERNS.items():
            template_name = TEMPLATE_FILES[key].name
            expect(not Path(template_name).match(pattern), f"{template_name} must not match discovery pattern {pattern}")
            result["guardrailChecks"][f"{template_name} :: avoids-discovery-pattern-{pattern}"] = "PASS"
        result["summary"] = {
            "candidatePairsCovered": len(expected_pair_ids),
            "templateFiles": len(TEMPLATE_FILES),
            "operatorGuidanceFiles": len(DOC_FILES),
            "captureKitReadyForFutureDeployment": True,
        }
    except Exception as exc:
        result["overall"] = "FAIL"
        result["fatalError"] = str(exc)
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(result["overall"])
    return 0 if result["overall"] != "FAIL" else 1

if __name__ == "__main__":
    raise SystemExit(main())
