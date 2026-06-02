# OFARM Phase 9 Active Baseline Patch Proposals v0.1

Status: proposal-only; do not apply without review.  
This file contains exact candidate wording. It is not an active baseline patch.

## Proposal BHP-001 — Constitution clarification

Target: `00_active_baseline/OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md`

Suggested insertion:

> Application-builder public surfaces, SDKs, capability manifests, tool manifests, traces, previews, read envelopes, and AI-agent outputs are runtime or implementation affordances. They do not create canonical truth, do not promote assertions, do not replace evidence policy, and do not allow projections, caches, compiled outputs, or AI output to become hidden governance decisions. Canonical consequence remains assertion/history-first and governed by accepted commit, promotion, authority, evidence, and pack law.

Review note: This is a clarification. It should not create new semantic categories.

## Proposal BHP-002 — Platform runtime public surface closure

Target: `00_active_baseline/OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md`

Suggested insertion:

> An OFARM Platform implementation may expose public application-builder and AI-agent surfaces only through governed runtime contracts. A public surface set must distinguish public contracts from platform internals; advertise actual capabilities; support preflight, dry-run, explain, and trace retrieval for high-consequence operations where applicable; return registered RuntimeProblem reason codes; preserve result qualification on read and preview surfaces; and generate SDKs only from public contracts. Client applications and AI agents must not mutate canonical stores, materialization stores, authority decisions, pack activation state, or publication records except through governed runtime operations.

Review note: This should be accepted only with wording that avoids claiming any current runtime has implemented these surfaces.

## Proposal BHP-003 — Alignment Register carrier/tooling row

Target: `00_active_baseline/OFARM_Alignment_Register_v0_13.md`

Suggested row text:

> Implementation-facing public contract publication may use OpenAPI, AsyncAPI, JSON Schema, capability/operation catalogues, problem-detail envelopes, and conformance-test descriptors as carrier and tooling patterns. These patterns do not import external semantic law into OFARM, do not override packs or authority policy, and do not allow public schemas or tool annotations to mutate core OFARM meaning.

Review note: External standards are implementation carriers, not OFARM semantic authorities.

## Proposal BHP-004 — Readiness gate memo update

Target: `00_active_baseline/OFARM_post_gap_closure_readiness_gate_memo_v0_1.md`

Suggested insertion:

> AI-agent-ready implementation support has been drafted as an additive implementation/conformance package: navigation guardrails, public surface drafts, preflight/explain contracts, reason-code registry, result qualification, workflow recipes, practical farm contracts, SDK/API skeletons, and conformance/break tests. This improves implementation direction but does not by itself establish runtime conformance, two-agent compatibility, live deployment evidence, or external standard readiness. Those claims remain blocked until the Phase 8/9 evidence gates are executed and passed.

Review note: This preserves the existing maturity status.

## Proposal BHP-005 — Final hostile-review gate

Target: `00_active_baseline/OFARM_final_hostile_review_after_gap_closure_v0_1.md`

Suggested insertion:

> Before any runtime or package is described as AI coding-agent ready, a hostile review must verify that: two independent AI coding agents can build compatible clients from the public contract pack without copying platform internals; semantic-law blocker tests pass; public SDKs expose no internal surfaces; high-consequence operations support preflight/explain/trace where advertised; candidate imports remain candidate-only; result qualification survives through UI/app flows; and no protocol success can waive OFARM semantic-law blockers.

Review note: This is a gate, not a claim that the gate has passed.
