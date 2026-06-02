#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMPL = ROOT / '04_implementation_and_conformance'
MC = ROOT / '03_machine_contracts'

DECISION_MATRIX = IMPL / 'OFARM_partner_output_surface_governance_decision_matrix_v0_1.json'
LINKAGE = IMPL / 'OFARM_runtime_surface_partner_output_telemetry_linkage_v0_2.json'
TELEMETRY = IMPL / 'OFARM_runtime_deployment_emitted_publication_telemetry_v0_1.json'
TRACEBACK = IMPL / 'OFARM_runtime_partner_surface_publication_trace_back_records_v0_1.json'
MANIFEST = MC / 'OFARM_Capability_Manifest_example_core_deployment_surface_linkage_v0_2_draft.json'
RESULTS = IMPL / 'OFARM_partner_output_surface_governance_boundary_results_v0_1.json'


def load_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def main() -> int:
    decision_matrix = load_json(DECISION_MATRIX)
    linkage = load_json(LINKAGE)
    telemetry = load_json(TELEMETRY)
    tracebacks = load_json(TRACEBACK)
    manifest = load_json(MANIFEST)

    checks: list[dict[str, str]] = []
    overall = 'PASS_WITH_LIMITATIONS'

    decisions = {row['partnerSurface']: row for row in decision_matrix['decisions']}
    summaries = {row['partnerSurface']: row for row in linkage['surfaceSummaries']}
    telemetry_counts = Counter(event['partnerSurface'] for event in telemetry['events'])
    traceback_counts = Counter(row['partnerSurface'] for row in tracebacks)

    def record(check_id: str, ok: bool, detail: str) -> None:
        checks.append({
            'checkId': check_id,
            'status': 'PASS' if ok else 'FAIL',
            'detail': detail,
        })

    # Top-level consistency
    record(
        'decision-matrix-linkage-ref',
        linkage.get('decisionMatrixRef') == '04_implementation_and_conformance/conformance_runners/authority_and_governance_conformance/OFARM_partner_output_surface_governance_decision_matrix_v0_1.json',
        'linkage summary should point at the explicit partner-output governance decision matrix',
    )
    record(
        'surface-set-match',
        set(decisions) == set(summaries) == set(telemetry_counts) == set(traceback_counts),
        'decision matrix, linkage summary, telemetry, and trace-back records should cover the same partner surfaces',
    )

    manifest_surfaces = {row['targetRef'] for row in manifest['capabilitySections']['importExportSupport']['declaredSurfaces']}
    manifest_contracts = {
        row['contractRef']
        for row in manifest['capabilitySections']['importExportSupport']['declaredSurfaces']
        if row.get('contractRef')
    }

    runtime_surface_examples = []
    for path in MC.glob('OFARM_RuntimeSurfaceContract_example_*.json'):
        try:
            runtime_surface_examples.append(load_json(path))
        except Exception:
            pass
    all_surface_identity_refs = {row.get('surfaceIdentityRef') for row in runtime_surface_examples if isinstance(row, dict)}
    all_contract_ids = {row.get('contractId') for row in runtime_surface_examples if isinstance(row, dict)}

    for partner_surface, decision in sorted(decisions.items()):
        summary = summaries[partner_surface]
        record(
            f'telemetry-count:{partner_surface}',
            summary['telemetryEventCount'] == telemetry_counts[partner_surface],
            'telemetry event count must match source publication telemetry',
        )
        record(
            f'traceback-count:{partner_surface}',
            summary['traceBackCount'] == traceback_counts[partner_surface],
            'trace-back count must match source trace-back records',
        )
        record(
            f'governance-decision-copy:{partner_surface}',
            summary.get('governanceDecision') == decision['decision'] and summary.get('governanceDecisionRef') == decision['decisionId'],
            'linkage summary should carry the explicit governance decision for the partner surface',
        )
        record(
            f'nonlive-telemetry:{partner_surface}',
            summary['telemetryQualification'] == 'PACKAGE_LOCAL_RUNTIME_EMITTED_NOT_LIVE_EVIDENCE',
            'partner-output telemetry must remain explicitly non-live in this package-local lane',
        )

        if decision['decision'] == 'ALREADY_GOVERNED_RUNTIME_SURFACE':
            ok = (
                summary['governedSurfaceIdentityRef'] == decision['governedSurfaceIdentityRef']
                and summary['surfaceContractRef'] == decision['contractRef']
                and summary['manifestTargetRef'] == decision['manifestTargetRef']
                and summary['modeledInReleaseBundle'] is True
                and decision['governedSurfaceIdentityRef'] in all_surface_identity_refs
                and decision['contractRef'] in all_contract_ids
                and (
                    decision['governedSurfaceIdentityRef'] in manifest_surfaces
                    or decision['manifestTargetRef'] in manifest_surfaces
                )
                and decision['contractRef'] in manifest_contracts
            )
            record(
                f'governed-runtime-surface:{partner_surface}',
                ok,
                'already-governed partner export should resolve to a manifest/runtime-surface lane and concrete runtime-surface example',
            )
        else:
            ok = (
                summary['governedSurfaceIdentityRef'] is None
                and summary['surfaceContractRef'] is None
                and summary['manifestTargetRef'] is None
                and summary['modeledInReleaseBundle'] is False
                and decision['adapterSurfaceRef'] not in all_surface_identity_refs
                and decision['adapterSurfaceRef'] not in manifest_surfaces
            )
            record(
                f'implementation-local-retained:{partner_surface}',
                ok,
                'implementation-local partner-output channels should stay out of the governed manifest/runtime-surface lane in the current package',
            )
            record(
                f'future-promotion-conditions:{partner_surface}',
                len(decision.get('futurePromotionConditions', [])) > 0,
                'retained implementation-local channels should carry explicit future-promotion conditions rather than silent ambiguity',
            )

    # Specific threshold-sensitive rule for submission XML.
    sub = decisions['PARTNER_SUBMISSION_XML']
    record(
        'submission-xml-threshold-explicit',
        'ESTABLISH_FORMAL_FILING_GATEWAY_OR_DELIVERY_NAMESPACE' in sub.get('futurePromotionConditions', []),
        'submission XML should stay implementation-local in the current package while still carrying an explicit future filing-gateway promotion condition',
    )

    result = {
        'metadata': {
            'runner': Path(__file__).name,
            'scope': 'partner-output governance boundary and explicit retention-versus-promotion posture for the current package',
        },
        'checks': checks,
        'overall': overall,
        'limitations': [
            'This runner validates package-local decision posture only; it does not prove live deployment evidence or future external partner contracts.',
            'The current package keeps partner-output channel governance explicit without adding new active machine-contract families.'
        ],
    }
    RESULTS.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    if any(check['status'] == 'FAIL' for check in checks):
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
