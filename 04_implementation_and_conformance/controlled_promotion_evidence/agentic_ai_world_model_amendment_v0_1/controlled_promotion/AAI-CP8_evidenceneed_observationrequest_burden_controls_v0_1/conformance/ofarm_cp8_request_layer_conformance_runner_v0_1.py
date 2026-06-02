#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[6]
PHASE = 'AAI-CP8'
CP8 = Path(__file__).resolve().parents[1]
REQUEST_SCHEMAS = ['EvidenceNeed','ObservationRequest','EvidenceOption','RequestTargetScope','RequestBurdenEstimate','RequestPriorityClassification','RequestRelevanceWindow','RequestCompletionCriteria','RequestLifecycleState','RequestSatisfactionTrace','RequestNoiseControlEnvelope','RequestBlockingBasis','RequestDeduplicationKey','RequestDisplayEnvelope','RequestGovernanceBlocker']
SCHEMA_DIR = ROOT/'03_machine_contracts/schemas/request_layer'
EXAMPLE_DIR = ROOT/'04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/request_layer'

def load(p):
    return json.loads(Path(p).read_text(encoding='utf-8'))

def main():
    failures=[]
    records=0
    try:
        import jsonschema
        validator_cls = jsonschema.Draft202012Validator
    except Exception as e:
        jsonschema = None
        validator_cls = None
    for name in REQUEST_SCHEMAS:
        sp=SCHEMA_DIR/f'OFARM_{name}_schema_v0_1.json'
        ep=EXAMPLE_DIR/f'OFARM_{name}_example_field17_spray_evidence_gap_v0_1.json'
        if not sp.exists(): failures.append(f'missing schema {sp.relative_to(ROOT)}'); continue
        if not ep.exists(): failures.append(f'missing example {ep.relative_to(ROOT)}'); continue
        schema=load(sp); example=load(ep); records += 1
        if validator_cls:
            try:
                validator_cls(schema).validate(example)
            except Exception as e:
                failures.append(f'{name} schema validation failed: {e}')
    # invariant checks
    en=load(EXAMPLE_DIR/'OFARM_EvidenceNeed_example_field17_spray_evidence_gap_v0_1.json')
    ore=load(EXAMPLE_DIR/'OFARM_ObservationRequest_example_field17_spray_evidence_gap_v0_1.json')
    rb=load(EXAMPLE_DIR/'OFARM_RequestBlockingBasis_example_field17_spray_evidence_gap_v0_1.json')
    rd=load(EXAMPLE_DIR/'OFARM_RequestDisplayEnvelope_example_field17_spray_evidence_gap_v0_1.json')
    st=load(EXAMPLE_DIR/'OFARM_RequestSatisfactionTrace_example_field17_spray_evidence_gap_v0_1.json')
    for label,obj in [('EvidenceNeed',en),('ObservationRequest',ore)]:
        if obj.get('notEvidence') is not True: failures.append(f'{label} notEvidence must be true')
        if obj.get('notObligation') is not True: failures.append(f'{label} notObligation must be true')
        if obj.get('notBlockerByItself') is not True: failures.append(f'{label} notBlockerByItself must be true')
    if en.get('blockingStatus')=='BLOCKING_BY_EXTERNAL_RULE' and not en.get('blockingBasisRef'):
        failures.append('blocking EvidenceNeed must cite RequestBlockingBasis')
    if rb.get('blockApplies') and rb.get('basisType')=='NONE':
        failures.append('blockApplies requires non-NONE basisType')
    if rb.get('blockApplies') and not (rb.get('externalRuleRef') or rb.get('gateRef')):
        failures.append('blockApplies requires externalRuleRef or gateRef')
    if rb.get('requestAloneIsNotBasis') is not True:
        failures.append('RequestBlockingBasis must declare requestAloneIsNotBasis true')
    for k in ['whyThisMatters','whatItBlocks','whatItDoesNotBlock']:
        if not rd.get(k): failures.append(f'RequestDisplayEnvelope missing {k}')
    if 'NOT_BLOCKER' not in rd.get('qualificationChips',[]):
        failures.append('RequestDisplayEnvelope must expose NOT_BLOCKER qualification chip')
    if st.get('doesNotCreateEvidence') is not True:
        failures.append('RequestSatisfactionTrace must declare doesNotCreateEvidence true')
    if st.get('acceptedEvidenceRefs') and not (st.get('reviewRequired') or st.get('promotionDecisionRef')):
        failures.append('acceptedEvidenceRefs require reviewRequired or promotionDecisionRef')
    # Negative cases should be detected by invariant checks.
    neg_dir = CP8/'examples/negative_policy_examples'
    expected_negatives = 0
    detected_negatives = 0
    for p in sorted(neg_dir.glob('*.json')):
        expected_negatives += 1
        rec = load(p).get('record', {})
        violated = False
        if rec.get('schemaVersion') == 'ofarm.evidenceneed.v0.1' and rec.get('blockingStatus') == 'BLOCKING_BY_EXTERNAL_RULE' and not rec.get('blockingBasisRef'):
            violated = True
        if rec.get('schemaVersion') == 'ofarm.observationrequest.v0.1' and rec.get('notEvidence') is not True:
            violated = True
        if rec.get('schemaVersion') == 'ofarm.requestsatisfactiontrace.v0.1' and rec.get('acceptedEvidenceRefs') and not (rec.get('reviewRequired') or rec.get('promotionDecisionRef')):
            violated = True
        if violated:
            detected_negatives += 1
        else:
            failures.append(f'negative case not detected: {p.name}')
    result = {
        'schemaVersion':'ofarm.cp8.validationResult.v0.1',
        'phase':PHASE,
        'status':'PASS' if not failures else 'FAIL',
        'scope':'synthetic CP8 request-layer contract fixtures only; not farmer UX, runtime, or production readiness',
        'records':records + expected_negatives,
        'positiveRecords':records,
        'negativePolicyCases':expected_negatives,
        'detectedNegativePolicyCases':detected_negatives,
        'failures':failures,
        'nonClaims':['not farmer UX readiness','not production runtime readiness','not autonomous compliance decisioning','requests are not evidence','requests are not obligations','requests are not blockers by themselves']
    }
    print(json.dumps(result, indent=2))
    return 0 if not failures else 1

if __name__ == '__main__':
    raise SystemExit(main())
