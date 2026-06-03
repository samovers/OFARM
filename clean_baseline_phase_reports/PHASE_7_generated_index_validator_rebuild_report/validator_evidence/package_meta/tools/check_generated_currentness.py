#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CURRENT = "OFARM2_2026-05-30_cp15_agentic_software_delivery_model_deployment_governance_merged_v0_2_final_currentness_normalized"
EXCLUDED_ROOT_ZIP = re.compile(r"^CLEAN_BASELINE_.*\.zip$")
STATUS_SELF_EXCLUSIONS = {"MANIFEST.csv", "MATERIAL_STATUS.csv", "MATERIAL_STATUS.json"}


def excluded(rel: str) -> bool:
    parts = rel.split("/")
    return (
        ".git" in parts
        or "__pycache__" in parts
        or parts[-1] == ".DS_Store"
        or parts[-1].endswith(".pyc")
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


def strip_generated(obj):
    if isinstance(obj, dict):
        return {
            k: strip_generated(v)
            for k, v in obj.items()
            if k not in {
                "generatedAt",
                "generatedOrCuratedAt",
                "derivedFrom",
                "doNotCiteAsIndependentSource",
                "doNotOverrideCanonicalAuthority",
                "semanticLawChanged",
            }
        }
    if isinstance(obj, list):
        return [strip_generated(v) for v in obj]
    return obj


def main() -> int:
    issues: list[str] = []
    current_files = set(files())
    material = load("MATERIAL_STATUS.json")
    records = material.get("records", [])
    records_by_path = {r["path"]: r for r in records}
    expected_status_files = current_files - STATUS_SELF_EXCLUSIONS

    if material.get("currentPackageIdentity") != CURRENT:
        issues.append("MATERIAL_STATUS.json currentPackageIdentity is stale")
    if set(records_by_path) != expected_status_files:
        issues.append("MATERIAL_STATUS.json does not match current package file set")

    authority = load("package_meta/generated/authority.index.json")
    expected_counts = dict(sorted(Counter(r["status"] for r in records).items()))
    if authority.get("counts") != expected_counts:
        issues.append("authority.index.json counts do not match MATERIAL_STATUS.json")
    expected_by_status: dict[str, list[str]] = defaultdict(list)
    for r in records:
        expected_by_status[r["status"]].append(r["path"])
    expected_by_status = {k: sorted(v) for k, v in expected_by_status.items() if v}
    actual_by_status = authority.get("recordsByStatus", {})
    for status, paths in expected_by_status.items():
        if actual_by_status.get(status) != paths:
            issues.append(f"authority.index.json records mismatch for status {status}")
            break

    materials = load("package_meta/generated/materials.index.json")
    if materials.get("fileCount") != len(current_files):
        issues.append("materials.index.json fileCount does not match current package tree")
    if materials.get("statusCounts") != expected_counts:
        issues.append("materials.index.json statusCounts do not match MATERIAL_STATUS.json")

    package_meta_index = load("package_meta/PACKAGE_META_INDEX.json")
    expected_pm = {
        p
        for p in current_files
        if p.startswith("package_meta/")
        and p not in {"package_meta/PACKAGE_META_INDEX.json", "package_meta/PACKAGE_META_INDEX.md"}
    }
    indexed_pm = {r.get("path") for r in package_meta_index.get("records", [])}
    if indexed_pm != expected_pm:
        issues.append("PACKAGE_META_INDEX.json path set does not match package_meta tree")
    for r in package_meta_index.get("records", []):
        path = r.get("path")
        if path in current_files and r.get("sha256") != sha256(path):
            issues.append(f"PACKAGE_META_INDEX.json hash drift: {path}")
            break

    mirror_pairs = [
        ("03_machine_contracts/CONTRACT_INDEX.json", "package_meta/generated/contracts.index.json"),
        ("SOURCE_INPUT_INDEX.json", "package_meta/generated/source_inputs.lock.json"),
        ("TRACEABILITY_INDEX.json", "package_meta/generated/traceability.index.json"),
    ]
    for source, generated in mirror_pairs:
        src = strip_generated(load(source))
        gen = strip_generated(load(generated))
        if gen != src:
            issues.append(f"{generated} is not a current derived mirror of {source}")

    example_src = load("03_machine_contracts/EXAMPLE_SCHEMA_MAP.json")
    example_gen = load("package_meta/generated/schema_example_map.json")
    if example_gen.get("records") != example_src.get("records"):
        issues.append("generated schema_example_map records do not match EXAMPLE_SCHEMA_MAP")

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
        if data.get("doNotCiteAsIndependentSource") is not True:
            issues.append(f"{rel} missing doNotCiteAsIndependentSource=true")
        if data.get("doNotOverrideCanonicalAuthority") is not True:
            issues.append(f"{rel} missing doNotOverrideCanonicalAuthority=true")
        if data.get("semanticLawChanged") is not False:
            issues.append(f"{rel} missing semanticLawChanged=false")
        if data.get("currentPackageIdentity") != CURRENT:
            issues.append(f"{rel} currentPackageIdentity is stale")

    source_map = load("CLEAN_BASELINE_GENERATED_VIEW_SOURCE_MAP.json")
    for rec in source_map.get("generatedViewRecords", []):
        if rec.get("status") != "CURRENT_DERIVED_VIEW":
            issues.append(f"generated view source map record not current: {rec.get('generatedPath')}")

    if issues:
        print("Generated currentness check: FAIL")
        for issue in issues:
            print(f"- {issue}")
        return 1
    print("Generated currentness check: OK")
    print(f"Checked generated indexes and material status in {REPO.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
