"""Reproduce PR57 B1/B2/F1 with coherent original bytes and exact assertions."""
from pathlib import Path
import argparse
import copy
import json

from generate_fixtures import make_case, raw, sha, digest
from verify_occupancy import verify, strict, selector_key, binding_keys

MATCHED = 'MATCHED_SELECTED_OCCUPANCY_EVIDENCE'


def rewrite(case, edit):
    """Author fixture selection, not a production resolver or independent pin source."""
    case = copy.deepcopy(case)
    context, request = strict(case['context']), strict(case['request'])
    facts = [strict(case['records'][selector_key(b)])['facts'] for b in context['episodeBindings']]
    edit(context, facts)
    # All edit cases use revision selectors, whose exact spelling is unchanged.
    request['selection'] = copy.deepcopy(context['selection'])
    request['episodes'] = []
    for binding, fact in zip(context['episodeBindings'], facts):
        key = selector_key(binding)
        record = {'schemaVersion': 'ofarm.material-occupancy-evidence.v0.1', 'facts': fact}
        case['records'][key] = raw(record)
        request['episodes'].append({'binding': binding, 'expectedFacts': copy.deepcopy(fact)})
        entry = next(e for e in context['records'] if selector_key(e['binding']) == key)
        entry.update(bytesSha256=sha(case['records'][key]), valueDigest=digest(record))
    required = set(binding_keys(facts)) | set(binding_keys(context['selection'])) | set(binding_keys(context['ownerIdentity'])) | {selector_key(b) for b in context['episodeBindings']}
    context['records'] = [e for e in context['records'] if selector_key(e['binding']) in required]
    case['records'] = {k: v for k, v in case['records'].items() if k in required}
    case.update(request=raw(request), context=raw(context))
    return case


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--package-root', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--source-root', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    rows = []
    contract_sha = sha((args.package_root / 'contract.json').read_bytes())

    def run(name, case, *, error=None, coverage=None, flags=None, quantity=None, covered=None, query=None):
        report = verify(case['request'], case['context'], case['records'],
                        trusted_pins={'contractSha256': contract_sha, 'contextSha256': sha(case['context']), 'requestSha256': sha(case['request'])},
                        package_root=args.package_root, source_root=args.source_root or args.package_root)
        codes = [e['code'] for e in report['errors']]
        episodes = report['episodes']
        if error:
            ok = report['status'] != MATCHED and error in codes and episodes == []
        else:
            expected = strict(case['request'])['episodes']
            ok = report['status'] == MATCHED and not codes and len(episodes) == len(expected)
            ok = ok and all(e['facts'] == f['expectedFacts'] and e['binding'] == f['binding'] for e, f in zip(episodes, expected))
            ok = ok and report['selection'] == strict(case['context'])['selection']
            ok = ok and report['runtimeAdmission'] == report['actualInventoryCompleteness'] == 'NOT_ESTABLISHED'
            for field, value in [('selectedWindowCoverage', coverage), ('selectedPostureSupportsUnqualifiedClaim', flags), ('quantitySupportsUnqualifiedClaim', quantity), ('coveredApplicability', covered), ('queryIntersection', query)]:
                if value is not None:
                    ok = ok and [e[field] for e in episodes] == value
        rows.append({'name': name, 'pass': ok, 'expectedError': error, 'status': report['status'], 'errors': codes,
                     'coverage': [e['selectedWindowCoverage'] for e in episodes], 'unqualified': [e['selectedPostureSupportsUnqualifiedClaim'] for e in episodes]})
        return report

    # A complete window inventory retains turnover, simultaneous occupants and
    # separated visits by the same occupant in original source order.
    for mode in ('digest', 'revision', 'mixed'):
        for variant, coverage, flags in [
            ('interval-turnover', ['PARTIAL_WINDOW'] * 2, [False] * 2),
            ('interval-turnover-plus-full', ['PARTIAL_WINDOW'] * 2 + ['FULL_WINDOW'], [False, False, True]),
            ('interval-two-visits', ['PARTIAL_WINDOW'] * 2, [False] * 2),
            ('interval-empty', [], []),
        ]:
            case = make_case(variant, selector_mode=mode, variant=variant)
            run('B1/' + mode + '/' + variant, case, coverage=coverage, flags=flags)
    turnover = make_case('turnover', selector_mode='revision', variant='interval-turnover-plus-full')
    for action in ('drop-first', 'retain-full-only', 'reorder', 'duplicate'):
        case = copy.deepcopy(turnover)
        request = strict(case['request'])
        if action == 'drop-first': request['episodes'].pop(0)
        elif action == 'retain-full-only': request['episodes'] = request['episodes'][2:]
        elif action == 'reorder': request['episodes'].reverse()
        else: request['episodes'].append(copy.deepcopy(request['episodes'][0]))
        case['request'] = raw(request)
        run('B1/inventory/' + action, case, error='EPISODE_SET_OR_ORDER_MISMATCH')

    interval = make_case('interval', selector_mode='revision', variant='interval-query')
    def applicability(c, fs, value): fs[0]['applicability'] = value
    # Wide source applicability still produces only the selected covered slice.
    wider = rewrite(interval, lambda c, f: applicability(c, f, {'mode':'INTERVAL','start':'2026-10-01T00:00:00Z','end':'2026-10-21T00:00:00Z','startInclusive':True,'endInclusive':False}))
    run('B1/full-source-window-retained', wider, coverage=['FULL_WINDOW'], flags=[True], covered=[strict(interval['context'])['selection']['applicability']])
    narrow = {'mode':'INTERVAL','start':'2026-10-16T00:00:00Z','end':'2026-10-19T00:00:00Z','startInclusive':True,'endInclusive':False}
    run('B1/query-intersection-distinct-from-support', rewrite(interval, lambda c, f: applicability(c, f, copy.deepcopy(narrow))), coverage=['PARTIAL_WINDOW'], flags=[False], covered=[narrow], query=[strict(interval['context'])['selection']['applicability']])
    for source_included in (False, True):
        for query_included in (False, True):
            for side in ('left', 'right'):
                def touch(c, fs):
                    f = fs[0]
                    c['selection']['applicability']['startInclusive' if side == 'left' else 'endInclusive'] = query_included
                    f['applicability'] = {'mode':'INTERVAL', 'start':'2026-10-14T00:00:00Z' if side == 'left' else '2026-10-20T00:00:00Z', 'end':'2026-10-15T00:00:00Z' if side == 'left' else '2026-10-21T00:00:00Z', 'startInclusive':True if side == 'left' else source_included, 'endInclusive':source_included if side == 'left' else False}
                case = rewrite(interval, touch)
                name = f'B1/touch/{side}/{source_included}/{query_included}'
                if source_included and query_included:
                    at = '2026-10-15T00:00:00Z' if side == 'left' else '2026-10-20T00:00:00Z'
                    run(name, case, coverage=['PARTIAL_WINDOW'], flags=[False], covered=[{'mode':'AS_OF','at':at}])
                else:
                    run(name, case, error='SOURCE_APPLICABILITY_MISMATCH')
    for at in ('2026-10-14T00:00:00Z', '2026-10-20T00:00:00.000000001Z'):
        case = rewrite(interval, lambda c, f, at=at: applicability(c, f, {'mode':'AS_OF','at':at}))
        run('B1/disjoint/' + at, case, error='SOURCE_APPLICABILITY_MISMATCH')
    run('B1/nanosecond-point', make_case('nano', selector_mode='revision', variant='nanosecond-point'), coverage=['FULL_WINDOW'], flags=[True])

    base = make_case('base', selector_mode='revision')
    for endpoint in ('start', 'end'):
        for inclusive in (False, True):
            def point_boundary(c, fs):
                fs[0]['interval'][endpoint] = {'posture':'KNOWN','at':c['selection']['applicability']['at'],'inclusive':inclusive}
            run(f'B1/as-of-membership/{endpoint}/{inclusive}', rewrite(base, point_boundary), error=None if inclusive else ('KNOWN_START_EXCLUDES_SOURCE_APPLICABILITY' if endpoint=='start' else 'KNOWN_END_EXCLUDES_SOURCE_APPLICABILITY'), coverage=['FULL_WINDOW'] if inclusive else None, flags=[True] if inclusive else None)
    for variant in ('base', 'open-end', 'unbounded-end', 'unknown-end', 'empty-inventory'):
        for query_mode in ('AS_OF', 'INTERVAL'):
            case = make_case(variant, selector_mode='revision', variant=variant)
            def future(c, fs):
                c['selection']['applicability'] = {'mode':'AS_OF','at':'2099-01-01T00:00:00Z'} if query_mode=='AS_OF' else {'mode':'INTERVAL','start':'2099-01-01T00:00:00Z','end':'2099-01-02T00:00:00Z','startInclusive':True,'endInclusive':False}
                for f in fs: f['applicability'] = copy.deepcopy(c['selection']['applicability'])
            run(f'B2/future-selection/{variant}/{query_mode}', rewrite(case, future), error='SELECTION_AFTER_CONTEXT')
    for endpoint in ('start', 'end'):
        for opposite in ('KNOWN', 'UNKNOWN', 'UNBOUNDED'):
            def future_boundary(c, fs):
                f = fs[0]
                f['interval'][endpoint] = {'posture':'KNOWN','at':'2099-01-01T00:00:00Z','inclusive':True}
                if opposite != 'KNOWN':
                    f['interval']['end' if endpoint=='start' else 'start'] = {'posture':opposite,'basis':copy.deepcopy(f['sourceEvidence'][0])}
            run(f'B2/future-known/{endpoint}/{opposite}', rewrite(base, future_boundary), error='KNOWN_BOUNDARY_AFTER_CONTEXT')
    def future_source(c, fs):
        fs[0]['applicability'] = {'mode':'INTERVAL','start':'2026-10-20T00:00:00Z','end':'2026-10-21T00:00:00.000000001Z','startInclusive':True,'endInclusive':False}
    run('B2/source-one-nanosecond-after-context', rewrite(base, future_source), error='SOURCE_APPLICABILITY_AFTER_CONTEXT')
    for target, code in [('selection','SELECTION_AFTER_CONTEXT'),('assessment','POSTURE_AFTER_CONTEXT'),('open','OPEN_POSTURE_AFTER_CONTEXT'),('known','KNOWN_BOUNDARY_AFTER_CONTEXT')]:
        def future_nano(c, fs):
            after = '2026-10-21T00:00:00.000000001Z'
            if target=='selection': c['selection']['applicability']['at'] = after
            elif target=='assessment': fs[0]['sourcePosture']['assessedAt'] = after
            elif target=='known': fs[0]['interval']['end']['at'] = after
            else: fs[0]['interval']['end'] = {'posture':'OPEN_AS_OF','asOf':after,'basis':copy.deepcopy(fs[0]['sourceEvidence'][0])}
        run('B2/nanosecond-horizon/' + target, rewrite(base, future_nano), error=code)
    for variant in ('unknown-start','unknown-end','unbounded-start','unbounded-end'):
        run('B2/no-infinite-coverage/' + variant, make_case(variant, selector_mode='revision', variant=variant), coverage=['UNRESOLVED'], flags=[False], covered=[None])
    run('B2/finite-open-observation', make_case('open', selector_mode='revision', variant='open-end'), coverage=['FULL_WINDOW'], flags=[True])
    for posture in ('UNKNOWN','UNBOUNDED'):
        def contradiction(c, fs):
            f = fs[0]
            f['interval']['start']['at'] = '2026-10-21T00:00:00Z'
            f['interval']['end'] = {'posture':posture,'basis':copy.deepcopy(f['sourceEvidence'][0])}
        run('B2/known-contradiction-with-' + posture, rewrite(base, contradiction), error='KNOWN_START_EXCLUDES_SOURCE_APPLICABILITY')
    def at_horizon(c, fs):
        f = fs[0]
        c['selection']['applicability'] = {'mode':'AS_OF','at':c['fixedAt']}
        f['applicability'] = copy.deepcopy(c['selection']['applicability'])
        f['interval']['end']['inclusive'] = True
    run('B2/exact-context-boundary', rewrite(base, at_horizon), coverage=['FULL_WINDOW'], flags=[True])
    def bad_later_episode(c, fs): fs[-1]['interval']['end']['at'] = '2099-01-01T00:00:00Z'
    run('B2/no-partial-output-on-later-failure', rewrite(turnover, bad_later_episode), error='KNOWN_BOUNDARY_AFTER_CONTEXT')

    for qualifier in ('EXACT','ESTIMATED','MINIMUM','MAXIMUM','RANGE_MIDPOINT','LABEL_LIMIT','MACHINE_REPORTED','HUMAN_REPORTED','UNKNOWN'):
        for has_cohort in (False, True):
            def qualified(c, fs):
                fs[0]['occupiedQuantity']['qualifier'] = qualifier
                if not has_cohort: fs[0]['occupiedCohort'] = {'posture':'UNREPORTED','reason':'Fictional quantity-only source.'}
            run(f'F1/qualifier/{qualifier}/cohort-{has_cohort}', rewrite(base, qualified), quantity=[qualifier=='EXACT'], flags=[qualifier=='EXACT'])
    run('F1/cohort-only-no-quantity-claim', make_case('cohort', selector_mode='revision', variant='cohort-only'), quantity=[False], flags=[True])
    run('F1/neither-reported', make_case('neither', selector_mode='revision', variant='both-unreported'), quantity=[False], flags=[False])

    result = {'status':'PASS' if all(r['pass'] for r in rows) else 'FAIL', 'contractSha256':contract_sha,
              'primaryTrustBoundary':'Material occupancy source evidence', 'scopeStayedInsideBoundary':True,
              'findings':['B1','B2','F1'], 'checks':len(rows), 'passed':sum(r['pass'] for r in rows),
              'failed':[r for r in rows if not r['pass']], 'results':rows}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_bytes(raw(result))
    print(json.dumps({k:v for k,v in result.items() if k!='results'}, indent=2))
    return 0 if result['status']=='PASS' else 1


if __name__ == '__main__': raise SystemExit(main())
