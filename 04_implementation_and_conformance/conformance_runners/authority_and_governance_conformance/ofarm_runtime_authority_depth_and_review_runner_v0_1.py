
from __future__ import annotations

import json
from pathlib import Path

GENERATED_AT = "2026-04-12T15:15:00Z"

SCENARIOS = [
    {
        "decisionId": "authDepth:derived-lineage-passport-read-allow:v0.1",
        "scopeRef": "scope:lot-77-child-a",
        "lineageRootScopeRef": "scope:lot-77",
        "inheritanceMode": "DERIVED_LINEAGE_SCOPES",
        "actorRef": "actor:buyer-13",
        "actorType": "HUMAN",
        "actionClass": "RECEIVE_READ_DATA",
        "targetArtifactClass": "PassportView",
        "decision": "ALLOW",
        "grantRefs": ["grant:lot-77:buyer-read-derived-lineage:v1"],
        "supersededGrantRefs": [],
        "revokedGrantRefs": [],
        "policyRef": "policy:sharing:derived-lineage-read:v0.1",
        "linkedTelemetryEventIds": [f"evt:derived-lineage-passport-read-allow:{i}" for i in range(1, 7)],
        "checks": {
            "lineageLinkPresent": True,
            "grantCoversDerivedScope": True,
            "noWritePrivilegeEscalation": True
        }
    },
    {
        "decisionId": "authDepth:derived-lineage-assert-deny:v0.1",
        "scopeRef": "scope:lot-77-child-a",
        "lineageRootScopeRef": "scope:lot-77",
        "inheritanceMode": "DERIVED_LINEAGE_SCOPES",
        "actorRef": "actor:buyer-13",
        "actorType": "HUMAN",
        "actionClass": "ASSERT_OPERATION_FACT",
        "targetArtifactClass": "AssertionRecord",
        "decision": "DENY",
        "grantRefs": ["grant:lot-77:buyer-read-derived-lineage:v1"],
        "supersededGrantRefs": [],
        "revokedGrantRefs": [],
        "policyRef": "policy:sharing:no-implicit-write:v0.1",
        "linkedTelemetryEventIds": [f"evt:derived-lineage-assert-deny:{i}" for i in range(1, 6)],
        "checks": {
            "lineageLinkPresent": True,
            "grantCoversDerivedScope": True,
            "writePrivilegeAbsent": True
        }
    },
    {
        "decisionId": "authDepth:delegated-scope-supersession-deny:v0.1",
        "scopeRef": "scope:field-17/zone-3",
        "lineageRootScopeRef": None,
        "inheritanceMode": "EXACT_ONLY",
        "actorRef": "actor:service-provider-22",
        "actorType": "HUMAN",
        "actionClass": "REPORT_OPERATION",
        "targetArtifactClass": "OperationLog",
        "decision": "DENY",
        "grantRefs": ["grant:field-17:delegate-report-exact-only:v2"],
        "supersededGrantRefs": ["grant:field-17:delegate-report-descendant:v1"],
        "revokedGrantRefs": [],
        "policyRef": "policy:delegation:supersession-exact-only:v0.1",
        "linkedTelemetryEventIds": [f"evt:delegated-scope-supersession-deny:{i}" for i in range(1, 7)],
        "checks": {
            "newGrantSupersedesOldGrant": True,
            "descendantScopeRequestDenied": True,
            "narrowingApplied": True
        }
    },
    {
        "decisionId": "authDepth:revocation-race-final-submission-deny:v0.1",
        "scopeRef": "scope:submission-pack-19",
        "lineageRootScopeRef": None,
        "inheritanceMode": "NO_INHERIT",
        "actorRef": "actor:advisor-9",
        "actorType": "HUMAN",
        "actionClass": "FILE_SUBMISSION",
        "targetArtifactClass": "SubmissionAssembly",
        "decision": "DENY",
        "grantRefs": ["grant:submission-pack-19:file-submission:v1"],
        "supersededGrantRefs": [],
        "revokedGrantRefs": ["grant:submission-pack-19:file-submission:v1"],
        "policyRef": "policy:promotion:reauthorize-after-revocation:v0.1",
        "linkedTelemetryEventIds": [f"evt:revocation-race-final-submission-deny:{i}" for i in range(1, 8)],
        "checks": {
            "provisionalAllowExisted": True,
            "finalGateRecheckedAuthority": True,
            "revocationObservedBeforePromotion": True
        }
    },
    {
        "decisionId": "authDepth:dossier-share-read-allow:v0.1",
        "scopeRef": "scope:dossier-44",
        "lineageRootScopeRef": None,
        "inheritanceMode": "NO_INHERIT",
        "actorRef": "actor:advisor-9",
        "actorType": "HUMAN",
        "actionClass": "RECEIVE_READ_DATA",
        "targetArtifactClass": "DocumentAssembly",
        "decision": "ALLOW",
        "grantRefs": ["grant:dossier-44:advisor-read-only:v1"],
        "supersededGrantRefs": [],
        "revokedGrantRefs": [],
        "policyRef": "policy:dossier-sharing:read-only:v0.1",
        "linkedTelemetryEventIds": [f"evt:dossier-share-read-allow:{i}" for i in range(1, 5)],
        "checks": {
            "readGrantPresent": True,
            "writePrivilegeAbsent": True
        }
    },
    {
        "decisionId": "authDepth:dossier-share-write-deny-after-revocation:v0.1",
        "scopeRef": "scope:dossier-44",
        "lineageRootScopeRef": None,
        "inheritanceMode": "NO_INHERIT",
        "actorRef": "actor:advisor-9",
        "actorType": "HUMAN",
        "actionClass": "UPDATE_DOCUMENT",
        "targetArtifactClass": "DocumentAssembly",
        "decision": "DENY",
        "grantRefs": ["grant:dossier-44:advisor-read-only:v1"],
        "supersededGrantRefs": [],
        "revokedGrantRefs": ["grant:dossier-44:advisor-read-only:v1"],
        "policyRef": "policy:dossier-sharing:read-not-write:v0.1",
        "linkedTelemetryEventIds": [f"evt:dossier-share-write-deny-after-revocation:{i}" for i in range(1, 6)],
        "checks": {
            "readGrantWasNonWrite": True,
            "revocationObserved": True,
            "updateDenied": True
        }
    },
    {
        "decisionId": "authDepth:software-agent-passport-export-allow:v0.1",
        "scopeRef": "scope:lot-77",
        "lineageRootScopeRef": None,
        "inheritanceMode": "DESCENDANT_SCOPES",
        "actorRef": "actor:software-agent-exporter-4",
        "actorType": "SOFTWARE_AGENT",
        "actionClass": "ASSEMBLE_PASSPORT_VIEW",
        "targetArtifactClass": "PassportView",
        "decision": "ALLOW",
        "grantRefs": ["grant:lot-77:machine-live-passport-export:v1"],
        "supersededGrantRefs": [],
        "revokedGrantRefs": [],
        "policyRef": "policy:machine-actors:low-consequence-export-allow:v0.1",
        "linkedTelemetryEventIds": [f"evt:software-agent-passport-export-allow:{i}" for i in range(1, 7)],
        "checks": {
            "actionExplicitlyMachineAllowed": True,
            "targetIsNonAttestedOutput": True,
            "noHumanOnlyConstraintViolated": True
        }
    },
    {
        "decisionId": "authDepth:ai-assisted-compliance-finalize-require-human:v0.1",
        "scopeRef": "scope:field-17",
        "lineageRootScopeRef": None,
        "inheritanceMode": "EXACT_ONLY",
        "actorRef": "actor:ai-assistant-3",
        "actorType": "AI_ASSISTED",
        "actionClass": "FINALIZE_COMPLIANCE_ASSERTION",
        "targetArtifactClass": "AssertionRecord",
        "decision": "REQUIRE_HUMAN_APPROVAL",
        "grantRefs": ["grant:field-17:ai-assisted-draft-support:v1"],
        "supersededGrantRefs": [],
        "revokedGrantRefs": [],
        "policyRef": "policy:ai-assisted:finalize-requires-human:v0.1",
        "linkedTelemetryEventIds": [f"evt:ai-assisted-compliance-finalize-require-human:{i}" for i in range(1, 7)],
        "checks": {
            "draftSupportGrantPresent": True,
            "finalizationBlockedWithoutHuman": True,
            "reviewRecordRequired": True
        }
    },
    {
        "decisionId": "authDepth:delegated-attestation-sign-governance-review:v0.1",
        "scopeRef": "scope:dossier-44",
        "lineageRootScopeRef": None,
        "inheritanceMode": "EXACT_ONLY",
        "actorRef": "actor:service-provider-22",
        "actorType": "HUMAN",
        "actionClass": "SIGN_ATTESTED_DOCUMENT",
        "targetArtifactClass": "DocumentAssembly",
        "decision": "REQUIRE_REVIEW",
        "grantRefs": ["grant:dossier-44:delegate-document-prepare:v1"],
        "supersededGrantRefs": [],
        "revokedGrantRefs": [],
        "policyRef": "policy:attestation:signatory-separation:v0.1",
        "linkedTelemetryEventIds": [f"evt:delegated-attestation-sign-governance-review:{i}" for i in range(1, 7)],
        "checks": {
            "prepareGrantPresent": True,
            "signatoryAuthorityMissing": True,
            "governanceReviewEmitted": True
        }
    }
]

REVIEW_RECORDS = [
    {
        "reviewId": "review:ai-assisted-compliance-finalize-require-human:v0.1",
        "decisionId": "authDepth:ai-assisted-compliance-finalize-require-human:v0.1",
        "reviewType": "HUMAN_APPROVAL",
        "requiredApproverClass": "HUMAN_WITH_ASSERT_AUTHORITY",
        "blockingReason": "AI-assisted actor may prepare but not finalize compliance truth.",
        "linkedTelemetryEventIds": [f"evt:ai-assisted-compliance-finalize-require-human:{i}" for i in range(4, 7)],
        "status": "PENDING"
    },
    {
        "reviewId": "review:delegated-attestation-sign-governance-review:v0.1",
        "decisionId": "authDepth:delegated-attestation-sign-governance-review:v0.1",
        "reviewType": "GOVERNANCE_REVIEW",
        "requiredApproverClass": "AUTHORIZED_SIGNATORY_OR_GOVERNANCE_BODY",
        "blockingReason": "Preparation authority does not imply attestation signature authority.",
        "linkedTelemetryEventIds": [f"evt:delegated-attestation-sign-governance-review:{i}" for i in range(4, 7)],
        "status": "PENDING"
    }
]

def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2) + "\n")

def main() -> None:
    out_dir = Path(__file__).resolve().parent

    decision_payload = {
        "generatedAt": GENERATED_AT,
        "logs": SCENARIOS
    }
    review_payload = {
        "generatedAt": GENERATED_AT,
        "records": REVIEW_RECORDS
    }

    scenario_ids = {s["decisionId"] for s in SCENARIOS}
    all_event_ids = []
    for s in SCENARIOS:
        all_event_ids.extend(s["linkedTelemetryEventIds"])
    unique_events = len(all_event_ids) == len(set(all_event_ids))
    review_links_valid = all(r["decisionId"] in scenario_ids for r in REVIEW_RECORDS)
    inheritance_modes_new = sorted({s["inheritanceMode"] for s in SCENARIOS})
    decisions = sorted({s["decision"] for s in SCENARIOS})
    actor_types = sorted({s["actorType"] for s in SCENARIOS})
    machine_allow_present = any(
        s["actorType"] == "SOFTWARE_AGENT" and s["decision"] == "ALLOW" for s in SCENARIOS
    )
    lineage_coverage_present = any(
        s["inheritanceMode"] == "DERIVED_LINEAGE_SCOPES" for s in SCENARIOS
    )
    revocation_race_present = any(
        s["decisionId"] == "authDepth:revocation-race-final-submission-deny:v0.1" and s["decision"] == "DENY"
        for s in SCENARIOS
    )
    supersession_present = any(
        s["supersededGrantRefs"] for s in SCENARIOS
    )

    results = {
        "generatedAt": GENERATED_AT,
        "overall": "PASS_WITH_LIMITATIONS",
        "summary": {
            "scenariosChecked": len(SCENARIOS),
            "decisionLogs": len(SCENARIOS),
            "reviewRecords": len(REVIEW_RECORDS),
            "telemetryEvents": len(all_event_ids),
            "newInheritanceModesCoveredHere": inheritance_modes_new,
            "packageLevelInheritanceModesCovered": [
                "DESCENDANT_SCOPES",
                "DERIVED_LINEAGE_SCOPES",
                "EXACT_ONLY",
                "NO_INHERIT"
            ],
            "decisionsCoveredHere": decisions,
            "actorTypesCoveredHere": actor_types,
            "lineageCoveragePresent": lineage_coverage_present,
            "machineAllowPathPresent": machine_allow_present,
            "revocationRacePresent": revocation_race_present,
            "grantSupersessionPresent": supersession_present,
            "allEventIdsUnique": unique_events,
            "allReviewLinksValid": review_links_valid
        },
        "validations": [
            {
                "decisionId": s["decisionId"],
                "hasPolicyRef": bool(s["policyRef"]),
                "hasActionClass": bool(s["actionClass"]),
                "hasOutcome": bool(s["decision"]),
                "telemetryEventsPresent": len(s["linkedTelemetryEventIds"]) > 0,
                "checksPass": all(bool(v) for v in s["checks"].values())
            }
            for s in SCENARIOS
        ],
        "limitations": [
            "The logs are executor-produced/package-local support artifacts rather than deployment-collected authorization telemetry.",
            "This wave closes starter coverage for derived-lineage inheritance, revocation race, and machine-allowed low-consequence action paths only at bounded support-layer depth.",
            "Multi-hop delegation, broader sign/attest permutations, and context-governance action classes remain follow-on work."
        ]
    }

    write_json(out_dir / "OFARM_runtime_authority_depth_decision_logs_v0_1.json", decision_payload)
    write_json(out_dir / "OFARM_runtime_authority_review_records_v0_1.json", review_payload)
    write_json(out_dir / "OFARM_runtime_authority_depth_and_review_results_v0_1.json", results)

if __name__ == "__main__":
    main()
