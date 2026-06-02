# Spec Part 7: Universal Capture Intake Contract (Backend)

Version: 0.1 (draft)  
Date: 2026-03-13  
Applies to: OF Platform / Farm_RM backend + Farman Lite iOS universal scanner clients

This part is the current backend authority for session-based, document-first intake. Product-facing discussions may still say "universal scanner," but the canonical backend term in this repo is **universal capture intake**.

When older AI-capture pages differ on intake orchestration, route naming, or persistence semantics, this Part 7 wins for those topics because it is reconciled to current runtime code, tests, route-registry data, and SQL.

## 0. Purpose

Define the current public backend contract for:

1. session-based capture intake,
2. route analysis over persisted document and parse provenance,
3. human review and field edits,
4. route-specific commit dispatch through existing authoritative adapters,
5. backlog boundaries for shadow or not-yet-proven route families.

Hard boundary:

- This part is document-first.
- It does not broaden current runtime support beyond what code, tests, route registry, and SQL already prove.
- It does not introduce new public enums or new canonical persistence families where repo-native contracts already exist.

## 1. Authority Order

For universal capture intake, use this precedence order:

1. Runtime implementation and tests in [main.py](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/app/main.py), [universal_capture.py](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/app/universal_capture.py), [test_api.py](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/tests/test_api.py), and [test_openapi_contract_alignment.py](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/tests/test_openapi_contract_alignment.py)
2. Public runtime models and checked-in OpenAPI for intake paths in [openapi-farm-rm.yaml](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/openapi-farm-rm.yaml)
3. Route and helper metadata in [universal_capture_route_registry.json](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/app/universal_capture_route_registry.json)
4. Persistence helpers and SQL schema in [persistence.py](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/app/persistence.py) and [0114_v1_7_universal_capture_intake.sql](/Users/einstein/Documents/Codex/Semantic%20farming/specs/v0.8/sql/migrations/0114_v1_7_universal_capture_intake.sql)
5. This Part 7

Normative evidence inputs for this part:

- Intake endpoints and models: [main.py](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/app/main.py)
- Intake analysis and route/helper selection logic: [universal_capture.py](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/app/universal_capture.py)
- Route registry and alias metadata: [universal_capture_route_registry.json](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/app/universal_capture_route_registry.json)
- Intake persistence helpers: [persistence.py](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/app/persistence.py)
- Intake SQL tables and append-only guards: [0114_v1_7_universal_capture_intake.sql](/Users/einstein/Documents/Codex/Semantic%20farming/specs/v0.8/sql/migrations/0114_v1_7_universal_capture_intake.sql)
- Public-path contract alignment: [test_openapi_contract_alignment.py](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/tests/test_openapi_contract_alignment.py)
- Route-flow behavior tests: [test_api.py](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/tests/test_api.py)
- Persistence-on smoke coverage across intake routes: [run-v0_8-db-smoke.sh](/Users/einstein/Documents/Codex/Semantic%20farming/specs/v1.0.0/qa/run-v0_8-db-smoke.sh)

## 2. Terminology Mapping

| Product or skeleton term | Current repo-native term | Notes |
|---|---|---|
| universal scanner | universal capture intake | Use "universal scanner" only as product-facing shorthand. |
| `CaptureSession` | `CaptureSession` | Already implemented as the public intake-session response model. |
| `DocumentRoute` | `routeId` plus `routeAliases` | The route registry is the canonical source of route identifiers and aliases. |
| `ResolutionMode` | not a public enum | Current behavior is expressed by `commitStrategy`, `targetForm`, session `status`, helper IDs, review gates, exact-match behavior, and optional `operationDraftFollowUp`. |
| `UniversalIntakeAnalyze` | `POST /v1/intake/analyze` | Already implemented; do not add a second analyze wrapper. |
| `EvidenceIngest` | document registry + parse-run provenance + capture envelope | Current intake depends on persisted `documentUri` and optional `parseRunUri`. |
| `DraftBootstrap` / `CommitAdapter` | route-specific existing endpoint adapter | Current commit dispatch is through the public intake commit route plus existing endpoint models and writers. |
| evidence-only fallback | `unknown.review` | Current fallback is manual review, not a generic public review-queue contract. |

## 3. Observed Current State

Observed current state:

1. Runtime already implements `GET /v1/intake/routes`, `POST /v1/intake/captures`, `POST /v1/intake/analyze`, `GET /v1/intake/sessions/{sessionId}`, `POST /v1/intake/sessions/{sessionId}/review`, and `POST /v1/intake/sessions/{sessionId}/commit`. Evidence: [main.py](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/app/main.py), [openapi-farm-rm.yaml](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/openapi-farm-rm.yaml), [test_openapi_contract_alignment.py](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/tests/test_openapi_contract_alignment.py)
2. Runtime already exposes the public intake models `CaptureEnvelopeCreateRequest`, `CaptureSession`, `IntakeAnalyzeRequest`, `IntakeSessionReviewRequest`, `IntakeSessionCommitRequest`, `IntakeSessionCommitResponse`, and `UniversalCaptureRouteRegistryResponse`. Evidence: [main.py](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/app/main.py), [test_openapi_contract_alignment.py](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/tests/test_openapi_contract_alignment.py)
3. Persistence already includes `intake_session`, `intake_session_revision`, and `intake_capture_envelope`, with links to `document_ingest_item` and `document_parse_run`. Evidence: [0114_v1_7_universal_capture_intake.sql](/Users/einstein/Documents/Codex/Semantic%20farming/specs/v0.8/sql/migrations/0114_v1_7_universal_capture_intake.sql), [persistence.py](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/app/persistence.py)
4. The route registry already defines enabled, shadow, catalog-only, alias, helper, review-gate, and commit-target metadata for multiple route families. Evidence: [universal_capture_route_registry.json](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/app/universal_capture_route_registry.json)
5. The currently proven enabled route set is broader than the downloaded skeleton assumed: `receipt.invoice`, `seed_label_or_tag`, `fertilizer_label`, `soil_analysis_report`, `fertilization_plan`, `delivery_note`, `seed_authorization_or_derogation`, `storage_lot_label`, and fallback `unknown.review`. Evidence: [universal_capture_route_registry.json](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/app/universal_capture_route_registry.json), [test_api.py](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/tests/test_api.py)
6. Commit support is route-specific and currently limited to the eight implemented commit routes above. Fallback review routes and shadow routes are not public commit adapters. Evidence: [main.py](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/app/main.py)
7. Partial "use in context" behavior is proven for `seed_label_or_tag` only: a successful seed-label intake commit may return `operationDraftFollowUp` for a planting draft when scoped field context is already present. Evidence: [main.py](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/app/main.py), [test_api.py](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/tests/test_api.py)

## 4. Evidence-Backed Inference

Evidence-backed inference:

1. The repo does not need a second `CaptureSession`, second analyze contract, or placeholder intake persistence family; those seams already exist in runtime.
2. The downloaded skeleton is useful as product framing and route/backlog source material, but not as the canonical transport contract.
3. The correct alignment move is to map the skeleton's `DocumentRoute` and `ResolutionMode` ideas onto current runtime `routeId`, `routeAliases`, `commitStrategy`, helper IDs, session status, and route-specific commit support.
4. `repoStatus` and runtime `availability` must stay separate. Some routes are runtime-enabled while still marked `planned`, `partial`, `unknown`, or `implemented-adjacent` in the route registry.

## 5. Recommended Working Assumption

Recommended working assumption:

1. Treat universal capture intake as an additive orchestration layer over document registry, OCR parse provenance, reference search, route analysis, review, and route-specific commit adapters.
2. Use `/v1/intake/*` as the canonical backend seam for scanner-style orchestration; keep `/v1/ai/ocr/parse` and direct route-specific write endpoints as lower-level building blocks.
3. Do not publish new public enums such as `DocumentRoute` or `ResolutionMode` unless runtime models first adopt them.
4. Keep shadow, catalog-only, and not-yet-proven behaviors in explicit backlog sections instead of presenting them as public runtime truth.

## 6. Canonical Runtime Surfaces

### 6.1 Intake endpoints

| Endpoint | Public model(s) | Current runtime role |
|---|---|---|
| `GET /v1/intake/routes` | `UniversalCaptureRouteRegistryResponse` | Returns route catalog, route aliases, and helper inventory, with runtime `availability` derived from route-required capability flags. |
| `POST /v1/intake/captures` | `CaptureEnvelopeCreateRequest` -> `CaptureSession` | Creates a new session or appends another capture to an existing session. Requires a persisted `documentUri` for the current farm scope and may carry an existing `parseRunUri`. |
| `POST /v1/intake/analyze` | `IntakeAnalyzeRequest` -> `CaptureSession` | Builds route candidates, selects a route and helper set, generates field proposals, evidence bindings, and a draft commit plan. |
| `GET /v1/intake/sessions/{sessionId}` | `CaptureSession` | Reloads the current session head. |
| `POST /v1/intake/sessions/{sessionId}/review` | `IntakeSessionReviewRequest` -> `CaptureSession` | Accepts route override, field edits, and review notes; updates payload draft, proposals, and review decisions. |
| `POST /v1/intake/sessions/{sessionId}/commit` | `IntakeSessionCommitRequest` -> `IntakeSessionCommitResponse` | Dispatches to a supported existing endpoint adapter, persists the commit result into the session, and may return `operationDraftFollowUp` for `seed_label_or_tag`. |

### 6.2 Supporting lower-level seams

Universal capture intake builds on these supporting surfaces instead of replacing them:

- OCR parse: [part-1-ocr-parse-contract.md](/Users/einstein/Documents/Codex/Semantic%20farming/docs/implementation/ai-capture-assist/part-1-ocr-parse-contract.md), [main.py](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/app/main.py)
- Capabilities: [main.py](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/app/main.py), [openapi-farm-rm.yaml](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/openapi-farm-rm.yaml)
- Document-backed parse and promotion routes: [main.py](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/app/main.py)
- Reference search and exact-match helpers: [main.py](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/app/main.py), [universal_capture.py](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/app/universal_capture.py)

## 7. Canonical Models And Capability Gates

Public intake models to anchor:

1. `CaptureEnvelopeCreateRequest`
2. `CaptureSession`
3. `IntakeAnalyzeRequest`
4. `IntakeSessionReviewRequest`
5. `IntakeSessionCommitRequest`
6. `IntakeSessionCommitResponse`
7. `UniversalCaptureRouteRegistryResponse`

Capability gates that materially affect intake behavior:

1. `documentRegistry`: master gate for universal capture intake and route fallback availability
2. `referenceSearch`: additional route gate for `seed_label_or_tag`
3. `soilLabResults`: additional route gate for `soil_analysis_report`
4. `fertiliserProductCompositions`: additional route gate for `fertilizer_label`
5. `fertilisationPlans`: additional route gate for `fertilization_plan`

Rules:

1. Runtime route `availability` is computed from the route registry plus the live capability state exposed by `/v1/capabilities`.
2. `repoStatus` is descriptive repo metadata and must not be flattened into the same field as runtime `availability`.
3. The `unknown.review` fallback stays enabled when intake itself is enabled, even when more specific routes are shadowed or unavailable.

## 8. Persistence And Revision Semantics

Current persistence semantics:

1. `intake_session` is the mutable head row for a session. It stores current status, selected route, latest revision pointer, current snapshot JSON, optional commit result JSON, timestamps, and actor.
2. `intake_session_revision` is append-only revision history. The SQL migration installs a trigger that blocks update and delete operations on revision rows.
3. `intake_capture_envelope` is append-only capture evidence metadata. It links a session to `document_ingest_item` and optional `document_parse_run`, and it also carries modality, source, locale, payload refs, derived refs, hints, and quality JSON.
4. The currently proven public status values are: `collecting`, `analyzing`, `awaiting_capture`, `awaiting_review`, `ready_to_commit`, `committed`, and `abandoned`.
5. Current runtime exposes create, analyze, review, read, and commit. It does **not** expose a public discard or delete endpoint, even though SQL already reserves the `abandoned` status.

## 9. Session Lifecycle

### 9.1 Create or append capture

1. `POST /v1/intake/captures` requires a farm-scoped persisted `documentUri`.
2. The caller may supply `sessionId` to append another capture to an existing session.
3. The caller may supply `parseRunUri`, but runtime also supports later analyze-time fallback to the latest parse for the capture's `documentUri`.
4. Committed sessions reject new captures.

### 9.2 Analyze

1. `POST /v1/intake/analyze` loads the scoped session and capture set.
2. Runtime analysis resolves parse runs from explicit `parseRunUri` first, then from the latest parse attached to `documentUri`.
3. Route selection, helper selection, exact-match behavior, field proposals, evidence bindings, blocking reasons, and payload drafting come from [universal_capture.py](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/app/universal_capture.py).

### 9.3 Review

1. `POST /v1/intake/sessions/{sessionId}/review` accepts `selectedRouteId`, field edits, and review notes.
2. Field edits update both the payload draft and the proposal set. Human edits become the highest-authority proposal layer for the touched field.
3. Review is the public seam for route override and human correction. It is not a new generic draft family.

### 9.4 Commit

1. `POST /v1/intake/sessions/{sessionId}/commit` supports only: `receipt.invoice`, `seed_label_or_tag`, `soil_analysis_report`, `fertilizer_label`, `fertilization_plan`, `delivery_note`, `seed_authorization_or_derogation`, and `storage_lot_label`.
2. Commit dispatches to existing endpoint models and writers. It does not introduce a generic intake write abstraction beneath those adapters.
3. `unknown.review` is manual-review-only and does not have a public commit adapter.

### 9.5 Partial "use in context" proof

The current repo proves only one limited "use in context" variant:

1. After a successful `seed_label_or_tag` commit, runtime may return `operationDraftFollowUp`.
2. The currently proven follow-up is a planting draft request when scoped field context is already present.
3. This is not a general cross-route `ResolutionMode` enum. It is a route-specific post-commit continuation.

## 10. Enabled Route Matrix

| `routeId` | Runtime availability | `repoStatus` | Commit target | Required capabilities | Current notes |
|---|---|---|---|---|---|
| `receipt.invoice` | `enabled` | `partial` | `/v1/inventory/receipts/import` | `documentRegistry` | Supports source-document plus supporting-label evidence. The enabled helper `receipt_plus_label_link` can enrich receipt line items with label-derived variety, status, and lot data. |
| `seed_label_or_tag` | `enabled` | `implemented-adjacent` | `/v1/inventory/material-lots` | `documentRegistry`, `referenceSearch` | Route-specific exact-match and reference-resolution behavior is implemented. Commit may return planting `operationDraftFollowUp` when scoped field context is already present. |
| `fertilizer_label` | `enabled` | `planned` | `/v1/fertiliser-product-compositions/import` | `documentRegistry`, `fertiliserProductCompositions` | Runtime supports current label-to-product-composition review and commit flow, but the route registry still marks the family as `planned`. Preserve both facts. |
| `soil_analysis_report` | `enabled` | `planned` | `/v1/soil-lab-results/import` | `documentRegistry`, `soilLabResults` | Runtime supports soil-lab session flow, field resolution, and exact lab partner resolution, while route metadata still marks the family as `planned`. |
| `fertilization_plan` | `enabled` | `implemented-adjacent` | `/v1/fertilisation-plans` | `documentRegistry`, `fertilisationPlans` | Runtime supports field and crop-instance resolution plus review-time fixups for plan windows and target nutrients. |
| `delivery_note` | `enabled` | `implemented-adjacent` | `/v1/commerce/delivery-tickets` | `documentRegistry` | Runtime can exact-resolve storage lot, commodity, and buyer only when evidence is uniquely sufficient; ambiguous matches stay in review. |
| `seed_authorization_or_derogation` | `enabled` | `unknown` | `/v1/compliance/seed-sourcing-exceptions` | `documentRegistry` | Canonical route alias target for `seed_authorisation_or_derogation`. Commit remains route-specific and requires scope anchors, decision status, reason classification, and attachment-evidence review. |
| `storage_lot_label` | `enabled` | `partial` | `/v1/warehouse/storage-lots/{storageLotUri:path}/attachment-evidence` | `documentRegistry` | Commit attaches evidence to an existing storage lot. Ambiguous lot-code matches remain review-only. |
| `unknown.review` | `enabled` | `runtime-fallback` | `manual.intake.review.v1` | `documentRegistry` | Current fallback for unsupported or ambiguous captures. Manual review only; no public commit adapter is defined. |

### 10.1 Enabled helper behavior

`receipt_plus_label_link` is the currently proven enabled helper:

1. It is advertised by `GET /v1/intake/routes`.
2. It is selected when a receipt capture and a supporting seed-label capture exist in the same session.
3. It enriches the receipt payload draft and evidence bindings without creating a second route family.

Evidence: [universal_capture_route_registry.json](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/app/universal_capture_route_registry.json), [universal_capture.py](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/app/universal_capture.py), [test_api.py](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/tests/test_api.py)

## 11. Mapping From The Downloaded Skeleton

### 11.1 Route-name mapping

| Downloaded skeleton term | Current runtime mapping | Status |
|---|---|---|
| `receipt.invoice` | `receipt.invoice` | Canonical and enabled |
| `seed_label.tag` | `seed_label_or_tag` | Canonical runtime name differs |
| `fertilizer_label` | `fertilizer_label` | Canonical and enabled |
| `ffs_label` | `ffs_label` | Present in route registry, `shadow`, `new_adapter_required` |
| `o10_fertilizer_log` | `o10_fertilizer_log` | Present in route registry, `shadow`, `new_adapter_required` |
| `o11_ffs_log` | `o11_ffs_log` | Present in route registry, `shadow`, `new_adapter_required` |
| `soil_analysis_report` | `soil_analysis_report` | Canonical and enabled |
| `plant_or_leaf_lab_analysis_report` | no current public runtime `routeId` proven | Backlog only |
| `fertilization_plan` | `fertilization_plan` | Canonical and enabled |
| `storage_lot_label` | `storage_lot_label` | Canonical and enabled |
| `unknown` | `unknown.review` | Canonical fallback route |

### 11.2 Alias mapping already implemented in runtime

Current route aliases already published by runtime:

1. `seed_authorisation_or_derogation` -> `seed_authorization_or_derogation`
2. `inspection_report` -> `inspection_or_noncompliance_doc`
3. `noncompliance_notice` -> `inspection_or_noncompliance_doc`

### 11.3 Resolution-mode mapping

| Downloaded skeleton `ResolutionMode` | Current runtime equivalent | Current boundary |
|---|---|---|
| `create_or_import` | commit-supported routes with `existing_endpoint_adapter` | Publicly proven for the eight commit-capable routes listed above |
| `enrich_draft` | review edits plus helper-driven `commitPlan.payloadDraft` enrichment | Publicly proven via `POST /review` and helper selection |
| `resolve_existing` | analyze-time exact-match behavior for storage lots, buyers, partners, fields, crop instances, and resources when uniquely sufficient | Proved only where tests exist; ambiguous matches stay review-only |
| `use_in_context` | route-specific follow-up continuation such as seed-label -> planting `operationDraftFollowUp` | Partial only; do not generalize across all routes |
| `evidence_only` | `unknown.review` fallback plus supporting evidence bindings | No generic public review-queue or deferred-job contract yet |

Rule:

- Do not publish `ResolutionMode` as a new canonical public enum unless runtime models first adopt it.

## 12. Backlog And Residual Gaps

| Backlog item | Current repo evidence | Current status |
|---|---|---|
| `ffs_label` | Route exists in the registry but remains `shadow` with `new_adapter_required` | Not a public commit-capable route |
| `o10_fertilizer_log` | Route exists in the registry but remains `shadow` with `new_adapter_required` | Not a public commit-capable route |
| `o11_ffs_log` | Route exists in the registry but remains `shadow` with `new_adapter_required` | Not a public commit-capable route |
| Async/background scanner jobs | Downloaded skeleton proposes them, but no public `/v1/intake/*` async job contract is implemented | Keep out of the current contract |
| Discard/delete semantics | SQL reserves `abandoned`, but runtime does not expose a public discard or delete route | Keep out of the current contract |
| Plant/leaf lab analysis report | Downloaded skeleton names it, but no public runtime `routeId`, tests, or commit adapter are proven | Keep in backlog only |
| Generic evidence-only review queue | `unknown.review` exists as a fallback route, but no shared public review-queue contract is proven here | Keep out of the current contract |
| Photo-recognition flows | Some photo-oriented routes appear in the route registry as shadow or catalog-only, but this Part 7 is document-first | Explicitly out of scope for the current intake contract |

## 13. Validation Evidence

The most important runtime validation anchors for this part are:

1. Intake OpenAPI/runtime path and schema alignment in [test_openapi_contract_alignment.py](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/tests/test_openapi_contract_alignment.py)
2. Route-registry exposure plus helper availability in [test_api.py](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/tests/test_api.py)
3. End-to-end session-flow tests for fertilizer label, seed label, storage lot label, delivery note, seed authorization, fertilization plan, receipt plus label, and soil analysis in [test_api.py](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/tests/test_api.py)
4. Persistence-on smoke coverage for intake sessions and revisions in [run-v0_8-db-smoke.sh](/Users/einstein/Documents/Codex/Semantic%20farming/specs/v1.0.0/qa/run-v0_8-db-smoke.sh)

Refresh rule:

- If runtime intake paths, intake models, route-registry metadata, capability gates, or SQL status semantics change, update this Part 7 in the same batch where practical.
