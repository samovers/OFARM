# Runtime Architecture

Use this doc for the running system: process shape, backend composition, persistence mode, local stack behavior, and where major runtime responsibilities sit. For route-by-route contract detail, use [40-api-and-data-contracts.md](40-api-and-data-contracts.md). For operator commands, use [60-build-run-test-generate.md](60-build-run-test-generate.md).

## Runtime shape

```text
[Markdown archetypes/templates]         [Rulepacks / layouts / profiles / SQL / SHACL]
              |                                          |
              v                                          v
   tools/generate_fadl_from_markdown.py        OF Platform runtime (app.main)
              |                                          |
              v                                          +--> auth.py (Bearer + X-Farm-URI)
   specs/generated/fadl-manifest.json          +--> persistence.py (Postgres farm_rm_v1)
                                                         +--> reporting_control_pack.py
                                                         +--> SI official PDF renderer
                                                         +--> reference source planning / snapshot import / search
                                                         +--> OCR parse + metrics + advisor capabilities

[iOS / Simulator / browser]
              |
              v
   apps/control-center server (8091) --> local backend (8080) --> PostgreSQL
```

## Local stack bootstrap

- `implemented`: `apps/control-center/run_stack.sh` is the local orchestration entry point. It defaults `FARM_RM_DATABASE_URL` to local Postgres and disables auth for local runs unless overridden. `apps/control-center/run_stack.sh:L17-L18`
- `implemented`: the script attempts to load `OPENAI_API_KEY` from macOS Keychain and enables OCR OpenAI mode automatically when present. `apps/control-center/run_stack.sh:L20-L42`
- `implemented`: the backend is launched from `specs/api/v1/server/fastapi` and must satisfy the current checked-in `releaseVersion` from `specs/v1.0.0/release-manifest.json` according to the startup health check; Control Center also uses that same release version as the fallback mobile baseline when no same-release iOS contract file is present locally. `apps/control-center/run_stack.sh`, `apps/control-center/server.py`, `specs/v1.0.0/release-manifest.json`
- `implemented`: local readiness now has three separate layers on purpose: `run_stack.sh` startup preflight and additive patching for the default DB, the shell schema-check scripts for live DB-state readiness, and `make operation-schema-check` for runtime-to-SQL source parity. None of those layers replaces the others. `apps/control-center/run_stack.sh:L430-L583`, `apps/control-center/check_operation_schema.sh:L1-L84`, `apps/control-center/check_reporting_schema.sh:L1-L57`, `tools/check_operation_schema_parity.py:L1-L104`, `apps/control-center/README.md:L29-L55`
- `implemented`: the hub listens on `8091` and acts as the recommended URL for simulator or iPhone traffic. `apps/control-center/README.md:L65-L67`, `apps/control-center/README.md:L119-L127`

## Backend composition

- `implemented`: `app.main` discovers the repo root and binds runtime dependencies to spec assets: validator shell scripts, report packs and layouts, template projections, and reference-ingest profiles. `specs/api/v1/server/fastapi/app/main.py:L135-L165`
- `implemented`: the OF Platform FastAPI app uses global auth dependency injection and custom OpenAPI security schemes for Bearer JWT and `X-Farm-URI`. `specs/api/v1/server/fastapi/app/main.py:L225-L232`, `specs/api/v1/server/fastapi/app/main.py:L8877-L9101`
- `implemented`: the backend also wires an advisor runtime service and policy into `app.main`, exposing capability-backed `/v1/advisor/*` routes that use the authored handoff bundle under `docs/advisor/v1/`. `docs/advisor/v1/README.md:L1-L13`, `specs/api/v1/server/fastapi/app/main.py:L21458-L21464`, `specs/api/v1/server/fastapi/app/main.py:L21770-L21915`, `specs/api/v1/server/fastapi/tests/test_advisor_api.py:L289-L310`
- `implemented`: runtime validator paths still point into older version streams (`v0.1` to `v0.4`) for several operations. That is an architectural boundary, not just stale prose. `specs/api/v1/server/fastapi/app/main.py:L143-L152`

## Auth and tenancy

- `implemented`: non-`/v1/` routes bypass auth; `v1` routes require `Authorization: Bearer` and `X-Farm-URI` unless `FARM_RM_DISABLE_AUTH` is on. `specs/api/v1/server/fastapi/app/auth.py:L84-L122`
- `implemented`: JWT farm scope is enforced against the request header. `specs/api/v1/server/fastapi/app/auth.py:L124-L181`
- `implemented`: tests cover missing bearer token, missing farm scope, and mismatched farm scope. `specs/api/v1/server/fastapi/tests/test_api.py:L109-L135`

## Persistence mode

- `implemented`: persistence is optional and depends on both `psycopg` availability and `FARM_RM_DATABASE_URL`. `specs/api/v1/server/fastapi/app/persistence.py:L147-L157`
- `partial`: several reporting and overview endpoints degrade to incomplete payloads or example or static data when persistence is disabled. `specs/api/v1/server/fastapi/app/reporting_control_pack.py:L647-L648`, `specs/api/v1/server/fastapi/app/reporting_control_pack.py:L810-L837`, `specs/api/v1/server/fastapi/app/main.py:L11960-L12040`
- `implemented`: the persistence layer is broad and already includes farms, fields, crop instances, assets, executed operations, reference snapshots, reporting rows, and more. `specs/api/v1/server/fastapi/app/persistence.py:L13633-L13900`, `specs/api/v1/server/fastapi/app/persistence.py:L13901-L14140`

## Reporting path

- `implemented`: `build_si_org_control_pack_payload()` assembles the canonical SI control-pack payload with section scaffolding, inspector notes, traceability, jurisdiction facts, and binding warnings. `specs/api/v1/server/fastapi/app/reporting_control_pack.py:L644-L803`
- `implemented`: when persistence is enabled, the binder pulls certification scopes, executed operations, fertilizer events, plant-protection rows, receipts, cleanouts, deliveries, complaints, harvest rows, rotation rows, buffer zones, contamination risk, residue panels, input authorization, tasks, control registrations, processing recipes or batches, inventory snapshots, warehouse moves, and phytosanitary case files. `specs/api/v1/server/fastapi/app/reporting_control_pack.py:L845-L1015`
- `implemented`: the official PDF renderer loads the layout map and writes the official form with overflow handling and Slovenian glyph support. `specs/api/v1/server/fastapi/tests/test_si_control_pack_official_form_pdf.py:L70-L99`, `specs/api/v1/server/fastapi/tests/test_si_control_pack_official_form_pdf.py:L102-L159`, `specs/api/v1/server/fastapi/tests/test_si_control_pack_official_form_pdf.py:L206-L243`
- For regulatory scope and non-assumptions, use [50-compliance-and-reporting.md](50-compliance-and-reporting.md).

## Operation logging path

- `implemented`: the write path for logged operations is event-family-specific, not generic. Confirmed routes include planting, mechanical weeding, cover-crop management, tillage, plant protection, pesticide, irrigation, and harvest. `specs/api/v1/server/fastapi/app/main.py:L25109-L28988`
- `implemented`: representative crop-bound routes are strict about `fieldUri` and `cropInstanceUri`, while still allowing ad-hoc execution because `plannedOperationUri` is optional. `specs/api/v1/server/fastapi/app/main.py:L25121-L25344`, `specs/api/v1/server/fastapi/app/main.py:L28519-L28735`, `specs/api/v1/server/fastapi/app/main.py:L28835-L28920`
- `implemented`: immutable execution is written through persistence helpers that insert `executed_operation`, create `api_payload` evidence, link that evidence, then write the family-specific event row. `specs/api/v1/server/fastapi/app/persistence.py:L6176-L6326`, `specs/api/v1/server/fastapi/app/persistence.py:L7939-L8097`, `specs/api/v1/server/fastapi/app/persistence.py:L8099-L8261`
- `implemented`: missing crop context is handled by an explicit pre-resolution step, not by weakening commit semantics. `specs/api/v1/server/fastapi/app/main.py:L15444-L15452`, `specs/api/v1/server/fastapi/app/main.py:L21752-L21920`, `specs/api/v1/server/fastapi/tests/test_crop_context_ensure.py:L89-L376`
- For route families and request or response surface details, use [40-api-and-data-contracts.md](40-api-and-data-contracts.md).

## Control Center role

- `implemented`: the hub is more than a launcher. It captures and redacts request data, carries default reporting-pack category signals, and bootstraps field or crop context used by local diagnostics. `apps/control-center/server.py:L28-L65`
- `implemented`: the README describes the hub as the preferred local bridge for simulator or iPhone traffic and explains OCR mode switching and service start or stop semantics. `apps/control-center/README.md:L1-L10`, `apps/control-center/README.md:L69-L92`, `apps/control-center/README.md:L128-L148`
- `implemented`: reporting governance inventory is currently advisory and read-only. `apps/control-center/README.md:L151-L194`, `apps/control-center/server.py:L3227-L3236`
- `partial`: Control Center now documents and proxies additive logging or attestation review queue, detail, action, and report-binding backfill surfaces, but the rollout remains local and proxy-first rather than a broader hosted workflow. ADR 0004 records that boundary explicitly. `apps/control-center/README.md`, `docs/architecture/adr/0004-control-center-local-internal-workbench.md`, `apps/control-center/server.py:L3191-L3497`, `apps/control-center/tests/test_operation_review_workbench.py:L47-L181`, `specs/api/v1/server/fastapi/app/main.py:L48958-L49173`

## Runtime tensions

- `implemented`: the runtime is now labeled `OF Platform API`, which matches the operational behavior already present in persistence, report rendering, official PDF filling, and test-backed endpoints. `specs/api/v1/server/fastapi/app/main.py:L225-L232`, `specs/api/v1/openapi-farm-rm.yaml:L1-L5`, `specs/api/v1/server/fastapi/app/reporting_control_pack.py:L644-L837`, `specs/api/v1/server/fastapi/tests/test_api.py:L226-L260`
- `partial`: durable runtime identifiers still keep legacy `farm_rm` tokens in env vars and Postgres defaults for compatibility. `apps/control-center/run_stack.sh:L17-L18`, `specs/api/v1/server/fastapi/app/persistence.py:L147-L157`
