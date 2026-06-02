# OFARM wave 6 RC2.1 harmonization memo v0.1

Date: 2026-04-11  
Status: active implementation/conformance memo  
Scope: document the narrow baseline-law harmonization pass performed after Waves 1-5 of the hardest-design amendment plan

---

## 1. Purpose

This memo records the deferred Wave 6 harmonization pass described in `OFARM_hardest_design_amendment_plan_v0_1.md`.

The goal is to align RC2.1 baseline prose with already-accepted closure artifacts from Waves 1-5 without reopening architecture or promoting any new design beyond what is already active.

---

## 2. Affected active baseline files

This pass touches only:
- `00_active_baseline/OFARM_Reference_Model_and_Artifact_Constitution_RC2_1.md`
- `00_active_baseline/OFARM_Platform_Runtime_and_Product_Architecture_RC2_1.md`
- `00_active_baseline/OFARM_Alignment_Register_v0_13.md`

That scope matches the amendment plan’s explicit Wave 6 boundary.

---

## 3. Change class

**Change class:** baseline law patch, minimal and deferred until after wave acceptance.

This pass does **not**:
- add a new architectural layer
- reopen truth-model decisions
- reopen public query language design
- replace RC2.1 with RFC prose
- promote machine-contract detail wholesale into the Constitution

---

## 4. Closure artifacts harmonized into baseline references

This pass aligns RC2.1 prose with the following already-active closure artifacts:
- `02_accepted_rfcs/OFARM_Lot_Traceability_and_Claim_Basis_RFC_v0_1.md`
- `02_accepted_rfcs/OFARM_ContextSnapshot_Closure_RFC_v0_1.md`
- `02_accepted_rfcs/OFARM_SemanticPathAlias_Governance_RFC_v0_1.md`
- `01_companion_artifacts/OFARM_Evidence_Sufficiency_and_Attestation_Policy_v0_1.md`
- Wave 5 runtime-boundary contract family in `03_machine_contracts/`

---

## 5. File-by-file summary

### 5.1 Constitution

The Constitution was patched narrowly to:
- make the PackActivationSet versus ContextSnapshot distinction explicit
- clarify that PackMergeResolutionTrace may ground a ContextSnapshot basis
- point the Lot lifecycle rule at the accepted lot-traceability closure RFC
- add the lot-traceability RFC to the identity/authority companion list
- add the alias-governance RFC to the query companion list
- state that the concrete context-basis realization is ContextSnapshot
- connect attested/claim-bearing/filed DocumentAssembly use to evidence-sufficiency policy
- expand the section-10 companion list to include ContextSnapshot closure and evidence-sufficiency policy
- add a glossary entry for `ContextSnapshot`

### 5.2 Platform

The Platform baseline was patched narrowly to:
- require high-consequence materialization basis to resolve to a governed ContextSnapshot
- require alias resolution to identify a governing alias catalog and traceable resolution outcome
- connect attested/claim-bearing/filed DocumentAssembly runtime behavior to evidence-sufficiency evaluation
- restate that runtime metadata contracts must preserve PassportView versus DocumentAssembly separation
- acknowledge typed request/result envelopes at the authorization boundary without changing governing semantics
- extend the minimum conformance/testability baseline to include ContextSnapshot, alias-resolution trace, EvidenceSufficiencyCase, and request/result-envelope tests
- add a glossary entry for `ContextSnapshot`

### 5.3 Alignment Register

The Alignment Register was patched narrowly to:
- add `ContextSnapshot` as a first-class OFARM-owned truth/governance concept
- sharpen the `Lot` row to mention shipment-reference continuity explicitly
- sharpen the `PackActivationSet` row to show its role in later ContextSnapshot grounding
- sharpen the `MaterializationBasis` row to include resolved context
- sharpen the `SemanticPathAlias` row to mention governed alias catalogs and explicit resolution traces
- add `ContextSnapshot` to the truth-mechanics consequence list

---

## 6. Controlled risks

This harmonization pass intentionally avoids:
- introducing a broad `TraceObject` family
- treating ContextSnapshot as a second truth store
- turning alias catalogs into a second schema
- flattening PassportView and DocumentAssembly into one output family
- turning runtime envelopes into a new constitutional ontology

---

## 7. Outcome

After this pass:
- baseline law now explicitly points to the accepted lot, context-snapshot, alias-governance, and evidence-sufficiency closures
- baseline law now acknowledges the Wave 5 runtime-boundary contract family at the runtime-law level
- the Alignment Register now includes `ContextSnapshot` and reflects the tightened post-wave semantics
- RC2.1 remains intact as the governing baseline; this is a harmonization patch, not a redesign
