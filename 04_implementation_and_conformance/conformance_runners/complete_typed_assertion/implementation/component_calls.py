"""Recompute domain comparisons; caller reports and pass flags are forbidden."""
import json
from pathlib import Path
import sys
from reference_roles import collect, audit_schema_roles
from owner_calls import selected_owner_root
from domain_reader_occurrences import reader, branch as observed_branch, origin as read_origin, guard_refs, guard as observe_guard

HERE = Path(__file__).resolve().parent


def invoke(intent, result, action, requests, prior=None, resolved_sources=None, occupancy=None, source_context_digest=None, event=None):
    request = {'intent': intent, 'result': result, 'action': action,
               'requests': requests, 'prior': prior, 'resolvedSources': resolved_sources, 'occupancy': occupancy,
               'sourceContextDigest': source_context_digest, 'event': event}
    return evaluate_components(request)


def evaluate_components(request, *, independent_read_trace=False):
    sys.path.insert(0, str(HERE / 'components/revision-02'))
    sys.path.insert(0, str(HERE / 'outer'))
    from domain_api import evaluate
    from runtime_support import Schemas
    from runtime_support import exact, error
    from intrinsics import time_bounds
    from referencing import Registry, Resource
    import domain_mapping
    schemas = _schemas()
    role_errors = audit_schema_roles(schemas.schemas, 'https://ofarm.dev/schema/drafts/non-default/assertion-domain/proposition/v0.1')
    if role_errors:
        raise ValueError('Typed reference role coverage differs from the exact schemas: ' + json.dumps(role_errors))
    branch = {'ASSERT_STRUCTURE': 'structure', 'ASSERT_OPERATION_CLAIM': 'operation',
              'ASSERT_COMPLIANCE': 'compliance'}[request['action']]
    prefix = 'https://ofarm.dev/schema/drafts/non-default/assertion-record-domain-validation/'
    report = {'intentErrors': schemas.errors(prefix + branch + '-intent/v0.1', request['intent']),
              'resultErrors': schemas.errors(prefix + 'result/v0.1', request['result']),
              'copyFacts': domain_mapping.copy_facts(request['intent'], request['result'], request['action']),
              'componentReports': []}
    if not report['intentErrors']:
        report['referenceInventory'] = collect(request['intent'])
    if request.get('prior') is not None:
        prior = request['prior']
        prior_id = {'ofarm.assertionrecord.v0.2': 'https://ofarm.dev/schema/assertionrecord/v0.2',
                    'ofarm.assertionrecord.typed.v0.1': prefix + 'result/v0.1'}.get(prior.get('schemaVersion'))
        report['priorErrors'] = schemas.errors(prior_id, prior) if prior_id else [error('UNSUPPORTED_PRIOR_SCHEMA', '/schemaVersion')]
    try:
        report['renderedText'] = domain_mapping.render(request['intent'], request['action'])
        report['projectionDigest'] = domain_mapping.value_digest(domain_mapping.project(request['intent'], request['action']))
    except (domain_mapping.ProjectionError, ValueError, KeyError, TypeError, IndexError) as exc:
        report['renderingError'] = str(exc)
    _source_components(request, schemas, report, independent_read_trace=independent_read_trace)
    for item in request['requests']:
        try:
            report['componentReports'].append({'id': item['id'], 'report': evaluate(item['request'])})
        except (ValueError, KeyError, TypeError, IndexError) as exc:
            report['componentReports'].append({'id': item.get('id', '<missing>'),
                                              'invocationError': str(exc)})
    return report


def _schemas():
    sys.path.insert(0, str(HERE / 'components/revision-02'))
    sys.path.insert(0, str(HERE / 'outer'))
    from runtime_support import Schemas
    from referencing import Registry, Resource
    schemas = Schemas()
    for p in sorted((selected_owner_root('act') / 'source-contracts').glob('*.json')):
        value = json.loads(p.read_bytes())
        if '$id' in value:
            previous = schemas.schemas.get(value['$id'])
            if previous is not None and previous != value:
                raise ValueError('Conflicting selected schema bytes under one schema ID: ' + value['$id'])
            schemas.schemas[value['$id']] = value
    for p in sorted((HERE / 'outer/carriers').glob('*.schema.json')):
        value = json.loads(p.read_bytes())
        schemas.schemas[value['$id']] = value
    for name in ['IdentityRecord', 'Party']:
        value = json.loads((HERE / 'source-contracts' / (name + '.schema.json')).read_bytes())
        previous = schemas.schemas.get(value['$id'])
        if previous is not None and previous != value:
            raise ValueError('Conflicting selected identity schema: ' + value['$id'])
        schemas.schemas[value['$id']] = value
    schemas.registry = Registry().with_resources((k, Resource.from_contents(v)) for k, v in schemas.schemas.items())
    return schemas


@reader('component_calls.py:source_dispatch', ['AR_BODY'])
def _source_components(request, schemas, report, *, independent_read_trace=False):
    from domain_api import evaluate
    from runtime_support import exact, error
    from intrinsics import time_bounds
    body = request['intent'].get('assertionBody')
    if isinstance(body, dict) and isinstance(body.get('proposition'), dict):
        report['intrinsics'] = evaluate({'operation': 'intrinsics', 'proposition': body['proposition']})
        report['outerBindingErrors'] = []
        if not report['intrinsics']['errors']:
            intent = request['intent']
            def walk(p, path, sequence=False):
                sequence = sequence or p['form'] == 'SEQUENCE'
                if p['form'] == 'ATOM':
                    scope = p['scope']; subject = scope['subject']
                    if observed_branch('ATOM_OUTER_SUBJECT_DIFFERS', not exact(subject, intent.get('subject')),
                            origins=[read_origin('EFFECT_INTENT', path + '/scope/subject'), read_origin('EFFECT_INTENT', '/subject')]):
                        selector = {k: subject[k] for k in ['revisionRef', 'digest'] if k in subject}
                        binding = {'ref': subject['subjectRef'], **selector}
                        context_operands = []
                        def context_field(value, index, field):
                            context_operands.append(read_origin('EFFECT_INTENT',
                                '/assertionBody/contextBindings/' + str(index) + '/' + field))
                            return value.get(field)
                        matches = [v for n, v in enumerate(body.get('contextBindings', []))
                                   if context_field(v, n, 'contextRole') == subject['subjectType']
                                   and exact(context_field(v, n, 'binding'), binding)
                                   and context_field(v, n, 'relationshipProofBindings')]
                        if observed_branch('ATOM_CONTEXT_SELECTION_MISSING', not matches,
                                origins=[read_origin('EFFECT_INTENT', path + '/scope/subject')] + context_operands,
                                depends_on=guard_refs('ATOM_OUTER_SUBJECT_DIFFERS')):
                            report['outerBindingErrors'].append(error('ATOM_SUBJECT_OUTSIDE_DECLARED_CONTEXT', path + '/scope/subject'))
                    if sequence:
                        try:
                            lo, hi = time_bounds(intent['subjectTime']); a, z = time_bounds(scope['subjectTime'])
                            if observed_branch('SEQUENCE_OUTER_TIME_CONTRADICTION', a < lo or hi is not None and (z is None or z > hi),
                                    origins=[read_origin('EFFECT_INTENT', path + '/scope/subjectTime'), read_origin('EFFECT_INTENT', '/subjectTime')]):
                                report['outerBindingErrors'].append(error('SEQUENCE_OUTSIDE_OUTER_TIME', path + '/scope/subjectTime'))
                        except (KeyError, ValueError, TypeError):
                            report['outerBindingErrors'].append(error('OUTER_TIME_UNAVAILABLE', '/subjectTime'))
                    elif observed_branch('ATOM_OUTER_TIME_DIFFERS', not exact(scope['subjectTime'], intent.get('subjectTime')),
                            origins=[read_origin('EFFECT_INTENT', path + '/scope/subjectTime'), read_origin('EFFECT_INTENT', '/subjectTime')]):
                        report['outerBindingErrors'].append(error('ATOM_OUTER_TIME_MISMATCH', path + '/scope/subjectTime'))
                    if observed_branch('ATOM_OPERATION_OUTER_FIELDS', p['definition'].startswith('candidate:assertion-domain-construction:2026-10-21:r2:O'),
                            origins=[read_origin('EFFECT_INTENT', path + '/definition')]):
                        if observed_branch('ATOM_OUTER_PERFORMER_DIFFERS', not exact(p['body'].get('performedBy'), body.get('performedByBinding')),
                                origins=[read_origin('EFFECT_INTENT', path + '/body/performedBy'), read_origin('EFFECT_INTENT', '/assertionBody/performedByBinding')],
                                depends_on=guard_refs('ATOM_OPERATION_OUTER_FIELDS')):
                            report['outerBindingErrors'].append(error('ATOM_OUTER_PERFORMER_MISMATCH', path + '/body/performedBy'))
                        if observed_branch('ATOM_OUTER_POSTURE_DIFFERS', p['body'].get('claimPosture') != intent.get('claimPosture'),
                                origins=[read_origin('EFFECT_INTENT', path + '/body/claimPosture'), read_origin('EFFECT_INTENT', '/claimPosture')],
                                depends_on=guard_refs('ATOM_OPERATION_OUTER_FIELDS')):
                            report['outerBindingErrors'].append(error('ATOM_OUTER_CLAIM_POSTURE_MISMATCH', path + '/body/claimPosture'))
                elif p['form'] in ['NOT', 'QUALIFIED']:
                    walk(p['child'], path + '/child', sequence)
                else:
                    for i, child in enumerate(p['children']):
                        walk(child, path + '/children/' + str(i), sequence)
            walk(body['proposition'], '/assertionBody/proposition')
            if request.get('resolvedSources') is not None:
                from identity_sources import evaluate as identity_sources
                report['identitySourceComparisons'] = identity_sources(intent, request['resolvedSources'], schemas)
                from context_sources import evaluate as context_sources
                report['contextSourceComparisons'] = context_sources(intent, request['resolvedSources'], schemas, report['referenceInventory'])
                from source_derivation import derive
                report['automaticSourceComparisons'] = derive(intent, request['resolvedSources'], request.get('occupancy'), endpoint_schemas=schemas)
                if intent.get('associatedSemanticEventBinding') is not None:
                    from event_sources import evaluate as event_sources
                    report['eventSourceComparisons'] = event_sources(intent, request.get('event'),
                        report['automaticSourceComparisons'], request['resolvedSources'], schemas)
                from temporal_sources import evaluate as temporal
                report['temporalSources'] = temporal(intent, request['resolvedSources'], schemas)
                from proposition_logic import evaluate as proposition_logic
                report['propositionEvaluation'] = proposition_logic(intent, report['automaticSourceComparisons'], time_bounds)
                if request.get('sourceContextDigest') is not None:
                    _register_source_schemas(schemas)
                    from source_trace import collect as source_trace
                    report['sourceTrace'] = source_trace(schemas, request['resolvedSources'], request['sourceContextDigest'])
                    from evidence_sources import evaluate as evidence_sources
                    report['evidenceSourceComparisons'] = evidence_sources(intent, report['referenceInventory'],
                        request['resolvedSources'], report['sourceTrace'])
                    from compliance_sources import evaluate as compliance_sources
                    report['complianceSourceComparisons'] = compliance_sources(intent,
                        request['resolvedSources'], report['sourceTrace'])
                elif independent_read_trace:
                    # Independent C3 replay has no protected context/admission.
                    # Retain attempted original reads under unresolved schema/use.
                    _register_source_schemas(schemas)
                    from source_trace import inspect as inspect_sources
                    unresolved_trace = inspect_sources(schemas, request['resolvedSources'])
                    from evidence_sources import evaluate as evidence_sources
                    report['evidenceSourceComparisons'] = evidence_sources(intent, report['referenceInventory'],
                        request['resolvedSources'], unresolved_trace)
                    from compliance_sources import evaluate as compliance_sources
                    report['complianceSourceComparisons'] = compliance_sources(intent,
                        request['resolvedSources'], unresolved_trace)


def _register_source_schemas(schemas):
    from definition_inputs import register
    register(schemas)
    from work_definition_inputs import register as register_work
    register_work(schemas)
    from event_definition_inputs import register as register_event
    register_event(schemas)
    from analysis_output_definitions import register as register_analysis_output
    register_analysis_output(schemas)
    from sample_collection_definitions import register as register_sample_collection
    register_sample_collection(schemas)
    from observation_acquisition_definitions import register as register_observation_acquisition
    register_observation_acquisition(schemas)
    from drying_definitions import register as register_drying
    register_drying(schemas)
    from irrigation_definitions import register as register_irrigation
    register_irrigation(schemas)
    from sanitation_definitions import register as register_sanitation
    register_sanitation(schemas)
    from si_c17_sources import register as register_si_c17
    register_si_c17(schemas)

def evaluate_reader_components(intent, sources, action, *, occupancy=None, event=None):
    """Same fixed source dispatch without requiring an unrelated result root."""
    schemas = _schemas()
    branch = {'ASSERT_STRUCTURE': 'structure', 'ASSERT_OPERATION_CLAIM': 'operation',
              'ASSERT_COMPLIANCE': 'compliance'}[action]
    schema_id = 'https://ofarm.dev/schema/drafts/non-default/assertion-record-domain-validation/' + branch + '-intent/v0.1'
    errors = schemas.errors(schema_id, intent)
    report = {'intentErrors': errors}
    if errors:
        return report
    report['referenceInventory'] = collect(intent)
    request = {'intent': intent, 'resolvedSources': sources, 'occupancy': occupancy,
               'event': event, 'sourceContextDigest': None}
    _source_components(request, schemas, report, independent_read_trace=True)
    return report


def worker():
    request = json.load(sys.stdin)
    print(json.dumps(evaluate_components(request), allow_nan=False))


if __name__ == '__main__':
    if sys.argv[1:] != ['--worker']:
        raise SystemExit('Private worker; use the public domain entry point.')
    worker()
