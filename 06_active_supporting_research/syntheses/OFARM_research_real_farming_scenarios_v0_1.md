# Real-life staple crop farming scenarios to stress test OFARM before implementation

> Source note (migration cleanup, 2026-04-10): This report preserves a prior Deep Research synthesis. Inline web/file citation markers were removed during packaging cleanup because their source handles were not portable into the migrated project. Treat the report as supporting research and re-verify external claims before promoting any recommendation into active law.

## Executive summary

1) **Replant and partial re-establishment is a routine “identity breaker” in real farms, not an edge case.** Poor stands can arise from seed quality, planting depth, crusting, saturated soils, herbicide injury, insects and disease; replant decisions depend on cause and timing, and partial replant can create overlapping “attempts” on the same field. This is a direct stress test for OFARM’s **CropCycle new-identity vs same-cycle** rule, plus lineage for partial reconstitution.

2) **Wet grain + temporary storage + drying is a common operational sequence that creates high-consequence traceability and freshness risks.** Safe storage life depends on *moisture* and *temperature*; wet grain can only be held safely for limited periods, and drying quality matters (overdrying damage, cracks, quality loss). OFARM should treat “wet grain held overnight in a trailer / pile / bin” as normal and model it explicitly as events + material-state consequences.

3) **On-farm storage is a multi-operation campaign with visible failure modes (insects, mould, heating) that require repeated observation + intervention loops.** Multiple extension guides emphasise “start clean” (bin sanitation, remove old grain/dust) and then manage temperature via aeration, monitoring, and pest control; storage quality *never improves*, it only deteriorates more slowly with good practice. This forces OFARM to support **long-running, stateful storage episodes** and repeated evidence updates without turning every update into a new Lot identity.

4) **“Lot” is where bulk commodity reality collides with strict traceability: splitting, merging, commingling and reconditioning are operationally frequent.** Grain quality can vary truckload-to-truckload from a single field; grades/dockage/moisture are assessed on delivery and can be disputed and re-examined; bulk elevators are structurally prone to mixing unless designed otherwise. This aligns with OFARM’s own warning that “lot remains the most dangerous object family”.

5) **Organic + conventional coexistence on the same holding creates “messy but common” segregation scenarios (shared equipment, shared storage, shared transport).** Organic integrity depends on preventing commingling and prohibited-substance contact via documented practices and barriers; this is explicitly emphasised in USDA and EU-facing guidance. For OFARM, this is a combined stress test of **pack context**, **evidence policies**, **authority**, **outputs**, and **late dispute** handling.

6) **Plant protection product (PPP) record-keeping is getting stricter and more digitally shaped, so “machine records vs human records” will be a daily source of conflict.** EU Regulation (EU) 2023/564 updates professional-user PPP record-keeping expectations, and UK guidance ties pesticide use to “sustainable use” obligations; failures are often administrative rather than agronomic (missing fields, wrong product identifiers, timing gaps). OFARM must assume incomplete, late, and corrected pesticide records as normal.

7) **Nutrient management and manure rules create recurring “compliance-by-record” workflows tightly tied to time windows, buffers, and storage capacity.** NVZ-style regimes explicitly require planning and records, and include closed periods and storage constraints; this drives multi-party scenarios (advisor plans, operator spreads, inspector checks, regulator audits). It is tailor-made to stress OFARM’s **authority action classes**, **evidence sufficiency**, and **submission assemblies**.

8) **Subsidy/area-control reality (LPIS/IACS-style) turns field geometry revisions into operational events with financial consequences.** LPIS is a key control mechanism for CAP payments and depends on geospatial reference parcels; disputes or corrections can arise from remote sensing / imagery checks and lead to retroactive admin pressure. OFARM has to distinguish “field revision” from “new field identity” while keeping auditability for filings.

9) **Contractor work is not “just provenance”; it forces explicit delegation, revocation boundaries, and versioned evidence.** ISOXML/EFDI ecosystems exist precisely because task data is often malformed and needs validation; real deployments will see partial logs, corrupted files, and delayed exports. OFARM’s default-deny, action-class-based authorisation and delegation trace requirements are directly hit here.

10) **The highest-risk OFARM failures are not exotic agronomy—they’re governance/timing failures: stale current-state used in a high-consequence flow, conflicting packs on the same scope, late evidence after a submission, or revoked authority mid-draft.** RC2.1 explicitly defines freshness states (FRESH/STALE/INVALID) and a high-consequence recomputation/refusal rule; the hostile review still flags conformance depth and lot maturity as the key remaining risk.

## Scenario inventory

This inventory models “scenario families” rather than one-off anecdotes. Each scenario is written as something that a real farm could plausibly encounter in staple crops (cereals, maize/corn, oilseeds, pulses) and is mapped to OFARM’s event families and commit classes.

**Scenario: Patchy emergence and partial replant creates overlapping crop attempts**
Operational context: early-season establishment failure in patches; replant only in parts; sometimes with a different seed lot/variety.
Key actors: owner/operator; agronomist; seed supplier.
Key objects: Field, CropCycle (parent + partial “child”), seed lot evidence, scouting evidence.
Likely event families: ObservationEvent (stand count), InterventionEvent (replant), StructureEvent (crop-cycle split/overlap relation).
Likely commit classes: observation assertion → operation claim; possibly governance decision if compliance/insurance depends on it.
Pack/context: crop pack (maize/soy), insurance/subsidy pack, local “replant heuristics” pack; potential rule conflicts on “when is a new CropCycle”.
Freshness issues: stale “current crop cycle” if replant hasn’t been accepted/promoted yet.
Outputs: Field PassportView; CropCycle PassportView; potential insurance dossier/submission.
Why hard for OFARM: forces deterministic identity/lifecycle decisions (same vs new cycle) plus explicit overlap lineage.

**Scenario: Full crop failure → new crop planted (crop switch) within the same season**
Operational context: crop fails (flood/hail/cold/heat) and farmer switches to another crop (or plants a cover crop) within the same field-year.
Actors: farmer; insurer; advisor; possibly inspector.
Objects: Field, CropCycle A (failed), CropCycle B (new), Occurrence evidence (weather/damage), seed purchase evidence.
Event families: OccurrenceEvent (damage), GovernanceEvent (claim/decision), InterventionEvent (new planting), StructureEvent (cycle termination + successor).
Commit classes: occurrence/observation assertions; operation claims; compliance assertions where relevant.
Pack/context: insurance/subsidy packs, regional agronomic packs; conflicting policies on “double cropping” or “practical to replant”.
Freshness: high risk if a submission assembles using stale “crop-in-force” state.
Outputs: DossierAssembly (insurance); SubmissionAssembly (area/crop declaration update).
Hardness: multi-temporal truth (event vs effective dates) + severe downstream consequences if cycle lineage is wrong.

**Scenario: Seed lot substitution mid-planting (mixed seed provenance inside one field)**
Operational context: seed shortage or delivery delay; farmer switches seed lot or variety halfway through planting.
Actors: farmer; seed dealer; contractor planter.
Objects: AppliedResource (seed), CropCycle, ManagementZone (optional), evidence (tags, invoices).
Event families: InterventionEvent (planting), EvidenceEvent (receipt/tag capture), ObservationEvent (emergence variability).
Commit classes: operation claim + evidence record + later observation assertion.
Packs: certification (non-GMO/identity preserved) pack may require stronger evidence; crop-system pack may change phenology expectations.
Freshness: later evidence arrival (seed invoice scanned weeks later) should update provenance without rewriting record-time.
Outputs: CropCycle PassportView; buyer-facing Lot PassportView if identity-preserved marketing applies.
Hardness: “one crop cycle” but heterogeneous inputs → OFARM needs scoped input attribution without creating spurious new cycles.

**Scenario: Field boundary correction during the season (subsidy + operations mismatch)**
Operational context: LPIS/IACS update or farmer correction changes eligible area; operations already recorded on old geometry.
Actors: farmer; agency; advisor.
Objects: Field identity revision; historical operations; subsidy declaration evidence.
Event families: StructureEvent (field revision), GovernanceEvent (submission / correction), InterventionEvent (operations tied to geometry).
Commit classes: structure assertion; governance decision; evidence record.
Packs: “subsidy filing” pack may install stricter geometry constraints; scope conflict with farm’s operational mapping pack.
Freshness: materialisation invalidation trigger due to identity revision affecting scope interpretation.
Outputs: SubmissionAssembly (area/crop filing) and Field PassportView for audit.
Hardness: tests OFARM’s “same field, new revision” semantics and downstream query equivalence across revisions.

**Scenario: Relay/double cropping creates explicitly overlapping crop cycles**
Operational context: small grains followed by soybean, or undersowing/relay cropping creating concurrent cycles on the same field.
Actors: farmer; advisor; insurer.
Objects: Field; CropCycle A and B with overlap relation; interventions; yield measures.
Event families: InterventionEvent (plant/harvest), StructureEvent (overlap relation/lineage), ObservationEvent (stage/yield).
Commit classes: operation claims; observation assertions; possibly governance decision for insurance declarations.
Packs: policies diverge strongly by region—some systems support double cropping in claims, some restrict; pack conflicts likely.
Freshness: “current crop” view becomes ambiguous unless queries specify cycle identity and evaluation time.
Outputs: CropCycle PassportViews for both cycles; possible SubmissionAssembly for insurance and acreage reporting.
Hardness: forces explicit overlap modelling (not silent overwrite) and robust querying.

**Scenario: Variable-rate fertiliser with partial machine logs and manual top-ups**
Operational context: VR prescription applied; operator stops to refill; some passes recorded, others lost; manual correction later.
Actors: farmer; contractor; advisor (nutrient plan).
Objects: AppliedResource (fertiliser), Equipment, OperationRecord claims, machine task data, evidence (delivery note).
Event families: InterventionEvent (application), EvidenceEvent (task file import), ObservationEvent (crop response).
Commit classes: operation claim + evidence record; later correction/supersession.
Packs: NVZ/nutrient pack requires planning + record; equipment pack binds ISOXML/EFDI; potential merge on evidence policy.
Freshness: “applied N to date” is high-consequence for compliance decisions; stale materialisation must block filings.
Outputs: Field PassportView; compliance report; NVZ submission or inspection dossier.
Hardness: reconciling conflicting sources without letting projections become truth; strong need for evidence and supersession traces.

**Scenario: Manure storage + closed periods + emergency spreading constraints**
Operational context: storage nearly full; weather blocks spreading; closed period approaching; risk-map and buffer rules apply.
Actors: farmer; advisor; regulator/inspector.
Objects: Facility/storage, AppliedResource (manure), Field constraints, evidence (plans, maps).
Event families: StructureEvent (storage capacity change), InterventionEvent (spreading), GovernanceEvent (inspection/nonconformity).
Commit classes: structure assertion; operation claim; compliance assertion; governance decision (NC/corrective action).
Packs: NVZ/law pack plus local “risk map” templates; high precedence constraints over method convenience.
Freshness: time-policy triggers (crossing closed period boundary) can invalidate pre-planned actions.
Outputs: SubmissionAssembly (records), DossierAssembly (inspection), corrective-action report.
Hardness: time-sensitive compliance rules + multi-party evidence—classic “freshness is purpose-sensitive” test.

**Scenario: PPP application record is required, but product identity is ambiguous (label vs local name)**
Operational context: operator records “fungicide X” in notebook; later needs exact authorisation number / formulation; digital record expectations rise.
Actors: farmer; contractor sprayer; advisor; auditor.
Objects: AppliedResource (PPP), evidence (label photo, invoice), operation claim record.
Event families: InterventionEvent (spray), EvidenceEvent (label capture), GovernanceEvent (audit/inspection).
Commit classes: operation claim + evidence record; later correction.
Packs: jurisdiction/regulatory pack defines required fields; certification pack may add stricter evidence retention.
Freshness: late evidence arrival after inspection dossier assembly.
Outputs: Field/CropCycle passport; inspection dossier; submission package.
Hardness: forces OFARM to support “evidence that exists but is low quality” and upgrade pathways without rewriting history.

**Scenario: Spray drift allegation affecting an organic neighbour**
Operational context: neighbour claims drift; organic integrity at risk; investigation requires weather, operation details, buffer compliance, and dispute handling.
Actors: conventional farmer; organic neighbour; advisor; certifier/inspector; possibly insurer.
Objects: Field(s), OperationClaim, Occurrence evidence (wind), lab residues, boundary buffers.
Event families: OccurrenceEvent (drift incident), ObservationEvent (residue test), GovernanceEvent (dispute/decision), EvidenceEvent (lab report).
Commit classes: occurrence/observation assertions; compliance assertions; governance decisions.
Packs: organic certification pack vs pesticide safety pack; likely pack conflict on evidence sufficiency and outputs.
Freshness: high-consequence decisions must recompute current state before attested outputs.
Outputs: DossierAssembly (case), possibly a corrective-action report.
Hardness: multi-party authority, contested truth, and output taxonomy discipline (this is a dossier, not a “passport”).

**Scenario: Irrigation event with sensor telemetry vs human report mismatch**
Operational context: irrigation performed; telemetry says shorter duration; human claims full application; water restrictions or permits may require accurate records.
Actors: farmer; irrigation manager; water authority (region-specific).
Objects: Equipment, OperationClaim, sensor evidence, advisory outputs.
Event families: InterventionEvent (irrigation), EvidenceEvent (telemetry capture), GovernanceEvent (audit if regulated).
Commit classes: operation claim + evidence record; possibly governance decision.
Packs: water-use compliance pack; equipment telemetry mapping pack; potential merge on evidence policy and validation rules.
Freshness: irrigation scheduling advice is tolerant of stale state; compliance is not—tests twin boundary + bridge rule.
Outputs: advisory report vs compliance submission (must stay distinct).
Hardness: “machine-generated vs reported” reconciliation plus twin separation.

**Scenario: Weak-signal disease suspicion → lab confirmation arrives late**
Operational context: scout suspects rust/FHB; sends sample; corrective spray decision happens before lab return; lab report arrives after the spray.
Actors: farmer; advisor; lab; contractor sprayer.
Objects: Observation evidence (photos), lab report, intervention operation, hypotheses.
Event families: ObservationEvent (scouting/sample), EvidenceEvent (lab certificate), InterventionEvent (spray), GovernanceEvent (if compliance claim depends on confirmation).
Commit classes: hypothesis assertion → observation assertion; evidence record; advisory output; operation claim.
Packs: crop-protection pack may demand threshold logic; certification pack may constrain spray choices.
Freshness: “current disease state” is inherently uncertain; OFARM must allow competing hypotheses in Advisory Twin but block fake certainty in Compliance Twin.
Outputs: advisory risk report; later inspection dossier might need the lab report linkage.
Hardness: contradictions & uncertainty discipline under real decision pressure.

**Scenario: Remote sensing shows “stress”; scout says “fine” (contradictory observations)**
Operational context: EO/NDVI highlights a patch; field walk contradicts; later yield map supports one side.
Actors: farmer; advisor; remote-sensing provider.
Objects: Observation events (EO), narrative observations, hypotheses, crop zones (ephemeral vs durable).
Event families: ObservationEvent; possibly StructureEvent if a zone becomes governed.
Commit classes: observation assertion; hypothesis assertion; advisory output.
Packs: advisory pack introduces EO layers; must not silently create constitutional zones unless explicitly governed.
Freshness: EO snapshots are time-sensitive; stale imagery can mislead operations.
Outputs: advisory prioritisation view; Field PassportView should clearly label source and time.
Hardness: durable-vs-ephemeral zone rule + query provenance constraints.

**Scenario: Local microclimate frost/hail incident triggers damage claims**
Operational context: damage is spatially uneven; loss adjuster/insurer needs documented timing, extent, and pre/post photos; operations afterwards (replant, salvage for forage) depend on claim rules.
Actors: farmer; insurer/adjuster; advisor.
Objects: OccurrenceEvent evidence, crop-cycle status, salvage intervention.
Event families: OccurrenceEvent, ObservationEvent, GovernanceEvent, InterventionEvent.
Commit classes: occurrence assertion; evidence records; governance decision.
Packs: insurance pack; microclimate pack; crop pack; potential decision-rule conflicts.
Freshness: governance decisions depend on as-of state at incident time, not “now”.
Outputs: DossierAssembly (insurance).
Hardness: multi-temporal modelling + high-consequence outputs with required basis snapshots.

**Scenario: Harvest at high moisture → safe storage period countdown**
Operational context: corn comes off wet; may be held “a bit” in a truck, floor pile, or bin before drying; safe storage time decreases rapidly with higher moisture and temperature.
Actors: farmer; drying service; buyer.
Objects: CropCycle harvest action, Lot creation, Facility/StorageLocation, drying intervention, moisture evidence.
Event families: InterventionEvent (harvest/drying), MaterialEvent (lot creation/movement), ObservationEvent (moisture tests).
Commit classes: operation claim; evidence record; observation assertion.
Packs: post-harvest handling pack; buyer contract pack (moisture specs and discounts).
Freshness: material state (moisture/temp) is perishable; stale state is dangerous for operational decisions.
Outputs: Lot PassportView; buyer delivery report.
Hardness: OFARM must model “time-sensitive material condition” without collapsing it into a single static attribute.

**Scenario: Drying damage and overdrying vs safe storage constraints**
Operational context: overdrying causes cracking/darkening/seed damage; underdrying raises mould/insect risk; dryer logs may be incomplete.
Actors: farmer; dryer operator; buyer.
Objects: Lot, Facility, drying equipment, quality tests.
Event families: InterventionEvent (drying), ObservationEvent (quality/moisture), EvidenceEvent (dryer logs).
Commit classes: operation claim; evidence records; observation assertions.
Packs: quality grading pack; safety pack; potential evidence-policy strengthening for attested outputs.
Freshness: drying parameters are needed “as-of drying time”, not later edited guesses.
Outputs: lot quality report; dispute dossier if rejected.
Hardness: requires rigorous evidence/provenance handling and correction without deleting history.

**Scenario: Bin sanitation failure → insects migrate from old residues into new grain**
Operational context: guidance repeatedly warns that leftover grain/dust can seed infestations; “do not put new grain on top of old grain” is a common rule-of-thumb; clean bins and equipment weeks before harvest.
Actors: farmer; workers; pest-control provider.
Objects: Facility/StorageLocation, Lot, evidence of cleaning actions, monitoring observations.
Event families: InterventionEvent (cleaning/treatment), ObservationEvent (monitoring), OccurrenceEvent (infestation).
Commit classes: operation claim; observation assertion; evidence record.
Packs: organic pack may limit chemical options; pest-control pack adds rules; safety pack.
Freshness: repeated monitoring updates; state becomes stale quickly if not recalculated.
Outputs: storage management report; organic inspection dossier if relevant.
Hardness: long-running maintenance campaign across multiple lots and containers—high query complexity and evidence volume.

**Scenario: Aeration and temperature stratification creates hidden spoilage pockets**
Operational context: aeration is used to cool grain; cool temperatures reduce insect/mould activity; without proper aeration, temperature differentials build.
Actors: farmer; storage manager.
Objects: Facility, Lot, aeration equipment, temperature cables.
Event families: InterventionEvent (aeration run), ObservationEvent (temperature readings), OccurrenceEvent (heating/mould).
Commit classes: observation assertions; operation claims; evidence records.
Packs: storage management pack; equipment telemetry pack.
Freshness: operational decisions rely on current readings; stale materialisation should be marked and policy-limited.
Outputs: Facility PassportView and Lot PassportView.
Hardness: high-frequency observations, potentially offline, requiring robust sync and materialisation policies.

**Scenario: Lot creation from harvest stream → split into bins → partial merge later**
Operational context: one field harvested over days; grain placed into multiple bins; later blended for shipment; quality varies by load.
Actors: farmer; buyer; sometimes elevator.
Objects: Lot identities, StorageLocations, Container occupancy episodes, lineage relations.
Event families: MaterialEvent (create/split/merge), InterventionEvent (harvest/handling), ObservationEvent (grading/moisture).
Commit classes: operation claim; observation assertion; evidence record.
Packs: traceability pack; buyer contract pack; potential view shaping for buyer vs internal.
Freshness: “what is in this bin now” is a governed current-state question—materialisation critical.
Outputs: Lot PassportView; ReportAssembly for shipment lot composition.
Hardness: OFARM Lot lifecycle rules + container/occupancy semantics must be honoured, or traceability collapses.

**Scenario: Grain delivery grading dispute (moisture/dockage/grade) with re-examination**
Operational context: moisture meters differ; dockage and grade factors affect price; disputes can trigger formal re-check and written determinations.
Actors: farmer; elevator; inspector/regulator.
Objects: Lot, delivery tickets, official weigh/grade results, dispute case file.
Event families: MaterialEvent (delivery), ObservationEvent (grade determination), GovernanceEvent (appeal/reinspection), EvidenceEvent (tickets/certificates).
Commit classes: evidence record; governance decision; observation assertion.
Packs: buyer contract pack; grain standards pack; dossier templates.
Freshness: dispute is about “as delivered” state; later storage changes must not rewrite it.
Outputs: DossierAssembly (dispute); buyer-facing report.
Hardness: multi-party authority + immutable outputs + strong trace-back to basis.

**Scenario: Mycotoxin risk management across harvest/storage with buyer testing and rejection**
Operational context: mycotoxins can arise pre- and post-harvest; post-harvest handling/drying/storage is critical; some buyers test for DON/aflatoxin and reject sublots over thresholds.
Actors: farmer; buyer; lab; possibly regulator.
Objects: Lot, lab certificates, storage records, diversion decision (feed vs food).
Event families: ObservationEvent (testing), EvidenceEvent (lab report), GovernanceEvent (accept/reject), MaterialEvent (diversion/disposal).
Commit classes: observation assertions; evidence record; governance decision.
Packs: food-safety pack; buyer-spec pack; evidence-policy strengthening.
Freshness: test results are per-sublot/time; later merges must preserve which sublot was tested.
Outputs: DossierAssembly (food safety); compliance submission if required.
Hardness: forces sublot semantics and identity discipline; easy place for weak implementations to “average away” danger.

**Scenario: Organic + conventional share equipment and storage (commingling prevention plan under stress)**
Operational context: same auger/truck/bin used; cleaning is imperfect; paperwork exists but execution is messy.
Actors: farmer; organic certifier/inspector; buyer.
Objects: Facility, Container, Lot, cleaning interventions, commingling risk evidence, organic system plan records.
Event families: InterventionEvent (cleanout), MaterialEvent (lot movement), GovernanceEvent (inspection/nonconformity), EvidenceEvent (records).
Commit classes: operation claim; evidence record; compliance assertion; governance decision.
Packs: organic certification pack imposes segregation controls; local method pack may conflict with evidence requirements.
Freshness: after a commingling incident, prior “organic lot state” may become INVALID for compliance use.
Outputs: Inspection dossier; corrected lot passport; possibly nonconformity + corrective action.
Hardness: simultaneously tests lots, facilities/containers, evidence sufficiency, and output taxonomy.

**Scenario: Temporary storage outside “normal facilities” (piles, bags, drums) under weather risk**
Operational context: bumper harvest or bin shortage; temporary storage used; moisture ingress and contamination risk increase; practices vary by region.
Actors: farmer; workers; buyer.
Objects: StorageLocation, Container, Lot, evidence of conditions.
Event families: MaterialEvent (move to temporary storage), OccurrenceEvent (rain ingress), ObservationEvent (moisture/condition).
Commit classes: observation assertion; evidence record; operation claim.
Packs: post-harvest pack; organic pack may restrict allowable surfaces/containers.
Freshness: condition changes quickly; late observations can invalidate earlier “safe” state.
Outputs: Facility/Lot passports; buyer report.
Hardness: stresses container identity vs occupant identity and “current-state is derivative and explainable” requirement.

**Scenario: Contractor executes operation but provides late/partial records**
Operational context: custom applicator plants/sprays/harvests; farmer receives an invoice, maybe an ISOXML file later; details missing (rate, product ID, time).
Actors: contractor; farmer; advisor; auditor.
Objects: OperationClaims, EvidenceRecords, DelegationGrant (if contractor is allowed to report).
Event families: InterventionEvent, EvidenceEvent, GovernanceEvent (if audited).
Commit classes: operation claim; evidence record; governance decision if contested.
Packs: integration pack for task data; compliance pack requiring record completeness; pack merge risk on evidence-policy rules.
Freshness: revocation or changed delegation can occur before contractor “finalises” reported execution.
Outputs: Field passport; compliance dossier.
Hardness: this is the archetypal stress test for executable authority with delegation and revocation re-check at promotion time.

**Scenario: Owner vs operator vs tenant disagreement over who can approve compliance submissions**
Operational context: land is owned by Party A, farmed by Party B, compliance obligations shared; approvals and signatures are disputed.
Actors: owner; tenant/operator; advisor; certifier.
Objects: AuthorityGrants, RoleAssignments, RevocationDecisions, SubmissionAssembly drafts.
Event families: GovernanceEvent (approval/attestation), StructureEvent (role assignment change).
Commit classes: governance decision; compliance assertion; evidence record.
Packs: certification pack defines who must attest; governance pack defines action-class requirements.
Freshness: long-running “draft submission” crosses revocation boundary; must re-evaluate authority at final promotion.
Outputs: SubmissionAssembly with attestation trace.
Hardness: directly exercises AuthorityActionClass, default-deny, human-only attestation defaults, and decision traces.

**Scenario: Advisor-prepared filing that requires human approval and traceable AI assistance**
Operational context: advisor (or AI tool) drafts nutrient plan, spray log, or organic system update; farmer must approve; AI may be used for assembly.
Actors: advisor; farmer; software agent.
Objects: draft assertions, AuthorizationDecisionTrace, AI-assisted action markers, DocumentAssembly drafts.
Event families: GovernanceEvent (approve/attest), EvidenceEvent (assembly).
Commit classes: compliance assertion; governance decision; evidence record.
Packs: authority pack with AI rules; evidence policy may require human approval for final submission.
Freshness: if underlying current-state materialisation is stale, final assembly must block.
Outputs: SubmissionAssembly.
Hardness: stresses REQUIRE_HUMAN_APPROVAL outcome and “assistance is not authority borrowing”.

**Scenario: Buyer requests read-only access to a lot, then disputes identity and demands deeper history**
Operational context: buyer contract needs traceability; buyer wants lot passport; later disputes attributes (e.g., “same lot?”) and requests more evidence.
Actors: farmer; buyer; possibly auditor.
Objects: SharingGrants, Lot passport view, evidence bundles, lineage relations.
Event families: GovernanceEvent (sharing grant), MaterialEvent (lot lineage), EvidenceEvent (bundle).
Commit classes: evidence record; governance decision.
Packs: buyer “profile” for the Lot PassportView; data sovereignty boundary must prevent silent over-sharing.
Freshness: buyer requests “current lot state”; must be generated from a clear context snapshot and basis.
Outputs: Lot PassportView; possibly a ReportAssembly for contractual delivery.
Hardness: stresses output taxonomy (passport vs report), scoped sharing, and query reproducibility under different recipient profiles.

**Scenario: Certifier inspection finds missing evidence, issues nonconformity, and requires corrective action**
Operational context: inspection asks for spray logs, cleaning records, invoices; gaps exist; corrective actions required.
Actors: farmer; certifier/inspector.
Objects: InspectionCase, NonConformity, CorrectiveAction, evidence bundle.
Event families: GovernanceEvent (inspection/NC), EvidenceEvent (late uploads).
Commit classes: compliance assertion; governance decision; evidence record.
Packs: certification pack; evidence policy pack; document assembly shaping for dossier.
Freshness: dossier assembled from stale state is unacceptable; must snapshot basis.
Outputs: DossierAssembly; later SubmissionAssembly for corrective-action completion.
Hardness: stresses evidence sufficiency gating + supersession after a dossier already circulated.

**Scenario: Pack conflict—two same-precedence packs touch evidence policy or decision rules for the same operation**
Operational context: certification pack and local/community pack both define evidence sufficiency or decision rules; overlap is not declared safely mergeable.
Actors: farm governance steward.
Objects: PackActivationSet, PackMergeResolutionTrace, evidence policy modules, decision-rule modules.
Event families: StructureEvent (pack activation), GovernanceEvent (compatibility decision).
Commit classes: governance decision; structure assertion.
Packs: surface family = EVIDENCE_POLICY or DECISION_RULE; safe merge modes differ and may HARD_FAIL without declared legality.
Freshness: pack activation changes context snapshot and can invalidate current-state materialisations.
Outputs: Pack conflict report; governance dossier.
Hardness: deterministic failure behaviour is required; “prompt the user” is explicitly discouraged.

**Scenario: Late evidence after a formal submission was assembled**
Operational context: submission filed; later missing lab report / ticket appears; must supersede or append without invalidating audit trail.
Actors: farmer; advisor; authority/agency.
Objects: EvidenceRecord late arrival; SubmissionAssembly; ReviewDecision supersession; MaterializationSnapshot of what was relied upon.
Event families: EvidenceEvent (late receipt), GovernanceEvent (supersede), possibly StructureEvent if scope identity revisions involved.
Commit classes: evidence record; governance decision.
Packs: submission shaping + evidence policy; stricter retention for attested outputs.
Freshness: correction should not rewrite prior “generated-at” basis; new submission version required.
Outputs: new SubmissionAssembly version; trace to prior.
Hardness: large stressor for supersession law, basis snapshots, and externally-visible corrections.

## Top stress-test scenarios

These are the scenarios most likely to break a weak implementation because they combine **bulk-material reality**, **multi-party authority**, and **time-sensitive governance**.

1) **Partial replant inside one field** → must create explicit crop-cycle overlap/split lineage, not overwrite the existing cycle.
2) **Crop switch after failure with insurance/subsidy linkage** → multi-temporal “as-of incident time” state + governance decision objects.
3) **Harvest wet grain held temporarily before drying** → safe-storage countdown + evidence of moisture/temperature at each step.
4) **Bin not cleaned; infestation sourced from residues** → explicit sanitation interventions + monitoring loop; avoid “new lot because insects”.
5) **Lot split/merge across bins and shipments** → strict lot lineage; container identity across occupancy episodes; queryable “what is in bin X now”.
6) **Organic + conventional using shared equipment/storage** → commingling prevention evidence; nonconformity/corrective action workflows.
7) **PPP records incomplete, then “repaired” later** → must preserve record time vs effective time; prevent silent auto-promotion into compliance fact.
8) **EU/UK nutrient (NVZ) rules: closed periods + required records** → time-window triggers that invalidate planned actions and filings.
9) **Contractor provides ISOXML/EFDI after the fact; some task data invalid** → ingestion normalisation + evidence quality downgrade path.
10) **Advisor drafts submission; farmer’s authority revoked mid-draft** → re-evaluate authorisation at final promotion; require human approval.
11) **Pack activation conflict on evidence policy/decision rule** → must hard fail activation deterministically unless declared safe merge exists.
12) **Stale current-state used for high-consequence submission assembly** → must recompute or refuse; snapshot relied-upon basis.
13) **Grain grading/moisture dispute for delivered lot** → “as delivered” evidence and governance-case packaging.
14) **Mycotoxin test failure in a sublot** → sublot identity discipline; avoid illegal/meaningless merges; evidence retention.
15) **Remote-sensing vs on-foot scout contradiction** → allow competing hypotheses; prevent fake certainty in Compliance Twin.
16) **Organic neighbour drift allegation** → disputed occurrence + lab evidence + authority and sharing boundaries across farms.
17) **Field geometry revision after operations recorded** → identity revision triggers invalidation of some materialisations and some mappings.
18) **Late evidence after submission already sent** → supersession with immutable history, not “edit-in-place”.
19) **Buyer wants read-only passport, then presses for full history** → enforce SharingGrant scope; output taxonomy discipline; trace-back.
20) **Mixed grain moisture reporting basis across markets** → requires explicit “measurement method and basis” modelling, or cross-border comparisons get misleading.

## Scenario clusters by OFARM risk

**Identity and lifecycle risk**
Highest-risk cluster: *Field revisions under subsidy controls; CropCycle replant/crop switch/overlap; Lot split/merge/commingling; reusable Container occupancy.* These scenarios fail when implementations do “CRUD thinking” and collapse *state change* into *new identity* or silently overwrite instead of creating lineage relations. OFARM explicitly requires durable identity vs identity revision vs time-bounded state to remain distinct, and singles out “lot” as the red-flag object.

**Current-state freshness risk**
Highest-risk cluster: *wet grain condition; compliance filings; pack activation changes; late-arriving evidence; long-running offline capture.* The failure pattern is “stale but looks recent”: using cached state for a high-consequence action (submission, attestation, compliance decision) without recomputation or a provable FRESH status. RC2.1 demands FRESH/STALE/INVALID states and invalidation triggers, and requires recompute/refuse for high-consequence uses.

**Pack merge risk**
Highest-risk cluster: *certification packs + local packs + method packs overlapping on evidence policy, decision rules, templates, or view/document shaping.* The dominant failure mode is non-deterministic compatibility (“it worked on one farm install, broke on another”). OFARM’s surface-family merge model restricts legal merge modes (for example: evidence policy often STRONGEST_REQUIREMENT; decision rules require ORDERED_COMPOSITION or hard fail). Implementations that “best-effort merge” violate the architecture.

**Authority risk**
Highest-risk cluster: *contractor reporting; advisor-assisted submissions; owner vs tenant approval; buyer read-only; certifier review powers; revocations mid-flow.* The platform must decide “who may do what at which scope/time” against explicit action classes with default-deny, delegation constraints, and revocation re-check on long-running flows. Weak implementations tend to treat “has access” ≈ “may act” and collapse delegation + sharing into one.

**Evidence risk**
Highest-risk cluster: *PPP logs; grain tickets; lab certificates; machine task data; cleaning logs; photos; emails.* Real farms have “evidence that exists but is low quality” and “evidence that arrives late”; OFARM’s commit/promotion matrix exists explicitly to prevent weak inputs from silently becoming hard truth, and requires structured handling of evidence records as support rather than truth by itself.

**Output taxonomy risk**
Highest-risk cluster: *inspections, nonconformities, insurance disputes, subsidy filings.* The failure mode is output “bucket collapse” (everything becomes a “passport”), which destroys governance meaning and audit usability. OFARM draws a hard line: PassportViews are live summaries; DocumentAssemblies are frozen outputs, with dossiers and submissions as distinct subtypes.

**Query and retrieval risk**
Highest-risk cluster: *“what was true as-of incident time”, “what rules applied under which pack set”, “what evidence supported this accepted consequence”, “what is in this bin now”.* These queries require deterministic alias resolution, versioned artefact context, and an explicit basis trace. OFARM standardises QuerySpecification/QueryPlanIR and emphasises equivalence across execution targets.

## What must be added to conformance fixtures

RC2.1 already lists a broad conformance baseline, but the scenario set above implies concrete fixture expansions that are *domain-realistic* rather than abstract.

Conformance fixtures that should be added (or strengthened) as scenario-driven tests:

- **Partial replant fixture**: one Field, one initial CropCycle, patch failure → partial replant; require explicit CropCycle overlap or split lineage; verify queries for “current crop in zone” do not silently pick the wrong one.
- **Wet-grain custody chain fixture**: harvest → temporary storage → drying → bin; track moisture observations and safe-storage timing; ensure material-state consequences are time-bounded and basis-traceable, and that stale state blocks “attest lot quality” outputs.
- **Lot split/merge/commingle fixture with sublot tests**: two lots in two bins → partial merge into shipment lot; one sublot fails mycotoxin test; ensure lineage preserves “tested sublot vs merged lot” semantics and prevents unsafe claim propagation.
- **Organic commingling prevention fixture**: one farm operates organic + conventional; shared equipment and facility; require recorded cleanout interventions and commingling-prevention controls; simulate inspection raising nonconformity and corrective action.
- **PPP record “upgrade” fixture**: initial spray recorded as weak note; later upgraded to operation claim with label photo and invoice; verify promotion rules prevent silent compliance-fact creation and preserve record/effective time separation.
- **NVZ time-window fixture**: planned manure application crosses closed-period boundary; ensure time-policy trigger marks materialisation stale/invalid and blocks compliance submission until recompute.
- **Contractor delegation fixture**: contractor allowed to OPERATE_REPORT_EXECUTION at field scope via DelegationGrant but denied ASSERT_COMPLIANCE and denied OUTPUT_ATTEST_DOCUMENT_ASSEMBLY; verify authorization traces for allow/deny.
- **Revocation on long-running flow fixture**: advisor drafts SubmissionAssembly; SharingGrant revoked or AuthorityGrant narrowed before final filing; verify final authorisation re-evaluation yields DENY or REQUIRE_HUMAN_APPROVAL.
- **Pack conflict hard-fail fixture (same precedence)**: two packs overlap on EVIDENCE_POLICY without declared safe merge; activation must HARD_FAIL with PackMergeResolutionTrace, not partial activation.
- **Submission supersession fixture**: assemble and “file” a SubmissionAssembly; then late evidence arrives; require a superseding submission version with preserved basis snapshot and audit trail.
- **Cross-market moisture/grade measurement fixture**: record moisture with method/basis metadata; ensure queries and outputs can render correct basis and avoid false equivalence across standards.

## What OFARM already handles well vs weakly

This section is grounded in the current RC2.1 baseline plus the post-gap-closure hostile review and readiness memo.

OFARM already appears strong where the real-world scenarios above most need architectural discipline:

- **Clear separation of truth substrate vs projections and “capture is not commitment” discipline** (reduces incentives to treat imported task files or UI forms as truth).
- **Event grammar + commit/promotion matrix** that explicitly blocks silent promotion from weak inputs (notes, hypotheses) into hard consequences (accepted executed consequences, compliance facts). This is exactly what messy evidence and late records require.
- **Identity/lifecycle semantics for the objects that farms actually fight about** (Field revisions, CropCycle replants/overlaps, Lot cohort continuity, Facility/Container separation). This matches the stress points in bulk grain reality.
- **Pack law with surface-specific merge semantics and deterministic failure posture**, which is necessary because real compliance contexts are “multi-pack by default” (law + certification + crop system + method + local).
- **Executable authority direction** via action classes, inheritance modes, delegation and revocation traces (crucial for contractors, advisors, certifiers, buyers).
- **Current-state materialisation with freshness states and invalidation triggers**, which directly targets the most common governance failure: using stale “current state” in a high-consequence action.
- **Output taxonomy boundary** between passports and dossiers/submissions, which aligns with how inspections, disputes, and filings actually behave.

Weaknesses that remain (and matter specifically for the farming scenarios in this report):

- **Lot remains the main divergence risk in practice**, even with improved semantics. Bulk supply chains force hard choices about when “handling” becomes a new traceability cohort; weak implementations will either over-split (identity explosion) or over-merge (traceability fiction). This is explicitly called out as remaining risk.
- **Trace-object formal schemas are still debt** (notably PackMergeResolutionTrace and AuthorizationDecisionTrace). Real audits and disputes will demand those traces to be machine-consumable, not just conceptual.
- **Conformance depth is still a seed, not a stress-tested suite.** The hostile review and readiness memo both frame the remaining work as “implementation-scale + deeper conformance expansion”, which strongly matches the scenario-driven fixture program demanded here.
- **Template merge validator maturity remains sensitive**, and real multi-pack deployments will run into contradictory constraints (especially in compliance documentation templates). If template merge fails non-deterministically, the system becomes non-auditable.

## Prioritised next actions

1) **Build a governed “Scenario Fixture Library” as a first-class artefact set, not a spreadsheet.** Each scenario in the “Top stress-test” list should become: (a) a minimal canonical dataset of events/assertions/evidence, (b) an expected current-state materialisation outcome for Compliance vs Advisory twins, and (c) expected PassportViews / DocumentAssemblies. This directly aligns with RC2.1’s conformance direction and the readiness memo’s “deeper conformance expansion” mandate.

2) **Make “Lot campaign” fixtures the centrepiece of early correctness work.** Start with 4–6 canonical grain post-harvest campaigns (wet harvest → drying → bin → merge → delivery → dispute). Use authoritative post-harvest sources to anchor realism (moisture thresholds, safe storage time, sanitation and aeration practices) so fixtures represent real operational constraints.

3) **Hard-code “high-consequence use” refusal tests early, and treat them as non-negotiable regression gates.** Every flow that produces an attested output, a submission, or an accepted consequence must prove it relied on FRESH materialisation or recomputed; otherwise fail or route to explicit review.

4) **Prioritise scenario packs that are *guaranteed* to co-activate in the real world: jurisdiction/nutrient + organic + crop-system + equipment task-data + buyer contract.** Then deliberately engineer overlaps on EVIDENCE_POLICY, DECISION_RULE, and DOCUMENT_ASSEMBLY_SHAPING to force PackMergeResolutionTrace maturity and deterministic activation failures.

5) **Treat contractor/advisor/buyer/certifier as first-class parties from day one, with explicit grants and revocation drills.** Build fixtures where drafting spans revocation boundaries, contractors can report execution but cannot assert compliance, and certifiers can review/contest but not operate. Require AuthorizationDecisionTrace outputs for every allow/deny.

6) **Implement “evidence quality downgrades” as a formal thing, not an informal note.** Many real records are incomplete (handwritten spray books, partial task files, photos without metadata). OFARM should support: (a) low-quality evidence that still exists, (b) later upgrades with better evidence, and (c) explicit constraints on what can be promoted from that basis.

7) **Define a minimal “bulk grading & dispute” dossier template family and bind it to real grading mechanics.** Use Canadian and US official grading/weighting references to build dossier expectations (tickets, official determinations, appeal steps). This will immediately surface OFARM’s requirements for “as delivered” state, evidence, and governance events.
