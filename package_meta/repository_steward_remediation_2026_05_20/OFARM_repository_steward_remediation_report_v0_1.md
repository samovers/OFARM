# Repository steward remediation report

Supersession status: **historical Batch 1 remediation lineage**. Batch 2 completed physical structural remediation, and Batch 2.1 updated currentness pointers. Do not cite this Batch 1 report as the current completion state.

Current completion/currentness reports:

- `package_meta/repository_steward_completion_batch2_2026_05_20/OFARM_repository_steward_completion_batch2_report_v0_1.json`
- `package_meta/repository_steward_completion_batch2_1_2026_05_20/OFARM_repository_steward_completion_batch2_1_currentness_patch_v0_1.json`

Generated: 2026-05-20T00:00:00+02:00

Status: package metadata only; no active OFARM law changed.

| Phase | Status | Problem | Action |
|---:|---|---|---|
| 1 | applied | active-law classification for navigation files | MATERIAL_STATUS records now expose activeLaw/artifactRole/searchDefault overlays; README/folder.status are metadata, not law. |
| 2 | applied | folder.status canonical fields | Batch 1 added canonical camelCase fields; Batch 2 later removed legacy compatibility keys. |
| 3 | applied | default search exclusions | Historical, spike, and draft implementation folders are excluded in IMPLEMENTATION_SUBFOLDER_INDEX and default search profile. |
| 4 | applied | CI workflow naming | generate_indexes.yml renamed to validate_generated_currentness.yml and workflows run the full steward guardrail step. |
| 5 | applied | changelog linearization | Root delta/changelog rewritten as current-first chronological repository-steward summaries. |
| 6 | applied | final validation/live scan reconciliation | Final validation summaries are refreshed from the current cross-reference scan after this patch. |
| 7 | applied | PATH_REMAPS current identity | PATH_REMAPS.json now separates sourcePackage from currentPackage and marks applicability to the current package. |
| 8 | applied | validator documentation single source | Validator documentation now points to a complete validation suite and wrapper command. |
| 9 | applied | handover/agent validation instructions | Handover, AGENTS, llms, and README now reference the full validation suite. |
| 10 | applied | latest cleanup wording | README reserves latest/current language for the current steward remediation and marks phases 12-15 as history. |
| 11 | contained | non-active schema copy quarantine | Batch 1 indexed and search-excluded non-active copies; Batch 2 later physically renamed/archived same-basename copies. |
| 12 | applied | canonical traceability index | TRACEABILITY_INDEX.json remains canonical; generated traceability is derived; Markdown regenerated as path table. |
| 13 | applied | derived generated map policy | Generated duplicates are explicitly marked by policy as derived from canonical active/root indexes. |
| 14 | contained | review-holding default visibility | Batch 1 search-excluded review-holding snapshots; Batch 2 later archived root reviewed_* snapshots under archive/review_holding/. |
| 15 | applied | implementation lane taxonomy | Batch 1 added recommended lanes; Batch 2 later physically split 04_implementation_and_conformance/ into those controlled lane folders. |
| 16 | applied | accepted RFC typed grouping | Accepted RFC README now groups RFCs, closure notes, matrices, and other accepted governance records. |
| 17 | applied | decision index regeneration | DECISION_INDEX.md regenerated from DECISION_INDEX.json with human-readable decision tables. |
| 18 | applied | traceability markdown path table | TRACEABILITY_INDEX.md regenerated from JSON with concept-to-authority/RFC/schema/example columns. |
| 19 | applied | current source-input summary | CURRENT_SOURCE_INPUTS.md added and research/source-input README updated for current vs lineage source input navigation. |
| 20 | applied | regression guardrails | check_repository_steward_guardrails.py added and included in validation suite/workflows. |
