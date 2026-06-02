#!/usr/bin/env python3
import json, sys, os
from pathlib import Path
from datetime import datetime, timezone
from jsonschema import Draft202012Validator

EVALUATION_TIME = datetime.fromisoformat('2026-06-01T12:00:00+00:00')
STRONG_FORBIDDEN = {
    'use:farm-truth','use:current-state','use:compliance-fact','use:mission-authority',
    'use:model-deployment','use:automatic-execution','use:unqualified-sustainability-claim',
    'FARM_TRUTH','CURRENT_STATE','COMPLIANCE_FACT','MISSION_AUTHORITY','MODEL_DEPLOYMENT',
    'AUTOMATIC_EXECUTION','UNQUALIFIED_SUSTAINABILITY_CLAIM'
}
BAD_POISON_DISPOSITIONS = {'BLOCK_USE','QUARANTINE','WITHDRAW','REQUIRE_HUMAN_REVIEW'}

def parse_dt(s):
    if not s: return None
    return datetime.fromisoformat(s.replace('Z','+00:00'))

def load_json(p):
    with open(p,'r') as f: return json.load(f)

def find_root(start):
    p = Path(start).resolve()
    for cand in [p] + list(p.parents):
        if (cand/'03_machine_contracts/drafts_non_default/farm_to_farm_intelligence_boundary').exists():
            return cand
    return Path.cwd()

def artifact_schema_name(schema):
    return schema.get('properties',{}).get('artifactType',{}).get('const')

def overlaps(a,b): return bool(set(a or []) & set(b or []))

def ref_map(records): return {r.get('artifactId'):r for r in records if 'artifactId' in r}

def by_type(records, t): return [r for r in records if r.get('artifactType') == t]

def fail(msg, errors): errors.append(msg)

def semantic_checks(records):
    errors=[]
    ids=ref_map(records)
    one=lambda t: by_type(records,t)[0] if by_type(records,t) else {}
    # no overlaps
    for r in records:
        if overlaps(r.get('allowedUseClasses'), r.get('prohibitedUseClasses')):
            fail(f"{r.get('artifactId')} allowedUseClasses/prohibitedUseClasses overlap", errors)
        if overlaps(r.get('allowedUseClasses'), r.get('blockedUseClasses')):
            fail(f"{r.get('artifactId')} allowedUseClasses/blockedUseClasses overlap", errors)
        if overlaps(r.get('usableForClasses'), r.get('blockedUseClasses')):
            fail(f"{r.get('artifactId')} usableForClasses/blockedUseClasses overlap", errors)
    # share grants
    for g in by_type(records,'FarmIntelligenceShareGrant'):
        vf,vu=parse_dt(g.get('validFrom')), parse_dt(g.get('validUntil'))
        if vf and vu and vu <= vf: fail(f"{g['artifactId']} invalid grant window", errors)
        if g.get('grantState') == 'ACTIVE':
            if not g.get('approvalDecisionRef') and not g.get('authorityDecisionTraceRef'): fail(f"{g['artifactId']} active grant lacks approval/authority", errors)
            if vu and vu < EVALUATION_TIME: fail(f"{g['artifactId']} active grant expired at evaluation time", errors)
        if g.get('grantState') in {'REVOKED','EXPIRED','DENIED','SUSPENDED'}:
            # If any package/contribution/receipt uses it, fail
            for r in records:
                uses = []
                for key in ('shareGrantRef','shareGrantRefs','grantCoverageRef'):
                    v=r.get(key)
                    if isinstance(v,list): uses += v
                    elif isinstance(v,str): uses.append(v)
                if g.get('artifactId') in uses:
                    fail(f"{r.get('artifactId')} uses non-active grant {g.get('artifactId')}", errors)
    # Agent tool success cannot be authority
    for g in by_type(records,'FarmIntelligenceShareGrant'):
        if str(g.get('authorityDecisionTraceRef','')).startswith('tool:success') or str(g.get('approvalDecisionRef','')).startswith('tool:success'):
            fail(f"{g['artifactId']} uses tool success as grant authority", errors)
    # output qualifications
    for o in by_type(records,'IntelligenceOutputQualification'):
        allowed=set(o.get('allowedUseClasses',[])); blocked=set(o.get('blockedUseClasses',[]))
        if allowed & STRONG_FORBIDDEN:
            fail(f"{o['artifactId']} allows forbidden strong CP14 use {sorted(allowed & STRONG_FORBIDDEN)}", errors)
        needed={'use:farm-truth','use:current-state','use:compliance-fact','use:mission-authority','use:model-deployment','use:automatic-execution'}
        if not needed.issubset(blocked): fail(f"{o['artifactId']} missing default blocked strong uses", errors)
        # High re-id risk output disclosure
        risk=ids.get(o.get('reidentificationRiskAssessmentRef'))
        if risk and risk.get('riskClass') in {'HIGH','UNKNOWN_BLOCKING'}:
            if 'use:public-disclosure' in allowed or o.get('disclosureClass') == 'PUBLIC':
                fail(f"{o['artifactId']} public disclosure with high/unknown reidentification risk", errors)
            if ('use:partner-disclosure' in allowed or o.get('disclosureClass') == 'PARTNER') and not risk.get('reviewDecisionRef'):
                fail(f"{o['artifactId']} partner disclosure high risk without review", errors)
    # regional alert published
    for a in by_type(records,'RegionalAlert'):
        if a.get('alertState') == 'PUBLISHED':
            if not a.get('outputQualificationRef'): fail(f"{a['artifactId']} published without output qualification", errors)
            if not a.get('riskSignalRefs'): fail(f"{a['artifactId']} published without risk signals", errors)
            if not a.get('applicabilityAssessmentRef'): fail(f"{a['artifactId']} published without applicability assessment", errors)
            oq=ids.get(a.get('outputQualificationRef'))
            if oq and ('use:farm-truth' in oq.get('allowedUseClasses',[]) or 'FARM_TRUTH' in oq.get('allowedUseClasses',[])):
                fail(f"{a['artifactId']} regional alert used as farm truth", errors)
    # benchmark
    for b in by_type(records,'BenchmarkDelta'):
        if b.get('benchmarkState') == 'PUBLISHED_ADVISORY':
            if not b.get('outputQualificationRef'): fail(f"{b['artifactId']} published benchmark without output qualification", errors)
            floor=ids.get(b.get('aggregationFloorRef'))
            if not floor: fail(f"{b['artifactId']} benchmark without aggregation floor record", errors)
            else:
                if b.get('publicDisclosureIntended') and (floor.get('minimumSourceFarmCount',0) < 5 or floor.get('minimumDistinctOperatorCount',0) < 3 or floor.get('minimumSpatialSeparationClass') == 'NONE'):
                    fail(f"{b['artifactId']} public benchmark with weak aggregation floor", errors)
            risk=ids.get(b.get('reidentificationRiskAssessmentRef')) or ids.get(ids.get(b.get('deidentificationClaimRef'),{}).get('reidentificationRiskAssessmentRef'))
            if b.get('publicDisclosureIntended') and risk and risk.get('riskClass') in {'HIGH','UNKNOWN_BLOCKING'}:
                fail(f"{b['artifactId']} public benchmark high re-id risk", errors)
    # aggregation floor
    for af in by_type(records,'AggregationFloor'):
        if af.get('aggregationDoesNotEqualAnonymisation') is not True:
            fail(f"{af['artifactId']} aggregation incorrectly implies anonymisation", errors)
    # anonymisation / deidentification
    for ac in by_type(records,'AnonymisationClaim'):
        if ac.get('claimState') == 'APPROVED':
            if not ac.get('approvalDecisionRef'): fail(f"{ac['artifactId']} approved anonymisation without approval", errors)
            if not ac.get('reidentificationRiskAssessmentRef'): fail(f"{ac['artifactId']} approved anonymisation without risk assessment", errors)
            if ac.get('residualRiskClass') not in {'VERY_LOW','LOW'}: fail(f"{ac['artifactId']} approved anonymisation with high/moderate/unknown risk", errors)
            if ac.get('methodClass') == 'OTHER' and not ac.get('reviewDecisionRef'): fail(f"{ac['artifactId']} approved anonymisation OTHER without review", errors)
    for dc in by_type(records,'DeidentificationClaim'):
        if dc.get('claimState') in {'CLAIMED','REVIEWED'}:
            if not dc.get('reidentificationRiskAssessmentRef'): fail(f"{dc['artifactId']} deidentification without risk assessment", errors)
            if not dc.get('claimBasisRefs'): fail(f"{dc['artifactId']} deidentification without basis", errors)
    # revocation propagation
    for rv in by_type(records,'RevocationPropagationTrace'):
        if rv.get('revocationState') == 'COMPLETE':
            if not rv.get('propagationCompletedAt'): fail(f"{rv['artifactId']} complete revocation without completion time", errors)
            if rv.get('unresolvedRecipientRefs'): fail(f"{rv['artifactId']} complete revocation with unresolved recipients", errors)
        if rv.get('revocationState') == 'PARTIAL' and not rv.get('unresolvedRecipientRefs'):
            fail(f"{rv['artifactId']} partial revocation without unresolved recipients", errors)
        if rv.get('revocationState') == 'FAILED' and not rv.get('failureReasonRefs'):
            fail(f"{rv['artifactId']} failed revocation without failure reasons", errors)
    # Learning artifact / farm memory boundary
    for lp in by_type(records,'LearningArtifactSharePackage'):
        if lp.get('farmMemoryEntryRefs'):
            if not lp.get('farmMemoryDerivativeSharingExplicitlyPermitted'): fail(f"{lp['artifactId']} farm memory derivative share not explicitly permitted", errors)
            if not lp.get('recipientFarmMemoryCreationBlocked'): fail(f"{lp['artifactId']} recipient farm memory creation not blocked", errors)
            if not lp.get('crossFarmApplicabilityAssessmentRef'): fail(f"{lp['artifactId']} farm memory share lacks applicability assessment", errors)
            grant=ids.get(lp.get('shareGrantRef'))
            if grant and not any('farm-memory-derivative' in x or x == 'FARM_MEMORY_DERIVATIVE' for x in grant.get('allowedUseClasses',[])):
                fail(f"{lp['artifactId']} grant lacks farm-memory-derivative permission", errors)
    # CP11/CP12 signal qualifications
    for c in by_type(records,'FarmIntelligenceContribution'):
        if c.get('contributionClass') == 'CP11_SUSTAINABILITY_SIGNAL' or c.get('containsSustainabilityClaim'):
            if not c.get('cp11QualificationRefs'): fail(f"{c['artifactId']} sustainability signal lacks CP11 qualification", errors)
            oq=ids.get(c.get('outputQualificationRef'))
            if oq and any('certification' in x or 'compliance-fact' in x for x in oq.get('allowedUseClasses',[])):
                fail(f"{c['artifactId']} sustainability signal claims certification/compliance use", errors)
        if c.get('contributionClass') in {'CP12_MISSION_SIGNAL','CP12_INCIDENT_SIGNAL'} or c.get('containsMissionOrIncidentSignal'):
            if not c.get('cp12QualificationRefs'): fail(f"{c['artifactId']} mission/incident signal lacks CP12 qualification", errors)
            oq=ids.get(c.get('outputQualificationRef'))
            if oq and any(x in oq.get('allowedUseClasses',[]) for x in ['use:compliance-fact','use:liability-determination','COMPLIANCE_FACT']):
                fail(f"{c['artifactId']} mission/incident signal allows compliance/liability fact", errors)
    # Federated learning / training use
    for fc in by_type(records,'FederatedLearningContribution'):
        if fc.get('contributionState') in {'SUBMITTED','ACCEPTED_BY_AGGREGATOR'}:
            if not ids.get(fc.get('shareGrantRef')) or ids.get(fc.get('shareGrantRef'),{}).get('grantState') != 'ACTIVE': fail(f"{fc['artifactId']} lacks active share grant", errors)
            tb=ids.get(fc.get('trainingUsePolicyBindingRef'))
            if not tb or tb.get('bindingState') != 'ACTIVE' or not tb.get('trainingUseAllowed'): fail(f"{fc['artifactId']} lacks active training-use policy", errors)
            if fc.get('privacyMechanismClass') == 'NONE_DECLARED' and not fc.get('privacyReviewApprovalRef'): fail(f"{fc['artifactId']} accepted/submitted without privacy mechanism or approval", errors)
            if not fc.get('qualityAssessmentRef'): fail(f"{fc['artifactId']} lacks quality assessment", errors)
            if fc.get('contributionState') == 'ACCEPTED_BY_AGGREGATOR' and not fc.get('poisoningOrAnomalyReviewRef'): fail(f"{fc['artifactId']} accepted without poisoning/anomaly review", errors)
        if fc.get('doesNotAuthorizeModelDeployment') is not True or fc.get('cp15RequiredForDeployment') is not True: fail(f"{fc['artifactId']} tries to authorize deployment", errors)
    for tb in by_type(records,'TrainingUsePolicyBinding'):
        if tb.get('trainingUseAllowed'):
            if not tb.get('allowedTrainingPurposeClasses') or not tb.get('recipientPartyRefs') or not tb.get('targetModelFamilyRefs'):
                fail(f"{tb['artifactId']} training allowed without purpose/recipient/model", errors)
            if tb.get('trainingUseReceiptRequired') is not True: fail(f"{tb['artifactId']} training allowed without receipt requirement", errors)
            if not tb.get('retentionPolicyRef') or not tb.get('revocationPolicyRef'): fail(f"{tb['artifactId']} training allowed without retention/revocation policy", errors)
    for tr in by_type(records,'TrainingUseReceipt'):
        if tr.get('receiptState') == 'CONFIRMED' and tr.get('usedForTraining'):
            if tr.get('policyCompliant') is not True: fail(f"{tr['artifactId']} confirmed training use not policy compliant", errors)
            if not tr.get('trainingUsePolicyBindingRef'): fail(f"{tr['artifactId']} training use lacks policy binding", errors)
    # Model improvement signals
    for ms in by_type(records,'ModelImprovementSignal'):
        if ms.get('doesNotAuthorizeDeployment') is not True or ms.get('cp15RequiredForDeployment') is not True:
            fail(f"{ms['artifactId']} model signal authorizes deployment", errors)
        if ms.get('confidenceClass') == 'HIGH':
            if not (ms.get('federatedAggregationReceiptRef') or ms.get('basisRefs')): fail(f"{ms['artifactId']} high-confidence model signal lacks aggregation/basis", errors)
            if not ms.get('qualityAssessmentRef'): fail(f"{ms['artifactId']} high-confidence model signal lacks quality basis", errors)
            if not ms.get('poisoningOrAnomalyReviewRef'): fail(f"{ms['artifactId']} high-confidence model signal lacks anomaly review", errors)
    # Poisoning/anomaly downstream blocks
    bad_targets=set()
    for pr in by_type(records,'PoisoningOrAnomalyReview'):
        if pr.get('reviewDisposition') in BAD_POISON_DISPOSITIONS:
            bad_targets.update(pr.get('targetRefs',[]))
    if bad_targets:
        # any alert/benchmark/fed/model improvement using the target should fail
        for a in by_type(records,'RegionalAlert'):
            if a.get('contributionPackageRefs'): fail(f"{a['artifactId']} uses contribution under poisoning/anomaly block", errors)
        for b in by_type(records,'BenchmarkDelta'):
            if b.get('benchmarkState') == 'PUBLISHED_ADVISORY': fail(f"{b['artifactId']} benchmark uses contribution under poisoning/anomaly block", errors)
        for fc in by_type(records,'FederatedLearningContribution'):
            if fc.get('artifactId') in bad_targets and fc.get('contributionState') in {'SUBMITTED','ACCEPTED_BY_AGGREGATOR'}: fail(f"{fc['artifactId']} federated contribution blocked by poisoning/anomaly review", errors)
    # Cross-farm applicability for local use
    for oq in by_type(records,'IntelligenceOutputQualification'):
        if any(x in oq.get('allowedUseClasses',[]) for x in ['use:local-recommendation','use:local-action','use:cp13-farm-memory-candidate']):
            if not oq.get('localApplicabilityRequiredBeforeAction'): fail(f"{oq['artifactId']} local use without applicability flag", errors)
            if not any(r.get('artifactType') == 'CrossFarmApplicabilityAssessment' for r in records): fail(f"{oq['artifactId']} local use without applicability assessment record", errors)
    # Redisclosure posture
    for rc in by_type(records,'RecipientUseConstraint'):
        if rc.get('redisclosurePosture') == 'ALLOWED':
            fail(f"{rc['artifactId']} redisclosure allowed without explicit CP14 permission", errors)
    return errors

def main():
    root = find_root(__file__)
    schema_dir = root/'03_machine_contracts/drafts_non_default/farm_to_farm_intelligence_boundary'
    fixture_dir = Path(__file__).parent/'fixtures'
    schemas={}
    validators={}
    schema_errors=[]
    for sp in schema_dir.glob('*.json'):
        s=load_json(sp)
        art=s.get('properties',{}).get('artifactType',{}).get('const')
        if art:
            schemas[art]=s
            try: Draft202012Validator.check_schema(s)
            except Exception as e: schema_errors.append(f"{sp.name}: {e}")
            validators[art]=Draft202012Validator(s)
    results=[]
    for fp in sorted(fixture_dir.glob('*.json')):
        f=load_json(fp)
        errors=[]
        for r in f.get('records',[]):
            art=r.get('artifactType')
            v=validators.get(art)
            if not v:
                errors.append(f"no schema for {art}")
            else:
                for e in v.iter_errors(r): errors.append(f"schema {r.get('artifactId')}: {e.message} at {list(e.path)}")
        errors += semantic_checks(f.get('records',[]))
        passed = not errors
        expected = f.get('expectedPass') is True
        ok = (passed == expected)
        results.append({'fixtureId':f.get('fixtureId'), 'expectedPass':expected, 'actualPass':passed, 'passed':ok, 'errors':errors[:20]})
    summary={
        'schemaAware': True,
        'semanticHardeningAware': True,
        'crossRecordAware': True,
        'schemaCount': len(schemas),
        'schemaErrors': schema_errors,
        'fixtureCount': len(results),
        'positiveFixtureCount': sum(1 for r in results if r['expectedPass']),
        'negativeFixtureCount': sum(1 for r in results if not r['expectedPass']),
        'allFixturesPassed': all(r['passed'] for r in results) and not schema_errors,
        'results': results,
    }
    out = Path(__file__).parent/'CP14_PHASE6_1_CONFORMANCE_RESULTS.json'
    with open(out,'w') as f: json.dump(summary,f,indent=2)
    print(json.dumps({k:v for k,v in summary.items() if k!='results'}, indent=2))
    if not summary['allFixturesPassed']:
        for r in results:
            if not r['passed']:
                print('FAILED', r['fixtureId'], 'expected',r['expectedPass'],'actual',r['actualPass'], r['errors'][:5])
        sys.exit(1)

if __name__ == '__main__': main()
