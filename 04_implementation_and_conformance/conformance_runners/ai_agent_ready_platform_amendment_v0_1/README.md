# OFARM AI-Agent-Ready Platform Implementation Amendment v0.1

Date: 2026-05-13  
Status: active supporting implementation/conformance candidate patch  
Scope: Phase 0–9 implementation-facing closure for AI coding-agent readiness

## Purpose

This amendment package turns reviewer findings and the attached deep-research intake into concrete, repository-relative artifacts. It is designed to help future AI coding agents implement OFARM Platform without:

- flattening OFARM into CRUD
- treating materializations as hidden truth stores
- inventing public APIs
- copying platform internals into apps
- bypassing authority, evidence, pack, promotion, or publication gates
- making AI output a governance decision
- hiding stale, disputed, redacted, candidate-only, or evidence-insufficient app results

## Authority posture

This patch is additive. It does not edit active baseline files. It introduces candidate implementation-facing artifacts that may later be promoted into companion artifacts, accepted RFCs, and machine contracts.

Active baseline law still wins:

1. `00_active_baseline/`
2. `02_accepted_rfcs/`
3. `01_companion_artifacts/`
4. `03_machine_contracts/`
5. this amendment package under `04_implementation_and_conformance/`

## Included phases

| Phase | Included in this package | Primary output |
|---|---:|---|
| 0 | yes | agent navigation and authority guardrails |
| 1 | yes | platform module boundary map |
| 2 | yes | public application surface draft RFC and schemas |
| 3 | yes | AI agent use policy, preflight/explain draft RFC, RuntimeProblem reason-code draft RFC |
| 4 | yes | query, current-state display/cache, result qualification, output preview/assembly app contracts, workflow cookbook, UI-state matrix, and golden/hard path app demos |
| 5 | yes | workflow cookbook, UI-safe state matrix, golden/hard path app demos |
| 6 | yes | practical farm contracts: calculation/unit service, identity/deduplication, source-fidelity/loss maps, offline sync, FMIS shadow import, minimum capture boundaries |
| 7 | yes | SDK/API bundle and reference platform skeleton |
| 8 | yes | agent conformance and break tests |
| 9 | yes | baseline harmonization readiness, promotion candidates, unresolved gate register, and draft non-applied baseline patch proposals |
| 10+ | backlog | active baseline patching only after promotion review and unresolved gates close where required |

## Main artifacts

```text
AGENT_NAVIGATION.md
agent_authority_map.json
04_implementation_and_conformance/conformance_runners/ai_agent_ready_platform_amendment_v0_1/OFARM_Platform_Module_Boundary_Map_v0_1.md
04_implementation_and_conformance/conformance_runners/ai_agent_ready_platform_amendment_v0_1/draft_rfcs/OFARM_Application_Builder_Surface_RFC_v0_1.md
04_implementation_and_conformance/conformance_runners/ai_agent_ready_platform_amendment_v0_1/draft_rfcs/OFARM_Preflight_DryRun_and_Explain_Surface_RFC_v0_1.md
04_implementation_and_conformance/conformance_runners/ai_agent_ready_platform_amendment_v0_1/draft_rfcs/OFARM_RuntimeProblem_Reason_Code_Registry_RFC_v0_1.md
04_implementation_and_conformance/conformance_runners/ai_agent_ready_platform_amendment_v0_1/draft_rfcs/OFARM_Publication_and_Output_Assembly_Surface_RFC_v0_1.md
04_implementation_and_conformance/conformance_runners/ai_agent_ready_platform_amendment_v0_1/draft_companion/OFARM_AI_Agent_Use_and_Autonomy_Policy_v0_1.md
04_implementation_and_conformance/conformance_runners/ai_agent_ready_platform_amendment_v0_1/draft_companion/OFARM_Current_State_App_Display_and_Cache_Policy_v0_1.md
04_implementation_and_conformance/conformance_runners/ai_agent_ready_platform_amendment_v0_1/draft_companion/OFARM_Query_Result_Display_and_Freshness_Policy_v0_1.md
04_implementation_and_conformance/conformance_runners/ai_agent_ready_platform_amendment_v0_1/draft_companion/OFARM_Application_Workflow_State_Matrix_v0_1.md
04_implementation_and_conformance/conformance_runners/ai_agent_ready_platform_amendment_v0_1/draft_companion/OFARM_Application_Workflow_Cookbook_Policy_v0_1.md
04_implementation_and_conformance/implementation_notes/application_workflow_cookbook_v0_1/README.md
04_implementation_and_conformance/implementation_notes/golden_path_application_demo_v0_1/README.md
04_implementation_and_conformance/implementation_notes/hard_path_application_demo_v0_1/README.md
04_implementation_and_conformance/conformance_runners/ai_agent_ready_platform_amendment_v0_1/draft_machine_contracts/
04_implementation_and_conformance/implementation_notes/query_cookbook_v0_1/
04_implementation_and_conformance/examples_and_fixtures/output_assembly_examples_v0_1/
04_implementation_and_conformance/service_and_sdk_candidates/service_descriptions/ofarm_public_platform_api_v0_1/
```

## Phase 4 control line

Phase 4 is the query/current-state/output app-contract closure. It adds result-qualification and public-read envelopes so that AI-built applications preserve stale, disputed, redacted, candidate-only, permission-limited, advisory-only, and evidence-insufficient states rather than collapsing them into plain values or treating materializations as truth.


## Phase 6 control line

Phase 6 is the practical-farm contract closure. It adds governed calculation/unit preview, identity resolution and duplicate import posture, source-fidelity and loss-map envelopes, offline capture/delayed-sync replay, FMIS shadow import candidate-only fixtures, and non-default minimum capture profile boundaries. It prevents AI-built platform/app code from hiding formulas, guessing identities, promoting external imports, or treating offline drafts as accepted truth.

## Promotion principle

Do not move these artifacts into `01_companion_artifacts/`, `02_accepted_rfcs/`, or `03_machine_contracts/` until review confirms they do not conflict with active baseline law.

## Immediate use

A platform implementer or AI coding agent may use this package to draft the platform skeleton, public API bundle, SDK contract, reason-code registry, preflight/explain surfaces, query/read/result display surfaces, output preview surfaces, and conformance gates.

Production runtime claims should wait until the relevant artifacts are promoted and implemented.

## Phase 7 addition — SDK/API bundle and reference platform skeleton

Phase 7 adds implementation-facing delivery tooling so an AI coding agent can begin platform development from public contracts and a reference skeleton instead of inventing architecture.

Added artifact groups:

- `service_descriptions/ofarm_public_platform_api_v0_1/openapi_platform_core_phase7_v0_1.json`
- `service_descriptions/ofarm_public_platform_api_v0_1/asyncapi_platform_events_v0_1.json`
- `service_descriptions/ofarm_public_platform_api_v0_1/OFARM_PublicContractPackManifest_v0_1.json`
- `sdk_contracts_v0_1/`
- `reference_platform_skeleton_v0_1/`
- Phase 7 draft machine contracts for SDK codegen, public contract pack manifest, skeleton manifest, and import boundary matrix.
- Phase 7 conformance gates and matrix.

Phase 7 remains additive and implementation-facing. It does not edit active baseline law.


## Phase 8 addition — Agent conformance and break tests

Phase 8 adds implementation-facing conformance suites that prove the prior public API, SDK, workflow, practical-farm, and trace contracts actually prevent AI-agent shortcut failures.

Added artifact groups:

- `04_implementation_and_conformance/conformance_runners/agent_readiness_conformance_v0_1/`
- `conformance/OFARM_Phase8_Agent_Conformance_and_Break_Test_Gates_v0_1.md`
- `conformance/OFARM_Phase8_Agent_Conformance_and_Break_Test_Matrix_v0_1.json`
- Phase 8 draft machine contracts for conformance case/suite, two-agent build test, and execution report
- Phase 8 research intake note

Phase 8 remains additive and implementation-facing. It defines tests and gates but does not claim runtime conformance until a platform implementation executes the suite.


## Phase 9 addition — Baseline harmonization readiness

Phase 9 adds a controlled promotion and baseline-harmonization readiness package under:

```text
04_implementation_and_conformance/conformance_runners/ai_agent_ready_platform_amendment_v0_1/phase9_baseline_harmonization_readiness_v0_1/
```

It identifies promotion candidates, do-not-promote items, unresolved runtime gates, authority impact, and draft baseline patch language. It does **not** edit active baseline law. Runtime execution and the two-agent FMIS compatibility build remain `NOT_RUN` until a platform implementation exists.


## Workstream reset and inclusion boundary

This inclusion-ready package stops the pre-development amendment track at Phase 9. Any later Phase 10, Phase 11, Phase 12, or Phase 13 material is outside this package unless explicitly reviewed and imported as a separate workstream.

See:

```text
04_implementation_and_conformance/conformance_runners/ai_agent_ready_platform_amendment_v0_1/OFARM_AI_Agent_Readiness_Workstream_Reset_and_Inclusion_Boundary_v0_1.md
```
