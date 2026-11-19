"""Portable design/example checks. Does not implement or call verify_domain."""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
from pathlib import Path
import sys

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('candidate_dir', nargs='?', type=Path, default=Path(__file__).resolve().parent)
parser.add_argument('--source-examples', type=Path)
parser.add_argument('--packet', type=Path, help='Packet containing reviewed-input/domain/whole-claim-examples.json')
parser.add_argument('--frozen-root', type=Path, help='Optional original frozen-03 directory for all-member custody checks')
parser.add_argument('--repo-root', type=Path, help='Optional canonical repository for real base-v0.2 schema checks')
parser.add_argument('--dependency-dir', type=Path, help='Optional directory containing rfc8785==0.1.4')
parser.add_argument('--output', type=Path, help='Results JSON path; otherwise print complete JSON')
args = parser.parse_args()
if args.dependency_dir: sys.path.insert(0, str(args.dependency_dir.resolve()))
import rfc8785

checks = []
def check(name, condition, **detail):
    checks.append({'check': name, 'passed': bool(condition), **detail})
def sha(raw): return hashlib.sha256(raw).hexdigest()
def digest(value): return 'sha256:' + sha(rfc8785.dumps(value))
def read(name): return json.loads((args.candidate_dir / name).read_text())
def pointer(value, path):
    for k in path.split('/')[1:]:
        k = k.replace('~1', '/').replace('~0', '~')
        value = value[int(k)] if isinstance(value, list) else value[k]
    return value
def rendering(c): return 'Pending claim: ' + rfc8785.dumps(c).decode('utf-8') + '.'

bundle = read('candidate-examples-v2.json')
projection = read('projection-contract-v2.json')
selector_table = read('evidence-selectors.json')
byid = {e['id']: e for e in bundle['examples']}
original_path = args.source_examples or (args.packet / 'reviewed-input/domain/whole-claim-examples.json' if args.packet else None)
if original_path is None: parser.error('supply --source-examples or --packet for historical custody checks')
original_raw = original_path.read_bytes()
originals = json.loads(original_raw)['examples']
check('original examples file bytes unchanged', sha(original_raw) == bundle['source']['examplesFileSha256'])
check('23 originals and two new examples', len(originals) == 23 and len(bundle['examples']) == 25)
check('original IDs preserved in order', [x['id'] for x in originals] == [x['id'] for x in bundle['examples'][:23]])
check('real RFC8785 implementation', hasattr(rfc8785, 'dumps'))

# Independent expected repair set from the typed source audit, not generated selectors.
si = ['SI-product-authorisation:fictional', 'parcel-snapshot:fictional', 'use-context:fictional', 'training:fictional', 'inspection:fictional']
expected_additions = {
    'W01': ['configuration:sprayer-C'],
    'W02': si + ['source:fictional:treatedArea', 'plan:fictional'],
    'W07': ['history-claim:fictional', 'soil-source:fictional', 'rustgewas-history:fictional', 'Skal-or-RVO-route:fictional', 'profile-evaluation:fictional'],
    'W08': si + ['source:fictional:dose', 'source:fictional:treatedArea'],
    'W10': ['delivery:receipt', 'source:fictional:handledQuantity'],
    'W11': ['classification-evidence:inspection', 'source:fictional:handledQuantity'],
    'W12': ['disposal-record:fictional', 'source:fictional:handledQuantity'],
    'W13': ['source:fictional:handledQuantity'],
    'W14': ['source:fictional:rate', 'source:fictional:applicationVolume'],
    'W15': ['source:fictional:waterVolume', 'source:fictional:rate'],
    'W17': ['analysis-result:fictional'], 'W19': ['report:fictional']}

def missing_citations(e, content):
    return [x['pointer'] for x in e['evidenceClosure']['selectedCitations']
            if pointer(content, x['pointer']) not in content['evidenceBindings']]

def typed_atoms(node, path='/proposition'):
    if node['form'] == 'ATOM':
        yield path, node
    elif node['form'] in ['ALL', 'ANY', 'SEQUENCE']:
        for i, child in enumerate(node['children']): yield from typed_atoms(child, path + '/children/' + str(i))
    elif node['form'] in ['NOT', 'QUALIFIED']:
        yield from typed_atoms(node['child'], path + '/child')
    else: raise ValueError('Unknown typed proposition')

def expand_selector(value, selector, prefix):
    pieces = selector.split('/')[1:]
    pending = [(value, prefix)]
    for token in pieces:
        next_pending = []
        for current, path in pending:
            if token == '*':
                if not isinstance(current, list): raise ValueError('Selector requires array')
                next_pending.extend((x, path + '/' + str(i)) for i, x in enumerate(current))
            elif isinstance(current, dict) and token in current:
                next_pending.append((current[token], path + '/' + token))
        pending = next_pending
    return [(path, current) for current, path in pending]

def selected_by_table(content, table):
    found = []
    for base, atom in typed_atoms(content['proposition']):
        row = atom['definition'].split('#')[-1]
        body = atom['body']
        for spec in table['rowSelectors']:
            if spec['definition'] != row: continue
            guard = spec.get('guard')
            if isinstance(guard, dict) and pointer(body, guard['pointer']) != guard['equals']: continue
            for selector in spec['selectors']:
                for path, value in expand_selector(body, selector, base + '/body'):
                    if row == 'O24' and value.get('state') == 'UNREPORTED': continue
                    found.append((path, digest(value)))
        for spec in table['sharedSelectors']:
            if spec['type'] != 'OPERATION_QUANTITY_PARAMETER': continue
            if row not in ['O' + str(i).zfill(2) for i in range(1, 28)]: continue
            for path, value in expand_selector(body, spec['selector'], base + '/body'):
                # This typed source selector is conditional on its containing quantity value.
                parent = pointer(content, path.rsplit('/original/sourceBinding', 1)[0])
                if parent['state'] == 'STATED' and parent['original']['presence'] == 'PRESENT':
                    found.append((path, digest(value)))
    for spec in table['sharedSelectors']:
        if spec['type'] not in ['MEASUREMENT_TEMPORAL_BASIS', 'SAMPLE_COLLECTION_TEMPORAL_BASIS']: continue
        if content.get('temporalBasis', {}).get('kind') != 'MEASUREMENT_EVIDENCE': continue
        for selector in spec['selectors']:
            found.extend((path, digest(value)) for path, value in expand_selector(content, selector, ''))
    return sorted(found)

for e in bundle['examples']:
    recorded = sorted((x['pointer'], digest(x['binding'])) for x in e['evidenceClosure']['selectedCitations'])
    check(e['id'] + ': authored selector table equals recorded citations', selected_by_table(e['claimContent'], selector_table) == recorded)
mutated_table = copy.deepcopy(selector_table)
next(x for x in mutated_table['rowSelectors'] if x['definition'] == 'S12')['selectors'].remove('/configuration')
w01 = byid['W01_EQUIPMENT']
check('dropping configuration selector detected despite unchanged citation metadata',
      selected_by_table(w01['claimContent'], mutated_table) != sorted((x['pointer'], digest(x['binding'])) for x in w01['evidenceClosure']['selectedCitations']))

for old in originals:
    e = byid[old['id']]; c = e['claimContent']; source = old['literalTypedClaim']
    before = copy.deepcopy(source); before.pop('assertionAct'); before['candidateGrammar'] = bundle['bundleVersion']
    after = copy.deepcopy(c); after['evidenceBindings'] = source['evidenceBindings']
    check(e['id'] + ': all original domain fields preserved', before == after)
    check(e['id'] + ': full historical example digest', digest(old) == e['derivedFrom']['sourceExampleJcsSha256'])
    check(e['id'] + ': original evidence array remains exact prefix', c['evidenceBindings'][:len(source['evidenceBindings'])] == source['evidenceBindings'])
    got = [x['fixtureLogicalRef'] for x in e['evidenceClosure']['addedBindings']]
    check(e['id'] + ': independently expected evidence additions', got == expected_additions.get(e['id'][:3], []))
    for citation in e['evidenceClosure']['selectedCitations']:
        p = citation['pointer']; b = pointer(c, p)
        check(e['id'] + ': exact typed citation at ' + p, b == citation['binding'] and b in c['evidenceBindings'])
        # Same ref but wrong immutable revision must not meet exact membership.
        hostile = copy.deepcopy(c)
        for member in hostile['evidenceBindings']:
            if member == b: member['fixtureRevision'] = 'different-revision'
        check(e['id'] + ': wrong revision rejected at ' + p, p in missing_citations(e, hostile))
    for citation in e['evidenceClosure']['repairedCitationOccurrences']:
        p = citation['pointer']; b = pointer(c, p)
        hostile = copy.deepcopy(c)
        hostile['evidenceBindings'] = [x for x in hostile['evidenceBindings'] if x != b]
        check(e['id'] + ': omission rejected at ' + p, p in missing_citations(e, hostile))

for e in bundle['examples']:
    c = e['claimContent']; text = e['exactRenderedText']
    check(e['id'] + ': exact JCS rendering', text == rendering(c))
    check(e['id'] + ': exact render and content digests', e['renderedTextSha256'] == 'sha256:' + sha(text.encode()) and e['claimContentDigest'] == digest(c))
    check(e['id'] + ': explicit root projection and no act metadata',
          set(projection['requiredRootMembers']).issubset(c) and
          set(c).issubset(set(projection['requiredRootMembers'] + projection['conditionalRootMembers'])) and
          all(k not in c for k in ['assertionAct', 'assertedAt', 'assertedByPartyRef', 'assertionActEvidenceBinding', 'assertionActPosture']))
    changed = copy.deepcopy(e)
    changed['governedContextExample']['assertedAt'] = '2026-10-21T09:00:00Z'
    changed['governedContextExample']['authoritySubjectPartyRef'] = 'party:different-authority-owner'
    check(e['id'] + ': changed governed context cannot change text', rendering(changed['claimContent']) == text)
    if e['id'][:3] in ['W04', 'W22']:
        check(e['id'] + ': event inputs preserve distinct roles',
              c['association']['envelope'] not in c['evidenceBindings'] and
              c['association']['ingressEvidence'] not in c['evidenceBindings'])

check('40 occurrence repairs / 33 bindings / 12 originals',
      sum(len(e['evidenceClosure']['repairedCitationOccurrences']) for e in bundle['examples'][:23]) == 40 and
      sum(len(e['evidenceClosure']['addedBindings']) for e in bundle['examples'][:23]) == 33 and
      sum(bool(e['evidenceClosure']['addedBindings']) for e in bundle['examples'][:23]) == 12)

def offline_errors(x):
    evidence, intent, result = x['evidenceRecord'], x['intent'], x['result']
    errors = []
    if digest(evidence) != intent['assertionActEvidenceBinding']['digest']: errors.append('ACT_EVIDENCE_DIGEST_MISMATCH')
    if evidence['submittedContent']['assertionBody'] != intent['assertionBody']: errors.append('ATTESTED_BODY_MISMATCH')
    if evidence['scope'] != intent['resources'][0]['scope']: errors.append('ATTESTED_SCOPE_MISMATCH')
    for k, value in evidence['submittedContent'].items():
        if k != 'assertionBody' and value != intent[k]: errors.append('ATTESTED_CONTENT_MISMATCH:' + k)
    if evidence['assertedAt'] != intent['assertedAt'] or intent['assertedAt'] != result['assertedAt']: errors.append('ACT_TIME_MISMATCH')
    if evidence['assertingPartyBasis']['partyRef'] != result['assertedByPartyRef']: errors.append('ACT_PARTY_MISMATCH')
    if intent['assertionBody'] != result['assertionBody']: errors.append('INTENT_RESULT_BODY_MISMATCH')
    if intent['assertionActEvidenceBinding'] != result['assertionActEvidenceBinding']: errors.append('INTENT_RESULT_ACT_BINDING_MISMATCH')
    if digest(intent) != x['effectIntentDigest'] or digest(result) != x['proposedResultDigest']: errors.append('WHOLE_VALUE_DIGEST_MISMATCH')
    return errors

offline = byid['W25_OFFLINE_DIGEST_BOUND_PRUNING']['offlineBindingIllustration']
check('offline digest-bound content positive', offline_errors(offline) == [])
check('offline same domain claim and text as W03', byid['W25_OFFLINE_DIGEST_BOUND_PRUNING']['claimContent'] == byid['W03_MEASURED_PRUNING_NO_EVENT']['claimContent'])
check('offline evidence has no later intent digest', 'effectIntentDigest' not in offline['evidenceRecord'])
check('offline exact rendered body is attested', offline['evidenceRecord']['submittedContent']['assertionBody']['claimText'] == byid['W25_OFFLINE_DIGEST_BOUND_PRUNING']['exactRenderedText'])
for h in bundle['hostileExamples']:
    errors = offline_errors(h['inputs'])
    check(h['id'] + ': isolated hostile outcome', errors == [h['expected']], observedErrors=errors)
for field, code in [('assertedAt', 'ACT_TIME_MISMATCH'), ('assertedByPartyRef', 'ACT_PARTY_MISMATCH')]:
    h = copy.deepcopy(offline); h['result'][field] = '2026-10-21T09:00:00Z' if field == 'assertedAt' else 'party:wrong'
    h['proposedResultDigest'] = digest(h['result'])
    check('excluded metadata still verified: ' + field, code in offline_errors(h))

# Fixture-resolved alias check: same actual record digest under another logical name
# does not convert assertion-act self-attestation into ordinary domain evidence.
act_digest = digest(offline['evidenceRecord'])
def self_act_aliases(ordinary_bindings, resolved_digest_by_binding):
    return [b for b in ordinary_bindings if resolved_digest_by_binding.get(digest(b)) == act_digest]
alias = {'ref': 'ordinary-support:renamed-offline-act', 'revisionRef': 'fixture-revision:alias:r1'}
resolved = {digest(alias): act_digest}
check('self-attestation alias into ordinary evidence rejected', bool(self_act_aliases([alias], resolved)))
check('ordinary distinct evidence not rejected as self-attestation', not self_act_aliases([alias], {digest(alias): 'sha256:' + '1' * 64}))
check('self-attestation alias prevention is explicit contract rule', 'alias' in projection['exclusionSemantics'] or 'laundered' in projection['exclusionSemantics'])

structure = byid['W24_EXISTING_FARM_IDENTIFIER']
check('existing-kind structure example', structure['claimContent']['selectedAction'] == 'ASSERT_STRUCTURE' and structure['claimContent']['subject']['kind'] == 'FARM')
check('same identity/revision subject and sole anchor', structure['claimContent']['subject'] == structure['claimContent']['soleAuthorityAnchor'])
online = structure['baseV02CarrierIllustration']
changed = copy.deepcopy(online); changed['intent']['assertedAt'] = '2026-10-21T09:00:00Z'; changed['result']['assertedAt'] = changed['intent']['assertedAt']
check('runtime time injection changes whole intent digest but not body', digest(changed['intent']) != digest(online['intent']) and changed['intent']['assertionBody'] == online['intent']['assertionBody'])
check('no caller-selected reporter in base intent', 'assertedByPartyRef' not in online['intent'] and 'assertedByPartyRef' not in offline['intent'])

optional = {}
if args.frozen_root:
    manifest_raw = (args.frozen_root / 'manifest.json').read_bytes()
    check('frozen manifest exact bytes', sha(manifest_raw) == bundle['source']['manifestSha256'])
    members = json.loads(manifest_raw)['members']
    for m in members: check('frozen member unchanged: ' + m['path'], sha((args.frozen_root / m['path']).read_bytes()) == m['sha256'])
    optional['frozenMembersVerified'] = len(members)
if args.repo_root:
    import jsonschema
    from referencing import Registry, Resource
    base = args.repo_root / '03_machine_contracts/drafts_non_default'
    records = [
        base / 'assertion_record_submission/OFARM_AssertionRecord_schema_v0_2.json',
        base / 'authorization_policy_bundle/effect_intents/OFARM_OperationAssertionEffectIntent_schema_v0_2.json',
        base / 'authorization_policy_bundle/effect_intents/OFARM_StructureAssertionEffectIntent_schema_v0_2.json']
    schemas = [json.loads(p.read_text()) for p in records]
    registry = Registry().with_resources([(s['$id'], Resource.from_contents(s)) for s in schemas])
    for label, item, schema in [('offline intent', offline['intent'], schemas[1]), ('offline result', offline['result'], schemas[0]), ('existing-kind structure intent', online['intent'], schemas[2]), ('existing-kind structure result', online['result'], schemas[0])]:
        errors = list(jsonschema.Draft202012Validator(schema, registry=registry, format_checker=jsonschema.FormatChecker()).iter_errors(item))
        check('real base-v0.2 schema: ' + label, not errors, errors=[e.message for e in errors])
    optional['baseSchemaFiles'] = [{'path': str(p.relative_to(args.repo_root)), 'sha256': sha(p.read_bytes())} for p in records]

result = {'status': 'DESIGN_EXAMPLE_CHECKS_PASS' if all(c['passed'] for c in checks) else 'DESIGN_EXAMPLE_CHECKS_FAIL',
          'checks': len(checks), 'passed': sum(c['passed'] for c in checks), 'failed': sum(not c['passed'] for c in checks),
          'results': checks, 'optionalChecks': optional,
          'limits': ['No complete domain verifier was implemented or executed.',
                     'Offline positive means content/digest consistency of fictional inputs only; no owner evidence admission or real signature was verified.',
                     'The alias check uses explicit fictional resolved-byte identity; production must obtain that identity and dependency closure from the existing evidence owner.',
                     'Base-v0.2 carrier schema checks do not validate the proposed new typed-proposition language or establish any predicate/admission result.',
                     'No claim of a new 946-check inventory review, base-PR approval, CI success, runtime conformance or merge.'],
          'next': 'Integrate the versioned design/examples, then obtain fresh review of the amended PR head.'}
if args.output:
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ['status', 'checks', 'passed', 'failed']}))
    for c in checks:
        if not c['passed']: print(json.dumps(c))
else: print(json.dumps(result, indent=2))
raise SystemExit(0 if result['failed'] == 0 else 1)
