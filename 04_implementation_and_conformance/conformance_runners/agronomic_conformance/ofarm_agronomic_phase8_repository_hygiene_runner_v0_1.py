#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMPL = ROOT / "04_implementation_and_conformance"
OUT = IMPL / "OFARM_agronomic_phase8_repository_hygiene_results_v0_1.json"

REQUIRED_FILES = [
    "04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_Agronomic_Runtime_Chain_Closure_Fixtures_v0_1.md",
    "04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_Agronomic_Runtime_Chain_Closure_Summary_v0_1.md",
    "04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_agronomic_runtime_chain_records_v0_1.json",
    "04_implementation_and_conformance/conformance_runners/agronomic_conformance/ofarm_agronomic_runtime_chain_runner_v0_1.py",
    "04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_agronomic_runtime_chain_results_v0_1.json",
    "04_implementation_and_conformance/conformance_runners/agronomic_conformance/ofarm_agronomic_scenario_fixture_runner_v0_1.py",
    "04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_agronomic_scenario_fixture_results_v0_1.json",
]

NO_PHASE8_BASELINE_DIR = ROOT / "00_active_baseline"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_manifest_paths() -> set[str]:
    path = ROOT / "MANIFEST.csv"
    if not path.exists():
        return set()
    with path.open(newline="", encoding="utf-8") as f:
        return {row["path"] for row in csv.DictReader(f)}


def load_status_map() -> dict[str, str]:
    path = ROOT / "MATERIAL_STATUS.json"
    if not path.exists():
        return {}
    return load_json(path)


def main() -> int:
    manifest_paths = load_manifest_paths()
    status_map = load_status_map()
    required_exist = {rel: (ROOT / rel).exists() for rel in REQUIRED_FILES}
    required_in_manifest = {rel: rel in manifest_paths for rel in REQUIRED_FILES if not rel.endswith("OFARM_agronomic_phase8_repository_hygiene_results_v0_1.json")}
    required_status = {rel: status_map.get(rel) for rel in REQUIRED_FILES if rel in status_map}

    active_baseline_mentions_phase8 = []
    if NO_PHASE8_BASELINE_DIR.exists():
        for file in NO_PHASE8_BASELINE_DIR.glob("*.md"):
            if "AGR-P8" in file.read_text(encoding="utf-8", errors="ignore"):
                active_baseline_mentions_phase8.append(str(file.relative_to(ROOT)))

    runtime_result = load_json(IMPL / "OFARM_agronomic_runtime_chain_results_v0_1.json")
    scenario_result = load_json(IMPL / "OFARM_agronomic_scenario_fixture_results_v0_1.json")
    task_register = load_json(IMPL / "OFARM_Implementation_Task_Register_v0_1.json")
    task_map = {task.get("taskId"): task for task in task_register.get("tasks", [])}

    checks = {
        "required_files_exist": all(required_exist.values()),
        "required_files_manifested": all(required_in_manifest.values()) if required_in_manifest else False,
        "supporting_files_classified_supporting_implementation": all(
            status_map.get(rel) == "ACTIVE_SUPPORTING_IMPLEMENTATION" for rel in REQUIRED_FILES if rel.startswith("04_implementation") and rel in status_map
        ),
        "runtime_chain_result_pass": runtime_result.get("overallStatus") == "PASS",
        "scenario_runner_result_pass": scenario_result.get("overallStatus") == "PASS",
        "imp304_done": task_map.get("IMP-304", {}).get("status") == "DONE",
        "imp308_active": task_map.get("IMP-308", {}).get("status") == "ACTIVE",
        "imp313_done": task_map.get("IMP-313", {}).get("status") == "DONE",
        "no_phase8_baseline_text": len(active_baseline_mentions_phase8) == 0,
    }
    overall = "OK" if all(checks.values()) else "FAIL"
    result = {
        "schemaVersion": "ofarm.agronomicPhase8RepositoryHygieneResults.v0.1",
        "date": "2026-05-13",
        "runner": Path(__file__).name,
        "overallStatus": overall,
        "checks": checks,
        "requiredFilesExist": required_exist,
        "requiredFilesManifested": required_in_manifest,
        "requiredFileStatuses": required_status,
        "activeBaselinePhase8Mentions": active_baseline_mentions_phase8,
        "notes": [
            "This hygiene runner checks AGR-P8 repository integration only.",
            "It does not validate production runtime behavior, live registry checks, or wire-level exchange mappings."
        ]
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(overall)
    return 0 if overall == "OK" else 1


if __name__ == "__main__":
    raise SystemExit(main())
