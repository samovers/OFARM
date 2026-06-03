# DEV/AUDIT Packaging Policy

Current package: `OFARM2_2026-05-30_cp15_agentic_software_delivery_model_deployment_governance_merged_v0_2_final_currentness_normalized`.

Latest controlled amendment: **CP15**.

This policy defines external packaging profiles only. It does not create OFARM law, change authority, promote drafts, or move source repository material.

## Purpose

The source repository is clean-baseline-current and still carries audit/provenance material needed for stewardship. The DEV/AUDIT split gives two package views without redesigning the source repo:

- DEV: a lean development-starting-point package for implementation work.
- AUDIT: a complete proof/provenance package for review and reconstruction.

## DEV Package

The DEV package includes the current root entrypoints, active authority lanes, machine contracts, supporting development material, current generated indexes, release-profile tooling, final minimal validation/readiness proof, and release metadata needed to begin implementation.

The DEV package excludes audit-heavy phase report folders and generated ZIP/report artifacts. It may include clean-baseline ledgers when those ledgers are needed by current reader views, validators, or development currentness checks.

## AUDIT Package

The AUDIT package includes source context plus proof material: clean-baseline ledgers and reports, phase report folders, final validation/readiness/debt records, relocation maps, currentness audits, generated-index rebuild ledgers, validator update ledgers, material-status repair ledgers, GitHub reconciliation repair evidence, and package release metadata.

The AUDIT package is not the lean development baseline. It is a provenance bundle for reviewers and stewards.

## Source Repository

The source repository remains the canonical working repository. Do not move audit files out of the source repo as part of this packaging-profile split. Do not move canonical authority files, baseline patch folders, schema lanes, draft/non-default lanes, `legacy_reference/`, `07_linked_domain_architectures/`, or additional package history folders.

## Excluded Source-Tree Clutter

The following must not be committed as source-tree content:

- root-level final package ZIPs
- root-level report ZIPs
- generated DEV/AUDIT ZIPs
- generated DEV/AUDIT staging directories
- local OS/cache/editor files
- `.DS_Store`
- `__pycache__/`
- `*.pyc`
- `node_modules/`

Intentional archive ZIPs under `archive/` are not banned by this policy.

## Validation Expectations

Before release-profile packaging, the source repo must pass:

- `python3 package_meta/tools/check_release_profile_policy.py`
- `python3 package_meta/tools/run_repository_validation_suite.py`

Each generated profile package must pass profile staging checks. The DEV profile should validate as a development package. The AUDIT profile should validate as a provenance package.

## Handoff

Hand off DEV packages to developers and Codex implementation work. Hand off AUDIT packages to reviewers, auditors, and stewards who need evidence reconstruction.
