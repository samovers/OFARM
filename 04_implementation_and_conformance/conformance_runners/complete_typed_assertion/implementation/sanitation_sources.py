"""Selected sanitation contact and procedure termination from original observations.

Contact means the minimum continuous contact duration of the selected material
at every selected surface. It is not elapsed work time or a hygiene outcome.
An independent duration-unit meaning checks the bounded work interval.
"""
from decimal import Decimal
from definition_inputs import SCHEMAS as TERM_SCHEMAS
from strict_inputs import same, digest, pointer
from sanitation_definitions import SCHEMAS, register, CONTACT, TERMINATION


def sanitation_initial_inputs(condition, atom, read):
    """Yield specification then work, preserving the comparison between reads."""
    from work_definition_inputs import SCHEMAS as WORK
    spec = read(condition, '/sanitationSpecificationBinding',
        SCHEMAS['sanitation']['$id'], 'SELECTED_SANITATION_FINISH_SPECIFICATION', ())
    yield spec
    if spec is None:
        return
    yield read(atom, '/body/workSpecification/binding', WORK['work']['$id'],
        'SANITATION_SELECTED_WORK_DEFINITION', (spec,))


def sanitation_named_condition_inputs(spec, work, read, before_read=None):
    """Retain named-role order and the unique selected-work-position guard."""
    from work_definition_inputs import SCHEMAS as WORK
    for role in ('contact', 'termination'):
        selected = spec[role]
        matches = [(i, item) for i, item in enumerate(work['finishConditions'])
                   if item['conditionId'] == selected['conditionId']]
        record = None
        if len(matches) == 1:
            index, item = matches[0]
            if before_read is not None:
                before_read(role, index, item)
            record = read(spec, '/' + role + '/definitionBinding',
                WORK['workCondition']['$id'],
                'SANITATION_NAMED_' + role.upper() + '_CONDITION', (work,))
        yield role, matches, record


def read_sanitation_duration_unit(condition, method, spec, work, read):
    """Read CONTACT unit meaning independently of earlier semantic failures."""
    if condition['predicateKind'] != CONTACT:
        return None
    return read(method, '/quantityContext/unitProfile', TERM_SCHEMAS['term']['$id'],
        'SANITATION_DURATION_UNIT_MEANING', (spec, work))


def evaluate(condition, atom, method, criterion, measurement, property_definition, sources, schemas, condition_binding):
    register(schemas)
    errors, missing, refs, ids, comparisons = [], [], [], [], []
    origins = {id(v['record']): v['id'] for v in sources}
    retained = None; interval_context = None; claim_meaning = None

    def original(record, path): return {'inputRole': origins[id(record)], 'pointer': path}
    def claimed(path): return {'inputRole': 'ATOM:' + atom['atomId'], 'pointer': path}
    def result():
        return {'errors': errors, 'remainingRoles': missing, 'requiredReferences': refs,
            'sourceInputIds': sorted(set(ids)), 'comparisons': comparisons,
            'retainedSourceQualifications': retained, 'intervalContext': interval_context}
    def compare(code, actual, expected, source, destination, equal=None):
        if equal is None: equal = same(actual, expected)
        comparisons.append({'predicateId': code, 'source': {**source, 'valueDigest': digest(actual)},
            'destination': {**destination, 'valueDigest': digest(expected)}, 'disposition': 'PASS' if equal else 'FAIL'})
        if not equal: errors.append({'code': code, 'pointer': source['pointer']})
    def get(binding, schema_id, role):
        refs.append({'role': role, 'binding': binding, 'pointer': '/sanitation/' + role})
        found = [v for v in sources if same(v['binding'], binding)]
        if len(found) != 1:
            missing.append({'role': role, 'pointer': '/sanitation/' + role}); return None
        entry = found[0]; ids.append(entry['id'])
        shape = schemas.errors(schema_id, entry['record']); errors.extend(shape)
        return None if shape else entry['record']

    def read(parent, path, schema_id, role, prerequisites):
        return get(pointer(parent, path), schema_id, role)

    binding = condition['sanitationSpecificationBinding']
    initial = sanitation_initial_inputs(condition, atom, read)
    spec = next(initial)
    if spec is None: return result()
    compare('SANITATION_SPECIFICATION_IDENTITY_MISMATCH', spec['definitionId'], binding['ref'],
        original(spec, '/definitionId'), original(condition, '/sanitationSpecificationBinding/ref'))
    body = atom['body']; work = body['workSpecification']; time = atom['scope']['subjectTime']
    work_definition = next(initial)
    if work_definition is None: return result()
    for key, expected, path in [
        ('workSpecificationBinding', work['binding'], '/body/workSpecification/binding'),
        ('sanitationKind', body['parameters']['sanitationKind'], '/body/parameters/sanitationKind'),
        ('procedureBinding', work['procedure'], '/body/workSpecification/procedure'),
        ('materialBinding', body['parameters']['material'], '/body/parameters/material'),
        ('contactDurationParameterId', body['parameters']['contactDuration']['quantityParameterId'], '/body/parameters/contactDuration/quantityParameterId'),
        ('finishConditionIds', work['finishConditionIds'], '/body/workSpecification/finishConditionIds')]:
        compare('SANITATION_SPECIFICATION_' + key.upper() + '_MISMATCH', spec[key], expected,
            original(spec, '/' + key), claimed(path))
    compare('SANITATION_METHOD_PROCEDURE_MISMATCH', body['parameters']['method'], work['procedure'],
        claimed('/body/parameters/method'), claimed('/body/workSpecification/procedure'))
    if spec['contact']['conditionId'] == spec['termination']['conditionId'] or same(spec['contact']['definitionBinding'], spec['termination']['definitionBinding']):
        errors.append({'code': 'SANITATION_DISTINCT_CONTACT_AND_TERMINATION_REQUIRED', 'pointer': '/termination'})
    # Both conditions must actually occur in the selected work definition. The
    # work evaluator will evaluate every one, including extra procedure checks.
    def before_named_read(role, index, item):
        compare('SANITATION_' + role.upper() + '_CONDITION_BINDING_MISMATCH', item['definitionBinding'], spec[role]['definitionBinding'],
            original(work_definition, '/finishConditions/' + str(index) + '/definitionBinding'), original(spec, '/' + role + '/definitionBinding'))
    for role, found, named_condition in sanitation_named_condition_inputs(
            spec, work_definition, read, before_named_read):
        selected = spec[role]
        if len(found) != 1:
            errors.append({'code': 'SANITATION_REQUIRED_' + role.upper() + '_CONDITION_MISSING', 'pointer': '/finishConditions'}); continue
        if named_condition is None: continue
        compare('SANITATION_NAMED_CONDITION_IDENTITY_MISMATCH', named_condition['definitionId'], selected['definitionBinding']['ref'],
            original(named_condition, '/definitionId'), original(spec, '/' + role + '/definitionBinding/ref'))
        for key in ['conditionId', 'predicateKind']:
            compare('SANITATION_NAMED_CONDITION_' + key.upper() + '_MISMATCH', named_condition[key], selected[key],
                original(named_condition, '/' + key), original(spec, '/' + role + '/' + key))
        if 'sanitationSpecificationBinding' not in named_condition:
            errors.append({'code': 'SANITATION_NAMED_CONDITION_SPECIFICATION_MISSING', 'pointer': '/sanitationSpecificationBinding'})
        else:
            compare('SANITATION_NAMED_CONDITION_SPECIFICATION_MISMATCH', named_condition['sanitationSpecificationBinding'], binding,
                original(named_condition, '/sanitationSpecificationBinding'), original(condition, '/sanitationSpecificationBinding'))
    role = 'contact' if condition['predicateKind'] == CONTACT else 'termination'
    selected = spec[role]; base = '/' + role
    for key in ['conditionId', 'predicateKind']:
        compare('SANITATION_CONDITION_' + key.upper() + '_MISMATCH', condition[key], selected[key],
            original(condition, '/' + key), original(spec, base + '/' + key))
    compare('SANITATION_CURRENT_CONDITION_IDENTITY_MISMATCH', condition['definitionId'], selected['definitionBinding']['ref'],
        original(condition, '/definitionId'), original(spec, base + '/definitionBinding/ref'))
    compare('SANITATION_PROPERTY_SELECTION_MISMATCH', method['propertyBinding'], selected['propertyBinding'],
        original(method, '/propertyBinding'), original(spec, base + '/propertyBinding'))
    compare('SANITATION_MEASUREMENT_QUANTITY_CONTEXT_MISMATCH', method['quantityContext'], selected['quantityContext'],
        original(method, '/quantityContext'), original(spec, base + '/quantityContext'))
    compare('SANITATION_THRESHOLD_OPERATOR_MISMATCH', criterion['operator'], selected['operator'],
        original(criterion, '/operator'), original(spec, base + '/operator'))
    threshold_field = 'minimumContactDuration' if role == 'contact' else 'maximumFinishActivity'
    threshold = spec[threshold_field]
    compare('SANITATION_THRESHOLD_SPECIFICATION_MISMATCH', criterion['threshold'], threshold,
        original(criterion, '/threshold'), original(spec, '/' + threshold_field))
    for key in ['quantityKind', 'unit', 'unitProfile']:
        compare('SANITATION_THRESHOLD_' + key.upper() + '_MISMATCH', threshold[key], selected['quantityContext'][key],
            original(spec, '/' + threshold_field + '/' + key), original(spec, base + '/quantityContext/' + key))
    if Decimal(spec['minimumContactDuration']['decimal']) <= 0:
        errors.append({'code': 'SANITATION_POSITIVE_REQUIRED_CONTACT_DURATION_REQUIRED', 'pointer': '/minimumContactDuration/decimal'})
    if 'start' not in time or 'end' not in time:
        missing.append({'role': 'SANITATION_BOUNDED_CONTACT_WORK_INTERVAL', 'pointer': '/scope/subjectTime'})
    if 'at' not in method['scope']['subjectTime']:
        errors.append({'code': 'SANITATION_FINISH_INSTANT_OBSERVATION_REQUIRED', 'pointer': '/method/scope/subjectTime'})
    meaning = property_definition.get('sanitationPropertyMeaning')
    if meaning is None:
        missing.append({'role': 'SANITATION_EXACT_PROPERTY_MEANING', 'pointer': '/property/sanitationPropertyMeaning'})
    else:
        for key, expected, dest in [
            ('specificationBinding', binding, original(condition, '/sanitationSpecificationBinding')),
            ('materialBinding', spec['materialBinding'], original(spec, '/materialBinding')),
            ('workTime', time, claimed('/scope/subjectTime'))]:
            compare('SANITATION_PROPERTY_' + key.upper() + '_MISMATCH', meaning[key], expected,
                original(property_definition, '/sanitationPropertyMeaning/' + key), dest)
        expected_role = 'MINIMUM_CONTINUOUS_MATERIAL_CONTACT_ACROSS_SELECTED_EXTENT' if role == 'contact' else 'SELECTED_SANITATION_PROCEDURE_ACTIVITY_AT_FINISH'
        if meaning['role'] != expected_role:
            errors.append({'code': 'SANITATION_PROPERTY_ROLE_MISMATCH', 'pointer': '/property/sanitationPropertyMeaning/role'})
    quantity = None; path = None; seconds_per_unit = None; work_seconds = None; unit = None
    if role == 'contact':
        from fractions import Fraction
        from time_validation import foreign_seconds
        unit = read_sanitation_duration_unit(condition, method, spec, work_definition, read)
        if unit is not None:
            compare('SANITATION_DURATION_UNIT_IDENTITY_MISMATCH',unit['definitionId'],method['quantityContext']['unitProfile']['ref'],
                original(unit,'/definitionId'),original(method,'/quantityContext/unitProfile/ref'))
            if isinstance(unit['quantityContext'],dict):
                for key in ['quantityKind','unit']:
                    compare('SANITATION_DURATION_UNIT_'+key.upper()+'_MISMATCH',unit['quantityContext'][key],method['quantityContext'][key],
                        original(unit,'/quantityContext/'+key),original(method,'/quantityContext/'+key))
            unit_meaning=unit.get('durationUnitMeaning')
            if unit_meaning is None:missing.append({'role':'SANITATION_DURATION_UNIT_SCALE','pointer':'/unit/durationUnitMeaning'})
            else:
                seconds_per_unit=Fraction(unit_meaning['secondsPerUnit'])
                if seconds_per_unit<=0:
                    errors.append({'code':'SANITATION_POSITIVE_DURATION_UNIT_SCALE_REQUIRED','pointer':'/durationUnitMeaning/secondsPerUnit'});seconds_per_unit=None
        if 'start' in time and 'end' in time:
            try:work_seconds=Fraction(foreign_seconds(time['end']))-Fraction(foreign_seconds(time['start']))
            except ValueError:missing.append({'role':'SANITATION_EXACT_WORK_TIME_INTERPRETATION','pointer':'/scope/subjectTime'})
        matches = [(i, q) for i, q in enumerate(body['quantityParameters']) if q['parameterId'] == spec['contactDurationParameterId']]
        if len(matches) != 1:
            errors.append({'code': 'SANITATION_ACTUAL_CONTACT_DURATION_PARAMETER_NOT_UNIQUE', 'pointer': '/body/quantityParameters'}); return result()
        index, quantity = matches[0]; path = '/body/quantityParameters/' + str(index)
        if quantity['parameterRole'] != 'TIMING_INTERVAL' or quantity['valuePosture'] != 'ACTUAL':
            errors.append({'code': 'SANITATION_ACTUAL_TIMING_INTERVAL_REQUIRED', 'pointer': path})
        if quantity['material']['presence'] != 'NOT_APPLICABLE':
            errors.append({'code':'SANITATION_DURATION_IS_NOT_MATERIAL_QUANTITY','pointer':path+'/material'})
        compare('SANITATION_QUANTITY_ACTIVITY_MISMATCH', quantity['activityInstance'], body['activityInstance'],
            claimed(path + '/activityInstance'), claimed('/body/activityInstance'))
        for key, expected, dest in [('target', body['target'], '/body/target'), ('extent', body['extent'], '/body/extent'), ('subjectTime', time, '/scope/subjectTime')]:
            compare('SANITATION_QUANTITY_' + key.upper() + '_MISMATCH', quantity['appliesTo'][key], expected,
                claimed(path + '/appliesTo/' + key), claimed(dest))
        if quantity['appliesTo']['phase'] != 'WHOLE_ACTIVITY':
            errors.append({'code': 'SANITATION_WHOLE_WORK_CONTACT_DURATION_REQUIRED', 'pointer': path + '/appliesTo/phase'})
        if quantity['basis']['presence'] != 'NOT_APPLICABLE':
            errors.append({'code': 'SANITATION_ABSOLUTE_CONTACT_DURATION_REQUIRED', 'pointer': path + '/basis'})
        if quantity['value']['state'] != 'STATED':
            missing.append({'role': 'SANITATION_STATED_ACTUAL_CONTACT_DURATION', 'pointer': path + '/value'})
        else:
            value = quantity['value']
            claim_meaning = spec['reportedActualDurationMeanings'][value['qualifier']]
            if claim_meaning == 'REQUIRES_SELECTED_QUALIFIER_MEANING':
                missing.append({'role': 'SANITATION_EXACT_REPORTED_CONTACT_DURATION_MEANING', 'pointer': path + '/value/qualifier'})
            for key in ['quantityKind', 'unit']:
                compare('SANITATION_ACTUAL_CONTACT_DURATION_' + key.upper() + '_MISMATCH', value['quantity'][key], selected['quantityContext'][key],
                    claimed(path + '/value/quantity/' + key), original(spec, base + '/quantityContext/' + key))
            compare('SANITATION_ACTUAL_CONTACT_DURATION_UNIT_PROFILE_MISMATCH', value['unitProfile'], selected['quantityContext']['unitProfile'],
                claimed(path + '/value/unitProfile'), original(spec, base + '/quantityContext/unitProfile'))
    retained = {'scope': 'CONDITIONAL_SANITATION_CONTACT_AND_TERMINATION',
        'specificationBinding': binding, 'role': role, 'originalMeasurement': measurement,
        'originalClaimedContactDuration': quantity, 'originalDurationUnitDefinition':unit,
        'reportedActualDurationMeaning': claim_meaning,
        'notEstablished': ['ACHIEVED_HYGIENE', 'CLEANOUT_COMPLETION', 'PHYSICAL_TRUTH', 'SOURCE_ELIGIBLE_USE', 'ACCEPTED_EXECUTION', 'OTHER_BOUND_FINISH_CONDITIONS']}
    interval_context = {'role': role, 'quantity': quantity, 'path': path, 'claimMeaning': claim_meaning,
        'measurement': measurement, 'measurementOrigin': original(measurement, '/result'),
        'claimRole': 'ATOM:' + atom['atomId'], 'workTime':time, 'secondsPerUnit':seconds_per_unit, 'workSeconds':work_seconds}
    return result()


def check_interval(interval, context):
    """Interpret the derived set without presenting it as an original value."""
    errors, missing, comparisons = [], [], []
    lower, upper = interval['lower'], interval['upper']
    if 'decimal' not in lower or Decimal(lower['decimal']) < 0:
        errors.append({'code': 'SANITATION_NONNEGATIVE_OBSERVATION_REQUIRED', 'pointer': '/measurement/result'})
    quantity = context['quantity']
    if context['role']=='termination':
        if ('decimal' not in lower or 'decimal' not in upper or
                Decimal(lower['decimal']) not in [0,1] or Decimal(upper['decimal'])!=Decimal(lower['decimal']) or
                not lower['inclusive'] or not upper['inclusive']):
            errors.append({'code':'SANITATION_EXACT_BOOLEAN_ACTIVITY_OBSERVATION_REQUIRED','pointer':'/measurement/result'})
    if context['role']=='contact' and context.get('secondsPerUnit') is not None and context.get('workSeconds') is not None:
        from fractions import Fraction
        scale,maximum=context['secondsPerUnit'],context['workSeconds']
        lo_seconds=Fraction(lower['decimal'])*scale if 'decimal' in lower else None
        hi_seconds=Fraction(upper['decimal'])*scale if 'decimal' in upper else None
        impossible=lo_seconds is not None and (lo_seconds>maximum or lo_seconds==maximum and not lower['inclusive'])
        within=hi_seconds is not None and hi_seconds<=maximum
        if impossible:errors.append({'code':'SANITATION_CONTACT_DURATION_EXCEEDS_WORK_INTERVAL','pointer':'/measurement/result'})
        elif not within:missing.append({'role':'SANITATION_CONTACT_DURATION_WORK_INTERVAL_BOUND_UNRESOLVED','pointer':'/measurement/result'})
        if impossible or within:
            comparisons.append({'predicateId':'SANITATION_CONTACT_DURATION_WITHIN_ORIGINAL_WORK_INTERVAL',
                'source':{**context['measurementOrigin'],'valueDigest':digest(context['measurement']['result'])},
                'destination':{'inputRole':context['claimRole'],'pointer':'/scope/subjectTime','valueDigest':digest(context['workTime'])},
                'disposition':'FAIL' if impossible else 'PASS'})
    if context['role'] == 'contact' and quantity and quantity['value']['state'] == 'STATED':
        amount = Decimal(quantity['value']['quantity']['decimal'])
        lo = Decimal(lower['decimal']) if 'decimal' in lower else None
        hi = Decimal(upper['decimal']) if 'decimal' in upper else None
        contains = (lo is None or amount > lo or amount == lo and lower['inclusive']) and (hi is None or amount < hi or amount == hi and upper['inclusive'])
        meaning = context['claimMeaning']
        if meaning == 'REPORTED_POINT':
            satisfied = lo == hi == amount and lower.get('inclusive') and upper.get('inclusive')
            disjoint = not contains
        elif meaning == 'INCLUSIVE_LOWER_BOUND':
            satisfied = lo is not None and lo >= amount
            disjoint = hi is not None and (hi < amount or hi == amount and not upper['inclusive'])
        elif meaning == 'INCLUSIVE_UPPER_BOUND':
            satisfied = hi is not None and hi <= amount
            disjoint = lo is not None and (lo > amount or lo == amount and not lower['inclusive'])
        else:
            # Unspecified uncertainty or label-limit use has no invented set.
            return {'errors': errors, 'remainingRoles': missing, 'comparisons': comparisons}
        if disjoint:
            code = 'SANITATION_CLAIMED_CONTACT_DURATION_OUTSIDE_OBSERVED_SET'
            errors.append({'code': code, 'pointer': context['path'] + '/value/quantity/decimal'})
        elif not satisfied:
            missing.append({'role': 'SANITATION_EXACT_CONTACT_DURATION_UNRESOLVED' if meaning == 'REPORTED_POINT' else 'SANITATION_ACTUAL_CONTACT_DURATION_BOUND_UNRESOLVED', 'pointer': '/measurement/result'})
        # A range merely overlapping the claim gives no PASS. The original
        # result and qualified claim are compared only when decided.
        if satisfied or disjoint:
            comparisons.append({'predicateId': 'SANITATION_ORIGINAL_RESULT_ESTABLISHES_CLAIMED_ACTUAL_CONTACT_DURATION',
                'source': {**context['measurementOrigin'], 'valueDigest': digest(context['measurement']['result'])},
                'destination': {'inputRole': context['claimRole'], 'pointer': context['path'] + '/value',
                    'valueDigest': digest(quantity['value'])}, 'disposition': 'PASS' if satisfied else 'FAIL'})
    return {'errors': errors, 'remainingRoles': missing, 'comparisons': comparisons}
