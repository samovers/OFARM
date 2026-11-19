"""Public construction entry point for original intent/result bytes.

This is continuing construction, not a complete verifier or runtime gate. It
executes independent owned predicates and concrete owner checkers and retains
all 49 duties. Unclosed owner/source interfaces prevent a completed payload.
No supplied report, admission Boolean or later receipt can satisfy a gate.
"""
from pathlib import Path
import importlib.metadata
import json

from strict_inputs import InputError, parse, sha, digest, same, pointer, verify_pins
from contract_refs import verify_references
from duty_graph import PREREQUISITES, OWNER_DEPENDENCIES, validate_graph
from report_contract import REPORT_SCHEMA
import component_calls
import owner_calls
import payload_builder
import input_manifest
import payload_inputs
import authorization_sources
import closure_graph
import protected_identity_provenance
import protected_known_write

HERE = Path(__file__).resolve().parent
ACTIONS = {'ASSERT_STRUCTURE', 'ASSERT_OPERATION_CLAIM', 'ASSERT_COMPLIANCE'}


def diagnostic(code, detail, path=''):
    return {'code': code, 'pointer': path, 'detail': str(detail)[:4000]}


def _present(value, path):
    try:
        return True, pointer(value, path)
    except InputError:
        return False, None


def _required_original_row(row):
    """Only established original reads may fail immutable-input closure."""
    return closure_graph._is_immutable_input_requirement(row)


def _invocation_summary(value):
    """Keep exact transport identities without repeating megabytes of bytes.

    The parsed owner report has one explicit home in ownerReports. Its worker
    stdout and generated report serialization remain hash/length bound here.
    The original direct owner invocation can be archived separately by the
    caller when exact transport bytes are needed for audit replay.
    """
    def compact(item):
        if isinstance(item, dict):
            return {key: compact(member) for key, member in item.items()
                    if key not in ('originalBytesBase64', 'ownerReport', 'domainReport')}
        if isinstance(item, list):
            return [compact(member) for member in item]
        return item
    return compact(value)


def _link_observed_invocation_selections(graph, observations, linked):
    """Connect an actual invocation to its already executed claim selectors."""
    for event in observations:
        for invocation in event.get('selectsOwnerInvocations', []):
            for row in graph['requirements']:
                if (row.get('kind') == 'CANDIDATE_OWNER_INVOCATION_GUARD'
                        and row['origin']['invocationId'] == invocation):
                    row['dependsOn'] = list(dict.fromkeys([*row['dependsOn'], linked[event['id']]]))


def _preserve_interrupted_callsite_prefix(graph, bound, attempts, original_intent_bytes,
                                        queues, selected_action):
    """Keep already executed call sites when a later local guard aborts.

    This does not replay any source reader or infer an invocation after the
    exception. The ordinary input error and unfinished findings stay unchanged.
    """
    from owner_input_occurrences import collect as collect_owner_arguments
    from c3_dependency_coverage import occurrence_fixed_point
    if 'ownerArgumentCoverage' not in graph:
        owners = collect_owner_arguments(bound, attempts, original_intent_bytes)
        graph['requirements'].extend(owners['requirements'])
        graph['uses'].extend(owners['uses'])
        graph['ownerArgumentCoverage'] = {'readerCoverage': owners['readerCoverage'],
                                         'qualification': owners['qualification']}
    for observations in queues:
        if not any(row.get('observedEventId') in {event['id'] for event in observations}
                   for row in graph['requirements']):
            linked = closure_graph.materialize_local_observations(
                graph, bound, observations, selected_action=selected_action)
            _link_observed_invocation_selections(graph, observations, linked)
    graph['actualCallSitePrefix'] = {
        'status': 'INTERRUPTED_ACTUAL_PREFIX_ONLY',
        'observedInvocationIds': [attempt['invocationId'] for attempt in attempts],
        'observedEventIds': [event['id'] for queue in queues for event in queue],
        'laterReaderReplayAttempted': False,
        'findingEvaluationComplete': False}
    graph['derivation']['knownRequirementCount'] = len(graph['requirements'])
    graph['knownOccurrenceFixedPoint'] = occurrence_fixed_point(graph['requirements'], graph['uses'])
    closure_graph.refresh_known_finding_attribution(graph)


def verify_domain(original_intent_bytes, original_result_bytes, *, package, owner_inputs):
    report = {'schemaVersion': 'ofarm.domainConstructionEvaluation.v0.1',
              'status': 'INPUT_ERROR', 'implementationCompleteness': 'INCOMPLETE',
              'runtimeAdmission': 'NOT_ESTABLISHED', 'atomicCommit': 'NOT_EVALUATED',
              'primaryTrustBoundary': 'AssertionRecord domain meaning and validation integrity',
              'scopeStayedInsideBoundary': True, 'inputBindings': {}, 'errors': [],
              'ownerReports': {}, 'ownerInvocations': {}, 'componentReports': [], 'dependencyFindings': [],
              'mappingFindings': [], 'postconditionFindings': [], 'payload': None}
    try:
        if not isinstance(package, dict) or not {'root', 'manifestRawSha256', 'selectedAction'} <= set(package) or set(package) - {'root', 'manifestRawSha256', 'selectedAction', 'evaluationSelectionRawSha256'}:
            raise InputError('package requires root, manifestRawSha256, independent selectedAction and optional evaluationSelectionRawSha256.')
        if Path(package['root']).resolve() != HERE or package['selectedAction'] not in ACTIONS:
            raise InputError('Select this exact pinned checker directory and a supported action.')
        for name, version in [('rfc8785', '0.1.4'), ('jsonschema', '4.26.0')]:
            if importlib.metadata.version(name) != version:
                raise InputError('Required dependency: ' + name + '==' + version)
        manifest = verify_pins(HERE, (HERE / 'candidate-manifest.json').read_bytes(), package['manifestRawSha256'])
        verify_references(lambda member: (HERE / member).read_bytes())
        report['packageManifestRawSha256'] = package['manifestRawSha256']
        if manifest.get('implementationCompleteness') != 'INCOMPLETE':
            raise InputError('This candidate cannot consume a manifest claiming completed implementation.')
        if not isinstance(owner_inputs, dict) or set(owner_inputs) - {'act', 'event', 'state', 'authorization', 'occupancy', 'evaluationSelection', 'originals'}:
            raise InputError('Unknown owner input or supplied report/Boolean. Only concrete input APIs are accepted.')
        intent, result = parse(original_intent_bytes), parse(original_result_bytes)
        if not isinstance(intent, dict) or not isinstance(result, dict):
            raise InputError('Original intent and proposed result must be JSON objects.')
        selection = None
        inventory_gate = None
        if ('evaluationSelection' in owner_inputs) != ('evaluationSelectionRawSha256' in package):
            raise InputError('Evaluation selection bytes and their independent pin must be supplied together.')
        if 'evaluationSelection' in owner_inputs:
            selection = payload_builder.validate_selection(owner_inputs['evaluationSelection'], package['evaluationSelectionRawSha256'], intent)
            inventory = owner_calls.verify_original_inventory_in_worker(owner_inputs['evaluationSelection'],
                                                                         package['evaluationSelectionRawSha256'],
                                                                         owner_inputs.get('originals', {}))
            report['originalInventory'] = inventory
            if inventory['status'] != 'ORIGINAL_INVENTORY':
                raise InputError('Exact selected original inventory failed: ' + inventory['status'] + ': ' + str(inventory.get('error')))
            outcomes = [row['result']['status'] for row in inventory['inventory']]
            inventory_gate = ('FAIL' if 'MISMATCH' in outcomes else
                              'NOT_EVALUATED' if 'NOT_EVALUATED' in outcomes else 'PASS')
        report['inputBindings'] = {
            'effectIntent': {'rawSha256': sha(original_intent_bytes), 'valueDigest': digest(intent)},
            'proposedResult': {'rawSha256': sha(original_result_bytes), 'valueDigest': digest(result)}}
        action = package['selectedAction']
        duties = parse((HERE / 'outer/source-duties.json').read_bytes())['duties']
        ordered = [d['id'] for d in duties]
        validate_graph(ordered)
        components = component_calls.invoke(intent, result, action, [])
        report['componentReports'] = components['componentReports']
        report['intrinsicFinding'] = components.get('intrinsics')
        report['schemaFindings'] = {'intent': components['intentErrors'], 'result': components['resultErrors']}
        if 'referenceInventory' in components:
            report['referenceInventory'] = components['referenceInventory']
        if 'renderedText' in components:
            report['exactRenderedText'] = components['renderedText']
            report['claimProjectionDigest'] = components['projectionDigest']

        dependencies = {name: {'id': name, 'disposition': 'NOT_EVALUATED',
                               'reason': reason, 'diagnostics': []}
                        for name, reason in OWNER_DEPENDENCIES.items()}
        def dependency(name, disposition, reason, errors=None):
            dependencies[name].update(disposition=disposition, reason=reason,
                                      diagnostics=errors or [])
        owner_boundary_observations = []
        source_mapping_observations = []
        boundary_owner_guards = {}
        def boundary_operand(owner, argument_path, value, path):
            present, selected = _present(value, path)
            origin = ({'root': owner} if argument_path is None else
                      {'owner': owner, 'argumentPath': argument_path})
            return {**origin, 'pointer': path, 'present': present,
                    **({'valueDigest': digest(selected)} if present else {})}
        def boundary_observe(gate, predicate, outcome, operands=(), *,
                             depends_on=(), controls=None, rule_operands=(),
                             edge_class='SELECTION_GUARD', owner_invocation=None,
                             inherit_owner_guards=True):
            # Record the result of the actual call-site expression. False
            # applicability is an observed branch, never a failed obligation.
            rid = 'owner-boundary:' + str(len(owner_boundary_observations))
            owner_boundary_observations.append({
                'id': rid, 'predicate': predicate, 'outcome': bool(outcome),
                'edgeClass': edge_class,
                'findingIds': [duty for duty, parents in PREREQUISITES.items() if gate in parents],
                'operands': list(operands),
                'dependsOn': list(dict.fromkeys([
                    *(boundary_owner_guards.get(gate, []) if inherit_owner_guards else []), *depends_on])),
                'controls': controls or {}, 'ruleOperands': list(rule_operands),
                **({'ownerInvocationId': owner_invocation} if owner_invocation else {}),
                'rule': {'module': 'verify_domain.py',
                         'moduleRawSha256': sha((HERE / 'verify_domain.py').read_bytes()),
                         'predicate': predicate}})
            return bool(outcome)
        def boundary_id():
            return owner_boundary_observations[-1]['id']
        owner_attempts = []
        def owner(kind, gate):
            attempt = {'owner': kind, 'gate': gate, 'invocationId': kind,
                       'inputs': owner_inputs.get(kind), 'outcome': 'NOT_SUPPLIED'}
            owner_attempts.append(attempt)
            if kind not in owner_inputs:
                dependency(gate, 'NOT_EVALUATED', 'Required concrete owner input was not supplied.')
                return None
            try:
                transport = owner_calls.invoke_owner(kind, owner_inputs[kind], original_intent_bytes)
            except (ValueError, TypeError, KeyError, OSError) as exc:
                attempt['outcome'] = 'INVOCATION_EXCEPTION'
                dependency(gate, 'FAIL', 'Owner input invocation failed.', [diagnostic('OWNER_INPUT', exc)])
                return None
            attempt['outcome'] = transport['status']
            report['ownerInvocations'][kind] = _invocation_summary(transport)
            if transport['status'] != 'OWNER_REPORT':
                disposition = 'FAIL' if transport['status'] == 'INVOCATION_INPUT_ERROR' else 'NOT_EVALUATED'
                dependency(gate, disposition, 'Exact selected owner checker did not return a report.',
                           [diagnostic(transport['status'], transport.get('error', 'No owner report.'))])
                return None
            value = transport['ownerReport']
            report['ownerReports'][kind] = value
            owner_outcome = value.get('disposition') if kind == 'authorization' else value.get('status')
            okay = owner_outcome == ('PASS' if kind == 'authorization' else 'CONDITIONAL_CONFORMANCE_PASS')
            unavailable = owner_outcome in ('DEPENDENCY_UNAVAILABLE', 'NOT_EVALUATED')
            dependency(gate, 'PASS' if okay else 'NOT_EVALUATED' if unavailable else 'FAIL',
                       'Recomputed concrete owner report; its exact status and runtime qualifications remain unchanged.',
                       [] if okay else [diagnostic('OWNER_DEPENDENCY_UNAVAILABLE' if unavailable
                                                  else 'OWNER_COMPARISON_FAILED', owner_outcome)])
            return value if okay else None
        authorization = owner('authorization', 'SELECTED_AUTHORIZATION_PATH')
        authorization_observations = []
        if authorization:
            authorization_observations.append({
                'id': 'authorization:owner-result', 'predicate': 'AUTHORIZATION_PASSING_OWNER_RESULT',
                'outcome': True, 'edgeClass': 'SELECTION_GUARD',
                'findingIds': [duty for duty, gates in PREREQUISITES.items() if 'SELECTED_AUTHORIZATION_PATH' in gates],
                'ownerInvocationId': 'authorization', 'operands': [],
                'controls': {'kind': 'RECOMPUTED_OWNER_REPORT_CONTROL', 'valueDigest': digest(authorization),
                             'selectionRawSha256': package.get('evaluationSelectionRawSha256')},
                'rule': {'module': 'verify_domain.py', 'moduleRawSha256': sha(Path(__file__).read_bytes()),
                         'predicate': 'authorization-owner-result'}})
            linked = authorization_sources.compare(owner_inputs['authorization'], original_intent_bytes,
                                                    result, action, selection, observations=authorization_observations)
            report['authorizationSourceComparisons'] = linked
            dependency('SELECTED_AUTHORIZATION_PATH', linked['disposition'],
                       'The exact reviewed owner API and original intent/action/schema/result/rule/assertor links compared. Eligibility, principal trust, candidate completeness and canonical selection remain explicitly NOT_ESTABLISHED in the owner report.', linked['errors'])
        act = owner('act', 'ASSERTION_ACT')
        boundary_observe('ASSERTION_ACT', 'ACT_OWNER_RESULT_ACCEPTED', bool(act),
            controls={'kind': 'RECOMPUTED_OWNER_REPORT_CONTROL', 'ownerInvocationId': 'act',
                      'ownerReportDigest': digest(report['ownerReports']['act']) if 'act' in report['ownerReports'] else None},
            owner_invocation='act')
        boundary_owner_guards['ASSERTION_ACT'] = [boundary_id()]
        if act:
            selected_profile = parse(owner_inputs['act']['intent_profile_bytes'])
            branch = {'ASSERT_STRUCTURE': 'structure', 'ASSERT_OPERATION_CLAIM': 'operation',
                      'ASSERT_COMPLIANCE': 'compliance'}[action]
            expected_schema = 'https://ofarm.dev/schema/drafts/non-default/assertion-record-domain-validation/' + branch + '-intent/v0.1'
            expected = {}
            schema_rules = []
            for path in [*(HERE / 'outer/carriers').glob('*.schema.json'),
                         HERE / 'components/revision-02/proposition.schema.json',
                         HERE / 'components/revision-02/owned-value-types-amendment.schema.json']:
                raw = path.read_bytes(); schema = parse(raw)
                expected[schema['$id']] = sha(raw)
                schema_rules.append({'localPath': str(path.relative_to(HERE)), 'pointer': '/$id',
                                     'valueDigest': digest(schema['$id']), 'rawSha256': sha(raw)})
            offered = {p['schemaId']: p['sha256'] for p in selected_profile['extraSchemas']}
            boundary_observe('ASSERTION_ACT', 'ACT_DOMAIN_SCHEMA_BUNDLE_READ', True,
                [boundary_operand('act', ['intent_profile_bytes'], selected_profile,
                                  '/extraSchemas/' + str(index) + '/' + field)
                 for index, item in enumerate(selected_profile['extraSchemas']) for field in ['schemaId', 'sha256']]
                or [boundary_operand('act', ['intent_profile_bytes'], selected_profile, '/extraSchemas')],
                controls={'offeredSchemaClosure': offered, 'expectedSchemaClosure': expected},
                rule_operands=schema_rules)
            bundle_read = boundary_id()
            schema_differs = boundary_observe('ASSERTION_ACT', 'ACT_DOMAIN_INTENT_SCHEMA_DIFFERS',
                    selected_profile['intentSchemaId'] != expected_schema,
                    [boundary_operand('act', ['intent_profile_bytes'], selected_profile, '/intentSchemaId')],
                    controls={'expectedSchemaId': expected_schema, 'selectedAction': action})
            schema_guard = boundary_id()
            if (schema_differs or boundary_observe('ASSERTION_ACT', 'ACT_DOMAIN_SCHEMA_CLOSURE_DIFFERS', offered != expected,
                        depends_on=[bundle_read, schema_guard], controls={'offeredSchemaClosure': offered,
                                                          'expectedSchemaClosure': expected},
                        rule_operands=schema_rules)):
                dependency('ASSERTION_ACT', 'FAIL', 'Act profile does not select this exact domain carrier and complete schema-byte closure.',
                           [diagnostic('ACT_DOMAIN_SCHEMA_CLOSURE_MISMATCH', 'An independently passing act profile cannot select different domain schemas.')])
                act = None
        boundary_observe('ASSERTION_ACT', 'ACT_DOMAIN_PROFILE_ELIGIBLE', bool(act),
            depends_on=[row['id'] for row in owner_boundary_observations if row['predicate'].startswith('ACT_DOMAIN_')],
            controls={'kind': 'RECOMPUTED_OWNER_REPORT_CONTROL', 'ownerInvocationId': 'act',
                      'ownerReportDigest': digest(report['ownerReports']['act']) if 'act' in report['ownerReports'] else None,
                      'domainGateDisposition': dependencies['ASSERTION_ACT']['disposition']}, owner_invocation='act')
        act_eligibility = boundary_id()
        associated = intent.get('associatedSemanticEventBinding')
        if boundary_observe('EVENT_OWNER', 'ASSOCIATED_EVENT_ABSENT', associated is None,
                [boundary_operand('effectIntent', None, intent, '/associatedSemanticEventBinding')]):
            if 'event' in owner_inputs:
                dependency('EVENT_OWNER', 'FAIL', 'Unselected Event Ingress input was supplied.')
            else:
                dependency('EVENT_OWNER', 'NOT_APPLICABLE', 'No associatedSemanticEventBinding is declared.')
                dependency('EVENT_DOMAIN', 'NOT_APPLICABLE', 'No associatedSemanticEventBinding is declared.')
        else:
            association_guard = boundary_id()
            owner_boundary_observations[-1]['selectsOwnerInvocations'] = ['event']
            event = owner('event', 'EVENT_OWNER')
            boundary_observe('EVENT_OWNER', 'EVENT_OWNER_RESULT_ACCEPTED', bool(event),
                depends_on=[association_guard],
                controls={'kind': 'RECOMPUTED_OWNER_REPORT_CONTROL', 'ownerInvocationId': 'event',
                          'ownerReportDigest': digest(report['ownerReports']['event']) if 'event' in report['ownerReports'] else None},
                owner_invocation='event')
            boundary_owner_guards['EVENT_OWNER'] = [boundary_id()]
            if event:
                raw = owner_inputs['event']['envelope_bytes']
                envelope = parse(raw)
                selected = associated.get('digest')
                boundary_observe('EVENT_OWNER', 'ASSOCIATED_EVENT_DIGEST_SELECTED', bool(selected),
                    [boundary_operand('effectIntent', None, intent, '/associatedSemanticEventBinding/digest')])
                digest_selection = boundary_id()
                identity_differs = boundary_observe('EVENT_OWNER', 'ASSOCIATED_EVENT_IDENTITY_DIFFERS',
                        envelope.get('semanticEventId') != associated.get('ref'),
                        [boundary_operand('event', ['envelope_bytes'], envelope, '/semanticEventId'),
                         boundary_operand('effectIntent', None, intent, '/associatedSemanticEventBinding/ref')])
                identity_guard = boundary_id()
                event_comparison_guards = [identity_guard, digest_selection]
                digest_differs = False
                if not identity_differs and selected:
                    digest_differs = boundary_observe('EVENT_OWNER', 'ASSOCIATED_EVENT_DIGEST_DIFFERS',
                            digest(envelope) != selected,
                            [boundary_operand('event', ['envelope_bytes'], envelope, ''),
                             boundary_operand('effectIntent', None, intent, '/associatedSemanticEventBinding/digest')],
                            depends_on=[digest_selection, identity_guard])
                    event_comparison_guards.append(boundary_id())
                if identity_differs or digest_differs:
                    dependency('EVENT_OWNER', 'FAIL', 'Owner proof envelope differs from the intent association.',
                               [diagnostic('ASSOCIATED_EVENT_BYTES_MISMATCH', 'Exact association selection failed.')])
                elif boundary_observe('EVENT_OWNER', 'ASSOCIATED_EVENT_REVISION_SELECTED', 'revisionRef' in associated,
                        [boundary_operand('effectIntent', None, intent, '/associatedSemanticEventBinding/revisionRef')],
                        depends_on=event_comparison_guards):
                    mappings = []
                    revision_selection = boundary_id()
                    mapping_is_available = boundary_observe('EVENT_OWNER', 'ASSOCIATED_EVENT_ACT_MAPPING_AVAILABLE',
                            bool(act and dependencies['ASSERTION_ACT']['disposition'] == 'PASS'),
                            depends_on=[revision_selection, act_eligibility],
                            controls={'actPresent': bool(act), 'actDisposition': dependencies['ASSERTION_ACT']['disposition']})
                    mapping_available = boundary_id()
                    if mapping_is_available:
                        context = parse(owner_inputs['act']['context_bytes'])
                        boundary_observe('EVENT_OWNER', 'ASSOCIATED_EVENT_MAPPING_SET', True,
                            [boundary_operand('act', ['context_bytes'], context, '/selectedSourceInputs')],
                            depends_on=[mapping_available], controls={'entryCount': len(context['selectedSourceInputs'])})
                        mapping_set = boundary_id()
                        def event_mapping(entry, index):
                            prefix = '/selectedSourceInputs/' + str(index)
                            def field(name):
                                return boundary_operand('act', ['context_bytes'], context, prefix + '/' + name)
                            previous = [mapping_set]
                            checks = [('ROLE', 'role', lambda: entry['role'] == 'SEMANTIC_EVENT_ENVELOPE',
                                       lambda: [], {'expectedRole': 'SEMANTIC_EVENT_ENVELOPE'}),
                                      ('BINDING', 'binding', lambda: same(entry['binding'], associated),
                                       lambda: [boundary_operand('effectIntent', None, intent, '/associatedSemanticEventBinding')], {}),
                                      ('RAW', 'bytesSha256', lambda: entry['bytesSha256'] == sha(raw),
                                       lambda: [boundary_operand('event', ['envelope_bytes'], envelope, '')], {'envelopeRawSha256': sha(raw)}),
                                      ('VALUE', 'valueDigest', lambda: entry['valueDigest'] == digest(envelope),
                                       lambda: [boundary_operand('event', ['envelope_bytes'], envelope, '')], {})]
                            for name, key, predicate, operands, controls in checks:
                                matches = boundary_observe('EVENT_OWNER', 'ASSOCIATED_EVENT_MAPPING_' + name,
                                    predicate(), [field(key), *operands()], depends_on=previous, controls=controls)
                                previous = [boundary_id()]
                                if not matches:
                                    return False
                            offered_raw = owner_inputs['act']['source_inputs'].get(associated['ref'])
                            return boundary_observe('EVENT_OWNER', 'ASSOCIATED_EVENT_MAPPING_SOURCE_BYTES', offered_raw == raw,
                                [boundary_operand('effectIntent', None, intent, '/associatedSemanticEventBinding/ref'),
                                 {'owner': 'act', 'argumentPath': ['source_inputs', associated['ref']], 'pointer': ''},
                                 boundary_operand('event', ['envelope_bytes'], envelope, '')], depends_on=previous,
                                controls={'offeredRawSha256': sha(offered_raw) if offered_raw is not None else None,
                                          'envelopeRawSha256': sha(raw)})
                        mappings = [entry for index, entry in enumerate(context['selectedSourceInputs'])
                                    if event_mapping(entry, index)]
                    boundary_observe('EVENT_OWNER', 'ASSOCIATED_EVENT_MAPPING_CARDINALITY', len(mappings) == 1,
                        depends_on=[mapping_available, *[row['id'] for row in owner_boundary_observations
                                    if row['predicate'].startswith('ASSOCIATED_EVENT_MAPPING_')]],
                        controls={'cardinality': len(mappings), 'requiredCardinality': 1})
                    if len(mappings) != 1:
                        dependency('EVENT_OWNER', 'NOT_EVALUATED', 'The supplied revision association lacks one exact independently pinned raw/JCS mapping through the passing act source interface.')
        state = owner('state', 'PROTECTED_PROPOSED_STATE')
        state_context = None
        if state:
            state_context = parse(owner_inputs['state']['context_bytes'])
            checks = []
            for field, raw, value in [('effectIntent', original_intent_bytes, intent),
                                       ('proposedAssertion', original_result_bytes, result)]:
                spec = state_context[field]
                if spec['rawSha256'] != sha(raw) or spec['binding']['digest'] != digest(value):
                    checks.append(diagnostic('STATE_INPUT_BYTES_MISMATCH', field))
                selected_raw = owner_inputs['state']['records'].get(spec['binding']['ref'])
                if selected_raw != raw:
                    checks.append(diagnostic('STATE_RECORD_RAW_BYTES_MISMATCH', field))
            if state_context['actionClass'] != action:
                checks.append(diagnostic('STATE_ACTION_MISMATCH', 'State context action must match the independently selected action.'))
            if checks:
                dependency('PROTECTED_PROPOSED_STATE', 'FAIL', 'State proof does not protect this exact evaluation.', checks)
                state = None
            # This pass means the proposed write/read observations compared. It
            # never establishes the selected later transaction gate or commit.
        if state:
            # The owner checker proves its offered context/proof/snapshot are
            # internally consistent. EvaluationSelection v0.4 does not name
            # which independently pinned originals are those three artifacts,
            # and it does not supply the domain-derived full obligation set.
            # Keep that separate comparison explicitly open. An owner PASS must
            # not become a domain postcondition PASS through this dependency.
            report['protectedStateComparison'] = {
                'status': 'NOT_EVALUATED',
                'reason': 'Independent #51 artifact roles and complete domain-required read, absence, set and write obligations are not selected.',
                'ownerStatus': state['status'],
                'sourceAdmission': 'NOT_ESTABLISHED',
                'runtimeProtection': 'NOT_ESTABLISHED'}
            dependency('PROTECTED_PROPOSED_STATE', 'NOT_EVALUATED',
                       'The exact #51 owner report passed conditionally, but the independent domain obligation comparison is incomplete.')
        partial_graph = None
        graph_state_context = state_context if state else None
        if selection is not None:
            partial_graph = closure_graph.derive(
                owner_inputs['evaluationSelection'], inventory,
                original_intent_bytes, original_result_bytes,
                selected_state_context=graph_state_context,
                selected_action=action, original_bytes=owner_inputs.get('originals', {}))
            report['partialRequirementGraph'] = partial_graph
        identity_provenance = protected_identity_provenance.derive(
            action, original_result_bytes,
            selection_bytes=owner_inputs.get('evaluationSelection') if selection is not None else None,
            independent_selection_raw_sha256=package.get('evaluationSelectionRawSha256'),
            checked_inventory=inventory if selection is not None else None,
            partial_requirement_graph=partial_graph)
        report['protectedIdentityProvenance'] = identity_provenance
        if state:
            known_identity = protected_identity_provenance.compare_known_to_offered(
                identity_provenance, owner_inputs['state']['context_bytes'])
            report['knownIdentityComparison'] = known_identity
            known_write = protected_known_write.compare(
                action, original_result_bytes,
                selection_bytes=owner_inputs.get('evaluationSelection') if selection is not None else None,
                independent_selection_raw_sha256=package.get('evaluationSelectionRawSha256'),
                checked_inventory=inventory if selection is not None else None,
                partial_requirement_graph=partial_graph,
                context_bytes=owner_inputs['state']['context_bytes'],
                proof_bytes=owner_inputs['state']['proof_bytes'],
                snapshot_bytes=owner_inputs['state']['snapshot_bytes'])
            report['protectedKnownWrite'] = known_write
            if known_identity['status'] == 'FAIL' or known_write['status'] == 'FAIL':
                identity_contradiction = any(row['code'] == 'KNOWN_IDENTITY_CONTRADICTION'
                                             for row in known_identity['comparisons'])
                write_contradiction = any(row['disposition'] == 'FAIL'
                                          for row in known_write['comparisons'])
                if identity_contradiction or write_contradiction:
                    comparison_reason = 'An independently known domain identity, proposed write, or ID absence contradicts the offered #51 artifacts.'
                else:
                    comparison_reason = 'Independent domain provenance or offered #51 artifact validation failed.'
                report['protectedStateComparison'] = {
                    'status': 'FAIL',
                    'reason': comparison_reason,
                    'knownIdentityComparison': known_identity,
                    'protectedKnownWrite': known_write,
                    'sourceAdmission': 'NOT_ESTABLISHED',
                    'runtimeProtection': 'NOT_ESTABLISHED'}
                dependency('PROTECTED_PROPOSED_STATE', 'FAIL',
                           comparison_reason,
                           [diagnostic(row['code'], row['field']) for row in known_identity['comparisons']
                            if row['disposition'] == 'FAIL']
                           + [diagnostic(item['code'], item.get('field', item['code']))
                              for item in known_identity['diagnostics']]
                           + [diagnostic(row['code'], row['artifact'] + ':' + row['key'])
                              for row in known_write['comparisons'] if row['disposition'] == 'FAIL']
                           + [diagnostic(item['code'], item.get('artifact', item['code']))
                              for item in known_write['diagnostics']
                              if item['code'] != 'OFFERED_ARTIFACT_UNAVAILABLE'])
                state = None
        boundary_observe(None, 'FINAL_STATE_ELIGIBILITY_FOR_EVENT_REVISION', bool(state),
            controls={'kind': 'RECOMPUTED_OWNER_REPORT_CONTROL', 'ownerInvocationId': 'state',
                      'ownerReportDigest': digest(report['ownerReports']['state']) if 'state' in report['ownerReports'] else None,
                      'domainStateLinkageDigest': digest(dependencies['PROTECTED_PROPOSED_STATE']),
                      'knownIdentityComparisonDigest': digest(report['knownIdentityComparison']) if 'knownIdentityComparison' in report else None,
                      'protectedKnownWriteDigest': digest(report['protectedKnownWrite']) if 'protectedKnownWrite' in report else None,
                      'qualification': 'Already computed domain control outcomes, not original operands or C4 acceptance.'},
            owner_invocation='state')
        final_state_eligibility = boundary_id()
        occupancy = {}
        occupancy_outcome_guards = {}
        if 'occupancy' in owner_inputs:
            if not isinstance(owner_inputs['occupancy'], dict):
                raise InputError('Occupancy inputs must map exact atom IDs to original owner inputs.')
            def occupancy_atoms(p, path='/assertionBody/proposition', parents=()):
                if boundary_observe('DOMAIN_MEANING', 'OCCUPANCY_ATOM_FORM', p['form'] == 'ATOM',
                        [boundary_operand('effectIntent', None, intent, path + '/form')], depends_on=parents):
                    form_guard = boundary_id()
                    if boundary_observe('DOMAIN_MEANING', 'OCCUPANCY_ATOM_DEFINITION', p['definition'].endswith(':S13'),
                            [boundary_operand('effectIntent', None, intent, path + '/definition')],
                            depends_on=[form_guard], controls={'definitionSuffix': ':S13'}):
                        boundary_observe('DOMAIN_MEANING', 'OCCUPANCY_ATOM_ID', True,
                            [boundary_operand('effectIntent', None, intent, path + '/atomId')],
                            depends_on=[boundary_id()], controls={'atomId': p['atomId']})
                        return {p['atomId']}
                    return set()
                form_guard = boundary_id()
                if boundary_observe('DOMAIN_MEANING', 'OCCUPANCY_SINGLE_CHILD', 'child' in p,
                        [boundary_operand('effectIntent', None, intent, path + '/child')], depends_on=[form_guard]):
                    return occupancy_atoms(p['child'], path + '/child', [boundary_id()])
                children_guard = boundary_id()
                boundary_observe('DOMAIN_MEANING', 'OCCUPANCY_CHILDREN', True,
                    [boundary_operand('effectIntent', None, intent, path + '/children')], depends_on=[children_guard])
                children_guard = boundary_id()
                return set().union(*(occupancy_atoms(c, path + '/children/' + str(index), [children_guard])
                                     for index, c in enumerate(p['children'])))
            selected_occupancy_atoms = occupancy_atoms(intent['assertionBody']['proposition'])
            if boundary_observe('DOMAIN_MEANING', 'OCCUPANCY_UNSELECTED_INPUT_KEYS',
                    bool(set(owner_inputs['occupancy']) - selected_occupancy_atoms),
                    depends_on=[row['id'] for row in owner_boundary_observations
                                if row['predicate'].startswith('OCCUPANCY_ATOM_')
                                or row['predicate'] in {'OCCUPANCY_SINGLE_CHILD', 'OCCUPANCY_CHILDREN'}],
                    controls={'suppliedInvocationKeys': sorted(owner_inputs['occupancy']),
                              'selectedAtomIds': sorted(selected_occupancy_atoms)}):
                raise InputError('Unselected occupancy owner input for a missing or non-occupancy atom.')
            occupancy_key_guard = boundary_id()
            report['ownerReports']['occupancy'] = {}
            for atom_id, original_inputs in owner_inputs['occupancy'].items():
                selecting_events = [row for row in owner_boundary_observations
                    if row['id'] == occupancy_key_guard or
                    (row['predicate'] == 'OCCUPANCY_ATOM_ID' and row['controls']['atomId'] == atom_id)]
                for row in selecting_events:
                    row.setdefault('selectsOwnerInvocations', []).append('occupancy:' + atom_id)
                attempt = {'owner': 'occupancy', 'gate': 'OCCUPANCY_OWNER',
                           'invocationId': 'occupancy:' + atom_id, 'inputs': original_inputs,
                           'outcome': 'NOT_RETURNED'}
                owner_attempts.append(attempt)
                transport = owner_calls.invoke_owner('occupancy', original_inputs)
                attempt['outcome'] = transport['status']
                report['ownerInvocations'].setdefault('occupancy', {})[atom_id] = _invocation_summary(transport)
                owner_report_unavailable = boundary_observe('DOMAIN_MEANING', 'OCCUPANCY_OWNER_REPORT_UNAVAILABLE', transport['status'] != 'OWNER_REPORT',
                        depends_on=[row['id'] for row in selecting_events],
                        controls={'kind': 'RECOMPUTED_OWNER_REPORT_CONTROL', 'ownerInvocationId': 'occupancy:' + atom_id,
                                  'transportStatus': transport['status'],
                                  'ownerReportDigest': digest(transport['ownerReport']) if 'ownerReport' in transport else None},
                        owner_invocation='occupancy:' + atom_id)
                occupancy_outcome_guards[atom_id] = boundary_id()
                if owner_report_unavailable:
                    continue
                checked = transport['ownerReport']
                report['ownerReports']['occupancy'][atom_id] = checked
                occupancy[atom_id] = {'report': checked, 'request': parse(original_inputs['request_bytes'])}
        source_selections = list(selection.get('sourceSelections', [])) if selection else []
        source_mapping_origins = [[] for item in source_selections]
        if act:
            act_context = parse(owner_inputs['act']['context_bytes'])
            boundary_observe(None, 'ACT_SOURCE_MAPPING_SET', True,
                [boundary_operand('act', ['context_bytes'], act_context, '/selectedSourceInputs')],
                depends_on=[act_eligibility], controls={'entryCount': len(act_context['selectedSourceInputs'])})
            act_mapping_set = boundary_id()
            for index, selected_source in enumerate(act_context['selectedSourceInputs']):
                mapping = {'binding': selected_source['binding'], 'rawSha256': selected_source['bytesSha256'], 'valueDigest': selected_source['valueDigest']}
                previous_indices = [n for n, v in enumerate(source_selections) if same(v['binding'], mapping['binding'])]
                previous = [source_selections[n] for n in previous_indices]
                conflict = bool(previous and not same(previous[0], mapping))
                boundary_observe(None, 'ACT_SOURCE_MAPPING_MERGE', not conflict,
                    [boundary_operand('act', ['context_bytes'], act_context,
                                      '/selectedSourceInputs/' + str(index) + '/' + field)
                     for field in ['binding', 'bytesSha256', 'valueDigest']],
                    depends_on=[act_mapping_set, *[rid for n in previous_indices for rid in source_mapping_origins[n]]],
                    controls={'mapping': mapping, 'previousMappings': previous,
                              'evaluationSelectionDigest': digest(selection) if selection else None,
                              'branch': 'CONFLICT' if conflict else 'EXISTING' if previous else 'APPEND'})
                mapping_observation = boundary_id()
                source_mapping_observations.append({'binding': mapping['binding'], 'rawSha256': mapping['rawSha256'],
                    'valueDigest': mapping['valueDigest'], 'observationId': mapping_observation})
                if conflict:
                    raise InputError('Conflicting independently pinned act/domain source selector mappings.')
                if not previous:
                    source_selections.append(mapping)
                    source_mapping_origins.append([mapping_observation])
                else:
                    source_mapping_origins[previous_indices[0]].append(mapping_observation)
        for atom_id, checked in occupancy.items():
            if boundary_observe('DOMAIN_MEANING', 'OCCUPANCY_SOURCE_MAPPING_OWNER_UNMATCHED',
                    checked['report']['status'] != 'MATCHED_SELECTED_OCCUPANCY_EVIDENCE',
                    depends_on=[occupancy_outcome_guards[atom_id]],
                    controls={'kind': 'RECOMPUTED_OWNER_REPORT_CONTROL', 'ownerInvocationId': 'occupancy:' + atom_id,
                              'ownerReportDigest': digest(checked['report']), 'ownerReportStatus': checked['report']['status']},
                    owner_invocation='occupancy:' + atom_id):
                continue
            owner_guard = boundary_id()
            context = parse(owner_inputs['occupancy'][atom_id]['context_bytes'])
            boundary_observe('DOMAIN_MEANING', 'OCCUPANCY_SOURCE_MAPPING_SET', True,
                [boundary_operand('occupancy:' + atom_id, ['context_bytes'], context, '/records')],
                depends_on=[owner_guard], controls={'entryCount': len(context['records'])})
            mapping_set = boundary_id()
            for index, entry in enumerate(context['records']):
                if boundary_observe('DOMAIN_MEANING', 'OCCUPANCY_SOURCE_MAPPING_NON_JSON', entry['digestMode'] != 'JCS_JSON',
                        [boundary_operand('occupancy:' + atom_id, ['context_bytes'], context,
                                          '/records/' + str(index) + '/digestMode')], depends_on=[mapping_set]):
                    continue
                mode_guard = boundary_id()
                mapping = {'binding': entry['binding'], 'rawSha256': entry['bytesSha256'], 'valueDigest': entry['valueDigest']}
                previous_indices = [n for n, v in enumerate(source_selections) if same(v['binding'], mapping['binding'])]
                previous = [source_selections[n] for n in previous_indices]
                conflict = bool(previous and not same(previous[0], mapping))
                boundary_observe(None, 'OCCUPANCY_SOURCE_MAPPING_MERGE', not conflict,
                    [boundary_operand('occupancy:' + atom_id, ['context_bytes'], context,
                                      '/records/' + str(index) + '/' + field)
                     for field in ['binding', 'bytesSha256', 'valueDigest']],
                    depends_on=[mode_guard, *[rid for n in previous_indices for rid in source_mapping_origins[n]]],
                    controls={'mapping': mapping, 'previousMappings': previous,
                              'evaluationSelectionDigest': digest(selection) if selection else None,
                              'branch': 'CONFLICT' if conflict else 'EXISTING' if previous else 'APPEND'})
                mapping_observation = boundary_id()
                source_mapping_observations.append({'binding': mapping['binding'], 'rawSha256': mapping['rawSha256'],
                    'valueDigest': mapping['valueDigest'], 'observationId': mapping_observation})
                if conflict:
                    raise InputError('Conflicting independently pinned occupancy/domain source selector mappings.')
                if not previous:
                    source_selections.append(mapping)
                    source_mapping_origins.append([mapping_observation])
                else:
                    source_mapping_origins[previous_indices[0]].append(mapping_observation)
        manifest_report, resolved_sources = input_manifest.derive(owner_inputs, components.get('referenceInventory', {}),
                                                                  state_context if state else None,
                                                                  source_selections, {'intent': original_intent_bytes, 'proposedResult': original_result_bytes})
        report['immutableInputManifest'] = manifest_report
        fallback_parent_ids = [final_state_eligibility]
        if state:
            fallback_parent_ids.extend(row['id'] for row in owner_boundary_observations
                                       if row['predicate'] == 'ASSOCIATED_EVENT_ABSENT')
        if state and associated and 'revisionRef' in associated:
            # These are the actually executed decisions that produced the
            # current event gate. Their own edges retain short-circuit parents.
            event_decisions = [row['id'] for row in owner_boundary_observations if row['predicate'] in {
                'EVENT_OWNER_RESULT_ACCEPTED', 'ASSOCIATED_EVENT_IDENTITY_DIFFERS',
                'ASSOCIATED_EVENT_DIGEST_DIFFERS', 'ASSOCIATED_EVENT_MAPPING_CARDINALITY'}]
            if event_decisions:
                fallback_parent_ids.append(event_decisions[-1])
        if boundary_observe('EVENT_OWNER', 'ASSOCIATED_EVENT_REVISION_FALLBACK_APPLICABLE',
                bool(state and associated and 'revisionRef' in associated
                     and dependencies['EVENT_OWNER']['disposition'] == 'NOT_EVALUATED'
                     and report.get('ownerReports', {}).get('event', {}).get('status') == 'CONDITIONAL_CONFORMANCE_PASS'),
                [boundary_operand('effectIntent', None, intent, '/associatedSemanticEventBinding/revisionRef')]
                    if state and associated else [],
                depends_on=fallback_parent_ids, inherit_owner_guards=False,
                controls={'stateAvailable': bool(state), 'eventOwnerDisposition': dependencies['EVENT_OWNER']['disposition'],
                          'eventOwnerReportStatus': report.get('ownerReports', {}).get('event', {}).get('status')}):
            envelope_raw = owner_inputs['event']['envelope_bytes']
            fallback_guard = boundary_id()
            fallback_checks = []
            def fallback_match(entry):
                if not boundary_observe('EVENT_OWNER', 'ASSOCIATED_EVENT_REVISION_FALLBACK_BINDING',
                        same(entry['binding'], associated),
                        [boundary_operand('effectIntent', None, intent, '/associatedSemanticEventBinding')],
                        depends_on=[fallback_guard], controls={'sourceId': entry['id'], 'binding': entry['binding'],
                            'candidateOrigin': 'DERIVED_EXISTING_PROTECTED_RESOLUTION_NOT_SOURCE_ADMISSION'}):
                    fallback_checks.append(boundary_id())
                    return False
                binding_guard = boundary_id()
                if not boundary_observe('EVENT_OWNER', 'ASSOCIATED_EVENT_REVISION_FALLBACK_RAW',
                        entry['rawSha256'] == sha(envelope_raw),
                        [boundary_operand('event', ['envelope_bytes'], parse(envelope_raw), '')],
                        depends_on=[binding_guard], controls={'sourceId': entry['id'], 'rawSha256': entry['rawSha256'],
                            'envelopeRawSha256': sha(envelope_raw),
                            'candidateOrigin': 'DERIVED_EXISTING_PROTECTED_RESOLUTION_NOT_SOURCE_ADMISSION'}):
                    fallback_checks.append(boundary_id())
                    return False
                raw_guard = boundary_id()
                matches = boundary_observe('EVENT_OWNER', 'ASSOCIATED_EVENT_REVISION_FALLBACK_VALUE',
                    entry['valueDigest'] == digest(parse(envelope_raw)),
                    [boundary_operand('event', ['envelope_bytes'], parse(envelope_raw), '')],
                    depends_on=[raw_guard], controls={'sourceId': entry['id'], 'valueDigest': entry['valueDigest'],
                        'candidateOrigin': 'DERIVED_EXISTING_PROTECTED_RESOLUTION_NOT_SOURCE_ADMISSION'})
                fallback_checks.append(boundary_id())
                return matches
            matches = [entry for entry in resolved_sources if fallback_match(entry)]
            if boundary_observe('EVENT_OWNER', 'ASSOCIATED_EVENT_REVISION_FALLBACK_CARDINALITY', len(matches) == 1,
                    depends_on=[fallback_guard, *fallback_checks, *[row['observationId'] for row in source_mapping_observations
                                                 if same(row['binding'], associated)]],
                    controls={'matchingSourceIds': [entry['id'] for entry in matches],
                              'requiredCardinality': 1,
                              'candidateOrigin': 'DERIVED_EXISTING_PROTECTED_RESOLUTION_NOT_SOURCE_ADMISSION'}):
                dependency('EVENT_OWNER', 'PASS', 'The unchanged event revision selector resolves through an independently pinned raw/JCS mapping to the exact protected original envelope bytes.')
        if state:
            dependency('RESOLVED_INPUT_CLOSURE', 'FAIL' if manifest_report['errors'] else 'PASS',
                       'Exact original-byte owner inputs and typed claim references are inventoried; every required source resolves through the protected read set. Eligible use remains separate.', manifest_report['errors'])
        event_inputs = None
        if not components['intentErrors'] and not components.get('intrinsics', {}).get('errors'):
            event_inputs = ({'report': report['ownerReports']['event'],
                             'envelope': parse(owner_inputs['event']['envelope_bytes']),
                             'envelopeRawSha256': sha(owner_inputs['event']['envelope_bytes']),
                             'profile': parse(owner_inputs['event']['profile_bytes'])}
                            if 'event' in report['ownerReports'] else None)
            ordinary_sources = resolved_sources
            if selection is not None and selection.get('schemaVersion') == 'ofarm.assertionDomainEvaluationSelection.v0.5':
                from original_inputs import bind_roots
                from condition_property_resolution import catalog as condition_property_catalog
                source_bound = bind_roots(owner_inputs['evaluationSelection'], inventory,
                    original_intent_bytes, original_result_bytes,
                    selected_state_context=graph_state_context, original_bytes=owner_inputs.get('originals', {}))
                # This ordinary route still requires the existing protected
                # source catalog. Independent generic originals cannot silently
                # replace a missing state-owner read or source relationship.
                ordinary_sources = condition_property_catalog(resolved_sources, source_bound, require_existing=True)
            source_checks = component_calls.invoke(intent, result, action, [], resolved_sources=ordinary_sources, occupancy=occupancy,
                                                   source_context_digest=digest(state_context) if state else digest(selection) if selection else digest(intent), event=event_inputs)
            report['sourceTrace'] = source_checks.get('sourceTrace', {'resolvedInputs': [], 'unresolvedInputs': []})
            evidence = source_checks.get('evidenceSourceComparisons')
            if evidence is not None:
                report['evidenceSourceComparisons'] = evidence
                dependency('EVIDENCE_USE_AND_CITATION_CLOSURE', evidence['disposition'],
                           evidence['qualification'], evidence['errors'])
            report['complianceSourceComparisons'] = source_checks.get('complianceSourceComparisons', {})
            for gate, finding in report['complianceSourceComparisons'].items():
                dependency(gate, finding['disposition'], finding['qualification'], finding['errors'])
            report['identitySourceComparisons'] = source_checks.get('identitySourceComparisons', {})
            context = source_checks.get('contextSourceComparisons')
            if context is not None:
                report['contextSourceComparisons'] = context
                dependency('CONTEXT_IDENTITIES_AND_RELATIONS', context['disposition'], context['qualification'], context['errors'])
            for gate, finding in report['identitySourceComparisons'].items():
                dependency(gate, finding['disposition'],
                           finding.get('reason', finding.get('qualification', 'Exact selected identity comparison.')),
                           finding['errors'])
            temporal = source_checks.get('temporalSources')
            if temporal is not None:
                report['temporalSources'] = temporal
                dependency('SUBJECT_TIME_SOURCES', temporal['disposition'],
                           'Exact profile-selected body applicability, body time or original payload/measurement fields are compared; measured activity meaning remains a separate required use.', temporal['errors'])
            automatic = source_checks.get('automaticSourceComparisons')
            if 'propositionEvaluation' in source_checks:
                report['propositionEvaluation'] = source_checks['propositionEvaluation']
            event_domain = source_checks.get('eventSourceComparisons')
            if event_domain is not None:
                report['eventSourceComparisons'] = event_domain
                dependency('EVENT_DOMAIN', event_domain['disposition'], event_domain['qualification'], event_domain['errors'])
                if event_domain.get('caseDefinitionBinding'):
                    report['eventCaseDefinitionBinding'] = event_domain['caseDefinitionBinding']
            if automatic is not None:
                required_references = automatic.get('requiredReferences', []) + (event_domain or {}).get('requiredReferences', [])
                if required_references:
                    expanded = {'references': components['referenceInventory']['references'] + required_references}
                    manifest_report, _ = input_manifest.derive(owner_inputs, expanded, state_context if state else None, source_selections,
                                                              {'intent': original_intent_bytes, 'proposedResult': original_result_bytes})
                    report['immutableInputManifest'] = manifest_report
                    if state:
                        dependency('RESOLVED_INPUT_CLOSURE', 'FAIL' if manifest_report['errors'] else 'PASS',
                                   'The protected original-byte manifest includes recursively consumed normative definition inputs as well as typed claim and concrete owner inputs.', manifest_report['errors'])
                report['automaticSourceComparisons'] = automatic
                report['unresolvedSourceRoles'] = automatic['remainingRoles']
                dependency('DOMAIN_MEANING', 'FAIL' if automatic['errors'] else 'NOT_EVALUATED' if automatic['remainingRoles'] else 'PASS',
                           'Every recursive atom selects its source comparisons from the protected original records; caller-supplied expected meanings cannot choose or discharge a predicate.', automatic['errors'])
                if action == 'ASSERT_OPERATION_CLAIM':
                    operation_atoms = [a for a in automatic['atoms'] if a['row'].startswith('O')]
                    operation_errors = [e for a in operation_atoms for e in a['errors']]
                    operation_roles = [r for a in operation_atoms for r in a['remainingRoles']]
                    dependency('OPERATION_SOURCES', 'FAIL' if operation_errors else 'NOT_EVALUATED' if operation_roles else 'PASS',
                               'Selected operation carrier, performer/asset roles and quantity array indices are derived from the exact typed claim and source bytes.', operation_errors)
        if partial_graph is not None:
            # Extend after every actual owner invocation, including failures.
            # Replay source readers from the independent original catalog;
            # offered protected reads never define the C3 denominator.
            from original_inputs import bind_roots
            from c3_dependency_coverage import extend as extend_c3_coverage
            bound = bind_roots(owner_inputs['evaluationSelection'], inventory,
                               original_intent_bytes, original_result_bytes,
                               selected_state_context=graph_state_context,
                               original_bytes=owner_inputs.get('originals', {}))
            extend_c3_coverage(partial_graph, bound, owner_attempts,
                               original_intent_bytes, action, occupancy=occupancy, event=event_inputs)
        if inventory_gate is not None:
            current = dependencies['RESOLVED_INPUT_CLOSURE']['disposition']
            if inventory_gate == 'FAIL' or inventory_gate == 'NOT_EVALUATED' and current == 'PASS':
                dependency('RESOLVED_INPUT_CLOSURE', inventory_gate,
                           'Independently pinned original byte inventory has a mismatch or missing selected input.',
                           dependencies['RESOLVED_INPUT_CLOSURE']['diagnostics']
                           + [diagnostic('ORIGINAL_INVENTORY_' + inventory_gate, inventory_gate)])
        if partial_graph is not None:
            current = dependencies['RESOLVED_INPUT_CLOSURE']['disposition']
            input_failures = [row for row in partial_graph['requirements']
                              if row['disposition'] == 'FAIL'
                              and _required_original_row(row)]
            source_graph_errors = [item for item in partial_graph['diagnostics']
                                   if closure_graph._is_immutable_input_diagnostic(item)]
            if input_failures or source_graph_errors:
                graph_errors = [diagnostic('PARTIAL_GRAPH_REQUIREMENT_FAILED', row['id'])
                                for row in input_failures]
                graph_errors.extend(diagnostic(item['code'], item.get('detail', item['code']))
                                    for item in source_graph_errors)
                dependency('RESOLVED_INPUT_CLOSURE', 'FAIL',
                           'An independently selected root or typed reference contradicts the original input inventory.',
                           dependencies['RESOLVED_INPUT_CLOSURE']['diagnostics'] + graph_errors)
            elif current == 'PASS':
                dependency('RESOLVED_INPUT_CLOSURE', 'NOT_EVALUATED',
                           'Known selected roots and typed references are retained, but recursive source and protected-read closure remains incomplete.')
        elif dependencies['RESOLVED_INPUT_CLOSURE']['disposition'] == 'PASS':
            dependency('RESOLVED_INPUT_CLOSURE', 'NOT_EVALUATED',
                       'The owner input manifest is bounded; no independently pinned evaluation selection or fixed-point requirement/use graph is available.')
        facts = {f['predicateId']: closure_graph.bind_copy_operands(f, action) for f in components['copyFacts']}
        local = {name: {'comparisons': [], 'diagnostics': []} for name in ordered}
        if partial_graph is not None:
            for row in partial_graph['requirements']:
                if row['disposition'] == 'FAIL':
                    if row.get('kind') == 'CANDIDATE_COPY_FACT':
                        for finding_id in row['findingIds']:
                            local[finding_id]['diagnostics'].append(
                                diagnostic('SELECTED_COPY_REQUIREMENT_FAILED', row['id'],
                                           row.get('origin', {}).get('pointer', '')))
                    elif row.get('kind') == 'CANDIDATE_PROPOSITION_OCCURRENCE':
                        local['AR_BODY']['diagnostics'].append(
                            diagnostic('SELECTED_PROPOSITION_REQUIREMENT_FAILED', row['id'],
                                       row.get('origin', {}).get('pointer', '')))
                    elif row.get('kind') == 'CANDIDATE_CITATION_COMPARISON':
                        for finding_id in row['findingIds']:
                            local[finding_id]['diagnostics'].append(
                                diagnostic('SELECTED_CITATION_MEMBERSHIP_FAILED', row['id'],
                                           row.get('origin', {}).get('pointer', '')))
                    elif _required_original_row(row):
                        local['PC_INPUTS_IMMUTABLE']['diagnostics'].append(
                            diagnostic('SELECTED_ORIGINAL_REQUIREMENT_FAILED', row['id'],
                                       row.get('origin', {}).get('pointer', '')))
                    elif (row.get('kind') in closure_graph.TYPED_OCCURRENCE_KINDS
                          and row.get('edgeClass') in {'COMPARISON_VALUE', 'SOURCE_SHAPE',
                                                      'CONDITIONAL', 'SELECTION_GUARD'}):
                        for finding_id in row['findingIds']:
                            local[finding_id]['diagnostics'].append(
                                diagnostic({'SOURCE_SHAPE': 'SELECTED_SOURCE_SHAPE_FAILED',
                                            'COMPARISON_VALUE': 'SELECTED_SOURCE_COMPARISON_POSITION_FAILED',
                                            'CONDITIONAL': 'SELECTED_SOURCE_CONDITION_FAILED',
                                            'SELECTION_GUARD': 'SELECTED_SOURCE_SELECTION_GUARD_FAILED'}[row['edgeClass']], row['id'],
                                           row.get('origin', {}).get('pointer', '')))
        def add_copy(duty, *ids):
            for id_ in ids:
                fact = facts.get(id_)
                if fact is None:
                    local[duty]['diagnostics'].append(diagnostic('MISSING_OWNED_COPY_PREDICATE', id_))
                    continue
                local[duty]['comparisons'].append(fact)
                if not fact['equal']:
                    local[duty]['diagnostics'].append(diagnostic('COPY_MISMATCH', id_, fact['destinationPointer']))
        def observe_local(duty, code, condition, fields, *, controls=None,
                          dependencies=(), edge_class='COMPARISON_VALUE'):
            if partial_graph is not None:
                return closure_graph.record_local_predicate(
                    partial_graph, bound, duty, code, condition,
                    [{'root': role, 'pointer': path} for role, path in fields],
                    selected_action=action, edge_class=edge_class,
                    controls=controls, additional_dependencies=dependencies)
        def owner_argument_dependencies(owner):
            return [row['id'] for row in partial_graph['requirements']
                    if row.get('kind') in {'CANDIDATE_OWNER_INPUT_OCCURRENCE',
                                          'CANDIDATE_OWNER_CONTROL_OCCURRENCE',
                                          'CANDIDATE_OWNER_INVOCATION_GUARD'}
                    and row.get('origin', {}).get('invocationId') == owner] if partial_graph is not None else []
        def argument_operand(owner, argument_path, field):
            rows = [row for row in partial_graph['requirements']
                    if row.get('kind') == 'CANDIDATE_OWNER_INPUT_OCCURRENCE'
                    and row['origin']['invocationId'] == owner
                    and row['origin']['argumentPath'] == argument_path] if partial_graph is not None else []
            row = rows[0] if len(rows) == 1 else None
            iid = row['inputIds'][0] if row is not None and row['disposition'] == 'PASS' and len(row['inputIds']) == 1 else None
            return {'inputId': iid, 'pointer': field}, [row['id']] if row is not None else []
        def check(duty, code, condition, path='', detail=None, *, fields=None,
                  controls=None, dependencies=()):
            if fields is not None:
                observe_local(duty, code, condition, fields, controls=controls, dependencies=dependencies)
            if not condition:
                local[duty]['diagnostics'].append(diagnostic(code, detail or code, path))
        def compare(duty, code, source, sp, destination, dp, optional=False):
            a, av = _present(source, sp); b, bv = _present(destination, dp)
            okay = a == b and (not a or same(av, bv)) and (optional or a)
            roles = {id(intent): 'EFFECT_INTENT', id(result): 'PROPOSED_RESULT'}
            comparison = {'predicateId': code, 'sourcePointer': sp, 'destinationPointer': dp,
                          'sourcePresent': a, 'destinationPresent': b, 'equal': okay,
                          'disposition': 'PASS' if okay else 'FAIL'}
            for side, document, path, present, value in [('source', source, sp, a, av),
                                                        ('destination', destination, dp, b, bv)]:
                if present:
                    value_digest = digest(value)
                    comparison[side + 'ValueDigest'] = value_digest
                    comparison[side] = {'inputRole': roles[id(document)], 'pointer': path, 'valueDigest': value_digest}
            local[duty]['comparisons'].append(comparison)
            roots = {id(intent): 'effectIntent', id(result): 'proposedAssertion'}
            check(duty, code, okay, dp, fields=[(roots[id(source)], sp), (roots[id(destination)], dp)],
                  controls={'optional': optional})
        def record_field_errors(duties, predicate, errors, root, path, code=None):
            for duty in duties:
                observe_local(duty, predicate, not errors, [(root, path)],
                              controls={'errors': errors}, edge_class='SOURCE_SHAPE')
                for error in errors:
                    local[duty]['diagnostics'].append(
                        diagnostic(code or error['code'], root, path + error['pointer'].rstrip('/')))
        if partial_graph is not None:
            boundary_links = closure_graph.materialize_local_observations(
                partial_graph, bound, owner_boundary_observations, selected_action=action)
            _link_observed_invocation_selections(partial_graph, owner_boundary_observations, boundary_links)
            for mapping in source_mapping_observations:
                link = boundary_links.get(mapping['observationId'])
                if link is None:
                    continue
                # A mapping controls only reads of its exact selected original.
                # Unused supplied mappings never become blanket duty links.
                for row in partial_graph['requirements']:
                    if not _required_original_row(row) or row.get('selectedBinding') is None:
                        continue
                    selected_binding = row['selectedBinding']
                    binding_matches = (same(selected_binding, mapping['binding']) or
                        same(selected_binding, {'ref': mapping['binding']['ref'], 'digest': mapping['valueDigest']}))
                    exact_inputs = [iid for iid in row['inputIds']
                                    if bound['pinsById'][iid]['ref'] == mapping['binding']['ref']
                                    and bound['pinsById'][iid]['rawSha256'] == mapping['rawSha256']
                                    and bound['pinsById'][iid].get('wholeJcsDigest') == mapping['valueDigest']]
                    if binding_matches and exact_inputs:
                        row['dependsOn'] = list(dict.fromkeys([*row['dependsOn'], link]))
        body = intent.get('assertionBody') if isinstance(intent.get('assertionBody'), dict) else {}
        add_copy('AR_SCHEMA', 'result.schemaVersion')
        local['AR_SCHEMA']['diagnostics'].extend(components['resultErrors'])
        local['AR_ACTION_PROFILE']['diagnostics'].extend(components['intentErrors'])
        observe_local('AR_SCHEMA', 'RESULT_SCHEMA_VALIDATION', not components['resultErrors'],
                      [('proposedAssertion', '')], edge_class='SOURCE_SHAPE',
                      controls={'schemaId': 'https://ofarm.dev/schema/drafts/non-default/assertion-record-domain-validation/result/v0.1',
                                'errors': components['resultErrors']})
        observe_local('AR_ACTION_PROFILE', 'INTENT_SCHEMA_VALIDATION', not components['intentErrors'],
                      [('effectIntent', '')], edge_class='SOURCE_SHAPE',
                      controls={'selectedAction': action, 'errors': components['intentErrors']})
        for fact in report.get('authorizationSourceComparisons', {}).get('comparisons', []):
            duty = 'AR_ASSERTOR' if fact['predicateId'] == 'AUTHORIZATION_ASSERTOR_MISMATCH' else 'AR_ACTION_PROFILE'
            local[duty]['comparisons'].append(fact)
            if not fact['equal']:
                local[duty]['diagnostics'].append(diagnostic(fact['predicateId'], 'Selected authorization output differs from this domain evaluation.', fact['pointer']))
        if partial_graph is not None:
            closure_graph.materialize_local_observations(partial_graph, bound, authorization_observations,
                                                        selected_action=action)
        add_copy('AR_ACTION_PROFILE', 'intent.schemaVersion')
        add_copy('AR_EFFECT_SUBJECT', 'intent.effectKind', 'intent.effectPosture', 'mapping.id')
        add_copy('AR_ID', 'mapping.id'); add_copy('AR_TYPE', 'result.assertionType')
        add_copy('PC_ACTION_TYPE', 'intent.schemaVersion', 'result.schemaVersion',
                 'intent.effectKind', 'intent.effectPosture', 'result.assertionType')
        add_copy('PC_PENDING_REVIEW', 'result.pending')
        add_copy('AR_SUBJECT', 'mapping.subject'); add_copy('AR_SCOPE', 'mapping.scope')
        check('AR_SCOPE', 'EXACT_ONE_ANCHOR', isinstance(result.get('anchorScopes'), list) and len(result['anchorScopes']) == 1,
              fields=[('proposedAssertion', '/anchorScopes')])
        check('AR_SCOPE', 'EXACT_ONE_RESOURCE', isinstance(intent.get('resources'), list) and len(intent['resources']) == 1,
              fields=[('effectIntent', '/resources')])
        add_copy('AR_SUBJECT_SCOPE_PROOF', 'mapping.subjectScopeProofBindings')
        for gate, duty in [('SUBJECT_SCOPE_RELATION', 'AR_SUBJECT_SCOPE_PROOF'),
                           ('PERFORMER_IDENTITY', 'AR_OPERATION_PERFORMER')]:
            finding = report.get('identitySourceComparisons', {}).get(gate, {})
            local[duty]['comparisons'].extend(finding.get('comparisons', []))
            local[duty]['diagnostics'].extend(finding.get('errors', []))
        add_copy('AR_ASSERTED_AT', 'mapping.assertedAt')
        add_copy('AR_ASSERTION_ACT_POSTURE', 'mapping.assertionActPosture')
        add_copy('AR_ASSERTION_ACT_EVIDENCE', 'mapping.assertionActEvidenceBinding')
        posture = intent.get('assertionActPosture')
        check('AR_ASSERTION_ACT_POSTURE', 'ACT_POSTURE', posture in ['TRUSTED_ONLINE_SUBMISSION', 'VERIFIED_OFFLINE_SUBMISSION'],
              fields=[('effectIntent', '/assertionActPosture')])
        check('AR_ASSERTION_ACT_EVIDENCE', 'ACT_BINDING_PRESENCE',
              ('assertionActEvidenceBinding' in intent) == (posture == 'VERIFIED_OFFLINE_SUBMISSION'),
              fields=[('effectIntent', '/assertionActEvidenceBinding'), ('effectIntent', '/assertionActPosture')])
        if act:
            for duty, field, expected in [('AR_ASSERTOR', 'assertedByPartyRef', act['result']['accountablePartyRef']),
                                           ('AR_ASSERTED_AT', 'assertedAt', act['result']['assertedAt'])]:
                check(duty, 'ACT_RESULT_MISMATCH', result.get(field) == expected, '/' + field,
                      fields=[('proposedAssertion', '/' + field)],
                      controls={'kind': 'RECOMPUTED_OWNER_RESULT', 'owner': 'act', 'valueDigest': digest(expected)},
                      dependencies=owner_argument_dependencies('act'))
        add_copy('AR_SUBJECT_TIME', 'mapping.subjectTime'); add_copy('AR_BODY', 'mapping.assertionBody')
        for role, root in [('intent', 'effectIntent'), ('result', 'proposedAssertion')]:
            record_field_errors(('AR_ASSERTED_AT', 'PC_ASSERTION_ACT'), 'CANONICAL_ASSERTED_AT',
                                components['assertedAtErrors'][role], root, '/assertedAt', 'INVALID_ASSERTED_AT')
            record_field_errors(('AR_SUBJECT_TIME', 'PC_SUBJECT_TIME'), 'SUBJECT_TIME_SHAPE_AND_ORDER',
                                components['subjectTimeErrors'][role], root, '/subjectTime')
        local['AR_BODY']['comparisons'].extend(report.get('contextSourceComparisons', {}).get('comparisons', []))
        local['AR_BODY']['diagnostics'].extend(report.get('contextSourceComparisons', {}).get('errors', []))
        if action != 'ASSERT_OPERATION_CLAIM':
            add_copy('AR_SUBJECT_TIME', 'body.applicability')
        temporal = report.get('temporalSources', {})
        for duty in ('AR_SUBJECT_TIME', 'PC_SUBJECT_TIME'):
            local[duty]['diagnostics'].extend(temporal.get('errors', []))
            local[duty]['comparisons'].extend(temporal.get('comparisons', []))
        if action == 'ASSERT_OPERATION_CLAIM':
            local['AR_OPERATION_PAYLOADS']['diagnostics'].extend(
                e for e in temporal.get('errors', []) if e['code'] == 'PAYLOAD_TIME_BASIS_MISMATCH')
            local['AR_OPERATION_PAYLOADS']['comparisons'].extend(
                c for c in temporal.get('comparisons', []) if c['predicateId'] == 'PAYLOAD_TIME_BASIS_MISMATCH')
        check('AR_BODY', 'EXACT_RENDERED_TEXT', body.get('claimText') == components.get('renderedText') and 'renderedText' in components,
              '/assertionBody/claimText', components.get('renderingError', 'Claim text must equal the exact complete rendering.'),
              fields=[('effectIntent', '/assertionBody/claimText')],
              controls={'kind': 'PINNED_RENDERER_OUTPUT', 'available': 'renderedText' in components,
                        **({'valueDigest': digest(components['renderedText'])} if 'renderedText' in components else {})})
        intrinsic = components.get('intrinsics')
        if intrinsic:
            local['AR_BODY']['diagnostics'].extend(intrinsic['errors'])
            local['AR_BODY']['diagnostics'].extend(components.get('outerBindingErrors', []))
            observe_local('AR_BODY', 'PROPOSITION_INTRINSIC_VALIDATION', not intrinsic['errors'],
                          [('effectIntent', '/assertionBody/proposition')],
                          controls={'errors': intrinsic['errors']}, edge_class='SOURCE_SHAPE')
        else:
            check('AR_BODY', 'MISSING_PROPOSITION', False, '/assertionBody/proposition',
                  fields=[('effectIntent', '/assertionBody/proposition')])
        add_copy('AR_EVIDENCE', 'mapping.evidenceBindings'); add_copy('AR_CLAIM_STATE', 'result.pending')
        local['AR_EVIDENCE']['diagnostics'].extend(components.get('referenceInventory', {}).get('errors', []))
        local['AR_EVIDENCE']['comparisons'].extend(report.get('evidenceSourceComparisons', {}).get('comparisons', []))
        local['AR_EVIDENCE']['diagnostics'].extend(e for e in report.get('evidenceSourceComparisons', {}).get('errors', [])
            if e not in local['AR_EVIDENCE']['diagnostics'])
        check('AR_EVIDENCE', 'NONEMPTY_EVIDENCE', isinstance(intent.get('evidenceBindings'), list) and bool(intent['evidenceBindings']),
              fields=[('effectIntent', '/evidenceBindings')])
        check('AR_EVENT_ASSOCIATION', 'EVENT_TRACE_ONLY', 'associatedSemanticEventBinding' not in result and 'primaryEventFamily' not in result,
              fields=[('proposedAssertion', '/associatedSemanticEventBinding')]
                     + ([('proposedAssertion', '/primaryEventFamily')] if 'associatedSemanticEventBinding' not in result else []))
        local['AR_EVENT_ASSOCIATION']['comparisons'].extend(report.get('eventSourceComparisons', {}).get('comparisons', []))
        local['AR_EVENT_ASSOCIATION']['diagnostics'].extend(report.get('eventSourceComparisons', {}).get('errors', []))
        if associated is not None:
            check('AR_EVENT_ASSOCIATION', 'INTENDED_EVENT_PROHIBITED', intent.get('claimPosture') != 'INTENDED',
                  fields=[('effectIntent', '/associatedSemanticEventBinding'), ('effectIntent', '/claimPosture')])
        if action == 'ASSERT_OPERATION_CLAIM':
            add_copy('AR_OPERATION_POSTURE', 'mapping.claimPosture')
            for document, root, posture_path in [(intent, 'effectIntent', '/claimPosture'),
                                                 (result, 'proposedAssertion', '/operationClaimContext/claimPosture')]:
                _, claim_posture = _present(document, posture_path)
                _, profile = _present(document, '/subjectTime/profile')
                matches = ((claim_posture == 'INTENDED' and profile == 'INTENDED_WINDOW') or
                           (claim_posture == 'PERFORMED' and profile in ('PERFORMED_INSTANT', 'PERFORMED_INTERVAL')))
                for duty in ('AR_OPERATION_POSTURE', 'AR_SUBJECT_TIME', 'PC_SUBJECT_TIME'):
                    check(duty, 'OPERATION_POSTURE_TIME_PROFILE', matches, '/subjectTime/profile', root,
                          fields=[(root, posture_path), (root, '/subjectTime/profile')])
            body_time_compared = any(c['predicateId'] == 'BODY_TIME_BASIS_MISMATCH' for c in temporal.get('comparisons', []))
            for document in (intent, result):
                _, kind = _present(document, '/assertionBody/temporalBasis/sourceKind')
                if kind == 'BODY_TIME' and (document is result or not body_time_compared):
                    for duty in ('AR_SUBJECT_TIME', 'PC_SUBJECT_TIME'):
                        compare(duty, 'BODY_TIME_BASIS_MISMATCH', document, '/subjectTime',
                                document, '/assertionBody/temporalBasis/time')
            add_copy('AR_OPERATION_PERFORMER', 'mapping.performedByPartyRef', 'body.performerRef')
            add_copy('AR_OPERATION_AGENT_ACTORSHIP', 'mapping.softwareAgentActorshipBindings')
            add_copy('AR_OPERATION_PERFORMER_AUTHORITY', 'mapping.performerAuthorityEvidenceBindings')
            agent_required = intent.get('claimPosture') == 'PERFORMED' and body.get('allegesSoftwareAgentPerformance') is True
            check('AR_OPERATION_AGENT_ACTORSHIP', 'AGENT_EVIDENCE_PRESENCE', ('softwareAgentActorshipBindings' in intent) == agent_required,
                  fields=[('effectIntent', '/softwareAgentActorshipBindings'), ('effectIntent', '/claimPosture')]
                         + ([('effectIntent', '/assertionBody/allegesSoftwareAgentPerformance')] if intent.get('claimPosture') == 'PERFORMED' else []))
            if not agent_required:
                dependency('AGENT_ACTORSHIP', 'NOT_APPLICABLE', 'Performed software-agent allegation is absent.')
            if 'performerAuthorityEvidenceBindings' not in intent:
                dependency('PERFORMER_AUTHORITY_EVIDENCE', 'NOT_APPLICABLE', 'Optional performer-authority evidence is absent.')
            check('AR_OPERATION_PERFORMER_AUTHORITY', 'INTENDED_PERFORMER_AUTHORITY_ABSENCE', intent.get('claimPosture') != 'INTENDED' or 'performerAuthorityEvidenceBindings' not in intent,
                  fields=[('effectIntent', '/claimPosture')]
                         + ([('effectIntent', '/performerAuthorityEvidenceBindings')] if intent.get('claimPosture') == 'INTENDED' else []))
            report['operationPerformerAuthorityDisposition'] = 'NOT_EVALUATED_BY_AUTHORIZATION'
            for field in ['interventionIntentPayloadBindings', 'executionRecordPayloadBindings']:
                compare('AR_OPERATION_PAYLOADS', 'body.' + field, intent, '/assertionBody/' + field,
                        result, '/assertionBody/' + field, True)
                for role, root in [('intent', 'effectIntent'), ('result', 'proposedAssertion')]:
                    errors = components['operationPayloadErrors'][role].get(field)
                    if errors is not None:
                        record_field_errors(('AR_OPERATION_PAYLOADS',), 'TYPED_PAYLOAD_BINDINGS', errors,
                                            root, '/assertionBody/' + field, 'INVALID_PAYLOAD_BINDING')
        if action == 'ASSERT_COMPLIANCE':
            add_copy('AR_COMPLIANCE_RULES', 'mapping.ruleRevisionBindings')
            add_copy('AR_COMPLIANCE_EVIDENCE_POLICY', 'mapping.evidencePolicyRevisionBindings')
            for gate, duty in [('COMPLIANCE_RULE_SELECTION', 'AR_COMPLIANCE_RULES'),
                               ('EVIDENCE_POLICY_SELECTION', 'AR_COMPLIANCE_EVIDENCE_POLICY')]:
                finding = report.get('complianceSourceComparisons', {}).get(gate, {})
                local[duty]['comparisons'].extend(finding.get('comparisons', []))
                local[duty]['diagnostics'].extend(finding.get('errors', []))
        add_copy('AR_CORRECTION_LINEAGE', 'mapping.supersedesAssertionRecordBinding')
        correction = body.get('assertionPosture') == 'CORRECTION'
        check('AR_CORRECTION_LINEAGE', 'CORRECTION_BINDING_PRESENCE', ('supersedesAssertionRecordBinding' in intent) == correction,
              fields=[('effectIntent', '/supersedesAssertionRecordBinding'), ('effectIntent', '/assertionBody/assertionPosture')])
        if not correction:
            dependency('PRIOR_ASSERTION_CONTEXT', 'NOT_APPLICABLE', 'Initial assertion has no prior correction target.')
        elif state and state_context and 'priorAssertion' in state_context:
            prior_spec = state_context['priorAssertion']['record']
            prior = parse(owner_inputs['state']['records'][prior_spec['binding']['ref']])
            prior_checks = component_calls.invoke(intent, result, action, [], prior=prior)
            errors = list(prior_checks['priorErrors'])
            prior_comparisons = []
            if partial_graph is not None:
                prior_operand, prior_links = argument_operand('state', ['records', prior_spec['binding']['ref']], '')
                prior_operand['valueDigest'] = digest(prior)
                context_operand, context_links = argument_operand('state', ['context_bytes'], '/priorAssertion/record/binding')
                context_operand['valueDigest'] = digest(prior_spec['binding'])
                closure_graph.record_local_predicate(partial_graph, bound, 'AR_CORRECTION_LINEAGE',
                    'PRIOR_ASSERTION_SCHEMA_VALIDATION', not prior_checks['priorErrors'], [prior_operand, context_operand],
                    selected_action=action, edge_class='SOURCE_SHAPE',
                    additional_dependencies=prior_links + context_links,
                    controls={'errors': prior_checks['priorErrors']})
            def prior_compare(code, path):
                before_present, before = _present(prior, path)
                after_present, after = _present(result, path)
                if partial_graph is not None:
                    operand, links = argument_operand('state', ['records', prior_spec['binding']['ref']], path)
                    if before_present:
                        operand['valueDigest'] = digest(before)
                    closure_graph.record_local_predicate(partial_graph, bound, 'AR_CORRECTION_LINEAGE', code,
                        before_present and after_present and same(before, after),
                        [operand, {'root': 'proposedAssertion', 'pointer': path}],
                        selected_action=action, additional_dependencies=links)
                if not before_present or not after_present:
                    return False
                equal = same(before, after)
                prior_comparisons.append({'predicateId': code,
                    'source': {'inputRole': 'PRIOR_ASSERTION', 'pointer': path, 'valueDigest': digest(before)},
                    'destination': {'inputRole': 'PROPOSED_RESULT', 'pointer': path, 'valueDigest': digest(after)},
                    'disposition': 'PASS' if equal else 'FAIL'})
                return equal
            prior_binding_equal = same(intent.get('supersedesAssertionRecordBinding'), prior_spec['binding'])
            if partial_graph is not None:
                closure_graph.record_local_predicate(partial_graph, bound, 'AR_CORRECTION_LINEAGE',
                    'PRIOR_SELECTION_MISMATCH', prior_binding_equal,
                    [{'root': 'effectIntent', 'pointer': '/supersedesAssertionRecordBinding'}, context_operand],
                    selected_action=action, additional_dependencies=context_links)
            if not prior_binding_equal:
                errors.append(diagnostic('PRIOR_SELECTION_MISMATCH', 'Exact bound prior record differs.'))
            for field in ['assertionType', 'anchorScopes']:
                if not prior_compare('PRIOR_' + field.upper() + '_MISMATCH', '/' + field):
                    errors.append(diagnostic('PRIOR_' + field.upper() + '_MISMATCH', field))
            for field in ['subjectType', 'subjectRef']:
                if not prior_compare('PRIOR_LOGICAL_SUBJECT_' + field, '/subject/' + field):
                    errors.append(diagnostic('PRIOR_LOGICAL_SUBJECT_MISMATCH', field))
            report['correctionContext'] = {
                'transactionSnapshot': state_context['attempt']['transactionSnapshot'],
                'priorRecord': {'ref': prior_spec['binding']['ref'], 'digest': digest(prior)},
                'priorCreationEvidence': state_context['priorAssertion']['creationEvidence']['binding'],
                'governanceBoundaryDigest': digest(state_context['governanceContext']),
                'twinPosture': state_context['governanceContext']['twin']['posture'],
                'comparisons': prior_comparisons}
            dependency('PRIOR_ASSERTION_CONTEXT', 'FAIL' if errors else 'PASS',
                       'Concrete state owner checked positive prior visibility and creation boundary/twin; domain checks exact subtype, anchor and logical subject.', errors)
        for duty, forbidden in [
            ('AR_STRUCTURE_BRANCH_ABSENCE', ['operationClaimContext', 'complianceBasis']),
            ('AR_OPERATION_BRANCH_ABSENCE', ['complianceBasis']),
            ('AR_COMPLIANCE_BRANCH_ABSENCE', ['operationClaimContext'])]:
            branch = {'AR_STRUCTURE_BRANCH_ABSENCE': 'ASSERT_STRUCTURE', 'AR_OPERATION_BRANCH_ABSENCE': 'ASSERT_OPERATION_CLAIM',
                      'AR_COMPLIANCE_BRANCH_ABSENCE': 'ASSERT_COMPLIANCE'}[duty]
            if action == branch:
                for field in forbidden:
                    check(duty, 'INAPPLICABLE_BRANCH_MEMBER', field not in result, '/' + field,
                          fields=[('proposedAssertion', '/' + field)])
        legacy = ['benefitingPartyRef', 'supersedesAssertionRecordRef', 'supersededByReviewDecisionRef', 'notes',
                  'eventTime', 'occurrenceTime', 'effectiveFrom', 'effectiveUntil', 'performedAt', 'provenanceRefs', 'payloadRefs']
        for field in legacy:
            check('AR_LEGACY_ABSENCE', 'LEGACY_MEMBER', field not in result, '/' + field,
                  fields=[('proposedAssertion', '/' + field)])
        compare('PC_TEMPORAL_SEPARATION', 'temporal.assertedAt', intent, '/assertedAt', result, '/assertedAt')
        compare('PC_TEMPORAL_SEPARATION', 'temporal.subjectTime', intent, '/subjectTime', result, '/subjectTime')
        for field in ['writeAuthorizationCheckedAt', 'effectCommittedAt', 'humanActedAt', 'authorizationEvaluatedAt',
                      'capturedAt', 'checkpoint', 'consumedAt']:
            check('PC_TEMPORAL_SEPARATION', 'LATER_TRANSACTION_FIELD', field not in result, '/' + field,
                  fields=[('proposedAssertion', '/' + field)])

        local['AR_BODY']['diagnostics'].extend(report.get('automaticSourceComparisons', {}).get('errors', []))
        na = {}
        for prefix, branch in [('AR_OPERATION_', 'ASSERT_OPERATION_CLAIM'), ('AR_COMPLIANCE_', 'ASSERT_COMPLIANCE')]:
            for duty in ordered:
                if duty.startswith(prefix) and action != branch:
                    na[duty] = 'Selected action is ' + action + '.'
        for duty, branch in [('AR_STRUCTURE_BRANCH_ABSENCE', 'ASSERT_STRUCTURE'), ('PC_STRUCTURE', 'ASSERT_STRUCTURE'),
                             ('PC_OPERATION', 'ASSERT_OPERATION_CLAIM'), ('PC_COMPLIANCE', 'ASSERT_COMPLIANCE')]:
            if action != branch:
                na[duty] = 'Selected action is ' + action + '.'
        if associated is None and 'event' not in owner_inputs:
            na['AR_EVENT_ASSOCIATION'] = na['PC_EVENT_ASSOCIATION'] = 'No event association is declared.'
        findings = {}
        def evaluate(duty):
            if duty in findings:
                return findings[duty]
            item = {'id': duty, **local[duty]}
            # Independent failures take precedence over both dependencies and NA.
            if item['diagnostics']:
                item['disposition'] = 'FAIL'
            elif duty in na:
                item.update(disposition='NOT_APPLICABLE', branchReason=na[duty])
            else:
                unmet = []
                for dep in PREREQUISITES[duty]:
                    value = evaluate(dep) if dep in PREREQUISITES else dependencies[dep]
                    if value['disposition'] not in ['PASS', 'NOT_APPLICABLE']:
                        unmet.append(dep)
                if unmet:
                    item.update(disposition='NOT_EVALUATED', failedPrerequisites=unmet)
                else:
                    item['disposition'] = 'PASS'
            findings[duty] = item
            return item
        for duty in ordered:
            evaluate(duty)
        report['mappingFindings'] = [findings[d] for d in ordered if d.startswith('AR_')]
        report['postconditionFindings'] = [findings[d] for d in ordered if d.startswith('PC_')]
        if partial_graph is not None:
            from c3_dependency_coverage import occurrence_fixed_point
            partial_graph['knownOccurrenceFixedPoint'] = occurrence_fixed_point(
                partial_graph['requirements'], partial_graph['uses'])
            closure_graph.refresh_known_finding_attribution(partial_graph,
                report['mappingFindings'] + report['postconditionFindings'])
        report['dependencyFindings'] = list(dependencies.values())
        passing_owners = [kind for kind, gate in [('act', 'ASSERTION_ACT'), ('event', 'EVENT_OWNER'), ('state', 'PROTECTED_PROPOSED_STATE'), ('authorization', 'SELECTED_AUTHORIZATION_PATH')]
                          if dependencies[gate]['disposition'] == 'PASS']
        # A failed domain binding does not erase schema-checked original owner
        # evidence from a FAIL payload. This does not promote the failed gate.
        if report.get('ownerReports', {}).get('authorization', {}).get('disposition') == 'PASS' and 'authorization' not in passing_owners:
            passing_owners.append('authorization')
        if report.get('ownerReports', {}).get('event', {}).get('status') == 'CONDITIONAL_CONFORMANCE_PASS' and 'event' not in passing_owners:
            passing_owners.append('event')
        if state and report.get('ownerReports', {}).get('state', {}).get('status') == 'CONDITIONAL_CONFORMANCE_PASS' and 'state' not in passing_owners:
            # The exact owner evidence remains visible after the independent
            # domain obligation gate is downgraded. This is no source admission.
            passing_owners.append('state')
        unresolved_owner_inputs = []
        report['resolvedOwnerInputs'] = payload_inputs.collect(owner_inputs, passing_owners,
            report.get('ownerReports', {}).get('occupancy'), unresolved_owner_inputs)
        report.setdefault('sourceTrace', {'resolvedInputs': [], 'unresolvedInputs': []})['unresolvedInputs'].extend(unresolved_owner_inputs)
        report['resolvedDomainInputs'] = report.get('sourceTrace', {}).get('resolvedInputs', [])
        report['failedDependencyIds'] = [item['id'] for item in dependencies.values()
                                         if item['disposition'] == 'FAIL']
        report['status'] = ('FAIL' if report['failedDependencyIds']
                            or any(f['disposition'] == 'FAIL' for f in findings.values())
                            else 'DEPENDENCY_UNAVAILABLE')
        if selection is not None:
            report['payloadUnavailableReason'] = ('Complete v0.3 immutable-input closure and independent protected-state '
                                                  'obligation comparison are not established; the v0.4 public payload is withheld.')
        else:
            report['payloadUnavailableReason'] = 'Full payload identity bindings require the original independently pinned evaluation selection; no foreign binding is invented.'
        report['next'] = 'Close the named owner interfaces in separate prerequisites and finish remaining domain source-role predicates; then review and verify the complete public payload.'
        _validate_report(report)
        return report
    except (InputError, ValueError, TypeError, KeyError, OSError, importlib.metadata.PackageNotFoundError) as exc:
        if report.get('partialRequirementGraph') is not None:
            try:
                from original_inputs import bind_roots
                prefix_bound = bind_roots(owner_inputs['evaluationSelection'], inventory,
                    original_intent_bytes, original_result_bytes,
                    selected_state_context=graph_state_context,
                    original_bytes=owner_inputs.get('originals', {}))
                _preserve_interrupted_callsite_prefix(report['partialRequirementGraph'], prefix_bound,
                    owner_attempts, original_intent_bytes,
                    [owner_boundary_observations, authorization_observations], action)
            except (InputError, ValueError, TypeError, KeyError, OSError) as trace_error:
                report['partialRequirementGraph']['actualCallSitePrefix'] = {
                    'status': 'INTERRUPTED_PREFIX_PROVENANCE_UNAVAILABLE',
                    'reason': str(trace_error)[:400], 'findingEvaluationComplete': False}
        report['errors'].append(diagnostic('INPUT_OR_PACKAGE_ERROR', exc))
        report['next'] = 'Supply exact original inputs and the independently pinned local construction package.'
        _validate_report(report)
        return report


def _validate_report(report):
    from jsonschema import Draft202012Validator
    errors = list(Draft202012Validator(REPORT_SCHEMA).iter_errors(report))
    if errors:
        raise RuntimeError('Internal construction report schema failure: ' + errors[0].message)
