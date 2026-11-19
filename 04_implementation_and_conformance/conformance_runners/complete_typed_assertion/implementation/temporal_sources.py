"""Domain-owned temporal source selection over original resolved records."""
from strict_inputs import same, digest
from time_validation import foreign_instant, foreign_seconds


from domain_reader_occurrences import reader, selection as observe_selection, guard as observe_guard, origin as read_origin, observed_shape, branch as observed_branch, observe_comparisons


@reader('temporal_sources.py', ['AR_SUBJECT_TIME', 'PC_SUBJECT_TIME'])
def evaluate(intent, sources, schemas):
    from runtime_support import Values
    values = Values(schemas)
    time, body = intent['subjectTime'], intent['assertionBody']
    errors, missing, comparisons, ids = [], [], [], []
    errors.extend(values.time_errors(time))
    def predicate(code, okay, operands, *, depends_on=()):
        """Observe an existing decision without changing ordinary reader facts."""
        fact = {'predicateId': code, 'source': operands[0],
                'disposition': 'PASS' if okay else 'FAIL'}
        if len(operands) > 1:
            fact['destination'] = operands[1]
        return observe_comparisons([fact], depends_on=depends_on)
    def equal(code, left, right, source_path, destination_path, source_role='EFFECT_INTENT', semantic_equal=None, depends_on=()):
        okay = same(left, right) if semantic_equal is None else semantic_equal
        comparisons.append({'predicateId': code, 'sourcePointer': source_path, 'destinationPointer': destination_path,
                            'sourceValueDigest': digest(left), 'destinationValueDigest': digest(right), 'equal': okay,
                            'source': {'inputRole': source_role, 'pointer': source_path, 'valueDigest': digest(left)},
                            'destination': {'inputRole': 'EFFECT_INTENT', 'pointer': destination_path, 'valueDigest': digest(right)},
                            'disposition': 'PASS' if okay else 'FAIL'})
        findings = (['AR_SUBJECT_TIME', 'PC_SUBJECT_TIME', 'AR_OPERATION_PAYLOADS']
                    if code == 'PAYLOAD_TIME_BASIS_MISMATCH' else None)
        observe_comparisons([comparisons[-1]], findings=findings, depends_on=depends_on)
        if not okay:
            errors.append({'code': code, 'pointer': destination_path})
    def time_equal(code, left, right, source_path, destination_path, source_role, *, depends_on=()):
        operands = [read_origin(source_role, source_path), read_origin('EFFECT_INTENT', destination_path)]
        dependencies = list(depends_on)
        parsed_operands = operands[:1]
        try:
            parsed=foreign_instant(left)
            known = not parsed['unknownLocalOffset']
            observed = observe_guard('TEMPORAL_SOURCE_KNOWN_INSTANT', known, origins=parsed_operands,
                                     depends_on=dependencies)
            if observed is not None: dependencies.append(observed)
            if not known:
                missing.append({'role':'TEMPORAL_SOURCE_KNOWN_INSTANT_INTERPRETATION','pointer':source_path})
                return None
            parsed_operands = operands
            okay=parsed['seconds']==foreign_seconds(right)
        except (ValueError,TypeError):
            predicate('TEMPORAL_SOURCE_INSTANT_INVALID', False, parsed_operands, depends_on=dependencies)
            errors.append({'code':'TEMPORAL_SOURCE_INSTANT_INVALID','pointer':source_path})
            return None
        equal(code,left,right,source_path,destination_path,source_role,semantic_equal=okay,depends_on=dependencies)
        return okay
    if observed_branch('TEMPORAL_BASIS_ABSENCE', 'temporalBasis' not in body, origins=[read_origin('EFFECT_INTENT', '/assertionBody/temporalBasis')]):
        equal('BODY_APPLICABILITY_TIME_MISMATCH', time, body['applicability'], '/subjectTime', '/assertionBody/applicability')
    else:
        basis = body['temporalBasis']; kind = basis['sourceKind']
        if observed_branch('TEMPORAL_BODY_TIME', kind == 'BODY_TIME', origins=[read_origin('EFFECT_INTENT', '/assertionBody/temporalBasis/sourceKind')]):
            equal('BODY_TIME_BASIS_MISMATCH', time, basis['time'], '/subjectTime', '/assertionBody/temporalBasis/time')
        else:
            wrapper = basis['evidenceBinding' if kind == 'MEASUREMENT_EVIDENCE' else 'payloadBinding']
            binding = {k: wrapper[k] for k in ['ref', 'revisionRef', 'digest'] if k in wrapper}
            selected = [v for v in sources if same(v['binding'], binding)]
            observe_selection('TEMPORAL_SOURCE', sources, selected, binding=binding,
                origins=[read_origin('EFFECT_INTENT', '/assertionBody/temporalBasis/sourceKind'),
                    read_origin('EFFECT_INTENT', '/assertionBody/temporalBasis/' + ('evidenceBinding' if kind == 'MEASUREMENT_EVIDENCE' else 'payloadBinding'))])
            if len(selected) != 1:
                missing.append({'role': 'EXACT_SELECTED_TEMPORAL_SOURCE', 'pointer': '/assertionBody/temporalBasis'})
            else:
                source = selected[0]; record = source['record']; ids.append(source['id'])
                errors.extend(observed_shape(schemas, wrapper['schemaRef'], record))
                if not errors:
                    id_field={'MEASUREMENT_EVIDENCE':'measurementEvidenceId',
                              'INTERVENTION_INTENT_PAYLOAD':'interventionIntentPayloadId',
                              'EXECUTION_RECORD_PAYLOAD':'executionRecordPayloadId'}[kind]
                    wrapper_field='evidenceBinding' if kind=='MEASUREMENT_EVIDENCE' else 'payloadBinding'
                    equal('TEMPORAL_SOURCE_IDENTITY_MISMATCH', record[id_field], binding['ref'], '/'+id_field,
                          '/assertionBody/temporalBasis/'+wrapper_field+'/ref', source['id'])
                    if kind == 'MEASUREMENT_EVIDENCE':
                        selected_role = body.get('temporalQualifications', {}).get('sourceTimeBasis', 'ABSENT')
                        phenomenon=record['phenomenonTime']
                        instant_type = phenomenon['timeType']=='INSTANT'
                        predicate('PERFORMANCE_REQUIRES_INSTANT', instant_type, [read_origin(source['id'], '/phenomenonTime/timeType')])
                        if not instant_type:errors.append({'code':'PERFORMANCE_REQUIRES_INSTANT','pointer':'/phenomenonTime/timeType'})
                        performed_profile = time['profile']=='PERFORMED_INSTANT'
                        predicate('PERFORMANCE_PROFILE_MISMATCH', performed_profile, [read_origin('EFFECT_INTENT', '/subjectTime/profile')])
                        if not performed_profile:errors.append({'code':'PERFORMANCE_PROFILE_MISMATCH','pointer':'/subjectTime/profile'})
                        qualifier_operands = [read_origin(source['id'], '/phenomenonTime/timeBasis'),
                                              read_origin('EFFECT_INTENT', '/assertionBody/temporalQualifications/sourceTimeBasis')]
                        if selected_role=='ABSENT':
                            qualifier_absent = 'timeBasis' not in phenomenon
                            predicate('TIME_QUALIFIER_PRESENCE_MISMATCH', qualifier_absent, qualifier_operands)
                            if not qualifier_absent:errors.append({'code':'TIME_QUALIFIER_PRESENCE_MISMATCH','pointer':'/phenomenonTime/timeBasis'})
                        else:
                            qualifier_allowed = selected_role in ['OBSERVED_TIME','SAMPLE_TIME','RESULT_TIME','RECORD_TIME','ESTIMATED_TIME']
                            qualifier_matches = qualifier_allowed and phenomenon.get('timeBasis')==selected_role
                            predicate('TIME_QUALIFIER_MISMATCH', qualifier_matches,
                                      qualifier_operands if qualifier_allowed else [qualifier_operands[1]])
                            if not qualifier_matches:errors.append({'code':'TIME_QUALIFIER_MISMATCH','pointer':'/phenomenonTime/timeBasis'})
                        instant_present = 'instant' in phenomenon
                        available = instant_present and 'at' in time
                        instant_operands = [read_origin(source['id'], '/phenomenonTime/instant')]
                        if instant_present: instant_operands.append(read_origin('EFFECT_INTENT', '/subjectTime/at'))
                        availability = observe_guard('TEMPORAL_INSTANT_FIELDS_PRESENT', available, origins=instant_operands)
                        if available:
                            compared=time_equal('MEASUREMENT_PHENOMENON_TIME_MISMATCH', phenomenon['instant'], time['at'],
                                  '/phenomenonTime/instant', '/subjectTime/at', source['id'],
                                  depends_on=[availability] if availability is not None else [])
                            if compared is False:errors.append({'code':'PHENOMENON_TIME_MISMATCH','pointer':'/phenomenonTime/instant'})
                        else:
                            predicate('INVALID_TIME', False, instant_operands,
                                      depends_on=[availability] if availability is not None else [])
                            errors.append({'code':'INVALID_TIME','pointer':'/phenomenonTime/instant'})
                        if 'timeBasis' in record['phenomenonTime'] and 'sourceTimeBasis' in body.get('temporalQualifications', {}):
                            equal('MEASUREMENT_TIME_BASIS_MISMATCH', record['phenomenonTime']['timeBasis'], selected_role,
                                  '/phenomenonTime/timeBasis', '/assertionBody/temporalQualifications/sourceTimeBasis', source['id'])
                        # Coincident time alone cannot identify the activity,
                        # property, method or finish condition being measured.
                        missing.append({'role': 'OPERATION_SPECIFIC_MEASUREMENT_PROPERTY_RESULT_CONTEXT_METHOD_USE',
                                        'pointer': '/assertionBody/temporalBasis/evidenceBinding'})
                    else:
                        field = 'intendedTimeWindow' if kind == 'INTERVENTION_INTENT_PAYLOAD' else 'effectiveTimeInterval'
                        for member in ['start', 'end']:
                            original = record[field][member]
                            time_equal('PAYLOAD_TIME_BASIS_MISMATCH', original, time[member], '/' + field + '/' + member, '/subjectTime/' + member, source['id'])
                        if kind == 'INTERVENTION_INTENT_PAYLOAD':
                            supported = record[field].get('timeBasis') in ['PLANNED_WINDOW', 'PRESCRIPTION_WINDOW']
                            observe_guard('INTENDED_PAYLOAD_TIME_BASIS_SUPPORTED', supported,
                                          origins=[read_origin(source['id'], '/' + field + '/timeBasis')])
                            if not supported:
                                missing.append({'role': 'INTENDED_PAYLOAD_TIME_BASIS_INTERPRETATION', 'pointer': '/' + field + '/timeBasis'})
                        else:
                            supported = record[field].get('timeBasis') == 'EXECUTION_INTERVAL'
                            observe_guard('EXECUTION_PAYLOAD_TIME_BASIS_SUPPORTED', supported,
                                          origins=[read_origin(source['id'], '/' + field + '/timeBasis')])
                            if not supported:
                                missing.append({'role': 'EXECUTION_PAYLOAD_TIME_BASIS_INTERPRETATION', 'pointer': '/' + field + '/timeBasis'})
    return {'disposition': 'FAIL' if errors else 'NOT_EVALUATED' if missing else 'PASS',
            'errors': errors, 'remainingRoles': missing, 'comparisons': comparisons, 'sourceInputIds': ids}
