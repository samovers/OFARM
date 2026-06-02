# OFARM AI-Agent-Ready Platform Amendment Phase 4 Patch Apply Guide

Date: 2026-05-13  
Patch: `OFARM2_ai_agent_ready_platform_amendment_phase4_patch_v0_1.zip`

## Purpose

Overlay this patch onto the Phase 0–3 preview package. It adds Phase 4 query/current-state/output app contracts.

## Authority posture

The patch is additive active supporting implementation/conformance material. It does not edit active baseline law.

## Apply

From repository root:

```bash
unzip OFARM2_ai_agent_ready_platform_amendment_phase4_patch_v0_1.zip -d .
```

Then inspect:

```text
04_implementation_and_conformance/conformance_runners/ai_agent_ready_platform_amendment_v0_1/OFARM_AI_Agent_Ready_Platform_Phase4_Validation_Report_v0_1.json
04_implementation_and_conformance/implementation_notes/query_cookbook_v0_1/
04_implementation_and_conformance/examples_and_fixtures/output_assembly_examples_v0_1/
```

## Validation included

The patch includes local JSON parse and JSON Schema validation results. External OpenAPI overlay tooling was not run.
