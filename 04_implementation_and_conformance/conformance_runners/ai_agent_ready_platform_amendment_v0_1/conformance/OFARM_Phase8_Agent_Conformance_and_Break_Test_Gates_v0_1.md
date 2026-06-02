# OFARM Phase 8 Agent Conformance and Break-Test Gates v0.1

Date: 2026-05-14  
Status: active supporting implementation/conformance candidate  
Applies to: Phase 8 of the AI-agent-ready platform amendment

## Gate statement

An OFARM platform implementation is not AI-coding-agent-ready until the Phase 8 blocker gates pass.

Phase 8 does not create new model law. It makes existing OFARM law executable as implementation tests so that an AI coding agent cannot pass protocol checks while bypassing source-of-truth, authority, evidence, promotion, materialization, pack, import, output, and advisory/compliance boundaries.

## Required blocker gates

1. **Semantic-law blockers pass.** No implementation path may turn current-state materializations, projections, AI outputs, compiled outputs, or FMIS/machine imports into accepted truth without governed source/evidence/promotion paths.
2. **Public/internal contract discipline passes.** Public SDKs and public contract packs must exclude internal storage, materialization, authority, promotion, and projection mutation surfaces.
3. **Sync/import conflict safety passes.** Idempotency, stale preconditions, duplicate detection, candidate-only imports, source fidelity, loss maps, and sync-time authority recheck must work.
4. **Numeric/display determinism passes.** Unit conversion, formulas, rounding, and display qualification must remain deterministic and must not be hidden in UI code.
5. **Explainability regression passes.** Denials, dry-runs, output refusals, import decisions, query freshness, and pack conflicts must produce retrievable structured traces.
6. **Two-agent FMIS compatibility passes.** Two independent AI coding agents must build compatible client semantics from the package without copying platform internals or inventing public APIs.
7. **Hard-path offline contractor replay passes.** Offline capture, delayed sync, authority revocation, geometry drift, duplicate retry, partial execution, dispute, correction, and high-consequence output must remain reconstructable and safe.

## Waiver rule

Protocol/API shape success cannot waive Phase 8 semantic-law blockers. A waiver may only document a missing runtime capability during implementation, not declare the platform agent-ready.

## Runtime readiness claim

This package defines tests. It does not claim runtime conformance. A runtime may claim Phase 8 readiness only after returning a `PASS` execution report against the Phase 8 suite.
