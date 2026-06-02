#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
import jsonschema

ROOT = Path(__file__).resolve().parents[1]
MC = ROOT / '03_machine_contracts'
IMPL = ROOT / '04_implementation_and_conformance'
RECORDS = IMPL / 'OFARM_agronomic_query_output_reconstruction_records_v0_1.json'
SCENARIOS = IMPL / 'OFARM_agronomic_scenario_records_v0_1.json'
RESULTS = IMPL / 'OFARM_agronomic_query_output_reconstruction_results_v0_1.json'


def load(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def validate_file(file_name: str, schema_name: str, result: dict):
    data = load(MC / file_name)
    schema = load(MC / schema_name)
    jsonschema.validate(data, schema)
    result['schemaValidation'].append({'file': file_name, 'schema': schema_name, 'status': 'PASS'})
    return data


def main() -> int:
    records = load(RECORDS)
    phase1 = load(SCENARIOS)
    expected_scenarios = {s['scenarioId'] for s in phase1.get('scenarios', [])}
    covered_scenarios = {c['phase1ScenarioId'] for c in records['coverage']}
    result = {'runner': Path(__file__).name, 'fixtureSetId': records['fixtureSetId'], 'schemaValidation': [], 'coverageChecks': [], 'behaviorChecks': [], 'overall': 'PASS'}
    try:
        jsonschema.Draft202012Validator.check_schema(load(MC / records['policySchemaRef']))
        jsonschema.Draft202012Validator.check_schema(load(MC / records['traceSchemaRef']))
        result['schemaValidation'].append({'file': records['policySchemaRef'], 'schema': 'JSON_SCHEMA_DRAFT_2020_12', 'status': 'PASS'})
        result['schemaValidation'].append({'file': records['traceSchemaRef'], 'schema': 'JSON_SCHEMA_DRAFT_2020_12', 'status': 'PASS'})
        for p in records['policyExamples']:
            validate_file(p, records['policySchemaRef'], result)
        for t in records['traceExamples']:
            validate_file(t, records['traceSchemaRef'], result)
        validate_file(records['aliasCatalogExample'], 'OFARM_SemanticPathAliasCatalog_schema_v0_1.json', result)
        schema_by_field = {
            'querySpecificationExample': 'OFARM_QuerySpecification_schema_v0_1.json',
            'queryPlanExample': 'OFARM_QueryPlanIR_schema_v0_1.json',
            'queryExecutionRequestExample': 'OFARM_QueryExecutionRequest_schema_v0_1.json',
            'queryExecutionResultExample': 'OFARM_QueryExecutionResult_schema_v0_1.json',
            'passportViewMetadataExample': 'OFARM_PassportViewMetadata_schema_v0_1.json',
            'documentAssemblyMetadataExample': 'OFARM_DocumentAssemblyMetadata_schema_v0_1.json',
            'reconstructionTraceExample': records['traceSchemaRef']
        }
        for case in records['coverage']:
            for field, schema in schema_by_field.items():
                if field in case:
                    validate_file(case[field], schema, result)
        for out in records.get('outputExamples', []):
            schema = 'OFARM_PassportViewMetadata_schema_v0_1.json' if 'PassportViewMetadata' in out else 'OFARM_DocumentAssemblyMetadata_schema_v0_1.json'
            validate_file(out, schema, result)
        coverage_ok = expected_scenarios <= covered_scenarios
        result['coverageChecks'].append({'check': 'all_phase1_scenarios_have_reconstruction_case', 'expectedCount': len(expected_scenarios), 'coveredCount': len(covered_scenarios), 'status': 'PASS' if coverage_ok else 'FAIL'})
        if not coverage_ok:
            result['overall'] = 'FAIL'
        query_files = {c['querySpecificationExample'] for c in records['coverage']}
        result['coverageChecks'].append({'check': 'ten_reconstruction_query_specs_present', 'count': len(query_files), 'status': 'PASS' if len(query_files) >= 10 else 'FAIL'})
        if len(query_files) < 10:
            result['overall'] = 'FAIL'
        # Behavior checks.
        stale_case = next(c for c in records['coverage'] if c['phase1ScenarioId'] == 'AGR-SCEN-009')
        stale_result = load(MC / stale_case['queryExecutionResultExample'])
        stale_trace = load(MC / stale_case['reconstructionTraceExample'])
        stale_ok = stale_result['outcome'] == 'REFUSED' and stale_trace['traceOutcome'] == 'REFUSE_OUTPUT' and any(p.get('reasonCode') == 'STALE_MATERIALIZATION_HIGH_CONSEQUENCE' for p in stale_result.get('problems', []))
        result['behaviorChecks'].append({'check': 'stale_high_consequence_materialization_refused', 'status': 'PASS' if stale_ok else 'FAIL'})
        if not stale_ok:
            result['overall'] = 'FAIL'
        passport = load(MC / 'OFARM_PassportViewMetadata_example_field_17_mixed_crop_cycle_disclosure_v0_1.json')
        passport_ok = passport['freezeState'] == 'LIVE_RECOMPUTABLE' and 'mixed' in passport.get('notes', '').lower() and 'reconstructionTraceRef' in passport
        result['behaviorChecks'].append({'check': 'passport_view_live_and_reconstruction_traced', 'status': 'PASS' if passport_ok else 'FAIL'})
        if not passport_ok:
            result['overall'] = 'FAIL'
        document = load(MC / 'OFARM_DocumentAssemblyMetadata_example_field_17_agronomic_audit_dossier_disputed_annex_v0_1.json')
        doc_ok = document['reviewState'] in ('APPROVED', 'ATTESTED', 'FILED') and 'annex' in document.get('notes', '').lower() and document.get('reconstructionTraceRefs')
        result['behaviorChecks'].append({'check': 'document_assembly_frozen_with_disputed_annex_trace', 'status': 'PASS' if doc_ok else 'FAIL'})
        if not doc_ok:
            result['overall'] = 'FAIL'
        policies = [load(MC / p) for p in records['policyExamples']]
        high_policy_ok = any(p['scope']['truthScope'] == 'COMPLIANCE' and p['materializationPolicy']['freshnessPolicy'] == 'REQUIRE_FRESH' and p['outputPolicy']['requiresTraceBack'] is True for p in policies)
        result['behaviorChecks'].append({'check': 'high_consequence_policy_requires_freshness_and_traceback', 'status': 'PASS' if high_policy_ok else 'FAIL'})
        if not high_policy_ok:
            result['overall'] = 'FAIL'
        trace_policy_ok = True
        for t in records['traceExamples']:
            trace = load(MC / t)
            if trace['policyRef'] not in {p['policyId'] for p in policies}:
                trace_policy_ok = False
        result['behaviorChecks'].append({'check': 'reconstruction_traces_reference_known_policy_examples', 'status': 'PASS' if trace_policy_ok else 'FAIL'})
        if not trace_policy_ok:
            result['overall'] = 'FAIL'
    except Exception as exc:
        result['overall'] = 'FAIL'
        result.setdefault('errors', []).append(str(exc))
    RESULTS.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(RESULTS)
    print(result['overall'])
    return 0 if result['overall'] == 'PASS' else 1

if __name__ == '__main__':
    raise SystemExit(main())
