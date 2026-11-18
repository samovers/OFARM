"""Compare a complete typed occupancy allegation with reviewed R3 owner output.

UNQUALIFIED_OCCUPANCY requires each selected episode to cover the complete
query. UNQUALIFIED_EPISODES_DURING_WINDOW is a separate owned meaning: clean
qualified source support for an episode during the query, without asserting
continuous presence throughout it. Neither establishes actual completeness.
"""
from strict_inputs import same,digest


from domain_reader_occurrences import reader, owner_control, observe_comparisons


@reader('occupancy_sources.py', ['AR_BODY'])
def evaluate(atom,checked):
    errors,missing,comparisons=[],[],[]
    body=atom['body'];atom_id=atom['atomId']
    def claim(path):return {'inputRole':'ATOM:'+atom_id,'pointer':path}
    def compare(code,actual,expected,path,source=None,destination=None):
        equal=same(actual,expected)
        value={'predicateId':code,'pointer':path,'equal':equal,'actualValueDigest':digest(actual),'expectedValueDigest':digest(expected)}
        if source is not None and destination is not None:
            value.update(source={**source,'valueDigest':digest(actual)},destination={**destination,'valueDigest':digest(expected)},disposition='PASS' if equal else 'FAIL')
        comparisons.append(value)
        observe_comparisons([value])
        if not equal:errors.append({'code':code,'pointer':path})
    owner_control('OCCUPANCY_OWNER_INPUTS_AVAILABLE', 'occupancy:' + atom_id,
                  checked.get('report') if checked is not None else None, checked is not None, activate=checked is not None)
    if checked is None:missing.append({'role':'SELECTED_ORIGINAL_OCCUPANCY_OWNER_INPUTS','pointer':'/body/occupancyEvidence'})
    else:
        owner=checked['report']
        matched=owner['status']=='MATCHED_SELECTED_OCCUPANCY_EVIDENCE'
        if not matched:errors.append({'code':'OCCUPANCY_OWNER_COMPARISON_FAILED','pointer':'/body/occupancyEvidence','ownerStatus':owner['status']})
        if 'occupancyEvidence' not in body:errors.append({'code':'COMPLETE_OCCUPANCY_ALLEGATION_REQUIRED','pointer':'/body/occupancies'})
        else:
            allegation=body['occupancyEvidence']
            compare('OCCUPANCY_REQUEST_NOT_DERIVED_FROM_CLAIM',allegation,checked['request'],'/body/occupancyEvidence')
            compare('OCCUPANCY_CONTAINER_SELECTION_MISMATCH',allegation['selection']['place'],{'kind':'CONTAINER','binding':body['container']},'/body/occupancyEvidence/selection/place')
            subject=atom['scope']['subject']
            compare('OCCUPANCY_SUBJECT_SELECTION_MISMATCH',body['container'],{'ref':subject['subjectRef'],**{k:subject[k] for k in ['digest','revisionRef'] if k in subject}},'/scope/subject')
            time=atom['scope']['subjectTime'];window=allegation['selection']['applicability']
            if 'at' in time:compare('OCCUPANCY_AS_OF_TIME_MISMATCH',window,{'mode':'AS_OF','at':time['at']},'/body/occupancyEvidence/selection/applicability')
            elif 'end' in time:
                compare('OCCUPANCY_INTERVAL_MODE_MISMATCH',window['mode'],'INTERVAL','/body/occupancyEvidence/selection/applicability/mode')
                for key in ['start','end']:compare('OCCUPANCY_INTERVAL_TIME_MISMATCH',window.get(key),time[key],'/body/occupancyEvidence/selection/applicability/'+key)
            else:errors.append({'code':'FINITE_OCCUPANCY_SELECTION_CANNOT_SUPPORT_OPEN_SUBJECT_TIME','pointer':'/scope/subjectTime'})
            owner_control('OCCUPANCY_OWNER_MATCHED', 'occupancy:' + atom_id, owner, matched, activate=matched)
            if matched:
                context_id='occupancy:'+atom_id+':context'
                compare('OCCUPANCY_ORIGINAL_QUERY_SELECTION_MISMATCH',owner['selection'],allegation['selection'],'/body/occupancyEvidence/selection',
                    {'inputRole':context_id,'pointer':'/selection'},claim('/body/occupancyEvidence/selection'))
                for index,episode in enumerate(owner['episodes']):
                    prefix='/body/occupancyEvidence/episodes/'+str(index);facts=episode['facts']
                    if index<len(allegation['episodes']):
                        expected=allegation['episodes'][index]['expectedFacts'];source_id='occupancy:'+atom_id+':source:'+digest(episode['binding'])
                        for field,value in facts.items():
                            if field in expected:compare('OCCUPANCY_ORIGINAL_'+field.upper()+'_MISMATCH',value,expected[field],prefix+'/expectedFacts/'+field,
                                {'inputRole':source_id,'pointer':'/facts/'+field},claim(prefix+'/expectedFacts/'+field))
                    if body['occupancyClaimPosture']=='UNQUALIFIED_OCCUPANCY':
                        if not episode['selectedPostureSupportsUnqualifiedClaim']:
                            errors.append({'code':'UNQUALIFIED_OCCUPANCY_NOT_SUPPORTED_BY_SELECTED_SOURCE','pointer':prefix})
                    elif body['occupancyClaimPosture']=='UNQUALIFIED_EPISODES_DURING_WINDOW':
                        posture=facts['sourcePosture'];quantity=facts['occupiedQuantity']
                        amount=(episode['quantitySupportsUnqualifiedClaim'] if quantity['posture']=='REPORTED' else facts['occupiedCohort']['posture']=='IDENTIFIED')
                        okay=(episode['temporalCoverage']=='SUPPORTED' and episode['queryIntersection'] is not None and episode['coveredApplicability'] is not None
                            and episode['selectedWindowCoverage'] in ['FULL_WINDOW','PARTIAL_WINDOW'] and amount and facts['relevantExtent']['posture']!='UNRESOLVED'
                            and posture['validity']=='VALID' and posture['dispute']=='UNDISPUTED' and posture['revision'] in ['CURRENT','HISTORICAL_APPLICABLE'])
                        if not okay:errors.append({'code':'UNQUALIFIED_EPISODE_DURING_WINDOW_NOT_SUPPORTED_BY_SELECTED_SOURCE','pointer':prefix})
    # Container configuration is a distinct property, not established by an
    # occupancy report or by a continuity token naming the same container.
    missing.append({'role':'CONTAINER_REUSABLE_CONFIGURATION_SOURCE','pointer':'/body/reusable'})
    return {'scope':'COMPLETE_SELECTED_OCCUPANCY_FACTS','disposition':'FAIL' if errors else 'NOT_EVALUATED' if missing else 'PASS',
        'errors':errors,'remainingRoles':missing,'comparisons':comparisons,
        'sourceInputIds':(['occupancy:'+atom_id+':context']+['occupancy:'+atom_id+':source:'+digest(v['binding']) for v in checked['report']['episodes']]) if checked else [],'requiredReferences':[],
        'occupancyComparisonDisposition':'FAIL' if errors else 'NOT_EVALUATED' if checked is None else 'PASS',
        **({'ownerQualifications':checked['report']['qualifications'],'episodes':checked['report']['episodes'],
            'selectedQuery':checked['report'].get('selection'),'observationalHorizon':checked['report'].get('fixedAt'),
            'claimMeaning':body['occupancyClaimPosture'],'actualInventoryCompleteness':checked['report']['actualInventoryCompleteness']} if checked else {})}
