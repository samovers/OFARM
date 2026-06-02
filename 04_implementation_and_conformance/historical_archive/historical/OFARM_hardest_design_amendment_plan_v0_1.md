# OFARM hardest-design amendment plan v0.1

Date: 2026-04-11  
Status: active supporting implementation plan  
Scope: translate `06_active_supporting_research/syntheses/OFARM_research_hardest_design_problems_v0_1.md` into a bounded amendment program for the active OFARM 2 baseline without reopening RC2.1 architecture

---

## 1. Purpose

This plan converts the hardest-design-problems research report into a controlled OFARM amendment program.

It does **not** treat the report as active law.
It uses the report as a prioritisation input against the active authority set:
- `00_active_baseline/`
- `01_companion_artifacts/`
- `02_accepted_rfcs/`
- `03_machine_contracts/`

The goal is to close the remaining executable gaps that the report correctly highlights while preserving the RC2.1 architecture.

---

## 2. Authority basis and decision rule

### 2.1 Governing rule
The active OFARM authority order remains:
1. `00_active_baseline/`
2. `02_accepted_rfcs/`
3. `01_companion_artifacts/`
4. `03_machine_contracts/`

The hardest-design-problems report lives in `06_active_supporting_research/` and therefore informs this plan but does not override RC2.1 by itself.

### 2.2 Files that control this plan
This amendment plan is grounded primarily in:
- `PROJECT_AUTHORITY.md`
- `ACTIVE_SUBSTANCE_README.md`
- `00_active_baseline/OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md`
- `00_active_baseline/OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md`
- `00_active_baseline/OFARM_Alignment_Register_v0_13.md`
- `00_active_baseline/OFARM_post_gap_closure_readiness_gate_memo_v0_1.md`
- `00_active_baseline/OFARM_final_hostile_review_after_gap_closure_v0_1.md`
- `04_implementation_and_conformance/historical_archive/historical_archive/historical/OFARM_conformance_coverage_matrix_v0_1.md`
- `06_active_supporting_research/syntheses/OFARM_research_hardest_design_problems_v0_1.md`

### 2.3 Amendment posture
The controlling package already says the next move is:
- controlled closure work on contracts and conformance
- not another architecture rewrite
- not another charter round

This plan follows that posture.

---

## 3. Working assessment

The report is directionally correct about OFARM’s hardest remaining problems.
The package’s own readiness artifacts agree that the most important remaining debt is now concentrated in:
- lot pressure cases and claim-basis-sensitive lineage
- context/materialization explainability depth
- alias stability and query reproducibility
- evidence sufficiency structure for high-consequence outputs
- runtime boundary envelopes beyond pack activation
- output-taxonomy, sharing/revocation, and AI-assisted authority depth

The architecture itself is **not** the main issue anymore.
The issue is that several already-decided semantic moves still need tighter executable closure.

---

## 4. Recommendation triage

| Report recommendation | Disposition in this plan | Reason | Primary amendment target |
|---|---|---|---|
| 1. Formalise TraceObject/Lot algebra | Promote as RFC extension | Biggest remaining domain/runtime drift risk | lot traceability + claim-basis closure |
| 2. Add chain-of-custody model semantics | Promote with lot closure | Same seam as lot identity under mixing | lot traceability + claim-basis closure |
| 3. Require explainable MaterializationBasis | Treat as already-active law needing closure | Current-state law already makes this move | context snapshot + runtime/materialization tests |
| 4. Compile PackActivationSet into effective context snapshot | Promote as RFC extension | Context snapshot is implied but not yet explicitly contracted | ContextSnapshot closure |
| 5. Govern SemanticPathAlias like a canonical resource | Promote as RFC extension | Alias drift remains uncovered in conformance matrix | alias governance + query reproducibility |
| 6. Relationship+ABAC hybrid authorization kernel | Treat as mostly-active law needing deeper executable closure | Authority model already formalises action classes, inheritance, delegation, AI restrictions | runtime boundary and authority conformance |
| 7. Constrain offline auto-merge to draft layer | Treat as already-active law needing stronger fixtures | RC2.1 already keeps capture/draft/promotion distinct | commit-promotion + sync conformance |
| 8. Implement evidence sufficiency as compilable structure | Promote as companion-policy extension + contract | Biggest high-consequence evidence gap | evidence sufficiency + attestation policy |
| 9. Evolve Capability Manifest into verifiable ecosystem interface | Treat as mostly closed in current package | v0.6 already added narrow manifest + reference extensions | only expand negative fixtures later |
| 10. Ship conformance tooling with the standard | Treat as active program direction needing broader closure | Package already ships contract/runner patterns | runtime-boundary + conformance wave |

---

## 5. Amendment principles

### 5.1 Smallest controlled patch
Use the smallest patch that closes the missing executable contract.
Do not create a fresh architecture layer unless existing active law is genuinely insufficient.

### 5.2 RFC-first closure order
For each open seam, use this order:
1. add narrow RFC or companion-policy closure where active law is missing
2. add machine contracts and examples
3. add executable conformance fixtures and runners
4. only then harmonise RC2.1 baseline references

### 5.3 No silent promotion into baseline law
This plan itself is a supporting implementation artifact.
Nothing in this document becomes active OFARM law until separately accepted into the active authority set.

### 5.4 Preserve core OFARM invariants
This amendment cycle must preserve:
- assertion/history-first truth
- governed current-state materialisation
- explicit authority and explicit evidence policy
- strict promotion law
- one semantic substrate with logical twins
- clear separation between truth, projection, and compiled output

---

## 6. Amendment waves

### Wave 1 — lot traceability and claim-basis closure

**Change class:** RFC extension + machine contracts + conformance expansion

**Add to active set when accepted**
- `02_accepted_rfcs/OFARM_Lot_Traceability_and_Claim_Basis_RFC_v0_1.md`
- `03_machine_contracts/schemas/core/OFARM_LotLineageChange_schema_v0_1.json`
- `03_machine_contracts/schemas/core/OFARM_TraceabilityClaimBasis_schema_v0_1.json`
- example fixtures for split, merge/commingle, transform, shipment-reference continuity, and claim-basis reset

**Why this wave exists**
The Constitution, Identity RFC, and Alignment Register already say lot identity is cohort-first and must break or branch under split, merge/commingle, transformation, and strong claim-basis change. The missing piece is a tighter executable algebra and conformance-ready fixture set.

**Baseline files affected later**
- `00_active_baseline/OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md`
- `00_active_baseline/OFARM_Alignment_Register_v0_13.md`
- `04_implementation_and_conformance/historical_archive/historical_archive/historical/OFARM_conformance_coverage_matrix_v0_1.md`

**Main risks**
- Do not introduce a new generic constitutional `TraceObject` family unless lot-first closure proves insufficient.
- Do not allow mass-balance or book-and-claim semantics to masquerade as identity-preserved lineage.

**Acceptance criteria**
- split/merge/commingle/transform/shipment continuity cases are executable
- claim-basis transitions are query-visible
- lineage requires explicit edges and evidence hooks
- coverage matrix advances the lot rows materially beyond the current partial state

### Wave 2 — context snapshot closure

**Change class:** RFC extension + machine contract + materialization/runtime closure

**Add to active set when accepted**
- `02_accepted_rfcs/OFARM_ContextSnapshot_Closure_RFC_v0_1.md`
- `03_machine_contracts/schemas/current_state/OFARM_ContextSnapshot_schema_v0_1.json`
- examples showing resolved active packs, profiles, scoped extensions, governing policy revisions, and merge traces

**Why this wave exists**
Current-state law already requires a `context snapshot` basis for materialisation, and `MaterializationBasis` already carries `contextSnapshotRefs`. The package still lacks a concrete object contract for what a context snapshot is.

**Baseline files affected later**
- `00_active_baseline/OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md`
- `02_accepted_rfcs/OFARM_Current_State_Materialization_RFC_v0_1.md`
- `00_active_baseline/OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md` only if cross-reference tightening is needed

**Main risks**
- Do not let `ContextSnapshot` become a hidden truth store.
- Do not confuse runtime cache state with a governed basis object.

**Acceptance criteria**
- high-consequence `MaterializationBasis` points to a real `ContextSnapshot`
- snapshot examples include enough active context to explain recomputation
- runtime tests distinguish basis-preserving recomputation from basis drift

### Wave 3 — alias governance and query reproducibility

**Change class:** RFC extension + machine contracts + query conformance suites

**Add to active set when accepted**
- `02_accepted_rfcs/OFARM_SemanticPathAlias_Governance_RFC_v0_1.md`
- `03_machine_contracts/schemas/query/OFARM_SemanticPathAliasCatalog_schema_v0_1.json`
- `03_machine_contracts/schemas/query/OFARM_SemanticPathAliasResolutionTrace_schema_v0_1.json`
- fixtures for version-pinned resolution, deprecated alias rollover, ambiguity hard-fail, and cross-target semantic-equivalence checks

**Why this wave exists**
The query note and platform law already require governed, versioned alias handling. The gap is an executable alias catalog contract plus regression fixtures.

**Baseline files affected later**
- `01_companion_artifacts/OFARM_Query_Architecture_Note_v0_1.md`
- `00_active_baseline/OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md`
- `04_implementation_and_conformance/historical_archive/historical_archive/historical/OFARM_conformance_coverage_matrix_v0_1.md`

**Main risks**
- Do not reopen public expert query language design.
- Do not allow alias resolution to depend on hidden runtime conventions.

**Acceptance criteria**
- alias resolution is versioned and traceable
- ambiguous alias resolution hard-fails
- same logical query can be checked for semantic equivalence across targets
- coverage matrix closes alias-stability gaps currently marked not started

### Wave 4 — evidence sufficiency and attestation policy closure

**Change class:** companion-artifact extension + machine contract + output/materialization conformance

**Add to active set when accepted**
- `01_companion_artifacts/OFARM_Evidence_Sufficiency_and_Attestation_Policy_v0_1.md`
- `03_machine_contracts/schemas/evidence/OFARM_EvidenceSufficiencyCase_schema_v0_1.json`
- examples for compliance assertion support, attested document support, submission support, and refusal cases

**Why this wave exists**
OFARM already has evidence-policy modules, evidence sufficiency gating, and output taxonomy boundaries. The missing piece is a structured evaluation object linking claim, governing policy, evidence bundle, basis state, and outcome.

**Baseline files affected later**
- `00_active_baseline/OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md`
- `01_companion_artifacts/OFARM_Compiled_Output_and_Passport_Taxonomy_Note_v0_1.md`
- `04_implementation_and_conformance/historical_archive/historical_archive/historical/OFARM_conformance_coverage_matrix_v0_1.md`

**Main risks**
- Do not make routine farm actions carry heavyweight assurance-case overhead.
- Do not let compiled outputs become hidden truth stores.

**Acceptance criteria**
- evidence sufficiency becomes machine-checkable for high-consequence actions
- refusal/review/allow outcomes are distinguishable and traceable
- PassportView and DocumentAssembly remain separate from canonical truth

### Wave 5 — runtime boundary envelopes and conformance expansion

**Change class:** implementation/conformance implication with narrow contract wave

**Add to active set when accepted**
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

**Implementation work in support layer**
- extend runtime/conformance runners
- add fixtures for delegation, revocation, AI-assisted gating, freshness states, refusal/reroute logic, twin differences, and output-class separation

**Why this wave exists**
The readiness memo and hostile review both identify runtime boundary envelopes beyond pack activation as a remaining bounded debt cluster.

**Baseline files affected later**
- mostly `04_implementation_and_conformance/` first
- RC2.1 baseline only if envelope work reveals a real contradiction

**Main risks**
- Do not over-standardise internal plumbing.
- Keep envelopes narrow, typed, and semantically anchored.

**Acceptance criteria**
- authority/materialization/query/publication seams have typed request/result envelopes
- AI-assisted and non-human authority paths become executable
- current-state freshness and refusal routing cover FRESH, STALE, and INVALID outcomes
- PassportView vs DocumentAssembly separation becomes machine-checkable

### Wave 6 — narrow RC2.1 harmonisation pass

**Change class:** baseline law patch, minimal and deferred until after wave acceptance

**Touch only after prior waves are accepted**
- `00_active_baseline/OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md`
- `00_active_baseline/OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md`
- `00_active_baseline/OFARM_Alignment_Register_v0_13.md`

**Why this wave is last**
RC2.1 should only be edited once the new closure artifacts are real, accepted, and test-backed. Otherwise prose will outrun executable meaning again.

**Main risks**
- Do not smear draft RFC detail broadly into the constitutional baseline.
- Do not let harmonisation become a disguised redesign.

**Acceptance criteria**
- baseline cross-references match accepted closure artifacts
- no new broad architecture questions are opened
- baseline edits stay narrow and traceable to accepted closure work

---

## 7. Explicit deferrals and non-goals

This amendment cycle should **not** do the following unless later evidence shows a real contradiction:
- broad Capability Manifest redesign
- broad authority-model redesign
- public expert query language standardisation
- a new generic `TraceObject` constitutional family
- auto-merge or CRDT-based promotion into compliance truth
- any change that makes projections or compiled outputs act like canonical truth

---

## 8. Sequencing and dependency order

Recommended execution order:
1. Wave 1 — lot traceability and claim-basis closure
2. Wave 2 — context snapshot closure
3. Wave 3 — alias governance and query reproducibility
4. Wave 4 — evidence sufficiency and attestation policy closure
5. Wave 5 — runtime boundary envelopes and conformance expansion
6. Wave 6 — narrow RC2.1 harmonisation

Dependencies:
- Wave 2 depends on existing current-state law, but not on Wave 1.
- Wave 3 can run in parallel with late Wave 2 if query/runtime staffing allows.
- Wave 4 should consume the MaterializationBasis/ContextSnapshot pattern from Wave 2.
- Wave 5 should reuse outcomes from Waves 1–4 rather than pre-empting them.
- Wave 6 depends on accepted outputs from all earlier waves.

---

## 9. Exit condition for this amendment cycle

This cycle is complete when the package can honestly say all of the following are true:
- lot split/merge/commingle/transform/shipment continuity is executable
- claim-basis-sensitive lineage is represented without hidden semantics
- high-consequence `MaterializationBasis` points to a real `ContextSnapshot`
- alias resolution is versioned, traceable, and regression-tested
- evidence sufficiency is machine-checkable where OFARM already treats the action as high consequence
- authority/materialization/query/publication seams have typed request/result envelopes
- PassportView vs DocumentAssembly separation is machine-checkable
- the coverage matrix materially advances lot, alias, revocation, AI-assisted, freshness, and output-taxonomy rows beyond the current partial/not-started posture

---

## 10. Immediate next authoring set

The smallest useful next authoring set after this plan is:
- draft `OFARM_Lot_Traceability_and_Claim_Basis_RFC_v0_1.md`
- draft `OFARM_ContextSnapshot_Closure_RFC_v0_1.md`
- draft `OFARM_SemanticPathAlias_Governance_RFC_v0_1.md`
- draft `OFARM_Evidence_Sufficiency_and_Attestation_Policy_v0_1.md`
- prepare matching schema outlines for the wave-1 to wave-4 machine contracts
- extend the conformance matrix with a named closure tranche for these additions

That is the smallest amendment bundle that matches both the research report and the active RC2.1 readiness posture.
