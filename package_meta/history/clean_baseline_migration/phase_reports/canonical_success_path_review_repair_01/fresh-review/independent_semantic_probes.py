"""Independent root-authored semantic probes; no author fixture helpers imported."""
from pathlib import Path
import argparse, base64, copy, hashlib, importlib.util, json, subprocess, sys, tempfile
import rfc8785

ap=argparse.ArgumentParser();ap.add_argument('--snapshot',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
P=a.snapshot.resolve();O=a.out.resolve();O.mkdir(parents=True,exist_ok=True)
spec=importlib.util.spec_from_file_location('reviewed_path',P/'verify_success_path.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
def raw(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def sha(x):return hashlib.sha256(x).hexdigest()
def digest(x):return 'sha256:'+sha(rfc8785.dumps(x))
def outputs(m):return [m['sources'][m['context']['coreSources'][n]]['projection'] for n in ('RESULT','TRACE')]
def paths(m):return [m['evidence']['selectedPath'],outputs(m)[0]['selectedPath'],*outputs(m)[1]['paths']]
def fresh(name):return json.loads((P/'fixtures'/name/'model.json').read_bytes())
def repack(m):
    # Independent exact serialization of a fictional owner selection. Keep
    # semantic contradictions; only repair the hashes required to reach them.
    sources=m['sources'];core=m['context']['coreSources']
    for o in outputs(m):
        for field,role in [('policyDigest','POLICY'),('ruleDigest','RULE'),('effectIntentDigest','EFFECT_INTENT'),('derivedViewDigest','DERIVED_VIEW')]:o[field]=digest(sources[core[role]])
    sources[core['REQUEST']]['projection']['effectIntentDigest']=digest(sources[core['EFFECT_INTENT']])
    m['profile']['schemaDigests']={sid:sha(raw(s)) for sid,s in m['schemas'].items()}
    for f in m['profile']['formats'].values():f['schemaSha256']=m['profile']['schemaDigests'][f['schemaId']]
    m['context']['profileBytesSha256']=sha(raw(m['profile']))
    request=sources[core['REQUEST']];result=copy.deepcopy(sources[core['RESULT']]);trace=copy.deepcopy(sources[core['TRACE']])
    result.pop('decisionBundleDigest');trace.pop('decisionBundleDigest')
    d=digest({'schemaVersion':'ofarm.authorizationDecisionBundleDigestInput.v0.2','request':request,'result':result,'trace':trace})
    sources[core['RESULT']]['decisionBundleDigest']=sources[core['TRACE']]['decisionBundleDigest']=m['evidence']['decisionBundleDigest']=d
    for row in m['context']['sources']:
        data=raw(sources[row['key']]);row.update(bytesSha256=sha(data),valueDigest=digest(sources[row['key']]))
    return m
def args(m):return [raw(m['evidence']),raw(m['profile']),raw(m['context']),{k:raw(v) for k,v in m['sources'].items()},{k:raw(v) for k,v in m['schemas'].items()}]
def rebind(m,key,binding):
    row=next(x for x in m['context']['sources'] if x['key']==key);row['binding']=copy.deepcopy(binding)
    if key in m['evidence']['sources']:m['evidence']['sources'][key]=copy.deepcopy(binding)
    for p in paths(m):
        for b in p['basis']:
            if b['sourceKey']==key:b['binding']=copy.deepcopy(binding)
        p['authoritySubjectBasisRefs']=[copy.deepcopy(b['binding']) for b in p['basis']]
    vk='visibility:'+key
    if vk in m['sources']:
        m['sources'][vk]['projection']['sourceBinding']=copy.deepcopy(binding)
        vb=next(x['binding'] for x in m['context']['sources'] if x['key']==vk)
        for b in m['sources']['EVALUATION_SNAPSHOT']['projection']['visibleBasis']:
            if b['visibilityBinding']==vb:b['binding']=copy.deepcopy(binding)

rows=[]
def check(name,m,code=None,group='semantic-consistency'):
    xs=args(m);r=module.verify(*xs,expected_context_sha256=sha(xs[2]),contract_root=P)
    codes=[e['code'] for e in r['errors']]
    ok=(r['disposition']=='PASS' if code is None else r['disposition']!='PASS') and codes==([] if code is None else [code])
    ok=ok and {'AUTHORIZATION_ELIGIBILITY','CANDIDATE_SET_COMPLETENESS','CP3_ADMISSION','RUNTIME_PROTECTION_OR_EFFECT_PERMISSION'}<=set(r['notEstablished'])
    rows.append({'name':name,'group':group,'pass':ok,'expectedCode':code,'status':r['disposition'],'codes':codes})
    if not ok:(O/('failure-'+str(len(rows))+'.json')).write_bytes(raw({'input':m,'report':r}))
    return r

for n in range(1,5):
    for target in ('party','role'):
        name=f'basis-{n}-{target}';baseline=fresh(name)
        check(name+'/baseline',baseline,group='positive-controls')
        # Reach native-revision validation with matching original-byte pins.
        for key in ('AUTHENTICATED_PRINCIPAL','AUTHORITY_SUBJECT_PARTY','EVALUATION_SNAPSHOT','RESULT','TRACE'):
            m=copy.deepcopy(baseline);m['sources'][key]['recordRevision']='review:r2';check(name+'/native-revision/'+key,repack(m),'SOURCE_RECORD_REVISION_MISMATCH')
        m=copy.deepcopy(baseline);m['profile']['formats']['AUTHENTICATED_PRINCIPAL']['revisionPointer']=None
        check(name+'/revision-pointer-required',repack(m),'REVISION_POINTER_REQUIRED')
        # Two versions are individually native-revision-consistent but conflict
        # as one logical Party identity in the selected decision snapshot.
        m=copy.deepcopy(baseline);m['sources']['AUTHORITY_SUBJECT_PARTY']['recordRevision']='review:r2'
        rebind(m,'AUTHORITY_SUBJECT_PARTY',{'ref':m['sources']['AUTHORITY_SUBJECT_PARTY']['recordId'],'revisionRef':'review:r2'})
        check(name+'/conflicting-party-versions',repack(m),'IMMUTABLE_ID_REUSED_WITH_DIFFERENT_BYTES')
        # Every retained path is checked, even when it is not selected or ALLOW.
        for field,value in [('pathTypeOrder',99),('sourceRecordId','grant:unrelated'),('delegationSourceRecordIds',['delegation:unrelated'])]:
            m=copy.deepcopy(baseline);other=copy.deepcopy(outputs(m)[1]['paths'][0]);other.update(pathId='review:other',pathDisposition='PATH_DENY');other['canonicalTuple'][field]=(other['canonicalTuple'][field]+1)%4 if field=='pathTypeOrder' else value;outputs(m)[1]['paths'].append(other)
            check(name+'/retained-tuple/'+field,repack(m),'CANONICAL_TUPLE_ENCODING_MISMATCH')
        for field,value,code in [
            ('primaryReasonCode','NO_AUTHORITY_BASIS','SUCCESS_PRIMARY_REASON_MISMATCH'),
            ('humanFinalizationRequirement','DIRECT_HUMAN_ACTION_REQUIRED','HUMAN_FINALIZATION_RULE_MISMATCH'),
            ('authorizationViewExtractorRef','extractor:other','EXTRACTOR_REFERENCE_MISMATCH'),
            ('authorizationViewExtractorDigest','sha256:'+'0'*64,'EXTRACTOR_DIGEST_MISMATCH'),
            ('resolvedPrincipalKind','NATURAL_PERSON' if n>=3 else 'SOFTWARE_AGENT','OUTPUT_PRINCIPAL_KIND_MISMATCH'),
            ('agentActionPosture','HUMAN_ONLY','OUTPUT_CP3_POSTURE_MISMATCH'),
        ]:
            m=copy.deepcopy(baseline)
            for o in outputs(m):o[field]=value
            check(name+'/output/'+field,repack(m),code)
        m=copy.deepcopy(baseline);m['sources']['AUTHORIZATION_VIEW_EXTRACTOR']['projection']['transformation']='REVIEW_CHANGED'
        check(name+'/extractor-content',repack(m),'SOURCE_BINDING_DIGEST_MISMATCH')
        if n>=3:
            for key,field,code in [('CP3_ACTORSHIP_BINDING','agentSponsorRef','CP3_IDENTITY_LINK_MISMATCH'),('CP3_AUTHORITY_ENVELOPE','executingAgentInstanceRef','CP3_IDENTITY_LINK_MISMATCH'),('CP3_AUTHORITY_ENVELOPE','revocationStateRef','CP3_EVIDENCE_LINK_MISMATCH'),('CP3_REVOCATION_STATE','agentSponsorRef','CP3_REVOCATION_LINK_MISMATCH')]:
                m=copy.deepcopy(baseline);m['sources'][key]['projection'][field]='review:wrong';check(name+'/deep-cp3/'+key+'/'+field,repack(m),code)

for disposition in ('PATH_ALLOW','PATH_DENY','PATH_REQUIRE_REVIEW','PATH_REQUIRE_HUMAN_APPROVAL','PATH_INAPPLICABLE'):
    m=fresh('basis-1-role');other=copy.deepcopy(outputs(m)[1]['paths'][0]);other.update(pathId='review:earlier',pathType='DIRECT_PARTY_GRANT',pathDisposition=disposition);other['canonicalTuple']['pathTypeOrder']=0;outputs(m)[1]['paths'].append(other)
    check('retained-lower/'+disposition,repack(m),'RETAINED_ALLOW_PATH_PRECEDES_SELECTION' if disposition=='PATH_ALLOW' else None)
for field in ('primaryReasonCode','humanFinalizationRequirement','authorizationViewExtractorRef','authorizationViewExtractorDigest','resolvedPrincipalKind','agentActionPosture'):
    m=fresh('basis-3-party')
    for o in outputs(m):del o[field]
    check('closed-output/missing-'+field,repack(m),'SCHEMA_INVALID')
for name in ('basis-1-party','basis-3-role','basis-4-party'):
    m=fresh(name)
    for p in paths(m):p['pathType']='SHARING_GRANT_ACCESS';p['canonicalTuple']['pathTypeOrder']=3
    check(name+'/sharing-explicit-limit',repack(m),'SELECTED_SHARING_PATH_OUTSIDE_PROFILE')

# Native field locations may be nested and are selected by the profile.
m=fresh('basis-3-party');key='AUTHENTICATED_PRINCIPAL';record=m['sources'][key]
record['native']={'revision':record.pop('recordRevision')};fmt=m['profile']['formats'][key];fmt['revisionPointer']='/native/revision'
schema=m['schemas'][fmt['schemaId']];schema['required'].remove('recordRevision');schema['required'].append('native');old=schema['properties'].pop('recordRevision');schema['properties']['native']={'type':'object','additionalProperties':False,'required':['revision'],'properties':{'revision':old}}
check('profile/nested-native-revision',repack(m))
record['native']['revision']='wrong';check('profile/nested-native-revision-mismatch',repack(m),'SOURCE_RECORD_REVISION_MISMATCH')

m=fresh('basis-3-party');record=m['sources']['EFFECT_INTENT'];record['metadata']={'wireVersion':record.pop('schemaVersion')};fmt=m['profile']['formats']['EFFECT_INTENT'];fmt['schemaVersionPointer']='/metadata/wireVersion';schema=m['schemas'][fmt['schemaId']];schema['required'].remove('schemaVersion');schema['required'].append('metadata');old=schema['properties'].pop('schemaVersion');schema['properties']['metadata']={'type':'object','additionalProperties':False,'required':['wireVersion'],'properties':{'wireVersion':old}}
new_digest='sha256:'+sha(raw(schema));m['sources']['RULE']['projection']['intentSchema']['schemaDigest']=new_digest
for o in outputs(m):o['intentSchema']['schemaDigest']=new_digest
check('profile/nested-intent-version',repack(m));m['sources']['EFFECT_INTENT']['metadata']['wireVersion']='wrong';check('profile/nested-intent-version-mismatch',repack(m),'INTENT_VERSION_MISMATCH')

result={'status':'PASS' if all(r['pass'] for r in rows) else 'FINDINGS','primaryTrustBoundary':'Canonical authorization decision evidence','scopeStayedInsideBoundary':True,
        'checks':len(rows),'passed':sum(r['pass'] for r in rows),'groups':{g:sum(r['group']==g for r in rows) for g in sorted({r['group'] for r in rows})},
        'failed':[r for r in rows if not r['pass']],'results':rows,
        'method':'Root-authored repacking of actual fixture models without importing author helpers; coherent hashes reach specific semantic error codes. Actual public API unchanged.',
        'limits':['Fictional independently selected context assumptions; no actual source authority established.','Technical review is not formal GitHub approval or a two-reviewer governance gate.']}
(O/'independent-semantic-review.json').write_bytes(raw(result));print(json.dumps({k:v for k,v in result.items() if k!='results'},indent=2));raise SystemExit(result['status']!='PASS')
