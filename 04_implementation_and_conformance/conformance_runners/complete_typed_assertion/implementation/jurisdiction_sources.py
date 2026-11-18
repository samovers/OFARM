"""Interpret a selected profile's jurisdiction code through original definitions.

This is a code-to-reference meaning comparison. It makes no claim of current
law, governing jurisdiction, regulatory authority or source-use eligibility.
The definition is selected by the independently fixed profile binding before
examining the claimant's code or the verification trace's asserted reference.
"""
from definition_inputs import SCHEMAS, register
from strict_inputs import same, digest, distinct_selected_originals


from domain_reader_occurrences import reader, selection as observe_selection, guard as observe_guard, origin as read_origin, observed_shape, predicate_value, guard_refs, observe_comparisons


@reader('jurisdiction_sources.py', ['AR_BODY'])
def evaluate(atom, sources, schemas):
    register(schemas)
    body = atom['body']; errors, missing, ids, references, comparisons = [], [], [], [], []
    definition_schema = SCHEMAS['jurisdiction']
    matches = [s for s in sources if predicate_value(s, '', isinstance(s['record'], dict), 'PROFILE_JURISDICTION_DEFINITION')
               and predicate_value(s, '/schemaVersion', s['record'].get('schemaVersion'), 'PROFILE_JURISDICTION_DEFINITION') == definition_schema['properties']['schemaVersion']['const']
               and same(predicate_value(s, '/profileBinding', s['record'].get('profileBinding'), 'PROFILE_JURISDICTION_DEFINITION'), body['profile'])]
    # Protected digest and explicitly selected revision aliases are the same
    # original input, not two competing definitions. Only independent domain
    # selections can nominate this otherwise unmentioned normative record.
    matches = distinct_selected_originals([s for s in matches if 'selectorMapping' in s])
    definition_selection = observe_selection('PROFILE_JURISDICTION_DEFINITION', sources, matches,
        origins=[read_origin('ATOM:' + atom['atomId'], '/body/profile')])
    selected = None
    if len(matches) != 1:
        missing.append({'role': 'INDEPENDENT_JURISDICTION_CODE_TO_IDENTITY_REFERENCE', 'pointer': '/body/profile'})
        if len(matches) > 1:
            observe_comparisons([{'predicateId': 'AMBIGUOUS_PROFILE_JURISDICTION_DEFINITION',
                'source': read_origin('ATOM:' + atom['atomId'], '/body/profile'), 'disposition': 'FAIL'}],
                depends_on=[definition_selection] if definition_selection is not None else [])
            errors.append({'code': 'AMBIGUOUS_PROFILE_JURISDICTION_DEFINITION', 'pointer': '/body/profile'})
    else:
        entry = matches[0]; definition = entry['record']; ids.append(entry['id'])
        references.append({'role': 'PROFILE_JURISDICTION_DEFINITION', 'binding': entry['binding'], 'pointer': '/body/profile'})
        errors.extend(observed_shape(schemas, definition_schema['$id'], definition))
        if not errors:
            identity_matches = definition['definitionId'] == entry['binding']['ref']
            # The expected ref is retained by the actual selected-read event.
            observe_comparisons([{'predicateId': 'JURISDICTION_DEFINITION_IDENTITY_MISMATCH',
                'source': read_origin(entry['id'], '/definitionId'),
                'disposition': 'PASS' if identity_matches else 'FAIL'}])
            if not identity_matches:
                errors.append({'code': 'JURISDICTION_DEFINITION_IDENTITY_MISMATCH', 'pointer': '/definitionId'})
            for code, source_path, source_value, expected_path, expected_value in [
                ('JURISDICTION_DEFINITION_PROFILE_MISMATCH', '/profileBinding', definition['profileBinding'], '/body/profile', body['profile']),
                ('JURISDICTION_DEFINITION_CODE_MISMATCH', '/jurisdictionCode', definition['jurisdictionCode'], '/body/jurisdiction', body['jurisdiction']),
            ]:
                equal = same(source_value, expected_value)
                comparisons.append({'predicateId': code, 'pointer': expected_path, 'equal': equal,
                    'source': {'inputRole': entry['id'], 'pointer': source_path, 'valueDigest': digest(source_value)},
                    'destination': {'inputRole': 'ATOM:' + atom['atomId'], 'pointer': expected_path, 'valueDigest': digest(expected_value)},
                    'disposition': 'PASS' if equal else 'FAIL'})
                observe_comparisons([comparisons[-1]])
                if not equal:
                    errors.append({'code': code, 'pointer': expected_path})
            selected = definition['jurisdictionBinding']['ref']
            traces = [s for s in sources if same(s['binding'], body['verificationTrace'])]
            observe_selection('JURISDICTION_TRACE', sources, traces, binding=body['verificationTrace'],
                origins=[read_origin('ATOM:' + atom['atomId'], '/body/verificationTrace')])
            if len(traces) != 1:
                missing.append({'role': 'EXACT_SELECTED_JURISDICTION_TRACE_ORIGINAL', 'pointer': '/body/verificationTrace'})
            else:
                trace = traces[0]; ids.append(trace['id'])
                shape = observed_shape(schemas, 'https://ofarm.dev/schema/externalregistryverificationtrace/v0.1', trace['record'])
                errors.extend(shape)
                if not shape:
                    actual = trace['record']['traceJurisdictionRef']; equal = same(actual, selected)
                    comparisons.append({'predicateId': 'TRACE_JURISDICTION_MISMATCH', 'pointer': '/traceJurisdictionRef', 'equal': equal,
                        'source': {'inputRole': trace['id'], 'pointer': '/traceJurisdictionRef', 'valueDigest': digest(actual)},
                        'destination': {'inputRole': entry['id'], 'pointer': '/jurisdictionBinding/ref', 'valueDigest': digest(selected)},
                        'disposition': 'PASS' if equal else 'FAIL'})
                    observe_comparisons([comparisons[-1]])
                    if not equal: errors.append({'code': 'TRACE_JURISDICTION_MISMATCH', 'pointer': '/traceJurisdictionRef'})
    return {'scope': 'PROFILE_JURISDICTION_CODE_AND_ORIGINAL_TRACE_REFERENCE_MAPPING_ONLY',
            'disposition': 'FAIL' if errors else 'NOT_EVALUATED' if missing else 'PASS',
            'errors': errors, 'remainingRoles': missing, 'comparisons': comparisons,
            'sourceInputIds': ids, 'requiredReferences': references,
            'selectedJurisdictionRef': selected,
            'qualification': 'Selected normative mapping only; no legal applicability, currentness, regulatory authority or admission is inferred.'}
