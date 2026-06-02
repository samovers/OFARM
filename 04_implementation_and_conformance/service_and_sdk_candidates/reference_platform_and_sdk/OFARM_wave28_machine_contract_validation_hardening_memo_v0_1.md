# OFARM wave 28 machine-contract validation hardening memo v0.1

Date: 2026-04-12  
Status: active supporting implementation artifact  
Change class: implementation/conformance implication  
Affected active law: none  
Affected active baseline files: none

---

## 1. Purpose

This wave closes the remaining package-internal gap on **baseline validation suites for core artifact kinds**.

The package already had broad positive schema/example validation through `OFARM_machine_contract_validation_results_v0_8.json`, but the conformance matrix still marked the row **PARTIAL** because it lacked three things:
- bounded negative validation
- bounded broken-reference cases
- richer package-local cross-file consistency checks

Wave 28 adds those three elements without changing baseline law, accepted RFCs, companion policy, or machine-contract substance.

---

## 2. What was added

Wave 28 adds:
- `ofarm_contract_validation_runner_v0_9.py`
- `OFARM_machine_contract_validation_results_v0_9.json`
- `OFARM_machine_contract_negative_validation_records_v0_1.json`
- `OFARM_machine_contract_reference_consistency_records_v0_1.json`
- `OFARM_Machine_Contract_Negative_and_Reference_Validation_Fixtures_v0_1.md`

The runner now executes four bounded checks over the consolidated amended package:
1. schema self-validation
2. positive example validation
3. one bounded negative mutation per shipped schema family
4. package-local resolvable reference consistency plus injected broken-reference failure cases

---

## 3. Validation outcome

The resulting package evidence is:
- 34 schemas validated
- 101 positive examples validated
- 34 bounded negative mutation cases checked, with 34 expected failures and 0 unexpected passes
- 138 package-local resolvable reference checks recorded
- 4 multi-target variant reference cases recorded as controlled variants
- 20 injected broken-reference cases checked, with 20 expected failures and 0 unexpected passes

Overall result: `PASS`

---

## 4. Boundary of the claim

This wave does **not** claim that every ref string in the package should resolve inside the package.

Some refs are intentionally external, deployment-anchored, or only meaningful at runtime boundary level. The Wave 28 cross-file check is therefore explicitly scoped to **package-local resolvable refs** only.

That narrower claim is still sufficient to close the conformance row because the row was about baseline validation for shipped core artifact kinds, not universal deployment-time resolution.

---

## 5. Conformance effect

`OFARM_conformance_coverage_matrix_v0_1.md` now advances:
- `baseline validation suites for core artifact kinds` → `COVERED`

This leaves the remaining partials concentrated in areas that depend on broader deployment evidence rather than purely package-internal validation.
