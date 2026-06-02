# Spec Part 4: Agronomy Season Windows (Backend Knowledge Pack)

Version: 0.1 (draft)  
Date: 2026-03-01  
Endpoint: `GET /v1/agronomy/season-windows`

## 0. Scope

Define a deterministic, versioned “season windows” service that returns crop-level timing priors (at minimum: planting + harvest windows) for a given crop and location.

Primary use:

- iOS uses these windows as **priors** for operation suggestion ranking.

This service is **not** a crop growth simulator. It is a stable, auditable knowledge pack.

## 1. Goals / Non-goals

### 1.1 Goals

1. Deterministic, cacheable results for crop + location.
2. Versioned dataset semantics (ability to pin a dataset version).
3. Canonical window representation + derived convenience forms.
4. EU-first (Slovenia + Serbia initially) with a clear fallback strategy.

### 1.2 Non-goals (v1)

1. Predicting actual phenology for a specific season (no GDD/real-time weather).
2. Variety-specific windows (allowed later as modifiers).
3. Returning “what to do” recommendations (clients compute ranking).

## 2. Data Model (Normative)

### 2.1 Window Types

v1 window codes:

- `planting`
- `harvest`

Future extensions may add:

- `emergence`, `flowering`, `maturity`, `cover_crop_sow`, etc.

### 2.2 Canonical Representation: Dekads

Canonical representation is **dekad-based**, using 36 dekads per year.

- Dekad 1: days 1–10
- Dekad 2: days 11–20
- Dekad 3: days 21–end of month
- …
- Dekad 36: late December

Window fields:

- `startDekad` (int 1..36)
- `endDekad` (int 1..36)
- `wrapsYear` (bool)

Derived convenience fields (computed deterministically):

- `startDayOfYear` (int 1..366)
- `endDayOfYear` (int 1..366)
- `dayOfYearRanges[]` (array of `{start,end}`) for wrap-year windows

### 2.3 Dataset Identity

Every response MUST include dataset identity:

- `datasetUri` (string)
- `datasetVersion` (string)
- `publishedAt` (ISO date)
- `sources[]` (array of `{sourceSystem, sourceRef, licenseHint}`) (best effort)

## 3. Region Identity (Normative)

The season windows dataset is indexed by a region identity.

The service MUST support:

1. `lat` + `lon` → `regionId` mapping (primary).
2. An optional `regionId` override for callers that already know it.

Response MUST include:

- `regionId` (string)
- `regionKind` (enum): `admin|grid|country_fallback|unknown`
- `regionMethod` (string): implementation detail (e.g., `iso3166-2`, `gaul1`, `grid_0.1deg`)
- `regionConfidence` (number 0..1)

Fallback rule (normative):

- If exact region mapping is unavailable, return a country-level fallback windows set (if available) and set `regionKind="country_fallback"`.
- If no data exists at all, return HTTP 404 with a clear error code.

## 4. API Contract (Normative)

### 4.1 `GET /v1/agronomy/season-windows`

Query params:

- `cropUri` (required, string)
- `lat` (required unless `regionId` provided, number)
- `lon` (required unless `regionId` provided, number)
- `regionId` (optional, string)
- `jurisdiction` (optional, string): `SI|RS|EU|…` (used only for fallback selection rules)
- `datasetVersion` (optional, string): if provided, pin to this version; else use latest.

Response (example):

```json
{
  "cropUri": "https://data.farmco.si/farm-rm/v1/crop-species/EU/ZEAMA",
  "jurisdiction": "SI",
  "location": {"lat": 46.05, "lon": 14.51},
  "region": {
    "regionId": "SI-061",
    "regionKind": "admin",
    "regionMethod": "iso3166-2/admin1",
    "regionConfidence": 0.88
  },
  "dataset": {
    "datasetUri": "https://data.farm-rm.org/agronomy/season-windows/v1",
    "datasetVersion": "eu-asap-2018.1+sl-rs-curation-2026-03",
    "publishedAt": "2026-03-01",
    "sources": [
      {"sourceSystem": "JRC_ASAP", "sourceRef": "…", "licenseHint": "see dataset"},
      {"sourceSystem": "FAO", "sourceRef": "…", "licenseHint": "see dataset"}
    ]
  },
  "windows": [
    {
      "windowCode": "planting",
      "startDekad": 9,
      "endDekad": 12,
      "wrapsYear": false,
      "startDayOfYear": 61,
      "endDayOfYear": 120,
      "dayOfYearRanges": [{"start": 61, "end": 120}]
    },
    {
      "windowCode": "harvest",
      "startDekad": 26,
      "endDekad": 30,
      "wrapsYear": false,
      "startDayOfYear": 214,
      "endDayOfYear": 304,
      "dayOfYearRanges": [{"start": 214, "end": 304}]
    }
  ]
}
```

### 4.2 Caching (Normative)

The endpoint MUST be cacheable:

- `Cache-Control: public, max-age=86400` (recommended default)
- `ETag` based on `(datasetVersion, cropUri, regionId)`

If `datasetVersion` is pinned, caching can be longer (e.g., 30 days).

### 4.3 Determinism (Normative)

For the same inputs and pinned `datasetVersion`, the service MUST return the same response (including ordering of `windows[]`).

## 5. Optional Derived Features (Non-normative, v1.1+)

An optional endpoint may provide derived features for operation ranking:

- `GET /v1/agronomy/season-features?cropUri=…&lat=…&lon=…&date=YYYY-MM-DD`

Possible features:

- `inPlantingWindow` / `inHarvestWindow`
- `daysIntoWindow` / `daysToWindowStart`
- `windowProgressPct`

These are deterministic transforms of season windows plus a date input.

## 6. Error Handling (Normative)

- `400` missing `cropUri` or missing location info
- `422` invalid lat/lon range or invalid URI
- `404` no season windows available for crop + region (or fallback)

Error response shape uses Farm_RM standard:

```json
{"code":"no_season_windows", "message":"No season windows available for this crop/location.", "details":["cropUri=…","regionId=…"]}
```

## 7. Acceptance Criteria (Testable)

1. For a known crop + location, the endpoint returns planting + harvest windows.
2. Responses include dataset identity and region identity metadata.
3. Pinning `datasetVersion` makes responses stable and cacheable.
4. Wrap-year windows return `dayOfYearRanges[]` split correctly.

## 8. Dependencies

- Part 3 reference: `cropUri` must resolve to a known crop/species.
- A curated season windows dataset must exist and be packaged with Farm_RM (file or DB-backed).

## 9. Next Part

Part 5: iOS integration (flows, offline queue, UX rules): [part-5-ios-integration.md](/Users/einstein/Documents/Codex/Semantic%20farming/docs/implementation/ai-capture-assist/part-5-ios-integration.md)

