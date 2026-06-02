#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[6]
SCHEMA_DIR = ROOT / '03_machine_contracts/schemas/agent_manifest'
EXAMPLE_DIR = ROOT / '04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agent_manifest'
CP5_DIR = ROOT / '04_implementation_and_conformance/controlled_promotion_evidence/agentic_ai_world_model_amendment_v0_1/controlled_promotion/AAI-CP5_capability_tool_manifest_honesty_v0_1'

SCHEMA_BY_EXAMPLE = {
    'OFARM_AgentToolEffectClassification_example_evidence_candidate_v0_1.json':'OFARM_AgentToolEffectClassification_schema_v0_1.json',
    'OFARM_AgentToolApprovalRequirement_example_evidence_candidate_v0_1.json':'OFARM_AgentToolApprovalRequirement_schema_v0_1.json',
    'OFARM_AgentToolSemanticPrecondition_example_authority_not_revoked_v0_1.json':'OFARM_AgentToolSemanticPrecondition_schema_v0_1.json',
    'OFARM_AgentExternalCallPolicy_example_no_external_calls_v0_1.json':'OFARM_AgentExternalCallPolicy_schema_v0_1.json',
    'OFARM_AgentTraceRetentionPolicy_example_governed_run_minimum_v0_1.json':'OFARM_AgentTraceRetentionPolicy_schema_v0_1.json',
    'OFARM_RedactionAndPermissionLimitedResultPolicy_example_permission_limited_v0_1.json':'OFARM_RedactionAndPermissionLimitedResultPolicy_schema_v0_1.json',
    'OFARM_AgentDataLearningPolicy_example_no_training_v0_1.json':'OFARM_AgentDataLearningPolicy_schema_v0_1.json',
    'OFARM_AgentToolDeclaredHintSet_example_untrusted_read_hint_v0_1.json':'OFARM_AgentToolDeclaredHintSet_schema_v0_1.json',
    'OFARM_AgentCapabilityReadinessClaimLimit_example_static_validated_v0_1.json':'OFARM_AgentCapabilityReadinessClaimLimit_schema_v0_1.json',
    'OFARM_AgentToolDescriptor_example_evidence_label_classifier_v0_1.json':'OFARM_AgentToolDescriptor_schema_v0_1.json',
    'OFARM_AgentSupportSection_example_static_only_v0_1.json':'OFARM_AgentSupportSection_schema_v0_1.json',
    'OFARM_AgentToolManifest_example_evidence_tools_v0_1.json':'OFARM_AgentToolManifest_schema_v0_1.json',
    'OFARM_AgenticCapabilityManifestOverlay_example_static_only_v0_1.json':'OFARM_AgenticCapabilityManifestOverlay_schema_v0_1.json'
}

def load(p: Path):
    return json.loads(p.read_text(encoding='utf-8'))

def main() -> int:
    failures = []
    records = []
    for example_name, schema_name in SCHEMA_BY_EXAMPLE.items():
        ep = EXAMPLE_DIR / example_name
        sp = SCHEMA_DIR / schema_name
        if not ep.exists():
            failures.append(f'missing example {ep}')
            continue
        if not sp.exists():
            failures.append(f'missing schema {sp}')
            continue
        schema = load(sp)
        instance = load(ep)
        errors = sorted(Draft202012Validator(schema).iter_errors(instance), key=lambda e: e.path)
        if errors:
            failures.append(f'{example_name} failed {schema_name}: ' + '; '.join(e.message for e in errors[:5]))
        records.append({'example': str(ep.relative_to(ROOT)), 'schema': str(sp.relative_to(ROOT)), 'status': 'PASS' if not errors else 'FAIL'})
    # Positive semantic policy checks
    manifest = load(EXAMPLE_DIR / 'OFARM_AgentToolManifest_example_evidence_tools_v0_1.json')
    if not manifest.get('manifestDoesNotGrantAuthority') or not manifest.get('toolHintsAreNonAuthoritative') or not manifest.get('manifestIsNotGovernanceSuccess'):
        failures.append('positive manifest does not preserve non-authoritative flags')
    if manifest.get('runtimeConformanceClaimed') is not False:
        failures.append('positive manifest claims runtime conformance')
    desc = load(EXAMPLE_DIR / 'OFARM_AgentToolDescriptor_example_evidence_label_classifier_v0_1.json')
    if desc.get('descriptorDoesNotGrantAuthority') is not True:
        failures.append('positive descriptor grants or implies authority')
    claim = load(EXAMPLE_DIR / 'OFARM_AgentCapabilityReadinessClaimLimit_example_static_validated_v0_1.json')
    if claim.get('claimStatus') not in {'DECLARED_ONLY','STATIC_SCHEMA_VALIDATED','STATIC_EXAMPLE_VALIDATED'}:
        failures.append('positive readiness claim exceeds CP5 static posture')
    # Negative fixture checks
    for fname, expected in [
        ('OFARM_CP5_negative_read_only_hint_hidden_write_v0_1.json','DECLARED_HINT_CONFLICTS_WITH_EFFECT_CLASS'),
        ('OFARM_CP5_negative_hidden_external_egress_v0_1.json','HIDDEN_EXTERNAL_EGRESS'),
        ('OFARM_CP5_negative_runtime_claim_without_evidence_v0_1.json','RUNTIME_CLAIM_WITHOUT_EVIDENCE')
    ]:
        fp = CP5_DIR / 'examples/negative' / fname
        fx = load(fp)
        if fx.get('expectedPolicyOutcome') != 'BLOCKED':
            failures.append(f'{fname} expectedPolicyOutcome is not BLOCKED')
        if expected not in fx.get('expectedReasonCodes', []):
            failures.append(f'{fname} missing expected reason code {expected}')
        records.append({'negativeFixture': str(fp.relative_to(ROOT)), 'status':'PASS_EXPECTED_BLOCK'})
    # Active non-promotion check.
    if (SCHEMA_DIR / 'OFARM_WorldModelSupportSection_schema_v0_1.json').exists():
        failures.append('WorldModelSupportSection was promoted in CP5, but CP5 must not promote world-model support')
    result = {'schemaVersion':'ofarm.cp5.validationReport.v0.1','phase':'AAI-CP5','status':'PASS' if not failures else 'FAIL','records':records,'failures':failures}
    print(json.dumps(result, indent=2))
    return 0 if not failures else 1

if __name__ == '__main__':
    raise SystemExit(main())
