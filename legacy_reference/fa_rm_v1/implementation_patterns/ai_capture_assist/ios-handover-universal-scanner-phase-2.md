# iOS Handover: Universal Scanner Phase 2

Version: 0.1 (handover)
Date: 2026-03-13
Applies to: Farman Lite iOS client + OF Platform / Farm_RM backend

This handover defines the current Phase 2 implementation contract for the Farman Lite iOS universal scanner. Product-facing language may still say "universal scanner," but the backend seam it uses is the runtime **universal capture intake** contract under `/v1/intake/*`.

This document is a standalone product-plus-engineering handoff. It is not a new backend contract, not a wireframe spec, and not an attempt to supersede the runtime-backed contracts already documented in [part-7-universal-capture-intake-contract.md](/Users/einstein/Documents/Codex/Semantic%20farming/docs/implementation/ai-capture-assist/part-7-universal-capture-intake-contract.md) and [part-5-ios-integration.md](/Users/einstein/Documents/Codex/Semantic%20farming/docs/implementation/ai-capture-assist/part-5-ios-integration.md).

## 0. Purpose

Define how Farman Lite iOS should implement a single "Scan anything" entry point that:

1. captures document evidence locally and safely,
2. registers that evidence with the document registry,
3. runs OCR and barcode extraction on device,
4. uses OCR parse as a lower-level dependency when needed,
5. orchestrates review and commit through universal capture intake,
6. supports offline save, resume, and retry without inventing unsupported backend behavior.

Hard boundaries:

- Main-body route coverage in this handover is limited to runtime-proven routes.
- Shadow or future routes stay in a backlog appendix.
- Photo-recognition flows for crop, pest, or leaf diagnosis are out of scope.
- The client must not invent route support, exact-match semantics, or commit adapters that runtime does not expose.

## 1. Authority And Runtime Baseline

### 1.1 Authority order

For this iOS handover, use this precedence order:

1. Runtime implementation and tests in [main.py](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/app/main.py), [test_api.py](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/tests/test_api.py), and [test_openapi_contract_alignment.py](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/tests/test_openapi_contract_alignment.py)
2. Route metadata in [universal_capture_route_registry.json](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/app/universal_capture_route_registry.json)
3. Backend handover authority in [part-7-universal-capture-intake-contract.md](/Users/einstein/Documents/Codex/Semantic%20farming/docs/implementation/ai-capture-assist/part-7-universal-capture-intake-contract.md)
4. iOS integration baseline in [part-5-ios-integration.md](/Users/einstein/Documents/Codex/Semantic%20farming/docs/implementation/ai-capture-assist/part-5-ios-integration.md)
5. This document

If this handover conflicts with runtime code, tests, route registry, or Part 7, the repo-backed runtime contract wins.

### 1.2 Observed current state

Observed current state:

1. Runtime already exposes `GET /v1/capabilities`, `GET /v1/intake/routes`, `POST /v1/documents/ingest`, `POST /v1/intake/captures`, `POST /v1/intake/analyze`, `GET /v1/intake/sessions/{sessionId}`, `POST /v1/intake/sessions/{sessionId}/review`, and `POST /v1/intake/sessions/{sessionId}/commit`. Evidence: [main.py](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/app/main.py), [test_openapi_contract_alignment.py](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/tests/test_openapi_contract_alignment.py)
2. `POST /v1/intake/captures` requires a persisted `documentUri` for the current farm scope, so iOS cannot treat evidence registration as optional. Evidence: [main.py](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/app/main.py)
3. OCR parse persists a `document_parse_run` only when `POST /v1/ai/ocr/parse` is called with a `documentUri`, and `POST /v1/intake/analyze` then resolves parse runs from explicit `parseRunUri` or the latest parse attached to that document. Evidence: [main.py](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/app/main.py), [part-1-ocr-parse-contract.md](/Users/einstein/Documents/Codex/Semantic%20farming/docs/implementation/ai-capture-assist/part-1-ocr-parse-contract.md)
4. Current runtime-proven scanner routes are `receipt.invoice`, `seed_label_or_tag`, `fertilizer_label`, `soil_analysis_report`, `fertilization_plan`, `delivery_note`, `seed_authorization_or_derogation`, `storage_lot_label`, and fallback `unknown.review`. Evidence: [universal_capture_route_registry.json](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/app/universal_capture_route_registry.json), [test_api.py](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/tests/test_api.py)
5. The helper `receipt_plus_label_link` is runtime-enabled and enriches receipt sessions when a supporting seed label exists in the same session. Evidence: [universal_capture_route_registry.json](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/app/universal_capture_route_registry.json), [test_api.py](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/tests/test_api.py)
6. The only currently proven "use in context" follow-up is `operationDraftFollowUp` after a successful `seed_label_or_tag` commit. Evidence: [main.py](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/app/main.py), [test_api.py](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/tests/test_api.py)
7. Runtime does not currently expose a public async intake job contract or a public discard/delete contract for intake sessions. Evidence: [part-7-universal-capture-intake-contract.md](/Users/einstein/Documents/Codex/Semantic%20farming/docs/implementation/ai-capture-assist/part-7-universal-capture-intake-contract.md)

### 1.3 Recommended working assumption

Recommended working assumption:

1. The default scanner orchestration seam is document ingest plus universal capture intake, not direct route-specific persistence.
2. `POST /v1/ai/ocr/parse` remains a lower-level dependency that normally produces the parse run universal capture intake needs, but it is not the session orchestration surface.
3. Client route support is dynamic and comes from runtime capabilities plus route-registry `availability`, not from hardcoded enums.
4. Any client-side route or state enums are presentation-only derived values, not canonical backend symbols.

## 2. Product Contract And Hard Boundaries

### 2.1 Working product contract

> Scan supported evidence, preserve proof early, prefill the correct review state, and only commit through runtime-supported routes after review.

### 2.2 Hard constraints for iOS

1. Primary CTA remains **Scan anything**.
2. The flow is document-first. Universal scanner covers supported document evidence, not plant or symptom recognition.
3. Evidence must be retained locally before network work starts.
4. The first required network persistence step is document registration, not route-specific commit.
5. The client must not silently mutate committed backend truth.
6. Unsupported or shadowed routes degrade to `unknown.review` or to explicit lower-level manual flows, not to invented auto-commit logic.
7. Async in this handover means client-side continuation, local queueing, resume, and notifications only.
8. Local abandonment is allowed; backend discard or delete is not part of the public scanner contract today.

## 3. Canonical Scanner Network Flow

### 3.1 Required orchestration flow

The scanner should build around this runtime-backed flow:

1. `GET /v1/capabilities`
2. `GET /v1/intake/routes`
3. `POST /v1/documents/ingest`
4. `POST /v1/intake/captures`
5. `POST /v1/intake/analyze`
6. `GET /v1/intake/sessions/{sessionId}`
7. `POST /v1/intake/sessions/{sessionId}/review`
8. `POST /v1/intake/sessions/{sessionId}/commit`

Rule:

- Treat `POST /v1/ai/ocr/parse` and direct route-specific write endpoints as lower-level building blocks, not as the default scanner orchestration seam.

### 3.2 Current parse dependency

The scanner still needs OCR parse in the current runtime:

1. iOS runs OCR and barcode extraction on device first.
2. iOS SHOULD call `POST /v1/ai/ocr/parse` with the persisted `documentUri` before `POST /v1/intake/analyze`, so analyze can use either:
   - the explicit `parseRunUri`, or
   - the latest persisted parse for the document.
3. iOS MAY create the intake capture before parse completes, but SHOULD NOT expect meaningful route analysis until a parse run exists or the user intentionally accepts fallback review behavior.

Evidence: [main.py](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/app/main.py), [part-1-ocr-parse-contract.md](/Users/einstein/Documents/Codex/Semantic%20farming/docs/implementation/ai-capture-assist/part-1-ocr-parse-contract.md)

### 3.3 Save-evidence-early rule

"Save evidence early" means:

1. retain the local asset immediately in client storage,
2. register the document through `POST /v1/documents/ingest` as soon as the scanner can provide evidence identity and capture metadata,
3. use the returned `documentUri` for downstream parse and intake calls.

`POST /v1/documents/ingest` requires:

- `farmUri`
- `source`
- `sourceRef`
- `documentHint`
- either `evidenceUri` or `evidenceType + evidenceRef`

Recommended extras when available:

- `fileName`
- `mimeType`
- `capturedAt`
- `sha256`
- `idempotencyKey`

`sourceRef` must stay stable for the same local capture so retries resolve the same document rather than creating duplicates.

Evidence: [main.py](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/app/main.py), [test_api.py](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/tests/test_api.py)

## 4. Scanner-Facing Runtime Contracts

### 4.1 Backend models iOS should anchor to

Use these repo-native request/response models as the scanner-facing contract anchors:

- `DocumentIngestRequest`
- `DocumentIngestResponse`
- `CaptureEnvelopeCreateRequest`
- `CaptureSession`
- `IntakeAnalyzeRequest`
- `IntakeSessionReviewRequest`
- `IntakeSessionCommitRequest`
- `IntakeSessionCommitResponse`
- `UniversalCaptureRouteRegistryResponse`
- `OcrParseRequest`
- `OcrParseResponse`

Do not introduce parallel client-facing backend concepts for route selection or resolution when these transport models already exist.

### 4.2 Fields iOS should read from runtime

The client should treat these `CaptureSession` fields as the canonical session state:

- `sessionId`
- `status`
- `selectedRouteId`
- `selectedHelperIds`
- `captures`
- `routeCandidates`
- `fieldProposals`
- `evidenceBindings`
- `reviewDecisions`
- `commitPlan`
- `analysisSummary`
- `commitResult`

The client should treat these route-registry fields as the canonical route catalog:

- `routeId`
- `availability`
- `requiredCapabilities`
- `targetForm`
- `commitStrategy`
- `humanReviewGates`
- `aliasRouteIds`
- `documentHints`
- `expectedDocumentTypes`

Client policy:

- use `availability` for actual UI enablement,
- treat `repoStatus` as descriptive only,
- never let a local enum override runtime route availability.

## 5. Recommended Client Architecture

No Farman Lite iOS source tree is present in this repo, so the module names below are recommended ownership boundaries rather than existing code symbols.

Recommended boundaries:

| Module | Responsibility |
|---|---|
| `UniversalScannerCoordinator` | Own scanner flow, launch context, and resume behavior |
| `CapabilityRegistry` | Cache `/v1/capabilities` and min-client-version metadata |
| `RouteCatalogStore` | Cache `/v1/intake/routes` and expose runtime route availability |
| `DocumentRegistryClient` | Own `POST /v1/documents/ingest` and document reload |
| `OCRPipeline` | Run on-device OCR and normalize line geometry payloads |
| `BarcodePipeline` | Extract and dedupe barcode/QR values |
| `CaptureSessionStore` | Persist local session state and queued jobs |
| `IntakeClient` | Call `/v1/intake/*` endpoints and map results into local state |
| `ReviewComposer` | Build the compact review summary from proposals and commit plan |
| `ResumeCoordinator` | Recover interrupted sessions and notification-driven resume |

Rules:

- Camera and OCR logic should not live in view code.
- Route and review logic should not be spread across per-screen files.
- Networking should not invent UX state that is already represented by `CaptureSession.status`.

## 6. Local Client Models

### 6.1 Required local models

These are client-owned models, but they should mirror repo-native transport shapes rather than redefine them:

| Local model | Purpose | Remote mirror or source |
|---|---|---|
| `ScannerLaunchContext` | Scanner entry context and inherited anchors | local only |
| `CaptureSessionLocal` | Local session head and queue state | `CaptureSession` |
| `CaptureEnvelopeLocal` | Local capture metadata and asset refs | `CaptureEnvelope` |
| `QueuedDocumentIngestJob` | Retryable document-registry work | `DocumentIngestRequest` |
| `QueuedIntakeJob` | Retryable intake create/analyze/review/commit work | `CaptureEnvelopeCreateRequest`, `IntakeAnalyzeRequest`, `IntakeSessionReviewRequest`, `IntakeSessionCommitRequest` |
| `ReviewFieldEditLocal` | Review edits prior to submit | `IntakeReviewFieldEdit` |
| `CapabilitySnapshotLocal` | Cached feature gates and min versions | `CapabilitiesResponse` |
| `RouteCatalogSnapshotLocal` | Cached route and helper registry | `UniversalCaptureRouteRegistryResponse` |

### 6.2 Presentation-only derived values

If the iOS client wants local enums for UI rendering, they must be presentation-only derived values:

- route display keys derived from runtime `selectedRouteId` and `routeCandidates`
- scanner-state display keys derived from local sync state plus runtime `status`

Do not make local enums the source of truth for backend route identity, commit behavior, or existing-match semantics.

## 7. State Machine And Lifecycle

### 7.1 Local lifecycle states

The scanner should model the lifecycle around actual backend and queue milestones:

1. `local_only`
2. `document_registered`
3. `capture_created`
4. `analyzing`
5. `awaiting_review`
6. `ready_to_commit`
7. `committed`
8. `sync_failed`
9. `abandoned_local`

### 7.2 Transition rules

1. `local_only` -> `document_registered` after successful `POST /v1/documents/ingest`
2. `document_registered` -> `capture_created` after successful `POST /v1/intake/captures`
3. `capture_created` -> `analyzing` when parse dependency and analyze call are in flight
4. `analyzing` -> `awaiting_review` or `ready_to_commit` from returned `CaptureSession.status`
5. `ready_to_commit` -> `committed` after successful `POST /v1/intake/sessions/{sessionId}/commit`
6. Any network step can move to `sync_failed` with resumable local state retained
7. Only local state may move to `abandoned_local`; no backend discard route is defined in this contract

Rule:

- Route choice is not a separate client state machine. It comes from `selectedRouteId`, `routeCandidates`, `selectedHelperIds`, review edits, and `commitPlan.blockingReasonCodes`.

## 8. Capture Payload Composition

### 8.1 Mandatory fields for the scanner happy path

The scanner should treat these fields as mandatory for the document-ingest plus intake happy path:

- `farmUri`
- `source`
- `sourceRef`
- `documentHint`
- local image or file metadata for `/v1/documents/ingest`
- `documentUri` before `/v1/intake/captures`
- `payloadRef.kind`
- `payloadRef.id`
- `payloadRef.mimeType`
- `createdAt`
- `locale`
- `modality`
- `quality.adequate`
- `quality.issues`

When present, also send:

- `derivedRefs.barcodeValues`
- `hints.contextRefs.fieldUri`
- `hints.contextRefs.cropInstanceUri`
- `hints.contextRefs.fromStorageLotUri`
- `hints.contextRefs.buyerRef`
- `hints.contextRefs.commodityRef`
- `hints.intentHint`
- `hints.routeHint`

### 8.2 OCR payload alignment

The OCR layer should align to the current parse request shape rather than inventing a mobile-specific schema:

- `ocrText`
- `ocrLines[].text`
- `ocrLines[].confidence`
- `ocrLines[].geometry.coordinateOrigin`
- `ocrLines[].geometry.normalized`
- `ocrLines[].geometry.boundingBox`
- optional `image`
- optional `context.jurisdiction`
- optional `context.currencyHint`

Barcode and QR values should be passed through intake as `derivedRefs.barcodeValues`, not hidden in free text.

### 8.3 Hint semantics

Client hint rules:

1. `documentHint`, `intentHint`, and `routeHint` are hints only.
2. `contextRefs` are strong scope anchors when the scanner is launched from known field, crop, storage-lot, buyer, or commodity context.
3. The client must not treat its own hints as authoritative over runtime analysis.

## 9. Capability Gating

### 9.1 Required gates

Before exposing route-specific affordances, iOS must read and cache:

- `documentRegistry`
- `referenceSearch`
- `soilLabResults`
- `fertiliserProductCompositions`
- `fertilisationPlans`
- any `minClientVersion` returned for those features

### 9.2 Client policy

1. The universal scanner entry remains visible.
2. `documentRegistry` is the master gate for document ingest and universal capture intake.
3. Route support is dynamic and comes from route-registry `availability` plus capabilities.
4. Unsupported or shadowed route families degrade to `unknown.review` or explicit manual lower-level fallback.
5. The client must not expose commit actions for route families whose runtime `availability` is not `enabled`.

Evidence: [main.py](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/app/main.py), [test_api.py](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/tests/test_api.py)

## 10. Runtime-Proven Route Coverage

### 10.1 Main-body route matrix

| `routeId` | Required capabilities | Current commit target | Current client note |
|---|---|---|---|
| `receipt.invoice` | `documentRegistry` | `/v1/inventory/receipts/import` | Primary receipt and invoice scanner path. Can combine source document and supporting label evidence. |
| `seed_label_or_tag` | `documentRegistry`, `referenceSearch` | `/v1/inventory/material-lots` | Label-driven lot capture. Can return `operationDraftFollowUp` after commit. |
| `fertilizer_label` | `documentRegistry`, `fertiliserProductCompositions` | `/v1/fertiliser-product-compositions/import` | Product-composition review and commit flow, gated by fertiliser composition capability. |
| `soil_analysis_report` | `documentRegistry`, `soilLabResults` | `/v1/soil-lab-results/import` | Soil report review and commit flow, including exact field or partner resolution where uniquely sufficient. |
| `fertilization_plan` | `documentRegistry`, `fertilisationPlans` | `/v1/fertilisation-plans` | Plan review and commit flow with field and crop-context resolution. |
| `delivery_note` | `documentRegistry` | `/v1/commerce/delivery-tickets` | Delivery-note and weigh-ticket flow. Exact storage-lot or buyer resolution stays conditional on unique evidence. |
| `seed_authorization_or_derogation` | `documentRegistry` | `/v1/compliance/seed-sourcing-exceptions` | Compliance document route for seed authorization or derogation review and commit. |
| `storage_lot_label` | `documentRegistry` | `/v1/warehouse/storage-lots/{storageLotUri:path}/attachment-evidence` | Evidence-attachment flow to an existing storage lot when exact resolution is sufficient. |
| `unknown.review` | `documentRegistry` | manual review only | Fallback for unsupported, ambiguous, or currently shadowed routes. No public commit adapter. |

### 10.2 Helper behavior

`receipt_plus_label_link` is the only currently proven helper behavior iOS should special-case in UX copy:

1. It is exposed by `GET /v1/intake/routes`.
2. It is selected when a receipt capture and a supporting seed-label capture are in the same session.
3. It enriches the receipt draft and evidence bindings; it does not create a new route family.

### 10.3 Existing-match and ambiguity policy

Current runtime-proven exact-resolution behavior is analyze-time and evidence-bound. The client should describe it as exact resolution or ambiguity handling surfaced in proposals and commit plans, not as a separate shared lookup API.

Proven exact-resolution domains include:

- storage lots
- buyers
- partners
- fields
- crop instances
- input-material resources

Client rule:

- when evidence is uniquely sufficient, the review flow may show resolved existing records;
- when evidence is ambiguous, the flow stays review-first and must not silently mutate committed truth.

## 11. Review, Commit, And Follow-Up

### 11.1 Review contract

Use `POST /v1/intake/sessions/{sessionId}/review` for:

- route override via `selectedRouteId`
- field edits via `fieldEdits[]`
- review notes

`fieldEdits` must update the rendered payload draft from `commitPlan.payloadDraft`, not just local UI state.

### 11.2 Commit contract

Use `POST /v1/intake/sessions/{sessionId}/commit` as the only scanner-level commit call.

Rules:

1. `payloadOverride` is optional and should be rare. The normal path is to review into a clean `commitPlan.payloadDraft`.
2. Invalid commit payloads are user-fixable review failures, not reasons to invent client-side route writes.
3. Committed sessions cannot accept new captures.

### 11.3 Proven "use in context" follow-up

Only one route-specific follow-up is currently proven:

1. After `seed_label_or_tag` commit, the response may include `operationDraftFollowUp`.
2. If `hints.contextRefs.fieldUri` was already present on the capture, the follow-up can be `ready_to_create`.
3. If field context is missing, the follow-up returns `needs_context`.
4. This is a route-specific continuation, not a generic route-resolution enum.

Evidence: [test_api.py](/Users/einstein/Documents/Codex/Semantic%20farming/specs/api/v1/server/fastapi/tests/test_api.py)

## 12. Offline, Resume, And Resilience

### 12.1 Offline-safe subset

The scanner must work locally without network for:

- image or document capture
- local asset retention
- on-device OCR
- barcode and QR extraction
- local session creation
- queueing document-ingest and intake work

### 12.2 Reconnect behavior

On reconnect, the preferred replay order is:

1. run queued document-ingest work,
2. run queued OCR parse work when needed,
3. create or append intake captures,
4. run analyze,
5. refresh review state,
6. notify the user when action is needed or the session is ready.

### 12.3 Async meaning in this handover

Async here means:

- local queueing,
- retries with backoff,
- resume from app relaunch,
- notification or inbox resume entry,
- interactive timeout fallback that never loses evidence.

It does not mean a public backend job API under `/v1/intake/*`.

## 13. Open Decisions

Keep these as explicit open decisions unless the Farman Lite iOS repo proves them later:

1. minimum iOS version
2. SwiftUI versus UIKit ownership split
3. exact notification or reminder strategy
4. scanner presentation chrome and camera-shell composition
5. local storage budget for unsynced captures
6. confidence display treatment in UI

## 14. Acceptance Test Plan

### 14.1 Startup and gating

1. capabilities fetch succeeds and caches `enabled` plus `minClientVersion`
2. route registry fetch succeeds and honors runtime `availability`
3. feature-disabled route families do not surface commit affordances

### 14.2 Happy-path scanner flows

1. receipt capture through document ingest, capture creation, analyze, review, and commit
2. seed-label capture through commit, including seed-quality follow-up fields
3. receipt plus supporting label in one session selects `receipt_plus_label_link`
4. soil analysis report commit
5. fertilizer label commit
6. fertilization plan commit
7. delivery note commit
8. seed authorization or derogation commit
9. storage-lot label attach-evidence commit

### 14.3 Review and ambiguity handling

1. `fieldEdits` update `commitPlan.payloadDraft`
2. invalid route override is rejected
3. ambiguous or disabled route falls back to `unknown.review`
4. blocking reasons remain visible until review fixes them
5. bad `payloadOverride` returns a user-fixable validation error

### 14.4 Context and follow-up behavior

1. seed-label commit without `fieldUri` returns `operationDraftFollowUp.status = needs_context`
2. seed-label commit with `hints.contextRefs.fieldUri` returns `ready_to_create`
3. committed sessions reject appended captures
4. farm-scope mismatch or invalid `documentUri` fails early

### 14.5 Offline and resume

1. local capture and OCR work without network
2. reconnect runs document ingest first, then intake creation and analyze
3. local resume restores the current `CaptureSessionLocal`
4. no evidence loss when analyze exceeds the interactive budget
5. no duplicate session promotion when queued work retries

## Appendix A - Backlog And Explicitly Out-Of-Scope Items

Keep these out of the main implementation contract until runtime proves them:

- `ffs_label`
- `o10_fertilizer_log`
- `o11_ffs_log`
- plant or leaf lab analysis report
- photo-recognition flows
- backend async job orchestration under `/v1/intake/*`
- backend discard or delete semantics for intake sessions
- any generic evidence-only review queue beyond `unknown.review`

## Appendix B - Relationship To Older iOS Notes

This handover is the current standalone universal-scanner implementation handoff.

Relationship to existing docs:

1. [part-5-ios-integration.md](/Users/einstein/Documents/Codex/Semantic%20farming/docs/implementation/ai-capture-assist/part-5-ios-integration.md) remains the UX and offline-first integration baseline.
2. [part-7-universal-capture-intake-contract.md](/Users/einstein/Documents/Codex/Semantic%20farming/docs/implementation/ai-capture-assist/part-7-universal-capture-intake-contract.md) remains the backend intake authority.
3. [ios-handover-ai-inventory-scan-si.md](/Users/einstein/Documents/Codex/Semantic%20farming/docs/implementation/ai-capture-assist/ios-handover-ai-inventory-scan-si.md) remains useful for SI inventory field and payload detail, but it is not the current scanner orchestration handover.
