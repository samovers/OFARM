# OFARM staple-crop scenario stress test report

> Phase 9 currentness note (2026-05-18): this report is retained as active supporting research for an earlier package snapshot. Its `Package used` line and authority-order wording are historical report context only. The current package endpoint is `OFARM2_2026-05-17_agentic_ai_controlled_promotion_cp10_v0_1`, with active-law navigation governed by `CURRENT_ACTIVE_ENTRYPOINT.md` and `PROJECT_AUTHORITY.md`.


Date: 2026-04-14

Package used: `OFARM2_project_migration_seed_v0_6-4_with_economic_intelligence_consolidated_v0_1.zip` (newest package in sources)

## Scope and method

This report stress-tests the active OFARM 2 baseline against real-life staple-crop scenario families already preserved in the package supporting research (`06_active_supporting_research/syntheses/OFARM_research_real_farming_scenarios_v0_1.md`), then re-verifies the most load-bearing external farming realities against authoritative extension, regulatory, and grain-handling sources.

Authority posture used:
- Active law: `00_active_baseline/`, `01_companion_artifacts/`, `02_accepted_rfcs/`, `03_machine_contracts/`
- Supporting but non-overriding material: `04_implementation_and_conformance/`, `06_active_supporting_research/`
- Legacy material was not used as active law.

Baseline verdict carried into this report:
- OFARM is implementation-directed with bounded debt.
- The main remaining debt is conformance depth, trace-object formalization, and the still-dangerous lot family.
- This report does not reopen architecture. It identifies scenario-driven pressure points and the smallest controlled next expansions.

## Executive summary

1. **The most dangerous failures are routine, not exotic.** Partial replant, late contractor logs, ambiguous PPP records, wet grain held before drying, mixed organic/conventional handling, and field-geometry corrections are ordinary farm reality. Weak implementations fail here first.

2. **CropCycle identity is under immediate pressure from establishment reality.** OFARM law already distinguishes failed cycle versus replanted new cycle and allows overlaps, but partial replant inside one field still needs scenario fixtures that force deterministic lineage rather than silent overwrite.

3. **Wet grain and post-harvest storage are the strongest “freshness stress test” in the whole domain.** Grain condition is time-sensitive, cumulative, and operationally dangerous. OFARM’s freshness model is directionally right, but it needs campaign-grade fixtures for moisture/temperature condition decay, drying, aeration, and temporary storage.

4. **Lot remains the hardest object family exactly where real grain systems are messiest.** Split, merge, commingling, sublot testing, temporary storage, grading disputes, and mycotoxin-triggered diversion are normal enough that a weak lot implementation will produce either traceability fiction or identity explosion.

5. **Evidence quality is usually degraded before it is missing.** Real farms often have low-quality but existent evidence: notebook names instead of product IDs, partial ISOXML task data, late tickets, missing timestamps, or incomplete dryer logs. OFARM handles “do not auto-promote” well, but needs explicit evidence-quality downgrade and later-upgrade fixtures.

6. **Authority failures and freshness failures combine in long-running flows.** Contractor reporting, advisor-prepared filings, owner/operator/tenant signoff disputes, buyer read-only access, certifier review, and revocation mid-draft all hit the same seam: promotion-time re-evaluation with explicit traces.

7. **Pack conflict is not theoretical; it is the real shape of farming compliance.** Law, certification, crop-system, tooling, and local method packs co-activate routinely. OFARM’s hard-fail merge law is one of its strongest parts and should be tested directly against nutrient, organic, buyer-spec, and storage-handling combinations.

8. **Output taxonomy is a practical governance issue, not naming polish.** Drift claims, insurance cases, inspections, corrective actions, subsidy filings, and buyer deliveries are not all “passports”. OFARM’s PassportView vs DossierAssembly vs SubmissionAssembly split is correct and must be enforced in fixtures.

9. **The latest package already contains useful executable seed coverage, but not enough campaign realism.** Identity/lifecycle, lot commingling, authority, materialization, pack merge, and output-path fixtures exist. What is missing is multi-step farm campaign coverage spanning weeks, multiple actors, and late evidence.

10. **The next move should be scenario-library expansion, not architecture rewrite.** Almost all required action falls into implementation/conformance expansion, trace-object schema hardening, and a few small companion-artifact clarifications. This is consistent with the active package verdict.


## Scenario inventory

### 1. Patchy emergence and partial replant creates overlapping crop attempts
- Category: `planning_establishment`
- Commonness: Messy but common
- Stress priority: Critical
- Operational context: early-season establishment failure in patches; replant only in parts; sometimes with a different seed lot/variety.
- Key actors: owner/operator; agronomist; seed supplier.
- Key objects: Field, CropCycle (parent + partial “child”), seed lot evidence, scouting evidence.
- Likely event families: ObservationEvent (stand count), InterventionEvent (replant), StructureEvent (crop-cycle split/overlap relation).
- Likely commit classes: observation assertion → operation claim; possibly governance decision if compliance/insurance depends on it.
- Likely pack/context interactions: crop pack (maize/soy), insurance/subsidy pack, local “replant heuristics” pack; potential rule conflicts on “when is a new CropCycle”.
- Likely current-state / freshness issues: stale “current crop cycle” if replant hasn’t been accepted/promoted yet.
- Likely outputs: Field PassportView; CropCycle PassportView; potential insurance dossier/submission.
- Why it is hard for OFARM: forces deterministic identity/lifecycle decisions (same vs new cycle) plus explicit overlap lineage.
- Dominant OFARM risk clusters: identity/lifecycle; freshness; query/retrieval
- Baseline fit assessment: Partial — law strong, scenario fixture weak

### 2. Full crop failure → new crop planted (crop switch) within the same season
- Category: `planning_establishment`
- Commonness: Common after shock/failure
- Stress priority: Critical
- Operational context: crop fails (flood/hail/cold/heat) and farmer switches to another crop (or plants a cover crop) within the same field-year.
- Key actors: farmer; insurer; advisor; possibly inspector.
- Key objects: Field, CropCycle A (failed), CropCycle B (new), Occurrence evidence (weather/damage), seed purchase evidence.
- Likely event families: OccurrenceEvent (damage), GovernanceEvent (claim/decision), InterventionEvent (new planting), StructureEvent (cycle termination + successor).
- Likely commit classes: occurrence/observation assertions; operation claims; compliance assertions where relevant.
- Likely pack/context interactions: insurance/subsidy packs, regional agronomic packs; conflicting policies on “double cropping” or “practical to replant”.
- Likely current-state / freshness issues: high risk if a submission assembles using stale “crop-in-force” state.
- Likely outputs: DossierAssembly (insurance); SubmissionAssembly (area/crop declaration update).
- Why it is hard for OFARM: multi-temporal truth (event vs effective dates) + severe downstream consequences if cycle lineage is wrong.
- Dominant OFARM risk clusters: identity/lifecycle; freshness; output taxonomy
- Baseline fit assessment: Partial — law strong, multi-party filing fixture weak

### 3. Seed lot substitution mid-planting (mixed seed provenance inside one field)
- Category: `planning_establishment`
- Commonness: Common enough
- Stress priority: High
- Operational context: seed shortage or delivery delay; farmer switches seed lot or variety halfway through planting.
- Key actors: farmer; seed dealer; contractor planter.
- Key objects: AppliedResource (seed), CropCycle, ManagementZone (optional), evidence (tags, invoices).
- Likely event families: InterventionEvent (planting), EvidenceEvent (receipt/tag capture), ObservationEvent (emergence variability).
- Likely commit classes: operation claim + evidence record + later observation assertion.
- Likely pack/context interactions: certification (non-GMO/identity preserved) pack may require stronger evidence; crop-system pack may change phenology expectations.
- Likely current-state / freshness issues: later evidence arrival (seed invoice scanned weeks later) should update provenance without rewriting record-time.
- Likely outputs: CropCycle PassportView; buyer-facing Lot PassportView if identity-preserved marketing applies.
- Why it is hard for OFARM: “one crop cycle” but heterogeneous inputs → OFARM needs scoped input attribution without creating spurious new cycles.
- Dominant OFARM risk clusters: evidence; query/retrieval
- Baseline fit assessment: Partial — evidence/provenance law strong, scoped input attribution thin

### 4. Field boundary correction during the season (subsidy + operations mismatch)
- Category: `planning_establishment`
- Commonness: Common enough
- Stress priority: High
- Operational context: LPIS/IACS update or farmer correction changes eligible area; operations already recorded on old geometry.
- Key actors: farmer; agency; advisor.
- Key objects: Field identity revision; historical operations; subsidy declaration evidence.
- Likely event families: StructureEvent (field revision), GovernanceEvent (submission / correction), InterventionEvent (operations tied to geometry).
- Likely commit classes: structure assertion; governance decision; evidence record.
- Likely pack/context interactions: “subsidy filing” pack may install stricter geometry constraints; scope conflict with farm’s operational mapping pack.
- Likely current-state / freshness issues: materialisation invalidation trigger due to identity revision affecting scope interpretation.
- Likely outputs: SubmissionAssembly (area/crop filing) and Field PassportView for audit.
- Why it is hard for OFARM: tests OFARM’s “same field, new revision” semantics and downstream query equivalence across revisions.
- Dominant OFARM risk clusters: identity/lifecycle; freshness; query/retrieval
- Baseline fit assessment: Strong in law, partial in executable fixtures

### 5. Relay/double cropping creates explicitly overlapping crop cycles
- Category: `planning_establishment`
- Commonness: Regionally common
- Stress priority: High
- Operational context: small grains followed by soybean, or undersowing/relay cropping creating concurrent cycles on the same field.
- Key actors: farmer; advisor; insurer.
- Key objects: Field; CropCycle A and B with overlap relation; interventions; yield measures.
- Likely event families: InterventionEvent (plant/harvest), StructureEvent (overlap relation/lineage), ObservationEvent (stage/yield).
- Likely commit classes: operation claims; observation assertions; possibly governance decision for insurance declarations.
- Likely pack/context interactions: policies diverge strongly by region—some systems support double cropping in claims, some restrict; pack conflicts likely.
- Likely current-state / freshness issues: “current crop” view becomes ambiguous unless queries specify cycle identity and evaluation time.
- Likely outputs: CropCycle PassportViews for both cycles; possible SubmissionAssembly for insurance and acreage reporting.
- Why it is hard for OFARM: forces explicit overlap modelling (not silent overwrite) and robust querying.
- Dominant OFARM risk clusters: identity/lifecycle; query/retrieval; pack merge
- Baseline fit assessment: Strong in law, partial in query/output fixtures

### 6. Variable-rate fertiliser with partial machine logs and manual top-ups
- Category: `routine_operations`
- Commonness: Messy but common
- Stress priority: Critical
- Operational context: VR prescription applied; operator stops to refill; some passes recorded, others lost; manual correction later.
- Key actors: farmer; contractor; advisor (nutrient plan).
- Key objects: AppliedResource (fertiliser), Equipment, OperationRecord claims, machine task data, evidence (delivery note).
- Likely event families: InterventionEvent (application), EvidenceEvent (task file import), ObservationEvent (crop response).
- Likely commit classes: operation claim + evidence record; later correction/supersession.
- Likely pack/context interactions: NVZ/nutrient pack requires planning + record; equipment pack binds ISOXML/EFDI; potential merge on evidence policy.
- Likely current-state / freshness issues: “applied N to date” is high-consequence for compliance decisions; stale materialisation must block filings.
- Likely outputs: Field PassportView; compliance report; NVZ submission or inspection dossier.
- Why it is hard for OFARM: reconciling conflicting sources without letting projections become truth; strong need for evidence and supersession traces.
- Dominant OFARM risk clusters: evidence; freshness; query/retrieval
- Baseline fit assessment: Partial — event/evidence law strong, reconciliation fixture weak

### 7. Manure storage + closed periods + emergency spreading constraints
- Category: `routine_operations`
- Commonness: Common in regulated systems
- Stress priority: Critical
- Operational context: storage nearly full; weather blocks spreading; closed period approaching; risk-map and buffer rules apply.
- Key actors: farmer; advisor; regulator/inspector.
- Key objects: Facility/storage, AppliedResource (manure), Field constraints, evidence (plans, maps).
- Likely event families: StructureEvent (storage capacity change), InterventionEvent (spreading), GovernanceEvent (inspection/nonconformity).
- Likely commit classes: structure assertion; operation claim; compliance assertion; governance decision (NC/corrective action).
- Likely pack/context interactions: NVZ/law pack plus local “risk map” templates; high precedence constraints over method convenience.
- Likely current-state / freshness issues: time-policy triggers (crossing closed period boundary) can invalidate pre-planned actions.
- Likely outputs: SubmissionAssembly (records), DossierAssembly (inspection), corrective-action report.
- Why it is hard for OFARM: time-sensitive compliance rules + multi-party evidence—classic “freshness is purpose-sensitive” test.
- Dominant OFARM risk clusters: freshness; authority; output taxonomy
- Baseline fit assessment: Partial — freshness/authority law strong, domain packs/templates missing

### 8. PPP application record is required, but product identity is ambiguous (label vs local name)
- Category: `routine_operations`
- Commonness: Messy but common
- Stress priority: Critical
- Operational context: operator records “fungicide X” in notebook; later needs exact authorisation number / formulation; digital record expectations rise.
- Key actors: farmer; contractor sprayer; advisor; auditor.
- Key objects: AppliedResource (PPP), evidence (label photo, invoice), operation claim record.
- Likely event families: InterventionEvent (spray), EvidenceEvent (label capture), GovernanceEvent (audit/inspection).
- Likely commit classes: operation claim + evidence record; later correction.
- Likely pack/context interactions: jurisdiction/regulatory pack defines required fields; certification pack may add stricter evidence retention.
- Likely current-state / freshness issues: late evidence arrival after inspection dossier assembly.
- Likely outputs: Field/CropCycle passport; inspection dossier; submission package.
- Why it is hard for OFARM: forces OFARM to support “evidence that exists but is low quality” and upgrade pathways without rewriting history.
- Dominant OFARM risk clusters: evidence; pack merge; output taxonomy
- Baseline fit assessment: Partial — evidence law strong, vocabulary/low-quality upgrade path thin

### 9. Spray drift allegation affecting an organic neighbour
- Category: `routine_operations`
- Commonness: Less common, high consequence
- Stress priority: Critical
- Operational context: neighbour claims drift; organic integrity at risk; investigation requires weather, operation details, buffer compliance, and dispute handling.
- Key actors: conventional farmer; organic neighbour; advisor; certifier/inspector; possibly insurer.
- Key objects: Field(s), OperationClaim, Occurrence evidence (wind), lab residues, boundary buffers.
- Likely event families: OccurrenceEvent (drift incident), ObservationEvent (residue test), GovernanceEvent (dispute/decision), EvidenceEvent (lab report).
- Likely commit classes: occurrence/observation assertions; compliance assertions; governance decisions.
- Likely pack/context interactions: organic certification pack vs pesticide safety pack; likely pack conflict on evidence sufficiency and outputs.
- Likely current-state / freshness issues: high-consequence decisions must recompute current state before attested outputs.
- Likely outputs: DossierAssembly (case), possibly a corrective-action report.
- Why it is hard for OFARM: multi-party authority, contested truth, and output taxonomy discipline (this is a dossier, not a “passport”).
- Dominant OFARM risk clusters: authority; evidence; output taxonomy; pack merge
- Baseline fit assessment: Partial — dossier/authority law strong, cross-farm dispute fixture weak

### 10. Irrigation event with sensor telemetry vs human report mismatch
- Category: `routine_operations`
- Commonness: Common where irrigation/telemetry exist
- Stress priority: High
- Operational context: irrigation performed; telemetry says shorter duration; human claims full application; water restrictions or permits may require accurate records.
- Key actors: farmer; irrigation manager; water authority (region-specific).
- Key objects: Equipment, OperationClaim, sensor evidence, advisory outputs.
- Likely event families: InterventionEvent (irrigation), EvidenceEvent (telemetry capture), GovernanceEvent (audit if regulated).
- Likely commit classes: operation claim + evidence record; possibly governance decision.
- Likely pack/context interactions: water-use compliance pack; equipment telemetry mapping pack; potential merge on evidence policy and validation rules.
- Likely current-state / freshness issues: irrigation scheduling advice is tolerant of stale state; compliance is not—tests twin boundary + bridge rule.
- Likely outputs: advisory report vs compliance submission (must stay distinct).
- Why it is hard for OFARM: “machine-generated vs reported” reconciliation plus twin separation.
- Dominant OFARM risk clusters: evidence; freshness; authority
- Baseline fit assessment: Partial — twin boundary strong, telemetry contradiction fixture weak

### 11. Weak-signal disease suspicion → lab confirmation arrives late
- Category: `observation_decision`
- Commonness: Messy but common
- Stress priority: High
- Operational context: scout suspects rust/FHB; sends sample; corrective spray decision happens before lab return; lab report arrives after the spray.
- Key actors: farmer; advisor; lab; contractor sprayer.
- Key objects: Observation evidence (photos), lab report, intervention operation, hypotheses.
- Likely event families: ObservationEvent (scouting/sample), EvidenceEvent (lab certificate), InterventionEvent (spray), GovernanceEvent (if compliance claim depends on confirmation).
- Likely commit classes: hypothesis assertion → observation assertion; evidence record; advisory output; operation claim.
- Likely pack/context interactions: crop-protection pack may demand threshold logic; certification pack may constrain spray choices.
- Likely current-state / freshness issues: “current disease state” is inherently uncertain; OFARM must allow competing hypotheses in Advisory Twin but block fake certainty in Compliance Twin.
- Likely outputs: advisory risk report; later inspection dossier might need the lab report linkage.
- Why it is hard for OFARM: contradictions & uncertainty discipline under real decision pressure.
- Dominant OFARM risk clusters: evidence; freshness; query/retrieval
- Baseline fit assessment: Strong in twin law, partial in late-lab workflow fixtures

### 12. Remote sensing shows “stress”; scout says “fine” (contradictory observations)
- Category: `observation_decision`
- Commonness: Common enough
- Stress priority: Medium
- Operational context: EO/NDVI highlights a patch; field walk contradicts; later yield map supports one side.
- Key actors: farmer; advisor; remote-sensing provider.
- Key objects: Observation events (EO), narrative observations, hypotheses, crop zones (ephemeral vs durable).
- Likely event families: ObservationEvent; possibly StructureEvent if a zone becomes governed.
- Likely commit classes: observation assertion; hypothesis assertion; advisory output.
- Likely pack/context interactions: advisory pack introduces EO layers; must not silently create constitutional zones unless explicitly governed.
- Likely current-state / freshness issues: EO snapshots are time-sensitive; stale imagery can mislead operations.
- Likely outputs: advisory prioritisation view; Field PassportView should clearly label source and time.
- Why it is hard for OFARM: durable-vs-ephemeral zone rule + query provenance constraints.
- Dominant OFARM risk clusters: query/retrieval; freshness; identity/lifecycle
- Baseline fit assessment: Strong in advisory/ephemeral-zone law, partial in provenance-heavy views

### 13. Local microclimate frost/hail incident triggers damage claims
- Category: `observation_decision`
- Commonness: Periodic but common enough
- Stress priority: High
- Operational context: damage is spatially uneven; loss adjuster/insurer needs documented timing, extent, and pre/post photos; operations afterwards (replant, salvage for forage) depend on claim rules.
- Key actors: farmer; insurer/adjuster; advisor.
- Key objects: OccurrenceEvent evidence, crop-cycle status, salvage intervention.
- Likely event families: OccurrenceEvent, ObservationEvent, GovernanceEvent, InterventionEvent.
- Likely commit classes: occurrence assertion; evidence records; governance decision.
- Likely pack/context interactions: insurance pack; microclimate pack; crop pack; potential decision-rule conflicts.
- Likely current-state / freshness issues: governance decisions depend on as-of state at incident time, not “now”.
- Likely outputs: DossierAssembly (insurance).
- Why it is hard for OFARM: multi-temporal modelling + high-consequence outputs with required basis snapshots.
- Dominant OFARM risk clusters: freshness; output taxonomy; evidence
- Baseline fit assessment: Partial — as-of state law strong, insurer dossier fixture weak

### 14. Harvest at high moisture → safe storage period countdown
- Category: `harvest_postharvest`
- Commonness: Messy but common
- Stress priority: Critical
- Operational context: corn comes off wet; may be held “a bit” in a truck, floor pile, or bin before drying; safe storage time decreases rapidly with higher moisture and temperature.
- Key actors: farmer; drying service; buyer.
- Key objects: CropCycle harvest action, Lot creation, Facility/StorageLocation, drying intervention, moisture evidence.
- Likely event families: InterventionEvent (harvest/drying), MaterialEvent (lot creation/movement), ObservationEvent (moisture tests).
- Likely commit classes: operation claim; evidence record; observation assertion.
- Likely pack/context interactions: post-harvest handling pack; buyer contract pack (moisture specs and discounts).
- Likely current-state / freshness issues: material state (moisture/temp) is perishable; stale state is dangerous for operational decisions.
- Likely outputs: Lot PassportView; buyer delivery report.
- Why it is hard for OFARM: OFARM must model “time-sensitive material condition” without collapsing it into a single static attribute.
- Dominant OFARM risk clusters: freshness; identity/lifecycle; query/retrieval
- Baseline fit assessment: Weakest operational gap — freshness law strong, perishable condition modeling thin

### 15. Drying damage and overdrying vs safe storage constraints
- Category: `harvest_postharvest`
- Commonness: Common enough
- Stress priority: High
- Operational context: overdrying causes cracking/darkening/seed damage; underdrying raises mould/insect risk; dryer logs may be incomplete.
- Key actors: farmer; dryer operator; buyer.
- Key objects: Lot, Facility, drying equipment, quality tests.
- Likely event families: InterventionEvent (drying), ObservationEvent (quality/moisture), EvidenceEvent (dryer logs).
- Likely commit classes: operation claim; evidence records; observation assertions.
- Likely pack/context interactions: quality grading pack; safety pack; potential evidence-policy strengthening for attested outputs.
- Likely current-state / freshness issues: drying parameters are needed “as-of drying time”, not later edited guesses.
- Likely outputs: lot quality report; dispute dossier if rejected.
- Why it is hard for OFARM: requires rigorous evidence/provenance handling and correction without deleting history.
- Dominant OFARM risk clusters: evidence; freshness; output taxonomy
- Baseline fit assessment: Partial — evidence/provenance strong, dryer-log semantics thin

### 16. Bin sanitation failure → insects migrate from old residues into new grain
- Category: `harvest_postharvest`
- Commonness: Common and avoidable
- Stress priority: High
- Operational context: guidance repeatedly warns that leftover grain/dust can seed infestations; “do not put new grain on top of old grain” is a common rule-of-thumb; clean bins and equipment weeks before harvest.
- Key actors: farmer; workers; pest-control provider.
- Key objects: Facility/StorageLocation, Lot, evidence of cleaning actions, monitoring observations.
- Likely event families: InterventionEvent (cleaning/treatment), ObservationEvent (monitoring), OccurrenceEvent (infestation).
- Likely commit classes: operation claim; observation assertion; evidence record.
- Likely pack/context interactions: organic pack may limit chemical options; pest-control pack adds rules; safety pack.
- Likely current-state / freshness issues: repeated monitoring updates; state becomes stale quickly if not recalculated.
- Likely outputs: storage management report; organic inspection dossier if relevant.
- Why it is hard for OFARM: long-running maintenance campaign across multiple lots and containers—high query complexity and evidence volume.
- Dominant OFARM risk clusters: evidence; query/retrieval; freshness
- Baseline fit assessment: Partial — event model fits, long-running storage campaign fixtures weak

### 17. Aeration and temperature stratification creates hidden spoilage pockets
- Category: `harvest_postharvest`
- Commonness: Common enough in bins
- Stress priority: High
- Operational context: aeration is used to cool grain; cool temperatures reduce insect/mould activity; without proper aeration, temperature differentials build.
- Key actors: farmer; storage manager.
- Key objects: Facility, Lot, aeration equipment, temperature cables.
- Likely event families: InterventionEvent (aeration run), ObservationEvent (temperature readings), OccurrenceEvent (heating/mould).
- Likely commit classes: observation assertions; operation claims; evidence records.
- Likely pack/context interactions: storage management pack; equipment telemetry pack.
- Likely current-state / freshness issues: operational decisions rely on current readings; stale materialisation should be marked and policy-limited.
- Likely outputs: Facility PassportView and Lot PassportView.
- Why it is hard for OFARM: high-frequency observations, potentially offline, requiring robust sync and materialisation policies.
- Dominant OFARM risk clusters: freshness; query/retrieval; evidence
- Baseline fit assessment: Partial — materialization law fits, high-frequency telemetry/offline fixtures weak

### 18. Lot creation from harvest stream → split into bins → partial merge later
- Category: `harvest_postharvest`
- Commonness: Messy but common
- Stress priority: Critical
- Operational context: one field harvested over days; grain placed into multiple bins; later blended for shipment; quality varies by load.
- Key actors: farmer; buyer; sometimes elevator.
- Key objects: Lot identities, StorageLocations, Container occupancy episodes, lineage relations.
- Likely event families: MaterialEvent (create/split/merge), InterventionEvent (harvest/handling), ObservationEvent (grading/moisture).
- Likely commit classes: operation claim; observation assertion; evidence record.
- Likely pack/context interactions: traceability pack; buyer contract pack; potential view shaping for buyer vs internal.
- Likely current-state / freshness issues: “what is in this bin now” is a governed current-state question—materialisation critical.
- Likely outputs: Lot PassportView; ReportAssembly for shipment lot composition.
- Why it is hard for OFARM: OFARM Lot lifecycle rules + container/occupancy semantics must be honoured, or traceability collapses.
- Dominant OFARM risk clusters: identity/lifecycle; query/retrieval; freshness
- Baseline fit assessment: Partial to weak — lot law exists, bulk-campaign executable coverage thin

### 19. Grain delivery grading dispute (moisture/dockage/grade) with re-examination
- Category: `harvest_postharvest`
- Commonness: Common enough at delivery
- Stress priority: High
- Operational context: moisture meters differ; dockage and grade factors affect price; disputes can trigger formal re-check and written determinations.
- Key actors: farmer; elevator; inspector/regulator.
- Key objects: Lot, delivery tickets, official weigh/grade results, dispute case file.
- Likely event families: MaterialEvent (delivery), ObservationEvent (grade determination), GovernanceEvent (appeal/reinspection), EvidenceEvent (tickets/certificates).
- Likely commit classes: evidence record; governance decision; observation assertion.
- Likely pack/context interactions: buyer contract pack; grain standards pack; dossier templates.
- Likely current-state / freshness issues: dispute is about “as delivered” state; later storage changes must not rewrite it.
- Likely outputs: DossierAssembly (dispute); buyer-facing report.
- Why it is hard for OFARM: multi-party authority + immutable outputs + strong trace-back to basis.
- Dominant OFARM risk clusters: evidence; output taxonomy; authority
- Baseline fit assessment: Partial — governance/output law strong, grade-basis packs/dispute fixtures thin

### 20. Mycotoxin risk management across harvest/storage with buyer testing and rejection
- Category: `harvest_postharvest`
- Commonness: Less common, high consequence
- Stress priority: Critical
- Operational context: mycotoxins can arise pre- and post-harvest; post-harvest handling/drying/storage is critical; some buyers test for DON/aflatoxin and reject sublots over thresholds.
- Key actors: farmer; buyer; lab; possibly regulator.
- Key objects: Lot, lab certificates, storage records, diversion decision (feed vs food).
- Likely event families: ObservationEvent (testing), EvidenceEvent (lab report), GovernanceEvent (accept/reject), MaterialEvent (diversion/disposal).
- Likely commit classes: observation assertions; evidence record; governance decision.
- Likely pack/context interactions: food-safety pack; buyer-spec pack; evidence-policy strengthening.
- Likely current-state / freshness issues: test results are per-sublot/time; later merges must preserve which sublot was tested.
- Likely outputs: DossierAssembly (food safety); compliance submission if required.
- Why it is hard for OFARM: forces sublot semantics and identity discipline; easy place for weak implementations to “average away” danger.
- Dominant OFARM risk clusters: identity/lifecycle; evidence; output taxonomy
- Baseline fit assessment: Partial to weak — sublot identity and claim propagation remain dangerous

### 21. Organic + conventional share equipment and storage (commingling prevention plan under stress)
- Category: `compliance_inspection`
- Commonness: Messy but common on mixed farms
- Stress priority: Critical
- Operational context: same auger/truck/bin used; cleaning is imperfect; paperwork exists but execution is messy.
- Key actors: farmer; organic certifier/inspector; buyer.
- Key objects: Facility, Container, Lot, cleaning interventions, commingling risk evidence, organic system plan records.
- Likely event families: InterventionEvent (cleanout), MaterialEvent (lot movement), GovernanceEvent (inspection/nonconformity), EvidenceEvent (records).
- Likely commit classes: operation claim; evidence record; compliance assertion; governance decision.
- Likely pack/context interactions: organic certification pack imposes segregation controls; local method pack may conflict with evidence requirements.
- Likely current-state / freshness issues: after a commingling incident, prior “organic lot state” may become INVALID for compliance use.
- Likely outputs: Inspection dossier; corrected lot passport; possibly nonconformity + corrective action.
- Why it is hard for OFARM: simultaneously tests lots, facilities/containers, evidence sufficiency, and output taxonomy.
- Dominant OFARM risk clusters: identity/lifecycle; pack merge; evidence; output taxonomy
- Baseline fit assessment: Partial to weak — lot/evidence/output law fits, mixed-context segregation stress is severe

### 22. Temporary storage outside “normal facilities” (piles, bags, drums) under weather risk
- Category: `harvest_postharvest`
- Commonness: Periodic but common under capacity stress
- Stress priority: High
- Operational context: bumper harvest or bin shortage; temporary storage used; moisture ingress and contamination risk increase; practices vary by region.
- Key actors: farmer; workers; buyer.
- Key objects: StorageLocation, Container, Lot, evidence of conditions.
- Likely event families: MaterialEvent (move to temporary storage), OccurrenceEvent (rain ingress), ObservationEvent (moisture/condition).
- Likely commit classes: observation assertion; evidence record; operation claim.
- Likely pack/context interactions: post-harvest pack; organic pack may restrict allowable surfaces/containers.
- Likely current-state / freshness issues: condition changes quickly; late observations can invalidate earlier “safe” state.
- Likely outputs: Facility/Lot passports; buyer report.
- Why it is hard for OFARM: stresses container identity vs occupant identity and “current-state is derivative and explainable” requirement.
- Dominant OFARM risk clusters: identity/lifecycle; freshness; evidence
- Baseline fit assessment: Partial — container/storage identity law strong, temporary-storage risk policies thin

### 23. Contractor executes operation but provides late/partial records
- Category: `authority_sharing`
- Commonness: Very common
- Stress priority: Critical
- Operational context: custom applicator plants/sprays/harvests; farmer receives an invoice, maybe an ISOXML file later; details missing (rate, product ID, time).
- Key actors: contractor; farmer; advisor; auditor.
- Key objects: OperationClaims, EvidenceRecords, DelegationGrant (if contractor is allowed to report).
- Likely event families: InterventionEvent, EvidenceEvent, GovernanceEvent (if audited).
- Likely commit classes: operation claim; evidence record; governance decision if contested.
- Likely pack/context interactions: integration pack for task data; compliance pack requiring record completeness; pack merge risk on evidence-policy rules.
- Likely current-state / freshness issues: revocation or changed delegation can occur before contractor “finalises” reported execution.
- Likely outputs: Field passport; compliance dossier.
- Why it is hard for OFARM: this is the archetypal stress test for executable authority with delegation and revocation re-check at promotion time.
- Dominant OFARM risk clusters: authority; evidence; freshness
- Baseline fit assessment: Strong in authority law, partial in ingest/evidence-quality upgrade fixtures

### 24. Owner vs operator vs tenant disagreement over who can approve compliance submissions
- Category: `authority_sharing`
- Commonness: Common enough in leased/contracted land
- Stress priority: Critical
- Operational context: land is owned by Party A, farmed by Party B, compliance obligations shared; approvals and signatures are disputed.
- Key actors: owner; tenant/operator; advisor; certifier.
- Key objects: AuthorityGrants, RoleAssignments, RevocationDecisions, SubmissionAssembly drafts.
- Likely event families: GovernanceEvent (approval/attestation), StructureEvent (role assignment change).
- Likely commit classes: governance decision; compliance assertion; evidence record.
- Likely pack/context interactions: certification pack defines who must attest; governance pack defines action-class requirements.
- Likely current-state / freshness issues: long-running “draft submission” crosses revocation boundary; must re-evaluate authority at final promotion.
- Likely outputs: SubmissionAssembly with attestation trace.
- Why it is hard for OFARM: directly exercises AuthorityActionClass, default-deny, human-only attestation defaults, and decision traces.
- Dominant OFARM risk clusters: authority; output taxonomy; freshness
- Baseline fit assessment: Strong in authority law, partial in multi-signatory/revocation permutations

### 25. Advisor-prepared filing that requires human approval and traceable AI assistance
- Category: `authority_sharing`
- Commonness: Increasingly common
- Stress priority: Critical
- Operational context: advisor (or AI tool) drafts nutrient plan, spray log, or organic system update; farmer must approve; AI may be used for assembly.
- Key actors: advisor; farmer; software agent.
- Key objects: draft assertions, AuthorizationDecisionTrace, AI-assisted action markers, DocumentAssembly drafts.
- Likely event families: GovernanceEvent (approve/attest), EvidenceEvent (assembly).
- Likely commit classes: compliance assertion; governance decision; evidence record.
- Likely pack/context interactions: authority pack with AI rules; evidence policy may require human approval for final submission.
- Likely current-state / freshness issues: if underlying current-state materialisation is stale, final assembly must block.
- Likely outputs: SubmissionAssembly.
- Why it is hard for OFARM: stresses REQUIRE_HUMAN_APPROVAL outcome and “assistance is not authority borrowing”.
- Dominant OFARM risk clusters: authority; freshness; output taxonomy
- Baseline fit assessment: Strong in authority law, partial in stale-state + AI-assisted filing chain

### 26. Buyer requests read-only access to a lot, then disputes identity and demands deeper history
- Category: `authority_sharing`
- Commonness: Common enough in traceability-heavy sales
- Stress priority: High
- Operational context: buyer contract needs traceability; buyer wants lot passport; later disputes attributes (e.g., “same lot?”) and requests more evidence.
- Key actors: farmer; buyer; possibly auditor.
- Key objects: SharingGrants, Lot passport view, evidence bundles, lineage relations.
- Likely event families: GovernanceEvent (sharing grant), MaterialEvent (lot lineage), EvidenceEvent (bundle).
- Likely commit classes: evidence record; governance decision.
- Likely pack/context interactions: buyer “profile” for the Lot PassportView; data sovereignty boundary must prevent silent over-sharing.
- Likely current-state / freshness issues: buyer requests “current lot state”; must be generated from a clear context snapshot and basis.
- Likely outputs: Lot PassportView; possibly a ReportAssembly for contractual delivery.
- Why it is hard for OFARM: stresses output taxonomy (passport vs report), scoped sharing, and query reproducibility under different recipient profiles.
- Dominant OFARM risk clusters: authority; output taxonomy; query/retrieval
- Baseline fit assessment: Strong in sharing law, partial in recipient-profile deep-history retrieval

### 27. Certifier inspection finds missing evidence, issues nonconformity, and requires corrective action
- Category: `compliance_inspection`
- Commonness: Common enough
- Stress priority: Critical
- Operational context: inspection asks for spray logs, cleaning records, invoices; gaps exist; corrective actions required.
- Key actors: farmer; certifier/inspector.
- Key objects: InspectionCase, NonConformity, CorrectiveAction, evidence bundle.
- Likely event families: GovernanceEvent (inspection/NC), EvidenceEvent (late uploads).
- Likely commit classes: compliance assertion; governance decision; evidence record.
- Likely pack/context interactions: certification pack; evidence policy pack; document assembly shaping for dossier.
- Likely current-state / freshness issues: dossier assembled from stale state is unacceptable; must snapshot basis.
- Likely outputs: DossierAssembly; later SubmissionAssembly for corrective-action completion.
- Why it is hard for OFARM: stresses evidence sufficiency gating + supersession after a dossier already circulated.
- Dominant OFARM risk clusters: evidence; output taxonomy; freshness
- Baseline fit assessment: Partial — evidence/dossier/submission law strong, corrective-action campaigns thin

### 28. Pack conflict—two same-precedence packs touch evidence policy or decision rules for the same operation
- Category: `heavy_ugly`
- Commonness: Rare per pack pair, dangerous when it happens
- Stress priority: Critical
- Operational context: certification pack and local/community pack both define evidence sufficiency or decision rules; overlap is not declared safely mergeable.
- Key actors: farm governance steward.
- Key objects: PackActivationSet, PackMergeResolutionTrace, evidence policy modules, decision-rule modules.
- Likely event families: StructureEvent (pack activation), GovernanceEvent (compatibility decision).
- Likely commit classes: governance decision; structure assertion.
- Likely pack/context interactions: surface family = EVIDENCE_POLICY or DECISION_RULE; safe merge modes differ and may HARD_FAIL without declared legality.
- Likely current-state / freshness issues: pack activation changes context snapshot and can invalidate current-state materialisations.
- Likely outputs: Pack conflict report; governance dossier.
- Why it is hard for OFARM: deterministic failure behaviour is required; “prompt the user” is explicitly discouraged.
- Dominant OFARM risk clusters: pack merge; freshness; authority
- Baseline fit assessment: Strong — pack law and hard-fail posture are explicit and executable

### 29. Late evidence after a formal submission was assembled
- Category: `heavy_ugly`
- Commonness: Messy but common
- Stress priority: Critical
- Operational context: submission filed; later missing lab report / ticket appears; must supersede or append without invalidating audit trail.
- Key actors: farmer; advisor; authority/agency.
- Key objects: EvidenceRecord late arrival; SubmissionAssembly; ReviewDecision supersession; MaterializationSnapshot of what was relied upon.
- Likely event families: EvidenceEvent (late receipt), GovernanceEvent (supersede), possibly StructureEvent if scope identity revisions involved.
- Likely commit classes: evidence record; governance decision.
- Likely pack/context interactions: submission shaping + evidence policy; stricter retention for attested outputs.
- Likely current-state / freshness issues: correction should not rewrite prior “generated-at” basis; new submission version required.
- Likely outputs: new SubmissionAssembly version; trace to prior.
- Why it is hard for OFARM: large stressor for supersession law, basis snapshots, and externally-visible corrections.
- Dominant OFARM risk clusters: evidence; freshness; output taxonomy
- Baseline fit assessment: Strong in supersession law, partial in post-filing correction workflows

## Top stress-test scenarios

These 20 scenario families are the most likely to break a weak implementation because they combine high operational frequency, multiple actors, and high-consequence governance:

1. Partial replant inside one field
2. Crop switch after failure with insurance/subsidy linkage
3. Variable-rate fertiliser with partial machine logs and manual top-ups
4. Manure storage + closed periods + emergency spreading constraints
5. PPP application record with ambiguous product identity
6. Spray drift allegation affecting an organic neighbour
7. Harvest at high moisture → safe storage period countdown
8. Drying damage and overdrying vs safe storage constraints
9. Bin sanitation failure → insects migrate from old residues into new grain
10. Aeration and temperature stratification creates hidden spoilage pockets
11. Lot creation from harvest stream → split into bins → partial merge later
12. Grain delivery grading dispute with re-examination
13. Mycotoxin risk management across harvest/storage with buyer testing and rejection
14. Organic + conventional share equipment and storage
15. Temporary storage outside normal facilities under weather risk
16. Contractor executes operation but provides late/partial records
17. Owner vs operator vs tenant disagreement over submission approval
18. Advisor-prepared filing that requires human approval and traceable AI assistance
19. Pack conflict on evidence policy or decision rules
20. Late evidence after a formal submission was assembled

## Scenario clusters by OFARM risk

### Identity/lifecycle risk
Primary scenarios:
- partial replant
- crop switch after failure
- relay/double cropping overlap
- field boundary correction during the season
- lot split/merge/commingling
- temporary storage and reusable container occupancy
- mycotoxin-triggered sublot diversion

Stress verdict:
- **Strong in law, partial in executable realism.**
- RC2.1 and the identity RFC already distinguish durable identity, identity revision, and time-bounded state, and explicitly cover field revision, CropCycle replant/overlap, lot split/merge/commingling, and container occupancy.
- The main weakness is not semantic absence; it is insufficient multi-step campaign fixtures, especially for bulk grain and partial re-establishment.

### Current-state freshness risk
Primary scenarios:
- wet grain held before drying
- aeration and hidden spoilage pockets
- manure closed-period crossing
- stale filing after geometry revision
- long-running submission draft crossing revocation or evidence-arrival boundary
- irrigation telemetry mismatch
- late lab report after operational decision

Stress verdict:
- **Strong architectural law, still thin on high-frequency and cross-step fixtures.**
- OFARM’s FRESH / STALE / INVALID model, invalidation triggers, and high-consequence recompute/refuse rule are exactly the right answer.
- What is still thin is campaign-grade execution evidence: repeated material condition updates, edge/offline timing, and output-path refusal after freshness drift.

### Pack merge risk
Primary scenarios:
- nutrient/NVZ + local method packs
- organic + local handling pack
- certification + buyer-spec pack
- storage-handling + telemetry pack
- same-precedence evidence-policy conflict
- decision-rule conflict on operation acceptance or compliance sufficiency

Stress verdict:
- **One of OFARM’s strongest areas.**
- Surface-specific merge law is explicit and already has machine contracts.
- The main next step is not new law; it is realistic co-activation fixture sets centered on common farm compliance combinations.

### Authority risk
Primary scenarios:
- contractor reports execution late
- owner/operator/tenant signoff conflict
- advisor-prepared filing requiring farmer approval
- buyer read-only passport access followed by deeper-history demand
- certifier inspection and corrective-action follow-up
- revocation during a long-running draft

Stress verdict:
- **Strong in law, partial in depth.**
- Action classes, default deny, scope inheritance, delegation, sharing, revocation, and AI-assisted human approval posture are explicit.
- The latest package also adds deeper authority-depth fixtures, but multi-hop delegation, deployment-collected authorization telemetry, and broader signatory permutations remain debt.

### Evidence risk
Primary scenarios:
- ambiguous PPP identity
- partial machine task logs
- handwritten or late tickets
- dryer logs missing fields
- weak-signal disease observations
- remote-sensing contradiction
- sanitation records and cleanout evidence
- lab certificates and reinspection outcomes

Stress verdict:
- **Architecturally strong, operationally under-fixtured.**
- OFARM’s commit/promotion law correctly prevents weak evidence from silently becoming hard truth.
- What is missing is a first-class graded evidence-quality pattern and upgrade-path fixtures for “exists but poor”, “late but stronger”, and “contradictory source tiers”.

### Output taxonomy risk
Primary scenarios:
- drift allegation case package
- grain grading dispute
- insurance frost/hail claim
- organic nonconformity and corrective action
- nutrient filing
- subsidy/geometry correction
- buyer lot summary versus contractual report

Stress verdict:
- **Strong and strategically important.**
- OFARM is right to separate live PassportViews from frozen reports, dossiers, and submissions.
- The main risk now is implementer drift back into “passport as catch-all”, especially for disputes and filings.

### Query / retrieval risk
Primary scenarios:
- what was true as-of incident time
- what is in bin X now
- which pack set governed this filing
- which evidence supported this accepted consequence
- which lot lineage path connects tested sublot to shipped lot
- what exactly the buyer can see versus the certifier can see

Stress verdict:
- **Semantically well-posed, operationally demanding.**
- QuerySpecification + QueryPlanIR + materialization basis are the right foundation.
- The biggest remaining challenge is campaign-scale retrieval across identity revisions, pack snapshots, recipient profiles, and late supersession.


## What must be added to conformance fixtures

The latest package already covers:
- field boundary revision vs split
- crop-cycle replant after failure
- lot commingling into new cohort identity
- relay/intercrop overlap
- delegated service-provider execution allow
- buyer write denial
- current-state recomputation on context drift
- dossier attestation and submission filing recomputation/refusal paths
- pack merge legality and hard fail paths
- explicit no-attestation and no-filing rule for PassportView

That is good baseline coverage, but it is still mostly **single-seam** coverage. The scenario library now needs **campaign realism**.

### High-priority fixture additions

1. **Partial replant campaign fixture**
   - Affected baseline files: none initially.
   - Change type: implementation/conformance implication.
   - Need: one field, one parent CropCycle, patch-level failure, partial replant, later harvest, insurance branch.
   - Required proofs: overlap lineage, zone-scoped query correctness, no silent overwrite of current crop state.

2. **Wet-grain campaign fixture**
   - Affected baseline files: none initially; possibly later companion note if condition-state vocabulary needs tightening.
   - Change type: implementation/conformance implication.
   - Need: harvest → temporary storage → moisture observation → drying → bin storage → buyer delivery.
   - Required proofs: condition observations stay time-bounded; stale condition blocks attested quality output; “what was in this bin when” remains reconstructable.

3. **Lot split/merge/sublot contamination fixture**
   - Affected baseline files: none initially.
   - Change type: implementation/conformance implication.
   - Need: harvest stream split into bins, one sublot tested, partial merge into shipment lot, buyer rejection.
   - Required proofs: tested sublot lineage is preserved; unsafe result does not silently propagate or disappear through merge.

4. **Organic/conventional mixed-farm segregation fixture**
   - Affected baseline files: none initially; later pack examples may help.
   - Change type: implementation/conformance implication.
   - Need: shared auger/truck/bin, cleaning records, certifier inspection, nonconformity, corrective action.
   - Required proofs: pack activation, evidence sufficiency, lot invalidation, dossier/submission outputs, sharing boundaries.

5. **PPP evidence-quality upgrade fixture**
   - Affected baseline files: likely `01_companion_artifacts/OFARM_Event_Grammar_and_Commit_Matrix_v0_1.md` and a new evidence-quality companion note if formalized.
   - Change type: small companion-artifact extension plus implementation/conformance implication.
   - Need: weak note (“fungicide X”), late label photo, invoice, authorisation number correction.
   - Required proofs: no auto-promotion to compliance fact; record time preserved; improved evidence can supersede without rewriting history.

6. **NVZ closed-period time-window fixture**
   - Affected baseline files: none initially.
   - Change type: implementation/conformance implication.
   - Need: planned spreading crosses closed period and storage-capacity pressure.
   - Required proofs: time-policy invalidation trigger; blocked filing; explicit corrective path.

7. **Contractor late-record / revocation-race fixture**
   - Affected baseline files: none initially.
   - Change type: implementation/conformance implication.
   - Need: contractor with delegated execution-report authority sends partial ISOXML/task data late; delegation narrows before final promotion.
   - Required proofs: allow report, deny compliance assertion, deny attestation, re-evaluate at promotion time.

8. **Post-filing late-evidence supersession fixture**
   - Affected baseline files: none initially; trace-object schema hardening would improve it.
   - Change type: implementation/conformance implication.
   - Need: filed SubmissionAssembly, late evidence arrival, superseding version.
   - Required proofs: previous basis snapshot preserved; new version created; no edit-in-place.

9. **Recipient-profile retrieval fixture**
   - Affected baseline files: none initially.
   - Change type: implementation/conformance implication.
   - Need: buyer, certifier, and farm operator query the same lot.
   - Required proofs: same underlying substrate, different sharing scope, different output family, deterministic trace-back.

10. **Storage campaign telemetry fixture**
    - Affected baseline files: none initially.
    - Change type: implementation/conformance implication.
    - Need: temperature cable data, aeration events, offline sync, spoilage alert, later query.
    - Required proofs: repeated observation events, freshness warnings, edge/offline reconciliation, no projection-as-truth shortcut.


## What OFARM already handles well vs weakly

### What OFARM already handles well

1. **Assertion/history-first truth discipline**
   - Real farm mess becomes survivable when imported logs, notes, scans, and AI suggestions do not become truth by default.
   - OFARM is strong here.

2. **Event grammar and commit/promotion separation**
   - This is exactly the right architecture for partial records, late evidence, ambiguous observations, and contested operations.
   - Weak farm systems usually fail because they flatten these distinctions.

3. **Identity/lifecycle law**
   - OFARM is unusually strong on field revision vs new field, failed vs replanted CropCycle, lot cohort continuity, and reusable container identity.
   - That is strategically correct for staple-crop operations.

4. **Freshness and high-consequence refusal**
   - OFARM’s current-state materialization model is one of the best parts of the baseline.
   - It is precisely what real filings, attestation, and dispute workflows need.

5. **Authority, delegation, sharing, and revocation**
   - OFARM is already better than most implementation baselines at separating “can see” from “can act”, and “can draft” from “can approve”.

6. **Pack merge law**
   - OFARM’s deterministic hard-fail posture is correct.
   - Real-world compliance stacks need this exact discipline.

7. **Output taxonomy**
   - The PassportView / ReportAssembly / DossierAssembly / SubmissionAssembly split is operationally right and should not be softened.

### What OFARM still handles weakly or only partially

1. **Bulk grain campaign realism**
   - The baseline knows what a lot is.
   - It is still not deeply stress-tested against real post-harvest campaigns with moisture, aeration, bin movement, sublots, grading, and disputes.

2. **Evidence-quality gradation**
   - OFARM correctly blocks auto-promotion.
   - It is less explicit about structured downgrade/upgrade handling for poor-but-real evidence.

3. **Trace-object formalization depth**
   - AuthorizationDecisionTrace and PackMergeResolutionTrace conceptually exist and the package now includes schemas/examples, but more schema rigor and wider scenario coverage would materially reduce implementation divergence.

4. **Deployment-collected telemetry for the hardest seams**
   - The package still lacks deployment-collected authorization telemetry, deployment-collected materialization telemetry, and live field-collected same-standard bridge telemetry.
   - That matters for real machinery and contractor scenarios.

5. **Multi-step campaign query fixtures**
   - OFARM query law is fine.
   - What is missing is enough campaign-scale regression evidence for “as-of incident”, “what is in this bin now”, and “which evidence supported this accepted consequence”.

6. **Lot sublot propagation and claim carry-over**
   - This remains the single highest divergence risk in the domain.


## Prioritized next actions

### Action 1 — Scenario fixture library
- Affected files: `04_implementation_and_conformance/` new fixture families, plus likely additions to `OFARM_conformance_seed_set_v0_1.md` and `OFARM_conformance_coverage_matrix_v0_1.md`
- Change type: implementation/conformance implication
- Priority: highest
- Reason: almost every stress point above is now architecture-ready but fixture-thin.

### Action 2 — Bulk grain campaign pack
- Affected files: primarily `04_implementation_and_conformance/`; possibly a small `01_companion_artifacts/` note if material-condition semantics need clearer canonical examples
- Change type: implementation/conformance implication first
- Priority: highest
- Reason: this concentrates lot, freshness, evidence, output, and query risk into a small number of realistic campaigns.

### Action 3 — Evidence-quality downgrade/upgrade pattern
- Affected files: likely a new companion artifact under `01_companion_artifacts/`, plus fixture work
- Change type: small controlled companion-artifact extension
- Priority: high
- Reason: many real farm records are not absent, just weak. OFARM needs a more explicit executable pattern for that.

### Action 4 — Mixed-context farm pack set
- Affected files: `04_implementation_and_conformance/` pack co-activation fixtures; optionally example pack manifests under supporting or machine-contract layers
- Change type: implementation/conformance implication
- Priority: high
- Reason: organic + conventional + nutrient + buyer-spec + machinery telemetry is the real-world multi-pack baseline.

### Action 5 — Post-filing correction workflow hardening
- Affected files: `03_machine_contracts/` and `04_implementation_and_conformance/`
- Change type: machine-contract and implementation/conformance implication
- Priority: high
- Reason: late evidence after filing is guaranteed in practice and directly tests snapshots, supersession, and external traceability.

### Action 6 — Multi-party authority depth expansion
- Affected files: `03_machine_contracts/` and `04_implementation_and_conformance/`
- Change type: machine-contract and implementation/conformance implication
- Priority: high
- Reason: contractor, advisor, buyer, certifier, owner, tenant, and software-agent interactions are routine enough to justify broader executable permutations.

### Action 7 — Do not reopen architecture
- Affected files: none
- Change type: governance posture
- Priority: constant
- Reason: the right move remains implementation-scale work plus deeper conformance expansion, not fresh redesign.

## Bottom line

Using the newest package in sources, the verdict is:

- **OFARM is structurally strong enough for these staple-crop scenarios.**
- **Its main failure risk is not missing architecture; it is insufficient scenario realism in executable conformance.**
- **The worst unresolved stressor is still lot-centric bulk grain traceability under freshness, evidence, and dispute pressure.**
- **The next correct move is a scenario fixture program centered on replant, wet grain, lot lineage, mixed-context segregation, contractor authority, and post-filing supersession.**


## External source families re-verified for scenario realism

Authoritative external anchors used to re-check the most load-bearing farming realities:
- Purdue, Missouri, Minnesota, Iowa State, Ohio State, Mississippi State and other extension sources on replant and stand failure
- University of Minnesota, NDSU, Oklahoma State, Missouri Extension and related extension sources on wet grain, allowable storage time, aeration, sanitation, and storage deterioration
- USDA AMS organic guidance on commingling prevention and organic system plans
- EUR-Lex and European Commission pages on plant protection product records, IACS, LPIS and geospatial aid applications
- GOV.UK guidance on NVZ storage, closed periods, fertiliser planning and recordkeeping
- Canadian Grain Commission guidance on moisture, dockage, reinspection, producer rights at delivery, and grain quality determinations
- AEF ISOBUS conformance and compatibility materials relevant to machine/task-data reliability
