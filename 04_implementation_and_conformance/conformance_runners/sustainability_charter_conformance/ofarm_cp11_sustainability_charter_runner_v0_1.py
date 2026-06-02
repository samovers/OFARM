#!/usr/bin/env python3
from pathlib import Path
import json, sys
from datetime import datetime, timezone
from jsonschema import Draft202012Validator
ROOT = Path(__file__).resolve().parents[3]
FIXTURE_ROOT = Path(__file__).parent / 'fixtures'
HIGH_GOVERNANCE_ACTIONS={'CHARTER_APPROVE_EXCEPTION','CHARTER_ATTEST_SUSTAINABILITY_CLAIM','CHARTER_SET_OBJECTIVE_PRIORITY','CHARTER_ACTIVATE_POLICY_PACK','CHARTER_ACCEPT_BREACH_FINDING','CHARTER_RESOLVE_BREACH_FINDING','CHARTER_APPROVE_RISK_BUDGET','CHARTER_APPROVE_REGRET_BUDGET','CHARTER_APPROVE_TRADEOFF','CHARTER_APPROVE_CLAIM_BASIS'}
READY_STATES={'CLAIM_READY','ATTESTATION_READY','FILED'}
BAD_BLOCKING_RESULTS={'FAILED','BLOCKED','INSUFFICIENT_BASIS','REQUIRES_REVIEW'}
ALLOWING_DISPOSITIONS={'ALLOW','ALLOW_WITH_QUALIFICATION'}
BLOCKING_DISPOSITIONS={'REFUSE','REQUIRE_REVIEW','REQUIRE_HUMAN_APPROVAL','INSUFFICIENT_BASIS','BLOCKED','BLOCKED_BY_PACK_CONFLICT','BLOCKED_BY_AUTHORITY'}

def parse_ts(s):
    if not s: return None
    if s.endswith('Z'): s=s[:-1] + '+00:00'
    return datetime.fromisoformat(s)

def eval_record(r):
    t=r.get('type')
    if t=='PolicyEvaluation':
        if r.get('hardConstraintViolated'): return False
        if r.get('evaluationCompleteness') not in (None,'COMPLETE') and r.get('resultDisposition')=='ALLOW': return bool(r.get('lowConsequenceAdvisoryExceptionBasis'))
        return True
    if t=='ClaimBasis':
        if r.get('claimReadiness') in READY_STATES:
            if r.get('evidenceQualityState') in ['INSUFFICIENT','MISSING','STALE','INVALIDATED']: return False
            if r.get('currentStateReliance')=='UNKNOWN_BLOCKING': return False
            if r.get('currentStateReliance')=='RELIES_ON_CURRENT_STATE' and not r.get('materializationBasisRef'): return False
            if r.get('currentStateReliance')=='RELIES_ON_CURRENT_STATE' and r.get('currentStateNotUsedReason'): return False
            if r.get('currentStateReliance')=='RELIES_ON_CURRENT_STATE' and r.get('stalenessClass') in ['STALE_BLOCKING','INVALIDATED','UNKNOWN']: return False
            expected_disposition={'CLAIM_READY':'CLAIM_BEARING','ATTESTATION_READY':'ATTESTATION_CANDIDATE','FILED':'FILED_SUBMISSION'}.get(r.get('claimReadiness'))
            if expected_disposition and r.get('outputDisposition') != expected_disposition: return False
            if not r.get('evidenceSufficiencyCaseRef'): return False
        return True
    if t=='ApprovalAttempt': return not (r.get('actorType')=='SOFTWARE_AGENT' and r.get('actionClass') in HIGH_GOVERNANCE_ACTIONS)
    if t=='RegretBudget': return r.get('doesNotAuthorizeExperimentation') is True and r.get('doesNotAuthorizeExecution') is True and r.get('doesNotAuthorizeRobotMission') is True
    return False

def semantic_claim_basis(instance):
    readiness=instance.get('claimReadiness')
    reliance=instance.get('currentStateReliance')
    if readiness in READY_STATES:
        expected_disposition={'CLAIM_READY':'CLAIM_BEARING','ATTESTATION_READY':'ATTESTATION_CANDIDATE','FILED':'FILED_SUBMISSION'}[readiness]
        if instance.get('outputDisposition') != expected_disposition:
            return False, f'{readiness} requires outputDisposition={expected_disposition}'
        if reliance=='UNKNOWN_BLOCKING': return False, 'ready claim cannot have UNKNOWN_BLOCKING currentStateReliance'
        if reliance=='RELIES_ON_CURRENT_STATE':
            if not instance.get('materializationBasisRef'): return False, 'current-state reliance requires materializationBasisRef'
            if instance.get('currentStateNotUsedReason'): return False, 'currentStateNotUsedReason must be absent when currentStateReliance=RELIES_ON_CURRENT_STATE'
        if reliance=='DOES_NOT_RELY_ON_CURRENT_STATE' and not instance.get('currentStateNotUsedReason'):
            return False, 'non-current-state claim basis requires currentStateNotUsedReason'
    return True, None

def semantic_output_qualification(instance):
    allowed=set(instance.get('allowedUseClasses',[])); blocked=set(instance.get('blockedUseClasses',[])); posture=instance.get('dataSharingPosture')
    if allowed & blocked: return False, 'allowedUseClasses and blockedUseClasses overlap'
    if 'PARTNER_DISCLOSURE' in allowed:
        if posture!='PARTNER_DISCLOSURE_ALLOWED': return False, 'PARTNER_DISCLOSURE use requires PARTNER_DISCLOSURE_ALLOWED posture'
        if not (instance.get('sharingGrantRefs') or instance.get('publicAuthorityBasisRef')): return False, 'partner disclosure requires sharingGrantRefs or publicAuthorityBasisRef'
    if 'PUBLIC_DISCLOSURE' in allowed:
        if instance.get('advisoryOnly') is True: return False, 'advisory-only output cannot allow PUBLIC_DISCLOSURE by default in CP11'
        if posture!='PUBLIC_ALLOWED': return False, 'PUBLIC_DISCLOSURE use requires PUBLIC_ALLOWED posture'
        if not (instance.get('sharingGrantRefs') or instance.get('publicAuthorityBasisRef')): return False, 'public disclosure requires sharingGrantRefs or publicAuthorityBasisRef'
    if instance.get('advisoryOnly') is True and 'PUBLIC_DISCLOSURE' not in blocked:
        return False, 'advisory-only output must block PUBLIC_DISCLOSURE by default'
    if posture=='INTERNAL_ONLY' and (allowed & {'PARTNER_DISCLOSURE','PUBLIC_DISCLOSURE'}): return False, 'INTERNAL_ONLY posture cannot allow external disclosure'
    if instance.get('sharingGrantRefs') is not None and len(instance.get('sharingGrantRefs'))==0: return False, 'sharingGrantRefs cannot be empty when present'
    return True, None

def semantic_policy_trace(instance):
    disposition=instance.get('resultDisposition')
    result_sets={
        'constraintResults': instance.get('constraintResults',[]) or [],
        'objectiveResults': instance.get('objectiveResults',[]) or [],
        'tradeoffResults': instance.get('tradeoffResults',[]) or [],
        'evidenceResults': instance.get('evidenceResults',[]) or []
    }
    results=[]
    for arr, vals in result_sets.items():
        for res in vals:
            results.append((arr,res))
    # Hard sustainability constraints cannot fail and still permit ALLOW/ALLOW_WITH_QUALIFICATION,
    # even if an implementer tries to set blocking=false. Failed constraints are blocking by class.
    for arr,res in results:
        if arr=='constraintResults' and res.get('result') in {'FAILED','BLOCKED','INSUFFICIENT_BASIS'} and disposition in ALLOWING_DISPOSITIONS:
            return False, f'{disposition} cannot coexist with failed constraint result {res.get("result")} even when blocking=false'
    for arr,res in results:
        if res.get('blocking') is True and res.get('result') in BAD_BLOCKING_RESULTS:
            if disposition in ALLOWING_DISPOSITIONS:
                return False, f'{disposition} cannot coexist with blocking {res.get("result")} result'
            if disposition not in BLOCKING_DISPOSITIONS and disposition!='EMERGENCY_EXCEPTION_ONLY':
                return False, f'blocking result requires blocking/review disposition, got {disposition}'
    if instance.get('evaluationCompleteness')=='COMPLETE' and disposition in ALLOWING_DISPOSITIONS and not results and not instance.get('noApplicableRulesBasis'):
        return False, f'complete {disposition} with no typed results requires noApplicableRulesBasis'
    return True, None

def semantic_charter_exception(instance, semanticEvaluationTime=None):
    state=instance.get('exceptionState')
    valid_from=parse_ts(instance.get('validFrom'))
    expiry=instance.get('expiry') or {}
    expires_at=parse_ts(expiry.get('expiresAt'))
    review_by=parse_ts(expiry.get('requiredReviewBy'))
    if valid_from and expires_at and expires_at <= valid_from:
        return False, 'expiresAt must be after validFrom'
    if review_by and expires_at and review_by > expires_at:
        return False, 'requiredReviewBy must be on or before expiresAt'
    if state=='ACTIVE' and semanticEvaluationTime and expires_at:
        eval_at=parse_ts(semanticEvaluationTime)
        if eval_at and eval_at >= expires_at:
            return False, 'ACTIVE exception must not be expired at evaluation time'
    return True, None

def semantic_validate(schema_file, instance, semanticEvaluationTime=None):
    if schema_file.endswith('OFARM_SustainabilityClaimBasis_schema_v0_1.json'):
        return semantic_claim_basis(instance)
    if schema_file.endswith('OFARM_SustainabilityOutputQualification_schema_v0_1.json'):
        return semantic_output_qualification(instance)
    if schema_file.endswith('OFARM_SustainabilityPolicyEvaluationTrace_schema_v0_1.json'):
        return semantic_policy_trace(instance)
    if schema_file.endswith('OFARM_CharterException_schema_v0_1.json'):
        return semantic_charter_exception(instance, semanticEvaluationTime)
    return True, None

def schema_validate(rel, instance):
    schema=json.loads((ROOT/rel).read_text())
    Draft202012Validator.check_schema(schema)
    v=Draft202012Validator(schema)
    errors=sorted(v.iter_errors(instance), key=lambda e:list(e.path))
    return (not errors, [('/'.join(map(str,e.path)) or '<root>')+': '+e.message for e in errors[:10]])

def main():
    results=[]
    for d in sorted(FIXTURE_ROOT.iterdir()):
        if not d.is_dir(): continue
        inp=json.loads((d/'input'/'records.json').read_text())
        exp=json.loads((d/'expected'/'expected_result.json').read_text())['expectedPass']
        sem_results=[]; schema_results=[]; sem_ok=True; schema_ok=True
        for r in inp.get('records',[]):
            ok=eval_record(r); sem_results.append({'recordType':r.get('type'),'actualPass':ok}); sem_ok = sem_ok and ok
        for item in inp.get('schemaValidations',[]):
            ok, errs=schema_validate(item['schemaFile'], item['instance'])
            semantic_ok, semantic_err = semantic_validate(item['schemaFile'], item['instance'], item.get('semanticEvaluationTime'))
            schema_results.append({'schemaFile':item['schemaFile'],'actualSchemaValid':ok,'schemaErrors':errs,'actualSemanticValid':semantic_ok,'semanticError':semantic_err})
            schema_ok = schema_ok and ok and semantic_ok
        actual=sem_ok and schema_ok
        result={'fixtureId':d.name,'actualPass':actual,'expectedPass':exp,'conformanceFixturePassed':actual==exp,'semanticResults':sem_results,'schemaResults':schema_results}
        (d/'results'/'result.json').write_text(json.dumps(result,indent=2)+'\n')
        results.append(result)
    out={'runner':'ofarm_cp11_sustainability_charter_runner_v0_1_schema_aware_phase7_3','schemaAware':True,'semanticHardeningAware':True,'allFixturesPassed':all(r['conformanceFixturePassed'] for r in results),'fixtureCount':len(results),'positiveFixtureCount':sum(1 for r in results if r['expectedPass']),'negativeFixtureCount':sum(1 for r in results if not r['expectedPass']),'results':results}
    print(json.dumps(out,indent=2))
    (Path(__file__).parent/'CP11_sustainability_charter_conformance_results_v0_1.json').write_text(json.dumps(out,indent=2)+'\n')
    return 0 if out['allFixturesPassed'] else 1
if __name__=='__main__': raise SystemExit(main())
