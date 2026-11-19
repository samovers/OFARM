"""Exact domain coverage over an original extent clock and selected meaning.

Bindings, source schemas and meaning selection are checked by each consumer.
This calculation never returns a rewritten original or establishes eligible use.
"""
from time_validation import foreign_instant, foreign_seconds


def evaluate(original, claim, meaning=None):
    errors, roles = [], []
    form = original['timeType']; point_form = form in ['INSTANT', 'AS_OF']
    result = {'coverage': None, 'pointForm': point_form, 'errors': errors, 'remainingRoles': roles}
    fields = {'instant', 'intervalStart', 'intervalEnd'} & original.keys()
    conflict = (point_form and bool(fields - {'instant'})) or (not point_form and 'instant' in fields) or (form == 'OPEN_INTERVAL' and 'intervalEnd' in fields)
    if conflict:
        errors.append({'code': 'TIME_FORM_INVALID', 'pointer': '/temporalApplicability'}); return result
    required = {'instant'} if point_form else {'intervalStart'}
    if not required <= fields:
        roles.append('ORIGINAL_TIME_BOUND'); return result
    try:
        parsed = {k: foreign_instant(original[k]) for k in fields}
        lo = foreign_seconds(claim.get('at', claim.get('start')))
        hi = foreign_seconds(claim['end']) if 'end' in claim else lo if 'at' in claim else None
    except (ValueError, TypeError):
        errors.append({'code': 'TIME_INVALID', 'pointer': '/temporalApplicability'}); return result
    if any(v['unknownLocalOffset'] for v in parsed.values()):
        roles.append('KNOWN_INSTANT_INTERPRETATION'); return result
    if point_form:
        result['coverage'] = 'at' in claim and parsed['instant']['seconds'] == lo
        return result
    start = parsed['intervalStart']['seconds']
    end = parsed['intervalEnd']['seconds'] if 'intervalEnd' in parsed else None
    covered = not (start > lo or end is not None and (end <= start or hi is None or hi > end))
    if end is not None and meaning is not None and meaning['endBoundary'] == 'UNBOUNDED':
        errors.append({'code': 'MEANING_END_BOUND_MISMATCH', 'pointer': '/extentTemporalMeaning/endBoundary'})
    if covered and end is None and (meaning is None or meaning['endBoundary'] != 'UNBOUNDED'):
        roles.append('END_BOUND_INTERPRETATION')
    if covered and (start == lo or end is not None and hi == end):
        if meaning is None:
            roles.append('BOUNDARY_INTERPRETATION')
        elif start == lo and meaning['startBoundary'] == 'EXCLUSIVE' or end is not None and hi == end and meaning['endBoundary'] == 'EXCLUSIVE':
            covered = False
    if not roles:
        result['coverage'] = covered
    return result
