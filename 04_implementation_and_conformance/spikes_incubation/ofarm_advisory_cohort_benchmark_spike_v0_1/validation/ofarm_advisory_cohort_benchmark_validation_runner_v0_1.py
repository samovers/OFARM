import json
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / 'experimental_machine_contracts' / 'schemas'
POS_DIR = ROOT / 'experimental_machine_contracts' / 'examples' / 'positive'
NEG_DIR = ROOT / 'experimental_machine_contracts' / 'examples' / 'negative'
FIXTURE_DIR = ROOT / 'fixtures'
REPO_ROOT = ROOT.parents[1]
ACTIVE_SCHEMA_DIR = REPO_ROOT / '03_machine_contracts'

SCHEMA_MAP = {
    'ProductNormalizationTrace': 'OFARM_ProductNormalizationTrace_schema_v0_1.json',
    'BenchmarkContribution': 'OFARM_BenchmarkContribution_schema_v0_1.json',
    'BenchmarkDisclosureDecision': 'OFARM_BenchmarkDisclosureDecision_schema_v0_1.json',
}

ALLOWED_USER_METRICS = {'AVG_UNIT_PRICE', 'QUANTITY_BAND', 'POSITION_BAND'}
DISALLOWED_METRIC_NAMES = {'TOTAL_SPEND', 'SPEND_PER_HECTARE', 'MIN_UNIT_PRICE', 'MAX_UNIT_PRICE', 'PERCENTILE'}
FORBIDDEN_CONTRIB_KEYS = {'rawEvidenceRefs', 'lineItems', 'ledgerAccountRef', 'perHectareValue', 'journalEntryRef'}


def load_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def schema_for_file(path: Path):
    name = path.name
    if 'ProductNormalizationTrace' in name:
        return 'ProductNormalizationTrace'
    if 'BenchmarkContribution' in name:
        return 'BenchmarkContribution'
    if 'BenchmarkDisclosureDecision' in name:
        return 'BenchmarkDisclosureDecision'
    return None


def semantic_checks(obj, kind):
    errors = []
    if kind == 'ProductNormalizationTrace':
        if obj.get('targetTwin') != 'ADVISORY':
            errors.append('ProductNormalizationTrace must remain in the Advisory twin.')
        outcome = obj.get('normalizationOutcome')
        ambiguity = obj.get('ambiguityReasonCodes') or []
        if outcome == 'EXACT_PRODUCT' and ambiguity:
            errors.append('Exact-product normalization may not carry active ambiguity reason codes.')
        if outcome == 'REFUSED' and obj.get('comparabilityStatus') == 'COMPARABLE':
            errors.append('Refused normalization may not claim comparable status.')
        if obj.get('sourceCurrency') != obj.get('normalizedCurrency') and not obj.get('currencyNormalizationApplied'):
            errors.append('Currency changed without explicit normalization flag.')
    elif kind == 'BenchmarkContribution':
        if obj.get('targetTwin') != 'ADVISORY':
            errors.append('BenchmarkContribution must remain in the Advisory twin.')
        overlap = FORBIDDEN_CONTRIB_KEYS.intersection(obj.keys())
        if overlap:
            errors.append(f'BenchmarkContribution contains forbidden keys: {sorted(overlap)}')
        qty = obj.get('normalizedQuantity')
        amt = obj.get('totalAmount')
        metric = obj.get('metricValue')
        if qty and amt and metric is not None:
            expected = amt / qty
            if abs(metric - expected) > 1e-6:
                errors.append(f'UNIT_PRICE metricValue {metric} does not equal totalAmount/normalizedQuantity {expected}.')
        if obj.get('revocationState') == 'REVOKED_FOR_FUTURE_USE' and obj.get('currentUseState') == 'ELIGIBLE':
            errors.append('Revoked contribution may not remain ELIGIBLE for future use.')
        if obj.get('benchmarkKind') == 'EXACT_PRODUCT' and not obj.get('normalizedProductRef'):
            errors.append('Exact-product contribution must carry normalizedProductRef.')
    elif kind == 'BenchmarkDisclosureDecision':
        if obj.get('targetTwin') != 'ADVISORY':
            errors.append('BenchmarkDisclosureDecision must remain in the Advisory twin.')
        for metric in obj.get('userVisibleMetrics', []):
            name = metric.get('metricName')
            if name in DISALLOWED_METRIC_NAMES:
                errors.append(f'User-visible metric {name} is out of scope for wave 1.')
            if name not in ALLOWED_USER_METRICS:
                errors.append(f'User-visible metric {name} is not allowed in this spike.')
        decision = obj.get('decision')
        count = obj.get('contributorCountInternal', 0)
        minimum = obj.get('minContributorsRequired', 0)
        dom = obj.get('dominanceShareMax', 0)
        threshold = obj.get('dominanceThreshold', 1)
        guard = obj.get('differencingGuardStatus')
        if decision == 'ALLOW':
            if count < minimum:
                errors.append('ALLOW decision violates minimum contributor threshold.')
            if dom > threshold:
                errors.append('ALLOW decision violates dominance threshold.')
            if guard != 'CLEAR':
                errors.append('ALLOW decision requires differencing guard CLEAR.')
            if obj.get('effectiveBenchmarkKind') == 'NONE':
                errors.append('ALLOW decision may not have effectiveBenchmarkKind NONE.')
        if decision == 'BROADEN':
            if obj.get('requestedBenchmarkKind') != 'EXACT_PRODUCT' or obj.get('effectiveBenchmarkKind') != 'PRODUCT_CLASS':
                errors.append('BROADEN must move from exact product to product class.')
        if decision in {'SUPPRESS', 'REFUSE'} and obj.get('userVisibleMetrics'):
            errors.append(f'{decision} decision may not expose user-visible metrics in this spike.')
    return errors


def validate_instance(path: Path):
    kind = schema_for_file(path)
    if not kind:
        return False, [f'No schema mapping for {path.name}']
    obj = load_json(path)
    schema = load_json(SCHEMA_DIR / SCHEMA_MAP[kind])
    validator = Draft202012Validator(schema)
    errors = [f'SCHEMA: {e.message}' for e in validator.iter_errors(obj)]
    errors.extend([f'SEMANTIC: {e}' for e in semantic_checks(obj, kind)])
    return len(errors) == 0, errors


def load_bundle(bundle_dir: Path):
    traces = {}
    contributions = {}
    decisions = {}
    for f in sorted(bundle_dir.glob('*.json')):
        obj = load_json(f)
        if 'ProductNormalizationTrace' in f.name:
            traces[obj['normalizationTraceId']] = obj
        elif 'BenchmarkContribution' in f.name:
            contributions[obj['contributionId']] = obj
        elif 'BenchmarkDisclosureDecision' in f.name:
            decisions[obj['decisionId']] = obj
    return traces, contributions, decisions


def cross_bundle_checks(bundle_dir: Path):
    errors = []
    traces, contributions, decisions = load_bundle(bundle_dir)
    # Contribution references
    for cid, contrib in contributions.items():
        trace_id = contrib['sourceNormalizationTraceRef']
        if trace_id not in traces:
            errors.append(f'Contribution {cid} references missing normalization trace {trace_id}.')
            continue
        trace = traces[trace_id]
        if contrib['sourceExtractRef'] != trace['sourceExtractRef']:
            errors.append(f'Contribution {cid} sourceExtractRef does not match normalization trace.')
        if contrib['normalizedProductClassRef'] != trace.get('normalizedProductClassRef'):
            errors.append(f'Contribution {cid} product class does not match normalization trace.')
        if contrib['benchmarkKind'] == 'EXACT_PRODUCT':
            if contrib.get('normalizedProductRef') != trace.get('normalizedProductRef'):
                errors.append(f'Contribution {cid} exact product does not match normalization trace.')
            if trace.get('normalizationOutcome') != 'EXACT_PRODUCT':
                errors.append(f'Contribution {cid} exact-product benchmark requires EXACT_PRODUCT normalization trace.')
        if contrib['benchmarkKind'] == 'PRODUCT_CLASS' and trace.get('normalizationOutcome') == 'REFUSED':
            errors.append(f'Contribution {cid} may not derive from refused normalization trace.')

    # Decision references and aggregate checks
    for did, decision in decisions.items():
        refs = decision.get('sourceContributionRefs', [])
        missing = [r for r in refs if r not in contributions]
        if missing:
            errors.append(f'Decision {did} references missing contributions {missing}.')
            continue
        selected = [contributions[r] for r in refs]
        total = sum(c['totalAmount'] for c in selected)
        max_amt = max(c['totalAmount'] for c in selected) if selected else 0
        if selected:
            dominance = round(max_amt / total, 6)
            if abs(decision['dominanceShareMax'] - dominance) > 1e-3:
                errors.append(f'Decision {did} dominanceShareMax {decision["dominanceShareMax"]} does not match contributions {dominance}.')
        count = len(selected)
        if decision['contributorCountInternal'] != count:
            errors.append(f'Decision {did} contributorCountInternal {decision["contributorCountInternal"]} != bundle count {count}.')
        # Product/exactness checks
        if decision['effectiveBenchmarkKind'] == 'EXACT_PRODUCT':
            products = {c.get('normalizedProductRef') for c in selected}
            if None in products or len(products) != 1:
                errors.append(f'Decision {did} exact-product benchmark requires exactly one normalizedProductRef across contributions.')
        if decision['effectiveBenchmarkKind'] == 'PRODUCT_CLASS':
            classes = {c.get('normalizedProductClassRef') for c in selected}
            if len(classes) != 1:
                errors.append(f'Decision {did} product-class benchmark requires exactly one product class across contributions.')
        # Average unit price cross-check if present
        avg_metrics = [m for m in decision.get('userVisibleMetrics', []) if m.get('metricName') == 'AVG_UNIT_PRICE']
        if avg_metrics:
            expected_avg = round(sum(c['metricValue'] for c in selected) / len(selected), 3)
            shown_avg = round(float(avg_metrics[0]['numericValue']), 3)
            if shown_avg != expected_avg:
                errors.append(f'Decision {did} AVG_UNIT_PRICE {shown_avg} != contribution average {expected_avg}.')
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
        selected_funcs = []
        for item in obj.get('selection', []):
            src = item.get('source', {})
            if src.get('kind') == 'AGGREGATE':
                selected_funcs.append(src.get('function'))
        disallowed = [fn for fn in selected_funcs if fn not in {'COUNT', 'SUM', 'MAX', 'AVG'}]
        if disallowed:
            errs.append(f'SEMANTIC: Disallowed aggregate functions used: {sorted(disallowed)}')
        if obj.get('resultProfile', {}).get('mode') not in {'SUMMARY_ROWS', 'VIEW_MODULE'}:
            errs.append('SEMANTIC: Query template resultProfile must be SUMMARY_ROWS or VIEW_MODULE.')
        if errs:
            overall_ok = False
            lines.append(f'- {f.name}: FAIL')
            lines.extend([f'    * {e}' for e in errs])
        else:
            lines.append(f'- {f.name}: PASS')
    return overall_ok, lines


if __name__ == '__main__':
    pos_ok, pos_lines = validate_positive_bundles()
    neg_ok, neg_lines = validate_negative_examples()
    query_ok, query_lines = validate_query_templates()
    overall = pos_ok and neg_ok and query_ok
    report = []
    report.extend(pos_lines)
    report.extend(neg_lines)
    report.extend(query_lines)
    report.append('\nOVERALL: ' + ('PASS' if overall else 'FAIL'))
    out = '\n'.join(report) + '\n'
    print(out)
    (ROOT / 'validation' / 'OFARM_advisory_cohort_benchmark_validation_results_v0_1.txt').write_text(out, encoding='utf-8')
