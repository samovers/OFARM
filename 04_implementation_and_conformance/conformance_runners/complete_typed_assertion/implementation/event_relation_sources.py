"""One explicit event operation -> execution -> target relation.

This is an original-field comparison for V06-operation-target. It is not an
admitted relationship proof, an authority path, or a transitive graph search.
The caller uses it only after direct event-subject membership has failed.
"""
from strict_inputs import same, digest


def mandatory_positive(proposition, atom_ids, negated=False):
    if proposition['form'] == 'ATOM':
        return not negated and proposition['atomId'] in atom_ids
    if proposition['form'] == 'NOT':
        return mandatory_positive(proposition['child'], atom_ids, not negated)
    if proposition['form'] == 'QUALIFIED':
        return mandatory_positive(proposition['child'], atom_ids, negated)
    values = [mandatory_positive(child, atom_ids, negated) for child in proposition['children']]
    return all(values) if (proposition['form'] == 'ANY') != negated else any(values)


from domain_reader_occurrences import reader, selection as observe_selection, guard as observe_guard, origin as read_origin, observed_shape, observe_comparisons


@reader('event_relation_sources.py', ['AR_EVENT_ASSOCIATION'])
def evaluate(intent, envelope, atoms, automatic, sources, schemas, definition):
    from time_validation import foreign_seconds
    errors, missing, comparisons, ids, refs, candidates = [], [], [], [], [], []
    matched = set()
    checked = {a['atomId']: a for a in automatic.get('atoms', [])}

    def compare(code, left, right, source, destination):
        equal = same(left, right)
        comparisons.append({'predicateId': code, 'equal': equal, 'pointer': source['pointer'],
            'source': {**source, 'valueDigest': digest(left)},
            'destination': {**destination, 'valueDigest': digest(right)},
            'disposition': 'PASS' if equal else 'FAIL'})
        observe_comparisons([comparisons[-1]])
        if not equal:
            errors.append({'code': code, 'pointer': source['pointer']})

    for atom in atoms:
        finding = checked.get(atom['atomId'], {})
        request = finding.get('derivedRequest') or {}
        if request.get('operation') != 'operationSource' or request['input']['sourceKind'] != 'execution':
            continue
        path = finding['pointer']; binding = request['input']['source']['binding']
        selected = [entry for entry in sources if same(entry['binding'], binding)]
        observe_selection('EVENT_EXECUTION_RELATION', sources, selected, binding=binding,
            origins=[read_origin('EFFECT_INTENT', '/assertionBody/executionRecordPayloadBindings/' + str(n))
                for n, value in enumerate(intent['assertionBody'].get('executionRecordPayloadBindings', []))
                if same({k: value[k] for k in ('ref', 'digest', 'revisionRef') if k in value}, binding)])
        if len(selected) != 1:
            missing.append({'role': 'EXACT_EVENT_OPERATION_EXECUTION_ORIGINAL', 'pointer': path})
            continue
        entry = selected[0]; record = entry['record']; start_error = len(errors)
        ids.append(entry['id'])
        proof_indices = [n for n, b in enumerate(intent['subjectScopeProofBindings']) if same(b, binding)]
        if not proof_indices:
            missing.append({'role': 'EXACT_SELECTED_EXECUTION_RELATION_BINDING', 'pointer': '/subjectScopeProofBindings'})
            continue
        proof_pointer = '/subjectScopeProofBindings/' + str(proof_indices[0])
        refs.append({'role': 'EVENT_OPERATION_TARGET_ORIGINAL_CARRIER', 'binding': binding, 'pointer': proof_pointer})
        shape = observed_shape(schemas, 'https://ofarm.dev/schema/executionrecordpayload/v0.1', record)
        errors.extend(shape)
        if shape:
            continue
        def src(pointer): return {'inputRole': entry['id'], 'pointer': pointer}
        def claim(pointer): return {'inputRole': 'EFFECT_INTENT', 'pointer': pointer}
        def event(pointer): return {'inputRole': 'event:envelope', 'pointer': pointer}
        compare('EVENT_RELATION_EXECUTION_IDENTITY_MISMATCH', record['executionRecordPayloadId'], binding['ref'],
                src('/executionRecordPayloadId'), claim(proof_pointer + '/ref'))
        body = atom['body']; activity = body['activityInstance']; target = body['target']
        compare('EVENT_RELATION_OPERATION_KIND_MISMATCH', record['subject']['subjectType'], 'OPERATION',
                src('/subject/subjectType'), {'inputRole': 'DOMAIN_DEFINITIONS',
                    'pointer': '/definitions/' + str(definition['index']) + '/sourceDefinition/typedRepresentation/fromKind'})
        compare('EVENT_RELATION_OPERATION_IDENTITY_MISMATCH', record['subject']['subjectRef'], activity['ref'],
                src('/subject/subjectRef'), claim(path + '/body/activityInstance/ref'))
        operation_indices = [n for n, ref in enumerate(envelope['subjectRefs']) if ref == activity['ref']]
        payload_indices = [n for n, ref in enumerate(envelope.get('executionRecordPayloadRefs', [])) if ref == binding['ref']]
        for indices, field, value, source_pointer, code in [
            (operation_indices, 'subjectRefs', activity['ref'], path + '/body/activityInstance/ref', 'EVENT_RELATION_OPERATION_NOT_IN_EVENT'),
            (payload_indices, 'executionRecordPayloadRefs', binding['ref'], proof_pointer + '/ref', 'EVENT_RELATION_EXECUTION_NOT_IN_EVENT')]:
            if indices:
                compare(code, envelope[field][indices[0]], value, event('/' + field + '/' + str(indices[0])), claim(source_pointer))
            else:
                errors.append({'code': code, 'pointer': '/event/' + field})
        if 'sourceEventRef' in record:
            compare('EVENT_RELATION_EXECUTION_REVERSE_EVENT_MISMATCH', record['sourceEventRef'], envelope['semanticEventId'],
                    src('/sourceEventRef'), event('/semanticEventId'))
        for key, target_key, subject_key in [('scopeType', 'kind', 'subjectType'), ('scopeRef', 'ref', 'subjectRef')]:
            value = target['binding']['ref'] if target_key == 'ref' else target[target_key]
            target_pointer = path + '/body/target/' + ('binding/ref' if target_key == 'ref' else target_key)
            compare('EVENT_RELATION_TARGET_' + key.upper() + '_MISMATCH', record['executionExtent']['targetScope'][key], value,
                    src('/executionExtent/targetScope/' + key), claim(target_pointer))
            compare('EVENT_RELATION_CLAIM_SUBJECT_' + key.upper() + '_MISMATCH', value, intent['subject'][subject_key],
                    claim(target_pointer), claim('/subject/' + subject_key))
        # Every immutable selector field is compared. A shared logical ref does
        # not erase a different target revision or digest.
        target_subject = {'ref': intent['subject']['subjectRef'], **{k: intent['subject'][k] for k in ['revisionRef', 'digest'] if k in intent['subject']}}
        if not same(target['binding'], target_subject):
            errors.append({'code': 'EVENT_RELATION_TARGET_SUBJECT_SELECTOR_MISMATCH', 'pointer': path + '/body/target/binding'})
        for key in ['revisionRef', 'digest']:
            if key in target['binding'] and key in intent['subject']:
                compare('EVENT_RELATION_TARGET_SUBJECT_' + key.upper() + '_MISMATCH', target['binding'][key], intent['subject'][key],
                        claim(path + '/body/target/binding/' + key), claim('/subject/' + key))
        extent = body['extent']
        if extent['posture'] == 'PARTIAL_TARGET_SCOPE':
            if record['executionExtent'].get('extentRef') is None:
                errors.append({'code': 'EVENT_RELATION_PARTIAL_EXTENT_MISSING', 'pointer': '/executionExtent/extentRef'})
            else:
                compare('EVENT_RELATION_PARTIAL_EXTENT_MISMATCH', record['executionExtent']['extentRef'], extent['binding']['ref'],
                        src('/executionExtent/extentRef'), claim(path + '/body/extent/binding/ref'))
            if record['executionExtent']['extentClass'] == 'WHOLE_TARGET_SCOPE':
                errors.append({'code': 'EVENT_RELATION_WHOLE_SOURCE_FOR_PARTIAL_CLAIM', 'pointer': '/executionExtent/extentClass'})
        elif record['executionExtent']['extentClass'] != 'WHOLE_TARGET_SCOPE' or 'extentRef' in record['executionExtent']:
            errors.append({'code': 'EVENT_RELATION_PARTIAL_SOURCE_FOR_WHOLE_CLAIM', 'pointer': '/executionExtent'})
        time = atom['scope']['subjectTime']; interval = record['effectiveTimeInterval']
        try:
            start, end = foreign_seconds(interval['start']), foreign_seconds(interval['end'])
            lo = foreign_seconds(time.get('at', time.get('start')))
            hi = foreign_seconds(time['end']) if 'end' in time else lo if 'at' in time else None
            covered = start < end and start <= lo and hi is not None and hi <= end
            if not covered:
                errors.append({'code': 'EVENT_RELATION_EXECUTION_TIME_DOES_NOT_COVER_CLAIM', 'pointer': '/effectiveTimeInterval'})
            comparisons.append({'predicateId': 'EVENT_RELATION_EXECUTION_TIME_COVERS_CLAIM',
                'source': {**src('/effectiveTimeInterval'), 'valueDigest': digest(interval)},
                'destination': {**claim(path + '/scope/subjectTime'), 'valueDigest': digest(time)},
                'disposition': 'PASS' if covered else 'FAIL'})
            observe_comparisons([comparisons[-1]])
        except (ValueError, TypeError):
            errors.append({'code': 'EVENT_RELATION_EXECUTION_TIME_UNINTERPRETABLE', 'pointer': '/effectiveTimeInterval'})
        okay = len(errors) == start_error and not finding.get('errors')
        candidates.append({'atomId': atom['atomId'], 'executionBinding': binding, 'sourceInputId': entry['id'],
            'operationBinding': activity, 'targetBinding': target['binding'], 'matchedOriginalFields': okay,
            'eventSubjectIndices': operation_indices, 'eventPayloadIndices': payload_indices})
        if okay:
            matched.add(atom['atomId'])
        missing.extend({'role': role, 'pointer': proof_pointer} for role in [
            'EVENT_OPERATION_TARGET_ENDPOINT_VERSION_AND_KIND_USE',
            'EVENT_OPERATION_TARGET_PROVENANCE_TIME_EXTENT_AND_ELIGIBLE_USE'])
    if candidates and not mandatory_positive(intent['assertionBody']['proposition'], matched):
        errors.append({'code': 'EVENT_RELATION_MANDATORY_POSITIVE_OPERATION_NOT_ESTABLISHED', 'pointer': '/assertionBody/proposition'})
    established = bool(candidates) and mandatory_positive(intent['assertionBody']['proposition'], matched)
    return {'canonicalRow': 'V06-operation-target', 'caseDefinitionBinding': definition['binding'],
        'scope': 'CONDITIONAL_ORIGINAL_OPERATION_TO_TARGET_FIELDS_ONLY',
        'disposition': 'FAIL' if errors else 'NOT_EVALUATED',
        'errors': errors, 'remainingRoles': missing, 'comparisons': comparisons,
        'sourceInputIds': sorted(set(ids)), 'requiredReferences': refs,
        'candidates': candidates, 'matchedAtomIds': sorted(matched), 'mandatoryOriginalRelationEstablished': established,
        'qualification': 'Original directed field comparisons only; no admitted relationship, occurrence, endpoint currentness or authority is inferred.'}
