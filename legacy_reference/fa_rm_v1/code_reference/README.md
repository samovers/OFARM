
> **OFARM 2 legacy currentness note**  
> This file is preserved inside `legacy_reference/` as read-only historical context. It does not define active OFARM 2 law, active schema authority, current package status, or implementation direction. Read the active authority set and `legacy_reference/LEGACY_REFERENCE_INDEX.json` before using this material.

# Legacy reference — code reference

Status: `LEGACY_REFERENCE`  
Authority: read-only contextual reference only  
Latest active OFARM endpoint: `AAI-CP10`

This folder is historical FA_RM / FARM_RM / Farm-RM material retained for comparison, source mining, and lineage review. It is **not** active OFARM 2 law.

Use active authority first:

1. `00_active_baseline/`
2. `02_accepted_rfcs/`
3. `01_companion_artifacts/`
4. `03_machine_contracts/`

Then use this folder only when historical context is explicitly needed.

Repository index: `legacy_reference/LEGACY_REFERENCE_INDEX.json` and `legacy_reference/LEGACY_REFERENCE_INDEX.md`.

## Direct files

- `field_passport.py`
- `test_field_passport.py`
- `test_operation_drafts.py`
- `test_universal_capture_receipt_mixed_label_lot.py`
- `test_voice_session_fixtures.py`
- `test_voice_session_store.py`
- `universal_capture.py`
- `universal_capture_route_registry.json`
- `voice_session_routes.py`
- `voice_session_service.py`
- `voice_session_store.py`

## Subfolders

- `__pycache__/`

## Guardrail

If any legacy file conflicts with the active baseline, accepted RFCs, companion artifacts, or machine contracts, the active authority set wins. Legacy terms such as FA_RM, FARM_RM, Farm-RM, or old product/runtime names must not silently re-enter OFARM 2 active law.
