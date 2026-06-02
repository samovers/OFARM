# OFARM agronomic scenario coverage matrix v0.1

Date: 2026-05-12  
Status: active supporting implementation artifact  
Scope: agronomic scenario coverage matrix derived from the Senior Agronomist Reviewer findings, updated after Phase 2 observation/measurement context closure  
Audience: implementers, conformance authors, reviewers, and AI agents

---

## 1. Purpose

This matrix makes real agronomic failure modes visible before new baseline law or new machine contracts are written.

It answers:
- which agronomic scenarios the current package can already express
- where the current package is only partially sufficient
- which future narrow carrier or fixture should close the gap

This matrix is conformance planning. It does not override active law.

---

## 2. Status key

- **COVERED** — active package has executable evidence and enough payload semantics for the scenario.
- **PARTIAL** — active package has governance/truth mechanics but lacks some agronomic payload or scenario-specific fixture depth.
- **PARTIAL_WITH_CARRIER** — active package now has a relevant carrier shell, but the end-to-end scenario is not yet fully executable.
- **NOT_STARTED** — no meaningful package-local evidence yet.

---

## 3. Scenario coverage matrix

| Scenario | Main agronomic risk | Current OFARM fit | Current evidence | Missing or weak element | Next closure task |
|---|---|---|---|---|---|
| AGR-SCEN-001 — observation to decision | scouting or measurement drives a treatment decision without enough crop-stage, method, threshold, or uncertainty context | PARTIAL_WITH_CARRIER | `OFARM_AgronomicObservationContext_schema_v0_1.json`, `OFARM_MeasurementEvidence_schema_v0_1.json`, `OFARM_EvidenceSufficiencyCase_schema_v0_2.json`, `OFARM_Agronomic_Observation_and_Measurement_Context_RFC_v0_1.md` | end-to-end recommendation/prescription/execution and query reconstruction still pending | IMP-303 closed; IMP-305, IMP-309 pending |
| AGR-SCEN-002 — recommendation to prescription to execution | recommendation, prescription, plan, operation claim, and accepted execution collapse into one record | PARTIAL | `OFARM_Event_Grammar_and_Commit_Matrix_v0_1.md`, `OFARM_PlannedIntervention_schema_v0_1.json`, `OFARM_AcceptedEventConsequence_schema_v0_1.json` | quantity/rate/product/target/actual-extent payload across stages | IMP-305, IMP-304 |
| AGR-SCEN-003 — offline contractor late sync | contractor reports late; delegation, revocation, incomplete machine data, and manual corrections interact | PARTIAL | `OFARM_Event_Ingress_and_Promotion_Boundary_Closure_RFC_v0_1.md`, authorization examples, delayed-sync examples, `IMP-201` | agronomic treatment payload and partial extent detail | IMP-304, IMP-305, IMP-306 |
| AGR-SCEN-004 — partial failed application and correction | failed pass or partial application is incorrectly treated as whole-field accepted truth | PARTIAL | `OFARM_EvidenceSufficiencyCase_example_partial_machine_log_manual_top_up_v0_2.json`, event/promotion law | explicit actual extent and geometry-basis descriptor | IMP-304, IMP-306 |
| AGR-SCEN-005 — partial replant with different variety | one field contains overlapping crop attempts, seed lots, varieties, and lineage | PARTIAL | `OFARM_Identity_and_Lifecycle_RFC_v0_1.md`, `OFARM_IdentityLifecycleChange_schema_v0_1.json`, replant example | partial extent, mixed cycle/variety output disclosure, query reconstruction fixture | IMP-304, IMP-306, IMP-309 |
| AGR-SCEN-006 — measurement-context dispute | soil, moisture, pest, or disease measurement appears precise but method/calibration/sampling is weak | PARTIAL_WITH_CARRIER | `OFARM_MeasurementEvidence_schema_v0_1.json`, `OFARM_AgronomicObservationContext_schema_v0_1.json`, measurement-context sufficiency examples | policy-specific measurement insufficiency vocabulary and full query/output reconstruction still pending | IMP-303 closed; IMP-309 pending |
| AGR-SCEN-007 — ambiguous product or input identity | local product name, invoice, label, and machine log disagree | PARTIAL_WITH_CARRIER | `OFARM_AgronomicIdentityBinding_schema_v0_1.json`, `OFARM_AgronomicCodeBindingProfile_schema_v0_1.json`, unresolved marketing-name-only and resolved PPP identity examples | end-to-end query/output reconstruction and product-identity disclosure still pending | IMP-307 closed; IMP-309 pending |
| AGR-SCEN-008 — wet grain held before drying | lot/material state changes with moisture, temperature, temporary storage, and later drying | PARTIAL_WITH_CARRIER | lot/material/event architecture, `OFARM_MeasurementEvidence_schema_v0_1.json`, supporting staple-crop stress research | storage-specific observation examples and lot/state query fixture | IMP-303 closed; IMP-309 pending |
| AGR-SCEN-009 — field geometry revision after operations | old operations are tied to old geometry; new geometry affects filing/output truth | PARTIAL | `OFARM_Current_State_Materialization_RFC_v0_1.md`, identity/lifecycle fixtures, materialization freshness fixtures | scope/extent basis, stale-output disclosure, geometry-sensitive query fixture | IMP-306, IMP-309 |
| AGR-SCEN-010 — schema, example, glossary, and query drift | agronomic concept names drift across docs, schemas, examples, aliases, and packs | PARTIAL_WITH_CARRIER | alignment-register coverage, alias governance fixtures, `AgronomicCodeBindingProfile`, and `AgronomicIdentityBinding` examples | agronomic alias/query fixture suite still pending | IMP-307 closed; IMP-309 pending |

---

## 4. Phase 1 minimum pass condition

Phase 1 is considered started, not complete, when the package contains:
- this matrix
- fixture narratives
- machine-readable scenario records
- a runner that checks every scenario has expected promotion, materialization, output, and negative-test behavior
- results that honestly classify current state as `PASS_WITH_LIMITATIONS`, not full agronomic closure

---

## 5. Interpretation

The matrix shows that OFARM already has strong truth, authority, evidence, event, and materialization mechanics.

The remaining agronomic risk is not broad architecture. It is missing executable payload and scenario depth for:
- observation and measurement context
- product/rate/quantity/as-applied detail
- partial spatial extent
- code-binding and standards profiles
- query/output reconstruction


---

## 6. Phase 2 update — observation and measurement carriers

Phase 2 added active carrier shells and examples for observation and measurement context:

- `02_accepted_rfcs/OFARM_Agronomic_Observation_and_Measurement_Context_RFC_v0_1.md`
- `03_machine_contracts/schemas/agronomic/OFARM_AgronomicObservationContext_schema_v0_1.json`
- `03_machine_contracts/schemas/evidence/OFARM_MeasurementEvidence_schema_v0_1.json`
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_Agronomic_Observation_Measurement_Context_Fixtures_v0_1.md`
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_agronomic_observation_measurement_context_results_v0_1.json`

This upgrades `AGR-SCEN-001`, `AGR-SCEN-006`, and part of `AGR-SCEN-008` from plain `PARTIAL` to `PARTIAL_WITH_CARRIER`.

The overall scenario suite remains `PASS_WITH_LIMITATIONS` because intervention/as-applied payload, partial extent, agronomic code-binding profile, and query/output reconstruction are still unresolved future closures.


---

## Phase AGR-P4 coverage update — 2026-05-13

Phase AGR-P4 closes the partial extent / geometry-basis carrier gap at RFC and machine-contract level.

| Scenario pressure | Previous gap | Phase AGR-P4 artifact | Updated status |
|---|---|---|---|
| Partial failed application and correction | partial actual extent and failed-pass geometry basis were only thin payload fields | `OFARM_PartialExtent_schema_v0_1.json`; failed-pass and accepted-treated-slice examples | carrier closed; deeper query/output reconstruction still pending |
| Partial replant with mixed variety/crop-cycle state | partial replant area could be cited but not carried with geometry basis/quality | replant PartialExtent plus identity-lifecycle and materialization-refusal bridge examples | carrier closed; PassportView/DocumentAssembly disclosure fixtures still pending |
| Disputed geometry | disputed operator/machine extents could be retained as records but not typed as parallel geometry | disputed PartialExtent example | carrier closed; output/reconstruction policy still pending |


---

## Phase AGR-P5 coverage update — 2026-05-13

Phase AGR-P5 closes the code-binding and standards-profile carrier gap at RFC and machine-contract level.

| Scenario pressure | Previous gap | Phase AGR-P5 artifact | Updated status |
|---|---|---|---|
| Ambiguous product or input identity | product/input identity depended on inline examples and reference snapshots only | `AgronomicIdentityBinding`, `AgronomicCodeBindingProfile`, resolved PPP product and unresolved marketing-name-only examples | carrier/profile closed; query/output disclosure still pending |
| Crop/stage/target identity drift | code roles were named but not governed by a profile | crop species, BBCH crop-stage, and EPPO weed/target examples | carrier/profile closed; alias/query fixture still pending |
| Quantity kind and unit drift | existing payloads carried QUDT/UCUM-like refs but profile invariants were not explicit | profile invariants require quantity kind and unit code | carrier/profile closed; reconstruction fixtures still pending |
| Threshold orphaning | threshold references could be carried without a dedicated binding shell | threshold-source binding with issuer, role, effective period, and quantity | carrier/profile closed; output policy still pending |

## Phase AGR-P5 scenario coverage update — 2026-05-13

| Scenario | Prior code-binding gap | Phase AGR-P5 result | Remaining gap |
|---|---|---|---|
| AGR-SCEN-007 ambiguous product or input identity | No executable agronomic code-binding/profile carrier | `AgronomicIdentityBinding` and `AgronomicCodeBindingProfile` now block marketing-only product identity from compliance-grade use | Query/output reconstruction still pending |
| AGR-SCEN-010 semantic drift across artifacts | No executable profile governing scheme roles and pack merge behavior | Profile-level role map and fail-closed pack merge behavior now exist | Query alias/output reconstruction still pending |

Scenario records may now use `PARTIAL_WITH_CARRIER` where Phase AGR-P5 carriers exist but reconstruction remains incomplete.


## Phase AGR-P6 and AGR-P7 coverage update — 2026-05-13

AGR-P6 closes query/output reconstruction at RFC, machine-contract, and fixture level. AGR-P7 then harmonises the active baseline around the accepted carrier-shell law.

| Scenario pressure | Earlier remaining gap | AGR-P6/AGR-P7 result | Remaining limitation |
|---|---|---|---|
| Observation-to-decision reconstruction | structured carriers existed but output/query policy was pending | reconstruction policy/trace and baseline law now cover observation, threshold, evidence, and advisory/compliance separation | real pilot event chains still need live data |
| Prescription-to-execution audit | intent/execution carriers existed but query/output reconstruction was pending | treatment history, prescribed-vs-applied, and accepted-only output behavior are fixture-covered | wire-level machinery exchange mappings remain implementation-specific |
| Partial failed application and correction | PartialExtent existed but PassportView/DocumentAssembly behavior was pending | mixed/disputed/extents can now reconstruct into PassportView or DocumentAssembly under policy | production geometry quality policies remain profile-specific |
| Ambiguous product/input identity | code-binding carriers existed but disclosure/refusal behavior was pending | unresolved identity fails high-consequence output; DocumentAssembly can annex unresolved evidence under policy | live registry verification remains outside this phase |
| Schema/example/glossary/query drift | aliases and profiles were pending | agronomic alias/query/output examples plus baseline glossary/alignment rows reduce drift risk | future pack changes still require regression checks |

The AGR-P1 scenario runner remains `PASS_WITH_LIMITATIONS` because it is an expectation-level scenario harness, not a full runtime event/assertion/evidence-chain executor. AGR-P2 through AGR-P7 provide the carrier, reconstruction, and baseline closure evidence behind those expectations.


## Phase AGR-P8 runtime-chain coverage update — 2026-05-13

AGR-P8 closes the AGR-P1 scenario-suite limitation at package-local conformance level.

| Scenario pressure | Earlier remaining gap | AGR-P8 result | Remaining limitation |
|---|---|---|---|
| AGR-SCEN-001 observation to decision | expectation-level only after carrier closures | covered by runtime chains using observation, measurement, threshold, evidence, recommendation, and output gates | live pilot evidence remains future work |
| AGR-SCEN-002 recommendation to prescription to execution | needed end-to-end chain assembly | covered by chain separating recommendation, prescription, plan, claim, as-applied evidence, and accepted consequence | wire-level machine exchange mapping remains future work |
| AGR-SCEN-003 offline contractor late sync | needed concrete late-claim and identity-refusal chain | covered by late contractor and unresolved-product chain | live delegation/revocation telemetry remains future work |
| AGR-SCEN-004 partial failed application and correction | needed concrete partial/correction/dispute chain | covered by failed-pass, accepted-slice, correction, and dispute chains | production geometry-quality policy remains profile-specific |
| AGR-SCEN-005 partial replant mixed variety | needed mixed lineage/output chain | covered by PartialExtent, seed/variety bindings, IdentityLifecycleChange, materialization refusal, and mixed PassportView trace | crop/jurisdiction profile depth remains future work |
| AGR-SCEN-006 measurement-context dispute | needed qualified result and refusal chain | covered by pending lab, below-LOQ, calibration/method review, and output qualification behavior | live lab/accreditation verification remains future work |
| AGR-SCEN-007 ambiguous product/input identity | needed end-to-end identity refusal path | covered by unresolved marketing-name binding, evidence sufficiency, and accepted-only output policy | live registry lookup remains future work |
| AGR-SCEN-008 wet grain/storage condition | needed storage-condition measurement/output pressure | covered by measurement/materialization chain pattern for storage condition evidence | storage-specific profile examples can expand later |
| AGR-SCEN-009 field geometry revision after operations | needed geometry/materialization chain | covered by disputed geometry, partial replant, and stale materialization chains | production GIS exchange remains implementation-specific |
| AGR-SCEN-010 schema/example/glossary/query drift | needed alias/profile/query regression chain | covered by code-binding profile, alias catalog, QuerySpecification, QueryPlanIR, and reconstruction trace chain | future pack changes require regression checks |

The AGR-P1 scenario runner now reports `PASS` when AGR-P8 runtime-chain results are present. This is package-local conformance evidence, not live pilot readiness.


### AGR-P8 final record-state cleanup — 2026-05-13

The scenario record set now marks all `AGR-SCEN-*` entries as `EXECUTABLE_CHAIN_SUPPORTED` with `AGR-P8_RUNTIME_CHAIN_CLOSED` closure status. Earlier gaps are retained as `closedPackageGaps` so the original review pressure remains traceable without continuing to report active package gaps.

## AGR-P9 local-knowledge rationale lineage overlay

AGR-P9 adds an overlay fixture for the observation-to-decision and recommendation-to-execution scenarios. It proves that local farm knowledge can explain why a plan was created without making the local rule itself an accepted compliance fact.

Evidence:
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_Agronomic_Local_Knowledge_Rationale_Lineage_Fixtures_v0_1.md`
- `04_implementation_and_conformance/conformance_runners/agronomic_conformance/OFARM_agronomic_local_knowledge_rationale_lineage_results_v0_1.json`
