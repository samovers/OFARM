"""Bind selected originals to exact public roots after byte inventory.

This is a domain-owned construction component. The caller supplies the actual
guarded original-inventory report, not a verdict flag. PASS here means only an
exact root/byte/value selection comparison. It never admits source use, proves
storage protection, or completes the #47 domain verdict.
"""

from strict_inputs import InputError, digest, parse, sha


def validate_condition_property_revision_sources(selection):
    """Check optional v0.5 references without interpreting rule or map bytes."""
    from owner_calls import validate_condition_property_revision_sources as validate
    try:
        validate(selection)
    except ValueError as exc:
        raise InputError(str(exc)) from exc


def selected_index(selection_bytes, checked_inventory):
    """Check the inventory's one-to-one relationship with the pinned selection.

    The guarded original-inventory worker must already have produced this
    report. Rechecking its exact shape prevents later graph code from silently
    shortening or overwriting a selected original.
    """
    if not isinstance(selection_bytes, bytes) or not isinstance(checked_inventory, dict):
        raise InputError('Selection bytes and a checked inventory report are required.')
    selection = parse(selection_bytes)
    validate_condition_property_revision_sources(selection)
    if (checked_inventory.get('status') != 'ORIGINAL_INVENTORY'
            or checked_inventory.get('selectionBinding', {}).get('rawSha256') != sha(selection_bytes)):
        raise InputError('The checked inventory does not bind these selection bytes.')
    pins = selection.get('originalSelections')
    rows = checked_inventory.get('inventory')
    admitted = checked_inventory.get('admittedJson')
    if not isinstance(pins, list) or not isinstance(rows, list) or not isinstance(admitted, dict):
        raise InputError('Checked inventory shape is incomplete.')
    if len(pins) != len(rows):
        raise InputError('Checked inventory does not cover every selected original.')
    by_id, by_ref, results = {}, {}, {}
    for pin, row in zip(pins, rows):
        if (not isinstance(pin, dict) or not isinstance(row, dict)
                or row.get('inputId') != pin.get('inputId')
                or pin.get('inputId') in by_id or pin.get('ref') in by_ref):
            raise InputError('Selected original IDs, refs or inventory order conflict.')
        result = row.get('result')
        if not isinstance(result, dict) or result.get('status') not in {'MATCHED', 'MISMATCH', 'NOT_EVALUATED'}:
            raise InputError('Unknown checked original result.')
        iid = pin['inputId']
        if iid in admitted:
            if (pin.get('digestMode') != 'JCS_JSON' or result['status'] != 'MATCHED'
                    or digest(admitted[iid]) != pin.get('wholeJcsDigest')):
                raise InputError('Admitted JSON conflicts with the checked original selection.')
        elif pin.get('digestMode') == 'JCS_JSON' and result['status'] == 'MATCHED':
            raise InputError('Matched JSON original is absent from the admitted value map.')
        by_id[iid] = pin
        by_ref[pin['ref']] = pin
        results[iid] = result
    if set(admitted) - set(by_id):
        raise InputError('Unselected JSON appeared in the admitted value map.')
    return selection, by_id, by_ref, results, admitted


def _finding(role, binding, by_ref, results, *, original_bytes=None,
             context_raw_sha=None, absent_disposition='FAIL'):
    findings = []
    if not isinstance(binding, dict) or not isinstance(binding.get('ref'), str):
        return {'role': role, 'disposition': 'FAIL', 'inputId': None,
                'diagnostics': [{'code': 'ROOT_BINDING_MALFORMED'}]}
    pin = by_ref.get(binding['ref'])
    if pin is None:
        return {'role': role, 'disposition': absent_disposition, 'inputId': None,
                'diagnostics': [{'code': 'ROOT_NOT_IN_INDEPENDENT_SELECTION'
                                 if absent_disposition == 'FAIL' else 'SEPARATELY_PINNED_CONTROL_PENDING',
                                 'ref': binding['ref']}]}
    iid = pin['inputId']
    if pin.get('digestMode') != 'JCS_JSON' or binding.get('digest') != pin.get('wholeJcsDigest'):
        findings.append({'code': 'ROOT_VALUE_OR_MODE_MISMATCH'})
    if context_raw_sha is not None and context_raw_sha != pin['rawSha256']:
        findings.append({'code': 'ROOT_CONTEXT_RAW_PIN_MISMATCH'})
    if original_bytes is not None:
        if not isinstance(original_bytes, bytes):
            findings.append({'code': 'ROOT_ORIGINAL_NOT_BYTES'})
        elif sha(original_bytes) != pin['rawSha256'] or len(original_bytes) != pin['byteLength']:
            findings.append({'code': 'ROOT_PUBLIC_ORIGINAL_RAW_MISMATCH'})
    result = results[iid]
    if result['status'] == 'MISMATCH':
        findings.append({'code': 'ROOT_SELECTED_ORIGINAL_MISMATCH', 'reason': result.get('reason')})
    disposition = ('FAIL' if findings else
                   'NOT_EVALUATED' if result['status'] == 'NOT_EVALUATED' else 'PASS')
    if result['status'] == 'NOT_EVALUATED' and not findings:
        findings.append({'code': 'ROOT_SELECTED_ORIGINAL_UNAVAILABLE'})
    return {'role': role, 'disposition': disposition, 'inputId': iid,
            'selectedRef': pin['ref'], 'selectedRawSha256': pin['rawSha256'],
            'diagnostics': findings,
            'qualification': 'Exact selection only; no source admission or runtime protection.'}


def bind_roots(selection_bytes, checked_inventory, original_intent_bytes,
               original_result_bytes, *, selected_state_context=None, original_bytes=None):
    """Compare independently selected intent/result roots without inputId names.

    `selected_state_context` must be the context of an actually recomputed #51
    owner report. Its proposedAssertion is the result selection; if that context
    is unavailable, the proposed root stays NOT_EVALUATED. The caller must keep
    the owner report and its qualifications separate from these local findings.
    """
    if not isinstance(original_intent_bytes, bytes) or not isinstance(original_result_bytes, bytes):
        raise InputError('Public intent and proposed result originals must be bytes.')
    selection, by_id, by_ref, results, admitted = selected_index(selection_bytes, checked_inventory)
    intent = _finding('EFFECT_INTENT', selection.get('effectIntent'), by_ref, results,
                      original_bytes=original_intent_bytes)
    if selected_state_context is None:
        proposed = {'role': 'PROPOSED_ASSERTION', 'disposition': 'NOT_EVALUATED',
                    'inputId': None, 'diagnostics': [{'code': 'SELECTED_STATE_CONTEXT_UNAVAILABLE'}]}
    elif not isinstance(selected_state_context, dict):
        proposed = {'role': 'PROPOSED_ASSERTION', 'disposition': 'FAIL',
                    'inputId': None, 'diagnostics': [{'code': 'SELECTED_STATE_CONTEXT_MALFORMED'}]}
    else:
        proposal = selected_state_context.get('proposedAssertion')
        if not isinstance(proposal, dict):
            proposed = {'role': 'PROPOSED_ASSERTION', 'disposition': 'FAIL',
                        'inputId': None, 'diagnostics': [{'code': 'SELECTED_PROPOSED_ASSERTION_MISSING'}]}
        else:
            proposed = _finding('PROPOSED_ASSERTION', proposal.get('binding'), by_ref, results,
                                original_bytes=original_result_bytes,
                                context_raw_sha=proposal.get('rawSha256'))
            if 'rawSha256' not in proposal:
                proposed['diagnostics'].append({'code': 'SELECTED_PROPOSED_RAW_PIN_MISSING'})
                proposed['disposition'] = 'FAIL'
        effect = selected_state_context.get('effectIntent')
        if (not isinstance(effect, dict)
                or effect.get('binding') != selection.get('effectIntent')
                or effect.get('rawSha256') != sha(original_intent_bytes)):
            intent['diagnostics'].append({'code': 'SELECTED_STATE_INTENT_MISMATCH'})
            intent['disposition'] = 'FAIL'
    authorization = _finding('AUTHORIZATION_RESULT', selection.get('authorizationResult'),
                             by_ref, results, absent_disposition='NOT_EVALUATED')
    rule = selection.get('currentActionRuleBinding', {})
    current_rule = _finding('CURRENT_ACTION_RULE',
                            {'ref': rule.get('ruleRef'), 'digest': rule.get('ruleDigest')},
                            by_ref, results, absent_disposition='NOT_EVALUATED')
    if current_rule['disposition'] == 'PASS' and rule.get('ruleRevisionSelector'):
        current_rule['disposition'] = 'NOT_EVALUATED'
        current_rule['diagnostics'].append({'code': 'RULE_REVISION_RESOLUTION_PENDING'})
        current_rule['revisionQualification'] = 'Selected rule revision requires its separate owner resolver.'
    bound = {'scope': 'EXACT_ROOT_BINDINGS_ONLY_NOT_FULL_CLOSURE',
             'selection': selection, 'pinsById': by_id, 'pinsByRef': by_ref,
             'inventoryResults': results, 'admittedJson': admitted,
             'roots': {'effectIntent': intent, 'proposedAssertion': proposed,
                       'authorizationResult': authorization, 'currentActionRule': current_rule}}
    if selection.get('schemaVersion') == 'ofarm.assertionDomainEvaluationSelection.v0.5':
        # Internal transport only. A consumer must recheck these exact bytes
        # against independent pins; parsed JSON is never reserialized as raw.
        bound['originalBytes'] = dict(original_bytes or {})
        bound['selectionRawSha256'] = sha(selection_bytes)
    return bound
