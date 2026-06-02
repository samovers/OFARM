# OFARM Phase 6 Practical Farm Contracts Conformance Gates v0.1

Date: 2026-05-13  
Status: implementation/conformance candidate

## Gates

A platform implementation fails Phase 6 conformance if any of the following is true:

1. A high-consequence calculation succeeds with unresolved unit, product, area, formula, rounding, or inventory identity.
2. Display rounding changes a governed quantity result.
3. A UI or SDK computes consequence-bearing product quantities locally without a `CalculationSpec`/`CalculationResult` trace.
4. An external FMIS/machinery/sensor payload is promoted directly to accepted truth.
5. A candidate import lacks a source-fidelity envelope, immutable import receipt, or loss map.
6. Ambiguous actor, product, field, geometry, machine, or inventory identity is silently accepted.
7. Duplicate import replay creates duplicate facts instead of reusing or blocking a receipt.
8. Offline capture is displayed as accepted execution before governed sync replay succeeds.
9. Sync replay does not recheck authority, delegation, revocation, scope, identity, and evidence posture.
10. Minimum capture defaults unknown actor/product/unit/area/time values instead of preserving missing/late-bound states.

## Required positive proof

- Calculation preview success and refusal fixtures validate.
- Identity ambiguity remains app-visible.
- FMIS shadow import stays candidate-only.
- Offline delayed sync returns review-required when revocation crossing or missing evidence exists.
- Minimum capture profile remains `DRAFT_NON_DEFAULT` and blocks high-consequence output when required data is missing.
