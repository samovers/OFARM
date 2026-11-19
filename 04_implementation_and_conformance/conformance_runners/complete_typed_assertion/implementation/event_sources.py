"""Domain association checks against an actually recomputed ingress selection.

This does not classify an event or prove occurrence. It binds the owner's
selected description to the exact claim context, preserves independent source
failures and never accepts a supplied report through the public interface.
"""
from pathlib import Path
from strict_inputs import same,digest,parse
HERE=Path(__file__).resolve().parent

# These are fixed semantic roles of the reviewed canonical cases. A compatible
# envelope alone never supplies a body predicate or physical completion fact.
REQUIRED_ROWS={
    'V04-boundary':{'S01','S09'},'V04-stand-count':{'C04'},'V04-hail':{'C01'},
    'V04-harvest':{'O06'},'V04-lot-split':{'O11','O15'},'V04-report-ingest':{'O23'},
    'V04-inspection':{'C08'},'V04-prune':{'O08'},'V04-spray':{'O01','O19'},
}


from domain_reader_occurrences import reader, selection as observe_selection, guard as observe_guard, origin as read_origin, observed_shape, owner_control, observe_comparisons, result_dependencies


@reader('event_sources.py', ['AR_EVENT_ASSOCIATION'])
def evaluate(intent,event,automatic,sources,schemas):
    from runtime_support import Values
    from intrinsics import time_bounds
    errors,missing,comparisons=[],[],[]
    result={'scope':'EVENT_DESCRIPTION_TO_DOMAIN_CLAIM_ONLY','sourceInputIds':['event:envelope','event:profile','event:context','event:proof'],'requiredReferences':[]}
    def finish():
        return {**result,'disposition':'FAIL' if errors else 'NOT_EVALUATED' if missing else 'PASS',
                'errors':errors,'remainingRoles':missing,'comparisons':comparisons,
                'qualification':'Original event description and selected domain comparisons only; no occurrence, accepted consequence, authority or runtime admission is inferred.'}
    def compare(code,actual,expected,source,destination,*,depends_on=()):
        equal=same(actual,expected)
        comparisons.append({'predicateId':code,'equal':equal,'pointer':source['pointer'],
            'source':{**source,'valueDigest':digest(actual)},'destination':{**destination,'valueDigest':digest(expected)},
            'disposition':'PASS' if equal else 'FAIL'})
        observe_comparisons([comparisons[-1]],depends_on=depends_on)
        if not equal:errors.append({'code':code,'pointer':source['pointer']})
    def check(code,equal,source=None,*,depends_on=()):
        fact={'predicateId':code,'disposition':'PASS' if equal else 'FAIL'}
        if source is not None:fact['source']=source
        return observe_comparisons([fact],depends_on=depends_on)
    binding=intent['associatedSemanticEventBinding']
    selected=[v for v in sources if same(v['binding'],binding)]
    envelope_read=observe_selection('SEMANTIC_EVENT_ENVELOPE', sources, selected, binding=binding,
        origins=[read_origin('EFFECT_INTENT', '/associatedSemanticEventBinding')])
    resolution_dependencies=[]
    if len(selected)==1:
        source=selected[0];original=source['record']
        if (not observed_shape(schemas, 'https://ofarm.dev/schema/semanticeventenvelope/v0.1',original)
                and original['semanticEventId']==binding['ref']
                and source['valueDigest']==digest(original)):
            result['selectedEnvelopeResolution']={'selectedBinding':binding,
                'resolvedBinding':{'ref':binding['ref'],'digest':source['valueDigest']},'sourceInputId':source['id']}
            result['sourceInputIds'].append(source['id'])
            resolved=observe_guard('EVENT_SELECTED_ENVELOPE_RESOLVED',True,
                origins=[read_origin(source['id'],'')],depends_on=[envelope_read] if envelope_read is not None else [])
            if resolved is not None:resolution_dependencies.append(resolved)
    owner_control('EVENT_OWNER_INPUTS_AVAILABLE', 'event', event.get('report') if event is not None else None,
                  event is not None, activate=event is not None)
    if event is None:
        missing.append({'role':'RECOMPUTED_EVENT_OWNER_ORIGINAL_INPUTS','pointer':'/associatedSemanticEventBinding'})
        return finish()
    envelope=event['envelope'];owner=event['report'];profile=event['profile']
    shape=observed_shape(schemas, 'https://ofarm.dev/schema/semanticeventenvelope/v0.1',envelope)
    errors.extend(shape)
    if shape:return finish()
    selected_digest=binding.get('digest') or result.get('selectedEnvelopeResolution',{}).get('resolvedBinding',{}).get('digest')
    digest_available=observe_guard('EVENT_ENVELOPE_DIGEST_AVAILABLE',bool(selected_digest),
        origins=[read_origin('EFFECT_INTENT','/associatedSemanticEventBinding/digest')],
        depends_on=[] if binding.get('digest') else resolution_dependencies)
    identity_matches=envelope['semanticEventId']==binding['ref']
    identity_guard=observe_guard('EVENT_OWNER_ENVELOPE_ID_MATCH',identity_matches,
        origins=[read_origin('event:envelope','/semanticEventId'),read_origin('EFFECT_INTENT','/associatedSemanticEventBinding/ref')])
    envelope_dependencies=[identity_guard] if identity_guard is not None else []
    digest_mismatch=False
    if identity_matches and selected_digest:
        digest_mismatch=digest(envelope)!=selected_digest
        digest_origins=[read_origin('event:envelope','')]
        if binding.get('digest'):digest_origins.append(read_origin('EFFECT_INTENT','/associatedSemanticEventBinding/digest'))
        matched=observe_guard('EVENT_OWNER_ENVELOPE_DIGEST_MATCH',not digest_mismatch,origins=digest_origins,
            depends_on=envelope_dependencies+([digest_available] if digest_available is not None else []))
        if matched is not None:envelope_dependencies.append(matched)
    envelope_mismatch=not identity_matches or digest_mismatch
    check('EVENT_OWNER_ENVELOPE_SELECTION_MISMATCH',not envelope_mismatch,depends_on=envelope_dependencies)
    if envelope_mismatch:
        errors.append({'code':'EVENT_OWNER_ENVELOPE_SELECTION_MISMATCH','pointer':'/associatedSemanticEventBinding'})
        return finish()
    if selected_digest is None:
        missing.append({'role':'EXACT_SELECTED_EVENT_ENVELOPE_ORIGINAL','pointer':'/associatedSemanticEventBinding'})
        return finish()
    owner_control('EVENT_OWNER_COMPARISON_PASS', 'event', owner,
                  owner.get('status') == 'CONDITIONAL_CONFORMANCE_PASS',
                  activate=owner.get('status') == 'CONDITIONAL_CONFORMANCE_PASS')
    if owner.get('status')!='CONDITIONAL_CONFORMANCE_PASS':
        missing.append({'role':'PASSING_PREVERDICT_EVENT_OWNER_COMPARISON','pointer':'/event/proof'})
        return finish()
    classification=owner['classification']
    result['envelopePrimaryFamily']=envelope['primaryEventFamily']
    candidates=[(n,c) for n,c in enumerate(profile['cases']) if c['caseId']==classification['caseId']]
    if len(candidates)!=1:
        errors.append({'code':'EVENT_OWNER_SELECTED_CASE_UNAVAILABLE','pointer':'/event/profile/cases'});return finish()
    n,classified=candidates[0]
    for field,owner_field in [('primaryEventFamily','authoritativePrimaryFamily'),('dominantSemanticConsequence','dominantSemanticConsequence')]:
        compare('EVENT_SELECTED_OWNER_'+field.upper()+'_MISMATCH',envelope[field],classified[owner_field],
                {'inputRole':'event:envelope','pointer':'/'+field},
                {'inputRole':'event:profile','pointer':'/cases/'+str(n)+'/'+owner_field})
    definitions=parse((HERE/'domain-definitions.json').read_bytes())['definitions']
    definitions_read=check('EVENT_CANONICAL_DEFINITION_ARRAY_READ',True,
        read_origin('DOMAIN_DEFINITIONS','/definitions'))
    from event_definition_inputs import select
    selection=select(intent,sources,schemas,definitions)
    case_dependencies=result_dependencies(selection,'EVENT_CASE_DEFINITION',producer='event_definition_inputs.py')
    use_dependencies=result_dependencies(selection,'EVENT_USE_SELECTION',producer='event_definition_inputs.py')
    use_dependencies+=result_dependencies(selection,'EVENT_CASE_UNAVAILABLE',producer='event_definition_inputs.py')
    errors.extend(selection['errors']);missing.extend(selection['remainingRoles'])
    result['requiredReferences'].extend(selection['requiredReferences'])
    result['sourceInputIds'].extend(selection['sourceInputIds'])
    matching=[]
    for index,definition in enumerate(definitions):
        row=definition['id']
        if row not in REQUIRED_ROWS:continue
        source=definition['sourceDefinition'];presence='PRESENT' if 'eventSubtypeId' in envelope else 'ABSENT'
        case=source.get('typedRepresentation',{}).get('eventMeaningCase',{}) if presence=='PRESENT' else source.get('subtypeAbsentVariant',{})
        if case.get('subtypePresence')==presence and case.get('eventSubtypeId')==envelope.get('eventSubtypeId') and case.get('dominantSemanticConsequence')==envelope['dominantSemanticConsequence']:
            matching.append((index,definition,case,presence))
    presence_dependencies=[]
    if selection['definition'] is not None:
        definition=selection['definition'];index=definitions.index(definition) if 'extensionRecord' not in definition else -1
        presence=selection['subtypePresence']
        use_ref=next(v for v in selection['requiredReferences'] if v['role']=='EXACT_EVENT_USE_DEFINITION')
        use_source=next(v for v in sources if same(v['binding'],use_ref['binding']) and v['id'] in selection['sourceInputIds'])
        presence_matches=presence==('PRESENT' if 'eventSubtypeId' in envelope else 'ABSENT')
        presence_guard=observe_guard('EVENT_SELECTED_SUBTYPE_PRESENCE',presence_matches,
            origins=[read_origin(use_source['id'],'/subtypePresence'),read_origin('event:envelope','/eventSubtypeId')],
            depends_on=case_dependencies)
        if presence_guard is not None:presence_dependencies.append(presence_guard)
        check('EVENT_SELECTED_SUBTYPE_PRESENCE_MISMATCH',presence_matches,
            depends_on=[presence_guard] if presence_guard is not None else [])
        if not presence_matches:
            errors.append({'code':'EVENT_SELECTED_SUBTYPE_PRESENCE_MISMATCH','pointer':'/eventSubtypeId'})
        source=definition['sourceDefinition']
        case=source['typedRepresentation']['eventMeaningCase'] if presence=='PRESENT' else source.get('subtypeAbsentVariant',{})
        matching=[(index,definition,case,presence)]
        result['meaningDefinitionSelection']={k:selection[k] for k in ['useDefinitionBinding','vocabularyDefinitionBinding','packDefinitionBinding'] if k in selection}
    case_cardinality=observe_guard('EVENT_DOMAIN_CASE_UNIQUE',len(matching)==1,
        origins=[read_origin('event:envelope','/eventSubtypeId'),read_origin('event:envelope','/dominantSemanticConsequence')],
        depends_on=definitions_read+case_dependencies+use_dependencies)
    if case_cardinality is not None:case_dependencies.append(case_cardinality)
    if len(matching)!=1:
        missing.append({'role':'EXACT_VERSIONED_DOMAIN_EVENT_EXTENSION_DEFINITION','pointer':'/event'})
        if len(matching)>1:errors.append({'code':'AMBIGUOUS_DOMAIN_EVENT_CASE','pointer':'/event'})
        return finish()
    index,definition,case,presence=matching[0];row=definition['id']
    result['canonicalRow']=row
    result['caseDefinitionBinding']=selection.get('caseDefinitionBinding') or {'ref':definition['definitionRef'],'digest':digest(definition)}
    base='/definitions/'+str(index)+'/sourceDefinition/'+('typedRepresentation/eventMeaningCase' if presence=='PRESENT' else 'subtypeAbsentVariant')
    def case_origin(field):
        if 'extensionRecord' in definition:
            return {'inputRole':definition['extensionSourceId'],'pointer':'/'+('primaryFamily' if field=='primaryFamilyFromSource' else field)}
        return {'inputRole':'DOMAIN_DEFINITIONS','pointer':base+'/'+field}
    required_case_origin=(read_origin(definition['extensionSourceId'],'/caseKind') if 'extensionRecord' in definition
        else read_origin('DOMAIN_DEFINITIONS','/definitions/'+str(index)+'/id'))
    required_case=check('EVENT_REQUIRED_BODY_CASE',True,required_case_origin,depends_on=case_dependencies)
    if selection['definition'] is None:
        # The actual fallback chose this pinned case; full scan coverage remains separate.
        fallback=observe_guard('EVENT_FALLBACK_CASE_SELECTED',True,
            origins=[read_origin('event:envelope','/eventSubtypeId'),read_origin('event:envelope','/dominantSemanticConsequence')],
            depends_on=required_case+use_dependencies)
        if fallback is not None:case_dependencies.append(fallback)
    body_dependencies=case_dependencies+required_case
    for field in ['dominantSemanticConsequence']+(['eventSubtypeId'] if presence=='PRESENT' else []):
        field_present=field in envelope
        field_dependencies=body_dependencies+(presence_dependencies if field=='eventSubtypeId' else [])
        field_guard=observe_guard('EVENT_SELECTED_FIELD_PRESENT:'+field,field_present,
            origins=[read_origin('event:envelope','/'+field)],depends_on=field_dependencies)
        if field_guard is not None:field_dependencies=field_dependencies+[field_guard]
        if not field_present:
            check('EVENT_SELECTED_SUBTYPE_VALUE_MISSING',False,read_origin('event:envelope','/'+field),
                depends_on=field_dependencies)
            errors.append({'code':'EVENT_SELECTED_SUBTYPE_VALUE_MISSING','pointer':'/'+field});continue
        compare('EVENT_DOMAIN_'+field.upper()+'_MISMATCH',envelope[field],case[field],
                {'inputRole':'event:envelope','pointer':'/'+field},
                case_origin(field),depends_on=field_dependencies)
    if 'primaryFamilyFromSource' in case:
        compare('EVENT_DOMAIN_FAMILY_MISMATCH',envelope['primaryEventFamily'],case['primaryFamilyFromSource'],
                {'inputRole':'event:envelope','pointer':'/primaryEventFamily'},
                case_origin('primaryFamilyFromSource'),depends_on=body_dependencies)
    elif row in ['V04-prune','V04-spray']:
        from common import source as historical_source
        fragment='OFARM_SemanticEventEnvelope_example_pruning_operation' if row=='V04-prune' else 'OFARM_SemanticEventEnvelope_example_field_17_contractor_spot_spray_late_sync'
        pins=parse((HERE/'components/revision-02/source-pins.json').read_bytes())['sources']
        pin=next(p for p in pins if fragment in p['originalPath'])
        original=historical_source(pin['originalPath'],pin['commit'],pin['repository'])
        compare('EVENT_DOMAIN_FAMILY_MISMATCH',envelope['primaryEventFamily'],original['primaryEventFamily'],
                {'inputRole':'event:envelope','pointer':'/primaryEventFamily'},
                {'inputRole':'PINNED_CANONICAL_SOURCE:'+pin['localPath'],'pointer':'/primaryEventFamily'},
                depends_on=body_dependencies)
    atom_traversal_origins=[]
    def atoms(p,path='/assertionBody/proposition'):
        atom_traversal_origins.append(read_origin('EFFECT_INTENT',path+'/form'))
        if p['form']=='ATOM':return [p]
        atom_traversal_origins.append(read_origin('EFFECT_INTENT',path+'/child'))
        if 'child' in p:return atoms(p['child'],path+'/child')
        atom_traversal_origins.append(read_origin('EFFECT_INTENT',path+'/children'))
        return [a for n,c in enumerate(p['children']) for a in atoms(c,path+'/children/'+str(n))]
    positive_origins=[]
    def positive_rows(p,negated=False,path='/assertionBody/proposition'):
        positive_origins.append(read_origin('EFFECT_INTENT',path+'/form'))
        if p['form']=='ATOM':
            if not negated:positive_origins.append(read_origin('EFFECT_INTENT',path+'/definition'))
            return set() if negated else {p['definition'].split(':')[-1]}
        if p['form']=='NOT':return positive_rows(p['child'],not negated,path+'/child')
        if p['form']=='QUALIFIED':return positive_rows(p['child'],negated,path+'/child')
        sets=[positive_rows(c,negated,path+'/children/'+str(n)) for n,c in enumerate(p['children'])]
        # De Morgan's transformation preserves mandatory positive roles. No
        # missing source is treated as evidence for a negated proposition.
        intersection=(p['form']=='ANY')!=negated
        return set.intersection(*sets) if intersection else set.union(*sets)
    proposition=intent['assertionBody']['proposition'];all_atoms=atoms(proposition);positive=positive_rows(proposition)
    atoms_traversed=observe_guard('EVENT_BODY_ATOMS_TRAVERSED',True,origins=atom_traversal_origins)
    atom_dependencies=body_dependencies+([atoms_traversed] if atoms_traversed is not None else [])
    required=({'O08'} if case['concept']=='PRUNING_COMPLETION' else {'O22'}) if row=='V04-extension' else REQUIRED_ROWS[row]
    body_matches=bool(required & positive) if row=='V04-spray' else required<=positive
    body_guard=observe_guard('EVENT_POSITIVE_BODY_MEANING',body_matches,origins=positive_origins,depends_on=body_dependencies)
    check('EVENT_DESCRIPTION_DOES_NOT_MATCH_POSITIVE_BODY_MEANING',body_matches,
        depends_on=[body_guard] if body_guard is not None else [])
    if not body_matches:
        errors.append({'code':'EVENT_DESCRIPTION_DOES_NOT_MATCH_POSITIVE_BODY_MEANING','pointer':'/assertionBody/proposition'})
    relevance={}
    def relevant_atom(atom):
        matches=atom['definition'].split(':')[-1] in required
        relevance[id(atom)]=observe_guard('EVENT_RELEVANT_ATOM:'+atom['atomId'],matches,
            origins=[read_origin('ATOM:'+atom['atomId'],'/definition')],depends_on=atom_dependencies)
        return matches
    relevant=[a for a in all_atoms if relevant_atom(a)]
    result['associatedAtomIds']=[a['atomId'] for a in relevant]
    if row=='V04-extension':
        required_facet='COMPLETED' if case['concept']=='PRUNING_COMPLETION' else 'IN_PROGRESS'
        for atom in relevant:
            atom_dependencies=body_dependencies+([relevance[id(atom)]] if relevance[id(atom)] is not None else [])
            facet_matches=atom['body']['performanceFacet']==required_facet
            facet_guard=observe_guard('EVENT_EXTENSION_WORK_FACET:'+atom['atomId'],facet_matches,
                origins=[required_case_origin,read_origin('ATOM:'+atom['atomId'],'/body/performanceFacet')],
                depends_on=atom_dependencies)
            check('EVENT_EXTENSION_WORK_FACET_MISMATCH',facet_matches,
                depends_on=[facet_guard] if facet_guard is not None else [])
            if not facet_matches:
                errors.append({'code':'EVENT_EXTENSION_WORK_FACET_MISMATCH','pointer':'/assertionBody/proposition'})
            analysis_case=case['concept']=='ANALYSIS_WORK_IN_PROGRESS_PENDING_OUTPUT'
            analysis_guard=observe_guard('EVENT_EXTENSION_PENDING_OUTPUT_APPLICABLE:'+atom['atomId'],analysis_case,
                origins=[required_case_origin],depends_on=atom_dependencies)
            if analysis_case:
                output=atom['body']['parameters']['producedResult']
                pending_role=output['role']=='PENDING_OUTPUT'
                role_guard=observe_guard('EVENT_EXTENSION_PENDING_OUTPUT_ROLE:'+atom['atomId'],pending_role,
                    origins=[read_origin('ATOM:'+atom['atomId'],'/body/parameters/producedResult/role')],
                    depends_on=[analysis_guard] if analysis_guard is not None else [])
                output_dependencies=[role_guard] if role_guard is not None else []
                output_matches=False
                if pending_role:
                    output_matches=output.get('outputState')=='NOT_YET_PRODUCED'
                    state_guard=observe_guard('EVENT_EXTENSION_PENDING_OUTPUT_STATE:'+atom['atomId'],output_matches,
                        origins=[read_origin('ATOM:'+atom['atomId'],'/body/parameters/producedResult/outputState')],
                        depends_on=output_dependencies)
                    if state_guard is not None:output_dependencies.append(state_guard)
                check('EVENT_EXTENSION_PENDING_ANALYSIS_OUTPUT_MISMATCH',output_matches,
                    depends_on=output_dependencies)
                if not output_matches:
                    errors.append({'code':'EVENT_EXTENSION_PENDING_ANALYSIS_OUTPUT_MISMATCH','pointer':'/assertionBody/proposition'})
    if row=='V04-boundary' and any(a['body'].get('case')!='REVISION_ONLY' for a in relevant if a['definition'].endswith(':S09')):
        errors.append({'code':'BOUNDARY_REVISION_EVENT_REQUIRES_SAME_IDENTITY_REVISION','pointer':'/assertionBody/proposition'})
    if row=='V04-lot-split' and any(a['body']['parameters'].get('movementPhase')!='DISPATCH' for a in relevant if a['definition'].endswith(':O15')):
        errors.append({'code':'SPLIT_DISPATCH_EVENT_REQUIRES_DISPATCH_PHASE','pointer':'/assertionBody/proposition'})
    posture_scan=[]
    def intended_atom(atom):
        intended=atom['body'].get('claimPosture')=='INTENDED'
        observed=observe_guard('EVENT_BODY_POSTURE:'+atom['atomId'],intended,
            origins=[read_origin('ATOM:'+atom['atomId'],'/body/claimPosture')],
            depends_on=body_dependencies+([relevance[id(atom)]] if relevance[id(atom)] is not None else []))
        if observed is not None:posture_scan.append(observed)
        return intended
    intended=any(intended_atom(a) for a in relevant)
    intended_guard=observe_guard('EVENT_INTENDED_BODY_PRESENT',intended,
        depends_on=body_dependencies+[v for v in relevance.values() if v is not None]+posture_scan)
    check('INTENDED_BODY_CANNOT_USE_PERFORMED_EVENT_CASE',not intended,
        depends_on=[intended_guard] if intended_guard is not None else [])
    if intended:
        errors.append({'code':'INTENDED_BODY_CANNOT_USE_PERFORMED_EVENT_CASE','pointer':'/assertionBody/proposition'})
    subject=intent['subject'];anchor=intent['resources'][0]['scope']
    subject_indices=[n for n,v in enumerate(envelope['subjectRefs']) if v==subject['subjectRef']]
    anchor_projection={k:anchor[k] for k in ['scopeType','scopeRef']}
    anchor_scan=[]
    def anchor_matches(n,value):
        matched=same(value,anchor_projection)
        observed=observe_guard('EVENT_ANCHOR_PAIR_MEMBER:'+str(n),matched,
            origins=[read_origin('event:envelope','/anchorScopes/'+str(n)),
                     read_origin('EFFECT_INTENT','/resources/0/scope/scopeType'),
                     read_origin('EFFECT_INTENT','/resources/0/scope/scopeRef')])
        if observed is not None:anchor_scan.append(observed)
        return matched
    anchor_indices=[n for n,v in enumerate(envelope['anchorScopes']) if anchor_matches(n,v)]
    anchor_present=observe_guard('EVENT_ANCHOR_PAIR_PRESENT',bool(anchor_indices),
        origins=[read_origin('event:envelope','/anchorScopes')],depends_on=anchor_scan)
    anchor_dependencies=[anchor_present] if anchor_present is not None else []
    observe_comparisons([{'predicateId':'EVENT_ANCHOR_PAIR_NOT_PRESENT',
        'disposition':'PASS' if anchor_indices else 'FAIL'}],depends_on=anchor_dependencies)
    if subject_indices:
        index=subject_indices[0];result['directSubjectIndex']=index
        compare('EVENT_DIRECT_SUBJECT_MISMATCH',envelope['subjectRefs'][index],subject['subjectRef'],
                {'inputRole':'event:envelope','pointer':'/subjectRefs/'+str(index)},
                {'inputRole':'EFFECT_INTENT','pointer':'/subject/subjectRef'})
    else:
        from event_relation_sources import evaluate as relation_sources
        relation_definition=next((n,d) for n,d in enumerate(definitions) if d['id']=='V06-operation-target')
        relation=relation_sources(intent,envelope,relevant,automatic,sources,schemas,
            {'index':relation_definition[0],'binding':{'ref':relation_definition[1]['definitionRef'],'digest':digest(relation_definition[1])}})
        if not relation['candidates'] and not relation['errors']:
            from event_extent_sources import evaluate as extent_sources
            extent_definition=next(d for d in definitions if d['id']=='V06-extent')
            extent_relation=extent_sources(intent,envelope,relevant,automatic,sources,schemas,
                {'binding':{'ref':extent_definition['definitionRef'],'digest':digest(extent_definition)}},
                temporal_meanings=selection.get('selectedExtentTemporalMeanings',[]))
            if extent_relation['candidates'] or extent_relation['errors'] or extent_relation['remainingRoles']:
                relation=extent_relation
        result['directedSubjectRelation']=relation
        errors.extend(relation['errors']);missing.extend(relation['remainingRoles']);comparisons.extend(relation['comparisons'])
        result['sourceInputIds'].extend(relation['sourceInputIds']);result['requiredReferences'].extend(relation['requiredReferences'])
        if not relation['mandatoryOriginalRelationEstablished']:
            missing.append({'role':'EXACT_DIRECTED_EVENT_SUBJECT_RELATION','pointer':'/subjectScopeProofBindings'})
    if anchor_indices:
        index=anchor_indices[0];result['directAnchorIndex']=index
        for field in ['scopeType','scopeRef']:
            compare('EVENT_DIRECT_ANCHOR_'+field.upper()+'_MISMATCH',envelope['anchorScopes'][index][field],anchor[field],
                    {'inputRole':'event:envelope','pointer':'/anchorScopes/'+str(index)+'/'+field},
                    {'inputRole':'EFFECT_INTENT','pointer':'/resources/0/scope/'+field},depends_on=anchor_dependencies)
    else:errors.append({'code':'EVENT_ANCHOR_PAIR_NOT_PRESENT','pointer':'/resources/0/scope'})
    time=intent['subjectTime'];profile_name=time['profile']
    if profile_name=='INTENDED_WINDOW':
        errors.append({'code':'INTENDED_EVENT_ASSOCIATION_PROHIBITED','pointer':'/subjectTime'})
    else:
        if profile_name.endswith('INTERVAL'):
            selector=['/timeSemantics/effectiveFrom','/timeSemantics/effectiveUntil']
        elif profile_name.endswith('EFFECTIVE_FROM'):
            selector='/timeSemantics/effectiveFrom'
        elif profile_name.startswith('STRUCTURE'):
            selector='/timeSemantics/effectiveFrom'
        elif row in ['V04-stand-count','V04-inspection']:
            selector='/timeSemantics/'+('observationTime' if row=='V04-stand-count' else 'decisionTime')
        else:selector='/timeSemantics/eventTime'
        result['selectedTimeSelector']=selector
        time_route=observe_guard('EVENT_TIME_SELECTOR_SELECTED',True,
            origins=[read_origin('EFFECT_INTENT','/subjectTime/profile')],depends_on=body_dependencies)
        time_dependencies=body_dependencies+([time_route] if time_route is not None else [])
        time_errors=Values(schemas).event_time_errors(time,envelope,selector)
        errors.extend(time_errors)
        if any(e.get('code')=='EMPTY_OR_REVERSED_INTERVAL' and e.get('pointer')=='' for e in time_errors):
            observe_comparisons([{'predicateId':'EMPTY_OR_REVERSED_INTERVAL','disposition':'FAIL',
                'source':read_origin('EFFECT_INTENT','/subjectTime/start'),
                'destination':read_origin('EFFECT_INTENT','/subjectTime/end')}],depends_on=time_dependencies)
        from strict_inputs import pointer
        for claim_field,source_pointer in (list(zip(['start','end'],selector)) if isinstance(selector,list) else [('start' if profile_name.endswith('EFFECTIVE_FROM') else 'at',selector)]):
            try:
                original=pointer(envelope,source_pointer)
            except ValueError:
                available=observe_guard('EVENT_TIME_SOURCE_AVAILABLE:'+claim_field.upper(),False,
                    origins=[read_origin('event:envelope',source_pointer)],depends_on=time_dependencies)
                if any(e.get('code')=='EVENT_TIME_MISMATCH' and e.get('pointer')==source_pointer for e in time_errors):
                    observe_comparisons([{'predicateId':'EVENT_TIME_MISMATCH','disposition':'FAIL',
                        'source':read_origin('event:envelope',source_pointer),
                        'destination':read_origin('EFFECT_INTENT','/subjectTime/'+claim_field)}],
                        depends_on=time_dependencies+([available] if available is not None else []))
                continue
            if claim_field in time:
                compare('EVENT_DOMAIN_TIME_'+claim_field.upper()+'_MISMATCH',original,time[claim_field],
                        {'inputRole':'event:envelope','pointer':source_pointer},
                        {'inputRole':'EFFECT_INTENT','pointer':'/subjectTime/'+claim_field},depends_on=time_dependencies)
    if row=='V04-inspection':
        missing.append({'role':'EXACT_EVENT_CONDITION_OR_DECISION_CONCEPT:'+case['concept'],'pointer':'/assertionBody/proposition'})
    if row=='V04-stand-count':
        from event_observation_sources import evaluate as observation_sources
        observation=observation_sources(intent,envelope,relevant,automatic,sources,selection,case_origin('concept'))
        result['observationMeaningComparison']=observation
        errors.extend(observation['errors']);missing.extend(observation['remainingRoles']);comparisons.extend(observation['comparisons'])
        result['sourceInputIds'].extend(observation['sourceInputIds']);result['requiredReferences'].extend(observation['requiredReferences'])
    checked={a['atomId']:a for a in automatic.get('atoms',[])}
    if row=='V04-hail':
        matched_ids=set();candidates=[]
        for atom in relevant:
            finding=checked.get(atom['atomId'],{})
            selected=finding.get('sourceInterpretation',{}).get('selectedRelevanceMeaning')
            if selected is None:continue
            matching=(selected['concept']==case['concept']
                and same(selected['basisBinding'],intent['associatedSemanticEventBinding'])
                and selected['basisValueDigest']==digest(envelope)
                and selected['basisRawSha256']==event.get('envelopeRawSha256')
                and not finding.get('errors'))
            candidates.append({'atomId':atom['atomId'],'basisBinding':selected['basisBinding'],
                               'basisRawSha256':selected['basisRawSha256'],
                               'associatedEnvelopeRawSha256':event.get('envelopeRawSha256'),
                               'concept':selected['concept'],'matchesAssociatedEvent':matching})
            if not matching:continue
            matched_ids.add(atom['atomId'])
            compare('EVENT_HAIL_RELEVANCE_CONCEPT_MISMATCH',selected['concept'],case['concept'],
                    selected['conceptOrigin'],case_origin('concept'))
            for field in ['ref','revisionRef','digest']:
                if field in atom['body']['basis']:
                    compare('EVENT_HAIL_EXACT_BASIS_'+field.upper()+'_MISMATCH',atom['body']['basis'][field],intent['associatedSemanticEventBinding'][field],
                        {'inputRole':'EFFECT_INTENT','pointer':finding['pointer']+'/body/basis/'+field},
                        {'inputRole':'EFFECT_INTENT','pointer':'/associatedSemanticEventBinding/'+field})
        from event_relation_sources import mandatory_positive
        result['eventConceptCandidates']=candidates
        result['eventConceptMatchedAtomIds']=sorted(matched_ids)
        if not candidates:
            missing.append({'role':'EXACT_EVENT_CONDITION_OR_DECISION_CONCEPT:'+case['concept'],'pointer':'/assertionBody/proposition'})
        elif not mandatory_positive(proposition,matched_ids):
            errors.append({'code':'EVENT_HAIL_EXACT_POSITIVE_BASIS_NOT_ESTABLISHED','pointer':'/assertionBody/proposition'})
    for atom in relevant:
        finding=checked.get(atom['atomId'])
        if finding is None:
            missing.append({'role':'COMPLETE_EVENT_BODY_SOURCE:'+atom['atomId'],'pointer':'/assertionBody/proposition'})
            continue
        errors.extend(finding['errors'])
        missing.extend({'role':'EVENT_BODY:'+v['role'],'pointer':v['pointer']} for v in finding['remainingRoles'])
        request=finding.get('derivedRequest')
        request_available=bool(request and request['operation']=='operationSource')
        request_dependencies=result_dependencies(finding,'EVENT_OPERATION_SELECTION',
            producer='source_derivation.py',scope=atom['atomId'])
        source_identity_dependencies=result_dependencies(finding,'EVENT_OPERATION_SOURCE_IDENTITY',
            producer='source_derivation.py',scope=atom['atomId'])
        carrier_dependencies=(result_dependencies(request['input']['source'],'EVENT_OPERATION_CARRIER',
            producer='source_derivation.py',scope=atom['atomId']) if request_available else [])
        request_guard=observe_guard('EVENT_OPERATION_REQUEST:'+atom['atomId'],request_available,
            origins=[read_origin('ATOM:'+atom['atomId'],'/definition'),read_origin('ATOM:'+atom['atomId'],'/body/claimPosture')],
            depends_on=body_dependencies+request_dependencies+source_identity_dependencies+carrier_dependencies+([relevance[id(atom)]] if relevance[id(atom)] is not None else []))
        if request_available:
            source=request['input']['source'];kind=request['input']['sourceKind']
            field='interventionIntentPayloadRefs' if kind=='intent' else 'executionRecordPayloadRefs'
            declared_field='interventionIntentPayloadBindings' if kind=='intent' else 'executionRecordPayloadBindings'
            declared=intent['assertionBody'].get(declared_field,[])
            selector_indices=[n for n,b in enumerate(declared)
                if same({k:b[k] for k in ['ref','revisionRef','digest'] if k in b},source['binding'])]
            selector_origins=([read_origin('EFFECT_INTENT','/assertionBody/'+declared_field+'/'+str(selector_indices[0])+'/'+key)
                for key in ['ref','revisionRef','digest'] if key in declared[selector_indices[0]]] if selector_indices else [])
            selector_guard=observe_guard('EVENT_OPERATION_DECLARED_SELECTOR:'+atom['atomId'],bool(selector_indices),
                origins=selector_origins,depends_on=carrier_dependencies+([request_guard] if request_guard is not None else []))
            link_dependencies=[selector_guard] if selector_guard is not None else []
            link_scan=[]
            def linked_payload(n,value):
                linked=value==source['binding']['ref']
                observed=observe_guard('EVENT_OPERATION_PAYLOAD_MEMBER:'+atom['atomId']+':'+str(n),linked,
                    origins=[read_origin('event:envelope','/'+field+'/'+str(n))]+selector_origins,depends_on=link_dependencies)
                if observed is not None:link_scan.append(observed)
                return linked
            linked=any(linked_payload(n,value) for n,value in enumerate(envelope.get(field,[])))
            link_guard=observe_guard('EVENT_OPERATION_PAYLOAD_LINK:'+atom['atomId'],linked,
                origins=[read_origin('event:envelope','/'+field)],depends_on=link_dependencies+link_scan)
            check('EVENT_SELECTED_OPERATION_PAYLOAD_LINK_MISSING',linked,
                depends_on=[link_guard] if link_guard is not None else [])
            if not linked:
                errors.append({'code':'EVENT_SELECTED_OPERATION_PAYLOAD_LINK_MISSING','pointer':'/event/'+field})
    return finish()
