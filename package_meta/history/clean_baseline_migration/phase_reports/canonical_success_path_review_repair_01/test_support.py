"""Fictional test construction helpers; never a verifier or trusted runtime input."""
import copy,json
from pathlib import Path
from build_fixtures import raw,encode,infer
from path_common import sha,digest
H=Path(__file__).resolve().parent
def replace(v,old,new):
 if v==old:return copy.deepcopy(new)
 if isinstance(v,dict):return {k:replace(x,old,new) for k,x in v.items()}
 if isinstance(v,list):return [replace(x,old,new) for x in v]
 return v

def repin(m,bundle=True,source_digests=True):
 if source_digests:
  for entry in list(m['context']['sources']):
   rec=m['sources'][entry['key']]
   if 'sourceRecordDigest' in rec:
    d=digest({k:v for k,v in rec.items() if k!='sourceRecordDigest'})
    if d!=rec['sourceRecordDigest']:
     old=copy.deepcopy(entry['binding']);new={'ref':old['ref'],'digest':d};rec['sourceRecordDigest']=d;m=replace(m,old,new)
 if bundle:
  r=copy.deepcopy(m['sources']['RESULT']);t=copy.deepcopy(m['sources']['TRACE']);r.pop('decisionBundleDigest');t.pop('decisionBundleDigest');d=digest({'schemaVersion':'ofarm.authorizationDecisionBundleDigestInput.v0.2','request':m['sources']['REQUEST'],'result':r,'trace':t});m['sources']['RESULT']['decisionBundleDigest']=d;m['sources']['TRACE']['decisionBundleDigest']=d;m['evidence']['decisionBundleDigest']=d
 for entry in m['context']['sources']:
  if entry['key'] in m['sources']:
   b=raw(m['sources'][entry['key']]);entry['bytesSha256']=sha(b);entry['valueDigest']=digest(m['sources'][entry['key']])
 return m


def fresh(name='basis-1-party'):
 return json.loads((H/'fixtures'/name/'model.json').read_bytes())
def outputs(m):return [m['sources'][x]['projection'] for x in ['RESULT','TRACE']]
def selected(m):return [m['evidence']['selectedPath'],m['sources']['RESULT']['projection']['selectedPath'],m['sources']['TRACE']['projection']['paths'][0]]
def cohere(m,content=True):
 if content:
  for out in outputs(m):
   for field,key in [('policyDigest','POLICY'),('ruleDigest','RULE'),('derivedViewDigest','DERIVED_VIEW'),('effectIntentDigest','EFFECT_INTENT')]:out[field]=digest(m['sources'][key])
  m['sources']['REQUEST']['projection']['effectIntentDigest']=digest(m['sources']['EFFECT_INTENT'])
 for sid,sc in m['schemas'].items():m['profile']['schemaDigests'][sid]=sha(raw(sc))
 for fmt in m['profile']['formats'].values():fmt['schemaSha256']=m['profile']['schemaDigests'][fmt['schemaId']]
 m['context']['profileBytesSha256']=sha(raw(m['profile']))
 return repin(m)
def rebind_key(m,key,new):
 entry=next(x for x in m['context']['sources'] if x['key']==key);old=copy.deepcopy(entry['binding']);entry['binding']=copy.deepcopy(new)
 if key in m['evidence']['sources']:m['evidence']['sources'][key]=copy.deepcopy(new)
 for path in selected(m):
  for item in path['basis']:
   if item['sourceKey']==key:item['binding']=copy.deepcopy(new)
  path['authoritySubjectBasisRefs']=[x['binding'] for x in path['basis']]
 vis='visibility:'+key
 if vis in m['sources']:
  m['sources'][vis]['projection']['sourceBinding']=copy.deepcopy(new)
  vbinding=next(x['binding'] for x in m['context']['sources'] if x['key']==vis)
  for item in m['sources']['EVALUATION_SNAPSHOT']['projection']['visibleBasis']:
   if item['visibilityBinding']==vbinding:item['binding']=copy.deepcopy(new)
 return m
