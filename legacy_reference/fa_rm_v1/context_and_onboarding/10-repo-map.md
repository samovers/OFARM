# Repo Map

## Topology

```text
Semantic farming/
├── specs/
│   ├── v0.1 .. v0.8/          # authored semantic, regulatory, SQL, and profile sources
│   ├── generated/             # generated FADL/JSON registry from markdown sources
│   ├── api/v1/server/fastapi/ # OF Platform runtime, tests, examples, persistence
│   └── v1.0.0/                # stable package metadata and bundle QA
├── tools/                     # generators, release guards, ingest and sync tooling
├── apps/control-center/       # local launcher, recorder, and diagnostics hub
└── docs/                      # onboarding, implementation notes, ADRs, booklet output
```

## What each major area owns

| Path | Owns | Authority level |
| --- | --- | --- |
| `specs/v0.1` to `specs/v0.8` | semantic sources, ontology, SHACL, SQL, authored archetypes/templates, rulepacks, profiles | high |
| `specs/api/v1/server/fastapi/` | runtime behavior, request/response models, auth, persistence, contract tests | highest |
| `specs/v1.0.0/` | stable package metadata, release manifests, bundle QA | medium-high |
| `tools/` | generation, bundle verification, reference sync and snapshot tooling | medium |
| `apps/control-center/` | local stack orchestration, request capture, diagnostics, local proxy workbench surfaces | medium-high |
| `docs/ai/onboarding/` and `docs/ai/indexes/` | routing, orientation, authority guidance | advisory |
| `docs/booklet/reference/` | generated narrative/reference output | derivative |

This split matches the repo-level ownership map and authority order. `docs/ai/indexes/ownership-map.yaml`, `docs/ai/indexes/repo-index.yaml`, `AGENTS.md`

## Directory roles

### `specs/`

- The core source tree. Base RM authority starts in `v0.1`, while major agronomy, plant-reference, and organic-compliance extensions continue through `v0.8`. `specs/v0.1/Farm-RM-v0.1-Specification.md:L49-L119`, `specs/v0.8/Farm-RM-v0.8-Agronomy-Archetypes-and-Templates-Specification.md:L71-L98`
- `specs/v1.0.0` is the stable packaging layer, not the place where most substantive source meaning is authored. `specs/v1.0.0/version-map.md:L20-L37`, `specs/v1.0.0/release-manifest.json:L87-L201`

### `specs/generated/`

- Generated artifact registry and outputs derived from authored markdown specs. Do not treat this folder as upstream authority over the markdown sources. `specs/generated/README.md:L6-L24`, `specs/generated/fadl-manifest.json:L1-L25`

### `specs/api/v1/server/fastapi/`

- The main runtime surface: app entry, auth, persistence, reporting binders, tests, and examples all live here. `specs/api/v1/server/fastapi/app/main.py:L143-L232`, `specs/api/v1/server/fastapi/tests/test_api.py:L109-L260`

### `tools/`

- Build and translation layer for the repo: markdown-to-artifact generation, booklet link generation, release-bundle guards, generic reference snapshot building, and source-specific EU PVP or EPPO sync tooling. `tools/generate_fadl_from_markdown.py:L1-L320`, `tools/release_bundle_guard.py:L1-L320`, `tools/reference_snapshot_pipeline.py:L278-L320`, `tools/eu_pvp_portal_sync.py:L1-L20`, `tools/eppo_gd_sync.py:L1-L24`

### `apps/control-center/`

- Local operational hub for stack launch, request capture, contract checks, OCR mode switching, and local review-workbench proxy flows. `apps/control-center/README.md:L1-L18`, `apps/control-center/run_stack.sh:L17-L42`, `apps/control-center/server.py:L28-L65`
- `run_stack.sh` derives the minimum acceptable local backend API version from `specs/v1.0.0/release-manifest.json` instead of keeping a stale hard-coded floor. `apps/control-center/run_stack.sh`, `specs/v1.0.0/release-manifest.json`

### `docs/`

- `docs/ai/onboarding/`: orientation pack
- `docs/ai/indexes/`: routing and validation indexes
- `docs/implementation/`: larger implementation packets and boundary notes
- `docs/booklet/reference/`: generated secondary narrative output

## Authored versus generated assets

- Authored first: `specs/v0.x`, `specs/v0.4/regulatory/`, `specs/v0.8/reference-ingest/`, `specs/api/v1/server/fastapi/app/`, `docs/implementation/`
- Generated or derivative: `specs/generated/`, `docs/booklet/reference/`, generated index families noted in `docs/ai/indexes/artifact-lineage.yaml`

When in doubt, change the authored source and regenerate or refresh the derivative layer instead of patching the derivative by hand. `specs/generated/README.md:L6-L24`

## Build and runtime relationships

```text
authored specs and profiles
        |
        +--> tools/* --------------------> generated artifacts / bundle checks
        |
        +--> FastAPI runtime -----------> runtime responses, persistence, tests
        |
        +--> reporting binders/renderers
        |
        +--> onboarding and indexes (summary layer only)
```

## Entry points by task

- semantic model and authored templates: `specs/v0.1/` and `specs/v0.8/`
- runtime contracts and behavior: `specs/api/v1/server/fastapi/app/main.py`, `specs/api/v1/server/fastapi/tests/`
- local stack and device routing: `apps/control-center/run_stack.sh`, `apps/control-center/README.md`
- reference-ingest operator flow: `specs/v0.8/reference-ingest/README.md`
- reporting and official PDF behavior: `specs/api/v1/server/fastapi/app/reporting_control_pack.py`, `specs/api/v1/server/fastapi/app/si_control_pack_official_form_pdf.py`
- onboarding and routing: `docs/ai/onboarding/`, `docs/ai/indexes/`

## Practical authority map

- Build on first: runtime/tests, authored semantic and regulatory sources, source-specific tooling, stable-package manifests when release packaging matters
- Treat as advisory: onboarding docs, implementation notes, curated indexes
- Treat as derivative: booklet output and generated artifact mirrors
