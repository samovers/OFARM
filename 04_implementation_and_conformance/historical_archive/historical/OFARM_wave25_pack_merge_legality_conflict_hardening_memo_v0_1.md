# OFARM Wave 25 pack-merge legality and conflict hardening memo v0.1

Date: 2026-04-12  
Status: active supporting implementation artifact  
Scope: bounded implementation/conformance closure for the remaining pack-merge seam after Wave 24

---

## 1. Why this wave exists

After Wave 24, the central query-side seams were closed, but the conformance matrix still left the pack-merge cluster only partially covered.

The remaining open rows were:

- pack compatibility tests
- pack conflict determinism checks
- surface-family merge-mode legality tests
- vocabulary-binding merge fixtures
- evidence-policy merge fixtures
- template-constraint merge fixtures
- decision-rule merge fixtures
- event-subtype merge fixtures
- view/document shaping merge fixtures

Those rows all depend on the same constitutional/runtime seam:
surface-family-specific pack merge legality under deterministic activation evaluation.

This wave closes that cluster without changing active law.

---

## 2. What this wave does

This wave adds bounded runtime-shaped evidence for all governed merge surface families named in the Pack Merge Semantics RFC:

- VOCABULARY_BINDINGS
- EVIDENCE_POLICY
- ARCHETYPE_DEFINITION
- TEMPLATE_CONSTRAINT
- VALIDATION_RULE
- DECISION_RULE
- EVENT_SUBTYPE_DEFINITION
- VIEW_SHAPING
- DOCUMENT_ASSEMBLY_SHAPING

For each family, the wave emits executable records that show:

- which merge mode was selected
- whether the overlap was safe or unsafe
- which deterministic activation outcome followed
- which reason code was emitted
- that repeated evaluation stays stable

The wave also emits a surface-family coverage record so the matrix can point to a direct runtime-shaped coverage summary instead of only older prose fixtures.

---

## 3. What this wave does not do

This wave does **not**:

- change baseline law
- amend accepted RFCs
- amend companion policy
- add new machine-contract substance
- claim deployment-produced pack-activation telemetry

The added evidence is still fixture-bounded, but it is now broad enough to close the remaining pack-merge conformance rows that were only partially covered.

---

## 4. Main evidence produced

The new core artifacts are:

- `OFARM_Runtime_Pack_Merge_and_Surface_Legality_Fixtures_v0_1.md`
- `ofarm_runtime_pack_merge_and_surface_legality_runner_v0_1.py`
- `OFARM_runtime_pack_merge_surface_legality_records_v0_1.json`
- `OFARM_runtime_pack_conflict_determinism_records_v0_1.json`
- `OFARM_runtime_pack_surface_family_coverage_records_v0_1.json`
- `OFARM_runtime_pack_merge_telemetry_v0_1.json`
- `OFARM_runtime_pack_merge_and_surface_legality_results_v0_1.json`

---

## 5. Expected matrix movement

This wave is intended to move the following rows to `COVERED`:

- pack compatibility tests
- pack conflict determinism checks
- surface-family merge-mode legality tests
- vocabulary-binding merge fixtures
- evidence-policy merge fixtures
- template-constraint merge fixtures
- decision-rule merge fixtures
- event-subtype merge fixtures
- view/document shaping merge fixtures

---

## 6. Remaining boundary after this wave

The pack-merge cluster is still only fixture-backed, not deployment-backed.
That is acceptable for this stage because the target was conformance closure of the constitutional/runtime seam, not rollout telemetry.

If later deployment-produced pack-activation telemetry is added, these rows can be retained as covered and simply widened.
