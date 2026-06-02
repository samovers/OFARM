# Patch Apply Guide — OFARM Pre-development AI-Agent-Readiness Amendment Package v0.1

Date: 2026-05-14

## What this is

This zip is a repository-relative overlay patch for the OFARM pre-development package. It assembles the completed Phase 0–9 AI-agent-readiness amendment into a single inclusion-ready package.

## What this is not

It is not a runtime implementation. It is not a baseline-law edit. It does not claim that OFARM is runtime-ready, externally standard-ready, or proven by executed conformance tests.

## Apply rule

Unzip this package at the root of the OFARM repository/package:

```text
unzip OFARM2_predevelopment_ai_agent_ready_amendment_package_v0_1.zip -d <OFARM_ROOT>
```

The patch adds implementation/conformance support files and updates package navigation/status metadata. It should not overwrite any `00_active_baseline/` file.

## Inclusion boundary

Included:

- original amendment Phase 0–9 artifacts
- consolidated workstream-reset memo
- attached AI-agent implementation readiness research as active supporting research
- package metadata and build report

Excluded:

- Phase 10 promotion-review patches as accepted authority
- Phase 11 runtime-kickoff work as active law
- Phase 12 runtime-slice kickoff work as active law
- any Phase 13 runtime implementation work

## Recommended post-apply check

After applying, verify:

```text
1. No files under 00_active_baseline/ were changed.
2. New amendment materials appear under 04_implementation_and_conformance/conformance_runners/ai_agent_ready_platform_amendment_v0_1/.
3. AGENT_NAVIGATION.md and agent_authority_map.json are present.
4. MATERIAL_STATUS.csv/json include the amendment package and research support files.
5. Draft RFCs, draft companion artifacts, and draft machine contracts remain in draft/supporting locations.
```

## Primary entry point

Start here:

```text
04_implementation_and_conformance/conformance_runners/ai_agent_ready_platform_amendment_v0_1/README.md
04_implementation_and_conformance/conformance_runners/ai_agent_ready_platform_amendment_v0_1/OFARM_AI_Agent_Readiness_Workstream_Reset_and_Inclusion_Boundary_v0_1.md
AGENT_NAVIGATION.md
```
