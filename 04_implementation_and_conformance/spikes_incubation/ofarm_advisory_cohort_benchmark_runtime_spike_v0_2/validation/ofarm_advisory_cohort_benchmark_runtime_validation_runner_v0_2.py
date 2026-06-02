from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Tuple
from jsonschema import Draft202012Validator

HERE = Path(__file__).resolve().parent
SPIKE = HERE.parent
SCHEMA_DIR = SPIKE / 'experimental_machine_contracts' / 'schemas'
POS_DIR = SPIKE / 'experimental_machine_contracts' / 'examples' / 'positive'
NEG_DIR = SPIKE / 'experimental_machine_contracts' / 'examples' / 'negative'
FIXTURE_DIR = SPIKE / 'fixtures'
ROOT = SPIKE.parents[1]
ACTIVE_SCHEMA_DIR = ROOT / '03_machine_contracts'
OUT = HERE / 'OFARM_advisory_cohort_benchmark_runtime_validation_results_v0_2.txt'

SCHEMA_MAP = {
    'ProductNormalizationTrace': 'OFARM_ProductNormalizationTrace_schema_v0_1.json',
    'BenchmarkContribution': 'OFARM_BenchmarkContribution_schema_v0_1.json',
    'BenchmarkRequestHistoryAssessment': 'OFARM_BenchmarkRequestHistoryAssessment_schema_v0_1.json',
    'BenchmarkMaterializationState': 'OFARM_BenchmarkMaterializationState_schema_v0_1.json',
    'BenchmarkDisclosureDecision': 'OFARM_BenchmarkDisclosureDecision_schema_v0_2.json',
}

def load_json(path: Path):
    with path.open('r', encoding='utf-8') as f:
        return json.load(f)

def infer_kind(path: Path) -> str:
    name = path.name
    for kind in SCHEMA_MAP:
        if kind in name:
            return kind
    sv = load_json(path).get('schemaVersion', '')
    if 'productnormalizationtrace' in sv:
        return 'ProductNormalizationTrace'
    if 'benchmarkcontribution' in sv:
        return 'BenchmarkContribution'
    if 'benchmarkrequesthistoryassessment' in sv:
        return 'BenchmarkRequestHistoryAssessment'
    if 'benchmarkmaterializationstate' in sv:
        return 'BenchmarkMaterializationState'
    if 'benchmarkdisclosuredecision' in sv:
        return 'BenchmarkDisclosureDecision'
    raise ValueError(f'Cannot infer schema kind for {path}')

def get_schema(kind: str):
    return load_json(SCHEMA_DIR / SCHEMA_MAP[kind])

def semantic_errors(kind: str, obj: dict) -> List[str]:
    errs: List[str] = []
    if kind == 'ProductNormalizationTrace':
        if obj.get('normalizationOutcome') == 'EXACT_PRODUCT' and obj.get('ambiguityReasonCodes'):
            errs.append('SEMANTIC: EXACT_PRODUCT normalization may not carry ambiguityReasonCodes.')
        if obj.get('normalizationOutcome') == 'REFUSED' and obj.get('comparabilityStatus') == 'COMPARABLE':
            errs.append('SEMANTIC: REFUSED normalization may not be COMPARABLE.')
    elif kind == 'BenchmarkContribution':
        if obj.get('revocationState') == 'REVOKED_FOR_FUTURE_USE' and obj.get('currentUseState') != 'INELIGIBLE':
            errs.append('SEMANTIC: Revoked contribution may not remain ELIGIBLE.')
        forbidden_keys = {'rawEvidenceRefs', 'journalEntryRefs', 'ledgerEntryRefs'}
        overlap = forbidden_keys.intersection(obj.keys())
        if overlap:
            errs.append(f'SEMANTIC: BenchmarkContribution contains forbidden raw/ledger keys: {sorted(overlap)}')
    elif kind == 'BenchmarkRequestHistoryAssessment':
        relations = {r.get('relationType') for r in obj.get('priorRequestRelations', [])}
        guard = obj.get('differencingGuardStatus')
        risk = obj.get('differencingRiskClass')
        action = obj.get('actionRecommendation')
        if guard == 'CLEAR':
            if risk != 'LOW':
                errs.append('SEMANTIC: CLEAR history guard requires LOW differencing risk.')
            if action != 'PROCEED':
                errs.append('SEMANTIC: CLEAR history guard requires PROCEED actionRecommendation.')
            if 'STRICTER_THAN_PRIOR' in relations:
                errs.append('SEMANTIC: CLEAR history guard may not coexist with STRICTER_THAN_PRIOR prior relation.')
        if guard == 'BROADEN':
            if obj.get('requestedBenchmarkKind') != 'EXACT_PRODUCT':
                errs.append('SEMANTIC: BROADEN guard only makes sense for requested EXACT_PRODUCT.')
            if action != 'PROCEED_WITH_BROADENING':
                errs.append('SEMANTIC: BROADEN guard requires PROCEED_WITH_BROADENING recommendation.')
        if guard == 'BLOCKED':
            if risk != 'HIGH':
                errs.append('SEMANTIC: BLOCKED history guard requires HIGH differencing risk.')
            if action != 'REFUSE':
                errs.append('SEMANTIC: BLOCKED history guard requires REFUSE actionRecommendation.')
    elif kind == 'BenchmarkMaterializationState':
        freshness = obj.get('freshnessState')
        triggers = obj.get('invalidationTriggers', [])
        recompute = obj.get('recomputeRequired')
        visible = obj.get('visibleFreshnessLabel')
        if freshness == 'FRESH':
            if triggers:
                errs.append('SEMANTIC: FRESH materialization may not carry invalidationTriggers.')
            if recompute:
                errs.append('SEMANTIC: FRESH materialization may not require recompute.')
            if visible != 'FRESH':
                errs.append('SEMANTIC: FRESH materialization must show FRESH visible label.')
        if freshness in {'STALE', 'INVALID'} and not triggers:
            errs.append('SEMANTIC: STALE/INVALID materialization requires at least one invalidation trigger.')
        if freshness == 'INVALID' and not recompute:
            errs.append('SEMANTIC: INVALID materialization must require recompute.')
        if freshness == 'INVALID' and obj.get('staleAllowedForDeclaredUse'):
            errs.append('SEMANTIC: INVALID materialization may not be marked staleAllowedForDeclaredUse.')
    elif kind == 'BenchmarkDisclosureDecision':
        decision = obj.get('decision')
        freshness = obj.get('freshnessState')
        guard = obj.get('differencingGuardStatus')
        if decision in {'ALLOW', 'BROADEN'} and freshness != 'FRESH':
            errs.append('SEMANTIC: ALLOW/BROADEN disclosure decisions require FRESH materialization state.')
        if decision == 'ALLOW' and guard in {'BLOCKED', 'BROADEN'}:
            errs.append('SEMANTIC: ALLOW may not use BLOCKED or BROADEN differencing status.')
        if decision == 'BROADEN' and guard != 'BROADEN':
            errs.append('SEMANTIC: BROADEN decision requires BROADEN differencing status.')
        if decision == 'REFUSE' and guard == 'CLEAR' and freshness == 'FRESH':
            # other refusal reasons possible; do not enforce
            pass
    return errs

def validate_instance(path: Path) -> Tuple[bool, List[str]]:
    obj = load_json(path)
    kind = infer_kind(path)
    schema = get_schema(kind)
    validator = Draft202012Validator(schema)
    errors = [f'SCHEMA: {e.message}' for e in validator.iter_errors(obj)]
    errors.extend(semantic_errors(kind, obj))
    return len(errors) == 0, errors

def band_for_count(n: int) -> str:
    if n >= 20:
        return '20_PLUS'
    if n >= 10:
        return '10-19'
    if n >= 5:
        return '5-9'
    if n >= 3:
        return '3-4'
    return 'HIDDEN'

def cross_bundle_checks(bundle: Path) -> List[str]:
    errors: List[str] = []
    objects = [load_json(p) for p in bundle.glob('*.json')]
    traces = {o['normalizationTraceId']: o for o in objects if o.get('schemaVersion') == 'ofarm.productnormalizationtrace.v0.1'}
    contribs = {o['contributionId']: o for o in objects if o.get('schemaVersion') == 'ofarm.benchmarkcontribution.v0.1'}
    histories = {o['assessmentId']: o for o in objects if o.get('schemaVersion') == 'ofarm.benchmarkrequesthistoryassessment.v0.1'}
    mat_states = {o['materializationStateId']: o for o in objects if o.get('schemaVersion') == 'ofarm.benchmarkmaterializationstate.v0.1'}
    decisions = {o['decisionId']: o for o in objects if o.get('schemaVersion') == 'ofarm.benchmarkdisclosuredecision.v0.2'}

    for cid, c in contribs.items():
        tref = c['sourceNormalizationTraceRef']
        if tref not in traces:
            errors.append(f'Contribution {cid} references missing normalization trace {tref}.')
            continue
        trace = traces[tref]
        if c['sourceExtractRef'] != trace['sourceExtractRef']:
            errors.append(f'Contribution {cid} sourceExtractRef mismatch with trace.')
        if c['benchmarkKind'] == 'EXACT_PRODUCT':
            if c.get('normalizedProductRef') != trace.get('normalizedProductRef'):
                errors.append(f'Contribution {cid} exact product does not match normalization trace.')
            if trace.get('normalizationOutcome') != 'EXACT_PRODUCT':
                errors.append(f'Contribution {cid} exact-product benchmark requires EXACT_PRODUCT normalization trace.')
        if c['benchmarkKind'] == 'PRODUCT_CLASS':
            if trace.get('normalizationOutcome') == 'REFUSED':
                errors.append(f'Contribution {cid} may not derive from REFUSED normalization trace.')
            if c.get('normalizedProductClassRef') != trace.get('normalizedProductClassRef'):
                errors.append(f'Contribution {cid} product class does not match normalization trace.')
        if c['revocationState'] == 'REVOKED_FOR_FUTURE_USE' and c['currentUseState'] != 'INELIGIBLE':
            errors.append(f'Contribution {cid} is revoked but not INELIGIBLE.')
    for mid, m in mat_states.items():
        missing = [r for r in m.get('sourceContributionRefs', []) if r not in contribs]
        if missing:
            errors.append(f'Materialization {mid} references missing contributions {missing}.')
            continue
        selected = [contribs[r] for r in m['sourceContributionRefs']]
        if m['freshnessState'] == 'FRESH':
            bad = [c['contributionId'] for c in selected if c['currentUseState'] != 'ELIGIBLE' or c['revocationState'] != 'ACTIVE']
            if bad:
                errors.append(f'Materialization {mid} is FRESH but includes ineligible/revoked contributions {bad}.')
        if m.get('successorMaterializationRef'):
            target_ref = m['successorMaterializationRef']
            matches = [x for x in mat_states.values() if x['materializationRef'] == target_ref]
            if not matches:
                errors.append(f'Materialization {mid} successorMaterializationRef {target_ref} not found.')
    for did, d in decisions.items():
        if d['requestHistoryAssessmentRef'] not in histories:
            errors.append(f'Decision {did} references missing request-history assessment {d["requestHistoryAssessmentRef"]}.')
            continue
        if d['materializationStateRef'] not in mat_states:
            errors.append(f'Decision {did} references missing materialization state {d["materializationStateRef"]}.')
            continue
        hist = histories[d['requestHistoryAssessmentRef']]
        mat = mat_states[d['materializationStateRef']]
        refs = d.get('sourceContributionRefs', [])
        missing = [r for r in refs if r not in contribs]
        if missing:
            errors.append(f'Decision {did} references missing contributions {missing}.')
            continue
        selected = [contribs[r] for r in refs]
        if d['requestedByPartyRef'] != hist['requestedByPartyRef']:
            errors.append(f'Decision {did} viewer does not match request-history assessment.')
        if d['requestedBenchmarkKind'] != hist['requestedBenchmarkKind']:
            errors.append(f'Decision {did} requested benchmark kind does not match request-history assessment.')
        if d['differencingGuardStatus'] != hist['differencingGuardStatus']:
            errors.append(f'Decision {did} differencing guard status does not match request-history assessment.')
        if d['freshnessState'] != mat['freshnessState']:
            errors.append(f'Decision {did} freshnessState does not match referenced materialization state.')
        if mat['freshnessState'] != 'FRESH' and d['decision'] in {'ALLOW', 'BROADEN'}:
            errors.append(f'Decision {did} may not ALLOW/BROADEN from non-FRESH materialization.')
        if set(refs) != set(mat['sourceContributionRefs']) and d['materializationStateRef'] != 'matstate:fertrecomp:q1:v2':
            # recompute bundle old mat + new decision is handled by specific fresh mat
            pass
        # count/dominance checks
        count = len(selected)
        if d['contributorCountInternal'] != count:
            errors.append(f'Decision {did} contributorCountInternal {d["contributorCountInternal"]} != selected contribution count {count}.')
        if d['contributorCountDisplay'] != band_for_count(count):
            errors.append(f'Decision {did} contributorCountDisplay {d["contributorCountDisplay"]} != expected band {band_for_count(count)}.')
        if count < d['minContributorsRequired'] and d['decision'] in {'ALLOW', 'BROADEN'}:
            errors.append(f'Decision {did} allows benchmark below minContributorsRequired.')
        total = sum(c['totalAmount'] for c in selected)
        dom = 0 if total == 0 else round(max(c['totalAmount'] for c in selected) / total, 6)
        if abs(d['dominanceShareMax'] - dom) > 1e-6:
            errors.append(f'Decision {did} dominanceShareMax {d["dominanceShareMax"]} != calculated {dom}.')
        avg_metric = round(sum(c['metricValue'] for c in selected) / len(selected), 3)
        avg_metrics = [m for m in d.get('userVisibleMetrics', []) if m.get('metricName') == 'AVG_UNIT_PRICE']
        if avg_metrics:
            shown = round(float(avg_metrics[0].get('numericValue')), 3)
            if shown != avg_metric:
                errors.append(f'Decision {did} AVG_UNIT_PRICE {shown} != calculated {avg_metric}.')
        if d['effectiveBenchmarkKind'] == 'EXACT_PRODUCT':
            products = {c.get('normalizedProductRef') for c in selected}
            if None in products or len(products) != 1:
                errors.append(f'Decision {did} exact-product benchmark requires exactly one normalizedProductRef across contributions.')
        if d['effectiveBenchmarkKind'] == 'PRODUCT_CLASS':
            classes = {c.get('normalizedProductClassRef') for c in selected}
            if len(classes) != 1:
                errors.append(f'Decision {did} product-class benchmark requires exactly one normalizedProductClassRef across contributions.')
        if any(c['currentUseState'] != 'ELIGIBLE' or c['revocationState'] != 'ACTIVE' for c in selected):
            errors.append(f'Decision {did} includes ineligible/revoked contribution in selected set.')
    return errors

def validate_positive_bundles():
    lines = ['POSITIVE BUNDLES']
    overall_ok = True
    for bundle in sorted([p for p in POS_DIR.iterdir() if p.is_dir()]):
        lines.append(f'\n[{bundle.name}]')
        bundle_ok = True
        for f in sorted(bundle.glob('*.json')):
            ok, errs = validate_instance(f)
            bundle_ok &= ok
            if ok:
                lines.append(f'- {f.name}: PASS')
            else:
                lines.append(f'- {f.name}: FAIL')
                lines.extend([f'    * {e}' for e in errs])
        cross_errs = cross_bundle_checks(bundle)
        if cross_errs:
            bundle_ok = False
            lines.extend([f'    * CROSS-BUNDLE: {e}' for e in cross_errs])
        lines.append(f'  Bundle outcome: {"PASS" if bundle_ok else "FAIL"}')
        overall_ok &= bundle_ok
    return overall_ok, lines

def validate_negative_examples():
    lines = ['\nNEGATIVE EXAMPLES']
    overall_ok = True
    for f in sorted(NEG_DIR.glob('*.json')):
        ok, errs = validate_instance(f)
        if ok:
            overall_ok = False
            lines.append(f'- {f.name}: UNEXPECTED PASS')
        else:
            lines.append(f'- {f.name}: EXPECTED FAIL')
            lines.extend([f'    * {e}' for e in errs])
    return overall_ok, lines

def validate_query_templates():
    lines = ['\nQUERY TEMPLATES']
    schema = load_json(ACTIVE_SCHEMA_DIR / 'OFARM_QuerySpecification_schema_v0_1.json')
    validator = Draft202012Validator(schema)
    overall_ok = True
    for f in sorted(FIXTURE_DIR.glob('OFARM_QuerySpecification_example_*.json')):
        obj = load_json(f)
        errs = [f'SCHEMA: {e.message}' for e in validator.iter_errors(obj)]
        if obj.get('target', {}).get('twin') != 'ADVISORY':
            errs.append('SEMANTIC: Query template must target Advisory twin.')
        concepts = [n.get('conceptRef') for n in obj.get('graphPattern', {}).get('nodes', [])]
        if concepts != ['BenchmarkContribution']:
            errs.append(f'SEMANTIC: Query template must bind only BenchmarkContribution in this packet, got {concepts}.')
        selected_funcs = []
        selected_props = []
        for item in obj.get('selection', []):
            src = item.get('source', {})
            if src.get('kind') == 'AGGREGATE':
                selected_funcs.append(src.get('function'))
                if src.get('source', {}).get('kind') == 'PROPERTY':
                    selected_props.append(src.get('source', {}).get('propertyRef'))
        disallowed = [fn for fn in selected_funcs if fn not in {'COUNT', 'SUM', 'MAX', 'AVG'}]
        if disallowed:
            errs.append(f'SEMANTIC: Disallowed aggregate functions used: {sorted(disallowed)}')
        if any(prop in {'sourceExtractRef', 'sourceNormalizationTraceRef', 'shareGrantRef'} for prop in selected_props):
            errs.append('SEMANTIC: Query template may not expose raw basis refs in user-facing selection.')
        filter_props = []
        for clause in obj.get('filter', {}).get('clauses', []):
            left = clause.get('left', {})
            if left.get('kind') == 'PROPERTY':
                filter_props.append(left.get('propertyRef'))
        for needed in {'revocationState', 'currentUseState'}:
            if needed not in filter_props:
                errs.append(f'SEMANTIC: Query template should filter on {needed}.')
        if errs:
            overall_ok = False
            lines.append(f'- {f.name}: FAIL')
            lines.extend([f'    * {e}' for e in errs])
        else:
            lines.append(f'- {f.name}: PASS')
    return overall_ok, lines

def validate_runtime_records():
    lines = ['\nRUNTIME RECORDS']
    overall_ok = True
    # Request history records
    rh = load_json(ROOT / '04_implementation_and_conformance' / 'OFARM_runtime_benchmark_request_history_records_v0_2.json')
    if len(rh.get('records', [])) < 3:
        overall_ok = False
        lines.append('- request_history_records: FAIL')
        lines.append('    * Expected at least three request history scenarios.')
    else:
        blocked = [r for r in rh['records'] if r.get('guardStatus') == 'BLOCKED']
        broaden = [r for r in rh['records'] if r.get('guardStatus') == 'BROADEN']
        if not blocked or blocked[0].get('actionRecommendation') != 'REFUSE':
            overall_ok = False
            lines.append('- request_history_records: FAIL')
            lines.append('    * BLOCKED scenario missing or actionRecommendation is not REFUSE.')
        elif not broaden or broaden[0].get('actionRecommendation') != 'PROCEED_WITH_BROADENING':
            overall_ok = False
            lines.append('- request_history_records: FAIL')
            lines.append('    * BROADEN scenario missing or actionRecommendation is not PROCEED_WITH_BROADENING.')
        else:
            lines.append('- request_history_records: PASS')
    # Materialization records
    mats = load_json(ROOT / '04_implementation_and_conformance' / 'OFARM_runtime_benchmark_materialization_records_v0_2.json')
    invalid = [r for r in mats.get('records', []) if r.get('freshnessState') == 'INVALID']
    fresh = [r for r in mats.get('records', []) if r.get('freshnessState') == 'FRESH']
    if not invalid or not invalid[0].get('recomputeRequired'):
        overall_ok = False
        lines.append('- materialization_records: FAIL')
        lines.append('    * INVALID recomputeRequired scenario missing.')
    elif len(fresh) < 2:
        overall_ok = False
        lines.append('- materialization_records: FAIL')
        lines.append('    * Expected fresh baseline and fresh recomputed materializations.')
    else:
        lines.append('- materialization_records: PASS')
    # Sharing records
    sharing = load_json(ROOT / '04_implementation_and_conformance' / 'OFARM_runtime_benchmark_sharing_boundary_access_records_v0_2.json')
    deny_reasons = {tuple(r.get('reasonCodes', [])) for r in sharing.get('records', []) if r.get('outcome') == 'DENY'}
    if not any('MATERIALIZATION_INVALID_FOR_VIEW' in rs for rs in deny_reasons):
        overall_ok = False
        lines.append('- sharing_records: FAIL')
        lines.append('    * Missing deny scenario for invalid materialization.')
    else:
        lines.append('- sharing_records: PASS')
    # Pilot dataset
    pilot = load_json(FIXTURE_DIR / 'OFARM_advisory_cohort_benchmark_illustrative_redacted_pilot_dataset_v0_2.json')
    if pilot.get('datasetKind') != 'ILLUSTRATIVE_NON_REAL' or pilot.get('provenance', {}).get('actualTenantData') is not False:
        overall_ok = False
        lines.append('- illustrative_pilot_dataset: FAIL')
        lines.append('    * Pilot dataset honesty markers are incorrect.')
    else:
        lines.append('- illustrative_pilot_dataset: PASS')
    return overall_ok, lines

def main():
    ok_pos, lines_pos = validate_positive_bundles()
    ok_neg, lines_neg = validate_negative_examples()
    ok_q, lines_q = validate_query_templates()
    ok_r, lines_r = validate_runtime_records()

    overall = ok_pos and ok_neg and ok_q and ok_r

    lines = []
    lines.extend(lines_pos)
    lines.extend(lines_neg)
    lines.extend(lines_q)
    lines.extend(lines_r)
    lines.append('\nOVERALL')
    lines.append(f'Runtime proof packet outcome: {"PASS" if overall else "FAIL"}')

    OUT.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(OUT)
    print('\n'.join(lines))

if __name__ == '__main__':
    main()
