# Logging and Attestation Open Decisions

- Date: 2026-03-11
- Scope: unresolved modeling questions that remain after the current spec package.
- Exclusion rule: settled decisions from the master spec are intentionally omitted.

## 1. Persistence shape for `OperationDraft`

- Open question: should drafts live as typed family-specific payload columns, a generic JSON payload plus indexed anchors, or a mixed model?
- Why unresolved: the runtime commit path is family-specific, but the target orchestration layer is generic.
- Current default from the spec: allow a generic `draftPayload` plus indexed anchors, then revisit typed columns only for hot-path reporting or queue filters.

## 2. Persistence shape for `OperationComplianceAssessment`

- Open question: should assessments be append-only superseding records, mutable rows with an audit trail, or a pure derived cache regenerated on demand?
- Why unresolved: the repo currently proves append-only fact capture strongly, but does not yet prove the right operational model for reviewer edits and waivers.
- Current default from the spec: prefer append-only or superseding assessment records over in-place mutation.

## 3. Hosting boundary for review and attestation workbench APIs

- Open question: should review-queue and attestation-action routes live in the FastAPI backend directly, in Control Center as a proxy/workbench layer, or in a split model?
- Why unresolved: Control Center is already the local operational plane, but current product and deployment assumptions for a broader workbench are not yet explicit.
- Current default from the spec: treat Control Center as the current local proxy/workbench entry point while keeping the final hosting split open.

## 4. Scope of the first `OperationCatalog`

- Open question: should the first generic catalog stay limited to the five currently implemented generic families, or also reserve entries for future generic/logical families such as irrigation, plant protection, observation-only logging, or bundled task completion?
- Why unresolved: over-broad catalog scope will outrun the proven commit and reporting paths.
- Current default from the spec: the generic catalog should include only families that are already implemented end-to-end in the additive draft, assessment, and attestation slice.
- Open question: should the first generic catalog stay limited to the currently implemented five additive families, or expand later toward other proven event-specific commit families such as `irrigation`, `plant_protection_application`, and `pesticide_application`?
- Why unresolved: over-broad catalog scope will outrun the currently implemented additive runtime even though more event-specific commit routes already exist outside the present catalog boundary.
- Current default from the spec: catalog v1 stays limited to the currently implemented additive families with live catalog, draft, assessment, review-queue, and SQL-family-scope support.

## 5. Profile-governance source for `OperationRequirementProfile`

- Open question: should requirement profiles be authored as code/config beside rulepacks and report packs, derived from them at build time, or curated manually in a new registry?
- Why unresolved: current repo assets already contain pieces of the answer, but no single source currently expresses operation-save, attestation, and report-binding requirements together.
- Current default from the spec: start with additive config generated or curated beside report-pack/rulepack assets, without attempting full automatic derivation in the first slice.

## 6. `ProductionUnitSeasonSlot` scope outside current crops-only rollout

- Open question: how should the overlay handle perennial systems, mixed-use fields, or livestock-linked production units once the program expands beyond SI organic crops-only?
- Why unresolved: current repo-backed planning evidence is strongest for crops-only and A.5 semantics.
- Current default from the spec: keep the overlay limited to crops-only semantics until new domain evidence exists.
