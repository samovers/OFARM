# OFARM Deep Research prompt — agronomic code binding and intervention context v0.1

Current in family: yes

Use this prompt before activating the agronomic code-binding profile or finalizing observation/intervention/extent carriers.

---

You are conducting Deep Research for the OFARM 2 project.

## Context

OFARM 2 is a crop-farming semantic reference model and platform architecture. It already has:

- assertion/history-first canonical truth
- governed current-state materialization
- Compliance Twin and Advisory Twin separation
- explicit event grammar and commit classes
- explicit authority, delegation, evidence, and promotion gates
- pack/profile law
- QuerySpecification and QueryPlanIR
- PassportView and DocumentAssembly separation
- runtime enforcement chain
- Capability Manifest
- active alignment to external standards rather than private reinvention

The active baseline must not be overwritten by research. Research may inform amendments only.

## Research objective

Identify the smallest standards-aligned agronomic amendment set needed for OFARM to support real crop-farming observations, recommendations, prescriptions, as-applied records, partial treatments, delayed contractor work, measurement evidence, and audit reconstruction.

## Focus areas

1. Agronomic observation context
2. Measurement and sampling context
3. Crop stage / phenology
4. Pest, weed, disease, and target-organism identity
5. Crop, variety, and seed-lot identity
6. Product/input identity for crop protection, fertilizer, seed, irrigation, and related interventions
7. Quantity, rate, dose, concentration, units, and unit-code handling
8. Partial spatial extent, treatment areas, sampled areas, damage areas, and geometry basis
9. As-applied and machine-work-record interoperability
10. Evidence quality, calibration, lab method, detection limit, uncertainty, and sampling protocol
11. Query/output reconstruction for audit, certification, buyer, and compliance use

## Standards and resources to investigate

Prefer official standards bodies, technical specifications, authoritative registries, and implementation documentation.

Investigate:

- AIM / agricultural information model references
- ADAPT
- ISOXML
- AEF / EFDI / machinery work-record standards
- SOSA/SSN
- OGC Observations and Measurements, if relevant
- QUDT
- UCUM
- GeoSPARQL
- OWL-Time
- PROV-O
- SKOS
- BBCH
- EPPO codes
- AGROVOC
- Crop Ontology
- SAREF4Agri
- jurisdictional or industry examples for pesticide/product identity, fertilizer/nutrient records, and seed/variety identifiers
- representative farm-management or precision-ag examples where as-applied and observation data are exchanged

## Important OFARM constraints

- Do not flatten OFARM into CRUD.
- Do not let projections become truth.
- Do not let AI or advisory outputs become compliance truth.
- Do not let packs mutate core meaning.
- Do not let stale current state drive high-consequence outputs.
- Do not create a huge agronomy ontology if a small carrier plus code-binding profile is sufficient.
- Preserve the distinction between recommendation, prescription, plan, operation claim, accepted execution, correction, outcome, and evidence.
- Research informs; the active baseline governs until explicitly amended.

## Required output

Prepare a research report with these sections.

### 1. Executive recommendation

State whether OFARM needs new baseline law, RFC extensions, machine contracts, conformance fixtures, or only supporting guidance.

### 2. Recommended minimum carriers

For each proposed carrier, provide:

- carrier name
- purpose
- minimum fields
- optional fields
- external standards alignment
- what it must not do
- which OFARM existing artifacts it should reference
- whether it belongs in core, pack/profile, or implementation conformance

### 3. Standards role map

For each relevant standard or code system, classify it as:

- semantic anchor
- code binding
- exchange mapping
- runtime surface
- attestation wrapper
- not recommended

### 4. Agronomic code-binding strategy

Recommend how OFARM should handle:

- crop species
- variety/cultivar
- seed lot
- crop stage
- pest
- weed
- disease
- target organism
- crop-protection product
- fertilizer/nutrient input
- unit and quantity kind
- sampling method
- measurement method
- threshold source

### 5. As-applied and intervention strategy

Recommend minimum semantics for:

- recommendation
- prescription
- planned operation
- operation claim
- as-applied record
- accepted consequence
- correction
- disputed record

### 6. Measurement and evidence strategy

Recommend minimum semantics for:

- sampling protocol
- measurement method
- instrument/sensor
- calibration
- lab method
- detection limit
- uncertainty
- evidence source
- evidence degradation
- late evidence upgrade

### 7. Partial spatial extent strategy

Recommend minimum semantics for:

- sampled area
- treatment area
- failed pass
- re-treatment area
- replant area
- damage area
- disputed geometry
- when partial extent should and should not become a durable identity

### 8. Conformance scenario set

Provide at least 10 scenarios OFARM should use as fixtures.
Include expected pass/fail behavior for:

- promotion
- materialization
- query reconstruction
- PassportView
- DocumentAssembly

### 9. Risks and anti-patterns

Identify where OFARM could create fake precision, semantic drift, over-normalization, or hidden truth stores.

### 10. Source list

Cite all sources with dates accessed.
Flag any uncertain or unavailable claims.

## Output style

- concise but technically specific
- no greenfield redesign
- prioritize smallest controlled patches
- distinguish active-law recommendations from implementation/conformance recommendations
