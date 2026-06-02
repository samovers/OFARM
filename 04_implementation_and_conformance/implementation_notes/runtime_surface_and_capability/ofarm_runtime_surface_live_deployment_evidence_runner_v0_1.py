#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MC = ROOT / '03_machine_contracts'
IMPL = Path(__file__).resolve().parent

BUNDLE = IMPL / 'OFARM_runtime_surface_deployment_release_bundle_example_core_surface_linkage_v0_1.json'
MANIFEST = MC / 'OFARM_Capability_Manifest_example_core_deployment_surface_linkage_v0_2_draft.json'
ACTIVE = MC / 'OFARM_ActiveArtifactSet_example_core_deployment_surface_linkage_v0_1.json'
CLAIMSET = MC / 'OFARM_ConformanceClaimSet_example_core_deployment_surface_linkage_v0_1.json'
PUB_TELEMETRY = IMPL / 'OFARM_runtime_deployment_emitted_publication_telemetry_v0_1.json'
TRACEBACK = IMPL / 'OFARM_runtime_partner_surface_publication_trace_back_records_v0_1.json'
GATE_SEQUENCE = IMPL / 'OFARM_runtime_deployment_emitted_publication_gate_sequence_records_v0_1.json'
RELEASE_RESULTS = IMPL / 'OFARM_runtime_surface_deployment_release_traceability_results_v0_1.json'
SURFACE_TEMPLATE = IMPL / 'OFARM_runtime_surface_live_deployment_evidence_capture_template_v0_1.json'
PARTNER_TEMPLATE = IMPL / 'OFARM_runtime_surface_partner_output_telemetry_capture_template_v0_1.json'
REGISTRY_OUT = IMPL / 'OFARM_runtime_surface_live_deployment_evidence_registry_v0_1.json'
LINKAGE_OUT = IMPL / 'OFARM_runtime_surface_partner_output_telemetry_linkage_v0_1.json'
RESULTS_OUT = IMPL / 'OFARM_runtime_surface_live_deployment_evidence_results_v0_1.json'


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding='utf-8'))


def dump_json(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, indent=2) + '\n', encoding='utf-8')


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def main() -> int:
    bundle = load_json(BUNDLE)
    manifest = load_json(MANIFEST)
    active = load_json(ACTIVE)
    claimset = load_json(CLAIMSET)
    telemetry = load_json(PUB_TELEMETRY)
    traces = load_json(TRACEBACK)
    gate_sequences = load_json(GATE_SEQUENCE)
    release_results = load_json(RELEASE_RESULTS)
    surface_template = load_json(SURFACE_TEMPLATE)
    partner_template = load_json(PARTNER_TEMPLATE)

    contract_examples: dict[str, dict[str, Any]] = {}
    for path in MC.glob('OFARM_RuntimeSurfaceContract_example_*v0_2_draft.json'):
        payload = load_json(path)
        contract_examples[payload['contractId']] = payload

    rows = [row for row in manifest['capabilitySections']['importExportSupport']['declaredSurfaces'] if row.get('contractRef')]
    row_by_contract = {row['contractRef']: row for row in rows}
    bundle_by_contract = {entry['surfaceContractRef']: entry for entry in bundle['surfaceReleases']}

    release_surface_status: list[dict[str, Any]] = []
    for entry in bundle['surfaceReleases']:
        contract_ref = entry['surfaceContractRef']
        contract = contract_examples.get(contract_ref, {})
        live_posture = entry['releasePosture'] in {'LIVE_SUPPORTED', 'LIVE_PARTIAL'}
        release_surface_status.append({
            'surfaceContractRef': contract_ref,
            'surfaceIdentityRef': entry['surfaceIdentityRef'],
            'manifestTargetRef': entry['manifestTargetRef'],
            'manifestSurfaceStatus': entry['manifestSurfaceStatus'],
            'releasePosture': entry['releasePosture'],
            'serviceDescriptionRefs': entry.get('serviceDescriptionRefs', []),
            'evidenceEligibility': 'ELIGIBLE_WHEN_DEPLOYED' if live_posture else 'PREVIEW_ONLY_NOT_ELIGIBLE',
            'currentEvidenceStatus': 'NOT_COLLECTED' if live_posture else 'PREVIEW_ONLY_NO_CAPTURE',
            'captureTemplateRef': rel(SURFACE_TEMPLATE) if live_posture else None,
            'surfaceBinding': contract.get('surfaceBinding'),
            'notes': 'Live-posture surface is capture-ready but no qualifying live deployment evidence is present yet.' if live_posture else 'Preview-only surface remains ineligible for a live-evidence claim in the current release lane.',
        })

    events_by_surface: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for event in telemetry['events']:
        events_by_surface[event['partnerSurface']].append(event)

    traces_by_surface: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for trace in traces:
        traces_by_surface[trace['partnerSurface']].append(trace)

    governed_partner_mapping = {
        'NGSI_LD_PARTNER_EXPORT': {
            'surfaceContractRef': 'surface-contract:ngsi-ld-export:v0.2-draft',
            'governedSurfaceIdentityRef': 'surface:ngsi-ld-export:v1',
            'manifestTargetRef': 'mapping:ngsi-ld-export:v1',
        }
    }

    partner_summaries: list[dict[str, Any]] = []
    all_partner_surfaces = sorted(set(events_by_surface) | set(traces_by_surface))
    for partner_surface in all_partner_surfaces:
        events = events_by_surface.get(partner_surface, [])
        surface_traces = traces_by_surface.get(partner_surface, [])
        adapter_refs = sorted({trace.get('adapterSurfaceRef') for trace in surface_traces if trace.get('adapterSurfaceRef')})
        family_set = sorted({trace.get('outputFamily') for trace in surface_traces if trace.get('outputFamily')})
        subtype_set = sorted({trace.get('outputSubtype') for trace in surface_traces if trace.get('outputSubtype')})
        outcome_counts = dict(sorted(Counter(trace.get('finalOutcome') for trace in surface_traces).items()))
        scenario_ids = sorted({event.get('scenarioId') for event in events if event.get('scenarioId')} | {trace.get('scenarioId') for trace in surface_traces if trace.get('scenarioId')})
        mapping = governed_partner_mapping.get(partner_surface)
        modeled = mapping is not None
        summary = {
            'partnerSurface': partner_surface,
            'adapterSurfaceRef': adapter_refs[0] if len(adapter_refs) == 1 else adapter_refs,
            'governedSurfaceIdentityRef': mapping['governedSurfaceIdentityRef'] if mapping else None,
            'surfaceContractRef': mapping['surfaceContractRef'] if mapping else None,
            'manifestTargetRef': mapping['manifestTargetRef'] if mapping else None,
            'modeledInReleaseBundle': modeled,
            'releasePosture': bundle_by_contract[mapping['surfaceContractRef']]['releasePosture'] if modeled else None,
            'telemetryEventCount': len(events),
            'traceBackCount': len(surface_traces),
            'linkedScenarioIds': scenario_ids,
            'outputFamilies': family_set,
            'outputSubtypes': subtype_set,
            'finalOutcomeCounts': outcome_counts,
            'telemetryQualification': 'PACKAGE_LOCAL_RUNTIME_EMITTED_NOT_LIVE_EVIDENCE',
            'modelingGapPosture': None if modeled else 'PARTNER_OUTPUT_SURFACE_PENDING_GOVERNED_RUNTIME_SURFACE',
        }
        partner_summaries.append(summary)

    linkage = {
        'linkageVersion': 'ofarm.runtimesurface.partneroutputtelemetry.linkage.v0.1.impl',
        'linkageId': 'linkage:runtime-surface-partner-output-telemetry:core-surface-linkage:v1',
        'generatedAt': now_iso(),
        'releaseBundleRef': bundle['releaseBundleId'],
        'releaseLabel': bundle['releaseLabel'],
        'deploymentScope': bundle['deploymentScope'],
        'sourceTelemetryArtifactRef': rel(PUB_TELEMETRY),
        'sourceTraceBackArtifactRef': rel(TRACEBACK),
        'surfaceSummaries': partner_summaries,
        'notes': 'Aggregated partner-output telemetry linkage for the bounded release lane. Only the NGSI-LD publication surface is already bound to a governed runtime-surface draft contract in the current release lane; the remaining partner-output surfaces stay explicit as implementation-local support identities.'
    }

    nonqualifying = [
        {
            'artifactRef': rel(BUNDLE),
            'evidenceClass': 'PACKAGE_LOCAL_RELEASE_TRACEABILITY_FIXTURE',
            'qualifiesAsLiveDeploymentEvidence': False,
            'reasonCode': 'PACKAGE_LOCAL_FIXTURE_ONLY',
        },
        {
            'artifactRef': '04_implementation_and_conformance/service_and_sdk_candidates/service_descriptions/core_surface_linkage_release_v0_1/service_description_catalog_v0_2.json',
            'evidenceClass': 'PACKAGE_LOCAL_SERVICE_DESCRIPTION_CATALOG',
            'qualifiesAsLiveDeploymentEvidence': False,
            'reasonCode': 'PACKAGE_LOCAL_FIXTURE_ONLY',
        },
        {
            'artifactRef': rel(PUB_TELEMETRY),
            'evidenceClass': 'RUNTIME_EMITTED_PACKAGE_LOCAL_OUTPUT_TELEMETRY',
            'qualifiesAsLiveDeploymentEvidence': False,
            'reasonCode': 'PACKAGE_LOCAL_RUNTIME_EMITTED_NOT_LIVE',
        },
        {
            'artifactRef': rel(TRACEBACK),
            'evidenceClass': 'RUNTIME_EMITTED_PACKAGE_LOCAL_TRACEBACK',
            'qualifiesAsLiveDeploymentEvidence': False,
            'reasonCode': 'PACKAGE_LOCAL_RUNTIME_EMITTED_NOT_LIVE',
        },
        {
            'artifactRef': rel(GATE_SEQUENCE),
            'evidenceClass': 'RUNTIME_EMITTED_PACKAGE_LOCAL_GATE_SEQUENCE',
            'qualifiesAsLiveDeploymentEvidence': False,
            'reasonCode': 'PACKAGE_LOCAL_RUNTIME_EMITTED_NOT_LIVE',
        },
    ]

    partner_capture_status: list[dict[str, Any]] = []
    for summary in partner_summaries:
        modeled = bool(summary['modeledInReleaseBundle'])
        partner_capture_status.append({
            'partnerSurface': summary['partnerSurface'],
            'adapterSurfaceRef': summary['adapterSurfaceRef'],
            'governedSurfaceIdentityRef': summary['governedSurfaceIdentityRef'],
            'surfaceContractRef': summary['surfaceContractRef'],
            'currentEvidenceStatus': 'PACKAGE_LOCAL_RUNTIME_EMITTED_NON_QUALIFYING',
            'captureEligibility': 'ELIGIBLE_WHEN_DEPLOYMENT_COLLECTION_EXISTS' if modeled else 'SUPPORT_ONLY_PENDING_GOVERNED_SURFACE_DECISION',
            'captureTemplateRef': rel(PARTNER_TEMPLATE),
            'telemetryEventCount': summary['telemetryEventCount'],
            'traceBackCount': summary['traceBackCount'],
        })

    registry = {
        'registryVersion': 'ofarm.runtimesurface.liveevidence.registry.v0.1.impl',
        'registryId': 'registry:runtime-surface-live-evidence:core-surface-linkage:v1',
        'generatedAt': now_iso(),
        'templateOnly': False,
        'qualifiesAsLiveDeploymentEvidence': False,
        'evidencePosture': 'CAPTURE_READY_NOT_COLLECTED',
        'releaseBundleRef': bundle['releaseBundleId'],
        'releaseLabel': bundle['releaseLabel'],
        'manifestRef': bundle['manifestRef'],
        'activeArtifactSetRef': bundle['activeArtifactSetRef'],
        'conformanceClaimSetRef': bundle['conformanceClaimSetRef'],
        'deploymentScope': bundle['deploymentScope'],
        'captureTemplateRefs': [rel(SURFACE_TEMPLATE), rel(PARTNER_TEMPLATE)],
        'partnerOutputTelemetryLinkageRef': rel(LINKAGE_OUT),
        'qualifyingLiveDeploymentEvidenceCount': 0,
        'releaseSurfaceEvidenceStatus': release_surface_status,
        'partnerOutputTelemetryCaptureStatus': partner_capture_status,
        'nonQualifyingSupportArtifacts': nonqualifying,
        'notes': 'Capture-ready registry only. The current package-local artifacts remain non-qualifying support evidence until replaced later by real deployment-collected evidence.'
    }

    dump_json(LINKAGE_OUT, linkage)
    dump_json(REGISTRY_OUT, registry)

    checks: list[dict[str, str]] = []
    failures: list[str] = []

    def record(check_id: str, ok: bool, detail: str) -> None:
        checks.append({'checkId': check_id, 'status': 'PASS' if ok else 'FAIL', 'detail': detail})
        if not ok:
            failures.append(f'{check_id}: {detail}')

    record('surface-template-flag', surface_template.get('templateOnly') is True and surface_template.get('qualifiesAsLiveDeploymentEvidence') is False, 'runtime-surface evidence template must stay template-only and non-qualifying')
    record('partner-template-flag', partner_template.get('templateOnly') is True and partner_template.get('qualifiesAsLiveDeploymentEvidence') is False, 'partner-output telemetry template must stay template-only and non-qualifying')
    record('release-traceability-still-passing', release_results.get('overall') == 'PASS_WITH_LIMITATIONS', 'previous release-traceability lane should still be passing with explicit limitations')
    record('registry-release-bundle-ref', registry['releaseBundleRef'] == bundle['releaseBundleId'], 'registry must resolve to the linked release bundle')
    record('registry-manifest-ref', registry['manifestRef'] == manifest['manifestId'], 'registry must resolve to the linked manifest example')
    record('registry-active-artifact-set-ref', registry['activeArtifactSetRef'] == active['activeArtifactSetId'], 'registry must resolve to the linked ActiveArtifactSet')
    record('registry-claimset-ref', registry['conformanceClaimSetRef'] == claimset['claimSetId'], 'registry must resolve to the linked ConformanceClaimSet')
    record('registry-scope-match', registry['deploymentScope'] == bundle['deploymentScope'] == manifest['deploymentScope'] == active['deploymentScope'], 'registry deployment scope must match release-bundle, manifest, and ActiveArtifactSet scope')
    record('registry-qualifying-count-zero', registry['qualifyingLiveDeploymentEvidenceCount'] == 0 and registry['qualifiesAsLiveDeploymentEvidence'] is False, 'registry must stay capture-ready and claim zero qualifying live deployment evidence')
    record('release-surface-status-count', len(registry['releaseSurfaceEvidenceStatus']) == len(bundle['surfaceReleases']), 'registry should include one release-surface evidence status row per bundle surface release')

    for entry in registry['releaseSurfaceEvidenceStatus']:
        live = entry['releasePosture'] in {'LIVE_SUPPORTED', 'LIVE_PARTIAL'}
        record(f'release-surface-eligibility:{entry["surfaceContractRef"]}', entry['evidenceEligibility'] == ('ELIGIBLE_WHEN_DEPLOYED' if live else 'PREVIEW_ONLY_NOT_ELIGIBLE'), 'release-surface evidence eligibility must follow release posture')
        record(f'release-surface-status:{entry["surfaceContractRef"]}', entry['currentEvidenceStatus'] == ('NOT_COLLECTED' if live else 'PREVIEW_ONLY_NO_CAPTURE'), 'release-surface evidence status must stay explicit for live vs preview surfaces')
        record(f'release-surface-template:{entry["surfaceContractRef"]}', (entry['captureTemplateRef'] == rel(SURFACE_TEMPLATE)) if live else (entry['captureTemplateRef'] is None), 'only live-posture surfaces should point at the runtime-surface capture template')

    record('partner-summary-count', len(linkage['surfaceSummaries']) == len(all_partner_surfaces), 'partner-output telemetry linkage should include one summary per observed partner surface')
    for summary in linkage['surfaceSummaries']:
        partner_surface = summary['partnerSurface']
        record(f'partner-event-count:{partner_surface}', summary['telemetryEventCount'] == len(events_by_surface[partner_surface]), 'telemetry event count must match source publication telemetry')
        record(f'partner-trace-count:{partner_surface}', summary['traceBackCount'] == len(traces_by_surface[partner_surface]), 'trace-back count must match source trace-back records')
        record(f'partner-nonlive-posture:{partner_surface}', summary['telemetryQualification'] == 'PACKAGE_LOCAL_RUNTIME_EMITTED_NOT_LIVE_EVIDENCE', 'partner-output telemetry summary must stay explicitly non-live')
        if partner_surface == 'NGSI_LD_PARTNER_EXPORT':
            record('ngsi-governed-link', summary['modeledInReleaseBundle'] is True and summary['surfaceContractRef'] in bundle_by_contract and bundle_by_contract[summary['surfaceContractRef']]['surfaceIdentityRef'] == summary['governedSurfaceIdentityRef'], 'NGSI-LD partner telemetry must resolve to the governed runtime-surface release lane')
        else:
            record(f'partner-gap-explicit:{partner_surface}', summary['modeledInReleaseBundle'] is False and summary['surfaceContractRef'] is None and summary['governedSurfaceIdentityRef'] is None and summary['modelingGapPosture'] == 'PARTNER_OUTPUT_SURFACE_PENDING_GOVERNED_RUNTIME_SURFACE', 'unmodeled partner surfaces must stay explicit as implementation-local support identities')

    record('nonqualifying-artifact-count', len(registry['nonQualifyingSupportArtifacts']) >= 5, 'registry should explicitly list the non-qualifying package-local support artifacts for this lane')
    for item in registry['nonQualifyingSupportArtifacts']:
        path = ROOT / item['artifactRef']
        record(f'nonqualifying-path:{item["artifactRef"]}', path.exists(), 'listed non-qualifying support artifact must exist in the package')
        record(f'nonqualifying-flag:{item["artifactRef"]}', item['qualifiesAsLiveDeploymentEvidence'] is False, 'listed support artifact must stay explicitly non-qualifying')

    results = {
        'metadata': {
            'runner': Path(__file__).name,
            'scope': 'runtime-surface live deployment evidence capture readiness and partner-output telemetry linkage',
        },
        'checks': checks,
        'summary': {
            'releaseSurfaceCount': len(registry['releaseSurfaceEvidenceStatus']),
            'partnerSurfaceCount': len(linkage['surfaceSummaries']),
            'telemetryEventCount': len(telemetry['events']),
            'traceBackCount': len(traces),
            'gateSequenceCount': len(gate_sequences),
            'qualifyingLiveDeploymentEvidenceCount': registry['qualifyingLiveDeploymentEvidenceCount'],
        },
        'limitations': [
            'The package still contains zero qualifying live deployment evidence for the runtime-surface release lane.',
            'Only the NGSI-LD publication surface is already modeled in the current governed runtime-surface release lane; other partner-output surfaces remain implementation-local support identities.',
            'The current publication telemetry and trace-back records are runtime-emitted package-local support evidence, not deployment-collected live evidence.'
        ],
        'overall': 'PASS_WITH_LIMITATIONS' if not failures else 'FAIL',
        'failingChecks': failures,
    }
    dump_json(RESULTS_OUT, results)
    return 0 if not failures else 1


if __name__ == '__main__':
    raise SystemExit(main())
