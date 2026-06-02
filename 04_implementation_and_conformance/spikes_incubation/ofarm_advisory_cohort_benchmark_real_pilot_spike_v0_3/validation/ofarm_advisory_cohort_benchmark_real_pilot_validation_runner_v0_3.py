from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, Any, List, Tuple
from jsonschema import Draft202012Validator

HERE = Path(__file__).resolve().parent
SPIKE = HERE.parent
ROOT = SPIKE.parents[1]
SCHEMA_DIR = SPIKE / "experimental_machine_contracts" / "schemas"
POS_DIR = SPIKE / "experimental_machine_contracts" / "examples" / "positive"
NEG_DIR = SPIKE / "experimental_machine_contracts" / "examples" / "negative"
FIXTURE_DIR = SPIKE / "fixtures"
OUTPUT_DIR = SPIKE / "outputs"
TOOLS_DIR = SPIKE / "tools"
OUT = HERE / "OFARM_advisory_cohort_benchmark_real_pilot_validation_results_v0_3.txt"

SCHEMA_MAP = {
    "BenchmarkPilotExecutionRecord": "OFARM_BenchmarkPilotExecutionRecord_schema_v0_1.json",
    "BenchmarkViewSurfaceAudit": "OFARM_BenchmarkViewSurfaceAudit_schema_v0_1.json",
}

def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))

def infer_kind(obj: Dict[str, Any]) -> str:
    sv = obj.get("schemaVersion", "")
    if sv == "ofarm.benchmarkpilotexecutionrecord.v0.1":
        return "BenchmarkPilotExecutionRecord"
    if sv == "ofarm.benchmarkviewsurfaceaudit.v0.1":
        return "BenchmarkViewSurfaceAudit"
    raise ValueError(f"Cannot infer schema kind from schemaVersion={sv!r}")

def get_schema(kind: str) -> Dict[str, Any]:
    return load_json(SCHEMA_DIR / SCHEMA_MAP[kind])

def semantic_errors(kind: str, obj: Dict[str, Any]) -> List[str]:
    errs: List[str] = []
    if kind == "BenchmarkPilotExecutionRecord":
        if obj.get("datasetKind") == "REDACTED_REHEARSAL_NON_REAL" and obj.get("actualTenantData") is not False:
            errs.append("SEMANTIC: REDACTED_REHEARSAL_NON_REAL must carry actualTenantData=false.")
        if obj.get("datasetKind") == "REAL_REDACTED_TEMPLATE" and obj.get("actualTenantData") is not None:
            errs.append("SEMANTIC: REAL_REDACTED_TEMPLATE must carry actualTenantData=null.")
        if obj.get("decision") in {"ALLOW", "BROADEN"}:
            if obj.get("materializationFreshnessState") != "FRESH":
                errs.append("SEMANTIC: ALLOW/BROADEN requires FRESH materialization.")
            if obj.get("contributorCountInternal", 0) < 5:
                errs.append("SEMANTIC: ALLOW/BROADEN requires at least 5 contributors in this packet.")
            if obj.get("blockingReasonCodes"):
                errs.append("SEMANTIC: ALLOW/BROADEN may not carry blockingReasonCodes.")
        if obj.get("decision") == "REFUSE" and not obj.get("blockingReasonCodes"):
            errs.append("SEMANTIC: REFUSE must carry blockingReasonCodes.")
        if obj.get("effectiveBenchmarkKind") == "NONE" and obj.get("decision") != "REFUSE":
            errs.append("SEMANTIC: effectiveBenchmarkKind=NONE only valid for REFUSE.")
        if obj.get("requestedBenchmarkKind") == "EXACT_PRODUCT" and obj.get("effectiveBenchmarkKind") == "PRODUCT_CLASS" and obj.get("decision") != "BROADEN":
            errs.append("SEMANTIC: EXACT_PRODUCT -> PRODUCT_CLASS requires BROADEN decision.")
        for flag in ("exactContributorCountHidden", "rawPeerRowsHidden", "rawEvidenceHidden"):
            if obj.get(flag) is not True:
                errs.append(f"SEMANTIC: {flag} must remain true.")
        metric_names = {m.get("metricName") for m in obj.get("userVisibleMetrics", [])}
        if "TOTAL_SPEND" in metric_names or "PER_HECTARE_SPEND" in metric_names:
            errs.append("SEMANTIC: forbidden metrics may not appear on userVisibleMetrics.")
    elif kind == "BenchmarkViewSurfaceAudit":
        leak_flags = {
            "showsRawPeerRows": obj.get("showsRawPeerRows"),
            "showsRawEvidenceRefs": obj.get("showsRawEvidenceRefs"),
            "showsExactContributorCount": obj.get("showsExactContributorCount"),
            "showsPeerTotalSpend": obj.get("showsPeerTotalSpend"),
            "showsPerHectareMetric": obj.get("showsPerHectareMetric"),
        }
        if obj.get("outcome") == "PASS":
            bad = [k for k, v in leak_flags.items() if v]
            if bad:
                errs.append(f"SEMANTIC: PASS surface audit may not expose {bad}.")
            for required_flag in ("showsBasisExplanation", "showsFreshnessExplanation", "showsDisclosureReason"):
                if obj.get(required_flag) is not True:
                    errs.append(f"SEMANTIC: PASS surface audit requires {required_flag}=true.")
        if obj.get("outcome") == "FAIL" and not obj.get("failureReasonCodes"):
            errs.append("SEMANTIC: FAIL surface audit must carry failureReasonCodes.")
    return errs

def validate_object(obj: Dict[str, Any]) -> Tuple[bool, List[str]]:
    kind = infer_kind(obj)
    validator = Draft202012Validator(get_schema(kind))
    errors = [f"SCHEMA: {e.message}" for e in validator.iter_errors(obj)]
    errors.extend(semantic_errors(kind, obj))
    return len(errors) == 0, errors

def validate_examples() -> Tuple[bool, List[str], bool, List[str]]:
    pos_lines = ["POSITIVE EXAMPLES"]
    pos_ok = True
    for path in sorted(POS_DIR.glob("*.json")):
        obj = load_json(path)
        ok, errs = validate_object(obj)
        pos_ok &= ok
        if ok:
            pos_lines.append(f"- {path.name}: PASS")
        else:
            pos_lines.append(f"- {path.name}: FAIL")
            pos_lines.extend([f"    * {e}" for e in errs])
    neg_lines = ["\nNEGATIVE EXAMPLES"]
    neg_ok = True
    for path in sorted(NEG_DIR.glob("*.json")):
        obj = load_json(path)
        ok, errs = validate_object(obj)
        if ok:
            neg_ok = False
            neg_lines.append(f"- {path.name}: UNEXPECTED PASS")
        else:
            neg_lines.append(f"- {path.name}: EXPECTED FAIL")
            neg_lines.extend([f"    * {e}" for e in errs])
    return pos_ok, pos_lines, neg_ok, neg_lines

def run_tools() -> Tuple[bool, List[str]]:
    lines = ["\nTOOL EXECUTION"]
    py = sys.executable
    template = FIXTURE_DIR / "OFARM_advisory_cohort_benchmark_real_pilot_dataset_template_v0_3.json"
    rehearsal = FIXTURE_DIR / "OFARM_advisory_cohort_benchmark_redacted_rehearsal_dataset_v0_3.json"
    template_report = OUTPUT_DIR / "OFARM_advisory_cohort_benchmark_template_readiness_report_v0_3.json"
    rehearsal_report = OUTPUT_DIR / "OFARM_advisory_cohort_benchmark_rehearsal_readiness_report_v0_3.json"
    results_path = OUTPUT_DIR / "OFARM_advisory_cohort_benchmark_rehearsal_results_v0_3.json"
    summary_path = OUTPUT_DIR / "OFARM_advisory_cohort_benchmark_rehearsal_summary_v0_3.md"
    subprocess.run([py, str(TOOLS_DIR / "ofarm_advisory_cohort_benchmark_real_pilot_validator_v0_3.py"), str(template), str(template_report)], check=True)
    subprocess.run([py, str(TOOLS_DIR / "ofarm_advisory_cohort_benchmark_real_pilot_validator_v0_3.py"), str(rehearsal), str(rehearsal_report)], check=True)
    subprocess.run([py, str(TOOLS_DIR / "ofarm_advisory_cohort_benchmark_real_pilot_runner_v0_3.py"), str(rehearsal), str(results_path), str(summary_path)], check=True)
    t = load_json(template_report)
    r = load_json(rehearsal_report)
    ok = True
    if t.get("overallOutcome") != "TEMPLATE_ONLY":
        ok = False
        lines.append("- template_validator: FAIL")
        lines.append(f"    * Expected TEMPLATE_ONLY, got {t.get('overallOutcome')}.")
    else:
        lines.append("- template_validator: PASS")
    if r.get("overallOutcome") != "READY_FOR_REHEARSAL":
        ok = False
        lines.append("- rehearsal_validator: FAIL")
        lines.append(f"    * Expected READY_FOR_REHEARSAL, got {r.get('overallOutcome')}.")
    else:
        lines.append("- rehearsal_validator: PASS")
    if not results_path.exists() or not summary_path.exists():
        ok = False
        lines.append("- rehearsal_runner: FAIL")
        lines.append("    * Runner did not create expected outputs.")
    else:
        lines.append("- rehearsal_runner: PASS")
    return ok, lines

def validate_generated_outputs() -> Tuple[bool, List[str]]:
    lines = ["\nGENERATED OUTPUTS"]
    ok = True
    results = load_json(OUTPUT_DIR / "OFARM_advisory_cohort_benchmark_rehearsal_results_v0_3.json")
    exec_records = results.get("executionRecords", [])
    audits = results.get("viewSurfaceAudits", [])
    if len(exec_records) < 4:
        ok = False
        lines.append("- execution_records_count: FAIL")
        lines.append("    * Expected at least four execution records.")
    else:
        lines.append("- execution_records_count: PASS")
    for record in exec_records:
        obj_ok, errs = validate_object(record)
        if not obj_ok:
            ok = False
            lines.append(f"- {record.get('pilotExecutionId')}: FAIL")
            lines.extend([f"    * {e}" for e in errs])
    if ok:
        lines.append("- execution_records_schema_and_semantics: PASS")
    for audit in audits:
        obj_ok, errs = validate_object(audit)
        if not obj_ok:
            ok = False
            lines.append(f"- {audit.get('auditId')}: FAIL")
            lines.extend([f"    * {e}" for e in errs])
    if ok:
        lines.append("- surface_audits_schema_and_semantics: PASS")
    return ok, lines

def validate_root_runtime_records() -> Tuple[bool, List[str]]:
    lines = ["\nROOT RUNTIME RECORDS"]
    ok = True
    results = load_json(OUTPUT_DIR / "OFARM_advisory_cohort_benchmark_rehearsal_results_v0_3.json")
    pilots = load_json(ROOT / "04_implementation_and_conformance" / "OFARM_runtime_benchmark_pilot_execution_records_v0_3.json")
    surfaces = load_json(ROOT / "04_implementation_and_conformance" / "OFARM_runtime_benchmark_view_surface_records_v0_3.json")
    if len(pilots.get("records", [])) != len(results.get("executionRecords", [])):
        ok = False
        lines.append("- pilot_execution_records: FAIL")
        lines.append("    * Root pilot records count does not match generated execution records.")
    else:
        lines.append("- pilot_execution_records: PASS")
    if len(surfaces.get("records", [])) != len(results.get("viewSurfaceAudits", [])):
        ok = False
        lines.append("- view_surface_records: FAIL")
        lines.append("    * Root view surface records count does not match generated audits.")
    else:
        lines.append("- view_surface_records: PASS")
    if all(rec.get("promotionReadiness") == "NOT_FOR_PROMOTION" for rec in pilots.get("records", [])):
        lines.append("- promotion_block_preserved: PASS")
    else:
        ok = False
        lines.append("- promotion_block_preserved: FAIL")
        lines.append("    * All pilot execution records must preserve NOT_FOR_PROMOTION.")
    return ok, lines

def main() -> None:
    pos_ok, pos_lines, neg_ok, neg_lines = validate_examples()
    tools_ok, tools_lines = run_tools()
    out_ok, out_lines = validate_generated_outputs()
    root_ok, root_lines = validate_root_runtime_records()
    overall = pos_ok and neg_ok and tools_ok and out_ok and root_ok
    lines: List[str] = []
    lines.extend(pos_lines)
    lines.extend(neg_lines)
    lines.extend(tools_lines)
    lines.extend(out_lines)
    lines.extend(root_lines)
    lines.append("\nOVERALL")
    lines.append(f"Real-pilot handoff packet outcome: {'PASS' if overall else 'FAIL'}")
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(OUT)
    print("\n".join(lines))

if __name__ == "__main__":
    main()
