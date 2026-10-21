"""Finite B2 dependency/placement model; no Event Ingress producer or verifier."""
import hashlib
import rfc8785
from commit_class_checks_v3 import canonical_event_errors

def dg(v):return 'sha256:'+hashlib.sha256(rfc8785.dumps(v)).hexdigest()
def event_errors(case,package):
    x=case;intent=x['intent'];errors=canonical_event_errors(case,package)
    def bad(code,ok):
        if not ok:errors.append(code)
    b=intent.get('associatedSemanticEventBinding')
    if b is None:
        bad('UNEXPECTED_ASSOCIATION_INPUT',x.get('envelope') is None and x.get('proof') is None)
        return errors
    rule=package['cases'][x['exampleId']]
    env=x['envelope'];proof=x.get('proof')
    bad('ENVELOPE_BINDING_MISMATCH',b==x['resolvedEnvelopeBinding'])
    bad('FIXED_ENVELOPE_DIGEST_MISMATCH',dg(env)==x['fixedEnvelopeDigest'])
    if proof is None:return errors+['MISSING_INGRESS_PROOF']
    bad('ASSOCIATION_EVIDENCE_ALIAS',not set(x.get('ordinaryEvidenceResolvedDigests',[]))&{dg(env),dg(proof)})
    bad('PROOF_ENVELOPE_DIGEST_MISMATCH',proof.get('envelopeDigest')==dg(env))
    bad('PROOF_NOT_PASSING',proof.get('classificationOutcome')=='PASS')
    bad('FIXED_COMMIT_CLASS_MISMATCH',proof.get('commitClass')==rule['commitClass'])
    bad('AUTHORITATIVE_FAMILY_MISMATCH',proof.get('authoritativeFamily')==env['primaryEventFamily'])
    bad('PROOF_UNAVAILABLE',proof.get('completedBeforeDomainVerdict') is True)
    bad('CYCLIC_PROOF_DEPENDENCY',not set(proof.get('dependsOn',[]))&{'this-domain-verdict','this-domain-trace','final-assertion-effect','later-receipt'})
    bad('CASE_SELECTION_MISMATCH',x['selectedCase']==rule['caseDefinition'])
    bad('TIME_SELECTOR_NOT_PACKAGE_OWNED',x['selectedTimeSelector']==rule['timeSelector'])
    bad('SUBJECT_MEMBERSHIP_MISMATCH',intent['subject']['subjectRef'] in env['subjectRefs'])
    scope={k:intent['resources'][0]['scope'][k] for k in ['scopeType','scopeRef']}
    bad('ANCHOR_MEMBERSHIP_MISMATCH',scope in env['anchorScopes'])
    bad('TIME_COMPARISON_MISMATCH',env['timeSemantics']['eventTime']==intent['subjectTime']['at'])
    bad('COMPATIBILITY_MISMATCH',env['eventSubtypeId']==rule['eventSubtypeId'] and env['dominantSemanticConsequence']==rule['dominantSemanticConsequence'] and x['claimMeaningDigest']==rule['claimMeaningDigest'])
    return errors
