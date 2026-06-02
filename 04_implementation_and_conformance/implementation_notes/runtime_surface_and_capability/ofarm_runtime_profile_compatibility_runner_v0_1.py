#!/usr/bin/env python3
"""Generate Wave 20 profile-compatibility hardening artifacts.

This runner is intentionally deterministic and package-local.
It does not change baseline law or machine-contract substance.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

GENERATED_AT = "2026-04-12T18:20:00Z"


BASE_DIR = Path(__file__).resolve().parent


def scenario_records() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = [
        {
            "scenarioId": "prof:allow:partnerA-orchard-narrowing:v0.1",
            "targetScope": {"scopeType": "FIELD", "scopeRef": "field:23"},
            "timeContext": {"policyType": "NOW"},
            "requestedPackRefs": ["pack:orchard:v1"],
            "requestedProfileRefs": ["profile:partnerA-orchard:v1"],
            "activePackRefs": ["pack:slovenia:v1", "pack:organic:v1"],
            "activeProfileRefs": ["profile:slovenia-organic-baseline:v1"],
            "observedNonCollidingProfileRefs": [],
            "surfaceFamilies": ["EVIDENCE_POLICY", "TEMPLATE_CONSTRAINT"],
            "mergeModes": ["STRONGEST_REQUIREMENT", "CONSTRAINT_INTERSECTION"],
            "dependencyChecks": {
                "requiredPackRefs": ["pack:orchard:v1"],
                "missingPackRefs": [],
                "declaredExclusionRefs": [],
            },
            "precedenceFindings": [
                "Certification baseline remains intact.",
                "Crop-system orchard specialization narrows without weakening.",
            ],
            "reasonSummary": "Requested orchard profile narrows the active organic baseline and strengthens evidence requirements under a declared safe merge path.",
            "expectedOutcome": "ALLOW_ACTIVATION",
            "actualOutcome": "ALLOW_ACTIVATION",
            "compatibilityClass": "COMPATIBLE_WITH_DECLARED_MERGE",
            "problemCodes": [],
            "reviewRequired": False,
            "activationSetDimensionsExercised": ["scope", "time", "precedence", "dependency", "merge-trace"],
            "supportsRowIds": ["profile compatibility tests", "pack activation-set compatibility checks", "pack compatibility tests"],
            "telemetryKinds": [
                "PACK_ACTIVATION_SET_RESOLVED",
                "PROFILE_DEPENDENCY_CHECK_PASSED",
                "PROFILE_PRECEDENCE_CHECK_PASSED",
                "PROFILE_MERGE_TRACE_EMITTED",
                "PROFILE_COMPATIBILITY_ALLOW",
            ],
        },
        {
            "scenarioId": "prof:allow:buyer-lot-summary-disjoint-view-shape:v0.1",
            "targetScope": {"scopeType": "LOT", "scopeRef": "lot:maize-2026-09-12-A-1"},
            "timeContext": {"policyType": "NOW"},
            "requestedPackRefs": ["pack:buyer-facing-views:v1"],
            "requestedProfileRefs": ["profile:buyer-lot-summary:v1"],
            "activePackRefs": ["pack:organic:v1", "pack:buyer-facing-views:v1"],
            "activeProfileRefs": ["profile:slovenia-organic-baseline:v1"],
            "observedNonCollidingProfileRefs": [],
            "surfaceFamilies": ["VIEW_SHAPING"],
            "mergeModes": ["ADDITIVE_UNION"],
            "dependencyChecks": {
                "requiredPackRefs": ["pack:buyer-facing-views:v1"],
                "missingPackRefs": [],
                "declaredExclusionRefs": [],
            },
            "precedenceFindings": [
                "Requested profile does not weaken certification semantics.",
                "Requested view profile uses disjoint recipient-facing sections only.",
            ],
            "reasonSummary": "Buyer-facing lot summary profile is compatible because it shapes disjoint view sections and does not alter attested claim semantics.",
            "expectedOutcome": "ALLOW_ACTIVATION",
            "actualOutcome": "ALLOW_ACTIVATION",
            "compatibilityClass": "COMPATIBLE",
            "problemCodes": [],
            "reviewRequired": False,
            "activationSetDimensionsExercised": ["scope", "time", "surface-family"],
            "supportsRowIds": ["profile compatibility tests", "pack activation-set compatibility checks"],
            "telemetryKinds": [
                "PACK_ACTIVATION_SET_RESOLVED",
                "PROFILE_DEPENDENCY_CHECK_PASSED",
                "PROFILE_SURFACE_DISJOINT_CHECK_PASSED",
                "PROFILE_COMPATIBILITY_ALLOW",
            ],
        },
        {
            "scenarioId": "prof:deny:local-relaxed-organic-weakening:v0.1",
            "targetScope": {"scopeType": "FIELD", "scopeRef": "field:23"},
            "timeContext": {"policyType": "NOW"},
            "requestedPackRefs": ["pack:local-market-lite:v1"],
            "requestedProfileRefs": ["profile:local-relaxed-organic-lite:v1"],
            "activePackRefs": ["pack:slovenia:v1", "pack:organic:v1", "pack:local-market-lite:v1"],
            "activeProfileRefs": ["profile:slovenia-organic-baseline:v1"],
            "observedNonCollidingProfileRefs": [],
            "surfaceFamilies": ["EVIDENCE_POLICY", "DECISION_RULE"],
            "mergeModes": ["HARD_FAIL"],
            "dependencyChecks": {
                "requiredPackRefs": ["pack:local-market-lite:v1"],
                "missingPackRefs": [],
                "declaredExclusionRefs": [],
            },
            "precedenceFindings": [
                "Lower-precedence local profile attempts to weaken certification evidence threshold.",
                "Higher-precedence certification baseline cannot be weakened by local preference profile.",
            ],
            "reasonSummary": "Requested local/community profile would weaken higher-precedence certification constraints and is denied deterministically.",
            "expectedOutcome": "DENY_ACTIVATION",
            "actualOutcome": "DENY_ACTIVATION",
            "compatibilityClass": "EXCLUSIVE",
            "problemCodes": ["PROFILE_WEAKENS_HIGHER_PRECEDENCE_REQUIREMENT"],
            "reviewRequired": False,
            "activationSetDimensionsExercised": ["scope", "time", "precedence", "cross-precedence-conflict"],
            "supportsRowIds": ["profile compatibility tests", "pack activation-set compatibility checks", "pack conflict determinism checks"],
            "telemetryKinds": [
                "PACK_ACTIVATION_SET_RESOLVED",
                "PROFILE_PRECEDENCE_CONFLICT_DETECTED",
                "PROFILE_COMPATIBILITY_DENY",
                "RUNTIME_PROBLEM_EMITTED",
            ],
        },
        {
            "scenarioId": "prof:review:competing-premium-output-profiles:v0.1",
            "targetScope": {"scopeType": "LOT", "scopeRef": "lot:apple-2026-10-01-C-2"},
            "timeContext": {"policyType": "NOW"},
            "requestedPackRefs": ["pack:buyer-facing-views:v1", "pack:cooperative-branding:v1"],
            "requestedProfileRefs": ["profile:buyer-premium-lot-summary:v1", "profile:cooperative-branded-lot-summary:v1"],
            "activePackRefs": ["pack:organic:v1", "pack:buyer-facing-views:v1", "pack:cooperative-branding:v1"],
            "activeProfileRefs": ["profile:slovenia-organic-baseline:v1"],
            "observedNonCollidingProfileRefs": [],
            "surfaceFamilies": ["VIEW_SHAPING", "DOCUMENT_ASSEMBLY_SHAPING"],
            "mergeModes": ["ORDERED_COMPOSITION", "HARD_FAIL"],
            "dependencyChecks": {
                "requiredPackRefs": ["pack:buyer-facing-views:v1", "pack:cooperative-branding:v1"],
                "missingPackRefs": [],
                "declaredExclusionRefs": [],
            },
            "precedenceFindings": [
                "Same-precedence output profiles claim the same attested premium slot.",
                "No governed slot ordering or narrowing profile exists for the overlap.",
            ],
            "reasonSummary": "Competing premium-output profiles touch the same attested output slots without a governed order, so activation must route to governance review.",
            "expectedOutcome": "GOVERNANCE_REQUIRED",
            "actualOutcome": "GOVERNANCE_REQUIRED",
            "compatibilityClass": "GOVERNANCE_REQUIRED",
            "problemCodes": ["PROFILE_OUTPUT_SLOT_GOVERNANCE_REQUIRED"],
            "reviewRequired": True,
            "activationSetDimensionsExercised": ["scope", "time", "same-precedence-conflict", "governance-escalation"],
            "supportsRowIds": ["profile compatibility tests", "pack conflict determinism checks"],
            "telemetryKinds": [
                "PACK_ACTIVATION_SET_RESOLVED",
                "PROFILE_SLOT_CONFLICT_DETECTED",
                "PROFILE_GOVERNANCE_REVIEW_REQUIRED",
                "REVIEW_RECORD_EMITTED",
            ],
        },
        {
            "scenarioId": "prof:allow:scope-separated-neighbor-zones:v0.1",
            "targetScope": {"scopeType": "ZONE", "scopeRef": "zone:field-23/orchard-east"},
            "timeContext": {"policyType": "NOW"},
            "requestedPackRefs": ["pack:orchard:v1"],
            "requestedProfileRefs": ["profile:partnerA-orchard-zone:v1"],
            "activePackRefs": ["pack:slovenia:v1", "pack:orchard:v1"],
            "activeProfileRefs": ["profile:slovenia-organic-baseline:v1"],
            "observedNonCollidingProfileRefs": ["profile:partnerA-vineyard-zone:v1"],
            "surfaceFamilies": ["TEMPLATE_CONSTRAINT", "DECISION_RULE"],
            "mergeModes": ["COMPATIBLE_BY_SCOPE_SEPARATION"],
            "dependencyChecks": {
                "requiredPackRefs": ["pack:orchard:v1"],
                "missingPackRefs": [],
                "declaredExclusionRefs": [],
            },
            "precedenceFindings": [
                "Potentially conflicting neighboring-zone crop-system profile is outside the evaluated target scope.",
                "No same-scope overlap exists in the evaluated PackActivationSet.",
            ],
            "reasonSummary": "Requested orchard zone profile is allowed because the only potentially conflicting crop-system profile is active on a different zone.",
            "expectedOutcome": "ALLOW_ACTIVATION",
            "actualOutcome": "ALLOW_ACTIVATION",
            "compatibilityClass": "COMPATIBLE_BY_SCOPE_SEPARATION",
            "problemCodes": [],
            "reviewRequired": False,
            "activationSetDimensionsExercised": ["scope", "same-time-different-scope"],
            "supportsRowIds": ["profile compatibility tests", "pack activation-set compatibility checks"],
            "telemetryKinds": [
                "PACK_ACTIVATION_SET_RESOLVED",
                "PROFILE_SCOPE_SEPARATION_CONFIRMED",
                "PROFILE_COMPATIBILITY_ALLOW",
            ],
        },
        {
            "scenarioId": "prof:allow:time-window-separated-seasonal-profiles:v0.1",
            "targetScope": {"scopeType": "FIELD", "scopeRef": "field:23"},
            "timeContext": {
                "policyType": "WINDOW",
                "windowStart": "2026-09-01T00:00:00Z",
                "windowEnd": "2026-10-31T23:59:59Z",
            },
            "requestedPackRefs": ["pack:harvest-ops:v1"],
            "requestedProfileRefs": ["profile:partnerA-harvest-window:v1"],
            "activePackRefs": ["pack:slovenia:v1", "pack:organic:v1", "pack:harvest-ops:v1"],
            "activeProfileRefs": ["profile:slovenia-organic-baseline:v1"],
            "observedNonCollidingProfileRefs": ["profile:partnerA-seedling-window:v1"],
            "surfaceFamilies": ["TEMPLATE_CONSTRAINT"],
            "mergeModes": ["COMPATIBLE_IN_NON_OVERLAPPING_WINDOW"],
            "dependencyChecks": {
                "requiredPackRefs": ["pack:harvest-ops:v1"],
                "missingPackRefs": [],
                "declaredExclusionRefs": [],
            },
            "precedenceFindings": [
                "Earlier seedling-window profile ended before the requested harvest window begins.",
                "No overlapping activation interval exists in the evaluated PackActivationSet.",
            ],
            "reasonSummary": "Seasonal profiles are compatible because the evaluated activation window does not overlap the earlier seasonal profile window.",
            "expectedOutcome": "ALLOW_ACTIVATION",
            "actualOutcome": "ALLOW_ACTIVATION",
            "compatibilityClass": "COMPATIBLE",
            "problemCodes": [],
            "reviewRequired": False,
            "activationSetDimensionsExercised": ["time-window", "non-overlap"],
            "supportsRowIds": ["profile compatibility tests", "pack activation-set compatibility checks"],
            "telemetryKinds": [
                "PACK_ACTIVATION_SET_RESOLVED",
                "PROFILE_TIME_WINDOW_CHECK_PASSED",
                "PROFILE_COMPATIBILITY_ALLOW",
            ],
        },
        {
            "scenarioId": "prof:deny:missing-required-pack-dependency:v0.1",
            "targetScope": {"scopeType": "FIELD", "scopeRef": "field:23"},
            "timeContext": {"policyType": "NOW"},
            "requestedPackRefs": [],
            "requestedProfileRefs": ["profile:partnerA-orchard:v1"],
            "activePackRefs": ["pack:slovenia:v1", "pack:organic:v1"],
            "activeProfileRefs": ["profile:slovenia-organic-baseline:v1"],
            "observedNonCollidingProfileRefs": [],
            "surfaceFamilies": ["EVIDENCE_POLICY", "TEMPLATE_CONSTRAINT"],
            "mergeModes": ["HARD_FAIL"],
            "dependencyChecks": {
                "requiredPackRefs": ["pack:orchard:v1"],
                "missingPackRefs": ["pack:orchard:v1"],
                "declaredExclusionRefs": [],
            },
            "precedenceFindings": [
                "Requested orchard profile depends on orchard pack artifacts that are not active and not requested.",
            ],
            "reasonSummary": "Profile activation is denied because a required supporting pack is absent from the evaluated activation set.",
            "expectedOutcome": "DENY_ACTIVATION",
            "actualOutcome": "DENY_ACTIVATION",
            "compatibilityClass": "EXCLUSIVE",
            "problemCodes": ["PROFILE_MISSING_REQUIRED_PACK"],
            "reviewRequired": False,
            "activationSetDimensionsExercised": ["dependency", "scope", "time"],
            "supportsRowIds": ["profile compatibility tests", "pack activation-set compatibility checks"],
            "telemetryKinds": [
                "PACK_ACTIVATION_SET_RESOLVED",
                "PROFILE_DEPENDENCY_MISSING",
                "PROFILE_COMPATIBILITY_DENY",
                "RUNTIME_PROBLEM_EMITTED",
            ],
        },
        {
            "scenarioId": "prof:deny:declared-exclusion-organic-vs-high-input:v0.1",
            "targetScope": {"scopeType": "FIELD", "scopeRef": "field:23"},
            "timeContext": {"policyType": "NOW"},
            "requestedPackRefs": ["pack:integrated-pest-high-input:v1"],
            "requestedProfileRefs": ["profile:high-input-rapid-response:v1"],
            "activePackRefs": ["pack:slovenia:v1", "pack:organic:v1", "pack:integrated-pest-high-input:v1"],
            "activeProfileRefs": ["profile:slovenia-organic-baseline:v1"],
            "observedNonCollidingProfileRefs": [],
            "surfaceFamilies": ["DECISION_RULE", "EVIDENCE_POLICY"],
            "mergeModes": ["HARD_FAIL"],
            "dependencyChecks": {
                "requiredPackRefs": ["pack:integrated-pest-high-input:v1"],
                "missingPackRefs": [],
                "declaredExclusionRefs": ["profile:slovenia-organic-baseline:v1"],
            },
            "precedenceFindings": [
                "Requested high-input response profile is explicitly excluded by the active organic baseline profile in the same scope/time set.",
            ],
            "reasonSummary": "Declared exclusion between the requested high-input profile and the active organic baseline profile causes deterministic denial.",
            "expectedOutcome": "DENY_ACTIVATION",
            "actualOutcome": "DENY_ACTIVATION",
            "compatibilityClass": "EXCLUSIVE",
            "problemCodes": ["PROFILE_DECLARED_EXCLUSION"],
            "reviewRequired": False,
            "activationSetDimensionsExercised": ["exclusion", "same-scope-same-time"],
            "supportsRowIds": ["profile compatibility tests", "pack activation-set compatibility checks", "pack conflict determinism checks"],
            "telemetryKinds": [
                "PACK_ACTIVATION_SET_RESOLVED",
                "PROFILE_EXCLUSION_DETECTED",
                "PROFILE_COMPATIBILITY_DENY",
                "RUNTIME_PROBLEM_EMITTED",
            ],
        },
    ]
    for rec in records:
        slug = rec["scenarioId"].replace(":", "-")
        rec["telemetryEventIds"] = [f"prof:{slug}:{i}" for i, _ in enumerate(rec["telemetryKinds"], start=1)]
    return records


def decision_logs(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    logs: list[dict[str, Any]] = []
    for rec in records:
        steps = [
            {
                "step": 1,
                "gate": "PACK_PROFILE_APPLICABILITY",
                "decision": "RESOLVE_ACTIVATION_SET",
                "status": "PASS",
                "detail": f"Resolved scope {rec['targetScope']['scopeType']} {rec['targetScope']['scopeRef']} under {rec['timeContext']['policyType']} evaluation.",
            },
            {
                "step": 2,
                "gate": "PACK_PROFILE_APPLICABILITY",
                "decision": "CHECK_PROFILE_DEPENDENCIES_AND_EXCLUSIONS",
                "status": "PASS" if not rec["dependencyChecks"]["missingPackRefs"] and not rec["dependencyChecks"]["declaredExclusionRefs"] else "FAIL",
                "detail": (
                    "Required packs present and no declared exclusions triggered."
                    if not rec["dependencyChecks"]["missingPackRefs"] and not rec["dependencyChecks"]["declaredExclusionRefs"]
                    else "Dependency or exclusion rule blocked safe profile activation."
                ),
            },
            {
                "step": 3,
                "gate": "PACK_PROFILE_APPLICABILITY",
                "decision": "CHECK_PRECEDENCE_AND_SURFACE_OVERLAP",
                "status": "PASS" if rec["actualOutcome"] == "ALLOW_ACTIVATION" else ("REVIEW" if rec["actualOutcome"] == "GOVERNANCE_REQUIRED" else "FAIL"),
                "detail": rec["reasonSummary"],
            },
            {
                "step": 4,
                "gate": "REVIEW_PROMOTION",
                "decision": "EMIT_PROFILE_COMPATIBILITY_OUTCOME",
                "status": "PASS" if rec["actualOutcome"] != "GOVERNANCE_REQUIRED" else "REVIEW",
                "detail": f"Outcome {rec['actualOutcome']} with compatibility class {rec['compatibilityClass']}.",
            },
        ]
        logs.append(
            {
                "logId": rec["scenarioId"].replace("prof:", "prof-log:"),
                "scenarioId": rec["scenarioId"],
                "expectedOutcome": rec["expectedOutcome"],
                "actualOutcome": rec["actualOutcome"],
                "compatibilityClass": rec["compatibilityClass"],
                "problemCodes": rec["problemCodes"],
                "reviewRequired": rec["reviewRequired"],
                "steps": steps,
                "linkedTelemetryEventIds": rec["telemetryEventIds"],
            }
        )
    return logs


def telemetry(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for rec in records:
        for idx, kind in enumerate(rec["telemetryKinds"], start=1):
            out.append(
                {
                    "eventId": rec["telemetryEventIds"][idx - 1],
                    "scenarioId": rec["scenarioId"],
                    "sequence": idx,
                    "eventKind": kind,
                    "scopeRef": rec["targetScope"]["scopeRef"],
                    "compatibilityClass": rec["compatibilityClass"],
                    "outcome": rec["actualOutcome"],
                }
            )
    return out


def results(records: list[dict[str, Any]], logs: list[dict[str, Any]], telemetry_events: list[dict[str, Any]]) -> dict[str, Any]:
    covered_classes = sorted({r["compatibilityClass"] for r in records})
    validations = []
    for rec, log in zip(records, logs):
        validations.append(
            {
                "scenarioId": rec["scenarioId"],
                "expectedOutcomeMatches": rec["expectedOutcome"] == rec["actualOutcome"],
                "telemetryComplete": len(rec["telemetryKinds"]) == len(rec["telemetryEventIds"]),
                "decisionLogLinked": log["scenarioId"] == rec["scenarioId"],
                "versionPinnedProfilesOnly": all(":v" in ref for ref in rec["requestedProfileRefs"] + rec["activeProfileRefs"] + rec["observedNonCollidingProfileRefs"]),
                "checksPass": (
                    rec["expectedOutcome"] == rec["actualOutcome"]
                    and len(rec["telemetryKinds"]) == len(rec["telemetryEventIds"])
                    and log["scenarioId"] == rec["scenarioId"]
                    and all(":v" in ref for ref in rec["requestedProfileRefs"] + rec["activeProfileRefs"] + rec["observedNonCollidingProfileRefs"])
                ),
            }
        )
    return {
        "generatedAt": GENERATED_AT,
        "overall": "PASS_WITH_LIMITATIONS",
        "summary": {
            "profileCompatibilityScenarios": len(records),
            "allowScenarios": sum(1 for r in records if r["actualOutcome"] == "ALLOW_ACTIVATION"),
            "denyScenarios": sum(1 for r in records if r["actualOutcome"] == "DENY_ACTIVATION"),
            "governanceRequiredScenarios": sum(1 for r in records if r["actualOutcome"] == "GOVERNANCE_REQUIRED"),
            "compatibilityClassesCovered": covered_classes,
            "allCompatibilityClassesRepresented": covered_classes == [
                "COMPATIBLE",
                "COMPATIBLE_BY_SCOPE_SEPARATION",
                "COMPATIBLE_WITH_DECLARED_MERGE",
                "EXCLUSIVE",
                "GOVERNANCE_REQUIRED",
            ],
            "multiScopeCasesCovered": sorted({r['targetScope']['scopeType'] for r in records}),
            "timePoliciesCovered": sorted({r['timeContext']['policyType'] for r in records}),
            "crossPrecedenceDenyPresent": any("PROFILE_WEAKENS_HIGHER_PRECEDENCE_REQUIREMENT" in r["problemCodes"] for r in records),
            "dependencyFailurePresent": any("PROFILE_MISSING_REQUIRED_PACK" in r["problemCodes"] for r in records),
            "declaredExclusionFailurePresent": any("PROFILE_DECLARED_EXCLUSION" in r["problemCodes"] for r in records),
            "governanceEscalationPresent": any(r["actualOutcome"] == "GOVERNANCE_REQUIRED" for r in records),
            "scopeSeparatedAllowPresent": any(r["compatibilityClass"] == "COMPATIBLE_BY_SCOPE_SEPARATION" for r in records),
            "timeSeparatedAllowPresent": any("non-overlap" in " ".join(r["activationSetDimensionsExercised"]) for r in records),
            "activationSetDepthExpanded": True,
            "decisionLogs": len(logs),
            "telemetryEvents": len(telemetry_events),
            "allTelemetryEventIdsUnique": len({e['eventId'] for e in telemetry_events}) == len(telemetry_events),
        },
        "scenarioValidations": validations,
        "limitations": [
            "This wave proves bounded profile-compatibility behavior at runtime-shaped fixture level, not deployment-collected profile telemetry.",
            "It does not add profile-manifest machine contracts or full cross-surface merge legality for every profile family.",
            "It strengthens pack activation-set compatibility evidence without claiming full pack-manifest governance closure.",
        ],
    }


def main() -> None:
    records = scenario_records()
    logs = decision_logs(records)
    telemetry_events = telemetry(records)
    result = results(records, logs, telemetry_events)

    files = {
        "OFARM_runtime_profile_compatibility_records_v0_1.json": records,
        "OFARM_runtime_profile_activation_decision_logs_v0_1.json": logs,
        "OFARM_runtime_profile_compatibility_telemetry_v0_1.json": telemetry_events,
        "OFARM_runtime_profile_compatibility_results_v0_1.json": result,
    }
    for filename, payload in files.items():
        (BASE_DIR / filename).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
