"""Typed identity and direct anchor comparisons over selected original records.

This reads identity metadata only. It creates no principal, authority, identity,
active-state conclusion or relation by association. Non-direct relationships
retain their exact required source role until their directed proof is checked.
"""
from strict_inputs import same, digest
from original_operand import select_operand

IDENTITY_SCHEMA='https://ofarm.dev/schema/identityrecord/v0.1'
PARTY_SCHEMA='https://ofarm.dev/schema/party/v0.1'
KINDS={k:{k} for k in ['FARM','SITE','FIELD','CROP_CYCLE','LOT','EQUIPMENT','FACILITY','STORAGE_LOCATION','CONTAINER']}
KINDS.update(ZONE={'MANAGEMENT_ZONE','MICROCLIMATE_ZONE'},INPUT={'APPLIED_RESOURCE'})


from domain_reader_occurrences import reader, selection as observe_selection, guard as observe_guard, origin as read_origin, observed_shape, observe_comparisons


@reader('identity_sources.py', ['AR_SUBJECT_SCOPE_PROOF', 'AR_OPERATION_PERFORMER'])
def evaluate(intent,sources,schemas):
    subject=intent['subject'];anchor=intent['resources'][0]['scope'];body=intent['assertionBody']
    outputs={}
    for gate in ['SUBJECT_SCOPE_RELATION','PERFORMER_IDENTITY']:
        errors,missing,comparisons,ids,postures=[],[],[],[],[];origins={}
        def compare(code,actual,expected,path,source=None,destination=None,equal=None):
            equal=same(actual,expected) if equal is None else equal
            fact={'predicateId':code,'pointer':path,'equal':equal,
                  'actualValueDigest':digest(actual),'expectedValueDigest':digest(expected)}
            if source is not None and destination is not None:
                fact.update(source={**source,'valueDigest':digest(actual)},
                            destination={**destination,'valueDigest':digest(expected)},
                            disposition='PASS' if equal else 'FAIL')
            comparisons.append(fact)
            observe_comparisons([comparisons[-1]], findings=['AR_SUBJECT_SCOPE_PROOF'] if gate == 'SUBJECT_SCOPE_RELATION' else ['AR_OPERATION_PERFORMER'])
            if not equal:errors.append({'code':code,'pointer':path})
        def resolve(binding,schema_id,id_field,role,binding_path):
            matches=[v for v in sources if same(v['binding'],binding)]
            observe_selection(role, sources, matches, binding=binding,
                origins=[read_origin('EFFECT_INTENT', binding_path)],
                findings=['AR_SUBJECT_SCOPE_PROOF'] if gate == 'SUBJECT_SCOPE_RELATION' else ['AR_OPERATION_PERFORMER'])
            if len(matches)!=1:
                missing.append({'role':role,'pointer':'/'+role});return None
            item=matches[0];ids.append(item['id']);record=item['record']
            shape=observed_shape(schemas, schema_id,record);errors.extend(shape)
            if shape:return None
            origins[id(record)]=item['id']
            compare('IDENTITY_RECORD_BINDING_MISMATCH',record[id_field],binding['ref'],'/'+id_field,
                    {'inputRole':item['id'],'pointer':'/'+id_field},
                    {'inputRole':'EFFECT_INTENT','pointer':binding_path})
            return record
        if gate=='SUBJECT_SCOPE_RELATION':
            anchor_binding={'ref':anchor['scopeRef'],**{k:anchor[k] for k in ['digest','revisionRef'] if k in anchor}}
            source_binding={'ref':subject['subjectRef'],**{k:subject[k] for k in ['digest','revisionRef'] if k in subject}}
            if subject['subjectPosture']=='EXISTING_SUBJECT' and subject['subjectType'] in KINDS:
                record=resolve(source_binding,IDENTITY_SCHEMA,'identityRecordId','EXACT_LOGICAL_SUBJECT_IDENTITY','/subject/subjectRef')
                if record is not None:
                    created_here=record.get('createdByAssertionRecordRef')==intent['effectSubject']['subjectRef']
                    # Preserve an absent optional field as absent, not JSON null.
                    observe_comparisons([{'predicateId':'IDENTITY_CANNOT_BE_CREATED_BY_THIS_PROPOSED_ASSERTION',
                        'source':{'inputRole':origins[id(record)],'pointer':'/createdByAssertionRecordRef'},
                        'destination':{'inputRole':'EFFECT_INTENT','pointer':'/effectSubject/subjectRef'},
                        'disposition':'FAIL' if created_here else 'PASS'}], findings=['AR_SUBJECT_SCOPE_PROOF'])
                    if created_here:
                        errors.append({'code':'IDENTITY_CANNOT_BE_CREATED_BY_THIS_PROPOSED_ASSERTION','pointer':'/createdByAssertionRecordRef'})
                    compare('SUBJECT_IDENTITY_KIND_MISMATCH',record['identityType'],subject['subjectType'],'/identityType',
                        {'inputRole':origins[id(record)],'pointer':'/identityType'},
                        {'inputRole':'EFFECT_INTENT','pointer':'/subject/subjectType'},equal=record['identityType'] in KINDS[subject['subjectType']])
                    postures.append({'binding':source_binding,'identityType':record['identityType'],'lifecycleState':record['lifecycleState']})
            else:
                missing.append({'role':'PROSPECTIVE_OR_SPECIALIZED_SUBJECT_KIND_SOURCE:'+subject['subjectType'],'pointer':'/subject'})
            direct=subject['subjectType']==anchor['scopeType'] and same(source_binding,anchor_binding)
            if not direct:
                from relation_sources import evaluate as relations
                relation=relations(intent,sources,schemas)
                errors.extend(relation['errors']);missing.extend(relation['remainingRoles'])
                comparisons.extend(relation['comparisons']);ids.extend(relation['sourceInputIds'])
                if anchor['scopeType'] in KINDS:
                    record=resolve(anchor_binding,IDENTITY_SCHEMA,'identityRecordId','EXACT_AUTHORITY_ANCHOR_IDENTITY','/resources/0/scope/scopeRef')
                    if record is not None:
                        compare('ANCHOR_IDENTITY_KIND_MISMATCH',record['identityType'],anchor['scopeType'],'/identityType',
                            {'inputRole':origins[id(record)],'pointer':'/identityType'},
                            {'inputRole':'EFFECT_INTENT','pointer':'/resources/0/scope/scopeType'},equal=record['identityType'] in KINDS[anchor['scopeType']])
            else:
                for source_key,anchor_key in [('subjectRef','scopeRef'), *[(k,k) for k in ['revisionRef','digest'] if k in subject]]:
                    compare('EXACT_DIRECT_SUBJECT_ANCHOR_'+source_key,subject[source_key],anchor[anchor_key],'/subject/'+source_key,
                            {'inputRole':'EFFECT_INTENT','pointer':'/subject/'+source_key},
                            {'inputRole':'EFFECT_INTENT','pointer':'/resources/0/scope/'+anchor_key})
        elif 'performedByBinding' not in body:
            outputs[gate]={'disposition':'NOT_APPLICABLE','errors':[],'remainingRoles':[],'comparisons':[],
                           'sourceInputIds':[],'reason':'This assertion branch makes no operation performer allegation.'};continue
        else:
            performer=body['performedByBinding'];party=resolve(performer,PARTY_SCHEMA,'partyId','EXACT_PERFORMER_PARTY_IDENTITY','/assertionBody/performedByBinding/ref')
            if party is not None:
                compare('PERFORMER_IDENTITY_ALIAS_MISMATCH',performer['ref'],intent['performedByPartyRef'],'/performedByPartyRef',
                        {'inputRole':'EFFECT_INTENT','pointer':'/assertionBody/performedByBinding/ref'},
                        {'inputRole':'EFFECT_INTENT','pointer':'/performedByPartyRef'})
                software=party['partyClass']=='SOFTWARE_AGENT'
                flag=body['allegesSoftwareAgentPerformance'];matches=flag==(software and intent['claimPosture']=='PERFORMED')
                flag_origin={'inputRole':'EFFECT_INTENT','pointer':'/assertionBody/allegesSoftwareAgentPerformance'}
                compare('PERFORMER_SOFTWARE_AGENT_ALLEGATION_MISMATCH',party['partyClass'],flag,flag_origin['pointer'],
                    {'inputRole':origins[id(party)],'pointer':'/partyClass'},flag_origin,equal=matches)
                # This same three-input predicate consumes the original posture
                # as well as class and flag. Retain that operand separately,
                # without presenting its internally derived Boolean as a source.
                comparisons.append({'predicateId':'PERFORMER_SOFTWARE_AGENT_ALLEGATION_CLAIM_POSTURE','pointer':flag_origin['pointer'],
                    'equal':matches,'source':{'inputRole':'EFFECT_INTENT','pointer':'/claimPosture','valueDigest':digest(intent['claimPosture'])},
                    'destination':{**flag_origin,'valueDigest':digest(flag)},'disposition':'PASS' if matches else 'FAIL'})
                observe_comparisons([comparisons[-1]], findings=['AR_SUBJECT_SCOPE_PROOF'] if gate == 'SUBJECT_SCOPE_RELATION' else ['AR_OPERATION_PERFORMER'])
                if software:
                    present=bool(party.get('agentInstanceRef'))
                    operands={'source':select_operand(party,'/agentInstanceRef',origins[id(party)]),
                              'destination':select_operand(party,'/partyClass',origins[id(party)])}
                    comparison={'predicateId':'SOFTWARE_PERFORMER_INSTANCE_LINK_MISSING','pointer':'/agentInstanceRef','equal':present}
                    if present:comparison.update(**operands,disposition='PASS')
                    else:comparison['operandAvailability']=operands
                    comparisons.append(comparison)
                    observe_comparisons([comparisons[-1]], findings=['AR_SUBJECT_SCOPE_PROOF'] if gate == 'SUBJECT_SCOPE_RELATION' else ['AR_OPERATION_PERFORMER'])
                    if not present:errors.append({'code':'SOFTWARE_PERFORMER_INSTANCE_LINK_MISSING','pointer':'/agentInstanceRef'})
                postures.append({'binding':performer,'partyClass':party['partyClass'],'partyState':party['partyState'],
                                 **({'agentInstanceRef':party['agentInstanceRef']} if software and party.get('agentInstanceRef') else {})})
        outputs[gate]={'disposition':'FAIL' if errors else 'NOT_EVALUATED' if missing else 'PASS',
                       'errors':errors,'remainingRoles':missing,'comparisons':comparisons,'sourceInputIds':sorted(set(ids)),
                       'sourceIdentityPostures':postures,'qualification':'Exact identity metadata comparison only; no active-state, principal, authority or admission conclusion.'}
    return outputs
