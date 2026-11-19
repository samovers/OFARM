"""Exact explicit rule/policy references and their selected original records.

The named rule is what a compliance assertion claims against. Membership is a
domain consistency predicate; it never adopts the rule, establishes its legal
currentness, or supplies a policy owner's applicability/use decision.
"""
from strict_inputs import same, digest

# Only explicit rule/policy roles. Criteria, charters, profiles, and mere
# documentary references are not silently promoted into these roles.
FIELDS = {'C01': ('rule', 'ruleRevisionBindings'), 'C02': ('rule', 'ruleRevisionBindings'),
          'C08': ('rule', 'ruleRevisionBindings'), 'C10': ('policy', 'evidencePolicyRevisionBindings')}


from domain_reader_occurrences import reader, selection as observe_selection, guard as observe_guard, origin as read_origin, observed_shape, observe_comparisons


@reader('compliance_sources.py', ['AR_COMPLIANCE_RULES', 'AR_COMPLIANCE_EVIDENCE_POLICY'])
def evaluate(intent, sources, source_trace):
    if intent['schemaVersion'] != 'ofarm.complianceassertioneffectintent.typed.v0.1':
        return {}
    references = []
    def walk(p, path):
        if p['form'] == 'ATOM':
            row = p['definition'].split(':')[-1]
            if row in FIELDS:
                field, array = FIELDS[row]
                references.append({'binding': p['body'][field], 'pointer': path + '/body/' + field, 'array': array})
        elif 'child' in p:
            walk(p['child'], path + '/child')
        else:
            for n, child in enumerate(p['children']):
                walk(child, path + '/children/' + str(n))
    walk(intent['assertionBody']['proposition'], '/assertionBody/proposition')
    traced = {v['id']: v for v in source_trace['resolvedInputs']}
    unresolved = {v['id']: v for v in source_trace['unresolvedInputs']}
    outputs = {}
    for array, gate, kind in [('ruleRevisionBindings', 'COMPLIANCE_RULE_SELECTION', 'RULE'),
                              ('evidencePolicyRevisionBindings', 'EVIDENCE_POLICY_SELECTION', 'EVIDENCE_POLICY')]:
        errors, missing, comparisons, ids, selected = [], [], [], [], []
        findings = ['AR_COMPLIANCE_RULES'] if kind == 'RULE' else ['AR_COMPLIANCE_EVIDENCE_POLICY']
        for ref in [v for v in references if v['array'] == array]:
            exact = [n for n, b in enumerate(intent[array]) if same(b, ref['binding'])]
            # Record the existing membership decision even when no fallback
            # exists. Keep this trace fact out of ordinary comparison results.
            membership = observe_comparisons([{
                'predicateId': 'BODY_' + kind + '_NOT_EXACT_SELECTED_REVISION',
                'source': read_origin('EFFECT_INTENT', ref['pointer']),
                'destination': read_origin('EFFECT_INTENT', '/' + array),
                'disposition': 'PASS' if exact else 'FAIL',
            }], findings=findings)
            if not exact:
                errors.append({'code': 'BODY_' + kind + '_NOT_EXACT_SELECTED_REVISION', 'pointer': ref['pointer']})
            candidates = exact or [n for n, b in enumerate(intent[array]) if b['ref'] == ref['binding']['ref']]
            if not candidates:
                continue
            n = candidates[0]
            for key in ['ref', 'revisionRef', 'digest']:
                if key not in ref['binding'] or key not in intent[array][n]:
                    continue
                a, b = ref['binding'][key], intent[array][n][key]
                comparisons.append({'predicateId': 'BODY_' + kind + '_EXACT_SELECTED_REVISION:' + key,
                    'source': {'inputRole': 'EFFECT_INTENT', 'pointer': ref['pointer'] + '/' + key, 'valueDigest': digest(a)},
                    'destination': {'inputRole': 'EFFECT_INTENT', 'pointer': '/' + array + '/' + str(n) + '/' + key, 'valueDigest': digest(b)},
                    'disposition': 'PASS' if exact and same(a, b) else 'FAIL'})
                observe_comparisons([comparisons[-1]], findings=findings, depends_on=membership)
        for n, binding in enumerate(intent[array]):
            path = '/' + array + '/' + str(n)
            entry = {'binding': binding, 'pointer': path, 'sourceDisposition': 'NOT_EVALUATED'}
            matches = [v for v in sources if same(v['binding'], binding)]
            observe_selection('SELECTED_' + kind, sources, matches, binding=binding,
                origins=[read_origin('EFFECT_INTENT', path)],
                findings=findings)
            if len(matches) != 1:
                missing.append({'role': 'EXACT_SELECTED_' + kind + '_ORIGINAL', 'pointer': path, 'binding': binding})
            else:
                source = matches[0]
                entry.update(sourceInputId=source['id'], rawSha256=source['rawSha256'], valueDigest=source['valueDigest'])
                if source['id'] in traced:
                    ids.append(source['id'])
                    entry.update(sourceDisposition='PASS', schemaBinding=traced[source['id']]['schemaBinding'])
                elif unresolved.get(source['id'], {}).get('reason') == 'SELECTED_SOURCE_SCHEMA_MISMATCH':
                    entry['sourceDisposition'] = 'FAIL'
                    errors.append({'code': 'SELECTED_' + kind + '_SOURCE_SCHEMA_MISMATCH', 'pointer': path,
                                   'sourceInputId': source['id']})
                else:
                    missing.append({'role': 'EXACT_SELECTED_' + kind + '_SOURCE_FORMAT', 'pointer': path, 'binding': binding})
                missing.append({'role': 'EXISTING_' + kind + '_OWNER_APPLICABILITY_AND_USE', 'pointer': path,
                                'binding': binding, 'sourceInputId': source['id']})
            selected.append(entry)
        outputs[gate] = {'disposition': 'FAIL' if errors else 'NOT_EVALUATED' if missing else 'PASS',
            'errors': errors, 'remainingRoles': missing, 'comparisons': comparisons, 'sourceInputIds': sorted(set(ids)),
            'selectedOriginals': selected,
            'qualification': 'Exact explicit body-to-selected revision consistency and original-source inspection only. Existing owner applicability, governed selection and eligible use remain separate.'}
    return outputs
