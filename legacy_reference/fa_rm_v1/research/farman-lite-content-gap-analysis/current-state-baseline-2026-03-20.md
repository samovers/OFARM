# Farman Lite Current-State Baseline (Compliance-First Spec-Writing Wave)

Date: 2026-03-20
Applies to: EU + SI program scope (crops-only)

This baseline supersedes [current-state-baseline-2026-03-09.md](/Users/einstein/Documents/Codex/Semantic farming/docs/research/farman-lite-content-gap-analysis/current-state-baseline-2026-03-09.md) as the active planning reference for Farman Lite content-governance work.

## 1. Observed Current State

1. The repo already has the March 9 writing-wave boundary specs for:
   - seed purchase and exception continuity,
   - claim-anchor sufficiency,
   - minimum-chain traceability,
   - organic environmental scope guard,
   - transition downstream linkage,
   - parallel-production segregation boundary,
   - unsupported transition-category guard,
   - comparability primitives,
   - equipment task linkage,
   - farm-type scope governance.
2. The remaining repo-visible issues are mostly shared-interface or phase-mapping issues:
   - production-system profile vs canonical production status vs SI `E|P|K` projection mapping,
   - climate plan-tab card labels vs canonical climate signal types,
   - overlay facts vs admitted obligation-pack meaning,
   - legacy compatibility surfaces vs richer reviewer surfaces,
   - A.5 year-grid evidentiary wording,
   - active ledger drift between backlog, signoff, fixtures, README, and master tracker.
3. Current detailed-spec filenames still reflect the earlier March 9 numbering. Active phase ownership is therefore defined by the March 20 backlogs and triage, not by filename prefix alone.

## 2. Evidence-Backed Inference

1. Repo truth is still strongest for EU baseline + SI crops-only organic control-pack work.
2. The repo already has enough authored content to close the remaining issues through writing-layer governance rather than more source-model promotion.
3. The highest remaining risk is wrong content meaning, not missing runtime or missing domain entities.

## 3. Recommended Working Assumptions

1. Jurisdictions remain limited to EU baseline + SI.
2. Domain scope remains crops-only.
3. Priority order remains `organic`, then `in_transition`, then `conventional`.
4. Admitted farm types remain `arable_row_crop`, `grain`, and `mixed_crop`.
5. `horticulture`, `orchard`, `vineyard`, `permanent_tree_crop`, and `protected_horticulture` remain `Unknown` or out of scope unless a separate content pack is admitted first.
6. Environmental obligation packs beyond organic contamination, buffer, and residue controls remain `Unknown`.
7. This wave is documentation and contract-governance work only; no runtime or source-model expansion is implied unless a writing-only fix is proven insufficient.

## 4. Proposed Change

Replace the March 9 reset as the active writing ledger with one compliance-first phase program:

1. Phase 0: writing framework lock plus shared reference artifacts.
2. Phase 1: organic compliance blockers.
3. Phase 2: organic cross-surface harmonization.
4. Phase 3: transition and mixed-status boundaries.
5. Phase 4: conventional and comparability refinement.
6. Phase 5: governance closeout.

## 5. Active Phase Program

### Phase 0

1. Publish shared reference artifacts for:
   - production-system, production-status, and SI code crosswalk,
   - overlay descriptive-vs-obligation boundary,
   - legacy-vs-canonical reviewer-surface precedence.
2. Use these as shared anchors in later phase notes rather than restating the same rule repeatedly.

### Phase 1

1. Seed purchase and exception continuity.
2. Claim-anchor sufficiency and label-artifact boundary.
3. Minimum-chain traceability boundary.
4. Organic environmental scope guard.
5. A.5 year-grid evidence clarification.

### Phase 2

1. Adopt the shared production-system/status/code crosswalk from Phase 0 as the active harmonization anchor.
2. Unit, basis, and code-system crosswalk.
3. Climate plan card to canonical signal mapping.
4. Adopt the shared field-passport overlay boundary note from Phase 0 as the active harmonization anchor.

### Phase 3

1. Transition downstream linkage boundary.
2. Parallel-production segregation vs mass-balance boundary.
3. Unsupported transition-category guard.

Detailed-spec filenames for this bundle remain:
- [phase-2-5-detailed-spec-transition-downstream-linkage-boundary.md](/Users/einstein/Documents/Codex/Semantic farming/docs/implementation/phase-2-5-detailed-spec-transition-downstream-linkage-boundary.md)
- [phase-2-6-detailed-spec-parallel-production-segregation-vs-mass-balance-boundary.md](/Users/einstein/Documents/Codex/Semantic farming/docs/implementation/phase-2-6-detailed-spec-parallel-production-segregation-vs-mass-balance-boundary.md)
- [phase-2-7-detailed-spec-transition-unsupported-category-guard.md](/Users/einstein/Documents/Codex/Semantic farming/docs/implementation/phase-2-7-detailed-spec-transition-unsupported-category-guard.md)

### Phase 4

1. Comparability primitives bundle.
2. Conventional projection boundary.
3. Equipment task-linkage governance note.
4. Farm-type scope freeze refresh.

Detailed-spec filenames for this bundle remain mixed across:
- [phase-3-6-detailed-spec-comparability-primitives-bundle.md](/Users/einstein/Documents/Codex/Semantic farming/docs/implementation/phase-3-6-detailed-spec-comparability-primitives-bundle.md)
- [phase-4-1-detailed-spec-conventional-projection-boundary.md](/Users/einstein/Documents/Codex/Semantic farming/docs/implementation/phase-4-1-detailed-spec-conventional-projection-boundary.md)
- [phase-3-5-detailed-spec-farm-type-scope-governance.md](/Users/einstein/Documents/Codex/Semantic farming/docs/implementation/phase-3-5-detailed-spec-farm-type-scope-governance.md)
- [phase-7-10-detailed-spec-equipment-identity-task-linkage-normalization.md](/Users/einstein/Documents/Codex/Semantic farming/docs/implementation/phase-7-10-detailed-spec-equipment-identity-task-linkage-normalization.md)

### Phase 5

1. Governance closeout note.
2. Baseline, triage, README, and master tracker alignment.
3. Ledger audit proving every active row ends as `promoted`, `doc-only final`, `defer as Unknown`, or `explicitly out of scope`.

## 6. Active Writing Artifacts

1. Active baseline: [current-state-baseline-2026-03-20.md](/Users/einstein/Documents/Codex/Semantic farming/docs/research/farman-lite-content-gap-analysis/current-state-baseline-2026-03-20.md)
2. Active triage: [spec-writing-triage-2026-03-20.csv](/Users/einstein/Documents/Codex/Semantic farming/docs/research/farman-lite-content-gap-analysis/spec-writing-triage-2026-03-20.csv)
3. Phase 0 backlog, fixture pack, signoff:
   - [phase-0-content-backlog.csv](/Users/einstein/Documents/Codex/Semantic farming/docs/research/farman-lite-content-gap-analysis/phase-0-content-backlog.csv)
   - [phase-0-fixture-pack.json](/Users/einstein/Documents/Codex/Semantic farming/docs/research/farman-lite-content-gap-analysis/phase-0-fixture-pack.json)
   - [phase-0-signoff-matrix.csv](/Users/einstein/Documents/Codex/Semantic farming/docs/research/farman-lite-content-gap-analysis/phase-0-signoff-matrix.csv)
4. Phase 1 backlog, fixture pack, signoff:
   - [phase-1-content-backlog.csv](/Users/einstein/Documents/Codex/Semantic farming/docs/research/farman-lite-content-gap-analysis/phase-1-content-backlog.csv)
   - [phase-1-fixture-pack.json](/Users/einstein/Documents/Codex/Semantic farming/docs/research/farman-lite-content-gap-analysis/phase-1-fixture-pack.json)
   - [phase-1-signoff-matrix.csv](/Users/einstein/Documents/Codex/Semantic farming/docs/research/farman-lite-content-gap-analysis/phase-1-signoff-matrix.csv)
5. Phase 2 backlog, fixture pack, signoff:
   - [phase-2-content-backlog.csv](/Users/einstein/Documents/Codex/Semantic farming/docs/research/farman-lite-content-gap-analysis/phase-2-content-backlog.csv)
   - [phase-2-fixture-pack.json](/Users/einstein/Documents/Codex/Semantic farming/docs/research/farman-lite-content-gap-analysis/phase-2-fixture-pack.json)
   - [phase-2-signoff-matrix.csv](/Users/einstein/Documents/Codex/Semantic farming/docs/research/farman-lite-content-gap-analysis/phase-2-signoff-matrix.csv)
6. Phase 3 backlog, fixture pack, signoff:
   - [phase-3-content-backlog.csv](/Users/einstein/Documents/Codex/Semantic farming/docs/research/farman-lite-content-gap-analysis/phase-3-content-backlog.csv)
   - [phase-3-fixture-pack.json](/Users/einstein/Documents/Codex/Semantic farming/docs/research/farman-lite-content-gap-analysis/phase-3-fixture-pack.json)
   - [phase-3-signoff-matrix.csv](/Users/einstein/Documents/Codex/Semantic farming/docs/research/farman-lite-content-gap-analysis/phase-3-signoff-matrix.csv)
7. Phase 4 backlog, fixture pack, signoff:
   - [phase-4-content-backlog.csv](/Users/einstein/Documents/Codex/Semantic farming/docs/research/farman-lite-content-gap-analysis/phase-4-content-backlog.csv)
   - [phase-4-fixture-pack.json](/Users/einstein/Documents/Codex/Semantic farming/docs/research/farman-lite-content-gap-analysis/phase-4-fixture-pack.json)
   - [phase-4-signoff-matrix.csv](/Users/einstein/Documents/Codex/Semantic farming/docs/research/farman-lite-content-gap-analysis/phase-4-signoff-matrix.csv)
8. Phase 5 backlog, fixture pack, signoff:
   - [phase-5-content-backlog.csv](/Users/einstein/Documents/Codex/Semantic farming/docs/research/farman-lite-content-gap-analysis/phase-5-content-backlog.csv)
   - [phase-5-fixture-pack.json](/Users/einstein/Documents/Codex/Semantic farming/docs/research/farman-lite-content-gap-analysis/phase-5-fixture-pack.json)
   - [phase-5-signoff-matrix.csv](/Users/einstein/Documents/Codex/Semantic farming/docs/research/farman-lite-content-gap-analysis/phase-5-signoff-matrix.csv)

## 7. Historical Artifacts

These remain for audit trail only and are not the active writing ledger:

1. [content-only-gap-analysis-2026-03-06.md](/Users/einstein/Documents/Codex/Semantic farming/docs/research/farman-lite-content-gap-analysis/content-only-gap-analysis-2026-03-06.md)
2. [backlog-closure-matrix-2026-03-06.csv](/Users/einstein/Documents/Codex/Semantic farming/docs/research/farman-lite-content-gap-analysis/backlog-closure-matrix-2026-03-06.csv)
3. [spec-only-triage-2026-03-06.csv](/Users/einstein/Documents/Codex/Semantic farming/docs/research/farman-lite-content-gap-analysis/spec-only-triage-2026-03-06.csv)
4. [current-state-baseline-2026-03-09.md](/Users/einstein/Documents/Codex/Semantic farming/docs/research/farman-lite-content-gap-analysis/current-state-baseline-2026-03-09.md)
5. [spec-writing-triage-2026-03-09.csv](/Users/einstein/Documents/Codex/Semantic farming/docs/research/farman-lite-content-gap-analysis/spec-writing-triage-2026-03-09.csv)
6. Pre-refresh phase ledgers captured on 2026-03-09:
   - [phase-1-content-backlog-2026-03-09.csv](/Users/einstein/Documents/Codex/Semantic farming/docs/research/farman-lite-content-gap-analysis/phase-1-content-backlog-2026-03-09.csv)
   - [phase-1-signoff-matrix-2026-03-09.csv](/Users/einstein/Documents/Codex/Semantic farming/docs/research/farman-lite-content-gap-analysis/phase-1-signoff-matrix-2026-03-09.csv)
   - [phase-1-fixture-pack-2026-03-09.json](/Users/einstein/Documents/Codex/Semantic farming/docs/research/farman-lite-content-gap-analysis/phase-1-fixture-pack-2026-03-09.json)
   - [phase-2-content-backlog-2026-03-09.csv](/Users/einstein/Documents/Codex/Semantic farming/docs/research/farman-lite-content-gap-analysis/phase-2-content-backlog-2026-03-09.csv)
   - [phase-2-signoff-matrix-2026-03-09.csv](/Users/einstein/Documents/Codex/Semantic farming/docs/research/farman-lite-content-gap-analysis/phase-2-signoff-matrix-2026-03-09.csv)
   - [phase-2-fixture-pack-2026-03-09.json](/Users/einstein/Documents/Codex/Semantic farming/docs/research/farman-lite-content-gap-analysis/phase-2-fixture-pack-2026-03-09.json)
   - [phase-3-content-backlog-2026-03-09.csv](/Users/einstein/Documents/Codex/Semantic farming/docs/research/farman-lite-content-gap-analysis/phase-3-content-backlog-2026-03-09.csv)
   - [phase-3-signoff-matrix-2026-03-09.csv](/Users/einstein/Documents/Codex/Semantic farming/docs/research/farman-lite-content-gap-analysis/phase-3-signoff-matrix-2026-03-09.csv)
   - [phase-3-fixture-pack-2026-03-09.json](/Users/einstein/Documents/Codex/Semantic farming/docs/research/farman-lite-content-gap-analysis/phase-3-fixture-pack-2026-03-09.json)
7. Earlier dated pre-reset phase snapshots from March 6 and March 8 remain historical companions.

## 8. Risks and Uncertainties

1. The active phase bundle and the detailed-spec filename prefix no longer line up perfectly.
2. Unsupported environmental regimes, unsupported farm types, and unsupported permanent-crop transition semantics remain intentionally unresolved and must stay `Unknown`.
3. Climate plan-tab labels remain presentation-level names layered over canonical climate signals; the mapping note is the authority for that translation.
