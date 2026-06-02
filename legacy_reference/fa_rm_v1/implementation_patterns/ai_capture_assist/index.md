# AI Capture Assist + Reference + Agronomy Knowledge (Spec Set)

Version: 0.4 (draft)
Date: 2026-03-13
Applies to: Farm_RM backend + Farman Lite iOS (offline-first)

This spec set defines a single coherent feature spanning:

1. AI-assisted OCR structuring (backend proposes structured data, never persists truth directly).
2. Crop/species + variety reference and deterministic normalization.
3. Agronomy “season windows” knowledge pack for operation timing priors.
4. Session-based universal capture intake over document registry, OCR parse provenance, review, helpers, and route-specific commit adapters.
5. iOS integration: receipt scan + label scan flows, offline queue, provenance UX.
6. Security, privacy, QA, rollout gates.

Design principle (normative): **AI proposes business meaning; Farm_RM enforces truth.** Intake may persist document and parse provenance when the contract explicitly says so.

Current backend intake authority:

- Part 7 is the current runtime-reconciled source for universal capture intake and universal scanner backend behavior. Older Parts 0-6 remain useful context, but Part 7 wins when those pages differ on intake orchestration, route naming, or persistence semantics.

## Spec Parts

1. Part 0: Fit, invariants, glossary (foundation): [part-0-fit-invariants-glossary.md](/Users/einstein/Documents/Codex/Semantic%20farming/docs/implementation/ai-capture-assist/part-0-fit-invariants-glossary.md)
2. Part 1: OCR parse contract (`POST /v1/ai/ocr/parse`): [part-1-ocr-parse-contract.md](/Users/einstein/Documents/Codex/Semantic%20farming/docs/implementation/ai-capture-assist/part-1-ocr-parse-contract.md)
3. Part 1A: Hybrid per-item resolution + prompt registry (backend): [part-1a-hybrid-item-resolution-prompts.md](/Users/einstein/Documents/Codex/Semantic%20farming/docs/implementation/ai-capture-assist/part-1a-hybrid-item-resolution-prompts.md)
4. Part 2: Inventory persistence targets (label flow + backward compatibility): [part-2-inventory-persistence-targets.md](/Users/einstein/Documents/Codex/Semantic%20farming/docs/implementation/ai-capture-assist/part-2-inventory-persistence-targets.md)
5. Part 3: Crop/variety reference + normalization: [part-3-crop-variety-reference-normalization.md](/Users/einstein/Documents/Codex/Semantic%20farming/docs/implementation/ai-capture-assist/part-3-crop-variety-reference-normalization.md)
6. Part 4: Agronomy season windows (knowledge pack + API): [part-4-agronomy-season-windows.md](/Users/einstein/Documents/Codex/Semantic%20farming/docs/implementation/ai-capture-assist/part-4-agronomy-season-windows.md)
7. Part 5: iOS integration (flows, offline queue, UX rules): [part-5-ios-integration.md](/Users/einstein/Documents/Codex/Semantic%20farming/docs/implementation/ai-capture-assist/part-5-ios-integration.md)
8. Part 6: Security, privacy, QA, rollout: [part-6-security-privacy-qa-rollout.md](/Users/einstein/Documents/Codex/Semantic%20farming/docs/implementation/ai-capture-assist/part-6-security-privacy-qa-rollout.md)
9. Part 7: Universal capture intake contract (`/v1/intake/*`): [part-7-universal-capture-intake-contract.md](/Users/einstein/Documents/Codex/Semantic%20farming/docs/implementation/ai-capture-assist/part-7-universal-capture-intake-contract.md)
10. iOS handover (universal scanner Phase 2 over document ingest + universal capture intake): [ios-handover-universal-scanner-phase-2.md](/Users/einstein/Documents/Codex/Semantic%20farming/docs/implementation/ai-capture-assist/ios-handover-universal-scanner-phase-2.md)
11. iOS handover (SI inventory scan fields + payload mapping): [ios-handover-ai-inventory-scan-si.md](/Users/einstein/Documents/Codex/Semantic%20farming/docs/implementation/ai-capture-assist/ios-handover-ai-inventory-scan-si.md)
12. iOS residual Phase 1 follow-up handover (seed-exception sync + A.1/A.5 read-model deltas): [ios-handover-residual-phase-1-client-followup-2026-03-06.md](/Users/einstein/Documents/Codex/Semantic%20farming/docs/implementation/ai-capture-assist/ios-handover-residual-phase-1-client-followup-2026-03-06.md)
13. iOS E2E smoke checklist (seed-exception receipt flow): [ios-seed-exception-receipt-flow-e2e-smoke-checklist-2026-03-06.md](/Users/einstein/Documents/Codex/Semantic%20farming/docs/implementation/ai-capture-assist/ios-seed-exception-receipt-flow-e2e-smoke-checklist-2026-03-06.md)
14. Backend rollout checklist for residual Phase 1 seed-exception runtime alignment: [backend-rollout-checklist-v1-0-14-seed-exception.md](/Users/einstein/Documents/Codex/Semantic%20farming/docs/implementation/backend-rollout-checklist-v1-0-14-seed-exception.md)
15. Gap analysis (runtime baseline + residual gaps): [gap-analysis.md](/Users/einstein/Documents/Codex/Semantic%20farming/docs/implementation/ai-capture-assist/gap-analysis.md)
16. Implementation plan (historical baseline + residual work): [implementation-plan.md](/Users/einstein/Documents/Codex/Semantic%20farming/docs/implementation/ai-capture-assist/implementation-plan.md)
17. Reference snapshot ingestion runbook (EPPO/EU/CPVO -> Farm-RM): [specs/v0.8/reference-ingest/README.md](/Users/einstein/Documents/Codex/Semantic%20farming/specs/v0.8/reference-ingest/README.md)

## Normative Dependencies (Existing Artifacts)

This spec set is designed to align with existing Farm_RM persistence primitives and patterns:

- Receipt import persistence (already present): `inventory_receipt_import` + `inventory_receipt_line_item`
  - Migration: [0018_v1_7_si_recordbook_diary_persistence.sql](/Users/einstein/Documents/Codex/Semantic%20farming/specs/v0.8/sql/migrations/0018_v1_7_si_recordbook_diary_persistence.sql)
  - API implementation: `POST /v1/inventory/receipts/import`
    - Server: [main.py](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/app/main.py)
    - OpenAPI: [openapi-farm-rm.yaml](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/openapi-farm-rm.yaml)

- Reference crop/variety tables (already present; will be extended/served via API in this spec):
  - Migration: [0006_v1_2_crop_suitability.sql](/Users/einstein/Documents/Codex/Semantic%20farming/specs/v0.3/sql/migrations/0006_v1_2_crop_suitability.sql)

- Multilingual labels (already present; used by reference endpoints in this spec):
  - Migration: [0010_v1_5_equipment_energy_multilingual.sql](/Users/einstein/Documents/Codex/Semantic%20farming/specs/v0.6/sql/migrations/0010_v1_5_equipment_energy_multilingual.sql)
