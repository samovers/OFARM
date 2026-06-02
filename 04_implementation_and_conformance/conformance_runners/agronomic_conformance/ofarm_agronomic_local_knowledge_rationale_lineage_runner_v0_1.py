#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
IMPL = ROOT / "04_implementation_and_conformance"
RECORDS = IMPL / "OFARM_agronomic_local_knowledge_rationale_lineage_records_v0_1.json"
OUT = IMPL / "OFARM_agronomic_local_knowledge_rationale_lineage_results_v0_1.json"
TASKS = IMPL / "OFARM_Implementation_Task_Register_v0_1.json"

REQUIRED_FAMILIES = {
    "NarrativeObservation",
    "AgronomicObservationContext",
    "LocalMemoryRule",
    "InterventionIntentPayload",
    "PlannedIntervention",
    "ExecutionRecordPayload",
    "AssertionRecord",
    "AcceptedEventConsequence",
}
NEGATIVE_TOKENS = {"direct", "accepted", "compliance", "passport", "current-state", "high-consequence", "plan", "claim"}
UPSTREAM_PASS_KEYS = ("overallStatus", "overall")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def upstream_status(path: Path) -> str:
    data = load_json(path)
    for key in UPSTREAM_PASS_KEYS:
        value = data.get(key)
        if isinstance(value, str):
            return value
    return "UNKNOWN"


def validate_step(step: dict[str, Any]) -> dict[str, Any]:
    artifact = ROOT / step.get("artifact", "")
    schema = ROOT / step.get("schema", "")
    checks: dict[str, bool] = {
        "artifact_exists": artifact.exists(),
        "schema_exists": schema.exists(),
        "has_stage_and_family": bool(step.get("stage") and step.get("contractFamily")),
        "has_instance_ref": bool(step.get("instanceRef")),
        "has_twin_and_promotion": bool(step.get("targetTwin") and step.get("promotionOutcome")),
        "has_distinctness_rule": bool(step.get("mustRemainDistinctFrom")),
    }
    validation_detail = None
    if checks["artifact_exists"] and checks["schema_exists"]:
        try:
            jsonschema.validate(load_json(artifact), load_json(schema))
            checks["schema_validates"] = True
        except Exception as exc:
            checks["schema_validates"] = False
            validation_detail = str(exc).splitlines()[0]
    else:
        checks["schema_validates"] = False
    return {
        "stepId": step.get("stepId"),
        "family": step.get("contractFamily"),
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "validationDetail": validation_detail,
    }


def check_lineage(lineage: dict[str, Any]) -> dict[str, Any]:
    steps = lineage.get("steps", [])
    families = {s.get("contractFamily") for s in steps}
    stages = [s.get("stage") for s in steps]
    negative_text = " ".join(n.get("mustFail", "") for n in lineage.get("negativeChecks", [])).lower()
    outputs = lineage.get("expectedOutputBehavior", {})
    step_results = [validate_step(s) for s in steps]
    checks = {
        "has_identity": bool(lineage.get("lineageId") and lineage.get("title")),
        "status_closed": lineage.get("status") == "COVERED_BY_PACKAGE_LOCAL_LINEAGE",
        "minimum_steps": len(steps) >= 2,
        "step_order_has_observation_or_context": any(s in stages for s in ["NARRATIVE_OBSERVATION", "STRUCTURED_OBSERVATION_CONTEXT", "DEGRADED_OBSERVATION_CONTEXT"]),
        "has_rule_or_blocked_context": "LOCAL_MEMORY_RULE" in stages or lineage.get("lineageKind") == "LOCAL_CONTEXT_BLOCKED_FOR_HIGH_CONSEQUENCE_USE",
        "positive_lineage_has_accepted_or_blocked_outcome": ("ACCEPTED_CONSEQUENCE" in stages) or ("BLOCK_HIGH_CONSEQUENCE_USE" in " ".join(s.get("promotionOutcome", "") for s in steps)),
        "families_present": bool(families & REQUIRED_FAMILIES),
        "steps_validate": all(r["status"] == "PASS" for r in step_results),
        "negative_controls_present": len(lineage.get("negativeChecks", [])) >= 2,
        "negative_controls_block_shortcuts": any(tok in negative_text for tok in NEGATIVE_TOKENS),
        "output_behavior_declared": bool(outputs.get("advisoryView") and outputs.get("passportView") and outputs.get("documentAssembly")),
    }
    return {
        "lineageId": lineage.get("lineageId"),
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "stepResults": step_results,
    }


def main() -> int:
    records = load_json(RECORDS)
    task_register = load_json(TASKS)
    task_map = {t.get("taskId"): t for t in task_register.get("tasks", [])}

    upstream_checks = []
    for rel in records.get("upstreamPhaseResultRefs", []):
        path = ROOT / rel
        exists = path.exists()
        status = upstream_status(path) if exists else "MISSING"
        upstream_checks.append({"artifact": rel, "exists": exists, "status": status, "pass": exists and status == "PASS"})

    lineage_results = [check_lineage(l) for l in records.get("lineages", [])]
    used_families = {s.get("contractFamily") for l in records.get("lineages", []) for s in l.get("steps", [])}
    lineages = records.get("lineages", [])
    positive_lineage = next((l for l in lineages if l.get("lineageId") == "AGR-LKR-001"), None)
    blocked_lineage = next((l for l in lineages if l.get("lineageId") == "AGR-LKR-002"), None)

    checks = {
        "fixture_set_declared": records.get("fixtureSetId") == "AGR-P9-local-knowledge-rationale-lineage-v0.1",
        "imp310_done": task_map.get("IMP-310", {}).get("status") == "DONE",
        "upstream_phase_results_pass": all(c["pass"] for c in upstream_checks),
        "required_families_covered": REQUIRED_FAMILIES <= used_families,
        "minimum_lineage_count": len(lineage_results) >= 2,
        "positive_lineage_has_accepted_consequence": bool(positive_lineage and any(s.get("stage") == "ACCEPTED_CONSEQUENCE" for s in positive_lineage.get("steps", []))),
        "blocked_lineage_blocks_high_consequence": bool(blocked_lineage and any("BLOCK" in s.get("promotionOutcome", "") for s in blocked_lineage.get("steps", []))),
        "all_lineages_pass": all(r["status"] == "PASS" for r in lineage_results),
    }
    overall = "PASS" if all(checks.values()) else "FAIL"
    result = {
        "schemaVersion": "ofarm.agronomicLocalKnowledgeRationaleLineageResults.v0.1",
        "date": "2026-05-13",
        "runner": Path(__file__).name,
        "fixtureSetId": records.get("fixtureSetId"),
        "overallStatus": overall,
        "checks": checks,
        "upstreamPhaseChecks": upstream_checks,
        "usedContractFamilies": sorted(f for f in used_families if f),
        "missingContractFamilies": sorted(REQUIRED_FAMILIES - used_families),
        "lineageResults": lineage_results,
        "closureAdvances": [
            "closes IMP-310 at package-local conformance level",
            "links narrative observation, local memory, recommendation, plan, claim, and accepted consequence",
            "proves local rationale remains explainable without becoming direct compliance truth",
            "keeps PassportView default behavior tied to accepted consequences rather than local memory"
        ],
        "limitations": records.get("limitations", [])
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(overall)
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
