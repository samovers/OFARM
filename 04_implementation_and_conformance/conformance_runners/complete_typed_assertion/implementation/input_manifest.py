"""Whole original input inventory and exact protected source resolution.

Raw bytes and JCS values are distinct. Revision selectors remain revision
selectors. This code never treats a digest as evidence-use admission.
"""
from strict_inputs import parse, sha, digest, same, canonical


def derive(owner_inputs, reference_inventory, state_context=None, source_selections=(), original_inputs=None):
    manifest, resolved, errors = [], [], []
    identities = {
        'act': {'act': 'recordId', 'content': 'contentId', 'context': 'contextId', 'policy': 'policyId', 'intent_profile': 'profileId'},
        'event': {'proof': 'proofId', 'envelope': 'semanticEventId', 'request': 'requestId', 'context': 'contextId', 'profile': 'profileId'},
        'state': {'proof': 'proofId', 'context': 'contextId', 'policy': 'policyId', 'snapshot': 'snapshotId'},
        'authorization': {'evidence': 'evidenceId', 'context': 'contextId', 'profile': 'profileId'},
    }
    originals = {}
    for name, raw in (original_inputs or {}).items():
        value = parse(raw)
        manifest.append({'id': 'domain:' + name, 'role': 'DOMAIN_' + name.upper(),
                         'rawSha256': sha(raw), 'valueDigest': digest(value)})
    if 'evaluationSelection' in owner_inputs:
        raw = owner_inputs['evaluationSelection']; value = parse(raw)
        manifest.append({'id': 'domain:evaluationSelection', 'role': 'DOMAIN_EVALUATION_SELECTION',
                         'rawSha256': sha(raw), 'valueDigest': digest(value), 'valueIdentity': value['selectionId']})
    for owner, fields in identities.items():
        inputs = owner_inputs.get(owner, {})
        state_modes = {}
        if owner == 'state' and 'context_bytes' in inputs:
            selected_context = state_context or parse(inputs['context_bytes'])
            for read in selected_context['requiredReads']:
                ref = read['binding']['ref']
                mode = read.get('digestMode', 'JCS_JSON')
                if ref in state_modes and state_modes[ref] != mode:
                    errors.append({'code': 'CONFLICTING_STATE_DIGEST_MODES', 'pointer': '/state/context/requiredReads', 'ref': ref})
                state_modes[ref] = mode
        for name, id_field in fields.items():
            raw = inputs.get(name + '_bytes')
            if raw is None:
                continue
            value = parse(raw)
            entry = {'id': owner + ':' + name, 'role': owner.upper() + '_' + name.upper(),
                     'rawSha256': sha(raw), 'valueDigest': digest(value)}
            if isinstance(value, dict) and value.get(id_field):
                entry['valueIdentity'] = value[id_field]
            manifest.append(entry)
            originals[entry['id']] = (raw, value)
        if owner == 'act' and 'rendered_bytes' in inputs:
            manifest.append({'id': 'act:rendered', 'role': 'ACT_RENDERED_CONTENT',
                             'rawSha256': sha(inputs['rendered_bytes']), 'format': 'UTF8_TEXT'})
        for name in ['records', 'source_inputs', 'schema_bundle', 'source_bytes', 'schema_bytes']:
            for ref, raw in sorted(inputs.get(name, {}).items()):
                mode = state_modes.get(ref, 'JCS_JSON') if owner == 'state' and name == 'records' else 'JCS_JSON'
                entry = {'id': owner + ':' + name + ':' + ref, 'role': owner.upper() + '_' + name.upper(),
                         'selectedKey': ref, 'rawSha256': sha(raw), 'byteLength': len(raw),
                         'digestMode': mode}
                if mode == 'JCS_JSON':
                    entry['valueDigest'] = digest(parse(raw))
                elif mode != 'RAW_BYTES':
                    errors.append({'code': 'UNKNOWN_STATE_DIGEST_MODE', 'pointer': '/state/context/requiredReads', 'ref': ref})
                manifest.append(entry)
    occupancy_originals = []
    for atom_id, inputs in owner_inputs.get('occupancy', {}).items():
        for name in ['request', 'context']:
            raw = inputs[name + '_bytes']; value = parse(raw)
            manifest.append({'id': 'occupancy:' + atom_id + ':' + name, 'role': 'OCCUPANCY_' + name.upper(),
                             'rawSha256': sha(raw), 'valueDigest': digest(value)})
        context = parse(inputs['context_bytes'])
        for entry in context['records']:
            import json
            key = json.dumps(entry['binding'], sort_keys=True, separators=(',', ':'), ensure_ascii=False)
            raw = inputs['records'].get(key)
            if raw is None:
                errors.append({'code': 'OCCUPANCY_ORIGINAL_BYTES_MISSING', 'pointer': '/occupancy/' + atom_id + '/records', 'binding': entry['binding']})
                continue
            value_digest = digest(parse(raw)) if entry['digestMode'] == 'JCS_JSON' else None
            manifest.append({'id': 'occupancy:' + atom_id + ':' + key, 'role': 'OCCUPANCY_' + entry['role'],
                             'selectedBinding': entry['binding'], 'rawSha256': sha(raw),
                             'byteLength': len(raw),
                             **({'valueDigest': value_digest} if value_digest else {}),
                             'digestMode': entry['digestMode']})
            occupancy_originals.append((entry, raw))
    if state_context is None:
        return {'originalInputs': manifest, 'protectedSources': [], 'errors': errors,
                'resolutionAvailable': False}, []
    records = owner_inputs['state']['records']
    # Full #51 bundles permit 4096 reads. Key by the exact canonical binding
    # bytes so duplicate detection and reference lookup do not rescan every
    # prior read. Equal bindings still collapse only after byte consistency.
    resolved_by_binding = {}
    for read in state_context['requiredReads']:
        binding = read['binding']; raw = records.get(binding['ref'])
        if raw is None or sha(raw) != read['rawSha256']:
            errors.append({'code': 'PROTECTED_SOURCE_RAW_BYTES_MISMATCH', 'pointer': '/requiredReads', 'ref': binding['ref']})
            continue
        mode = read.get('digestMode', 'JCS_JSON')
        if mode == 'RAW_BYTES':
            record = None
            value_digest = None
            if 'digest' in binding:
                errors.append({'code': 'RAW_STORAGE_BINDING_HAS_JSON_DIGEST', 'pointer': '/requiredReads', 'ref': binding['ref']})
                continue
        elif mode == 'JCS_JSON':
            record = parse(raw)
            value_digest = digest(record)
        else:
            errors.append({'code': 'UNKNOWN_STATE_DIGEST_MODE', 'pointer': '/requiredReads', 'ref': binding['ref']})
            continue
        if 'digest' in binding and binding['digest'] != value_digest:
            errors.append({'code': 'PROTECTED_SOURCE_VALUE_DIGEST_MISMATCH', 'pointer': '/requiredReads', 'ref': binding['ref']})
            continue
        binding_key = canonical(binding)
        duplicate = resolved_by_binding.get(binding_key)
        if duplicate:
            if duplicate['rawSha256'] != sha(raw):
                errors.append({'code': 'INCONSISTENT_SELECTOR_BYTES', 'pointer': '/requiredReads'})
            duplicate['selectedReadRoles'].append(read['role'])
            continue
        resolved_entry = {'id': 'resolved:' + digest(binding).removeprefix('sha256:'),
                         'binding': binding, 'record': record, 'rawSha256': sha(raw),
                         **({'valueDigest': value_digest} if value_digest else {}),
                         'digestMode': mode, 'byteLength': len(raw),
                         'selectedReadRoles': [read['role']],
                         'availability': read['availability'], 'claimRoles': []}
        resolved.append(resolved_entry)
        resolved_by_binding[binding_key] = resolved_entry
    # Domain-owned independent selector maps connect a revision to the same
    # original raw/JCS record guarded by the state owner's digest interface.
    # The revision is retained; it is never rewritten to a digest in a claim.
    storage_sources = list(resolved)
    for entry, raw in occupancy_originals:
        matches = [v for v in storage_sources if v['binding']['ref'] == entry['binding']['ref'] and v['rawSha256'] == sha(raw)]
        if len(matches) != 1:
            errors.append({'code': 'OCCUPANCY_SOURCE_NOT_IN_PROTECTED_READ_SET', 'pointer': '/occupancy/records',
                           'binding': entry['binding'], 'digestMode': entry['digestMode']})
    # Authorization source grants use an owner-defined self-digest exclusion.
    # Preserve those original selectors and compare the full protected bytes;
    # never replace their source digest with a whole-value digest.
    if 'authorization' in owner_inputs:
        authorization = owner_inputs['authorization']
        context = parse(authorization['context_bytes'])
        for entry in context['sources']:
            raw = authorization['source_bytes'][entry['key']]
            matches = [v for v in storage_sources if v['binding']['ref'] == entry['binding']['ref']
                       and v['rawSha256'] == sha(raw) and v.get('valueDigest') == digest(parse(raw))]
            if len(matches) != 1:
                errors.append({'code': 'AUTHORIZATION_SOURCE_NOT_IN_PROTECTED_READ_SET',
                               'pointer': '/authorization/source_bytes/' + entry['key'], 'binding': entry['binding']})
    for selection in source_selections:
        candidates = [v for v in storage_sources if v['binding']['ref'] == selection['binding']['ref']
                      and v['rawSha256'] == selection['rawSha256'] and v.get('valueDigest') == selection['valueDigest']]
        if 'digest' in selection['binding'] and selection['binding']['digest'] != selection['valueDigest']:
            candidates = []
        if len(candidates) != 1:
            errors.append({'code': 'INDEPENDENT_SOURCE_SELECTOR_MAPPING_MISMATCH', 'pointer': '/sourceSelections', 'binding': selection['binding']})
            continue
        selection_key = canonical(selection['binding'])
        existing = resolved_by_binding.get(selection_key)
        if existing is None:
            source = candidates[0]
            alias = {**source, 'id': 'resolved:' + digest(selection['binding']).removeprefix('sha256:'),
                     'binding': selection['binding'], 'protectedDigestBinding': source['binding'],
                     'claimRoles': [], 'selectorMapping': selection}
            resolved.append(alias)
            resolved_by_binding[selection_key] = alias
        else:
            existing['selectorMapping'] = selection
    for reference in reference_inventory.get('references', []):
        match = resolved_by_binding.get(canonical(reference['binding']))
        if match is None:
            errors.append({'code': 'REQUIRED_IMMUTABLE_READ_MISSING', 'pointer': reference['pointer'],
                           'role': reference['role'], 'binding': reference['binding']})
        else:
            match['claimRoles'].append({'role': reference['role'], 'pointer': reference['pointer']})
    # Concrete evidence inputs consumed by the act/event checkers must be the
    # same original records protected for this domain use. Context, policy and
    # schema selections are independently pinned checker inputs; they are fully
    # inventoried but are not recast as a self-referential storage proof.
    for key in ['act:act', 'act:content', 'event:proof', 'event:envelope', 'event:request']:
        if key not in originals:
            continue
        raw, value = originals[key]
        entry = next(v for v in manifest if v['id'] == key)
        matches = [v for v in storage_sources if v['binding']['ref'] == entry.get('valueIdentity')
                   and v['rawSha256'] == sha(raw) and v.get('valueDigest') == digest(value)]
        if len(matches) != 1:
            errors.append({'code': 'OWNER_INPUT_NOT_IN_PROTECTED_READ_SET', 'pointer': '/' + key.replace(':', '/'), 'role': entry['role']})
    public = [{k: v for k, v in entry.items() if k != 'record'} for entry in resolved]
    return {'originalInputs': manifest, 'protectedSources': public, 'errors': errors,
            'resolutionAvailable': True}, [entry for entry in resolved if entry['digestMode'] == 'JCS_JSON']
