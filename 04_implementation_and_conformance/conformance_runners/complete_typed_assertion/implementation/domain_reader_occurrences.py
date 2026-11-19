"""Construction-only observations at actual domain reader selection seams.

These hooks observe existing selectors; they do not select sources, admit uses,
or alter the ordinary reader result. Only the independent C3 replay enables
recording. Source-selection sets and selected reads remain different events.
"""
from contextvars import ContextVar
from functools import wraps
from copy import deepcopy

from strict_inputs import digest, pointer, InputError, sha, parse
from pathlib import Path
import sys

_ACTIVE = ContextVar('domain_reader_occurrences', default=None)


def origin(role, path):
    return {'inputRole': role, 'pointer': path}


def _event(kind, **fields):
    active = _ACTIVE.get()
    if active is None or not active['stack']:
        return None
    invocation = active['stack'][-1]
    row = {'id': 'reader-occurrence:' + str(len(active['events'])),
           'kind': kind, 'reader': invocation['reader'],
           'invocationId': invocation['id'],
           'findingIds': invocation['findingIds'], **deepcopy(fields)}
    row['dependsOn'] = list(dict.fromkeys([invocation['id']] + invocation.get('controlDependencies', []) + row.get('dependsOn', [])))
    active['events'].append(row)
    active.setdefault('eventScopes', {})[row['id']] = (invocation['id'], deepcopy(invocation.get('selectorScope')))
    return row['id']


def register_result_dependencies(result, role, event_ids):
    """Retain actual producer events on an unchanged, held internal result."""
    active = _ACTIVE.get()
    if active is None:
        return
    if not active['stack'] or not isinstance(result, dict):
        raise ValueError('Result dependencies require an active dictionary producer.')
    invocation = active['stack'][-1]
    scope = invocation.get('selectorScope')
    ids = tuple(dict.fromkeys(event_ids))
    if not ids or any(active.get('eventScopes', {}).get(event_id) != (invocation['id'], scope) for event_id in ids):
        raise ValueError('Result dependency is not an emitted event of this producer scope.')
    registry = active.setdefault('resultDependencies', {})
    key = (id(result), role)
    if key in registry:
        raise ValueError('Result dependency role is already registered.')
    registry[key] = {'object': result, 'invocation': invocation, 'scope': deepcopy(scope), 'eventIds': ids}


def result_dependencies(result, role, *, producer, scope=None):
    """Read only this collection's exact completed producer result and role."""
    active = _ACTIVE.get()
    if active is None or not active['stack']:
        return []
    saved = active.get('resultDependencies', {}).get((id(result), role))
    if saved is None or saved['object'] is not result or saved['scope'] != scope:
        return []
    invocation = saved['invocation']
    if (invocation['reader'] != producer or invocation['status'] != 'RETURNED'
            or any(item is invocation for item in active['stack'])):
        return []
    return list(saved['eventIds'])


def _operands(items):
    active = _ACTIVE.get()
    if active is None:
        return []
    result = []
    for item in items:
        role, path = item['inputRole'], item['pointer']
        if role == 'DOMAIN_DEFINITIONS' or role.startswith('PINNED_CANONICAL_SOURCE:'):
            continue
        if role.startswith('ATOM:'):
            atom_path = active['atoms'].get(role[5:])
            if atom_path is not None:
                path = atom_path + path
                role = 'EFFECT_INTENT'
        iid = active['roots'].get(role, role)
        if iid is None:
            continue
        value = active['documents'].get(iid)
        present = iid in active['documents']
        if present:
            try:
                selected = pointer(value, path)
            except (InputError, ValueError, KeyError, IndexError, TypeError):
                present = False
        observed = {'inputId': iid, 'pointer': path, 'present': present,
                    **({'valueDigest': digest(selected)} if present else {})}
        if 'valueDigest' in item:
            observed['annotatedValueDigest'] = item['valueDigest']
            observed['annotationMatchesOriginal'] = present and observed['valueDigest'] == item['valueDigest']
        result.append(observed)
    return result


def _dependencies(operands, explicit=()):
    """Connect only actual selector operands and their already observed guards."""
    active = _ACTIVE.get()
    if active is None:
        return []
    found = list(explicit)
    ancestors = {active['stack'][-1]['id']} if active['stack'] else set()
    for operand in operands:
        iid, path = operand['inputId'], operand['pointer']
        reads = [v for v in active['events'] if v['kind'] == 'SELECTED_READ' and v.get('inputId') == iid
                 and v['invocationId'] in ancestors]
        if reads:
            found.append(reads[-1]['id'])
        for previous in reversed(active['events']):
            if previous['invocationId'] not in ancestors or previous['kind'] != 'SOURCE_SHAPE':
                continue
            if any(consumed['inputId'] == iid and (not consumed['pointer'] or path == consumed['pointer']
                   or path.startswith(consumed['pointer'] + '/') or consumed['pointer'].startswith(path + '/'))
                   for consumed in previous.get('operands', [])):
                found.append(previous['id'])
                break
    return list(dict.fromkeys(found))


def branch(site, value, *, origins=(), depends_on=()):
    """Observe a Boolean already computed by the existing if statement."""
    guard_id = guard(site, value, origins=origins, depends_on=depends_on)
    active = _ACTIVE.get()
    if active is not None and active['stack']:
        active['stack'][-1].setdefault('guards', {})[site] = guard_id
    return value


def guard_refs(*sites):
    active = _ACTIVE.get()
    if active is None or not active['stack']:
        return []
    guards = active['stack'][-1].get('guards', {})
    return [guards[site] for site in sites if site in guards]


def selector_scope(value):
    active = _ACTIVE.get()
    if active is not None and active['stack']:
        active['stack'][-1]['selectorScope'] = value


def predicate_value(entry, path, value, site, *, depends_on=()):
    """Observe a field expression at the exact point it actually executes."""
    if _ACTIVE.get() is None:
        return value
    active = _ACTIVE.get()
    invocation = active['stack'][-1]
    operands = _operands([origin(entry['id'], path)])
    _event('PREDICATE_FIELD_READ', site=site, inputId=entry['id'],
           selectedBinding=entry['binding'], digestMode=entry.get('digestMode', 'JCS_JSON'),
           rawSha256=entry.get('rawSha256'), valueDigest=entry.get('valueDigest'),
           operands=operands, disposition='PASS', dependsOn=_dependencies(operands, depends_on),
           selectorScope=invocation.get('selectorScope'),
           derivedExpressionResultDigest=digest(value))
    return value


def _predicate_dependencies(site, additional_sites=()):
    active = _ACTIVE.get()
    if active is None or not active['stack']:
        return []
    invocation = active['stack'][-1]
    names = {site, *additional_sites}
    return [e['id'] for e in active['events'] if e['kind'] == 'PREDICATE_FIELD_READ'
            and e['invocationId'] == invocation['id'] and e['site'] in names
            and e.get('selectorScope') in (None, invocation.get('selectorScope'))]


def selection(site, pool, selected, *, binding=None, origins=(), guards=(), findings=None, predicate_sites=()):
    """Observe the exact candidates already computed by an actual selector.

    The catalog is an input to the selection predicate, not a declaration that
    every catalog member is a positive source read. Empty/ambiguous sets retain
    the attempted selector and its original operands.
    """
    if _ACTIVE.get() is None:
        return None
    candidates = [v[0] if isinstance(v, tuple) else v for v in selected]
    operands = _operands(origins)
    set_id = _event('SELECTOR_SET', site=site,
        dependsOn=_dependencies(operands, list(guards) + _predicate_dependencies(site, predicate_sites)),
        catalogInputIds=[v['id'] for v in pool],
        candidateInputIds=[v['id'] for v in candidates],
        operands=operands, selectedBinding=binding,
        selectionOperands=[],
        requiredCardinality=1, observedCardinality=len(candidates),
        disposition='PASS' if len(candidates) == 1 else 'NOT_EVALUATED',
        guards=list(guards), **({'findingIds': list(findings)} if findings is not None else {}))
    if len(candidates) == 1:
        item = candidates[0]
        return _event('SELECTED_READ', site=site, inputId=item['id'],
            selectedBinding=item['binding'], digestMode=item.get('digestMode', 'JCS_JSON'),
            rawSha256=item.get('rawSha256'), valueDigest=item.get('valueDigest'),
            operands=_operands(origins), dependsOn=[set_id], disposition='PASS',
            **({'findingIds': list(findings)} if findings is not None else {}))
    if binding is not None:
        return _event('ATTEMPTED_READ', site=site, inputId=None,
            selectedBinding=binding, digestMode='JCS_JSON', operands=operands,
            dependsOn=[set_id], disposition='NOT_EVALUATED',
            reason='EXACT_ORIGINAL_MISSING' if not candidates else 'EXACT_ORIGINAL_AMBIGUOUS',
            **({'findingIds': list(findings)} if findings is not None else {}))
    return set_id


def guard(site, value, *, origins=(), depends_on=(), predicate_sites=()):
    operands = _operands(origins)
    return _event('APPLICABILITY_GUARD', site=site, outcome=bool(value),
                  operands=operands, dependsOn=_dependencies(operands,
                      list(depends_on) + (_predicate_dependencies(site, predicate_sites) if predicate_sites else [])),
                  disposition='PASS')


def shape(site, entry, schema_id, errors, *, depends_on=()):
    return _event('SOURCE_SHAPE', site=site, inputId=entry['id'],
                  schemaId=schema_id, errors=errors,
                  operands=_operands([origin(entry['id'], '')]),
                  dependsOn=list(depends_on),
                  disposition='FAIL' if errors else 'PASS')


def _schema_rule(schemas, schema_id):
    active = _ACTIVE.get()
    if active is None:
        return None
    value = schemas.schemas.get(schema_id)
    if value is None:
        return {'schemaId': schema_id, 'status': 'UNAVAILABLE'}
    providers = ('definition_inputs', 'work_definition_inputs', 'event_definition_inputs',
        'analysis_output_definitions', 'sample_collection_definitions',
        'observation_acquisition_definitions', 'drying_definitions',
        'irrigation_definitions', 'sanitation_definitions')
    for name in providers:
        module = sys.modules.get(name)
        if module is not None and any(item is value for item in getattr(module, 'SCHEMAS', {}).values()):
            path = Path(module.__file__)
            return {'schemaId': schema_id, 'schemaValueDigest': digest(value),
                    'status': 'GENERATED_BY_PINNED_DOMAIN_CODE',
                    'providerCode': {'path': path.name, 'rawSha256': sha(path.read_bytes())}}
    cache = active.setdefault('schemaRuleFiles', {})
    if not cache:
        root = Path(__file__).resolve().parent
        manifest = parse((root / 'candidate-manifest.json').read_bytes())
        for member in manifest['members']:
            if not member['path'].endswith('.json'):
                continue
            raw = (root / member['path']).read_bytes()
            try:
                candidate = parse(raw)
            except ValueError:
                continue
            if isinstance(candidate, dict) and candidate.get('$id'):
                cache.setdefault(candidate['$id'], []).append((member['path'], raw, candidate))
    for relative, raw, candidate in cache.get(schema_id, []):
        if candidate == value:
            return {'schemaId': schema_id, 'schemaValueDigest': digest(value),
                    'status': 'PINNED_JSON_SCHEMA',
                    'ruleOperand': {'path': relative, 'pointer': '', 'rawSha256': sha(raw),
                                    'present': True, 'valueDigest': digest(candidate)}}
    return {'schemaId': schema_id, 'schemaValueDigest': digest(value),
            'status': 'REGISTERED_SCHEMA_PROVIDER_UNRESOLVED'}


def owner_control(site, invocation_id, report, outcome, *, activate=False):
    """A real recomputed owner result is a derived control, never an original."""
    guard_id = _event('APPLICABILITY_GUARD', site=site, ownerInvocationId=invocation_id,
        derivedControlValueDigest=digest(report) if report is not None else None,
        derivedControlMissing=report is None, outcome=bool(outcome), operands=[],
        disposition='PASS' if report is not None else 'NOT_EVALUATED')
    active = _ACTIVE.get()
    if activate and active is not None and active['stack'] and guard_id is not None:
        active['stack'][-1].setdefault('controlDependencies', []).append(guard_id)
    return guard_id


def observed_shape(schemas, schema_id, record):
    """Call the existing schema checker exactly once and observe its operand."""
    errors = schemas.errors(schema_id, record)
    active = _ACTIVE.get()
    if active is not None and active['stack']:
        ids = [iid for iid, original in active['documents'].items() if original is record]
        prior = [e for e in active['events'] if e['kind'] == 'SELECTED_READ'
                 and e.get('inputId') in ids
                 and e['invocationId'] == active['stack'][-1]['id']]
        schema_rule = _schema_rule(schemas, schema_id)
        _event('SOURCE_SHAPE', site=schema_id, inputIds=ids, schemaRule=schema_rule,
               ruleOperands=[schema_rule['ruleOperand']] if schema_rule and 'ruleOperand' in schema_rule else [],
               operands=_operands([origin(iid, '') for iid in ids]),
               schemaId=schema_id, errors=errors,
               dependsOn=[prior[-1]['id']] if prior else [],
               disposition='FAIL' if errors else 'PASS',
               **({'findingIds': prior[-1]['findingIds']} if prior else {}))
    return errors


def _rule_operands(operands):
    result = []
    root = Path(__file__).resolve().parent
    for operand in operands:
        role = operand['inputRole']
        if role == 'DOMAIN_DEFINITIONS':
            relative = 'domain-definitions.json'
        elif role.startswith('PINNED_CANONICAL_SOURCE:'):
            local = role.split(':', 1)[1]
            pins = parse((root / 'components/revision-02/source-pins.json').read_bytes())['sources']
            matches = [pin for pin in pins if pin['localPath'] == local]
            if len(matches) != 1:
                continue
            relative = 'components/revision-02/' + local
            path = (root / relative).resolve()
            if not path.is_relative_to(root.resolve()) or sha(path.read_bytes()) != matches[0]['sha256']:
                continue
        else:
            continue
        raw = (root / relative).read_bytes()
        value = parse(raw)
        try:
            selected = pointer(value, operand['pointer'])
        except (InputError, ValueError, KeyError, IndexError, TypeError):
            result.append({'path': relative, 'pointer': operand['pointer'],
                           'rawSha256': sha(raw), 'present': False,
                           **({'annotatedValueDigest': operand['valueDigest'], 'annotationMatchesOriginal': False}
                              if 'valueDigest' in operand else {})})
        else:
            result.append({'path': relative, 'pointer': operand['pointer'],
                           'rawSha256': sha(raw), 'present': True, 'valueDigest': digest(selected),
                           **({'annotatedValueDigest': operand['valueDigest'],
                               'annotationMatchesOriginal': operand['valueDigest'] == digest(selected)}
                              if 'valueDigest' in operand else {})})
    return result


def schema_selection(source, candidates):
    """Observe existing pinned schema choice; this creates no source admission."""
    rules = []
    for schema_id, hashes in candidates:
        for raw_sha, paths in hashes.items():
            for path, value in paths:
                rules.append({'path': path, 'pointer': '/properties/schemaVersion/const',
                    'rawSha256': raw_sha, 'present': True,
                    'valueDigest': digest(value['properties']['schemaVersion']['const'])})
    operands = _operands([origin(source['id'], '/schemaVersion' if isinstance(source['record'], dict) else '')])
    role_findings = {'ASSERTION_EVIDENCE': 'AR_EVIDENCE', 'RULE_REVISION': 'AR_COMPLIANCE_RULES',
                     'EVIDENCE_POLICY_REVISION': 'AR_COMPLIANCE_EVIDENCE_POLICY'}
    findings = sorted({role_findings[v['role']] for v in source.get('claimRoles', []) if v['role'] in role_findings})
    selected = len(candidates) == 1 and len(candidates[0][1]) == 1
    set_id = _event('SELECTOR_SET', site='SOURCE_SCHEMA_SELECTION', findingIds=findings,
        operands=operands, ruleOperands=rules, dependsOn=_dependencies(operands, _predicate_dependencies('SOURCE_SCHEMA_SELECTION')),
        catalogInputIds=[source['id']], candidateInputIds=[],
        requiredCardinality=1, observedCardinality=len(candidates),
        schemaCandidateIds=[sid for sid, _ in candidates],
        disposition='PASS' if selected else 'NOT_EVALUATED')
    if selected:
        _event('SELECTED_READ', site='SOURCE_SCHEMA_ORIGINAL', findingIds=findings,
            inputId=source['id'], selectedBinding=source['binding'],
            digestMode=source.get('digestMode', 'JCS_JSON'), rawSha256=source['rawSha256'],
            valueDigest=source['valueDigest'], operands=operands, dependsOn=[set_id], disposition='PASS')
    return set_id


def observe_comparisons(comparisons, *, findings=None, depends_on=()):
    """Observe original operands and return IDs for explicit derived dependencies."""
    active = _ACTIVE.get()
    if active is None or not active['stack']:
        return []
    event_ids = []
    for comparison in comparisons:
        if active is not None and active['stack']:
            observed = active['stack'][-1].setdefault('_observedComparisons', [])
            if any(previous is comparison for previous in observed):
                prior = active.get('comparisonEvents', {}).get(id(comparison))
                if prior is not None and prior[0] is comparison:
                    event_ids.append(prior[1])
                continue
            observed.append(comparison)
        previous = active.setdefault('comparisonEvents', {}).get(id(comparison))
        if previous is not None and previous[0] is comparison:
            event_id = _event('COMPARISON', site=comparison.get('predicateId'), operands=[], ruleOperands=[],
                dependsOn=[previous[1], *depends_on], forwardedComparisonId=previous[1],
                disposition=previous[2], provenanceStatus='FORWARDED_ACTUAL_READER_COMPARISON',
                fact=comparison, **({'findingIds': findings} if findings is not None else {}))
            event_ids.append(event_id)
            continue
        operands = comparison.get('operandAvailability', comparison)
        if not isinstance(operands, dict):
            continue
        originals = [operands[k] for k in ('source', 'destination')
                     if isinstance(operands.get(k), dict)
                     and 'inputRole' in operands[k] and 'pointer' in operands[k]]
        original_operands = _operands(originals)
        rule_operands = _rule_operands(originals)
        contradicted = any(v.get('annotationMatchesOriginal') is False
                           for v in original_operands + rule_operands)
        event_id = _event('COMPARISON', site=comparison.get('predicateId'),
               operands=original_operands, ruleOperands=rule_operands,
               dependsOn=_dependencies(original_operands, depends_on),
               disposition='NOT_EVALUATED' if contradicted else comparison.get('disposition', 'NOT_EVALUATED'),
               provenanceStatus='ANNOTATED_ORIGINAL_VALUE_MISMATCH' if contradicted else 'OBSERVED',
               fact=comparison,
               **({'findingIds': findings} if findings is not None else {}))
        active['comparisonEvents'][id(comparison)] = (comparison, event_id,
            'NOT_EVALUATED' if contradicted else comparison.get('disposition', 'NOT_EVALUATED'))
        event_ids.append(event_id)
    return event_ids


def reader(name, findings):
    """Fixed internal annotation; no caller-supplied predicate or selector."""
    def decorate(function):
        @wraps(function)
        def call(*args, **kwargs):
            active = _ACTIVE.get()
            if active is None:
                return function(*args, **kwargs)
            entry_controls = list(active['stack'][-1].get('controlDependencies', [])) if active['stack'] else []
            invocation = {'id': 'reader-invocation:' + str(len(active['invocations'])),
                          'reader': name, 'findingIds': list(findings),
                          'parentInvocationId': active['stack'][-1]['id'] if active['stack'] else None,
                          'status': 'RUNNING',
                          'controlDependencies': list(entry_controls)}
            active['invocations'].append(invocation)
            active['stack'].append(invocation)
            try:
                result = function(*args, **kwargs)
                invocation['status'] = 'RETURNED'
                if isinstance(result, dict):
                    invocation['disposition'] = result.get('disposition')
                    invocation['remainingRoles'] = deepcopy(result.get('remainingRoles', []))
                    invocation['errors'] = deepcopy(result.get('errors', []))
                    invocation['sourceInputIds'] = deepcopy(result.get('sourceInputIds', []))
                    observe_comparisons(result.get('comparisons', []))
                    sections = {'SUBJECT_SCOPE_RELATION': ['AR_SUBJECT_SCOPE_PROOF'],
                        'PERFORMER_IDENTITY': ['AR_OPERATION_PERFORMER'],
                        'COMPLIANCE_RULE_SELECTION': ['AR_COMPLIANCE_RULES'],
                        'EVIDENCE_POLICY_SELECTION': ['AR_COMPLIANCE_EVIDENCE_POLICY']}
                    for section, finding_ids in sections.items():
                        if isinstance(result.get(section), dict):
                            observe_comparisons(result[section].get('comparisons', []), findings=finding_ids)
                invocation.pop('_observedComparisons', None)
                return result
            except Exception as exc:
                invocation.pop('_observedComparisons', None)
                invocation.update(status='READER_ERROR', errorType=type(exc).__name__, detail=str(exc))
                raise
            finally:
                # Guards activated during this call govern later events and
                # child calls; they cannot retroactively govern this entry.
                invocation['controlDependencies'] = entry_controls
                active['stack'].pop()
        return call
    return decorate


def collect(intent, result, action, catalog, root_input_ids, *, occupancy=None, event=None, owner_originals=None):
    """Replay fixed readers over independent matched originals only.

    The caller supplies bind_roots-admitted documents and a catalog built from
    the independent selection, never from an offered protected-read list.
    There is no protected-context digest or source-admission result here.
    """
    from component_calls import evaluate_reader_components
    atoms = {}
    def walk(node, path):
        if node.get('form') == 'ATOM':
            atoms[node['atomId']] = path
        elif 'child' in node:
            walk(node['child'], path + '/child')
        else:
            for n, child in enumerate(node.get('children', [])):
                walk(child, path + '/children/' + str(n))
    walk(intent['assertionBody']['proposition'], '/assertionBody/proposition')
    roots = {'EFFECT_INTENT': root_input_ids.get('EFFECT_INTENT', root_input_ids.get('effectIntent')),
             'PROPOSED_ASSERTION': root_input_ids.get('PROPOSED_ASSERTION', root_input_ids.get('proposedAssertion'))}
    documents = {v['id']: v['record'] for v in catalog}
    documents.update({iid: value for iid, value in ((roots['EFFECT_INTENT'], intent),
        (roots['PROPOSED_ASSERTION'], result)) if iid is not None and value is not None})
    for alias, original in (owner_originals or {}).items():
        # The caller has already matched these actual invocation argument bytes
        # to independent JCS pins. They are operand aliases, not nominations.
        roots[alias] = original['inputId']
        documents[original['inputId']] = original['record']
    active = {'events': [], 'invocations': [], 'stack': [], 'atoms': atoms,
              'roots': roots, 'documents': documents}
    token = _ACTIVE.set(active)
    errors = []
    try:
        replay = evaluate_reader_components(intent, catalog, action, occupancy=occupancy, event=event)
        if replay.get('intentErrors'):
            errors.append({'code': 'DOMAIN_READER_INTENT_SCHEMA_BLOCKED', 'errors': replay['intentErrors']})
        if replay.get('intrinsics', {}).get('errors'):
            errors.append({'code': 'DOMAIN_READER_INTRINSIC_DISPATCH_BLOCKED', 'errors': replay['intrinsics']['errors']})
    except Exception as exc:
        errors.append({'code': 'DOMAIN_READER_REPLAY_INCOMPLETE',
                       'errorType': type(exc).__name__, 'detail': str(exc)})
    finally:
        _ACTIVE.reset(token)
    return {'schemaVersion': 'candidate.domainReaderOccurrences.v0.1',
            'scope': 'INDEPENDENT_CATALOG_READ_OBSERVATIONS_NOT_SOURCE_ADMISSION',
            'readerOccurrences': active['events'], 'readerCoverage': active['invocations'],
            'errors': errors}
