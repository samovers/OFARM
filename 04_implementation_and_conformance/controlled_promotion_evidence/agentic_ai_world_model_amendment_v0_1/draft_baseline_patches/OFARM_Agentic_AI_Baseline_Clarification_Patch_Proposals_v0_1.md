# OFARM Agentic AI Baseline Clarification Patch Proposals v0.1

Date: 2026-05-14  
Status: draft baseline clarification proposals; not applied to active baseline.  
Role: Phase 1 no-regrets protective clarifications.

## Patch posture

These proposals are intended as baseline clarifications, not architectural rewrites. They should be reviewed against the active RC2.1 baseline before insertion.

## Proposal AAI-BP-001 — Constitution anti-goal clarification

Target file: `00_active_baseline/OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md`  
Suggested location: after existing anti-goals in §2.2.

Suggested insertion:

> OFARM must not become a system where AI outputs, agent memories, runtime tool-call results, projections, caches, public read models, compiled-output previews, or world-model states become hidden truth stores or hidden governance decisions. Generated-by-agent status is provenance and authority context, not a separate truth category.

Rationale: protects active assertion/history-first truth law before agent and world-model runtime contracts are added.

## Proposal AAI-BP-002 — Constitution Party / non-human actor clarification

Target file: `00_active_baseline/OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md`  
Suggested location: near Party, Authority, and non-human actor rules.

Suggested insertion:

> A software agent may participate only through explicit governance. Agent identity must distinguish the accountable human or organizational sponsor, the software-agent profile, the deployed agent instance, the model/tool profile where relevant, the authority grant or delegated envelope, and the requested action class. Agent identity does not itself confer authority.

Rationale: prevents vague “AI did it” actorship and preserves human/organizational accountability.

## Proposal AAI-BP-003 — Platform public-surface and store-mutation clarification

Target file: `00_active_baseline/OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md`  
Suggested location: near runtime enforcement chain and AI/autonomy sections.

Suggested insertion:

> AI-agent-facing operations must pass through governed runtime surfaces and enforcement gates. Agents and applications may not directly mutate canonical history stores, materialization stores, authority decisions, pack activation state, publication records, or sharing grants except through explicitly governed operations that produce traceable results.

Rationale: protects the runtime chain from agent/tool shortcuts.

## Proposal AAI-BP-004 — Platform Advisory world-model clarification

Target file: `00_active_baseline/OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md`  
Suggested location: near Advisory Twin / scenario runtime sections.

Suggested insertion:

> World-model runs and scenario states are Advisory Twin runtime artifacts unless separately bridged and accepted through normal OFARM governance. World-model state is not canonical truth, not Compliance Twin state, not current-state materialization, and not an accepted event consequence.

Rationale: enables world-model AI while preventing a third twin or hidden current state.

## Proposal AAI-BP-005 — Readiness memo bounded-debt update

Target file: `00_active_baseline/OFARM_post_gap_closure_readiness_gate_memo_v0_1.md`

Suggested insertion:

> Agentic AI and world-model readiness remain bounded debt until agent actorship, agent run envelope, run trace, handoff, capability-manifest support, world-model advisory-state contracts, and multi-agent hostile tests are promoted and, where relevant, executed against an implementation.

Rationale: preserves honest maturity posture.

## Proposal AAI-BP-006 — Hostile-review gate update

Target file: `00_active_baseline/OFARM_final_hostile_review_after_gap_closure_v0_1.md`

Suggested insertion:

> Before any implementation is described as multi-agent-ready or world-model-ready, hostile review must verify that agents cannot activate packs, self-certify, promote their own advisory outputs, treat world-model state as current state, transfer authority by handoff, hide stale/permission-limited results, over-disclose through sharing tools, or bypass semantic-law blockers through public operation success.

Rationale: provides a clear future readiness gate.
