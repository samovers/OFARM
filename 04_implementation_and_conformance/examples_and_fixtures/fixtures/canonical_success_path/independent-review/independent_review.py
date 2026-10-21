"""Root-authored public-API probes against a separately frozen author packet."""
from pathlib import Path
import argparse,base64,copy,hashlib,importlib.util,json,sys
import rfc8785

parser=argparse.ArgumentParser();parser.add_argument('--snapshot',type=Path,required=True);parser.add_argument('--out',type=Path,required=True);args=parser.parse_args()
P=args.snapshot.resolve();O=args.out.resolve();O.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(P))
from verify_success_path import verify
def raw(x):return (json.dumps(x,indent=2,ensure_ascii=False)+'\n').encode()
def sha(x):return hashlib.sha256(x).hexdigest()
def digest(x):return 'sha256:'+sha(rfc8785.dumps(x))
def load_wire(path):
    w=json.loads(path.read_bytes());dec=lambda v:base64.b64decode(v,validate=True)
    return [dec(w['evidenceBytesBase64']),dec(w['profileBytesBase64']),dec(w['contextBytesBase64']),{k:dec(v) for k,v in w['sourceBytesBase64'].items()},{k:dec(v) for k,v in w['schemaBytesBase64'].items()}]
rows=[]
def probe(name,inputs,expected_pass,context_pin=None,qualification=True):
    result=verify(*inputs,expected_context_sha256=context_pin or sha(inputs[2]),contract_root=P)
    expected_limits={'AUTHORIZATION_ELIGIBILITY','CANDIDATE_SET_COMPLETENESS','CANONICAL_SELECTION_CORRECTNESS','OWNER_OUTPUT_RUNTIME_ORIGIN','RUNTIME_PROTECTION_OR_EFFECT_PERMISSION'}
    passed=(result['disposition']=='PASS')==expected_pass
    if qualification:passed=passed and expected_limits<=set(result['notEstablished']) and result['verificationScope']=='SELECTED_OWNER_OUTPUT_INTEGRITY_ONLY'
    rows.append({'name':name,'pass':passed,'disposition':result['disposition'],'errors':result['errors'][:3]})
    return result

def coherent_repack(inputs,source_change=None,evidence_change=None):
    out=copy.deepcopy(inputs);e,p,c=map(json.loads,out[:3]);sources={k:json.loads(v) for k,v in out[3].items()}
    if source_change:source_change(sources,c,e)
    if evidence_change:evidence_change(e)
    rk=c['coreSources']['RESULT'];tk=c['coreSources']['TRACE'];qk=c['coreSources']['REQUEST'];r=copy.deepcopy(sources[rk]);t=copy.deepcopy(sources[tk]);r.pop('decisionBundleDigest');t.pop('decisionBundleDigest');bd=digest({'schemaVersion':'ofarm.authorizationDecisionBundleDigestInput.v0.2','request':sources[qk],'result':r,'trace':t})
    sources[rk]['decisionBundleDigest']=sources[tk]['decisionBundleDigest']=e['decisionBundleDigest']=bd
    for entry in c['sources']:
        entry['bytesSha256']=sha(raw(sources[entry['key']]));entry['valueDigest']=digest(sources[entry['key']])
    out[:3]=[raw(e),raw(p),raw(c)];out[3]={k:raw(v) for k,v in sources.items()};return out

for fixture in sorted((P/'fixtures').glob('basis-*')):
    tag=fixture.name;inputs=load_wire(fixture/'wire.json');context=json.loads(inputs[2]);sourcepin=(fixture/'context.sha256').read_text().strip()
    probe(tag+'/positive',inputs,True,context_pin=sourcepin)
    for key in inputs[3]:
        changed=copy.deepcopy(inputs);changed[3][key]+=b'\n';probe(tag+'/original-byte-change/'+key,changed,False,context_pin=sourcepin)
    for key in context['coreSources'].values():
        changed=copy.deepcopy(inputs);del changed[3][key];probe(tag+'/missing-core/'+key,changed,False,context_pin=sourcepin)
    for i in [0,1,2]:
        for label,data in [('nonobject',b'[]'),('duplicate',b'{"x":1,"x":2}'),('invalid-utf8',b'\xff'),('surrogate',b'{"x":"\\ud800"}')]:
            changed=copy.deepcopy(inputs);changed[i]=data;probe(tag+'/strict-input/'+str(i)+'/'+label,changed,False,context_pin=sourcepin)
    # Coherent result/trace/evidence mirror changes must still disagree with
    # actual independently selected Party/basis records or tuple encoding.
    for field,value in [('authoritySubjectPartyRef','party:unselected'),('authoritySubjectBasis','NATURAL_PERSON_SELF'),('pathId','path:unselected')]:
        def mutate(s,c,e,field=field,value=value):
            targets=[e['selectedPath'],s[c['coreSources']['RESULT']]['projection']['selectedPath'],s[c['coreSources']['TRACE']]['projection']['paths'][0]]
            for target in targets:target[field]=value
        old=json.loads(inputs[0])['selectedPath'].get(field)
        if old!=value:probe(tag+'/coherent-selected-path-'+field,coherent_repack(inputs,mutate),False)
    def tuple_change(s,c,e):
        for target in [e['selectedPath'],s[c['coreSources']['RESULT']]['projection']['selectedPath'],s[c['coreSources']['TRACE']]['projection']['paths'][0]]:
            target['canonicalTuple']['sourceRecordId']='authority-grant:unselected'
    probe(tag+'/coherent-wrong-canonical-tuple',coherent_repack(inputs,tuple_change),False)
    # Complete actual intent bytes, including otherwise unused fields, matter.
    def intent_change(s,c,e):s[c['coreSources']['EFFECT_INTENT']]['reviewerExtraMeaning']='Changed complete intent'
    probe(tag+'/changed-complete-intent',coherent_repack(inputs,intent_change),False)
    changed=copy.deepcopy(inputs);profile=json.loads(changed[1]);profile['outputKind']='CONSUMER_REPORT';changed[1]=raw(profile);ctx=json.loads(changed[2]);ctx['profileBytesSha256']=sha(changed[1]);changed[2]=raw(ctx);probe(tag+'/consumer-report-source',changed,False)
    changed=copy.deepcopy(inputs);ctx=json.loads(changed[2]);ctx['admitted']=True;changed[2]=raw(ctx);probe(tag+'/generic-admitted-context',changed,False)
    probe(tag+'/wrong-independent-context-pin',inputs,False,context_pin='0'*64)

summary={'status':'PASS' if all(r['pass'] for r in rows) else 'FINDINGS','primaryTrustBoundary':'Canonical authorization decision evidence','scopeStayedInsideBoundary':True,'checks':len(rows),'passed':sum(r['pass'] for r in rows),'failed':[r for r in rows if not r['pass']],'results':rows,'limitations':['Conditional selected-owner-output integrity only; no eligibility, canonical selection or actual source admission is established.','This is a root-authored review of an owner-authored packet, not a GitHub approval or production gate.'],'next':'Resolve any reproduced findings, replay the installed split layout and publish only the exact reviewed draft.'}
(O/'public-api-review.json').write_bytes(raw(summary));print(json.dumps({k:v for k,v in summary.items() if k!='results'},indent=2));raise SystemExit(0 if summary['status']=='PASS' else 1)
