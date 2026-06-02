
#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
IMPL = Path(__file__).resolve().parent
LIVE = IMPL / 'live_evidence_packets'

REGISTRY = IMPL / 'OFARM_external_evidence_intake_registry_v0_1.json'
PACKET = IMPL / 'OFARM_External_Evidence_Intake_Packet_v0_1.md'
RT_NOTE = IMPL / 'OFARM_RuntimeSurface_Live_Deployment_Evidence_Operator_Note_v0_2.md'
BRIDGE_NOTE = IMPL / 'OFARM_live_field_same_standard_bridge_operator_note_v0_2.md'
SNAP_V3 = IMPL / 'OFARM_post_hardening_readiness_snapshot_v0_3.json'
RESULTS_OUT = IMPL / 'OFARM_external_evidence_intake_results_v0_1.json'

SEARCHES = {
    'runtimeSurfaceLiveEvidence': {
        'pattern': 'runtime_surface_release_lane/OFARM_runtime_surface_live_deployment_evidence_v*.json',
        'required_keys': ['templateOnly', 'qualifiesAsLiveDeploymentEvidence', 'releaseBundleRef', 'surfaceContractRef', 'surfaceIdentityRef'],
        'qualifying_field': ('qualifiesAsLiveDeploymentEvidence', True),
    },
    'partnerOutputTelemetry': {
        'pattern': 'partner_output_channels/OFARM_runtime_surface_partner_output_telemetry_v*.json',
        'required_keys': ['templateOnly', 'partnerSurface', 'adapterSurfaceRef', 'traceBackRef'],
        'qualifying_field': ('templateOnly', False),
    },
    'sameStandardBridgeTelemetry': {
        'pattern': 'same_standard_bridge/OFARM_live_field_same_standard_bridge_telemetry_v*.json',
        'required_keys': ['templateOnly', 'qualifiesForPromotionIntake', 'requiredEvidenceClass'],
        'qualifying_field': ('qualifiesForPromotionIntake', True),
        'expected_class': 'LIVE_FIELD_COLLECTED_SAME_STANDARD_BRIDGE_TELEMETRY',
    },
    'sameStandardBridgeTraceBack': {
        'pattern': 'same_standard_bridge/OFARM_live_field_same_standard_bridge_trace_back_records_v*.json',
        'required_keys': ['templateOnly', 'qualifiesForPromotionIntake', 'requiredEvidenceClass'],
        'qualifying_field': ('qualifiesForPromotionIntake', True),
        'expected_class': 'DEPLOYMENT_PRODUCED_TRACE_BACK_LINKAGE',
    },
    'sameStandardBridgeApproval': {
        'pattern': 'same_standard_bridge/OFARM_same_standard_bridge_production_approval_record_v*.json',
        'required_keys': ['templateOnly', 'qualifiesForPromotionIntake', 'requiredEvidenceClass'],
        'qualifying_field': ('qualifiesForPromotionIntake', True),
        'expected_class': 'PRODUCTION_PROMOTION_APPROVAL_RECORD',
    },
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding='utf-8'))


def dump_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


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
    for field in ['releaseBundleRef', 'surfaceContractRef', 'surfaceIdentityRef', 'partnerSurface', 'adapterSurfaceRef', 'traceBackRef']:
        if field in payload and isinstance(payload.get(field), str) and payload.get(field, '').startswith('replace-with-'):
            reasons.append(f'PLACEHOLDER:{field}')
    if spec.get('expected_class') and payload.get('requiredEvidenceClass') != spec['expected_class']:
        reasons.append('EVIDENCE_CLASS_MISMATCH')
    qualifying = not reasons
    return {
        'file': path.relative_to(IMPL).as_posix(),
        'qualifying': qualifying,
        'reasons': reasons,
    }


def main() -> int:
    registry = load_json(REGISTRY)
    snapshot = load_json(SNAP_V3)

    results: dict[str, Any] = {
        'evaluatedAt': now_iso(),
        'packetRef': PACKET.name,
        'registryRef': REGISTRY.name,
        'snapshotRef': SNAP_V3.name,
        'dropZoneChecks': {},
        'artifactDiscovery': {},
        'summary': {},
        'limitations': [
            'No real deployment evidence artifacts are expected in the package at this stage.',
            'This runner operationalizes intake and qualification rules but does not fabricate live evidence.',
            'Partner-output telemetry remains support evidence unless a later governed promotion decision is made explicitly.'
        ],
        'overall': 'PASS_WITH_LIMITATIONS',
        'failingChecks': []
    }

    # Packet and notes exist
    for path in [PACKET, RT_NOTE, BRIDGE_NOTE, LIVE / 'README.md', LIVE / 'runtime_surface_release_lane' / 'README.md', LIVE / 'same_standard_bridge' / 'README.md', LIVE / 'partner_output_channels' / 'README.md']:
        key = path.relative_to(IMPL).as_posix() if path.is_relative_to(IMPL) else path.name
        status = 'PASS' if path.exists() else 'FAIL'
        results['dropZoneChecks'][f'{key} :: exists'] = status
        if status == 'FAIL':
            results['failingChecks'].append(f'{key} missing')

    # Registry consistency
    results['dropZoneChecks']['registry-overall-posture'] = 'PASS' if registry.get('overall') == 'PREPARED_FOR_EXTERNAL_EVIDENCE_COLLECTION' else 'FAIL'
    if results['dropZoneChecks']['registry-overall-posture'] == 'FAIL':
        results['failingChecks'].append('registry overall posture mismatch')
    results['dropZoneChecks']['snapshot-phase'] = 'PASS' if snapshot.get('currentPhase') == 'IMPLEMENTATION_AND_EVIDENCE' else 'FAIL'
    if results['dropZoneChecks']['snapshot-phase'] == 'FAIL':
        results['failingChecks'].append('snapshot phase mismatch')

    discovered_counts: dict[str, int] = {}
    qualifying_counts: dict[str, int] = {}
    for key, spec in SEARCHES.items():
        files = sorted((LIVE).glob(spec['pattern']))
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
        'productionFilenameFamilies': registry.get('summary', {}).get('productionFilenameFamilies', 0),
        'runtimeSurfaceLiveEvidenceArtifactsFound': discovered_counts['runtimeSurfaceLiveEvidence'],
        'runtimeSurfaceLiveEvidenceArtifactsQualifying': qualifying_counts['runtimeSurfaceLiveEvidence'],
        'partnerOutputTelemetryArtifactsFound': discovered_counts['partnerOutputTelemetry'],
        'partnerOutputTelemetryArtifactsQualifyingAsSupportEvidence': qualifying_counts['partnerOutputTelemetry'],
        'sameStandardBridgeTelemetryArtifactsFound': discovered_counts['sameStandardBridgeTelemetry'],
        'sameStandardBridgeTraceBackArtifactsFound': discovered_counts['sameStandardBridgeTraceBack'],
        'sameStandardBridgeApprovalArtifactsFound': discovered_counts['sameStandardBridgeApproval'],
        'sameStandardBridgePairsReadyByExternalEvidence': bridge_ready,
        'packageStillMissingQualifyingLiveEvidence': qualifying_counts['runtimeSurfaceLiveEvidence'] == 0 and bridge_ready == 0,
    }

    if results['failingChecks']:
        results['overall'] = 'FAIL'
    dump_json(RESULTS_OUT, results)
    return 0 if results['overall'] != 'FAIL' else 1


if __name__ == '__main__':
    raise SystemExit(main())
