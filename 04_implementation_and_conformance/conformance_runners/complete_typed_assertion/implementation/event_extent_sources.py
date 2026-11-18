"""Bounded event partial-extent -> declared parent comparisons.

Only the atom's exact partial extent, explicitly selected as a relation input,
is considered. Geometry overlap, same-farm membership and label matching never
create an edge. All original extent qualifications remain controlling.
"""
from strict_inputs import same, digest
from event_relation_sources import mandatory_positive


from domain_reader_occurrences import reader, selection as observe_selection, guard as observe_guard, origin as read_origin, observed_shape, observe_comparisons


@reader('event_extent_sources.py', ['AR_EVENT_ASSOCIATION'])
def evaluate(intent, envelope, atoms, automatic, sources, schemas, definition, *, temporal_meanings=()):
    from extent_temporal import evaluate as extent_time
    errors, missing, comparisons, ids, refs, candidates = [], [], [], [], [], []
    checked = {v['atomId']: v for v in automatic['atoms']}; matched = set()

    def compare(code, a, b, source, destination):
        equal = same(a, b)
        comparisons.append({'predicateId': code, 'equal': equal, 'pointer': source['pointer'],
            'source': {**source, 'valueDigest': digest(a)}, 'destination': {**destination, 'valueDigest': digest(b)},
            'disposition': 'PASS' if equal else 'FAIL'})
        observe_comparisons([comparisons[-1]])
        if not equal:
            errors.append({'code': code, 'pointer': source['pointer']})

    for atom in atoms:
        finding = checked.get(atom['atomId'], {}); path = finding.get('pointer')
        extent = atom['scope']['extent']
        if extent['posture'] != 'PARTIAL_TARGET_SCOPE' or path is None:
            continue
        binding = extent['binding']; proof_indices = [n for n, b in enumerate(intent['subjectScopeProofBindings']) if same(b, binding)]
        if not proof_indices:
            missing.append({'role': 'EXACT_SELECTED_EVENT_EXTENT_RELATION_BINDING', 'pointer': path + '/scope/extent/binding'})
            continue
        proof_pointer = '/subjectScopeProofBindings/' + str(proof_indices[0])
        refs.append({'role': 'EVENT_EXTENT_ORIGINAL_RELATION_CARRIER', 'binding': binding, 'pointer': proof_pointer})
        entries = [v for v in sources if same(v['binding'], binding)]
        observe_selection('EVENT_PARTIAL_EXTENT', sources, entries, binding=binding,
            origins=[read_origin('ATOM:' + atom['atomId'], '/scope/extent/binding')])
        if len(entries) != 1:
            missing.append({'role': 'EXACT_EVENT_EXTENT_ORIGINAL', 'pointer': proof_pointer})
            continue
        entry = entries[0]; record = entry['record']; ids.append(entry['id'])
        shape = observed_shape(schemas, 'https://ofarm.dev/schema/partialextent/v0.1', record); errors.extend(shape)
        if shape:
            continue
        start_error = len(errors)
        def src(p): return {'inputRole': entry['id'], 'pointer': p}
        def claim(p): return {'inputRole': 'EFFECT_INTENT', 'pointer': p}
        compare('EVENT_EXTENT_IDENTITY_MISMATCH', record['partialExtentId'], binding['ref'],
                src('/partialExtentId'), claim(path + '/scope/extent/binding/ref'))
        event_indices = [n for n, ref in enumerate(envelope['subjectRefs']) if ref == binding['ref']]
        evidence_indices = [n for n, ref in enumerate(envelope.get('evidenceRefs', [])) if ref == binding['ref']]
        for indices, field, code in [(event_indices, 'subjectRefs', 'EVENT_EXTENT_NOT_IN_EVENT_SUBJECTS'),
                                      (evidence_indices, 'evidenceRefs', 'EVENT_EXTENT_NOT_IN_EVENT_EVIDENCE')]:
            if not indices:
                errors.append({'code': code, 'pointer': '/event/' + field})
            else:
                compare(code, envelope[field][indices[0]], record['partialExtentId'],
                        {'inputRole': 'event:envelope', 'pointer': '/' + field + '/' + str(indices[0])}, src('/partialExtentId'))
        for parent_key, subject_key in [('scopeType', 'subjectType'), ('scopeRef', 'subjectRef')]:
            compare('EVENT_EXTENT_PARENT_' + parent_key.upper() + '_MISMATCH', record['parentScope'][parent_key], intent['subject'][subject_key],
                    src('/parentScope/' + parent_key), claim('/subject/' + subject_key))
            compare('EVENT_EXTENT_ATOM_SUBJECT_' + subject_key.upper() + '_MISMATCH', atom['scope']['subject'][subject_key], intent['subject'][subject_key],
                    claim(path + '/scope/subject/' + subject_key), claim('/subject/' + subject_key))
        if not same(atom['scope']['subject'], intent['subject']):
            errors.append({'code': 'EVENT_EXTENT_TARGET_SUBJECT_SELECTOR_MISMATCH', 'pointer': path + '/scope/subject'})
        for key in ['revisionRef', 'digest']:
            if key in atom['scope']['subject'] and key in intent['subject']:
                compare('EVENT_EXTENT_TARGET_' + key.upper() + '_MISMATCH', atom['scope']['subject'][key], intent['subject'][key],
                        claim(path + '/scope/subject/' + key), claim('/subject/' + key))
        for key in ['scopeType', 'scopeRef']:
            compare('EVENT_EXTENT_ANCHOR_' + key.upper() + '_MISMATCH', record['anchorScope'][key], intent['resources'][0]['scope'][key],
                    src('/anchorScope/' + key), claim('/resources/0/scope/' + key))
        original = record['temporalApplicability']; time = atom['scope']['subjectTime']
        selected_meanings=[v for v in temporal_meanings if same(v['meaning']['extentBinding'],binding)]
        meaning=None
        if len(selected_meanings)>1:
            errors.append({'code':'AMBIGUOUS_EVENT_EXTENT_TIME_MEANING','pointer':proof_pointer})
        elif selected_meanings:
            selected_meaning=selected_meanings[0];meaning=selected_meaning['meaning'];origin=selected_meaning['origin'];ids.append(origin['inputRole'])
            for key,expected,destination in [
                ('extentBinding',binding,claim(path+'/scope/extent/binding')),
                ('sourceTimeType',original['timeType'],src('/temporalApplicability/timeType')),
                ('timeBasis',original['timeBasis'],src('/temporalApplicability/timeBasis'))]:
                compare('EVENT_EXTENT_MEANING_'+key.upper()+'_MISMATCH',meaning[key],expected,
                    {'inputRole':origin['inputRole'],'pointer':origin['pointer']+'/'+key},destination)
        checked_time=extent_time(original,time,meaning)
        errors.extend({'code':'EVENT_EXTENT_'+v['code'],'pointer':v['pointer']} for v in checked_time['errors'])
        missing.extend({'role':'EVENT_EXTENT_'+role,'pointer':'/temporalApplicability'} for role in checked_time['remainingRoles'])
        covered=checked_time['coverage']
        if covered is not None:
            comparisons.append({'predicateId': 'EVENT_EXTENT_APPLICABILITY_COVERS_CLAIM',
                'source': {**src('/temporalApplicability'), 'valueDigest': digest(original)},
                'destination': {**claim(path + '/scope/subjectTime'), 'valueDigest': digest(time)},
                'disposition': 'PASS' if covered else 'FAIL'})
            observe_comparisons([comparisons[-1]])
            if not covered:
                errors.append({'code': 'EVENT_EXTENT_APPLICABILITY_DOES_NOT_COVER_CLAIM', 'pointer': '/temporalApplicability'})
        okay = len(errors) == start_error and not finding.get('errors') and covered is True
        qualifications = {k: record[k] for k in record if k not in ['schemaVersion', 'partialExtentId', 'parentScope', 'anchorScope']}
        candidates.append({'atomId': atom['atomId'], 'extentBinding': binding, 'sourceInputId': entry['id'],
            'parentSubject': intent['subject'], 'eventSubjectIndices': event_indices, 'eventEvidenceIndices': evidence_indices,
            'sourceQualifications': qualifications, 'originalRecordDigest': digest(record), 'matchedOriginalFields': okay})
        if okay:
            matched.add(atom['atomId'])
        missing.extend({'role': role, 'pointer': proof_pointer} for role in [
            'EVENT_EXTENT_ENDPOINT_VERSION_AND_KIND_USE', 'EVENT_EXTENT_PROVENANCE_PURPOSE_AND_ELIGIBLE_USE'])
    established = bool(candidates) and mandatory_positive(intent['assertionBody']['proposition'], matched)
    if candidates and not established:
        errors.append({'code': 'EVENT_EXTENT_MANDATORY_POSITIVE_RELATION_NOT_ESTABLISHED', 'pointer': '/assertionBody/proposition'})
    return {'canonicalRow': 'V06-extent', 'caseDefinitionBinding': definition['binding'],
        'scope': 'CONDITIONAL_ORIGINAL_PARTIAL_EXTENT_TO_PARENT_FIELDS_ONLY',
        'disposition': 'FAIL' if errors else 'NOT_EVALUATED', 'errors': errors, 'remainingRoles': missing,
        'comparisons': comparisons, 'sourceInputIds': sorted(set(ids)), 'requiredReferences': refs,
        'candidates': candidates, 'matchedAtomIds': sorted(matched), 'mandatoryOriginalRelationEstablished': established,
        'qualification': 'No whole-target support, geometric containment, activity performance, accepted relation, endpoint currentness or authority follows from this edge.'}
