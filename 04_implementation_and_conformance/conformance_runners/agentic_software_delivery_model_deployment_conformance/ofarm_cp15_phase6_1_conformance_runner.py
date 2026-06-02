#!/usr/bin/env python3
import json, sys
from pathlib import Path
from datetime import datetime, timezone
from jsonschema import Draft202012Validator

EVAL_TIME = datetime.fromisoformat('2026-05-30T00:00:00+00:00')
ROOT = Path(__file__).resolve().parents[3]
SCHEMA_DIR = ROOT/'03_machine_contracts/drafts_non_default/agentic_software_delivery_model_deployment'
FIXTURE_FILE = Path(__file__).with_name('fixtures_cp15_phase6_1.json')
RESULT_FILE = Path(__file__).with_name('CP15_phase6_1_conformance_results.json')

def parse_dt(s):
    if not s: return None
    return datetime.fromisoformat(s.replace('Z','+00:00'))

def load_schemas():
    schemas={}
    validators={}
    for p in SCHEMA_DIR.glob('OFARM_*_schema_v0_1.json'):
        d=json.load(open(p))
        t=d.get('properties',{}).get('artifactType',{}).get('const')
        if t:
            schemas[t]=d
            validators[t]=Draft202012Validator(d)
    return schemas, validators

def has(r,k): return k in r and r[k] not in (None,'',[],{})

def get(refs, byid):
    if isinstance(refs,str): return byid.get(refs)
    return [byid.get(x) for x in (refs or [])]

def status_ok_for_scan(r, waivers):
    sev=r.get('severityMax')
    disp=r.get('disposition')
    state=r.get('scanState') or r.get('analysisState')
    if state=='FAILED' and disp=='PASS': return False
    if sev=='CRITICAL' and disp=='PASS': return False
    if sev in ['HIGH','CRITICAL'] and disp not in ['REQUIRE_REVIEW','BLOCK','PASS_WITH_WARNINGS']:
        return False
    if sev=='CRITICAL' and disp=='PASS_WITH_WARNINGS':
        return any(waivers.get(w,{}).get('waiverState')=='APPROVED' for w in r.get('securityFindingWaiverRefs',[]))
    if disp in ['BLOCK','TOOL_FAILED']: return False
    return True

def sem_check(records):
    issues=[]
    byid={r.get('artifactId'):r for r in records if r.get('artifactId')}
    waivers={rid:r for rid,r in byid.items() if r.get('artifactType')=='SecurityFindingWaiver'}
    def issue(msg): issues.append(msg)
    # standalone gates
    for r in records:
        t=r.get('artifactType')
        if t in ['SecurityScanResult','StaticAnalysisResult']:
            if not status_ok_for_scan(r, waivers): issue(f'{t} {r.get("artifactId")} has invalid severity/disposition/state')
        if t=='DependencyRiskAssessment':
            risk=r.get('riskClass'); disp=r.get('disposition')
            if risk=='CRITICAL' and not (disp=='ALLOW_WITH_REVIEW' and has(r,'reviewDecisionRef')): issue('critical dependency risk without review')
            if risk=='UNKNOWN' and disp=='ALLOW': issue('unknown dependency risk cannot ALLOW')
            if disp=='ALLOW' and risk not in ['LOW','MEDIUM']: issue('dependency ALLOW requires low/medium risk')
        if t=='RollbackPlan' and r.get('rollbackReadinessState')=='READY':
            if parse_dt(r.get('lastTestedAt')) and parse_dt(r.get('lastTestedAt')) > EVAL_TIME: issue('rollback ready with future test')
            if r.get('rollbackReadinessFreshnessState')!='FRESH': issue('rollback ready without fresh state')
            if not r.get('rollbackTestResultRefs'): issue('rollback ready without test result refs')
        if t=='SecurityFindingWaiver' and r.get('waiverState')=='APPROVED':
            if parse_dt(r.get('expiresAt')) <= parse_dt(r.get('createdAt')): issue('waiver expires before created')
            if parse_dt(r.get('expiresAt')) < EVAL_TIME: issue('approved waiver expired')
            if r.get('severityCovered')=='CRITICAL' and not has(r,'specialAuthorityRef'): issue('critical waiver missing special authority')
        if t=='ModelEvaluationEvidence':
            if r.get('biasRiskClass') in ['HIGH','UNKNOWN'] and r.get('evaluationDisposition')=='SUFFICIENT_FOR_CANDIDATE': issue('high/unknown bias model evidence cannot be sufficient')
        if t=='GeneratedPromptOrPolicyArtifact':
            if r.get('targetUseClass') in ['STATE_AFFECTING','HIGH_CONSEQUENCE','DEPLOYMENT_RELATED','MISSION_RELATED']:
                if r.get('reviewRequired') is not True: issue('high consequence prompt/policy requires review')
                if r.get('artifactStatus')=='APPROVED_CANDIDATE':
                    if not has(r,'authorityDecisionTraceRef') or not r.get('conformanceRunRefs') or not r.get('securityScanResultRefs'): issue('approved prompt/policy missing authority/conformance/security')
        if t=='SemanticMappingCandidate' and r.get('mappingStatus')=='APPROVED_CANDIDATE':
            if r.get('mappingConfidenceClass')=='INSUFFICIENT': issue('insufficient mapping cannot be approved')
            if r.get('mappingConfidenceClass')=='HIGH' and not (r.get('mappingCoverageSufficient') is True and r.get('lossMapDisposition')=='ACCEPTABLE'):
                issue('high confidence mapping missing coverage/loss sufficiency')
        if t=='GeneratedAdapterArtifact' and r.get('adapterStatus')=='APPROVED_CANDIDATE':
            if r.get('adapterKind')=='ROBOT_VENDOR_ADAPTER' and not r.get('cp12GateTraceRefs'): issue('robot adapter missing cp12 gate')
            if r.get('adapterKind')=='DATA_SPACE_ADAPTER' and not r.get('cp14GateTraceRefs'): issue('data-space adapter missing cp14 gate')
            if r.get('adapterKind')=='REGISTRY_ADAPTER' and not has(r,'mappingCurrentnessReviewRef'): issue('registry adapter missing currentness review')
            if not r.get('conformanceRunRefs') or not r.get('securityScanResultRefs'): issue('approved adapter missing conformance/security')
            if not (r.get('mappingCoverageSufficient') is True and r.get('lossMapDisposition')=='ACCEPTABLE'): issue('approved adapter mapping insufficient')
        if t=='DeploymentOutputQualification':
            allowed=set(r.get('allowedUseClasses') or []); blocked=set(r.get('blockedUseClasses') or [])
            if allowed & blocked: issue('deployment output allowed/blocked overlap')
            strong={'DEPLOYMENT_AUTHORITY','RUNTIME_AUTHORITY','CURRENT_DEFAULT_PROMOTION','MISSION_AUTHORITY','COMPLIANCE_FACT','PRODUCTION_READINESS','MODEL_DEPLOYMENT_AUTHORITY','AUTOMATIC_EXECUTION'}
            if r.get('advisoryOnly') and not strong.issubset(blocked): issue('advisory output missing strong blocked uses')
            if r.get('outputDisposition')=='PRODUCTION_READINESS_CANDIDATE' and not has(r,'reviewBasisRef'): issue('production readiness candidate lacks review basis')
    # record-specific cross-record checks
    for r in records:
        t=r.get('artifactType')
        if t=='DeploymentCandidate' and r.get('candidateState')=='APPROVED_CANDIDATE':
            b=byid.get(r.get('buildProvenanceRef')); s=byid.get(r.get('sbomRef')); d=byid.get(r.get('dependencyRiskAssessmentRef'))
            if not b or b.get('buildStatus')!='SUCCEEDED': issue('approved deployment candidate references failed/missing build')
            if not s or s.get('sbomStatus')!='VALIDATED': issue('approved deployment candidate references invalid sbom')
            if not d or d.get('artifactType')!='DependencyRiskAssessment': issue('approved candidate missing dependency risk assessment')
            for ref in r.get('staticAnalysisResultRefs',[]):
                x=byid.get(ref); 
                if not x or not status_ok_for_scan(x, waivers): issue('approved candidate references unacceptable static analysis')
            for ref in r.get('securityScanResultRefs',[]):
                x=byid.get(ref)
                if not x or not status_ok_for_scan(x, waivers): issue('approved candidate references unacceptable security scan')
            for ref in r.get('conformanceRunRefs',[]):
                x=byid.get(ref)
                if not x or x.get('runDisposition') not in ['PASS','PASS_WITH_WARNINGS']: issue('approved candidate references failed conformance')
        if t=='DeploymentPlan' and r.get('planState')=='APPROVED_CANDIDATE':
            c=byid.get(r.get('deploymentCandidateRef'))
            rb=byid.get(r.get('rollbackPlanRef')); cp=byid.get(r.get('canaryPlanRef'))
            if c and c.get('candidateState') not in ['APPROVED_CANDIDATE','UNDER_REVIEW']: issue('approved plan references rejected candidate')
            if not rb or rb.get('rollbackReadinessState')!='READY': issue('approved plan lacks ready rollback')
            if not cp or cp.get('canaryState') not in ['APPROVED','ACTIVE','COMPLETED']: issue('approved plan lacks approved canary')
            if not r.get('cpGateRefs') and not has(r,'noApplicableCPGatesBasis'): issue('approved plan lacks cp gates or no-applicable basis')
            if r.get('blastRadiusClass') in ['SINGLE_FARM','MULTI_FARM','GLOBAL'] and not has(r,'blastRadiusApprovalRef'): issue('broad blast radius missing approval')
            if r.get('blastRadiusClass')=='GLOBAL' and not has(r,'stagedRolloutPlanRef'): issue('global blast radius missing staged rollout')
        if t=='DeploymentAuthorization':
            vf=parse_dt(r.get('validFrom')); vu=parse_dt(r.get('validUntil'))
            if vu <= vf: issue('deployment authorization invalid time window')
            if r.get('authorizationState')=='ACTIVE' and vu < EVAL_TIME: issue('active deployment authorization expired')
            if r.get('authorizationState') in ['APPROVED','ACTIVE']:
                p=byid.get(r.get('deploymentPlanRef'))
                if p and p.get('planState')!='APPROVED_CANDIDATE': issue('authorization references non-approved plan')
        if t=='ReleaseBundle' and r.get('bundleState') in ['SIGNED','RELEASE_CANDIDATE']:
            dc=byid.get(r.get('deploymentCandidateRef')); sb=byid.get(r.get('sbomRef'))
            if dc and dc.get('candidateState')!='APPROVED_CANDIDATE': issue('release bundle references non-approved candidate')
            if sb and sb.get('sbomStatus')!='VALIDATED': issue('release bundle references invalid sbom')
            if sb and set(r.get('artifactRefs',[])) - set(sb.get('artifactRefs',[]) + sb.get('coveredArtifactRefs',[])): issue('release bundle artifact not covered by sbom')
            for cref in r.get('conformanceRunRefs',[]):
                c=byid.get(cref)
                if c and c.get('runDisposition') not in ['PASS','PASS_WITH_WARNINGS']: issue('release bundle references failed conformance')
            required={'RELEASE_DIGEST','ARTIFACT_REFS','SBOM','DEPLOYMENT_CANDIDATE'}
            if not required.issubset(set(r.get('signatureCoverageClasses') or [])): issue('release bundle missing signature coverage')
        if t=='DeploymentPromotionDecision' and r.get('decisionState')=='APPROVED':
            dc=byid.get(r.get('deploymentCandidateRef')); au=byid.get(r.get('deploymentAuthorizationRef'))
            if dc and dc.get('candidateState')!='APPROVED_CANDIDATE': issue('promotion references non-approved candidate')
            if au and au.get('authorizationState') not in ['APPROVED','ACTIVE']: issue('promotion references non-active authorization')
            if r.get('promotionDisposition') in ['PROMOTE_TO_RUNTIME','PROMOTE_TO_RELEASE_BUNDLE','PROMOTE_TO_CANARY']:
                if parse_dt(au.get('validUntil')) < EVAL_TIME if au else True: issue('promotion authorization expired')
            if r.get('promotionDisposition')=='PROMOTE_TO_RUNTIME':
                rel=byid.get(r.get('releaseBundleRef')); rb=byid.get(r.get('rollbackPlanRef')); cr=byid.get(r.get('canaryResultRef'))
                if not rel or rel.get('bundleState') not in ['SIGNED','RELEASE_CANDIDATE']: issue('runtime promotion lacks signed/release bundle')
                if not rb or rb.get('rollbackReadinessState')!='READY': issue('runtime promotion lacks ready rollback')
                if cr and not (cr.get('resultState')=='PASSED' and cr.get('resultDisposition')=='PASS'): issue('runtime promotion has failed canary')
                # incidents block
                for inc in records:
                    if inc.get('artifactType')=='DeploymentIncident' and inc.get('incidentState')=='CONFIRMED' and inc.get('severityClass') in ['HIGH','CRITICAL'] and inc.get('deploymentRef') in [r.get('deploymentCandidateRef'), r.get('releaseBundleRef')]:
                        issue('critical deployment incident blocks promotion')
        if t=='RuntimeSurfaceReleaseBinding' and r.get('bindingState')=='ACTIVE_NON_DEFAULT':
            rel=byid.get(r.get('releaseBundleRef')); au=byid.get(r.get('deploymentAuthorizationRef'))
            if not rel or rel.get('bundleState') not in ['SIGNED','RELEASE_CANDIDATE']: issue('active binding lacks signed bundle')
            if not au or au.get('authorizationState')!='ACTIVE': issue('active binding lacks active authorization')
            if r.get('doesNotPromoteCurrentDefault') is not True: issue('runtime binding promotes current default')
            for sci in records:
                if sci.get('artifactType')=='SoftwareSupplyChainIncident' and sci.get('incidentState')=='CONFIRMED' and sci.get('severityClass') in ['HIGH','CRITICAL']:
                    if set(sci.get('affectedArtifactRefs',[])) & set(rel.get('artifactRefs',[]) if rel else []): issue('critical supply chain incident blocks binding')
        if t=='RuntimeDeploymentReceipt' and r.get('receiptState')=='CONFIRMED_BY_RUNTIME':
            au=byid.get(r.get('deploymentAuthorizationRef')); rel=byid.get(r.get('releaseBundleRef')); b=byid.get(r.get('runtimeSurfaceBindingRef'))
            if not au or au.get('authorizationState')!='ACTIVE': issue('runtime receipt lacks active authorization')
            if not rel or rel.get('bundleState') not in ['SIGNED','RELEASE_CANDIDATE']: issue('runtime receipt lacks signed bundle')
            if not b or b.get('bindingState')!='ACTIVE_NON_DEFAULT': issue('runtime receipt lacks active non-default binding')
            deployed=parse_dt(r.get('deployedAt'))
            if au and not (parse_dt(au.get('validFrom')) <= deployed <= parse_dt(au.get('validUntil'))): issue('runtime receipt outside authorization window')
            if r.get('doesNotCreateProductionReadiness') is not True: issue('runtime receipt creates production readiness')
        if t=='CanaryResult':
            if r.get('resultState')=='PASSED' and r.get('resultDisposition')!='PASS': issue('canary passed with non-pass disposition')
            if r.get('resultDisposition')=='PASS' and r.get('resultState')!='PASSED': issue('canary pass disposition without passed state')
            for tr in r.get('telemetryRefs',[]):
                tel=byid.get(tr)
                if tel and tel.get('telemetryDisposition') in ['INCIDENT_CANDIDATE','INVALIDATED']: issue('canary passed with incident telemetry')
        if t=='ModelDeploymentCandidate' and r.get('modelCandidateState')=='APPROVED_CANDIDATE':
            for evr in r.get('modelEvaluationEvidenceRefs',[]):
                ev=byid.get(evr)
                if not ev or ev.get('evaluationDisposition')!='SUFFICIENT_FOR_CANDIDATE' or ev.get('biasRiskClass') in ['HIGH','UNKNOWN']: issue('model candidate lacks sufficient low/medium bias evidence')
    return issues

def run():
    schemas, validators = load_schemas()
    data=json.load(open(FIXTURE_FILE))
    results=[]; all_pass=True
    for fx in data['fixtures']:
        issues=[]
        for r in fx['records']:
            t=r.get('artifactType')
            if t in validators:
                errs=sorted(validators[t].iter_errors(r), key=lambda e:e.path)
                for e in errs:
                    issues.append(f'schema:{t}:{list(e.path)}:{e.message}')
            else:
                issues.append(f'unknown artifactType {t}')
        if not issues:
            issues.extend(sem_check(fx['records']))
        actual = (len(issues)==0)
        passed = actual == fx['expectedPass']
        all_pass = all_pass and passed
        results.append({'fixtureId':fx['fixtureId'],'expectedPass':fx['expectedPass'],'actualPass':actual,'passed':passed,'issues':issues[:20]})
    summary={
        'schemaAware': True,
        'semanticHardeningAware': True,
        'crossRecordAware': True,
        'supplyChainAware': True,
        'modelDeploymentBoundaryAware': True,
        'fixtureCount': len(results),
        'positiveFixtureCount': sum(1 for f in data['fixtures'] if f['expectedPass']),
        'negativeFixtureCount': sum(1 for f in data['fixtures'] if not f['expectedPass']),
        'allFixturesPassed': all_pass,
        'results': results
    }
    json.dump(summary, open(RESULT_FILE,'w'), indent=2, sort_keys=True)
    print(json.dumps({k:v for k,v in summary.items() if k!='results'}, indent=2))
    return 0 if all_pass else 1
if __name__=='__main__':
    raise SystemExit(run())
