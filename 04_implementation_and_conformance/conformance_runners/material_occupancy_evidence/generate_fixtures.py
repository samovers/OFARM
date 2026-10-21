"""Generate explicitly fictional source-owner selections for interface checks."""
from pathlib import Path
import argparse
import copy
import hashlib
import json
import rfc8785
from verify_occupancy import selector_key, binding_keys

def raw(value): return (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode()
def sha(value): return hashlib.sha256(value).hexdigest()
def digest(value): return 'sha256:' + sha(rfc8785.dumps(value))

def make_case(name='base', selector_mode='digest', occupant_kind='LOT', place_kind='CONTAINER', variant='base'):
    records, entries = {}, {}
    count = 0
    def add(ref, value, role='SUPPORTING_SOURCE', binary=False):
        nonlocal count
        count += 1
        data = value if binary else raw(value)
        vd = 'sha256:' + sha(data) if binary else digest(value)
        revision = selector_mode == 'revision' or (selector_mode == 'mixed' and count % 2 == 0)
        binding = {'ref': ref, 'revisionRef': ref + '/r1'} if revision else {'ref': ref, 'digest': vd}
        key = selector_key(binding)
        records[key] = data
        entries[key] = {'binding': binding, 'bytesSha256': sha(data), 'valueDigest': vd, 'digestMode': 'RAW_BYTES' if binary else 'JCS_JSON', 'role': role}
        return binding
    def illustrative(ref):
        return add('fixture:' + ref, {'fixtureNotice':'Illustrative selected original bytes; no foreign schema, runtime truth or owner admission is asserted.', 'identity':ref})
    occupant = {'kind': occupant_kind, 'binding': illustrative('occupant')}
    place = {'kind': place_kind, 'binding': illustrative('place')}
    owner = illustrative('source-owner')
    selection_basis = illustrative('inventory-selection')
    unit = illustrative('unit-kilogram')
    relation = illustrative('occupies-relation-r1')
    evidence = add('fixture:source-observation', b'Fictional retained occupancy observation bytes.\n', binary=True)
    status_basis = illustrative('source-status-assessment')
    facts = {
        'episodeId': 'fixture:occupancy/episode-1', 'direction':'MATERIAL_TO_PLACE', 'relationKind':'OCCUPIES',
        'relationConcept':relation, 'occupant':occupant, 'place':place,
        'interval':{'start':{'posture':'KNOWN','at':'2026-10-01T00:00:00Z','inclusive':True},'end':{'posture':'KNOWN','at':'2026-11-01T00:00:00Z','inclusive':False}},
        'applicability':{'mode':'AS_OF','at':'2026-10-20T10:00:00Z'},
        'occupiedQuantity':{'posture':'REPORTED','quantityKind':illustrative('quantity-mass'), 'decimal':'25.00','unitIdentity':unit, 'originalLexicalValue':'25.00', 'originalUnitText':'kg','qualifier':'EXACT'},
        'occupiedCohort':{'posture':'IDENTIFIED','binding':illustrative('cohort-1')},
        'relevantExtent':{'posture':'WHOLE'},
        'sourcePosture':{'validity':'VALID','dispute':'UNDISPUTED','revision':'CURRENT','assessedAt':'2026-10-20T11:00:00Z','ownerEvidence':[status_basis],'supersededBy':[]},
        'sourceEvidence':[evidence], 'lifecycleEvidence':[]}
    if variant in ('unknown-start','unbounded-start'):
        facts['interval']['start'] = {'posture':'UNKNOWN' if variant.startswith('unknown') else 'UNBOUNDED','basis':illustrative(variant)}
    elif variant in ('unknown-end','unbounded-end'):
        facts['interval']['end'] = {'posture':'UNKNOWN' if variant.startswith('unknown') else 'UNBOUNDED','basis':illustrative(variant)}
    elif variant == 'open-end':
        facts['interval']['end'] = {'posture':'OPEN_AS_OF','asOf':'2026-10-20T11:00:00Z','basis':illustrative('open-end-observation')}
    elif variant == 'interval-query':
        facts['applicability'] = {'mode':'INTERVAL','start':'2026-10-15T00:00:00Z','end':'2026-10-20T00:00:00Z','startInclusive':True,'endInclusive':False}
    elif variant == 'nanosecond-point':
        facts['interval'] = {'start':{'posture':'KNOWN','at':'2026-10-20T10:00:00.123456789Z','inclusive':True}, 'end':{'posture':'KNOWN','at':'2026-10-20T10:00:00.123456789Z','inclusive':True}}
        facts['applicability'] = {'mode':'AS_OF','at':'2026-10-20T10:00:00.123456789Z'}
    elif variant == 'cohort-only':
        facts['occupiedQuantity'] = {'posture':'UNREPORTED','unitIdentity':unit,'reason':'Source identifies cohort without an amount.'}
    elif variant == 'quantity-only':
        facts['occupiedCohort'] = {'posture':'UNREPORTED','reason':'Source identifies an amount without a cohort.'}
    elif variant == 'both-unreported':
        facts['occupiedQuantity'] = {'posture':'UNREPORTED','unitIdentity':unit,'reason':'No amount in selected source.'}
        facts['occupiedCohort'] = {'posture':'UNREPORTED','reason':'No cohort in selected source.'}
    elif variant == 'partial':
        facts['relevantExtent'] = {'posture':'PARTIAL','binding':illustrative('retained-partial-extent')}
    elif variant == 'unresolved-extent':
        facts['relevantExtent'] = {'posture':'UNRESOLVED','reason':'Source extent is unresolved.'}
    elif variant in ('invalid','disputed','unknown-validity','unknown-dispute','historical','superseded','unknown-revision'):
        field, value = {'invalid':('validity','INVALID'),'disputed':('dispute','DISPUTED'),'unknown-validity':('validity','UNKNOWN'),'unknown-dispute':('dispute','UNKNOWN'),'historical':('revision','HISTORICAL_APPLICABLE'),'superseded':('revision','SUPERSEDED'),'unknown-revision':('revision','UNKNOWN')}[variant]
        facts['sourcePosture'][field] = value
        if variant == 'superseded':
            facts['sourcePosture']['supersededBy'] = [illustrative('successor-episode-source')]
    elif variant.startswith('qualifier-'):
        facts['occupiedQuantity']['qualifier'] = variant.removeprefix('qualifier-')
    all_facts = [facts]
    if variant == 'empty-inventory':
        all_facts = []
    if variant == 'overlapping-repeated':
        second = copy.deepcopy(facts)
        second['episodeId'] = 'fixture:occupancy/episode-2'
        second['interval']['start']['at'] = '2026-10-10T00:00:00Z'
        second['occupiedQuantity']['decimal'] = '3.000'
        second['occupiedQuantity']['originalLexicalValue'] = '3.000'
        third = copy.deepcopy(second)
        third['episodeId'] = 'fixture:occupancy/episode-3'
        third['occupant'] = {'kind':'MATERIAL','binding':illustrative('second-occupant')}
        all_facts += [second, third]
    episode_bindings = [add('fixture:occupancy/source-' + str(i), {'schemaVersion':'ofarm.material-occupancy-evidence.v0.1','facts':f}, 'EPISODE') for i,f in enumerate(all_facts)]
    selection = {'place':place,'applicability':copy.deepcopy(facts['applicability']), 'inventoryPosture':'COMPLETE_FOR_SELECTED_PLACE_AND_APPLICABILITY','selectionBasis':[selection_basis]}
    needed = set(binding_keys(all_facts)) | set(binding_keys(selection)) | set(binding_keys(owner)) | {selector_key(b) for b in episode_bindings}
    # Remove illustrative values that a variant explicitly replaced; no orphan inputs.
    records = {k:v for k,v in records.items() if k in needed}
    entries = {k:v for k,v in entries.items() if k in needed}
    context = {'schemaVersion':'ofarm.materialOccupancyOwnerContext.v0.1','contractId':'ofarm.material-occupancy-evidence.v0.1','ownerContextId':'fixture:owner-context/' + name,'ownerIdentity':owner, 'fixedAt':'2026-10-21T00:00:00Z','selection':selection,'episodeBindings':episode_bindings,'records':list(entries.values())}
    request = {'schemaVersion':'ofarm.materialOccupancyRequest.v0.1','selection':copy.deepcopy(selection),'episodes':[{'binding':b,'expectedFacts':copy.deepcopy(f)} for b,f in zip(episode_bindings,all_facts)]}
    return {'request':raw(request), 'context':raw(context), 'records':records}

def write_case(directory, case, contract_hash):
    directory.mkdir(parents=True, exist_ok=True)
    (directory/'request.json').write_bytes(case['request'])
    (directory/'context.json').write_bytes(case['context'])
    mapping = []
    for i, (key, value) in enumerate(case['records'].items()):
        name = f'record-{i:03}.bin'
        (directory/name).write_bytes(value)
        mapping.append({'binding':json.loads(key),'path':name})
    (directory/'record-map.json').write_bytes(raw(mapping))
    (directory/'trusted-pins.json').write_bytes(raw({'contractSha256':contract_hash,'requestSha256':sha(case['request']),'contextSha256':sha(case['context'])}))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', required=True, type=Path)
    parser.add_argument('--package-root', type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    contract_hash = sha((args.package_root/'contract.json').read_bytes())
    cases = []
    for selector in ('digest','revision','mixed'):
        for occupant in ('LOT','MATERIAL'):
            for place in ('CONTAINER','STORAGE_LOCATION','FACILITY'):
                cases.append((f'{selector}-{occupant}-{place}',dict(selector_mode=selector,occupant_kind=occupant,place_kind=place)))
    for variant in ('empty-inventory','unknown-start','unbounded-start','unknown-end','unbounded-end','open-end','interval-query','nanosecond-point','cohort-only','quantity-only','both-unreported','partial','unresolved-extent','invalid','disputed','unknown-validity','unknown-dispute','historical','superseded','unknown-revision','overlapping-repeated'):
        cases.append((variant,dict(variant=variant,selector_mode='mixed')))
    for qualifier in ('ESTIMATED','MINIMUM','MAXIMUM','RANGE_MIDPOINT','LABEL_LIMIT','MACHINE_REPORTED','HUMAN_REPORTED','UNKNOWN'):
        cases.append(('qualifier-'+qualifier,dict(variant='qualifier-'+qualifier)))
    for name, kwargs in cases:
        write_case(args.out/name, make_case(name, **kwargs), contract_hash)
    (args.out/'catalog.json').write_bytes(raw({'fixtureNotice':'Fictional source-owner selections; no production record or source admission is claimed.', 'cases':[n for n,_ in cases]}))

if __name__ == '__main__': main()
