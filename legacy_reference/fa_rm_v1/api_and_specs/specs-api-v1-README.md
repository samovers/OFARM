# OF Platform API Contract (v1)

## File

- `openapi-farm-rm.yaml` (legacy compatibility filename; user-facing product name is OF Platform)

## Coverage

1. Seed suitability evaluation.
2. Equipment suitability evaluation.
3. Scenario viability and replanning evaluation.
4. Contamination risk evaluation.
5. Compliance claim validation.
6. Asset obligation due listing.
7. Asset overview listing.
8. Asset service-readiness evaluation.
9. Asset obligation reminder trigger.
10. Asset obligation reminder status updates.
11. Field profitability retrieval.
12. Authority report rendering + pack listing + export bundle assembly.
13. Telematics segment classification.
14. Coverage assessment from segment traces.
15. Fuel allocation with closure diagnostics.
16. Localized label resolution.
17. Planting, mechanical weeding, cover crop management, tillage, and replant field-op events.
18. Crop stand counts, weed pressure, pest trap counts, and remote sensing index observations.
19. Warehouse lot moves, storage condition snapshots, storage aeration events, and quality panel recording.
20. Compliance dossier assembly endpoint.
21. Template projection retrieval for crop-/system-specific UI constraints.
22. AI OCR parse endpoint for deterministic receipt/label structuring proposals (`/v1/ai/ocr/parse`).
23. Capabilities discovery endpoint for client feature gating (`/v1/capabilities`).
24. Inventory resource create/resolve endpoint for confirmed label workflows (`/v1/inventory/resources`).
25. Inventory material lot create/resolve endpoint including seed lot extension semantics (`/v1/inventory/material-lots`).
26. Crop/species and variety deterministic reference search endpoints (`/v1/reference/crops/search`, `/v1/reference/varieties/search`).
27. Optional persistence pipeline to `v0.6` and `v0.8` SQL tables when DB is configured.

## Design notes

- API is contract-first and maps OF Platform behavior onto OFARM semantic artifacts packaged in `specs/v1.0.0` (source streams: `specs/v0.1` to `specs/v0.8`).
- Recommendation and risk endpoints are explainable and confidence-aware.
- Profile priority remains: organic > in-transition > conventional.
- Claim and reporting endpoints are jurisdiction-pack aware (`specs/v0.4/regulatory/rulepacks`, `specs/v0.4/regulatory/report-packs`).
- Stable contract in `openapi-farm-rm.yaml` includes the v1.0.4 asset lifecycle additions.
- v1.0.4 draft delta assets: `specs/v1.0.0/deltas/v1.0.4-scope-draft.md`, `specs/v1.0.0/deltas/v1.0.4-api-delta.yaml`.
