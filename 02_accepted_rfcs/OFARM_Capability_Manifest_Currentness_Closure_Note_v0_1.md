# OFARM Capability Manifest currentness closure note v0.1

Date: 2026-04-17  
Status: accepted closure companion artifact (colocated with the Capability Manifest RFC family)  
Scope: clarify the default currentness rule for parallel v0.1 and v0.2 draft Capability Manifest contracts

---

## Decision

- `03_machine_contracts/schemas/runtime_surface/OFARM_Capability_Manifest_schema_v0_1.json` remains the **default current contract** for general OFARM Capability Manifest validation and deployment comparison.
- `03_machine_contracts/drafts_non_default/schemas/runtime_surface/OFARM_Capability_Manifest_schema_v0_2_draft.json` remains an **active extension-era draft** introduced by `OFARM_Conformance_Claim_Set_and_Capability_Manifest_Reference_Extension_RFC_v0_1.md`.
- The v0.2 draft is **non-default** until a non-draft successor or a later accepted note explicitly promotes it.

## Why this note exists

The package currently contains both a v0.1 Capability Manifest contract family and a v0.2 draft extension family at active-substance level.
Without an explicit currentness rule, tools and reviewers could choose different defaults and fragment comparison behavior.

## Practical rule

- default validation target: v0.1
- controlled extension experimentation: v0.2 draft
- repository maps and implementation notes should state this distinction explicitly whenever both families are shown together
