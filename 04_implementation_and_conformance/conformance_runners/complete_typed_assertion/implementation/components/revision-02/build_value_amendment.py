"""Amend active original-quantity representation without editing the seal."""
import copy
import hashlib
import json
from common import HERE, put


def main():
    base_path = HERE.parent / 'owned-value-types.schema.json'
    raw = base_path.read_bytes()
    seal_raw = (HERE.parent / 'checkpoint-manifest.json').read_bytes()
    seal = json.loads(seal_raw)
    member = next(v for v in seal['members'] if v['path'] == base_path.name)
    if hashlib.sha256(raw).hexdigest() != member['sha256']:
        raise ValueError('Sealed base value schema changed.')
    base = json.loads(raw); amended = copy.deepcopy(base)
    original = amended['$defs']['originalQuantity']
    original['properties']['lexicalValue'] = {'type': ['string', 'null']}
    original['properties']['unitText'] = {'type': ['string', 'null']}
    original['properties']['reportedValue'] = {
        'type': 'number',
        '$comment': 'Original JSON number from the selected carrier reportedValue field. Never a parsed or stringified lexical value, normalized quantity or synthesized value.'}
    original['allOf'] = [{
        'if': {'properties': {'presence': {'const': 'UNREPORTED'}}},
        'then': {'properties': {'lexicalValue': {'type': 'null'}, 'unitText': {'type': 'null'}},
                 'not': {'required': ['reportedValue']}},
        'else': {'anyOf': [
            {'properties': {'lexicalValue': {'type': 'string'}}},
            {'properties': {'unitText': {'type': 'string'}}},
            {'required': ['reportedValue']}]},
    }, {
        'if': {'required': ['reportedValue']},
        'then': {'properties': {'presence': {'const': 'PRESENT'}, 'lexicalValue': {'type': 'null'}}},
    }]
    original['$comment'] = ('Active domain-owned amendment: retain original strings in lexicalValue and original JSON numbers '
        'in reportedValue. Empty original strings remain strings. Absence is distinct from a number, including zero. '
        'The carrier comparison must establish exact presence, type, value, source selector and pointer.')
    amended['$comment'] = (base.get('$comment', '') + ' Active unsealed originalQuantity amendment; the sealed base remains unchanged. '
        'Exact active schema bytes are selected by the candidate and act profile. See owned-value-types-amendment.json.').strip()
    for key, value in base['$defs'].items():
        if key != 'originalQuantity' and amended['$defs'][key] != value:
            raise ValueError('Unrelated value type changed.')
    put('owned-value-types-amendment.schema.json', amended)
    put('owned-value-types-amendment.json', {
        'status': 'UNSEALED_DOMAIN_OWNED_SCHEMA_AMENDMENT',
        'primaryTrustBoundary': 'AssertionRecord domain meaning and validation integrity',
        'scopeStayedInsideBoundary': True,
        'base': {'path': '../owned-value-types.schema.json', 'rawSha256': hashlib.sha256(raw).hexdigest(),
                 'checkpointManifestRawSha256': hashlib.sha256(seal_raw).hexdigest()},
        'active': {'path': 'owned-value-types-amendment.schema.json', 'schemaId': amended['$id'],
                   'rawSha256': hashlib.sha256((HERE / 'owned-value-types-amendment.schema.json').read_bytes()).hexdigest()},
        'changedDefinition': 'originalQuantity',
        'meaning': 'Exact original JSON scalar representation; no source acceptance, quantity conversion, inferred lexical text or manufactured value.',
        'compatibility': 'Existing nonempty text and absent-value branches remain unchanged. Numeric originals now require a numeric reportedValue and PRESENT posture. Empty original strings can be preserved explicitly.',
        'next': 'Verify original-byte operation carriers and active schema closure without changing the sealed checkpoint.',
    })
    print(json.dumps({'activeSchema': 'owned-value-types-amendment.schema.json', 'sealedBaseUnchanged': base_path.read_bytes() == raw}))


if __name__ == '__main__': main()
