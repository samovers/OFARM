# Spec Part 3: Crop/Variety Reference + Normalization (Backend)

Version: 0.2 (draft)  
Date: 2026-03-01  
Endpoints: `GET /v1/reference/snapshots`, `GET /v1/reference/sources`, `GET /v1/reference/source-profiles`, `GET /v1/reference/source-plan`, `POST /v1/reference/source-ingestion/check`, `GET /v1/reference/crops/search`, `GET /v1/reference/varieties/search`, `POST /v1/reference/snapshots/import`

## 0. Scope

Define a Farm_RM reference layer for:

1. **Crop/species** identity (stable URIs, multilingual labels, synonyms).
2. **Variety** identity within a crop/species (stable URIs, multilingual labels, synonyms, basic metadata).
3. Deterministic **search + ranking** so clients can normalize OCR tokens into stable URIs.

This spec intentionally avoids committing to a single upstream provider in v1; it requires that Farm_RM hosts a **local snapshot** with source attribution.

## 1. Goals / Non-goals

### 1.1 Goals

1. Provide stable internal URIs for crop/species and varieties.
2. Provide deterministic search endpoints (same query + dataset version → same ordering).
3. Support multilingual display labels (English + Slovenian at minimum).
4. Support synonyms/alternate labels for normalization (“koruza” ↔ “maize”).
5. Expose source attribution so reference decisions are auditable.

### 1.2 Non-goals (v1)

1. Full agronomic knowledge graph (traits, adaptation, risks). Those exist elsewhere in Farm_RM; this part only covers identity + lookup.
2. Real-time fetching from external registries at request time.
3. Forcing every input to match a reference term (clients must be allowed to choose “Unknown”).

## 2. Reference Object Model (Normative)

### 2.1 Crop/Species (`CropRef`)

Fields returned by the API:

- `uri` (string, required): stable Farm_RM URI.
- `code` (string, required): stable internal code (can mirror an external code).
- `label` (string, required): default display label.
- `labels` (object, optional): `{ "<lang>": "<text>" }` for requested/available languages.
- `synonyms` (array of strings, optional): common synonyms (tokenization-ready).
- `source` (object, optional):
  - `sourceSystem` (string): e.g., `EPPO`, `AGROVOC`, `FARM-RM`
  - `sourceId` (string): upstream identifier
  - `sourceVersion` (string): snapshot/version identifier

### 2.2 Variety (`VarietyRef`)

- `uri` (string, required)
- `cropUri` (string, required): references a `CropRef`.
- `code` (string, required): stable internal variety code.
- `label` (string, required)
- `labels` (object, optional)
- `synonyms` (array, optional)
- `breederName` (string, optional)
- `maturityGroup` (string, optional)
- `source` (object, optional)

## 3. Persistence Alignment (Normative)

This spec can be implemented using existing Farm_RM persistence primitives:

- `crop_species(uri, code, label, vocabulary_uri, …)`
- `variety(uri, crop_species_uri, code, label, breeder_name, maturity_group, …)`
- `localized_label(subject_uri, label_role, lang_tag, label_text, …)` for multilingual labels/synonyms

Normative mapping:

- `CropRef.uri` ↔ `crop_species.uri`
- `CropRef.code` ↔ `crop_species.code`
- `CropRef.label` ↔ `crop_species.label`
- `VarietyRef.uri` ↔ `variety.uri`
- `VarietyRef.cropUri` ↔ `variety.crop_species_uri`
- `VarietyRef.code` ↔ `variety.code`
- `VarietyRef.label` ↔ `variety.label`

Multilingual labels:

- `localized_label.subject_uri = crop_species.uri|variety.uri`
- `label_role`:
  - `pref` for primary labels
  - `alt` for synonyms/alternate spellings

Source attribution:

- v1 minimum: provide `source` via:
  - `crop_species.vocabulary_uri` when present, and/or
  - `localized_label.source_scheme_uri/source_ref` when present
- v1: use `reference_source_snapshot` + entry tables for explicit snapshot versioning and deterministic search.

## 4. Snapshot Catalog + Search Endpoints (Normative)

### 4.1 `GET /v1/reference/snapshots`

Purpose:

- let clients discover available snapshot versions before pinning `sourceVersion` in search requests.

Query params:

- `sourceSystem` (optional): filter snapshots by source (`EU_CATALOG`, `CPVO`, ...).
- `limit` (optional int, default 20, max 200).

Response:

```json
{
  "sourceSystem": "EU_CATALOG",
  "total": 2,
  "items": [
    {
      "snapshotUri": "urn:reference-source-snapshot:...",
      "sourceSystem": "EU_CATALOG",
      "sourceVersion": "snapshot-2026-03",
      "publishedAt": "2026-03-01",
      "importedAt": "2026-03-01T12:00:00Z",
      "cropCount": 1200,
      "varietyCount": 8300,
      "isLatest": true
    }
  ]
}
```

### 4.2 `GET /v1/reference/sources`

Purpose:

- let clients and operators discover which source systems are authoritative for crop/species vs variety data.

Query params:

- `entityType` (optional): `crop_species` or `variety` (alias `crop` accepted).
- `jurisdiction` (optional): jurisdiction filter (e.g., `SI`, `RS`, `EU`).
- `sourceSystem` (optional): exact source system filter.
- `includeSnapshotStatus` (optional bool): include latest imported snapshot metadata per source.
- `limit` (optional int, default 50, max 200).

Response:

```json
{
  "entityType": "variety",
  "jurisdiction": "RS",
  "sourceSystem": null,
  "snapshotStatusAvailable": true,
  "total": 2,
  "items": [
    {
      "sourceSystem": "EU_CATALOG",
      "label": "EU Common Catalogue",
      "entities": ["variety"],
      "jurisdictionScopes": ["EU", "SI", "RS"],
      "sourceRef": "https://food.ec.europa.eu/...",
      "sourceRefLabel": "EU plant variety catalogues and databases",
      "updateCadence": "annual",
      "ingestProfilePath": "specs/v0.8/reference-ingest/profiles/eu-catalog-2026.json",
      "recommendedForCrops": false,
      "recommendedForVarieties": true,
      "latestSnapshot": {
        "snapshotUri": "urn:reference-source-snapshot:...",
        "sourceSystem": "EU_CATALOG",
        "sourceVersion": "snapshot-2026-03",
        "importedAt": "2026-03-02T08:00:00Z",
        "cropCount": 1200,
        "varietyCount": 8300,
        "isLatest": true
      }
    }
  ]
}
```

### 4.3 `GET /v1/reference/source-plan`

Purpose:

- return deterministic ingestion priority order for a selected entity scope and jurisdiction.

Query params:

- `entityType` (required): `crop_species` or `variety` (alias `crop` accepted).
- `jurisdiction` (optional): jurisdiction code (`SI`, `RS`, `EU`, ...).
- `productionProfile` (optional): `organic`, `in_transition`, or `conventional` (default `organic`).
- `includeSnapshotStatus` (optional bool, default `true`): include latest imported snapshot for each plan step.
- `limit` (optional int, default 10, max 50).

Response:

```json
{
  "entityType": "variety",
  "jurisdiction": "RS",
  "productionProfile": "organic",
  "planVersion": "2026-03",
  "snapshotStatusAvailable": true,
  "total": 3,
  "steps": [
    {
      "order": 1,
      "sourceSystem": "RS_CATALOG",
      "label": "Serbia Variety Register",
      "selectionReason": "Serbian national variety list prioritized for Serbian compliance workflows.",
      "ingestProfilePath": null,
      "sourceRef": "https://www.minpolj.gov.rs/",
      "latestSnapshot": {
        "snapshotUri": "urn:reference-source-snapshot:...",
        "sourceSystem": "RS_CATALOG",
        "sourceVersion": "snapshot-2026-03",
        "importedAt": "2026-03-02T08:00:00Z",
        "cropCount": 0,
        "varietyCount": 1240,
        "isLatest": true
      }
    }
  ]
}
```

### 4.4 `GET /v1/reference/source-profiles`

Purpose:

- return profile metadata and required CSV schema for deterministic ingestion payload builds.

Query params:

- `sourceSystem` (optional): filter profile list by source system.
- `limit` (optional int, default 50, max 200).

Response:

```json
{
  "sourceSystem": "EPPO",
  "total": 1,
  "items": [
    {
      "profileCode": "eppo-2026",
      "sourceSystem": "EPPO",
      "profilePath": "specs/v0.8/reference-ingest/profiles/eppo-2026.json",
      "sourceRef": "https://gd.eppo.int/",
      "licenseHint": "Use and attribution must follow EPPO data terms",
      "recommendedRefreshCadence": "quarterly",
      "acquisition": {
        "entryPointUrl": "https://gd.eppo.int/",
        "requiresAuth": false,
        "authHint": null,
        "artifacts": [
          {
            "artifactCode": "eppo-crop-species-export",
            "entityType": "crop_species",
            "label": "EPPO crop/species taxonomy export",
            "accessUrl": "https://gd.eppo.int/",
            "format": "html+download",
            "requiresAuth": false,
            "note": "Primary source for crop/species URI normalization."
          }
        ]
      },
      "cropsCsv": {
        "requiredHeaders": ["uri", "code", "label"],
        "optionalHeaders": ["labels_json", "synonyms_json", "source_id"]
      },
      "varietiesCsv": {
        "requiredHeaders": ["uri", "crop_uri", "code", "label"],
        "optionalHeaders": ["labels_json", "synonyms_json", "source_id", "breeder_name", "maturity_group"]
      },
      "cliBuildExample": "python3 tools/reference_snapshot_pipeline.py build --profile specs/v0.8/reference-ingest/profiles/eppo-2026.json --source-version snapshot-YYYY-MM --crops-csv ./crops.csv --varieties-csv ./varieties.csv --out ./payload.json"
    }
  ]
}
```

### 4.5 `POST /v1/reference/source-ingestion/check`

Purpose:

- validate source/profile/sourceVersion/header readiness before executing snapshot import.

Request (abbrev):

```json
{
  "sourceSystem": "EU_CATALOG",
  "sourceVersion": "snapshot-2026-04",
  "profileCode": "eu-catalog-2026",
  "entityType": "variety",
  "expectedChecksContractVersion": "1.0.0",
  "requireHeaders": true,
  "jurisdiction": "SI",
  "cropsCsvHeaders": ["uri", "code", "label"],
  "varietiesCsvHeaders": ["uri", "crop_uri", "code", "label", "source_id"]
}
```

Response (abbrev):

```json
{
  "ready": true,
  "sourceSystem": "EU_CATALOG",
  "sourceVersion": "snapshot-2026-04",
  "profileCode": "eu-catalog-2026",
  "profilePath": "specs/v0.8/reference-ingest/profiles/eu-catalog-2026.json",
  "errors": [],
  "warnings": [],
  "checks": {
    "contractVersion": "1.0.0",
    "expectedChecksContractVersion": "1.0.0",
    "contractVersionMatch": true,
    "headerValidationMode": "strict",
    "expectedCropsRequiredHeaders": ["uri", "code", "label"],
    "expectedVarietiesRequiredHeaders": ["uri", "crop_uri", "code", "label"],
    "missingCropsRequiredHeaders": [],
    "missingVarietiesRequiredHeaders": [],
    "acquisitionGuidanceAvailable": true,
    "acquisitionEntryPointUrl": "https://food.ec.europa.eu/plants/plant-reproductive-material/plant-variety-catalogues-databases-information-systems_en",
    "acquisitionRequiresAuth": false,
    "acquisitionArtifactEntityTypes": ["crop_species", "variety"],
    "missingAcquisitionEntityTypes": [],
    "preferredSourceSystem": "EU_CATALOG"
  }
}
```

Readiness contract note:

- `checks` is a typed object contract (`ReferenceIngestionReadinessChecks`) with stable sub-structures,
  including typed `recommendedAcquisitionSources[]`, rather than an unbounded free-form map.
- `checks.contractVersion` provides explicit contract versioning for client parsers.
- `/v1/capabilities.contracts.referenceIngestionReadinessChecks.version` mirrors the same contract version
  for feature/capability-time negotiation before requests are sent.
- clients may optionally send `expectedChecksContractVersion` in readiness requests; mismatches are
  surfaced via `checks.contractVersionMatch=false` and warning `checks_contract_version_mismatch`.

Strict mode behavior:

1. `requireHeaders=false` (default): readiness reports missing required columns only when header lists are provided.
2. `requireHeaders=true`: readiness fails (`ready=false`) when required header input is absent for the requested scope.
3. Scope rules in strict mode:
   - `entityType=variety`: `varietiesCsvHeaders` required
   - `entityType=crop_species`: `cropsCsvHeaders` required
   - no `entityType`: both header sets required
4. Acquisition coverage checks:
   - response includes `acquisition*` diagnostics from selected source profile
   - if selected profile requires auth, warning `source_access_requires_auth` is returned
   - if requested `entityType` has no acquisition artifact in selected profile, readiness fails with `missing_acquisition_artifact_for_entity_type`
   - if `entityType` is omitted, readiness requires artifacts for both `crop_species` and `variety`
   - when acquisition scope is missing, response includes deterministic fallback suggestions in
     `checks.recommendedAcquisitionSources[]` and warning `acquisition_guidance_scope_mismatch`

### 4.6 `GET /v1/reference/crops/search`

Query params:

- `q` (required): user query string.
- `lang` (optional): preferred language tag (default: `en`).
- `sourceVersion` (optional): pin search to a specific imported snapshot version.
- `sourceSystem` (optional): restrict results to a specific source system (e.g., `EPPO`, `EU_CATALOG`).
- `limit` (optional int, default 10, max 50)

Response:

```json
{
  "q": "koruza",
  "lang": "sl-SI",
  "sourceVersion": "snapshot-2026-02",
  "items": [
    {
      "uri": "https://data.farmco.si/farm-rm/v1/crop-species/EU/ZEAMA",
      "code": "ZEAMA",
      "label": "Koruza",
      "labels": {"sl-SI": "Koruza", "en": "Maize"},
      "synonyms": ["maize", "corn"],
      "match": {"kind": "synonym_exact", "score": 0.98},
      "source": {"sourceSystem": "EPPO", "sourceId": "ZEAMA", "sourceVersion": "snapshot-2026-02"}
    }
  ]
}
```

### 4.7 `GET /v1/reference/varieties/search`

Query params:

- `q` (required): query string.
- `cropUri` (required): restrict to a crop/species.
- `lang` (optional): preferred language tag.
- `sourceVersion` (optional): pin search to a specific imported snapshot version.
- `sourceSystem` (optional): restrict results to a specific source system (e.g., `EU_CATALOG`, `CPVO`).
- `limit` (optional int, default 10, max 50)

Response:

```json
{
  "q": "PIONEER 123",
  "cropUri": "https://data.farmco.si/farm-rm/v1/crop-species/EU/ZEAMA",
  "lang": "en",
  "sourceVersion": "snapshot-2026-01",
  "items": [
    {
      "uri": "https://data.farmco.si/farm-rm/v1/variety/EU/ZEAMA-PIO-123",
      "cropUri": "https://data.farmco.si/farm-rm/v1/crop-species/EU/ZEAMA",
      "code": "ZEAMA-PIO-123",
      "label": "PIONEER 123",
      "labels": {"en": "PIONEER 123"},
      "synonyms": ["Pioneer123", "PIO 123"],
      "match": {"kind": "label_exact", "score": 0.96},
      "source": {"sourceSystem": "EU_CATALOG", "sourceId": "…", "sourceVersion": "snapshot-2026-01"}
    }
  ]
}
```

### 4.8 `POST /v1/reference/snapshots/import` (Operator/Admin)

Purpose:

- Import a versioned local snapshot of crop/species and variety references sourced from authoritative catalogues.

Request shape (abbrev):

```json
{
  "snapshot": {
    "sourceSystem": "EU_CATALOG",
    "sourceVersion": "snapshot-2026-03",
    "publishedAt": "2026-03-01",
    "sourceRef": "https://food.ec.europa.eu/...",
    "licenseHint": "see source"
  },
  "crops": [
    {
      "uri": "https://data.farmco.si/farm-rm/v1/crop-species/EU/ZEAMA",
      "code": "ZEAMA",
      "label": "Maize",
      "labels": {"en": "Maize", "sl-SI": "Koruza"},
      "synonyms": ["corn"],
      "sourceId": "ZEAMA"
    }
  ],
  "varieties": [
    {
      "uri": "https://data.farmco.si/farm-rm/v1/variety/EU/ZEAMA-PIO-123",
      "cropUri": "https://data.farmco.si/farm-rm/v1/crop-species/EU/ZEAMA",
      "code": "ZEAMA-PIO-123",
      "label": "PIONEER 123",
      "labels": {"en": "PIONEER 123"},
      "synonyms": ["PIO 123"],
      "sourceId": "PIO-123"
    }
  ]
}
```

Response shape (abbrev):

```json
{
  "snapshotUri": "urn:reference-source-snapshot:…",
  "sourceSystem": "EU_CATALOG",
  "sourceVersion": "snapshot-2026-03",
  "counts": {
    "persistedSnapshots": 1,
    "persistedCropEntries": 1200,
    "persistedVarietyEntries": 8300
  }
}
```

### 4.9 `POST /v1/reference/snapshots/import/preview` (Operator/Admin)

Purpose:

- run deterministic pre-import validation and impact preview without writing snapshot data.

Request shape:

- same as `POST /v1/reference/snapshots/import`.

Response shape (abbrev):

```json
{
  "ready": true,
  "sourceSystem": "EU_CATALOG",
  "sourceVersion": "snapshot-2026-03",
  "snapshotUri": "urn:reference-source-snapshot:...",
  "errors": [],
  "warnings": [],
  "checks": {
    "persistenceEnabled": true,
    "previewImportHashSha256": "sha256...",
    "existingImportHashSha256": null,
    "latestImportedSourceVersion": "snapshot-2026-02",
    "snapshotVersionAlreadyImported": false
  },
  "counts": {
    "payloadCrops": 1200,
    "payloadVarieties": 8300,
    "uniqueCropUris": 1200,
    "uniqueVarietyUris": 8300,
    "duplicateCropUris": [],
    "duplicateVarietyUris": [],
    "unresolvedVarietyCropUris": []
  }
}
```

### 4.10 `GET /v1/reference/snapshots/diff`

Purpose:

- compare two imported snapshot versions for the same source system before switching pinned versions in clients.

Query params:

- `sourceSystem` (required)
- `fromSourceVersion` (required)
- `toSourceVersion` (required)
- `entityType` (optional): `all` (default), `crop_species`, `variety`
- `sampleLimit` (optional int, default 20, max 200)

Response shape (abbrev):

```json
{
  "sourceSystem": "EU_CATALOG",
  "fromSourceVersion": "snapshot-2026-03",
  "toSourceVersion": "snapshot-2026-04",
  "entityType": "all",
  "checks": {
    "fromSnapshotUri": "urn:reference-source-snapshot:...",
    "toSnapshotUri": "urn:reference-source-snapshot:...",
    "sampleLimit": 20,
    "sameVersion": false
  },
  "cropSpecies": {
    "counts": {
      "fromCount": 1200,
      "toCount": 1220,
      "addedCount": 30,
      "removedCount": 10,
      "changedCount": 15,
      "unchangedCount": 1175
    },
    "sample": {
      "addedUris": ["..."],
      "removedUris": ["..."],
      "changedUris": ["..."]
    }
  }
}
```

Normative behavior:

1. Import is append-only and idempotent for `(sourceSystem, sourceVersion)`.
2. Re-import of an existing `(sourceSystem, sourceVersion)` with a different payload MUST fail with conflict (`409`).
3. Search endpoints use the latest imported snapshot when available.
4. If no DB snapshot is available, search falls back to bundled reference seed data.
5. Import endpoint availability MUST be discoverable via `/v1/capabilities.features.referenceSnapshotImport` and independently gateable (`503 feature_disabled`).
6. Preview endpoint availability MUST be discoverable via `/v1/capabilities.features.referenceSnapshotImportPreview` and independently gateable (`503 feature_disabled`).
7. Preview endpoint MUST be side-effect free (no snapshot writes).
8. Preview MUST detect version-hash status when persistence is available:
   - same `(sourceSystem, sourceVersion)` + same hash => warning `source_version_already_imported_same_payload`
   - same `(sourceSystem, sourceVersion)` + different hash => error `source_version_conflicts_with_existing_payload`
9. Duplicate `crop.uri` or `variety.uri` entries in one payload are invalid:
   - import MUST fail with `422` (`duplicate_crop_uri_in_payload` / `duplicate_variety_uri_in_payload`)
   - preview MUST set `ready=false` and include the same duplicate error codes.
10. Snapshot diff endpoint availability MUST be discoverable via `/v1/capabilities.features.referenceSnapshotDiff` and independently gateable (`503 feature_disabled`).
11. Snapshot diff MUST return deterministic counts/samples for the same `(sourceSystem, fromSourceVersion, toSourceVersion, entityType)` input.
12. Source profile responses MUST include source acquisition guidance (`entryPointUrl`, `requiresAuth`, artifacts) when available in profile metadata.
13. Ingestion readiness checks MUST validate that selected profile acquisition artifacts cover the requested `entityType` scope, and both scopes when `entityType` is omitted.
14. On acquisition scope mismatch, readiness checks MUST provide deterministic source/profile fallback suggestions.

Operational ingestion tooling:

- Pipeline CLI: `tools/reference_snapshot_pipeline.py`
- Runbook + sample CSV files: `specs/v0.8/reference-ingest/README.md`
- Source profiles (EU catalog / CPVO / EPPO metadata defaults):
  `specs/v0.8/reference-ingest/profiles/*.json`

## 5. Ranking Rules (Normative)

Search must be deterministic and explainable. Implementation MUST:

1. Normalize strings:
   - lowercase
   - trim
   - fold diacritics
   - collapse whitespace
2. Score candidates using a stable priority order:
   - exact code match
   - exact preferred-label match (in requested `lang` if available)
   - exact alt-label/synonym match
   - prefix matches
   - token containment matches
   - (optional) bounded fuzzy match
3. Return `match.kind` and `match.score` for each item.

If fuzzy match is used, it must be bounded and deterministic (no ML at query time).

## 6. Versioning and Snapshot Semantics (Normative)

Requirement:

- The reference dataset MUST be treated as a snapshot, not a live external registry.

The API SHOULD expose:

- a stable `sourceVersion` per item, and
- a response-level `sourceVersion` field (effective snapshot used for the query), and
- cache/version headers:
  - `ETag`
  - `Cache-Control: max-age=…`
  - `X-Reference-Source-Version`

If `sourceVersion` is supplied as query param and no matching snapshot exists, API SHOULD return `404`.
If `sourceSystem` is supplied with `sourceVersion`, API SHOULD resolve the snapshot by both filters and return `404` when the pair has no matching data.

This enables iOS to cache and replay normalization consistently.

## 7. Interaction With OCR Parse (Normative)

Two allowed integration patterns:

1. **Client-driven lookup (baseline)**:
   - `/v1/ai/ocr/parse` returns `referenceHints` (tokens + suggested queries).
   - iOS calls search endpoints and lets the user choose.
2. **Backend-embedded candidates (optional)**:
   - backend performs deterministic search using tokens and includes `referenceCandidates[]` in parse response.
   - AI may select among candidates, but may not invent URIs.

## 8. Error Handling (Normative)

- `400` missing required params (`q`, `cropUri`)
- `422` invalid `lang` tag
- `200` with `items=[]` when no results

## 9. Acceptance Criteria (Testable)

1. Search results are stable for the same query and dataset snapshot.
2. `lang` preference changes labels where available, without changing identity.
3. Synonym matching works for common names (e.g., “koruza” finds maize).
4. “None/Unknown” remains a valid client choice (no forced normalization).

## 10. Dependencies

- `localized_label` exists for multilingual and synonyms.
- Crop/species and variety tables exist (or equivalent reference store).

## 11. Next Part

Part 4: Agronomy season windows (knowledge pack + API): [part-4-agronomy-season-windows.md](/Users/einstein/Documents/Codex/Semantic%20farming/docs/implementation/ai-capture-assist/part-4-agronomy-season-windows.md)
