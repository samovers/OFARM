# Semantic Core

Use this doc when the question is about canonical domain meaning: what the core entities are, where the semantic rules live, and which model-level anchors are stable enough to design against. For runtime topology and endpoint contracts, use [30-runtime-architecture.md](30-runtime-architecture.md) and [40-api-and-data-contracts.md](40-api-and-data-contracts.md).

## What this layer owns

- `implemented`: the base OFARM reference model is explicitly layered into RM, archetypes, templates, profiles, and execution bindings. `specs/v0.1/Farm-RM-v0.1-Specification.md:L49-L67`
- `implemented`: the same base model is carried in four parallel source forms:
  - narrative spec: `specs/v0.1/Farm-RM-v0.1-Specification.md:L68-L180`
  - OWL ontology: `specs/v0.1/ontology/farm-rm-v1.ttl:L14-L116`
  - SHACL constraints: `specs/v0.1/constraints/farm-rm-v1.shacl.ttl:L5-L76`
  - SQL persistence: `specs/v0.1/sql/migrations/0001_init_farm_rm_v1.sql:L32-L320`
- `implemented`: current extension authority is concentrated in `v0.8`, especially plant reference, agronomy archetypes, and organic-compliance additions. `specs/v0.8/ontology/farm-rm-v1_7-plant-reference.ttl:L8-L101`, `specs/v0.8/ontology/farm-rm-v1_7-agronomy-archetypes.ttl:L8-L68`, `specs/v0.8/ontology/farm-rm-v1_7-organic-compliance-eu-si-crops-only.ttl`

## Base entities

| Entity group | What it covers | Primary evidence | Status |
| --- | --- | --- | --- |
| Farm structure | `Farm`, `Field`, `ParcelBlock`, `GERK` | `specs/v0.1/Farm-RM-v0.1-Specification.md:L68-L79`, `specs/v0.1/ontology/farm-rm-v1.ttl:L14-L20`, `specs/v0.1/sql/migrations/0001_init_farm_rm_v1.sql:L61-L98` | implemented |
| Crop scope | `CropInstance`, crop type links, production status | `specs/v0.1/Farm-RM-v0.1-Specification.md:L79-L90`, `specs/v0.1/ontology/farm-rm-v1.ttl:L18-L20`, `specs/v0.1/sql/migrations/0001_init_farm_rm_v1.sql:L99-L109` | implemented |
| Resources and lots | `Resource`, `MaterialLot`, `StorageLot` | `specs/v0.1/Farm-RM-v0.1-Specification.md:L83-L91`, `specs/v0.1/ontology/farm-rm-v1.ttl:L20-L22`, `specs/v0.1/sql/migrations/0001_init_farm_rm_v1.sql:L110-L136` | implemented |
| Planning | `OperationTemplate`, `PlannedOperation`, constraints, time windows | `specs/v0.1/Farm-RM-v0.1-Specification.md:L91-L102`, `specs/v0.1/ontology/farm-rm-v1.ttl:L22-L28`, `specs/v0.1/sql/migrations/0001_init_farm_rm_v1.sql:L140-L200` | implemented |
| Execution | `ExecutedOperation`, evidence linkage, event records | `specs/v0.1/Farm-RM-v0.1-Specification.md:L99-L112`, `specs/v0.1/ontology/farm-rm-v1.ttl:L24-L30`, `specs/v0.1/sql/migrations/0001_init_farm_rm_v1.sql:L204-L269` | implemented |
| Compliance and governance | claims, inspections, certifications, rules | `specs/v0.1/Farm-RM-v0.1-Specification.md:L103-L112`, `specs/v0.1/sql/migrations/0001_init_farm_rm_v1.sql:L271-L320` | implemented |

## Stable semantic rules

- `implemented`: URI-first identity is a first-class rule. `specs/v0.1/Farm-RM-v0.1-Specification.md:L120-L130`
- `implemented`: append-only semantics are enforced both conceptually and in SQL triggers that block update/delete. `specs/v0.1/Farm-RM-v0.1-Specification.md:L131-L152`, `specs/v0.1/sql/migrations/0001_init_farm_rm_v1.sql:L9-L28`
- `implemented`: executed operations are expected to carry evidence. This is present in the conceptual rules, SHACL, and SQL trigger logic. `specs/v0.1/Farm-RM-v0.1-Specification.md:L113-L119`, `specs/v0.1/constraints/farm-rm-v1.shacl.ttl:L34-L42`, `specs/v0.1/sql/migrations/0001_init_farm_rm_v1.sql:L18-L28`
- `contradiction between docs and code`: the runtime currently satisfies that evidence-bearing execution rule minimally by auto-generating `api_payload` evidence at commit time; this preserves append-only semantics but does not itself prove profile-complete regulatory readiness. `specs/api/v1/server/fastapi/app/persistence.py:L6259-L6278`, `specs/api/v1/server/fastapi/app/persistence.py:L8024-L8043`, `specs/api/v1/server/fastapi/app/persistence.py:L8189-L8208`
- `implemented`: organic-first profile priority is explicit in the base model and carried into current packaging. `specs/v0.1/Farm-RM-v0.1-Specification.md:L173-L180`, `specs/v1.0.0/release-manifest.json:L206-L210`

## Plant reference extension

- `implemented`: plant taxonomy, crop species reference, and crop variety reference are modeled as explicit ontology classes. `specs/v0.8/ontology/farm-rm-v1_7-plant-reference.ttl:L12-L49`
- `implemented`: controlled schemes exist for taxon rank, crop type, season type, life cycle, and variety status. `specs/v0.8/ontology/farm-rm-v1_7-plant-reference.ttl:L50-L101`
- `implemented`: SHACL enforces crop type enumerations and variety date consistency. `specs/v0.8/constraints/farm-rm-v1_7-plant-reference.shacl.ttl:L5-L38`
- `implemented`: the human-readable archetypes keep deployment-facing fields like localized labels and raw portal payload preservation explicit. `specs/v0.8/archetypes/ADMIN.plant_taxon_reference.v1.md:L1-L25`, `specs/v0.8/archetypes/ADMIN.crop_species_reference.v1.md:L1-L30`, `specs/v0.8/archetypes/ADMIN.crop_variety_reference.v1.md:L1-L44`

## Agronomy and workflow extension

- `implemented`: the v1.7 agronomy ontology adds a broad extension family for crop stage, scouting, remote sensing, soil, climate hazards, adaptation, seed health, diagnostics, irrigation, harvest, storage, warehouse quality, cover crops, tillage, and equipment integrity or maintenance. `specs/v0.8/ontology/farm-rm-v1_7-agronomy-archetypes.ttl:L8-L68`
- `implemented`: SHACL rules are substantive rather than nominal. They encode value domains, numeric bounds, temporal ordering, and cross-field dependencies such as trap exposure ordering, scouting severity requirements, remote-sensing index bounds, and sensor-unit consistency. `specs/v0.8/constraints/farm-rm-v1_7-agronomy-archetypes.shacl.ttl:L7-L30`, `specs/v0.8/constraints/farm-rm-v1_7-agronomy-archetypes.shacl.ttl:L32-L70`, `specs/v0.8/constraints/farm-rm-v1_7-agronomy-archetypes.shacl.ttl:L72-L94`, `specs/v0.8/constraints/farm-rm-v1_7-agronomy-archetypes.shacl.ttl:L96-L185`
- `implemented`: SQL migrations mirror the extension into append-only tables such as `pesticide_application_event`, `disease_control_operation`, `crop_scouting_signs_observation`, `soil_amendment_plan_ext`, and reference ingest tables. `specs/v0.8/sql/migrations/0075_v1_7_crop_scouting_signs_observation_v2.sql:L1-L76`, `specs/v0.8/sql/migrations/0079_v1_7_soil_amendment_plan_ext.sql:L1-L53`, `specs/v0.8/sql/migrations/0080_v1_7_pesticide_application_event_v2.sql:L1-L52`, `specs/v0.8/sql/migrations/0081_v1_7_disease_control_operation_v2.sql:L1-L37`, `specs/v0.8/sql/migrations/0082_v1_7_reference_snapshot_ingest.sql:L1-L72`

## Archetypes, templates, and projections

- `implemented`: markdown archetypes and templates are the human authoring layer; generated FADL and JSON are derivative artifacts. `specs/generated/README.md:L6-L24`, `specs/generated/fadl-manifest.json:L1-L25`
- `implemented`: template projections are the app-facing field-rule layer on top of archetype content. The crop-health visit projection is a representative example that joins multiple archetypes, crop-context filters, production-system rules, and numeric value limits. `specs/v0.8/templates/template-crop-health-visit-ipm-nutrition-v0_8.md:L1-L32`, `specs/v0.8/templates/projections/template-crop-health-visit-ipm-nutrition-v0_8.json:L1-L92`
- `implemented`: projection contracts are tested against archetype JSON and vocabulary instead of being treated as free-standing UI lore. `specs/api/v1/server/fastapi/tests/test_template_projection_contracts.py:L54-L93`

## Safe semantic anchors for design work

- Base identity, lifecycle, and append-only evidence semantics.
- `Field`, `CropInstance`, and immutable `ExecutedOperation` as the safest anchors for new logging or attestation work. The additive draft and assessment layer is intentionally built around them, not instead of them. `docs/implementation/logging-attestation-master-spec.md:L22-L121`
- Plant taxonomy, crop species, and crop variety reference semantics.
- Evidence-centric linkage between operations, compliance, and reporting.
- The projection layer as a separate, app-facing contract above archetype meaning.
- Vocabulary, SHACL, and drift-guard patterns. `specs/api/v1/server/fastapi/tests/test_value_set_drift_guards.py:L17-L94`
