#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[6]
CP7 = ROOT/'04_implementation_and_conformance/controlled_promotion_evidence/agentic_ai_world_model_amendment_v0_1/controlled_promotion/AAI-CP7_advisory_world_model_runtime_v0_1'
EX = ROOT/'04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/world_model'

REQUIRED_TRUE = {
    'WorldModelRun': ['advisoryOnly','noCurrentStateMutation'],
    'WorldModelState': ['advisoryOnly','noCurrentStateMutation'],
    'ScenarioSpec': ['advisoryOnly'],
    'ScenarioResultSet': ['advisoryOnly'],
}

failures = []
records = []

def load(path):
    return json.loads(path.read_text(encoding='utf-8'))

for path in sorted(EX.glob('OFARM_*_example_*_v0_1.json')):
    obj = load(path)
    name = path.name
    records.append(path.relative_to(ROOT).as_posix())
    if name.startswith('OFARM_WorldModelRun'):
        if obj.get('twinRef') != 'ADVISORY': failures.append(f'{name}: WorldModelRun twinRef must be ADVISORY')
        if obj.get('advisoryOnly') is not True: failures.append(f'{name}: advisoryOnly must be true')
        if obj.get('noCurrentStateMutation') is not True: failures.append(f'{name}: noCurrentStateMutation must be true')
        if obj.get('runtimeConformanceClaimed') is not False: failures.append(f'{name}: runtimeConformanceClaimed must be false')
        if obj.get('currentStateBridgeRef') is not None: failures.append(f'{name}: currentStateBridgeRef must be null in CP7 positive fixture')
        for k in ['validityWindowRef','uncertaintyStatementRef','invalidationRuleRefs','outputDispositionRefs','resultQualificationRef']:
            if not obj.get(k): failures.append(f'{name}: missing {k}')
    if name.startswith('OFARM_WorldModelState'):
        if obj.get('twinRef') != 'ADVISORY': failures.append(f'{name}: WorldModelState twinRef must be ADVISORY')
        if obj.get('advisoryOnly') is not True: failures.append(f'{name}: advisoryOnly must be true')
        if obj.get('currentStateMaterializationRef') is not None: failures.append(f'{name}: currentStateMaterializationRef must be null in CP7 positive fixture')
        if obj.get('bridgeStatus') != 'NONE': failures.append(f'{name}: bridgeStatus must be NONE in CP7 positive fixture')
        for k in ['uncertaintyByVariable','provenanceSplit','validityWindowRef','invalidationStatus','reconciliationStatus']:
            if not obj.get(k): failures.append(f'{name}: missing {k}')
    if name.startswith('OFARM_ScenarioSpec'):
        if obj.get('twinRef') != 'ADVISORY': failures.append(f'{name}: ScenarioSpec twinRef must be ADVISORY')
    if name.startswith('OFARM_WorldModelOutputDisposition'):
        if obj.get('requiresBridgeForComplianceUse') is not True: failures.append(f'{name}: requiresBridgeForComplianceUse must be true')
    if name.startswith('OFARM_WorldModelReconciliationRecord'):
        if obj.get('noSilentPromotion') is not True: failures.append(f'{name}: noSilentPromotion must be true')

for path in sorted((CP7/'examples/negative').glob('OFARM_CP7_hostile_*_v0_1.json')):
    obj=load(path)
    records.append(path.relative_to(ROOT).as_posix())
    if obj.get('expectedPolicyOutcome') not in {'DENY','REVIEW_REQUIRED'}:
        failures.append(f'{path.name}: hostile case must expect DENY or REVIEW_REQUIRED')
    prohibited=set(obj.get('prohibitedOutcomes',[]))
    for required in ['CURRENT_STATE_MUTATION','COMPLIANCE_PROMOTION','WORLD_MODEL_READINESS_CLAIM']:
        if required not in prohibited:
            failures.append(f'{path.name}: missing prohibited outcome {required}')

result = {'schemaVersion':'ofarm.cp7ConformanceResult.v0.1','phase':'AAI-CP7','status':'PASS' if not failures else 'FAIL','records':len(records),'failures':failures,'scope':'synthetic CP7 advisory world-model contract fixtures only; not runtime or production readiness'}
print(json.dumps(result, indent=2))
raise SystemExit(0 if not failures else 1)
