# OFARM Query Architecture Note v0.1

Date: 2026-04-08  
Status: phase-8 baseline artifact  
Scope: normative note for the internal canonical query model of OFARM 2.0

---

## 1. Purpose

OFARM needs a query model that is:
- semantically native
- archetype/template-aware
- safe for AI mediation
- compatible with graph querying
- compatible with current-state materializations and derived projections
- not prematurely frozen into a public syntax in v2

This note defines that baseline.

---

## 2. Core stance

OFARM standardizes an **internal canonical query model** in v2.

OFARM does **not** standardize a public expert textual syntax in v2.

This is deliberate:
- the model must be hard enough to build against
- the syntax should stay flexible until the internal model stabilizes

---

## 3. Main influences

The OFARM internal query model intentionally borrows lessons from:
- graph-pattern querying
- archetype/path-addressed querying
- geospatial/resource filter languages

But OFARM does not simply adopt any one of them as-is.

The internal model should be understood as:
- graph-pattern-first for semantic relationships
- path-aware for archetype/template-bound content
- filter-rich for spatial, temporal, provenance, pack, and authority constraints

---

## 4. QuerySpecification

The canonical constitutional query artifact is **QuerySpecification**.

A QuerySpecification defines at minimum:

- target twin
- target scope
- target time policy
- target authority/sharing context where relevant
- anchor concepts/entities
- graph pattern block
- optional semantic path-alias block
- predicate/filter block
- selection/projection block
- ordering/pagination block where relevant
- result profile or ViewModule reference where relevant

QuerySpecification is an abstract formal object.
It is not yet a public text language commitment.

---

## 5. Graph-pattern core

The primary semantic retrieval mechanism is the **graph pattern**.

Reason:
- OFARM truth is relational and semantic
- state depends on relationships, lineage, evidence, roles, packs, and review state
- graph patterns are the right base for that kind of retrieval

This means queries should be able to express:
- entity/relation matching
- multi-hop lineage
- optional related structures
- provenance-bound conditions
- review-state and validity predicates

---

## 6. SemanticPathAlias

OFARM also recognizes **SemanticPathAlias**.

Purpose:
- provide governed shorthand into archetype/template-bound content structures
- make content-bound retrieval practical without forcing users or tools to reason only in raw graph relations

Rules:
- a SemanticPathAlias must resolve to a semantic anchor or a content node under a semantic anchor
- a SemanticPathAlias may not become a hidden alternate schema
- if alias resolution becomes stale or ambiguous, the system should fail clearly rather than guess

SemanticPathAlias is convenience with governance, not a substitute for semantic meaning.

---

## 7. Filter families

The canonical query model should support at least these filter families:

- structural/relationship predicates
- scalar/value predicates
- temporal predicates
- spatial predicates
- provenance predicates
- authority/sharing predicates
- epistemic/review-status predicates
- pack/profile/validity predicates

This is one reason OFARM should keep an abstract model first and a public syntax later.

---

## 8. View and passport relation

A **ViewModule** is not the same thing as a query.

But a ViewModule should compile from:
- one or more QuerySpecifications
- additional result shaping/presentation rules

Similarly:
- Farm Passport family outputs compile from QuerySpecifications + view logic
- Document Assembly compiles from state/history/evidence plus view logic and attestation rules

This keeps retrieval, presentation, and publication separate.

---

## 9. AI mediation rule

AI-mediated retrieval must compile through formal objects.

Recommended chain:
1. human request
2. AI interpretation
3. QuerySpecification
4. runtime QueryPlanIR
5. governed execution
6. result shaping via ViewModule or direct result profile

The platform must not allow freeform prompt text to become ungoverned backend queries.

---

## 10. QueryPlanIR

**QueryPlanIR** is a runtime planning representation, not the constitutional query artifact itself.

Purpose:
- take a QuerySpecification
- resolve aliases, scopes, twin constraints, and policies
- compile to one or more execution targets

Possible execution targets include:
- semantic graph engines
- current-state materializations
- derived read models or search indexes
- resource/geospatial filter endpoints

The same QuerySpecification may compile differently for performance reasons, provided semantic equivalence and traceability are preserved.

---

## 11. External/runtime filter surfaces

OFARM may expose runtime filter surfaces for specific APIs or resource views.

Examples:
- geospatial/resource APIs
- search/list APIs
- partner-facing projections

Those runtime surfaces may use other filter notations.
They are not the canonical query model itself.

---

## 12. Safety rules

### 12.1 No hidden schema rule
Storage layout or index layout must not redefine canonical query meaning.

### 12.2 No alias drift rule
Path aliases must stay governed and versioned.

### 12.3 No AI shortcut rule
AI may help author or refine QuerySpecifications.
AI may not directly bypass governed query compilation.

### 12.4 No projection-only semantics rule
If a query can only be answered from one projection because meaning was never preserved in canonical truth, the architecture is wrong.

---

## 13. Public exposure posture

In v2:
- internal canonical query model = yes
- saved query/view artifacts = yes
- AI-guided retrieval = yes
- public expert textual query language = no

Future public exposure remains possible, but should follow the internal model rather than precede it.
