"""Normative remaining-work counts, separate from factual observations.

The counted population is every unit selected by the exact bound procedure
over the exact work target and extent. A unit with an unsatisfied or unresolved
required finish criterion is unfinished. A total/completed-unit count or an
observation of an easier subset cannot establish these properties.
"""
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR

COUNTS = {
    'O01': ('NO_SELECTED_TREATMENT_SEGMENTS_UNFINISHED', 'candidate:quantitykind:unfinished-selected-treatment-segment-count', 'SELECTED_TREATMENT_SEGMENT'),
    'O02': ('NO_SPECIFIED_FERTILIZATION_PASSES_UNFINISHED', 'candidate:quantitykind:unfinished-specified-fertilization-pass-count', 'SPECIFIED_FERTILIZATION_PASS'),
    'O03': ('NO_REQUIRED_PLANTING_POSITIONS_OR_PASSES_UNFINISHED', 'candidate:quantitykind:unfinished-required-planting-position-or-pass-count', 'PROCEDURE_REQUIRED_PLANTING_POSITION_OR_PASS'),
    'O05': ('NO_REQUIRED_CULTIVATION_PASSES_OR_DEPTH_REQUIREMENTS_UNFINISHED', 'candidate:quantitykind:unfinished-required-cultivation-pass-or-depth-requirement-count', 'PROCEDURE_REQUIRED_CULTIVATION_PASS_OR_DEPTH_REQUIREMENT'),
    'O06': ('NO_SELECTED_CROP_MATERIAL_HANDLING_UNFINISHED', 'candidate:quantitykind:unfinished-selected-crop-material-unit-count', 'PROCEDURE_SELECTED_CROP_MATERIAL_UNIT'),
    'O11': ('NO_SELECTED_SOURCE_MATERIAL_SPLIT_UNFINISHED', 'candidate:quantitykind:unfinished-selected-split-source-material-unit-count', 'PROCEDURE_SELECTED_SPLIT_SOURCE_MATERIAL_UNIT'),
    'O13': ('NO_SELECTED_INPUT_MATERIAL_MIXING_UNFINISHED', 'candidate:quantitykind:unfinished-selected-mixing-input-material-unit-count', 'PROCEDURE_SELECTED_MIXING_INPUT_MATERIAL_UNIT'),
}

MEANINGS = {row: {
    'definitionId': 'candidate:domain:unfinished-work-count:' + row + ':v0.1',
    'activityRow': row, 'stage': 'FINISH', 'predicateKind': predicate, 'quantityKind': quantity_kind,
    'unit': 'ofarm.unit:count', 'countedUnit': unit,
    'population': 'EVERY_UNIT_SELECTED_BY_BOUND_WORK_PROCEDURE_TARGET_AND_EXTENT',
    'unfinishedRule': 'ANY_REQUIRED_PROCEDURE_FINISH_CRITERION_UNSATISFIED_OR_UNRESOLVED',
    'missingObservationRule': 'INCLUDE_UNIT_AS_UNFINISHED_OR_KEEP_RESULT_INDETERMINATE',
    'domain': 'NONNEGATIVE_INTEGERS', 'operator': 'LE', 'threshold': '0', 'thresholdQualifier': 'EXACT',
} for row, (predicate, quantity_kind, unit) in COUNTS.items()}


def refine_interval(interval):
    """Intersect a source interval with the explicitly selected integer domain.

    This is a mathematical projection. Its rounded endpoints are never labelled
    as original measurement values, and the original interval stays available.
    """
    errors = []
    lower, upper = interval['lower'], interval['upper']
    lo = Decimal(lower['decimal']) if 'decimal' in lower else None
    hi = Decimal(upper['decimal']) if 'decimal' in upper else None
    first = int(lo.to_integral_value(rounding=ROUND_CEILING)) if lo is not None else 0
    last = int(hi.to_integral_value(rounding=ROUND_FLOOR)) if hi is not None else None
    if lo is not None and not lower['inclusive'] and first == lo: first += 1
    if hi is not None and not upper['inclusive'] and last == hi: last -= 1
    first = max(first, 0)
    if 'decimal' in lower and 'decimal' in upper:
        if lo == hi and lo != lo.to_integral_value():
            errors.append({'code': 'UNFINISHED_WORK_COUNT_NONINTEGER_RESULT', 'pointer': '/measurement/result'})
        if lo == hi and lo < 0:
            errors.append({'code': 'UNFINISHED_WORK_COUNT_NEGATIVE_RESULT', 'pointer': '/measurement/result'})
    if last is not None and first > last:
        errors.append({'code': 'UNFINISHED_WORK_COUNT_EMPTY_INTEGER_SET', 'pointer': '/measurement/result'})
    refined = None if errors else {'kind': 'INTERVAL',
        'lower': {'decimal': str(first), 'inclusive': True},
        'upper': {'kind': 'UNBOUNDED'} if last is None else {'decimal': str(last), 'inclusive': True},
        'basis': 'EXPLICIT_NONNEGATIVE_INTEGER_PROPERTY_DOMAIN_INTERSECTION'}
    return {'interval': refined, 'errors': errors}


def interval_errors(interval):
    return refine_interval(interval)['errors']


def criterion_outcome(interval, operator, threshold):
    """Classify every integer in a nonempty refined interval, including gaps."""
    lo = int(interval['lower']['decimal'])
    hi = int(interval['upper']['decimal']) if 'decimal' in interval['upper'] else None
    def floor(value): return int(Decimal(value).to_integral_value(rounding=ROUND_FLOOR))
    def ceiling(value): return int(Decimal(value).to_integral_value(rounding=ROUND_CEILING))
    if operator == 'BETWEEN':
        a, z = threshold['lower']['decimal'], threshold['upper']['decimal']
        first = ceiling(a) if threshold['lowerInclusive'] else floor(a) + 1
        last = floor(z) if threshold['upperInclusive'] else ceiling(z) - 1
    else:
        value = threshold['decimal']
        if operator == 'LT': first, last = None, ceiling(value) - 1
        elif operator == 'LE': first, last = None, floor(value)
        elif operator == 'GT': first, last = floor(value) + 1, None
        elif operator == 'GE': first, last = ceiling(value), None
        else: raise ValueError('Unsupported integer-count operator.')
    empty = first is not None and last is not None and first > last
    inside = (first is None or lo >= first) and (last is None or hi is not None and hi <= last)
    disjoint = empty or (hi is not None and first is not None and hi < first) or (last is not None and lo > last)
    outcome = 'NOT_SATISFIED' if disjoint else 'SATISFIED' if inside else 'INDETERMINATE'
    return outcome
