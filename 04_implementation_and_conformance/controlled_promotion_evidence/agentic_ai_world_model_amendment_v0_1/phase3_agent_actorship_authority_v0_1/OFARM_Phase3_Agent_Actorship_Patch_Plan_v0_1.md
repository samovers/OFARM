# OFARM Phase 3 Agent Actorship Patch Plan v0.1

Date: 2026-05-14  
Status: patch plan; no active patch applied

## Future promotion target

If promoted, Phase 3 should create an accepted RFC:

- `02_accepted_rfcs/OFARM_Agent_Actorship_and_Authority_RFC_v0_1.md`

and machine contracts:

- `03_machine_contracts/OFARM_SoftwareAgentProfile_schema_v0_1.json`
- `03_machine_contracts/OFARM_AgentInstance_schema_v0_1.json`
- `03_machine_contracts/OFARM_AgentSponsorRef_schema_v0_1.json`
- `03_machine_contracts/OFARM_AgentModelToolProfile_schema_v0_1.json`
- `03_machine_contracts/OFARM_AgentAuthorityEnvelope_schema_v0_1.json`
- `03_machine_contracts/OFARM_AgentRevocationState_schema_v0_1.json`
- `03_machine_contracts/OFARM_AgentActorshipBinding_schema_v0_1.json`
- `03_machine_contracts/OFARM_AgentAuthorizationDecisionTrace_schema_v0_1.json`

## Baseline impact

No immediate baseline rewrite is required. A small pointer may be added later to the Constitution and Platform baseline saying that detailed software-agent actorship is governed by the accepted Agent Actorship RFC.

## RFC dependencies

Phase 4 `AgentRunEnvelope`, `AgentRunTrace`, and `AgentHandoffEnvelope` should depend on this phase rather than duplicate sponsor/profile/instance concepts.

## Promotion hold points

Do not promote until architect review confirms:

- no contradiction with active Authority Policy Model;
- no weakening of human-governed defaults;
- no implicit authorization of autonomous compliance decisioning;
- no hidden truth family is introduced.
