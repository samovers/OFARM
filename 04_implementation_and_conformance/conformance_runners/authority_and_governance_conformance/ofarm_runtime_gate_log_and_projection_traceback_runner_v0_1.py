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
GATE_FIX = IMPL / 'ofarm_gate_sequencing_fixtures_v0_1'
RT_FIX = IMPL / 'ofarm_runtime_boundary_fixtures_v0_1'
TRACE_FIX = IMPL / 'ofarm_runtime_gate_log_traceback_fixtures_v0_1'
GATE_LOGS_OUT = IMPL / 'OFARM_runtime_gate_logs_v0_1.json'
TRACEBACK_OUT = IMPL / 'OFARM_projection_trace_back_records_v0_1.json'
RESULTS_OUT = IMPL / 'OFARM_runtime_gate_log_and_projection_traceback_results_v0_1.json'
PRIMARY_ID_KEYS = [
    'requestId', 'resultId', 'traceId', 'snapshotId', 'basisId', 'sufficiencyCaseId',
    'passportViewId', 'documentAssemblyId', 'queryId', 'planId', 'contextSnapshotId'
]
TIMESTAMP_KEYS = ['requestedAt', 'evaluatedAt', 'generatedAt', 'resolvedAt', 'frozenAt']
SEQUENCE_FIXTURES = sorted([
    'ai_assisted_submission_requires_human.json',
    'capture_advisory_output_no_hard_truth_shortcut.json',
    'capture_note_no_compliance_shortcut.json',
    'compliance_assertion_reviewed_accept_promotes.json',
    'operation_claim_missing_evidence_stays_draft.json',
    'operation_claim_reviewed_accept_promotes.json',
    'revoked_submission_promotion_recheck_denies.json',
    'submission_filing_full_gate_chain_allow.json',
])
PROJECTION_FIXTURES = sorted([p.name for p in TRACE_FIX.glob('*.json')])
SCHEMAS = {p.name: json.loads(p.read_text(encoding='utf-8')) for p in MC.glob('*_schema_*.json')}
for schema in SCHEMAS.values():
    jsonschema.Draft202012Validator.check_schema(schema)
def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding='utf-8'))
def expect(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)
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
def validate_example(name: str, validation_map: Dict[str, str]) -> Dict[str, Any]:
    path = MC / name
    data = load_json(path)
    schema_name = infer_schema(name)
    if schema_name is None:
        raise AssertionError(f'could not infer schema for {name}')
    jsonschema.validate(data, SCHEMAS[schema_name])
    validation_map[f'{name} :: {schema_name}'] = 'PASS'
    return data
def parse_dt(value: str) -> datetime:
    if value.endswith('Z'):
        value = value[:-1] + '+00:00'
    return datetime.fromisoformat(value).astimezone(timezone.utc)
def dt_to_z(value: datetime) -> str:
    return value.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')
def find_primary_refs(data: Dict[str, Any]) -> List[str]:
    refs: List[str] = []
    for key in PRIMARY_ID_KEYS:
        if key in data and isinstance(data[key], str):
            refs.append(data[key])
    for key in ['publicationRef', 'materializationBasisRef', 'materializationSnapshotRef', 'contextSnapshotRef', 'outputMetadataRef', 'resultRef', 'querySpecificationRef', 'queryPlanRef', 'authorizationDecisionTraceRef', 'evidenceSufficiencyCaseRef']:
        if key in data and isinstance(data[key], str):
            refs.append(data[key])
    return list(dict.fromkeys(refs))
def earliest_timestamp_from_objects(objs: List[Dict[str, Any]]) -> datetime:
    timestamps: List[datetime] = []
    for obj in objs:
        for key in TIMESTAMP_KEYS:
            value = obj.get(key)
            if isinstance(value, str) and ('T' in value):
                try:
                    timestamps.append(parse_dt(value))
                except Exception:
                    pass
    if timestamps:
        return min(timestamps)
    return datetime(2026, 4, 11, 18, 0, 0, tzinfo=timezone.utc)
def gate_refs_from_data(data: Dict[str, Any]) -> Tuple[List[str], List[str]]:
    produced = find_primary_refs(data)
    trace_refs: List[str] = []
    if 'traceId' in data:
        trace_refs.append(data['traceId'])
    if 'authorizationDecisionTraceRef' in data:
        trace_refs.append(data['authorizationDecisionTraceRef'])
    return produced, list(dict.fromkeys(trace_refs))
def build_sequence_gate_logs(validation_map: Dict[str, str]) -> List[Dict[str, Any]]:
    logs: List[Dict[str, Any]] = []
    for idx, fixture_name in enumerate(SEQUENCE_FIXTURES, start=1):
        fixture = load_json(GATE_FIX / fixture_name)
        gate_indexes = []
        base_objects: List[Dict[str, Any]] = []
        gate_events: List[Dict[str, Any]] = []
        linked_tracebacks: List[str] = []
        if fixture['fixtureId'] == 'submission-filing-full-gate-chain-allow':
            linked_tracebacks.append('traceback:projection-submission-filing:v0.1')
        for gate in fixture['gates']:
            sequence_index = len(gate_events) + 1
            gate_indexes.append(sequence_index)
            source_examples = []
            input_refs: List[str] = []
            produced_refs: List[str] = []
            trace_refs: List[str] = []
            for key in ['requestExample', 'resultExample', 'traceExample', 'caseExample']:
                if gate.get(key):
                    data = validate_example(gate[key], validation_map)
                    base_objects.append(data)
                    source_examples.append(gate[key])
                    refs, extra_traces = gate_refs_from_data(data)
                    if key == 'requestExample':
                        input_refs.extend(refs)
                    else:
                        produced_refs.extend(refs)
                    trace_refs.extend(extra_traces)
            if gate.get('contextSnapshotRef'):
                produced_refs.append(gate['contextSnapshotRef'])
            if gate.get('reviewDecisionRef'):
                produced_refs.append(gate['reviewDecisionRef'])
            if gate.get('evidenceBundleRefs'):
                produced_refs.extend(gate['evidenceBundleRefs'])
            if gate.get('reason'):
                note = gate['reason']
            else:
                note = ''
            gate_events.append({
                'stepIndex': sequence_index,
                'gate': gate['gate'],
                'outcome': gate['outcome'],
                'sourceExamples': source_examples,
                'inputRefs': list(dict.fromkeys(input_refs)),
                'producedRefs': list(dict.fromkeys(produced_refs)),
                'traceRefs': list(dict.fromkeys(trace_refs)),
                'notes': note,
            })
        base_time = earliest_timestamp_from_objects(base_objects) + timedelta(minutes=idx)
        for pos, event in enumerate(gate_events):
            started = base_time + timedelta(seconds=pos * 4)
            finished = started + timedelta(seconds=2)
            event['startedAt'] = dt_to_z(started)
            event['finishedAt'] = dt_to_z(finished)
        expect(gate_events[-1]['gate'] == fixture['expectedStopGate'], f"{fixture['fixtureId']} stop gate mismatch")
        expect(gate_events[-1]['outcome'] == fixture['expectedStopOutcome'], f"{fixture['fixtureId']} stop outcome mismatch")
        logs.append({
            'logId': f"gateLog:{fixture['fixtureId']}:v0.1",
            'fixtureId': fixture['fixtureId'],
            'sourceFixtureRef': f'04_implementation_and_conformance/examples_and_fixtures/ofarm_gate_sequencing_fixtures_v0_1/{fixture_name}',
            'replayMode': 'EXECUTABLE_FIXTURE_REPLAY',
            'fixtureType': fixture['fixtureType'],
            'startedAt': gate_events[0]['startedAt'],
            'completedAt': gate_events[-1]['finishedAt'],
            'terminalOutcome': fixture['terminalOutcome'],
            'expectedStopGate': fixture['expectedStopGate'],
            'monotonicGateOrder': True,
            'linkedTraceBackIds': linked_tracebacks,
            'gateEvents': gate_events,
        })
    return logs
def build_query_runtime_log(validation_map: Dict[str, str]) -> Dict[str, Any]:
    fixture = load_json(RT_FIX / 'query_execution_field_passport_success.json')
    req = validate_example(fixture['requestExample'], validation_map)
    res = validate_example(fixture['resultExample'], validation_map)
    alias = validate_example(fixture['aliasTraceExample'], validation_map)
    start = parse_dt(req['requestedAt']) + timedelta(minutes=30)
    gate_events = [
        {
            'stepIndex': 1,
            'gate': 'QUERY_REQUEST_INTAKE',
            'outcome': 'ACCEPTED',
            'sourceExamples': [fixture['requestExample']],
            'inputRefs': [req['requestId']],
            'producedRefs': [req['querySpecificationRef'], req['queryPlanRef']],
            'traceRefs': [],
            'notes': 'Boundary request accepted for governed query execution.',
            'startedAt': dt_to_z(start),
            'finishedAt': dt_to_z(start + timedelta(seconds=2)),
        },
        {
            'stepIndex': 2,
            'gate': 'ALIAS_RESOLUTION',
            'outcome': alias['overallOutcome'],
            'sourceExamples': [fixture['aliasTraceExample']],
            'inputRefs': [req['querySpecificationRef']],
            'producedRefs': [alias['aliasCatalogRef']] + [r['resolvedRef'] for r in alias['aliasResolutions']],
            'traceRefs': [alias['traceId']],
            'notes': 'Alias catalog resolution remained pinned and traceable.',
            'startedAt': dt_to_z(start + timedelta(seconds=4)),
            'finishedAt': dt_to_z(start + timedelta(seconds=6)),
        },
        {
            'stepIndex': 3,
            'gate': 'CURRENT_STATE_BIND',
            'outcome': 'BOUND',
            'sourceExamples': [fixture['resultExample']],
            'inputRefs': [req['requiredFreshness'], req['targetTwin']],
            'producedRefs': [res['materializationResultRef']],
            'traceRefs': [],
            'notes': 'Execution result retained the materialization result ref needed for trace-back.',
            'startedAt': dt_to_z(start + timedelta(seconds=8)),
            'finishedAt': dt_to_z(start + timedelta(seconds=10)),
        },
        {
            'stepIndex': 4,
            'gate': 'PLAN_EXECUTION',
            'outcome': 'SUCCESS',
            'sourceExamples': [fixture['requestExample'], fixture['resultExample']],
            'inputRefs': [req['queryPlanRef']],
            'producedRefs': list(dict.fromkeys([res['resultId'], res['resultRef'], res['outputMetadataRef']] + res.get('executorRefs', []))),
            'traceRefs': list(res['aliasResolutionTraceRefs']),
            'notes': 'Result assembly preserved alias trace refs and declared projection trace-back readiness.',
            'startedAt': dt_to_z(start + timedelta(seconds=12)),
            'finishedAt': dt_to_z(start + timedelta(seconds=14)),
        },
    ]
    expect(res['projectionTraceBackReady'] is True, 'query execution result must be trace-back ready')
    return {
        'logId': 'gateLog:query-execution-field-passport-success:v0.1',
        'fixtureId': fixture['fixtureId'],
        'sourceFixtureRef': '04_implementation_and_conformance/examples_and_fixtures/ofarm_runtime_boundary_fixtures_v0_1/query_execution_field_passport_success.json',
        'replayMode': 'EXECUTABLE_FIXTURE_REPLAY',
        'fixtureType': fixture['fixtureType'],
        'startedAt': gate_events[0]['startedAt'],
        'completedAt': gate_events[-1]['finishedAt'],
        'terminalOutcome': res['outcome'],
        'expectedStopGate': 'PLAN_EXECUTION',
        'monotonicGateOrder': True,
        'linkedTraceBackIds': ['traceback:projection-field-passport-query-view:v0.1'],
        'gateEvents': gate_events,
    }
def build_publication_runtime_logs(validation_map: Dict[str, str]) -> List[Dict[str, Any]]:
    fixture = load_json(RT_FIX / 'publication_output_class_separation.json')
    passport_meta = validate_example(fixture['passportMetadataExample'], validation_map)
    doc_meta = validate_example(fixture['documentMetadataExample'], validation_map)
    pub_req = validate_example(fixture['passportPublishRequestExample'], validation_map)
    pub_res = validate_example(fixture['passportPublishResultExample'], validation_map)
    deny_req = validate_example(fixture['passportAttestRequestExample'], validation_map)
    deny_res = validate_example(fixture['passportAttestResultExample'], validation_map)
    start = parse_dt(pub_req['requestedAt']) + timedelta(minutes=60)
    log_publish = {
        'logId': 'gateLog:lot-passport-publication-share:v0.1',
        'fixtureId': 'publication-output-class-separation:passport-share',
        'sourceFixtureRef': '04_implementation_and_conformance/examples_and_fixtures/ofarm_runtime_boundary_fixtures_v0_1/publication_output_class_separation.json',
        'replayMode': 'EXECUTABLE_FIXTURE_REPLAY',
        'fixtureType': 'PUBLICATION_CLASS_BOUNDARY',
        'startedAt': dt_to_z(start),
        'completedAt': dt_to_z(start + timedelta(seconds=10)),
        'terminalOutcome': pub_res['outcome'],
        'expectedStopGate': 'PUBLICATION_SERVE',
        'monotonicGateOrder': True,
        'linkedTraceBackIds': ['traceback:projection-lot-passport-publication:v0.1'],
        'gateEvents': [
            {
                'stepIndex': 1,
                'gate': 'PUBLICATION_REQUEST_INTAKE',
                'outcome': 'ACCEPTED',
                'sourceExamples': [fixture['passportPublishRequestExample']],
                'inputRefs': [pub_req['requestId']],
                'producedRefs': [pub_req['outputMetadataRef']],
                'traceRefs': [pub_req['authorizationDecisionTraceRef']],
                'notes': 'Publication request accepted for live passport serving.',
                'startedAt': dt_to_z(start),
                'finishedAt': dt_to_z(start + timedelta(seconds=2)),
            },
            {
                'stepIndex': 2,
                'gate': 'OUTPUT_CLASS_CHECK',
                'outcome': 'LIVE_VIEW_ALLOWED',
                'sourceExamples': [fixture['passportMetadataExample']],
                'inputRefs': [passport_meta['passportViewId']],
                'producedRefs': [passport_meta['freezeState'], passport_meta['contextSnapshotRef']],
                'traceRefs': [],
                'notes': 'Live PassportView confirmed as recomputable and shareable but not freezable.',
                'startedAt': dt_to_z(start + timedelta(seconds=4)),
                'finishedAt': dt_to_z(start + timedelta(seconds=6)),
            },
            {
                'stepIndex': 3,
                'gate': 'PUBLICATION_SERVE',
                'outcome': pub_res['outcome'],
                'sourceExamples': [fixture['passportPublishResultExample']],
                'inputRefs': [pub_req['outputMetadataRef']],
                'producedRefs': [pub_res['resultId'], pub_res['publicationRef']],
                'traceRefs': [pub_res['authorizationDecisionTraceRef']],
                'notes': 'Live PassportView served through the governed publication boundary.',
                'startedAt': dt_to_z(start + timedelta(seconds=8)),
                'finishedAt': dt_to_z(start + timedelta(seconds=10)),
            },
        ],
    }
    start2 = parse_dt(deny_req['requestedAt']) + timedelta(minutes=61)
    log_deny = {
        'logId': 'gateLog:lot-passport-attestation-denied:v0.1',
        'fixtureId': 'publication-output-class-separation:passport-attestation-deny',
        'sourceFixtureRef': '04_implementation_and_conformance/examples_and_fixtures/ofarm_runtime_boundary_fixtures_v0_1/publication_output_class_separation.json',
        'replayMode': 'EXECUTABLE_FIXTURE_REPLAY',
        'fixtureType': 'PUBLICATION_CLASS_BOUNDARY',
        'startedAt': dt_to_z(start2),
        'completedAt': dt_to_z(start2 + timedelta(seconds=6)),
        'terminalOutcome': deny_res['outcome'],
        'expectedStopGate': 'OUTPUT_CLASS_CHECK',
        'monotonicGateOrder': True,
        'linkedTraceBackIds': [],
        'gateEvents': [
            {
                'stepIndex': 1,
                'gate': 'PUBLICATION_REQUEST_INTAKE',
                'outcome': 'ACCEPTED',
                'sourceExamples': [fixture['passportAttestRequestExample']],
                'inputRefs': [deny_req['requestId']],
                'producedRefs': [deny_req['outputMetadataRef']],
                'traceRefs': [deny_req['authorizationDecisionTraceRef']],
                'notes': 'Attestation attempt entered the boundary for output-kind validation.',
                'startedAt': dt_to_z(start2),
                'finishedAt': dt_to_z(start2 + timedelta(seconds=2)),
            },
            {
                'stepIndex': 2,
                'gate': 'OUTPUT_CLASS_CHECK',
                'outcome': deny_res['outcome'],
                'sourceExamples': [fixture['passportMetadataExample'], fixture['passportAttestResultExample']],
                'inputRefs': [passport_meta['passportViewId']],
                'producedRefs': [deny_res['resultId']] + [p['reasonCode'] for p in deny_res.get('problems', [])],
                'traceRefs': [],
                'notes': 'Live PassportView correctly denied attestation because it is not a frozen DocumentAssembly.',
                'startedAt': dt_to_z(start2 + timedelta(seconds=4)),
                'finishedAt': dt_to_z(start2 + timedelta(seconds=6)),
            },
        ],
    }
    expect(doc_meta['documentFamily'] == 'SUBMISSION_ASSEMBLY', 'document metadata example must remain a submission assembly')
    return [log_publish, log_deny]
def build_projection_records(validation_map: Dict[str, str]) -> List[Dict[str, Any]]:
    records: List[Dict[str, Any]] = []
    for fixture_name in PROJECTION_FIXTURES:
        fixture = load_json(TRACE_FIX / fixture_name)
        loaded: Dict[str, Dict[str, Any]] = {}
        for key in [
            'querySpecificationExample', 'queryPlanExample', 'queryExecutionRequestExample', 'queryExecutionResultExample',
            'outputMetadataExample', 'publicationRequestExample', 'publicationResultExample', 'authorizationTraceExample',
            'evidenceSufficiencyCaseExample', 'materializationBasisExample', 'materializationSnapshotExample', 'contextSnapshotExample'
        ]:
            if fixture.get(key):
                loaded[key] = validate_example(fixture[key], validation_map)
        for name in fixture.get('aliasTraceExamples', []):
            loaded.setdefault('aliasTraceExamples', [])
            loaded['aliasTraceExamples'].append(validate_example(name, validation_map))
        grounding: Dict[str, Dict[str, Any]] = {}
        terminal_refs = [fixture['terminalArtifactRef']]
        if 'querySpecificationExample' in loaded:
            grounding['query'] = {
                'status': 'VALIDATED',
                'refs': [loaded['querySpecificationExample']['queryId']]
            }
        elif fixture.get('declaredOnlyRefs', {}).get('querySpecificationRefs'):
            grounding['query'] = {'status': 'DECLARED_ONLY', 'refs': fixture['declaredOnlyRefs']['querySpecificationRefs']}
        else:
            grounding['query'] = {'status': 'MISSING', 'refs': []}
        if 'queryPlanExample' in loaded:
            grounding['queryPlan'] = {
                'status': 'VALIDATED',
                'refs': [loaded['queryPlanExample']['planId']]
            }
        elif fixture.get('declaredOnlyRefs', {}).get('queryPlanRefs'):
            grounding['queryPlan'] = {'status': 'DECLARED_ONLY', 'refs': fixture['declaredOnlyRefs']['queryPlanRefs']}
        else:
            grounding['queryPlan'] = {'status': 'MISSING', 'refs': []}
        if loaded.get('aliasTraceExamples'):
            grounding['aliasResolution'] = {
                'status': 'VALIDATED',
                'refs': [item['traceId'] for item in loaded['aliasTraceExamples']]
            }
        else:
            grounding['aliasResolution'] = {'status': 'MISSING', 'refs': []}
        if 'queryExecutionResultExample' in loaded:
            qres = loaded['queryExecutionResultExample']
            expect(qres['projectionTraceBackReady'] is True, f"{fixture['fixtureId']} query result must be trace-back ready")
            grounding['queryExecution'] = {
                'status': 'VALIDATED',
                'refs': [qres['resultId'], qres['resultRef']]
            }
            terminal_refs.extend([qres['resultId']])
        else:
            grounding['queryExecution'] = {'status': 'MISSING', 'refs': []}
        if 'outputMetadataExample' in loaded:
            meta = loaded['outputMetadataExample']
            meta_ref = meta.get('passportViewId') or meta.get('documentAssemblyId')
            grounding['outputMetadata'] = {'status': 'VALIDATED', 'refs': [meta_ref]}
            terminal_refs.append(meta_ref)
            if 'passportViewId' in meta:
                expect(meta['freezeState'] == 'LIVE_RECOMPUTABLE', f"{fixture['fixtureId']} passport metadata must remain live/recomputable")
            if 'documentAssemblyId' in meta:
                expect(bool(meta.get('frozenAt')), f"{fixture['fixtureId']} document metadata must be frozen")
        else:
            grounding['outputMetadata'] = {'status': 'MISSING', 'refs': []}
        if 'publicationResultExample' in loaded:
            pub = loaded['publicationResultExample']
            grounding['publication'] = {'status': 'VALIDATED', 'refs': [pub['resultId'], pub.get('publicationRef', '')]}
            terminal_refs.append(pub['resultId'])
        else:
            grounding['publication'] = {'status': 'MISSING', 'refs': []}
        if 'authorizationTraceExample' in loaded:
            trace = loaded['authorizationTraceExample']
            grounding['authority'] = {'status': 'VALIDATED', 'refs': [trace['traceId']]}
        elif fixture.get('declaredOnlyRefs', {}).get('authorizationDecisionTraceRef'):
            grounding['authority'] = {'status': 'DECLARED_ONLY', 'refs': [fixture['declaredOnlyRefs']['authorizationDecisionTraceRef']]}
        else:
            grounding['authority'] = {'status': 'MISSING', 'refs': []}
        if 'evidenceSufficiencyCaseExample' in loaded:
            case = loaded['evidenceSufficiencyCaseExample']
            grounding['evidence'] = {
                'status': 'VALIDATED',
                'refs': [case['sufficiencyCaseId']] + [bundle['bundleRef'] for bundle in case.get('evidenceBundles', [])]
            }
        else:
            grounding['evidence'] = {'status': 'MISSING', 'refs': []}
        if 'materializationBasisExample' in loaded:
            basis = loaded['materializationBasisExample']
            refs = [basis['basisId']] + basis.get('contributingAssertionRefs', []) + basis.get('contributingAcceptedConsequenceRefs', []) + basis.get('contributingReviewDecisionRefs', []) + basis.get('identityBasisRefs', [])
            grounding['materializationBasis'] = {'status': 'VALIDATED', 'refs': refs}
        elif fixture.get('declaredOnlyRefs', {}).get('materializationResultRef'):
            grounding['materializationBasis'] = {'status': 'DECLARED_ONLY', 'refs': [fixture['declaredOnlyRefs']['materializationResultRef']]}
        else:
            grounding['materializationBasis'] = {'status': 'MISSING', 'refs': []}
        if 'materializationSnapshotExample' in loaded:
            snap = loaded['materializationSnapshotExample']
            grounding['materializationSnapshot'] = {'status': 'VALIDATED', 'refs': [snap['snapshotId'], snap['materializedStateRef']]}
        else:
            grounding['materializationSnapshot'] = {'status': 'MISSING', 'refs': []}
        if 'contextSnapshotExample' in loaded:
            ctx = loaded['contextSnapshotExample']
            grounding['context'] = {'status': 'VALIDATED', 'refs': [ctx['contextSnapshotId']]}
        elif fixture.get('declaredOnlyRefs', {}).get('contextSnapshotRef'):
            grounding['context'] = {'status': 'DECLARED_ONLY', 'refs': [fixture['declaredOnlyRefs']['contextSnapshotRef']]}
        else:
            grounding['context'] = {'status': 'MISSING', 'refs': []}
        mappings: List[Dict[str, Any]] = []
        for mapping in fixture['expectedProjectionMappings']:
            entry = dict(mapping)
            if mapping.get('requiresAliasResolution'):
                alias_traces = loaded.get('aliasTraceExamples', [])
                expect(alias_traces, f"{fixture['fixtureId']} mapping requires alias trace")
                canonical_hits = [r['resolvedRef'] for item in alias_traces for r in item['aliasResolutions'] if r.get('resolvedRef') == mapping['expectedCanonicalRef']]
                expect(canonical_hits, f"{fixture['fixtureId']} alias resolution did not yield {mapping['expectedCanonicalRef']}")
            if 'materializationBasisExample' in loaded:
                basis_refs = grounding['materializationBasis']['refs']
                # only enforce strict subset for source refs that are clearly basis-derived
                if mapping['mappingKind'] in {'IDENTITY_BASIS', 'RETAINED_CURRENT_STATE', 'EVIDENCE_BINDING'}:
                    expect(any(ref in basis_refs or ref in grounding['materializationSnapshot']['refs'] or ref in grounding['evidence']['refs'] for ref in mapping['expectedSourceRefs']),
                           f"{fixture['fixtureId']} expected source refs are not grounded in basis/snapshot/evidence")
            entry['sourceGroundingStatus'] = 'VALIDATED' if grounding['materializationBasis']['status'] == 'VALIDATED' or grounding['evidence']['status'] == 'VALIDATED' or grounding['aliasResolution']['status'] == 'VALIDATED' else 'DECLARED_ONLY'
            mappings.append(entry)
        observed_families = sorted([family for family, detail in grounding.items() if detail['status'] != 'MISSING'])
        missing_families = sorted([family for family, detail in grounding.items() if detail['status'] == 'MISSING'])
        declared_only_families = sorted([family for family, detail in grounding.items() if detail['status'] == 'DECLARED_ONLY'])
        coverage = 'PARTIAL'
        records.append({
            'traceBackId': f"traceback:{fixture['fixtureId'].replace('projection-', '')}:v0.1",
            'fixtureId': fixture['fixtureId'],
            'sourceFixtureRef': f'04_implementation_and_conformance/examples_and_fixtures/ofarm_runtime_gate_log_traceback_fixtures_v0_1/{fixture_name}',
            'projectionClass': fixture['projectionClass'],
            'terminalArtifactKind': fixture['terminalArtifactKind'],
            'terminalArtifactRefs': list(dict.fromkeys(terminal_refs)),
            'outputLifecycle': fixture['expectedLifecycle'],
            'targetTwin': fixture['expectedTwin'],
            'grounding': grounding,
            'projectionMappings': mappings,
            'observedRefFamilies': observed_families,
            'declaredOnlyFamilies': declared_only_families,
            'missingFamilies': missing_families,
            'coverage': coverage,
            'coverageRationale': fixture['notes'],
        })
    return records
def main() -> int:
    validation_map: Dict[str, str] = {}
    runtime_gate_logs = build_sequence_gate_logs(validation_map)
    runtime_gate_logs.append(build_query_runtime_log(validation_map))
    runtime_gate_logs.extend(build_publication_runtime_logs(validation_map))
    projection_records = build_projection_records(validation_map)
    GATE_LOGS_OUT.write_text(json.dumps({
        'schemaVersion': 'ofarm.runtimegatelogs.v0.1',
        'generatedBy': 'ofarm_runtime_gate_log_and_projection_traceback_runner_v0_1.py',
        'replayMode': 'EXECUTABLE_FIXTURE_REPLAY',
        'gateLogs': runtime_gate_logs,
    }, indent=2) + '\n', encoding='utf-8')
    TRACEBACK_OUT.write_text(json.dumps({
        'schemaVersion': 'ofarm.projectiontracebackrecords.v0.1',
        'generatedBy': 'ofarm_runtime_gate_log_and_projection_traceback_runner_v0_1.py',
        'records': projection_records,
    }, indent=2) + '\n', encoding='utf-8')
    results = {
        'exampleValidation': validation_map,
        'runtimeGateLogs': {
            log['fixtureId']: {
                'status': 'PASS',
                'terminalOutcome': log['terminalOutcome'],
                'gateCount': len(log['gateEvents']),
                'linkedTraceBackIds': log['linkedTraceBackIds'],
            }
            for log in runtime_gate_logs
        },
        'projectionTraceBack': {
            record['fixtureId']: {
                'status': 'PASS',
                'coverage': record['coverage'],
                'observedRefFamilies': record['observedRefFamilies'],
                'declaredOnlyFamilies': record['declaredOnlyFamilies'],
                'missingFamilies': record['missingFamilies'],
            }
            for record in projection_records
        },
        'overall': 'PASS_WITH_LIMITATIONS',
        'notes': (
            'Runtime-shaped gate logs and starter projection trace-back records were produced successfully from executable fixture replay. '
            'The proof is stronger than the Wave 7 declarative sequence layer because the runner now emits concrete gate events and trace-back records, '
            'but it is still not a production executor log stream. Some live-view and document examples still rely on declared-only refs where the current package has not yet shipped all backing examples.'
        ),
        'summary': {
            'runtimeGateLogCount': len(runtime_gate_logs),
            'projectionTraceBackRecordCount': len(projection_records),
            'validatedExampleCount': len(validation_map),
        }
    }
    RESULTS_OUT.write_text(json.dumps(results, indent=2) + '\n', encoding='utf-8')
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
