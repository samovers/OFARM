# OFARM AI-Agent Readiness Amendment Control v0.1

Date: 2026-05-13  
Status: active supporting implementation/conformance control artifact  
Role: phase control and authority discipline for the AI-agent-ready platform amendment

## 1. Problem being closed

The active OFARM 2 baseline is conceptually strong, but the pre-development package does not yet give an AI coding agent an explicit enough implementation boundary for building OFARM Platform or client apps.

The highest-risk missing layer is not semantic theory. It is a machine- and agent-consumable implementation contract layer:

- module boundaries
- public application surfaces
- public/internal schema catalogues
- AI agent autonomy limits
- dry-run/preflight behavior
- trace/explain retrieval
- RuntimeProblem reason-code registry
- conformance gates for likely AI shortcuts

## 2. Scope of this amendment

This amendment covers Phases 0–3:

- Phase 0: repository navigation and authority guardrails
- Phase 1: platform module boundary map
- Phase 2: public application surface closure
- Phase 3: AI agent use, preflight/dry-run/explain, trace retrieval, and RuntimeProblem reason-code closure

## 3. Non-goals

This amendment does not:

- rewrite the Constitution
- rewrite the Platform baseline
- make reviewed holding material active law
- make farm-owner draft contracts default law
- make regulatory inspector addenda active unless separately promoted
- define livestock semantics
- turn OFARM into CRUD
- make external FMIS, machinery, or sensor data accepted truth by default
- make AI outputs governance decisions

## 4. Affected active baseline files

No direct baseline edits are made by this patch.

The following active files are affected conceptually and should be harmonized only after review/promotion:

- `00_active_baseline/OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md`
- `00_active_baseline/OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md`
- `01_companion_artifacts/OFARM_Platform_Enforcement_Architecture_Memo_v0_1.md`
- `01_companion_artifacts/OFARM_Query_Architecture_Note_v0_1.md`
- `02_accepted_rfcs/OFARM_Capability_Manifest_RFC_v0_1.md`
- `03_machine_contracts/schemas/runtime_surface/OFARM_RuntimeSurfaceContract_schema_v0_1.json`
- `03_machine_contracts/schemas/core/OFARM_RuntimeProblem_schema_v0_1.json`

## 5. Promotion path

| Candidate artifact | First location | Promotion target |
|---|---|---|
| AI Agent Use and Autonomy Policy | draft companion | `01_companion_artifacts/` |
| Application Builder Surface RFC | draft RFC | `02_accepted_rfcs/` |
| Preflight/DryRun/Explain Surface RFC | draft RFC | `02_accepted_rfcs/` |
| RuntimeProblem Reason Code Registry RFC | draft RFC | `02_accepted_rfcs/` |
| Public surface/schema/agent-tool schemas | draft machine contracts | `03_machine_contracts/` |
| OpenAPI public platform core draft | service descriptions | `04_implementation_and_conformance/service_and_sdk_candidates/service_descriptions/` until platform release |
| Module boundary map | implementation/conformance | may stay support unless made normative |

## 6. Risks controlled

This amendment controls these implementation risks:

- public API invention
- internal schema leakage
- local materialization mutation
- silent authority bypass
- AI action without dry-run/preflight
- destructive retry or duplicate import
- unstructured error handling
- stale or redacted data displayed as complete truth
- client workflow state collapse

## 7. Acceptance rule for this patch

The patch is successful if an AI coding agent can answer, without reading platform internals:

```text
What may an app call?
What may an AI agent call?
What requires preflight?
What requires human approval?
What is public versus internal?
What reason codes can be returned?
Where are traces retrieved?
What must not become a truth store?
```

