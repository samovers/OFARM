"""Typed citation closure and selected original evidence inspection.

Membership uses complete declared selectors, even if two selectors resolve to
the same bytes. Schema checking and protected resolution never imply eligible
use. The existing evidence owner must establish the use of each relied-on
record; this module neither manufactures that mechanism nor accepts flags.
"""
from strict_inputs import same, digest


from domain_reader_occurrences import reader, selection as observe_selection, guard as observe_guard, origin as read_origin, observed_shape, observe_comparisons


@reader('evidence_sources.py', ['AR_EVIDENCE'])
def evaluate(intent, inventory, sources, source_trace):
    errors = list(inventory['errors'])
    missing, comparisons, records, ids = [], [], [], []
    evidence = intent['evidenceBindings']
    citations = [v for v in inventory['references'] if v['role'] == 'ASSERTION_EVIDENCE'
                 and not v['pointer'].startswith('/evidenceBindings/')]
    traced = {v['id']: v for v in source_trace['resolvedInputs']}
    unresolved = {v['id']: v for v in source_trace['unresolvedInputs']}

    def fields(code, left, lp, right, rp, allowed=True):
        # Wrappers contain schema metadata as well as the selector. Trace only
        # actual selector fields; never hash a projected binding as a whole
        # original object when the original object is a larger wrapper.
        for key in ['ref', 'revisionRef', 'digest']:
            if key not in left or key not in right:
                continue
            equal = same(left[key], right[key])
            comparisons.append({'predicateId': code + ':' + key,
                'source': {'inputRole': 'EFFECT_INTENT', 'pointer': lp + '/' + key,
                           'valueDigest': digest(left[key])},
                'destination': {'inputRole': 'EFFECT_INTENT', 'pointer': rp + '/' + key,
                                'valueDigest': digest(right[key])},
                'disposition': 'PASS' if allowed and equal else 'FAIL'})
            observe_comparisons([comparisons[-1]])

    for citation in citations:
        selected = citation['binding']
        exact = [i for i, item in enumerate(evidence) if same(selected, item)]
        # For a wrong revision, retain the actual conflicting original fields.
        # A missing member has no destination value and remains a diagnostic.
        candidates = exact or [i for i, item in enumerate(evidence) if item['ref'] == selected['ref']]
        if candidates:
            i = candidates[0]
            fields('CITATION_EXACT_EVIDENCE_MEMBER', selected, citation['pointer'],
                   evidence[i], '/evidenceBindings/' + str(i), bool(exact))

    act_binding = intent.get('assertionActEvidenceBinding')
    act_sources = [v for v in sources if act_binding is not None and same(v['binding'], act_binding)]
    if act_binding is not None:
        observe_selection('ASSERTION_ACT_SELF_ATTESTATION_CHECK', sources, act_sources, binding=act_binding,
            origins=[read_origin('EFFECT_INTENT', '/assertionActEvidenceBinding')])
    for i, binding in enumerate(evidence):
        path = '/evidenceBindings/' + str(i)
        matched = [v for v in sources if same(v['binding'], binding)]
        observe_selection('DECLARED_EVIDENCE_ORIGINAL', sources, matched, binding=binding,
            origins=[read_origin('EFFECT_INTENT', path)])
        entry = {'binding': binding, 'pointer': path,
                 'citationPointers': [v['pointer'] for v in citations if same(v['binding'], binding)],
                 'sourceDisposition': 'NOT_EVALUATED', 'eligibleUseDisposition': 'NOT_EVALUATED'}
        # This is the current self-attestation, not a generic ban on evidence
        # with a similar name. Protected byte aliases cannot hide that record.
        self_attestation = act_binding is not None and same(binding, act_binding)
        if len(matched) == 1 and len(act_sources) == 1:
            a, b = matched[0], act_sources[0]
            self_attestation = self_attestation or (a['binding']['ref'] == b['binding']['ref']
                and a['rawSha256'] == b['rawSha256'] and a['valueDigest'] == b['valueDigest'])
        if self_attestation:
            errors.append({'code': 'ACT_SELF_ATTESTATION_IS_NOT_ORDINARY_CLAIM_EVIDENCE', 'pointer': path})
            fields('ACT_SELF_ATTESTATION_IS_NOT_ORDINARY_CLAIM_EVIDENCE', binding, path,
                   act_binding, '/assertionActEvidenceBinding', False)
        if len(matched) != 1:
            missing.append({'role': 'EXACT_DECLARED_EVIDENCE_ORIGINAL', 'pointer': path, 'binding': binding})
        else:
            source = matched[0]
            entry.update(sourceInputId=source['id'], rawSha256=source['rawSha256'], valueDigest=source['valueDigest'])
            if source['id'] in traced:
                ids.append(source['id'])
                entry.update(sourceDisposition='PASS', schemaBinding=traced[source['id']]['schemaBinding'])
            else:
                failure = unresolved.get(source['id'], {})
                if failure.get('reason') == 'SELECTED_SOURCE_SCHEMA_MISMATCH':
                    entry['sourceDisposition'] = 'FAIL'
                    errors.append({'code': 'DECLARED_EVIDENCE_SOURCE_SCHEMA_MISMATCH', 'pointer': path,
                                   'sourceInputId': source['id'], 'sourceErrors': failure.get('errors', [])})
                else:
                    missing.append({'role': 'EXACT_DECLARED_EVIDENCE_SOURCE_SCHEMA', 'pointer': path, 'binding': binding})
            missing.append({'role': 'EXISTING_EVIDENCE_OWNER_USE_FOR_SELECTED_CLAIM', 'pointer': path,
                            'binding': binding, 'sourceInputId': source['id']})
        records.append(entry)
    return {'disposition': 'FAIL' if errors else 'NOT_EVALUATED' if missing else 'PASS',
            'citationDisposition': 'FAIL' if inventory['errors'] else 'PASS',
            'errors': errors, 'remainingRoles': missing, 'comparisons': comparisons,
            'sourceInputIds': sorted(set(ids)), 'declaredEvidence': records,
            'qualification': 'Exact typed citation membership and schema-checked protected originals only. Each declared record remains subject to its existing owner use/admission mechanism; a schema, digest, or matching citation does not supply it.'}
