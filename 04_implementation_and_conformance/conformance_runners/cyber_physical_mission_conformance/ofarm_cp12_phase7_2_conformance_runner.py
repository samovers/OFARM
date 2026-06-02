#!/usr/bin/env python3
"""CP12 Phase 7.2 schema-aware cross-record conformance runner."""
import json, sys
from pathlib import Path
from datetime import datetime
from jsonschema import Draft202012Validator, FormatChecker
EVALUATION_TIME=datetime.fromisoformat('2026-05-28T12:00:00+00:00')
BAD_PREFLIGHT={"FAIL","BLOCKED","INSUFFICIENT_BASIS","REQUIRE_REVIEW","REQUIRE_HUMAN_APPROVAL"}
HARD_PREFLIGHT={"GEOMETRY","SAFETY","CP11_CHARTER","CURRENT_STATE","CAPABILITY","COMMAND_INTEGRITY","EMERGENCY_STOP","HUMAN_OVERRIDE","LOCAL_FALLBACK","EXECUTION_WINDOW","AUTHORITY"}
CRITICAL_SAFETY={"EMERGENCY_STOP_REQUIRED","HUMAN_OVERRIDE_REQUIRED","LOCAL_FALLBACK_REQUIRED","COMMAND_INTEGRITY_REQUIRED","GEOFENCE_REQUIRED","NO_GO_ZONE_REQUIRED"}
FORBIDDEN_OUTPUT={"CLAIM_BEARING_OUTPUT","ATTESTATION_CANDIDATE","FILED_SUBMISSION","DISPATCH_AUTHORITY","EXECUTION_TRUTH","COMPLIANCE_FACT"}
def parse_dt(v):
    if not v: return None
    return datetime.fromisoformat(v.replace('Z','+00:00'))
def after(a,b):
    da,db=parse_dt(a),parse_dt(b)
    if da is None or db is None: return True
    return da>db
def in_window(nb,na,vf,vu):
    nb,na,vf,vu=map(parse_dt,(nb,na,vf,vu))
    if not all([nb,na,vf,vu]): return True
    return nb>=vf and na<=vu and na>nb and vu>vf

def semantic_errors(r, records=None, by_id=None):
    records=records or []; by_id=by_id or {}
    t=r.get('contractType'); err=[]
    if t=='CyberPhysicalMissionEnvelope':
        state=r.get('missionLifecycleState')
        def req(fields):
            for f in fields:
                if not r.get(f): err.append(f'{state} requires {f}')
        if state=='COMMAND_PACKAGED': req(['missionDispatchAuthorizationRefs','commandEnvelopeRefs'])
        if state=='DISPATCHED': req(['missionDispatchAuthorizationRefs','commandEnvelopeRefs'])
        if state=='ACKNOWLEDGED': req(['missionDispatchAuthorizationRefs','commandEnvelopeRefs','commandAcknowledgementRefs'])
        if state=='IN_PROGRESS':
            req(['missionDispatchAuthorizationRefs','commandEnvelopeRefs'])
            if not (r.get('telemetryEnvelopeRefs') or r.get('executionReceiptRefs')): err.append('IN_PROGRESS requires telemetryEnvelopeRefs or executionReceiptRefs')
        if state=='COMPLETED_REPORTED': req(['missionDispatchAuthorizationRefs','commandEnvelopeRefs','executionReceiptRefs'])
        if state=='VERIFIED': req(['missionDispatchAuthorizationRefs','commandEnvelopeRefs','executionReceiptRefs','missionVerificationRefs'])
        if state=='CLOSED':
            if not (r.get('closureReviewDecisionRef') or r.get('missionVerificationRefs')): err.append('CLOSED requires closure review or verification')
        if state=='ABORTED':
            if not (r.get('abortEventRefs') or r.get('emergencyStopActivationRefs')): err.append('ABORTED requires abortEventRefs or emergencyStopActivationRefs')
            if r.get('abortedAfterDispatch') is True and not (r.get('missionDispatchAuthorizationRefs') and r.get('commandEnvelopeRefs')): err.append('post-dispatch abort must preserve dispatch/command refs')
    if t=='MissionPreflightTrace' and r.get('overallDisposition')=='PASS':
        seen={}
        for c in r.get('checkResults',[]):
            cls=c.get('checkClass'); res=c.get('result')
            if cls in HARD_PREFLIGHT: seen[cls]=c
            if cls in HARD_PREFLIGHT and res in BAD_PREFLIGHT:
                err.append(f"preflight PASS with hard bad check {cls}={res}")
            if c.get('blocking') and res in BAD_PREFLIGHT:
                err.append(f"preflight PASS with blocking bad check {cls}={res}")
            if res=='NOT_APPLICABLE' and not c.get('basisRef'):
                err.append(f"NOT_APPLICABLE check requires basisRef for {cls}")
        missing=sorted(HARD_PREFLIGHT-set(seen))
        if missing: err.append('preflight PASS missing hard checks: '+','.join(missing))
        for cls,c in seen.items():
            if c.get('result') not in ('PASS','NOT_APPLICABLE'):
                err.append(f'preflight hard check {cls} not pass/not-applicable')
    if t=='ExecutionWindow':
        if not after(r.get('notAfter'),r.get('notBefore')): err.append('ExecutionWindow.notAfter must be after notBefore')
        if r.get('preflightValidUntil') and not after(r.get('preflightValidUntil'),r.get('notBefore')): err.append('preflightValidUntil must be after notBefore')
    if t=='MissionDispatchAuthorization':
        if r.get('validFrom') and r.get('validUntil') and not after(r.get('validUntil'),r.get('validFrom')): err.append('MissionDispatchAuthorization.validUntil must be after validFrom')
        if r.get('cp11ApplicabilityState')=='UNKNOWN_BLOCKING' and r.get('authorizationState') in ('APPROVED','ACTIVE'): err.append('UNKNOWN_BLOCKING CP11 applicability cannot support approved/active dispatch')
        pf=by_id.get(r.get('missionPreflightTraceRef'))
        if pf and pf.get('overallDisposition')!='PASS': err.append('MissionDispatchAuthorization references non-PASS MissionPreflightTrace')
        for ref in r.get('capabilityCompatibilityResultRefs',[]) or []:
            comp=by_id.get(ref)
            if comp and comp.get('compatibilityDisposition')!='COMPATIBLE': err.append('MissionDispatchAuthorization references non-COMPATIBLE capability result')
        est=by_id.get(r.get('emergencyStopPolicyRef'))
        if est and est.get('readinessFreshnessState')!='FRESH': err.append('MissionDispatchAuthorization references non-FRESH EmergencyStopPolicy')
        hov=by_id.get(r.get('humanOverridePolicyRef'))
        if hov and hov.get('overrideReadinessState') not in ('READY','FRESH'): err.append('MissionDispatchAuthorization references unready HumanOverridePolicy')
        for ref in r.get('localFallbackPolicyRefs',[]) or []:
            lf=by_id.get(ref)
            if lf and lf.get('requiredBeforeDispatch') is not True: err.append('MissionDispatchAuthorization references LocalFallbackPolicy not requiredBeforeDispatch')
    if t=='CommandIntegrityBasis':
        if not after(r.get('expiresAt'),r.get('createdAtCommandTime')): err.append('CommandIntegrityBasis.expiresAt must be after createdAtCommandTime')
    if t=='CommandEnvelope':
        if not after(r.get('notAfter'),r.get('notBefore')): err.append('CommandEnvelope.notAfter must be after notBefore')
        nb,na=parse_dt(r.get('notBefore')),parse_dt(r.get('notAfter'))
        b=r.get('resolvedExecutionWindow') or {}; bnb,bna=parse_dt(b.get('notBefore')),parse_dt(b.get('notAfter'))
        if nb and bnb and nb<bnb: err.append('CommandEnvelope.notBefore before resolvedExecutionWindow.notBefore')
        if na and bna and na>bna: err.append('CommandEnvelope.notAfter after resolvedExecutionWindow.notAfter')
        daf,dau=parse_dt(r.get('dispatchAuthorizationValidFrom')),parse_dt(r.get('dispatchAuthorizationValidUntil'))
        if nb and daf and nb<daf: err.append('CommandEnvelope.notBefore before dispatch authorisation validFrom')
        if na and dau and na>dau: err.append('CommandEnvelope.notAfter after dispatch authorisation validUntil')
        if daf and dau and dau<=daf: err.append('dispatchAuthorizationValidUntil must be after dispatchAuthorizationValidFrom')
        da=by_id.get(r.get('missionDispatchAuthorizationRef'))
        if da:
            if da.get('authorizationState') not in ('APPROVED','ACTIVE'): err.append('CommandEnvelope references dispatch authorization not APPROVED/ACTIVE')
            if r.get('missionEnvelopeRef')!=da.get('missionEnvelopeRef'): err.append('CommandEnvelope missionEnvelopeRef mismatch with dispatch authorization')
            if r.get('missionPlanRef')!=da.get('missionPlanRef'): err.append('CommandEnvelope missionPlanRef mismatch with dispatch authorization')
            if r.get('recipientActorRef') not in (da.get('physicalActorRefs') or []): err.append('CommandEnvelope recipientActorRef not in dispatch authorization physicalActorRefs')
            if not in_window(r.get('notBefore'),r.get('notAfter'),da.get('validFrom'),da.get('validUntil')): err.append('CommandEnvelope command window not inside dispatch authorization validity window')
    if t=='MissionGeometryValidationResult' and r.get('resultDisposition')=='PASS':
        if r.get('overlapResult')=='OVERLAPS_NO_GO_ZONE': err.append('geometry PASS with no-go overlap')
        if r.get('crsCompatibilityState')!='COMPATIBLE': err.append('geometry PASS without CRS compatibility')
        if r.get('geometryFreshnessState')!='FRESH': err.append('geometry PASS without fresh geometry')
        if r.get('containmentResult')!='CONTAINED': err.append('geometry PASS without containment')
    if t=='MissionSafetyConstraint' and r.get('constraintClass') in CRITICAL_SAFETY and r.get('constraintStrength')=='ADVISORY_WARNING': err.append('critical mission safety constraint cannot be advisory warning')
    if t=='MissionOutputQualification':
        allowed=set(r.get('allowedUseClasses',[])); blocked=set(r.get('blockedUseClasses',[])); ov=allowed & blocked
        if ov: err.append('allowedUseClasses and blockedUseClasses overlap: '+','.join(sorted(ov)))
        if 'DISPATCH_AUTHORITY' in allowed: err.append('MissionOutputQualification may never allow DISPATCH_AUTHORITY')
        if r.get('outputDisposition')=='ADVISORY_ONLY':
            if allowed & FORBIDDEN_OUTPUT: err.append('advisory output allows forbidden uses: '+','.join(sorted(allowed & FORBIDDEN_OUTPUT)))
            missing=FORBIDDEN_OUTPUT - blocked
            if missing: err.append('advisory output missing blocked uses: '+','.join(sorted(missing)))
        if r.get('outputDisposition')=='MISSION_REPORT' and allowed!={'MISSION_REPORT'}: err.append('MISSION_REPORT disposition may allow only MISSION_REPORT use')
        if r.get('outputDisposition')=='EXECUTION_TRUTH_CANDIDATE' and 'EXECUTION_TRUTH' in allowed and not r.get('executionTruthPromotionBasisRef'): err.append('EXECUTION_TRUTH_CANDIDATE cannot allow EXECUTION_TRUTH without promotion basis')
        if r.get('outputDisposition')=='COMPLIANCE_FACT_CANDIDATE' and 'COMPLIANCE_FACT' in allowed and not r.get('complianceTwinPromotionBasisRef'): err.append('COMPLIANCE_FACT_CANDIDATE cannot allow COMPLIANCE_FACT without promotion basis')
    if t=='MissionVerification':
        if r.get('verificationDisposition') in ('FAILED_VERIFICATION','NOT_VERIFIED','DISPUTED') and r.get('acceptedConsequenceCandidateRefs'): err.append('failed/not verified/disputed verification cannot carry accepted consequence candidates')
        if r.get('verificationDisposition')=='VERIFIED_AS_REPORTED' and not r.get('acceptedConsequenceCandidateRefs') and not r.get('noAcceptedConsequencesReason'): err.append('verified as reported needs consequence candidate or noAcceptedConsequencesReason')
    if t=='CommandAcknowledgement':
        ack,end=parse_dt(r.get('acknowledgedAt')),parse_dt(r.get('commandNotAfter'))
        if ack and end and ack>end and r.get('acknowledgementState') in ('RECEIVED','ACCEPTED'): err.append('late acknowledgement cannot be RECEIVED/ACCEPTED')
    if t=='EmergencyStopPolicy':
        lt=parse_dt(r.get('lastTestedAt')); et=parse_dt(r.get('evaluationTime')) or EVALUATION_TIME
        if lt and lt>et: err.append('EmergencyStopPolicy.lastTestedAt must not be after evaluation time')
        if r.get('dispatchBoundUse') is True and r.get('readinessFreshnessState')!='FRESH': err.append('dispatch-bound emergency stop must be FRESH')
    if t=='PhysicalActorCapabilityProfile':
        if r.get('capabilityState')=='VERIFIED' and not r.get('lastVerifiedAt'): err.append('VERIFIED capability requires lastVerifiedAt')
        lv=parse_dt(r.get('lastVerifiedAt'))
        if lv and lv>EVALUATION_TIME: err.append('PhysicalActorCapabilityProfile.lastVerifiedAt must not be after evaluation time')
    if t=='MissionCapabilityCompatibilityResult' and r.get('compatibilityDisposition')=='COMPATIBLE':
        if r.get('capabilityStateAtCheck')!='VERIFIED': err.append('COMPATIBLE requires VERIFIED capability state')
        if r.get('capabilityFreshnessState')!='FRESH': err.append('COMPATIBLE requires fresh capability')
        if not r.get('checkedSafetyConstraintRefs'): err.append('COMPATIBLE requires checkedSafetyConstraintRefs')
        if r.get('commandChannelCompatibilityState')!='COMPATIBLE': err.append('COMPATIBLE requires command channel compatibility')
    if t=='NearMissEvent' and r.get('severity') in ('HIGH','CRITICAL') and r.get('requiresReview') is not True: err.append('HIGH/CRITICAL near miss requires review')
    if t=='PhysicalSafetyIncident':
        if r.get('severity') in ('CRITICAL','FATAL') and not r.get('reviewDecisionRef'): err.append('CRITICAL/FATAL incident requires reviewDecisionRef')
        if r.get('incidentState') in ('CONFIRMED','RESOLVED') and not (r.get('reviewDecisionRef') or r.get('authorityDecisionTraceRef')): err.append('CONFIRMED/RESOLVED incident requires review or authority trace')
    return err

def run(root):
    root=Path(root); schema_dir=root/'03_machine_contracts/drafts_non_default/cyber_physical_mission'; fixture_file=root/'04_implementation_and_conformance/conformance_runners/cyber_physical_mission_conformance/fixtures/cp12_phase7_2_fixtures.json'
    if not fixture_file.exists(): fixture_file=root/'04_implementation_and_conformance/conformance_runners/cyber_physical_mission_conformance/fixtures/cp12_phase7_1_fixtures.json'
    schemas={}
    for sf in schema_dir.glob('*.json'):
        data=json.load(open(sf)); Draft202012Validator.check_schema(data); schemas[data['properties']['contractType']['const']]=data
    fixtures=json.load(open(fixture_file))['fixtures']; results=[]
    for f in fixtures:
        records=f.get('records') or [f.get('record')]; errs=[]
        by_id={r.get('id'):r for r in records if r}
        for rec in records:
            if not rec: errs.append('missing record'); continue
            ct=rec.get('contractType')
            if ct not in schemas: errs.append('no schema for contractType '+str(ct))
            else: errs += [f'{ct}: '+e.message for e in Draft202012Validator(schemas[ct], format_checker=FormatChecker()).iter_errors(rec)]
            errs += [f'{ct}: '+e for e in semantic_errors(rec, records, by_id)]
        for rec in records:
            if rec and rec.get('contractType')=='CommandEnvelope':
                ib=by_id.get(rec.get('commandIntegrityBasisRef'))
                if ib:
                    bound=ib.get('resolvedRecipientActorRef') or ib.get('recipientBindingRef')
                    if bound != rec.get('recipientActorRef'): errs.append('CommandEnvelope recipientActorRef does not match CommandIntegrityBasis recipient binding')
        passed=len(errs)==0; ok=passed==f['expectedPass']
        results.append({'name':f['name'],'expectedPass':f['expectedPass'],'actualPass':passed,'ok':ok,'errors':errs})
    return {'schemaAware':True,'semanticHardeningAware':True,'crossRecordAware':True,'phase':'CP12 Phase 7.2','schemaCount':len(schemas),'fixtureCount':len(fixtures),'positiveFixtureCount':sum(1 for f in fixtures if f['expectedPass']),'negativeFixtureCount':sum(1 for f in fixtures if not f['expectedPass']),'allFixturesPassed':all(r['ok'] for r in results),'results':results}
if __name__=='__main__':
    root=sys.argv[1] if len(sys.argv)>1 else Path(__file__).resolve().parents[3]
    s=run(root); print(json.dumps(s,indent=2)); sys.exit(0 if s['allFixturesPassed'] else 1)
