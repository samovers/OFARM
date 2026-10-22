"""Author-side AST fault injection; no installed code or dependency bypass is edited."""
from pathlib import Path
import ast,base64,copy,json,types
import verify_success_path as real
from build_fixtures import raw
H=Path(__file__).resolve().parent
source=(H/'verify_success_path.py').read_text();tree=ast.parse(source);fn=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='verify')
sites={};keys={}
for node in ast.walk(fn):
 if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id=='must':
  key=f'{node.lineno}:{node.col_offset}';keys[(node.lineno,node.col_offset)]=key;sites[key]={'id':key,'line':node.lineno,'code':ast.unparse(node.args[1]),'expression':ast.unparse(node.args[0])}
def compile_verify(mutant=None,observe=None):
 class T(ast.NodeTransformer):
  def visit_Call(self,node):
   node=self.generic_visit(node)
   if isinstance(node.func,ast.Name) and node.func.id=='must':
    key=keys[(node.lineno,node.col_offset)]
    if key==mutant:return ast.copy_location(ast.Constant(value=None),node)
    if observe:node.args[0]=ast.Call(func=ast.Name(id='_observe',ctx=ast.Load()),args=[ast.Constant(value=key),node.args[0]],keywords=[])
   return node
 modified=ast.fix_missing_locations(T().visit(copy.deepcopy(fn)));namespace=real.__dict__.copy()
 if observe:namespace['_observe']=observe
 exec(compile(ast.Module(body=[modified],type_ignores=[]),str(H/'verify_success_path.py'),'exec'),namespace)
 return namespace['verify']
def load_case(group,row):
 d=H/group/row['id'];w=json.loads((d/'wire.json').read_bytes());dec=lambda x:base64.b64decode(x)
 result={'id':group+'/'+row['id'],'expected':row['expected'],'expectedCodes':row['expectedCodes'],'expectedDetailContains':row.get('expectedDetailContains'),
         'args':[dec(w['evidenceBytesBase64']),dec(w['profileBytesBase64']),dec(w['contextBytesBase64']),{k:dec(v) for k,v in w['sourceBytesBase64'].items()},{k:dec(v) for k,v in w['schemaBytesBase64'].items()}],
         'pin':(d/'context.sha256').read_text().strip()}
 for arg,value in row.get('apiOverrides',{}).items():result['args'][int(arg)]=value
 return result
cases=[]
for report,group in [('conformance-results.json','checks'),('targeted-results.json','targeted-checks'),('edge-results.json','edge-checks'),('api-only-results.json','api-only-checks')]:
 for row in json.loads((H/report).read_bytes())['results']:
  if 'expectedCodes' in row and row['id'] not in ['changed-installed-source-law','missing-installed-source-root']:cases.append(load_case(group,row))
reached=set();witnesses={};baseline=[];observed_failed=[]
def observe(key,value):
 reached.add(key)
 if not value:observed_failed.append(key)
 return value
instrumented=compile_verify(observe=observe)
for c in cases:
 observed_failed.clear();r=instrumented(*c['args'],expected_context_sha256=c['pin'])
 codes=[e['code'] for e in r['errors']];ok=(r['disposition']=='PASS' if c['expected']=='PASS' else r['disposition']!='PASS') and codes==c['expectedCodes']
 if c['expectedDetailContains']:ok=ok and c['expectedDetailContains'] in r['errors'][0]['detail']
 assert ok,('instrumented baseline differs',c['id'],codes)
 baseline.append({'id':c['id'],'matched':ok})
 for key in observed_failed:witnesses.setdefault(key,[]).append(c)
print('Instrumented corpus',len(cases),'sites',len(sites),'direct witnesses',len(witnesses),flush=True)
mutations=[]
for key,site in sites.items():
 candidates=witnesses.get(key,[])
 if not candidates:
  mutations.append({**site,'classification':'NO_DIRECT_NEGATIVE_WITNESS','executedByCorpus':key in reached});continue
 mutated=compile_verify(mutant=key);tested=[];killed=False;pass_seen=False
 for c in candidates:
  r=mutated(*c['args'],expected_context_sha256=c['pin']);codes=[e['code'] for e in r['errors']]
  matches=(r['disposition']=='PASS' if c['expected']=='PASS' else r['disposition']!='PASS') and codes==c['expectedCodes']
  if c['expectedDetailContains']:matches=matches and bool(r['errors']) and c['expectedDetailContains'] in r['errors'][0]['detail']
  tested.append({'case':c['id'],'disposition':r['disposition'],'codes':codes,'expectedCodeOracleMatches':matches})
  if not matches:killed=True
  if r['disposition']=='PASS':pass_seen=True;break
  if len(tested)>=3 and killed:break
 mutations.append({**site,'classification':'PASS_EXPOSED' if pass_seen else 'SPECIFIC_ERROR_CHANGED' if killed else 'SURVIVED_SAME_EXPECTED_ERROR','witnesses':tested})
 print(key,mutations[-1]['classification'],flush=True)
summary={'scope':'AUTHOR_SIDE_FAULT_INJECTION_NOT_RUNTIME_ATTESTATION','method':'Clone verify AST only, record every must site, then remove one must call in a separate in-memory function. Package/helper/schema/hash checks stay active. Never alter sealed or installed runtime bytes. Specific-code kills and newly accepted negatives are reported separately.',
         'corpusCases':len(cases),'checkSites':len(sites),'directNegativeWitnessSites':len(witnesses),'reachedSites':len(reached),
         'classifications':{s:sum(r['classification']==s for r in mutations) for s in ['PASS_EXPOSED','SPECIFIC_ERROR_CHANGED','SURVIVED_SAME_EXPECTED_ERROR','NO_DIRECT_NEGATIVE_WITNESS']},
         'mutations':mutations,'next':'Review unwitnessed and redundant checks explicitly; do not claim exhaustive mutation coverage.'}
(H/'mutation-results.json').write_bytes(raw(summary));print(json.dumps({k:v for k,v in summary.items() if k!='mutations'},indent=2))
