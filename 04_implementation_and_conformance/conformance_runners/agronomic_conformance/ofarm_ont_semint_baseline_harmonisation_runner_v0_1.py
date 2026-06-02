#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "04_implementation_and_conformance" / "OFARM_ont_semint_baseline_harmonisation_results_v0_1.json"

REQUIRED = {
    "00_active_baseline/OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md": [
        "ONT-SEMINT v0.3 baseline-harmonisation addendum",
        "schema-valid object shape",
        "ExternalRegistryVerificationTrace",
        "PassportView",
    ],
    "00_active_baseline/OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md": [
        "ONT-SEMINT v0.3 runtime-enforcement baseline addendum",
        "ReferenceResolutionReport",
        "external registry currentness",
        "Capability Manifest",
    ],
    "00_active_baseline/OFARM_Alignment_Register_v0_13.md": [
        "ONT-SEMINT v0.3 alignment supplement",
        "ReferenceResolutionManifest",
        "ExternalRegistryVerificationTrace",
        "TemporalFieldConformanceMatrix",
    ],
    "00_active_baseline/OFARM_post_gap_closure_readiness_gate_memo_v0_1.md": [
        "ONT-SEMINT v0.3 readiness-gate addendum",
        "IMPLEMENTATION-DIRECTED WITH BOUNDED DEBT",
        "live external registry integration",
    ],
    "00_active_baseline/OFARM_final_hostile_review_after_gap_closure_v0_1.md": [
        "ONT-SEMINT v0.3 hostile-review addendum",
        "no live Phytoweb integration is claimed",
        "implementation-directed with bounded debt",
    ],
}

NONCLAIM_TEXT = [
    "production runtime readiness",
    "live external registry integration",
    "external-standard readiness",
    "livestock",
]

def main() -> int:
    findings = []
    for rel, needles in REQUIRED.items():
        text = (ROOT / rel).read_text(encoding="utf-8", errors="ignore")
        for needle in needles:
            if needle not in text:
                findings.append({"artifact": rel, "status": "FAIL", "missing": needle})
    constitution = (ROOT / "00_active_baseline/OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md").read_text(encoding="utf-8", errors="ignore")
    for needle in NONCLAIM_TEXT:
        if needle.lower() not in constitution.lower():
            findings.append({"artifact": "Constitution", "status": "WARN", "missingNonClaimText": needle})
    overall = "PASS" if not any(f["status"] == "FAIL" for f in findings) else "FAIL"
    result = {
        "schemaVersion": "ofarm.ontSemintBaselineHarmonisationResults.v0.1",
        "date": "2026-05-14",
        "runner": Path(__file__).name,
        "overallStatus": overall,
        "baselineFilesChecked": len(REQUIRED),
        "findingCount": len(findings),
        "findings": findings,
        "notes": "Checks that ONT-SEMINT v0.3 baseline harmonisation text is present and preserves explicit non-claims."
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(overall)
    return 0 if overall == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
