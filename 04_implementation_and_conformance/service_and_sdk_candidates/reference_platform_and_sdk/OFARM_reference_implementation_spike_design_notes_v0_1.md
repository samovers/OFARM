# OFARM reference implementation spike design notes v0.1

Date: 2026-04-08  
Status: phase-8 baseline artifact  
Scope: bounded spike that exercises the hardest post-charter interfaces in something closer to executable system behavior than pure prose

---

## 1. Executive stance

The spike should not attempt to “implement OFARM.”

That would be the wrong move.

The spike should do two things:

1. prove that the hardest contracts can be exercised together without collapsing into ambiguity  
2. produce a conformance seed set that later implementations can extend

The spike therefore uses:

- **one vertical slice**
- **one lightweight contract-validation harness**
- **a focused seed fixture set**
- **an implementation risk memo**

That is enough to expose hidden friction without wasting effort on a fake full product.

---

## 2. Recommended spike shape

### 2.1 Two complementary parts

#### Part A — contract-validation harness
Purpose:
- validate schemas
- run deterministic decision functions on seed fixtures
- prove that the RFC contracts are not only prose

This harness is deliberately narrow.
It is not a production engine.

#### Part B — one vertical slice
Purpose:
- exercise the main runtime path that crosses:
  - delegated authority
  - pack merge behavior
  - evidence sufficiency
  - current-state invalidation/recompute
  - query/path resolution
  - passport output generation
  - capability-manifest grounding

---

## 3. Chosen vertical slice

### 3.1 Scenario
**Delegated service-provider execution on an orchard field under Slovenia + Organic + Orchard packs, followed by fresh field-passport regeneration.**

### 3.2 Why this slice
This slice is the best first spike because it touches all high-risk seams at once:

- identity/lifecycle context through field/crop-cycle references
- pack merge through evidence-policy and template-constraint overlap
- authority through delegated service-provider action
- truth/promotion through operation claim + evidence + accepted consequence
- materialization through invalidation and recompute
- query through QuerySpecification and alias resolution
- compiled output through PassportView
- capability self-description through manifest validation

### 3.3 Minimal flow
1. validate deployment Capability Manifest  
2. validate QuerySpecification for field passport retrieval  
3. evaluate pack overlap for evidence policy and template constraints  
4. evaluate delegated authority for service provider reporting execution  
5. create operation claim and evidence records  
6. apply evidence sufficiency rule  
7. accept executed intervention consequence  
8. invalidate previous field current-state materialization  
9. recompute fresh compliance current-state materialization  
10. generate Field PassportView from query + view logic  

---

## 4. Spike components

### 4.1 Identity decision component
Purpose:
- classify scenarios into:
  - same identity
  - new revision
  - new identity with lineage

Covers:
- field boundary revision vs split
- crop-cycle failure vs replant
- lot commingling

### 4.2 Query contract component
Purpose:
- validate QuerySpecification
- validate QueryPlanIR where produced
- prove alias resolution is version-aware enough for the spike

### 4.3 Pack merge component
Purpose:
- evaluate surface-family merge legality
- produce merge/fail result
- later upgrade path toward PackMergeResolutionTrace

### 4.4 Authority decision component
Purpose:
- evaluate action-based authorization
- evaluate delegated service-provider execution
- deny buyer write path
- model AI/human approval posture later if needed

### 4.5 Current-state materialization component
Purpose:
- classify freshness
- detect invalidation after relevant triggers
- force recompute before high-consequence use

### 4.6 Capability-manifest component
Purpose:
- validate manifest schema
- prove active-artifact grounding is part of deployment self-description

---

## 5. What this spike intentionally does not do

The spike does not try to:
- build a real UI
- build a real graph store
- implement all pack families
- implement all authority action classes
- optimize queries
- produce a real full passport application stack
- build external integrations end to end

That would be fake completeness.

---

## 6. Repository/harness shape

A reasonable spike structure is:

- `/schemas`
  - QuerySpecification schema
  - QueryPlanIR schema
  - Capability Manifest schema

- `/fixtures`
  - identity fixtures
  - pack merge fixtures
  - authority fixtures
  - current-state fixtures
  - vertical slice manifest/query fixtures

- `/harness`
  - schema validation
  - deterministic reference decision functions
  - run results

- `/notes`
  - design notes
  - risk memo
  - failure examples

This spike package follows that spirit in lightweight form.

---

## 7. Success criteria

The spike is successful if it proves, at minimum:

- identity/lifecycle decisions are not pure guesswork
- QuerySpecification is actually machine-validatable
- pack merge decisions are not only policy prose
- action-based authorization can return deterministic outcomes
- current-state freshness can be invalidated and recomputed
- Capability Manifest can be validated and tied to runtime claims
- one realistic vertical slice can pass through the architecture without conceptual collapse

---

## 8. Exit criterion judgment

This spike is not meant to prove:
- production readiness

It is meant to prove:
- the hardest interfaces have now been exercised in something more concrete than prose

That is the right exit criterion for this phase.

---

## 9. Update in v0.4

The delivered package now includes the previously indexed spike `fixtures/` and `schemas/` payload, a packaged reproducibility note, and a rerun result generated from the delivered package. The vertical slice remains a design fixture, while the constituent seam checks remain executable and intentionally narrow.


---

## 10. Update in v0.5

The surrounding package now adds executable pack-activation and manifest-grounding contracts around the spike. That does not change the spike’s own narrow design-fixture role, but it reduces the amount of runtime-governance behavior that previously existed only as prose around the spike.
