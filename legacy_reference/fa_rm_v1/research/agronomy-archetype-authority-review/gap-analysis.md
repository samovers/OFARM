# Cross-Archetype Gap Analysis (Final)

Reviewed: 2026-02-27
Input set: 58 authority review docs in `docs/research/agronomy-archetype-authority-review/archetypes/`.

This file is a roll-up checklist/backlog. The numbered items in **Prioritized Backlog** reference the gap numbers in **Raw Gap List**.

## Cross-Cutting Missing Primitives (What Farm-RM Repeatedly Needs)

1. **Procedure/method provenance as a first-class pattern**:
   - Many observations/actions are only comparable when we capture a procedure reference (SOP/standard) in addition to a method code.
   - Implementation impact: archetypes + templates/profiles + SHACL + API models + persistence.
2. **Multi-evidence attachment pattern with roles**:
   - "Evidence-bearing" records typically need multiple attachments with roles (invoice, lab report, photo, calibration sheet), not a single `evidenceRef`.
   - Implementation impact: `evidence_record` usage + link tables + API payload conventions + SHACL.
3. **Measurement-basis semantics for quantities and summaries**:
   - Repeated ambiguity appears as "basis" (withdrawn/applied/consumed water; point vs avg/max sensor readings; loss basis; unit basis).
   - Implementation impact: archetype fields + vocab + constraints + API/DB.
4. **Case/package identifiers for grouping records over time**:
   - Disease incidents, regulatory submissions, and compliance evidence need stable identifiers to group assessments/evidence/submissions.
   - Implementation impact: admin/event primitives + submission package linkage + templates/profiles.
5. **A consistent repeating-group persistence approach**:
   - Mix components, sampling increments, product uses, and attachments recur; decide when to use link tables vs JSONB (and make it consistent).
   - Implementation impact: SQL migration patterns + API schema conventions.

## Cross-Cutting Vocabulary Needs (External + Governed)

1. **EPPO** (pests/pathogens, crop codes where applicable).
2. **AGROVOC** (crop/cover species terms).
3. **BBCH** (growth stage semantics across field operations).
4. **Standards-backed grain quality/grade systems** (jurisdiction-specific, but must be explicitly identified).
5. **Lab method/analyte code systems** (AOAC/ISO/ASABE/EPPO/other as applicable per domain).
6. **Units normalization guidance** (local units allowed via profiles; ensure explicit unit + basis semantics where ambiguity is high).

## Template/Profile Recommendations (Multi-Jurisdiction Packaging)

1. Use **profiles** to encode jurisdiction/program strictness (required fields, allowed codes, ranges, attachment requirements).
2. Use **production-system profiles** (`organic|in_transition|conventional`) to require:
   - cleanout evidence + compliance evidence packaging in organic modes
   - label/version and interval constraints where applicable.
3. Profiles should also encode "comparability requirements":
   - enforce method/procedure provenance for observations that drive decisions (sampling, sensors, forecasts, quality panels).

## Prioritized Backlog (By Risk/ROI)

### High Scientific Risk (Comparability or Audit Failure)

1. **Sampling + assay comparability and provenance** (gaps: #1, #2, #3, #44, #45):
   - Add result-qualifier semantics, governed analyte/method codes, and required sampling-plan metadata where it dominates uncertainty.
   - Impact: archetypes + vocab + SHACL + SQL + API + tests.
2. **Observation/sensor/time-support provenance** (gaps: #6, #7, #8, #13, #21, #22, #23, #24):
   - Normalize how we encode deployment context, QC flags, averaging/accumulation intervals, thresholds, and procedure refs.
   - Impact: archetypes + vocab + SHACL + SQL + API.
3. **Water/irrigation accounting semantics** (gaps: #36, #37, #38, #39):
   - Require explicit basis (withdrawn/applied/consumed), measurement method, and threshold/ruleset references for decisions.
   - Impact: archetypes + vocab + SHACL + SQL + API.
4. **Storage quality + sampling uncertainty** (gaps: #42, #43, #44, #45, #46):
   - Add measurement-basis semantics, explicit sampling-plan metadata, grade-system context, and action-to-condition linkage.
   - Impact: archetypes + vocab + SHACL + SQL + API.

### High Operational ROI (Farm Usability)

1. **Fix template references to missing primitives and spec/impl drift** (gaps: #11, #14, #50):
   - Ensure templates only depend on implemented archetypes; add missing admin primitives where templates require them.
   - Impact: archetypes/templates + SHACL + SQL + API + tests.
2. **Case/package workflows for compliance submissions** (gaps: #18, #50):
   - Implement evidence sets and submission linkages as first-class, queryable admin records.
   - Impact: admin archetypes + SQL + API + reporting persistence.
3. **Equipment integrity workflows** (gaps: #47, #48):
   - Add schedule/procedure provenance, outcomes, and multi-evidence attachments for maintenance/cleanout.
   - Impact: archetypes + SQL + API + tests.
4. **Cover crop mix + termination-stage capture** (gap: #49):
   - Support mixes and stage semantics to make termination records interpretable (esp. roller-crimp in organic systems).
   - Impact: archetypes + SQL + API + SHACL.

### Interoperability (Export/Import Mapping)

1. **Governed code systems + external mappings** (gaps: #3, #20, #41, #43, #49):
   - Make external code-system alignment explicit (EPPO/AGROVOC/BBCH/grades/methods) and persist code-system identifiers.
   - Impact: vocab registries + SHACL + API payload conventions.
2. **Units and basis normalization** (gaps: #10, #39, #41, #43):
   - Make ambiguous units and basis semantics explicit (especially tickets, water, storage loss/grades).
   - Impact: archetypes + vocab + constraints.

## Reviewed Archetypes
- `OBSERVATION.soil_sample_collection.v1`
- `OBSERVATION.soil_lab_panel.v1`
- `EVALUATION.soil_fertility_status.v1`
- `EVALUATION.soil_constraint_risk.v1`
- `OBSERVATION.soil_sensor_series.v1`
- `OBSERVATION.soil_moisture_profile.v1`
- `OBSERVATION.soil_temperature_profile.v1`
- `INSTRUCTION.soil_amendment_plan.v1`
- `ACTION.soil_amendment_application.v1`
- `ACTION.fertilizer_application_event.v1`
- `EVALUATION.nutrient_deficiency_assessment.v1`
- `ACTION.planting_event.v1`
- `OBSERVATION.crop_stand_count.v1`
- `EVALUATION.replant_need_assessment.v1`
- `OBSERVATION.crop_stage_assessment.v1`
- `OBSERVATION.crop_scouting_signs.v1`
- `OBSERVATION.weed_pressure_assessment.v1`
- `ACTION.mechanical_weeding_event.v1`
- `INSTRUCTION.ipm_control_plan.v1`
- `OBSERVATION.pest_trap_count.v1`
- `EVALUATION.disease_risk_forecast.v1`
- `EVALUATION.disease_case_assessment.v1`
- `OBSERVATION.diagnostic_test_result.v1`
- `ADMIN.phytosanitary_case_file.v1`
- `ACTION.disease_control_operation.v1`
- `ACTION.pesticide_application_event.v1`
- `OBSERVATION.leaf_wetness_duration.v1`
- `OBSERVATION.agrometeorological_station_observation.v1`
- `OBSERVATION.remote_sensing_index_observation.v1`
- `OBSERVATION.forecast_scenario_bundle.v1`
- `OBSERVATION.climate_hazard_profile.v1`
- `OBSERVATION.crop_adaptation_profile.v1`
- `OBSERVATION.field_pedoclimatic_profile.v1`
- `OBSERVATION.equipment_capability_profile.v1`
- `EVALUATION.equipment_field_suitability.v1`
- `OBSERVATION.seed_lot_quality_health.v1`
- `EVALUATION.seed_field_compatibility.v1`
- `OBSERVATION.variety_trial_result.v1`
- `EVALUATION.variety_risk_profile.v1`
- `EVALUATION.variety_field_suitability.v1`
- `INSTRUCTION.variety_selection_plan.v1`
- `ADMIN.variety_evidence_package.v1`
- `INSTRUCTION.irrigation_event_plan.v1`
- `ACTION.irrigation_event.v1`
- `EVALUATION.irrigation_need_assessment.v1`
- `OBSERVATION.water_allocation_and_use.v1`
- `ACTION.harvest_event.v1`
- `OBSERVATION.delivery_ticket_record.v1`
- `OBSERVATION.storage_bin_condition_snapshot.v1`
- `OBSERVATION.storage_quality_conditions.v1`
- `OBSERVATION.warehouse_product_sample_collection.v1`
- `OBSERVATION.warehouse_product_quality_panel.v1`
- `ACTION.storage_bin_aeration_event.v1`
- `ACTION.equipment_maintenance_event.v1`
- `ACTION.equipment_cleanout_event.v1`
- `ACTION.cover_crop_management_event.v1`
- `ACTION.tillage_event.v1`
- `ADMIN.soil_compliance_evidence.v1`

## Raw Gap List (From Per-Archetype Reviews)

1. **Sampling context is under-modeled and/or not persisted**:
   - Soil sampling depth + method are specified as required by the archetype, but are not persisted/validated in the current reference implementation.
2. **Lab results need a first-class \"result qualifier\" concept**:
   - Common lab patterns like `<LOD` / non-detect require explicit qualifiers, not just nullable values.
3. **Governed code systems/value sets are missing for analytes and methods**:
   - Interoperability requires published analyte codes and method codes (especially when results depend on extraction/determination method).
4. **Evaluations need explicit provenance ("which guideline/system")**:
   - Interpretations like "low/target/high" are calibration- and region-dependent; evaluations should record which interpretation system was used.
5. **Risk evaluations need indicator+method structure and governed risk vocab**:
   - Constraint risks (e.g., compaction) are assessed via measured indicators with known methods/standards; risk types/levels should be controlled codes, not ad-hoc strings.
6. **Raw sensor series needs a deployment/calibration model and numeric semantics**:
   - Sensor readings are only interpretable with deployment context (field/zone/depth) and calibration/provenance; the current archetype does not capture these.
   - The RM/ontology currently models observation values as strings, while SQL supports numeric values; this misalignment should be resolved for sensor data.
7. **Profiles/observations need a consistent way to encode "where in the field"**:
   - Both soil sampling and soil moisture monitoring benefit from an explicit `geoFeatureUri`/zone reference, not just `fieldUri`.
8. **Sensor observations need "measurement site context" (surface cover / representativeness)**:
   - Soil temperature meaning changes with surface cover (bare soil vs under residue/canopy); standards often assume representative bare-ground plots for comparability.
9. **Instruction/plan archetypes need 4R-complete parameters plus evidence basis**:
   - Nutrient/soil amendment plans are typically evaluated/audited using the "right source, rate, time, place" framing and require traceable basis inputs (soil tests, assumptions, constraints).
10. **Execution events need explicit area+rate basis and application method (not just quantities)**:
   - Audit-ready nutrient/amendment application records commonly require applied area, rate units, method/placement, and (often) conditions/calibration references.
11. **Spec vs implementation drift is already present for core field operations**:
   - Some archetype+SHACL specs model richer semantics (e.g., product identity, method codes, nutrient composition) than the current SQL/API persistence captures, so the stack cannot currently guarantee consistent meaning end-to-end.
12. **Nutrient diagnosis evaluations need interpretation-system provenance (SRA vs DRIS) and norms references**:
   - Nutritional diagnosis outputs depend on the interpretation method and reference norms; without recording the method/norms, severity and recommendations are not comparable across labs/advisors/time.
13. **Field observation procedures need protocol/procedure provenance, not just a method code**:
   - Observations like stand counts depend on a defined counting protocol (row length or quadrat area); recording a procedure/protocol reference improves repeatability and auditability.
14. **Some v0.8 templates reference legacy v0.5 archetypes that are not carried into the v1.7 validation/persistence stack**:
   - Example: crop-stage assessment is referenced by v0.8 templates but is only validated in the legacy v1.4 SHACL pack and has no DB/API persistence today.
15. **Scouting observations need a first-class "intensity" model (incidence vs severity + scale/units)**:
   - Pest/disease scouting is only comparable when records distinguish incidence (percent plants affected) from severity (percent tissue affected) and capture the scale/units and sampling effort.
16. **Forecast/derived evaluations need model/run provenance and threshold references**:
   - Disease risk forecasts are model-derived; without model identifier/version/config and the thresholds used to produce risk classes/triggers, outputs are not reproducible or auditable.
17. **Append-only "incident" workflows need a stable case identifier for grouping assessments over time**:
   - Disease case management needs a `caseUri` concept to group multiple assessments/evidence as the incident evolves; current v0.2 archetype does not provide this and the v1.7 stack does not persist it.
18. **Regulatory "case file" packaging needs a first-class submission/ack linkage model**:
   - Phytosanitary pest reporting requires structured report content, evidence links, and update/correction history; Farm-RM currently has generic submission/ack tables but no first-class phytosanitary case file record linking a disease case to submission artifacts and authority responses.
19. **Plant protection actions need (a) case linkage and (b) defensible conditions metadata**:
   - Chemical disease control operations often need linkage to the disease case/assessment (why the action was taken) and may need environmental conditions + measurement context (wind, etc.) to defend drift-risk claims; current v1.7 plant protection persistence lacks a disease-case link and does not model conditions metadata.
20. **Label-derived compliance constraints need versioned label/authorization references**:
   - Safety intervals like REI and PHI and other constraints are label-derived; records should capture the specific authorization/label reference (and ideally version) used to interpret PHI/REI and buffer zone requirements, not just free text.
21. **Leaf wetness duration needs explicit provenance (threshold + deployment context) to be comparable**:
   - Leaf wetness duration is sensitive to sensor type, placement/height, calibration and the wet/dry thresholding procedure; without these, values from different stations/sensors/models are often not comparable.
22. **Weather station observations need explicit temporal support (averaging/accumulation interval) and QC provenance**:
   - Variables like rainfall and wind are often reported as accumulations/averages over an interval; without time support metadata and consistent QC flag semantics, station observations are ambiguous and can mislead downstream models.
23. **Forecast scenario bundles need explicit issuance time, scope, and variable-level semantics/provenance**:
   - Probabilistic scenarios are only meaningful for a defined time window and scope and should record issuance/run time; assumptions must be structured (variable codes, values, units, time support) and linked to a forecast provider/model/source for reproducibility and auditability.
24. **Climate hazard profiles need baseline/reference period + hazard metric parameterization (not just hazard labels)**:
   - Hazard "profiles" are derived statistics; to be comparable and defensible they must record baseline period boundaries and structured hazard metric definitions/parameters (thresholds, index time scale, method), plus source and confidence metadata.
25. **Variety adaptation traits need explicit descriptor + scale + evidence semantics (especially maturity/GDD)**:
   - Many adaptation-related ratings (maturity, drought tolerance, waterlogging tolerance) are not globally standardized, so Farm-RM needs a trait assertion pattern with explicit descriptor identity, rating scale/unit, and evidence/provenance; GDD-based maturity/fit also needs method-definitional metadata.
26. **Field pedoclimatic profiles need controlled soil-class codes + climate reference-period provenance**:
   - Soil texture and drainage are classification systems (not free text), and climate-derived indicators like annual GDD need an explicit reference period and method/basis metadata to be comparable across data sources and over time.
27. **Equipment capability profiles need provenance + configuration context (not just point values)**:
   - Metrics like power and ground pressure depend on measurement basis (engine/PTO/drawbar) and equipment configuration (tires/tracks, inflation/ballast); capability profiles should record source/test basis and key configuration parameters for defensible field suitability decisions.
28. **Equipment suitability evaluations need structured reasons/mitigations + ruleset provenance**:
   - Fit/unsafe decisions should not be free-text only; they need coded reasons and mitigations plus a method/ruleset reference so results are defensible, comparable, and reproducible.
29. **Seed lot quality/health needs test-date + evidence + treatment/certification identifiers, not just booleans**:
   - Germination/purity values require test completion date and provenance, certified seed needs certifying agency/class identifiers, and treated seed needs substance/process disclosure; Farm-RM should link these records to evidence artifacts and allow optional vigor/health test references for establishment-risk use.
30. **Suitability/compatibility evaluations need structured missing-data + factor outputs and method provenance**:
   - A score/class alone is not defensible; evaluations should expose which inputs were missing and which factors/limitations drove the outcome, and record a method/ruleset reference so recommendations are reproducible and comparable over time.
31. **Variety trial results need structured trial design + management metadata for comparability**:
   - Site-year performance evidence is not interpretable without trial design (replications/design) and key management context (e.g., irrigated vs rainfed) and yield basis; evidence links help, but a minimal structured dataset improves interoperability and analysis.
32. **Variety risk profiles need explicit criteria/provenance and local-context input refs**:
   - Risk dimensions (lodging, disease susceptibility, drought mismatch, etc.) depend on environment and assumptions; Farm-RM should persist per-dimension risk classes with method provenance, confidence, and references to the pedoclimatic/disease-pressure context used.
33. **Duplicate "suitability" evaluation archetypes should be consolidated (two-level modeling)**:
   - `EVALUATION.seed_field_compatibility.*` and `EVALUATION.variety_field_suitability.*` overlap; Farm-RM should converge on one canonical suitability assessment archetype and use templates/profiles to specialize for seed-lot recommendations and jurisdiction/crop constraints.
34. **Planning artifacts need explicit approvals + linkage to evaluations (ranked plans and fallback options)**:
   - Variety/seed selection should be persisted as an approved plan object (ranked recommendations plus fallbacks) that links back to the suitability/risk evaluations and evidence basis used, instead of only free-text decisions or single-lot recommendations.
35. **Advisory outputs need first-class "evidence packages" with summaries/unknowns/penalties**:
   - Evidence links exist, but trust/auditability improve when we persist an explicit package snapshot that summarizes evidence tiers used, unknowns/missing critical inputs, and reasons for confidence penalties, instead of scattering that context across free text.
36. **Irrigation plans need decision-basis traceability + allocation/system constraints to be auditable**:
   - A plan should be able to reference the scheduling method/procedure (ET-based water balance vs soil moisture sensor, etc.) and relevant water-right/allocation constraints, and link back to the assessment/evidence basis used to create the plan; the current archetype is not integrated into the v1.7 ontology/SHACL/API/persistence stack.
37. **Irrigation events need measurement provenance + evidence links for auditability**:
   - Water volume values are only defensible if Farm-RM can capture how the volume was measured (flow meter vs runtime estimate vs controller report) and link to supporting evidence (logs/photos/exports) and allocation/right references when applicable.
38. **Irrigation need evaluations need explicit method + trigger metric/threshold structure (not just a boolean)**:
   - "Threshold crossed" must specify what metric was evaluated (e.g., depletion fraction, soil water potential, VWC) and what threshold/value/unit/ruleset was used; otherwise decisions are not comparable across sensors, advisors, and seasons.
39. **Water allocation/use reporting needs explicit accounting basis (withdrawn/applied/consumed) + measurement provenance**:
   - "Used volume" is ambiguous unless Farm-RM records what it represents and how it was measured/estimated, and ties summary snapshots back to raw water-use events for reconciliation/audit.
40. **Harvest records need measurement provenance + standards-based quality codes to support traceability**:
   - Yield/quality values are only interpretable if Farm-RM can reference how they were measured (yield monitor vs scale tickets) and capture moisture/grade with code-system context; harvest events should link cleanly to storage lots and downstream delivery/storage evidence.
41. **Delivery/weigh ticket records need explicit evidence attachment patterns and unambiguous unit semantics**:
   - Tickets are evidence artifacts; the archetype contract should include attachment roles/links, and quantity units like `bu` need commodity/context to avoid mixing mass and volume semantics under a single `weightUnit`.
42. **Storage condition snapshots need measurement-basis semantics and minimal device/procedure provenance**:
   - Grain-bin monitoring commonly aggregates multiple sensor/probe readings; a single temperature/moisture value should state whether it is a point vs max/avg/min summary and include minimal device/procedure references to keep snapshots comparable and audit-ready.
43. **Storage quality "state" needs explicit grade-system and loss-basis semantics (and transitions)**:
   - Quality grades are standards-based, and "loss %" is ambiguous without a basis (quantity vs value vs dry matter); Farm-RM needs structured quality state + transition records linked to condition observations and evidence to support traceability and value-at-risk workflows.
44. **Product sampling needs increment/composite metadata and a first-class sample->storage-lot link**:
   - Sampling dominates uncertainty for many quality/safety assays (e.g., mycotoxins); Farm-RM should capture minimal sampling plan metadata (increments, composite) and persist a direct linkage between the sample record and the storage lot/bin context.
45. **Quality panels need method-standard and grade-system provenance (and should align with persistence outputs)**:
   - Warehoused-lot release decisions depend on method-dependent measurements (lab vs NIR vs rapid tests) and (when grades are asserted) the grade system; Farm-RM should persist explicit provenance and keep archetype contracts aligned with actual API outputs (release recommendation, evidence links).
46. **Storage actions need explicit before/after condition observation links to support decision loops**:
   - Aeration/drying is condition-driven; records should directly reference the condition snapshots (before/during/after) that motivated the action and show outcomes, rather than relying on implicit correlation by timestamps alone.
47. **Equipment maintenance records need schedule/procedure provenance and outcome semantics (not just "service/repair")**:
   - Preventive maintenance is often executed on hour-based intervals from an operator manual; Farm-RM should be able to capture the schedule/procedure basis and whether work was completed vs follow-up required, and allow multiple evidence attachments (work orders/invoices/calibration sheets), not just a single evidence URI.
48. **Equipment cleanout needs first-class cleaning-agent identity + procedure references (and the archetype contract must match the API/DB)**:
   - Cleanout protocols often specify cleaning agents and multiple rinse/flush steps, and organic integrity depends on documented practices; Farm-RM should represent cleaning-agent identity (and optionally lot references) and procedure refs in the archetype itself, not only in API/DB extensions, and should support multiple evidence attachments.
49. **Cover crop records need explicit support for mixes and termination-stage semantics**:
   - Practice standards and research treat cover crops as species and mixes, and termination methods like roller-crimping depend on crop maturity; Farm-RM should be able to represent multi-species mixes (optionally with per-component rates) and capture a growth-stage code at termination when relevant.
50. **Compliance evidence "sets" are referenced by templates but not implemented as first-class admin records**:
   - Organic and regulatory workflows are audit-driven and time-bounded; Farm-RM needs a structured evidence packaging primitive that links scope (farm/field/jurisdiction/program) and period to underlying samples/assays/operations and attachments, and ties cleanly into submission packages/rendered reports.
