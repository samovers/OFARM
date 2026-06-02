# Everyday Farm Use-Cases -> Farm-RM Backlog (Research + Gap Analysis)

Date: 2026-02-23

This is a research-backed inventory of everyday farm workflows and the archetype/template/ontology coverage needed to support them.
It also maps those workflows to what exists in this repo today (Farm-RM v0.1..v0.6) and proposes a prioritized backlog.

## 0) Scope Assumptions (So This Stays Concrete)

- Primary scope: crop farms (row crops / grains / mixed), with an emphasis on organic + traceability.
- Secondary scope (optional packs): produce safety (FSMA Produce Safety Rule), research trials.
- Out of scope for this pass: livestock, permanent tree crops/forestry, full accounting/ERP.

## 1) What Farm-RM Is Trying To Be (As Implemented Here)

Farm-RM in this repo is not "run the whole system inside an ontology engine".
It is an openEHR-inspired two-level modeling pattern:

1. RM (stable): identifiers, relationships, intent-vs-reality, evidence scaffolding.
2. Archetypes (reusable concept specs): "what a soil moisture profile is", "what a pesticide application event is", etc.
3. Templates (workflow composition): archetypes assembled for a specific real workflow and reporting need.

In implementation terms here:

- RM is expressed as RDF/OWL-ish TTL + SHACL constraints + SQL schema.
- Archetypes/templates are human-authored Markdown, compiled to FADL + JSON, and then enforced via SHACL/SQL where it matters.

## 2) What You Already Have (Inventory Snapshot)

### Existing archetype packs (by stream)

- v0.2 (soil + disease):
  - OBSERVATION: crop scouting signs, diagnostic test result, soil lab panel, soil sample collection, soil sensor series
  - INSTRUCTION: IPM control plan, soil amendment plan
  - ACTION: disease control operation, soil amendment application
  - EVALUATION: disease case assessment, disease risk forecast, soil fertility status, soil constraint risk
  - ADMIN: phytosanitary case file, soil compliance evidence
- v0.3 (crop suitability):
  - OBSERVATION: field pedoclimatic profile, seed lot quality health, variety trial result
  - INSTRUCTION: variety selection plan
  - EVALUATION: variety field suitability, variety risk profile
  - ADMIN: variety evidence package
- v0.4 (planning/risk/regulation):
  - OBSERVATION: climate hazard profile, crop adaptation profile, equipment capability profile, field trafficability profile, forecast scenario bundle, storage quality conditions, water allocation and use
  - EVALUATION: equipment field suitability, seed field compatibility, scenario impact assessment, recommendation outcome feedback
  - ADMIN: incident contingency case, safety and competency gate, tenure contract constraints
- v0.5 (canonical ops + measurements):
  - OBSERVATION: soil moisture profile, soil temperature profile, agromet station observation, leaf wetness duration, crop stage assessment
  - ACTION: pesticide application event, fertilizer application event, irrigation event, harvest event
  - EVALUATION: irrigation need assessment, nutrient deficiency assessment
  - INSTRUCTION: irrigation event plan
  - OBSERVATION (post-harvest): warehouse product sample collection, warehouse product quality panel
- v0.6 (equipment/telematics/energy + multilingual):
  - OBSERVATION: equipment telemetry point
  - EVALUATION: field coverage assessment, fuel allocation batch
  - ACTION: refuel event
  - CLUSTER: localized label

### Existing templates (by stream)

- v0.2: soil fertility monitoring cycle; disease case management (IPM); organic contamination guard (SI 2026)
- v0.3: variety selection (granular); variety selection (sparse seller)
- v0.4: organic resilience small team; pro irrigation quality loop; enterprise contract traceability
- v0.5: irrigation decision visit; research field trial cycle; warehouse quality release check
- v0.6: fleet energy/coverage cycle

## 3) Research-Derived "Everyday Farm" Workflow Inventory

This list is intentionally pragmatic: it is built from what farmers are asked to DO and RECORD.
Organic and food-safety requirements are useful because they enumerate the minimum evidence required for day-to-day operations.

### A) Field activity records (what happened, where, when, with what)

Common, everyday items (especially for organic audits and for general traceability):
- Planting/seeding details: date, field, crop/variety, seed lot/source, seeding rate, equipment used.
- Field operations log: tillage, cultivation, mowing/termination, irrigation, harvest, transport.
- Input use: fertilizers/soil amendments and pest control products (including organic-approved inputs).
- Application details: rate, method, timing, weather constraints, operator/equipment.

Evidence basis (examples of what certifiers ask you to keep):
- USDA NOP recordkeeping requirement (7 CFR 205.103).
- Organic system integrity: preventing commingling and contact with prohibited substances (7 CFR 205.272).
- Organic certifier guidance and sample logs (field activity, inputs, seed/planting stock, harvest, sales).

### B) Scouting, monitoring, and decision support (observations -> evaluations -> actions)

Common, everyday items:
- Routine scouting visits: weeds, insects, disease symptoms, crop stage, stand counts, lodging, drought stress.
- Weather and leaf wetness (already present) plus simple "field ready" assessments (trafficability, soil moisture).
- Soil tests and lab panels (already present) plus nutrient follow-up or tissue tests (gap).
- IPM recordkeeping: what was found, thresholds, what action was taken, what product was used (if any).

Evidence basis:
- University IPM programs repeatedly emphasize recordkeeping for monitoring and decision-making.

### C) Equipment readiness, maintenance, and cleaning (a real everyday friction point)

Common, everyday items:
- Maintenance events: inspections, service, repairs, calibration.
- Cleanout events to prevent commingling (organic) or residues (sprayer/tender/bins/combines).
- Equipment allocation: which equipment/implement was used on which field/operation (partially present via v0.6 telematics, but not as operator-entered maintenance/cleaning records).

Evidence basis:
- Organic rules and certifier checklists frequently require cleanout and commingling prevention documentation.

### D) Harvest -> storage -> quality -> sale (traceability chain)

Common, everyday items:
- Harvest event (present) but typically needs: load IDs, weights, moisture/quality at intake, destination bin, lot linkage.
- Storage monitoring: temperature/moisture/aeration actions and logs (storage quality conditions exist, but not the action log).
- Quality sampling/panel (present) and release check (present).
- Sales/delivery records: buyer, contract reference, weights, delivery tickets, lot identifiers.

Evidence basis:
- Grain storage best practices and guidance emphasize monitoring and aeration management logs.
- Organic and food-safety programs require lot traceability and handling records.

### E) Compliance packaging (what gets assembled for an audit or authority)

Common, everyday items:
- Organic system plan + updates (practice changes, input approvals, seed sourcing exceptions, buffer zones).
- Inspection case: evidence bundles, nonconformities, corrective actions (core RM scaffolding exists).
- Jurisdictional or program reports (already partially represented by template mapping + report templates in SQL streams).

Evidence basis:
- Organic programs define recordkeeping and audit evidence expectations; food-safety programs define required logs.

## 4) Gap Map: Everyday Use-Cases vs Current Coverage

Legend:
- Covered: direct archetype + constraints exist
- Partial: can be expressed, but lacks canonical fields/constraints or workflow template
- Missing: no archetype/template; would become ad-hoc fields and lose interoperability

### Field operations

- Planting/seeding: Missing (no ACTION.* archetype)
- Tillage/seedbed prep: Missing
- Mechanical weed control/cultivation: Missing
- Cover crop management (planting/termination, biomass): Missing
- Irrigation: Covered (ACTION.irrigation_event, INSTRUCTION.irrigation_event_plan, irrigation templates)
- Fertility: Partial (ACTION.fertilizer_application_event exists, but compost/manure/amendment scenarios are split across packs and not unified as "nutrient application")
- Pest control: Covered for "application event", but organic-specific "product approval + restricted materials" workflow is Missing
- Harvest: Partial (ACTION.harvest_event exists, but load/bin/lot chain is not modeled as a first-class workflow)

### Monitoring and decisions

- Soil moisture/temperature/agromet/leaf wetness: Covered
- Crop stage: Covered
- Scouting visits (structured, repeatable): Partial (OBSERVATION.crop_scouting_signs exists, but there is no "scouting visit template" that ties stage + weeds + pests + decision outputs)
- Weed pressure (quantified): Missing
- Stand count/emergence assessment: Missing
- Tissue tests / nutrient lab: Missing (soil lab exists, crop tissue does not)

### Equipment + storage

- Telematics/coverage/fuel: Covered (v0.6)
- Maintenance events / calibration: Missing
- Equipment cleanout (organic commingling prevention): Missing
- Bin aeration/drying actions: Missing
- Storage monitoring: Partial (OBSERVATION.storage_quality_conditions exists; missing action + template)

### Traceability and sales

- Warehouse sampling + quality panel + release: Covered (v0.5)
- Lot movement (field -> load -> storage lot -> sale lot): Partial (RM has MaterialLot/StorageLot, but there is no canonical action/event archetype/template for movements and ticket capture)
- Delivery/weigh ticket record: Missing

## 5) Proposed Archetypes (Backlog)

The intent is to keep core RM stable and add everyday specificity via archetypes + templates, consistent with the repo's modeling method.

### 5.1 High-ROI ACTION archetypes (daily operations)

1. ACTION.planting_event.v1
   - Purpose: record seeding/planting execution with seed lot linkage and equipment context.
   - Key fields: fieldUri, cropInstanceUri, seedLotRef, plantedAt, seedingRate(+unit), rowSpacing, plantingDepth, equipmentInstanceRef, operatorRef, sourceQuality.
2. ACTION.tillage_event.v1
   - Purpose: record tillage/seedbed prep passes (depth/implement/speed/coverage).
   - Key fields: fieldUri, executedAt, implement/equipment refs, tillageDepthCm, passCount, workingWidth, coverageRef (optional), soilConditionNote.
3. ACTION.mechanical_weeding_event.v1
   - Purpose: record cultivation/harrow/hoe passes with intent to manage weeds (very common in organic).
   - Key fields: fieldUri, cropStageRef (BBCH), implement type, rowSpacing, settings, executedAt, areaHa, operatorRef, evidence refs.
4. ACTION.cover_crop_termination_event.v1
   - Purpose: record mow/roll/crimp/incorporate termination (organic reliance).
   - Key fields: fieldUri, coverCropInstanceRef, methodCode, executedAt, biomassEstimateRef, followupPlanRef.
5. ACTION.storage_bin_aeration_event.v1
   - Purpose: record aeration/drying/fan runtime and settings as an auditable action.
   - Key fields: storageLotRef/binRef, startedAt/endedAt, mode (aeration/drying), targetMoisture, fanHours, measuredBefore/after refs.
6. ACTION.equipment_maintenance_event.v1
   - Purpose: inspections/service/repair/calibration as an evidence-bearing operation.
   - Key fields: equipmentInstanceRef, performedAt, maintenanceType, meterReading, partsUsed, downtimeMinutes, performedBy, evidenceRef.
7. ACTION.equipment_cleanout_event.v1
   - Purpose: prevent commingling/contact with prohibited substances (organic) and document cleanout between lots/fields.
   - Key fields: equipmentInstanceRef (sprayer/combine/bin/auger/truck), cleanedAt, previousUseRef, nextUseRef, methodCode, rinseCycles, inspectionResult, evidenceRef.

### 5.2 High-ROI OBSERVATION archetypes (what drives decisions)

1. OBSERVATION.crop_stand_count.v1
   - Purpose: emergence/stand assessment (plant population) tied to planting decisions and replant triggers.
   - Key fields: fieldUri, observedAt, methodCode, samplesCounted, plantsPerMeter/acre, rowSpacing, confidence.
2. OBSERVATION.weed_pressure_assessment.v1
   - Purpose: quantify weed pressure by species group and severity class to support weed-control timing.
   - Key fields: fieldUri, observedAt, cropStageRef (BBCH), severityScale, dominantWeeds (EPPO/AGROVOC refs), coveragePct.
3. OBSERVATION.crop_tissue_lab_panel.v1
   - Purpose: nutrient status evidence that complements soil lab panel and nutrient deficiency evaluation.
   - Key fields: cropInstanceUri, observedAt, growthStage, analytes list (N/P/K + micronutrients), units, labRef, QA flags.
4. OBSERVATION.storage_bin_condition_snapshot.v1
   - Purpose: normalized temp/moisture/CO2 snapshots for stored lots (more granular than "storage quality conditions").
   - Key fields: storageLotRef/binRef, observedAt, tempC, moisturePct, fanState, sensorRef, qualityFlag.
5. OBSERVATION.delivery_ticket_record.v1
   - Purpose: bring weigh tickets into the evidence graph without reinventing accounting.
   - Key fields: deliveredAt, fromStorageLotRef, toPartyRef/buyer, grossWeight/netWeight, moisture, ticketRef, transportRef.

### 5.3 EVALUATION + INSTRUCTION archetypes (make governance executable)

1. EVALUATION.replant_need_assessment.v1
   - Inputs: crop stand count + weather + variety constraints; output: recommendation + confidence.
2. INSTRUCTION.field_work_order.v1
   - Purpose: daily/weekly planned work packages (what to do, where, prerequisites, safety gate refs).
3. EVALUATION.organic_integrity_risk.v1
   - Purpose: commingling/prohibited-substance contact risk evaluation (extends beyond spray drift to storage and equipment).

## 6) Proposed Templates (Workflow Compositions)

1. template-planting-execution-and-emergence-check-v1
   - Compose: INSTRUCTION.field_work_order + ACTION.planting_event + OBSERVATION.crop_stand_count + EVALUATION.replant_need_assessment.
2. template-organic-weed-control-loop-v1
   - Compose: OBSERVATION.weed_pressure_assessment + OBSERVATION.crop_stage_assessment + ACTION.mechanical_weeding_event + EVALUATION.recommendation_outcome_feedback.
3. template-cover-crop-termination-to-planting-handoff-v1
   - Compose: ACTION.cover_crop_termination_event + OBSERVATION.field_trafficability_profile + ACTION.planting_event.
4. template-storage-aeration-quality-preservation-loop-v1
   - Compose: OBSERVATION.storage_bin_condition_snapshot + ACTION.storage_bin_aeration_event + OBSERVATION.warehouse_product_quality_panel (optional) + template-warehouse-quality-release-check.
5. template-organic-lot-switch-cleanout-and-release-v1
   - Compose: ACTION.equipment_cleanout_event + EVALUATION.organic_integrity_risk + (existing) warehouse sample + quality panel + release check.
6. template-harvest-intake-to-storage-lot-traceability-v1
   - Compose: ACTION.harvest_event + OBSERVATION.delivery_ticket_record + OBSERVATION.storage_bin_condition_snapshot + enterprise contract traceability template.

## 7) Ontology/Constraint Implications (Minimal and Compatible)

To avoid "ontology lecture, no software value", keep this aligned with your existing stance:

- Keep Farm-RM URIs canonical; treat external vocabularies (AGROVOC/Crop Ontology/EPPO/BBCH) as bindings.
- Add ontology classes/properties only when they create stable anchors for indexing and validation.

Minimal additions that help immediately:

1. Extend operationType and observationType concept binding guidance:
   - ACTION.planting_event maps to an operationType URI (AGROVOC or local concept scheme).
2. Introduce stable "lot movement" and "ticket" anchors (optional module):
   - If you want first-class traceability queries, consider adding an RM-level class like farm:TransferEvent or farm:InventoryTransaction.
   - Otherwise, keep as OBSERVATION.delivery_ticket_record + ACTION.* archetypes and link via existing MaterialLot/StorageLot.
3. SHACL shapes should be added for any archetype you expect to validate deterministically (like soil moisture already is).

## 8) Suggested Priority (If You Want Real Product Impact Fast)

1. Planting/seeding + emergence (because it is universal, frequent, and drives downstream decisions).
2. Mechanical weed control loop (organic core workflow; also useful in conventional).
3. Equipment maintenance + cleanout (audit + uptime; reduces real-world friction).
4. Harvest intake -> storage lot traceability (turns "we harvested" into sellable/auditable lots).
5. Storage aeration/drying loop (quality preservation and loss prevention).

## 9) Notes On "Why Codex Did What You Asked"

Your intuition was right: openEHR-style modeling is powerful.
But the value only shows up when:

- archetypes are comprehensive for everyday work (not just the example you gave),
- templates map to real workflows (what the farm does weekly),
- constraints are executable where it matters (SHACL/SQL), and
- governance exists for versioning and change.

This repo has the modeling spine and some important packs, but it is missing several of the most universal day-to-day workflows (planting, tillage, cultivation, maintenance, cleanout, intake tickets).

## References (external)

Organic recordkeeping and integrity requirements (use-case drivers):
- 7 CFR 205.103 (Recordkeeping): https://www.ecfr.gov/current/title-7/subtitle-B/chapter-I/subchapter-M/part-205/subpart-E/section-205.103
- 7 CFR 205.272 (Commingling and contact with prohibited substance): https://www.ecfr.gov/current/title-7/subtitle-B/chapter-I/subchapter-M/part-205/subpart-C/section-205.272
- Oregon Tilth (recordkeeping examples and "what to keep"): https://tilth.org/product/organic-farming-recordkeeping/
- CCOF (sample recordkeeping forms): https://www.ccof.org/page/sample-recordkeeping-forms

Everyday monitoring and decision workflows (scouting, IPM):
- Michigan State University Extension (IPM and recordkeeping): https://www.canr.msu.edu/news/integrated_pest_management_and_recordkeeping

Everyday post-harvest operations (storage monitoring and aeration):
- University of Minnesota Extension (stored grain aeration management): https://extension.umn.edu/crop-harvest-and-storage/stored-grain-aeration-management

Optional program packs (if you target these farms):
- USDA FSA acreage reporting overview (drives planting/activity records): https://www.fsa.usda.gov/programs-and-services/arcplc_program/arcplc-program-data-terms/acreage-reporting
- FDA FSMA Produce Safety Rule (recordkeeping-focused rule text): https://www.ecfr.gov/current/title-21/chapter-I/subchapter-M/part-112
