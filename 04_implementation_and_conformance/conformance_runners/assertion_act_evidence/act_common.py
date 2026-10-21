"""Finite offline input handling. No network or implicit source resolver."""
import hashlib,json,re
from pathlib import Path
from datetime import datetime
from importlib.metadata import version,PackageNotFoundError

MAX_BYTES=2*1024*1024
MAX_DEPTH=64
JCS_FILES={'__init__.py':'fa44927afd547caf7547247078bcf28863d1e69caf116d258c532b3f20ffd154','_impl.py':'c25bc3a046528482d53bee3487b837f31dd9c05f33e8f13288c7aab320932cec'}
class InputFault(ValueError):pass
def sha(raw):return hashlib.sha256(raw).hexdigest()
def strict(raw):
    if not isinstance(raw,bytes) or not raw:raise InputFault('MISSING_OR_NONBYTE_INPUT')
    if len(raw)>MAX_BYTES:raise InputFault('INPUT_SIZE_LIMIT')
    depth=0;quoted=False;escaped=False
    for byte in raw:
        if quoted:
            if escaped:escaped=False
            elif byte==92:escaped=True
            elif byte==34:quoted=False
        elif byte==34:quoted=True
        elif byte in (91,123):
            depth+=1
            if depth>MAX_DEPTH:raise InputFault('INPUT_DEPTH_LIMIT')
        elif byte in (93,125):depth-=1
    def pairs(items):
        result={}
        for key,value in items:
            if key in result:raise InputFault('DUPLICATE_JSON_NAME')
            result[key]=value
        return result
    def bad(value):raise InputFault('NON_JSON_NUMBER')
    try:return json.loads(raw.decode('utf-8'),object_pairs_hook=pairs,parse_constant=bad)
    except (UnicodeError,json.JSONDecodeError,RecursionError) as exc:raise InputFault('INVALID_UTF8_JSON') from exc
def load_jcs():
    import rfc8785
    if version('rfc8785')!='0.1.4' or any(sha((Path(rfc8785.__file__).parent/n).read_bytes())!=p for n,p in JCS_FILES.items()):raise InputFault('UNSUPPORTED_RFC8785_IMPLEMENTATION')
    if rfc8785.dumps({'z':-0.0,'a':1e-7,'\ue000':2,'\U00010000':3})!=b'{"a":1e-7,"z":0,"\xf0\x90\x80\x80":3,"\xee\x80\x80":2}':raise InputFault('RFC8785_BEHAVIOR_MISMATCH')
    return rfc8785
def pointer(path):return ''.join('/'+str(v).replace('~','~0').replace('/','~1') for v in path)
def date_time(value):
    if not isinstance(value,str):return True
    if not re.fullmatch(r'[0-9]{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12][0-9]|3[01])[Tt](?:[01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9](?:\.[0-9]+)?(?:[Zz]|[+-](?:[01][0-9]|2[0-3]):[0-5][0-9])',value):return False
    datetime.fromisoformat(value.upper().replace('Z','+00:00'));return True
def top_fields(raw):
    """Return exact top-level value bytes after strict JSON parsing elsewhere."""
    text=raw.decode('utf-8');decoder=json.JSONDecoder();i=0;result={}
    def skip(i):
        while i<len(text) and text[i] in ' \r\n\t':i+=1
        return i
    i=skip(i)
    if text[i]!='{':raise InputFault('EXPECTED_RENDERED_OBJECT')
    i=skip(i+1)
    while text[i]!='}':
        key,i=decoder.raw_decode(text,i);i=skip(i)
        if text[i]!=':':raise InputFault('INVALID_OBJECT_SEPARATOR')
        start=skip(i+1);_,i=decoder.raw_decode(text,start);result[key]=text[start:i].encode('utf-8');i=skip(i)
        if text[i]==',':i=skip(i+1)
        elif text[i]!='}':raise InputFault('INVALID_OBJECT_SEPARATOR')
    return result
def report_matches(schema,value):
    """Only the finite frozen owned report vocabulary, including dependency errors."""
    allowed={'$schema','$id','title','oneOf','type','const','enum','pattern','minLength','additionalProperties','properties','required','minItems','uniqueItems','items'}
    if set(schema)-allowed:raise RuntimeError('Unsupported owned report keyword')
    if 'oneOf' in schema:return sum(report_matches(s,value) for s in schema['oneOf'])==1
    if 'const' in schema and value!=schema['const']:return False
    if 'enum' in schema and value not in schema['enum']:return False
    typ=schema.get('type')
    if typ=='null':return value is None
    if typ=='string':return isinstance(value,str) and len(value)>=schema.get('minLength',0) and ('pattern' not in schema or re.search(schema['pattern'],value) is not None)
    if typ=='object':return isinstance(value,dict) and set(schema.get('required',[]))<=set(value) and (schema.get('additionalProperties') is not False or set(value)<=set(schema['properties'])) and all(report_matches(schema['properties'][k],v) for k,v in value.items())
    if typ=='array':return isinstance(value,list) and len(value)>=schema.get('minItems',0) and (not schema.get('uniqueItems') or all(value[i] not in value[:i] for i in range(len(value)))) and all(report_matches(schema['items'],v) for v in value)
    return typ is None
