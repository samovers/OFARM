#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from jsonschema import Draft202012Validator

REPO = Path(__file__).resolve().parents[6]
SCHEMA_EXAMPLES = {
  '03_machine_contracts/schemas/agent_runtime/OFARM_AgentRunInputBundle_schema_v0_1.json': '04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agent_runtime/OFARM_AgentRunInputBundle_example_label_capture_v0_1.json',
  '03_machine_contracts/schemas/agent_runtime/OFARM_AgentRunFreshnessRequirement_schema_v0_1.json': '04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agent_runtime/OFARM_AgentRunFreshnessRequirement_example_evidence_capture_v0_1.json',
  '03_machine_contracts/schemas/agent_runtime/OFARM_AgentRunStopCondition_schema_v0_1.json': '04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agent_runtime/OFARM_AgentRunStopCondition_example_human_governed_action_v0_1.json',
  '03_machine_contracts/schemas/agent_runtime/OFARM_AgentRunApprovalCheckpoint_schema_v0_1.json': '04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agent_runtime/OFARM_AgentRunApprovalCheckpoint_example_pack_activation_denied_v0_1.json',
  '03_machine_contracts/schemas/agent_runtime/OFARM_AgentRunEnvelope_schema_v0_1.json': '04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agent_runtime/OFARM_AgentRunEnvelope_example_evidence_steward_capture_v0_1.json',
  '03_machine_contracts/schemas/agent_runtime/OFARM_AgentToolInvocationTrace_schema_v0_1.json': '04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agent_runtime/OFARM_AgentToolInvocationTrace_example_label_classifier_v0_1.json',
  '03_machine_contracts/schemas/agent_runtime/OFARM_AgentOutputDisposition_schema_v0_1.json': '04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agent_runtime/OFARM_AgentOutputDisposition_example_evidence_candidate_v0_1.json',
  '03_machine_contracts/schemas/agent_runtime/OFARM_AgentBlockedActionTrace_schema_v0_1.json': '04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agent_runtime/OFARM_AgentBlockedActionTrace_example_attempt_pack_activation_v0_1.json',
  '03_machine_contracts/schemas/agent_runtime/OFARM_AgentHandoffEnvelope_schema_v0_1.json': '04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agent_runtime/OFARM_AgentHandoffEnvelope_example_scouting_to_planning_v0_1.json',
  '03_machine_contracts/schemas/agent_runtime/OFARM_AgentRunTrace_schema_v0_1.json': '04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agent_runtime/OFARM_AgentRunTrace_example_evidence_steward_capture_allowed_v0_1.json'
}
NEG_DIR = REPO / '04_implementation_and_conformance/controlled_promotion_evidence/agentic_ai_world_model_amendment_v0_1/controlled_promotion/AAI-CP4_agent_run_trace_handoff_v0_1/examples/negative'

def load(rel):
    return json.loads((REPO/rel).read_text(encoding='utf-8'))

def main():
    failures=[]; records=[]
    for schema_rel, example_rel in SCHEMA_EXAMPLES.items():
        schema=load(schema_rel); example=load(example_rel)
        errors=sorted(Draft202012Validator(schema).iter_errors(example), key=lambda e:e.path)
        records.append({'type':'schema_validation','schema':schema_rel,'example':example_rel,'status':'PASS' if not errors else 'FAIL'})
        if errors: failures.append({'schema':schema_rel,'example':example_rel,'errors':[e.message for e in errors]})
    run_env=load('04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agent_runtime/OFARM_AgentRunEnvelope_example_evidence_steward_capture_v0_1.json')
    run_trace=load('04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agent_runtime/OFARM_AgentRunTrace_example_evidence_steward_capture_allowed_v0_1.json')
    handoff=load('04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agent_runtime/OFARM_AgentHandoffEnvelope_example_scouting_to_planning_v0_1.json')
    blocked=load('04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agent_runtime/OFARM_AgentBlockedActionTrace_example_attempt_pack_activation_v0_1.json')
    tool=load('04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agent_runtime/OFARM_AgentToolInvocationTrace_example_label_classifier_v0_1.json')
    if run_env.get('traceRequired') is not True or run_env.get('blockedActionTraceRequired') is not True or run_env.get('resultQualificationRequired') is not True:
        failures.append({'policy':'run_envelope_required_trace_flags','status':'FAIL'})
    if not run_trace.get('traceRetrievalRef') or not run_trace.get('resultQualificationRefs'):
        failures.append({'policy':'run_trace_missing_trace_retrieval_or_qualification','status':'FAIL'})
    if not run_trace.get('blockedActionTraceRefs'):
        failures.append({'policy':'run_trace_missing_blocked_action_trace_refs','status':'FAIL'})
    if handoff.get('authorityTransferred') is not False or handoff.get('receivingAgentMustReauthorize') is not True:
        failures.append({'policy':'handoff_no_authority_transfer','status':'FAIL'})
    if not handoff.get('nonDelegatedRights') or not handoff.get('requiredRevalidationChecks'):
        failures.append({'policy':'handoff_missing_non_delegated_rights_or_revalidation','status':'FAIL'})
    if blocked.get('acceptedFarmFactCreated') is not False or blocked.get('blockedBeforeSideEffect') is not True:
        failures.append({'policy':'blocked_action_should_not_create_fact','status':'FAIL'})
    if tool.get('toolResultState') == 'CALL_SUCCEEDED' and tool.get('toolSuccessIsNotGovernanceSuccess') is not True:
        failures.append({'policy':'tool_success_not_governance_success','status':'FAIL'})
    for p in sorted(NEG_DIR.glob('*.json')):
        obj=json.loads(p.read_text(encoding='utf-8')); cid=obj.get('caseId'); cand=obj.get('candidate',{})
        should_fail=False
        if cid=='CP4-NEG-001': should_fail = cand.get('authorityTransferred') is True or cand.get('receivingAgentMustReauthorize') is False
        elif cid=='CP4-NEG-002': should_fail = cand.get('toolResultState')=='CALL_SUCCEEDED' and cand.get('authorizationPosture') in {'DENIED','REQUIRE_REVIEW','NOT_EVALUATED'} and cand.get('governanceOutcome')=='PASS'
        elif cid=='CP4-NEG-003': should_fail = cand.get('attemptedForbiddenActionClass') and not cand.get('blockedActionTraceRefs')
        elif cid=='CP4-NEG-004': should_fail = any(str(x).startswith('agent_memory:') for x in cand.get('evidenceBasisRefs',[])) and cand.get('acceptedFarmFactCreated') is True
        elif cid=='CP4-NEG-005': should_fail = cand.get('freshnessEvaluationResult','').startswith('FAIL') and not cand.get('resultQualificationRefs')
        elif cid=='CP4-NEG-006': should_fail = cand.get('traceRequired') is True and (not cand.get('traceRetrievalRef') or not cand.get('resultQualificationRefs'))
        records.append({'type':'negative_policy','caseId':cid,'path':str(p.relative_to(REPO)),'status':'PASS' if should_fail else 'FAIL'})
        if not should_fail: failures.append({'negative_policy_not_detected':str(p.relative_to(REPO))})
    result={'status':'PASS' if not failures else 'FAIL','records':records,'failures':failures}
    print(json.dumps(result, indent=2))
    return 0 if not failures else 1
if __name__=='__main__': raise SystemExit(main())
