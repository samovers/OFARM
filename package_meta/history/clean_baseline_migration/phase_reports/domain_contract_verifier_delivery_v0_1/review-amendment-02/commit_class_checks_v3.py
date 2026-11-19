"""Finite source-backed token checks. No event classification or admission."""
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import re

# Exact owner source pins, independent of the fictional compatibility package.
SOURCE_HASHES={
 'PR23':'b4b4b502666f78b69fc54b55ffaeb3b9c6759acde946bbdfdc782b86819e5809',
 'INGRESS_REQUEST':'397ec3a61ed572b14f9916bc9e7b316ff48150c743c6b7aa2eab94a3be3e8ffc',
 'INGRESS_RESULT':'55a21c697a651cdff6ce8d64dd7c29dd2afaa329047b4ebd55c94497a411e7d5',
 'OPERATION_INTENT':'66825f09c714a2f4ad7dea2ee24d7f20bbd3a2c0f3241d5b14a6aff2227cf5f6'}

@lru_cache(maxsize=4)
def canonical_roles(directory=None):
    root=Path(directory) if directory else Path(__file__).resolve().parent
    pins=json.loads((root/'commit-class-source-pins.json').read_text())['sources']
    if {p['id'] for p in pins}!=set(SOURCE_HASHES):raise ValueError('Canonical source inventory mismatch')
    sources={}
    for p in pins:
        raw=(root/p['file']).read_bytes();actual=hashlib.sha256(raw).hexdigest()
        if actual!=SOURCE_HASHES[p['id']] or actual!=p['sha256']:raise ValueError('Canonical source pin mismatch: '+p['id'])
        sources[p['id']]=raw.decode()
    # Read only the exact normative table; no package-provided mapping is consulted.
    section=sources['PR23'].split('### 7.2 Exact action, effect-subject, result, and commit-class map',1)[1].split('### 7.3',1)[0]
    mappings={}
    for line in section.splitlines():
        if not line.startswith('| `ASSERT_'):continue
        cells=[c.strip() for c in line.strip('|').split('|')]
        if len(cells)!=5:raise ValueError('Unexpected PR23 table shape')
        quoted=[re.findall(r'`([^`]+)`',cell) for cell in cells]
        if [len(v) for v in quoted]!=[1,1,1,1,2]:raise ValueError('Unexpected PR23 table cells')
        action=quoted[0][0]
        if action in mappings:raise ValueError('Duplicate PR23 action')
        mappings[action]={'intentProfile':quoted[1][0],'effectSubjectKind':quoted[2][0],'resultSubtype':quoted[3][0],'constitutionalLabel':quoted[4][0],'commitClass':quoted[4][1]}
    if set(mappings)!={'ASSERT_STRUCTURE','ASSERT_OPERATION_CLAIM','ASSERT_COMPLIANCE'}:raise ValueError('Incomplete PR23 mapping')
    request=json.loads(sources['INGRESS_REQUEST'])['properties']['commitClass']['enum']
    result=json.loads(sources['INGRESS_RESULT'])['properties']['commitClass']['enum']
    if request!=result:raise ValueError('Ingress source enums disagree')
    if any(row['commitClass'] not in request for row in mappings.values()):raise ValueError('PR23 token not in ingress enum')
    intent=json.loads(sources['OPERATION_INTENT'])
    return {'actionMap':mappings,'requestEnum':request,'resultEnum':result,
            'operationIntentVersion':intent['properties']['schemaVersion']['const'],
            'sourcePins':pins}

def canonical_event_errors(case,package,directory=None):
    source=canonical_roles(directory);errors=[]
    action=case.get('selectedAction');row=source['actionMap'].get(action)
    if row is None:return ['UNKNOWN_CANONICAL_ACTION']
    intent=case['intent'];result=case['result']
    # This finite corpus contains operation intent carriers. Cross-check that exact
    # schema discriminator against the PR23 profile; an action label cannot remap it.
    if intent.get('schemaVersion')!=source['operationIntentVersion'] or row['intentProfile']!='EI_OPERATION_ASSERTION_V0_2':errors.append('ACTION_INTENT_PROFILE_MISMATCH')
    if intent.get('effectSubject',{}).get('subjectKind')!=row['effectSubjectKind']:errors.append('EFFECT_SUBJECT_KIND_MISMATCH')
    if result.get('assertionType')!=row['resultSubtype']:errors.append('RESULT_SUBTYPE_MISMATCH')
    if 'associatedSemanticEventBinding' not in intent:return errors
    rule=package['cases'][case['exampleId']]
    roles=[('PACKAGE',rule.get('commitClass')),('TRACE',case.get('traceIllustration',{}).get('commitClass'))]
    if case.get('proof') is not None:roles.append(('PROOF',case['proof'].get('commitClass')))
    for role,value in roles:
        if value not in source['requestEnum'] or value not in source['resultEnum']:errors.append(role+'_COMMIT_CLASS_NOT_IN_INGRESS_ENUM')
        if value!=row['commitClass']:errors.append(role+'_COMMIT_CLASS_NOT_CANONICAL')
    return errors
