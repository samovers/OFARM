"""Build and validate the actual PR23/PR43-shaped domain payload.

Input selection is domain-owned configuration, not a new authorization record.
Selected foreign bindings are retained in FAIL payloads while their actual
owner gates remain failed or unavailable. No field is an admission override.
"""
import json
from pathlib import Path
from strict_inputs import parse, sha, digest, same, InputError
from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

HERE = Path(__file__).resolve().parent
TRACE_ID = 'https://ofarm.dev/schema/drafts/non-default/authorization-finalization-evidence/protected-effect-validation-trace/v0.1'
PAYLOAD_ID = 'https://ofarm.dev/schema/drafts/non-default/assertion-record-domain-validation/payload/v0.4'
PAYLOAD_VERSION = 'ofarm.assertionRecordDomainValidationPayload.v0.4'
PAYLOAD_SCHEMA_RAW_SHA256 = '674c84e2c8fe56da2c10e95dd25957d323f911f5771ff86bf04ba5381e278557'
CLOSURE_SCHEMA_RAW_SHA256 = '133af8f25a06f7eea180875cc33bd20f357f832ecd506de5dbbafb3a549d0b85'
PROTECTED_IDENTITY_FIELDS = {'actionClass', 'storageOwnerRef', 'transactionAttemptId',
                             'atomicPersistenceBoundaryRef', 'proposedAssertionId'}


def record_ref(name):
    return {'$ref': TRACE_ID + '#/$defs/' + name}


SELECTION_SCHEMA_RAW_SHA256 = 'b0f5ffdc4e97ab745c6e666dcbbeef8ee4485efdb265251904f5447e966b03d9'
SELECTION_V0_5_SCHEMA_RAW_SHA256 = '3928be7c89dc3a4547415b21938f6f79256627171508384270beb968118942b5'
SELECTION_SCHEMAS = {
    'ofarm.assertionDomainEvaluationSelection.v0.4': (
        'schemas/evaluation-selection.schema.json', SELECTION_SCHEMA_RAW_SHA256,
        'https://ofarm.dev/schema/drafts/non-default/assertion-domain/evaluation-selection/v0.4'),
    'ofarm.assertionDomainEvaluationSelection.v0.5': (
        'schemas/evaluation-selection-v0_5.schema.json', SELECTION_V0_5_SCHEMA_RAW_SHA256,
        'https://ofarm.dev/schema/drafts/non-default/assertion-domain/evaluation-selection/v0.5'),
}
SELECTED_SCHEMAS = [
    ('components/revision-02/sources/OFARM/389a8f6b6bb2/03_machine_contracts/drafts_non_default/assertion_record_submission/OFARM_AssertionRecord_schema_v0_2.json',
     '3a7044086a2b0a226109ac00b361332503d77b07efd602b29402662515b67f1e',
     'https://ofarm.dev/schema/assertionrecord/v0.2'),
    ('outer/payload-schema.json',
     '1a1622fdce7d4437c5d63afbb6888e17a01c89dba8fb363cf7a051ace6493add',
     'https://ofarm.dev/schema/drafts/non-default/assertion-record-domain-validation/payload/v0.1'),
    ('schemas/evaluation-selection.schema.json', SELECTION_SCHEMA_RAW_SHA256,
     'https://ofarm.dev/schema/drafts/non-default/assertion-domain/evaluation-selection/v0.4'),
    ('schemas/immutable-input-closure.schema.json', CLOSURE_SCHEMA_RAW_SHA256,
     'https://ofarm.dev/schema/drafts/non-default/assertion-domain/immutable-input-closure/v0.3'),
    ('source-contracts/ProtectedEffectValidationTrace.schema.json', 'a5150119555a2faaa0531ae96e650dcefd5cb491fa30fd8ffe337c873f6cdae3', TRACE_ID),
    ('schemas/payload.schema.json', PAYLOAD_SCHEMA_RAW_SHA256, PAYLOAD_ID),
]


def registry(selection_version='ofarm.assertionDomainEvaluationSelection.v0.4'):
    def reject(uri):
        raise InputError('Unselected schema reference: ' + uri)
    selected = Registry(retrieve=reject)
    for relative, expected, uri in SELECTED_SCHEMAS:
        if relative == 'schemas/evaluation-selection.schema.json':
            if selection_version not in SELECTION_SCHEMAS:
                raise InputError('Unsupported evaluation selection version.')
            relative, expected, uri = SELECTION_SCHEMAS[selection_version]
        raw = (HERE / relative).read_bytes()
        if sha(raw) != expected:
            raise InputError('Selected schema byte pin mismatch: ' + relative)
        schema = parse(raw)
        if '$id' in schema and schema['$id'] != uri:
            raise InputError('Selected schema ID mismatch: ' + relative)
        selected = selected.with_resource(uri, Resource.from_contents(schema, default_specification=DRAFT202012))
    return selected


def validate_selection(raw, expected_hash, intent):
    if sha(raw) != expected_hash:
        raise InputError('Evaluation selection differs from its independent raw-byte pin.')
    value = parse(raw)
    version = value.get('schemaVersion') if isinstance(value, dict) else None
    if version not in SELECTION_SCHEMAS:
        raise InputError('Unsupported evaluation selection version.')
    relative, expected_schema_hash, _uri = SELECTION_SCHEMAS[version]
    schema_raw = (HERE / relative).read_bytes()
    if sha(schema_raw) != expected_schema_hash:
        raise InputError('Reviewed selection schema bytes differ.')
    schema = parse(schema_raw)
    errors = list(Draft202012Validator(schema, registry=registry(version)).iter_errors(value))
    if errors:
        raise InputError('Evaluation selection schema: ' + errors[0].message)
    if value['effectIntent']['digest'] != digest(intent):
        raise InputError('Evaluation selection binds a different complete intent value.')
    selectors = value.get('sourceSelections', [])
    if len({digest(v['binding']) for v in selectors}) != len(selectors):
        raise InputError('Duplicate independently selected immutable source binding.')
    originals = value['originalSelections']
    if len({v['inputId'] for v in originals}) != len(originals) or len({v['ref'] for v in originals}) != len(originals):
        raise InputError('Duplicate selected original identity or reference.')
    from original_inputs import validate_condition_property_revision_sources
    validate_condition_property_revision_sources(value)
    return value


def _diagnostic(error):
    return {'code': error['code'], 'inputRole': 'DOMAIN_COMPARISON', 'pointer': error.get('pointer', '')}


def expected_payload_schema_binding():
    """Use the reviewed contract rule: schema digests hash exact file bytes.

    Contract and payload value digests use JCS, but schemaDigest is the exact
    schema-file SHA-256 under the pinned PHASE_A contract rule.
    """
    raw = (HERE / 'schemas/payload.schema.json').read_bytes()
    if sha(raw) != PAYLOAD_SCHEMA_RAW_SHA256:
        raise InputError('Reviewed v0.4 payload schema bytes differ.')
    schema = parse(raw)
    if schema.get('$id') != PAYLOAD_ID or schema.get('properties', {}).get('schemaVersion', {}).get('const') != PAYLOAD_VERSION:
        raise InputError('Reviewed v0.4 payload schema identity differs.')
    return {'schemaRef': PAYLOAD_ID, 'schemaVersion': PAYLOAD_VERSION,
            'schemaDigest': 'sha256:' + sha(raw), 'canonicalization': 'JCS_RFC8785_SHA256'}


def require_payload_contract(contract):
    """A v0.1 contract cannot silently authorize a v0.4 payload."""
    if not isinstance(contract, dict) or not same(contract.get('payloadSchemaBinding'), expected_payload_schema_binding()):
        raise InputError('Domain contract has not selected the exact reviewed v0.4 payload schema.')


def require_completed_contract_for_payload(contract):
    """An incomplete draft cannot authorize any public payload."""
    if (not isinstance(contract, dict) or contract.get('implementationCompleteness') != 'COMPLETE'
            or contract.get('status') in (None, 'DRAFT_NON_DEFAULT_CONSTRUCTION')):
        raise InputError('Domain contract is still explicitly incomplete construction.')


def require_selected_closure(selection, report):
    """Bind a schema-valid complete or partial closure to guarded originals."""
    closure = report.get('immutableInputClosure')
    if not isinstance(closure, dict):
        raise InputError('Selected v0.3 immutable-input closure is unavailable.')
    raw = (HERE / 'schemas/immutable-input-closure.schema.json').read_bytes()
    if sha(raw) != CLOSURE_SCHEMA_RAW_SHA256:
        raise InputError('Reviewed v0.3 immutable-input closure schema bytes differ.')
    schema = parse(raw)
    errors = list(Draft202012Validator(schema, registry=registry()).iter_errors(closure))
    if errors:
        raise InputError('Immutable-input closure schema: ' + errors[0].message)
    observed = report.get('originalInventory', {}).get('selectionBinding', {})
    if (closure['selectionBinding']['rawSha256'] != observed.get('rawSha256')
            or closure['selectionBinding']['wholeJcsDigest'] != observed.get('wholeJcsDigest')
            or closure['selectionBinding']['wholeJcsDigest'] != digest(selection)):
        raise InputError('Immutable-input closure does not bind the independently pinned evaluation selection.')
    checked_rows = report.get('originalInventory', {}).get('inventory')
    selected_ids = [row['inputId'] for row in selection['originalSelections']]
    closure_rows = closure['inventory']
    if not isinstance(checked_rows, list) or not (len(closure_rows) == len(checked_rows) == len(selected_ids)):
        raise InputError('Immutable-input closure inventory differs from the guarded original inventory.')
    closure_by_id = {row['inputId']: row for row in closure_rows}
    checked_by_id = {row.get('inputId'): row for row in checked_rows if isinstance(row, dict)}
    if (len(closure_by_id) != len(closure_rows) or len(checked_by_id) != len(checked_rows)
            or len(set(selected_ids)) != len(selected_ids)
            or set(closure_by_id) != set(selected_ids)
            or set(checked_by_id) != set(selected_ids)
            or any(not same(closure_by_id[iid], checked_by_id[iid]) for iid in selected_ids)):
        raise InputError('Immutable-input closure inventory differs from the guarded original inventory.')
    if closure['protectedState']['status'] == 'OBSERVED':
        state = report.get('ownerReports', {}).get('state', {})
        serialization = report.get('ownerInvocations', {}).get('state', {}).get('ownerReportSerialization', {})
        if (closure['protectedState']['ownerStatus'] != state.get('status')
                or closure['protectedState']['reportRawSha256'] != serialization.get('rawSha256')
                or closure['protectedState']['reportWholeJcsDigest'] != digest(state)):
            raise InputError('Immutable-input closure does not bind the actual selected owner report.')
    return closure


def require_complete_closure(selection, report):
    """PASS requires complete derivation and every protected comparison."""
    closure = require_selected_closure(selection, report)
    if (closure['derivation']['status'] != 'COMPLETE' or closure['derivation']['blockedInputIds']
            or closure['protectedState']['status'] != 'OBSERVED'):
        raise InputError('Immutable-input closure is partial or protected state is not observed.')
    if any(row['outcome']['disposition'] != 'PASS'
           for group in ('readComparisons', 'guardComparisons')
           for row in closure['protectedState'][group]):
        raise InputError('Immutable-input closure retains an unmatched protected-state obligation.')
    return closure


def _closure_obligation_digest(closure):
    protected = closure['protectedState']
    reads = [row['expected'] for row in protected['readComparisons']]
    guards = protected['guardComparisons']
    return digest({
        'reads': sorted(reads, key=lambda row: row['key']),
        'negativeReads': sorted((row['expected'] for row in guards if row['kind'] == 'NEGATIVE'),
                                key=lambda row: row['key']),
        'setReads': sorted((row['expected'] for row in guards if row['kind'] == 'SET'),
                           key=lambda row: row['key']),
        'writes': [row['expected'] for row in guards if row['kind'] == 'WRITE'],
    })


def require_complete_protected_comparison(report, closure=None, *, derived_identities=None):
    """Bind C4 to identities derived outside offered #51 artifacts and facts."""
    if (type(derived_identities) is not dict or set(derived_identities) != PROTECTED_IDENTITY_FIELDS
            or any(type(value) is not str or not value for value in derived_identities.values())):
        raise InputError('Independent protected-state identity vector is unavailable.')
    value = report.get('protectedStateComparison')
    state = report.get('ownerReports', {}).get('state')
    if not isinstance(state, dict):
        raise InputError('Exact selected state owner report is unavailable.')
    if (not isinstance(closure, dict) or not isinstance(value, dict) or value.get('status') != 'PASS'
            or value.get('expectedDerivationStatus') != 'COMPLETE'
            or value.get('comparisonScope') != 'CONDITIONAL_TECHNICAL_ONLY'
            or value.get('ownerStatus') != 'CONDITIONAL_CONFORMANCE_PASS'
            or state.get('status') != value.get('ownerStatus')
            or value.get('ownerReportWholeJcsDigest') != digest(state)
            or value.get('sourceAdmission') != 'NOT_ESTABLISHED'
            or value.get('runtimeProtection') != 'NOT_ESTABLISHED'
            or value.get('errors') != []
            or not isinstance(value.get('comparisons'), list)
            or not value['comparisons']
            or any(row.get('disposition') != 'PASS' for row in value['comparisons'] if isinstance(row, dict))
            or any(not isinstance(row, dict) for row in value['comparisons'])
            or value.get('expectedObligationDigest') != _closure_obligation_digest(closure)):
        raise InputError('Complete independently derived protected-state comparison has not passed.')
    if (value.get('expectedIdentityDigest') != digest(derived_identities)
            or not same(value.get('expectedIdentities'), derived_identities)):
        raise InputError('Protected-state comparison does not bind independent domain identities.')
    pins = value.get('artifactPins')
    inventory = {row['inputId']: row['result'] for row in closure['inventory']}
    protected = closure['protectedState']
    if (not isinstance(pins, dict) or set(pins) != {'contextRawSha256', 'policyRawSha256',
                                                 'proofRawSha256', 'snapshotRawSha256'}
            or any(inventory.get(protected[part + 'InputId'], {}).get('observedRawSha256')
                   != pins[part + 'RawSha256']
                   for part in ('context', 'policy', 'proof', 'snapshot'))):
        raise InputError('Protected-state comparison is not bound to the selected original artifacts.')
    return value


def overall_disposition(report, closure):
    """Retain an independent FAIL and never infer PASS from local rows alone."""
    mapping = report.get('mappingFindings')
    postconditions = report.get('postconditionFindings')
    if (not isinstance(mapping, list) or not isinstance(postconditions, list)
            or len(mapping) != 29 or len(postconditions) != 20
            or any(not isinstance(row, dict) for row in mapping + postconditions)):
        raise InputError('The 49 ordered domain duties are incomplete.')
    findings = mapping + postconditions
    semantic = closure['semanticDependencies']
    protected = closure['protectedState']
    independent_failure = (
        any(row.get('disposition') == 'FAIL' for row in findings)
        or bool(report.get('failedDependencyIds'))
        or closure['closure']['disposition'] == 'FAIL'
        or any(row['result']['status'] == 'MISMATCH' for row in closure['inventory'])
        or any(row['outcome']['disposition'] == 'FAIL' for row in closure['requirements'])
        or any(row['outcome']['disposition'] == 'FAIL' for row in semantic.values())
        or (protected['status'] in ('OBSERVED', 'PARTIAL')
            and any(row['outcome']['disposition'] == 'FAIL'
                    for group in ('readComparisons', 'guardComparisons')
                    for row in protected[group])))
    if independent_failure:
        return 'FAIL'
    all_semantic_ready = all(row['outcome']['disposition'] in ('PASS', 'NOT_APPLICABLE')
                             for row in semantic.values())
    public_findings = {
        **{'/mappingFindings/' + str(index): row for index, row in enumerate(mapping)},
        **{'/postconditionFindings/' + str(index): row for index, row in enumerate(postconditions)},
    }
    if (report.get('status') == 'CONDITIONAL_CONFORMANCE_PASS'
            and closure['closure']['disposition'] == 'PASS'
            and _constituents_ready_for_pass(closure)
            and _finding_links_structurally_complete(closure, public_findings)
            and all_semantic_ready
            and all(row.get('disposition') in ('PASS', 'NOT_APPLICABLE') for row in findings)):
        # The v0.3 link rows do not identify independently derived roots for
        # each public finding. A closed internal graph can still attribute an
        # unrelated requirement to every finding. C3 must derive and compare
        # that relation before any public PASS is available.
        raise InputError('Independent finding-to-requirement attribution is unavailable.')
    raise InputError('No independently established public payload disposition is available.')


def _constituents_ready_for_pass(closure):
    """A PASS label cannot hide a conflicting inventory, occurrence or use."""
    inventory = closure.get('inventory')
    requirements = closure.get('requirements')
    uses = closure.get('uses')
    roots = closure.get('rootInputIds')
    if (not isinstance(inventory, list) or not inventory
            or not isinstance(requirements, list) or not requirements
            or not isinstance(uses, list) or not isinstance(roots, list) or not roots):
        return False
    input_ids = [row.get('inputId') for row in inventory if isinstance(row, dict)]
    requirement_ids = [row.get('id') for row in requirements if isinstance(row, dict)]
    if (len(input_ids) != len(inventory) or len(set(input_ids)) != len(input_ids)
            or len(requirement_ids) != len(requirements)
            or len(set(requirement_ids)) != len(requirement_ids)
            or not set(roots) <= set(input_ids)):
        return False
    if any(row.get('result', {}).get('status') != 'MATCHED' for row in inventory):
        return False
    inventory_by_id = {row['inputId']: row['result'] for row in inventory}
    for row in requirements:
        if (row.get('outcome', {}).get('disposition') not in ('PASS', 'NOT_APPLICABLE')
                or not set(row.get('inputIds', [])) <= set(input_ids)
                or not set(row.get('dependsOn', [])) <= set(requirement_ids)):
            return False
    protected = closure.get('protectedState', {})
    if protected.get('status') != 'OBSERVED':
        return False
    reads = protected.get('readComparisons', [])
    guards = protected.get('guardComparisons', [])
    read_by_key = {row['key']: row for row in reads}
    if len(read_by_key) != len(reads):
        return False
    for row in reads:
        if (row.get('outcome', {}).get('disposition') != 'PASS'
                or row.get('inputId') not in inventory_by_id
                or row.get('expected', {}).get('key') != row.get('key')
                or inventory_by_id[row['inputId']]['observedRawSha256']
                    != row['expected']['rawSha256']
                or not set(row.get('requirementIds', [])) <= set(requirement_ids)):
            return False
    for row in guards:
        if (row.get('outcome', {}).get('disposition') != 'PASS'
                or row.get('expected', {}).get('key') != row.get('key')
                or not set(row.get('requirementIds', [])) <= set(requirement_ids)):
            return False
    for row in uses:
        if (not isinstance(row, dict) or row.get('requirementId') not in requirement_ids
                or row.get('inputId') not in input_ids
                or row.get('treatment', {}).get('kind') == 'NOT_EVALUATED'):
            return False
        treatment = row['treatment']
        if treatment['kind'] == 'PROTECTED_READ':
            selected_read = read_by_key.get(treatment['key'])
            if (selected_read is None or selected_read['inputId'] != row['inputId']
                    or row['requirementId'] not in selected_read['requirementIds']):
                return False
        if (treatment['kind'] == 'DERIVED_TRANSPORT'
                and not set(treatment['sourceInputIds']) <= set(input_ids)):
            return False
    return True


def _finding_links_structurally_complete(closure, expected_findings, *, exact=False):
    """Check pointer coverage and graph edges without granting attribution.

    The early disposition gate checks the 49 known duties; the final gate
    additionally resolves atom predicates and rejects any extra pointer.
    """
    links = closure.get('findingLinks')
    if not isinstance(links, list) or not isinstance(expected_findings, dict):
        return False
    pointers = [row.get('payloadPointer') for row in links if isinstance(row, dict)]
    if len(pointers) != len(links) or len(set(pointers)) != len(pointers):
        return False
    if not set(expected_findings) <= set(pointers) or (exact and set(pointers) != set(expected_findings)):
        return False
    requirements = closure.get('requirements', [])
    uses = closure.get('uses', [])
    protected = closure.get('protectedState', {})
    if not isinstance(requirements, list) or not isinstance(uses, list) or not isinstance(protected, dict):
        return False
    req_by_id = {row['id']: row for row in requirements}
    use_by_id = {row['id']: row for row in uses}
    reads = protected.get('readComparisons', [])
    guards = protected.get('guardComparisons', [])
    if (len(req_by_id) != len(requirements) or len(use_by_id) != len(uses)
            or not isinstance(reads, list) or not isinstance(guards, list)):
        return False
    for link in links:
        pointer = link['payloadPointer']
        if pointer not in expected_findings:
            continue  # Atom pointers are checked after their findings are built.
        finding = expected_findings[pointer]
        if (finding.get('disposition') not in ('PASS', 'NOT_APPLICABLE')
                or not (finding.get('id') or finding.get('predicateId'))):
            return False
        requirement_ids = link['requirementIds']
        use_ids = link['useIds']
        read_keys = link['readKeys']
        guard_refs = link['guardRefs']
        required = set(requirement_ids)
        if (not required or len(required) != len(requirement_ids)
                or not required <= set(req_by_id)
                or any(not set(req_by_id[rid]['dependsOn']) <= required for rid in required)
                or len(set(use_ids)) != len(use_ids)
                or set(use_ids) != {uid for uid, use in use_by_id.items()
                                    if use['requirementId'] in required}
                or len(set(read_keys)) != len(read_keys)
                or set(read_keys) != {row['key'] for row in reads
                                     if required.intersection(row['requirementIds'])}):
            return False
        actual_guards = {(row['kind'], row['key']) for row in guards
                         if required.intersection(row['requirementIds'])}
        selected_guards = [(row['kind'], row['key']) for row in guard_refs]
        if len(set(selected_guards)) != len(selected_guards) or set(selected_guards) != actual_guards:
            return False
    return True


def derive_available_fields(intent, result, action, selection, report, contract):
    """Derive bound v0.4 fields without presenting a public payload or verdict.

    These values have local original/contract/selection inputs. This helper does
    not supply a finding graph, protected-state comparison or admission.
    """
    if action not in contract['actions'] or selection['effectIntent']['digest'] != digest(intent):
        raise InputError('Selected action or complete intent binding differs.')
    selected = contract['actions'][action]
    subject, subject_time = intent['subject'], intent['subjectTime']
    return {'schemaVersion': PAYLOAD_VERSION,
            'proposedResultDigest': digest(result), 'effectIntentDigest': digest(intent),
            'protectedEffectContractDigest': contract['contractDigest'],
            'selectedActionBodySchemaBinding': selected['bodySchemaBinding'],
            'authorizationResult': selection['authorizationResult'],
            'currentActionRuleBinding': selection['currentActionRuleBinding'],
            'effectIntent': selection['effectIntent'],
            'effectIntentSchemaBinding': selected['intentSchemaBinding'],
            'proposedResult': {'resultId': result['assertionRecordId'],
                               'resultRef': result['assertionRecordId'],
                               'resultDigest': digest(result),
                               'resultSchemaBinding': contract['resultSchemaBinding']},
            'protectedEffectContractBinding': {key: contract[key] for key in
                                               ('contractId', 'contractVersion', 'contractRef', 'contractDigest')},
            'selectedAction': action, 'recordCommitClass': selected['recordCommitClass'],
            'subjectDigest': digest(subject),
            'soleAuthorityScopeDigest': digest(intent['resources'][0]['scope']),
            'subjectTimeDigest': digest(subject_time),
            'subjectTimeProfile': subject_time['profile'],
            'claimProjectionDigest': report['claimProjectionDigest'],
            'exactRenderedText': report['exactRenderedText']}


def build(intent, result, action, selection, report):
    contract = parse((HERE / 'domain-contract.json').read_bytes())
    if digest({k: v for k, v in contract.items() if k != 'contractDigest'}) != contract['contractDigest']:
        raise InputError('Domain contract whole-value digest is inconsistent.')
    require_payload_contract(contract)
    require_completed_contract_for_payload(contract)
    closure = require_selected_closure(selection, report)
    overall = overall_disposition(report, closure)
    if overall == 'PASS':
        require_complete_closure(selection, report)
        require_complete_protected_comparison(report, closure)
    resolved_inputs = report.get('resolvedOwnerInputs', []) + report.get('resolvedDomainInputs', [])
    resolved_ids = {v['id'] for v in resolved_inputs}
    def owner_ids(owner):
        return [v['id'] for v in resolved_inputs if v['id'].startswith(owner + ':')]
    def comparisons(finding, atom_pointer=None):
        out = []
        for c in finding['comparisons']:
            if all(k in c for k in ['source', 'destination', 'disposition']):
                entry={k: c[k] for k in ['predicateId', 'source', 'destination', 'disposition']}
                if atom_pointer is not None:
                    for side in ['source', 'destination']:
                        if entry[side]['inputRole'].startswith('ATOM:'):
                            entry[side]={**entry[side], 'inputRole':'EFFECT_INTENT',
                                         'pointer':atom_pointer+entry[side]['pointer']}
                out.append(entry)
                continue
            if 'sourceValueDigest' not in c or 'destinationValueDigest' not in c:
                continue  # Absence has no value digest; the duty still records it.
            source_role, source_pointer = 'EFFECT_INTENT', c['sourcePointer']
            destination_role = 'EFFECT_INTENT' if c['predicateId'] in ['body.performerRef', 'body.applicability'] else 'PROPOSED_RESULT'
            if source_pointer == '/selectedConstant':
                source_role = 'DOMAIN_CONTRACT'
                source_pointer = '/actions/' + action + '/predicateConstants/' + c['predicateId']
            out.append({'predicateId': c['predicateId'],
                        'source': {'inputRole': source_role, 'pointer': source_pointer, 'valueDigest': c['sourceValueDigest']},
                        'destination': {'inputRole': destination_role, 'pointer': c['destinationPointer'], 'valueDigest': c['destinationValueDigest']},
                        'disposition': 'PASS' if c['equal'] else 'FAIL'})
        return out
    def operand_availability(items,atom_pointer=None):
        findings=[]
        for comparison in items:
            if 'operandAvailability' not in comparison:continue
            entry={'predicateId':comparison['predicateId']}
            for side,original in comparison['operandAvailability'].items():
                operand=dict(original)
                if atom_pointer is not None and operand['inputRole'].startswith('ATOM:'):
                    operand['inputRole']='EFFECT_INTENT'
                    for key in ['pointer','ancestorPointer']:
                        if key in operand:operand[key]=atom_pointer+operand[key]
                entry[side]=operand
            findings.append(entry)
        return findings
    def finding(value):
        identity_gate = {'AR_SUBJECT_SCOPE_PROOF': 'SUBJECT_SCOPE_RELATION',
                         'AR_OPERATION_PERFORMER': 'PERFORMER_IDENTITY'}.get(value['id'])
        identity_ids = report.get('identitySourceComparisons', {}).get(identity_gate, {}).get('sourceInputIds', [])
        authorization_ids = report.get('authorizationSourceComparisons', {}).get('sourceInputIds', []) if value['id'] in ['AR_ACTION_PROFILE', 'AR_ASSERTOR'] else []
        event_ids = report.get('eventSourceComparisons', {}).get('sourceInputIds', []) if value['id'] == 'AR_EVENT_ASSOCIATION' else []
        temporal_ids = report.get('temporalSources', {}).get('sourceInputIds', []) if value['id'] == 'AR_SUBJECT_TIME' else []
        evidence_ids = report.get('evidenceSourceComparisons', {}).get('sourceInputIds', []) if value['id'] == 'AR_EVIDENCE' else []
        compliance_gate = {'AR_COMPLIANCE_RULES': 'COMPLIANCE_RULE_SELECTION',
                           'AR_COMPLIANCE_EVIDENCE_POLICY': 'EVIDENCE_POLICY_SELECTION'}.get(value['id'])
        compliance_ids = report.get('complianceSourceComparisons', {}).get(compliance_gate, {}).get('sourceInputIds', [])
        context_ids = report.get('contextSourceComparisons', {}).get('sourceInputIds', []) if value['id'] == 'AR_BODY' else []
        availability=operand_availability(value['comparisons'])
        return {'id': value['id'], 'disposition': value['disposition'],
                'comparisons': comparisons(value), 'resolvedInputIds': sorted({v for v in identity_ids + authorization_ids + event_ids + temporal_ids + evidence_ids + compliance_ids + context_ids if v in resolved_ids}),
                'diagnostics': [_diagnostic(e) for e in value['diagnostics']],
                **({'operandAvailabilityFindings':availability} if availability else {}),
                **({'failedPrerequisites': value['failedPrerequisites']} if 'failedPrerequisites' in value else {}),
                **({'branchReason': value['branchReason']} if 'branchReason' in value else {})}
    body = intent['assertionBody']
    payload = {**derive_available_fields(intent, result, action, selection, report, contract),
               'assertionAct': {'posture': intent['assertionActPosture'], 'assertedAt': intent['assertedAt'],
                                 'assertingPartyRef': result['assertedByPartyRef'], 'resolvedInputIds': owner_ids('act')},
               'subjectTimeComparisons': [c for f in report['mappingFindings'] if f['id'] == 'AR_SUBJECT_TIME' for c in comparisons(f)],
               'resolvedInputs': resolved_inputs, 'mappingFindings': [finding(v) for v in report['mappingFindings']],
               'postconditionFindings': [finding(v) for v in report['postconditionFindings']],
               'atomFindings': [], 'overallDisposition': overall,
               'immutableInputClosure': closure}
    if 'assertionActEvidenceBinding' in intent:
        payload['assertionAct']['evidenceBinding'] = intent['assertionActEvidenceBinding']
    if action == 'ASSERT_OPERATION_CLAIM':
        payload['operationPerformerAuthorityDisposition'] = 'NOT_EVALUATED_BY_AUTHORIZATION'
    def atoms(p):
        if p['form'] == 'ATOM':
            yield p
        elif 'child' in p:
            yield from atoms(p['child'])
        else:
            for child in p['children']:
                yield from atoms(child)
    definitions = parse((HERE / 'domain-definitions.json').read_bytes())['definitions']
    for atom in atoms(body['proposition']):
        row = atom['definition'].split(':')[-1]
        definition = next(v for v in definitions if v['id'] == row)
        # Owned predicates record INDETERMINATE until their complete selected
        # source-use conjunction has been evaluated; ANY/NOT cannot erase it.
        # FAIL here rejects a source/claim validation, not the proposition
        # itself. It must not become logical FALSE for a later NOT fold.
        automatic = next((a for a in report.get('automaticSourceComparisons', {}).get('atoms', []) if a['atomId'] == atom['atomId']), None)
        source_gate = next(d for d in report['dependencyFindings'] if d['id'] == 'DOMAIN_MEANING')
        atom_disposition = automatic['disposition'] if automatic else source_gate['disposition']
        diagnostics = automatic['errors'] if automatic else source_gate['diagnostics']
        predicate = {'predicateId': 'COMPLETE_SOURCE_MEANING:' + row, 'disposition': atom_disposition,
                     'comparisons': comparisons({'comparisons': automatic.get('comparisons', []) + automatic.get('sourceInterpretation', {}).get('comparisons', [])}, automatic['pointer']) if automatic else [],
                     'resolvedInputIds': [v for v in automatic.get('sourceInputIds', []) if v in resolved_ids] if automatic else [], 'diagnostics': [_diagnostic(e) for e in diagnostics],
                     'failedPrerequisites': sorted(set(r['role'] for r in automatic['remainingRoles'])) if automatic and atom_disposition == 'NOT_EVALUATED'
                     else ['DOMAIN_MEANING'] if atom_disposition == 'NOT_EVALUATED' else []}
        availability=operand_availability(automatic.get('comparisons',[])+automatic.get('sourceInterpretation',{}).get('comparisons',[]),automatic['pointer']) if automatic else []
        if availability: predicate['operandAvailabilityFindings'] = availability
        payload['atomFindings'].append({'atomId': atom['atomId'],
                                       'definitionBinding': {'ref': atom['definition'], 'digest': digest(definition)},
                                       'scopeDigest': digest(atom['scope']), 'bodyDigest': digest(atom['body']),
                                       'interpretation': 'TRUE' if atom_disposition == 'PASS' else 'INDETERMINATE', 'predicateFindings': [predicate]})
    if 'associatedSemanticEventBinding' not in intent:
        payload['eventAssociation'] = {'disposition': 'NOT_APPLICABLE'}
    else:
        # A revision without resolved bytes cannot be mislabeled as a digest.
        event = report.get('ownerReports', {}).get('event')
        binding = intent['associatedSemanticEventBinding']
        event_domain = report.get('eventSourceComparisons', {})
        resolution = event_domain.get('selectedEnvelopeResolution', {})
        resolved = resolution.get('resolvedBinding', {}).get('digest') if same(resolution.get('selectedBinding'), binding) else None
        envelope_digest = binding.get('digest') or resolved
        duty = next(v for v in report['mappingFindings'] if v['id'] == 'AR_EVENT_ASSOCIATION')
        payload['eventAssociation'] = {'disposition': duty['disposition'],
                                      'selectedEnvelopeBinding': binding,
                                      'compatibilityFindings': comparisons(duty),
                                      'failedPrerequisites': duty.get('failedPrerequisites', []),
                                      'diagnostics': [_diagnostic(e) for e in duty['diagnostics']]}
        unresolved = []
        if envelope_digest:
            payload['eventAssociation']['envelope'] = {'ref': binding['ref'], 'digest': envelope_digest}
        else:
            unresolved.append('EVENT_ENVELOPE_DIGEST')
        if report.get('eventCaseDefinitionBinding') is not None:
            payload['eventAssociation']['caseDefinitionBinding'] = report['eventCaseDefinitionBinding']
        else:
            unresolved.append('EVENT_MEANING_CASE_DEFINITION')
        if unresolved:
            if duty['disposition'] == 'PASS':
                raise InputError('A passing event duty cannot have unresolved event selections.')
            finding = payload['eventAssociation']
            finding['unresolvedSelections'] = unresolved
            finding['failedPrerequisites'] = sorted(set(finding['failedPrerequisites'] + unresolved))
            finding['diagnostics'].extend(_diagnostic({'code': role + '_UNRESOLVED',
                'pointer': '/associatedSemanticEventBinding'}) for role in unresolved)
        if 'directSubjectIndex' in event_domain:
            payload['eventAssociation']['subjectMatch']={'mode':'DIRECT','subjectRefsIndex':event_domain['directSubjectIndex']}
        if 'directAnchorIndex' in event_domain:
            payload['eventAssociation']['anchorScopesIndex']=event_domain['directAnchorIndex']
        if 'envelopePrimaryFamily' in event_domain:
            payload['eventAssociation']['envelopePrimaryFamily']=event_domain['envelopePrimaryFamily']
        event_gate = next(v for v in report['dependencyFindings'] if v['id'] == 'EVENT_OWNER')
        if event and event.get('status')=='CONDITIONAL_CONFORMANCE_PASS' and event_gate['disposition']=='PASS':
            payload['eventAssociation']['ingressEvidence']=event['proofBinding']
            payload['eventAssociation']['ingressPrimaryFamily']=event['classification']['authoritativePrimaryFamily']
    if body['assertionPosture'] == 'INITIAL':
        payload['correction'] = {'posture': 'INITIAL'}
    else:
        duty = next(v for v in report['mappingFindings'] if v['id'] == 'AR_CORRECTION_LINEAGE')
        payload['correction'] = {'posture': 'CORRECTION', 'selectedPriorBinding': intent['supersedesAssertionRecordBinding'],
                                  'comparisons': comparisons(duty), 'failedPrerequisites': duty.get('failedPrerequisites', [])}
        if 'correctionContext' in report:
            payload['correction'].update(report['correctionContext'])
    if overall == 'PASS':
        public_findings = {
            **{'/mappingFindings/' + str(index): row
               for index, row in enumerate(payload['mappingFindings'])},
            **{'/postconditionFindings/' + str(index): row
               for index, row in enumerate(payload['postconditionFindings'])},
            **{'/atomFindings/' + str(index) + '/predicateFindings/' + str(predicate_index): predicate
               for index, atom in enumerate(payload['atomFindings'])
               for predicate_index, predicate in enumerate(atom['predicateFindings'])},
        }
        if not _finding_links_structurally_complete(closure, public_findings, exact=True):
            raise InputError('Public findings lack complete independently linked source requirements.')
    schema = parse((HERE / 'schemas/payload.schema.json').read_bytes())
    failures = list(Draft202012Validator(schema, registry=registry()).iter_errors(payload))
    if failures:
        raise InputError('Constructed domain payload does not conform: ' + failures[0].message)
    return payload
