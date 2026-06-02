
#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MC = ROOT / "03_machine_contracts"
IMP = ROOT / "04_implementation_and_conformance"
RECORDS = IMP / "OFARM_advisory_to_execution_to_passport_dispute_break_test_records_v0_1.json"
OUT = IMP / "OFARM_advisory_to_execution_to_passport_dispute_break_test_results_v0_1.json"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def collect_primary_ids(obj: Any) -> dict[str, str]:
    ids: dict[str, str] = {}
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, str) and (key.endswith("Id") or key in {"basisId", "snapshotId", "passportViewId", "reviewDecisionId"}):
                ids[value] = key
    return ids


def build_index() -> dict[str, tuple[str, Any]]:
    index: dict[str, tuple[str, Any]] = {}
    for path in sorted(MC.glob("*_example_*.json")):
        obj = load_json(path)
        for value in collect_primary_ids(obj):
            index[value] = (path.name, obj)
    return index


def main() -> int:
    records = load_json(RECORDS)
    id_index = build_index()

    scenario_results = []
    all_pass = True

    for scenario in records["scenarios"]:
        checks: dict[str, bool] = {}

        bridge = id_index.get(scenario["bridgeCandidateRef"])
        adv_mat = id_index.get(scenario["advisoryMaterializationResultRef"])
        plan = id_index.get(scenario["plannedInterventionRef"])
        event = id_index.get(scenario["semanticEventRef"])
        assertion = id_index.get(scenario["assertionRef"])
        review = id_index.get(scenario["reviewDecisionRef"])
        consequence = id_index.get(scenario["acceptedConsequenceRef"])
        basis = id_index.get(scenario["complianceMaterializationBasisRef"])
        snapshot = id_index.get(scenario["complianceMaterializationSnapshotRef"])
        comp_mat = id_index.get(scenario["complianceMaterializationResultRef"])
        passport = id_index.get(scenario["passportViewRef"])
        sharing = id_index.get(scenario["sharingGrantRef"])
        auth_trace = id_index.get(scenario["authorizationTraceRef"])
        pub_req = id_index.get(scenario["publicationRequestRef"])
        pub_res = id_index.get(scenario["publicationResultRef"])
        attest_req = id_index.get(scenario["attestationRequestRef"])
        attest_res = id_index.get(scenario["attestationResultRef"])

        checks["bridgeResolvable"] = bridge is not None
        checks["advisoryMaterializationResolvable"] = adv_mat is not None
        checks["draftPlanResolvable"] = plan is not None
        checks["semanticEventResolvable"] = event is not None
        checks["assertionResolvable"] = assertion is not None
        checks["reviewResolvable"] = review is not None
        checks["acceptedConsequenceResolvable"] = consequence is not None
        checks["complianceBasisResolvable"] = basis is not None
        checks["complianceSnapshotResolvable"] = snapshot is not None
        checks["complianceMaterializationResolvable"] = comp_mat is not None
        checks["passportResolvable"] = passport is not None
        checks["sharingGrantResolvable"] = sharing is not None
        checks["authorizationTraceResolvable"] = auth_trace is not None
        checks["publicationRequestResolvable"] = pub_req is not None
        checks["publicationResultResolvable"] = pub_res is not None
        checks["attestationRequestResolvable"] = attest_req is not None
        checks["attestationResultResolvable"] = attest_res is not None

        if bridge and plan and adv_mat:
            checks["bridgeIsProposalOnly"] = bridge[1].get("bridgePosture") == "PROPOSAL_ONLY"
            checks["bridgeOriginIsAdvisory"] = bridge[1].get("originTwin") == "ADVISORY"
            checks["bridgeHumanGateRequired"] = bridge[1].get("requiresHumanApproval") is True
            checks["bridgeTargetsCompliance"] = bridge[1].get("intendedNextTwin") == "COMPLIANCE"
            checks["bridgeLinksDraftPlan"] = bridge[1].get("proposedDraftArtifactRef") == plan[1].get("plannedInterventionId")
            checks["advisoryMaterializationIsStale"] = adv_mat[1].get("targetTwin") == "ADVISORY" and adv_mat[1].get("freshnessState") == "STALE"
            checks["bridgeRequiresComplianceRecheck"] = "RECHECK_COMPLIANCE_FRESHNESS" in bridge[1].get("recheckRequirements", [])
        else:
            checks["bridgeIsProposalOnly"] = False
            checks["bridgeOriginIsAdvisory"] = False
            checks["bridgeHumanGateRequired"] = False
            checks["bridgeTargetsCompliance"] = False
            checks["bridgeLinksDraftPlan"] = False
            checks["advisoryMaterializationIsStale"] = False
            checks["bridgeRequiresComplianceRecheck"] = False

        if plan:
            checks["draftPlanStillDraft"] = plan[1].get("planState") == "DRAFT"
        else:
            checks["draftPlanStillDraft"] = False

        if event and assertion and review and consequence:
            checks["assertionLinksSemanticEvent"] = scenario["semanticEventRef"] in assertion[1].get("provenanceRefs", [])
            checks["reviewTargetsAssertion"] = review[1].get("reviewedArtifactRef") == scenario["assertionRef"]
            checks["reviewProducesAcceptedConsequence"] = scenario["acceptedConsequenceRef"] in review[1].get("resultingAcceptedConsequenceRefs", [])
            checks["acceptedConsequenceComesFromEvent"] = consequence[1].get("sourceEventRef") == scenario["semanticEventRef"]
            checks["acceptedConsequenceUsesReview"] = consequence[1].get("acceptedByReviewDecisionRef") == scenario["reviewDecisionRef"]
            checks["noBridgeShortcutIntoAcceptedConsequence"] = consequence[1].get("sourceEventRef") != scenario["bridgeCandidateRef"]
        else:
            checks["assertionLinksSemanticEvent"] = False
            checks["reviewTargetsAssertion"] = False
            checks["reviewProducesAcceptedConsequence"] = False
            checks["acceptedConsequenceComesFromEvent"] = False
            checks["acceptedConsequenceUsesReview"] = False
            checks["noBridgeShortcutIntoAcceptedConsequence"] = False

        if basis and snapshot and comp_mat and bridge:
            checks["complianceBasisUsesAcceptedConsequence"] = scenario["acceptedConsequenceRef"] in basis[1].get("contributingAcceptedConsequenceRefs", [])
            checks["basisDoesNotUseBridgeCandidate"] = scenario["bridgeCandidateRef"] not in basis[1].get("contributingAcceptedConsequenceRefs", []) and scenario["bridgeCandidateRef"] not in basis[1].get("contributingAssertionRefs", [])
            checks["snapshotLinksBasis"] = snapshot[1].get("materializationBasisRef") == scenario["complianceMaterializationBasisRef"]
            checks["complianceMaterializationFresh"] = comp_mat[1].get("targetTwin") == "COMPLIANCE" and comp_mat[1].get("freshnessState") == "FRESH"
            checks["complianceMaterializationDistinctFromAdvisorySource"] = comp_mat[1].get("resultId") != bridge[1].get("sourceMaterializationResultRef")
            checks["publicationGroundedInComplianceMaterialization"] = comp_mat[1].get("materializationBasisRef") == scenario["complianceMaterializationBasisRef"]
        else:
            checks["complianceBasisUsesAcceptedConsequence"] = False
            checks["basisDoesNotUseBridgeCandidate"] = False
            checks["snapshotLinksBasis"] = False
            checks["complianceMaterializationFresh"] = False
            checks["complianceMaterializationDistinctFromAdvisorySource"] = False
            checks["publicationGroundedInComplianceMaterialization"] = False

        if passport and comp_mat and sharing and auth_trace and pub_req and pub_res:
            checks["passportUsesComplianceTwin"] = passport[1].get("twin") == "COMPLIANCE"
            checks["passportRemainsLive"] = passport[1].get("freezeState") == "LIVE_RECOMPUTABLE"
            checks["passportLinksFreshMaterialization"] = passport[1].get("materializationResultRef") == scenario["complianceMaterializationResultRef"]
            checks["sharingGrantTargetsPassport"] = sharing[1].get("sharedArtifactRef") == scenario["passportViewRef"]
            checks["authorizationUsesSharingGrant"] = scenario["sharingGrantRef"] in auth_trace[1].get("sharingBasisUsed", [])
            checks["publicationServesPassport"] = pub_req[1].get("outputMetadataRef") == scenario["passportViewRef"] and pub_res[1].get("outputMetadataRef") == scenario["passportViewRef"]
            checks["publicationResultPublished"] = pub_res[1].get("outcome") == "PUBLISHED"
            checks["publicationTraceMatchesAuthorization"] = pub_res[1].get("authorizationDecisionTraceRef") == scenario["authorizationTraceRef"]
        else:
            checks["passportUsesComplianceTwin"] = False
            checks["passportRemainsLive"] = False
            checks["passportLinksFreshMaterialization"] = False
            checks["sharingGrantTargetsPassport"] = False
            checks["authorizationUsesSharingGrant"] = False
            checks["publicationServesPassport"] = False
            checks["publicationResultPublished"] = False
            checks["publicationTraceMatchesAuthorization"] = False

        if attest_req and attest_res:
            reason_codes = []
            for problem in attest_res[1].get("problems", []):
                reason_codes.append(problem.get("reasonCode"))
            checks["attestationAttemptTargetsSamePassport"] = attest_req[1].get("outputMetadataRef") == scenario["passportViewRef"] and attest_res[1].get("outputMetadataRef") == scenario["passportViewRef"]
            checks["livePassportAttestationDenied"] = attest_res[1].get("outcome") == "DENIED"
            checks["passportDocumentBoundaryPreserved"] = "OUTPUT_KIND_NOT_ATTESTABLE" in reason_codes
        else:
            checks["attestationAttemptTargetsSamePassport"] = False
            checks["livePassportAttestationDenied"] = False
            checks["passportDocumentBoundaryPreserved"] = False

        checks["expectedTerminalOutcomeValid"] = (
            scenario["expectedTerminalOutcome"] == "PUBLISHED_LIVE_PASSPORT_WITH_NO_ADVISORY_SHORTCUT"
            and checks["publicationResultPublished"]
            and checks["noBridgeShortcutIntoAcceptedConsequence"]
            and checks["passportDocumentBoundaryPreserved"]
        )

        status = "PASS" if all(checks.values()) else "FAIL"
        if status != "PASS":
            all_pass = False
        scenario_results.append({
            "scenarioId": scenario["scenarioId"],
            "status": status,
            "checks": checks
        })

    results = {
        "wave": records["wave"],
        "title": records["title"],
        "overallStatus": "PASS_WITH_LIMITATIONS" if all_pass else "FAIL",
        "scenarioCount": len(records["scenarios"]),
        "scenarioResults": scenario_results,
        "coverageAdvances": [
            "proves an Advisory-origin bridge candidate does not become authoritative truth directly",
            "proves buyer-facing passport publication rechecks fresh Compliance materialization rather than reusing exploratory Advisory state",
            "proves the live PassportView versus frozen DocumentAssembly boundary remains enforced during dispute pressure"
        ],
        "limitations": [
            "This is a package-local hostile composition test rather than deployment-collected bridge approval telemetry.",
            "The test proves one pruning-to-passport chain only; broader advisory-to-submission and advisory-to-dossier permutations remain follow-on work."
        ]
    }
    OUT.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
