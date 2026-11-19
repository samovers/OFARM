"""Partial domain check of one proposed AssertionRecord write and ID absence.

The expected ID and content pins come from a guarded, schema-valid public
proposed original, never from #51 context, proof, or snapshot. The exact
INSERT shape and ID-absence purpose follow the pinned #51 technical contract.
No transaction owner, predicate digest, version, full read set, source
admission, or runtime protection is inferred here.
"""

from strict_inputs import InputError, parse
import protected_identity_provenance


ABSENCE_PURPOSE = 'ASSERTION_ID_ABSENCE'


def _result(status, provenance, checks, diagnostics, expected=None):
    return {'schemaVersion': 'candidate.partialProtectedKnownWrite.v0.1',
            'status': status, 'comparisonScope': 'KNOWN_PROPOSED_WRITE_AND_ID_ABSENCE_ONLY',
            'identityProvenance': provenance,
            'expectedKnown': expected, 'comparisons': checks, 'diagnostics': diagnostics,
            'unresolved': ['INDEPENDENT_TRANSACTION_STORAGE_IDENTITIES',
                           'ARTIFACT_ROLE_PINS', 'COMPLETE_READ_NEGATIVE_SET_WRITE_OBLIGATIONS',
                           'ABSENCE_PREDICATE_DIGEST_AND_GUARD_VERSIONS',
                           'ACTUAL_SOURCE_ADMISSION_AND_RUNTIME_PROTECTION'],
            'sourceAdmission': 'NOT_ESTABLISHED', 'runtimeProtection': 'NOT_ESTABLISHED',
            'qualification': 'Known contradiction may fail; matching rows cannot complete C4.'}


def compare(independent_selected_action, original_result_bytes, *, selection_bytes=None,
            independent_selection_raw_sha256=None, checked_inventory=None,
            partial_requirement_graph=None, context_bytes=None, proof_bytes=None,
            snapshot_bytes=None):
    """Compare fixed domain write facts to offered #51 artifacts, never PASS.

    The caller must have verified the candidate package and selected actual
    #51 owner artifacts. This function independently reruns the guarded
    proposed-result provenance check; a caller-supplied PASS flag is forbidden.
    Missing selection or invalid result schema leaves the known write pending.
    """
    try:
        provenance = protected_identity_provenance.derive(
            independent_selected_action, original_result_bytes,
            selection_bytes=selection_bytes,
            independent_selection_raw_sha256=independent_selection_raw_sha256,
            checked_inventory=checked_inventory,
            partial_requirement_graph=partial_requirement_graph)
    except InputError:
        return _result('FAIL', None, [], [{'code': 'INDEPENDENT_ACTION_INVALID'}])
    proposed = provenance['fields']['proposedAssertionId']
    if proposed['disposition'] == 'FAIL':
        return _result('FAIL', provenance, [], proposed['diagnostics'])
    if proposed['disposition'] != 'PASS':
        return _result('NOT_EVALUATED', provenance, [], proposed['diagnostics'])

    identity = proposed['value']
    source = proposed['source']
    expected_write = {'operation': 'INSERT', 'recordType': 'AssertionRecord',
                      'key': identity,
                      'binding': {'ref': identity, 'digest': source['wholeJcsDigest']},
                      'rawSha256': source['rawSha256']}
    expected = {'actionClass': independent_selected_action,
                'proposedAssertionId': identity, 'proposedWrite': expected_write,
                'idAbsence': {'key': identity, 'purpose': ABSENCE_PURPOSE},
                'derivation': {'proposedOriginalInputId': source['inputId'],
                               'proposedOriginalRawSha256': source['rawSha256'],
                               'proposedOriginalWholeJcsDigest': source['wholeJcsDigest'],
                               'resultSchemaRawSha256': source['resultSchemaRawSha256'],
                               'actionPointer': '/package/selectedAction'}}
    documents, diagnostics = {}, []
    for name, raw in (('context', context_bytes), ('proof', proof_bytes),
                      ('snapshot', snapshot_bytes)):
        if raw is None:
            documents[name] = None
            diagnostics.append({'code': 'OFFERED_ARTIFACT_UNAVAILABLE', 'artifact': name})
            continue
        if type(raw) is not bytes:
            documents[name] = None
            diagnostics.append({'code': 'OFFERED_ARTIFACT_BYTES_INVALID', 'artifact': name})
            continue
        try:
            value = parse(raw)
        except InputError:
            documents[name] = None
            diagnostics.append({'code': 'OFFERED_ARTIFACT_JSON_INVALID', 'artifact': name})
            continue
        if type(value) is not dict:
            documents[name] = None
            diagnostics.append({'code': 'OFFERED_ARTIFACT_SHAPE_INVALID', 'artifact': name})
            continue
        documents[name] = value

    checks = []
    def check(artifact, key, actual, wanted):
        checks.append({'artifact': artifact, 'key': key,
                       'disposition': 'PASS' if type(actual) is type(wanted) and actual == wanted else 'FAIL',
                       'code': 'KNOWN_WRITE_FACT_MATCH' if type(actual) is type(wanted) and actual == wanted
                       else 'KNOWN_WRITE_FACT_CONTRADICTION'})

    context = documents['context']
    if context is not None:
        check('context', 'actionClass', context.get('actionClass'), independent_selected_action)
        check('context', 'proposedAssertionId', context.get('proposedAssertionId'), identity)
        check('context', 'proposedAssertion', context.get('proposedAssertion'),
              {'binding': expected_write['binding'], 'rawSha256': expected_write['rawSha256']})
    proof = documents['proof']
    if proof is not None:
        check('proof', 'proposedDomainWrites', proof.get('proposedDomainWrites'), [expected_write])
    for name, member in (('context', 'requiredNegativeReads'),
                         ('proof', 'negativeGuards'), ('snapshot', 'negativeRecords')):
        document = documents[name]
        if document is None:
            continue
        rows = document.get(member)
        if type(rows) is not list:
            checks.append({'artifact': name, 'key': member,
                           'disposition': 'FAIL', 'code': 'ID_ABSENCE_ROWS_INVALID'})
            continue
        selected = [row for row in rows if type(row) is dict
                    and row.get('purpose') == ABSENCE_PURPOSE]
        matched = len(selected) == 1 and selected[0].get('key') == identity
        checks.append({'artifact': name, 'key': member,
                       'disposition': 'PASS' if matched else 'FAIL',
                       'code': 'ID_ABSENCE_KEY_MATCH' if matched else 'ID_ABSENCE_KEY_CONTRADICTION'})

    failure = (any(row['disposition'] == 'FAIL' for row in checks)
               or any(row['code'] != 'OFFERED_ARTIFACT_UNAVAILABLE' for row in diagnostics))
    return _result('FAIL' if failure else 'NOT_EVALUATED', provenance, checks,
                   diagnostics, expected)
