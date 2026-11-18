"""Bounded original-byte JSON parsing and canonical value hashes."""
import hashlib
import json
from pathlib import Path
import re

MAX_BYTES = 2 * 1024 * 1024
MAX_DEPTH = 64


class InputError(ValueError):
    pass


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def parse(raw):
    if not isinstance(raw, bytes) or len(raw) > MAX_BYTES:
        raise InputError('Expected original bytes, at most 2 MiB per JSON input.')
    def pairs(items):
        result = {}
        for k, v in items:
            if k in result:
                raise InputError('Duplicate JSON object name: ' + k)
            result[k] = v
        return result
    def constant(value):
        raise InputError('Non-JSON numeric constant: ' + value)
    # Check nesting before recursive JSON decoding, respecting quoted escapes.
    depth = 0
    quoted = escaped = False
    for byte in raw:
        if quoted:
            if escaped:
                escaped = False
            elif byte == 92:
                escaped = True
            elif byte == 34:
                quoted = False
        elif byte == 34:
            quoted = True
        elif byte in (91, 123):
            depth += 1
            if depth > MAX_DEPTH:
                raise InputError('JSON nesting exceeds 64 levels.')
        elif byte in (93, 125):
            depth -= 1
    try:
        value = json.loads(raw.decode('utf-8'), object_pairs_hook=pairs,
                           parse_constant=constant)
        canonical(value)  # Reject unsafe integers, surrogates and overflow.
        return value
    except (ValueError, UnicodeError, RecursionError) as exc:
        raise InputError(str(exc)) from exc


def canonical(value):
    import rfc8785
    try:
        return rfc8785.dumps(value)
    except (ValueError, TypeError, UnicodeError) as exc:
        raise InputError(str(exc)) from exc


def digest(value):
    return 'sha256:' + sha(canonical(value))


def same(a, b):
    return canonical(a) == canonical(b)


def pointer(value, path):
    if not isinstance(path, str) or (path and not path.startswith('/')):
        raise InputError('Invalid JSON pointer.')
    for part in path.split('/')[1:]:
        if re.search(r'~(?![01])', part):
            raise InputError('Invalid pointer escape.')
        key = part.replace('~1', '/').replace('~0', '~')
        if isinstance(value, dict) and key in value:
            value = value[key]
        elif isinstance(value, list) and re.fullmatch(r'0|[1-9][0-9]*', key) and int(key) < len(value):
            value = value[int(key)]
        else:
            raise InputError('Missing pointer target: ' + path)
    return value


def safe_path(root, relative):
    root = Path(root).resolve()
    path = root / relative
    if not isinstance(relative, str) or Path(relative).is_absolute() or '..' in Path(relative).parts:
        raise InputError('Package path must be relative and contained.')
    if not path.resolve().is_relative_to(root) or not path.is_file():
        raise InputError('Package member missing or outside its root: ' + relative)
    return path


def verify_pins(root, manifest_bytes, expected_raw_sha):
    if sha(manifest_bytes) != expected_raw_sha:
        raise InputError('Package manifest does not match independent raw-byte pin.')
    manifest = parse(manifest_bytes)
    if not isinstance(manifest, dict) or not isinstance(manifest.get('members'), list):
        raise InputError('Package member manifest is malformed.')
    seen = set()
    for member in manifest['members']:
        name = member['path']
        if name in seen:
            raise InputError('Duplicate package member: ' + name)
        seen.add(name)
        if sha(safe_path(root, name).read_bytes()) != member['rawSha256']:
            raise InputError('Package byte pin mismatch: ' + name)
    return manifest


def distinct_selected_originals(entries):
    """Collapse selected aliases only when logical identity and both hashes match.

    The caller supplies already resolved/protected entries. Different records,
    logical identities or original bytes remain separate candidates. No claim
    selector is rewritten, and every alias remains in the input inventory.
    """
    originals = {}
    for entry in entries:
        key = (entry['binding']['ref'], entry['rawSha256'], entry['valueDigest'])
        originals.setdefault(key, entry)
    return list(originals.values())
