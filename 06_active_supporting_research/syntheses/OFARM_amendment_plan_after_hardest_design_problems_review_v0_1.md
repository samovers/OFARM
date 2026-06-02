# OFARM amendment plan after hardest design problems review v0.1

Date: 2026-04-11  
Status: active supporting research / controlled amendment plan  
Scope: translate the hardest-design-problems research review into the smallest justified OFARM amendment program without reopening the settled RC2.1 architecture

---

## 1. Purpose

This document turns the review of `OFARM_research_hardest_design_problems_v0_1.md` into a concrete amendment plan for the active OFARM 2 package.

This document does **not** amend OFARM by itself.
It is a planning artifact that proposes the next controlled patch wave.

The intended use is:
- follow-on RFC authoring
- machine-contract expansion
- conformance-program expansion
- later narrow harmonization of RC2.1 where needed

---

## 2. Authority posture

This plan follows the active authority order of the migration package:
1. `00_active_baseline/`
2. `02_accepted_rfcs/`
3. `01_companion_artifacts/`
4. `03_machine_contracts/`

It treats:
- `06_active_supporting_research/syntheses/OFARM_research_hardest_design_problems_v0_1.md` as **supporting research**, not active law
- `04_implementation_and_conformance/` as evidence of what is and is not yet executable
- legacy material as out of scope unless a specific contradiction appears

The governing stance for this plan is:
- **do not rewrite OFARM from scratch**
- **do not treat the research report as replacement constitution**
- **close the remaining hard seams with the smallest controlled patch set**

---

## 3. Basis reviewed

This plan was prepared against the active OFARM 2 package, with emphasis on:
- `PROJECT_AUTHORITY.md`
- `ACTIVE_SUBSTANCE_README.md`
- `00_active_baseline/OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md`
- `00_active_baseline/OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md`
- `00_active_baseline/OFARM_Alignment_Register_v0_13.md`
- `00_active_baseline/OFARM_post_gap_closure_readiness_gate_memo_v0_1.md`
- `00_active_baseline/OFARM_final_hostile_review_after_gap_closure_v0_1.md`
- `01_companion_artifacts/OFARM_Query_Architecture_Note_v0_1.md`
- `01_companion_artifacts/OFARM_Compiled_Output_and_Passport_Taxonomy_Note_v0_1.md`
- `02_accepted_rfcs/OFARM_Identity_and_Lifecycle_RFC_v0_1.md`
- `02_accepted_rfcs/OFARM_Current_State_Materialization_RFC_v0_1.md`
- `02_accepted_rfcs/OFARM_Authority_Policy_Model_RFC_v0_1.md`
- `02_accepted_rfcs/OFARM_QuerySpecification_Schema_RFC_v0_1.md`
- `02_accepted_rfcs/OFARM_Capability_Manifest_RFC_v0_1.md`
- `02_accepted_rfcs/OFARM_Conformance_Claim_Set_and_Capability_Manifest_Reference_Extension_RFC_v0_1.md`
- `02_accepted_rfcs/OFARM_Interoperability_Mapping_Coverage_Loss_and_Runtime_Surface_RFC_v0_1.md`
- `02_accepted_rfcs/OFARM_Semantic_Substrate_Bundle_and_External_Profile_Packaging_RFC_v0_1.md`
- `04_implementation_and_conformance/historical_archive/historical_archive/historical/OFARM_conformance_coverage_matrix_v0_1.md`
- `06_active_supporting_research/syntheses/OFARM_research_hardest_design_problems_v0_1.md`

---

## 4. Main judgment

The research report is directionally strong.
It correctly identifies the hardest remaining OFARM problems as:
- lot lineage under split/merge/commingling/transformation
- explainable and governable current-state materialization
- deterministic pack/profile composition
- delegation/revocation/offline authority depth
- alias stability and query reproducibility
- evidence sufficiency for high-consequence outputs
- trustworthy offline and AI-assisted operation
- conformance tooling as part of the standard package

But the report should be used as a **priority map**, not as replacement law.
Several of its recommendations are already partly closed by the current package, especially:
- governed current-state materialization and freshness posture
- draft-only offline posture for edge work
- narrow machine-readable Capability Manifest posture
- separation of conformance claims, substrate bundles, mapping coverage/loss, and runtime surfaces

The remaining gap is therefore no longer “core architecture uncertainty”.
It is “missing executable closure and a few still-absent contracts”.

---

## 5. Disposition of the report’s ten recommendations

### 5.1 Promote into new OFARM artifacts now

Promote these as the next amendment wave:
- recommendation 1 — lot / traceability algebra
- recommendation 2 — chain-of-custody semantics under commingling
- recommendation 4 — effective context snapshot
- recommendation 5 — alias governance and regression safety
- recommendation 8 — evidence sufficiency as a compilable structure

### 5.2 Treat as already-correct baseline needing executable closure

Do not reopen the model semantics for these.
Instead deepen contracts and conformance around them:
- recommendation 3 — high-consequence materialization explainability
- recommendation 6 — authority / delegation / revocation / composition depth
- recommendation 7 — offline draft-only posture and sync-time revalidation
- recommendation 10 — conformance tooling as part of the standard package

### 5.3 Do not broaden now

Do not launch a broad redesign for recommendation 9.
Capability self-description has already been narrowed correctly and extended by reference.
The remaining work there is continued consistency testing, edge-case coverage, and eventual promotion of the draft extension path.

---

## 6. Controlled amendment program

### 6.1 Amendment A — lot traceability and claim-basis closure

**Change class:** RFC extension + machine contracts + conformance expansion

### Proposed new files
- `02_accepted_rfcs/OFARM_Lot_Traceability_and_Claim_Basis_RFC_v0_1.md`
- `03_machine_contracts/schemas/core/OFARM_LotLineageChange_schema_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/core/OFARM_LotLineageChange_example_split_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/pack_merge/OFARM_LotLineageChange_example_merge_commingle_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/core/OFARM_LotLineageChange_example_transform_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/identity_lifecycle/OFARM_LotLineageChange_example_shipment_reference_v0_1.json`
- `03_machine_contracts/schemas/core/OFARM_TraceabilityClaimBasis_schema_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/identity_lifecycle/OFARM_TraceabilityClaimBasis_example_identity_preserved_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/core/OFARM_TraceabilityClaimBasis_example_mass_balance_v0_1.json`

### Active files affected later
- `00_active_baseline/OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md`
- `00_active_baseline/OFARM_Alignment_Register_v0_13.md`
- `04_implementation_and_conformance/historical_archive/historical_archive/historical/OFARM_conformance_coverage_matrix_v0_1.md`

### Why this amendment is first
The active baseline already says lot identity is cohort-first and must break on split, merge/commingling, transformation, and strong claim-basis reset.
The gap is that OFARM still lacks a tighter executable algebra and a machine-readable claim-basis contract.
The conformance matrix still shows lot continuity and shipment continuity as only partially covered.

### Guardrails
- do **not** introduce a broad new constitutional `TraceObject` family yet
- keep the patch lot-first unless a real contradiction proves lot is insufficient
- do **not** allow “single lot ID survives everything” semantics to re-enter OFARM
- do **not** let weaker accounting models masquerade as physical lineage by default

### Acceptance criteria
This amendment wave is complete when OFARM can execute and validate:
- lot split
- lot merge / commingling
- lot transformation
- shipment continuity without false new-lot creation
- claim-basis reset with visible lineage consequences
- query-visible distinction between stronger and weaker chain-of-custody models

---

### 6.2 Amendment B — ContextSnapshot closure for materialization and pack activation

**Change class:** RFC extension + machine contract + runtime/conformance closure

### Proposed new files
- `02_accepted_rfcs/OFARM_ContextSnapshot_Closure_RFC_v0_1.md`
- `03_machine_contracts/schemas/current_state/OFARM_ContextSnapshot_schema_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/current_state/OFARM_ContextSnapshot_example_field_compliance_v0_1.json`
- `03_machine_contracts/OFARM_ContextSnapshot_example_partner_runtime_v0_1.json`

### Active files affected later
- `02_accepted_rfcs/OFARM_Current_State_Materialization_RFC_v0_1.md`
- `00_active_baseline/OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md`
- `00_active_baseline/OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md`
- `04_implementation_and_conformance/historical_archive/historical_archive/historical/OFARM_conformance_coverage_matrix_v0_1.md`

### Why this amendment is justified
The baseline and current-state RFC already require a context snapshot conceptually.
`MaterializationBasis` already points to `contextSnapshotRefs`.
The missing piece is the contract for what a ContextSnapshot actually contains and how it is produced from active packs, profiles, merge traces, and runtime context.

### Guardrails
- do **not** let ContextSnapshot become a hidden truth store
- do **not** duplicate assertion/history authority in the snapshot object
- keep it as a governed basis object that explains active context at a point in time
- preserve the current rule that pack activation and merge remain explicit, traceable, and deterministic

### Acceptance criteria
This amendment wave is complete when OFARM can produce a versioned ContextSnapshot that includes at minimum:
- active packs and profiles
- relevant merge traces and precedence outcomes
- governing evidence/validation policy references
- active semantic/profile assumptions where needed
- the references required for a reproducible MaterializationBasis

---

### 6.3 Amendment C — SemanticPathAlias governance and query reproducibility

**Change class:** RFC extension + machine contracts + query conformance suites

### Proposed new files
- `02_accepted_rfcs/OFARM_SemanticPathAlias_Governance_RFC_v0_1.md`
- `03_machine_contracts/schemas/query/OFARM_SemanticPathAliasCatalog_schema_v0_1.json`
- `03_machine_contracts/schemas/query/OFARM_SemanticPathAliasResolutionTrace_schema_v0_1.json`
- `03_machine_contracts/OFARM_SemanticPathAliasCatalog_example_core_v0_1.json`
- `03_machine_contracts/OFARM_SemanticPathAliasResolutionTrace_example_version_pinned_v0_1.json`

### Active files affected later
- `01_companion_artifacts/OFARM_Query_Architecture_Note_v0_1.md`
- `00_active_baseline/OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md`
- `00_active_baseline/OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md`
- `04_implementation_and_conformance/historical_archive/historical_archive/historical/OFARM_conformance_coverage_matrix_v0_1.md`

### Why this amendment is justified
The baseline already treats `SemanticPathAlias` as governed and versioned, and the schema already has alias-version hooks.
What is still missing is alias catalog law, resolution traces, and executable stability checks.
The conformance matrix still shows alias resolution, graph-pattern equivalence, and cross-target semantic equivalence as not started.

### Guardrails
- do **not** reopen public query language design
- do **not** collapse query meaning into implementation-specific syntax
- keep OFARM internal-model-first
- require ambiguity to hard-fail rather than silently degrade

### Acceptance criteria
This amendment wave is complete when OFARM ships executable coverage for:
- version-pinned alias resolution
- deprecated-alias rollover with explicit lineage
- ambiguity hard-fail
- same-semantics query equivalence fixtures across execution targets

---

### 6.4 Amendment D — evidence sufficiency structure for high-consequence uses

**Change class:** companion-artifact extension + machine contract + output/materialization conformance

### Proposed new files
- `01_companion_artifacts/OFARM_Evidence_Sufficiency_and_Attestation_Policy_v0_1.md`
- `03_machine_contracts/schemas/evidence/OFARM_EvidenceSufficiencyCase_schema_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/evidence/OFARM_EvidenceSufficiencyCase_example_compliance_assertion_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/evidence/OFARM_EvidenceSufficiencyCase_example_attested_document_v0_1.json`
- `04_implementation_and_conformance/examples_and_fixtures/examples/machine_contracts/evidence/OFARM_EvidenceSufficiencyCase_example_refusal_v0_1.json`

### Active files affected later
- `00_active_baseline/OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md`
- `01_companion_artifacts/OFARM_Compiled_Output_and_Passport_Taxonomy_Note_v0_1.md`
- `02_accepted_rfcs/OFARM_Current_State_Materialization_RFC_v0_1.md`
- `04_implementation_and_conformance/historical_archive/historical_archive/historical/OFARM_conformance_coverage_matrix_v0_1.md`

### Why this amendment is justified
OFARM already has an evidence sufficiency gate, high-consequence materialization rules, and output/basis separation.
What it still lacks is a structured object that records:
- which policy was applied
- which evidence and provenance links mattered
- which basis state was relied upon
- why the result was allow, refuse, or route-to-review

### Guardrails
- do **not** make every routine farm action carry a heavyweight assurance case
- keep this structure for high-consequence compliance, attested outputs, and submissions
- do **not** let compiled outputs become the truth store
- preserve the raw-source-versus-interpretation discipline

### Acceptance criteria
This amendment wave is complete when OFARM can produce machine-readable sufficiency cases for:
- accepted compliance assertions
- attested/frozen document outputs
- submission packages
- refusal or review-routing because evidence is insufficient

---

### 6.5 Amendment E — runtime boundary envelopes and conformance depth

**Change class:** implementation/conformance implication + narrow horizontal contract wave

### Proposed new files
- `03_machine_contracts/schemas/authority/OFARM_AuthorizationDecisionRequest_schema_v0_1.json`
- `03_machine_contracts/schemas/authority/OFARM_AuthorizationDecisionResult_schema_v0_1.json`
- `03_machine_contracts/schemas/current_state/OFARM_MaterializationRequest_schema_v0_1.json`
- `03_machine_contracts/schemas/current_state/OFARM_MaterializationResult_schema_v0_1.json`
- `03_machine_contracts/schemas/query/OFARM_QueryExecutionRequest_schema_v0_1.json`
- `03_machine_contracts/schemas/query/OFARM_QueryExecutionResult_schema_v0_1.json`
- `03_machine_contracts/schemas/output_assembly/OFARM_PublicationAssemblyRequest_schema_v0_1.json`
- `03_machine_contracts/schemas/output_assembly/OFARM_PublicationAssemblyResult_schema_v0_1.json`
- `03_machine_contracts/schemas/output_assembly/OFARM_PassportViewMetadata_schema_v0_1.json`
- `03_machine_contracts/schemas/output_assembly/OFARM_DocumentAssemblyMetadata_schema_v0_1.json`

### Expected implementation/conformance changes
- extend contract validation runners
- extend governance/runtime closure runners
- add executable fixtures for delegation/revocation timing
- add AI-assisted decision-gating fixtures
- add no-implicit-sharing fixtures
- add FRESH / STALE / INVALID materialization fixtures
- add refusal / recompute / review-routing fixtures
- add Compliance-versus-Advisory twin materialization fixtures
- add PassportView-versus-DocumentAssembly separation checks

### Active files affected later
- `04_implementation_and_conformance/historical_archive/historical_archive/historical/OFARM_conformance_coverage_matrix_v0_1.md`
- `04_implementation_and_conformance/historical_archive/historical_archive/historical/ofarm_contract_validation_runner_v0_2.py`
- `04_implementation_and_conformance/conformance_runners/authority_and_governance_conformance/ofarm_governance_runtime_closure_runner_v0_1.py`
- supporting fixture sets under `04_implementation_and_conformance/`

### Why this amendment is justified
The readiness memo already identifies missing runtime boundary envelopes beyond pack activation.
The hostile review and coverage matrix both show the same gap: the architecture is mostly settled, but important seams are not yet consistently executable.

### Guardrails
- keep the boundary contracts narrow and semantically grounded
- do **not** standardize accidental internal plumbing
- do **not** introduce hidden write paths around canonical truth
- keep export/publication surfaces downstream of constitutional governance

### Acceptance criteria
This amendment wave is complete when the coverage matrix materially advances these rows:
- delegation and revocation tests
- non-human / AI-assisted action tests
- current-state freshness tests
- high-consequence recomputation/refusal tests
- Compliance-versus-Advisory materialization tests
- alias stability and query equivalence tests
- compiled-output taxonomy and passport-vs-document separation tests
- enforcement-gate sequencing and projection trace-back tests

---

### 6.6 Amendment F — narrow RC2.1 harmonization after closure acceptance

**Change class:** baseline law patch, only after the closure artifacts above are accepted and tested

### Baseline files eligible for later harmonization
- `00_active_baseline/OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md`
- `00_active_baseline/OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md`
- `00_active_baseline/OFARM_Alignment_Register_v0_13.md`

### Expected harmonization scope
- sharpen lot semantics where the new RFC adds precise executable distinctions
- recognize `ContextSnapshot` explicitly where the current package already implies it
- add cross-references for alias governance and evidence-sufficiency closure where needed
- update the Alignment Register only where the closure wave changes explicit consequences or coverage expectations

### Guardrails
- do **not** rewrite the core truth model
- do **not** rewrite the twin model
- do **not** reopen broad pack or query architecture questions
- keep RC2.1 edits minimal and cross-reference-oriented

---

## 7. What should not be amended in this wave

Do **not** do the following now:
- broad Capability Manifest redesign
- broad authority-model redesign
- public query language design restart
- second truth substrate for current state
- generic “passport” bucketting of all compiled outputs
- silent re-entry of legacy FA_RM or FARM_RM terminology into active law

These are either already settled or would create unnecessary churn relative to the real gaps.

---

## 8. Recommended execution order

1. Amendment A — lot traceability and claim-basis closure  
2. Amendment B — ContextSnapshot closure  
3. Amendment C — SemanticPathAlias governance  
4. Amendment D — evidence sufficiency structure  
5. Amendment E — runtime boundary envelopes and conformance depth  
6. Amendment F — narrow RC2.1 harmonization  

This order is intentional.
It closes the sharpest semantic risk first, then the sharpest explainability/reproducibility gaps, then the runtime boundary depth that proves the package is executable.

---

## 9. Exit criteria for the amendment cycle

This amendment cycle is complete when the package can truthfully say:
- lot split/merge/commingling/transformation/shipment continuity is executable and testable
- chain-of-custody claim basis is explicit where mixing semantics matter
- high-consequence current-state basis points to a real ContextSnapshot
- alias resolution is versioned, traceable, and regression-tested
- evidence sufficiency is structured and auditable for high-consequence outputs
- authority/materialization/query/publication seams have narrow machine contracts
- PassportView versus DocumentAssembly separation is machine-checkable
- the coverage matrix materially improves the current lot, alias, revocation, AI-assisted, freshness, twin-materialization, and output-taxonomy gaps

---

## 10. Immediate next authoring tasks

The next authoring move after accepting this plan should be:
1. draft `OFARM_Lot_Traceability_and_Claim_Basis_RFC_v0_1.md`
2. draft `OFARM_ContextSnapshot_Closure_RFC_v0_1.md`
3. add the first lot and context snapshot schemas/examples
4. update the conformance coverage matrix to introduce explicit rows for the new contracts where needed

That is the smallest credible next step that converts this plan into active amendment work.
