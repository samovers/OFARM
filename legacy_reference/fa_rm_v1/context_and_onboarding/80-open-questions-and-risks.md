# Open Questions And Risks

Use this file as the conceptual worklist for future design sessions. It is intentionally organized by question type so agents can jump straight to the boundary they are about to stress.

## Authority and versioning

### Which OpenAPI artifact is authoritative when metadata conflicts?

- `implemented`: the checked-in OpenAPI file and the runtime app currently align on `1.0.26` and `OF Platform API`, but authority order still matters when future conflicts appear. `specs/api/v1/openapi-farm-rm.yaml:L1-L5`, `specs/api/v1/server/fastapi/app/main.py:L285-L320`, `specs/api/v1/server/fastapi/tests/test_openapi_contract_alignment.py:L98-L108`
- Why it matters: client baselines, release gating, and external integrations can still break if static YAML, runtime models, and tests diverge again.

### What do the aligned generated-artifact totals actually prove?

- `implemented`: the generated manifest and the stable release manifest currently both report `176` artifacts on the current stable line. `specs/generated/fadl-manifest.json:L1-L5`, `specs/v1.0.0/release-manifest.json:L1-L5`, `specs/v1.0.0/release-manifest.json:L136-L141`
- Why it matters: agents need to distinguish working-tree artifact growth from stable-package release metadata and avoid treating a release manifest as current branch truth between releases.

### What is the intended long-term authority split between `specs/v0.x` and `specs/v1.0.0`?

- `partial`: version-map and release-manifest explain packaging, but they do not eliminate the need to read historical source streams for actual semantics. `specs/v1.0.0/version-map.md:L20-L37`, `specs/v1.0.0/release-manifest.json:L87-L116`
- Why it matters: agents need to know whether to change pre-release source streams, stable package metadata, or both when evolving the model.

## Model-to-runtime operationalization

### Is every archetype/template supposed to have runtime persistence or API exposure?

- `partial` / `inferred`: the repo has a large generated artifact catalog, a smaller projection index, and a long but selective migration/API surface. `specs/generated/fadl-manifest.json:L1-L220`, `specs/v0.8/templates/projections/template-crop-health-visit-ipm-nutrition-v0_8.json:L1-L92`, `specs/v0.6/sql/bin-run-v1_6-migrations.sh:L20-L106`
- Why it matters: conceptual work can go wrong if an agent assumes the entire semantic catalog is already operationalized.

### When persistence is disabled, which endpoints are still trustworthy for integration testing?

- `partial`: some endpoints return explicit incomplete payloads or example/static data in no-DB mode. `specs/api/v1/server/fastapi/app/reporting_control_pack.py:L810-L837`, `specs/api/v1/server/fastapi/app/main.py:L11960-L12040`
- Why it matters: another agent can misread successful responses as proof of full stack behavior when they may only reflect fallback mode.

### Are older validator scripts meant to remain the compliance engine, or be absorbed into Python/runtime code?

- `implemented`: `app.main` still points to shell validators in older spec streams. `specs/api/v1/server/fastapi/app/main.py:L143-L152`
- Why it matters: future conceptual changes around rule execution, auditability, or platform portability depend on whether shell validators are legacy glue or intentional architecture.

## Compliance and reporting boundaries

### How much of reporting is guaranteed outside the SI crops-only control pack?

- `partial`: the inspected report pack and tests are strongly SI crops-only oriented, with explicit section exclusions. `specs/v0.4/regulatory/report-packs/si-org-control-pack-2026.json:L29-L35`, `specs/api/v1/server/fastapi/tests/test_si_recordbook_contract_v1.py:L218-L260`
- Why it matters: expanding into other jurisdictions or product scopes without a clear boundary will overestimate current compliance coverage.

### How should save-before-proof coexist with the base RM evidence-first semantics?

- `contradiction between docs and code`: base RM semantics expect evidence-bearing immutable execution facts, while current runtime commit paths satisfy that minimally with auto-generated `api_payload` evidence. `specs/v0.1/Farm-RM-v0.1-Specification.md:L113-L152`, `specs/api/v1/server/fastapi/app/persistence.py:L6259-L6278`, `specs/api/v1/server/fastapi/app/persistence.py:L8024-L8043`
- Why it matters: draft/save flows can accidentally violate append-only semantics unless they stay outside committed execution facts.

### How should `operator_attestation` differ from profile-scoped `attested`?

- `partial`: the runtime treats `operator_attestation` as draft evidence and review-action input while keeping `non_attested`, `partially_attested`, `attested`, and `report_ready` as separate assessment lifecycle states for covered operation families. `specs/api/v1/server/fastapi/tests/test_operation_drafts.py:L717-L765`, `specs/api/v1/server/fastapi/app/main.py:L48857-L49173`, `docs/implementation/logging-attestation-master-spec.md:L52-L89`
- Why it matters: conflating operator declaration with profile-complete attestation will either weaken attestation meaning or block saveable draft workflows.

## Operational ownership and workflow boundaries

### What is the intended operational owner of the Control Center versus the backend?

- `implemented` / `inferred`: the Control Center does more than process launch; it also acts as the preferred local URL, recorder, and diagnostic layer. `apps/control-center/README.md:L1-L10`, `apps/control-center/README.md:L119-L148`, `apps/control-center/server.py:L28-L65`
- Why it matters: changes to local testing, iOS integration, or feature discovery may need to land in the hub, not only in FastAPI.

### Where should the generic `Operation*` layer stop and the event-specific runtime begin?

- `implemented`: the current runtime exposes additive generic catalog/proposal/draft/assessment/review surfaces, but committed execution still flows through event-specific `/v1/field-ops/*` routes. `specs/api/v1/server/fastapi/app/main.py:L47920-L49173`, `specs/api/v1/server/fastapi/tests/test_operation_drafts.py:L703-L1348`, `docs/implementation/logging-attestation-master-spec.md:L91-L121`
- Why it matters: replacing the proven commit path too early would sever reporting and persistence contracts that already exist.

### Is Control Center just the local diagnostics hub, or the long-term review and attestation workbench?

- `partial`: current Control Center code and README document diagnostics, request capture, contract checks, advisory governance inventory, and review-workbench proxy surfaces, but they still stop at a local Control Center workbench in front of backend routes rather than a standalone hosted approval system. `apps/control-center/server.py:L3191-L3370`, `apps/control-center/tests/test_operation_review_workbench.py:L47-L181`, `apps/control-center/README.md:L141-L238`
- Why it matters: queue/read-model hosting, auth expectations, and rollout sequencing depend on this boundary.

## Naming, compatibility, and source strategy

### Which legacy Farm-RM / farm_rm identifiers are compatibility-sensitive?

- `implemented`: user-facing runtime titles can now distinguish `OF Platform` from `OFARM`, but the repo still carries compatibility-sensitive legacy identifiers such as `openapi-farm-rm.yaml`, `FARM_RM_DATABASE_URL`, and `farm_rm` Postgres defaults. `specs/api/v1/openapi-farm-rm.yaml:L1-L5`, `apps/control-center/run_stack.sh:L17-L18`, `specs/api/v1/server/fastapi/app/persistence.py:L147-L157`
- Why it matters: blind rename work here can break local ops, CI, clients, or compatibility scripts even when visible product naming is improved.

### What is the normative source strategy for crop/common-name enrichment beyond EU portal exports?

- `implemented` / `partial`: the EU portal sync tool states there is no documented public REST API and uses XLSX export; the repo also carries an EPPO GD sync path, EPPO/AGROVOC bridge profiles, and curated common-name enrichment or override files. `tools/eu_pvp_portal_sync.py:L3-L20`, `tools/eppo_gd_sync.py:L1-L24`, `specs/v0.8/reference-ingest/profiles/eu-catalog-2026.json:L1-L30`, `specs/v0.8/reference-ingest/profiles/eppo-2026.json`, `specs/v0.8/reference-ingest/enrichment/upov-species-common-names-2026.csv`, `specs/v0.8/reference-ingest/enrichment/eppo-common-names-overrides-2026.csv`
- Why it matters: provenance, licensing, refresh cadence, and cross-language trust all depend on the chosen authority chain.

## Highest-value questions for the project owner

1. Should the repo intentionally operationalize more of the semantic catalog, or is selective runtime coverage the long-term model?
2. Is the current SI crops-only reporting boundary meant to stay product-defining, or is broader jurisdiction support an active near-term target?
3. Should Control Center remain a local proxy/workbench, or is there a planned hosted review and attestation product surface?
4. Are shell validators part of the intended long-term compliance architecture, or are they transitional glue?
