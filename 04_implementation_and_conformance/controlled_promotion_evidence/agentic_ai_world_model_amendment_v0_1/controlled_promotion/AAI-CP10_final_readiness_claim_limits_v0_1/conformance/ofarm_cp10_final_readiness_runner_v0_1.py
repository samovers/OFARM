#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[6]
CP = REPO/'04_implementation_and_conformance/controlled_promotion_evidence/agentic_ai_world_model_amendment_v0_1/controlled_promotion/AAI-CP10_final_readiness_claim_limits_v0_1'

phase_report_paths = [
 '04_implementation_and_conformance/controlled_promotion_evidence/agentic_ai_world_model_amendment_v0_1/controlled_promotion/AAI-CP1_ai_facing_release_qualification_gate_v0_1/conformance/validation_report.json',
 '04_implementation_and_conformance/controlled_promotion_evidence/agentic_ai_world_model_amendment_v0_1/controlled_promotion/AAI-CP2_public_surface_preflight_trace_result_qualification_v0_1/conformance/validation_report.json',
 '04_implementation_and_conformance/controlled_promotion_evidence/agentic_ai_world_model_amendment_v0_1/controlled_promotion/AAI-CP3_agent_actorship_sponsor_bound_authority_v0_1/conformance/validation_report.json',
 '04_implementation_and_conformance/controlled_promotion_evidence/agentic_ai_world_model_amendment_v0_1/controlled_promotion/AAI-CP4_agent_run_trace_handoff_v0_1/conformance/validation_report.json',
 '04_implementation_and_conformance/controlled_promotion_evidence/agentic_ai_world_model_amendment_v0_1/controlled_promotion/AAI-CP5_capability_tool_manifest_honesty_v0_1/conformance/validation_report.json',
 '04_implementation_and_conformance/controlled_promotion_evidence/agentic_ai_world_model_amendment_v0_1/controlled_promotion/AAI-CP6_minimal_hostile_runtime_conformance_stub_v0_1/conformance/validation_report.json',
 '04_implementation_and_conformance/controlled_promotion_evidence/agentic_ai_world_model_amendment_v0_1/controlled_promotion/AAI-CP7_advisory_world_model_runtime_v0_1/conformance/validation_report.json',
 '04_implementation_and_conformance/controlled_promotion_evidence/agentic_ai_world_model_amendment_v0_1/controlled_promotion/AAI-CP8_evidenceneed_observationrequest_burden_controls_v0_1/conformance/validation_report.json',
 '04_implementation_and_conformance/controlled_promotion_evidence/agentic_ai_world_model_amendment_v0_1/controlled_promotion/AAI-CP9_farmer_value_ux_scenario_conformance_v0_1/conformance/validation_report.json',
]

required_blocked = {
 'production readiness',
 'full runtime AI-agent readiness',
 'two-agent compatibility as a general/platform claim',
 'full Phase 9 conformance pass',
 'autonomous compliance decisioning',
 'world-model readiness',
 'farmer UX readiness',
 'live farmer-pilot validation',
 'legal advice',
 'external-standard readiness',
}

failures=[]
records=[]

for rel in phase_report_paths:
    path=REPO/rel
    if not path.exists():
        failures.append(f'missing phase report: {rel}')
        continue
    data=json.loads(path.read_text())
    status=data.get('status') or data.get('result',{}).get('status')
    records.append({'path': rel, 'status': status})
    if status != 'PASS': failures.append(f'phase report not PASS: {rel} -> {status}')

posture=json.loads((CP/'final_readiness_posture.json').read_text())
claims=json.loads((CP/'readiness_claim_register.json').read_text())
limits=json.loads((CP/'claim_limits.json').read_text())

blocked=set(posture.get('blockedClaims', []))
missing=required_blocked-blocked
if missing: failures.append(f'final_readiness_posture missing blocked claims: {sorted(missing)}')

claim_status={c['claim']: c['status'] for c in claims.get('claims',[])}
for c in required_blocked:
    if claim_status.get(c) != 'blocked':
        failures.append(f'readiness_claim_register does not block: {c}')

if any('production readiness' in x.lower() and 'blocked' not in str(x).lower() for x in posture.get('allowedBoundedClaims', [])):
    failures.append('allowedBoundedClaims appears to allow production readiness')

memo=(REPO/'00_active_baseline/OFARM_post_gap_closure_readiness_gate_memo_v0_1.md').read_text()
hostile=(REPO/'00_active_baseline/OFARM_final_hostile_review_after_gap_closure_v0_1.md').read_text()
if 'AAI-CP10 final readiness and claim-limit addendum' not in memo:
    failures.append('readiness memo missing CP10 addendum')
if 'AAI-CP10 hostile-review closure update' not in hostile:
    failures.append('hostile review memo missing CP10 update')

report={
 'schemaVersion':'ofarm.aai.cp10.validationReport.v0.1',
 'phase':'AAI-CP10',
 'status':'PASS' if not failures else 'FAIL',
 'scope':'final readiness and claim-limit validation; not production readiness and not new semantic promotion',
 'phaseReportsChecked': len(records),
 'records': records,
 'blockedClaimsChecked': sorted(required_blocked),
 'failures': failures,
 'nonClaims': sorted(required_blocked)
}
(CP/'conformance/validation_report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
print(json.dumps(report, indent=2))
raise SystemExit(0 if not failures else 1)
