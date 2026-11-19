"""Exact source loading and explicit JSON Schema construction primitives."""
import copy,hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
HEAD='389a8f6b6bb2f43435c35f32df769e723d736856'
PACKET='package_meta/history/clean_baseline_migration/phase_reports/domain_contract_verifier_delivery_v0_1'
SCHEMA_ID='https://ofarm.dev/schema/drafts/non-default/assertion-domain/proposition/v0.1'
BASE_ID='https://ofarm.dev/schema/assertionrecord/v0.2'
VALUE_ID='https://ofarm.dev/schema/drafts/non-default/assertion-domain/owned-value-types/v0.1'
DEFINITION_PREFIX='candidate:assertion-domain-construction:2026-10-21:r2:'
BASE_PATH='03_machine_contracts/drafts_non_default/assertion_record_submission/OFARM_AssertionRecord_schema_v0_2.json'
KINDS=['FARM','SITE','FIELD','ZONE','CROP_CYCLE','LOT','FACILITY','OPERATION','INPUT','EQUIPMENT','TOOL','STORAGE_LOCATION','CONTAINER']
TEXT={'type':'string','minLength':1}
DATE={'type':'string','format':'date','pattern':r'^[0-9]{4}-[0-9]{2}-[0-9]{2}$(?![\s\S])'}
TIMESTAMP={'$ref':BASE_ID+'#/$defs/canonicalTimestamp'}
BINDING={'$ref':BASE_ID+'#/$defs/immutableBinding'}
LOGICAL_REF={'$ref':BASE_ID+'#/$defs/logicalRef'}

def source(path,commit=HEAD,repository='samovers/OFARM'):
    pins=json.loads((HERE/'source-pins.json').read_text())['sources']
    pin=next(p for p in pins if p['originalPath']==path and p['commit']==commit and p['repository']==repository)
    raw=(HERE/pin['localPath']).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=pin['sha256']:raise ValueError('Pinned source changed: '+path)
    return json.loads(raw) if path.endswith('.json') else raw.decode()
def reviewed(name):return source(PACKET+'/'+name)
def ref(name):return {'$ref':'#/$defs/'+name}
def vref(name):return {'$ref':VALUE_ID+'#/$defs/'+name}
def const(value):return {'const':value}
def enum(values):return {'enum':list(values)}
def obj(properties,required=None):return {'type':'object','additionalProperties':False,'properties':properties,'required':list(properties) if required is None else list(required)}
def arr(items,min_items=0,unique=False):return {'type':'array','items':items,'minItems':min_items,**({'uniqueItems':True} if unique else {})}
def one(*options):return {'oneOf':list(options)}
def unreported():return obj({'state':const('UNREPORTED'),'reason':TEXT})
def binding_or_unreported():return one(BINDING,unreported())
def typed_binding(kinds=KINDS):return obj({'kind':enum(kinds),'binding':BINDING})
def condition(field,value,then,otherwise=None):
    return {'if':{'required':[field],'properties':{field:const(value)}},'then':then,**({'else':otherwise} if otherwise is not None else {})}
def absolute_refs(value,base=BASE_ID):
    if isinstance(value,list):return [absolute_refs(x,base) for x in value]
    if not isinstance(value,dict):return value
    return {k:(base+v if k=='$ref' and v.startswith('#') else absolute_refs(v,base)) for k,v in value.items()}
def base_subject():
    value=absolute_refs(copy.deepcopy(source(BASE_PATH)['$defs']['subject']))
    value['properties']['subjectType']=enum(KINDS)
    value['$comment']='New body/subject kind extension only. Existing and prospective wire branches are preserved. Authority anchors are not widened.'
    return value
def base_context():
    value=absolute_refs(copy.deepcopy(source(BASE_PATH)['$defs']['contextBinding']))
    value['properties']['contextRole']=enum(KINDS)
    return value
def put(name,value):(HERE/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
