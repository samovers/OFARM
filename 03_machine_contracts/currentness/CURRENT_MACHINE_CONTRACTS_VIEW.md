# Current Machine Contracts View

Metadata:

- viewType: MACHINE_CONTRACT_CURRENTNESS_READER_VIEW
- generatedOrCuratedAt: `2026-06-02T22:05:00+02:00`
- currentPackageIdentity: `OFARM2_2026-05-30_cp15_agentic_software_delivery_model_deployment_governance_merged_v0_2_final_currentness_normalized`
- latestControlledAmendment: CP15
- doNotOverrideCanonicalAuthority: true
- semanticLawChanged: false
- activeAuthorityContentModified: false
- schemasMoved: false
- draftsMoved: false
- draftContractsPromoted: false

This reader view separates the machine-contract lanes for development navigation. It does not override `00_active_baseline/`, `02_accepted_rfcs/`, or `01_companion_artifacts/`.

## Current/default schema lane

- `03_machine_contracts/schemas/`
- moved: false
- promotionChanged: false

Use `CONTRACT_FAMILY_CURRENTNESS.json` and `CONTRACT_INDEX.json` to select current/default schemas. Do not select current/default schemas by filename search alone.

## Draft/non-default lane

- `03_machine_contracts/drafts_non_default/`
- moved: false
- promotionChanged: false

CP11, CP12, CP13, CP14, and CP15 draft/non-default contracts remain draft/non-default. Phase 3 does not promote them to current/default.

## Currentness/control maps

- `03_machine_contracts/CONTRACT_FAMILY_CURRENTNESS.json`
- `03_machine_contracts/CONTRACT_INDEX.json`
- `03_machine_contracts/DRAFT_NON_DEFAULT_INDEX.json`
- `03_machine_contracts/EXAMPLE_SCHEMA_MAP.json`

These are currentness/control maps. They are not generated-only artifacts unless a separate derived mirror explicitly marks itself as derived.

## Examples and schema-example mappings

Examples and fixtures live under `04_implementation_and_conformance/`. `EXAMPLE_SCHEMA_MAP.json` maps examples to the schemas they exercise and does not make examples active contract law.

## Path remaps and migration aids

- `03_machine_contracts/PATH_REMAPS.json`

Path remaps are navigation and migration aids. They preserve lineage and do not create active law.

## Generated mirror policy

Generated mirrors are derived views only. A generated mirror must self-mark `derivedFrom` and `doNotCiteAsIndependentSource`. Generated mirror rebuild belongs to Phase 7 unless the mirror is local to this `currentness/` view.

