"""Offline validation of pinned source schemas and sealed pure value helpers."""
import hashlib, importlib.util, json, sys
from common import *
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource
from time_validation import foreign_instant

# Verify the sealed inputs before importing their pure helpers. Nothing in the
# sealed checkpoint is rewritten and no old finite-form checker is called.
manifest=json.loads((HERE.parent/'checkpoint-manifest.json').read_text())
manifest_bytes=(HERE.parent/'checkpoint-manifest.json').read_bytes()
if hashlib.sha256(manifest_bytes).hexdigest()!='f294ae03ec72ab7fd404b412014261823783a9ce71578fa12884115efa91a775':
    raise ValueError('Sealed checkpoint manifest changed')
# The manifest has its own explicit member list, inspected below by path.
for entry in manifest.get('members',[]):
    path=entry.get('path',entry.get('file'))
    if path and hashlib.sha256((HERE.parent/path).read_bytes()).hexdigest()!=entry['sha256']:
        raise ValueError('Sealed checkpoint member changed: '+path)
sys.path.append(str(HERE.parent))
spec=importlib.util.spec_from_file_location('sealed_domain_values',HERE.parent/'domain_owned.py')
sealed=importlib.util.module_from_spec(spec);spec.loader.exec_module(sealed)
exact,instant,number,error=sealed.exact,sealed.instant,sealed.number,sealed.error
interval_outcome=sealed.interval_outcome

def pointer(value,path):
    """RFC 6901 traversal, with no dynamic evaluation or string fallback."""
    if not isinstance(path,str) or (path and not path.startswith('/')):raise ValueError('Invalid JSON pointer')
    for encoded in path.split('/')[1:]:
        import re
        if re.search(r'~(?![01])',encoded):raise ValueError('Invalid JSON pointer escape')
        key=encoded.replace('~1','/').replace('~0','~')
        if isinstance(value,list):
            if not re.fullmatch(r'0|[1-9][0-9]*',key):raise ValueError('Invalid array index')
            try:value=value[int(key)]
            except IndexError:raise ValueError('Missing array index') from None
        elif isinstance(value,dict) and key in value:value=value[key]
        else:raise ValueError('Missing pointer target')
    return value

def schema_resources():
    values={}
    pins=json.loads((HERE/'source-pins.json').read_text())['sources']
    # Current contracts win over historical schemas of the same identity.
    for pin in sorted(pins,key=lambda p:p['commit']==HEAD):
        if not pin['originalPath'].endswith('.json'):continue
        value=source(pin['originalPath'],pin['commit'],pin['repository'])
        if '$schema' in value and '$id' in value:values[value['$id']]=value
    for path in [HERE/'owned-value-types-amendment.schema.json',HERE/'proposition.schema.json',HERE/'canonical-inputs.schema.json']:
        if path.exists():
            value=json.loads(path.read_text());values[value['$id']]=value
    return values

class Schemas:
    def __init__(self):
        self.schemas=schema_resources()
        self.registry=Registry().with_resources((key,Resource.from_contents(value)) for key,value in self.schemas.items())
        self.format_checker=FormatChecker()
        @self.format_checker.checks('date-time',raises=ValueError)
        def strict_source_timestamp(value):
            if not isinstance(value,str):return True
            foreign_instant(value)
            return True
    def errors(self,schema_id,value,definition=None):
        target=schema_id+('#/$defs/'+definition if definition else '')
        if schema_id not in self.schemas:return [error('SCHEMA_NOT_IN_PINNED_REGISTRY','',schemaId=schema_id)]
        validator=Draft202012Validator({'$ref':target},registry=self.registry,format_checker=self.format_checker)
        try:
            return [error('SCHEMA_SHAPE','/'+('/'.join(str(x).replace('~','~0').replace('/','~1') for x in e.absolute_path)),keyword=e.validator,schema=target) for e in sorted(validator.iter_errors(value),key=lambda e:str(list(e.absolute_path)))]
        except Exception as exc:
            # An unresolved schema is an execution error, never a successful leaf.
            return [error('SCHEMA_RESOLUTION_ERROR','',schema=target,reason=str(exc))]

class Values(sealed.OwnedComponent):
    def __init__(self,schemas):
        self.schemas=schemas;self.value_schema=schemas.schemas[VALUE_ID];self.registry=schemas.registry
        self.contracts=json.loads((HERE.parent/'owned-contract-inputs.json').read_text())
    def value_errors(self,name,value):return self.schemas.errors(VALUE_ID,value,name)
