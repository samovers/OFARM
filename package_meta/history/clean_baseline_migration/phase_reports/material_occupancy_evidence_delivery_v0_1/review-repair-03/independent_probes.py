"""Independent original-byte API/installed-CLI probes of the frozen R3 packet.

No author fixture builder or private temporal helper is used. The owner context
and supporting-source identities below are explicitly fictional assumptions.
"""
from pathlib import Path
from datetime import datetime, timezone
import copy
import hashlib
import importlib.util
import itertools
import json
import os
import shutil
import subprocess
import sys
import rfc8785
from jsonschema import Draft202012Validator

HERE=Path(__file__).resolve().parent
SNAP=HERE/'snapshot'
D=copy.deepcopy
MATCH='MATCHED_SELECTED_OCCUPANCY_EVIDENCE'

def raw(v):return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def digest(v):return 'sha256:'+sha(rfc8785.dumps(v))
def key(b):return json.dumps(b,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def binding(name):return {'ref':'review:'+name,'revisionRef':'review:r1'}
def refs(v):
    if isinstance(v,dict):
        if set(v)=={'ref','revisionRef'} or set(v)=={'ref','digest'}:yield v
        else:
            for child in v.values():yield from refs(child)
    elif isinstance(v,list):
        for child in v:yield from refs(child)
def stamp(day,ns=0):return f'2026-10-{day:02d}T00:00:00'+(f'.{ns:09d}' if ns else '')+'Z'
def point(day,ns=0):return {'mode':'AS_OF','at':stamp(day,ns)}
def interval(a,b,ai=True,bi=False):return {'mode':'INTERVAL','start':stamp(a),'end':stamp(b),'startInclusive':ai,'endInclusive':bi}
def endpoint(day,inclusive=True,ns=0):return {'posture':'KNOWN','at':stamp(day,ns),'inclusive':inclusive}
def record(a=1,b=21,app=None,occupant='lot-a',episode='episode-a',ai=True,bi=False):
    return {'schemaVersion':'ofarm.materialOccupancyEvidence.v0.1','facts':{
        'episodeId':'review:'+episode,'direction':'MATERIAL_TO_PLACE','relationKind':'OCCUPIES','relationConcept':binding('occupies'),
        'occupant':{'kind':'LOT','binding':binding(occupant)},'place':{'kind':'CONTAINER','binding':binding('container')},
        'interval':{'start':endpoint(a,ai),'end':endpoint(b,bi)},'applicability':app or point(20),
        'occupiedQuantity':{'posture':'REPORTED','quantityKind':binding('mass'),'decimal':'25.00','unitIdentity':binding('kg'),
            'originalLexicalValue':'25.00','originalUnitText':'kg','qualifier':'EXACT'},
        'occupiedCohort':{'posture':'IDENTIFIED','binding':binding('cohort')},'relevantExtent':{'posture':'WHOLE'},
        'sourcePosture':{'validity':'VALID','dispute':'UNDISPUTED','revision':'CURRENT','assessedAt':stamp(21),'ownerEvidence':[binding('status')],'supersededBy':[]},
        'sourceEvidence':[binding('raw-observation')],'lifecycleEvidence':[]}}

# Check the exact record discriminator without importing a fixture generator.
RECORD_VERSION=json.loads((SNAP/'schemas/record.schema.json').read_bytes())['properties']['schemaVersion']['const']

def make(records=None,query=None,extra=None,fixed=None,digest_selectors=False):
    records=D(records if records is not None else [record()]);query=D(query or point(20));extra=extra or {}
    context={'schemaVersion':'ofarm.materialOccupancyOwnerContext.v0.1','contractId':'ofarm.material-occupancy-evidence.v0.1',
        'ownerContextId':'review:owner-context','ownerIdentity':binding('owner'),'fixedAt':fixed or stamp(22),
        'selection':{'place':{'kind':'CONTAINER','binding':binding('container')},'applicability':query,
            'inventoryPosture':'COMPLETE_FOR_SELECTED_PLACE_AND_APPLICABILITY','selectionBasis':[binding('inventory-selection')]},
        'episodeBindings':[],'records':[]}
    request={'schemaVersion':'ofarm.materialOccupancyRequest.v0.1','selection':D(context['selection']),'episodes':[]}
    values={}; episodes=[]
    for i,r in enumerate(records):
        r['schemaVersion']=RECORD_VERSION;b=binding('source-'+str(i))
        if digest_selectors:b={'ref':b['ref'],'digest':digest(r)}
        values[key(b)]=raw(r);episodes.append(b);context['episodeBindings'].append(b)
        request['episodes'].append({'binding':D(b),'expectedFacts':D(r['facts'])})
    needed={key(b):b for b in refs([context['selection'],context['ownerIdentity'],[r['facts'] for r in records]])}
    for k,b in needed.items():
        if k in values:continue
        data=extra.get(b['ref'],b'Independent fictional retained observation bytes.\x00\xff\n' if b['ref']=='review:raw-observation' else raw({'reviewFixtureSource':b['ref']}))
        values[k]=data
        mode='RAW_BYTES' if b['ref']=='review:raw-observation' or b['ref'].startswith('review:binary-') else 'JCS_JSON'
        context['records'].append({'binding':b,'bytesSha256':sha(data),'valueDigest':'sha256:'+sha(data) if mode=='RAW_BYTES' else digest(json.loads(data)),
            'digestMode':mode,'role':'SUPPORTING_SOURCE'})
    for b,r in zip(episodes,records):
        data=values[key(b)];context['records'].append({'binding':b,'bytesSha256':sha(data),'valueDigest':digest(r),'digestMode':'JCS_JSON','role':'EPISODE'})
    return {'request':raw(request),'context':raw(context),'records':values}

spec=importlib.util.spec_from_file_location('independent_review_occupancy',SNAP/'verify_occupancy.py')
api=importlib.util.module_from_spec(spec);spec.loader.exec_module(api)
CONTRACT_SHA=sha((SNAP/'contract.json').read_bytes())
results=[];failures=[]

def pins(c):return {'contractSha256':CONTRACT_SHA,'contextSha256':sha(c['context']),'requestSha256':sha(c['request'])}
def save(name,c,report):
    folder=HERE/'cases'/name;folder.mkdir(parents=True,exist_ok=True)
    (folder/'request.json').write_bytes(c['request']);(folder/'context.json').write_bytes(c['context'])
    (folder/'trusted-pins.json').write_bytes(raw(pins(c)));(folder/'report.json').write_bytes(raw(report))
    mapping=[]
    for n,(k,b) in enumerate(c['records'].items()):
        path=f'original-{n}.bin';(folder/path).write_bytes(b);mapping.append({'binding':json.loads(k),'path':path})
    (folder/'record-map.json').write_bytes(raw(mapping))
    return folder

def check(name,c,expect=True,assertion=None,code=None,save_case=False):
    report=api.verify(c['request'],c['context'],c['records'],trusted_pins=pins(c),package_root=SNAP,source_root=SNAP)
    okay=(report['status']==MATCH)==expect
    if code:okay=okay and code in [v['code'] for v in report['errors']]
    if expect:
        req=json.loads(c['request']);ctx=json.loads(c['context'])
        okay=okay and len(report['episodes'])==len(req['episodes']) and report['selection']==ctx['selection'] and report['fixedAt']==ctx['fixedAt']
        okay=okay and report['runtimeAdmission']==report['actualInventoryCompleteness']=='NOT_ESTABLISHED'
        okay=okay and all(a['binding']==b['binding'] and a['facts']==b['expectedFacts'] for a,b in zip(report['episodes'],req['episodes']))
        okay=okay and report['boundRecords']==ctx['records']
    else:okay=okay and report['episodes']==[]
    if assertion:
        try:okay=okay and assertion(report)
        except (KeyError,IndexError,TypeError):okay=False
    row={'name':name,'passed':bool(okay),'status':report['status'],'errorCodes':[v['code'] for v in report['errors']]}
    results.append(row)
    if save_case or not okay:save(name,c,report)
    if not okay:failures.append(row)
    return report

# Explicit new turnover and repeated-visit scenarios; no author builder.
q=interval(15,20)
a=record(1,17,interval(15,17),episode='visit-a')
b=record(17,21,interval(17,20),occupant='lot-b',episode='visit-b')
c=record(1,21,q,occupant='lot-c',episode='visit-c')
check('turnover',make([a,b],q),assertion=lambda r:[e['selectedWindowCoverage'] for e in r['episodes']]==['PARTIAL_WINDOW']*2 and all(not e['selectedPostureSupportsUnqualifiedClaim'] for e in r['episodes']),save_case=True)
check('turnover-plus-full',make([a,b,c],q),assertion=lambda r:[e['selectedWindowCoverage'] for e in r['episodes']]==['PARTIAL_WINDOW','PARTIAL_WINDOW','FULL_WINDOW'] and [e['selectedPostureSupportsUnqualifiedClaim'] for e in r['episodes']]==[False,False,True],save_case=True)
a2=record(18,20,interval(18,20),episode='visit-a-again')
check('two-visits-same-lot',make([a,a2],q),assertion=lambda r:len(r['episodes'])==2 and r['episodes'][0]['facts']['occupant']==r['episodes'][1]['facts']['occupant'],save_case=True)
check('narrow-support-full-original',make([record(1,21,interval(16,18))],q),assertion=lambda r:r['episodes'][0]['queryIntersection']==q and r['episodes'][0]['coveredApplicability']==interval(16,18) and r['episodes'][0]['selectedWindowCoverage']=='PARTIAL_WINDOW',save_case=True)
check('asof-point',make(),assertion=lambda r:r['episodes'][0]['coveredApplicability']==point(20) and r['episodes'][0]['selectedWindowCoverage']=='FULL_WINDOW')
check('empty-selected-window',make([],q),assertion=lambda r:r['episodes']==[] and r['actualInventoryCompleteness']=='NOT_ESTABLISHED')

# Independent finite-window oracle: select extrema then test each tied bound
# against both windows' membership, instead of using the candidate's helper.
def ns(t):
    date,time=t[:-1].split('T');clock,_,fraction=time.partition('.')
    dt=datetime.fromisoformat(date+'T'+clock).replace(tzinfo=timezone.utc)
    return int(dt.timestamp())*10**9+int(fraction.ljust(9,'0') or '0')
def bounds(w):
    return (w['at'],True,w['at'],True) if w['mode']=='AS_OF' else (w['start'],w['startInclusive'],w['end'],w['endInclusive'])
def includes(w,t):
    a,ai,b,bi=bounds(w);n=ns(t)
    return (n>ns(a) or n==ns(a) and ai) and (n<ns(b) or n==ns(b) and bi)
def intersect(x,y):
    a,ai,b,bi=bounds(x);c,ci,d,di=bounds(y)
    lo=max([a,c],key=ns);hi=min([b,d],key=ns)
    li=includes(x,lo) and includes(y,lo);ri=includes(x,hi) and includes(y,hi)
    if ns(lo)>ns(hi) or ns(lo)==ns(hi) and not(li and ri):return None
    return {'mode':'AS_OF','at':lo} if ns(lo)==ns(hi) else {'mode':'INTERVAL','start':lo,'end':hi,'startInclusive':li,'endInclusive':ri}

grid=[]
for x,y in [(14,15),(14,17),(15,20),(16,18),(20,21),(19,21)]:
 for ai,bi,qi,qz in itertools.product([False,True],repeat=4):
    window=interval(15,20,qi,qz);app=interval(x,y,ai,bi);expected=intersect(app,window)
    rr=record(1,21,app,bi=True)
    n=f'grid-{x}-{y}-{int(ai)}{int(bi)}{int(qi)}{int(qz)}'
    check(n,make([rr],window),expect=expected is not None,assertion=(lambda r,e=expected,w=window:r['episodes'][0]['coveredApplicability']==e and r['episodes'][0]['queryIntersection']==w and r['episodes'][0]['selectedWindowCoverage']==('FULL_WINDOW' if e==w else 'PARTIAL_WINDOW')) if expected else None,code=None if expected else 'SOURCE_APPLICABILITY_MISMATCH')
for side in ['start','end']:
 for inclusive in [False,True]:
    rr=record(15,20,point(15 if side=='start' else 20),ai=inclusive if side=='start' else True,bi=inclusive if side=='end' else False)
    check(f'asof-{side}-{inclusive}',make([rr],point(15 if side=='start' else 20)),expect=inclusive,code=None if inclusive else ('KNOWN_START_EXCLUDES_SOURCE_APPLICABILITY' if side=='start' else 'KNOWN_END_EXCLUDES_SOURCE_APPLICABILITY'))
# Original interval and source intersection are both exactly one included point.
r=record(20,20,point(20),bi=True)
check('one-point-original-episode',make([r],interval(19,21)),assertion=lambda r:r['episodes'][0]['queryIntersection']==point(20) and r['episodes'][0]['coveredApplicability']==point(20),save_case=True)
r=record(1,21,point(20,1));r['facts']['interval']['end']=endpoint(20,True,1)
check('nanosecond-included',make([r],point(20,1)),assertion=lambda r:r['episodes'][0]['coveredApplicability']==point(20,1),save_case=True)
r['facts']['interval']['end']['inclusive']=False
check('nanosecond-excluded',make([r],point(20,1)),False,code='KNOWN_END_EXCLUDES_SOURCE_APPLICABILITY',save_case=True)

for kind in ['query-point','query-interval','source-applicability','known-start','known-end','open-end','assessment']:
 r=record();query=point(20)
 if kind=='query-point':query=point(22,1)
 if kind=='query-interval':query=interval(20,22);query['end']=stamp(22,1)
 if kind=='source-applicability':r['facts']['applicability']=interval(20,22);r['facts']['applicability']['end']=stamp(22,1);r['facts']['interval']['end']={'posture':'UNKNOWN','basis':binding('raw-observation')}
 if kind=='known-start':r['facts']['interval']['start']=endpoint(22,True,1)
 if kind=='known-end':r['facts']['interval']['end']=endpoint(22,False,1)
 if kind=='open-end':r['facts']['interval']['end']={'posture':'OPEN_AS_OF','asOf':stamp(22,1),'basis':binding('raw-observation')}
 if kind=='assessment':r['facts']['sourcePosture']['assessedAt']=stamp(22,1)
 code={'query-point':'SELECTION_AFTER_CONTEXT','query-interval':'SELECTION_AFTER_CONTEXT','source-applicability':'SOURCE_APPLICABILITY_AFTER_CONTEXT','known-start':'KNOWN_BOUNDARY_AFTER_CONTEXT','known-end':'KNOWN_BOUNDARY_AFTER_CONTEXT','open-end':'OPEN_POSTURE_AFTER_CONTEXT','assessment':'POSTURE_AFTER_CONTEXT'}[kind]
 check('horizon-'+kind,make([r],query),False,code=code,save_case=True)
for unknown in ['UNKNOWN','UNBOUNDED']:
 for side in ['start','end']:
    r=record();r['facts']['interval'][side]={'posture':unknown,'basis':binding('raw-observation')}
    check(f'unresolved-{side}-{unknown}',make([r]),assertion=lambda r:r['episodes'][0]['temporalCoverage']=='UNRESOLVED' and r['episodes'][0]['coveredApplicability'] is None and r['episodes'][0]['queryIntersection'] is None and not r['episodes'][0]['selectedPostureSupportsUnqualifiedClaim'],save_case=True)
    opposite='end' if side=='start' else 'start';r['facts']['interval'][opposite]=endpoint(19 if opposite=='end' else 21)
    check(f'unresolved-keeps-known-contradiction-{side}-{unknown}',make([r]),False,code='KNOWN_END_EXCLUDES_SOURCE_APPLICABILITY' if opposite=='end' else 'KNOWN_START_EXCLUDES_SOURCE_APPLICABILITY')
r=record();r['facts']['interval']['end']={'posture':'OPEN_AS_OF','asOf':stamp(20),'basis':binding('raw-observation')}
check('observed-open-at-query',make([r]),assertion=lambda r:r['episodes'][0]['queryIntersectionBasis']=='OBSERVED_OPEN_RANGE' and r['episodes'][0]['selectedPostureSupportsUnqualifiedClaim'],save_case=True)
r['facts']['applicability']=point(20,1)
check('open-one-nanosecond-too-early',make([r],point(20,1)),False,code='OPEN_END_OBSERVATION_EXCLUDES_SOURCE_APPLICABILITY')

qualifiers=['EXACT','ESTIMATED','MINIMUM','MAXIMUM','RANGE_MIDPOINT','LABEL_LIMIT','MACHINE_REPORTED','HUMAN_REPORTED','UNKNOWN']
for qualifier,cohort in itertools.product(qualifiers,[False,True]):
 r=record();r['facts']['occupiedQuantity']['qualifier']=qualifier
 if not cohort:r['facts']['occupiedCohort']={'posture':'UNREPORTED','reason':'Independent test has no cohort selection.'}
 check(f'quantity-{qualifier}-cohort-{cohort}',make([r]),assertion=lambda v,e=qualifier=='EXACT':v['episodes'][0]['quantitySupportsUnqualifiedClaim']==e and v['episodes'][0]['selectedPostureSupportsUnqualifiedClaim']==e,save_case=qualifier in ['UNKNOWN','MAXIMUM'])
for cohort in [False,True]:
 r=record();r['facts']['occupiedQuantity']={'posture':'UNREPORTED','unitIdentity':binding('kg'),'reason':'Amount not reported.'}
 if not cohort:r['facts']['occupiedCohort']={'posture':'UNREPORTED','reason':'No identified cohort.'}
 check(f'unreported-amount-cohort-{cohort}',make([r]),assertion=lambda v,e=cohort:not v['episodes'][0]['quantitySupportsUnqualifiedClaim'] and v['episodes'][0]['selectedPostureSupportsUnqualifiedClaim']==e)

# Full original event/measurement records remain opaque and unchanged. Each
# newly fictional result form is separately shape-checked against frozen owners.
foreign=SNAP/'foreign-fixtures';es=json.loads((foreign/'event.schema.json').read_bytes());ms=json.loads((foreign/'measurement.schema.json').read_bytes())
event=json.loads((foreign/'event-intervention.json').read_bytes());numeric=json.loads((foreign/'measurement-numeric.json').read_bytes())
measurements={'NUMERIC':numeric,'CENSORED_NUMERIC':json.loads((foreign/'measurement-censored.json').read_bytes()),'ABSENT_PENDING':json.loads((foreign/'measurement-pending.json').read_bytes())}
for k,value in [('CODED',{'resultKind':'CODED','codedValueRef':'review:code','originalLexicalValue':'reported code'}),('QUALITATIVE',{'resultKind':'QUALITATIVE','qualitativeValue':'Reported observation','originalLexicalValue':'Reported observation'})]:
 m=D(numeric);m['result']=value;measurements[k]=m
for family in ['StructureEvent','ObservationEvent','OccurrenceEvent','InterventionEvent','MaterialEvent','EvidenceEvent','GovernanceEvent']:
 e=D(event);e['primaryEventFamily']=family;e.pop('eventSubtypeId',None);e['dominantSemanticConsequence']='Fictional retained '+family+' record for independent byte-fidelity testing.'
 assert Draft202012Validator(es).is_valid(e)
 for k,m in measurements.items():
    assert Draft202012Validator(ms).is_valid(m)
    r=record();r['facts']['sourceEvidence'] += [binding('event'),binding('measurement')]
    fixture=make([r],extra={'review:event':raw(e),'review:measurement':raw(m)})
    check('foreign-'+family+'-'+k,fixture,save_case=True)
    altered=D(fixture);altered['records'][key(binding('measurement'))]+=b'\n'
    check('foreign-raw-mutation-'+family+'-'+k,altered,False,code='ORIGINAL_BYTES_MISMATCH')

# Selection/order/source integrity attacks use deliberately unchanged or
# independently reselected pins as stated; no expected dictionary is an oracle.
base=make([a,b,c],q)
for attack in ['drop','reorder','duplicate','extra','manifest-order','changed-fact','missing-original','extra-original','raw-whitespace','raw-binary','extra-consistent-reference','missing-consistent-reference']:
 t=D(base);rq=json.loads(t['request']);cx=json.loads(t['context'])
 if attack=='drop':rq['episodes'].pop(1)
 if attack=='reorder':rq['episodes'].reverse()
 if attack=='duplicate':rq['episodes'].append(D(rq['episodes'][0]))
 if attack=='extra':rq['episodes'].append({'binding':binding('extra-source'),'expectedFacts':D(rq['episodes'][0]['expectedFacts'])})
 if attack=='manifest-order':
    original=[v for v in cx['records'] if v['role']=='EPISODE'];cx['records']=[v for v in cx['records'] if v['role']!='EPISODE']+list(reversed(original))
 if attack=='changed-fact':rq['episodes'][0]['expectedFacts']['occupiedQuantity']['decimal']='26.00'
 if attack=='missing-original':t['records'].pop(next(iter(t['records'])))
 if attack=='extra-original':t['records'][key(binding('unexpected'))]=b'{}'
 if attack=='raw-whitespace':t['records'][key(cx['episodeBindings'][0])]+=b'\n'
 if attack=='raw-binary':t['records'][key(binding('raw-observation'))]+=b'changed'
 if attack=='extra-consistent-reference':
    x=binding('unreferenced');t['records'][key(x)]=b'{}';cx['records'].append({'binding':x,'bytesSha256':sha(b'{}'),'valueDigest':digest({}),'digestMode':'JCS_JSON','role':'SUPPORTING_SOURCE'})
 if attack=='missing-consistent-reference':
    k=key(binding('kg'));t['records'].pop(k);cx['records']=[v for v in cx['records'] if key(v['binding'])!=k]
 t.update(request=raw(rq),context=raw(cx))
 check('attack-'+attack,t,False,save_case=True)
check('digest-selected-sources',make([a,b],q,digest_selectors=True),save_case=True)

# Split-lane installation uses only pinned integration-map entries and remains
# inside this review directory. The frozen candidate/snapshot are never edited.
integration=json.loads((SNAP/'integration-map.json').read_bytes());installed=HERE/'installed';installed.mkdir(exist_ok=True)
for entry in integration['files']:
 data=(SNAP/entry['source']).read_bytes();assert sha(data)==entry['sha256'] and len(data)==entry['bytes']
 dest=installed/entry['destination'];assert dest.resolve().is_relative_to(installed.resolve());dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
package=installed/integration['packageRoot'];source_root=installed/integration['fixtureRoot'];checker=installed/integration['checkerRoot']/'verify_occupancy.py'
for name in ['turnover','turnover-plus-full','two-visits-same-lot','one-point-original-episode','nanosecond-included','nanosecond-excluded','horizon-known-end','quantity-MAXIMUM-cohort-True','unresolved-end-UNBOUNDED','foreign-ObservationEvent-ABSENT_PENDING','attack-raw-binary','digest-selected-sources']:
 folder=HERE/'cases'/name;output=folder/'installed-cli-report.json'
 command=[sys.executable,'-B',str(checker),'--request',str(folder/'request.json'),'--context',str(folder/'context.json'),'--record-map',str(folder/'record-map.json'),'--trusted-pins',str(folder/'trusted-pins.json'),'--package-root',str(package),'--source-root',str(source_root),'--out',str(output)]
 run=subprocess.run(command,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
 value=json.loads(output.read_bytes()) if output.exists() else None;api_report=json.loads((folder/'report.json').read_bytes())
 okay=value==api_report and run.returncode==(0 if api_report['status']==MATCH else 1)
 row={'name':'installed-cli-'+name,'passed':okay,'exitCode':run.returncode,'stderr':run.stderr}
 results.append(row)
 if not okay:failures.append(row)
summary={'status':'PASS' if not failures else 'FAIL','candidateSealSha256':'5c0a0119085d77223060d30c92a79990d525133f338e17f2e405ed71c57e3609','contractRawSha256':CONTRACT_SHA,
    'provenance':'Independent test builder and interval oracle; imported only frozen public API. Domain semantics author, not repair implementation author. Not formal GitHub approval.',
    'counts':{'checks':len(results),'passed':sum(v['passed'] for v in results),'fullForeignPairs':35,'installedCliCases':12,'integrationMappings':len(integration['files'])},'failures':failures,'results':results}
(HERE/'independent-results.json').write_bytes(raw(summary));print(json.dumps({k:v for k,v in summary.items() if k!='results'},indent=2))
raise SystemExit(0 if not failures else 1)
