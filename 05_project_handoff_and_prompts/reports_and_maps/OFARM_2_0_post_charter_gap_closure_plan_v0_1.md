# OFARM 2.0 post-charter gap closure plan v0.1

Date: 2026-04-08  
Status: planning artifact  
Purpose: close the six remaining post-charter gaps identified in the charter gate without reopening the whole OFARM 2.0 architecture

---

## 1. Objective

Move OFARM 2.0 from:

- **charter-ready with reservations**

to:

- **implementation-directed baseline with bounded RFC debt**

without falling back into another broad rewrite.

The gap-closure program is intentionally narrow.
It addresses only the unresolved areas called out in the charter gate:

1. identity and lifecycle semantics
2. QuerySpecification and QueryPlanIR formal schemas
3. pack merge semantics by surface
4. authority action matrix and policy model
5. Capability Manifest schema and registry relation
6. current-state materialization operational policy

---

## 2. Program rule

Do not reopen the RC2 constitutional decisions unless a gap forces it.

The job now is:
- formalize missing contracts
- make runtime/model interfaces executable
- reduce ambiguity for implementers
- create a smaller RFC stack that can be completed sequentially

This is **not** another concept-generation phase.

---

## 3. Deliverable strategy

Each gap becomes its own RFC stream with:
- one problem statement
- one bounded normative artifact
- one explicit patch set against Constitution RC2 and/or Platform RC2
- one focused skeptical review before acceptance

The point is to keep token context and reasoning depth high by making each unit small and sharp.

---

## 4. Phase map

### Phase 0 — Gap freeze and dependency map
Purpose:
- freeze the six-gap list
- route each gap to Constitution, Platform, or both
- define dependencies so the RFC order is justified

Outputs:
- issue dependency map
- RFC routing table
- no document rewrite yet

Exit criteria:
- every gap has one primary artifact path
- no hidden seventh gap is smuggled in

---

### Phase 1 — RFC-1 Identity and lifecycle semantics
Purpose:
- define lifecycle/version/supersession rules for the objects most likely to cause implementation divergence

Must cover:
- field boundary change: new identity vs new version
- zone lifecycle and lineage
- crop-cycle lifecycle, failed cycles, split cycles, overlapping cycles
- lot identity semantics: physical, logical, commercial, split/merge lineage
- equipment, facility, container lifecycle and identity/versioning
- relationship between durable identity and time-bounded state

Primary outputs:
- **OFARM Identity and Lifecycle RFC v0.1**
- Constitution patch set
- Alignment Register update where needed

Why first:
- identity mistakes spread everywhere
- query, current-state policy, and authority enforcement all depend on identity clarity

Exit criteria:
- implementers can tell when something is “the same thing with a new version” versus “a new thing”

---

### Phase 2 — RFC-6 Current-state materialization operational policy
Purpose:
- turn current-state materialization from a clean principle into a practical operational contract

Must cover:
- what counts as a materialization instance
- invalidation triggers
- refresh/recompute policy
- version/snapshot trace
- staleness rules
- obligations before high-consequence actions
- twin-specific materialization rules
- relation between assertion/history substrate and materialized state

Primary outputs:
- **OFARM Current-State Materialization RFC v0.1**
- Constitution patch set
- Platform patch set

Why second:
- current-state policy depends on identity/lifecycle semantics
- many later RFCs need a stable answer to “what current state means operationally”

Exit criteria:
- builders can explain exactly when materialized state is valid, stale, or must be recomputed

---

### Phase 3 — RFC-2 QuerySpecification and QueryPlanIR formal schemas
Purpose:
- replace prose-only query law with actual machine-usable contracts

Must cover:
- formal schema for QuerySpecification
- formal schema for QueryPlanIR
- alias-resolution contract
- target-twin/scope/time/authority fields
- graph-pattern block representation
- path-alias block representation
- projection/selection/result-profile structure
- semantic-equivalence obligations across execution targets

Primary outputs:
- **OFARM QuerySpecification Schema RFC v0.1**
- Constitution patch set
- Platform patch set
- example query fixtures

Why third:
- query law now exists conceptually, but it is not implementable without schemas
- better done after identity and state semantics are hardened

Exit criteria:
- a tool or service can validate whether a QuerySpecification is well-formed

---

### Phase 4 — RFC-3 Pack merge semantics by surface
Purpose:
- make “declared safe merge” mean something concrete for each surface family

Must cover:
- merge semantics for vocabulary/code bindings
- merge semantics for evidence policies
- merge semantics for templates/archetypes
- merge semantics for event subtypes
- merge semantics for view/output shaping
- merge semantics for rules and validations
- precedence interaction with merge behavior
- when merge is impossible and hard fail is mandatory

Primary outputs:
- **OFARM Pack Merge Semantics RFC v0.1**
- Constitution patch set
- Pack Safety Policy update
- example conflict/merge fixtures

Why fourth:
- the policy layer is already good
- the missing piece is implementation-grade merge semantics

Exit criteria:
- implementers can determine whether two packs touching the same surface:
  - merge safely
  - require governance
  - must hard fail

---

### Phase 5 — RFC-4 Authority action matrix and policy model
Purpose:
- turn principle-level authority law into a practical executable policy model without bloating the Constitution

Must cover:
- action families and sub-actions
- scope inheritance rules
- role-to-authority mapping patterns
- delegation constraints
- revocation behavior
- AI-assisted action treatment
- signing/attestation actions
- pack activation / compiled-output approval / supersession / submission actions
- default deny model and exception structure

Primary outputs:
- **OFARM Authority Policy Model RFC v0.1**
- Platform patch set
- optional Constitution clarifications only if strictly needed
- example policy matrix

Why fifth:
- this is operationally important, but it should be built on already-hardened identity and state assumptions

Exit criteria:
- a policy engine can decide whether a Party may perform a given action at a given scope/time

---

### Phase 6 — RFC-5 Capability Manifest schema and registry relation
Purpose:
- formalize the platform self-description contract and how it relates to artifact/package discovery

Must cover:
- formal Capability Manifest schema
- mandatory fields
- versioning/evolution policy
- relation to package registry and activation state
- compatibility declaration semantics
- declared enforcement-relevant behavior
- optional vs mandatory capability sections
- discovery relation
- conformance relation

Primary outputs:
- **OFARM Capability Manifest RFC v0.1**
- Platform patch set
- example manifests
- compatibility fixtures

Why sixth:
- the Capability Manifest depends on what the previous RFCs settle
- it should describe stabilized capabilities, not shifting assumptions

Exit criteria:
- a deployment can declare its supported capabilities in machine-readable form and a tool can validate it

---

### Phase 7 — Cross-RFC harmonization and RC2.1 baseline patch
Purpose:
- integrate all accepted RFC outcomes without allowing contradictions back in

Must cover:
- Constitution updates
- Platform updates
- companion artifact updates
- cross-reference cleanup
- glossary normalization
- version-compatibility notes between companion artifacts

Primary outputs:
- **Constitution RC2.1**
- **Platform RC2.1**
- updated companion artifacts where needed
- consistency report

Why here:
- doing integration only after all six RFCs are drafted keeps reasoning cleaner and reduces churn

Exit criteria:
- the patched baseline is internally coherent again

---

### Phase 8 — Reference implementation spike and conformance seed set
Purpose:
- prove the architecture is not only elegant prose

Must cover at least:
- one implementation path for identity/lifecycle edge cases
- one implementation path for QuerySpecification parsing/validation
- one implementation path for pack merge decisions
- one implementation path for authority-policy enforcement
- one implementation path for capability-manifest validation
- one implementation path for current-state materialization generation/refresh

Primary outputs:
- reference spike design notes
- conformance seed fixtures
- failure-case examples
- implementation risk memo

Why:
- the charter gate explicitly said the baseline is not implementation-complete
- at least one reference path is the fastest way to expose hidden ambiguity

Exit criteria:
- the hardest interfaces have been exercised in something more concrete than prose

---

### Phase 9 — Final hostile review after gap closure
Purpose:
- assess whether the RFC program actually closed the reservations or merely produced more documents

Must test:
- is the baseline now implementation-directed?
- what still remains too abstract?
- what would still cause divergence between teams?
- what would still make an external standards reviewer skeptical?

Primary outputs:
- final hostile review
- readiness recommendation:
  - implementation-directed with bounded debt
  - still charter-only
  - not coherent enough

Exit criteria:
- explicit go/no-go recommendation for implementation-scale work and external positioning

---

## 5. Recommended order

### Block A — hardest semantic/runtime foundations
Phase 0 -> Phase 1 -> Phase 2 -> Phase 3

### Block B — modularity and governance execution
Phase 4 -> Phase 5 -> Phase 6

### Block C — integration and proof
Phase 7 -> Phase 8 -> Phase 9

This order is deliberate.

Reason:
- identity and state semantics should settle before query schemas
- pack merge semantics should settle before implementation teams try to support real multi-pack farms
- capability self-description should describe a more stabilized runtime, not a moving target

---

## 6. Prompt and context discipline

For maximum quality in ChatGPT Pro:
- run one RFC per prompt/session
- never combine more than one normative gap closure in a single step
- write the RFC first
- then patch the affected baseline documents
- then run one skeptical pass on that RFC before moving on

Bad combinations:
- identity + current-state + query schemas in one prompt
- pack merge + authority action matrix in one prompt
- capability manifest + full RC2.1 rewrite in one prompt

Good combinations:
- one RFC
- one patch set
- one skeptical pass

---

## 7. Success criteria

The program is successful if, at the end:

- RC2.1 is more executable without becoming bloated
- the six charter reservations are materially reduced
- implementation teams can start from formal interfaces instead of only prose
- no new broad rewrite is needed
- external standard ambitions remain future-facing but less speculative

---

## 8. What this plan deliberately avoids

This plan does **not** try to:
- finish every future external profile
- define every jurisdiction/crop pack
- publish a public expert query language
- finalize every agent/tool interoperability surface
- create a full certification ecosystem

Those are downstream programs, not the right next move.

---

## 9. Short recommendation

The immediate next RFC should be:

**RFC-1 Identity and lifecycle semantics**

because identity confusion will poison every other gap if left unresolved.
