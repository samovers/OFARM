"""Work-definition meaning selected from protected original definition bytes.

Conditions are checked against original measurements through the selected
criterion/method interface. Definition text is never treated as executable
policy or as a factual witness. Physical action and identity creation remain
separate from this pending assertion's meaning.
"""
from strict_inputs import same,digest
from work_definition_inputs import SCHEMAS,register


# Shared semantic rules for the evaluated reader and independent original
# collector. Selection, schema validation, provenance and status stay with
# each caller; these rules do not admit a source or evaluate a condition.
WORK_CLAIM_VALUE_RULES = (
    ('WORK_PROCEDURE_PARAMETERS_MISMATCH',
     'WORK_PROCEDURE_PARAMETERS_COMPARISON', 'body', 'parameters'),
    *[('WORK_DEFINITION_' + key.upper() + '_MISMATCH',
       'WORK_SPECIFICATION_' + key.upper() + '_COMPARISON',
       'workSpecification', key)
      for key in ('activityInstance', 'target', 'extent', 'procedure')],
    *[('WORK_ATOM_' + key.upper() + '_MISMATCH',
       'WORK_ATOM_' + key.upper() + '_COMPARISON', 'body', key)
      for key in ('activityInstance', 'target', 'extent')],
)
WORK_CONDITION_GROUPS = (
    ('startConditions', 'startConditionIds', 'START', 'start:'),
    ('inProgressConditions', 'inProgressConditionIds', 'IN_PROGRESS', 'progress:'),
    ('finishConditions', 'finishConditionIds', 'FINISH', 'finish:'),
)
WORK_EXECUTION_STAGES = {
    'STARTED': 'START', 'IN_PROGRESS': 'IN_PROGRESS', 'COMPLETED': 'FINISH',
}


def condition_parent_expectations(condition_id, row, stage, work_position):
    """Expected condition values and their work-original pointers."""
    return (
        ('conditionId', condition_id, work_position + '/conditionId'),
        ('activityRow', row, '/activityRow'),
        ('stage', stage, None),
    )


def condition_at_stage(condition, stage):
    """The evaluated reader dispatches on the original condition's stage."""
    return stage is not None and condition['stage'] == stage


def work_time_basis_selection(kind, source):
    """Interpret the source's declared basis without comparing timestamps."""
    field, allowed = (('intendedTimeWindow', ('PLANNED_WINDOW', 'PRESCRIPTION_WINDOW'))
                      if kind == 'intent' else
                      ('effectiveTimeInterval', ('EXECUTION_INTERVAL',)))
    interval = source[field]
    basis = interval.get('timeBasis')
    return {'sourcePointer': '/' + field + '/timeBasis',
            'parentPointer': '/' + field,
            'present': 'timeBasis' in interval, 'value': basis,
            'allowedValues': list(allowed), 'supported': basis in allowed}


def work_performer_pointer(capture_role):
    """Identify a physical-performer field from its declared capture role."""
    return {'OPERATOR': '/actor/operatorPartyRef',
            'CONTRACTOR': '/actor/contractorPartyRef'}.get(capture_role)


def source_performer_pointer(source):
    """Use the legacy source-role-first reference selector, not claim matching.

    The fallback actor reference is comparable, but does not identify a
    physical performer. That interpretation remains a separate work rule.
    """
    actor = source.get('actor', {})
    expected = work_performer_pointer(actor.get('roleAtCapture'))
    return (expected if expected is not None and expected.rsplit('/', 1)[1] in actor
            else '/actor/actorPartyRef')


def actual_carrier_comparisons(adapter, row, atom, kind, source):
    """Reuse the sealed adapter's party/time predicates on a complete input.

    Empty quantity selections do not stand in for quantity evidence: this
    bounded call consumes only the existing party/time predicates below.
    Other adapter findings remain the responsibility of their reader paths.
    """
    from operation_adapters import OP_INPUT_ID
    data = {'atom': atom, 'sourceKind': kind, 'source': source,
            'quantitySelections': []}
    if kind == 'execution':
        data['performerPointer'] = source_performer_pointer(source['record'])
    errors = adapter.schemas.errors(OP_INPUT_ID, data, row)
    if errors:
        unavailable = any(item['code'] in {'SCHEMA_NOT_IN_PINNED_REGISTRY',
                                          'SCHEMA_RESOLUTION_ERROR'} for item in errors)
        return {'status': 'NOT_EVALUATED',
                'reason': 'OPERATION_ADAPTER_INPUT_SCHEMA_UNAVAILABLE' if unavailable else
                'COMPLETE_OPERATION_ADAPTER_INPUT_SCHEMA_INVALID',
                'schemaErrors': errors}
    checked = adapter.check(row, data)
    codes = {'SOURCE_PERFORMER_REF_MISMATCH', 'SOURCE_PROFILE_TIME_MISMATCH'}
    roles = {'SOURCE_PROFILE_TIME_INSTANT_INTERPRETATION',
             'INSTANT_FACET_MEASUREMENT_AT_PHENOMENON_TIME'}
    return {'status': 'CHECKED', 'performerPointer': data.get('performerPointer'),
            'comparisons': [item for item in checked['comparisons'] if item['code'] in codes],
            'remainingRoles': [item for item in checked['requiredOwnerRoles']
                               if item['role'] in roles],
            'errors': [item for item in checked['errors']
                       if item['code'] == 'SOURCE_PROFILE_TIME_UNAVAILABLE']}


def carrier_meaning_checks(kind, source, meaning, parameters):
    """Yield code, values, display path, source scope/pointer and presence.

    Callers retain their own original-byte and claim-shape checks. An absent
    optional carrier field projects to null without becoming an observation.
    """
    action_path = '/intendedAction' if kind == 'intent' else '/actualAction'
    actual = source[action_path[1:]]
    yield ('WORK_CARRIER_ACTION_MEANING_MISMATCH', actual['actionType'],
           meaning['actionType'], '/source/actionType', 'carrier',
           action_path + '/actionType', '/carrierMeaning/actionType', True)
    if meaning['interventionKind'] is not None:
        value = source if kind == 'intent' else actual
        path = ('/' if kind == 'intent' else action_path + '/') + 'interventionKind'
        yield ('WORK_CARRIER_INTERVENTION_MISMATCH', value.get('interventionKind'),
               meaning['interventionKind'], '/source/interventionKind', 'carrier',
               path, '/carrierMeaning/interventionKind', 'interventionKind' in value)
    if meaning['methodBinding'] is not None:
        yield ('WORK_CARRIER_METHOD_MISMATCH', actual.get('methodRef'),
               meaning['methodBinding']['ref'], '/source/methodRef', 'carrier',
               action_path + '/methodRef', '/carrierMeaning/methodBinding/ref',
               'methodRef' in actual)
    if 'specificActivity' in parameters:
        yield ('WORK_SPECIFIC_ACTIVITY_MISMATCH', parameters['specificActivity'],
               meaning['specificActivity'], '/body/parameters/specificActivity',
               'claim', '/body/parameters/specificActivity',
               '/carrierMeaning/specificActivity', True)


def evaluate(atom, request, sources, schemas):
    from referencing import Resource
    from runtime_support import instant
    from common import reviewed
    register(schemas)
    for value in SCHEMAS.values():
        schemas.schemas[value['$id']]=value
        schemas.registry=schemas.registry.with_resource(value['$id'],Resource.from_contents(value))
    body=atom['body'];row=atom['definition'].split(':')[-1];selected=body['workSpecification']
    errors,missing,comparisons,refs,ids,closed=[],[],[],[],[],[]
    condition_findings=[]
    origins={}
    def original(record,path):
        return {'inputRole':origins[id(record)],'pointer':path} if id(record) in origins else None
    def claimed(path):
        return {'inputRole':'ATOM:'+atom['atomId'],'pointer':path}
    def compare(code,actual,expected,path,source=None,destination=None):
        equal=same(actual,expected)
        fact={'predicateId':code,'pointer':path,'equal':equal,
              'actualValueDigest':digest(actual),'expectedValueDigest':digest(expected)}
        if source is not None and destination is not None:
            fact.update(source={**source,'valueDigest':digest(actual)},destination={**destination,'valueDigest':digest(expected)},
                        disposition='PASS' if equal else 'FAIL')
        comparisons.append(fact)
        if not equal:errors.append({'code':code,'pointer':path})
    def resolve(binding,name,role,binding_origin=None):
        refs.append({'binding':binding,'role':role,'pointer':'/workDefinitions/'+role})
        found=[v for v in sources if same(v['binding'],binding)]
        if len(found)!=1:
            missing.append({'role':role,'pointer':'/workDefinitions/'+role});return None
        source=found[0];ids.append(source['id']);record=source['record']
        shape=schemas.errors(SCHEMAS[name]['$id'],record);errors.extend(shape)
        if shape:return None
        origins[id(record)]=source['id']
        compare('WORK_DEFINITION_IDENTITY_MISMATCH',record['definitionId'],binding['ref'],'/definitionId',
                original(record,'/definitionId'),binding_origin)
        return record
    def result():
        return {'scope':'WORK_DEFINITION_AND_ACTUAL_CONDITION_SOURCES','disposition':'FAIL' if errors else 'NOT_EVALUATED' if missing else 'PASS',
                'errors':errors,'remainingRoles':missing,'comparisons':comparisons,'requiredReferences':refs,
                'sourceInputIds':sorted(set(ids)),'closedRoles':sorted(set(closed)),
                'conditionFindings':condition_findings}
    definition=resolve(selected['binding'],'work','SELECTED_VERSIONED_WORK_SPECIFICATION',claimed('/body/workSpecification/binding/ref'))
    if definition is None:return result()
    compare('WORK_DEFINITION_ROW_MISMATCH',definition['activityRow'],row,'/activityRow')
    for code, _role, container, key in WORK_CLAIM_VALUE_RULES:
        values = selected if container == 'workSpecification' else body
        path = '/body/' + ('workSpecification/' if container == 'workSpecification' else '') + key
        compare(code,values[key],definition[key],path,
                claimed(path),original(definition,'/'+key))
    compare('WORK_OUTPUT_SPECIFICATION_MISMATCH',selected.get('outputSpecification'),definition['outputSpecification'],'/body/workSpecification/outputSpecification',
            claimed('/body/workSpecification/outputSpecification') if 'outputSpecification' in selected else None,original(definition,'/outputSpecification'))
    if body['claimPosture']=='INTENDED':
        compare('INTENDED_WORK_PERFORMER_MISMATCH',body['performedBy'],definition['intendedPerformer'],'/body/performedBy',
                claimed('/body/performedBy'),original(definition,'/intendedPerformer'))
        closed.append('INTENDED_NAMED_PERFORMER_FROM_WORK_DEFINITION')
    normative=next(v for v in reviewed('reviewed-input/domain/work-condition-definitions.json')['rows'] if v['activityRow']==row)
    conditions=[]
    for source_field,claim_field,stage,canonical_prefix in WORK_CONDITION_GROUPS:
        group=definition[source_field]
        canonical_id=canonical_prefix+row
        if canonical_id not in [v['conditionId'] for v in group]:
            errors.append({'code':'REQUIRED_CANONICAL_WORK_CONDITION_OMITTED','pointer':'/'+source_field})
        compare('WORK_CONDITION_SET_MISMATCH',selected[claim_field],[v['conditionId'] for v in group],'/body/workSpecification/'+claim_field)
        if len({v['conditionId'] for v in group})!=len(group):errors.append({'code':'DUPLICATE_WORK_CONDITION_ID','pointer':'/'+source_field})
        for index,item in enumerate(group):
            prefix='/'+source_field+'/'+str(index)
            if index<len(selected[claim_field]):
                compare('WORK_SELECTED_CONDITION_ID_MISMATCH',selected[claim_field][index],item['conditionId'],
                        '/body/workSpecification/'+claim_field+'/'+str(index),
                        claimed('/body/workSpecification/'+claim_field+'/'+str(index)),original(definition,prefix+'/conditionId'))
            condition=resolve(item['definitionBinding'],'workCondition','CONDITION:'+item['conditionId'],
                              original(definition,prefix+'/definitionBinding/ref'))
            if condition is None:continue
            for field,expected,expected_pointer in condition_parent_expectations(item['conditionId'],row,stage,prefix):
                destination=original(definition,expected_pointer) if expected_pointer is not None else None
                compare('WORK_CONDITION_'+field.upper()+'_MISMATCH',condition[field],expected,'/condition/'+field,
                        original(condition,'/'+field),destination)
            # The source packet's exact condition identifiers/text remain fixed.
            # A concrete procedure can add separately identified conditions, but
            # cannot change the meaning of one of these bound condition IDs.
            if item['conditionId'] in normative['conditionDefinitions']:
                compare('REVIEWED_WORK_CONDITION_MEANING_CHANGED',condition['meaning'],normative['conditionDefinitions'][item['conditionId']],'/condition/meaning')
            conditions.append((item['definitionBinding'],condition,original(definition,prefix+'/definitionBinding')))
    if not errors and not missing:closed.append('WORK_SPECIFICATION_ACTIVITY_TARGET_EXTENT_CONDITIONS')
    if request is None:
        missing.append({'role':'EXACT_ORIGINAL_OPERATION_CARRIER','pointer':'/source'})
        return result()
    source=request['input']['source']['record'];kind=request['input']['sourceKind']
    found=[v for v in sources if same(v['binding'],request['input']['source']['binding'])]
    if len(found)==1:origins[id(source)]=found[0]['id']
    source_schema='https://ofarm.dev/schema/'+('interventionintentpayload' if kind=='intent' else 'executionrecordpayload')+'/v0.1'
    shape=schemas.errors(source_schema,source)
    if shape:
        errors.extend(shape);return result()
    meaning=definition['carrierMeaning']
    for code,actual,expected,path,scope,source_pointer,expected_pointer,present in carrier_meaning_checks(kind,source,meaning,body['parameters']):
        origin = claimed(source_pointer) if scope == 'claim' else original(source,source_pointer) if present else None
        compare(code,actual,expected,path,origin,original(definition,expected_pointer))
    if 'specificActivity' in body['parameters']:
        if meaning['methodBinding'] is not None and not errors:
            closed.append('EXACT_SPECIFIC_ACTIVITY_DEFINITION_NOT_OTHER_ACTION_TOKEN')
    time_basis=work_time_basis_selection(kind,source)
    if time_basis['supported']:closed.append('SELECTED_PAYLOAD_TIME_BASIS_INTERPRETATION')
    else:missing.append({'role':'EXACT_SELECTED_WORK_TIME_BASIS','pointer':'/source/timeBasis'})
    if kind=='execution':
        actor=source['actor'];role=actor.get('roleAtCapture')
        expected=work_performer_pointer(role)
        if expected and request['input']['performerPointer']==expected:
            closed.append('PERFORMER_ROLE_IDENTIFICATION_NOT_REPORTER')
        else:missing.append({'role':'EXACT_PHYSICAL_PERFORMER_ROLE_SOURCE','pointer':'/source/actor'})
    required_stage=WORK_EXECUTION_STAGES.get(body['performanceFacet'])
    if kind=='execution' and required_stage:
        from condition_sources import evaluate as evaluate_condition
        for condition_binding,condition,selection_origin in [(b,c,o) for b,c,o in conditions if condition_at_stage(c,required_stage)]:
            checked=evaluate_condition(condition,atom,sources,schemas,
                condition_binding=condition_binding,condition_binding_origin=selection_origin,work_specification_binding=selected['binding'],
                procedure_binding=definition['procedure'])
            errors.extend(checked['errors']);missing.extend(checked['remainingRoles']);refs.extend(checked['requiredReferences']);ids.extend(checked['sourceInputIds'])
            comparisons.extend(checked['comparisons'])
            condition_finding={'conditionId':condition['conditionId'],'disposition':checked['disposition']}
            for key in ['retainedSourceQualifications','admissibleDomainInterpretation']:
                if checked.get(key) is not None:condition_finding[key]=checked[key]
            condition_findings.append(condition_finding)
        if body['performanceFacet']=='COMPLETED' and not errors and not missing:
            closed.append('ALL_BOUND_FINISH_CONDITIONS_OVER_ENTIRE_WORK_EXTENT')
    return result()
