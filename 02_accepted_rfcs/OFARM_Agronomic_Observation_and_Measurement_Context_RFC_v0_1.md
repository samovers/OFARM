# OFARM Agronomic Observation and Measurement Context RFC v0.1

Date: 2026-05-12  
Status: accepted post-charter RFC  
Scope: create the smallest active carrier closure for agronomic observation context and measurement evidence, without replacing NarrativeObservation, changing truth law, or importing a full agronomy ontology

---

## 1. Problem statement

The active package already has strong truth, event, evidence, promotion, and materialization law.
It can preserve:

- narrative local observations
- assertion records
- evidence sufficiency cases
- current-state materialization basis
- advisory/compliance twin separation
- high-consequence freshness and refusal/review behavior

That is necessary but not sufficient for field agronomy.

A scouting note, sample, lab result, sensor reading, image interpretation, or pest/weed/disease observation may later drive a recommendation, prescription, treatment, dispute, certification statement, or buyer-facing output.
If the record only says that something was observed, OFARM cannot reliably reconstruct:

- what agronomic phenomenon was observed
- when and where it was observed
- which crop cycle and crop stage it related to
- which method, sampling support, sensor, lab method, calibration, threshold, or uncertainty was involved
- whether the evidence is complete enough for high-consequence promotion

The Phase 0/1 agronomic amendment lane and the Deep Research intake both point to the same narrow closure: add small OFARM-owned carrier shells for agronomic observation context and measurement evidence, while external standards remain anchors and bindings rather than replacement truth.

---

## 2. Core stance

### 2.1 Small carriers, not a greenfield agronomy model

This RFC does not create a full agronomic ontology, a new truth substrate, or a separate observation platform.
It adds two bounded machine-contract families:

- `AgronomicObservationContext`
- `MeasurementEvidence`

These carriers provide structured context around observations and measurements so existing OFARM promotion, evidence, materialization, query, and output law can make better decisions.

### 2.2 NarrativeObservation remains valid

`NarrativeObservation` remains the correct OFARM-owned carrier for rich human field knowledge.
It must not be flattened into scalar measurements.

`AgronomicObservationContext` may reference a `NarrativeObservation`, but it does not replace it.
A narrative-only record may remain advisory-supporting evidence even when it is not strong enough for high-consequence compliance or execution promotion.

### 2.3 Evidence remains evidence, not truth

`MeasurementEvidence` represents sampled, measured, sensed, lab-derived, interpreted, or imported evidence.
It may support an assertion, review decision, recommendation, or evidence sufficiency case.
It does not by itself create accepted observation state, compliance truth, accepted execution, or current-state materialization.

### 2.4 External standards are anchors and bindings

The carrier shapes align to existing standards roles:

- O&M and SOSA/SSN for observations, samples, procedures, sensors, and results
- OWL-Time for instants and intervals
- GeoSPARQL-style discipline for spatial references and geometry basis
- PROV-O-style discipline for provenance
- QUDT and UCUM for quantity kinds and unit codes
- BBCH, EPPO, AGROVOC, Crop Ontology, and jurisdictional registries through scheme-bound references where relevant

This RFC does not make AIM, O&M JSON, ADAPT, ISOXML, EFDI, or any external runtime file format the canonical OFARM wire format.

### 2.5 High-consequence promotion stays governed

The default OFARM rule remains unchanged:

- weak or degraded observation context may support weaker classes
- stronger promotion requires the declared promotion path, evidence sufficiency, authority, and review where applicable
- missing method, unit, threshold, calibration, sample support, crop stage, or geometry basis must block, downgrade, or route high-consequence use to review according to policy

---

## 3. New active contract families

This RFC creates these active machine-contract families in `03_machine_contracts/`:

- `OFARM_AgronomicObservationContext_schema_v0_1.json`
- `OFARM_MeasurementEvidence_schema_v0_1.json`

It also adds package-local examples and implementation/conformance fixtures proving that:

- structured scouting context can remain advisory unless promoted through the right path
- sample collection without a result is retained without becoming nutrient-status truth
- qualified lab results such as below-LOQ results are not coerced into false exact values
- sensor results carry calibration and method context
- narrative-only context remains usable but blocked for high-consequence automatic promotion

---

## 4. AgronomicObservationContext minimums

An `AgronomicObservationContext` must be able to carry at least:

- stable context identifier
- context state
- observation class
- subject and target scope
- observed property reference
- phenomenon time or interval
- observer, sampler, sensor, or imported-system reference
- spatial context, including scope and optional partial extent / geometry basis
- procedure or method reference
- evidence references
- context completeness posture
- promotion-use posture

It may also carry:

- narrative observation reference
- crop cycle reference
- crop-stage / phenology binding
- target organism bindings
- crop/species/variety bindings
- part evaluated
- severity or pressure statement
- threshold reference
- environmental context references
- measurement evidence references
- confidence or uncertainty statement
- related recommendation or planned-intervention references
- reference snapshot references

### 4.1 What it must not do

`AgronomicObservationContext` must not:

- become current-state truth merely because it exists
- become a recommendation, prescription, plan, operation claim, or accepted execution
- bypass EvidenceSufficiencyCase, review, authority, or materialization freshness rules
- imply exact spatial or biological certainty where the context is estimated, degraded, provisional, or disputed

---

## 5. MeasurementEvidence minimums

A `MeasurementEvidence` record must be able to carry at least:

- stable evidence identifier
- evidence class
- observed property reference
- result time
- result kind and result payload
- source reference
- provenance references
- evidence status

When numeric, the result must carry both:

- quantity-kind reference
- unit reference

It may also carry:

- sample reference
- observation context reference
- sampling protocol reference
- measurement method reference
- sensor, sampler, instrument, or lab context
- calibration reference
- detection or quantification limit
- uncertainty
- chain-of-custody posture
- original payload reference or hash
- degradation reasons
- upgrade/supersession relation

### 5.1 What it must not do

`MeasurementEvidence` must not:

- silently replace the original reported value with only a normalized value
- coerce censored results such as below-LOQ into zero
- auto-promote to compliance truth
- smuggle model-derived advice into evidence fact
- erase earlier weak evidence when later stronger evidence arrives

---

## 6. Relationship to existing active law

### 6.1 Relationship to NarrativeObservation

`NarrativeObservation` continues to preserve human narrative.
`AgronomicObservationContext` supplies structured context around an observation when that context is needed for promotion, evidence sufficiency, query reconstruction, or output basis.

### 6.2 Relationship to EvidenceSufficiencyCase

`EvidenceSufficiencyCase v0.2` remains the active sufficiency gate for degraded and late evidence.
This RFC does not require a `v0.3` evidence sufficiency schema.

Measurement-specific degradation reasons may be carried inside `MeasurementEvidence`; an evidence sufficiency case may then use existing `v0.2` reason codes such as:

- `MISSING_REQUIRED_EVIDENCE`
- `MISSING_NORMALIZED_INTERPRETATION`
- `BASIS_NOT_RETAINED`
- `TIMESTAMP_INCOMPLETE`
- `SOURCE_QUALITY_LOW`
- `CONFLICTING_EVIDENCE`

If pilots show that measurement-specific insufficiency reason codes are needed inside `EvidenceSufficiencyCase`, that should be a later narrow `v0.3` patch.

### 6.3 Relationship to current-state materialization

Observation and measurement carriers may feed current-state materialization only through accepted assertions, accepted event consequences, review decisions, and declared evidence sufficiency paths.
They do not create current state directly.

### 6.4 Relationship to packs and code bindings

Packs may constrain method, code-list, threshold, and reference-snapshot expectations for these carriers.
They may not redefine what the carriers mean or weaken the core separation between evidence, observation context, advisory output, accepted truth, and current state.

---

## 7. Conformance expectation

A package or implementation claiming this RFC must show at least:

1. schema validation for both new contracts
2. positive examples for scouting, sample pending result, qualified lab result, calibrated sensor measurement, and narrative-only degraded context
3. negative checks proving required identifiers and numeric quantity/unit semantics cannot be omitted
4. a measurement-context dispute fixture where missing method, calibration, threshold, unit, or sample support blocks or downgrades high-consequence use
5. retained provenance for original values, normalized values, and late upgrades where present
6. no direct path from observation context or measurement evidence to accepted execution or compliance fact

---

## 8. Out of scope

This RFC does not:

- create the quantity-bearing intervention/as-applied carrier
- create the partial extent / geometry-basis carrier
- create the agronomic code-binding profile
- modify baseline law text directly
- adopt AIM or O&M JSON as OFARM's canonical runtime format
- create a global confidence scoring engine
- make every narrative observation require a full structured agronomic context record

Those remain separate follow-on closures.

---

## 9. Outcome

After this RFC:

- OFARM has active machine contracts for agronomic observation context and measurement evidence
- high-consequence observation-driven decisions can require explicit method, sampling, unit, threshold, confidence, and evidence context
- weak narrative observations remain preservable without being over-promoted
- measurement context can block false precision rather than being buried in prose
- Phase 3 quantity-bearing intervention, partial extent, code-binding, and query/output reconstruction work can build on these carriers without reopening truth law
