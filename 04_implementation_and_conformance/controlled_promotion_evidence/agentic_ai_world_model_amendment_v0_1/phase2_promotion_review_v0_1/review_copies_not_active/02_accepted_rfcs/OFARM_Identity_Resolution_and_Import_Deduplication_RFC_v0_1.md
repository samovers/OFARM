<!--
Promotion review copy only. This file is included inside the Phase 2 supporting review folder.
It is not active OFARM law unless copied to the active target path by a separate controlled promotion.
Phase 2 classification: AMBER.
-->

# OFARM Identity Resolution and Import Deduplication RFC v0.1

Date: 2026-05-13  
Status: draft implementation-facing RFC candidate  
Scope: Phase 6 practical farm contracts for external IDs, duplicate imports, and app/adapter identity safety

## 1. Purpose

This draft defines an app/adapter-facing identity-resolution contract so AI coding agents do not invent local duplicate handling or silently merge farm, product, worker, contractor, field, geometry, machine, storage, crop-cycle, or inventory identities.

## 2. Authority posture

This draft supports, but does not override:

- `02_accepted_rfcs/OFARM_Identity_and_Lifecycle_RFC_v0_1.md`
- `02_accepted_rfcs/OFARM_IdentityLifecycleChange_Closure_RFC_v0_1.md`
- `03_machine_contracts/schemas/agronomic/OFARM_AgronomicIdentityBinding_schema_v0_1.json`
- `03_machine_contracts/schemas/identity_lifecycle/OFARM_IdentityLifecycleChange_schema_v0_1.json`

## 3. Core decisions

1. External IDs are not OFARM canonical IDs by default.
2. Apps and adapters may propose identity bindings; they must not silently accept ambiguous bindings.
3. Duplicate import detection must run before candidate material can be submitted for promotion.
4. Ambiguous actor, product, field/geometry, or inventory identity blocks high-consequence use.
5. Supplier names, machine-local IDs, and FMIS local IDs are evidence inputs, not canonical identity decisions.
6. Duplicate replay must reuse or block prior receipts instead of creating duplicate facts.

## 4. Public operation candidates

| Operation | Purpose | Consequence |
|---|---|---|
| `identity.resolve` | Resolve/propose binding for external/local IDs | no truth effect unless later reviewed |
| `imports.checkDuplicate` | Check replay/fingerprint/idempotency posture | no truth effect |

## 5. Machine contracts

- `OFARM_IdentityResolutionRequest_schema_v0_1.json`
- `OFARM_IdentityResolutionResult_schema_v0_1.json`
- `OFARM_ImportReceipt_schema_v0_1.json`

## 6. Required app-visible states

- resolved
- ambiguous
- unresolved
- duplicate candidate
- review required
- refused

An AI-built app must render those states explicitly. It must not show “no problem” or “verified” when the platform returned ambiguity.
