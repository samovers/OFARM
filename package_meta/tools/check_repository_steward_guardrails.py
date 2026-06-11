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
LOWER_AUTHORITY_LANES = [
    "02_accepted_rfcs",
    "01_companion_artifacts",
    "03_machine_contracts",
]
TEXT_SUFFIXES = {".json", ".md", ".txt", ".yaml", ".yml"}
AUTHORITY_CHANGE_RE = re.compile(
    r"\b(overrid(?:e|es|den|ing)?|replac(?:e|es|ed|ing)?|supersed(?:e|es|ed|ing)?|"
    r"redefin(?:e|es|ed|ing)?)\b",
    re.IGNORECASE,
)
BASELINE_AUTHORITY_TERM_RE = re.compile(
    r"\b(00_active_baseline|active baseline|baseline law|baseline|constitutional law|"
    r"constitution|model law|runtime law|canonical law|authority law|pack law|truth law|"
    r"current-state law|accepted RFC law|OFARM law)\b",
    re.IGNORECASE,
)
COMPANION_MACHINE_CLAIM_TERM_RE = re.compile(
    r"\b(model law|runtime law|canonical law|source[- ]of[- ]truth|canonical truth)\b",
    re.IGNORECASE,
)
COMPANION_MACHINE_CLAIM_RE = re.compile(
    r"\b(is|are|becomes?|became|constitutes?|creates?|defines?|declares?|serves as|"
    r"acts as|remains|promotes? to)\b.{0,120}\b(model law|runtime law|canonical law|"
    r"source[- ]of[- ]truth|canonical truth)\b|"
    r"\b(model law|runtime law|canonical law|source[- ]of[- ]truth|canonical truth)\b"
    r".{0,80}\b(store|carrier|layer|source|law|truth)\b",
    re.IGNORECASE,
)
LINE_SAFE_BOUNDARY_RE = re.compile(
    r"\b(does\s+\W*not|do\s+\W*not|must\s+\W*not|may\s+\W*not|cannot|can not|"
    r"is\s+\W*not|are\s+\W*not|not a|not an|not the|never|without|unless|"
    r"separate from|rather than|doesNotOverrideActiveBaseline|doNotOverrideCanonicalAuthority)\b",
    re.IGNORECASE,
)
FILE_SAFE_BOUNDARY_RE = re.compile(
    r"(subordinate to `00_active_baseline/`|does\s+\W*not\s+override|do\s+\W*not\s+override|"
    r"must\s+\W*not\s+override|may\s+\W*not\s+override|does\s+\W*not\s+replace|"
    r"not replacement baseline law|baseline wins|doNotOverrideCanonicalAuthority|"
    r"doesNotOverrideActiveBaseline|draft/non-default|not current/default|not active law|"
    r"not canonical truth|not a source-of-truth|currentness)",
    re.IGNORECASE,
)
ACCEPTED_RFC_BOUNDARY_RE = re.compile(
    r"(Status:\s*accepted|accepted/merged|Authority tier(?: if accepted)?: accepted RFC; "
    r"subordinate to `00_active_baseline/`|subordinate to `00_active_baseline/`)",
    re.IGNORECASE,
)

# Boundary table rows are safe because the file declares itself an interpretive
# map, not replacement baseline law, and says the active baseline wins on conflict.
CONTENT_GUARDRAIL_LINE_ALLOWLIST = {
    ("01_companion_artifacts/OFARM_Concept_Boundary_Map_v0_1.md", 30),
    ("01_companion_artifacts/OFARM_Concept_Boundary_Map_v0_1.md", 32),
}


def load(rel: str):
    return json.loads((REPO / rel).read_text(encoding="utf-8"))


def is_text_file(path: Path) -> bool:
    return path.suffix.lower() in TEXT_SUFFIXES


def line_preview(line: str) -> str:
    return line.strip().replace("\t", " ")[:220]


def has_file_safe_boundary(text: str) -> bool:
    return FILE_SAFE_BOUNDARY_RE.search(text) is not None


def has_accepted_rfc_boundary(rel: str, text: str) -> bool:
    return rel.startswith("02_accepted_rfcs/") and ACCEPTED_RFC_BOUNDARY_RE.search(text) is not None


def is_safe_boundary_line(line: str) -> bool:
    return LINE_SAFE_BOUNDARY_RE.search(line) is not None


def is_baseline_override_claim(line: str) -> bool:
    return (
        AUTHORITY_CHANGE_RE.search(line) is not None
        and BASELINE_AUTHORITY_TERM_RE.search(line) is not None
    )


def is_companion_or_machine_authority_claim(line: str) -> bool:
    return (
        COMPANION_MACHINE_CLAIM_TERM_RE.search(line) is not None
        and COMPANION_MACHINE_CLAIM_RE.search(line) is not None
    )


def scan_authority_order_content(issues: list[str]) -> None:
    for lane in LOWER_AUTHORITY_LANES:
        for path in sorted((REPO / lane).rglob("*")):
            if not path.is_file() or not is_text_file(path):
                continue
            rel = path.relative_to(REPO).as_posix()
            text = path.read_text(encoding="utf-8", errors="replace")
            file_has_safe_boundary = has_file_safe_boundary(text)
            accepted_rfc_has_boundary = has_accepted_rfc_boundary(rel, text)
            for lineno, line in enumerate(text.splitlines(), start=1):
                if (rel, lineno) in CONTENT_GUARDRAIL_LINE_ALLOWLIST:
                    continue

                if is_baseline_override_claim(line):
                    if is_safe_boundary_line(line) and (file_has_safe_boundary or accepted_rfc_has_boundary):
                        continue
                    issues.append(
                        "authority-order content guardrail: "
                        f"{rel}:{lineno}: lower-authority text appears to change baseline law: "
                        f"{line_preview(line)}"
                    )

                if not (rel.startswith("01_companion_artifacts/") or rel.startswith("03_machine_contracts/")):
                    continue
                if not is_companion_or_machine_authority_claim(line):
                    continue
                if is_safe_boundary_line(line) and file_has_safe_boundary:
                    continue
                issues.append(
                    "authority-order content guardrail: "
                    f"{rel}:{lineno}: companion/machine-contract text could read as baseline-level law or truth: "
                    f"{line_preview(line)}"
                )


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

    scan_authority_order_content(issues)

    if issues:
        print("Repository steward guardrail check: FAIL")
        for issue in issues:
            print(f"- {issue}")
        return 1
    print("Repository steward guardrail check: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
