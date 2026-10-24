"""Offline conformance of independently selected pre-verdict storage evidence.

No database, authorization, transaction, network or signing operation is performed.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import importlib.metadata
import json
import math
import re
from pathlib import Path

MAX_BYTES = 2097152
MAX_BUNDLE = 16777216
MAX_DEPTH = 64
PREFIX = 'https://ofarm.dev/schema/drafts/non-default/protected-state-evidence/'
EXIT = {'CONDITIONAL_CONFORMANCE_PASS': 0, 'FAIL': 1, 'INPUT_ERROR': 2, 'DEPENDENCY_UNAVAILABLE': 3}


class InputError(ValueError):
    pass


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def strict_json(raw):
    if not isinstance(raw, bytes) or len(raw) > MAX_BYTES or raw.startswith(b'\xef\xbb\xbf'):
        raise InputError('Expected original UTF-8 JSON bytes without BOM, at most 2 MiB.')
    def pairs(items):
        value = {}
        for k, v in items:
            if k in value:
                raise InputError('Duplicate object key: ' + k)
            value[k] = v
        return value
    def invalid(value):
        raise InputError('Non-finite numeric token: ' + value)
    try:
        value = json.loads(raw.decode('utf-8'), object_pairs_hook=pairs, parse_constant=invalid)
    except (UnicodeError, ValueError, RecursionError) as exc:
        raise InputError(str(exc)) from exc
    def visit(v, depth):
        if depth > MAX_DEPTH:
            raise InputError('JSON nesting exceeds 64.')
        if isinstance(v, str):
            try:
                v.encode('utf-8')
            except UnicodeError as exc:
                raise InputError('Invalid Unicode scalar value.') from exc
        elif type(v) is int and abs(v) > 9007199254740991:
            raise InputError('Integer exceeds interoperable JCS safe-integer range.')
        elif type(v) is float and not math.isfinite(v):
            raise InputError('Non-finite number.')
        elif isinstance(v, dict):
            for k, item in v.items():
                visit(k, depth + 1)
                visit(item, depth + 1)
        elif isinstance(v, list):
            for item in v:
                visit(item, depth + 1)
    visit(value, 0)
    return value


def pointer(value, path):
    if path == '':
        return value
    if not isinstance(path, str) or not path.startswith('/') or re.search(r'~(?![01])', path):
        raise InputError('Invalid JSON pointer.')
    for raw in path[1:].split('/'):
        key = raw.replace('~1', '/').replace('~0', '~')
        if isinstance(value, dict) and key in value:
            value = value[key]
        elif isinstance(value, list) and re.fullmatch(r'0|[1-9][0-9]*', key) and int(key) < len(value):
            value = value[int(key)]
        else:
            raise InputError('JSON pointer does not resolve: ' + path)
    return value


def safe_path(root, relative):
    if not isinstance(relative, str) or Path(relative).is_absolute() or '..' in Path(relative).parts:
        raise InputError('Package pin path must be relative and contained.')
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file():
        raise InputError('Pinned package file is absent or outside its root: ' + relative)
    return path


def verify_state(proof_bytes, *, package_root, selected, context_bytes, policy_bytes,
                 snapshot_bytes, records, source_root=None):
    report = {'schemaVersion': 'ofarm.preVerdictProtectedStateReport.v0.1', 'status': 'INPUT_ERROR',
              'runtimeProtection': 'NOT_ESTABLISHED', 'laterTransactionGate': 'NOT_EVALUATED',
              'errors': [], 'checks': [], 'bindings': {}}
    def identifier(code):
        return code if len(code) <= 4096 else code[:4000] + ':sha256:' + sha(code.encode('utf-8'))
    def error(code, path, detail):
        report['errors'].append({'code': identifier(code), 'path': path, 'detail': str(detail)[:4096] or code[:4096]})
    def check(code, ok, detail):
        report['checks'].append({'id': identifier(code), 'disposition': 'PASS' if ok else 'FAIL', 'detail': detail[:4096]})
        if not ok:
            error(code, '', detail)
        return ok
    # These exact runtime versions are dependencies, not runtime trust anchors.
    try:
        for name, version in [('rfc8785', '0.1.4'), ('jsonschema', '4.26.0')]:
            if importlib.metadata.version(name) != version:
                raise ImportError(name + ' version ' + version + ' is required.')
        import rfc8785
        from jsonschema import Draft202012Validator
        from jsonschema.exceptions import SchemaError
        from referencing import Registry, Resource
        from referencing.exceptions import Unresolvable
        import package_contract
    except (ImportError, importlib.metadata.PackageNotFoundError) as exc:
        report['status'] = 'DEPENDENCY_UNAVAILABLE'
        error('DEPENDENCY_UNAVAILABLE', '', exc)
        return report
    def canonical(v):
        try:
            return rfc8785.dumps(v)
        except (ValueError, TypeError) as exc:
            raise InputError(str(exc)) from exc
    def digest(v):
        return 'sha256:' + sha(canonical(v))
    def equal(a, b):
        return canonical(a) == canonical(b)
    def binding(v, ref):
        return {'ref': ref, 'digest': digest(v)}
    validators = {}
    validators['report'] = Draft202012Validator(package_contract.REPORT_SCHEMA)
    def validate(name, v):
        errors = sorted(validators[name].iter_errors(v), key=lambda e: (list(map(str, e.absolute_path)), e.message))
        if errors:
            for e in errors[:16]:
                error('SCHEMA', '/' + '/'.join(map(str, e.absolute_path)), name + ': ' + e.message)
            return False
        return True
    def finish():
        # The output schema is pinned before semantic evaluation. Early package
        # errors still have the same fixed envelope; no success facts are emitted.
        if report['status'] != 'CONDITIONAL_CONFORMANCE_PASS':
            report.pop('facts', None)
        if 'report' in validators:
            output_errors = list(validators['report'].iter_errors(report))
            if output_errors:
                raise RuntimeError('Implementation produced a nonconforming report: ' + output_errors[0].message)
        return report
    try:
        root = Path(package_root).resolve()
        if Path(package_contract.__file__).resolve() != Path(__file__).resolve().parent / 'package_contract.py':
            raise InputError('Frozen package schema module is outside the selected checker directory.')
        if not isinstance(records, dict) or not all(isinstance(k, str) and isinstance(v, bytes) for k, v in records.items()):
            raise InputError('records must map exact string refs to original byte strings.')
        raws = [proof_bytes, context_bytes, policy_bytes, snapshot_bytes, *records.values()]
        if not all(isinstance(v, bytes) for v in raws) or sum(len(v) for v in raws) > MAX_BUNDLE:
            raise InputError('Input bundle exceeds 16 MiB or contains values other than bytes.')
        if any(len(v) > MAX_BYTES for v in raws):
            raise InputError('An input record exceeds 2 MiB.')
        contract_raw = safe_path(root, 'contract.json').read_bytes()
        contract = strict_json(contract_raw)
        if not isinstance(selected, dict) or sha(contract_raw) != selected.get('contractRawSha256'):
            raise InputError('Contract does not match independent selected raw hash.')
        if not isinstance(contract, dict) or not all(isinstance(contract.get(k), list) for k in ['schemas', 'sources', 'checker']):
            raise InputError('Malformed package pin lists.')
        if contract['schemas'] != package_contract.SCHEMA_PINS or contract['sources'] != package_contract.SOURCE_PINS:
            raise InputError('Package schema/source closure is not supported by this checker revision.')
        if {p.get('path') for p in contract['checker'] if isinstance(p, dict)} != {'verify_state.py', 'package_contract.py'}:
            raise InputError('Incomplete or unknown checker code closure.')
        schemas = {}
        path_seen = set()
        for group in ['schemas', 'sources', 'checker']:
            for pin in contract[group]:
                if not isinstance(pin, dict) or set(pin) != {'path', 'rawSha256'}:
                    raise InputError('Malformed package pin.')
                key = (group, pin['path'])
                if key in path_seen:
                    raise InputError('Duplicate package pin.')
                path_seen.add(key)
                base = Path(__file__).resolve().parent if group == 'checker' else (Path(source_root).resolve() if group == 'sources' and source_root is not None else root)
                raw = safe_path(base, pin['path']).read_bytes()
                if sha(raw) != pin['rawSha256']:
                    raise InputError('Package raw-byte pin mismatch: ' + pin['path'])
                if group == 'schemas':
                    s = strict_json(raw)
                    Draft202012Validator.check_schema(s)
                    if '$id' not in s or s['$id'] in schemas:
                        raise InputError('Schema ID is absent or duplicated.')
                    schemas[s['$id']] = s
        registry = Registry().with_resources([(key, Resource.from_contents(v)) for key, v in schemas.items()])
        for name in ['policy', 'context', 'snapshot', 'creation', 'proof', 'selection', 'contract', 'report']:
            key = PREFIX + name + '/v0.1'
            if key not in schemas:
                raise InputError('Required owned schema absent: ' + name)
            validators[name] = Draft202012Validator(schemas[key], registry=registry)
        if not validate('contract', contract) or not validate('selection', selected):
            return finish()
        unhashed = {k: v for k, v in contract.items() if k != 'contractDigest'}
        if digest(unhashed) != contract['contractDigest']:
            raise InputError('Contract self digest mismatch.')
        if contract['dependencies'] != {'rfc8785': '0.1.4', 'jsonschema': '4.26.0'}:
            raise InputError('Dependency contract mismatch.')
        context, policy, snapshot, proof = map(strict_json, [context_bytes, policy_bytes, snapshot_bytes, proof_bytes])
        structurally_valid = [validate(name, v) for name, v in [('context', context), ('policy', policy), ('snapshot', snapshot), ('proof', proof)]]
        if not all(structurally_valid):
            return finish()
        if sha(context_bytes) != selected['contextRawSha256'] or sha(policy_bytes) != selected['policyRawSha256']:
            raise InputError('Context or policy does not match independent selected raw hash.')
        def mode(spec):
            return spec.get('digestMode', 'JCS_JSON')
        modes = {}
        for spec in context['requiredReads']:
            ref = spec['binding']['ref']
            if ref in modes and modes[ref] != mode(spec):
                raise InputError('One ref cannot use more than one digest mode: ' + ref)
            modes[ref] = mode(spec)
        # Core records and source-pointer inputs keep their structured meaning.
        structured = [context[k] for k in ['effectIntent', 'transactionProfile', 'transactionTimePolicy', 'proposedAssertion']]
        structured += list(context.get('priorAssertion', {}).values())
        if any(modes.get(s['binding']['ref'], 'JCS_JSON') != 'JCS_JSON' for s in structured):
            raise InputError('A structured core input cannot be selected as RAW_BYTES.')
        parsed = {key: strict_json(raw) for key, raw in records.items() if modes.get(key, 'JCS_JSON') == 'JCS_JSON'}
        for value in parsed.values():
            canonical(value)
        # Canonical timestamp spelling is inherited verbatim from the actual
        # attempt schema; datetime additionally rejects impossible calendar values.
        attempt = context['attempt']
        try:
            for key in ['transactionStartedAt', 'transactionDeadline']:
                if not re.fullmatch(r'[0-9]{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12][0-9]|3[01])T(?:[01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9](?:\.[0-9]{0,5}[1-9])?Z', attempt[key]):
                    raise ValueError('Noncanonical or out-of-range timestamp component.')
            times = [dt.datetime.fromisoformat(attempt[k].replace('Z', '+00:00'))
                     for k in ['transactionStartedAt', 'transactionDeadline']]
        except ValueError as exc:
            raise InputError('Invalid attempt calendar timestamp.') from exc
        check('ATTEMPT_DEADLINE', times[0] < times[1], 'The selected attempt deadline is after its start.')
        cb = binding(context, context['contextId'])
        sb = binding(snapshot, snapshot['snapshotId'])
        pb = binding(policy, policy['policyId'])
        eb = binding(proof, proof['proofId'])
        report['bindings'] = {'context': cb, 'snapshot': sb, 'guardPolicy': pb, 'proof': eb}
        check('INDEPENDENT_PROOF_BINDING', equal(eb, selected['proofBinding']), 'Offered proof matches its independent immutable selection.')
        check('CONTEXT_BINDING', equal(cb, proof['context']), 'Proof binds the complete selected context.')
        check('SNAPSHOT_BINDING', equal(sb, proof['snapshot']) and equal(sb, attempt['transactionSnapshot']), 'Proof and actual attempt context bind the selected transaction-start snapshot.')
        check('POLICY_BINDING', equal(pb, proof['guardPolicy']) and equal(pb, attempt['guardPolicyBinding']), 'Proof and attempt bind the independently selected guard policy.')
        check('PROOF_ID', proof['proofId'] == context['proofId'], 'Proof has the expected identity.')
        check('OWNER', len({context['storageOwnerRef'], snapshot['storageOwnerRef'], proof['storageOwnerRef'], policy['storageOwnerRef']}) == 1, 'All records belong to the independently selected storage owner.')
        check('ATTEMPT', attempt['transactionAttemptId'] == snapshot['transactionAttemptId'] == proof['transactionAttemptId'], 'Snapshot and observations belong to this exact attempt.')
        check('ATOMIC_BOUNDARY', attempt['atomicPersistenceBoundaryRef'] == snapshot['atomicPersistenceBoundaryRef'] == policy['atomicPersistenceBoundaryRef'], 'Snapshot and policy name the attempt persistence boundary.')
        check('TIME_POLICY', equal(context['transactionTimePolicy']['binding'], attempt['transactionTimePolicyBinding']), 'Exact selected time-policy binding is preserved; its policy evaluation is external.')
        def by_key(items, label):
            result = {}
            for item in items:
                k = item['key']
                if k in result:
                    error('DUPLICATE_KEY', label, 'Duplicate observation key: ' + k)
                result[k] = item
            return result
        def verify_bytes(spec, label):
            ref = spec['binding']['ref']
            raw_mode = mode(spec) == 'RAW_BYTES'
            ok = ref in records and spec['rawSha256'] == sha(records[ref])
            ok = ok and (('digest' not in spec['binding']) if raw_mode else
                         (ref in parsed and spec['binding'].get('digest') == digest(parsed[ref])))
            check('BYTES_' + label, ok, 'Exact selected digest mode and original raw bytes: ' + ref)
            return parsed.get(ref) if ok else None
        def content_selection(spec):
            return {k: spec[k] for k in ['binding', 'rawSha256', 'revisionRef'] if k in spec} | {'digestMode': mode(spec)}
        def revision_consistent(spec):
            return ('revisionRef' not in spec or 'revisionRef' not in spec['binding'] or
                    spec['revisionRef'] == spec['binding']['revisionRef'])
        def late_artifact(value):
            if not isinstance(value, dict):
                return False
            current = attempt['transactionAttemptId']
            artifact_attempt = value.get('attempt', {})
            tied = (value.get('transactionAttemptId') == current or
                    isinstance(artifact_attempt, dict) and artifact_attempt.get('transactionAttemptId') == current)
            schema = value.get('schemaVersion')
            known_late = isinstance(schema, str) and schema in {'ofarm.notRequiredGovernedEffectReceipt.v0.1',
                                   'ofarm.notRequiredDecisionConsumption.v0.1',
                                   'ofarm.notRequiredTransactionAttempt.v0.1'}
            late_shape = ('checkpoint' in value or 'gateTraces' in value or
                          'governedEffectReceiptDigest' in value or 'decisionConsumptionDigest' in value or
                          'authorizationEvaluatedAt' in value and 'writeAuthorizationCheckedAt' in value or
                          'gateId' in value and 'disposition' in value)
            return tied and (known_late or late_shape)
        read_specs = by_key(context['requiredReads'], 'context.requiredReads')
        reads = by_key(proof['readGuards'], 'proof.readGuards')
        positives = by_key(snapshot['positiveRecords'], 'snapshot.positiveRecords')
        negatives = by_key(context['requiredNegativeReads'], 'context.requiredNegativeReads')
        negative_guards = by_key(proof['negativeGuards'], 'proof.negativeGuards')
        negative_snap = by_key(snapshot['negativeRecords'], 'snapshot.negativeRecords')
        sets = by_key(context['requiredSetReads'], 'context.requiredSetReads')
        set_guards = by_key(proof['setGuards'], 'proof.setGuards')
        set_snap = by_key(snapshot['setRecords'], 'snapshot.setRecords')
        committed_keys = {k for k, s in read_specs.items() if s['availability'] == 'COMMITTED_AT_TRANSACTION_START'}
        check('READ_COVERAGE', set(read_specs) == set(reads) and committed_keys == set(positives), 'All required reads have exact guards; all and only committed-at-start reads have positive snapshot observations.')
        check('NEGATIVE_COVERAGE', set(negatives) == set(negative_guards) == set(negative_snap), 'All and only selected negative reads have snapshot and guard observations.')
        check('SET_COVERAGE', set(sets) == set(set_guards) == set(set_snap), 'All and only selected set reads have snapshot and guard observations.')
        # One ref must have one immutable source meaning in this attempt. Multiple
        # roles can be represented by distinct keys with exactly identical bytes.
        ref_specs = {}
        ref_guards = {}
        for key, spec in read_specs.items():
            ref = spec['binding']['ref']
            bytespec = content_selection(spec)
            guarded_spec = bytespec | {k: spec[k] for k in ['availability', 'fixedInputVersion'] if k in spec}
            if ref in ref_specs:
                check('REF_CONSISTENCY_' + key, equal(ref_specs[ref], guarded_spec), 'Repeated refs keep the same bytes, revision, digest mode, availability and fixed version.')
            ref_specs[ref] = guarded_spec
            check('READ_REVISION_' + key, revision_consistent(spec), 'Outer and binding revision selectors do not disagree.')
            verify_bytes(spec, key)
            # A RAW_BYTES selection does not hide a recognized JSON later artifact.
            # Parsing here is detection only; it neither changes the original pin
            # nor imposes I-JSON/JCS requirements on opaque source bytes.
            value = parsed.get(ref)
            if mode(spec) == 'RAW_BYTES' and ref in records:
                try:
                    value = json.loads(records[ref].decode('utf-8'))
                except (UnicodeError, ValueError, RecursionError):
                    value = None
            check('NO_LATER_ARTIFACT_' + key, not late_artifact(value), 'A recognized current-attempt later transaction artifact cannot be pre-verdict input.')
            if key in reads:
                guard = reads[key]
                check('READ_AVAILABILITY_' + key, spec['availability'] == guard['availability'], 'The guard preserves the independently selected input availability posture.')
                check('GUARD_REVISION_' + key, revision_consistent(guard), 'The guard revision selectors agree.')
                versions = {k: guard[k] for k in ['snapshotVersion', 'fixedInputVersion', 'observedVersion'] if k in guard}
                if ref in ref_guards:
                    check('REF_GUARD_CONSISTENCY_' + key, equal(ref_guards[ref], versions), 'Repeated refs have one exact guarded version.')
                ref_guards[ref] = versions
            if key in reads and spec['availability'] == 'COMMITTED_AT_TRANSACTION_START' and key in positives and reads[key]['availability'] == spec['availability']:
                guard, observed = reads[key], positives[key]
                check('READ_BINDING_' + key,
                      equal(bytespec, content_selection(guard)) and equal(bytespec, content_selection(observed)) and revision_consistent(observed),
                      'The input, positive snapshot and read guard bind the same immutable bytes.')
                check('READ_VERSION_' + key, observed['rowVersion'] == guard['snapshotVersion'] == guard['observedVersion'], 'The read version is unchanged at the pre-verdict observation.')
            elif key in reads and spec['availability'] == 'FIXED_BEFORE_DOMAIN_VERDICT' and reads[key]['availability'] == spec['availability']:
                guard = reads[key]
                check('FIXED_INPUT_BINDING_' + key, equal(bytespec, content_selection(guard)), 'Exact bytes fixed before the domain verdict are guarded without claiming transaction-start visibility.')
                check('FIXED_INPUT_VERSION_' + key, spec['fixedInputVersion'] == guard['fixedInputVersion'] == guard['observedVersion'], 'The independently selected fixed input version is unchanged.')
        for key, spec in negatives.items():
            if key in negative_guards and key in negative_snap:
                g, s = negative_guards[key], negative_snap[key]
                check('NEGATIVE_PREDICATE_' + key, all(equal(spec[k], g[k]) and equal(spec[k], s[k]) for k in spec), 'Exact selected negative predicate and purpose are observed.')
                check('NEGATIVE_VERSION_' + key, s['guardVersion'] == g['snapshotVersion'] == g['observedVersion'], 'The negative predicate version is unchanged.')
        for key, spec in sets.items():
            if key in set_guards and key in set_snap:
                g, s = set_guards[key], set_snap[key]
                check('SET_PREDICATE_' + key, all(equal(spec[k], g[k]) and equal(spec[k], s[k]) for k in spec), 'Exact selected set predicate and ordered member bindings are observed.')
                check('SET_VERSION_' + key, s['guardVersion'] == g['snapshotVersion'] == g['observedVersion'], 'The set predicate version is unchanged.')
                members = spec['members']
                check('SET_UNIQUE_' + key, len({v['ref'] for v in members}) == len(members), 'Set member logical refs are unique.')
                positive_refs = {v['binding']['ref'] for v in positives.values()}
                def member_matches(v):
                    ref = v['ref']
                    if ref not in positive_refs or ref not in ref_specs:
                        return False
                    selected_read = ref_specs[ref]
                    expected = selected_read['binding']
                    if selected_read['digestMode'] == 'RAW_BYTES':
                        expected = expected | {'digestMode': 'RAW_BYTES', 'rawSha256': selected_read['rawSha256']}
                    return equal(v, expected)
                check('SET_MEMBERS_' + key, all(member_matches(v) for v in members), 'Every snapshot set member has an exact committed positive read and guard, preserving its digest mode.')
        proposed = verify_bytes(context['proposedAssertion'], 'PROPOSED_ASSERTION')
        for label, role in [('effectIntent', 'EFFECT_INTENT'), ('transactionProfile', 'TRANSACTION_PROFILE'), ('transactionTimePolicy', 'TRANSACTION_TIME_POLICY')]:
            verify_bytes(context[label], label)
            check('REQUIRED_ROLE_' + label, any(s['role'] == role and all(equal(context[label][k], s[k]) for k in ['binding', 'rawSha256']) for s in read_specs.values()), 'The selected ' + label + ' is a protected immutable read.')
        proposed_ref = context['proposedAssertion']['binding']['ref']
        check('INPUT_RECORD_SET', set(records) == set(ref_specs) | {proposed_ref}, 'No required record is absent and no unselected record is supplied.')
        check('RESULT_ID', isinstance(proposed, dict) and proposed.get('assertionRecordId') == context['proposedAssertionId'] == proposed_ref, 'Proposed result identity matches the independently selected key and binding.')
        expected_write = {'operation': 'INSERT', 'recordType': 'AssertionRecord', 'key': context['proposedAssertionId'], **context['proposedAssertion']}
        check('ONE_EXACT_INSERT', equal(proof['proposedDomainWrites'], [expected_write]), 'The entire pre-verdict domain write set is one exact assertion INSERT.')
        check('UNIQUE_PROPOSED_ID', proposed_ref not in ref_specs and not any(v['binding']['ref'] == proposed_ref for v in positives.values()), 'The proposed assertion does not already exist in the start snapshot.')
        unique = [v for v in negatives.values() if v['purpose'] == 'ASSERTION_ID_ABSENCE']
        expected_predicate = digest({'recordType': 'AssertionRecord', 'id': context['proposedAssertionId'], 'predicate': 'ABSENT'})
        check('RESULT_ABSENCE_GUARD', len(unique) == 1 and unique[0]['key'] == context['proposedAssertionId'] and unique[0]['predicateDigest'] == expected_predicate,
              'Exactly one absence guard protects this proposed AssertionRecord ID.')
        facts = {'snapshotBinding': sb, 'proposedResult': context['proposedAssertion'],
                 'readBindings': [v | {'digestMode': mode(v)} |
                                  {k: reads[key][k] for k in ['snapshotVersion', 'observedVersion'] if k in reads.get(key, {})}
                                  for key, v in read_specs.items()]}
        if 'priorAssertion' in context:
            prior = context['priorAssertion']
            prior_value = verify_bytes(prior['record'], 'PRIOR_RECORD')
            creation = verify_bytes(prior['creationEvidence'], 'PRIOR_CREATION')
            for field, role in [('record', 'PRIOR_ASSERTION'), ('creationEvidence', 'PRIOR_CREATION_EVIDENCE')]:
                check('PRIOR_READ_' + field, any(s['role'] == role and all(equal(prior[field][k], s[k]) for k in ['binding', 'rawSha256']) and (field != 'record' or s['availability'] == 'COMMITTED_AT_TRANSACTION_START') for s in read_specs.values()), 'Prior record must be a committed positive start-snapshot read; exact creation evidence must be a guarded immutable input.')
            check('PRIOR_DISTINCT', prior['record']['binding']['ref'] != proposed_ref and isinstance(prior_value, dict) and prior_value.get('assertionRecordId') == prior['record']['binding']['ref'], 'The prior AssertionRecord identity is exact and differs from the proposed assertion.')
            if validate('creation', creation):
                check('CREATION_ID', creation['creationEvidenceId'] == prior['creationEvidence']['binding']['ref'], 'Creation evidence identity matches its exact selected binding.')
                check('CREATION_RECORD', equal(creation['priorRecord'], prior['record']), 'Creation evidence identifies the exact visible prior bytes.')
                check('CREATION_OWNER', creation['storageOwnerRef'] == context['storageOwnerRef'], 'Creation extraction is from the selected storage owner.')
                if 'creatorAttemptId' in creation:
                    check('PRIOR_ATTEMPT', creation['creatorAttemptId'] != attempt['transactionAttemptId'], 'The original creator attempt, when present, differs from the current attempt.')
                check('GOVERNANCE_CONTEXT', equal(creation['governanceContext'], context['governanceContext']), 'Exact typed tenant/deployment boundary and twin posture match the selected current context.')
                sources = {}
                for spec in creation['sourceRecords']:
                    ref = spec['binding']['ref']
                    if ref in sources:
                        error('DUPLICATE_CREATION_SOURCE', '', 'Duplicate creation source ref: ' + ref)
                    value = verify_bytes(spec, 'CREATION_SOURCE')
                    check('CREATION_SOURCE_READ_' + ref, ref in ref_specs and mode(ref_specs[ref]) == 'JCS_JSON' and
                          all(equal(spec[k], ref_specs[ref][k]) for k in ['binding', 'rawSha256']), 'Original creation/ingress bytes are a structured protected immutable read.')
                    check('CREATION_SOURCE_COMMITTED_' + ref,
                          any(s['binding']['ref'] == ref and s['availability'] == 'COMMITTED_AT_TRANSACTION_START' for s in read_specs.values()),
                          'Original creation/ingress source bytes were committed and visible at transaction start; a later current-attempt receipt cannot supply them.')
                    sources[ref] = value
                values = {'creationKind': creation['creationKind'], 'priorRecordBinding': prior['record']['binding'], 'governanceContext': creation['governanceContext'], 'recordedAnchorScopes': creation['recordedAnchorScopes']}
                if 'creatorAttemptId' in creation:
                    values['creatorAttemptId'] = creation['creatorAttemptId']
                for key, derivation in creation['sourceDerivations'].items():
                    try:
                        actual = pointer(sources[derivation['sourceRef']], derivation['pointer'])
                        ok = equal(actual, values[key])
                    except (KeyError, InputError):
                        ok = False
                    check('CREATION_DERIVATION_' + key, ok, 'Exact source JSON pointer yields the bound ' + key + '.')
                facts.update(priorRecord=prior['record'], priorCreationEvidence=prior['creationEvidence'], priorCreationKind=creation['creationKind'],
                             priorGovernanceContext=creation['governanceContext'], priorRecordedAnchorScopes=creation['recordedAnchorScopes'])
        report['status'] = 'FAIL' if report['errors'] else 'CONDITIONAL_CONFORMANCE_PASS'
        if not report['errors']:
            report['facts'] = facts
        return finish()
    except (InputError, OSError, KeyError, TypeError, ValueError, RecursionError, SchemaError, Unresolvable) as exc:
        error('INPUT_ERROR', '', exc)
        report['status'] = 'INPUT_ERROR'
        return finish()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--package-root', type=Path, required=True)
    p.add_argument('--source-root', type=Path)
    p.add_argument('--selection', type=Path, required=True)
    p.add_argument('--context', type=Path, required=True)
    p.add_argument('--policy', type=Path, required=True)
    p.add_argument('--snapshot', type=Path, required=True)
    p.add_argument('--proof', type=Path, required=True)
    p.add_argument('--records-manifest', type=Path, required=True)
    p.add_argument('--report', type=Path, required=True)
    a = p.parse_args()
    try:
        manifest = strict_json(a.records_manifest.read_bytes())
        # Explicit local file access supplied by the operator. Manifest entries
        # cannot escape their directory or use absolute paths/symlinks outward.
        if not isinstance(manifest, dict):
            raise InputError('Records manifest must be an object.')
        records = {ref: safe_path(a.records_manifest.parent, path).read_bytes() for ref, path in manifest.items()}
        report = verify_state(a.proof.read_bytes(), package_root=a.package_root,
                              selected=strict_json(a.selection.read_bytes()), context_bytes=a.context.read_bytes(),
                              policy_bytes=a.policy.read_bytes(), snapshot_bytes=a.snapshot.read_bytes(), records=records,
                              source_root=a.source_root)
    except (InputError, OSError, ValueError, TypeError) as exc:
        report = {'schemaVersion': 'ofarm.preVerdictProtectedStateReport.v0.1', 'status': 'INPUT_ERROR',
                  'runtimeProtection': 'NOT_ESTABLISHED', 'laterTransactionGate': 'NOT_EVALUATED',
                  'errors': [{'code': 'INPUT_ERROR', 'path': '', 'detail': str(exc)[:4096] or 'Invalid input.'}],
                  'checks': [], 'bindings': {}}
    a.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'status': report['status'], 'checks': len(report['checks']), 'errors': len(report['errors'])}))
    return EXIT[report['status']]


if __name__ == '__main__':
    raise SystemExit(main())
