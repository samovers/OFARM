#!/usr/bin/env python3
from __future__ import annotations
import importlib.util, json, sys
from pathlib import Path
from typing import Any

CP6 = Path(__file__).resolve().parents[1]
STUB_PATH = CP6 / "runtime_stub" / "ofarm_cp6_minimal_hostile_runtime_stub_v0_1.py"
FIXTURE_DIR = CP6 / "examples" / "hostile"
TRACE_DIR = CP6 / "trace_corpus" / "generated"
REPORT = CP6 / "conformance" / "validation_report.json"

spec = importlib.util.spec_from_file_location("cp6_stub", STUB_PATH)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = module
spec.loader.exec_module(module)
runtime = module.MinimalOFARMHostileRuntime()

def validate_case(case: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    exp = case["expected"]; trace = result["trace"]; cid = case["caseId"]
    def failure(msg): return {"caseId": cid, "scenarioKind": case["scenarioKind"], "status": "FAIL", "failure": msg}
    for flag in ["currentStateMutation","canonicalTruthMutation","acceptedEvidenceCreated","obligationCreated","complianceBlockerCreatedByRequestOnly"]:
        if exp.get(flag) is False and trace.get(flag):
            return failure(f"{flag} unexpectedly true")
    if exp.get("traceRetrievable") and not trace.get("traceRetrievable"):
        return failure("trace was not retrievable")
    br = exp.get("blockedReasonCode")
    if br and br not in [b.get("reasonCode") for b in trace.get("blockedActions", [])]:
        return failure(f"expected blocked reason {br}")
    limits = trace.get("resultQualification", {}).get("materialLimitations", [])
    missing = [x for x in exp.get("requiredMaterialLimitations", []) if x not in limits]
    if missing: return failure(f"missing limitations {missing}")
    if exp.get("governanceOutcome") and trace.get("governanceOutcome") != exp["governanceOutcome"]:
        return failure(f"expected governance outcome {exp['governanceOutcome']}, got {trace.get('governanceOutcome')}")
    if exp.get("toolStatus") and trace.get("toolOutcome", {}).get("status") != exp["toolStatus"]:
        return failure(f"expected tool status {exp['toolStatus']}, got {trace.get('toolOutcome', {}).get('status')}")
    return {"caseId": cid, "scenarioKind": case["scenarioKind"], "status": "PASS", "governanceOutcome": trace.get("governanceOutcome"), "blockedReasonCode": br, "traceId": trace.get("traceId")}

def main() -> int:
    TRACE_DIR.mkdir(parents=True, exist_ok=True)
    records = []
    for path in sorted(FIXTURE_DIR.glob("*.json")):
        case = json.loads(path.read_text(encoding="utf-8"))
        result = runtime.run_case(case)
        records.append(validate_case(case, result))
        (TRACE_DIR / f"OFARM_CP6_trace_{case['caseId']}_v0_1.json").write_text(json.dumps(result["trace"], indent=2) + "\n", encoding="utf-8")
    failures = [r for r in records if r["status"] != "PASS"]
    report = {
        "schemaVersion": "ofarm.cp6.validationReport.v0.1",
        "phase": "AAI-CP6",
        "status": "PASS" if not failures else "FAIL",
        "scope": "selected synthetic hostile runtime stub; not full Phase 9 and not production runtime evidence",
        "fixtureCount": len(records),
        "records": records,
        "failures": failures,
        "claimLimits": {
            "allowed": "minimal CP6 hostile runtime stub passed selected synthetic agentic gates" if not failures else "no conformance claim",
            "blocked": ["runtime AI-agent readiness","two-agent compatibility","autonomous compliance decisioning","world-model readiness","production readiness","external-standard readiness","full Phase 9 pass"]
        }
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "records": len(records), "failures": len(failures)}, indent=2))
    return 0 if not failures else 1

if __name__ == "__main__":
    raise SystemExit(main())
