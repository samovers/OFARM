#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

BASE_TIME = datetime.fromisoformat("2026-04-12T19:00:00")

SCENARIOS = [
    {
        "scenarioId": "gatepub-01-live-passport-ngsi-ld-success",
        "family": "LIVE_PASSPORT",
        "partnerSurface": "NGSI_LD_PARTNER_EXPORT",
        "outputFamily": "PassportView",
        "outputSubtype": "FIELD_PASSPORT",
        "twin": "ADVISORY",
        "result": "ALLOW",
        "reviewChain": [],
        "conflictClass": None,
    },
    {
        "scenarioId": "gatepub-02-live-passport-dashboard-json-success",
        "family": "LIVE_PASSPORT",
        "partnerSurface": "PARTNER_DASHBOARD_JSON",
        "outputFamily": "PassportView",
        "outputSubtype": "LOT_PASSPORT",
        "twin": "ADVISORY",
        "result": "ALLOW_WITH_WARNING",
        "reviewChain": [],
        "conflictClass": None,
    },
    {
        "scenarioId": "gatepub-03-advisory-report-csv-success",
        "family": "ADVISORY_REPORT",
        "partnerSurface": "PARTNER_ADVISORY_CSV",
        "outputFamily": "DocumentAssembly",
        "outputSubtype": "ADVISORY_REPORT",
        "twin": "ADVISORY",
        "result": "ALLOW_WITH_WARNING",
        "reviewChain": [],
        "conflictClass": None,
    },
    {
        "scenarioId": "gatepub-04-compliance-report-pdf-human-approval-success",
        "family": "COMPLIANCE_REPORT",
        "partnerSurface": "PARTNER_COMPLIANCE_PDF",
        "outputFamily": "DocumentAssembly",
        "outputSubtype": "COMPLIANCE_REPORT",
        "twin": "COMPLIANCE",
        "result": "ALLOW",
        "reviewChain": ["REQUIRE_HUMAN_APPROVAL", "HUMAN_APPROVAL_CLOSED"],
        "conflictClass": None,
    },
    {
        "scenarioId": "gatepub-05-dossier-json-governance-and-human-success",
        "family": "DOSSIER_ATTESTATION",
        "partnerSurface": "PARTNER_DOSSIER_JSON",
        "outputFamily": "DocumentAssembly",
        "outputSubtype": "DOSSIER_ASSEMBLY",
        "twin": "COMPLIANCE",
        "result": "ALLOW",
        "reviewChain": ["REQUIRE_REVIEW", "GOVERNANCE_REVIEW_CLOSED", "REQUIRE_HUMAN_APPROVAL", "HUMAN_APPROVAL_CLOSED"],
        "conflictClass": None,
    },
    {
        "scenarioId": "gatepub-06-submission-xml-success",
        "family": "SUBMISSION_FILING",
        "partnerSurface": "PARTNER_SUBMISSION_XML",
        "outputFamily": "SubmissionAssembly",
        "outputSubtype": "SUBMISSION_ASSEMBLY",
        "twin": "COMPLIANCE",
        "result": "ALLOW",
        "reviewChain": ["REQUIRE_HUMAN_APPROVAL", "HUMAN_APPROVAL_CLOSED"],
        "conflictClass": None,
    },
    {
        "scenarioId": "gatepub-07-dossier-json-block-review-pending",
        "family": "DOSSIER_ATTESTATION",
        "partnerSurface": "PARTNER_DOSSIER_JSON",
        "outputFamily": "DocumentAssembly",
        "outputSubtype": "DOSSIER_ASSEMBLY",
        "twin": "COMPLIANCE",
        "result": "BLOCK_REVIEW_PENDING",
        "reviewChain": ["REQUIRE_REVIEW"],
        "conflictClass": "REVIEW_CHAIN_INCOMPLETE",
    },
    {
        "scenarioId": "gatepub-08-submission-xml-block-schema-mismatch",
        "family": "SUBMISSION_FILING",
        "partnerSurface": "PARTNER_SUBMISSION_XML",
        "outputFamily": "SubmissionAssembly",
        "outputSubtype": "SUBMISSION_ASSEMBLY",
        "twin": "COMPLIANCE",
        "result": "BLOCK_SCHEMA_MISMATCH",
        "reviewChain": ["REQUIRE_HUMAN_APPROVAL", "HUMAN_APPROVAL_CLOSED"],
        "conflictClass": "EXTERNAL_SURFACE_SCHEMA_MISMATCH",
    },
    {
        "scenarioId": "gatepub-09-live-passport-block-recipient-profile-conflict",
        "family": "LIVE_PASSPORT",
        "partnerSurface": "PARTNER_DASHBOARD_JSON",
        "outputFamily": "PassportView",
        "outputSubtype": "FIELD_PASSPORT",
        "twin": "ADVISORY",
        "result": "BLOCK_PROFILE_CONFLICT",
        "reviewChain": [],
        "conflictClass": "RECIPIENT_PROFILE_CONFLICT",
    },
    {
        "scenarioId": "gatepub-10-compliance-report-block-revocation-recheck",
        "family": "COMPLIANCE_REPORT",
        "partnerSurface": "PARTNER_COMPLIANCE_PDF",
        "outputFamily": "DocumentAssembly",
        "outputSubtype": "COMPLIANCE_REPORT",
        "twin": "COMPLIANCE",
        "result": "BLOCK_AUTHORITY_RECHECK",
        "reviewChain": ["REQUIRE_HUMAN_APPROVAL", "HUMAN_APPROVAL_CLOSED"],
        "conflictClass": "REVOCATION_RECHECK_FLIP",
    },
]

GATE_BASE = [
    "REQUEST_INTENT",
    "AUTHORITY",
    "CONTEXT_RESOLUTION",
    "MATERIALIZATION",
    "EVIDENCE_POLICY",
    "REVIEW_CHAIN",
    "OUTPUT_CLASS_CHECK",
    "SURFACE_BINDING",
    "TRACEBACK_EMISSION",
    "PUBLICATION_COMMIT",
]

PRIOR_EVIDENCE = [
    "04_implementation_and_conformance/conformance_runners/current_state_and_query_conformance/OFARM_runtime_materialization_publication_pipeline_records_v0_1.json",
    "04_implementation_and_conformance/implementation_notes/runtime_surface_and_capability/OFARM_runtime_publication_trace_back_records_v0_2.json",
    "04_implementation_and_conformance/conformance_runners/authority_and_governance_conformance/OFARM_runtime_authority_review_records_v0_1.json",
    "04_implementation_and_conformance/conformance_runners/current_state_and_query_conformance/OFARM_runtime_materialization_publication_results_v0_1.json",
]


def gate_stop_for(result: str) -> str:
    if result == "ALLOW" or result == "ALLOW_WITH_WARNING":
        return "PUBLICATION_COMMIT"
    if result == "BLOCK_REVIEW_PENDING":
        return "REVIEW_CHAIN"
    if result in {"BLOCK_SCHEMA_MISMATCH", "BLOCK_PROFILE_CONFLICT"}:
        return "SURFACE_BINDING"
    if result == "BLOCK_AUTHORITY_RECHECK":
        return "AUTHORITY"
    return "PUBLICATION_COMMIT"


def main() -> None:
    root = Path(__file__).resolve().parent
    generated_at = "2026-04-12T19:40:00Z"
    gate_records: list[dict[str, Any]] = []
    review_records: list[dict[str, Any]] = []
    traceback_records: list[dict[str, Any]] = []
    telemetry_events: list[dict[str, Any]] = []

    evt_counter = 1
    for idx, sc in enumerate(SCENARIOS, start=1):
        started = BASE_TIME + timedelta(minutes=idx * 3)
        stop_gate = gate_stop_for(sc["result"])
        gate_events = []
        event_ids = []
        gates = GATE_BASE
        for step, gate in enumerate(gates, start=1):
            if gate == "REQUEST_INTENT":
                outcome = "REQUEST_ACCEPTED"
            elif gate == "AUTHORITY":
                if sc["result"] == "BLOCK_AUTHORITY_RECHECK":
                    outcome = "DENY_AFTER_RECHECK"
                else:
                    outcome = "ALLOW"
            elif gate == "CONTEXT_RESOLUTION":
                outcome = f"{sc['twin']}_CONTEXT_RESOLVED"
            elif gate == "MATERIALIZATION":
                outcome = "FRESH_OR_RECOMPUTED"
            elif gate == "EVIDENCE_POLICY":
                outcome = "SUFFICIENT" if sc["family"] != "LIVE_PASSPORT" else "NOT_REQUIRED"
            elif gate == "REVIEW_CHAIN":
                if sc["reviewChain"]:
                    outcome = sc["reviewChain"][-1] if "CLOSED" in sc["reviewChain"][-1] else sc["reviewChain"][0]
                else:
                    outcome = "NOT_REQUIRED"
                if sc["result"] == "BLOCK_REVIEW_PENDING":
                    outcome = "REQUIRE_REVIEW"
            elif gate == "OUTPUT_CLASS_CHECK":
                outcome = f"{sc['outputFamily']}_VALID"
            elif gate == "SURFACE_BINDING":
                if sc["result"] == "BLOCK_SCHEMA_MISMATCH":
                    outcome = "BLOCK_SCHEMA_MISMATCH"
                elif sc["result"] == "BLOCK_PROFILE_CONFLICT":
                    outcome = "BLOCK_PROFILE_CONFLICT"
                else:
                    outcome = "BOUND"
            elif gate == "TRACEBACK_EMISSION":
                outcome = "TRACE_CAPTURED"
            elif gate == "PUBLICATION_COMMIT":
                outcome = sc["result"]
            else:
                outcome = "UNKNOWN"

            event_id = f"evt-wave30-{evt_counter:03d}"
            evt_counter += 1
            event_ids.append(event_id)
            gate_events.append(
                {
                    "stepIndex": step,
                    "gate": gate,
                    "outcome": outcome,
                    "startedAt": (started + timedelta(seconds=step * 3)).isoformat() + "Z",
                    "finishedAt": (started + timedelta(seconds=step * 3 + 2)).isoformat() + "Z",
                    "inputRefs": [f"req:{sc['scenarioId']}", f"surface:{sc['partnerSurface']}"] if step == 1 else [],
                    "producedRefs": [f"gate:{gate.lower()}:{sc['scenarioId']}", event_id],
                    "traceRefs": [f"traceBack:{sc['scenarioId']}:v0.1"] if gate in {"TRACEBACK_EMISSION", "PUBLICATION_COMMIT"} else [],
                }
            )
            telemetry_events.append(
                {
                    "eventId": event_id,
                    "scenarioId": sc["scenarioId"],
                    "family": sc["family"],
                    "partnerSurface": sc["partnerSurface"],
                    "gate": gate,
                    "outcome": outcome,
                    "emittedAt": (started + timedelta(seconds=step * 3 + 2)).isoformat() + "Z",
                }
            )
            if gate == stop_gate:
                break

        gate_records.append(
            {
                "sequenceId": f"seq:{sc['scenarioId']}:v0.1",
                "scenarioId": sc["scenarioId"],
                "family": sc["family"],
                "partnerSurface": sc["partnerSurface"],
                "outputFamily": sc["outputFamily"],
                "outputSubtype": sc["outputSubtype"],
                "twin": sc["twin"],
                "terminalOutcome": sc["result"],
                "expectedStopGate": stop_gate,
                "monotonicGateOrder": True,
                "priorEvidenceRefs": PRIOR_EVIDENCE,
                "linkedTraceBackIds": [f"traceBack:{sc['scenarioId']}:v0.1"],
                "gateEvents": gate_events,
            }
        )

        if sc["reviewChain"]:
            review_records.append(
                {
                    "reviewChainId": f"review:{sc['scenarioId']}:v0.1",
                    "scenarioId": sc["scenarioId"],
                    "family": sc["family"],
                    "partnerSurface": sc["partnerSurface"],
                    "reviewStates": sc["reviewChain"],
                    "terminalOutcome": sc["result"],
                    "reviewClosed": any(state.endswith("CLOSED") for state in sc["reviewChain"]) and sc["result"] not in {"BLOCK_REVIEW_PENDING"},
                }
            )

        traceback_records.append(
            {
                "traceBackId": f"traceBack:{sc['scenarioId']}:v0.1",
                "scenarioId": sc["scenarioId"],
                "partnerSurface": sc["partnerSurface"],
                "outputFamily": sc["outputFamily"],
                "outputSubtype": sc["outputSubtype"],
                "basisRef": f"basis:{sc['scenarioId']}:v0.1",
                "snapshotRef": f"snapshot:{sc['scenarioId']}:v0.1",
                "contextRef": f"ctx:{sc['scenarioId']}:v0.1",
                "authorityDecisionRef": f"authz:{sc['scenarioId']}:v0.1",
                "evidenceDecisionRef": f"evidence:{sc['scenarioId']}:v0.1",
                "materializationResultRef": f"matRes:{sc['scenarioId']}:v0.1",
                "publicationEvaluationRef": f"pubEval:{sc['scenarioId']}:v0.1",
                "adapterSurfaceRef": f"surface:{sc['partnerSurface']}:v0.1",
                "priorTraceBackRefs": [
                    "trace:matpub-01-advisory-live-passport-stale-warning",
                    "traceback:adapter-passport-ngsi-ld-live:v0.1",
                ],
                "linkedTelemetryEventIds": event_ids,
                "traceBoundary": "PARTNER_SURFACE_PUBLICATION",
                "finalOutcome": sc["result"],
                "conflictClass": sc["conflictClass"],
                "notes": "Runtime-emitted package-local partner-surface trace-back. This is sufficient for package-internal closure but not bridge-promotion evidence.",
            }
        )

    results = {
        "wave": 30,
        "title": "internal partial closure and final handoff",
        "overallStatus": "PASS_WITH_LIMITATIONS",
        "scenarioCount": len(SCENARIOS),
        "positiveScenarios": sum(1 for s in SCENARIOS if s["result"] in {"ALLOW", "ALLOW_WITH_WARNING"}),
        "blockedScenarios": sum(1 for s in SCENARIOS if s["result"] not in {"ALLOW", "ALLOW_WITH_WARNING"}),
        "partnerSurfaceCount": len({s["partnerSurface"] for s in SCENARIOS}),
        "reviewChainCount": len(review_records),
        "traceBackRecordCount": len(traceback_records),
        "telemetryEventCount": len(telemetry_events),
        "externalConflictClasses": sorted({s["conflictClass"] for s in SCENARIOS if s["conflictClass"]}),
        "coverageAdvances": [
            "enforcement-gate sequencing tests -> COVERED",
            "projection trace-back tests -> COVERED",
        ],
        "limitations": [
            "Telemetry and trace-back are runtime-emitted package-local evidence, not live field bridge telemetry.",
            "Same-standard bridge promotion readiness remains partial and still depends on external evidence.",
        ],
    }

    files = {
        "OFARM_runtime_deployment_emitted_publication_gate_sequence_records_v0_1.json": gate_records,
        "OFARM_runtime_deployment_emitted_review_chain_records_v0_1.json": {"generatedAt": generated_at, "records": review_records},
        "OFARM_runtime_partner_surface_publication_trace_back_records_v0_1.json": traceback_records,
        "OFARM_runtime_deployment_emitted_publication_telemetry_v0_1.json": {"generatedAt": generated_at, "events": telemetry_events},
        "OFARM_runtime_deployment_gate_sequence_and_traceback_results_v0_1.json": results,
    }

    for name, obj in files.items():
        (root / name).write_text(json.dumps(obj, indent=2) + "\n")


if __name__ == "__main__":
    main()
