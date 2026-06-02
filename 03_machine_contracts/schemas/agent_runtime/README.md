# schemas / agent_runtime

Status: active machine-contract family by AAI-CP4  
Updated: 2026-05-18T00:00:00+02:00

Files in this folder are grouped for findability only. Semantic authority and default status are governed by active OFARM law and the contract indexes at `03_machine_contracts/`.

AAI-CP4 promotes bounded agent run, trace, approval-checkpoint, blocked-action, freshness, input-bundle, stop-condition, tool-invocation, output-disposition, and handoff-envelope contracts.

Governing RFC: `02_accepted_rfcs/OFARM_Agent_Run_Envelope_Trace_and_Handoff_RFC_v0_1.md`

## Promoted families

- `AgentBlockedActionTrace`
- `AgentHandoffEnvelope`
- `AgentOutputDisposition`
- `AgentRunApprovalCheckpoint`
- `AgentRunEnvelope`
- `AgentRunFreshnessRequirement`
- `AgentRunInputBundle`
- `AgentRunStopCondition`
- `AgentRunTrace`
- `AgentToolInvocationTrace`

## Files

- `OFARM_AgentBlockedActionTrace_schema_v0_1.json`
- `OFARM_AgentHandoffEnvelope_schema_v0_1.json`
- `OFARM_AgentOutputDisposition_schema_v0_1.json`
- `OFARM_AgentRunApprovalCheckpoint_schema_v0_1.json`
- `OFARM_AgentRunEnvelope_schema_v0_1.json`
- `OFARM_AgentRunFreshnessRequirement_schema_v0_1.json`
- `OFARM_AgentRunInputBundle_schema_v0_1.json`
- `OFARM_AgentRunStopCondition_schema_v0_1.json`
- `OFARM_AgentRunTrace_schema_v0_1.json`
- `OFARM_AgentToolInvocationTrace_schema_v0_1.json`

## Non-claims

These schemas do not establish full runtime AI-agent readiness, autonomous compliance decisioning, two-agent compatibility, or authority to mutate current state. Authority remains sponsor-bound and governed by the authority/action matrix and runtime enforcement chain.

Examples for this family live under `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/agent_runtime/` and are mapped by `03_machine_contracts/EXAMPLE_SCHEMA_MAP.json`.
