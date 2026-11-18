"""Bounded domain comparison for one selected raw supporting source.

The caller must derive the pins, locator, and storage read from independently
selected originals and rules. This check cannot establish source admission,
storage chronology, a complete requirement graph, or an owner verdict.
"""
import re

from jsonschema import Draft202012Validator

from strict_inputs import InputError, digest, parse, pointer, sha
import owner_calls


CONTRACT_SHA256 = '8d0bf72d370b08601d5bd8e909609095f54ab15bb20d95d0c28beea70a188ea0'
CONTEXT_SCHEMA_SHA256 = 'e69c67bec85452c4bdce3f28a333cce2d8bf56041b906bcb65c0c4792da9e2d2'
HEX = re.compile(r'[0-9a-f]{64}\Z')
DIGEST = re.compile(r'sha256:[0-9a-f]{64}\Z')
ENTRY_POINTER = re.compile(r'/records/(?:0|[1-9][0-9]*)\Z')
MAX_ORIGINAL_BYTES = 2 * 1024 * 1024


def _result(disposition, code, detail, **data):
    return {'disposition': disposition, 'code': code, 'detail': detail,
            'qualification': 'Bounded selector shape and content only; no owner admission or state verdict.', **data}


def _has_schema_ref(value):
    if isinstance(value, dict):
        return any(key in ('$ref', '$dynamicRef', '$recursiveRef') or _has_schema_ref(item)
                   for key, item in value.items())
    if isinstance(value, list):
        return any(_has_schema_ref(item) for item in value)
    return False


def _selected_entry_validator():
    root = owner_calls.selected_owner_root('occupancy')
    contract_raw = (root / 'contract.json').read_bytes()
    schema_raw = (root / 'schemas/context.schema.json').read_bytes()
    if sha(contract_raw) != CONTRACT_SHA256 or sha(schema_raw) != CONTEXT_SCHEMA_SHA256:
        raise owner_calls.IntegrityError('SELECTED_SOURCE_SCHEMA_PIN_MISMATCH')
    contract, schema = parse(contract_raw), parse(schema_raw)
    if contract.get('schemas', {}).get('context') != CONTEXT_SCHEMA_SHA256 or _has_schema_ref(schema):
        raise owner_calls.IntegrityError('SELECTED_SOURCE_SCHEMA_CLOSURE_MISMATCH')
    entry = schema['properties']['records']['items']
    Draft202012Validator.check_schema(entry)
    return Draft202012Validator(entry)


def _valid_pins(context_pin, source_pin, entry_pointer):
    return (type(context_pin) is dict
            and set(context_pin) == {'rawSha256', 'byteLength', 'wholeJcsDigest'}
            and type(context_pin['rawSha256']) is str and HEX.fullmatch(context_pin['rawSha256'])
            and type(context_pin['byteLength']) is int and 0 <= context_pin['byteLength'] <= MAX_ORIGINAL_BYTES
            and type(context_pin['wholeJcsDigest']) is str and DIGEST.fullmatch(context_pin['wholeJcsDigest'])
            and type(source_pin) is dict
            and set(source_pin) == {'ref', 'digestMode', 'rawSha256', 'byteLength'}
            and type(source_pin['ref']) is str and source_pin['ref']
            and source_pin['digestMode'] == 'RAW_BYTES'
            and type(source_pin['rawSha256']) is str and HEX.fullmatch(source_pin['rawSha256'])
            and type(source_pin['byteLength']) is int and 0 <= source_pin['byteLength'] <= MAX_ORIGINAL_BYTES
            and type(entry_pointer) is str and ENTRY_POINTER.fullmatch(entry_pointer))


def compare(context_bytes, context_pin, entry_pointer, source_bytes, source_pin, storage_spec):
    """Compare exact selected originals and an independently derived #51 read.

    A PASS is only a prerequisite for the named source-selector requirement.
    The full domain evaluator must also check inventory membership, owner facts,
    chronology, graph completeness, and each semantic owner separately.
    """
    if not _valid_pins(context_pin, source_pin, entry_pointer):
        return _result('FAIL', 'INVALID_INDEPENDENT_SELECTION', 'Malformed independently selected source pins or locator.')
    if (context_bytes is not None and type(context_bytes) is not bytes
            or source_bytes is not None and type(source_bytes) is not bytes):
        return _result('FAIL', 'INVALID_ORIGINAL_TRANSPORT', 'Originals must be exact bytes.')
    if (context_bytes is not None and (len(context_bytes) != context_pin['byteLength']
                                       or sha(context_bytes) != context_pin['rawSha256'])
            or source_bytes is not None and (len(source_bytes) != source_pin['byteLength']
                                             or sha(source_bytes) != source_pin['rawSha256'])):
        return _result('FAIL', 'ORIGINAL_PIN_MISMATCH', 'Selected original bytes differ from independent pins.')
    if context_bytes is None:
        return _result('NOT_EVALUATED', 'ORIGINAL_UNAVAILABLE', 'Selected source context is unavailable.')
    try:
        context = parse(context_bytes)
        if digest(context) != context_pin['wholeJcsDigest']:
            return _result('FAIL', 'CONTEXT_VALUE_MISMATCH', 'Selected context whole-value digest differs.')
        entry = pointer(context, entry_pointer)
    except InputError as exc:
        return _result('FAIL', 'INVALID_CONTEXT_OR_LOCATOR', str(exc))
    validator = _selected_entry_validator()
    errors = sorted(validator.iter_errors(entry), key=lambda error: (tuple(map(str, error.absolute_path)), error.message))
    if errors:
        first = errors[0]
        return _result('FAIL', 'SOURCE_ENTRY_SCHEMA',
                       'Selected entry violates the exact owner schema at /' + '/'.join(map(str, first.absolute_path))
                       + ': ' + first.message)
    if type(storage_spec) is not dict or type(storage_spec.get('binding')) is not dict:
        return _result('FAIL', 'INVALID_STORAGE_SELECTION', 'The independent #51 read is missing its binding.')
    binding = storage_spec['binding']
    if (set(binding) not in ({'ref'}, {'ref', 'revisionRef'})
            or type(binding.get('ref')) is not str or not binding['ref']
            or ('revisionRef' in binding and (type(binding['revisionRef']) is not str or not binding['revisionRef']))
            or ('revisionRef' in storage_spec and (type(storage_spec['revisionRef']) is not str
                                                   or not storage_spec['revisionRef']))):
        return _result('FAIL', 'INVALID_STORAGE_BINDING', 'A RAW_BYTES storage binding must keep its exact ref and revision placement.')
    revisions = [value for value in (binding.get('revisionRef'), storage_spec.get('revisionRef')) if value is not None]
    if len(set(revisions)) > 1:
        return _result('FAIL', 'CONTRADICTORY_STORAGE_REVISIONS', 'The storage read selects two different revisions.')
    source_binding = entry['binding']
    source_revision = source_binding.get('revisionRef')
    expected_hash = source_pin['rawSha256']
    if (source_binding['ref'] != source_pin['ref'] or binding['ref'] != source_pin['ref']
            or entry['bytesSha256'] != expected_hash
            or entry['valueDigest'] != 'sha256:' + expected_hash
            or ('digest' in source_binding and source_binding['digest'] != 'sha256:' + expected_hash)
            or entry['digestMode'] != 'RAW_BYTES' or entry['role'] != 'SUPPORTING_SOURCE'
            or storage_spec.get('digestMode') != 'RAW_BYTES' or storage_spec.get('role') != 'EVIDENCE'
            or storage_spec.get('rawSha256') != expected_hash
            or (source_revision is not None and any(value != source_revision for value in revisions))):
        return _result('FAIL', 'SOURCE_STORAGE_CONTRADICTION',
                       'Selected source entry contradicts the raw original or independent storage read.')
    if source_bytes is None:
        return _result('NOT_EVALUATED', 'ORIGINAL_UNAVAILABLE', 'Selected raw source is unavailable.')
    return _result('PASS', 'SOURCE_SELECTOR_MATCH',
                   'Exact owner entry schema and selected raw content relationship match.',
                   entryPointer=entry_pointer, sourceBinding=source_binding.copy(),
                   storageBinding=binding.copy(),
                   storageReadRevisionRef=storage_spec.get('revisionRef'))
