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
IC = Path(__file__).resolve().parent
SVC = IC / 'service_descriptions' / 'core_surface_linkage_release_v0_1'
OUT = IC / 'OFARM_runtime_surface_deployment_release_traceability_results_v0_1.json'


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding='utf-8'))


def load_contract(name: str) -> Any:
    return load_json(MC / name)


def validate_against(example_name: str, schema_name: str) -> None:
    data = load_contract(example_name)
    schema = load_contract(schema_name)
    jsonschema.validate(data, schema)


def parse_ts(value: str) -> datetime:
    return datetime.fromisoformat(value.replace('Z', '+00:00'))


RELEASE_POSTURE_BY_STATUS = {
    'SUPPORTED': 'LIVE_SUPPORTED',
    'PARTIAL': 'LIVE_PARTIAL',
    'PLANNED': 'PREVIEW_ONLY',
}


def evaluate(
    manifest: dict[str, Any],
    active: dict[str, Any],
    claimset: dict[str, Any],
    contracts: list[dict[str, Any]],
    bundle: dict[str, Any],
    catalog: dict[str, Any],
    docs_by_path: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    reasons: list[str] = []

    def record(check_id: str, ok: bool, detail: str) -> None:
        checks.append({'checkId': check_id, 'status': 'PASS' if ok else 'FAIL', 'detail': detail})
        if not ok:
            reasons.append(f'{check_id}: {detail}')

    contract_by_id = {item['contractId']: item for item in contracts}
    rows = [row for row in manifest['capabilitySections']['importExportSupport']['declaredSurfaces'] if row.get('contractRef')]
    row_by_contract = {row['contractRef']: row for row in rows}
    row_by_target = {row['targetRef']: row for row in rows}
    bundle_entries = bundle['surfaceReleases']
    bundle_by_contract = {entry['surfaceContractRef']: entry for entry in bundle_entries}
    catalog_entries = catalog['entries']
    catalog_by_id = {entry['entryId']: entry for entry in catalog_entries}
    catalog_by_doc = {entry['serviceDescriptionId']: entry for entry in catalog_entries}

    record(
        'bundle-evidence-posture',
        bundle.get('evidencePosture') == 'PACKAGE_LOCAL_FIXTURE_ONLY',
        'release bundle must stay explicitly fixture-only',
    )
    record(
        'bundle-live-evidence-flag',
        bundle.get('qualifiesAsLiveDeploymentEvidence') is False,
        'release bundle must not claim live deployment evidence',
    )
    record(
        'bundle-manifest-ref',
        bundle['manifestRef'] == manifest['manifestId'],
        'release bundle manifestRef must resolve to the linked manifest example',
    )
    record(
        'bundle-activeartifactset-ref',
        bundle['activeArtifactSetRef'] == active['activeArtifactSetId'],
        'release bundle activeArtifactSetRef must resolve to the linked ActiveArtifactSet',
    )
    record(
        'bundle-claimset-ref',
        bundle['conformanceClaimSetRef'] == claimset['claimSetId'],
        'release bundle conformanceClaimSetRef must resolve to the linked ConformanceClaimSet',
    )
    record(
        'bundle-scope-match',
        bundle['deploymentScope'] == manifest['deploymentScope'] == active['deploymentScope'],
        'release bundle deployment scope must match manifest and ActiveArtifactSet scope',
    )
    record(
        'bundle-catalog-ref',
        bundle['runtimeSurfaceCatalogRef'] == catalog['catalogId'],
        'release bundle must point at the local service-description catalog',
    )
    record(
        'catalog-manifest-ref',
        catalog['manifestRef'] == manifest['manifestId'],
        'service-description catalog manifestRef must resolve to the linked manifest example',
    )
    record(
        'catalog-evidence-posture',
        catalog.get('evidencePosture') == 'PACKAGE_LOCAL_FIXTURE_ONLY' and catalog.get('qualifiesAsLiveDeploymentEvidence') is False,
        'service-description catalog must stay explicitly fixture-only and non-live',
    )

    bundle_ts = parse_ts(bundle['generatedAt'])
    record(
        'bundle-generated-after-manifest',
        bundle_ts >= parse_ts(manifest['publishedAt']),
        'release bundle timestamp must be on or after manifest publication time',
    )
    record(
        'bundle-generated-after-activeartifactset',
        bundle_ts >= parse_ts(active['generatedAt']),
        'release bundle timestamp must be on or after ActiveArtifactSet generation time',
    )
    record(
        'bundle-generated-after-claimset',
        bundle_ts >= parse_ts(claimset['generatedAt']),
        'release bundle timestamp must be on or after ConformanceClaimSet generation time',
    )

    record(
        'surface-release-count',
        len(bundle_entries) == len(rows),
        'release bundle should include one surface-release entry per manifest row carrying contractRef',
    )
    record(
        'catalog-entry-count',
        len(catalog_entries) == len(rows),
        'service-description catalog should include one entry per manifest row carrying serviceDescriptionRefs',
    )

    for entry in bundle_entries:
        contract_ref = entry['surfaceContractRef']
        contract = contract_by_id.get(contract_ref)
        row = row_by_contract.get(contract_ref)
        record(
            f'bundle-contract-resolves:{contract_ref}',
            contract is not None,
            'release bundle surfaceContractRef must resolve to a linked runtime-surface contract',
        )
        record(
            f'bundle-manifest-row-resolves:{contract_ref}',
            row is not None,
            'release bundle surfaceContractRef must resolve to a manifest surface row',
        )
        if contract is None or row is None:
            continue
        record(
            f'bundle-manifest-target:{contract_ref}',
            entry['manifestTargetRef'] == row['targetRef'],
            'release bundle manifestTargetRef must match the linked manifest row targetRef',
        )
        record(
            f'bundle-surface-identity:{contract_ref}',
            entry['surfaceIdentityRef'] == contract['surfaceIdentityRef'],
            'release bundle surfaceIdentityRef must match the linked runtime-surface contract surfaceIdentityRef',
        )
        record(
            f'bundle-surface-kind:{contract_ref}',
            entry['surfaceKind'] == contract['surfaceKind'],
            'release bundle surfaceKind must match the linked runtime-surface contract surfaceKind',
        )
        record(
            f'bundle-status-alignment:{contract_ref}',
            entry['manifestSurfaceStatus'] == row['status'] and entry['contractStatus'] == contract['status'],
            'release bundle surface status fields must match the linked manifest row and runtime-surface contract',
        )
        record(
            f'bundle-release-posture:{contract_ref}',
            entry['releasePosture'] == RELEASE_POSTURE_BY_STATUS[row['status']],
            'release bundle releasePosture must follow the manifest surface status mapping',
        )
        record(
            f'bundle-doc-refs:{contract_ref}',
            entry['serviceDescriptionRefs'] == row.get('serviceDescriptionRefs', []),
            'release bundle serviceDescriptionRefs must match the linked manifest row',
        )
        record(
            f'bundle-catalog-entry-ids:{contract_ref}',
            [catalog_by_doc[doc]['entryId'] for doc in row.get('serviceDescriptionRefs', [])] == entry['catalogEntryIds'],
            'release bundle catalogEntryIds must resolve deterministically from serviceDescriptionRefs',
        )
        if row['status'] == 'PLANNED' or contract['status'] == 'DRAFT':
            record(
                f'bundle-planned-preview-only:{contract_ref}',
                entry['releasePosture'] == 'PREVIEW_ONLY',
                'planned or draft surfaces must remain preview-only in the release bundle',
            )

    for entry in catalog_entries:
        path = ROOT / entry['localPath']
        doc = docs_by_path.get(entry['localPath'])
        contract = contract_by_id.get(entry['linkedContractRef'])
        matching_rows = [row for row in rows if entry['serviceDescriptionId'] in row.get('serviceDescriptionRefs', [])]
        row = matching_rows[0] if matching_rows else None
        record(
            f'catalog-path-exists:{entry["entryId"]}',
            path.exists() and doc is not None,
            'service-description catalog localPath must resolve to a parseable local JSON document',
        )
        record(
            f'catalog-contract-resolves:{entry["entryId"]}',
            contract is not None,
            'service-description catalog linkedContractRef must resolve to a linked runtime-surface contract',
        )
        record(
            f'catalog-manifest-row-resolves:{entry["entryId"]}',
            row is not None,
            'service-description catalog serviceDescriptionId must resolve to a manifest surface row',
        )
        if doc is None or contract is None or row is None:
            continue
        record(
            f'catalog-target-surface:{entry["entryId"]}',
            entry['targetSurfaceRef'] == contract['surfaceIdentityRef'],
            'service-description catalog targetSurfaceRef must match the linked runtime-surface contract surfaceIdentityRef',
        )
        record(
            f'catalog-status:{entry["entryId"]}',
            entry['status'] == row['status'],
            'service-description catalog status must match the linked manifest row status',
        )
        record(
            f'catalog-release-label:{entry["entryId"]}',
            catalog['releaseLabel'] == bundle['releaseLabel'],
            'service-description catalog release label must match the release bundle',
        )
        doc_kind = entry['kind']
        if doc_kind == 'EQUIVALENT_JSON_CONTRACT':
            record(
                f'doc-id:{entry["entryId"]}',
                doc.get('documentId') == entry['serviceDescriptionId'],
                'endpoint-description documentId must match the catalog serviceDescriptionId',
            )
            record(
                f'doc-target-surface:{entry["entryId"]}',
                doc.get('targetSurfaceRef') == entry['targetSurfaceRef'],
                'endpoint-description targetSurfaceRef must match the catalog targetSurfaceRef',
            )
            record(
                f'doc-linked-contract:{entry["entryId"]}',
                doc.get('linkedContractRef') == entry['linkedContractRef'],
                'endpoint-description linkedContractRef must match the catalog linkedContractRef',
            )
            record(
                f'doc-linked-manifest:{entry["entryId"]}',
                doc.get('linkedManifestRef') == manifest['manifestId'],
                'endpoint-description linkedManifestRef must match the linked manifest',
            )
            record(
                f'doc-status:{entry["entryId"]}',
                doc.get('status') == entry['status'],
                'endpoint-description status must match the catalog status',
            )
            record(
                f'doc-release-label:{entry["entryId"]}',
                doc.get('releaseLabel') == bundle['releaseLabel'],
                'endpoint-description release label must match the release bundle',
            )
            binding_value = contract.get('surfaceBinding', {}).get('bindingValue')
            record(
                f'doc-locator:{entry["entryId"]}',
                doc.get('locator') == binding_value == entry['locator'],
                'endpoint-description locator must match runtime-surface binding and catalog locator',
            )
            response_local_path = doc.get('responseLocalPath')
            response_doc = docs_by_path.get(response_local_path, {}) if isinstance(response_local_path, str) else {}
            record(
                f'discovery-response-exists:{entry["entryId"]}',
                isinstance(response_local_path, str) and (ROOT / response_local_path).exists() and bool(response_doc),
                'endpoint-description responseLocalPath must resolve to a local discovery response document',
            )
            if response_doc:
                record(
                    f'discovery-response-id:{entry["entryId"]}',
                    response_doc.get('documentId') == doc.get('responseArtifactRef'),
                    'discovery response documentId must match the endpoint-description responseArtifactRef',
                )
                record(
                    f'discovery-response-manifest:{entry["entryId"]}',
                    response_doc.get('manifestRef') == manifest['manifestId'],
                    'discovery response manifestRef must match the linked manifest',
                )
                record(
                    f'discovery-response-scope:{entry["entryId"]}',
                    response_doc.get('deploymentScope') == bundle['deploymentScope'],
                    'discovery response deploymentScope must match the release bundle scope',
                )
                record(
                    f'discovery-response-release-label:{entry["entryId"]}',
                    response_doc.get('releaseLabel') == bundle['releaseLabel'],
                    'discovery response release label must match the release bundle',
                )
                reg = response_doc.get('registryRefs', {})
                record(
                    f'discovery-response-registry-refs:{entry["entryId"]}',
                    reg.get('activeArtifactSetRef') == active['activeArtifactSetId'] and reg.get('conformanceClaimSetRef') == claimset['claimSetId'],
                    'discovery response registry refs must point to the linked ActiveArtifactSet and ConformanceClaimSet',
                )
                expected_surfaces = {e['surfaceIdentityRef']: e['manifestSurfaceStatus'] for e in bundle_entries}
                discovery_surfaces = {e['surfaceRef']: e['status'] for e in response_doc.get('surfaceEntries', [])}
                record(
                    f'discovery-response-surface-coverage:{entry["entryId"]}',
                    discovery_surfaces == expected_surfaces,
                    'discovery response surface entries must mirror the release bundle surface identities and statuses',
                )
        elif doc_kind == 'OPENAPI_3_1':
            record(
                f'doc-openapi-version:{entry["entryId"]}',
                str(doc.get('openapi', '')).startswith('3.1'),
                'OpenAPI service-description documents must declare OpenAPI 3.1',
            )
            record(
                f'doc-id:{entry["entryId"]}',
                doc.get('x-ofarm-documentId') == entry['serviceDescriptionId'],
                'OpenAPI x-ofarm-documentId must match the catalog serviceDescriptionId',
            )
            record(
                f'doc-target-surface:{entry["entryId"]}',
                doc.get('x-ofarm-targetSurfaceRef') == entry['targetSurfaceRef'],
                'OpenAPI x-ofarm-targetSurfaceRef must match the catalog targetSurfaceRef',
            )
            record(
                f'doc-linked-contract:{entry["entryId"]}',
                doc.get('x-ofarm-linkedContractRef') == entry['linkedContractRef'],
                'OpenAPI x-ofarm-linkedContractRef must match the catalog linkedContractRef',
            )
            record(
                f'doc-linked-manifest:{entry["entryId"]}',
                doc.get('x-ofarm-linkedManifestRef') == manifest['manifestId'],
                'OpenAPI x-ofarm-linkedManifestRef must match the linked manifest',
            )
            record(
                f'doc-status:{entry["entryId"]}',
                doc.get('x-ofarm-surfaceStatus') == entry['status'],
                'OpenAPI x-ofarm-surfaceStatus must match the catalog status',
            )
            record(
                f'doc-release-label:{entry["entryId"]}',
                doc.get('x-ofarm-releaseLabel') == bundle['releaseLabel'],
                'OpenAPI x-ofarm-releaseLabel must match the release bundle',
            )
            server_urls = [srv.get('url') for srv in doc.get('servers', []) if isinstance(srv, dict)]
            record(
                f'doc-locator:{entry["entryId"]}',
                entry['locator'] in server_urls,
                'OpenAPI servers should include the catalog locator',
            )
        elif doc_kind == 'ASYNCAPI_3_0':
            record(
                f'doc-asyncapi-version:{entry["entryId"]}',
                str(doc.get('asyncapi', '')).startswith('3.0'),
                'AsyncAPI service-description documents must declare AsyncAPI 3.0',
            )
            record(
                f'doc-id:{entry["entryId"]}',
                doc.get('x-ofarm-documentId') == entry['serviceDescriptionId'],
                'AsyncAPI x-ofarm-documentId must match the catalog serviceDescriptionId',
            )
            record(
                f'doc-target-surface:{entry["entryId"]}',
                doc.get('x-ofarm-targetSurfaceRef') == entry['targetSurfaceRef'],
                'AsyncAPI x-ofarm-targetSurfaceRef must match the catalog targetSurfaceRef',
            )
            record(
                f'doc-linked-contract:{entry["entryId"]}',
                doc.get('x-ofarm-linkedContractRef') == entry['linkedContractRef'],
                'AsyncAPI x-ofarm-linkedContractRef must match the catalog linkedContractRef',
            )
            record(
                f'doc-linked-manifest:{entry["entryId"]}',
                doc.get('x-ofarm-linkedManifestRef') == manifest['manifestId'],
                'AsyncAPI x-ofarm-linkedManifestRef must match the linked manifest',
            )
            record(
                f'doc-status:{entry["entryId"]}',
                doc.get('x-ofarm-surfaceStatus') == entry['status'],
                'AsyncAPI x-ofarm-surfaceStatus must match the catalog status',
            )
            record(
                f'doc-release-label:{entry["entryId"]}',
                doc.get('x-ofarm-releaseLabel') == bundle['releaseLabel'],
                'AsyncAPI x-ofarm-releaseLabel must match the release bundle',
            )
            record(
                f'doc-channel-presence:{entry["entryId"]}',
                bool(doc.get('channels')),
                'AsyncAPI service-description documents should expose at least one channel',
            )
        else:
            record(
                f'doc-kind-known:{entry["entryId"]}',
                False,
                f'unknown service-description kind {doc_kind}',
            )

    return {'outcome': 'PASS' if not reasons else 'FAIL', 'checks': checks, 'reasons': reasons}


def main() -> int:
    result: dict[str, Any] = {
        'generatedAt': datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z'),
        'overall': 'PASS_WITH_LIMITATIONS',
        'summary': {
            'activeSchemaValidations': 0,
            'localFixtureFilesChecked': 0,
            'traceabilityChecks': 0,
            'negativeCasesChecked': 0,
            'negativeCasesExpectedFail': 0,
        },
        'activeSchemaValidations': [],
        'localFixtureFiles': [],
        'traceabilityChecks': [],
        'negativeChecks': [],
        'limitations': [
            'This wave is package-local release-traceability proof only and does not fetch live deployment endpoints.',
            'The local discovery/service-description files remain active supporting implementation artifacts, not active semantic/runtime law.',
            'These files do not qualify as live deployment evidence and do not change same-standard bridge promotion posture.',
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
        result['activeSchemaValidations'].append({'exampleFile': example_name, 'schemaFile': schema_name, 'status': 'PASS'})
    result['summary']['activeSchemaValidations'] = len(result['activeSchemaValidations'])

    fixture_paths = [
        IC / 'OFARM_runtime_surface_deployment_release_bundle_example_core_surface_linkage_v0_1.json',
        SVC / 'service_description_catalog_v0_2.json',
        SVC / 'ofarm_capability_discovery_endpoint_description_v0_1.json',
        SVC / 'ofarm_capability_discovery_document_v0_1.json',
        SVC / 'ngsi_ld_export_openapi_v0_1.json',
        SVC / 'ogc_features_query_facade_openapi_v0_1.json',
        SVC / 'semantic_event_ingress_asyncapi_v0_1.json',
    ]
    docs_by_path: dict[str, dict[str, Any]] = {}
    for path in fixture_paths:
        payload = load_json(path)
        rel = path.relative_to(ROOT).as_posix()
        docs_by_path[rel] = payload
        result['localFixtureFiles'].append({'file': rel, 'status': 'PASS'})
    result['summary']['localFixtureFilesChecked'] = len(result['localFixtureFiles'])

    manifest = load_contract('OFARM_Capability_Manifest_example_core_deployment_surface_linkage_v0_2_draft.json')
    active = load_contract('OFARM_ActiveArtifactSet_example_core_deployment_surface_linkage_v0_1.json')
    claimset = load_contract('OFARM_ConformanceClaimSet_example_core_deployment_surface_linkage_v0_1.json')
    contracts = [
        load_contract('OFARM_RuntimeSurfaceContract_example_capability_discovery_v0_2_draft.json'),
        load_contract('OFARM_RuntimeSurfaceContract_example_ngsi_ld_export_v0_2_draft.json'),
        load_contract('OFARM_RuntimeSurfaceContract_example_cql2_query_facade_v0_2_draft.json'),
        load_contract('OFARM_RuntimeSurfaceContract_example_semantic_event_ingress_v0_2_draft.json'),
    ]
    bundle = docs_by_path['04_implementation_and_conformance/implementation_notes/runtime_surface_and_capability/OFARM_runtime_surface_deployment_release_bundle_example_core_surface_linkage_v0_1.json']
    catalog = docs_by_path['04_implementation_and_conformance/service_and_sdk_candidates/service_descriptions/core_surface_linkage_release_v0_1/service_description_catalog_v0_2.json']

    evaluation = evaluate(manifest, active, claimset, contracts, bundle, catalog, docs_by_path)
    result['traceabilityChecks'] = evaluation['checks']
    result['summary']['traceabilityChecks'] = len(evaluation['checks'])
    if evaluation['outcome'] != 'PASS':
        result['overall'] = 'FAIL'

    # Negative cases
    negative_cases: list[tuple[str, dict[str, Any], dict[str, Any], dict[str, Any]]] = []

    neg_bundle = copy.deepcopy(bundle)
    neg_bundle['manifestRef'] = 'manifest:core-deployment:wrong:v9'
    negative_cases.append(('neg-bundle-manifest-drift', neg_bundle, catalog, docs_by_path, 'bundle-manifest-ref'))

    neg_catalog = copy.deepcopy(catalog)
    for entry in neg_catalog['entries']:
        if entry['entryId'] == 'catalog-entry:cql2-query-facade:v1':
            entry['targetSurfaceRef'] = 'surface:wrong-query-surface:v9'
    negative_cases.append(('neg-catalog-target-surface-drift', bundle, neg_catalog, docs_by_path, 'catalog-target-surface:catalog-entry:cql2-query-facade:v1'))

    neg_docs = copy.deepcopy(docs_by_path)
    neg_discovery = copy.deepcopy(neg_docs['04_implementation_and_conformance/service_and_sdk_candidates/service_descriptions/core_surface_linkage_release_v0_1/ofarm_capability_discovery_document_v0_1.json'])
    neg_discovery['manifestRef'] = 'manifest:core-deployment:wrong:v9'
    neg_docs['04_implementation_and_conformance/service_and_sdk_candidates/service_descriptions/core_surface_linkage_release_v0_1/ofarm_capability_discovery_document_v0_1.json'] = neg_discovery
    negative_cases.append(('neg-discovery-manifest-drift', bundle, catalog, neg_docs, 'discovery-response-manifest:catalog-entry:capability-discovery:v1'))

    neg_bundle2 = copy.deepcopy(bundle)
    for entry in neg_bundle2['surfaceReleases']:
        if entry['surfaceContractRef'] == 'surface-contract:cql2-query-facade:v0.2-draft':
            entry['releasePosture'] = 'LIVE_SUPPORTED'
    negative_cases.append(('neg-planned-surface-marked-live', neg_bundle2, catalog, docs_by_path, 'bundle-release-posture:surface-contract:cql2-query-facade:v0.2-draft'))

    for case_id, case_bundle, case_catalog, case_docs, expected_check in negative_cases:
        ev = evaluate(manifest, active, claimset, contracts, case_bundle, case_catalog, case_docs)
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
