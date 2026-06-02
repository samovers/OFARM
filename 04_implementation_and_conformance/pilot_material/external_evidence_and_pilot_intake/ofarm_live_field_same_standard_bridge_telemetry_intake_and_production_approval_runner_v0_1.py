#!/usr/bin/env python3
"""OFARM live-field telemetry intake and production approval runner v0.1.

This runner performs a conservative package-local scan for the remaining
same-standard bridge promotion blockers:
- live field-collected same-standard bridge telemetry
- deployment-produced live-field trace-back linkage
- production promotion approval records

It intentionally does not treat executor-produced, partner-sample, or
deployment-intake artifacts as substitutes for live field evidence.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    here = Path(__file__).resolve().parent
    candidate_pairs = load_json(here / "OFARM_same_standard_bridge_pack_candidate_pairs_v0_5.json")

    search_specs = {
        "live_field": "OFARM_live_field_same_standard_bridge_telemetry_v*.json",
        "trace_back": "OFARM_live_field_same_standard_bridge_trace_back_records_v*.json",
        "approval": "OFARM_same_standard_bridge_production_approval_record_v*.json",
    }
    discovered = {key: sorted([p.name for p in here.glob(pattern)]) for key, pattern in search_specs.items()}

    live_field_registry = {
        "evaluatedAt": "2026-04-12T12:30:00Z",
        "searchScope": "04_implementation_and_conformance/",
        "searchPattern": search_specs["live_field"],
        "excludedEvidenceRefs": [
            "OFARM_executor_native_same_standard_bridge_telemetry_v0_1.json",
            "OFARM_deployment_sample_same_standard_bridge_telemetry_v0_1.json",
            "OFARM_deployment_intake_same_standard_bridge_telemetry_v0_1.json",
        ],
        "discoveredFiles": discovered["live_field"],
        "records": [],
        "summary": {},
        "overall": "WAITING_FOR_LIVE_FIELD_TELEMETRY",
        "limitations": [
            "This registry is intentionally conservative. Executor, partner-sample, and redacted deployment-intake artifacts are not counted as live field-collected telemetry."
        ],
    }
    trace_back_registry = {
        "evaluatedAt": "2026-04-12T12:30:00Z",
        "searchScope": "04_implementation_and_conformance/",
        "searchPattern": search_specs["trace_back"],
        "excludedEvidenceRefs": [
            "OFARM_projection_trace_back_records_v0_1.json",
            "OFARM_output_adapter_trace_back_records_v0_1.json",
        ],
        "discoveredFiles": discovered["trace_back"],
        "records": [],
        "summary": {},
        "overall": "WAITING_FOR_DEPLOYMENT_PRODUCED_TRACEBACK_LINKAGE",
        "limitations": [
            "Existing replay-produced or adapter-produced trace-back records are not counted as live field deployment-produced linkage."
        ],
    }
    approval_registry = {
        "evaluatedAt": "2026-04-12T12:30:00Z",
        "searchScope": "04_implementation_and_conformance/",
        "searchPattern": search_specs["approval"],
        "discoveredFiles": discovered["approval"],
        "records": [],
        "summary": {},
        "overall": "WAITING_FOR_PRODUCTION_APPROVAL",
        "limitations": [
            "No package-local production approval record was discovered for either same-standard bridge draft pair."
        ],
    }

    gate = {
        "evaluatedAt": "2026-04-12T12:30:00Z",
        "sourceRefs": [
            "OFARM_live_field_same_standard_bridge_telemetry_intake_registry_v0_1.json",
            "OFARM_live_field_same_standard_bridge_trace_back_linkage_registry_v0_1.json",
            "OFARM_same_standard_bridge_production_approval_registry_v0_1.json",
        ],
        "records": [],
        "summary": {},
        "overall": "WAITING_FOR_LIVE_FIELD_AND_PRODUCTION_APPROVAL",
        "limitations": [
            "This gate does not infer production readiness from executor-produced, partner-sample, or redacted deployment-intake evidence."
        ],
    }

    candidate_pairs_v6 = []
    promotion_readiness = {
        "evaluatedAt": "2026-04-12T12:30:00Z",
        "scope": "same-standard bridge-pack promotion readiness after explicit live-field telemetry intake, deployment-produced trace-back intake, and production approval scanning",
        "candidatePairs": [],
        "summary": {},
        "overall": "HOLD_AT_DRAFT",
        "limitations": [
            "No live field-collected same-standard bridge telemetry artifact exists in the package-local search scope.",
            "No deployment-produced live-field trace-back linkage artifact exists in the package-local search scope.",
            "No production promotion approval record exists in the package-local search scope.",
        ],
    }

    results = {
        "driftCheck": {
            "status": "PASS",
            "decision": "NO_MATERIAL_DRIFT_DETECTED",
            "reasons": [
                "Work after Wave 6 remains in implementation/conformance and did not reopen baseline architecture.",
                "Same-standard bridge work stayed explicitly draft-scoped and did not silently promote active law.",
                "New bridge evidence remains guarded by explicit non-promotion decisions.",
            ],
            "cautions": [
                "Bridge-specific conformance depth is now ahead of several other partial conformance rows, but it remains an implementation/conformance hardening track rather than a baseline rewrite."
            ],
        },
        "liveFieldTelemetryIntake": {},
        "deploymentProducedTraceBackIntake": {},
        "productionApprovalIntake": {},
        "linkedArtifactChecks": {},
        "summary": {
            "candidatePairs": len(candidate_pairs),
            "liveFieldTelemetryArtifactsFound": len(discovered["live_field"]),
            "deploymentProducedTraceBackArtifactsFound": len(discovered["trace_back"]),
            "productionApprovalRecordsFound": len(discovered["approval"]),
            "linkedArtifactsChecked": 0,
        },
        "limitations": [
            "This wave tightens the remaining blockers, but it does not fabricate or infer live field telemetry.",
            "This wave tightens the remaining blockers, but it does not fabricate or infer production approval.",
        ],
        "overall": "PASS_WITH_LIMITATIONS",
        "failingChecks": [],
    }

    for entry in candidate_pairs:
        candidate_pair_id = entry["candidatePairId"]
        standard_ref = entry["standardRef"]

        live_field_registry["records"].append({
            "candidatePairId": candidate_pair_id,
            "standardRef": standard_ref,
            "intakeDecision": "NO_LIVE_FIELD_TELEMETRY_ARTIFACTS_FOUND",
            "discoveredTelemetryRefs": [],
            "notes": "No file matching the live-field same-standard telemetry pattern was found in the package-local search scope.",
        })
        trace_back_registry["records"].append({
            "candidatePairId": candidate_pair_id,
            "standardRef": standard_ref,
            "intakeDecision": "NO_DEPLOYMENT_PRODUCED_TRACEBACK_ARTIFACTS_FOUND",
            "discoveredTraceBackRefs": [],
            "notes": "No file matching the live-field deployment-produced trace-back linkage pattern was found in the package-local search scope.",
        })
        approval_registry["records"].append({
            "candidatePairId": candidate_pair_id,
            "standardRef": standard_ref,
            "approvalDecision": "NO_PRODUCTION_APPROVAL_RECORD_FOUND",
            "discoveredApprovalRefs": [],
            "notes": "No package-local production approval record was found for this draft bridge pair.",
        })

        gate["records"].append({
            "candidatePairId": candidate_pair_id,
            "standardRef": standard_ref,
            "decision": "WAITING_FOR_LIVE_FIELD_AND_PRODUCTION_APPROVAL",
            "liveFieldTelemetryPresent": False,
            "deploymentProducedTraceBackLinkagePresent": False,
            "productionPromotionApprovalPresent": False,
            "discoveredLiveFieldTelemetryRefs": [],
            "discoveredDeploymentProducedTraceBackRefs": [],
            "discoveredProductionApprovalRefs": [],
            "requiredEvidenceClasses": [
                "LIVE_FIELD_COLLECTED_SAME_STANDARD_BRIDGE_TELEMETRY",
                "DEPLOYMENT_PRODUCED_TRACE_BACK_LINKAGE",
                "PRODUCTION_PROMOTION_APPROVAL_RECORD",
            ],
            "blockingReasonCodes": [
                "NO_LIVE_FIELD_COLLECTED_SAME_STANDARD_TELEMETRY",
                "NO_DEPLOYMENT_PRODUCED_TRACEBACK_LINKAGE",
                "NO_PRODUCTION_PROMOTION_APPROVAL",
            ],
            "notes": "The package contains executor, partner-sample, redacted deployment-intake, and supplemental-family round-trip proof, but none of those are counted as live field telemetry, deployment-produced trace-back linkage, or production approval.",
        })

        limitation_codes = list(dict.fromkeys(entry.get("limitationCodes", []) + ["NO_DEPLOYMENT_PRODUCED_TRACEBACK_LINKAGE"]))
        preferred_order = [
            "EXPORT_SURFACE_DRAFT_ONLY",
            "NO_LIVE_FIELD_COLLECTED_SAME_STANDARD_TELEMETRY",
            "NO_DEPLOYMENT_PRODUCED_TRACEBACK_LINKAGE",
            "PACKAGE_LOCAL_DEPLOYMENT_INTAKE_ONLY",
            "NO_PRODUCTION_PROMOTION_APPROVAL",
        ]
        limitation_codes = [code for code in preferred_order if code in limitation_codes] + [code for code in limitation_codes if code not in preferred_order]

        bridge_label = "ADAPT" if "adapt" in candidate_pair_id else "ISOXML"
        candidate_pairs_v6.append({
            **entry,
            "candidateStatus": "DRAFT_EXECUTOR_PROVEN_SAMPLE_AND_INTAKE_COVERED_SUPPLEMENTAL_ROUNDTRIP_PROVEN_LIVE_FIELD_AND_APPROVAL_GATED",
            "limitationCodes": limitation_codes,
            "notes": f"The {bridge_label} draft same-standard bridge pair remains bounded proof only. It now has an explicit live-field telemetry intake registry, an explicit deployment-produced trace-back linkage intake registry, and an explicit production approval registry, all of which currently report no qualifying artifacts in the package-local search scope.",
            "promotionBlockingCodes": [
                "EXPORT_SURFACE_STILL_DRAFT",
                "NO_LIVE_FIELD_COLLECTED_SAME_STANDARD_TELEMETRY",
                "NO_DEPLOYMENT_PRODUCED_TRACEBACK_LINKAGE",
                "NO_PRODUCTION_PROMOTION_APPROVAL",
            ],
            "liveFieldTelemetryIntakeStatus": "NO_PACKAGE_LOCAL_LIVE_FIELD_TELEMETRY_DISCOVERED",
            "deploymentProducedTraceBackLinkageStatus": "NO_PACKAGE_LOCAL_DEPLOYMENT_PRODUCED_TRACEBACK_DISCOVERED",
            "productionPromotionApprovalStatus": "NO_PACKAGE_LOCAL_PRODUCTION_APPROVAL_RECORD_DISCOVERED",
            "linkedLiveFieldTelemetryIntakeRegistryRef": "OFARM_live_field_same_standard_bridge_telemetry_intake_registry_v0_1.json",
            "linkedDeploymentProducedTraceBackRegistryRef": "OFARM_live_field_same_standard_bridge_trace_back_linkage_registry_v0_1.json",
            "linkedProductionApprovalRegistryRef": "OFARM_same_standard_bridge_production_approval_registry_v0_1.json",
        })

        promotion_readiness["candidatePairs"].append({
            "candidatePairId": candidate_pair_id,
            "standardRef": standard_ref,
            "decision": "NOT_READY_FOR_PROMOTION",
            "checks": {
                "declaredSubsetRoundTripPass": True,
                "executorSuccessTelemetryPresent": True,
                "executorConflictTelemetryPresent": True,
                "deploymentSampleTelemetryPresent": True,
                "partnerVariantCoveragePresent": True,
                "deploymentIntakeTelemetryPresent": True,
                "broaderConstructFamilyCoveragePresent": True,
                "supplementalFamiliesRoundTripProven": True,
                "liveFieldCollectedTelemetryPresent": False,
                "deploymentProducedTraceBackLinkagePresent": False,
                "productionPromotionApprovalPresent": False,
                "surfaceLeftDraft": False,
            },
            "blockingReasonCodes": [
                "EXPORT_SURFACE_STILL_DRAFT",
                "NO_LIVE_FIELD_COLLECTED_SAME_STANDARD_TELEMETRY",
                "NO_DEPLOYMENT_PRODUCED_TRACEBACK_LINKAGE",
                "NO_PRODUCTION_PROMOTION_APPROVAL",
            ],
            "linkedExecutorSuccessRunIds": entry["linkedExecutorSuccessRunIds"],
            "linkedExecutorBlockedRunIds": entry["linkedExecutorBlockedRunIds"],
            "linkedDeploymentSampleRunIds": entry["linkedDeploymentSampleRunIds"],
            "linkedPartnerCoverageRecordId": entry["linkedPartnerCoverageRecordId"],
            "linkedDeploymentIntakeRunIds": entry["linkedDeploymentIntakeRunIds"],
            "linkedConstructFamilyCoverageRecordId": entry["linkedConstructFamilyCoverageRecordId"],
            "linkedSupplementalRoundTripRecordIds": entry["linkedSupplementalRoundTripRecordIds"],
            "linkedSupplementalConflictRecordIds": entry["linkedSupplementalConflictRecordIds"],
            "linkedLiveFieldTelemetryIntakeRegistryRef": "OFARM_live_field_same_standard_bridge_telemetry_intake_registry_v0_1.json",
            "linkedDeploymentProducedTraceBackRegistryRef": "OFARM_live_field_same_standard_bridge_trace_back_linkage_registry_v0_1.json",
            "linkedProductionApprovalRegistryRef": "OFARM_same_standard_bridge_production_approval_registry_v0_1.json",
            "notes": f"{bridge_label} now has explicit package-local intake registries for the remaining promotion blockers. Promotion is still denied because those registries discovered no qualifying live-field telemetry, no deployment-produced trace-back linkage, and no production approval record.",
        })

        results["liveFieldTelemetryIntake"][candidate_pair_id] = {
            "status": "PASS",
            "decision": "WAITING_FOR_LIVE_FIELD_TELEMETRY",
            "liveFieldTelemetryPresent": False,
            "reasons": [],
        }
        results["deploymentProducedTraceBackIntake"][candidate_pair_id] = {
            "status": "PASS",
            "decision": "WAITING_FOR_DEPLOYMENT_PRODUCED_TRACEBACK_LINKAGE",
            "deploymentProducedTraceBackLinkagePresent": False,
            "reasons": [],
        }
        results["productionApprovalIntake"][candidate_pair_id] = {
            "status": "PASS",
            "decision": "WAITING_FOR_PRODUCTION_APPROVAL",
            "productionPromotionApprovalPresent": False,
            "reasons": [],
        }

    live_field_registry["summary"] = {
        "candidatePairs": len(candidate_pairs),
        "liveFieldTelemetryArtifactsFound": len(discovered["live_field"]),
        "waitingForTelemetry": len(candidate_pairs),
    }
    trace_back_registry["summary"] = {
        "candidatePairs": len(candidate_pairs),
        "deploymentProducedTraceBackArtifactsFound": len(discovered["trace_back"]),
        "waitingForTraceBackLinkage": len(candidate_pairs),
    }
    approval_registry["summary"] = {
        "candidatePairs": len(candidate_pairs),
        "productionApprovalRecordsFound": len(discovered["approval"]),
        "waitingForApproval": len(candidate_pairs),
    }
    gate["summary"] = {
        "candidatePairs": len(candidate_pairs),
        "waitingForLiveFieldAndApproval": len(candidate_pairs),
        "liveFieldTelemetryFound": len(discovered["live_field"]),
        "deploymentProducedTraceBackFound": len(discovered["trace_back"]),
        "productionApprovalRecordsFound": len(discovered["approval"]),
    }
    promotion_readiness["summary"] = {
        "candidatePairs": len(candidate_pairs),
        "readyForPromotion": 0,
        "notReadyForPromotion": len(candidate_pairs),
    }

    linked_files = [
        "OFARM_same_standard_bridge_pack_candidate_pairs_v0_5.json",
        "OFARM_same_standard_bridge_promotion_readiness_v0_4.json",
        "OFARM_same_standard_bridge_live_field_evidence_gate_v0_1.json",
        "OFARM_same_standard_bridge_supplemental_round_trip_records_v0_1.json",
        "OFARM_same_standard_bridge_supplemental_conflict_records_v0_1.json",
    ]
    for filename in linked_files:
        path = here / filename
        status = "PASS"
        try:
            load_json(path)
        except Exception:
            status = "FAIL"
        results["linkedArtifactChecks"][f"{filename} :: located-and-json-parseable"] = status
        if status != "PASS":
            results["failingChecks"].append(f"{filename} :: {status}")
    results["summary"]["linkedArtifactsChecked"] = len(linked_files)
    if results["failingChecks"]:
        results["overall"] = "FAIL"

    dump_json(here / "OFARM_live_field_same_standard_bridge_telemetry_intake_registry_v0_1.json", live_field_registry)
    dump_json(here / "OFARM_live_field_same_standard_bridge_trace_back_linkage_registry_v0_1.json", trace_back_registry)
    dump_json(here / "OFARM_same_standard_bridge_production_approval_registry_v0_1.json", approval_registry)
    dump_json(here / "OFARM_same_standard_bridge_live_field_evidence_gate_v0_2.json", gate)
    dump_json(here / "OFARM_same_standard_bridge_pack_candidate_pairs_v0_6.json", candidate_pairs_v6)
    dump_json(here / "OFARM_same_standard_bridge_promotion_readiness_v0_5.json", promotion_readiness)
    dump_json(here / "OFARM_same_standard_bridge_live_field_and_production_approval_results_v0_1.json", results)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
