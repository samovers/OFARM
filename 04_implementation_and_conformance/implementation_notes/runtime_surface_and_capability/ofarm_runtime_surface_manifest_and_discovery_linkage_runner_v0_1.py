#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import jsonschema
except ImportError as e:  # pragma: no cover
    raise SystemExit('jsonschema is required for this validator') from e

ROOT = Path(__file__).resolve().parents[1]
MC = ROOT / '03_machine_contracts'
OUT = Path(__file__).resolve().parent / 'OFARM_runtime_surface_manifest_and_discovery_linkage_results_v0_1.json'


def load_json(name: str) -> Any:
    return json.loads((MC / name).read_text(encoding='utf-8'))


def validate_against(example_name: str, schema_name: str) -> None:
    data = load_json(example_name)
    schema = load_json(schema_name)
    jsonschema.validate(data, schema)


def evaluate(manifest: dict[str, Any], active: dict[str, Any], claimset: dict[str, Any], substrate: dict[str, Any], contracts: list[dict[str, Any]]) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    reasons: list[str] = []

    def record(check_id: str, ok: bool, detail: str) -> None:
        checks.append({
            'checkId': check_id,
            'status': 'PASS' if ok else 'FAIL',
            'detail': detail,
        })
        if not ok:
            reasons.append(f'{check_id}: {detail}')

    contract_by_id = {item['contractId']: item for item in contracts}
    discovery_targets = {
        row['targetRef']
        for row in manifest['capabilitySections']['importExportSupport']['declaredSurfaces']
        if row['surfaceType'] == 'DISCOVERY_SURFACE'
    }
    non_mapping_targets = {
        row['targetRef']
        for row in manifest['capabilitySections']['importExportSupport']['declaredSurfaces']
        if row['surfaceType'] not in {'IMPORT_MAPPING', 'EXPORT_MAPPING'}
    }
    claim_targets = {claim['targetRef'] for claim in claimset['claims'] if claim['claimFamily'] == 'RUNTIME_SURFACE'}

    record(
        'manifest-activeartifactset-ref',
        manifest['registryRelation']['activeArtifactSetRef'] == active['activeArtifactSetId'],
        'manifest activeArtifactSetRef must resolve to the linked ActiveArtifactSet id',
    )
    record(
        'manifest-claimset-ref',
        manifest['registryRelation'].get('conformanceClaimSetRef') == claimset['claimSetId'],
        'manifest conformanceClaimSetRef must resolve to the linked ConformanceClaimSet',
    )
    record(
        'claimset-activeartifactset-ref',
        claimset['activeArtifactSetRef'] == active['activeArtifactSetId'],
        'ConformanceClaimSet must ground on the same ActiveArtifactSet as the linked manifest',
    )
    record(
        'manifest-substrate-ref',
        manifest['registryRelation'].get('semanticSubstrateBundleRef') == substrate['bundleId'],
        'manifest semanticSubstrateBundleRef must resolve to the promoted substrate bundle example',
    )
    record(
        'scope-match',
        manifest['deploymentScope'] == active['deploymentScope'],
        'manifest and active artifact set must describe the same deployment scope',
    )
    record(
        'artifact-registry-match',
        manifest['registryRelation']['artifactRegistryRef'] == active['artifactRegistryRef'],
        'manifest and active artifact set must use the same artifact registry ref',
    )

    active_refs = set(active['activeArtifactRefs'])
    for ref, cid in [
        (manifest['manifestId'], 'active-grounding-manifest'),
        (manifest['registryRelation']['semanticSubstrateBundleRef'], 'active-grounding-substrate'),
        (manifest['registryRelation']['conformanceClaimSetRef'], 'active-grounding-claimset'),
    ]:
        record(cid, ref in active_refs, f'linked active artifact set must include {ref}')

    requires_discovery = manifest['registryRelation']['discoveryVisibility'] != 'PRIVATE'
    discovery_rows = [
        row for row in manifest['capabilitySections']['importExportSupport']['declaredSurfaces']
        if row['surfaceType'] == 'DISCOVERY_SURFACE' and row['status'] in {'SUPPORTED', 'PARTIAL'}
    ]
    record(
        'discovery-row-required',
        (not requires_discovery) or bool(discovery_rows),
        'restricted/public discovery visibility requires at least one supported/partial discovery surface row',
    )

    supported_contract_refs: set[str] = set()
    for row in manifest['capabilitySections']['importExportSupport']['declaredSurfaces']:
        contract_ref = row.get('contractRef')
        if not contract_ref:
            continue
        contract = contract_by_id.get(contract_ref)
        record(
            f'contract-resolves:{contract_ref}',
            contract is not None,
            f'manifest contractRef must resolve to a known runtime-surface contract: {contract_ref}',
        )
        if contract is None:
            continue
        if row['status'] in {'SUPPORTED', 'PARTIAL'}:
            supported_contract_refs.add(contract_ref)
        if row['surfaceType'] in {'IMPORT_MAPPING', 'EXPORT_MAPPING'}:
            record(
                f'mapping-linkage:{contract_ref}',
                row['targetRef'] in contract.get('mappingModuleRefs', []),
                'mapping manifest row targetRef must appear in linked runtime-surface mappingModuleRefs',
            )
        else:
            record(
                f'surface-identity-linkage:{contract_ref}',
                row['targetRef'] == contract.get('surfaceIdentityRef'),
                'non-mapping manifest row targetRef must equal linked runtime-surface surfaceIdentityRef',
            )
        manifest_docs = set(row.get('serviceDescriptionRefs', []))
        contract_docs = set(contract.get('serviceDescriptionRefs', []))
        record(
            f'service-description-linkage:{contract_ref}',
            manifest_docs.issubset(contract_docs),
            'manifest serviceDescriptionRefs must be a subset of linked runtime-surface serviceDescriptionRefs',
        )
        if row['status'] in {'SUPPORTED', 'PARTIAL'}:
            record(
                f'active-grounding-surface:{contract_ref}',
                contract_ref in active_refs,
                'supported/partial runtime-surface contract must be present in ActiveArtifactSet activeArtifactRefs',
            )
        else:
            record(
                f'planned-surface-may-be-inactive:{contract_ref}',
                contract_ref not in active_refs,
                'planned runtime-surface contract may remain out of ActiveArtifactSet activeArtifactRefs',
            )

    for contract in contracts:
        for ref in contract.get('discoveryRefs', []):
            record(
                f'discovery-ref-linkage:{contract["contractId"]}:{ref}',
                ref in discovery_targets,
                'runtime-surface discoveryRefs should resolve to a declared governed discovery surface identity',
            )

    record(
        'supported-contract-count',
        supported_contract_refs == {
            row['contractRef']
            for row in manifest['capabilitySections']['importExportSupport']['declaredSurfaces']
            if row.get('contractRef') and row['status'] in {'SUPPORTED', 'PARTIAL'}
        },
        'supported/partial surface contracts must be identified deterministically',
    )

    record(
        'claimset-runtime-surface-targets-grounded',
        claim_targets.issuperset(non_mapping_targets),
        'linked ConformanceClaimSet runtime-surface claims should cover the non-mapping surface identities declared in the linked manifest',
    )

    outcome = 'PASS' if not reasons else 'FAIL'
    return {
        'outcome': outcome,
        'checks': checks,
        'reasons': reasons,
    }


def main() -> int:
    result: dict[str, Any] = {
        'generatedAt': datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z'),
        'overall': 'PASS_WITH_LIMITATIONS',
        'summary': {
            'positiveValidations': 0,
            'linkageChecks': 0,
            'negativeCasesChecked': 0,
            'negativeCasesExpectedFail': 0,
            'supportedOrPartialSurfaceContractsGrounded': 0,
            'plannedSurfaceContractsLeftInactive': 0,
        },
        'positiveValidations': [],
        'linkageChecks': [],
        'negativeChecks': [],
        'limitations': [
            'This proof is package-local deployment-linkage hardening only and does not fetch live `.well-known`, OpenAPI, or AsyncAPI endpoints.',
            'Service-description documents are matched by declared ref only; the runner does not parse those external documents.',
            'RuntimeSurfaceContract v0.2 draft remains a non-default extension lane even where the linked manifest points at bounded draft contracts.',
        ],
    }

    validations = [
        ('OFARM_Capability_Manifest_example_core_deployment_surface_linkage_v0_2_draft.json', 'OFARM_Capability_Manifest_schema_v0_2_draft.json'),
        ('OFARM_ActiveArtifactSet_example_core_deployment_surface_linkage_v0_1.json', 'OFARM_ActiveArtifactSet_schema_v0_1.json'),
        ('OFARM_ConformanceClaimSet_example_core_deployment_surface_linkage_v0_1.json', 'OFARM_ConformanceClaimSet_schema_v0_1.json'),
        ('OFARM_RuntimeSurfaceContract_example_capability_discovery_v0_2_draft.json', 'OFARM_RuntimeSurfaceContract_schema_v0_2_draft.json'),
        ('OFARM_RuntimeSurfaceContract_example_ngsi_ld_export_v0_2_draft.json', 'OFARM_RuntimeSurfaceContract_schema_v0_2_draft.json'),
        ('OFARM_RuntimeSurfaceContract_example_cql2_query_facade_v0_2_draft.json', 'OFARM_RuntimeSurfaceContract_schema_v0_2_draft.json'),
        ('OFARM_RuntimeSurfaceContract_example_semantic_event_ingress_v0_2_draft.json', 'OFARM_RuntimeSurfaceContract_schema_v0_2_draft.json'),
    ]

    for example_name, schema_name in validations:
        validate_against(example_name, schema_name)
        result['positiveValidations'].append({
            'exampleFile': example_name,
            'schemaFile': schema_name,
            'status': 'PASS',
        })
    result['summary']['positiveValidations'] = len(result['positiveValidations'])

    manifest = load_json('OFARM_Capability_Manifest_example_core_deployment_surface_linkage_v0_2_draft.json')
    active = load_json('OFARM_ActiveArtifactSet_example_core_deployment_surface_linkage_v0_1.json')
    claimset = load_json('OFARM_ConformanceClaimSet_example_core_deployment_surface_linkage_v0_1.json')
    substrate = load_json('OFARM_SemanticSubstrateBundle_example_core_profile_v0_1.json')
    contracts = [
        load_json('OFARM_RuntimeSurfaceContract_example_capability_discovery_v0_2_draft.json'),
        load_json('OFARM_RuntimeSurfaceContract_example_ngsi_ld_export_v0_2_draft.json'),
        load_json('OFARM_RuntimeSurfaceContract_example_cql2_query_facade_v0_2_draft.json'),
        load_json('OFARM_RuntimeSurfaceContract_example_semantic_event_ingress_v0_2_draft.json'),
    ]

    evaluation = evaluate(manifest, active, claimset, substrate, contracts)
    result['linkageChecks'] = evaluation['checks']
    result['summary']['linkageChecks'] = len(evaluation['checks'])
    result['summary']['supportedOrPartialSurfaceContractsGrounded'] = sum(
        1 for item in evaluation['checks'] if item['checkId'].startswith('active-grounding-surface:') and item['status'] == 'PASS'
    )
    result['summary']['plannedSurfaceContractsLeftInactive'] = sum(
        1 for item in evaluation['checks'] if item['checkId'].startswith('planned-surface-may-be-inactive:') and item['status'] == 'PASS'
    )
    if evaluation['outcome'] != 'PASS':
        result['overall'] = 'FAIL'

    negative_cases: list[tuple[str, dict[str, Any], dict[str, Any], dict[str, Any], list[dict[str, Any]], str]] = []

    neg_manifest = copy.deepcopy(manifest)
    neg_manifest['capabilitySections']['importExportSupport']['declaredSurfaces'] = [
        row for row in neg_manifest['capabilitySections']['importExportSupport']['declaredSurfaces']
        if row['surfaceType'] != 'DISCOVERY_SURFACE'
    ]
    negative_cases.append(('neg-missing-discovery-surface', neg_manifest, active, claimset, contracts, 'discovery-row-required'))

    neg_manifest = copy.deepcopy(manifest)
    for row in neg_manifest['capabilitySections']['importExportSupport']['declaredSurfaces']:
        if row.get('contractRef') == 'surface-contract:ngsi-ld-export:v0.2-draft':
            row['serviceDescriptionRefs'] = ['openapi:wrong-ngsi-ld-export:v9']
    negative_cases.append(('neg-manifest-service-description-drift', neg_manifest, active, claimset, contracts, 'service-description-linkage:surface-contract:ngsi-ld-export:v0.2-draft'))

    neg_active = copy.deepcopy(active)
    neg_active['activeArtifactRefs'] = [
        ref for ref in neg_active['activeArtifactRefs']
        if ref != 'surface-contract:ngsi-ld-export:v0.2-draft'
    ]
    negative_cases.append(('neg-missing-supported-surface-grounding', manifest, neg_active, claimset, contracts, 'active-grounding-surface:surface-contract:ngsi-ld-export:v0.2-draft'))

    neg_contracts = copy.deepcopy(contracts)
    for contract in neg_contracts:
        if contract['contractId'] == 'surface-contract:ngsi-ld-export:v0.2-draft':
            contract['discoveryRefs'] = ['surface:missing-discovery:v1']
    negative_cases.append(('neg-undeclared-discovery-ref', manifest, active, claimset, neg_contracts, 'discovery-ref-linkage:surface-contract:ngsi-ld-export:v0.2-draft:surface:missing-discovery:v1'))

    neg_manifest = copy.deepcopy(manifest)
    for row in neg_manifest['capabilitySections']['importExportSupport']['declaredSurfaces']:
        if row.get('contractRef') == 'surface-contract:ngsi-ld-export:v0.2-draft':
            row['targetRef'] = 'mapping:ngsi-ld-export:wrong:v1'
    negative_cases.append(('neg-export-mapping-target-drift', neg_manifest, active, claimset, contracts, 'mapping-linkage:surface-contract:ngsi-ld-export:v0.2-draft'))

    for case_id, man, act, clm, ctrs, expected_check in negative_cases:
        ev = evaluate(man, act, clm, substrate, ctrs)
        failed_checks = {item['checkId'] for item in ev['checks'] if item['status'] == 'FAIL'}
        ok = expected_check in failed_checks
        result['negativeChecks'].append({
            'caseId': case_id,
            'status': 'EXPECTED_FAIL' if ok else 'UNEXPECTED_PASS',
            'expectedFailedCheck': expected_check,
            'failedChecks': sorted(failed_checks),
            'reasons': ev['reasons'],
        })
        if not ok:
            result['overall'] = 'FAIL'

    result['summary']['negativeCasesChecked'] = len(result['negativeChecks'])
    result['summary']['negativeCasesExpectedFail'] = sum(1 for item in result['negativeChecks'] if item['status'] == 'EXPECTED_FAIL')

    OUT.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(OUT)
    print(result['overall'])
    return 0 if result['overall'] != 'FAIL' else 1


if __name__ == '__main__':
    raise SystemExit(main())
