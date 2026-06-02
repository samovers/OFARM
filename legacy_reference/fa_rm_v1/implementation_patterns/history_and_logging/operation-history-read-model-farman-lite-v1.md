# Field Operation History Read Model for Farman Lite v1

## Goal
- Give Farman Lite one exact backend read contract for committed field-operation history so the app can render real historical activity without inferring it from write endpoints or local draft storage.

## Capability Gate
- `fieldOperationHistory`
- If `GET /v1/capabilities` reports `features.fieldOperationHistory.enabled=false`, keep the existing local-only draft experience and do not call the read model.
- Respect `features.fieldOperationHistory.minClientVersion` when the backend sets it.

## Farm Scope
- Farm scope uses the same tenancy rules as the rest of `/v1`.
- In local and smoke environments, send `X-Farm-URI`.
- In auth-enabled environments, keep the existing bearer token plus farm-scope header behavior.
- The endpoint resolves the field against the authenticated farm scope and returns `404 field_not_found` when the field does not belong to that scope.

## Backend Contract
- Endpoint: `GET /v1/fields/{fieldUri}/operation-history`
- Query parameters:
  - `periodStart` optional ISO date
  - `periodEnd` optional ISO date
- Response contract: `FieldOperationHistoryListResponse`
- Response shape:
  - `fieldUri`
  - `periodStart`
  - `periodEnd`
  - `total`
  - `items[]`

## Item Fields
- `executedOperationUri`: canonical committed operation URI
- `fieldUri`: canonical field URI
- `cropInstanceUri`: crop instance linked to the committed operation when present
- `seasonCode`: crop season code when crop context exists
- `cropTypeUri`: crop species URI when crop context exists
- `productionStatus`: production status from the crop instance when present
- `status`: committed operation status from `executed_operation`
- `startedAt`: operation start timestamp
- `endedAt`: operation end timestamp
- `operationFamilyCode`: backend-normalized family code
- `operationTypeUri`: canonical operation type URI
- `operationTypeDerivation`: `planned_template`, `extension_inference`, or `unknown`
- `commitRoute`: authoritative event-specific write route for that family
- `eventUri`: concrete event record URI when the execution has an event extension row
- `actualQuantity`: committed quantity value when present
- `unit`: committed unit when present
- `materialLotUri`: first linked material lot URI for backward-compatible primary display
- `materialLotUris[]`: all linked material lot URIs
- `evidenceUris[]`: all linked evidence URIs

## Ordering And Semantics
- Items are returned newest first by committed operation start time.
- This is a read model over canonical committed operations, not over local drafts.
- `commitRoute` is informational for client routing, labels, and future deep links. The client should not replay a write blindly from this value.
- `operationFamilyCode` can currently resolve to:
  - `planting`
  - `tillage`
  - `mechanical_weeding`
  - `cover_crop_management`
  - `fertilizer_application`
  - `harvest`
  - `input_use`
  - `plant_protection_application`
  - `pesticide_application`
  - `irrigation`
  - `unknown`

## Error Handling
- `503 feature_disabled`: backend gate is off
- `404 field_not_found`: field is absent or outside the active farm scope
- `422 invalid_field_uri`: empty path field URI
- `422 invalid_date`: malformed `periodStart` or `periodEnd`
- `422 invalid_date_range`: `periodEnd < periodStart`

## Client Integration Rules
- Treat this endpoint as the source of truth for committed historical operations.
- Keep `DraftOperationStore` only for local unsynced drafts, review state, and in-progress authoring.
- Do not try to synthesize committed history from the field passport `recentEvents` surface. That surface is action-evaluation driven and can remain empty while committed operations exist.
- Do not treat a field-URI probe result of `invalid_crop_instance_uri` as a missing field. In current backend and current iOS source, that means the field resolves and only the synthetic probe crop instance is invalid.

## Recommended iOS Handoff
1. Add a capability check for `fieldOperationHistory`.
2. Add one API client method: `GET /v1/fields/{fieldUri}/operation-history`.
3. Introduce one remote model that mirrors `FieldOperationHistoryItem`.
4. In the Operations screen or field detail timeline, render remote committed history separately from local pending drafts.
5. Keep local draft actions and server history rows visually distinct. Pending local drafts should not pretend to be committed backend rows.
6. If the capability is disabled, fall back to the current local-only draft view without error noise.

## Suggested iOS Screen Behavior
- Section 1: `Pending drafts` from local storage
- Section 2: `Completed field history` from the backend read model
- Primary title:
  - derive from `operationFamilyCode`
- Secondary text:
  - prefer crop season or crop context, then quantity and unit, then `startedAt`
- Optional detail chips:
  - `productionStatus`
  - `status`
  - lot count from `materialLotUris`
  - evidence count from `evidenceUris`

## RealFarm Local Smoke Values
- Recommended hub base URL for local iOS smoke:
  - `http://localhost:8091`
- Current hub routing truth:
  - `GET /api/status` now exposes the active profile, routed backend URL, routed database, and routed default farm URI.
  - `GET /api/profiles` now exposes the canonical `defaultFarmUri` for each known local profile.
  - In the current RealFarm local setup, the hub routes to active profile `realfarm`, backend `http://127.0.0.1:18081`, database `farm_rm_profile_realfarm`, and farm `https://data.example/farm-rm/v1/farm/SI/REALFARM-001`.
  - The hub now owns local proxied profile/farm routing, so stale incoming `X-Farman-Profile` or `X-Farm-URI` values do not override the active local profile on `:8091`.
- Direct backend base URLs:
  - default backend: `http://localhost:8080`
  - managed RealFarm profile backend: `http://localhost:18081`
- Farm URI:
  - `https://data.example/farm-rm/v1/farm/SI/REALFARM-001`
- Example field URI:
  - `https://data.example/farm-rm/v1/field/SI/GERK-3544798`
- Example request:
  - `GET /v1/fields/https%3A%2F%2Fdata.example%2Ffarm-rm%2Fv1%2Ffield%2FSI%2FGERK-3544798/operation-history?periodStart=2024-01-01&periodEnd=2026-03-12`
- Current expected local result for that field through both the hub and the RealFarm profile backend:
  - `total=14`
  - completed oats, catch-crop, buckwheat, and spelt-related operations are present

## Migration Boundary
- This read model does not replace `/v1/field-ops/*`.
- New logging flows should keep using the authoritative event-specific write routes.
- Farman Lite should read historical committed operations from this contract and write new operations through the existing event-specific surfaces already in use by the backend.
- If diagnostics and backend responses disagree, check the hub routing block first to confirm which backend, database, and farm scope the active local profile owns.
