"""Directed parent-scope fields from existing identity payloads.

This reads the original selected Field/CropCycle payload. It does not create
relationship proofs or infer authority from a parent relationship. Field parent
applicability and eligible use stay separate where the carrier supplies neither.
"""
from strict_inputs import same,digest,pointer

KINDS={
 'FIELD':('ofarm.fieldidentitypayload.v0.1','https://ofarm.dev/schema/fieldidentitypayload/v0.1','fieldidentitypayloadId'),
 'CROP_CYCLE':('ofarm.cropcycleidentitypayload.v0.1','https://ofarm.dev/schema/cropcycleidentitypayload/v0.1','cropcycleidentitypayloadId'),
}


from domain_reader_occurrences import reader, selection as observe_selection, guard as observe_guard, origin as read_origin, observed_shape, predicate_value, observe_comparisons, branch as observed_branch, guard_refs


def _evaluate(intent,sources,schemas,*,subject_pointer='/subject',subject_ref_field='subjectRef',
             proofs_pointer='/subjectScopeProofBindings',time_pointer='/subjectTime',
             anchor_pointer='/resources/0/scope',anchor_kind_field='scopeType',anchor_ref_field='scopeRef',
             selected_proofs=None,subject_kind_pointer=None):
    from time_validation import foreign_seconds
    subject=intent['subject'];anchor=intent['resources'][0]['scope']
    anchor_ref=pointer(anchor,'/'+anchor_ref_field)
    errors,missing,comparisons,ids,refs=[],[],[],[],[]
    result={'scope':'DIRECTED_ORIGINAL_PARENT_SCOPE_FIELDS_ONLY','errors':errors,'remainingRoles':missing,
            'comparisons':comparisons,'sourceInputIds':ids,'requiredReferences':refs}
    def finish():
        return {**result,'disposition':'FAIL' if errors else 'NOT_EVALUATED' if missing else 'PASS',
                'qualification':'Original parent identity fields and supplied lifetime only; no relationship eligibility, authority, accepted membership or runtime admission is inferred.'}
    def compare(code,left,right,src,dst,*,depends_on=()):
        okay=same(left,right)
        comparisons.append({'predicateId':code,'equal':okay,'pointer':src['pointer'],
            'source':{**src,'valueDigest':digest(left)},'destination':{**dst,'valueDigest':digest(right)},
            'disposition':'PASS' if okay else 'FAIL'})
        observe_comparisons([comparisons[-1]], depends_on=depends_on)
        if not okay:errors.append({'code':code,'pointer':src['pointer']})
    kind=subject['subjectType']
    kind_origin=read_origin('EFFECT_INTENT',subject_kind_pointer or subject_pointer+'/subjectType')
    if not observed_branch('DIRECTED_PARENT_SCOPE_KIND_SUPPORTED',kind in KINDS,origins=[kind_origin]):
        missing.append({'role':'EXACT_DIRECTED_SUBJECT_TO_ANCHOR_PROOF_AT_TIME_AND_EXTENT','pointer':proofs_pointer});return finish()
    version,schema_id,id_field=KINDS[kind]
    selected=[];seen=set()
    proofs=selected_proofs if selected_proofs is not None else [
        (binding,proofs_pointer+'/'+str(index)) for index,binding in enumerate(intent.get('subjectScopeProofBindings',[]))]
    for binding,selection_pointer in proofs:
        for entry in sources:
            if same(entry['binding'],binding) and predicate_value(entry, '', isinstance(entry['record'],dict), 'DIRECTED_PARENT_SCOPE_PAYLOAD') and predicate_value(entry, '/schemaVersion', entry['record'].get('schemaVersion'), 'DIRECTED_PARENT_SCOPE_PAYLOAD')==version:
                original=(entry['binding']['ref'],entry['rawSha256'],entry['valueDigest'])
                if original not in seen:selected.append((selection_pointer,entry));seen.add(original)
    selected_read=observe_selection('DIRECTED_PARENT_SCOPE_PAYLOAD', sources, [(entry, location) for location, entry in selected],
        origins=[read_origin('EFFECT_INTENT', subject_pointer), kind_origin, read_origin('EFFECT_INTENT', proofs_pointer)],
        guards=guard_refs('DIRECTED_PARENT_SCOPE_KIND_SUPPORTED'))
    if len(selected)!=1:
        missing.append({'role':'EXACT_SELECTED_'+kind+'_PARENT_IDENTITY_PAYLOAD','pointer':proofs_pointer})
        if len(selected)>1:
            observe_comparisons([{'predicateId':'AMBIGUOUS_PARENT_SCOPE_PAYLOAD',
                'source':read_origin('EFFECT_INTENT',proofs_pointer),'disposition':'FAIL'}],
                depends_on=[selected_read] if selected_read is not None else [])
            errors.append({'code':'AMBIGUOUS_PARENT_SCOPE_PAYLOAD','pointer':proofs_pointer})
        return finish()
    selection_pointer,entry=selected[0];record=entry['record'];ids.append(entry['id'])
    refs.append({'role':'DIRECTED_PARENT_SCOPE_PAYLOAD','binding':entry['binding'],'pointer':selection_pointer})
    shape=observed_shape(schemas, schema_id,record);errors.extend(shape)
    shape_accepted=observe_guard('DIRECTED_PARENT_SCOPE_SHAPE_ACCEPTED',not shape,
        origins=[read_origin(entry['id'],'')],depends_on=[selected_read] if selected_read is not None else [])
    if shape:return finish()
    compare('RELATION_PAYLOAD_IDENTITY_MISMATCH',record[id_field],entry['binding']['ref'],
        {'inputRole':entry['id'],'pointer':'/'+id_field},{'inputRole':'EFFECT_INTENT','pointer':selection_pointer+'/ref'})
    compare('RELATION_CHILD_IDENTITY_MISMATCH',record['identityRecordRef'],subject['subjectRef'],
        {'inputRole':entry['id'],'pointer':'/identityRecordRef'},{'inputRole':'EFFECT_INTENT','pointer':subject_pointer+'/'+subject_ref_field})
    subject_binding={'ref':subject['subjectRef'],**{k:subject[k] for k in ['revisionRef','digest'] if k in subject}}
    identities=[s for s in sources if same(s['binding'],subject_binding)]
    observe_selection('PARENT_SUBJECT_IDENTITY_LINK', sources, identities, binding=subject_binding,
        origins=[read_origin('EFFECT_INTENT', subject_pointer)])
    if len(identities)==1 and predicate_value(identities[0], '', isinstance(identities[0]['record'],dict), 'PARENT_SUBJECT_IDENTITY_CURRENT_PAYLOAD') and predicate_value(identities[0], '/currentPayloadRef', identities[0]['record'].get('currentPayloadRef'), 'PARENT_SUBJECT_IDENTITY_CURRENT_PAYLOAD') is not None:
        identity=identities[0];ids.append(identity['id'])
        compare('RELATION_PAYLOAD_NOT_SELECTED_BY_SUBJECT_IDENTITY',identity['record']['currentPayloadRef'],record[id_field],
            {'inputRole':identity['id'],'pointer':'/currentPayloadRef'},{'inputRole':entry['id'],'pointer':'/'+id_field})
    else:missing.append({'role':'SUBJECT_IDENTITY_TO_SELECTED_PARENT_PAYLOAD_LINK','pointer':subject_pointer})
    if observed_branch('DIRECTED_PARENT_SCOPE_FIELD_BRANCH',kind=='FIELD',origins=[kind_origin],
            depends_on=[shape_accepted] if shape_accepted is not None else []):
        correct_kind=anchor[anchor_kind_field]=='FARM'
        observe_comparisons([{'predicateId':'FIELD_PARENT_ANCHOR_KIND_MISMATCH',
            'source':read_origin('EFFECT_INTENT',anchor_pointer+'/'+anchor_kind_field),
            'disposition':'PASS' if correct_kind else 'FAIL'}],
            depends_on=guard_refs('DIRECTED_PARENT_SCOPE_FIELD_BRANCH'))
        if not correct_kind:errors.append({'code':'FIELD_PARENT_ANCHOR_KIND_MISMATCH','pointer':anchor_pointer+'/'+anchor_kind_field})
        compare('FIELD_PARENT_ANCHOR_IDENTITY_MISMATCH',record['parentFarmIdentityRef'],anchor_ref,
            {'inputRole':entry['id'],'pointer':'/parentFarmIdentityRef'},{'inputRole':'EFFECT_INTENT','pointer':anchor_pointer+'/'+anchor_ref_field})
        # recordedAt is capture time; this carrier has no validity interval.
        missing.append({'role':'FIELD_PARENT_RELATION_TIME_APPLICABILITY','pointer':selection_pointer})
    else:
        indices=[n for n,v in enumerate(record['parentScopeRefs']) if predicate_value(entry,
            '/parentScopeRefs/'+str(n),v,'CYCLE_PARENT_ANCHOR_IDENTITY_MEMBERSHIP',
            depends_on=guard_refs('DIRECTED_PARENT_SCOPE_FIELD_BRANCH'))==anchor_ref]
        membership=observe_guard('CYCLE_PARENT_ANCHOR_IDENTITY_MEMBERSHIP:OPERANDS',bool(indices),
            origins=[read_origin('EFFECT_INTENT',anchor_pointer+'/'+anchor_ref_field)],
            depends_on=guard_refs('DIRECTED_PARENT_SCOPE_FIELD_BRANCH'),
            predicate_sites=('CYCLE_PARENT_ANCHOR_IDENTITY_MEMBERSHIP',))
        membership_dependencies=[membership] if membership is not None else []
        observe_comparisons([{'predicateId':'CYCLE_PARENT_ANCHOR_IDENTITY_MISSING',
            'source':read_origin(entry['id'],'/parentScopeRefs'),
            'destination':read_origin('EFFECT_INTENT',anchor_pointer+'/'+anchor_ref_field),
            'disposition':'PASS' if indices else 'FAIL'}],depends_on=membership_dependencies)
        if not indices:errors.append({'code':'CYCLE_PARENT_ANCHOR_IDENTITY_MISSING','pointer':'/parentScopeRefs'})
        else:
            n=indices[0];result['parentScopeIndex']=n
            compare('CYCLE_PARENT_ANCHOR_IDENTITY_MISMATCH',record['parentScopeRefs'][n],anchor_ref,
                {'inputRole':entry['id'],'pointer':'/parentScopeRefs/'+str(n)},
                {'inputRole':'EFFECT_INTENT','pointer':anchor_pointer+'/'+anchor_ref_field},
                depends_on=membership_dependencies)
        if 'startedAt' not in record:
            missing.append({'role':'CROP_CYCLE_TIME_APPLICABILITY','pointer':'/startedAt'})
        else:
            time=intent['subjectTime']
            try:
                start=foreign_seconds(record['startedAt']);end=foreign_seconds(record['endedAt']) if 'endedAt' in record else None
                lo=foreign_seconds(time.get('at',time.get('start')))
                hi=foreign_seconds(time['end']) if 'end' in time else lo if 'at' in time else None
                if end is not None and start>=end:errors.append({'code':'EMPTY_CROP_CYCLE_SOURCE_INTERVAL','pointer':'/endedAt'})
                covered=start<=lo and (end is None or hi is not None and hi<=end)
                boundary_unknown=end is not None and 'at' in time and lo==end
                if boundary_unknown:missing.append({'role':'CROP_CYCLE_END_INSTANT_INCLUSION_APPLICABILITY','pointer':selection_pointer})
                if not covered:errors.append({'code':'CROP_CYCLE_LIFETIME_DOES_NOT_COVER_CLAIM','pointer':time_pointer})
                if boundary_unknown:
                    # The carrier does not specify inclusion of the exact end
                    # instant. Record only the supported scalar comparisons;
                    # the missing role above retains interval-use uncertainty.
                    for field,predicate in [('startedAt','CROP_CYCLE_START_NOT_AFTER_CLAIM_INSTANT'),
                                            ('endedAt','CROP_CYCLE_END_EQUALS_CLAIM_INSTANT')]:
                        comparisons.append({'predicateId':predicate,
                            'source':{'inputRole':entry['id'],'pointer':'/'+field,'valueDigest':digest(record[field])},
                            'destination':{'inputRole':'EFFECT_INTENT','pointer':time_pointer+'/at','valueDigest':digest(time['at'])},
                            'disposition':'PASS' if (start<=lo if field=='startedAt' else end==lo) else 'FAIL'})
                        observe_comparisons([comparisons[-1]])
                for field in [] if boundary_unknown else ['startedAt']+(['endedAt'] if 'endedAt' in record else []):
                    comparisons.append({'predicateId':'CROP_CYCLE_LIFETIME_COVERS_CLAIM_'+field.upper(),
                        'source':{'inputRole':entry['id'],'pointer':'/'+field,'valueDigest':digest(record[field])},
                        'destination':{'inputRole':'EFFECT_INTENT','pointer':time_pointer,'valueDigest':digest(time)},
                        'disposition':'PASS' if covered and not any(e['code']=='EMPTY_CROP_CYCLE_SOURCE_INTERVAL' for e in errors) else 'FAIL'})
                    observe_comparisons([comparisons[-1]])
            except (ValueError,TypeError):errors.append({'code':'INVALID_CROP_CYCLE_SOURCE_TIME','pointer':'/startedAt'})
    # Current payload selection and a parent reference do not prove that this
    # historical relation is an eligible governing source at the claimed time.
    missing.append({'role':'PARENT_RELATION_SOURCE_USE_AT_SELECTED_TIME_AND_EXTENT','pointer':selection_pointer})
    return finish()


# Fixed internal entry points keep each actual caller's duty separate. Both
# observe the same reader implementation and preserve existing call compatibility.
evaluate=reader('relation_sources.py',['AR_SUBJECT_SCOPE_PROOF'])(_evaluate)
evaluate_body=reader('relation_sources.py',['AR_BODY'])(_evaluate)
