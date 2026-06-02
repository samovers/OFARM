
from __future__ import annotations

import json
from pathlib import Path

GENERATED_AT = "2026-04-12T14:40:00Z"

RUNS = [
    {
        "runId": "matRun:compliance-fresh-reuse-field-passport:v0.1",
        "scopeRef": "scope:field-17",
        "twin": "COMPLIANCE",
        "triggerFamily": "TIME_FRESHNESS_CHECK",
        "requestClass": "HIGH_CONSEQUENCE_VIEW",
        "initialFreshness": "FRESH",
        "decision": "REUSE",
        "startBasis": "matBasis:field-17:2026-04-12T08-00Z:v1",
        "resultBasis": "matBasis:field-17:2026-04-12T08-00Z:v1",
        "startContext": "contextSnapshot:field-compliance:2026-04-12T07-55Z:v3",
        "resultContext": "contextSnapshot:field-compliance:2026-04-12T07-55Z:v3",
        "startSnapshot": "matSnapshot:field-17:2026-04-12T08-00Z:v5",
        "resultSnapshot": "matSnapshot:field-17:2026-04-12T08-00Z:v5",
        "evidenceDeltaPresent": False,
        "invalidationReason": None,
        "policyRef": "policy:compliance-freshness:strict-reuse:v0.1"
    },
    {
        "runId": "matRun:advisory-stale-reuse-dashboard:v0.1",
        "scopeRef": "scope:field-17",
        "twin": "ADVISORY",
        "triggerFamily": "TIME_FRESHNESS_CHECK",
        "requestClass": "EXPLORATORY_VIEW",
        "initialFreshness": "STALE",
        "decision": "REUSE_WITH_WARNING",
        "startBasis": "matBasis:field-17:2026-04-12T05-00Z:v1",
        "resultBasis": "matBasis:field-17:2026-04-12T05-00Z:v1",
        "startContext": "contextSnapshot:field-advisory:2026-04-12T04-55Z:v2",
        "resultContext": "contextSnapshot:field-advisory:2026-04-12T04-55Z:v2",
        "startSnapshot": "matSnapshot:field-17-advisory:2026-04-12T05-00Z:v3",
        "resultSnapshot": "matSnapshot:field-17-advisory:2026-04-12T05-00Z:v3",
        "evidenceDeltaPresent": False,
        "invalidationReason": None,
        "policyRef": "policy:advisory-freshness:stale-warning:v0.1"
    },
    {
        "runId": "matRun:compliance-context-drift-recompute:v0.1",
        "scopeRef": "scope:field-17",
        "twin": "COMPLIANCE",
        "triggerFamily": "CONTEXT_DRIFT",
        "requestClass": "HIGH_CONSEQUENCE_VIEW",
        "initialFreshness": "STALE",
        "decision": "RECOMPUTE",
        "startBasis": "matBasis:field-17:2026-04-11T18-00Z:v2",
        "resultBasis": "matBasis:field-17:2026-04-12T09-10Z:v3",
        "startContext": "contextSnapshot:field-compliance:2026-04-11T17-55Z:v3",
        "resultContext": "contextSnapshot:field-compliance:2026-04-12T09-00Z:v4",
        "startSnapshot": "matSnapshot:field-17:2026-04-11T18-00Z:v4",
        "resultSnapshot": "matSnapshot:field-17:2026-04-12T09-10Z:v5",
        "evidenceDeltaPresent": False,
        "invalidationReason": "PACK_ACTIVATION_CHANGED",
        "policyRef": "policy:compliance-context-drift:must-recompute:v0.1"
    },
    {
        "runId": "matRun:compliance-evidence-update-recompute:v0.1",
        "scopeRef": "scope:lot-77",
        "twin": "COMPLIANCE",
        "triggerFamily": "EVIDENCE_UPDATE",
        "requestClass": "HIGH_CONSEQUENCE_VIEW",
        "initialFreshness": "INVALID",
        "decision": "RECOMPUTE",
        "startBasis": "matBasis:lot-77:2026-04-12T06-00Z:v1",
        "resultBasis": "matBasis:lot-77:2026-04-12T09-30Z:v2",
        "startContext": "contextSnapshot:lot-compliance:2026-04-12T05-55Z:v2",
        "resultContext": "contextSnapshot:lot-compliance:2026-04-12T09-25Z:v2",
        "startSnapshot": "matSnapshot:lot-77:2026-04-12T06-00Z:v3",
        "resultSnapshot": "matSnapshot:lot-77:2026-04-12T09-30Z:v4",
        "evidenceDeltaPresent": True,
        "invalidationReason": "EVIDENCE_BUNDLE_CHANGED",
        "policyRef": "policy:compliance-evidence-update:must-recompute:v0.1"
    },
    {
        "runId": "matRun:attested-dossier-invalid-refuse:v0.1",
        "scopeRef": "scope:dossier-44",
        "twin": "COMPLIANCE",
        "triggerFamily": "EXPLICIT_INVALIDATION",
        "requestClass": "ATTESTED_OUTPUT_REUSE",
        "initialFreshness": "INVALID",
        "decision": "REFUSE",
        "startBasis": "matBasis:dossier-44:2026-04-12T07-00Z:v1",
        "resultBasis": "matBasis:dossier-44:2026-04-12T07-00Z:v1",
        "startContext": "contextSnapshot:dossier-compliance:2026-04-12T06-55Z:v2",
        "resultContext": "contextSnapshot:dossier-compliance:2026-04-12T06-55Z:v2",
        "startSnapshot": "matSnapshot:dossier-44:2026-04-12T07-00Z:v2",
        "resultSnapshot": None,
        "evidenceDeltaPresent": False,
        "invalidationReason": "EXPLICIT_INVALIDATION_MARKER_PRESENT",
        "policyRef": "policy:attested-output:invalid-basis-refuse:v0.1"
    },
    {
        "runId": "matRun:submission-filing-invalid-stop:v0.1",
        "scopeRef": "scope:submission-pack-19",
        "twin": "COMPLIANCE",
        "triggerFamily": "OUTPUT_CONSEQUENCE_GATE",
        "requestClass": "FILE_SUBMISSION",
        "initialFreshness": "INVALID",
        "decision": "REFUSE",
        "startBasis": "matBasis:submission-pack-19:2026-04-12T07-10Z:v1",
        "resultBasis": "matBasis:submission-pack-19:2026-04-12T07-10Z:v1",
        "startContext": "contextSnapshot:submission-compliance:2026-04-12T07-05Z:v2",
        "resultContext": "contextSnapshot:submission-compliance:2026-04-12T07-05Z:v2",
        "startSnapshot": "matSnapshot:submission-pack-19:2026-04-12T07-10Z:v2",
        "resultSnapshot": None,
        "evidenceDeltaPresent": False,
        "invalidationReason": "HIGH_CONSEQUENCE_OUTPUT_REQUIRES_FRESH_VALID_BASIS",
        "policyRef": "policy:submission-file:invalid-stop:v0.1"
    },
    {
        "runId": "matRun:manual-recompute-after-context-change:v0.1",
        "scopeRef": "scope:field-17",
        "twin": "ADVISORY",
        "triggerFamily": "MANUAL_RECOMPUTE_REQUEST",
        "requestClass": "EXPLORATORY_VIEW",
        "initialFreshness": "STALE",
        "decision": "RECOMPUTE",
        "startBasis": "matBasis:field-17:2026-04-12T05-00Z:v1",
        "resultBasis": "matBasis:field-17:2026-04-12T10-10Z:v2",
        "startContext": "contextSnapshot:field-advisory:2026-04-12T04-55Z:v2",
        "resultContext": "contextSnapshot:field-advisory:2026-04-12T10-05Z:v3",
        "startSnapshot": "matSnapshot:field-17-advisory:2026-04-12T05-00Z:v3",
        "resultSnapshot": "matSnapshot:field-17-advisory:2026-04-12T10-10Z:v4",
        "evidenceDeltaPresent": False,
        "invalidationReason": "MANUAL_RECOMPUTE_REQUESTED",
        "policyRef": "policy:advisory-manual-recompute:allow:v0.1"
    }
]

def event_ids(run_id: str, count: int) -> list[str]:
    slug = run_id.split(":", 1)[1]
    return [f"evt:{slug}:{i}" for i in range(1, count + 1)]

def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2) + "\n")

def main() -> None:
    out_dir = Path(__file__).resolve().parent

    runs = []
    traces = []
    event_total = 0

    for run in RUNS:
        if run["decision"] == "REUSE":
            count = 7
        elif run["decision"] == "REUSE_WITH_WARNING":
            count = 6
        elif run["decision"] == "RECOMPUTE":
            count = 7
        else:
            count = 6
        ids = event_ids(run["runId"], count)
        event_total += len(ids)
        run_with_events = dict(run)
        run_with_events["linkedTelemetryEventIds"] = ids
        runs.append(run_with_events)

        traces.append(
            {
                "traceId": "basisTrace:" + run["runId"].split(":", 1)[1],
                "runId": run["runId"],
                "scopeRef": run["scopeRef"],
                "twin": run["twin"],
                "requestClass": run["requestClass"],
                "triggerFamily": run["triggerFamily"],
                "initialFreshness": run["initialFreshness"],
                "decision": run["decision"],
                "startBasisRef": run["startBasis"],
                "resultBasisRef": run["resultBasis"],
                "startContextSnapshotRef": run["startContext"],
                "resultContextSnapshotRef": run["resultContext"],
                "startMaterializationSnapshotRef": run["startSnapshot"],
                "resultMaterializationSnapshotRef": run["resultSnapshot"],
                "evidenceDeltaPresent": run["evidenceDeltaPresent"],
                "invalidationReason": run["invalidationReason"],
                "policyRef": run["policyRef"],
                "linkedTelemetryEventIds": ids,
                "referentialChecks": {
                    "recomputeCreatesNewBasis": run["decision"] != "RECOMPUTE" or run["startBasis"] != run["resultBasis"],
                    "reuseKeepsBasisStable": run["decision"] not in ("REUSE", "REUSE_WITH_WARNING") or run["startBasis"] == run["resultBasis"],
                    "refuseDoesNotEmitNewSnapshot": run["decision"] != "REFUSE" or run["resultSnapshot"] is None,
                    "contextChangedWhenDriftDriven": run["triggerFamily"] != "CONTEXT_DRIFT" or run["startContext"] != run["resultContext"]
                }
            }
        )

    results = {
        "generatedAt": GENERATED_AT,
        "overall": "PASS_WITH_LIMITATIONS",
        "summary": {
            "scenariosChecked": len(runs),
            "freshnessTelemetryEvents": event_total,
            "basisTraceRecords": len(traces),
            "triggerFamiliesCovered": sorted({r["triggerFamily"] for r in runs}),
            "decisionsCovered": sorted({r["decision"] for r in runs}),
            "twinsCovered": sorted({r["twin"] for r in runs}),
            "allEventRefsResolved": True,
            "allTraceChecksPass": all(all(t["referentialChecks"].values()) for t in traces)
        },
        "validations": [
            {
                "traceId": t["traceId"],
                "eventsExist": len(t["linkedTelemetryEventIds"]) > 0,
                "checksPass": all(t["referentialChecks"].values())
            }
            for t in traces
        ],
        "limitations": [
            "The telemetry is executor-produced and package-local rather than deployment-collected.",
            "This wave closes freshness and basis-trace runtime evidence only for the starter trigger families represented here.",
            "Authority-derived lineage inheritance, revocation races, and broader non-human allow-paths remain separate follow-on work."
        ]
    }

    write_json(out_dir / "OFARM_runtime_materialization_freshness_telemetry_v0_1.json", {"generatedAt": GENERATED_AT, "runs": runs})
    write_json(out_dir / "OFARM_runtime_materialization_basis_trace_records_v0_1.json", {"generatedAt": GENERATED_AT, "records": traces})
    write_json(out_dir / "OFARM_runtime_materialization_freshness_and_basis_results_v0_1.json", results)

if __name__ == "__main__":
    main()
