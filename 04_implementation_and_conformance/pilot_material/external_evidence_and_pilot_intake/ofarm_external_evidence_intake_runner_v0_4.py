#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

IMPL = Path(__file__).resolve().parent
LIVE = IMPL / 'live_evidence_packets'
DECISIONS = IMPL / 'live_evidence_decisions'

REGISTRY = IMPL / 'OFARM_external_evidence_intake_registry_v0_4.json'
PACKET = IMPL / 'OFARM_External_Evidence_Intake_Packet_v0_4.md'
HANDOFF = IMPL / 'OFARM_External_Evidence_Pilot_Handoff_Packet_v0_3.md'
CHECKLIST = IMPL / 'OFARM_External_Evidence_Pilot_Day0_Operator_Checklist_v0_3.md'
REDACTION = IMPL / 'OFARM_External_Evidence_Redaction_and_Sovereignty_Note_v0_1.md'
AUTH_NOTE = IMPL / 'OFARM_External_Evidence_Authenticity_and_Qualification_Note_v0_1.md'
RT_NOTE = IMPL / 'OFARM_RuntimeSurface_Live_Deployment_Evidence_Operator_Note_v0_4.md'
BRIDGE_NOTE = IMPL / 'OFARM_live_field_same_standard_bridge_operator_note_v0_4.md'
DECISION_PACKET = IMPL / 'OFARM_External_Evidence_Decision_and_Disposition_Packet_v0_2.md'
REVIEWER_PACKET = IMPL / 'OFARM_External_Evidence_Reviewer_Handoff_Packet_v0_2.md'
REVIEWER_CHECKLIST = IMPL / 'OFARM_External_Evidence_Reviewer_Checklist_v0_2.md'
DECISION_TEMPLATE = IMPL / 'OFARM_external_evidence_decision_record_template_v0_2.json'
DECISION_REGISTRY = IMPL / 'OFARM_external_evidence_decision_registry_v0_2.json'
SNAP_V7 = IMPL / 'OFARM_post_hardening_readiness_snapshot_v0_7.json'
RESULTS_OUT = IMPL / 'OFARM_external_evidence_intake_results_v0_4.json'

SEARCHES = {
    'runtimeSurfaceLiveEvidence': {
        'pattern': 'runtime_surface_release_lane/OFARM_runtime_surface_live_deployment_evidence_v*.json',
        'required_keys': ['templateOnly', 'qualifiesAsLiveDeploymentEvidence', 'releaseBundleRef', 'surfaceContractRef', 'surfaceIdentityRef'],
        'qualifying_field': ('qualifiesAsLiveDeploymentEvidence', True),
        'expected_claim_kind': 'GOVERNED_RUNTIME_SURFACE_LIVE_DEPLOYMENT_EVIDENCE',
        'allowed_capture_modes': {'LIVE_DEPLOYMENT_OPERATOR_CAPTURE', 'LIVE_DEPLOYMENT_SYSTEM_EXPORT', 'LIVE_DEPLOYMENT_OPERATOR_CAPTURE_OR_SYSTEM_EXPORT'},
    },
    'partnerOutputTelemetry': {
        'pattern': 'partner_output_channels/OFARM_runtime_surface_partner_output_telemetry_v*.json',
        'required_keys': ['templateOnly', 'partnerSurface', 'adapterSurfaceRef', 'traceBackRef'],
        'qualifying_field': ('templateOnly', False),
        'expected_claim_kind': 'PARTNER_OUTPUT_SUPPORT_TELEMETRY',
        'allowed_capture_modes': {'LIVE_DEPLOYMENT_OPERATOR_CAPTURE', 'LIVE_DEPLOYMENT_SYSTEM_EXPORT', 'LIVE_DEPLOYMENT_OPERATOR_CAPTURE_OR_SYSTEM_EXPORT'},
    },
    'sameStandardBridgeTelemetry': {
        'pattern': 'same_standard_bridge/OFARM_live_field_same_standard_bridge_telemetry_v*.json',
        'required_keys': ['templateOnly', 'qualifiesForPromotionIntake', 'requiredEvidenceClass'],
        'qualifying_field': ('qualifiesForPromotionIntake', True),
        'expected_class': 'LIVE_FIELD_COLLECTED_SAME_STANDARD_BRIDGE_TELEMETRY',
        'expected_claim_kind': 'LIVE_FIELD_COLLECTED_SAME_STANDARD_BRIDGE_TELEMETRY',
        'allowed_capture_modes': {'LIVE_FIELD_OPERATOR_CAPTURE', 'LIVE_FIELD_SYSTEM_EXPORT', 'LIVE_FIELD_OPERATOR_CAPTURE_OR_SYSTEM_EXPORT'},
    },
    'sameStandardBridgeTraceBack': {
        'pattern': 'same_standard_bridge/OFARM_live_field_same_standard_bridge_trace_back_records_v*.json',
        'required_keys': ['templateOnly', 'qualifiesForPromotionIntake', 'requiredEvidenceClass'],
        'qualifying_field': ('qualifiesForPromotionIntake', True),
        'expected_class': 'DEPLOYMENT_PRODUCED_TRACE_BACK_LINKAGE',
        'expected_claim_kind': 'DEPLOYMENT_PRODUCED_TRACE_BACK_LINKAGE',
        'allowed_capture_modes': {'DEPLOYMENT_CONTROLLED_TRACEBACK_EXPORT'},
    },
    'sameStandardBridgeApproval': {
        'pattern': 'same_standard_bridge/OFARM_same_standard_bridge_production_approval_record_v*.json',
        'required_keys': ['templateOnly', 'qualifiesForPromotionIntake', 'requiredEvidenceClass'],
        'qualifying_field': ('qualifiesForPromotionIntake', True),
        'expected_class': 'PRODUCTION_PROMOTION_APPROVAL_RECORD',
        'expected_claim_kind': 'PRODUCTION_PROMOTION_APPROVAL_RECORD',
        'allowed_capture_modes': {'ACCOUNTABLE_PRODUCTION_APPROVAL'},
    },
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding='utf-8'))


def dump_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding='utf-8')


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def is_placeholder(value: Any) -> bool:
    if isinstance(value, str):
        return value.startswith('replace-with-') or value.startswith('<') or 'YYYY-MM-DD' in value or 'FILL_WITH_REAL' in value
    if isinstance(value, list):
        return any(is_placeholder(v) for v in value)
    if isinstance(value, dict):
        return any(is_placeholder(v) for v in value.values())
    return False


def classify_file(path: Path, spec: dict[str, Any]) -> dict[str, Any]:
    payload = load_json(path)
    reasons: list[str] = []
    for key in spec['required_keys']:
        if key not in payload:
            reasons.append(f'MISSING_KEY:{key}')
    q_key, q_expected = spec['qualifying_field']
    if payload.get(q_key) != q_expected:
        reasons.append(f'FIELD_MISMATCH:{q_key}')
    if payload.get('templateOnly') is not False:
        reasons.append('TEMPLATE_ONLY_OR_UNSET')
    if spec.get('expected_class') and payload.get('requiredEvidenceClass') != spec['expected_class']:
        reasons.append('EVIDENCE_CLASS_MISMATCH')

    auth = payload.get('authenticityEnvelope')
    if not isinstance(auth, dict):
        reasons.append('MISSING_AUTHENTICITY_ENVELOPE')
    else:
        for key in ['captureMode', 'repositoryAuthored', 'redactionApplied', 'attestedByRef', 'attestedAt', 'artifactDigest', 'sourceRealityClass']:
            if key not in auth:
                reasons.append(f'MISSING_AUTHENTICITY_KEY:{key}')
        if auth.get('repositoryAuthored') is not False:
            reasons.append('REPOSITORY_AUTHORED_OR_UNSET')
        if auth.get('sourceRealityClass') in {None, 'REHEARSAL'}:
            reasons.append('NON_REAL_SOURCE_REALITY_CLASS')
        if auth.get('captureMode') not in spec['allowed_capture_modes']:
            reasons.append('CAPTURE_MODE_MISMATCH')
        for key in ['attestedByRef', 'attestedAt', 'artifactDigest']:
            if is_placeholder(auth.get(key)):
                reasons.append(f'PLACEHOLDER:authenticityEnvelope.{key}')

    claim = payload.get('qualificationClaim')
    if not isinstance(claim, dict):
        reasons.append('MISSING_QUALIFICATION_CLAIM')
    else:
        if claim.get('claimKind') != spec['expected_claim_kind']:
            reasons.append('CLAIM_KIND_MISMATCH')
        if not isinstance(claim.get('nonClaims'), list) or not claim.get('nonClaims'):
            reasons.append('NON_CLAIMS_MISSING')
        if is_placeholder(claim.get('claimScopeRef')):
            reasons.append('PLACEHOLDER:qualificationClaim.claimScopeRef')

    for field in ['releaseBundleRef', 'surfaceContractRef', 'surfaceIdentityRef', 'partnerSurface', 'adapterSurfaceRef', 'traceBackRef']:
        if field in payload and is_placeholder(payload.get(field)):
            reasons.append(f'PLACEHOLDER:{field}')

    for lane_field in ['deploymentEvidenceRefs', 'serviceDescriptionRefs', 'relatedEvidenceRefs']:
        value = payload.get(lane_field)
        if isinstance(value, list) and any(isinstance(v, str) and 'pilot_intake_rehearsal/' in v for v in value):
            reasons.append(f'REHEARSAL_REF_IN_{lane_field.upper()}')
    if isinstance(payload.get('traceBackRef'), str) and 'pilot_intake_rehearsal/' in payload['traceBackRef']:
        reasons.append('REHEARSAL_REF_IN_TRACEBACK')

    qualifying = not reasons
    return {
        'file': path.relative_to(IMPL).as_posix(),
        'qualifying': qualifying,
        'claimKind': claim.get('claimKind') if isinstance(claim, dict) else None,
        'artifactDigest': auth.get('artifactDigest') if isinstance(auth, dict) else None,
        'reasons': reasons,
    }


def main() -> int:
    registry = load_json(REGISTRY)
    decision_registry = load_json(DECISION_REGISTRY)
    snapshot = load_json(SNAP_V7)

    results: dict[str, Any] = {
        'evaluatedAt': now_iso(),
        'packetRef': PACKET.name,
        'registryRef': REGISTRY.name,
        'snapshotRef': SNAP_V7.name,
        'decisionPacketRef': DECISION_PACKET.name,
        'decisionRegistryRef': DECISION_REGISTRY.name,
        'dropZoneChecks': {},
        'artifactDiscovery': {},
        'summary': {},
        'limitations': [
            'No real deployment evidence artifacts are expected in the package at this stage.',
            'This runner operationalizes authenticity and qualification rules but does not fabricate live evidence.',
            'The operator handoff kit, rehearsal lane, and mirrored decision lane reduce ambiguity but do not reduce the qualifying-evidence debt by themselves.'
        ],
        'overall': 'PASS_WITH_LIMITATIONS',
        'failingChecks': []
    }

    expected_paths = [
        PACKET, REGISTRY, HANDOFF, CHECKLIST, REDACTION, AUTH_NOTE, RT_NOTE, BRIDGE_NOTE,
        DECISION_PACKET, REVIEWER_PACKET, REVIEWER_CHECKLIST, DECISION_TEMPLATE, DECISION_REGISTRY,
        LIVE / 'README.md', LIVE / 'runtime_surface_release_lane' / 'README.md', LIVE / 'same_standard_bridge' / 'README.md', LIVE / 'partner_output_channels' / 'README.md',
        DECISIONS / 'README.md', DECISIONS / 'runtime_surface_release_lane' / 'README.md', DECISIONS / 'same_standard_bridge' / 'README.md', DECISIONS / 'partner_output_channels' / 'README.md',
    ]
    for path in expected_paths:
        key = path.relative_to(IMPL).as_posix()
        status = 'PASS' if path.exists() else 'FAIL'
        results['dropZoneChecks'][f'{key} :: exists'] = status
        if status == 'FAIL':
            results['failingChecks'].append(f'{key} missing')

    posture_ok = registry.get('overall') == 'PREPARED_FOR_AUTHENTICITY_GATED_PILOT_HANDOFF_EXTERNAL_EVIDENCE_AND_REVIEW_DECISIONS'
    results['dropZoneChecks']['registry-overall-posture'] = 'PASS' if posture_ok else 'FAIL'
    if not posture_ok:
        results['failingChecks'].append('registry overall posture mismatch')
    decision_ok = decision_registry.get('overall') == 'PREPARED_FOR_AUTHENTICITY_AWARE_ACCOUNTABLE_EXTERNAL_EVIDENCE_DECISIONS'
    results['dropZoneChecks']['decision-registry-overall-posture'] = 'PASS' if decision_ok else 'FAIL'
    if not decision_ok:
        results['failingChecks'].append('decision registry overall posture mismatch')
    snapshot_ok = snapshot.get('currentPhase') == 'IMPLEMENTATION_AND_EVIDENCE'
    results['dropZoneChecks']['snapshot-phase'] = 'PASS' if snapshot_ok else 'FAIL'
    if not snapshot_ok:
        results['failingChecks'].append('snapshot phase mismatch')

    discovered_counts: dict[str, int] = {}
    qualifying_counts: dict[str, int] = {}
    for key, spec in SEARCHES.items():
        files = sorted(LIVE.glob(spec['pattern']))
        classified = [classify_file(path, spec) for path in files]
        discovered_counts[key] = len(classified)
        qualifying_counts[key] = sum(1 for row in classified if row['qualifying'])
        results['artifactDiscovery'][key] = {
            'pattern': f'04_implementation_and_conformance/pilot_material/live_evidence_packets/{spec["pattern"]}',
            'discoveredFiles': [row['file'] for row in classified],
            'qualifyingFiles': [row['file'] for row in classified if row['qualifying']],
            'nonQualifyingFiles': [row for row in classified if not row['qualifying']],
        }

    bridge_ready = min(
        qualifying_counts['sameStandardBridgeTelemetry'],
        qualifying_counts['sameStandardBridgeTraceBack'],
        qualifying_counts['sameStandardBridgeApproval'],
    )

    results['summary'] = {
        'dropZonesPrepared': len(registry.get('dropZones', [])),
        'decisionLanesPrepared': len(decision_registry.get('decisionLanes', [])),
        'productionFilenameFamilies': registry.get('summary', {}).get('productionFilenameFamilies', 0),
        'pilotHandoffKitPresent': registry.get('summary', {}).get('pilotHandoffKitPresent', False),
        'reviewerDecisionLanePresent': registry.get('summary', {}).get('reviewerDecisionLanePresent', False),
        'authenticityQualificationGatePresent': registry.get('summary', {}).get('authenticityQualificationGatePresent', False),
        'runtimeSurfaceLiveEvidenceArtifactsFound': discovered_counts['runtimeSurfaceLiveEvidence'],
        'runtimeSurfaceLiveEvidenceArtifactsQualifying': qualifying_counts['runtimeSurfaceLiveEvidence'],
        'partnerOutputTelemetryArtifactsFound': discovered_counts['partnerOutputTelemetry'],
        'partnerOutputTelemetryArtifactsQualifyingAsSupportEvidence': qualifying_counts['partnerOutputTelemetry'],
        'sameStandardBridgeTelemetryArtifactsFound': discovered_counts['sameStandardBridgeTelemetry'],
        'sameStandardBridgeTraceBackArtifactsFound': discovered_counts['sameStandardBridgeTraceBack'],
        'sameStandardBridgeApprovalArtifactsFound': discovered_counts['sameStandardBridgeApproval'],
        'sameStandardBridgePairsReadyByExternalEvidence': bridge_ready,
        'packageStillMissingQualifyingLiveEvidence': sum(qualifying_counts.values()) == 0,
    }

    if results['failingChecks']:
        results['overall'] = 'FAIL'
    dump_json(RESULTS_OUT, results)
    return 0 if results['overall'] != 'FAIL' else 1


if __name__ == '__main__':
    raise SystemExit(main())
