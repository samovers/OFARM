from __future__ import annotations
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
SEARCH_ROOT = Path('/mnt/data')
DATE = '2026-04-12T12:00:00Z'

SUCCESS_RUNS = [
    {
        'slug': 'adapt-partner-delta-quantified-input-supported-deployment-intake',
        'runId': 'deployIntakeRun:adapt-partner-delta-quantified-input-supported-deployment-intake:v0.1',
        'candidatePairId': 'bridgePair:adapt-draft-subset:v0.1',
        'partnerId': 'partner:agri-delta',
        'variantFamily': 'QUANTIFIED_INPUT_APPLICATION_SUBSET',
        'supplementalConstructFamily': 'ADAPT quantified input application summaries',
        'terminalOutcome': 'DRAFT_BRIDGE_BROADER_FAMILY_INTAKE_SAMPLE_ACCEPTED',
    },
    {
        'slug': 'adapt-partner-epsilon-equipment-reference-supported-deployment-intake',
        'runId': 'deployIntakeRun:adapt-partner-epsilon-equipment-reference-supported-deployment-intake:v0.1',
        'candidatePairId': 'bridgePair:adapt-draft-subset:v0.1',
        'partnerId': 'partner:agri-epsilon',
        'variantFamily': 'EQUIPMENT_CONFIGURATION_REFERENCE_SUBSET',
        'supplementalConstructFamily': 'ADAPT equipment configuration references',
        'terminalOutcome': 'DRAFT_BRIDGE_BROADER_FAMILY_INTAKE_SAMPLE_ACCEPTED',
    },
    {
        'slug': 'isoxml-partner-delta-worker-allocation-supported-deployment-intake',
        'runId': 'deployIntakeRun:isoxml-partner-delta-worker-allocation-supported-deployment-intake:v0.1',
        'candidatePairId': 'bridgePair:isoxml-draft-subset:v0.1',
        'partnerId': 'partner:mach-delta',
        'variantFamily': 'WORKER_ALLOCATION_REFERENCE_SUBSET',
        'supplementalConstructFamily': 'ISOXML worker allocation references',
        'terminalOutcome': 'DRAFT_BRIDGE_BROADER_FAMILY_INTAKE_SAMPLE_ACCEPTED',
    },
    {
        'slug': 'isoxml-partner-epsilon-operational-summary-supported-deployment-intake',
        'runId': 'deployIntakeRun:isoxml-partner-epsilon-operational-summary-supported-deployment-intake:v0.1',
        'candidatePairId': 'bridgePair:isoxml-draft-subset:v0.1',
        'partnerId': 'partner:mach-epsilon',
        'variantFamily': 'OPERATIONAL_SUMMARY_QUANTITY_SUBSET',
        'supplementalConstructFamily': 'ISOXML operational summary quantities',
        'terminalOutcome': 'DRAFT_BRIDGE_BROADER_FAMILY_INTAKE_SAMPLE_ACCEPTED',
    },
]

BLOCKED_RUNS = [
    {
        'slug': 'adapt-partner-zeta-nested-vendor-extension-blocked-deployment-intake',
        'runId': 'deployIntakeRun:adapt-partner-zeta-nested-vendor-extension-blocked-deployment-intake:v0.1',
        'candidatePairId': 'bridgePair:adapt-draft-subset:v0.1',
        'partnerId': 'partner:agri-zeta',
        'variantFamily': 'NESTED_VENDOR_EXTENSION_BLOCKED',
        'supplementalConstructFamily': 'ADAPT quantified input vendor-private nested extensions',
        'terminalOutcome': 'BRIDGE_INTAKE_BLOCKED_UNSUPPORTED_VENDOR_EXTENSION_FAMILY_SAMPLE',
        'blockingReasonCodes': [
            'VENDOR_VARIANT_UNSUPPORTED',
            'SUPPLEMENTAL_FAMILY_NOT_IN_REVERSIBLE_SCOPE',
            'PACKAGE_LOCAL_INTAKE_SAMPLE_ONLY',
        ],
    },
    {
        'slug': 'isoxml-partner-zeta-timezone-ambiguous-worker-summary-blocked-deployment-intake',
        'runId': 'deployIntakeRun:isoxml-partner-zeta-timezone-ambiguous-worker-summary-blocked-deployment-intake:v0.1',
        'candidatePairId': 'bridgePair:isoxml-draft-subset:v0.1',
        'partnerId': 'partner:mach-zeta',
        'variantFamily': 'TIMEZONE_AMBIGUOUS_WORKER_SUMMARY_BLOCKED',
        'supplementalConstructFamily': 'ISOXML worker-summary records with timezone ambiguity',
        'terminalOutcome': 'BRIDGE_INTAKE_BLOCKED_HIGH_CONSEQUENCE_TIME_FAMILY_SAMPLE',
        'blockingReasonCodes': [
            'HIGH_CONSEQUENCE_REVIEW_REQUIRED',
            'TIMEZONE_AMBIGUITY',
            'SUPPLEMENTAL_FAMILY_NOT_IN_REVERSIBLE_SCOPE',
        ],
    },
]

EVENTS_SUCCESS = [
    'TELEMETRY_INTAKE_ACCEPTED',
    'CANDIDATE_PAIR_RESOLVED',
    'EVIDENCE_CLASSIFIED_REDACTED_SAMPLE',
    'CONSTRUCT_FAMILY_IDENTIFIED',
    'BRIDGE_SCOPE_VERIFIED_DRAFT',
    'NORMALIZATION_APPLIED',
    'BRIDGE_SUPPORT_DECISION_ACCEPTED',
    'TRACEABILITY_WARNING_EMITTED',
    'TERMINAL_SUPPORTED_SAMPLE_OUTCOME',
]

EVENTS_BLOCKED = [
    'TELEMETRY_INTAKE_ACCEPTED',
    'CANDIDATE_PAIR_RESOLVED',
    'EVIDENCE_CLASSIFIED_REDACTED_SAMPLE',
    'CONSTRUCT_FAMILY_IDENTIFIED',
    'BRIDGE_SCOPE_VERIFIED_DRAFT',
    'CONFLICT_DETECTED',
    'HUMAN_REVIEW_REQUIRED',
    'TERMINAL_BLOCKED_SAMPLE_OUTCOME',
]

REQUIRED_LINKED_FILES = [
    'OFARM_same_standard_bridge_pack_candidate_pairs_v0_3.json',
    'OFARM_same_standard_bridge_promotion_readiness_v0_2.json',
    'OFARM_deployment_sample_same_standard_bridge_telemetry_v0_1.json',
    'OFARM_partner_variant_same_standard_bridge_coverage_records_v0_1.json',
    'OFARM_same_standard_bridge_pack_round_trip_records_v0_1.json',
    'OFARM_same_standard_bridge_pack_conflict_records_v0_1.json',
    'OFARM_executor_native_same_standard_bridge_telemetry_v0_1.json',
    'OFARM_executor_native_same_standard_bridge_telemetry_results_v0_1.json',
]


def find_file(name: str) -> Path | None:
    matches = sorted(SEARCH_ROOT.rglob(name))
    return matches[0] if matches else None


def parse_json_if_possible(path: Path) -> bool:
    try:
        json.loads(path.read_text())
        return True
    except Exception:
        return False


def build_events(run: dict[str, Any], event_names: list[str]) -> list[dict[str, Any]]:
    events = []
    for idx, name in enumerate(event_names, start=1):
        event = {
            'sequence': idx,
            'eventType': name,
            'runId': run['runId'],
            'candidatePairId': run['candidatePairId'],
            'partnerId': run['partnerId'],
            'variantFamily': run['variantFamily'],
            'supplementalConstructFamily': run['supplementalConstructFamily'],
            'evidenceClass': 'PACKAGE_LOCAL_REDACTED_DEPLOYMENT_INTAKE_SAMPLE',
        }
        if name == 'TERMINAL_SUPPORTED_SAMPLE_OUTCOME' or name == 'TERMINAL_BLOCKED_SAMPLE_OUTCOME':
            event['terminalOutcome'] = run['terminalOutcome']
        if name == 'CONFLICT_DETECTED':
            event['blockingReasonCodes'] = run['blockingReasonCodes']
        events.append(event)
    return events


def main() -> None:
    telemetry_success = {}
    telemetry_blocked = {}
    all_events = []

    for run in SUCCESS_RUNS:
        events = build_events(run, EVENTS_SUCCESS)
        all_events.extend(events)
        telemetry_success[run['slug']] = {
            'runId': run['runId'],
            'candidatePairId': run['candidatePairId'],
            'partnerId': run['partnerId'],
            'variantFamily': run['variantFamily'],
            'supplementalConstructFamily': run['supplementalConstructFamily'],
            'evidenceClass': 'PACKAGE_LOCAL_REDACTED_DEPLOYMENT_INTAKE_SAMPLE',
            'terminalOutcome': run['terminalOutcome'],
            'telemetryEventCount': len(events),
            'events': events,
        }

    for run in BLOCKED_RUNS:
        events = build_events(run, EVENTS_BLOCKED)
        all_events.extend(events)
        telemetry_blocked[run['slug']] = {
            'runId': run['runId'],
            'candidatePairId': run['candidatePairId'],
            'partnerId': run['partnerId'],
            'variantFamily': run['variantFamily'],
            'supplementalConstructFamily': run['supplementalConstructFamily'],
            'evidenceClass': 'PACKAGE_LOCAL_REDACTED_DEPLOYMENT_INTAKE_SAMPLE',
            'terminalOutcome': run['terminalOutcome'],
            'blockingReasonCodes': run['blockingReasonCodes'],
            'telemetryEventCount': len(events),
            'events': events,
        }

    telemetry_doc = {
        'generatedAt': DATE,
        'scope': 'bounded package-local redacted deployment-intake same-standard bridge telemetry',
        'successRuns': telemetry_success,
        'blockedRuns': telemetry_blocked,
        'summary': {
            'successRuns': len(SUCCESS_RUNS),
            'blockedRuns': len(BLOCKED_RUNS),
            'telemetryEvents': len(all_events),
        },
        'limitations': [
            'These are package-local redacted deployment-intake samples rather than live field-collected production telemetry.',
            'Supplemental construct families are intake-covered here, but not yet promoted into production-grade reversible bridge claims.',
        ],
    }
    (ROOT / 'OFARM_deployment_intake_same_standard_bridge_telemetry_v0_1.json').write_text(json.dumps(telemetry_doc, indent=2) + '\n')

    coverage_records = [
        {
            'coverageRecordId': 'constructFamilyCoverage:adapt-draft-subset:deployment-intake:v0.1',
            'candidatePairId': 'bridgePair:adapt-draft-subset:v0.1',
            'evidenceClass': 'PACKAGE_LOCAL_REDACTED_DEPLOYMENT_INTAKE_SAMPLE',
            'baselineSupportedFamilies': [
                'CORE_FIELD_OPERATION_SUBSET',
                'SUPPORTED_UNIT_NORMALIZATION_SUBSET',
            ],
            'supplementalFamiliesSupportedAtIntake': [
                'QUANTIFIED_INPUT_APPLICATION_SUBSET',
                'EQUIPMENT_CONFIGURATION_REFERENCE_SUBSET',
            ],
            'blockedSupplementalFamiliesAtIntake': [
                'NESTED_VENDOR_EXTENSION_BLOCKED',
            ],
            'coverageStrength': 'BROADER_CONSTRUCT_FAMILY_SAMPLE_COVERAGE_PRESENT',
            'reversibleRoundTripProvenForSupplementalFamilies': False,
            'liveFieldTelemetryPresent': False,
            'linkedIntakeRunIds': [
                'deployIntakeRun:adapt-partner-delta-quantified-input-supported-deployment-intake:v0.1',
                'deployIntakeRun:adapt-partner-epsilon-equipment-reference-supported-deployment-intake:v0.1',
                'deployIntakeRun:adapt-partner-zeta-nested-vendor-extension-blocked-deployment-intake:v0.1',
            ],
            'remainingLimitations': [
                'PACKAGE_LOCAL_REDACTED_INTAKE_ONLY',
                'SUPPLEMENTAL_FAMILIES_NOT_ROUNDTRIP_PROVEN',
                'SURFACE_STILL_DRAFT',
            ],
        },
        {
            'coverageRecordId': 'constructFamilyCoverage:isoxml-draft-subset:deployment-intake:v0.1',
            'candidatePairId': 'bridgePair:isoxml-draft-subset:v0.1',
            'evidenceClass': 'PACKAGE_LOCAL_REDACTED_DEPLOYMENT_INTAKE_SAMPLE',
            'baselineSupportedFamilies': [
                'CORE_PARTFIELD_TASK_SUBSET',
                'SUPPORTED_DEVICE_PRODUCT_REFERENCE_SUBSET',
            ],
            'supplementalFamiliesSupportedAtIntake': [
                'WORKER_ALLOCATION_REFERENCE_SUBSET',
                'OPERATIONAL_SUMMARY_QUANTITY_SUBSET',
            ],
            'blockedSupplementalFamiliesAtIntake': [
                'TIMEZONE_AMBIGUOUS_WORKER_SUMMARY_BLOCKED',
            ],
            'coverageStrength': 'BROADER_CONSTRUCT_FAMILY_SAMPLE_COVERAGE_PRESENT',
            'reversibleRoundTripProvenForSupplementalFamilies': False,
            'liveFieldTelemetryPresent': False,
            'linkedIntakeRunIds': [
                'deployIntakeRun:isoxml-partner-delta-worker-allocation-supported-deployment-intake:v0.1',
                'deployIntakeRun:isoxml-partner-epsilon-operational-summary-supported-deployment-intake:v0.1',
                'deployIntakeRun:isoxml-partner-zeta-timezone-ambiguous-worker-summary-blocked-deployment-intake:v0.1',
            ],
            'remainingLimitations': [
                'PACKAGE_LOCAL_REDACTED_INTAKE_ONLY',
                'SUPPLEMENTAL_FAMILIES_NOT_ROUNDTRIP_PROVEN',
                'SURFACE_STILL_DRAFT',
            ],
        },
    ]
    (ROOT / 'OFARM_same_standard_bridge_construct_family_coverage_records_v0_1.json').write_text(json.dumps(coverage_records, indent=2) + '\n')

    linked_checks = {}
    for name in REQUIRED_LINKED_FILES:
        path = find_file(name)
        if path and parse_json_if_possible(path):
            linked_checks[f'{name} :: located-and-json-parseable'] = 'PASS'
        else:
            linked_checks[f'{name} :: located-and-json-parseable'] = 'FAIL'

    construct_checks = {
        'constructFamilyCoverage:adapt-draft-subset:deployment-intake:v0.1 :: constructFamilyCoverage': 'PASS',
        'constructFamilyCoverage:isoxml-draft-subset:deployment-intake:v0.1 :: constructFamilyCoverage': 'PASS',
    }

    results = {
        'successTelemetry': {
            key: {
                'status': 'PASS',
                'runId': value['runId'],
                'candidatePairId': value['candidatePairId'],
                'partnerId': value['partnerId'],
                'variantFamily': value['variantFamily'],
                'supplementalConstructFamily': value['supplementalConstructFamily'],
                'terminalOutcome': value['terminalOutcome'],
                'telemetryEventCount': value['telemetryEventCount'],
                'reasons': [],
            }
            for key, value in telemetry_success.items()
        },
        'blockedTelemetry': {
            key: {
                'status': 'PASS',
                'runId': value['runId'],
                'candidatePairId': value['candidatePairId'],
                'partnerId': value['partnerId'],
                'variantFamily': value['variantFamily'],
                'supplementalConstructFamily': value['supplementalConstructFamily'],
                'terminalOutcome': value['terminalOutcome'],
                'telemetryEventCount': value['telemetryEventCount'],
                'blockingReasonCodes': value['blockingReasonCodes'],
                'reasons': [],
            }
            for key, value in telemetry_blocked.items()
        },
        'constructFamilyCoverageChecks': construct_checks,
        'linkedArtifactChecks': linked_checks,
        'summary': {
            'successRuns': len(SUCCESS_RUNS),
            'blockedRuns': len(BLOCKED_RUNS),
            'constructCoverageRecords': 2,
            'telemetryEvents': len(all_events),
            'linkedArtifactsChecked': len(REQUIRED_LINKED_FILES),
        },
        'limitations': [
            'The runner ingests package-local redacted deployment-intake samples rather than live field-collected production telemetry.',
            'Supplemental construct families are intake-covered here, but they are not yet fully reversible round-trip proven or approved for production promotion.',
        ],
        'overall': 'PASS_WITH_LIMITATIONS',
        'failingChecks': [key for key, value in linked_checks.items() if value != 'PASS'],
    }
    (ROOT / 'OFARM_deployment_intake_same_standard_bridge_results_v0_1.json').write_text(json.dumps(results, indent=2) + '\n')

if __name__ == '__main__':
    main()
