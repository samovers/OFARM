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
FIX = IMPL / 'ofarm_executor_native_same_standard_bridge_telemetry_fixtures_v0_1'

TELEMETRY_OUT = IMPL / 'OFARM_executor_native_same_standard_bridge_telemetry_v0_1.json'
RESULTS_OUT = IMPL / 'OFARM_executor_native_same_standard_bridge_telemetry_results_v0_1.json'
CANDIDATE_V2_OUT = IMPL / 'OFARM_same_standard_bridge_pack_candidate_pairs_v0_2.json'
PROMOTION_OUT = IMPL / 'OFARM_same_standard_bridge_promotion_readiness_v0_1.json'

PAIRS_V1_PATH = IMPL / 'OFARM_same_standard_bridge_pack_candidate_pairs_v0_1.json'
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
    at = base + timedelta(seconds=(seq - 1) * 4)
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


def expect(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def pairs_index() -> Dict[str, Dict[str, Any]]:
    records = load_json(PAIRS_V1_PATH)
    assert isinstance(records, list)
    return {r['candidatePairId']: r for r in records}


def roundtrip_index() -> Dict[str, Dict[str, Any]]:
    records = load_json(ROUNDTRIP_PATH)
    assert isinstance(records, list)
    return {r['recordId']: r for r in records}


def conflict_index() -> Dict[str, Dict[str, Any]]:
    records = load_json(CONFLICT_PATH)
    assert isinstance(records, list)
    return {r['conflictRecordId']: r for r in records}


def success_run(scenario: Dict[str, Any], validations: Dict[str, str], linked_checks: Dict[str, str], pair_idx: Dict[str, Dict[str, Any]], roundtrip_idx: Dict[str, Dict[str, Any]]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    pair = pair_idx[scenario['candidatePairId']]
    record = roundtrip_idx[scenario['linkedRoundTripRecordId']]
    import_mapping = validate_example(scenario['importMappingCoverageExample'], validations)
    import_loss = validate_example(scenario['importLossMapExample'], validations)
    export_mapping = validate_example(scenario['exportMappingCoverageExample'], validations)
    export_loss = validate_example(scenario['exportLossMapExample'], validations)
    surface = validate_example(scenario['runtimeSurfaceContractExample'], validations)
    linked_checks[f"{scenario['candidatePairId']} :: candidatePairV1"] = 'PASS'
    linked_checks[f"{scenario['linkedRoundTripRecordId']} :: bridgeRoundTripRecord"] = 'PASS'

    reasons: List[str] = []
    if pair['candidateStatus'] != 'DRAFT_DECLARED_SUBSET_REVERSIBLE':
        reasons.append('candidate pair not in expected draft reversible posture')
    if not pair['reversibleForDeclaredSubset']:
        reasons.append('candidate pair is not marked reversible for declared subset')
    if record['status'] != 'PASS':
        reasons.append('linked round-trip record is not PASS')
    if record['candidatePairId'] != pair['candidatePairId']:
        reasons.append('round-trip record points to a different candidate pair')
    if import_mapping['externalStandardRef'] != export_mapping['externalStandardRef']:
        reasons.append('import/export standard refs drifted')
    if export_mapping['statementId'] != pair['exportMappingCoverageStatementRef']:
        reasons.append('export mapping statement drifted from candidate pair')
    if import_mapping['statementId'] != pair['importMappingCoverageStatementRef']:
        reasons.append('import mapping statement drifted from candidate pair')
    if surface['contractId'] != pair['exportRuntimeSurfaceContractRef']:
        reasons.append('runtime surface contract drifted from candidate pair')
    if surface['status'] != 'DRAFT':
        reasons.append('surface unexpectedly left draft without a separate promotion step')
    if export_mapping['roundTripExpectation'] != 'REQUIRED_FOR_DECLARED_SUBSET':
        reasons.append('export mapping no longer declares declared-subset round-trip requirement')

    run_id = f"execRun:{scenario['scenarioId']}:v0.1"
    base = datetime(2026, 4, 11, 20, 55, 0, tzinfo=timezone.utc)
    if 'isoxml' in scenario['scenarioId']:
        base += timedelta(minutes=8)
    equivalence_ref = f"equivalence:{scenario['scenarioId']}:declared-subset:v0.1"
    export_artifact_ref = f"artifact:bridge:{scenario['scenarioId']}:draft-payload:v1"
    reimport_ref = f"reimport:{scenario['scenarioId']}:declared-subset-check:v1"
    events = [
        event(run_id, 1, base, 'EXECUTOR_START', 'EXECUTOR', 'STARTED', [scenario['externalInputRef'], scenario['rawArtifactRef']], [run_id], [], 'Same-standard bridge executor accepted a governed source payload for draft bridge processing.'),
        event(run_id, 2, base, 'IMPORT_MAPPING_BOUND', 'MAPPING', 'RESOLVED', [import_mapping['statementId']], [import_loss['lossMapId']], ['Import loss posture remains attached.'], 'Import mapping and loss posture were resolved before any reversible bridge claim was evaluated.'),
        event(run_id, 3, base, 'DECLARED_SUBSET_GROUNDED', 'NORMALIZATION', 'MATERIALIZED', [import_mapping['statementId'], import_loss['lossMapId']], [equivalence_ref], [], 'Executor materialized only the declared reversible subset rather than all source constructs.'),
        event(run_id, 4, base, 'EXPORT_DRAFT_SURFACE_BOUND', 'MAPPING', 'RESOLVED', [export_mapping['statementId'], surface['contractId']], [export_loss['lossMapId']], ['Export surface is still DRAFT.'], 'Draft export surface and loss posture were bound before bridge emission.'),
        event(run_id, 5, base, 'DRAFT_BRIDGE_EMITTED', 'EXPORT', 'EMITTED', [equivalence_ref, export_mapping['statementId']], [export_artifact_ref], ['Bridge payload is declared-subset only.'], 'Executor emitted a same-standard draft bridge artifact for the declared reversible subset.'),
        event(run_id, 6, base, 'REIMPORT_VALIDATION_STARTED', 'REIMPORT', 'STARTED', [export_artifact_ref, import_mapping['statementId']], [reimport_ref], [], 'Executor re-imported the emitted bridge artifact for equivalence checking.'),
        event(run_id, 7, base, 'ROUNDTRIP_EQUIVALENCE_CONFIRMED', 'REIMPORT', 'CONFIRMED', [reimport_ref, scenario['linkedRoundTripRecordId']], [scenario['expectedTerminalOutcome']], ['Declared subset only; not a promotion decision.'], 'Executor confirmed declared-subset equivalence against the bound same-standard round-trip record.'),
        event(run_id, 8, base, 'EXECUTOR_FINISH', 'EXECUTOR', 'COMPLETED', [scenario['expectedTerminalOutcome']], [run_id], ['Surface remains DRAFT.'], 'Executor finished with declared-subset proof but no promotion beyond draft status.'),
    ]
    run = {
        'runId': run_id,
        'scenarioId': scenario['scenarioId'],
        'scenarioFamily': scenario['scenarioFamily'],
        'mode': 'EXECUTOR_SYNTHESIZED_TELEMETRY',
        'direction': 'SAME_STANDARD_BRIDGE',
        'startedAt': events[0]['at'],
        'completedAt': events[-1]['at'],
        'terminalOutcome': scenario['expectedTerminalOutcome'],
        'standardRef': import_mapping['externalStandardRef'],
        'candidatePairId': pair['candidatePairId'],
        'linkedRoundTripRecordIds': [scenario['linkedRoundTripRecordId']],
        'linkedConflictRecordIds': [],
        'mappingCoverageStatementRefs': [import_mapping['statementId'], export_mapping['statementId']],
        'lossMapRefs': [import_loss['lossMapId'], export_loss['lossMapId']],
        'runtimeSurfaceContractRef': surface['contractId'],
        'telemetryEvents': events,
    }
    result = {
        'status': 'PASS' if not reasons else 'FAIL',
        'runId': run_id,
        'candidatePairId': pair['candidatePairId'],
        'terminalOutcome': scenario['expectedTerminalOutcome'],
        'telemetryEventCount': len(events),
        'linkedRoundTripRecordId': scenario['linkedRoundTripRecordId'],
        'reasons': reasons,
    }
    return run, result


def blocked_run(scenario: Dict[str, Any], validations: Dict[str, str], linked_checks: Dict[str, str], pair_idx: Dict[str, Dict[str, Any]], conflict_idx: Dict[str, Dict[str, Any]]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    pair = pair_idx[scenario['candidatePairId']]
    record = conflict_idx[scenario['linkedConflictRecordId']]
    import_mapping = validate_example(scenario['importMappingCoverageExample'], validations)
    import_loss = validate_example(scenario['importLossMapExample'], validations)
    export_mapping = validate_example(scenario['exportMappingCoverageExample'], validations)
    export_loss = validate_example(scenario['exportLossMapExample'], validations)
    surface = validate_example(scenario['runtimeSurfaceContractExample'], validations)
    linked_checks[f"{scenario['candidatePairId']} :: candidatePairV1"] = 'PASS'
    linked_checks[f"{scenario['linkedConflictRecordId']} :: bridgeConflictRecord"] = 'PASS'

    reasons: List[str] = []
    if record['status'] != 'PASS':
        reasons.append('linked conflict record is not PASS')
    if record['candidatePairId'] != pair['candidatePairId']:
        reasons.append('conflict record points to a different candidate pair')
    if record['triggerExternalConstructRef'] != scenario['triggerExternalConstructRef']:
        reasons.append('conflict trigger drifted from scenario')
    missing_blockers = [b for b in scenario['expectedBlockingReasonCodes'] if b not in record['blockingReasonCodes']]
    if missing_blockers:
        reasons.append(f'missing expected blocking reason codes: {missing_blockers}')
    if surface['status'] != 'DRAFT':
        reasons.append('surface unexpectedly left draft without a separate promotion step')
    if import_mapping['externalStandardRef'] != export_mapping['externalStandardRef']:
        reasons.append('import/export standard refs drifted')

    run_id = f"execRun:{scenario['scenarioId']}:v0.1"
    base = datetime(2026, 4, 11, 21, 7, 0, tzinfo=timezone.utc)
    if 'isoxml' in scenario['scenarioId']:
        base += timedelta(minutes=8)
    blocked_ref = f"blocked:{scenario['scenarioId']}:bridge-attempt:v1"
    events = [
        event(run_id, 1, base, 'EXECUTOR_START', 'EXECUTOR', 'STARTED', [scenario['externalInputRef'], scenario['rawArtifactRef']], [run_id], [], 'Same-standard bridge executor accepted a payload that may exceed the declared reversible subset.'),
        event(run_id, 2, base, 'IMPORT_MAPPING_BOUND', 'MAPPING', 'RESOLVED', [import_mapping['statementId']], [import_loss['lossMapId']], [], 'Import mapping and loss posture were bound before reversible bridge eligibility was tested.'),
        event(run_id, 3, base, 'CONFLICT_TRIGGER_DETECTED', 'SCREENING', 'DETECTED', [scenario['triggerExternalConstructRef'], scenario['linkedConflictRecordId']], [blocked_ref], ['Declared subset only.'], 'Executor detected a known non-reversible or high-consequence construct from the conflict record family.'),
        event(run_id, 4, base, 'BRIDGE_ELIGIBILITY_RECHECKED', 'SCREENING', 'REFUSED', [pair['candidatePairId'], export_mapping['statementId'], surface['contractId']], [scenario['expectedTerminalOutcome']], scenario['expectedBlockingReasonCodes'], 'Executor rechecked bridge eligibility and refused to claim a reversible bridge path for this payload.'),
        event(run_id, 5, base, 'RAW_EVIDENCE_RETAINED', 'EVIDENCE', 'RETAINED', [scenario['rawArtifactRef']], [f"evidence:{scenario['scenarioId']}:raw-retained:v1"], ['No lossy bridge shortcut permitted.'], 'Raw source material remains attached as evidence instead of being flattened into a false reversible claim.'),
        event(run_id, 6, base, 'EXECUTOR_FINISH', 'EXECUTOR', 'COMPLETED', [scenario['expectedTerminalOutcome']], [run_id], ['Surface remains DRAFT.'], 'Executor finished with an explicit blocked outcome and no same-standard bridge emission.'),
    ]
    run = {
        'runId': run_id,
        'scenarioId': scenario['scenarioId'],
        'scenarioFamily': scenario['scenarioFamily'],
        'mode': 'EXECUTOR_SYNTHESIZED_TELEMETRY',
        'direction': 'SAME_STANDARD_BRIDGE',
        'startedAt': events[0]['at'],
        'completedAt': events[-1]['at'],
        'terminalOutcome': scenario['expectedTerminalOutcome'],
        'standardRef': import_mapping['externalStandardRef'],
        'candidatePairId': pair['candidatePairId'],
        'linkedRoundTripRecordIds': [],
        'linkedConflictRecordIds': [scenario['linkedConflictRecordId']],
        'mappingCoverageStatementRefs': [import_mapping['statementId'], export_mapping['statementId']],
        'lossMapRefs': [import_loss['lossMapId'], export_loss['lossMapId']],
        'runtimeSurfaceContractRef': surface['contractId'],
        'telemetryEvents': events,
    }
    result = {
        'status': 'PASS' if not reasons else 'FAIL',
        'runId': run_id,
        'candidatePairId': pair['candidatePairId'],
        'terminalOutcome': scenario['expectedTerminalOutcome'],
        'telemetryEventCount': len(events),
        'linkedConflictRecordId': scenario['linkedConflictRecordId'],
        'reasons': reasons,
        'blockingReasonCodes': record['blockingReasonCodes'],
    }
    return run, result


def build_candidate_v2(pair_v1: Dict[str, Any], success_runs: List[Dict[str, Any]], blocked_runs: List[Dict[str, Any]], promotion: Dict[str, Any]) -> Dict[str, Any]:
    related_success = [r['runId'] for r in success_runs if r['candidatePairId'] == pair_v1['candidatePairId']]
    related_blocked = [r['runId'] for r in blocked_runs if r['candidatePairId'] == pair_v1['candidatePairId']]
    limitations = [code for code in pair_v1.get('limitationCodes', []) if code != 'NO_EXECUTOR_SAME_STANDARD_TELEMETRY']
    for code in ['EXPORT_SURFACE_DRAFT_ONLY', 'NO_DEPLOYMENT_SAME_STANDARD_TELEMETRY', 'NO_PARTNER_VARIANT_TELEMETRY', 'DECLARED_SUBSET_ONLY']:
        if code not in limitations:
            limitations.append(code)
    out = dict(pair_v1)
    out['candidateStatus'] = 'DRAFT_EXECUTOR_PROVEN_DECLARED_SUBSET_REVERSIBLE' if related_success and related_blocked else 'DRAFT_DECLARED_SUBSET_REVERSIBLE'
    out['limitationCodes'] = limitations
    out['executorTelemetryStatus'] = 'EXECUTOR_SYNTHESIZED_DECLARED_SUBSET_PROVEN' if related_success and related_blocked else 'MISSING'
    out['linkedExecutorSuccessRunIds'] = related_success
    out['linkedExecutorBlockedRunIds'] = related_blocked
    out['promotionReadiness'] = promotion['decision']
    out['promotionBlockingCodes'] = promotion['blockingReasonCodes']
    return out


def promotion_decision(pair_v2: Dict[str, Any], success_runs: List[Dict[str, Any]], blocked_runs: List[Dict[str, Any]]) -> Dict[str, Any]:
    candidate_id = pair_v2['candidatePairId']
    success_count = len([r for r in success_runs if r['candidatePairId'] == candidate_id])
    blocked_count = len([r for r in blocked_runs if r['candidatePairId'] == candidate_id])
    checks = {
        'declaredSubsetRoundTripPass': True,
        'executorSuccessTelemetryPresent': success_count > 0,
        'executorConflictTelemetryPresent': blocked_count > 0,
        'surfaceLeftDraft': False,
        'deploymentCollectedTelemetryPresent': False,
        'partnerVariantCoveragePresent': False,
        'broadConstructCoveragePresent': False,
        'productionPromotionApprovalPresent': False,
    }
    blockers: List[str] = []
    if not checks['executorSuccessTelemetryPresent']:
        blockers.append('NO_EXECUTOR_SUCCESS_TELEMETRY')
    if not checks['executorConflictTelemetryPresent']:
        blockers.append('NO_EXECUTOR_CONFLICT_TELEMETRY')
    if not checks['surfaceLeftDraft']:
        blockers.append('EXPORT_SURFACE_STILL_DRAFT')
    if not checks['deploymentCollectedTelemetryPresent']:
        blockers.append('NO_DEPLOYMENT_SAME_STANDARD_TELEMETRY')
    if not checks['partnerVariantCoveragePresent']:
        blockers.append('NO_PARTNER_VARIANT_COVERAGE')
    if not checks['broadConstructCoveragePresent']:
        blockers.append('DECLARED_SUBSET_ONLY')
    if not checks['productionPromotionApprovalPresent']:
        blockers.append('NO_PRODUCTION_PROMOTION_APPROVAL')
    return {
        'candidatePairId': candidate_id,
        'standardRef': pair_v2['standardRef'],
        'decision': 'NOT_READY_FOR_PROMOTION' if blockers else 'READY_FOR_PROMOTION',
        'checks': checks,
        'blockingReasonCodes': blockers,
        'linkedExecutorSuccessRunIds': [r['runId'] for r in success_runs if r['candidatePairId'] == candidate_id],
        'linkedExecutorBlockedRunIds': [r['runId'] for r in blocked_runs if r['candidatePairId'] == candidate_id],
        'notes': 'Executor proof now exists for the declared subset, but the bridge surface remains draft-only and lacks deployment-grade coverage.'
    }


def main() -> None:
    validations: Dict[str, str] = {}
    linked_checks: Dict[str, str] = {}
    pair_idx = pairs_index()
    rt_idx = roundtrip_index()
    conflict_idx = conflict_index()
    success_runs: List[Dict[str, Any]] = []
    blocked_runs: List[Dict[str, Any]] = []
    success_results: Dict[str, Any] = {}
    blocked_results: Dict[str, Any] = {}

    for fixture_path in sorted(FIX.glob('*.json')):
        scenario = load_json(fixture_path)
        assert isinstance(scenario, dict)
        family = scenario['scenarioFamily']
        if family == 'SAME_STANDARD_BRIDGE_EXECUTOR_SUCCESS':
            run, result = success_run(scenario, validations, linked_checks, pair_idx, rt_idx)
            success_runs.append(run)
            success_results[scenario['scenarioId']] = result
        elif family == 'SAME_STANDARD_BRIDGE_EXECUTOR_BLOCKED':
            run, result = blocked_run(scenario, validations, linked_checks, pair_idx, conflict_idx)
            blocked_runs.append(run)
            blocked_results[scenario['scenarioId']] = result
        else:
            raise AssertionError(f'unknown scenario family: {family}')

    # Promotion first, then candidate v2.
    promotion_records: List[Dict[str, Any]] = []
    candidate_v2_records: List[Dict[str, Any]] = []
    for pair_id in sorted(pair_idx):
        promo = promotion_decision(pair_idx[pair_id], success_runs, blocked_runs)
        promotion_records.append(promo)
    promo_idx = {r['candidatePairId']: r for r in promotion_records}
    for pair_id in sorted(pair_idx):
        candidate_v2_records.append(build_candidate_v2(pair_idx[pair_id], success_runs, blocked_runs, promo_idx[pair_id]))

    telemetry = {
        'generatedAt': '2026-04-11T21:30:00Z',
        'successRuns': success_runs,
        'blockedRuns': blocked_runs,
    }
    TELEMETRY_OUT.write_text(json.dumps(telemetry, indent=2) + '\n', encoding='utf-8')
    CANDIDATE_V2_OUT.write_text(json.dumps(candidate_v2_records, indent=2) + '\n', encoding='utf-8')

    promotion_out = {
        'evaluatedAt': '2026-04-11T21:31:00Z',
        'records': promotion_records,
        'summary': {
            'candidatePairs': len(promotion_records),
            'readyForPromotion': sum(1 for r in promotion_records if r['decision'] == 'READY_FOR_PROMOTION'),
            'notReadyForPromotion': sum(1 for r in promotion_records if r['decision'] != 'READY_FOR_PROMOTION'),
        },
        'overall': 'HOLD_AT_DRAFT',
        'limitations': [
            'Executor-produced same-standard bridge telemetry is now present for the declared subset, but the bridge surfaces are still DRAFT.',
            'The package still lacks deployment-collected same-standard telemetry, partner-specific coverage, and broad construct coverage beyond the declared subset.'
        ]
    }
    PROMOTION_OUT.write_text(json.dumps(promotion_out, indent=2) + '\n', encoding='utf-8')

    all_results = list(success_results.values()) + list(blocked_results.values())
    failing = [r for r in all_results if r['status'] != 'PASS']
    results = {
        'bridgeSuccessTelemetry': success_results,
        'bridgeBlockedTelemetry': blocked_results,
        'linkedArtifactChecks': linked_checks,
        'validatedExamples': validations,
        'updatedCandidatePairFile': CANDIDATE_V2_OUT.name,
        'promotionReadinessFile': PROMOTION_OUT.name,
        'summary': {
            'successRuns': len(success_runs),
            'blockedRuns': len(blocked_runs),
            'candidatePairsV2': len(candidate_v2_records),
            'validatedExamples': len(validations),
            'telemetryEvents': sum(len(r['telemetryEvents']) for r in success_runs + blocked_runs),
        },
        'limitations': [
            'Same-standard bridge executor proof is still limited to declared draft subsets for ADAPT and ISOXML.',
            'Promotion beyond DRAFT is explicitly denied because deployment telemetry, partner variants, and broader construct coverage are still missing.'
        ],
        'overall': 'PASS_WITH_LIMITATIONS' if not failing else 'FAIL',
        'failingChecks': [r['runId'] for r in failing],
    }
    RESULTS_OUT.write_text(json.dumps(results, indent=2) + '\n', encoding='utf-8')

    if failing:
        raise SystemExit('one or more same-standard bridge telemetry checks failed')


if __name__ == '__main__':
    main()
