# AI Onboarding Pack

This folder is the entry point for agents who need to reason about OFARM and the OF Platform without reading the whole repository first. Current baseline reviewed at commit `239ba5e` on `2026-03-21 11:08 CET`. Compatibility-sensitive names such as `Farm-RM`, `farm_rm`, and `openapi-farm-rm.yaml` still remain where the repo needs them.

## What this pack is

- A compact orientation layer for the repo’s semantic model, runtime, compliance stack, generation flow, and current implementation boundaries.
- A routing aid that points you to stronger authority files before you change anything important.
- A summary layer that must yield to runtime code, tests, ontology, SHACL, SQL, rulepacks, profiles, and authored archetype/template specs when they disagree. `AGENTS.md`, `BRAIN.md`, `specs/generated/README.md:L6-L24`

## Fast facts

- OFARM is the reference-model side of the repo; the OF Platform is the operational FastAPI runtime layered on top of those source specs. `specs/v0.1/Farm-RM-v0.1-Specification.md:L49-L119`, `specs/api/v1/server/fastapi/app/main.py:L225-L232`
- Runtime code and tests outrank onboarding prose and the checked-in OpenAPI file when contract questions matter. `AGENTS.md`, `specs/api/v1/server/fastapi/tests/test_openapi_contract_alignment.py:L98-L108`
- Human-authored markdown archetypes and templates remain the source of truth for generated FADL and JSON artifacts. `specs/generated/README.md:L6-L24`, `tools/generate_fadl_from_markdown.py:L1-L320`
- The strongest reporting evidence is still Slovenia crops-only organic control-pack work plus a few additional SI helper/reporting packs, not broad multi-jurisdiction coverage. `specs/v0.4/regulatory/report-packs/si-org-control-pack-2026.json:L29-L35`, `docs/ai/indexes/drift-register.yaml`
- Reference source planning, source profiles, readiness checks, snapshot preview/import, and pinned search are live repo surfaces, not just tooling aspirations. `specs/v0.8/reference-ingest/README.md:L1-L198`, `specs/api/v1/server/fastapi/app/main.py:L9663-L9770`, `specs/api/v1/server/fastapi/app/main.py:L10759-L10980`
- Event-specific `/v1/field-ops/*` routes remain commit authority even though the additive `OperationProposal` and `OperationDraft` layer is now implemented. `docs/implementation/logging-attestation-master-spec.md:L91-L121`, `specs/api/v1/server/fastapi/tests/test_operation_drafts.py:L703-L1348`
- Control Center is a local launcher, recorder, and proxy workbench surface, not proof of a broader hosted approval platform. `apps/control-center/README.md:L141-L238`, `docs/architecture/adr/0004-control-center-local-internal-workbench.md`
- The stable package root is `specs/v1.0.0`, but most semantic and implementation authority still lives in `specs/v0.1` through `specs/v0.8`. `specs/v1.0.0/version-map.md:L20-L37`, `specs/v1.0.0/release-manifest.json:L87-L116`

## Start here

1. Read [00-index.md](00-index.md) for the pack map and task-based reading order.
2. Read [10-repo-map.md](10-repo-map.md) if you first need directory ownership and authority boundaries.
3. Then jump by question:
   - semantic model: [20-semantic-core.md](20-semantic-core.md)
   - runtime and contracts: [30-runtime-architecture.md](30-runtime-architecture.md), [40-api-and-data-contracts.md](40-api-and-data-contracts.md)
   - compliance/reporting: [50-compliance-and-reporting.md](50-compliance-and-reporting.md)
   - build/test/generate flow: [60-build-run-test-generate.md](60-build-run-test-generate.md)
   - maturity and cautions: [70-implementation-status.md](70-implementation-status.md), [80-open-questions-and-risks.md](80-open-questions-and-risks.md)
   - lookup references: [90-glossary.md](90-glossary.md), [sources-manifest.yaml](sources-manifest.yaml)

## When to leave this pack

- For logging, attestation, or review-workbench questions, go to the `docs/implementation/logging-attestation-*.md` packet named in [00-index.md](00-index.md).
- For reference-ingest operator flow, source profiles, and sync tooling, go to `specs/v0.8/reference-ingest/README.md` and the source profiles under `specs/v0.8/reference-ingest/profiles/`.
- For runtime route shape, persistence coverage, and examples, go to `specs/api/v1/server/fastapi/README.md`, `specs/api/v1/server/fastapi/app/main.py`, and the FastAPI test suite.
- For advisor runtime behavior, go to `docs/advisor/v1/README.md` and the `advisor_*` runtime modules.

## How to use this pack

- Use this folder to decide where the real authority lives before editing.
- Treat repeated cautions as intentional whenever they defend a boundary like SI crops-only reporting, compatibility-sensitive naming, or runtime-over-doc authority.
- When a claim in this pack and a stronger authority source disagree, update the pack instead of forcing the repo to fit the prose.
