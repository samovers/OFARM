"""O04 cumulative delivery and zero inflow, from separate original sources.

The required minimum comes from a selected normative specification. The claim's
ACTUAL water volume is reconciled with the observed delivered-volume set. A
minimum-satisfying observation alone cannot establish either the claimed actual
amount or termination. Other bound finish conditions remain mandatory.
"""
from decimal import Decimal
from strict_inputs import same, digest, pointer
from irrigation_definitions import SCHEMAS, register, DELIVERY, TERMINATION


def irrigation_initial_inputs(condition, atom, read):
    """Yield specification then work, preserving the comparison between reads."""
    from work_definition_inputs import SCHEMAS as WORK
    spec = read(condition, '/irrigationSpecificationBinding',
        SCHEMAS['irrigation']['$id'], 'SELECTED_IRRIGATION_FINISH_SPECIFICATION', ())
    yield spec
    if spec is None:
        return
    yield read(atom, '/body/workSpecification/binding', WORK['work']['$id'],
        'IRRIGATION_SELECTED_WORK_DEFINITION', (spec,))


def irrigation_named_condition_inputs(spec, work, read, before_read=None):
    """Retain named-role order and the unique selected-work-position guard."""
    from work_definition_inputs import SCHEMAS as WORK
    for role in ('delivery', 'termination'):
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
                'IRRIGATION_NAMED_' + role.upper() + '_CONDITION', (work,))
        yield role, matches, record


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
        refs.append({'role': role, 'binding': binding, 'pointer': '/irrigation/' + role})
        found = [v for v in sources if same(v['binding'], binding)]
        if len(found) != 1:
            missing.append({'role': role, 'pointer': '/irrigation/' + role}); return None
        entry = found[0]; ids.append(entry['id'])
        shape = schemas.errors(schema_id, entry['record']); errors.extend(shape)
        return None if shape else entry['record']

    def read(parent, path, schema_id, role, prerequisites):
        return get(pointer(parent, path), schema_id, role)

    binding = condition['irrigationSpecificationBinding']
    initial = irrigation_initial_inputs(condition, atom, read)
    spec = next(initial)
    if spec is None: return result()
    compare('IRRIGATION_SPECIFICATION_IDENTITY_MISMATCH', spec['definitionId'], binding['ref'],
        original(spec, '/definitionId'), original(condition, '/irrigationSpecificationBinding/ref'))
    body = atom['body']; work = body['workSpecification']; time = atom['scope']['subjectTime']
    work_definition = next(initial)
    if work_definition is None: return result()
    for key, expected, path in [
        ('workSpecificationBinding', work['binding'], '/body/workSpecification/binding'),
        ('procedureBinding', work['procedure'], '/body/workSpecification/procedure'),
        ('waterSourceBinding', body['parameters']['waterSource'], '/body/parameters/waterSource'),
        ('waterVolumeParameterId', body['parameters']['waterVolume']['quantityParameterId'], '/body/parameters/waterVolume/quantityParameterId'),
        ('finishConditionIds', work['finishConditionIds'], '/body/workSpecification/finishConditionIds')]:
        compare('IRRIGATION_SPECIFICATION_' + key.upper() + '_MISMATCH', spec[key], expected,
            original(spec, '/' + key), claimed(path))
    compare('IRRIGATION_METHOD_PROCEDURE_MISMATCH', body['parameters']['method'], work['procedure'],
        claimed('/body/parameters/method'), claimed('/body/workSpecification/procedure'))
    if spec['delivery']['conditionId'] == spec['termination']['conditionId'] or same(spec['delivery']['definitionBinding'], spec['termination']['definitionBinding']):
        errors.append({'code': 'IRRIGATION_DISTINCT_DELIVERY_AND_TERMINATION_REQUIRED', 'pointer': '/termination'})
    # Both conditions must actually occur in the selected work definition. The
    # work evaluator will evaluate every one, including extra procedure checks.
    def before_named_read(role, index, item):
        compare('IRRIGATION_' + role.upper() + '_CONDITION_BINDING_MISMATCH', item['definitionBinding'], spec[role]['definitionBinding'],
            original(work_definition, '/finishConditions/' + str(index) + '/definitionBinding'), original(spec, '/' + role + '/definitionBinding'))
    for role, found, named_condition in irrigation_named_condition_inputs(
            spec, work_definition, read, before_named_read):
        selected = spec[role]
        if len(found) != 1:
            errors.append({'code': 'IRRIGATION_REQUIRED_' + role.upper() + '_CONDITION_MISSING', 'pointer': '/finishConditions'}); continue
        if named_condition is None: continue
        compare('IRRIGATION_NAMED_CONDITION_IDENTITY_MISMATCH', named_condition['definitionId'], selected['definitionBinding']['ref'],
            original(named_condition, '/definitionId'), original(spec, '/' + role + '/definitionBinding/ref'))
        for key in ['conditionId', 'predicateKind']:
            compare('IRRIGATION_NAMED_CONDITION_' + key.upper() + '_MISMATCH', named_condition[key], selected[key],
                original(named_condition, '/' + key), original(spec, '/' + role + '/' + key))
        if 'irrigationSpecificationBinding' not in named_condition:
            errors.append({'code': 'IRRIGATION_NAMED_CONDITION_SPECIFICATION_MISSING', 'pointer': '/irrigationSpecificationBinding'})
        else:
            compare('IRRIGATION_NAMED_CONDITION_SPECIFICATION_MISMATCH', named_condition['irrigationSpecificationBinding'], binding,
                original(named_condition, '/irrigationSpecificationBinding'), original(condition, '/irrigationSpecificationBinding'))
    role = 'delivery' if condition['predicateKind'] == DELIVERY else 'termination'
    selected = spec[role]; base = '/' + role
    for key in ['conditionId', 'predicateKind']:
        compare('IRRIGATION_CONDITION_' + key.upper() + '_MISMATCH', condition[key], selected[key],
            original(condition, '/' + key), original(spec, base + '/' + key))
    compare('IRRIGATION_CURRENT_CONDITION_IDENTITY_MISMATCH', condition['definitionId'], selected['definitionBinding']['ref'],
        original(condition, '/definitionId'), original(spec, base + '/definitionBinding/ref'))
    compare('IRRIGATION_PROPERTY_SELECTION_MISMATCH', method['propertyBinding'], selected['propertyBinding'],
        original(method, '/propertyBinding'), original(spec, base + '/propertyBinding'))
    compare('IRRIGATION_MEASUREMENT_QUANTITY_CONTEXT_MISMATCH', method['quantityContext'], selected['quantityContext'],
        original(method, '/quantityContext'), original(spec, base + '/quantityContext'))
    compare('IRRIGATION_THRESHOLD_OPERATOR_MISMATCH', criterion['operator'], selected['operator'],
        original(criterion, '/operator'), original(spec, base + '/operator'))
    threshold_field = 'minimumDeliveredVolume' if role == 'delivery' else 'maximumFinishInflow'
    threshold = spec[threshold_field]
    compare('IRRIGATION_THRESHOLD_SPECIFICATION_MISMATCH', criterion['threshold'], threshold,
        original(criterion, '/threshold'), original(spec, '/' + threshold_field))
    for key in ['quantityKind', 'unit', 'unitProfile']:
        compare('IRRIGATION_THRESHOLD_' + key.upper() + '_MISMATCH', threshold[key], selected['quantityContext'][key],
            original(spec, '/' + threshold_field + '/' + key), original(spec, base + '/quantityContext/' + key))
    if Decimal(spec['minimumDeliveredVolume']['decimal']) <= 0:
        errors.append({'code': 'IRRIGATION_POSITIVE_REQUIRED_VOLUME_REQUIRED', 'pointer': '/minimumDeliveredVolume/decimal'})
    if 'start' not in time or 'end' not in time:
        missing.append({'role': 'IRRIGATION_BOUNDED_DELIVERY_WORK_INTERVAL', 'pointer': '/scope/subjectTime'})
    if 'at' not in method['scope']['subjectTime']:
        errors.append({'code': 'IRRIGATION_FINISH_INSTANT_OBSERVATION_REQUIRED', 'pointer': '/method/scope/subjectTime'})
    meaning = property_definition.get('irrigationPropertyMeaning')
    if meaning is None:
        missing.append({'role': 'IRRIGATION_EXACT_PROPERTY_MEANING', 'pointer': '/property/irrigationPropertyMeaning'})
    else:
        for key, expected, dest in [
            ('specificationBinding', binding, original(condition, '/irrigationSpecificationBinding')),
            ('waterSourceBinding', spec['waterSourceBinding'], original(spec, '/waterSourceBinding')),
            ('workTime', time, claimed('/scope/subjectTime'))]:
            compare('IRRIGATION_PROPERTY_' + key.upper() + '_MISMATCH', meaning[key], expected,
                original(property_definition, '/irrigationPropertyMeaning/' + key), dest)
        expected_role = 'CUMULATIVE_WATER_DELIVERED_OVER_SELECTED_WORK' if role == 'delivery' else 'WATER_INFLOW_TO_SELECTED_EXTENT_AT_FINISH'
        if meaning['role'] != expected_role:
            errors.append({'code': 'IRRIGATION_PROPERTY_ROLE_MISMATCH', 'pointer': '/property/irrigationPropertyMeaning/role'})
    quantity = None; path = None
    if role == 'delivery':
        matches = [(i, q) for i, q in enumerate(body['quantityParameters']) if q['parameterId'] == spec['waterVolumeParameterId']]
        if len(matches) != 1:
            errors.append({'code': 'IRRIGATION_ACTUAL_VOLUME_PARAMETER_NOT_UNIQUE', 'pointer': '/body/quantityParameters'}); return result()
        index, quantity = matches[0]; path = '/body/quantityParameters/' + str(index)
        if quantity['parameterRole'] != 'WATER_VOLUME' or quantity['valuePosture'] != 'ACTUAL':
            errors.append({'code': 'IRRIGATION_ACTUAL_WATER_VOLUME_REQUIRED', 'pointer': path})
        if quantity['material']['presence'] != 'PRESENT' or quantity['material'].get('materialRole') != 'WATER':
            errors.append({'code': 'IRRIGATION_WATER_SOURCE_MATERIAL_REQUIRED', 'pointer': path + '/material'})
        else:
            compare('IRRIGATION_ACTUAL_WATER_SOURCE_MISMATCH', quantity['material']['binding'], spec['waterSourceBinding'],
                claimed(path + '/material/binding'), original(spec, '/waterSourceBinding'))
        compare('IRRIGATION_QUANTITY_ACTIVITY_MISMATCH', quantity['activityInstance'], body['activityInstance'],
            claimed(path + '/activityInstance'), claimed('/body/activityInstance'))
        for key, expected, dest in [('target', body['target'], '/body/target'), ('extent', body['extent'], '/body/extent'), ('subjectTime', time, '/scope/subjectTime')]:
            compare('IRRIGATION_QUANTITY_' + key.upper() + '_MISMATCH', quantity['appliesTo'][key], expected,
                claimed(path + '/appliesTo/' + key), claimed(dest))
        if quantity['appliesTo']['phase'] != 'WHOLE_ACTIVITY':
            errors.append({'code': 'IRRIGATION_WHOLE_WORK_VOLUME_REQUIRED', 'pointer': path + '/appliesTo/phase'})
        if quantity['basis']['presence'] != 'NOT_APPLICABLE':
            errors.append({'code': 'IRRIGATION_ABSOLUTE_VOLUME_REQUIRED', 'pointer': path + '/basis'})
        if quantity['value']['state'] != 'STATED':
            missing.append({'role': 'IRRIGATION_STATED_ACTUAL_VOLUME', 'pointer': path + '/value'})
        else:
            value = quantity['value']
            claim_meaning = spec['reportedActualVolumeMeanings'][value['qualifier']]
            if claim_meaning == 'REQUIRES_SELECTED_QUALIFIER_MEANING':
                missing.append({'role': 'IRRIGATION_EXACT_REPORTED_VOLUME_MEANING', 'pointer': path + '/value/qualifier'})
            for key in ['quantityKind', 'unit']:
                compare('IRRIGATION_ACTUAL_VOLUME_' + key.upper() + '_MISMATCH', value['quantity'][key], selected['quantityContext'][key],
                    claimed(path + '/value/quantity/' + key), original(spec, base + '/quantityContext/' + key))
            compare('IRRIGATION_ACTUAL_VOLUME_UNIT_PROFILE_MISMATCH', value['unitProfile'], selected['quantityContext']['unitProfile'],
                claimed(path + '/value/unitProfile'), original(spec, base + '/quantityContext/unitProfile'))
    retained = {'scope': 'CONDITIONAL_IRRIGATION_DELIVERY_AND_TERMINATION',
        'specificationBinding': binding, 'role': role, 'originalMeasurement': measurement,
        'originalClaimedWaterQuantity': quantity,
        'reportedActualVolumeMeaning': claim_meaning,
        'notEstablished': ['PHYSICAL_TRUTH', 'SOURCE_ELIGIBLE_USE', 'ACCEPTED_EXECUTION', 'OTHER_BOUND_FINISH_CONDITIONS']}
    interval_context = {'role': role, 'quantity': quantity, 'path': path, 'claimMeaning': claim_meaning,
        'measurement': measurement, 'measurementOrigin': original(measurement, '/result'),
        'claimRole': 'ATOM:' + atom['atomId']}
    return result()


def check_interval(interval, context):
    """Interpret the derived set without presenting it as an original value."""
    errors, missing, comparisons = [], [], []
    lower, upper = interval['lower'], interval['upper']
    if 'decimal' not in lower or Decimal(lower['decimal']) < 0:
        errors.append({'code': 'IRRIGATION_NONNEGATIVE_OBSERVATION_REQUIRED', 'pointer': '/measurement/result'})
    quantity = context['quantity']
    if context['role'] == 'delivery' and quantity and quantity['value']['state'] == 'STATED':
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
            code = 'IRRIGATION_CLAIMED_VOLUME_OUTSIDE_OBSERVED_SET'
            errors.append({'code': code, 'pointer': context['path'] + '/value/quantity/decimal'})
        elif not satisfied:
            missing.append({'role': 'IRRIGATION_EXACT_DELIVERED_VOLUME_UNRESOLVED' if meaning == 'REPORTED_POINT' else 'IRRIGATION_ACTUAL_VOLUME_BOUND_UNRESOLVED', 'pointer': '/measurement/result'})
        # A range merely overlapping the claim gives no PASS. The original
        # result and qualified claim are compared only when decided.
        if satisfied or disjoint:
            comparisons.append({'predicateId': 'IRRIGATION_ORIGINAL_RESULT_ESTABLISHES_CLAIMED_ACTUAL_VOLUME',
                'source': {**context['measurementOrigin'], 'valueDigest': digest(context['measurement']['result'])},
                'destination': {'inputRole': context['claimRole'], 'pointer': context['path'] + '/value',
                    'valueDigest': digest(quantity['value'])}, 'disposition': 'PASS' if satisfied else 'FAIL'})
    return {'errors': errors, 'remainingRoles': missing, 'comparisons': comparisons}
