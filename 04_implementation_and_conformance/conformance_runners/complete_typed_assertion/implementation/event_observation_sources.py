"""Exact selected count measurement for the canonical stand-count event case."""
from strict_inputs import same, digest
from event_relation_sources import mandatory_positive


from domain_reader_occurrences import reader, selection as observe_selection, guard as observe_guard, origin as read_origin, observed_shape, observe_comparisons


@reader('event_observation_sources.py', ['AR_EVENT_ASSOCIATION'])
def evaluate(intent, envelope, atoms, automatic, sources, selection, concept_origin):
    from time_validation import foreign_seconds
    errors, missing, comparisons, ids, refs, candidates = [], [], [], [], [], []
    matched=set();checked={a['atomId']:a for a in automatic.get('atoms',[])}
    def compare(code, left, right, source, destination, okay=None):
        equal=same(left,right) if okay is None else okay
        comparisons.append({'predicateId':code,'equal':equal,'pointer':source['pointer'],
            'source':{**source,'valueDigest':digest(left)},'destination':{**destination,'valueDigest':digest(right)},
            'disposition':'PASS' if equal else 'FAIL'})
        observe_comparisons([comparisons[-1]])
        if not equal:errors.append({'code':code,'pointer':source['pointer']})
    def finish():
        return {'canonicalRow':'V04-stand-count','disposition':'FAIL' if errors else 'NOT_EVALUATED',
            'errors':errors,'remainingRoles':missing,'comparisons':comparisons,'sourceInputIds':sorted(set(ids)),
            'requiredReferences':refs,'candidates':candidates,'matchedAtomIds':sorted(matched),
            'mandatoryPositiveMeasurementEstablished':mandatory_positive(intent['assertionBody']['proposition'],matched),
            'qualification':'Selected normative count meaning and original event/measurement links only; source version use, factual correctness and admission remain separate.'}
    selected=selection.get('selectedObservationMeasurement')
    if selected is None:
        missing.append({'role':'EXACT_EVENT_OBSERVATION_MEASUREMENT_SELECTION','pointer':'/eventDefinition'})
        return finish()
    refs.append({'role':'EXACT_EVENT_OBSERVATION_MEASUREMENT','binding':selected['binding'],**selected['origin']})
    ids.append(selected['origin']['inputRole'])
    for atom in atoms:
        finding=checked.get(atom['atomId'],{});meaning=finding.get('sourceInterpretation',{}).get('selectedObservationMeaning')
        if meaning is None:continue
        begin=len(errors);path=finding['pointer'];binding=meaning['measurementBinding']
        source=[v for v in sources if same(v['binding'],binding)]
        observe_selection('EVENT_OBSERVATION_MEASUREMENT', sources, source, binding=binding,
            origins=[read_origin('EFFECT_INTENT', path + '/body/operand/source/measurementBinding'), selected['origin']])
        if len(source)!=1:
            missing.append({'role':'EXACT_ORIGINAL_STAND_COUNT_MEASUREMENT','pointer':path+'/body/operand/source/measurementBinding'})
            continue
        entry=source[0];record=entry['record'];ids.extend([entry['id'],meaning['conceptOrigin']['inputRole']])
        compare('EVENT_STAND_COUNT_CONCEPT_MISMATCH',meaning['concept'],'STAND_COUNT_OBSERVATION',meaning['conceptOrigin'],concept_origin)
        compare('EVENT_STAND_COUNT_MEASUREMENT_SELECTION_MISMATCH',selected['binding'],binding,selected['origin'],
                {'inputRole':'EFFECT_INTENT','pointer':path+'/body/operand/source/measurementBinding'})
        # The interpretation and association must consume the same original,
        # even if an equal JSON value has another raw-byte representation.
        if entry['rawSha256']!=meaning['measurementRawSha256'] or entry['valueDigest']!=meaning['measurementValueDigest']:
            errors.append({'code':'EVENT_STAND_COUNT_ORIGINAL_MEASUREMENT_MISMATCH','pointer':path})
        indices=[n for n,ref in enumerate(envelope.get('evidenceRefs',[])) if ref==record['measurementEvidenceId']]
        if not indices:
            errors.append({'code':'EVENT_STAND_COUNT_MEASUREMENT_NOT_IN_EVIDENCE','pointer':'/event/evidenceRefs'})
        else:
            compare('EVENT_STAND_COUNT_MEASUREMENT_NOT_IN_EVIDENCE',envelope['evidenceRefs'][indices[0]],record['measurementEvidenceId'],
                {'inputRole':'event:envelope','pointer':'/evidenceRefs/'+str(indices[0])},
                {'inputRole':entry['id'],'pointer':'/measurementEvidenceId'})
        phenomenon=record['phenomenonTime'];known_time=False
        if phenomenon['timeType']!='INSTANT' or 'instant' not in phenomenon or 'observationTime' not in envelope['timeSemantics']:
            missing.append({'role':'EXACT_EVENT_OBSERVATION_PHENOMENON_INSTANT','pointer':path+'/body/operand/source/measurementBinding'})
        else:
            try:
                equal=foreign_seconds(phenomenon['instant'])==foreign_seconds(envelope['timeSemantics']['observationTime'])
                compare('EVENT_STAND_COUNT_PHENOMENON_TIME_MISMATCH',phenomenon['instant'],envelope['timeSemantics']['observationTime'],
                    {'inputRole':entry['id'],'pointer':'/phenomenonTime/instant'},
                    {'inputRole':'event:envelope','pointer':'/timeSemantics/observationTime'},equal)
                known_time=True
            except (ValueError,TypeError):
                missing.append({'role':'EXACT_EVENT_OBSERVATION_TIME_INTERPRETATION','pointer':path+'/body/operand/source/measurementBinding'})
        okay=len(errors)==begin and known_time and not finding.get('errors')
        candidates.append({'atomId':atom['atomId'],'measurementBinding':binding,'measurementRawSha256':entry['rawSha256'],
            'evidenceIndices':indices,'matchesSelectedObservation':okay})
        if okay:matched.add(atom['atomId'])
        missing.append({'role':'EVENT_OBSERVATION_SOURCE_VERSION_AND_ELIGIBLE_USE','pointer':path+'/body/operand/source/measurementBinding'})
    if not candidates:
        missing.append({'role':'EXACT_EVENT_CONDITION_OR_DECISION_CONCEPT:STAND_COUNT_OBSERVATION','pointer':'/assertionBody/proposition'})
    elif not mandatory_positive(intent['assertionBody']['proposition'],matched):
        errors.append({'code':'EVENT_STAND_COUNT_MANDATORY_POSITIVE_MEASUREMENT_NOT_ESTABLISHED','pointer':'/assertionBody/proposition'})
    return finish()
