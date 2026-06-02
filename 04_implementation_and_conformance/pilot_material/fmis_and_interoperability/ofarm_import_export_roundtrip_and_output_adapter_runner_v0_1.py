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
FIX = IMPL / 'ofarm_import_export_roundtrip_output_adapter_fixtures_v0_1'

GATE_LOGS_OUT = IMPL / 'OFARM_import_export_path_gate_logs_v0_1.json'
ROUNDTRIP_OUT = IMPL / 'OFARM_mapping_round_trip_records_v0_1.json'
OUTPUT_TRACE_OUT = IMPL / 'OFARM_output_adapter_trace_back_records_v0_1.json'
RESULTS_OUT = IMPL / 'OFARM_import_export_roundtrip_and_output_adapter_results_v0_1.json'

SCHEMAS = {p.name: json.loads(p.read_text(encoding='utf-8')) for p in MC.glob('*_schema_*.json')}
for schema in SCHEMAS.values():
    jsonschema.Draft202012Validator.check_schema(schema)

IMPORT_FIXTURES = [
    'adapt_import_claim_first.json',
    'isoxml_import_claim_first.json',
]
EXPORT_FIXTURES = [
    'ngsi_ld_live_passport_export.json',
]
ROUNDTRIP_FIXTURES = [
    'roundtrip_adapt_import_declared_surface.json',
    'roundtrip_isoxml_import_declared_surface.json',
    'roundtrip_ngsi_ld_export_declared_surface.json',
]
OUTPUT_FIXTURES = [
    'output_adapter_field_dossier_frozen_package.json',
    'output_adapter_submission_filing_frozen.json',
]
ALL_COVERAGE_EXAMPLES = [
    'OFARM_MappingCoverageStatement_example_adapt_import_v0_1.json',
    'OFARM_MappingCoverageStatement_example_isoxml_import_v0_1.json',
    'OFARM_MappingCoverageStatement_example_ngsi_ld_export_v0_1.json',
]


def load_json(path: Path) -> Dict[str, Any]:
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


def expect(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def make_import_gate_log(fixture: Dict[str, Any], statement: Dict[str, Any], lossm: Dict[str, Any], base_time: datetime) -> Dict[str, Any]:
    gates = [
        {
            'gate': 'IMPORT_SURFACE_INTAKE',
            'outcome': 'ACCEPTED',
            'sourceExamples': [fixture['mappingCoverageExample']],
            'inputRefs': [statement['externalStandardRef']],
            'producedRefs': [statement['mappingModuleRef']],
            'notes': f"Inbound payload is recognized under {statement['externalStandardRef']} and routed into governed mapping resolution.",
        },
        {
            'gate': 'MAPPING_COVERAGE_RESOLUTION',
            'outcome': 'RESOLVED',
            'sourceExamples': [fixture['mappingCoverageExample']],
            'inputRefs': [statement['mappingModuleRef']],
            'producedRefs': [statement['statementId']],
            'notes': 'Coverage statement resolved and binds the ingest path to explicit OFARM targets.',
        },
        {
            'gate': 'LOSS_POSTURE_DISCLOSURE',
            'outcome': 'DISCLOSED',
            'sourceExamples': [fixture['lossMapExample']],
            'inputRefs': [statement['statementId']],
            'producedRefs': [lossm['lossMapId']],
            'notes': f"Loss posture is {lossm['overallLossPosture']} and must remain visible before any high-consequence use.",
        },
        {
            'gate': 'NORMALIZE_TO_ALLOWED_COMMIT_CLASSES',
            'outcome': 'NORMALIZED_TO_DRAFT',
            'sourceExamples': [fixture['mappingCoverageExample']],
            'inputRefs': [statement['mappingModuleRef']],
            'producedRefs': list(statement['promotionPosture']['defaultCommitClasses']),
            'notes': 'Normalization lands in claim/evidence-first commit classes rather than accepted truth.',
        },
        {
            'gate': 'ACCEPTED_CONSEQUENCE_GUARD',
            'outcome': fixture['expectedAcceptedConsequencePolicy'],
            'sourceExamples': [fixture['mappingCoverageExample'], fixture['lossMapExample']],
            'inputRefs': list(statement['promotionPosture']['defaultCommitClasses']),
            'producedRefs': [fixture['expectedTerminalOutcome']],
            'notes': 'Accepted consequence promotion remains gated and cannot occur from format presence alone.',
        },
    ]
    for idx, gate in enumerate(gates, start=1):
        start = base_time + timedelta(seconds=(idx - 1) * 4)
        gate['stepIndex'] = idx
        gate['traceRefs'] = []
        gate['startedAt'] = dt_to_z(start)
        gate['finishedAt'] = dt_to_z(start + timedelta(seconds=2))
    return {
        'logId': f"gateLog:{fixture['fixtureId']}:v0.1",
        'fixtureId': fixture['fixtureId'],
        'fixtureType': fixture['fixtureType'],
        'sourceFixtureRef': f"04_implementation_and_conformance/examples_and_fixtures/ofarm_import_export_roundtrip_output_adapter_fixtures_v0_1/{fixture['fixtureId'].replace('-', '_')}.json",
        'replayMode': 'EXECUTABLE_FIXTURE_REPLAY',
        'startedAt': gates[0]['startedAt'],
        'completedAt': gates[-1]['finishedAt'],
        'terminalOutcome': fixture['expectedTerminalOutcome'],
        'expectedStopGate': 'ACCEPTED_CONSEQUENCE_GUARD',
        'monotonicGateOrder': True,
        'linkedTraceBackIds': [],
        'gateEvents': gates,
    }


def validate_import_fixture(fixture_name: str, validations: Dict[str, str], index: int) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    fixture = load_json(FIX / fixture_name)
    statement = validate_example(fixture['mappingCoverageExample'], validations)
    lossm = validate_example(fixture['lossMapExample'], validations)
    reasons: List[str] = []
    if statement['direction'] != 'IMPORT':
        reasons.append('mapping direction must be IMPORT')
    if lossm['mappingCoverageStatementRef'] != statement['statementId']:
        reasons.append('loss map must point back to the coverage statement')
    if statement['promotionPosture'].get('autoPromotionAllowed') is not False:
        reasons.append('import surfaces must not auto-promote to accepted truth')
    if statement['promotionPosture'].get('requiresReviewForAcceptedConsequences') is not True:
        reasons.append('accepted consequences must require review for imports')
    if statement['promotionPosture'].get('defaultCommitClasses') != fixture['expectedCommitClasses']:
        reasons.append('default commit classes drifted from the expected evidence/claim-first posture')
    base_time = datetime(2026, 4, 11, 8, 0, 0, tzinfo=timezone.utc) + timedelta(minutes=index)
    log = make_import_gate_log(fixture, statement, lossm, base_time)
    status = 'PASS' if not reasons else 'FAIL'
    result = {
        'status': status,
        'statementId': statement['statementId'],
        'lossMapId': lossm['lossMapId'],
        'logId': log['logId'],
        'reasons': reasons,
    }
    return result, log


def make_export_gate_log(fixture: Dict[str, Any], statement: Dict[str, Any], lossm: Dict[str, Any], contract: Dict[str, Any], passport: Dict[str, Any], pub_req: Dict[str, Any], pub_res: Dict[str, Any], base_time: datetime) -> Dict[str, Any]:
    gates = [
        {
            'gate': 'EXPORT_REQUEST_INTAKE',
            'outcome': 'ACCEPTED',
            'sourceExamples': [fixture['publicationRequestExample']],
            'inputRefs': [pub_req['requestId']],
            'producedRefs': [pub_req['outputMetadataRef']],
            'notes': 'Publication/export request is accepted against a live passport publication path.',
        },
        {
            'gate': 'MAPPING_COVERAGE_RESOLUTION',
            'outcome': 'RESOLVED',
            'sourceExamples': [fixture['mappingCoverageExample']],
            'inputRefs': [statement['mappingModuleRef']],
            'producedRefs': [statement['statementId']],
            'notes': 'Export mapping coverage binds the outward projection path explicitly.',
        },
        {
            'gate': 'LOSS_POSTURE_DISCLOSURE',
            'outcome': 'DISCLOSED',
            'sourceExamples': [fixture['lossMapExample']],
            'inputRefs': [statement['statementId']],
            'producedRefs': [lossm['lossMapId']],
            'notes': 'Declared export loss posture is carried alongside the surface use.',
        },
        {
            'gate': 'OUTPUT_BOUNDARY_CHECK',
            'outcome': 'LIVE_PASSPORT_CONFIRMED',
            'sourceExamples': [fixture['passportMetadataExample'], fixture['publicationRequestExample']],
            'inputRefs': [passport['passportViewId'], pub_req['publicationAction']],
            'producedRefs': [passport['freezeState']],
            'notes': 'The outward resource remains a live PassportView and is not converted into a frozen document.',
        },
        {
            'gate': 'RUNTIME_SURFACE_EXPORT',
            'outcome': 'PUBLISHED',
            'sourceExamples': [fixture['runtimeSurfaceContractExample'], fixture['publicationResultExample']],
            'inputRefs': [contract['contractId'], pub_req['requestId']],
            'producedRefs': [pub_res['publicationRef'], pub_res['resultId']],
            'notes': 'Runtime surface contract, publication result, and passport metadata remain aligned on a projection-only export posture.',
        },
    ]
    for idx, gate in enumerate(gates, start=1):
        start = base_time + timedelta(seconds=(idx - 1) * 4)
        gate['stepIndex'] = idx
        gate['traceRefs'] = [pub_req['authorizationDecisionTraceRef']] if idx in {1, 5} else []
        gate['startedAt'] = dt_to_z(start)
        gate['finishedAt'] = dt_to_z(start + timedelta(seconds=2))
    return {
        'logId': f"gateLog:{fixture['fixtureId']}:v0.1",
        'fixtureId': fixture['fixtureId'],
        'fixtureType': fixture['fixtureType'],
        'sourceFixtureRef': f"04_implementation_and_conformance/examples_and_fixtures/ofarm_import_export_roundtrip_output_adapter_fixtures_v0_1/{fixture['fixtureId'].replace('-', '_')}.json",
        'replayMode': 'EXECUTABLE_FIXTURE_REPLAY',
        'startedAt': gates[0]['startedAt'],
        'completedAt': gates[-1]['finishedAt'],
        'terminalOutcome': fixture['expectedTerminalOutcome'],
        'expectedStopGate': 'RUNTIME_SURFACE_EXPORT',
        'monotonicGateOrder': True,
        'linkedTraceBackIds': ['traceback:adapter-passport-ngsi-ld-live:v0.1'],
        'gateEvents': gates,
    }


def validate_export_fixture(fixture_name: str, validations: Dict[str, str], index: int) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    fixture = load_json(FIX / fixture_name)
    statement = validate_example(fixture['mappingCoverageExample'], validations)
    lossm = validate_example(fixture['lossMapExample'], validations)
    contract = validate_example(fixture['runtimeSurfaceContractExample'], validations)
    passport = validate_example(fixture['passportMetadataExample'], validations)
    pub_req = validate_example(fixture['publicationRequestExample'], validations)
    pub_res = validate_example(fixture['publicationResultExample'], validations)
    reasons: List[str] = []
    if statement['direction'] != 'EXPORT':
        reasons.append('mapping direction must be EXPORT')
    if lossm['mappingCoverageStatementRef'] != statement['statementId']:
        reasons.append('loss map must point back to the export coverage statement')
    if statement['mappingModuleRef'] not in contract.get('mappingModuleRefs', []):
        reasons.append('runtime surface contract must reference the export mapping module')
    if contract['semanticPreservationPosture'] != fixture['expectedSemanticPosture']:
        reasons.append('runtime surface semantic posture drifted')
    if passport['freezeState'] != 'LIVE_RECOMPUTABLE':
        reasons.append('passport export must remain live and recomputable')
    if pub_req['outputKind'] != 'PASSPORT_VIEW' or pub_res['outputKind'] != 'PASSPORT_VIEW':
        reasons.append('export publication must stay within PassportView output kind')
    if pub_req['requiresFrozenOutput']:
        reasons.append('live passport export must not require a frozen output')
    if pub_req['attestationRequested']:
        reasons.append('live passport export must not request attestation')
    if pub_res['outcome'] != 'PUBLISHED':
        reasons.append('export publication result must be PUBLISHED')
    if pub_req['outputMetadataRef'] != passport['passportViewId'] or pub_res['outputMetadataRef'] != passport['passportViewId']:
        reasons.append('passport publication refs must align on the same PassportView metadata object')
    base_time = parse_dt(pub_req['requestedAt']) + timedelta(minutes=index)
    log = make_export_gate_log(fixture, statement, lossm, contract, passport, pub_req, pub_res, base_time)
    trace_record = {
        'traceBackId': 'traceback:adapter-passport-ngsi-ld-live:v0.1',
        'family': 'PASSPORT_VIEW_EXPORT_ADAPTER',
        'outputKind': 'PASSPORT_VIEW',
        'outputMetadataRef': passport['passportViewId'],
        'publicationRef': pub_res['publicationRef'],
        'runtimeSurfaceContractRef': contract['contractId'],
        'mappingCoverageStatementRef': statement['statementId'],
        'lossMapRef': lossm['lossMapId'],
        'materializationResultRef': passport['materializationResultRef'],
        'contextSnapshotRef': passport['contextSnapshotRef'],
        'querySpecificationRef': passport['querySpecificationRef'],
        'queryPlanRef': passport['queryPlanRef'],
        'authorizationDecisionTraceRef': pub_res['authorizationDecisionTraceRef'],
        'traceBoundary': fixture['expectedBoundary'],
        'notes': 'Live buyer-facing passport export is traced through NGSI-LD as a governed projection-only surface.',
    }
    summary = {
        'status': 'PASS' if not reasons else 'FAIL',
        'statementId': statement['statementId'],
        'contractId': contract['contractId'],
        'logId': log['logId'],
        'traceBackId': trace_record['traceBackId'],
        'reasons': reasons,
    }
    output_check = {
        'status': 'PASS' if not reasons else 'FAIL',
        'traceBackId': trace_record['traceBackId'],
        'boundary': fixture['expectedBoundary'],
        'reasons': reasons,
    }
    return summary, log, trace_record, output_check


def build_roundtrip_record(fixture_name: str, validations: Dict[str, str], all_coverage: List[Dict[str, Any]]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    fixture = load_json(FIX / fixture_name)
    statement = validate_example(fixture['mappingCoverageExample'], validations)
    lossm = validate_example(fixture['lossMapExample'], validations)
    contract = None
    if fixture.get('runtimeSurfaceContractExample'):
        contract = validate_example(fixture['runtimeSurfaceContractExample'], validations)
    counterpart_refs = [item['statementId'] for item in all_coverage if item['externalStandardRef'] == statement['externalStandardRef'] and item['direction'] != statement['direction']]
    reason_codes: List[str] = []
    if statement['direction'] == 'IMPORT':
        roundtrip_class = 'ONE_WAY_IMPORT_LOSS_AWARE'
        if not counterpart_refs:
            reason_codes.append('NO_DECLARED_RETURN_SURFACE')
        if statement['promotionPosture'].get('autoPromotionAllowed') is False:
            reason_codes.append('IMPORT_PROMOTION_REMAINS_GOVERNED')
    else:
        if contract and contract.get('semanticPreservationPosture') == 'PROJECTION_ONLY':
            roundtrip_class = 'ONE_WAY_EXPORT_PROJECTION_ONLY'
            reason_codes.append('PROJECTION_ONLY_EXPORT')
        else:
            roundtrip_class = 'ONE_WAY_EXPORT_LOSS_AWARE'
        if not counterpart_refs:
            reason_codes.append('NO_DECLARED_IMPORT_SURFACE')
    reasons: List[str] = []
    if roundtrip_class != fixture['expectedRoundTripClass']:
        reasons.append(f'expected roundTripClass {fixture["expectedRoundTripClass"]} but got {roundtrip_class}')
    for code in fixture['expectedReasonCodes']:
        if code not in reason_codes:
            reasons.append(f'missing expected reason code: {code}')
    record = {
        'recordId': f"roundTrip:{fixture['fixtureId']}:v0.1",
        'mappingCoverageStatementRef': statement['statementId'],
        'lossMapRef': lossm['lossMapId'],
        'runtimeSurfaceContractRef': contract['contractId'] if contract else None,
        'externalStandardRef': statement['externalStandardRef'],
        'direction': statement['direction'],
        'declaredRoundTripExpectation': statement['roundTripExpectation'],
        'availableCounterpartSurfaceRefs': counterpart_refs,
        'roundTripClass': roundtrip_class,
        'blockingReasonCodes': reason_codes,
        'notes': fixture['notes'],
    }
    result = {
        'status': 'PASS' if not reasons else 'FAIL',
        'roundTripClass': roundtrip_class,
        'blockingReasonCodes': reason_codes,
        'reasons': reasons,
    }
    return record, result


def validate_output_fixture(fixture_name: str, validations: Dict[str, str]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    fixture = load_json(FIX / fixture_name)
    document = validate_example(fixture['documentMetadataExample'], validations)
    case = validate_example(fixture['evidenceSufficiencyExample'], validations)
    pub_req = pub_res = None
    reasons: List[str] = []
    if not document.get('frozenAt'):
        reasons.append('document output must be frozen for this adapter family')
    if case['subject']['subjectRef'] != document['documentAssemblyId']:
        reasons.append('evidence sufficiency subject does not match document assembly id')
    if case['outcome']['decision'] != 'ALLOW' or case['outcome'].get('attestationAllowed') is not True:
        reasons.append('evidence sufficiency outcome must allow the frozen adapter path')
    if fixture['expectedBoundary'] == 'FROZEN_DOCUMENT_ONLY':
        if document['documentFamily'] != 'DOSSIER_ASSEMBLY':
            reasons.append('dossier adapter must reference DOSSIER_ASSEMBLY metadata')
        if document['reviewState'] != 'ATTESTED':
            reasons.append('dossier package should already be in an attested review state')
        record = {
            'traceBackId': 'traceback:adapter-dossier-frozen-package:v0.1',
            'family': 'DOSSIER_ASSEMBLY_EXPORT_PACKAGE',
            'outputKind': 'DOSSIER_ASSEMBLY',
            'outputMetadataRef': document['documentAssemblyId'],
            'publicationRef': document['durableArtifactRef'],
            'runtimeSurfaceContractRef': None,
            'mappingCoverageStatementRef': None,
            'lossMapRef': None,
            'materializationBasisRef': document['materializationBasisRef'],
            'materializationSnapshotRef': document['materializationSnapshotRef'],
            'contextSnapshotRef': document['contextSnapshotRef'],
            'querySpecificationRefs': document['querySpecificationRefs'],
            'queryPlanRefs': document['queryPlanRefs'],
            'evidenceSufficiencyCaseRef': document['evidenceSufficiencyCaseRef'],
            'authorizationDecisionTraceRef': document['authorizationDecisionTraceRef'],
            'traceBoundary': fixture['expectedBoundary'],
            'notes': 'Frozen dossier package remains a document-family export/attestation path, not a live API surface.',
        }
    else:
        pub_req = validate_example(fixture['publicationRequestExample'], validations)
        pub_res = validate_example(fixture['publicationResultExample'], validations)
        if document['documentFamily'] != 'SUBMISSION_ASSEMBLY':
            reasons.append('submission filing adapter must reference SUBMISSION_ASSEMBLY metadata')
        if pub_req['outputMetadataRef'] != document['documentAssemblyId'] or pub_res['outputMetadataRef'] != document['documentAssemblyId']:
            reasons.append('publication request/result must target the same submission metadata object')
        if pub_req['requiresFrozenOutput'] is not True or pub_req['attestationRequested'] is not True:
            reasons.append('submission filing must remain a frozen attested output path')
        if pub_res['outcome'] != 'FILED':
            reasons.append('submission filing result must be FILED')
        record = {
            'traceBackId': 'traceback:adapter-submission-filing:v0.1',
            'family': 'SUBMISSION_ASSEMBLY_FILE_ADAPTER',
            'outputKind': 'SUBMISSION_ASSEMBLY',
            'outputMetadataRef': document['documentAssemblyId'],
            'publicationRef': pub_res['publicationRef'],
            'runtimeSurfaceContractRef': None,
            'mappingCoverageStatementRef': None,
            'lossMapRef': None,
            'materializationBasisRef': document['materializationBasisRef'],
            'materializationSnapshotRef': document['materializationSnapshotRef'],
            'contextSnapshotRef': document['contextSnapshotRef'],
            'querySpecificationRefs': document['querySpecificationRefs'],
            'queryPlanRefs': document['queryPlanRefs'],
            'evidenceSufficiencyCaseRef': document['evidenceSufficiencyCaseRef'],
            'authorizationDecisionTraceRef': document['authorizationDecisionTraceRef'],
            'traceBoundary': fixture['expectedBoundary'],
            'notes': 'Frozen submission filing remains a governed file/export path rather than a live passport-style share.',
        }
    result = {
        'status': 'PASS' if not reasons else 'FAIL',
        'traceBackId': record['traceBackId'],
        'boundary': fixture['expectedBoundary'],
        'reasons': reasons,
    }
    return record, result


def main() -> int:
    validations: Dict[str, str] = {}
    results: Dict[str, Any] = {
        'importSurfacePromotionPosture': {},
        'exportSurfaceProjectionPosture': {},
        'mappingRoundTripFeasibility': {},
        'outputAdapterBoundaryChecks': {},
        'validatedExamples': validations,
        'limitations': [
            'This wave still replays package-relative fixtures rather than executor-native ingest/export telemetry.',
            'The current active package ships one-way mapping surfaces only; same-standard reversible bridge-pack loops remain future work.',
            'Dossier and submission output-adapter coverage is package-level and publication-level, not yet backed by broader partner-specific runtime surface contracts.',
        ],
        'overall': 'PASS_WITH_LIMITATIONS',
    }

    all_coverage = [validate_example(name, validations) for name in ALL_COVERAGE_EXAMPLES]

    gate_logs: List[Dict[str, Any]] = []
    roundtrip_records: List[Dict[str, Any]] = []
    output_records: List[Dict[str, Any]] = []

    any_fail = False

    for idx, fixture_name in enumerate(IMPORT_FIXTURES, start=1):
        entry, log = validate_import_fixture(fixture_name, validations, idx)
        results['importSurfacePromotionPosture'][load_json(FIX / fixture_name)['fixtureId']] = entry
        gate_logs.append(log)
        if entry['status'] == 'FAIL':
            any_fail = True

    for idx, fixture_name in enumerate(EXPORT_FIXTURES, start=1):
        summary, log, trace_record, output_check = validate_export_fixture(fixture_name, validations, idx)
        fixture = load_json(FIX / fixture_name)
        results['exportSurfaceProjectionPosture'][fixture['fixtureId']] = summary
        results['outputAdapterBoundaryChecks'][fixture['fixtureId']] = output_check
        gate_logs.append(log)
        output_records.append(trace_record)
        if summary['status'] == 'FAIL' or output_check['status'] == 'FAIL':
            any_fail = True

    for fixture_name in ROUNDTRIP_FIXTURES:
        record, result = build_roundtrip_record(fixture_name, validations, all_coverage)
        fixture = load_json(FIX / fixture_name)
        results['mappingRoundTripFeasibility'][fixture['fixtureId']] = result
        roundtrip_records.append(record)
        if result['status'] == 'FAIL':
            any_fail = True

    for fixture_name in OUTPUT_FIXTURES:
        record, result = validate_output_fixture(fixture_name, validations)
        fixture = load_json(FIX / fixture_name)
        results['outputAdapterBoundaryChecks'][fixture['fixtureId']] = result
        output_records.append(record)
        if result['status'] == 'FAIL':
            any_fail = True

    results['counts'] = {
        'fixturesChecked': len(IMPORT_FIXTURES) + len(EXPORT_FIXTURES) + len(ROUNDTRIP_FIXTURES) + len(OUTPUT_FIXTURES),
        'validatedExamples': len(validations),
        'importExportGateLogs': len(gate_logs),
        'mappingRoundTripRecords': len(roundtrip_records),
        'outputAdapterTraceBackRecords': len(output_records),
    }
    if any_fail:
        results['overall'] = 'FAIL'

    GATE_LOGS_OUT.write_text(json.dumps(gate_logs, indent=2) + '\n', encoding='utf-8')
    ROUNDTRIP_OUT.write_text(json.dumps(roundtrip_records, indent=2) + '\n', encoding='utf-8')
    OUTPUT_TRACE_OUT.write_text(json.dumps(output_records, indent=2) + '\n', encoding='utf-8')
    RESULTS_OUT.write_text(json.dumps(results, indent=2) + '\n', encoding='utf-8')

    print(GATE_LOGS_OUT)
    print(ROUNDTRIP_OUT)
    print(OUTPUT_TRACE_OUT)
    print(RESULTS_OUT)
    print(results['overall'])
    return 0 if results['overall'] != 'FAIL' else 1


if __name__ == '__main__':
    raise SystemExit(main())
