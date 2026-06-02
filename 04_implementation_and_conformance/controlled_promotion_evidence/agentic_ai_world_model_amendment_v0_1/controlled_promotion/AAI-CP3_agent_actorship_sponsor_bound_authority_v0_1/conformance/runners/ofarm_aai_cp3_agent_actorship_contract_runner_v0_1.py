#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
import sys
from jsonschema import Draft202012Validator

REPO = Path(__file__).resolve().parents[6]
SCHEMA_EXAMPLES = {
  '03_machine_contracts/schemas/authority/OFARM_SoftwareAgentProfile_schema_v0_1.json': '04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_SoftwareAgentProfile_example_compliance_steward_v0_1.json',
  '03_machine_contracts/schemas/authority/OFARM_AgentInstance_schema_v0_1.json': '04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_AgentInstance_example_compliance_steward_field17_v0_1.json',
  '03_machine_contracts/schemas/authority/OFARM_AgentSponsorRef_schema_v0_1.json': '04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_AgentSponsorRef_example_farmer_operator_field17_v0_1.json',
  '03_machine_contracts/schemas/authority/OFARM_AgentModelToolProfile_schema_v0_1.json': '04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_AgentModelToolProfile_example_compliance_steward_v0_1.json',
  '03_machine_contracts/schemas/authority/OFARM_AgentAuthorityEnvelope_schema_v0_1.json': '04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_AgentAuthorityEnvelope_example_preflight_requires_human_approval_v0_1.json',
  '03_machine_contracts/schemas/authority/OFARM_AgentRevocationState_schema_v0_1.json': '04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_AgentRevocationState_example_no_active_revocation_v0_1.json',
  '03_machine_contracts/schemas/authority/OFARM_AgentActorshipBinding_schema_v0_1.json': '04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_AgentActorshipBinding_example_compliance_steward_field17_v0_1.json',
  '03_machine_contracts/schemas/authority/OFARM_AgentAuthorizationDecisionTrace_schema_v0_1.json': '04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_AgentAuthorizationDecisionTrace_example_preflight_requires_approval_v0_1.json'
}
NEG_DIR = REPO / '04_implementation_and_conformance/controlled_promotion_evidence/agentic_ai_world_model_amendment_v0_1/controlled_promotion/AAI-CP3_agent_actorship_sponsor_bound_authority_v0_1/examples/negative'

def load(rel):
    return json.loads((REPO/rel).read_text(encoding='utf-8'))

def main():
    failures = []
    records = []
    for schema_rel, example_rel in SCHEMA_EXAMPLES.items():
        schema = load(schema_rel)
        example = load(example_rel)
        errors = sorted(Draft202012Validator(schema).iter_errors(example), key=lambda e: e.path)
        if errors:
            failures.append({'example': example_rel, 'schema': schema_rel, 'errors': [e.message for e in errors]})
        records.append({'type':'schema_validation','schema':schema_rel,'example':example_rel,'status':'PASS' if not errors else 'FAIL'})

    binding = load('04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_AgentActorshipBinding_example_compliance_steward_field17_v0_1.json')
    if not binding.get('noSilentDelegation') or not binding.get('notAuthorityGrant'):
        failures.append({'policy':'binding_flags','status':'FAIL'})
    envelope = load('04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/authority/OFARM_AgentAuthorityEnvelope_example_preflight_requires_human_approval_v0_1.json')
    for key in ['agentSponsorRef','executingAgentInstanceRef','authoritySnapshotRef','revocationStateRef','authorizationDecisionTraceRef']:
        if not envelope.get(key): failures.append({'policy':'envelope_required_policy_field','missing':key})
    if envelope.get('finalActionPermitted') is True and envelope.get('humanApprovalRequired') is True:
        failures.append({'policy':'human_approval_required_cannot_be_final_permitted','status':'FAIL'})

    for p in sorted(NEG_DIR.glob('*.json')):
        obj=json.loads(p.read_text(encoding='utf-8'))
        cid=obj.get('caseId')
        cand=obj.get('candidate',{})
        should_fail=False
        if cid=='CP3-NEG-001': should_fail = 'agentSponsorRef' not in cand
        elif cid=='CP3-NEG-002': should_fail = str(cand.get('authoritySnapshotRef','')).startswith('tool:')
        elif cid=='CP3-NEG-003': should_fail = cand.get('revocationResult')=='ACTIVE_REVOCATION_FOUND' and cand.get('finalActionPermitted') is True
        elif cid=='CP3-NEG-004': should_fail = cand.get('noSilentDelegation') is False or cand.get('delegatedRights')=='implicit'
        else: should_fail = False
        records.append({'type':'negative_policy','caseId':cid,'path':str(p.relative_to(REPO)),'status':'PASS' if should_fail else 'FAIL'})
        if not should_fail: failures.append({'negative_policy_not_detected':str(p.relative_to(REPO))})
    result={'status':'PASS' if not failures else 'FAIL','records':records,'failures':failures}
    print(json.dumps(result, indent=2))
    return 0 if not failures else 1
if __name__=='__main__': raise SystemExit(main())
