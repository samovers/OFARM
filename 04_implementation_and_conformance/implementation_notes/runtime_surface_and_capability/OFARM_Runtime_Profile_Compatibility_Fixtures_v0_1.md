# OFARM Runtime Profile Compatibility Fixtures v0.1

Date: 2026-04-12  
Status: executable/conformance fixture note  
Scope: bounded runtime-shaped fixtures for profile compatibility and PackActivationSet evaluation depth

---

## Purpose

These fixtures make profile compatibility executable at package level.

They focus on the smallest high-value cases still missing after earlier pack-activation and authority/current-state waves:
- narrowing profiles that are safe
- disjoint recipient-facing shaping profiles that are safe
- lower-precedence weakening attempts that must fail
- unresolved same-precedence shaping conflicts that must route to governance
- scope-separated and time-separated coexistence
- dependency and exclusion failures

They do **not** claim full pack/profile manifest closure.

---

## Executable scenarios in this package

### Fixture 1 — orchard narrowing profile allowed by declared merge
- active baseline profile: `profile:slovenia-organic-baseline:v1`
- requested profile: `profile:partnerA-orchard:v1`
- dominant surfaces: `EVIDENCE_POLICY`, `TEMPLATE_CONSTRAINT`
- safety posture: monotone narrowing + stronger evidence requirement

Expected:
- activation allowed
- compatibility class = `COMPATIBLE_WITH_DECLARED_MERGE`

### Fixture 2 — buyer lot-summary profile allowed as plain compatibility
- requested profile affects only disjoint `VIEW_SHAPING`
- no same-slot attested conflict with active baseline profile

Expected:
- activation allowed
- compatibility class = `COMPATIBLE`

### Fixture 3 — local relaxed profile denied for higher-precedence weakening attempt
- active certification baseline is higher precedence
- requested local/community profile would weaken evidence or claim constraints

Expected:
- activation denied
- compatibility class = `EXCLUSIVE`
- stable reason code = `PROFILE_WEAKENS_HIGHER_PRECEDENCE_REQUIREMENT`

### Fixture 4 — competing premium-output profiles require governance
- same-precedence recipient/output profiles touch conflicting attested output slots
- no approved ordering or narrowing profile exists

Expected:
- activation outcome = `GOVERNANCE_REQUIRED`
- compatibility class = `GOVERNANCE_REQUIRED`

### Fixture 5 — scope-separated crop-system profiles are allowed
- potentially conflicting crop-system profiles exist on neighboring zones
- evaluated activation set is for a non-colliding target zone

Expected:
- activation allowed
- compatibility class = `COMPATIBLE_BY_SCOPE_SEPARATION`

### Fixture 6 — time-window-separated seasonal profiles are allowed
- a prior seasonal profile exists outside the evaluated window
- requested profile applies in a later non-overlapping window

Expected:
- activation allowed
- compatibility class = `COMPATIBLE`

### Fixture 7 — missing required pack dependency is denied
- requested profile depends on a pack that is neither already active nor requested

Expected:
- activation denied
- compatibility class = `EXCLUSIVE`
- stable reason code = `PROFILE_MISSING_REQUIRED_PACK`

### Fixture 8 — declared exclusion is denied deterministically
- requested profile is explicitly excluded by an already-active profile in the same activation set

Expected:
- activation denied
- compatibility class = `EXCLUSIVE`
- stable reason code = `PROFILE_DECLARED_EXCLUSION`

---

## Executable evidence

This wave writes:
- `OFARM_runtime_profile_compatibility_records_v0_1.json`
- `OFARM_runtime_profile_activation_decision_logs_v0_1.json`
- `OFARM_runtime_profile_compatibility_telemetry_v0_1.json`
- `OFARM_runtime_profile_compatibility_results_v0_1.json`
