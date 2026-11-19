"""C04 interpretation from original normative definitions and actual carriers.

Required definitions are selected by the claim's immutable bindings and checked
against independent raw/JCS source selection. Operator, threshold, property,
method, context, qualifications and admissible sets are derived from those
definitions and actual source fields, never a caller-provided expected atom.
"""
import copy
from decimal import Decimal
from strict_inputs import same, digest
from definition_inputs import SCHEMAS, register


def evaluate(atom, sources, schemas, *, claim_origin='ACTUAL_ATOM'):
    return _evaluate_criterion(atom, sources, schemas, claim_origin=claim_origin)


def evaluate_traced(atom, sources, schemas, *, claim_origin=None):
    """Run the same reader and retain each attempted original-source read.

    Derived criterion pointers describe construction inputs, not original
    evidence. Their real source origins must be resolved by the constructor.
    """
    reads, guards = [], []
    report = _evaluate_criterion(atom, sources, schemas, claim_origin=claim_origin, reads=reads, guards=guards)
    return {'report': report, 'reads': reads, 'guards': guards}


def _evaluate_criterion(atom, sources, schemas, *, claim_origin, reads=None, guards=None):
    from runtime_support import pointer, number
    from meaning_comparisons import MeaningComparisons
    from time_validation import foreign_instant, foreign_seconds
    register(schemas)
    errors, missing, comparisons, refs, selected_ids = [], [], [], [], []
    body = atom['body']; source_role = body['operand']['source']
    origins = {}
    observation_selection = None
    domain_interpretation = None

    def source_origin(record, path):
        return {'inputRole': origins[id(record)], 'pointer': path}

    def atom_origin(path):
        # Work conditions construct an internal criterion from original fields.
        # Those synthetic fields must never be labelled as submitted atom bytes.
        return {'inputRole': 'ATOM:' + atom['atomId'], 'pointer': path} if claim_origin == 'ACTUAL_ATOM' else None

    def binding_origin(record, path):
        if record is not None:
            return {'kind': 'ORIGINAL', **source_origin(record, path)}
        if claim_origin == 'ACTUAL_ATOM':
            return {'kind': 'ACTUAL_ATOM', **atom_origin(path)}
        return {'kind': 'DERIVED_CRITERION', 'pointer': path}

    def last_read():
        return len(reads) - 1 if reads is not None else None

    def guard(rule, satisfied, read_indices=(), operands=(), *, diagnostic_state=False):
        if guards is None: return None
        gid = 'criterion-guard:' + str(len(guards))
        fact = {'id': gid, 'rule': rule, 'satisfied': satisfied,
                'readIndices': [index for index in read_indices if index is not None],
                'operands': list(operands)}
        if diagnostic_state:
            fact.update(stateProvenance='DERIVED_READER_DIAGNOSTICS',
                        errorCount=len(errors), errors=copy.deepcopy(errors),
                        comparisonPredicateIds=[item['predicateId'] for item in comparisons])
        guards.append(fact)
        return gid

    def compare(code, actual, expected, path, source=None, destination=None, equal=None):
        if equal is None: equal = same(actual, expected)
        fact={'predicateId': code, 'pointer': path, 'equal': equal,
              'actualValueDigest': digest(actual), 'expectedValueDigest': digest(expected)}
        if source is not None and destination is not None:
            fact.update(source={**source,'valueDigest':digest(actual)}, destination={**destination,'valueDigest':digest(expected)},
                        disposition='PASS' if equal else 'FAIL')
        comparisons.append(fact)
        if not equal:
            errors.append({'code': code, 'pointer': path})

    def resolve(binding, schema_id, role, origin, guard_ids=()):
        refs.append({'role': role, 'binding': binding, 'pointer': '/definitionInputs/' + role})
        matches = [v for v in sources if same(v['binding'], binding)]
        if role == 'CRITERION_OBSERVED_PROPERTY_DEFINITION' and 'revisionRef' in binding:
            from condition_property_resolution import ConditionSources
            if isinstance(sources, ConditionSources):
                matches = (sources.property_for(method, recursive=True)
                           if origin == binding_origin(method, '/propertyBinding') else [])
        event = None
        if reads is not None:
            event = {'role': role, 'binding': copy.deepcopy(binding), 'schemaId': schema_id,
                     'bindingOrigin': origin, 'selectedInputId': None,
                     'matchCount': len(matches), 'schemaErrors': None,
                     'guardIds': [gid for gid in guard_ids if gid is not None]}
            reads.append(event)
        if len(matches) != 1:
            missing.append({'role': role, 'pointer': '/definitionInputs/' + role})
            return None
        item = matches[0]; record = item['record']; selected_ids.append(item['id'])
        if event is not None:
            event['selectedInputId'] = item['id']
        shape = schemas.errors(schema_id, record)
        if event is not None:
            event['schemaErrors'] = copy.deepcopy(shape)
        errors.extend(shape)
        if shape:
            return None
        origins[id(record)] = item['id']
        if schema_id in [v['$id'] for v in SCHEMAS.values()]:
            compare('DEFINITION_IDENTITY_MISMATCH', record['definitionId'], binding['ref'], '/definitionInputs/' + role + '/definitionId')
        else:
            identity = {'https://ofarm.dev/schema/measurementevidence/v0.1': 'measurementEvidenceId',
                        'https://ofarm.dev/schema/agronomicobservationcontext/v0.1': 'agronomicObservationContextId',
                        'https://ofarm.dev/schema/executionrecordpayload/v0.1': 'executionRecordPayloadId',
                        'https://ofarm.dev/schema/partialextent/v0.1': 'partialExtentId'}[schema_id]
            compare('CRITERION_SOURCE_IDENTITY_MISMATCH', record[identity], binding['ref'], '/definitionInputs/' + role + '/' + identity)
        return record

    def term(binding, category, path, origin, guard_ids=()):
        record = resolve(binding, SCHEMAS['term']['$id'], 'CRITERION_' + category + '_DEFINITION', origin, guard_ids)
        if record is not None:
            compare('CRITERION_TERM_CATEGORY_MISMATCH', record['category'], category, path)
        return record

    def finish(outcome=None):
        return {'scope': 'C04_ORIGINAL_SOURCE_INTERPRETATION',
                'disposition': 'FAIL' if errors else 'NOT_EVALUATED' if missing else 'PASS',
                'errors': errors, 'remainingRoles': missing, 'comparisons': comparisons,
                'requiredReferences': refs, 'sourceInputIds': sorted(set(selected_ids)),
                **({'selectedObservationMeaning': observation_selection} if observation_selection is not None else {}),
                **({'admissibleDomainInterpretation': domain_interpretation} if domain_interpretation is not None else {}),
                **({'conditionalMathematicalOutcome': outcome} if outcome else {})}

    criterion = resolve(body['criterion'], SCHEMAS['criterion']['$id'], 'SELECTED_C04_CRITERION_DEFINITION',
                        binding_origin(None, '/body/criterion'))
    criterion_ready = guard('CRITERION_DEFINITION_AVAILABLE', criterion is not None, (last_read(),))
    if criterion is None:
        return finish()
    method = resolve(criterion['methodUseBinding'], SCHEMAS['method']['$id'], 'SELECTED_MEASUREMENT_USE_DEFINITION',
                     binding_origin(criterion, '/methodUseBinding'), (criterion_ready,))
    method_index = last_read()
    method_ready = guard('MEASUREMENT_USE_DEFINITION_AVAILABLE', method is not None, (method_index,))
    if method is None:
        return finish()
    terms = {}
    for field, category in [('propertyBinding', 'OBSERVED_PROPERTY'), ('methodBinding', 'MEASUREMENT_METHOD'), ('protocolBinding', 'SAMPLING_PROTOCOL')]:
        selected_term = guard('OPTIONAL_TERM_PRESENT:' + field, method[field] is not None,
                              (method_index,), (binding_origin(method, '/' + field),))
        if method[field] is not None:
            terms[category] = term(method[field], category, '/method/' + field, binding_origin(method, '/' + field),
                                   (method_ready, selected_term))
    unit_term = term(method['quantityContext']['unitProfile'], 'UNIT_PROFILE', '/method/quantityContext/unitProfile',
                     binding_origin(method, '/quantityContext/unitProfile'), (method_ready,))
    if unit_term is not None:
        compare('CRITERION_UNIT_PROFILE_CONTEXT_MISMATCH', unit_term['quantityContext'],
                {k: method['quantityContext'][k] for k in ['quantityKind', 'unit']}, '/unitProfile/quantityContext')
    compare('CRITERION_METHOD_SELECTION_MISMATCH', source_role['methodUseBinding'], criterion['methodUseBinding'], '/body/operand/source/methodUseBinding',
            atom_origin('/body/operand/source/methodUseBinding'), source_origin(criterion,'/methodUseBinding'))
    compare('METHOD_SCOPE_MISMATCH', atom['scope'], method['scope'], '/scope',atom_origin('/scope'),source_origin(method,'/scope'))
    compare('METHOD_CONTEXT_SELECTION_MISMATCH', source_role['contextBinding'], method['contextBinding'], '/body/operand/source/contextBinding',
            atom_origin('/body/operand/source/contextBinding'),source_origin(method,'/contextBinding'))
    compare('METHOD_SUBJECT_RELATION_SELECTION_MISMATCH', source_role['subjectRelationBinding'], method['subjectRelationBinding'], '/body/operand/source/subjectRelationBinding',
            atom_origin('/body/operand/source/subjectRelationBinding'),source_origin(method,'/subjectRelationBinding'))
    compare('SELECTED_CRITERION_OPERATOR_MISMATCH', body['operator'], criterion['operator'], '/body/operator',atom_origin('/body/operator'),source_origin(criterion,'/operator'))
    measure = resolve(source_role['measurementBinding'], 'https://ofarm.dev/schema/measurementevidence/v0.1', 'CRITERION_MEASUREMENT',
                      binding_origin(None, '/body/operand/source/measurementBinding'), (method_ready,))
    measurement_index = last_read()
    context = resolve(method['contextBinding'], 'https://ofarm.dev/schema/agronomicobservationcontext/v0.1', 'CRITERION_CONTEXT',
                      binding_origin(method, '/contextBinding'), (method_ready,))
    context_index = last_read()
    measure_context_ready = guard('MEASUREMENT_AND_CONTEXT_AVAILABLE', measure is not None and context is not None,
                                  (measurement_index, context_index))
    if measure is None or context is None:
        return finish()
    relation = resolve(method['subjectRelationBinding'], 'https://ofarm.dev/schema/agronomicobservationcontext/v0.1',
                       'CRITERION_SUBJECT_RELATION_CONTEXT', binding_origin(method, '/subjectRelationBinding'),
                       (measure_context_ready,))
    relation_ready = guard('SUBJECT_RELATION_CONTEXT_AVAILABLE', relation is not None, (last_read(),))
    if relation is not None:
        compare('CRITERION_RELATION_CONTEXT_MISMATCH', relation, context, '/subjectRelation',source_origin(relation,''),source_origin(context,''))
        left,right=context['phenomenonTime'],measure['phenomenonTime']
        clocks={'instant','intervalStart','intervalEnd'}
        matched=(left.keys()==right.keys() and same({k:v for k,v in left.items() if k not in clocks},{k:v for k,v in right.items() if k not in clocks}))
        unknown=False
        if matched:
            required={'instant'} if left['timeType'] in ['INSTANT','AS_OF'] else {'intervalStart'}
            if not required<=left.keys():unknown=True
            for key in clocks & left.keys():
                a,z=foreign_instant(left[key]),foreign_instant(right[key])
                if a['unknownLocalOffset'] or z['unknownLocalOffset']:unknown=True
                elif a['seconds']!=z['seconds']:matched=False
        if matched and unknown:
            missing.append({'role':'CRITERION_CONTEXT_KNOWN_PHENOMENON_TIME_INTERPRETATION','pointer':'/context/phenomenonTime'})
        else:
            compare('CRITERION_CONTEXT_TIME_MISMATCH',left,right,'/context/phenomenonTime',
                source_origin(context,'/phenomenonTime'),source_origin(measure,'/phenomenonTime'),equal=matched)
        expected_subject = {k: atom['scope']['subject'][k] for k in ['subjectType', 'subjectRef']}
        target = {'scopeType': expected_subject['subjectType'], 'scopeRef': expected_subject['subjectRef']}
        if context['subject']['subjectType'] == 'SAMPLE':
            compare('CRITERION_SAMPLE_LINK_MISMATCH', context['subject']['subjectRef'], measure.get('sampleRef'), '/context/subject')
            compare('CRITERION_SAMPLE_TARGET_MISMATCH', context.get('targetScope'), target, '/context/targetScope')
        else:
            compare('CRITERION_DIRECT_SUBJECT_MISMATCH', context['subject'], expected_subject, '/context/subject')
        spatial = context['spatialContext']; extent = atom['scope']['extent']
        compare('CRITERION_SPATIAL_SCOPE_MISMATCH', spatial['scope'], target, '/context/spatialContext/scope')
        partial_extent = guard('PARTIAL_EXTENT_POSTURE', extent['posture'] != 'FULL_TARGET_SCOPE',
                               (), (binding_origin(None, '/scope/extent/posture'),))
        if extent['posture'] == 'FULL_TARGET_SCOPE':
            if 'partialExtentRef' in spatial or spatial['spatialBasis'] != 'WHOLE_SCOPE':
                errors.append({'code': 'CRITERION_PARTIAL_OR_UNKNOWN_SOURCE_FOR_WHOLE_CLAIM', 'pointer': '/context/spatialContext'})
        else:
            compare('CRITERION_PARTIAL_EXTENT_SELECTION_MISMATCH', spatial.get('partialExtentRef'), extent['binding']['ref'], '/context/spatialContext/partialExtentRef')
            extent_record = resolve(extent['binding'], 'https://ofarm.dev/schema/partialextent/v0.1', 'CRITERION_SELECTED_PARTIAL_EXTENT',
                                    binding_origin(None, '/scope/extent/binding'),
                                    (measure_context_ready, relation_ready, partial_extent))
            if extent_record is not None:
                compare('CRITERION_PARTIAL_EXTENT_ID_MISMATCH', extent_record['partialExtentId'], extent['binding']['ref'], '/extent/partialExtentId')
                compare('CRITERION_PARTIAL_PARENT_MISMATCH', extent_record['parentScope'], target, '/extent/parentScope')
                # Interpret the original extent clock without changing its text.
                # Omitted end fields do not silently become infinite bounds.
                original_time=extent_record['temporalApplicability'];claim_time=atom['scope']['subjectTime']
                meaning=method.get('extentTemporalMeaning');form=original_time['timeType']
                if meaning is not None:
                    for key,expected,destination in [
                        ('extentBinding',extent['binding'],source_origin(method,'/scope/extent/binding')),
                        ('sourceTimeType',form,source_origin(extent_record,'/temporalApplicability/timeType')),
                        ('timeBasis',original_time['timeBasis'],source_origin(extent_record,'/temporalApplicability/timeBasis'))]:
                        code={'extentBinding':'BINDING','sourceTimeType':'TIME_FORM','timeBasis':'TIME_BASIS'}[key]
                        compare('CRITERION_EXTENT_MEANING_'+code+'_MISMATCH',meaning[key],expected,'/method/extentTemporalMeaning/'+key,
                            source_origin(method,'/extentTemporalMeaning/'+key),destination)
                from extent_temporal import evaluate as extent_time
                checked_time=extent_time(original_time,claim_time,meaning)
                for error in checked_time['errors']:
                    location=('/method' if error['pointer'].startswith('/extentTemporalMeaning') else '/extent')+error['pointer']
                    errors.append({'code':'CRITERION_EXTENT_'+error['code'],'pointer':location})
                missing.extend({'role':'CRITERION_EXTENT_'+role,'pointer':'/extent/temporalApplicability'} for role in checked_time['remainingRoles'])
                if checked_time['coverage'] is not None:
                    code='CRITERION_EXTENT_INSTANT_MISMATCH' if checked_time['pointForm'] else 'CRITERION_EXTENT_DOES_NOT_COVER_CLAIM'
                    compare(code,original_time,claim_time,'/extent/temporalApplicability',
                        source_origin(extent_record,'/temporalApplicability'),source_origin(method,'/scope/subjectTime'),equal=checked_time['coverage'])
    compare('CRITERION_PROPERTY_MISMATCH', measure['observedPropertyRef'], method['propertyBinding']['ref'], '/measurement/observedPropertyRef',
            source_origin(measure,'/observedPropertyRef'),source_origin(method,'/propertyBinding/ref'))
    compare('CRITERION_CONTEXT_PROPERTY_MISMATCH', context['observedPropertyRef'], method['propertyBinding']['ref'], '/context/observedPropertyRef',
            source_origin(context,'/observedPropertyRef'),source_origin(method,'/propertyBinding/ref'))
    compare('CRITERION_MEASUREMENT_METHOD_MISMATCH', measure.get('measurementMethod', {}).get('procedureRef'), method['methodBinding']['ref'], '/measurement/measurementMethod/procedureRef')
    if method['protocolBinding'] is not None:
        compare('CRITERION_SAMPLING_PROTOCOL_MISMATCH', measure.get('samplingProtocol', {}).get('procedureRef'), method['protocolBinding']['ref'], '/measurement/samplingProtocol/procedureRef')
    elif measure.get('samplingProtocol', {}).get('procedureRef') is not None:
        errors.append({'code': 'SOURCE_SAMPLING_PROTOCOL_NOT_SELECTED', 'pointer': '/method/protocolBinding'})
    # The version of the independently selected meaning definition is not the
    # version asserted by the original procedure. Compare the latter to the
    # definition's explicit procedure-version meaning, including digest-selected
    # definitions. Missing or unknown source metadata remains unresolved.
    for source_field, category, label in [('measurementMethod', 'MEASUREMENT_METHOD', 'METHOD'),
                                           ('samplingProtocol', 'SAMPLING_PROTOCOL', 'PROTOCOL')]:
        definition = terms.get(category)
        if definition is None:
            continue
        procedure = measure.get(source_field, {})
        if procedure.get('procedureStatus') == 'UNKNOWN_OR_MISSING':
            missing.append({'role': 'CRITERION_' + label + '_INTERPRETATION', 'pointer': '/' + source_field})
        if 'procedureVersionRef' not in definition:
            missing.append({'role': 'CRITERION_' + label + '_VERSION_MEANING', 'pointer': '/definitionInputs/CRITERION_' + category + '_DEFINITION'})
        elif 'versionRef' not in procedure:
            missing.append({'role': 'CRITERION_' + label + '_ORIGINAL_VERSION', 'pointer': '/' + source_field + '/versionRef'})
        else:
            compare('CRITERION_' + label + '_VERSION_MISMATCH', procedure['versionRef'], definition['procedureVersionRef'],
                '/measurement/' + source_field + '/versionRef', source_origin(measure, '/' + source_field + '/versionRef'),
                source_origin(definition, '/procedureVersionRef'))
    compare('CRITERION_PHENOMENON_TIME_MISMATCH', measure.get('phenomenonTime'), method['phenomenonTime']['sourceProjection'], '/measurement/phenomenonTime',
            source_origin(measure,'/phenomenonTime'),source_origin(method,'/phenomenonTime/sourceProjection'))
    compare('METHOD_TIME_TYPE_MISMATCH', method['phenomenonTime']['timeType'], method['phenomenonTime']['sourceProjection']['timeType'], '/method/phenomenonTime/timeType',
            source_origin(method,'/phenomenonTime/timeType'),source_origin(method,'/phenomenonTime/sourceProjection/timeType'))
    compare('REQUIRED_QUALIFICATION_POINTERS_MISMATCH', source_role['qualificationPointers'], method['qualificationPointers'], '/body/operand/source/qualificationPointers',
            atom_origin('/body/operand/source/qualificationPointers'),source_origin(method,'/qualificationPointers'))
    qualification_fields = ['evidenceClass', 'source', 'samplingProtocol', 'measurementMethod', 'instrument',
                            'calibration', 'labContext', 'result', 'uncertainty', 'chainOfCustodyStatus',
                            'evidenceStatus', 'degradationReasons']
    mandatory = {'/' + key for key in qualification_fields if key in measure}
    if not mandatory <= set(method['qualificationPointers']):
        errors.append({'code': 'INCOMPLETE_MEASUREMENT_QUALIFICATIONS', 'pointer': '/method/qualificationPointers',
                       'missingPointers': sorted(mandatory - set(method['qualificationPointers']))})
    for path in method['qualificationPointers']:
        try:
            pointer(measure, path)
        except ValueError:
            errors.append({'code': 'METHOD_REQUIRED_QUALIFICATION_MISSING', 'pointer': path})
    if 'measuredQualification' in body:
        qualification = body['measuredQualification']
        compare('QUALIFICATION_METHOD_MISMATCH', qualification['methodUseBinding'], criterion['methodUseBinding'], '/body/measuredQualification/methodUseBinding')
        compare('QUALIFICATION_SOURCE_MISMATCH', qualification['sourceBinding'], source_role['measurementBinding'], '/body/measuredQualification/sourceBinding')
        compare('QUALIFICATION_INTERPRETATION_MISMATCH', qualification['interpretation'], method['qualificationInterpretation'], '/body/measuredQualification/interpretation')
        if qualification['sourcePointer'] not in method['qualificationPointers']:
            errors.append({'code': 'UNSELECTED_QUALIFICATION_POINTER', 'pointer': '/body/measuredQualification/sourcePointer'})
    elif method['qualificationInterpretation'] != 'NOT_APPLICABLE_BY_BOUND_METHOD':
        errors.append({'code': 'METHOD_REQUIRED_MEASURED_QUALIFICATION_MISSING', 'pointer': '/body/measuredQualification'})
    quality = method['sourceResultQualification']
    if measure['evidenceStatus'] not in quality['permittedEvidenceStatuses']:
        errors.append({'code': 'MEASUREMENT_STATUS_NOT_ELIGIBLE_FOR_SELECTED_USE', 'pointer': '/measurement/evidenceStatus'})
    compare('SOURCE_DEGRADATION_QUALIFICATION_MISMATCH', measure.get('degradationReasons', []), quality['requiredDegradationReasons'], '/measurement/degradationReasons')
    result = measure['result']; kind = result['resultKind']
    if kind not in criterion['permittedResultKinds']:
        errors.append({'code': 'RESULT_KIND_NOT_PERMITTED_BY_CRITERION', 'pointer': '/measurement/result/resultKind'})
    compare('SOURCE_RESULT_KIND_MISMATCH', body['operand']['resultKind'], kind, '/body/operand/resultKind',
            atom_origin('/body/operand/resultKind'),source_origin(measure,'/result/resultKind'))
    if quality['requireOriginalLexicalValue'] and not isinstance(result.get('originalLexicalValue'), str):
        errors.append({'code': 'REQUIRED_ORIGINAL_RESULT_LEXICAL_MISSING', 'pointer': '/measurement/result/originalLexicalValue'})

    numeric_kind = kind in ['NUMERIC', 'CENSORED_NUMERIC']
    numeric_guard = guard('NUMERIC_OR_CENSORED_RESULT', numeric_kind, (measurement_index,),
                          (binding_origin(measure, '/result/resultKind'),))
    if numeric_kind:
        scalar_rule = method['scalarSource']
        scalar_guard = guard('SCALAR_SOURCE_SELECTED', scalar_rule is not None, (method_index,),
                             (binding_origin(method, '/scalarSource'),))
        if scalar_rule is None:
            errors.append({'code': 'SELECTED_ORIGINAL_SCALAR_SOURCE_REQUIRED', 'pointer': '/method/scalarSource'})
        else:
            scalar_record = resolve(scalar_rule['binding'], 'https://ofarm.dev/schema/executionrecordpayload/v0.1',
                                    'CRITERION_CAPTURED_SCALAR_SOURCE', binding_origin(method, '/scalarSource/binding'),
                                    (measure_context_ready, numeric_guard, scalar_guard))
            quantity = body['operand']['quantity' if kind == 'NUMERIC' else 'limit']
            scalar_path = '/actualQuantityParameters/' + str(scalar_rule['parameterIndex'])
            compare('CRITERION_SCALAR_USE_MISMATCH', scalar_rule['use'], 'NUMERIC_READING' if kind == 'NUMERIC' else 'DETECTION_LIMIT', '/method/scalarSource/use')
            provenance = quantity['provenance']
            compare('CRITERION_SCALAR_BINDING_MISMATCH', provenance['sourceBinding'], scalar_rule['binding'], '/body/operand/provenance/sourceBinding')
            for key, suffix in [('valuePointer', '/value'), ('lexicalPointer', '/reportedValue'), ('qualifierPointer', '/qualifier')]:
                compare('CRITERION_SCALAR_POINTER_MISMATCH', provenance[key], scalar_path + suffix, '/body/operand/provenance/' + key)
            if scalar_record is not None:
                try:
                    scalar = pointer(scalar_record, scalar_path)
                    for claimed, original in [('quantityKind', 'quantityKindRef'), ('unit', 'unitRef'),
                                               ('qualifier', 'qualifier'), ('originalLexicalValue', 'reportedValue')]:
                        compare('CRITERION_CAPTURED_SCALAR_' + claimed.upper() + '_MISMATCH', quantity[claimed], scalar.get(original), scalar_path + '/' + original,
                                atom_origin('/body/operand/'+('quantity' if kind=='NUMERIC' else 'limit')+'/'+claimed),
                                source_origin(scalar_record,scalar_path+'/'+original) if original in scalar else None)
                    if Decimal(quantity['decimal']) != Decimal(str(scalar['value'])):
                        errors.append({'code': 'CRITERION_CAPTURED_SCALAR_VALUE_MISMATCH', 'pointer': scalar_path + '/value'})
                    compare('CRITERION_CAPTURED_SCALAR_ROLE_MISMATCH', scalar['parameterRole'], scalar_rule['parameterRole'], scalar_path + '/parameterRole')
                    if measure['measurementEvidenceId'] not in scalar.get('evidenceRefs', []):
                        errors.append({'code': 'CRITERION_SCALAR_MEASUREMENT_LINK_MISSING', 'pointer': scalar_path + '/evidenceRefs'})
                    compare('CRITERION_SCALAR_UNIT_PROFILE_MISMATCH', quantity['unitProfile'], method['quantityContext']['unitProfile'], '/body/operand/unitProfile')
                    if 'originalUnitText' in quantity:
                        compare('CRITERION_SCALAR_UNIT_TEXT_MISMATCH', quantity['originalUnitText'], scalar.get('reportedUnitLabel'), scalar_path + '/reportedUnitLabel')
                except (ValueError, KeyError, TypeError):
                    errors.append({'code': 'CRITERION_CAPTURED_SCALAR_FIELDS_MISSING', 'pointer': scalar_path})
    elif method['scalarSource'] is not None:
        errors.append({'code': 'CRITERION_UNSELECTED_SCALAR_SOURCE', 'pointer': '/method/scalarSource'})
    coded_guard = guard('CODED_RESULT', kind == 'CODED', (measurement_index,),
                        (binding_origin(measure, '/result/resultKind'),))
    qualitative_guard = guard('QUALITATIVE_RESULT', kind == 'QUALITATIVE', (measurement_index,),
                              (binding_origin(measure, '/result/resultKind'),))
    if kind == 'CODED':
        term(body['operand']['codedValue'], 'CODED_RESULT', '/body/operand/codedValue',
             binding_origin(None, '/body/operand/codedValue'), (measure_context_ready, coded_guard))
    elif kind == 'QUALITATIVE':
        term(body['operand']['scaleBinding'], 'QUALITATIVE_SCALE', '/body/operand/scaleBinding',
             binding_origin(None, '/body/operand/scaleBinding'), (measure_context_ready, qualitative_guard))

    def threshold(claimed, fixed, path, definition_path):
        compare('INDEPENDENT_THRESHOLD_MISMATCH', {k: v for k, v in claimed.items() if k != 'provenance'}, fixed, path)
        for key in fixed:
            if key in claimed:
                compare('INDEPENDENT_THRESHOLD_FIELD_'+key.upper()+'_MISMATCH',claimed[key],fixed[key],path+'/'+key,
                        atom_origin(path+'/'+key),source_origin(criterion,definition_path+'/'+key))
        provenance = claimed.get('provenance', {})
        compare('THRESHOLD_SOURCE_BINDING_MISMATCH', provenance.get('sourceBinding'), body['criterion'], path + '/provenance/sourceBinding')
        for field, suffix in [('valuePointer', '/decimal'), ('lexicalPointer', '/originalLexicalValue'), ('qualifierPointer', '/qualifier')]:
            compare('THRESHOLD_SOURCE_POINTER_MISMATCH', provenance.get(field), definition_path + suffix, path + '/provenance/' + field)
        for key in ['quantityKind', 'unit', 'unitProfile']:
            compare('METHOD_THRESHOLD_QUANTITY_CONTEXT_MISMATCH', fixed[key], method['quantityContext'][key], path + '/' + key)
    if criterion['operator'] == 'BETWEEN':
        if not all(k in body['threshold'] for k in ['lower', 'upper']):
            errors.append({'code': 'CRITERION_THRESHOLD_FORM_MISMATCH', 'pointer': '/body/threshold'})
        else:
            for side in ['lower', 'upper']:
                threshold(body['threshold'][side], criterion['threshold'][side], '/body/threshold/' + side, '/threshold/' + side)
            for key in ['lowerInclusive', 'upperInclusive']:
                compare('THRESHOLD_BOUNDARY_MISMATCH', body['threshold'][key], criterion['threshold'][key], '/body/threshold/' + key)
    elif 'decimal' in body['threshold']:
        threshold(body['threshold'], criterion['threshold'], '/body/threshold', '/threshold')
    else:
        errors.append({'code': 'CRITERION_THRESHOLD_FORM_MISMATCH', 'pointer': '/body/threshold'})
    no_errors = guard('NO_ERRORS_BEFORE_ADMISSIBLE_SET', not errors,
                      range(len(reads)) if reads is not None else (), diagnostic_state=True)
    if errors:
        return finish()

    def decimal(value):
        if type(value) not in [int, float]:
            raise ValueError('The selected actual source field is not numeric.')
        return format(Decimal(str(value)), 'f')

    admissible = None; mapping_context = None
    try:
        if kind == 'NUMERIC':
            for key, source_key in [('quantityKind', 'quantityKindRef'), ('unit', 'unitRef')]:
                compare('METHOD_RESULT_QUANTITY_CONTEXT_MISMATCH', result[source_key], method['quantityContext'][key], '/measurement/result/' + source_key)
            if method['numericSet']['kind'] == 'EXACT_POINT':
                d = decimal(result['numericValue'])
                admissible = {'kind': 'INTERVAL', 'lower': {'decimal': d, 'inclusive': True}, 'upper': {'decimal': d, 'inclusive': True}, 'basis': 'EXACT_NUMERIC_POINT'}
            else:
                if method['qualificationInterpretation'] != 'METHOD_DEFINED_HARD_BOUND':
                    errors.append({'code': 'HARD_INTERVAL_REQUIRES_EXPLICIT_METHOD_INTERPRETATION', 'pointer': '/method/numericSet'})
                rule = method['numericSet']
                admissible = {'kind': 'INTERVAL', 'lower': {'decimal': decimal(pointer(measure, rule['lowerPointer'])), 'inclusive': rule['lowerInclusive']},
                              'upper': {'decimal': decimal(pointer(measure, rule['upperPointer'])), 'inclusive': rule['upperInclusive']}, 'basis': 'METHOD_DEFINED_HARD_BOUND'}
        elif kind == 'CENSORED_NUMERIC':
            matching = [r for r in method['censoringRules'] if r['qualifier'] == result['censoringQualifier'] and r['limitType'] == result['detectionLimit']['limitType']]
            if len(matching) != 1:
                errors.append({'code': 'EXACT_CENSORING_RULE_REQUIRED', 'pointer': '/method/censoringRules'})
            else:
                rule = matching[0]
                compare('CENSORING_NONNEGATIVE_MEANING_MISMATCH', body['operand']['nonnegative'], rule['nonnegative'], '/body/operand/nonnegative')
                def endpoint(spec):
                    if spec['origin'] == 'UNBOUNDED':
                        return {'kind': 'UNBOUNDED'}
                    return {'decimal': '0' if spec['origin'] == 'ZERO' else decimal(result['detectionLimit']['value']), 'inclusive': spec['inclusive']}
                admissible = {'kind': 'INTERVAL', 'lower': endpoint(rule['lower']), 'upper': endpoint(rule['upper']), 'basis': rule['basis']}
        elif kind in ['CODED', 'QUALITATIVE']:
            mapping_guard = guard('RESULT_MAPPING_SELECTED', method['mappingBinding'] is not None,
                                  (method_index,), (binding_origin(method, '/mappingBinding'),))
            if method['mappingBinding'] is None:
                errors.append({'code': 'MAPPING_DEFINITION_REQUIRED', 'pointer': '/method/mappingBinding'})
            else:
                mapping = resolve(method['mappingBinding'], SCHEMAS['mapping']['$id'], 'SELECTED_RESULT_MAPPING_DEFINITION',
                                  binding_origin(method, '/mappingBinding'),
                                  (no_errors, coded_guard if kind == 'CODED' else qualitative_guard, mapping_guard))
                compare('MAPPING_SELECTION_MISMATCH', body['operand']['mappingBinding'], method['mappingBinding'], '/body/operand/mappingBinding')
                if mapping is not None:
                    compare('MAPPING_METHOD_QUANTITY_CONTEXT_MISMATCH', mapping['quantityContext'], method['quantityContext'], '/mapping/quantityContext')
                    source_value = result['codedValueRef' if kind == 'CODED' else 'qualitativeValue']
                    rows = [v for v in mapping['entries'] if v['resultKind'] == kind and v['sourceValue'] == source_value]
                    if len(rows) != 1:
                        errors.append({'code': 'UNIQUE_EXACT_SOURCE_VALUE_MAPPING_REQUIRED', 'pointer': '/mapping/entries'})
                    else:
                        admissible = {'kind': 'INTERVAL', **rows[0]['admissibleValues'], 'basis': rows[0]['basis']}
                        mapping_context = {'mappingBinding': method['mappingBinding'], **mapping['quantityContext']}
    except (ValueError, KeyError, TypeError) as exc:
        errors.append({'code': 'SOURCE_ADMISSIBLE_SET_INPUT_ERROR', 'pointer': '/measurement', 'detail': str(exc)})
    if admissible is not None:
        compare('SOURCE_DERIVED_ADMISSIBLE_SET_MISMATCH', body['operand'].get('admissibleValues'), admissible, '/body/operand/admissibleValues')
    if errors or missing:
        return finish()
    property_term = terms.get('OBSERVED_PROPERTY')
    observation = property_term.get('observationMeaning') if property_term is not None else None
    if observation is not None:
        for key, field in [('quantityKind', 'quantityKindRef'), ('unit', 'unitRef')]:
            compare('CRITERION_STAND_COUNT_' + key.upper() + '_MISMATCH', method['quantityContext'][key], observation[key],
                    '/method/quantityContext/' + key, source_origin(method, '/quantityContext/' + key),
                    source_origin(property_term, '/observationMeaning/' + key))
            if field in measure['result']:
                compare('CRITERION_STAND_COUNT_RESULT_' + key.upper() + '_MISMATCH', measure['result'][field], observation[key],
                        '/measurement/result/' + field, source_origin(measure, '/result/' + field),
                        source_origin(property_term, '/observationMeaning/' + key))
        # This definition expressly interprets an exact nonnegative integer
        # count. Other result/uncertainty forms need their own selected meaning;
        # no continuous bound, qualitative label or pending value becomes a count.
        if kind != 'NUMERIC' or method['numericSet']['kind'] != 'EXACT_POINT':
            missing.append({'role': 'EXACT_OBSERVED_STAND_COUNT_RESULT_INTERPRETATION', 'pointer': '/result'})
        else:
            value = Decimal(decimal(measure['result']['numericValue']))
            valid_count = value >= 0 and value == value.to_integral_value()
            comparisons.append({'predicateId': 'CRITERION_STAND_COUNT_RESULT_DOMAIN_MISMATCH',
                'source': {**source_origin(measure, '/result/numericValue'), 'valueDigest': digest(measure['result']['numericValue'])},
                'destination': {**source_origin(property_term, '/observationMeaning/resultDomain'), 'valueDigest': digest(observation['resultDomain'])},
                'disposition': 'PASS' if valid_count else 'FAIL'})
            if not valid_count:
                errors.append({'code': 'CRITERION_STAND_COUNT_RESULT_DOMAIN_MISMATCH', 'pointer': '/result/numericValue'})
    mathematical_atom = atom
    count_meaning = property_term.get('completionCountMeaning') if property_term is not None else None
    if count_meaning is not None:
        from completion_count_meanings import refine_interval, MEANINGS
        normative = MEANINGS[count_meaning['activityRow']]
        compare('CRITERION_COUNT_DOMAIN_MEANING_MISMATCH', count_meaning, normative, '/property/completionCountMeaning',
                source_origin(property_term, '/completionCountMeaning'),
                {'inputRole': 'COMPLETION_COUNT_MEANINGS', 'pointer': '/definitions/' + count_meaning['activityRow']})
        for field in ['quantityKind', 'unit']:
            compare('CRITERION_COUNT_DOMAIN_' + field.upper() + '_MISMATCH', method['quantityContext'][field], count_meaning[field],
                    '/method/quantityContext/' + field, source_origin(method, '/quantityContext/' + field),
                    source_origin(property_term, '/completionCountMeaning/' + field))
        if errors or missing: return finish()
        if admissible is None:
            # Pending output has no value set to intersect. Preserve the normal
            # pending-result outcome and every validated source qualification.
            mathematical = MeaningComparisons().criterion(atom, copy.deepcopy(atom), mapping_context)
            errors.extend(mathematical['errors'])
            return finish(mathematical.get('conditionalMathematicalOutcome'))
        refined = refine_interval(admissible); errors.extend(refined['errors'])
        domain_interpretation = {'domain': count_meaning['domain'],
            'interpretationKind': 'DERIVED_VALUE_SET_NOT_ORIGINAL_SOURCE_FIELDS',
            'propertyDefinitionBinding': method['propertyBinding'],
            'meaningDefinitionBinding': {'ref': normative['definitionId'], 'digest': digest(normative)},
            'sourceAdmissibleValues': copy.deepcopy(admissible), 'effectiveAdmissibleValues': refined['interval']}
        if errors or missing: return finish()
        mathematical_atom = copy.deepcopy(atom)
        mathematical_atom['body']['operand']['admissibleValues'] = refined['interval']
    mathematical = MeaningComparisons().criterion(mathematical_atom, copy.deepcopy(mathematical_atom), mapping_context)
    if count_meaning is None:
        errors.extend(mathematical['errors'])
    else:
        from completion_count_meanings import criterion_outcome
        # Keep every schema, source, quantity-context and threshold failure.
        # Only the final allegation/outcome comparison uses the selected
        # discrete domain instead of the interval's continuous hull.
        errors.extend(v for v in mathematical['errors'] if v['code'] != 'ALLEGED_CRITERION_OUTCOME_MISMATCH')
        outcome = criterion_outcome(refined['interval'], body['operator'], body['threshold'])
        domain_interpretation['continuousHullOutcome'] = mathematical.get('conditionalMathematicalOutcome')
        domain_interpretation['integerDomainOutcome'] = outcome
        if body['allegedOutcome'] != outcome:
            errors.append({'code': 'ALLEGED_CRITERION_OUTCOME_MISMATCH', 'pointer': '/body/allegedOutcome', 'expected': outcome})
        mathematical['conditionalMathematicalOutcome'] = outcome
    if observation is not None and not errors and not missing:
        selected_measurement = next(v for v in sources if same(v['binding'], source_role['measurementBinding']))
        observation_selection = {'concept': observation['concept'], 'conceptOrigin': source_origin(property_term, '/observationMeaning/concept'),
            'propertyDefinitionBinding': method['propertyBinding'], 'measurementBinding': source_role['measurementBinding'],
            'measurementInputId': selected_measurement['id'], 'measurementRawSha256': selected_measurement['rawSha256'],
            'measurementValueDigest': selected_measurement['valueDigest']}
    return finish(mathematical.get('conditionalMathematicalOutcome'))
