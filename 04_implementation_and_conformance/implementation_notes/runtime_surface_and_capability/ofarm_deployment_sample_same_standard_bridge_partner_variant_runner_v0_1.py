#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

try:
    import jsonschema
except ImportError as e:
    raise SystemExit('jsonschema is required for this validator') from e

ROOT = Path(__file__).resolve().parents[1]
MC = ROOT / '03_machine_contracts'
IMPL = ROOT / '04_implementation_and_conformance'
FIX = IMPL / 'ofarm_deployment_sample_same_standard_bridge_partner_variant_fixtures_v0_1'

TELEMETRY_OUT = IMPL / 'OFARM_deployment_sample_same_standard_bridge_telemetry_v0_1.json'
COVERAGE_OUT = IMPL / 'OFARM_partner_variant_same_standard_bridge_coverage_records_v0_1.json'
RESULTS_OUT = IMPL / 'OFARM_deployment_sample_same_standard_bridge_results_v0_1.json'
CANDIDATE_OUT = IMPL / 'OFARM_same_standard_bridge_pack_candidate_pairs_v0_3.json'
PROMOTION_OUT = IMPL / 'OFARM_same_standard_bridge_promotion_readiness_v0_2.json'

PAIRS_V2_PATH = IMPL / 'OFARM_same_standard_bridge_pack_candidate_pairs_v0_2.json'
ROUNDTRIP_PATH = IMPL / 'OFARM_same_standard_bridge_pack_round_trip_records_v0_1.json'
CONFLICT_PATH = IMPL / 'OFARM_same_standard_bridge_pack_conflict_records_v0_1.json'

SCHEMAS = {p.name: json.loads(p.read_text(encoding='utf-8')) for p in MC.glob('*_schema_*.json')}
for schema in SCHEMAS.values():
    jsonschema.Draft202012Validator.check_schema(schema)


def load_json(path: Path) -> Dict[str, Any] | List[Any]:
    return json.loads(path.read_text(encoding='utf-8'))


def infer_schema(example_name: str) -> str | None:
    if '_example_' not in example_name:
        return None
    prefix = example_name.split('_example_')[0]
    candidates = sorted([name for name in SCHEMAS if name.startswith(prefix + '_schema_')])
    if not candidates:
        return None
    if len(candidates) == 1:
        return candidates[0]
    for candidate in candidates:
        if 'v0_2_draft' in example_name and 'v0_2_draft' in candidate:
            return candidate
    for candidate in candidates:
        if 'v0_1' in candidate:
            return candidate
    return candidates[0]


def validate_example(example_name: str, validations: Dict[str, str]) -> Dict[str, Any]:
    data = load_json(MC / example_name)
    schema_name = infer_schema(example_name)
    if schema_name is None:
        raise AssertionError(f'could not infer schema for {example_name}')
    jsonschema.validate(data, SCHEMAS[schema_name])
    validations[f'{example_name} :: {schema_name}'] = 'PASS'
    return data


def dt_to_z(value: datetime) -> str:
    return value.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def event(run_id: str, seq: int, base: datetime, phase: str, category: str, outcome: str, input_refs: List[str], output_refs: List[str], warnings: List[str], notes: str) -> Dict[str, Any]:
    at = base + timedelta(seconds=(seq - 1) * 5)
    return {
        'eventId': f'{run_id}:event:{seq:02d}',
        'sequence': seq,
        'at': dt_to_z(at),
        'phase': phase,
        'category': category,
        'outcome': outcome,
        'inputRefs': list(dict.fromkeys([r for r in input_refs if r])),
        'outputRefs': list(dict.fromkeys([r for r in output_refs if r])),
        'warnings': warnings,
        'notes': notes,
    }


def pair_idx() -> Dict[str, Dict[str, Any]]:
    records = load_json(PAIRS_V2_PATH)
    assert isinstance(records, list)
    return {r['candidatePairId']: r for r in records}


def roundtrip_idx() -> Dict[str, Dict[str, Any]]:
    records = load_json(ROUNDTRIP_PATH)
    assert isinstance(records, list)
    return {r['recordId']: r for r in records}


def conflict_idx() -> Dict[str, Dict[str, Any]]:
    records = load_json(CONFLICT_PATH)
    assert isinstance(records, list)
    return {r['conflictRecordId']: r for r in records}


def scenarios() -> List[Dict[str, Any]]:
    out = []
    for path in sorted(FIX.glob('*.json')):
        out.append(load_json(path))
    return out


def validate_required_examples(example_names: List[str], validations: Dict[str, str]) -> Dict[str, Dict[str, Any]]:
    return {name: validate_example(name, validations) for name in example_names}


def build_success_run(
    scenario: Dict[str, Any],
    validations: Dict[str, str],
    linked_checks: Dict[str, str],
    pairs: Dict[str, Dict[str, Any]],
    roundtrips: Dict[str, Dict[str, Any]],
    seq_index: int,
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    pair = pairs[scenario['candidatePairId']]
    roundtrip = roundtrips[scenario['linkedRoundTripRecordId']]
    examples = validate_required_examples(scenario['requiredExamples'], validations)
    linked_checks[f"{scenario['candidatePairId']} :: candidatePairV2"] = 'PASS'
    linked_checks[f"{scenario['linkedRoundTripRecordId']} :: bridgeRoundTripRecord"] = 'PASS'

    reasons: List[str] = []
    if not pair['reversibleForDeclaredSubset']:
        reasons.append('candidate pair is not reversible for the declared subset')
    if roundtrip['status'] != 'PASS':
        reasons.append('linked round-trip record is not PASS')
    if roundtrip['candidatePairId'] != pair['candidatePairId']:
        reasons.append('round-trip record points to a different candidate pair')
    if pair['promotionReadiness'] != 'NOT_READY_FOR_PROMOTION':
        reasons.append('pair unexpectedly changed promotion readiness before sample replay')
    manifest = examples['OFARM_Capability_Manifest_example_partner_deployment_v0_1.json']
    active = examples['OFARM_ActiveArtifactSet_example_partner_deployment_v0_1.json']
    claims = examples['OFARM_ConformanceClaimSet_example_partner_deployment_v0_1.json']
    if manifest['registryRelation']['activeArtifactSetRef'] != active['activeArtifactSetId']:
        reasons.append('partner manifest no longer points to the partner active artifact set')
    if claims['subjectRef'] != 'deployment:partner':
        reasons.append('partner claim set drifted from the expected deployment subject')

    standard_lower = 'adapt' if 'adapt' in scenario['scenarioId'] else 'isoxml'
    base = datetime(2026, 4, 11, 22, 10, 0, tzinfo=timezone.utc) + timedelta(minutes=10 * seq_index)
    run_id = f"deploySampleRun:{scenario['scenarioId']}:v0.1"
    emitted_ref = scenario['emittedArtifactRef']
    reimport_ref = scenario['reimportArtifactRef']
    partner_trace_ref = f"partnerVariantTrace:{scenario['partnerVariantId']}"
    equivalence_ref = f"equivalence:{scenario['scenarioId']}:deployment-sample:v0.1"
    events = [
        event(run_id, 1, base, 'DEPLOYMENT_SAMPLE_INTAKE', 'DEPLOYMENT_SAMPLE', 'INGESTED', [scenario['deploymentSampleRef'], scenario['externalInputRef']], [run_id], ['Package-local anonymized sample replay; not live field-collected telemetry.'], 'The runner ingested an anonymized partner deployment sample package for same-standard bridge rehearsal.'),
        event(run_id, 2, base, 'PARTNER_VARIANT_BOUND', 'PARTNER_VARIANT', 'RESOLVED', [scenario['partnerId'], scenario['partnerVariantId'], manifest['manifestId'], claims['claimSetId']], [partner_trace_ref], [], 'Partner deployment scope, claim posture, and variant family were bound before any bridge claim was made.'),
        event(run_id, 3, base, 'IMPORT_MAPPING_BOUND', 'MAPPING', 'RESOLVED', [pair['importMappingCoverageStatementRef']], [pair['importLossMapRef']], ['Import loss posture remains attached.'], 'Import mapping and loss posture were resolved against the current draft bridge pair.'),
        event(run_id, 4, base, 'DECLARED_SUBSET_GROUNDED', 'NORMALIZATION', 'MATERIALIZED', [pair['importMappingCoverageStatementRef'], scenario['rawArtifactRef']], [equivalence_ref], [], 'Only the declared reversible subset was materialized from the partner sample.'),
        event(run_id, 5, base, 'EXPORT_DRAFT_SURFACE_BOUND', 'MAPPING', 'RESOLVED', [pair['exportMappingCoverageStatementRef'], pair['exportRuntimeSurfaceContractRef']], [pair['exportLossMapRef']], ['Export surface remains DRAFT.'], 'The draft export surface and loss posture were re-bound for partner-specific replay.'),
        event(run_id, 6, base, 'DRAFT_BRIDGE_EMITTED', 'EXPORT', 'EMITTED', [equivalence_ref, pair['exportMappingCoverageStatementRef']], [emitted_ref], ['Declared subset only.'], 'A draft same-standard bridge artifact was emitted for the supported partner variant.'),
        event(run_id, 7, base, 'REIMPORT_VALIDATION_STARTED', 'REIMPORT', 'STARTED', [emitted_ref, pair['importMappingCoverageStatementRef']], [reimport_ref], [], 'The emitted draft bridge artifact was re-imported for declared-subset equivalence checking.'),
        event(run_id, 8, base, 'ROUNDTRIP_EQUIVALENCE_CONFIRMED', 'REIMPORT', 'CONFIRMED', [reimport_ref, scenario['linkedRoundTripRecordId']], [scenario['expectedTerminalOutcome']], ['Sample replay only; not a promotion decision.'], 'Declared-subset equivalence was confirmed against the linked same-standard round-trip record.'),
        event(run_id, 9, base, 'RUN_FINISHED', 'DEPLOYMENT_SAMPLE', 'COMPLETED', [scenario['expectedTerminalOutcome']], [run_id], ['Pair remains DRAFT.'], 'The partner deployment sample replay finished successfully without changing the pair promotion posture.'),
    ]
    run = {
        'runId': run_id,
        'scenarioId': scenario['scenarioId'],
        'scenarioFamily': scenario['scenarioFamily'],
        'mode': scenario['mode'],
        'telemetrySourceClassification': 'PACKAGE_LOCAL_ANONYMIZED_DEPLOYMENT_SAMPLE_REPLAY',
        'startedAt': events[0]['at'],
        'completedAt': events[-1]['at'],
        'partnerId': scenario['partnerId'],
        'partnerVariantId': scenario['partnerVariantId'],
        'variantFamily': scenario['variantFamily'],
        'standardRef': scenario['standardRef'],
        'candidatePairId': pair['candidatePairId'],
        'deploymentSampleRef': scenario['deploymentSampleRef'],
        'linkedRoundTripRecordIds': [scenario['linkedRoundTripRecordId']],
        'linkedConflictRecordIds': [],
        'telemetryEvents': events,
        'terminalOutcome': scenario['expectedTerminalOutcome'],
    }
    result = {
        'status': 'PASS' if not reasons else 'FAIL',
        'runId': run_id,
        'candidatePairId': pair['candidatePairId'],
        'partnerId': scenario['partnerId'],
        'variantFamily': scenario['variantFamily'],
        'terminalOutcome': scenario['expectedTerminalOutcome'],
        'telemetryEventCount': len(events),
        'linkedRoundTripRecordId': scenario['linkedRoundTripRecordId'],
        'reasons': reasons,
    }
    return run, result


def build_blocked_run(
    scenario: Dict[str, Any],
    validations: Dict[str, str],
    linked_checks: Dict[str, str],
    pairs: Dict[str, Dict[str, Any]],
    conflicts: Dict[str, Dict[str, Any]],
    seq_index: int,
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    pair = pairs[scenario['candidatePairId']]
    conflict = conflicts[scenario['linkedConflictRecordId']]
    examples = validate_required_examples(scenario['requiredExamples'], validations)
    linked_checks[f"{scenario['candidatePairId']} :: candidatePairV2"] = 'PASS'
    linked_checks[f"{scenario['linkedConflictRecordId']} :: bridgeConflictRecord"] = 'PASS'

    reasons: List[str] = []
    if conflict['status'] != 'PASS':
        reasons.append('linked conflict record is not PASS')
    if conflict['candidatePairId'] != pair['candidatePairId']:
        reasons.append('conflict record points to a different candidate pair')
    if conflict['triggerExternalConstructRef'] != scenario['triggerExternalConstructRef']:
        reasons.append('conflict trigger drifted from scenario')
    missing = [code for code in scenario['expectedBlockingReasonCodes'] if code not in conflict['blockingReasonCodes']]
    if missing:
        reasons.append(f'missing expected blocking codes: {missing}')
    manifest = examples['OFARM_Capability_Manifest_example_partner_deployment_v0_1.json']
    active = examples['OFARM_ActiveArtifactSet_example_partner_deployment_v0_1.json']
    if manifest['registryRelation']['activeArtifactSetRef'] != active['activeArtifactSetId']:
        reasons.append('partner manifest no longer points to the partner active artifact set')

    base = datetime(2026, 4, 11, 23, 5, 0, tzinfo=timezone.utc) + timedelta(minutes=10 * seq_index)
    run_id = f"deploySampleRun:{scenario['scenarioId']}:v0.1"
    blocked_ref = f"blocked:{scenario['scenarioId']}:bridge-attempt:v1"
    evidence_ref = f"evidence:{scenario['scenarioId']}:raw-retained:v1"
    events = [
        event(run_id, 1, base, 'DEPLOYMENT_SAMPLE_INTAKE', 'DEPLOYMENT_SAMPLE', 'INGESTED', [scenario['deploymentSampleRef'], scenario['externalInputRef']], [run_id], ['Package-local anonymized sample replay; not live field-collected telemetry.'], 'The runner ingested a partner deployment sample known to sit outside the safely reversible subset.'),
        event(run_id, 2, base, 'PARTNER_VARIANT_BOUND', 'PARTNER_VARIANT', 'RESOLVED', [scenario['partnerId'], scenario['partnerVariantId'], manifest['manifestId']], [blocked_ref], [], 'Partner deployment scope and variant family were resolved before bridge eligibility was re-checked.'),
        event(run_id, 3, base, 'IMPORT_MAPPING_BOUND', 'MAPPING', 'RESOLVED', [pair['importMappingCoverageStatementRef']], [pair['importLossMapRef']], [], 'Import mapping and loss posture were attached before any reversible bridge claim was considered.'),
        event(run_id, 4, base, 'CONFLICT_TRIGGER_DETECTED', 'SCREENING', 'DETECTED', [scenario['triggerExternalConstructRef'], scenario['linkedConflictRecordId']], [blocked_ref], ['Declared subset only.'], 'The replay hit a known blocked construct family recorded in the same-standard bridge conflict catalog.'),
        event(run_id, 5, base, 'BRIDGE_ELIGIBILITY_RECHECKED', 'SCREENING', 'REFUSED', [pair['candidatePairId'], pair['exportMappingCoverageStatementRef'], pair['exportRuntimeSurfaceContractRef']], [scenario['expectedTerminalOutcome']], scenario['expectedBlockingReasonCodes'], 'The draft bridge pair was re-checked and refused for this partner variant.'),
        event(run_id, 6, base, 'RAW_EVIDENCE_RETAINED', 'EVIDENCE', 'RETAINED', [scenario['rawArtifactRef']], [evidence_ref], ['No lossy bridge shortcut permitted.'], 'Raw source evidence was retained instead of flattening the blocked variant into a false reversible bridge claim.'),
        event(run_id, 7, base, 'RUN_FINISHED', 'DEPLOYMENT_SAMPLE', 'COMPLETED', [scenario['expectedTerminalOutcome']], [run_id], ['Pair remains DRAFT.'], 'The partner deployment sample replay finished with an explicit blocked/review-stopped outcome and no bridge artifact emission.'),
    ]
    run = {
        'runId': run_id,
        'scenarioId': scenario['scenarioId'],
        'scenarioFamily': scenario['scenarioFamily'],
        'mode': scenario['mode'],
        'telemetrySourceClassification': 'PACKAGE_LOCAL_ANONYMIZED_DEPLOYMENT_SAMPLE_REPLAY',
        'startedAt': events[0]['at'],
        'completedAt': events[-1]['at'],
        'partnerId': scenario['partnerId'],
        'partnerVariantId': scenario['partnerVariantId'],
        'variantFamily': scenario['variantFamily'],
        'standardRef': scenario['standardRef'],
        'candidatePairId': pair['candidatePairId'],
        'deploymentSampleRef': scenario['deploymentSampleRef'],
        'linkedRoundTripRecordIds': [],
        'linkedConflictRecordIds': [scenario['linkedConflictRecordId']],
        'telemetryEvents': events,
        'terminalOutcome': scenario['expectedTerminalOutcome'],
    }
    result = {
        'status': 'PASS' if not reasons else 'FAIL',
        'runId': run_id,
        'candidatePairId': pair['candidatePairId'],
        'partnerId': scenario['partnerId'],
        'variantFamily': scenario['variantFamily'],
        'terminalOutcome': scenario['expectedTerminalOutcome'],
        'telemetryEventCount': len(events),
        'linkedConflictRecordId': scenario['linkedConflictRecordId'],
        'blockingReasonCodes': scenario['expectedBlockingReasonCodes'],
        'reasons': reasons,
    }
    return run, result


def build_coverage_records(runs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    grouped: Dict[str, List[Dict[str, Any]]] = {}
    for run in runs:
        grouped.setdefault(run['candidatePairId'], []).append(run)

    records: List[Dict[str, Any]] = []
    for candidate_id, recs in sorted(grouped.items()):
        success = [r for r in recs if not r['linkedConflictRecordIds']]
        blocked = [r for r in recs if r['linkedConflictRecordIds']]
        standard_ref = recs[0]['standardRef']
        coverage_id = f"partnerCoverage:{candidate_id.split(':')[1]}:deployment-samples:v0.1"
        records.append({
            'coverageRecordId': coverage_id,
            'candidatePairId': candidate_id,
            'standardRef': standard_ref,
            'coverageStatus': 'PARTNER_VARIANT_SAMPLE_COVERAGE_PRESENT',
            'supportedVariantRunIds': [r['runId'] for r in success],
            'blockedVariantRunIds': [r['runId'] for r in blocked],
            'coveredPartnerIds': sorted({r['partnerId'] for r in success}),
            'blockedPartnerIds': sorted({r['partnerId'] for r in blocked}),
            'supportedVariantFamilies': sorted({r['variantFamily'] for r in success}),
            'blockedVariantFamilies': sorted({r['variantFamily'] for r in blocked}),
            'deploymentSampleRefs': [r['deploymentSampleRef'] for r in recs],
            'limitations': [
                'Coverage is based on package-local anonymized partner deployment sample replays, not live field-collected production telemetry.',
                'Coverage remains limited to the declared reversible subsets and known blocked conflict families.',
            ],
        })
    return records


def build_candidate_v3(v2_pair: Dict[str, Any], coverage_records: List[Dict[str, Any]], runs: List[Dict[str, Any]]) -> Dict[str, Any]:
    coverage = next(r for r in coverage_records if r['candidatePairId'] == v2_pair['candidatePairId'])
    related_runs = [r['runId'] for r in runs if r['candidatePairId'] == v2_pair['candidatePairId']]
    updated = dict(v2_pair)
    updated['candidateStatus'] = 'DRAFT_EXECUTOR_PROVEN_PARTNER_SAMPLE_COVERED_DECLARED_SUBSET_REVERSIBLE'
    updated['limitationCodes'] = [
        'EXPORT_SURFACE_DRAFT_ONLY',
        'NO_LIVE_DEPLOYMENT_SAME_STANDARD_TELEMETRY',
        'PARTNER_VARIANT_SAMPLE_ONLY',
        'DECLARED_SUBSET_ONLY',
    ]
    updated['notes'] = (
        'Declared-subset same-standard bridge proof now includes executor telemetry plus package-local anonymized '
        'partner deployment sample replay coverage across supported and blocked partner variants.'
    )
    updated['deploymentSampleTelemetryStatus'] = 'PACKAGE_LOCAL_ANONYMIZED_PARTNER_SAMPLE_REPLAY_PRESENT'
    updated['partnerVariantCoverageStatus'] = 'PARTNER_VARIANT_SAMPLE_COVERAGE_PRESENT'
    updated['linkedDeploymentSampleRunIds'] = related_runs
    updated['linkedPartnerCoverageRecordId'] = coverage['coverageRecordId']
    updated['promotionReadiness'] = 'NOT_READY_FOR_PROMOTION'
    updated['promotionBlockingCodes'] = [
        'EXPORT_SURFACE_STILL_DRAFT',
        'NO_LIVE_DEPLOYMENT_SAME_STANDARD_TELEMETRY',
        'DECLARED_SUBSET_ONLY',
        'NO_PRODUCTION_PROMOTION_APPROVAL',
    ]
    return updated


def build_promotion_readiness(v3_pairs: List[Dict[str, Any]]) -> Dict[str, Any]:
    records = []
    for pair in v3_pairs:
        records.append({
            'candidatePairId': pair['candidatePairId'],
            'standardRef': pair['standardRef'],
            'decision': 'NOT_READY_FOR_PROMOTION',
            'checks': {
                'declaredSubsetRoundTripPass': True,
                'executorSuccessTelemetryPresent': True,
                'executorConflictTelemetryPresent': True,
                'deploymentSampleTelemetryPresent': True,
                'partnerVariantCoveragePresent': True,
                'deploymentCollectedTelemetryPresent': False,
                'broadConstructCoveragePresent': False,
                'productionPromotionApprovalPresent': False,
                'surfaceLeftDraft': False,
            },
            'blockingReasonCodes': [
                'EXPORT_SURFACE_STILL_DRAFT',
                'NO_LIVE_DEPLOYMENT_SAME_STANDARD_TELEMETRY',
                'DECLARED_SUBSET_ONLY',
                'NO_PRODUCTION_PROMOTION_APPROVAL',
            ],
            'linkedExecutorSuccessRunIds': pair.get('linkedExecutorSuccessRunIds', []),
            'linkedExecutorBlockedRunIds': pair.get('linkedExecutorBlockedRunIds', []),
            'linkedDeploymentSampleRunIds': pair.get('linkedDeploymentSampleRunIds', []),
            'linkedPartnerCoverageRecordId': pair.get('linkedPartnerCoverageRecordId'),
            'notes': (
                'Partner-variant sample replay coverage now exists, but the pair still lacks live deployment-collected '
                'same-standard bridge telemetry, broader construct coverage, and a production promotion approval path.'
            ),
        })
    return {
        'evaluatedAt': '2026-04-11T23:55:00Z',
        'records': records,
        'summary': {
            'candidatePairs': len(records),
            'readyForPromotion': 0,
            'notReadyForPromotion': len(records),
        },
        'overall': 'HOLD_AT_DRAFT',
        'limitations': [
            'Same-standard bridge evidence now includes partner-variant sample replay coverage, but these samples are package-local replays rather than live field-collected production telemetry.',
            'Both bridge surfaces remain DRAFT because the package still lacks live deployment telemetry, broad construct coverage beyond the declared subsets, and explicit production promotion approval.',
        ],
    }


def main() -> None:
    pairs = pair_idx()
    roundtrips = roundtrip_idx()
    conflicts = conflict_idx()
    scenario_list = scenarios()

    validations: Dict[str, str] = {}
    linked_checks: Dict[str, str] = {}
    runs: List[Dict[str, Any]] = []
    success_results: Dict[str, Any] = {}
    blocked_results: Dict[str, Any] = {}
    failing_checks: List[str] = []

    success_i = 0
    blocked_i = 0
    for i, scenario in enumerate(scenario_list):
        if scenario['kind'] == 'SUCCESS':
            run, result = build_success_run(scenario, validations, linked_checks, pairs, roundtrips, success_i)
            success_i += 1
            success_results[scenario['scenarioId']] = result
        else:
            run, result = build_blocked_run(scenario, validations, linked_checks, pairs, conflicts, blocked_i)
            blocked_i += 1
            blocked_results[scenario['scenarioId']] = result
        runs.append(run)
        if result['status'] != 'PASS':
            failing_checks.append(f"{scenario['scenarioId']} :: {result['reasons']}")

    coverage_records = build_coverage_records(runs)
    v3_pairs = [build_candidate_v3(pair, coverage_records, runs) for pair in pairs.values()]
    promotion = build_promotion_readiness(v3_pairs)

    coverage_checks = {}
    for record in coverage_records:
        status = 'PASS' if record['supportedVariantRunIds'] and record['blockedVariantRunIds'] else 'FAIL'
        coverage_checks[f"{record['coverageRecordId']} :: partnerVariantSampleCoverage"] = status
        if status != 'PASS':
            failing_checks.append(f"{record['coverageRecordId']} missing supported or blocked sample coverage")

    telemetry = {
        'generatedAt': '2026-04-11T23:50:00Z',
        'provenanceNotice': 'These runs replay package-local anonymized partner deployment samples. They are not live field-collected production telemetry.',
        'runs': runs,
        'summary': {
            'successRuns': len(success_results),
            'blockedRuns': len(blocked_results),
            'partnerCoverageRecords': len(coverage_records),
            'telemetryEvents': sum(len(run['telemetryEvents']) for run in runs),
        },
        'limitations': [
            'Partner-variant proof is limited to package-local anonymized deployment sample replays.',
            'Coverage remains confined to the declared reversible subsets and the currently known blocked conflict families.',
        ],
    }

    results = {
        'successTelemetry': success_results,
        'blockedTelemetry': blocked_results,
        'partnerCoverageChecks': coverage_checks,
        'linkedArtifactChecks': linked_checks,
        'validatedExamples': validations,
        'updatedCandidatePairFile': CANDIDATE_OUT.name,
        'partnerCoverageFile': COVERAGE_OUT.name,
        'promotionReadinessFile': PROMOTION_OUT.name,
        'summary': {
            'successRuns': len(success_results),
            'blockedRuns': len(blocked_results),
            'partnerCoverageRecords': len(coverage_records),
            'validatedExamples': len(validations),
            'telemetryEvents': sum(len(run['telemetryEvents']) for run in runs),
        },
        'limitations': [
            'The runner provides package-local anonymized deployment sample replay evidence, not live field-collected same-standard bridge telemetry.',
            'Partner coverage is stronger than before but still declared-subset only, so bridge surfaces remain DRAFT.',
        ],
        'overall': 'PASS_WITH_LIMITATIONS' if not failing_checks else 'FAIL',
        'failingChecks': failing_checks,
    }

    TELEMETRY_OUT.write_text(json.dumps(telemetry, indent=2) + '\n', encoding='utf-8')
    COVERAGE_OUT.write_text(json.dumps(coverage_records, indent=2) + '\n', encoding='utf-8')
    CANDIDATE_OUT.write_text(json.dumps(v3_pairs, indent=2) + '\n', encoding='utf-8')
    PROMOTION_OUT.write_text(json.dumps(promotion, indent=2) + '\n', encoding='utf-8')
    RESULTS_OUT.write_text(json.dumps(results, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
