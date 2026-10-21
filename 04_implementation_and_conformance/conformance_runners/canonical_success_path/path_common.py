"""Strict offline bytes, canonical values and non-evaluating source selection."""
import hashlib,json,math,re
from pathlib import Path
from importlib.metadata import version
from datetime import datetime
MAX_BYTES=4*1024*1024
class Fault(ValueError):
 def __init__(self,code,pointer='',detail=''):super().__init__(code);self.code,self.pointer,self.detail=code,pointer,detail

def sha(raw):return hashlib.sha256(raw).hexdigest()
def strict(raw):
 if type(raw)is not bytes or not raw or len(raw)>MAX_BYTES:raise Fault('INVALID_INPUT_BYTES')
 depth=0;quoted=False;escaped=False
 for c in raw:
  if quoted:
   if escaped:escaped=False
   elif c==92:escaped=True
   elif c==34:quoted=False
  elif c==34:quoted=True
  elif c in [91,123]:
   depth+=1
   if depth>64:raise Fault('JSON_DEPTH_LIMIT')
  elif c in [93,125]:depth-=1
 def pairs(xs):
  d={}
  for k,v in xs:
   if k in d:raise Fault('DUPLICATE_JSON_MEMBER')
   d[k]=v
  return d
 def bad(v):raise Fault('NONFINITE_JSON_NUMBER')
 try:
  v=json.loads(raw.decode('utf-8'),object_pairs_hook=pairs,parse_constant=bad)
  canonical(v)
  return v
 except Fault:raise
 except (UnicodeError,ValueError,RecursionError) as exc:raise Fault('INVALID_JSON_OR_CANONICAL_VALUE',detail=str(exc)) from None

def canonical(v):
 import rfc8785
 if version('rfc8785')!='0.1.4':raise Fault('DEPENDENCY_VERSION_MISMATCH')
 pins={'__init__.py':'fa44927afd547caf7547247078bcf28863d1e69caf116d258c532b3f20ffd154','_impl.py':'c25bc3a046528482d53bee3487b837f31dd9c05f33e8f13288c7aab320932cec'}
 if any(sha((Path(rfc8785.__file__).parent/n).read_bytes())!=h for n,h in pins.items()):raise Fault('RFC8785_IMPLEMENTATION_MISMATCH')
 return rfc8785.dumps(v)
def digest(v):return 'sha256:'+sha(canonical(v))
def equal(a,b):return canonical(a)==canonical(b)
def at(v,p):
 if not isinstance(p,str) or (p and not p.startswith('/')):raise Fault('INVALID_POINTER',str(p))
 for part in p.split('/')[1:]:
  if re.search(r'~(?![01])',part):raise Fault('INVALID_POINTER',p)
  k=part.replace('~1','/').replace('~0','~')
  if isinstance(v,list):
   if not re.fullmatch(r'0|[1-9][0-9]*',k) or int(k)>=len(v):raise Fault('UNRESOLVED_POINTER',p)
   v=v[int(k)]
  elif isinstance(v,dict) and k in v:v=v[k]
  else:raise Fault('UNRESOLVED_POINTER',p)
 return v

def instant(t):
 if not isinstance(t,str) or not re.fullmatch(r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{0,8}[1-9])?Z',t):raise Fault('NONCANONICAL_TIME')
 try:d=datetime.strptime(t[:19],'%Y-%m-%dT%H:%M:%S')
 except ValueError:raise Fault('INVALID_CALENDAR_TIME') from None
 f=t[20:-1] if len(t)>20 else ''
 return (d.year,d.month,d.day,d.hour,d.minute,d.second,int(f.ljust(9,'0') or '0'))
