# OFARM External Standards Integration and Interoperability Policy v0.1

Date: 2026-04-10  
Status: active companion artifact  
Scope: classify external standards by governed role and define the boundary between semantic reuse, profile packaging, interoperability mappings, runtime surfaces, and portable attestations

---

## 1. Purpose

OFARM already reuses public standards where they are the best stewards of meaning.

The remaining problem is not whether OFARM should align externally.
The remaining problem is how OFARM admits external standards **without** letting them silently become:
- hidden constitutional law
- hidden runtime law
- hidden truth stores
- hidden governance decisions

This policy makes that boundary explicit.

---

## 2. Core principle

Every external standard or ontology used by OFARM must be admitted in one or more explicitly declared roles:
- **semantic anchor**
- **semantic profile**
- **exchange mapping**
- **runtime surface contract**
- **attestation wrapper**

A standard may appear in more than one role across different artifacts.
But each OFARM artifact must declare the role it is using.

OFARM does **not** accept “general external standard support” as a meaningful governance category.

---

## 3. Role definitions

### 3.1 Semantic anchor
A semantic anchor supplies reused meaning for a constitutional concept family or a governed extension concept family.

Admission rules:
- it must appear in a governed `SemanticSubstrateBundle`
- if it changes constitutional-core meaning, the corresponding concept must also be handled through the Alignment Register and any required baseline patch
- it may not override OFARM-owned truth, promotion, evidence, authority, or current-state law

### 3.2 Semantic profile
A semantic profile narrows, constrains, or specializes an admitted anchor for OFARM use.

Admission rules:
- it must be published as governed OFARM artifacts or packs/profiles
- it must declare touched surfaces
- it must use the existing OFARM pack/merge law
- it may not create an alternate operational truth model

### 3.3 Exchange mapping
An exchange mapping translates between OFARM and an external exchange or interoperability format.

Admission rules:
- it must be represented by an import/export mapping module
- it must publish a `MappingCoverageStatement`
- it must publish a `LossMap`
- it must declare the ingest/export promotion posture
- it may not silently auto-promote external payloads into accepted OFARM truth beyond what governed policy explicitly allows

### 3.4 Runtime surface contract
A runtime surface contract describes a partner-facing or tool-facing API, event, query façade, or discovery document.

Admission rules:
- it must be representable as a governed `RuntimeSurfaceContract`
- it must preserve the constitutional source-of-meaning rather than replace it
- it may reference service-description artifacts such as OpenAPI, AsyncAPI, or equivalent contracts
- it may expose query or event façades, but those façades do not become the constitutional query or event model

### 3.5 Attestation wrapper
An attestation wrapper is a boundary artifact for portable verification or signing.

Admission rules:
- it wraps governed OFARM outputs such as `DocumentAssembly`
- it does not become OFARM truth merely because it is signed or portable
- it does not replace OFARM authority, review, evidence, or promotion logic

---

## 4. Boundary rules

### 4.1 Alignment Register boundary
The Alignment Register records constitutional semantic core concepts.
It is **not** the place for:
- deployment-specific conformance claims
- runtime surface claims
- mapping coverage statements
- loss disclosures

Those belong in the conformance and interoperability artifacts.

### 4.2 Pack-law boundary
External profile packs, mapping packs, and runtime-surface packs remain subject to OFARM pack law.
They do not gain special override powers merely because they reference a public standard.

### 4.3 Truth boundary
NGSI-LD entities, EPCIS messages, ADAPT payloads, ISOXML files, EFDI flows, OpenAPI contracts, AsyncAPI contracts, and VC payloads are never canonical OFARM truth by default.
They are boundary surfaces that must resolve back to the OFARM canonical substrate.

### 4.4 Discovery boundary
Discovery is required for interoperability, but discovery artifacts do not constitute semantic law.
A discovery document may help a client find a manifest or runtime surface.
It may not redefine what OFARM means.

---

## 5. Default role map for current external-standard-readiness work

### 5.1 Semantic anchors and profile hubs
- **GeoSPARQL** — semantic anchor for geometry and spatial relations
- **OWL-Time** — semantic anchor for temporal structure and interval/instant relations
- **QUDT** — semantic anchor for quantity/unit semantics
- **SOSA/SSN** — semantic anchor for observation foundations
- **PROV-O** — semantic anchor for provenance foundations
- **AIM** — semantic-profile hub and agricultural alignment anchor
- **AGROVOC** — vocabulary bridge, not OFARM operational truth
- **EPPO Codes** — governed code-binding/profile surface
- **BBCH** — governed code-binding/profile surface

### 5.2 Exchange bindings and mappings
- **UCUM** — exchange binding for payload unit codes, not a replacement for QUDT semantics
- **ADAPT** — exchange mapping surface
- **ISOXML** — exchange mapping surface
- **EFDI / ISO 5231 flows** — exchange/runtime mapping surface
- **EPCIS / CBV** — traceability exchange mapping and profile surface

### 5.3 Runtime surface contracts
- **NGSI-LD** — runtime façade and mapping target, not the OFARM core model
- **OGC API Features / CQL2** — query/runtime façade surface, not the constitutional query contract
- **OpenAPI** — service-description surface for HTTP APIs
- **AsyncAPI** — service-description surface for event surfaces
- **`.well-known` discovery documents** — capability/runtime discovery surface

### 5.4 Attestation wrappers
- **W3C Verifiable Credentials** — optional boundary wrapper around governed OFARM outputs

---

## 6. Promotion rule for supporting research

A recommendation from supporting research is not ready for promotion into active OFARM law until it is expressed through the correct artifact family.

At minimum, promotion should provide whichever of these apply:
- `SemanticSubstrateBundle`
- semantic profile artifacts or packs
- import/export mapping modules
- `MappingCoverageStatement`
- `LossMap`
- `RuntimeSurfaceContract`
- `ConformanceClaimSet`
- a Capability Manifest reference path where relevant

---

## 7. Anti-drift rules

OFARM should refuse the following failure modes:
- “we support standard X” without saying whether X is an anchor, profile, mapping, runtime surface, or wrapper
- mapping packs that have no disclosed loss posture
- runtime APIs that become de facto governance decisions through undocumented behavior
- conformance claims that cannot be traced to tests and active artifact state
- external discovery/service-description documents that silently outrank the Constitution or Platform

---

## 8. Practical consequence

This policy does not require OFARM to standardize every external surface immediately.
It requires OFARM to admit them through the correct lane.

That is the controlled path from research into governed OFARM amendments.
