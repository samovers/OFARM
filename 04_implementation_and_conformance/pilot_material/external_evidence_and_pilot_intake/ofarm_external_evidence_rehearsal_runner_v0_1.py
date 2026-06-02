#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

IMPL = Path(__file__).resolve().parent
REHEARSAL = IMPL / 'pilot_intake_rehearsal'
RUNTIME = REHEARSAL / 'runtime_surface_release_lane' / 'OFARM_runtime_surface_live_deployment_evidence_rehearsal_v0_1.json'
PARTNER = REHEARSAL / 'partner_output_channels' / 'OFARM_runtime_surface_partner_output_telemetry_rehearsal_v0_1.json'
README = REHEARSAL / 'README.md'
INTAKE_RESULTS = IMPL / 'OFARM_external_evidence_intake_results_v0_2.json'
OUT = IMPL / 'OFARM_external_evidence_rehearsal_results_v0_1.json'


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding='utf-8'))


def dump_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def has_placeholder(value: Any) -> bool:
    if isinstance(value, str):
        return value.startswith('replace-with-') or 'YYYY-MM-DD' in value
    if isinstance(value, list):
        return any(has_placeholder(v) for v in value)
    if isinstance(value, dict):
        return any(has_placeholder(v) for v in value.values())
    return False


def main() -> int:
    runtime = load_json(RUNTIME)
    partner = load_json(PARTNER)
    intake = load_json(INTAKE_RESULTS)

    checks: dict[str, str] = {}
    issues: list[str] = []

    for path in [README, RUNTIME, PARTNER, INTAKE_RESULTS]:
        key = path.relative_to(IMPL).as_posix()
        ok = path.exists()
        checks[f'{key} :: exists'] = 'PASS' if ok else 'FAIL'
        if not ok:
            issues.append(f'missing {key}')

    def expect(payload: dict[str, Any], field: str, expected: Any, label: str) -> None:
        ok = payload.get(field) == expected
        checks[label] = 'PASS' if ok else 'FAIL'
        if not ok:
            issues.append(f'{label} expected {expected!r}')

    expect(runtime, 'templateOnly', False, 'runtime rehearsal templateOnly false')
    expect(runtime, 'qualifiesAsLiveDeploymentEvidence', False, 'runtime rehearsal remains non-qualifying')
    expect(runtime, 'rehearsalOnly', True, 'runtime rehearsal flag present')
    expect(partner, 'templateOnly', False, 'partner rehearsal templateOnly false')
    expect(partner, 'qualifiesAsLiveDeploymentEvidence', False, 'partner rehearsal remains non-qualifying')
    expect(partner, 'rehearsalOnly', True, 'partner rehearsal flag present')

    no_placeholders_runtime = not has_placeholder(runtime)
    checks['runtime rehearsal placeholders removed'] = 'PASS' if no_placeholders_runtime else 'FAIL'
    if not no_placeholders_runtime:
        issues.append('runtime rehearsal still has placeholders')

    no_placeholders_partner = not has_placeholder(partner)
    checks['partner rehearsal placeholders removed'] = 'PASS' if no_placeholders_partner else 'FAIL'
    if not no_placeholders_partner:
        issues.append('partner rehearsal still has placeholders')

    telemetry_nonempty = isinstance(partner.get('telemetryEvents'), list) and len(partner['telemetryEvents']) > 0
    checks['partner rehearsal telemetry present'] = 'PASS' if telemetry_nonempty else 'FAIL'
    if not telemetry_nonempty:
        issues.append('partner rehearsal missing telemetry events')

    live_still_zero = intake.get('summary', {}).get('packageStillMissingQualifyingLiveEvidence') is True
    checks['live intake lane still has zero qualifying evidence'] = 'PASS' if live_still_zero else 'FAIL'
    if not live_still_zero:
        issues.append('live intake lane unexpectedly reports qualifying evidence')

    results = {
        'evaluatedAt': now_iso(),
        'rehearsalRoot': '04_implementation_and_conformance/pilot_material/pilot_intake_rehearsal/',
        'rehearsalArtifacts': [
            '04_implementation_and_conformance/pilot_material/pilot_intake_rehearsal/runtime_surface_release_lane/OFARM_runtime_surface_live_deployment_evidence_rehearsal_v0_1.json',
            '04_implementation_and_conformance/pilot_material/pilot_intake_rehearsal/partner_output_channels/OFARM_runtime_surface_partner_output_telemetry_rehearsal_v0_1.json'
        ],
        'checks': checks,
        'summary': {
            'runtimeSurfaceRehearsalPackets': 1,
            'partnerOutputRehearsalPackets': 1,
            'sameStandardBridgeRehearsalPackets': 0,
            'qualifyingLiveEvidenceAddedByRehearsal': 0,
            'liveDropZonesRemainUnevidenced': live_still_zero,
        },
        'limitations': [
            'Rehearsal packets remain non-qualifying by design.',
            'Same-standard bridge rehearsal artifacts are intentionally absent.',
            'A real deployment artifact is still required before the readiness gate can change materially.'
        ],
        'overall': 'PASS_WITH_LIMITATIONS' if not issues else 'FAIL',
        'issues': issues,
    }
    dump_json(OUT, results)
    return 0 if not issues else 1


if __name__ == '__main__':
    raise SystemExit(main())
