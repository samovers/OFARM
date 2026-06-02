import json
from pathlib import Path
from jsonschema import Draft202012Validator

HERE = Path(__file__).resolve().parent

PROFIT_TERMS = {
    'profit', 'profitability', 'gross margin', 'net margin', 'operating margin',
    'roa', 'roi', 'irr', 'npv', 'dscr', 'payback', 'allocated depreciation', 'allocated overhead'
}


def locate_spike_root() -> Path:
    candidates = [
        HERE / 'ofarm_economic_intelligence_spike_v0_1',
        HERE.parent / 'ofarm_economic_intelligence_spike_v0_1',
    ]
    for c in candidates:
        if (c / 'experimental_machine_contracts').exists():
            return c
    raise FileNotFoundError('Could not locate ofarm_economic_intelligence_spike_v0_1 with experimental_machine_contracts')

ROOT = locate_spike_root()
SCHEMA_DIR = ROOT / 'experimental_machine_contracts' / 'schemas'
POS_DIR = ROOT / 'experimental_machine_contracts' / 'examples' / 'positive'
NEG_DIR = ROOT / 'experimental_machine_contracts' / 'examples' / 'negative'

SCHEMA_MAP = {
    'AdvisoryScenarioSpec': 'OFARM_AdvisoryScenarioSpec_schema_v0_1.json',
    'ImportedFactExtract': 'OFARM_ImportedFactExtract_schema_v0_1.json',
    'AdvisoryScenarioResultSet': 'OFARM_AdvisoryScenarioResultSet_schema_v0_1.json',
    'BridgeCandidate': 'OFARM_BridgeCandidate_schema_v0_1.json',
}


def load_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def schema_for_file(path: Path):
    name = path.name
    if 'AdvisoryScenarioSpec' in name:
        return 'AdvisoryScenarioSpec'
    if 'ImportedFactExtract' in name:
        return 'ImportedFactExtract'
    if 'AdvisoryScenarioResultSet' in name:
        return 'AdvisoryScenarioResultSet'
    if 'BridgeCandidate' in name:
        return 'BridgeCandidate'
    return None


def semantic_checks(obj, kind):
    errors = []
    if kind == 'BridgeCandidate':
        if obj.get('requiresHumanApproval') is not True:
            errors.append('BridgeCandidate must remain human-gated in this spike.')
    if kind == 'AdvisoryScenarioResultSet':
        notes = (obj.get('notes') or '').lower()
        if 'current state' in notes and 'not' not in notes:
            errors.append('ScenarioResultSet notes imply current-state semantics.')
    if kind == 'ImportedFactExtract':
        forbidden = {'journalEntryRefs', 'chartOfAccountsRef', 'payableStatus', 'receivableStatus', 'bankTxnRef', 'reconciliationStatus'}
        overlap = forbidden.intersection(obj.keys())
        if overlap:
            errors.append(f'ImportedFactExtract contains forbidden ledger-like keys: {sorted(overlap)}')
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


def is_operational_only_scenario(obj):
    basis = obj.get('basisRefs', {})
    return obj.get('scenarioClass') == 'CROP_SYSTEM_RANKING' and not basis.get('importedFactExtractRefs')


def is_lane_b_capacity_scenario(obj):
    basis = obj.get('basisRefs', {})
    return obj.get('scenarioClass') == 'CONSTRAINT_CAPACITY' and bool(basis.get('importedFactExtractRefs'))


def text_contains_profit_terms(text: str) -> bool:
    t = (text or '').lower()
    return any(term in t for term in PROFIT_TERMS)


def validate_positive_bundles():
    lines = ['POSITIVE BUNDLES']
    overall_ok = True
    for bundle in sorted([p for p in POS_DIR.iterdir() if p.is_dir()]):
        lines.append(f'\n[{bundle.name}]')
        scenario_obj = None
        result_obj = None
        bridge_obj = None
        bundle_ok = True
        for f in sorted(bundle.glob('*.json')):
            if f.name.startswith('OFARM_AllocationBasisDeclaration'):
                lines.append(f'- {f.name}: SKIPPED (informal example, no schema yet)')
                continue
            ok, errs = validate_instance(f)
            bundle_ok &= ok
            obj = load_json(f)
            if 'AdvisoryScenarioSpec' in f.name:
                scenario_obj = obj
            if 'AdvisoryScenarioResultSet' in f.name:
                result_obj = obj
            if 'BridgeCandidate' in f.name:
                bridge_obj = obj
            if ok:
                lines.append(f'- {f.name}: PASS')
            else:
                lines.append(f'- {f.name}: FAIL')
                lines.extend([f'    * {e}' for e in errs])
        # cross-link checks
        if scenario_obj and result_obj and scenario_obj.get('scenarioId') != result_obj.get('sourceScenarioId'):
            bundle_ok = False
            lines.append(f"    * CROSS-LINK FAIL: result set sourceScenarioId {result_obj.get('sourceScenarioId')} != scenarioId {scenario_obj.get('scenarioId')}")
        if result_obj and bridge_obj and result_obj.get('scenarioResultSetId') != bridge_obj.get('sourceScenarioResultSetId'):
            bundle_ok = False
            lines.append(f"    * CROSS-LINK FAIL: bridge sourceScenarioResultSetId {bridge_obj.get('sourceScenarioResultSetId')} != scenarioResultSetId {result_obj.get('scenarioResultSetId')}")
        # Scenario-1 honesty checks
        if scenario_obj and is_operational_only_scenario(scenario_obj):
            notes = (result_obj or {}).get('notes', '')
            if 'screening only' not in notes.lower() or 'not a profitability statement' not in notes.lower():
                bundle_ok = False
                lines.append('    * SCENARIO-1 FAIL: result notes must declare screening-only and non-profitability posture.')
            if result_obj and result_obj.get('resultClass') not in {'RANKED_ALTERNATIVES', 'THRESHOLD_SCREEN'}:
                bundle_ok = False
                lines.append('    * SCENARIO-1 FAIL: operational-only result class must stay ranked/threshold style.')
            for item in (result_obj or {}).get('results', []):
                if text_contains_profit_terms(item.get('label', '')) or text_contains_profit_terms(item.get('valueExpression', '')):
                    bundle_ok = False
                    lines.append(f"    * SCENARIO-1 FAIL: profitability term detected in result {item.get('resultId')}")
            if bridge_obj and bridge_obj.get('proposedNextStepClass') in {'PREPARE_DOSSIER_ASSEMBLY', 'PREPARE_SUBMISSION_ASSEMBLY'}:
                bundle_ok = False
                lines.append('    * SCENARIO-1 FAIL: operational-only bridge may not prepare dossier/submission output.')
        # Lane-B honesty checks
        if scenario_obj and is_lane_b_capacity_scenario(scenario_obj):
            notes = (result_obj or {}).get('notes', '').lower()
            if 'decision support only' not in notes:
                bundle_ok = False
                lines.append('    * LANE-B FAIL: result notes must declare decision-support posture.')
            if 'not ledger truth' not in notes:
                bundle_ok = False
                lines.append('    * LANE-B FAIL: result notes must declare non-ledger posture.')
            if result_obj and result_obj.get('resultClass') not in {'CAPACITY_SCREEN', 'GENERAL_SUMMARY'}:
                bundle_ok = False
                lines.append('    * LANE-B FAIL: capacity lane must stay CAPACITY_SCREEN or GENERAL_SUMMARY.')
            if scenario_obj.get('requestedOutputClass') not in {'VIEW', 'REPORT_ASSEMBLY'}:
                bundle_ok = False
                lines.append('    * LANE-B FAIL: capacity lane may not request dossier/submission output.')
            for item in (result_obj or {}).get('results', []):
                if text_contains_profit_terms(item.get('label', '')) or text_contains_profit_terms(item.get('valueExpression', '')):
                    bundle_ok = False
                    lines.append(f"    * LANE-B FAIL: profitability term detected in result {item.get('resultId')}")
            if bridge_obj and bridge_obj.get('proposedNextStepClass') in {'PREPARE_DOSSIER_ASSEMBLY', 'PREPARE_SUBMISSION_ASSEMBLY'}:
                bundle_ok = False
                lines.append('    * LANE-B FAIL: capacity lane bridge may not prepare dossier/submission output.')
        lines.append(f"  Bundle outcome: {'PASS' if bundle_ok else 'FAIL'}")
        overall_ok &= bundle_ok
    return overall_ok, lines


def validate_negative_examples():
    lines = ['\nNEGATIVE EXAMPLES']
    overall_ok = True
    for f in sorted(NEG_DIR.glob('*.json')):
        ok, errs = validate_instance(f)
        should_fail_semantically = 'profitability_claim' in f.name
        if should_fail_semantically and ok:
            # apply ad hoc profitability check to negative result-set files with no scenario wrapper
            obj = load_json(f)
            found = text_contains_profit_terms(obj.get('notes', ''))
            found = found or any(text_contains_profit_terms(i.get('valueExpression', '')) or text_contains_profit_terms(i.get('label', '')) for i in obj.get('results', []))
            if found:
                ok = False
                errs = ['SEMANTIC: Negative example uses forbidden profitability or hidden-allocation language.']
        if ok:
            overall_ok = False
            lines.append(f'- {f.name}: UNEXPECTED PASS')
        else:
            lines.append(f'- {f.name}: EXPECTED FAIL')
            lines.extend([f'    * {e}' for e in errs])
    return overall_ok, lines


if __name__ == '__main__':
    pos_ok, pos_lines = validate_positive_bundles()
    neg_ok, neg_lines = validate_negative_examples()
    report = []
    report.extend(pos_lines)
    report.extend(neg_lines)
    report.append('\nOVERALL: ' + ('PASS' if (pos_ok and neg_ok) else 'FAIL'))
    print('\n'.join(report) + '\n')
