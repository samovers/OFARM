# OFARM Agentic AI / World Model Amendment — Phase AAI-P1 Baseline Safety Clarification v0.1

Date: 2026-05-14  
Status: active baseline clarification applied; pre-implementation only.  
Role: continue the amendment by hardening active baseline safety boundaries before promoting agent/world-model contracts.

## Summary

AAI-P1 applies the no-regrets baseline clarification phase. It adds active-baseline addenda that prevent AI outputs, agent memory, public surfaces, tool-call success, projections, caches, compiled-output previews, scenario state, and world-model state from becoming hidden truth or hidden governance.

## Active baseline files changed

- `00_active_baseline/OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md`
- `00_active_baseline/OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md`
- `00_active_baseline/OFARM_Alignment_Register_v0_13.md`
- `00_active_baseline/OFARM_post_gap_closure_readiness_gate_memo_v0_1.md`
- `00_active_baseline/OFARM_final_hostile_review_after_gap_closure_v0_1.md`

## Root/package-control files changed

- `ACTIVE_SUBSTANCE_README.md`
- `PROJECT_AUTHORITY.md`
- `CURRENT_PACKAGE_CHANGELOG.md`
- `MATERIAL_STATUS.json`
- `MATERIAL_STATUS.csv`
- `MANIFEST.csv`

## What changed materially

- AI-generated status is provenance and authority context, not a new truth category.
- Software-agent participation requires explicit governance and cannot be inferred from model/tool/prompt/session identity.
- Agent and app operations must use governed public/runtime surfaces.
- Tool-call success is not governance success.
- Agent handoff may carry task context but may not transfer authority.
- World-model state remains Advisory-only unless bridged and accepted through normal OFARM governance.
- AI-facing answers must preserve result qualifications.

## What remains deliberately unpromoted

- `SoftwareAgentProfile`
- `AgentInstance`
- `AgentAuthorityEnvelope`
- `AgentRunEnvelope`
- `AgentRunTrace`
- `AgentHandoffEnvelope`
- `AgentToolManifest`
- `WorldModelRun`
- `WorldModelState`
- `ScenarioSpec`
- `ScenarioResultSet`
- `EvidenceNeed`
- `ObservationRequest`

Those concepts remain supporting/draft until later controlled RFC and machine-contract phases.

## Non-claims

AAI-P1 does not claim production readiness, runtime readiness, two-agent compatibility, world-model compliance readiness, autonomous compliance decisioning, live external-tool integration, legal/regulatory certification, or external-standard readiness.

## Historical next-phase note

At the time of AAI-P1, the next planned controlled phase was AAI-P2: artifact-by-artifact review and selected promotion of existing AI/app support material, especially public operation descriptors, preflight/dry-run/explain surfaces, result qualification, runtime problem reason codes, and trace retrieval.

Current package note: the current controlled-promotion endpoint is `AAI-CP10`; use `../controlled_promotion/PROMOTION_INDEX.json` for the current CP0-CP10 lifecycle map.
