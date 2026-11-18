"""Owned normative event meaning packages; no foreign pack admission is created."""
from definition_inputs import schema,obj,BINDING,TEXT,EXTENT_TEMPORAL_MEANING,register as register_base

CASES=['V04-boundary','V04-stand-count','V04-hail','V04-harvest','V04-lot-split','V04-report-ingest','V04-inspection','V04-prune','V04-spray']
SCHEMAS={
 'eventExtension':schema('event-extension-definition','ofarm.assertionDomainEventExtensionDefinition.v0.1',{
    'caseKind':{'enum':['PRUNING_COMPLETION','ANALYSIS_WORK_IN_PROGRESS_PENDING_OUTPUT']},
    'subtypePresence':{'enum':['PRESENT','ABSENT']},
    'eventSubtypeId':{'type':['string','null']},'dominantSemanticConsequence':TEXT,
    'primaryFamily':{'enum':['StructureEvent','ObservationEvent','OccurrenceEvent','InterventionEvent','MaterialEvent','EvidenceEvent','GovernanceEvent']},
    'vocabularyRevision':TEXT,'sourcePackRef':{'type':['string','null']},
 }),
 'eventUse':schema('event-use-definition','ofarm.assertionDomainEventUseDefinition.v0.1',{
    'envelopeBinding':BINDING,'canonicalCaseBinding':BINDING,
    'subtypePresence':{'enum':['PRESENT','ABSENT']},
    'vocabularyDefinitionBinding':BINDING,'packDefinitionBinding':BINDING,
    'observationMeasurementBinding':BINDING,
    'extentTemporalMeanings':{'type':'array','minItems':1,'uniqueItems':True,'items':EXTENT_TEMPORAL_MEANING},
 }),
 'eventVocabulary':schema('event-vocabulary-definition','ofarm.assertionDomainEventVocabularyDefinition.v0.1',{
    'vocabularyRevision':TEXT,'caseBindings':{'type':'array','minItems':1,'uniqueItems':True,'items':BINDING},
 }),
 'eventPack':schema('event-meaning-pack-definition','ofarm.assertionDomainEventMeaningPackDefinition.v0.1',{
    'sourcePackRef':{'type':['string','null']},'vocabularyDefinitionBinding':BINDING,
    'caseBindings':{'type':'array','minItems':1,'uniqueItems':True,'items':BINDING},
    'scope':{'const':'DOMAIN_MEANING_SELECTION_ONLY'},
 }),
}
SCHEMAS['eventUse']['required'].remove('observationMeasurementBinding')
SCHEMAS['eventUse']['required'].remove('extentTemporalMeanings')


def register(schemas):
    from referencing import Resource
    register_base(schemas)
    for value in SCHEMAS.values():
        schemas.schemas[value['$id']]=value
        schemas.registry=schemas.registry.with_resource(value['$id'],Resource.from_contents(value))


from domain_reader_occurrences import reader, selection as observe_selection, guard as observe_guard, origin as read_origin, observed_shape, predicate_value, guard_refs, observe_comparisons, register_result_dependencies


@reader('event_definition_inputs.py', ['AR_EVENT_ASSOCIATION'])
def select(intent,sources,schemas,definitions):
    from strict_inputs import same,digest,distinct_selected_originals
    register(schemas)
    errors,missing,refs,ids=[],[],[],[]
    resolved={}
    result={'errors':errors,'remainingRoles':missing,'requiredReferences':refs,'sourceInputIds':ids,'definition':None}
    pre_case_dependencies=[]
    def unavailable_case():
        register_result_dependencies(result,'EVENT_CASE_UNAVAILABLE',
            [value for value in pre_case_dependencies if value is not None])
        return result
    def original(kind,path):
        return read_origin(resolved[kind]['id'],path)
    def check(code,equal,source,destination=None,*,depends_on=()):
        fact={'predicateId':code,'source':source,'disposition':'PASS' if equal else 'FAIL'}
        if destination is not None:fact['destination']=destination
        return observe_comparisons([fact],depends_on=depends_on)
    def resolve(binding,kind,role,origins):
        refs.append({'binding':binding,'role':role,'pointer':'/eventDefinition/'+role})
        matches=[s for s in sources if same(s['binding'],binding)]
        resolution=observe_selection(role, sources, matches, binding=binding, origins=origins)
        if kind in ('eventUse','eventExtension'):pre_case_dependencies.append(resolution)
        if len(matches)!=1:
            missing.append({'role':role,'pointer':'/eventDefinition/'+role});return None
        item=matches[0];ids.append(item['id']);value=item['record'];resolved[kind]=item
        shape=observed_shape(schemas, SCHEMAS[kind]['$id'],value);errors.extend(shape)
        if kind in ('eventUse','eventExtension'):
            pre_case_dependencies.append(observe_guard('EVENT_PRE_CASE_SOURCE_SHAPE:'+kind,not shape,
                origins=[read_origin(item['id'],'')],
                depends_on=[resolution] if resolution is not None else []))
        if shape:return None
        identity_matches=value['definitionId']==binding['ref']
        check('EVENT_DEFINITION_IDENTITY_MISMATCH',identity_matches,original(kind,'/definitionId'))
        if not identity_matches:
            errors.append({'code':'EVENT_DEFINITION_IDENTITY_MISMATCH','pointer':'/definitionId'})
        return value
    matches=[s for s in sources if 'selectorMapping' in s and predicate_value(s, '', isinstance(s['record'],dict), 'EVENT_USE_DEFINITION')
             and predicate_value(s, '/schemaVersion', s['record'].get('schemaVersion'), 'EVENT_USE_DEFINITION')=='ofarm.assertionDomainEventUseDefinition.v0.1'
             and same(predicate_value(s, '/envelopeBinding', s['record'].get('envelopeBinding'), 'EVENT_USE_DEFINITION'),intent['associatedSemanticEventBinding'])]
    matches=distinct_selected_originals(matches)
    use_selection=observe_selection('EVENT_USE_DEFINITION', sources, matches,
        origins=[read_origin('EFFECT_INTENT', '/associatedSemanticEventBinding')])
    pre_case_dependencies.append(use_selection)
    register_result_dependencies(result,'EVENT_USE_SELECTION',[use_selection])
    if len(matches)!=1:
        missing.append({'role':'INDEPENDENT_EVENT_USE_DEFINITION','pointer':'/associatedSemanticEventBinding'})
        if len(matches)>1:
            check('AMBIGUOUS_EVENT_USE_DEFINITION',False,read_origin('EFFECT_INTENT','/associatedSemanticEventBinding'),
                depends_on=[use_selection] if use_selection is not None else [])
            errors.append({'code':'AMBIGUOUS_EVENT_USE_DEFINITION','pointer':'/eventDefinition'})
        return unavailable_case()
    use=resolve(matches[0]['binding'],'eventUse','EXACT_EVENT_USE_DEFINITION',
        [read_origin('EFFECT_INTENT', '/associatedSemanticEventBinding')])
    if use is None:return unavailable_case()
    result['subtypePresence']=use['subtypePresence']
    selected=use['canonicalCaseBinding']
    cases=[d for d in definitions if same(selected,{'ref':d['definitionRef'],'digest':digest(d)}) and d['id'] in CASES]
    if len(cases)==1:
        definition=cases[0]
        result['caseDefinitionBinding']=selected
    else:
        extension=resolve(selected,'eventExtension','EXACT_TYPED_EVENT_EXTENSION_DEFINITION',
            [read_origin(matches[0]['id'], '/canonicalCaseBinding')])
        if extension is None:return unavailable_case()
        subtype_shape_matches=(extension['subtypePresence']=='PRESENT')==(isinstance(extension['eventSubtypeId'],str) and bool(extension['eventSubtypeId']))
        check('EVENT_EXTENSION_SUBTYPE_SHAPE_MISMATCH',subtype_shape_matches,
            original('eventExtension','/eventSubtypeId'),original('eventExtension','/subtypePresence'))
        if not subtype_shape_matches:
            errors.append({'code':'EVENT_EXTENSION_SUBTYPE_SHAPE_MISMATCH','pointer':'/eventSubtypeId'})
        presence_matches=extension['subtypePresence']==use['subtypePresence']
        check('EVENT_EXTENSION_SELECTED_PRESENCE_MISMATCH',presence_matches,
            original('eventExtension','/subtypePresence'),original('eventUse','/subtypePresence'))
        if not presence_matches:
            errors.append({'code':'EVENT_EXTENSION_SELECTED_PRESENCE_MISMATCH','pointer':'/subtypePresence'})
        item=next(s for s in sources if same(s['binding'],selected))
        meaning={'subtypePresence':extension['subtypePresence'],
                 'dominantSemanticConsequence':extension['dominantSemanticConsequence'],
                 'concept':extension['caseKind'],'candidateVocabularyRevision':extension['vocabularyRevision'],
                 'primaryFamilyFromSource':extension['primaryFamily'],'sourcePackRef':extension['sourcePackRef']}
        if extension['subtypePresence']=='PRESENT':meaning['eventSubtypeId']=extension['eventSubtypeId']
        definition={'id':'V04-extension','definitionRef':extension['definitionId'],
                    'sourceDefinition':{'typedRepresentation':{'eventMeaningCase':meaning},'subtypeAbsentVariant':meaning},
                    'extensionRecord':extension,'extensionSourceId':item['id']}
        result['caseDefinitionBinding']={'ref':extension['definitionId'],'digest':digest(extension)}
    result['definition']=definition
    case_choice=observe_guard('EVENT_CASE_DEFINITION_SELECTED',True,
        origins=[original('eventUse','/canonicalCaseBinding')]
            +([original('eventExtension','')] if 'extensionRecord' in definition else []))
    register_result_dependencies(result,'EVENT_CASE_DEFINITION',[case_choice])
    case_dependencies=[case_choice] if case_choice is not None else []
    def case_origin(field):
        if 'extensionRecord' in definition:
            source_field={'candidateVocabularyRevision':'vocabularyRevision','concept':'caseKind',
                          'primaryFamilyFromSource':'primaryFamily'}.get(field,field)
            return original('eventExtension','/'+source_field)
        return read_origin('DOMAIN_DEFINITIONS','/definitions/'+str(definitions.index(definition))
            +'/sourceDefinition/typedRepresentation/eventMeaningCase/'+field)
    vocab=resolve(use['vocabularyDefinitionBinding'],'eventVocabulary','EXACT_EVENT_VOCABULARY_DEFINITION',
        [read_origin(matches[0]['id'], '/vocabularyDefinitionBinding')])
    pack=resolve(use['packDefinitionBinding'],'eventPack','EXACT_EVENT_MEANING_PACK_DEFINITION',
        [read_origin(matches[0]['id'], '/packDefinitionBinding')])
    if vocab is None or pack is None:return result
    case=definition['sourceDefinition']['typedRepresentation']['eventMeaningCase']
    vocabulary_matches=vocab['vocabularyRevision']==case['candidateVocabularyRevision']
    check('EVENT_VOCABULARY_REVISION_MISMATCH',vocabulary_matches,original('eventVocabulary','/vocabularyRevision'),
        case_origin('candidateVocabularyRevision'),depends_on=case_dependencies)
    if not vocabulary_matches:
        errors.append({'code':'EVENT_VOCABULARY_REVISION_MISMATCH','pointer':'/vocabularyRevision'})
    for kind,value in [('vocabulary',vocab),('pack',pack)]:
        selected_kind='eventVocabulary' if kind=='vocabulary' else 'eventPack'
        site='EVENT_CASE_MEMBERSHIP:'+kind
        member=any(same(predicate_value(resolved[selected_kind],'/caseBindings/'+str(n),b,site),selected)
            for n,b in enumerate(value['caseBindings']))
        membership=observe_guard(site,member,origins=[original('eventUse','/canonicalCaseBinding')],
            predicate_sites=[site],depends_on=case_dependencies)
        check('EVENT_CASE_NOT_IN_SELECTED_'+kind.upper(),member,original(selected_kind,'/caseBindings'),
            original('eventUse','/canonicalCaseBinding'),depends_on=[membership] if membership is not None else [])
        if not member:
            errors.append({'code':'EVENT_CASE_NOT_IN_SELECTED_'+kind.upper(),'pointer':'/'+kind+'/caseBindings'})
    pack_vocabulary_matches=same(pack['vocabularyDefinitionBinding'],use['vocabularyDefinitionBinding'])
    check('EVENT_PACK_VOCABULARY_BINDING_MISMATCH',pack_vocabulary_matches,
        original('eventPack','/vocabularyDefinitionBinding'),original('eventUse','/vocabularyDefinitionBinding'),
        depends_on=case_dependencies)
    if not pack_vocabulary_matches:
        errors.append({'code':'EVENT_PACK_VOCABULARY_BINDING_MISMATCH','pointer':'/pack/vocabularyDefinitionBinding'})
    pack_source_matches=pack['sourcePackRef']==case.get('sourcePackRef')
    check('EVENT_PACK_SOURCE_REFERENCE_MISMATCH',pack_source_matches,original('eventPack','/sourcePackRef'),
        case_origin('sourcePackRef'),depends_on=case_dependencies)
    if not pack_source_matches:
        errors.append({'code':'EVENT_PACK_SOURCE_REFERENCE_MISMATCH','pointer':'/pack/sourcePackRef'})
    result['selectedExtentTemporalMeanings']=[{'meaning':v,'origin':{'inputRole':matches[0]['id'],'pointer':'/extentTemporalMeanings/'+str(i)}} for i,v in enumerate(use.get('extentTemporalMeanings',[]))]
    result['useDefinitionBinding']=matches[0]['binding']
    result['vocabularyDefinitionBinding']=use['vocabularyDefinitionBinding']
    result['packDefinitionBinding']=use['packDefinitionBinding']
    measurement_present=observe_guard('EVENT_OBSERVATION_MEASUREMENT_PRESENT','observationMeasurementBinding' in use,
        origins=[original('eventUse','/observationMeasurementBinding')],depends_on=case_dependencies)
    if 'observationMeasurementBinding' in use:
        measurement_case_matches=definition['id']=='V04-stand-count'
        case_identity=(original('eventExtension','/caseKind') if 'extensionRecord' in definition
            else read_origin('DOMAIN_DEFINITIONS','/definitions/'+str(definitions.index(definition))+'/id'))
        check('EVENT_MEASUREMENT_SELECTOR_FOR_WRONG_CASE',measurement_case_matches,
            original('eventUse','/observationMeasurementBinding'),case_identity,
            depends_on=case_dependencies+([measurement_present] if measurement_present is not None else []))
        if not measurement_case_matches:
            errors.append({'code':'EVENT_MEASUREMENT_SELECTOR_FOR_WRONG_CASE','pointer':'/observationMeasurementBinding'})
        elif not errors:
            result['selectedObservationMeasurement']={'binding':use['observationMeasurementBinding'],
                'origin':{'inputRole':matches[0]['id'],'pointer':'/observationMeasurementBinding'}}
    return result
