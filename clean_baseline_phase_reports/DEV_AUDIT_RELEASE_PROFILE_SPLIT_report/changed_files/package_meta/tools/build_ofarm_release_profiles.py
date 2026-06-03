#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CURRENT = "OFARM2_2026-05-30_cp15_agentic_software_delivery_model_deployment_governance_merged_v0_2_final_currentness_normalized"
PACKAGE_BASE = "OFARM2_2026-05-30_cp15_materialized_development_baseline_v0_2"
PROFILE_FILES = {
    "DEV": "package_meta/release_profiles/dev_package_profile.json",
    "AUDIT": "package_meta/release_profiles/audit_package_profile.json",
}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_profile(profile_id: str) -> dict:
    path = REPO / PROFILE_FILES[profile_id]
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("profileId") != profile_id:
        raise SystemExit(f"profileId mismatch in {path}")
    if data.get("currentPackageIdentity") != CURRENT:
        raise SystemExit(f"currentPackageIdentity mismatch in {path}")
    return data


def common_excluded(rel: str) -> bool:
    parts = rel.split("/")
    name = parts[-1]
    if ".git" in parts or "__pycache__" in parts:
        return True
    if name == ".DS_Store" or name.endswith(".pyc"):
        return True
    if ".pytest_cache" in parts or ".mypy_cache" in parts or "node_modules" in parts:
        return True
    if ".idea" in parts or ".vscode" in parts:
        return True
    if name.endswith((".tmp", ".swp", ".swo")):
        return True
    if "/" not in rel and name.endswith(".zip"):
        return True
    return False


def profile_excluded(profile_id: str, rel: str) -> bool:
    if common_excluded(rel):
        return True
    if profile_id == "DEV" and rel.startswith("clean_baseline_phase_reports/"):
        return True
    return False


def iter_source_files(profile_id: str) -> list[str]:
    files: list[str] = []
    for path in REPO.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(REPO).as_posix()
        if profile_excluded(profile_id, rel):
            continue
        files.append(rel)
    return sorted(files)


def copy_profile_files(profile_id: str, stage: Path) -> list[str]:
    files = iter_source_files(profile_id)
    for rel in files:
        src = REPO / rel
        dst = stage / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    return files


def remove_junk(root: Path) -> None:
    for path in sorted(root.rglob("*"), reverse=True):
        if path.name == ".DS_Store" or path.suffix == ".pyc":
            path.unlink(missing_ok=True)
        elif path.is_dir() and path.name in {"__pycache__", ".pytest_cache", ".mypy_cache"}:
            shutil.rmtree(path, ignore_errors=True)


def run_command(stage: Path, command: list[str]) -> dict:
    env = os.environ.copy()
    result = subprocess.run(command, cwd=stage, capture_output=True, text=True, env=env)
    return {
        "command": " ".join(command),
        "exitCode": result.returncode,
        "stdout": result.stdout[-8000:],
        "stderr": result.stderr[-8000:],
    }


def check_required(profile: dict, stage: Path, profile_id: str) -> list[str]:
    issues: list[str] = []
    for rel in profile.get("requiredFiles", []):
        if not (stage / rel).is_file():
            issues.append(f"missing required file: {rel}")
    for rel in profile.get("requiredFolders", []):
        if profile_id == "DEV" and rel == "clean_baseline_phase_reports/":
            continue
        if not (stage / rel.rstrip("/")).is_dir():
            issues.append(f"missing required folder: {rel}")
    if profile_id == "DEV" and (stage / "clean_baseline_phase_reports").exists():
        issues.append("DEV staging unexpectedly contains clean_baseline_phase_reports/")
    if profile_id == "AUDIT" and not (stage / "clean_baseline_phase_reports").is_dir():
        issues.append("AUDIT staging does not contain clean_baseline_phase_reports/")
    for p in stage.glob("*.zip"):
        issues.append(f"root ZIP artifact present in staging: {p.name}")
    return issues


def json_parse_check(stage: Path) -> dict:
    failures = []
    for path in stage.rglob("*.json"):
        if ".git" in path.parts:
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            failures.append({"path": path.relative_to(stage).as_posix(), "error": str(exc)})
    return {"name": "JSON parse all profile package JSON", "exitCode": 0 if not failures else 1, "failures": failures[:50]}


def contents(stage: Path) -> list[str]:
    return sorted(p.relative_to(stage).as_posix() for p in stage.rglob("*") if p.is_file())


def write_contents_manifest(stage: Path, output: Path, package_dir_name: str) -> int:
    file_list = contents(stage)
    output.write_text("\n".join(f"./{p}" for p in file_list) + "\n", encoding="utf-8")
    return len(file_list)


def make_zip(stage: Path, zip_path: Path, package_dir_name: str) -> None:
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for rel in contents(stage):
            src = stage / rel
            zf.write(src, f"{package_dir_name}/{rel}")


def build_profile(profile_id: str, output_dir: Path) -> dict:
    profile = load_profile(profile_id)
    package_dir_name = f"{PACKAGE_BASE}_{profile_id}"
    stage_parent = output_dir / "staging"
    stage = stage_parent / package_dir_name
    if stage.exists():
        shutil.rmtree(stage)
    stage.mkdir(parents=True, exist_ok=True)

    copied = copy_profile_files(profile_id, stage)
    required_issues = check_required(profile, stage, profile_id)
    validation_results = [json_parse_check(stage)]
    for command in profile.get("validationCommands", []):
        validation_results.append(run_command(stage, command.split()))
    remove_junk(stage)

    zip_path = output_dir / f"{package_dir_name}.zip"
    sha_path = output_dir / f"{package_dir_name}.zip.sha256"
    contents_path = output_dir / f"{package_dir_name}_contents.txt"
    report_json_path = output_dir / f"{package_dir_name}_build_report.json"
    report_md_path = output_dir / f"{package_dir_name}_build_report.md"

    file_count = write_contents_manifest(stage, contents_path, package_dir_name)
    make_zip(stage, zip_path, package_dir_name)
    digest = sha256(zip_path)
    sha_path.write_text(f"{digest}  {zip_path.name}\n", encoding="utf-8")

    validation_passed = not required_issues and all(item.get("exitCode") == 0 for item in validation_results)
    report = {
        "schemaVersion": "ofarm.releaseProfileBuildReport.v1",
        "generatedOrCuratedAt": now(),
        "profileId": profile_id,
        "packageKind": profile.get("packageKind"),
        "currentPackageIdentity": CURRENT,
        "latestControlledAmendment": "CP15",
        "stagePath": stage.as_posix(),
        "zipPath": zip_path.as_posix(),
        "sha256Path": sha_path.as_posix(),
        "contentsManifestPath": contents_path.as_posix(),
        "fileCount": file_count,
        "zipSha256": digest,
        "copiedSourceFileCount": len(copied),
        "requiredIssues": required_issues,
        "validationResults": validation_results,
        "validationPassed": validation_passed,
        "packagesCommittedToRepo": False,
        "semanticLawChanged": False,
        "activeAuthorityContentModified": False,
        "canonicalActiveAuthorityFilesMoved": False,
        "machineContractSchemasMoved": False,
        "draftNonDefaultLaneMoved": False,
        "draftContractsPromoted": False,
    }
    report_json_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    md = [
        f"# {profile_id} Release Profile Build Report",
        "",
        f"Status: {'PASS' if validation_passed else 'FAIL'}",
        "",
        f"Package: `{zip_path.name}`",
        f"SHA-256: `{digest}`",
        f"File count: `{file_count}`",
        "",
        "No OFARM semantic law was changed by this package build.",
    ]
    report_md_path.write_text("\n".join(md) + "\n", encoding="utf-8")
    if not validation_passed:
        raise SystemExit(f"{profile_id} package validation failed; see {report_json_path}")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Build OFARM DEV/AUDIT release profile packages outside the source repo.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--profile", choices=sorted(PROFILE_FILES))
    group.add_argument("--all", action="store_true")
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    output_dir = Path(args.output_dir).expanduser().resolve()
    repo_resolved = REPO.resolve()
    if output_dir == repo_resolved or repo_resolved in output_dir.parents:
        raise SystemExit("output-dir must be outside the source repository")
    output_dir.mkdir(parents=True, exist_ok=True)

    profiles = sorted(PROFILE_FILES) if args.all else [args.profile]
    reports = [build_profile(profile_id, output_dir) for profile_id in profiles]
    print(json.dumps({"status": "OK", "outputDir": output_dir.as_posix(), "reports": reports}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
