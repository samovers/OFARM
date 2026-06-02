#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

IMPL = Path(__file__).resolve().parent
LIVE = IMPL / 'live_evidence_packets'
DECISIONS = IMPL / 'live_evidence_decisions'

REGISTRY = IMPL / 'OFARM_external_evidence_decision_registry_v0_1.json'
PACKET = IMPL / 'OFARM_External_Evidence_Decision_and_Disposition_Packet_v0_1.md'
REVIEWER_PACKET = IMPL / 'OFARM_External_Evidence_Reviewer_Handoff_Packet_v0_1.md'
REVIEWER_CHECKLIST = IMPL / 'OFARM_External_Evidence_Reviewer_Checklist_v0_1.md'
TEMPLATE = IMPL / 'OFARM_external_evidence_decision_record_template_v0_1.json'
INTAKE_RESULTS = IMPL / 'OFARM_external_evidence_intake_results_v0_3.json'
SNAP = IMPL / 'OFARM_post_hardening_readiness_snapshot_v0_6.json'
RESULTS_OUT = IMPL / 'OFARM_external_evidence_decision_results_v0_1.json'

LANES = {
    'runtimeSurfaceReviewDecisions': {
        'pattern': 'runtime_surface_release_lane/OFARM_runtime_surface_live_deployment_evidence_decision_v*.json',
        'evidence_prefix': '04_implementation_and_conformance/pilot_material/live_evidence_packets/runtime_surface_release_lane/',
        'lane': 'RUNTIME_SURFACE_RELEASE_LANE',
        'allowed': {
            'QUALIFY_AS_GOVERNED_RUNTIME_SURFACE_LIVE_EVIDENCE',
            'REQUIRE_REDACTION_REWORK',
            'REQUIRE_SCOPE_REVIEW',
            'REJECT_AS_NON_QUALIFYING',
        },
    },
    'partnerOutputReviewDecisions': {
        'pattern': 'partner_output_channels/OFARM_runtime_surface_partner_output_telemetry_decision_v*.json',
        'evidence_prefix': '04_implementation_and_conformance/pilot_material/live_evidence_packets/partner_output_channels/',
        'lane': 'PARTNER_OUTPUT_CHANNELS',
        'allowed': {
            'QUALIFY_AS_PARTNER_OUTPUT_SUPPORT_EVIDENCE',
            'REQUIRE_REDACTION_REWORK',
            'REQUIRE_SCOPE_REVIEW',
            'REJECT_AS_NON_QUALIFYING',
        },
    },
    'sameStandardBridgeReviewDecisions': {
        'pattern': 'same_standard_bridge/OFARM_same_standard_bridge_promotion_evidence_decision_v*.json',
        'evidence_prefix': '04_implementation_and_conformance/pilot_material/live_evidence_packets/same_standard_bridge/',
        'lane': 'SAME_STANDARD_BRIDGE',
        'allowed': {
            'COUNT_TOWARD_SAME_STANDARD_BRIDGE_PROMOTION_GATE',
            'HOLD_FOR_BRIDGE_SET_COMPLETION',
            'REQUIRE_REDACTION_REWORK',
            'REQUIRE_SCOPE_REVIEW',
            'REJECT_AS_NON_QUALIFYING',
        },
    },
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding='utf-8'))


def dump_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding='utf-8')


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def classify_decision(path: Path, spec: dict[str, Any]) -> dict[str, Any]:
    payload = load_json(path)
    reasons: list[str] = []
    for key in ['templateOnly', 'reviewedArtifactRef', 'decisionLane', 'decision', 'reviewedAt', 'reviewerPartyRef', 'reviewerRoleRef', 'linkedIntakeResultsRef']:
        if key not in payload:
            reasons.append(f'MISSING_KEY:{key}')
    if payload.get('templateOnly') is not False:
        reasons.append('TEMPLATE_ONLY_OR_UNSET')
    if payload.get('decisionLane') != spec['lane']:
        reasons.append('DECISION_LANE_MISMATCH')
    if payload.get('decision') not in spec['allowed']:
        reasons.append('DECISION_VALUE_MISMATCH')
    if payload.get('linkedIntakeResultsRef') != INTAKE_RESULTS.name:
        reasons.append('INTAKE_RESULTS_REF_MISMATCH')
    if not isinstance(payload.get('reviewedArtifactRef'), str) or not payload.get('reviewedArtifactRef', '').startswith(spec['evidence_prefix']):
        reasons.append('REVIEWED_ARTIFACT_PREFIX_MISMATCH')
    else:
        ref = IMPL.parent / payload['reviewedArtifactRef'].replace('04_implementation_and_conformance/', '')
        if not ref.exists():
            reasons.append('REVIEWED_ARTIFACT_MISSING')
    if payload.get('decision') == 'COUNT_TOWARD_SAME_STANDARD_BRIDGE_PROMOTION_GATE':
        if not payload.get('candidatePairId') or str(payload.get('candidatePairId')).startswith('replace-with-'):
            reasons.append('MISSING_CANDIDATE_PAIR_ID')
    for field in ['reviewedArtifactRef', 'reviewedArtifactDigest', 'reviewerPartyRef', 'reviewerRoleRef']:
        value = payload.get(field)
        if isinstance(value, str) and (value.startswith('replace-with-') or 'FILL_WITH_REAL' in value):
            reasons.append(f'PLACEHOLDER:{field}')
    qualifying = not reasons
    return {
        'file': path.relative_to(IMPL).as_posix(),
        'qualifying': qualifying,
        'decision': payload.get('decision'),
        'reviewedArtifactRef': payload.get('reviewedArtifactRef'),
        'reasons': reasons,
    }


def main() -> int:
    registry = load_json(REGISTRY)
    snapshot = load_json(SNAP)
    intake_results = load_json(INTAKE_RESULTS)

    results: dict[str, Any] = {
        'evaluatedAt': now_iso(),
        'packetRef': PACKET.name,
        'registryRef': REGISTRY.name,
        'intakeResultsRef': INTAKE_RESULTS.name,
        'snapshotRef': SNAP.name,
        'decisionLaneChecks': {},
        'decisionDiscovery': {},
        'summary': {},
        'limitations': [
            'No accountable review decision artifacts are expected in the package at this stage.',
            'This runner checks the mirrored reviewer-side lane but does not replace human judgment.',
            'A decision record without a real matching evidence artifact still does not count as proof.'
        ],
        'overall': 'PASS_WITH_LIMITATIONS',
        'failingChecks': []
    }

    expected_paths = [
        PACKET,
        REGISTRY,
        REVIEWER_PACKET,
        REVIEWER_CHECKLIST,
        TEMPLATE,
        INTAKE_RESULTS,
        DECISIONS / 'README.md',
        DECISIONS / 'runtime_surface_release_lane' / 'README.md',
        DECISIONS / 'same_standard_bridge' / 'README.md',
        DECISIONS / 'partner_output_channels' / 'README.md',
    ]
    for path in expected_paths:
        key = path.relative_to(IMPL).as_posix()
        status = 'PASS' if path.exists() else 'FAIL'
        results['decisionLaneChecks'][f'{key} :: exists'] = status
        if status == 'FAIL':
            results['failingChecks'].append(f'{key} missing')

    results['decisionLaneChecks']['registry-overall-posture'] = 'PASS' if registry.get('overall') == 'PREPARED_FOR_ACCOUNTABLE_EXTERNAL_EVIDENCE_DECISIONS' else 'FAIL'
    if results['decisionLaneChecks']['registry-overall-posture'] == 'FAIL':
        results['failingChecks'].append('registry overall posture mismatch')
    results['decisionLaneChecks']['snapshot-phase'] = 'PASS' if snapshot.get('currentPhase') == 'IMPLEMENTATION_AND_EVIDENCE' else 'FAIL'
    if results['decisionLaneChecks']['snapshot-phase'] == 'FAIL':
        results['failingChecks'].append('snapshot phase mismatch')
    results['decisionLaneChecks']['intake-runner-overall'] = 'PASS' if intake_results.get('overall') == 'PASS_WITH_LIMITATIONS' else 'FAIL'
    if results['decisionLaneChecks']['intake-runner-overall'] == 'FAIL':
        results['failingChecks'].append('intake results not in expected posture')

    discovered = {}
    qualifying = {}
    decision_counts = {}
    for key, spec in LANES.items():
        files = sorted(DECISIONS.glob(spec['pattern']))
        classified = [classify_decision(path, spec) for path in files]
        discovered[key] = len(classified)
        qualifying[key] = sum(1 for row in classified if row['qualifying'])
        decision_counts[key] = {}
        for row in classified:
            decision_counts[key][row['decision']] = decision_counts[key].get(row['decision'], 0) + 1
        results['decisionDiscovery'][key] = {
            'pattern': f'04_implementation_and_conformance/pilot_material/live_evidence_decisions/{spec["pattern"]}',
            'discoveredFiles': [row['file'] for row in classified],
            'qualifyingFiles': [row['file'] for row in classified if row['qualifying']],
            'nonQualifyingFiles': [row for row in classified if not row['qualifying']],
            'decisionCounts': decision_counts[key],
        }

    results['summary'] = {
        'decisionLanesPrepared': len(registry.get('decisionLanes', [])),
        'reviewDecisionArtifactsFound': sum(discovered.values()),
        'reviewDecisionArtifactsQualifying': sum(qualifying.values()),
        'qualifyingRuntimeSurfaceDecisions': decision_counts['runtimeSurfaceReviewDecisions'].get('QUALIFY_AS_GOVERNED_RUNTIME_SURFACE_LIVE_EVIDENCE', 0),
        'partnerOutputSupportDecisions': decision_counts['partnerOutputReviewDecisions'].get('QUALIFY_AS_PARTNER_OUTPUT_SUPPORT_EVIDENCE', 0),
        'sameStandardBridgeGateCountingDecisions': decision_counts['sameStandardBridgeReviewDecisions'].get('COUNT_TOWARD_SAME_STANDARD_BRIDGE_PROMOTION_GATE', 0),
        'packageStillMissingAccountableReviewDecisions': sum(discovered.values()) == 0,
    }

    if results['failingChecks']:
        results['overall'] = 'FAIL'
    dump_json(RESULTS_OUT, results)
    return 0 if results['overall'] != 'FAIL' else 1


if __name__ == '__main__':
    raise SystemExit(main())
