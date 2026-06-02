#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from jsonschema import Draft202012Validator

REPO = Path(__file__).resolve().parents[6]
SCHEMA_DIR = REPO / '03_machine_contracts/schemas/runtime_surface'
EX_DIR = REPO / '04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/runtime_surface'
NEG_DIR = REPO / '04_implementation_and_conformance/controlled_promotion_evidence/agentic_ai_world_model_amendment_v0_1/controlled_promotion/AAI-CP2_public_surface_preflight_trace_result_qualification_v0_1/examples/negative'
REPORT = REPO / '04_implementation_and_conformance/controlled_promotion_evidence/agentic_ai_world_model_amendment_v0_1/controlled_promotion/AAI-CP2_public_surface_preflight_trace_result_qualification_v0_1/conformance/validation_report.json'

POSITIVE = {
  'OFARM_PublicOperationDescriptor_example_queries_execute_public_v0_1.json': 'OFARM_PublicOperationDescriptor_schema_v0_1.json',
  'OFARM_PreflightRequest_example_commit_submit_field17_v0_1.json': 'OFARM_PreflightRequest_schema_v0_1.json',
  'OFARM_PreflightResult_example_blocked_missing_evidence_v0_1.json': 'OFARM_PreflightResult_schema_v0_1.json',
  'OFARM_RuntimeProblemReasonCodeRegistry_example_cp2_core_v0_1.json': 'OFARM_RuntimeProblemReasonCodeRegistry_schema_v0_1.json',
  'OFARM_ResultQualificationEnvelope_example_blocked_high_consequence_v0_1.json': 'OFARM_ResultQualificationEnvelope_schema_v0_1.json',
  'OFARM_TraceRetrievalResult_example_preflight_gate_outcomes_v0_1.json': 'OFARM_TraceRetrievalResult_schema_v0_1.json',
  'OFARM_PublicReadModelEnvelope_example_daily_brief_qualified_v0_1.json': 'OFARM_PublicReadModelEnvelope_schema_v0_1.json',
  'OFARM_SourceFidelityEnvelope_example_sensor_import_managed_loss_v0_1.json': 'OFARM_SourceFidelityEnvelope_schema_v0_1.json',
}


def load(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def schema_validate(schema_name: str, payload: dict) -> list[str]:
    schema = load(SCHEMA_DIR / schema_name)
    return [e.message for e in Draft202012Validator(schema).iter_errors(payload)]


def policy_fail_reason(payload: dict) -> str | None:
    obj = payload.get('payload', payload)
    schema_under_test = payload.get('schemaUnderTest', '')
    if 'PublicOperationDescriptor' in schema_under_test or obj.get('schemaVersion') == 'ofarm.publicoperationdescriptor.v0.1':
        if obj.get('consequenceClass') in {'STATE_AFFECTING', 'HIGH_CONSEQUENCE', 'PUBLICATION_AFFECTING'} and (not obj.get('preflightRequired') or not obj.get('traceRequired')):
            return 'high-consequence/state-affecting operation lacks preflight or trace requirement'
    if 'ResultQualificationEnvelope' in schema_under_test or obj.get('schemaVersion') == 'ofarm.resultqualificationenvelope.v0.1':
        if obj.get('highConsequenceUseAllowed') and (obj.get('stalenessClass') in {'STALE_BLOCKING', 'INVALIDATED', 'UNKNOWN'} or obj.get('evidenceSufficiency') in {'INSUFFICIENT', 'MISSING', 'REDACTED', 'REVIEW_REQUIRED'}):
            return 'qualification overstates high-consequence use despite stale/evidence limits'
    if 'PublicReadModelEnvelope' in schema_under_test or obj.get('schemaVersion') == 'ofarm.publicreadmodelenvelope.v0.1':
        q = obj.get('qualification', {})
        if q.get('highConsequenceUseAllowed') and (q.get('stalenessClass') in {'STALE_BLOCKING', 'INVALIDATED', 'UNKNOWN'} or q.get('evidenceSufficiency') in {'INSUFFICIENT', 'MISSING', 'REDACTED', 'REVIEW_REQUIRED'}):
            return 'public read model hides material qualification limits'
    if 'TraceRetrievalResult' in schema_under_test or obj.get('schemaVersion') == 'ofarm.traceretrievalresult.v0.1':
        if obj.get('status') in {'ACCESS_DENIED', 'REDACTED', 'PARTIALLY_REDACTED'} and not obj.get('problems') and not obj.get('redactions'):
            return 'trace retrieval redaction/access denial lacks safe explanation'
    if 'SourceFidelityEnvelope' in schema_under_test or obj.get('schemaVersion') == 'ofarm.sourcefidelityenvelope.v0.1':
        pe = obj.get('promotionEligibility', {})
        if obj.get('fidelityPosture') in {'MATERIAL_LOSS', 'HIGH_RISK_LOSS', 'UNKNOWN'} and pe.get('highConsequenceUseAllowed'):
            return 'lossy source fidelity marked high-consequence eligible'
    if 'RuntimeProblemReasonCodeRegistry' in schema_under_test or obj.get('schemaVersion') == 'ofarm.runtimeproblemreasoncoderegistry.v0.1':
        for rc in obj.get('reasonCodes', []):
            combined = (rc.get('safeUiBehavior', '') + ' ' + rc.get('safeUserMessage', '')).lower()
            if rc.get('family') == 'PERMISSION_REDACTION' and ('no data' in combined or 'no records' in combined):
                return 'permission/redaction code may be displayed as absent data'
    return None


def main() -> int:
    records = []
    failures = []
    for example_name, schema_name in POSITIVE.items():
        payload = load(EX_DIR / example_name)
        errors = schema_validate(schema_name, payload)
        policy = policy_fail_reason(payload)
        status = 'PASS' if not errors and policy is None else 'FAIL'
        if status != 'PASS':
            failures.append(example_name)
        records.append({'id': example_name, 'kind': 'positive_schema_and_policy', 'schema': schema_name, 'status': status, 'errors': errors, 'policyFailure': policy})
    for path in sorted(NEG_DIR.glob('*.json')):
        wrapper = load(path)
        schema_name = Path(wrapper['schemaUnderTest']).name
        errors = schema_validate(schema_name, wrapper['payload'])
        policy = policy_fail_reason(wrapper)
        expected = wrapper.get('expectedConformance')
        if expected == 'FAIL_SCHEMA':
            status = 'PASS' if errors else 'FAIL'
        elif expected == 'FAIL_POLICY':
            status = 'PASS' if policy else 'FAIL'
        else:
            status = 'FAIL'
        if status != 'PASS':
            failures.append(path.name)
        records.append({'id': path.name, 'kind': 'negative', 'expected': expected, 'schema': schema_name, 'status': status, 'schemaErrors': errors, 'policyFailure': policy})
    report = {
        'schemaVersion': 'ofarm.aai.cp2.validation_report.v0.1',
        'generatedAt': '2026-05-16T14:00:00+02:00',
        'runner': 'ofarm_aai_cp2_public_surface_contract_runner_v0_1.py',
        'status': 'PASS' if not failures else 'FAIL',
        'records': records,
        'failures': failures,
        'nonClaims': ['runtime readiness not claimed', 'two-agent compatibility not claimed', 'production readiness not claimed']
    }
    REPORT.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'status': report['status'], 'records': len(records), 'failures': failures}, indent=2))
    return 0 if not failures else 1

if __name__ == '__main__':
    raise SystemExit(main())
