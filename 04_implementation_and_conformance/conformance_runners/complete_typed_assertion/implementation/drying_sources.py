"""O07 moisture finish from exact target, basis and original measurement use.

The independently selected definition fixes the water-mass ratio and scale.
No wet/dry or fraction/percent conversion is inferred. Every other condition
in the bound procedure remains required by work_sources. This is conditional
source interpretation, not accepted execution, measurement truth or admission.
"""
from decimal import Decimal
from strict_inputs import same, digest
from drying_definitions import SCHEMAS, register


def interval_errors(interval, ratio):
    """Reject impossible moisture sets before the ordinary criterion comparison."""
    lower, upper = interval['lower'], interval['upper']
    invalid = 'decimal' not in lower or Decimal(lower['decimal']) < 0
    if ratio['massBasis'] == 'WET_BASIS':
        invalid = invalid or 'decimal' not in upper or Decimal(upper['decimal']) > ratio['scale']
    return [{'code': 'DRYING_MOISTURE_OUTSIDE_DEFINED_RATIO_DOMAIN', 'pointer': '/measurement/result'}] if invalid else []


def resolve_drying_specification(condition, read, need):
    if condition.get('dryingSpecificationBinding') is None:
        need('SELECTED_DRYING_FINISH_SPECIFICATION', '/condition/dryingSpecificationBinding'); return None
    return read(condition, '/dryingSpecificationBinding', SCHEMAS['drying']['$id'],
                'SELECTED_DRYING_FINISH_SPECIFICATION', ())


def drying_target_parameters(atom):
    parameter_id = atom['body']['parameters']['targetMoisture']['quantityParameterId']
    return [(i, value) for i, value in enumerate(atom['body']['quantityParameters'])
            if value['parameterId'] == parameter_id]


def drying_target_has_basis(target):
    return target['value']['state'] == 'STATED' and target['basis']['presence'] == 'PRESENT'


def drying_term_inputs(method, spec, read):
    """Yield independently resolved term originals in the evaluator's order."""
    from definition_inputs import SCHEMAS as TERMS
    ratio = spec['ratioMeaning']
    for path, role, field, expected in [
        ('/propertyBinding', 'DRYING_MOISTURE_PROPERTY_MEANING', 'moisturePropertyMeaning',
         {k: ratio[k] for k in ['massBasis', 'numerator', 'denominator']}),
        ('/quantityContext/unitProfile', 'DRYING_MASS_FRACTION_UNIT_MEANING', 'massFractionUnitMeaning',
         {'scale': ratio['scale'], 'ratio': 'MASS_OVER_MASS'})]:
        term = read(method, path, TERMS['term']['$id'], role, (spec,))
        yield role, field, expected, term


def evaluate(condition, atom, method, criterion, measurement, sources, schemas):
    from strict_inputs import pointer
    register(schemas)
    errors, missing, refs, ids, comparisons = [], [], [], [], []
    retained, ratio = None, None
    origins = {}
    for source in sources:
        origins[id(source['record'])] = source['id']

    def original(record, path):
        return {'inputRole': origins[id(record)], 'pointer': path}

    def claimed(path):
        return {'inputRole': 'ATOM:' + atom['atomId'], 'pointer': path}

    def result():
        return {'disposition': 'FAIL' if errors else 'NOT_EVALUATED' if missing else 'PASS',
            'errors': errors, 'remainingRoles': missing, 'requiredReferences': refs,
            'sourceInputIds': sorted(set(ids)), 'comparisons': comparisons,
            'retainedSourceQualifications': retained, 'ratioMeaning': ratio}

    def compare(code, actual, expected, path, source=None, destination=None, equal=None):
        if equal is None: equal = same(actual, expected)
        fact = {'predicateId': code, 'pointer': path, 'equal': equal,
            'actualValueDigest': digest(actual), 'expectedValueDigest': digest(expected)}
        if source is not None and destination is not None:
            fact.update(source={**source, 'valueDigest': digest(actual)},
                destination={**destination, 'valueDigest': digest(expected)}, disposition='PASS' if equal else 'FAIL')
        comparisons.append(fact)
        if not equal: errors.append({'code': code, 'pointer': path})

    compare('WORK_CONDITION_PREDICATE_KIND_MISMATCH', condition['predicateKind'],
        'TARGET_MOISTURE_ON_DEFINED_MASS_BASIS', '/condition/predicateKind')
    def need(role, path): missing.append({'role': role, 'pointer': path})
    def read_input(parent, path, schema, role, prerequisites):
        binding = pointer(parent, path)
        location = '/condition/dryingSpecificationBinding' if role == 'SELECTED_DRYING_FINISH_SPECIFICATION' else '/drying/' + role
        refs.append({'role': role, 'binding': binding, 'pointer': location})
        found = [v for v in sources if same(v['binding'], binding)]
        if len(found) != 1: need(role, location); return None
        entry = found[0]; ids.append(entry['id'])
        shape = schemas.errors(schema, entry['record']); errors.extend(shape)
        return None if shape else entry['record']
    spec = resolve_drying_specification(condition, read_input, need)
    if spec is None: return result()
    binding = condition['dryingSpecificationBinding']
    compare('DRYING_DEFINITION_IDENTITY_MISMATCH', spec['definitionId'], binding['ref'], '/definitionId',
        original(spec, '/definitionId'), original(condition, '/dryingSpecificationBinding/ref'))
    body = atom['body']; work = body['workSpecification']; parameters = body['parameters']
    for key, expected, path in [
        ('workSpecificationBinding', work['binding'], '/body/workSpecification/binding'),
        ('procedureBinding', work['procedure'], '/body/workSpecification/procedure'),
        ('inputLot', parameters['inputLot'], '/body/parameters/inputLot'),
        ('finishConditionIds', work['finishConditionIds'], '/body/workSpecification/finishConditionIds')]:
        compare('DRYING_SPECIFICATION_' + key.upper() + '_MISMATCH', spec[key], expected, '/' + key,
            original(spec, '/' + key), claimed(path))
    compare('DRYING_METHOD_PROCEDURE_MISMATCH', parameters['method'], work['procedure'], '/body/parameters/method',
        claimed('/body/parameters/method'), claimed('/body/workSpecification/procedure'))
    if body['target']['kind'] != 'LOT' or not same(parameters['inputLot'], body['target']['binding']):
        missing.append({'role': 'DRYING_INPUT_LOT_TO_WORK_TARGET_RELATION', 'pointer': '/body/parameters/inputLot'})
    selected_parameters = drying_target_parameters(atom)
    if len(selected_parameters) != 1:
        errors.append({'code': 'DRYING_TARGET_PARAMETER_NOT_UNIQUE', 'pointer': '/body/quantityParameters'})
        return result()
    index, target = selected_parameters[0]; path = '/body/quantityParameters/' + str(index)
    compare('DRYING_TARGET_PARAMETER_MISMATCH', spec['targetMoistureParameter'], target, '/targetMoistureParameter',
        original(spec, '/targetMoistureParameter'), claimed(path))
    for key, expected in [('valuePosture', 'TARGET'), ('parameterRole', 'OTHER_PARAMETER'), ('otherRoleDefinition', 'MOISTURE_TARGET')]:
        compare('DRYING_TARGET_' + key.upper() + '_MISMATCH', target.get(key), expected, path + '/' + key)
    if not drying_target_has_basis(target):
        missing.append({'role': 'DRYING_STATED_TARGET_AND_MASS_BASIS', 'pointer': path})
        return result()
    basis = target['basis']; value = target['value']; ratio = spec['ratioMeaning']; quantity = value['quantity']
    if value['qualifier'] not in ['EXACT', 'MAXIMUM', 'LABEL_LIMIT', 'MACHINE_REPORTED', 'HUMAN_REPORTED']:
        missing.append({'role': 'DRYING_EXACT_UPPER_BOUND_TARGET_MEANING', 'pointer': path + '/value/qualifier'})
    for role, field, expected, term in drying_term_inputs(method, spec, read_input):
        if term is None: continue
        if field not in term:
            missing.append({'role': role, 'pointer': '/' + field}); continue
        compare(role + '_MISMATCH', term[field], expected, '/' + field)
        # Trace exact original scalar fields, not the synthetic projection.
        for key in expected:
            if key in ratio:
                compare(role + '_' + key.upper() + '_MISMATCH', term[field][key], ratio[key], '/' + field + '/' + key,
                    original(term, '/' + field + '/' + key), original(spec, '/ratioMeaning/' + key))
    if 'massBasis' not in basis:
        missing.append({'role': 'DRYING_TARGET_MASS_BASIS_DISCLOSURE', 'pointer': path + '/basis/massBasis'})
    else:
        compare('DRYING_TARGET_BASIS_MASSBASIS_MISMATCH', basis['massBasis'], ratio['massBasis'], path + '/basis/massBasis',
            claimed(path + '/basis/massBasis'), original(spec, '/ratioMeaning/massBasis'))
    subject = basis['subject']; subject_path = path + '/basis/subject'
    if 'binding' in subject:
        compare('DRYING_TARGET_BASIS_SUBJECT_KIND_MISMATCH', subject['kind'], 'LOT', subject_path + '/kind')
        subject_binding = subject['binding']; subject_path += '/binding'
    else:
        # The value schema also permits a bare immutable reference. Retain
        # its exact selector without inferring a kind from its name or use.
        subject_binding = subject
        missing.append({'role': 'DRYING_TARGET_BASIS_SUBJECT_KIND', 'pointer': subject_path})
    compare('DRYING_TARGET_BASIS_INPUT_LOT_MISMATCH', subject_binding, parameters['inputLot'], subject_path,
        claimed(subject_path), claimed('/body/parameters/inputLot'))
    if basis['quantity']['quantityKind'] != 'qudt:Mass' or Decimal(basis['quantity']['decimal']) <= 0:
        errors.append({'code': 'DRYING_POSITIVE_MASS_DENOMINATOR_REQUIRED', 'pointer': path + '/basis/quantity'})
    for key, expected in [('activityInstance', body['activityInstance'])]:
        compare('DRYING_TARGET_ACTIVITY_MISMATCH', target[key], expected, path + '/' + key, claimed(path + '/' + key), claimed('/body/' + key))
    for key, expected, dest in [('target', body['target'], '/body/target'), ('extent', body['extent'], '/body/extent'),
            ('subjectTime', atom['scope']['subjectTime'], '/scope/subjectTime')]:
        compare('DRYING_TARGET_APPLICABILITY_' + key.upper() + '_MISMATCH', target['appliesTo'][key], expected,
            path + '/appliesTo/' + key, claimed(path + '/appliesTo/' + key), claimed(dest))
    compare('DRYING_PROPERTY_SELECTION_MISMATCH', spec['propertyBinding'], method['propertyBinding'], '/propertyBinding',
        original(spec, '/propertyBinding'), original(method, '/propertyBinding'))
    compare('DRYING_MEASUREMENT_QUANTITY_CONTEXT_MISMATCH', method['quantityContext'], spec['quantityContext'], '/method/quantityContext',
        original(method, '/quantityContext'), original(spec, '/quantityContext'))
    for key in ['quantityKind', 'unit']:
        compare('DRYING_TARGET_' + key.upper() + '_MISMATCH', quantity[key], spec['quantityContext'][key], path + '/value/quantity/' + key,
            claimed(path + '/value/quantity/' + key), original(spec, '/quantityContext/' + key))
    compare('DRYING_TARGET_UNIT_PROFILE_MISMATCH', value['unitProfile'], spec['quantityContext']['unitProfile'], path + '/value/unitProfile',
        claimed(path + '/value/unitProfile'), original(spec, '/quantityContext/unitProfile'))
    compare('DRYING_THRESHOLD_OPERATOR_MISMATCH', criterion['operator'], spec['thresholdOperator'], '/criterion/operator',
        original(criterion, '/operator'), original(spec, '/thresholdOperator'))
    threshold = criterion['threshold']
    if 'decimal' not in threshold:
        errors.append({'code': 'DRYING_SCALAR_TARGET_THRESHOLD_REQUIRED', 'pointer': '/criterion/threshold'})
        return result()
    compare('DRYING_THRESHOLD_TARGET_MISMATCH', threshold['decimal'], quantity['decimal'], '/criterion/threshold/decimal',
        original(criterion, '/threshold/decimal'), claimed(path + '/value/quantity/decimal'),
        Decimal(threshold['decimal']) == Decimal(quantity['decimal']))
    compare('DRYING_THRESHOLD_QUALIFIER_MISMATCH', threshold['qualifier'], 'EXACT', '/criterion/threshold/qualifier')
    target_amount = Decimal(quantity['decimal'])
    if target_amount < 0 or ratio['massBasis'] == 'WET_BASIS' and target_amount > ratio['scale']:
        errors.append({'code': 'DRYING_TARGET_OUTSIDE_DEFINED_RATIO_DOMAIN', 'pointer': path + '/value/quantity/decimal'})
    retained = {'scope': 'CONDITIONAL_MOISTURE_INTERPRETATION_ONLY', 'ratioMeaning': ratio,
        'targetMoistureParameter': target, 'measurementQualifications': {k: v for k, v in measurement.items()
            if k not in ['schemaVersion', 'measurementEvidenceId']},
        'targetThresholdMeaning': spec['targetThresholdMeaning'],
        'finishConditionIds': spec['finishConditionIds'],
        'notEstablished': ['SOURCE_ELIGIBLE_USE', 'ACCEPTED_EXECUTION', 'PHYSICAL_TRUTH', 'OTHER_FINISH_CONDITIONS_BY_THIS_MOISTURE_RESULT']}
    return result()
