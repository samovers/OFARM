"""Bounded sample -> original support -> target fields, without admission.

An independently selected domain use definition fixes the exact original
chain and time interpretation. It is not a specimen record or a foreign proof.
Every relied-on original is also explicitly declared in the selected operation
output specification's relation proof set. The selected support time concerns
the sample phenomenon; it is not the later analysis production/work time.
"""
import copy
from strict_inputs import same,digest,distinct_selected_originals,pointer
from definition_inputs import SCHEMAS,register


def evaluate(atom,sources,schemas):
    return _evaluate_sample_relation(atom, sources, schemas)


def evaluate_traced(atom, sources, schemas):
    """Observe the actual sample reader without replacing its selectors."""
    trace = {'reads': [], 'guards': []}
    report = _evaluate_sample_relation(atom, sources, schemas, trace=trace)
    return {'report': report, **trace}


def _evaluate_sample_relation(atom, sources, schemas, *, trace=None):
    from time_validation import foreign_instant
    from extent_temporal import evaluate as temporal
    register(schemas)
    errors,missing,comparisons,ids,refs,retained=[],[],[],[],[],[]
    body=atom['body'];row=atom['definition'].split(':')[-1]
    proofs_pointer='/sampleTargetRelationProofBindings'
    def original(entry,path):return {'inputRole':entry['id'],'pointer':path}
    def claimed(path):return {'inputRole':'ATOM:'+atom['atomId'],'pointer':path}
    def selector(entry, path):
        return ({'kind': 'ORIGINAL', **original(entry, path)} if entry is not None
                else {'kind': 'ACTUAL_ATOM', **claimed(path)})
    def guard(rule, satisfied, read_indices=(), operands=(), **details):
        if trace is None: return None
        gid = 'sample-guard:' + str(len(trace['guards']))
        trace['guards'].append({'id': gid, 'rule': rule, 'satisfied': satisfied,
            'readIndices': [index for index in read_indices if index is not None],
            'operands': list(operands), **details})
        return gid
    def read_event(binding, schema_id, role, origin, found, guard_ids=(), *, attempted=True):
        if trace is None: return None
        event = {'binding': copy.deepcopy(binding), 'schemaId': schema_id, 'role': role,
            'bindingOrigin': origin, 'selectedInputId': found[0]['id'] if attempted and len(found) == 1 else None,
            'matchCount': len(found) if attempted else None, 'schemaErrors': None,
            'guardIds': [gid for gid in guard_ids if gid is not None],
            'attempted': attempted, 'reportedReference': False}
        trace['reads'].append(event)
        return event
    def read_index(): return len(trace['reads']) - 1 if trace is not None else None
    def shape_event(event, shape):
        if event is not None: event['schemaErrors'] = copy.deepcopy(shape)
    def reference_event(event):
        if event is not None: event['reportedReference'] = True
    def need(role,path):missing.append({'role':role,'pointer':path})
    def finish():return {'canonicalRow':'V06-sample-target','scope':'EXACT_ORIGINAL_SAMPLE_SUPPORT_CHAIN_NOT_IDENTITY_OR_ELIGIBLE_USE',
        'disposition':'FAIL' if errors else 'NOT_EVALUATED' if missing else 'PASS','errors':errors,'remainingRoles':missing,
        'comparisons':comparisons,'sourceInputIds':sorted(set(ids)),'requiredReferences':refs,
        'retainedSourceQualifications':retained}
    def compare(code,left,right,source,destination,equal=None):
        equal=same(left,right) if equal is None else equal
        comparisons.append({'predicateId':code,'pointer':destination['pointer'],'equal':equal,
            'source':{**source,'valueDigest':digest(left)},'destination':{**destination,'valueDigest':digest(right)},
            'disposition':'PASS' if equal else 'FAIL'})
        if not equal:errors.append({'code':code,'pointer':destination['pointer']})
    if row=='O10':
        from sample_collection_definitions import SCHEMAS as output_schemas, register as register_output
        output_name='sampleCollection'
    elif row=='O22':
        from analysis_output_definitions import SCHEMAS as output_schemas, register as register_output
        output_name='analysisOutput'
    else:
        errors.append({'code':'SAMPLE_TARGET_OPERATION_ROW_MISMATCH','pointer':'/definition'});return finish()
    register_output(schemas)
    selected_output=body['workSpecification'].get('outputSpecification')
    outputs=[s for s in sources if same(s['binding'],selected_output)]
    output_event = read_event(selected_output, output_schemas[output_name]['$id'],
        'SAMPLE_TARGET_OPERATION_OUTPUT_SPECIFICATION', selector(None, '/body/workSpecification/outputSpecification'), outputs)
    output_index = read_index()
    if len(outputs)!=1:
        need('SAMPLE_TARGET_EXACT_OPERATION_OUTPUT_SPECIFICATION','/body/workSpecification/outputSpecification');return finish()
    output=outputs[0];output_definition=output['record'];ids.append(output['id'])
    shape=schemas.errors(output_schemas[output_name]['$id'],output_definition);errors.extend(shape)
    shape_event(output_event, shape)
    output_ready = guard('SAMPLE_OUTPUT_SHAPE_AVAILABLE', not shape, (output_index,))
    if shape:return finish()
    refs.append({'role':'SAMPLE_TARGET_OPERATION_OUTPUT_SPECIFICATION','binding':selected_output,'pointer':'/body/workSpecification/outputSpecification'})
    reference_event(output_event)
    compare('SAMPLE_TARGET_OUTPUT_SPECIFICATION_IDENTITY_MISMATCH',output_definition['definitionId'],selected_output['ref'],
        original(output,'/definitionId'),claimed('/body/workSpecification/outputSpecification/ref'))
    for field,path in [('workSpecificationBinding','/body/workSpecification/binding'),('procedureBinding','/body/workSpecification/procedure'),('sampleBinding','/body/parameters/sample')]:
        compare('SAMPLE_TARGET_OUTPUT_'+field.upper()+'_MISMATCH',output_definition[field],pointer(atom,path),original(output,'/'+field),claimed(path))
    proofs=[(b,proofs_pointer+'/'+str(i)) for i,b in enumerate(output_definition.get('sampleTargetRelationProofBindings',[]))]
    candidates, selection_reads = [], []
    for candidate in sources:
        proof_paths = [path for binding, path in proofs if same(candidate['binding'], binding)]
        if not proof_paths: continue
        record = candidate['record']
        matches = (isinstance(record, dict)
                   and record.get('schemaVersion') == 'ofarm.assertionDomainSampleTargetRelationUseDefinition.v0.1')
        if trace is not None:
            observed_pointer = '/schemaVersion' if isinstance(record, dict) and 'schemaVersion' in record else ''
            selection_reads.append({'binding': copy.deepcopy(candidate['binding']),
                'bindingOrigin': selector(output, proof_paths[0]), 'selectedInputId': candidate['id'],
                'sourcePointer': observed_pointer,
                'sourceValueDigest': digest(record['schemaVersion'] if observed_pointer else record),
                'matchesRelationDefinition': matches})
        if matches: candidates.append(candidate)
    selected=distinct_selected_originals(candidates)
    unique_relation = guard('UNIQUE_SAMPLE_RELATION_ORIGINAL', len(selected) == 1, (output_index,),
        (selector(output, proofs_pointer),), selectedCandidateInputIds=[item['id'] for item in selected],
        selectionReads=selection_reads)
    if len(selected)!=1:
        need('EXACT_SAMPLE_TARGET_RELATION_USE_DEFINITION',proofs_pointer)
        if len(selected)>1:errors.append({'code':'AMBIGUOUS_SAMPLE_TARGET_RELATION_USE','pointer':proofs_pointer})
        return finish()
    spec=selected[0];definition=spec['record'];ids.append(spec['id'])
    selected_path=next(p for b,p in proofs if same(b,spec['binding']))
    relation_event = read_event(spec['binding'], SCHEMAS['sampleTargetUse']['$id'], 'SAMPLE_TARGET_RELATION_USE',
        selector(output, selected_path), selected, (output_ready, unique_relation))
    relation_index = read_index()
    shape=schemas.errors(SCHEMAS['sampleTargetUse']['$id'],definition);errors.extend(shape)
    shape_event(relation_event, shape)
    relation_ready = guard('SAMPLE_RELATION_SHAPE_AVAILABLE', not shape, (relation_index,))
    if shape:return finish()
    refs.append({'role':'SAMPLE_TARGET_RELATION_USE','binding':spec['binding'],'pointer':selected_path})
    reference_event(relation_event)
    compare('SAMPLE_TARGET_USE_IDENTITY_MISMATCH',definition['definitionId'],spec['binding']['ref'],original(spec,'/definitionId'),original(output,selected_path+'/ref'))
    compare('SAMPLE_TARGET_SAMPLE_SELECTION_MISMATCH',definition['sampleBinding'],body['parameters']['sample'],original(spec,'/sampleBinding'),claimed('/body/parameters/sample'))
    for field,code in [('binding','TARGET_SELECTION'),('kind','TARGET_KIND')]:
        compare('SAMPLE_TARGET_'+code+'_MISMATCH',definition['target'][field],output_definition['sampleTarget'][field],original(spec,'/target/'+field),original(output,'/sampleTarget/'+field))
        if row=='O10':
            compare('SAMPLE_TARGET_OPERATION_'+code+'_MISMATCH',definition['target'][field],body['target'][field],original(spec,'/target/'+field),claimed('/body/target/'+field))
    time=definition['subjectTime']
    output_guards = (relation_ready,)
    if row=='O10':
        if body['extent']['posture']=='PARTIAL_TARGET_SCOPE':
            compare('SAMPLE_TARGET_OPERATION_EXTENT_SELECTION_MISMATCH',definition['partialExtentBinding'],body['extent']['binding'],
                original(spec,'/partialExtentBinding'),claimed('/body/extent/binding'))
        for field,other in [('measurementBinding','collectionMeasurementBinding'),('contextBinding','collectionContextBinding'),
                            ('samplingProtocolBinding','samplingProcedureBinding'),('samplingProtocolVersionRef','samplingProcedureVersionRef')]:
            compare('SAMPLE_TARGET_OPERATION_'+field.upper()+'_MISMATCH',definition[field],output_definition[other],original(spec,'/'+field),original(output,'/'+other))
    else:
        compare('SAMPLE_TARGET_ANALYSIS_OUTPUT_SPECIFICATION_SELECTION_MISMATCH',body['parameters']['producedResult']['specificationBinding'],selected_output,
            claimed('/body/parameters/producedResult/specificationBinding'),claimed('/body/workSpecification/outputSpecification'))
        actual_output = guard('ACTUAL_ANALYSIS_OUTPUT_SELECTED', body['parameters']['producedResult']['role'] == 'ACTUAL_OUTPUT',
            (), (selector(None, '/body/parameters/producedResult/role'),))
        output_guards = (relation_ready, actual_output)
        if body['parameters']['producedResult']['role']!='ACTUAL_OUTPUT':
            need('SAMPLE_TARGET_ACTUAL_ANALYSIS_OUTPUT','/body/parameters/producedResult');return finish()
        compare('SAMPLE_TARGET_OPERATION_MEASUREMENTBINDING_MISMATCH',definition['measurementBinding'],body['parameters']['producedResult']['binding'],
            original(spec,'/measurementBinding'),claimed('/body/parameters/producedResult/binding'))
    def resolve(field,schema_id,identity, guard_ids=()):
        binding=definition[field];path='/'+field;declared=[p for b,p in proofs if same(b,binding)]
        refs.append({'role':'SAMPLE_TARGET_'+field.upper(),'binding':binding,'pointer':path})
        declared_guard = guard('EXPLICIT_SAMPLE_PROOF_MEMBER:' + field, bool(declared), (output_index, relation_index),
            (selector(spec, path), selector(output, proofs_pointer)), matchingProofPointers=list(declared))
        found=[v for v in sources if same(v['binding'],binding)] if declared else []
        event = read_event(binding, schema_id, 'SAMPLE_TARGET_' + field.upper(), selector(spec, path), found,
                           (*output_guards, *guard_ids, declared_guard), attempted=bool(declared))
        reference_event(event)
        if not declared:
            need('SAMPLE_TARGET_EXPLICIT_'+field.upper()+'_PROOF',proofs_pointer);return None
        compare('SAMPLE_TARGET_EXACT_PROOF_SELECTION',binding,pointer(output_definition,declared[0]),original(spec,path),original(output,declared[0]))
        if len(found)!=1:need('SAMPLE_TARGET_ORIGINAL_'+field.upper(),path);return None
        entry=found[0];ids.append(entry['id']);record=entry['record'];shape=schemas.errors(schema_id,record);errors.extend(shape)
        shape_event(event, shape)
        if shape:return None
        compare('SAMPLE_TARGET_SOURCE_IDENTITY_MISMATCH',record[identity],binding['ref'],original(entry,'/'+identity),original(spec,path+'/ref'))
        retained.append({'inputId':entry['id'],'originalRecordDigest':digest(record),
            'fields':[{'pointer':'/'+k,'valueDigest':digest(v)} for k,v in record.items()]})
        return entry
    measurement=resolve('measurementBinding','https://ofarm.dev/schema/measurementevidence/v0.1','measurementEvidenceId')
    measurement_index = read_index()
    context=resolve('contextBinding','https://ofarm.dev/schema/agronomicobservationcontext/v0.1','agronomicObservationContextId')
    context_index = read_index()
    support_ready = guard('SAMPLE_MEASUREMENT_AND_CONTEXT_AVAILABLE', measurement is not None and context is not None,
                          (measurement_index, context_index))
    if measurement is None or context is None:return finish()
    m,c=measurement['record'],context['record']
    if 'sampleRef' not in m:need('SAMPLE_TARGET_ORIGINAL_SPECIMEN_LINK','/measurement/sampleRef')
    else:compare('SAMPLE_TARGET_SPECIMEN_MISMATCH',m['sampleRef'],definition['sampleBinding']['ref'],original(measurement,'/sampleRef'),original(spec,'/sampleBinding/ref'))
    compare('SAMPLE_TARGET_CONTEXT_SPECIMEN_KIND_MISMATCH',c['subject']['subjectType'],definition['sampleKind'],original(context,'/subject/subjectType'),original(spec,'/sampleKind'))
    compare('SAMPLE_TARGET_CONTEXT_SPECIMEN_MISMATCH',c['subject']['subjectRef'],definition['sampleBinding']['ref'],original(context,'/subject/subjectRef'),original(spec,'/sampleBinding/ref'))
    if 'agronomicObservationContextRef' in m:
        compare('SAMPLE_TARGET_FORWARD_CONTEXT_LINK_MISMATCH',m['agronomicObservationContextRef'],c['agronomicObservationContextId'],
            original(measurement,'/agronomicObservationContextRef'),original(context,'/agronomicObservationContextId'))
    else:
        compare('SAMPLE_TARGET_REVERSE_CONTEXT_LINK_MISSING',c['evidenceRefs'],m['measurementEvidenceId'],
            original(context,'/evidenceRefs'),original(measurement,'/measurementEvidenceId'),m['measurementEvidenceId'] in c['evidenceRefs'])
    compare('SAMPLE_TARGET_PROPERTY_MISMATCH',m['observedPropertyRef'],c['observedPropertyRef'],original(measurement,'/observedPropertyRef'),original(context,'/observedPropertyRef'))
    property_path='/body/parameters/'+('sampledProperty' if row=='O10' else 'property')+'/ref'
    compare('SAMPLE_TARGET_OPERATION_PROPERTY_MISMATCH',m['observedPropertyRef'],pointer(atom,property_path),original(measurement,'/observedPropertyRef'),claimed(property_path))
    for field in ['targetScope','spatialContext/scope']:
        try:value=pointer(c,'/'+field)
        except ValueError:need('SAMPLE_TARGET_ORIGINAL_TARGET_SCOPE','/context/'+field);continue
        for key,norm in [('scopeType','kind'),('scopeRef','binding/ref')]:
            compare('SAMPLE_TARGET_DIRECTED_'+key.upper()+'_MISMATCH',value[key],pointer(definition,'/target/'+norm),original(context,'/'+field+'/'+key),original(spec,'/target/'+norm))
    protocol=m.get('samplingProtocol')
    if protocol is None:need('SAMPLE_TARGET_COLLECTION_PROTOCOL','/measurement/samplingProtocol')
    else:
        compare('SAMPLE_TARGET_COLLECTION_PROTOCOL_MISMATCH',protocol['procedureRef'],definition['samplingProtocolBinding']['ref'],original(measurement,'/samplingProtocol/procedureRef'),original(spec,'/samplingProtocolBinding/ref'))
        if 'versionRef' not in protocol:need('SAMPLE_TARGET_COLLECTION_PROTOCOL_VERSION','/measurement/samplingProtocol/versionRef')
        else:compare('SAMPLE_TARGET_COLLECTION_PROTOCOL_VERSION_MISMATCH',protocol['versionRef'],definition['samplingProtocolVersionRef'],original(measurement,'/samplingProtocol/versionRef'),original(spec,'/samplingProtocolVersionRef'))
        if protocol['procedureStatus']=='UNKNOWN_OR_MISSING':need('SAMPLE_TARGET_COLLECTION_PROTOCOL_MEANING','/measurement/samplingProtocol')
    if 'samplingProtocolRef' not in c['procedure']:need('SAMPLE_TARGET_CONTEXT_COLLECTION_PROTOCOL','/context/procedure/samplingProtocolRef')
    else:compare('SAMPLE_TARGET_CONTEXT_COLLECTION_PROTOCOL_MISMATCH',c['procedure']['samplingProtocolRef'],definition['samplingProtocolBinding']['ref'],original(context,'/procedure/samplingProtocolRef'),original(spec,'/samplingProtocolBinding/ref'))
    if c['procedure']['procedureStatus']=='UNKNOWN_OR_MISSING':need('SAMPLE_TARGET_CONTEXT_PROCEDURE_MEANING','/context/procedure')
    if 'chainOfCustodyStatus' not in m:need('SAMPLE_TARGET_COLLECTION_CUSTODY_SOURCE','/measurement/chainOfCustodyStatus')
    def clock(entry,field,meaning,prefix):
        original_time=entry['record'][field]
        if meaning is not None:
            for key,source_key in [('sourceTimeType','timeType'),('timeBasis','timeBasis')]:
                if source_key not in original_time:need(prefix+'_ORIGINAL_TIME_BASIS','/'+field);continue
                compare(prefix+'_MEANING_'+key.upper()+'_MISMATCH',meaning[key],original_time[source_key],original(spec,('/measurementIntervalMeaning/' if prefix=='SAMPLE_TARGET_MEASUREMENT' else '/extentTemporalMeaning/')+key),original(entry,'/'+field+'/'+source_key))
        checked=temporal(original_time,time,meaning)
        errors.extend({'code':prefix+'_'+v['code'],'pointer':v['pointer']} for v in checked['errors'])
        for role in checked['remainingRoles']:need(prefix+'_'+role,'/'+field)
        if checked['coverage'] is not None:compare(prefix+'_TIME_COVERAGE_MISMATCH',original_time,definition['subjectTime'],original(entry,'/'+field),original(spec,'/subjectTime'),checked['coverage'])
    if 'phenomenonTime' not in m:need('SAMPLE_TARGET_ORIGINAL_PHENOMENON_TIME','/measurement/phenomenonTime')
    else:
        left,right=m['phenomenonTime'],c['phenomenonTime'];clocks={'instant','intervalStart','intervalEnd'}
        matched=left.keys()==right.keys() and same({k:v for k,v in left.items() if k not in clocks},{k:v for k,v in right.items() if k not in clocks});unknown=False
        if matched:
            unknown=not ({'instant'} if left['timeType']=='INSTANT' else {'intervalStart'})<=left.keys()
            for key in clocks & left.keys():
                a,z=foreign_instant(left[key]),foreign_instant(right[key])
                if a['unknownLocalOffset'] or z['unknownLocalOffset']:unknown=True
                elif a['seconds']!=z['seconds']:matched=False
        if matched and unknown:need('SAMPLE_TARGET_CONTEXT_KNOWN_TIME_INTERPRETATION','/context/phenomenonTime')
        else:compare('SAMPLE_TARGET_CONTEXT_TIME_MISMATCH',left,right,original(measurement,'/phenomenonTime'),original(context,'/phenomenonTime'),matched)
        if 'timeBasis' not in left:need('SAMPLE_TARGET_ORIGINAL_TIME_BASIS','/measurement/phenomenonTime/timeBasis')
        else:compare('SAMPLE_TARGET_TIME_BASIS_MISMATCH',left['timeBasis'],definition['phenomenonTimeBasis'],original(measurement,'/phenomenonTime/timeBasis'),original(spec,'/phenomenonTimeBasis'))
        clock(measurement,'phenomenonTime',definition.get('measurementIntervalMeaning'),'SAMPLE_TARGET_MEASUREMENT')
    extent_binding=definition['partialExtentBinding'];extent_ref=c['spatialContext'].get('partialExtentRef')
    extent_guard = guard('SAMPLE_PARTIAL_EXTENT_LINK_SELECTED', extent_ref is not None and extent_binding is not None,
        (context_index, relation_index), (selector(context, '/spatialContext'), selector(spec, '/partialExtentBinding')))
    if extent_ref is None:
        if extent_binding is not None:errors.append({'code':'SAMPLE_TARGET_UNLINKED_PARTIAL_EXTENT','pointer':'/partialExtentBinding'})
    elif extent_binding is None:need('SAMPLE_TARGET_EXACT_PARTIAL_EXTENT_SELECTION','/partialExtentBinding')
    else:
        if c['spatialContext']['spatialBasis'] in ['WHOLE_SCOPE','UNKNOWN']:
            errors.append({'code':'SAMPLE_TARGET_PARTIAL_SUPPORT_BASIS_MISMATCH','pointer':'/context/spatialContext/spatialBasis'})
        compare('SAMPLE_TARGET_PARTIAL_EXTENT_LINK_MISMATCH',extent_ref,extent_binding['ref'],original(context,'/spatialContext/partialExtentRef'),original(spec,'/partialExtentBinding/ref'))
        extent=resolve('partialExtentBinding','https://ofarm.dev/schema/partialextent/v0.1','partialExtentId',
                       (support_ready, extent_guard))
        if extent is not None:
            for key,norm in [('scopeType','kind'),('scopeRef','binding/ref')]:
                compare('SAMPLE_TARGET_EXTENT_PARENT_'+key.upper()+'_MISMATCH',extent['record']['parentScope'][key],pointer(definition,'/target/'+norm),original(extent,'/parentScope/'+key),original(spec,'/target/'+norm))
            meaning=definition.get('extentTemporalMeaning')
            if meaning is not None:compare('SAMPLE_TARGET_EXTENT_MEANING_BINDING_MISMATCH',meaning['extentBinding'],extent_binding,original(spec,'/extentTemporalMeaning/extentBinding'),original(spec,'/partialExtentBinding'))
            clock(extent,'temporalApplicability',meaning,'SAMPLE_TARGET_EXTENT')
    for role in ['SAMPLE_TARGET_ENDPOINT_VERSIONS_AND_ORIGINAL_SOURCE_USE','SAMPLE_TARGET_CUSTODY_GEOMETRY_AND_REPRESENTATIVENESS_USE']:
        need(role,selected_path)
    return finish()
