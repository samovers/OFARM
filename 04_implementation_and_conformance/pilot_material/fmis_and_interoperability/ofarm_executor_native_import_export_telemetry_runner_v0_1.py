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
FIX = IMPL / 'ofarm_executor_native_import_export_telemetry_fixtures_v0_1'

TELEMETRY_OUT = IMPL / 'OFARM_executor_native_import_export_telemetry_v0_1.json'
RESULTS_OUT = IMPL / 'OFARM_executor_native_import_export_telemetry_results_v0_1.json'

ROUNDTRIP_PATH = IMPL / 'OFARM_mapping_round_trip_records_v0_1.json'
TRACEBACK_PATH = IMPL / 'OFARM_output_adapter_trace_back_records_v0_1.json'

SCHEMAS = {p.name: json.loads(p.read_text(encoding='utf-8')) for p in MC.glob('*_schema_*.json')}
for schema in SCHEMAS.values():
    jsonschema.Draft202012Validator.check_schema(schema)

SCENARIOS = sorted(p.name for p in FIX.glob('*.json'))


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


def parse_dt(value: str) -> datetime:
    if value.endswith('Z'):
        value = value[:-1] + '+00:00'
    return datetime.fromisoformat(value).astimezone(timezone.utc)


def dt_to_z(value: datetime) -> str:
    return value.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def event(run_id: str, seq: int, base: datetime, phase: str, category: str, outcome: str, input_refs: List[str], output_refs: List[str], warnings: List[str], notes: str) -> Dict[str, Any]:
    at = base + timedelta(seconds=(seq - 1) * 3)
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


def expect(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


def roundtrip_index() -> Dict[str, Dict[str, Any]]:
    records = load_json(ROUNDTRIP_PATH)
    assert isinstance(records, list)
    return {r['recordId']: r for r in records}


def traceback_index() -> Dict[str, Dict[str, Any]]:
    records = load_json(TRACEBACK_PATH)
    assert isinstance(records, list)
    return {r['traceBackId']: r for r in records}


def base_time_from_data(candidates: List[Dict[str, Any]], fallback: datetime) -> datetime:
    found: List[datetime] = []
    for data in candidates:
        for key in ('requestedAt', 'evaluatedAt', 'generatedAt', 'frozenAt'):
            if isinstance(data.get(key), str) and 'T' in data[key]:
                try:
                    found.append(parse_dt(data[key]))
                except Exception:
                    pass
    return min(found) if found else fallback


def import_run(scenario: Dict[str, Any], validations: Dict[str, str], linked_checks: Dict[str, str], record_idx: Dict[str, Dict[str, Any]]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    mapping = validate_example(scenario['mappingCoverageExample'], validations)
    loss = validate_example(scenario['lossMapExample'], validations)
    rt = record_idx[scenario['linkedRoundTripRecordId']]
    linked_checks[f"{scenario['linkedRoundTripRecordId']} :: roundTripRecord"] = 'PASS'

    reasons: List[str] = []
    expect(mapping['direction'] == 'IMPORT', 'import run must bind import mapping')
    if loss['mappingCoverageStatementRef'] != mapping['statementId']:
        reasons.append('loss map does not point to bound mapping coverage statement')
    if mapping['promotionPosture']['autoPromotionAllowed'] is not False:
        reasons.append('import mapping unexpectedly allows auto-promotion')
    if mapping['promotionPosture']['requiresReviewForAcceptedConsequences'] is not True:
        reasons.append('import mapping must require review for accepted consequences')
    if mapping['promotionPosture']['defaultCommitClasses'] != scenario['expectedDefaultCommitClasses']:
        reasons.append('default commit classes drifted from expected evidence-first posture')
    if rt['mappingCoverageStatementRef'] != mapping['statementId']:
        reasons.append('linked round-trip record does not match mapping statement')
    if rt['lossMapRef'] != loss['lossMapId']:
        reasons.append('linked round-trip record does not match loss map')

    run_id = f"execRun:{scenario['scenarioId']}:v0.1"
    base = datetime(2026, 4, 11, 13, 0, 0, tzinfo=timezone.utc)
    if 'adapt' not in scenario['scenarioId']:
        base += timedelta(minutes=5)
    elevated_warning = 'MATERIAL loss posture retained; accepted consequence remains review-gated.' if loss['overallLossPosture'] == 'MATERIAL' else 'Loss posture retained for downstream review visibility.'
    review_ref = f"review:{scenario['scenarioId']}:accepted-consequence-gate"
    normalized_refs = [
        f"normalized:{scenario['scenarioId']}:observation-assertion",
        f"normalized:{scenario['scenarioId']}:operation-claim",
        f"normalized:{scenario['scenarioId']}:evidence-record",
    ]
    events = [
        event(run_id, 1, base, 'EXECUTOR_START', 'EXECUTOR', 'STARTED', [scenario['externalInputRef'], scenario['rawArtifactRef']], [run_id], [], 'Import executor accepted a raw external payload for governed normalization.'),
        event(run_id, 2, base, 'SOURCE_PAYLOAD_BOUND', 'INGEST', 'BOUND', [scenario['rawArtifactRef']], [mapping['externalStandardRef']], [], 'Raw inbound artifact is bound to the declared external standard family.'),
        event(run_id, 3, base, 'MAPPING_COVERAGE_RESOLVED', 'MAPPING', 'RESOLVED', [mapping['mappingModuleRef']], [mapping['statementId']], [], 'Executor resolved the declared mapping coverage statement before any semantic promotion.'),
        event(run_id, 4, base, 'LOSS_POSTURE_ATTACHED', 'MAPPING', 'DISCLOSED', [mapping['statementId']], [loss['lossMapId']], [elevated_warning], 'Loss map is attached into the executor telemetry stream so downstream consumers cannot treat the import as lossless.'),
        event(run_id, 5, base, 'NORMALIZATION_TARGETS_EMITTED', 'NORMALIZATION', 'EMITTED', [mapping['statementId']], normalized_refs, [], 'Executor emitted only claim/evidence-first normalized artifacts.'),
        event(run_id, 6, base, 'COMMIT_POSTURE_EVALUATED', 'PROMOTION', 'REVIEW_REQUIRED', normalized_refs, list(mapping['promotionPosture']['defaultCommitClasses']) + [review_ref], ['Accepted consequence remains gated.'], 'Executor enforced the declared promotion posture and refused any direct accepted-truth shortcut.'),
        event(run_id, 7, base, 'EXECUTOR_FINISH', 'EXECUTOR', 'COMPLETED', [review_ref], [scenario['expectedTerminalOutcome']], [], 'Import executor completed with normalized draft material and an explicit review guard for accepted consequences.'),
    ]
    run = {
        'runId': run_id,
        'scenarioId': scenario['scenarioId'],
        'scenarioFamily': scenario['scenarioFamily'],
        'mode': 'EXECUTOR_SYNTHESIZED_TELEMETRY',
        'direction': 'IMPORT',
        'startedAt': events[0]['at'],
        'completedAt': events[-1]['at'],
        'terminalOutcome': scenario['expectedTerminalOutcome'],
        'sourceSurfaceRef': mapping['externalStandardRef'],
        'runtimeSurfaceContractRef': None,
        'mappingCoverageStatementRef': mapping['statementId'],
        'lossMapRef': loss['lossMapId'],
        'linkedRoundTripRecordIds': [scenario['linkedRoundTripRecordId']],
        'linkedTraceBackIds': [],
        'telemetryEvents': events,
    }
    result = {
        'status': 'PASS' if not reasons else 'FAIL',
        'runId': run_id,
        'terminalOutcome': scenario['expectedTerminalOutcome'],
        'telemetryEventCount': len(events),
        'linkedRoundTripRecordId': scenario['linkedRoundTripRecordId'],
        'reasons': reasons,
    }
    return run, result


def export_surface_run(scenario: Dict[str, Any], validations: Dict[str, str], linked_checks: Dict[str, str], record_idx: Dict[str, Dict[str, Any]], trace_idx: Dict[str, Dict[str, Any]]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    mapping = validate_example(scenario['mappingCoverageExample'], validations)
    loss = validate_example(scenario['lossMapExample'], validations)
    contract = validate_example(scenario['runtimeSurfaceContractExample'], validations)
    req = validate_example(scenario['publicationRequestExample'], validations)
    res = validate_example(scenario['publicationResultExample'], validations)
    meta = validate_example(scenario['passportMetadataExample'], validations)
    rt = record_idx[scenario['linkedRoundTripRecordId']]
    tb = trace_idx[scenario['linkedTraceBackId']]
    linked_checks[f"{scenario['linkedRoundTripRecordId']} :: roundTripRecord"] = 'PASS'
    linked_checks[f"{scenario['linkedTraceBackId']} :: traceBackRecord"] = 'PASS'

    reasons: List[str] = []
    if mapping['direction'] != 'EXPORT':
        reasons.append('export surface run did not bind an export mapping statement')
    if contract['semanticPreservationPosture'] != 'PROJECTION_ONLY':
        reasons.append('runtime surface is expected to remain projection-only')
    if mapping['mappingModuleRef'] not in contract['mappingModuleRefs']:
        reasons.append('runtime surface contract is not bound to the declared export mapping module')
    if req['outputKind'] != 'PASSPORT_VIEW' or res['outputKind'] != 'PASSPORT_VIEW':
        reasons.append('live export surface must remain passport-family only')
    if meta['freezeState'] != 'LIVE_RECOMPUTABLE':
        reasons.append('passport export metadata unexpectedly ceased to be live/recomputable')
    if tb['outputKind'] != 'PASSPORT_VIEW':
        reasons.append('linked trace-back record drifted away from passport-family output')

    run_id = f"execRun:{scenario['scenarioId']}:v0.1"
    base = base_time_from_data([req, res, meta], datetime(2026, 4, 11, 13, 15, 0, tzinfo=timezone.utc))
    payload_ref = f"payload:{scenario['scenarioId']}:ngsi-ld-response"
    events = [
        event(run_id, 1, base, 'EXECUTOR_START', 'EXECUTOR', 'STARTED', [req['requestId']], [run_id], [], 'Export executor accepted a governed live passport publication request.'),
        event(run_id, 2, base, 'PUBLICATION_REQUEST_BOUND', 'PUBLICATION', 'BOUND', [req['requestId']], [req['outputMetadataRef'], req['materializationResultRef']], [], 'Publication request is bound to the live passport metadata and current-state result references.'),
        event(run_id, 3, base, 'RUNTIME_SURFACE_RESOLVED', 'SURFACE', 'RESOLVED', [contract['contractId']], [mapping['statementId']], [], 'Executor resolved the declared runtime surface contract before projection materialization.'),
        event(run_id, 4, base, 'LOSS_POSTURE_ATTACHED', 'MAPPING', 'DISCLOSED', [mapping['statementId']], [loss['lossMapId']], ['Projection export remains loss-aware.'], 'Loss posture is retained in telemetry so the outward facade is not mistaken for canonical OFARM truth.'),
        event(run_id, 5, base, 'OUTPUT_BOUNDARY_CLASSIFIED', 'OUTPUT', 'LIVE_PASSPORT_ONLY', [meta['passportViewId']], [tb['traceBackId']], [], 'Executor classified the outward artifact as a live passport-family export and linked the adapter trace-back record.'),
        event(run_id, 6, base, 'EXPORT_PAYLOAD_EMITTED', 'EXPORT', 'EMITTED', [meta['passportViewId'], mapping['statementId']], [payload_ref, res['publicationRef']], [], 'Executor emitted the outward NGSI-LD projection payload and retained the publication reference.'),
        event(run_id, 7, base, 'EXECUTOR_FINISH', 'EXECUTOR', 'COMPLETED', [payload_ref], [scenario['expectedTerminalOutcome']], [], 'Export executor completed without crossing into frozen document-family semantics.'),
    ]
    run = {
        'runId': run_id,
        'scenarioId': scenario['scenarioId'],
        'scenarioFamily': scenario['scenarioFamily'],
        'mode': 'EXECUTOR_SYNTHESIZED_TELEMETRY',
        'direction': 'EXPORT',
        'startedAt': events[0]['at'],
        'completedAt': events[-1]['at'],
        'terminalOutcome': scenario['expectedTerminalOutcome'],
        'sourceSurfaceRef': mapping['externalStandardRef'],
        'runtimeSurfaceContractRef': contract['contractId'],
        'mappingCoverageStatementRef': mapping['statementId'],
        'lossMapRef': loss['lossMapId'],
        'linkedRoundTripRecordIds': [scenario['linkedRoundTripRecordId']],
        'linkedTraceBackIds': [scenario['linkedTraceBackId']],
        'telemetryEvents': events,
    }
    result = {
        'status': 'PASS' if not reasons else 'FAIL',
        'runId': run_id,
        'terminalOutcome': scenario['expectedTerminalOutcome'],
        'telemetryEventCount': len(events),
        'linkedRoundTripRecordId': scenario['linkedRoundTripRecordId'],
        'linkedTraceBackId': scenario['linkedTraceBackId'],
        'reasons': reasons,
    }
    return run, result


def dossier_run(scenario: Dict[str, Any], validations: Dict[str, str], linked_checks: Dict[str, str], trace_idx: Dict[str, Dict[str, Any]]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    doc = validate_example(scenario['documentMetadataExample'], validations)
    suff = validate_example(scenario['evidenceSufficiencyCaseExample'], validations)
    snap = validate_example(scenario['materializationSnapshotExample'], validations)
    tb = trace_idx[scenario['linkedTraceBackId']]
    linked_checks[f"{scenario['linkedTraceBackId']} :: traceBackRecord"] = 'PASS'

    reasons: List[str] = []
    if doc['documentFamily'] != 'DOSSIER_ASSEMBLY':
        reasons.append('dossier adapter did not bind dossier-family metadata')
    if suff['subject']['subjectType'] != 'DOSSIER_ASSEMBLY':
        reasons.append('evidence sufficiency case is not bound to a dossier subject')
    if suff['outcome']['decision'] != 'ALLOW':
        reasons.append('dossier export adapter requires an allow sufficiency decision')
    if snap['freshnessState'] != 'FRESH':
        reasons.append('dossier package expects a fresh retained snapshot in this starter path')
    if tb['traceBoundary'] != 'FROZEN_DOCUMENT_ONLY':
        reasons.append('linked trace-back boundary drifted away from frozen document posture')

    run_id = f"execRun:{scenario['scenarioId']}:v0.1"
    base = base_time_from_data([doc, suff, snap], datetime(2026, 4, 11, 13, 30, 0, tzinfo=timezone.utc))
    package_ref = f"package:{scenario['scenarioId']}:durable-export"
    events = [
        event(run_id, 1, base, 'EXECUTOR_START', 'EXECUTOR', 'STARTED', [doc['documentAssemblyId']], [run_id], [], 'Document export adapter accepted a frozen dossier assembly for package emission.'),
        event(run_id, 2, base, 'DOCUMENT_METADATA_BOUND', 'OUTPUT', 'BOUND', [doc['documentAssemblyId']], [doc['materializationBasisRef'], doc['materializationSnapshotRef']], [], 'Frozen dossier metadata is bound together with retained basis and snapshot references.'),
        event(run_id, 3, base, 'EVIDENCE_SUFFICIENCY_CONFIRMED', 'EVIDENCE', 'ALLOW', [suff['sufficiencyCaseId']], [suff['attestationPlan']['signatoryAuthorityRef']], [], 'Executor confirmed that the dossier family remains attestation-eligible under the bound evidence case.'),
        event(run_id, 4, base, 'OUTPUT_BOUNDARY_CLASSIFIED', 'OUTPUT', 'FROZEN_DOCUMENT_ONLY', [doc['documentAssemblyId']], [tb['traceBackId']], [], 'Executor classified the output as frozen document-family only and linked the existing adapter trace-back record.'),
        event(run_id, 5, base, 'DURABLE_PACKAGE_EMITTED', 'EXPORT', 'EMITTED', [doc['durableArtifactRef']], [package_ref], [], 'Executor emitted a durable dossier package rather than a live export facade.'),
        event(run_id, 6, base, 'EXECUTOR_FINISH', 'EXECUTOR', 'COMPLETED', [package_ref], [scenario['expectedTerminalOutcome']], [], 'Dossier adapter completed while preserving passport-vs-document separation.'),
    ]
    run = {
        'runId': run_id,
        'scenarioId': scenario['scenarioId'],
        'scenarioFamily': scenario['scenarioFamily'],
        'mode': 'EXECUTOR_SYNTHESIZED_TELEMETRY',
        'direction': 'EXPORT',
        'startedAt': events[0]['at'],
        'completedAt': events[-1]['at'],
        'terminalOutcome': scenario['expectedTerminalOutcome'],
        'sourceSurfaceRef': None,
        'runtimeSurfaceContractRef': None,
        'mappingCoverageStatementRef': None,
        'lossMapRef': None,
        'linkedRoundTripRecordIds': [],
        'linkedTraceBackIds': [scenario['linkedTraceBackId']],
        'telemetryEvents': events,
    }
    result = {
        'status': 'PASS' if not reasons else 'FAIL',
        'runId': run_id,
        'terminalOutcome': scenario['expectedTerminalOutcome'],
        'telemetryEventCount': len(events),
        'linkedTraceBackId': scenario['linkedTraceBackId'],
        'reasons': reasons,
    }
    return run, result


def submission_success_run(scenario: Dict[str, Any], validations: Dict[str, str], linked_checks: Dict[str, str], trace_idx: Dict[str, Dict[str, Any]]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    req = validate_example(scenario['publicationRequestExample'], validations)
    res = validate_example(scenario['publicationResultExample'], validations)
    doc = validate_example(scenario['documentMetadataExample'], validations)
    suff = validate_example(scenario['evidenceSufficiencyCaseExample'], validations)
    mat = validate_example(scenario['materializationResultExample'], validations)
    snap = validate_example(scenario['materializationSnapshotExample'], validations)
    tb = trace_idx[scenario['linkedTraceBackId']]
    linked_checks[f"{scenario['linkedTraceBackId']} :: traceBackRecord"] = 'PASS'

    reasons: List[str] = []
    if req['outputKind'] != 'SUBMISSION_ASSEMBLY' or res['outputKind'] != 'SUBMISSION_ASSEMBLY':
        reasons.append('submission filing must remain submission-family throughout publication request/result')
    if mat['freshnessState'] != 'FRESH' or mat['decisionOutcome'] != 'ALLOW_REUSE':
        reasons.append('submission filing expects fresh reusable materialization in this allow path')
    if suff['outcome']['decision'] != 'ALLOW':
        reasons.append('submission filing expects an allow evidence sufficiency decision')
    if doc['documentFamily'] != 'SUBMISSION_ASSEMBLY':
        reasons.append('submission filing must bind submission assembly metadata')
    if tb['traceBoundary'] != 'FROZEN_FILEABLE_ONLY':
        reasons.append('linked trace-back boundary drifted away from frozen fileable posture')

    run_id = f"execRun:{scenario['scenarioId']}:v0.1"
    base = base_time_from_data([req, res, doc, mat, snap], datetime(2026, 4, 11, 13, 45, 0, tzinfo=timezone.utc))
    filing_ref = res['publicationRef']
    events = [
        event(run_id, 1, base, 'EXECUTOR_START', 'EXECUTOR', 'STARTED', [req['requestId']], [run_id], [], 'Submission-file adapter accepted a governed filing request.'),
        event(run_id, 2, base, 'PUBLICATION_REQUEST_BOUND', 'PUBLICATION', 'BOUND', [req['requestId']], [req['outputMetadataRef'], req['materializationResultRef']], [], 'Publication request is bound to submission metadata and the retained materialization result.'),
        event(run_id, 3, base, 'MATERIALIZATION_STATE_CONFIRMED', 'MATERIALIZATION', 'FRESH_ALLOW_REUSE', [mat['resultId']], [snap['snapshotId']], [], 'Executor confirmed that the retained compliance materialization remained fresh enough for filing.'),
        event(run_id, 4, base, 'EVIDENCE_SUFFICIENCY_CONFIRMED', 'EVIDENCE', 'ALLOW', [suff['sufficiencyCaseId']], [suff['attestationPlan']['signatoryAuthorityRef']], [], 'Evidence sufficiency and filing authority remained aligned for the submission path.'),
        event(run_id, 5, base, 'OUTPUT_BOUNDARY_CLASSIFIED', 'OUTPUT', 'FROZEN_FILEABLE_ONLY', [doc['documentAssemblyId']], [tb['traceBackId']], [], 'Executor classified the output as a frozen fileable submission and linked the existing adapter trace-back record.'),
        event(run_id, 6, base, 'FILEABLE_OUTPUT_EMITTED', 'EXPORT', 'FILED', [doc['durableArtifactRef']], [filing_ref], [], 'Executor emitted the governed filing reference into the external process boundary.'),
        event(run_id, 7, base, 'EXECUTOR_FINISH', 'EXECUTOR', 'COMPLETED', [filing_ref], [scenario['expectedTerminalOutcome']], [], 'Submission-file adapter completed without collapsing into live passport semantics.'),
    ]
    run = {
        'runId': run_id,
        'scenarioId': scenario['scenarioId'],
        'scenarioFamily': scenario['scenarioFamily'],
        'mode': 'EXECUTOR_SYNTHESIZED_TELEMETRY',
        'direction': 'EXPORT',
        'startedAt': events[0]['at'],
        'completedAt': events[-1]['at'],
        'terminalOutcome': scenario['expectedTerminalOutcome'],
        'sourceSurfaceRef': None,
        'runtimeSurfaceContractRef': None,
        'mappingCoverageStatementRef': None,
        'lossMapRef': None,
        'linkedRoundTripRecordIds': [],
        'linkedTraceBackIds': [scenario['linkedTraceBackId']],
        'telemetryEvents': events,
    }
    result = {
        'status': 'PASS' if not reasons else 'FAIL',
        'runId': run_id,
        'terminalOutcome': scenario['expectedTerminalOutcome'],
        'telemetryEventCount': len(events),
        'linkedTraceBackId': scenario['linkedTraceBackId'],
        'reasons': reasons,
    }
    return run, result


def submission_invalid_run(scenario: Dict[str, Any], validations: Dict[str, str]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    doc = validate_example(scenario['documentMetadataExample'], validations)
    suff = validate_example(scenario['evidenceSufficiencyCaseExample'], validations)
    mat = validate_example(scenario['materializationResultExample'], validations)
    snap = validate_example(scenario['materializationSnapshotExample'], validations)

    reasons: List[str] = []
    if mat['freshnessState'] != 'INVALID' or mat['decisionOutcome'] != 'REFUSE_USE':
        reasons.append('blocked submission path requires an invalid/refuse-use materialization result')
    if snap['freshnessState'] != 'INVALID':
        reasons.append('blocked submission path should bind the invalid retained snapshot')
    if doc['documentFamily'] != 'SUBMISSION_ASSEMBLY':
        reasons.append('blocked submission path must still target a submission assembly output family')
    if suff['outcome']['decision'] != 'ALLOW':
        reasons.append('evidence sufficiency remains allow-capable in this scenario; block must come from invalid materialization')

    run_id = f"execRun:{scenario['scenarioId']}:v0.1"
    base = base_time_from_data([doc, suff, mat, snap], datetime(2026, 4, 11, 14, 0, 0, tzinfo=timezone.utc))
    problem_ids = [p['problemId'] for p in mat.get('problems', [])]
    events = [
        event(run_id, 1, base, 'EXECUTOR_START', 'EXECUTOR', 'STARTED', [doc['documentAssemblyId']], [run_id], [], 'Submission-file adapter accepted an attempted filing path for validation.'),
        event(run_id, 2, base, 'DOCUMENT_METADATA_BOUND', 'OUTPUT', 'BOUND', [doc['documentAssemblyId']], [doc['materializationBasisRef'], doc['materializationSnapshotRef']], [], 'Submission metadata was bound before the runtime freshness recheck.'),
        event(run_id, 3, base, 'EVIDENCE_SUFFICIENCY_BOUND', 'EVIDENCE', 'ALLOW_READY', [suff['sufficiencyCaseId']], [suff['attestationPlan']['signatoryAuthorityRef']], [], 'Evidence posture alone would have permitted filing if current-state freshness had remained acceptable.'),
        event(run_id, 4, base, 'MATERIALIZATION_STATE_REJECTED', 'MATERIALIZATION', 'INVALID_REFUSE_USE', [mat['resultId']], problem_ids, ['Context drift invalidated the retained compliance basis.'], 'Executor refused to continue once the bound materialization result reported invalid current-state reuse.'),
        event(run_id, 5, base, 'EXECUTOR_FINISH', 'EXECUTOR', 'STOPPED', problem_ids, [scenario['expectedTerminalOutcome']], [], 'No fileable or frozen output was emitted because the materialization gate failed before export.'),
    ]
    run = {
        'runId': run_id,
        'scenarioId': scenario['scenarioId'],
        'scenarioFamily': scenario['scenarioFamily'],
        'mode': 'EXECUTOR_SYNTHESIZED_TELEMETRY',
        'direction': 'EXPORT',
        'startedAt': events[0]['at'],
        'completedAt': events[-1]['at'],
        'terminalOutcome': scenario['expectedTerminalOutcome'],
        'sourceSurfaceRef': None,
        'runtimeSurfaceContractRef': None,
        'mappingCoverageStatementRef': None,
        'lossMapRef': None,
        'linkedRoundTripRecordIds': [],
        'linkedTraceBackIds': [],
        'telemetryEvents': events,
    }
    result = {
        'status': 'PASS' if not reasons else 'FAIL',
        'runId': run_id,
        'terminalOutcome': scenario['expectedTerminalOutcome'],
        'telemetryEventCount': len(events),
        'reasons': reasons,
    }
    return run, result


def main() -> None:
    validations: Dict[str, str] = {}
    linked_checks: Dict[str, str] = {}
    roundtrip = roundtrip_index()
    tracebacks = traceback_index()

    import_results: Dict[str, Any] = {}
    export_results: Dict[str, Any] = {}
    runs: List[Dict[str, Any]] = []

    for name in SCENARIOS:
        scenario = load_json(FIX / name)
        assert isinstance(scenario, dict)
        family = scenario['scenarioFamily']
        if family == 'IMPORT_EXECUTOR':
            run, result = import_run(scenario, validations, linked_checks, roundtrip)
            import_results[scenario['scenarioId']] = result
        elif family == 'EXPORT_SURFACE_EXECUTOR':
            run, result = export_surface_run(scenario, validations, linked_checks, roundtrip, tracebacks)
            export_results[scenario['scenarioId']] = result
        elif family == 'DOCUMENT_EXPORT_ADAPTER_EXECUTOR':
            run, result = dossier_run(scenario, validations, linked_checks, tracebacks)
            export_results[scenario['scenarioId']] = result
        elif family == 'SUBMISSION_FILE_ADAPTER_EXECUTOR' and 'publicationRequestExample' in scenario:
            run, result = submission_success_run(scenario, validations, linked_checks, tracebacks)
            export_results[scenario['scenarioId']] = result
        elif family == 'SUBMISSION_FILE_ADAPTER_EXECUTOR':
            run, result = submission_invalid_run(scenario, validations)
            export_results[scenario['scenarioId']] = result
        else:
            raise AssertionError(f'unsupported scenario family {family}')
        runs.append(run)

    overall = 'PASS'
    for bucket in (import_results, export_results):
        for result in bucket.values():
            if result['status'] != 'PASS':
                overall = 'FAIL'
                break
    limitations = [
        'Telemetry is produced by a package-local execution runner rather than collected from a deployed OFARM runtime.',
        'Same-standard reversible bridge-pack loops still do not ship; linked round-trip records remain one-way or projection-only.',
        'NGSI-LD remains the only declared live export runtime surface in the package; dossier and submission paths are still frozen package/file adapters rather than partner-specific runtime surfaces.'
    ]
    if overall == 'PASS':
        overall = 'PASS_WITH_LIMITATIONS'

    results = {
        'importExecutorTelemetry': import_results,
        'exportExecutorTelemetry': export_results,
        'linkedArtifactChecks': linked_checks,
        'validatedExamples': validations,
        'limitations': limitations,
        'overall': overall,
        'counts': {
            'scenarios': len(runs),
            'validatedExamples': len(validations),
            'linkedRoundTripRecords': sum(1 for k in linked_checks if 'roundTripRecord' in k),
            'linkedTraceBackRecords': sum(1 for k in linked_checks if 'traceBackRecord' in k),
            'telemetryRuns': len(runs),
            'telemetryEvents': sum(len(r['telemetryEvents']) for r in runs),
        }
    }

    TELEMETRY_OUT.write_text(json.dumps(runs, indent=2) + '\n', encoding='utf-8')
    RESULTS_OUT.write_text(json.dumps(results, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
