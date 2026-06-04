#!/usr/bin/env python3
from __future__ import annotations

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


def load(rel: str):
    return json.loads((REPO / rel).read_text(encoding="utf-8"))


def main() -> int:
    issues: list[str] = []

    for d in CP_ROOT_DIRS:
        if (REPO / "package_meta" / d).exists():
            issues.append(f"controlled-amendment evidence folder reappeared at package_meta root: {d}")
        if not (REPO / "package_meta/history/controlled_amendments" / d).exists():
            issues.append(f"controlled-amendment evidence folder missing from history lane: {d}")

    if not (REPO / "03_machine_contracts/schemas").is_dir():
        issues.append("03_machine_contracts/schemas/ missing or moved")
    if not (REPO / "03_machine_contracts/drafts_non_default").is_dir():
        issues.append("03_machine_contracts/drafts_non_default/ missing or moved")

    for rel in [
        "legacy_reference/folder.status.json",
        "07_linked_domain_architectures/folder.status.json",
    ]:
        data = load(rel)
        if data.get("currentPackageIdentity") != CURRENT:
            issues.append(f"{rel} currentPackageIdentity is stale")
        if data.get("searchDefault") is not False:
            issues.append(f"{rel} must remain searchDefault=false")
        if data.get("activeLaw") is not False:
            issues.append(f"{rel} must not be active law")

    entry = load("CURRENT_ACTIVE_ENTRYPOINT.json")
    expected = "package_meta/history/controlled_amendments/cp15_merge_2026_05_30/CP15_FINAL_ACCEPTANCE_GATE.md"
    if entry.get("cp15MergeEvidence") != expected:
        issues.append("CURRENT_ACTIVE_ENTRYPOINT.json cp15MergeEvidence does not point to relocated CP15 final acceptance gate")
    if not (REPO / expected).exists():
        issues.append("relocated CP15 final acceptance gate does not exist")

    family = load("03_machine_contracts/CONTRACT_FAMILY_CURRENTNESS.json")
    if family.get("draftContractsPromoted") is not False:
        issues.append("CONTRACT_FAMILY_CURRENTNESS.json does not declare draftContractsPromoted=false")
    for fam in family.get("families", []):
        current_default = fam.get("currentDefaultSchema")
        if current_default and "draft" in current_default.lower():
            issues.append(f"draft/non-default schema promoted as current default: {current_default}")
            break

    draft_index = load("03_machine_contracts/DRAFT_NON_DEFAULT_INDEX.json")
    if draft_index.get("draftContractsPromoted") is not False:
        issues.append("DRAFT_NON_DEFAULT_INDEX.json does not declare draftContractsPromoted=false")
    for rec in draft_index.get("records", []):
        if rec.get("promotedToCurrentDefault") not in {False, None}:
            issues.append(f"draft record promoted to current/default: {rec.get('path')}")
            break

    generated_views = [
        "package_meta/generated/authority.index.json",
        "package_meta/generated/materials.index.json",
        "package_meta/generated/contracts.index.json",
        "package_meta/generated/schema_example_map.json",
        "package_meta/generated/source_inputs.lock.json",
        "package_meta/generated/traceability.index.json",
        "package_meta/generated/handover_gate.json",
    ]
    for rel in generated_views:
        data = load(rel)
        if data.get("doNotCiteAsIndependentSource") is not True:
            issues.append(f"{rel} missing doNotCiteAsIndependentSource")
        if data.get("doNotOverrideCanonicalAuthority") is not True:
            issues.append(f"{rel} missing doNotOverrideCanonicalAuthority")
        if data.get("semanticLawChanged") is not False:
            issues.append(f"{rel} does not declare semanticLawChanged=false")

    material = load("MATERIAL_STATUS.json")
    for record in material.get("records", []):
        path = record.get("path", "")
        if (path == "README.md" or path.endswith("/README.md")) and record.get("activeLaw") is True:
            issues.append(f"README metadata is file-level active law in MATERIAL_STATUS.json: {path}")
        if (path == "folder.status.json" or path.endswith("/folder.status.json")) and record.get("activeLaw") is True:
            issues.append(f"folder.status metadata is file-level active law in MATERIAL_STATUS.json: {path}")
        if ("/current/" in path or "/currentness/" in path) and record.get("activeLaw") is True:
            issues.append(f"current reader/currentness view is file-level active law in MATERIAL_STATUS.json: {path}")
        if path.startswith("package_meta/generated/") and record.get("activeLaw") is True:
            issues.append(f"generated view is file-level active law in MATERIAL_STATUS.json: {path}")
        if (
            path.startswith("package_meta/history/clean_baseline_migration/")
            or path.startswith("package_meta/release/final_clean_baseline/")
        ) and record.get("activeLaw") is True:
            issues.append(f"clean-baseline proof/release metadata is file-level active law in MATERIAL_STATUS.json: {path}")

    for rel, expected_status in {
        "03_machine_contracts/schemas/README.md": "MACHINE_CONTRACT_SCHEMA_NAVIGATION_METADATA",
        "03_machine_contracts/drafts_non_default/README.md": "MACHINE_CONTRACT_DRAFT_NAVIGATION_METADATA",
        "package_meta/history/controlled_amendments/README.md": "CONTROLLED_AMENDMENT_HISTORY",
        "package_meta/history/clean_baseline_migration/README.md": "CLEAN_BASELINE_MIGRATION_HISTORY",
        "package_meta/history/currentness_overlays/README.md": "CURRENTNESS_OVERLAY_HISTORY",
        "legacy_reference/README.md": "LEGACY_REFERENCE_CONTEXTUAL_ONLY",
        "07_linked_domain_architectures/README.md": "LINKED_DOMAIN_ARCHITECTURE_NON_DEFAULT",
    }.items():
        record = next((r for r in material.get("records", []) if r.get("path") == rel), None)
        if not record or record.get("status") != expected_status:
            issues.append(f"MATERIAL_STATUS.json does not classify {rel} as {expected_status}")

    pmi = load("package_meta/PACKAGE_META_INDEX.json")
    indexed_paths = {r.get("path") for r in pmi.get("records", [])}
    if any(path and re.search(r"package_meta/cp1[1-5]_", path) for path in indexed_paths):
        issues.append("PACKAGE_META_INDEX.json includes live CP11-CP15 root evidence paths")
    if not any(path and path.startswith("package_meta/history/controlled_amendments/") for path in indexed_paths):
        issues.append("PACKAGE_META_INDEX.json does not include controlled amendment history lane")
    if not any(path and path.startswith("package_meta/history/clean_baseline_migration/") for path in indexed_paths):
        issues.append("PACKAGE_META_INDEX.json does not include clean-baseline migration history lane")

    suite_text = (REPO / "package_meta/tools/run_repository_validation_suite.py").read_text(encoding="utf-8")
    for runner in [
        "ofarm_cp10_final_readiness_runner_v0_1.py",
        "ofarm_cp12_phase7_2_conformance_runner.py",
        "ofarm_cp13_phase7_2_conformance_runner.py",
        "ofarm_cp14_phase7_2_conformance_runner.py",
        "ofarm_cp15_phase7_2_conformance_runner.py",
    ]:
        if runner not in suite_text:
            issues.append(f"validation suite no longer preserves {runner}")

    for rel in [
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
    ]:
        text = (REPO / rel).read_text(encoding="utf-8")
        if "package_meta/cp15_merge_2026_05_30/CP15_MERGE_DECISION.md" in text:
            issues.append(f"default root/currentness file references missing CP15 merge decision: {rel}")

    if issues:
        print("Repository steward guardrail check: FAIL")
        for issue in issues:
            print(f"- {issue}")
        return 1
    print("Repository steward guardrail check: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
