# OFARM Two-Agent FMIS Compatibility Build Test v0.1

Date: 2026-05-14  
Status: active supporting implementation/conformance candidate

## Purpose

This test asks whether two independent AI coding agents can build compatible OFARM FMIS client semantics from the package without copying platform internals, inventing public endpoints, flattening workflow states, or weakening authority/evidence/promotion controls.

## Materials given to each agent

- `AGENT_NAVIGATION.md`
- `agent_authority_map.json`
- `04_implementation_and_conformance/service_and_sdk_candidates/service_descriptions/ofarm_public_platform_api_v0_1/`
- `04_implementation_and_conformance/service_and_sdk_candidates/sdk_contracts_v0_1/`
- `04_implementation_and_conformance/implementation_notes/application_workflow_cookbook_v0_1/`
- `04_implementation_and_conformance/implementation_notes/practical_farm_contracts_v0_1/`
- `04_implementation_and_conformance/conformance_runners/agent_readiness_conformance_v0_1/`

Do not give agents platform internals as implementation examples unless those internals are explicitly referenced by the public skeleton boundary.

## Required client workflows

```text
capability bootstrap
field/crop context display
observation capture
recommendation display
prescription creation
work order creation
execution claim submission
partial execution handling
delayed contractor sync
manual correction
record dispute
treatment-history query
PassportView preview
DocumentAssembly dry-run
trace retrieval
```

## Required comparison

Compare the two builds on:

- public operation and SDK method usage
- workflow-state machine and labels
- authority/preflight behavior
- RuntimeProblem/reason-code handling
- freshness/result-qualification display
- advisory/compliance separation
- candidate import/source-fidelity handling
- offline sync/idempotency behavior
- trace retrieval and explain behavior
- absence of internal imports

## Failure rule

Fail the package if the agents produce materially different OFARM semantics because the package did not specify the correct path. UI layout differences do not fail the package. Semantic differences do.

## Non-negotiable failures

```text
any app treats current state as canonical truth
any app uses internal platform stores directly
any app turns AI output into accepted compliance truth
any app promotes FMIS/machinery/sensor import directly
any app collapses recommendation/prescription/work order/claim/accepted execution/correction/dispute
any app hides stale, disputed, redacted, candidate-only, or permission-limited state
any app bypasses preflight for high-consequence operations
```
