# Farm-RM v0.8 Agronomy Archetypes and Templates Specification (Draft)

## 1. Objective

Define a practical, scientifically grounded set of agronomy archetypes and templates that supports:

1. Day-to-day crop monitoring and agronomic decision-making.
2. Organic-first farm management and compliance evidence capture.
3. Interoperable data exchange across FMIS, mobile apps, advisory tools, sensors, and machinery stacks.
4. Crop-specific data entry and analysis UX where irrelevant fields are hidden and value limits are contextual.

This specification is **openEHR-inspired**:

1. A stable reference model (Farm-RM core) carries generic structures.
2. Archetypes define reusable agronomic concepts (measurements, assessments, actions).
3. Templates constrain and compose archetypes for specific workflows and crops.

## 2. Scope

### 2.1 In scope

1. Arable and mixed crop farms (field operations, scouting, irrigation, fertilization, crop protection, harvest, storage).
2. Core agronomy domains:
   - soil and fertility,
   - weather and crop microclimate,
   - crop stage and establishment,
   - pests/diseases/weeds (IPM),
   - water management,
   - post-harvest quality and storage continuity.
3. Organic-first operations and risk management (contamination risk, cleanout, mechanical weed control, evidence).
4. Crop-specific UX constraints as template projections (hide irrelevant fields; apply crop/crop-stage value ranges).

### 2.2 Out of scope (for this pack)

1. Livestock.
2. Full accounting, payroll, tax ledgers (finance-ready hooks remain in core RM; accounting is an extension).
3. Precision agronomy algorithm internals (models can exist outside; Farm-RM standardizes inputs/outputs and evidence).
4. Proprietary breeder datasets beyond mapped outputs.

## 3. Domain Terminologies and Codes (Normative Guidance)

Farm-RM is URI-first. Archetypes SHOULD prefer controlled codes/URIs over free text.

### 3.1 Crop stage coding

1. Crop stage SHOULD be recorded using **BBCH codes** (`bbchCode`).
2. Templates MAY restrict allowed BBCH ranges for a workflow (example: pre-emergence actions only before emergence).

### 3.2 Pest/disease/weed organism coding

1. Pest/disease/weed identifiers SHOULD use **EPPO** codes where available:
   - pathogens and pests (`suspectedPathogenCode`, `pestCode`),
   - weeds (`weedCode`),
   - host plants (crop species/variety) when practical.
2. Templates MAY constrain which organism codes are relevant for a crop and region.

### 3.3 Soil context coding

1. Soil texture and drainage SHOULD be captured using controlled enumerations:
   - `soilTextureClass` (for example: sand/loamy_sand/sandy_loam/.../clay),
   - `drainageClass` (for example: well/moderate/poor).
2. Templates MAY restrict acceptable ranges (example: `phMin/phMax` bounds and consistency).

### 3.4 Units and measurement method codes

1. Observations MUST carry units. For analyte panels:
   - `resultUnit` MUST be specified per analyte.
2. Every measurement MUST carry a `methodCode` or `sensorRef` where possible.
3. Templates SHOULD restrict units to a small set to reduce ambiguity (example: `mm`, `C`, `m/s`, `%`, `kg/ha`).

## 4. Archetype Modeling Principles (openEHR analogy)

Archetypes should be:

1. **Reusable**: one concept, measured/recorded repeatedly across farms.
2. **Scientifically interpretable**: include method/context to make results comparable.
3. **Evidence-ready**: support audit trails (who/when/how).
4. **Composable**: easy to include in multiple templates.

### 4.1 Archetype families

1. `OBSERVATION.*`: raw measured or observed facts (soil moisture, stand count, scouting signs).
2. `EVALUATION.*`: interpreted states or assessments (disease case assessment, irrigation need).
3. `INSTRUCTION.*`: intent/plans (irrigation plan, IPM plan, soil amendment plan).
4. `ACTION.*`: executed interventions (planting, irrigation, fertilizer, pesticide, mechanical weeding).
5. `ADMIN.*`: compliance/operational governance artifacts (case files, competency gates, tenancy constraints).

### 4.2 Minimum required metadata (recommended baseline)

Archetypes SHOULD include:

1. `subject` (field/crop instance/lot/equipment).
2. `time` (observedAt/measuredAt/startTime/endTime).
3. `method` (methodCode/sensorRef/assayMethod).
4. `qualityFlag` (good/suspect/estimated).
5. `sourceRefs` (links to lab report, device, advisory bulletin) when applicable.

Templates can tighten these requirements by crop, jurisdiction, and production system.

## 5. Agronomy Archetype Catalog (Relevant Set)

This catalog consolidates the current Farm-RM archetypes across `v0.2..v0.7` that are most relevant to agronomy.

### 5.1 Soil and fertility

Existing archetypes:

1. `OBSERVATION.soil_sample_collection.v1` (`specs/v0.2/archetypes/OBSERVATION.soil_sample_collection.v1.md`)
2. `OBSERVATION.soil_lab_panel.v1` (`specs/v0.2/archetypes/OBSERVATION.soil_lab_panel.v1.md`)
3. `EVALUATION.soil_fertility_status.v1` (`specs/v0.2/archetypes/EVALUATION.soil_fertility_status.v1.md`)
4. `EVALUATION.soil_fertility_status.v2` (`specs/v0.8/archetypes/EVALUATION.soil_fertility_status.v2.md`)
5. `EVALUATION.soil_constraint_risk.v1` (`specs/v0.2/archetypes/EVALUATION.soil_constraint_risk.v1.md`)
6. `EVALUATION.soil_constraint_risk.v2` (`specs/v0.8/archetypes/EVALUATION.soil_constraint_risk.v2.md`)
7. `INSTRUCTION.soil_amendment_plan.v1` (`specs/v0.2/archetypes/INSTRUCTION.soil_amendment_plan.v1.md`)
8. `ACTION.soil_amendment_application.v1` (`specs/v0.2/archetypes/ACTION.soil_amendment_application.v1.md`)
9. `ACTION.soil_amendment_application.v2` (`specs/v0.8/archetypes/ACTION.soil_amendment_application.v2.md`)
10. `OBSERVATION.soil_sensor_series.v1` (`specs/v0.2/archetypes/OBSERVATION.soil_sensor_series.v1.md`)
11. `OBSERVATION.soil_moisture_profile.v1` (`specs/v0.5/archetypes/OBSERVATION.soil_moisture_profile.v1.md`)
12. `OBSERVATION.soil_temperature_profile.v1` (`specs/v0.5/archetypes/OBSERVATION.soil_temperature_profile.v1.md`)
13. `OBSERVATION.soil_sensor_series.v2` (`specs/v0.8/archetypes/OBSERVATION.soil_sensor_series.v2.md`)

Recommended analyte coverage policy for templates:

1. MUST support at least: pH, organic matter, total N, available P, available K, EC/salinity.
2. SHOULD support optional micronutrients: Mg, Ca, S, B, Zn, Mn, Cu, Fe, plus CEC when provided by labs.

### 5.2 Weather, microclimate, and hazards

Existing archetypes:

1. `OBSERVATION.agrometeorological_station_observation.v1` (`specs/v0.5/archetypes/OBSERVATION.agrometeorological_station_observation.v1.md`)
2. `OBSERVATION.agrometeorological_station_observation.v2` (`specs/v0.8/archetypes/OBSERVATION.agrometeorological_station_observation.v2.md`)
3. `OBSERVATION.leaf_wetness_duration.v1` (`specs/v0.5/archetypes/OBSERVATION.leaf_wetness_duration.v1.md`)
4. `OBSERVATION.climate_hazard_profile.v1` (`specs/v0.4/archetypes/OBSERVATION.climate_hazard_profile.v1.md`)
5. `OBSERVATION.climate_hazard_profile.v2` (`specs/v0.8/archetypes/OBSERVATION.climate_hazard_profile.v2.md`)
6. `OBSERVATION.forecast_scenario_bundle.v1` (`specs/v0.4/archetypes/OBSERVATION.forecast_scenario_bundle.v1.md`)
7. `OBSERVATION.forecast_scenario_bundle.v2` (`specs/v0.8/archetypes/OBSERVATION.forecast_scenario_bundle.v2.md`)

### 5.3 Crop establishment, stage, and adaptation

Existing archetypes:

1. `OBSERVATION.crop_stage_assessment.v1` (`specs/v0.5/archetypes/OBSERVATION.crop_stage_assessment.v1.md`)
2. `ACTION.planting_event.v1` (`specs/v0.7/archetypes/ACTION.planting_event.v1.md`)
3. `OBSERVATION.crop_stand_count.v1` (`specs/v0.7/archetypes/OBSERVATION.crop_stand_count.v1.md`)
4. `EVALUATION.replant_need_assessment.v1` (`specs/v0.7/archetypes/EVALUATION.replant_need_assessment.v1.md`)
5. `OBSERVATION.field_pedoclimatic_profile.v1` (`specs/v0.3/archetypes/OBSERVATION.field_pedoclimatic_profile.v1.md`)
6. `OBSERVATION.field_pedoclimatic_profile.v2` (`specs/v0.8/archetypes/OBSERVATION.field_pedoclimatic_profile.v2.md`)
7. `OBSERVATION.crop_adaptation_profile.v1` (`specs/v0.4/archetypes/OBSERVATION.crop_adaptation_profile.v1.md`)
8. `OBSERVATION.crop_adaptation_profile.v2` (`specs/v0.8/archetypes/OBSERVATION.crop_adaptation_profile.v2.md`)

Seed/variety selection related archetypes:

1. `ADMIN.variety_evidence_package.v1` (`specs/v0.3/archetypes/ADMIN.variety_evidence_package.v1.md`)
2. `ADMIN.variety_evidence_package.v2` (`specs/v0.8/archetypes/ADMIN.variety_evidence_package.v2.md`)
3. `INSTRUCTION.variety_selection_plan.v1` (`specs/v0.3/archetypes/INSTRUCTION.variety_selection_plan.v1.md`)
4. `INSTRUCTION.variety_selection_plan.v2` (`specs/v0.8/archetypes/INSTRUCTION.variety_selection_plan.v2.md`)
5. `EVALUATION.variety_field_suitability.v1` (`specs/v0.3/archetypes/EVALUATION.variety_field_suitability.v1.md`)
6. `EVALUATION.variety_risk_profile.v1` (`specs/v0.3/archetypes/EVALUATION.variety_risk_profile.v1.md`)
7. `OBSERVATION.seed_lot_quality_health.v1` (`specs/v0.3/archetypes/OBSERVATION.seed_lot_quality_health.v1.md`)
8. `OBSERVATION.seed_lot_quality_health.v2` (`specs/v0.8/archetypes/OBSERVATION.seed_lot_quality_health.v2.md`)
9. `OBSERVATION.variety_trial_result.v1` (`specs/v0.3/archetypes/OBSERVATION.variety_trial_result.v1.md`)
10. `OBSERVATION.variety_trial_result.v2` (`specs/v0.8/archetypes/OBSERVATION.variety_trial_result.v2.md`)
11. `EVALUATION.suitability_assessment.v2` (`specs/v0.8/archetypes/EVALUATION.suitability_assessment.v2.md`)
12. `EVALUATION.seed_field_compatibility.v2` (`specs/v0.8/archetypes/EVALUATION.seed_field_compatibility.v2.md`)
13. `EVALUATION.variety_risk_profile.v2` (`specs/v0.8/archetypes/EVALUATION.variety_risk_profile.v2.md`)
14. `EVALUATION.variety_field_suitability.v2` (`specs/v0.8/archetypes/EVALUATION.variety_field_suitability.v2.md`)

### 5.4 Pests, diseases, weeds (IPM)

Existing archetypes:

1. `OBSERVATION.crop_scouting_signs.v1` (`specs/v0.2/archetypes/OBSERVATION.crop_scouting_signs.v1.md`)
2. `OBSERVATION.crop_scouting_signs.v2` (`specs/v0.8/archetypes/OBSERVATION.crop_scouting_signs.v2.md`)
3. `OBSERVATION.diagnostic_test_result.v1` (`specs/v0.2/archetypes/OBSERVATION.diagnostic_test_result.v1.md`)
4. `EVALUATION.disease_case_assessment.v1` (`specs/v0.2/archetypes/EVALUATION.disease_case_assessment.v1.md`)
5. `EVALUATION.disease_case_assessment.v2` (`specs/v0.8/archetypes/EVALUATION.disease_case_assessment.v2.md`)
6. `EVALUATION.disease_risk_forecast.v1` (`specs/v0.2/archetypes/EVALUATION.disease_risk_forecast.v1.md`)
7. `EVALUATION.disease_risk_forecast.v2` (`specs/v0.8/archetypes/EVALUATION.disease_risk_forecast.v2.md`)
8. `INSTRUCTION.ipm_control_plan.v1` (`specs/v0.2/archetypes/INSTRUCTION.ipm_control_plan.v1.md`)
9. `INSTRUCTION.ipm_control_plan.v2` (`specs/v0.8/archetypes/INSTRUCTION.ipm_control_plan.v2.md`)
10. `ACTION.disease_control_operation.v1` (`specs/v0.2/archetypes/ACTION.disease_control_operation.v1.md`)
11. `ACTION.disease_control_operation.v2` (`specs/v0.8/archetypes/ACTION.disease_control_operation.v2.md`)
12. `OBSERVATION.weed_pressure_assessment.v1` (`specs/v0.7/archetypes/OBSERVATION.weed_pressure_assessment.v1.md`)
13. `ACTION.mechanical_weeding_event.v1` (`specs/v0.7/archetypes/ACTION.mechanical_weeding_event.v1.md`)

Severity guidance:

1. Archetypes SHOULD support both ordinal severity (low/medium/high) and quantitative measures where possible
   (example: `coveragePct`, `leafAreaAffectedPct`).
2. Templates SHOULD tie severity scales to crop stage and observation method (visual estimate vs trap count vs lab test).

### 5.5 Nutrients and water management

Existing archetypes:

1. `ACTION.fertilizer_application_event.v1` (`specs/v0.5/archetypes/ACTION.fertilizer_application_event.v1.md`)
2. `EVALUATION.nutrient_deficiency_assessment.v1` (`specs/v0.5/archetypes/EVALUATION.nutrient_deficiency_assessment.v1.md`)
3. `ACTION.irrigation_event.v1` (`specs/v0.5/archetypes/ACTION.irrigation_event.v1.md`)
4. `INSTRUCTION.irrigation_event_plan.v1` (`specs/v0.5/archetypes/INSTRUCTION.irrigation_event_plan.v1.md`)
5. `EVALUATION.irrigation_need_assessment.v1` (`specs/v0.5/archetypes/EVALUATION.irrigation_need_assessment.v1.md`)
6. `OBSERVATION.water_allocation_and_use.v1` (`specs/v0.4/archetypes/OBSERVATION.water_allocation_and_use.v1.md`)

### 5.6 Crop protection and compliance-critical interventions

Existing archetypes:

1. `ACTION.pesticide_application_event.v1` (`specs/v0.5/archetypes/ACTION.pesticide_application_event.v1.md`)
2. `ACTION.pesticide_application_event.v2` (`specs/v0.8/archetypes/ACTION.pesticide_application_event.v2.md`)
3. `ADMIN.phytosanitary_case_file.v1` (`specs/v0.2/archetypes/ADMIN.phytosanitary_case_file.v1.md`)
4. `ADMIN.phytosanitary_case_file.v2` (`specs/v0.8/archetypes/ADMIN.phytosanitary_case_file.v2.md`)
5. `ADMIN.soil_compliance_evidence.v1` (`specs/v0.2/archetypes/ADMIN.soil_compliance_evidence.v1.md`)
6. `ADMIN.soil_compliance_evidence.v2` (`specs/v0.8/archetypes/ADMIN.soil_compliance_evidence.v2.md`)

Notes:

1. Organic-first deployments SHOULD treat chemical crop-protection events as higher-risk and more constrained.
2. Templates SHOULD require weather context (wind) and buffer-zone metadata for drift/contamination risk workflows.

### 5.7 Harvest, storage, and quality

Existing archetypes:

1. `ACTION.harvest_event.v1` (`specs/v0.5/archetypes/ACTION.harvest_event.v1.md`)
2. `OBSERVATION.storage_quality_conditions.v1` (`specs/v0.4/archetypes/OBSERVATION.storage_quality_conditions.v1.md`)
3. `OBSERVATION.warehouse_product_sample_collection.v1` (`specs/v0.5/archetypes/OBSERVATION.warehouse_product_sample_collection.v1.md`)
4. `OBSERVATION.warehouse_product_quality_panel.v1` (`specs/v0.5/archetypes/OBSERVATION.warehouse_product_quality_panel.v1.md`)
5. `OBSERVATION.storage_bin_condition_snapshot.v1` (`specs/v0.7/archetypes/OBSERVATION.storage_bin_condition_snapshot.v1.md`)
6. `ACTION.storage_bin_aeration_event.v1` (`specs/v0.7/archetypes/ACTION.storage_bin_aeration_event.v1.md`)
7. `OBSERVATION.delivery_ticket_record.v1` (`specs/v0.7/archetypes/OBSERVATION.delivery_ticket_record.v1.md`)

### 5.8 Equipment context relevant to agronomy (not telematics-specific)

Existing archetypes:

1. `OBSERVATION.equipment_capability_profile.v1` (`specs/v0.4/archetypes/OBSERVATION.equipment_capability_profile.v1.md`)
2. `OBSERVATION.equipment_capability_profile.v2` (`specs/v0.8/archetypes/OBSERVATION.equipment_capability_profile.v2.md`)
3. `EVALUATION.equipment_field_suitability.v1` (`specs/v0.4/archetypes/EVALUATION.equipment_field_suitability.v1.md`)
4. `EVALUATION.equipment_field_suitability.v2` (`specs/v0.8/archetypes/EVALUATION.equipment_field_suitability.v2.md`)
5. `ACTION.equipment_maintenance_event.v1` (`specs/v0.7/archetypes/ACTION.equipment_maintenance_event.v1.md`)
6. `ACTION.equipment_cleanout_event.v1` (`specs/v0.7/archetypes/ACTION.equipment_cleanout_event.v1.md`)

## 6. Templates (Workflow Compositions)

Templates are the primary mechanism for crop-specific UX, field relevance, and value limits.

### 6.1 Soil fertility monitoring cycle (v0.2)

Template:

1. `Template: Soil Fertility Monitoring Cycle v1.1`
   - `specs/v0.2/templates/template-soil-fertility-monitoring-cycle-v1_1.md`

Expected composition:

1. Soil sample collection.
2. Soil lab panel results.
3. Soil fertility status evaluation.
4. Soil amendment plan.
5. Amendment application event(s).

Crop-specific projection guidance:

1. Cereals: emphasize N, P, K, pH, OM.
2. Horticulture/vineyards: add micronutrient panel and EC emphasis.
3. Organic: require amendment source and compliance evidence links.

### 6.2 Variety/seed selection templates (v0.3)

Templates:

1. `Template: Variety Selection (Granular) v1.2`
2. `Template: Variety Selection (Sparse Seller) v1.2`

Projection guidance:

1. If seller-only: hide unsupported trait fields and downgrade confidence deterministically.
2. If trials exist: require evidence package links and show full trait vector.

### 6.3 IPM disease case management template (v0.2)

Template:

1. `Template: Disease Case Management (IPM) v1.1`

Expected composition:

1. Structured scouting signs.
2. Diagnostic test result(s).
3. Disease case assessment.
4. Risk forecast.
5. IPM control plan.
6. Control operation execution(s).

Crop-specific projection guidance:

1. Restrict relevant pathogen/pest code sets by crop.
2. Restrict BBCH stage windows for certain interventions.
3. Organic: present non-chemical actions first (mechanical, cultural, biological) and require justification for chemical use.

### 6.4 Irrigation decision visit template (v0.5)

Template:

1. `Template: Irrigation Decision Visit v1.4`

Expected composition:

1. Soil moisture profile.
2. Weather station summary.
3. Crop stage.
4. Irrigation need assessment.
5. Irrigation plan and (optionally) irrigation event.

Crop-specific projection guidance:

1. Constrain threshold values and interpretation texts by crop and stage.
2. Hide irrigation-specific fields entirely for rain-fed crops/farms unless explicitly enabled.

### 6.5 Organic weed control loop template (v0.7)

Template:

1. `Template: Organic Weed Control Loop v1.6`

Expected composition:

1. Weed pressure assessment.
2. Mechanical weeding event(s).
3. Optional cleanout events on lot/status transitions.

Projection guidance:

1. Crop-specific allowed weeding methods by row spacing / crop type.
2. Enforce field trafficability checks for heavy equipment conditions.

### 6.6 Planting execution and emergence check template (v0.7)

Template:

1. `Template: Planting Execution + Emergence Check v1.6`

Expected composition:

1. Planting execution record.
2. Stand count observation.
3. Replant need assessment.

Projection guidance:

1. Crop-specific seeding rate units and plausible ranges.
2. Crop-specific emergence windows (date constraints).

### 6.7 Harvest -> storage lot traceability template (v0.7)

Template:

1. `Template: Harvest Intake -> Storage Lot Traceability v1.6`

Expected composition:

1. Harvest event.
2. Delivery ticket record.
3. Storage lot identity and movement journal.

Organic-first notes:

1. Templates MUST surface lot status transitions and cleanout requirements when switching between organic and conventional lots.

### 6.8 Storage monitoring and aeration template (v0.7)

Template:

1. `Template: Storage Aeration + Quality Preservation Loop v1.6`

Expected composition:

1. Storage condition snapshots.
2. Aeration actions.
3. Quality panel linkage where relevant.

### 6.9 Warehouse quality release check template (v0.5)

Template:

1. `Template: Warehouse Quality Release Check v1.4`

Expected composition:

1. Sample collection record.
2. Quality panel results (impurities, moisture, hectolitre mass, temperature, proteins, broken kernels, empty grains, insect presence).
3. Release recommendation.

## 7. Crop-Specific Template Projections (How to Hide Irrelevant Fields)

This section answers the practical UX question:

> For an analysis workflow on a specific crop, should the system hide irrelevant fields and enforce crop-specific value limits?

Yes. Templates are the correct place to do it.

### 7.1 Principle: archetype stays broad, template narrows

1. Archetype defines full semantic concept and potential fields.
2. Template narrows:
   - requiredness (`required` vs `optional`),
   - allowed codes (`allowedValues`),
   - unit constraints (`allowedUnits`),
   - magnitude constraints (`min/max`),
   - visibility (`hidden` fields are excluded from UI projection).
3. Backend validation MUST still enforce template constraints (not only UI).

### 7.2 Recommended template projection format (implementation guidance)

Templates SHOULD carry a machine-readable projection block, for example:

```json
{
  "templateId": "farm.tpl.si.winter_wheat.crop_health_visit.v1",
  "context": {
    "applicableCropTypes": ["eppo:TRZAW", "agrovoc:winter_wheat"],
    "productionSystem": ["organic", "in_transition", "conventional"]
  },
  "projectionRules": [
    { "field": "bbchCode", "required": true },
    { "field": "suspectedPathogenCode", "allowedCodeSystem": "EPPO", "required": true },
    { "field": "leafWetnessDurationHours", "hidden": true }
  ],
  "valueLimits": [
    { "field": "seedingRate", "unit": "kg/ha", "min": 80, "max": 260 }
  ]
}
```

This pack does not require a specific projection DSL, but it makes the requirement explicit:
templates MUST be able to drive crop-specific UI and validation.

## 8. Implemented Additions (v0.8)

The current catalog covers many core needs, but agronomy teams often need these additional canonical concepts.
These are implemented in this pack as concrete archetypes/templates with SHACL, ontology, SQL, and API mapping.

### 8.1 Added archetypes

1. `OBSERVATION.pest_trap_count.v1`
   - standardize trap-based monitoring (count, trap type, placement, window).
2. `OBSERVATION.remote_sensing_index_observation.v1`
   - NDVI/NDRE style indices with provenance (sensor/product, resolution, date, geometryRef).
3. `ACTION.cover_crop_management_event.v1`
   - cover crop planting/termination as organic-first agronomy primitives.
4. `ACTION.tillage_event.v1`
   - tillage/seedbed prep is a high-frequency operation with soil-structure consequences.

### 8.2 Added templates

1. `Template: Crop Health Visit (IPM + Nutrition) v0.8`
   - crop stage + scouting signs + weed pressure + nutrient deficiency assessment.
2. `Template: Organic Establishment Risk Guard v0.8`
   - planting + weather hazard + soil trafficability + contingency actions.
3. `Template: Remote Sensing Review -> Scout Task v0.8`
   - index anomaly observation -> task dispatch -> scouting evidence -> recommendation feedback.

### 8.3 Added implementation artifacts

1. SHACL constraints: `specs/v0.8/constraints/farm-rm-v1_7-agronomy-archetypes.shacl.ttl`
2. SHACL tests:
   - pass: `specs/v0.8/constraints/tests/data/pass-agronomy-v1_7.ttl`
   - fail: `specs/v0.8/constraints/tests/data/fail-agronomy-v1_7.ttl`
3. Ontology extension: `specs/v0.8/ontology/farm-rm-v1_7-agronomy-archetypes.ttl`
4. SQL migration: `specs/v0.8/sql/migrations/0016_v1_7_agronomy_archetypes.sql`
5. Template projection packs (machine-readable UI constraints):
   - `specs/v0.8/templates/projections/template-crop-health-visit-ipm-nutrition-v0_8.json`
   - `specs/v0.8/templates/projections/template-organic-establishment-risk-guard-v0_8.json`
   - `specs/v0.8/templates/projections/template-remote-sensing-review-to-scout-task-v0_8.json`
6. API bindings (reference FastAPI contract):
   - `POST /v1/field-ops/cover-crop-management-events`
   - `POST /v1/field-ops/tillage-events`
   - `POST /v1/reporting/pest-trap-counts`
   - `POST /v1/reporting/remote-sensing-index-observations`
   - `GET /v1/templates/projections/{templateId}`

## 9. Definition of Done (for adopting this pack)

An implementation can claim conformance with this pack when it can:

1. Render crop-specific templates that hide irrelevant fields.
2. Enforce template limits and requiredness in backend validation (SHACL and/or API validation).
3. Capture at least one complete flow per domain:
   - soil fertility cycle,
   - disease/IPM case cycle,
   - irrigation decision cycle,
   - planting -> emergence -> replant cycle,
   - harvest -> storage -> delivery continuity.

## 10. References (non-normative)

1. BBCH growth stage coding is commonly used in European agronomy and appears in EPPO contexts.
2. EPPO coding system is widely used for plant, pest, and weed identifiers in agronomic data exchange.
3. Soil test analyte sets vary by lab; templates should declare required analytes and accept optional additions.

Convenient entry points:

1. EPPO codes: https://www.eppo.int/ACTIVITIES/standards/codes
2. EPPO BBCH: https://www.eppo.int/RESOURCES/eppo_databases/eppo_bbch
