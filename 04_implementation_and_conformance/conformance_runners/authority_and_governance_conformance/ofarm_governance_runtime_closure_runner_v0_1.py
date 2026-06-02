#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Dict, List

try:
    import jsonschema
except ImportError as e:
    raise SystemExit('jsonschema is required for this validator') from e

ROOT = Path(__file__).resolve().parents[1]
MC = ROOT / '03_machine_contracts'
FIX = Path(__file__).resolve().parent / 'ofarm_governance_runtime_fixtures_v0_1'
OUT = Path(__file__).resolve().parent / 'OFARM_governance_runtime_closure_results_v0_1.json'

SCHEMAS = [
    'OFARM_Capability_Manifest_schema_v0_1.json',
    'OFARM_PackActivationSet_schema_v0_1.json',
    'OFARM_ActiveArtifactSet_schema_v0_1.json',
    'OFARM_RuntimeProblem_schema_v0_1.json',
    'OFARM_PackActivationRequest_schema_v0_1.json',
    'OFARM_PackActivationResult_schema_v0_1.json',
    'OFARM_DataSovereigntyBoundary_schema_v0_1.json',
    'OFARM_PackCompatibilityDeclaration_schema_v0_1.json',
    'OFARM_PackMergePolicy_schema_v0_1.json',
    'OFARM_PackExclusionRule_schema_v0_1.json',
]

EXAMPLES = [
    ('OFARM_Capability_Manifest_schema_v0_1.json', 'OFARM_Capability_Manifest_example_core_deployment_v0_1.json'),
    ('OFARM_Capability_Manifest_schema_v0_1.json', 'OFARM_Capability_Manifest_example_partner_deployment_v0_1.json'),
    ('OFARM_PackActivationSet_schema_v0_1.json', 'OFARM_PackActivationSet_example_field_orchard_activation_v0_1.json'),
    ('OFARM_ActiveArtifactSet_schema_v0_1.json', 'OFARM_ActiveArtifactSet_example_core_deployment_v0_1.json'),
    ('OFARM_ActiveArtifactSet_schema_v0_1.json', 'OFARM_ActiveArtifactSet_example_partner_deployment_v0_1.json'),
    ('OFARM_ActiveArtifactSet_schema_v0_1.json', 'OFARM_ActiveArtifactSet_example_partner_missing_orchard_v0_1.json'),
    ('OFARM_RuntimeProblem_schema_v0_1.json', 'OFARM_RuntimeProblem_example_pack_conflict_v0_1.json'),
    ('OFARM_PackActivationRequest_schema_v0_1.json', 'OFARM_PackActivationRequest_example_field_orchard_plan_v0_1.json'),
    ('OFARM_PackActivationRequest_schema_v0_1.json', 'OFARM_PackActivationRequest_example_field_23_conflict_v0_1.json'),
    ('OFARM_PackActivationResult_schema_v0_1.json', 'OFARM_PackActivationResult_example_allow_orchard_v0_1.json'),
    ('OFARM_PackActivationResult_schema_v0_1.json', 'OFARM_PackActivationResult_example_hard_fail_template_conflict_v0_1.json'),
    ('OFARM_DataSovereigntyBoundary_schema_v0_1.json', 'OFARM_DataSovereigntyBoundary_example_farm_ana_kovac_operational_boundary_v0_1.json'),
    ('OFARM_PackCompatibilityDeclaration_schema_v0_1.json', 'OFARM_PackCompatibilityDeclaration_example_slovenia_organic_orchard_merge_v0_1.json'),
    ('OFARM_PackMergePolicy_schema_v0_1.json', 'OFARM_PackMergePolicy_example_evidence_policy_organic_orchard_v0_1.json'),
    ('OFARM_PackExclusionRule_schema_v0_1.json', 'OFARM_PackExclusionRule_example_orchard_template_exclusive_v0_1.json'),
]

MANIFEST_FIXTURES = [
    'manifest_consistency_core_match.json',
    'manifest_consistency_partner_match.json',
    'manifest_consistency_partner_mismatch_missing_orchard.json',
]

PACK_ACTIVATION_FIXTURES = [
    'pack_activation_evidence_merge_allow.json',
    'pack_activation_template_conflict_deny.json',
    'pack_activation_decision_rule_governance_required.json',
    'pack_activation_scope_separation_allow.json',
]


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding='utf-8'))


def validate_manifest_against_active_state(manifest: Dict[str, Any], active_state: Dict[str, Any]) -> Dict[str, Any]:
    reasons: List[str] = []
    outcome = 'PASS'

    if manifest['registryRelation']['activeArtifactSetRef'] != active_state['activeArtifactSetId']:
        reasons.append('registryRelation.activeArtifactSetRef does not match activeArtifactSetId')
    if manifest['registryRelation']['artifactRegistryRef'] != active_state['artifactRegistryRef']:
        reasons.append('registryRelation.artifactRegistryRef does not match active artifact state')
    if manifest['deploymentScope'] != active_state['deploymentScope']:
        reasons.append('deploymentScope does not match active artifact state')

    manifest_packs = set(manifest['capabilitySections']['packSupport'].get('activePackRefs', []))
    active_packs = set(active_state.get('activePackRefs', []))
    missing_packs = sorted(manifest_packs - active_packs)
    if missing_packs:
        reasons.append('manifest activePackRefs missing from active artifact state: ' + ', '.join(missing_packs))

    manifest_profiles = set(manifest['capabilitySections']['packSupport'].get('activeProfileRefs', []))
    active_profiles = set(active_state.get('activeProfileRefs', []))
    missing_profiles = sorted(manifest_profiles - active_profiles)
    if missing_profiles:
        reasons.append('manifest activeProfileRefs missing from active artifact state: ' + ', '.join(missing_profiles))

    if reasons:
        outcome = 'FAIL'
    return {'outcome': outcome, 'reasons': reasons}


def evaluate_pack_activation(facts: Dict[str, Any]) -> Dict[str, Any]:
    if not facts.get('dependenciesSatisfied', True):
        return {'outcome': 'DENY_ACTIVATION', 'compatibilityClass': 'EXCLUSIVE', 'reasonCode': 'PACK_DEPENDENCY_MISSING'}
    if facts.get('declaredExclusions'):
        return {'outcome': 'DENY_ACTIVATION', 'compatibilityClass': 'EXCLUSIVE', 'reasonCode': 'PACK_EXCLUSION_DECLARED'}
    if facts.get('scopeSeparated'):
        return {'outcome': 'ALLOW_ACTIVATION', 'compatibilityClass': 'COMPATIBLE_BY_SCOPE_SEPARATION', 'reasonCode': 'PACK_SCOPE_SEPARATION'}

    compatibility = 'COMPATIBLE'
    reason_code = 'NONE'

    for overlap in facts.get('overlaps', []):
        if overlap.get('governanceRequired'):
            return {
                'outcome': 'GOVERNANCE_REQUIRED',
                'compatibilityClass': 'GOVERNANCE_REQUIRED',
                'reasonCode': 'PACK_GOVERNANCE_REVIEW_REQUIRED'
            }
        if overlap.get('contradictory'):
            if overlap.get('precedenceRelationship') == 'SAME_PRECEDENCE':
                return {
                    'outcome': 'DENY_ACTIVATION',
                    'compatibilityClass': 'EXCLUSIVE',
                    'reasonCode': 'PACK_SAME_PRECEDENCE_CONFLICT'
                }
            return {
                'outcome': 'DENY_ACTIVATION',
                'compatibilityClass': 'EXCLUSIVE',
                'reasonCode': 'PACK_PRECEDENCE_CONTRADICTION'
            }
        if overlap.get('declaredMergeMode') and overlap.get('safe'):
            compatibility = 'COMPATIBLE_WITH_DECLARED_MERGE'

    return {'outcome': 'ALLOW_ACTIVATION', 'compatibilityClass': compatibility, 'reasonCode': reason_code}


def main() -> int:
    result: Dict[str, Any] = {
        'schemaChecks': {},
        'exampleValidation': {},
        'manifestConsistency': {},
        'packActivationFixtures': {},
        'overall': 'PASS'
    }

    schemas: Dict[str, Any] = {}
    for schema_name in SCHEMAS:
        path = MC / schema_name
        try:
            schema = load_json(path)
            jsonschema.Draft202012Validator.check_schema(schema)
            schemas[schema_name] = schema
            result['schemaChecks'][schema_name] = 'PASS'
        except Exception as e:
            result['schemaChecks'][schema_name] = f'FAIL: {e}'
            result['overall'] = 'FAIL'

    for schema_name, example_name in EXAMPLES:
        key = f'{example_name} :: {schema_name}'
        try:
            data = load_json(MC / example_name)
            jsonschema.validate(data, schemas[schema_name])
            result['exampleValidation'][key] = 'PASS'
        except Exception as e:
            result['exampleValidation'][key] = f'FAIL: {e}'
            result['overall'] = 'FAIL'

    for fixture_name in MANIFEST_FIXTURES:
        fixture = load_json(FIX / fixture_name)
        manifest = load_json(MC / fixture['manifestFile'])
        active_state = load_json(MC / fixture['activeArtifactSetFile'])
        actual = validate_manifest_against_active_state(manifest, active_state)
        status = 'PASS' if actual['outcome'] == fixture['expectedOutcome'] else 'FAIL'
        result['manifestConsistency'][fixture['fixtureId']] = {
            'status': status,
            'actual': actual,
            'expectedOutcome': fixture['expectedOutcome']
        }
        if status == 'FAIL':
            result['overall'] = 'FAIL'

    for fixture_name in PACK_ACTIVATION_FIXTURES:
        fixture = load_json(FIX / fixture_name)
        actual = evaluate_pack_activation(fixture['facts'])
        expected = fixture['expectedOutcome']
        status = 'PASS' if all(actual.get(k) == v for k, v in expected.items()) else 'FAIL'
        result['packActivationFixtures'][fixture['fixtureId']] = {
            'status': status,
            'actual': actual,
            'expected': expected
        }
        if status == 'FAIL':
            result['overall'] = 'FAIL'

    OUT.write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(OUT)
    print(result['overall'])
    return 0 if result['overall'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
