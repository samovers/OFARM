# OFARM Pack Safety and Compatibility Policy v0.2

Date: 2026-04-08  
Status: updated by RFC-3 pack merge semantics  
Scope: normative pack law for safe modular composition in OFARM 2.0

---

## 1. Purpose

Packs are powerful because they can carry real farming context:
- regulation
- certification
- crop-system logic
- tooling/method constraints
- local/community context

That same power can become chaos unless OFARM makes pack behavior predictable.

This policy defines:
- what a pack must declare
- what a pack may change
- what a pack must never change
- how compatibility is classified
- how conflicts are resolved
- what the default failure behavior is

---

## 2. Core principle

A pack is an **installable context module** that assembles governed artifacts.

A pack is **not**:
- a semantic fork of OFARM
- a hidden mini-platform
- an excuse to bypass constitutional truth law
- a free-form bundle with unspecified behavior

---

## 3. Activation and compatibility are evaluated by activation set

Compatibility is not an abstract global property.
It is evaluated for a specific **PackActivationSet** defined by:

- time
- scope
- active packs
- active profiles
- active scoped extensions
- relevant precedence classes

This matters because two packs may be:
- compatible at different scopes
- compatible in sequence over time
- incompatible only when active together on the same scope and time interval

---

## 4. Required pack declarations

Every pack must declare at least:

- stable identifier
- version
- status
- steward/owner
- precedence class
- eligible scopes
- dependency list
- incompatibility/exclusion list
- touched constitutional surfaces
- declared compatibility policy where known
- governance status
- artifact inventory

### 4.1 Precedence classes
OFARM fixes these baseline precedence classes:

1. **jurisdiction / law / safety**
2. **certification / claim / contract**
3. **crop-system / biophysical context**
4. **tooling / method**
5. **local / community / preference**

### 4.2 Touched constitutional surfaces
A pack must declare which constitutional surfaces it touches, such as:

- controlled vocabularies and bindings
- archetypes/templates
- interaction specifications
- evidence policies
- validation rules
- decision/rule modules
- event-family subtypes
- views and Document Assemblies
- import/export mappings
- runtime API/event/query/discovery surface contracts
- advisory behavior

If a pack declares mapping or runtime-surface support, it should also declare the corresponding coverage/loss/contract artifacts so compatibility checking remains explainable.

This is required so compatibility checking is explainable rather than magical.

---

## 5. What packs may change

A pack may:

- activate scoped behavior
- narrow constraints
- add required evidence
- add event-family subtypes
- add context-specific attributes where allowed
- add validation and rule modules
- add views, Document Assemblies, mappings, and runtime surface contracts
- restrict or specialize workflows
- add pack-scoped terminology and code bindings
- define explicit compatibility/merge declarations for touched surfaces

---

## 6. What packs may not change

A pack may not:

- rewrite universal OFARM core meaning
- rewrite the Alignment Register by local force
- change the truth model
- change the twin law
- change the fixed top-level event families
- change the commit classes by private interpretation
- bypass provenance, evidence, review, or audit rules
- weaken constitutional anti-goals
- silently shadow another pack’s artifact without declaration
- silently override a higher-precedence requirement
- invent undeclared merge behavior

---

## 7. Compatibility classes

OFARM uses these pack-level compatibility classes:

### 7.1 COMPATIBLE
The packs may be active together at the same scope/time without special conditions.

### 7.2 COMPATIBLE_WITH_DECLARED_MERGE
The packs may be active together only because a declared merge policy exists for the touched surfaces.

### 7.3 COMPATIBLE_BY_SCOPE_SEPARATION
The packs are compatible only when applied to different scopes or time intervals.

### 7.4 EXCLUSIVE
The packs may not be active together on the same scope/time.

### 7.5 GOVERNANCE_REQUIRED
No safe automatic determination exists yet.
Activation requires a governed compatibility decision before use.

---

## 8. Same-precedence conflict rule

When two active packs in the same precedence class touch the same constitutional surface in incompatible ways:

- if a declared safe merge policy exists, apply it
- otherwise hard fail activation for that PackActivationSet

OFARM does **not** use default ad hoc runtime human-choice prompts as the normal conflict strategy.

Reason:
- prompts create inconsistent installations
- hidden manual choices destroy reproducibility
- deterministic composition matters more than convenience

Governed override is allowed, but only through an explicit compatibility artifact or decision, not an ephemeral click.

---

## 9. Cross-precedence rule

When packs conflict across precedence classes:

- higher precedence wins
- lower precedence may still enrich where it does not contradict the higher one
- if the lower pack cannot operate meaningfully under that restriction, activation should fail rather than pretend compatibility

This means:
- law/safety beats certification convenience
- certification/claim beats crop-system preference when truly in conflict
- crop-system reality beats tooling/method preference
- tooling/method beats local preference

---

## 10. Deterministic failure behavior

When activation fails, the platform should produce a governed conflict result that at minimum states:

- the conflicting packs/profiles
- the affected scope/time
- the touched constitutional surface
- the precedence relationship
- whether a declared merge path exists
- what would be required to resolve it

Failed activation must not degrade into partial hidden activation.

---

## 11. Governed override path

Override is allowed only through explicit governance artifacts or decisions such as:

- approved compatibility declaration
- approved scoped conflict-resolution artifact
- approved narrowing profile
- approved pack revision

Override must itself become traceable OFARM truth.
It may not exist only in operator memory or runtime settings.

---

## 12. Minimum safe pack manifest fields

A v2-safe pack manifest should contain at least:

- id
- version
- status
- precedence class
- eligible scopes
- dependencies
- incompatibilities
- touched surfaces
- merge policies
- provided artifacts
- required reference snapshots where relevant
- signing/approval status where relevant

---

## 13. Why this structure is necessary

Without this policy, packs become the most likely source of future OFARM failure:

- semantic drift
- inconsistent farm behavior
- incompatible local overrides
- query instability
- impossible debugging
- non-reproducible compliance outcomes

This policy keeps packs modular without letting them become lawless.

---

## 14. Default safety bias

If OFARM lacks a declared safe answer, the default is:

- do not guess
- do not silently merge
- do not activate partially
- fail deterministically
- require explicit governance or revised pack design


## 15. Surface-specific merge semantics

This policy now adopts the surface-specific merge semantics defined by:

- **OFARM Pack Merge Semantics RFC v0.1**

### 15.1 Covered baseline surface families
- VOCABULARY_BINDINGS
- EVIDENCE_POLICY
- ARCHETYPE_DEFINITION
- TEMPLATE_CONSTRAINT
- VALIDATION_RULE
- DECISION_RULE
- EVENT_SUBTYPE_DEFINITION
- VIEW_SHAPING
- DOCUMENT_ASSEMBLY_SHAPING
- IMPORT_EXPORT_MAPPING
- RUNTIME_SURFACE_CONTRACT

### 15.2 Covered merge modes
- ADDITIVE_UNION
- CONSTRAINT_INTERSECTION
- STRONGEST_REQUIREMENT
- ORDERED_COMPOSITION
- IDENTICAL_ONLY
- HARD_FAIL

### 15.3 Runtime consequence
A declared safe merge is only valid if:
- the overlapping artifacts are in a covered surface family
- the chosen merge mode is legal for that family
- the runtime can explain the result through a PackMergeResolutionTrace or equivalent trace

Otherwise the system must fail or require governance.
