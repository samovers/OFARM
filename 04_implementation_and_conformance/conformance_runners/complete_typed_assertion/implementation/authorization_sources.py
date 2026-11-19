"""Domain comparisons against a recomputed selected authorization output.

The separate owner verifies its original-byte graph. These comparisons bind
that graph to this domain invocation. They do not evaluate eligibility,
candidate completeness, canonical selection, principal trust or permission.
"""
from pathlib import Path
from strict_inputs import parse, sha, digest, same, pointer

HERE = Path(__file__).resolve().parent


def compare(inputs, original_intent_bytes, result, action, selection, *, observations=None):
    # This optional internal queue records the same executed comparisons. It
    # cannot select sources, change rules or supply an owner verdict.
    owner_guard = observations[-1]['id'] if observations else None
    selection_ids = []
    reader_rule = ({'kind': 'EXACT_READER_MODULE_BYTES', 'module': 'authorization_sources.py', 'moduleRawSha256': sha(Path(__file__).read_bytes()),
             'predicate': 'compare'} if observations is not None else None)

    def operand(argument, path, value, *, present=True):
        return {'owner': 'authorization', 'argumentPath': argument, 'pointer': path,
                'present': present, **({'valueDigest': digest(value)} if present else {})}

    def root_operand(root, path, value, *, present=True):
        return {'root': root, 'pointer': path, 'present': present,
                **({'valueDigest': digest(value)} if present else {})}

    def emit(code, outcome, operands=(), *, controls=None, rules=(), guard=False, dependencies=None):
        if observations is None:
            return None
        iid = 'authorization-local:' + str(len(observations))
        observations.append({'id': iid, 'predicate': code, 'outcome': bool(outcome),
            'edgeClass': 'SELECTION_GUARD' if guard else 'COMPARISON_VALUE',
            'findingIds': ['AR_ASSERTOR' if code == 'AUTHORIZATION_ASSERTOR_MISMATCH' else 'AR_ACTION_PROFILE'],
            'ownerInvocationId': 'authorization', 'operands': list(operands),
            'controls': controls, 'rule': reader_rule, 'ruleOperands': list(rules),
            'dependsOn': ([owner_guard] if owner_guard else []) + list(
                selection_ids if dependencies is None else dependencies)})
        return iid

    context = parse(inputs['context_bytes']); profile = parse(inputs['profile_bytes'])
    catalog, catalog_indexes = {}, {}
    for index, entry in enumerate(context['sources']):
        key = entry['key']
        catalog[key] = entry
        catalog_indexes[key] = index
        event = emit('AUTHORIZATION_CATALOG_KEY', True,
                     [operand(['context_bytes'], '/sources/' + str(index) + '/key', key)],
                     controls={'sourceIndex': index}, guard=True)
        if event is not None:
            selection_ids.append(event)
    evidence = parse(inputs['evidence_bytes'])
    errors, comparisons = [], []

    def check(code, actual, expected, path, source=None, destination=None, *,
              operands=(), controls=None, rules=()):
        equal = same(actual, expected)
        fact = {'predicateId': code, 'pointer': path, 'equal': equal,
                'actualValueDigest': digest(actual), 'expectedValueDigest': digest(expected)}
        if source is not None and destination is not None:
            fact.update(source={**source, 'valueDigest': digest(actual)},
                        destination={**destination, 'valueDigest': digest(expected)},
                        disposition='PASS' if equal else 'FAIL')
        comparisons.append(fact)
        emit(code, equal, operands, controls=controls, rules=rules)
        if not equal:
            errors.append({'code': code, 'pointer': path})

    def core(role):
        key = context['coreSources'][role]; entry = catalog[key]
        raw = inputs['source_bytes'][key]
        source_format = profile['formats'][entry['formatId']]
        document = parse(raw)
        projected = pointer(document, source_format['projectionPointer'])
        escaped = entry['formatId'].replace('~', '~0').replace('/', '~1')
        event = emit('AUTHORIZATION_CORE_SOURCE_' + role, True, [
            operand(['context_bytes'], '/coreSources/' + role, key),
            operand(['context_bytes'], '/sources/' + str(catalog_indexes[key]) + '/formatId', entry['formatId']),
            operand(['profile_bytes'], '/formats/' + escaped + '/projectionPointer', source_format['projectionPointer']),
            operand(['source_bytes', key], source_format['projectionPointer'], projected)],
            controls={'sourceKey': key, 'formatId': entry['formatId'], 'sourceRawSha256': sha(raw)}, guard=True)
        if event is not None:
            selection_ids.append(event)
        return entry, raw, projected

    def source_location(role, suffix):
        key = context['coreSources'][role]
        selected_format = profile['formats'][catalog[key]['formatId']]
        return {'inputRole': 'authorization:source:' + key,
                'pointer': selected_format['projectionPointer'] + suffix}

    def source_operand(role, suffix, value):
        location = source_location(role, suffix)
        return operand(['source_bytes', context['coreSources'][role]], location['pointer'], value)

    def selected_control(path, value):
        return {'kind': 'INDEPENDENTLY_PINNED_EVALUATION_SELECTION', 'pointer': path,
                'valueDigest': digest(value)}

    intent_entry, intent_raw, _ = core('EFFECT_INTENT')
    result_entry, result_raw, output = core('RESULT')
    _, _, rule = core('RULE')
    check('AUTHORIZATION_ORIGINAL_INTENT_BYTES_MISMATCH', sha(intent_raw), sha(original_intent_bytes), '/EFFECT_INTENT',
          operands=[operand(['source_bytes', context['coreSources']['EFFECT_INTENT']], '', parse(intent_raw)),
                    root_operand('effectIntent', '', parse(original_intent_bytes))],
          controls={'kind': 'EXACT_ORIGINAL_BYTE_COMPARISON', 'sourceRawSha256': sha(intent_raw),
                    'intentRawSha256': sha(original_intent_bytes)})
    check('AUTHORIZATION_ACTION_MISMATCH', context['selectedActionClass'], action, '/selectedActionClass',
          operands=[operand(['context_bytes'], '/selectedActionClass', context['selectedActionClass'])],
          controls={'kind': 'SELECTED_PACKAGE_ACTION', 'selectedAction': action})
    check('AUTHORIZATION_ASSERTOR_MISMATCH', result.get('assertedByPartyRef'), output['selectedPath']['authoritySubjectPartyRef'], '/assertedByPartyRef',
          {'inputRole': 'PROPOSED_RESULT', 'pointer': '/assertedByPartyRef'},
          source_location('RESULT', '/selectedPath/authoritySubjectPartyRef'),
          operands=[root_operand('proposedAssertion', '/assertedByPartyRef', result.get('assertedByPartyRef'),
                                 present='assertedByPartyRef' in result),
                    source_operand('RESULT', '/selectedPath/authoritySubjectPartyRef', output['selectedPath']['authoritySubjectPartyRef'])])
    branch = {'ASSERT_STRUCTURE': 'structure', 'ASSERT_OPERATION_CLAIM': 'operation', 'ASSERT_COMPLIANCE': 'compliance'}[action]
    schema_raw = (HERE / 'outer/carriers' / (branch + '-intent.schema.json')).read_bytes()
    schema = parse(schema_raw)
    schema_path = 'outer/carriers/' + branch + '-intent.schema.json'
    schema_rule = {'localPath': schema_path, 'rawSha256': sha(schema_raw)}
    schema_id_rule = {**schema_rule, 'pointer': '/$id', 'valueDigest': digest(schema['$id'])}
    schema_event = emit('AUTHORIZATION_SELECTED_DOMAIN_SCHEMA', True, controls={
        'kind': 'SELECTED_PACKAGE_ACTION', 'selectedAction': action, 'branch': branch},
        rules=[schema_id_rule], guard=True)
    if schema_event is not None:
        selection_ids.append(schema_event)
    expected_schema = {'schemaId': schema['$id'], 'schemaVersion': parse(original_intent_bytes)['schemaVersion'],
                       'schemaDigest': 'sha256:' + sha(schema_raw)}
    check('AUTHORIZATION_DOMAIN_SCHEMA_MISMATCH', rule['intentSchema'], expected_schema, '/RULE/intentSchema',
          operands=[source_operand('RULE', '/intentSchema', rule['intentSchema']),
                    root_operand('effectIntent', '/schemaVersion', expected_schema['schemaVersion'])],
          controls={'kind': 'CONSTRUCTED_SCHEMA_BINDING', 'valueDigest': digest(expected_schema)}, rules=[schema_id_rule])
    for source_key, contract_key in [('schemaId', 'schemaRef'), ('schemaVersion', 'schemaVersion'), ('schemaDigest', 'schemaDigest')]:
        check('AUTHORIZATION_DOMAIN_SCHEMA_FIELD_' + source_key, rule['intentSchema'][source_key], expected_schema[source_key],
              '/RULE/intentSchema/' + source_key, source_location('RULE', '/intentSchema/' + source_key),
              {'inputRole': 'DOMAIN_CONTRACT', 'pointer': '/actions/' + action + '/intentSchemaBinding/' + contract_key},
              operands=[source_operand('RULE', '/intentSchema/' + source_key, rule['intentSchema'][source_key])] +
                  ([root_operand('effectIntent', '/schemaVersion', expected_schema['schemaVersion'])] if source_key == 'schemaVersion' else []),
              controls={'kind': 'PACKAGE_SCHEMA_RAW_DIGEST', 'rawSha256': sha(schema_raw)} if source_key == 'schemaDigest' else None,
              rules=[schema_id_rule] if source_key == 'schemaId' else [schema_rule] if source_key == 'schemaDigest' else [])
    # The selected profile must use the complete domain intent schema and bytes,
    # even if another permissive foreign format also validated the same object.
    format_ = profile['formats'][intent_entry['formatId']]
    escaped_format = intent_entry['formatId'].replace('~', '~0').replace('/', '~1')
    check('AUTHORIZATION_INTENT_FORMAT_MISMATCH', format_['schemaId'], schema['$id'], '/EFFECT_INTENT/format',
          {'inputRole': 'authorization:profile', 'pointer': '/formats/' + escaped_format + '/schemaId'},
          {'inputRole': 'DOMAIN_CONTRACT', 'pointer': '/actions/' + action + '/intentSchemaBinding/schemaRef'},
          operands=[operand(['profile_bytes'], '/formats/' + escaped_format + '/schemaId', format_['schemaId'])],
          rules=[schema_id_rule])
    selected_event = emit('AUTHORIZATION_EVALUATION_SELECTION_PRESENT', selection is not None,
                          controls={'selectionPresent': selection is not None}, guard=True)
    if selection is not None:
        if selected_event is not None:
            selection_ids.append(selected_event)
        intent_index = catalog_indexes[context['coreSources']['EFFECT_INTENT']]
        result_index = catalog_indexes[context['coreSources']['RESULT']]
        check('AUTHORIZATION_EVALUATION_INTENT_SELECTION_MISMATCH', selection['effectIntent'], intent_entry['binding'], '/selection/effectIntent',
              operands=[operand(['context_bytes'], '/sources/' + str(intent_index) + '/binding', intent_entry['binding'])],
              controls=selected_control('/effectIntent', selection['effectIntent']))
        check('AUTHORIZATION_EVALUATION_RESULT_SELECTION_MISMATCH', selection['authorizationResult'],
              {'ref': result_entry['binding']['ref'], 'digest': digest(parse(result_raw))}, '/selection/authorizationResult',
              operands=[operand(['context_bytes'], '/sources/' + str(result_index) + '/binding/ref', result_entry['binding']['ref']),
                        operand(['source_bytes', context['coreSources']['RESULT']], '', parse(result_raw))],
              controls=selected_control('/authorizationResult', selection['authorizationResult']))
        rule_binding = output['ruleBinding']
        expected_rule = {'ruleId': output['selectedRuleId'], 'ruleRef': rule_binding['ref'],
                         'ruleRevisionSelector': {k: v for k, v in rule_binding.items() if k != 'ref'},
                         'ruleDigest': output['ruleDigest']}
        check('AUTHORIZATION_EVALUATION_RULE_SELECTION_MISMATCH', selection['currentActionRuleBinding'], expected_rule, '/selection/currentActionRuleBinding',
              operands=[source_operand('RESULT', '/selectedRuleId', output['selectedRuleId']),
                        source_operand('RESULT', '/ruleBinding', rule_binding),
                        source_operand('RESULT', '/ruleDigest', output['ruleDigest'])],
              controls={**selected_control('/currentActionRuleBinding', selection['currentActionRuleBinding']),
                        'constructedExpectedValueDigest': digest(expected_rule)})
        for field, source_pointer in [('ruleId', '/selectedRuleId'), ('ruleRef', '/ruleBinding/ref'), ('ruleDigest', '/ruleDigest')]:
            check('AUTHORIZATION_SELECTED_RULE_FIELD_' + field, selection['currentActionRuleBinding'][field], expected_rule[field],
                  '/selection/currentActionRuleBinding/' + field,
                  {'inputRole': 'domain:evaluationSelection', 'pointer': '/currentActionRuleBinding/' + field},
                  source_location('RESULT', source_pointer),
                  operands=[source_operand('RESULT', source_pointer, expected_rule[field])],
                  controls=selected_control('/currentActionRuleBinding/' + field, selection['currentActionRuleBinding'][field]))
        for key, value in expected_rule['ruleRevisionSelector'].items():
            escaped_key = key.replace('~', '~0').replace('/', '~1')
            member_event = emit('AUTHORIZATION_SELECTED_RULE_SELECTOR_PRESENT_' + key,
                key in selection['currentActionRuleBinding']['ruleRevisionSelector'],
                [source_operand('RESULT', '/ruleBinding', rule_binding)],
                controls=selected_control('/currentActionRuleBinding/ruleRevisionSelector', selection['currentActionRuleBinding']['ruleRevisionSelector']),
                guard=True)
            if key in selection['currentActionRuleBinding']['ruleRevisionSelector']:
                check('AUTHORIZATION_SELECTED_RULE_SELECTOR_' + key, selection['currentActionRuleBinding']['ruleRevisionSelector'][key], value,
                      '/selection/currentActionRuleBinding/ruleRevisionSelector/' + key,
                      {'inputRole': 'domain:evaluationSelection', 'pointer': '/currentActionRuleBinding/ruleRevisionSelector/' + key},
                      source_location('RESULT', '/ruleBinding/' + key),
                      operands=[source_operand('RESULT', '/ruleBinding/' + escaped_key, value)],
                      controls={**selected_control('/currentActionRuleBinding/ruleRevisionSelector/' + escaped_key,
                                                   selection['currentActionRuleBinding']['ruleRevisionSelector'][key]),
                                'applicabilityEventId': member_event})
                if observations is not None:
                    observations[-1]['dependsOn'].append(member_event)
    emit('AUTHORIZATION_RETURNED_SOURCE_FIELDS', True, [
        source_operand('RESULT', '/selectedPath/authoritySubjectPartyRef', output['selectedPath']['authoritySubjectPartyRef']),
        source_operand('RESULT', '/selectedPath/authoritySubjectBasis', output['selectedPath']['authoritySubjectBasis']),
        source_operand('RESULT', '', output), operand(['evidence_bytes'], '/selectedPath', evidence['selectedPath']),
        operand(['profile_bytes'], '/selectedPathTypes', profile['selectedPathTypes']),
        operand(['context_bytes'], '/sources/' + str(catalog_indexes[context['coreSources']['RESULT']]) + '/binding', result_entry['binding']),
        operand(['context_bytes'], '/profileBinding', context['profileBinding']),
        operand(['context_bytes'], '/sourceOrigin', context['sourceOrigin'])], guard=True)
    return {'disposition': 'FAIL' if errors else 'PASS', 'errors': errors, 'comparisons': comparisons,
            'scope': 'SELECTED_OWNER_OUTPUT_DOMAIN_BINDING_ONLY',
            'authoritySubjectPartyRef': output['selectedPath']['authoritySubjectPartyRef'],
            'authoritySubjectBasis': output['selectedPath']['authoritySubjectBasis'],
            'selectedPath': evidence['selectedPath'],
            'completeSelectedOwnerOutput': output,
            'selectedPathTypesWithinProfile': profile['selectedPathTypes'],
            'authorizationResultBinding': result_entry['binding'],
            'sourceInputIds': ['authorization:context', 'authorization:profile',
                               *('authorization:source:' + context['coreSources'][role] for role in ['EFFECT_INTENT', 'RESULT', 'RULE'])],
            'sourceProfileBinding': context['profileBinding'],
            'sourceOrigin': context['sourceOrigin']}
