#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[6]
CP9 = Path(__file__).resolve().parents[1]
REQ_CHIPS = {
    'ADVISORY_OR_COMPLIANCE_SCOPE',
    'FRESHNESS_STATUS',
    'EVIDENCE_STATUS',
    'PERMISSION_STATUS',
    'APPROVAL_STATUS',
    'LAST_HUMAN_VERIFIED_STEP',
}
REQ_DISPUTE_KEYS = {
    'timeOrdered',
    'showsWhatSystemKnew',
    'showsWhatSystemAssumed',
    'showsWhatSystemAskedFor',
    'showsWhatSystemSimulated',
    'showsWhatSystemWasAllowedToSee',
    'showsWhatSystemWasNotAllowedToShare',
    'showsGateOrApprovalChanges',
    'governingPackRefsVisible',
    'freshnessSnapshotVisible',
}
READINESS_CLAIMS = [
    'farmerUxReadinessClaimed',
    'productionReadinessClaimed',
    'autonomousComplianceDecisioningClaimed',
    'legalAdviceClaimed',
    'externalStandardReadinessClaimed',
]

def load(rel: str):
    return json.loads((CP9/rel).read_text(encoding='utf-8'))

def scenario_violations(rec: dict) -> list[str]:
    v=[]
    sid=rec.get('scenarioId','<missing>')
    surface=rec.get('farmerSurface',{})
    if surface.get('qualificationBeforeContent') is not True:
        v.append('qualification_after_content')
    chips=set(surface.get('alwaysVisibleQualificationChips',[]))
    missing=sorted(REQ_CHIPS-chips)
    if missing:
        v.append('missing_required_qualification_chips:' + ','.join(missing))
    rq=rec.get('requestLayer',{})
    if rq.get('requestsAreEvidence') is not False:
        v.append('request_treated_as_evidence')
    if rq.get('requestsAreObligations') is not False:
        v.append('request_treated_as_obligation')
    if rq.get('requestsAreBlockersByThemselves') is not False:
        v.append('request_treated_as_blocker_by_itself')
    for key,name in [('deduplicationApplied','request_dedupe_missing'),('burdenVisible','request_burden_hidden'),('relevanceWindowVisible','request_relevance_hidden'),('whyItMattersVisible','request_why_hidden')]:
        if rq.get(key) is not True:
            v.append(name)
    off=rec.get('offlineAndSync',{})
    if off.get('localCapturesLabeledCapturedLocallyNotAccepted') is not True:
        v.append('offline_capture_labeled_accepted')
    if off.get('shareRequiresFreshPolicyRecheckAfterSync') is not True:
        v.append('missing_post_sync_share_recheck')
    share=rec.get('sharingAndSovereignty',{})
    if share.get('permissionLimitsVisible') is not True:
        v.append('permission_limits_hidden')
    if share.get('redactionAppliedToSummaryAndDetail') is not True:
        v.append('redaction_not_applied_to_summary')
    if share.get('revocationRecheckedBeforeShare') is not True:
        v.append('revocation_not_rechecked_before_share')
    wm=rec.get('worldModelBoundary',{})
    if wm.get('advisoryOnlyDisplayed') is not True or wm.get('worldModelStateNotCurrentState') is not True:
        v.append('world_model_laundered_to_current_fact')
    if wm.get('uncertaintyVisible') is not True:
        v.append('world_model_uncertainty_hidden')
    disp=rec.get('disputeTimeline',{})
    if any(disp.get(k) is not True for k in REQ_DISPUTE_KEYS):
        v.append('dispute_timeline_incomplete')
    claims=rec.get('claims',{})
    for key in READINESS_CLAIMS:
        if claims.get(key) is not False:
            v.append('premature_readiness_claim')
            break
    return v

def main() -> int:
    failures=[]
    bundle=load('examples/positive/OFARM_CP9_farmer_value_scenario_bundle_v0_1.json')
    scenarios=bundle.get('scenarios',[])
    if len(scenarios) != 11:
        failures.append(f'expected 11 positive scenarios, found {len(scenarios)}')
    positive_failures=[]
    for rec in scenarios:
        violations=scenario_violations(rec)
        if violations:
            positive_failures.append({'scenarioId':rec.get('scenarioId'), 'violations':violations})
    failures.extend([f"positive scenario failed: {x['scenarioId']} {x['violations']}" for x in positive_failures])
    # scenario-specific daily brief sections
    daily=[s for s in scenarios if s.get('scenarioFamily')=='daily_farm_command_brief']
    if not daily:
        failures.append('missing daily farm command brief scenario')
    else:
        sections=daily[0].get('dailyBriefSections',{})
        for k in ['knownFacts','staleFacts','advisoryPredictions','missingEvidence','requiredApprovals','disputesOrCorrections']:
            if not sections.get(k):
                failures.append(f'daily brief missing {k}')
    neg=load('examples/negative_policy_examples/OFARM_CP9_negative_farmer_ux_policy_examples_v0_1.json')
    detected=[]
    undetected=[]
    for case in neg.get('cases',[]):
        violations=scenario_violations(case.get('record',{}))
        if violations:
            detected.append({'caseId':case.get('caseId'), 'violations':violations})
        else:
            undetected.append(case.get('caseId'))
    if undetected:
        failures.append('negative cases not detected: ' + ','.join(undetected))
    # Snapshot checks
    snaps=load('examples/display_snapshots/OFARM_CP9_farmer_display_snapshots_v0_1.json').get('snapshots',[])
    if len(snaps) < 3:
        failures.append('expected at least 3 display snapshots')
    for snap in snaps:
        if not snap.get('oneLineQualification') or not snap.get('visibleChips'):
            failures.append(f'display snapshot incomplete: {snap.get("snapshotId")}')
    result={
        'schemaVersion':'ofarm.cp9.validationResult.v0.1',
        'phase':'AAI-CP9',
        'status':'PASS' if not failures else 'FAIL',
        'scope':'synthetic farmer-value UX scenario conformance only; not live farmer validation, production readiness, or legal/compliance advice',
        'positiveScenarioRecords':len(scenarios),
        'negativePolicyCases':len(neg.get('cases',[])),
        'detectedNegativePolicyCases':len(detected),
        'displaySnapshots':len(snaps),
        'failures':failures,
        'nonClaims':['not farmer UX readiness','not production readiness','not live pilot evidence','not autonomous compliance decisioning','not legal advice','not external-standard readiness'],
        'detectedNegativeCaseDetails':detected
    }
    print(json.dumps(result, indent=2))
    return 0 if not failures else 1

if __name__ == '__main__':
    raise SystemExit(main())
