"""Original JSON values or verifiable absence at an original ancestor.

An absent path has no value digest. Its closest existing ancestor, exact
requested path and failure kind allow a reviewer to reproduce the absence.
"""
import hashlib
import re
import rfc8785


def value_digest(value):
    return 'sha256:' + hashlib.sha256(rfc8785.dumps(value)).hexdigest()


def select_operand(original, path, role):
    if not isinstance(path, str) or path and not path.startswith('/'):
        raise ValueError('Invalid original operand pointer')
    if re.search(r'~(?![01])', path): raise ValueError('Invalid original operand escape')
    value = original; ancestor = ''
    for encoded in path.split('/')[1:]:
        if re.search(r'~(?![01])', encoded): raise ValueError('Invalid original operand escape')
        key = encoded.replace('~1', '/').replace('~0', '~')
        reason = None
        if isinstance(value, dict):
            if key not in value: reason = 'OBJECT_MEMBER_ABSENT'
        elif isinstance(value, list):
            if not re.fullmatch(r'0|[1-9][0-9]*', key): raise ValueError('Invalid original operand array index')
            key = int(key)
            if key >= len(value): reason = 'ARRAY_INDEX_ABSENT'
        else:
            reason = 'NON_CONTAINER_ANCESTOR'
        if reason:
            return {'inputRole': role, 'pointer': path, 'valuePosture': 'ABSENT',
                    'ancestorPointer': ancestor, 'ancestorValueDigest': value_digest(value),
                    'absenceReason': reason}
        value = value[key]; ancestor += '/' + encoded
    return {'inputRole': role, 'pointer': path, 'valueDigest': value_digest(value)}
