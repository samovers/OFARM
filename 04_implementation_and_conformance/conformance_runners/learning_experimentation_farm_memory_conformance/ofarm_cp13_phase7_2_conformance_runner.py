#!/usr/bin/env python3
import json, sys, pathlib
from datetime import datetime, timezone
from jsonschema import Draft202012Validator

BASE = pathlib.Path(__file__).resolve().parent
SCHEMA_DIR = BASE.parents[2] / '03_machine_contracts' / 'drafts_non_default' / 'learning_experimentation_farm_memory'
FIXTURE_DIR = BASE / 'fixtures'
EVAL_TIME = datetime.fromisoformat('2026-05-29T08:00:00+00:00')
HARD_CHECKS = {'DESIGN','EVIDENCE','MISSINGNESS','CP11_CHARTER','CP12_EVIDENCE','CAUSAL_IDENTIFICATION','UNCERTAINTY','AUTHORITY','SCOPE','DATA_SOVEREIGNTY','OUTPUT_QUALIFICATION'}
PROMOTION_REQUIRED_CHECKS = {'DESIGN','EVIDENCE','MISSINGNESS','CAUSAL_IDENTIFICATION','UNCERTAINTY','AUTHORITY','SCOPE','OUTPUT_QUALIFICATION'}
BAD_RESULTS = {'FAIL','BLOCKED','INSUFFICIENT_BASIS','REQUIRE_REVIEW','REQUIRE_HUMAN_APPROVAL'}
FAILED_OR_BLOCKED_CP12 = {'FAILED','BLOCKED','REFUSE','UNKNOWN'}
SUFFICIENT_STATES = {'SUFFICIENT_FOR_ADVISORY','SUFFICIENT_FOR_FARM_MEMORY_CANDIDATE','SUFFICIENT_FOR_CLAIM_SUPPORT_CANDIDATE'}
FARM_MEMORY_OR_CLAIM_SUFFICIENT = {'SUFFICIENT_FOR_FARM_MEMORY_CANDIDATE','SUFFICIENT_FOR_CLAIM_SUPPORT_CANDIDATE'}
STRONG_EVIDENCE_FOR_CAUSAL = {'SUFFICIENT_FOR_FARM_MEMORY_CANDIDATE','SUFFICIENT_FOR_CLAIM_SUPPORT_CANDIDATE'}
DEFAULT_MEMORY_RETRIEVAL_BLOCKS = {'CURRENT_STATE','COMPLIANCE_FACT','AUTOMATIC_EXECUTION','MISSION_DISPATCH','CLAIM_BEARING_OUTPUT','MODEL_DEPLOYMENT','CROSS_FARM_SHARING'}

def parse_dt(s):
    return datetime.fromisoformat(s.replace('Z','+00:00'))

def load_schemas():
    schemas={}
    for p in SCHEMA_DIR.glob('OFARM_*_schema_v0_1*.json'):
        data=json.loads(p.read_text())
        typ=data['properties']['artifactType']['const']
        schemas[typ]=Draft202012Validator(data)
    return schemas

def hard_check_failure(trace):
    for c in trace.get('checkResults',[]):
        if c.get('checkClass') in HARD_CHECKS and c.get('result') in BAD_RESULTS:
            return True
    return False

def check_coverage(trace, required):
    present={c.get('checkClass') for c in trace.get('checkResults',[]) if c.get('checkClass')}
    return required - present

def not_applicable_without_basis(trace):
    return [c.get('checkClass') for c in trace.get('checkResults',[]) if c.get('checkClass') in HARD_CHECKS and c.get('result')=='NOT_APPLICABLE' and not c.get('basisRef')]

def trace_supports_promotion(trace):
    return trace and trace.get('evaluationCompleteness')=='COMPLETE' and trace.get('overallDisposition')=='PROMOTION_CANDIDATE' and not hard_check_failure(trace) and not not_applicable_without_basis(trace)

def trace_blocked_or_failed(trace):
    if not trace: return True
    if trace.get('evaluationCompleteness') in {'AUTHORITY_BLOCKED','CHARTER_BLOCKED','MISSION_BLOCKED','INSUFFICIENT_EVIDENCE','INSUFFICIENT_DESIGN'}:
        return True
    if trace.get('overallDisposition') in {'REFUSE','BLOCKED','REQUIRE_MORE_EVIDENCE'}:
        return True
    if hard_check_failure(trace): return True
    return False

def typed_cp12_items(bundle):
    return bundle.get('cp12EvidenceRefs',[]) or []

def typed_cp11_items(bundle):
    return bundle.get('cp11TraceRefs',[]) or []

def semantic_errors(records):
    errs=[]
    by_type={}
    by_id={}
    for r in records:
        by_type.setdefault(r.get('artifactType'), []).append(r)
        if r.get('artifactId'): by_id[r['artifactId']]=r

    # LearningScope temporal coherence and active horizon.
    for r in by_type.get('LearningScope',[]):
        ts=r.get('temporalScope',{})
        if ts.get('validFrom') and ts.get('validUntil'):
            if parse_dt(ts['validUntil']) <= parse_dt(ts['validFrom']):
                errs.append(f"{r['artifactId']}: temporalScope validUntil not after validFrom")
            if r.get('learningScopeState')=='ACTIVE' and parse_dt(ts['validUntil']) <= EVAL_TIME:
                errs.append(f"{r['artifactId']}: ACTIVE learning scope expired at evaluation time")

    # LearningEvaluationTrace hard check consistency and promotion-candidate coverage.
    for r in by_type.get('LearningEvaluationTrace',[]):
        disp=r.get('overallDisposition')
        if disp in {'ALLOW_ADVISORY','PROMOTION_CANDIDATE'}:
            for c in r.get('checkResults',[]):
                if c.get('checkClass') in HARD_CHECKS and c.get('result') in BAD_RESULTS:
                    errs.append(f"{r['artifactId']}: {disp} with failed hard check {c.get('checkClass')}={c.get('result')}")
        if disp=='PROMOTION_CANDIDATE':
            if r.get('evaluationCompleteness')!='COMPLETE':
                errs.append(f"{r['artifactId']}: promotion candidate without COMPLETE evaluation")
            missing=check_coverage(r, PROMOTION_REQUIRED_CHECKS)
            if missing:
                errs.append(f"{r['artifactId']}: promotion candidate missing hard-check coverage {sorted(missing)}")
            na=not_applicable_without_basis(r)
            if na:
                errs.append(f"{r['artifactId']}: promotion candidate has NOT_APPLICABLE hard checks without basis {sorted(na)}")
            used_cp12=False; used_cp11=False
            for ref in r.get('evidenceBundleRefs',[]):
                b=by_id.get(ref)
                if b and typed_cp12_items(b): used_cp12=True
                if b and typed_cp11_items(b): used_cp11=True
                if b and b.get('evidenceSufficiencyState') in {'INSUFFICIENT','UNKNOWN','INSUFFICIENT_FOR_FARM_MEMORY','INSUFFICIENT_FOR_CLAIM_SUPPORT'}:
                    errs.append(f"{r['artifactId']}: promotion candidate references insufficient evidence bundle {ref}")
            if used_cp12 and 'CP12_EVIDENCE' not in {c.get('checkClass') for c in r.get('checkResults',[])}:
                errs.append(f"{r['artifactId']}: promotion candidate uses CP12 evidence without CP12_EVIDENCE check or non-applicability basis")
            if used_cp11 and 'CP11_CHARTER' not in {c.get('checkClass') for c in r.get('checkResults',[])}:
                errs.append(f"{r['artifactId']}: promotion candidate uses CP11 traces without CP11_CHARTER check or non-applicability basis")

    # CausalEstimate semantic safety and cross-record support.
    for r in by_type.get('CausalEstimate',[]):
        trace=by_id.get(r.get('learningEvaluationTraceRef'))
        evidence=by_id.get(r.get('evidenceBundleRef')) if r.get('evidenceBundleRef') else None
        trial=by_id.get(r.get('trialDesignRef')) if r.get('trialDesignRef') else None
        if r.get('estimateMethod')=='INSUFFICIENT_FOR_ESTIMATE':
            if r.get('confidenceClass')!='INSUFFICIENT': errs.append(f"{r['artifactId']}: insufficient method with non-insufficient confidence")
            if r.get('effectDirection')!='UNKNOWN': errs.append(f"{r['artifactId']}: insufficient method with directional effect")
            if 'effectSize' in r: errs.append(f"{r['artifactId']}: insufficient method with effectSize")
        if r.get('confidenceClass')=='HIGH':
            if r.get('estimateMethod') in {'EXPLORATORY_ASSOCIATION','EXPERT_INTERPRETATION','INSUFFICIENT_FOR_ESTIMATE'}:
                errs.append(f"{r['artifactId']}: high confidence with weak method {r.get('estimateMethod')}")
            if r.get('biasRiskClass') in {'HIGH','UNKNOWN'}:
                errs.append(f"{r['artifactId']}: high confidence with bias risk {r.get('biasRiskClass')}")
            if r.get('missingnessImpactClass') in {'BLOCKING','UNKNOWN'}:
                errs.append(f"{r['artifactId']}: high confidence with missingness impact {r.get('missingnessImpactClass')}")
            if not trace or trace.get('evaluationCompleteness')!='COMPLETE' or trace_blocked_or_failed(trace):
                errs.append(f"{r['artifactId']}: high confidence estimate without complete supporting evaluation trace")
            if evidence and evidence.get('evidenceSufficiencyState') not in STRONG_EVIDENCE_FOR_CAUSAL:
                errs.append(f"{r['artifactId']}: high confidence estimate with insufficient evidence sufficiency {evidence.get('evidenceSufficiencyState')}")
            if r.get('estimateMethod')=='RANDOMIZED_TRIAL':
                if not trial or trial.get('preRegistered') is not True:
                    errs.append(f"{r['artifactId']}: high confidence randomized trial without preregistered trial design")
                if trial:
                    for ms_ref in trial.get('outcomeMeasureSpecRefs',[]):
                        ms=by_id.get(ms_ref)
                        if ms and ms.get('preRegistered') is not True:
                            errs.append(f"{r['artifactId']}: high confidence estimate uses non-preregistered outcome measure {ms_ref}")
        if r.get('confidenceClass')=='MODERATE':
            if r.get('estimateMethod')=='INSUFFICIENT_FOR_ESTIMATE':
                errs.append(f"{r['artifactId']}: moderate confidence with insufficient method")
            if trace and trace_blocked_or_failed(trace):
                errs.append(f"{r['artifactId']}: moderate confidence references failed/blocked trace")

    # LearningEvidenceBundle sufficiency/current-state/missingness/bias consistency and typed CP11/CP12 evidence items.
    for b in by_type.get('LearningEvidenceBundle',[]):
        suff=b.get('evidenceSufficiencyState')
        if b.get('currentStateReliance')=='UNKNOWN_BLOCKING' and suff in SUFFICIENT_STATES:
            errs.append(f"{b['artifactId']}: sufficient evidence with UNKNOWN_BLOCKING current-state reliance")
        if b.get('currentStateReliance')=='RELIES_ON_CURRENT_STATE':
            if not b.get('materializationBasisRefs'):
                errs.append(f"{b['artifactId']}: current-state reliance without materializationBasisRefs")
            if not b.get('freshnessQualificationRef'):
                errs.append(f"{b['artifactId']}: current-state reliance without freshnessQualificationRef")
        if b.get('missingnessSummary') in {'SEVERE','UNKNOWN'} and suff in FARM_MEMORY_OR_CLAIM_SUFFICIENT and not b.get('reviewDecisionRef'):
            errs.append(f"{b['artifactId']}: sufficient farm-memory/claim evidence with severe/unknown missingness and no review")
        if b.get('biasRiskState') in {'HIGH','UNKNOWN','DISPUTED'} and suff in FARM_MEMORY_OR_CLAIM_SUFFICIENT and not b.get('reviewDecisionRef'):
            errs.append(f"{b['artifactId']}: sufficient farm-memory/claim evidence with high/unknown/disputed bias and no review")
        for item in typed_cp12_items(b):
            if isinstance(item, str):
                errs.append(f"{b['artifactId']}: cp12EvidenceRefs must use typed evidence item objects")
                continue
            if item.get('evidenceClass')=='MISSION_EXECUTION_RECEIPT' and item.get('intendedStrength')=='STRONG' and not item.get('verificationRef'):
                errs.append(f"{b['artifactId']}: CP12 receipt used as strong evidence without verification")
            if item.get('traceDisposition') in FAILED_OR_BLOCKED_CP12 and item.get('intendedStrength') in {'MODERATE','STRONG'} and suff in FARM_MEMORY_OR_CLAIM_SUFFICIENT:
                errs.append(f"{b['artifactId']}: failed/blocking CP12 evidence used for sufficient farm-memory/claim evidence")
        for item in typed_cp11_items(b):
            if isinstance(item, str):
                errs.append(f"{b['artifactId']}: cp11TraceRefs must use typed trace item objects")
                continue
            if item.get('resultDisposition') not in {'ALLOW','ALLOW_WITH_QUALIFICATION','PASS'} and item.get('intendedStrength')=='SUFFICIENT':
                errs.append(f"{b['artifactId']}: failed CP11 trace used as sufficient basis")

    # Promotion temporal, state, disposition, and cross-record LearningEvaluationTrace support.
    for r in by_type.get('LearningPromotionDecision',[]):
        disp=r.get('promotionDisposition')
        trace=by_id.get(r.get('learningEvaluationTraceRef'))
        if disp=='PROMOTE_TO_FARM_MEMORY':
            if r.get('decisionState')!='APPROVED': errs.append(f"{r['artifactId']}: farm memory promotion not APPROVED")
            for f in ['farmMemoryEntryRef','reviewDecisionRef','authorityDecisionTraceRef','effectiveFrom','expiresAt']:
                if not r.get(f): errs.append(f"{r['artifactId']}: missing {f} for farm memory promotion")
            if r.get('effectiveFrom') and r.get('expiresAt'):
                if parse_dt(r['expiresAt']) <= parse_dt(r['effectiveFrom']):
                    errs.append(f"{r['artifactId']}: expiresAt not after effectiveFrom")
                if parse_dt(r['expiresAt']) <= EVAL_TIME:
                    errs.append(f"{r['artifactId']}: promotion decision expired at evaluation time")
            if not trace_supports_promotion(trace):
                errs.append(f"{r['artifactId']}: farm memory promotion without complete PROMOTION_CANDIDATE trace")
        if disp in {'DO_NOT_PROMOTE','REFUSE','REQUIRE_MORE_EVIDENCE'} and r.get('farmMemoryEntryRef'):
            errs.append(f"{r['artifactId']}: {disp} includes farmMemoryEntryRef")

    # FarmMemoryEntry cross-record with LearningPromotionDecision and temporal validity.
    for m in by_type.get('FarmMemoryEntry',[]):
        if m.get('sourceKind')=='AGENT_MEMORY': errs.append(f"{m['artifactId']}: agent memory submitted as farm memory")
        vh=m.get('validityHorizon',{})
        if vh.get('validFrom') and vh.get('validUntil'):
            if parse_dt(vh['validUntil']) <= parse_dt(vh['validFrom']):
                errs.append(f"{m['artifactId']}: validityHorizon validUntil not after validFrom")
            if m.get('memoryStatus') in {'ACTIVE_ADVISORY','ACTIVE_REVIEW_REQUIRED'} and parse_dt(vh['validUntil']) <= EVAL_TIME:
                errs.append(f"{m['artifactId']}: active farm memory expired at evaluation time")
        promo=by_id.get(m.get('learningPromotionDecisionRef'))
        status=m.get('memoryStatus')
        if status in {'ACTIVE_ADVISORY','ACTIVE_REVIEW_REQUIRED'}:
            if not promo:
                errs.append(f"{m['artifactId']}: active memory without promotion decision record")
            elif not (promo.get('decisionState')=='APPROVED' and promo.get('promotionDisposition')=='PROMOTE_TO_FARM_MEMORY' and promo.get('farmMemoryEntryRef')==m.get('artifactId') and promo.get('reviewDecisionRef') and promo.get('authorityDecisionTraceRef')):
                errs.append(f"{m['artifactId']}: active memory not supported by approved matching PROMOTE_TO_FARM_MEMORY decision")
            elif promo.get('expiresAt') and parse_dt(promo['expiresAt']) <= EVAL_TIME:
                errs.append(f"{m['artifactId']}: active memory supported by expired promotion decision")
        if status=='CANDIDATE' and promo and promo.get('promotionDisposition') not in {'PROMOTE_TO_FARM_MEMORY_CANDIDATE','PROMOTE_TO_FARM_MEMORY'}:
            errs.append(f"{m['artifactId']}: candidate memory unsupported by candidate/promotion decision")

    # FarmMemoryRetrievalQualification blocked-use minimums.
    for r in by_type.get('FarmMemoryRetrievalQualification',[]):
        blocked=set(r.get('blockedUseClasses',[]))
        if not blocked:
            errs.append(f"{r['artifactId']}: empty blockedUseClasses")
        missing=DEFAULT_MEMORY_RETRIEVAL_BLOCKS-blocked
        if missing:
            errs.append(f"{r['artifactId']}: missing default blocked uses {sorted(missing)}")
        if r.get('highConsequenceUse') and not r.get('reviewRequired'):
            errs.append(f"{r['artifactId']}: high consequence memory retrieval without reviewRequired")

    # LearningOutputQualification restrictions.
    prohibited_allowed={'CLAIM_BEARING_OUTPUT','MODEL_TRAINING','MODEL_DEPLOYMENT','CROSS_FARM_SHARING','FEDERATED_LEARNING','PUBLIC_DISCLOSURE','CURRENT_STATE','COMPLIANCE_FACT','MISSION_DISPATCH'}
    for r in by_type.get('LearningOutputQualification',[]):
        allowed=set(r.get('allowedUseClasses',[])); blocked=set(r.get('blockedUseClasses',[]))
        if allowed & blocked: errs.append(f"{r['artifactId']}: allowed/blocked overlap")
        if r.get('advisoryOnly') and not {'CANONICAL_TRUTH','CURRENT_STATE','COMPLIANCE_FACT','AUTOMATIC_EXECUTION','MISSION_DISPATCH','CLAIM_BEARING_OUTPUT','MODEL_DEPLOYMENT','CROSS_FARM_SHARING'}.issubset(blocked):
            errs.append(f"{r['artifactId']}: advisory output missing required blocked uses")
        if allowed & prohibited_allowed:
            errs.append(f"{r['artifactId']}: prohibited allowed-use class {sorted(allowed & prohibited_allowed)}")

    # OutcomeObservationSet missingness.
    for r in by_type.get('OutcomeObservationSet',[]):
        if r.get('missingnessState') in {'MATERIAL','UNKNOWN'} and r.get('evidenceQualityState')=='SUFFICIENT' and not (r.get('missingnessResolutionRef') or r.get('reviewDecisionRef')):
            errs.append(f"{r['artifactId']}: material/unknown missingness sufficient without review/resolution")
        if r.get('missingnessState')=='BLOCKING' and r.get('evidenceQualityState') not in {'INSUFFICIENT','UNKNOWN'}:
            errs.append(f"{r['artifactId']}: blocking missingness with too-strong evidence state")

    # ExperimentProtocol active approval/authority and charter-sensitive context.
    for r in by_type.get('ExperimentProtocol',[]):
        if r.get('protocolState')=='ACTIVE':
            if not r.get('approvalDecisionRef'):
                errs.append(f"{r['artifactId']}: active protocol without approvalDecisionRef")
            if not r.get('authorityDecisionTraceRef'):
                errs.append(f"{r['artifactId']}: active protocol without authorityDecisionTraceRef")
            if r.get('charterSensitive') and not r.get('charterEvaluationTraceRefs'):
                errs.append(f"{r['artifactId']}: charter-sensitive active protocol without charterEvaluationTraceRefs")
        if r.get('protocolState')=='COMPLETED' and not (r.get('completionEvidenceBundleRef') and r.get('completedAt')):
            errs.append(f"{r['artifactId']}: completed protocol without completion evidence/timestamp")
        if r.get('protocolState')=='PAUSED' and not (r.get('pauseReason') and r.get('resumeAuthorityRequirement')):
            errs.append(f"{r['artifactId']}: paused protocol without pause reason/resume authority")

    # ExperimentException temporal.
    for r in by_type.get('ExperimentException',[]):
        if r.get('validFrom') and r.get('validUntil'):
            if parse_dt(r['validUntil']) <= parse_dt(r['validFrom']): errs.append(f"{r['artifactId']}: validUntil not after validFrom")
            if r.get('exceptionState')=='ACTIVE' and parse_dt(r['validUntil']) <= EVAL_TIME: errs.append(f"{r['artifactId']}: active exception expired at evaluation time")

    # TrialDesign cross-record only for relevant observation sets.
    for trial in by_type.get('TrialDesign',[]):
        t=set(trial.get('treatmentUnitRefs',[])); c=set(trial.get('controlUnitRefs',[])); units=set(trial.get('experimentalUnitRefs',[])); arms=set(trial.get('treatmentArmRefs',[]))|set(trial.get('controlConditionRefs',[]))
        if t & c: errs.append(f"{trial['artifactId']}: treatment/control unit overlap")
        for a in trial.get('randomizationAssignments',[]):
            if a.get('unitRef') not in units: errs.append(f"{trial['artifactId']}: randomization assignment unit not in experimentalUnitRefs")
            if a.get('armRef') not in arms: errs.append(f"{trial['artifactId']}: randomization assignment arm not declared")
        for obs in by_type.get('OutcomeObservationSet',[]):
            if obs.get('learningScopeRef')==trial.get('learningScopeRef') and obs.get('outcomeMeasureSpecRef') in set(trial.get('outcomeMeasureSpecRefs',[])):
                if not units.issubset(set(obs.get('experimentalUnitRefs',[]))):
                    errs.append(f"{obs['artifactId']}: outcome observation missing required units from trial {trial['artifactId']}")

    # SeasonalLearningSummary claim support boundaries.
    for r in by_type.get('SeasonalLearningSummary',[]):
        if r.get('summaryDisposition')=='CLAIM_SUPPORT_CANDIDATE':
            for f in ['sustainabilityClaimBasisRefs','learningOutputQualificationRef','reviewDecisionRef']:
                if not r.get(f): errs.append(f"{r['artifactId']}: claim-support seasonal summary missing {f}")
    return errs

def main():
    schemas=load_schemas()
    results=[]; ok=True
    for p in sorted(FIXTURE_DIR.glob('*.json')):
        fx=json.loads(p.read_text())
        errors=[]
        for r in fx['records']:
            typ=r.get('artifactType')
            if typ in schemas and r.get('schemaVersion'):
                for e in schemas[typ].iter_errors(r):
                    errors.append(f"schema:{typ}:{'/'.join(map(str,e.path))}: {e.message}")
            elif typ not in schemas:
                errors.append(f"unknown artifactType {typ}")
        errors.extend(semantic_errors(fx['records']))
        passed=not errors
        expected=fx['expectedPass']
        if passed != expected: ok=False
        results.append({'fixtureName':fx['fixtureName'],'expectedPass':expected,'actualPass':passed,'errors':errors})
    report={'schemaAware':True,'semanticHardeningAware':True,'crossRecordAware':True,'temporalCausalEvidenceChainAware':True,'phase':'CP13 Phase 7.2 temporal causal evidence chain hardening','fixtureCount':len(results),'positiveFixtureCount':sum(1 for r in results if r['expectedPass']),'negativeFixtureCount':sum(1 for r in results if not r['expectedPass']),'allFixturesPassed':ok,'results':results}
    out=BASE/'CP13_phase7_2_conformance_results.json'
    out.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({k:report[k] for k in ['fixtureCount','positiveFixtureCount','negativeFixtureCount','allFixturesPassed']}, indent=2))
    return 0 if ok else 1
if __name__=='__main__': sys.exit(main())
