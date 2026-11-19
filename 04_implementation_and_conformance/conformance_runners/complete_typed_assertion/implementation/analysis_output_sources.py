"""O22 finish: a recorded original analysis output for the exact selected use.

An already collected sample, execution carrier, pending result, or arbitrary
passing criterion cannot discharge this condition. Sample/term version use,
source eligibility and factual acceptance remain distinct row/owner duties.
"""
from strict_inputs import same, digest
from analysis_output_definitions import SCHEMAS, register

MEASUREMENT_SCHEMA = 'https://ofarm.dev/schema/measurementevidence/v0.1'


def resolve_analysis_inputs(condition, atom, read, reject, need, after_specification):
    """Keep the actual two-read order and guards at the reader boundary.

    Read returns a selected source entry. The callbacks retain the evaluator's
    diagnostics and intervening specification comparisons without making them
    gates that the original reader did not have.
    """
    if condition['activityRow'] != 'O22' or condition['stage'] != 'FINISH' or condition['predicateKind'] != 'ANALYSIS_OUTPUT_RECORDED':
        reject('ANALYSIS_OUTPUT_CONDITION_KIND_MISMATCH', '/condition/predicateKind'); return None
    output = atom['body']['parameters']['producedResult']
    if output['role'] != 'ACTUAL_OUTPUT':
        reject('ANALYSIS_FINISH_REQUIRES_ACTUAL_OUTPUT', '/body/parameters/producedResult'); return None
    if atom['body']['workSpecification'].get('outputSpecification') is None:
        need('EXACT_ANALYSIS_OUTPUT_SPECIFICATION', '/body/workSpecification/outputSpecification'); return None
    specification = read(atom, '/body/workSpecification/outputSpecification',
        SCHEMAS['analysisOutput']['$id'], 'EXACT_ANALYSIS_OUTPUT_SPECIFICATION', 'definitionId', ())
    if specification is None: return None
    after_specification(specification)
    entry = read(atom, '/body/parameters/producedResult/binding', MEASUREMENT_SCHEMA,
        'EXACT_ACTUAL_ANALYSIS_OUTPUT', 'measurementEvidenceId', (specification['record'],))
    return None if entry is None else (specification, entry)


def evaluate(condition, atom, sources, schemas, *, work_specification_binding, procedure_binding):
    from time_validation import foreign_seconds
    register(schemas)
    errors, missing, refs, ids, comparisons = [], [], [], [], []
    retained = None
    body = atom['body']; parameters = body['parameters']; output = parameters['producedResult']
    def origin(entry, path): return {'inputRole': entry['id'], 'pointer': path}
    def claim(path): return {'inputRole': 'ATOM:' + atom['atomId'], 'pointer': path}
    def need(role, path): missing.append({'role': role, 'pointer': path})
    def compare(code, actual, expected, source, destination, equal=None):
        okay = same(actual, expected) if equal is None else equal
        comparisons.append({'predicateId': code, 'pointer': destination['pointer'], 'equal': okay,
            'source': {**source, 'valueDigest': digest(actual)}, 'destination': {**destination, 'valueDigest': digest(expected)},
            'disposition': 'PASS' if okay else 'FAIL'})
        if not okay: errors.append({'code': code, 'pointer': destination['pointer']})
    def finish():
        return {'scope': 'O22_REPORTED_OUTPUT_FIELDS_NOT_PHYSICAL_TRUTH_OR_ADMISSION',
            'disposition': 'FAIL' if errors else 'NOT_EVALUATED' if missing else 'PASS',
            'errors': errors, 'remainingRoles': missing, 'requiredReferences': refs,
            'sourceInputIds': sorted(set(ids)), 'comparisons': comparisons,
            'retainedSourceQualifications': retained}
    def resolve(binding, schema_id, role, path, identity):
        refs.append({'binding': binding, 'role': role, 'pointer': path})
        found = [v for v in sources if same(v['binding'], binding)]
        if len(found) != 1:
            need(role, path); return None
        entry = found[0]; ids.append(entry['id']); record = entry['record']
        shape = schemas.errors(schema_id, record); errors.extend(shape)
        if shape: return None
        compare('ANALYSIS_SOURCE_IDENTITY_MISMATCH', record[identity], binding['ref'],
            origin(entry, '/' + identity), claim(path + '/ref'))
        return entry if record[identity] == binding['ref'] else None
    def compare_specification(specification):
        definition = specification['record']
        for field, value, path in [
        ('workSpecificationBinding', work_specification_binding, '/body/workSpecification/binding'),
        ('procedureBinding', procedure_binding, '/body/workSpecification/procedure'),
        ('sampleBinding', parameters['sample'], '/body/parameters/sample'),
        ('propertyBinding', parameters['property'], '/body/parameters/property'),
        ('methodBinding', parameters['method'], '/body/parameters/method')]:
            compare('ANALYSIS_SPECIFICATION_' + field.upper() + '_MISMATCH', definition[field], value,
                origin(specification, '/' + field), claim(path))
        compare('ANALYSIS_OUTPUT_SPECIFICATION_SELECTION_MISMATCH', output['specificationBinding'], body['workSpecification']['outputSpecification'],
            claim('/body/parameters/producedResult/specificationBinding'), claim('/body/workSpecification/outputSpecification'))
    from strict_inputs import pointer
    resolved = resolve_analysis_inputs(condition, atom,
        lambda parent, path, schema, role, identity, prerequisites: resolve(pointer(parent, path), schema, role, path, identity),
        lambda code, path: errors.append({'code': code, 'pointer': path}), need, compare_specification)
    if resolved is None: return finish()
    specification, entry = resolved
    definition = specification['record']
    record = entry['record']
    # Retain every original qualification, including dispute/degradation. These
    # statuses are neither dropped nor interpreted as admission booleans.
    retained = {'inputId': entry['id'], 'originalRecordDigest': digest(record),
        'fields': [{'pointer': '/' + k, 'valueDigest': digest(v)} for k,v in record.items()
                   if k not in ['schemaVersion', 'measurementEvidenceId']]}
    for source_field, parameter in [('sampleRef', 'sample'), ('observedPropertyRef', 'property')]:
        if source_field not in record:
            need('ANALYSIS_OUTPUT_' + source_field.upper(), '/body/parameters/' + parameter)
        else:
            compare('ANALYSIS_OUTPUT_' + parameter.upper() + '_MISMATCH', record[source_field], parameters[parameter]['ref'],
                origin(entry, '/' + source_field), claim('/body/parameters/' + parameter + '/ref'))
    method = record.get('measurementMethod')
    if method is None:
        need('ANALYSIS_OUTPUT_METHOD_SOURCE', '/body/parameters/method')
    else:
        compare('ANALYSIS_OUTPUT_METHOD_MISMATCH', method['procedureRef'], parameters['method']['ref'],
            origin(entry, '/measurementMethod/procedureRef'), claim('/body/parameters/method/ref'))
        if method['procedureStatus'] == 'UNKNOWN_OR_MISSING':
            need('ANALYSIS_OUTPUT_METHOD_INTERPRETATION', '/body/parameters/method')
        if 'methodVersionRef' in definition and 'versionRef' in method:
            compare('ANALYSIS_OUTPUT_METHOD_REVISION_MISMATCH', method['versionRef'], definition['methodVersionRef'],
                origin(entry, '/measurementMethod/versionRef'), origin(specification, '/methodVersionRef'))
        else:
            need('ANALYSIS_OUTPUT_EXACT_METHOD_VERSION', '/body/parameters/method')
    kind = record['result']['resultKind']
    compare('ANALYSIS_OUTPUT_RESULT_KIND_NOT_PERMITTED', kind, definition['permittedResultKinds'],
        origin(entry, '/result/resultKind'), origin(specification, '/permittedResultKinds'), kind in definition['permittedResultKinds'])
    if kind == 'ABSENT_PENDING' or 'RESULT_PENDING' in record.get('degradationReasons', []):
        errors.append({'code': 'PENDING_ANALYSIS_OUTPUT_CANNOT_ESTABLISH_FINISH', 'pointer': '/body/parameters/producedResult'})
    if kind == 'QUALITATIVE' and not record['result']['qualitativeValue'].strip():
        errors.append({'code': 'EMPTY_ANALYSIS_OUTPUT_CANNOT_ESTABLISH_FINISH', 'pointer': '/body/parameters/producedResult'})
    if kind in ['NUMERIC', 'CENSORED_NUMERIC']:
        if definition['quantityContext'] is None:
            need('ANALYSIS_OUTPUT_QUANTITY_CONTEXT_DEFINITION', '/body/workSpecification/outputSpecification')
        else:
            for field, key in [('quantityKindRef', 'quantityKind'), ('unitRef', 'unit')]:
                compare('ANALYSIS_OUTPUT_' + key.upper() + '_MISMATCH', record['result'][field], definition['quantityContext'][key],
                    origin(entry, '/result/' + field), origin(specification, '/quantityContext/' + key))
                if kind == 'CENSORED_NUMERIC':
                    compare('ANALYSIS_OUTPUT_LIMIT_' + key.upper() + '_MISMATCH', record['result']['detectionLimit'][field], definition['quantityContext'][key],
                        origin(entry, '/result/detectionLimit/' + field), origin(specification, '/quantityContext/' + key))
    time = atom['scope']['subjectTime']
    try:
        at = foreign_seconds(record['resultTime']); start = foreign_seconds(time.get('at', time.get('start')))
        end = foreign_seconds(time['end']) if 'end' in time else start if 'at' in time else None
        compare('ANALYSIS_OUTPUT_RESULT_TIME_OUTSIDE_WORK', record['resultTime'], time,
            origin(entry, '/resultTime'), claim('/scope/subjectTime'), end is not None and start <= at <= end)
    except (ValueError, TypeError):
        need('ANALYSIS_OUTPUT_RESULT_TIME_INTERPRETATION', '/body/parameters/producedResult')
    return finish()
