"""Trace concrete owner-checked input records without claiming admission."""
from pathlib import Path
from strict_inputs import parse, digest, sha, pointer, InputError
from owner_calls import selected_owner_root

HERE = Path(__file__).resolve().parent


def collect(owner_inputs, passing_owners, occupancy_reports=None, unresolved=None):
    entries = []
    unresolved = unresolved if unresolved is not None else []
    fields = {
        'act': {'act': ('act', 'recordId'), 'content': ('content', 'contentId'),
                'context': ('context', 'contextId'), 'policy': ('policy', 'policyId'),
                'intent_profile': ('intent_profile', 'profileId')},
        'event': {'proof': ('proof', 'proofId'), 'envelope': ('envelope', 'semanticEventId'),
                  'request': ('request', 'requestId'), 'context': ('context', 'contextId'), 'profile': ('profile', 'profileId')},
        'state': {'proof': ('proof', 'proofId'), 'context': ('context', 'contextId'),
                  'policy': ('policy', 'policyId'), 'snapshot': ('snapshot', 'snapshotId')},
    }
    for owner, names in fields.items():
        if owner not in passing_owners:
            continue
        data = owner_inputs[owner]
        context = parse(data['context_bytes'])
        root = selected_owner_root(owner)
        contract = parse((root / 'contract.json').read_bytes())
        contract_binding = {'contractId': contract['contractId'], 'contractRef': contract['contractId'],
                            'contractVersion': contract.get('version', '0.1'), 'contractDigest': contract['contractDigest']}
        for name, (schema_name, id_field) in names.items():
            raw = data[name + '_bytes']; value = parse(raw)
            if owner == 'state':
                schema_path = root / 'schemas' / (schema_name + '.schema.json')
            else:
                schema_path = root / contract['schemas'][schema_name]['path']
            schema_raw = schema_path.read_bytes(); schema = parse(schema_raw)
            selected = {'ref': value[id_field], 'digest': digest(value)}
            if owner == 'act':
                selection_fields = {'act': context['actSelection']['binding'],
                                    'content': context['submittedContentBinding'],
                                    'policy': context['sourcePolicyBinding'],
                                    'intent_profile': context['intentProfileBinding']}
                selected = selection_fields.get(name, selected)
            elif owner == 'event':
                selection_fields = {'proof': data['expected_proof_binding'],
                                    'envelope': context['envelopeBinding'],
                                    'request': context['ingressRequestBinding'],
                                    'profile': context['classificationProfileBinding']}
                selected = selection_fields.get(name, selected)
            elif name == 'proof':
                selected = data['selected']['proofBinding']
            elif name == 'snapshot':
                selected = context['attempt']['transactionSnapshot']
            elif name == 'policy':
                selected = context['attempt']['guardPolicyBinding']
            entries.append({'id': owner + ':' + name, 'role': owner.upper() + '_' + name.upper(),
                            'selectedBinding': selected, 'resolvedDigest': digest(value),
                            'schemaBinding': {'schemaRef': schema['$id'], 'schemaVersion': value['schemaVersion'],
                                              'schemaDigest': 'sha256:' + sha(schema_raw), 'canonicalization': 'JCS_RFC8785_SHA256'},
                            'ownerContractBinding': contract_binding, 'contextDigest': digest(context),
                            # Conditional original-byte conformance is not
                            # runtime admission; no admission record is invented.
                            'admissionEvidenceBindings': []})
    def append(owner, id_, role, raw, selected, schema_raw, context, contract, version_pointer='/schemaVersion'):
        value=parse(raw);schema=parse(schema_raw)
        try:
            version=pointer(value,version_pointer) if version_pointer is not None else None
        except InputError:
            version=None
        if not isinstance(version,str):
            unresolved.append({'id':id_,'reason':'ORIGINAL_OWNER_SOURCE_HAS_NO_SELECTED_SCHEMA_VERSION',
                               'schemaVersionPointer':version_pointer,
                               'binding':selected,'rawSha256':sha(raw),'valueDigest':digest(value)})
            return
        entries.append({'id':id_,'role':role,'selectedBinding':selected,'resolvedDigest':digest(value),
                        'schemaBinding':{'schemaRef':schema['$id'],'schemaVersion':version,
                                         'schemaDigest':'sha256:'+sha(schema_raw),'canonicalization':'JCS_RFC8785_SHA256'},
                        'ownerContractBinding':{'contractId':contract['contractId'],'contractRef':contract['contractId'],
                            'contractVersion':contract.get('version','0.1'),'contractDigest':contract['contractDigest']},
                        'contextDigest':digest(context),'admissionEvidenceBindings':[]})
    if 'authorization' in passing_owners:
        data=owner_inputs['authorization'];context=parse(data['context_bytes']);profile=parse(data['profile_bytes'])
        root=selected_owner_root('authorization');contract=parse((root/'contract.json').read_bytes())
        for name,id_field in [('evidence','evidenceId'),('context','contextId'),('profile','profileId')]:
            raw=data[name+'_bytes'];value=parse(raw)
            selected=context['profileBinding'] if name=='profile' else {'ref':value[id_field],'digest':digest(value)}
            append('authorization','authorization:'+name,'AUTHORIZATION_'+name.upper(),raw,selected,
                   (root/'schemas'/(name+'.schema.json')).read_bytes(),context,contract)
        for entry in context['sources']:
            selected_format=profile['formats'][entry['formatId']]
            append('authorization','authorization:source:'+entry['key'],'AUTHORIZATION_'+entry['artifactFamily'],
                   data['source_bytes'][entry['key']],entry['binding'],data['schema_bytes'][selected_format['schemaId']],context,contract,
                   version_pointer=selected_format['schemaVersionPointer'])
    for atom_id, report in (occupancy_reports or {}).items():
        if report['status']!='MATCHED_SELECTED_OCCUPANCY_EVIDENCE':
            continue
        data=owner_inputs['occupancy'][atom_id];context=parse(data['context_bytes'])
        root=selected_owner_root('occupancy');contract=parse((root/'contract.json').read_bytes())
        append('occupancy','occupancy:'+atom_id+':context','OCCUPANCY_OWNER_CONTEXT',data['context_bytes'],
               {'ref':context['ownerContextId'],'digest':digest(context)},(root/'schemas/context.schema.json').read_bytes(),context,contract)
        for entry in context['records']:
            import json
            key=json.dumps(entry['binding'],sort_keys=True,separators=(',',':'),ensure_ascii=False)
            id_='occupancy:'+atom_id+':source:'+digest(entry['binding'])
            if entry['role']=='EPISODE':
                append('occupancy',id_,'OCCUPANCY_EPISODE',data['records'][key],entry['binding'],
                       (root/'schemas/record.schema.json').read_bytes(),context,contract)
            else:
                unresolved.append({'id':id_,'reason':'OPAQUE_OCCUPANCY_SUPPORT_RETAINS_EXISTING_OWNER_SEMANTICS',
                                   'binding':entry['binding'],'rawSha256':entry['bytesSha256'],
                                   'valueDigest':entry['valueDigest'],'digestMode':entry['digestMode']})
    return entries
