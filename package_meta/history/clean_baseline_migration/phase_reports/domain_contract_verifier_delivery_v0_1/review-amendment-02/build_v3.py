"""Finite fictional design construction; no verifier, owner admission or runtime."""
import argparse, copy, hashlib, json, sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--previous-amendment',type=Path,required=True);p.add_argument('--frozen-root',type=Path,required=True);p.add_argument('--repo-root',type=Path,required=True);p.add_argument('--dependency-dir',type=Path,required=True)
a=p.parse_args();sys.path.insert(0,str(a.dependency_dir.resolve()));import rfc8785
OUT=Path(__file__).resolve().parent
VERSION='local-candidate:complete-claims:2026-10-21:amendment-02'
HEAD='8e86208f96756b8f271f490696e6aa7cf23605fe'
def sha(b):return hashlib.sha256(b).hexdigest()
def dg(x):return 'sha256:'+sha(rfc8785.dumps(x))
def bind(ref):return {'fixtureLogicalRef':ref,'fixtureRevision':'r1','admittedRuntimeBinding':False}
def load(p):return json.loads(p.read_text())
def write(name,x): (OUT/name).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def render(c):return 'Pending claim: '+rfc8785.dumps(c).decode()+'.'
prior=load(a.previous_amendment/'candidate-examples-v2.json')
rows=load(a.frozen_root/'domain/inventory.json')['rows']
canon=load(a.frozen_root/'canonical/inventory.json')['rows']
# Expectations are authored independently of the resolved measurement. These are
# fictional criterion/method-owner requirements, not inferred from record labels.
w05=prior['examples'][4]; oldbody=w05['claimContent']['proposition']['body']
expect={
 'id':'fictional-criterion-owner:W05:v3','status':'FICTIONAL_PINNED_EXPECTATIONS_NOT_ADOPTED_RULE_OR_OWNER_ADMISSION',
 'criterionBinding':bind('criterion:W05-nitrate-fictional'),
 'ruleBinding':bind('rule:fictional'),'evidencePolicyBinding':bind('policy:fictional'),
 'definition':VERSION+'#C04','declaredUse':'PENDING_COMPLIANCE_ALLEGATION_ONLY',
 'subject':{'kind':'FIELD','binding':bind('field:fictional')},
 'subjectTime':{'profile':'COMPLIANCE_AS_OF','at':'2026-05-07T18:25:00Z'},
 'extent':{'posture':'FULL_TARGET_SCOPE','binding':bind('field:fictional')},
 'sampleRef':'sample:W05-soil-fictional',
 'observedPropertyRef':'observed-property:soil-nitrate-n',
 'matrixRef':'matrix:soil','analyteRefs':['analyte:nitrate-n'],
 'phenomenonTime':{'timeType':'INSTANT','instant':'2026-05-06T10:05:00Z','timeBasis':'SAMPLE_TIME'},
 'timeUse':{'sampleMustBeNoLaterThanAsOf':True,'resultMayArriveAfterAsOf':True,'claimDoesNotAllegeAnalysisAtSampleTime':True},
 'samplingProtocol':{'procedureRef':'protocol:soil-sampling:composite-topsoil:v1','procedureStatus':'DOCUMENTED_METHOD','issuerRef':'issuer:ofarm-example-profile','versionRef':'v1'},
 'measurementMethod':{'procedureRef':'method:soil-nitrate-colorimetric:example-v2','procedureStatus':'DOCUMENTED_METHOD','issuerRef':'lab:soil-lab-alpha','versionRef':'v2'},
 'contextRef':'observation-context:W05-nitrate-fictional',
 'spatialBasis':'COMPOSITE_SAMPLE_SUPPORT','supportExtentRef':'extent:W05-composite-fictional',
 'geometryBasisRef':'geometry:W05-composite-fictional',
 'measurementBinding':bind('nitrate-measurement:fictional'),
 'contextBinding':bind('observation-context:W05-nitrate-fictional'),
 'subjectRelationBinding':bind('sample-to-field:fictional'),
 'methodUseBinding':bind('method-use:W05-nitrate-fictional'),
 'resultPointer':'/result','qualificationPointers':['/uncertainty'],
 'resultKind':'CENSORED_NUMERIC','censoringQualifier':'BELOW_LOQ',
 'limit':{'limitType':'LOQ','quantityKindRef':'qudt:MassFraction','unitRef':'ucum:mg.kg-1','value':2,'qualifier':'below quantification limit'},
 'originalResultLexicalValue':'< 2 mg/kg','originalUnitText':'mg/kg',
 'uncertainty':{'uncertaintyClass':'QUALITATIVE','statement':'Below-LOQ result is analytically qualified; do not convert to exact zero.'},
 'admissibleValues':{'kind':'INTERVAL','lower':{'decimal':'0','inclusive':True},'upper':{'decimal':'2','inclusive':False},'basis':'METHOD_NONNEGATIVE_BELOW_LOQ'},
 'operator':'LE','threshold':copy.deepcopy(oldbody['threshold']),'allegedOutcome':'INDETERMINATE',
 'evidenceStatus':'REVIEW_REQUIRED','chainOfCustodyStatus':'PRESERVED',
 'scopeLimit':'The sample-support-to-field use is a separately fictional owner qualification. The original canonical field-17 sample is not evidence about field:fictional. No general sample-to-whole-field inference is admitted.',
 'provenance':'C04 meaning and threshold come from the frozen W05. Property, protocol/method and LOQ shape are illustrative nitrate source concepts. Exact target/sample/extent and use permission are newly authored fictional owner assumptions, pinned here before record resolution; no statutory criterion or real owner determination is claimed.'}
write('criterion-expectations-v3.json',expect)
# Exact source clone with an explicit field-level transform map below.
mpath='04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agronomic/OFARM_MeasurementEvidence_example_soil_nitrate_below_loq_lab_result_v0_1.json'
source=load(a.repo_root/mpath);m=copy.deepcopy(source)
m.update(measurementEvidenceId='nitrate-measurement:fictional',sampleRef='sample:W05-soil-fictional',agronomicObservationContextRef='observation-context:W05-nitrate-fictional',evidenceStatus='REVIEW_REQUIRED',provenanceRefs=['provenance:W05-fictional'],originalPayloadRef='local-artifact:W05-fictional',originalPayloadHash='sha256:fictional-unadmitted-payload',notes='Fictional W05 design operand only; not the original field-17 record and not admitted.')
m.pop('upgradeOfMeasurementEvidenceRef')
m['source']={'sourceType':'LAB_REPORT','sourceRef':'lab-report:W05-fictional','sourceSystemRef':'system:W05-fictional','sourceCapturedAt':'2026-05-08T13:32:00Z'}
ctx={
 'schemaVersion':'ofarm.agronomicobservationcontext.v0.1','agronomicObservationContextId':'observation-context:W05-nitrate-fictional','contextState':'REPORTED','observationClass':'LAB_CONTEXT',
 'subject':{'subjectType':'SAMPLE','subjectRef':'sample:W05-soil-fictional'},'targetScope':{'scopeType':'FIELD','scopeRef':'field:fictional'},
 'observedPropertyRef':'observed-property:soil-nitrate-n','phenomenonTime':copy.deepcopy(expect['phenomenonTime']),
 'observationAgent':{'agentType':'PARTY','agentRef':'lab:soil-lab-alpha'},
 'spatialContext':{'scope':{'scopeType':'FIELD','scopeRef':'field:fictional'},'partialExtentRef':'extent:W05-composite-fictional','geometryBasisRef':'geometry:W05-composite-fictional','spatialBasis':'COMPOSITE_SAMPLE_SUPPORT','spatialQuality':'MEASURED'},
 'procedure':{'procedureRef':'method:soil-nitrate-colorimetric:example-v2','procedureStatus':'DOCUMENTED_METHOD','samplingProtocolRef':'protocol:soil-sampling:composite-topsoil:v1','measurementMethodRef':'method:soil-nitrate-colorimetric:example-v2'},
 'measurementEvidenceRefs':['nitrate-measurement:fictional'],'evidenceRefs':['sample-to-field:fictional'],
 'uncertainty':copy.deepcopy(expect['uncertainty']),'contextCompleteness':'DEGRADED_REVIEW_REQUIRED',
 'promotionUse':{'allowedTwinScope':'COMPLIANCE_BLOCKED','highConsequenceUse':'REVIEW_REQUIRED','mustNotPromoteTo':['COMPLIANCE_FACT','CURRENT_STATE_DIRECTLY','ATTESTED_OUTPUT_DIRECTLY']},
 'notes':'Fictional source context; composite support does not itself prove whole-field applicability.'}
relation={'fixtureRecordType':'UNADOPTED_SAMPLE_SUPPORT_RELATION_EXAMPLE','sampleRef':'sample:W05-soil-fictional','contextBinding':bind('observation-context:W05-nitrate-fictional'),'subject':copy.deepcopy(expect['subject']),'subjectTime':copy.deepcopy(expect['subjectTime']),'claimExtent':copy.deepcopy(expect['extent']),'supportExtentRef':'extent:W05-composite-fictional','geometryBasisRef':'geometry:W05-composite-fictional','criterionBinding':copy.deepcopy(expect['criterionBinding']),'declaredUse':'PENDING_COMPLIANCE_ALLEGATION_ONLY','qualification':'FICTIONAL_OWNER_SCOPE_COMPARISON_ASSUMED_NOT_ADMITTED'}
method={'fixtureRecordType':'UNADOPTED_METHOD_USE_EXAMPLE','criterionBinding':copy.deepcopy(expect['criterionBinding']),'method':copy.deepcopy(expect['measurementMethod']),'propertyRef':'observed-property:soil-nitrate-n','matrixRef':'matrix:soil','analyteRefs':['analyte:nitrate-n'],'limit':copy.deepcopy(expect['limit']),'domainLowerBound':{'decimal':'0','inclusive':True},'censoringUpperBound':'EXCLUSIVE_LOQ','statisticalConfidenceIsHardBound':False,'declaredUse':'PENDING_COMPLIANCE_ALLEGATION_ONLY','status':'FICTIONAL_UNADMITTED'}
records=[{'role':role,'binding':expect[key],'contentDigest':dg(record),'record':record} for role,key,record in [('MEASUREMENT','measurementBinding',m),('OBSERVATION_CONTEXT','contextBinding',ctx),('SAMPLE_SUPPORT_RELATION','subjectRelationBinding',relation),('METHOD_USE_QUALIFICATION','methodUseBinding',method)]]
write('measurement-fixtures-v3.json',{'status':'FICTIONAL_RESOLVED_BYTE_MAP_NOT_OWNER_RESOLVER','records':records,'sourceMeasurement':{'path':mpath,'commit':HEAD,'sha256':sha((a.repo_root/mpath).read_bytes())},'sourceTransform':[{'pointer':'/'+k,'before':source.get(k),'after':m.get(k),'operation':'remove' if k not in m else 'add' if k not in source else 'replace'} for k in sorted(source.keys()|m.keys()) if source.get(k)!=m.get(k)]})
# Candidate-only shape. Source membership is separate from mandatory role presence.
src={'role':'MEASURED_COMPLIANCE_OPERAND','measurementBinding':expect['measurementBinding'],'resultPointer':'/result','contextBinding':expect['contextBinding'],'subjectRelationBinding':expect['subjectRelationBinding'],'methodUseBinding':expect['methodUseBinding'],'qualificationPointers':['/uncertainty']}
bundle=copy.deepcopy(prior);bundle.update(bundleVersion=VERSION,projectionContract='projection-contract-v3.json')
trans=[]
for e in bundle['examples']:
 old=next(x for x in prior['examples'] if x['id']==e['id']);c=e['claimContent']; c['candidateGrammar']=VERSION
 ops=[{'op':'replace','path':'/claimContent/candidateGrammar','before':old['claimContent']['candidateGrammar'],'after':VERSION}]
 if 'association' in c:
  e['associationVerificationInputs']=c.pop('association')
  ops.append({'op':'move','from':'/claimContent/association','path':'/associationVerificationInputs','value':e['associationVerificationInputs'],'meaning':'Verification-only association metadata; complete value preserved outside P.'})
 if e['id']=='W05_CENSORED_CRITERION':
  atom=c['proposition'];atom['definition']=VERSION+'#C04';atom['body']['criterion']=copy.deepcopy(expect['criterionBinding']);atom['body']['operand']['source']=copy.deepcopy(src);atom['body']['operand']['admissibleValues']=copy.deepcopy(expect['admissibleValues'])
  ops += [{'op':'replace','path':'/claimContent/proposition/definition','before':old['claimContent']['proposition']['definition'],'after':atom['definition']},{'op':'add','path':'/claimContent/proposition/body/criterion','value':atom['body']['criterion']},{'op':'add','path':'/claimContent/proposition/body/operand/source','value':src},{'op':'add','path':'/claimContent/proposition/body/operand/admissibleValues','value':expect['admissibleValues']}]
  newcites=[];added=[]
  for k in ['measurementBinding','contextBinding','subjectRelationBinding','methodUseBinding']:
   b=src[k];sel='/operand/source/'+k;newcites.append({'pointer':'/proposition/body'+sel,'binding':b,'role':'ASSERTION_EVIDENCE','definition':atom['definition'],'selector':sel})
   if b not in c['evidenceBindings']:c['evidenceBindings'].append(copy.deepcopy(b));added.append(b)
  e['evidenceClosure']['selectedCitations']+=newcites
  e['evidenceClosure']['amendment02AddedBindings']=added
  ops.append({'op':'append','path':'/claimContent/evidenceBindings','values':added})
 e['exactRenderedText']=render(c);e['renderedTextSha256']='sha256:'+sha(e['exactRenderedText'].encode());e['claimContentDigest']=dg(c)
 e['amendment02DerivedFrom']={'sourceHead':HEAD,'sourceExampleJcsSha256':dg(old),'sourceClaimContentDigest':old['claimContentDigest']}
 e['limits']=[x.replace('selector-map.json','selector-map-v3.json') for x in e['limits']]
 trans.append({'id':e['id'],'sourceExampleJcsSha256':dg(old),'sourceContentDigest':old['claimContentDigest'],'targetContentDigest':e['claimContentDigest'],'sourceTextDigest':old['renderedTextSha256'],'targetTextDigest':e['renderedTextSha256'],'operations':ops})
# Rebuild existing carriers and their offline evidence chain, preserving construction order.
e24,e25=bundle['examples'][23:25]
for item in e24['baseV02CarrierIllustration'].values(): item['assertionBody']['claimText']=e24['exactRenderedText']
x=e25['offlineBindingIllustration']
for item in [x['intent'],x['result'],x['evidenceRecord']['submittedContent']]:item['assertionBody']['claimText']=e25['exactRenderedText']
x['evidenceDigest']=dg(x['evidenceRecord'])
for item in [x['intent'],x['result']]: item['assertionActEvidenceBinding']['digest']=x['evidenceDigest']
e25['governedContextExample']['assertionActEvidenceBinding']=copy.deepcopy(x['intent']['assertionActEvidenceBinding'])
x['effectIntentDigest']=dg(x['intent']);x['proposedResultDigest']=dg(x['result']);x['bodyDigest']=dg(x['intent']['assertionBody'])
e25['derivedFrom']['sameClaimContentDigest']=bundle['examples'][2]['claimContentDigest']
for h in bundle['hostileExamples']:
 h['inputs']=copy.deepcopy(x);y=h['inputs']
 if h['expected']=='ATTESTED_BODY_MISMATCH':
  y['evidenceRecord']['submittedContent']['assertionBody']['claimText']+=' Altered.';y['evidenceDigest']=dg(y['evidenceRecord'])
  for k in ['intent','result']:y[k]['assertionActEvidenceBinding']['digest']=y['evidenceDigest']
 else:
  for k in ['intent','result']:y[k]['assertionActEvidenceBinding']['digest']='sha256:'+'0'*64
 y['effectIntentDigest']=dg(y['intent']);y['proposedResultDigest']=dg(y['result'])
bundle['source']['priorAmendment']={'commit':HEAD,'file':'../review-amendment/candidate-examples-v2.json','sha256':sha((a.previous_amendment/'candidate-examples-v2.json').read_bytes())}
write('candidate-examples-v3.json',bundle)
write('source-transform-map-v3.json',{'sourceHead':HEAD,'priorAmendmentDefault':'../review-amendment','examples':trans,'derivedCarrierChanges':['W24: replace claimText in intent/result','W25: replace rendered body, then hash act evidence, then bind it, then hash intent/result','H01/H02: regenerate from W25 with original isolated hostile change'],'priorAmendmentMembers':[{'path':str(f.relative_to(a.previous_amendment)),'sha256':sha(f.read_bytes())} for f in sorted(a.previous_amendment.rglob('*')) if f.is_file()],'frozenManifestSha256':sha((a.frozen_root/'manifest.json').read_bytes()),'preservation':'All 25 domain meanings remain; only grammar/explicit C04 extension, disclosed C04 bindings and removal of verification-only association from P are allowed. All source bytes remain untouched.'})
# V3 projection deliberately excludes the entire association role, including ABSENT.
proj=load(a.previous_amendment/'projection-contract-v2.json');proj['id']=proj['id'].replace(':v2',':v3');proj['projectionSource']=proj['projectionSource'].replace('-v2','-v3');proj['conditionalRootMembers'].remove('association')
proj['presenceRules']['association']='Association is never a member of P. Outside P, ABSENT means no intent associatedSemanticEventBinding; PRESENT carries exact owner verification inputs. No association presence, envelope, ingress reference, compatibility case, time selector, family, proof or association outcome is serialized into claimText or added to assertionBody. Claim domain time and operation meaning remain complete in P.'
proj['excludedExactRoles'].append({'candidateLocation':'associationVerificationInputs (entire object)','wireLocation':'intent /associatedSemanticEventBinding plus separately supplied verification inputs and protected-effect trace; no AssertionRecord destination','reason':'PR23 section 1 item 8, section 7.3 and AR_EVENT_ASSOCIATION require trace-only association. Case IDs and time selectors select verification predicates, not additional claim content.'})
proj['preservation']='Every domain meaning field, exact string, qualification, absence and array order is preserved. The complete association verification role moves outside P; only explicit versioned C04 source/criterion/bounds additions change domain shape. No recursive label filter is used.'
proj['eventMeaningDecision']={'W04':'The pruning completion case restates O08 performanceFacet COMPLETED, exact activityInstance/work specification/finish conditions, target/extent and subjectTime already in P. It adds no domain allegation.','W22':'The O22 in-progress compatibility case restates performanceFacet IN_PROGRESS and actual pending analytical output, target/context and subjectTime already in P. It adds no domain allegation.','futureDomainMeaning':'A new domain allegation about an event requires an independently versioned domain atom and ordinary supporting-evidence role; it may not smuggle this submission association or its verification data into P.'}
proj['timingStatus']='WAITING_FOR_COORDINATOR_CANONICAL_TIMING_NOTE'
write('projection-contract-v3.json',proj)
sel=load(a.previous_amendment/'evidence-selectors.json');sel['id']=sel['id'].replace(':v2',':v3');sel['definitionPrefixes']=[sel.pop('definitionPrefix'),VERSION+'#']
sel['rowSelectors'] += [{'definition':'C03','selectors':['/measurement'],'meaning':'Required measured numeric operand; operandPointer and criterion are separately mandatory.'},{'definition':'C04','selectors':['/operand/source/'+k for k in ['measurementBinding','contextBinding','subjectRelationBinding','methodUseBinding']],'meaning':'Four required source roles exist before membership is checked; resultPointer and qualificationPointers select exact source content.'},{'definition':'C06','selectors':['/rateSource/sourceBinding'],'guard':'Required for a relied-on rate; sourceKind selects MEASUREMENT_EVIDENCE or exact report/operation-parameter source. The measured branch also needs complete measurementSource.','meaning':'Rate cannot become an unbound measured fact.'},{'definition':'C09','selectors':['/measurementSource/measurementBinding','/measurementSource/contextBinding','/measurementSource/subjectRelationBinding','/measurementSource/methodUseBinding'],'guard':{'pointer':'/evidencePosture','equals':'MEASURED'},'meaning':'Measured branch requires source completeness; MODELLED remains an explicit model-owner branch.'}]
for r in sel['separateCompleteInputRoles']:
 if r['role'] in ['SEMANTIC_EVENT','EVENT_INGRESS_PROOF']:
  r['selectors']=[x.replace('/association/','associationVerificationInputs/') for x in r['selectors']];r['includeInRender']=False
sel['completenessContract']='measurement-role-contract-v3.json; check required roles from the selected definition/criterion before enumerating citations. Missing source or value pointer is a failure even when table and recorded citations both omit it.'
sel['coverageLimit']='All cited roles in the 25 whole examples; required measured-compliance role rules additionally cover C03/C04 and analogous C06/C09 branches plus qualifications and owner-evaluated inputs. This does not materialize all 99 definitions or establish production admission.'
write('evidence-selectors-v3.json',sel)
sm=load(a.previous_amendment/'selector-map.json');sm['id']=sm['id'].replace(':v2',':v3');sm['base']='PR45 2110f6d78451b50712264dba87d0b8989f134907; immediate source PR47 '+HEAD
for r in sm['existingMappings']:
 if r['candidate'].startswith('/association/'):
  r['candidate']='associationVerificationInputs/envelope when PRESENT';r['rule']='Only this immutable binding enters intent /associatedSemanticEventBinding. All association metadata remains outside P and AssertionRecord. ABSENT means absence. Event ingress and case/time predicates are separately governed verification inputs.'
sm['newTypedBodyRequirements']=[x for x in sm['newTypedBodyRequirements'] if x['candidate']!='association case/context']
sm['newTypedBodyRequirements'].append({'candidate':'C04 operand/source, criterion and admissibleValues; other measured compliance roles','proposedSelector':'/assertionBody/proposition under the new explicitly selected body schema','rule':'Versioned domain meaning/source links from measurement-role-contract-v3.json. These fields do not exist in the old v0.2 body schema; no old schema is modified.'})
sm['timingStatus']='WAITING_FOR_COORDINATOR_CANONICAL_TIMING_NOTE'
write('selector-map-v3.json',sm)
print('Built v3 fictional examples; event timing remains pending.')
