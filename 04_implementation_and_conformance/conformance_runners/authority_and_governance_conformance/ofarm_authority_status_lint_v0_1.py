#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "04_implementation_and_conformance" / "OFARM_authority_status_lint_results_v0_1.json"
ACTIVE_DIRS = ["00_active_baseline", "01_companion_artifacts", "02_accepted_rfcs", "03_machine_contracts"]
FORBIDDEN_ACTIVE_PATTERNS = ["legacy_reference/", "reviewed_preimplementation_thread", "reviewed_regulatory_inspector_thread", "reviewed_ai_assistant", "reviewed_common_sense", "reviewed_farm_owner"]
ALLOWED_CONTEXT_TERMS = ["REVIEW_HOLDING", "read-only", "does not override", "not active law", "source context"]


def main() -> int:
    findings = []
    files_checked = 0
    for d in ACTIVE_DIRS:
        for p in (ROOT / d).rglob("*"):
            if not p.is_file() or p.suffix not in {".md", ".json"}:
                continue
            files_checked += 1
            text = p.read_text(encoding="utf-8", errors="ignore")
            for pattern in FORBIDDEN_ACTIVE_PATTERNS:
                if pattern in text:
                    context_ok = any(term in text for term in ALLOWED_CONTEXT_TERMS)
                    findings.append({
                        "artifact": str(p.relative_to(ROOT)),
                        "pattern": pattern,
                        "status": "WARN_CONTEXTUAL_REFERENCE" if context_ok else "FAIL_POTENTIAL_AUTHORITY_DRIFT",
                        "note": "Active substance should not cite review-holding or legacy material as active law."
                    })
    fail_count = sum(1 for f in findings if f["status"].startswith("FAIL"))
    result = {
        "schemaVersion": "ofarm.authorityStatusLintResults.v0.1",
        "date": "2026-05-14",
        "runner": Path(__file__).name,
        "overallStatus": "PASS" if fail_count == 0 else "FAIL",
        "filesChecked": files_checked,
        "findingCount": len(findings),
        "failCount": fail_count,
        "findings": findings,
        "notes": "Checks active authority folders for accidental review-holding or legacy authority import. Package metadata and explicit authority maps are not treated as semantic law."
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(result["overallStatus"])
    return 0 if result["overallStatus"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
