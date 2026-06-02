# Gap Analysis: AI Capture Assist Runtime Baseline vs Residual Gaps

Date: 2026-03-13
Applies to: Farm_RM backend + Farman Lite iOS

This page is the runtime-reconciled gap view for the AI Capture Assist spec pack.

It supersedes earlier assumptions that OCR parse, capabilities, reference search, season windows, document registry, and session-based intake were still missing. For the current backend intake contract, use [part-7-universal-capture-intake-contract.md](/Users/einstein/Documents/Codex/Semantic%20farming/docs/implementation/ai-capture-assist/part-7-universal-capture-intake-contract.md).

## 1. Implemented Backend Baseline

Observed current state:

1. `GET /v1/capabilities` is implemented and typed.
2. `POST /v1/ai/ocr/parse` is implemented, contract-tested, and already supports document-backed provenance through `documentUri` and `parseRunUri`.
3. Reference search and snapshot surfaces are implemented for crop/species and variety lookup.
4. `GET /v1/agronomy/season-windows` is implemented.
5. Document registry and parse-run persistence are implemented.
6. Session-based intake under `/v1/intake/*` is implemented and backed by runtime models, SQL tables, and tests.

Evidence:

- Runtime/backend contracts: [main.py](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/app/main.py)
- Static contract snapshot: [openapi-farm-rm.yaml](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/openapi-farm-rm.yaml)
- Intake analysis and route selection: [universal_capture.py](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/app/universal_capture.py)
- Intake SQL schema: [0114_v1_7_universal_capture_intake.sql](/Users/einstein/Documents/Codex/Semantic%20farming/specs/v0.8/sql/migrations/0114_v1_7_universal_capture_intake.sql)
- Intake and OCR tests: [test_api.py](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/tests/test_api.py), [test_openapi_contract_alignment.py](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/tests/test_openapi_contract_alignment.py)

## 2. Implemented Intake Coverage

Current enabled route families:

1. `receipt.invoice`
2. `seed_label_or_tag`
3. `fertilizer_label`
4. `soil_analysis_report`
5. `fertilization_plan`
6. `delivery_note`
7. `seed_authorization_or_derogation`
8. `storage_lot_label`
9. `unknown.review`

Current proven helper behavior:

1. `receipt_plus_label_link` is enabled and can enrich a receipt session with supporting seed-label evidence.

Important nuance:

1. Route `availability` and route `repoStatus` are intentionally different signals.
2. Some routes are runtime-enabled even though the registry still labels them `planned`, `partial`, `unknown`, or `implemented-adjacent`.

## 3. Residual Backend Gaps

Residual backend gaps:

1. `ffs_label` exists only as a shadow route with `new_adapter_required`.
2. `o10_fertilizer_log` exists only as a shadow route with `new_adapter_required`.
3. `o11_ffs_log` exists only as a shadow route with `new_adapter_required`.
4. Async/background scanner jobs are not yet a public intake contract.
5. Public discard/delete semantics for intake sessions and linked evidence are not yet implemented, even though SQL reserves `abandoned`.
6. A plant/leaf lab analysis report route is not yet proven in current runtime routes, tests, or public models.
7. Generic evidence-only review queue behavior is not yet a separate public contract; current fallback is `unknown.review`.

## 4. Residual Client And Product Gaps

Residual client and product gaps:

1. Farman Lite iOS docs still need to converge on `/v1/intake/*` as the canonical orchestration seam, instead of treating direct parse plus route-specific writes as the only flow.
2. Photo-recognition flows remain out of scope for the current document-first intake contract.
3. Some route families are still gated behind capability state or remain shadow-only until route-specific commit adapters and tests are added.

## 5. Key Risks And Watchouts

1. Do not flatten `repoStatus` into runtime availability; both fields matter.
2. Do not generalize the current partial `use_in_context` proof beyond the tested seed-label -> planting follow-up flow.
3. Do not introduce new public enums such as `DocumentRoute` or `ResolutionMode` until runtime models actually adopt them.
4. Do not claim async jobs, discard semantics, or plant/leaf lab routes as implemented public contracts.

## 6. Best Next Moves

1. Treat [part-7-universal-capture-intake-contract.md](/Users/einstein/Documents/Codex/Semantic%20farming/docs/implementation/ai-capture-assist/part-7-universal-capture-intake-contract.md) as the current intake authority.
2. Move Farman Lite client handover and integration guidance toward `/v1/intake/*` where orchestration is desired.
3. Promote shadow routes only when each route has:
   - route-specific commit adapters,
   - contract tests,
   - capability wiring,
   - clear evidence-binding semantics.
