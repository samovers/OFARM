"""Derive carrier comparisons from typed claims and selected original records.

No caller-supplied comparison, expected atom, actor pointer or array index is
accepted. This module runs inside the pinned component process. A successful
field comparison does not discharge the remaining interpretation/use roles.
"""
import re
from pathlib import Path
import json
from strict_inputs import same, distinct_selected_originals


from domain_reader_occurrences import reader, selection as observe_selection, guard as observe_guard, origin as read_origin, observed_shape, observe_comparisons, predicate_value, selector_scope, register_result_dependencies


@reader('source_derivation.py', ['AR_BODY'])
def derive(intent, inputs, occupancy=None, endpoint_schemas=None):
    from operation_adapters import OperationAdapters
    from record_comparisons import RecordComparisons, SOURCES, BRANCHES
    from runtime_support import pointer
    operations, records = OperationAdapters(), RecordComparisons()
    schemas = records.schemas.schemas
    all_inputs = inputs
    inputs = [entry for entry in inputs if entry['claimRoles']]
    by_kind = {}
    for kind, (schema_id, _) in SOURCES.items():
        version = schemas[schema_id]['properties']['schemaVersion']['const']
        by_kind[kind] = [entry for entry in inputs if predicate_value(entry, '', isinstance(entry['record'], dict), 'RECORD_SOURCE_KIND:' + kind) and predicate_value(entry, '/schemaVersion', entry['record'].get('schemaVersion'), 'RECORD_SOURCE_KIND:' + kind) == version]
    reports = []
    definitions = json.loads((Path(__file__).resolve().parent / 'domain-definitions.json').read_bytes())['definitions']

    def walk(p, path):
        if p['form'] != 'ATOM':
            if 'child' in p:
                yield from walk(p['child'], path + '/child')
            else:
                for n, child in enumerate(p['children']):
                    yield from walk(child, path + '/children/' + str(n))
        else:
            yield p, path

    for atom, path in walk(intent['assertionBody']['proposition'], '/assertionBody/proposition'):
        selector_scope(atom['atomId'])
        row = atom['definition'].split(':')[-1]
        body = atom['body']
        errors, missing, selected = [], [], []
        jurisdiction_interpretation = None
        sufficiency_interpretation = None

        def need(role, location=path):
            missing.append({'role': role, 'pointer': location})

        def pick(kind, binding=None, relation=None, origins=(), guards=()):
            candidates = by_kind[kind]
            if binding is not None:
                candidates = [v for v in candidates if same(v['binding'], binding)]
                bound = [v for v in inputs if same(v['binding'], binding)]
                if bound and not candidates:
                    errors.append({'code': 'SOURCE_SCHEMA_KIND_MISMATCH', 'pointer': path, 'sourceKind': kind})
            elif relation is not None:
                candidates = [v for v in candidates if relation(v)]
            else:
                raise ValueError('A source selector must have a typed binding or an explicit relation.')
            # Resolve the actual selector/relation first. Independently protected
            # aliases for exactly the same logical identity and original bytes
            # are one source candidate; every alias stays in the input inventory.
            # Different bytes, values or logical identities remain ambiguous.
            candidates = distinct_selected_originals(candidates)
            selected_read = observe_selection('RECORD_SOURCE_' + kind.upper(), inputs, candidates, binding=binding, guards=guards,
                origins=[read_origin('EFFECT_INTENT', path + '/definition')] +
                    ([read_origin('EFFECT_INTENT', path + '/body/claimPosture')] if row.startswith('O') else []) + list(origins),
                predicate_sites=('RECORD_SOURCE_KIND:' + kind,))
            if len(candidates) != 1:
                need('UNIQUE_SELECTED_' + kind.upper() + '_SOURCE')
                if len(candidates) > 1:
                    errors.append({'code': 'AMBIGUOUS_SELECTED_SOURCE', 'pointer': path, 'sourceKind': kind})
                return None
            entry = candidates[0]
            selected.append(entry['id'])
            source = {'binding': entry['binding'], 'record': entry['record']}
            if row.startswith('O'):
                register_result_dependencies(source, 'EVENT_OPERATION_CARRIER', [selected_read])
            return source

        request = None
        carrier_guard = None
        carrier_ambiguity_dependencies = []
        if row.startswith('O'):
            kind = 'intent' if body['claimPosture'] == 'INTENDED' else 'execution'
            field = 'interventionIntentPayloadBindings' if kind == 'intent' else 'executionRecordPayloadBindings'
            declared = intent['assertionBody'].get(field, [])
            declared = [{k: b[k] for k in ['ref', 'revisionRef', 'digest'] if k in b} for b in declared]
            for binding in declared:
                for entry in [v for v in inputs if same(v['binding'], binding)]:
                    errors.extend(observed_shape(operations.schemas, SOURCES[kind][0], entry['record']))
            candidates = [v for v in by_kind[kind] if any(same(v['binding'], b) for b in declared)]
            activity = {'subjectType': 'OPERATION', 'subjectRef': body['activityInstance']['ref']}
            matching = [v for v in candidates if same(predicate_value(v, '/subject', v['record'].get('subject'), 'OPERATION_CARRIER_SUBJECT'), activity)]
            # A lone declared carrier still gets compared when its subject is a
            # target. The adapter retains the required directed activity relation.
            chosen = distinct_selected_originals(matching if matching else candidates)
            carrier_read = observe_selection('DECLARED_OPERATION_CARRIER', inputs, chosen,
                origins=[read_origin('EFFECT_INTENT', path + '/definition'),
                         read_origin('EFFECT_INTENT', path + '/body/claimPosture'),
                         read_origin('EFFECT_INTENT', '/assertionBody/' + field),
                         read_origin('EFFECT_INTENT', path + '/body/activityInstance')],
                predicate_sites=('RECORD_SOURCE_KIND:' + kind, 'OPERATION_CARRIER_SUBJECT'))
            carrier_guard = observe_guard('OPERATION_CARRIER_UNIQUE', len(chosen) == 1,
                origins=[read_origin('EFFECT_INTENT', path + '/definition'),
                         read_origin('EFFECT_INTENT', '/assertionBody/' + field)],
                depends_on=[carrier_read] if carrier_read is not None else [])
            if len(chosen) == 1:
                source = pick(kind, chosen[0]['binding'], origins=[
                    read_origin('EFFECT_INTENT', '/assertionBody/' + field + '/' + str(n))
                    for n, binding in enumerate(declared) if same(binding, chosen[0]['binding'])],
                    guards=[carrier_guard] if carrier_guard is not None else [])
                data = {'atom': atom, 'sourceKind': kind, 'source': source, 'quantitySelections': []}
                for qindex, q in enumerate(body['quantityParameters']):
                    qpath = path + '/body/quantityParameters/' + str(qindex)
                    quantity_guard = observe_guard('OPERATION_QUANTITY_STATED', q['value']['state'] == 'STATED',
                        origins=[read_origin('EFFECT_INTENT', qpath + '/value/state')],
                        depends_on=[carrier_guard] if carrier_guard is not None else [])
                    if q['value']['state'] != 'STATED':
                        continue
                    original = q['value']['original']
                    array = 'quantityParameters' if kind == 'intent' else 'actualQuantityParameters'
                    match = re.fullmatch('/' + array + r'/(0|[1-9][0-9]*)/reportedValue', original['sourcePointer'])
                    pointer_guard = observe_guard('OPERATION_QUANTITY_POINTER_PATTERN', match is not None,
                        origins=[read_origin('EFFECT_INTENT', qpath + '/value/original/sourcePointer'),
                                 read_origin('EFFECT_INTENT', path + '/body/claimPosture')],
                        depends_on=[quantity_guard] if quantity_guard is not None else [])
                    # Keep each submitted quantity selector. A protected alias
                    # can name the same original carrier without rewriting it.
                    from operation_adapters import selected_original_alias
                    quantity_source=selected_original_alias(source,original['sourceBinding'],inputs)
                    alias_read = observe_selection('OPERATION_QUANTITY_ORIGINAL_ALIAS', inputs,
                        [quantity_source] if quantity_source is not None else [],
                        binding=original['sourceBinding'],
                        origins=[read_origin('EFFECT_INTENT', qpath + '/value/original/sourceBinding'),
                                 read_origin(chosen[0]['id'], '')],
                        guards=[quantity_guard] if quantity_guard is not None else [])
                    accepted_guard = observe_guard('OPERATION_QUANTITY_SELECTION_ACCEPTED', bool(match) and quantity_source is not None,
                        origins=[read_origin('EFFECT_INTENT', qpath + '/value/original/sourcePointer'),
                                 read_origin('EFFECT_INTENT', qpath + '/value/original/sourceBinding')],
                        depends_on=[item for item in (pointer_guard, alias_read) if item is not None])
                    if match and quantity_source is not None:
                        observe_guard('OPERATION_QUANTITY_SELECTION_INPUT', True,
                            origins=[read_origin('EFFECT_INTENT', qpath + '/parameterId'),
                                     read_origin('EFFECT_INTENT', qpath + '/value/original/sourcePointer')],
                            depends_on=[accepted_guard] if accepted_guard is not None else [])
                        selected.append(quantity_source['id'])
                        data['quantitySelections'].append({'parameterId': q['parameterId'], 'sourceIndex': int(match[1])})
                    else:
                        errors.append({'code': 'QUANTITY_ORIGINAL_SOURCE_SELECTION_MISMATCH', 'pointer': path + '/body/quantityParameters'})
                if kind == 'execution':
                    # Select from source-declared capture roles before comparing
                    # the claimant's performer. Searching for a matching party
                    # would suppress a real mismatch or be ambiguous when the
                    # actor and operator legitimately name the same person.
                    from work_sources import source_performer_pointer, work_performer_pointer
                    data['performerPointer'] = source_performer_pointer(source['record'])
                    role_pointer = work_performer_pointer(source['record'].get('actor', {}).get('roleAtCapture'))
                    observe_guard('OPERATION_PERFORMER_SOURCE_SELECTOR', data['performerPointer'] is not None,
                        origins=[read_origin(chosen[0]['id'], '/actor/roleAtCapture')] +
                                ([read_origin(chosen[0]['id'], role_pointer)] if role_pointer is not None else []),
                        depends_on=[carrier_guard] if carrier_guard is not None else [])
                    equipment_guard = observe_guard('OPERATION_EQUIPMENT_TARGET_APPLIES', body['target']['kind'] in ['EQUIPMENT', 'TOOL'],
                        origins=[read_origin('EFFECT_INTENT', path + '/body/target/kind')],
                        depends_on=[carrier_guard] if carrier_guard is not None else [])
                    if body['target']['kind'] in ['EQUIPMENT', 'TOOL']:
                        roles = [key for key in ['equipmentRef', 'tractorOrPowerUnitRef', 'implementRef', 'controllerRef']
                                 if predicate_value(chosen[0], '/equipment/' + key, source['record'].get('equipment', {}).get(key), 'OPERATION_EQUIPMENT_ROLE',
                                                    depends_on=[equipment_guard] if equipment_guard is not None else []) == body['target']['binding']['ref']]
                        observe_guard('OPERATION_EQUIPMENT_ROLE_UNIQUE', len(roles) == 1,
                            origins=[read_origin('EFFECT_INTENT', path + '/body/target/binding/ref')] +
                                    [read_origin(chosen[0]['id'], '/equipment/' + key)
                                     for key in ['equipmentRef', 'tractorOrPowerUnitRef', 'implementRef', 'controllerRef']],
                            depends_on=[equipment_guard] if equipment_guard is not None else [],
                            predicate_sites=('OPERATION_EQUIPMENT_ROLE',))
                        if len(roles) == 1:
                            data['assetTargetRole'] = roles[0]
                        else:
                            need('UNIQUE_ASSET_ROLE_IN_SELECTED_EXECUTION')
                if kind == 'intent' or 'performerPointer' in data:
                    request = {'operation': 'operationSource', 'row': row, 'input': data}
            else:
                need('UNIQUE_DECLARED_OPERATION_PAYLOAD_FOR_ACTIVITY')
                if len(chosen) > 1:
                    carrier_ambiguity_dependencies = observe_comparisons([{
                        'predicateId': 'AMBIGUOUS_OPERATION_SOURCE',
                        'source': read_origin('EFFECT_INTENT', '/assertionBody/' + field),
                        'disposition': 'FAIL'}],
                        depends_on=[carrier_guard] if carrier_guard is not None else [])
                    errors.append({'code': 'AMBIGUOUS_OPERATION_SOURCE', 'pointer': path})
        elif row in BRANCHES:
            data = {'atom': atom}
            def add(kind, binding=None, relation=None, origins=()):
                source = pick(kind, binding, relation, origins)
                if source is not None:
                    data[kind] = source
            claim = lambda relative: read_origin('EFFECT_INTENT', path + relative)
            if row in ['C03', 'C04', 'C09'] or row == 'C06' and body['rateSource']['sourceKind'] == 'MEASUREMENT_EVIDENCE':
                role = body['operand']['source'] if row == 'C04' else body.get('measurementSource') if row != 'C06' else body['rateSource'].get('measurementSource')
                if role:
                    role_path = '/body/operand/source' if row == 'C04' else '/body/rateSource/measurementSource' if row == 'C06' else '/body/measurementSource'
                    add('measurement', role['measurementBinding'], origins=[claim(role_path + '/measurementBinding')])
                    add('context', role['contextBinding'], origins=[claim(role_path + '/contextBinding')])
                else:
                    need('SELECTED_NONMEASURED_COMPLIANCE_SOURCE')
            elif row == 'C06':
                add('execution', body['rateSource']['sourceBinding'], origins=[claim('/body/rateSource/sourceBinding'), claim('/body/rateSource/sourceKind')])
            elif row in ['S01', 'S11']:
                if row == 'S11':
                    add('extent', body['value'], origins=[claim('/body/value')])
                else:
                    add('extent', relation=lambda r: predicate_value(r, '/geometryBasis/geometryRef', r['record'].get('geometryBasis', {}).get('geometryRef'), 'RECORD_SOURCE_EXTENT') == body['value']['ref'], origins=[claim('/body/value/ref')])
            elif row in ['S02', 'S04']:
                kind = 'cycle' if row == 'S04' else {'FIELD': 'field', 'CROP_CYCLE': 'cycle'}.get(atom['scope']['subject']['subjectType'])
                ref = body['attempt']['ref'] if row == 'S04' else atom['scope']['subject']['subjectRef']
                if kind is not None:
                    add(kind, relation=lambda r: predicate_value(r, '/identityRecordRef', r['record'].get('identityRecordRef'), 'RECORD_SOURCE_' + kind.upper()) == ref, origins=[claim('/body/attempt/ref' if row == 'S04' else '/scope/subject/subjectRef'), claim('/scope/subject/subjectType')])
            elif row in ['S06', 'C07']:
                binding = body['traceabilityClaimBasis' if row == 'S06' else 'basis']
                add('traceability', binding, origins=[claim('/body/traceabilityClaimBasis' if row == 'S06' else '/body/basis')])
                if row == 'S06':
                    add('lotLineage', relation=lambda r: body['cohort']['ref'] in predicate_value(r, '/subjectLotRefs', r['record'].get('subjectLotRefs', []), 'RECORD_SOURCE_LOTLINEAGE') + predicate_value(r, '/predecessorLotRefs', r['record'].get('predecessorLotRefs', []), 'RECORD_SOURCE_LOTLINEAGE') + predicate_value(r, '/successorLotRefs', r['record'].get('successorLotRefs', []), 'RECORD_SOURCE_LOTLINEAGE'), origins=[claim('/body/cohort/ref')])
            elif row == 'S07':
                add('resource', relation=lambda r: predicate_value(r, '/identityRecordRef', r['record'].get('identityRecordRef'), 'RECORD_SOURCE_RESOURCE') == body['identity']['ref'], origins=[claim('/body/identity/ref')])
                if 'resource' in data:
                    add('code', relation=lambda r: predicate_value(r, '/agronomicIdentityBindingId', r['record'].get('agronomicIdentityBindingId'), 'RECORD_SOURCE_CODE') in data['resource']['record'].get('identityBindingRefs', []), origins=[read_origin(v['id'], '/identityBindingRefs') for v in all_inputs if v['record'] is data['resource']['record']])
            elif row == 'S08':
                add('intent', relation=lambda r: predicate_value(r, '/targetScope/scopeRef', r['record'].get('targetScope', {}).get('scopeRef'), 'RECORD_SOURCE_INTENT') == body['target']['ref'], origins=[claim('/body/target/ref')])
            elif row == 'S09':
                add('lineage', relation=lambda r: all(v['ref'] in predicate_value(r, '/oldIdentityRefs', r['record'].get('oldIdentityRefs', []), 'RECORD_SOURCE_LINEAGE') for v in body['predecessors']), origins=[claim('/body/predecessors')])
            elif row == 'S10':
                add('code', relation=lambda r: predicate_value(r, '/externalScheme/schemeRef', r['record'].get('externalScheme', {}).get('schemeRef'), 'RECORD_SOURCE_CODE') == body['scheme']['ref'] and predicate_value(r, '/bindingValue/capturedLabel', r['record'].get('bindingValue', {}).get('capturedLabel'), 'RECORD_SOURCE_CODE') == body['originalLexicalValue'], origins=[claim('/body/scheme/ref'), claim('/body/originalLexicalValue')])
            elif row == 'S12':
                add('equipment', relation=lambda r: predicate_value(r, '/identityRecordRef', r['record'].get('identityRecordRef'), 'RECORD_SOURCE_EQUIPMENT') == body['asset']['ref'], origins=[claim('/body/asset/ref')])
            elif row == 'S14':
                add('lineage', relation=lambda r: body['location']['ref'] in predicate_value(r, '/oldIdentityRefs', r['record'].get('oldIdentityRefs', []), 'RECORD_SOURCE_LINEAGE') + predicate_value(r, '/newIdentityRefs', r['record'].get('newIdentityRefs', []), 'RECORD_SOURCE_LINEAGE'), origins=[claim('/body/location/ref')])
            elif row == 'C05':
                add('registry', body['verificationTrace'], origins=[claim('/body/verificationTrace')]); add('codeProfile', body['profile'], origins=[claim('/body/profile')])
                from jurisdiction_sources import evaluate as jurisdiction_sources
                jurisdiction_interpretation = jurisdiction_sources(atom, all_inputs, records.schemas)
                errors.extend(jurisdiction_interpretation['errors']); missing.extend(jurisdiction_interpretation['remainingRoles'])
                selected.extend(jurisdiction_interpretation['sourceInputIds'])
                if jurisdiction_interpretation['selectedJurisdictionRef'] is not None:
                    data['selectedJurisdictionRef'] = jurisdiction_interpretation['selectedJurisdictionRef']
            elif row == 'C08':
                add('decision', body['decision'], origins=[claim('/body/decision')])
            elif row == 'C10':
                from sufficiency_sources import evaluate as sufficiency_sources
                sufficiency_interpretation = sufficiency_sources(atom, all_inputs, records.schemas, intent['evidenceBindings'])
                errors.extend(sufficiency_interpretation['errors']); missing.extend(sufficiency_interpretation['remainingRoles'])
                selected.extend(sufficiency_interpretation['sourceInputIds'])
                if sufficiency_interpretation['selectedCaseBinding'] is not None:
                    add('sufficiency', sufficiency_interpretation['selectedCaseBinding'], origins=[read_origin(v['id'], '/sufficiencyCaseBinding') for v in all_inputs if v['id'] in sufficiency_interpretation['sourceInputIds'] and isinstance(v['record'], dict) and 'sufficiencyCaseBinding' in v['record']])
                else:
                    add('sufficiency', relation=lambda r: body['policy']['ref'] in predicate_value(r, '/governingPolicyRefs', r['record'].get('governingPolicyRefs', []), 'RECORD_SOURCE_SUFFICIENCY'), origins=[claim('/body/policy/ref')])
            if any(all(kind in data for kind in branch) for branch in BRANCHES[row]) and (row != 'C05' or 'selectedJurisdictionRef' in data):
                request = {'operation': 'recordSource', 'row': row, 'input': data}
        else:
            need('ROW_SOURCE_INTERPRETATION:' + row)

        result = None
        if request is not None:
            result = operations.check(row, request['input'], resolved_sources=inputs) if row.startswith('O') else records.check(row, request['input'])
            if row.startswith('O'):
                # Adapter operands are checked against the actual original
                # values before being rebound to public source/claim paths.
                source_binding=request['input']['source']['binding']
                source_id=next(v['id'] for v in all_inputs if same(v['binding'],source_binding))
                selector_index=next(i for i,v in enumerate(declared) if same(v,source_binding))
                definition_index=next(i for i,v in enumerate(definitions) if v['id']==row)
                for comparison in result['comparisons']:
                    operands=comparison.get('operandAvailability',comparison)
                    for side in ['source','destination']:
                        if side not in operands:continue
                        operand=operands[side];role=operand['inputRole']
                        if role=='OPERATION_SOURCE':operand['inputRole']=source_id
                        elif role.startswith('OPERATION_QUANTITY_SOURCE:'):
                            qindex=int(role.split(':')[-1]);binding=body['quantityParameters'][qindex]['value']['original']['sourceBinding']
                            operand['inputRole']=next(v['id'] for v in all_inputs if same(v['binding'],binding))
                        elif role=='OPERATION_SOURCE_SELECTOR':
                            if 'ancestorPointer' in operand:operand['ancestorPointer']='/assertionBody/'+field+'/'+str(selector_index)+operand['ancestorPointer']
                            operand.update(inputRole='EFFECT_INTENT',pointer='/assertionBody/'+field+'/'+str(selector_index)+operand['pointer'])
                        elif role=='DOMAIN_DEFINITION:'+row:
                            if 'ancestorPointer' in operand:operand['ancestorPointer']='/definitions/'+str(definition_index)+'/sourceDefinition'+operand['ancestorPointer']
                            operand.update(inputRole='DOMAIN_DEFINITIONS',pointer='/definitions/'+str(definition_index)+'/sourceDefinition'+operand['pointer'])
            else:
                # Original operand paths come from the fixed record adapter.
                # Rebind selectors only to an actual typed claim reference;
                # an internally constructed selector is never original bytes.
                for comparison in result['comparisons']:
                    unresolved = False
                    operands = comparison.get('operandAvailability', comparison)
                    for side in ['source', 'destination']:
                        if side not in operands: continue
                        operand = operands[side]; role = operand['inputRole']
                        if role.startswith(('DOMAIN_COMPARISON_RULES:', 'DOMAIN_DEFINITION:')):
                            definition_row = role.split(':', 1)[1]
                            index = next(i for i, v in enumerate(definitions) if v['id'] == definition_row)
                            prefix = '/definitions/' + str(index) + ('/ownedComparisonRules' if role.startswith('DOMAIN_COMPARISON_RULES:') else '/sourceDefinition')
                            operand['inputRole'] = 'DOMAIN_DEFINITIONS'
                            for key in ['pointer', 'ancestorPointer']:
                                if key in operand: operand[key] = prefix + operand[key]
                            continue
                        if not role.startswith(('RECORD_SOURCE:', 'RECORD_SELECTOR:')): continue
                        kind = role.split(':', 1)[1]
                        binding = request['input'][kind]['binding']
                        entry = next(v for v in all_inputs if same(v['binding'], binding))
                        if role.startswith('RECORD_SOURCE:'):
                            operand['inputRole'] = entry['id']; continue
                        candidates = []
                        expected = pointer(binding, operand['pointer'])
                        for use in entry['claimRoles']:
                            location = use['pointer'] + operand['pointer']
                            try: original = pointer(intent, location)
                            except ValueError: continue
                            if same(original, expected): candidates.append(location)
                        if candidates:
                            operand.update(inputRole='EFFECT_INTENT', pointer=candidates[0])
                        else:
                            comparison.setdefault('unavailableOriginalOperands', []).append(side)
                            unresolved = True
                    if unresolved:
                        for key in ['source', 'destination', 'disposition', 'operandAvailability']: comparison.pop(key, None)
            errors.extend(result['errors'])
            # Exact raw-byte selection has been completed before this worker.
            # Every other role remains an explicit named prerequisite until its
            # actual field predicates are evaluated; it is never an input flag.
            missing.extend(r for r in result.get('requiredOwnerRoles', []) if r['role'] != 'EXACT_IMMUTABLE_SOURCE_RESOLUTION')
        interpretation = jurisdiction_interpretation
        if sufficiency_interpretation is not None:
            interpretation = sufficiency_interpretation
            if interpretation['selectedCaseBinding'] is not None:
                missing = [r for r in missing if r['role'] != 'SUFFICIENCY_REQUIRED_USE_EVIDENCE_SET_MISSING_KINDS_AND_OUTCOME_MAPPING']
        if row in ['C01', 'C02']:
            from rule_meaning_sources import evaluate as rule_meaning
            interpretation = rule_meaning(atom, all_inputs, records.schemas, intent['evidenceBindings'])
            errors.extend(interpretation['errors']); missing.extend(interpretation['remainingRoles'])
            selected.extend(interpretation['sourceInputIds'])
            missing = [r for r in missing if r['role'] != 'ROW_SOURCE_INTERPRETATION:' + row]
            if interpretation['selectedDefinitionBinding'] is not None:
                request = {'operation': 'ownedRuleMeaning', 'row': row, 'definitionBinding': interpretation['selectedDefinitionBinding']}
        if row == 'C17':
            from si_c17_sources import evaluate as si_c17_sources
            interpretation = si_c17_sources(atom, all_inputs, endpoint_schemas or records.schemas,
                                            intent['evidenceBindings'])
            errors.extend(interpretation['errors']); missing.extend(interpretation['remainingRoles'])
            selected.extend(interpretation['sourceInputIds'])
            missing = [r for r in missing if r['role'] != 'ROW_SOURCE_INTERPRETATION:C17']
        if row.startswith('O'):
            from work_sources import evaluate as work_sources
            interpretation = work_sources(atom, request, all_inputs, operations.schemas)
            errors.extend(interpretation['errors']); missing.extend(interpretation['remainingRoles'])
            selected.extend(interpretation['sourceInputIds'])
            missing = [r for r in missing if r['role'] not in interpretation['closedRoles']]
            if row in ['O10', 'O22']:
                from sample_relation_sources import evaluate as sample_relation
                relation = sample_relation(atom, all_inputs, operations.schemas)
                # A work condition can pass while sample source-use remains
                # unresolved. Keep its disposition and closure separate.
                interpretation['sourceRelationFindings'] = [relation]
                interpretation['comparisons'].extend(relation['comparisons'])
                interpretation['requiredReferences'].extend(relation['requiredReferences'])
                errors.extend(relation['errors']); missing.extend(relation['remainingRoles'])
                selected.extend(relation['sourceInputIds'])
        if row == 'C04':
            from criterion_sources import evaluate as criterion_sources
            interpretation = criterion_sources(atom, all_inputs, records.schemas)
            errors.extend(interpretation['errors'])
            missing.extend(interpretation['remainingRoles'])
            selected.extend(interpretation['sourceInputIds'])
            if interpretation['disposition'] == 'PASS':
                closed = {'SELECTED_RESULT_ADMISSIBLE_SET_MAPPING_AND_THRESHOLD_PROVENANCE',
                          'EXACT_PROPERTY_METHOD_USE_SUBJECT_RELATION_AND_COMPLETE_QUALIFICATIONS',
                          'EXACT_LIMIT_SCALAR_LEXICAL_AND_QUALIFIER_PROVENANCE'}
                missing = [r for r in missing if r['role'] not in closed]
        if row == 'S02':
            from parent_claim_sources import evaluate as parent_claim_sources
            interpretation = parent_claim_sources(atom, intent, all_inputs, endpoint_schemas or records.schemas, path)
            errors.extend(interpretation['errors']); missing.extend(interpretation['remainingRoles'])
            selected.extend(interpretation['sourceInputIds'])
            missing = [v for v in missing if v['role'] != 'PARENT_RELATION_KIND_TIME_AND_PROSPECTIVE_APPLICABILITY']
        if row == 'S10':
            from identifier_sources import evaluate as identifier_sources
            interpretation = identifier_sources(atom, request, all_inputs, records.schemas, endpoint_schemas, intent)
            errors.extend(interpretation['errors']); missing.extend(interpretation['remainingRoles'])
            selected.extend(interpretation['sourceInputIds'])
            if interpretation['disposition'] == 'PASS':
                missing = [v for v in missing if v['role'] != 'EXACT_NAMED_ATTRIBUTE_AND_IDENTIFIER_ROLE']
                need('IDENTIFIER_SUBJECT_VERSION_TIME_AND_GOVERNED_SOURCE_USE', path + '/body/scheme')
        if row == 'S13':
            from occupancy_sources import evaluate as occupancy_evaluate
            interpretation = occupancy_evaluate(atom, (occupancy or {}).get(atom['atomId']))
            errors.extend(interpretation['errors']); missing.extend(interpretation['remainingRoles'])
            selected.extend(interpretation['sourceInputIds'])
            missing = [v for v in missing if v['role'] != 'ROW_SOURCE_INTERPRETATION:S13']
            if (occupancy or {}).get(atom['atomId']) is not None:
                request = {'operation': 'reviewedOccupancyOwner', 'row': row, 'atomId': atom['atomId']}
        source_identity_dependencies = []
        if result is not None:
            observe_comparisons(result.get('comparisons', []))
            if row.startswith('O'):
                # Reuse the actual same-object comparison IDs for this atom.
                source_identity_dependencies = observe_comparisons([comparison
                    for comparison in result.get('comparisons', [])
                    if comparison.get('predicateId') == 'SOURCE_ID_BINDING_MISMATCH'])
        finding = {'atomId': atom['atomId'], 'row': row, 'pointer': path,
                        'sourceInputIds': sorted(set(selected)), 'derivedRequest': request,
                        'disposition': 'FAIL' if errors else 'NOT_EVALUATED' if missing else 'PASS',
                        'errors': errors, 'remainingRoles': missing,
                        'comparisons': result.get('comparisons', []) if result else [],
                        **({'sourceInterpretation': interpretation} if interpretation is not None else {})}
        if row.startswith('O') and carrier_guard is not None:
            register_result_dependencies(finding, 'EVENT_OPERATION_SELECTION', [carrier_guard] + carrier_ambiguity_dependencies)
        if source_identity_dependencies:
            register_result_dependencies(finding, 'EVENT_OPERATION_SOURCE_IDENTITY', source_identity_dependencies)
        reports.append(finding)
    return {'atoms': reports, 'errors': [e for r in reports for e in r['errors']],
            'remainingRoles': [{'atomId': r['atomId'], **role} for r in reports for role in r['remainingRoles']],
            'requiredReferences': [ref for r in reports for ref in r.get('sourceInterpretation', {}).get('requiredReferences', [])]}
