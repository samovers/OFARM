#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CURRENT = "OFARM2_2026-05-30_cp15_agentic_software_delivery_model_deployment_governance_merged_v0_2_final_currentness_normalized"

REQUIRED_POLICY_FILES = [
    "package_meta/release_profiles/README.md",
    "package_meta/release_profiles/DEV_AUDIT_PACKAGING_POLICY.md",
    "package_meta/release_profiles/dev_package_profile.json",
    "package_meta/release_profiles/audit_package_profile.json",
    "package_meta/release_profiles/RELEASE_PROFILE_VALIDATION.md",
    "package_meta/tools/build_ofarm_release_profiles.py",
    "package_meta/tools/check_release_profile_policy.py",
]

ROOT_ZIP_PATTERNS = [
    re.compile(r".*\.zip$"),
    re.compile(r"CLEAN_BASELINE_PHASE.*_REPORT_PACKAGE_.*\.zip$"),
    re.compile(r"OFARM2_FINAL_PACKAGE_REPORT_PACKAGE_.*\.zip$"),
    re.compile(r"OFARM2_.*_(DEV|AUDIT)\.zip$"),
]


def load_json(rel: str):
    return json.loads((REPO / rel).read_text(encoding="utf-8"))


def root_zip_artifacts() -> list[str]:
    bad: list[str] = []
    for p in REPO.glob("*.zip"):
        name = p.name
        if any(pattern.fullmatch(name) or pattern.match(name) for pattern in ROOT_ZIP_PATTERNS):
            bad.append(p.as_posix())
    return sorted(bad)


def forbidden_cache_files() -> list[str]:
    bad: list[str] = []
    for p in REPO.rglob("*"):
        rel = p.relative_to(REPO).as_posix()
        if ".git/" in rel:
            continue
        if p.name == ".DS_Store":
            bad.append(rel)
        elif p.is_dir() and p.name == "__pycache__":
            bad.append(rel + "/")
        elif p.is_file() and p.suffix == ".pyc":
            bad.append(rel)
    return sorted(bad)


def main() -> int:
    issues: list[str] = []

    for rel in REQUIRED_POLICY_FILES:
        if not (REPO / rel).exists():
            issues.append(f"missing release profile policy file: {rel}")

    profiles = {}
    for rel, expected_id in [
        ("package_meta/release_profiles/dev_package_profile.json", "DEV"),
        ("package_meta/release_profiles/audit_package_profile.json", "AUDIT"),
    ]:
        try:
            data = load_json(rel)
        except Exception as exc:
            issues.append(f"{rel} does not parse as JSON: {exc}")
            continue
        profiles[expected_id] = data
        if data.get("profileId") != expected_id:
            issues.append(f"{rel} profileId is not {expected_id}")
        if data.get("currentPackageIdentity") != CURRENT:
            issues.append(f"{rel} currentPackageIdentity is stale")
        if data.get("latestControlledAmendment") != "CP15":
            issues.append(f"{rel} latestControlledAmendment is not CP15")
        if not data.get("requiredFiles"):
            issues.append(f"{rel} has no requiredFiles")
        if not data.get("requiredFolders"):
            issues.append(f"{rel} has no requiredFolders")

    dev = profiles.get("DEV", {})
    audit = profiles.get("AUDIT", {})
    dev_excludes = "\n".join(dev.get("excludeRules", []))
    audit_includes = "\n".join(audit.get("includeRules", []) + audit.get("requiredFolders", []) + audit.get("requiredFiles", []))
    if "clean_baseline_phase_reports/" not in dev_excludes:
        issues.append("DEV profile does not exclude clean_baseline_phase_reports/")
    if "OFARM2_*.zip at repo root" not in dev_excludes:
        issues.append("DEV profile does not exclude root OFARM2 ZIP artifacts")
    if "clean_baseline_phase_reports/" not in audit_includes:
        issues.append("AUDIT profile does not include clean_baseline_phase_reports/")
    if "CLEAN_BASELINE_" not in audit_includes:
        issues.append("AUDIT profile does not include clean-baseline ledgers/reports")

    for rel in dev.get("requiredFiles", []) + audit.get("requiredFiles", []):
        if not (REPO / rel).exists():
            issues.append(f"profile required file missing from package tree: {rel}")
    for rel in dev.get("requiredFolders", []):
        if not (REPO / rel.rstrip("/")).is_dir():
            issues.append(f"DEV required folder missing from package tree: {rel}")
    # AUDIT is allowed to be checked inside a DEV package, where phase reports are intentionally absent.
    for rel in audit.get("requiredFolders", []):
        if rel == "clean_baseline_phase_reports/":
            continue
        if not (REPO / rel.rstrip("/")).is_dir():
            issues.append(f"AUDIT required folder missing from package tree: {rel}")

    try:
        entry = load_json("CURRENT_ACTIVE_ENTRYPOINT.json")
    except Exception as exc:
        issues.append(f"CURRENT_ACTIVE_ENTRYPOINT.json does not parse: {exc}")
        entry = {}
    if entry.get("currentPackageIdentity") != CURRENT:
        issues.append("CURRENT_ACTIVE_ENTRYPOINT.json currentPackageIdentity is stale")
    if entry.get("latestControlledAmendment") != "CP15":
        issues.append("CURRENT_ACTIVE_ENTRYPOINT.json latestControlledAmendment is not CP15")
    if entry.get("cleanBaselineCompletionStatus") != "COMPLETE":
        issues.append("CURRENT_ACTIVE_ENTRYPOINT.json cleanBaselineCompletionStatus is not COMPLETE")
    if entry.get("cp16Started") is not False:
        issues.append("CURRENT_ACTIVE_ENTRYPOINT.json cp16Started is not false")
    if entry.get("postCP15AmendmentStarted") is not False:
        issues.append("CURRENT_ACTIVE_ENTRYPOINT.json postCP15AmendmentStarted is not false")
    if entry.get("remainingCleanBaselinePhases") not in (None, []):
        issues.append("CURRENT_ACTIVE_ENTRYPOINT.json remainingCleanBaselinePhases is non-empty")
    policy = entry.get("releaseArtifactPolicy", {})
    if policy.get("sourceTreeBulkyZipArtifacts") != "removed_from_source_tree_distributed_as_external_release_assets":
        issues.append("CURRENT_ACTIVE_ENTRYPOINT.json releaseArtifactPolicy is missing or inconsistent")
    if policy.get("releaseMetadataLane") != "package_meta/release/final_clean_baseline/":
        issues.append("CURRENT_ACTIVE_ENTRYPOINT.json releaseMetadataLane is not package_meta/release/final_clean_baseline/")

    try:
        readiness = load_json("CLEAN_BASELINE_FINAL_PACKAGE_READINESS.json")
        validation = load_json("CLEAN_BASELINE_FINAL_VALIDATION_LEDGER.json")
        debt = load_json("CLEAN_BASELINE_UNRESOLVED_DEBT_REGISTER.json")
    except Exception as exc:
        issues.append(f"final validation/readiness/debt JSON does not parse: {exc}")
        readiness = validation = debt = {}
    if validation.get("finalVerdict") not in {"ACCEPT_AS_CLEAN_BASELINE", "ACCEPT_WITH_MINOR_DEBT"}:
        issues.append("final validation verdict is not accepted")
    if validation.get("fullValidationSuitePassed") is not True:
        issues.append("full validation suite is not recorded as passed")
    if readiness.get("readinessVerdict") not in {"READY_FOR_FINAL_PACKAGE", "READY_WITH_MINOR_DEBT"}:
        issues.append("final package readiness is not ready")
    if readiness.get("unresolvedBlockers"):
        issues.append("final package readiness has unresolved blockers")
    if debt.get("blockers"):
        issues.append("unresolved debt register has blockers")

    for rel in [
        "00_active_baseline/OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md",
        "00_active_baseline/OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md",
        "00_active_baseline/OFARM_Alignment_Register_v0_13.md",
        "00_active_baseline/OFARM_post_gap_closure_readiness_gate_memo_v0_1.md",
        "00_active_baseline/OFARM_final_hostile_review_after_gap_closure_v0_1.md",
    ]:
        if not (REPO / rel).exists():
            issues.append(f"canonical active authority file missing: {rel}")
    if not (REPO / "03_machine_contracts/schemas").is_dir():
        issues.append("03_machine_contracts/schemas/ is missing")
    if not (REPO / "03_machine_contracts/drafts_non_default").is_dir():
        issues.append("03_machine_contracts/drafts_non_default/ is missing")

    for rel in root_zip_artifacts():
        issues.append(f"root-level ZIP artifact present: {rel}")
    for rel in forbidden_cache_files():
        issues.append(f"forbidden cache/OS file present: {rel}")

    if issues:
        print("Release profile policy check: FAIL")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print("Release profile policy check: OK")
    print("DEV/AUDIT release profiles are source-policy clean")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
