"""Explicit, offline occupancy evidence checks; never a default CI gate."""
from pathlib import Path
import argparse
import copy
import json
import subprocess
import sys
import tempfile
from generate_fixtures import raw, sha, digest, make_case, write_case
from verify_occupancy import verify, selector_key, strict, binding_keys

def read_case(root):
    mapping = json.loads((root/'record-map.json').read_bytes())
    return {'request':(root/'request.json').read_bytes(), 'context':(root/'context.json').read_bytes(), 'records':{selector_key(r['binding']):(root/r['path']).read_bytes() for r in mapping}}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--package-root', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--fixture-root', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--source-root', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    source_root = args.source_root or args.fixture_root
    contract_sha = sha((args.package_root/'contract.json').read_bytes())
    rows = []
    def call(case, pins=None):
        pins = pins or {'contractSha256':contract_sha,'contextSha256':sha(case['context']),'requestSha256':sha(case['request'])}
        return verify(case['request'],case['context'],case['records'],trusted_pins=pins,package_root=args.package_root,source_root=source_root)
    def check(name, case, expected=True, extra=None, pins=None):
        report = call(case, pins)
        observed = report['status'] == 'MATCHED_SELECTED_OCCUPANCY_EVIDENCE'
        ok = observed == expected and (extra(report) if extra else True)
        rows.append({'name':name,'pass':ok,'status':report['status'],'errors':report['errors'][:3]})
        return report
    catalog = json.loads((args.fixture_root/'fixtures/catalog.json').read_bytes())
    for name in catalog['cases']:
        case = read_case(args.fixture_root/'fixtures'/name)
        expected_unqualified = name not in {'unknown-start','unbounded-start','unknown-end','unbounded-end','both-unreported','unresolved-extent','invalid','disputed','unknown-validity','unknown-dispute','superseded','unknown-revision','interval-turnover','interval-two-visits'} and not name.startswith('qualifier-')
        check('positive/'+name,case,extra=lambda r, value=expected_unqualified, n=name: ([e['selectedPostureSupportsUnqualifiedClaim'] for e in r['episodes']] == [False,False,True] if n=='interval-turnover-plus-full' else all(e['selectedPostureSupportsUnqualifiedClaim'] == value for e in r['episodes'])) and r['runtimeAdmission'] == r['actualInventoryCompleteness'] == 'NOT_ESTABLISHED')
    baseline = make_case('independent-hostile-base',selector_mode='revision')
    def change_request(name, change):
        case = copy.deepcopy(baseline); request = strict(case['request']); change(request); case['request'] = raw(request)
        check(name,case,False)
    change_request('wrong-unit-same-number',lambda r:r['episodes'][0]['expectedFacts']['occupiedQuantity']['unitIdentity'].update(revisionRef='fixture:unit-litre/r1'))
    change_request('wrong-quantity-kind-same-number',lambda r:r['episodes'][0]['expectedFacts']['occupiedQuantity']['quantityKind'].update(revisionRef='fixture:count/r1'))
    change_request('wrong-occupant-alias',lambda r:r['episodes'][0]['expectedFacts']['occupant']['binding'].update(ref='fixture:alias'))
    change_request('wrong-relationship-revision',lambda r:r['episodes'][0]['expectedFacts']['relationConcept'].update(revisionRef='fixture:occupies/r2'))
    change_request('omitted-episode',lambda r:r['episodes'].clear())
    change_request('duplicate-episode',lambda r:r['episodes'].append(copy.deepcopy(r['episodes'][0])))
    # Every retained fact leaf is covered by schema or complete semantic comparison.
    def leaves(value,path=()):
        if isinstance(value,dict):
            for k,v in value.items(): yield from leaves(v,path+(k,))
        elif isinstance(value,list):
            for i,v in enumerate(value): yield from leaves(v,path+(i,))
        else: yield path,value
    leaf_count=0
    for path,value in leaves(strict(baseline['request'])['episodes'][0]['expectedFacts']):
        case=copy.deepcopy(baseline); request=strict(case['request']); target=request['episodes'][0]['expectedFacts']
        for key in path[:-1]: target=target[key]
        target[path[-1]] = not value if isinstance(value,bool) else str(value)+'_changed'
        case['request']=raw(request);check('fact-leaf/'+('/'.join(map(str,path))),case,False);leaf_count+=1
    # Preserve the independent selected context while changing submitted bytes.
    for kind in ('missing-source','extra-source','changed-original-whitespace','changed-original-bytes','revision-alias','digest-selector-substitution'):
        case=copy.deepcopy(baseline); key=next(iter(case['records']))
        if kind=='missing-source': del case['records'][key]
        elif kind=='extra-source': case['records']['extra']=b'{}'
        elif kind=='changed-original-whitespace': case['records'][key]+=b'\n'
        elif kind=='changed-original-bytes': case['records'][key]=b'{}'
        else:
            new=json.loads(key)
            if kind=='revision-alias': new['ref']='fixture:other'
            else: new={'ref':new['ref'],'digest':'sha256:'+sha(case['records'][key])}
            case['records'][selector_key(new)]=case['records'].pop(key)
        check(kind,case,False)
    for pin in ('contractSha256','contextSha256','requestSha256'):
        pins={'contractSha256':contract_sha,'contextSha256':sha(baseline['context']),'requestSha256':sha(baseline['request'])};pins[pin]='0'*64
        check('wrong-independent-'+pin,baseline,False,pins=pins)
    for kind,data in [('duplicate-json',b'{"schemaVersion":1,"schemaVersion":2}'),('invalid-utf8',b'\xff'),('bom',b'\xef\xbb\xbf{}'),('not-json',b'no'),('nonfinite',b'{"x":NaN}'),('deep-json',b'['*65+b'0'+b']'*65),('unsafe-number',b'{"x":9007199254740993}'),('oversized',b' '*2097153)]:
        case=copy.deepcopy(baseline);case['request']=data;check(kind,case,False)
    # Independently selected but internally contradictory source fixtures must fail.
    def source_change(name,change,expected=False,extra=None):
        case=copy.deepcopy(baseline);context=strict(case['context']);request=strict(case['request']);key=selector_key(context['episodeBindings'][0]);record=strict(case['records'][key]);change(record['facts']);case['records'][key]=raw(record)
        request['episodes'][0]['expectedFacts']=copy.deepcopy(record['facts'])
        for entry in context['records']:
            if selector_key(entry['binding'])==key:
                entry.update(bytesSha256=sha(case['records'][key]),valueDigest=digest(record))
        case.update(context=raw(context),request=raw(request));check(name,case,expected,extra)
    source_change('reversed-direction',lambda f:f.update(direction='PLACE_TO_MATERIAL'))
    source_change('reversed-endpoints',lambda f:f.update(occupant=f['place'],place=f['occupant']))
    # Same durable identity remains contradictory even with complete consistent
    # selected source mappings. Different revision spelling cannot disguise it.
    for spelling in ('same-selector','different-revision'):
        case=copy.deepcopy(baseline);ctx=strict(case['context']);request=strict(case['request']);key=selector_key(ctx['episodeBindings'][0]);record=strict(case['records'][key]);old=copy.deepcopy(record['facts']['occupant']['binding'])
        replacement=copy.deepcopy(record['facts']['place']['binding'])
        if spelling=='different-revision':
            replacement['revisionRef']='fixture:place/r2';other=selector_key(replacement);original=selector_key(record['facts']['place']['binding']);case['records'][other]=case['records'][original]
            entry=copy.deepcopy(next(e for e in ctx['records'] if selector_key(e['binding'])==original));entry['binding']=replacement;ctx['records'].append(entry)
        record['facts']['occupant']['binding']=replacement;case['records'][key]=raw(record);request['episodes'][0]['expectedFacts']=copy.deepcopy(record['facts'])
        needed=set(binding_keys(record['facts']))|set(binding_keys(ctx['selection']))|set(binding_keys(ctx['ownerIdentity']))|{key}
        ctx['records']=[e for e in ctx['records'] if selector_key(e['binding']) in needed];case['records']={k:v for k,v in case['records'].items() if k in needed}
        for e in ctx['records']:
            if selector_key(e['binding'])==key:e.update(bytesSha256=sha(case['records'][key]),valueDigest=digest(record))
        case.update(context=raw(ctx),request=raw(request));check('same-occupant-place-identity/'+spelling,case,False,extra=lambda r:any(e['code']=='OCCUPANT_AND_PLACE_IDENTITY_NOT_DISTINCT' for e in r['errors']))
    source_change('interval-reversed',lambda f:f['interval']['end'].update(at='2026-09-01T00:00:00Z'))
    source_change('start-excludes-query',lambda f:f['interval']['start'].update(at='2026-10-20T10:00:00Z',inclusive=False))
    source_change('end-excludes-query',lambda f:f['interval']['end'].update(at='2026-10-20T10:00:00Z',inclusive=False))
    source_change('source-applicability-outside-query',lambda f:f['applicability'].update(at='2026-10-19T00:00:00Z'))
    source_change('future-status-assessment',lambda f:f['sourcePosture'].update(assessedAt='2026-10-22T00:00:00Z'))
    source_change('unproven-superseded-status',lambda f:f['sourcePosture'].update(revision='SUPERSEDED'))
    def unknown_opposite(f,variant):
        basis=copy.deepcopy(f['sourceEvidence'][0])
        if variant in ('known-start-after','known-start-exclusive'):
            f['interval']['end']={'posture':'UNKNOWN','basis':basis}
            f['interval']['start'].update(at='2026-10-21T00:00:00Z' if variant=='known-start-after' else '2026-10-20T10:00:00Z',inclusive=variant!='known-start-exclusive')
        else:
            f['interval']['start']={'posture':'UNKNOWN','basis':basis}
            if variant=='open-end-before':f['interval']['end']={'posture':'OPEN_AS_OF','asOf':'2026-10-19T00:00:00Z','basis':basis}
            else:f['interval']['end'].update(at='2026-10-19T00:00:00Z' if variant=='known-end-before' else '2026-10-20T10:00:00Z',inclusive=variant!='known-end-exclusive')
    for variant in ('known-start-after','known-start-exclusive','known-end-before','known-end-exclusive','open-end-before'):
        source_change('unknown-opposite/'+variant,lambda f,v=variant:unknown_opposite(f,v))
    for bad in ['2026-02-30T00:00:00Z','2026-10-01T24:00:00Z','2026-10-01T00:00:60Z','2026-10-01T00:00:00+00:00','2026-10-01T00:00:00+01:99','2026-10-01t00:00:00z','0000-10-01T00:00:00Z','2026-10-01T00:00:00.1234567890Z']:
        source_change('invalid-timestamp/'+bad,lambda f,v=bad:f['interval']['start'].update(at=v))
    overlap=make_case('overlap-rejection',selector_mode='revision',variant='overlapping-repeated')
    for name,mutate in [('drop-middle',lambda r:r['episodes'].pop(1)),('reorder',lambda r:r['episodes'].reverse())]:
        case=copy.deepcopy(overlap);request=strict(case['request']);mutate(request);case['request']=raw(request);check('episode-inventory/'+name,case,False)
    report=check('overlap-retained-exact',overlap,extra=lambda r:len(r['episodes'])==3 and len({e['facts']['episodeId'] for e in r['episodes']})==3)
    # A real lifecycle token cannot replace the new typed occupancy source.
    case=copy.deepcopy(baseline);ctx=strict(case['context']);key=selector_key(ctx['episodeBindings'][0]);case['records'][key]=(source_root/'sources/container-continuity-example.json').read_bytes()
    for e in ctx['records']:
        if selector_key(e['binding'])==key:e.update(bytesSha256=sha(case['records'][key]),valueDigest=digest(strict(case['records'][key])))
    case['context']=raw(ctx);check('bare-lifecycle-token',case,False)
    # Full foreign bodies stay opaque to occupancy; test validity separately against
    # the exact existing owner schemas, then test retention and raw-byte binding.
    from jsonschema import Draft202012Validator
    foreign=args.fixture_root/'foreign-fixtures'
    es=json.loads((foreign/'event.schema.json').read_bytes());ms=json.loads((foreign/'measurement.schema.json').read_bytes())
    event=json.loads((foreign/'event-intervention.json').read_bytes())
    numeric=json.loads((foreign/'measurement-numeric.json').read_bytes())
    measurements={'NUMERIC':numeric,'CENSORED_NUMERIC':json.loads((foreign/'measurement-censored.json').read_bytes()),'ABSENT_PENDING':json.loads((foreign/'measurement-pending.json').read_bytes())}
    for kind,result in [('CODED',{'resultKind':'CODED','codedValueRef':'fixture:observed-code','originalLexicalValue':'selected code'}),('QUALITATIVE',{'resultKind':'QUALITATIVE','qualitativeValue':'Retained qualitative observation','originalLexicalValue':'Retained qualitative observation'})]:
        measurement=copy.deepcopy(numeric);measurement['result']=result;measurements[kind]=measurement
    for family in ('StructureEvent','ObservationEvent','OccurrenceEvent','InterventionEvent','MaterialEvent','EvidenceEvent','GovernanceEvent'):
        envelope=copy.deepcopy(event);envelope['primaryEventFamily']=family;envelope.pop('eventSubtypeId',None);envelope['dominantSemanticConsequence']='Fictional retained '+family+' fixture; no occurrence or classification admission is asserted.'
        assert Draft202012Validator(es).is_valid(envelope)
        for kind,measurement in measurements.items():
            assert Draft202012Validator(ms).is_valid(measurement)
            case=copy.deepcopy(baseline);ctx=strict(case['context']);request=strict(case['request']);key=selector_key(ctx['episodeBindings'][0]);record=strict(case['records'][key])
            for name,value in [('event',envelope),('measurement',measurement)]:
                data=raw(value);binding={'ref':'fixture:'+name,'revisionRef':'fixture:'+name+'/r1'};k=selector_key(binding);case['records'][k]=data
                ctx['records'].append({'binding':binding,'bytesSha256':sha(data),'valueDigest':digest(value),'digestMode':'JCS_JSON','role':'SUPPORTING_SOURCE'})
                record['facts']['sourceEvidence'].append(binding)
            case['records'][key]=raw(record);request['episodes'][0]['expectedFacts']=copy.deepcopy(record['facts'])
            for e in ctx['records']:
                if selector_key(e['binding'])==key:e.update(bytesSha256=sha(case['records'][key]),valueDigest=digest(record))
            case.update(context=raw(ctx),request=raw(request))
            check('full-foreign-bytes/'+family+'/'+kind,case,extra=lambda r:len(r['episodes'][0]['facts']['sourceEvidence'])==3)
            hostile=copy.deepcopy(case);hostile['records'][selector_key({'ref':'fixture:measurement','revisionRef':'fixture:measurement/r1'})]+=b'\n'
            check('changed-foreign-bytes/'+family+'/'+kind,hostile,False)
    with tempfile.TemporaryDirectory(prefix='occupancy-cli-') as tmp:
        tmp=Path(tmp);write_case(tmp,baseline,contract_sha)
        cmd=[sys.executable,'-B',str(Path(__file__).with_name('verify_occupancy.py')),'--request',str(tmp/'request.json'),'--context',str(tmp/'context.json'),'--record-map',str(tmp/'record-map.json'),'--trusted-pins',str(tmp/'trusted-pins.json'),'--package-root',str(args.package_root),'--source-root',str(source_root),'--out',str(tmp/'report.json')]
        result=subprocess.run(cmd,capture_output=True,text=True)
        rows.append({'name':'cli-positive','pass':result.returncode==0,'status':result.returncode,'errors':result.stderr[:500]})
        mapping=json.loads((tmp/'record-map.json').read_bytes());mapping.append(mapping[0]);(tmp/'record-map.json').write_bytes(raw(mapping))
        result=subprocess.run(cmd,capture_output=True,text=True)
        rows.append({'name':'cli-duplicate-map','pass':result.returncode!=0 and 'DUPLICATE_RECORD_FILE_SELECTOR' in (tmp/'report.json').read_text(),'status':result.returncode,'errors':result.stderr[:500]})
    with tempfile.TemporaryDirectory(prefix='occupancy-review-regressions-') as tmp:
        review_out=Path(tmp)/'report.json'
        review_run=subprocess.run([sys.executable,'-B',str(Path(__file__).with_name('run_review_regressions.py')),'--package-root',str(args.package_root),'--source-root',str(source_root),'--out',str(review_out)],capture_output=True,text=True)
        review_report=json.loads(review_out.read_bytes())
        for row in review_report['results']:
            rows.append({**row,'name':'review/'+row['name']})
        if review_run.returncode not in (0,1):
            rows.append({'name':'review/runner-completion','pass':False,'status':review_run.returncode,'errors':review_run.stderr})
    result={'status':'PASS' if all(r['pass'] for r in rows) else 'FAIL','primaryTrustBoundary':'Material occupancy source evidence','scopeStayedInsideBoundary':True,'contractSha256':contract_sha,'positiveCases':len(catalog['cases']),'fullForeignEventMeasurementPairs':35,'meaningLeavesMutated':leaf_count,'reviewRegressionChecks':review_report['checks'],'checks':len(rows),'passed':sum(r['pass'] for r in rows),'failed':[r for r in rows if not r['pass']],'results':rows,'runtimeAdmission':'NOT_ESTABLISHED','actualInventoryCompleteness':'NOT_ESTABLISHED'}
    args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_bytes(raw(result))
    print(json.dumps({k:v for k,v in result.items() if k!='results'},indent=2))
    return 0 if result['status']=='PASS' else 1

if __name__=='__main__': raise SystemExit(main())
