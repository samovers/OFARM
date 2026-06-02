# Glossary

Use this file as a lookup reference, not a summary page. When two similar names exist, the preferred meaning is listed first and the compatibility-sensitive alias is called out explicitly.

## Product and naming terms

### OFARM

Preferred for the semantic reference model: the base RM, archetypes, templates, profiles, ontology, SHACL, SQL semantics, and generated machine artifacts. Repo evidence also shows the model currently reaches beyond agronomy into compliance, reporting, inspection, evidence, and storage semantics, so the "Agronomy" label is a semantic-scope risk rather than proof of narrow scope. `specs/v0.1/Farm-RM-v0.1-Specification.md:L49-L119`, `specs/v0.1/ontology/farm-rm-v1.ttl:L14-L116`, `specs/v0.1/sql/migrations/0001_init_farm_rm_v1.sql:L32-L320`, `specs/generated/README.md:L1-L27`

### OF Platform

Preferred for the executing system: the FastAPI runtime, API surface, persistence/auth/reporting behavior, and the local Control Center operations plane in front of it. `specs/api/v1/server/fastapi/app/main.py:L225-L232`, `specs/api/v1/server/fastapi/app/main.py:L8877-L9101`, `apps/control-center/README.md:L1-L24`

### Legacy aliases

`Farm_RM`, `Farm-RM`, and `farm_rm` are compatibility-sensitive legacy identifiers. Keep them where filenames, namespaces, SQL identifiers, env vars, database names, contract filenames, manifests, or integration-sensitive symbols still require them. `fa_rm` appears in repo evidence only as a legacy external-repo alias pattern, not as the preferred product name. `specs/api/v1/openapi-farm-rm.yaml:L1-L5`, `apps/control-center/run_stack.sh:L17-L18`, `specs/v0.1/ontology/farm-rm-v1.ttl:L1-L7`, `tools/backend_request_concept_review.py:L168-L170`

## Semantic-core terms

### Reference model (RM)

The stable backbone layer beneath archetypes, templates, and profiles. `specs/v0.1/Farm-RM-v0.1-Specification.md:L49-L67`

### Archetype

A reusable domain concept defined in markdown and generated into FADL/JSON. Examples include plant taxonomy, crop species reference, and crop scouting observations. `specs/generated/README.md:L8-L24`, `specs/v0.8/archetypes/ADMIN.plant_taxon_reference.v1.md:L1-L25`, `specs/generated/fadl-manifest.json:L6-L18`

### Template

A workflow or use-case composition of archetypes. Example: crop health visit (IPM + nutrition). `specs/generated/README.md:L8-L24`, `specs/v0.8/templates/template-crop-health-visit-ipm-nutrition-v0_8.md:L1-L32`

### Template projection

A client/app-facing rule layer that maps template fields to archetype fields, crop filters, production-system filters, and value limits. `specs/v0.8/templates/projections/template-crop-health-visit-ipm-nutrition-v0_8.json:L1-L92`, `specs/api/v1/server/fastapi/tests/test_template_projection_contracts.py:L54-L93`

### CropInstance

A crop grown on a specific field/season context. Defined in the base RM ontology and SQL schema, and used across reporting/runtime. `specs/v0.1/ontology/farm-rm-v1.ttl:L18-L20`, `specs/v0.1/sql/migrations/0001_init_farm_rm_v1.sql:L99-L109`, `specs/api/v1/server/fastapi/app/reporting_control_pack.py:L873-L915`

### EvidenceRecord

Evidence attached to operations, reports, complaints, or traceability. Required by base RM execution semantics. `specs/v0.1/Farm-RM-v0.1-Specification.md:L103-L119`, `specs/v0.1/constraints/farm-rm-v1.shacl.ttl:L34-L42`, `specs/api/v1/server/fastapi/app/reporting_control_pack.py:L1021-L1063`

### GERK

Slovenian land parcel identifier in the base RM and reporting rows. `specs/v0.1/Farm-RM-v0.1-Specification.md:L68-L79`, `specs/v0.1/constraints/farm-rm-v1.shacl.ttl:L71-L76`, `specs/api/v1/server/fastapi/app/reporting_control_pack.py:L1078-L1107`

### Production status

Farm/crop/storage status with explicit organic-first priority and SI reporting mappings such as E/P/K. `specs/v0.1/Farm-RM-v0.1-Specification.md:L173-L180`, `specs/v0.1/ontology/farm-rm-v1.ttl:L120-L133`, `specs/api/v1/server/fastapi/app/reporting_control_pack.py:L1127-L1154`

## Operation and attestation layer

### Compliance profile

Planned additive key for operation logging and attestation work that composes `jurisdiction + scheme + scope + version`. The first concrete example in the new spec package is SI organic crops-only. `docs/implementation/logging-attestation-master-spec.md:L7-L20`, `docs/implementation/logging-attestation-master-spec.md:L161-L209`

### OperationCatalog

Implemented additive runtime registry of covered operation families, commit adapters, required anchors, and supported profiles. It complements the event-specific commit routes rather than replacing them. `specs/api/v1/server/fastapi/app/main.py:L53060-L53066`, `specs/api/v1/server/fastapi/tests/test_operation_drafts.py:L703-L705`, `specs/api/v1/server/fastapi/tests/test_openapi_contract_alignment.py:L1818-L1821`

### OperationProposal

Implemented additive ranked suggestion record for operation-logging intake from OCR, operator prompts, template hints, or manual selection. OCR parse can seed proposal content, and the runtime now exposes generic proposal create/fetch routes. `specs/api/v1/server/fastapi/app/main.py:L1716-L1793`, `specs/api/v1/server/fastapi/app/main.py:L53071-L53177`, `specs/api/v1/server/fastapi/tests/test_openapi_contract_alignment.py:L1805-L1823`

### OperationDraft

Implemented additive saveable mutable operation record that exists before immutable commit. The runtime exposes create/list/get/patch/commit draft surfaces, while final immutable execution still maps back to the authoritative event-specific field-op routes. `specs/api/v1/server/fastapi/app/main.py:L53180-L53879`, `specs/api/v1/server/fastapi/tests/test_openapi_contract_alignment.py:L1807-L1833`, `specs/api/v1/server/fastapi/tests/test_operation_drafts.py:L693-L700`

### OperationRequirementProfile

Planned per-operation, per-profile completeness contract covering save, attestation, and report-binding requirements. `docs/implementation/logging-attestation-master-spec.md:L47-L50`, `docs/implementation/logging-attestation-master-spec.md:L161-L209`

### OperationComplianceAssessment

Implemented additive profile-scoped evaluation of one committed operation against one requirement profile. It stays distinct from the append-only compliance fact routes, which capture supporting facts separately. `specs/api/v1/server/fastapi/app/main.py:L53884-L54310`, `specs/api/v1/server/fastapi/tests/test_openapi_contract_alignment.py:L1834-L1842`, `specs/api/v1/server/fastapi/tests/test_operation_drafts.py:L717-L930`

### ProductionUnitSeasonSlot

Planned lightweight planning/logging overlay that binds field, season, crop-context intent, and status before or alongside full planning. It is explicitly not a replacement for `Field` or `CropInstance`. `docs/implementation/logging-attestation-master-spec.md:L15-L18`, `docs/implementation/logging-attestation-master-spec.md:L123-L159`

### Operator attestation

Planned evidence type for operator-supplied declaration in the saveable logging flow. It is not the same thing as the profile-scoped lifecycle state `attested`. `docs/implementation/logging-attestation-master-spec.md:L84-L89`, `docs/implementation/logging-attestation-master-spec.md:L306-L338`

## Runtime and contract terms

### Advisor recommendation bundle

Runtime bundle returned by the advisor recommendation and bundle-fetch routes. It carries advisor decision surfaces, evidence/proof deltas, and persistence-aware lifecycle behavior for accept, override, and supersede flows. `specs/api/v1/server/fastapi/app/main.py:L21770-L21915`, `specs/api/v1/server/fastapi/tests/test_advisor_api.py:L289-L310`, `specs/api/v1/server/fastapi/tests/test_openapi_contract_alignment.py:L194-L264`

### Advisor objective profile

Named advisor objective-profile catalog entry backed by the authored advisor handoff bundle and exposed at `/v1/advisor/objective-profiles`. `docs/advisor/v1/README.md:L1-L13`, `specs/api/v1/server/fastapi/app/main.py:L21909-L21915`, `specs/api/v1/server/fastapi/tests/test_advisor_api.py:L308-L310`

### Capabilities endpoint

Runtime feature-discovery endpoint used for client gating. `specs/api/v1/server/fastapi/app/main.py:L223-L246`, `specs/api/v1/server/fastapi/app/main.py:L8877-L9081`

### OcrParseRequest / OcrParseResponse

Typed request/response contracts for OCR parsing with optional image input and proposal/provenance outputs. `specs/api/v1/server/fastapi/app/main.py:L1705-L1793`

### Control Center

Local launcher and diagnostic hub that fronts the backend for simulator/iPhone usage. `apps/control-center/README.md:L1-L18`, `apps/control-center/README.md:L119-L148`, `apps/control-center/run_stack.sh:L215-L280`

## Reference and reporting terms

### PlantTaxon

Reference entity for taxonomy ranks such as family/genus/species. `specs/v0.8/ontology/farm-rm-v1_7-plant-reference.ttl:L12-L39`, `specs/v0.8/archetypes/ADMIN.plant_taxon_reference.v1.md:L1-L25`

### CropSpeciesReference

Reference entity bridging botanical identity and agricultural grouping. `specs/v0.8/ontology/farm-rm-v1_7-plant-reference.ttl:L14-L40`, `specs/v0.8/archetypes/ADMIN.crop_species_reference.v1.md:L1-L30`

### CropVarietyReference

Reference entity for cultivars/varieties with season type, lifecycle, market class, register status, and raw source payload. `specs/v0.8/ontology/farm-rm-v1_7-plant-reference.ttl:L16-L49`, `specs/v0.8/archetypes/ADMIN.crop_variety_reference.v1.md:L1-L44`

### Reference snapshot

Immutable imported bundle of taxa/crops/varieties from an external source version. `specs/v0.8/sql/migrations/0082_v1_7_reference_snapshot_ingest.sql:L1-L72`, `specs/api/v1/server/fastapi/app/persistence.py:L13901-L14140`, `specs/api/v1/server/fastapi/app/main.py:L9663-L9770`

### MaterialLot

Lot of input material used in operations/inventory. Part of the base RM and traceability/reporting flows. `specs/v0.1/Farm-RM-v0.1-Specification.md:L83-L91`, `specs/v0.1/sql/migrations/0001_init_farm_rm_v1.sql:L121-L128`, `specs/api/v1/server/fastapi/app/reporting_control_pack.py:L1032-L1065`

### StorageLot

Lot of harvested/stored product used in traceability, inventory, and marketing sections. `specs/v0.1/Farm-RM-v0.1-Specification.md:L83-L91`, `specs/v0.1/sql/migrations/0001_init_farm_rm_v1.sql:L129-L136`, `specs/api/v1/server/fastapi/app/reporting_control_pack.py:L1993-L2106`

### RuleExecutionTrace

Trace or explanation record for rules/validation. Present in the base RM and used in compatibility/suitability request shapes. `specs/v0.1/Farm-RM-v0.1-Specification.md:L109-L112`, `specs/v0.1/ontology/farm-rm-v1.ttl:L28-L30`, `specs/api/v1/server/fastapi/app/main.py:L1905-L1923`

### Rulepack

Machine-readable regulatory ruleset for a profile/jurisdiction. `specs/v0.4/regulatory/rulepacks/organic-eu-2026.json:L1-L86`, `specs/v0.1/validation/bin/validate-claim.sh:L60-L93`

### Report pack

Registry asset describing a formal reporting package: authority, template, layout, sources, required fields, and export profile. `specs/v0.4/regulatory/report-packs/si-org-control-pack-2026.json:L1-L81`

### Layout map

Coordinate/structure mapping from a bound reporting payload to an official PDF form. `specs/v0.4/regulatory/report-layouts/si-2026-pdf-01.layout-map.v1.json:L1-L260`, `specs/api/v1/server/fastapi/tests/test_si_control_pack_official_form_pdf.py:L70-L99`

### Control pack

The Slovenia organic control recordbook/reporting bundle implemented in code and assets. `specs/v0.4/regulatory/report-packs/si-org-control-pack-2026.json:L1-L81`, `specs/api/v1/server/fastapi/app/reporting_control_pack.py:L644-L723`
