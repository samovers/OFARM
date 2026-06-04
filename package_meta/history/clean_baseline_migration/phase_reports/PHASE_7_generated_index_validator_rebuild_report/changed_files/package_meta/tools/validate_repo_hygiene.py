#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CURRENT = "OFARM2_2026-05-30_cp15_agentic_software_delivery_model_deployment_governance_merged_v0_2_final_currentness_normalized"
CP_ROOT_DIRS = [
    "cp11_merge_2026_05_28",
    "cp12_merge_2026_05_28",
    "cp12_phase7",
    "cp12_steward_remediation_2026_05_28",
    "cp13_merge_2026_05_29",
    "cp13_phase7_2026_05_29",
    "cp13_steward_remediation_2026_05_29",
    "cp14_merge_2026_05_30",
    "cp14_phase7_2026_05_30",
    "cp14_steward_remediation_2026_05_30",
    "cp15_merge_2026_05_30",
    "cp15_phase7_2026_05_30",
    "cp15_final_currentness_normalization_2026_05_30",
]
EXCLUDED_ROOT_ZIP = re.compile(r"^CLEAN_BASELINE_.*\.zip$")


def excluded(rel: str) -> bool:
    parts = rel.split("/")
    name = parts[-1]
    return (
        ".git" in parts
        or "__pycache__" in parts
        or name == ".DS_Store"
        or name.endswith(".pyc")
        or rel.startswith("clean_baseline_phase_reports/")
        or ("/" not in rel and EXCLUDED_ROOT_ZIP.match(rel) is not None)
    )


def files() -> list[str]:
    return sorted(
        p.relative_to(REPO).as_posix()
        for p in REPO.rglob("*")
        if p.is_file() and not excluded(p.relative_to(REPO).as_posix())
    )


def load(rel: str):
    return json.loads((REPO / rel).read_text(encoding="utf-8"))


def sha256(rel: str) -> str:
    h = hashlib.sha256()
    with (REPO / rel).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def assert_json_view(rel: str, issues: list[str]) -> None:
    data = load(rel)
    if data.get("doNotOverrideCanonicalAuthority") is not True:
        issues.append(f"{rel} does not declare doNotOverrideCanonicalAuthority=true")
    if data.get("semanticLawChanged") is not False:
        issues.append(f"{rel} does not declare semanticLawChanged=false")


def main() -> int:
    issues: list[str] = []
    current_files = set(files())

    forbidden = [p for p in REPO.rglob("*") if p.name == ".DS_Store" or "__pycache__" in p.parts or p.suffix == ".pyc"]
    if forbidden:
        issues.append(f"forbidden cache/OS files present: {[str(p.relative_to(REPO)) for p in forbidden[:20]]}")

    for rel in [
        "00_active_baseline/current/CURRENT_BASELINE_VIEW.json",
        "01_companion_artifacts/current/CURRENT_COMPANION_ARTIFACTS_VIEW.json",
        "02_accepted_rfcs/current/CURRENT_ACCEPTED_RFC_VIEW.json",
        "03_machine_contracts/currentness/CURRENT_MACHINE_CONTRACTS_VIEW.json",
    ]:
        if rel not in current_files:
            issues.append(f"missing current reader/currentness view: {rel}")
        else:
            assert_json_view(rel, issues)

    for rel in [
        "00_active_baseline/OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md",
        "00_active_baseline/OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md",
        "00_active_baseline/OFARM_Alignment_Register_v0_13.md",
        "00_active_baseline/OFARM_post_gap_closure_readiness_gate_memo_v0_1.md",
        "00_active_baseline/OFARM_final_hostile_review_after_gap_closure_v0_1.md",
    ]:
        if rel not in current_files:
            issues.append(f"missing canonical active baseline file: {rel}")

    for cp_dir in CP_ROOT_DIRS:
        if (REPO / "package_meta" / cp_dir).exists():
            issues.append(f"CP package-meta evidence folder remains at root: package_meta/{cp_dir}")

    expected_cp15 = "package_meta/history/controlled_amendments/cp15_merge_2026_05_30/CP15_FINAL_ACCEPTANCE_GATE.md"
    if not (REPO / expected_cp15).exists():
        issues.append(f"missing relocated CP15 final acceptance gate: {expected_cp15}")
    entrypoint = load("CURRENT_ACTIVE_ENTRYPOINT.json")
    if entrypoint.get("cp15MergeEvidence") != expected_cp15:
        issues.append(f"cp15MergeEvidence is not the relocated CP15 final acceptance gate: {entrypoint.get('cp15MergeEvidence')}")

    for rel in [
        "03_machine_contracts/schemas",
        "03_machine_contracts/drafts_non_default",
        "legacy_reference",
        "07_linked_domain_architectures",
        "package_meta/history/controlled_amendments",
        "package_meta/history/currentness_overlays",
    ]:
        if not (REPO / rel).exists():
            issues.append(f"required lane missing: {rel}")

    for rel in ["legacy_reference/folder.status.json", "07_linked_domain_architectures/folder.status.json"]:
        data = load(rel)
        if data.get("searchDefault") is not False or data.get("activeLaw") is not False:
            issues.append(f"{rel} must be non-default and not active law")

    material = load("MATERIAL_STATUS.json")
    if material.get("currentPackageIdentity") != CURRENT:
        issues.append("MATERIAL_STATUS.json currentPackageIdentity is stale")
    material_by_path = {r["path"]: r for r in material.get("records", [])}
    expected_status_files = current_files - {"MANIFEST.csv", "MATERIAL_STATUS.csv", "MATERIAL_STATUS.json"}
    if set(material_by_path) != expected_status_files:
        issues.append("MATERIAL_STATUS.json path set does not match current package tree")

    with (REPO / "MATERIAL_STATUS.csv").open(newline="", encoding="utf-8") as f:
        csv_paths = {r["path"] for r in csv.DictReader(f)}
    if csv_paths != expected_status_files:
        issues.append("MATERIAL_STATUS.csv path set does not match current package tree")

    with (REPO / "MANIFEST.csv").open(newline="", encoding="utf-8") as f:
        manifest_rows = list(csv.DictReader(f))
    if {r["path"] for r in manifest_rows} != current_files - {"MANIFEST.csv"}:
        issues.append("MANIFEST.csv path set does not match current package tree")
    for row in manifest_rows[:]:
        rel = row["path"]
        if rel in current_files and row.get("sha256") != sha256(rel):
            issues.append(f"MANIFEST.csv hash drift: {rel}")
            break

    critical_statuses = {
        "00_active_baseline/current/CURRENT_BASELINE_VIEW.json": "CURRENT_READER_VIEW",
        "package_meta/history/controlled_amendments/README.md": "CONTROLLED_AMENDMENT_HISTORY",
        "package_meta/history/currentness_overlays/README.md": "CURRENTNESS_OVERLAY_HISTORY",
        "legacy_reference/README.md": "LEGACY_REFERENCE_CONTEXTUAL_ONLY",
        "07_linked_domain_architectures/README.md": "LINKED_DOMAIN_ARCHITECTURE_NON_DEFAULT",
    }
    for rel, expected in critical_statuses.items():
        if material_by_path.get(rel, {}).get("status") != expected:
            issues.append(f"material status for {rel} is not {expected}")

    for rel in [
        "package_meta/generated/authority.index.json",
        "package_meta/generated/materials.index.json",
        "package_meta/generated/contracts.index.json",
        "package_meta/generated/schema_example_map.json",
        "package_meta/generated/source_inputs.lock.json",
        "package_meta/generated/traceability.index.json",
        "package_meta/generated/handover_gate.json",
    ]:
        data = load(rel)
        if data.get("doNotCiteAsIndependentSource") is not True or data.get("doNotOverrideCanonicalAuthority") is not True:
            issues.append(f"generated view missing non-authoritative markers: {rel}")

    package_meta_index = load("package_meta/PACKAGE_META_INDEX.json")
    indexed = {r.get("path") for r in package_meta_index.get("records", [])}
    if any(p.startswith(f"package_meta/{d}/") for p in indexed for d in CP_ROOT_DIRS):
        issues.append("PACKAGE_META_INDEX.json still indexes CP evidence at package_meta root")
    if not any(p.startswith("package_meta/history/controlled_amendments/") for p in indexed):
        issues.append("PACKAGE_META_INDEX.json does not index controlled amendment history")

    family = load("03_machine_contracts/CONTRACT_FAMILY_CURRENTNESS.json")
    for fam in family.get("families", []):
        default = fam.get("currentDefaultSchema")
        if default and "draft" in default.lower():
            issues.append(f"draft schema marked current/default: {default}")
            break

    suite = (REPO / "package_meta/tools/run_repository_validation_suite.py").read_text(encoding="utf-8")
    for marker in ["cp10_final_readiness", "cp12_phase7_2", "cp13_phase7_2", "cp14_phase7_2", "cp15_phase7_2"]:
        if marker not in suite:
            issues.append(f"validation suite no longer preserves runner marker: {marker}")

    live_targets = [
        "README.md",
        "PROJECT_AUTHORITY.md",
        "ACTIVE_SUBSTANCE_README.md",
        "CURRENT_ACTIVE_ENTRYPOINT.md",
        "CURRENT_ACTIVE_ENTRYPOINT.json",
        "AGENTS.md",
        "AGENT_NAVIGATION.md",
        "llms.txt",
        "DEVELOPMENT_HANDOVER.md",
        "CURRENT_DELTA.md",
        "CURRENT_PACKAGE_CHANGELOG.md",
    ]
    for rel in live_targets:
        if "CP15_MERGE_DECISION.md" in (REPO / rel).read_text(encoding="utf-8"):
            issues.append(f"default live file references CP15_MERGE_DECISION.md: {rel}")

    if issues:
        print("Repository hygiene check: FAIL")
        for issue in issues:
            print(f"- {issue}")
        return 1
    print("Repository hygiene check: OK")
    print(f"Checked {len(current_files)} package files in {REPO.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
