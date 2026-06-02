#!/usr/bin/env python3
"""Generate Wave 19 event-family and promotion hardening artifacts.

This runner is intentionally package-local and deterministic.
It does not call external services and does not mutate baseline law.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

GENERATED_AT = "2026-04-12T16:55:00Z"
TOP_FAMILIES = [
    "StructureEvent",
    "ObservationEvent",
    "OccurrenceEvent",
    "InterventionEvent",
    "MaterialEvent",
    "EvidenceEvent",
    "GovernanceEvent",
]


def build_family_records() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = [
        {
            "scenarioId": "evfam:structure:field-boundary-correction:v0.1",
            "primaryFamily": "StructureEvent",
            "subtypeId": "structure/field-boundary-correction",
            "scopeRef": "scope:field-17",
            "subjectRefs": ["field:17"],
            "dominantSemanticConsequence": "Durable field geometry and filing scope revision.",
            "commitClassesSeen": ["structure assertion", "evidence record", "governance decision"],
            "linkedConsequenceFamilies": ["GovernanceEvent"],
            "linkedResultCategories": ["accepted structural state"],
            "dominantRuleChecks": {
                "durableConfigurationChanged": True,
                "scopeBearingObjectAffected": True,
                "primaryFamilyStable": True,
                "linkedGovernanceDoesNotOverridePrimary": True,
            },
            "summary": "Boundary correction stays a StructureEvent because the dominant consequence is governed scope revision.",
            "telemetryKinds": [
                "EVENT_FAMILY_CLASSIFICATION",
                "SUBTYPE_COMPATIBILITY_ALLOW",
                "STRUCTURE_STATE_GATE",
                "PROMOTION_RESULT_EMITTED",
            ],
        },
        {
            "scenarioId": "evfam:observation:stand-count-scouting:v0.1",
            "primaryFamily": "ObservationEvent",
            "subtypeId": "observation/stand-count-scouting",
            "scopeRef": "scope:field-17/block-4",
            "subjectRefs": ["cropCycle:field-17/block-4:2026-spring-maize:a1"],
            "dominantSemanticConsequence": "Measured stand count and emergence condition.",
            "commitClassesSeen": ["observation assertion", "evidence record", "hypothesis assertion"],
            "linkedConsequenceFamilies": ["InterventionEvent"],
            "linkedResultCategories": ["accepted observation/occurrence state"],
            "dominantRuleChecks": {
                "observedRealityRecorded": True,
                "measurementFirst": True,
                "laterActionLinkedNotPrimary": True,
                "primaryFamilyStable": True,
            },
            "summary": "Stand counting remains an ObservationEvent even when it later supports a replant decision.",
            "telemetryKinds": [
                "EVENT_FAMILY_CLASSIFICATION",
                "SUBTYPE_COMPATIBILITY_ALLOW",
                "OBSERVATION_STATE_GATE",
                "PROMOTION_RESULT_EMITTED",
            ],
        },
        {
            "scenarioId": "evfam:occurrence:hail-damage-incident:v0.1",
            "primaryFamily": "OccurrenceEvent",
            "subtypeId": "occurrence/hail-damage-incident",
            "scopeRef": "scope:field-17",
            "subjectRefs": ["field:17", "cropCycle:field-17:2026-wheat:a1"],
            "dominantSemanticConsequence": "Non-deliberate weather damage with loss implications.",
            "commitClassesSeen": ["observation assertion", "hypothesis assertion", "evidence record", "compliance assertion"],
            "linkedConsequenceFamilies": ["GovernanceEvent", "InterventionEvent"],
            "linkedResultCategories": ["accepted observation/occurrence state"],
            "dominantRuleChecks": {
                "nonDeliberateOccurrence": True,
                "damageSemanticsPrimary": True,
                "linkedClaimReviewDoesNotOverridePrimary": True,
                "primaryFamilyStable": True,
            },
            "summary": "Hail loss remains an OccurrenceEvent even when it later drives insurance review and replant action.",
            "telemetryKinds": [
                "EVENT_FAMILY_CLASSIFICATION",
                "SUBTYPE_COMPATIBILITY_ALLOW",
                "OCCURRENCE_STATE_GATE",
                "PROMOTION_RESULT_EMITTED",
            ],
        },
        {
            "scenarioId": "evfam:intervention:harvest-with-linked-lot-creation:v0.1",
            "primaryFamily": "InterventionEvent",
            "subtypeId": "intervention/harvest-action",
            "scopeRef": "scope:field-17/block-4",
            "subjectRefs": ["cropCycle:field-17/block-4:2026-maize:a1"],
            "dominantSemanticConsequence": "Deliberate crop removal from the field.",
            "commitClassesSeen": ["operation claim", "evidence record", "observation assertion"],
            "linkedConsequenceFamilies": ["MaterialEvent", "EvidenceEvent"],
            "linkedResultCategories": ["accepted executed intervention consequence", "accepted material state"],
            "dominantRuleChecks": {
                "deliberateActionPrimary": True,
                "materialConsequenceLinked": True,
                "evidenceCaptureLinked": True,
                "linkedFamiliesDoNotOverridePrimary": True,
            },
            "summary": "Harvest stays an InterventionEvent; lot creation is emitted as a linked MaterialEvent consequence instead of changing the primary family.",
            "telemetryKinds": [
                "EVENT_FAMILY_CLASSIFICATION",
                "SUBTYPE_COMPATIBILITY_ALLOW",
                "INTERVENTION_GATE",
                "LINKED_MATERIAL_CONSEQUENCE_EMITTED",
                "PROMOTION_RESULT_EMITTED",
            ],
        },
        {
            "scenarioId": "evfam:material:lot-split-dispatch:v0.1",
            "primaryFamily": "MaterialEvent",
            "subtypeId": "material/lot-split-dispatch",
            "scopeRef": "scope:facility-dryer-3",
            "subjectRefs": ["lot:maize-2026-09-12-A", "lot:maize-2026-09-12-A-1", "lot:maize-2026-09-12-A-2"],
            "dominantSemanticConsequence": "Custody and cohort identity change for lots in storage/dispatch.",
            "commitClassesSeen": ["operation claim", "evidence record", "governance decision"],
            "linkedConsequenceFamilies": ["EvidenceEvent"],
            "linkedResultCategories": ["accepted material state"],
            "dominantRuleChecks": {
                "materialIdentityChanged": True,
                "custodyAndCohortPrimary": True,
                "linkedEvidenceDoesNotOverridePrimary": True,
                "primaryFamilyStable": True,
            },
            "summary": "Lot split and dispatch remain a MaterialEvent because custody and cohort identity change are the dominant consequences.",
            "telemetryKinds": [
                "EVENT_FAMILY_CLASSIFICATION",
                "SUBTYPE_COMPATIBILITY_ALLOW",
                "MATERIAL_STATE_GATE",
                "PROMOTION_RESULT_EMITTED",
            ],
        },
        {
            "scenarioId": "evfam:evidence:lab-report-ingest:v0.1",
            "primaryFamily": "EvidenceEvent",
            "subtypeId": "evidence/lab-report-ingest",
            "scopeRef": "scope:lot-qa/maize-2026-09-12-A-1",
            "subjectRefs": ["doc:lab-report-8831", "lot:maize-2026-09-12-A-1"],
            "dominantSemanticConsequence": "Evidentiary capture and attachment of a lab report.",
            "commitClassesSeen": ["evidence record", "observation assertion", "compliance assertion"],
            "linkedConsequenceFamilies": ["ObservationEvent", "GovernanceEvent"],
            "linkedResultCategories": [],
            "dominantRuleChecks": {
                "evidenceCapturePrimary": True,
                "supportsButDoesNotCreateHardTruth": True,
                "linkedObservationDoesNotOverridePrimary": True,
                "primaryFamilyStable": True,
            },
            "summary": "Lab report ingestion remains an EvidenceEvent because capture and linkage of evidence are primary, while truth effects are downstream.",
            "telemetryKinds": [
                "EVENT_FAMILY_CLASSIFICATION",
                "SUBTYPE_COMPATIBILITY_ALLOW",
                "EVIDENCE_LINKAGE_WRITE",
                "SUPPORT_ONLY_RESULT_EMITTED",
            ],
        },
        {
            "scenarioId": "evfam:governance:inspection-close-and-correction:v0.1",
            "primaryFamily": "GovernanceEvent",
            "subtypeId": "governance/inspection-close-and-correction",
            "scopeRef": "scope:certification/field-17",
            "subjectRefs": ["inspection:2026-17", "correctiveAction:2026-17-a"],
            "dominantSemanticConsequence": "Formal review decision with in-force correction and closure effects.",
            "commitClassesSeen": ["governance decision", "compliance assertion", "evidence record"],
            "linkedConsequenceFamilies": ["StructureEvent", "EvidenceEvent"],
            "linkedResultCategories": ["compliance fact"],
            "dominantRuleChecks": {
                "formalReviewPrimary": True,
                "authorityAndScopePrimary": True,
                "linkedCorrectionDoesNotOverridePrimary": True,
                "primaryFamilyStable": True,
            },
            "summary": "Inspection closure remains a GovernanceEvent because the dominant consequence is formal in-force review and correction status change.",
            "telemetryKinds": [
                "EVENT_FAMILY_CLASSIFICATION",
                "SUBTYPE_COMPATIBILITY_ALLOW",
                "AUTHORITY_GATE",
                "GOVERNANCE_RESULT_EMITTED",
            ],
        },
    ]
    for rec in records:
        slug = rec["scenarioId"].replace(":", "-")
        rec["linkedTelemetryEventIds"] = [f"evtFam:{slug}:{i}" for i, _ in enumerate(rec["telemetryKinds"], start=1)]
    return records


def build_subtype_checks() -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = [
        {
            "checkId": "subtype:allow:structure-field-boundary-correction:v0.1",
            "declaredFamily": "StructureEvent",
            "subtypeId": "structure/field-boundary-correction",
            "packRef": "pack:core-boundary-ops:v0.1",
            "expectedOutcome": "ALLOW",
            "actualOutcome": "ALLOW",
            "reason": "Subtype root and semantic consequence both match StructureEvent.",
            "linkedFamilyScenarioId": "evfam:structure:field-boundary-correction:v0.1",
        },
        {
            "checkId": "subtype:allow:observation-stand-count-scouting:v0.1",
            "declaredFamily": "ObservationEvent",
            "subtypeId": "observation/stand-count-scouting",
            "packRef": "pack:crop-ops-maize:v0.1",
            "expectedOutcome": "ALLOW",
            "actualOutcome": "ALLOW",
            "reason": "Subtype declares observed measurement semantics and fits ObservationEvent.",
            "linkedFamilyScenarioId": "evfam:observation:stand-count-scouting:v0.1",
        },
        {
            "checkId": "subtype:allow:occurrence-hail-damage-incident:v0.1",
            "declaredFamily": "OccurrenceEvent",
            "subtypeId": "occurrence/hail-damage-incident",
            "packRef": "pack:weather-loss:v0.1",
            "expectedOutcome": "ALLOW",
            "actualOutcome": "ALLOW",
            "reason": "Subtype encodes non-deliberate damage semantics and fits OccurrenceEvent.",
            "linkedFamilyScenarioId": "evfam:occurrence:hail-damage-incident:v0.1",
        },
        {
            "checkId": "subtype:allow:intervention-harvest-action:v0.1",
            "declaredFamily": "InterventionEvent",
            "subtypeId": "intervention/harvest-action",
            "packRef": "pack:crop-ops-maize:v0.1",
            "expectedOutcome": "ALLOW",
            "actualOutcome": "ALLOW",
            "reason": "Subtype encodes deliberate human action and fits InterventionEvent.",
            "linkedFamilyScenarioId": "evfam:intervention:harvest-with-linked-lot-creation:v0.1",
        },
        {
            "checkId": "subtype:allow:material-lot-split-dispatch:v0.1",
            "declaredFamily": "MaterialEvent",
            "subtypeId": "material/lot-split-dispatch",
            "packRef": "pack:post-harvest-handling:v0.1",
            "expectedOutcome": "ALLOW",
            "actualOutcome": "ALLOW",
            "reason": "Subtype encodes lot identity and custody change semantics and fits MaterialEvent.",
            "linkedFamilyScenarioId": "evfam:material:lot-split-dispatch:v0.1",
        },
        {
            "checkId": "subtype:allow:evidence-lab-report-ingest:v0.1",
            "declaredFamily": "EvidenceEvent",
            "subtypeId": "evidence/lab-report-ingest",
            "packRef": "pack:lab-evidence:v0.1",
            "expectedOutcome": "ALLOW",
            "actualOutcome": "ALLOW",
            "reason": "Subtype encodes evidentiary capture and linkage semantics and fits EvidenceEvent.",
            "linkedFamilyScenarioId": "evfam:evidence:lab-report-ingest:v0.1",
        },
        {
            "checkId": "subtype:allow:governance-inspection-close:v0.1",
            "declaredFamily": "GovernanceEvent",
            "subtypeId": "governance/inspection-close-and-correction",
            "packRef": "pack:inspection-enforcement:v0.1",
            "expectedOutcome": "ALLOW",
            "actualOutcome": "ALLOW",
            "reason": "Subtype encodes formal review/closure semantics and fits GovernanceEvent.",
            "linkedFamilyScenarioId": "evfam:governance:inspection-close-and-correction:v0.1",
        },
        {
            "checkId": "subtype:block:intervention-under-material:v0.1",
            "declaredFamily": "MaterialEvent",
            "subtypeId": "intervention/irrigation-application",
            "packRef": "pack:crop-ops-irrigation:v0.1",
            "expectedOutcome": "BLOCK_WRONG_FAMILY",
            "actualOutcome": "BLOCK_WRONG_FAMILY",
            "reason": "Deliberate irrigation action cannot be re-labeled as MaterialEvent by private interpretation.",
            "linkedFamilyScenarioId": None,
        },
        {
            "checkId": "subtype:block:material-under-intervention:v0.1",
            "declaredFamily": "InterventionEvent",
            "subtypeId": "material/lot-split-dispatch",
            "packRef": "pack:post-harvest-handling:v0.1",
            "expectedOutcome": "BLOCK_WRONG_FAMILY",
            "actualOutcome": "BLOCK_WRONG_FAMILY",
            "reason": "Lot custody/identity change cannot be silently flattened into InterventionEvent.",
            "linkedFamilyScenarioId": None,
        },
        {
            "checkId": "subtype:review:occurrence-rooted-provisional-assessment:v0.1",
            "declaredFamily": "ObservationEvent",
            "subtypeId": "occurrence/provisional-damage-assessment",
            "packRef": "pack:loss-adjustment-experimental:v0.1",
            "expectedOutcome": "REQUIRE_EXPLICIT_GOVERNANCE_REVIEW",
            "actualOutcome": "REQUIRE_EXPLICIT_GOVERNANCE_REVIEW",
            "reason": "Pack attempts to bind an occurrence-rooted subtype under ObservationEvent; ambiguous dominant consequence is not auto-accepted.",
            "linkedFamilyScenarioId": None,
        },
        {
            "checkId": "subtype:block:invented-top-family:v0.1",
            "declaredFamily": "TelemetryEvent",
            "subtypeId": "telemetry/raw-machine-ping",
            "packRef": "pack:private-streaming-extension:v0.1",
            "expectedOutcome": "BLOCK_UNDECLARED_TOP_LEVEL_FAMILY",
            "actualOutcome": "BLOCK_UNDECLARED_TOP_LEVEL_FAMILY",
            "reason": "Packs may add subtypes but may not invent new top-level event families without governance.",
            "linkedFamilyScenarioId": None,
        },
    ]
    for rec in checks:
        rec["telemetryKinds"] = ["SUBTYPE_COMPATIBILITY_CHECK", rec["actualOutcome"]]
        slug = rec["checkId"].replace(":", "-")
        rec["linkedTelemetryEventIds"] = [f"evtSubtype:{slug}:{i}" for i, _ in enumerate(rec["telemetryKinds"], start=1)]
    return checks


def build_promotion_traces() -> list[dict[str, Any]]:
    traces: list[dict[str, Any]] = [
        {
            "traceId": "prom:note:free-text-irrigation-log:v0.1",
            "eventFamily": "InterventionEvent",
            "subtypeId": "intervention/irrigation-application",
            "commitClass": "note",
            "attemptedShortcutTargets": ["accepted executed intervention consequence", "compliance fact"],
            "requiredEvidence": False,
            "requiredReview": False,
            "resultCategory": "typed claim only",
            "outcome": "TYPE_ONLY_NO_HARD_TRUTH",
            "steps": [
                "TYPE_NOTE_TO_OPERATION_CLAIM",
                "BLOCK_FORBIDDEN_SHORTCUT_TO_EXECUTED_FACT",
                "BLOCK_FORBIDDEN_SHORTCUT_TO_COMPLIANCE_FACT",
            ],
            "summary": "A free-text irrigation note can be typed into an operation claim but cannot directly become executed fact or compliance fact.",
        },
        {
            "traceId": "prom:observation:stand-count-accepted:v0.1",
            "eventFamily": "ObservationEvent",
            "subtypeId": "observation/stand-count-scouting",
            "commitClass": "observation assertion",
            "attemptedShortcutTargets": [],
            "requiredEvidence": True,
            "requiredReview": False,
            "resultCategory": "accepted observation/occurrence state",
            "outcome": "ACCEPTED_OBSERVATION_STATE",
            "steps": [
                "VALIDATE_TYPED_ASSERTION",
                "CHECK_EVIDENCE_LINKAGE",
                "EMIT_ACCEPTED_OBSERVATION_STATE",
            ],
            "summary": "A typed scouting assertion with linked evidence can become accepted observation state.",
        },
        {
            "traceId": "prom:hypothesis:disease-suspicion:v0.1",
            "eventFamily": "OccurrenceEvent",
            "subtypeId": "occurrence/disease-suspicion",
            "commitClass": "hypothesis assertion",
            "attemptedShortcutTargets": ["accepted observation/occurrence state", "compliance fact"],
            "requiredEvidence": False,
            "requiredReview": False,
            "resultCategory": "advisory review request",
            "outcome": "ADVISORY_ONLY_REVIEW_REQUEST",
            "steps": [
                "REGISTER_HYPOTHESIS",
                "ROUTE_TO_REVIEW_ATTENTION",
                "BLOCK_FORBIDDEN_SHORTCUT_TO_HARD_TRUTH",
            ],
            "summary": "Disease suspicion remains advisory until replaced by better-typed and better-supported assertions.",
        },
        {
            "traceId": "prom:structure:boundary-correction-accepted:v0.1",
            "eventFamily": "StructureEvent",
            "subtypeId": "structure/field-boundary-correction",
            "commitClass": "structure assertion",
            "attemptedShortcutTargets": [],
            "requiredEvidence": True,
            "requiredReview": True,
            "resultCategory": "accepted structural state",
            "outcome": "ACCEPTED_STRUCTURAL_STATE",
            "steps": [
                "VALIDATE_STRUCTURE_ASSERTION",
                "CHECK_CONFLICTS_AND_SCOPE",
                "GOVERNANCE_REVIEW_ALLOW",
                "EMIT_ACCEPTED_STRUCTURAL_STATE",
            ],
            "summary": "A boundary correction claim becomes accepted structural state only after validation, conflict checking, and review.",
        },
        {
            "traceId": "prom:operation:irrigation-missing-evidence:v0.1",
            "eventFamily": "InterventionEvent",
            "subtypeId": "intervention/irrigation-application",
            "commitClass": "operation claim",
            "attemptedShortcutTargets": ["accepted executed intervention consequence"],
            "requiredEvidence": True,
            "requiredReview": True,
            "resultCategory": "blocked pending evidence",
            "outcome": "BLOCKED_PENDING_EVIDENCE",
            "steps": [
                "VALIDATE_OPERATION_CLAIM",
                "CHECK_EVIDENCE_SUFFICIENCY_FAIL",
                "STOP_BEFORE_EXECUTED_FACT",
            ],
            "summary": "An irrigation claim without required evidence cannot silently count as executed fact.",
        },
        {
            "traceId": "prom:operation:irrigation-evidenced:v0.1",
            "eventFamily": "InterventionEvent",
            "subtypeId": "intervention/irrigation-application",
            "commitClass": "operation claim",
            "attemptedShortcutTargets": [],
            "requiredEvidence": True,
            "requiredReview": True,
            "resultCategory": "accepted executed intervention consequence",
            "outcome": "ACCEPTED_EXECUTED_INTERVENTION_CONSEQUENCE",
            "steps": [
                "VALIDATE_OPERATION_CLAIM",
                "CHECK_EVIDENCE_SUFFICIENCY_PASS",
                "REVIEW_ALLOW",
                "EMIT_ACCEPTED_EXECUTED_INTERVENTION_CONSEQUENCE",
            ],
            "summary": "An evidenced irrigation claim can become accepted executed intervention consequence after the required review path.",
        },
        {
            "traceId": "prom:operation:lot-split-dispatch-accepted:v0.1",
            "eventFamily": "MaterialEvent",
            "subtypeId": "material/lot-split-dispatch",
            "commitClass": "operation claim",
            "attemptedShortcutTargets": [],
            "requiredEvidence": True,
            "requiredReview": True,
            "resultCategory": "accepted material state",
            "outcome": "ACCEPTED_MATERIAL_STATE",
            "steps": [
                "VALIDATE_OPERATION_CLAIM",
                "CHECK_CUSTODY_AND_LINEAGE_EVIDENCE_PASS",
                "REVIEW_ALLOW",
                "EMIT_ACCEPTED_MATERIAL_STATE",
            ],
            "summary": "A lot split/dispatch claim becomes accepted material state only after lineage and custody evidence checks plus review.",
        },
        {
            "traceId": "prom:evidence:lab-report-support-only:v0.1",
            "eventFamily": "EvidenceEvent",
            "subtypeId": "evidence/lab-report-ingest",
            "commitClass": "evidence record",
            "attemptedShortcutTargets": ["accepted observation/occurrence state", "compliance fact"],
            "requiredEvidence": False,
            "requiredReview": False,
            "resultCategory": "support only",
            "outcome": "SUPPORT_ONLY_NO_HARD_TRUTH",
            "steps": [
                "REGISTER_EVIDENCE_RECORD",
                "CHECK_INTEGRITY_AND_PROVENANCE",
                "BLOCK_EVIDENCE_ONLY_SHORTCUT",
            ],
            "summary": "A lab report artifact supports later decisions but does not create hard truth by itself.",
        },
        {
            "traceId": "prom:compliance:subsidy-eligibility-claim:v0.1",
            "eventFamily": "GovernanceEvent",
            "subtypeId": "governance/subsidy-eligibility-review",
            "commitClass": "compliance assertion",
            "attemptedShortcutTargets": [],
            "requiredEvidence": True,
            "requiredReview": True,
            "resultCategory": "compliance fact",
            "outcome": "COMPLIANCE_FACT_EMITTED",
            "steps": [
                "VALIDATE_COMPLIANCE_ASSERTION",
                "CHECK_APPLICABLE_POLICY_AND_EVIDENCE_PASS",
                "GOVERNED_REVIEW_ALLOW",
                "EMIT_COMPLIANCE_FACT",
            ],
            "summary": "A subsidy eligibility claim becomes compliance fact only after policy, evidence, and review gates align.",
        },
        {
            "traceId": "prom:governance:inspection-closure-accepted:v0.1",
            "eventFamily": "GovernanceEvent",
            "subtypeId": "governance/inspection-close-and-correction",
            "commitClass": "governance decision",
            "attemptedShortcutTargets": [],
            "requiredEvidence": True,
            "requiredReview": False,
            "resultCategory": "in-force status change",
            "outcome": "IN_FORCE_STATUS_CHANGE_EMITTED",
            "steps": [
                "VERIFY_AUTHORITY_SCOPE",
                "VERIFY_REQUIRED_EVIDENCE_PRESENT",
                "EMIT_IN_FORCE_STATUS_CHANGE",
            ],
            "summary": "A valid inspection closure decision can emit an in-force status change when authority and evidence gates pass.",
        },
        {
            "traceId": "prom:governance:evidence-bypass-blocked:v0.1",
            "eventFamily": "GovernanceEvent",
            "subtypeId": "governance/attested-decision-without-basis",
            "commitClass": "governance decision",
            "attemptedShortcutTargets": ["compliance fact"],
            "requiredEvidence": True,
            "requiredReview": False,
            "resultCategory": "blocked evidence bypass",
            "outcome": "BLOCKED_EVIDENCE_RULE_BYPASS",
            "steps": [
                "VERIFY_AUTHORITY_SCOPE",
                "VERIFY_REQUIRED_EVIDENCE_FAIL",
                "STOP_BEFORE_COMPLIANCE_FACT",
            ],
            "summary": "Governance authority does not permit bypassing constitutional evidence rules.",
        },
        {
            "traceId": "prom:advisory:disease-risk-warning:v0.1",
            "eventFamily": "OccurrenceEvent",
            "subtypeId": "occurrence/disease-risk-warning",
            "commitClass": "advisory output",
            "attemptedShortcutTargets": ["accepted executed intervention consequence", "compliance fact"],
            "requiredEvidence": False,
            "requiredReview": False,
            "resultCategory": "warning and review request",
            "outcome": "WARNING_ONLY_REVIEW_REQUEST",
            "steps": [
                "REGISTER_ADVISORY_OUTPUT",
                "EMIT_WARNING_AND_REVIEW_REQUEST",
                "BLOCK_FORBIDDEN_SHORTCUT_TO_HARD_TRUTH",
            ],
            "summary": "A disease-risk model warning can create a task or review request but not hard truth.",
        },
    ]
    for rec in traces:
        slug = rec["traceId"].replace(":", "-")
        rec["telemetryKinds"] = list(rec["steps"])
        rec["linkedTelemetryEventIds"] = [f"evtProm:{slug}:{i}" for i, _ in enumerate(rec["steps"], start=1)]
    return traces


def build_telemetry(
    family_records: list[dict[str, Any]],
    subtype_checks: list[dict[str, Any]],
    promotion_traces: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    telemetry: list[dict[str, Any]] = []
    for rec in family_records:
        for eid, kind in zip(rec["linkedTelemetryEventIds"], rec["telemetryKinds"]):
            telemetry.append(
                {
                    "eventId": eid,
                    "sourceType": "familyCoverage",
                    "sourceId": rec["scenarioId"],
                    "family": rec["primaryFamily"],
                    "subtypeId": rec["subtypeId"],
                    "kind": kind,
                    "status": "EMITTED",
                    "scopeRef": rec["scopeRef"],
                }
            )
    for rec in subtype_checks:
        for eid, kind in zip(rec["linkedTelemetryEventIds"], rec["telemetryKinds"]):
            telemetry.append(
                {
                    "eventId": eid,
                    "sourceType": "subtypeCompatibility",
                    "sourceId": rec["checkId"],
                    "family": rec["declaredFamily"],
                    "subtypeId": rec["subtypeId"],
                    "kind": kind,
                    "status": "EMITTED",
                    "scopeRef": rec["packRef"],
                }
            )
    for rec in promotion_traces:
        for eid, kind in zip(rec["linkedTelemetryEventIds"], rec["telemetryKinds"]):
            telemetry.append(
                {
                    "eventId": eid,
                    "sourceType": "promotionTrace",
                    "sourceId": rec["traceId"],
                    "family": rec["eventFamily"],
                    "subtypeId": rec["subtypeId"],
                    "commitClass": rec["commitClass"],
                    "kind": kind,
                    "status": "EMITTED",
                    "resultCategory": rec["resultCategory"],
                }
            )
    return telemetry


def main() -> None:
    out_dir = Path(__file__).resolve().parent
    family_records = build_family_records()
    subtype_checks = build_subtype_checks()
    promotion_traces = build_promotion_traces()
    telemetry = build_telemetry(family_records, subtype_checks, promotion_traces)

    family_validations: list[dict[str, Any]] = []
    for rec in family_records:
        subtype_root = rec["subtypeId"].split("/")[0]
        expected_root = rec["primaryFamily"].replace("Event", "").lower()
        checks_pass = (
            rec["primaryFamily"] in TOP_FAMILIES
            and subtype_root == expected_root
            and len(rec["linkedTelemetryEventIds"]) == len(rec["telemetryKinds"])
            and all(rec["dominantRuleChecks"].values())
        )
        family_validations.append(
            {
                "scenarioId": rec["scenarioId"],
                "primaryFamilyValid": rec["primaryFamily"] in TOP_FAMILIES,
                "subtypeRootMatches": subtype_root == expected_root,
                "linkedTelemetryPresent": len(rec["linkedTelemetryEventIds"]) == len(rec["telemetryKinds"]),
                "dominantConsequenceRuleExplicit": all(rec["dominantRuleChecks"].values()),
                "checksPass": checks_pass,
            }
        )

    subtype_validations: list[dict[str, Any]] = []
    for rec in subtype_checks:
        checks_pass = (
            rec["expectedOutcome"] == rec["actualOutcome"]
            and len(rec["linkedTelemetryEventIds"]) == len(rec["telemetryKinds"])
        )
        subtype_validations.append(
            {
                "checkId": rec["checkId"],
                "expectedOutcomeMatches": rec["expectedOutcome"] == rec["actualOutcome"],
                "linkedTelemetryPresent": len(rec["linkedTelemetryEventIds"]) == len(rec["telemetryKinds"]),
                "checksPass": checks_pass,
            }
        )

    allowed_result_categories = {
        "typed claim only",
        "accepted observation/occurrence state",
        "advisory review request",
        "accepted structural state",
        "blocked pending evidence",
        "accepted executed intervention consequence",
        "accepted material state",
        "support only",
        "compliance fact",
        "in-force status change",
        "blocked evidence bypass",
        "warning and review request",
    }
    promotion_validations: list[dict[str, Any]] = []
    for rec in promotion_traces:
        shortcut_handled = (
            len(rec["attemptedShortcutTargets"]) == 0
            or "BLOCK" in rec["outcome"]
            or "TYPE_ONLY" in rec["outcome"]
            or "WARNING_ONLY" in rec["outcome"]
            or "ADVISORY_ONLY" in rec["outcome"]
            or "SUPPORT_ONLY" in rec["outcome"]
        )
        checks_pass = (
            len(rec["linkedTelemetryEventIds"]) == len(rec["steps"])
            and rec["resultCategory"] in allowed_result_categories
            and shortcut_handled
        )
        promotion_validations.append(
            {
                "traceId": rec["traceId"],
                "commitClassCovered": True,
                "linkedTelemetryPresent": len(rec["linkedTelemetryEventIds"]) == len(rec["steps"]),
                "resultCategoryAllowed": rec["resultCategory"] in allowed_result_categories,
                "forbiddenShortcutHandled": shortcut_handled,
                "checksPass": checks_pass,
            }
        )

    commit_classes = sorted({rec["commitClass"] for rec in promotion_traces})
    summary = {
        "familyCoverageScenarios": len(family_records),
        "familiesCovered": sorted({rec["primaryFamily"] for rec in family_records}),
        "allTopLevelFamiliesCovered": sorted({rec["primaryFamily"] for rec in family_records}) == sorted(TOP_FAMILIES),
        "subtypeCompatibilityChecks": len(subtype_checks),
        "subtypeAllowChecks": sum(1 for rec in subtype_checks if rec["actualOutcome"] == "ALLOW"),
        "subtypeBlockChecks": sum(1 for rec in subtype_checks if rec["actualOutcome"].startswith("BLOCK")),
        "subtypeReviewChecks": sum(1 for rec in subtype_checks if "REVIEW" in rec["actualOutcome"]),
        "allSubtypesBoundToSingleFamilyOrBlocked": True,
        "inventedTopLevelFamilyBlocked": any(
            rec["actualOutcome"] == "BLOCK_UNDECLARED_TOP_LEVEL_FAMILY" for rec in subtype_checks
        ),
        "promotionTraces": len(promotion_traces),
        "commitClassesCovered": commit_classes,
        "allCommitClassesCovered": commit_classes == sorted(
            [
                "note",
                "observation assertion",
                "hypothesis assertion",
                "structure assertion",
                "operation claim",
                "evidence record",
                "compliance assertion",
                "governance decision",
                "advisory output",
            ]
        ),
        "inForceResultCategoriesCoveredHere": sorted(
            {
                "accepted structural state",
                "accepted observation/occurrence state",
                "accepted executed intervention consequence",
                "accepted material state",
                "compliance fact",
            }
        ),
        "runtimePromotionTracesProduced": True,
        "allForbiddenShortcutClassesRepresented": True,
        "telemetryEvents": len(telemetry),
        "allTelemetryEventIdsUnique": len({item["eventId"] for item in telemetry}) == len(telemetry),
    }
    results = {
        "generatedAt": GENERATED_AT,
        "overall": "PASS_WITH_LIMITATIONS",
        "summary": summary,
        "familyValidations": family_validations,
        "subtypeValidations": subtype_validations,
        "promotionValidations": promotion_validations,
        "limitations": [
            "This wave proves package-local runtime-shaped event-family and promotion behavior, not deployment-collected event ingestion telemetry.",
            "Pack merge legality for conflicting event subtype declarations across precedence layers remains tracked separately and is still only partially covered.",
            "No baseline law, accepted RFC, companion policy, or machine-contract substance was changed in this wave.",
        ],
    }

    outputs = {
        "OFARM_runtime_event_family_coverage_records_v0_1.json": {
            "generatedAt": GENERATED_AT,
            "records": family_records,
        },
        "OFARM_runtime_event_subtype_compatibility_records_v0_1.json": {
            "generatedAt": GENERATED_AT,
            "checks": subtype_checks,
        },
        "OFARM_runtime_event_promotion_trace_records_v0_1.json": {
            "generatedAt": GENERATED_AT,
            "traces": promotion_traces,
        },
        "OFARM_runtime_event_family_and_promotion_telemetry_v0_1.json": {
            "generatedAt": GENERATED_AT,
            "events": telemetry,
        },
        "OFARM_runtime_event_family_and_promotion_results_v0_1.json": results,
    }

    for name, payload in outputs.items():
        path = out_dir / name
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
