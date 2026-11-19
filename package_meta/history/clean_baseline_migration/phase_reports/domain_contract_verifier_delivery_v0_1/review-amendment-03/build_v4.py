"""Build v4 only from pinned v3 inputs plus independently authored owner records."""
import argparse,copy,hashlib,json,sys
from pathlib import Path
from build_fix01_sources import repair_hostiles,extend_role_contract
p=argparse.ArgumentParser();p.add_argument('--prior-packet',type=Path,required=True);p.add_argument('--dependency-dir',type=Path,required=True);a=p.parse_args();sys.path.insert(0,str(a.dependency_dir.resolve()));import rfc8785
O=Path(__file__).resolve().parent;V='local-candidate:complete-claims:2026-10-21:amendment-03'
def sha(b):return hashlib.sha256(b).hexdigest()
def dg(x):return 'sha256:'+sha(rfc8785.dumps(x))
def rd(n):return json.loads((a.prior_packet/n).read_text())
def wr(n,x):(O/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
pins=json.loads((O/'source-pins-v4.json').read_text())
for f in pins['priorPacketFiles']:
 if sha((a.prior_packet/f['path']).read_bytes())!=f['sha256']:raise ValueError('Prior source changed: '+f['path'])
owners=json.loads((O/'owner-records-v4.json').read_text());q=owners['quantityProvenance'];k=owners['criterionOwner']
def provenance(binding,root):return {'sourceBinding':copy.deepcopy(binding),'valuePointer':root,'lexicalPointer':root+'/originalLexicalValue','qualifierPointer':root+'/qualifier'}
qp=provenance(q['binding'],'/loq');kp=provenance(k['binding'],'/threshold')
def amend_claim(c):
 c['candidateGrammar']=V;c['proposition']['definition']=V+'#C04';b=c['proposition']['body']
 b['operand']['limit']['provenance']=copy.deepcopy(qp);b['threshold']['provenance']=copy.deepcopy(kp)
 if q['binding'] not in c['evidenceBindings']:c['evidenceBindings'].append(copy.deepcopy(q['binding']))
 return c
prior=rd('candidate-examples-v3.json');bundle=copy.deepcopy(prior);bundle['bundleVersion']=V;bundle['projectionContract']='projection-contract-v4.json';bundle['inheritedGrammarRevisions']=[prior['bundleVersion']]
e=bundle['examples'][4];old=copy.deepcopy(e);amend_claim(e['claimContent']);text='Pending claim: '+rfc8785.dumps(e['claimContent']).decode()+'.';e['exactRenderedText']=text;e['renderedTextSha256']='sha256:'+sha(text.encode());e['claimContentDigest']=dg(e['claimContent']);e['amendment03DerivedFrom']={'sourceHead':pins['sourceHead'],'sourceExampleDigest':dg(old)}
e['evidenceClosure']['selectedCitations'].append({'pointer':'/proposition/body/operand/limit/provenance/sourceBinding','binding':copy.deepcopy(q['binding']),'role':'ASSERTION_EVIDENCE','definition':V+'#C04','selector':'/operand/limit/provenance/sourceBinding'})
e['evidenceClosure']['amendment03AddedBindings']=[copy.deepcopy(q['binding'])]
wr('candidate-examples-v4.json',bundle)
records=rd('measurement-fixtures-v3.json')
records['records'] += [{'role':role,'binding':x['binding'],'contentDigest':dg(x['record']),'record':x['record']} for role,x in [('QUANTITY_PROVENANCE',q),('CRITERION_OWNER',k)]]
wr('measurement-fixtures-v4.json',records)
wr('source-resolution-trace-v4.json',{'status':'FICTIONAL_TRACE_ILLUSTRATION_NOT_VERIFIER_OUTPUT_OR_ADMISSION','case':'W05_CENSORED_CRITERION','ordinaryEvidence':[{'binding':q['binding'],'recordDigest':dg(q['record']),'selectors':qp,'selectedQuantity':q['record']['loq']}],'definitionSources':[{'binding':k['binding'],'recordDigest':dg(k['record']),'selectors':kp,'selectedQuantity':k['record']['threshold'],'operator':k['record']['operator']}],'rule':'All resolved bytes and selected source roles must be bound in the actual domain validation evidence; this illustration grants no admission.'})
expect=rd('criterion-expectations-v3.json');expect['id']='fictional-criterion-owner:W05:v4';expect['definition']=V+'#C04';expect['threshold']=copy.deepcopy(k['record']['threshold']);expect['threshold']['provenance']=kp;expect['operator']=k['record']['operator'];expect['quantityProvenanceBinding']=q['binding'];expect['criterionOwnerBinding']=k['binding'];expect['criterionOwnerDigest']=dg(k['record']);expect['quantityProvenanceDigest']=dg(q['record']);expect['provenance']='Threshold/operator come from separately authored owner-records-v4.json, not the claim. The LOQ scalar lexical/provenance comes from the exact resolved quantity source. All inputs remain fictional and unadmitted.'
wr('criterion-expectations-v4.json',expect)
hostiles=rd('measurement-hostiles-v3.json')
for h in hostiles['cases']:
 amend_claim(h['claimContent']);h['records']+=copy.deepcopy(records['records'][-2:])
repair_hostiles(hostiles,O)
wr('measurement-hostiles-v4.json',hostiles)
proj=rd('projection-contract-v3.json');proj['id']=proj['id'].replace(':v3',':v4');proj['projectionSource']='candidate-examples-v4.json /examples/*/claimContent; v3 definitions remain inherited, W05 uses the explicit v4 C04 extension.';proj['preservation']='24 examples are byte-identical to v3. W05 retains every prior scalar value and qualification, adds exact source provenance and ordinary evidence binding, and is exactly re-rendered under v4. No association metadata is reintroduced.'
wr('projection-contract-v4.json',proj)
sel=rd('evidence-selectors-v3.json');sel['id']=sel['id'].replace(':v3',':v4');sel['definitionPrefixes'].append(V+'#');next(r for r in sel['rowSelectors'] if r['definition']=='C04')['selectors'].append('/operand/limit/provenance/sourceBinding');sel['separateCompleteInputRoles'].append({'role':'CRITERION_THRESHOLD_DEFINITION_SOURCE','selectors':['/proposition/body/threshold/provenance/sourceBinding'],'includeInAssertionEvidenceByDefault':False,'requirement':'Exact independently authored criterion owner record selected by body.criterion; compare operator, bound, qualifier and source lexical value.'})
wr('evidence-selectors-v4.json',sel)
contract=rd('measurement-role-contract-v3.json');contract['id']=V+'#measured-compliance-role-contract';contract['independentExpectation']['file']='criterion-expectations-v4.json';contract['independentExpectation']['sha256']=sha((O/'criterion-expectations-v4.json').read_bytes());contract['ownerRecords']={'file':'owner-records-v4.json','sha256':sha((O/'owner-records-v4.json').read_bytes())};contract['v4Extension']={'definition':V+'#C04','inherits':'local-candidate:complete-claims:2026-10-21:amendment-02#C04','requiredAdditions':['operand.limit.provenance','threshold.provenance'],'meaning':'Qualifier belongs to the exact scalar reporting role; censoring qualifier belongs to the complete measured result. LAB_RESULT alone cannot imply MACHINE_REPORTED. W05 explicitly models human transcription of the LOQ and an independently human-authored fictional criterion.','lexical':'Read the LOQ scalar lexical from the resolved quantity record selected by the exact lexicalPointer; full measured result originalLexicalValue remains < 2 mg/kg. No constant 2 comparison or loss of censoring.','threshold':'The independently authored criterion owner record fixes operator, threshold, qualifier, lexical value, rule/policy and property; changing claim and expected mirror together cannot redefine it.','wrongOrUnknownProvenance':'Reject unknown tokens and tokens inconsistent with the resolved source reporting role, including UNKNOWN for this known reporting role. A broader carrier enum is not semantic permission.','traceClosure':'Bind the exact quantity-source and criterion-owner record digests, immutable bindings and selected value/lexical/qualifier pointers in the domain payload. Ordinary quantity evidence additionally requires exact root evidence membership; the criterion record remains a definition input.', 'typeChecks':'Require object shapes before any member or alias access. Required missing/null/empty/wrong types return structured {code,pointer,...}; closed bindings and absolute RFC6901 pointer strings are checked. This does not expand into the complete domain verifier.'}
extend_role_contract(contract,O)
wr('measurement-role-contract-v4.json',contract)
wr('transformation-ledger-v4.json',{'sourceHead':pins['sourceHead'],'sourceBundleSha256':sha((a.prior_packet/'candidate-examples-v3.json').read_bytes()),'sourceW05Digest':dg(old),'targetW05Digest':dg(e),'unchangedExampleIds':[x['id'] for i,x in enumerate(bundle['examples']) if i!=4 and x==prior['examples'][i]],'W05Changes':['candidateGrammar and C04 definition version','operand.limit.provenance and threshold.provenance','append one exact ordinary quantity-source binding','typed citation metadata and exact JCS/text/content digests'],'unchangedScalarMeaning':{'limit':'2 mg/kg','threshold':'<= 1 mg/kg','allegedOutcome':'INDETERMINATE','limitQualifier':'HUMAN_REPORTED','thresholdQualifier':'HUMAN_REPORTED'},'ownerInputs':'New explicit fictional source records; no producer or source-adoption claim.'})
print('Built v4 bundle, exact owner records, roles and rebased 19 measurement hostiles; 24 examples remain byte-identical.')
