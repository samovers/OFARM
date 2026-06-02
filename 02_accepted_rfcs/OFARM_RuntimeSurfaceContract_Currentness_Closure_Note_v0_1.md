# OFARM RuntimeSurfaceContract currentness closure note v0.1

Date: 2026-04-19  
Status: accepted closure companion artifact (colocated with the interoperability/runtime-surface RFC family)  
Scope: clarify the default currentness rule for parallel RuntimeSurfaceContract v0.1 and v0.2 draft contract families and introduce a bounded non-default extension for meaning-bearing runtime-surface fields

---

## Decision

- `03_machine_contracts/schemas/runtime_surface/OFARM_RuntimeSurfaceContract_schema_v0_1.json` remains the **default current contract** for general OFARM RuntimeSurfaceContract validation and ordinary manifest/discovery comparison.
- `03_machine_contracts/drafts_non_default/schemas/runtime_surface/OFARM_RuntimeSurfaceContract_schema_v0_2_draft.json` is introduced as an **active extension-era draft** for bounded experimentation with meaning-bearing runtime-surface fields that are currently too implicit in the v0.1 contract family.
- The v0.2 draft is **non-default** until a later accepted RFC or accepted promotion note explicitly promotes it.

## Why this note exists

The accepted interoperability/runtime-surface RFC already says that pack merge legality depends on whether runtime surfaces are disjoint or materially identical in their meaning-bearing parts, including endpoint/path/topic/query-façade identity.

The shipped v0.1 contract is intentionally minimal, but that minimality leaves several comparison-critical details outside the governed contract shape:
- surface identity across contract revisions
- endpoint/path/topic/query/discovery binding identity
- surface version and compatibility posture
- auth posture
- delivery semantics
- idempotency posture

Without an explicit currentness rule, tools and reviewers could either:
- over-read the v0.1 contract and infer behavior from external service-description documents, or
- prematurely treat a richer experimental schema as the new default.

This note prevents both failure modes.

## Practical rule

- default validation target: `OFARM_RuntimeSurfaceContract_schema_v0_1.json`
- controlled extension experimentation: `OFARM_RuntimeSurfaceContract_schema_v0_2_draft.json`
- manifests, discovery records, and current package maps should continue to treat v0.1 as the current default unless a later active note says otherwise
- runtime-surface drift analysis may use v0.2 draft examples where a package needs to compare meaning-bearing boundary posture more explicitly

## What the v0.2 draft adds

The v0.2 draft adds a bounded set of non-default fields for:
- stable surface identity separate from contract artifact identity
- explicit surface binding identity
- version/compatibility posture
- auth posture
- delivery semantics
- idempotency posture

This is a hardening extension only.
It does **not**:
- turn OFARM into an API-first standard
- replace service-description artifacts such as OpenAPI or AsyncAPI
- reopen RC2.1 constitutional/runtime law
- change the pack-merge family names introduced by the accepted interoperability/runtime-surface RFC

## Result

After this note:
- v0.1 remains the live default for normal package work
- v0.2 draft is available for bounded runtime-surface hardening and hostile integrator comparison work
- package maps and implementation notes should state the distinction explicitly whenever both contract families are shown together
