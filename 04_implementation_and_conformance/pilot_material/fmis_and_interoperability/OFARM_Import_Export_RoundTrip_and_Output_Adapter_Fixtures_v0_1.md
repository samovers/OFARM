# OFARM import/export round-trip and output-adapter fixtures v0.1

Date: 2026-04-11  
Status: active supporting implementation artifact  
Scope: starter executable fixtures for import-surface promotion posture, declared mapping round-trip feasibility, and output-adapter boundary trace-back after Wave 8

---

## Purpose

This wave keeps work inside `04_implementation_and_conformance/`.
It does not amend baseline law, accepted RFCs, companion policy, or machine-contract substance.

The goal is to close the next honest gap after Wave 8:
- move external-surface conformance from static consistency checks toward runtime-shaped path evidence
- start a declared-surface round-trip suite even though the package still ships only one-way mappings
- widen output-boundary proof across live passport export, frozen dossier packaging, and frozen submission filing

---

## Fixture families

### 1. Import-surface promotion posture

Fixtures:
- `adapt_import_claim_first.json`
- `isoxml_import_claim_first.json`

Expected:
- mapping direction is `IMPORT`
- coverage and loss declarations resolve cleanly
- default commit classes stay limited to evidence/claim-first material
- accepted consequences still require review
- the simulated gate path stops at normalized draft/claim material instead of direct accepted truth

### 2. Export-surface projection posture

Fixture:
- `ngsi_ld_live_passport_export.json`

Expected:
- mapping direction is `EXPORT`
- runtime surface contract resolves to the declared NGSI-LD export surface
- semantic posture remains `PROJECTION_ONLY`
- publication is a live `PassportView` share, not a frozen attestable document action

### 3. Declared mapping round-trip feasibility

Fixtures:
- `roundtrip_adapt_import_declared_surface.json`
- `roundtrip_isoxml_import_declared_surface.json`
- `roundtrip_ngsi_ld_export_declared_surface.json`

Expected:
- each declared surface receives a machine-generated round-trip feasibility record
- one-way import surfaces are marked honestly as non-reversible in the current package
- the NGSI-LD export surface is marked honestly as projection-only and non-canonical

### 4. Output-adapter boundary trace-back

Fixtures:
- `output_adapter_field_dossier_frozen_package.json`
- `output_adapter_submission_filing_frozen.json`

Expected:
- dossier packaging remains a frozen document-family path with retained basis/snapshot/evidence grounding
- submission filing remains a frozen submission-family path with evidence sufficiency and publication outcome retained
- live passport export remains distinct from both frozen document families

---

## Validation posture

The paired runner intentionally emits `PASS_WITH_LIMITATIONS` when successful.
That is the correct posture for this wave because:
- the package still ships declared one-way mapping surfaces rather than reversible bridge packs
- runtime evidence is replay-shaped and package-relative, not executor-native ingest/export telemetry
- some output-adapter families remain package-level rather than runtime-surface-level in the current active package
