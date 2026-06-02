# Implementation Status

Use this file to separate proven repo surfaces from partial, planned, and still-unproven ones. It is intentionally blunt and should stay more literal than the rest of the pack.

## Status matrix

| Area | Status | Evidence | What that means |
| --- | --- | --- | --- |
| Base RM semantics | implemented | `specs/v0.1/Farm-RM-v0.1-Specification.md:L49-L180`, `specs/v0.1/ontology/farm-rm-v1.ttl:L14-L116`, `specs/v0.1/sql/migrations/0001_init_farm_rm_v1.sql:L32-L320` | The core domain model exists in narrative, ontology, SHACL, and SQL form. |
| Append-only/evidence discipline | implemented | `specs/v0.1/Farm-RM-v0.1-Specification.md:L113-L152`, `specs/v0.1/constraints/farm-rm-v1.shacl.ttl:L34-L58`, `specs/v0.1/sql/migrations/0001_init_farm_rm_v1.sql:L9-L28` | Lifecycle and evidence rules are not just aspirational. |
| Agronomy extension v1.7 | implemented | `specs/v0.8/ontology/farm-rm-v1_7-agronomy-archetypes.ttl:L8-L68`, `specs/v0.8/constraints/farm-rm-v1_7-agronomy-archetypes.shacl.ttl:L7-L220`, `specs/v0.8/sql/migrations/0016_v1_7_agronomy_archetypes.sql`, `specs/v0.8/sql/migrations/0080_v1_7_pesticide_application_event_v2.sql:L1-L52` | Agronomy content is backed by ontology, SHACL, and SQL migrations. |
| Plant reference/crop/variety model | implemented | `specs/v0.8/ontology/farm-rm-v1_7-plant-reference.ttl:L8-L101`, `specs/v0.8/constraints/farm-rm-v1_7-plant-reference.shacl.ttl:L5-L38`, `specs/v0.8/sql/migrations/0082_v1_7_reference_snapshot_ingest.sql:L1-L72`, `specs/v0.8/sql/migrations/0085_v1_7_plant_reference_variety_portal.sql:L1-L65` | There is real ingest/storage/search support for taxa, crops, and varieties. |
| Generated FADL/JSON artifact pipeline | implemented | `specs/generated/README.md:L6-L24`, `tools/generate_fadl_from_markdown.py:L1-L320`, `specs/generated/fadl-manifest.json:L1-L25` | Archetype/template markdown is turned into machine-readable artifacts. |
| FastAPI backend | implemented | `specs/api/v1/server/fastapi/app/main.py:L160-L205` | This is a large operational backend, not a schema stub. |
| Auth and tenancy | implemented | `specs/api/v1/server/fastapi/app/auth.py:L84-L181`, `specs/api/v1/server/fastapi/tests/test_api.py:L109-L135` | Farm-scoped JWT plus `X-Farm-URI` are enforced when auth is on. |
| Receipt import for inventory/seed purchases | implemented | `specs/api/v1/server/fastapi/app/main.py:L1134-L1157`, `specs/api/v1/server/fastapi/app/main.py:L1795-L1824`, `specs/api/v1/server/fastapi/app/main.py:L25324-L25440` | Client-ready import contract exists, including seed-specific fields. |
| OCR parse pipeline | implemented | `specs/api/v1/server/fastapi/app/main.py:L1705-L1793`, `specs/api/v1/server/fastapi/app/main.py:L9129-L9299`, `specs/api/v1/server/fastapi/tests/test_ai_ocr_slovenian_label_fallbacks.py:L50-L260` | OCR parse, metrics, and hybrid/deterministic behavior exist in code and tests. |
| Advisor recommendation runtime | implemented | `docs/advisor/v1/README.md:L1-L13`, `specs/api/v1/server/fastapi/app/main.py:L21458-L21464`, `specs/api/v1/server/fastapi/app/main.py:L21770-L21915`, `specs/api/v1/server/fastapi/tests/test_advisor_api.py:L289-L310` | Preview bundles, objective-profile discovery, and persistence-gated accept/override/supersede flows exist in runtime and tests. |
| Reference snapshot import/search | implemented | `specs/api/v1/server/fastapi/app/main.py:L9663-L9770`, `specs/api/v1/server/fastapi/app/main.py:L10759-L10980`, `specs/api/v1/server/fastapi/app/persistence.py:L13901-L14140` | Import and search are real runtime surfaces, not just spec ideas. |
| Template projection layer | implemented | `specs/v0.8/templates/projections/template-crop-health-visit-ipm-nutrition-v0_8.json:L1-L92`, `specs/api/v1/server/fastapi/tests/test_template_projection_contracts.py:L54-L93` | There is an app-facing projection contract on top of archetypes. |
| SI organic control-pack binder | implemented | `specs/v0.4/regulatory/report-packs/si-org-control-pack-2026.json:L1-L81`, `specs/api/v1/server/fastapi/app/reporting_control_pack.py:L644-L837`, `specs/api/v1/server/fastapi/app/reporting_control_pack.py:L845-L1015` | Reporting is a major implemented slice. |
| Official PDF rendering | implemented | `specs/api/v1/server/fastapi/tests/test_si_control_pack_official_form_pdf.py:L70-L159`, `specs/api/v1/server/fastapi/tests/test_si_control_pack_official_form_pdf.py:L206-L243` | Official-form rendering exists and is test-backed. |
| Local Control Center | implemented | `apps/control-center/README.md:L1-L18`, `apps/control-center/run_stack.sh:L17-L42`, `apps/control-center/server.py:L28-L65` | Local orchestration and diagnostics are real, productized tools. |
| Event-specific field-operation logging path | implemented | `specs/api/v1/server/fastapi/app/main.py:L25109-L28988`, `specs/api/v1/server/fastapi/app/persistence.py:L6172-L8261` | Operation logging already has strict commit routes and immutable persistence writers. |
| Crop-context ensure | implemented | `specs/api/v1/server/fastapi/app/main.py:L15444-L15452`, `specs/api/v1/server/fastapi/app/main.py:L21752-L21920`, `specs/api/v1/server/fastapi/tests/test_crop_context_ensure.py:L89-L376` | Missing crop context is handled by explicit pre-resolution rather than weakened commit semantics. |
| Compliance fact capture for attestation | implemented | `specs/api/v1/server/fastapi/app/main.py:L42017-L42960`, `specs/api/v1/server/fastapi/app/persistence.py:L14217-L15106`, `specs/api/v1/server/fastapi/tests/test_api.py:L13543-L13996` | The runtime already persists append-only jurisdiction facts, conversion timelines, parallel-production controls, and seed-sourcing exceptions. |
| Unified `OperationProposal` / `OperationDraft` / `OperationComplianceAssessment` layer | implemented | `specs/api/v1/server/fastapi/app/main.py:L47920-L49173`, `specs/api/v1/server/fastapi/app/persistence.py:L10358-L10854`, `specs/api/v1/server/fastapi/tests/test_openapi_contract_alignment.py:L1588-L1695`, `specs/api/v1/server/fastapi/tests/test_operation_drafts.py:L703-L1348` | The additive generic layer is now a runtime and static-contract surface, while event-specific `/v1/field-ops/*` routes remain commit authority. |
| Control Center attestation workbench | partial | `apps/control-center/README.md`, `apps/control-center/server.py:L3191-L3497`, `apps/control-center/tests/test_operation_review_workbench.py:L47-L181`, `specs/api/v1/server/fastapi/tests/test_operation_drafts.py:L1190-L1348` | Control Center now documents and proxies review queue/detail/action and report-binding backfill flows, but the surface is still local and proxy-first rather than a broader hosted workflow. |
| Static OpenAPI metadata freshness | implemented | `specs/api/v1/openapi-farm-rm.yaml:L1-L5`, `specs/api/v1/server/fastapi/app/main.py:L160-L178` | The static contract file and runtime app version now read as the same current release line. |
| Runtime/API naming alignment | implemented | `specs/api/v1/openapi-farm-rm.yaml:L1-L5`, `specs/api/v1/README.md:L1-L5`, `specs/api/v1/server/fastapi/README.md:L1-L5` | User-facing runtime docs now present the service as OF Platform while preserving legacy compatibility filenames where needed. |
| Artifact count reporting | implemented | `specs/generated/fadl-manifest.json:L1-L5`, `specs/v1.0.0/release-manifest.json:L136-L141` | The generated and release manifests currently align at `176` total artifacts; the remaining risk is over-reading that count as proof of full runtime coverage. |
| Coverage of every archetype by API/persistence | partial | `specs/generated/fadl-manifest.json:L1-L220`, `specs/v0.6/sql/bin-run-v1_6-migrations.sh:L20-L106`, `specs/api/v1/server/fastapi/app/main.py:L143-L152` | Many archetypes are present, but there is no single repo file proving one-to-one runtime coverage for all of them. |
| US regulatory/reporting support | unknown | `specs/v1.0.0/version-map.md:L20-L37`, `specs/v0.4/regulatory/report-packs/si-org-control-pack-2026.json:L1-L81` | No inspected runtime/report-pack asset in this pass established active US reporting support. |

## Implemented now

- Core RM identity, lifecycle, and evidence discipline.
- Plant reference planning/profile/readiness plus snapshot import/search.
- Inventory receipt import and OCR parse.
- SI crops-only organic reporting and official PDF rendering.
- Event-specific field-operation logging plus crop-context ensure.
- Append-only compliance fact capture for attestation and reporting.
- Control Center local stack path and local governance/workbench proxy surfaces.

## Partial or constrained

- Reporting strength remains strongest in the SI crops-only line, not as a general multi-jurisdiction guarantee. `specs/v0.4/regulatory/report-packs/si-org-control-pack-2026.json:L29-L35`, `docs/ai/indexes/drift-register.yaml`
- No-DB mode still yields incomplete or example-driven responses on some surfaces. `specs/api/v1/server/fastapi/app/reporting_control_pack.py:L810-L837`, `specs/api/v1/server/fastapi/app/main.py:L11960-L12040`
- The additive operation-draft layer is implemented, but its long-term completeness versus SQL migration coverage still needs care. `specs/api/v1/server/fastapi/tests/test_operation_drafts.py:L703-L1348`, `docs/implementation/logging-attestation-master-spec.md:L253-L338`
- Control Center workbench behavior remains local and proxy-first rather than a proven hosted workflow. `docs/architecture/adr/0004-control-center-local-internal-workbench.md`, `apps/control-center/tests/test_operation_review_workbench.py:L47-L181`

## Planned but not yet present

- `OperationRequirementProfile` remains a planned completeness contract rather than a proven runtime object. `docs/implementation/logging-attestation-master-spec.md:L47-L50`, `docs/ai/onboarding/90-glossary.md`
- `ProductionUnitSeasonSlot` remains a planned planning/logging overlay, not a shipped semantic or runtime anchor. `docs/implementation/logging-attestation-master-spec.md:L123-L159`, `docs/ai/onboarding/90-glossary.md`
- Stable package policy still reserves future major or minor package roots beyond the current `v1.0.0` line. `specs/v1.0.0/version-map.md:L20-L37`

## Claims in docs not yet matched in code

- The aligned `176` artifact count is real metadata, but it should not be read as proof of full runtime or persistence coverage. `specs/generated/fadl-manifest.json:L1-L5`, `specs/v1.0.0/release-manifest.json:L136-L141`, `docs/ai/indexes/drift-register.yaml`
- Broader non-SI or non-crops reporting support should not be inferred from the current pack. `specs/v0.4/regulatory/report-packs/si-org-control-pack-2026.json:L29-L35`, `docs/ai/indexes/drift-register.yaml`
- Local Control Center review-workbench surfaces should not be described as a finished hosted approval engine. `apps/control-center/server.py:L3191-L3497`, `docs/ai/indexes/drift-register.yaml`

## Architectural debt and open debt trackers

- Shell validators from older spec streams still sit in the runtime path, which keeps a portability and architecture question open. `specs/api/v1/server/fastapi/app/main.py:L143-L152`, `docs/ai/onboarding/80-open-questions-and-risks.md`
- The base RM expects evidence-bearing immutable execution facts, while current runtime commit paths satisfy that minimally with generated `api_payload` evidence. `specs/v0.1/Farm-RM-v0.1-Specification.md:L113-L152`, `specs/api/v1/server/fastapi/app/persistence.py:L6259-L6278`
- The strongest current debt trackers are the drift register and implementation decision ledgers rather than inline TODO/FIXME clusters promoted into this onboarding pack. `docs/ai/indexes/drift-register.yaml`, `docs/implementation/logging-attestation-open-decisions.md`, `docs/ai/onboarding/80-open-questions-and-risks.md`

## Safe to build on immediately

- Core RM identities, lifecycle rules, and evidence discipline.
- Plant reference source planning/profile/readiness plus snapshot import/search.
- Inventory receipt import.
- OCR parse contract.
- SI crops-only organic reporting and PDF rendering.
- Event-specific field-operation logging plus crop-context ensure.
- Append-only compliance fact capture for attestation and reporting.
- Control Center local stack path.

## Do not assume without checking

- Full runtime coverage for every generated archetype/template.
- Any non-SI regulatory profile beyond what rulepacks/report packs explicitly show.
- That every additive operation-draft family in runtime/tests is already reconciled with canonical SQL migration constraints.
- That Control Center README/operator docs fully describe the implemented review-workbench proxy surface.
