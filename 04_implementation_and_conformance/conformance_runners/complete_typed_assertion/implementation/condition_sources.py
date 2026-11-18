"""Compute a work condition from original evidence and its normative criterion.

There is no expected-atom input. The internal criterion operand is constructed
from the selected source fields; SATISFIED is the fixed meaning of a required
work condition. The normal criterion engine independently rechecks source,
method, property, qualifications, extent and exact scalar provenance.
"""
import copy
from decimal import Decimal
from strict_inputs import same,digest
from definition_inputs import SCHEMAS,register
from activity_condition_meanings import activity_predicate
from completion_count_meanings import MEANINGS as COMPLETION_COUNTS


def condition_reader_kind(condition):
    """Select the existing condition reader without interpreting its result."""
    if condition['activityRow']=='O22' and condition['stage']=='FINISH':
        return 'ANALYSIS_OUTPUT'
    if condition['activityRow']=='O09' and condition['stage']=='FINISH':
        return 'OBSERVATION_ACQUISITION'
    return 'CRITERION_MEASUREMENT'


def condition_linked_reader(condition):
    """Select the existing pre-error-gate row reader, respecting prior branches."""
    row, stage = condition['activityRow'], condition['stage']
    if stage != 'FINISH' or row == 'O08' or row in COMPLETION_COUNTS:
        return None
    if row == 'O04' and condition['predicateKind'] in ['IRRIGATION_REQUIRED_VOLUME_DELIVERED', 'IRRIGATION_INFLOW_ZERO_AT_FINISH']:
        return 'IRRIGATION'
    if row == 'O17' and condition['predicateKind'] in ['SANITATION_REQUIRED_CONTINUOUS_MATERIAL_CONTACT', 'SANITATION_PROCEDURE_INACTIVE_AT_FINISH']:
        return 'SANITATION'
    if row == 'O07': return 'DRYING'
    if row == 'O10': return 'SAMPLE_COLLECTION'
    return None


def condition_required_unit(condition):
    """Return the unit from the existing fixed-unit branches only."""
    if condition['stage'] in ('START', 'IN_PROGRESS') or condition['activityRow'] == 'O08':
        return 'ofarm.unit:count' if condition['stage'] == 'FINISH' else 'ofarm.unit:boolean'
    if condition_linked_reader(condition) == 'SAMPLE_COLLECTION':
        return 'ofarm.unit:boolean'
    return None


def condition_activity_quantity_kind(condition):
    """Return the existing activity/O08 branch's required quantity kind."""
    if condition['stage'] in ('START', 'IN_PROGRESS') or condition['activityRow'] == 'O08':
        return ('ofarm.quantitykind:SelectedPlantElementCount' if condition['stage'] == 'FINISH'
                else 'ofarm.quantitykind:ActivityPresence')
    return None


def condition_activity_operator(condition):
    """Return the existing activity/O08 branch's required operator."""
    if condition['stage'] in ('START', 'IN_PROGRESS') or condition['activityRow'] == 'O08':
        return 'LE' if condition['stage'] == 'FINISH' else 'GE'
    return None


def condition_activity_predicate_kind(condition):
    """Return the existing activity/O08 branch's fixed predicate kind."""
    if condition['stage'] in ('START', 'IN_PROGRESS') or condition['activityRow'] == 'O08':
        return ('NO_SELECTED_PLANT_ELEMENTS_REMAINING' if condition['stage'] == 'FINISH'
                else activity_predicate(condition['activityRow'], condition['stage']))
    return None


def condition_activity_threshold_decimal(condition):
    """Return the existing activity/O08 branch's fixed threshold decimal."""
    if condition['stage'] in ('START', 'IN_PROGRESS') or condition['activityRow'] == 'O08':
        return '0' if condition['stage'] == 'FINISH' else '1'
    return None


def condition_activity_threshold_qualifier(condition):
    """Return the existing activity/O08 branch's fixed threshold qualifier."""
    if condition['stage'] in ('START', 'IN_PROGRESS') or condition['activityRow'] == 'O08':
        return 'EXACT'
    return None


def resolve_condition_inputs(condition, read):
    """Read the generic condition's initial inputs through the caller's seam.

    The caller owns selection, validation and provenance. Preserve the reader's
    early returns: measurement is attempted even when method is unavailable,
    while property is reached only after both inputs resolve.
    """
    criterion_def=read(condition,'criterionBinding',SCHEMAS['criterion']['$id'],'WORK_CONDITION_CRITERION',())
    if criterion_def is None:return None
    method=read(criterion_def,'methodUseBinding',SCHEMAS['method']['$id'],'WORK_CONDITION_METHOD',(criterion_def,))
    measurement=read(condition,'measurementBinding','https://ofarm.dev/schema/measurementevidence/v0.1','WORK_CONDITION_MEASUREMENT',(criterion_def,))
    if method is None or measurement is None:return None
    property_definition=read(method,'propertyBinding',SCHEMAS['term']['$id'],'WORK_CONDITION_PROPERTY_DEFINITION',(method,measurement))
    if property_definition is None:return None
    return criterion_def,method,measurement,property_definition


def _condition_coded_value_index(condition, value):
    selected = [index for index, binding in enumerate(condition['resultTerms']['codedValues'])
                if binding['ref'] == value]
    if len(selected) != 1:
        raise ValueError('Exact independently selected result term unavailable.')
    return selected[0]


def condition_criterion_binding_origins(condition, method, measurement):
    """Map constructed C04 read bindings and guards to original fields.

    Inputs must be the schema-checked originals used by the constructor. These
    paths describe its selection only; they do not admit or authenticate a source.
    """
    origins = {
        '/body/criterion': {'recordKind': 'condition', 'pointer': '/criterionBinding', 'guards': []},
        '/body/operand/source/measurementBinding': {
            'recordKind': 'condition', 'pointer': '/measurementBinding', 'guards': []},
        '/scope/extent/posture': {'recordKind': 'method', 'pointer': '/scope/extent/posture', 'guards': []}}
    extent = method['scope']['extent']
    if 'binding' in extent:
        origins['/scope/extent/binding'] = {
            'recordKind': 'method', 'pointer': '/scope/extent/binding',
            'guards': [{'recordKind': 'method', 'pointer': '/scope/extent/posture'}]}
    kind = measurement['result']['resultKind']
    if kind == 'CODED':
        index = _condition_coded_value_index(condition, measurement['result']['codedValueRef'])
        origins['/body/operand/codedValue'] = {
            'recordKind': 'condition', 'pointer': '/resultTerms/codedValues/' + str(index),
            'guards': [{'recordKind': 'measurement', 'pointer': '/result/resultKind'},
                       {'recordKind': 'measurement', 'pointer': '/result/codedValueRef'},
                       {'recordKind': 'condition', 'pointer': '/resultTerms/codedValues'}]}
    elif kind == 'QUALITATIVE' and condition['resultTerms']['qualitativeScale'] is not None:
        origins['/body/operand/scaleBinding'] = {
            'recordKind': 'condition', 'pointer': '/resultTerms/qualitativeScale',
            'guards': [{'recordKind': 'measurement', 'pointer': '/result/resultKind'}]}
    return origins


def condition_property_comparisons(condition, property_definition, work_atom, *,
                                   condition_binding, work_specification_binding, procedure_binding):
    """Describe the reader's property-link predicates and original operand paths.

    The aggregate compares meaning to a selection-derived expectation, while
    retaining the original condition as its displayed right-hand operand.
    Callers must retain the three selected binding inputs as well.
    """
    meaning = property_definition.get('workConditionMeaning')
    code = 'WORK_CONDITION_PROPERTY_SEMANTIC_LINK_MISMATCH'
    if not isinstance(meaning, dict):
        return [{'code': code, 'actual': None, 'expected': condition,
                 'sourcePointer': '/workConditionMeaning', 'sourcePresent': False,
                 'destinationKind': 'condition', 'destinationPointer': '',
                 'path': '/property/workConditionMeaning', 'equal': False}]
    expected_meaning = {'conditionDefinitionBinding': condition_binding,
        'workSpecificationBinding': work_specification_binding, 'procedureBinding': procedure_binding,
        **{key: condition[key] for key in ('activityRow', 'stage', 'conditionId', 'predicateKind')}}
    checks = [{'code': code, 'actual': meaning, 'expected': condition,
        'sourcePointer': '/workConditionMeaning', 'sourcePresent': True,
        'destinationKind': 'condition', 'destinationPointer': '',
        'path': '/property/workConditionMeaning', 'equal': same(meaning, expected_meaning),
        'usesSelectedBindings': True}]
    checks.append({'code': 'WORK_CONDITION_PROPERTY_CONDITION_BINDING_MISMATCH',
        'actual': meaning['conditionDefinitionBinding'], 'expected': condition_binding,
        'sourcePointer': '/workConditionMeaning/conditionDefinitionBinding', 'sourcePresent': True,
        'destinationKind': 'conditionSelection', 'destinationPointer': '',
        'path': '/property/workConditionMeaning/conditionDefinitionBinding',
        'equal': same(meaning['conditionDefinitionBinding'], condition_binding)})
    for key in ('activityRow', 'stage', 'conditionId', 'predicateKind'):
        if key in meaning:
            checks.append({'code': 'WORK_CONDITION_PROPERTY_' + key.upper() + '_MISMATCH',
                'actual': meaning[key], 'expected': condition[key], 'sourcePresent': True,
                'sourcePointer': '/workConditionMeaning/' + key, 'destinationKind': 'condition',
                'destinationPointer': '/' + key, 'path': '/property/workConditionMeaning/' + key,
                'equal': same(meaning[key], condition[key])})
    for key, path in (('workSpecificationBinding', 'binding'), ('procedureBinding', 'procedure')):
        if key in meaning:
            expected = work_atom['body']['workSpecification'][path]
            checks.append({'code': 'WORK_CONDITION_PROPERTY_' + key.upper() + '_MISMATCH',
                'actual': meaning[key], 'expected': expected, 'sourcePresent': True,
                'sourcePointer': '/workConditionMeaning/' + key, 'destinationKind': 'claim',
                'destinationPointer': '/body/workSpecification/' + path,
                'path': '/property/workConditionMeaning/' + key, 'equal': same(meaning[key], expected)})
    return checks


def condition_scope_checks(condition, work_atom, method, measurement):
    """Retain ordered target, extent and clock checks over original fields.

    Record kinds name the four caller-owned originals. Operand pointers may
    name absent leaves; consumers must retain absence and the real ancestor.
    Parsed timestamps are predicate inputs, never original-field observations.
    """
    from time_validation import foreign_instant, foreign_seconds
    from runtime_support import instant
    checks = []

    def operand(kind, path):
        return {'recordKind': kind, 'pointer': path}

    def compare(code, actual, expected, path, source, destination=None,
                *, equal=None, legacy_origins=True):
        checks.append({'kind': 'COMPARE', 'code': code, 'path': path,
            'actual': actual, 'expected': expected,
            'equal': same(actual, expected) if equal is None else equal,
            'source': source, 'destination': destination,
            'legacyOrigins': legacy_origins,
            'operands': [source, *([destination] if destination is not None else [])]})

    def error(code, path, operands):
        checks.append({'kind': 'ERROR', 'code': code, 'path': path, 'operands': operands})

    def compare_time(actual, expected, path, source, destination):
        if actual is None and expected is None:
            return
        operands = [source, destination]
        try:
            parsed = foreign_instant(actual)
            if parsed['unknownLocalOffset']:
                checks.append({'kind': 'MISSING',
                    'role': 'WORK_CONDITION_KNOWN_PHENOMENON_INSTANT_INTERPRETATION',
                    'path': path, 'operands': operands})
                return
            equal = parsed['seconds'] == foreign_seconds(expected)
        except (ValueError, TypeError):
            error('WORK_CONDITION_TIME_UNAVAILABLE', path, operands)
            return
        compare('WORK_CONDITION_PHENOMENON_TIME_MISMATCH', actual, expected,
                path, source, destination, equal=equal)

    target = work_atom['body']['target']
    subject = method['scope']['subject']
    compare('WORK_CONDITION_TARGET_KIND_MISMATCH', subject['subjectType'], target['kind'],
        '/condition/scope/subjectType', operand('method', '/scope/subject/subjectType'),
        operand('claim', '/body/target/kind'))
    projected_binding = {'ref': subject['subjectRef'],
                         **{key: subject[key] for key in ('digest', 'revisionRef') if key in subject}}
    compare('WORK_CONDITION_TARGET_BINDING_MISMATCH', subject, target['binding'],
        '/condition/scope/subject', operand('method', '/scope/subject'),
        operand('claim', '/body/target/binding'), equal=same(projected_binding, target['binding']))
    for key, source_key in (('ref', 'subjectRef'), ('revisionRef', 'revisionRef'), ('digest', 'digest')):
        if source_key in subject and key in target['binding']:
            compare('WORK_CONDITION_TARGET_' + key.upper() + '_MISMATCH', subject[source_key],
                target['binding'][key], '/condition/scope/subject/' + source_key,
                operand('method', '/scope/subject/' + source_key),
                operand('claim', '/body/target/binding/' + key))
    compare('WORK_CONDITION_EXTENT_MISMATCH', method['scope']['extent'], work_atom['body']['extent'],
        '/condition/scope/extent', operand('method', '/scope/extent'), operand('claim', '/body/extent'))
    condition_time = method['scope']['subjectTime']
    work_time = work_atom['scope']['subjectTime']
    phenomenon = measurement['phenomenonTime']
    if 'at' in condition_time:
        if phenomenon['timeType'] not in ('INSTANT', 'AS_OF'):
            error('WORK_CONDITION_PHENOMENON_TIME_FORM_MISMATCH', '/measurement/phenomenonTime',
                [operand('measurement', '/phenomenonTime/timeType'),
                 operand('method', '/scope/subjectTime')])
        compare_time(phenomenon.get('instant'), condition_time['at'],
            '/measurement/phenomenonTime/instant', operand('measurement', '/phenomenonTime/instant'),
            operand('method', '/scope/subjectTime/at'))
    else:
        expected_type = 'INTERVAL' if 'end' in condition_time else 'OPEN_INTERVAL'
        compare('WORK_CONDITION_PHENOMENON_TIME_FORM_MISMATCH', phenomenon['timeType'], expected_type,
            '/measurement/phenomenonTime/timeType', operand('measurement', '/phenomenonTime/timeType'),
            legacy_origins=False)
        checks[-1]['operands'].append(operand('method', '/scope/subjectTime'))
        for source_key, selected in (('intervalStart', 'start'), ('intervalEnd', 'end')):
            compare_time(phenomenon.get(source_key), condition_time.get(selected),
                '/measurement/phenomenonTime/' + source_key,
                operand('measurement', '/phenomenonTime/' + source_key),
                operand('method', '/scope/subjectTime/' + selected))
    time_operands = [operand('method', '/scope/subjectTime'), operand('claim', '/scope/subjectTime'),
                     operand('condition', '/temporalRole'), operand('condition', '/stage')]
    try:
        a = instant(condition_time.get('at', condition_time.get('start')))
        z = instant(condition_time['end']) if 'end' in condition_time else a if 'at' in condition_time else None
        start = instant(work_time.get('at', work_time.get('start')))
        end = instant(work_time['end']) if 'end' in work_time else start if 'at' in work_time else None
        role, stage = condition['temporalRole'], condition['stage']
        compare('WORK_CONDITION_STAGE_TIME_ROLE_MISMATCH', role,
            {'START': 'AT_WORK_START', 'IN_PROGRESS': 'DURING_WORK', 'FINISH': 'AT_WORK_FINISH'}[stage],
            '/condition/temporalRole', operand('condition', '/temporalRole'), legacy_origins=False)
        checks[-1]['operands'].append(operand('condition', '/stage'))
        compare('WORK_CONDITION_OUTSIDE_CLAIMED_TIME', condition_time, work_time,
            '/condition/scope/subjectTime', operand('method', '/scope/subjectTime'),
            operand('claim', '/scope/subjectTime'),
            equal=not (a < start or end is not None and (z is None or z > end)))
        if role == 'AT_WORK_START' and a != start or role == 'AT_WORK_FINISH' and (end is None or z != end):
            error('WORK_CONDITION_BOUNDARY_TIME_MISMATCH', '/condition/scope/subjectTime', time_operands)
    except (ValueError, KeyError, TypeError):
        error('WORK_CONDITION_TIME_UNAVAILABLE', '/condition/scope/subjectTime', time_operands)
    return checks


def condition_operand_source_request(method, measurement):
    """Select the existing operand read; null selectors establish no read."""
    kind = measurement['result']['resultKind']
    if kind in ('NUMERIC', 'CENSORED_NUMERIC') and method['scalarSource'] is not None:
        return {'parentKind': 'method', 'pointer': '/scalarSource/binding',
                'binding': method['scalarSource']['binding'],
                'schemaId': 'https://ofarm.dev/schema/executionrecordpayload/v0.1',
                'role': 'WORK_CONDITION_ORIGINAL_SCALAR', 'resultKind': kind}
    if kind in ('CODED', 'QUALITATIVE') and method['mappingBinding'] is not None:
        return {'parentKind': 'method', 'pointer': '/mappingBinding',
                'binding': method['mappingBinding'], 'schemaId': SCHEMAS['mapping']['$id'],
                'role': 'WORK_CONDITION_RESULT_MAPPING', 'resultKind': kind}
    return None


def evaluate(condition,work_atom,sources,schemas,*,condition_binding,condition_binding_origin,work_specification_binding,procedure_binding):
    return _evaluate_condition(condition,work_atom,sources,schemas,
        condition_binding=condition_binding,condition_binding_origin=condition_binding_origin,
        work_specification_binding=work_specification_binding,procedure_binding=procedure_binding)


def evaluate_preoperand(condition,work_atom,sources,schemas,*,condition_binding,condition_binding_origin,work_specification_binding,procedure_binding):
    """Run the actual generic reader prefix, without constructing an operand.

    This derived report is not source admission or condition satisfaction.
    Consumers must independently verify the selected originals and ordered
    required references. Missing roles alone do not close the error gate.
    """
    reader = condition_reader_kind(condition)
    if reader != 'CRITERION_MEASUREMENT':
        return {'scope': 'WORK_CONDITION_PRE_OPERAND_PREFIX', 'readerKind': reader,
                'reachedOperandBoundary': False, 'resolvedInputIds': None, 'report': None}
    return _evaluate_condition(condition,work_atom,sources,schemas,
        condition_binding=condition_binding,condition_binding_origin=condition_binding_origin,
        work_specification_binding=work_specification_binding,procedure_binding=procedure_binding,
        stop_before_operand=True)


def evaluate_precriterion(condition,work_atom,sources,schemas,*,condition_binding,condition_binding_origin,work_specification_binding,procedure_binding):
    """Stop after validating the derived C04, before its criterion reader.

    The returned atom is constructed data, not an original observation.
    Reaching criterion entry is independent of accumulated interval errors.
    """
    reader = condition_reader_kind(condition)
    if reader != 'CRITERION_MEASUREMENT':
        return {'scope': 'WORK_CONDITION_PRE_CRITERION_PREFIX', 'readerKind': reader,
                'reachedOperandBoundary': False, 'reachedCriterionEntry': False,
                'resolvedInputIds': None, 'derivedCriterion': None,
                'criterionSchemaErrors': None, 'report': None}
    return _evaluate_condition(condition,work_atom,sources,schemas,
        condition_binding=condition_binding,condition_binding_origin=condition_binding_origin,
        work_specification_binding=work_specification_binding,procedure_binding=procedure_binding,
        stop_before_criterion=True)


def _evaluate_condition(condition,work_atom,sources,schemas,*,condition_binding,condition_binding_origin,work_specification_binding,procedure_binding,stop_before_operand=False,stop_before_criterion=False):
    reader=condition_reader_kind(condition)
    if reader=='ANALYSIS_OUTPUT':
        from analysis_output_sources import evaluate as analysis_output
        return analysis_output(condition,work_atom,sources,schemas,
            work_specification_binding=work_specification_binding,procedure_binding=procedure_binding)
    if reader=='OBSERVATION_ACQUISITION':
        from observation_acquisition_sources import evaluate as acquisition
        return acquisition(condition,work_atom,sources,schemas,condition_binding=condition_binding)
    from runtime_support import pointer
    from criterion_sources import evaluate as criterion
    register(schemas)
    errors,missing,refs,ids,comparisons=[],[],[],[],[]
    origins={}
    retained=None
    drying_ratio=None
    irrigation_interval=None
    sanitation_interval=None
    domain_interpretation=None
    resolved=None
    reached_operand_boundary=False
    reached_criterion_entry=False
    internal=None
    criterion_schema_errors=None
    completion_count = COMPLETION_COUNTS.get(condition['activityRow']) if condition['stage'] == 'FINISH' else None
    linked_reader = condition_linked_reader(condition)
    selected_conditions=[v for v in sources if same(v['binding'],condition_binding)]
    if len(selected_conditions)==1:origins[id(condition)]=selected_conditions[0]['id']
    def original(record,path):
        return {'inputRole':origins[id(record)],'pointer':path} if id(record) in origins else None
    def claimed(path):
        return {'inputRole':'ATOM:'+work_atom['atomId'],'pointer':path}
    def report():
        return {'disposition':'FAIL' if errors else 'NOT_EVALUATED' if missing else 'PASS',
                'errors':errors,'remainingRoles':missing,'requiredReferences':refs,
                'sourceInputIds':sorted(set(ids)),'comparisons':comparisons,
                'retainedSourceQualifications':retained,
                **({'admissibleDomainInterpretation':domain_interpretation} if domain_interpretation is not None else {})}
    def resolved_ids():
        return ({name: origins[id(record)] for name, record in
                 zip(('criterion', 'method', 'measurement', 'property'), resolved)}
                if resolved is not None else None)
    def result():
        if not stop_before_criterion:return report()
        return {'scope': 'WORK_CONDITION_PRE_CRITERION_PREFIX', 'readerKind': reader,
                'reachedOperandBoundary': reached_operand_boundary,
                'reachedCriterionEntry': reached_criterion_entry,
                'resolvedInputIds': resolved_ids(), 'derivedCriterion': internal,
                'criterionSchemaErrors': criterion_schema_errors, 'report': report()}
    def preoperand_result(resolved):
        return {'scope': 'WORK_CONDITION_PRE_OPERAND_PREFIX', 'readerKind': reader,
                'reachedOperandBoundary': resolved is not None,
                'resolvedInputIds': resolved_ids(), 'report': report()}
    def get(binding,schema_id,role,parent=None,field=None):
        refs.append({'binding':binding,'role':role,'pointer':'/condition/'+role})
        found=[v for v in sources if same(v['binding'],binding)]
        if role=='WORK_CONDITION_PROPERTY_DEFINITION' and field=='propertyBinding' and 'revisionRef' in binding:
            from condition_property_resolution import ConditionSources
            if isinstance(sources,ConditionSources):
                found=sources.property_for(parent)
        if len(found)!=1:
            missing.append({'role':role,'pointer':'/condition/'+role});return None
        item=found[0];ids.append(item['id']);shape=schemas.errors(schema_id,item['record']);errors.extend(shape)
        if shape:return None
        origins[id(item['record'])]=item['id']
        return item['record']
    def compare(code,actual,expected,path,source=None,destination=None,equal=None):
        if equal is None:equal=same(actual,expected)
        fact={'predicateId':code,'pointer':path,'equal':equal,
            'actualValueDigest':digest(actual),'expectedValueDigest':digest(expected)}
        if source is not None and destination is not None:
            fact.update(source={**source,'valueDigest':digest(actual)},destination={**destination,'valueDigest':digest(expected)},
                        disposition='PASS' if equal else 'FAIL')
        comparisons.append(fact)
        if not equal:errors.append({'code':code,'pointer':path})
    resolved=resolve_condition_inputs(condition,lambda parent,field,schema_id,role,prerequisites:get(parent[field],schema_id,role,parent,field))
    if resolved is None:return preoperand_result(None) if stop_before_operand else result()
    criterion_def,method,measurement,property_definition=resolved
    for check in condition_property_comparisons(condition,property_definition,work_atom,
            condition_binding=condition_binding,work_specification_binding=work_specification_binding,procedure_binding=procedure_binding):
        if not check['sourcePresent']:
            from original_operand import select_operand
            errors.append({'code':check['code'],'pointer':check['path']})
            comparisons.append({'predicateId':check['code'],'equal':False,'pointer':check['path'],'operandAvailability':{
                'source':select_operand(property_definition,check['sourcePointer'],origins[id(property_definition)]),
                'destination':select_operand(condition,'',origins[id(condition)])}})
            continue
        destination=(condition_binding_origin if check['destinationKind']=='conditionSelection' else
                     claimed(check['destinationPointer']) if check['destinationKind']=='claim' else
                     original(condition,check['destinationPointer']))
        compare(check['code'],check['actual'],check['expected'],check['path'],
            original(property_definition,check['sourcePointer']),destination,equal=check['equal'])
    activity_stage=condition['stage'] in ['START','IN_PROGRESS']
    if activity_stage or condition['activityRow']=='O08':
        finish=condition['stage']=='FINISH'
        compare('WORK_CONDITION_PREDICATE_KIND_MISMATCH',condition['predicateKind'],
                condition_activity_predicate_kind(condition),'/condition/predicateKind')
        compare('WORK_CONDITION_REQUIRED_QUANTITY_KIND_MISMATCH',method['quantityContext']['quantityKind'],
                condition_activity_quantity_kind(condition),'/method/quantityContext/quantityKind')
        compare('WORK_CONDITION_REQUIRED_UNIT_MISMATCH',method['quantityContext']['unit'],
                condition_required_unit(condition),'/method/quantityContext/unit')
        compare('WORK_CONDITION_REQUIRED_OPERATOR_MISMATCH',criterion_def['operator'],condition_activity_operator(condition),'/criterion/operator')
        compare('WORK_CONDITION_REQUIRED_THRESHOLD_MISMATCH',criterion_def['threshold'].get('decimal'),condition_activity_threshold_decimal(condition),'/criterion/threshold/decimal')
        compare('WORK_CONDITION_REQUIRED_THRESHOLD_QUALIFIER_MISMATCH',criterion_def['threshold'].get('qualifier'),condition_activity_threshold_qualifier(condition),'/criterion/threshold/qualifier')
    elif completion_count is not None:
        retained={'measurementBinding':condition['measurementBinding'],'originalMeasurement':copy.deepcopy(measurement),
                  'propertyDefinitionBinding':method['propertyBinding']}
        if condition['activityRow']=='O11':
            population=property_definition.get('splitCountPopulation')
            if population is None:
                missing.append({'role':'EXACT_SPLIT_COUNT_POPULATION_MEANING','pointer':'/property/splitCountPopulation'})
            else:
                parameters=work_atom['body']['parameters'];target=work_atom['body']['target']
                source_lot=population['sourceLotBinding'];outputs=population['successorLotBindings']
                prefix='/splitCountPopulation/'
                # This selected meaning supports the direct source-lot target only.
                # Another target needs an independently established relation, never
                # an inference from a matching label or from the count itself.
                compare('SPLIT_COUNT_SOURCE_TARGET_MISMATCH',source_lot,target,
                        '/property'+prefix+'sourceLotBinding',original(property_definition,prefix+'sourceLotBinding'),
                        claimed('/body/target'),equal=target['kind']=='LOT' and same(source_lot,target['binding']))
                compare('SPLIT_COUNT_PREDECESSOR_MISMATCH',source_lot,parameters['predecessors'],
                        '/property'+prefix+'sourceLotBinding',original(property_definition,prefix+'sourceLotBinding'),
                        claimed('/body/parameters/predecessors'),
                        equal=len(parameters['predecessors'])==1 and same(source_lot,parameters['predecessors'][0]))
                compare('SPLIT_COUNT_SOURCE_EXTENT_MISMATCH',population['sourceExtent'],work_atom['body']['extent'],
                        '/property'+prefix+'sourceExtent',original(property_definition,prefix+'sourceExtent'),claimed('/body/extent'))
                selected_outputs=parameters['successors']
                compare('SPLIT_COUNT_SUCCESSORS_MISMATCH',outputs,selected_outputs,
                        '/property'+prefix+'successorLotBindings',original(property_definition,prefix+'successorLotBindings'),
                        claimed('/body/parameters/successors'),
                        equal=len(outputs)==len(selected_outputs) and {digest(v) for v in outputs}=={digest(v) for v in selected_outputs})
                # Distinct revisions of one logical lot are not distinct cohorts.
                # The original arrays stay intact in these predicate operands.
                compare('SPLIT_COUNT_DISTINCT_SUCCESSORS_REQUIRED',outputs,selected_outputs,
                        '/property'+prefix+'successorLotBindings',original(property_definition,prefix+'successorLotBindings'),
                        claimed('/body/parameters/successors'),
                        equal=all(len(values)>=2 and len({v['ref'] for v in values})==len(values) for values in [outputs,selected_outputs]))
                compare('SPLIT_COUNT_SOURCE_REUSED_AS_SUCCESSOR',outputs,source_lot,
                        '/property'+prefix+'successorLotBindings',original(property_definition,prefix+'successorLotBindings'),
                        original(property_definition,prefix+'sourceLotBinding'),
                        equal=all(v['ref']!=source_lot['ref'] for v in outputs))
                compare('SPLIT_COUNT_LINEAGE_RELATION_MISMATCH',population['lineageRelation'],parameters['lineageRelation'],
                        '/property'+prefix+'lineageRelation',original(property_definition,prefix+'lineageRelation'),
                        claimed('/body/parameters/lineageRelation'))
        if condition['activityRow']=='O06':
            population=property_definition.get('harvestCountPopulation')
            if population is None:
                missing.append({'role':'EXACT_HARVEST_COUNT_POPULATION_MEANING','pointer':'/property/harvestCountPopulation'})
            else:
                parameters=work_atom['body']['parameters']
                for field,key in [('cropCycleBinding','cropCycle'),('outputLotBindings','outputLots')]:
                    compare('HARVEST_COUNT_'+key.upper()+'_MISMATCH',population[field],parameters[key],'/property/harvestCountPopulation/'+field,
                        original(property_definition,'/harvestCountPopulation/'+field),claimed('/body/parameters/'+key))
                selected=[(i,q) for i,q in enumerate(work_atom['body']['quantityParameters']) if q['parameterId']==parameters['harvestedMass']['quantityParameterId']]
                if len(selected)!=1 or selected[0][1]['material']['presence']!='PRESENT':
                    missing.append({'role':'EXACT_HARVEST_COUNT_MATERIAL_SELECTION','pointer':'/body/parameters/harvestedMass'})
                else:
                    index,quantity=selected[0]
                    compare('HARVEST_COUNT_MATERIAL_MISMATCH',population['harvestedMaterialBinding'],quantity['material']['binding'],
                        '/property/harvestCountPopulation/harvestedMaterialBinding',original(property_definition,'/harvestCountPopulation/harvestedMaterialBinding'),
                        claimed('/body/quantityParameters/'+str(index)+'/material/binding'))
        if condition['activityRow']=='O13':
            population=property_definition.get('mixingCountPopulation')
            if population is None:
                missing.append({'role':'EXACT_MIXING_COUNT_POPULATION_MEANING','pointer':'/property/mixingCountPopulation'})
            else:
                parameters=work_atom['body']['parameters']
                for field,key in [('predecessorLotBindings','predecessors'),('successorLotBindings','successors'),
                                  ('claimBasisAfterBinding','claimBasisAfter'),('mixingPosture','mixingPosture')]:
                    compare('MIXING_COUNT_'+key.upper()+'_MISMATCH',population[field],parameters[key],'/property/mixingCountPopulation/'+field,
                        original(property_definition,'/mixingCountPopulation/'+field),claimed('/body/parameters/'+key))
        if 'completionCountMeaning' not in property_definition:
            missing.append({'role':'EXACT_UNFINISHED_WORK_COUNT_PROPERTY_MEANING','pointer':'/property/completionCountMeaning'})
        else:
            compare('UNFINISHED_WORK_COUNT_PROPERTY_MEANING_MISMATCH',property_definition['completionCountMeaning'],completion_count,
                    '/property/completionCountMeaning',original(property_definition,'/completionCountMeaning'),
                    {'inputRole':'COMPLETION_COUNT_MEANINGS','pointer':'/definitions/'+condition['activityRow']})
        for actual,field,path,origin in [
            (condition['predicateKind'],'predicateKind','/condition/predicateKind',original(condition,'/predicateKind')),
            (method['quantityContext']['quantityKind'],'quantityKind','/method/quantityContext/quantityKind',original(method,'/quantityContext/quantityKind')),
            (method['quantityContext']['unit'],'unit','/method/quantityContext/unit',original(method,'/quantityContext/unit')),
            (criterion_def['operator'],'operator','/criterion/operator',original(criterion_def,'/operator')),
            (criterion_def['threshold'].get('decimal'),'threshold','/criterion/threshold/decimal',original(criterion_def,'/threshold/decimal') if 'decimal' in criterion_def['threshold'] else None),
            (criterion_def['threshold'].get('qualifier'),'thresholdQualifier','/criterion/threshold/qualifier',original(criterion_def,'/threshold/qualifier') if 'qualifier' in criterion_def['threshold'] else None),
        ]:
            compare('UNFINISHED_WORK_COUNT_'+field.upper()+'_MISMATCH',actual,completion_count[field],path,origin,
                    {'inputRole':'COMPLETION_COUNT_MEANINGS','pointer':'/definitions/'+condition['activityRow']+'/'+field})
    elif linked_reader=='IRRIGATION':
        from irrigation_sources import evaluate as irrigation
        linked=irrigation(condition,work_atom,method,criterion_def,measurement,property_definition,sources,schemas,condition_binding)
        errors.extend(linked['errors']);missing.extend(linked['remainingRoles']);refs.extend(linked['requiredReferences'])
        ids.extend(linked['sourceInputIds']);comparisons.extend(linked['comparisons']);retained=linked['retainedSourceQualifications']
        irrigation_interval=linked['intervalContext']
    elif linked_reader=='SANITATION':
        from sanitation_sources import evaluate as sanitation
        linked=sanitation(condition,work_atom,method,criterion_def,measurement,property_definition,sources,schemas,condition_binding)
        errors.extend(linked['errors']);missing.extend(linked['remainingRoles']);refs.extend(linked['requiredReferences'])
        ids.extend(linked['sourceInputIds']);comparisons.extend(linked['comparisons']);retained=linked['retainedSourceQualifications']
        sanitation_interval=linked['intervalContext']
    elif linked_reader=='DRYING':
        from drying_sources import evaluate as drying
        linked=drying(condition,work_atom,method,criterion_def,measurement,sources,schemas)
        errors.extend(linked['errors']);missing.extend(linked['remainingRoles']);refs.extend(linked['requiredReferences'])
        ids.extend(linked['sourceInputIds']);comparisons.extend(linked['comparisons']);retained=linked['retainedSourceQualifications']
        drying_ratio=linked['ratioMeaning']
    elif linked_reader=='SAMPLE_COLLECTION':
        compare('WORK_CONDITION_PREDICATE_KIND_MISMATCH',condition['predicateKind'],
                'PROTOCOL_SAMPLE_AND_SUPPORT_COLLECTION_RECORDED','/condition/predicateKind')
        compare('WORK_CONDITION_REQUIRED_QUANTITY_KIND_MISMATCH',method['quantityContext']['quantityKind'],
                'candidate:quantitykind:protocol-sample-support-completion','/method/quantityContext/quantityKind')
        compare('WORK_CONDITION_REQUIRED_UNIT_MISMATCH',method['quantityContext']['unit'],condition_required_unit(condition),'/method/quantityContext/unit')
        compare('WORK_CONDITION_REQUIRED_OPERATOR_MISMATCH',criterion_def['operator'],'GE','/criterion/operator')
        compare('WORK_CONDITION_REQUIRED_THRESHOLD_MISMATCH',criterion_def['threshold'].get('decimal'),'1','/criterion/threshold/decimal')
        compare('WORK_CONDITION_REQUIRED_THRESHOLD_QUALIFIER_MISMATCH',criterion_def['threshold'].get('qualifier'),'EXACT','/criterion/threshold/qualifier')
        from sample_collection_sources import evaluate as sample_collection
        linked=sample_collection(work_atom,condition,measurement,sources,schemas)
        errors.extend(linked['errors']);missing.extend(linked['remainingRoles']);refs.extend(linked['requiredReferences'])
        ids.extend(linked['sourceInputIds']);comparisons.extend(linked['comparisons']);retained=linked['retainedSourceQualifications']
    else:
        missing.append({'role':'ROW_CONDITION_SEMANTICS:'+condition['activityRow']+':'+condition['stage'],'pointer':'/condition/predicateKind'})
    scope_records = {'condition': condition, 'claim': work_atom,
                     'method': method, 'measurement': measurement}
    def scope_origin(operand):
        if operand['recordKind'] == 'claim':
            return claimed(operand['pointer'])
        return original(scope_records[operand['recordKind']], operand['pointer'])
    for check in condition_scope_checks(condition, work_atom, method, measurement):
        if check['kind'] == 'ERROR':
            errors.append({'code': check['code'], 'pointer': check['path']})
        elif check['kind'] == 'MISSING':
            missing.append({'role': check['role'], 'pointer': check['path']})
        else:
            source = scope_origin(check['source']) if check['legacyOrigins'] else None
            destination = scope_origin(check['destination']) if check['legacyOrigins'] else None
            compare(check['code'], check['actual'], check['expected'], check['path'],
                    source, destination, equal=check['equal'])
    reached_operand_boundary=True
    if stop_before_operand:return preoperand_result(resolved)
    if errors:return result()
    source={'role':'MEASURED_COMPLIANCE_OPERAND','measurementBinding':condition['measurementBinding'],
            'resultPointer':'/result','contextBinding':method['contextBinding'],'subjectRelationBinding':method['subjectRelationBinding'],
            'methodUseBinding':criterion_def['methodUseBinding'],'qualificationPointers':method['qualificationPointers']}
    measured=measurement['result'];kind=measured['resultKind'];operand={'resultKind':kind,'source':source}
    def decimal(value):
        if type(value) not in [int,float]:raise ValueError('Expected an actual numeric source field.')
        return format(Decimal(str(value)),'f')
    try:
        if kind in ['NUMERIC','CENSORED_NUMERIC']:
            selected=method['scalarSource']
            if selected is None:
                errors.append({'code':'WORK_CONDITION_SCALAR_SOURCE_REQUIRED','pointer':'/method/scalarSource'});return result()
            request=condition_operand_source_request(method,measurement)
            record=get(request['binding'],request['schemaId'],request['role'])
            if record is None:return result()
            path='/actualQuantityParameters/'+str(selected['parameterIndex']);scalar=pointer(record,path)
            if type(scalar.get('reportedValue')) not in [str,int,float] or 'qualifier' not in scalar:
                errors.append({'code':'WORK_CONDITION_ORIGINAL_SCALAR_QUALIFICATION_REQUIRED','pointer':path});return result()
            quantity={'quantityKind':scalar['quantityKindRef'],'unit':scalar['unitRef'],'decimal':decimal(scalar['value']),
                      'qualifier':scalar['qualifier'],'originalLexicalValue':scalar['reportedValue'],
                      'unitProfile':method['quantityContext']['unitProfile'],
                      'provenance':{'sourceBinding':selected['binding'],'valuePointer':path+'/value','lexicalPointer':path+'/reportedValue','qualifierPointer':path+'/qualifier'}}
            if 'reportedUnitLabel' in scalar:quantity['originalUnitText']=scalar['reportedUnitLabel']
            operand['quantity' if kind=='NUMERIC' else 'limit']=quantity
            if kind=='NUMERIC':
                rule=method['numericSet']
                if rule['kind']=='EXACT_POINT':
                    amount=decimal(measured['numericValue']);lower={'decimal':amount,'inclusive':True};upper=copy.deepcopy(lower);basis='EXACT_NUMERIC_POINT'
                else:
                    lower={'decimal':decimal(pointer(measurement,rule['lowerPointer'])),'inclusive':rule['lowerInclusive']}
                    upper={'decimal':decimal(pointer(measurement,rule['upperPointer'])),'inclusive':rule['upperInclusive']};basis='METHOD_DEFINED_HARD_BOUND'
            else:
                rules=[v for v in method['censoringRules'] if v['qualifier']==measured['censoringQualifier'] and v['limitType']==measured['detectionLimit']['limitType']]
                if len(rules)!=1:raise ValueError('Exact censoring rule unavailable.')
                rule=rules[0]
                def endpoint(value):
                    return {'kind':'UNBOUNDED'} if value['origin']=='UNBOUNDED' else {'decimal':'0' if value['origin']=='ZERO' else decimal(measured['detectionLimit']['value']),'inclusive':value['inclusive']}
                lower,upper=endpoint(rule['lower']),endpoint(rule['upper']);basis=rule['basis']
                operand.update(qualifier=measured['censoringQualifier'],nonnegative=rule['nonnegative'])
            operand['admissibleValues']={'kind':'INTERVAL','lower':lower,'upper':upper,'basis':basis}
        elif kind in ['CODED','QUALITATIVE']:
            if method['mappingBinding'] is None:raise ValueError('Exact selected result mapping unavailable.')
            request=condition_operand_source_request(method,measurement)
            mapping=get(request['binding'],request['schemaId'],request['role'])
            if mapping is None:return result()
            value=measured['codedValueRef' if kind=='CODED' else 'qualitativeValue']
            rows=[v for v in mapping['entries'] if v['resultKind']==kind and v['sourceValue']==value]
            if len(rows)!=1:raise ValueError('Unique original result mapping unavailable.')
            operand.update(mappingBinding=method['mappingBinding'],admissibleValues={'kind':'INTERVAL',**rows[0]['admissibleValues'],'basis':rows[0]['basis']})
            if kind=='CODED':
                index=_condition_coded_value_index(condition,value)
                operand['codedValue']=condition['resultTerms']['codedValues'][index]
            else:
                if condition['resultTerms']['qualitativeScale'] is None:raise ValueError('Exact qualitative scale unavailable.')
                operand.update(originalText=value,scaleBinding=condition['resultTerms']['qualitativeScale'])
        else:
            errors.append({'code':'PENDING_RESULT_CANNOT_ESTABLISH_REQUIRED_WORK_CONDITION','pointer':'/measurement/result'});return result()
    except (ValueError,KeyError,TypeError) as exc:
        errors.append({'code':'WORK_CONDITION_ORIGINAL_OPERAND_UNAVAILABLE','pointer':'/measurement/result','detail':str(exc)});return result()
    interval=operand['admissibleValues']
    if irrigation_interval is not None:
        from irrigation_sources import check_interval
        linked=check_interval(interval,irrigation_interval)
        errors.extend(linked['errors']);missing.extend(linked['remainingRoles']);comparisons.extend(linked['comparisons'])
    if sanitation_interval is not None:
        from sanitation_sources import check_interval
        linked=check_interval(interval,sanitation_interval)
        errors.extend(linked['errors']);missing.extend(linked['remainingRoles']);comparisons.extend(linked['comparisons'])
    if completion_count is not None:
        from completion_count_meanings import interval_errors as count_interval_errors
        errors.extend(count_interval_errors(interval))
    if drying_ratio is not None:
        from drying_sources import interval_errors
        errors.extend(interval_errors(interval,drying_ratio))
    if activity_stage or condition['activityRow']=='O08':
        lower,upper=interval['lower'],interval['upper']
        if 'decimal' not in lower or Decimal(lower['decimal'])<0:
            errors.append({'code':'WORK_CONDITION_NEGATIVE_OR_UNBOUNDED_COUNT','pointer':'/measurement/result'})
        if condition['stage']!='FINISH' and ('decimal' not in upper or Decimal(upper['decimal'])>1):
            errors.append({'code':'WORK_ACTIVITY_PRESENCE_OUTSIDE_BOOLEAN_DOMAIN','pointer':'/measurement/result'})
    if condition['activityRow']=='O10' and condition['stage']=='FINISH':
        lower,upper=interval['lower'],interval['upper']
        if ('decimal' not in lower or 'decimal' not in upper or
                Decimal(lower['decimal']) not in [0,1] or Decimal(upper['decimal']) not in [0,1] or
                Decimal(lower['decimal'])!=Decimal(upper['decimal']) or not lower['inclusive'] or not upper['inclusive']):
            errors.append({'code':'SAMPLE_COLLECTION_FINISH_OUTSIDE_DISCRETE_COMPLETION_DOMAIN','pointer':'/measurement/result'})
    threshold=copy.deepcopy(criterion_def['threshold'])
    for suffix,quantity in ([('/lower',threshold['lower']),('/upper',threshold['upper'])] if criterion_def['operator']=='BETWEEN' else [('',threshold)]):
        path='/threshold'+suffix
        quantity['provenance']={'sourceBinding':condition['criterionBinding'],'valuePointer':path+'/decimal','lexicalPointer':path+'/originalLexicalValue','qualifierPointer':path+'/qualifier'}
    internal={'form':'ATOM','atomId':'work-condition:'+condition['conditionId'],
              'definition':'candidate:assertion-domain-construction:2026-10-21:r2:C04','scope':copy.deepcopy(method['scope']),
              'body':{'form':'CRITERION_OUTCOME','criterion':condition['criterionBinding'],'operand':operand,'operator':criterion_def['operator'],
                      'threshold':threshold,'allegedOutcome':'SATISFIED',
                      'measuredQualification':{'sourceBinding':condition['measurementBinding'],'sourcePointer':method['qualificationPointers'][0],
                         'methodUseBinding':criterion_def['methodUseBinding'],'interpretation':method['qualificationInterpretation']}}}
    shape=schemas.errors('https://ofarm.dev/schema/drafts/non-default/assertion-domain/proposition/v0.1',internal,'C04')
    criterion_schema_errors=shape
    if shape:
        errors.extend(shape);return result()
    reached_criterion_entry=True
    if stop_before_criterion:return result()
    from condition_property_resolution import ConditionSources
    criterion_sources=sources.for_method(method) if isinstance(sources,ConditionSources) else sources
    checked=criterion(internal,criterion_sources,schemas,claim_origin=None)
    domain_interpretation=checked.get('admissibleDomainInterpretation')
    errors.extend(checked['errors']);missing.extend(checked['remainingRoles']);refs.extend(checked['requiredReferences']);ids.extend(checked['sourceInputIds']);comparisons.extend(checked['comparisons'])
    if checked.get('conditionalMathematicalOutcome') not in [None,'SATISFIED']:
        errors.append({'code':'REQUIRED_WORK_CONDITION_NOT_SATISFIED','pointer':'/condition','outcome':checked['conditionalMathematicalOutcome']})
    return result()
