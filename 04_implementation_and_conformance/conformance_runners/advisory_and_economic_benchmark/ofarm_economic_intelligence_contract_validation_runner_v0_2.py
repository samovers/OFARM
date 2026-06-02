import json
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
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
        forbidden = {'journalEntryRefs', 'chartOfAccountsRef', 'payableStatus', 'receivableStatus', 'bankTxnRef'}
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


def validate_positive_bundles():
    lines = ['POSITIVE BUNDLES']
    overall_ok = True
    for bundle in sorted([p for p in POS_DIR.iterdir() if p.is_dir()]):
        lines.append(f'\n[{bundle.name}]')
        scenario_id = None
        result_set_id = None
        source_scenario_id = None
        source_result_set_id = None
        bundle_ok = True
        for f in sorted(bundle.glob('*.json')):
            if f.name.startswith('OFARM_AllocationBasisDeclaration'):
                lines.append(f'- {f.name}: SKIPPED (informal example, no schema yet)')
                continue
            ok, errs = validate_instance(f)
            bundle_ok &= ok
            if 'AdvisoryScenarioSpec' in f.name:
                scenario_id = load_json(f).get('scenarioId')
            if 'AdvisoryScenarioResultSet' in f.name:
                obj = load_json(f)
                result_set_id = obj.get('scenarioResultSetId')
                source_scenario_id = obj.get('sourceScenarioId')
            if 'BridgeCandidate' in f.name:
                source_result_set_id = load_json(f).get('sourceScenarioResultSetId')
            if ok:
                lines.append(f'- {f.name}: PASS')
            else:
                lines.append(f'- {f.name}: FAIL')
                lines.extend([f'    * {e}' for e in errs])
        # cross-bundle linkage checks
        if scenario_id and source_scenario_id and scenario_id != source_scenario_id:
            bundle_ok = False
            lines.append(f'    * CROSS-LINK FAIL: result set sourceScenarioId {source_scenario_id} != scenarioId {scenario_id}')
        if result_set_id and source_result_set_id and result_set_id != source_result_set_id:
            bundle_ok = False
            lines.append(f'    * CROSS-LINK FAIL: bridge sourceScenarioResultSetId {source_result_set_id} != scenarioResultSetId {result_set_id}')
        lines.append(f'  Bundle outcome: {'PASS' if bundle_ok else 'FAIL'}')
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


if __name__ == '__main__':
    pos_ok, pos_lines = validate_positive_bundles()
    neg_ok, neg_lines = validate_negative_examples()
    report = []
    report.extend(pos_lines)
    report.extend(neg_lines)
    report.append('\nOVERALL: ' + ('PASS' if (pos_ok and neg_ok) else 'FAIL'))
    out = '\n'.join(report) + '\n'
    print(out)
