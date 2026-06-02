# OFARM Wave 20 repo-relative patch README v0.1

Date: 2026-04-12  
Status: active supporting implementation artifact  
Scope: bounded profile-compatibility and activation-set conformance hardening patch

---

## What this patch changes

This patch adds a new implementation/conformance wave for:
- runtime-shaped profile compatibility scenarios
- runtime activation decision logs for profile evaluation
- telemetry/results artifacts for profile compatibility
- conformance matrix updates
- conformance seed-set updates

It does **not** change:
- baseline law
- accepted RFCs
- companion policy
- machine-contract substance

---

## Primary artifacts added

- `OFARM_wave20_profile_compatibility_activation_set_hardening_memo_v0_1.md`
- `OFARM_Runtime_Profile_Compatibility_Fixtures_v0_1.md`
- `ofarm_runtime_profile_compatibility_runner_v0_1.py`
- `OFARM_runtime_profile_compatibility_records_v0_1.json`
- `OFARM_runtime_profile_activation_decision_logs_v0_1.json`
- `OFARM_runtime_profile_compatibility_telemetry_v0_1.json`
- `OFARM_runtime_profile_compatibility_results_v0_1.json`

## Files updated

- `OFARM_conformance_coverage_matrix_v0_1.md`
- `OFARM_conformance_seed_set_v0_1.md`

---

## Intended effect

This patch is intended to:
- close `profile compatibility tests`
- close `pack activation-set compatibility checks`
- strengthen profile-side evidence for pack compatibility and deterministic conflict handling
