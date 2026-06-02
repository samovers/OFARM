#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
IMPL = ROOT / '04_implementation_and_conformance'
MC = ROOT / '03_machine_contracts'
DECISION_MATRIX = IMPL / 'OFARM_submission_gateway_promotion_decision_matrix_v0_1.json'
PARTNER_GOV = IMPL / 'OFARM_partner_output_surface_governance_decision_matrix_v0_1.json'
LINKAGE = IMPL / 'OFARM_runtime_surface_partner_output_telemetry_linkage_v0_2.json'
TELEMETRY = IMPL / 'OFARM_runtime_deployment_emitted_publication_telemetry_v0_1.json'
REVIEWS = IMPL / 'OFARM_runtime_deployment_emitted_review_chain_records_v0_1.json'
CANDIDATE = IMPL / 'OFARM_submission_gateway_contract_candidate_v0_1.json'
DESCRIPTOR = IMPL / 'service_descriptions/submission_gateway_candidate_v0_1/organic_certifier_submission_gateway_descriptor_v0_1.json'
MANIFEST = MC / 'OFARM_Capability_Manifest_example_core_deployment_surface_linkage_v0_2_draft.json'
RELEASE = IMPL / 'OFARM_runtime_surface_deployment_release_bundle_example_core_surface_linkage_v0_1.json'
REQ = MC / 'OFARM_PublicationAssemblyRequest_example_submission_file_v0_1.json'
RES = MC / 'OFARM_PublicationAssemblyResult_example_submission_filed_v0_1.json'
META = MC / 'OFARM_DocumentAssemblyMetadata_example_submission_package_v0_1.json'
EVID = MC / 'OFARM_EvidenceSufficiencyCase_example_submission_package_v0_1.json'
TRACE = MC / 'OFARM_AuthorizationDecisionTrace_example_submission_file_allow_v0_1.json'
RESULTS = IMPL / 'OFARM_submission_gateway_promotion_boundary_results_v0_1.json'
def load_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))
def main() -> int:
    decision = load_json(DECISION_MATRIX)
    partner = load_json(PARTNER_GOV)
    linkage = load_json(LINKAGE)
    telemetry = load_json(TELEMETRY)
    reviews = load_json(REVIEWS)
    candidate = load_json(CANDIDATE)
    descriptor = load_json(DESCRIPTOR)
    manifest = load_json(MANIFEST)
    release = load_json(RELEASE)
    req = load_json(REQ)
    res = load_json(RES)
    meta = load_json(META)
    evid = load_json(EVID)
    trace = load_json(TRACE)
    checks: list[dict[str, str]] = []
    def record(check_id: str, ok: bool, detail: str) -> None:
        checks.append({
            'checkId': check_id,
            'status': 'PASS' if ok else 'FAIL',
            'detail': detail,
        })
    partner_decision = next(row for row in partner['decisions'] if row['partnerSurface'] == 'PARTNER_SUBMISSION_XML')
    linkage_summary = next(row for row in linkage['surfaceSummaries'] if row['partnerSurface'] == 'PARTNER_SUBMISSION_XML')
    record(
        'partner-output-posture-still-implementation-local',
        partner_decision['decision'] == 'RETAIN_IMPLEMENTATION_LOCAL_SUPPORT_OUTPUT_CHANNEL' and linkage_summary['governanceDecision'] == 'RETAIN_IMPLEMENTATION_LOCAL_SUPPORT_OUTPUT_CHANNEL',
        'submission XML should remain implementation-local in the current partner-output governance lane',
    )
    record(
        'formal-filing-threshold-still-required',
        'ESTABLISH_FORMAL_FILING_GATEWAY_OR_DELIVERY_NAMESPACE' in partner_decision.get('futurePromotionConditions', []),
        'partner-output governance decision should still require an explicit filing-gateway threshold before promotion',
    )
    record(
        'submission-specific-threshold-unsatisfied',
        decision['currentDecision']['promotionThresholdSatisfied'] is False and len(decision['currentDecision']['missingPromotionCriteria']) >= 5,
        'submission-specific decision matrix should keep the threshold unsatisfied in the current package',
    )
    record(
        'candidate-contract-basic-shape',
        candidate['partnerSurface'] == 'PARTNER_SUBMISSION_XML' and candidate['underlyingOutputKind'] == 'SUBMISSION_ASSEMBLY' and candidate['status'] == 'CANDIDATE_NOT_ACTIVE',
        'candidate contract should stay fixture-only and bound to SubmissionAssembly plus the current submission XML surface',
    )
    record(
        'candidate-descriptor-linked',
        candidate['partnerContractArtifacts']['serviceDescriptionRef'] == descriptor['serviceDescriptionId'] and candidate['partnerContractArtifacts']['localArtifactRef'] == '04_implementation_and_conformance/service_and_sdk_candidates/service_descriptions/submission_gateway_candidate_v0_1/organic_certifier_submission_gateway_descriptor_v0_1.json',
        'candidate contract should point to the local submission-gateway descriptor stub',
    )
    record(
        'receipt-and-correction-semantics-explicit',
        descriptor['receiptContract']['receiptRequired'] is True and descriptor['correctionContract']['noEditInPlace'] is True and descriptor['duplicateAndRetryContract']['requiresSubmissionCorrelationId'] is True,
        'candidate descriptor should make receipt, no-edit-in-place correction, and correlation-id semantics explicit',
    )
    required_refs = candidate['requiredGovernedRefs']
    record(
        'candidate-refs-bind-to-active-filing-artifacts',
        required_refs['publicationRequestRef'] == req['requestId']
        and required_refs['publicationResultRef'] == res['resultId']
        and required_refs['outputMetadataRef'] == meta['documentAssemblyId']
        and required_refs['evidenceSufficiencyCaseRef'] == evid['sufficiencyCaseId']
        and required_refs['authorizationDecisionTraceRef'] == trace['traceId'],
        'candidate contract should bind back to the active filing-path artifacts already shipped in 03_machine_contracts',
    )
    manifest_surface_refs = {row['targetRef'] for row in manifest['capabilitySections']['importExportSupport']['declaredSurfaces']}
    release_surface_refs = {row['surfaceIdentityRef'] for row in release['surfaceReleases']}
    record(
        'candidate-not-in-governed-manifest-or-release-lane',
        candidate['gatewayIdentityRef'] not in manifest_surface_refs and candidate['gatewayIdentityRef'] not in release_surface_refs,
        'candidate submission gateway should remain outside the current governed manifest and release lane',
    )
    scenario_ids = {e['scenarioId'] for e in telemetry['events'] if e['partnerSurface'] == 'PARTNER_SUBMISSION_XML'}
    record(
        'submission-success-and-schema-mismatch-scenarios-present',
        'gatepub-06-submission-xml-success' in scenario_ids and 'gatepub-08-submission-xml-block-schema-mismatch' in scenario_ids,
        'current publication telemetry should still demonstrate both successful filing and schema-mismatch refusal for the submission XML path',
    )
    review_records = {r['scenarioId']: r for r in reviews['records'] if r['partnerSurface'] == 'PARTNER_SUBMISSION_XML'}
    record(
        'submission-review-chain-closed-before-terminal-outcomes',
        review_records['gatepub-06-submission-xml-success']['reviewClosed'] is True and review_records['gatepub-08-submission-xml-block-schema-mismatch']['reviewClosed'] is True,
        'submission scenarios should still show closed human-approval review chains before the terminal filing or schema-block outcomes',
    )
    record(
        'lane-choice-prefers-equivalent-contract-only-because-filing-semantics-exceed-generic-surface',
        decision['currentDecision']['recommendedLaneIfPromoted'] == 'USE_EQUIVALENT_SUBMISSION_GATEWAY_CONTRACT' and any(rule['laneDecision'] == 'USE_EQUIVALENT_SUBMISSION_GATEWAY_CONTRACT' for rule in decision['laneChoiceRules']),
        'submission-specific decision lane should only point to an equivalent contract because receipt/correction/finality semantics are being treated as first-class concerns',
    )
    result = {
        'metadata': {
            'runner': Path(__file__).name,
            'scope': 'submission-gateway promotion threshold and fixture-only equivalent contract candidate for the current package',
        },
        'checks': checks,
        'overall': 'PASS_WITH_LIMITATIONS',
        'limitations': [
            'This runner validates package-local promotion posture only; it does not prove a live governed filing gateway exists.',
            'The candidate gateway contract remains implementation-support only and must not be treated as active machine-contract law.'
        ]
    }
    RESULTS.write_text(json.dumps(result, indent=2) + "\n", encoding='utf-8')
    if any(c['status'] == 'FAIL' for c in checks):
        return 1
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
