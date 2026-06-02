# OFARM Capability Manifest Agentic Extension RFC v0.1

Date: 2026-05-14  
Status: draft candidate RFC; not accepted baseline law until promoted.  
Role: extend runtime self-description with agent support and world-model support declarations.


## 1. Problem statement

OFARM Capability Manifest support currently describes semantic/runtime support areas, but multi-agent platforms need explicit declarations for agent-callable tools, autonomy, approval, trace, offline operation, external calls, and world-model support.

## 2. Scope

This RFC proposes a Capability Manifest v0.3 extension with:

- `agentSupport`
- `agentToolManifestRefs`
- `worldModelSupport`
- supported run/trace/handoff schema versions
- max autonomy by action class
- preflight and human-approval declarations
- data-learning and cross-farm policies

## 3. Deployment self-description rule

Agent support in a Capability Manifest must describe actual deployment behavior. It must not describe aspirational, planned, or vendor-marketing capabilities.

## 4. agentSupport minimum fields

`agentSupport` should declare:

- supported agent classes
- supported autonomy levels
- maximum autonomy by action class
- human-only action classes
- preflight-required action classes
- supported AgentRunEnvelope versions
- supported AgentRunTrace versions
- supported AgentHandoffEnvelope versions
- AgentToolManifest refs
- offline-agent support
- external-tool-use policy
- farm-data-learning policy
- cross-farm-data-use policy
- revocation handling
- trace retention
- redaction and permission-limited answer policy

## 5. AgentToolManifest relation

The Capability Manifest should point to one or more `OFARM_AgentToolManifest` documents. Each tool should map to a public operation and declare action class, target twin, effect class, autonomy, preflight, approval, output disposition, and trace behavior.

## 6. worldModelSupport minimum fields

If world-model capability is advertised, the manifest must declare:

- supported WorldModelRun schema versions
- supported WorldModelState schema versions
- scenario spec/result support
- allowed target scopes
- advisory-only enforcement
- invalidation support
- bridge generation support
- evidence/observation request support
- whether outputs can be used for high-consequence workflows only after recheck

## 7. Negative cases

The manifest must not:

- create authority by advertisement
- relax human-only defaults
- imply runtime certification before tests execute
- advertise autonomous compliance decisioning unless active OFARM law explicitly allows it
- hide that world-model outputs are Advisory-only

## 8. Machine contracts

Candidate schemas:

- `OFARM_AgentSupportSection_schema_v0_1.json`
- `OFARM_WorldModelSupportSection_schema_v0_1.json`

Existing candidate support:

- `OFARM_AgentToolManifest_schema_v0_1.json` from the prior AI-agent readiness support package, to be promoted only after review.
