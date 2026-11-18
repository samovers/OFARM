"""Reviewed three-valued composition over recomputed atom findings.

This module is called inside the private component worker, after intrinsic and
original-source checks. It accepts no public atom-result override. A source
validation failure is not a false proposition. All children, exact qualifier
values and explicit order comparisons remain visible, including under ANY.
The result is an internal conditional interpretation, never accepted truth.
"""
from pathlib import Path
from strict_inputs import parse, digest

HERE = Path(__file__).resolve().parent
VALUES = {'TRUE', 'FALSE', 'INDETERMINATE'}


def fold(form, values):
    """Pure algebra helper; inputs are internal child results, not owner flags."""
    if not values or any(v not in VALUES for v in values):
        raise ValueError('A nonempty list of three-valued child results is required.')
    if form == 'NOT':
        if len(values) != 1:
            raise ValueError('NOT requires exactly one child.')
        return {'TRUE': 'FALSE', 'FALSE': 'TRUE', 'INDETERMINATE': 'INDETERMINATE'}[values[0]]
    if form in ['ALL', 'SEQUENCE']:
        return 'FALSE' if 'FALSE' in values else 'TRUE' if all(v == 'TRUE' for v in values) else 'INDETERMINATE'
    if form == 'ANY':
        return 'TRUE' if 'TRUE' in values else 'FALSE' if all(v == 'FALSE' for v in values) else 'INDETERMINATE'
    raise ValueError('Unsupported logical form.')


def evaluate(intent, automatic, time_bounds):
    rules = parse((HERE / 'proposition-rules.json').read_bytes())
    findings = automatic.get('atoms', [])
    by_id = {}
    for i, finding in enumerate(findings):
        if finding['atomId'] in by_id:
            raise ValueError('Duplicate recomputed atom finding.')
        by_id[finding['atomId']] = (i, finding)
    atoms, qualifications, orders = [], [], []

    def reference(path, value):
        return {'inputRole': 'EFFECT_INTENT', 'pointer': path, 'valueDigest': digest(value)}

    def walk(p, path):
        form = p['form']
        node = {'form': form, 'source': reference(path, p)}
        if form == 'ATOM':
            selected = by_id.get(p['atomId'])
            index, finding = selected if selected else (None, {})
            # PASS is a conjunction of complete source meaning and use roles.
            # A matched scalar or conditional subcomparison is insufficient.
            complete = (finding.get('disposition') == 'PASS'
                        and not finding.get('errors') and not finding.get('remainingRoles'))
            value = 'TRUE' if complete else 'INDETERMINATE'
            node.update(atomId=p['atomId'], interpretation=value,
                        scopeDigest=digest(p['scope']), bodyDigest=digest(p['body']),
                        sourceValidationDisposition=finding.get('disposition', 'NOT_EVALUATED'),
                        sourceFindingPointer='/automaticSourceComparisons/atoms/' + str(index) if selected else None,
                        remainingRoles=finding.get('remainingRoles', []),
                        diagnostics=finding.get('errors', []))
            if 'conditionalMathematicalOutcome' in finding.get('sourceInterpretation', {}):
                # NOT_SATISFIED can be the correctly alleged result of a
                # criterion. It is not FALSE for the complete assertion atom.
                node['conditionalMathematicalOutcome'] = finding['sourceInterpretation']['conditionalMathematicalOutcome']
            atoms.append(node)
            return node
        if form in ['NOT', 'QUALIFIED']:
            child = walk(p['child'], path + '/child')
            node['child'] = child
            if form == 'NOT':
                node['interpretation'] = fold(form, [child['interpretation']])
            else:
                # Qualification scopes this exact allegation. It neither
                # rewrites the child nor creates source eligibility, precision
                # or a probability. Source-quality meaning remains part of
                # the source checks, separate from preserving this wrapper.
                node.update(appliesToAtomId=p['appliesToAtomId'], qualifiers=p['qualifiers'],
                            qualifierSource=reference(path + '/qualifiers', p['qualifiers']),
                            interpretation=child['interpretation'],
                            qualificationScope='EXACT_CHILD_ALLEGATION_NOT_UNQUALIFIED_TRUTH')
                qualifications.append({'atomId': p['appliesToAtomId'], 'source': node['qualifierSource'],
                                       'qualifiers': p['qualifiers']})
            return node
        children = [walk(child, path + '/children/' + str(i)) for i, child in enumerate(p['children'])]
        node['children'] = children
        values = [child['interpretation'] for child in children]
        if form == 'SEQUENCE':
            leaves = {}
            def collect(q, pointer):
                if q['form'] == 'ATOM':
                    leaves[q['atomId']] = (q, pointer)
                elif 'child' in q:
                    collect(q['child'], pointer + '/child')
                else:
                    for i, c in enumerate(q['children']):
                        collect(c, pointer + '/children/' + str(i))
            collect(p, path)
            node['orderFindings'] = []
            for i, relation in enumerate(p['orderRelations']):
                before, before_path = leaves[relation['beforeAtomId']]
                after, after_path = leaves[relation['afterAtomId']]
                before_time = before['scope']['subjectTime']; after_time = after['scope']['subjectTime']
                _, end = time_bounds(before_time); start, _ = time_bounds(after_time)
                value = 'INDETERMINATE' if end is None else 'TRUE' if end < start else 'FALSE'
                order = {'relationSource': reference(path + '/orderRelations/' + str(i), relation),
                         'before': reference(before_path + '/scope/subjectTime', before_time),
                         'after': reference(after_path + '/scope/subjectTime', after_time),
                         'interpretation': value, 'scope': 'STRICT_ORDER_OF_DECLARED_CHILD_TIMES'}
                node['orderFindings'].append(order); orders.append(order); values.append(value)
        node['interpretation'] = fold(form, values)
        return node

    tree = walk(intent['assertionBody']['proposition'], '/assertionBody/proposition')
    if set(by_id) != {v['atomId'] for v in atoms}:
        raise ValueError('Recomputed atom findings do not exactly cover the proposition.')
    return {'scope': 'CONDITIONAL_PROPOSITION_INTERPRETATION_NOT_ACCEPTED_TRUTH',
            'rulesBinding': {'ref': rules['definitionId'], 'digest': digest(rules)},
            'interpretation': tree['interpretation'], 'tree': tree,
            'atomFindings': atoms, 'qualifications': qualifications, 'orderFindings': orders,
            'mandatorySourceDisposition': 'FAIL' if automatic['errors'] else 'NOT_EVALUATED' if automatic['remainingRoles'] else 'PASS',
            'mandatoryGates': 'EVERY_DOMAIN_AUTHORITY_EVIDENCE_AND_TRANSACTION_GATE_REMAINS_INDEPENDENT',
            'qualification': 'The fold preserves exact qualifiers and every child finding. It does not independently validate source-quality claims or complete outstanding source-use roles.'}
