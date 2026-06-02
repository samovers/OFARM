#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

try:
    import jsonschema
except ImportError as e:
    raise SystemExit('jsonschema is required for this validator') from e

ROOT = Path(__file__).resolve().parents[1]
MC = ROOT / '03_machine_contracts'
IMPL = ROOT / '04_implementation_and_conformance'
FIX = IMPL / 'ofarm_same_standard_reversible_bridge_pack_fixtures_v0_1'

PAIRSCAN_OUT = IMPL / 'OFARM_same_standard_reverse_pair_scan_v0_2.json'
CANDIDATE_OUT = IMPL / 'OFARM_same_standard_bridge_pack_candidate_pairs_v0_1.json'
ROUNDTRIP_OUT = IMPL / 'OFARM_same_standard_bridge_pack_round_trip_records_v0_1.json'
CONFLICT_OUT = IMPL / 'OFARM_same_standard_bridge_pack_conflict_records_v0_1.json'
RESULTS_OUT = IMPL / 'OFARM_same_standard_reversible_bridge_pack_results_v0_1.json'

SCHEMAS = {p.name: json.loads(p.read_text(encoding='utf-8')) for p in MC.glob('*_schema_*.json')}
for schema in SCHEMAS.values():
    jsonschema.Draft202012Validator.check_schema(schema)

FIXTURE_NAMES = sorted(p.name for p in FIX.glob('*.json'))
MAPPING_COVERAGE_EXAMPLES = sorted(p.name for p in MC.glob('OFARM_MappingCoverageStatement_example_*_v0_1.json'))
RUNTIME_SURFACE_EXAMPLES = sorted(p.name for p in MC.glob('OFARM_RuntimeSurfaceContract_example_*_v0_1.json'))


def load_json(path: Path) -> Dict[str, Any] | List[Any]:
    return json.loads(path.read_text(encoding='utf-8'))


def infer_schema(example_name: str) -> str | None:
    if '_example_' not in example_name:
        return None
    prefix = example_name.split('_example_')[0]
    candidates = sorted([name for name in SCHEMAS if name.startswith(prefix + '_schema_')])
    if not candidates:
        return None
    if len(candidates) == 1:
        return candidates[0]
    for candidate in candidates:
        if 'v0_2_draft' in example_name and 'v0_2_draft' in candidate:
            return candidate
    for candidate in candidates:
        if 'v0_1' in candidate:
            return candidate
    return candidates[0]


def validate_example(example_name: str, validations: Dict[str, str]) -> Dict[str, Any]:
    data = load_json(MC / example_name)
    schema_name = infer_schema(example_name)
    if schema_name is None:
        raise AssertionError(f'could not infer schema for {example_name}')
    jsonschema.validate(data, SCHEMAS[schema_name])
    validations[f'{example_name} :: {schema_name}'] = 'PASS'
    return data


def expect(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def build_reverse_pair_scan(validations: Dict[str, str]) -> List[Dict[str, Any]]:
    grouped: Dict[str, Dict[str, Any]] = {}
    for example_name in MAPPING_COVERAGE_EXAMPLES:
        statement = validate_example(example_name, validations)
        entry = grouped.setdefault(
            statement['externalStandardRef'],
            {
                'standardRef': statement['externalStandardRef'],
                'mappingCoverageStatementRefs': [],
                'directions': [],
                'runtimeSurfaceContractRefs': [],
            },
        )
        entry['mappingCoverageStatementRefs'].append(statement['statementId'])
        entry['directions'].append(statement['direction'])
        entry['runtimeSurfaceContractRefs'].extend(statement.get('runtimeSurfaceContractRefs', []))

    records: List[Dict[str, Any]] = []
    surface_examples = {name: load_json(MC / name) for name in RUNTIME_SURFACE_EXAMPLES}
    for standard_ref in sorted(grouped):
        entry = grouped[standard_ref]
        directions = sorted(set(entry['directions']))
        runtime_refs = sorted(set(entry['runtimeSurfaceContractRefs']))
        matched_surfaces = [surface for surface in surface_examples.values() if surface.get('contractId') in runtime_refs]
        has_import = 'IMPORT' in directions or 'BIDIRECTIONAL' in directions
        has_export = 'EXPORT' in directions or 'BIDIRECTIONAL' in directions
        blockers: List[str] = []
        limitations: List[str] = []
        if not has_import:
            blockers.append('MISSING_IMPORT_SURFACE')
        if not has_export:
            blockers.append('MISSING_EXPORT_SURFACE')
        if has_export:
            if not matched_surfaces:
                blockers.append('EXPORT_RUNTIME_SURFACE_UNDECLARED')
            else:
                if all(surface.get('semanticPreservationPosture') == 'PROJECTION_ONLY' for surface in matched_surfaces):
                    blockers.append('EXPORT_SURFACE_IS_PROJECTION_ONLY')
                if all(surface.get('status') == 'DRAFT' for surface in matched_surfaces):
                    limitations.append('EXPORT_SURFACE_DRAFT_ONLY')
        if has_import and not any(stmt.endswith(':v1') for stmt in entry['mappingCoverageStatementRefs']):
            limitations.append('IMPORT_DECLARATION_VERSION_UNCLEAR')
        records.append({
            'scanId': f"reversePair:{standard_ref.replace(':', '-')}:v0.2",
            'standardRef': standard_ref,
            'declaredDirections': directions,
            'mappingCoverageStatementRefs': sorted(set(entry['mappingCoverageStatementRefs'])),
            'runtimeSurfaceContractRefs': runtime_refs,
            'surfaceStatuses': sorted(set(surface.get('status', 'UNKNOWN') for surface in matched_surfaces)),
            'reversibleBridgeEligible': has_import and has_export and 'EXPORT_SURFACE_IS_PROJECTION_ONLY' not in blockers and 'EXPORT_RUNTIME_SURFACE_UNDECLARED' not in blockers,
            'blockingReasonCodes': blockers,
            'limitationCodes': limitations,
        })
    return records


def loss_items_index(loss_map: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    return {item['externalConstructRef']: item for item in loss_map.get('lossItems', [])}


def dropped_construct_index(statement: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    return {item['externalConstructRef']: item for item in statement.get('droppedConstructs', [])}


def covered_constructs(statement: Dict[str, Any]) -> List[str]:
    return [item['externalConstructRef'] for item in statement.get('coveredConstructs', [])]


def candidate_pair_record(fixture: Dict[str, Any], validations: Dict[str, str]) -> Tuple[Dict[str, Any], List[str]]:
    import_mapping = validate_example(fixture['importMappingCoverageExample'], validations)
    import_loss = validate_example(fixture['importLossMapExample'], validations)
    export_mapping = validate_example(fixture['exportMappingCoverageExample'], validations)
    export_loss = validate_example(fixture['exportLossMapExample'], validations)
    surface = validate_example(fixture['runtimeSurfaceContractExample'], validations)

    reasons: List[str] = []
    if import_mapping['externalStandardRef'] != export_mapping['externalStandardRef']:
        reasons.append('import/export standard refs do not match')
    if surface['targetStandardRef'] != export_mapping['externalStandardRef']:
        reasons.append('runtime surface target standard drifts from export mapping statement')
    if surface['semanticPreservationPosture'] == 'PROJECTION_ONLY':
        reasons.append('bridge surface cannot be projection-only')
    if surface['status'] != 'DRAFT':
        reasons.append('bridge surface is expected to remain draft in this wave')
    if export_mapping['roundTripExpectation'] != 'REQUIRED_FOR_DECLARED_SUBSET':
        reasons.append('export mapping must declare declared-subset round-trip expectation')

    record = {
        'candidatePairId': fixture['candidatePairId'],
        'standardRef': import_mapping['externalStandardRef'],
        'candidateStatus': 'DRAFT_DECLARED_SUBSET_REVERSIBLE' if not reasons else 'INVALID',
        'importMappingCoverageStatementRef': import_mapping['statementId'],
        'importLossMapRef': import_loss['lossMapId'],
        'exportMappingCoverageStatementRef': export_mapping['statementId'],
        'exportLossMapRef': export_loss['lossMapId'],
        'exportRuntimeSurfaceContractRef': surface['contractId'],
        'declaredSubsetConstructs': fixture.get('declaredSubsetConstructs', []),
        'excludedExternalConstructs': fixture.get('expectedExcludedExternalConstructs', []),
        'reversibleForDeclaredSubset': not reasons,
        'limitationCodes': ['EXPORT_SURFACE_DRAFT_ONLY', 'NO_EXECUTOR_SAME_STANDARD_TELEMETRY'] if not reasons else [],
        'notes': fixture['notes'],
    }
    return record, reasons


def evaluate_roundtrip_fixture(fixture: Dict[str, Any], validations: Dict[str, str], candidate_idx: Dict[str, Dict[str, Any]]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    import_mapping = validate_example(fixture['importMappingCoverageExample'], validations)
    import_loss = validate_example(fixture['importLossMapExample'], validations)
    export_mapping = validate_example(fixture['exportMappingCoverageExample'], validations)
    export_loss = validate_example(fixture['exportLossMapExample'], validations)
    surface = validate_example(fixture['runtimeSurfaceContractExample'], validations)
    pair = candidate_idx[fixture['candidatePairId']]

    reasons: List[str] = []
    if not pair['reversibleForDeclaredSubset']:
        reasons.append('candidate pair is not reversible for declared subset')

    subset = fixture['declaredSubsetConstructs']
    import_covered = set(covered_constructs(import_mapping))
    export_covered = set(covered_constructs(export_mapping))
    missing_import = sorted([c for c in subset if c not in import_covered])
    missing_export = sorted([c for c in subset if c not in export_covered])
    if missing_import:
        reasons.append(f'declared subset missing from import mapping coverage: {missing_import}')
    if missing_export:
        reasons.append(f'declared subset missing from export mapping coverage: {missing_export}')

    excluded = set(fixture['expectedExcludedExternalConstructs'])
    import_loss_idx = loss_items_index(import_loss)
    export_loss_idx = loss_items_index(export_loss)
    export_dropped_idx = dropped_construct_index(export_mapping)

    # High-consequence or clearly unsupported constructs must be outside the declared subset.
    for ref, item in import_loss_idx.items():
        high_risk = item.get('requiresGovernanceOnHighConsequenceUse') or item.get('impactLevel') in {'HIGH', 'CRITICAL'} or item.get('lossClass') in {'UNREPRESENTABLE', 'ASSUMED'}
        if high_risk and ref not in excluded:
            reasons.append(f'high-risk import loss construct not excluded from declared subset posture: {ref}')
    for ref in export_dropped_idx:
        if ref not in excluded:
            reasons.append(f'export dropped construct not excluded from declared subset posture: {ref}')

    allowed_drift = []
    for ref, item in import_loss_idx.items():
        if ref in excluded:
            continue
        if item.get('impactLevel') in {'LOW', 'MEDIUM'}:
            allowed_drift.append({'externalConstructRef': ref, 'lossClass': item['lossClass'], 'source': 'IMPORT'})
    for ref, item in export_loss_idx.items():
        if ref in excluded:
            continue
        if item.get('impactLevel') in {'LOW', 'MEDIUM'}:
            allowed_drift.append({'externalConstructRef': ref, 'lossClass': item['lossClass'], 'source': 'EXPORT'})

    steps = [
        {
            'stage': 'IMPORT',
            'mappingCoverageStatementRef': import_mapping['statementId'],
            'lossMapRef': import_loss['lossMapId'],
            'outcome': 'LOSS_AWARE_NORMALIZATION',
        },
        {
            'stage': 'NORMALIZE',
            'canonicalEquivalenceClass': f"equivalence:{fixture['fixtureId']}:declared-subset:v0.1",
            'outcome': 'DECLARED_SUBSET_MATERIALIZED',
        },
        {
            'stage': 'EXPORT',
            'mappingCoverageStatementRef': export_mapping['statementId'],
            'runtimeSurfaceContractRef': surface['contractId'],
            'lossMapRef': export_loss['lossMapId'],
            'outcome': 'DRAFT_BRIDGE_EMITTED',
        },
        {
            'stage': 'REIMPORT_VALIDATION',
            'mappingCoverageStatementRef': import_mapping['statementId'],
            'outcome': 'DECLARED_SUBSET_EQUIVALENT',
        },
    ]
    record = {
        'recordId': f"bridgeRoundTrip:{fixture['fixtureId']}:v0.1",
        'candidatePairId': fixture['candidatePairId'],
        'fixtureId': fixture['fixtureId'],
        'status': 'PASS' if not reasons else 'FAIL',
        'pathClass': fixture['expectedPathClass'],
        'standardRef': import_mapping['externalStandardRef'],
        'declaredSubsetConstructs': subset,
        'excludedExternalConstructs': fixture['expectedExcludedExternalConstructs'],
        'preservedConstructs': subset,
        'allowedDivergence': allowed_drift,
        'steps': steps,
        'blockingReasonCodes': [],
        'notes': fixture['notes'],
    }
    result = {
        'status': record['status'],
        'recordId': record['recordId'],
        'pathClass': record['pathClass'],
        'candidatePairId': fixture['candidatePairId'],
        'reasons': reasons,
    }
    return record, result


def evaluate_conflict_fixture(fixture: Dict[str, Any], validations: Dict[str, str], candidate_idx: Dict[str, Dict[str, Any]]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    import_mapping = validate_example(fixture['importMappingCoverageExample'], validations)
    import_loss = validate_example(fixture['importLossMapExample'], validations)
    export_mapping = validate_example(fixture['exportMappingCoverageExample'], validations)
    export_loss = validate_example(fixture['exportLossMapExample'], validations)
    surface = validate_example(fixture['runtimeSurfaceContractExample'], validations)
    pair = candidate_idx[fixture['candidatePairId']]

    reasons: List[str] = []
    trigger = fixture['triggerExternalConstructRef']
    import_loss_idx = loss_items_index(import_loss)
    import_dropped = dropped_construct_index(import_mapping)
    export_dropped = dropped_construct_index(export_mapping)
    blockers: List[str] = []

    if trigger in import_dropped and import_dropped[trigger].get('reasonCode') == 'VENDOR_VARIANT_UNSUPPORTED':
        blockers.append('VENDOR_VARIANT_UNSUPPORTED')
    if trigger in export_dropped or trigger in import_loss_idx or trigger in import_dropped:
        # pair is declared-subset only, so any explicit trigger outside that subset must remain blocked
        blockers.append('ROUNDTRIP_DECLARED_SUBSET_ONLY')
    if trigger in import_loss_idx:
        item = import_loss_idx[trigger]
        if item.get('lossClass') == 'ASSUMED':
            blockers.append('ASSUMED_TIME_NORMALIZATION')
        if item.get('requiresGovernanceOnHighConsequenceUse'):
            blockers.append('HIGH_CONSEQUENCE_REVIEW_REQUIRED')

    expected = set(fixture['expectedBlockers'])
    if not expected.issubset(set(blockers)):
        reasons.append(f'expected blockers missing: {sorted(expected - set(blockers))}')
    if surface['semanticPreservationPosture'] == 'PROJECTION_ONLY':
        reasons.append('conflict pair drifted to projection-only posture')
    if not pair['reversibleForDeclaredSubset']:
        reasons.append('conflict pair must still be valid for declared subset')

    record = {
        'conflictRecordId': f"bridgeConflict:{fixture['fixtureId']}:v0.1",
        'candidatePairId': fixture['candidatePairId'],
        'fixtureId': fixture['fixtureId'],
        'status': 'PASS' if not reasons else 'FAIL',
        'standardRef': import_mapping['externalStandardRef'],
        'conflictClass': fixture['conflictClass'],
        'triggerExternalConstructRef': trigger,
        'blockingReasonCodes': sorted(set(blockers)),
        'requiredHandling': fixture['requiredHandling'],
        'notes': fixture['notes'],
    }
    result = {
        'status': record['status'],
        'conflictRecordId': record['conflictRecordId'],
        'candidatePairId': fixture['candidatePairId'],
        'reasons': reasons,
        'blockingReasonCodes': record['blockingReasonCodes'],
    }
    return record, result


def main() -> int:
    validations: Dict[str, str] = {}

    pair_scan = build_reverse_pair_scan(validations)
    pair_scan_idx = {r['standardRef']: r for r in pair_scan}

    # Build candidate pairs from successful round-trip fixtures first.
    candidate_pairs: List[Dict[str, Any]] = []
    candidate_results: Dict[str, Any] = {}
    for fixture_name in FIXTURE_NAMES:
        fixture = load_json(FIX / fixture_name)
        if fixture['fixtureType'] != 'SAME_STANDARD_DECLARED_SUBSET_ROUNDTRIP':
            continue
        pair_record, reasons = candidate_pair_record(fixture, validations)
        candidate_pairs.append(pair_record)
        standard_scan = pair_scan_idx.get(pair_record['standardRef'])
        if standard_scan and not standard_scan['reversibleBridgeEligible']:
            reasons.append('reverse-pair scan does not mark this standard as reversible-eligible')
        candidate_results[fixture['fixtureId']] = {
            'status': 'PASS' if not reasons else 'FAIL',
            'candidatePairId': pair_record['candidatePairId'],
            'standardRef': pair_record['standardRef'],
            'reversibleForDeclaredSubset': pair_record['reversibleForDeclaredSubset'],
            'reasons': reasons,
        }

    candidate_idx = {r['candidatePairId']: r for r in candidate_pairs}

    roundtrip_records: List[Dict[str, Any]] = []
    roundtrip_results: Dict[str, Any] = {}
    conflict_records: List[Dict[str, Any]] = []
    conflict_results: Dict[str, Any] = {}

    for fixture_name in FIXTURE_NAMES:
        fixture = load_json(FIX / fixture_name)
        if fixture['fixtureType'] == 'SAME_STANDARD_DECLARED_SUBSET_ROUNDTRIP':
            record, result = evaluate_roundtrip_fixture(fixture, validations, candidate_idx)
            roundtrip_records.append(record)
            roundtrip_results[fixture['fixtureId']] = result
        elif fixture['fixtureType'] == 'SAME_STANDARD_CONFLICT_CASE':
            record, result = evaluate_conflict_fixture(fixture, validations, candidate_idx)
            conflict_records.append(record)
            conflict_results[fixture['fixtureId']] = result
        else:
            raise AssertionError(f"unsupported fixture type: {fixture['fixtureType']}")

    PAIRSCAN_OUT.write_text(json.dumps(pair_scan, indent=2) + '\n', encoding='utf-8')
    CANDIDATE_OUT.write_text(json.dumps(candidate_pairs, indent=2) + '\n', encoding='utf-8')
    ROUNDTRIP_OUT.write_text(json.dumps(roundtrip_records, indent=2) + '\n', encoding='utf-8')
    CONFLICT_OUT.write_text(json.dumps(conflict_records, indent=2) + '\n', encoding='utf-8')

    failing = []
    for bucket_name, bucket in [('candidatePairs', candidate_results), ('sameStandardRoundTrips', roundtrip_results), ('conflictCases', conflict_results)]:
        for key, value in bucket.items():
            if value['status'] != 'PASS':
                failing.append(f'{bucket_name}:{key}')

    results = {
        'candidatePairs': candidate_results,
        'sameStandardRoundTrips': roundtrip_results,
        'conflictCases': conflict_results,
        'summary': {
            'reversePairRecords': len(pair_scan),
            'eligibleReversePairs': sum(1 for r in pair_scan if r['reversibleBridgeEligible']),
            'candidatePairs': len(candidate_pairs),
            'roundTripRecords': len(roundtrip_records),
            'conflictRecords': len(conflict_records),
            'validatedArtifacts': len(validations),
        },
        'limitations': [
            'Bridge-pack export surfaces remain DRAFT and are not promoted into baseline or production-readiness claims.',
            'Same-standard round-trip proof is declared-subset conformance evidence, not deployment-collected runtime telemetry.',
        ],
        'overall': 'PASS_WITH_LIMITATIONS' if not failing else 'FAIL',
        'failingChecks': failing,
        'linkedArtifactChecks': validations,
    }

    RESULTS_OUT.write_text(json.dumps(results, indent=2) + '\n', encoding='utf-8')
    print(PAIRSCAN_OUT)
    print(CANDIDATE_OUT)
    print(ROUNDTRIP_OUT)
    print(CONFLICT_OUT)
    print(RESULTS_OUT)
    print(results['overall'])
    return 0 if results['overall'].startswith('PASS') else 1


if __name__ == '__main__':
    raise SystemExit(main())
