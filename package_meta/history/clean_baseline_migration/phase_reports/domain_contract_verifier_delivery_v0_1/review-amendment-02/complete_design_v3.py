"""Complete finite owner design records after the canonical timing note."""
import argparse,copy,hashlib,json,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--frozen-root',type=Path,required=True);p.add_argument('--canonical-owner',type=Path,required=True);p.add_argument('--dependency-dir',type=Path,required=True);a=p.parse_args();sys.path.insert(0,str(a.dependency_dir.resolve()));import rfc8785
O=Path(__file__).resolve().parent
sys.path.insert(0,str(O));from measurement_checks_v3 import w05_errors,required_role_errors
V='local-candidate:complete-claims:2026-10-21:amendment-02'
def read(n):return json.loads((O/n).read_text())
def write(n,x):(O/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def sha(b):return hashlib.sha256(b).hexdigest()
def dg(x):return 'sha256:'+sha(rfc8785.dumps(x))
def bind(x):return {'fixtureLogicalRef':x,'fixtureRevision':'r1','admittedRuntimeBinding':False}
def wire(x):return {'ref':x['fixtureLogicalRef'],'revisionRef':'fixture-revision:'+x['fixtureLogicalRef']+':'+x['fixtureRevision']}
expected=read('criterion-expectations-v3.json');bundle=read('candidate-examples-v3.json');fixtures=read('measurement-fixtures-v3.json')
canonical={'resolutionPath':'canonical-owner/resolution.md','resolutionSha256':sha((a.canonical_owner/'resolution.md').read_bytes()),'checksPath':'canonical-owner/source-checks.json','checksSha256':sha((a.canonical_owner/'source-checks.json').read_bytes())}
for f in ['projection-contract-v3.json','selector-map-v3.json']:
 x=read(f);x['timingStatus']='SOURCE_OWNER_RESOLUTION_INTEGRATED_NO_PRODUCER_GUARANTEE';x['canonicalOwnerResolution']=canonical
 x['associationAliasRule']='No association envelope, ingress proof or dependent validation trace may be laundered into ordinary assertion evidence under another logical name; use owner-resolved immutable byte identity and dependency closure. This excludes association verification roles, not independently defined ordinary domain evidence about an event.'
 x['eventTiming']={'beforeIntentHash':'Fix exact body, expected package and either no association or immutable resolvable envelope binding/bytes.','beforeDomainPass':'Separate owner proof must be complete, eligible and exact for envelope digest, authoritative family and fixed commit class.','preSubmissionProofGuaranteed':False,'validationPhaseProof':'Permitted dependency order if independently completed before the verdict consumes it. No existing producer is claimed.','forbiddenDependencies':['this domain verdict','this domain trace','final assertion effect','later receipt'],'openOwnerInterface':'Actual proof artifact/schema, producer, admission/reuse/context and availability milestone. A late CommitIngressResult is not automatically the earlier classification proof.'}
 write(f,x)
contract={
 'id':V+'#measured-compliance-role-contract','status':'PROPOSED_EXTENSION_NOT_ADOPTED_SCHEMA_OR_VERIFIER','trustBoundary':'AssertionRecord domain meaning and validation integrity',
 'independentExpectation':{'file':'criterion-expectations-v3.json','sha256':sha((O/'criterion-expectations-v3.json').read_bytes()),'authority':'Fictional independently authored criterion/method-owner expectations. Resolve the selected rule/criterion first; never set expected property, scope or method from the cited measurement. A runtime positive requires real adopted owner inputs.'},
 'definitionOverrides':[{'definition':V+'#'+r,'inherits':'local-candidate:complete-claims:2026-10-20:r4#'+r,'change':desc} for r,desc in [('C03','Require complete measured source tuple; preserve measurement and operandPointer and compare their exact equality to tuple aliases.'),('C04','Require criterion, operand.source and explicit admissibleValues; preserve existing resultKind/qualifier/limit/nonnegative/operator/threshold/outcome.'),('C06','Require rateSource for the relied-on reported rate. Distinguish HUMAN_REPORT, OPERATION_PARAMETER and MEASUREMENT_EVIDENCE; measured branch needs complete measurementSource.'),('C09','MEASURED requires measurementSource. MODELLED/ESTIMATED/DISPUTED retain exact owner basis and qualifications; no substitution of a measured source.')]],
 'sourceTuple':{'role':'MEASURED_COMPLIANCE_OPERAND','required':['role','measurementBinding','resultPointer','contextBinding','subjectRelationBinding','methodUseBinding','qualificationPointers'],'bindingShape':'Exact fixture binding here; production exact immutable ref plus revisionRef XOR digest, specialized measurement schema identity separately verified and trace-bound.','pointerSemantics':'Absolute RFC6901 pointer into the exact resolved measurement; no search/latest/first-member/default. C04 below-LOQ uses /result, then fixed resultKind/censoringQualifier/detectionLimit fields. C03 numeric uses /result/numericValue plus the containing result metadata. No value guessed from the pointer name.','qualificationPointers':'Nonempty exact pointers for every relied-on uncertainty/quality field required by the selected method/use; explicit NOT_APPLICABLE must itself be method-bound.','unknownMembers':'The future selected row/body schema must be closed. These are proposed additions, not permissive extras to frozen r4 or base v0.2 schemas.'},
 'requiredBeforeCitationSelection':['Select exact adopted definition and criterion/evidence-use requirements independently.','Require every operand and qualification role that definition/use requires, even if no citation or metadata has been supplied.','Reject missing/empty source bindings and value/qualification pointers; unknown branch or missing branch discriminator cannot suppress a requirement.','Resolve exact immutable source bytes and schema; prove exact evidenceBindings membership separately.','Validate source pointers and typed value shape before semantic comparison.','Compare property, subject/sample/target/support, method/protocol revision, analyte/matrix, phenomenon-time role/value, unit/basis, LOQ/LOD/range and uncertainty against criterion and owner facts.','Only then calculate the criterion relation using exact supported units and admissible values.'],
 'C04Branches':{
  'NUMERIC':'Require exact numeric pointer, quantity/unit/profile and original lexical preservation; uncertainty can widen admissible values only under explicit method rule.',
  'CENSORED_NUMERIC':'Require full result pointer, qualifier and detectionLimit type/kind/unit/value. BELOW_LOQ cannot use LOD, zero or numericValue. BELOW_LOD, ABOVE_RANGE, NON_DETECT and TRACE_DETECTED need their own method interpretation; no borrowed BELOW_LOQ rule.',
  'INTERVAL_OR_QUANTIFIED_UNCERTAINTY':'Bind exact source uncertainty fields and separately pinned method rule supplying endpoints, inclusivity, units and interpretation. A confidence interval is not automatically a hard admissible set. Missing endpoints/interpretation prevents the claimed comparison.',
  'CODED_OR_QUALITATIVE':'A numeric criterion needs an explicitly bound owner mapping that preserves the source code/text semantics; no implicit number conversion.',
  'ABSENT_PENDING':'No numeric operand exists; keep pending/unknown qualification and INDETERMINATE where the rule permits. Do not invent zero or a limit.'},
 'comparison':'Use exact rule operator and bound. SATISFIED iff all admissible values satisfy; NOT_SATISFIED iff all fail; otherwise INDETERMINATE. Source insufficiency remains a separate failed/unresolved obligation; it is not excused merely by alleging INDETERMINATE.',
 'W05':'Criterion independently expects soil nitrate-N in the declared sample/context/method, with a nonnegative domain and exclusive upper LOQ 2 mg/kg. [0,2) against <=1 mg/kg is INDETERMINATE. Sample time May 6 is permitted for as-of May 7 under this fictional use; later resultTime does not rewrite subjectTime or allege analysis at sample time.',
 'qualificationRules':'A measured/uncertain sourceQuality claim or method-required qualification requires explicit measuredQualification {sourceBinding,sourcePointer,methodUseBinding,interpretation} on its exact atom under the new definition. This field is outside the three existing QUALIFIED wrapper keys; the wrapper never changes atom values. Missing required qualifier cannot be concealed by removing both qualifier and its citation. Only the selected owner use determines when required.',
 'analogousOwnerEvaluations':'C02 measured applicability, C07 measured accounting inputs, C10 policy-qualified evidence and C16 calculated operands remain governed by the exact rule/model/profile evaluation owner. Resolve each required measured role inside the exact referenced evaluation and apply this source-tuple discipline, without inventing statutory formulas or converting owner summaries into measurements.',
 'evidenceClosure':'measurementBinding/contextBinding/subjectRelationBinding/methodUseBinding and qualification source/method records are ASSERTION_EVIDENCE for these roles. Criterion/rule/unit profile definitions remain exact definition inputs. No source gets admission from list membership.',
 'limits':['Only W05 source-semantic comparisons and a finite required-role corpus are executable here. No all-branch numerical engine or public verifier is implemented.','All 99 frozen inventory definitions, event/time cells and qualifiers remain obligations; no narrowed coverage or adoption is asserted.']}
write('measurement-role-contract-v3.json',contract)
# An explicit all-compliance-row audit, independent of the prior selector table.
rows=json.loads((a.frozen_root/'domain/inventory.json').read_text())['rows']
decisions={
'C01':('SOURCE_RELEVANCE','Report/event basis is evidence, not a numeric operand. If the selected relevance use relies on measured content, the exact report-to-measurement link and measured role are required by that use.'),
'C02':('CONDITIONAL_OWNER_OPERAND','Applicability conditions can depend on measured context. Required roles come from the pinned rule; absent measured conditions may not be silently skipped.'),
'C03':('DIRECT_MEASURED_OPERAND_REPAIRED','Existing measurement and operandPointer now have mandatory presence, exact tuple consistency and an evidence selector. New supplementary role fixture checks deletion even when citation table omits the role.'),
'C04':('DIRECT_MEASURED_OPERAND_REPAIRED','W05 adds exact source tuple, criterion, admissible bounds and independently pinned expectations. Uncertainty/censoring qualifiers are linked to exact source pointers and method use.'),
'C05':('NO_MEASURED_OPERAND_IN_ROW','Registry identity/currentness is separate owner verification; do not infer measurement from status.'),
'C06':('REPORTED_RATE_SOURCE_REPAIRED','HUMAN_REPORTED rate remains that posture. Required rateSource links the exact reported value; measured branch uses complete tuple. Label-bound thresholds and actual/planned material/basis/scope remain independent.'),
'C07':('CONDITIONAL_OWNER_OPERAND','Mass-balance/accounting owner may require measured inputs. The row is a model allegation, not an unbound numeric total; preserve exact owner evaluation and require its operands under its pinned contract.'),
'C08':('NO_MEASURED_OPERAND_IN_ROW','Report exact inspection decision; do not reinterpret its finding as a raw measurement.'),
'C09':('MEASURED_BRANCH_REPAIRED','MODELLED baseline retains model basis. MEASURED branch requires tuple and qualification provenance; qualifier/branch deletion cannot bypass selected metric requirements.'),
'C10':('MEASUREMENT_QUALIFICATION_USE','Policy sufficiency may depend on calibration/custody or other measurement qualification. Required-use owner determines fields; qualify exact records/pointers, never generic ACCEPTED_SUPPORT labels.'),
'C11':('NO_MEASURED_OPERAND_IN_ROW','Official registration/status source, not measured quantity.'),
'C12':('NO_MEASURED_OPERAND_IN_ROW','Certificate/issuer/scope/date/adverse status evidence remains exact; no measured quantity.'),
'C13':('NO_MEASURED_OPERAND_IN_ROW','Ministry/accreditation scope/date reports remain owner references.'),
'C14':('NO_MEASURED_OPERAND_IN_ROW','Review/appeal state remains official artifact meaning.'),
'C15':('NO_MEASURED_OPERAND_IN_ROW','Source-preserved filing/history and year-code lineage; cannot insert measured area arithmetic without a defined owner role.'),
'C16':('CONDITIONAL_OWNER_OPERAND','Any measured/calculated profile operand must be explicitly sourced in the pinned profile-owner evaluation. Do not manufacture missing NL calculation rules; current INDETERMINATE example remains unchanged.'),
'C17':('NO_MEASURED_OPERAND_IN_ROW','Record completeness checks presence/units/roles of the use record, distinct from proving measured actual quantities or lawful use.')}
write('compliance-role-audit-v3.json',{'status':'SOURCE_ROW_AUDIT_NOT_FULL_VERIFIER','sourceFile':'reviewed-input/domain/inventory.json','sourceSha256':sha((a.frozen_root/'domain/inventory.json').read_bytes()),'rows':[{'id':r['id'],'sourceRowDigest':dg(r),'name':r['name'],'evidencePredicates':r['evidencePredicates'],'classification':decisions[r['id']][0],'disposition':decisions[r['id']][1]} for r in rows if r['id'].startswith('C')],'crossCutting':['C04 source/result and method-derived bound qualifiers','QUALIFIED sourceQuality on an atom that alleges a measured/uncertain basis','C06 source posture and C09 MEASURED vs MODELLED/ESTIMATED/DISPUTED','Required measured inputs inside C02/C07/C10/C16 selected owner evaluations'],'limit':'Conditional owner roles are identified as required construction obligations, not claimed materialized or admitted here.'})
# Concrete C04 near-misses use complete fixtures and rehash every changed source.
c=next(x['claimContent'] for x in bundle['examples'] if x['id']=='W05_CENSORED_CRITERION');base={'claimContent':c,'records':fixtures['records']}
cases=[]
def add(name,modify,expected_codes):
 x=copy.deepcopy(base);modify(x)
 for r in x['records']:r['contentDigest']=dg(r['record'])
 cases.append({'id':name,'expectedErrors':expected_codes,**x})
def operand(x):return x['claimContent']['proposition']['body']['operand']
def record(x,role):return next(r['record'] for r in x['records'] if r['role']==role)
def wrong_property(x):
 r=next(r for r in x['records'] if r['role']=='MEASUREMENT');old=copy.deepcopy(r['binding']);r['binding']=bind('measurement:wrong-property-fictional');r['record']['measurementEvidenceId']=r['binding']['fixtureLogicalRef'];r['record']['observedPropertyRef']='observed-property:soil-potassium'
 operand(x)['source']['measurementBinding']=copy.deepcopy(r['binding']);x['claimContent']['evidenceBindings']=[r['binding'] if b==old else b for b in x['claimContent']['evidenceBindings']]
 record(x,'OBSERVATION_CONTEXT')['measurementEvidenceRefs']=[r['binding']['fixtureLogicalRef']]
add('H03_WRONG_PROPERTY_VALID_SOURCE_AND_MEMBERSHIP',wrong_property,['PROPERTY_MISMATCH'])
add('H04_MISSING_SOURCE_ROLE',lambda x:operand(x).pop('source'),['MISSING_REQUIRED_ROLE:/operand/source'])
add('H05_MISSING_VALUE_POINTER',lambda x:operand(x)['source'].pop('resultPointer'),['MISSING_REQUIRED_ROLE:/operand/source/resultPointer'])
add('H06_WRONG_POINTER_VALID_SCALAR',lambda x:operand(x)['source'].update(resultPointer='/result/detectionLimit/value'),['SOURCE_POINTER_MISMATCH','SOURCE_VALUE_SHAPE_MISMATCH'])
add('H07_WRONG_TARGET',lambda x:record(x,'SAMPLE_SUPPORT_RELATION')['subject']['binding'].update(fixtureLogicalRef='field:other'),['TARGET_SUPPORT_MISMATCH'])
add('H08_WRONG_METHOD_REVISION',lambda x:record(x,'MEASUREMENT')['measurementMethod'].update(versionRef='v3'),['METHOD_MISMATCH'])
add('H09_LOD_NOT_LOQ',lambda x:record(x,'MEASUREMENT')['result']['detectionLimit'].update(limitType='LOD'),['LOQ_VALUE_UNIT_MISMATCH'])
add('H10_WRONG_PHENOMENON_TIME',lambda x:record(x,'MEASUREMENT')['phenomenonTime'].update(instant='2026-05-07T18:25:00Z'),['PHENOMENON_TIME_MISMATCH'])
add('H11_LOQ_UPPER_MADE_INCLUSIVE',lambda x:operand(x)['admissibleValues']['upper'].update(inclusive=True),['METHOD_DOMAIN_BOUNDS_MISMATCH'])
add('H12_CONFIDENCE_USED_AS_HARD_BOUND',lambda x:record(x,'METHOD_USE_QUALIFICATION').update(statisticalConfidenceIsHardBound=True),['METHOD_DOMAIN_BOUNDS_MISMATCH'])
add('H13_CONTEXT_NOT_IN_EVIDENCE',lambda x:x['claimContent']['evidenceBindings'].remove(expected['contextBinding']),['MISSING_ASSERTION_EVIDENCE:contextBinding'])
add('H14_MISSING_QUALIFICATION_POINTER',lambda x:operand(x)['source'].pop('qualificationPointers'),['MISSING_REQUIRED_ROLE:/operand/source/qualificationPointers'])
add('H15_WRONG_THRESHOLD',lambda x:x['claimContent']['proposition']['body']['threshold'].update(decimal='3'),['THRESHOLD_RULE_MISMATCH'])
add('H16_FALSE_SATISFIED',lambda x:x['claimContent']['proposition']['body'].update(allegedOutcome='SATISFIED'),['OUTCOME_MISMATCH'])
add('H17_WRONG_SAMPLE',lambda x:record(x,'MEASUREMENT').update(sampleRef='sample:other'),['SAMPLE_MISMATCH'])
add('H18_WRONG_MATRIX',lambda x:record(x,'MEASUREMENT')['labContext'].update(matrixRef='matrix:water'),['MATRIX_ANALYTE_MISMATCH'])
add('H19_WRONG_LEXICAL_RESULT',lambda x:record(x,'MEASUREMENT')['result'].update(originalLexicalValue='0 mg/kg'),['LEXICAL_RESULT_MISMATCH'])
add('H20_UNCERTAINTY_ERASED',lambda x:record(x,'MEASUREMENT').pop('uncertainty'),['QUALIFICATION_SOURCE_MISMATCH','QUALIFICATION_POINTER_UNRESOLVED'])
add('H21_DISPUTED_AS_UNQUALIFIED',lambda x:record(x,'MEASUREMENT').update(evidenceStatus='DISPUTED'),['SOURCE_POSTURE_MISMATCH'])
for x in cases:
 observed=w05_errors(x['claimContent'],x['records'],expected)
 if observed!=x['expectedErrors']:raise ValueError((x['id'],observed,x['expectedErrors']))
write('measurement-hostiles-v3.json',{'status':'FICTIONAL_ISOLATED_CASES_NOT_VERIFIER_RESULTS','cases':cases})
# Role presence examples are separate from the 25 preserved whole claims.
byrow={r['id']:r for r in rows};src=copy.deepcopy(c['proposition']['body']['operand']['source'])
rolecases=[]
for row in ['C03','C06','C09']:
 b=copy.deepcopy(byrow[row]['typedRepresentation']['body'])
 if row=='C03':
  s=copy.deepcopy(src);s.update(measurementBinding=b['measurement'],resultPointer=b['operandPointer']);b['measurementSource']=s
 if row=='C06':b['rateSource']={'sourceKind':'HUMAN_REPORT','sourceBinding':bind('rate-report:fictional'),'valuePointer':'/rate'}
 if row=='C09':b['evidencePosture']='MEASURED';b['measurementSource']=copy.deepcopy(src)
 rolecases.append({'id':row+'_ROLE_COMPLETE','definition':V+'#'+row,'body':b,'expectedErrors':[],'limit':'Required-role structure only; no numeric value, source-semantic or owner-admission positive claimed.'})
 for key in ({'C03':['measurement','operandPointer','measurementSource'],'C06':['rateSource'],'C09':['measurementSource']}[row]):
  b2=copy.deepcopy(b);b2.pop(key);rolecases.append({'id':row+'_MISSING_'+key,'definition':V+'#'+row,'body':b2,'expectedErrors':required_role_errors(row,b2)})
qbody=copy.deepcopy(rolecases[0]['body']);qbody['measuredQualification']={'sourceBinding':src['measurementBinding'],'sourcePointer':'/uncertainty','methodUseBinding':src['methodUseBinding'],'interpretation':'STATISTICAL_NOT_HARD_BOUND'}
rolecases.append({'id':'C03_REQUIRED_QUALIFICATION_COMPLETE','definition':V+'#C03','body':qbody,'qualificationRequiredByOwner':True,'expectedErrors':[]})
qbad=copy.deepcopy(qbody);qbad.pop('measuredQualification');rolecases.append({'id':'C03_REQUIRED_QUALIFICATION_REMOVED','definition':V+'#C03','body':qbad,'qualificationRequiredByOwner':True,'expectedErrors':['MISSING_REQUIRED_ROLE:/measuredQualification']})
write('compliance-role-cases-v3.json',{'status':'FINITE_REQUIRED_ROLE_CASES_ONLY','cases':rolecases})
# Coverage preservation: whole frozen inventories remain dependencies, not a narrowed replacement.
ci=json.loads((a.frozen_root/'canonical/inventory.json').read_text())['rows']
write('coverage-preservation-v3.json',{'domainRows':[{'id':r['id'],'jcsDigest':dg(r)} for r in rows],'canonicalRows':[{'id':r['id'],'jcsDigest':dg(r)} for r in ci],'domainCount':len(rows),'canonicalCount':len(ci),'eventRows':len([r for r in ci if r['id'].startswith('V04')]),'measurementRows':len([r for r in ci if r['id'].startswith('V05')]),'wholeExampleIds':[e['id'] for e in bundle['examples']],'eventTimeCoverage':'All 9 time profiles and 17 eligible event/profile cells remain required from the frozen canonical V04-profiles definition; none is removed or reclassified.','measurementCoverage':'All 17 V05 rows, including six phenomenon-time postures, five result branches, source examples, full context and code bindings remain required.','limit':'Custody and preservation coverage only, not a rerun or replacement of the original semantic inventory review.'})
write('canonical-timing-integration-v3.json',{'canonicalOwner':canonical,'decision':'Complete association role excluded from P; exact existing intent envelope slot plus separate owner proof and protected-effect trace. No new authority or producer.','timing':read('projection-contract-v3.json')['eventTiming']})
print('Completed F4 role audit, 19 measurement negatives, coverage and canonical timing integration.')
