"""Fictional event-owner context and exact carrier placement, not producer output."""
import argparse,copy,hashlib,json,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--dependency-dir',type=Path,required=True);a=p.parse_args();sys.path.insert(0,str(a.dependency_dir.resolve()));import rfc8785
O=Path(__file__).resolve().parent;sys.path.insert(0,str(O));from event_checks_v3 import event_errors

def read(n):return json.loads((O/n).read_text())
def write(n,x):(O/n).write_text(json.dumps(x,indent=2)+'\n')
def dg(x):return 'sha256:'+hashlib.sha256(rfc8785.dumps(x)).hexdigest()
def wire(b):return {'ref':b['fixtureLogicalRef'],'revisionRef':'fixture-revision:'+b['fixtureLogicalRef']+':'+b['fixtureRevision']}
def subject(s):return {'subjectPosture':'EXISTING_SUBJECT','subjectType':s['kind'],'subjectRef':s['binding']['fixtureLogicalRef'],'revisionRef':wire(s['binding'])['revisionRef']}
bundle=read('candidate-examples-v3.json');source=bundle['examples'][24]['offlineBindingIllustration'];package={'status':'FICTIONAL_CLOSED_COMPATIBILITY_RULES_NOT_ADOPTED_EVENT_VOCABULARY','cases':{}};cases=[]
for e in bundle['examples']:
 assoc=e.get('associationVerificationInputs',{})
 if assoc.get('presence')!='PRESENT':continue
 c=e['claimContent'];i=copy.deepcopy(source['intent']);r=copy.deepcopy(source['result'])
 for v in [i,r]:
  v.pop('assertionActEvidenceBinding',None);v['assertionActPosture']='TRUSTED_ONLINE_SUBMISSION';v['assertedAt']=e['governedContextExample']['assertedAt'];v['subject']=subject(c['subject']);v['subjectTime']=copy.deepcopy(c['subjectTime']);v['evidenceBindings']=[wire(b) for b in c['evidenceBindings']];v['subjectScopeProofBindings']=[wire(b) for b in c.get('subjectScopeProofBindings',[])];v['assertionBody']['claimText']=e['exactRenderedText'];v['assertionBody']['temporalBasis']['evidenceBinding'].update(wire(c['temporalBasis']['binding']));v['assertionBody']['temporalBasis']['atPointer']=c['temporalBasis']['pointer'];v['assertionBody']['allegesSoftwareAgentPerformance']=c['allegesSoftwareAgentPerformance']
 i['effectSubject']['subjectRef']='assertion:'+e['id'];r['assertionRecordId']=i['effectSubject']['subjectRef'];i['performedByPartyRef']=c['performedBy']['fixtureLogicalRef'];r['operationClaimContext']['performedByPartyRef']=i['performedByPartyRef'];i['associatedSemanticEventBinding']=wire(assoc['envelope'])
 scope={'scopeType':c['soleAuthorityAnchor']['kind'],'scopeRef':c['soleAuthorityAnchor']['binding']['fixtureLogicalRef'],'revisionRef':wire(c['soleAuthorityAnchor']['binding'])['revisionRef']};i['resources'][0]['scope']=scope;r['anchorScopes']=[copy.deepcopy(scope)]
 meaning=c['proposition'];atom=meaning['child'] if meaning['form']=='QUALIFIED' else meaning
 pruning=e['id'].startswith('W04');dominant='Observed completion of the specified pruning work on the west-edge extent.' if pruning else 'The specified analysis process is in progress for the bound sample and property; no analytical result has yet been produced.'
 rule={'caseDefinition':assoc['caseDefinition'],'timeSelector':'/timeSemantics/eventTime','commitClass':'OPERATION_CLAIM_ASSERTION','eventSubtypeId':'candidate/pruning-completion' if pruning else 'candidate/analysis-in-progress','dominantSemanticConsequence':dominant,'claimMeaningDigest':dg(meaning),'scope':'Only this fictional exact body/case. The immutable package, not caller hints, selects case and pointer.'};package['cases'][e['id']]=rule
 env={'schemaVersion':'ofarm.semanticeventenvelope.v0.1','semanticEventId':assoc['envelope']['fixtureLogicalRef'],'primaryEventFamily':'InterventionEvent' if pruning else 'OccurrenceEvent','eventSubtypeId':rule['eventSubtypeId'],'dominantSemanticConsequence':dominant,'subjectRefs':[c['subject']['binding']['fixtureLogicalRef']],'anchorScopes':[{k:scope[k] for k in ['scopeType','scopeRef']}],'timeSemantics':{'eventTime':c['subjectTime']['at'],'recordTime':e['governedContextExample']['assertedAt']},'notes':'FICTIONAL owner-classification assumption only; family is not inferred by the domain checker.'}
 proof={'fixtureRecordType':'UNADOPTED_CLASSIFICATION_PROOF_MODEL','binding':wire(assoc['ingressEvidence']),'envelopeDigest':dg(env),'authoritativeFamily':env['primaryEventFamily'],'commitClass':'OPERATION_CLAIM_ASSERTION','classificationOutcome':'PASS','completedBeforeDomainVerdict':True,'availability':'VALIDATION_PHASE_BEFORE_DOMAIN_VERDICT','dependsOn':['fixed-envelope','fixed-commit-class'],'admission':'HYPOTHETICAL_OWNER_INPUT_NOT_ADMITTED'}
 case={'exampleId':e['id'],'intent':i,'result':r,'effectIntentDigest':dg(i),'proposedResultDigest':dg(r),'resolvedEnvelopeBinding':wire(assoc['envelope']),'fixedEnvelopeDigest':dg(env),'envelope':env,'proof':proof,'selectedCase':rule['caseDefinition'],'selectedTimeSelector':rule['timeSelector'],'claimMeaningDigest':dg(meaning),'expectedErrors':[],'traceIllustration':{'disposition':'ASSOCIATION_COMPARISONS_HYPOTHETICALLY_COHERENT_NOT_ADMITTED_PASS','envelopeBinding':wire(assoc['envelope']),'envelopeDigest':dg(env),'ingressProofBinding':proof['binding'],'ingressProofDigest':dg(proof),'caseDefinition':rule['caseDefinition'],'selectedTimeSelector':rule['timeSelector'],'subjectIndex':0,'anchorIndex':0,'comparedSubjectTime':c['subjectTime'],'commitClass':proof['commitClass'],'authoritativeFamily':proof['authoritativeFamily']}}
 cases.append(case)
hostiles=[]
for id,fn,code in [
 ('E01_MISSING_PROOF',lambda x:x.update(proof=None),'MISSING_INGRESS_PROOF'),
 ('E02_WRONG_ENVELOPE_DIGEST',lambda x:x['proof'].update(envelopeDigest='sha256:'+'0'*64),'PROOF_ENVELOPE_DIGEST_MISMATCH'),
 ('E03_WRONG_COMMIT_CLASS',lambda x:x['proof'].update(commitClass='STRUCTURE_ASSERTION'),'FIXED_COMMIT_CLASS_MISMATCH'),
 ('E04_FAMILY_DIVERGENCE',lambda x:x['proof'].update(authoritativeFamily='EvidenceEvent'),'AUTHORITATIVE_FAMILY_MISMATCH'),
 ('E05_CALLER_TIME_SELECTOR',lambda x:x.update(selectedTimeSelector='/timeSemantics/recordTime'),'TIME_SELECTOR_NOT_PACKAGE_OWNED'),
 ('E06_LATER_VERDICT_DEPENDENCY',lambda x:x['proof'].update(dependsOn=['this-domain-verdict']),'CYCLIC_PROOF_DEPENDENCY'),
 ('E07_LATER_RECEIPT_DEPENDENCY',lambda x:x['proof'].update(dependsOn=['later-receipt']),'CYCLIC_PROOF_DEPENDENCY'),
 ('E08_UNFINISHED_PROOF',lambda x:x['proof'].update(completedBeforeDomainVerdict=False),'PROOF_UNAVAILABLE'),
 ('E09_PERMISSIVE_CASE_HINT',lambda x:x.update(selectedCase='caller:permissive-case'),'CASE_SELECTION_MISMATCH'),
 ('E10_NOT_PASSING_PROOF',lambda x:x['proof'].update(classificationOutcome='FAIL'),'PROOF_NOT_PASSING')]:
 x=copy.deepcopy(cases[0]);fn(x);x['id']=id;x['expectedErrors']=[code];hostiles.append(x)
for x in cases+hostiles:
 if event_errors(x,package)!=x['expectedErrors']:raise ValueError((x.get('id'),event_errors(x,package)))
write('event-compatibility-package-v3.json',package)
write('event-cases-v3.json',{'status':'FINITE_FICTIONAL_PLACEMENT_AND_DEPENDENCY_MODEL_ONLY','packageFile':'event-compatibility-package-v3.json','packageDigest':dg(package),'positiveCases':cases,'hostileCases':hostiles,'limit':'Base-shaped carriers and schema-shaped fictional envelopes; proof and trace examples are explicitly unadopted models. No producer, reuse/admission interface or current family classification is established. These focused checks do not implement all event compatibility or relationship proof rules.'})
# Complete all tuple source/qualification selectors; prior-only prefix remains valid.
s=read('evidence-selectors-v3.json')
for row in s['rowSelectors']:
 if row['definition']=='C03':row['selectors']+=['/measurementSource/'+k for k in ['measurementBinding','contextBinding','subjectRelationBinding','methodUseBinding']]
 if row['definition']=='C06':row['selectors']+=['/rateSource/measurementSource/'+k for k in ['measurementBinding','contextBinding','subjectRelationBinding','methodUseBinding']]
s['sharedSelectors'].append({'type':'COMPLIANCE_MEASURED_QUALIFICATION','selectors':['/measuredQualification/sourceBinding','/measuredQualification/methodUseBinding'],'guard':'Selected definition/use requires this qualification; presence is independently checked before selection. Applies on the exact atom, never inferred from a wrapper label.'})
write('evidence-selectors-v3.json',s)
print('Built 2 event carrier models and 10 isolated event negatives.')
