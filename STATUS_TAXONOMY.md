# OFARM status taxonomy crosswalk

Date: 2026-05-20  
Status: package metadata / repository navigation control  
Scope: crosswalk between `PROJECT_AUTHORITY.md`, `MATERIAL_STATUS.*`, and `AGENT_NAVIGATION.md`.

This file does not create semantic or runtime law. It prevents repository-control files from using incompatible status vocabularies.

## Crosswalk

| Authority class | Material-status labels | Agent-safe classes | Default handling |
|---|---|---|---|
| `ACTIVE_SUBSTANCE` | `ACTIVE_BASELINE`, `ACCEPTED_RFC`, `COMPANION_ARTIFACT`, `MACHINE_CONTRACT` | `ACTIVE_LAW`, `ACTIVE_MACHINE_CONTRACT` | Active authority according to PROJECT_AUTHORITY order; machine-contract defaults still require contract-family currentness map. |
| `ACTIVE_SUPPORTING_IMPLEMENTATION` | `IMPLEMENTATION_CONFORMANCE` | `CONFORMANCE_ONLY`, `DRAFT_NON_DEFAULT`, `PUBLIC_APP_CONTRACT_CANDIDATE`, `PLATFORM_INTERNAL_CONTRACT` | Use for implementation planning, fixtures, runners, and conformance evidence only; does not override active law. |
| `ACTIVE_SUPPORTING_RESEARCH` | `ACTIVE_SUPPORTING_RESEARCH` | `SUPPORTING_RESEARCH` | Use as research input; baseline wins. |
| `ACTIVE_SUPPORTING_CONTEXT` | `HANDOFF_PROMPT`, `LINKED_DOMAIN_ARCHITECTURE` | `PACKAGE_METADATA`, `SUPPORTING_RESEARCH` | Use for handoff, prompts, and adjacent-domain context only. |
| `REVIEW_HOLDING` | `REVIEW_HOLDING` | `REVIEW_HOLDING` | Do not treat as active law unless selectively promoted. |
| `READ_ONLY_CONTEXT` | `LEGACY_REFERENCE` | `LEGACY_DO_NOT_COPY` | Historical context only; do not copy legacy terminology into active law. |
| `PACKAGE_META` | `ROOT_PACKAGE_METADATA`, `PACKAGE_METADATA` | `PACKAGE_METADATA` | Navigation, status, inventory, validation, and package-history metadata only. |

## Authority precedence

1. `00_active_baseline/`
2. `02_accepted_rfcs/`
3. `01_companion_artifacts/`
4. `03_machine_contracts/`
5. `04_implementation_and_conformance/`
6. `06_active_supporting_research/`
7. `07_linked_domain_architectures/`
8. `05_project_handoff_and_prompts/`
9. `archive/review_holding/`
10. `legacy_reference/`

## Self-exclusion rules

- `MANIFEST.csv` excludes itself to avoid recursive self-hash ambiguity.
- `MATERIAL_STATUS.csv` and `MATERIAL_STATUS.json` exclude `MANIFEST.csv`, `MATERIAL_STATUS.csv`, and `MATERIAL_STATUS.json` for the same reason.

Use `STATUS_TAXONOMY.json` for machine-readable status control.
