# OFARM Campaign Query and Retrieval Regression Spec v0.1

Date: 2026-04-14  
Status: proposed active supporting implementation artifact  
Scope: define campaign-grade retrieval obligations for the staple-crop scenarios most likely to expose query divergence across execution targets

---

## 1. Purpose

The OFARM query model is already formal and architecture should not be reopened.

What is still missing is enough campaign-grade regression proof for the retrieval questions that matter most in real farming disputes, filings, storage campaigns, and buyer interactions.

---

## 2. Core stance

- query correctness must be scenario-visible
- equivalent meaning across execution targets is mandatory
- ambiguity must fail clearly

---

## 3. Mandatory query families

### 3.1 `as_of_incident_scope_state`
Canonical question: what was the in-force state of this scope at the time of the incident or decision?

Minimum scenario coverage:
- crop switch after failure
- subsidy filing after field revision
- spray-drift or contamination incident

Mandatory proof:
- event time and evaluation time remain distinct
- same query meaning survives across execution targets
- ambiguous time posture fails clearly

### 3.2 `current_storage_contents`
Canonical question: what lot or lots are currently in this storage location or container, under which claim basis and condition posture?

Minimum scenario coverage:
- wet grain hold/dry/store/deliver
- storage transfer
- sublot split and later merge

Mandatory proof:
- lot identity and storage occupancy do not drift across targets
- stale condition basis is marked or refused according to profile
- trace-back to lot lineage and relevant materialization basis is available

### 3.3 `evidence_supporting_accepted_consequence`
Canonical question: which evidence bundles and review decisions support the accepted consequence that is now in force?

Minimum scenario coverage:
- variable-rate fertiliser reconciliation
- ambiguous PPP record later upgraded
- corrective-action or inspection closure

Mandatory proof:
- output or materialized answer can trace back to evidence bundles
- later supersession remains visible
- conflicting or partial evidence remains query-visible rather than erased

### 3.4 `lot_claim_basis_before_after_reset`
Canonical question: what claim basis applied before and after this lot change, and did physical continuity remain one-to-one?

Minimum scenario coverage:
- split and merge/commingle
- claim-basis reset
- buyer-facing rejection or reclassification

Mandatory proof:
- claim-basis difference is query-visible
- same-lot continuity is not falsely reported across a red-flag boundary
- shipment references alone do not fabricate new lot identity

### 3.5 `same_field_across_revision`
Canonical question: how do operations, filings, and observations resolve across field revisions without falsely creating a new field?

Minimum scenario coverage:
- field boundary correction during season
- operations recorded on old geometry
- filing assembled on new revision

Mandatory proof:
- field identity stays stable where law says it should
- revision-aware retrieval remains deterministic
- old and new revision views are both reconstructable

### 3.6 `recipient_specific_lot_view`
Canonical question: what is the governed lot answer for farm operator, buyer, and certifier respectively?

Minimum scenario coverage:
- shared lot queried by three recipients
- organic/conventional segregation or buyer delivery context

Mandatory proof:
- same substrate, different governed visibility
- correct output family per recipient
- read-only access does not imply write or review authority

### 3.7 `late_evidence_supersession_chain`
Canonical question: what changed after late evidence arrived, and which frozen outputs or accepted consequences were superseded?

Minimum scenario coverage:
- post-filing late evidence
- late lab result after a dossier was assembled

Mandatory proof:
- old and new outputs are both retrievable
- basis snapshots differ and are preserved
- the runtime does not silently patch the old output in place

---

## 4. Negative cases that must be present

Every mandatory query family should include at least one negative case showing:
- ambiguous alias version
- ambiguous time policy
- insufficiently pinned claim basis
- scope mismatch across revision/lineage boundary
- sharing or authority denial for retrieval

These failures should be explicit and reproducible.

---

## 5. Minimum execution-target obligations

For each required query family, implementations should prove semantic equivalence across at least two targets chosen from:
- canonical graph execution
- current-state materialization
- derived read model/search index

If one target cannot safely answer the query without semantic loss, the runtime should fail clearly rather than degrade.

---

## 6. Minimum trace-back obligations

Every campaign-grade query answer should expose enough linkage to recover:
- query or saved-view ref
- materialization basis ref where current state was used
- context snapshot ref where relevant
- underlying lot/field/cycle/output lineage refs where relevant
- relevant frozen output refs where the answer came from a frozen family

---

## 7. Mandatory fixture result checks

A conforming implementation should demonstrate:
- equivalent `as_of_incident_scope_state` answers across two targets
- deterministic `current_storage_contents` under transfer and drying events
- retrievable evidence chain for an accepted consequence after later upgrade
- visible claim-basis transition across a lot reset
- stable field identity across revision-aware retrieval
- governed recipient difference on the same lot
- preserved supersession chain after late evidence

---

## 8. Non-goals

This note does not:
- standardize a public textual query language
- create a second retrieval model beside QuerySpecification
- authorize target-specific semantic shortcuts
