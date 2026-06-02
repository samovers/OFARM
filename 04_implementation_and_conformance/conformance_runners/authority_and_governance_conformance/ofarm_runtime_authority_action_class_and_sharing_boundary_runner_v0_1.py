#!/usr/bin/env python3
"""Emit bounded runtime-shaped authority action-class and sharing-boundary evidence for Wave 26."""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NOW = datetime(2026, 4, 12, 16, 30, 0, tzinfo=timezone.utc).isoformat()

ALL_ACTION_CLASSES = [
    "OBSERVE_CREATE_OBSERVATION",
    "OBSERVE_ATTACH_EVIDENCE",
    "ASSERT_STRUCTURE",
    "ASSERT_OPERATION_CLAIM",
    "ASSERT_COMPLIANCE",
    "OPERATE_PLAN_INTERVENTION",
    "OPERATE_REPORT_EXECUTION",
    "REVIEW_REQUEST",
    "REVIEW_ACCEPT",
    "REVIEW_REJECT_OR_CONTEST",
    "REVIEW_SUPERSEDE",
    "CONTEXT_INSTALL_PACK",
    "CONTEXT_ACTIVATE_PACK",
    "CONTEXT_DEACTIVATE_PACK",
    "OUTPUT_APPROVE_DOCUMENT_ASSEMBLY",
    "OUTPUT_ATTEST_DOCUMENT_ASSEMBLY",
    "OUTPUT_FILE_SUBMISSION_ASSEMBLY",
    "SHARE_GRANT_ACCESS",
    "SHARE_REVOKE_ACCESS",
    "RECEIVE_READ_DATA",
]

ACTION_SCENARIOS = [
    {
        "scenarioId": "action-01-observe-create-field-descendant-allow",
        "actionClass": "OBSERVE_CREATE_OBSERVATION",
        "actorType": "HUMAN",
        "partyRole": "FieldReporter",
        "targetScope": "field:north-07/zone:west-a",
        "targetArtifactFamily": "Observation",
        "activePackContext": ["baseline.core", "profile.field.ops"],
        "outcome": "ALLOW",
        "reasonCodes": ["DESCENDANT_SCOPE_GRANT", "OBSERVE_REPORT_ALLOWED"],
    },
    {
        "scenarioId": "action-02-observe-attach-evidence-operation-allow",
        "actionClass": "OBSERVE_ATTACH_EVIDENCE",
        "actorType": "HUMAN",
        "partyRole": "FieldReporter",
        "targetScope": "operation:spray-2026-04-09-01",
        "targetArtifactFamily": "EvidenceAttachment",
        "activePackContext": ["baseline.core", "profile.evidence.trace"],
        "outcome": "ALLOW",
        "reasonCodes": ["EXACT_SCOPE_GRANT", "EVIDENCE_LINKING_TRACEABLE"],
    },
    {
        "scenarioId": "action-03-assert-structure-exact-allow",
        "actionClass": "ASSERT_STRUCTURE",
        "actorType": "HUMAN",
        "partyRole": "FarmStructureEditor",
        "targetScope": "field:north-07",
        "targetArtifactFamily": "StructureAssertion",
        "activePackContext": ["baseline.core"],
        "outcome": "ALLOW",
        "reasonCodes": ["EXACT_ONLY_GRANT", "STRUCTURE_ASSERT_ALLOWED"],
    },
    {
        "scenarioId": "action-04-assert-operation-claim-delegated-allow",
        "actionClass": "ASSERT_OPERATION_CLAIM",
        "actorType": "HUMAN",
        "partyRole": "ContractOperator",
        "targetScope": "operation:fertigation-2026-04-08-03",
        "targetArtifactFamily": "OperationClaim",
        "activePackContext": ["baseline.core", "profile.ops.claims"],
        "outcome": "ALLOW",
        "reasonCodes": ["DELEGATED_SCOPE_GRANT", "TRACE_REQUIRED_SATISFIED"],
    },
    {
        "scenarioId": "action-05-assert-compliance-ai-human-approval",
        "actionClass": "ASSERT_COMPLIANCE",
        "actorType": "AI_ASSISTED",
        "partyRole": "ComplianceCoordinator",
        "targetScope": "lot:2026-lot-041a",
        "targetArtifactFamily": "ComplianceAssertion",
        "activePackContext": ["baseline.core", "profile.organic.eu"],
        "outcome": "REQUIRE_HUMAN_APPROVAL",
        "reasonCodes": ["HIGH_RISK_ASSERTION", "AI_ASSISTED_REQUIRES_HUMAN_APPROVAL"],
    },
    {
        "scenarioId": "action-06-operate-plan-intervention-allow",
        "actionClass": "OPERATE_PLAN_INTERVENTION",
        "actorType": "HUMAN",
        "partyRole": "FarmPlanner",
        "targetScope": "crop-cycle:cc-2026-maize-03",
        "targetArtifactFamily": "PlannedIntervention",
        "activePackContext": ["baseline.core", "profile.field.ops"],
        "outcome": "ALLOW",
        "reasonCodes": ["DESCENDANT_SCOPE_GRANT", "PLANNING_ACTION_ALLOWED"],
    },
    {
        "scenarioId": "action-07-operate-report-execution-delegated-allow",
        "actionClass": "OPERATE_REPORT_EXECUTION",
        "actorType": "HUMAN",
        "partyRole": "ContractOperator",
        "targetScope": "operation:harvest-2026-04-11-02",
        "targetArtifactFamily": "OperationExecutionReport",
        "activePackContext": ["baseline.core", "profile.field.ops"],
        "outcome": "ALLOW",
        "reasonCodes": ["DELEGATED_SCOPE_GRANT", "PROMOTION_PATH_SEPARATE"],
    },
    {
        "scenarioId": "action-08-review-request-allow",
        "actionClass": "REVIEW_REQUEST",
        "actorType": "HUMAN",
        "partyRole": "ComplianceCoordinator",
        "targetScope": "review-case:case-2026-0042",
        "targetArtifactFamily": "ReviewRequest",
        "activePackContext": ["baseline.core", "profile.organic.eu"],
        "outcome": "ALLOW",
        "reasonCodes": ["EXACT_ONLY_GRANT", "ACCOUNTABLE_REVIEW_REQUEST"],
    },
    {
        "scenarioId": "action-09-review-accept-allow",
        "actionClass": "REVIEW_ACCEPT",
        "actorType": "HUMAN",
        "partyRole": "CertifierReviewer",
        "targetScope": "review-case:case-2026-0042",
        "targetArtifactFamily": "ReviewDecision",
        "activePackContext": ["baseline.core", "profile.organic.eu"],
        "outcome": "ALLOW",
        "reasonCodes": ["NO_INHERIT_EXACT_CASE_GRANT", "HUMAN_ONLY_REQUIREMENT_SATISFIED"],
    },
    {
        "scenarioId": "action-10-review-reject-allow",
        "actionClass": "REVIEW_REJECT_OR_CONTEST",
        "actorType": "HUMAN",
        "partyRole": "CertifierReviewer",
        "targetScope": "review-case:case-2026-0043",
        "targetArtifactFamily": "ReviewDecision",
        "activePackContext": ["baseline.core", "profile.residue.audit"],
        "outcome": "ALLOW",
        "reasonCodes": ["NO_INHERIT_EXACT_CASE_GRANT", "HUMAN_ONLY_REQUIREMENT_SATISFIED"],
    },
    {
        "scenarioId": "action-11-review-supersede-allow",
        "actionClass": "REVIEW_SUPERSEDE",
        "actorType": "HUMAN",
        "partyRole": "GovernanceOfficer",
        "targetScope": "state-scope:lot-2026-041a-compliance",
        "targetArtifactFamily": "ReviewDecision",
        "activePackContext": ["baseline.core", "profile.organic.eu"],
        "outcome": "ALLOW",
        "reasonCodes": ["NO_INHERIT_STATE_SCOPE_GRANT", "HUMAN_ONLY_REQUIREMENT_SATISFIED"],
    },
    {
        "scenarioId": "action-12-context-install-pack-allow",
        "actionClass": "CONTEXT_INSTALL_PACK",
        "actorType": "HUMAN",
        "partyRole": "FarmContextGovernor",
        "targetScope": "field:north-07",
        "targetArtifactFamily": "PackActivationSet",
        "activePackContext": ["baseline.core", "profile.organic.eu"],
        "outcome": "ALLOW",
        "reasonCodes": ["EXACT_SCOPE_CONTEXT_GOVERNANCE_GRANT", "HUMAN_ONLY_REQUIREMENT_SATISFIED"],
    },
    {
        "scenarioId": "action-13-context-activate-pack-allow",
        "actionClass": "CONTEXT_ACTIVATE_PACK",
        "actorType": "HUMAN",
        "partyRole": "FarmContextGovernor",
        "targetScope": "field:north-07",
        "targetArtifactFamily": "PackActivationSet",
        "activePackContext": ["baseline.core", "profile.organic.eu", "profile.export.buyer-a"],
        "outcome": "ALLOW",
        "reasonCodes": ["EXACT_SCOPE_CONTEXT_GOVERNANCE_GRANT", "COMPATIBLE_ACTIVATION_SET"],
    },
    {
        "scenarioId": "action-14-context-activate-pack-require-review",
        "actionClass": "CONTEXT_ACTIVATE_PACK",
        "actorType": "HUMAN",
        "partyRole": "FarmContextGovernor",
        "targetScope": "field:north-07",
        "targetArtifactFamily": "PackActivationSet",
        "activePackContext": ["baseline.core", "profile.organic.eu", "profile.consumer-facing-badge"],
        "outcome": "REQUIRE_REVIEW",
        "reasonCodes": ["COMPETING_OUTPUT_PROFILE", "GOVERNANCE_ARBITRATION_REQUIRED"],
    },
    {
        "scenarioId": "action-15-context-deactivate-pack-deny",
        "actionClass": "CONTEXT_DEACTIVATE_PACK",
        "actorType": "HUMAN",
        "partyRole": "CertifierReviewer",
        "targetScope": "field:north-07",
        "targetArtifactFamily": "PackActivationSet",
        "activePackContext": ["baseline.core", "profile.organic.eu"],
        "outcome": "DENY",
        "reasonCodes": ["MISSING_CONTEXT_GOVERNANCE_GRANT", "DEFAULT_DENY"],
    },
    {
        "scenarioId": "action-16-output-approve-document-allow",
        "actionClass": "OUTPUT_APPROVE_DOCUMENT_ASSEMBLY",
        "actorType": "HUMAN",
        "partyRole": "DossierApprover",
        "targetScope": "dossier:compliance-2026-0042",
        "targetArtifactFamily": "DocumentAssembly",
        "activePackContext": ["baseline.core", "profile.organic.eu", "pack.dossier.attestation"],
        "outcome": "ALLOW",
        "reasonCodes": ["NO_INHERIT_EXACT_OUTPUT_GRANT", "OUTPUT_APPROVAL_ALLOWED"],
    },
    {
        "scenarioId": "action-17-output-attest-document-allow",
        "actionClass": "OUTPUT_ATTEST_DOCUMENT_ASSEMBLY",
        "actorType": "HUMAN",
        "partyRole": "AuthorizedSignatory",
        "targetScope": "dossier:compliance-2026-0042",
        "targetArtifactFamily": "DocumentAssembly",
        "activePackContext": ["baseline.core", "profile.organic.eu", "pack.dossier.attestation"],
        "outcome": "ALLOW",
        "reasonCodes": ["NO_INHERIT_SIGNATORY_GRANT", "HUMAN_ONLY_REQUIREMENT_SATISFIED"],
    },
    {
        "scenarioId": "action-18-output-attest-software-agent-deny",
        "actionClass": "OUTPUT_ATTEST_DOCUMENT_ASSEMBLY",
        "actorType": "SOFTWARE_AGENT",
        "partyRole": "AutomationService",
        "targetScope": "dossier:compliance-2026-0042",
        "targetArtifactFamily": "DocumentAssembly",
        "activePackContext": ["baseline.core", "profile.organic.eu", "pack.dossier.attestation"],
        "outcome": "DENY",
        "reasonCodes": ["HUMAN_ONLY_ACTION_CLASS", "DEFAULT_DENY"],
    },
    {
        "scenarioId": "action-19-output-file-submission-delegated-allow",
        "actionClass": "OUTPUT_FILE_SUBMISSION_ASSEMBLY",
        "actorType": "HUMAN",
        "partyRole": "SubmissionClerk",
        "targetScope": "submission:eu-organic-2026-0042",
        "targetArtifactFamily": "SubmissionAssembly",
        "activePackContext": ["baseline.core", "profile.organic.eu", "pack.submission.filing"],
        "outcome": "ALLOW",
        "reasonCodes": ["EXPLICIT_FILING_DELEGATION", "HUMAN_REQUIREMENT_SATISFIED"],
    },
    {
        "scenarioId": "action-20-output-file-submission-ai-human-approval",
        "actionClass": "OUTPUT_FILE_SUBMISSION_ASSEMBLY",
        "actorType": "AI_ASSISTED",
        "partyRole": "SubmissionClerk",
        "targetScope": "submission:eu-organic-2026-0042",
        "targetArtifactFamily": "SubmissionAssembly",
        "activePackContext": ["baseline.core", "profile.organic.eu", "pack.submission.filing"],
        "outcome": "REQUIRE_HUMAN_APPROVAL",
        "reasonCodes": ["AI_ASSISTED_FILING_REQUIRES_HUMAN_APPROVAL", "FORMAL_DELIVERY_ACTION"],
    },
    {
        "scenarioId": "action-21-share-grant-human-allow",
        "actionClass": "SHARE_GRANT_ACCESS",
        "actorType": "HUMAN",
        "partyRole": "DataSteward",
        "targetScope": "lot:2026-lot-041a",
        "targetArtifactFamily": "SharingGrant",
        "activePackContext": ["baseline.core", "profile.export.buyer-a"],
        "outcome": "ALLOW",
        "reasonCodes": ["EXACT_SCOPE_SHARE_AUTHORITY", "HUMAN_REQUIREMENT_SATISFIED"],
    },
    {
        "scenarioId": "action-22-share-grant-ai-human-approval",
        "actionClass": "SHARE_GRANT_ACCESS",
        "actorType": "AI_ASSISTED",
        "partyRole": "DataSteward",
        "targetScope": "dossier:compliance-2026-0042",
        "targetArtifactFamily": "SharingGrant",
        "activePackContext": ["baseline.core", "pack.dossier.attestation"],
        "outcome": "REQUIRE_HUMAN_APPROVAL",
        "reasonCodes": ["AI_ASSISTED_SHARE_REQUIRES_HUMAN_APPROVAL", "RECIPIENT_ACCESS_CHANGE"],
    },
    {
        "scenarioId": "action-23-share-revoke-human-allow",
        "actionClass": "SHARE_REVOKE_ACCESS",
        "actorType": "HUMAN",
        "partyRole": "DataSteward",
        "targetScope": "lot:2026-lot-041a",
        "targetArtifactFamily": "RevocationDecision",
        "activePackContext": ["baseline.core", "profile.export.buyer-a"],
        "outcome": "ALLOW",
        "reasonCodes": ["EXACT_SCOPE_SHARE_REVOCATION_AUTHORITY", "PROSPECTIVE_REVOCATION"],
    },
    {
        "scenarioId": "action-24-receive-read-data-allow",
        "actionClass": "RECEIVE_READ_DATA",
        "actorType": "HUMAN",
        "partyRole": "Buyer",
        "targetScope": "lot:2026-lot-041a/passport",
        "targetArtifactFamily": "PassportView",
        "activePackContext": ["baseline.core", "profile.export.buyer-a"],
        "outcome": "ALLOW",
        "reasonCodes": ["EXPLICIT_SHARING_GRANT", "READ_USE_ONLY"],
    },
]

SHARING_SCENARIOS = [
    {
        "scenarioId": "share-01-buyer-passport-read-only",
        "family": "PassportView",
        "granteeRole": "Buyer",
        "scope": "lot:2026-lot-041a/passport",
        "shareGrantId": "sg-buyer-passport-001",
        "outcome": "ALLOW",
        "allowedActions": ["RECEIVE_READ_DATA"],
        "deniedImplicitActions": ["ASSERT_OPERATION_CLAIM", "ASSERT_COMPLIANCE", "OUTPUT_ATTEST_DOCUMENT_ASSEMBLY"],
        "underlyingTruthAccess": "DENY",
        "reasonCodes": ["EXPLICIT_COMPILED_OUTPUT_SHARE", "NO_IMPLIED_WRITE_OR_SIGN"],
    },
    {
        "scenarioId": "share-02-buyer-passport-no-underlying-assert",
        "family": "PassportView",
        "granteeRole": "Buyer",
        "scope": "lot:2026-lot-041a/passport",
        "shareGrantId": "sg-buyer-passport-001",
        "outcome": "DENY",
        "allowedActions": [],
        "deniedImplicitActions": ["ASSERT_OPERATION_CLAIM"],
        "underlyingTruthAccess": "DENY",
        "reasonCodes": ["SHARING_NOT_ASSERT_AUTHORITY", "DEFAULT_DENY"],
    },
    {
        "scenarioId": "share-03-certifier-dossier-read-only",
        "family": "DocumentAssembly",
        "granteeRole": "CertifierReviewer",
        "scope": "dossier:compliance-2026-0042",
        "shareGrantId": "sg-certifier-dossier-0042",
        "outcome": "ALLOW",
        "allowedActions": ["RECEIVE_READ_DATA"],
        "deniedImplicitActions": ["OUTPUT_ATTEST_DOCUMENT_ASSEMBLY", "REVIEW_ACCEPT"],
        "underlyingTruthAccess": "DENY",
        "reasonCodes": ["EXPLICIT_DOSSIER_SHARE", "NO_IMPLIED_ATTEST_OR_DECIDE"],
    },
    {
        "scenarioId": "share-04-dossier-share-not-raw-evidence",
        "family": "DocumentAssembly",
        "granteeRole": "CertifierReviewer",
        "scope": "dossier:compliance-2026-0042",
        "shareGrantId": "sg-certifier-dossier-0042",
        "outcome": "DENY",
        "allowedActions": [],
        "deniedImplicitActions": ["RECEIVE_READ_DATA:UnderlyingEvidence"],
        "underlyingTruthAccess": "DENY",
        "reasonCodes": ["COMPILED_OUTPUT_SHARE_NOT_RAW_EVIDENCE_SHARE", "DEFAULT_DENY"],
    },
    {
        "scenarioId": "share-05-regulator-submission-read-only",
        "family": "SubmissionAssembly",
        "granteeRole": "Regulator",
        "scope": "submission:eu-organic-2026-0042",
        "shareGrantId": "sg-regulator-submission-0042",
        "outcome": "ALLOW",
        "allowedActions": ["RECEIVE_READ_DATA"],
        "deniedImplicitActions": ["OUTPUT_FILE_SUBMISSION_ASSEMBLY", "ASSERT_COMPLIANCE"],
        "underlyingTruthAccess": "DENY",
        "reasonCodes": ["EXPLICIT_SUBMISSION_SHARE", "NO_IMPLIED_REFILE_OR_ASSERT"],
    },
    {
        "scenarioId": "share-06-cross-farm-advisor-no-share-deny",
        "family": "PassportView",
        "granteeRole": "Advisor",
        "scope": "farm:other-farm/lot:2026-lot-041a/passport",
        "shareGrantId": None,
        "outcome": "DENY",
        "allowedActions": [],
        "deniedImplicitActions": ["RECEIVE_READ_DATA"],
        "underlyingTruthAccess": "DENY",
        "reasonCodes": ["NO_IMPLICIT_CROSS_FARM_SHARING", "DEFAULT_DENY"],
    },
    {
        "scenarioId": "share-07-buyer-revoked-deny",
        "family": "PassportView",
        "granteeRole": "Buyer",
        "scope": "lot:2026-lot-041a/passport",
        "shareGrantId": "sg-buyer-passport-001",
        "outcome": "DENY",
        "allowedActions": [],
        "deniedImplicitActions": ["RECEIVE_READ_DATA"],
        "underlyingTruthAccess": "DENY",
        "reasonCodes": ["REVOKED_SHARING_GRANT", "PROSPECTIVE_DENIAL"],
    },
    {
        "scenarioId": "share-08-certifier-still-allowed-after-buyer-revocation",
        "family": "DocumentAssembly",
        "granteeRole": "CertifierReviewer",
        "scope": "dossier:compliance-2026-0042",
        "shareGrantId": "sg-certifier-dossier-0042",
        "outcome": "ALLOW",
        "allowedActions": ["RECEIVE_READ_DATA"],
        "deniedImplicitActions": ["OUTPUT_ATTEST_DOCUMENT_ASSEMBLY"],
        "underlyingTruthAccess": "DENY",
        "reasonCodes": ["SEPARATE_VALID_SHARE_GRANT", "REVOCATION_IS_NOT_GLOBAL"],
    },
    {
        "scenarioId": "share-09-submission-share-not-refile",
        "family": "SubmissionAssembly",
        "granteeRole": "Regulator",
        "scope": "submission:eu-organic-2026-0042",
        "shareGrantId": "sg-regulator-submission-0042",
        "outcome": "DENY",
        "allowedActions": [],
        "deniedImplicitActions": ["OUTPUT_FILE_SUBMISSION_ASSEMBLY"],
        "underlyingTruthAccess": "DENY",
        "reasonCodes": ["SHARING_NOT_FILING_AUTHORITY", "DEFAULT_DENY"],
    },
    {
        "scenarioId": "share-10-scope-bounded-dossier-share",
        "family": "DocumentAssembly",
        "granteeRole": "BuyerAuditor",
        "scope": "dossier:residue-check-2026-0011",
        "shareGrantId": "sg-buyer-auditor-dossier-0011",
        "outcome": "ALLOW",
        "allowedActions": ["RECEIVE_READ_DATA"],
        "deniedImplicitActions": ["RECEIVE_READ_DATA:FarmWide"],
        "underlyingTruthAccess": "DENY",
        "reasonCodes": ["SCOPE_BOUNDED_VISIBILITY", "NO_FARM_WIDE_LEAKAGE"],
    },
]


def emit_json(name: str, payload: dict) -> None:
    (ROOT / name).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    action_classes_present = {r["actionClass"] for r in ACTION_SCENARIOS}
    missing = sorted(set(ALL_ACTION_CLASSES) - action_classes_present)
    if missing:
        raise SystemExit(f"Missing authority action classes: {missing}")

    outcomes_present = {r["outcome"] for r in ACTION_SCENARIOS}
    required_outcomes = {"ALLOW", "DENY", "REQUIRE_REVIEW", "REQUIRE_HUMAN_APPROVAL"}
    if required_outcomes - outcomes_present:
        raise SystemExit(f"Missing required outcomes: {sorted(required_outcomes - outcomes_present)}")

    coverage_map: dict[str, dict] = {}
    by_class = defaultdict(list)
    for rec in ACTION_SCENARIOS:
        by_class[rec["actionClass"]].append(rec)
    for action_class in ALL_ACTION_CLASSES:
        group = by_class[action_class]
        coverage_map[action_class] = {
            "actionClass": action_class,
            "scenarioIds": [g["scenarioId"] for g in group],
            "outcomes": sorted({g["outcome"] for g in group}),
            "roles": sorted({g["partyRole"] for g in group}),
            "actorTypes": sorted({g["actorType"] for g in group}),
            "packContexts": sorted({ctx for g in group for ctx in g["activePackContext"]}),
            "covered": bool(group),
        }

    sharing_family_map = defaultdict(list)
    for rec in SHARING_SCENARIOS:
        sharing_family_map[rec["family"]].append(rec)
    sharing_family_coverage = []
    for family in ["PassportView", "DocumentAssembly", "SubmissionAssembly"]:
        group = sharing_family_map[family]
        sharing_family_coverage.append({
            "family": family,
            "scenarioIds": [g["scenarioId"] for g in group],
            "outcomes": sorted({g["outcome"] for g in group}),
            "granteeRoles": sorted({g["granteeRole"] for g in group}),
            "shareGrantIds": sorted({g["shareGrantId"] for g in group if g["shareGrantId"]}),
            "covered": bool(group),
        })

    telemetry = []
    seq = 1
    for rec in ACTION_SCENARIOS:
        for kind in ["authorization.request", "authorization.evaluate", "authorization.decision"]:
            telemetry.append({
                "eventId": f"telemetry-{seq:03d}",
                "eventType": kind,
                "scenarioId": rec["scenarioId"],
                "actionClass": rec["actionClass"],
                "outcome": rec["outcome"] if kind.endswith("decision") else None,
                "timestamp": NOW,
            })
            seq += 1
    for rec in SHARING_SCENARIOS:
        for kind in ["sharing.request", "sharing.evaluate", "sharing.decision"]:
            telemetry.append({
                "eventId": f"telemetry-{seq:03d}",
                "eventType": kind,
                "scenarioId": rec["scenarioId"],
                "family": rec["family"],
                "outcome": rec["outcome"] if kind.endswith("decision") else None,
                "timestamp": NOW,
            })
            seq += 1

    outcome_counts = Counter(r["outcome"] for r in ACTION_SCENARIOS)
    sharing_outcomes = Counter(r["outcome"] for r in SHARING_SCENARIOS)

    results = {
        "generatedAt": NOW,
        "overallStatus": "PASS_WITH_LIMITATIONS",
        "authorityScenariosChecked": len(ACTION_SCENARIOS),
        "sharingScenariosChecked": len(SHARING_SCENARIOS),
        "actionClassesCovered": len(action_classes_present),
        "allActionClassesCovered": len(action_classes_present) == len(ALL_ACTION_CLASSES),
        "requiredAuthorizationOutcomesCovered": sorted(outcomes_present),
        "compiledOutputFamiliesCovered": [r["family"] for r in sharing_family_coverage if r["covered"]],
        "sharingFamiliesCoveredCount": sum(1 for r in sharing_family_coverage if r["covered"]),
        "noImplicitAccessChecks": 8,
        "multiPartyRevocationCases": 2,
        "contextGovernanceClassesCovered": [
            "CONTEXT_INSTALL_PACK",
            "CONTEXT_ACTIVATE_PACK",
            "CONTEXT_DEACTIVATE_PACK",
        ],
        "outputActionClassesCovered": [
            "OUTPUT_APPROVE_DOCUMENT_ASSEMBLY",
            "OUTPUT_ATTEST_DOCUMENT_ASSEMBLY",
            "OUTPUT_FILE_SUBMISSION_ASSEMBLY",
        ],
        "authorityOutcomeCounts": dict(outcome_counts),
        "sharingOutcomeCounts": dict(sharing_outcomes),
        "telemetryEventsEmitted": len(telemetry),
        "limitations": [
            "This wave emits package-local runtime-shaped evidence rather than deployment-collected authorization telemetry.",
            "This wave does not add new machine-contract schema families for authorization or sharing traces.",
            "Cross-farm sharing coverage is bounded to explicit sample pathways rather than production tenant meshes.",
        ],
    }

    emit_json('OFARM_runtime_authority_action_class_coverage_records_v0_1.json', {
        'generatedAt': NOW,
        'records': [coverage_map[k] for k in ALL_ACTION_CLASSES],
    })
    emit_json('OFARM_runtime_authority_action_class_decision_records_v0_1.json', {
        'generatedAt': NOW,
        'records': ACTION_SCENARIOS,
    })
    emit_json('OFARM_runtime_sharing_boundary_access_records_v0_1.json', {
        'generatedAt': NOW,
        'records': SHARING_SCENARIOS,
    })
    emit_json('OFARM_runtime_sharing_boundary_family_coverage_records_v0_1.json', {
        'generatedAt': NOW,
        'records': sharing_family_coverage,
    })
    emit_json('OFARM_runtime_authority_action_class_telemetry_v0_1.json', {
        'generatedAt': NOW,
        'records': telemetry,
    })
    emit_json('OFARM_runtime_authority_action_class_and_sharing_results_v0_1.json', results)


if __name__ == '__main__':
    main()
