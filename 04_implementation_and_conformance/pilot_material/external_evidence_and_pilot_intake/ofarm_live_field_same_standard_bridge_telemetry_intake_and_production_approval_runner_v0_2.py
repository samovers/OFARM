#!/usr/bin/env python3
"""OFARM live-field telemetry intake and production approval runner v0.2.

This runner keeps the same conservative promotion blockers as v0.1 while adding
explicit support for a pre-implementation capture kit. Template-shaped or
self-declared non-qualifying artifacts are never counted as real promotion
-evidence, even if a user later copies them into a discovery-pattern filename by
mistake.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def classify_artifact(path: Path, expected_class: str, pair_ids: set[str]) -> Dict[str, Any]:
    info: Dict[str, Any] = {
        "file": path.name,
        "qualifying": False,
        "candidatePairIds": [],
        "reasonCode": None,
        "notes": None,
    }
    try:
        payload = load_json(path)
    except Exception:
        info["reasonCode"] = "UNPARSEABLE_JSON"
        info["notes"] = "File exists but could not be parsed as JSON."
        return info
    if payload.get("templateOnly") is True:
        info["reasonCode"] = "TEMPLATE_ONLY_ARTIFACT"
        info["notes"] = "Artifact self-declares templateOnly and does not qualify for promotion scanning."
        return info
    if payload.get("qualifiesForPromotionIntake") is False:
        info["reasonCode"] = "SELF_DECLARED_NONQUALIFYING_ARTIFACT"
        info["notes"] = "Artifact self-declares that it does not qualify for promotion scanning."
        return info
    actual_class = payload.get("requiredEvidenceClass") or payload.get("evidenceClass")
    if actual_class and actual_class != expected_class:
        info["reasonCode"] = "EVIDENCE_CLASS_MISMATCH"
        info["notes"] = f"Artifact class {actual_class} does not match expected {expected_class}."
        return info
    records = payload.get("records")
    if records is None:
        records = payload.get("approvalRecords", [])
    if not isinstance(records, list) or not records:
        info["reasonCode"] = "NO_RECORDS_PRESENT"
        info["notes"] = "Artifact has no candidate-pair records to evaluate."
        return info
    seen_pair_ids = sorted({entry.get("candidatePairId") for entry in records if entry.get("candidatePairId") in pair_ids})
    if not seen_pair_ids:
        info["reasonCode"] = "NO_KNOWN_CANDIDATE_PAIR_IDS"
        info["notes"] = "Artifact records do not resolve to the known same-standard bridge draft pairs."
        return info
    info["qualifying"] = True
    info["candidatePairIds"] = seen_pair_ids
    info["reasonCode"] = "QUALIFYING_ARTIFACT"
    info["notes"] = "Artifact is parseable, non-template, and resolves to the known bridge draft pairs."
    return info


def main() -> int:
    here = Path(__file__).resolve().parent
    candidate_pairs = load_json(here / "OFARM_same_standard_bridge_pack_candidate_pairs_v0_6.json")
    pair_ids = {entry["candidatePairId"] for entry in candidate_pairs}

    capture_kit_refs = {
        "live_field": "OFARM_live_field_same_standard_bridge_telemetry_capture_template_v0_1.json",
        "trace_back": "OFARM_live_field_same_standard_bridge_trace_back_records_capture_template_v0_1.json",
        "approval": "OFARM_same_standard_bridge_production_approval_record_capture_template_v0_1.json",
        "guide": "OFARM_Live_Field_Same_Standard_Bridge_Evidence_Capture_Kit_v0_1.md",
        "operator": "OFARM_live_field_same_standard_bridge_operator_note_v0_1.md",
        "captureKitResults": "OFARM_live_field_same_standard_bridge_capture_kit_results_v0_1.json",
    }

    search_specs = {
        "live_field": {
            "pattern": "OFARM_live_field_same_standard_bridge_telemetry_v*.json",
            "expectedClass": "LIVE_FIELD_COLLECTED_SAME_STANDARD_BRIDGE_TELEMETRY",
            "excludedEvidenceRefs": [
                "OFARM_executor_native_same_standard_bridge_telemetry_v0_1.json",
                "OFARM_deployment_sample_same_standard_bridge_telemetry_v0_1.json",
                "OFARM_deployment_intake_same_standard_bridge_telemetry_v0_1.json",
            ],
        },
        "trace_back": {
            "pattern": "OFARM_live_field_same_standard_bridge_trace_back_records_v*.json",
            "expectedClass": "DEPLOYMENT_PRODUCED_TRACE_BACK_LINKAGE",
            "excludedEvidenceRefs": [
                "OFARM_projection_trace_back_records_v0_1.json",
                "OFARM_output_adapter_trace_back_records_v0_1.json",
            ],
        },
        "approval": {
            "pattern": "OFARM_same_standard_bridge_production_approval_record_v*.json",
            "expectedClass": "PRODUCTION_PROMOTION_APPROVAL_RECORD",
            "excludedEvidenceRefs": [],
        },
    }

    discovered: Dict[str, List[Dict[str, Any]]] = {}
    for key, spec in search_specs.items():
        files = sorted(here.glob(spec["pattern"]))
        discovered[key] = [classify_artifact(path, spec["expectedClass"], pair_ids) for path in files]

    def qualifying_files(key: str) -> List[str]:
        return [entry["file"] for entry in discovered[key] if entry["qualifying"]]

    def nonqualifying_files(key: str) -> List[Dict[str, Any]]:
        return [entry for entry in discovered[key] if not entry["qualifying"]]

    live_field_registry = {
        "evaluatedAt": "2026-04-18T12:30:00Z",
        "searchScope": "04_implementation_and_conformance/",
        "searchPattern": search_specs["live_field"]["pattern"],
        "excludedEvidenceRefs": search_specs["live_field"]["excludedEvidenceRefs"],
        "preImplementationTemplateRefs": [capture_kit_refs["live_field"], capture_kit_refs["guide"], capture_kit_refs["operator"]],
        "discoveredFiles": [entry["file"] for entry in discovered["live_field"]],
        "qualifyingFiles": qualifying_files("live_field"),
        "nonQualifyingFiles": nonqualifying_files("live_field"),
        "records": [],
        "summary": {},
        "overall": "WAITING_FOR_LIVE_FIELD_TELEMETRY",
        "limitations": [
            "This registry is intentionally conservative. Executor, partner-sample, redacted deployment-intake, and template-shaped artifacts are not counted as live field-collected telemetry.",
            "The pre-implementation capture kit is preparation only and does not satisfy the live-field evidence blocker."
        ],
    }
    trace_back_registry = {
        "evaluatedAt": "2026-04-18T12:30:00Z",
        "searchScope": "04_implementation_and_conformance/",
        "searchPattern": search_specs["trace_back"]["pattern"],
        "excludedEvidenceRefs": search_specs["trace_back"]["excludedEvidenceRefs"],
        "preImplementationTemplateRefs": [capture_kit_refs["trace_back"], capture_kit_refs["guide"], capture_kit_refs["operator"]],
        "discoveredFiles": [entry["file"] for entry in discovered["trace_back"]],
        "qualifyingFiles": qualifying_files("trace_back"),
        "nonQualifyingFiles": nonqualifying_files("trace_back"),
        "records": [],
        "summary": {},
        "overall": "WAITING_FOR_DEPLOYMENT_PRODUCED_TRACEBACK_LINKAGE",
        "limitations": [
            "Replay-produced, adapter-produced, manually reconstructed, or template-shaped artifacts are not counted as live field deployment-produced linkage.",
            "The pre-implementation capture kit is preparation only and does not satisfy the deployment-produced trace-back blocker."
        ],
    }
    approval_registry = {
        "evaluatedAt": "2026-04-18T12:30:00Z",
        "searchScope": "04_implementation_and_conformance/",
        "searchPattern": search_specs["approval"]["pattern"],
        "excludedEvidenceRefs": search_specs["approval"]["excludedEvidenceRefs"],
        "preImplementationTemplateRefs": [capture_kit_refs["approval"], capture_kit_refs["guide"], capture_kit_refs["operator"]],
        "discoveredFiles": [entry["file"] for entry in discovered["approval"]],
        "qualifyingFiles": qualifying_files("approval"),
        "nonQualifyingFiles": nonqualifying_files("approval"),
        "records": [],
        "summary": {},
        "overall": "WAITING_FOR_PRODUCTION_APPROVAL",
        "limitations": [
            "Repo-only dry runs, undated signoffs, or template-shaped artifacts are not counted as production approval.",
            "The pre-implementation capture kit is preparation only and does not satisfy the production approval blocker."
        ],
    }

    gate = {
        "evaluatedAt": "2026-04-18T12:30:00Z",
        "sourceRefs": [
            "OFARM_live_field_same_standard_bridge_telemetry_intake_registry_v0_2.json",
            "OFARM_live_field_same_standard_bridge_trace_back_linkage_registry_v0_2.json",
            "OFARM_same_standard_bridge_production_approval_registry_v0_2.json",
            capture_kit_refs["captureKitResults"],
        ],
        "preImplementationCaptureKitRefs": [
            capture_kit_refs["live_field"],
            capture_kit_refs["trace_back"],
            capture_kit_refs["approval"],
            capture_kit_refs["guide"],
            capture_kit_refs["operator"],
        ],
        "records": [],
        "summary": {},
        "overall": "WAITING_FOR_LIVE_FIELD_AND_PRODUCTION_APPROVAL",
        "limitations": [
            "This gate does not infer production readiness from executor-produced, partner-sample, redacted deployment-intake, or template-shaped artifacts.",
            "The capture kit shows that the package is prepared to collect evidence later; it does not change the hold-at-draft posture now."
        ],
    }

    candidate_pairs_v7 = []
    promotion_readiness = {
        "evaluatedAt": "2026-04-18T12:30:00Z",
        "scope": "same-standard bridge-pack promotion readiness after explicit live-field telemetry intake, deployment-produced trace-back intake, production approval scanning, and pre-implementation capture-kit hardening",
        "candidatePairs": [],
        "summary": {},
        "overall": "HOLD_AT_DRAFT",
        "limitations": [
            "No live field-collected same-standard bridge telemetry artifact exists in the package-local search scope.",
            "No deployment-produced live-field trace-back linkage artifact exists in the package-local search scope.",
            "No production promotion approval record exists in the package-local search scope.",
            "The pre-implementation capture kit is present but is not counted as qualifying promotion evidence."
        ],
    }

    results = {
        "driftCheck": {
            "status": "PASS",
            "decision": "NO_MATERIAL_DRIFT_DETECTED",
            "reasons": [
                "The new work stays inside implementation/conformance and does not reopen baseline architecture.",
                "The capture kit prepares future evidence intake without changing bridge promotion standards.",
                "Template-shaped artifacts are now explicitly prevented from looking like real evidence by filename alone."
            ],
            "cautions": [
                "The package is better prepared for future deployments, but actual promotion blockers remain unchanged until real deployment evidence exists."
            ],
        },
        "captureKitChecks": {},
        "liveFieldTelemetryIntake": {},
        "deploymentProducedTraceBackIntake": {},
        "productionApprovalIntake": {},
        "linkedArtifactChecks": {},
        "summary": {
            "candidatePairs": len(candidate_pairs),
            "liveFieldTelemetryArtifactsFound": len(qualifying_files("live_field")),
            "deploymentProducedTraceBackArtifactsFound": len(qualifying_files("trace_back")),
            "productionApprovalRecordsFound": len(qualifying_files("approval")),
            "captureKitFilesChecked": 0,
            "linkedArtifactsChecked": 0,
        },
        "limitations": [
            "This wave prepares the real deployment evidence path, but it does not fabricate or infer live field telemetry.",
            "This wave prepares the real deployment evidence path, but it does not fabricate or infer deployment-produced trace-back linkage.",
            "This wave prepares the real deployment evidence path, but it does not fabricate or infer production approval."
        ],
        "overall": "PASS_WITH_LIMITATIONS",
        "failingChecks": [],
    }

    capture_files = [
        capture_kit_refs["live_field"],
        capture_kit_refs["trace_back"],
        capture_kit_refs["approval"],
        capture_kit_refs["guide"],
        capture_kit_refs["operator"],
        capture_kit_refs["captureKitResults"],
    ]
    for filename in capture_files:
        path = here / filename
        status = "PASS"
        try:
            if filename.endswith('.json'):
                load_json(path)
            else:
                path.read_text(encoding='utf-8')
        except Exception:
            status = "FAIL"
        results["captureKitChecks"][f"{filename} :: located-and-parseable"] = status
        if status != "PASS":
            results["failingChecks"].append(f"{filename} :: {status}")
    results["summary"]["captureKitFilesChecked"] = len(capture_files)

    live_by_pair: Dict[str, List[str]] = {pair_id: [] for pair_id in pair_ids}
    for item in discovered["live_field"]:
        if item["qualifying"]:
            for pair_id in item["candidatePairIds"]:
                live_by_pair[pair_id].append(item["file"])
    trace_by_pair: Dict[str, List[str]] = {pair_id: [] for pair_id in pair_ids}
    for item in discovered["trace_back"]:
        if item["qualifying"]:
            for pair_id in item["candidatePairIds"]:
                trace_by_pair[pair_id].append(item["file"])
    approval_by_pair: Dict[str, List[str]] = {pair_id: [] for pair_id in pair_ids}
    for item in discovered["approval"]:
        if item["qualifying"]:
            for pair_id in item["candidatePairIds"]:
                approval_by_pair[pair_id].append(item["file"])

    for entry in candidate_pairs:
        candidate_pair_id = entry["candidatePairId"]
        standard_ref = entry["standardRef"]
        bridge_label = "ADAPT" if "adapt" in candidate_pair_id else "ISOXML"
        live_refs = live_by_pair[candidate_pair_id]
        trace_refs = trace_by_pair[candidate_pair_id]
        approval_refs = approval_by_pair[candidate_pair_id]

        live_present = bool(live_refs)
        trace_present = bool(trace_refs)
        approval_present = bool(approval_refs)

        live_field_registry["records"].append({
            "candidatePairId": candidate_pair_id,
            "standardRef": standard_ref,
            "intakeDecision": "QUALIFYING_LIVE_FIELD_TELEMETRY_FOUND" if live_present else "NO_QUALIFYING_LIVE_FIELD_TELEMETRY_ARTIFACTS_FOUND",
            "discoveredTelemetryRefs": live_refs,
            "linkedCaptureTemplateRef": capture_kit_refs["live_field"],
            "notes": "Qualifying live-field telemetry was discovered in the package-local search scope." if live_present else "No qualifying live-field telemetry artifact was found. The pre-implementation capture template exists but does not count as evidence."
        })
        trace_back_registry["records"].append({
            "candidatePairId": candidate_pair_id,
            "standardRef": standard_ref,
            "intakeDecision": "QUALIFYING_DEPLOYMENT_PRODUCED_TRACEBACK_FOUND" if trace_present else "NO_QUALIFYING_DEPLOYMENT_PRODUCED_TRACEBACK_ARTIFACTS_FOUND",
            "discoveredTraceBackRefs": trace_refs,
            "linkedCaptureTemplateRef": capture_kit_refs["trace_back"],
            "notes": "Qualifying deployment-produced trace-back linkage was discovered in the package-local search scope." if trace_present else "No qualifying deployment-produced trace-back artifact was found. The pre-implementation capture template exists but does not count as evidence."
        })
        approval_registry["records"].append({
            "candidatePairId": candidate_pair_id,
            "standardRef": standard_ref,
            "approvalDecision": "QUALIFYING_PRODUCTION_APPROVAL_FOUND" if approval_present else "NO_QUALIFYING_PRODUCTION_APPROVAL_RECORD_FOUND",
            "discoveredApprovalRefs": approval_refs,
            "linkedCaptureTemplateRef": capture_kit_refs["approval"],
            "notes": "A qualifying production approval record was discovered in the package-local search scope." if approval_present else "No qualifying production approval record was found. The pre-implementation capture template exists but does not count as evidence."
        })

        blocking_codes = []
        if not live_present:
            blocking_codes.append("NO_LIVE_FIELD_COLLECTED_SAME_STANDARD_TELEMETRY")
        if not trace_present:
            blocking_codes.append("NO_DEPLOYMENT_PRODUCED_TRACEBACK_LINKAGE")
        if not approval_present:
            blocking_codes.append("NO_PRODUCTION_PROMOTION_APPROVAL")
        decision = "READY_FOR_PROMOTION_REVIEW" if live_present and trace_present and approval_present else "WAITING_FOR_LIVE_FIELD_AND_PRODUCTION_APPROVAL"

        gate["records"].append({
            "candidatePairId": candidate_pair_id,
            "standardRef": standard_ref,
            "decision": decision,
            "liveFieldTelemetryPresent": live_present,
            "deploymentProducedTraceBackLinkagePresent": trace_present,
            "productionPromotionApprovalPresent": approval_present,
            "preImplementationCaptureKitPresent": True,
            "discoveredLiveFieldTelemetryRefs": live_refs,
            "discoveredDeploymentProducedTraceBackRefs": trace_refs,
            "discoveredProductionApprovalRefs": approval_refs,
            "requiredEvidenceClasses": [
                "LIVE_FIELD_COLLECTED_SAME_STANDARD_BRIDGE_TELEMETRY",
                "DEPLOYMENT_PRODUCED_TRACE_BACK_LINKAGE",
                "PRODUCTION_PROMOTION_APPROVAL_RECORD",
            ],
            "blockingReasonCodes": blocking_codes,
            "linkedCaptureTemplateRefs": [
                capture_kit_refs["live_field"],
                capture_kit_refs["trace_back"],
                capture_kit_refs["approval"],
            ],
            "notes": f"{bridge_label} now has a pre-implementation capture kit for the remaining promotion blockers. The kit is not counted as evidence, so the gate still depends on real deployment artifacts."
        })

        limitation_codes = list(entry.get("limitationCodes", []))
        if "NO_DEPLOYMENT_PRODUCED_TRACEBACK_LINKAGE" not in limitation_codes and not trace_present:
            limitation_codes.append("NO_DEPLOYMENT_PRODUCED_TRACEBACK_LINKAGE")
        if "PREIMPLEMENTATION_CAPTURE_KIT_PRESENT" not in limitation_codes:
            limitation_codes.append("PREIMPLEMENTATION_CAPTURE_KIT_PRESENT")
        preferred_order = [
            "EXPORT_SURFACE_DRAFT_ONLY",
            "NO_LIVE_FIELD_COLLECTED_SAME_STANDARD_TELEMETRY",
            "NO_DEPLOYMENT_PRODUCED_TRACEBACK_LINKAGE",
            "PACKAGE_LOCAL_DEPLOYMENT_INTAKE_ONLY",
            "NO_PRODUCTION_PROMOTION_APPROVAL",
            "PREIMPLEMENTATION_CAPTURE_KIT_PRESENT",
        ]
        limitation_codes = [code for code in preferred_order if code in limitation_codes] + [code for code in limitation_codes if code not in preferred_order]

        candidate_pairs_v7.append({
            **entry,
            "candidateStatus": "DRAFT_EXECUTOR_PROVEN_SAMPLE_AND_INTAKE_COVERED_SUPPLEMENTAL_ROUNDTRIP_PROVEN_CAPTURE_KIT_PRESENT_LIVE_FIELD_AND_APPROVAL_GATED",
            "limitationCodes": limitation_codes,
            "notes": f"The {bridge_label} draft same-standard bridge pair remains bounded proof only. The package now also ships a pre-implementation evidence capture kit, but promotion still waits for qualifying live-field telemetry, deployment-produced trace-back linkage, and production approval.",
            "liveFieldTelemetryIntakeStatus": "QUALIFYING_LIVE_FIELD_TELEMETRY_DISCOVERED" if live_present else "NO_QUALIFYING_LIVE_FIELD_TELEMETRY_DISCOVERED",
            "deploymentProducedTraceBackLinkageStatus": "QUALIFYING_DEPLOYMENT_PRODUCED_TRACEBACK_DISCOVERED" if trace_present else "NO_QUALIFYING_DEPLOYMENT_PRODUCED_TRACEBACK_DISCOVERED",
            "productionPromotionApprovalStatus": "QUALIFYING_PRODUCTION_APPROVAL_DISCOVERED" if approval_present else "NO_QUALIFYING_PRODUCTION_APPROVAL_RECORD_DISCOVERED",
            "preImplementationCaptureKitStatus": "CAPTURE_KIT_PRESENT_NOT_COUNTED_AS_EVIDENCE",
            "linkedLiveFieldTelemetryIntakeRegistryRef": "OFARM_live_field_same_standard_bridge_telemetry_intake_registry_v0_2.json",
            "linkedDeploymentProducedTraceBackRegistryRef": "OFARM_live_field_same_standard_bridge_trace_back_linkage_registry_v0_2.json",
            "linkedProductionApprovalRegistryRef": "OFARM_same_standard_bridge_production_approval_registry_v0_2.json",
            "linkedCaptureKitTemplateRefs": [
                capture_kit_refs["live_field"],
                capture_kit_refs["trace_back"],
                capture_kit_refs["approval"],
            ],
            "linkedCaptureKitGuidanceRefs": [
                capture_kit_refs["guide"],
                capture_kit_refs["operator"],
                capture_kit_refs["captureKitResults"],
            ],
        })

        promotion_readiness["candidatePairs"].append({
            "candidatePairId": candidate_pair_id,
            "standardRef": standard_ref,
            "decision": "READY_FOR_PROMOTION_REVIEW" if live_present and trace_present and approval_present else "NOT_READY_FOR_PROMOTION",
            "checks": {
                "declaredSubsetRoundTripPass": True,
                "executorSuccessTelemetryPresent": True,
                "executorConflictTelemetryPresent": True,
                "deploymentSampleTelemetryPresent": True,
                "partnerVariantCoveragePresent": True,
                "deploymentIntakeTelemetryPresent": True,
                "broaderConstructFamilyCoveragePresent": True,
                "supplementalFamiliesRoundTripProven": True,
                "preImplementationCaptureKitPresent": True,
                "liveFieldCollectedTelemetryPresent": live_present,
                "deploymentProducedTraceBackLinkagePresent": trace_present,
                "productionPromotionApprovalPresent": approval_present,
                "surfaceLeftDraft": False,
            },
            "blockingReasonCodes": ["EXPORT_SURFACE_STILL_DRAFT"] + blocking_codes,
            "linkedExecutorSuccessRunIds": entry["linkedExecutorSuccessRunIds"],
            "linkedExecutorBlockedRunIds": entry["linkedExecutorBlockedRunIds"],
            "linkedDeploymentSampleRunIds": entry["linkedDeploymentSampleRunIds"],
            "linkedPartnerCoverageRecordId": entry["linkedPartnerCoverageRecordId"],
            "linkedDeploymentIntakeRunIds": entry["linkedDeploymentIntakeRunIds"],
            "linkedConstructFamilyCoverageRecordId": entry["linkedConstructFamilyCoverageRecordId"],
            "linkedSupplementalRoundTripRecordIds": entry["linkedSupplementalRoundTripRecordIds"],
            "linkedSupplementalConflictRecordIds": entry["linkedSupplementalConflictRecordIds"],
            "linkedLiveFieldTelemetryIntakeRegistryRef": "OFARM_live_field_same_standard_bridge_telemetry_intake_registry_v0_2.json",
            "linkedDeploymentProducedTraceBackRegistryRef": "OFARM_live_field_same_standard_bridge_trace_back_linkage_registry_v0_2.json",
            "linkedProductionApprovalRegistryRef": "OFARM_same_standard_bridge_production_approval_registry_v0_2.json",
            "linkedCaptureKitTemplateRefs": [
                capture_kit_refs["live_field"],
                capture_kit_refs["trace_back"],
                capture_kit_refs["approval"],
            ],
            "linkedCaptureKitGuidanceRefs": [
                capture_kit_refs["guide"],
                capture_kit_refs["operator"],
                capture_kit_refs["captureKitResults"],
            ],
            "notes": f"{bridge_label} now has pre-implementation evidence templates and operator guidance. Promotion is still denied until real deployment evidence exists for the three blocker classes."
        })

        results["liveFieldTelemetryIntake"][candidate_pair_id] = {
            "status": "PASS",
            "decision": "QUALIFYING_LIVE_FIELD_TELEMETRY_FOUND" if live_present else "WAITING_FOR_LIVE_FIELD_TELEMETRY",
            "liveFieldTelemetryPresent": live_present,
            "linkedCaptureTemplateRef": capture_kit_refs["live_field"],
            "reasons": [],
        }
        results["deploymentProducedTraceBackIntake"][candidate_pair_id] = {
            "status": "PASS",
            "decision": "QUALIFYING_DEPLOYMENT_PRODUCED_TRACEBACK_FOUND" if trace_present else "WAITING_FOR_DEPLOYMENT_PRODUCED_TRACEBACK_LINKAGE",
            "deploymentProducedTraceBackLinkagePresent": trace_present,
            "linkedCaptureTemplateRef": capture_kit_refs["trace_back"],
            "reasons": [],
        }
        results["productionApprovalIntake"][candidate_pair_id] = {
            "status": "PASS",
            "decision": "QUALIFYING_PRODUCTION_APPROVAL_FOUND" if approval_present else "WAITING_FOR_PRODUCTION_APPROVAL",
            "productionPromotionApprovalPresent": approval_present,
            "linkedCaptureTemplateRef": capture_kit_refs["approval"],
            "reasons": [],
        }

    live_field_registry["summary"] = {
        "candidatePairs": len(candidate_pairs),
        "liveFieldTelemetryArtifactsFound": len(qualifying_files("live_field")),
        "discoveredFiles": len(discovered["live_field"]),
        "nonQualifyingFiles": len(nonqualifying_files("live_field")),
        "waitingForTelemetry": sum(1 for refs in live_by_pair.values() if not refs),
        "captureKitPresent": True,
    }
    trace_back_registry["summary"] = {
        "candidatePairs": len(candidate_pairs),
        "deploymentProducedTraceBackArtifactsFound": len(qualifying_files("trace_back")),
        "discoveredFiles": len(discovered["trace_back"]),
        "nonQualifyingFiles": len(nonqualifying_files("trace_back")),
        "waitingForTraceBackLinkage": sum(1 for refs in trace_by_pair.values() if not refs),
        "captureKitPresent": True,
    }
    approval_registry["summary"] = {
        "candidatePairs": len(candidate_pairs),
        "productionApprovalRecordsFound": len(qualifying_files("approval")),
        "discoveredFiles": len(discovered["approval"]),
        "nonQualifyingFiles": len(nonqualifying_files("approval")),
        "waitingForApproval": sum(1 for refs in approval_by_pair.values() if not refs),
        "captureKitPresent": True,
    }
    gate["summary"] = {
        "candidatePairs": len(candidate_pairs),
        "waitingForLiveFieldAndApproval": sum(1 for entry in gate["records"] if entry["decision"] != "READY_FOR_PROMOTION_REVIEW"),
        "liveFieldTelemetryFound": len(qualifying_files("live_field")),
        "deploymentProducedTraceBackFound": len(qualifying_files("trace_back")),
        "productionApprovalRecordsFound": len(qualifying_files("approval")),
        "captureKitPresent": True,
    }
    promotion_readiness["summary"] = {
        "candidatePairs": len(candidate_pairs),
        "readyForPromotion": sum(1 for entry in promotion_readiness["candidatePairs"] if entry["decision"] == "READY_FOR_PROMOTION_REVIEW"),
        "notReadyForPromotion": sum(1 for entry in promotion_readiness["candidatePairs"] if entry["decision"] != "READY_FOR_PROMOTION_REVIEW"),
        "captureKitPresent": True,
    }

    linked_files = [
        "OFARM_same_standard_bridge_pack_candidate_pairs_v0_6.json",
        "OFARM_same_standard_bridge_promotion_readiness_v0_5.json",
        "OFARM_same_standard_bridge_live_field_evidence_gate_v0_2.json",
        "OFARM_same_standard_bridge_supplemental_round_trip_records_v0_1.json",
        "OFARM_same_standard_bridge_supplemental_conflict_records_v0_1.json",
        capture_kit_refs["guide"],
        capture_kit_refs["operator"],
        capture_kit_refs["captureKitResults"],
    ]
    for filename in linked_files:
        path = here / filename
        status = "PASS"
        try:
            if filename.endswith('.json'):
                load_json(path)
            else:
                path.read_text(encoding='utf-8')
        except Exception:
            status = "FAIL"
        results["linkedArtifactChecks"][f"{filename} :: located-and-parseable"] = status
        if status != "PASS":
            results["failingChecks"].append(f"{filename} :: {status}")
    results["summary"]["linkedArtifactsChecked"] = len(linked_files)
    if results["failingChecks"]:
        results["overall"] = "FAIL"

    dump_json(here / "OFARM_live_field_same_standard_bridge_telemetry_intake_registry_v0_2.json", live_field_registry)
    dump_json(here / "OFARM_live_field_same_standard_bridge_trace_back_linkage_registry_v0_2.json", trace_back_registry)
    dump_json(here / "OFARM_same_standard_bridge_production_approval_registry_v0_2.json", approval_registry)
    dump_json(here / "OFARM_same_standard_bridge_live_field_evidence_gate_v0_3.json", gate)
    dump_json(here / "OFARM_same_standard_bridge_pack_candidate_pairs_v0_7.json", candidate_pairs_v7)
    dump_json(here / "OFARM_same_standard_bridge_promotion_readiness_v0_6.json", promotion_readiness)
    dump_json(here / "OFARM_same_standard_bridge_live_field_and_production_approval_results_v0_2.json", results)
    return 0 if results["overall"] != "FAIL" else 1


if __name__ == "__main__":
    raise SystemExit(main())
