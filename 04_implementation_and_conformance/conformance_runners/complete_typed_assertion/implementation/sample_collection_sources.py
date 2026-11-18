"""O10 exact collection-record, specimen, protocol and support comparisons.

A separate observed finish property is still required by condition_sources.
ABSENT_PENDING is a retained analytical state, never completion evidence.
"""
from strict_inputs import same, digest
from sample_collection_definitions import SCHEMAS, register

MEASUREMENT = 'https://ofarm.dev/schema/measurementevidence/v0.1'
CONTEXT = 'https://ofarm.dev/schema/agronomicobservationcontext/v0.1'


def resolve_collection_inputs(atom, read, need, after_specification):
    """Read specification, collection record and context in the actual order."""
    if atom['body']['workSpecification'].get('outputSpecification') is None:
        need('EXACT_SAMPLE_COLLECTION_SPECIFICATION', '/body/workSpecification/outputSpecification'); return None
    spec = read(atom, '/body/workSpecification/outputSpecification', SCHEMAS['sampleCollection']['$id'],
        'EXACT_SAMPLE_COLLECTION_SPECIFICATION', 'definitionId', ())
    if spec is None: return None
    after_specification(spec)
    entry = read(spec['record'], '/collectionMeasurementBinding', MEASUREMENT,
        'EXACT_SAMPLE_COLLECTION_RECORD', 'measurementEvidenceId', (spec['record'],))
    context = read(spec['record'], '/collectionContextBinding', CONTEXT,
        'EXACT_SAMPLE_COLLECTION_SUPPORT_CONTEXT', 'agronomicObservationContextId', (spec['record'],))
    return None if entry is None or context is None else (spec, entry, context)


def resolve_collection_analysis(atom, entry, context, read):
    """Read a declared analytical result only after both collection inputs."""
    if atom['body']['parameters']['analyticalResult']['kind'] == 'ABSENT_PENDING': return None
    return read(atom, '/body/parameters/analyticalResult/binding', MEASUREMENT,
        'EXACT_SAMPLE_ANALYTICAL_RESULT', 'measurementEvidenceId', (entry['record'], context['record']))


def evaluate(atom, condition, observation, sources, schemas):
    from time_validation import foreign_seconds
    from strict_inputs import pointer
    register(schemas)
    errors, missing, refs, ids, comparisons, retained = [], [], [], [], [], []
    body = atom['body']; parameters = body['parameters']; work = body['workSpecification']
    def origin(entry, path): return {'inputRole': entry['id'], 'pointer': path}
    def claim(path): return {'inputRole': 'ATOM:' + atom['atomId'], 'pointer': path}
    def need(role, path): missing.append({'role': role, 'pointer': path})
    def compare(code, actual, expected, left, right, equal=None):
        equal = same(actual, expected) if equal is None else equal
        comparisons.append({'predicateId': code, 'pointer': right['pointer'], 'equal': equal,
            'source': {**left, 'valueDigest': digest(actual)}, 'destination': {**right, 'valueDigest': digest(expected)},
            'disposition': 'PASS' if equal else 'FAIL'})
        if not equal: errors.append({'code': code, 'pointer': right['pointer']})
    def result():
        return {'disposition': 'FAIL' if errors else 'NOT_EVALUATED' if missing else 'PASS',
            'errors': errors, 'remainingRoles': missing, 'requiredReferences': refs,
            'sourceInputIds': sorted(set(ids)), 'comparisons': comparisons,
            'retainedSourceQualifications': {'scope': 'ORIGINAL_COLLECTION_AND_SUPPORT_NOT_ANALYTICAL_TRUTH_OR_ADMISSION', 'records': retained}}
    def resolve(binding, schema_id, role, selected_origin, identity):
        refs.append({'binding': binding, 'role': role, 'pointer': selected_origin['pointer']})
        found = [v for v in sources if same(v['binding'], binding)]
        if len(found) != 1:
            need(role, selected_origin['pointer']); return None
        entry = found[0]; ids.append(entry['id']); record = entry['record']
        shape = schemas.errors(schema_id, record); errors.extend(shape)
        if shape: return None
        compare('SAMPLE_COLLECTION_SOURCE_IDENTITY_MISMATCH', record[identity], binding['ref'],
            origin(entry, '/' + identity), {**selected_origin, 'pointer': selected_origin['pointer'] + '/ref'})
        if record[identity] != binding['ref']: return None
        return entry
    def compare_specification(spec):
        definition = spec['record']
        for key, value, path in [
        ('workSpecificationBinding', work['binding'], '/body/workSpecification/binding'),
        ('procedureBinding', work['procedure'], '/body/workSpecification/procedure'),
        ('sampleBinding', parameters['sample'], '/body/parameters/sample'),
        ('sampledPropertyBinding', parameters['sampledProperty'], '/body/parameters/sampledProperty'),
        ('samplingProcedureBinding', parameters['samplingProcedure'], '/body/parameters/samplingProcedure')]:
            compare('SAMPLE_COLLECTION_SPECIFICATION_' + key.upper() + '_MISMATCH', definition[key], value,
                origin(spec, '/' + key), claim(path))
    entries = {}
    def read_input(parent, path, schema, role, identity, prerequisites):
        selected_origin = claim(path) if parent is atom else origin(entries[id(parent)], path)
        entry = resolve(pointer(parent, path), schema, role, selected_origin, identity)
        if entry is not None: entries[id(entry['record'])] = entry
        return entry
    resolved = resolve_collection_inputs(atom, read_input, need, compare_specification)
    if resolved is None: return result()
    spec, entry, context_entry = resolved
    definition = spec['record']
    record = entry['record']; context = context_entry['record']
    for source in [entry, context_entry]:
        retained.append({'inputId': source['id'], 'originalRecordDigest': digest(source['record']),
            'fields': [{'pointer': '/' + key, 'valueDigest': digest(value)} for key,value in source['record'].items()]})
    if record['evidenceClass'] != 'SAMPLE_COLLECTION':
        errors.append({'code': 'SAMPLE_COLLECTION_RECORD_CLASS_MISMATCH', 'pointer': '/collection/evidenceClass'})
    for source_key, parameter in [('sampleRef', 'sample'), ('observedPropertyRef', 'sampledProperty')]:
        if source_key not in record: need('SAMPLE_COLLECTION_' + source_key.upper(), '/collection/' + source_key)
        else: compare('SAMPLE_COLLECTION_' + parameter.upper() + '_MISMATCH', record[source_key], parameters[parameter]['ref'],
            origin(entry, '/' + source_key), claim('/body/parameters/' + parameter + '/ref'))
    protocol = record.get('samplingProtocol')
    if protocol is None:
        need('SAMPLE_COLLECTION_ORIGINAL_PROTOCOL', '/collection/samplingProtocol')
    else:
        compare('SAMPLE_COLLECTION_PROTOCOL_MISMATCH', protocol['procedureRef'], parameters['samplingProcedure']['ref'],
            origin(entry, '/samplingProtocol/procedureRef'), claim('/body/parameters/samplingProcedure/ref'))
        if protocol['procedureStatus'] == 'UNKNOWN_OR_MISSING': need('SAMPLE_COLLECTION_PROTOCOL_INTERPRETATION', '/collection/samplingProtocol')
        if 'versionRef' not in protocol: need('SAMPLE_COLLECTION_PROTOCOL_VERSION', '/collection/samplingProtocol/versionRef')
        else: compare('SAMPLE_COLLECTION_PROTOCOL_VERSION_MISMATCH', protocol['versionRef'], definition['samplingProcedureVersionRef'],
            origin(entry, '/samplingProtocol/versionRef'), origin(spec, '/samplingProcedureVersionRef'))
    # Preserve qualifications. Only the explicitly defined corresponding labels
    # have a comparison; BROKEN does not silently mean disputed and NOT_REQUIRED
    # does not mean complete.
    custody = record.get('chainOfCustodyStatus')
    mapped = {'PRESERVED': 'COMPLETE', 'PARTIAL': 'PARTIAL', 'UNKNOWN': 'UNKNOWN'}.get(custody)
    if mapped is None: need('SAMPLE_COLLECTION_CUSTODY_POSTURE_INTERPRETATION', '/collection/chainOfCustodyStatus')
    else: compare('SAMPLE_COLLECTION_CUSTODY_POSTURE_MISMATCH', custody, parameters['custodyPosture'],
        origin(entry, '/chainOfCustodyStatus'), claim('/body/parameters/custodyPosture'), mapped == parameters['custodyPosture'])
    compare('SAMPLE_COLLECTION_EVIDENCE_POSTURE_MISMATCH', record['evidenceStatus'], parameters['evidencePosture'],
        origin(entry, '/evidenceStatus'), claim('/body/parameters/evidencePosture'))
    if parameters['analyticalResult']['kind'] == 'ABSENT_PENDING':
        compare('SAMPLE_COLLECTION_PENDING_ANALYSIS_MISMATCH', record['result']['resultKind'], 'ABSENT_PENDING',
            origin(entry, '/result/resultKind'), claim('/body/parameters/analyticalResult/kind'))
    else:
        analytic = resolve_collection_analysis(atom, entry, context_entry, read_input)
        if analytic is not None:
            ar = analytic['record']
            retained.append({'inputId': analytic['id'], 'originalRecordDigest': digest(ar),
                'fields': [{'pointer': '/' + key, 'valueDigest': digest(value)} for key,value in ar.items()]})
            if ar['result']['resultKind'] == 'ABSENT_PENDING': errors.append({'code': 'BOUND_SAMPLE_ANALYSIS_STILL_PENDING', 'pointer': '/analysis/result'})
            for key, parameter in [('sampleRef', 'sample'), ('observedPropertyRef', 'sampledProperty')]:
                if key not in ar: need('SAMPLE_ANALYSIS_' + key.upper(), '/analysis/' + key)
                else: compare('SAMPLE_ANALYSIS_' + parameter.upper() + '_MISMATCH', ar[key], parameters[parameter]['ref'],
                    origin(analytic, '/' + key), claim('/body/parameters/' + parameter + '/ref'))
    if context['subject']['subjectType'] != 'SAMPLE': errors.append({'code': 'SAMPLE_COLLECTION_CONTEXT_SUBJECT_KIND_MISMATCH', 'pointer': '/collectionContext/subject'})
    compare('SAMPLE_COLLECTION_CONTEXT_SPECIMEN_MISMATCH', context['subject']['subjectRef'], parameters['sample']['ref'],
        origin(context_entry, '/subject/subjectRef'), claim('/body/parameters/sample/ref'))
    compare('SAMPLE_COLLECTION_CONTEXT_PROPERTY_MISMATCH', context['observedPropertyRef'], parameters['sampledProperty']['ref'],
        origin(context_entry, '/observedPropertyRef'), claim('/body/parameters/sampledProperty/ref'))
    for path in ['/targetScope', '/spatialContext/scope']:
        scoped = context.get('targetScope') if path == '/targetScope' else context['spatialContext']['scope']
        if scoped is None: need('SAMPLE_COLLECTION_TARGET_SCOPE', '/collectionContext' + path); continue
        for key, target_key in [('scopeType', 'kind'), ('scopeRef', 'binding')]:
            expected = body['target']['kind'] if key == 'scopeType' else body['target']['binding']['ref']
            compare('SAMPLE_COLLECTION_SUPPORT_TARGET_MISMATCH', scoped[key], expected,
                origin(context_entry, path + '/' + key), claim('/body/target/' + target_key + ('/ref' if key == 'scopeRef' else '')))
    spatial = context['spatialContext']; extent = body['extent']
    if extent['posture'] == 'PARTIAL_TARGET_SCOPE':
        if 'partialExtentRef' not in spatial: need('SAMPLE_COLLECTION_PARTIAL_SUPPORT', '/collectionContext/spatialContext')
        else: compare('SAMPLE_COLLECTION_SUPPORT_EXTENT_MISMATCH', spatial['partialExtentRef'], extent['binding']['ref'],
            origin(context_entry, '/spatialContext/partialExtentRef'), claim('/body/extent/binding/ref'))
        if spatial['spatialBasis'] in ['WHOLE_SCOPE', 'UNKNOWN']:
            errors.append({'code': 'SAMPLE_COLLECTION_PARTIAL_SUPPORT_BASIS_MISMATCH', 'pointer': '/collectionContext/spatialContext'})
    elif 'partialExtentRef' in spatial or spatial['spatialBasis'] != 'WHOLE_SCOPE':
        errors.append({'code': 'SAMPLE_COLLECTION_PARTIAL_SUPPORT_FOR_WHOLE_CLAIM', 'pointer': '/collectionContext/spatialContext'})
    cp = context['procedure']
    if cp['procedureStatus'] == 'UNKNOWN_OR_MISSING': need('SAMPLE_COLLECTION_CONTEXT_PROTOCOL_INTERPRETATION', '/collectionContext/procedure')
    for key in ['procedureRef', 'samplingProtocolRef']:
        if key not in cp: need('SAMPLE_COLLECTION_CONTEXT_' + key.upper(), '/collectionContext/procedure/' + key)
        else: compare('SAMPLE_COLLECTION_CONTEXT_PROTOCOL_MISMATCH', cp[key], parameters['samplingProcedure']['ref'],
            origin(context_entry, '/procedure/' + key), claim('/body/parameters/samplingProcedure/ref'))
    compare('SAMPLE_COLLECTION_CONTEXT_EVIDENCE_LINK_MISSING', context['evidenceRefs'], record['measurementEvidenceId'],
        origin(context_entry, '/evidenceRefs'), origin(entry, '/measurementEvidenceId'), record['measurementEvidenceId'] in context['evidenceRefs'])
    observation_entry = next((v for v in sources if same(v['binding'], condition['measurementBinding'])), None)
    if observation_entry is not None:
        compare('SAMPLE_COLLECTION_COMPLETION_OBSERVATION_LINK_MISSING', observation['provenanceRefs'], record['measurementEvidenceId'],
            origin(observation_entry, '/provenanceRefs'), origin(entry, '/measurementEvidenceId'), record['measurementEvidenceId'] in observation['provenanceRefs'])
        if 'sampleRef' not in observation: need('SAMPLE_COLLECTION_COMPLETION_SPECIMEN', '/completion/sampleRef')
        else: compare('SAMPLE_COLLECTION_COMPLETION_SPECIMEN_MISMATCH', observation['sampleRef'], parameters['sample']['ref'],
            origin(observation_entry, '/sampleRef'), claim('/body/parameters/sample/ref'))
    time = record.get('phenomenonTime'); work_time = atom['scope']['subjectTime']
    if time is None: need('SAMPLE_COLLECTION_ORIGINAL_PHENOMENON_TIME', '/collection/phenomenonTime')
    else:
        compare('SAMPLE_COLLECTION_CONTEXT_TIME_MISMATCH', context['phenomenonTime'], time,
            origin(context_entry, '/phenomenonTime'), origin(entry, '/phenomenonTime'))
        try:
            start = foreign_seconds(work_time.get('start', work_time.get('at')))
            end = foreign_seconds(work_time['end']) if 'end' in work_time else start if 'at' in work_time else None
            first = foreign_seconds(time.get('instant', time.get('intervalStart')))
            last = foreign_seconds(time['intervalEnd']) if 'intervalEnd' in time else first if time['timeType'] in ['INSTANT', 'AS_OF'] else None
            produced = foreign_seconds(record['resultTime'])
            compare('SAMPLE_COLLECTION_TIME_OUTSIDE_WORK', time, work_time, origin(entry, '/phenomenonTime'), claim('/scope/subjectTime'),
                last is not None and end is not None and start <= first <= last <= end)
            compare('SAMPLE_COLLECTION_RECORDING_TIME_OUTSIDE_WORK', record['resultTime'], work_time,
                origin(entry, '/resultTime'), claim('/scope/subjectTime'), last is not None and end is not None and start <= last <= produced <= end)
        except (ValueError, TypeError, KeyError): need('SAMPLE_COLLECTION_TIME_INTERPRETATION', '/collection/phenomenonTime')
    return result()
