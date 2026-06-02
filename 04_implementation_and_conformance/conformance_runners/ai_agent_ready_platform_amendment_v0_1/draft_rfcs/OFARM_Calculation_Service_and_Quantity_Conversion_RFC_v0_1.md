# OFARM Calculation Service and Quantity Conversion RFC v0.1

Date: 2026-05-13  
Status: draft implementation-facing RFC candidate  
Scope: Phase 6 practical farm contracts for AI-agent-ready platform implementation

## 1. Purpose

This draft closes the application-builder gap around farm calculations. It does not create new agronomic formula law. It defines the public/platform contract needed so AI-generated platform or app code does not hide unit conversion, product amount, rate-area, carrier volume, active ingredient, inventory drawdown, or rounding logic in UI code.

## 2. Authority posture

Active baseline law and accepted RFCs still govern. This draft supports, but does not override:

- `00_active_baseline/OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md`
- `00_active_baseline/OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md`
- `02_accepted_rfcs/OFARM_Quantity_Bearing_Intervention_and_As_Applied_RFC_v0_1.md`
- `00_active_baseline/OFARM_Alignment_Register_v0_13.md`

## 3. Core decisions

1. Consequence-bearing calculations must be requested through a governed calculation surface or service.
2. UI-local arithmetic may be used only for non-governed display hints and must be marked display-only.
3. A calculation preview does not create canonical truth, accepted consequence, inventory mutation, or compliance output.
4. Unit, product, area, formula, rounding-policy, or inventory identity ambiguity must be surfaced as a refusal or review-required result for high-consequence use.
5. Calculation results must carry trace references and blocked-use posture.
6. Formula catalog entries remain draft/profile-governed unless promoted by normal OFARM authority.

## 4. Public operation candidates

| Operation | Purpose | Consequence |
|---|---|---|
| `calculations.preview` | Calculate without truth effect | read-only / no truth effect |
| `calculations.convertUnits` | Convert with governed unit basis | read-only / trace required |
| `calculations.formulas.get` | Read formula catalogue | read-only |

## 5. Machine contracts

- `OFARM_CalculationSpec_schema_v0_1.json`
- `OFARM_CalculationResult_schema_v0_1.json`
- `OFARM_UnitConversionTrace_schema_v0_1.json`
- `OFARM_FormulaCatalog_schema_v0_1.json`

## 6. Required refusals

The calculation service must refuse or mark review-required when:

- `unitRef` is unresolved
- product identity is ambiguous
- extent/area basis is stale, disputed, or missing
- formula or rounding policy is not governed for the requested use
- source quantity comes from candidate-only import and requested use is compliance or publication
- inventory identity is unresolved for drawdown

## 7. Conformance hooks

Phase 6 conformance must prove that:

- display rounding cannot alter governed results
- unresolved units block high-consequence output
- candidate FMIS quantities do not become inventory mutation without promotion
- formula IDs and versions are traceable
- calculation previews return `blockedUses` where appropriate
