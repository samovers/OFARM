#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CURRENT = "OFARM2_2026-05-30_cp15_agentic_software_delivery_model_deployment_governance_merged_v0_2_final_currentness_normalized"
TEXT_EXTS = {".md", ".txt", ".json", ".jsonl", ".py", ".yml", ".yaml", ".csv"}
OLD_PACKAGE_RE = re.compile(
    r"OFARM2_2026-05-(14|17|28|29|30)_[A-Za-z0-9_.-]+"
)
OLD_CP_ROOT_RE = re.compile(
    r"package_meta/(cp11_merge_2026_05_28|cp12_merge_2026_05_28|cp12_phase7|"
    r"cp12_steward_remediation_2026_05_28|cp13_merge_2026_05_29|"
    r"cp13_phase7_2026_05_29|cp13_steward_remediation_2026_05_29|"
    r"cp14_merge_2026_05_30|cp14_phase7_2026_05_30|"
    r"cp14_steward_remediation_2026_05_30|cp15_merge_2026_05_30|"
    r"cp15_phase7_2026_05_30|cp15_final_currentness_normalization_2026_05_30)"
)
EXCLUDED_ROOT_ZIP = re.compile(r"^CLEAN_BASELINE_.*\.zip$")
REPORT_SELF = {"REPOSITORY_CROSS_REFERENCE_SCAN.json", "REPOSITORY_CROSS_REFERENCE_SCAN.md"}


def excluded(rel: str) -> bool:
    parts = rel.split("/")
    return (
        ".git" in parts
        or "__pycache__" in parts
        or parts[-1] == ".DS_Store"
        or parts[-1].endswith(".pyc")
        or rel.startswith("clean_baseline_phase_reports/")
        or rel in REPORT_SELF
        or ("/" not in rel and EXCLUDED_ROOT_ZIP.match(rel) is not None)
    )


def files() -> list[str]:
    return sorted(
        p.relative_to(REPO).as_posix()
        for p in REPO.rglob("*")
        if p.is_file() and not excluded(p.relative_to(REPO).as_posix())
    )


def history_or_provenance(path: str, line: str) -> bool:
    lowered = line.lower()
    return (
        path.startswith("package_meta/history/")
        or path.startswith("package_meta/release/final_clean_baseline/")
        or path.startswith("package_meta/final_validation_")
        or path.startswith("package_meta/consolidation_")
        or path.startswith("package_meta/preimplementation_final_consolidation_")
        or path.startswith("package_meta/ontology_semint_")
        or path.startswith("package_meta/agentic_ai_world_model_consolidation_")
        or path.startswith("package_meta/predevelopment_ai_agent_ready_amendment_")
        or path.startswith("package_meta/repository_cleanup_")
        or path.startswith("package_meta/repository_handover_publication_layer_")
        or path.startswith("package_meta/repository_steward_")
        or path.startswith("package_meta/tools/")
        or path.startswith("package_meta/release_profiles/")
        or path.startswith("legacy_reference/")
        or path.startswith("04_implementation_and_conformance/historical_archive/")
        or "/controlled_promotion_evidence/" in path
        or "/examples_and_fixtures/" in path
        or path.startswith("05_project_handoff_and_prompts/prompts/")
        or path.startswith("05_project_handoff_and_prompts/eval_datasets/")
        or path.startswith("05_project_handoff_and_prompts/output_schemas/")
        or path.startswith("05_project_handoff_and_prompts/reports_and_maps/")
        or path.startswith("05_project_handoff_and_prompts/review_runs/")
        or path.startswith("06_active_supporting_research/incubation_and_candidate_decisions/")
        or path.startswith("06_active_supporting_research/source_inputs/")
        or path.startswith("06_active_supporting_research/syntheses/")
        or path.startswith("archive/")
        or path.endswith("folder.status.json")
        or path == "03_machine_contracts/DRAFT_NON_DEFAULT_INDEX_CP11_EXCERPT.md"
        or path in {"03_machine_contracts/PATH_REMAPS.json", "CLEAN_BASELINE_RELOCATION_MAP.json"}
        or path.startswith("CLEAN_BASELINE_")
        or path.startswith("DEV_AUDIT_RELEASE_PROFILE_SPLIT_REPORT")
        or "oldpath" in lowered
        or "previouspackage" in lowered
        or "sourcepackage" in lowered
        or "historical" in lowered
        or "provenance" in lowered
        or "final_clean_baseline" in lowered
        or "release profile" in lowered
        or "external release asset" in lowered
        or "missing" in lowered
        or "not create" in lowered
        or "not point" in lowered
        or "closed" in lowered
    )


def scan() -> dict:
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    json_errors = []
    old_packages = []
    old_paths = []
    cp15_decision_refs = []
    rels = files()

    for rel in rels:
        p = REPO / rel
        if p.suffix.lower() == ".json":
            try:
                json.loads(p.read_text(encoding="utf-8"))
            except Exception as exc:
                json_errors.append({"path": rel, "error": str(exc)})
        if p.suffix.lower() not in TEXT_EXTS:
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        for lineno, line in enumerate(text.splitlines(), 1):
            for match in OLD_PACKAGE_RE.finditer(line):
                value = match.group(0)
                if value == CURRENT:
                    continue
                allowed = history_or_provenance(rel, line)
                old_packages.append(
                    {
                        "path": rel,
                        "line": lineno,
                        "match": value,
                        "text": line.strip()[:240],
                        "classification": "HISTORY_ALLOWED" if allowed else "NEEDS_REVIEW",
                    }
                )
            for match in OLD_CP_ROOT_RE.finditer(line):
                allowed = history_or_provenance(rel, line)
                old_paths.append(
                    {
                        "path": rel,
                        "line": lineno,
                        "match": match.group(0),
                        "text": line.strip()[:240],
                        "classification": "PROVENANCE_ALLOWED" if allowed else "BLOCKER_STALE_CURRENT_FIELD",
                    }
                )
            if "CP15_MERGE_DECISION.md" in line:
                allowed = history_or_provenance(rel, line)
                cp15_decision_refs.append(
                    {
                        "path": rel,
                        "line": lineno,
                        "text": line.strip()[:240],
                        "classification": "HISTORY_ALLOWED" if allowed else "BLOCKER_STALE_CURRENT_FIELD",
                    }
                )

    blockers = [
        *[x for x in old_packages if x["classification"] == "NEEDS_REVIEW"],
        *[x for x in old_paths if x["classification"].startswith("BLOCKER")],
        *[x for x in cp15_decision_refs if x["classification"].startswith("BLOCKER")],
    ]
    return {
        "schemaVersion": "ofarm.repositoryCrossReferenceScan.v0.2.cleanBaseline",
        "generatedAt": now,
        "currentPackageIdentity": CURRENT,
        "package": CURRENT,
        "latestControlledAmendment": "CP15",
        "activeLaw": False,
        "doesNotOverrideActiveBaseline": True,
        "status": "PASS" if not blockers and not json_errors else "FAIL",
        "summary": {
            "fileCount": len(rels),
            "jsonParseErrors": len(json_errors),
            "oldPackageStringMatches": len(old_packages),
            "oldPackageStringBlockers": len([x for x in old_packages if x["classification"] == "NEEDS_REVIEW"]),
            "oldCpRootPathMatches": len(old_paths),
            "oldCpRootPathBlockers": len([x for x in old_paths if x["classification"].startswith("BLOCKER")]),
            "cp15MergeDecisionReferences": len(cp15_decision_refs),
            "cp15MergeDecisionReferenceBlockers": len(
                [x for x in cp15_decision_refs if x["classification"].startswith("BLOCKER")]
            ),
        },
        "actionableFindings": {
            "jsonParseErrors": json_errors[:100],
            "oldPackageStringBlockers": [x for x in old_packages if x["classification"] == "NEEDS_REVIEW"][:100],
            "oldCpRootPathBlockers": [x for x in old_paths if x["classification"].startswith("BLOCKER")][:100],
            "cp15MergeDecisionReferenceBlockers": [
                x for x in cp15_decision_refs if x["classification"].startswith("BLOCKER")
            ][:100],
        },
        "allowedHistoricalOrProvenanceFindings": {
            "oldPackageStrings": [x for x in old_packages if x["classification"] != "NEEDS_REVIEW"][:200],
            "oldCpRootPaths": [x for x in old_paths if not x["classification"].startswith("BLOCKER")][:200],
            "cp15MergeDecisionReferences": [
                x for x in cp15_decision_refs if not x["classification"].startswith("BLOCKER")
            ][:50],
        },
        "generatedViewPolicy": {
            "generatedViewsDoNotOverrideCanonicalAuthority": True,
            "generatedViewsAreNotIndependentTruth": True,
        },
    }


def write_report(report: dict) -> None:
    (REPO / "REPOSITORY_CROSS_REFERENCE_SCAN.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    summary = report["summary"]
    md = [
        "# Repository Cross-Reference Scan",
        "",
        f"Current package: `{CURRENT}`.",
        "",
        f"Status: **{report['status']}**",
        "",
        f"Files scanned: {summary['fileCount']}",
        f"Old CP root path blockers: {summary['oldCpRootPathBlockers']}",
        f"CP15 merge-decision reference blockers: {summary['cp15MergeDecisionReferenceBlockers']}",
        "",
    ]
    (REPO / "REPOSITORY_CROSS_REFERENCE_SCAN.md").write_text("\n".join(md), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = scan()
    if args.write:
        write_report(report)
        print(f"Repository cross-reference scan written: {report['status']}")
        return 0 if report["status"] == "PASS" else 1

    existing = json.loads((REPO / "REPOSITORY_CROSS_REFERENCE_SCAN.json").read_text(encoding="utf-8"))
    comparable_existing = dict(existing)
    comparable_report = dict(report)
    comparable_existing.pop("generatedAt", None)
    comparable_report.pop("generatedAt", None)
    if comparable_existing != comparable_report:
        print("Repository cross-reference check: FAIL")
        print("- REPOSITORY_CROSS_REFERENCE_SCAN.json is not current with live scan")
        return 1
    if report["status"] != "PASS":
        print("Repository cross-reference check: FAIL")
        print("- fresh scan has blockers")
        return 1
    print("Repository cross-reference check: OK")
    print(f"Checked cross-references in {REPO.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
