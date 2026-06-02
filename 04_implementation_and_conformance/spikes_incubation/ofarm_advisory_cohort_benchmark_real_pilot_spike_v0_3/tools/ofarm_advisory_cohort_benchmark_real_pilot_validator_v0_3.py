from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import List, Dict, Any

FORBIDDEN_KEY_FRAGMENTS = ("tax", "iban", "bank", "staffName", "personName", "governmentId", "email")

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

def _contains_forbidden_key(obj: Any, path: str = "") -> List[str]:
    hits: List[str] = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            kp = f"{path}.{k}" if path else k
            if any(fragment.lower() in k.lower() for fragment in FORBIDDEN_KEY_FRAGMENTS):
                hits.append(kp)
            hits.extend(_contains_forbidden_key(v, kp))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            hits.extend(_contains_forbidden_key(v, f"{path}[{i}]"))
    return hits

def validate_dataset(obj: Dict[str, Any]) -> Dict[str, Any]:
    checks: List[Dict[str, str]] = []
    def add(check_id: str, passed: bool, note: str) -> None:
        checks.append({"checkId": check_id, "outcome": "PASS" if passed else "FAIL", "note": note})
    required_top = ["datasetId","datasetKind","participantIdentityMode","provenance","policy","benchmarkWindow","requests","entries"]
    for key in required_top:
        add(f"TOPLEVEL_{key}", key in obj, f"Top-level key {key} present." if key in obj else f"Missing top-level key {key}.")
    add("IDENTITY_MODE_REDACTED", obj.get("participantIdentityMode") == "REDACTED_STABLE_REF", "participantIdentityMode must be REDACTED_STABLE_REF.")
    forbidden = _contains_forbidden_key(obj)
    add("NO_OBVIOUS_PII_KEYS", not forbidden, "No obvious forbidden key names present." if not forbidden else f"Forbidden key fragments found: {forbidden}.")
    dataset_kind = obj.get("datasetKind")
    actual = obj.get("provenance", {}).get("actualTenantData")
    template_only = bool(obj.get("templateOnly"))
    if dataset_kind == "REAL_REDACTED_TEMPLATE":
        add("TEMPLATE_HONESTY", template_only and actual is None, "Template datasets must be templateOnly and actualTenantData null.")
    elif dataset_kind == "REDACTED_REHEARSAL_NON_REAL":
        add("REHEARSAL_HONESTY", (not template_only) and actual is False, "Rehearsal dataset must be non-template and actualTenantData false.")
    elif dataset_kind == "REAL_REDACTED_PILOT":
        add("REAL_PILOT_HONESTY", (not template_only) and actual is True, "Real pilot dataset must be non-template and actualTenantData true.")
    else:
        add("DATASET_KIND_ALLOWED", False, f"Unsupported datasetKind {dataset_kind}.")
    entries = obj.get("entries", [])
    requests = obj.get("requests", [])
    add("HAS_REQUESTS", isinstance(requests, list) and len(requests) >= 1, "At least one request scenario required.")
    add("HAS_ENTRIES", isinstance(entries, list) and len(entries) >= 1, "At least one contribution entry required.")
    policy = obj.get("policy", {})
    min_count = int(policy.get("minContributorsRequired", 0) or 0)
    add("MIN_COUNT_REASONABLE", min_count >= 5, "minContributorsRequired should be >= 5 in this packet.")
    add("FORBIDDEN_METRICS_DECLARE_TOTAL_SPEND", "TOTAL_SPEND" in policy.get("forbiddenMetrics", []), "TOTAL_SPEND must remain forbidden.")
    counts_by_class: Dict[str, int] = {}
    counts_by_product: Dict[str, int] = {}
    valid_entries = 0
    for entry in entries:
        ok = True
        for req in ["entryId","participantRef","farmRef","shareGrantRef","shareGrantState","extractRef","extractReviewStatus","evidenceRef","useEligibility","revocationState","normalizedQuantity","normalizedUnitCode","amountEUR","normalizedProductClassRef"]:
            if req not in entry:
                ok = False
                break
        if not ok:
            continue
        if entry["shareGrantState"] != "ACTIVE":
            continue
        if entry["extractReviewStatus"] != "REVIEWED":
            continue
        if entry["useEligibility"] != "ELIGIBLE":
            continue
        valid_entries += 1
        counts_by_class[entry["normalizedProductClassRef"]] = counts_by_class.get(entry["normalizedProductClassRef"], 0) + 1
        if entry.get("normalizedProductRef"):
            counts_by_product[entry["normalizedProductRef"]] = counts_by_product.get(entry["normalizedProductRef"], 0) + 1
    add("HAS_REVIEWED_ACTIVE_ENTRIES", valid_entries >= 1, "At least one reviewed active entry required.")
    if dataset_kind == "REDACTED_REHEARSAL_NON_REAL":
        add("FERTILIZER_CLASS_COUNT_OK", counts_by_class.get("productclass:fertilizer:npk_15_15_15", 0) >= 5, "Rehearsal fertilizer class should have 5+ contributions.")
        add("SEED_EXACT_COUNT_OK", counts_by_product.get("product:seed:maize:hybrid_abc_treated_50k", 0) >= 5, "Rehearsal seed exact product should have 5+ contributions.")
    overall = "FAIL"
    if dataset_kind == "REAL_REDACTED_TEMPLATE":
        overall = "TEMPLATE_ONLY" if all(c["outcome"] == "PASS" for c in checks) else "FAIL"
    elif dataset_kind == "REDACTED_REHEARSAL_NON_REAL":
        overall = "READY_FOR_REHEARSAL" if all(c["outcome"] == "PASS" for c in checks) else "FAIL"
    elif dataset_kind == "REAL_REDACTED_PILOT":
        overall = "READY_FOR_REAL_PILOT_EXECUTION" if all(c["outcome"] == "PASS" for c in checks) else "FAIL"
    return {
        "datasetId": obj.get("datasetId"),
        "datasetKind": dataset_kind,
        "actualTenantData": actual,
        "templateOnly": template_only,
        "checks": checks,
        "overallOutcome": overall
    }

def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python ofarm_advisory_cohort_benchmark_real_pilot_validator_v0_3.py <dataset.json> [output.json]")
    dataset_path = Path(sys.argv[1]).resolve()
    out_path = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else None
    report = validate_dataset(load_json(dataset_path))
    text = json.dumps(report, indent=2)
    if out_path:
        out_path.write_text(text + "\n", encoding="utf-8")
    print(text)

if __name__ == "__main__":
    main()
