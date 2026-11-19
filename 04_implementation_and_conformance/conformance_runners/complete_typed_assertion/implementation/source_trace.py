"""Trace schema-checked original domain sources under the comparison contract.

The contract binding identifies this domain comparison, not a foreign admission
or a producer. Every source keeps its actual selector, complete value hash and
raw schema hash. Unknown producer formats remain explicit unresolved entries.
"""
from pathlib import Path
from strict_inputs import parse, digest, sha, same

HERE=Path(__file__).resolve().parent


from domain_reader_occurrences import reader, observed_shape, schema_selection, predicate_value, selector_scope


def collect(schemas, sources, context_digest):
    inspected = inspect(schemas, sources)
    if not sources:
        return inspected
    contract=parse((HERE/'domain-contract.json').read_bytes())
    contract_binding={k:contract[k] for k in ['contractId','contractRef','contractVersion','contractDigest']}
    return {'resolvedInputs': [{**entry, 'ownerContractBinding': contract_binding,
             'contextDigest': context_digest, 'admissionEvidenceBindings': []}
             for entry in inspected['resolvedInputs']],
            'unresolvedInputs': inspected['unresolvedInputs']}


@reader('source_trace.py', [])
def inspect(schemas, sources):
    if not sources:
        return {'resolvedInputs': [], 'unresolvedInputs': []}
    manifest=parse((HERE/'candidate-manifest.json').read_bytes())
    selected_schemas={}
    for member in manifest['members']:
        if not member['path'].endswith('.json'):
            continue
        raw=(HERE/member['path']).read_bytes()
        try:
            value=parse(raw)
        except ValueError:
            continue
        if not isinstance(value,dict) or '$id' not in value or '$schema' not in value:
            continue
        sid=value['$id']
        if sid in schemas.schemas and same(value,schemas.schemas[sid]):
            selected_schemas.setdefault(sid,{}).setdefault(sha(raw), []).append((member['path'], value))
    entries,unresolved=[],[]
    for source in sources:
        record=source['record']
        selector_scope(source['id'])
        version=predicate_value(source, '/schemaVersion', record.get('schemaVersion'), 'SOURCE_SCHEMA_SELECTION') if predicate_value(source, '', isinstance(record,dict), 'SOURCE_SCHEMA_SELECTION') else None
        candidates=[(sid,hashes) for sid,hashes in selected_schemas.items()
                    if version and schemas.schemas[sid].get('properties',{}).get('schemaVersion',{}).get('const')==version]
        schema_selection(source, candidates)
        if len(candidates)!=1 or len(candidates[0][1])!=1:
            unresolved.append({'id':source['id'],'reason':'EXACT_SOURCE_SCHEMA_SELECTION_UNAVAILABLE',
                               'binding':source['binding'],'valueDigest':source['valueDigest']})
            continue
        sid,hashes=candidates[0];raw_sha=next(iter(hashes))
        errors=observed_shape(schemas,sid,record)
        if errors:
            unresolved.append({'id':source['id'],'reason':'SELECTED_SOURCE_SCHEMA_MISMATCH','errors':errors,
                               'binding':source['binding'],'valueDigest':source['valueDigest']})
            continue
        entries.append({'id':source['id'],'role':'DOMAIN_COMPARED_ORIGINAL_SOURCE','selectedBinding':source['binding'],
                        'resolvedDigest':source['valueDigest'],
                        'schemaBinding':{'schemaRef':sid,'schemaVersion':version,'schemaDigest':'sha256:'+raw_sha,
                                         'canonicalization':'JCS_RFC8785_SHA256'}})
    return {'resolvedInputs':entries,'unresolvedInputs':unresolved}
