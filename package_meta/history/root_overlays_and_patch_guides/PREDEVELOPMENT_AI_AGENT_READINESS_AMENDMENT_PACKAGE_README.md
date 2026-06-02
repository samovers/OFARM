# OFARM Pre-development AI-Agent-Readiness Amendment Package v0.1

Date: 2026-05-14  
Package posture: repository-relative amendment overlay  
Authority posture: active supporting implementation/conformance material only

## Summary

This package assembles the completed Phase 0–9 OFARM AI-agent-readiness amendment into one inclusion-ready overlay for the pre-development OFARM package.

The amendment is designed to make future OFARM platform development safer for AI coding agents by making implementation boundaries explicit before code is written.

It adds guidance and draft contracts for:

- agent navigation and authority guardrails
- platform module boundaries
- public application/runtime surfaces
- AI-agent use and autonomy limits
- preflight, dry-run, explain, trace, and RuntimeProblem reason-code behavior
- query, current-state, result-qualification, and output assembly surfaces
- workflow cookbook and UI-safe state matrix
- calculation, identity, import, offline sync, source-fidelity, and minimum-capture boundaries
- SDK/codegen and public/internal contract-pack boundaries
- agent-readiness conformance and break tests
- baseline harmonization readiness proposals

## Inclusion boundary

This package includes only the pre-development amendment track: Phase 0 through Phase 9.

It intentionally excludes later Phase 10–12 promotion/runtime planning packages from the pre-development amendment boundary. See:

```text
04_implementation_and_conformance/conformance_runners/ai_agent_ready_platform_amendment_v0_1/OFARM_AI_Agent_Readiness_Workstream_Reset_and_Inclusion_Boundary_v0_1.md
```

## Authority statement

This package does not alter active baseline law.

No `00_active_baseline/` files are edited.

Draft RFCs, draft companion artifacts, and draft machine contracts remain draft/supporting material until a later promotion decision explicitly moves them.

## Main locations

```text
AGENT_NAVIGATION.md
agent_authority_map.json
04_implementation_and_conformance/conformance_runners/ai_agent_ready_platform_amendment_v0_1/
04_implementation_and_conformance/conformance_runners/agent_readiness_conformance_v0_1/
04_implementation_and_conformance/implementation_notes/application_workflow_cookbook_v0_1/
04_implementation_and_conformance/implementation_notes/query_cookbook_v0_1/
04_implementation_and_conformance/examples_and_fixtures/output_assembly_examples_v0_1/
04_implementation_and_conformance/implementation_notes/practical_farm_contracts_v0_1/
04_implementation_and_conformance/service_and_sdk_candidates/service_descriptions/ofarm_public_platform_api_v0_1/
04_implementation_and_conformance/service_and_sdk_candidates/sdk_contracts_v0_1/
04_implementation_and_conformance/service_and_sdk_candidates/reference_platform_skeleton_v0_1/
06_active_supporting_research/syntheses/OFARM_AI_Agent_Implementation_Readiness_Amendment_Research_Report_v0_1.md
```

## Non-claims

This package does not claim:

- implemented runtime
- live API readiness
- executed conformance pass
- two-agent FMIS compatibility pass
- external standard readiness
- live farm deployment readiness
- promotion of draft material into active law

## Recommended next governance action

After inclusion, run a controlled promotion review to decide which draft artifacts should move into `01_companion_artifacts/`, `02_accepted_rfcs/`, or `03_machine_contracts/`. Keep runtime-evidence-dependent claims blocked until a platform implementation executes the conformance suite.
