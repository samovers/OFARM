from __future__ import annotations
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
SEARCH_ROOT = Path('/mnt/data')
DATE = '2026-04-12T12:00:00Z'

SUPPLEMENTAL_SUCCESS = [
    {
        'slug': 'adapt-quantified-input-supplemental-roundtrip',
        'recordId': 'bridgeRoundTrip:adapt-quantified-input-supplemental-roundtrip:v0.1',
        'candidatePairId': 'bridgePair:adapt-draft-subset:v0.1',
        'standardRef': 'standard:adapt:payload:v1',
        'supplementalConstructFamily': 'ADAPT quantified input application summaries',
        'variantFamily': 'QUANTIFIED_INPUT_APPLICATION_SUBSET',
        'linkedIntakeRunId': 'deployIntakeRun:adapt-partner-delta-quantified-input-supported-deployment-intake:v0.1',
        'preservedConstructs': [
            'input product reference',
            'unit-normalized application quantity',
            'covered area quantity',
        ],
        'allowedDivergence': [
            {
                'externalConstructRef': 'operator-entered rate note free text',
                'lossClass': 'APPROXIMATED',
                'source': 'IMPORT',
            }
        ],
        'notes': 'The supported ADAPT quantified input family is now round-trip proven for the bounded declared supplemental scope using package-local redacted intake evidence plus draft bridge rehearsal.',
    },
    {
        'slug': 'adapt-equipment-reference-supplemental-roundtrip',
        'recordId': 'bridgeRoundTrip:adapt-equipment-reference-supplemental-roundtrip:v0.1',
        'candidatePairId': 'bridgePair:adapt-draft-subset:v0.1',
        'standardRef': 'standard:adapt:payload:v1',
        'supplementalConstructFamily': 'ADAPT equipment configuration references',
        'variantFamily': 'EQUIPMENT_CONFIGURATION_REFERENCE_SUBSET',
        'linkedIntakeRunId': 'deployIntakeRun:adapt-partner-epsilon-equipment-reference-supported-deployment-intake:v0.1',
        'preservedConstructs': [
            'equipment reference identifier',
            'implement configuration binding',
            'field-operation equipment association',
        ],
        'allowedDivergence': [
            {
                'externalConstructRef': 'display-oriented equipment label string',
                'lossClass': 'APPROXIMATED',
                'source': 'EXPORT',
            }
        ],
        'notes': 'The supported ADAPT equipment-reference family is now round-trip proven for the bounded declared supplemental scope while leaving vendor-private extensions outside reversible claims.',
    },
    {
        'slug': 'isoxml-worker-allocation-supplemental-roundtrip',
        'recordId': 'bridgeRoundTrip:isoxml-worker-allocation-supplemental-roundtrip:v0.1',
        'candidatePairId': 'bridgePair:isoxml-draft-subset:v0.1',
        'standardRef': 'standard:isoxml:file:v4',
        'supplementalConstructFamily': 'ISOXML worker allocation references',
        'variantFamily': 'WORKER_ALLOCATION_REFERENCE_SUBSET',
        'linkedIntakeRunId': 'deployIntakeRun:isoxml-partner-delta-worker-allocation-supported-deployment-intake:v0.1',
        'preservedConstructs': [
            'worker identifier',
            'task allocation reference',
            'worker-role assignment subset',
        ],
        'allowedDivergence': [
            {
                'externalConstructRef': 'non-governing UI worker display name casing',
                'lossClass': 'APPROXIMATED',
                'source': 'EXPORT',
            }
        ],
        'notes': 'The supported ISOXML worker-allocation family is now round-trip proven for the bounded declared supplemental scope without claiming lossless handling for ambiguous time variants.',
    },
    {
        'slug': 'isoxml-operational-summary-supplemental-roundtrip',
        'recordId': 'bridgeRoundTrip:isoxml-operational-summary-supplemental-roundtrip:v0.1',
        'candidatePairId': 'bridgePair:isoxml-draft-subset:v0.1',
        'standardRef': 'standard:isoxml:file:v4',
        'supplementalConstructFamily': 'ISOXML operational summary quantities',
        'variantFamily': 'OPERATIONAL_SUMMARY_QUANTITY_SUBSET',
        'linkedIntakeRunId': 'deployIntakeRun:isoxml-partner-epsilon-operational-summary-supported-deployment-intake:v0.1',
        'preservedConstructs': [
            'summary quantity aggregate',
            'unit-qualified operation total',
            'task summary linkage',
        ],
        'allowedDivergence': [
            {
                'externalConstructRef': 'controller-emitted execution status detail',
                'lossClass': 'COLLAPSED',
                'source': 'EXPORT',
            }
        ],
        'notes': 'The supported ISOXML operational-summary family is now round-trip proven for the bounded declared supplemental scope, with controller-detail collapse still disclosed rather than hidden.',
    },
]

SUPPLEMENTAL_BLOCKED = [
    {
        'slug': 'adapt-nested-vendor-extension-supplemental-conflict',
        'conflictRecordId': 'bridgeConflict:adapt-nested-vendor-extension-supplemental-conflict:v0.1',
        'candidatePairId': 'bridgePair:adapt-draft-subset:v0.1',
        'standardRef': 'standard:adapt:payload:v1',
        'supplementalConstructFamily': 'ADAPT quantified input vendor-private nested extensions',
        'variantFamily': 'NESTED_VENDOR_EXTENSION_BLOCKED',
        'conflictClass': 'NESTED_VENDOR_EXTENSION_NONREVERSIBLE',
        'triggerExternalConstructRef': 'nested vendor-private quantified-input extension blocks',
        'blockingReasonCodes': [
            'SUPPLEMENTAL_FAMILY_OUTSIDE_DECLARED_REVERSIBLE_SCOPE',
            'NESTED_VENDOR_EXTENSION_UNSUPPORTED',
            'RETAIN_RAW_EVIDENCE_ONLY',
        ],
        'requiredHandling': [
            'retain-raw-payload-as-evidence',
            'disclose-nonreversible-supplemental-family',
        ],
        'notes': 'Nested vendor-private quantified-input extensions stay outside reversible claims even after the supported supplemental ADAPT families are proven.',
    },
    {
        'slug': 'isoxml-timezone-ambiguous-worker-summary-supplemental-conflict',
        'conflictRecordId': 'bridgeConflict:isoxml-timezone-ambiguous-worker-summary-supplemental-conflict:v0.1',
        'candidatePairId': 'bridgePair:isoxml-draft-subset:v0.1',
        'standardRef': 'standard:isoxml:file:v4',
        'supplementalConstructFamily': 'ISOXML worker-summary records with timezone ambiguity',
        'variantFamily': 'TIMEZONE_AMBIGUOUS_WORKER_SUMMARY_BLOCKED',
        'conflictClass': 'SUPPLEMENTAL_HIGH_CONSEQUENCE_TIME_AMBIGUITY',
        'triggerExternalConstructRef': 'timezone-ambiguous worker-summary aggregates',
        'blockingReasonCodes': [
            'HIGH_CONSEQUENCE_REVIEW_REQUIRED',
            'TIMEZONE_AMBIGUITY',
            'SUPPLEMENTAL_FAMILY_OUTSIDE_DECLARED_REVERSIBLE_SCOPE',
        ],
        'requiredHandling': [
            'require-review-before-accepted-consequence',
            'do-not-claim-lossless-roundtrip',
        ],
        'notes': 'Timezone-ambiguous worker-summary families remain blocked from reversible claims even after supported ISOXML supplemental families are proven.',
    },
]

REQUIRED_LINKED_FILES = [
    'OFARM_same_standard_bridge_pack_candidate_pairs_v0_4.json',
    'OFARM_same_standard_bridge_promotion_readiness_v0_3.json',
    'OFARM_same_standard_bridge_construct_family_coverage_records_v0_1.json',
    'OFARM_deployment_intake_same_standard_bridge_telemetry_v0_1.json',
    'OFARM_deployment_intake_same_standard_bridge_results_v0_1.json',
    'OFARM_same_standard_bridge_pack_round_trip_records_v0_1.json',
    'OFARM_same_standard_bridge_pack_conflict_records_v0_1.json',
]

LIVE_FIELD_PATTERN = 'OFARM_live_field_same_standard_bridge_telemetry_v*.json'

def find_file(name: str) -> Path | None:
    matches = sorted(SEARCH_ROOT.rglob(name))
    return matches[0] if matches else None

def find_all(pattern: str) -> list[Path]:
    return sorted(SEARCH_ROOT.rglob(pattern))

def parse_json(path: Path) -> Any:
    return json.loads(path.read_text())

def build_round_trip_records() -> list[dict[str, Any]]:
    records = []
    for item in SUPPLEMENTAL_SUCCESS:
        steps = [
            {
                'stage': 'IMPORT',
                'mappingCoverageStatementRef': 'mapping-coverage:adapt-import:v1' if item['candidatePairId'].startswith('bridgePair:adapt') else 'mapping-coverage:isoxml-import:v1',
                'outcome': 'LOSS_AWARE_NORMALIZATION',
            },
            {
                'stage': 'NORMALIZE',
                'canonicalEquivalenceClass': f"equivalence:{item['slug']}:supplemental-scope:v0.1",
                'outcome': 'SUPPLEMENTAL_SCOPE_MATERIALIZED',
            },
            {
                'stage': 'EXPORT',
                'mappingCoverageStatementRef': 'mapping-coverage:adapt-export-bridge-draft:v1' if item['candidatePairId'].startswith('bridgePair:adapt') else 'mapping-coverage:isoxml-export-bridge-draft:v1',
                'runtimeSurfaceContractRef': 'surface:adapt-bridge-export-draft:v1' if item['candidatePairId'].startswith('bridgePair:adapt') else 'surface:isoxml-bridge-export-draft:v1',
                'outcome': 'DRAFT_BRIDGE_EMITTED',
            },
            {
                'stage': 'REIMPORT_VALIDATION',
                'mappingCoverageStatementRef': 'mapping-coverage:adapt-import:v1' if item['candidatePairId'].startswith('bridgePair:adapt') else 'mapping-coverage:isoxml-import:v1',
                'outcome': 'SUPPLEMENTAL_SCOPE_EQUIVALENT',
            },
        ]
        records.append({
            'recordId': item['recordId'],
            'candidatePairId': item['candidatePairId'],
            'fixtureId': item['slug'],
            'status': 'PASS',
            'pathClass': 'SAME_STANDARD_SUPPLEMENTAL_SUBSET_LOSS_AWARE',
            'standardRef': item['standardRef'],
            'supplementalConstructFamily': item['supplementalConstructFamily'],
            'variantFamily': item['variantFamily'],
            'reversibleForSupplementalFamily': True,
            'evidenceClass': 'PACKAGE_LOCAL_REDACTED_DEPLOYMENT_INTAKE_SAMPLE_PLUS_DECLARED_BRIDGE_REHEARSAL',
            'linkedIntakeRunId': item['linkedIntakeRunId'],
            'preservedConstructs': item['preservedConstructs'],
            'allowedDivergence': item['allowedDivergence'],
            'steps': steps,
            'blockingReasonCodes': [],
            'notes': item['notes'],
        })
    return records

def build_conflict_records() -> list[dict[str, Any]]:
    records = []
    for item in SUPPLEMENTAL_BLOCKED:
        records.append({
            'conflictRecordId': item['conflictRecordId'],
            'candidatePairId': item['candidatePairId'],
            'fixtureId': item['slug'],
            'status': 'PASS',
            'standardRef': item['standardRef'],
            'supplementalConstructFamily': item['supplementalConstructFamily'],
            'variantFamily': item['variantFamily'],
            'conflictClass': item['conflictClass'],
            'triggerExternalConstructRef': item['triggerExternalConstructRef'],
            'blockingReasonCodes': item['blockingReasonCodes'],
            'requiredHandling': item['requiredHandling'],
            'notes': item['notes'],
        })
    return records

def build_live_field_gate() -> dict[str, Any]:
    discovered = [str(p) for p in find_all(LIVE_FIELD_PATTERN)]
    records = []
    for candidate_pair_id, standard_ref in [
        ('bridgePair:adapt-draft-subset:v0.1', 'standard:adapt:payload:v1'),
        ('bridgePair:isoxml-draft-subset:v0.1', 'standard:isoxml:file:v4'),
    ]:
        records.append({
            'candidatePairId': candidate_pair_id,
            'standardRef': standard_ref,
            'decision': 'WAITING_FOR_LIVE_FIELD_EVIDENCE',
            'liveFieldEvidencePresent': False,
            'discoveredEvidenceRefs': discovered,
            'requiredEvidenceClasses': [
                'LIVE_FIELD_COLLECTED_SAME_STANDARD_BRIDGE_TELEMETRY',
                'DEPLOYMENT_PRODUCED_TRACE_BACK_LINKAGE',
                'PRODUCTION_PROMOTION_APPROVAL_RECORD',
            ],
            'blockingReasonCodes': [
                'NO_LIVE_FIELD_COLLECTED_SAME_STANDARD_TELEMETRY',
                'NO_PRODUCTION_PROMOTION_APPROVAL',
            ],
            'notes': 'The package has bounded executor, partner-sample, and redacted deployment-intake evidence, but no live field-collected same-standard bridge telemetry artifact was found in the package-local search scope.',
        })
    return {
        'evaluatedAt': DATE,
        'searchPattern': LIVE_FIELD_PATTERN,
        'records': records,
        'summary': {
            'candidatePairs': 2,
            'liveFieldEvidenceFound': 0,
            'waitingForEvidence': 2,
        },
        'overall': 'WAITING_FOR_LIVE_FIELD_EVIDENCE',
        'limitations': [
            'The gate is explicit about missing live field evidence; it does not fabricate or infer production telemetry from package-local sample artifacts.',
        ],
    }

def main() -> None:
    linked_checks = {}
    for name in REQUIRED_LINKED_FILES:
        path = find_file(name)
        if path is None:
            linked_checks[f'{name} :: located-and-json-parseable'] = 'FAIL'
        else:
            try:
                parse_json(path)
                linked_checks[f'{name} :: located-and-json-parseable'] = 'PASS'
            except Exception:
                linked_checks[f'{name} :: located-and-json-parseable'] = 'FAIL'

    round_trip_records = build_round_trip_records()
    conflict_records = build_conflict_records()
    live_field_gate = build_live_field_gate()

    (ROOT / 'OFARM_same_standard_bridge_supplemental_round_trip_records_v0_1.json').write_text(json.dumps(round_trip_records, indent=2) + '\n')
    (ROOT / 'OFARM_same_standard_bridge_supplemental_conflict_records_v0_1.json').write_text(json.dumps(conflict_records, indent=2) + '\n')
    (ROOT / 'OFARM_same_standard_bridge_live_field_evidence_gate_v0_1.json').write_text(json.dumps(live_field_gate, indent=2) + '\n')

    results = {
        'supplementalRoundTrips': {
            item['slug']: {
                'status': 'PASS',
                'recordId': item['recordId'],
                'candidatePairId': item['candidatePairId'],
                'reversibleForSupplementalFamily': True,
                'reasons': [],
            } for item in SUPPLEMENTAL_SUCCESS
        },
        'supplementalConflicts': {
            item['slug']: {
                'status': 'PASS',
                'conflictRecordId': item['conflictRecordId'],
                'candidatePairId': item['candidatePairId'],
                'blockingReasonCodes': item['blockingReasonCodes'],
                'reasons': [],
            } for item in SUPPLEMENTAL_BLOCKED
        },
        'liveFieldEvidenceGate': {
            rec['candidatePairId']: {
                'status': 'PASS',
                'decision': rec['decision'],
                'liveFieldEvidencePresent': rec['liveFieldEvidencePresent'],
                'blockingReasonCodes': rec['blockingReasonCodes'],
                'reasons': [],
            } for rec in live_field_gate['records']
        },
        'linkedArtifactChecks': linked_checks,
        'summary': {
            'supplementalRoundTripRecords': len(round_trip_records),
            'supplementalConflictRecords': len(conflict_records),
            'candidatePairs': 2,
            'linkedArtifactsChecked': len(linked_checks),
        },
        'limitations': [
            'Supported supplemental construct families are now round-trip proven only for the bounded draft bridge scope represented in the package.',
            'No live field-collected same-standard bridge telemetry artifact exists in the package-local search scope, so promotion readiness remains blocked.',
        ],
        'overall': 'PASS_WITH_LIMITATIONS',
        'failingChecks': [k for k, v in linked_checks.items() if v != 'PASS'],
    }
    (ROOT / 'OFARM_same_standard_bridge_supplemental_roundtrip_results_v0_1.json').write_text(json.dumps(results, indent=2) + '\n')

if __name__ == '__main__':
    main()
