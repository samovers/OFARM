# Index

This is the navigation page for the onboarding pack. Current baseline reviewed at commit `239ba5e` on `2026-03-21 11:08 CET`.

## Repo identity and purpose

- OFARM is the reference-model and semantic-spec side of the repository.
- The OF Platform is the runtime, persistence, reporting, and local-operations side.
- This onboarding pack exists to route agents to the right authority quickly, not to replace runtime code, tests, ontology, SHACL, SQL, or authored markdown specs. `specs/v0.1/Farm-RM-v0.1-Specification.md:L49-L119`, `specs/api/v1/server/fastapi/app/main.py:L225-L232`, `AGENTS.md`

## Definitely in scope

- semantic-core sources under `specs/v0.x`
- runtime contract and persistence evidence under `specs/api/v1/server/fastapi/`
- SI/EU organic reporting assets that are explicitly present in rulepacks, report packs, layouts, runtime binders, and tests
- generation, bundle, and reference-ingest tooling
- local Control Center behavior

## Definitely out of scope unless stronger evidence appears

- broad non-SI reporting guarantees
- livestock or beekeeping reporting support inside the SI crops-only control-pack line
- blind renames of compatibility-sensitive identifiers such as `farm_rm`, `openapi-farm-rm.yaml`, or `api_stub`
- treating booklet content or onboarding prose as more authoritative than runtime/tests/source specs

## Current maturity summary

- `implemented`: base RM semantics, generated artifact flow, FastAPI runtime, reference snapshot import/search, OCR parse, SI control-pack binder/PDF path, event-specific field-op logging, additive operation workbench layer, local Control Center
- `partial`: broader reporting scope, no-DB fallback behavior, full runtime coverage for every generated archetype/template, hosted workbench rollout beyond the local Control Center
- `unknown`: broad US or non-SI reporting support unless the relevant runtime/tests/report assets prove it

## Recommended reading order

1. [AI_ONBOARDING.md](AI_ONBOARDING.md) for the fast briefing.
2. [10-repo-map.md](10-repo-map.md) for path ownership and authority boundaries.
3. Choose the next doc by task:
   - model or vocabulary work: [20-semantic-core.md](20-semantic-core.md)
   - runtime/API work: [30-runtime-architecture.md](30-runtime-architecture.md), [40-api-and-data-contracts.md](40-api-and-data-contracts.md)
   - compliance/reporting work: [50-compliance-and-reporting.md](50-compliance-and-reporting.md)
   - operator flow, build, or test work: [60-build-run-test-generate.md](60-build-run-test-generate.md)
   - reality check and cautions: [70-implementation-status.md](70-implementation-status.md), [80-open-questions-and-risks.md](80-open-questions-and-risks.md)
   - terminology or source lookup: [90-glossary.md](90-glossary.md), [sources-manifest.yaml](sources-manifest.yaml)

## Targeted implementation packages

### Logging and attestation

Read this packet when the task is about generic `Operation*` abstractions, save-before-proof workflow, attestation state, or the Control Center review workbench:

- `docs/implementation/logging-attestation-current-state.md`
- `docs/implementation/logging-attestation-capability-matrix.md`
- `docs/implementation/logging-attestation-contradictions-ledger.md`
- `docs/implementation/logging-attestation-master-spec.md`
- `docs/implementation/logging-attestation-contracts.md`
- `docs/implementation/logging-attestation-open-decisions.md`

### Advisor runtime

Read this cluster when the task is specifically about `/v1/advisor/*`, objective profiles, knowledge-pack reloads, preview versus persisted bundle behavior, or proof-delta routing:

- `docs/advisor/v1/README.md`
- `specs/api/v1/server/fastapi/app/advisor_engine.py`
- `specs/api/v1/server/fastapi/app/advisor_models.py`
- `specs/api/v1/server/fastapi/app/advisor_policy.py`
- `specs/api/v1/server/fastapi/tests/test_advisor_api.py`

## Top 10 truths about this repo

1. Runtime/tests beat onboarding prose when they disagree.
2. Authored markdown archetypes/templates beat generated artifacts.
3. `specs/v0.x` still carries most semantic authority even though `specs/v1.0.0` exists.
4. The runtime is substantial and persistence-backed, not a placeholder service.
5. Reference-ingest is a real route family with planning, profiles, readiness, preview, import, catalog, diff, and pinned search behavior.
6. SI crops-only organic reporting is the clearest proven compliance/reporting slice.
7. Event-specific field-op routes still own committed execution.
8. The additive `OperationProposal` and `OperationDraft` layer is implemented, but it does not replace event-specific commit authority.
9. Control Center is local, proxy-first, and operationally important.
10. Compatibility-sensitive legacy identifiers still matter even after user-facing naming cleanup.

## Top 10 open questions or risks

1. How much of the generated semantic catalog is meant to become runtime or persistence coverage?
2. How much reporting support exists outside the SI crops-only path?
3. Which legacy names are still operationally unsafe to rename?
4. How should `specs/v0.x` authority and `specs/v1.0.0` packaging evolve over time?
5. What is the long-term authority chain for crop/common-name enrichment?
6. Which no-DB responses are trustworthy for integration testing?
7. How far should Control Center grow beyond local diagnostics and proxy workbench behavior?
8. How long should shell validators remain part of the compliance engine?
9. Where should the additive `Operation*` layer stop?
10. How should operator attestation differ from assessment lifecycle completion?

For evidence and why these matter, go to [80-open-questions-and-risks.md](80-open-questions-and-risks.md).
