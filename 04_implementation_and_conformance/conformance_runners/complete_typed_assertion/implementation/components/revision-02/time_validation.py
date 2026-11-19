"""Strict source RFC3339 validation without datetime.fromisoformat coercion.

Foreign timestamps retain arbitrary fractional precision and permitted offsets.
Canonical domain claim strings are separately constrained to Z and 0..9 digits
with no trailing zero. Neither parser accepts leap seconds under this profile.
"""
from datetime import date
from decimal import Decimal,localcontext
import re
RFC3339=re.compile(r'([0-9]{4})-([0-9]{2})-([0-9]{2})[Tt]([0-9]{2}):([0-9]{2}):([0-9]{2})(?:\.([0-9]+))?([Zz]|[+-][0-9]{2}:[0-9]{2})',re.ASCII)

def foreign_instant(value):
    if not isinstance(value,str):raise ValueError('RFC3339 string required')
    m=RFC3339.fullmatch(value)
    if m is None:raise ValueError('ASCII RFC3339 syntax required')
    y,mo,d,h,mi,se=map(int,m.groups()[:6]);fraction=m.group(7) or '';zone=m.group(8)
    if not 0<=h<=23 or not 0<=mi<=59 or not 0<=se<=59:raise ValueError('Time component out of range')
    day=date(y,mo,d) # Gregorian day/month/leap-year validation, no normalization.
    offset=0
    if zone.upper()!='Z':
        oh,om=int(zone[1:3]),int(zone[4:6])
        if not 0<=oh<=23 or not 0<=om<=59:raise ValueError('Offset component out of range')
        # RFC3339 -00:00 conveys an unknown local offset. Preserve that semantic
        # qualification; do not use it as a known UTC instant comparison.
        if zone=='-00:00':return {'seconds':None,'unknownLocalOffset':True,'raw':value}
        offset=(oh*60+om)*60*(1 if zone[0]=='+' else -1)
    with localcontext() as ctx:
        ctx.prec=max(40,len(fraction)+20)
        seconds=Decimal(day.toordinal()*86400+h*3600+mi*60+se-offset)+(Decimal('0.'+fraction) if fraction else Decimal(0))
    return {'seconds':seconds,'unknownLocalOffset':False,'raw':value}

def foreign_seconds(value):
    result=foreign_instant(value)
    if result['unknownLocalOffset']:raise ValueError('Unknown local offset needs selected interpretation')
    return result['seconds']
