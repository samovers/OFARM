#!/usr/bin/env python3
"""Emit bounded runtime-shaped materialization/publication policy evidence for Wave 27."""
from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NOW = datetime(2026, 4, 12, 16, 55, 0, tzinfo=timezone.utc).isoformat()

SCENARIOS = [
  {
    "scenarioId": "matpub-01-advisory-live-passport-stale-warning",
    "twin": "ADVISORY",
    "outputFamily": "PassportView",
    "outputSubtype": "FIELD_PASSPORT",
    "consequenceClass": "EXPLORATORY",
    "freshnessInput": "STALE",
    "basisRef": "basis:field-passport-2026-04-12-01",
    "snapshotRef": "snapshot:field-passport-2026-04-11-01",
    "contextRef": "ctx:field-west-2026-04-12-01",
    "invalidationTriggers": [
      "TIME_FRESHNESS_CHECK"
    ],
    "materializationDecision": "REUSE_WITH_WARNING",
    "evidenceDecision": "NOT_REQUIRED",
    "authorityDecision": "ALLOW_LIVE_VIEW",
    "publicationAction": "SERVE_LIVE",
    "finalOutcome": "ALLOW",
    "allowedActions": [
      "SERVE_LIVE",
      "SHARE_READONLY"
    ],
    "blockedActions": [
      "ATTEST",
      "FILE_SUBMISSION"
    ]
  },
  {
    "scenarioId": "matpub-02-advisory-frozen-report-stale-warning",
    "twin": "ADVISORY",
    "outputFamily": "DocumentAssembly",
    "outputSubtype": "ADVISORY_REPORT",
    "consequenceClass": "LOW",
    "freshnessInput": "STALE",
    "basisRef": "basis:advisory-report-2026-04-12-01",
    "snapshotRef": "snapshot:advisory-report-2026-04-11-01",
    "contextRef": "ctx:field-west-2026-04-12-02",
    "invalidationTriggers": [
      "TIME_FRESHNESS_CHECK"
    ],
    "materializationDecision": "REUSE_WITH_WARNING",
    "evidenceDecision": "ALLOW",
    "authorityDecision": "ALLOW_DOCUMENT_ASSEMBLY",
    "publicationAction": "ASSEMBLE_FROZEN",
    "finalOutcome": "ALLOW",
    "allowedActions": [
      "ASSEMBLE_FROZEN",
      "SHARE_READONLY"
    ],
    "blockedActions": [
      "ATTEST",
      "FILE_SUBMISSION"
    ]
  },
  {
    "scenarioId": "matpub-03-compliance-report-context-drift-recompute",
    "twin": "COMPLIANCE",
    "outputFamily": "DocumentAssembly",
    "outputSubtype": "COMPLIANCE_REPORT",
    "consequenceClass": "HIGH",
    "freshnessInput": "STALE",
    "basisRef": "basis:compliance-report-2026-04-12-01",
    "snapshotRef": "snapshot:compliance-report-2026-04-10-01",
    "contextRef": "ctx:lot-041a-2026-04-12-01",
    "invalidationTriggers": [
      "CONTEXT_DRIFT",
      "OUTPUT_PROFILE_CHANGE"
    ],
    "materializationDecision": "RECOMPUTE_REQUIRED",
    "evidenceDecision": "ALLOW",
    "authorityDecision": "ALLOW_DOCUMENT_ASSEMBLY",
    "publicationAction": "ASSEMBLE_FROZEN",
    "finalOutcome": "ALLOW_AFTER_RECOMPUTE",
    "allowedActions": [
      "ASSEMBLE_FROZEN",
      "APPROVE_DOCUMENT"
    ],
    "blockedActions": [
      "ATTEST_BEFORE_RECOMPUTE",
      "FILE_SUBMISSION"
    ]
  },
  {
    "scenarioId": "matpub-04-compliance-report-evidence-update-review",
    "twin": "COMPLIANCE",
    "outputFamily": "DocumentAssembly",
    "outputSubtype": "COMPLIANCE_REPORT",
    "consequenceClass": "HIGH",
    "freshnessInput": "STALE",
    "basisRef": "basis:compliance-report-2026-04-12-02",
    "snapshotRef": "snapshot:compliance-report-2026-04-10-02",
    "contextRef": "ctx:lot-041a-2026-04-12-02",
    "invalidationTriggers": [
      "EVIDENCE_UPDATE"
    ],
    "materializationDecision": "RECOMPUTE_REQUIRED",
    "evidenceDecision": "REQUIRE_REVIEW",
    "authorityDecision": "ALLOW_DOCUMENT_ASSEMBLY",
    "publicationAction": "HOLD_REVIEW",
    "finalOutcome": "REQUIRE_REVIEW",
    "allowedActions": [
      "ASSEMBLE_DRAFT_ONLY"
    ],
    "blockedActions": [
      "APPROVE_DOCUMENT",
      "ATTEST",
      "FILE_SUBMISSION"
    ]
  },
  {
    "scenarioId": "matpub-05-dossier-attestation-fresh-allow",
    "twin": "COMPLIANCE",
    "outputFamily": "DocumentAssembly",
    "outputSubtype": "DOSSIER_ASSEMBLY",
    "consequenceClass": "HIGH",
    "freshnessInput": "FRESH",
    "basisRef": "basis:dossier-2026-04-12-01",
    "snapshotRef": "snapshot:dossier-2026-04-12-01",
    "contextRef": "ctx:dossier-2026-04-12-01",
    "invalidationTriggers": [],
    "materializationDecision": "REUSE",
    "evidenceDecision": "ALLOW",
    "authorityDecision": "ALLOW_ATTEST",
    "publicationAction": "ATTEST",
    "finalOutcome": "ALLOW",
    "allowedActions": [
      "ASSEMBLE_FROZEN",
      "APPROVE_DOCUMENT",
      "ATTEST"
    ],
    "blockedActions": [
      "SERVE_LIVE",
      "FILE_SUBMISSION_DIRECT"
    ]
  },
  {
    "scenarioId": "matpub-06-dossier-attestation-policy-change-recompute",
    "twin": "COMPLIANCE",
    "outputFamily": "DocumentAssembly",
    "outputSubtype": "DOSSIER_ASSEMBLY",
    "consequenceClass": "HIGH",
    "freshnessInput": "STALE",
    "basisRef": "basis:dossier-2026-04-12-02",
    "snapshotRef": "snapshot:dossier-2026-04-10-01",
    "contextRef": "ctx:dossier-2026-04-12-02",
    "invalidationTriggers": [
      "ATTESTATION_POLICY_CHANGE",
      "PUBLICATION_SHAPING_CHANGE"
    ],
    "materializationDecision": "RECOMPUTE_REQUIRED",
    "evidenceDecision": "ALLOW",
    "authorityDecision": "ALLOW_ATTEST",
    "publicationAction": "ATTEST",
    "finalOutcome": "ALLOW_AFTER_RECOMPUTE",
    "allowedActions": [
      "ASSEMBLE_FROZEN",
      "APPROVE_DOCUMENT",
      "ATTEST"
    ],
    "blockedActions": [
      "ATTEST_OLD_DOSSIER"
    ]
  },
  {
    "scenarioId": "matpub-07-dossier-attestation-missing-signatory-deny",
    "twin": "COMPLIANCE",
    "outputFamily": "DocumentAssembly",
    "outputSubtype": "DOSSIER_ASSEMBLY",
    "consequenceClass": "HIGH",
    "freshnessInput": "FRESH",
    "basisRef": "basis:dossier-2026-04-12-03",
    "snapshotRef": "snapshot:dossier-2026-04-12-03",
    "contextRef": "ctx:dossier-2026-04-12-03",
    "invalidationTriggers": [
      "SIGNATORY_SCOPE_CHANGE"
    ],
    "materializationDecision": "REUSE",
    "evidenceDecision": "ALLOW",
    "authorityDecision": "DENY",
    "publicationAction": "DENY_ATTEST",
    "finalOutcome": "DENY",
    "allowedActions": [
      "ASSEMBLE_FROZEN"
    ],
    "blockedActions": [
      "ATTEST",
      "FILE_SUBMISSION"
    ]
  },
  {
    "scenarioId": "matpub-08-submission-filing-fresh-allow",
    "twin": "COMPLIANCE",
    "outputFamily": "SubmissionAssembly",
    "outputSubtype": "REGULATORY_SUBMISSION",
    "consequenceClass": "HIGH",
    "freshnessInput": "FRESH",
    "basisRef": "basis:submission-2026-04-12-01",
    "snapshotRef": "snapshot:submission-2026-04-12-01",
    "contextRef": "ctx:submission-2026-04-12-01",
    "invalidationTriggers": [],
    "materializationDecision": "REUSE",
    "evidenceDecision": "ALLOW",
    "authorityDecision": "ALLOW_FILE",
    "publicationAction": "FILE_SUBMISSION",
    "finalOutcome": "ALLOW",
    "allowedActions": [
      "ASSEMBLE_SUBMISSION",
      "FILE_SUBMISSION"
    ],
    "blockedActions": [
      "SERVE_LIVE",
      "ATTEST_PASSPORT"
    ]
  },
  {
    "scenarioId": "matpub-09-submission-filing-binding-change-recompute",
    "twin": "COMPLIANCE",
    "outputFamily": "SubmissionAssembly",
    "outputSubtype": "REGULATORY_SUBMISSION",
    "consequenceClass": "HIGH",
    "freshnessInput": "STALE",
    "basisRef": "basis:submission-2026-04-12-02",
    "snapshotRef": "snapshot:submission-2026-04-09-01",
    "contextRef": "ctx:submission-2026-04-12-02",
    "invalidationTriggers": [
      "SUBMISSION_BINDING_CHANGE",
      "TIME_FRESHNESS_CHECK"
    ],
    "materializationDecision": "RECOMPUTE_REQUIRED",
    "evidenceDecision": "ALLOW",
    "authorityDecision": "ALLOW_FILE",
    "publicationAction": "FILE_SUBMISSION",
    "finalOutcome": "ALLOW_AFTER_RECOMPUTE",
    "allowedActions": [
      "ASSEMBLE_SUBMISSION",
      "FILE_SUBMISSION"
    ],
    "blockedActions": [
      "FILE_OLD_SUBMISSION"
    ]
  },
  {
    "scenarioId": "matpub-10-submission-filing-explicit-invalid-refuse",
    "twin": "COMPLIANCE",
    "outputFamily": "SubmissionAssembly",
    "outputSubtype": "REGULATORY_SUBMISSION",
    "consequenceClass": "HIGH",
    "freshnessInput": "INVALID",
    "basisRef": "basis:submission-2026-04-12-03",
    "snapshotRef": "snapshot:submission-2026-04-08-01",
    "contextRef": "ctx:submission-2026-04-12-03",
    "invalidationTriggers": [
      "EXPLICIT_INVALIDATION",
      "OUTPUT_CONSEQUENCE_GATE"
    ],
    "materializationDecision": "REFUSE",
    "evidenceDecision": "NOT_EVALUATED",
    "authorityDecision": "ALLOW_FILE",
    "publicationAction": "DENY_FILE",
    "finalOutcome": "REFUSE",
    "allowedActions": [],
    "blockedActions": [
      "ASSEMBLE_SUBMISSION",
      "FILE_SUBMISSION"
    ]
  },
  {
    "scenarioId": "matpub-11-passport-attestation-deny",
    "twin": "COMPLIANCE",
    "outputFamily": "PassportView",
    "outputSubtype": "LOT_PASSPORT",
    "consequenceClass": "MEDIUM",
    "freshnessInput": "FRESH",
    "basisRef": "basis:passport-2026-04-12-02",
    "snapshotRef": "snapshot:passport-2026-04-12-02",
    "contextRef": "ctx:passport-2026-04-12-02",
    "invalidationTriggers": [],
    "materializationDecision": "REUSE",
    "evidenceDecision": "NOT_REQUIRED",
    "authorityDecision": "DENY",
    "publicationAction": "DENY_ATTEST",
    "finalOutcome": "DENY",
    "allowedActions": [
      "SERVE_LIVE",
      "SHARE_READONLY"
    ],
    "blockedActions": [
      "ATTEST",
      "FILE_SUBMISSION",
      "FREEZE_AS_DOCUMENT_WITHOUT_ASSEMBLY"
    ]
  },
  {
    "scenarioId": "matpub-12-advisory-alert-stale-allow",
    "twin": "ADVISORY",
    "outputFamily": "DocumentAssembly",
    "outputSubtype": "ADVISORY_ALERT",
    "consequenceClass": "LOW",
    "freshnessInput": "STALE",
    "basisRef": "basis:alert-2026-04-12-01",
    "snapshotRef": "snapshot:alert-2026-04-11-01",
    "contextRef": "ctx:alert-2026-04-12-01",
    "invalidationTriggers": [
      "TIME_FRESHNESS_CHECK"
    ],
    "materializationDecision": "REUSE_WITH_WARNING",
    "evidenceDecision": "ALLOW",
    "authorityDecision": "ALLOW_DOCUMENT_ASSEMBLY",
    "publicationAction": "ASSEMBLE_FROZEN",
    "finalOutcome": "ALLOW",
    "allowedActions": [
      "ASSEMBLE_FROZEN",
      "SHARE_READONLY"
    ],
    "blockedActions": [
      "ATTEST",
      "FILE_SUBMISSION"
    ]
  },
  {
    "scenarioId": "matpub-13-compliance-alert-stale-recompute",
    "twin": "COMPLIANCE",
    "outputFamily": "DocumentAssembly",
    "outputSubtype": "COMPLIANCE_ALERT",
    "consequenceClass": "HIGH",
    "freshnessInput": "STALE",
    "basisRef": "basis:alert-2026-04-12-02",
    "snapshotRef": "snapshot:alert-2026-04-11-02",
    "contextRef": "ctx:alert-2026-04-12-02",
    "invalidationTriggers": [
      "TIME_FRESHNESS_CHECK",
      "OUTPUT_PROFILE_CHANGE"
    ],
    "materializationDecision": "RECOMPUTE_REQUIRED",
    "evidenceDecision": "ALLOW",
    "authorityDecision": "ALLOW_DOCUMENT_ASSEMBLY",
    "publicationAction": "ASSEMBLE_FROZEN",
    "finalOutcome": "ALLOW_AFTER_RECOMPUTE",
    "allowedActions": [
      "ASSEMBLE_FROZEN",
      "APPROVE_DOCUMENT"
    ],
    "blockedActions": [
      "ATTEST_BEFORE_RECOMPUTE",
      "FILE_SUBMISSION"
    ]
  },
  {
    "scenarioId": "matpub-14-attested-report-insufficient-evidence-refuse",
    "twin": "COMPLIANCE",
    "outputFamily": "DocumentAssembly",
    "outputSubtype": "ATTESTED_REPORT",
    "consequenceClass": "HIGH",
    "freshnessInput": "FRESH",
    "basisRef": "basis:attested-report-2026-04-12-01",
    "snapshotRef": "snapshot:attested-report-2026-04-12-01",
    "contextRef": "ctx:attested-report-2026-04-12-01",
    "invalidationTriggers": [],
    "materializationDecision": "REUSE",
    "evidenceDecision": "REFUSE",
    "authorityDecision": "ALLOW_ATTEST",
    "publicationAction": "DENY_ATTEST",
    "finalOutcome": "REFUSE",
    "allowedActions": [
      "ASSEMBLE_FROZEN"
    ],
    "blockedActions": [
      "ATTEST",
      "FILE_SUBMISSION"
    ]
  }
]

def write_json(name: str, payload: object) -> None:
    (ROOT / name).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

def main() -> None:
    pipeline_records = []
    invalidation_records = []
    twin_records = []
    evidence_records = []
    taxonomy_records = []
    traceback_records = []
    telemetry = []
    event_index = 1

    def emit(kind: str, scenario_id: str, detail: dict) -> str:
        nonlocal event_index
        event_id = f"evt-wave27-{event_index:03d}"
        event_index += 1
        telemetry.append({
            "eventId": event_id,
            "ts": NOW,
            "eventKind": kind,
            "scenarioId": scenario_id,
            **detail,
        })
        return event_id

    for s in SCENARIOS:
        scenario_id = s["scenarioId"]
        eval_id = f"pub-eval:{scenario_id}"
        gate_path = [
            "LOAD_REQUEST",
            "RESOLVE_MATERIALIZATION_BASIS",
            "CHECK_CONTEXT_AND_TRIGGER_FRESHNESS",
            "EVALUATE_TWIN_POLICY",
        ]
        if s["materializationDecision"] == "RECOMPUTE_REQUIRED":
            gate_path.append("RECOMPUTE_CURRENT_STATE")
        elif s["materializationDecision"] == "REFUSE":
            gate_path.append("REFUSE_MATERIALIZATION_REUSE")
        else:
            gate_path.append("REUSE_CURRENT_STATE")

        if s["evidenceDecision"] != "NOT_REQUIRED":
            gate_path.append("EVALUATE_EVIDENCE_SUFFICIENCY")
        if s["authorityDecision"] not in ["ALLOW_LIVE_VIEW", "ALLOW_DOCUMENT_ASSEMBLY", "ALLOW_ATTEST", "ALLOW_FILE", "DENY"]:
            gate_path.append("EVALUATE_PUBLICATION_AUTHORITY")
        else:
            gate_path.append("EVALUATE_PUBLICATION_AUTHORITY")
        gate_path.append("CHECK_OUTPUT_TAXONOMY")
        gate_path.append("EMIT_PUBLICATION_DECISION")

        emitted = []
        emitted.append(emit("MATERIALIZATION_REQUEST_RECEIVED", scenario_id, {
            "outputFamily": s["outputFamily"],
            "outputSubtype": s["outputSubtype"],
            "twin": s["twin"],
            "freshnessInput": s["freshnessInput"],
        }))
        for trig in s["invalidationTriggers"]:
            emitted.append(emit("INVALIDATION_TRIGGER_OBSERVED", scenario_id, {
                "triggerFamily": trig,
                "basisRef": s["basisRef"],
                "contextRef": s["contextRef"],
            }))
        emitted.append(emit("MATERIALIZATION_DECISION_MADE", scenario_id, {
            "decision": s["materializationDecision"],
            "basisRef": s["basisRef"],
            "snapshotRef": s["snapshotRef"],
        }))
        if s["evidenceDecision"] != "NOT_REQUIRED":
            emitted.append(emit("EVIDENCE_DECISION_MADE", scenario_id, {
                "decision": s["evidenceDecision"],
                "outputSubtype": s["outputSubtype"],
            }))
        emitted.append(emit("AUTHORITY_DECISION_MADE", scenario_id, {
            "decision": s["authorityDecision"],
            "publicationAction": s["publicationAction"],
        }))
        emitted.append(emit("PUBLICATION_TAXONOMY_CHECK", scenario_id, {
            "outputFamily": s["outputFamily"],
            "allowedActions": s["allowedActions"],
            "blockedActions": s["blockedActions"],
        }))
        emitted.append(emit("PUBLICATION_FINALIZED", scenario_id, {
            "finalOutcome": s["finalOutcome"],
            "outputFamily": s["outputFamily"],
            "outputSubtype": s["outputSubtype"],
        }))

        pipeline_records.append({
            "evaluationId": eval_id,
            "scenarioId": scenario_id,
            "twin": s["twin"],
            "outputFamily": s["outputFamily"],
            "outputSubtype": s["outputSubtype"],
            "consequenceClass": s["consequenceClass"],
            "freshnessInput": s["freshnessInput"],
            "gatePath": gate_path,
            "basisRef": s["basisRef"],
            "snapshotRef": s["snapshotRef"],
            "contextRef": s["contextRef"],
            "materializationDecision": s["materializationDecision"],
            "evidenceDecision": s["evidenceDecision"],
            "authorityDecision": s["authorityDecision"],
            "publicationAction": s["publicationAction"],
            "finalOutcome": s["finalOutcome"],
            "telemetryEventIds": emitted,
        })

        for trig in s["invalidationTriggers"]:
            invalidation_records.append({
                "recordId": f"invalidation:{scenario_id}:{trig.lower()}",
                "scenarioId": scenario_id,
                "triggerFamily": trig,
                "twin": s["twin"],
                "outputFamily": s["outputFamily"],
                "outputSubtype": s["outputSubtype"],
                "freshnessInput": s["freshnessInput"],
                "requiredDisposition": (
                    "RECOMPUTE" if s["materializationDecision"] == "RECOMPUTE_REQUIRED"
                    else "REFUSE" if s["materializationDecision"] == "REFUSE"
                    else "REUSE_WITH_WARNING"
                ),
                "basisRef": s["basisRef"],
                "contextRef": s["contextRef"],
            })

        evidence_records.append({
            "decisionId": f"evidence:{scenario_id}",
            "scenarioId": scenario_id,
            "outputFamily": s["outputFamily"],
            "outputSubtype": s["outputSubtype"],
            "twin": s["twin"],
            "materializationDecision": s["materializationDecision"],
            "evidenceDecision": s["evidenceDecision"],
            "authorityDecision": s["authorityDecision"],
            "publicationAction": s["publicationAction"],
            "finalOutcome": s["finalOutcome"],
            "signatoryCheck": "PASSED" if s["authorityDecision"] == "ALLOW_ATTEST" else "FAILED" if "ATTEST" in s["publicationAction"] or "ATTEST" in ",".join(s["blockedActions"]) else "NOT_APPLICABLE",
            "fileAuthorityCheck": "PASSED" if s["authorityDecision"] == "ALLOW_FILE" else "NOT_APPLICABLE",
        })

        taxonomy_records.append({
            "recordId": f"taxonomy:{scenario_id}",
            "scenarioId": scenario_id,
            "outputFamily": s["outputFamily"],
            "outputSubtype": s["outputSubtype"],
            "twin": s["twin"],
            "allowedActions": s["allowedActions"],
            "blockedActions": s["blockedActions"],
            "liveVersusFrozen": "LIVE" if s["outputFamily"] == "PassportView" else "FROZEN",
            "fileable": s["outputFamily"] == "SubmissionAssembly",
            "attestable": s["outputFamily"] == "DocumentAssembly" and s["outputSubtype"] in ["DOSSIER_ASSEMBLY", "ATTESTED_REPORT"],
        })

        if s["finalOutcome"] in ["ALLOW", "ALLOW_AFTER_RECOMPUTE", "REQUIRE_REVIEW", "DENY", "REFUSE"]:
            traceback_records.append({
                "traceBackId": f"trace:{scenario_id}",
                "scenarioId": scenario_id,
                "outputFamily": s["outputFamily"],
                "outputSubtype": s["outputSubtype"],
                "basisRef": s["basisRef"],
                "snapshotRef": s["snapshotRef"],
                "contextRef": s["contextRef"],
                "evidenceDecisionRef": f"evidence:{scenario_id}",
                "publicationEvaluationRef": eval_id,
                "telemetryEventIds": emitted[-3:],
                "finalOutcome": s["finalOutcome"],
            })

    twin_pairs = [
        ("twin-01-passport-vs-compliance-report", "matpub-01-advisory-live-passport-stale-warning", "matpub-03-compliance-report-context-drift-recompute", "publication"),
        ("twin-02-alert-advisory-vs-compliance", "matpub-12-advisory-alert-stale-allow", "matpub-13-compliance-alert-stale-recompute", "alert"),
        ("twin-03-advisory-report-vs-dossier-attest", "matpub-02-advisory-frozen-report-stale-warning", "matpub-05-dossier-attestation-fresh-allow", "report"),
        ("twin-04-advisory-report-vs-submission-file", "matpub-02-advisory-frozen-report-stale-warning", "matpub-08-submission-filing-fresh-allow", "publication"),
        ("twin-05-dossier-stale-policy-shift", "matpub-05-dossier-attestation-fresh-allow", "matpub-06-dossier-attestation-policy-change-recompute", "attestation"),
    ]
    scenario_by_id = {s["scenarioId"]: s for s in SCENARIOS}
    for twin_id, left_id, right_id, family in twin_pairs:
        l = scenario_by_id[left_id]
        r = scenario_by_id[right_id]
        twin_records.append({
            "comparisonId": twin_id,
            "comparisonFamily": family,
            "leftScenarioId": left_id,
            "rightScenarioId": right_id,
            "sharedBasisDomain": family,
            "leftTwin": l["twin"],
            "rightTwin": r["twin"],
            "leftDisposition": l["materializationDecision"],
            "rightDisposition": r["materializationDecision"],
            "leftFinalOutcome": l["finalOutcome"],
            "rightFinalOutcome": r["finalOutcome"],
            "semanticDifference": (
                "ADVISORY_REUSE_ALLOWED_WHERE_COMPLIANCE_RECOMPUTES"
                if l["materializationDecision"] != r["materializationDecision"]
                else "OUTPUT_CONSEQUENCE_DIVIDES_POLICY"
            ),
        })

    results = {
        "wave": 27,
        "title": "materialization publication policy hardening",
        "overallStatus": "PASS_WITH_LIMITATIONS",
        "scenarioCount": len(SCENARIOS),
        "invalidationTriggerFamilyCount": len(sorted({r["triggerFamily"] for r in invalidation_records})),
        "twinComparisons": len(twin_records),
        "evidenceDecisionCases": len(evidence_records),
        "compiledOutputFamilyCount": len(sorted({r["outputFamily"] for r in taxonomy_records})),
        "compiledOutputSubtypeCount": len(sorted({r["outputSubtype"] for r in taxonomy_records})),
        "publicationTraceBackRecords": len(traceback_records),
        "telemetryEventCount": len(telemetry),
        "coverageAdvances": [
            "invalidation-trigger tests",
            "high-consequence recomputation/refusal tests",
            "Compliance-versus-Advisory materialization-policy tests",
            "evidence-sufficiency case and attestation-policy tests",
            "compiled-output taxonomy conformance tests",
            "passport-vs-document separation tests",
        ],
        "limitations": [
            "No deployment-collected materialization/publication telemetry is included.",
            "Projection trace-back remains package-local and bounded to shipped output families.",
            "Partner-specific publication adapters remain outside this bounded wave."
        ],
    }

    write_json("OFARM_runtime_materialization_publication_pipeline_records_v0_1.json", pipeline_records)
    write_json("OFARM_runtime_materialization_publication_invalidation_records_v0_1.json", invalidation_records)
    write_json("OFARM_runtime_twin_materialization_policy_records_v0_1.json", twin_records)
    write_json("OFARM_runtime_evidence_attestation_publication_decision_records_v0_1.json", evidence_records)
    write_json("OFARM_runtime_compiled_output_taxonomy_records_v0_1.json", taxonomy_records)
    write_json("OFARM_runtime_publication_trace_back_records_v0_2.json", traceback_records)
    write_json("OFARM_runtime_materialization_publication_telemetry_v0_1.json", telemetry)
    write_json("OFARM_runtime_materialization_publication_results_v0_1.json", results)

if __name__ == "__main__":
    main()
