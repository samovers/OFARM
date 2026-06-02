# OFARM Capability Manifest RFC v0.1

Date: 2026-04-08  
Status: accepted post-charter RFC  
Scope: formalize the Capability Manifest as a machine-readable runtime self-description contract and define how it relates to registries and active artifact state

---

## 1. Problem statement

RC2 and the Platform baseline already say:
- Capability Manifest is a v2 must
- the platform should expose machine-readable self-description
- package/registry runtime exists
- activation and approval trace exists

That is directionally right.
It is not yet a usable contract.

The missing questions are:
- what exactly is a Capability Manifest
- which fields are mandatory
- how it relates to the artifact/package registry
- how it relates to active pack/profile/artifact state
- how tools compare two deployments
- how conformance claims are attached without turning the manifest into another ontology blob

This RFC closes that gap.

---

## 2. Core stance

### 2.1 Capability Manifest is a contract, not an ontology
The Capability Manifest should be:
- machine-readable
- comparable
- stable enough for tooling and integration
- narrow enough to stay useful

It should not become a second runtime ontology of everything.

### 2.2 Deployment self-description, not wish list
A manifest describes what a deployment or tenant **actually supports**, not every future feature the vendor hopes to add.

### 2.3 Registry relation is explicit
A manifest is not just a static brochure.
It must point to:
- the registry context in which it lives
- the active artifact set that grounds its claims

Without that, compatibility claims remain hard to verify.

---

## 3. Formal artifact produced by this RFC

This RFC creates:

- **OFARM Capability Manifest schema v0.1** (`ofarm.capabilitymanifest.v0.1`)

Example manifests included:
- core deployment example
- partner/tenant deployment example

Schema and example manifests were validated against JSON Schema draft 2020-12.

---

## 4. Capability Manifest schema decisions

### 4.1 Mandatory top-level fields
A valid Capability Manifest must include:
- schemaVersion
- manifestId
- ofarmVersion
- platformVersion
- publishedAt
- deploymentScope
- capabilitySections
- registryRelation
- conformance

### 4.2 Why these are mandatory
Without these fields:
- the manifest is not stably identifiable
- the compatibility target is unclear
- the runtime scope is unclear
- the claims are ungrounded in registry/activation reality
- the conformance level is opaque

### 4.3 Deployment scope
The manifest is scoped to:
- a deployment, or
- a tenant

This avoids pretending one giant global manifest always describes every runtime situation.

### 4.4 Capability sections
The baseline section set is:

- artifactSupport
- packSupport
- querySupport
- eventSupport
- authoritySupport
- importExportSupport
- enforcementSupport

This is enough to support:
- tooling
- integration planning
- compatibility comparison
- declared-conformance checks

without over-expanding the manifest.

### 4.5 Registry relation
The manifest now explicitly declares a **registryRelation** including:
- manifestRegistryRef
- artifactRegistryRef
- activeArtifactSetRef
- discoveryVisibility

This is the key missing bridge between:
- a deployment’s self-description
- the artifact/package registry
- the actual currently active state that grounds the description

### 4.6 Conformance section
The manifest now carries a minimal conformance block including:
- minimumConformanceLevel
- optional testSuiteRefs
- optional declaredProfileRefs

This keeps self-description tied to actual verification posture rather than bare marketing language.

---

## 5. Why this schema is intentionally narrow

This RFC does **not** try to encode:
- every artifact detail
- every pack manifest detail
- every rule module detail
- every policy nuance
- every external profile claim

Those belong in:
- the artifact registry
- the activation state
- the conformance system
- future profile packages

The Capability Manifest should stay a top-level entry contract.

---

## 6. Registry relation model

### 6.1 manifestRegistryRef
Identifies where the manifest itself is registered or published.

### 6.2 artifactRegistryRef
Identifies the artifact/package registry that holds the governed artifacts the deployment depends on.

### 6.3 activeArtifactSetRef
Identifies the activation snapshot or artifact-set state that grounds the manifest’s capability claims.

This is crucial.
Without activeArtifactSetRef, a manifest might describe supported pack/runtime behavior without any trace to what is actually active.

### 6.4 discoveryVisibility
Distinguishes whether a manifest is:
- PRIVATE
- RESTRICTED
- PUBLIC

This allows registry/discovery posture without forcing every manifest to be publicly visible.

---

## 7. Compatibility and comparison meaning

A Capability Manifest should support at least these practical questions:

- does this deployment support the artifact types I need?
- does it support pack activation and the surface families I need?
- does it support the query schemas I need?
- does it support the event families / commit classes I expect?
- does it support the authority action classes and traces I depend on?
- does it expose the import/export surfaces I need?
- does it support the enforcement features I require?

This is why the manifest is useful:
it becomes a comparison target rather than just a prose document.

---

## 8. Main patch consequences

This RFC requires:
- Platform patching in section 13, glossary, and testability direction
- no Constitution patch required by default, because this is a runtime self-description contract rather than model law
- no Alignment Register patch required by default, because Capability Manifest is not a constitutional semantic core concept
- example manifests and compatibility fixtures

---

## 9. Hard stop question

The RFC succeeds only if a tool can answer:

**What does this deployment actually support, and what active registry/activation state makes that claim credible?**
