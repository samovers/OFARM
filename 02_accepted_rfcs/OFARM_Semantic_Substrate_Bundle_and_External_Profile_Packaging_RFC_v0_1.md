# OFARM Semantic Substrate Bundle and External Profile Packaging RFC v0.1

Date: 2026-04-10  
Status: accepted RFC extension  
Scope: formalize a version-pinned `SemanticSubstrateBundle` and define how external semantic profiles enter OFARM without reopening the constitutional core

---

## 1. Problem statement

RC2.1 already states that OFARM reuses a shared semantic substrate.
That is directionally correct.
It is not yet explicit enough for external-standard-readiness work.

The remaining gap is:
- the substrate is described as a prose list rather than a governed, version-pinned artifact
- validation backbones such as SHACL are implied but not packaged as part of the admitted substrate posture
- exchange bindings such as UCUM can matter operationally, but OFARM lacks a clear place to declare them without confusing them for semantic anchors
- external semantic profiles can be built today, but there is no single contract that says which substrate assumptions they depend on

This RFC closes that gap.

---

## 2. Core stance

### 2.1 The substrate must be version-pinned
The OFARM shared semantic substrate should be expressible as a governed machine-readable artifact: `SemanticSubstrateBundle`.

A `SemanticSubstrateBundle` does **not** replace the Alignment Register.
It packages the external dependencies that the active OFARM semantics and profiles depend on.

### 2.2 Semantic anchors, validation backbones, and exchange bindings are distinct
This RFC separates three different things that are often accidentally collapsed:
- **semantic anchors** — reused meaning
- **validation backbones** — profile/shape validation mechanisms
- **exchange bindings** — payload-side serialization or code-expression bindings

Example posture:
- GeoSPARQL, OWL-Time, QUDT, SOSA/SSN, PROV-O, AIM-related modules, and governed agricultural vocabularies can appear as anchors or profile hubs
- SHACL is the baseline validation backbone for RDF-grounded semantic profiles
- UCUM may be declared as an exchange binding for payload interoperability without replacing QUDT semantics

### 2.3 External semantic profiles are OFARM-governed packs/profiles
This RFC does **not** create a second profile system.
External semantic profiles remain normal OFARM packs/profiles that:
- declare touched surfaces
- remain subject to pack precedence and merge law
- may constrain or specialize admitted anchors
- may not rewrite OFARM-owned truth, promotion, evidence, authority, or current-state law

---

## 3. Formal artifacts produced by this RFC

This RFC defines:
- **OFARM SemanticSubstrateBundle schema v0.1** (`ofarm.semanticsubstratebundle.v0.1`)
- **OFARM SemanticSubstrateBundle example core profile v0.1**

It does not add a new pack-manifest schema because external semantic profiles should reuse the existing OFARM pack/profile machinery.

---

## 4. SemanticSubstrateBundle schema decisions

### 4.1 Mandatory top-level fields
A valid `SemanticSubstrateBundle` should include at minimum:
- `schemaVersion`
- `bundleId`
- `status`
- `ofarmVersion`
- `publishedAt`
- `alignmentRegisterVersionRef`
- `semanticAnchors`
- `validationBackbones`

### 4.2 Semantic anchor entries
Each semantic anchor entry should declare at minimum:
- `anchorRef`
- `role`
- `versionPin`

Optional profile references may narrow or specialize an anchor for OFARM use.

### 4.3 Validation backbone entries
A validation backbone entry should declare:
- `standardRef`
- `usage`
- `versionPin`

This keeps semantic-profile validation explicit rather than hidden in implementation folklore.

### 4.4 Exchange bindings
Exchange bindings are optional in the bundle.
When declared, they should identify:
- the bound standard or code system
- the usage role
- the runtime surfaces or mappings that rely on it

This is the right place to say “payloads use UCUM codes for declared mapping surfaces” without pretending UCUM is the semantic source of truth.

---

## 5. Packaging rules for external semantic profiles

An external semantic profile pack or profile should:
- reference the `SemanticSubstrateBundle` it assumes
- declare the specific touched pack surfaces it modifies
- declare any required SHACL/profile validation artifacts
- declare code bindings and vocabulary bindings explicitly
- avoid importing large external ontologies wholesale when OFARM only needs a stable constrained subset

An external semantic profile pack should **not**:
- silently rewrite an OFARM-owned concept family
- publish an alternate current-state truth model
- bypass pack merge law by claiming external authority
- treat runtime surface documentation as semantic source-of-meaning

---

## 6. Why this patch is needed now

Without a `SemanticSubstrateBundle`, OFARM standard-readiness work will drift into one of two bad patterns:
- every deployment quietly depends on a different unrecorded external substrate
- the Capability Manifest starts carrying too much semantic dependency detail because no better grounding artifact exists

This RFC prevents both.

---

## 7. Main patch consequences

If promoted, this RFC implies:
- a narrow Constitution patch recognizing `SemanticSubstrateBundle`
- a Constitution clarification that SHACL-style validation belongs in substrate/profile packaging rather than hidden implementation behavior
- a Platform/Capability path that can ground semantic conformance without bloating the manifest
- no reopening of the constitutional source-of-meaning method

---

## 8. Hard stop question

Should OFARM admit a semantic dependency into active readiness work if it cannot be pinned in a `SemanticSubstrateBundle` and traced to a governed profile or alignment decision?

This RFC’s answer is **no**.
