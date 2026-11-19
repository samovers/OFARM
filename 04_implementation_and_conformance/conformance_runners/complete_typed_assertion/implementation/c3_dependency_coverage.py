"""Join actual domain-reader and owner-argument occurrences to the C3 graph.

This is construction accounting over independently checked originals. It does
not provide source/use rules, complete protected-state guards or a payload.
Dependencies are occurrence identities, not a claim that expanding an input
once covers every reader of that input.
"""
from pathlib import Path

from strict_inputs import canonical, digest, pointer, InputError, sha, parse
from owner_input_occurrences import collect as collect_owner_arguments

HERE = Path(__file__).resolve().parent
EDGE_CLASSES = {'SELECTOR_SET': 'CONDITIONAL', 'SELECTED_READ': 'REQUIRED_ORIGINAL_READ',
                'ATTEMPTED_READ': 'REQUIRED_ORIGINAL_READ',
                'PREDICATE_FIELD_READ': 'REQUIRED_ORIGINAL_READ',
                'SOURCE_SHAPE': 'SOURCE_SHAPE', 'COMPARISON': 'COMPARISON_VALUE',
                'APPLICABILITY_GUARD': 'CONDITIONAL'}


def independent_catalog(bound, requirements):
    """Use only matched originals with exact independently derived nominations."""
    nominees = {}
    for row in requirements:
        if (row['id'].startswith('selected-source:') and row['disposition'] == 'PASS'
                or row.get('kind') == 'CANDIDATE_CLAIM_SOURCE_OCCURRENCE'
                and row.get('structuralSelection') == 'PASS'):
            if row.get('selectedBinding') is not None and len(row['inputIds']) == 1:
                nominees.setdefault(canonical(row['selectedBinding']), []).append(row)
    entries = []
    for pin in bound['selection']['originalSelections']:
        iid = pin['inputId']
        if pin['digestMode'] != 'JCS_JSON' or bound['inventoryResults'][iid]['status'] != 'MATCHED':
            continue
        binding = {'ref': pin['ref'], 'digest': pin['wholeJcsDigest']}
        nominated = [row for row in nominees.get(canonical(binding), []) if iid in row['inputIds']]
        if not nominated:
            continue
        mappings = [item for item in bound['selection'].get('sourceSelections', [])
                    if item['binding'] == binding and item['rawSha256'] == pin['rawSha256']
                    and item['valueDigest'] == pin['wholeJcsDigest']
                    and any(row['id'].startswith('selected-source:') for row in nominated)]
        entry = {'id': iid, 'binding': binding, 'record': bound['admittedJson'][iid],
                        'rawSha256': pin['rawSha256'], 'valueDigest': pin['wholeJcsDigest'],
                        'digestMode': 'JCS_JSON', 'byteLength': pin['byteLength'],
                        'claimRoles': [{'role': row['role'], 'pointer': row['origin']['pointer']}
                                       for row in nominated
                                       if row.get('kind') == 'CANDIDATE_CLAIM_SOURCE_OCCURRENCE']}
        if mappings and len({canonical(item) for item in mappings}) == 1:
            # Preserve the actual independently pinned nomination consumed by
            # definition readers. A direct typed reference alone is not this
            # mapping, and no source-admission flag is invented.
            entry['selectorMapping'] = dict(mappings[0])
        entries.append(entry)
    from condition_property_resolution import catalog
    return catalog(entries, bound)


def _checked_operands(bound, operands):
    checked, problems = [], []
    for operand in operands:
        iid, path = operand.get('inputId'), operand.get('pointer')
        if iid not in bound['admittedJson'] or not isinstance(path, str):
            problems.append({'code': 'READER_OPERAND_ORIGINAL_UNAVAILABLE', 'inputId': iid})
            continue
        present = True
        try:
            value = pointer(bound['admittedJson'][iid], path)
        except (InputError, KeyError, TypeError, IndexError, ValueError):
            present = False
        if present != operand.get('present') or present and digest(value) != operand.get('valueDigest'):
            problems.append({'code': 'READER_OPERAND_ORIGINAL_MISMATCH', 'inputId': iid, 'pointer': path})
            continue
        annotation = {}
        if 'annotatedValueDigest' in operand:
            matches = present and operand['annotatedValueDigest'] == digest(value)
            annotation = {'annotatedValueDigest': operand['annotatedValueDigest'],
                          'annotationMatchesOriginal': matches}
            if not matches or operand.get('annotationMatchesOriginal') is not matches:
                problems.append({'code': 'READER_COMPARISON_ANNOTATION_MISMATCH', 'inputId': iid,
                                 'pointer': path})
        checked.append({'inputRole': iid, 'pointer': path, 'present': present,
                        **({'valueDigest': digest(value)} if present else {}), **annotation})
    return checked, problems


def _checked_rule_operands(operands):
    """Recheck named selected package rule fields without source-use admission."""
    if not operands:
        return [], []
    members = {item['path']: item['rawSha256']
               for item in parse((HERE / 'candidate-manifest.json').read_bytes())['members']}
    checked, problems = [], []
    for item in operands:
        path, field = item.get('path'), item.get('pointer')
        if path not in members or not isinstance(field, str):
            problems.append({'code': 'READER_RULE_NOT_IN_SELECTED_PACKAGE', 'path': path})
            continue
        raw = (HERE / path).read_bytes()
        if sha(raw) != members[path] or sha(raw) != item.get('rawSha256'):
            problems.append({'code': 'READER_RULE_ORIGINAL_BYTES_MISMATCH', 'path': path})
            continue
        present = True
        try:
            value = pointer(parse(raw), field)
        except (InputError, KeyError, TypeError, IndexError, ValueError):
            present = False
        if present != item.get('present') or present and digest(value) != item.get('valueDigest'):
            problems.append({'code': 'READER_RULE_FIELD_MISMATCH', 'path': path, 'pointer': field})
            continue
        if 'annotatedValueDigest' in item:
            matches = present and item['annotatedValueDigest'] == digest(value)
            if not matches or item.get('annotationMatchesOriginal') is not matches:
                problems.append({'code': 'READER_RULE_COMPARISON_ANNOTATION_MISMATCH',
                                 'path': path, 'pointer': field})
        checked.append(dict(item))
    return checked, problems


def merge_reader_trace(graph, bound, trace, *, owner_controls=None):
    """Materialize exact trace fields; reject unresolved provenance as incomplete."""
    requirements, uses = graph['requirements'], graph['uses']
    indexes = {pin['inputId']: n for n, pin in enumerate(bound['selection']['originalSelections'])}
    catalog_ids = {entry['id'] for entry in independent_catalog(bound, requirements)}
    errors = list(trace.get('errors', []))
    invocation_ids = set()
    owner_controls = owner_controls or {}
    missing_owner_controls = {}
    for invocation in trace['readerCoverage']:
        rid = invocation['id']
        if rid in invocation_ids:
            raise ValueError('Repeated reader invocation ID.')
        invocation_ids.add(rid)
        parent = invocation.get('parentInvocationId')
        requirements.append({'id': rid, 'kind': 'CANDIDATE_DOMAIN_READER_OCCURRENCE',
            'role': 'ACTUAL_READER_INVOCATION', 'edgeClass': 'CONDITIONAL',
            'origin': {'inputRole': 'CANDIDATE_READER_RULE', 'reader': invocation['reader']},
            'inputIds': [], 'dependsOn': list(dict.fromkeys(
                ([parent] if parent else ['root:effectIntent']) + invocation.get('controlDependencies', []))),
            'findingIds': invocation['findingIds'],
            'disposition': 'NOT_EVALUATED',
            'readerStatus': invocation['status'],
            'diagnostics': [{'code': 'READER_INVOCATION_' + invocation['status']}],
            'qualification': 'Invocation control provenance; actual field/shape comparisons are separate occurrences.'})
    for event in trace['readerOccurrences']:
        kind = event['kind']
        if kind not in EDGE_CLASSES:
            raise ValueError('Unknown domain reader occurrence kind: ' + kind)
        observations, problems = _checked_operands(bound, event.get('operands', []))
        selector_observations, selector_problems = _checked_operands(bound, event.get('selectionOperands', []))
        problems.extend(selector_problems)
        rule_observations, rule_problems = _checked_rule_operands(event.get('ruleOperands', []))
        problems.extend(rule_problems)
        ids = list(dict.fromkeys(v['inputRole'] for v in [*observations, *selector_observations]))
        selected = event.get('inputId') if kind in {'SELECTED_READ', 'PREDICATE_FIELD_READ'} else None
        if selected is not None:
            pin = bound['pinsById'].get(selected)
            if (pin is None or selected not in catalog_ids
                    or bound['inventoryResults'][selected]['status'] != 'MATCHED'
                    or pin['digestMode'] != 'JCS_JSON'
                    or event.get('selectedBinding') != {'ref': pin['ref'], 'digest': pin['wholeJcsDigest']}):
                problems.append({'code': 'READER_SELECTED_ORIGINAL_MISMATCH', 'inputId': selected})
                selected = None
            elif selected not in ids:
                ids.append(selected)
        dependencies = list(dict.fromkeys([event['invocationId'], *event.get('dependsOn', [])]))
        dependencies.extend('selected-original:' + str(indexes[iid]) for iid in ids)
        owner_invocation = event.get('ownerInvocationId')
        if owner_invocation is not None:
            expected = owner_controls.get(owner_invocation)
            expected_digest = digest(expected) if expected is not None else None
            if (event.get('derivedControlValueDigest') != expected_digest
                    or event.get('derivedControlMissing') is not (expected is None)):
                problems.append({'code': 'RECOMPUTED_OWNER_CONTROL_MISMATCH',
                                 'invocationId': owner_invocation})
            owner_dependencies = [row['id'] for row in requirements
                                  if row.get('kind') in {'CANDIDATE_OWNER_INPUT_OCCURRENCE',
                                      'CANDIDATE_OWNER_CONTROL_OCCURRENCE', 'CANDIDATE_OWNER_INVOCATION_GUARD'}
                                  and row.get('origin', {}).get('invocationId') == owner_invocation]
            if not owner_dependencies:
                if owner_invocation not in missing_owner_controls:
                    missing_id = 'missing-owner-control:' + str(len(missing_owner_controls))
                    missing_owner_controls[owner_invocation] = missing_id
                    requirements.append({'id': missing_id, 'kind': 'CANDIDATE_OWNER_CONTROL_OCCURRENCE',
                        'role': 'REQUIRED_OWNER_RESULT_UNAVAILABLE', 'edgeClass': 'SELECTION_GUARD',
                        'origin': {'inputRole': 'DOMAIN_OWNER_CALL_SITE', 'invocationId': owner_invocation},
                        'inputIds': [], 'dependsOn': ['root:effectIntent'], 'findingIds': event['findingIds'],
                        'disposition': 'NOT_EVALUATED',
                        'diagnostics': [{'code': 'NO_ACTUAL_OWNER_INVOCATION'}]})
                owner_dependencies = [missing_owner_controls[owner_invocation]]
            dependencies.extend(owner_dependencies)
        row = {'id': event['id'], 'kind': 'CANDIDATE_DOMAIN_READER_OCCURRENCE',
               'role': kind + ':' + str(event.get('site', event['reader'])),
               'edgeClass': EDGE_CLASSES[kind],
               'origin': ({'inputRole': observations[0]['inputRole'], 'pointer': observations[0]['pointer']}
                          if observations else {'inputRole': 'CANDIDATE_READER_RULE', 'reader': event['reader']}),
               'inputIds': ids, 'dependsOn': list(dict.fromkeys(dependencies)),
               'findingIds': event['findingIds'], 'observations': observations,
               'selectorObservations': selector_observations,
               'ruleObservations': rule_observations,
               'disposition': 'NOT_EVALUATED' if problems else event['disposition'],
               'diagnostics': problems,
               'reader': event['reader'], 'readerInvocationId': event['invocationId'],
               'traceKind': kind,
               'qualification': 'Observed actual reader over exact independent originals; no source admission or protected treatment.'}
        for key in ('selectedBinding', 'schemaId', 'errors', 'fact', 'catalogInputIds',
                    'candidateInputIds', 'observedCardinality', 'requiredCardinality', 'outcome', 'guards',
                    'derivedExpressionResultDigest', 'ownerInvocationId', 'derivedControlValueDigest',
                    'derivedControlMissing', 'schemaRule', 'forwardedComparisonId'):
            if key in event:
                row[key] = event[key]
        if 'provenanceStatus' in event:
            row['provenanceStatus'] = event['provenanceStatus']
        requirements.append(row)
        if selected is not None:
            uses.append({'id': event['id'] + ':use', 'requirementId': event['id'],
                         'inputId': selected, 'classification': ('DOMAIN_SELECTOR_FIELD_INSPECTION'
                             if kind == 'PREDICATE_FIELD_READ' else 'ACTUAL_DOMAIN_READER_ORIGINAL'),
                         'digestMode': 'JCS_JSON',
                         'treatment': {'kind': 'NOT_EVALUATED', 'reason': 'SEPARATE_SOURCE_USE_AND_STORAGE_RULES'}})
        errors.extend(problems)
    graph['actualDomainReaderCoverage'] = {
        'schemaVersion': trace['schemaVersion'], 'readerCoverage': trace['readerCoverage'],
        'occurrenceCount': len(trace['readerOccurrences']), 'errors': errors,
        'scope': 'ACTUAL_INDEPENDENT_READER_TRACE_NOT_SEMANTIC_OR_STORAGE_ACCEPTANCE'}


def occurrence_fixed_point(requirements, uses):
    """Check dependency coverage per occurrence, including repeated input uses."""
    by_id = {row['id']: row for row in requirements}
    if len(by_id) != len(requirements):
        raise ValueError('Duplicate C3 occurrence ID.')
    if len({use['id'] for use in uses}) != len(uses):
        raise ValueError('Duplicate C3 use ID.')
    completed, active, order = set(), set(), []
    def visit(rid):
        if rid not in by_id:
            raise ValueError('Unknown C3 occurrence dependency: ' + rid)
        if rid in active:
            raise ValueError('Cyclic C3 occurrence dependency: ' + rid)
        if rid in completed:
            return
        active.add(rid)
        for parent in by_id[rid]['dependsOn']:
            visit(parent)
        active.remove(rid); completed.add(rid); order.append(rid)
    for rid in by_id:
        visit(rid)
    input_uses = {}
    for use in uses:
        if use['requirementId'] not in by_id or use['inputId'] not in by_id[use['requirementId']]['inputIds']:
            raise ValueError('C3 use does not belong to its requirement input.')
        input_uses.setdefault(use['inputId'], []).append(use['requirementId'])
    return {'status': 'RECORDED_OCCURRENCE_DEPENDENCIES_EXHAUSTED',
            'requirementCount': len(by_id), 'expandedRequirementIds': order,
            'distinctInputUseOccurrences': {iid: list(dict.fromkeys(ids)) for iid, ids in input_uses.items()},
            'qualification': 'Structural fixed point for recorded occurrences; not a claim that uninstrumented reader paths or semantic rules are complete.'}


def collect_projection(graph, bound, selected_action):
    """Use the real projection core's read trace, including stopping guards."""
    from domain_mapping import project_traced
    root = bound['roots']['effectIntent']
    if root['disposition'] != 'PASS':
        graph['projectionReadCoverage'] = {'status': 'NOT_EVALUATED', 'reason': 'ORIGINAL_INTENT_UNAVAILABLE'}
        return
    iid = root['inputId']; original = bound['admittedJson'][iid]
    trace = project_traced(original, selected_action)
    prior = 'root:effectIntent'; ids = []
    for n, read in enumerate(trace['reads']):
        rid = 'projection-read:' + str(n)
        observations, problems = _checked_operands(bound, [{'inputId': iid, **read}])
        graph['requirements'].append({'id': rid, 'kind': 'CANDIDATE_DOMAIN_READER_OCCURRENCE',
            'role': 'ACTUAL_PROJECTION_' + read['kind'], 'edgeClass': 'CONDITIONAL',
            'origin': {'inputRole': iid, 'pointer': read['pointer']}, 'inputIds': [iid],
            'dependsOn': [prior], 'findingIds': ['AR_BODY'], 'observations': observations,
            'disposition': 'NOT_EVALUATED' if problems else 'PASS', 'diagnostics': problems,
            'rule': {'module': 'outer/domain_mapping.py', 'moduleRawSha256': sha((HERE/'outer/domain_mapping.py').read_bytes()),
                     'rule': '_project', 'selectedAction': selected_action},
            'qualification': 'Actual projection input/guard observation; no additional protected source read or semantic adoption.'})
        prior = rid; ids.append(rid)
    graph['projectionReadCoverage'] = {'status': trace['status'], 'requirementIds': ids,
        **({'error': trace['error']} if 'error' in trace else {}),
        'derivedProjectionDigest': digest(trace['projection']) if trace['projection'] is not None else None,
        'qualification': 'Same-core projection trace; returned projection and rendered text are derived outputs, not originals.'}


def owner_replay_inputs(bound, owner_rows, attempts, occupancy, event):
    """Bind real recomputed owner outputs to their independently pinned arguments.

    Owner results are control facts from actual invocation, never original
    observations. No owner-provided JSON is replayed as an original unless its
    exact argument bytes were independently selected and matched.
    """
    aliases, issues = {}, []
    by_invocation = {attempt['invocationId']: attempt for attempt in attempts}
    for row in owner_rows:
        if (row['kind'] != 'CANDIDATE_OWNER_INPUT_OCCURRENCE'
                or row['disposition'] != 'PASS' or row.get('digestMode') != 'JCS_JSON'):
            continue
        invocation = row['origin']['invocationId']; path = row['origin']['argumentPath']
        attempt = by_invocation[invocation]; owner = attempt['owner']; alias = None
        if len(path) == 1 and path[0].endswith('_bytes'):
            alias = invocation + ':' + path[0].removesuffix('_bytes')
        elif owner == 'occupancy' and len(path) == 2 and path[0] == 'records':
            try:
                binding = parse(path[1].encode())
                alias = invocation + ':source:' + digest(binding)
            except (InputError, TypeError, ValueError):
                pass
        if alias is not None:
            iid = row['inputIds'][0]
            aliases[alias] = {'inputId': iid, 'record': bound['admittedJson'][iid]}
    safe_event = None
    if event is not None:
        needed = ('event:envelope', 'event:profile')
        if all(alias in aliases for alias in needed):
            if all(digest(event[field]) == digest(aliases['event:'+field]['record']) for field in ('envelope','profile')):
                safe_event = {**event, 'envelope': aliases['event:envelope']['record'],
                              'profile': aliases['event:profile']['record']}
        if safe_event is None:
            issues.append({'code': 'EVENT_OWNER_REPLAY_ORIGINALS_UNAVAILABLE'})
    safe_occupancy = {}
    for atom_id, checked in (occupancy or {}).items():
        prefix = 'occupancy:' + atom_id
        request = aliases.get(prefix + ':request'); context = aliases.get(prefix + ':context')
        if request is not None and context is not None and digest(checked['request']) == digest(request['record']):
            safe_occupancy[atom_id] = {**checked, 'request': request['record']}
        else:
            issues.append({'code': 'OCCUPANCY_OWNER_REPLAY_ORIGINALS_UNAVAILABLE', 'atomId': atom_id})
    return safe_occupancy, safe_event, aliases, issues


def extend(graph, bound, attempts, original_intent_bytes, selected_action, *, occupancy=None, event=None):
    """Complete known input accounting after actual domain owner invocations."""
    if 'ownerArgumentCoverage' in graph or 'actualDomainReaderCoverage' in graph:
        raise ValueError('C3 additional coverage may only be joined once.')
    owners = collect_owner_arguments(bound, attempts, original_intent_bytes)
    graph['requirements'].extend(owners['requirements']); graph['uses'].extend(owners['uses'])
    graph['ownerArgumentCoverage'] = {'readerCoverage': owners['readerCoverage'],
                                     'qualification': owners['qualification']}
    collect_projection(graph, bound, selected_action)
    safe_occupancy, safe_event, owner_originals, bridge_issues = owner_replay_inputs(
        bound, owners['requirements'], attempts, occupancy, event)
    intent_root = bound['roots']['effectIntent']
    typed_blocked = any(item['code'] == 'TYPED_CLAIM_REFERENCE_DERIVATION_BLOCKED'
                        for item in graph['diagnostics'])
    if intent_root['disposition'] == 'PASS' and not typed_blocked:
        from domain_reader_occurrences import collect
        proposed = bound['roots']['proposedAssertion']
        proposed_id = proposed['inputId'] if proposed['disposition'] == 'PASS' else None
        trace = collect(bound['admittedJson'][intent_root['inputId']],
                        bound['admittedJson'].get(proposed_id), selected_action,
                        independent_catalog(bound, graph['requirements']),
                        {'effectIntent': intent_root['inputId'], 'proposedAssertion': proposed_id},
                        occupancy=safe_occupancy, event=safe_event, owner_originals=owner_originals)
        trace.setdefault('errors', []).extend(bridge_issues)
        controls = {'event': safe_event['report'] if safe_event is not None else None,
                    **{'occupancy:' + atom_id: checked['report'] for atom_id, checked in safe_occupancy.items()}}
        merge_reader_trace(graph, bound, trace, owner_controls=controls)
    else:
        graph['actualDomainReaderCoverage'] = {'readerCoverage': [], 'occurrenceCount': 0,
            'errors': [{'code': 'INDEPENDENT_INTENT_READER_SHAPE_UNAVAILABLE' if typed_blocked
                        else 'INDEPENDENT_INTENT_ROOT_UNAVAILABLE'}],
            'scope': 'ACTUAL_INDEPENDENT_READER_TRACE_NOT_SEMANTIC_OR_STORAGE_ACCEPTANCE'}
    graph['knownOccurrenceFixedPoint'] = occurrence_fixed_point(graph['requirements'], graph['uses'])
    graph['derivation']['knownRequirementCount'] = len(graph['requirements'])
    from closure_graph import _is_immutable_input_requirement, refresh_known_finding_attribution
    if any(row['disposition'] == 'FAIL' and _is_immutable_input_requirement(row) for row in graph['requirements']):
        graph['originalInputDisposition'] = 'FAIL'
    if any(row['disposition'] == 'FAIL' for row in graph['requirements']):
        graph['localDisposition'] = 'FAIL'
    refresh_known_finding_attribution(graph)
    return graph
