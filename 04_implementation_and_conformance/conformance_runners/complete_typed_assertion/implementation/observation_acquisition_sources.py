"""O09 finish from every explicitly required original observation and context.

The independently selected normative work condition fixes the required set.
Neither execution existence, result summaries, nor a passing generic criterion
substitutes for these originals. Their measured truth and eligible use remain
separate domain/owner obligations.
"""
from strict_inputs import same,digest
from observation_acquisition_definitions import SCHEMAS,register


def resolve_acquisition_inputs(condition, condition_entry, read, reject, need, after_specification):
    """Read the acquisition specification and context with the actual guards."""
    if condition['predicateKind'] != 'REQUIRED_OBSERVATIONS_ACQUIRED_AND_RECORDED':
        reject('OBSERVATION_ACQUISITION_CONDITION_KIND_MISMATCH', '/condition/predicateKind'); return None
    if condition.get('acquisitionSpecificationBinding') is None or condition_entry is None:
        need('EXACT_OBSERVATION_ACQUISITION_SPECIFICATION', '/condition/acquisitionSpecificationBinding'); return None
    spec = read(condition, '/acquisitionSpecificationBinding', SCHEMAS['observationAcquisition']['$id'],
        'EXACT_OBSERVATION_ACQUISITION_SPECIFICATION', 'definitionId', ())
    if spec is None: return None
    after_specification(spec)
    context = read(spec['record'], '/observationContextBinding',
        'https://ofarm.dev/schema/agronomicobservationcontext/v0.1',
        'EXACT_ACQUISITION_CONTEXT', 'agronomicObservationContextId', (spec['record'],))
    return None if context is None else (spec, context)


def resolve_acquisition_extent(atom, context, read):
    """Read the claim's partial extent after context selection, not its meaning."""
    if atom['body']['extent']['posture'] == 'FULL_TARGET_SCOPE':
        return None
    return read(atom, '/body/extent/binding',
        'https://ofarm.dev/schema/partialextent/v0.1',
        'EXACT_ACQUISITION_PARTIAL_EXTENT', 'partialExtentId', (context['record'],))


def acquisition_observation_inputs(spec, context, read):
    """Yield one required slot at a time so evaluation stays interleaved."""
    for index, required in enumerate(spec['record']['requiredObservations']):
        entry = read(spec['record'], '/requiredObservations/' + str(index) + '/measurementBinding',
            'https://ofarm.dev/schema/measurementevidence/v0.1',
            'REQUIRED_ORIGINAL_OBSERVATION:' + required['slotId'],
            'measurementEvidenceId', (context['record'],))
        yield index, required, entry


def evaluate(condition,atom,sources,schemas,*,condition_binding):
    from time_validation import foreign_instant, foreign_seconds
    from extent_temporal import evaluate as extent_time
    from strict_inputs import pointer
    register(schemas)
    errors,missing,refs,ids,comparisons,retained=[],[],[],[],[],[]
    body=atom['body'];parameters=body['parameters'];work=body['workSpecification']
    def origin(entry,path):return {'inputRole':entry['id'],'pointer':path}
    def claim(path):return {'inputRole':'ATOM:'+atom['atomId'],'pointer':path}
    def need(role,path):missing.append({'role':role,'pointer':path})
    def compare(code,actual,expected,left,right,equal=None):
        equal=same(actual,expected) if equal is None else equal
        comparisons.append({'predicateId':code,'pointer':right['pointer'],'equal':equal,
            'source':{**left,'valueDigest':digest(actual)},'destination':{**right,'valueDigest':digest(expected)},'disposition':'PASS' if equal else 'FAIL'})
        if not equal:errors.append({'code':code,'pointer':right['pointer']})
    def result():return {'scope':'REQUIRED_ORIGINAL_OBSERVATIONS_NOT_MEASURED_TRUTH_OR_INTERVENTION',
        'disposition':'FAIL' if errors else 'NOT_EVALUATED' if missing else 'PASS','errors':errors,'remainingRoles':missing,
        'requiredReferences':refs,'sourceInputIds':sorted(set(ids)),'comparisons':comparisons,
        'retainedSourceQualifications':{'records':retained}}
    def resolve(binding,schema,identity,role,selected):
        refs.append({'binding':binding,'role':role,'pointer':selected['pointer']})
        found=[v for v in sources if same(v['binding'],binding)]
        if len(found)!=1:need(role,selected['pointer']);return None
        entry=found[0];ids.append(entry['id']);shape=schemas.errors(schema,entry['record']);errors.extend(shape)
        if shape:return None
        compare('OBSERVATION_ACQUISITION_SOURCE_IDENTITY_MISMATCH',entry['record'][identity],binding['ref'],origin(entry,'/'+identity),{**selected,'pointer':selected['pointer']+'/ref'})
        return entry if entry['record'][identity]==binding['ref'] else None
    condition_entry=next((v for v in sources if same(v['binding'],condition_binding)),None)
    def compare_specification(spec):
        definition=spec['record'];requirements=definition['requiredObservations']
        for field,expected,path in [('workSpecificationBinding',work['binding'],'/body/workSpecification/binding'),
        ('procedureBinding',work['procedure'],'/body/workSpecification/procedure'),('propertyBinding',parameters['observedProperty'],'/body/parameters/observedProperty'),
        ('methodBinding',parameters['method'],'/body/parameters/method'),('observationContextBinding',parameters['observationContext'],'/body/parameters/observationContext')]:
            compare('OBSERVATION_ACQUISITION_SPECIFICATION_'+field.upper()+'_MISMATCH',definition[field],expected,origin(spec,'/'+field),claim(path))
        if len({v['slotId'] for v in requirements})!=len(requirements):errors.append({'code':'DUPLICATE_REQUIRED_OBSERVATION_SLOT','pointer':'/specification/requiredObservations'})
        if len({digest(v['measurementBinding']) for v in requirements})!=len(requirements):errors.append({'code':'REUSED_REQUIRED_OBSERVATION_BINDING','pointer':'/specification/requiredObservations'})
    entries={id(condition):condition_entry,
             id(atom):{'id':'ATOM:'+atom['atomId'],'record':atom}}
    def read_initial(parent,path,schema,role,identity,prerequisites):
        entry=resolve(pointer(parent,path),schema,identity,role,origin(entries[id(parent)],path))
        if entry is not None:entries[id(entry['record'])]=entry
        return entry
    resolved=resolve_acquisition_inputs(condition,condition_entry,read_initial,
        lambda code,path:errors.append({'code':code,'pointer':path}),need,compare_specification)
    if resolved is None:return result()
    spec,context=resolved
    definition=spec['record'];requirements=definition['requiredObservations']
    ctx=context['record'];target=body['target'];extent=body['extent']
    retained.append({'inputId':context['id'],'originalRecordDigest':digest(ctx),'fields':[{'pointer':'/'+k,'valueDigest':digest(v)} for k,v in ctx.items()]})
    compare('OBSERVATION_ACQUISITION_CONTEXT_PROPERTY_MISMATCH',ctx['observedPropertyRef'],parameters['observedProperty']['ref'],
        origin(context,'/observedPropertyRef'),claim('/body/parameters/observedProperty/ref'))
    if ctx['subject']['subjectType']=='SAMPLE':
        if 'targetScope' not in ctx:need('ACQUISITION_SAMPLE_TARGET_CONTEXT','/context/targetScope')
        else:
            for k,v,path in [('scopeType',target['kind'],'/body/target/kind'),('scopeRef',target['binding']['ref'],'/body/target/binding/ref')]:
                compare('OBSERVATION_ACQUISITION_SAMPLE_TARGET_MISMATCH',ctx['targetScope'][k],v,origin(context,'/targetScope/'+k),claim(path))
    else:
        compare('OBSERVATION_ACQUISITION_TARGET_KIND_MISMATCH',ctx['subject']['subjectType'],target['kind'],origin(context,'/subject/subjectType'),claim('/body/target/kind'))
        compare('OBSERVATION_ACQUISITION_TARGET_MISMATCH',ctx['subject']['subjectRef'],target['binding']['ref'],origin(context,'/subject/subjectRef'),claim('/body/target/binding/ref'))
    for k,v,path in [('scopeType',target['kind'],'/body/target/kind'),('scopeRef',target['binding']['ref'],'/body/target/binding/ref')]:
        compare('OBSERVATION_ACQUISITION_SPATIAL_TARGET_MISMATCH',ctx['spatialContext']['scope'][k],v,origin(context,'/spatialContext/scope/'+k),claim(path))
    spatial=ctx['spatialContext']
    meaning=definition.get('extentTemporalMeaning');partial=None
    if extent['posture']=='FULL_TARGET_SCOPE':
        if meaning is not None:errors.append({'code':'OBSERVATION_ACQUISITION_EXTENT_MEANING_WITHOUT_PARTIAL_SCOPE','pointer':'/specification/extentTemporalMeaning'})
        if 'partialExtentRef' in spatial or spatial['spatialBasis']!='WHOLE_SCOPE':errors.append({'code':'OBSERVATION_ACQUISITION_PARTIAL_FOR_WHOLE_SCOPE','pointer':'/context/spatialContext'})
    else:
        if 'partialExtentRef' not in spatial:need('EXACT_ACQUISITION_PARTIAL_EXTENT','/context/spatialContext/partialExtentRef')
        else:compare('OBSERVATION_ACQUISITION_PARTIAL_EXTENT_MISMATCH',spatial['partialExtentRef'],extent['binding']['ref'],origin(context,'/spatialContext/partialExtentRef'),claim('/body/extent/binding/ref'))
        if spatial['spatialBasis'] in ['WHOLE_SCOPE','UNKNOWN']:errors.append({'code':'OBSERVATION_ACQUISITION_PARTIAL_BASIS_MISMATCH','pointer':'/context/spatialContext/spatialBasis'})
        partial=resolve_acquisition_extent(atom,context,read_initial)
        if partial is not None:
            for k,v,path in [('scopeType',target['kind'],'/body/target/kind'),('scopeRef',target['binding']['ref'],'/body/target/binding/ref')]:
                compare('OBSERVATION_ACQUISITION_EXTENT_PARENT_MISMATCH',partial['record']['parentScope'][k],v,origin(partial,'/parentScope/'+k),claim(path))
            # Time of the actual required observation is checked against the
            # extent below; an entire work interval is not substituted for it.
            if meaning is not None:
                valid_meaning=True
                for key,expected,destination in [
                    ('extentBinding',extent['binding'],claim('/body/extent/binding')),
                    ('sourceTimeType',partial['record']['temporalApplicability']['timeType'],origin(partial,'/temporalApplicability/timeType')),
                    ('timeBasis',partial['record']['temporalApplicability']['timeBasis'],origin(partial,'/temporalApplicability/timeBasis'))]:
                    label={'extentBinding':'BINDING','sourceTimeType':'TIME_FORM','timeBasis':'TIME_BASIS'}[key]
                    compare('OBSERVATION_ACQUISITION_EXTENT_MEANING_'+label+'_MISMATCH',meaning[key],expected,
                        origin(spec,'/extentTemporalMeaning/'+key),destination)
                    valid_meaning=valid_meaning and same(meaning[key],expected)
                if not valid_meaning:meaning=None
    cp=ctx['procedure']
    if cp['procedureStatus']=='UNKNOWN_OR_MISSING':need('ACQUISITION_CONTEXT_PROCEDURE_MEANING','/context/procedure')
    if 'measurementMethodRef' not in cp:need('ACQUISITION_CONTEXT_METHOD','/context/procedure/measurementMethodRef')
    else:compare('OBSERVATION_ACQUISITION_CONTEXT_METHOD_MISMATCH',cp['measurementMethodRef'],parameters['method']['ref'],origin(context,'/procedure/measurementMethodRef'),claim('/body/parameters/method/ref'))
    def observation_window(t,slot):
        # An acquired observation needs an actual finite phenomenon bound before
        # it can be compared with its recording time. An absent end is not one.
        fields={'instant','intervalStart','intervalEnd'} & t.keys();point=t['timeType'] in ['INSTANT','AS_OF']
        conflict=(point and bool(fields-{'instant'})) or (not point and 'instant' in fields) or (t['timeType']=='OPEN_INTERVAL' and 'intervalEnd' in fields)
        if conflict:
            errors.append({'code':'OBSERVATION_ACQUISITION_PHENOMENON_TIME_FORM_INVALID','pointer':'/measurement/phenomenonTime'});return None
        required={'instant'} if point else {'intervalStart','intervalEnd'}
        if not required<=fields:
            need('ACQUISITION_PHENOMENON_TIME_BOUND:'+slot,'/measurement/phenomenonTime');return None
        try:values={key:foreign_instant(t[key]) for key in fields}
        except (ValueError,TypeError):
            errors.append({'code':'OBSERVATION_ACQUISITION_PHENOMENON_TIME_INVALID','pointer':'/measurement/phenomenonTime'});return None
        if any(v['unknownLocalOffset'] for v in values.values()):
            need('ACQUISITION_KNOWN_PHENOMENON_INSTANT_INTERPRETATION:'+slot,'/measurement/phenomenonTime');return None
        if not point and values['intervalEnd']['seconds']<values['intervalStart']['seconds']:
            errors.append({'code':'OBSERVATION_ACQUISITION_PHENOMENON_TIME_ORDER_INVALID','pointer':'/measurement/phenomenonTime'});return None
        # This is internal calculation input, never a replacement source operand.
        return {'at':t['instant']} if point else {'start':t['intervalStart'],'end':t['intervalEnd']}
    def context_time(actual,expected,entry,slot):
        clocks={'instant','intervalStart','intervalEnd'}
        matched=actual.keys()==expected.keys() and same({k:v for k,v in actual.items() if k not in clocks},{k:v for k,v in expected.items() if k not in clocks})
        unknown=False
        if matched:
            required={'instant'} if actual['timeType'] in ['INSTANT','AS_OF'] else {'intervalStart'}
            unknown=not required<=actual.keys()
            for key in clocks & actual.keys():
                left,right=foreign_instant(actual[key]),foreign_instant(expected[key])
                if left['unknownLocalOffset'] or right['unknownLocalOffset']:unknown=True
                elif left['seconds']!=right['seconds']:matched=False
        if matched and unknown:need('ACQUISITION_CONTEXT_KNOWN_PHENOMENON_TIME_INTERPRETATION:'+slot,'/context/phenomenonTime')
        else:compare('OBSERVATION_ACQUISITION_CONTEXT_TIME_MISMATCH',actual,expected,origin(entry,'/phenomenonTime'),origin(context,'/phenomenonTime'),matched)
    for index,required,entry in acquisition_observation_inputs(spec,context,read_initial):
        prefix='/requiredObservations/'+str(index)
        if entry is None:continue
        record=entry['record'];value=record['result'];kind=value['resultKind']
        retained.append({'inputId':entry['id'],'originalRecordDigest':digest(record),'fields':[{'pointer':'/'+k,'valueDigest':digest(v)} for k,v in record.items()]})
        compare('OBSERVATION_ACQUISITION_PROPERTY_MISMATCH',record['observedPropertyRef'],parameters['observedProperty']['ref'],origin(entry,'/observedPropertyRef'),claim('/body/parameters/observedProperty/ref'))
        if ctx['subject']['subjectType']=='SAMPLE':
            if 'sampleRef' not in record:need('ACQUISITION_SAMPLE_LINK:'+required['slotId'],'/measurement/sampleRef')
            else:compare('OBSERVATION_ACQUISITION_SAMPLE_LINK_MISMATCH',record['sampleRef'],ctx['subject']['subjectRef'],origin(entry,'/sampleRef'),origin(context,'/subject/subjectRef'))
        compare('OBSERVATION_ACQUISITION_CONTEXT_EVIDENCE_LINK_MISSING',ctx['evidenceRefs'],record['measurementEvidenceId'],origin(context,'/evidenceRefs'),origin(entry,'/measurementEvidenceId'),record['measurementEvidenceId'] in ctx['evidenceRefs'])
        method=record.get('measurementMethod')
        if method is None:need('ACQUISITION_MEASUREMENT_METHOD:'+required['slotId'],'/measurement/measurementMethod')
        else:
            compare('OBSERVATION_ACQUISITION_METHOD_MISMATCH',method['procedureRef'],parameters['method']['ref'],origin(entry,'/measurementMethod/procedureRef'),claim('/body/parameters/method/ref'))
            if method['procedureStatus']=='UNKNOWN_OR_MISSING':need('ACQUISITION_METHOD_MEANING:'+required['slotId'],'/measurement/measurementMethod')
            if 'versionRef' not in method:need('ACQUISITION_METHOD_VERSION:'+required['slotId'],'/measurement/measurementMethod/versionRef')
            else:compare('OBSERVATION_ACQUISITION_METHOD_VERSION_MISMATCH',method['versionRef'],definition['methodVersionRef'],origin(entry,'/measurementMethod/versionRef'),origin(spec,'/methodVersionRef'))
        compare('OBSERVATION_ACQUISITION_RESULT_KIND_NOT_PERMITTED',kind,required['permittedResultKinds'],origin(entry,'/result/resultKind'),origin(spec,prefix+'/permittedResultKinds'),kind in required['permittedResultKinds'])
        if kind=='ABSENT_PENDING' or 'RESULT_PENDING' in record.get('degradationReasons',[]):errors.append({'code':'PENDING_OBSERVATION_CANNOT_ESTABLISH_ACQUISITION_FINISH','pointer':'/measurement/result'})
        if kind=='QUALITATIVE' and not value['qualitativeValue'].strip():errors.append({'code':'EMPTY_OBSERVATION_CANNOT_ESTABLISH_ACQUISITION_FINISH','pointer':'/measurement/result'})
        if kind in ['NUMERIC','CENSORED_NUMERIC']:
            if required['quantityContext'] is None:need('ACQUISITION_QUANTITY_MEANING:'+required['slotId'],prefix+'/quantityContext')
            else:
                for field,key in [('quantityKindRef','quantityKind'),('unitRef','unit')]:
                    compare('OBSERVATION_ACQUISITION_'+key.upper()+'_MISMATCH',value[field],required['quantityContext'][key],origin(entry,'/result/'+field),origin(spec,prefix+'/quantityContext/'+key))
                    if kind=='CENSORED_NUMERIC':compare('OBSERVATION_ACQUISITION_LIMIT_'+key.upper()+'_MISMATCH',value['detectionLimit'][field],required['quantityContext'][key],origin(entry,'/result/detectionLimit/'+field),origin(spec,prefix+'/quantityContext/'+key))
        window=None
        if 'phenomenonTime' not in record:need('ACQUISITION_PHENOMENON_TIME:'+required['slotId'],'/measurement/phenomenonTime')
        else:
            window=observation_window(record['phenomenonTime'],required['slotId'])
            context_time(record['phenomenonTime'],ctx['phenomenonTime'],entry,required['slotId'])
            if extent['posture']=='PARTIAL_TARGET_SCOPE' and partial is not None and window is not None:
                checked=extent_time(partial['record']['temporalApplicability'],window,meaning)
                for error in checked['errors']:
                    location=('/specification' if error['pointer'].startswith('/extentTemporalMeaning') else '/extent')+error['pointer']
                    errors.append({'code':'OBSERVATION_ACQUISITION_EXTENT_'+error['code'],'pointer':location})
                for role in checked['remainingRoles']:need('ACQUISITION_EXTENT_'+role+':'+required['slotId'],'/extent/temporalApplicability')
                if checked['coverage'] is not None:
                    compare('OBSERVATION_ACQUISITION_EXTENT_TIME_MISMATCH',record['phenomenonTime'],partial['record']['temporalApplicability'],
                        origin(entry,'/phenomenonTime'),origin(partial,'/temporalApplicability'),checked['coverage'])
        try:
            time=atom['scope']['subjectTime'];start=foreign_seconds(time.get('start',time.get('at')))
            end=foreign_seconds(time['end']) if 'end' in time else start if 'at' in time else None
            at=foreign_seconds(record['resultTime'])
            if window is not None:
                z=foreign_seconds(window.get('end',window.get('at')))
                compare('OBSERVATION_ACQUISITION_PHENOMENON_AFTER_RECORDING',record['phenomenonTime'],record['resultTime'],origin(entry,'/phenomenonTime'),origin(entry,'/resultTime'),z<=at)
            compare('OBSERVATION_ACQUISITION_RECORDING_TIME_OUTSIDE_WORK',record['resultTime'],time,origin(entry,'/resultTime'),claim('/scope/subjectTime'),end is not None and start<=at<=end)
        except (ValueError,TypeError,KeyError):need('ACQUISITION_RECORDING_TIME_MEANING:'+required['slotId'],'/measurement/resultTime')
    return result()
