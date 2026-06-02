#!/usr/bin/env python3
"""Validate the OFARM AGR-P10 KIS adapter spike candidate fixture.

This runner validates package-local conformance posture only. It does not connect to BigQuery,
validate external wire formats, or promote any record to OFARM truth.
"""
from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
PHASE_DIR = ROOT / "04_implementation_and_conformance" / "fmis_interoperability_investigation_v0_1"
RECORDS_PATH = PHASE_DIR / "OFARM_kis_adapter_spike_candidate_records_v0_1.json"
RESULTS_PATH = PHASE_DIR / "OFARM_kis_adapter_spike_candidate_results_v0_1.json"
REPORT_RESULTS_PATH = PHASE_DIR / "source_report" / "codex_fmis_investigation_results.json"
CANDIDATE_PACKET_PATH = PHASE_DIR / "adapter_spike" / "ofarm_fmis_adapter_spike_candidate_packet.json"
SOURCE_PROBE_PATH = PHASE_DIR / "adapter_spike" / "ofarm_fmis_source_side_probe_packet.json"
ADDENDUM_PATH = PHASE_DIR / "source_report" / "codex_fmis_logineko_entity_package_addendum.md"
ENTITY_RECHECK_PATH = PHASE_DIR / "adapter_spike" / "ofarm_fmis_logineko_entity_recheck_packet.json"

REQUIRED_CARRIERS = {
    "InterventionIntentPayload",
    "ExecutionRecordPayload",
    "PartialExtent",
    "AgronomicIdentityBinding",
    "AgronomicReconstructionTrace",
}
REQUIRED_BLOCKERS = {
    "NO_ORIGINAL_SOURCE_API_EXPORT_OR_MACHINE_PAYLOAD",
    "NO_EXPLICIT_RECOMMENDATION_OR_PRESCRIPTION_AUTHORITY",
    "NO_EVIDENCE_SUFFICIENCY_OR_ACCEPTANCE_DECISION",
    "NO_REGULATORY_PRODUCT_BINDING_FOR_MATERIALS",
    "NO_DIRECT_SCOUTING_TO_APPLICATION_CAUSAL_LINK",
    "NO_MATERIAL_SESSION_OR_TRANSFER_EVIDENCE",
    "NO_CORRECTION_DISPUTE_OR_SUPERSESSION_SOURCE_PROBE",
}


def load(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    failures = []
    warnings = []

    records = load(RECORDS_PATH)
    report = load(REPORT_RESULTS_PATH)
    candidate_packet = load(CANDIDATE_PACKET_PATH)
    source_probe = load(SOURCE_PROBE_PATH)
    entity_recheck = load(ENTITY_RECHECK_PATH)

    if not ADDENDUM_PATH.exists():
        failures.append("Logineko entity package addendum source file is missing.")

    if report.get("meta", {}).get("investigation_status") != "partial":
        warnings.append("Codex report is not marked partial; verify intake posture.")
    if report.get("investigation", {}).get("readiness_assessment") != "needs_more_samples":
        failures.append("Investigation readiness must remain needs_more_samples for this fixture.")

    boundary = records.get("interpretationBoundary", {})
    if boundary.get("sourceTruthStatus") != "discovery_evidence_only":
        failures.append("Source surface must be discovery_evidence_only.")
    if boundary.get("entityPackageTruthStatus") != "source_map_aid_not_standalone_evidence":
        failures.append("Entity package must remain a source-map aid, not standalone truth evidence.")
    if boundary.get("acceptedConsequenceAllowed") is not False:
        failures.append("Accepted consequence must not be allowed for this fixture.")
    if boundary.get("promotionTraceAllowed") is not False:
        failures.append("Promotion trace must not be allowed for this fixture.")
    if boundary.get("coordinatesExported") is not False:
        failures.append("Fixture must remain redacted: no coordinates exported.")

    carriers = {r.get("carrierFamily") for r in records.get("ofarmCandidateRecords", [])}
    missing_carriers = sorted(REQUIRED_CARRIERS - carriers)
    if missing_carriers:
        failures.append(f"Missing candidate carrier families: {missing_carriers}")

    for item in records.get("ofarmCandidateRecords", []):
        cid = item.get("candidateId", "UNKNOWN")
        if item.get("promotionEligible") is not False:
            failures.append(f"{cid} must be promotionEligible=false.")
        if not item.get("missingForPromotion"):
            failures.append(f"{cid} must state missingForPromotion blockers.")
        posture = item.get("recordPosture", "")
        if "candidate" not in posture:
            failures.append(f"{cid} must remain a candidate-only posture.")

    blockers = set(records.get("promotionBlockers", []))
    missing_blockers = sorted(REQUIRED_BLOCKERS - blockers)
    if missing_blockers:
        failures.append(f"Missing required promotion blockers: {missing_blockers}")

    if not candidate_packet or not isinstance(candidate_packet, list):
        failures.append("Candidate packet must be a non-empty list.")
    else:
        cp = candidate_packet[0]
        actual = cp.get("actual_operation", {})
        if actual.get("actual_status") != "COMPLETED":
            failures.append("Expected selected actual operation status COMPLETED.")
        if len(actual.get("materials", [])) < 1:
            failures.append("Expected at least one actual material entry.")
        caveats = cp.get("caveats", {})
        if "accepted OFARM consequence" not in caveats.get("promotion_policy", ""):
            failures.append("Candidate packet must carry the accepted-consequence caveat.")
        if cp.get("crop_zone_actual_operation", {}).get("crop_zone_actual_rows") in (None, "0", 0):
            failures.append("Expected crop-zone actual operation rows.")

    if not source_probe or not isinstance(source_probe, list):
        failures.append("Source-side probe packet must be a non-empty list.")
    else:
        sp = source_probe[0]
        if sp.get("planned_audit", {}).get("row_count") in (None, "0", 0):
            failures.append("Expected planned audit rows in source-side probe.")
        if sp.get("work_orders", {}).get("statuses") != ["FINISHED"]:
            failures.append("Expected one FINISHED work order status.")
        if sp.get("task_results", {}).get("entries", [{}])[0].get("status") != "FINISHED":
            failures.append("Expected one FINISHED task result.")

    recheck = records.get("selectedCandidate", {}).get("entityGuidedRecheck", {})
    if recheck.get("sourceModelAid") is not True:
        failures.append("Entity-guided recheck must be marked sourceModelAid=true.")
    if recheck.get("workOrderCheckpointEvidencePresent") is not True:
        failures.append("Entity-guided recheck must record work-order checkpoint evidence.")
    if recheck.get("workOrderCheckpoints") != "2":
        failures.append("Expected two work-order checkpoints from the addendum.")
    if recheck.get("checkpointTypes") != ["START", "END"]:
        failures.append("Expected START and END checkpoint types.")
    if recheck.get("linkedMaterialSessions") != "0":
        failures.append("Selected candidate should still have zero linked material sessions.")
    if recheck.get("scoutingRelationshipVisibleForSelectedCandidate") is not False:
        failures.append("Selected candidate should still lack visible linked scouting rows.")

    if entity_recheck.get("status") != "source_map_aid_not_truth_evidence":
        failures.append("Entity recheck packet must be source_map_aid_not_truth_evidence.")
    er = entity_recheck.get("recheckResults", {})
    if er.get("workOrderCheckpoints") != "2" or er.get("linkedScoutingReports") != "0" or er.get("linkedMaterialSessions") != "0":
        failures.append("Entity recheck packet must preserve checkpoint/scouting/material-session results from the addendum.")
    oi = entity_recheck.get("ofarmInterpretation", {})
    if oi.get("acceptedConsequenceAllowed") is not False or oi.get("promotionTraceAllowed") is not False:
        failures.append("Entity recheck interpretation must block accepted consequences and promotion traces.")

    status = "PASS" if not failures else "FAIL"
    result = {
        "runnerId": "ofarm_kis_adapter_spike_candidate_runner_v0_1",
        "runAt": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "status": status,
        "summary": "KIS adapter spike fixture remains candidate-only and promotion-blocked; Logineko entity addendum strengthens source-side checkpoint evidence." if status == "PASS" else "KIS adapter spike fixture failed posture checks.",
        "checkedRecords": len(records.get("ofarmCandidateRecords", [])),
        "requiredCarrierFamilies": sorted(REQUIRED_CARRIERS),
        "presentCarrierFamilies": sorted(carriers),
        "requiredPromotionBlockers": sorted(REQUIRED_BLOCKERS),
        "presentPromotionBlockers": sorted(blockers),
        "entityAddendumChecks": {
            "addendumPresent": ADDENDUM_PATH.exists(),
            "workOrderCheckpoints": recheck.get("workOrderCheckpoints"),
            "checkpointTypes": recheck.get("checkpointTypes"),
            "linkedScoutingReports": er.get("linkedScoutingReports"),
            "linkedMaterialSessions": er.get("linkedMaterialSessions"),
            "sourceModelAidOnly": entity_recheck.get("status") == "source_map_aid_not_truth_evidence"
        },
        "warnings": warnings,
        "failures": failures,
        "limitations": [
            "No live BigQuery query is run by this package-local runner.",
            "The Logineko entity package is a source-map aid, not original payload evidence.",
            "No production adapter is claimed.",
            "No accepted OFARM consequence, promotion trace, or compliance-grade product identity is produced.",
            "No wire-level ADAPT, ISOXML, or EFDI conformance is claimed."
        ]
    }
    RESULTS_PATH.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(status)
    return 0 if status == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
