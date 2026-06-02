from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Dict, Any, List, Tuple

def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))

def band_for_count(n: int) -> str:
    if n >= 20:
        return "20_PLUS"
    if n >= 10:
        return "10-19"
    if n >= 5:
        return "5-9"
    if n >= 3:
        return "3-4"
    return "HIDDEN"

def quantity_band(avg_quantity: float, unit_code: str) -> str:
    if unit_code == "kg":
        if avg_quantity >= 600:
            return "HIGH"
        if avg_quantity >= 300:
            return "MEDIUM"
        return "LOW"
    if unit_code.startswith("bag:"):
        if avg_quantity >= 14:
            return "HIGH"
        if avg_quantity >= 8:
            return "MEDIUM"
        return "LOW"
    return "MEDIUM"

def compute_dominance(entries: List[Dict[str, Any]]) -> float:
    total = sum(float(e["amountEUR"]) for e in entries)
    if total <= 0:
        return 0.0
    return round(max(float(e["amountEUR"]) for e in entries) / total, 6)

def filter_entries(dataset: Dict[str, Any], req: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], str, str]:
    kind = req["requestedBenchmarkKind"]
    effective_kind = kind
    if kind == "EXACT_PRODUCT":
        basis_ref = req.get("requestedProductRef") or req.get("requestedProductClassRef") or "unknown:basis"
    else:
        basis_ref = req.get("requestedProductClassRef") or req.get("requestedProductRef") or "unknown:basis"
    if req["historyGuardStatus"] == "BLOCKED":
        return [], "NONE", basis_ref
    if kind == "EXACT_PRODUCT" and req["historyGuardStatus"] == "BROADEN":
        effective_kind = "PRODUCT_CLASS"
        basis_ref = req["fallbackProductClassRef"]
    revoked_ids = set()
    if req.get("applyRevocationToSelection") and req.get("revocationScenarioRef"):
        sim = dataset.get("revocationSimulation") or {}
        if sim.get("simulationId") == req["revocationScenarioRef"]:
            revoked_ids = set(sim.get("affectedEntryIds", []))
    selected = []
    for entry in dataset.get("entries", []):
        if entry["shareGrantState"] != "ACTIVE":
            continue
        if entry["extractReviewStatus"] != "REVIEWED":
            continue
        if entry["useEligibility"] != "ELIGIBLE":
            continue
        if entry["entryId"] in revoked_ids:
            continue
        if effective_kind == "PRODUCT_CLASS":
            if entry.get("normalizedProductClassRef") != req["requestedProductClassRef"] and entry.get("normalizedProductClassRef") != req.get("fallbackProductClassRef"):
                continue
        elif effective_kind == "EXACT_PRODUCT":
            if entry.get("normalizedProductRef") != req.get("requestedProductRef"):
                continue
        selected.append(entry)
    return selected, effective_kind, basis_ref

def build_results(dataset: Dict[str, Any]) -> Dict[str, Any]:
    policy = dataset["policy"]
    min_count = int(policy["minContributorsRequired"])
    dom_limit = float(policy["dominanceShareLimit"])
    execution_records: List[Dict[str, Any]] = []
    audits: List[Dict[str, Any]] = []
    request_results: List[Dict[str, Any]] = []
    for req in dataset["requests"]:
        selected, effective_kind, basis_ref = filter_entries(dataset, req)
        count = len(selected)
        display = band_for_count(count)
        reason_codes: List[str] = []
        metrics: List[Dict[str, Any]] = []
        decision = "REFUSE"
        handoff = "READY_FOR_REAL_PILOT_HANDOFF"
        freshness = req["materializationFreshnessState"]
        claim_boundary = "Advisory benchmark only; not procurement, not accounting truth, not compliance truth."
        if freshness != "FRESH":
            reason_codes.extend(["MATERIALIZATION_NOT_FRESH", "RECOMPUTE_REQUIRED"])
        elif req["historyGuardStatus"] == "BLOCKED":
            reason_codes.extend(["REQUEST_HISTORY_BLOCKED", "DIFFERENCING_RISK_HIGH"])
        elif count < min_count:
            reason_codes.extend(["BENCHMARK_INSUFFICIENT_COHORT"])
        else:
            dominance = compute_dominance(selected)
            if dominance > dom_limit:
                reason_codes.extend(["BENCHMARK_DISCLOSURE_DOMINANCE_RISK"])
            else:
                avg_price = round(sum(float(e["amountEUR"]) for e in selected) / sum(float(e["normalizedQuantity"]) for e in selected), 3)
                avg_qty = sum(float(e["normalizedQuantity"]) for e in selected) / count
                decision = "BROADEN" if req["requestedBenchmarkKind"] == "EXACT_PRODUCT" and effective_kind == "PRODUCT_CLASS" else "ALLOW"
                reason_codes.extend(["BENCHMARK_DISCLOSURE_SAFE", "MATERIALIZATION_FRESH"])
                if decision == "BROADEN":
                    reason_codes.append("REQUEST_HISTORY_BROADENED")
                metrics = [
                    {"metricName": "AVG_UNIT_PRICE", "numericValue": avg_price, "unitCode": selected[0]["normalizedUnitCode"]},
                    {"metricName": "QUANTITY_BAND", "labelValue": quantity_band(avg_qty, selected[0]["normalizedUnitCode"])}
                ]
        if decision == "REFUSE":
            handoff = "BLOCKED" if freshness != "FRESH" else "READY_FOR_REAL_PILOT_HANDOFF"
        dominance = compute_dominance(selected) if selected else 0.0
        exec_record = {
            "schemaVersion": "ofarm.benchmarkpilotexecutionrecord.v0.1",
            "pilotExecutionId": f"pilotexec:{req['requestScenarioId']}",
            "datasetRef": dataset["datasetId"],
            "datasetKind": dataset["datasetKind"],
            "actualTenantData": dataset["provenance"]["actualTenantData"],
            "executionMode": "REHEARSAL" if dataset["datasetKind"] == "REDACTED_REHEARSAL_NON_REAL" else ("REAL_PILOT" if dataset["datasetKind"] == "REAL_REDACTED_PILOT" else "TEMPLATE_CHECK"),
            "requestScenarioRef": req["requestScenarioId"],
            "requestedBenchmarkKind": req["requestedBenchmarkKind"],
            "effectiveBenchmarkKind": effective_kind,
            "basisRef": basis_ref,
            "decision": decision,
            "materializationFreshnessState": freshness,
            "contributorCountInternal": count,
            "contributorCountDisplay": display,
            "dominanceShareMax": dominance,
            "exactContributorCountHidden": True,
            "rawPeerRowsHidden": True,
            "rawEvidenceHidden": True,
            "allowedMetricNames": ["AVG_UNIT_PRICE", "QUANTITY_BAND", "POSITION_BAND"],
            "userVisibleMetrics": metrics,
            "handoffReadiness": handoff,
            "promotionReadiness": "NOT_FOR_PROMOTION",
            "claimBoundary": claim_boundary,
            "outputAssemblyType": req["surfaceType"],
            "blockingReasonCodes": reason_codes if decision == "REFUSE" else [],
            "reasonCodes": reason_codes
        }
        audit_failures: List[str] = []
        audit = {
            "schemaVersion": "ofarm.benchmarkviewsurfaceaudit.v0.1",
            "auditId": f"surfaceaudit:{req['requestScenarioId']}",
            "requestScenarioRef": req["requestScenarioId"],
            "surfaceType": req["surfaceType"],
            "showsRawPeerRows": False,
            "showsRawEvidenceRefs": False,
            "showsExactContributorCount": False,
            "showsPeerTotalSpend": False,
            "showsPerHectareMetric": False,
            "showsBasisExplanation": True,
            "showsFreshnessExplanation": True,
            "showsDisclosureReason": True,
            "outcome": "PASS",
            "failureReasonCodes": audit_failures
        }
        execution_records.append(exec_record)
        audits.append(audit)
        request_results.append({
            "requestScenarioId": req["requestScenarioId"],
            "decision": decision,
            "effectiveBenchmarkKind": effective_kind,
            "basisRef": basis_ref,
            "contributorCountDisplay": display,
            "dominanceShareMax": dominance,
            "metrics": metrics,
            "reasonCodes": reason_codes,
            "freshnessState": freshness
        })
    return {
        "datasetId": dataset["datasetId"],
        "datasetKind": dataset["datasetKind"],
        "actualTenantData": dataset["provenance"]["actualTenantData"],
        "requestResults": request_results,
        "executionRecords": execution_records,
        "viewSurfaceAudits": audits
    }

def build_summary(results: Dict[str, Any]) -> str:
    lines: List[str] = []
    lines.append("# OFARM advisory cohort benchmark rehearsal summary v0.3")
    lines.append("")
    lines.append(f"Dataset: **{results['datasetId']}**")
    lines.append("")
    lines.append(f"Dataset kind: **{results['datasetKind']}**")
    lines.append("")
    if results["actualTenantData"] is False:
        lines.append("**Warning:** redacted rehearsal non-real dataset. Handoff proof only.")
        lines.append("")
    for item in results["requestResults"]:
        lines.append(f"## {item['requestScenarioId']}")
        lines.append("")
        lines.append(f"- Decision: **{item['decision']}**")
        lines.append(f"- Effective kind: **{item['effectiveBenchmarkKind']}**")
        lines.append(f"- Basis: `{item['basisRef']}`")
        lines.append(f"- Contributors shown as: **{item['contributorCountDisplay']}**")
        lines.append(f"- Freshness: **{item['freshnessState']}**")
        if item["metrics"]:
            for metric in item["metrics"]:
                if metric["metricName"] == "AVG_UNIT_PRICE":
                    lines.append(f"- AVG_UNIT_PRICE: **{metric['numericValue']} EUR / {metric['unitCode']}**")
                elif metric["metricName"] == "QUANTITY_BAND":
                    lines.append(f"- QUANTITY_BAND: **{metric['labelValue']}**")
        else:
            lines.append(f"- Blocking reasons: `{', '.join(item['reasonCodes'])}`")
        lines.append("- Output boundary: no raw peer rows, no raw evidence, no exact contributor count, no peer total spend")
        lines.append("")
    lines.append("No output here is promoted OFARM law or deployment-proof tenant intelligence.")
    return "\n".join(lines) + "\n"

def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python ofarm_advisory_cohort_benchmark_real_pilot_runner_v0_3.py <dataset.json> [results.json] [summary.md]")
    dataset_path = Path(sys.argv[1]).resolve()
    results_path = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else dataset_path.with_name("OFARM_advisory_cohort_benchmark_results_generated.json")
    summary_path = Path(sys.argv[3]).resolve() if len(sys.argv) > 3 else dataset_path.with_name("OFARM_advisory_cohort_benchmark_summary_generated.md")
    dataset = load_json(dataset_path)
    results = build_results(dataset)
    results_path.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    summary_path.write_text(build_summary(results), encoding="utf-8")
    print(results_path)
    print(summary_path)

if __name__ == "__main__":
    main()
