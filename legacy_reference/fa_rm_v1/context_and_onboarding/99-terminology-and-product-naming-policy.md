# Terminology And Product Naming Policy

## One-Page Summary

### Observed current state

- `implemented`: user-facing onboarding, glossary, API docs, and runtime metadata now distinguish `OFARM` from `OF Platform`. `docs/ai/onboarding/AI_ONBOARDING.md:L3-L3`, `docs/ai/onboarding/00-index.md:L18-L22`, `docs/ai/onboarding/90-glossary.md:L3-L13`, `specs/api/v1/openapi-farm-rm.yaml:L1-L5`, `specs/api/v1/server/fastapi/app/main.py:L225-L232`, `specs/api/v1/README.md:L1-L5`, `specs/api/v1/server/fastapi/README.md:L1-L5`
- `partial`: compatibility-sensitive identifiers still use legacy `Farm_RM`, `Farm-RM`, or `farm_rm` tokens in filenames, env vars, database defaults, ontology namespaces, and release-manifest paths. `apps/control-center/run_stack.sh:L17-L18`, `specs/api/v1/openapi-farm-rm.yaml:L1-L5`, `specs/v0.1/ontology/farm-rm-v1.ttl:L1-L10`, `specs/v1.0.0/release-manifest.json:L182-L219`
- `unknown`: `fa_rm` is not a current product name in repo-facing docs or runtime labels. The only repo-evidenced occurrence in this inspection pass is an external issue-link alias pattern. `tools/backend_request_concept_review.py:L167-L170`

### Evidence-backed inference

- `inferred`: the safe first pass is to rename conceptual and user-facing layers while leaving machine-stable identifiers alone. The repo already supports that split because runtime titles/descriptions and docs are independent from env var names, ontology IRIs, and file paths. `docs/ai/onboarding/90-glossary.md:L3-L13`, `specs/api/v1/openapi-farm-rm.yaml:L1-L5`, `specs/api/v1/server/fastapi/app/main.py:L225-L232`, `apps/control-center/run_stack.sh:L17-L18`, `specs/v0.1/ontology/farm-rm-v1.ttl:L1-L10`
- `partial`: "Open Farm Agronomy Reference Model" may sound narrower than the model actually implemented here. Repo evidence shows the base model also covers compliance submissions, inspection cases, evidence, storage, and reporting-related semantics. `specs/v0.1/Farm-RM-v0.1-Specification.md:L49-L119`, `specs/v0.1/sql/migrations/0001_init_farm_rm_v1.sql:L32-L320`

### Recommended working assumption

- Use `OFARM` for the semantic model and its artifact stack.
- Use `OF Platform` for the executing system: FastAPI runtime, API contract presentation, Control Center, and local/server operations plane.
- Treat `Farm_RM`, `Farm-RM`, `farm_rm`, and `fa_rm` as legacy aliases unless a file/path/env/db/IRI/test explicitly proves they are compatibility-sensitive identifiers.

## Naming Inventory Summary

| Occurrence | File/path | Current term | Semantic role | Rename class | Safe action | Risk / confidence | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Onboarding pack intro | `docs/ai/onboarding/AI_ONBOARDING.md` | `OFARM`, `OF Platform`, legacy alias note | mixed model + platform explainer | ambiguous/mixed meaning | changed now | low risk / high confidence | `docs/ai/onboarding/AI_ONBOARDING.md:L3-L3`, `docs/ai/onboarding/AI_ONBOARDING.md:L15-L16`, `docs/ai/onboarding/AI_ONBOARDING.md:L36-L38` |
| Glossary lead terms | `docs/ai/onboarding/90-glossary.md` | `OFARM`, `OF Platform`, legacy aliases | canonical terminology map | reference-model meaning + platform/runtime meaning + alias map | changed now | low risk / high confidence | `docs/ai/onboarding/90-glossary.md:L3-L13` |
| Runtime API metadata | `specs/api/v1/server/fastapi/app/main.py` | `OF Platform API` | runtime/platform/server meaning | platform/runtime meaning | changed now | low to medium risk / high confidence | `specs/api/v1/server/fastapi/app/main.py:L225-L232` |
| Static OpenAPI metadata | `specs/api/v1/openapi-farm-rm.yaml` | `OF Platform API` with legacy filename | runtime/platform contract presentation | platform/runtime meaning + durable technical filename | changed title/description now; kept filename | low to medium risk / high confidence | `specs/api/v1/openapi-farm-rm.yaml:L1-L5` |
| API contract README | `specs/api/v1/README.md` | `OF Platform API Contract` | platform/runtime/server meaning | platform/runtime meaning | changed now | low risk / high confidence | `specs/api/v1/README.md:L1-L5`, `specs/api/v1/README.md:L37-L40` |
| FastAPI runtime README | `specs/api/v1/server/fastapi/README.md` | `OF Platform FastAPI Runtime For OFARM API Contract` | platform/runtime/server meaning | platform/runtime meaning | changed now | low risk / high confidence | `specs/api/v1/server/fastapi/README.md:L1-L5` |
| Generated artifacts README | `specs/generated/README.md` | `OFARM Generated Artifacts` | reference-model meaning | reference-model meaning | changed now | low risk / high confidence | `specs/generated/README.md:L1-L14` |
| Stable package README | `specs/v1.0.0/README.md` | `OFARM 1.0.0 Package` with legacy-path note | reference-model package meaning | reference-model meaning + legacy alias note | changed now | low risk / high confidence | `specs/v1.0.0/README.md:L1-L3` |
| DB/env defaults | `apps/control-center/run_stack.sh` | `FARM_RM_DATABASE_URL`, `farm_rm` | durable local ops identifier | durable technical identifier that should not be renamed in first pass | deferred | high risk / high confidence | `apps/control-center/run_stack.sh:L17-L18` |
| Ontology namespace | `specs/v0.1/ontology/farm-rm-v1.ttl` | `https://w3id.org/farm-rm/v1#`, `Farm-RM v1` | ontology IRI / semantic identifier | durable technical identifier that should not be renamed in first pass | deferred | high risk / high confidence | `specs/v0.1/ontology/farm-rm-v1.ttl:L1-L10` |
| Release-manifest artifact paths | `specs/v1.0.0/release-manifest.json` | `Farm-RM-v0.x-...` paths | release bundle index | durable technical identifier that should not be renamed in first pass | deferred | medium to high risk / high confidence | `specs/v1.0.0/release-manifest.json:L182-L219` |
| External issue alias | `tools/backend_request_concept_review.py` | `fa_rm` | legacy external repo alias | typo/inconsistent alias | deferred | medium risk / high confidence | `tools/backend_request_concept_review.py:L167-L170` |

## Target Naming Policy

- `implemented`: `OFARM` means the reference model and semantic architecture: base RM, ontology, SHACL, SQL semantics, archetypes, templates, profiles, and generated machine artifacts. `docs/ai/onboarding/90-glossary.md:L3-L5`, `specs/generated/README.md:L1-L14`
- `implemented`: `OF Platform` means the executing system: FastAPI runtime, API presentation, persistence/auth/reporting behavior, and Control Center operations plane. `docs/ai/onboarding/90-glossary.md:L7-L13`, `specs/api/v1/server/fastapi/app/main.py:L225-L232`, `apps/control-center/README.md:L3-L23`
- `partial`: legacy identifiers may remain when compatibility matters, including file paths, env vars, DB names, ontology namespaces, manifest paths, and integration-sensitive code/test symbols. `docs/ai/onboarding/90-glossary.md:L11-L13`, `apps/control-center/run_stack.sh:L17-L18`, `specs/v0.1/ontology/farm-rm-v1.ttl:L1-L10`, `specs/v1.0.0/release-manifest.json:L182-L219`
- `implemented`: mixed-scope docs should name both layers explicitly instead of collapsing them into one product term. `docs/ai/onboarding/00-index.md:L18-L22`, `docs/ai/onboarding/30-runtime-architecture.md:L33-L35`, `docs/ai/onboarding/40-api-and-data-contracts.md:L5-L8`

## Alias And Transition Rules

- `implemented`: newcomer-facing docs should map legacy names once, then prefer `OFARM` and `OF Platform`. `docs/ai/onboarding/AI_ONBOARDING.md:L3-L3`, `docs/ai/onboarding/90-glossary.md:L11-L13`
- `implemented`: visible runtime/API labels may say `OF Platform API` even while the checked-in contract file path remains `openapi-farm-rm.yaml`. `specs/api/v1/openapi-farm-rm.yaml:L1-L5`, `specs/api/v1/README.md:L1-L5`
- `partial`: legacy `Farm_RM`, `Farm-RM`, and `farm_rm` should be read as aliases unless the occurrence is clearly machine-stable. `apps/control-center/run_stack.sh:L17-L18`, `specs/v0.1/ontology/farm-rm-v1.ttl:L1-L10`, `specs/v1.0.0/release-manifest.json:L182-L219`
- `unknown`: `fa_rm` should not be treated as an endorsed product term. Current repo evidence only proves a legacy external-repo alias pattern. `tools/backend_request_concept_review.py:L167-L170`

## Semantic-Scope Risks

- `partial`: the requested expansion "Open Farm Agronomy Reference Model" may underspecify the actual model boundary. Base-repo evidence includes compliance submissions, inspections, evidence records, rule traces, and reporting-adjacent entities in the core model, not just agronomy. `specs/v0.1/Farm-RM-v0.1-Specification.md:L49-L119`, `specs/v0.1/sql/migrations/0001_init_farm_rm_v1.sql:L271-L320`
- `inferred`: use `OFARM` now because it is the requested public name, but keep a standing owner note that the model is semantically broader than agronomy-only wording suggests.

## First-Pass Patch List

- `implemented`: onboarding pack terminology split and legacy alias note. `docs/ai/onboarding/AI_ONBOARDING.md:L3-L3`, `docs/ai/onboarding/00-index.md:L18-L22`, `docs/ai/onboarding/10-repo-map.md:L5-L32`, `docs/ai/onboarding/20-semantic-core.md:L5-L5`, `docs/ai/onboarding/30-runtime-architecture.md:L5-L16`, `docs/ai/onboarding/40-api-and-data-contracts.md:L5-L8`, `docs/ai/onboarding/80-open-questions-and-risks.md:L18-L21`, `docs/ai/onboarding/90-glossary.md:L3-L13`
- `implemented`: runtime/API presentation renamed from legacy `Farm-RM` / `Contract Stub` wording to `OF Platform API`. `specs/api/v1/openapi-farm-rm.yaml:L1-L5`, `specs/api/v1/server/fastapi/app/main.py:L225-L232`, `specs/api/v1/server/fastapi/app/__init__.py:L1-L1`
- `implemented`: user-facing API/runtime/package docs updated with explicit legacy-filepath notes where needed. `specs/api/v1/README.md:L1-L5`, `specs/api/v1/server/fastapi/README.md:L1-L5`, `specs/generated/README.md:L1-L14`, `specs/v1.0.0/README.md:L1-L3`
- `implemented`: Control Center docs now refer to the local backend as OF Platform while preserving legacy schema/env identifiers in operational commands. `apps/control-center/README.md:L3-L23`

## Risk Matrix

| Change area | Changed now / deferred | Reason | Compatibility risk |
| --- | --- | --- | --- |
| Onboarding pack, glossary, conceptual docs | changed now | prose-only clarification of model vs platform scope | low |
| Static/runtime API `info.title` and `info.description` | changed now | user-facing metadata; static and runtime kept aligned together | low to medium |
| API/package/generated-artifact READMEs | changed now | reader-facing naming only | low |
| Control Center README wording | changed now | local-ops prose only | low |
| `openapi-farm-rm.yaml` filename | deferred | file path is consumed by tests, docs, and release/package references | high |
| `FARM_RM_*` env vars and `farm_rm` DB defaults | deferred | local stack, scripts, CI, and persistence configuration depend on them | high |
| ontology namespaces / TTL labels / SQL identifiers | deferred | ontology IRIs and schema names are semantic contract surfaces | high |
| release-manifest artifact paths containing `Farm-RM` | deferred | release package indexing and bundle integrity depend on exact paths | medium to high |
| behavior-sensitive prompt templates and contract/test schema titles using legacy names | deferred | string changes may affect OCR behavior, tests, or client expectations beyond presentation | medium |
| `fa_rm` external issue-link alias in tooling | deferred | tied to external URL shape rather than in-repo product naming | medium |
